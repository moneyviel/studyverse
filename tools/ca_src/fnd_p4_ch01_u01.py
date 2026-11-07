"""CA Foundation · Paper 4 Business Economics · Chapter 1 Nature & Scope of Business Economics · Unit 1 Introduction.
Original explanations, examples and questions (ICAI structure and scope only)."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch01-u01'


def Q(mid, q, opts, ans, ex, c, d='core', check=None):
    x = {'id': mid, 'q': q, 'options': opts, 'answer': ans, 'explain': ex, 'concept': c, 'difficulty': d}
    if check: x['check'] = check
    return x


def build():
    # ---------------- illustration 1: choice and opportunity cost ----------------
    c1 = Checks()
    gift = 3000
    opts = [('Weekend trip with friends', 3000, 90), ('Noise-cancelling headphones', 3000, 80), ('Coaching test series', 3000, 85)]
    best = max(opts, key=lambda o: o[2])
    second = sorted(opts, key=lambda o: -o[2])[1]
    oc_score = c1.add('85', 'satisfaction score of the next best option (coaching test series)')

    # ---------------- illustration 2: accounting vs economic view of a decision ----------------
    c2 = Checks()
    rev = 1800000; raw = 700000; wages = 420000; rent = 180000
    acc_cost = c2.add('700000+420000+180000', 'explicit (recorded) costs')
    acc_profit = c2.add('1800000-1300000', 'accounting profit')
    own_sal = 360000; own_int = 120000
    implicit = c2.add('360000+120000', 'implicit costs: salary given up + interest given up')
    eco_profit = c2.add('500000-480000', 'economic profit')

    # ---------------- illustration 3: classify issues micro / macro ----------------
    issues = [['Fixing the selling price of a new soap', 'Micro — product pricing', 'Internal (operational)'],
              ['Forecasting next year\'s demand for the firm\'s scooters', 'Micro — demand analysis and forecasting', 'Internal (operational)'],
              ['Choosing between a labour-heavy and a machine-heavy method', 'Micro — production and cost analysis', 'Internal (operational)'],
              ['Effect of a rise in the repo rate on loan costs', 'Macro — interest rates / monetary policy', 'External (environmental)'],
              ['Impact of a recession on sales across the economy', 'Macro — business cycle', 'External (environmental)'],
              ['Rupee weakening against the dollar for an importer', 'Macro — external value of currency', 'External (environmental)']]

    # ---------------- case set ----------------
    k = Checks()
    k_rev = 2400000; k_exp = 1650000
    k_accp = k.add('2400000-1650000', 'accounting profit of the bakery')
    k_imp = k.add('540000+90000', 'implicit costs: salary + interest foregone')
    k_ecop = k.add('750000-630000', 'economic profit of the bakery')

    concepts = [
        {'id': 'c1', 'title': 'What a business is, and the choices it must make',
         'body': ['Every business — a factory, a farm, a bank, a hospital, a transport company — takes inputs (land, labour, capital and entrepreneurship, or in plain words men, materials, machines and management) and turns them into outputs: goods and services. The aim is to add net value: the output should be worth more than the inputs used up.',
                  'Outputs are of many kinds: consumer goods and producer (capital) goods, private goods and public goods, merit goods (things society wants more of, such as vaccination or schooling) and non-merit goods (such as tobacco), durable goods and single-use goods.',
                  'Most enterprises aim at a surplus or profit; non-profit organisations aim at social benefit. Both must decide what to produce, when, for whom and why; a finance business must decide when to raise money, where to use it and on what terms. Every such decision is a choice among alternatives — and economics is the discipline that helps judge whether a choice is rational and optimal.'],
         'analogy': 'A business is a kitchen: raw ingredients go in, a meal comes out, and the cook keeps deciding what to cook, for whom and with which ingredients.',
         'work': 'When a CA prepares a project report for a bank loan, the first pages answer exactly these questions — what will be produced, for which customers, with what inputs and at what margin.'},
        {'id': 'c2', 'title': 'What economics is about: unlimited wants, scarce means',
         'body': ['Two facts create the subject: human wants are unlimited, and the means to satisfy them are relatively scarce and have alternative uses. Because we cannot have everything, we must choose — and every choice means giving up something else.',
                  'Economics studies how a society allocates its relatively scarce resources among competing wants, so that resources go to their highest-valued uses, and how the resulting goods and services are shared out.',
                  'The scarcity-and-choice view is the core of modern (neo-classical) microeconomics, but it is incomplete. Economics also studies how productive capacity grows over time (more and better workers, new resources, better technology) and why economies sometimes slump, leaving factories and workers idle for lack of demand (as during the 2008 global financial crisis or the pandemic years).',
                  'The word comes from the Greek "oikonomia" (management of a household). Until the nineteenth century the subject was called political economy; Adam Smith\'s "The Wealth of Nations" (1776) is treated as the first modern work of economics.',
                  'Economics gives an analytical approach and models for choosing the best course of action, but real problems also have political and social roots — economics will not solve every problem, though it helps us see each one in the right perspective.'],
         'analogy': 'A monthly salary is like a fixed-size pizza and your wants are a crowd of hungry friends. Economics is the art of slicing it so that the most important hunger is met first.',
         'work': 'Budgeting in any company — capital budget, marketing budget, staffing plan — is an exercise in allocating scarce funds among competing departments. CAs who prepare budgets are applying this idea every day.'},
        {'id': 'c3', 'title': 'Meaning and definition of Business Economics',
         'body': ['Business decisions — enter a market or not, which technology to use, make or buy a component, what price to charge, how much to spend on marketing, how to handle risk — are hard because the environment is complex, changing and uncertain, and information is imperfect.',
                  'Decision making means choosing, from two or more alternatives, the one that reaches a desired goal most efficiently. It involves listing feasible alternatives, judging them rationally on the information available, and choosing. Choice arises only because resources are limited and have alternative uses.',
                  'Business Economics (also called Managerial Economics) is the use of economic analysis to make business decisions about the best use of an organisation\'s scarce resources. Joel Dean described it as the use of economic analysis in formulating business policies. In short, it integrates economic theory with business practice — it is applied economics that bridges the gap between theory and practice.',
                  'It draws on economic theory (micro and macro), operations research, statistics, mathematics and decision theory, and uses quantitative tools — regression, linear programming, break-even and cost analysis, capital budgeting. It is useful not only to profit-seeking firms but also to managers of not-for-profit organisations such as NGOs.'],
         'analogy': 'Economic theory is a road map; Business Economics is the GPS that uses the map to choose the best route for one particular car on one particular day.',
         'work': 'A CA advising on "make or buy", pricing a new product, or evaluating an expansion is doing Business Economics — comparing costs and benefits of alternatives under uncertainty.'},
        {'id': 'c4', 'title': 'Microeconomics and macroeconomics',
         'body': ['Microeconomics studies individual units — consumers, firms, a particular industry — and how each allocates its scarce resources. Its main areas: how a product\'s price is set, how consumers behave, how factors (labour, land, capital) are priced, how firms behave, where industries locate, and the economic condition of a particular group of people. It looks at the trees, not the forest.',
                  'Macroeconomics studies the economy as a whole and its large aggregates: national income and output, the general level of prices, interest rates, balance of trade and of payments, the external value of the currency, total saving and investment, how many people have jobs and how fast the economy grows. These aggregates are the combined result of millions of individual decisions.',
                  'Business Economics is mainly microeconomic, but macroeconomics matters too: inflation, interest rates, government policy and the stage of the business cycle shape every firm\'s results, and long-run business trends are set by macro factors.'],
         'blocks': [table(['Basis', 'Microeconomics', 'Macroeconomics'], [
             ['Unit of study', 'An individual consumer, firm or industry', 'The whole economy'],
             ['Typical questions', 'Price of a product, a firm\'s output, wages in one industry', 'National income, inflation, unemployment, growth'],
             ['Typical tools', 'Demand, supply, cost and market analysis', 'Aggregate demand, money supply, fiscal and monetary policy'],
             ['Use in business', 'Internal (operational) decisions', 'Understanding the external environment']], title='Micro vs macro at a glance')],
         'analogy': 'Microeconomics studies one shop in the market; macroeconomics studies the weather over the whole city — both affect whether the shop does well.',
         'work': 'In an audit, going-concern review looks at the client\'s own costs and prices (micro) and also at interest rates, demand slowdown and currency moves (macro).'},
        {'id': 'c5', 'title': 'Nature of Business Economics',
         'body': ['Economic theories rest on simplifying assumptions, so there is a gap between theory and the messy real world. Business Economics applies economic logic and tools to close that gap. Its nature can be summed up in eight features:',
                  'Science — a systematic body of knowledge that sets out cause-and-effect relationships; it combines decision sciences (mathematics, statistics, econometrics) with economic theory and tests its results empirically. Based on microeconomics — its main concern is the decision problems of the individual firm. Incorporates macro analysis — the firm works inside an economy whose price level, income, employment and government policies (tax, interest, exchange rate, prices, wages, monopoly control) affect it.',
                  'Art — it is the practical application of rules and principles to reach set goals. Market and private-enterprise based — it applies the theory of the firm and of allocating resources in an economy run mainly by private enterprise. Pragmatic — unlike abstract micro theory built on unrealistic assumptions, it tackles real practical problems. Interdisciplinary — it borrows from mathematics, operations research, management, accounting, marketing, finance, statistics and econometrics.',
                  'Normative — positive economics describes "what is" without value judgements; normative economics prescribes "what ought to be" and carries value judgements and welfare considerations. Business Economics is mainly normative (it recommends decisions and policies), but sound prescriptions need a correct description of the environment, so it combines both, with the emphasis on the normative side.'],
         'blocks': [table(['Positive statement (what is)', 'Normative statement (what ought to be)'], [
             ['Petrol prices rose 8% this year.', 'The government should cut tax on petrol.'],
             ['A 10% price cut raised our sales by 15%.', 'We ought to cut our price to grow market share.'],
             ['Higher interest rates reduce housing loans.', 'Banks should lower rates for first-time buyers.']], title='Positive vs normative')],
         'analogy': 'A doctor first diagnoses (positive: the fever is 102°F) and then prescribes (normative: you should take rest and this medicine). Business Economics is a prescribing doctor who never skips the diagnosis.',
         'work': 'A CA\'s management report has both parts: a factual analysis of numbers (positive) and recommendations to the board (normative).'},
        {'id': 'c6', 'title': 'Scope of Business Economics',
         'body': ['Business issues fall into two groups. Internal or operational issues arise inside the firm and are within management\'s control — they are handled with microeconomics. External or environmental issues arise outside the firm and are beyond its control — they are understood with macroeconomics.',
                  'Microeconomics applied to operational issues: (1) demand analysis and forecasting — consumer behaviour, determinants of demand and prediction of future demand so that inputs can be arranged in time; (2) production and cost analysis — the input-output relation, optimum output, least-cost input mix and behaviour of costs as output, time and plant size change; (3) inventory management — rules (such as ABC analysis and simple models) to keep raw materials, work-in-progress and finished goods at minimum cost; (4) market structure and pricing policies — the extent of competition, the firm\'s market power and price policy; (5) resource allocation — tools like linear programming for best use of resources; (6) theory of capital and investment decisions — choosing projects and allocating scarce capital; (7) profit analysis — measuring and planning profits under uncertainty; (8) risk and uncertainty analysis — making efficient decisions when the future is uncertain.',
                  'Macroeconomics applied to environmental issues: the type of economic system; the stage of the business cycle; the general movement of national income, prices, employment, saving and investment; government policies (industrial, competition, fiscal, foreign trade, globalisation); the working of the central bank, financial sector and capital markets and their regulation; socio-economic organisations such as trade unions, producer and consumer associations and co-operatives; and the social and political environment. Since management cannot control these, it adapts its policies to soften their adverse effects.',
                  'Note: capital budgeting, risk and uncertainty analysis, inventory control, resource allocation and product/promotion policy are only listed here; they are studied in detail in later CA papers such as Financial Management and Strategic Management.'],
         'analogy': 'Steering and the engine are inside the car (operational, micro); road conditions and traffic rules are outside (environmental, macro). A good driver manages the first and adapts to the second.',
         'work': 'A CFO\'s annual plan has a section on internal levers (pricing, costs, capacity, inventory) and another on external assumptions (GDP growth, inflation, interest rates, exchange rate). That split is exactly the scope of Business Economics.'},
        {'id': 'c7', 'title': 'Economics vs Business Economics',
         'body': ['Economics is the broad subject; Business Economics is its applied branch focused on decisions of a particular firm.'],
         'blocks': [table(['Basis', 'Economics', 'Business Economics'], [
             ['Meaning', 'Develops (frames) economic principles', 'Applies those principles to business problems'],
             ['Character', 'Both micro and macro', 'Mainly micro'],
             ['Main task', 'Satisfying needs of individuals and entities', 'Sound decision making in a particular business'],
             ['Nature', 'Positive as well as normative', 'Normative (prescriptive)'],
             ['Scope', 'Wide', 'Comparatively narrow'],
             ['Branches', 'Has Business Economics as an applied branch', 'Is itself an applied branch of economics'],
             ['Concerned with', 'All theories — production, consumption, distribution', 'Mainly profit-related theory'],
             ['Analysis', 'Includes macro issues like growth, inflation, employment', 'Micro issues like demand, supply, cost and profit'],
             ['Concentration', 'Only the economic aspects of a problem', 'Economic and non-economic aspects of a business problem'],
             ['Assumptions', 'Built on assumptions', 'Some assumptions fail when applied in practice']], title='Distinction between Economics and Business Economics')],
         'analogy': 'Economics is medical science; Business Economics is clinical practice for one kind of patient — the business firm.',
         'work': 'Interview panels for CA industrial training often ask this distinction — it shows whether you see economics as a decision tool.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Scarcity, choice and opportunity cost', 'difficulty': 'core', 'minutes': 5,
         'q': f'Aarav receives {R(gift)} as a gift. Each of the following costs {R(gift)}, and he scores the satisfaction he expects out of 100: a weekend trip (90), noise-cancelling headphones (80), a coaching test series (85). (a) What is the economic problem he faces? (b) What will a rational Aarav choose, and what is the opportunity cost of that choice?',
         'solution': [table(['Option', 'Cost (₹)', 'Expected satisfaction (out of 100)', 'Rank'], [[o[0], o[1], o[2], i + 1] for i, o in enumerate(sorted(opts, key=lambda o: -o[2]))], title='Ranking the alternatives'),
                      p(f'(a) His wants (three items worth {R(9000)} in all) exceed his means ({R(gift)}), and the money has alternative uses — this is scarcity, which forces a choice.'),
                      p(f'(b) A rational chooser picks the alternative with the highest satisfaction: the {best[0].lower()} (score {best[2]}). The opportunity cost is the next best alternative given up — the {second[0].lower()} (score {oc_score}) — not the sum of all the options rejected.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Why a business economist looks beyond the books', 'difficulty': 'moderate', 'minutes': 8,
         'q': f'Riya leaves a job paying {R(own_sal)} a year to run her own printing unit. She invests her savings of {R(1000000)} that were earning 12% interest. In the first year, sales are {R(rev)}; raw material {R(raw)}, wages {R(wages)} and rent {R(rent)}. Compute (a) accounting profit, (b) economic profit, and (c) state what a business economist would advise.',
         'solution': [table(['Particulars', 'Amount (₹)'], [['Sales revenue', rev], ['Less: Raw material', raw], ['Less: Wages', wages], ['Less: Rent', rent], ['Accounting profit (a)', acc_profit]], title='Accounting view (explicit costs only)'),
                      table(['Implicit cost', 'Amount (₹)'], [['Salary given up', own_sal], ['Interest given up (12% of ₹10,00,000)', own_int], ['Total implicit cost', implicit]], num=[1], total=True, title='Costs the books do not show'),
                      p(f'(b) Economic profit = accounting profit − implicit costs = {R(acc_profit)} − {R(implicit)} = {R(eco_profit)}.'),
                      p('(c) The unit covers all its costs, including the income Riya gave up, so it earns a small economic (supernormal) profit and continuing is rational. Had economic profit been negative, the books would still have shown a healthy profit, yet she would have been better off in her old job — this is why economic analysis is used for decisions.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Placing business issues within the scope of Business Economics', 'difficulty': 'core', 'minutes': 5,
         'q': 'A two-wheeler company lists the issues below for its planning meeting. Classify each as a microeconomic (internal/operational) or macroeconomic (external/environmental) issue, naming the area.',
         'given': [ul([r[0] for r in issues])],
         'solution': [table(['Issue', 'Area of Business Economics', 'Type'], issues, title='Classification'),
                      note('Rule of thumb: if management can control it, it is operational and micro; if it comes from the economy or government and management can only adapt, it is environmental and macro.')]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Board asks: should we enter the packaged juice market?', 'role': 'CA in industry — business analyst at a food company',
         'situation': 'The CEO wants to launch packaged juices. Two directors object: competitors are strong and consumers are turning health-conscious.',
         'steps': ['Frame the decision as a choice among alternatives: enter now, enter later, or stay out and invest elsewhere.', 'Do demand analysis and forecasting: market size, growth, price sensitivity and changing tastes (micro, operational).',
                   'Do production and cost analysis: plant size, technology, least-cost input mix, break-even volume.', 'Study the market structure: number and strength of rivals and likely price war.',
                   'Scan the environment: inflation, interest rates, sugar-tax proposals, the business cycle (macro, environmental).', 'Compare the expected return with the return from the next best use of the same funds (opportunity cost) and recommend.'],
         'takeaway': 'A business decision uses micro tools for what the firm controls and macro scanning for what it does not.',
         'think': 'Which part of the analysis is positive and which part is normative?', 'answer': 'Measuring market size, costs and rivals\' shares is positive (what is); recommending "enter now" is normative (what ought to be done).'},
        {'id': 'j2', 'title': 'An NGO plans a mid-day meal kitchen', 'role': 'CA volunteering as finance adviser to an NGO',
         'situation': 'The NGO has a fixed grant and wants to feed as many children as possible while keeping quality.',
         'steps': ['Note that the goal is social benefit, not profit — but the resources are still scarce.', 'Compare kitchen options: central kitchen with machines vs several small kitchens with more staff (how to produce).', 'Cost each option per meal and choose the least-cost method for the required quality.', 'Plan for growth: keep part of the grant for equipment that raises capacity next year.'],
         'takeaway': 'Business Economics helps not-for-profit managers as much as profit-seeking ones, because scarcity applies to everybody.'},
        {'id': 'j3', 'title': 'Rupee depreciation hits an importer', 'role': 'Articled assistant preparing a management review',
         'situation': 'A client importing electronic parts has seen its margin fall after the rupee weakened.',
         'steps': ['Identify the issue as external (macro): exchange rate, outside management\'s control.', 'List adaptive actions within control: renegotiate prices, hedge foreign currency payables, source part of the input locally, revise selling prices.', 'Quantify the impact on cost per unit for the board.'],
         'takeaway': 'Management cannot change macro variables; it can only adjust its operational policies to soften their effect.'},
    ]

    mcqs = [
        Q('m1', 'The word "economics" is derived from the Greek word "oikonomia", which means:', ['Management of a household', 'Wealth of a nation', 'Study of markets', 'Political science'], 0, 'Oikonomia refers to household management.', 'c2'),
        Q('m2', 'Which book is regarded as the first modern work of economics?', ['The Wealth of Nations by Adam Smith (1776)', 'Principles of Economics by Alfred Marshall', 'The General Theory by J. M. Keynes', 'Das Kapital by Karl Marx'], 0, 'Adam Smith\'s 1776 book is generally treated as the starting point of modern economics.', 'c2'),
        Q('m3', 'Until the nineteenth century, economics was known as:', ['Political economy', 'Home science', 'Commerce', 'Social arithmetic'], 0, 'The older name of the subject was political economy.', 'c2'),
        Q('m4', 'The basic economic problem arises because:', ['Wants are unlimited and resources are scarce with alternative uses', 'Resources are unlimited', 'Wants are limited', 'Money is not available'], 0, 'Scarcity relative to unlimited wants, plus alternative uses of resources, forces choice.', 'c2'),
        Q('m5', 'If every resource had only one possible use, then:', ['The problem of choice would not arise for that resource', 'Scarcity would increase', 'Wants would become limited', 'Prices would rise'], 0, 'Choice is needed only because resources can be put to alternative uses.', 'c2', 'moderate'),
        Q('m6', 'Business Economics is also known as:', ['Managerial Economics', 'Welfare Economics', 'Public Economics', 'Development Economics'], 0, 'The two terms are used interchangeably.', 'c3'),
        Q('m7', 'Joel Dean defined Business Economics in terms of:', ['The use of economic analysis in formulating business policies', 'The study of national income', 'The study of wealth', 'The study of household budgets'], 0, 'Dean stressed the use of economic analysis in framing business policy.', 'c3'),
        Q('m8', 'Business Economics is best described as:', ['Integration of economic theory with business practice', 'Pure economic theory', 'Study of accounting standards', 'Study of the stock market only'], 0, 'It is applied economics that bridges theory and practice.', 'c3'),
        Q('m9', 'Which of the following is studied under microeconomics?', ['Product pricing', 'National income', 'General price level', 'Balance of payments'], 0, 'Product pricing is an individual-unit issue; the rest are aggregates.', 'c4'),
        Q('m10', 'Which of the following is a macroeconomic area?', ['External value of the currency', 'Consumer behaviour', 'Factor pricing', 'Location of an industry'], 0, 'The exchange rate concerns the economy as a whole.', 'c4'),
        Q('m11', 'Business Economics is mainly based on:', ['Microeconomics', 'Macroeconomics', 'Econometrics only', 'Public finance'], 0, 'Its focus is the decision problems of individual firms, so it relies mainly on micro tools.', 'c5'),
        Q('m12', 'Business Economics is called a science because:', ['It is a systematic body of knowledge establishing cause-and-effect relationships', 'It uses laboratories', 'Its laws are as exact as physics', 'It ignores data'], 0, 'It uses scientific method and tests results empirically.', 'c5'),
        Q('m13', 'Business Economics is called an art because it:', ['Applies rules and principles in practice to achieve set objectives', 'Is about painting', 'Has no principles', 'Is only descriptive'], 0, 'An art is the practical application of knowledge to reach goals.', 'c5'),
        Q('m14', '"The government ought to reduce GST on medicines." This statement is:', ['Normative', 'Positive', 'Neither positive nor normative', 'Microeconomic positive'], 0, '"Ought to" carries a value judgement — normative.', 'c5'),
        Q('m15', '"A 10% rise in bus fares reduced passengers by 4%." This statement is:', ['Positive', 'Normative', 'A value judgement', 'Prescriptive'], 0, 'It describes a fact that can be tested — positive.', 'c5'),
        Q('m16', 'Business Economics is primarily:', ['Normative, though it also uses positive analysis', 'Purely positive', 'Purely descriptive', 'Neither positive nor normative'], 0, 'It prescribes decisions (normative) but needs a correct description of the environment (positive).', 'c5', 'moderate'),
        Q('m17', 'Business Economics is pragmatic because:', ['It deals with practical problems faced by firms in the real world', 'It is purely abstract', 'It rests on unrealistic assumptions only', 'It avoids decision making'], 0, 'Pragmatic = practical, problem-solving.', 'c5'),
        Q('m18', 'Business Economics is interdisciplinary because it:', ['Draws tools from mathematics, statistics, accounting, finance, management and others', 'Studies only economics', 'Rejects other subjects', 'Is part of law'], 0, 'It integrates concepts from many disciplines.', 'c5'),
        Q('m19', 'Which of the following is an internal (operational) issue of a firm?', ['Choice of the least-cost technique of production', 'Stage of the business cycle', 'Government\'s fiscal policy', 'Trade union movements in the country'], 0, 'Technique choice is within management\'s control; the others are environmental.', 'c6'),
        Q('m20', 'External or environmental issues of a business are mainly studied with the help of:', ['Macroeconomics', 'Microeconomics', 'Cost accounting', 'Auditing'], 0, 'Environmental factors are economy-wide, so macro analysis applies.', 'c6'),
        Q('m21', 'Predicting future demand on the basis of past behaviour of its determinants is called:', ['Demand forecasting', 'Demand analysis', 'Inventory control', 'Profit planning'], 0, 'Forecasting predicts future demand; analysis studies present behaviour of demand.', 'c6'),
        Q('m22', 'ABC analysis is used in Business Economics for:', ['Inventory management', 'National income measurement', 'Demand forecasting', 'Fixing wages'], 0, 'It classifies stock items by value to control inventory cost.', 'c6'),
        Q('m23', 'Linear programming is a tool mainly used in:', ['Resource allocation', 'Measuring national income', 'Studying business cycles', 'Positive economics only'], 0, 'It helps find the best use of limited resources.', 'c6'),
        Q('m24', 'Which of the following is NOT a macroeconomic (environmental) factor for a firm?', ['The firm\'s own pricing policy', 'Stage of the business cycle', 'Working of the capital market', 'Social and political environment'], 0, 'Pricing policy is an internal decision.', 'c6', 'moderate'),
        Q('m25', 'Compared with Economics, Business Economics:', ['Has a narrower scope and is mainly micro in character', 'Has a wider scope', 'Is mainly macro in character', 'Is purely positive'], 0, 'It is an applied branch with narrower, mainly micro focus.', 'c7'),
        Q('m26', 'Which statement about Economics vs Business Economics is correct?', ['Business Economics considers non-economic aspects of business problems too', 'Economics is only normative', 'Business Economics deals with growth and inflation as its main concern', 'Economics is a branch of Business Economics'], 0, 'Economics concentrates on economic aspects only; Business Economics also weighs non-economic aspects.', 'c7', 'moderate'),
        Q('m27', 'The opportunity cost of a choice is:', ['The value of the next best alternative given up', 'The money spent', 'The sum of all alternatives rejected', 'Always zero for free goods bought'], 0, 'Only the single next-best alternative counts.', 'c2'),
        Q('m28', 'Riya\'s unit shows an accounting profit of ₹5,00,000; her salary given up is ₹3,60,000 and interest given up is ₹1,20,000. Her economic profit is:', ['₹20,000', '₹5,00,000', '₹1,40,000', '₹3,80,000'], 0, 'Economic profit = 5,00,000 − (3,60,000 + 1,20,000) = ₹20,000. ₹1,40,000 deducts only the salary; ₹3,80,000 deducts only the interest.', 'c3', 'moderate', '500000-(360000+120000)'),
        Q('m29', 'Which of these decisions is the most "strategic" (long-term) for a firm?', ['Whether the firm should be in this business at all', 'How many units to dispatch tomorrow', 'Which courier to use this week', 'Shift timing for today'], 0, 'Entering or exiting a business shapes the firm\'s long-term direction.', 'c3', 'moderate'),
        Q('m30', 'Business Economics uses the theory of the firm mainly in the setting of:', ['A private enterprise economy', 'A barter economy', 'A purely planned economy', 'A household'], 0, 'It largely uses the theory of markets and private enterprise.', 'c5'),
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
         'q': f'Kabir runs a café. Annual sales {R(k_rev)}; recorded expenses (materials, staff, rent, power) {R(k_exp)}. He left a job paying {R(540000)} a year and has invested {R(900000)} of his own savings, which could earn 10% elsewhere. (a) Compute accounting profit and economic profit. (b) Should he continue, from an economist\'s point of view? Show steps.',
         'model': [table(['Step', 'Working', 'Amount (₹)'], [['1. Accounting profit', '24,00,000 − 16,50,000', k_accp], ['2. Implicit costs', 'Salary 5,40,000 + interest 10% of 9,00,000 = 90,000', k_imp], ['3. Economic profit', '7,50,000 − 6,30,000', k_ecop]], title='Working'),
                   p(f'(b) Economic profit is positive ({R(k_ecop)}): revenue covers explicit costs and the income Kabir gave up, so continuing is rational. Accounting profit alone overstates his true gain.')],
         'scheme': [{'id': 's1', 'pt': 'Accounting profit = revenue − explicit costs', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'Identifies both implicit costs (salary and interest foregone)', 'm': 1.5, 'skill': 'concept'},
                    {'id': 's3', 'pt': 'Economic profit computed correctly', 'm': 1.5, 'skill': 'computation'}, {'id': 's4', 'pt': 'Conclusion based on economic profit', 'm': 1, 'skill': 'conclusion'}],
         'remarks': ['Most candidates compute accounting profit correctly but forget the interest on own capital.'], 'mistakes': ['Treating the whole ₹9,00,000 investment as a cost.', 'Concluding from accounting profit only.'], 'tips': ['Show a three-line working: accounting profit, implicit costs, economic profit.'], 'checks': k},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
         'q': 'Classify each statement as positive or normative and give the reason: (i) India\'s retail inflation was above 6% last month. (ii) The RBI should cut the repo rate to boost growth. (iii) Firms that advertise more tend to sell more. (iv) Our company ought to stop producing the loss-making model.',
         'model': [table(['Statement', 'Type', 'Reason'], [['(i)', 'Positive', 'States a fact that can be checked against data'], ['(ii)', 'Normative', '"Should" — a value judgement about policy'], ['(iii)', 'Positive', 'A testable cause-and-effect claim'], ['(iv)', 'Normative', '"Ought to" — a prescription for action']])],
         'scheme': [{'id': 's1', 'pt': '(i) positive with reason', 'm': 1, 'skill': 'application'}, {'id': 's2', 'pt': '(ii) normative with reason', 'm': 1, 'skill': 'application'}, {'id': 's3', 'pt': '(iii) positive with reason', 'm': 1, 'skill': 'application'}, {'id': 's4', 'pt': '(iv) normative with reason', 'm': 1, 'skill': 'application'}],
         'remarks': ['A testable claim is positive even if it turns out to be false.'], 'mistakes': ['Calling (iii) normative because it "sounds like advice".'], 'tips': ['Look for "should / ought / must" — signals of a value judgement.']},
        {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'core', 'pad': 'table',
         'q': 'A cement company faces these issues: (a) price to charge in a new state; (b) slowdown in construction across the country; (c) whether to buy a waste-heat power plant; (d) a hike in the policy interest rate; (e) how much stock of coal to hold; (f) a new competition law amendment. Classify each as operational (micro) or environmental (macro), naming the area of Business Economics.',
         'model': [table(['Issue', 'Type', 'Area'], [['(a)', 'Operational — micro', 'Market structure and pricing policy'], ['(b)', 'Environmental — macro', 'Stage of the business cycle'], ['(c)', 'Operational — micro', 'Capital and investment decision'], ['(d)', 'Environmental — macro', 'Monetary policy / interest rates (central bank)'], ['(e)', 'Operational — micro', 'Inventory management'], ['(f)', 'Environmental — macro', 'Government (competition) policy']])],
         'scheme': [{'id': f's{i+1}', 'pt': f'Issue ({"abcdef"[i]}) correctly classified with area', 'm': 1, 'skill': 'application'} for i in range(6)],
         'remarks': ['Naming the area earns the mark; "micro" alone is not enough.'], 'mistakes': ['Treating capital investment as macro because it involves money.'], 'tips': ['Ask: can management control it? Yes → operational/micro.']},
    ]

    viva = [
        V('v1', 'What is the central idea of economics?',
          'Economics arises because human wants are unlimited while the resources to satisfy them are scarce and have alternative uses. So we must choose, and economics studies how scarce resources are allocated among competing wants.',
          [P('p1', 'Wants are unlimited', 3, 'want unlimit|unlimited want|wants are unlimit|wants are endless|endless want|infinite want|want infinite|wants are infinite|wants never end'),
           P('p2', 'Resources are scarce / limited', 3, 'scarce|scarcity|limited resourc|resources are limit|resourc limit|resources are not enough|not enough resources|limited means|never end resourc limit|never end but resourc limit|never end resourc scarce'),
           P('p3', 'Resources have alternative uses, so choice is needed', 2, 'alternative use|many use|different use|several use|choice|choose|choosing', min=1),
           P('p4', 'Economics studies allocation of scarce resources among competing wants', 2, 'allocat|distribut|use of resourc|best use|how resources are used|competing', min=1)], 'c2'),
        V('v2', 'Define Business Economics.',
          'Business Economics, also called managerial economics, is the use of economic analysis to make business decisions about the best use of a firm\'s scarce resources. It integrates economic theory with business practice and so bridges the gap between theory and practice.',
          [P('p1', 'Use / application of economic analysis or theory', 3, 'economic analysis|economic theory|economic principle|economic tool|economic logic|economics'),
           P('p2', 'For business decision making', 3, 'decision|decid|business policy|business policies'),
           P('p3', 'Integrates theory with practice / bridges the gap', 3, 'integrat|bridg|gap|theory with practice|theory and practice|theory into practice|applied economics|applies', min=1),
           P('p4', 'Also called managerial economics / best use of scarce resources', 1, 'managerial|scarce resourc|best use|limited resourc', min=1)], 'c3'),
        V('v3', 'Distinguish between microeconomics and macroeconomics with an example of each.',
          'Microeconomics studies individual units such as a consumer, a firm or an industry, for example how the price of a product is set. Macroeconomics studies the economy as a whole and its aggregates, for example national income, inflation or unemployment.',
          [P('p1', 'Micro studies individual units (consumer, firm, industry)', 4, 'micro individual|micro single|micro one|micro particular|micro firm|micro consumer|micro unit|micro small|micro specific|individual unit micro'),
           P('p2', 'Macro studies the economy as a whole / aggregates', 4, 'macro whole|macro aggregate|macro entire|macro overall|macro total|macro national|macro economy whole|macro country'),
           P('p3', 'Correct examples (product price / national income, inflation, unemployment)', 2, 'price of a product|product pric|pricing|consumer behaviour|demand|firm output|wage', 'national income|inflation|unemploy|gdp|price level|balance of payment|growth|employment', min=1)], 'c4'),
        V('v4', 'Why is Business Economics said to be normative in nature? Is it purely normative?',
          'Business Economics is normative because it prescribes what ought to be done; it recommends decisions and policies and involves value judgements. But it is not purely normative, because sound advice needs a correct description of what is, so it also uses positive economics, with the emphasis on the normative side.',
          [P('p1', 'Normative = what ought to be / prescriptive / value judgement', 4, 'ought|should|prescri|value judg|recommend|advis|what must be'),
           P('p2', 'Not purely normative — also uses positive analysis', 4, 'not purely|not only normative|not wholly|not entirely|not completely|not just normative|combin|both positive|positive and normative|normative and positive|positive as well|uses positive|use positive|positive analysis', min=1),
           P('p3', 'Positive = what is / descriptive', 2, 'what is|describ|descriptive|facts|factual')], 'c5'),
        V('v5', 'What is the scope of Business Economics?',
          'The scope covers two groups of issues. Internal or operational issues are handled by microeconomics; they are within management control and include analysing and forecasting demand, production and cost analysis, managing inventory, pricing and market structure, resource allocation, capital and investment decisions, profit analysis and risk analysis. External or environmental issues are handled by macroeconomics; they are beyond the firm\'s control and include the economic system, the business cycle, national income, prices and employment trends, government policies and the financial sector.',
          [P('p1', 'Internal / operational issues — microeconomics', 4, 'internal micro|operational micro|micro internal|micro operational|internal issue micro|operational issue micro|operational problem micro|internal problem micro|within firm micro|inside firm micro|inside micro'),
           P('p2', 'External / environmental issues — macroeconomics', 4, 'external macro|environmental macro|macro external|macro environmental|external issue macro|environmental issue macro|environmental problem macro|external problem macro|outside firm macro|outside macro'),
           P('p3', 'Names at least two micro areas (demand forecasting, production and cost, pricing, inventory, capital, profit, risk)', 1, 'demand', 'cost|production', 'pric|market structure', 'inventor', 'capital|investment', 'profit', 'risk|uncertain', min=2),
           P('p4', 'Names at least one macro factor (business cycle, government policy, national income, inflation, financial sector)', 1, 'business cycle|trade cycle|government polic|fiscal|monetary|national income|inflation|prices|financial sector|capital market|economic system|central bank', min=1)], 'c6'),
        V('v6', 'Is Business Economics useful only for profit-making firms?',
          'No, it is not useful only for profit-making firms. Non-profit organisations such as NGOs also have scarce resources and must choose the best way to reach their goals, so the tools of Business Economics help their managers too.',
          [P('p1', 'No — not only profit-making firms', 4, 'no|not only|not just|not limited|as well|too', min=1),
           P('p2', 'Also useful for NGOs / not-for-profit organisations', 3, 'ngo|non profit|not for profit|nonprofit|non-profit|voluntary|charit|hospital|government'),
           P('p3', 'Because they too face scarcity and must choose', 3, 'scarce|scarcity|limited|choice|choose|decision|best use', min=1)], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Kabir\'s café — reading the numbers like an economist', 'difficulty': 'moderate',
              'case': (f'Kabir quit a job paying {R(540000)} a year to open a café. He put in {R(900000)} of savings that were earning 10% in fixed deposits. In the first year the café sold goods worth {R(k_rev)} and paid {R(k_exp)} for materials, staff, rent and power. '
                       'He is now debating whether to open a second outlet, keeping in mind that the RBI is expected to raise interest rates and that food inflation is high.'),
              'mcqs': [
                  Q('k1a', 'What is the accounting profit of the café?', [R(k_accp), R(k_ecop), R(k_rev), R(210000)], 0, f'24,00,000 − 16,50,000 = {R(k_accp)}. Accounting profit deducts explicit costs only.', 'c3', 'core', '2400000-1650000'),
                  Q('k1b', 'What is the economic profit of the café?', [R(k_ecop), R(k_accp), R(210000), R(660000)], 0, f'Implicit costs = 5,40,000 + 90,000 = {R(k_imp)}; 7,50,000 − 6,30,000 = {R(k_ecop)}. ₹2,10,000 deducts only the salary; ₹6,60,000 deducts only the interest.', 'c3', 'hard', '750000-(540000+90000)'),
                  Q('k1c', 'The expected rise in interest rates is, for Kabir, a(n):', ['External (environmental) issue analysed with macroeconomics', 'Internal issue analysed with microeconomics', 'Inventory decision', 'Purely normative statement'], 0, 'Interest rates are set by the central bank — outside Kabir\'s control.', 'c6', 'core'),
                  Q('k1d', '"Kabir should open the second outlet only if its expected economic profit is positive." This is:', ['A normative statement', 'A positive statement', 'A macroeconomic fact', 'Neither positive nor normative'], 0, '"Should" signals a prescription — normative.', 'c5', 'core'),
              ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch01', 'n': 1, 'title': 'Introduction',
        'outcomes': ['Explain what a business does, why scarcity forces choice, and what economics studies.', 'Define Business Economics and explain why it is called applied (managerial) economics.',
                     'Distinguish microeconomics from macroeconomics and positive from normative statements.', 'Describe the nature and scope of Business Economics, and distinguish it from Economics.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 35}, 'prereq': [],
                 'exam_tip': 'This unit is pure theory but yields easy MCQs: the eight features of the nature of Business Economics, internal vs external issues, and the Economics vs Business Economics table are asked repeatedly. Watch the words "should/ought" (normative).'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {'summary': ['Unlimited wants + scarce resources with alternative uses = economic problem → choice.', 'Business Economics (Managerial Economics) = economic analysis applied to business decisions; integrates theory and practice.',
                                 'Micro: individual units (pricing, consumer behaviour, factor pricing, firms, location). Macro: aggregates (national income, price level, interest, BoP, exchange rate, employment, growth).',
                                 'Nature: science, art, based on micro, uses macro, theory of markets and private enterprise, pragmatic, interdisciplinary, normative (with positive base).',
                                 'Scope: internal/operational issues (micro) — demand, production & cost, inventory, pricing, resource allocation, capital, profit, risk; external/environmental issues (macro) — economic system, business cycle, national trends, policies, financial sector, socio-economic organisations, social-political environment.'],
                     'remember': ['Oikonomia = household; Adam Smith, Wealth of Nations, 1776; old name "political economy".', 'Joel Dean: economic analysis in formulating business policies.', 'Positive = what is; normative = what ought to be.'],
                     'traps': ['Business Economics is mainly micro — but not exclusively; macro environment matters.', 'Opportunity cost is the next best alternative only, not all alternatives.', 'Inventory management, capital budgeting, risk analysis are named in the scope but studied in detail in later CA papers.']},
        'quickref': [{'k': 'Economic problem', 'v': 'Unlimited wants, scarce means, alternative uses'}, {'k': 'Business Economics', 'v': 'Economic theory + business practice = decision making'},
                     {'k': 'Micro areas', 'v': 'Product pricing, consumer behaviour, factor pricing, firms, location of industry'}, {'k': 'Macro areas', 'v': 'National income, price level, interest, BoP, exchange rate, saving-investment, employment, growth'},
                     {'k': 'Economic profit', 'v': 'Revenue − (explicit + implicit costs)'}, {'k': 'Nature (8)', 'v': 'Science, art, micro-based, macro-aware, market theory, pragmatic, interdisciplinary, normative'}],
        'viva': viva, 'cases': cases,
    }
