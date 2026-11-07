"""CA Foundation · Paper 4 Business Economics · Chapter 2 Theory of Demand and Supply · Unit 1 Law of Demand and Elasticity of Demand.
Original explanations, examples and questions (ICAI structure and scope only). Every figure is computed below."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch02-u01'
EXW = ['tea', 'coffee', 'pepsi', 'coke', 'example', 'butter', 'car', 'petrol']


def Q(mid, q, opts, ans, ex, c, d='core', check=None):
    x = {'id': mid, 'q': q, 'options': opts, 'answer': ans, 'explain': ex, 'concept': c, 'difficulty': d}
    if check: x['check'] = check
    return x


def build():
    # ---------- i1 market demand ----------
    c1 = Checks()
    prices = [50, 40, 30, 20, 10]
    A = [2, 4, 6, 8, 10]; B = [0, 3, 5, 9, 12]; Cc = [1, 2, 4, 5, 8]
    mkt = [c1.add(f'{a}+{b}+{c}', f'market demand at ₹{p}') for p, a, b, c in zip(prices, A, B, Cc)]

    # ---------- i2 percentage method ----------
    c2 = Checks()
    ep_pct = c2.add('((600-500)/500)/((40-36)/40)', 'price elasticity, percentage method')
    tr_old = c2.add('40*500', 'outlay at ₹40'); tr_new = c2.add('36*600', 'outlay at ₹36')

    # ---------- i3 arc ----------
    c3 = Checks()
    ep_arc = c3.add('((300-200)/(300+200))*((60+80)/(80-60))', 'arc elasticity (mid-point)')
    ep_arc_base_old = c3.add('((300-200)/200)/((80-60)/80)', 'elasticity using old values as base')
    ep_arc_base_new = c3.add('round(((300-200)/300)/((80-60)/60),2)', 'elasticity using new values as base (rising price from 60 to 80)')

    # ---------- i4 point / geometric ----------
    c4 = Checks()
    q40 = c4.add('1200-20*40', 'Q at P = 40'); e40 = c4.add('20*40/400', 'point elasticity at P = 40')
    q30 = c4.add('1200-20*30', 'Q at P = 30'); e30 = c4.add('20*30/600', 'point elasticity at P = 30')
    q15 = c4.add('1200-20*15', 'Q at P = 15'); e15 = c4.add('round(20*15/900,2)', 'point elasticity at P = 15')
    pmax = c4.add('1200/20', 'price at which Q = 0 (price-axis intercept)')

    # ---------- i5 total outlay ----------
    c5 = Checks()
    cases_to = [('Wheat flour', 30, 1000, 27, 1050), ('Earphones', 800, 150, 640, 220), ('Notebooks', 50, 400, 40, 500)]
    to_rows = []
    for nm, p1, q1, p2, q2 in cases_to:
        t1 = c5.add(f'{p1}*{q1}', f'{nm} outlay before'); t2 = c5.add(f'{p2}*{q2}', f'{nm} outlay after')
        verdict = 'Inelastic (Ep < 1)' if t2 < t1 else 'Elastic (Ep > 1)' if t2 > t1 else 'Unitary (Ep = 1)'
        to_rows.append([nm, f'{p1} → {p2}', f'{q1} → {q2}', t1, t2, verdict])

    # ---------- i6 income, cross, advertisement ----------
    c6 = Checks()
    ei = c6.add('((22-20)/20)/((50000-40000)/40000)', 'income elasticity (rice)')
    ei_lux = c6.add('((9-6)/6)/((50000-40000)/40000)', 'income elasticity (dining out)')
    ei_inf = c6.add('((8-10)/10)/((50000-40000)/40000)', 'income elasticity (coarse grain)')
    ec_sub = c6.add('((60-50)/50)/((240-200)/200)', 'cross elasticity coffee w.r.t. tea price')
    ec_comp = c6.add('((900-1000)/1000)/((120-100)/100)', 'cross elasticity of printer demand w.r.t. cartridge price')
    ea = c6.add('((12500-10000)/10000)/((300000-200000)/200000)', 'advertisement elasticity')

    # ---------- questions ----------
    cq1 = Checks()
    q1_e = cq1.add('((1800-1500)/1500)/((100-90)/100)', 'q1 Ep percentage method')
    q1_t1 = cq1.add('100*1500', 'q1 TR before'); q1_t2 = cq1.add('90*1800', 'q1 TR after')
    cq2 = Checks()
    q2_arc = cq2.add('round(((240-160)/(240+160))*((25+35)/(35-25)),2)', 'q2 arc elasticity')
    cq3 = Checks()
    q3_q = cq3.add('2000-40*30', 'q3 Q at P=30'); q3_e = cq3.add('40*30/800', 'q3 point elasticity at P=30')
    q3_pm = cq3.add('2000/40/2', 'q3 price where Ep = 1 (mid-point)')
    q3_ei = cq3.add('((960-800)/800)/((60000-50000)/50000)', 'q3 income elasticity')

    # ---------- case ----------
    k = Checks()
    k_ep = k.add('round(((5600-4000)/4000)/((250-200)/250),2)', 'case: Ep percentage method (price cut 250→200)')
    k_tr1 = k.add('250*4000', 'case TR before'); k_tr2 = k.add('200*5600', 'case TR after')
    k_ea = k.add('((4600-4000)/4000)/((150000-100000)/100000)', 'case: advertisement elasticity')
    k_ei = k.add('((4400-4000)/4000)/((33000-30000)/30000)', 'case: income elasticity')

    # ---------- MCQ numbers ----------
    m = Checks()

    concepts = [
        {'id': 'c1', 'title': 'Meaning of demand',
         'body': ['In economics, demand is not mere desire. It is the desire for a good backed by the ability and the willingness to pay for it. A student who wants a car but cannot pay has a wish, not demand; a rich person who can pay but does not want it has no demand either.',
                  'Two points make the definition precise. First, quantity demanded is always stated at a particular price — at another price the quantity will be different. Second, demand is a flow: it is the quantity bought per unit of time (per day, week, month or year), not a one-off purchase. "Demand for milk is 5,000 litres" means nothing; "5,000 litres a day at ₹60 a litre" is a proper statement.'],
         'analogy': 'Demand is a wish with a wallet and a decision: all three must be present.',
         'work': 'Sales budgets prepared by CAs are always stated as quantity per period at an assumed price — exactly the economist\'s definition of demand.'},
        {'id': 'c2', 'title': 'What determines demand',
         'body': ['(1) Price of the good itself — usually more is bought at a lower price. (2) Prices of related goods — substitutes (tea and coffee; a rise in the price of one raises demand for the other) and complements (car and petrol, printer and cartridge; a rise in the price of one lowers demand for the other). (3) Disposable income of the consumer — for normal goods demand rises with income; for inferior goods (coarse grains, cheap substitutes) demand falls as income rises because buyers shift to better goods.',
                  '(4) Tastes and preferences — shaped by fashion, habit, advertising and social influence. Special effects: the demonstration effect (copying others\' consumption), the bandwagon effect (buying because others are buying), the snob effect (buying less of a thing because many others have it), and the Veblen effect (wanting a costly good because its high price signals status). (5) Consumers\' expectations — of future prices and incomes; if prices are expected to rise, people buy more now.',
                  '(6) Other factors — size of population; composition of population (age, gender, urban/rural mix); level of national income and its distribution (more equal distribution raises demand for wage goods, unequal distribution raises demand for luxuries); availability of consumer credit; and interest rates (cheap loans raise demand for durables like houses and cars).'],
         'analogy': 'Price is the steering wheel of demand; the other determinants are the road, weather and passengers — change any of them and the journey changes.',
         'work': 'When a CA reviews a client\'s sales forecast, the assumptions to test are exactly these determinants: price plans, competitors\' prices, income growth, consumer trends, credit availability and interest rates.'},
        {'id': 'c3', 'title': 'The demand function',
         'body': ['A demand function states demand as a function of its determinants: Dx = f(Px, Py, M, T, A, U), where Px is the good\'s own price, Py prices of related goods, M money income, T tastes and preferences, A advertisement, and U other factors.',
                  'Since all determinants cannot be studied together, economists change one at a time and hold the rest constant (ceteris paribus). Holding everything except Px constant gives the price-demand relationship — the law of demand. A simple linear form is Q = a − bP: "a" captures the effect of all other determinants and "b" shows how much quantity falls when price rises by ₹1.'],
         'analogy': 'A demand function is a recipe: the dish (quantity demanded) depends on several ingredients, and to taste the effect of one spice you keep the others fixed.',
         'work': 'Demand forecasting models built by analysts (often by regression) are estimated demand functions; their coefficients feed revenue projections in project reports.'},
        {'id': 'c4', 'title': 'The law of demand: schedule and curve',
         'body': ['Law of demand: other things remaining the same, the quantity demanded of a good rises when its price falls and falls when its price rises — price and quantity demanded are inversely related.',
                  'Assumptions ("other things") include: no change in consumers\' income, tastes and preferences, prices of related goods, expectations, and the size and composition of population.',
                  'An individual demand schedule is a table of prices and the quantities one buyer will purchase. A market demand schedule adds, at each price, the quantities demanded by all buyers in the market (horizontal summation). Plotting either gives a demand curve that slopes downward from left to right, with price on the Y-axis and quantity on the X-axis.'],
         'analogy': 'A demand curve is like a see-saw: when price goes up, quantity comes down.',
         'work': 'Retail chains test the law of demand with "price-off" weeks; the extra units sold at the lower price are used to judge whether the discount paid for itself.'},
        {'id': 'c5', 'title': 'Why the demand curve slopes downward',
         'body': ['(1) Law of diminishing marginal utility (Marshall): each additional unit gives less extra satisfaction, so a consumer buys more only if the price falls. (2) Price effect = substitution effect + income effect (Hicks and Allen): when price falls, the good becomes cheaper relative to substitutes, so buyers switch towards it (substitution effect); the fall also raises real income (purchasing power), so more can be bought (income effect). For a normal good both work in the same direction.',
                  '(3) Arrival of new consumers: a lower price brings in buyers who could not afford it before. (4) Different uses: at a lower price a good is put to more uses (electricity used for lighting, then also for heating and cooking).'],
         'analogy': 'When biryani gets cheaper, you eat more because the next plate is still worth the lower price (utility), you switch from pizza (substitution), you feel richer (income), and your friends who couldn\'t afford it join in (new buyers).',
         'work': 'Pricing teams estimate how much of a sales jump after a price cut comes from new customers versus existing ones buying more — a practical use of these reasons.'},
        {'id': 'c6', 'title': 'Exceptions to the law of demand',
         'body': ['(1) Conspicuous (prestige) goods — diamonds, luxury watches, designer bags: bought to display wealth, so a higher price can raise demand (Veblen effect). (2) Giffen goods — named after Sir Robert Giffen, who observed that when the price of bread rose, poor families bought more of it; a very inferior staple that takes a large share of a poor family\'s budget can show a rising demand curve because the negative income effect outweighs the substitution effect. (3) Conspicuous necessities — goods like smartphones or televisions that have become social necessities and are bought even at higher prices. (4) Expectations of future prices — if prices are rising and expected to rise further, people buy more now even at the higher price.',
                  '(5) Incomplete information and irrational behaviour — buyers may judge quality by price or act on impulse. (6) Necessaries — demand for essentials like salt or basic medicines hardly changes with price. (7) Speculative goods — shares, gold or land: rising prices may trigger more buying in the hope of further rise.',
                  'Important: all Giffen goods are inferior goods, but not every inferior good is a Giffen good.'],
         'analogy': 'Exceptions are like people who leave a restaurant when prices fall — they think cheap means bad — or rush in when prices rise because they fear missing out.',
         'work': 'Luxury brands avoid discounting for exactly this reason: a lower price can damage the "status" value and reduce demand. CAs advising such brands treat price as a positioning tool, not only a revenue tool.'},
        {'id': 'c7', 'title': 'Movement along vs shift of the demand curve',
         'body': ['Expansion and contraction (change in quantity demanded) — caused only by a change in the good\'s own price, other things constant; shown as a movement along the same demand curve. A fall in price → expansion (move down the curve); a rise in price → contraction (move up the curve).',
                  'Increase and decrease (change in demand) — caused by a change in any other determinant (income, tastes, prices of related goods, expectations, population, credit). The whole curve shifts: rightward for an increase (more bought at the same price, or the same quantity at a higher price) and leftward for a decrease.',
                  'Examples: a rise in income shifts the demand curve for a normal good to the right but for an inferior good to the left; a rise in the price of tea shifts the coffee curve right; a rise in petrol prices shifts the demand curve for petrol cars left.'],
         'blocks': [table(['Cause', 'Term used', 'On the graph'], [['Fall in own price', 'Expansion (extension) of demand', 'Downward movement along the same curve'], ['Rise in own price', 'Contraction of demand', 'Upward movement along the same curve'],
                                                                ['Favourable change in another determinant', 'Increase in demand', 'Curve shifts to the right'], ['Unfavourable change in another determinant', 'Decrease in demand', 'Curve shifts to the left']], title='Four terms students mix up')],
         'analogy': 'Moving along the curve is walking along a road; a shift is the road itself being moved to a new place.',
         'work': 'In variance analysis, a CA separates a sales change into a price effect (movement) and a market/volume effect from other causes (shift) — the same distinction.'},
        {'id': 'c8', 'title': 'Price elasticity of demand: meaning and degrees',
         'body': ['Price elasticity of demand (Ep) measures how strongly quantity demanded responds to a change in price: Ep = percentage change in quantity demanded ÷ percentage change in price = (ΔQ/Q) × (P/ΔP). Because price and quantity move in opposite directions the result is negative; by convention the minus sign is dropped and the absolute value is read.',
                  'Degrees: perfectly inelastic (Ep = 0) — quantity does not change at all, vertical curve; relatively inelastic (0 < Ep < 1) — quantity changes by a smaller percentage than price; unitary elastic (Ep = 1) — equal percentages, curve is a rectangular hyperbola; relatively elastic (Ep > 1) — quantity changes by a larger percentage; perfectly elastic (Ep = ∞) — horizontal curve, the smallest price rise wipes out demand.',
                  'Elasticity is not the same as slope. Slope is ΔP/ΔQ in absolute units; elasticity uses percentages and depends on where you are on the curve. Comparing curves through the same point, the steeper one is less elastic there.'],
         'analogy': 'Elasticity is how far a rubber band stretches for the same pull. A thick band (salt) barely moves; a thin one (a particular brand of chips) stretches a lot.',
         'work': 'Before recommending a price increase, a CA estimates elasticity: if demand is inelastic, revenue will rise; if elastic, it will fall.'},
        {'id': 'c9', 'title': 'Measuring price elasticity: percentage, point, geometric and arc methods',
         'body': ['Percentage (proportionate) method: Ep = (ΔQ/Q) ÷ (ΔP/P), with the original price and quantity as base.',
                  'Point elasticity: for a very small change at a point on the curve, Ep = −(dQ/dP) × (P/Q). For a linear demand Q = a − bP, dQ/dP = −b, so Ep = b × P/Q. It is the price-quantity ratio at the point multiplied by the reciprocal of the slope.',
                  'Geometric method on a straight-line demand curve: at any point R, Ep = lower segment ÷ upper segment (the part of the line below R to the quantity axis divided by the part above R to the price axis). So elasticity is infinite where the line meets the price axis, greater than 1 above the mid-point, exactly 1 at the mid-point, less than 1 below it, and zero where it meets the quantity axis — even though the slope is constant.',
                  'Arc elasticity (mid-point method) for large changes between two points: Ep = [(Q2 − Q1) ÷ (Q2 + Q1)] × [(P2 + P1) ÷ (P2 − P1)], absolute value. Using the averages as base gives the same answer whether price rises or falls; the arc value lies between the point elasticities at the two ends (not necessarily in the middle).'],
         'blocks': [table(['Method', 'Formula', 'Use when'], [['Percentage', '(ΔQ/Q) ÷ (ΔP/P)', 'A single change from a known starting point'], ['Point', '−(dQ/dP) × P/Q', 'A demand equation is given, or the change is very small'],
                                                        ['Geometric', 'Lower segment ÷ upper segment', 'A straight-line demand curve is drawn'], ['Arc (mid-point)', '[(Q2 − Q1)/(Q2 + Q1)] × [(P2 + P1)/(P2 − P1)]', 'Two points with a large change; direction should not matter'],
                                                        ['Total outlay', 'Direction of change in P × Q', 'Only to say elastic / unitary / inelastic']], title='Choosing the method')],
         'analogy': 'Percentage method measures from where you started; the arc method measures from the middle of the bridge, so walking either way gives the same length.',
         'work': 'Analysts use arc elasticity on before-and-after data from a price change, and point elasticity when they have an estimated demand equation.'},
        {'id': 'c10', 'title': 'Total outlay (total revenue) method',
         'body': ['Total outlay (TO) by buyers = total revenue (TR) of sellers = P × Q. Watch how it changes when price changes:',
                  'If price falls and TO rises (or price rises and TO falls) — price and outlay move in opposite directions — demand is elastic (Ep > 1). If TO stays the same — demand is unitary elastic (Ep = 1). If price falls and TO falls (or price rises and TO rises) — same direction — demand is inelastic (Ep < 1).',
                  'Limitation: this method only tells whether demand is elastic, unitary or inelastic; it does not give the exact coefficient.',
                  'Business use: if demand is elastic, a price cut raises revenue; if inelastic, a price rise raises revenue. This is why the elasticity of demand matters so much for pricing.'],
         'analogy': 'Think of a shopkeeper\'s cash box: if a discount fills it more, customers are price-sensitive (elastic); if it empties it, they are not (inelastic).',
         'work': 'Revenue impact analysis for a tariff change, a toll revision or a GST rate change uses exactly this logic.'},
        {'id': 'c11', 'title': 'Determinants of price elasticity of demand',
         'body': ['(1) Availability of substitutes — the more and closer the substitutes, the more elastic (one brand of soap is elastic; salt in general is inelastic). (2) Position in the consumer\'s budget — goods taking a tiny share of income (matchboxes, salt) are inelastic; big-ticket items more elastic. (3) Number of uses — a good with many uses (electricity, milk) tends to be more elastic. (4) Nature of the good — necessities are inelastic, luxuries elastic. (5) Time period — demand is more elastic in the long run, as consumers find substitutes and change habits. (6) Habits and addiction — habitual goods (tea, cigarettes) are inelastic. (7) Possibility of postponing consumption — goods whose purchase can be postponed (durables) are more elastic. (8) Price range — very high-priced and very low-priced goods tend to be inelastic; elasticity is usually greater in the middle range. (9) Complementary goods — a good used jointly with another (ink with a pen) is usually inelastic. (10) Income level of buyers — the rich are less sensitive to price changes than the poor.'],
         'analogy': 'You are flexible about which café you visit (many substitutes) but not about buying medicine your doctor prescribed (no substitute, necessity).',
         'work': 'Tax authorities prefer taxing goods with inelastic demand (fuel, tobacco) because revenue is stable; CAs advising on indirect-tax impact on sales use the same reasoning.'},
        {'id': 'c12', 'title': 'Income elasticity and cross elasticity of demand',
         'body': ['Income elasticity (Ei) = % change in quantity demanded ÷ % change in income = (ΔQ/Q) × (Y/ΔY). Ei > 1: income-elastic (luxuries) — demand grows faster than income. 0 < Ei < 1: income-inelastic (necessities such as food and medicines) — demand grows more slowly than income. Ei = 0: demand does not respond to income. Ei < 0: inferior goods — demand falls as income rises. All normal goods have positive Ei.',
                  'Link with budget share: if the share of income spent on a good stays the same as income rises, Ei = 1; if the share rises, Ei > 1; if the share falls, Ei < 1.',
                  'Cross elasticity (Ec) = % change in quantity demanded of X ÷ % change in price of Y. Positive for substitutes (tea price up → coffee demand up); negative for complements (car price up → petrol demand down); zero for unrelated goods. The larger the positive value, the closer the substitutes.'],
         'analogy': 'Income elasticity asks "what do you buy more of after a raise?"; cross elasticity asks "what happens to your coffee habit when tea gets dearer?"',
         'work': 'Retailers planning store formats for rising-income towns stock more high-Ei goods; competition authorities use cross elasticity to define a "relevant market" in merger reviews.'},
        {'id': 'c13', 'title': 'Advertisement (promotional) elasticity',
         'body': ['Advertisement elasticity of demand (Ea) measures how sales respond to a change in advertising spend: Ea = (ΔQ/Q) ÷ (ΔA/A), where A is initial advertisement expenditure and ΔA the additional spend. It is usually positive and lies between zero and infinity.',
                  'Ea = 0: sales do not respond to more advertising. 0 < Ea < 1: sales rise less than proportionately. Ea = 1: sales rise in the same proportion. Ea > 1: sales rise more than proportionately. A higher value means a more effective campaign; firms use it to decide the optimum advertising budget.'],
         'analogy': 'Advertising is like watering a plant: up to a point growth responds well, after that extra water does little.',
         'work': 'Marketing ROI reviews by finance teams compute exactly this ratio before approving the next campaign budget.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Market demand schedule from individual schedules', 'difficulty': 'core', 'minutes': 5,
         'q': 'Three buyers, Asha, Bilal and Chetan, are the only buyers of a snack. Derive the market demand schedule and state the law of demand it shows.',
         'given': [table(['Price (₹)', 'Asha', 'Bilal', 'Chetan'], [[p_, a, b, c] for p_, a, b, c in zip(prices, A, B, Cc)])],
         'solution': [table(['Price (₹)', 'Asha', 'Bilal', 'Chetan', 'Market demand'], [[p_, a, b, c, mm] for p_, a, b, c, mm in zip(prices, A, B, Cc, mkt)], title='Market demand = horizontal sum'),
                      p(f'Market demand rises from {mkt[0]} units at ₹50 to {mkt[-1]} units at ₹10 — price and quantity are inversely related, as the law of demand says. Note that Bilal enters the market only when the price falls below ₹50 — one reason the market curve slopes downward (new buyers).')],
         'checks': c1},
        {'id': 'i2', 'title': 'Price elasticity — percentage method and the revenue check', 'difficulty': 'core', 'minutes': 5,
         'q': 'When the price of a pen falls from ₹40 to ₹36, sales rise from 500 to 600 a week. Find the price elasticity of demand and confirm the result with the total outlay method.',
         'solution': [table(['Step', 'Working', 'Result'], [['% change in quantity', '(600 − 500) ÷ 500 × 100', '20%'], ['% change in price', '(36 − 40) ÷ 40 × 100', '−10%'], ['Ep', '20 ÷ 10 (sign dropped)', ep_pct]], title='Percentage method'),
                      p(f'Ep = {ep_pct} > 1, so demand is elastic. Check: outlay rises from {R(tr_old)} to {R(tr_new)} when price falls — price and outlay move in opposite directions, confirming elastic demand.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Arc elasticity — why the mid-point method is used', 'difficulty': 'moderate', 'minutes': 7,
         'q': 'At ₹80 a box, 200 boxes of dates are sold; at ₹60, 300 boxes. Find (a) arc elasticity, (b) elasticity with ₹80/200 as base, (c) elasticity with ₹60/300 as base. Comment.',
         'solution': [p(f'(a) Arc Ep = [(300 − 200) ÷ (300 + 200)] × [(60 + 80) ÷ (80 − 60)] = (100 ÷ 500) × (140 ÷ 20) = 0.2 × 7 = {ep_arc}.'),
                      p(f'(b) Base ₹80 / 200: (100 ÷ 200) ÷ (20 ÷ 80) = 0.5 ÷ 0.25 = {ep_arc_base_old}.'),
                      p(f'(c) Base ₹60 / 300 (price rising from 60 to 80): (100 ÷ 300) ÷ (20 ÷ 60) = {ep_arc_base_new}.'),
                      p(f'Comment: the simple percentage method gives {ep_arc_base_old} or {ep_arc_base_new} depending on the direction of change. The mid-point (arc) method gives one value, {ep_arc}, either way, lying between the two.')],
         'checks': c3},
        {'id': 'i4', 'title': 'Point elasticity from a demand equation', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'The demand function is Q = 1,200 − 20P. Find the point elasticity at P = ₹40, ₹30 and ₹15, and identify the price at which demand is unitary elastic.',
         'solution': [p('dQ/dP = −20, so Ep = 20 × P ÷ Q (absolute value).'),
                      table(['Price (₹)', 'Q = 1,200 − 20P', 'Ep = 20P/Q', 'Nature'], [[40, q40, e40, 'Elastic'], [30, q30, e30, 'Unitary'], [15, q15, e15, 'Inelastic']], title='Point elasticity at three prices'),
                      p(f'Demand meets the price axis at P = {pmax} (Q = 0). The mid-point of the line is at P = 30, Q = 600, where Ep = 1, exactly as the geometric rule (lower segment = upper segment) predicts. Above ₹30 demand is elastic; below it, inelastic — though the slope is the same everywhere.')],
         'checks': c4},
        {'id': 'i5', 'title': 'Total outlay method for three products', 'difficulty': 'core', 'minutes': 6,
         'q': 'Classify the price elasticity of demand for each product using the total outlay method.',
         'solution': [table(['Product', 'Price (₹)', 'Quantity', 'Outlay before (₹)', 'Outlay after (₹)', 'Elasticity'], to_rows, title='Outlay before and after'),
                      note('Price and outlay in the same direction → inelastic; opposite directions → elastic; unchanged outlay → unitary.')],
         'checks': c5},
        {'id': 'i6', 'title': 'Income, cross and advertisement elasticities', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'A household\'s monthly income rises from ₹40,000 to ₹50,000. Its monthly purchases change: rice 20 kg → 22 kg; dining out 6 → 9 times; coarse grain 10 kg → 8 kg. Separately, when the price of tea rises from ₹200 to ₹240 a kg, a café\'s coffee sales rise from 50 to 60 kg; when the price of a cartridge rises from ₹100 to ₹120, printer sales fall from 1,000 to 900. A firm raises advertising from ₹2,00,000 to ₹3,00,000 and sales rise from 10,000 to 12,500 units. Compute and interpret each elasticity.',
         'solution': [table(['Measure', 'Working', 'Value', 'Interpretation'], [
             ['Ei — rice', '(2/20) ÷ (10,000/40,000) = 0.10 ÷ 0.25', ei, 'Necessity (0 < Ei < 1)'],
             ['Ei — dining out', '(3/6) ÷ 0.25 = 0.50 ÷ 0.25', ei_lux, 'Luxury (Ei > 1)'],
             ['Ei — coarse grain', '(−2/10) ÷ 0.25', ei_inf, 'Inferior good (Ei < 0)'],
             ['Ec — coffee w.r.t. tea price', '(10/50) ÷ (40/200) = 0.2 ÷ 0.2', ec_sub, 'Positive → substitutes'],
             ['Ec — printers w.r.t. cartridge price', '(−100/1,000) ÷ (20/100)', ec_comp, 'Negative → complements'],
             ['Ea — advertising', '(2,500/10,000) ÷ (1,00,000/2,00,000) = 0.25 ÷ 0.5', ea, 'Sales rise less than proportionately']], title='Elasticities')],
         'checks': c6},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Should the gym raise its membership fee?', 'role': 'CA advising a fitness chain (small business client)',
         'situation': 'The client wants to raise the monthly fee from ₹2,000 to ₹2,200. Last year, a 5% rise led to a 9% drop in members.',
         'steps': ['Estimate elasticity from past data: 9% ÷ 5% = 1.8 — elastic.', 'Predict the effect of a 10% rise: members may fall about 18%, so revenue falls (elastic demand).', 'Check determinants: many nearby gyms (substitutes) explain the high elasticity.', 'Advise differentiation (classes, timing, trainers) to lower elasticity before raising prices, or offer an annual plan instead.'],
         'takeaway': 'With elastic demand, price rises cut revenue; reduce elasticity first by differentiating the product.',
         'think': 'Approximately what will happen to revenue if the fee rises 10% and members fall 18%?', 'answer': 'Revenue becomes about 1.10 × 0.82 = 0.902 of the old level — roughly a 10% fall.',
         'checks': [{'expr': '9/5', 'value': 1.8, 'label': 'elasticity from past data'}, {'expr': '1.10*0.82', 'value': 0.902, 'label': 'revenue factor'}]},
        {'id': 'j2', 'title': 'Forecasting demand for a premium product line', 'role': 'CA in industry — FP&A analyst at a consumer goods company',
         'situation': 'Management expects household incomes in its markets to rise 8% next year and asks for a sales forecast for premium chocolates (income elasticity about 1.5) and basic biscuits (about 0.4).',
         'steps': ['Apply income elasticity: premium chocolates +1.5 × 8% = +12%; basic biscuits +0.4 × 8% = +3.2%.', 'Adjust for planned price changes using price elasticity.', 'Shift marketing and capacity planning towards the high-Ei product.'],
         'takeaway': 'Income elasticity converts macro forecasts (income growth) into product-level sales forecasts.',
         'checks': [{'expr': '1.5*8', 'value': 12, 'label': 'chocolate growth %'}, {'expr': '0.4*8', 'value': 3.2, 'label': 'biscuit growth %'}]},
        {'id': 'j3', 'title': 'Was the advertising campaign worth it?', 'role': 'Articled assistant in a management audit',
         'situation': 'A client doubled ad spend from ₹10 lakh to ₹20 lakh; sales rose from 50,000 to 60,000 units at a contribution of ₹80 per unit.',
         'steps': ['Compute advertisement elasticity: (10,000/50,000) ÷ (10,00,000/10,00,000) = 0.2.', 'Extra contribution = 10,000 × ₹80 = ₹8,00,000, less than the extra ₹10,00,000 spent.', 'Report that the campaign did not pay for itself at the margin.'],
         'takeaway': 'Low advertisement elasticity can make additional advertising unprofitable.',
         'checks': [{'expr': '(10000/50000)/(1000000/1000000)', 'value': 0.2, 'label': 'Ea'}, {'expr': '10000*80', 'value': 800000, 'label': 'extra contribution'}]},
    ]

    mcqs = [
        Q('m1', 'Demand in economics means:', ['Desire backed by ability and willingness to pay', 'Desire for a good', 'Need for a good', 'Quantity produced'], 0, 'All three elements must be present.', 'c1'),
        Q('m2', 'Demand is a flow concept because it is expressed:', ['Per unit of time', 'At one point of time', 'Only in money', 'Without reference to price'], 0, 'Quantity per day/week/month.', 'c1'),
        Q('m3', 'Tea and coffee are:', ['Substitutes', 'Complements', 'Inferior goods', 'Giffen goods'], 0, 'They satisfy the same want; a rise in the price of one raises demand for the other.', 'c2'),
        Q('m4', 'A fall in the price of cars is likely to:', ['Increase the demand for petrol', 'Decrease the demand for petrol', 'Leave petrol demand unchanged', 'Make petrol a Giffen good'], 0, 'Cars and petrol are complements.', 'c2'),
        Q('m5', 'For an inferior good, a rise in consumer income:', ['Decreases demand', 'Increases demand', 'Does not affect demand', 'Makes demand perfectly elastic'], 0, 'Buyers shift to superior alternatives.', 'c2'),
        Q('m6', 'Buying less of a product because many others have started using it is called the:', ['Snob effect', 'Bandwagon effect', 'Demonstration effect', 'Income effect'], 0, 'Snobs want exclusivity.', 'c2', 'moderate'),
        Q('m7', 'The tendency to buy a good because others are buying it is the:', ['Bandwagon effect', 'Snob effect', 'Veblen effect', 'Substitution effect'], 0, 'Joining the crowd.', 'c2'),
        Q('m8', 'In the demand function Dx = f(Px, Py, M, T, A, U), "M" stands for:', ['Money income of the consumer', 'Market size', 'Marginal utility', 'Monopoly power'], 0, 'M is money income.', 'c3'),
        Q('m9', 'Holding all other determinants constant, the law of demand tells us that:', ['Price and quantity demanded are inversely related', 'Price and quantity demanded are directly related', 'Demand is independent of price', 'Supply creates its own demand'], 0, 'More is bought at a lower price.', 'c4'),
        Q('m10', 'The market demand curve is obtained by:', ['Horizontal summation of individual demand curves', 'Vertical summation of individual demand curves', 'Averaging individual demand curves', 'Multiplying price and quantity'], 0, 'Quantities are added at each price.', 'c4'),
        Q('m11', 'According to Hicks and Allen, the demand curve slopes downward because of:', ['Income effect and substitution effect', 'Diminishing marginal utility only', 'Supply effect', 'Government policy'], 0, 'Price effect = income effect + substitution effect.', 'c5'),
        Q('m12', 'Marshall explained the downward slope of the demand curve with the:', ['Law of diminishing marginal utility', 'Law of variable proportions', 'Indifference curve', 'Law of supply'], 0, 'The utility approach.', 'c5'),
        Q('m13', 'A Giffen good is:', ['An inferior good whose demand rises when its price rises', 'A luxury good', 'Any normal good', 'A good with perfectly elastic demand'], 0, 'The strong negative income effect outweighs the substitution effect.', 'c6'),
        Q('m14', 'Which statement is correct?', ['All Giffen goods are inferior, but not all inferior goods are Giffen goods', 'All inferior goods are Giffen goods', 'Giffen goods are luxuries', 'Giffen goods have positive income elasticity'], 0, 'Giffen is a special case of inferior goods.', 'c6', 'moderate'),
        Q('m15', 'Demand for diamonds rising when their price rises illustrates:', ['Conspicuous (Veblen) goods', 'Giffen paradox', 'Law of supply', 'Inferior goods'], 0, 'Prestige value increases with price.', 'c6'),
        Q('m16', 'A fall in the price of a good, other things constant, causes:', ['Expansion of demand — movement down the same curve', 'Increase in demand — rightward shift', 'Decrease in demand', 'Contraction of demand'], 0, 'Own-price change = movement along the curve.', 'c7'),
        Q('m17', 'A rise in consumers\' income shifts the demand curve for a normal good to the:', ['Right', 'Left', 'Neither — it is a movement along the curve', 'Vertical position'], 0, 'Income change = shift; normal good → increase.', 'c7'),
        Q('m18', 'Which of the following causes a leftward shift of the demand curve for coffee?', ['A fall in the price of tea', 'A rise in the price of tea', 'A fall in the price of coffee', 'A rise in income (coffee being normal)'], 0, 'Cheaper tea (substitute) reduces coffee demand.', 'c7', 'moderate'),
        Q('m19', 'When demand is perfectly inelastic, the demand curve is:', ['Vertical', 'Horizontal', 'A rectangular hyperbola', 'Upward sloping'], 0, 'Ep = 0 — quantity does not respond to price.', 'c8'),
        Q('m20', 'A demand curve with unitary elasticity throughout is a:', ['Rectangular hyperbola', 'Straight line', 'Vertical line', 'Horizontal line'], 0, 'P × Q constant at every point.', 'c8', 'moderate'),
        Q('m21', 'Price of a pen falls from ₹40 to ₹36 and sales rise from 500 to 600. Price elasticity (percentage method) is:', ['2', '0.5', '1', '1.5'], 0, '(100/500) ÷ (4/40) = 0.2 ÷ 0.1 = 2. 0.5 inverts the ratio.', 'c9', 'core', '((600-500)/500)/((40-36)/40)'),
        Q('m22', 'Price falls from ₹80 to ₹60 and quantity rises from 200 to 300. Arc elasticity is:', [str(ep_arc), '2', '1.5', '1'], 0, '(100/500) × (140/20) = 1.4. 2 uses the old values as base; 1 uses the new values.', 'c9', 'moderate', '((300-200)/(300+200))*((60+80)/(80-60))'),
        Q('m23', 'For the demand function Q = 1,200 − 20P, point elasticity at P = ₹40 is:', ['2', '0.5', '1', '20'], 0, 'Q = 400; Ep = 20 × 40 ÷ 400 = 2. 0.5 inverts; 20 is the slope coefficient only.', 'c9', 'hard', '20*40/(1200-20*40)'),
        Q('m24', 'On a straight-line demand curve, at the mid-point elasticity is:', ['Equal to 1', 'Zero', 'Infinite', 'Greater than 1'], 0, 'Lower segment = upper segment.', 'c9'),
        Q('m25', 'On a straight-line demand curve, the point where it meets the quantity axis has elasticity:', ['Zero', 'One', 'Infinity', 'Greater than one'], 0, 'Lower segment is zero there.', 'c9', 'moderate'),
        Q('m26', 'A fall in price leads to a fall in total expenditure on a good. Demand is:', ['Inelastic', 'Elastic', 'Unitary elastic', 'Perfectly elastic'], 0, 'Price and outlay moving in the same direction → inelastic.', 'c10'),
        Q('m27', 'Price of a toy rises from ₹100 to ₹120 and quantity falls from 300 to 250. Total outlay method shows demand is:', ['Unitary elastic', 'Elastic', 'Inelastic', 'Perfectly inelastic'], 0, 'Outlay: 100 × 300 = 30,000 and 120 × 250 = 30,000 — unchanged.', 'c10', 'moderate'),
        Q('m28', 'The main limitation of the total outlay method is that it:', ['Cannot give the exact numerical value of elasticity', 'Needs a demand equation', 'Works only for luxuries', 'Ignores price'], 0, 'It only classifies demand as elastic, unitary or inelastic.', 'c10'),
        Q('m29', 'Demand for a good with many close substitutes is likely to be:', ['Elastic', 'Inelastic', 'Perfectly inelastic', 'Zero'], 0, 'Buyers can switch easily.', 'c11'),
        Q('m30', 'Price elasticity of demand is generally greater in the:', ['Long run', 'Short run', 'Very short run', 'Same in all periods'], 0, 'Over time consumers find substitutes and change habits.', 'c11'),
        Q('m31', 'Income rises from ₹40,000 to ₹50,000 and demand for rice rises from 20 kg to 22 kg. Income elasticity is:', ['0.4', '2.5', '1', '0.1'], 0, '(2/20) ÷ (10,000/40,000) = 0.1 ÷ 0.25 = 0.4 → necessity. 2.5 inverts the ratio.', 'c12', 'core', '((22-20)/20)/((50000-40000)/40000)'),
        Q('m32', 'Income elasticity of demand for an inferior good is:', ['Negative', 'Zero', 'Between 0 and 1', 'Greater than 1'], 0, 'Demand falls as income rises.', 'c12'),
        Q('m33', 'If the proportion of income spent on a good rises as income rises, its income elasticity is:', ['Greater than one', 'Equal to one', 'Less than one but positive', 'Negative'], 0, 'Demand grows faster than income.', 'c12', 'moderate'),
        Q('m34', 'Cross elasticity of demand between two complementary goods is:', ['Negative', 'Positive', 'Zero', 'Infinite'], 0, 'Price of one up → demand for the other down.', 'c12'),
        Q('m35', 'Cartridge price rises from ₹100 to ₹120 and printer sales fall from 1,000 to 900. Cross elasticity is:', ['-0.5', '0.5', '-2', '2'], 0, '(−100/1,000) ÷ (20/100) = −0.1 ÷ 0.2 = −0.5 — complements. +0.5 drops the sign that tells the relationship.', 'c12', 'moderate', '((900-1000)/1000)/((120-100)/100)'),
        Q('m36', 'Advertising spend rises from ₹2,00,000 to ₹3,00,000 and sales from 10,000 to 12,500 units. Advertisement elasticity is:', ['0.5', '2', '0.25', '1'], 0, '(2,500/10,000) ÷ (1,00,000/2,00,000) = 0.25 ÷ 0.5 = 0.5. 2 inverts the ratio.', 'c13', 'core', '((12500-10000)/10000)/((300000-200000)/200000)'),
        Q('m37', 'An advertisement elasticity greater than one means:', ['Sales rise more than proportionately to advertising spend', 'Sales do not respond', 'Sales fall when advertising rises', 'Sales rise less than proportionately'], 0, 'Ea > 1 → highly effective advertising.', 'c13'),
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'table',
         'q': 'A firm cuts the price of its water purifier filter from ₹100 to ₹90; monthly sales rise from 1,500 to 1,800 units. (a) Compute price elasticity of demand by the percentage method. (b) Verify using the total outlay method. (c) Should the firm cut the price further, assuming costs allow it? Show steps.',
         'model': [table(['Step', 'Working', 'Result'], [['% change in Q', '300 ÷ 1,500 × 100', '20%'], ['% change in P', '10 ÷ 100 × 100', '10%'], ['Ep', '20 ÷ 10', q1_e], ['Outlay before', '100 × 1,500', q1_t1], ['Outlay after', '90 × 1,800', q1_t2]]),
                   p(f'(a) Ep = {q1_e} (elastic). (b) Outlay rises from {R(q1_t1)} to {R(q1_t2)} as price falls — opposite directions, elastic. (c) With elastic demand, a further cut raises revenue; whether profit rises depends on the cost of the extra units, so the firm should compare the extra revenue with the extra cost.')],
         'scheme': [{'id': 's1', 'pt': 'Percentage changes in Q and P', 'm': 1.5, 'skill': 'computation'}, {'id': 's2', 'pt': 'Ep = 2 and classified elastic', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Total outlay before and after with conclusion', 'm': 1.5, 'skill': 'analysis'}, {'id': 's4', 'pt': 'Business advice linking elasticity, revenue and cost', 'm': 1, 'skill': 'conclusion'}],
         'remarks': ['Use the original price and quantity as base in the percentage method unless the arc method is asked.'], 'mistakes': ['Dividing % change in price by % change in quantity.', 'Claiming profit must rise because revenue rises.'], 'tips': ['Write the formula first, then substitute.'], 'checks': cq1},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'When the price of a movie ticket is ₹35, 160 tickets are sold per show; when the price is ₹25, 240 tickets are sold. Compute arc elasticity of demand and explain why the mid-point method is preferred here.',
         'model': [p(f'Arc Ep = [(240 − 160) ÷ (240 + 160)] × [(25 + 35) ÷ (35 − 25)] = (80 ÷ 400) × (60 ÷ 10) = 0.2 × 6 = {q2_arc}.'),
                   p('The price change is large. The percentage method would give 1.75 with ₹35/160 as the base [(80/160) ÷ (10/35)] but about 0.83 with ₹25/240 as the base [(80/240) ÷ (10/25)]. The mid-point method uses averages and gives one consistent value whichever direction the price moves.')],
         'scheme': [{'id': 's1', 'pt': 'Correct formula', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Substitution and result 1.2', 'm': 2, 'skill': 'computation'}, {'id': 's3', 'pt': 'Reason for mid-point method', 'm': 1, 'skill': 'concept'}],
         'remarks': ['Many students take only the old values as base — that is the percentage method, not arc.'], 'mistakes': ['Using (P2 − P1)/(P2 + P1) upside down.'], 'tips': ['Drop the minus sign and say so.'], 'checks': cq2},
        {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'table',
         'q': 'The demand for a brand of juice is Q = 2,000 − 40P. (a) Find the point price elasticity at P = ₹30. (b) At what price is demand unitary elastic? (c) If consumer income rises from ₹50,000 to ₹60,000 and, at the same price of ₹30, quantity demanded rises from 800 to 960 units, compute income elasticity and classify the good. (d) Is the change in (c) a movement along the demand curve or a shift?',
         'model': [table(['Part', 'Working', 'Result'], [['(a)', f'Q = 2,000 − 40 × 30 = {q3_q}; Ep = 40 × 30 ÷ 800', q3_e], ['(b)', 'Mid-point: price-axis intercept = 2,000 ÷ 40 = 50; half of 50', q3_pm], ['(c)', '(160/800) ÷ (10,000/50,000) = 0.2 ÷ 0.2', q3_ei]]),
                   p(f'(a) Ep = {q3_e}: elastic. (b) Demand is unitary elastic at P = ₹{q3_pm} (Q = 1,000). (c) Ei = {q3_ei}: normal good; the share of income spent on it stays the same (borderline between necessity and luxury). (d) Income changed while price stayed the same — the whole demand curve shifts to the right (increase in demand), not a movement along it.')],
         'scheme': [{'id': 's1', 'pt': 'Q at P = 30 and point elasticity formula', 'm': 1.5, 'skill': 'computation'}, {'id': 's2', 'pt': 'Price for unitary elasticity (mid-point)', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Income elasticity computed and classified', 'm': 2, 'skill': 'computation'}, {'id': 's4', 'pt': 'Shift vs movement correctly identified', 'm': 1, 'skill': 'concept'}],
         'remarks': ['Point elasticity on a linear demand curve uses the coefficient of P, not the slope of the drawn line (ΔP/ΔQ).'], 'mistakes': ['Writing Ep = 40 (coefficient only).', 'Calling an income-led change a movement along the curve.'], 'tips': ['Remember: on a linear demand curve Ep = 1 at half the maximum price.'], 'checks': cq3},
    ]

    viva = [
        V('v1', 'What is demand in economics?',
          'Demand is the desire for a good backed by the ability to pay and the willingness to pay. It is always stated at a given price and per unit of time, because demand is a flow.',
          [P('p1', 'Desire backed by ability (and willingness) to pay', 5, 'desire|want|wish', 'ability|able|afford|purchasing power|capacity to pay|means to pay', min=2),
           P('p2', 'Willingness to pay', 2, 'willingness|ready to pay|ready to spend|prepared to pay|wants to pay|want to pay'),
           P('p3', 'At a given price and per unit of time (flow)', 3, 'price', 'time|period|per day|per month|per week|flow', min=1)], 'c1'),
        V('v2', 'What causes a movement along a demand curve, and what is such a change called?',
          'A movement along the same demand curve is caused only by a change in the good\'s own price, other things remaining the same. A fall in its price causes an expansion (extension) of demand and a rise in its price causes a contraction of demand; this is a change in quantity demanded.',
          [P('p1', 'Caused only by a change in the good\'s own price, other things constant', 5, 'own price|its price|its own price|price itself|only price|only the price|price alone|price of that good|price of this good|price of the same good|price of the commodity itself|price of the good itself'),
           P('p2', 'Called expansion (extension) / contraction of demand', 3, 'expansion|extension|contraction|extend|contract'),
           P('p3', 'Fall in price → expansion; rise in price → contraction (change in quantity demanded)', 2, 'fall price expansion|price fall expansion|price falls expansion|lower price expansion|price decrease expansion|fall in price extension|price fall extension|rise price contraction|price rise contraction|price rises contraction|price increase contraction|higher price contraction|quantity demanded|same curve|same demand curve', min=1)], 'c7'),
        V('v7', 'What causes a shift of the demand curve, and what are the shifts called?',
          'The demand curve shifts when any determinant other than the good\'s own price changes, such as consumers\' income, tastes and preferences, prices of related goods, expectations or population. A rightward shift is called an increase in demand and a leftward shift a decrease in demand.',
          [P('p1', 'Change in a determinant other than own price (income, tastes, related prices, expectations, population)', 5, 'other than price|other than its own price|other than the own price|other determinant|other factor|income|taste|preference|related good|substitut|complement|expectation|population|fashion|credit', min=1),
           P('p2', 'Rightward = increase in demand', 3, 'right increase|rightward increase|increase right|increase in demand right|right is increase|right called increase|rightward shift is increase|increase rightward|increase shifts right|increase means right|right shift increase'),
           P('p3', 'Leftward = decrease in demand', 2, 'left decrease|leftward decrease|decrease left|decrease in demand left|left is decrease|left called decrease|leftward shift is decrease|decrease leftward|decrease shifts left|decrease means left|left shift decrease')], 'c7'),
        V('v3', 'How does the total outlay method tell us whether demand is elastic or inelastic?',
          'Under the total outlay method we see how total expenditure changes when price changes. Demand is elastic when price and total outlay move in opposite directions. Elasticity is unity when outlay stays the same. Demand is inelastic when price and outlay move in the same direction. It does not give the exact numerical value.',
          [P('p1', 'Opposite directions → elastic', 4, ALT('elastic when price and outlay move in opposite', 'elastic when price and total outlay move in opposite', 'elastic when price and expenditure move in opposite', 'opposite direction demand elastic', 'opposite {x} elastic', 'elastic {x} opposite', 'price falls outlay rises elastic', 'price fall expenditure rise elastic', 'price fall revenue rise elastic', 'price fall total outlay rise elastic', x=['', 'direction', 'directions']) + '|price rises outlay falls elastic|price rise expenditure fall elastic|price fall outlay increas elastic|price fall expenditure increas elastic|outlay rises when price falls elastic|expenditure increases when price falls elastic|more than one when outlay|greater than one when price and outlay move in opposite'),
           P('p2', 'Unchanged outlay → unitary', 3, 'same|unchanged|constant|no change|does not change|remains', 'unit|unity|unitary|one|1|not change unit|not change it is unit|no change unit|not change unitary', min=2),
           P('p3', 'Same direction → inelastic', 3, 'same direction inelastic|inelastic same direction|price falls outlay falls inelastic|price fall expenditure fall inelastic|price fall revenue fall inelastic|price rise outlay rise inelastic|price rise expenditure rise inelastic|outlay falls when price falls inelastic|less than one when price and outlay move in the same|same direction less than one|move together inelastic|together inelastic|inelastic when price and outlay move in the same|inelastic when price and total outlay move in the same|inelastic when price and expenditure move in the same|same direction demand inelastic')], 'c10'),
        V('v4', 'What is the sign of cross elasticity for substitutes and for complements? Give examples.',
          'Cross elasticity is positive for substitutes and negative for complements. For example, tea and coffee are substitutes: when the price of tea rises, demand for coffee rises. Cars and petrol are complements: when the price of cars rises, demand for petrol falls. For unrelated goods it is zero.',
          [P('p1', 'Positive for substitutes and negative for complements (correctly paired)', 8, ALT('{a} {b} {c} {d}', a=['substitut'], b=['positive'], c=['complement'], d=['negative']) + '|' + ALT('{x}', x=['positive substitut negative complement', 'substitut positive negative complement', 'positive substitut complement negative', 'negative complement positive substitut', 'complement negative substitut positive', 'complement negative positive substitut', 'negative complement substitut positive', 'substitut positive complement negative', 'substitut positive negative complementary', 'substitut positive complementary negative']) + '|' + ALT('substitut positive {x} complement negative', 'positive substitut {x} negative complement', 'complement negative {x} substitut positive', 'negative complement {x} positive substitut', 'substitut positive {x} {y} complement negative', 'complement negative {x} {y} substitut positive', x=EXW, y=EXW)),
           P('p3', 'Examples (tea/coffee; car/petrol etc.)', 2, 'tea|coffee|pepsi|coke|butter|margarine', 'petrol|car|printer|cartridge|pen|ink|bread', min=1)], 'c12'),
        V('v5', 'What is a Giffen good? Is every inferior good a Giffen good?',
          'A Giffen good is a very inferior staple whose quantity demanded rises when its price rises, because the negative income effect is stronger than the substitution effect, as Giffen observed for bread among poor families. Every Giffen good is inferior, but not every inferior good is a Giffen good.',
          [P('p1', 'Demand rises when its price rises (exception to the law)', 4, 'demand rise price rise|price rise demand rise|price rise demand increas|price increase demand increase|demand increas price increas|price rises more is bought|more demanded when price rises|demand goes up when price goes up|price goes up demand goes up|exception|upward slop|positive relation'),
           P('p2', 'Strong negative income effect outweighs substitution effect / inferior staple of the poor', 2, 'income effect|inferior|poor|staple|bread|necessit', min=1),
           P('p3', 'Not every inferior good is Giffen (but every Giffen good is inferior)', 4, 'not every inferior|not all inferior|every inferior good is not|all inferior goods are not|inferior goods need not|no not every|not necessarily giffen|not always giffen|not every|not all')], 'c6'),
        V('v6', 'Why is elasticity different at different points on a straight-line demand curve even though its slope is constant?',
          'Elasticity depends not only on the slope but also on the ratio of price to quantity at each point. On a straight-line demand curve, elasticity equals the lower segment divided by the upper segment, so it is infinite at the price axis, more than one above the mid-point, one at the mid-point, less than one below it, and zero at the quantity axis.',
          [P('p1', 'Depends on price/quantity ratio, not slope alone', 4, 'ratio|price quantity|p by q|p q|p over q|percentage|proportionate|relative change', min=1),
           P('p2', 'Lower segment ÷ upper segment', 3, 'lower segment|lower part|lower portion|below|lower'),
           P('p3', 'Unity at mid-point (infinite at price axis, zero at quantity axis)', 3, ALT('mid point {x}', 'middle {x}', 'midpoint {x}', 'centre {x}', x=['1', 'one', 'unit', 'unitary', 'equal to one', 'is one', 'is 1', 'elasticity 1', 'elasticity one', 'elasticity unit', 'elasticity is unity', 'unity']) + '|unity at the mid|unitary at the mid|one at the mid|1 at the mid|unity middle|unity at the middle|one at the middle|1 at the middle|unitary at the middle|unity centre|unity center')], 'c9'),
    ]

    cases = [{'id': 'k1', 'title': 'BrewFresh coffee capsules — pricing, promotion and incomes', 'difficulty': 'hard',
              'case': ('BrewFresh sells coffee capsules in a city. Last quarter it cut the price of a box from ₹250 to ₹200 and monthly sales rose from 4,000 to 5,600 boxes. In another month, with price unchanged, it raised its advertising budget from ₹1,00,000 to ₹1,50,000 and sales rose from 4,000 to 4,600 boxes. '
                       'A survey shows that when average household income in the city rose from ₹30,000 to ₹33,000 a month, sales rose from 4,000 to 4,400 boxes at an unchanged price. A rival tea-capsule brand is planning a price cut.'),
              'mcqs': [
                  Q('k1a', 'Price elasticity of demand for BrewFresh capsules (percentage method, original values as base) is:', [str(k_ep), '0.5', '1.6', '1'], 0, '(1,600/4,000) ÷ (50/250) = 0.4 ÷ 0.2 = 2. 0.5 inverts the ratio; 1.6 divides by 25% (using ₹200 as base).', 'c9', 'moderate', '((5600-4000)/4000)/((250-200)/250)'),
                  Q('k1b', 'What happened to BrewFresh\'s total revenue after the price cut?', [f'Rose from {R(k_tr1)} to {R(k_tr2)}, confirming elastic demand', f'Fell from {R(k_tr1)} to {R(k_tr2)}, showing inelastic demand', 'Remained unchanged — unitary elasticity', 'Cannot be determined'], 0, f'250 × 4,000 = {R(k_tr1)}; 200 × 5,600 = {R(k_tr2)}. Price fell, outlay rose — elastic.', 'c10', 'moderate'),
                  Q('k1c', 'Advertisement elasticity of demand is:', [str(k_ea), '3.33', '0.15', '1.5'], 0, '(600/4,000) ÷ (50,000/1,00,000) = 0.15 ÷ 0.5 = 0.3. 3.33 inverts it; 0.15 forgets to divide by the change in advertising.', 'c13', 'moderate', '((4600-4000)/4000)/((150000-100000)/100000)'),
                  Q('k1d', 'Income elasticity of demand for the capsules is:', [str(k_ei), '0.1', '10', '0.5'], 0, '(400/4,000) ÷ (3,000/30,000) = 0.1 ÷ 0.1 = 1: the share of income spent on capsules stays constant.', 'c12', 'hard', '((4400-4000)/4000)/((33000-30000)/30000)'),
                  Q('k1e', 'If the rival cuts the price of tea capsules, BrewFresh\'s demand curve will most likely:', ['Shift to the left', 'Shift to the right', 'Show a movement down the same curve', 'Become vertical'], 0, 'Tea capsules are substitutes: a fall in their price decreases demand for coffee capsules — a leftward shift.', 'c7', 'core'),
              ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch02', 'n': 1, 'title': 'Law of Demand and Elasticity of Demand',
        'outcomes': ['Define demand and explain its determinants and the demand function.', 'State the law of demand, derive market demand, explain why the curve slopes down, and list exceptions.',
                     'Distinguish expansion/contraction from increase/decrease in demand.', 'Measure price elasticity by the percentage, point, geometric, arc and total outlay methods, and explain its determinants.',
                     'Compute and interpret income, cross and advertisement elasticities.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 70, 'practice': 70}, 'prereq': ['fnd-p4-ch01-u01'],
                 'exam_tip': 'This is the heaviest-weighted unit of the chapter. Expect 4–6 MCQs: an elasticity calculation (percentage, arc or point), a total outlay classification, a shift-vs-movement question and a Giffen/Veblen exception. Always check which base the question wants.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {'summary': ['Demand = desire + ability + willingness to pay, at a price, per period.', 'Determinants: own price, related prices, income, tastes, expectations, population, income distribution, credit, interest rates.',
                                 'Law of demand: inverse price–quantity relation, ceteris paribus; reasons — DMU, income & substitution effects, new buyers, more uses.', 'Exceptions: Veblen/conspicuous goods, Giffen goods, conspicuous necessities, price expectations, irrational behaviour, necessaries, speculative goods.',
                                 'Own price change → movement (expansion/contraction); other determinant → shift (increase/decrease).', 'Ep = (ΔQ/Q)/(ΔP/P); arc = [(Q2−Q1)/(Q2+Q1)] × [(P2+P1)/(P2−P1)]; point = −(dQ/dP)(P/Q); linear curve: lower ÷ upper segment.',
                                 'Ei: >1 luxury, 0–1 necessity, <0 inferior. Ec: + substitutes, − complements, 0 unrelated. Ea = (ΔQ/Q)/(ΔA/A).'],
                     'remember': ['Total outlay: opposite direction = elastic; same direction = inelastic; unchanged = unitary.', 'Unitary elastic curve = rectangular hyperbola; perfectly inelastic = vertical; perfectly elastic = horizontal.', 'On Q = a − bP, Ep = 1 at P = a/(2b).'],
                     'traps': ['Slope ≠ elasticity.', 'All Giffen goods are inferior; not all inferior goods are Giffen.', 'A rise in income shifts demand for an inferior good to the left.', 'Arc and percentage methods give different answers — read the question.']},
        'quickref': [{'k': 'Ep (percentage)', 'v': '(ΔQ/Q) ÷ (ΔP/P)'}, {'k': 'Ep (arc)', 'v': '[(Q2−Q1)/(Q2+Q1)] × [(P2+P1)/(P2−P1)]'}, {'k': 'Ep (point)', 'v': '−(dQ/dP) × P/Q; linear: lower ÷ upper segment'},
                     {'k': 'Ei', 'v': '(ΔQ/Q) ÷ (ΔY/Y)'}, {'k': 'Ec', 'v': '(ΔQx/Qx) ÷ (ΔPy/Py)'}, {'k': 'Ea', 'v': '(ΔQ/Q) ÷ (ΔA/A)'}, {'k': 'Demand function', 'v': 'Dx = f(Px, Py, M, T, A, U)'}],
        'viva': viva, 'cases': cases,
    }
