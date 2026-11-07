"""CA Foundation · Paper 4 Business Economics · Chapter 4 Price Determination in Different Markets · Unit 3 Price-Output Determination under Different Market Forms.
Original explanations, numbers and questions. Every figure is computed in code and re-checked by tools/ca_validate.py."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch04-u03'


def Q(i, q, o, a, e, c, d='core', check=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'concept': c, 'difficulty': d}
    if check: m['check'] = check
    return m


def M(i, q, o, a, e, d='moderate', check=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if check: m['check'] = check
    return m


def build():
    # ---------- Illustration 1: competitive firm's cost table ----------
    c1 = Checks()
    qs = [0, 10, 20, 30, 40, 50, 60]
    tcs = [150, 270, 360, 470, 620, 850, 1140]
    rows1 = [['0', '150', '150', '0', '—', '—', '—']]
    for i in range(1, 7):
        tvc = c1.add(f'{tcs[i]}-150', f'TVC at {qs[i]}')
        avc = c1.add(f'({tcs[i]}-150)/{qs[i]}', f'AVC at {qs[i]}')
        afc = c1.add(f'150/{qs[i]}', f'AFC at {qs[i]}')
        mc = c1.add(f'({tcs[i]}-{tcs[i-1]})/10', f'MC between {qs[i-1]} and {qs[i]}')
        rows1.append([str(qs[i]), str(tcs[i]), '150', str(tvc), str(avc), str(afc), str(mc)])
    t1 = table(['Output (Q)', 'TC (₹)', 'TFC (₹)', 'TVC (₹)', 'AVC (₹)', 'AFC (₹)', 'MC per unit (₹)'], rows1, num=[0, 1, 2, 3], title='Costs of Chai Point Kiosk (price taker)')
    prof15 = c1.add('15*40-620', 'profit at price ₹15 and 40 units')
    atc40 = c1.add('620/40', 'ATC at 40 units')
    prof23 = c1.add('23*50-850', 'profit at price ₹23 and 50 units')
    tvc_cov = c1.add('15*40-470', 'contribution at ₹15 (TR - TVC)')

    # ---------- Illustration 2: normal vs supernormal profit ----------
    c2 = Checks()
    imp = c2.add('100000*10/100', 'implicit cost of own capital')
    tc2 = c2.add('40000+10000', 'total economic cost')
    atc2 = c2.add('50000/2000', 'ATC per unit')
    sn = c2.add('(28-25)*2000', 'supernormal profit at ₹28')
    ls = c2.add('(23-25)*2000', 'loss at ₹23')
    acc_prof = c2.add('28*2000-40000', 'accounting profit at ₹28')

    # ---------- Illustration 3: monopoly vs competition ----------
    c3 = Checks()
    qm = c3.add('(100-20)/(2*2)', 'monopoly output: MR = 100 - 4Q = 20')
    pm = c3.add('100-2*20', 'monopoly price')
    prm = c3.add('(60-20)*20', 'monopoly profit (AC = MC = 20)')
    qc = c3.add('(100-20)/2', 'competitive output where P = MC')
    pc = c3.add('100-2*40', 'competitive price')
    em = c3.add('60/(60-20)', 'elasticity at monopoly equilibrium = AR/(AR - MR)')

    # ---------- Illustration 4: price discrimination ----------
    c4 = Checks()
    mra = c4.add('48*(1.6-1)/1.6', 'MR in market A at single price')
    mrb = c4.add('48*(4-1)/4', 'MR in market B at single price')
    gain = c4.add('36-18', 'gain from shifting one unit A to B')
    qa = c4.add('(50-10)/4', 'QA where MRA = 50 - 4QA = MC 10')
    pa = c4.add('50-2*10', 'PA')
    qb = c4.add('(30-10)/2', 'QB where MRB = 30 - 2QB = 10')
    pb = c4.add('30-10', 'PB')
    ea = c4.add('30/(30-10)', 'elasticity in A at equilibrium')
    eb = c4.add('20/(20-10)', 'elasticity in B at equilibrium')
    totq = c4.add('10+10', 'total output')
    trd = c4.add('30*10+20*10', 'TR with discrimination')

    # ---------- written questions ----------
    w1 = Checks()
    w1q = w1.add('(120-30)/(2*3)', 'monopoly output: MR = 120 - 6Q = 30')
    w1p = w1.add('120-3*15', 'monopoly price')
    w1pr = w1.add('(75-30)*15', 'profit with AC = MC = 30')
    w1qc = w1.add('(120-30)/3', 'competitive output P = MC')
    w2 = Checks()
    w2_tr = w2.add('18*300', 'TR')
    w2_tc = w2.add('300*21', 'TC')
    w2_tvc = w2.add('300*16', 'TVC')
    w2_loss = w2.add('5400-6300', 'loss if it produces')
    w2_tfc = w2.add('6300-4800', 'TFC (loss if shut)')
    w3 = Checks()
    w3a = w3.add('60*(1.5-1)/1.5', 'MR in A')
    w3b = w3.add('60*(3-1)/3', 'MR in B')
    w3g = w3.add('40-20', 'gain per unit shifted')

    # ---------- case ----------
    k = Checks()
    kq = k.add('(400-40)/(2*4)', 'case: Q where MR = 400 - 8Q = 40')
    kp = k.add('400-4*45', 'case: price')
    kpr = k.add('(220-40)*45-1500', 'case: profit = (P - AVC) Q - fixed cost')
    ke = k.add('220/(220-40)', 'case: elasticity at equilibrium')

    concepts = [
        {'id': 'c1', 'title': 'Perfect competition — features', 'body': [
            'Features: (i) a very large number of buyers and sellers, each too small to affect price; (ii) a homogeneous product — the output of every firm is a perfect substitute for every other, so one price rules; (iii) free entry and exit — no legal, cost or market barriers. A market with only these three features is called pure competition (the essence is absence of any monopoly element).',
            'Perfect competition adds: (iv) perfect knowledge of prices, quantities and quality among buyers and sellers; (v) negligible transaction costs; (vi) every firm (and every buyer) is a price taker — if a seller asks more than the ruling price, he loses his customers. Textbooks also assume perfect mobility of factors, no government interference and no collusion.',
            'Truly perfect markets are rare (many call them a myth), but farm produce in a large mandi, shares and foreign exchange on exchanges, and gold or silver come close.'],
         'analogy': 'Hundreds of potato sellers in one mandi, all with the same potatoes and all asking ₹20 a kg — anyone asking ₹22 sells nothing; nobody needs to ask ₹18.',
         'work': 'In commodity businesses (steel billets, cotton, basic chemicals) margins depend almost entirely on cost control because the firm cannot set its price — a key point in credit appraisal.'},
        {'id': 'c2', 'title': 'Equilibrium of the industry and of the firm', 'body': [
            'Industry equilibrium: total quantity supplied by all firms equals total quantity demanded; the price at that point is the market price, which every firm must accept.',
            'Because the firm can sell any quantity at that price, its demand (AR) curve is a horizontal line at the market price — perfectly elastic. Every extra unit adds exactly the price to revenue, so P = AR = MR. The firm decides only how much to produce, not the price.',
            'Firm equilibrium (maximum profit) needs two conditions: (i) MR = MC, which for a competitive firm means P = MC; and (ii) MC must cut MR from below (MC rising). Where MC cuts MR while falling, profit is at a minimum, not a maximum.',
            'Short-run supply curve: at each price the firm produces where P = MC, so its MC curve traces how much it supplies at each price — but only the part of the MC curve above minimum AVC. Below minimum AVC it supplies nothing.'],
         'analogy': 'The price line is a flat shelf at the market price; the firm keeps adding units until the cost of the next unit climbs above that shelf.',
         'work': 'Capacity-expansion proposals in commodity firms are tested by asking: at the forecast market price, where does our marginal cost cross it? That gives the realistic output, not the nameplate capacity.'},
        {'id': 'c3', 'title': 'Short run: supernormal profit, normal profit or loss', 'body': [
            'Normal profit is the minimum return an entrepreneur must earn to stay in the business — the opportunity cost of his own capital and effort. Economists include it in cost (as an implicit cost), so when AR = ATC the firm earns normal profit, i.e. zero economic profit.',
            'Supernormal (economic) profit: AR > ATC at the equilibrium output; profit per unit = AR − ATC and total profit = (AR − ATC) × Q.',
            'Loss: AR < ATC at the equilibrium output. The firm still produces (it is minimising loss) as long as price covers AVC, because it recovers some fixed cost. If price is below minimum AVC, it shuts down temporarily and loses only its fixed cost.',
            'So in the short run a competitive firm in equilibrium may earn supernormal profit, normal profit or a loss — it depends on where the market price stands relative to its ATC and AVC.'],
         'analogy': 'A chartered bus: if fares cover diesel and the driver (variable cost), it runs even when the loan instalment (fixed cost) is not fully covered; if fares do not cover diesel, it stays in the depot.',
         'work': 'CAs often explain to clients the gap between accounting profit and economic profit: a business showing a "profit" may still not cover the return the owner could earn on his capital elsewhere.'},
        {'id': 'c4', 'title': 'Long run: firm and industry under perfect competition', 'body': [
            'In the long run firms can change their plant size and firms can enter or leave. Supernormal profits attract new firms; industry supply rises, price falls (and costs may rise as factor prices go up) until the profit disappears. Losses drive firms out; supply falls and price rises until the remaining firms earn normal profit.',
            'Long-run equilibrium of the firm: price equals the minimum of the long-run average cost curve, where the LAC is tangent to the horizontal demand line: P = LMC = LAC. At that point the plant is worked at its optimal capacity, so SMC = LMC = SAC = LAC = P = MR.',
            'Long-run equilibrium of the industry needs three things: every firm maximises profit; every firm earns only normal profit, so nobody wants to enter or leave; and industry quantity supplied equals quantity demanded.',
            'Results (optimal allocation of resources): output produced at the lowest possible cost (optimum firms); consumers pay a price equal to marginal cost (P = MC); plants used to full capacity (MC = AC, no waste); only normal profit (AR = AC); and an optimum number of firms. In short: LAR = LMR = P = LMC = LAC.'],
         'analogy': 'A food street where one new dish earns big profits: within months ten stalls copy it, the price drifts down, and soon each stall earns just enough to stay open.',
         'work': 'When valuing a firm in a highly competitive industry, analysts assume excess returns will fade towards the cost of capital over time — the long-run "normal profit" result in practice.'},
        {'id': 'c5', 'title': 'Monopoly — features and how it arises', 'body': [
            'Monopoly means a single seller of a product that has no close substitute. Features: (1) one firm, so firm and industry are the same; (2) strong barriers to entry — economic, legal, institutional or artificial; (3) no close substitutes, so cross elasticity with other goods is zero or very small and its demand curve falls steeply; (4) market power — the ability to set price above marginal cost. The monopolist is a price maker.',
            'Sources of monopoly (barriers): control of a scarce input, resource or technology; a unique product that is hard or costly to copy; exclusive rights granted by government; patents and copyrights; business combinations and cartels; huge start-up costs or costly know-how; natural monopoly (economies of scale so large that one firm can supply the whole market at a lower cost than two or more, as in power distribution, piped gas or telephone lines); long-standing goodwill; strict licensing and regulation; and predatory tactics such as limit pricing.',
            'Pure monopoly is rare because monopolies are usually regulated or prohibited. In India, rail transport by Indian Railways and nuclear power generation by the government are examples.'],
         'analogy': 'The only bridge across a river: everyone who wants to cross pays the toll you set — but set it too high and fewer people cross.',
         'work': 'Competition-law work (merger filings, abuse-of-dominance analysis) starts with these questions: how big are the entry barriers and how close are the substitutes?'},
        {'id': 'c6', 'title': 'Monopoly revenue curves and equilibrium', 'body': [
            'The monopolist\'s demand curve is the market demand curve, and since it charges one price for all units, AR = price, so the demand curve is its AR curve. To sell more it must lower the price on all units, so MR < AR.',
            'For a straight-line demand curve: both AR and MR slope downwards; MR has twice the slope of AR and lies halfway between the price axis and the AR curve (if P = a − bQ, then MR = a − 2bQ); AR is never zero at a positive price but MR can be zero or negative.',
            'Equilibrium (short run): output where MR = MC with MC cutting MR from below; the price is then read off the demand (AR) curve above that output. Profit per unit = AR − ATC. A monopolist does not always earn profit: if demand is weak and ATC > AR it makes a loss; it continues in the short run only if AVC is covered.',
            'Long run: the monopolist adjusts plant size. It will not stay if it makes losses, and because entry is blocked it can keep supernormal profit. It need not produce at the minimum point of LAC — it may operate at a sub-optimal scale.',
            'Because MC > 0, MR = MC requires MR > 0, so a monopolist always produces on the elastic part of the demand curve (e > 1). Monopoly may be simple (one price to all buyers) or discriminating (different prices to different buyers).'],
         'analogy': 'MR is a shadow that falls twice as fast as the AR line it follows.',
         'work': 'Regulators setting tariffs for utilities compare the price a monopolist would charge (MR = MC) with cost-based prices; CAs prepare the cost-of-service data used in these tariff petitions.'},
        {'id': 'c7', 'title': 'Price discrimination', 'body': [
            'Price discrimination means selling the same product to different buyers at different prices for reasons not linked to differences in cost — e.g. a doctor charging a rich patient more, cheaper electricity for rural homes than for factories, student subscriptions, off-peak call rates, dumping abroad at lower prices.',
            'Conditions: (I) the seller must have some monopoly (price-setting) power — necessary but not sufficient; (II) the market must be divisible into sub-markets; (III) price elasticity must differ between sub-markets; (IV) no arbitrage — buyers in the cheap market cannot resell in the dear market. It cannot persist under perfect competition.',
            'Degrees (Pigou): first degree — each buyer is charged the maximum he is willing to pay, taking away the entire consumer surplus (negotiated fees, auctions, bid-and-offer); second degree — price differs with the quantity bought (cheaper family packs, slab tariffs for water or electricity), taking part of the consumer surplus; third degree — the market is split by location, age, use or segment (domestic vs commercial power, senior-citizen fares, dumping).',
            'Equilibrium: MR in each market = AR(e − 1)/e. At a single price, MR is higher in the more elastic market, so the seller shifts output there until MRs are equal. Total output is fixed where the aggregate MR (horizontal sum of the sub-market MRs) = MC; output is split so that MRA = MRB = MC; the price is higher in the less elastic market.',
            'Objectives: maximum profit, disposing of surplus stock, economies of scale, capturing foreign markets, and equity through pricing. Effects: lower consumer surplus and welfare loss since price exceeds MC; but it can keep some firms or essential services (e.g. railways) viable, spread peak-load demand, and let poorer buyers purchase at lower prices.'],
         'analogy': 'One flight, one seat type, many fares: the business traveller who must fly tomorrow (inelastic) pays far more than the student who booked months ahead (elastic).',
         'work': 'Transfer-pricing, dynamic pricing and customer-segment profitability analyses in industry all rest on these conditions — and auditors check that discounts by segment comply with competition and consumer law.'},
        {'id': 'c8', 'title': 'Economic effects of monopoly', 'body': [
            'Criticisms: loss of productive and allocative efficiency; higher prices and lower output than under competition; unjustified long-run economic profit; price above MC, so consumer surplus is transferred to the monopolist; restricted consumer choice (sovereignty); costly efforts to keep rivals out raise average cost; political influence to win favourable laws; weak incentive to innovate; power to pay suppliers less; and X-inefficiency — managerial slack where competition is absent.',
            'Because of these effects, governments try to prevent monopolies from forming and regulate those that exist.'],
         'analogy': 'A monopolist is like the only canteen in a remote campus: prices high, menu short, and little reason to improve the food.',
         'work': 'Due-diligence reports flag a target\'s dominance not only as a strength but also as a regulatory risk (possible penalties or price controls).'},
        {'id': 'c9', 'title': 'Monopolistic competition', 'body': [
            'A blend of monopoly and perfect competition, very common in practice (soaps, clothing, restaurants, salons, retail shops in cities). Features: (i) a large number of independent sellers, each with a small market share; (ii) product differentiation — real or imagined, through brand, design, packaging, features, service — which creates brand loyalty and some monopoly power; (iii) relatively free entry and exit; (iv) non-price competition — heavy advertising, product development, better distribution and after-sales service, because price wars are risky; selling costs are vital.',
            'Each firm is a price maker for its own brand and faces a downward-sloping but fairly elastic demand curve — the less its product is differentiated, the more elastic the curve.',
            'Short run: MR = MC (MC cutting MR from below); the firm may earn supernormal profit or make a loss.',
            'Long run: supernormal profits attract new brands, each firm\'s demand shrinks and becomes tangent to its average cost curve (AR = AC), so only normal profit is earned; persistent losses make firms leave until the rest earn normal profit. The tangency lies on the falling part of the AC curve, so each firm produces less than the output at minimum AC — it has excess capacity. Expanding output to lower AC is irrational because price would have to fall more than cost.'],
         'blocks': [table(['Point', 'Perfect competition', 'Monopoly', 'Monopolistic competition'], [
             ['Sellers', 'Very many; firm = price taker', 'One; firm = industry', 'Many; some control over price'],
             ['Product', 'Homogeneous', 'No close substitute', 'Differentiated, close substitutes'],
             ['Entry', 'Free', 'Blocked', 'Free'],
             ['Demand curve of firm', 'Horizontal (perfectly elastic)', 'Downward sloping, relatively inelastic', 'Downward sloping, more elastic'],
             ['MR vs AR', 'MR = AR', 'MR below AR, twice as steep', 'MR below AR, twice as steep'],
             ['Price vs MC', 'P = MC', 'P > MC', 'P > MC'],
             ['Long-run profit', 'Normal', 'Supernormal possible', 'Normal'],
             ['Selling costs', 'None', 'Low (informative)', 'High (persuasive)'],
             ['Long-run output', 'At minimum AC (optimum)', 'On falling part of AC', 'On falling part of AC — excess capacity'],
             ['Resource allocation', 'Efficient', 'Inefficient', 'Inefficient; waste on advertising'],
         ], title='Three market forms compared')],
         'analogy': 'A street of cafés: each serves "its own" coffee and can charge a little more, but if one charges too much, customers walk next door.',
         'work': 'Marketing-spend budgets that a CA reviews in consumer businesses are the non-price competition of this market form — tested for return like any other investment.'},
        {'id': 'c10', 'title': 'Oligopoly — types and features', 'body': [
            'Oligopoly is "competition among the few": a few large sellers (roughly two to ten) of homogeneous or differentiated products, where each firm\'s policy depends partly on what it expects its close rivals to do (Stigler). Examples: cold drinks, automobiles, airlines, petroleum refining, mobile telephony.',
            'Types: pure (homogeneous product, e.g. steel, aluminium) vs differentiated (e.g. talcum powder); open (entry possible) vs closed (entry restricted); collusive (firms agree on price/output) vs competitive; partial (one dominant firm acts as price leader) vs full (no price leader); syndicated (sales through a central syndicate) vs organised (a central association fixes prices, output and quotas).',
            'Characteristics: a few large firms with a big market share and strong entry barriers; strategic interdependence — any move by one firm provokes reactions; great importance of advertising and selling costs, with firms avoiding price cuts that could trigger a price war; and group behaviour — there is no single accepted theory of how the group will act.',
            'Game theory (Von Neumann and Morgenstern, 1944) is used to analyse such strategic choices under uncertainty.'],
         'analogy': 'Three petrol pumps at one crossing: none dares to change its price without first guessing what the other two will do.',
         'work': 'In industries like telecom or aviation, analysts read every price move as part of a strategic game — and CAs in those firms model competitor reactions in their pricing papers.'},
        {'id': 'c11', 'title': 'Oligopoly — price and output models', 'body': [
            'Because rivals react, an oligopolist has no single definite demand curve, so price and output cannot be found without assumptions about behaviour. Three broad approaches: (i) firms ignore interdependence — demand becomes definite and MR = MC gives the output; (ii) firms predict rivals\' reactions — Cournot (output is the decision variable, no collusion), Stackelberg (a leader fixes output first, followers adjust), Bertrand (price is the decision variable); (iii) firms collude and act like one monopoly to maximise joint profit, sharing output or profit — a cartel (generally illegal; OPEC is the classic example). A cartel earns monopoly-like profit, especially when demand is inelastic, if members stick to the agreement.',
            'Price leadership: by a dominant firm (it sets the price that maximises its profit after allowing for the output of the small fringe firms — "live and let live"); by a low-cost firm (it sets a price that still leaves some profit for followers); and barometric (an old, experienced or respected firm reads market conditions and announces changes that others accept).',
            'Kinked demand curve (Paul Sweezy): explains why oligopoly prices are sticky. Each firm believes rivals will match a price cut but will not follow a price rise. So above the ruling price its demand is highly elastic (a rise loses many customers to rivals) and below it demand is inelastic (a cut gains few customers because rivals cut too). The demand curve has a kink at the prevailing price and each firm sticks to that price even when costs or demand change somewhat.',
            'Other market forms: duopoly — only two sellers (a special case of oligopoly); monopsony — a single buyer, mostly of a factor; oligopsony — a few large buyers; bilateral monopoly — one buyer facing one seller.'],
         'analogy': 'Kinked demand: raise your price and the crowd walks to your rivals; cut it and your rivals cut too — so you leave the price board alone.',
         'work': 'Competition authorities investigate parallel price moves for cartels; CAs supporting such inquiries analyse cost and price data to tell genuine price leadership from collusion.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'A price-taking kiosk: output, profit and shut-down price', 'difficulty': 'moderate', 'minutes': 12,
         'q': 'Chai Point Kiosk is a price taker. Its total cost at outputs 0, 10, 20, 30, 40, 50 and 60 cups an hour is ₹150, 270, 360, 470, 620, 850 and 1,140. Complete TFC, TVC, AVC, AFC and MC. (a) At a price of ₹15 a cup, how many cups should it sell and what is its profit or loss? (b) At ₹23? (c) Below what price should it shut down?',
         'solution': [t1, wn('(a) Price ₹15', f'P = MR = ₹15 = MC at 40 cups (MC rising). TR = 600, TC = 620, so a loss of ₹{-prof15} (ATC = ₹{atc40} > price). It still produces because TR exceeds TVC by ₹{tvc_cov}, which covers part of the fixed cost of ₹150.'),
                      wn('(b) Price ₹23', f'MC = ₹23 at 50 cups → profit = 1,150 − 850 = {R(prof23)} (supernormal).'), wn('(c)', 'Minimum AVC is ₹10.5 (at 20 cups) — the shut-down price. Below it the kiosk should stop serving for the time being.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Normal profit is a cost', 'difficulty': 'core', 'minutes': 7,
         'q': 'Meher invests ₹1,00,000 of her own money in a candle unit. Explicit costs of making 2,000 boxes a month are ₹40,000. She could earn 10% a month on her money elsewhere. Find ATC (economic) and state the type of profit at prices of ₹25, ₹28 and ₹23 a box.',
         'solution': [table(['Item', '₹'], [['Explicit costs', '40,000'], ['Implicit cost (normal profit) 10% of ₹1,00,000', inr(imp)], ['Total economic cost', inr(tc2)], ['ATC = 50,000 ÷ 2,000', str(atc2)]], title='Economic cost'),
                      ul([f'₹25 = ATC → normal profit (zero economic profit).', f'₹28 > ATC → supernormal profit of ₹3 a box = {R(sn)} a month (accounting profit would show {R(acc_prof)}, because it ignores the implicit cost).', f'₹23 < ATC → economic loss of {R(-ls)}.'])],
         'checks': c2},
        {'id': 'i3', 'title': 'Monopoly equilibrium vs the competitive outcome', 'difficulty': 'hard', 'minutes': 10,
         'q': 'A monopolist faces demand P = 100 − 2Q and has constant MC = AC = ₹20. Find its output, price and profit, and compare with the output and price if the industry were perfectly competitive (P = MC).',
         'solution': [wn('Monopoly', f'MR = 100 − 4Q (twice the slope of AR). MR = MC → 100 − 4Q = 20 → Q = {qm}; P = 100 − 40 = ₹{pm}; profit = (60 − 20) × 20 = {R(prm)}.'),
                      wn('Competition', f'P = MC → 100 − 2Q = 20 → Q = {qc}; P = ₹{pc}.'),
                      p(f'The monopolist produces half the competitive output at three times the price. Elasticity at the monopoly point = AR ÷ (AR − MR) = 60 ÷ 40 = {em} > 1 — the monopolist operates on the elastic part of demand.')],
         'checks': c3},
        {'id': 'i4', 'title': 'Third-degree price discrimination', 'difficulty': 'hard', 'minutes': 12,
         'q': '(a) A firm charges a single price of ₹48 in two markets where the elasticities are 1.6 (market A) and 4 (market B). Find MR in each market and explain what the firm should do. (b) Later the firm estimates PA = 50 − 2QA and PB = 30 − QB, with constant MC = ₹10. Find the profit-maximising quantities and prices in each market.',
         'solution': [wn('(a)', f'MRA = 48 × 0.6/1.6 = ₹{mra}; MRB = 48 × 3/4 = ₹{mrb}. Moving one unit from A to B loses ₹{mra} but gains ₹{mrb} — a net gain of ₹{gain}. The firm should shift sales to B (price in A rises, in B falls) until MRA = MRB.'),
                      wn('(b)', f'MRA = 50 − 4QA = 10 → QA = {qa}, PA = ₹{pa}. MRB = 30 − 2QB = 10 → QB = {qb}, PB = ₹{pb}. Total output {totq} units; MRA = MRB = MC = ₹10; total revenue {R(trd)}.'),
                      p(f'Elasticity at equilibrium: A = 30 ÷ 20 = {ea}; B = 20 ÷ 10 = {eb}. The higher price is charged in the less elastic market (A).')],
         'checks': c4},
        {'id': 'i5', 'title': 'Reading oligopoly behaviour', 'difficulty': 'moderate', 'minutes': 6,
         'q': 'Classify each situation: (a) Three cement makers in a region meet and agree output quotas; (b) the largest steel maker announces a price revision and smaller mills follow within a day; (c) an airline cuts fares and two rivals match it the same evening, but when it raised fares last month nobody followed; (d) a single sugar mill is the only buyer of cane in a district.',
         'solution': [table(['Situation', 'Market form / model', 'Why'], [
             ['(a)', 'Collusive oligopoly — cartel', 'Explicit agreement to fix output; acts like a joint monopoly (generally illegal)'],
             ['(b)', 'Price leadership by a dominant firm', 'Followers accept the leader\'s price'],
             ['(c)', 'Kinked demand curve behaviour', 'Rivals match cuts but not rises, so prices stay sticky'],
             ['(d)', 'Monopsony', 'Single buyer of a factor/input'],
         ])]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Pricing a new route: segment the market', 'role': 'CA in industry — revenue management at a regional airline',
         'situation': 'The airline launches a new route. Business travellers book late and rarely change plans; leisure travellers book early and compare fares.',
         'steps': ['Check the conditions for price discrimination: pricing power on the route, separable segments (booking date, flexibility), different elasticities, and no resale (tickets are named).', 'Set higher fares for late, flexible tickets (inelastic segment) and lower advance fares (elastic segment).', 'Allocate seats so that the marginal revenue from the last seat in each fare bucket is roughly equal.', 'Review for consumer-law and disclosure compliance.'],
         'takeaway': 'Third-degree price discrimination raises revenue when segments differ in elasticity and resale is impossible.', 'think': 'Why would the scheme fail if tickets could be freely transferred?', 'answer': 'Buyers would purchase cheap advance fares and resell them to business travellers — arbitrage would destroy the price difference.'},
        {'id': 'j2', 'title': 'Advising a café owner on the long run', 'role': 'CA in practice advising a small business',
         'situation': 'A client\'s specialty café earned high profits last year. Five similar cafés have opened nearby and footfall is falling.',
         'steps': ['Explain monopolistic competition: free entry erodes supernormal profit until only normal profit remains.', 'Recommend strengthening differentiation (menu, ambience, loyalty programme) rather than a price war.', 'Budget selling costs carefully and track their return.', 'Plan for capacity: in the long run the café may run below full capacity — keep fixed commitments flexible.'],
         'takeaway': 'In monopolistic competition, profits are temporary unless differentiation is continually renewed.'},
        {'id': 'j3', 'title': 'Spotting a possible cartel in tender data', 'role': 'Forensic accountant assisting a public-sector buyer',
         'situation': 'Bids from four suppliers for the same item move up together each year, and the lowest bidder rotates.',
         'steps': ['Tabulate bid prices against input-cost indices to see if increases exceed cost changes.', 'Look for bid rotation, identical figures and unusually narrow spreads.', 'Distinguish lawful price leadership (followers react to a public price) from collusion (agreed prices or quotas).', 'Report the pattern to management for referral to the competition authority if warranted.'],
         'takeaway': 'Collusive oligopoly leaves fingerprints in pricing data — economics tells you what to look for.'},
    ]

    mcqs = [
        Q('m1', 'Which feature, together with many sellers and a homogeneous product, defines "pure" competition?', ['Free entry and exit', 'Perfect knowledge', 'Zero transport cost', 'Government price control'], 0, 'Pure competition = large numbers, homogeneous product, free entry/exit. Perfect competition adds perfect knowledge, low transaction costs etc.', 'c1'),
        Q('m2', 'A firm under perfect competition is a:', ['Price taker', 'Price maker', 'Price leader', 'Price discriminator'], 0, 'It accepts the market price set by industry demand and supply.', 'c1'),
        Q('m3', 'Under perfect competition, the demand curve facing an individual firm is:', ['Horizontal at the market price', 'Downward sloping', 'Vertical', 'Kinked'], 0, 'Perfectly elastic: the firm sells any quantity at the ruling price.', 'c2'),
        Q('m4', 'For a perfectly competitive firm:', ['P = AR = MR', 'P > MR', 'AR > MR', 'MR = 0'], 0, 'Each extra unit sells at the same price.', 'c2'),
        Q('m5', 'The second condition for a firm\'s equilibrium is that:', ['MC must cut MR from below', 'MC must cut MR from above', 'AR must equal AC', 'MR must be zero'], 0, 'Where MC cuts MR from above (falling MC), profit is minimum, not maximum.', 'c2'),
        Q('m6', 'The short-run supply curve of a competitive firm is:', ['The part of its MC curve above minimum AVC', 'Its entire MC curve', 'Its AVC curve', 'Its ATC curve'], 0, 'Below minimum AVC the firm produces nothing.', 'c2', 'moderate'),
        Q('m7', 'When AR = ATC at the equilibrium output, a firm earns:', ['Normal profit', 'Supernormal profit', 'A loss', 'Monopoly profit'], 0, 'Normal profit is included in ATC; economic profit is zero.', 'c3'),
        Q('m8', 'A competitive firm making a loss in the short run will continue production if:', ['Price is at least equal to AVC', 'Price is below AVC', 'Price is below AFC', 'MR is zero'], 0, 'Covering variable cost and part of fixed cost reduces the loss compared with shutting down.', 'c3'),
        Q('m9', 'A competitive firm produces 400 units where P = MC = ₹30. Its ATC at 400 units is ₹26. Its supernormal profit is:', ['₹1,600', '₹12,000', '₹10,400', '₹400'], 0, '(AR − ATC) × Q = (30 − 26) × 400 = ₹1,600. ₹12,000 is TR and ₹10,400 is TC.', 'c3', 'moderate', '(30-26)*400'),
        Q('m10', 'In long-run equilibrium under perfect competition:', ['P = LMC = LAC (minimum)', 'P > LAC', 'P = LMC > LAC', 'P < LAC'], 0, 'Entry/exit drives price to the minimum of LAC: SMC = LMC = SAC = LAC = P = MR.', 'c4'),
        Q('m11', 'Supernormal profits of competitive firms in the short run will, in the long run, lead to:', ['Entry of new firms and a fall in price', 'Exit of firms and a rise in price', 'Formation of a cartel', 'Permanent supernormal profit'], 0, 'Free entry raises industry supply and lowers price until only normal profit remains.', 'c4'),
        Q('m12', 'Which is NOT a result of long-run equilibrium under perfect competition?', ['Excess capacity in each firm', 'Production at minimum average cost', 'Price equal to marginal cost', 'Only normal profit'], 0, 'Excess capacity is a feature of monopolistic competition.', 'c4', 'moderate'),
        Q('m13', 'The fundamental cause of monopoly is:', ['Barriers to entry', 'Large number of buyers', 'Homogeneous products', 'Perfect knowledge'], 0, 'Other firms cannot enter the market.', 'c5'),
        Q('m14', 'A natural monopoly arises when:', ['Economies of scale are so large that one firm can supply the market at lowest cost', 'The government nationalises an industry', 'A firm owns a patent', 'Consumers prefer one brand'], 0, 'Duplicating infrastructure (pipes, wires) would be wasteful.', 'c5'),
        Q('m15', 'The cross elasticity of demand between a monopolist\'s product and other goods is:', ['Zero or very small', 'Infinite', 'Greater than one', 'Negative and large'], 0, 'No close substitutes exist.', 'c5'),
        Q('m16', 'For a straight-line demand curve facing a monopolist, the MR curve:', ['Has twice the slope of AR and lies halfway between AR and the price axis', 'Coincides with AR', 'Lies above AR', 'Is horizontal'], 0, 'If P = a − bQ, MR = a − 2bQ.', 'c6'),
        Q('m17', 'A monopolist faces P = 80 − 2Q and constant MC = ₹20. Its profit-maximising output is:', ['15 units', '30 units', '20 units', '10 units'], 0, 'MR = 80 − 4Q = 20 → Q = 15 (price ₹50). 30 units is the competitive output where P = MC.', 'c6', 'hard', '(80-20)/4'),
        Q('m18', 'A monopolist always operates where the price elasticity of demand is:', ['Greater than one', 'Less than one', 'Equal to zero', 'Equal to one'], 0, 'MR = MC > 0 requires MR > 0, i.e. e > 1.', 'c6', 'moderate'),
        Q('m19', 'In the long run, a monopolist:', ['Can continue to earn supernormal profit because entry is blocked', 'Always produces at minimum LAC', 'Always earns only normal profit', 'Always makes a loss'], 0, 'Entry barriers protect profit; it need not reach minimum LAC.', 'c6'),
        Q('m20', 'Which is NOT a condition for price discrimination?', ['Equal price elasticity in all sub-markets', 'Some monopoly power', 'Market divisible into sub-markets', 'No resale between sub-markets'], 0, 'Elasticities must differ; with equal elasticities discrimination gives no gain.', 'c7'),
        Q('m21', 'Under price discrimination, a higher price is charged in the market where demand is:', ['Less elastic', 'More elastic', 'Perfectly elastic', 'Unit elastic'], 0, 'Buyers with inelastic demand do not cut purchases much at a higher price.', 'c7'),
        Q('m22', 'At a single price of ₹60, elasticities are 1.5 in market X and 3 in market Y. MR in market Y is:', ['₹40', '₹20', '₹30', '₹180'], 0, 'MR = 60 × (3 − 1)/3 = ₹40 (MR in X = 60 × 0.5/1.5 = ₹20).', 'c7', 'moderate', '60*(3-1)/3'),
        Q('m23', 'Charging each buyer the maximum he is willing to pay, so that the whole consumer surplus is taken, is:', ['First-degree price discrimination', 'Second-degree price discrimination', 'Third-degree price discrimination', 'Dumping'], 0, 'Pigou\'s first degree — e.g. negotiated professional fees, auctions.', 'c7'),
        Q('m24', 'Lower per-unit prices for bigger packs, or slab rates for electricity, are examples of:', ['Second-degree price discrimination', 'First-degree price discrimination', 'Third-degree price discrimination', 'Perfect competition'], 0, 'Price varies with the quantity bought.', 'c7'),
        Q('m25', 'A discriminating monopolist is in equilibrium when:', ['MRA = MRB = MC of total output', 'PA = PB = MC', 'ARA = ARB', 'MRA = MRB = 0'], 0, 'Total output where aggregate MR = MC, split so that each market\'s MR equals that MC.', 'c7', 'moderate'),
        Q('m26', '"X-inefficiency" associated with monopoly refers to:', ['Loss of managerial efficiency where competition is weak or absent', 'Excess capacity', 'Price discrimination', 'Inefficiency in foreign trade'], 0, 'Managers face little pressure to control cost.', 'c8'),
        Q('m27', 'In the long run, a firm under monopolistic competition earns:', ['Only normal profit, with excess capacity', 'Supernormal profit at minimum AC', 'Losses', 'Normal profit at minimum AC'], 0, 'Free entry removes profit; tangency is on the falling part of AC.', 'c9'),
        Q('m28', 'The most important form of competition under monopolistic competition is:', ['Non-price competition such as advertising and product differentiation', 'Price wars', 'Collusion', 'Price leadership'], 0, 'Price cuts risk price wars; firms compete through brands and selling costs.', 'c9'),
        Q('m29', 'The most important feature of oligopoly is:', ['Interdependence in decision-making', 'Homogeneous product', 'Free entry', 'Absence of selling costs'], 0, 'Each firm must allow for rivals\' reactions.', 'c10'),
        Q('m30', 'In the kinked demand curve model, an oligopolist believes rivals will:', ['Follow a price cut but not a price rise', 'Follow a price rise but not a cut', 'Follow both', 'Follow neither'], 0, 'Hence demand is elastic above the kink and inelastic below it, making prices sticky.', 'c11'),
        Q('m31', 'The kinked demand curve hypothesis was given by:', ['Paul Sweezy', 'Augustin Cournot', 'Joseph Bertrand', 'Heinrich von Stackelberg'], 0, 'Sweezy\'s model explains price rigidity in oligopoly.', 'c11'),
        Q('m32', 'In which oligopoly model is output the decision variable and firms do not collude?', ['Cournot', 'Bertrand', 'Kinked demand', 'Cartel'], 0, 'Cournot: output; Bertrand: price; Stackelberg: leader sets output first.', 'c11', 'moderate'),
        Q('m33', 'An old, experienced firm that reads market conditions and announces price changes followed by others is a case of:', ['Barometric price leadership', 'Dominant-firm price leadership', 'Low-cost price leadership', 'Cartel'], 0, 'The barometric leader acts like a barometer of market conditions.', 'c11'),
        Q('m34', 'A market with a single buyer and a single seller is:', ['Bilateral monopoly', 'Monopsony', 'Duopoly', 'Oligopsony'], 0, 'Monopoly on the selling side + monopsony on the buying side.', 'c11'),
        Q('m35', 'A competitive firm\'s TC at outputs 30 and 40 units is ₹470 and ₹620 respectively. Its MC per unit over this range is:', ['₹15', '₹150', '₹15.50', '₹11.75'], 0, 'MC = ΔTC/ΔQ = (620 − 470)/10 = ₹15. ₹150 is ΔTC, not per unit; ₹15.50 is ATC at 40 units (620/40); ₹11.75 wrongly divides TC at 30 units by 40. (If the market price were ₹15, P = MC here.)', 'c2', 'moderate', '(620-470)/10'),
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'hard', 'pad': 'text',
         'q': 'A monopolist faces the demand P = 120 − 3Q and has constant MC = AC = ₹30. (a) Find the profit-maximising output, price and profit. (b) What would output be under perfect competition? (c) Comment on the result.',
         'model': [wn('(a)', f'TR = 120Q − 3Q², so MR = 120 − 6Q. MR = MC → 120 − 6Q = 30 → Q = {w1q}; P = 120 − 45 = ₹{w1p}; profit = (75 − 30) × 15 = {R(w1pr)}.'),
                   wn('(b)', f'P = MC → 120 − 3Q = 30 → Q = {w1qc}.'), p('(c) The monopolist restricts output to half the competitive level and charges a price well above MC — the allocative inefficiency of monopoly; consumer surplus is transferred to the monopolist.')],
         'scheme': [{'id': 's1', 'pt': 'MR derived (twice the slope of AR)', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Output and price', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Profit', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'Competitive output and comment', 'm': 1.5, 'skill': 'analysis'}],
         'remarks': ['Many candidates set P = MC for the monopolist — that is the competitive rule.'], 'mistakes': ['Reading the price from the MR curve instead of the demand curve.', 'Forgetting to multiply margin by quantity for profit.'], 'tips': ['Write: output from MR = MC; price from the demand curve.'], 'checks': w1},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'A competitive firm is in short-run equilibrium producing 300 units at a market price of ₹18. Its ATC at that output is ₹21 and AVC is ₹16. Compute its profit or loss, its fixed cost, and advise whether it should continue production.',
         'model': [table(['Item', '₹'], [['TR (300 × 18)', inr(w2_tr)], ['TC (300 × 21)', inr(w2_tc)], ['Profit / (loss)', inr(w2_loss)], ['TVC (300 × 16)', inr(w2_tvc)], ['TFC = TC − TVC', inr(w2_tfc)]]),
                   p(f'If it shuts down it loses the whole fixed cost of {R(w2_tfc)}; by producing it loses only {R(-w2_loss)}, since price (₹18) exceeds AVC (₹16). It should continue in the short run.')],
         'scheme': [{'id': 's1', 'pt': 'Loss computed', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'Fixed cost computed', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Compares price with AVC', 'm': 1, 'skill': 'analysis'}, {'id': 's4', 'pt': 'Decision with reason', 'm': 1, 'skill': 'conclusion'}],
         'remarks': ['Good answers compare the two losses explicitly.'], 'mistakes': ['Advising shut-down because price < ATC.'], 'tips': ['Shut-down test = price vs AVC; profit test = price vs ATC.'], 'checks': w2},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'A firm sells the same product at a single price of ₹60 in market A (e = 1.5) and market B (e = 3). (a) Compute MR in each market. (b) Explain how the firm can raise profit by discriminating. (c) State any two conditions required.',
         'model': [wn('(a)', f'MRA = 60 × (1.5 − 1)/1.5 = ₹{w3a}; MRB = 60 × (3 − 1)/3 = ₹{w3b}.'),
                   p(f'(b) A unit moved from A to B loses ₹{w3a} of revenue in A but gains ₹{w3b} in B — a gain of ₹{w3g} with no change in total cost. The firm keeps shifting sales until MRA = MRB (= MC); price then rises in A (less elastic) and falls in B (more elastic).'),
                   p('(c) Any two: monopoly power; separable markets; different elasticities; no resale (arbitrage) between markets.')],
         'scheme': [{'id': 's1', 'pt': 'MR in both markets', 'm': 1.5, 'skill': 'computation'}, {'id': 's2', 'pt': 'Explains transfer until MRs equal; higher price in less elastic market', 'm': 1.5, 'skill': 'analysis'},
                    {'id': 's3', 'pt': 'Two valid conditions', 'm': 1, 'skill': 'concept'}],
         'remarks': ['Candidates often reverse the direction of transfer.'], 'mistakes': ['Saying the higher price goes to the more elastic market.'], 'tips': ['Higher MR = more elastic market = where extra units go.'], 'checks': w3},
    ]

    viva = [
        V('v1', 'What are the features of perfect competition?',
          'Perfect competition has a very large number of buyers and sellers, a homogeneous product, and free entry and exit of firms. In addition there is perfect knowledge of market conditions, negligible transaction costs, and every firm is a price taker that must accept the market price.',
          [P('p1', 'Very many buyers and sellers', 2, 'large number|many buyer|many seller|numerous|very many|lot of seller|lot of buyer'),
           P('p2', 'Homogeneous / identical product', 3, 'homogeneous|homogenous|identical|same product|perfect substitut|uniform product|standardised|standardized'),
           P('p3', 'Free entry and exit', 2, 'free entry|freedom of entry|no barrier|no entry barrier|enter and exit freely|enter freely|easy entry|free to enter'),
           P('p4', 'Perfect knowledge; firm is a price taker', 3, 'perfect knowledge|perfect information|full knowledge|full information|complete information|complete knowledge', 'price taker|accept the price|accept market price|accepts the price|cannot influence price|no control over price|cannot affect price', min=1)], 'c1'),
        V('v2', 'Describe the long-run equilibrium of a firm under perfect competition.',
          'In the long run, supernormal profit attracts new firms and losses drive firms out, so price settles where long run average cost is at its lowest. The firm earns only normal profit, and price equals long run marginal cost equals long run average cost. The firm produces at optimum capacity, at the lowest cost.',
          [P('p1', 'Entry and exit remove supernormal profit / losses', 3, 'new firm|entry|enter|firms come in|firms join', 'exit|leave|firms go out|quit|losses drive', min=1),
           P('p2', 'Only normal profit', 3, 'normal profit|zero economic profit|no supernormal|no abnormal|zero profit'),
           P('p3', 'P = LMC = LAC at minimum LAC (optimum)', 4, 'minimum|lowest|optimum|least cost', 'long run average cost|lac|average cost', 'marginal cost|lmc|mc', min=2)], 'c4'),
        V('v3', 'Why is marginal revenue less than average revenue for a monopolist?',
          'A monopolist faces the downward sloping market demand curve. To sell one more unit it has to lower the price, and the lower price applies to all the units it sells, not just the extra unit. So the addition to total revenue is less than the price. For a straight line demand curve, the MR curve is twice as steep as the AR curve and lies halfway between it and the price axis.',
          [P('p1', 'Downward-sloping demand — must lower price to sell more', 4, 'lower the price|reduce the price|cut the price|lower price|reduce price|cut price|price has to fall|price must fall|price must be reduced|downward slop|price fall'),
           P('p2', 'Lower price applies to all units, not just the extra one', 4, 'all units|all the units|every unit|previous units|earlier units|whole output|existing units|other units|units already|entire output'),
           P('p3', 'MR twice as steep / halfway', 2, 'twice|double|two times|halfway|half way|2 times')], 'c6'),
        V('v4', 'What conditions are necessary for price discrimination?',
          'First, the seller must have some monopoly power to set prices. Second, the market must be divisible into two or more sub-markets. Third, the price elasticity of demand must be different in the sub-markets. Fourth, there should be no resale or arbitrage from the cheaper market to the dearer market.',
          [P('p1', 'Monopoly power / control over price', 2, 'monopoly power|control over price|price setting|market power|price maker|control over supply|monopoly element|some monopoly'),
           P('p2', 'Market divisible into sub-markets', 2, 'divid|separat|sub market|submarket|segment|split'),
           P('p3', 'Different elasticities in sub-markets', 3, 'different elasticit|elasticity differ|elasticities differ|differ in elasticity|different price elasticit|elasticity must be different|elasticity should be different|elasticity is different|unequal elasticit|elasticities are different'),
           P('p4', 'No resale / arbitrage', 3, 'no resale|cannot resell|not possible to resell|no arbitrage|resale not possible|cannot be resold|no reselling|not be resold|arbitrage not|prevent resale|without resale')], 'c7'),
        V('v5', 'Why is there excess capacity under monopolistic competition in the long run?',
          'Under monopolistic competition free entry wipes out supernormal profit, so in the long run the downward sloping demand curve of each firm just touches its average cost curve. Because the demand curve slopes down, this tangency is on the falling part of the average cost curve, to the left of minimum average cost. So each firm produces less than the optimum output and has unused or excess capacity.',
          [P('p1', 'Free entry → only normal profit; AR tangent to AC', 3, 'tangent|touch|ar equal ac|ar equals ac|average revenue equal average cost|normal profit|zero profit'),
           P('p2', 'Demand curve slopes downward', 2, 'downward slop|slopes down|down slop|downward sloping|negatively slop|falling demand curve'),
           P('p3', 'Equilibrium on falling part of AC, left of minimum', 3, 'falling part|declining part|falling portion|declining portion|downward part|before minimum|left of minimum|not at minimum|above minimum|not minimum|less than minimum|short of minimum'),
           P('p4', 'Output less than optimum → unused capacity', 2, 'less than optimum|below optimum|less than full|unused|excess capacity|idle capacity|spare capacity|under-utili|underutili|not optimum|suboptimal|sub optimal')], 'c9'),
        V('v6', 'Explain the kinked demand curve model of oligopoly.',
          'The kinked demand curve model was given by Paul Sweezy to explain price rigidity in oligopoly. Each firm believes that rivals will follow a price cut but will not follow a price rise. So the demand curve is elastic above the prevailing price and inelastic below it, giving a kink at the current price. Since neither a rise nor a cut helps, the firm sticks to the prevailing price, which is why prices are sticky.',
          [P('p1', 'Sweezy; explains price rigidity', 2, 'sweezy|rigid|sticky|stable price|price stability|inflexible'),
           P('p2', 'Rivals follow a price cut but not a price rise', 3, ALT('{c} follow', 'follow {c}', c=['cut', 'cuts', 'reduce', 'reduction', 'lower', 'decrease', 'fall']), ALT('{r} not follow', 'not follow {r}', '{r} will not', '{r} not match', 'not match {r}', "{r} don't follow", 'but not a price {r}', 'but not price {r}', 'not follow', 'not match', r=['rise', 'raise', 'raises', 'increase', 'increases', 'hike'])),
           P('p3', 'Demand elastic above the kink (price rise loses many customers)', 3, 'elastic above|elastic for price rise|elastic for a rise|elastic upper|upper part elastic|upper portion elastic|upper segment elastic|upper part is elastic|upper portion is elastic|upper segment is elastic|elastic for price increase|elastic above the kink|elastic in upper|above the kink is elastic|above kink elastic|above the current price is elastic|above current price elastic|above the prevailing price is elastic'),
           P('p4', 'Demand inelastic below the kink (price cut gains few customers)', 2, 'inelastic below|inelastic lower|inelastic for price cut|inelastic for a cut|lower part inelastic|lower portion inelastic|lower segment inelastic|lower part is inelastic|lower portion is inelastic|lower segment is inelastic|below inelastic|inelastic in lower|less elastic below')], 'c11'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Jaldhara Water Supply — a local monopoly', 'difficulty': 'hard',
        'case': ('Jaldhara is the only licensed supplier of piped drinking water in a hill town. Its monthly demand (in thousand kilolitres) is P = 400 − 4Q, where P is ₹ per kilolitre. '
                 'It has a constant average variable cost (= marginal cost) of ₹40 a kilolitre and fixed cost of ₹1,500 thousand a month. The municipality is considering separate tariffs for hotels and households.'),
        'mcqs': [
            M('k1a', 'Jaldhara\'s profit-maximising output (thousand kilolitres) is:', ['45', '90', '50', '40'], 0, f'MR = 400 − 8Q = 40 → Q = {kq}. (90 is the output where P = MC.)', 'hard', '(400-40)/(2*4)'),
            M('k1b', 'The price it will charge (₹ per kilolitre) is:', ['220', '40', '180', '310'], 0, f'From the demand curve: P = 400 − 4 × 45 = ₹{kp}.', 'moderate', '400-4*45'),
            M('k1c', 'Its monthly profit (₹ thousand) is:', ['6,600', '8,100', '9,900', '1,500'], 0, f'(P − AVC) × Q − fixed cost = (220 − 40) × 45 − 1,500 = {inr(kpr)}.', 'hard', '(220-40)*45-1500'),
            M('k1d', 'If separate tariffs are allowed and hotels have less elastic demand than households, Jaldhara will:', ['Charge hotels a higher tariff than households', 'Charge households a higher tariff', 'Charge both the same tariff', 'Charge both a tariff equal to MC'], 0, 'Third-degree discrimination: the higher price goes to the less elastic segment; hotels cannot resell piped water, so arbitrage is not possible.', 'moderate'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch04', 'n': 3, 'title': 'Price Output Determination under Different Market Forms',
        'outcomes': ['Explain short-run and long-run equilibrium of a firm and an industry under perfect competition, including supernormal profit, normal profit, losses and the shut-down point.',
                     'Explain how monopolies arise, derive the monopolist\'s AR and MR, and determine its price, output and profit; analyse price discrimination and the economic effects of monopoly.',
                     'Explain short-run and long-run equilibrium under monopolistic competition, including excess capacity, and compare the three market forms.',
                     'Describe the types and characteristics of oligopoly, and the main models — collusion and cartels, price leadership and the kinked demand curve — and other market forms.'],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 70, 'practice': 60}, 'prereq': ['fnd-p4-ch04-u01', 'fnd-p4-ch04-u02', 'fnd-p4-ch03-u02'],
                 'exam_tip': 'This is the heaviest unit of the chapter: expect 5–8 MCQs. Know the comparison table cold, the equilibrium conditions (MR = MC, MC rising), long-run results (normal profit, excess capacity), conditions and degrees of price discrimination, and the kinked demand curve logic.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Perfect competition: many firms, homogeneous product, free entry, perfect knowledge; firm is a price taker with P = AR = MR.',
                        'Firm equilibrium: MR = MC with MC cutting MR from below; MC above minimum AVC = short-run supply curve.',
                        'Short run: supernormal profit (AR > ATC), normal profit (AR = ATC) or loss (AR < ATC, but ≥ AVC).',
                        'Long run (PC): entry/exit → normal profit; SMC = LMC = SAC = LAC = P = MR at minimum LAC; optimum firms.',
                        'Monopoly: single seller, no close substitute, barriers; AR = demand; MR twice as steep; MR = MC; operates where e > 1; supernormal profit can last.',
                        'Price discrimination: needs monopoly power, separable markets, different elasticities, no resale; MRA = MRB = MC; higher price where demand is less elastic. Degrees: first, second, third (Pigou).',
                        'Monopolistic competition: many firms, differentiated products, free entry, selling costs; long run normal profit with excess capacity.',
                        'Oligopoly: few firms, interdependence, selling costs, group behaviour; models — Cournot, Stackelberg, Bertrand, cartel; price leadership (dominant, low-cost, barometric); kinked demand (Sweezy) explains sticky prices.'],
            'remember': ['Normal profit is part of cost (implicit cost).', 'Monopolist need not produce at minimum LAC; a competitive firm must in the long run.', 'Duopoly = 2 sellers; monopsony = 1 buyer; oligopsony = few buyers; bilateral monopoly = 1 buyer + 1 seller.'],
            'traps': ['A monopolist is not certain to make profits — demand and cost decide.', 'Monopolistic competition ≠ monopoly: entry is free.', 'Under discrimination the higher price goes to the LESS elastic market.', 'Kinked demand: rivals follow a cut, not a rise — not the other way round.']},
        'quickref': [{'k': 'Firm equilibrium', 'v': 'MR = MC; MC cuts MR from below'}, {'k': 'Perfect competition (LR)', 'v': 'SMC = LMC = SAC = LAC = P = MR'},
                     {'k': 'Monopoly MR (linear)', 'v': 'P = a − bQ → MR = a − 2bQ'}, {'k': 'MR in a sub-market', 'v': 'MR = P(e − 1)/e'},
                     {'k': 'Discrimination equilibrium', 'v': 'Aggregate MR = MC; MRA = MRB = MC'}, {'k': 'Monopolistic competition (LR)', 'v': 'AR = AC (tangency), MR = MC, excess capacity'},
                     {'k': 'Kinked demand', 'v': 'Elastic above the kink, inelastic below; prices sticky (Sweezy)'}],
        'viva': viva, 'cases': cases,
    }
