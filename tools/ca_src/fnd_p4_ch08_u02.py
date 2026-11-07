"""CA Foundation · Paper 4 Business Economics · Chapter 8 Money Market · Unit 2 The Concept of Money Supply.
Original explanations, numbers and questions."""
from lib import *
from ca_viva import P, ALT, V

UID = 'fnd-p4-ch08-u02'


def M(i, q, o, a, e, c=None, d='core', check=None, topic=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if topic: m['topic'] = topic
    if c: m['concept'] = c
    if check: m['check'] = check
    return m


def build():
    c1 = Checks()
    cp, dd, odr, pos, td, pot = 320000, 280000, 6000, 18000, 1450000, 62000
    m1 = c1.add('320000+280000+6000', 'M1')
    m2 = c1.add('606000+18000', 'M2')
    m3 = c1.add('606000+1450000', 'M3')
    m4 = c1.add('2056000+62000', 'M4')

    c2 = Checks()
    cwp = c2.add('3340000+31200+750-118000', 'currency with the public')

    c3 = Checks()
    mm = c3.add('round((1+0.3)/(0.08+0.02+0.3),2)', 'money multiplier')
    ms = c3.add('3.25*60000', 'money supply')
    mm2 = c3.add('round((1+0.3)/(0.13+0.02+0.3),2)', 'multiplier after r rises to 13%')
    mm3 = c3.add('round((1+0.2)/(0.08+0.02+0.2),2)', 'multiplier when c falls to 0.2')
    simple = c3.add('1/0.08', 'simple deposit multiplier')

    c4 = Checks()
    cm8 = c4.add('1/0.08', 'credit multiplier at 8%')
    cr8 = c4.add('200000*12.5', 'total deposits at 8%')
    cm20 = c4.add('1/0.20', 'credit multiplier at 20%')
    cr20 = c4.add('200000*5', 'total deposits at 20%')
    r2 = c4.add('200000*0.92', 'round 2 deposit')
    r3 = c4.add('184000*0.92', 'round 3 deposit')
    r4 = c4.add('169280*0.92', 'round 4 deposit')
    new8 = c4.add('2500000-200000', 'new credit created at 8%')

    c5 = Checks()
    om1 = c5.add('5000/0.1', 'money created by OMO purchase (simple)')
    omm = c5.add('round((1+0.25)/(0.1+0.25),2)', 'multiplier with currency drain')
    om2 = c5.add('round(5000*(1+0.25)/(0.1+0.25))', 'money created with currency drain (exact multiplier 1.25/0.35)')

    q1 = Checks()
    q1m1 = q1.add('240000+410000+9000', 'M1')
    q1m2 = q1.add('659000+35000', 'M2')
    q1m3 = q1.add('659000+1820000', 'M3')
    q1m4 = q1.add('2479000+120000', 'M4')

    q2 = Checks()
    q2c = q2.add('500/1000', 'c')
    q2e = q2.add('5/1000*100', 'e as a percentage of deposits (e = 0.005)')
    q2m = q2.add('round((1+0.5)/(0.1+0.005+0.5),2)', 'm')
    q2ms = q2.add('500+1000', 'M = C + D')
    q2mm = q2.add('round((1+0.5)/(0.15+0.005+0.5),2)', 'm at 15%')
    q2s = q2.add('1/0.1', 'simple multiplier')

    q3 = Checks()
    q3a = q3.add('1/0.125', 'credit multiplier')
    q3b = q3.add('500000*8', 'total deposits')
    q3c = q3.add('4000000-500000', 'new loans/deposits')
    q3d = q3.add('2000/0.125', 'OMO effect')

    k = Checks()
    k1 = k.add('round((1+0.4)/(0.1+0.4),2)', 'case multiplier')
    k2 = k.add('2.8*20000', 'case M')
    k3 = k.add('round((1+0.4)/(0.1+0.1+0.4),2)', 'case multiplier with excess reserves')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch08', 'n': 2,
        'title': 'The Concept of Money Supply',
        'outcomes': [
            'Define money supply and the "public", explain why money supply is measured, and identify its sources — the central bank (high-powered money) and commercial banks (credit money); explain CBDC and the status of crypto-currencies.',
            'Compute the RBI\'s measures M1, M2, M3 and M4 and currency with the public.',
            'Explain the money multiplier and its determinants (currency ratio, reserve ratio, excess reserves), and compute it with m = (1 + c)/(r + e + c); distinguish it from the credit (deposit) multiplier 1/r.',
            'Explain how open market operations and government borrowing from the RBI (WMA/overdraft) change money supply.',
        ],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 55, 'practice': 60}, 'prereq': ['fnd-p4-ch08-u01'],
                 'exam_tip': 'Memorise M1–M4 exactly (M2 and M4 add POST OFFICE deposits; M3 adds TIME deposits of banks). For numericals: m = (1 + c)/(r + e + c); credit multiplier = 1/r. Every ratio — c, r, e — moves inversely with the multiplier.'},
        'concepts': [
            {'id': 'c1', 'title': 'Introduction — money supply and who the "public" is',
             'body': ['Whatever its form, money is a medium of exchange, unit of account and store of value. For policy, money is the set of liquid financial assets whose changes can affect overall economic activity. Stability needs money supply kept at an optimum level — which requires measuring it accurately and regulating it.',
                      'Money supply refers to money held by the public. The "public" means all economic units — households, firms, institutions, local authorities, non-bank financial companies, non-departmental public undertakings, foreign central banks and governments, and the IMF\'s deposits with the RBI — EXCEPT the producers of money: the government (Centre, States, local bodies in this context) and the banking system (RBI and banks accepting demand deposits).',
                      'So inter-bank deposits and money held by the government and banks are excluded.',
                      'Broad money (M3) in international usage covers currency, deposits with agreed maturity up to two years, deposits redeemable at notice up to three months, repos, money-market fund units and debt securities up to two years.'],
             'analogy': 'Money supply counts the water in people\'s buckets, not the water still in the municipal tank (the RBI and banks) or in the government\'s own drums.',
             'work': 'Bank treasury and economics teams track the RBI\'s fortnightly money-supply data to anticipate liquidity and interest-rate moves.'},
            {'id': 'c2', 'title': 'Rationale of measuring money supply',
             'body': ['(1) Analysis: it helps understand the causes of money growth.',
                      '(2) Policy: it tells whether the money stock is consistent with price stability, and why it deviates. Central banks stabilise prices and GDP growth by managing the monetary base; the success of monetary policy depends on how controllable the monetary base and money supply are.'],
             'analogy': 'You cannot regulate the water level of a dam without a gauge — measuring money supply is the gauge.',
             'work': 'Economists use money growth as one input when forecasting inflation and RBI policy decisions for clients.'},
            {'id': 'c3', 'title': 'Sources of money supply; CBDC and crypto-currencies',
             'body': ['Money supply depends on (a) the central bank\'s decisions under its legal authority and (b) the response of commercial banks to the central bank\'s policy changes.',
                      'Currency is issued only by the sovereign or the central bank on its behalf, and is legal tender. Paper currency is representative money — a debt instrument: a liability of the central bank (and government) and an asset of the public. The central bank is the primary source of money; the high-powered money it issues is the base for all other money. Its fiat money is backed by reserves and guaranteed by the government.',
                      'In principle currency should be backed by assets (gold, foreign exchange); in practice most countries use a minimum reserve system — the central bank may issue any amount of currency while holding only a prescribed minimum of gold and foreign assets as backing.',
                      'The second source is commercial banks: they create credit money through lending and borrowing with the public. High-powered money plus credit money make up the common measure of money stock.',
                      'Money has evolved from commodity to metallic to paper to digital. A Central Bank Digital Currency (CBDC) is legal tender issued by a central bank in digital form — like sovereign currency, exchangeable at par, a medium of payment and safe store of value, and a liability of the central bank. The RBI is introducing the Digital Rupee (e₹) in phases through pilots.',
                      'Crypto-currencies are not legally recognised as currency in India and are not counted as money. The RBI has clarified that banks cannot rely on its 2018 circular (which barred dealing in virtual currencies) — that circular was set aside.'],
             'analogy': 'The RBI pours the first jug of water (high-powered money); banks keep passing part of it from glass to glass, so the total water people can drink is many times the jug.',
             'work': 'Banks\' finance teams must classify CBDC holdings and understand that crypto assets are not "cash or cash equivalents" for accounting or regulatory purposes in India.'},
            {'id': 'c4', 'title': 'Measurement of money supply — M1, M2, M3, M4',
             'body': ['Many forms of credit money make measurement hard, and measures differ by country, time and purpose. The RBI has compiled monetary statistics since July 1935. Until 1967-68 it published only narrow money M1 (currency + demand deposits with the public). From 1967-68 it added "aggregate monetary resources" (AMR). From April 1977, on the Second Working Group\'s recommendations, it publishes four measures plus reserve money.',
                      'M1 = currency notes and coins with the public + demand deposits with the banking system (current accounts and savings accounts) + other deposits with the RBI.',
                      'M2 = M1 + savings deposits with post office savings banks.',
                      'M3 = M1 + time deposits with the banking system. M3 is "broad money" and the most widely used measure.',
                      'M4 = M3 + total deposits with the Post Office Savings Organisation (excluding National Savings Certificates).',
                      'Liquidity falls from M1 to M4: M1 is the most liquid. Currency with the public = notes in circulation + rupee coins + small coins − cash on hand with banks.',
                      'Reserve money (monetary base, high-powered money) = currency in circulation + other deposits with the RBI + balances that banks hold with the RBI.'],
             'blocks': [table(['Measure', 'Definition', 'Type'], [['M1', 'Currency with public + demand deposits of banks + other deposits with RBI', 'Narrow money'], ['M2', 'M1 + post office savings bank deposits', 'Narrow'], ['M3', 'M1 + time deposits of banks', 'Broad money'], ['M4', 'M3 + all post office savings deposits (excl. NSC)', 'Broad']], title='RBI measures of money supply')],
             'analogy': 'M1 is cash in hand plus money in your current account; M3 adds your fixed deposits; M2 and M4 add post office savings.',
             'work': 'Bank auditors verify the "demand" and "time" liability classification banks report to the RBI, because those numbers feed M1 and M3 and also determine CRR/SLR.'},
            {'id': 'c5', 'title': 'Determinants of money supply and the money multiplier concept',
             'body': ['Two views: money supply is exogenous (fixed by the central bank) or endogenous (driven by economic activity, people\'s currency preferences, interest rates). Current practice uses the money-multiplier approach, linking money stock to the monetary base (currency in circulation + bank reserves); total money supply is jointly determined by the central bank, commercial banks and the public.',
                      'The RBI creates the monetary base (high-powered money, H). Banks lend out excess reserves, creating deposits, so a one-rupee rise in H raises money supply by more than one rupee.',
                      'M = C + D (currency with the public + deposits). M = m × H, so the money multiplier m = money supply ÷ monetary base. Example: if a ₹100 crore open market purchase finally adds ₹400 crore to money supply, m = 4.',
                      'Simplest case (banks hold no excess reserves and the public holds no currency): m = 1/R, where R is the reserve ratio. At R = 10%, m = 10; at R = 5%, m = 20. Higher reserve ratio → smaller multiplier.',
                      'Money that leaks into currency is not multiplied; only the part that supports deposits is. So holding more cash shrinks the multiplier.'],
             'analogy': 'High-powered money is the seed; the money multiplier is how many plants grow from it. Seeds kept in the pocket (currency) never sprout.',
             'work': 'Treasury analysts estimate how much a CRR change will release or absorb — a direct multiplier calculation.'},
            {'id': 'c6', 'title': 'The money multiplier approach (Friedman and Schwartz)',
             'body': ['Milton Friedman and Anna Schwartz (1963) named three proximate determinants: (a) the stock of high-powered money H — behaviour of the central bank; (b) the reserve ratio r = reserves/deposits — behaviour of commercial banks; (c) the currency–deposit ratio c = C/D — behaviour of the public.',
                      'Central bank: with public and bank behaviour unchanged, money supply varies directly with H.',
                      'Commercial banks: a higher required reserve ratio forces banks to contract loans and deposits — money supply falls; a lower one expands it. Banks often hold excess reserves (ER = total reserves − required reserves) as a buffer. The excess reserve ratio e falls when market interest rates rise (higher opportunity cost of idle reserves) and rises when banks fear larger deposit withdrawals. In crises banks may refuse to lend to small firms even when policy rates are cut, slowing money growth despite easy policy (e.g. banks parked huge sums in the RBI\'s reverse repo window during COVID-19 despite a low 3.35% rate).',
                      'Public: when deposits are converted into currency, less credit can be created — m and money supply are inversely related to c. The currency ratio reflects banking habits, and falls with financial development, easier access, new liquid assets and innovation. A higher time-deposit to demand-deposit ratio frees reserves and enlarges deposit expansion.',
                      'Derivation: M = C + D and H = C + Reserves. With c = C/D and r = Reserves/D: M = (1 + c)D and H = (c + r)D, so m = (1 + c)/(r + c) and M = m × H. With excess reserves: m = (1 + c)/(r + e + c).',
                      'm is a function of c (set by depositors), e (set by banks) and r (set by the central bank through CRR and settlement needs). The lower these ratios, the larger the multiplier.'],
             'blocks': [table(['Ratio', 'Whose behaviour', 'If it rises, m…'], [['c = C/D', 'Public', 'Falls'], ['r = required reserves/D', 'Central bank (CRR)', 'Falls'], ['e = excess reserves/D', 'Commercial banks', 'Falls'], ['H', 'Central bank', 'M rises (m unchanged)']], title='Proximate determinants of money supply')],
             'analogy': 'Each ratio is a leak in a pipe: the more water leaks out as cash (c) or is held back in tanks (r, e), the less reaches the end of the pipe.',
             'work': 'Bank ALM committees decide how much excess liquidity to hold; collectively these decisions change e and the economy-wide multiplier.'},
            {'id': 'c7', 'title': 'Credit multiplier and its difference from the money multiplier',
             'body': ['The credit (deposit) multiplier shows how much additional deposit money the banking system creates by lending reserves above the requirement. Credit multiplier = 1 ÷ required reserve ratio. At 20%, it is 5.',
                      'It results from fractional-reserve banking: when a bank lends part of a deposit, the borrower gets a new deposit while the original depositor keeps his claim — the bank has more liabilities than cash. Example with a 10% ratio: an initial deposit of ₹1,000 supports loans of ₹900, then ₹810, ₹729 and so on, until total deposits reach 1,000 × 1/0.10 = ₹10,000.',
                      'Money created by banks is no different from money issued by the central bank, but creating money is not the same as creating wealth.',
                      'The two multipliers differ because banks usually hold more than the minimum reserves, and borrowers convert part of their loans into cash. So the actual money multiplier is smaller than 1/r.'],
             'analogy': 'A rumour passed along a chain — each person repeats 90% of what they heard; the total words spoken add up to ten times the original sentence.',
             'work': 'Credit-growth projections for banks start from deposits and the reserve requirement — a practical credit multiplier exercise.'},
            {'id': 'c8', 'title': 'Monetary policy, government expenditure and money supply',
             'body': ['To stimulate activity the central bank injects liquidity, e.g. through an open market purchase of government securities, which adds to banks\' reserves (monetary base). If banks hold no excess reserves, people do not hold extra currency and borrowers want loans, ΔMoney supply = (1/R) × ΔReserves.',
                      'An open market sale works the other way — it drains reserves and reduces money supply. (Exam note: one sentence of the study material, as printed, says an open market purchase reduces reserves; that is a slip — the material\'s own preceding sentences, and standard theory, show that a purchase injects reserves and a sale withdraws them. Answer on that basis.)',
                      'Can the multiplier be zero? Yes — if interest rates are very low and banks simply hold new reserves as risk-free excess reserves, nothing is lent out.',
                      'Government expenditure: when Central or State cash balances fall below the minimum, they can use the RBI\'s Ways and Means Advances (WMA) or overdraft. When the government spends this money, its account with the RBI is debited and the recipient\'s account in a commercial bank (say a government employee\'s salary account) is credited — banks\' balances with the RBI rise. These excess reserves can expand money supply through the multiplier.'],
             'analogy': 'An open market purchase is the RBI buying bonds from banks with freshly created money — like topping up every bank\'s tank so more water can flow out as loans.',
             'work': 'Liquidity forecasting desks in banks track government cash balances with the RBI, because government spending from WMA adds reserves to the banking system.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Computing M1, M2, M3 and M4', 'difficulty': 'core', 'minutes': 6,
             'q': f'Data (₹ crore): currency with the public {inr(cp)}; demand deposits with banks {inr(dd)}; other deposits with RBI {inr(odr)}; savings deposits with post office savings banks {inr(pos)}; time deposits with banks {inr(td)}; total post office deposits excluding NSC {inr(pot)}. Compute M1 to M4.',
             'solution': [table(['Measure', 'Working', '₹ crore'], [['M1', f'{inr(cp)} + {inr(dd)} + {inr(odr)}', m1], ['M2', f'M1 + {inr(pos)}', m2], ['M3', f'M1 + {inr(td)}', m3], ['M4', f'M3 + {inr(pot)}', m4]]),
                          note('M2 and M3 are both built on M1, not on each other. M4 adds the total post office deposits to M3.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Currency with the public', 'difficulty': 'core', 'minutes': 3,
             'q': 'Notes in circulation ₹33,40,000 crore; rupee coins ₹31,200 crore; small coins ₹750 crore; cash on hand with banks ₹1,18,000 crore. Find currency with the public.',
             'solution': [p(f'Currency with the public = 33,40,000 + 31,200 + 750 − 1,18,000 = ₹{inr(cwp)} crore. Cash held by banks is excluded because banks are producers of money, not part of the "public".')],
             'checks': c2},
            {'id': 'i3', 'title': 'The money multiplier with currency and excess reserves', 'difficulty': 'hard', 'minutes': 8,
             'q': 'Required reserve ratio r = 8%, excess reserve ratio e = 2%, currency–deposit ratio c = 0.30; high-powered money H = ₹60,000 crore. Find m and M. What happens to m if (a) r rises to 13%, (b) c falls to 0.20? Compare with the simple multiplier.',
             'solution': [p(f'm = (1 + c) ÷ (r + e + c) = 1.30 ÷ 0.40 = {mm}. M = {mm} × 60,000 = ₹{inr(ms)} crore.'),
                          p(f'(a) r = 13%: m = 1.30 ÷ 0.45 = {mm2} — a higher reserve ratio lowers the multiplier.'),
                          p(f'(b) c = 0.20: m = 1.20 ÷ 0.30 = {mm3} — less cash holding raises the multiplier.'),
                          p(f'Simple multiplier 1/r = 1/0.08 = {simple}; the actual multiplier is much smaller because of currency drain and excess reserves.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Credit creation by the banking system', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'A fresh deposit of ₹2,00,000 is made. Required reserve ratio is 8%. Show the first rounds of deposit creation and the total; repeat the total for a 20% ratio.',
             'solution': [table(['Round', 'Deposit ₹', 'Reserve kept (8%) ₹', 'Lent out ₹'], [['1', 200000, 16000, 184000], ['2', r2, round(r2 * 0.08, 2), r3], ['3', r3, round(r3 * 0.08, 2), r4], ['4', r4, round(r4 * 0.08, 2), round(r4 * 0.92, 2)]]),
                          p(f'Credit multiplier = 1/0.08 = {cm8}; total deposits = 2,00,000 × {cm8} = ₹{inr(cr8)} (new credit ₹{inr(new8)}).'),
                          p(f'At 20%: multiplier = {cm20}; total deposits = ₹{inr(cr20)}.')],
             'checks': c4},
            {'id': 'i5', 'title': 'Open market purchase', 'difficulty': 'moderate', 'minutes': 5,
             'q': 'The RBI buys government securities worth ₹5,000 crore from banks. Reserve ratio is 10%. Find the rise in money supply (a) if there is no currency drain or excess reserves, (b) if the public holds currency equal to 25% of deposits.',
             'solution': [p(f'(a) ΔM = (1/0.1) × 5,000 = ₹{inr(om1)} crore.'),
                          p(f'(b) m = 1.25 ÷ 0.35 = {omm}; ΔM = 5,000 × 1.25 ÷ 0.35 ≈ ₹{inr(om2)} crore (using the rounded multiplier {omm} gives about ₹17,850 crore). Currency drain sharply reduces the expansion.')],
             'checks': c5},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Explaining a CRR cut to a board', 'role': 'CA as CFO of a small finance bank',
             'situation': 'The RBI cuts CRR by 0.5 percentage points.',
             'steps': ['Compute reserves released = 0.5% × net demand and time liabilities.', 'Explain that the system-wide money multiplier rises as r falls.', 'Plan deployment — loans if demand exists, otherwise investments (excess reserves raise e and blunt the effect).'],
             'takeaway': 'A CRR change acts directly on the reserve ratio in the money multiplier.',
             'think': 'Why might money supply not rise much after the cut?', 'answer': 'If loan demand is weak or banks are risk-averse, they hold the released funds as excess reserves (higher e), so the multiplier barely changes.'},
            {'id': 'j2', 'title': 'Verifying a bank\'s demand and time liabilities', 'role': 'Articled assistant on a bank branch audit',
             'situation': 'You must check the branch\'s return of demand and time liabilities.',
             'steps': ['Classify current accounts and the demand portion of savings as demand liabilities; fixed deposits as time liabilities.', 'Reconcile with the general ledger.', 'Note that misclassification distorts CRR/SLR and national M1/M3 statistics.'],
             'takeaway': 'The building blocks of M1 and M3 come from millions of bank returns like this one.'},
            {'id': 'j3', 'title': 'Client asks: is crypto money?', 'role': 'CA in practice',
             'situation': 'A client holding crypto assets calls them "cash" in his books.',
             'steps': ['Explain crypto-currencies are not legal tender in India and are not counted as money.', 'Explain the Digital Rupee (CBDC) is legal tender issued by the RBI.', 'Reclassify crypto holdings as investments/virtual digital assets as per applicable law.'],
             'takeaway': 'Legal tender status decides what counts as money.'},
        ],
        'mcqs': [
            M('m1', 'For measuring money supply, the "public" excludes:', ['The government and the banking system', 'Households', 'Non-bank financial companies', 'Local authorities'], 0, "Money supply measures money held by the public, defined to exclude the producers of money — the government and the banking system. Their holdings are not counted, because money they hold is not in circulation for spending. Non-bank financial companies are the tempting trap: they are not part of the banking system, so their money balances are included. In practice: RBI's money-supply data count NBFC and household deposits, but not cash held by banks themselves.", 'c1', topic='Introduction'),
            M('m2', 'Which of the following is part of the "public" for money-supply purposes?', ['Foreign central banks holding deposits with the RBI', 'The Reserve Bank of India', 'Commercial banks accepting demand deposits', 'The Central Government'], 0, "For money-supply purposes, the public includes everyone except the money producers. Deposits held with the RBI by foreign central banks, foreign governments and international bodies such as the IMF count as part of the public's holdings ('other deposits with RBI'). The RBI, commercial banks and the Central Government are traps — they produce or issue money. In practice: these deposits appear as 'other deposits with RBI' in India's M1 figures.", 'c1', 'moderate', topic='Introduction'),
            M('m3', 'Which institution is the basic (primary) source of money supply in every country?', ['Central bank', 'Commercial banks', 'Stock exchange', 'Finance ministry\'s budget'], 0, "The central bank issues currency and holds banks' reserves; together these form high-powered money, the base on which all other money is built — so it is the primary source of money supply. Commercial banks are the trap: they do create credit money, but only on the base provided by the central bank. In practice: RBI's balance sheet determines reserve money, which shapes how much credit banks can extend.", 'c3', topic='The Sources of Money Supply'),
            M('m4', 'Money created by commercial banks through lending is called:', ['Credit money', 'Fiat money', 'Commodity money', 'High-powered money'], 0, "When a commercial bank grants a loan, it credits the borrower's account, creating a new deposit — credit money. 'High-powered money' is the trap: that is currency plus bank reserves, created by the central bank, not by commercial-bank lending. Fiat money is government-declared legal tender. In practice: most money in India's broad money measure consists of bank deposits created through lending, not currency notes.", 'c3', topic='The Sources of Money Supply'),
            M('m5', 'Under the minimum reserve system, the central bank:', ['May issue any amount of currency while holding a prescribed minimum of gold and foreign assets', 'Must back every note fully with gold', 'Cannot issue currency without Parliament\'s approval for each note', 'Issues currency only against government deficits'], 0, "Under the minimum reserve system, the central bank can issue currency to any extent as long as it keeps a prescribed minimum reserve of gold and foreign assets. 'Must back every note fully with gold' is the trap — full backing was a feature of the old gold standard. In practice: RBI follows this system, keeping a statutory minimum of gold and foreign securities and issuing currency according to the economy's needs.", 'c3', 'moderate', topic='The Sources of Money Supply'),
            M('m6', 'A CBDC is:', ['Legal tender issued by a central bank in digital form', 'A private crypto-currency', 'A bank deposit', 'A government bond'], 0, "A Central Bank Digital Currency is legal tender issued by the central bank in digital form; it is a direct liability of the central bank. 'A private crypto-currency' is the trap: crypto-currencies are issued privately with no central-bank backing. A bank deposit is a liability of the commercial bank. In practice: India's Digital Rupee (e₹), launched by RBI in pilots from 2022, can be used for retail and wholesale payments.", 'c3', topic='The Sources of Money Supply'),
            M('m7', 'In India, crypto-currencies are:', ['Not legally recognised as currency and not counted as money', 'Legal tender', 'Part of M1', 'Part of reserve money'], 0, "In India, crypto-currencies are not legal tender and are not counted in any money-supply measure; they face legal uncertainty, although gains from them are taxed. 'Legal tender' is the trap — only RBI-issued currency (including e₹) and government coins are legal tender. In practice: CAs compute 30% tax on gains from virtual digital assets under section 115BBH and check 1% TDS, while reminding clients these assets are not money.", 'c3', topic='The Sources of Money Supply'),
            M('m8', 'M1 consists of:', ['Currency with the public + demand deposits with banks + other deposits with the RBI', 'M1 + time deposits', 'Currency with the public only', 'Currency + post office savings deposits'], 0, "Narrow money M1 adds up three items: currency held by the public, banks' demand deposits, and 'other' deposits held with the RBI. 'M1 + time deposits' is the trap — that is M3, broad money. Currency alone omits demand deposits, which are spendable by cheque or transfer. In practice: economists watch M1 as an indicator of transaction money available in the economy.", 'c4', topic='Measurement of Money Supply'),
            M('m9', 'M3 equals:', ['M1 + time deposits with the banking system', 'M2 + time deposits', 'M1 + post office savings deposits', 'M3 + post office deposits'], 0, "M3 (broad money) = M1 + time deposits with the banking system; it is built on M1, not M2. 'M2 + time deposits' is the trap — M2 adds post office savings deposits, which are not part of M3. In practice: M3 is the most watched money aggregate in India; RBI reports its growth fortnightly, and analysts compare it with credit growth.", 'c4', topic='Measurement of Money Supply'),
            M('m10', 'M2 equals:', ['M1 + savings deposits with post office savings banks', 'M1 + time deposits with banks', 'M3 + total post office deposits', 'Currency + bank reserves'], 0, "M2 = M1 + savings deposits with post office savings banks. 'M1 + time deposits with banks' is the trap — that is M3. M4 adds total post office deposits to M3. In practice: post office savings form a significant part of household savings in rural India, which is why the RBI's older measures M2 and M4 include them.", 'c4', topic='Measurement of Money Supply'),
            M('m11', 'Which measure is called broad money?', ['M3', 'M1', 'M2', 'Reserve money'], 0, 'M3 is called broad money because it adds time deposits to the narrow M1, capturing money held as savings as well as for transactions; it is the measure used most widely. M1 is the trap — it is narrow money. Reserve money is the monetary base issued by the RBI. In practice: RBI and market analysts quote year-on-year M3 growth when assessing liquidity conditions and comparing it with bank credit growth.', 'c4', topic='Measurement of Money Supply'),
            M('m12', 'The RBI began publishing four measures of money supply (M1 to M4) from:', ['April 1977', 'July 1935', '1967-68', 'August 2016'], 0, "On the advice of its Second Working Group on Money Supply, the RBI began publishing four measures, M1 to M4, from April 1977. July 1935 is the trap — it falls in the RBI's very first year (the RBI began operating on 1 April 1935). August 2016 relates to the monetary policy framework. In practice: these measures, later supplemented by new aggregates, remain the base for money-supply analysis in India.", 'c4', 'moderate', topic='Measurement of Money Supply'),
            M('m13', 'Currency with the public 3,20,000; demand deposits 2,80,000; other deposits with RBI 6,000; time deposits 14,50,000 (₹ crore). M3 is:', ['₹20,56,000 crore', '₹6,06,000 crore', '₹20,50,000 crore', '₹17,70,000 crore'], 0, 'M1 = currency with public + demand deposits + other deposits with RBI = 3,20,000 + 2,80,000 + 6,000 = 6,06,000. M3 = M1 + time deposits = 6,06,000 + 14,50,000 = ₹20,56,000 crore. Traps: ₹6,06,000 crore stops at M1; ₹20,50,000 crore omits other deposits with RBI; ₹17,70,000 crore counts only currency and time deposits. In practice: RBI compiles M3 in this way.', 'c4', 'hard', '320000+280000+6000+1450000', topic='Measurement of Money Supply'),
            M('m14', 'Notes in circulation 33,40,000; rupee coins 31,200; small coins 750; cash with banks 1,18,000 (₹ crore). Currency with the public is:', ['₹32,53,950 crore', '₹34,89,950 crore', '₹33,71,950 crore', '₹32,22,000 crore'], 0, "Currency with the public = notes in circulation + rupee coins + small coins − cash held by banks = 33,40,000 + 31,200 + 750 − 1,18,000 = 33,71,950 − 1,18,000 = ₹32,53,950 crore. Traps: ₹33,71,950 crore forgets to subtract bank cash; ₹34,89,950 crore adds it; ₹32,22,000 crore omits coins. In practice: RBI's weekly statistical supplement reports currency with the public on exactly this basis.", 'c4', 'moderate', '3340000+31200+750-118000', topic='Measurement of Money Supply'),
            M('m15', 'If R = 10% and there is no currency drain or excess reserves, the money multiplier is:', ['10', '0.1', '1', '100'], 0, "With no currency drain and no excess reserves, the money multiplier = 1 ÷ reserve ratio = 1 ÷ 0.10 = 10. The tempting 0.1 is the reserve ratio itself; 100 treats 10% as 0.01. In practice: in reality, RBI's cash reserve ratio is low, but currency holding and excess reserves make India's actual multiplier much smaller than 1 ÷ CRR.", 'c5', 'core', '1/0.1', topic='The Concept of Money Multiplier'),
            M('m16', 'A ₹100 crore open market purchase finally raises money supply by ₹400 crore. The money multiplier is:', ['4', '0.25', '400', '5'], 0, 'Money multiplier = change in money supply ÷ change in high-powered money = 400 ÷ 100 = 4. The tempting 0.25 inverts the ratio (100 ÷ 400); 400 is the change in money supply itself. In practice: when RBI injects liquidity through open market purchases, analysts estimate the final effect on broad money by applying the observed multiplier.', 'c5', 'core', '400/100', topic='The Concept of Money Multiplier'),
            M('m17', 'The money-multiplier approach identifying H, r and c as proximate determinants was given by:', ['Milton Friedman and Anna Schwartz', 'Baumol and Tobin', 'Keynes', 'Irving Fisher'], 0, 'Milton Friedman and Anna Schwartz, in A Monetary History of the United States (1963), identified three proximate determinants — high-powered money H, the reserve–deposit ratio r and the currency–deposit ratio c — as the drivers of money supply. Baumol and Tobin are the trap — they worked on money demand. In practice: RBI economists use this framework to explain why broad money grows at a different rate from reserve money.', 'c6', topic='The Money Multiplier Approach to Supply of Money'),
            M('m18', 'The currency–deposit ratio reflects the behaviour of:', ['The public', 'Commercial banks', 'The central bank', 'The government'], 0, "The currency–deposit ratio (c = currency ÷ deposits) depends on how much cash the public chooses to hold relative to bank deposits, so it reflects public behaviour and banking habits. Commercial banks are the trap: they decide the excess reserve ratio, not the currency ratio. In practice: India's currency–deposit ratio jumped after demonetisation and during Covid, when people wanted to hold more cash.", 'c6', topic='The Money Multiplier Approach to Supply of Money'),
            M('m19', 'The money multiplier is NEGATIVELY related to:', ['The currency ratio, the reserve ratio and the excess reserve ratio', 'High-powered money', 'The time-deposit to demand-deposit ratio', 'Bank lending'], 0, 'The multiplier m = (1 + c) ÷ (r + e + c). A higher currency ratio, required reserve ratio or excess reserve ratio means more money leaks out of the deposit-creation process, so the multiplier falls — a negative relationship. High-powered money is the trap: it affects the level of money supply, not the multiplier. In practice: when RBI raises the CRR, the multiplier and broad money growth both slow.', 'c6', 'moderate', topic='The Money Multiplier Approach to Supply of Money'),
            M('m20', 'With r = 0.08, e = 0.02 and c = 0.30, the money multiplier m = (1 + c)/(r + e + c) is:', ['3.25', '12.5', '2.5', '4.33'], 0, 'm = (1 + c) ÷ (r + e + c) = (1 + 0.30) ÷ (0.08 + 0.02 + 0.30) = 1.30 ÷ 0.40 = 3.25. Traps: 12.5 is the simple multiplier 1 ÷ r; 4.33 leaves r and e out of the denominator (1.30 ÷ 0.30); 2.5 is 1 ÷ 0.40, forgetting the numerator. In practice: RBI analysts compute actual multipliers from c, r and e data, which are far below 1 ÷ CRR.', 'c6', 'hard', 'round((1+0.3)/(0.08+0.02+0.3),2)', topic='The Money Multiplier Approach to Supply of Money'),
            M('m21', 'Excess reserves of banks tend to FALL when:', ['Market interest rates rise', 'Banks expect larger deposit withdrawals', 'Interest rates fall', 'A financial crisis begins'], 0, 'Excess reserves earn little, so when market interest rates rise, holding them becomes costlier and banks lend them out — excess reserves fall. Rising expected deposit withdrawals and a financial crisis are traps: they make banks hold more reserves for safety. In practice: when call money rates rise in India, banks reduce surplus balances parked with RBI and lend more in the interbank market.', 'c6', 'moderate', topic='The Money Multiplier Approach to Supply of Money'),
            M('m22', 'Total reserves are ₹800 billion and required reserves ₹650 billion. Excess reserves are:', ['₹150 billion', '₹1,450 billion', '₹650 billion', '₹800 billion'], 0, "Excess reserves = total reserves − required reserves = 800 − 650 = ₹150 billion. The tempting ₹1,450 billion adds the two instead of subtracting; ₹650 billion and ₹800 billion are simply the given figures. In practice: banks track excess reserves daily, and RBI's liquidity operations aim to keep surplus or deficit liquidity within a target range.", 'c6', 'core', '800-650', topic='The Money Multiplier Approach to Supply of Money'),
            M('m23', 'If the required reserve ratio is 12.5%, the credit multiplier is:', ['8', '12.5', '0.125', '80'], 0, "Credit multiplier = 1 ÷ required reserve ratio = 1 ÷ 0.125 = 8, so each rupee of reserves can support up to ₹8 of deposits. The tempting 12.5 is the reserve ratio in percentage form; 0.125 is the ratio itself; 80 is a decimal slip. In practice: this shows why the CRR is a powerful tool; even small changes alter banks' lending capacity substantially.", 'c7', 'core', '1/0.125', topic='The Concept of Money Multiplier'),
            M('m24', 'A fresh deposit of ₹2,00,000 with a 20% reserve ratio can support total deposits of:', ['₹10,00,000', '₹40,000', '₹2,40,000', '₹8,00,000'], 0, 'Total deposits = initial deposit × 1 ÷ reserve ratio = 2,00,000 ÷ 0.20 = ₹10,00,000. The tempting ₹8,00,000 is only the new credit created, excluding the initial deposit; ₹40,000 is the reserve required on the first deposit; ₹2,40,000 simply adds 20%. In practice: this is the textbook ceiling; actual expansion is smaller because of cash withdrawals and excess reserves.', 'c7', 'moderate', '200000/0.2', topic='The Concept of Money Multiplier'),
            M('m25', 'The money multiplier is usually smaller than the credit multiplier because:', ['Banks hold excess reserves and borrowers convert part of loans into cash', 'The RBI prints too much money', 'Deposits earn interest', 'Government spending is high'], 0, "The credit multiplier (1 ÷ required reserve ratio) assumes no leakages. The money multiplier is smaller because banks keep some excess reserves and borrowers withdraw part of their loans as cash, both reducing deposit creation. 'The RBI prints too much money' is the trap — printing changes base money, not the multiplier. In practice: India's high cash usage historically kept its money multiplier low.", 'c7', 'moderate', topic='The Concept of Money Multiplier'),
            M('m26', 'An open market SALE of securities by the RBI will:', ['Reduce bank reserves and money supply', 'Increase bank reserves and money supply', 'Leave money supply unchanged', 'Increase currency with the public'], 0, "In an open market sale, banks and others buy securities from the RBI and pay from their reserve balances, so bank reserves fall, lending capacity shrinks and money supply falls. 'Increase bank reserves and money supply' is the trap — that is the effect of an open market purchase. In practice: RBI conducts OMO sales to absorb surplus liquidity when it wants to tighten conditions.", 'c8', topic='Monetary Policy and Money Supply'),
            M('m27', 'The money multiplier could be close to zero when:', ['Interest rates are very low and banks hold new reserves as excess reserves', 'Banks lend out all reserves', 'CRR is cut', 'The public holds no currency'], 0, "If interest rates are very low and banks fear risk, they may hold new reserves idle as excess reserves instead of lending; then little or no new deposit money is created, and the multiplier approaches zero. 'Banks lend out all reserves' is the trap — that would maximise the multiplier. In practice: after the 2008 crisis, banks globally sat on huge excess reserves, so central-bank injections did not raise money supply proportionately.", 'c8', 'hard', topic='Monetary Policy and Money Supply'),
            M('m28', 'When the government spends money borrowed from the RBI under WMA/overdraft:', ['Banks\' reserves with the RBI rise and money supply can expand', 'Money supply falls', 'Bank reserves fall', 'There is no effect on money supply'], 0, "When the government spends funds borrowed from RBI through Ways and Means Advances or overdraft, its account at RBI is debited and recipients' bank accounts are credited, so banks' reserves with RBI rise and money supply can expand. 'Money supply falls' is the trap. In practice: RBI watches government cash balances closely because such spending adds liquidity to the banking system.", 'c8', 'moderate', topic='Effect of Government Expenditure on Money Supply'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'table',
             'q': 'From the data (₹ crore) compute M1, M2, M3 and M4: currency with the public 2,40,000; demand deposits with banks 4,10,000; other deposits with RBI 9,000; post office savings bank deposits 35,000; time deposits with banks 18,20,000; total post office deposits (excluding NSC) 1,20,000.',
             'model': [table(['Measure', '₹ crore'], [['M1 = 2,40,000 + 4,10,000 + 9,000', q1m1], ['M2 = M1 + 35,000', q1m2], ['M3 = M1 + 18,20,000', q1m3], ['M4 = M3 + 1,20,000', q1m4]])],
             'scheme': [{'id': 's1', 'pt': 'M1', 'm': 1.5, 'skill': 'computation'}, {'id': 's2', 'pt': 'M2 built on M1', 'm': 1, 'skill': 'concept'}, {'id': 's3', 'pt': 'M3 built on M1', 'm': 1.5, 'skill': 'computation'}, {'id': 's4', 'pt': 'M4 built on M3', 'm': 1, 'skill': 'computation'}],
             'remarks': ['The classic error is building M3 on M2.'], 'mistakes': ['Adding post office deposits to M3.', 'Leaving out other deposits with the RBI.'], 'tips': ['Write each definition before the numbers.'], 'checks': q1},
            {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'text',
             'q': 'Required reserve ratio 10%; currency ₹500 billion; demand deposits ₹1,000 billion; excess reserves ₹5 billion. Find (a) c and e, (b) money supply, (c) the money multiplier, (d) the multiplier if the reserve ratio rises to 15%, (e) the simple deposit multiplier. Comment.',
             'model': [p(f'(a) c = 500/1,000 = {q2c}; e = 5/1,000 = 0.005 (i.e. {q2e}% of deposits). (b) M = C + D = ₹{inr(q2ms)} billion.'),
                       p(f'(c) m = (1 + 0.5) ÷ (0.10 + 0.005 + 0.5) = 1.5 ÷ 0.605 = {q2m}. (d) At 15%: 1.5 ÷ 0.655 = {q2mm}.'),
                       p(f'(e) Simple multiplier = 1/0.1 = {q2s}. The actual multiplier is far smaller because half of people\'s money is held as currency, which is not multiplied; a higher reserve ratio lowers it further.')],
             'scheme': [{'id': 's1', 'pt': 'c and e', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'Money supply', 'm': 1, 'skill': 'computation'}, {'id': 's3', 'pt': 'Multiplier formula and value', 'm': 1.5, 'skill': 'computation'}, {'id': 's4', 'pt': 'Multiplier at 15%', 'm': 1, 'skill': 'computation'}, {'id': 's5', 'pt': 'Simple multiplier and comment', 'm': 1.5, 'skill': 'analysis'}],
             'remarks': ['Show the formula with symbols first.'], 'mistakes': ['Omitting e from the denominator.', 'Using 1/r as the money multiplier.'], 'tips': ['Two-decimal answers are adequate.'], 'checks': q2},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'The required reserve ratio is 12.5%. (a) Find the credit multiplier. (b) What total deposits can a fresh deposit of ₹5,00,000 support, and how much new credit is created? (c) If the RBI buys securities worth ₹2,000 crore from banks, what is the maximum rise in money supply? State the assumptions.',
             'model': [p(f'(a) 1/0.125 = {q3a}. (b) Total deposits = 5,00,000 × 8 = ₹{inr(q3b)}; new credit = ₹{inr(q3c)}. (c) ΔM = 2,000 × 8 = ₹{inr(q3d)} crore.'),
                       p('Assumptions: banks keep no excess reserves, the public holds no extra currency, and there is enough demand for loans.')],
             'scheme': [{'id': 's1', 'pt': 'Multiplier', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'Total deposits and new credit', 'm': 2, 'skill': 'computation'}, {'id': 's3', 'pt': 'OMO effect', 'm': 1, 'skill': 'application'}, {'id': 's4', 'pt': 'Assumptions', 'm': 1, 'skill': 'concept'}],
             'remarks': ['Distinguish total deposits from new credit.'], 'mistakes': ['Treating an OMO purchase as reducing money supply.'], 'tips': ['List the assumptions — they explain why reality differs.'], 'checks': q3},
        ],
        'revision': {
            'summary': ['Money supply = money held by the public (excludes government and banking system).',
                        'Measured to understand money growth and to guide monetary policy.',
                        'Sources: central bank (high-powered money, fiat, minimum reserve system) and banks (credit money). CBDC (e₹) is legal tender; crypto is not money in India.',
                        'M1 = C + DD + other deposits with RBI; M2 = M1 + PO savings deposits; M3 = M1 + time deposits (broad money); M4 = M3 + total PO deposits (excl. NSC). Four measures since April 1977.',
                        'Money multiplier m = M/H = (1 + c)/(r + e + c); simple 1/r. Friedman–Schwartz: H (central bank), r (banks/central bank), c (public).',
                        'Credit multiplier = 1/required reserve ratio; larger than the actual money multiplier because of excess reserves and cash drain.',
                        'OMO purchase raises reserves and money supply; sale reduces them. Government spending from WMA/OD adds bank reserves.'],
            'remember': ['Currency with public = notes + rupee coins + small coins − cash with banks.', 'Excess reserves = total reserves − required reserves.', 'Money creation ≠ wealth creation.'],
            'traps': ['M3 is built on M1, not M2.', 'Higher c, r or e → LOWER multiplier.', 'Cash held by banks is not currency with the public.'],
        },
        'quickref': [
            {'k': 'M1', 'v': 'Currency with public + demand deposits with banks + other deposits with RBI'},
            {'k': 'M2 / M3 / M4', 'v': 'M1 + PO savings deposits / M1 + bank time deposits / M3 + total PO deposits (excl. NSC)'},
            {'k': 'Money multiplier', 'v': 'm = (1 + c) ÷ (r + e + c); M = m × H'},
            {'k': 'Credit multiplier', 'v': '1 ÷ required reserve ratio; total deposits = initial deposit × 1/r'},
            {'k': 'Monetary base (H)', 'v': 'Currency + bank reserves (reserve money)'},
            {'k': 'OMO', 'v': 'Purchase → ↑reserves → ↑M; Sale → ↓reserves → ↓M'},
        ],
        'viva': [
            V('v1', 'Define M1, M2, M3 and M4.',
              'M1 is currency with the public plus demand deposits with banks plus other deposits with the RBI. M2 is M1 plus savings deposits with post office savings banks. M3 is M1 plus time deposits with banks, and it is called broad money. M4 is M3 plus total post office deposits excluding National Savings Certificates.',
              [P('p1', 'M1 = currency with public + demand deposits + other deposits with RBI', 3, 'm1', 'currency', 'demand deposit', 'other deposit|rbi', min=3),
               P('p2', 'M2 = M1 + post office savings bank deposits', 2, ALT('m2 {x}', 'm2 is {x}', 'm2 equal {x}', x=('m1 plus post office', 'm1 post office', 'm1 and post office', 'm1 plus saving deposit with post office', 'm1 plus saving deposit of post office', 'm1 plus post office saving'))),
               P('p3', 'M3 = M1 + time deposits with banks', 3, ALT('m3 {x}', 'm3 is {x}', 'm3 equal {x}', x=('m1 plus time deposit', 'm1 time deposit', 'm1 and time deposit', 'm1 plus fixed deposit', 'm1 plus term deposit'))),
               P('p4', 'M4 = M3 + total post office deposits', 2, ALT('m4 {x}', 'm4 is {x}', 'm4 equal {x}', x=('m3 plus post office', 'm3 post office', 'm3 and post office', 'm3 plus total post office', 'm3 plus all post office')))], 'c4'),
            V('v2', 'Who determines the money supply according to the money multiplier approach?',
              'According to Friedman and Schwartz, money supply is jointly determined by the central bank, which controls high-powered money; the commercial banks, through the reserve ratio and excess reserves they keep; and the public, through the currency–deposit ratio, that is how much cash people hold compared with deposits.',
              [P('p1', 'Central bank — high-powered money', 4, 'central bank|rbi|reserve bank', 'high powered|monetary base|base money|reserve money|h', min=2),
               P('p2', 'Commercial banks — reserve / excess reserve ratio', 3, 'bank', 'reserve ratio|excess reserve|reserves', min=2),
               P('p3', 'Public — currency–deposit ratio', 3, 'public|people|household', 'currency deposit|currency ratio|cash|currency', min=2)], 'c6'),
            V('v3', 'What is the money multiplier, and how do the currency ratio and the reserve ratio affect it?',
              'The money multiplier is the ratio of money supply to high-powered money, so it shows how much money supply rises for each rupee of monetary base; it equals one plus c divided by r plus e plus c. A higher currency ratio lowers the multiplier because cash is not multiplied, and a higher reserve ratio also lowers it because banks can lend less.',
              [P('p1', 'Ratio of money supply to high-powered money (formula)', 4, 'money supply|money stock|stock of money|m', 'high powered|monetary base|base money|reserve money', min=2),
               P('p2', 'Higher currency ratio → lower multiplier', 3, ALT('{a} {b} {d}', '{a} {d}', '{a} {b} multiplier {d}', '{d} multiplier', a=('higher currency', 'more currency', 'more cash', 'higher cash', 'currency ratio rise', 'currency ratio increas', 'increase in currency', 'rise in currency', 'currency ratio'), b=('ratio', 'deposit ratio'), d=('lower', 'lowers', 'reduce', 'reduces', 'decrease', 'decreases', 'smaller', 'fall', 'falls', 'inverse', 'inversely', 'negative'))),
               P('p3', 'Higher reserve ratio → lower multiplier', 3, ALT('{a} {d}', '{a} also {d}', '{a} multiplier {d}', a=('higher reserve ratio', 'reserve ratio rise', 'reserve ratio increas', 'increase in reserve ratio', 'rise in reserve ratio', 'higher reserve', 'more reserve', 'reserve ratio'), d=('lower', 'lowers', 'reduce', 'reduces', 'decrease', 'decreases', 'smaller', 'fall', 'falls', 'inverse', 'inversely', 'negative')))], 'c5'),
            V('v4', 'What is the credit multiplier and why is it larger than the actual money multiplier?',
              'The credit multiplier is one divided by the required reserve ratio; it shows how many times the banking system can expand an initial deposit through repeated lending under fractional reserve banking. The actual money multiplier is smaller because banks keep excess reserves above the minimum and borrowers hold part of their loans as cash.',
              [P('p1', 'Credit multiplier = 1 ÷ required reserve ratio', 4, 'reciprocal|one divided|1 divided|1 by|one by|one over|1 over|inverse', 'reserve ratio|reserve requirement|crr|reserve', min=2),
               P('p2', 'Excess reserves held by banks', 3, 'excess reserve|more than required|above the minimum|above minimum|extra reserve|more reserve', min=1),
               P('p3', 'Borrowers convert part of loans into cash (currency drain)', 3, 'cash|currency', 'borrower|public|people|withdraw|hold|drain|leak', min=2)], 'c7'),
            V('v5', 'How does government expenditure financed by Ways and Means Advances affect money supply?',
              'When the government\'s cash falls short it borrows from the RBI through Ways and Means Advances or overdraft. When it spends, its account with the RBI is debited and the recipients\' accounts in commercial banks are credited, so banks\' reserves with the RBI rise. These excess reserves can increase money supply through the multiplier process.',
              [P('p1', 'Government borrows from RBI (WMA / overdraft)', 3, 'ways and means|wma|overdraft|borrow from rbi|borrow from the reserve bank', min=1),
               P('p2', 'Spending credits recipients\' bank accounts — bank reserves rise', 4, 'reserve|balance with rbi|bank balanc', 'rise|raise|increas|more|higher|creat|add', min=2),
               P('p3', 'Money supply expands via multiplier', 3, 'money supply', 'increas|rise|expand|grow|multipl', min=2)], 'c8'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Liquidity in a cash-loving economy', 'difficulty': 'hard',
            'case': ('In an economy the public holds currency equal to 40% of deposits, the required reserve ratio is 10% and banks initially hold no excess reserves. High-powered money is ₹20,000 crore. '
                     'During a crisis banks start holding excess reserves equal to 10% of deposits. The government is also campaigning for digital payments.'),
            'mcqs': [
                M('k1a', 'What is the money multiplier before the crisis?', ['2.8', '10', '3.5', '2.33'], 0, 'm = (1 + c) ÷ (r + c) with c = 0.4 and r = 0.1: (1 + 0.4) ÷ (0.1 + 0.4) = 1.4 ÷ 0.5 = 2.8. Traps: 10 is the simple 1 ÷ r, ignoring currency drain; 2.33 is the post-crisis multiplier with excess reserves; 3.5 leaves r out (1.4 ÷ 0.4). In practice: high cash preference sharply lowers the multiplier, as seen in India.', 'c6', 'moderate', 'round((1+0.4)/(0.1+0.4),2)', topic='The Money Multiplier Approach to Supply of Money'),
                M('k1b', 'What is the money supply before the crisis?', ['₹56,000 crore', '₹2,00,000 crore', '₹28,000 crore', '₹46,600 crore'], 0, 'Money supply = money multiplier × high-powered money = 2.8 × 20,000 = ₹56,000 crore. Traps: ₹2,00,000 crore uses 1 ÷ r = 10; ₹28,000 crore multiplies by 1.4 only; ₹46,600 crore uses the post-crisis multiplier of 2.33. In practice: RBI economists estimate how money supply will respond to changes in reserve money in this way.', 'c6', 'moderate', '2.8*20000', topic='The Money Multiplier Approach to Supply of Money'),
                M('k1c', 'After banks start holding 10% excess reserves, the multiplier becomes:', ['2.33', '2.8', '3.5', '1.4'], 0, 'With excess reserves e = 0.1: m = (1 + 0.4) ÷ (0.1 + 0.1 + 0.4) = 1.4 ÷ 0.6 ≈ 2.33. The tempting 2.8 is the pre-crisis multiplier, ignoring the new excess reserves; 3.5 ignores both reserve ratios; 1.4 is only the numerator. In practice: when banks turn cautious in a crisis, money supply falls even without any change in central-bank policy.', 'c6', 'hard', 'round((1+0.4)/(0.1+0.1+0.4),2)', topic='The Money Multiplier Approach to Supply of Money'),
                M('k1d', 'If the digital-payments campaign lowers the currency ratio, the money multiplier will:', ['Rise', 'Fall', 'Stay the same', 'Become zero'], 0, "A lower currency ratio means less cash leaks out of the banking system and more stays as deposits that banks can lend, so the money multiplier rises. 'Fall' is the trap, which reverses the effect. In practice: the spread of UPI and digital payments in India is expected to lower the currency–deposit ratio over time, strengthening the transmission of RBI's policy actions through bank credit.", 'c6', 'core', topic='The Money Multiplier Approach to Supply of Money'),
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
    'q1': {'s1': _CR(659000), 's2': _CR(694000), 's3': _CR(2479000), 's4': _CR(2599000)},
    'q2': {
        's1': _N(0.5, 0.005),
        's2': _N(1500),
        's3': _N(2.48, kw=['0.605|1.5 0.605|1 c r e c|c 1 c r e']),
        's4': _N(2.29),
        's5': _K('simple 10|1 0.1 10|10 times|multiplier 10|deposit multiplier 10|0.1 10', 'currency|cash|leak|smaller|less|lower'),
    },
    'q3': {
        'extra_ok': True,
        's1': _K('1 0.125 8|multiplier 8|8 times|k 8|0.125 8|multiplier is 8'),
        's2': _N(4000000, 3500000),
        's3': _CR(16000),
        's4': _K('excess reserve|no excess|reserves', 'currency|cash drain|public hold|leak|cash', 'demand for loans|loan demand|borrower|demand for credit|credit demand', min=2),
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
