"""CA Foundation · Paper 4 Business Economics · Chapter 7 Public Finance · Unit 1 Fiscal Functions: An Overview, Centre and State Finance.
Original explanations, numbers and questions; constitutional articles are cited by number only."""
from lib import *
from ca_viva import P, ALT, V

UID = 'fnd-p4-ch07-u01'


def M(i, q, o, a, e, c=None, d='core', check=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if c: m['concept'] = c
    if check: m['check'] = check
    return m


UP = ('increase', 'increases', 'raise', 'raises', 'boost', 'boosts', 'more', 'higher', 'step up', 'expand')
DOWN = ('cut', 'cuts', 'reduce', 'reduces', 'lower', 'lowers', 'decrease', 'decreases', 'less')
SP = ('spending', 'expenditure', 'spend')
TX = ('tax', 'taxes', 'taxation')
REC = ('recession', 'slump', 'downturn', 'depression', 'unemployment')
INF = ('inflation', 'boom', 'overheating', 'rising prices')


def build():
    # ---------------- Illustration 1: net divisible pool and vertical devolution ----------------
    c1 = Checks()
    gtr, cess, coll = 3800000, 460000, 40000
    ndp = c1.add('3800000-460000-40000', 'net divisible pool (₹ crore)')
    st = c1.add('3300000*41/100', "states' 41% share (₹ crore)")
    ce = c1.add('3300000-1353000', 'retained by the Union (₹ crore)')
    pct_gtr = c1.add('round(1353000/3800000*100,2)', "states' share as % of gross tax revenue")

    # ---------------- Illustration 2: horizontal distribution (15th FC weights) ----------------
    c2 = Checks()
    W = [('Income distance', 45), ('Population (2011)', 15), ('Area', 15), ('Forest and ecology', 10), ('Demographic performance', 12.5), ('Tax and fiscal effort', 2.5)]
    A = [40, 50, 30, 20, 60, 30]     # State A's share (%) under each criterion among the three states
    B = [25, 30, 45, 50, 26, 40]
    Cc = [35, 20, 25, 30, 14, 30]
    def wsum(s): return '(' + '+'.join(f'{w}*{x}' for (_, w), x in zip(W, s)) + ')/100'
    sa = c2.add(wsum(A), 'State A weighted share %')
    sb = c2.add(wsum(B), 'State B weighted share %')
    sc = c2.add(wsum(Cc), 'State C weighted share %')
    tot = c2.add(f'{sa}+{sb}+{sc}', 'shares add to 100')
    pool = 120000
    ra = c2.add(f'120000*{sa}/100', 'State A amount')
    rb = c2.add(f'120000*{sb}/100', 'State B amount')
    rc = c2.add(f'120000*{sc}/100', 'State C amount')
    horiz = table(['Criterion', 'Weight %', 'State A %', 'State B %', 'State C %'],
                  [[n, w, a, b, c] for (n, w), a, b, c in zip(W, A, B, Cc)] + [['Total of weights', 100, '', '', '']],
                  num=[1], total=True, title='Criterion shares of the three states')

    # ---------------- Illustration 3: GST split ----------------
    c3 = Checks()
    val = 250000
    cg = c3.add('250000*9/100', 'CGST 9%')
    sg = c3.add('250000*9/100', 'SGST 9%')
    ig = c3.add('250000*18/100', 'IGST 18%')

    # ---------------- Question checks ----------------
    q1c = Checks()
    q_ndp = q1c.add('2600000-310000-26000', 'NDP')
    q_st = q1c.add('2264000*41/100', 'states share')
    q_ce = q1c.add('2264000-928240', 'centre keeps')
    q_un = q1c.add('2600000-928240', 'Union keeps out of gross tax revenue')

    q2c = Checks()
    X = [30, 40, 20, 50, 30, 60]; Y = [70, 60, 80, 50, 70, 40]
    sx = q2c.add('(' + '+'.join(f'{w}*{x}' for (_, w), x in zip(W, X)) + ')/100', 'State X share %')
    sy = q2c.add('(' + '+'.join(f'{w}*{x}' for (_, w), x in zip(W, Y)) + ')/100', 'State Y share %')
    ax = q2c.add(f'80000*{sx}/100', 'State X amount')
    ay = q2c.add(f'80000*{sy}/100', 'State Y amount')

    # ---------------- MCQ checks ----------------
    m_ndp = '1500000-180000-20000'
    m_dev = '1300000*41/100'

    # ---------------- case ----------------
    k = Checks()
    k_ndp = k.add('2000000-250000-50000', 'NDP case')
    k_st = k.add('1700000*41/100', 'states case')
    k_14 = k.add('1700000*42/100', 'at 42%')
    k_diff = k.add('714000-697000', 'difference')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch07', 'n': 1,
        'title': 'Fiscal Functions: An Overview, Centre and State Finance',
        'outcomes': [
            'Explain why governments step into a market economy and state Musgrave\'s three fiscal functions — allocation, redistribution and stabilization.',
            'Classify any government measure (a subsidy, a tax change, a ban, a transfer payment) under the correct fiscal function.',
            'Describe how India divides taxing powers and spending duties between the Union, the States and local bodies (Article 246 lists, Articles 268–293).',
            'Explain the role of the Finance Commission (Article 280), vertical and horizontal devolution, the 41% share and the criteria used, and the federal design of GST.',
        ],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 50}, 'prereq': [],
                 'exam_tip': 'Most questions here are "which function is this?" or a fact about the Finance Commission or GST. Learn the three-function grid with two examples each, and the figures: 41% devolution (15th and 16th FC), 42% (14th FC), 28 States and 8 UTs.'},
        'concepts': [
            {'id': 'c1', 'title': 'Introduction — why the state has economic functions',
             'body': ['Even where markets decide most things, every government taxes, spends, borrows, employs people, makes rules and protects property. What it does — or leaves undone — shapes growth and the quality of life of citizens.',
                      'Macroeconomics names three national goals: (1) growth — real GDP rising faster than population so that living standards improve; (2) high employment — idle workers mean output lost for ever; (3) stable prices — inflation erodes real incomes and hurts poorer families most, while deflation signals slump and job losses.',
                      'Governments do not leave the economy to run on autopilot. They intervene because the purpose of an economic system is taken to be the welfare of households and individuals.'],
             'analogy': 'The market is the engine of a car; the government is the driver who steers, brakes and accelerates. A good engine still needs a driver on a winding road.',
             'work': 'Every Union Budget analysis a CA prepares for clients begins with these three goals — growth, jobs and inflation — because they decide tax rates, interest rates and demand for the client\'s products.'},
            {'id': 'c2', 'title': 'The role of government in an economic system — Musgrave\'s three branches',
             'body': ['Scarcity forces every society to answer what to produce, how, for whom, and how much to save for future capacity. Three systems answer these questions: the market (capitalism), the state (socialism) and a mix of both (mixed economy).',
                      'Adam Smith favoured a small but clear role for government: defence against external attack, a system of justice to keep internal order and protect property, and public works and institutions (roads, bridges, canals, harbours, postal service) that private profit-seekers would not build efficiently.',
                      'After the Great Depression of the 1930s the state took on economic (fiscal) functions in addition to these traditional ones.',
                      'Richard Musgrave (The Theory of Public Finance, 1959) split the government\'s economic role into three branches: allocation (for efficiency), redistribution (for fairness or equity) and stabilization (for price stability, full employment and growth). Allocation and redistribution are mainly microeconomic; stabilization is macroeconomic. The budget is the main vehicle through which all three are carried out.'],
             'blocks': [table(['Function', 'Aim', 'Typical tools'], [
                 ['Allocation', 'Efficiency — right goods in right quantities', 'Public provision, taxes and subsidies, bans, competition law, regulation'],
                 ['Redistribution', 'Equity — a fairer spread of income and wealth', 'Progressive taxes, subsidies, transfer payments, free or cheap services'],
                 ['Stabilization', 'Steady prices, full employment, growth', 'Fiscal policy (spending, taxes) and monetary policy (money supply, interest rates)']],
                 title='Musgrave\'s three-branch taxonomy')],
             'analogy': 'Think of a family kitchen: allocation decides what is cooked, redistribution decides who gets how big a share, and stabilization makes sure there is neither a feast one week nor hunger the next.',
             'work': 'When a client asks "how will this budget affect us?", a CA sorts the announcements into these three boxes — sector incentives (allocation), tax slabs and welfare schemes (redistribution), and the deficit or borrowing stance (stabilization).'},
            {'id': 'c3', 'title': 'The allocation function',
             'body': ['Resource allocation decides how scarce factors of production are spread across their many possible uses — and therefore how much of each good is produced. Allocative efficiency means producing the mix of goods that gives society the greatest value from given resources and technology.',
                      'Markets allocate through prices, consumer sovereignty and the profit motive; the state allocates through its revenue and spending decisions in the budget. Markets allocate efficiently only under perfect competition and rational choice, which never fully exist.',
                      'Sources of market failure that justify the allocation role: monopoly power (too little output at too high a price); public goods such as defence that markets do not supply; under-supply of merit goods such as education and health; over-use of common property resources such as the environment; externalities such as pollution; immobility of factors; imperfect information; and unequal income and wealth.',
                      'Through the budget the allocation function settles who and what is taxed, how much is spent and on what, the split of total resources among uses, the best mix of social goods (public and merit goods), the size of the public sector, and the shift of resources from private to public use.',
                      'Instruments: direct production (electricity, public transport); changing prices through taxes and subsidies (tax breaks for socially useful goods, heavy taxes on cigarettes and alcohol); legislation and force (a ban on single-use plastics stops resources flowing there); competition and merger policy (the Competition Act); regulation (licensing, controls, minimum wages, rules on where industry may locate); legal and administrative frameworks; or any combination.',
                      'In allocation the government complements the market; it does not replace it.'],
             'analogy': 'A traffic police officer does not drive anyone\'s car; he only redirects traffic where the signals (prices) give the wrong message.',
             'work': 'CAs in industry track allocation tools constantly — production-linked incentives, customs duty changes, a ban on a product category — because they change project viability and product pricing overnight.'},
            {'id': 'c4', 'title': 'The redistribution function',
             'body': ['Growth has raised total output enormously, but the gains are not spread evenly. Left to the market, income and wealth tend to be skewed, so the government acts to make the distribution more equal. This function answers the "for whom" question.',
                      'Two sides of the budget are used: the expenditure side (free or subsidised education, health care, housing, food and basic goods for the needy) and the revenue side (progressive taxation — higher rates on higher incomes).',
                      'Because effective demand depends on income, redistribution also changes how society\'s output is shared among households.',
                      'Aims: a fairer share of output for households, better lives for the deprived, equality of income, wealth and opportunity, and a minimum standard of living with basic needs secured.',
                      'Examples: progressive taxes combined with subsidies for poor households; highly subsidised food grains for BPL families; reservations, minimum wages and minimum support prices for farmers; unemployment benefits and transfer payments to the old, disabled and jobless; cash and in-kind aid to poor families; schemes for backward regions and vulnerable groups.',
                      'Equity–efficiency trade-off: redistribution that interferes with people\'s choices has efficiency costs (deadweight losses). Very high taxes on the rich can weaken the incentive to work, save, invest and take risks, shrinking output and future tax revenue. Good policy balances equity against efficiency and keeps the efficiency cost as small as possible.'],
             'analogy': 'Redistribution is like levelling a sports field: you want it fair, but if you dig too deep to level it, nobody can play on it.',
             'work': 'Tax practitioners see the trade-off directly: when slab rates rise, clients shift to lower-taxed forms of income or defer investment — exactly the disincentive the theory predicts.'},
            {'id': 'c5', 'title': 'The stabilization function',
             'body': ['An economy is macro-stable when output equals productive capacity, total spending equals total output, labour is fully employed and inflation is low and steady.',
                      'Rationale (Keynes): a market economy does not automatically deliver full employment and stable prices; business cycles are built in, so the government must act deliberately. Without action, recessions or inflation can drag on and hurt the poor most. Stagflation (inflation and unemployment together) and the contagion effect (instability spreading across countries through trade and finance) make the task harder.',
                      'The function looks at employment and capacity use, total output and income, the general price level, the balance of payments and the growth rate. The 2008 global crisis and the COVID-19 slump revived interest in counter-cyclical fiscal policy.',
                      'Tools: monetary policy (money supply and interest rates — by the central bank) and fiscal policy (government spending and taxes). Government spending puts money into the economy and lifts demand; taxes cut disposable income and reduce demand.',
                      'Recession or high unemployment → expansionary policy: raise spending, cut taxes, and/or increase money supply. High inflation → contractionary policy: cut spending, raise taxes, and/or reduce money supply. A deficit budget tends to stimulate activity; a surplus budget tends to slow it down.',
                      'Goals can conflict — pursuing one (say, growth) can endanger another (price stability); designing a budget that balances them is the real challenge.'],
             'analogy': 'Stabilization is the thermostat of the economy: switch on the heater (spend more, tax less) when it is cold, and the cooler when it overheats.',
             'work': 'Treasury and FP&A teams read the fiscal stance in the budget to forecast interest rates, demand and input costs for the coming year.'},
            {'id': 'c6', 'title': 'Centre and State finance — fiscal federalism and division of powers',
             'body': ['Fiscal federalism (a term from Musgrave) deals with how functions and finances are divided among levels of government. Musgrave argued that the central government should handle stabilization and redistribution, while allocation should rest mainly with state and local governments, which know local needs better.',
                      'India\'s federal structure has 28 States and 8 Union Territories. Each level is autonomous in its own sphere, and an independent judiciary settles disputes over division of powers.',
                      'Article 246 divides legislative powers into three lists: the Union List (only Parliament legislates), the State List (only State legislatures legislate) and the Concurrent List (both may legislate; if their laws conflict, the Union law prevails).',
                      'Union taxes include tax on non-agricultural income, corporation tax, customs and export duties, excise on certain goods, tax on the capital value of assets (excluding agricultural land), terminal taxes, securities transaction tax and CGST. State taxes include tax on agricultural income, on lands and buildings, mineral rights, electricity, vehicles, tolls and professions, land revenue, and excise on certain items (such as alcohol). Union property is exempt from State taxes, and State property and income are exempt from Union taxes.',
                      'Because States have fewer revenue sources than spending duties, they depend on transfers from the Union. Articles 268 to 281 govern the sharing: Art. 268 (certain duties the Union imposes but the States collect and keep), Art. 269 (taxes the Union both imposes and collects, whose proceeds are handed over to the States), Art. 270 (Union taxes whose proceeds are split between the Union and the States), Art. 271 (surcharges for the Union\'s own purposes), Art. 275 (statutory grants-in-aid to States in need). In addition, Art. 282 allows grants for any public purpose and Art. 293 deals with State borrowing.',
                      'Borrowing: under Article 292 the Union borrows on the security of the Consolidated Fund of India within limits fixed by Parliament; under Article 293 a State borrows within India on the security of its Consolidated Fund within limits set by its legislature. A State that still owes money to the Union needs the Union\'s consent to borrow.',
                      'Spending duties: the Union looks after defence, foreign affairs, foreign trade and exchange, money and banking, and inter-state transport and communication. States look after agriculture and industry support, health, education, police, and state roads. Local bodies (municipalities and panchayats) provide water supply, sanitation, local roads and electricity. Concurrent-list items are a shared responsibility.'],
             'analogy': 'A joint family business: the head office (Union) collects most of the money and runs the treasury; the branches (States) serve customers directly, so the head office must send them a fair share.',
             'work': 'Credit analysts and CAs who review State Development Loans or municipal bonds study how much a State earns on its own versus how much it receives from the Union — it decides the State\'s repayment capacity.'},
            {'id': 'c7', 'title': 'The Finance Commission (Article 280)',
             'body': ['Article 280 creates the Finance Commission — a constitutional body at the heart of Indian fiscal federalism. It reviews Union and State finances, recommends how Union taxes are shared, and lays down the principles for dividing the States\' share among them.',
                      'Its functions: (a) recommend the split of the net proceeds of shareable taxes between the Union and the States, and the share of each State; (b) recommend principles and amounts of grants-in-aid for States that need help; (c) suggest measures to strengthen a State\'s Consolidated Fund so that panchayats and municipalities get more resources (based on the State Finance Commission\'s advice); (d) any other matter the President refers to it for sound finance.',
                      'Vertical devolution decides what share of the Union\'s tax pool goes to all States together; horizontal devolution decides how that share is divided among the States.',
                      'The net divisible pool (NDP) is gross tax revenue minus cesses and surcharges (which are not shared) and cost of collection. Since the constitutional amendment of 2000, all Union taxes form part of the divisible pool.',
                      'Fifteenth Finance Commission (constituted 27 November 2017, after the Planning Commission was abolished and GST introduced): States\' share 41% for 2020-21 and 2021-26, against 42% recommended by the 14th FC for 2015-20; the 1% cut reflects the new Union Territories of Jammu and Kashmir and Ladakh, now funded by the Union.',
                      'Horizontal criteria used by the 15th FC (weights in brackets): income distance — how far a State\'s per-capita income is from the highest (45%); population 2011 (15%); area (15%); forest and ecology (10%); demographic performance — rewarding States that controlled population (12.5%); tax and fiscal effort (2.5%).',
                      'Sixteenth Finance Commission (chaired by Prof. Arvind Panagariya): recommended keeping the States\' share at 41% for the five years 2026-27 to 2030-31.', 'Real-world note (beyond the material): the 16th FC also revised the horizontal formula — income distance 42.5%, population (2011) 17.5%, demographic performance 10%, area 10%, forest 10% and a new criterion, contribution to GDP, 10% (tax and fiscal effort dropped). The study material lists only the 2021-26 (15th FC) criteria; use those in the exam.'],
             'blocks': [table(['Commission', 'Period', 'States\' share of divisible pool'], [['14th FC', '2015-20', '42%'], ['15th FC', '2020-21 and 2021-26', '41%'], ['16th FC (Arvind Panagariya)', '2026-27 to 2030-31', '41%']], title='Vertical devolution at a glance')],
             'analogy': 'The Finance Commission is the referee who decides, every five years, how the family income is split between the head office and the branches — and then among the branches.',
             'work': 'State budgets show "share in central taxes" as their biggest single receipt. A CA projecting a State\'s finances starts from the Finance Commission share and that State\'s horizontal percentage.'},
            {'id': 'c8', 'title': 'GST and Centre–State finance',
             'body': ['GST, rolled out on 1 July 2017, folded most indirect taxes (central excise, service tax, sales tax/VAT, octroi and entry tax) into one tax and made India\'s indirect tax system largely unified.',
                      'The Union levies and collects CGST; the States levy and collect SGST; for any supply, the CGST and SGST rates are equal. IGST applies to inter-state supplies and to imports; it equals CGST plus SGST, is collected and administered by the Union, held in a separate account, and shared between the Union and the destination State after input tax credit settlement.',
                      'GST is a destination (consumption) based tax, replacing the older production-based system. Manufacturing States feared losing revenue, so they were promised compensation for five years, funded by a compensation cess on certain luxury and demerit goods; compensation was extended beyond five years because of the pandemic slump.',
                      'GST forms about 35% of the Union\'s gross tax revenue and around 44% of the States\' own tax revenue.',
                      'In May 2022 the Supreme Court held that Parliament and State legislatures have equal, simultaneous powers to make GST laws, and that GST Council recommendations are persuasive, not binding.'],
             'analogy': 'GST works like a joint bank account opened by the Union and every State: each puts in an equal half (CGST and SGST), and for inter-state trade the Union collects the whole (IGST) and later passes the State its part.',
             'work': 'A GST practitioner must know the federal design — which tax applies (CGST + SGST or IGST) depends on the place of supply, and a wrong choice means paying tax to the wrong government and claiming a refund later.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Net divisible pool and the States\' 41% share', 'difficulty': 'core', 'minutes': 6,
             'q': f'For a year the Union\'s gross tax revenue is ₹{inr(gtr)} crore. Cesses and surcharges are ₹{inr(cess)} crore and the cost of collection is ₹{inr(coll)} crore. Applying the Finance Commission share of 41%, find (a) the net divisible pool, (b) the amount devolved to all States, (c) the amount the Union retains from the pool, and (d) the States\' share as a percentage of gross tax revenue.',
             'solution': [table(['Step', '₹ crore'], [['Gross tax revenue', gtr], ['Less: cesses and surcharges (not shared)', -cess], ['Less: cost of collection', -coll], ['Net divisible pool', ndp]], num=[1], total=True),
                          p(f'(b) States\' share = 41% × {inr(ndp)} = ₹{inr(st)} crore (vertical devolution).'),
                          p(f'(c) Union retains from the pool = {inr(ndp)} − {inr(st)} = ₹{inr(ce)} crore.'),
                          p(f'(d) As a share of gross tax revenue = {inr(st)} ÷ {inr(gtr)} × 100 = {pct_gtr}%. This is why States often say they receive "less than 41%" — cesses and surcharges stay with the Union.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Horizontal devolution using the 15th Finance Commission weights', 'difficulty': 'moderate', 'minutes': 10,
             'q': f'Three States A, B and C together receive ₹{inr(pool)} crore. The table gives each State\'s share (%) under each criterion. Using the 15th Finance Commission weights, find each State\'s overall share and amount.',
             'given': [horiz],
             'solution': [p('Overall share of a State = Σ (weight of criterion × State\'s share under that criterion) ÷ 100.'),
                          p(f'State A = (45×40 + 15×50 + 15×30 + 10×20 + 12.5×60 + 2.5×30) ÷ 100 = {sa}%'),
                          p(f'State B = (45×25 + 15×30 + 15×45 + 10×50 + 12.5×26 + 2.5×40) ÷ 100 = {sb}%'),
                          p(f'State C = (45×35 + 15×20 + 15×25 + 10×30 + 12.5×14 + 2.5×30) ÷ 100 = {sc}%  (check: {sa} + {sb} + {sc} = {tot}%)'),
                          table(['State', 'Share %', 'Amount ₹ crore'], [['A', sa, ra], ['B', sb, rb], ['C', sc, rc], ['Total', tot, pool]], num=[1, 2], total=True),
                          note('Income distance carries the heaviest weight (45%), so a poorer State — one far from the richest State\'s per-capita income — gains most. That is horizontal equity at work.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Who collects what under GST', 'difficulty': 'core', 'minutes': 5,
             'q': f'A trader in Maharashtra sells goods worth ₹{inr(val)} at an 18% GST rate. Find the tax and who receives it if (a) the buyer is in Maharashtra, (b) the buyer is in Karnataka.',
             'solution': [table(['Case', 'Tax', 'Amount ₹', 'Collected by'], [
                 ['(a) Intra-state', 'CGST 9%', cg, 'Union'], ['(a) Intra-state', 'SGST 9%', sg, 'Maharashtra'], ['(b) Inter-state', 'IGST 18%', ig, 'Union (later shared with the destination State, Karnataka)']]),
                 p(f'In (a) the total tax is ₹{inr(cg + sg)}, split equally between the Union and the State. In (b) the same ₹{inr(ig)} is collected wholly by the Union as IGST and the State share goes to the consuming State — GST is destination-based.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Classify the measure under Musgrave\'s functions', 'difficulty': 'core', 'minutes': 6,
             'q': 'Classify each measure: (1) a ban on single-use plastic; (2) free mid-day meals in government schools; (3) a cut in income tax rates during a recession; (4) building a national highway network; (5) old-age pension to poor citizens; (6) cutting government spending when inflation is 9%; (7) a heavy tax on cigarettes; (8) minimum support price for wheat.',
             'solution': [table(['Measure', 'Function', 'Reason'], [
                 ['1 Plastic ban', 'Allocation', 'Uses legislation to stop resources flowing into a harmful product'],
                 ['2 Mid-day meals', 'Redistribution', 'Free provision for poorer children (it also supports a merit good)'],
                 ['3 Tax cut in recession', 'Stabilization', 'Raises disposable income and aggregate demand'],
                 ['4 Highways', 'Allocation', 'Public provision of infrastructure markets under-supply'],
                 ['5 Old-age pension', 'Redistribution', 'Transfer payment to the vulnerable'],
                 ['6 Spending cut at 9% inflation', 'Stabilization', 'Contractionary policy to cool demand'],
                 ['7 Cigarette tax', 'Allocation', 'Price disincentive to a demerit good'],
                 ['8 MSP for wheat', 'Redistribution', 'Income support to farmers']])]},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Assessing a State\'s ability to repay its bonds', 'role': 'CA in a bank\'s treasury credit team',
             'situation': 'Your bank wants to invest in a State Development Loan. You must comment on the State\'s revenue base.',
             'steps': ['Split the State\'s revenue receipts into own tax revenue (SGST, excise on liquor, stamp duty, vehicle tax), own non-tax revenue, share in central taxes and grants-in-aid.',
                       'Check its horizontal share under the Finance Commission formula and whether it gets revenue-deficit grants under Article 275.',
                       'Note that GST compensation has ended, so revenue earlier protected at 14% growth must now come from the State\'s own SGST collections.',
                       'Check the borrowing limits set under Article 293 and whether the Union\'s consent is needed because the State owes the Union money.'],
             'takeaway': 'Federal transfers are a large, fairly stable part of State revenue; the risk lies in the State\'s own revenue and spending discipline.',
             'think': 'Why does a State that owes money to the Union need its consent before borrowing more?',
             'answer': 'Article 293 requires the Union\'s consent when a State has an outstanding loan from (or guaranteed by) the Union, so the Union can protect its exposure and overall fiscal discipline.'},
            {'id': 'j2', 'title': 'Explaining budget announcements to a board', 'role': 'CA working as a CFO\'s analyst',
             'situation': 'The board wants a one-page note on the new Union Budget.',
             'steps': ['Group announcements into allocation (sector incentives, customs changes, capital spending on roads), redistribution (tax slab changes, welfare schemes) and stabilization (fiscal deficit target and borrowing).',
                       'Link each to the company — e.g. a customs cut on inputs lowers cost; higher capital spending raises demand for cement and steel.',
                       'Flag the fiscal deficit path because it influences interest rates and borrowing costs.'],
             'takeaway': 'Musgrave\'s three boxes are a practical template for reading any budget.'},
            {'id': 'j3', 'title': 'Place of supply mistake', 'role': 'Articled assistant in a GST practice',
             'situation': 'A client charged CGST + SGST on a sale that was actually inter-state.',
             'steps': ['Identify that inter-state supplies attract IGST collected by the Union.', 'The client must pay IGST correctly and claim a refund of the CGST and SGST wrongly paid.', 'Explain to the client that the money went to the wrong government accounts — the Union and the origin State — rather than into the IGST pool shared with the destination State.'],
             'takeaway': 'The federal design of GST is not theory — it decides which government\'s account gets the tax.'},
        ],
        'mcqs': [
            M('m1', 'Who first split the economic role of government in a market economy into three branches?', ['Richard Musgrave', 'Adam Smith', 'J. M. Keynes', 'Paul Samuelson'], 0, 'Musgrave\'s "The Theory of Public Finance" (1959) separated allocation, redistribution and stabilization.', 'c2'),
            M('m2', 'Which of the following functions of government is macroeconomic in nature?', ['Stabilization', 'Allocation', 'Redistribution', 'Both allocation and redistribution'], 0, 'Allocation and redistribution are mainly microeconomic; stabilization deals with aggregate output, employment and prices.', 'c2'),
            M('m3', 'Adam Smith saw a role for government in all the following EXCEPT:', ['Fixing prices of consumer goods', 'National defence', 'A system of justice', 'Public works such as roads and harbours'], 0, 'Smith wanted a limited but defined role: defence, justice and public works/institutions. Price fixing goes against his free-market view.', 'c2'),
            M('m4', 'A government imposes a heavy tax on aerated sugary drinks to cut their consumption. This is mainly an example of the:', ['Allocation function', 'Redistribution function', 'Stabilization function', 'Monetary function'], 0, 'Using taxes to change prices and steer resources away from a harmful good is an allocation tool.', 'c3', 'moderate'),
            M('m5', 'Supply of food grains at highly subsidised prices to BPL families is an example of:', ['Redistribution', 'Allocation', 'Stabilization', 'Market failure'], 0, 'It shifts real income towards the poor — the distribution ("for whom") function.', 'c4'),
            M('m6', 'Redistribution policies are likely to carry efficiency costs mainly because:', ['They can weaken incentives to work, save and invest', 'Governments must stop collecting taxes', 'They always reduce government revenue to zero', 'They make markets perfectly competitive'], 0, 'High taxes and generous transfers can discourage effort and risk-taking — a deadweight loss.', 'c4', 'moderate'),
            M('m7', 'During a severe recession the appropriate stabilization measure is to:', ['Raise government spending and/or cut taxes', 'Cut government spending and raise taxes', 'Run a large budget surplus', 'Reduce the money supply'], 0, 'Expansionary policy lifts aggregate demand when output and employment are falling.', 'c5'),
            M('m8', 'A situation in which inflation and unemployment exist together is called:', ['Stagflation', 'Deflation', 'Contagion', 'Liquidity trap'], 0, 'Stagflation combines stagnation (unemployment) with inflation and makes stabilization harder.', 'c5'),
            M('m9', 'The "contagion effect" in the context of stabilization means:', ['Instability spreading from one country to others through trade and financial links', 'Rising prices of medicines', 'Tax evasion spreading among firms', 'Banks copying each other\'s interest rates'], 0, 'Greater international integration lets shocks travel easily across countries.', 'c5', 'moderate'),
            M('m10', 'Which statement is correct?', ['Fiscal policy uses taxes and government spending; monetary policy uses money supply and interest rates', 'Fiscal policy uses money supply; monetary policy uses taxes', 'Both use only price controls', 'Monetary policy is decided by Parliament through the budget'], 0, 'Fiscal = budget tools of the government; monetary = central bank tools.', 'c5'),
            M('m11', 'According to Musgrave, in a federation the allocation function should mainly be performed by:', ['State and local governments', 'The central government alone', 'The central bank', 'International agencies'], 0, 'Musgrave assigned stabilization and redistribution to the centre and allocation to lower levels, which know local preferences.', 'c6', 'moderate'),
            M('m12', 'Within a federation, which level of government is best placed to carry out stabilization?', ['The central government', 'Each State separately', 'Municipalities', 'Panchayats'], 0, 'Only the centre controls nation-wide tools — monetary policy, large borrowing, national taxes.', 'c6'),
            M('m13', 'Which Article of the Constitution divides legislative powers into the Union, State and Concurrent Lists?', ['Article 246', 'Article 280', 'Article 112', 'Article 293'], 0, 'Article 246 contains the three-list scheme; Art. 280 is the Finance Commission; Art. 112 the Annual Financial Statement; Art. 293 State borrowing.', 'c6'),
            M('m14', 'If a Union law and a State law on a Concurrent List subject conflict:', ['The Union law prevails', 'The State law prevails', 'Both become void', 'The Finance Commission decides'], 0, 'On concurrent subjects the law made by Parliament prevails in case of conflict.', 'c6'),
            M('m15', 'Which of these taxes can be levied ONLY by State governments?', ['Tax on agricultural income', 'Corporation tax', 'Customs duty', 'Securities transaction tax'], 0, 'Agricultural income is in the State list; the other three are Union taxes.', 'c6'),
            M('m16', 'Fiscal federalism refers to:', ['Division of economic functions and resources among different levels of government', 'Sharing of political power between parties', 'Management of monetary policy', 'Preparation of five-year plans'], 0, 'It is about who does what and who gets which revenues in a multi-level government.', 'c6'),
            M('m17', 'The body that recommends the sharing of Union taxes between the Union and the States is the:', ['Finance Commission', 'NITI Aayog', 'GST Council', 'Reserve Bank of India'], 0, 'Article 280 gives this task to the Finance Commission.', 'c7'),
            M('m18', 'Deciding the share of ALL States together in the Union\'s divisible tax pool is called:', ['Vertical devolution', 'Horizontal devolution', 'Fiscal drag', 'Revenue neutrality'], 0, 'Vertical = Union vs States; horizontal = among States.', 'c7'),
            M('m19', 'What share of the divisible pool did the Sixteenth Finance Commission recommend for the States for 2026-27 to 2030-31 (in %)?', ['41', '42', '32', '50'], 0, 'The 16th FC (Arvind Panagariya) kept the States\' share at 41%, the same as the 15th FC. The 14th FC had recommended 42%.', 'c7', 'core', '41'),
            M('m20', 'The 15th Finance Commission reduced the States\' share from 42% to 41% mainly because:', ['Jammu and Kashmir and Ladakh became Union Territories funded by the Union', 'GST revenues fell', 'The Planning Commission was revived', 'States asked for a lower share'], 0, 'The 1% adjustment provides for the new UTs from the Union\'s resources.', 'c7', 'moderate'),
            M('m21', 'Which of the following was NOT a criterion for horizontal distribution under the 15th Finance Commission?', ['Infrastructure performance', 'Income distance', 'Forest and ecology', 'Demographic performance'], 0, 'The criteria were income distance, population (2011), area, forest and ecology, demographic performance, and tax and fiscal effort.', 'c7', 'moderate'),
            M('m22', 'Under the 15th Finance Commission formula, the criterion with the highest weight is:', ['Income distance', 'Area', 'Population (2011)', 'Tax and fiscal effort'], 0, 'Income distance carries 45%; area and population 15% each; forest 10%; demographic performance 12.5%; tax effort 2.5%.', 'c7', 'hard'),
            M('m23', f'Gross tax revenue of the Union is ₹15,00,000 crore; cesses and surcharges ₹1,80,000 crore; cost of collection ₹20,000 crore. If States get 41% of the net divisible pool, the amount devolved is:',
              ['₹5,33,000 crore', '₹6,15,000 crore', '₹5,41,200 crore', '₹5,46,000 crore'], 0,
              'NDP = 15,00,000 − 1,80,000 − 20,000 = 13,00,000; 41% of it = 5,33,000. ₹6,15,000 wrongly applies 41% to gross revenue; ₹5,41,200 deducts only cesses; ₹5,46,000 uses 42%.', 'c7', 'hard', m_dev),
            M('m24', 'IGST on an inter-state supply is:', ['Levied and collected by the Union and shared with the destination State', 'Collected by the State where the supplier is located', 'Collected only by the destination State', 'Kept entirely by the Union'], 0, 'IGST = CGST + SGST, collected by the Union, kept in a separate account and apportioned after settlement.', 'c8'),
            M('m25', 'GST compensation was paid to:', ['States, for loss of revenue due to the introduction of GST', 'Industries that suffered losses under GST', 'Consumers of essential goods', 'Exporters for blocked input tax credit'], 0, 'Manufacturing States feared losses when tax moved from origin to destination; compensation was funded by a cess on luxury and demerit goods.', 'c8'),
            M('m26', 'As per the Supreme Court verdict of May 2022 on GST:', ['Parliament and State legislatures have equal, simultaneous powers to make GST laws', 'The Union\'s GST laws always prevail', 'GST Council recommendations bind all legislatures', 'States need the Union\'s permission to make GST rules'], 0, 'The Court held the powers equal and simultaneous, and the Council\'s recommendations persuasive, not binding.', 'c8', 'moderate'),
            M('m27', 'Providing health and education services is mainly the responsibility of:', ['State governments', 'The Union government', 'The RBI', 'The Finance Commission'], 0, 'Social sector services such as health and education, and police, are State functions.', 'c6'),
            M('m28', 'Water supply and sanitation are mainly provided by:', ['Local bodies such as municipalities and panchayats', 'The Union government', 'The Comptroller and Auditor General', 'Private monopolies by law'], 0, 'Local self-governments provide public utilities — water, sanitation, local roads, street lighting.', 'c6'),
            M('m29', 'Statutory grants-in-aid from the Union to States in need of assistance are made under:', ['Article 275', 'Article 268', 'Article 271', 'Article 292'], 0, 'Art. 275 provides statutory grants; Art. 282 gives discretionary grants for any public purpose.', 'c6', 'hard'),
            M('m30', 'Read the statements: (1) markets often allocate resources imperfectly; (2) government can correct every market failure at all times; (3) markets under-supply public goods. Which are correct?', ['1 and 3 only', '1, 2 and 3', '2 and 3 only', '3 only'], 0, 'Statement 2 is too strong — interventions can fail (government failure).', 'c3', 'moderate'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'From the following data of the Union for a year, compute (a) the net divisible pool, (b) the vertical devolution to States at 41%, (c) the amount the Union retains out of the pool, and (d) the amount the Union keeps out of gross tax revenue. Gross tax revenue ₹26,00,000 crore; cesses and surcharges ₹3,10,000 crore; cost of collection ₹26,000 crore.',
             'model': [table(['Step', '₹ crore'], [['Gross tax revenue', 2600000], ['Less: cesses and surcharges', -310000], ['Less: cost of collection', -26000], ['Net divisible pool', q_ndp]], num=[1], total=True),
                       p(f'(b) Devolution = 41% × {inr(q_ndp)} = ₹{inr(q_st)} crore.'),
                       p(f'(c) Union retains from the pool = {inr(q_ndp)} − {inr(q_st)} = ₹{inr(q_ce)} crore.'),
                       p(f'(d) Union keeps out of gross tax revenue = {inr(2600000)} − {inr(q_st)} = ₹{inr(q_un)} crore (pool share plus all cesses, surcharges and collection cost).')],
             'scheme': [{'id': 's1', 'pt': 'Correct deductions to arrive at the net divisible pool', 'm': 2, 'skill': 'computation'},
                        {'id': 's2', 'pt': '41% applied to the NDP (not to gross revenue)', 'm': 1, 'skill': 'application'},
                        {'id': 's3', 'pt': 'Union\'s retained share from the pool', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Union\'s total retention out of gross tax revenue', 'm': 1, 'skill': 'analysis'}],
             'remarks': ['Most candidates applied 41% straight to gross tax revenue.', 'Good answers stated why cesses and surcharges are excluded.'],
             'mistakes': ['Taking 42% (the 14th FC figure).', 'Forgetting the cost of collection.'],
             'tips': ['Lay the computation out as a short statement with "Less:" lines.', 'Label every figure in ₹ crore.'],
             'checks': q1c},
            {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'table',
             'q': 'Two States X and Y share ₹80,000 crore. Their shares (%) under the 15th FC criteria are — Income distance: X 30, Y 70; Population: X 40, Y 60; Area: X 20, Y 80; Forest and ecology: X 50, Y 50; Demographic performance: X 30, Y 70; Tax and fiscal effort: X 60, Y 40. Using the 15th FC weights (45, 15, 15, 10, 12.5, 2.5), compute each State\'s share and amount.',
             'model': [table(['Criterion', 'Weight', 'X %', 'Y %', 'X weighted', 'Y weighted'],
                             [[n, w, x, y, w * x / 100, w * y / 100] for (n, w), x, y in zip(W, X, Y)] + [['Total', 100, '', '', sx, sy]], num=[1, 4, 5], total=True),
                       p(f'X = {sx}% → ₹{inr(ax)} crore; Y = {sy}% → ₹{inr(ay)} crore. Total = ₹80,000 crore.'),
                       p('Y gets the larger share mainly because of income distance (45% weight) — Y is the poorer State.')],
             'scheme': [{'id': 's1', 'pt': 'Weights correctly recalled and applied', 'm': 2, 'skill': 'application'},
                        {'id': 's2', 'pt': 'Weighted shares computed for both States', 'm': 2, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Amounts computed and totals reconciled', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Interpretation linked to income distance / equity', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['A neat table earned full presentation credit.', 'Candidates who checked that the shares add to 100% caught their own errors.'],
             'mistakes': ['Treating all criteria equally.', 'Swapping the weights of demographic performance (12.5) and forest (10).'],
             'tips': ['Add a check line: X% + Y% = 100%.'],
             'checks': q2c},
            {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'core', 'pad': 'table',
             'q': 'Classify each measure under the allocation, redistribution or stabilization function, giving a one-line reason: (a) a carbon tax on coal-based power; (b) unemployment allowance; (c) a cut in GST rates on cars when demand is collapsing; (d) the government building rural roads; (e) progressive income tax slabs; (f) a reduction in government spending to control high inflation.',
             'model': [table(['Measure', 'Function', 'Reason'], [
                 ['(a) Carbon tax', 'Allocation', 'Makes the polluter pay; shifts resources away from a harmful activity'],
                 ['(b) Unemployment allowance', 'Redistribution', 'Transfer payment to the needy'],
                 ['(c) GST cut in a slump', 'Stabilization', 'Boosts aggregate demand during a downturn'],
                 ['(d) Rural roads', 'Allocation', 'Public provision of infrastructure the market under-supplies'],
                 ['(e) Progressive slabs', 'Redistribution', 'Higher burden on those with greater ability to pay'],
                 ['(f) Spending cut', 'Stabilization', 'Contractionary policy to remove excess demand']])],
             'scheme': [{'id': f's{i}', 'pt': f'Item ({ch}) correctly classified with reason', 'm': 1, 'skill': 'application'} for i, ch in enumerate('abcdef', 1)],
             'remarks': ['Reasons mattered: a bare label without a reason got half credit in practice sessions.'],
             'mistakes': ['Calling rural roads "redistribution" — they can help the poor, but the primary purpose is provision of infrastructure (allocation).', 'Calling the GST cut "allocation" when the context (collapsing demand) points to stabilization.'],
             'tips': ['Look for the context word: "recession/inflation" → stabilization; "poor/needy" → redistribution; "harmful/under-supplied" → allocation.']},
        ],
        'revision': {
            'summary': ['Musgrave (1959): allocation (efficiency), redistribution (equity), stabilization (prices, employment, growth). First two micro, third macro.',
                        'Allocation corrects market failure: monopoly, public goods, merit goods, common resources, externalities, factor immobility, imperfect information, inequality. Tools: direct production, taxes and subsidies, bans, competition law, regulation.',
                        'Redistribution: expenditure side (free/subsidised services, transfers) and revenue side (progressive taxes). Trade-off with efficiency.',
                        'Stabilization: recession → spend more / tax less / more money; inflation → the reverse. Deficit budgets stimulate, surplus budgets restrain.',
                        'Fiscal federalism: Art. 246 lists; Arts. 268–281 sharing; Art. 275 grants; Art. 280 Finance Commission; Arts. 292–293 borrowing.',
                        'FC share: 42% (14th), 41% (15th, 2021-26), 41% (16th, 2026-31). 15th FC criteria and weights: income distance 45, population 15, area 15, forest 10, demographic performance 12.5, tax effort 2.5.',
                        'GST from 1 July 2017: CGST = SGST rates; IGST collected by the Union and shared; compensation cess; SC (May 2022) — equal simultaneous powers, Council advice not binding.'],
            'remember': ['India = 28 States + 8 UTs.', 'NDP = gross tax revenue − cesses and surcharges − cost of collection.', 'Union: defence, foreign affairs, money and banking. States: health, education, police. Local bodies: water, sanitation.'],
            'traps': ['Allocation is assigned to States and local bodies in Musgrave\'s federal scheme — not to the centre.', '41% applies to the divisible pool, not to gross tax revenue.', 'GST subsumed mainly INDIRECT taxes, not direct taxes.', 'A heavy tax on a harmful good is allocation, not redistribution.'],
        },
        'quickref': [
            {'k': 'Three functions (Musgrave 1959)', 'v': 'Allocation – efficiency; Redistribution – equity; Stabilization – stable prices, full employment, growth'},
            {'k': 'Net divisible pool', 'v': 'Gross tax revenue − cesses & surcharges − cost of collection'},
            {'k': 'Vertical devolution', 'v': '41% of NDP to States (15th FC 2021-26; 16th FC 2026-31); 42% under 14th FC'},
            {'k': '15th FC criteria (weights)', 'v': 'Income distance 45 · Population 15 · Area 15 · Forest & ecology 10 · Demographic performance 12.5 · Tax & fiscal effort 2.5'},
            {'k': 'Key Articles', 'v': '246 lists · 268–271 tax sharing · 275 statutory grants · 280 Finance Commission · 282 discretionary grants · 292/293 borrowing'},
            {'k': 'GST', 'v': 'CGST (Union) + SGST (State), equal rates; IGST on inter-state & imports, collected by Union, shared with destination State'},
        ],
        'viva': [
            V('v1', 'Name the three fiscal functions of government given by Musgrave and the aim of each.',
              'Musgrave gave three functions. The allocation function aims at efficiency, so resources go to the right goods. The redistribution function aims at equity or fairness in income and wealth. The stabilization function aims at stable prices, full employment and growth.',
              [P('p1', 'Allocation — efficiency', 4, ALT('allocat {e}', '{e} allocat', e=('efficien', 'best use', 'optimal', 'optimum', 'right goods', 'proper use', 'aim efficien'))),
               P('p2', 'Redistribution — equity / fairness', 3, ALT('{d} {q}', '{q} {d}', '{d} income {q}', d=('redistribut', 'distribut'), q=('equity', 'equit', 'fair', 'just', 'equal'))),
               P('p3', 'Stabilization — stable prices, employment, growth', 3, ALT('stabili {x}', 'stabili keep {x}', 'stabili aim {x}', 'stabili function {x}', '{x} stabili', x=('price', 'employment', 'inflation', 'growth', 'business cycle', 'fluctuat', 'economy')))], 'c2'),
            V('v2', 'Why do redistribution policies carry an efficiency cost?',
              'Because very high taxes on the rich and very generous transfers weaken incentives. People may work less, save less, invest less and take fewer risks, so output and future tax revenue fall. This loss is called a deadweight loss, so equity has to be balanced against efficiency.',
              [P('p1', 'High taxes / generous transfers weaken incentives', 4, 'incentive|disincentive|discourag|demotivat|motivation', 'tax|transfer|benefit|subsid', min=1),
               P('p2', 'Less work, saving, investment or risk-taking', 3, 'work|sav|invest|risk|entrepreneur|effort'),
               P('p3', 'Output / revenue falls — deadweight loss; balance equity with efficiency', 3, 'deadweight|output fall|output fall|less output|lower output|growth|revenue|trade off|tradeoff|balanc', min=1)], 'c4'),
            V('v3', 'What fiscal action should a government take during a recession, and what during high inflation?',
              'In a recession the government should increase its spending and cut taxes so that aggregate demand rises. During high inflation it should do the opposite: reduce its spending and raise taxes to cut demand.',
              [P('p1', 'Recession: increase government spending (and/or cut taxes)', 5, ALT('{r} {u} {s}', '{u} {s} {r}', '{u} government {s} {r}', r=REC, u=UP, s=SP)),
               P('p2', 'Inflation: cut government spending (and/or raise taxes)', 5, ALT('{i} {d} {s}', '{d} {s} {i}', '{d} government {s} {i}', '{i} opposite', '{i} reverse', '{i} do opposite', '{i} do reverse', '{d} {s} {u} tax {i}', '{d} {s} {u} taxes {i}', i=INF, d=DOWN, s=SP, u=UP))], 'c5'),
            V('v4', 'What is the Finance Commission and what does it recommend?',
              'The Finance Commission is a constitutional body under Article 280. It recommends how the net proceeds of Union taxes are divided between the Union and the States, which is vertical devolution, and how the States\' share is divided among the States, which is horizontal devolution. It also recommends grants-in-aid to needy States and measures to strengthen resources of panchayats and municipalities.',
              [P('p1', 'Constitutional body under Article 280', 3, '280|constitution', min=1),
               P('p2', 'Share of Union taxes between Union and States (vertical)', 3, 'vertical|between union and state|between centre and state|between the centre and the state|union and state|centre and state', min=1),
               P('p3', 'Division among the States (horizontal)', 2, 'horizontal|among state|among the state|between state|each state', min=1),
               P('p4', 'Grants-in-aid / local bodies', 2, 'grant|panchayat|municipal|local bod', min=1)], 'c7'),
            V('v5', 'What share of the divisible pool goes to the States under the latest Finance Commission, and on what criteria is it divided among States?',
              'The Sixteenth Finance Commission kept the States\' share at 41 per cent for 2026-27 to 2030-31, the same as the Fifteenth. As per the study material, the criteria for dividing it among States, laid down for 2021-26, are income distance, population, area, forest and ecology, demographic performance, and tax and fiscal effort, with income distance carrying the largest weight of 45 per cent.',
              [P('p1', '41% of the divisible pool', 4, '41|forty one'),
               P('p2', 'Names at least three criteria', 4, 'income distance|income', 'population', 'area', 'forest|ecology', 'demographic', 'tax effort|fiscal effort|tax and fiscal', min=3),
               P('p3', 'Income distance has the highest weight (45%)', 2, '45|highest weight|largest weight|most weight|biggest weight', min=1)], 'c7'),
            V('v6', 'How is GST shared between the Union and the States?',
              'For a sale within a State, CGST goes to the Union and SGST goes to the State, and the two rates are equal. For an inter-state sale or an import, IGST is charged; the Union collects it and later passes the State share to the destination State. So GST is a destination based tax.',
              [P('p1', 'Intra-state: CGST to Union, SGST to State, equal rates', 4, 'cgst', 'sgst', 'equal|same|half|union|centre', min=2),
               P('p2', 'Inter-state: IGST collected by the Union', 4, 'igst|integrated', 'union|centre|central', 'inter state|interstate|import|another state|other state', min=2),
               P('p3', 'Shared with / goes to the destination (consuming) State', 2, 'destination|consum|buyer state|receiving state|shared|apportion', min=1)], 'c8'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Budget season in a federal country', 'difficulty': 'hard',
            'case': ('For the coming year the Union government of a federal country expects gross tax revenue of ₹20,00,000 crore, of which ₹2,50,000 crore is cesses and surcharges; '
                     'cost of collection is ₹50,000 crore. The Finance Commission has recommended that States receive 41% of the net divisible pool. The Finance Minister also announces: '
                     '(i) a 10% hike in excise on tobacco; (ii) a higher old-age pension for poor citizens; (iii) a cut in personal income tax because growth has slowed sharply.'),
            'mcqs': [
                M('k1a', 'What is the net divisible pool?', ['₹17,00,000 crore', '₹17,50,000 crore', '₹19,50,000 crore', '₹20,00,000 crore'], 0, 'NDP = 20,00,000 − 2,50,000 − 50,000 = 17,00,000.', 'c7', 'moderate', '2000000-250000-50000'),
                M('k1b', 'How much will be devolved to the States?', ['₹6,97,000 crore', '₹8,20,000 crore', '₹7,14,000 crore', '₹7,17,500 crore'], 0, f'41% × 17,00,000 = {inr(k_st)}. ₹8,20,000 applies 41% to gross revenue; ₹7,14,000 uses 42%; ₹7,17,500 ignores the cost of collection.', 'c7', 'hard', '1700000*41/100'),
                M('k1c', 'Had the 14th Finance Commission share applied, how much MORE would States have received?', ['₹17,000 crore', '₹20,000 crore', '₹1,700 crore', '₹2,00,000 crore'], 0, f'42% − 41% = 1% of 17,00,000 = {inr(k_diff)}.', 'c7', 'hard', '714000-697000'),
                M('k1d', 'Announcements (i), (ii) and (iii) relate respectively to which functions?', ['Allocation, redistribution, stabilization', 'Redistribution, allocation, stabilization', 'Stabilization, redistribution, allocation', 'Allocation, stabilization, redistribution'], 0, 'Tobacco tax steers resources away from a demerit good; pensions transfer income to the poor; a tax cut in a slowdown boosts demand.', 'c2', 'moderate'),
            ]}],
    }
