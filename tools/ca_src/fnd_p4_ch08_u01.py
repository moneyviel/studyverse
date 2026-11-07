"""CA Foundation · Paper 4 Business Economics · Chapter 8 Money Market · Unit 1 The Concept of Money Demand: Important Theories.
Original explanations, numbers and questions."""
from lib import *
from ca_viva import P, ALT, V

UID = 'fnd-p4-ch08-u01'


def M(i, q, o, a, e, c=None, d='core', check=None, topic=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if topic: m['topic'] = topic
    if c: m['concept'] = c
    if check: m['check'] = check
    return m


def build():
    c1 = Checks()
    p1 = c1.add('5000*6/10000', 'price level')
    p2 = c1.add('10000*6/10000', 'price level when M doubles')
    p3 = c1.add('(4000*5+6000*3)/19000', 'price level with credit money')

    c2 = Checks()
    md = c2.add('0.25*4*12000', 'Cambridge money demand')
    vel = c2.add('1/0.25', 'velocity = 1/k')
    md2 = c2.add('0.2*4*12000', 'money demand when k falls to 0.2')

    c3 = Checks()
    b8 = c3.add('80/0.08', 'bond price at 8%')
    b10 = c3.add('80/0.10', 'bond price at 10%')
    b5 = c3.add('80/0.05', 'bond price at 5%')
    loss = c3.add('1000-800', 'capital loss if rate rises to 10%')

    c4 = Checks()
    C1 = c4.add('(2*50*360000/0.04)**0.5', 'optimal withdrawal at 4%')
    n1 = c4.add('360000/30000', 'number of withdrawals at 4%')
    a1 = c4.add('30000/2', 'average cash at 4%')
    C2 = c4.add('(2*50*360000/0.09)**0.5', 'optimal withdrawal at 9%')
    a2 = c4.add('20000/2', 'average cash at 9%')
    C3 = c4.add('(2*200*360000/0.04)**0.5', 'withdrawal when broker fee is 200')

    c5 = Checks()
    lt = c5.add('0.2*50000', 'transactions + precautionary demand')
    tot = c5.add('10000+6000', 'total money demand at 6%')

    q1 = Checks()
    q1p = q1.add('(6000*4+9000*2)/21000', 'P')
    q1n = q1.add('(6000*1.2*4+9000*1.2*2)/21000', 'P after 20% rise in M and M\'')
    q1c = q1.add('round((2.4-2)/2*100,2)', '% rise in P')

    q2 = Checks()
    q2md = q2.add('(1/5)*2.5*40000', 'Md')
    q2k = q2.add('1/5', 'k')
    q2y = q2.add('25000/(0.25*2.5)', 'nominal-income check')

    q3 = Checks()
    q3c = q3.add('(2*20*490000/0.05)**0.5', 'C at 5%')
    q3n = q3.add('490000/19798.99', 'withdrawals')
    q3a = q3.add('round(19798.99/2,2)', 'average holding')
    q3c2 = q3.add('(2*20*490000/0.08)**0.5', 'C at 8%')

    k = Checks()
    k1 = k.add('60/0.06', 'consol price at 6%')
    k2 = k.add('60/0.04', 'consol price at 4%')
    k3 = k.add('1500-1000', 'capital gain')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch08', 'n': 1,
        'title': 'The Concept of Money Demand: Important Theories',
        'outcomes': [
            'State the functions and desirable characteristics of money, explain fiat money and how broad money is measured.',
            'Explain what the demand for money is and its determinants — income, prices, interest rate and financial innovation.',
            'Explain and compare the classical theories (Fisher\'s MV = PT and the Cambridge Md = kPY) and Keynes\'s liquidity preference theory with its three motives and the liquidity trap.',
            'Explain the post-Keynesian theories — Baumol–Tobin inventory approach (square-root rule), Friedman\'s restatement and Tobin\'s portfolio approach — and solve simple numericals on them.',
        ],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 60, 'practice': 55}, 'prereq': [],
                 'exam_tip': 'MCQs test who said what: Fisher — transactions, MV = PT; Cambridge (Marshall, Pigou) — cash balances, k; Keynes — three motives, speculative demand inversely related to interest; Baumol–Tobin — interest affects even transactions demand; Friedman — permanent income; Tobin — risk aversion and diversification.'},
        'concepts': [
            {'id': 'c1', 'title': 'Introduction — money, its functions and characteristics',
             'body': ['Money is anything that serves as (1) a store of value — saved and used later, smoothing purchases over time; (2) a unit of account — a common measure of prices; and (3) a medium of exchange — accepted in buying and selling.',
                      'Without money we would have barter: a tailor wanting rice must find a rice farmer who wants a shirt (the double-coincidence problem). Money lets people specialise, which raises output, transactions and the need for money.',
                      'Cowry shells, barley, pepper, gold and silver have all served as money. Paper receipts for deposited gold later became money themselves; when the link to metal was broken, fiat money was born — worthless as material but valuable because society agrees to accept it.',
                      'Desirable qualities: generally acceptable, durable, easy to recognise, hard to counterfeit, relatively scarce but with elastic supply, portable, uniform and divisible without loss of value.',
                      'Measuring money: official statistics use broad money — assets that store value and are liquid (can be turned into cash quickly at nearly full value). All countries include currency and transferable deposits (narrow money); broad money may add other deposits (savings and term deposits, repos) and securities other than shares (tradable certificates of deposit, commercial paper).'],
             'analogy': 'Money is the common language of trade — without it every deal needs a translator (a perfect barter partner).',
             'work': 'Treasury managers decide every day how much to keep as cash (liquidity) versus deposits or liquid funds — the practical side of money as a store of value.'},
            {'id': 'c2', 'title': 'The demand for money and its determinants',
             'body': ['Demand for money is the desire to hold wealth as money rather than as bonds or other assets. It is a derived demand — wanted for its purchasing power — so it is a demand for real balances. It is really a demand for liquidity and a store of value. People hold it despite little or no return because it is the most convenient way to transact.',
                      'Money demand helps determine interest rates, prices and income; the central bank needs to understand it to set targets.',
                      'Determinants: income (higher income, more spending, more money held); price level (money demand is directly proportional to prices); interest rate (the opportunity cost of holding money — higher rates, less money held); real GDP; and financial innovation (internet banking, UPI apps, ATMs reduce the need to hold cash). Firms hold money for the same basic reasons.'],
             'analogy': 'Holding cash is like keeping water in a bucket instead of pumping it into a field: convenient to use right away, but it grows nothing (no interest).',
             'work': 'Cash-management policies in companies (minimum cash balance, sweep accounts) apply exactly these determinants — higher interest rates push treasurers to hold less idle cash.'},
            {'id': 'c3', 'title': 'Classical approach — Fisher\'s quantity theory (MV = PT)',
             'body': ['The quantity theory of money (Irving Fisher, Yale, "The Purchasing Power of Money", 1911) holds that changes in the stock of money are what chiefly drive the price level (and so the value of money).',
                      'Equation of exchange (transactions approach): MV = PT, where M = average money in circulation, V = transactions velocity (average number of times a unit of money is spent), P = average price level (P = MV/T), T = total transactions. Later writers replaced T with real output Y.',
                      'Extended form with bank deposits: MV + M\'V\' = PT, where M\' = credit (deposit) money and V\' its velocity.',
                      'Assumptions: V and V\' are constant; T depends on national income and is fixed in the short run because full employment prevails. So the price level moves in proportion to the money supply.',
                      'PT represents the demand for money (value of transactions) and MV + M\'V\' its supply; more desired transactions mean more demand for money.'],
             'blocks': [table(['Symbol', 'Meaning'], [['M', 'Money in circulation'], ['V', 'Velocity of circulation of money'], ['M\'', 'Credit (bank deposit) money'], ['V\'', 'Velocity of credit money'], ['P', 'Average price level'], ['T', 'Volume of transactions']], title='MV + M\'V\' = PT')],
             'analogy': 'If the same number of goods are on sale and everyone spends money at the same speed, doubling everyone\'s cash simply doubles the price tags.',
             'work': 'When money supply grows much faster than real output, analysts expect inflation — a modern echo of Fisher\'s equation.'},
            {'id': 'c4', 'title': 'The Cambridge cash-balance approach (Md = kPY)',
             'body': ['At Cambridge, Marshall, Pigou, Robertson and the young Keynes asked a different question: why do people hold money at all? Money gives utility by (1) letting a sale and a later purchase be split in time — the transactions motive — and (2) acting as a hedge against uncertainty — a temporary abode of purchasing power, which adds a precautionary motive. So money is also demanded for itself.',
                      'Demand depends partly on income (more income, more purchases, more money needed) and partly on wealth and interest rates.',
                      'Md = kPY, where Md = demand for money balances, Y = real national income, P = price level, PY = nominal income and k = the fraction of nominal income people wish to hold as cash (the "Cambridge k"), reflecting the economic structure and monetary habits.',
                      'Thus the neoclassical version turned the quantity theory into a theory of money demand, as a function of money income. Like Fisher\'s, it is mainly a model of transactions demand. Note: k is the reciprocal of income velocity (k = 1/V).'],
             'analogy': 'Fisher asks "how fast does money run around?"; Cambridge asks "how much money do people like to keep sitting in their pockets?"',
             'work': 'A company\'s cash-to-sales ratio is a business version of the Cambridge k — finance teams benchmark it against peers.'},
            {'id': 'c5', 'title': 'Keynes\'s liquidity preference theory — three motives',
             'body': ['Liquidity preference (Keynes, "The General Theory", 1936) is people\'s desire to hold money rather than securities. People hold cash for three motives.',
                      'Transactions motive: income and spending are not synchronised, so cash is needed for current personal (income motive) and business (business/trade motive) exchanges. It depends on income, not on interest: Lt = kY, where k is the fraction of income kept for transactions. Aggregate transactions demand is a function of national income.',
                      'Precautionary motive: cash for unforeseen needs — illness, accidents, emergencies. It depends on income, economic and political conditions and personal traits (optimism, foresight). Like transactions balances, it is income-elastic and not very sensitive to interest.',
                      'Speculative motive: cash held to take advantage of changes in interest rates (bond prices). Bond prices and interest rates move inversely. Each investor has a "normal" or critical rate. If the current rate is above it, he expects rates to fall and bond prices to rise, so he holds bonds (high interest plus expected capital gain). If the current rate is below it, he expects rates to rise and bond prices to fall, so he holds cash (little interest lost, capital loss avoided, bonds can be bought cheaper later). At the critical rate he is indifferent.',
                      'An individual\'s choice is all-bonds or all-cash (a discontinuous demand curve), but adding up many investors with different critical rates gives a smooth downward-sloping aggregate speculative demand: the higher the interest rate, the lower the speculative demand for money.'],
             'blocks': [table(['Motive', 'Depends on', 'Interest sensitive?'], [['Transactions', 'Income (Lt = kY)', 'No (in Keynes)'], ['Precautionary', 'Income, conditions, personality', 'Not much'], ['Speculative', 'Interest rate vs critical rate', 'Yes — inverse']], title='Keynes\'s three motives')],
             'analogy': 'A shopper keeps cash for groceries (transactions), an emergency note in the wallet (precautionary), and extra cash while waiting for the big sale (speculative — waiting for bonds to become cheap).',
             'work': 'Debt-fund managers act like Keynes\'s speculators: when they expect rates to rise they shorten duration or sit in cash to avoid capital losses on bonds.'},
            {'id': 'c6', 'title': 'The liquidity trap',
             'body': ['A liquidity trap is a situation where an increase in money supply fails to lower interest rates or raise income — monetary policy becomes powerless.',
                      'At a very low (near zero) short-term interest rate, nobody wants bonds: money pays the same zero return and is usable for transactions, and bond prices can only fall. The public holds whatever money is supplied, often out of fear of deflation or war. Speculative demand becomes perfectly elastic — the curve is horizontal (parallel to the X-axis).',
                      'Open market purchases then only add to idle hoards; excess funds are not invested. Japan\'s experience — money printed by the central bank hoarded in expectation of further deflation, with the 10-year bond yield falling to about 0.2% — is the standard real-world example.'],
             'analogy': 'Pouring water into a bucket with no bottom: the central bank keeps adding money, but it vanishes into idle cash instead of flowing into spending.',
             'work': 'When interest rates are near zero, CFOs see that cheaper money no longer boosts demand for their products — the reason governments then lean on fiscal policy.'},
            {'id': 'c7', 'title': 'Post-Keynesian: Baumol–Tobin inventory approach',
             'body': ['Post-Keynesian theories stress money\'s store-of-value or asset role. Baumol (1952) and Tobin (1956) treated cash held for transactions as an inventory to be managed.',
                      'Two stores of value: money (no interest) and an interest-earning asset (savings deposits, bonds). Moving between them has a fixed cost (brokerage). Holding money costs the interest forgone (opportunity cost); converting often costs brokerage. People choose the cash balance that minimises total cost.',
                      'Square-root rule: the cost-minimising size of each cash withdrawal C = √(2bY/r), where b = brokerage per transaction, Y = income (total spending in the period) and r = interest rate. Average cash held = C/2.',
                      'Key results: transactions demand for money depends on the interest rate (inversely) — unlike Keynes; a higher brokerage fee raises money demand and lowers average bond holding; money demand rises less than proportionately with income.'],
             'analogy': 'Like a shopkeeper deciding how often to restock: frequent small trips to the bank cost fees; big withdrawals mean cash lying idle and losing interest.',
             'work': 'Corporate cash-concentration and sweep decisions use the same trade-off between transaction costs and interest forgone.'},
            {'id': 'c8', 'title': 'Friedman\'s restatement of the quantity theory',
             'body': ['Milton Friedman (1956) treated money as one asset among many, so its demand follows the general theory of demand for capital assets. Two factors: permanent income (his measure of wealth — the present expected value of all future income), and relative returns on assets (including risk).',
                      'Money is like a durable good yielding services; demand depends on many factors. Nominal demand for money: rises with total wealth (permanent income divided by the discount rate — the average return on five asset classes: human capital, physical capital, equity, bonds and money); moves in the same direction as the price level; rises when the opportunity cost of money (returns on bonds and shares) falls; and is reduced by higher inflation, which erodes the real value of money balances and raises the cost of holding money.',
                      'Unlike Keynes, Friedman uses permanent income rather than current income.'],
             'analogy': 'Friedman sees money as one fruit in a fruit basket of assets — how much of it you keep depends on how big your whole basket is (wealth) and how tasty the other fruits are (their returns).',
             'work': 'Wealth managers rebalance clients\' cash allocation when returns on equity and bonds change — a Friedman-style portfolio decision.'},
            {'id': 'c9', 'title': 'Tobin\'s portfolio approach — demand for money as behaviour toward risk',
             'body': ['James Tobin assumed people prefer more wealth to less and are risk-averse: for a given return they prefer less risk.',
                      'An investor chooses the share of wealth in money (safe, no return) and in bonds or shares (return, but risk of capital loss). All-risky portfolios give high average return but high risk; all-cash portfolios give zero risk and zero return. Risk-averse people therefore diversify, each choosing his own risk–return mix.',
                      'Tobin\'s liquidity preference function: as the return on bonds rises, people hold more bonds and less money — the asset demand for money slopes downward against the interest rate.'],
             'analogy': 'Not putting all your eggs in one basket: some eggs in the safe basket (cash), some in the riskier but rewarding basket (bonds).',
             'work': 'Asset-allocation advice — "keep some liquid funds, some debt, some equity" — is Tobin\'s diversification in practice.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Fisher\'s equation of exchange', 'difficulty': 'moderate', 'minutes': 6,
             'q': '(a) M = ₹5,000 crore, V = 6, T = 10,000 crore units. Find P. (b) What happens to P if M doubles, other things constant? (c) With M = ₹4,000 crore, V = 5, credit money M\' = ₹6,000 crore, V\' = 3 and T = 19,000 crore units, find P.',
             'solution': [p(f'(a) P = MV ÷ T = 5,000 × 6 ÷ 10,000 = {p1}.'),
                          p(f'(b) P = 10,000 × 6 ÷ 10,000 = {p2} — the price level doubles: P varies in direct proportion to M when V and T are constant.'),
                          p(f'(c) P = (MV + M\'V\') ÷ T = (20,000 + 18,000) ÷ 19,000 = {p3}.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Cambridge k and velocity', 'difficulty': 'core', 'minutes': 5,
             'q': 'Real income Y = 12,000 crore units, price level P = 4, and people wish to hold one-fourth of nominal income as cash. Find the demand for money and the implied income velocity. What happens if people now hold only 20%?',
             'solution': [p(f'Md = kPY = 0.25 × 4 × 12,000 = ₹{inr(md)} crore. Velocity V = 1/k = {vel}.'),
                          p(f'If k = 0.2: Md = 0.2 × 4 × 12,000 = ₹{inr(md2)} crore — a smaller k means money changes hands faster (V = 5).')],
             'checks': c2},
            {'id': 'i3', 'title': 'Why speculators hold cash when rates are low', 'difficulty': 'moderate', 'minutes': 6,
             'q': 'A perpetual bond pays ₹80 a year. Find its market price when the market interest rate is 8%, 10% and 5%. Explain the speculative motive.',
             'solution': [table(['Market rate', 'Price = 80 ÷ r (₹)'], [['8%', b8], ['10%', b10], ['5%', b5]]),
                          p(f'Bond prices move inversely with interest rates. Someone who buys at 8% (₹{inr(b8)}) loses ₹{loss} if rates rise to 10%. If rates are already low (below the critical rate), people expect them to rise and prices to fall, so they hold cash; if rates are high, they expect a fall and buy bonds for the capital gain. Hence speculative demand for money is inversely related to the interest rate.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Baumol\'s square-root rule', 'difficulty': 'hard', 'minutes': 8,
             'q': 'A person spends ₹3,60,000 evenly during a year, keeps the rest in a deposit earning 4% and pays ₹50 per withdrawal. Find the optimal withdrawal size, number of withdrawals and average cash held. Repeat for an interest rate of 9%, and for a fee of ₹200 at 4%.',
             'solution': [p(f'C = √(2bY/r) = √(2 × 50 × 3,60,000 ÷ 0.04) = ₹{inr(C1)}. Withdrawals = 3,60,000 ÷ {inr(C1)} = {n1}. Average cash = C/2 = ₹{inr(a1)}.'),
                          p(f'At 9%: C = √(2 × 50 × 3,60,000 ÷ 0.09) = ₹{inr(C2)}; average cash = ₹{inr(a2)} — higher interest, less money held.'),
                          p(f'With a ₹200 fee at 4%: C = ₹{inr(C3)} — a higher brokerage fee raises money holding.')],
             'checks': c4},
            {'id': 'i5', 'title': 'Total demand for money in the Keynesian scheme', 'difficulty': 'core', 'minutes': 4,
             'q': 'National income is ₹50,000 crore and people hold 20% of income for transactions and precautionary purposes. At an interest rate of 6% speculative demand is ₹6,000 crore. Find total demand for money.',
             'solution': [p(f'Transactions + precautionary = 0.2 × 50,000 = ₹{inr(lt)} crore (depends on income). Total = {inr(lt)} + 6,000 = ₹{inr(tot)} crore. If the rate rose, only the speculative part would fall.')],
             'checks': c5},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Setting a minimum cash balance', 'role': 'CA in a company treasury',
             'situation': 'The company pays ₹20 lakh of expenses every week and earns interest on surplus funds in a liquid fund.',
             'steps': ['Identify transactions needs (payroll, suppliers) and a precautionary buffer for surprises.', 'Weigh interest forgone on idle cash against the cost and time of frequent redemptions (Baumol\'s trade-off).', 'Reduce idle cash when interest rates rise; keep more when transaction costs are high.'],
             'takeaway': 'Money-demand theory is the logic behind every treasury cash policy.',
             'think': 'Why might the optimal cash balance fall when interest rates rise?', 'answer': 'The opportunity cost of holding non-interest-bearing cash rises, so it pays to keep more in interest-earning assets and withdraw more often.'},
            {'id': 'j2', 'title': 'Advising on debt funds in a rate cycle', 'role': 'CA advising a family office',
             'situation': 'Interest rates are at a cyclical low and expected to rise.',
             'steps': ['Explain the inverse relation between bond prices and yields.', 'Suggest keeping money in short-duration or cash-like instruments until rates rise (speculative motive).', 'Plan to move into longer bonds after rates rise to lock in yields and possible capital gains.'],
             'takeaway': 'Keynes\'s speculative motive is the everyday logic of duration management.'},
            {'id': 'j3', 'title': 'Reading money growth', 'role': 'CA in an equity research team',
             'situation': 'Broad money growth jumps well above real GDP growth.',
             'steps': ['Use the quantity-theory intuition: if velocity is stable, faster money growth points to inflation.', 'Check velocity trends — digital payments may be changing it.', 'Adjust inflation and interest-rate assumptions in valuation models.'],
             'takeaway': 'MV = PT is a quick sanity check on inflation forecasts.'},
        ],
        'mcqs': [
            M('m1', 'Which is NOT a function of money?', ['Guarantee of real returns', 'Medium of exchange', 'Unit of account', 'Store of value'], 0, "Money's functions are to act as a medium of exchange, to measure value as a unit of account, to store value over time, and to settle deferred payments. It does not guarantee real returns — cash earns nothing, and inflation erodes its purchasing power. 'Store of value' is the tempting trap, but storing value is a genuine function, even if imperfect. In practice: financial planners in India warn clients that idle savings-account money loses real value when inflation exceeds the interest rate.", 'c1', topic='Introduction'),
            M('m2', 'Fiat money has value because:', ['Society collectively agrees to accept it', 'It contains gold of equal value', 'It earns interest', 'It is always backed 100% by foreign exchange'], 0, "Fiat money, such as rupee notes, has little intrinsic value; it is accepted because the government declares it legal tender and society collectively agrees to accept it in payment. 'It contains gold of equal value' is the trap — that describes commodity money; modern rupees are not convertible into gold. In practice: the 2016 demonetisation showed that notes lose value immediately once their legal-tender status is withdrawn.", 'c1', topic='Introduction'),
            M('m3', 'Liquidity of an asset means:', ['How easily it can be converted into cash at close to full value', 'Its rate of return', 'Its durability', 'Its risk of default'], 0, "Liquidity measures how quickly and cheaply an asset can be converted into cash at close to its full value. Cash is perfectly liquid; land and jewellery are far less liquid. 'Its rate of return' is the trap: liquid assets usually earn lower returns, so liquidity and return are different properties. In practice: CAs analysing a company's balance sheet compute current and quick ratios to judge how liquid its assets are.", 'c1', topic='Introduction'),
            M('m4', 'The demand for money is a demand for:', ['Real balances (purchasing power)', 'Paper as a commodity', 'Gold', 'Interest income'], 0, "People want money not for the paper itself but for what it can buy, so what they really demand is real money balances, that is, purchasing power. When prices double, people need twice the nominal money for the same real purchases. 'Interest income' is the trap: money held as cash typically earns little or no interest. In practice: households raise cash holdings during festive seasons because they plan more real purchases.", 'c2', topic='The Demand for Money'),
            M('m5', 'The opportunity cost of holding money is:', ['The interest that could be earned on other assets', 'The price level', 'The cost of printing notes', 'Zero'], 0, "Holding money means giving up the interest you could earn by holding bonds or deposits instead, so that forgone interest is the opportunity cost. When interest rates rise, holding money becomes costlier and money demand falls. 'Zero' is the trap: money has no explicit cost, but the forgone return is a real cost. In practice: corporate treasurers park surplus cash in liquid funds or fixed deposits rather than current accounts to avoid this cost.", 'c2', topic='The Demand for Money'),
            M('m6', 'Financial innovations such as UPI and internet banking tend to:', ['Reduce the demand for money', 'Increase the demand for cash', 'Have no effect on money demand', 'Raise the interest rate directly'], 0, "UPI, internet banking and cards make payments and transfers between deposits and other assets quick and cheap, so people need to hold less money for transactions — money demand falls. 'Increase the demand for cash' is the trap; digital payments reduce the need for cash. In practice: with UPI widely used in India, many shopkeepers and households now keep far less cash on hand than they did a decade ago.", 'c2', topic='The Demand for Money'),
            M('m7', 'Fisher\'s quantity theory was set out in:', ['The Purchasing Power of Money (1911)', 'The General Theory (1936)', 'The Wealth of Nations (1776)', 'A Monetary History of the US (1963)'], 0, "Irving Fisher, a Yale economist, set out the transactions version of the quantity theory, MV = PT, in The Purchasing Power of Money (1911). The General Theory (1936) is the trap — that is Keynes's work, which challenged the classical view. A Monetary History of the US (1963) is by Friedman and Schwartz. In practice: the quantity theory's core idea, that excess money growth raises prices, still informs central-bank thinking on inflation.", 'c3', topic='The Demand for Money'),
            M('m8', 'In MV = PT, V stands for:', ['Transactions velocity of circulation of money', 'Volume of output', 'Value of money', 'Velocity of credit money only'], 0, "In Fisher's equation MV = PT, V is the transactions velocity of circulation — the average number of times a unit of money changes hands in buying goods and services during the period. 'Volume of output' is the trap: transactions are captured by T, not V. In practice: economists estimate velocity by dividing nominal GDP by the money stock to see whether money is circulating faster or slower over time.", 'c3', topic='The Demand for Money'),
            M('m9', 'If M = ₹5,000 crore, V = 6 and T = 10,000 crore units, the price level P is:', ['3', '12', '0.33', '8.33'], 0, 'From MV = PT, P = MV ÷ T = (5,000 × 6) ÷ 10,000 = 30,000 ÷ 10,000 = 3. The tempting 12 inverts the money term, computing VT ÷ M; 0.33 is T ÷ MV, the reciprocal of the correct answer. In practice: this equation is the simplest way to show students why rapid growth in money supply, with output unchanged, pushes up the price level.', 'c3', 'moderate', '5000*6/10000', topic='The Demand for Money'),
            M('m10', 'Using MV + M\'V\' = PT with M = 4,000, V = 5, M\' = 6,000, V\' = 3 and T = 19,000, P equals:', ['2', '1.05', '2.6', '1.58'], 0, "Including bank (credit) money: P = (MV + M'V') ÷ T = (4,000 × 5 + 6,000 × 3) ÷ 19,000 = (20,000 + 18,000) ÷ 19,000 = 2. The tempting 1.05 ignores credit money (20,000 ÷ 19,000); 1.58 uses V' for all money; 2.6 uses V for all money. In practice: because bank deposits dominate India's money supply, ignoring credit money badly understates spending power.", 'c3', 'hard', '(4000*5+6000*3)/19000', topic='The Demand for Money'),
            M('m11', 'Fisher assumes that in the short run:', ['V and T are constant, so P varies with M', 'P is constant and T varies with M', 'M is constant', 'V varies inversely with P'], 0, "Fisher treated velocity V as constant in the short run, set by payment habits, and transactions T as fixed at full employment, so the price level P varies directly and proportionately with M. 'P is constant and T varies with M' is the trap — that is closer to a Keynesian view with idle resources. In practice: this proportionality is behind the warning that printing money to fund deficits raises inflation.", 'c3', 'moderate', topic='The Demand for Money'),
            M('m12', 'The Cambridge equation for the demand for money is:', ['Md = kPY', 'MV = PT', 'C = √(2bY/r)', 'Lt = kY only'], 0, "The Cambridge cash-balance equation is Md = kPY: people hold a fraction k of their nominal income (PY) as money. MV = PT is the trap — that is Fisher's transactions version. C = √(2bY/r) is the Baumol square-root rule. In practice: if households and firms decide to hold a larger fraction of income in cash, as during uncertain times, the Cambridge k rises and spending slows.", 'c4', topic='The Demand for Money'),
            M('m13', 'Which economist is NOT associated with the Cambridge cash-balance approach?', ['Irving Fisher', 'Alfred Marshall', 'A. C. Pigou', 'D. H. Robertson'], 0, 'The cash-balance approach came from Cambridge: Marshall, Pigou, Robertson and Keynes all worked on it. Irving Fisher worked at Yale and gave the transactions version, MV = PT, so he is the exception. Pigou is a tempting distractor because of his links to welfare economics, but he was a Cambridge cash-balance theorist. In practice: knowing who belongs to which school helps students answer matching questions quickly.', 'c4', topic='The Demand for Money'),
            M('m14', 'With k = 0.25, P = 4 and Y = 12,000, the demand for money is:', ['12,000', '48,000', '3,000', '1,92,000'], 0, 'Md = kPY = 0.25 × 4 × 12,000 = 0.25 × 48,000 = 12,000. The tempting 48,000 is nominal income PY, forgetting to multiply by k; 3,000 is k × Y, ignoring the price level; 1,92,000 multiplies by P twice and drops k. In practice: if prices rise while k and real income stay the same, people need proportionately more money for transactions.', 'c4', 'moderate', '0.25*4*12000', topic='The Demand for Money'),
            M('m15', 'If people hold one-fifth of nominal income as money, income velocity of money is:', ['5', '0.2', '20', '2'], 0, 'Income velocity is the reciprocal of the Cambridge k: if k = 1/5 = 0.2, then V = 1 ÷ 0.2 = 5, meaning each rupee finances five rupees of income in a year. The tempting 0.2 is k itself, not velocity; 20 confuses 1/5 with 5%. In practice: analysts compare nominal GDP with the money stock to see whether velocity is falling, which can indicate people holding more money relative to income.', 'c4', 'moderate', '1/0.2', topic='The Demand for Money'),
            M('m16', 'According to Keynes, the transactions demand for money depends mainly on:', ['The level of income', 'The interest rate', 'Expected bond prices', 'The critical rate of interest'], 0, "Keynes held that the transactions demand for money (Lt = kY) depends mainly on the level of income, because higher incomes mean more spending to finance between paydays; he treated it as largely insensitive to the interest rate. 'The interest rate' is the trap — that drives the speculative demand. In practice: when salaries rise, households keep larger balances in savings accounts for routine expenses such as EMIs and groceries.", 'c5', topic='The Demand for Money'),
            M('m17', 'Speculative demand for money is:', ['Inversely related to the rate of interest', 'Directly related to the rate of interest', 'Independent of the interest rate', 'Directly related to income only'], 0, "When interest rates are high, people expect them to fall and bond prices to rise, so they buy bonds and hold less money; when rates are low, they expect rates to rise and hold money. So speculative demand is inversely related to the interest rate. 'Directly related' is the trap. In practice: in India, when G-sec yields are high, debt fund managers increase long-bond holdings expecting capital gains when yields fall.", 'c5', topic='The Demand for Money'),
            M('m18', 'If the current interest rate is above an investor\'s critical rate, Keynes predicts he will:', ['Hold bonds, expecting interest rates to fall and bond prices to rise', 'Hold all wealth in cash', 'Be indifferent', 'Sell bonds to avoid capital loss'], 0, "If the current rate is above the investor's critical rate, he expects rates to fall; falling rates mean rising bond prices, so he holds bonds to gain. 'Sell bonds to avoid capital loss' is the trap — that is the behaviour when the current rate is below the critical rate and rates are expected to rise. In practice: bond traders who expect RBI rate cuts buy long-duration G-secs to lock in capital gains.", 'c5', 'moderate', topic='The Demand for Money'),
            M('m19', 'A perpetual bond pays ₹80 a year. If the market interest rate rises from 8% to 10%, its price:', ['Falls from ₹1,000 to ₹800', 'Rises from ₹1,000 to ₹1,250', 'Stays at ₹1,000', 'Falls from ₹1,000 to ₹980'], 0, "A perpetual bond's price = annual coupon ÷ market interest rate. At 8%: 80 ÷ 0.08 = ₹1,000; at 10%: 80 ÷ 0.10 = ₹800. So the price falls to ₹800. 'Rises to ₹1,250' is the trap — that is the price if rates fell to 6.4%; bond prices and interest rates move inversely. In practice: debt mutual fund NAVs fall when market yields rise, which is why advisors warn investors about interest-rate risk.", 'c5', 'hard', topic='The Demand for Money'),
            M('m20', 'In a liquidity trap, the speculative demand for money curve is:', ['Perfectly elastic (horizontal)', 'Perfectly inelastic (vertical)', 'Upward sloping', 'Unit elastic'], 0, "In a liquidity trap, interest rates are so low that everyone expects them to rise, so people are willing to hold any extra money at that rate — the speculative demand curve becomes perfectly elastic, a horizontal line. 'Perfectly inelastic (vertical)' is the trap: that would mean money demand does not respond to the interest rate at all. In practice: Japan in the 1990s is the classic example cited by economists.", 'c6', topic='The Demand for Money'),
            M('m21', 'In a liquidity trap, an increase in money supply through open market purchases:', ['Fails to lower interest rates or raise income', 'Sharply lowers interest rates', 'Causes immediate hyperinflation', 'Raises bond yields'], 0, "In a liquidity trap, extra money from open market purchases is simply held as idle balances; interest rates cannot fall further, so investment and income do not rise — monetary policy becomes ineffective. 'Sharply lowers interest rates' is the trap: rates are already at their floor. In practice: during the 2008 crisis and its aftermath, central banks near zero rates turned to fiscal support and unconventional tools because ordinary rate cuts stopped working.", 'c6', topic='The Demand for Money'),
            M('m22', 'The inventory-theoretic approach to transactions demand was developed by:', ['Baumol and Tobin', 'Marshall and Pigou', 'Fisher and Friedman', 'Keynes and Robertson'], 0, 'William Baumol (1952) and James Tobin (1956) developed the inventory-theoretic approach, treating transactions money like an inventory to be managed by balancing interest forgone against brokerage costs. Marshall and Pigou are the trap — they belong to the Cambridge cash-balance school. In practice: corporate treasury teams use similar logic when deciding how often to sweep surplus cash into liquid funds.', 'c7', topic='Post-Keynesian Developments in the Theory of Demand for Money'),
            M('m23', 'Baumol\'s rule: spending Y = ₹3,60,000, brokerage b = ₹50, interest r = 4%. The optimal size of each withdrawal is:', ['₹30,000', '₹15,000', '₹9,00,000', '₹42,426'], 0, "Baumol's square-root rule: C = √(2bY ÷ r) = √(2 × 50 × 3,60,000 ÷ 0.04) = √90,00,00,000 = ₹30,000. The tempting ₹15,000 is the average cash balance held (C ÷ 2), not the withdrawal size. In practice: a business deciding how often to transfer money from a fixed deposit to its current account faces the same trade-off between transaction costs and interest forgone.", 'c7', 'hard', '(2*50*360000/0.04)**0.5', topic='Post-Keynesian Developments in the Theory of Demand for Money'),
            M('m24', 'According to Baumol–Tobin, an increase in the brokerage fee will:', ['Increase the transactions demand for money', 'Reduce the transactions demand for money', 'Leave money demand unchanged', 'Make money demand independent of income'], 0, "In the Baumol–Tobin model, a higher brokerage fee makes each switch between bonds and cash costlier, so people make fewer, larger withdrawals and hold more cash on average — transactions demand rises. 'Reduce the transactions demand' is the trap, which reverses the effect. In practice: when banks charge for frequent fund transfers or ATM use, customers withdraw larger amounts less often.", 'c7', 'moderate', topic='Post-Keynesian Developments in the Theory of Demand for Money'),
            M('m25', 'A key difference between Keynes and Baumol–Tobin is that Baumol–Tobin hold that:', ['Even transactions demand for money depends on the interest rate', 'Money demand depends only on income', 'There is no speculative motive', 'Velocity is constant'], 0, "Keynes treated transactions demand as depending only on income. Baumol and Tobin showed that even transactions balances respond to the interest rate: higher rates make holding cash costlier, so people hold less. 'Money demand depends only on income' is the trap — that is closer to Keynes's view. In practice: when deposit rates rise, firms trim idle current-account balances and invest surplus cash.", 'c7', 'moderate', topic='Post-Keynesian Developments in the Theory of Demand for Money'),
            M('m26', 'In Friedman\'s restatement, the demand for money depends on:', ['Permanent income and relative returns on assets', 'Current income only', 'The critical rate of interest only', 'The brokerage fee'], 0, "Friedman's restatement says demand for money depends on permanent income (his measure of wealth) and on the returns on money relative to other assets such as bonds, equities and physical goods. 'Current income only' is the trap — Friedman deliberately used permanent income because it is more stable than current income. In practice: households' cash and deposit holdings change little with a one-time bonus but rise steadily with lasting salary growth.", 'c8', topic='Post-Keynesian Developments in the Theory of Demand for Money'),
            M('m27', 'Which is NOT among Friedman\'s five asset classes?', ['Foreign exchange reserves', 'Money', 'Bonds', 'Human capital'], 0, "Friedman's five forms of wealth are money, bonds, equity, physical goods (non-human capital) and human capital. Foreign exchange reserves are not among them; they are held by the central bank, not households. Human capital is the tempting distractor because it seems unusual, but it is part of Friedman's framework. In practice: financial advisors today similarly consider a client's earning ability as well as their financial assets.", 'c8', 'hard', topic='Post-Keynesian Developments in the Theory of Demand for Money'),
            M('m28', 'According to Friedman, a higher expected inflation rate will:', ['Reduce the demand for money', 'Increase the demand for money', 'Not affect money demand', 'Raise permanent income'], 0, "In Friedman's framework, higher expected inflation means money will lose purchasing power faster, raising the cost of holding money relative to physical goods, so money demand falls. 'Increase the demand for money' is the trap. In practice: during high inflation, Indian households shift savings into gold and real estate rather than holding cash.", 'c8', 'moderate', topic='Post-Keynesian Developments in the Theory of Demand for Money'),
            M('m29', 'Tobin\'s portfolio approach explains money demand through:', ['Risk aversion and diversification between money and risky assets', 'Transactions costs only', 'Constant velocity', 'Permanent income'], 0, "Tobin's portfolio approach treats money as a riskless asset and bonds as risky ones. Risk-averse investors hold a mix, keeping some money to reduce overall portfolio risk — so money demand arises from risk aversion and diversification. 'Permanent income' is the trap — that is Friedman's approach. In practice: financial planners recommend keeping part of a portfolio in safe, liquid assets to balance risk.", 'c9', topic='Post-Keynesian Developments in the Theory of Demand for Money'),
            M('m30', 'In Tobin\'s analysis, a rise in the interest rate on bonds leads people to:', ['Hold more bonds and less money', 'Hold more money and fewer bonds', 'Hold only money', 'Hold only bonds in every case'], 0, "In Tobin's analysis, a higher return on bonds makes risky assets more attractive, so investors shift towards bonds and hold less money — the asset demand for money slopes downward. 'Hold more money and fewer bonds' is the trap, which reverses the response. In practice: when bank FD and bond rates rise in India, investors move money out of savings accounts into these higher-yielding instruments.", 'c9', topic='Post-Keynesian Developments in the Theory of Demand for Money'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'In an economy M = ₹6,000 crore, V = 4, M\' = ₹9,000 crore, V\' = 2 and T = 21,000 crore units. (a) Find the price level. (b) If both M and M\' rise by 20% with V, V\' and T unchanged, find the new price level and the % change. (c) State the assumption that makes the change proportional.',
             'model': [p(f'(a) P = (6,000×4 + 9,000×2) ÷ 21,000 = 42,000 ÷ 21,000 = {q1p}.'), p(f'(b) New P = (7,200×4 + 10,800×2) ÷ 21,000 = {q1n}; rise = {q1c}%.'), p('(c) V and V\' are constant and T is fixed (full employment), so P moves in proportion to the money supply.')],
             'scheme': [{'id': 's1', 'pt': 'Formula MV + M\'V\' = PT and P', 'm': 2, 'skill': 'computation'}, {'id': 's2', 'pt': 'New P and % change', 'm': 2, 'skill': 'computation'}, {'id': 's3', 'pt': 'Assumption stated', 'm': 1, 'skill': 'concept'}],
             'remarks': ['Good answers noticed the % change in P equals the % change in money.'], 'mistakes': ['Ignoring credit money.', 'Adding M + M\' and multiplying by V only.'], 'tips': ['Write the formula first.'], 'checks': q1},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'Income velocity of money is 5, the price level 2.5 and real income 40,000 units. (a) Find Cambridge k and the demand for money. (b) Show that the same answer comes from MV = PY. (c) If financial innovation reduces k, what happens to money demand at the same income?',
             'model': [p(f'(a) k = 1/V = {q2k}; Md = kPY = 0.2 × 2.5 × 40,000 = {inr(q2md)}.'), p('(b) M = PY ÷ V = 1,00,000 ÷ 5 = 20,000 — the same.'), p('(c) A smaller k means people hold a smaller share of income as money, so money demand falls (velocity rises).')],
             'scheme': [{'id': 's1', 'pt': 'k as reciprocal of V', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Md computed', 'm': 2, 'skill': 'computation'}, {'id': 's3', 'pt': 'Equivalence shown', 'm': 1, 'skill': 'analysis'}, {'id': 's4', 'pt': 'Effect of lower k', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Linking k and V shows real understanding.'], 'mistakes': ['Using real income instead of nominal income.'], 'tips': ['Nominal income = P × Y.'], 'checks': q2},
            {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'text',
             'q': 'An individual spends ₹4,90,000 evenly over a year, pays ₹20 per withdrawal and can earn 5% on funds not withdrawn. Using Baumol\'s square-root rule, find (a) the optimal withdrawal, (b) the number of withdrawals, (c) the average cash balance. (d) Find the optimal withdrawal at 8% and state the relationship shown.',
             'model': [p(f'(a) C = √(2 × 20 × 4,90,000 ÷ 0.05) = ₹{inr(q3c)} (approx.).'), p(f'(b) Number = 4,90,000 ÷ {inr(q3c)} ≈ {q3n}.'), p(f'(c) Average cash = C/2 = ₹{inr(q3a)}.'), p(f'(d) At 8%: C = ₹{inr(q3c2)}. Higher interest → smaller withdrawals and lower average cash — transactions demand for money is inversely related to the interest rate.')],
             'scheme': [{'id': 's1', 'pt': 'Formula and C', 'm': 2, 'skill': 'computation'}, {'id': 's2', 'pt': 'Number of withdrawals', 'm': 1, 'skill': 'computation'}, {'id': 's3', 'pt': 'Average balance', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'Recomputed at 8% with conclusion', 'm': 2, 'skill': 'analysis'}],
             'remarks': ['Round sensibly; examiners accept answers to the nearest rupee.'], 'mistakes': ['Forgetting the square root.', 'Treating C as the average balance.'], 'tips': ['Average holding is half of each withdrawal.'], 'checks': q3},
        ],
        'revision': {
            'summary': ['Money: medium of exchange, unit of account, store of value; fiat money; broad money and liquidity.',
                        'Money demand = demand for real balances; rises with income and prices; falls with interest rate and financial innovation.',
                        'Fisher (1911): MV = PT; MV + M\'V\' = PT; V, V\' constant, T fixed → P ∝ M.',
                        'Cambridge (Marshall, Pigou, Robertson, Keynes): Md = kPY; k = 1/V; transactions + precautionary.',
                        'Keynes (1936): transactions (Lt = kY), precautionary (income), speculative (inverse to interest; critical rate; bond prices inverse to rates). Liquidity trap: horizontal speculative demand; monetary policy powerless (Japan).',
                        'Baumol–Tobin: C = √(2bY/r); transactions demand depends on r (inverse) and brokerage (direct).',
                        'Friedman (1956): permanent income + relative returns; five assets; inflation reduces money demand.',
                        'Tobin: risk aversion → diversified portfolio → downward-sloping asset demand for money.'],
            'remember': ['Bond price = annual coupon ÷ market rate (perpetual bond).', 'Average cash in Baumol = C/2.'],
            'traps': ['Keynes: transactions demand NOT interest-sensitive; Baumol–Tobin: it IS.', 'Cambridge k is a fraction of NOMINAL income.', 'Friedman uses permanent, not current, income.'],
        },
        'quickref': [
            {'k': 'Fisher', 'v': 'MV = PT; MV + M\'V\' = PT; P = (MV + M\'V\')/T'},
            {'k': 'Cambridge', 'v': 'Md = kPY; k = 1/V'},
            {'k': 'Keynes', 'v': 'L = L1(Y) + L2(r): transactions & precautionary depend on Y; speculative inverse to r'},
            {'k': 'Baumol square-root rule', 'v': 'C = √(2bY/r); average cash = C/2; withdrawals = Y/C'},
            {'k': 'Friedman', 'v': 'Md = f(permanent income, returns on money, bonds, equity, physical & human capital, inflation, P)'},
            {'k': 'Liquidity trap', 'v': 'Near-zero rate; speculative demand perfectly elastic; monetary policy ineffective'},
        ],
        'viva': [
            V('v1', 'What are the functions of money?',
              'Money works as a medium of exchange, so goods can be bought and sold without barter. It is a unit of account, a common measure in which prices are expressed. And it is a store of value, so purchasing power can be saved and used later.',
              [P('p1', 'Medium of exchange', 4, 'medium of exchange|means of exchange|means of payment|buy and sell|exchange', min=1),
               P('p2', 'Unit of account / measure of value', 3, 'unit of account|measure of value|common measure|unit of value|express price|price', min=1),
               P('p3', 'Store of value', 3, 'store of value|store value|save|saving|later|future', min=1)], 'c1'),
            V('v2', 'How does the Cambridge approach differ from Fisher\'s quantity theory?',
              'Fisher\'s version, MV equals PT, looks at the flow of money spent on transactions and the velocity of circulation. The Cambridge cash-balance approach, Md equals kPY, looks at how much money people want to hold as cash balances, a fraction k of nominal income, and adds the precautionary motive as a hedge against uncertainty.',
              [P('p1', 'Fisher: MV = PT, transactions / velocity (flow)', 5, ALT('fisher {x}', 'fisher equation {x}', 'fisher version {x}', 'fisher stresses {x}', x=['mv', 'transaction', 'velocit', 'flow'])),
               P('p2', 'Cambridge: Md = kPY, cash balances held (fraction k of income)', 5, 'cambridge|cash balanc|marshall|pigou', 'kpy|k py|fraction|proportion|hold|cash balanc|k of', min=2)], 'c4'),
            V('v3', 'Explain Keynes\'s three motives for holding money.',
              'Keynes said people hold money for the transactions motive, to meet day to day payments, which depends on income. The precautionary motive is to meet unforeseen emergencies, which also depends on income. The speculative motive is to take advantage of expected changes in interest rates and bond prices, and it is inversely related to the rate of interest.',
              [P('p1', 'Transactions motive — day-to-day payments, depends on income', 3, 'transaction', 'income|day to day|daily|payment|expens|purchas', min=2),
               P('p2', 'Precautionary motive — emergencies', 3, 'precaution', 'emergenc|unforeseen|unexpected|contingenc|uncertain|rainy', min=2),
               P('p3', 'Speculative motive — inversely related to interest rate', 4, 'speculat', ALT('{v} {r}', '{v} to {r}', '{v} with {r}', '{v} relat {r}', '{v} related to {r}', r=('interest', 'rate of interest', 'interest rate'), v=('inverse', 'inversely', 'negatively', 'opposite')), 'bond price|bond|capital gain|expect', min=2)], 'c5'),
            V('v4', 'What is a liquidity trap?',
              'A liquidity trap is a situation where the interest rate is so low, near zero, that people are willing to hold any amount of money instead of bonds. The speculative demand for money becomes perfectly elastic, so an increase in money supply does not lower interest rates or raise income, and monetary policy becomes ineffective. Japan is the usual example.',
              [P('p1', 'Very low / near-zero interest rate; people hold any amount of money', 4, 'low|zero|minimum|bottom', 'interest|rate', 'hold|hoard|any amount|whatever', min=2),
               P('p2', 'Speculative demand perfectly elastic', 2, 'perfectly elastic|infinitely elastic|horizontal|flat', min=1),
               P('p3', 'More money does not lower rates or raise income — monetary policy ineffective', 4, 'ineffective|powerless|useless|no effect|not effective|does not work|fails|cannot|not lower|not reduce|not increase|not stimulat', min=1)], 'c6'),
            V('v5', 'State Baumol\'s square-root rule and what it implies about the demand for money.',
              'Baumol said the cost-minimising cash withdrawal is the square root of two times the brokerage fee times income divided by the interest rate. It implies that even the transactions demand for money depends on the interest rate inversely, and a higher brokerage fee raises the demand for money.',
              [P('p1', 'C = √(2bY/r) — square root of 2 × brokerage × income ÷ interest', 4, 'square root|root', '2by|two|2 b y|2 times|twice', 'brokerage|broker|fee|transaction cost', 'interest', min=3),
               P('p2', 'Transactions demand depends inversely on interest rate', 4, 'transaction', ALT('interest sensitive', 'interest elastic', 'falls as interest rises', 'falling as interest rises', '{v} {r}', '{v} to {r}', '{v} on {r}', '{v} related to {r}', 'depend on {r}', 'depends on {r}', 'affected by {r}', r=('interest', 'interest rate', 'rate of interest'), v=('inverse', 'inversely', 'negatively'))),
               P('p3', 'Higher brokerage fee raises money demand', 2, ALT('{b} {u}', 'higher {b}', 'increase in {b}', '{b} increas', b=('brokerage', 'broker fee', 'fee', 'transaction cost'), u=('raise', 'raises', 'increase', 'increases', 'more money', 'higher'))) ], 'c7'),
            V('v6', 'What is Friedman\'s view of the demand for money?',
              'Friedman treated money as one of many assets, so its demand follows the theory of demand for capital assets. It depends on permanent income, which is his measure of wealth, and on the relative returns on other assets like bonds, equity, physical and human capital. Higher inflation or higher returns on other assets reduce the demand for money, and it rises with the price level.',
              [P('p1', 'Money as an asset — theory of demand for assets', 3, 'asset|capital good|durable', min=1),
               P('p2', 'Permanent income (wealth) — not current income', 4, 'permanent income|permanent|wealth', min=1),
               P('p3', 'Relative returns on bonds, equity, physical and human capital / inflation', 3, 'return|bond|equit|human capital|physical capital|inflation|opportunity cost', min=1)], 'c8'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Arjun\'s bond decision', 'difficulty': 'moderate',
            'case': ('Arjun owns a perpetual government bond paying ₹60 a year. The current market interest rate is 6%. He believes the "normal" rate is about 4% and that rates will fall back to it. '
                     'His friend Meena, who thinks the normal rate is 8%, has sold her bonds and is holding cash.'),
            'mcqs': [
                M('k1a', 'What is the current price of Arjun\'s bond?', ['₹1,000', '₹1,500', '₹600', '₹750'], 0, "A perpetual bond's price = annual payment ÷ market interest rate = 60 ÷ 0.06 = ₹1,000. The tempting ₹1,500 is the price at 4%, the rate Arjun expects, not the current rate; ₹750 is the price at Meena's 8%. In practice: bond dealers value perpetual instruments, such as some bank AT1 bonds, by discounting coupons at current market yields.", 'c5', 'moderate', '60/0.06', topic='The Demand for Money'),
                M('k1b', 'If the rate falls to 4% as Arjun expects, the bond price becomes:', ['₹1,500', '₹1,000', '₹2,400', '₹1,040'], 0, 'At 4%, price = 60 ÷ 0.04 = ₹1,500, giving Arjun a capital gain of ₹500 over the current ₹1,000. The tempting ₹1,040 just adds 4% to the price, ignoring the inverse price–yield relationship; ₹2,400 divides by 2.5%. In practice: investors who expect RBI to cut rates buy long-term bonds to earn exactly this kind of capital gain.', 'c5', 'hard', '60/0.04', topic='The Demand for Money'),
                M('k1c', 'Meena holds cash because she expects:', ['Interest rates to rise and bond prices to fall', 'Interest rates to fall and bond prices to rise', 'No change in rates', 'Inflation to be zero'], 0, "Meena's normal (critical) rate is 8%, above the current 6%, so she expects rates to rise; rising rates mean falling bond prices and capital losses, so she sells bonds and holds cash. 'Interest rates to fall and bond prices to rise' is the trap — that is Arjun's expectation. In practice: fund managers who expect yield increases shorten portfolio duration or move to cash.", 'c5', 'moderate', topic='The Demand for Money'),
                M('k1d', 'Their behaviour illustrates that the speculative demand for money is:', ['Inversely related to the interest rate', 'Directly related to income', 'Independent of expectations', 'Perfectly inelastic'], 0, "When the current rate is low relative to what people consider normal, more of them expect rates to rise and prefer cash, so speculative money demand rises as interest rates fall — an inverse relationship. 'Directly related to income' is the trap — that describes transactions demand. In practice: when policy rates are cut sharply, money often piles up in liquid funds and bank balances awaiting better yields.", 'c5', 'core', topic='The Demand for Money'),
            ]}],
    }
