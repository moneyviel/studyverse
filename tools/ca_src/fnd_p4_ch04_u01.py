"""CA Foundation · Paper 4 Business Economics · Chapter 4 Price Determination in Different Markets · Unit 1 Meaning and Types of Markets.
Original explanations, numbers and questions. Every figure is computed in code and re-checked by tools/ca_validate.py."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch04-u01'


def Q(i, q, o, a, e, c, d='core', check=None, topic=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'concept': c, 'difficulty': d}
    if topic: m['topic'] = topic
    if check: m['check'] = check
    return m


def M(i, q, o, a, e, d='moderate', check=None, topic=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if topic: m['topic'] = topic
    if check: m['check'] = check
    return m


def build():
    # ---------- Illustration 1: revenue schedule, P = 44 - 4Q ----------
    c1 = Checks()
    rows1, prev = [], 0
    for q in range(1, 10):
        pr = c1.add(f'44-4*{q}', f'price (AR) at {q} units')
        tr = c1.add(f'{q}*(44-4*{q})', f'TR at {q} units')
        mr = c1.add(f'{tr}-{prev}', f'MR of unit {q}')
        rows1.append([str(q), str(pr), str(tr), str(mr)])
        prev = tr
    trmax = c1.add('5*(44-4*5)', 'maximum TR (at 5 and 6 units)')
    summr = c1.add('40+32+24+16+8', 'sum of MR of first five units = TR at 5 units')
    t1 = table(['Units sold (Q)', 'Price = AR (₹)', 'TR = P × Q (₹)', 'MR = TRn − TRn−1 (₹)'], rows1, num=[1, 2, 3], title='Revenue schedule of Vaani Crafts')

    # ---------- Illustration 2: MR from AR and elasticity ----------
    c2 = Checks()
    mra = c2.add('60*(3-1)/3', 'MR when AR 60, e = 3')
    mrb = c2.add('60*(1.5-1)/1.5', 'MR when AR 60, e = 1.5')
    mrc = c2.add('60*(1-1)/1', 'MR when AR 60, e = 1')
    mrd = c2.add('60*(0.75-1)/0.75', 'MR when AR 60, e = 0.75')
    e_rev = c2.add('80/(80-60)', 'e when AR 80 and MR 60')
    t2 = table(['Case', 'AR (₹)', 'e', 'MR = AR × (e − 1)/e (₹)', 'Effect on TR of selling one more unit'], [
        ['(a)', '60', '3', str(mra), 'Rises — demand elastic'],
        ['(b)', '60', '1.5', str(mrb), 'Rises — demand elastic'],
        ['(c)', '60', '1', str(mrc), 'No change — TR at its maximum'],
        ['(d)', '60', '0.75', str(mrd), 'Falls — demand inelastic'],
    ], num=[1, 2, 3], title='MR, AR and price elasticity')

    # ---------- Illustration 3: shut-down decision ----------
    c3 = Checks()
    tr3 = c3.add('2000*40', 'TR at ₹40')
    tvc3 = c3.add('2000*34', 'TVC at AVC ₹34')
    tfc3 = 18000
    contrib = c3.add('80000-68000', 'contribution at ₹40')
    loss_run = c3.add('80000-(68000+18000)', 'profit at ₹40 if it produces (negative = loss)')
    loss_shut = c3.add('0-18000', 'profit if it shuts down (loses fixed cost)')
    tr3b = c3.add('2000*31', 'TR at ₹31')
    contrib_b = c3.add('62000-68000', 'contribution at ₹31 (negative)')
    loss_run_b = c3.add('62000-(68000+18000)', 'loss if it produces at ₹31')
    t3 = table(['Item', 'Price ₹40', 'Price ₹31'], [
        ['Total revenue (2,000 units)', inr(tr3), inr(tr3b)],
        ['Less: total variable cost (₹34 × 2,000)', inr(tvc3), inr(tvc3)],
        ['Contribution', inr(contrib), inr(contrib_b)],
        ['Less: total fixed cost', inr(tfc3), inr(tfc3)],
        ['Profit / (loss) if it produces', inr(loss_run), inr(loss_run_b)],
        ['Loss if it shuts down (= fixed cost)', inr(loss_shut), inr(loss_shut)],
        ['Decision', 'Produce — smaller loss', 'Shut down — price below AVC'],
    ], title='Produce or shut down? (short run)')

    # ---------- Illustration 4: MR = MC with a schedule ----------
    c4 = Checks()
    prices = [30, 28, 26, 24, 22, 20]
    mcs = [22, 16, 12, 18, 26, 34]
    rows4, ptr, tc = [], 0, 20
    profits = []
    for i, (pr, mc) in enumerate(zip(prices, mcs)):
        q = i + 1
        tr = c4.add(f'{q}*{pr}', f'TR at {q}')
        mr = c4.add(f'{tr}-{ptr}', f'MR of unit {q}')
        tc = c4.add(f'{tc}+{mc}', f'TC at {q}')
        prof = c4.add(f'{tr}-{tc}', f'profit at {q}')
        profits.append(prof)
        rows4.append([str(q), str(pr), str(tr), str(mr), str(mc), str(tc), str(prof)])
        ptr = tr
    best = c4.add('96-(20+22+16+12+18)', 'profit at 4 units (maximum)')
    t4 = table(['Q', 'Price (₹)', 'TR (₹)', 'MR (₹)', 'MC (₹)', 'TC (₹) incl. TFC ₹20', 'Profit (₹)'], rows4, num=[1, 2, 3, 4, 5, 6], title='Finding the profit-maximising output')

    # ---------- written questions ----------
    w1 = Checks()
    w1_tr = [w1.add(f'{q}*(30-2*{q})', f'TR at {q}') for q in range(1, 10)]
    w1_mr = [w1.add(f'{w1_tr[i]}-{w1_tr[i-1] if i else 0}', f'MR of unit {i+1}') for i in range(9)]
    w1_ar = [30 - 2 * q for q in range(1, 10)]
    w1_tab = table(['Q', 'AR (₹)', 'TR (₹)', 'MR (₹)'], [[str(q + 1), str(w1_ar[q]), str(w1_tr[q]), str(w1_mr[q])] for q in range(9)], num=[1, 2, 3], title='Schedule for Q1')
    w2 = Checks()
    w2a = w2.add('120*(4-1)/4', 'MR when AR 120 and e 4')
    w2b = w2.add('120*(0.8-1)/0.8', 'MR when AR 120 and e 0.8')
    w2c = w2.add('90/(90-45)', 'e at AR 90, MR 45')
    w3 = Checks()
    w3_tr = w3.add('5000*26', 'TR')
    w3_tvc = w3.add('5000*22', 'TVC')
    w3_cont = w3.add('130000-110000', 'contribution')
    w3_loss = w3.add('130000-110000-35000', 'loss if it produces')
    w3_save = w3.add('35000-15000', 'loss avoided by producing')
    w3_shut = w3.add('5000*22', 'TR needed to cover TVC = shut-down point revenue')

    # ---------- case ----------
    k = Checks()
    k_tr1 = k.add('1200*2000', 'TR at 1,200 units')
    k_tr2 = k.add('1300*1900', 'TR at 1,300 units')
    k_mru = k.add('(1300*1900-1200*2000)/100', 'MR per unit of the extra 100 units')
    k_e = k.add('2000/(2000-1500)', 'e at AR 2000, MR 1500')

    concepts = [
        {'id': 'c1', 'title': 'Meaning of market, price and value', 'body': [
            'Goods like air and sunlight are free goods: they are plentiful, so nobody pays for them. Economic goods are scarce compared with what people want; obtaining them means giving up something else (an opportunity cost), so they are traded and carry a price.',
            'Price is the money a buyer must give for one unit of a good or service — the worth of the thing stated in money. Economists separate value in use (how useful a thing is in satisfying a want) from value in exchange (what the thing can fetch in other goods, normally measured in money). Ricardo described exchange value as general command over other purchasable goods. Economics deals with exchange value; purely sentimental value is ignored because the market does not pay for it.',
            'In economics a market is not a building. It is the whole network of buyers and sellers of a product who are in contact — face to face, by phone, through an app or an online portal — and whose dealings settle the price.',
            'Elements of a market: (i) people willing to buy and people willing to sell; (ii) the good or service being traded; (iii) haggling or bargaining that settles the price; (iv) awareness of market conditions among the parties; and (v) one price ruling for that product at any given moment.'],
         'analogy': 'An online marketplace for used phones has no shop at all, yet it is a full market: thousands of sellers and buyers, one product, haggling in chats, and a going price that everyone soon learns.',
         'work': 'When a CA values inventory at net realisable value or tests whether an asset is impaired, the question is "what would this fetch in the market?" — exchange value, not cost and not sentimental value.'},
        {'id': 'c2', 'title': 'Classification of markets', 'body': [
            'Product markets are where households buy goods and services from firms; factor markets are where firms hire land, labour, capital and entrepreneurship. Product markets allocate goods to consumers; factor markets allocate resources to producers. Prices in factor markets are called factor prices.',
            'By area: local (perishable or bulky goods, local services such as a tailor), regional (a few adjoining states), national (sold throughout one country), international (high-value, low-bulk goods such as gold). With cold chains and air freight, even perishables now reach international markets, so this split is less useful than it once was.',
            'By time (Alfred Marshall): very short period or market period — supply cannot be changed, so price depends only on demand (fresh fish, flowers); short period — output can be changed only by using more or less of the variable factors with the same plant; long period — all factors are variable and the scale of production can change, so supply fully adjusts and the price settled is the normal price; very long or secular period — slow changes in population, capital supply and raw materials.',
            'By nature of transaction: spot (cash) market — goods and money change hands now or within a short time; forward or futures market — delivery and payment on a future date at a price agreed today. By regulation: regulated markets (rules laid down by law, such as a stock exchange) and unregulated or free markets (a weekly village haat). By volume of business: wholesale (bulk, trader to trader — B2B) and retail (small lots to final consumers — B2C). By competition: perfectly competitive and imperfectly competitive.'],
         'analogy': 'Think of the same mango sold in six ways: in your lane (local), across the country (national), today for cash (spot), booked for next season (forward), in bulk at the mandi (wholesale) and one at a time at the fruit stall (retail).',
         'work': 'Hedging advice, contract reviews and audit of derivatives all start with knowing whether a deal is spot or forward; regulated markets also bring disclosure and compliance work for CAs.'},
        {'id': 'c3', 'title': 'Types of market structures', 'body': [
            'A firm can find its most profitable output only if it knows the demand curve for its own product — and that depends on how many rivals it has, how alike their products are and how they react to its price changes. These features together are called market structure.',
            'Perfect competition: very many sellers of an identical product; no single firm can influence the price. Monopolistic competition: many sellers of differentiated (branded) products, e.g. toothpaste or shampoo makers. Oligopoly: a few large sellers whose decisions affect each other, e.g. telecom operators. Monopoly: a single seller of a product with no close substitute, e.g. rail transport by Indian Railways.',
            'Moving from perfect competition to monopoly, the number of sellers falls, product differentiation and control over price rise, and the price elasticity of demand facing the individual firm falls from infinite to small.'],
         'blocks': [table(['Feature', 'Perfect competition', 'Monopolistic competition', 'Oligopoly', 'Monopoly'], [
             ['Number of sellers', 'Very large', 'Large', 'Few', 'One'],
             ['Product differentiation', 'None (identical)', 'Slight (brands)', 'None to substantial', 'Extreme — no close substitute'],
             ['Price elasticity of demand facing the firm', 'Infinite', 'Large', 'Small', 'Small'],
             ['Control over price', 'None — price taker', 'Some', 'Some', 'Very considerable — price maker'],
         ], title='The four market forms at a glance')],
         'analogy': 'A vegetable mandi (perfect), a street of cafés each with its own style (monopolistic), three telecom giants watching each other (oligopoly), and the only water supplier in town (monopoly).',
         'work': 'Industry analysis in credit appraisal, valuation and equity research begins by placing a company in one of these structures — it tells you how much pricing power and margin to expect.'},
        {'id': 'c4', 'title': 'Total, average and marginal revenue', 'body': [
            'Total revenue (TR) is the money a firm receives from selling a given quantity: TR = P × Q. It equals the total amount buyers spend on the firm\'s product.',
            'Average revenue (AR) is revenue per unit sold: AR = TR ÷ Q = (P × Q) ÷ Q = P. Because AR equals price at every quantity, the AR curve is the firm\'s demand curve.',
            'Marginal revenue (MR) is the change in TR from selling one more unit: MR = ΔTR ÷ ΔQ, or for a one-unit step MRn = TRn − TRn−1 (in calculus terms MR = dTR/dQ, the slope of the TR curve). Adding the MRs of all units sold gives TR: TR = ΣMR.',
            'When the firm must cut the price to sell more, MR is less than the price, because the lower price applies to all the earlier units too. Example: if 4 units sell at ₹50 each and 5 units at ₹47 each, the fifth unit brings ₹47 but the first four now fetch ₹3 less each (₹12), so MR = ₹47 − ₹12 = ₹35 (check: TR 235 − 200 = 35).',
            'With a falling AR, MR falls faster than AR and lies below it; TR rises while MR is positive, is maximum where MR = 0 (slope of TR is zero), and falls when MR turns negative — so the TR curve is shaped like an inverted U. AR can never be zero or negative at a positive output, but MR can be zero or negative.',
            'Under perfect competition the firm sells any amount at the market price, so AR is constant, MR = AR = price, both are one horizontal line, and TR is a straight line rising from the origin.'],
         'analogy': 'TR is the total in the till; AR is the average bill per item; MR is what the till gained from the very last item rung up.',
         'work': 'Pricing proposals that a CA reviews in industry are judged on incremental (marginal) revenue — a discount scheme that lifts volume can still cut total revenue if MR has turned negative.'},
        {'id': 'c5', 'title': 'MR, AR and price elasticity of demand', 'body': [
            'The three are linked by the formula MR = AR × (e − 1) ÷ e, where e is the price elasticity of demand (taken without its minus sign) at that point. Rearranged: e = AR ÷ (AR − MR).',
            'If e > 1 (elastic), MR is positive and TR rises when more is sold at a lower price. If e = 1, MR = 0 and TR is at its maximum. If e < 1 (inelastic), MR is negative and TR falls as more is sold.',
            'On a straight-line demand curve e = 1 at the mid-point, so MR cuts the quantity axis exactly below the mid-point; on the upper half demand is elastic and MR positive, on the lower half demand is inelastic and MR negative.',
            'A profit-maximising firm with a falling demand curve will therefore never choose an output where demand is inelastic, because there MR is negative while MC is always positive.'],
         'analogy': 'Elastic demand is a crowd that rushes in at a small discount — the till rings louder. Inelastic demand is a crowd that hardly moves — a discount only shrinks the takings.',
         'work': 'Before supporting a price cut, a finance controller estimates elasticity from past sales data; if demand is inelastic, the cut will reduce revenue as well as margin.'},
        {'id': 'c6', 'title': 'Behavioural principles of a firm', 'body': [
            'Principle 1 — do not produce at all unless total variable cost is covered. Fixed costs are already committed (sunk) and must be paid whether or not the firm produces, so they do not affect the shut-down decision. If price is below minimum average variable cost (AVC), producing adds to the loss; by shutting down the loss is limited to the fixed cost. Minimum AVC is therefore the shut-down price. Shutting down is a short-run, temporary step, not the same as leaving the industry.',
            'Ranking the cases: price below minimum AVC — shut down; price between minimum AVC and minimum average total cost (ATC) — produce, recover all variable cost and part of fixed cost, but make a loss; price equal to minimum ATC — normal profit (zero economic profit); price above minimum ATC — supernormal (economic) profit.',
            'Principle 2 — expand output up to the point where marginal revenue equals marginal cost. While MR > MC, each extra unit adds more to revenue than to cost and raises profit; beyond the point where MR = MC, MC > MR and each extra unit lowers profit. For a true maximum the MC curve must cut the MR curve from below.'],
         'analogy': 'A taxi driver on a slow night keeps driving if fares at least pay for fuel (variable cost); the car-loan EMI (fixed cost) is due either way. If fares do not even pay for fuel, he parks the car.',
         'work': 'CAs in industry apply exactly this logic in "make or shut", special-order and plant-suspension decisions — relevant costs are the avoidable (variable) ones, not the sunk fixed costs.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Revenue schedule with a falling price', 'difficulty': 'core', 'minutes': 8,
         'q': 'Vaani Crafts can sell 1 lamp at ₹40, and each extra lamp needs a price cut of ₹4 (price = 44 − 4Q). Prepare a schedule of AR, TR and MR for 1 to 9 lamps. At what output is TR maximum, and what is MR there?',
         'solution': [t1, wn('Reading the schedule', f'TR rises while MR is positive, reaches its maximum of {R(trmax)} at 5 and 6 lamps (MR of the 6th lamp = 0) and then falls as MR turns negative. AR falls by ₹4 per lamp, but MR falls by ₹8 — twice as fast.'),
                      p(f'Check: TR at 5 units = sum of the first five MRs = 40 + 32 + 24 + 16 + 8 = {R(summr)}.')],
         'checks': c1},
        {'id': 'i2', 'title': 'MR from AR and elasticity', 'difficulty': 'core', 'minutes': 6,
         'q': 'A firm sells at a price (AR) of ₹60. Find MR when price elasticity of demand is (a) 3, (b) 1.5, (c) 1, (d) 0.75. Also find the elasticity at a point where AR = ₹80 and MR = ₹60.',
         'solution': [t2, wn('Reverse use of the formula', f'e = AR ÷ (AR − MR) = 80 ÷ (80 − 60) = {e_rev}.'), note('MR is negative only when demand is inelastic (e < 1); a profit-maximiser will not operate there.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Should the plant run this month?', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'Sarthak Polymers, a price-taking firm, can produce 2,000 units a month. Its average variable cost at that output is ₹34 and monthly fixed cost (rent, permanent staff, interest) is ₹18,000. Should it produce if the market price is (a) ₹40, (b) ₹31?',
         'solution': [t3, p(f'At ₹40 the firm earns a contribution of {R(contrib)} towards fixed cost, so producing limits the loss to {R(-loss_run)} against {R(-loss_shut)} on shutting down. At ₹31 price is below AVC: producing would lose {R(-loss_run_b)}, more than the fixed cost, so it should shut down for now and restart when price recovers above AVC.')],
         'checks': c3},
        {'id': 'i4', 'title': 'Profit is highest where MR = MC', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'Nidhi Foods faces the price schedule below (₹30 for 1 unit, falling by ₹2 per extra unit). Its total fixed cost is ₹20 and the marginal costs of successive units are ₹22, 16, 12, 18, 26 and 34. Find the profit-maximising output and show that MR = MC there.',
         'solution': [t4, p(f'For units 1 to 3, MR (30, 26, 22) exceeds MC (22, 16, 12), so each adds to profit. For the 4th unit MR = MC = ₹18 — it adds nothing. For the 5th unit MR (₹14) is below MC (₹26), so profit falls from {R(profits[3])} to {R(profits[4])}.'),
                      p(f'Profit-maximising output = 4 units (where MR = MC and MC is rising, i.e. MC cuts MR from below); maximum profit = {R(best)} (the same profit at 3 units, because the 4th unit adds exactly as much to revenue as to cost).')],
         'checks': c4},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Will a price cut raise revenue?', 'role': 'CA in industry — commercial finance at a packaged-foods company',
         'situation': 'Sales wants to cut the price of a 1 kg pack of atta from ₹62 to ₹58 to "grow revenue". Past promotions show that a similar cut raised volume by about 4%.',
         'steps': ['Work out the price change: (62 − 58) ÷ 62 ≈ 6.5% fall.', 'Volume rose about 4% for a 6.5% cut, so elasticity ≈ 4 ÷ 6.5 ≈ 0.6 — demand is inelastic (e < 1).', 'With e < 1, MR is negative: selling more at the lower price reduces total revenue, before even counting margin.', 'Recommend non-price tools (bigger pack, visibility, combo offers) or a targeted discount instead of a blanket price cut.'],
         'takeaway': 'Link MR to elasticity before approving any discount: below e = 1, a price cut lowers revenue.', 'think': 'At what elasticity would the cut leave total revenue roughly unchanged?', 'answer': 'At unit elasticity (e = 1), where MR = 0 and TR is at its maximum.'},
        {'id': 'j2', 'title': 'Suspend the night shift?', 'role': 'CA in practice advising an MSME manufacturer during a slump',
         'situation': 'Market prices for the client\'s castings have fallen. The night shift adds output whose selling price no longer covers power, raw material and shift wages; factory rent and loan interest are paid anyway.',
         'steps': ['Separate avoidable (variable) costs — power, material, shift wages — from fixed costs that continue anyway.', 'Compare price with average variable cost of the night-shift output, not with full cost.', 'If price is below AVC, suspend the shift: the loss falls to the fixed costs that are unavoidable.', 'Advise that this is temporary — restart when price again exceeds AVC; exit from the industry is a separate long-run question.'],
         'takeaway': 'The shut-down rule uses variable cost; sunk fixed costs do not decide whether to produce in the short run.'},
    ]

    mcqs = [
        Q('m1', 'In economics, the term "market" refers to:', ['Buyers and sellers of a product in contact with one another, whose dealings settle its price', 'A building where goods are sold', 'Only the place where wholesale trade happens', 'The list of goods a shop keeps'], 0, 'In economics, a market is the whole arrangement through which buyers and sellers of a product are in contact — in person, by phone or online — and their dealings settle its price. "A building where goods are sold" is the trap: a physical place is not needed. In practice: India\'s share market runs on NSE and BSE screens, with buyers and sellers across the country trading without ever meeting.', 'c1', topic='Meaning of Market'),
        Q('m2', 'Which of the following is NOT an element of a market?', ['A fixed physical place of trade', 'Buyers and sellers', 'A product or service', 'Bargaining for a price'], 0, 'A market needs buyers and sellers, a product or service, bargaining over price, and knowledge of market conditions — but not a fixed physical place. "Bargaining for a price" is the tempting distractor, since price is often printed, yet price still emerges from the interaction of buyers and sellers. In practice: e-commerce platforms and online commodity exchanges are full markets with no physical marketplace at all.', 'c1', topic='Meaning of Market'),
        Q('m3', 'Economics is concerned mainly with:', ['Value in exchange', 'Value in use only', 'Sentimental value', 'Historical cost'], 0, 'Economics deals mainly with value in exchange — what a good can fetch in terms of money or other goods in the market. "Value in use only" is the trap: water has huge value in use but little exchange value, and economics studies market prices. In practice: when a CA values inventory or a business for sale, the question is what it would fetch in the market, not how useful it feels.', 'c1', topic='Meaning of Market'),
        Q('m4', 'Markets in which firms buy land, labour, capital and entrepreneurship are called:', ['Factor markets', 'Product markets', 'Spot markets', 'Retail markets'], 0, 'Factor markets are where firms hire or buy factors of production — land, labour, capital and entrepreneurship; their prices are rent, wages, interest and profit. "Product markets" is the trap — those are where finished goods and services are sold to buyers. In practice: a company recruiting engineers through campus placements is operating in the labour market, a factor market.', 'c2', topic='Meaning of Market'),
        Q('m5', 'The classification of markets into very short period, short period, long period and secular period is based on:', ['Time', 'Area', 'Volume of business', 'Regulation'], 0, 'Classifying markets into the very short period, short period, long period and secular period is based on time — how long sellers have to adjust supply. Alfred Marshall introduced this time element. "Area" is the trap; area-based classification gives local, national and international markets. In practice: vegetable prices react within a day to supply shocks, while steel capacity takes years to adjust.', 'c2', topic='Meaning of Market'),
        Q('m6', 'In the very short period (market period), price is determined mainly by:', ['Demand, since supply is fixed', 'Supply, since demand is fixed', 'Cost of production', 'Government only'], 0, 'In the very short period (market period), supply is fixed at the stock available, so price is determined mainly by demand: higher demand raises price, lower demand reduces it. "Supply, since demand is fixed" is the trap — it reverses the logic; demand can change any day, while supply cannot. In practice: flower prices shoot up on Diwali and wedding days because stock is fixed for that day while demand jumps.', 'c2', 'moderate', topic='Meaning of Market'),
        Q('m7', 'The price settled in the long period, when all factors are variable, is called:', ['Normal price', 'Market price', 'Shut-down price', 'Reserve price'], 0, 'In the long period, all factors can be varied and firms can enter or exit, so price settles at the long-run equilibrium level called the normal price. "Market price" is the trap — that is the short-term price in the market period, which can swing above or below the normal price. In practice: although tomato prices may spike for a week, over years they hover around a level that covers growers\' costs.', 'c2', topic='Meaning of Market'),
        Q('m8', 'A contract to buy US dollars from a bank three months from now at a rate fixed today is a transaction in the:', ['Forward market', 'Spot market', 'Retail market', 'Unregulated market'], 0, 'A deal to buy dollars three months from now at a rate fixed today is a forward contract: price is agreed now, delivery and payment happen later. "Spot market" is the trap — there, delivery and payment happen almost immediately at today\'s rate. In practice: Indian importers routinely book forward contracts with banks to protect themselves against the rupee weakening before payment is due.', 'c2', topic='Meaning of Market'),
        Q('m9', 'A stock exchange is an example of a:', ['Regulated market', 'Unregulated market', 'Local market', 'Factor market for labour'], 0, 'A stock exchange is a regulated market: trading follows statutory rules on listing, disclosure and settlement to prevent fraud and unfair practices. "Unregulated market" is the trap — unregulated markets have no such official oversight. In practice: in India, SEBI regulates NSE and BSE, and CAs certify financial results that listed companies must file with the exchanges.', 'c2', topic='Meaning of Market'),
        Q('m10', 'Trade between a manufacturer and a distributor in bulk lots (B2B) takes place in the:', ['Wholesale market', 'Retail market', 'Spot market only', 'Factor market'], 0, 'Bulk trade between a manufacturer and a distributor, business to business (B2B), takes place in the wholesale market. "Retail market" is the trap; retail involves selling in small quantities to final consumers (B2C). In practice: an FMCG company sells cartons to distributors at wholesale prices, who then supply kirana stores that sell single packs to households.', 'c2', topic='Meaning of Market'),
        Q('m11', 'Many sellers offering differentiated products to many buyers describes:', ['Monopolistic competition', 'Perfect competition', 'Oligopoly', 'Monopoly'], 0, 'Monopolistic competition has many sellers, each offering a slightly differentiated product — by brand, design or service — to many buyers. "Perfect competition" is the trap: it also has many sellers, but their products are identical, so no seller can charge more than the market price. In practice: restaurants, salons and toothpaste brands in India compete through differentiation rather than identical products.', 'c3', topic='Types of Market Structures'),
        Q('m12', 'The price elasticity of demand facing an individual firm under perfect competition is:', ['Infinite', 'Zero', 'Equal to one', 'Less than one'], 0, 'Under perfect competition, an individual firm is too small to influence price; it can sell any quantity at the market price but nothing above it, so its demand curve is horizontal — perfectly elastic, with elasticity infinite. "Zero" is the trap; that is a vertical, perfectly inelastic curve. In practice: a single wheat farmer at a mandi must accept the going price and cannot charge more.', 'c3', topic='Types of Market Structures'),
        Q('m13', 'Which market form has a few sellers whose decisions are interdependent?', ['Oligopoly', 'Monopoly', 'Perfect competition', 'Monopolistic competition'], 0, 'Oligopoly is competition among a few large sellers; because each holds a big share, one firm\'s price or output decision affects the others, so their decisions are interdependent. "Monopoly" is the trap — a monopolist has no rivals to react to. In practice: India\'s telecom market, with a handful of major operators, shows oligopoly behaviour: when one raises tariffs, the others usually follow soon after.', 'c3', topic='Types of Market Structures'),
        Q('m14', 'Average revenue is always equal to:', ['Price', 'Marginal revenue', 'Total revenue', 'Marginal cost'], 0, 'Average revenue = total revenue ÷ quantity = (price × quantity) ÷ quantity = price, so AR always equals price and the AR curve is the firm\'s demand curve. "Marginal revenue" is the trap — MR equals AR only when price is constant, as under perfect competition. In practice: a shop\'s revenue per unit sold, worked out from its sales register, is simply the average price it charged.', 'c4', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m15', 'A firm sells 10 units at ₹95 each. To sell 11 units it must cut the price to ₹92. MR of the 11th unit is:', ['₹62', '₹92', '₹3', '₹1,012'], 0, 'MR of the 11th unit = TR(11) − TR(10) = 11 × 92 − 10 × 95 = 1,012 − 950 = ₹62. ₹92 is the trap — that is the price (AR) of the 11th unit, but the ₹3 cut on the first 10 units (₹30) reduces the net gain. ₹1,012 is total revenue. In practice: a firm considering a price cut to sell one more unit must count the revenue lost on all existing sales.', 'c4', 'moderate', '(11*92)-(10*95)', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m16', 'A firm earns total revenue of ₹7,200 from selling 90 units. Its average revenue is:', ['₹80', '₹90', '₹72', '₹6,480'], 0, 'Average revenue = total revenue ÷ units sold = 7,200 ÷ 90 = ₹80 per unit, which is also the price. ₹90 is the trap — it is the quantity sold, not revenue per unit. In practice: a business owner checking average revenue per unit can see at once whether discounts have pulled the effective selling price down.', 'c4', 'core', '7200/90', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m17', 'When a firm must lower its price to sell an additional unit, MR is:', ['Less than AR', 'Equal to AR', 'Greater than AR', 'Always zero'], 0, 'When a firm must cut price to sell one more unit, the lower price applies to all earlier units too, so the extra revenue from that unit is less than its price — MR is less than AR. "Equal to AR" is the trap; that holds only when the firm can sell more at an unchanged price, as under perfect competition. In practice: a festival discount for new buyers also cuts revenue on customers who would have paid full price.', 'c4', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m18', 'Total revenue is maximum when:', ['MR is zero', 'MR equals AR', 'AR is zero', 'MR is maximum'], 0, 'Total revenue rises while MR is positive and falls once MR turns negative, so it is maximum where MR = 0 — at unit elasticity. "MR equals AR" is the trap; that holds under perfect competition at every output, not specifically at maximum TR. In practice: a firm interested only in sales value, ignoring costs, would set the price where demand elasticity is exactly one.', 'c4', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m19', 'Under perfect competition, the AR and MR curves of a firm are:', ['The same horizontal line', 'Downward sloping with MR below AR', 'Upward sloping', 'Vertical'], 0, 'Under perfect competition, the firm sells every unit at the same market price, so each extra unit adds exactly that price to revenue: AR = MR = P, a single horizontal line. "Downward sloping with MR below AR" is the trap — that describes a firm with some price-setting power, such as a monopolist. In practice: a small rice mill selling at the market rate earns the same amount per extra quintal.', 'c4', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m20', 'Price (AR) is ₹45 and price elasticity of demand is 2.5. Marginal revenue is:', ['₹27', '₹18', '₹63', '₹112.5'], 0, 'MR = AR × (e − 1) ÷ e = 45 × (2.5 − 1) ÷ 2.5 = 45 × 1.5 ÷ 2.5 = ₹27. ₹18 is the trap — it divides 45 by 2.5 and forgets the (e − 1) term. In practice: pricing analysts use this link to estimate the extra revenue from selling more once they know the price elasticity of demand.', 'c5', 'moderate', '45*(2.5-1)/2.5', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m21', 'If AR = ₹50 and MR = ₹30, price elasticity of demand is:', ['2.5', '1.67', '0.6', '0.4'], 0, 'From MR = AR(e − 1)/e, e = AR ÷ (AR − MR) = 50 ÷ (50 − 30) = 50 ÷ 20 = 2.5. 1.67 is the trap — it divides AR by MR (50 ÷ 30), using the wrong formula. In practice: if a firm knows its price and the extra revenue from one more sale, it can back out its demand elasticity to judge whether a price cut will pay.', 'c5', 'moderate', '50/(50-30)', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m22', 'When price elasticity of demand is less than one, marginal revenue is:', ['Negative', 'Positive', 'Zero', 'Equal to price'], 0, 'MR = AR × (e − 1) ÷ e. If e is less than one, (e − 1) is negative, so MR is negative: selling an extra unit actually reduces total revenue. "Positive" is the trap — MR is positive only when demand is elastic (e greater than 1). In practice: this is why a firm facing inelastic demand would never cut its price, since it would sell more but earn less.', 'c5', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m23', 'On a straight-line downward-sloping demand curve, MR is zero at:', ['The mid-point of the demand curve', 'The point where it meets the price axis', 'The point where it meets the quantity axis', 'Every point'], 0, 'On a straight-line demand curve, elasticity is one at the mid-point; since MR = AR × (e − 1) ÷ e, MR is zero there and total revenue is at its peak. "The point where it meets the quantity axis" is the trap — there elasticity is zero and MR is strongly negative. In practice: a toll operator seeking maximum collections, with negligible running cost, would set tolls near the mid-point of demand.', 'c5', 'moderate', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m24', 'A firm should shut down in the short run if price is below:', ['Minimum average variable cost', 'Minimum average total cost', 'Average fixed cost', 'Marginal revenue'], 0, 'In the short run, fixed cost is lost whether or not the firm produces. If price falls below minimum average variable cost, producing does not even cover variable cost, so the firm should shut down and limit its loss to fixed cost. "Minimum average total cost" is the trap — below that the firm makes a loss but can still keep producing if price covers AVC. In practice: seasonal units halt production when prices crash.', 'c6', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m25', 'If price lies between minimum AVC and minimum ATC, a firm in the short run will:', ['Continue producing at a loss', 'Shut down at once', 'Earn supernormal profit', 'Earn normal profit'], 0, 'If price is above minimum AVC but below minimum ATC, the firm covers all variable cost and part of fixed cost, so producing gives a smaller loss than shutting down (which loses all fixed cost). It continues at a loss in the short run. "Shut down at once" is the trap. In practice: hotels in the off-season keep operating at low rates because revenue still covers staff and power, plus some fixed cost.', 'c6', 'moderate', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m26', 'A firm maximises profit at the output where:', ['MR = MC and MC cuts MR from below', 'TR is maximum', 'AR = AC', 'MC is minimum'], 0, 'Profit is maximised where MR = MC and MC is rising — cutting MR from below. Before that point, each extra unit adds more to revenue than to cost; after it, the reverse. "TR is maximum" is the trap — that maximises revenue, not profit, because it ignores cost. In practice: a factory manager stops accepting extra orders once the extra cost of output exceeds the extra revenue it brings.', 'c6', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m27', 'A price-taking firm has fixed cost ₹50,000, AVC ₹60 and sells 1,000 units at ₹55. Its best short-run choice and resulting loss is:', ['Shut down; loss ₹50,000', 'Produce; loss ₹45,000', 'Produce; loss ₹55,000', 'Shut down; no loss'], 0, 'Price ₹55 is below AVC ₹60, so each unit loses ₹5 of variable cost. Producing: loss = 50,000 + 1,000 × 5 = ₹55,000. Shutting down: loss = fixed cost only = ₹50,000. So the best choice is to shut down. "Produce; loss ₹45,000" is the trap — it subtracts the ₹5,000 variable-cost shortfall from fixed cost instead of adding it. In practice: small manufacturers suspend production during price slumps to avoid adding to losses.', 'c6', 'hard', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        Q('m28', 'Which statement is correct?', ['AR can never be negative, but MR can be negative', 'MR can never be negative', 'AR and MR are always equal', 'TR keeps rising as long as AR is positive'], 0, 'Average revenue equals price, and price cannot be negative; but marginal revenue can be negative when cutting the price to sell more reduces total revenue (inelastic demand). "TR keeps rising as long as AR is positive" is the trap — TR falls once MR turns negative, even while price is still positive. In practice: flooding a market with stock can lower total sales value, as farmers find in glut years.', 'c4', 'moderate', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'Demand for a firm\'s product is P = 30 − 2Q. (a) Prepare a schedule of AR, TR and MR for Q = 1 to 9. (b) At what output is TR maximum? (c) State the relationship between AR and MR shown by your schedule.',
         'model': [w1_tab, p(f'(b) TR is maximum at {R(w1_tr[6])} for 7 and 8 units, where MR becomes zero (MR of the 8th unit = {w1_mr[7]}). Beyond this MR is negative ({w1_mr[8]} for the 9th unit) and TR falls.'),
                   p('(c) AR falls by ₹2 per unit while MR falls by ₹4 per unit: MR is below AR and falls twice as fast; MR = AR only for the first unit; TR = sum of MRs.')],
         'scheme': [{'id': 's1', 'pt': 'TR computed correctly for all quantities', 'm': 2, 'skill': 'computation'}, {'id': 's2', 'pt': 'MR column (TRn − TRn−1) correct', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Identifies TR maximum at 7–8 units where MR = 0', 'm': 1, 'skill': 'analysis'}, {'id': 's4', 'pt': 'States AR–MR relationship (MR below AR, falls twice as fast)', 'm': 1, 'skill': 'concept'}],
         'remarks': ['Most errors come from computing MR as TR ÷ Q (that is AR).', 'Candidates who label the columns and show one sample calculation get full credit even with a small slip later.'],
         'mistakes': ['Taking MR = price.', 'Stopping the schedule at the TR peak and missing negative MR.', 'Saying TR is maximum where AR is maximum.'], 'tips': ['Draw a four-column table: Q, AR, TR, MR.', 'Write MRn = TRn − TRn−1 once at the top.'], 'checks': w1},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'A firm sells its product at ₹120. (a) Find MR when price elasticity is 4 and when it is 0.8. (b) Find elasticity at a point where AR = ₹90 and MR = ₹45. (c) Why would a profit-maximising firm never operate where e = 0.8?',
         'model': [p(f'(a) MR = AR × (e − 1)/e. With e = 4: 120 × 3/4 = {R(w2a)}. With e = 0.8: 120 × (−0.2)/0.8 = −₹{abs(w2b)}.'),
                   p(f'(b) e = AR ÷ (AR − MR) = 90 ÷ 45 = {w2c} — demand is elastic, so MR is positive.'),
                   p('(c) With e < 1, MR is negative. MC is always positive, so MR = MC can never hold there; cutting output would raise revenue and lower cost at the same time.')],
         'scheme': [{'id': 's1', 'pt': 'Formula MR = AR(e − 1)/e', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Both MR values correct', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'e = AR/(AR − MR) = 2', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'Reason: MR negative, cannot equal positive MC', 'm': 1, 'skill': 'analysis'}],
         'remarks': ['Sign errors on MR at e < 1 are the most common slip.'], 'mistakes': ['Using MR = AR × e/(e − 1).', 'Dropping the minus sign of MR.'], 'tips': ['Memorise both forms: MR = AR(e − 1)/e and e = AR/(AR − MR).'], 'checks': w2},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'A price-taking firm sells 5,000 units at ₹26 each. AVC is ₹22 and total fixed cost is ₹35,000. Should it continue production in the short run? Show workings. Below what price should it shut down?',
         'model': [table(['Item', '₹'], [['TR (5,000 × 26)', inr(w3_tr)], ['Less: TVC (5,000 × 22)', inr(w3_tvc)], ['Contribution', inr(w3_cont)], ['Less: TFC', '35,000'], ['Loss if it produces', inr(w3_loss)], ['Loss if it shuts down', '-35,000']]),
                   p(f'Producing cuts the loss by {R(w3_save)} (from ₹35,000 to {R(-w3_loss)}), so the firm should continue. It should shut down if price falls below minimum AVC (here ₹22), when TR would be less than TVC of {R(w3_shut)}.')],
         'scheme': [{'id': 's1', 'pt': 'Contribution computed', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'Compares loss on producing with loss on shutting down', 'm': 1, 'skill': 'analysis'},
                    {'id': 's3', 'pt': 'Decision: continue', 'm': 1, 'skill': 'conclusion'}, {'id': 's4', 'pt': 'Shut-down price = minimum AVC', 'm': 1, 'skill': 'concept'}],
         'remarks': ['Strong answers state that fixed cost is unavoidable in the short run.'], 'mistakes': ['Comparing price with ATC and advising closure.', 'Treating shut-down as permanent exit.'], 'tips': ['Always show "loss if it produces" next to "loss if it shuts down".'], 'checks': w3},
    ]

    viva = [
        V('v1', 'What does the word market mean in economics, and what are its elements?',
          'In economics a market is not a place. It is all the buyers and sellers of a product who are in touch with each other and whose dealings fix the price. Its elements are the buyers and sellers themselves, the good being traded, bargaining over the price, knowledge of market conditions, and a single price ruling at any one time.',
          [P('p1', 'Not a place — buyers and sellers in contact who settle the price', 4, 'not a place|not place|not a building|no fixed place|need not be a place|not necessarily a place|not physical|any place|online|not a location', 'buyer', 'seller'),
           P('p2', 'Elements: product, bargaining, knowledge, one price', 6, 'product|commodity|service', 'bargain|negotiat|haggl', 'knowledge|information|aware', 'one price|single price|same price|uniform price', min=3)], 'c1'),
        V('v2', 'Define total revenue, average revenue and marginal revenue.',
          'Total revenue is price multiplied by quantity sold. Average revenue is total revenue divided by quantity, which is simply the price, so the average revenue curve is the demand curve. Marginal revenue is the change in total revenue from selling one more unit, that is TR of n units minus TR of n minus one units.',
          [P('p1', 'TR = price × quantity', 3, 'price multipl|price times|p into q|price into quantity|p times q|price x quantity|quantity multipl|quantity times price|multiply price'),
           P('p2', 'AR = TR ÷ Q = price (AR curve is the demand curve)', 3, 'divided by quantity|divide by quantity|per unit|by number of units|tr by q|divided by output', 'price|demand curve', min=2),
           P('p3', 'MR = change in TR from one more unit (TRn − TRn−1)', 4, 'change in total revenue|addition to total revenue|change in tr|extra revenue|additional revenue|increase in total revenue|add to total revenue', 'one more unit|additional unit|extra unit|one additional|n minus one|next unit|one extra|1 more unit|1 additional', min=2)], 'c4'),
        V('v3', 'How are marginal revenue, average revenue and price elasticity of demand related?',
          'Marginal revenue equals average revenue multiplied by e minus one, divided by e. So marginal revenue is positive when elasticity is more than one; marginal revenue is zero when elasticity equals one, which is where total revenue is at its maximum; and marginal revenue is negative when elasticity is less than one.',
          [P('p1', 'MR = AR × (e − 1)/e', 4, ALT('{e} minus 1', '{e} 1 divided', 'e 1 e', 'e 1 by e', 'e 1 over e', e=['e', 'elasticity'])),
           P('p2', 'e > 1 → MR positive', 2, ALT('{m} 1 {mr} positive', '{m} 1 marginal revenue positive', 'elastic {mr} positive', 'elastic marginal revenue positive', 'positive when {e} {m}', m=['more', 'greater', 'above', 'exceeds', 'over', 'bigger'], mr=['mr', 'it is', 'is'], e=['e', 'elasticity', 'demand is'])),
           P('p3', 'e = 1 → MR zero, TR maximum', 2, ALT('equal 1 {mr} zero', 'equals 1 {mr} zero', 'unity {mr} zero', 'unit elasticity {mr} zero', 'unit elastic {mr} zero', 'unitary {mr} zero', 'zero when {e} 1', 'is 1 {mr} zero', 'equal to 1 {mr} zero', mr=['mr', 'marginal revenue', 'it is', 'is'], e=['e', 'elasticity', 'e is', 'elasticity is'])),
           P('p4', 'e < 1 → MR negative', 2, ALT('less 1 {mr} negative', 'below 1 {mr} negative', 'inelastic {mr} negative', 'negative when {e} less', 'negative when demand inelastic', 'smaller 1 {mr} negative', mr=['mr', 'marginal revenue', 'it is', 'is', ''], e=['e', 'elasticity', 'e is', 'elasticity is']))], 'c5'),
        V('v4', 'When should a firm shut down in the short run, and why are fixed costs ignored in that decision?',
          'A firm should shut down in the short run when price falls below minimum average variable cost, because then it cannot even recover its variable cost. Fixed costs are ignored because they are sunk and have to be paid whether the firm produces or not; by shutting down the loss is limited to the fixed cost. Shutting down is temporary and is not the same as leaving the industry.',
          [P('p1', 'Shut down when price < minimum AVC', 5, 'below average variable cost|less than average variable cost|below avc|less than avc|below minimum avc|below minimum average variable|price not cover variable|not even cover variable|cannot cover variable|not recover variable|fail to cover variable|lower than average variable|under average variable|does not cover variable'),
           P('p2', 'Fixed costs are sunk — paid anyway; loss limited to fixed cost', 3, 'sunk|already incurred|paid anyway|paid whether|have to be paid|unavoidable|must be paid|incurred anyway|committed', 'loss limited to fixed|loss equal to fixed|lose only fixed|loss is fixed cost|loss = fixed|only lose fixed|loss limited|minimis loss|minimiz loss|minimise loss|minimize loss', min=1),
           P('p3', 'Shut-down is temporary, not exit', 2, 'temporar|short term|not permanent|not exit|not leave|restart|resume|not same as leaving|not close permanently')], 'c6'),
        V('v5', 'State the profit-maximising rule for a firm.',
          'A firm maximises profit where marginal revenue equals marginal cost. As long as marginal revenue is greater than marginal cost, each extra unit adds to profit, so output should be expanded. The second condition is that the marginal cost curve must cut the marginal revenue curve from below, that is MC must be rising at that point.',
          [P('p1', 'MR = MC', 5, 'marginal revenue equal marginal cost|mr equal mc|mr = mc|mr equals mc|marginal revenue equals marginal cost|marginal cost equal marginal revenue|mc equal mr|mc equals mr|marginal cost equals marginal revenue|equate marginal revenue|equate mr'),
           P('p2', 'Expand while MR > MC', 2, ALT('marginal revenue {g} marginal cost', 'mr {g} mc', 'mc less mr', 'marginal cost less marginal revenue', 'mr more mc', 'mr exceeds mc', g=['greater', 'more', 'exceeds', 'higher', 'above'])),
           P('p3', 'MC cuts MR from below (MC rising)', 3, 'from below|cut from below|rising|upward slop|positive slope|increasing mc|mc increas')], 'c6'),
        V('v6', 'How did Marshall classify markets on the basis of time?',
          'Marshall divided markets by time into four. In the very short or market period supply is fixed, so price depends on demand alone. In the short period supply can be changed only by using more or fewer variable factors with the same plant. In the long period all factors are variable and supply fully adjusts, giving the normal price. The very long or secular period covers slow changes in population, capital and raw materials.',
          [P('p1', 'Very short / market period — supply fixed, price set by demand', 3, 'very short|market period', 'supply fixed|fixed supply|supply cannot change|supply constant|supply cannot be|supply can not', min=2),
           P('p2', 'Short period — variable factors only, same plant', 2, 'short period|short run', 'variable factor|variable input|existing plant|same plant|fixed plant|plant fixed', min=2),
           P('p3', 'Long period — all factors variable; normal price', 3, 'long period|long run', 'all factors variable|all factor variable|all inputs variable|everything variable|normal price|scale change|scale of production', min=2),
           P('p4', 'Secular / very long period — population, capital, raw materials', 2, 'secular|very long', 'population|capital|raw material', min=2)], 'c2'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Shreya Electricals — pricing a ceiling fan', 'difficulty': 'hard',
        'case': ('Shreya Electricals sells 1,200 ceiling fans a month at ₹2,000 each. Its marketing head finds that cutting the price to ₹1,900 would raise monthly sales to 1,300 fans. '
                 'At the present price the finance team estimates the firm\'s marginal revenue at ₹1,500 a fan. The plant\'s monthly fixed cost is ₹6,00,000 and its minimum average variable cost is ₹1,200 a fan.'),
        'mcqs': [
            M('k1a', 'What is the marginal revenue per fan of the extra 100 fans sold at the lower price?', ['₹700', '₹1,900', '₹100', '₹1,800'], 0, "TR before = 1,200 × 2,000 = ₹24,00,000; after = 1,300 × 1,900 = ₹24,70,000. Extra revenue = ₹70,000 for 100 more fans, so MR = ₹700 per fan. ₹1,900 is the trap — it is the new price, but the ₹100 cut also applies to the 1,200 fans already being sold. In practice: before a price cut, Shreya's finance team must compare this ₹700 with the extra cost of producing each fan.", 'hard', '(1300*1900-1200*2000)/100', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
            M('k1b', 'Using AR = ₹2,000 and MR = ₹1,500, the price elasticity of demand at the present price is:', ['4', '1.33', '0.75', '0.25'], 0, 'Elasticity = AR ÷ (AR − MR) = 2,000 ÷ (2,000 − 1,500) = 2,000 ÷ 500 = 4, so demand is highly elastic. 1.33 is the trap — it divides AR by MR (2,000 ÷ 1,500), a common slip. In practice: an elasticity of 4 tells the marketing head that customers are very price-sensitive, which supports carefully targeted price cuts.', 'moderate', '2000/(2000-1500)', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
            M('k1c', 'Since MR is positive at the present price, the firm is operating on the:', ['Elastic part of its demand curve', 'Inelastic part of its demand curve', 'Point of unit elasticity', 'Horizontal part of its demand curve'], 0, 'MR = AR(e − 1)/e is positive only when e is greater than one, so a positive MR of ₹1,500 means the firm is on the elastic part of its demand curve. "Inelastic part" is the trap — there MR would be negative. In practice: a profit-maximising firm with some pricing power always operates where demand is elastic, which is a quick sense-check for any pricing proposal.', 'core', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
            M('k1d', 'If a slump pushed the fan price down to ₹1,100 for a few months, the firm should in the short run:', ['Stop production, because price is below minimum AVC of ₹1,200', 'Keep producing, because fixed cost must be recovered', 'Keep producing, because price is above zero', 'Close the business permanently at once'], 0, 'At ₹1,100, price is below the minimum AVC of ₹1,200, so each fan produced loses money even before fixed cost. Stopping production temporarily limits the loss to the ₹6,00,000 fixed cost. "Keep producing, because fixed cost must be recovered" is the trap — fixed cost is lost anyway, and producing only adds a variable-cost loss. In practice: manufacturers pause lines during slumps and restart when prices recover.', 'moderate', topic='Concepts of Total Revenue, Average Revenue and Marginal Revenue'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch04', 'n': 1, 'title': 'Meaning and Types of Markets',
        'outcomes': ['Explain what a market means in economics, its elements, and how markets are classified (area, time, transaction, regulation, volume, competition).',
                     'Describe the four market structures — perfect competition, monopolistic competition, oligopoly and monopoly — and compare their key features.',
                     'Compute total, average and marginal revenue from a schedule and use MR = AR(e − 1)/e.',
                     'Apply the two behavioural principles: the shut-down rule (price vs minimum AVC) and profit maximisation at MR = MC.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 45}, 'prereq': ['fnd-p4-ch02-u01', 'fnd-p4-ch03-u02'],
                 'exam_tip': 'Expect 2–4 MCQs from this unit: MR from a schedule, MR from elasticity, TR maximum at e = 1, and the shut-down condition. Write MRn = TRn − TRn−1 in rough work every time.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Market = buyers and sellers in contact who settle a price; it need not be a place.', 'Elements: buyers and sellers, the good traded, bargaining, knowledge, a single ruling price.',
                        'Classified by area, time (Marshall: very short, short, long, secular), transaction (spot/forward), regulation, volume (wholesale/retail) and competition.',
                        'Four structures: perfect competition, monopolistic competition, oligopoly, monopoly.', 'TR = P × Q; AR = TR/Q = P (demand curve); MR = TRn − TRn−1; TR = ΣMR.',
                        'MR = AR(e − 1)/e: e > 1 → MR +; e = 1 → MR 0, TR max; e < 1 → MR −.', 'Shut down if P < minimum AVC; profit maximum where MR = MC and MC cuts MR from below.'],
            'remember': ['Perfect competition: AR = MR = P (horizontal); TR a straight line from the origin.', 'Falling AR: MR below AR, TR an inverted U.', 'Minimum AVC = shut-down price; minimum ATC = break-even (normal profit) price.'],
            'traps': ['MR is not TR ÷ Q — that is AR.', 'TR is maximum where MR = 0, not where profit is maximum.', 'Shut-down (short run, temporary) is not exit (long run).', 'Sunk fixed cost does not decide whether to produce in the short run.']},
        'quickref': [{'k': 'TR', 'v': 'P × Q'}, {'k': 'AR', 'v': 'TR ÷ Q = P'}, {'k': 'MR', 'v': 'ΔTR ÷ ΔQ; MRn = TRn − TRn−1; TR = ΣMR'},
                     {'k': 'MR and elasticity', 'v': 'MR = AR × (e − 1)/e ; e = AR ÷ (AR − MR)'}, {'k': 'Shut-down rule', 'v': 'Produce only if P ≥ minimum AVC'}, {'k': 'Profit maximum', 'v': 'MR = MC, MC cutting MR from below'}],
        'viva': viva, 'cases': cases,
    }
