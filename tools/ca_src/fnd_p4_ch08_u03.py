"""CA Foundation · Paper 4 Business Economics · Chapter 8 Money Market · Unit 3 Monetary Policy.
Original explanations, numbers and questions. Policy rates are those quoted in the study material (as on 5 August 2026)."""
from lib import *
from ca_viva import P, ALT, V

UID = 'fnd-p4-ch08-u03'


def M(i, q, o, a, e, c=None, d='core', check=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if c: m['concept'] = c
    if check: m['check'] = check
    return m


def build():
    c1 = Checks()
    ndtl = 1000000
    crr = c1.add('1000000*3/100', 'CRR balance at 3%')
    slr = c1.add('1000000*18/100', 'SLR holding at 18%')
    free = c1.add('1000000-30000-180000', 'funds available for lending')
    rel = c1.add('1000000*0.5/100', 'released by 0.5 point CRR cut')

    c2 = Checks()
    rp = c2.add('round(500*5.25/100/365*100,2)', 'repo interest for one night (₹ lakh)')
    ms = c2.add('round(500*5.50/100/365*100,2)', 'MSF interest for one night (₹ lakh)')
    df = c2.add('round(7.53-7.19,2)', 'extra cost of MSF (₹ lakh)')
    rr = c2.add('round(500*3.35/100/365*100,2)', 'reverse repo income for one night (₹ lakh)')

    c3 = Checks()
    sp1 = c3.add('5.50-5.25', 'MSF minus repo')
    sp2 = c3.add('5.25-3.35', 'repo minus reverse repo')

    c4 = Checks()
    avgA = c4.add('round((6.4+6.8+6.2)/3,2)', 'average of three quarters A')
    avgB = c4.add('round((6.9+5.8+6.5)/3,2)', 'average B')

    q1 = Checks()
    q1c = q1.add('2500000*3/100', 'CRR')
    q1s = q1.add('2500000*18/100', 'SLR')
    q1f = q1.add('2500000-75000-450000', 'lendable')
    q1r = q1.add('2500000*0.25/100', 'released by 0.25 cut')
    q1m = q1.add('25000*4', 'potential money supply effect at m = 4')

    q2 = Checks()
    q2a = q2.add('round(800*5.25/100*7/365*100,2)', '7-day repo cost (₹ lakh)')
    q2b = q2.add('round(800*5.50/100*7/365*100,2)', '7-day MSF cost (₹ lakh)')
    q2c = q2.add('round(80.55-80.55+80.55,2)', 'repo cost restated')
    q2d = q2.add('round(84.38-80.55,2)', 'difference')

    q3 = Checks()
    q3a = q3.add('round((1.9+1.7+1.8)/3,2)', 'avg low quarters')
    q3b = q3.add('round((5.9+6.3+6.6)/3,2)', 'avg high quarters')

    k = Checks()
    k1 = k.add('round(200*5.25/100/365*100,2)', 'case repo cost')
    k2 = k.add('round(200*5.50/100/365*100,2)', 'case MSF cost')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch08', 'n': 3,
        'title': 'Monetary Policy',
        'outcomes': [
            'Define monetary policy and describe its framework — objectives, transmission (analytics) and operating procedure.',
            'Explain the channels of monetary transmission: saving–investment (interest rate), cash-flow, asset price and wealth, exchange rate and credit channels.',
            'Explain quantitative tools (CRR, SLR, OMO, bank rate, LAF — repo, reverse repo, MSF — and MSS) and qualitative tools (margin requirements, moral suasion, selective credit control), with the current rates quoted in the study material.',
            'Describe India\'s flexible inflation targeting framework and the Monetary Policy Committee — the 2016 amendment, the 4% ± 2% CPI target, and what counts as failure.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 45, 'practice': 50}, 'prereq': ['fnd-p4-ch08-u02'],
                 'exam_tip': 'Know the direction of every tool (tight vs easy money), the definitions (repo = RBI lends against securities; reverse repo = RBI borrows), the MPC (6 members, majority vote) and the target (CPI 4% with 2%–6% band; failure = average outside the band for three consecutive quarters). Quote the rates given in your study material: repo 5.25%, MSF 5.50%, reverse repo 3.35%, CRR 3%, SLR 18%.'},
        'concepts': [
            {'id': 'c1', 'title': 'Introduction and definition of monetary policy',
             'body': ['The RBI periodically changes policy rates to steer liquidity and explains why. Monetary policy is how the central bank tries to stabilise the economy.',
                      'Monetary policy is the central bank\'s use of its instruments to influence how much money and credit is available, what it costs and how it is used, in order to promote growth, price stability, optimum output and employment, balance-of-payments equilibrium, a stable currency or other goals of economic policy.',
                      'The RBI uses it mainly to achieve price stability — low and stable inflation — while supporting growth. It adjusts money supply, typically by buying or selling securities in the open market, which changes short-term interest rates; these in turn affect long-term rates and activity.',
                      'Lowering interest rates = easing (accommodative) policy; raising them = tightening.'],
             'analogy': 'Monetary policy is the economy\'s water valve: open it (cheaper, more money) when growth is dry, tighten it when prices are flooding.',
             'work': 'Every RBI policy announcement changes loan EMIs, deposit rates and bond prices — CAs in banks, treasuries and wealth management react the same day.'},
            {'id': 'c2', 'title': 'The monetary policy framework and its objectives',
             'body': ['Three components: (i) objectives; (ii) analytics — the transmission mechanism; (iii) operating procedure — operating targets and instruments.',
                      'The RBI Act, 1934 (preamble) sets the aim: to regulate the issue of bank notes and keep reserves to secure monetary stability, and to operate the currency and credit system to the country\'s advantage. The core objective has been a sensible balance between price stability and growth.',
                      'Developing countries add explicit objectives: sustaining growth, adequate credit to productive sectors, a moderate interest-rate structure to encourage investment, and an efficient government securities market. With a more open economy and financial reforms, financial stability and exchange-rate stability have gained importance in India.',
                      'Worldwide, the most common objectives today are price stability (controlling inflation) and growth.'],
             'analogy': 'Like a car with two goals — reaching quickly (growth) and safely (stable prices): the driver must balance speed and control.',
             'work': 'Bank ALCO meetings begin with the RBI\'s stated stance and objectives, because they decide the direction of rates for the bank\'s assets and liabilities.'},
            {'id': 'c3', 'title': 'Transmission of monetary policy — the channels',
             'body': ['Transmission is how changes in policy settings flow through to activity and inflation, in two stages: policy changes affect interest rates; interest rates affect spending and inflation. The timing and size of effects are uncertain and lagged.',
                      'Saving and investment (interest-rate) channel: lower deposit rates reduce the reward for saving and encourage spending; lower loan rates encourage households to borrow (supporting demand for housing and other assets) and firms to invest, as projects more easily beat the cost of borrowing — especially firms that rely on debt. A contractionary rate rise does the reverse: it raises the cost of capital and real borrowing costs for firms and households.',
                      'Cash-flow channel: lower lending rates cut interest payments, leaving more cash for spending — important for liquidity-constrained borrowers (e.g. floating-rate home loans). Lower deposit income may make some savers spend less, but the first effect is larger, so spending rises overall.',
                      'Asset prices and wealth channel: lower rates raise asset prices (housing, shares) because future income is discounted at a lower rate; higher asset values increase collateral and make borrowing easier; higher wealth raises consumption and housing investment.',
                      'Exchange rate channel: if Indian rates fall relative to the rest of the world, Indian assets become less attractive, capital moves out and the rupee depreciates; exports become more competitive and imports dearer, raising activity — and also inflation through import prices. Most important for export-oriented and import-competing sectors.',
                      'Credit channels: the bank lending channel (policy changes alter banks\' ability and willingness to lend) and the balance sheet channel (policy changes the net worth and cash flows of firms and households, and so their access to credit). Some texts call these the quantum channel.'],
             'blocks': [table(['Channel', 'Effect of a rate CUT'], [['Saving & investment', 'Less saving, more borrowing, more investment'], ['Cash flow', 'Lower EMIs leave more cash to spend'], ['Asset prices & wealth', 'Higher house and share prices, more collateral, more spending'], ['Exchange rate', 'Rupee weakens → exports rise, imports dearer, some inflation'], ['Credit', 'Banks lend more; stronger borrower balance sheets']], title='Transmission channels')],
             'analogy': 'A rate change is a stone dropped in a pond; the channels are the different ripples reaching different shores — savers, borrowers, asset owners and exporters.',
             'work': 'Since rates on most new bank loans are linked to an external benchmark like the repo rate, CAs in lending firms see transmission directly in EMIs.'},
            {'id': 'c4', 'title': 'Operating procedure — quantitative tools',
             'body': ['Quantitative tools affect money supply across the whole economy — manufacturing, agriculture, housing, autos and so on.',
                      'Cash Reserve Ratio (CRR): the share of net demand and time liabilities (NDTL) a scheduled commercial bank must keep as cash with the RBI, whatever its size. It earns nothing and cannot be lent. CRR = 3% (as on 5 August 2026). A CRR cut releases funds and expands credit — used in deflation or slowdown; a hike absorbs funds.',
                      'Statutory Liquidity Ratio (SLR): the share of NDTL that banks must hold themselves in cash, gold or approved securities such as government securities; these earn some (low) interest. SLR = 18% (as on 5 August 2026).',
                      'Open Market Operations (OMO): the RBI buys or sells government securities in the market to adjust rupee liquidity. Selling securities absorbs liquidity (anti-inflationary — used to control inflation); buying injects liquidity (used in a slowdown or liquidity shortage). Exam note: the study material says sales suck liquidity out and purchases do the opposite, but its next sentence, as printed, attaches "to control inflation" to purchases — a slip. In the exam, link OMO sales with controlling inflation and OMO purchases with easing. OMOs also smooth temporary liquidity mismatches, for example from foreign capital flows.',
                      'Market Stabilisation Scheme (MSS): to absorb surplus liquidity (typically from large capital inflows), the Government issues additional treasury bills or dated securities over and above its normal borrowing; the proceeds are kept in a separate account with the RBI.'],
             'analogy': 'CRR is money locked in the RBI\'s safe; SLR is money the bank must keep in its own safe in specified forms; OMO is the RBI\'s sponge — squeezing in or soaking up liquidity.',
             'work': 'Bank treasurers compute daily CRR and SLR positions; a shortfall attracts a penalty linked to the bank rate.'},
            {'id': 'c5', 'title': 'Policy rates — bank rate and the Liquidity Adjustment Facility',
             'body': ['Bank rate: the standard rate at which the RBI is prepared to buy or rediscount bills of exchange or other eligible commercial paper — in practice the rate for longer-term funds. Today it is mainly used to set penalties for banks that fall short of CRR or SLR; the RBI steers money supply chiefly through the LAF repo rate. (The bank rate is aligned to the MSF rate.)',
                      'Liquidity Adjustment Facility (LAF): introduced on the recommendations of the Narasimham Committee on banking reforms; through it the RBI adjusts day-to-day liquidity via repos and reverse repos.',
                      'Repo (repurchase agreement): banks borrow short-term funds from the RBI by selling government securities with an agreement to buy them back at a set price and date — collateralised lending. The fixed overnight repo rate under LAF is the policy rate. Repo rate = 5.25% (as on 5 August 2026).',
                      'Reverse repo: the RBI borrows from banks (absorbs liquidity) by selling them securities with an agreement to repurchase; the rate the RBI pays banks for parking surplus funds. Reverse repo rate = 3.35% (as on 5 August 2026).',
                      'Marginal Standing Facility (MSF): a penal window where scheduled banks borrow overnight over and above LAF by dipping into their SLR securities up to a limit (the material says a maximum of 1% of SLR securities; under current RBI operating rules a bank may dip into SLR holdings up to 2% of its NDTL for MSF). MSF rate = 5.50% (as on 5 August 2026), i.e. 0.25 percentage point above repo. Older texts give the relations MSF = repo + 1 and reverse repo = repo − 1; quote the current figures in the exam.',
                      'For awareness (beyond the material): since April 2022 the floor of the corridor is the Standing Deposit Facility (SDF), at 0.25 percentage point below repo; the fixed-rate reverse repo at 3.35% continues alongside.'],
             'blocks': [table(['Rate (5 Aug 2026)', '%', 'Direction of funds'], [['Repo (policy rate)', '5.25', 'RBI lends to banks against securities'], ['Marginal Standing Facility', '5.50', 'RBI lends overnight at a penal rate (from SLR securities)'], ['Reverse repo', '3.35', 'Banks park surplus funds with RBI'], ['CRR', '3', 'Cash kept with RBI (NDTL)'], ['SLR', '18', 'Liquid assets kept by banks (NDTL)']], title='Policy rates and ratios quoted in the study material')],
             'analogy': 'Repo is a pawn-shop loan: the bank hands over bonds, takes cash, and buys the bonds back tomorrow. Reverse repo is the bank lending its spare cash to the pawn-shop owner (RBI).',
             'work': 'Bank treasuries choose between the repo window, the inter-bank call market and MSF every day; MSF use signals tight liquidity.'},
            {'id': 'c6', 'title': 'Qualitative (selective) tools',
             'body': ['Qualitative tools affect credit to specific sectors rather than total money supply.',
                      'Margin requirements: the RBI prescribes the margin a borrower must bring against collateral; raising margins reduces how much can be borrowed (e.g. against shares or commodities).',
                      'Moral suasion: persuasion by the RBI — letters, meetings, speeches — urging banks to lend to or avoid certain sectors.',
                      'Selective credit control: restricting credit to particular industries or speculative activities.'],
             'analogy': 'Quantitative tools change the size of the river; qualitative tools dig channels that send water to some fields and not others.',
             'work': 'Higher margins on loans against shares or gold directly change how much a client can borrow — a practical point in wealth advisory.'},
            {'id': 'c7', 'title': 'Organisational structure — MPC and flexible inflation targeting',
             'body': ['The RBI Act, 1934 was amended (effective 27 June 2016) to put the Monetary Policy Framework Agreement (MPFA) on a legal footing and to create a Monetary Policy Committee (MPC). The MPFA is an agreement between the Government and the RBI on the maximum tolerable inflation the RBI should target; the amended Act provides the statutory basis for flexible inflation targeting.',
                      'Inflation targeting means announcing an official target range for inflation. The Expert Committee under Urjit Patel (January 2014) recommended dropping the "multiple indicator" approach and making inflation targeting the primary objective.',
                      'The Government, in consultation with the RBI, sets the target once every five years. It notified CPI inflation of 4% with an upper tolerance of 6% and a lower tolerance of 2% for 5 August 2016 to 31 March 2021; the same target was retained for April 2021 to March 2026.',
                      'Failure to meet the target: average inflation above the upper tolerance level for any three consecutive quarters, or below the lower tolerance level for any three consecutive quarters.',
                      'Twice a year (every six months) the RBI must release a Monetary Policy Report setting out where inflation is coming from and its forecasts for the next six to eighteen months.',
                      'CPI was chosen because it reflects the cost of living and strongly influences inflation expectations. India thus joined countries such as New Zealand, the US, the UK, the euro area and Brazil; some countries are now considering nominal GDP targeting.',
                      'The MPC has six members: the RBI Governor (chairperson), the Deputy Governor in charge of monetary policy, one RBI officer nominated by the Central Board, and three external members appointed by the Central Government. It sets the policy repo rate needed to reach the target by debate and majority vote; the Governor has a casting vote in a tie.'],
             'blocks': [table(['Item', 'Detail'], [['Legal basis', 'RBI Act amended, effective 27 June 2016'], ['Target', 'CPI inflation 4%, band 2%–6%'], ['Who sets target', 'Government in consultation with RBI, every 5 years'], ['Failure', 'Average outside the band for 3 consecutive quarters'], ['MPC', '6 members; majority vote; Governor\'s casting vote'], ['Report', 'Monetary Policy Report every 6 months']], title='Flexible inflation targeting in India')],
             'analogy': 'The government sets the thermostat (4% ± 2%); the MPC is the committee that turns the dial (repo rate) to keep the room within that range.',
             'work': 'Economists in banks and corporates forecast each MPC decision from CPI prints relative to the 4% target and the 6% upper band.'},
            {'id': 'c8', 'title': 'Conclusion — why monetary policy is hard',
             'body': ['Choosing a policy action is complicated by uncertainty and the need to balance growth and inflation.',
                      'Emerging markets like India face extra problems: rudimentary and non-competitive financial systems, poorly integrated money and inter-bank markets, external uncertainties, and limits to the central bank\'s operational autonomy. Inflation is also driven by oil and food prices, which monetary policy cannot control directly.',
                      'Explicit inflation targeting needs operational autonomy for the central bank and good coordination between fiscal and monetary authorities.'],
             'analogy': 'Steering a ship in fog with a delayed rudder: you act on today\'s readings, but the turn happens months later.',
             'work': 'Interest-rate risk management in companies (hedging, fixed vs floating debt) exists precisely because monetary policy outcomes are uncertain.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'CRR and SLR on a bank\'s balance sheet', 'difficulty': 'core', 'minutes': 5,
             'q': f'A bank\'s net demand and time liabilities are ₹{inr(ndtl)} crore. With CRR 3% and SLR 18%, find the CRR balance, SLR holding and funds available for lending. How much is released if CRR is cut by 0.5 percentage point?',
             'solution': [table(['Item', '₹ crore'], [['NDTL', ndtl], ['Less: CRR (3%) kept as cash with RBI', -crr], ['Less: SLR (18%) in approved securities', -slr], ['Available for lending', free]], num=[1], total=True),
                          p(f'A 0.5 point CRR cut releases 0.5% × {inr(ndtl)} = ₹{inr(rel)} crore of lendable funds.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Cost of overnight borrowing: repo vs MSF', 'difficulty': 'moderate', 'minutes': 6,
             'q': 'A bank needs ₹500 crore overnight. Find the interest cost (₹ lakh, 365-day year) under repo at 5.25% and under MSF at 5.50%. Another bank parks ₹500 crore overnight under reverse repo at 3.35%; find its income.',
             'solution': [table(['Window', 'Rate %', 'Interest for 1 night (₹ lakh)'], [['Repo', 5.25, rp], ['MSF', 5.50, ms], ['Reverse repo (income)', 3.35, rr]]),
                          p(f'MSF costs ₹{df} lakh more per night — a penalty for not planning liquidity.')],
             'checks': c2},
            {'id': 'i3', 'title': 'The policy corridor', 'difficulty': 'core', 'minutes': 3,
             'q': 'Using the rates in the study material, find the gap between MSF and repo, and between repo and reverse repo.',
             'solution': [p(f'MSF − repo = 5.50 − 5.25 = {sp1} percentage point; repo − reverse repo = 5.25 − 3.35 = {sp2} percentage points. Overnight inter-bank rates normally stay between the floor and the MSF ceiling, close to the repo rate.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Has the RBI failed to meet the target?', 'difficulty': 'moderate', 'minutes': 5,
             'q': 'Quarterly average CPI inflation: Case A — 6.4%, 6.8%, 6.2% in three consecutive quarters. Case B — 6.9%, 5.8%, 6.5%. Has the inflation target been missed in each case?',
             'solution': [p(f'Case A: every one of three consecutive quarters is above 6% (average of the three {avgA}%) → failure; the RBI must report reasons and remedial actions to the Government.'),
                          p(f'Case B: the middle quarter (5.8%) is within the band, so there are not three consecutive quarters above 6% (even though the three-quarter mean is {avgB}%) → not a failure under the rule.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Floating-rate loan after a repo hike', 'role': 'CA advising an SME borrower',
             'situation': 'The MPC raises the repo rate by 0.25%; the client\'s working-capital loan is linked to repo.',
             'steps': ['Explain transmission: the external benchmark rate rises, so the loan rate rises by the same margin at reset.', 'Compute the extra annual interest on the average outstanding balance.', 'Review options — faster collections, cheaper trade credit, or fixing part of the borrowing.'],
             'takeaway': 'Policy decisions reach firms quickly through benchmark-linked loans.',
             'think': 'Which transmission channel is this mainly?', 'answer': 'The cash-flow channel (and the saving–investment/interest-rate channel): higher repayments leave less cash to spend and make new investment costlier.'},
            {'id': 'j2', 'title': 'Treasury liquidity plan', 'role': 'CA in a bank\'s treasury',
             'situation': 'Large tax outflows will drain liquidity next week.',
             'steps': ['Forecast the shortfall.', 'Plan to borrow under repo/LAF using surplus SLR securities rather than the costlier MSF.', 'Keep CRR compliant every day to avoid penalties linked to the bank rate.'],
             'takeaway': 'Knowing the corridor (repo, MSF, reverse repo) saves real money.'},
            {'id': 'j3', 'title': 'Reading an MPC statement for clients', 'role': 'CA in a wealth-management firm',
             'situation': 'The MPC holds the repo rate but changes its stance to neutral.',
             'steps': ['Note CPI relative to the 4% target and 2–6% band.', 'Explain implications for bond prices and fixed-deposit rates.', 'Suggest portfolio duration changes.'],
             'takeaway': 'The inflation-targeting framework gives a clear yardstick for interpreting decisions.'},
        ],
        'mcqs': [
            M('m1', 'Monetary policy refers to the use of instruments by the central bank to regulate:', ['How much money and credit is available, its cost and its use', 'Government spending and taxation', 'Exchange rates only', 'Prices of individual goods'], 0, 'That is the standard definition; fiscal policy uses the budget.', 'c1'),
            M('m2', 'When the central bank lowers interest rates, monetary policy is said to be:', ['Easing', 'Tightening', 'Neutralising', 'Contractionary'], 0, 'Lower rates = easier money.', 'c1'),
            M('m3', 'The main objective of monetary policy in India is:', ['Price stability while keeping in mind the objective of growth', 'Reducing food shortages', 'Balancing the government budget', 'Fixing the exchange rate'], 0, 'Flexible inflation targeting: price stability with growth.', 'c2'),
            M('m4', 'The three components of the monetary policy framework are:', ['Objectives, analytics (transmission) and operating procedure', 'Taxes, spending and borrowing', 'CRR, SLR and OMO only', 'Allocation, distribution and stabilisation'], 0, 'Objectives, transmission and operating targets/instruments.', 'c2'),
            M('m5', 'The monetary transmission mechanism refers to:', ['The channels through which policy changes affect output and prices', 'Printing and distribution of currency notes', 'Transfer of RBI surplus to the government', 'Clearing of cheques'], 0, 'Transmission links policy settings to economic activity and inflation.', 'c3'),
            M('m6', 'A contractionary policy-induced rise in interest rates:', ['Raises the cost of capital and real borrowing costs for firms and households', 'Raises borrowing costs only for firms', 'Lowers the cost of capital', 'Has no effect on households'], 0, 'Both firms and households face higher borrowing costs.', 'c3'),
            M('m7', 'Lower interest rates raising share and house prices and thus consumption is the:', ['Asset price and wealth channel', 'Exchange rate channel', 'Cash-flow channel', 'Fiscal channel'], 0, 'Higher asset values raise wealth and collateral.', 'c3'),
            M('m8', 'A cut in Indian interest rates relative to world rates tends to:', ['Depreciate the rupee, boost exports and add to inflation', 'Appreciate the rupee and cut exports', 'Leave the exchange rate unchanged', 'Reduce import prices'], 0, 'Capital moves out, the rupee weakens, exports gain, imports cost more.', 'c3', 'moderate'),
            M('m9', 'The Cash Reserve Ratio is maintained by banks:', ['As cash with the RBI, as a share of NDTL', 'In government securities held by the bank', 'As gold with the government', 'In shares of companies'], 0, 'CRR is cash with the RBI; SLR assets are held by the bank itself.', 'c4'),
            M('m10', 'The SLR as on 5 August 2026 (per the study material) is (in %):', ['18', '3', '4', '24'], 0, 'SLR 18%; CRR 3%.', 'c4', 'core', '18'),
            M('m11', 'The CRR as on 5 August 2026 (per the study material) is (in %):', ['3', '4', '18', '5.25'], 0, 'CRR = 3% of NDTL.', 'c4', 'core', '3'),
            M('m12', 'During deflation the RBI would typically:', ['Reduce CRR so banks can expand credit', 'Raise CRR to expand credit', 'Raise SLR to expand credit', 'Sell government securities'], 0, 'A lower CRR releases funds for lending.', 'c4'),
            M('m13', 'NDTL of a bank is ₹10,00,000 crore; CRR 3%, SLR 18%. Funds available for lending are:', ['₹7,90,000 crore', '₹9,70,000 crore', '₹8,20,000 crore', '₹2,10,000 crore'], 0, '10,00,000 − 30,000 − 1,80,000 = 7,90,000. ₹9,70,000 deducts only CRR; ₹8,20,000 only SLR; ₹2,10,000 is the total locked up.', 'c4', 'moderate', '1000000-30000-180000'),
            M('m14', 'To absorb excess liquidity from the market, the RBI will:', ['Sell government securities through OMO', 'Buy government securities through OMO', 'Cut the CRR', 'Cut the repo rate'], 0, 'Banks pay for the securities, draining liquidity.', 'c4'),
            M('m15', 'An open market operation involves buying or selling of:', ['Government securities', 'Shares and debentures of companies', 'Foreign cars', 'Gold jewellery'], 0, 'OMOs are in government securities.', 'c4'),
            M('m16', 'Under the Market Stabilisation Scheme:', ['The government issues additional T-bills/securities to absorb surplus liquidity, the proceeds being held with the RBI', 'Banks borrow overnight from the RBI', 'The RBI cuts the repo rate', 'Exporters get subsidies'], 0, 'MSS is used mainly to sterilise large capital inflows.', 'c4', 'hard'),
            M('m17', 'Under which facility does the RBI provide accommodation to banks through repos and reverse repos?', ['Liquidity Adjustment Facility', 'Market Stabilisation Scheme', 'Statutory Liquidity Ratio', 'Ways and Means Advances'], 0, 'LAF — introduced on Narasimham Committee recommendations.', 'c5'),
            M('m18', 'In India the "policy rate" is:', ['The fixed overnight repo rate under the LAF', 'The bank rate', 'The CRR', 'The MSF rate'], 0, 'The repo rate set by the MPC is the policy rate.', 'c5'),
            M('m19', 'A reverse repo operation takes place when:', ['The RBI borrows from banks by giving them securities', 'Banks borrow from the RBI against securities', 'Banks borrow from each other overnight', 'The RBI lends to the government'], 0, 'It absorbs liquidity; repo injects it.', 'c5'),
            M('m20', 'Per the study material (5 August 2026), the repo rate is (in %):', ['5.25', '5.5', '3.35', '6.5'], 0, 'Repo 5.25%; MSF 5.50%; reverse repo 3.35%.', 'c5', 'core', '5.25'),
            M('m21', 'Banks borrowing overnight beyond LAF by dipping into SLR securities use the:', ['Marginal Standing Facility', 'Reverse repo window', 'Bank rate window only', 'Market Stabilisation Scheme'], 0, 'MSF is a penal-rate window above repo.', 'c5'),
            M('m22', 'A bank borrows ₹500 crore for one night under MSF at 5.50% (365-day year). The interest cost in ₹ lakh is about:', ['7.53', '7.19', '27.5', '4.59'], 0, '500 crore × 5.50% ÷ 365 = ₹0.0753 crore = ₹7.53 lakh. 7.19 uses the repo rate; 4.59 the reverse repo rate.', 'c5', 'hard', 'round(500*5.50/100/365*100,2)'),
            M('m23', 'Today the bank rate is mainly used to:', ['Set penalties for shortfalls in CRR/SLR', 'Determine the daily policy stance', 'Fix the exchange rate', 'Decide SLR'], 0, 'The repo rate is the operating policy rate; bank rate mainly sets penalties.', 'c5', 'moderate'),
            M('m24', 'Raising the margin requirement on loans against shares is a:', ['Qualitative (selective) tool', 'Quantitative tool', 'Fiscal tool', 'Exchange-rate tool'], 0, 'It affects credit to a particular use, not total money supply.', 'c6'),
            M('m25', 'Persuading banks through meetings and letters to restrict lending to a sector is called:', ['Moral suasion', 'Open market operation', 'Repo', 'Guillotine'], 0, 'Moral suasion relies on influence, not legal compulsion.', 'c6'),
            M('m26', 'The Monetary Policy Committee consists of:', ['Six members and decides by majority vote', 'Five members and decides by consensus of the Governor', 'Twelve bankers chosen by the Finance Ministry', 'The Governor alone'], 0, 'Six members (three from RBI, three external); majority vote; Governor\'s casting vote.', 'c7'),
            M('m27', 'The Monetary Policy Framework Agreement is an agreement on:', ['The maximum tolerable inflation the RBI should target', 'The maximum repo rate for government borrowing', 'Minimum SLR', 'Exchange rate bands'], 0, 'It sets the inflation target framework between the Government and the RBI.', 'c7'),
            M('m28', 'The inflation target notified by the Government is:', ['CPI inflation of 4% with a band of 2% to 6%', 'WPI inflation of 4% with a band of 2% to 6%', 'CPI inflation of 6% with a band of 4% to 8%', 'GDP deflator of 3%'], 0, 'CPI-based, 4% ± 2%.', 'c7'),
            M('m29', 'The inflation target is considered missed if average inflation is above the upper tolerance level for:', ['Any three consecutive quarters', 'Any one quarter', 'Two consecutive months', 'Six consecutive quarters'], 0, 'Or below the lower tolerance for three consecutive quarters.', 'c7', 'moderate'),
            M('m30', 'The RBI must publish a Monetary Policy Report every:', ['Six months', 'Month', 'Year', 'Five years'], 0, 'It explains sources of inflation and forecasts for 6–18 months.', 'c7'),
            M('m31', 'Which committee recommended making inflation targeting the primary objective of RBI\'s monetary policy?', ['Urjit Patel Committee (2014)', 'Narasimham Committee', 'Second Working Group on Money Supply', 'Fifteenth Finance Commission'], 0, 'The Expert Committee under Urjit Patel, January 2014.', 'c7'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'The banking system\'s NDTL is ₹25,00,000 crore. With CRR at 3% and SLR at 18%, compute (a) the CRR balance, (b) the SLR holding, (c) funds available for lending. (d) If CRR is cut by 0.25 percentage point and the money multiplier is 4, what is the potential effect on money supply? (e) Name the policy direction.',
             'model': [table(['Item', '₹ crore'], [['NDTL', 2500000], ['Less: CRR 3%', -q1c], ['Less: SLR 18%', -q1s], ['Available for lending', q1f]], num=[1], total=True),
                       p(f'(d) Released = 0.25% × 25,00,000 = ₹{inr(q1r)} crore; potential money supply effect = {inr(q1r)} × 4 = ₹{inr(q1m)} crore. (e) Expansionary (easy) monetary policy.')],
             'scheme': [{'id': 's1', 'pt': 'CRR and SLR amounts', 'm': 2, 'skill': 'computation'}, {'id': 's2', 'pt': 'Lendable funds', 'm': 1, 'skill': 'computation'}, {'id': 's3', 'pt': 'Released funds × multiplier', 'm': 1, 'skill': 'application'}, {'id': 's4', 'pt': 'Policy direction', 'm': 1, 'skill': 'concept'}],
             'remarks': ['Present as a statement with "Less:" lines.'], 'mistakes': ['Applying SLR to the amount left after CRR (both apply to NDTL).'], 'tips': ['State that both ratios are percentages of NDTL.'], 'checks': q1},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'hard', 'pad': 'text',
             'q': 'A bank needs ₹800 crore for 7 days. Compute the interest cost (₹ lakh, 365-day year) if borrowed (a) under repo at 5.25%, (b) under MSF at 5.50%, and (c) the extra cost of MSF. (d) Why does the RBI keep MSF above repo?',
             'model': [p(f'(a) 800 × 5.25% × 7/365 = ₹{q2a} lakh. (b) 800 × 5.50% × 7/365 = ₹{q2b} lakh. (c) Extra = ₹{q2d} lakh.'),
                       p('(d) MSF is a penal window for emergency overnight funds; keeping it above repo encourages banks to plan liquidity and borrow through regular LAF, and it caps overnight market rates (ceiling of the corridor).')],
             'scheme': [{'id': 's1', 'pt': 'Repo cost', 'm': 1.5, 'skill': 'computation'}, {'id': 's2', 'pt': 'MSF cost', 'm': 1.5, 'skill': 'computation'}, {'id': 's3', 'pt': 'Difference', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'Reason for penal rate', 'm': 1, 'skill': 'concept'}],
             'remarks': ['Convert crore to lakh carefully (× 100).'], 'mistakes': ['Forgetting the 7/365 factor.'], 'tips': ['Show the formula: principal × rate × days/365.'], 'checks': q2},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'Quarterly average CPI inflation over six quarters was 1.9%, 1.7%, 1.8%, 5.9%, 6.3%, 6.6%. (a) State the inflation target and tolerance band. (b) Was there a failure in quarters 1–3? (c) In quarters 4–6? (d) What must the RBI do on failure?',
             'model': [p(f'(a) CPI 4%, band 2%–6%. (b) Quarters 1–3 all below 2% (average {q3a}%) → three consecutive quarters below the lower tolerance → failure. (c) Quarter 4 (5.9%) is within the band, so only quarters 5 and 6 exceed 6% (three-quarter mean {q3b}%) → no failure yet.'),
                       p('(d) The RBI must report to the Government the reasons for failure, the remedial actions proposed and the time within which the target will be achieved.')],
             'scheme': [{'id': 's1', 'pt': 'Target and band', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Quarters 1–3 analysis', 'm': 1.5, 'skill': 'analysis'}, {'id': 's3', 'pt': 'Quarters 4–6 analysis', 'm': 1.5, 'skill': 'analysis'}, {'id': 's4', 'pt': 'Consequence of failure', 'm': 1, 'skill': 'application'}],
             'remarks': ['Failure can be on the LOW side too — many candidates forget this.'], 'mistakes': ['Using the average of the three quarters instead of checking each quarter.'], 'tips': ['Check each of the three consecutive quarters against the band.'], 'checks': q3},
        ],
        'revision': {
            'summary': ['Monetary policy regulates availability, cost and use of money and credit; easing = lower rates; tightening = higher rates.',
                        'Framework: objectives (price stability with growth; RBI Act 1934 preamble), transmission (interest rate/saving–investment, cash flow, asset price & wealth, exchange rate, credit channels), operating procedure.',
                        'Quantitative tools: CRR 3% (cash with RBI), SLR 18% (liquid assets with bank), OMO (sell to absorb, buy to inject), MSS, bank rate (penalties), LAF — repo 5.25% (policy rate), reverse repo 3.35%, MSF 5.50%.',
                        'Qualitative tools: margin requirements, moral suasion, selective credit control.',
                        'Flexible inflation targeting: RBI Act amended (27 June 2016); MPFA; CPI 4% ± 2%; target set by Government every five years; failure = three consecutive quarters outside the band; Monetary Policy Report every six months.',
                        'MPC: six members (Governor, Deputy Governor, one RBI officer, three external), majority vote, Governor\'s casting vote.',
                        'Challenges in emerging markets: weak financial systems, poor market integration, external shocks, autonomy, fiscal–monetary coordination.'],
            'remember': ['Repo = RBI lends; reverse repo = RBI borrows.', 'MSF is 0.25 point above repo per current rates; older texts say ±1.', 'Urjit Patel Committee, January 2014.'],
            'traps': ['RBI SELLS securities to fight inflation (absorbs liquidity) — buying injects liquidity.', 'CRR is with the RBI; SLR assets stay with the bank.', 'Failure also occurs if inflation stays BELOW 2% for three quarters.', 'The MPC decides by majority vote, not by the Governor alone.'],
        },
        'quickref': [
            {'k': 'Rates (5 Aug 2026, study material)', 'v': 'Repo 5.25% · MSF 5.50% · Reverse repo 3.35% · CRR 3% · SLR 18%'},
            {'k': 'Repo vs reverse repo', 'v': 'Repo: banks borrow from RBI against securities · Reverse repo: RBI borrows from banks'},
            {'k': 'Inflation target', 'v': 'CPI 4%, band 2%–6%; failure if average outside band for 3 consecutive quarters'},
            {'k': 'MPC', 'v': '6 members: Governor (chair), Deputy Governor (MP), 1 RBI officer, 3 external; majority vote; casting vote'},
            {'k': 'Easy vs tight money', 'v': 'Easy: ↓CRR, ↓repo, OMO purchase · Tight: ↑CRR, ↑repo, OMO sale'},
            {'k': 'Lendable funds', 'v': 'NDTL − CRR% × NDTL − SLR% × NDTL'},
        ],
        'viva': [
            V('v1', 'Distinguish between CRR and SLR.',
              'CRR is cash kept with the RBI: a bank must keep this share of its net demand and time liabilities (NDTL) as cash with the RBI, and it earns no interest. SLR is kept by the bank itself: a share of NDTL held in liquid assets like cash, gold or government securities, which earn some interest.',
              [P('p1', 'CRR — cash kept with the RBI (no interest)', 5, ALT('{c} {k}', '{c} cash {k}', '{c} kept {k}', '{c} kept as cash {k}', c=['crr', 'cash reserve ratio'], k=['rbi', 'reserve bank'])),
               P('p2', 'SLR — liquid assets (cash, gold, G-secs) kept by the bank itself', 5, ALT('{s} {a}', '{s} kept {a}', '{s} share kept {a}', '{s} kept by {a}', s=['slr', 'statutory liquidity ratio'], a=['bank itself', 'banks themselves', 'liquid asset', 'gold', 'government securit', 'approved securit', 'g secs', 'own vault']))], 'c4'),
            V('v2', 'What is the difference between the repo rate and the reverse repo rate?',
              'The repo rate is the rate at which banks borrow short-term funds from the RBI by selling government securities with an agreement to buy them back; it injects liquidity and is the policy rate. The reverse repo rate is the rate at which the RBI borrows from banks, that is, the rate the RBI pays banks for parking surplus funds, which absorbs liquidity.',
              [P('p1', 'Repo — banks borrow from RBI against securities', 5, ALT('repo rate {x}', 'repo {x}', 'repo is {x}', x=('bank borrow from rbi', 'banks borrow from rbi', 'bank borrow from the rbi', 'banks borrow from the rbi', 'bank borrow from reserve bank', 'rbi lend to bank', 'rbi lends to bank', 'rbi lend bank', 'bank borrow short term fund from rbi', 'banks borrow short term from rbi'))),
               P('p2', 'Reverse repo — RBI borrows from banks / banks park funds', 5, ALT('reverse repo {x}', 'reverse repo rate {x}', x=('rbi borrow from bank', 'rbi borrows from bank', 'rbi borrow from the bank', 'rbi borrows from banks', 'bank lend to rbi', 'banks lend to rbi', 'bank park', 'banks park', 'rbi pay bank', 'rbi pays bank', 'rate rbi pay', 'rbi borrow')))], 'c5'),
            V('v3', 'Describe the Monetary Policy Committee and how it decides.',
              'The Monetary Policy Committee was set up under the RBI Act amended in 2016. It has six members: the RBI Governor as chairperson, the Deputy Governor in charge of monetary policy, one RBI officer, and three external members appointed by the Central Government. It decides the policy repo rate needed to achieve the inflation target by majority vote, and the Governor has a casting vote in case of a tie.',
              [P('p1', 'Six members', 3, 'six|6'),
               P('p2', 'Governor chairs; three external members appointed by Government', 3, 'governor', 'external|government appoint|appointed by|three|outside', min=2),
               P('p3', 'Decides the policy (repo) rate by majority vote', 4, 'majority|vote|voting', 'repo|policy rate|interest rate', min=2)], 'c7'),
            V('v4', 'What is India\'s inflation target and when is it treated as a failure?',
              'The target is consumer price index inflation of four per cent, with an upper tolerance of six per cent and a lower tolerance of two per cent. It is a failure if average inflation stays above six per cent for three consecutive quarters, or below two per cent for three consecutive quarters.',
              [P('p1', 'CPI 4%', 3, '4|four', 'cpi|consumer price', min=2),
               P('p2', 'Band 2% to 6%', 3, '2|two', '6|six', min=2),
               P('p3', 'Failure: outside the band for three consecutive quarters', 4, 'three|3', 'consecutive|in a row|successive|continuous', 'quarter', min=3)], 'c7'),
            V('v5', 'Explain how a cut in the repo rate is transmitted to the economy.',
              'A repo rate cut lowers banks\' cost of funds, so lending and deposit rates fall. Lower deposit rates reduce saving and lower loan rates encourage households to borrow and firms to invest. Lower EMIs leave people with more cash to spend. Lower rates also raise asset prices like shares and houses, increasing wealth and spending, and may weaken the rupee, helping exports. Overall demand and output rise, with some upward pressure on inflation.',
              [P('p1', 'Lower lending/deposit rates → more borrowing and investment', 4, 'borrow|invest|loan|lending', 'lower|cheaper|fall|reduc|cut', min=2),
               P('p2', 'Names at least two channels (cash flow / asset prices & wealth / exchange rate / saving)', 4, 'emi|cash flow|repayment', 'asset|share|house|wealth|stock', 'exchange rate|rupee|export|currenc', 'saving|save', min=2),
               P('p3', 'Demand / output rises; inflation pressure', 2, 'demand|output|growth|spending|activit', 'rise|increas|more|boost|higher|inflation', min=2)], 'c3'),
            V('v6', 'How does the RBI use open market operations to control inflation?',
              'To control inflation the RBI sells government securities in the open market. Banks and the public pay for them, so liquidity is absorbed, bank reserves fall and money supply and credit contract. To inject liquidity during a slowdown the RBI buys government securities instead.',
              [P('p1', 'Sells government securities to fight inflation', 5, ALT('{s} government securit', '{s} securit', '{s} g secs', '{s} bond', 'inflation {s}', s=('sell', 'sells', 'selling', 'sale of', 'sale'))),
               P('p2', 'Liquidity / reserves / money supply absorbed', 3, 'liquidit|reserve|money supply|credit', 'absorb|fall|reduc|contract|drain|suck|less|decreas', min=2),
               P('p3', 'Buys securities to inject liquidity', 2, ALT('{b} government securit', '{b} securit', '{b} bond', '{b} g secs', b=('buy', 'buys', 'buying', 'purchase', 'purchases')))], 'c4'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'A tight week for Pragati Bank', 'difficulty': 'hard',
            'case': ('Pragati Bank has NDTL of ₹40,000 crore and has run short of funds after large advance-tax outflows. It needs ₹200 crore for one night. It can borrow under LAF repo at 5.25% '
                     'using surplus government securities, or under MSF at 5.50% by dipping into its SLR holdings. The same week the MPC, citing CPI inflation of 6.4% for the third straight quarter, raises the repo rate.'),
            'mcqs': [
                M('k1a', 'The one-night interest cost under repo (₹ lakh, 365-day year) is about:', ['2.88', '3.01', '10.5', '1.84'], 0, '200 × 5.25% ÷ 365 = ₹0.0288 crore = ₹2.88 lakh. 3.01 uses MSF; 1.84 uses the reverse repo rate.', 'c5', 'moderate', 'round(200*5.25/100/365*100,2)'),
                M('k1b', 'Under MSF, Pragati Bank is:', ['Borrowing overnight at a penal rate by dipping into SLR securities', 'Lending surplus funds to the RBI', 'Selling securities to the public', 'Borrowing from the government'], 0, 'MSF is the penal overnight window above repo.', 'c5', 'core'),
                M('k1c', 'With CPI at 6.4% for three straight quarters, the RBI has:', ['Failed to meet the inflation target and must report reasons and remedies to the Government', 'Met its target', 'Missed the target only if inflation crosses 8%', 'No obligation as the target is advisory'], 0, 'Three consecutive quarters above 6% = failure.', 'c7', 'moderate'),
                M('k1d', 'The MPC\'s repo hike will, through the cash-flow channel:', ['Raise EMIs on floating-rate loans, leaving borrowers less cash to spend', 'Lower EMIs', 'Increase exports immediately', 'Reduce CRR'], 0, 'Higher benchmark rates raise repayments.', 'c3', 'moderate'),
            ]}],
    }
