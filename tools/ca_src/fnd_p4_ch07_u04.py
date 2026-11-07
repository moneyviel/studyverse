"""CA Foundation · Paper 4 Business Economics · Chapter 7 Public Finance · Unit 4 Fiscal Policy.
Original explanations, numbers and questions."""
from lib import *
from ca_viva import P, ALT, V

UID = 'fnd-p4-ch07-u04'


def M(i, q, o, a, e, c=None, d='core', check=None, topic=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if topic: m['topic'] = topic
    if c: m['concept'] = c
    if check: m['check'] = check
    return m


EXP = ('expansionary', 'expansion', 'expand')
CON = ('contractionary', 'contraction', 'contract', 'restrictive')
UP = ('increase', 'increases', 'raise', 'raises', 'more', 'higher', 'boost', 'step up')
DOWN = ('cut', 'cuts', 'reduce', 'reduces', 'lower', 'lowers', 'decrease', 'less')
SP = ('spending', 'expenditure', 'spend')


def build():
    c1 = Checks()
    gap = c1.add('50000-46000', 'output gap (₹ crore)')
    k = c1.add('1/(1-0.8)', 'expenditure multiplier')
    dg = c1.add('4000/5', 'required rise in G')
    kt = c1.add('0.8/(1-0.8)', 'tax multiplier (absolute)')
    dt = c1.add('4000/4', 'required tax cut')

    c2 = Checks()
    k2 = c2.add('1/(1-0.75)', 'multiplier at MPC 0.75')
    dg2 = c2.add('1200/4', 'spending cut')
    kt2 = c2.add('0.75/(1-0.75)', 'tax multiplier')
    dt2 = c2.add('1200/3', 'tax increase')

    c3 = Checks()
    full = c3.add('1000*4', 'income rise without crowding out')
    net = c3.add('1000-400', 'net injection')
    act = c3.add('600*4', 'income rise with crowding out')
    lost = c3.add('4000-2400', 'income crowded out')
    pct = c3.add('1600/4000*100', '% of stimulus lost')

    c4 = Checks()
    bA = c4.add('500-500', 'budget A balance')
    bB = c4.add('560-500', 'budget B balance')
    bC = c4.add('500-580', 'budget C balance')

    q1 = Checks()
    q1g = q1.add('80000-74000', 'gap')
    q1k = q1.add('1/(1-0.75)', 'k')
    q1dg = q1.add('6000/4', 'ΔG')
    q1kt = q1.add('0.75/(1-0.75)', 'kt')
    q1dt = q1.add('6000/3', 'ΔT')

    q2 = Checks()
    q2k = q2.add('1/(1-0.9)', 'k at 0.9')
    q2f = q2.add('2000*10', 'full effect')
    q2n = q2.add('2000-500', 'net injection')
    q2a = q2.add('1500*10', 'actual')
    q2l = q2.add('20000-15000', 'lost')

    q3 = Checks()
    q3k = q3.add('1/(1-0.8)', 'k')
    q3dy = q3.add('900*5', 'ΔY from ΔG')
    q3kt = q3.add('0.8/(1-0.8)', 'kt')
    q3dyt = q3.add('900*4', 'ΔY from tax rise')
    q3net = q3.add('4500-3600', 'balanced budget effect')

    kk = Checks()
    kk1 = kk.add('1/(1-0.8)', 'case k')
    kk2 = kk.add('3000/5', 'case ΔG')
    kk3 = kk.add('3000/4', 'case ΔT')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch07', 'n': 4,
        'title': 'Fiscal Policy',
        'outcomes': [
            'Define fiscal policy, state its objectives and explain how it works through aggregate demand (GDP = C + I + G + NX).',
            'Distinguish expansionary and contractionary fiscal policy and match each to recession or inflation.',
            'Explain each instrument — government expenditure, taxes, public debt and the budget — and fiscal policy for long-run growth and for reducing inequality.',
            'Explain the limitations of fiscal policy: the four lags, timing problems, disincentives, deficit financing and crowding out; and compute simple multiplier effects.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 45, 'practice': 50}, 'prereq': ['fnd-p4-ch07-u01', 'fnd-p4-ch07-u03'],
                 'exam_tip': 'Remember the pairings: recession → expansionary (spend more, tax less, deficit); inflation → contractionary (spend less, tax more, surplus). Learn the four lags in order — recognition, decision, implementation, impact — and that crowding out is weak in a deep recession.'},
        'concepts': [
            {'id': 'c1', 'title': 'Introduction — what fiscal policy is',
             'body': ['Governments pursue many goals — fast growth, fair distribution, less poverty, stable prices and exchange rate, full employment and balanced regional development. The budget is one of the strongest tools, and its levers are public revenue (taxation), public expenditure, public debt and deficit financing. When these are used deliberately to achieve economic goals, public finance becomes fiscal policy.',
                      'Fiscal policy is the government\'s deliberate use of taxation, public spending and public borrowing to influence the pattern of economic activity and the level of aggregate demand, output and employment. It is a demand-side policy. An economy already at full employment does not need it.',
                      'Classical economists believed markets self-adjust and keep the economy at full employment with stable prices, so the government should just balance its budget. Before 1930, under laissez-faire, fiscal policy was not seen as a tool.',
                      'The Great Depression — very low demand and mass unemployment — could not be explained by classical theory. In 1936 J. M. Keynes, in "The General Theory of Employment, Interest and Money", argued for higher government spending to fight recession and unemployment. After the global financial crisis many countries again chose an active fiscal policy.'],
             'analogy': 'Classical economists saw the economy as a self-righting boat; Keynes saw a boat that can stay tipped over for years unless someone leans the other way.',
             'work': 'Every budget\'s fiscal stance — expansionary or tight — feeds directly into the demand forecasts that FP&A teams and equity analysts build.'},
            {'id': 'c2', 'title': 'Objectives of fiscal policy',
             'body': ['Objectives come from society\'s goals and differ by country, but the common ones are: achieving and maintaining full employment; price stability; faster economic development; and a fair distribution of income and wealth.',
                      'Priorities differ: developed countries may stress stability and equality; developing countries may put growth, jobs and equity first.',
                      'Fiscal policy works because it can change total output. From GDP = C + I + G + NX, the government controls G (its own purchases) directly and influences C (consumption), I (investment) and NX (net exports) indirectly through taxes, transfer payments and spending.'],
             'blocks': [table(['Component', 'How fiscal policy affects it'], [['C — private consumption', 'Income tax and transfer payments change disposable income'], ['I — investment', 'Corporate tax, incentives and public infrastructure change expected returns'], ['G — government purchases', 'Directly decided by the budget'], ['NX — net exports', 'Customs duties and export incentives change trade flows']], title='GDP = C + I + G + NX')],
             'analogy': 'The government holds one steering wheel (G) directly and has foot pedals (taxes, transfers) that nudge the other three drivers.',
             'work': 'Economists in banks and corporates model GDP growth by component; a budget raising capital expenditure lifts G and, through orders, I.'},
            {'id': 'c3', 'title': 'Types of fiscal policy — expansionary and contractionary',
             'body': ['Counter-cyclical fiscal policy adjusts revenue, spending and debt to fight unemployment in recessions and inflation in booms. It has two forms.',
                      'Expansionary fiscal policy is used in the contraction phase of the business cycle (or when a contraction is expected). A demand-deficient recession brings falling real GDP, weak demand and spending, and rising unemployment. The government closes this recessionary gap by cutting direct and indirect taxes (more purchasing power), raising government spending (money pumped into the economy), or both. It usually leads to a budget deficit.',
                      'Contractionary fiscal policy restrains activity in an inflationary phase or when a boom threatens inflation and asset bubbles — it closes an inflationary gap. It works through lower government spending, higher personal and business taxes (lower disposable income and investment; new entrants hold back), or both. It should reduce the deficit or create a surplus.',
                      'In short: in inflation (over-use of resources) fiscal policy curbs excess spending; in deflation or sluggish activity it makes up the shortfall in effective demand.'],
             'blocks': [table(['', 'Expansionary', 'Contractionary'], [['When', 'Recession / recessionary gap', 'Inflation / inflationary gap'], ['Spending', 'Increase', 'Decrease'], ['Taxes', 'Decrease', 'Increase'], ['Budget outcome', 'Deficit rises', 'Deficit falls / surplus'], ['Effect on AD', 'Raises', 'Lowers']], title='Two types of fiscal policy')],
             'analogy': 'Expansionary policy is pressing the accelerator on an uphill road; contractionary policy is braking on a steep downhill.',
             'work': 'During COVID-19 most governments ran expansionary policy; CAs saw it as loan guarantees, tax-payment deferrals and relief packages that clients had to account for.'},
            {'id': 'c4', 'title': 'Government expenditure as an instrument',
             'body': ['Public expenditure covers consumption, investment and transfer payments and is a large part of total spending, so changing it can shift national income significantly.',
                      'Three kinds: current expenditure (day-to-day running), capital expenditure (investment in equipment and infrastructure) and transfer payments (pensions, subsidies, relief — they move income between groups and do not add to GDP directly).',
                      'In a recession the government can start public works — roads, irrigation, sanitation, ports, rural electrification. These directly create incomes for workers and suppliers, and indirectly raise income further through the multiplier: incomes are spent on consumer goods, and how much is spent depends on the marginal propensity to consume (MPC). Since consumer-goods industries have idle capacity in a recession, output expands there too. Multiplier k = 1 ÷ (1 − MPC).',
                      'Financing: raising taxes would be self-defeating (it cuts disposable income), so the government runs a deficit financed by borrowing (which may crowd out private spending) or by monetisation (creating new money). Public investment also lifts business confidence; primary employment creates secondary and tertiary employment.',
                      'To fight inflation the government reduces its spending, which cuts incomes and removes excess demand.'],
             'analogy': 'A government contract is like a stone thrown in a pond — the first ring is the contractor\'s wages; the wider rings are the shops, farmers and transporters who earn from those wages.',
             'work': 'Infrastructure-heavy budgets lift order books of cement, steel and capital-goods companies — analysts track government capex as a lead indicator.'},
            {'id': 'c5', 'title': 'Taxes as an instrument',
             'body': ['Taxes are the main source of government revenue and a key stabilisation tool. Changing tax rates changes disposable income, private consumption and investment — and therefore aggregate demand and the inflationary or deflationary gap.',
                      'Recession: general income-tax cuts raise disposable income and consumption; lower corporate tax raises expected profits and investment. How big the tax cut (or spending rise) must be is decided by how large the recessionary gap is and by the multiplier.',
                      'Inflation: new taxes or higher rates absorb surplus purchasing power. But excessive taxation stifles investment, so tax increases must be used carefully.'],
             'analogy': 'Taxes are a tap on household pockets: open it wider (lower taxes) to let more money flow into spending; close it (higher taxes) to slow the flow.',
             'work': 'Corporate-tax rate changes (for example the 2019 reduction for new manufacturing companies) change investment decisions that CAs model in project appraisals.'},
            {'id': 'c6', 'title': 'Public debt and the budget as instruments',
             'body': ['Borrowing and repayment are powerful against both inflation and deflation. Internal debt is borrowed from people within the country; external debt from abroad.',
                      'Public debt takes two forms: market loans — treasury bills (short-term needs) and government securities/long-term bonds (capital projects) traded in debt markets — and small savings, which are non-negotiable, not traded (e.g. National Savings Certificates).',
                      'Selling bonds to the public withdraws money and curbs aggregate demand; repaying debt puts money back and raises demand.',
                      'The budget\'s net effect on demand depends on its balance. Balanced budget (spending = tax revenue): leakages equal injections, so no net effect (in this simple sense). Surplus (revenue > spending): leakages exceed injections — negative net effect; reduces national debt. Deficit (spending > revenue): injections exceed leakages — positive net effect; adds to national debt.'],
             'analogy': 'Bond sales are like a sponge soaking up money; repayment is squeezing the sponge back into the economy.',
             'work': 'Bond-market CAs watch the government\'s borrowing calendar: heavy borrowing pushes up G-sec yields and corporate borrowing costs.'},
            {'id': 'c7', 'title': 'Fiscal policy for long-run growth and for reducing inequality',
             'body': ['Demand management alone cannot give long-run growth; supply must grow too. Fiscal policy affects incentives: infrastructure spending provides overheads the private sector needs; public provision of education, health, nutrition and R&D builds human capital, which makes physical capital more productive; taxes can encourage or discourage saving and investment; a tax system that rewards innovation and enterprise helps growth (a corporate tax increase may hurt incentives); taxes and subsidies can correct externalities; environment taxes raise firms\' costs and reduce their output; input subsidies and support prices raise output.',
                      'Inequality: governments in developing countries use tax rates, tax structure and the level and direction of spending to tackle illiteracy, poverty, unemployment and inequality.',
                      'Tools: a progressive direct tax system (those with greater ability pay more); differential indirect taxes (heavy on luxuries, light or nil on necessities); targeted spending — poverty-alleviation programmes, free or subsidised health care, education, housing and essentials, selective infrastructure (rural roads, water for tribal areas), social security (old-age pension, unemployment relief, sickness allowance), subsidised mass-consumption goods, public production or subsidies for essentials, and building human capital for employability.',
                      'Caution: very high marginal tax rates and over-generous social programmes can discourage work, saving and investment.'],
             'analogy': 'Short-run fiscal policy waters the plant today; long-run fiscal policy improves the soil so the plant grows bigger every year.',
             'work': 'CSR and government-scheme advisory work by CAs often involves schemes designed under this redistributive fiscal logic.'},
            {'id': 'c8', 'title': 'Limitations of fiscal policy and crowding out',
             'body': ['Lags: recognition lag (data are slow and the economy is complex, so the need for action is noticed late); decision lag (time to evaluate options and choose); implementation lag (legislation and bureaucracy delay action, especially in a democracy); impact lag (results take time to appear).',
                      'Because of lags, policy may be badly timed — stimulus may arrive when recovery has already begun, and vice versa. Spending and tax policies cannot be changed instantly; cutting defence, social security or half-finished projects is hard; public works with long gestation (highways, dams) cannot follow the cycle, and urgent projects cannot be postponed.',
                      'Supply-side economists warn of disincentives: higher profit tax may reduce investment; higher social security may reduce work and saving. Deficit financing raises purchasing power faster than output in developing countries, causing inflation. Borrowing burdens future generations; unproductive use of borrowed money leaves too little surplus for servicing; external debt is a persistent problem.',
                      'Crowding out: an expansionary policy financed by heavy government borrowing reduces loanable funds and pushes up interest rates; interest-sensitive private investment and consumption fall. Government spending then replaces private spending, so the net rise in aggregate demand is smaller than expected and long-run growth may suffer.',
                      'In a deep recession crowding out is weak: private investment is already low, and the government can borrow without pushing up interest rates.',
                      'Conclusion: with idle capacity, higher demand raises output without raising prices; at full employment, expansionary policy only raises prices.'],
             'blocks': [table(['Lag', 'What causes the delay'], [['Recognition', 'Data take time; the problem is noticed late'], ['Decision', 'Evaluating alternatives and choosing a policy'], ['Implementation', 'Legislation and bureaucracy'], ['Impact', 'Effects take time to show in the economy']], title='The four lags')],
             'analogy': 'Crowding out is like two people trying to fill buckets from one tap: when the government brings a big bucket, the queue for the tap gets longer (interest rises) and some private buckets go home empty.',
             'work': 'When the government\'s borrowing programme is enlarged, corporate treasury teams brace for higher bond yields — crowding out in action.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Closing a recessionary gap', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'Full-employment GDP is ₹50,000 crore but equilibrium GDP is ₹46,000 crore. MPC = 0.8. By how much must the government (a) raise its spending, or (b) cut lump-sum taxes, to reach full employment?',
             'solution': [p(f'Output gap = 50,000 − 46,000 = ₹{inr(gap)} crore.'),
                          p(f'(a) Expenditure multiplier k = 1 ÷ (1 − 0.8) = {k}. Required ΔG = {inr(gap)} ÷ {k} = ₹{inr(dg)} crore.'),
                          p(f'(b) Tax multiplier (size) = MPC ÷ (1 − MPC) = 0.8 ÷ 0.2 = {kt}. Required tax cut = {inr(gap)} ÷ {kt} = ₹{inr(dt)} crore.'),
                          note('A tax cut needs to be bigger than a spending rise because part of each rupee of tax saved is saved, not spent.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Removing an inflationary gap', 'difficulty': 'moderate', 'minutes': 6,
             'q': 'Aggregate demand exceeds full-employment output so that equilibrium income is ₹1,200 crore above the full-employment level. MPC = 0.75. Find the cut in government spending, or the rise in taxes, needed.',
             'solution': [p(f'k = 1 ÷ (1 − 0.75) = {k2}; spending cut = 1,200 ÷ {k2} = ₹{dg2} crore.'),
                          p(f'Tax multiplier = 0.75 ÷ 0.25 = {kt2}; tax increase = 1,200 ÷ {kt2} = ₹{dt2} crore.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Crowding out reduces the stimulus', 'difficulty': 'hard', 'minutes': 7,
             'q': 'The government raises spending by ₹1,000 crore, financed by borrowing. The multiplier is 4. Higher interest rates reduce private investment by ₹400 crore. Find the rise in income with and without crowding out, and the share of the stimulus lost.',
             'solution': [table(['', 'No crowding out', 'With crowding out'], [['Net injection (₹ crore)', 1000, net], ['Multiplier', 4, 4], ['Rise in income (₹ crore)', full, act]]),
                          p(f'Income crowded out = {inr(full)} − {inr(act)} = ₹{inr(lost)} crore, i.e. {pct}% of the intended effect.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Reading the budget stance', 'difficulty': 'core', 'minutes': 4,
             'q': 'Three budgets (₹ crore): A — spending 500, taxes 500; B — spending 500, taxes 560; C — spending 580, taxes 500. Classify each and state its net effect on aggregate demand.',
             'solution': [table(['Budget', 'Taxes − spending', 'Type', 'Net effect on AD'], [['A', bA, 'Balanced', 'Neutral (leakages = injections)'], ['B', bB, 'Surplus', 'Negative — leakages exceed injections'], ['C', bC, 'Deficit', 'Positive — injections exceed leakages']])],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Sales forecast after a stimulus budget', 'role': 'CA in FP&A at a two-wheeler company',
             'situation': 'The budget cuts personal income tax and raises rural infrastructure spending.',
             'steps': ['Identify an expansionary fiscal stance.', 'Estimate higher disposable income in your customer segments; apply a demand elasticity.', 'Factor the multiplier effect in rural areas from road and irrigation projects.', 'Watch the government\'s borrowing plan — if it pushes up interest rates, vehicle loans become dearer (crowding out).'],
             'takeaway': 'Fiscal policy reaches company revenue through disposable income, government orders and interest rates.',
             'think': 'Why might the demand boost be smaller than hoped?', 'answer': 'Higher government borrowing can raise interest rates and crowd out interest-sensitive purchases such as vehicles bought on loan; lags may also delay the effect.'},
            {'id': 'j2', 'title': 'Relief package accounting', 'role': 'CA auditing an MSME',
             'situation': 'During a downturn the government offers tax deferrals and an interest subvention on working-capital loans.',
             'steps': ['Recognise these as expansionary fiscal measures.', 'Check eligibility and correct accounting (deferred liability, subsidy income).', 'Ensure deferred taxes are tracked for the due date.'],
             'takeaway': 'Expansionary policy often reaches firms as deferrals, guarantees and subsidies, each with its own accounting.'},
            {'id': 'j3', 'title': 'Explaining a tax hike', 'role': 'CA advising a high-net-worth family',
             'situation': 'An inflationary year brings a surcharge increase on high incomes.',
             'steps': ['Explain the contractionary and redistributive purpose.', 'Model the change in post-tax income.', 'Discuss legitimate planning without aggressive avoidance.'],
             'takeaway': 'The same tax change can serve both stabilisation and redistribution.'},
        ],
        'mcqs': [
            M('m1', 'Fiscal policy is best described as the use of:', ['Taxation, public expenditure and public borrowing to influence the economy', 'Money supply and interest rates', 'Price and wage controls only', 'Exchange-rate intervention'], 0, "Fiscal policy is the government's use of taxation, public expenditure and public borrowing — the budget — to influence output, employment, prices and distribution. 'Money supply and interest rates' is the trap: those are the tools of monetary policy, run by the central bank. In practice: the Union Budget's tax changes and capex allocations are fiscal policy, while RBI's repo-rate decisions are monetary policy; CAs advising clients track both.", 'c1', topic='Introduction'),
            M('m2', 'Fiscal policy is primarily a:', ['Demand-side policy', 'Supply-side policy only', 'Trade policy', 'Monetary policy'], 0, "Fiscal policy works mainly by changing aggregate demand — government spending adds to demand directly, while taxes and transfers change households' disposable income and hence consumption. 'Supply-side policy only' is the trap: some measures, such as infrastructure or tax incentives, do affect supply, but the primary channel is demand. In practice: a stimulus package in a slowdown is designed to lift demand quickly through spending and tax relief.", 'c1', topic='Introduction'),
            M('m3', 'Who advocated higher government spending to fight depression in "The General Theory" (1936)?', ['J. M. Keynes', 'Adam Smith', 'Milton Friedman', 'A. C. Pigou'], 0, "In The General Theory of Employment, Interest and Money (1936), J. M. Keynes argued that markets may not self-correct quickly and that higher government spending can lift a depressed economy. Milton Friedman is the trap — he is associated with monetarism and scepticism of activist fiscal policy. In practice: the case for public capex during India's Covid-era slowdown drew directly on Keynesian reasoning.", 'c1', topic='Introduction'),
            M('m4', 'According to classical economists, the government should:', ['Keep a balanced budget and avoid deliberate fiscal policy', 'Run large deficits in recessions', 'Nationalise all industries', 'Control all prices'], 0, "Classical economists believed flexible prices and wages keep the economy near full employment automatically, so government should keep a balanced budget and avoid deliberate (discretionary) fiscal policy. 'Run large deficits in recessions' is the trap — that is the Keynesian prescription. In practice: modern fiscal-rule debates, such as FRBM deficit targets, still reflect this classical concern for budget discipline.", 'c1', 'moderate', topic='Introduction'),
            M('m5', 'Which is NOT a usual objective of fiscal policy?', ['Maximising profits of public sector firms', 'Full employment', 'Price stability', 'Equitable distribution of income'], 0, "Fiscal policy's usual objectives are full employment, price stability, economic growth and development, and equitable distribution of income and wealth. Maximising profits of public sector firms is not a fiscal-policy objective. Equitable distribution is a tempting pick if you think fiscal policy is only about stabilisation, but it is a core objective. In practice: Budget speeches state goals like inclusive growth and fiscal consolidation, rarely PSU profit maximisation.", 'c2', topic='Objectives of Fiscal Policy'),
            M('m6', 'In GDP = C + I + G + NX, the component the government controls directly is:', ['G', 'C', 'I', 'NX'], 0, 'In GDP = C + I + G + NX, government purchases (G) are decided directly by the government through its budget. Consumption (C), investment (I) and net exports (NX) are private decisions that the government can influence only indirectly — via taxes, interest rates or trade policy. Choosing C is the trap, because taxes affect it but do not control it. In practice: in a slowdown, raising public capex is the quickest lever available.', 'c2', topic='Objectives of Fiscal Policy'),
            M('m7', 'Expansionary fiscal policy is appropriate when there is:', ['A recessionary gap', 'An inflationary gap', 'Full employment with rising prices', 'An asset bubble'], 0, "A recessionary gap means actual output is below full-employment output, so aggregate demand must rise; expansionary fiscal policy — more spending or lower taxes — fills that gap. 'Inflationary gap' is the trap: there demand already exceeds full-employment output, calling for contractionary policy. In practice: India's 2020-21 stimulus measures were expansionary because output had fallen well below its potential.", 'c3', topic='Types of Fiscal Policy'),
            M('m8', 'Which combination is contractionary?', ['Lower government spending and higher taxes', 'Higher government spending and lower taxes', 'Higher spending and higher transfers', 'Tax cuts and higher subsidies'], 0, "Lowering government spending reduces demand directly, and raising taxes reduces disposable income and consumption, so both together are contractionary. 'Higher spending and lower taxes' is the trap — that is expansionary. Higher transfers and subsidies also add to demand. In practice: governments use contractionary measures to cool inflation, for instance by cutting non-essential expenditure when prices are rising rapidly.", 'c3', topic='Types of Fiscal Policy'),
            M('m9', 'Expansionary fiscal policy usually leads to:', ['A larger budget deficit', 'A larger budget surplus', 'Lower public debt', 'No change in the budget balance'], 0, "Expansionary fiscal policy raises spending and/or cuts taxes, so expenditure rises relative to revenue and the budget deficit widens. 'A larger budget surplus' is the trap: surpluses arise from contractionary policy. Wider deficits must be financed by borrowing, which tends to raise public debt. In practice: India's fiscal deficit rose sharply in 2020-21 when the government expanded spending during the pandemic.", 'c3', topic='Types of Fiscal Policy'),
            M('m10', 'Transfer payments such as old-age pensions:', ['Do not add to GDP directly', 'Are counted as government purchases in GDP', 'Are capital expenditure', 'Are a tax'], 0, "Transfer payments such as old-age pensions move income from taxpayers to recipients without buying any current goods or services, so they do not add to GDP directly; they affect demand only when recipients spend. 'Counted as government purchases in GDP' is the trap — only actual purchases count in G. In practice: national accounts statisticians in India exclude pensions and scholarships from government final consumption expenditure.", 'c4', 'moderate', topic='The Instruments of Fiscal Policy'),
            M('m11', 'If MPC is 0.8, the government expenditure multiplier is:', ['5', '4', '1.25', '8'], 0, 'The spending multiplier is the reciprocal of the marginal propensity to save: MPS = 1 − 0.8 = 0.2, so the multiplier = 1 ÷ 0.2 = 5. The tempting 4 is the tax multiplier, MPC ÷ (1 − MPC) = 0.8 ÷ 0.2; 1.25 is 1 ÷ 0.8, which wrongly divides by MPC instead of MPS. In practice: economists estimating the impact of public capex on GDP use multiplier logic like this, though real-world multipliers are smaller because of leakages.', 'c4', 'moderate', '1/(1-0.8)', topic='The Instruments of Fiscal Policy'),
            M('m12', 'Full-employment income exceeds actual income by ₹4,000 crore; MPC = 0.8. The rise in government spending needed is:', ['₹800 crore', '₹1,000 crore', '₹3,200 crore', '₹20,000 crore'], 0, 'Required rise in spending = income gap ÷ multiplier. With MPC 0.8, k = 1 ÷ 0.2 = 5, so ΔG = 4,000 ÷ 5 = ₹800 crore. The tempting ₹1,000 crore is the tax cut needed (tax multiplier 4); ₹20,000 crore multiplies instead of dividing; ₹3,200 crore is 0.8 × 4,000. In practice: budget planners size stimulus packages by working backwards from the output gap in this way.', 'c4', 'hard', '4000/5', topic='The Instruments of Fiscal Policy'),
            M('m13', 'With MPC = 0.75 and an inflationary gap of ₹1,200 crore, the required increase in lump-sum taxes is:', ['₹400 crore', '₹300 crore', '₹900 crore', '₹4,800 crore'], 0, 'Tax multiplier = MPC ÷ (1 − MPC) = 0.75 ÷ 0.25 = 3, so the tax increase needed = 1,200 ÷ 3 = ₹400 crore. The tempting ₹300 crore is the spending cut needed, using the spending multiplier 1 ÷ 0.25 = 4; ₹900 crore is 0.75 × 1,200; ₹4,800 crore multiplies by 4. In practice: a tax rise must be larger than a spending cut for the same effect, because part of a tax change comes out of saving.', 'c5', 'hard', '1200/3', topic='The Instruments of Fiscal Policy'),
            M('m14', 'During a recession, financing extra spending by raising taxes is considered:', ['Self-defeating, as it reduces disposable income', 'The best option', 'Necessary to avoid deficits', 'Neutral for demand in every case'], 0, "In a recession, demand is already weak. Financing extra spending by raising taxes takes disposable income away from households, reducing consumption and cancelling much of the stimulus — so it is self-defeating. 'Necessary to avoid deficits' is the trap: avoiding deficits is not the priority in a slump. In practice: during downturns Indian governments usually borrow more rather than raise taxes, accepting a wider fiscal deficit.", 'c4', 'moderate', topic='The Instruments of Fiscal Policy'),
            M('m15', 'Creating additional money to finance government expenditure is called:', ['Monetisation', 'Crowding out', 'Disinvestment', 'Sterilisation'], 0, 'Monetisation means financing government spending by creating new money, typically through the central bank buying government securities. Crowding out is the trap — that is the reduction in private spending when government borrowing pushes up interest rates. In practice: India ended automatic monetisation through ad hoc treasury bills in 1997, and the FRBM Act restricts RBI from subscribing to primary issues of government securities except in specified circumstances.', 'c4', topic='The Instruments of Fiscal Policy'),
            M('m16', 'National Savings Certificates are an example of:', ['Small savings — non-negotiable public borrowing', 'Market loans traded in debt markets', 'Treasury bills', 'External debt'], 0, "National Savings Certificates are small-savings instruments sold through post offices; they are non-negotiable, meaning they cannot be traded in the market, and they form part of public borrowing. 'Market loans traded in debt markets' is the trap: dated G-secs are marketable, NSCs are not. In practice: tax advisors recommend NSCs to clients for Section 80C deductions under the old tax regime, and the money finances government spending.", 'c6', topic='The Instruments of Fiscal Policy'),
            M('m17', 'Selling government bonds to the public tends to:', ['Reduce aggregate demand', 'Increase aggregate demand', 'Leave money supply with the public unchanged', 'Reduce public debt'], 0, "When the public buys government bonds, money moves from private hands to the government; with less money to spend, private consumption and investment tend to fall, reducing aggregate demand. 'Reduce public debt' is the trap: selling bonds increases debt; repaying bonds reduces it. In practice: when the government sells large volumes of G-secs, bank liquidity tightens and analysts watch for higher bond yields.", 'c6', topic='The Instruments of Fiscal Policy'),
            M('m18', 'A balanced budget (spending = tax revenue) in the simple leakage–injection sense:', ['Has no net effect on aggregate demand', 'Always raises aggregate demand', 'Always lowers aggregate demand', 'Increases national debt'], 0, "In the simple leakage–injection view, a balanced budget means taxes (a leakage) equal government spending (an injection), so the two offset each other and there is no net effect on aggregate demand. 'Increases national debt' is the trap — a balanced budget requires no borrowing. In practice: a balanced budget stance is considered neutral, which is why stimulus usually requires running a deficit.", 'c6', 'moderate', topic='The Instruments of Fiscal Policy'),
            M('m19', 'A budget surplus:', ['Reduces aggregate demand and national debt', 'Increases aggregate demand', 'Adds to national debt', 'Has no effect on demand'], 0, "A budget surplus means taxes (leakages) exceed spending (injections), so aggregate demand falls; the extra revenue can also be used to repay debt, reducing national debt. 'Adds to national debt' is the trap — that is what deficits do. In practice: a government facing overheating and high debt might aim for a surplus to cool demand and pay down borrowings.", 'c6', topic='The Instruments of Fiscal Policy'),
            M('m20', 'Which fiscal measure supports long-run growth through human capital?', ['Public spending on education and health', 'A temporary cut in excise duty', 'Higher import duties on luxury cars', 'A one-time cash transfer'], 0, "Public spending on education and health builds human capital, raising the productivity of workers over many years — a long-run growth measure. A temporary excise cut and a one-time cash transfer are traps: they boost demand briefly but do not raise productive capacity. In practice: schemes like Samagra Shiksha and Ayushman Bharat are justified partly by their long-run effect on India's workforce productivity.", 'c7', topic='The Instruments of Fiscal Policy'),
            M('m21', 'Taxing luxuries heavily while exempting necessities mainly serves:', ['Reduction of inequality', 'Crowding out', 'Monetary transmission', 'Capital formation abroad'], 0, "Heavy taxes on luxuries and exemptions for necessities place more of the tax burden on richer consumers, who buy most luxuries, so the measure reduces inequality. 'Crowding out' is the trap — it concerns government borrowing displacing private spending, not tax design. In practice: under GST, many essential foods are exempt or at 5%, while luxury cars attract the highest rate plus cess, reflecting this equity logic.", 'c7', topic='The Instruments of Fiscal Policy'),
            M('m22', 'The delay between the need for policy action arising and the government realising it is the:', ['Recognition lag', 'Decision lag', 'Implementation lag', 'Impact lag'], 0, "The recognition lag is the time between when a problem arises and when policymakers realise it, because economic data arrive late and are often revised. 'Decision lag' is the trap: it starts after recognition, covering the time to choose a policy. In practice: India's quarterly GDP figures come out about two months after the quarter ends and are revised later, so a slowdown may be recognised only after it has begun.", 'c8', topic='The Instruments of Fiscal Policy'),
            M('m23', 'Delays in passing legislation and bureaucratic processes cause the:', ['Implementation lag', 'Recognition lag', 'Impact lag', 'Decision lag'], 0, "Even after a policy is decided, passing legislation and moving files through bureaucratic procedures takes time — the implementation lag. 'Recognition lag' is the trap: it occurs earlier, before the problem is even identified. In practice: a capex announcement in the Budget may take months to translate into actual contracts and payments on the ground, which is why stimulus effects arrive late.", 'c8', topic='The Instruments of Fiscal Policy'),
            M('m24', 'Crowding out occurs when:', ['Government borrowing raises interest rates and reduces private spending', 'Private investment rises after a tax cut', 'Exports exceed imports', 'The central bank cuts the repo rate'], 0, "Crowding out occurs when heavy government borrowing raises interest rates, making private borrowing costlier, so private consumption and investment fall and the stimulus is weakened. 'Private investment rises after a tax cut' is the trap — that is the opposite effect, called crowding in. In practice: when large government borrowing pushes up G-sec yields, corporate bond rates follow and companies may postpone projects.", 'c8', topic='The Instruments of Fiscal Policy'),
            M('m25', 'Crowding out is LEAST likely during:', ['A deep recession', 'A boom at full employment', 'High inflation', 'A period of very tight credit with strong private demand'], 0, "In a deep recession, private investment is already low and banks have idle funds, so government borrowing need not push interest rates up much — crowding out is least likely. 'A boom at full employment' is the trap: then funds are scarce and crowding out is strongest. In practice: this is why economists supported large public borrowing in 2020, when private demand for credit was weak.", 'c8', 'moderate', topic='The Instruments of Fiscal Policy'),
            M('m26', 'Government spending rises by ₹1,000 crore (multiplier 4), but private investment falls by ₹400 crore due to higher interest rates. The rise in income is:', ['₹2,400 crore', '₹4,000 crore', '₹1,600 crore', '₹5,600 crore'], 0, 'Net injection = ₹1,000 crore extra government spending − ₹400 crore crowded-out investment = ₹600 crore. Rise in income = 600 × multiplier 4 = ₹2,400 crore. The tempting ₹4,000 crore ignores crowding out; ₹1,600 crore is the income lost to crowding out (400 × 4); ₹5,600 crore wrongly adds the fall in investment. In practice: economists adjust stimulus estimates for crowding out like this.', 'c8', 'hard', '(1000-400)*4', topic='The Instruments of Fiscal Policy'),
            M('m27', 'If the economy is already at full employment, an expansionary fiscal policy will mainly:', ['Raise prices without raising output', 'Raise output without raising prices', 'Reduce prices', 'Reduce unemployment sharply'], 0, "At full employment there are no idle workers or machines, so extra demand from expansionary fiscal policy cannot raise output much; it pushes up prices instead. 'Raise output without raising prices' is the trap — that is possible only when resources are idle. In practice: when the economy is running near capacity, RBI often warns that additional fiscal stimulus could feed inflation.", 'c8', 'moderate', topic='The Instruments of Fiscal Policy'),
            M('m28', 'Which of the following is a limitation of fiscal policy?', ['Huge public projects with long gestation cannot be timed to the business cycle', 'It can change instantly', 'It has no effect on aggregate demand', 'It cannot affect income distribution'], 0, "Large public projects like highways and dams take years to plan and complete, so they cannot be switched on or off to match short-run swings in the business cycle; urgent ones cannot be postponed either. 'It can change instantly' is the trap — fiscal policy suffers from recognition, decision and implementation lags. In practice: by the time a road project funded for stimulus starts spending, the slowdown may already be over.", 'c8', topic='The Instruments of Fiscal Policy'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'Full-employment income is ₹80,000 crore; equilibrium income ₹74,000 crore; MPC = 0.75. Compute (a) the gap, (b) the expenditure multiplier and the required rise in government spending, (c) the tax multiplier and the required cut in lump-sum taxes. Name the type of policy.',
             'model': [p(f'(a) Gap = ₹{inr(q1g)} crore (recessionary).'), p(f'(b) k = 1 ÷ 0.25 = {q1k}; ΔG = 6,000 ÷ {q1k} = ₹{inr(q1dg)} crore.'), p(f'(c) Tax multiplier = 0.75 ÷ 0.25 = {q1kt}; tax cut = 6,000 ÷ {q1kt} = ₹{inr(q1dt)} crore.'), p('Policy: expansionary fiscal policy.')],
             'scheme': [{'id': 's1', 'pt': 'Gap identified as recessionary', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Multiplier and ΔG', 'm': 1.5, 'skill': 'computation'}, {'id': 's3', 'pt': 'Tax multiplier and ΔT', 'm': 1.5, 'skill': 'computation'}, {'id': 's4', 'pt': 'Policy named', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Most errors came from using the expenditure multiplier for the tax cut.'], 'mistakes': ['Multiplying the gap by k instead of dividing.'], 'tips': ['Write: required change = gap ÷ relevant multiplier.'], 'checks': q1},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'hard', 'pad': 'text',
             'q': 'MPC is 0.9. The government raises spending by ₹2,000 crore, financed by borrowing, which pushes up interest rates and cuts private investment by ₹500 crore. Compute the income effect with and without crowding out and the income lost. Explain why crowding out might be smaller in a deep recession.',
             'model': [p(f'k = 1 ÷ 0.1 = {q2k}. Without crowding out: 2,000 × {q2k} = ₹{inr(q2f)} crore. With crowding out: (2,000 − 500) × {q2k} = ₹{inr(q2a)} crore. Lost = ₹{inr(q2l)} crore.'),
                       p('In a deep recession private investment is already low and loanable funds are plentiful, so government borrowing need not raise interest rates — little is crowded out.')],
             'scheme': [{'id': 's1', 'pt': 'Multiplier', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'Both income effects', 'm': 2, 'skill': 'computation'}, {'id': 's3', 'pt': 'Income lost', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'Recession reasoning', 'm': 1, 'skill': 'analysis'}],
             'remarks': ['Good answers linked crowding out to the interest rate mechanism.'], 'mistakes': ['Subtracting 500 from final income instead of from the injection.'], 'tips': ['Net injection first, multiplier second.'], 'checks': q2},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'hard', 'pad': 'text',
             'q': 'MPC = 0.8. The government raises spending by ₹900 crore and finances it fully by raising lump-sum taxes by ₹900 crore. Compute the effect of each on income separately and the net effect. What does this suggest about a "balanced budget" change?',
             'model': [p(f'Spending effect = 900 × {q3k} = +₹{inr(q3dy)} crore. Tax effect = −900 × {q3kt} = −₹{inr(q3dyt)} crore. Net = +₹{q3net} crore.'),
                       p('A balanced increase in spending and taxes still raises income — here by exactly the amount of the spending (balanced-budget multiplier of 1) — because each rupee of tax reduces consumption by only MPC × 1 rupee. The "no net effect" of a balanced budget holds only in the simple leakage–injection sense.')],
             'scheme': [{'id': 's1', 'pt': 'Spending effect', 'm': 1.5, 'skill': 'computation'}, {'id': 's2', 'pt': 'Tax effect', 'm': 1.5, 'skill': 'computation'}, {'id': 's3', 'pt': 'Net effect', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'Interpretation', 'm': 1, 'skill': 'analysis'}],
             'remarks': ['This goes one step beyond the study material — useful for understanding, rarely asked directly.'], 'mistakes': ['Assuming the effects cancel completely.'], 'tips': ['Keep signs clear: tax rise has a negative effect.'], 'checks': q3},
        ],
        'revision': {
            'summary': ['Fiscal policy: deliberate use of taxes, spending and borrowing to influence demand, output and employment — a demand-side policy. Keynes (1936) vs classical balanced-budget view.',
                        'Objectives: full employment, price stability, faster development, equitable distribution. GDP = C + I + G + NX.',
                        'Expansionary (recession): ↑G, ↓T → deficit. Contractionary (inflation): ↓G, ↑T → smaller deficit or surplus.',
                        'Instruments: expenditure (current, capital, transfers; multiplier = 1/(1 − MPC)); taxes; public debt (market loans, small savings; bond sales curb demand, repayment raises it); budget (balanced neutral, surplus contractionary, deficit expansionary).',
                        'Long-run growth: infrastructure, human capital, growth-friendly taxes. Inequality: progressive taxes, differential indirect taxes, targeted spending.',
                        'Limitations: recognition, decision, implementation, impact lags; timing; rigid spending; disincentives; inflationary deficit financing; debt burden; crowding out (weak in deep recession).'],
            'remember': ['Spending multiplier 1/(1 − MPC); tax multiplier MPC/(1 − MPC).', 'At full employment, expansion only raises prices.'],
            'traps': ['Transfer payments are not part of G in GDP.', 'A tax cut must be bigger than a spending rise for the same effect.', 'Crowding out is weak, not strong, in a deep recession.'],
        },
        'quickref': [
            {'k': 'Expenditure multiplier', 'v': 'k = 1 ÷ (1 − MPC); ΔG needed = gap ÷ k'},
            {'k': 'Tax multiplier (size)', 'v': 'MPC ÷ (1 − MPC); ΔT needed = gap ÷ tax multiplier'},
            {'k': 'Expansionary vs contractionary', 'v': 'Recession: ↑G, ↓T (deficit) · Inflation: ↓G, ↑T (surplus)'},
            {'k': 'Four lags', 'v': 'Recognition → Decision → Implementation → Impact'},
            {'k': 'Budget balance effect', 'v': 'Balanced: neutral · Surplus: ↓AD, ↓debt · Deficit: ↑AD, ↑debt'},
            {'k': 'Crowding out', 'v': 'Govt borrowing → ↑interest → ↓private I and C → smaller net stimulus'},
        ],
        'viva': [
            V('v1', 'What is fiscal policy and what are its main objectives?',
              'Fiscal policy is the deliberate use of government spending, taxation and public borrowing to influence aggregate demand, output and employment. Its main objectives are full employment, price stability, faster economic growth and a fair distribution of income and wealth.',
              [P('p1', 'Use of spending, taxes and borrowing', 4, 'spend|expenditur', 'tax|taxes|taxation', 'borrow|debt|public debt', min=2),
               P('p2', 'To influence aggregate demand / output / employment', 2, 'aggregate demand|demand|output|economic activit|economy', min=1),
               P('p3', 'Objectives — at least three of employment, price stability, growth, equity', 4, 'employment|unemploy|job', 'price stabilit|stable price|inflation', 'growth|development', 'distribut|equit|inequalit|fair', min=3)], 'c1'),
            V('v2', 'Distinguish between expansionary and contractionary fiscal policy.',
              'Expansionary fiscal policy is used in a recession to close a recessionary gap; the government increases its spending and cuts taxes, which usually widens the budget deficit. Contractionary fiscal policy is used during inflation to close an inflationary gap; the government cuts its spending and raises taxes, reducing the deficit or creating a surplus.',
              [P('p1', 'Expansionary: in recession, more spending / lower taxes', 5, ALT('{e} {r}', '{e} used {r}', '{e} fiscal policy {r}', '{e} fiscal policy used {r}', '{e} {u} {s}', '{e} government {u} {s}', '{e} fiscal policy {u} {s}', e=EXP, r=('recession', 'slump', 'depression', 'recessionary', 'downturn'), u=UP, s=SP)),
               P('p2', 'Contractionary: in inflation, less spending / higher taxes', 5, ALT('{c} {i}', '{c} used {i}', '{c} fiscal policy {i}', '{c} fiscal policy used {i}', '{c} {d} {s}', '{c} government {d} {s}', '{c} fiscal policy {d} {s}', c=CON, i=('inflation', 'inflationary', 'boom', 'overheat'), d=DOWN, s=SP))], 'c3'),
            V('v3', 'Name and explain the lags in fiscal policy.',
              'There are four lags. The recognition lag is the delay in realising that action is needed because data come late. The decision lag is the time taken to choose the right policy. The implementation lag is the delay in passing laws and carrying out the policy through the bureaucracy. The impact lag is the time before the policy actually affects the economy.',
              [P('p1', 'Recognition lag', 3, 'recogni|identif|realis|realiz|notic', min=1),
               P('p2', 'Decision lag', 2, 'decision|decid|choos', min=1),
               P('p3', 'Implementation lag', 3, 'implement|legislat|bureaucra|carry out|execut', min=1),
               P('p4', 'Impact lag', 2, 'impact|effect take time|outcome|result take time', min=1)], 'c8'),
            V('v4', 'What is crowding out? When is it less likely?',
              'Crowding out happens when the government borrows heavily to finance a deficit, which pushes up interest rates and reduces private investment and consumption, so government spending replaces private spending and the stimulus is smaller. It is less likely in a deep recession, when private investment is already low and the government can borrow without raising interest rates.',
              [P('p1', 'Government borrowing raises interest rates', 4, 'borrow|deficit', 'interest rate|interest|cost of borrow', min=2),
               P('p2', 'Private investment / spending falls — replaced by government spending', 3, 'private', 'invest|spend|consum', 'fall|reduc|declin|lower|replac|less|discourag|crowd', min=3),
               P('p3', 'Less likely in a deep recession', 3, ALT('{l} {r}', '{r} {l}', '{l} during {r}', '{l} in {r}', '{l} deep {r}', '{l} during deep {r}', 'weak {r}', 'small {r}', 'minimal {r}', l=('less likely', 'unlikely', 'not likely', 'less', 'weak', 'small', 'minimal', 'little'), r=('recession', 'depression', 'slump', 'downturn')))], 'c8'),
            V('v5', 'How does the budget balance affect aggregate demand?',
              'A balanced budget has no net effect on aggregate demand because spending equals tax revenue and injections equal leakages. A budget surplus reduces aggregate demand because leakages exceed injections, and it reduces national debt. A budget deficit increases aggregate demand because injections exceed leakages, and it adds to national debt.',
              [P('p1', 'Balanced — neutral / no net effect', 3, ALT('balanced {x}', 'balanced budget {x}', x=('no net effect', 'no effect', 'neutral', 'equal', 'no change', 'not affect'))),
               P('p2', 'Surplus — reduces aggregate demand', 4, ALT('surplus {x}', 'surplus budget {x}', 'surplus {x} demand', x=('reduc', 'lower', 'decreas', 'negative', 'contract', 'fall', 'cut'))),
               P('p3', 'Deficit — raises aggregate demand', 3, ALT('deficit {x}', 'deficit budget {x}', 'deficit {x} demand', x=('increas', 'raise', 'positive', 'expand', 'boost', 'stimulat', 'more')))], 'c6'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'A finance minister\'s dilemma', 'difficulty': 'hard',
            'case': ('A country\'s equilibrium income is ₹3,000 crore below its full-employment level and MPC is 0.8. Private investment is weak and banks are flush with funds. '
                     'The finance minister must choose between more public works and a cut in personal income tax. Opposition members warn that borrowing will crowd out private investment.'),
            'mcqs': [
                M('k1a', 'What rise in government spending would close the gap?', ['₹600 crore', '₹750 crore', '₹2,400 crore', '₹15,000 crore'], 0, 'With MPC = 0.8, the spending multiplier = 1 ÷ (1 − 0.8) = 5. Required rise in government spending = gap ÷ multiplier = 3,000 ÷ 5 = ₹600 crore. The tempting ₹750 crore is the tax cut needed (tax multiplier 4); ₹15,000 crore multiplies instead of dividing; ₹2,400 crore is 0.8 × 3,000. In practice: the finance ministry would use this estimate when deciding the size of a public-works programme.', 'c4', 'moderate', '3000/5', topic='The Instruments of Fiscal Policy'),
                M('k1b', 'What cut in lump-sum taxes would close the gap instead?', ['₹750 crore', '₹600 crore', '₹3,750 crore', '₹2,400 crore'], 0, 'Tax multiplier = MPC ÷ (1 − MPC) = 0.8 ÷ 0.2 = 4, so the tax cut needed = 3,000 ÷ 4 = ₹750 crore. The tempting ₹600 crore is the spending rise needed, which is smaller because spending enters demand fully while part of a tax cut is saved. ₹3,750 crore divides by 0.8. In practice: this is why a tax-cut stimulus must be larger than a spending stimulus for the same impact on income.', 'c5', 'hard', '3000/4', topic='The Instruments of Fiscal Policy'),
                M('k1c', 'Is the opposition\'s crowding-out worry strong here?', ['No — private investment is weak and funds are plentiful, so interest rates need not rise much', 'Yes — crowding out is strongest in recessions', 'Yes — any borrowing fully crowds out private spending', 'No — because taxes will rise'], 0, "Crowding out happens when government borrowing pushes up interest rates and squeezes private investment. Here private investment is weak and banks are flush with funds, so rates need not rise much and crowding out will be small. 'Crowding out is strongest in recessions' is the trap — it is strongest at full employment. In practice: economists judge crowding-out risk by checking bank liquidity and credit demand before advising on borrowing.", 'c8', 'moderate', topic='The Instruments of Fiscal Policy'),
                M('k1d', 'Either option is an example of:', ['Expansionary fiscal policy', 'Contractionary fiscal policy', 'Monetary policy', 'A budget surplus policy'], 0, "More public works raises government spending, and a personal income-tax cut raises disposable income — both increase aggregate demand to close a recessionary gap, so either is expansionary fiscal policy. 'Monetary policy' is the trap: these are budget tools, not changes in money supply or interest rates. In practice: Budget announcements of higher capex or tax relief during a slowdown are classic expansionary fiscal moves.", 'c3', 'core', topic='Types of Fiscal Policy'),
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
        's1': _K('recessionary|deflationary|recession', '6000|60000000000'),
        's2': _K('k 4|multiplier 4|1 0.25 4|0.25 4|multiplier is 4|1 0.75 4|0.75 4', '1500|15000000000'),
        's3': _K('0.75 0.25 3|tax multiplier 3|tax multiplier is 3|multiplier 3', '2000|20000000000'),
        's4': _K('expansionary|expansionist|easy fiscal|expansion'),
    },
    'q2': {
        'extra_ok': True,
        's1': _K('k 10|multiplier 10|1 0.1 10|0.1 10|multiplier is 10|1 0.9 10|0.9 10'),
        's2': _CR(20000, 15000),
        's3': _CR(5000),
        's4': _K('low|idle|plentiful|surplus|excess|spare|weak|unused', 'investment|fund|interest|saving|capacity'),
    },
    'q3': {
        'extra_ok': True,
        's1': _CR(4500),
        's2': _K('-3600|3600|-36000000000|36000000000'),
        's3': _K('net 900|900 net|4500 3600 900|net effect 900|rise 900|increase 900|income 900|net 9000000000|9000000000 net|4500 3600 9000000000|net increase 900|net rise 900'),
        's4': _K('balanced budget multiplier 1|multiplier 1|multiplier of 1|multiplier one|raise income|increase income|income rise|income increase|not neutral|unity|expansionary'),
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
