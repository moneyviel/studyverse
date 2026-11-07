"""CA Foundation · Paper 4 Business Economics · Chapter 5 Determination of National Income · Unit 2 The Keynesian Theory of Determination of National Income.
Original explanations, numbers and questions. Every figure is computed in code and re-checked by tools/ca_validate.py."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch05-u02'


def Q(i, q, o, a, e, c, d='core', check=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'concept': c, 'difficulty': d}
    if check: m['check'] = check
    return m


def M(i, q, o, a, e, d='moderate', check=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if check: m['check'] = check
    return m


def build():
    # ---------- Illustration 1: consumption and saving schedule, C = 60 + 0.8Y ----------
    c1 = Checks()
    rows1 = []
    for y in [0, 100, 200, 300, 400, 500]:
        cc = c1.add(f'60+0.8*{y}', f'C at Y {y}')
        ss = c1.add(f'{y}-(60+0.8*{y})', f'S at Y {y}')
        if y:
            apc = c1.add(f'(60+0.8*{y})/{y}', f'APC at {y}')
            aps = c1.add(f'({y}-(60+0.8*{y}))/{y}', f'APS at {y}')
            rows1.append([str(y), str(cc), str(ss), str(apc), str(aps), '0.8', '0.2'])
        else:
            rows1.append(['0', str(cc), str(ss), '—', '—', '—', '—'])
    be = c1.add('60/(1-0.8)', 'break-even income where C = Y')
    t1 = table(['Income Y (₹ crore)', 'Consumption C', 'Saving S = Y − C', 'APC = C/Y', 'APS = S/Y', 'MPC', 'MPS'], rows1, num=[0, 1, 2], title='Consumption function C = 60 + 0.8Y')

    # ---------- Illustration 2: two-sector equilibrium ----------
    c2 = Checks()
    y2 = c2.add('(150+250)/(1-0.75)', 'equilibrium Y = (a + I)/(1 - b)')
    cc2 = c2.add('150+0.75*1600', 'C at equilibrium')
    s2 = c2.add('1600-1350', 'S at equilibrium')
    k2 = c2.add('1/(1-0.75)', 'multiplier')
    dy2 = c2.add('4*50', 'change in Y when I rises by 50')
    y2n = c2.add('(150+300)/(1-0.75)', 'new equilibrium Y')

    # ---------- Illustration 3: multiplier rounds ----------
    c3 = Checks()
    k3 = c3.add('1/(1-0.6)', 'multiplier with MPC 0.6')
    dy3 = c3.add('2.5*1000', 'total rise in income')
    dc3 = c3.add('2500*0.6', 'rise in consumption')
    ds3 = c3.add('2500*0.4', 'rise in saving')
    rounds, cum, inc = [], 0, 1000
    for r in range(1, 6):
        cum = c3.add(f'{cum}+{inc}', f'cumulative income after round {r}')
        rounds.append([str(r), str(inc), str(cum)])
        inc = c3.add(f'{inc}*0.6', f'income of round {r + 1}')
    t3 = table(['Round', 'Addition to income (₹ crore)', 'Cumulative rise in income'], rounds, num=[1, 2], title='First five rounds of the multiplier (MPC = 0.6)')

    # ---------- Illustration 4: three-sector ----------
    c4 = Checks()
    y4a = c4.add('(80-0.8*50+0.8*25+200+150)/(1-0.8)', 'Y with lump-sum tax and transfers')
    yd4a = c4.add('2050-50+25', 'disposable income')
    c4a = c4.add('80+0.8*2025', 'consumption')
    y4b = c4.add('(80-0.8*20+200+150)/(1-0.8*(1-0.25))', 'Y with proportional tax')
    k4b = c4.add('1/(1-0.8*(1-0.25))', 'multiplier with proportional tax')
    t4b = c4.add('20+0.25*1035', 'tax revenue at equilibrium')

    # ---------- Illustration 5: four-sector ----------
    c5 = Checks()
    y5 = c5.add('(50+120+100+80-20)/(1-0.75*(1-0.2)+0.1)', 'Y in four-sector model')
    m5 = c5.add('20+0.1*660', 'imports at equilibrium')
    nx5 = c5.add('80-86', 'net exports')
    k5 = c5.add('1/(1-0.75*(1-0.2)+0.1)', 'open-economy multiplier with tax')
    dy5 = c5.add('2*15', 'rise in Y when exports rise by 15')
    nx5b = c5.add('95-(20+0.1*690)', 'net exports after export rise')

    # ---------- Illustration 6: gaps ----------
    c6 = Checks()
    y6 = c6.add('(100+260)/(1-0.8)', 'equilibrium Y')
    ad6 = c6.add('100+0.8*2000+260', 'AD at full-employment income')
    dg6 = c6.add('2000-1960', 'deflationary gap')
    dI6 = c6.add('200/5', 'extra investment needed = shortfall / multiplier')
    ad6b = c6.add('100+0.8*2000+320', 'AD at Y* when I = 320')
    ig6 = c6.add('2020-2000', 'inflationary gap')

    # ---------- written questions ----------
    w1 = Checks()
    w1y = w1.add('(200+400)/(1-0.8)', 'equilibrium Y')
    w1c = w1.add('200+0.8*3000', 'C')
    w1s = w1.add('3000-2600', 'S')
    w1k = w1.add('1/(1-0.8)', 'k')
    w1y2 = w1.add('3000+5*60', 'new Y after I up 60')
    w2 = Checks()
    w2y = w2.add('(120-0.75*80+0.75*40+300+200)/(1-0.75)', 'Y three-sector lump-sum tax + TR')
    w2k = w2.add('1/(1-0.75)', 'multiplier')
    w2yd = w2.add('2360-80+40', 'Yd')
    w3 = Checks()
    w3y = w3.add('(40+60+50+70-10)/(1-0.8+0.05)', 'Y open economy')
    w3m = w3.add('10+0.05*840', 'imports')
    w3nx = w3.add('70-52', 'net exports')
    w3k = w3.add('1/(1-0.8+0.05)', 'foreign trade multiplier')

    # ---------- case ----------
    k = Checks()
    ky = k.add('(300+500+400+250-50)/(1-0.8*(1-0.25)+0.15)', 'case Y')
    kk = k.add('1/(1-0.8*(1-0.25)+0.15)', 'case multiplier')
    km = k.add('50+0.15*2545.45', 'case imports')
    kdy = k.add('(1/(1-0.8*(1-0.25)+0.15))*110', 'case: change in Y from G +110')

    concepts = [
        {'id': 'c1', 'title': 'Introduction — why Keynes', 'body': [
            'The Great Depression of the 1930s brought mass unemployment that classical economists could neither explain nor cure with a clear theory. In 1936 John Maynard Keynes published The General Theory of Employment, Interest and Money, which founded modern macroeconomics and gave a case for government spending.',
            'Keynes\'s building blocks: the link between consumption and income and the multiplier (how a shock to demand gets magnified into a bigger change in output); liquidity preference (the demand for money), through which monetary policy affects interest rates and demand; and the role of expectations in driving consumption and investment.',
            'The theory is presented in three models: the two-sector model (households and firms), the three-sector model (adding government) and the four-sector model (adding the foreign sector). The central idea: in the short run, the level of income and employment is decided by aggregate (effective) demand.'],
         'analogy': 'Classical economists trusted the car to steer itself back to full speed; Keynes argued it could stall on the roadside for years unless someone pressed the accelerator (demand).',
         'work': 'Every Union Budget speech on "capex push" or "demand support" rests on Keynesian reasoning — understanding it helps a CA read policy and its effect on clients\' sectors.'},
        {'id': 'c2', 'title': 'Circular flow in a simple two-sector model', 'body': [
            'Assumptions: only households and firms; households own all factors of production and spend all their income on goods and services produced by firms; firms hire factors from households, sell all output to households and do not save; no government, no foreign trade, no corporate saving. Total income produced (Y) accrues to households, so Y = disposable income (Yd).',
            'Real flows are the movement of factor services (households → firms) and goods and services (firms → households). Money flows are the payments that match them: factor payments (firms → households) and consumption spending (households → firms).',
            'With no leakages or injections, the amount firms pay out to factors equals what households earn, which equals what households spend, which equals what firms take in — and that equals the value of output.',
            'Equilibrium means a state of rest with no tendency to change: output is in equilibrium when what is produced equals what buyers plan to buy — i.e. the production plans of firms and the spending plans of households match. Keynesian analysis is in ex ante (planned) terms.'],
         'analogy': 'Water in a closed pipe loop with a pump: it keeps circulating at the same rate as long as nothing leaks out and nothing extra is poured in.',
         'work': 'The same loop thinking is used in group cash-flow and inter-company reconciliations — every payment out of one entity is a receipt somewhere else.'},
        {'id': 'c3', 'title': 'Consumption, saving and their propensities', 'body': [
            'Aggregate demand (AD) is total planned expenditure. In the two-sector model AD = C + I, where investment (I) is autonomous — determined outside the model and constant in the short run. Consumption is the largest component.',
            'Consumption function: C = a + bY. Here a (> 0) is autonomous consumption — consumption at zero income, financed by borrowing or past savings (dissaving); b = ΔC/ΔY is the marginal propensity to consume (MPC), with 0 < b < 1: consumption rises with income, but by less than the rise in income. Keynes\'s MPC is usually taken to be above 0.5.',
            'Average propensity to consume APC = C/Y. With a > 0, APC falls as income rises (it exceeds 1 at very low incomes, where people dissave).',
            'Income is either consumed or saved: Y = C + S, so S = Y − C = −a + (1 − b)Y. MPS = ΔS/ΔY = 1 − b; APS = S/Y. Therefore MPC + MPS = 1 and APC + APS = 1. Saving increases with income because MPS is positive.',
            'Aggregate supply (planned) is the total value of output firms plan to sell, which equals national income, all of which is either consumed or saved: AS = C + S.'],
         'analogy': 'Of every extra ₹100 earned, if you spend ₹75 and save ₹25, your MPC is 0.75 and MPS 0.25 — the two always add to the whole ₹100.',
         'work': 'Retail and FMCG forecasting models use income elasticity and propensity-to-consume ideas when projecting demand from changes in household income or tax cuts.'},
        {'id': 'c4', 'title': 'Two-sector equilibrium income', 'body': [
            'Equilibrium income is where planned aggregate demand equals aggregate supply: C + I = C + S, i.e. planned investment = planned saving (I = S).',
            'With C = a + bY and autonomous I: Y = a + bY + I, so Y = (a + I) ÷ (1 − b).',
            'On the 45° line diagram, every point on the 45° line has spending equal to output. The C + I line is flatter than the 45° line (b < 1) and cuts it at equilibrium. Below the equilibrium income, planned spending exceeds output — inventories run down unintentionally and firms raise output; above it, output exceeds spending — unsold stock piles up and firms cut output. In the Keynesian model it is these output changes, not price changes, that restore equilibrium.',
            'Keynes stressed that there is no automatic reason for households\' saving plans to match firms\' investment plans, or for consumption plans to match production plans. Leakages (saving) greater than injections (investment) make income fall; injections greater than leakages make it rise.'],
         'analogy': 'A shopkeeper who sees shelves emptying (spending > output) orders more; one whose godown overflows (output > spending) orders less — until the two match.',
         'work': 'Inventory build-up across many companies in quarterly results is a real-world signal that output has run ahead of demand — an early sign of a slowdown analysts watch for.'},
        {'id': 'c5', 'title': 'Equilibrium with unemployment or inflation — the two gaps', 'body': [
            'Keynesian equilibrium need not be at full employment (potential output). It can settle below or above it.',
            'Deflationary (recessionary, contractionary) gap: aggregate demand at the full-employment level of output falls short of that output — deficient demand. Firms find unsold stocks, cut output and jobs, and the economy settles at an under-employment equilibrium. The gap is measured vertically at full-employment income: full-employment output − AD at that output. Keynes argued this is what happened in the Great Depression, as wages and interest rates did not fall enough to restore full employment.',
            'Inflationary gap: AD at the full-employment output exceeds that output — excess demand. Real output cannot rise further, so prices rise (demand-pull inflation); nominal income increases but real output, real income and employment stay the same. Gap = AD at full-employment output − full-employment output.'],
         'analogy': 'A theatre with 500 seats: if only 450 want tickets, seats go empty (deflationary gap); if 550 want tickets, the black-market price rises but no new seats appear (inflationary gap).',
         'work': 'RBI and government statements about the "output gap" are this idea; businesses in a deflationary-gap phase face weak volumes, while an inflationary gap brings cost pressures.'},
        {'id': 'c6', 'title': 'The investment multiplier', 'body': [
            'An increase in autonomous investment raises equilibrium income by a multiple of itself. Investment multiplier k = ΔY ÷ ΔI = 1 ÷ (1 − MPC) = 1 ÷ MPS. So ΔY = k × ΔI.',
            'Process (the ripple effect): the new investment spending becomes income for factor owners; they spend the MPC share of it, which becomes someone else\'s income, who again spends the MPC share, and so on. The rounds become smaller each time; the sum of the series is ΔI × 1/(1 − MPC).',
            'The higher the MPC, the larger the multiplier; the higher the MPS, the smaller. If MPC = 1, k would be infinite; if MPC = 0, k = 1.',
            'Leakages that reduce the multiplier: progressive taxes; high liquidity preference and idle cash; demand met from existing stocks or imports; extra income used to buy existing assets, shares or securities; undistributed corporate profits; repayment of debts; full employment (extra spending only raises prices); and shortages of goods despite a high MPC.',
            'In under-developed economies the MPC is high but the multiplier is low in practice, because structural bottlenecks prevent output from rising — prices rise instead.',
            'Keynesian models are short-period and static: they compare one equilibrium with another (comparative statics) without tracing the path over time.'],
         'analogy': 'A stone dropped in a pond: the first ripple is the investment; each later ripple is smaller (because part leaks out as saving), but together they cover far more of the pond.',
         'work': 'Infrastructure project appraisals and government capex announcements cite "multiplier effects" on GDP and employment — a CA should know what limits them (imports, saving, capacity).'},
        {'id': 'c7', 'title': 'Three-sector model (adding government)', 'body': [
            'Government adds four flows: taxes from households and firms; transfer payments to households and subsidies to firms; purchases of goods and services and of factor services; and borrowing in financial markets when taxes fall short of spending.',
            'Leakages: saving and taxes. Injections: investment and government purchases. AD = C + I + G; AS = C + S + T. Equilibrium: C + I + G = Y = C + S + T, i.e. I + G = S + T. G and I are taken as autonomous (horizontal lines in the diagram).',
            'Lump-sum tax (T not dependent on income), with C = a + bYd and Yd = Y − T: Y = (a − bT + I + G) ÷ (1 − b). The expenditure multiplier is still 1/(1 − b).',
            'With transfer payments TR: Yd = Y − T + TR, so Y = (a + I + G − bT + bTR) ÷ (1 − b).',
            'With a proportional income tax T = T̄ + tY: Yd = Y − T̄ − tY, so Y = (a + I + G − bT̄ + bTR) ÷ [1 − b(1 − t)]. The multiplier becomes 1 ÷ [1 − b(1 − t)], smaller than 1/(1 − b), because part of every round of extra income leaks out as tax.'],
         'analogy': 'Government is a second pump on the pipe loop: it draws water out through taxes and pumps it back in through purchases and transfers.',
         'work': 'Fiscal-impact notes on a tax cut or a stimulus use exactly these formulas; CAs advising industry bodies on budget proposals often present such multiplier estimates.'},
        {'id': 'c8', 'title': 'Four-sector model (adding the foreign sector)', 'body': [
            'Exports (X) are an injection — foreign demand for domestic output — and depend on foreign income, so they are autonomous. Imports (M) are a leakage; M = M̄ + mY, where m = ΔM/ΔY is the marginal propensity to import.',
            'Equilibrium: Y = C + I + G + (X − M). With C = a + b(Y − T): Y = (a − bT + I + G + X − M̄) ÷ (1 − b + m). Leakages S + T + M equal injections I + G + X at equilibrium.',
            'Foreign trade multiplier: ΔY/ΔX = 1 ÷ (1 − b + m), which can be written 1 ÷ (1 − (b − m)). With a proportional tax: 1 ÷ [1 − b(1 − t) + m]. The higher m (the more open the economy), the smaller the multiplier, because each round of extra income leaks partly into foreign goods.',
            'Positive net exports (X > M) are a net injection that raises income; X < M is a net withdrawal. An autonomous rise in exports is expansionary; an autonomous rise in imports is contractionary. This does not mean imports are harmful: trade lets a country import what others produce more efficiently.'],
         'analogy': 'Imports are a side tap on the pipe loop: the more it is opened, the less of each round of spending stays inside the country.',
         'work': 'Export-promotion schemes and "Make in India" debates are partly about the foreign trade multiplier; CAs evaluating export incentives should note that the impact on GDP depends on import content.'},
        {'id': 'c9', 'title': 'Conclusion — effective demand and policy', 'body': [
            'In the Keynesian view national income depends on aggregate effective demand. If demand falls short of the full-employment output, unemployment results and actual output stays below potential; if demand exceeds it, the result is inflation — nominal output rises without more real output.',
            'Equilibrium output need not be full-employment output. Because private investment is unstable, income would be unstable too; by changing government spending (G) and taxes, the government can offset swings in investment and keep total autonomous expenditure — and hence income — steadier. This is the case for active fiscal policy.'],
         'analogy': 'Government acts like a shock absorber: when private investment hits a pothole, public spending takes up the jolt.',
         'work': 'Counter-cyclical government spending explains why public-sector orders often rise when private capex falls — useful context when CAs review order books of contractors.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Consumption and saving schedule', 'difficulty': 'core', 'minutes': 8,
         'q': 'The consumption function is C = 60 + 0.8Y (₹ crore). Prepare a schedule of C, S, APC, APS, MPC and MPS for income levels 0 to 500. At what income is saving zero?',
         'solution': [t1, p(f'Saving is zero where C = Y: Y = 60 ÷ (1 − 0.8) = ₹{be} crore. Below that income households dissave. APC falls as income rises while MPC stays constant at 0.8; APC + APS = 1 and MPC + MPS = 1 at every level.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Two-sector equilibrium', 'difficulty': 'core', 'minutes': 7,
         'q': 'C = 150 + 0.75Y and I = 250 (₹ crore). Find equilibrium income, consumption and saving. If investment rises to 300, find the new equilibrium income.',
         'solution': [wn('Equilibrium', f'Y = (a + I)/(1 − b) = (150 + 250)/0.25 = ₹{inr(y2)} crore; C = 150 + 0.75 × 1,600 = {inr(cc2)}; S = 1,600 − 1,350 = {s2} = I ✓.'),
                      wn('After the rise in investment', f'k = 1/(1 − 0.75) = {k2}; ΔY = 4 × 50 = {dy2}; new Y = (150 + 300)/0.25 = ₹{inr(y2n)} crore.')],
         'checks': c2},
        {'id': 'i3', 'title': 'The multiplier round by round', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'Investment rises by ₹1,000 crore and the MPC is 0.6. Find the multiplier, the total rise in income, consumption and saving, and show the first five rounds.',
         'solution': [wn('Totals', f'k = 1/(1 − 0.6) = {k3}; ΔY = 2.5 × 1,000 = ₹{inr(dy3)} crore; ΔC = 0.6 × 2,500 = ₹{inr(dc3)} crore; ΔS = 0.4 × 2,500 = ₹{inr(ds3)} crore (= ΔI, so saving again equals investment).'),
                      t3, note('After five rounds income has risen by about 92% of the final ₹2,500 crore; the rest comes from the ever-smaller later rounds.')],
         'checks': c3},
        {'id': 'i4', 'title': 'Three-sector model: lump-sum and proportional taxes', 'difficulty': 'hard', 'minutes': 10,
         'q': '(a) C = 80 + 0.8Yd, I = 200, G = 150, lump-sum tax T = 50 and transfers TR = 25. Find equilibrium Y, Yd and C. (b) Now let T = 20 + 0.25Y with no transfers (I and G unchanged). Find Y, the multiplier and tax revenue.',
         'solution': [wn('(a)', f'Y = (a + I + G − bT + bTR)/(1 − b) = (80 − 40 + 20 + 200 + 150)/0.2 = ₹{inr(y4a)} crore; Yd = 2,050 − 50 + 25 = {inr(yd4a)}; C = 80 + 0.8 × 2,025 = {inr(c4a)}.'),
                      wn('(b)', f'Y = (80 − 0.8 × 20 + 200 + 150)/[1 − 0.8(1 − 0.25)] = 414/0.4 = ₹{inr(y4b)} crore; multiplier = 1/0.4 = {k4b}; tax revenue = 20 + 0.25 × 1,035 = {t4b}.'),
                      note('The proportional tax cuts the multiplier from 5 to 2.5 because every round of extra income partly leaks into taxes.')],
         'checks': c4},
        {'id': 'i5', 'title': 'Four-sector model and the foreign trade multiplier', 'difficulty': 'hard', 'minutes': 10,
         'q': 'C = 50 + 0.75Yd, T = 0.2Y, I = 120, G = 100, X = 80, M = 20 + 0.1Y. Find equilibrium income, imports and net exports. If exports rise by 15, find the change in income and the new net exports.',
         'solution': [wn('Equilibrium', f'Y = (50 + 120 + 100 + 80 − 20)/[1 − 0.75(1 − 0.2) + 0.1] = 330/0.5 = ₹{y5} crore; M = 20 + 66 = {m5}; X − M = 80 − 86 = {nx5} (trade deficit).'),
                      wn('Exports +15', f'Multiplier = 1/0.5 = {k5}; ΔY = 2 × 15 = {dy5}; new Y = 690; new M = 20 + 69 = 89; new X − M = 95 − 89 = {nx5b}.'),
                      note('Net exports improve by less than the rise in exports, because higher income pulls in more imports.')],
         'checks': c5},
        {'id': 'i6', 'title': 'Measuring the deflationary and inflationary gaps', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'Full-employment income is ₹2,000 crore. C = 100 + 0.8Y. (a) If I = 260, find equilibrium income and the deflationary gap. How much extra investment would remove the gap? (b) If I = 320, find the inflationary gap.',
         'solution': [wn('(a)', f'Y = (100 + 260)/0.2 = ₹{inr(y6)} crore < 2,000. AD at Y* = 100 + 1,600 + 260 = {inr(ad6)} → deflationary gap = 2,000 − 1,960 = {dg6}. Income is short by 200; with k = 5, extra investment of 200 ÷ 5 = {dI6} closes the gap.'),
                      wn('(b)', f'AD at Y* = 100 + 1,600 + 320 = {inr(ad6b)} → inflationary gap = {ig6}. Real output cannot exceed 2,000, so prices rise.')],
         'checks': c6},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Reading a stimulus announcement', 'role': 'CA in industry — strategy team of a cement company',
         'situation': 'The government announces an extra ₹50,000 crore of capital spending on roads. The board wants to know the likely effect on demand.',
         'steps': ['Note the direct effect: cement and steel orders from the road projects.', 'Explain the multiplier: contractors\' and workers\' incomes are re-spent, raising demand across the economy.', 'Temper the estimate for leakages — taxes, saving, imports of machinery and fuel, and capacity limits — so the realistic multiplier is well below 1/(1 − MPC) computed on consumption alone.', 'Translate into a range of regional demand growth for the company\'s plants.'],
         'takeaway': 'The multiplier explains the indirect boost, but leakages decide its size.', 'think': 'Why would the multiplier be smaller if the economy were already near full capacity?', 'answer': 'Extra spending would mostly raise prices rather than real output — full employment is one of the leakages that weaken the multiplier.'},
        {'id': 'j2', 'title': 'Inventory pile-up across clients', 'role': 'Audit manager reviewing several manufacturing clients',
         'situation': 'In the year-end audits, three unrelated clients show unusually high finished-goods inventory and are cutting second shifts.',
         'steps': ['Recognise the Keynesian signal: unplanned inventory accumulation means planned spending is below output.', 'Expect firms to reduce output and employment until output matches demand.', 'Heighten audit focus on inventory valuation (NRV), going-concern indicators and covenant compliance.'],
         'takeaway': 'Unplanned stock build-up is how a fall in aggregate demand first shows up in company accounts.'},
    ]

    mcqs = [
        Q('m1', 'Keynes\'s General Theory of Employment, Interest and Money was published in:', ['1936', '1929', '1944', '1919'], 0, 'It followed the Great Depression of the early 1930s.', 'c1', 'core', '1936'),
        Q('m2', 'In the simple two-sector circular flow model:', ['Households spend all their income on goods produced by firms and firms do not save', 'Government collects taxes', 'There are exports and imports', 'Firms retain profits'], 0, 'No leakages or injections exist in the simple model.', 'c2'),
        Q('m3', 'In the circular flow, payment of wages by firms to households is a:', ['Money flow', 'Real flow', 'Leakage', 'Injection'], 0, 'Real flows are factor services and goods; money flows are the payments for them.', 'c2'),
        Q('m4', 'If C = 40 + 0.85Y, the marginal propensity to save is:', ['0.15', '0.85', '40', '1.15'], 0, 'MPS = 1 − MPC = 1 − 0.85.', 'c3', 'core', '1-0.85'),
        Q('m5', 'Consumption is ₹180 crore at an income of ₹200 crore. APS is:', ['0.1', '0.9', '1.11', '0.2'], 0, 'S = 200 − 180 = 20; APS = 20/200 = 0.1.', 'c3', 'core', '(200-180)/200'),
        Q('m6', 'Saving is ₹450 crore at an income of ₹1,500 crore. APC is:', ['0.7', '0.3', '1.43', '0.45'], 0, 'C = 1,050; APC = 1,050/1,500 = 0.7 (APC = 1 − APS).', 'c3', 'core', '(1500-450)/1500'),
        Q('m7', 'According to Keynes, the MPC is:', ['Greater than zero but less than one', 'Equal to one', 'Greater than one', 'Negative'], 0, 'Consumption rises with income, but by less than the rise in income.', 'c3'),
        Q('m8', 'In C = a + bY, the term "a" represents:', ['Autonomous consumption — consumption at zero income', 'MPC', 'Induced consumption', 'Saving at zero income'], 0, 'At zero income households dissave to consume "a".', 'c3'),
        Q('m9', 'As income rises with C = a + bY (a > 0), the APC:', ['Falls', 'Rises', 'Remains constant', 'Becomes equal to MPC immediately'], 0, 'APC = a/Y + b, which falls as Y rises.', 'c3', 'moderate'),
        Q('m10', 'Which is always true?', ['MPC + MPS = 1', 'APC + MPC = 1', 'APS + MPC = 1', 'APC = MPC'], 0, 'Each extra rupee is either consumed or saved (also APC + APS = 1).', 'c3'),
        Q('m11', 'In a two-sector economy, equilibrium income is where:', ['Planned saving equals planned investment', 'Consumption equals income', 'Saving is zero', 'Investment is maximum'], 0, 'C + I = C + S ⇒ I = S.', 'c4'),
        Q('m12', 'C = 100 + 0.8Y and I = 200. Equilibrium income is:', ['1,500', '1,000', '375', '2,500'], 0, 'Y = (100 + 200)/(1 − 0.8) = 1,500. 375 divides by 0.8 instead of 0.2.', 'c4', 'core', '(100+200)/(1-0.8)'),
        Q('m13', 'C = 250 + 0.8Y and I = 300. Saving at equilibrium is:', ['300', '2,750', '2,450', '250'], 0, 'At equilibrium S = I = 300 (Y = 2,750, C = 2,450).', 'c4', 'moderate', '2750-(250+0.8*2750)'),
        Q('m14', 'An economy in equilibrium has Y = 2,000, autonomous consumption 200 and investment 300. The MPC is:', ['0.75', '0.25', '0.85', '0.9'], 0, 'C = Y − I = 1,700 = 200 + b × 2,000 ⇒ b = 1,500/2,000 = 0.75.', 'c4', 'hard', '(2000-300-200)/2000'),
        Q('m15', 'When planned aggregate expenditure exceeds output, there will be:', ['An unplanned fall in inventories and a rise in output', 'An unplanned rise in inventories', 'A fall in output', 'No change'], 0, 'Firms sell more than they produce, stocks run down and they expand output.', 'c4', 'moderate'),
        Q('m16', 'A deflationary gap exists when aggregate demand at full-employment output is:', ['Less than full-employment output', 'More than full-employment output', 'Equal to full-employment output', 'Zero'], 0, 'Deficient demand leads to under-employment equilibrium.', 'c5'),
        Q('m17', 'An inflationary gap leads to:', ['A rise in prices with no rise in real output', 'A rise in real output and employment', 'A fall in prices', 'Unemployment'], 0, 'At full employment, excess demand only pushes up prices.', 'c5'),
        Q('m18', 'If MPC = 0.8, the investment multiplier is:', ['5', '1.25', '0.2', '8'], 0, 'k = 1/(1 − 0.8) = 5. 1.25 is 1/MPC.', 'c6', 'core', '1/(1-0.8)'),
        Q('m19', 'Investment rises by ₹500 crore and income rises by ₹2,000 crore. The MPC is:', ['0.75', '0.25', '4', '0.8'], 0, 'k = 2,000/500 = 4 = 1/(1 − MPC) ⇒ MPC = 0.75.', 'c6', 'moderate', '1-500/2000'),
        Q('m20', 'MPS is 0.25 and investment rises by ₹120 crore. Income rises by:', ['₹480 crore', '₹160 crore', '₹30 crore', '₹90 crore'], 0, 'k = 1/MPS = 4; ΔY = 4 × 120 = ₹480 crore.', 'c6', 'core', '120/0.25'),
        Q('m21', 'MPC is 0.6 and investment rises by ₹400 crore. The increase in consumption is:', ['₹600 crore', '₹1,000 crore', '₹400 crore', '₹240 crore'], 0, 'ΔY = 2.5 × 400 = 1,000; ΔC = 0.6 × 1,000 = ₹600 crore.', 'c6', 'moderate', '0.6*400/(1-0.6)'),
        Q('m22', 'Which of the following will REDUCE the value of the multiplier?', ['A higher marginal propensity to import', 'A higher MPC', 'A lower MPS', 'Lower taxes'], 0, 'Imports are a leakage from each round of spending.', 'c6'),
        Q('m23', 'The maximum value of the multiplier is reached when:', ['MPC = 1', 'MPC = 0', 'MPS = 1', 'MPC = 0.5'], 0, 'k = 1/(1 − 1) → infinity.', 'c6'),
        Q('m24', 'In the three-sector model, equilibrium requires:', ['I + G = S + T', 'I = S only', 'G = T always', 'C + S = T'], 0, 'Injections (I + G) equal leakages (S + T).', 'c7'),
        Q('m25', 'C = 10 + 0.75Yd, I = 50, G = T = 20 (lump-sum). Equilibrium income is:', ['260', '320', '200', '280'], 0, 'Y = (10 − 0.75×20 + 50 + 20)/0.25 = 65/0.25 = 260. 320 ignores the tax.', 'c7', 'moderate', '(10-0.75*20+50+20)/(1-0.75)'),
        Q('m26', 'With MPC = 0.8 and a proportional income tax rate of 25%, the expenditure multiplier is:', ['2.5', '5', '4', '1.25'], 0, 'k = 1/[1 − 0.8(1 − 0.25)] = 1/0.4 = 2.5.', 'c7', 'hard', '1/(1-0.8*(1-0.25))'),
        Q('m27', 'C = 100 + 0.8(Y − T + TR), I = 200, G = 100, T = 25 + 0.1Y, TR = 50. Equilibrium income is:', ['1,500', '2,100', '1,312.5', '1,750'], 0, 'Y(1 − 0.8 + 0.08) = 100 − 20 + 40 + 300 = 420 ⇒ Y = 420/0.28 = 1,500.', 'c7', 'hard', '(100-0.8*25+0.8*50+200+100)/(1-0.8*(1-0.1))'),
        Q('m28', 'In the four-sector model, the foreign trade multiplier (no income tax) is:', ['1/(1 − b + m)', '1/(1 − b)', '1/(1 + b − m)', '1/m'], 0, 'Imports add a leakage m to each round.', 'c8'),
        Q('m29', 'MPC = 0.9 and marginal propensity to import = 0.15. The foreign trade multiplier is:', ['4', '10', '6.67', '0.25'], 0, '1/(1 − 0.9 + 0.15) = 1/0.25 = 4. 10 ignores imports.', 'c8', 'moderate', '1/(1-0.9+0.15)'),
        Q('m30', 'An autonomous increase in imports, other things equal:', ['Reduces equilibrium income', 'Raises equilibrium income', 'Has no effect on income', 'Raises exports automatically'], 0, 'Imports are a leakage from domestic spending.', 'c8'),
        Q('m31', 'C = 60 + 0.9Y, I = 10, G = 10, T = 0, X = 20, M = 10 + 0.05Y. Equilibrium income is:', ['600', '900', '800', '533.3'], 0, 'Y = (60 + 10 + 10 + 20 − 10)/(1 − 0.9 + 0.05) = 90/0.15 = 600.', 'c8', 'hard', '(60+10+10+20-10)/(1-0.9+0.05)'),
        Q('m32', 'According to Keynes, equilibrium income:', ['Need not be at full employment', 'Is always at full employment', 'Is always below full employment', 'Is decided by supply alone'], 0, 'It depends on effective demand and may be above or below potential output.', 'c9'),
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'C = 200 + 0.8Y and I = 400 (₹ crore). (a) Find equilibrium income, consumption and saving. (b) Find the multiplier. (c) If investment rises by 60, find the new equilibrium income.',
         'model': [wn('(a)', f'Y = (200 + 400)/(1 − 0.8) = ₹{inr(w1y)} crore; C = 200 + 2,400 = {inr(w1c)}; S = 3,000 − 2,600 = {w1s} = I.'), wn('(b)', f'k = 1/(1 − 0.8) = {w1k}.'), wn('(c)', f'ΔY = 5 × 60 = 300; new Y = ₹{inr(w1y2)} crore.')],
         'scheme': [{'id': 's1', 'pt': 'Equilibrium condition Y = C + I', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Y, C and S correct', 'm': 2, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Multiplier', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'New Y', 'm': 1, 'skill': 'computation'}],
         'remarks': ['Most candidates get Y; marks are lost by not verifying S = I.'], 'mistakes': ['Dividing by MPC instead of (1 − MPC).'], 'tips': ['Always verify: saving at equilibrium equals investment in a two-sector model.'], 'checks': w1},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'hard', 'pad': 'text',
         'q': 'C = 120 + 0.75Yd; I = 300; G = 200; lump-sum T = 80; transfers TR = 40. Find equilibrium income, disposable income and the multiplier.',
         'model': [wn('Income', f'Y = (a + I + G − bT + bTR)/(1 − b) = (120 − 60 + 30 + 300 + 200)/0.25 = ₹{inr(w2y)} crore.'), wn('Disposable income', f'Yd = 2,360 − 80 + 40 = ₹{inr(w2yd)} crore.'), wn('Multiplier', f'1/(1 − 0.75) = {w2k}.')],
         'scheme': [{'id': 's1', 'pt': 'Correct equation with −bT and +bTR', 'm': 1.5, 'skill': 'concept'}, {'id': 's2', 'pt': 'Equilibrium Y', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Yd', 'm': 0.5, 'skill': 'computation'}, {'id': 's4', 'pt': 'Multiplier', 'm': 1, 'skill': 'computation'}],
         'remarks': ['Transfers enter multiplied by b, just like taxes but with a plus sign.'], 'mistakes': ['Adding TR in full instead of b × TR.', 'Subtracting T in full instead of b × T.'], 'tips': ['Write Yd = Y − T + TR first, then substitute.'], 'checks': w2},
        {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'hard', 'pad': 'text',
         'q': 'An open economy has C = 40 + 0.8Y, I = 60, G = 50, X = 70 and M = 10 + 0.05Y (no taxes). Find equilibrium income, net exports and the foreign trade multiplier. Comment on the trade balance.',
         'model': [wn('Income', f'Y = (40 + 60 + 50 + 70 − 10)/(1 − 0.8 + 0.05) = 210/0.25 = ₹{inr(w3y)} crore.'), wn('Net exports', f'M = 10 + 42 = {w3m}; X − M = 70 − 52 = {w3nx} → trade surplus.'),
                   wn('Multiplier', f'1/(1 − 0.8 + 0.05) = {w3k} (compared with 5 in a closed economy — imports are an extra leakage).')],
         'scheme': [{'id': 's1', 'pt': 'Equilibrium condition with X − M', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Equilibrium Y', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Net exports and comment', 'm': 1.5, 'skill': 'analysis'}, {'id': 's4', 'pt': 'Foreign trade multiplier', 'm': 1, 'skill': 'computation'}],
         'remarks': ['Write the autonomous terms separately from the induced terms to avoid sign errors.'], 'mistakes': ['Adding M̄ instead of subtracting.', 'Using 1/(1 − b) as the multiplier.'], 'tips': ['Denominator in an open economy: 1 − b + m (or 1 − b(1 − t) + m with tax).'], 'checks': w3},
    ]

    viva = [
        V('v1', 'What is the consumption function and what are MPC and APC?',
          'The consumption function shows the relationship between consumption and disposable income, written as C equals a plus bY. Here a is autonomous consumption at zero income. The marginal propensity to consume, b, is the change in consumption divided by the change in income, and it lies between zero and one. The average propensity to consume is total consumption divided by total income.',
          [P('p1', 'Relation between consumption and (disposable) income: C = a + bY', 3, 'relationship|relation|function|depends', 'income', min=2),
           P('p2', 'MPC = ΔC/ΔY, between 0 and 1', 4, 'change in consumption|increase in consumption|extra consumption|additional consumption|delta c', 'between zero and one|less than one|between 0 and 1|less than 1|less than unity|lies between', min=1),
           P('p3', 'APC = C/Y', 3, ALT('total consumption {d} total income', 'consumption {d} income', 'c {d} y', d=['divided by', 'by', 'over', 'to'])), ], 'c3'),
        V('v2', 'What is the condition for equilibrium income in the two-sector Keynesian model?',
          'Equilibrium income is reached where aggregate demand equals aggregate supply, that is C plus I equals C plus S. This means planned investment equals planned saving. On the diagram it is where the C plus I line cuts the 45 degree line. If spending exceeds output, stocks fall and output rises; if output exceeds spending, stocks pile up and output falls.',
          [P('p1', 'AD = AS (C + I = C + S)', 3, 'aggregate demand equal|aggregate demand equals|ad equal|ad equals|demand equals supply|aggregate demand is equal|c plus i equal|c + i'),
           P('p2', 'Planned saving = planned investment', 4, ALT('{s} equal {i}', '{s} equals {i}', '{i} equal {s}', '{i} equals {s}', '{s} is equal to {i}', '{i} is equal to {s}', s=['saving', 'savings', 'planned saving', 's'], i=['investment', 'planned investment', 'i'])),
           P('p3', '45° line / adjustment through inventories and output', 3, '45 degree|45°|forty five|45|inventor|stock|output rise|output fall|output adjust')], 'c4'),
        V('v3', 'What is the investment multiplier and on what does its size depend?',
          'The investment multiplier is the ratio of the change in income to the change in investment, k equals delta Y by delta I. It equals one divided by one minus MPC, which is the same as one divided by MPS. So a higher marginal propensity to consume gives a larger multiplier, and a higher marginal propensity to save gives a smaller one.',
          [P('p1', 'k = ΔY/ΔI', 3, 'change in income|increase in income|delta y|rise in income', 'change in investment|increase in investment|delta i|rise in investment', min=2),
           P('p2', 'k = 1/(1 − MPC) = 1/MPS', 4, '1 minus mpc|1 minus marginal propensity to consume|1 by mps|reciprocal of mps|1 divided by mps|1 over mps|1 by marginal propensity to save|1 divided by marginal propensity to save|reciprocal of marginal propensity to save|1 minus b|1 1 mpc|1 by 1 minus'),
           P('p3', 'Higher MPC → bigger multiplier (higher MPS → smaller)', 3, ALT('{h} mpc {l} multiplier', '{h} marginal propensity to consume {l} multiplier', '{h} the mpc {l} the multiplier', '{h} the mpc the {l} the multiplier', '{h} the marginal propensity to consume the {l}', 'directly related|direct relationship|positively related', h=['higher', 'greater', 'larger', 'more', 'bigger'], l=['larger', 'higher', 'greater', 'bigger', 'more']))], 'c6'),
        V('v4', 'What are leakages in the multiplier process? Give examples.',
          'Leakages are the parts of extra income that are not spent on domestically produced consumption goods, so they weaken the multiplier. Examples are saving and idle cash holding, taxes, imports, repayment of old debts, buying existing assets or shares, undistributed company profits, and full employment, where extra spending only raises prices.',
          [P('p1', 'Income not re-spent on domestic consumption — reduces multiplier', 4, 'not spent|not re-spent|withdrawn|leaks out|does not return|goes out|out of the income stream|reduce the multiplier|reduces the multiplier|weaken|smaller multiplier|lower multiplier'),
           P('p2', 'Examples (any three): saving, taxes, imports, debt repayment, existing assets, undistributed profits', 6, 'saving|savings|idle cash|hoard|liquidity preference', 'tax', 'import', 'debt|repay|loan', 'existing asset|shares|securities|second hand', 'undistributed|retained', 'full employment|inflation|price', min=3)], 'c6'),
        V('v5', 'Distinguish between a deflationary gap and an inflationary gap.',
          'A deflationary gap arises when aggregate demand at the full employment level of output is less than that output, so demand is deficient and the economy settles at an under-employment equilibrium with unemployment. An inflationary gap arises when aggregate demand at full employment output is more than that output, so there is excess demand; real output cannot rise, so prices rise.',
          [P('p1', 'Deflationary gap: AD < full-employment output (deficient demand)', 3, 'deflationary|recessionary|contractionary', 'less than|short of|falls short|deficient|below|lower than', min=2),
           P('p2', 'Leads to unemployment / under-employment equilibrium', 3, 'unemployment|under employment|underemployment|jobless|idle'),
           P('p3', 'Inflationary gap: AD > full-employment output (excess demand)', 2, 'inflationary', 'more than|exceeds|excess demand|greater than|above|higher than'),
           P('p4', 'Inflationary gap leads to rising prices, not more real output', 2, 'price rise|prices rise|price level rise|rise in price|demand pull|prices go up|price increase|prices increase|prices to rise|price to rise|causing inflation|cause inflation|leads to inflation|results in inflation')], 'c5'),
        V('v6', 'Why is the multiplier smaller in an open economy than in a closed economy?',
          'In an open economy part of every increase in income is spent on imports, which is a leakage from the domestic income stream. So the foreign trade multiplier is one divided by one minus b plus m, where m is the marginal propensity to import. A higher marginal propensity to import gives a smaller multiplier than one divided by one minus b in a closed economy.',
          [P('p1', 'Part of extra income spent on imports — a leakage', 4, 'import', 'leakage|leak|withdraw|spent abroad|foreign goods|outflow', min=2),
           P('p2', 'Multiplier = 1/(1 − b + m)', 3, '1 minus b plus m|1 b m|1 minus mpc plus mpm|1 minus b + m|1 b plus m|minus b plus m|1 minus mpc plus marginal propensity to import'),
           P('p3', 'Higher MPM → smaller multiplier', 3, ALT('{h} {m} {s}', '{h} the {m} the {s}', h=['higher', 'greater', 'larger', 'more', 'bigger'], m=['marginal propensity to import', 'm', 'mpm', 'propensity to import'], s=['smaller', 'lower', 'less']), 'more open|openness', min=1)], 'c8'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Economy of Suvarnadesh', 'difficulty': 'hard',
        'case': ('Suvarnadesh has the following behaviour (₹ crore): C = 300 + 0.8Yd; taxes T = 0.25Y; investment I = 500; government purchases G = 400; exports X = 250; imports M = 50 + 0.15Y. '
                 'The finance ministry is considering an extra ₹110 crore of road spending.'),
        'mcqs': [
            M('k1a', 'The expenditure multiplier for Suvarnadesh is approximately:', ['1.82', '5', '2.5', '4'], 0, f'k = 1/[1 − 0.8(1 − 0.25) + 0.15] = 1/0.55 = {kk}. 5 is the closed-economy multiplier without tax.', 'hard', 'round(1/(1-0.8*(1-0.25)+0.15),2)'),
            M('k1b', 'Equilibrium income (₹ crore, to two decimals) is:', ['2,545.45', '3,500', '2,800', '1,400'], 0, f'Y = (300 + 500 + 400 + 250 − 50)/0.55 = 1,400/0.55 = {inr(ky)}.', 'hard', '(300+500+400+250-50)/(1-0.8*(1-0.25)+0.15)'),
            M('k1c', 'If road spending rises by ₹110 crore, equilibrium income rises by about:', ['₹200 crore', '₹550 crore', '₹110 crore', '₹275 crore'], 0, f'ΔY = 1.818 × 110 = {kdy}. ₹550 crore would use the multiplier of 5.', 'hard', '(1/(1-0.8*(1-0.25)+0.15))*110'),
            M('k1d', 'Which change would make Suvarnadesh\'s multiplier larger?', ['A fall in the marginal propensity to import', 'A rise in the tax rate', 'A fall in the MPC', 'A rise in the marginal propensity to import'], 0, 'Smaller leakages (imports, taxes, saving) mean a bigger multiplier.', 'moderate'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch05', 'n': 2, 'title': 'The Keynesian Theory of Determination of National Income',
        'outcomes': ['Explain the circular flow in a two-sector economy and the Keynesian idea of equilibrium income.', 'Use the consumption and saving functions (MPC, APC, MPS, APS) and solve for equilibrium income in two-, three- and four-sector models.',
                     'Compute and explain the investment multiplier, its leakages, the tax multiplier and the foreign trade multiplier.', 'Explain deflationary and inflationary gaps and the role of fiscal policy.'],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 55, 'practice': 70}, 'prereq': ['fnd-p4-ch05-u01'],
                 'exam_tip': 'Equilibrium-income and multiplier MCQs are near-certain. Memorise: two-sector Y = (a + I)/(1 − b); with lump-sum tax subtract bT; with transfers add bTR; proportional tax → 1 − b(1 − t); imports → + m in the denominator.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Keynes (1936): output and employment set by aggregate effective demand.', 'C = a + bY; MPC = ΔC/ΔY (0 < b < 1); APC = C/Y falls as Y rises; MPC + MPS = 1; APC + APS = 1.',
                        'Two-sector equilibrium: C + I = C + S ⇒ I = S; Y = (a + I)/(1 − b).', 'Multiplier k = ΔY/ΔI = 1/(1 − MPC) = 1/MPS; leakages reduce it.',
                        'Three-sector: I + G = S + T; lump-sum tax Y = (a + I + G − bT + bTR)/(1 − b); proportional tax denominator 1 − b(1 − t).',
                        'Four-sector: Y = C + I + G + (X − M), M = M̄ + mY; foreign trade multiplier 1/(1 − b + m).', 'Deflationary gap = deficient demand at full employment; inflationary gap = excess demand → prices rise.'],
            'remember': ['Below equilibrium: unplanned inventory fall → output rises. Above: unplanned inventory rise → output falls.', 'At equilibrium in the two-sector model S = I always.', 'High MPC in LDCs but low effective multiplier due to supply bottlenecks.'],
            'traps': ['k = 1/(1 − MPC), not 1/MPC.', 'Taxes and transfers enter multiplied by b.', 'Imports are subtracted (M̄) and m is added in the denominator.', 'Inflationary gap raises nominal, not real, income.']},
        'quickref': [{'k': 'Consumption function', 'v': 'C = a + bY; MPC = b'}, {'k': 'Saving function', 'v': 'S = −a + (1 − b)Y; MPS = 1 − b'},
                     {'k': 'Two-sector equilibrium', 'v': 'Y = (a + I)/(1 − b); S = I'}, {'k': 'Investment multiplier', 'v': 'k = 1/(1 − MPC) = 1/MPS'},
                     {'k': 'Three-sector (lump-sum T, TR)', 'v': 'Y = (a + I + G − bT + bTR)/(1 − b)'}, {'k': 'Proportional tax', 'v': 'Y = (a + I + G − bT̄ + bTR)/[1 − b(1 − t)]'},
                     {'k': 'Four-sector', 'v': 'Y = (a − bT + I + G + X − M̄)/(1 − b + m)'}, {'k': 'Foreign trade multiplier', 'v': '1/(1 − b + m); with tax 1/[1 − b(1 − t) + m]'}],
        'viva': viva, 'cases': cases,
    }
