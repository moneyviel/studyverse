"""CA Foundation · Paper 4 Business Economics · Chapter 7 Public Finance · Unit 3 The Process of Budget Making: Sources of Revenue,
Expenditure Management and Management of Public Debt. Original explanations, numbers and questions; constitutional articles cited by number only."""
from lib import *
from ca_viva import P, ALT, V

UID = 'fnd-p4-ch07-u03'


def M(i, q, o, a, e, c=None, d='core', check=None, topic=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if topic: m['topic'] = topic
    if c: m['concept'] = c
    if check: m['check'] = check
    return m


def build():
    # ---- i1 deficits ----
    c1 = Checks()
    tax, ntax, rexp, intp, cexp, rec, dis, bor = 18000, 3500, 27800, 6200, 7400, 600, 900, 12200
    rr = c1.add('18000+3500', 'revenue receipts')
    rd = c1.add('27800-21500', 'revenue deficit')
    texp = c1.add('27800+7400', 'total expenditure')
    ndcr = c1.add('600+900', 'non-debt capital receipts')
    fd = c1.add('35200-(21500+1500)', 'fiscal deficit')
    pd = c1.add('12200-6200', 'primary deficit')
    sh = c1.add('round(6300/12200*100,2)', 'revenue deficit as % of fiscal deficit')
    cap = c1.add('1500+12200', 'total capital receipts')

    # ---- i3 FD as % GDP and debt ----
    c3 = Checks()
    fdp = c3.add('round(1600000/35000000*100,2)', 'FD % of GDP')
    pdp = c3.add('round((1600000-1250000)/35000000*100,2)', 'PD % of GDP')
    d26 = c3.add('19043590+674426', 'total debt 31 Mar 2026')
    d27 = c3.add('20770868+711182', 'total debt 31 Mar 2027')
    g = c3.add('round((21482050-19718016)/19718016*100,2)', 'growth in total debt %')
    ex = c3.add('round(711182/21482050*100,2)', 'external share 2027 %')

    # ---- questions ----
    q1 = Checks()
    q1rr = q1.add('41000+6500', 'RR')
    q1rd = q1.add('56900-47500', 'RD')
    q1te = q1.add('56900+15100', 'TE')
    q1nd = q1.add('1200+2300', 'NDCR')
    q1fd = q1.add('72000-(47500+3500)', 'FD')
    q1pd = q1.add('21000-(9800-800)', 'PD on net interest')
    q1pg = q1.add('21000-9800', 'PD on gross interest')
    q1ef = q1.add('round(9400/21000*100,2)', 'RD share of FD')

    q2 = Checks()
    q2rr = q2.add('64000+9000+2500', 'RR incl. dividends and interest receipts')
    q2re = q2.add('52000+14000+8000+11000', 'RE')
    q2ce = q2.add('9500+4000', 'CE')
    q2nd = q2.add('1800+3200', 'NDCR')
    q2rd = q2.add('85000-75500', 'RD')
    q2fd = q2.add('(85000+13500)-(75500+5000)', 'FD')
    q2pd = q2.add('18000-14000', 'PD')

    q3 = Checks()
    q3a = q3.add('round(1580000/32600000*100,2)', 'FD % GDP')
    q3b = q3.add('round(520000/32600000*100,2)', 'RD % GDP')
    q3c = q3.add('round((1580000-1170000)/32600000*100,2)', 'PD % GDP')
    q3d = q3.add('round(520000/1580000*100,2)', 'RD share of FD')

    k = Checks()
    k_rr = k.add('30000+6000', 'case RR')
    k_rd = k.add('44000-36000', 'case RD')
    k_fd = k.add('(44000+12000)-(36000+2500)', 'case FD')
    k_pd = k.add('17500-7000', 'case PD')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch07', 'n': 3,
        'title': 'The Process of Budget Making: Sources of Revenue, Expenditure Management and Management of Public Debt',
        'outcomes': [
            'Describe the Union budget cycle — preparation, presentation and enactment, execution — including the Annual Financial Statement (Article 112), the budget documents, the Finance and Appropriation Bills, guillotine and cut motions.',
            'Classify government receipts (revenue: tax and non-tax; capital: debt and non-debt) and expenditure (revenue and capital), and name the bodies that administer them (CBDT, CBIC, Department of Expenditure).',
            'Compute revenue deficit, fiscal deficit and primary deficit, and interpret what each tells us.',
            'Explain public debt management in India — objectives, institutions (RBI\'s IDMD, Department of Economic Affairs, PDMC), FRBM Act, 2003 — and the three government accounts.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 55, 'practice': 60}, 'prereq': ['fnd-p4-ch07-u01'],
                 'exam_tip': 'Deficit computations appear in almost every attempt — learn the three formulas cold and remember that recoveries of loans and disinvestment are NON-debt capital receipts (they reduce the fiscal deficit) while borrowings are not counted. Also expect fact MCQs: 1 February, 75 days, 14 days, guillotine, Article 112, Article 266(1).'},
        'concepts': [
            {'id': 'c1', 'title': 'Introduction — what a budget is and why it is needed',
             'body': ['Governments defend borders, keep law and order, provide public goods and run welfare programmes. All of this needs money, and the budget is the main policy instrument for raising and directing it.',
                      'Budgeting is needed because resources are limited: they must be allocated for maximum social welfare, reallocated to declared priorities, used to redistribute income and wealth, to reduce economic fluctuations, to raise real GDP sustainably and to narrow regional gaps.',
                      'A government budget is a statement of where the money will come from and where it will go: estimates of receipts and expenditure for the coming year and how any gap will be financed, along with projections for agriculture, industry and services. It is the most complete report of government finances. States and local bodies prepare their own budgets; this unit deals with the Union budget.'],
             'analogy': 'A household budget lists salary and other income against rent, food and fees, and plans a loan if needed. The Union budget is the same exercise for 140 crore people.',
             'work': 'Every year after 1 February, CA firms publish budget analyses and clients ask what the budget means for them — the starting point is reading the receipts and expenditure statements correctly.'},
            {'id': 'c2', 'title': 'The process of budget making',
             'body': ['The Ministry of Finance prepares the budget in consultation with NITI Aayog and the other ministries. It must be passed by both Houses of Parliament before the financial year begins (1 April to 31 March).',
                      'The word "budget" does not appear in the Constitution. Article 112 requires the President to place before both Houses, for every financial year, an estimate of what the Government of India expects to receive and to spend — this is called the Annual Financial Statement (AFS).',
                      'Three stages: (i) preparation, (ii) presentation and enactment, (iii) execution. Two kinds of activity: the administrative process (preparing the budget and documents with stakeholders) and the legislative process (Parliament discussing and passing it).',
                      'Work starts around August–September, months before the presentation. The Budget Division of the Ministry of Finance issues the budget circular with instructions and formats to all ministries, States, UTs and autonomous bodies; departments prepare separate estimates of receipts and expenditure. The Finance Minister holds pre-budget consultations with State finance ministers and chief ministers, industry, farmers, social sector and labour representatives, NITI Aayog experts and economists.',
                      'The documents show Budget Estimates (BE) for the coming year, Revised Estimates (RE) for the current year, and Actuals for the year before. The AFS shows receipts and payments under three accounts: the Consolidated Fund of India, the Contingency Fund of India and the Public Account.',
                      'Budget speech: Part A covers the macroeconomic situation, priorities, total resources and sector-wise allocations and new schemes; Part B covers progress on policies and the tax proposals.',
                      'Documents laid besides the speech: the Annual Financial Statement, Demands for Grants, the Finance Bill, and statements required by the FRBM Act (Macro-Economic Framework Statement; Medium-Term Fiscal Policy cum Fiscal Policy Strategy Statement), plus nine explanatory documents. Expenditure "charged" on the Consolidated Fund (e.g. emoluments of the President, Supreme Court judges and heads of constitutional bodies) is not voted on and is shown separately.',
                      'In an election year a Vote on Account may first be taken for a few months, followed later by the full budget.'],
             'analogy': 'Preparing the budget is like a school annual day: rehearsals (circular and estimates) start months earlier; the show (presentation) happens on one fixed day; then the real work of running the year (execution) begins.',
             'work': 'CAs working with government departments and PSUs prepare the departmental estimates that feed into the budget circular, and later track actual spending against BE and RE.'},
            {'id': 'c3', 'title': 'Presentation and enactment in Parliament',
             'body': ['The budget is presented in the Lok Sabha on 1 February (since 2017-18, or another date the government decides); the railway budget was merged with the general budget from 2017-18. It is laid in the Rajya Sabha after the Finance Minister\'s speech.',
                      'Lok Sabha discussion has two stages: a general discussion on the whole budget; then, after an adjournment during which departmental standing committees examine the Demands for Grants, ministry-wise discussion and voting on the demands. The Lok Sabha may approve, reject or reduce a demand. The Rajya Sabha only discusses; it does not vote on demands.',
                      'Cut motions seek to reduce a demand — for economy, to express a policy difference or to voice a grievance.',
                      'Guillotine: on the last allotted day the Speaker puts all remaining demands to vote together, whether discussed or not, to finish within time.',
                      'Appropriation Bill: after voting on demands, it authorises withdrawal of money from the Consolidated Fund of India.',
                      'Finance Bill: introduced right after the budget presentation to give effect to tax proposals (imposition, abolition, alteration or regulation of taxes), with an explanatory memorandum. The motion for leave to introduce it cannot be opposed. It is taken up after the Appropriation Bill and must be passed within 75 days of introduction. As a money bill, the Rajya Sabha must return it within 14 days, with or without recommendations, which the Lok Sabha may accept or reject.'],
             'blocks': [table(['Term', 'Meaning'], [['Annual Financial Statement', 'Article 112 statement of estimated receipts and expenditure'], ['Demands for Grants', 'Ministry-wise requests for voted expenditure'], ['Cut motion', 'Motion to reduce a demand'], ['Guillotine', 'All pending demands put to vote together on the last day'], ['Appropriation Bill', 'Authority to withdraw money from the Consolidated Fund'], ['Finance Bill', 'Gives effect to tax proposals; pass within 75 days; Rajya Sabha returns within 14 days'], ['Vote on Account', 'Interim grant for a few months, usually in an election year']], title='Budget vocabulary')],
             'analogy': 'The Appropriation Bill is the permission to spend; the Finance Bill is the permission to tax.',
             'work': 'Tax practitioners track the Finance Bill from introduction to enactment because amendments made in Parliament can change the final tax law clients must follow from 1 April.'},
            {'id': 'c4', 'title': 'Sources of revenue — receipts of the government',
             'body': ['The Department of Revenue (Ministry of Finance) controls Union taxes through two statutory boards: the Central Board of Direct Taxes (CBDT — income tax, corporation tax) and the Central Board of Indirect Taxes and Customs (CBIC — GST, customs, central excise and other indirect taxes). It also administers laws on GST, central sales tax and stamp duties.',
                      'Revenue receipts neither create a liability nor reduce an asset of the government. They are (a) tax revenue — corporation tax, taxes on income, wealth tax, customs, Union excise duties, GST including compensation cess, taxes of Union Territories; and (b) non-tax revenue — interest receipts, dividends and profits from public sector enterprises and surplus transferred by the RBI, other non-tax revenue (fees for social, economic and general services), and receipts of UTs.',
                      'Net tax revenue of the Centre = gross tax revenue − States\' share − the National Calamity Contingent Duty transferred to the National Calamity Contingency Fund.',
                      'Capital receipts either create a liability or reduce an asset. (a) Non-debt capital receipts: recoveries of loans and advances; miscellaneous capital receipts such as disinvestment. (b) Debt capital receipts: market loans, short-term borrowings and treasury bills, securities issued against small savings, State provident funds (net), net external debt and other receipts (net) such as Sovereign Gold Bonds.'],
             'blocks': [table(['Receipt', 'Revenue / Capital', 'Debt-creating?'], [['Income tax, GST, customs', 'Revenue (tax)', 'No'], ['Dividends from PSUs, RBI surplus', 'Revenue (non-tax)', 'No'], ['Interest received on loans given', 'Revenue (non-tax)', 'No'], ['Recovery of loans given to States', 'Capital', 'No'], ['Disinvestment proceeds', 'Capital', 'No'], ['Market borrowings, T-bills', 'Capital', 'Yes'], ['Small savings, provident funds', 'Capital', 'Yes'], ['Loans from World Bank / ADB', 'Capital', 'Yes']], title='Classifying receipts')],
             'analogy': 'Revenue receipts are like your salary — yours to keep. Capital receipts are either a loan you must repay, or money from selling your old car (you are poorer by the car).',
             'work': 'Disinvestment transactions — PSU share sales, offer for sale — involve CAs at every step; for the budget they are non-debt capital receipts that reduce the fiscal deficit.'},
            {'id': 'c5', 'title': 'Public expenditure management',
             'body': ['Resources are limited, so total public spending must fit a sustainable macroeconomic framework. Developing economies need large public spending for growth and jobs, and cutting the fiscal deficit needs a clever mix of revenue and spending policies. Spending should reach socially desirable areas and deliver given outputs at minimum cost.',
                      'Unproductive spending leads to larger deficits, higher taxes, slower growth, fewer resources for other uses and a heavier future debt burden.',
                      'The Department of Expenditure is the nodal department for public financial management at the Centre and matters connected with State finances. It implements Finance Commission and Central Pay Commission recommendations, monitors audit observations, prepares Union accounts, and helps ministries control costs and prices of public services and improve procedures.',
                      'Pre-budget meetings chaired by the Secretary (Expenditure) discuss each ministry\'s needs; estimates are finalised after the Finance Minister approves. The "Expenditure Profile" (earlier called the Expenditure Budget) aggregates spending across ministries.',
                      'Classification: A. Centre\'s expenditure — establishment expenditure; central sector schemes (fully funded and run by Union agencies); other central expenditure including CPSEs and autonomous bodies. B. Transfers to States — Finance Commission transfers, centrally sponsored schemes and other transfers.',
                      'Revenue expenditure creates no physical or financial asset: running departments and services, interest payments, and grants to States and others (even if some grants are used for assets). Capital expenditure creates assets or reduces liabilities: land, buildings, machinery, investment in shares, loans and advances to States, UTs, PSUs and others.'],
             'analogy': 'Revenue expenditure is your monthly grocery and electricity bill; capital expenditure is buying a house or repaying your home loan.',
             'work': 'Government auditors and CAs in PSUs classify every outflow as revenue or capital — a wrong classification distorts the revenue deficit reported to Parliament.'},
            {'id': 'c6', 'title': 'Types of budget and measures of deficit',
             'body': ['Balanced budget: receipts = expenditure. Surplus budget: receipts > expenditure. Deficit budget: receipts < expenditure — it increases liabilities or reduces reserves; most modern economies run deficits.',
                      'Budgetary (overall) deficit: excess of total expenditure over total receipts, revenue and capital (in older usage, before counting new borrowing).',
                      'Revenue deficit = revenue expenditure − revenue receipts. It shows that regular income cannot meet regular running costs, so the government borrows or diverts resources to pay for consumption.',
                      'Fiscal deficit = total expenditure − total receipts excluding borrowings = (revenue expenditure + capital expenditure) − (revenue receipts + non-debt capital receipts). Equivalently FD = RD + (capital expenditure − non-debt capital receipts). It equals the government\'s total borrowing requirement and is usually expressed as a % of GDP. If RD forms a large share of FD, much of the borrowing is going into consumption, not investment.',
                      'Primary deficit = fiscal deficit − net interest liabilities (interest paid − interest received on domestic lending). It shows borrowing needed for purposes other than interest, i.e. the current-year imbalance. In simple problems where no interest receipts are given, interest payments are deducted directly.',
                      'Outcome budget: links allocations for schemes to measurable output and outcome targets — a progress card on how last year\'s money was used.'],
             'blocks': [table(['Measure', 'Formula'], [['Revenue deficit', 'Revenue expenditure − Revenue receipts'], ['Fiscal deficit', 'Total expenditure − (Revenue receipts + Non-debt capital receipts)'], ['Fiscal deficit (alternative)', 'Revenue deficit + Capital expenditure − Non-debt capital receipts'], ['Primary deficit', 'Fiscal deficit − Net interest payments']], title='Deficit formulas')],
             'analogy': 'Revenue deficit: your salary does not cover your monthly bills. Fiscal deficit: the total you must borrow this year. Primary deficit: what you would still need to borrow even if you had no old loans to pay interest on.',
             'work': 'Rating agencies and bond desks read FD, RD and PD as % of GDP; CAs advising on G-sec investment or State bonds start from these ratios.'},
            {'id': 'c7', 'title': 'Public debt management',
             'body': ['Public debt is debt contracted by the government against the Consolidated Fund of India, from internal and external sources — mainly market-based, fixed-rate domestic instruments used to finance the fiscal deficit. It must be repaid with interest; since some debt falls due every month, maturing bonds are usually refinanced by issuing new ones.',
                      'Public debt management means deciding the size and composition of debt, maturity pattern, interest rates and redemption, and implementing a strategy to raise funds at the desired cost and risk. The Centre\'s objective: meet financing needs at the lowest possible long-term cost, keep debt sustainable, and develop a deep domestic bond market. Its strategy rests on three pillars: low cost, risk mitigation and market development.',
                      'Institutions: RBI — domestic marketable debt (dated securities, treasury bills, cash management bills); its Internal Debt Management Department (IDMD) manages the domestic debt of the Centre, 28 State governments and two UTs. Ministry of Finance (Department of Economic Affairs) — external debt. Ministry of Finance Budget Division with RBI — other liabilities such as small savings, deposits and reserve funds. Treasury bills meet short-term cash needs; dated securities raise long-term funds. Since 1997 the RBI has given Ways and Means Advances (WMA) — temporary loans for a period of up to three months — to States that bank with it, to cover gaps between receipts and payments.',
                      'External debt comes mostly from multilateral agencies (IBRD, ADB); there is no sovereign borrowing from international capital markets; it is long-term and mostly at fixed rates; its main risk is rupee depreciation, which raises the cost of servicing.',
                      'FRBM Act, 2003 gives a legal framework to cut deficits and debt to sustainable levels. Objectives: inter-generational equity, long-run macroeconomic stability, better fiscal–monetary coordination and transparency in fiscal operations.',
                      'In 2016 a Public Debt Management Cell (PDMC) was set up within the Department of Economic Affairs, while a Medium-Term Debt Management Strategy (MTDS) sets the desired composition of debt. The RBI Retail Direct facility (announced 5 February 2021) lets retail investors open a G-sec account with the RBI and buy and sell government securities online.',
                      'Pandemic years (2020-21 and 2021-22) saw health and social spending rise while revenue fell, so the fiscal deficit and borrowing programme expanded sharply to provide counter-cyclical support.'],
             'analogy': 'Debt management is like a family rolling over its loans wisely: borrowing at the cheapest rate, spreading repayment dates so not everything falls due in one month, and avoiding loans in a foreign currency that could suddenly become expensive.',
             'work': 'Treasury CAs in banks bid in RBI\'s G-sec and T-bill auctions; individuals can now buy G-secs via RBI Retail Direct — a product CAs often explain to clients.'},
            {'id': 'c8', 'title': 'The three government accounts',
             'body': ['Consolidated Fund of India: every rupee of revenue, every loan the government raises and every repayment of loans it has given goes into this fund, and all government spending is paid out of it. Money can be spent only with Parliament\'s appropriation. It has revenue and capital divisions.',
                      'Contingency Fund of India: placed at the disposal of the President to give advances for urgent unforeseen expenditure without prior approval of Parliament; the amount is later reported to Parliament and recouped from the Consolidated Fund.',
                      'Public Account (Article 266(1)): funds where the government acts only as a banker — provident funds, small savings and similar deposits. The money belongs to depositors and must be returned, so spending from it does not need Parliament\'s approval.'],
             'analogy': 'Consolidated Fund = the family\'s main account (spending needs the elders\' approval); Contingency Fund = the emergency cash in the drawer; Public Account = money a neighbour left with you for safe-keeping.',
             'work': 'In government audits, CAs check that payments came from the right fund — for example that an urgent advance from the Contingency Fund was later recouped.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Revenue, fiscal and primary deficit', 'difficulty': 'moderate', 'minutes': 8,
             'q': f'Budget data of a country (₹ crore): tax revenue {inr(tax)}; non-tax revenue {inr(ntax)}; revenue expenditure {inr(rexp)} (including interest payments {inr(intp)}); capital expenditure {inr(cexp)}; recovery of loans {inr(rec)}; disinvestment {inr(dis)}; borrowings {inr(bor)}. Compute revenue deficit, fiscal deficit and primary deficit, and the share of revenue deficit in fiscal deficit.',
             'solution': [table(['Item', '₹ crore'], [['Tax revenue', tax], ['Non-tax revenue', ntax], ['Revenue receipts', rr]], num=[1], total=True),
                          p(f'Revenue deficit = revenue expenditure − revenue receipts = {inr(rexp)} − {inr(rr)} = ₹{inr(rd)} crore.'),
                          p(f'Total expenditure = {inr(rexp)} + {inr(cexp)} = {inr(texp)}. Non-debt capital receipts = recovery of loans {inr(rec)} + disinvestment {inr(dis)} = {inr(ndcr)}.'),
                          p(f'Fiscal deficit = {inr(texp)} − ({inr(rr)} + {inr(ndcr)}) = ₹{inr(fd)} crore — exactly the borrowings shown, as it must be.'),
                          p(f'Primary deficit = {inr(fd)} − interest {inr(intp)} = ₹{inr(pd)} crore.'),
                          p(f'Revenue deficit as % of fiscal deficit = {inr(rd)} ÷ {inr(fd)} × 100 = {sh}%: more than half of the borrowing is financing current (consumption) spending.'),
                          note('Borrowings are never deducted in computing the fiscal deficit — the fiscal deficit measures how much has to be borrowed.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Revenue or capital?', 'difficulty': 'core', 'minutes': 5,
             'q': 'Classify: (1) dividend received from Coal India; (2) salaries of government staff; (3) loan given to a State; (4) proceeds from sale of shares of a PSU; (5) interest paid on G-secs; (6) construction of a highway; (7) grant to a State for building schools; (8) issue of treasury bills.',
             'solution': [table(['Item', 'Classification', 'Why'], [
                 ['1 Dividend from PSU', 'Revenue receipt (non-tax)', 'No liability, no asset reduction'],
                 ['2 Salaries', 'Revenue expenditure', 'Running cost; no asset created'],
                 ['3 Loan to a State', 'Capital expenditure', 'Creates a financial asset'],
                 ['4 Disinvestment', 'Capital receipt (non-debt)', 'Reduces an asset (shares)'],
                 ['5 Interest paid', 'Revenue expenditure', 'Cost of servicing debt'],
                 ['6 Highway', 'Capital expenditure', 'Creates a physical asset'],
                 ['7 Grant to a State', 'Revenue expenditure', 'Grants are revenue expenditure even if used for assets'],
                 ['8 Treasury bills', 'Capital receipt (debt)', 'Creates a liability']])]},
            {'id': 'i3', 'title': 'Deficits as % of GDP, and the size of public debt', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'A government\'s fiscal deficit is ₹16,00,000 crore and interest payments ₹12,50,000 crore; GDP is ₹3,50,00,000 crore. Find FD and PD as % of GDP. Also, Union debt (₹ crore) was: internal and other liabilities 1,90,43,590 and external 6,74,426 at 31 March 2026; 2,07,70,868 and 7,11,182 at 31 March 2027 (Budget 2026-27). Find total debt, its growth and the external share in 2027.',
             'solution': [p(f'FD % GDP = 16,00,000 ÷ 3,50,00,000 × 100 = {fdp}%. PD = 16,00,000 − 12,50,000 = 3,50,000 → {pdp}% of GDP. Interest absorbs most of the borrowing.'),
                          table(['', '31 Mar 2026', '31 Mar 2027'], [['Internal debt & other liabilities', 19043590, 20770868], ['External debt', 674426, 711182], ['Total', d26, d27]], num=[1, 2], total=True),
                          p(f'Growth = ({inr(d27)} − {inr(d26)}) ÷ {inr(d26)} × 100 = {g}%. External share in 2027 = {inr(711182)} ÷ {inr(d27)} × 100 = {ex}% — India\'s public debt is overwhelmingly domestic.')],
             'checks': c3},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Budget-day note for clients', 'role': 'CA in a mid-size practice',
             'situation': 'Your partner wants a two-page client note by the evening of 1 February.',
             'steps': ['Read Part B of the speech and the Finance Bill memorandum for tax changes and their effective dates.', 'From the AFS and receipts budget, note FD, RD and PD as % of GDP and the borrowing programme.', 'Flag provisions effective from 1 April versus those effective immediately.', 'Mention that the Finance Bill may be amended before it is passed within 75 days.'],
             'takeaway': 'Knowing the budget documents tells you where each piece of information lives.',
             'think': 'Why can a tax proposal in the budget speech still change before 1 April?', 'answer': 'The Finance Bill is debated and can be amended by the Lok Sabha before it is passed; only the enacted Finance Act binds.'},
            {'id': 'j2', 'title': 'Explaining G-secs to a retail client', 'role': 'CA advising individuals',
             'situation': 'A retired client wants a safe investment and has heard about RBI Retail Direct.',
             'steps': ['Explain that dated securities and T-bills are issued by the RBI on behalf of the government to finance the fiscal deficit.', 'Show how to open a Retail Direct account and bid non-competitively in auctions.', 'Explain interest-rate risk if sold before maturity.'],
             'takeaway': 'Public debt management has become a retail investment product.'},
            {'id': 'j3', 'title': 'Grant or capital?', 'role': 'CA auditing a State department',
             'situation': 'A department booked a grant to a municipal body for building drains as capital expenditure.',
             'steps': ['Apply the rule that grants-in-aid are revenue expenditure of the giver, even if the receiver builds assets.', 'Recommend reclassification; note that the revenue deficit is understated as booked.'],
             'takeaway': 'Classification changes the reported revenue deficit — a figure Parliament and rating agencies watch closely.'},
        ],
        'mcqs': [
            M('m1', 'The constitutional provision requiring an "Annual Financial Statement" to be laid before Parliament is:', ['Article 112', 'Article 280', 'Article 266', 'Article 246'], 0, "Article 112 requires the President to lay an 'Annual Financial Statement' — the budget — before Parliament each year; the word 'budget' itself does not appear in the Constitution. Article 280 is the tempting trap: it concerns public finance too, but it creates the Finance Commission. Article 266 covers the Consolidated Fund and Public Account. In practice: the Annual Financial Statement is the core document CA students and analysts open first on Budget day.", 'c2', topic='The Process of Budget Making'),
            M('m2', 'The Union budget is now normally presented on:', ['1 February', 'Last working day of February', '1 March', '1 April'], 0, 'From 2017-18 onwards, the Union Budget has normally been presented on 1 February, so that Parliament can pass it before the financial year begins on 1 April. The last working day of February is the trap — that was the old colonial-era practice. In practice: CA firms hold Budget-day webinars on 1 February, and companies can plan tax changes before 1 April instead of waiting until June or July.', 'c3', topic='The Process of Budget Making'),
            M('m3', 'From which year was the railway budget merged with the general budget?', ['2017-18', '2014-15', '2020-21', '2000-01'], 0, "The separate railway budget, presented since 1924, was merged with the general budget from the budget for 2017-18 — the same year the presentation date moved to 1 February. 2014-15 and 2020-21 are tempting guesses near the reform period. In practice: since the merger, railway capital spending appears as part of the Ministry of Railways' demand in the Union Budget, which analysts track for infrastructure stocks.", 'c3', topic='The Process of Budget Making'),
            M('m4', 'The budget circular is issued by the:', ['Budget Division of the Ministry of Finance', 'NITI Aayog', 'Reserve Bank of India', 'Comptroller and Auditor General'], 0, 'Budget making starts around August–September when the Budget Division of the Ministry of Finance issues the budget circular asking ministries and departments for their estimates. NITI Aayog is the trap — it advises on policy and programmes but does not run the budget process. The CAG audits spending afterwards. In practice: finance officers in each ministry prepare revised and budget estimates in the formats prescribed by this circular.', 'c2', topic='The Process of Budget Making'),
            M('m5', 'Part B of the Finance Minister\'s budget speech mainly contains:', ['Tax proposals and policy direction', 'Review of the macroeconomic situation only', 'Accounts of the previous year', 'Railway budget'], 0, "Part B of the budget speech sets out policy direction and the tax proposals — changes in income-tax slabs, customs duties and so on. The macroeconomic review and expenditure allocations are covered in Part A, which is the tempting trap. In practice: tax professionals and CA firms listen closely to Part B, because that is where announcements affecting clients' tax liability are made.", 'c2', topic='The Process of Budget Making'),
            M('m6', 'The Appropriation Bill is intended to:', ['Authorise withdrawal of money from the Consolidated Fund of India', 'Impose new taxes', 'Reduce wasteful expenditure', 'Approve borrowings from the IMF'], 0, "No money can be withdrawn from the Consolidated Fund of India without parliamentary approval; the Appropriation Bill gives that authority for spending. 'Impose new taxes' is the trap — taxation proposals are carried by the Finance Bill. In practice: ministries can spend their budget only after the Appropriation Act is passed, which is why a vote on account is needed when the full budget is delayed, as in an election year.", 'c3', topic='The Process of Budget Making'),
            M('m7', 'Within how many days of its introduction must Parliament pass the Finance Bill?', ['75 days', '14 days', '30 days', '90 days'], 0, 'The Finance Bill has to be passed by Parliament within 75 days from the day it is introduced. The tempting 14 days is a different rule: the Rajya Sabha must return a money bill to the Lok Sabha within 14 days, with or without recommendations. In practice: tax changes in the Finance Bill usually take effect from 1 April, and practitioners watch for amendments made before the Finance Act is finally passed.', 'c3', 'core', '75', topic='The Process of Budget Making'),
            M('m8', 'Putting all outstanding demands for grants to vote together on the last allotted day is called:', ['Guillotine', 'Cut motion', 'Vote on account', 'Zero hour'], 0, "On the last day allotted for discussing demands for grants, the Speaker puts all remaining demands to vote together — the guillotine — so that financial business finishes within time. 'Cut motion' is the trap: that is a motion to reduce a particular demand. In practice: many ministries' demands are passed without detailed debate through the guillotine, which commentators note when assessing parliamentary scrutiny of spending.", 'c3', topic='The Process of Budget Making'),
            M('m9', 'A motion to reduce the amount of a demand for grant is a:', ['Cut motion', 'Guillotine', 'Money bill', 'Adjournment motion'], 0, "A cut motion seeks to reduce the amount of a demand for grant — to suggest economy, disagree with policy, or voice a specific grievance. 'Guillotine' is the trap: that closes the debate by putting all outstanding demands to vote together. In practice: opposition members in the Lok Sabha use token cut motions to highlight issues such as farm distress during budget debates.", 'c3', topic='The Process of Budget Making'),
            M('m10', 'Which statement about the Rajya Sabha and the budget is correct?', ['It discusses the budget but does not vote on demands for grants', 'It votes on every demand for grant', 'It can reject the Finance Bill', 'It presents the budget'], 0, "The Rajya Sabha discusses the budget but does not vote on demands for grants; for money bills such as the Finance Bill it can only make recommendations within 14 days, which the Lok Sabha may accept or reject. 'It can reject the Finance Bill' is the trap. In practice: this is why the government of the day needs a Lok Sabha majority to pass its budget, regardless of its Rajya Sabha strength.", 'c3', 'moderate', topic='The Process of Budget Making'),
            M('m11', 'Direct taxes of the Union are administered by the:', ['CBDT', 'CBIC', 'GST Council', 'Department of Expenditure'], 0, "The Central Board of Direct Taxes (CBDT) administers direct taxes such as income tax and corporation tax. CBIC is the trap: it administers indirect taxes — GST, customs and central excise. The GST Council recommends GST policy; it does not administer taxes. In practice: CAs deal with the CBDT's Income Tax Department for returns and assessments, and with CBIC officers for GST and customs matters.", 'c4', topic='Sources of Revenue'),
            M('m12', 'Which of the following is a NON-tax revenue receipt?', ['Dividend and surplus transferred by the RBI', 'Corporation tax', 'Customs duty', 'GST compensation cess'], 0, "Non-tax revenue includes interest receipts, dividends and profits from public enterprises, fees, and the surplus transferred by the RBI. Corporation tax and customs duty are tax revenue. GST compensation cess is the tempting trap because it sounds different from a regular tax, but a cess is still tax revenue. In practice: the RBI's annual surplus transfer, often running into lakhs of crores, is a major non-tax receipt watched by fiscal analysts.", 'c4', topic='Sources of Revenue'),
            M('m13', 'Which of these is a non-debt capital receipt?', ['Disinvestment of government equity in a PSU', 'Market loans', 'Treasury bills', 'Small savings'], 0, 'Non-debt capital receipts reduce assets without creating a liability — recovery of loans and disinvestment of government equity in PSUs. Market loans, treasury bills and small savings are the traps: they are capital receipts too, but they create debt the government must repay. In practice: stake sales in companies such as LIC or Coal India appear as disinvestment receipts in the Budget and help reduce the fiscal deficit.', 'c4', topic='Sources of Revenue'),
            M('m14', 'Grants given by the Union to State governments are treated as:', ['Revenue expenditure', 'Capital expenditure', 'Capital receipts', 'Non-debt receipts'], 0, "Grants from the Union to States are revenue expenditure for the Union, because they create no asset or financial claim for the Union — even if States use part of them to build assets. Capital expenditure is the trap: that requires an asset or claim for the spender. In practice: this classification is why the Union's 'effective capital expenditure' figure separately adds grants for creating capital assets.", 'c5', 'moderate', topic='Public Expenditure Management'),
            M('m15', 'Loans and advances given by the Union to State governments are:', ['Capital expenditure', 'Revenue expenditure', 'Revenue receipts', 'Charged expenditure'], 0, 'Loans and advances by the Union to States create a financial asset — a claim to repayment — so they are capital expenditure. Revenue expenditure is the trap: it would apply to grants, which carry no repayment. In practice: the 50-year interest-free capex loans the Union has given States in recent Budgets are shown as capital expenditure because the Union expects repayment.', 'c5', topic='Public Expenditure Management'),
            M('m16', 'Fiscal deficit equals:', ['Total expenditure − total receipts excluding borrowings', 'Revenue expenditure − revenue receipts', 'Fiscal deficit − interest', 'Total expenditure − total receipts including borrowings'], 0, "Fiscal deficit = total expenditure − total receipts excluding borrowings; it shows how much the government must borrow. 'Revenue expenditure − revenue receipts' is the trap — that is the revenue deficit. Including borrowings in receipts would make the gap zero by definition. In practice: the fiscal deficit target (as a percentage of GDP) is the headline number credit-rating agencies and bond markets watch in every Indian Budget.", 'c6', topic='Public Debt Management'),
            M('m17', 'Primary deficit equals:', ['Fiscal deficit − net interest payments', 'Revenue deficit − interest payments', 'Fiscal deficit + interest payments', 'Revenue deficit + capital expenditure'], 0, "Primary deficit = fiscal deficit − net interest payments. It removes the burden of past borrowing and shows how much current policy adds to debt. 'Fiscal deficit + interest payments' is the trap — interest must be subtracted, not added. In practice: economists track whether India's primary deficit is shrinking, since a primary balance means borrowing goes only to pay interest on old debt.", 'c6', topic='Public Debt Management'),
            M('m18', 'Revenue receipts ₹21,500 crore; revenue expenditure ₹27,800 crore. Revenue deficit is:', ['₹6,300 crore', '₹49,300 crore', '₹5,300 crore', '₹7,300 crore'], 0, 'Revenue deficit = revenue expenditure − revenue receipts = 27,800 − 21,500 = ₹6,300 crore. The tempting ₹49,300 crore adds the two figures instead of subtracting; ₹5,300 and ₹7,300 crore are arithmetic slips of ₹1,000. In practice: a revenue deficit means the government is borrowing to pay for day-to-day expenses such as salaries, subsidies and interest, which analysts treat as a quality concern.', 'c6', 'core', '27800-21500', topic='Public Debt Management'),
            M('m19', 'Revenue receipts 24,000; recovery of loans 1,200; borrowings 16,300; other non-debt capital receipts 3,500; revenue expenditure 29,000; capital expenditure 16,000 (₹ crore). Fiscal deficit is:', ['₹16,300 crore', '₹21,000 crore', '₹19,800 crore', '₹5,000 crore'], 0,
              'Fiscal deficit = total expenditure − non-debt receipts = (29,000 + 16,000) − (24,000 + 1,200 + 3,500) = 45,000 − 28,700 = ₹16,300 crore, equal to borrowings. Traps: ₹21,000 ignores all non-debt capital receipts; ₹19,800 ignores the other non-debt receipts of 3,500; ₹5,000 is the revenue deficit (29,000 − 24,000). In practice: budget analysts reconcile fiscal deficit with the borrowing figure as a check.', 'c6', 'hard', '(29000+16000)-(24000+1200+3500)', topic='Public Debt Management'),
            M('m20', 'In the previous question, if interest payments are ₹4,100 crore (no interest receipts), the primary deficit is:', ['₹12,200 crore', '₹20,400 crore', '₹16,300 crore', '₹900 crore'], 0, 'Primary deficit = fiscal deficit − interest payments = 16,300 − 4,100 = ₹12,200 crore. The tempting ₹20,400 crore adds interest instead of deducting it; ₹900 crore wrongly deducts interest from the revenue deficit (5,000 − 4,100); ₹16,300 crore is the fiscal deficit itself. In practice: when interest absorbs a large share of the fiscal deficit, it signals heavy past borrowing, a point rating agencies highlight.', 'c6', 'moderate', '16300-4100', topic='Public Debt Management'),
            M('m21', 'A large share of revenue deficit in fiscal deficit indicates that:', ['Borrowed funds are largely being used for consumption rather than investment', 'The government is creating many assets', 'Interest payments are zero', 'The budget is in surplus'], 0, "Revenue deficit is borrowing used for current expenses such as salaries, subsidies and interest. If it forms a large share of the fiscal deficit, most borrowed money is being consumed rather than invested in assets that could repay it. 'The government is creating many assets' is the trap — that happens when capital expenditure drives the deficit. In practice: the FRBM framework targets reducing the revenue deficit for this reason.", 'c6', 'moderate', topic='Public Debt Management'),
            M('m22', 'A surplus budget tends to:', ['Reduce aggregate demand', 'Increase aggregate demand', 'Leave aggregate demand unchanged always', 'Increase public debt'], 0, "In a surplus budget receipts exceed expenditure, so the government withdraws more purchasing power through taxes than it injects through spending, reducing aggregate demand. 'Increase aggregate demand' is the trap — that is the effect of a deficit budget. A surplus also tends to reduce, not increase, public debt. In practice: a surplus stance would be used to cool an overheated, inflationary economy.", 'c6', topic='Public Debt Management'),
            M('m23', 'The domestic marketable debt of the Central and State governments is managed by the:', ['Reserve Bank of India (IDMD)', 'Department of Expenditure', 'SEBI', 'Finance Commission'], 0, "The RBI's Internal Debt Management Department manages the marketable domestic debt of the Centre and the States, issuing treasury bills and dated securities. The Department of Expenditure is the trap; external debt is managed by the Department of Economic Affairs, not the RBI. In practice: bond dealers at banks bid in the weekly G-sec and T-bill auctions conducted by the RBI as the government's debt manager.", 'c7', topic='Public Debt Management'),
            M('m24', 'Ways and Means Advances given by the RBI to State governments are:', ['Short-term credit up to three months to bridge cash mismatches', 'Long-term loans for capital projects', 'Grants that need not be repaid', 'Foreign currency loans'], 0, "Since 1997, the RBI gives States banking with it Ways and Means Advances — short-term credit of up to three months — to bridge temporary gaps between receipts and payments. 'Long-term loans for capital projects' is the trap: WMA are not meant to finance spending permanently. In practice: State finance departments monitor WMA and overdraft use closely, as prolonged overdrafts signal cash stress to analysts.", 'c7', 'moderate', topic='Public Debt Management'),
            M('m25', 'The FRBM Act was passed in:', ['2003', '1991', '2016', '2010'], 0, "The Fiscal Responsibility and Budget Management Act was passed in 2003 to provide a legal framework for reducing the Centre's deficits and debt to sustainable levels. 1991 is the tempting trap — the year of economic reforms, not of this Act; 2016 is when the Public Debt Management Cell was created. In practice: every Union Budget includes FRBM statements, such as the Medium-term Fiscal Policy Statement, required under this Act.", 'c7', 'core', '2003', topic='Public Debt Management'),
            M('m26', 'Which is NOT an objective of the FRBM Act?', ['Guaranteeing a budget surplus every year', 'Inter-generational equity in fiscal management', 'Long-run macroeconomic stability', 'Transparency in fiscal operations'], 0, "The FRBM Act aims at fairness between generations in fiscal management, macroeconomic stability over the long run, better fiscal–monetary coordination, and transparent fiscal operations. It sets deficit-reduction targets, but it never guaranteed a yearly budget surplus — that is the exception. In practice: the government has repeatedly used the Act's escape clause, for example during Covid, to relax deficit targets temporarily.", 'c7', 'moderate', topic='Public Debt Management'),
            M('m27', 'The main risk of the Government of India\'s external debt is:', ['Depreciation of the rupee raising servicing cost', 'Very short maturity', 'Floating interest on most of it', 'Sovereign bonds issued in international markets'], 0, "India's external government debt is long-term, mostly at fixed interest and largely from multilateral lenders, with no sovereign bonds in international markets. Its main risk is rupee depreciation, which raises the rupee cost of servicing foreign-currency loans. 'Very short maturity' and 'floating interest' are traps — they contradict its actual structure. In practice: when the rupee weakens, the Union's interest bill on loans from the World Bank and ADB rises.", 'c7', 'hard', topic='Public Debt Management'),
            M('m28', 'Provident fund and small savings deposits held by the government are kept in the:', ['Public Account', 'Contingency Fund of India', 'Consolidated Fund of India', 'National Calamity Contingency Fund'], 0, "Provident fund and small savings deposits belong to depositors; the government holds them as a banker, so they go to the Public Account under Article 266(2), and withdrawals do not need parliamentary vote. Consolidated Fund of India is the trap: it holds the government's own receipts. In practice: small-savings collections in schemes such as PPF flow to the National Small Savings Fund within the Public Account.", 'c8', topic='The Process of Budget Making'),
            M('m29', 'Urgent unforeseen expenditure before Parliament\'s approval is met from the:', ['Contingency Fund of India', 'Public Account', 'Consolidated Fund without any approval', 'RBI\'s reserves'], 0, "The Contingency Fund of India, placed at the President's disposal, meets urgent unforeseen expenditure before Parliament can approve it; the advance is later recouped from the Consolidated Fund after parliamentary authorisation. 'Consolidated Fund without any approval' is the trap — the Consolidated Fund can never be used without parliamentary approval. In practice: sudden disaster relief may first be met through this route.", 'c8', topic='The Process of Budget Making'),
            M('m30', 'The "Outcome Budget" mainly:', ['Links budget allocations to measurable outputs and outcomes', 'Shows only tax proposals', 'Replaces the Finance Bill', 'Lists the public debt'], 0, "An Outcome Budget links money allocated to schemes with measurable outputs and outcomes — for example, kilometres of road built or children immunised — acting as a progress card on spending. 'Shows only tax proposals' is the trap; those are in the Finance Bill and Part B of the speech. In practice: CAs in government audit and performance audit teams use outcome budgets to test whether schemes delivered results.", 'c6', topic='Public Expenditure Management'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'From the following (₹ crore) compute revenue deficit, fiscal deficit and primary deficit (on net interest and on gross interest), and the share of revenue deficit in fiscal deficit: tax revenue 41,000; non-tax revenue 6,500 (including interest receipts 800); revenue expenditure 56,900 (including interest payments 9,800); capital expenditure 15,100; recovery of loans 1,200; disinvestment 2,300; borrowings 21,000.',
             'model': [p(f'Revenue receipts = 41,000 + 6,500 = {inr(q1rr)}. RD = 56,900 − {inr(q1rr)} = ₹{inr(q1rd)} crore.'),
                       p(f'Total expenditure = 56,900 + 15,100 = {inr(q1te)}; non-debt capital receipts = 1,200 + 2,300 = {inr(q1nd)}. FD = {inr(q1te)} − ({inr(q1rr)} + {inr(q1nd)}) = ₹{inr(q1fd)} crore (= borrowings).'),
                       p(f'PD (net interest) = {inr(q1fd)} − (9,800 − 800) = ₹{inr(q1pd)} crore; PD (gross interest) = {inr(q1fd)} − 9,800 = ₹{inr(q1pg)} crore.'),
                       p(f'RD ÷ FD = {inr(q1rd)} ÷ {inr(q1fd)} × 100 = {q1ef}%.')],
             'scheme': [{'id': 's1', 'pt': 'Revenue receipts and revenue deficit', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Non-debt capital receipts identified; borrowings excluded', 'm': 1, 'skill': 'classification'},
                        {'id': 's3', 'pt': 'Fiscal deficit computed and reconciled with borrowings', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Primary deficit on both bases', 'm': 1, 'skill': 'computation'},
                        {'id': 's5', 'pt': 'RD share of FD with interpretation', 'm': 1, 'skill': 'analysis'}],
             'remarks': ['Reconciling FD with borrowings is a quick self-check that examiners appreciate.'],
             'mistakes': ['Treating disinvestment as a revenue receipt.', 'Deducting borrowings in the FD formula.'],
             'tips': ['Write each formula in words before substituting numbers.'], 'checks': q1},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'hard', 'pad': 'table',
             'q': 'Classify and compute RD, FD and PD (₹ crore): taxes 64,000; dividends from PSUs 9,000; interest received 2,500; salaries and pensions 52,000; interest paid 14,000; subsidies 8,000; grants to States 11,000; construction of dams 9,500; loans to PSUs 4,000; recovery of past loans 1,800; disinvestment 3,200; market borrowings 18,000. (Use gross interest payments for PD.)',
             'model': [table(['Head', 'Items', '₹ crore'], [['Revenue receipts', 'Taxes, dividends, interest received', q2rr], ['Revenue expenditure', 'Salaries, interest paid, subsidies, grants', q2re], ['Capital expenditure', 'Dams, loans to PSUs', q2ce], ['Non-debt capital receipts', 'Recovery of loans, disinvestment', q2nd]]),
                       p(f'RD = {inr(q2re)} − {inr(q2rr)} = ₹{inr(q2rd)}. FD = ({inr(q2re)} + {inr(q2ce)}) − ({inr(q2rr)} + {inr(q2nd)}) = ₹{inr(q2fd)} (= market borrowings). PD = {inr(q2fd)} − 14,000 = ₹{inr(q2pd)}.')],
             'scheme': [{'id': 's1', 'pt': 'Correct classification (grants as revenue expenditure; loans as capital)', 'm': 2, 'skill': 'classification'},
                        {'id': 's2', 'pt': 'RD', 'm': 1, 'skill': 'computation'}, {'id': 's3', 'pt': 'FD', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'PD', 'm': 1, 'skill': 'computation'}],
             'remarks': ['The grant to States is the trap — it is revenue expenditure.'], 'mistakes': ['Putting loans to PSUs under revenue expenditure.', 'Treating interest received as a capital receipt.'],
             'tips': ['Classify first in a table; compute second.'], 'checks': q2},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'GDP is ₹3,26,00,000 crore; fiscal deficit ₹15,80,000 crore; revenue deficit ₹5,20,000 crore; interest payments ₹11,70,000 crore. Compute FD, RD and PD as % of GDP and RD as % of FD, and comment.',
             'model': [p(f'FD/GDP = {q3a}%; RD/GDP = {q3b}%; PD = 15,80,000 − 11,70,000 = 4,10,000 → {q3c}% of GDP; RD/FD = {q3d}%.'),
                       p('Comment: about a third of borrowing finances current spending; interest payments take up nearly three-quarters of the fiscal deficit, so most fresh borrowing is used to service past debt.')],
             'scheme': [{'id': 's1', 'pt': 'FD and RD ratios', 'm': 2, 'skill': 'computation'}, {'id': 's2', 'pt': 'PD ratio', 'm': 1, 'skill': 'computation'}, {'id': 's3', 'pt': 'RD/FD ratio', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'Sensible comment on quality of deficit', 'm': 1, 'skill': 'analysis'}],
             'remarks': ['Ratios to two decimals are sufficient.'], 'mistakes': ['Dividing by FD instead of GDP.'], 'tips': ['Label each ratio clearly.'], 'checks': q3},
        ],
        'revision': {
            'summary': ['Budget = statement of estimated receipts and expenditure; Article 112 calls it the Annual Financial Statement.',
                        'Stages: preparation (Aug–Sep circular by Budget Division) → presentation (1 Feb) and enactment → execution.',
                        'Lok Sabha: general discussion, standing committees, voting on demands (cut motions, guillotine) → Appropriation Bill → Finance Bill (75 days; Rajya Sabha 14 days).',
                        'Receipts: revenue (tax, non-tax) and capital (non-debt: loan recoveries, disinvestment; debt: borrowings). CBDT (direct), CBIC (indirect).',
                        'Expenditure: revenue (no asset; includes interest and grants) and capital (asset creation, loans given). Department of Expenditure is the nodal department.',
                        'RD = RE − RR; FD = TE − (RR + NDCR) = borrowing; PD = FD − net interest.',
                        'Debt: RBI/IDMD (domestic marketable), DEA (external), PDMC (2016), MTDS, WMA (since 1997, up to 3 months), FRBM 2003, RBI Retail Direct (5 Feb 2021).',
                        'Accounts: Consolidated Fund (needs appropriation), Contingency Fund (President; recouped), Public Account (Art. 266(1); government as banker).'],
            'remember': ['Charged expenditure is not voted.', 'Vote on account in election years.', 'External debt: multilateral, long-term, fixed rate, no international bond issue; risk = rupee depreciation.'],
            'traps': ['Borrowings are not deducted in FD — FD equals borrowings.', 'Grants to States = revenue expenditure.', 'Disinvestment = capital (non-debt) receipt, not revenue.', 'Rajya Sabha cannot vote on demands.'],
        },
        'quickref': [
            {'k': 'Revenue deficit', 'v': 'Revenue expenditure − Revenue receipts'},
            {'k': 'Fiscal deficit', 'v': '(RE + CE) − (RR + recoveries of loans + disinvestment/other non-debt receipts) = borrowings'},
            {'k': 'Primary deficit', 'v': 'Fiscal deficit − net interest payments (interest paid − interest received)'},
            {'k': 'Key numbers', 'v': 'Art. 112 AFS · 1 Feb (from 2017-18) · Finance Bill 75 days · Rajya Sabha 14 days · FRBM 2003 · PDMC 2016'},
            {'k': 'Three accounts', 'v': 'Consolidated Fund · Contingency Fund · Public Account (Art. 266(1))'},
            {'k': 'Debt managers', 'v': 'RBI-IDMD: domestic marketable · DEA: external · Budget Division + RBI: small savings etc.'},
        ],
        'viva': [
            V('v1', 'Define revenue deficit, fiscal deficit and primary deficit.',
              'Revenue deficit is revenue expenditure minus revenue receipts. Fiscal deficit is total expenditure minus total receipts excluding borrowings, so it equals the total borrowing requirement. Primary deficit is fiscal deficit minus interest payments.',
              [P('p1', 'Revenue deficit = revenue expenditure − revenue receipts', 3, ALT('revenue deficit {x}', x=('revenue expenditure minus revenue receipt', 'revenue expenditure less revenue receipt', 'excess revenue expenditure over revenue receipt', 'revenue expenditure exceed revenue receipt', 'difference between revenue expenditure and revenue receipt', 'revenue spending minus revenue receipt', 'revenue expenditure more than revenue receipt', 'revenue expenditure revenue receipt'))),
               P('p2', 'Fiscal deficit = total expenditure − receipts excluding borrowings (= borrowing)', 4, 'fiscal deficit', 'excluding borrow|exclude borrow|other than borrow|except borrow|without borrow|non debt|borrowing requirement|total borrow|need to borrow|equal borrow|equals borrow', min=2),
               P('p3', 'Primary deficit = fiscal deficit − interest payments', 3, ALT('primary deficit {x}', x=('fiscal deficit minus interest', 'fiscal deficit less interest', 'fiscal deficit excluding interest', 'fiscal deficit net of interest', 'fiscal deficit without interest', 'fiscal deficit after deduct interest', 'fiscal deficit minus net interest', 'fiscal deficit interest')))], 'c6'),
            V('v2', 'Distinguish between revenue receipts and capital receipts with examples.',
              'Revenue receipts neither create a liability nor reduce an asset of the government, for example taxes, dividends from public sector companies and fees. Capital receipts either create a liability or reduce an asset, for example borrowings, recovery of loans and disinvestment proceeds.',
              [P('p1', 'Revenue receipts: no liability, no asset reduction', 4, 'revenue receipt', 'neither|not creat|no liabilit|do not creat|does not creat|nor reduc|not reduc', min=2),
               P('p2', 'Capital receipts: create a liability or reduce an asset', 4, 'capital receipt', 'creat liabilit|create a liabilit|reduc asset|reduce an asset|either creat|liabilit or reduc|increase liabilit', min=2),
               P('p3', 'Examples on each side', 2, 'tax|dividend|fee', 'borrow|loan|disinvest|recover', min=2)], 'c4'),
            V('v3', 'Explain the roles of the Finance Bill and the Appropriation Bill.',
              'The Finance Bill gives effect to the tax proposals of the budget, that is imposing, abolishing or changing taxes, and Parliament must pass it within 75 days. The Appropriation Bill authorises the government to withdraw money from the Consolidated Fund of India to meet expenditure.',
              [P('p1', 'Finance Bill — gives effect to tax proposals', 4, ALT('finance bill {x}', 'finance bill give effect {x}', 'finance bill deal {x}', 'finance bill contain {x}', x=('tax', 'taxation', 'tax proposal', 'impos', 'levy'))),
               P('p2', 'Appropriation Bill — authority to spend from the Consolidated Fund', 4, ALT('appropriation bill {x}', 'appropriation bill authoris {x}', 'appropriation bill allow {x}', 'appropriation bill give authorit {x}', x=('withdraw', 'spend', 'expenditure', 'consolidated fund', 'authoris', 'authoriz', 'money'))),
               P('p3', '75 days for the Finance Bill', 2, '75|seventy five')], 'c3'),
            V('v4', 'What are the Consolidated Fund, the Contingency Fund and the Public Account of India?',
              'The Consolidated Fund receives all revenues, loans raised and loan repayments, and all government expenditure comes out of it, but only with Parliament\'s appropriation. The Contingency Fund is at the disposal of the President for urgent unforeseen expenditure and is later recouped. The Public Account holds money like provident funds and small savings where the government is only a banker, so Parliament\'s approval is not needed to pay it out.',
              [P('p1', 'Consolidated Fund — all revenue, loans; spending needs Parliament\'s appropriation', 4, 'consolidated', 'revenue|loan|all receipt|appropriat|parliament', min=2),
               P('p2', 'Contingency Fund — President; urgent unforeseen spending; recouped', 3, 'contingency', 'president|urgent|unforeseen|emergenc|recoup', min=2),
               P('p3', 'Public Account — government as banker (PF, small savings)', 3, 'public account', 'banker|provident|small saving|depositor|belong|trust', min=2)], 'c8'),
            V('v5', 'Who manages India\'s public debt, and what is the objective of debt management?',
              'The Reserve Bank of India, through its Internal Debt Management Department, manages the domestic marketable debt of the Centre and the States, such as dated securities and treasury bills. The Finance Ministry\'s Department of Economic Affairs looks after external debt. The objective is to meet the financing needs at the lowest long-term cost while keeping debt sustainable and developing the bond market.',
              [P('p1', 'RBI (IDMD) manages domestic marketable debt', 4, 'reserve bank|rbi|idmd|internal debt management', 'domestic|internal|dated securit|treasury bill|g secs|marketable', min=2),
               P('p2', 'External debt — Ministry of Finance / DEA', 3, 'external|foreign', 'ministry of finance|finance ministry|economic affairs|dea|government', min=2),
               P('p3', 'Objective — lowest long-term cost, sustainable debt, market development', 3, 'lowest cost|low cost|lowest possible|least cost|cheap|minimum cost|sustainab|bond market|market development', min=1)], 'c7'),
            V('v6', 'What is a guillotine and what is a cut motion in the budget process?',
              'A cut motion is a motion moved to reduce the amount of a demand for grant, for economy, policy difference or to voice a grievance. The guillotine is when, on the last day allotted, the Speaker puts all the remaining demands for grants to vote at once, whether discussed or not.',
              [P('p1', 'Cut motion — reduce the amount of a demand', 5, ALT('cut motion {r}', r=['reduc', 'cut down', 'lower', 'decreas'])),
               P('p2', 'Guillotine — all remaining demands put to vote together on the last day', 5, 'guillotin', 'all|remaining|outstanding|pending|together|at once', 'vote|voted|voting|pass', min=3)], 'c3'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Reading a small nation\'s budget', 'difficulty': 'hard',
            'case': ('The budget of a small nation (₹ crore): tax revenue 30,000; non-tax revenue 6,000; revenue expenditure 44,000 including interest payments of 7,000; capital expenditure 12,000; '
                     'recovery of loans 1,000; disinvestment 1,500; borrowings 17,500. No interest is received by the government.'),
            'mcqs': [
                M('k1a', 'Revenue deficit is:', ['₹8,000 crore', '₹14,000 crore', '₹2,000 crore', '₹20,000 crore'], 0, 'Revenue receipts = tax 30,000 + non-tax 6,000 = 36,000. Revenue deficit = revenue expenditure − revenue receipts = 44,000 − 36,000 = ₹8,000 crore. The tempting ₹14,000 crore ignores non-tax revenue (44,000 − 30,000); ₹20,000 crore wrongly compares total spending with revenue. In practice: a finance ministry analyst would flag this revenue deficit as borrowing to fund running costs.', 'c6', 'moderate', '44000-36000', topic='Public Debt Management'),
                M('k1b', 'Fiscal deficit is:', ['₹17,500 crore', '₹20,000 crore', '₹19,000 crore', '₹35,000 crore'], 0, 'Fiscal deficit = total expenditure − non-debt receipts = (44,000 + 12,000) − (36,000 + 1,000 + 1,500) = 56,000 − 38,500 = ₹17,500 crore, equal to borrowings. Traps: ₹20,000 crore ignores both non-debt capital receipts; ₹19,000 crore ignores disinvestment. In practice: matching the fiscal deficit with stated borrowings is a quick check analysts use to validate budget numbers.', 'c6', 'hard', '(44000+12000)-(36000+2500)', topic='Public Debt Management'),
                M('k1c', 'Primary deficit is:', ['₹10,500 crore', '₹24,500 crore', '₹1,000 crore', '₹17,500 crore'], 0, 'Primary deficit = fiscal deficit − interest payments = 17,500 − 7,000 = ₹10,500 crore. The tempting ₹24,500 crore adds interest; ₹17,500 crore is the fiscal deficit itself; ₹1,000 crore wrongly deducts interest from the revenue deficit (8,000 − 7,000). In practice: this figure shows how much new borrowing arises from current policy decisions, after excluding the cost of past debt.', 'c6', 'moderate', '17500-7000', topic='Public Debt Management'),
                M('k1d', 'Which statement is correct for this budget?', ['Nearly half of the borrowing finances revenue (current) expenditure', 'The budget is in surplus', 'All borrowing finances asset creation', 'There is no primary deficit'], 0, "Revenue deficit ÷ fiscal deficit = 8,000 ÷ 17,500 ≈ 45.7%, so nearly half of the borrowing pays for current (revenue) expenditure rather than asset creation. 'All borrowing finances asset creation' is the trap — that would need a zero revenue deficit. There is also a primary deficit of ₹10,500 crore, and no surplus. In practice: analysts treat a high revenue-to-fiscal-deficit ratio as a sign of poor-quality borrowing.", 'c6', 'moderate', topic='Public Debt Management'),
            ]}],
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


def _CR(*vals, **x):
    """figures in Rs crore: nums matches '5,690' and '5,690 crore' alike"""
    return _N(*vals, **x)


AUTO = {
    'q1': {
        's1': _CR(47500, 9400),
        's2': _K('3500|35000000000', 'recovery|disinvest|non debt|1200 2300'),
        's3': _CR(72000, 21000),
        's4': _CR(12000, 11200),
        's5': _N(44.76),
    },
    'q2': {
        's1': _CR(75500, 85000, 13500, 5000),
        's2': _K('rd 9500|revenue deficit 9500|85000 75500 9500|rd 95000000000|revenue deficit 95000000000|85000 75500 95000000000'),
        's3': _K('98500|985000000000|85000 13500|80500|805000000000|75500 5000', '18000|180000000000'),
        's4': _K('18000 14000 4000|18000 14000 40000000000|pd 4000|pd 40000000000|primary deficit 4000|primary deficit 40000000000|pd is 4000'),
    },
    'q3': {
        'extra_ok': True,
        's1': _N(4.85, 1.6),
        's2': _N(1.26),
        's3': _N(32.91),
        's4': _K('servic|past debt|three quarter|third|consumption|current spending|unproductive|quality|74 percent|interest burden'),
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
