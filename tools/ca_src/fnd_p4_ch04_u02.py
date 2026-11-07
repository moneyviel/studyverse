"""CA Foundation · Paper 4 Business Economics · Chapter 4 Price Determination in Different Markets · Unit 2 Determination of Prices.
Original explanations, numbers and questions. Every figure is computed in code and re-checked by tools/ca_validate.py."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch04-u02'


def Q(i, q, o, a, e, c, d='core', check=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'concept': c, 'difficulty': d}
    if check: m['check'] = check
    return m


def M(i, q, o, a, e, d='moderate', check=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if check: m['check'] = check
    return m


def eq(a, b, c, d):
    """Qd = a - b P ; Qs = c + d P  ->  (P, Q)"""
    pr = (a - c) / (b + d)
    return pr, a - b * pr


def build():
    # ---------- Illustration 1: schedule ----------
    c1 = Checks()
    sch = [(10, 1000, 100), (20, 750, 300), (30, 500, 500), (40, 350, 700), (50, 250, 900)]
    rows1 = []
    for pr, d, s in sch:
        g = c1.add(f'{s}-{d}', f'Qs - Qd at ₹{pr}')
        rows1.append([str(pr), inr(d), inr(s), inr(g), 'Surplus — price falls' if g > 0 else ('Shortage — price rises' if g < 0 else 'Equilibrium')])
    t1 = table(['Price (₹/kg)', 'Quantity demanded (kg)', 'Quantity supplied (kg)', 'Qs − Qd (kg)', 'Market pressure'], rows1, num=[0, 1, 2, 3], title='Weekly market for paneer in a town')

    # ---------- Illustration 2: algebra ----------
    c2 = Checks()
    p0 = c2.add('(600-120)/(20+40)', 'original equilibrium price')
    q0 = c2.add('600-20*8', 'original equilibrium quantity')
    p1 = c2.add('(720-120)/(20+40)', 'price after demand rises by 120')
    q1 = c2.add('720-20*10', 'quantity after demand rises')
    p2 = c2.add('(720-240)/(20+40)', 'price after supply also rises by 120')
    q2 = c2.add('720-20*8', 'quantity after both rise')
    gap = c2.add('(720-20*8)-(120+40*8)', 'excess demand at old price after demand rises')

    # ---------- Illustration 3: simultaneous shifts ----------
    c3 = Checks()
    base = c3.add('(500+100)/(10+20)', 'base price')
    baseq = c3.add('500-10*20', 'base quantity')
    scen = [('(a) Demand +60, supply +60 (equal increase)', 60, 60), ('(b) Demand +90, supply +30 (demand rises more)', 90, 30), ('(c) Demand +30, supply +90 (supply rises more)', 30, 90),
            ('(d) Demand +60, supply −30 (opposite; demand shift larger)', 60, -30), ('(e) Demand +30, supply −90 (opposite; supply shift larger)', 30, -90)]
    rows3 = [['Original', '500 − 10P', '−100 + 20P', str(base), str(baseq), '—']]
    for lab, dd, ds in scen:
        a, cc = 500 + dd, -100 + ds
        pr = c3.add(f'({a}-({cc}))/(10+20)', f'price {lab[:3]}')
        qq = c3.add(f'{a}-10*({a}-({cc}))/(10+20)', f'quantity {lab[:3]}')
        eff = ('price ' + ('same' if pr == base else 'up' if pr > base else 'down') + ', quantity ' + ('same' if qq == baseq else 'up' if qq > baseq else 'down'))
        rows3.append([lab, f'{a} − 10P', f'{cc} + 20P'.replace('+ -', '− '), str(pr), str(qq), eff])
    t3 = table(['Case', 'Demand Qd', 'Supply Qs', 'Equilibrium price (₹)', 'Equilibrium quantity', 'Effect'], rows3, num=[3, 4], title='Same market, five combinations of shifts')

    # ---------- written questions ----------
    w1 = Checks()
    w1p = w1.add('(1800-300)/(30+20)', 'equilibrium price')
    w1q = w1.add('1800-30*30', 'equilibrium quantity')
    w1d = w1.add('1800-30*24', 'Qd at ₹24')
    w1s = w1.add('300+20*24', 'Qs at ₹24')
    w1g = w1.add('(1800-30*24)-(300+20*24)', 'shortage at ₹24')
    w1d2 = w1.add('1800-30*36', 'Qd at ₹36')
    w1s2 = w1.add('300+20*36', 'Qs at ₹36')
    w1g2 = w1.add('(300+20*36)-(1800-30*36)', 'surplus at ₹36')
    w2 = Checks()
    w2p = w2.add('(400-40)/(4+6)', 'original price')
    w2q = w2.add('400-4*36', 'original quantity')
    w2p1 = w2.add('(400-90)/(4+6)', 'price after supply rises by 50')
    w2q1 = w2.add('400-4*31', 'quantity after supply rises')
    w3 = Checks()
    w3p = w3.add('(240+60)/(5+10)', 'original price')
    w3q = w3.add('240-5*20', 'original quantity')
    w3p1 = w3.add('(270+90)/(5+10)', 'price when demand +30 and supply -30')
    w3q1 = w3.add('270-5*24', 'quantity in that case')

    # ---------- MCQ expressions ----------
    mq_p = '(500-50)/(15+15)'
    mq_q = '500-15*15'
    mq_short = '(1200-40*10)-(200+60*10)'

    # ---------- case ----------
    k = Checks()
    kp = k.add('(9000-1500)/(150+100)', 'case: equilibrium price')
    kq = k.add('9000-150*30', 'case: equilibrium quantity')
    kp1 = k.add('(9000-750)/(150+100)', 'case: price after supply falls by 750')
    kq1 = k.add('9000-150*33', 'case: quantity after supply falls')
    kg = k.add('(9000-150*30)-(750+100*30)', 'case: shortage at old price after the frost')

    concepts = [
        {'id': 'c1', 'title': 'Introduction — why price determination matters', 'body': [
            'Prices express the exchange value of goods. The rewards of the factors of production are also prices: rent for land, wages for labour, interest for capital and profit for organisation. That is why the way prices are formed sits at the centre of economics.',
            'In a free market, buyers and sellers act without outside interference and price is settled by demand and supply alone. In practice the government sometimes fixes or influences prices — for example administered prices of some fuels and fertilisers, or minimum support and procurement prices for wheat, rice and sugarcane — weighing input costs, business risk and the interests of both producers and consumers.',
            'The demand–supply model lets a business or a policy-maker predict how an event — a tax, a subsidy, a price ceiling or floor, a crop failure, a change in incomes — will change the equilibrium price and quantity.'],
         'analogy': 'Demand and supply are the two blades of a pair of scissors: neither cuts alone; price is where they meet.',
         'work': 'Commodity-price forecasts in budgets, impact notes on a new GST rate, and procurement planning all use this simple model before any detailed numbers are run.'},
        {'id': 'c2', 'title': 'Equilibrium price — the general view', 'body': [
            'Equilibrium is a state with no tendency to change. In a market it means quantity demanded equals quantity supplied: everything sellers want to sell at that price is bought, and every buyer who wants to buy at that price gets the good — the market clears. The price at which this happens is the equilibrium or market-clearing price.',
            'Above the equilibrium price, quantity supplied exceeds quantity demanded (a surplus or excess supply). Sellers with unsold stock cut prices; the lower price draws in more buyers and discourages some output, and the gap narrows until it vanishes.',
            'Below the equilibrium price, quantity demanded exceeds quantity supplied (a shortage or excess demand). Buyers who cannot get enough bid the price up; the higher price trims purchases and encourages extra output, until the gap is gone.',
            'Because any disturbance sets off forces that bring the market back, the equilibrium is called stable — provided other things (incomes, tastes, technology, input prices) stay the same. The self-correcting process is the price mechanism.'],
         'analogy': 'A crowded auction: if the auctioneer\'s price is too low, hands go up everywhere and the price climbs; if too high, the room falls silent and the price drops — until exactly as many items are wanted as are on offer.',
         'work': 'Persistent unsold stock (surplus) or long order backlogs (shortage) are signals an auditor or analyst reads as a price that is out of line with the market — often a lead indicator of a write-down or a price revision.'},
        {'id': 'c3', 'title': 'Finding equilibrium with equations', 'body': [
            'Exam questions often give linear functions: Qd = a − bP and Qs = c + dP. Set Qd = Qs and solve: a − bP = c + dP, so P* = (a − c) ÷ (b + d). Put P* back into either function to get Q*.',
            'Example: Qd = 260 − 4P and Qs = 20 + 8P. Then 260 − 4P = 20 + 8P, 240 = 12P, P* = 20, Q* = 260 − 80 = 180. (Check with supply: 20 + 160 = 180.)',
            'An increase in demand raises the constant a (more is demanded at every price); an increase in supply raises the constant c. Re-solve to get the new equilibrium. At any non-equilibrium price, excess demand = Qd − Qs and excess supply = Qs − Qd.'],
         'analogy': 'Two cars on the same road starting from opposite ends — the meeting point is where their positions are equal.',
         'work': 'Simple linear demand and supply estimates are used in pricing studies and in estimating how much of a tax will be passed on to customers.'},
        {'id': 'c4', 'title': 'Changes in demand (supply unchanged)', 'body': [
            'In real markets the "other things" — income, tastes, population, prices of related goods, expectations — keep changing and shift the whole demand curve.',
            'Increase in demand (shift to the right), e.g. higher incomes for a normal good: at the old price there is now excess demand, so price rises; the higher price calls forth more supply (a movement up the supply curve). Result: equilibrium price and quantity both rise.',
            'Decrease in demand (shift to the left), e.g. a fall in incomes: at the old price there is excess supply, so price falls and quantity supplied contracts. Result: equilibrium price and quantity both fall.',
            'Note the language: the demand curve shifts, but supply does not change — only the quantity supplied changes along the same supply curve.'],
         'analogy': 'More guests arrive at a wedding buffet (demand up): the caterer raises the per-plate rate and also cooks more plates.',
         'work': 'Analysts forecasting a company\'s sales after a rise in rural incomes or a festival season use exactly this "demand shifts right → price and volume up" logic.'},
        {'id': 'c5', 'title': 'Changes in supply (demand unchanged)', 'body': [
            'Supply shifts when costs, technology, input prices, the number of sellers, taxes and subsidies or the weather change.',
            'Increase in supply (shift to the right), e.g. better technology: at the old price there is a surplus, so price falls and quantity demanded expands. Result: equilibrium price falls, equilibrium quantity rises.',
            'Decrease in supply (shift to the left), e.g. a crop failure, a rise in input prices or outdated technology: at the old price there is a shortage, so price rises and quantity demanded contracts. Result: equilibrium price rises, equilibrium quantity falls.'],
         'analogy': 'A bumper tomato crop floods the mandi (supply up): prices crash and households buy more tomatoes.',
         'work': 'Input-cost shocks — a spike in crude oil or steel — are modelled as leftward supply shifts when a CA prepares a sensitivity analysis on margins and selling prices.'},
        {'id': 'c6', 'title': 'Simultaneous changes in demand and supply', 'body': [
            'Same direction: if both increase, equilibrium quantity certainly rises, but price may rise, fall or stay the same — it rises if demand increases more than supply, falls if supply increases more, and is unchanged if both increase equally. If both decrease, quantity certainly falls and the price change is uncertain (price falls if demand falls more, rises if supply falls more).',
            'Opposite directions: if demand increases and supply decreases, price certainly rises, but quantity may rise or fall — it rises if the demand shift is larger, falls if the supply shift is larger. If demand decreases and supply increases, price certainly falls and the quantity change is uncertain.',
            'Rule of thumb: when both curves move together, quantity is certain and price is uncertain; when they move in opposite directions, price is certain and quantity is uncertain. The curve that shifts more decides the uncertain variable.'],
         'blocks': [table(['Demand', 'Supply', 'Equilibrium price', 'Equilibrium quantity'], [
             ['Increases', 'Increases', 'Uncertain (up if D shift bigger, down if S shift bigger, same if equal)', 'Increases'],
             ['Decreases', 'Decreases', 'Uncertain (down if D shift bigger, up if S shift bigger)', 'Decreases'],
             ['Increases', 'Decreases', 'Increases', 'Uncertain (up if D shift bigger, down if S shift bigger)'],
             ['Decreases', 'Increases', 'Decreases', 'Uncertain (down if D shift bigger, up if S shift bigger)'],
         ], title='Simultaneous shifts — what is certain and what is not')],
         'analogy': 'Two people pulling a rope: if both pull the same way the rope surely moves that way (quantity); who wins the tug decides the rest.',
         'work': 'During a war or a pandemic, supply falls while some demand rises — the price spike is predictable, but sales volume depends on which force is stronger; budgets should show both cases.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Reading equilibrium from a schedule', 'difficulty': 'core', 'minutes': 6,
         'q': 'The weekly demand and supply of paneer in a town are given below. Find the equilibrium price and quantity and state the market pressure at every other price.',
         'solution': [t1, p('At ₹30 per kg quantity demanded = quantity supplied = 500 kg, so ₹30 is the equilibrium price and 500 kg the equilibrium quantity. Below ₹30 there is a shortage and buyers push the price up; above ₹30 there is a surplus and sellers cut the price.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Equilibrium by equations, and a shift in demand', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'For a brand of notebooks, Qd = 600 − 20P and Qs = 120 + 40P. (a) Find the equilibrium. (b) Rising school enrolment raises demand by 120 units at every price. Find the new equilibrium and the excess demand at the old price. (c) A new supplier then raises supply by 120 units at every price. Find the final equilibrium.',
         'solution': [wn('(a)', f'600 − 20P = 120 + 40P → 480 = 60P → P = ₹{p0}; Q = 600 − 160 = {q0}.'),
                      wn('(b)', f'New Qd = 720 − 20P. At the old price ₹8: Qd = 560, Qs = 440 → excess demand {gap}. New equilibrium: 720 − 20P = 120 + 40P → P = ₹{p1}; Q = {q1}. Price and quantity both rise.'),
                      wn('(c)', f'New Qs = 240 + 40P. 720 − 20P = 240 + 40P → P = ₹{p2}; Q = {q2}. Equal increases in demand and supply leave price unchanged at ₹8 but raise quantity from {q0} to {q2}.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Simultaneous shifts — five cases', 'difficulty': 'hard', 'minutes': 12,
         'q': 'A market has Qd = 500 − 10P and Qs = −100 + 20P. Work out the new equilibrium for each combination of shifts (figures are changes in quantity at every price) and state what happens to price and quantity.',
         'solution': [t3, p('Cases (a)–(c): both curves move right — quantity rises every time, but price stays the same, rises or falls depending on which shift is bigger. Cases (d)–(e): curves move in opposite directions — price rises every time, but quantity rises in (d) and falls in (e).')],
         'checks': c3},
        {'id': 'i4', 'title': 'Which curve moves? Four news items', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'State which curve shifts, in which direction, and the effect on equilibrium price and quantity: (a) incomes rise (normal good) and at the same time the price of a key raw material rises; (b) the price of a complementary good falls and a technology improvement cuts production cost; (c) unseasonal rain destroys part of the onion crop; (d) buyers expect car prices to rise sharply next year.',
         'solution': [table(['Event', 'Demand', 'Supply', 'Price', 'Quantity'], [
             ['(a) Income up; input price up', 'Shifts right', 'Shifts left', 'Rises (certain)', 'Uncertain — depends on relative shifts'],
             ['(b) Complement cheaper; better technology', 'Shifts right', 'Shifts right', 'Uncertain — depends on relative shifts', 'Rises (certain)'],
             ['(c) Crop damaged by rain', 'No change', 'Shifts left', 'Rises', 'Falls'],
             ['(d) Expected price rise of cars', 'Shifts right (buy now)', 'No change (assumed)', 'Rises', 'Rises'],
         ], title='Applying demand–supply analysis')]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Explaining a price spike to the board', 'role': 'CA in industry — FP&A at a restaurant chain',
         'situation': 'Tomato prices have tripled in two months. The board asks whether to lock in a 6-month forward contract.',
         'steps': ['Identify the cause: heavy rain damaged the crop — a leftward supply shift with demand roughly unchanged.', 'Predict: price high while the shortage lasts; when the next crop arrives supply shifts back right and price should fall.', 'Compare the forward rate offered with the expected path of prices; a 6-month lock-in at today\'s spike may be costly.', 'Recommend a shorter hedge for part of the requirement and menu tweaks to reduce tomato use meanwhile.'],
         'takeaway': 'Diagnose which curve has shifted before forecasting a price — a supply shock is usually temporary for seasonal crops.', 'think': 'If at the same time a festival season raises demand for restaurant meals, what happens to the predicted price?', 'answer': 'Demand for tomatoes also shifts right, so price rises even more; quantity may rise or fall depending on the relative shifts.'},
        {'id': 'j2', 'title': 'Is excess inventory a pricing problem?', 'role': 'Audit senior reviewing inventory at a garment maker',
         'situation': 'Closing stock of last season\'s jackets is three times the normal level, while the company has kept its list price unchanged.',
         'steps': ['Unsold stock at the current price signals that the list price is above the market-clearing level (a surplus).', 'Check post-year-end sales and discounts actually given to estimate the realisable price.', 'If goods can be sold only at a lower price, test net realisable value and propose a write-down where NRV is below cost.'],
         'takeaway': 'A surplus at the ruling price is the market\'s way of saying the price is too high — an audit flag for inventory valuation.'},
    ]

    mcqs = [
        Q('m1', 'A free market is one in which:', ['Price is settled by demand and supply without outside interference', 'The government fixes all prices', 'Goods are distributed free of cost', 'Only one seller operates'], 0, 'Free market = forces of demand and supply take their own course.', 'c1'),
        Q('m2', 'Wages, rent, interest and profit are:', ['Prices of the services of factors of production', 'Transfer payments', 'Prices of consumer goods', 'Indirect taxes'], 0, 'Factor rewards are also prices — for labour, land, capital and organisation.', 'c1'),
        Q('m3', 'Equilibrium price is the price at which:', ['Quantity demanded equals quantity supplied', 'Demand is maximum', 'Supply is maximum', 'Producers earn maximum profit'], 0, 'The market clears — no unsold stock and no unmet demand.', 'c2'),
        Q('m4', 'If the market price is above the equilibrium price, there will be:', ['Excess supply, and price will tend to fall', 'Excess demand, and price will tend to rise', 'Equilibrium', 'A shift of the demand curve'], 0, 'Above equilibrium Qs > Qd; sellers cut prices to clear stock.', 'c2'),
        Q('m5', 'A shortage in a market exists when:', ['Quantity demanded exceeds quantity supplied at the ruling price', 'Quantity supplied exceeds quantity demanded', 'Price is above equilibrium', 'Supply curve shifts right'], 0, 'Shortage = excess demand, occurring below the equilibrium price.', 'c2'),
        Q('m6', 'An equilibrium is called stable when:', ['Any departure from it sets off forces that restore it', 'Price never changes in any circumstances', 'Government holds the price fixed', 'Demand equals supply only by chance'], 0, 'Stability = self-correcting disturbances, other things being equal.', 'c2'),
        Q('m7', 'Qd = 500 − 15P and Qs = 50 + 15P. The equilibrium price is:', ['₹15', '₹18.33', '₹16.67', '₹30'], 0, '500 − 15P = 50 + 15P → 450 = 30P → P = ₹15. (₹16.67 = 500/30 — forgetting the supply intercept.)', 'c3', 'moderate', mq_p),
        Q('m8', 'For Qd = 500 − 15P and Qs = 50 + 15P, the equilibrium quantity is:', ['275', '225', '300', '450'], 0, 'P* = 15 → Q* = 500 − 225 = 275 (check: 50 + 225 = 275). 225 is 15 × 15, not Q.', 'c3', 'moderate', mq_q),
        Q('m9', 'Qd = 1,200 − 40P and Qs = 200 + 60P. If the price is ₹10, the market is:', ['In equilibrium', 'Facing a surplus of 200 units', 'Facing a shortage of 200 units', 'Facing a shortage of 400 units'], 0, 'Qd = 1,200 − 400 = 800 and Qs = 200 + 600 = 800, so ₹10 is the equilibrium price.', 'c3', 'moderate'),
        Q('m10', 'Other things equal, an increase in demand for a good leads to:', ['A rise in both equilibrium price and quantity', 'A rise in price and fall in quantity', 'A fall in price and rise in quantity', 'No change in price'], 0, 'Demand shifts right along an unchanged supply curve.', 'c4'),
        Q('m11', 'A fall in consumers\' incomes, for a normal good, with supply unchanged, causes:', ['Equilibrium price and quantity to fall', 'Equilibrium price to rise and quantity to fall', 'Equilibrium price to fall and quantity to rise', 'No change'], 0, 'Demand shifts left → excess supply at old price → price and quantity fall.', 'c4'),
        Q('m12', 'When demand increases and supply is unchanged, the higher price leads to:', ['An extension (rise) in quantity supplied along the same supply curve', 'A shift of the supply curve to the right', 'A decrease in supply', 'A shift of the supply curve to the left'], 0, 'Supply does not change; quantity supplied moves up along the curve.', 'c4', 'moderate'),
        Q('m13', 'An improvement in production technology, with demand unchanged, will:', ['Lower equilibrium price and raise equilibrium quantity', 'Raise both price and quantity', 'Lower both price and quantity', 'Raise price and lower quantity'], 0, 'Supply shifts right → surplus at old price → price falls, quantity rises.', 'c5'),
        Q('m14', 'A severe drought damages the wheat crop. With demand unchanged:', ['Price rises and quantity falls', 'Price falls and quantity rises', 'Both price and quantity rise', 'Both price and quantity fall'], 0, 'Supply shifts left → shortage at old price → price up, quantity down.', 'c5'),
        Q('m15', 'An increase in the price of a raw material used to make a product causes:', ['A leftward shift of the product\'s supply curve', 'A rightward shift of its demand curve', 'A rightward shift of its supply curve', 'A movement down the supply curve'], 0, 'Higher input cost reduces supply at every price.', 'c5'),
        Q('m16', 'When demand and supply both increase by the same amount:', ['Price is unchanged and quantity rises', 'Price rises and quantity is unchanged', 'Both price and quantity rise', 'Price falls and quantity rises'], 0, 'Equal rightward shifts leave the price where it was but raise quantity.', 'c6'),
        Q('m17', 'When both demand and supply increase, which is certain?', ['Equilibrium quantity rises', 'Equilibrium price rises', 'Equilibrium price falls', 'Equilibrium quantity falls'], 0, 'Same-direction shifts: quantity certain, price uncertain.', 'c6'),
        Q('m18', 'Demand increases and supply decreases at the same time. Then:', ['Price certainly rises; quantity may rise or fall', 'Price certainly falls; quantity rises', 'Quantity certainly rises; price uncertain', 'Both certainly fall'], 0, 'Opposite shifts: price certain (up here), quantity depends on which shift is bigger.', 'c6'),
        Q('m19', 'Demand falls and supply rises simultaneously. The equilibrium price will:', ['Fall', 'Rise', 'Remain unchanged', 'Become indeterminate in direction'], 0, 'Both changes push price down; only the quantity change is uncertain.', 'c6'),
        Q('m20', 'Demand and supply both increase, but the increase in supply is greater. Then:', ['Price falls and quantity rises', 'Price rises and quantity rises', 'Price rises and quantity falls', 'Price and quantity fall'], 0, 'Supply\'s bigger rightward move pulls price down; both shifts push quantity up.', 'c6', 'moderate'),
        Q('m21', 'Both demand and supply decrease, and the fall in supply is larger. Then:', ['Price rises and quantity falls', 'Price falls and quantity falls', 'Price falls and quantity rises', 'Price and quantity rise'], 0, 'Quantity surely falls; the bigger supply cut pushes price up.', 'c6', 'moderate'),
        Q('m22', 'The price of a complement of good Z falls and, at the same time, technology for producing Z improves. Equilibrium in the market for Z shows:', ['Higher quantity; price uncertain', 'Higher price; quantity uncertain', 'Lower price and lower quantity', 'Higher price and lower quantity'], 0, 'Cheaper complement → demand for Z shifts right; better technology → supply shifts right. Same direction → quantity up, price uncertain.', 'c6', 'hard'),
        Q('m23', 'Consumers expect a sharp rise in the price of a good next month. With supply unchanged, its current:', ['Price and quantity both rise', 'Price falls and quantity rises', 'Price rises and quantity falls', 'Demand falls'], 0, 'People buy now — demand shifts right today.', 'c4', 'moderate'),
        Q('m24', 'Qd = 900 − 30P and Qs = 300 + 20P. If demand increases by 250 units at every price, the new equilibrium price is:', ['₹17', '₹12', '₹22', '₹15'], 0, 'Old: 600 = 50P → P = ₹12. New: 1,150 − 30P = 300 + 20P → 850 = 50P → P = ₹17.', 'c3', 'hard', '(1150-300)/(30+20)'),
        Q('m25', 'Qd = 1,200 − 40P and Qs = 200 + 60P. If the price is held at ₹8, the shortage in the market is:', ['200 units', '880 units', '680 units', '1,000 units'], 0, 'Qd = 1,200 − 320 = 880; Qs = 200 + 480 = 680; shortage = 880 − 680 = 200 units.', 'c3', 'hard', '(1200-40*8)-(200+60*8)'),
        Q('m26', 'A government-fixed maximum price set below the equilibrium price will create:', ['A shortage', 'A surplus', 'Equilibrium', 'A shift of demand to the left'], 0, 'Below equilibrium Qd > Qs. (Price ceilings and floors are analysed with this same model.)', 'c1', 'moderate'),
    ]
    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'The demand and supply functions for a product are Qd = 1,800 − 30P and Qs = 300 + 20P. (a) Find the equilibrium price and quantity. (b) What happens in the market if price is ₹24? (c) If price is ₹36? Show how the market returns to equilibrium.',
         'model': [wn('(a)', f'1,800 − 30P = 300 + 20P → 1,500 = 50P → P* = ₹{w1p}; Q* = 1,800 − 900 = {inr(w1q)} units.'),
                   wn('(b) Price ₹24', f'Qd = {inr(w1d)}, Qs = {inr(w1s)} → shortage of {inr(w1g)} units. Buyers bid up the price; Qd contracts and Qs extends until price reaches ₹30.'),
                   wn('(c) Price ₹36', f'Qd = {inr(w1d2)}, Qs = {inr(w1s2)} → surplus of {inr(w1g2)} units. Sellers cut the price; Qd extends and Qs contracts until price falls to ₹30.')],
         'scheme': [{'id': 's1', 'pt': 'Equilibrium price and quantity', 'm': 2, 'skill': 'computation'}, {'id': 's2', 'pt': 'Shortage at ₹24 computed', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Surplus at ₹36 computed', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'Explains adjustment through price mechanism', 'm': 1, 'skill': 'analysis'}],
         'remarks': ['Most candidates solve (a) correctly; marks are lost in (b) and (c) by not naming shortage/surplus.'], 'mistakes': ['Saying "demand increases" when price falls — it is quantity demanded that extends.', 'Mixing up shortage and surplus.'],
         'tips': ['Write Qd and Qs at each price in a small table before commenting.'], 'checks': w1},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'Qd = 400 − 4P and Qs = 40 + 6P. A new technology raises supply by 50 units at every price. Find the equilibrium before and after, and comment.',
         'model': [wn('Before', f'400 − 4P = 40 + 6P → 360 = 10P → P = ₹{w2p}; Q = {w2q}.'), wn('After', f'New Qs = 90 + 6P. 400 − 4P = 90 + 6P → 310 = 10P → P = ₹{w2p1}; Q = {w2q1}.'),
                   p('Comment: an increase in supply with demand unchanged lowers the equilibrium price and raises the equilibrium quantity (a movement down the demand curve).')],
         'scheme': [{'id': 's1', 'pt': 'Original equilibrium', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'Correct new supply function', 'm': 1, 'skill': 'application'},
                    {'id': 's3', 'pt': 'New equilibrium', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'Comment on direction of change', 'm': 1, 'skill': 'conclusion'}],
         'remarks': ['An increase in supply adds to the constant term of the supply function — some candidates wrongly change the slope.'], 'mistakes': ['Writing new Qs as 40 + 56P.', 'Saying demand increased.'], 'tips': ['State "shift" for the curve that changes and "extension/contraction" for the other.'], 'checks': w2},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'hard', 'pad': 'text',
         'q': 'Qd = 240 − 5P and Qs = −60 + 10P. Demand rises by 30 units and supply falls by 30 units at every price. Find the new equilibrium and explain why the result on quantity cannot be predicted in general when demand and supply move in opposite directions.',
         'model': [wn('Before', f'240 − 5P = −60 + 10P → 300 = 15P → P = ₹{w3p}; Q = {w3q}.'), wn('After', f'Qd = 270 − 5P, Qs = −90 + 10P → 360 = 15P → P = ₹{w3p1}; Q = 270 − 120 = {w3q1}.'),
                   p(f'Price rises from ₹{w3p} to ₹{w3p1} — both shifts push it up, so the direction of price is certain. Quantity rises from {w3q} to {w3q1}: here the effect of the rise in demand outweighs that of the fall in supply (with the steeper demand slope, equal-sized shifts do not cancel out). In general, the rise in demand pushes quantity up and the fall in supply pushes it down, so the net effect on quantity depends on the relative size of the two shifts (and the slopes) — it cannot be predicted without figures.')],
         'scheme': [{'id': 's1', 'pt': 'Original equilibrium', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'New equilibrium with both functions changed', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Explanation: price certain, quantity depends on relative shifts', 'm': 1.5, 'skill': 'analysis'}],
         'remarks': ['Good answers state the general rule and then show, with the figures, which shift dominates here.'], 'mistakes': ['Concluding that quantity never changes when shifts are equal in size.'], 'tips': ['Quote the four-line rule table from memory.'], 'checks': w3},
    ]

    viva = [
        V('v1', 'What is meant by equilibrium price?',
          'Equilibrium price is the price at which quantity demanded equals quantity supplied, so the market clears — there is no unsold stock and no unsatisfied demand. At this price buyers\' and sellers\' plans match and there is no tendency for the price to change.',
          [P('p1', 'Quantity demanded = quantity supplied', 5, ALT('{d} equal {s}', '{d} equals {s}', '{d} same as {s}', '{s} equal {d}', '{s} equals {d}', d=['quantity demanded', 'demand', 'qd'], s=['quantity supplied', 'supply', 'qs']), 'demand and supply are equal|demand and supply equal|supply and demand are equal|supply and demand equal|demand meets supply|supply meets demand', min=1),
           P('p2', 'Market clears — no surplus, no shortage', 3, 'market clear|no surplus|no shortage|no unsold|no excess|no unsatisfied|no unmet|nothing left unsold'),
           P('p3', 'No tendency to change', 2, 'no tendency|no incentive|no pressure|state of rest|stays|stable|not change|no reason to change')], 'c2'),
        V('v2', 'How does the market move back to equilibrium if the price is set above the equilibrium level?',
          'Above equilibrium, quantity supplied is more than quantity demanded, so there is a surplus or excess supply. Sellers with unsold stock reduce the price. As the price falls, quantity demanded extends and quantity supplied contracts, until the surplus disappears at the equilibrium price.',
          [P('p1', 'Surplus / excess supply above equilibrium', 4, 'surplus|excess supply|supply exceeds demand|supply more than demand|supply greater than demand|unsold stock|glut'),
           P('p2', 'Sellers cut the price', 3, 'price fall|price falls|lower price|reduce price|cut price|price come down|price go down|price drop|price decline|price reduc|lower their price|reduce their price|cut their price'),
           P('p3', 'Qd extends and Qs contracts until gap closes', 3, 'quantity demanded rise|quantity demanded increase|quantity demanded extend|demand extend|demand rise|buy more|demand increase', 'quantity supplied fall|quantity supplied decrease|quantity supplied contract|supply contract|supply fall|supply decrease|produce less|sell less', min=1)], 'c2'),
        V('v3', 'What happens to equilibrium price and quantity when supply decreases and demand stays the same?',
          'When supply decreases, the supply curve shifts to the left. At the old price there is a shortage, so price rises and quantity demanded contracts. The new equilibrium has a higher price and a lower quantity.',
          [P('p1', 'Supply curve shifts left', 3, 'shift left|shifts left|leftward|shift to the left|shifts to the left|moves left|move to the left|shift backward|shifts backward|shift upward'),
           P('p2', 'Shortage at the old price', 2, 'shortage|excess demand|demand exceeds supply|demand more than supply'),
           P('p3', 'Price rises', 3, 'price rise|price rises|price increase|price goes up|higher price|price go up|raises price|price up'),
           P('p4', 'Quantity falls', 2, 'quantity fall|quantity falls|quantity decrease|lower quantity|quantity goes down|less quantity|quantity reduc|quantity declin|quantity down|quantity contract|quantity demanded contract|fall in quantity|quantity bought and sold fall')], 'c5'),
        V('v4', 'When demand and supply both increase, what can we say about equilibrium price and quantity?',
          'When both demand and supply increase, equilibrium quantity definitely increases. The change in price is uncertain: price rises if demand increases more than supply, falls if supply increases more, and stays the same if both increase equally.',
          [P('p1', 'Quantity certainly rises', 4, 'quantity definitely increas|quantity certainly increas|quantity will increase|quantity increas|quantity rises|quantity rise|quantity go up|quantity goes up|higher quantity|quantity surely|quantity always'),
           P('p2', 'Price change uncertain', 3, 'price uncertain|price is uncertain|price change uncertain|price change is uncertain|price indeterminate|cannot say about price|price may rise or fall|price can go either|price depends|price is not certain|price not certain|cannot predict price|price may go up or down|price ambiguous|price unclear|price not always|price is not always|price change depends|price may rise fall or stay'),
           P('p3', 'Rises if demand shift bigger, falls if supply shift bigger, same if equal', 3, 'demand increases more|demand rises more|demand increase is more|bigger demand|larger demand|demand increase more|demand more than supply|demand shift larger|demand shift is larger|demand shift bigger', 'supply increases more|supply rises more|supply increase is more|bigger supply|larger supply|supply increase more|supply more than demand|supply shift larger|supply shift is larger|supply shift bigger', 'equally|equal|same amount|same extent|both increase equal|unchanged|stay the same|remain same|remains the same', min=2)], 'c6'),
        V('v5', 'What happens to price and quantity when demand increases and supply decreases at the same time?',
          'Price will certainly rise, because both changes push it up. But nothing certain can be said about quantity: it rises if the increase in demand is larger than the decrease in supply, and falls if the decrease in supply is larger.',
          [P('p1', 'Price certainly rises', 4, 'price certainly rise|price definitely rise|price will rise|price rises|price rise|price increas|price goes up|higher price|price surely|price always rise|price go up'),
           P('p2', 'Quantity uncertain', 3, 'quantity uncertain|quantity is uncertain|nothing certain|cannot say|quantity indeterminate|quantity may rise or fall|quantity can go either|quantity depends|quantity not certain|quantity is not certain|cannot predict|quantity ambiguous|either way|may increase or decrease|may go up or down'),
           P('p3', 'Depends on which shift is larger', 3, 'demand increase is larger|demand increase larger|demand shift is larger|demand shift larger|demand rises more|demand increases more|larger increase in demand|bigger increase in demand|increase in demand is larger|increase in demand is more|increase in demand larger|increase in demand more|demand increase more|which shift is larger|which shift larger|which shift is bigger|which change is larger|relative size of the shifts|relative size of the two shifts', 'supply decrease is larger|supply decrease larger|supply shift is larger|supply shift larger|supply falls more|supply decreases more|larger decrease in supply|bigger decrease in supply|decrease in supply is larger|decrease in supply is more|decrease in supply larger|decrease in supply more|supply decrease more', min=1)], 'c6'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Frost hits the apple orchards', 'difficulty': 'hard',
        'case': ('In a hill-state wholesale market, the weekly demand for apples (in crates) is Qd = 9,000 − 150P and supply is Qs = 1,500 + 100P, where P is the price per crate in ₹ hundreds. '
                 'A late frost destroys part of the crop, reducing supply by 750 crates at every price. Demand is unchanged in the first week after the frost.'),
        'mcqs': [
            M('k1a', 'Before the frost, the equilibrium price (₹ hundreds per crate) is:', ['30', '42', '25', '36'], 0, f'9,000 − 150P = 1,500 + 100P → 7,500 = 250P → P = {kp}.', 'moderate', '(9000-1500)/(150+100)'),
            M('k1b', 'Immediately after the frost, at the old price, the shortage of apples is:', ['750 crates', '4,500 crates', '3,750 crates', '1,500 crates'], 0, f'At P = 30: Qd = 4,500; new Qs = 750 + 3,000 = 3,750; shortage = {inr(kg)} crates.', 'hard', '(9000-150*30)-(750+100*30)'),
            M('k1c', 'The new equilibrium price (₹ hundreds per crate) is:', ['33', '30', '27', '36'], 0, f'9,000 − 150P = 750 + 100P → 8,250 = 250P → P = {kp1}; Q = {inr(kq1)} crates (down from {inr(kq)}).', 'hard', '(9000-750)/(150+100)'),
            M('k1d', 'If, in the second week, demand also falls because buyers switch to imported apples, the equilibrium quantity will:', ['Fall further, while the price effect depends on the relative size of the shifts', 'Rise, while price certainly falls', 'Stay the same', 'Rise and the price will rise'], 0, 'Supply down and demand down: quantity surely falls; price is uncertain.', 'moderate'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch04', 'n': 2, 'title': 'Determination of Prices',
        'outcomes': ['Explain how the interaction of demand and supply settles the equilibrium (market-clearing) price and why that equilibrium is stable.',
                     'Compute equilibrium price and quantity, and shortages or surpluses, from schedules and linear functions.',
                     'Predict the effect of a shift in demand or in supply on equilibrium price and quantity.',
                     'Analyse simultaneous changes in demand and supply and state which outcome is certain and which depends on the relative shifts.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 40}, 'prereq': ['fnd-p4-ch02-u01', 'fnd-p4-ch02-u03'],
                 'exam_tip': 'Simultaneous-shift MCQs are frequent. Memorise: same direction → quantity certain; opposite directions → price certain. For equation questions write P* = (a − c)/(b + d) and verify Q* in both functions.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Equilibrium price: Qd = Qs; the market clears.', 'Above equilibrium → surplus → price falls; below → shortage → price rises (stable equilibrium via the price mechanism).',
                        'Demand up → P up, Q up; demand down → P down, Q down.', 'Supply up → P down, Q up; supply down → P up, Q down.',
                        'Both up → Q up, P uncertain; both down → Q down, P uncertain.', 'D up & S down → P up, Q uncertain; D down & S up → P down, Q uncertain.'],
            'remember': ['Linear case: P* = (a − c)/(b + d) for Qd = a − bP, Qs = c + dP.', 'An increase in demand/supply changes the constant term, not the slope.', 'Government sometimes fixes prices (administered prices, MSP) — the model still shows the shortage or surplus that results.'],
            'traps': ['A change in price causes a movement along a curve, not a shift.', '"Supply rises" after a demand increase is wrong — quantity supplied extends.', 'Equal shifts in the same direction leave price unchanged, not quantity.']},
        'quickref': [{'k': 'Equilibrium', 'v': 'Qd = Qs'}, {'k': 'Linear equilibrium', 'v': 'P* = (a − c)/(b + d); Q* = a − bP*'}, {'k': 'Excess demand / supply', 'v': 'Qd − Qs (shortage) / Qs − Qd (surplus)'},
                     {'k': 'Same-direction shifts', 'v': 'Quantity certain, price uncertain'}, {'k': 'Opposite shifts', 'v': 'Price certain, quantity uncertain'}],
        'viva': viva, 'cases': cases,
    }
