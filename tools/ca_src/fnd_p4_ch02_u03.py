"""CA Foundation · Paper 4 Business Economics · Chapter 2 · Unit 3 Supply.
Original explanations, examples and questions (ICAI structure and scope only). Every figure is computed below."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch02-u03'


def Q(mid, q, opts, ans, ex, c, d='core', check=None):
    x = {'id': mid, 'q': q, 'options': opts, 'answer': ans, 'explain': ex, 'concept': c, 'difficulty': d}
    if check: x['check'] = check
    return x


def build():
    # ---------- i1 market supply ----------
    c1 = Checks()
    prices = [10, 20, 30, 40, 50]
    F1 = [0, 10, 20, 30, 40]; F2 = [5, 12, 18, 25, 30]; F3 = [0, 0, 8, 15, 22]
    msup = [c1.add(f'{a}+{b}+{c}', f'market supply at ₹{p_}') for p_, a, b, c in zip(prices, F1, F2, F3)]

    # ---------- i2 percentage method ----------
    c2 = Checks()
    es1 = c2.add('((3000-2400)/2400)/((550-500)/500)', 'Es percentage method')

    # ---------- i3 point elasticity from function ----------
    c3 = Checks()
    qs20 = c3.add('-200+30*20', 'Q at P = 20 for Q = −200 + 30P'); es20 = c3.add('30*20/400', 'Es at P = 20')
    qs40 = c3.add('-200+30*40', 'Q at P = 40'); es40 = c3.add('30*40/1000', 'Es at P = 40')
    qo = c3.add('25*20', 'Q at P = 20 for Q = 25P (through origin)'); eso = c3.add('25*20/500', 'Es for a line through the origin')

    # ---------- i4 arc ----------
    c4 = Checks()
    es_arc = c4.add('round(((900-600)/(900+600))*((60+45)/(60-45)),2)', 'arc Es')

    # ---------- i5 equilibrium ----------
    c5 = Checks()
    eq_p = c5.add('(500-50)/(10+5)', 'equilibrium price: 500 − 10P = 50 + 5P')
    eq_q = c5.add('500-10*30', 'equilibrium quantity')
    ex_d = c5.add('(500-10*20)-(50+5*20)', 'excess demand at ₹20')
    ex_s = c5.add('(50+5*40)-(500-10*40)', 'excess supply at ₹40')

    # ---------- questions ----------
    cq1 = Checks()
    q1_es = cq1.add('((5600-4000)/4000)/((1250-1000)/1000)', 'q1 Es')
    cq2 = Checks()
    q2_q = cq2.add('-50+10*15', 'q2 Q at P = 15'); q2_es = cq2.add('10*15/100', 'q2 Es at P = 15')
    q2_arc = cq2.add('round(((150-100)/(150+100))*((20+15)/(20-15)),2)', 'q2 arc Es between ₹15 and ₹20')
    q2_q20 = cq2.add('-50+10*20', 'q2 Q at P = 20')
    cq3 = Checks()
    q3_p = cq3.add('(1200-300)/(20+10)', 'q3 equilibrium price'); q3_q = cq3.add('1200-20*30', 'q3 equilibrium quantity')
    q3_p2 = cq3.add('(1200-450)/(20+10)', 'q3 new equilibrium price after supply rises by 150 at every price')
    q3_q2 = cq3.add('1200-20*25', 'q3 new equilibrium quantity')

    # ---------- case ----------
    k = Checks()
    k_es = k.add('((13000-10000)/10000)/((60-50)/50)', 'case Es for strawberries over a season')
    k_es_sr = k.add('((10500-10000)/10000)/((60-50)/50)', 'case Es in the first week')
    k_arc = k.add('round(((13000-10000)/(13000+10000))*((60+50)/(60-50)),2)', 'case arc Es')

    concepts = [
        {'id': 'c1', 'title': 'Meaning of supply',
         'body': ['Supply is the quantity of a good or service that producers are willing and able to offer for sale at various prices during a given period. Sellers may be individuals, firms or governments.',
                  'Three points: (1) supply is what is offered for sale, not necessarily what is actually sold — some of it may remain unsold; (2) it needs both willingness and ability to supply, and the cost of production mainly decides the ability; (3) supply is a flow — so much per day, week or year.',
                  'Supply differs from stock. Stock is the total quantity available with sellers at a point of time; supply is the part of it offered for sale at a given price. For perishable goods (fresh fish, flowers), supply tends to equal stock because they cannot be held back; for durable goods, sellers can keep part of the stock off the market if the price is low.'],
         'analogy': 'A mango seller\'s whole basket is his stock; the mangoes he puts on the cart at today\'s price are his supply.',
         'work': 'Inventory (stock) appears in the balance sheet; how much of it the company releases to the market at a given price is a supply decision — a link CAs see in working-capital reviews.'},
        {'id': 'c2', 'title': 'Determinants of supply',
         'body': ['(1) Price of the good — other things equal, a higher relative price makes production more profitable and raises quantity supplied. (2) Prices of related goods — if other goods a firm could produce become dearer, it shifts resources to them and supply of this good falls (a farmer switches from wheat to mustard when mustard prices rise). (3) Prices of factors of production — higher wages, raw-material or energy costs raise cost of production and reduce supply; cheaper inputs increase it.',
                  '(4) State of technology — better technology lowers cost per unit and increases supply. (5) Government policy — taxes (such as excise or GST) raise costs and reduce supply; subsidies lower costs and increase supply; quotas, licensing and regulation can restrict supply. (6) Nature of competition and size of the industry — under competition, supply tends to be larger than under monopoly. (7) Expectations — if prices are expected to rise, sellers may hold back supply now; expected falls lead them to sell more now. (8) Number of sellers — more firms in the market mean larger market supply. Other influences include natural factors such as weather for farm products.'],
         'analogy': 'Price is the accelerator for supply; costs, taxes and technology decide how powerful the engine is.',
         'work': 'Cost audits and margin analysis by CAs explain shifts in a client\'s supply capacity: a rise in input costs or a new tax shows up as reduced willingness to supply at the old price.'},
        {'id': 'c3', 'title': 'The law of supply: schedule and curve',
         'body': ['Producers are ready to sell a unit if the price at least covers the cost of producing that extra unit; the bigger the gap between price and that cost, the greater their willingness to supply.',
                  'Law of supply: other things remaining constant, the quantity of a good offered for sale rises as its price rises and falls as its price falls — a direct (positive) relationship. Reason: a higher price means higher profits and a stronger incentive to produce and sell.',
                  'A supply schedule tabulates prices and the quantities offered. The supply curve plots it and slopes upward from left to right. It shows at the same time the most that suppliers will offer at each price and the minimum price needed to coax out each quantity.',
                  'Market supply is the horizontal sum of all individual firms\' supplies at each price; it depends on everything that affects individual supply plus the number of firms.',
                  'Exception: the supply of labour at very high wages may fall — workers prefer more leisure once they earn enough (backward-bending supply of labour). Time also matters: supply is harder to raise in the short run than in the long run.'],
         'analogy': 'A higher price is like a bigger reward at a quiz — more people raise their hands.',
         'work': 'Capacity planning in manufacturing companies follows the supply curve: when realised prices rise, finance teams model the profitability of running extra shifts.'},
        {'id': 'c4', 'title': 'Movement along vs shift of the supply curve',
         'body': ['A change in the good\'s own price, other things constant, causes a movement along the same supply curve — a change in quantity supplied. A rise in price → expansion (extension) of supply, an upward movement along the curve; a fall in price → contraction of supply, a downward movement.',
                  'A change in any other determinant — input prices, technology, taxes and subsidies, prices of related goods, expectations, number of firms — shifts the whole supply curve. A rightward shift is an increase in supply: more is offered at each price (or the same quantity at a lower price). A leftward shift is a decrease in supply: less is offered at each price.',
                  'Examples: a new labour-saving machine shifts supply right; a rise in the GST rate or in diesel prices shifts supply left; a crop failure shifts farm supply left.'],
         'blocks': [table(['Cause', 'Term', 'On the graph'], [['Rise in own price', 'Expansion / increase in quantity supplied', 'Upward movement along the curve'], ['Fall in own price', 'Contraction / decrease in quantity supplied', 'Downward movement along the curve'],
                                                         ['Lower costs, better technology, subsidy', 'Increase in supply', 'Rightward shift'], ['Higher costs, tax, natural calamity', 'Decrease in supply', 'Leftward shift']], title='Movement vs shift')],
         'analogy': 'Moving along the supply curve is a factory running faster or slower on the same machines; a shift is the factory getting new machines (right) or losing some (left).',
         'work': 'When explaining a fall in a client\'s output to auditors or lenders, CAs separate "we chose to sell less because prices fell" (movement) from "our costs rose so we can offer less at any price" (shift).'},
        {'id': 'c5', 'title': 'Elasticity of supply: meaning and types',
         'body': ['Price elasticity of supply (Es) measures how much quantity supplied responds to a change in price: Es = % change in quantity supplied ÷ % change in price = (Δq/q) × (p/Δp). Because supply curves slope upward, Es is normally positive.',
                  'Types: perfectly inelastic (Es = 0) — quantity does not change, vertical supply curve (e.g. paintings of a dead artist, land in a city centre in the short run); relatively less elastic (0 < Es < 1) — quantity changes less than proportionately; unitary elastic (Es = 1) — equal proportionate change, the dividing line; relatively greater elastic (Es > 1) — quantity changes more than proportionately; perfectly elastic (Es = ∞) — horizontal curve: nothing is offered below the price, and any quantity is offered at it.',
                  'A useful rule for straight-line supply curves: a line through the origin has Es = 1 at every point; a line that cuts the price (Y) axis has Es > 1; a line that cuts the quantity (X) axis has Es < 1.'],
         'analogy': 'Elastic supply is a tap that opens wide with a small twist; inelastic supply is a rusty tap that barely moves however hard you turn it.',
         'work': 'Commodity analysts and CAs in agri-finance know that farm supply is inelastic within a season — prices swing sharply because quantity cannot respond until the next sowing.'},
        {'id': 'c6', 'title': 'Measuring elasticity of supply',
         'body': ['Percentage method: Es = (Δq/q) ÷ (Δp/p), using the original price and quantity as base.',
                  'Point method: Es = (dq/dp) × (p/q), where dq/dp is the derivative of the supply function. For a linear supply q = c + dP, dq/dp = d, so Es = d × P/q.',
                  'Arc method (mid-point) between two prices: Es = [(Q2 − Q1) ÷ (Q2 + Q1)] × [(P2 + P1) ÷ (P2 − P1)], where P1, Q1 are original and P2, Q2 new values. It gives the same answer whichever direction the price moves.'],
         'analogy': 'Same three rulers as for demand — only the sign is normally positive because price and quantity move together.',
         'work': 'Analysts estimate supply elasticity when forecasting how fast competitors will add capacity after a price rise.'},
        {'id': 'c7', 'title': 'Determinants of elasticity of supply',
         'body': ['(1) Behaviour of costs as output expands — if costs rise sharply, supply is less elastic; if costs stay roughly constant, it is elastic. (2) Complexity and time needed to produce — aircraft and ships have less elastic supply than motorbikes. (3) Time period — the longer the period, the more elastic; in the long run new plants are built and new firms enter. (4) Number of producers and ease of entry — many competing producers and low entry barriers make supply more elastic. (5) Spare capacity — firms working below full capacity can expand output without extra cost, so supply is more elastic.',
                  '(6) Availability of inputs — if key raw materials are easy and cheap to obtain, supply is elastic. (7) Stocks and storability — firms with stocks of materials and finished goods, and goods that can be stored cheaply without losing value, have more elastic supply. (8) Ease of factor substitution — commonly available, easily substitutable inputs make supply elastic; scarce, specialised or long-training inputs (doctors, chartered accountants) make it inelastic. (9) Mobility of factors — if capital and labour can switch easily between products (a printing press moving from magazines to greeting cards), supply is more elastic. (10) Expectations — if sellers expect prices to rise further, they respond less to a current price rise.'],
         'analogy': 'A street food stall can double its output tomorrow (elastic); a shipyard needs years (inelastic).',
         'work': 'Supply of qualified CAs is itself inelastic in the short run — years of training — which is why their fees rise quickly when demand spikes, for example during audit season or new compliance requirements.'},
        {'id': 'c8', 'title': 'Equilibrium price and social efficiency (link to demand)',
         'body': ['The equilibrium (market-clearing) price is where quantity demanded equals quantity supplied — the intersection of the demand and supply curves. Above it there is excess supply, which pushes price down; below it there is excess demand, which pushes price up. This is why microeconomics is also called price theory.',
                  'Social efficiency in a market is the total of consumer surplus and producer surplus. Producer surplus is what sellers receive above the minimum price at which they would have been willing to supply each unit — the region lying over the supply curve and under the market price. A competitive equilibrium maximises the sum of the two.'],
         'analogy': 'Equilibrium is the point where a tug-of-war between buyers and sellers stops moving.',
         'work': 'Fair-value measurement and transfer pricing both ask "what price would a willing buyer and willing seller agree on?" — the market-clearing idea in professional practice.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Market supply from individual supply schedules', 'difficulty': 'core', 'minutes': 5,
         'q': 'Three firms supply a product. Derive the market supply schedule and comment.',
         'given': [table(['Price (₹)', 'Firm 1', 'Firm 2', 'Firm 3'], [[p_, a, b, c] for p_, a, b, c in zip(prices, F1, F2, F3)])],
         'solution': [table(['Price (₹)', 'Firm 1', 'Firm 2', 'Firm 3', 'Market supply'], [[p_, a, b, c, mm] for p_, a, b, c, mm in zip(prices, F1, F2, F3, msup)], title='Horizontal summation'),
                      p(f'Market supply rises from {msup[0]} units at ₹10 to {msup[-1]} units at ₹50 — the law of supply. Firm 3 starts supplying only at ₹30, showing that higher prices also bring in higher-cost producers.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Elasticity of supply — percentage method', 'difficulty': 'core', 'minutes': 4,
         'q': 'When the price of a toy rises from ₹500 to ₹550, the quantity supplied rises from 2,400 to 3,000 units a month. Find Es and classify.',
         'solution': [p(f'% change in q = 600 ÷ 2,400 = 25%; % change in p = 50 ÷ 500 = 10%. Es = 25 ÷ 10 = {es1}. Supply is relatively greater elastic (Es > 1).')],
         'checks': c2},
        {'id': 'i3', 'title': 'Point elasticity from a supply function', 'difficulty': 'moderate', 'minutes': 7,
         'q': 'The supply function is q = −200 + 30P. Find Es at P = ₹20 and P = ₹40. Then find Es at P = ₹20 for the supply function q = 25P and comment.',
         'solution': [table(['Supply function', 'Price', 'q', 'Es = (dq/dp) × P/q'], [['q = −200 + 30P', 20, qs20, es20], ['q = −200 + 30P', 40, qs40, es40], ['q = 25P', 20, qo, eso]], title='Point elasticity'),
                      p(f'For q = −200 + 30P, dq/dp = 30: Es = {es20} at ₹20 and {es40} at ₹40 — elastic, falling towards 1 as price rises. This line cuts the price axis (at P ≈ 6.67), so Es > 1 throughout. For q = 25P, a line through the origin, Es = {eso} at every price.')],
         'checks': c3},
        {'id': 'i4', 'title': 'Arc elasticity of supply', 'difficulty': 'core', 'minutes': 5,
         'q': 'At ₹45 a kg, 600 kg of paneer is supplied; at ₹60, 900 kg. Find arc elasticity of supply.',
         'solution': [p(f'Es = [(900 − 600) ÷ (900 + 600)] × [(60 + 45) ÷ (60 − 45)] = (300 ÷ 1,500) × (105 ÷ 15) = 0.2 × 7 = {es_arc}. Supply is elastic.')],
         'checks': c4},
        {'id': 'i5', 'title': 'Equilibrium price from demand and supply functions', 'difficulty': 'moderate', 'minutes': 7,
         'q': 'Qd = 500 − 10P and Qs = 50 + 5P. Find the equilibrium price and quantity, and the excess demand or supply at ₹20 and ₹40.',
         'solution': [p(f'500 − 10P = 50 + 5P → 15P = 450 → P = ₹{eq_p}; Q = 500 − 10 × 30 = {eq_q} units.'),
                      table(['Price (₹)', 'Qd', 'Qs', 'Gap'], [[20, 500 - 200, 50 + 100, f'Excess demand {ex_d}'], [30, eq_q, eq_q, 'Equilibrium'], [40, 500 - 400, 50 + 200, f'Excess supply {ex_s}']], title='Market at three prices'),
                      p('Excess demand at ₹20 pushes the price up; excess supply at ₹40 pushes it down — until the market clears at ₹30.')],
         'checks': c5},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Why did vegetable prices spike?', 'role': 'CA in a food-processing company — procurement finance',
         'situation': 'Tomato prices doubled in two weeks after heavy rains. Management asks why suppliers did not simply supply more.',
         'steps': ['Identify the shift: rain damage reduced supply — a leftward shift of the supply curve.', 'Explain short-run inelasticity: crops cannot be grown in two weeks, so quantity cannot respond to the higher price.', 'Plan: long-term contracts with farmers, storage and processing capacity (tomato puree) to reduce exposure.'],
         'takeaway': 'Farm supply is inelastic in the short run; price shocks are large until the next harvest.'},
        {'id': 'j2', 'title': 'Impact of a subsidy on an EV maker\'s supply', 'role': 'CA in industry — strategy and planning',
         'situation': 'The government announces a production-linked incentive per electric scooter.',
         'steps': ['A subsidy lowers effective cost per unit — the supply curve shifts right.', 'Estimate the firm\'s supply elasticity: spare capacity and available battery supply decide how fast output can rise.', 'Model the new output and the incentive receivable, and the conditions attached.'],
         'takeaway': 'Subsidies shift supply right; how much output actually rises depends on elasticity of supply.'},
        {'id': 'j3', 'title': 'Pricing audit season staff', 'role': 'Partner in a mid-size CA firm',
         'situation': 'Demand for audit staff peaks in April–September; freelance rates jump 40%.',
         'steps': ['The supply of qualified staff is inelastic in the short run (long training).', 'Plan in advance: train articled assistants, schedule work across the year, use technology.', 'Expect elasticity to rise in the long run as more people qualify.'],
         'takeaway': 'Inelastic supply of skilled labour explains seasonal fee spikes; long-run planning raises elasticity.'},
    ]

    mcqs = [
        Q('m1', 'Supply refers to:', ['Quantity offered for sale at a price during a period', 'Total stock with the seller', 'Quantity actually sold', 'Quantity produced in a year regardless of price'], 0, 'Supply is what is offered at a given price per period.', 'c1'),
        Q('m2', 'Stock and supply are equal in the case of:', ['Highly perishable goods', 'Durable goods', 'Gold', 'Land'], 0, 'Perishables cannot be held back, so all stock is offered.', 'c1', 'moderate'),
        Q('m3', 'Supply is a flow concept because it is:', ['Measured per unit of time', 'Measured at a point of time', 'Always equal to demand', 'Fixed'], 0, 'So much per day/week/year.', 'c1'),
        Q('m4', 'A rise in the price of a factor of production, other things constant, will:', ['Decrease supply (shift left)', 'Increase supply (shift right)', 'Cause expansion of supply', 'Leave supply unchanged'], 0, 'Higher cost reduces willingness to supply at each price.', 'c2'),
        Q('m5', 'An improvement in technology will generally:', ['Shift the supply curve to the right', 'Shift the supply curve to the left', 'Cause a movement along the supply curve', 'Make supply perfectly inelastic'], 0, 'Lower unit cost → more supplied at each price.', 'c2'),
        Q('m6', 'A farmer grows less wheat when the price of mustard rises. This shows the effect of:', ['Prices of related goods on supply', 'Technology on supply', 'Taxes on supply', 'Consumer income'], 0, 'Resources move to the more profitable alternative.', 'c2'),
        Q('m7', 'If sellers expect the price of a good to rise next month, current supply is likely to:', ['Fall', 'Rise', 'Stay the same', 'Become infinite'], 0, 'They hold back stock to sell later.', 'c2', 'moderate'),
        Q('m8', 'A per-unit subsidy to producers will:', ['Increase supply', 'Decrease supply', 'Cause contraction of supply', 'Not affect supply'], 0, 'It lowers effective cost.', 'c2'),
        Q('m9', 'The law of supply states that, other things constant:', ['Quantity supplied varies directly with price', 'Quantity supplied varies inversely with price', 'Supply is independent of price', 'Supply equals demand'], 0, 'Positive relationship.', 'c3'),
        Q('m10', 'A supply curve shows:', ['The maximum quantity offered at each price and the minimum price needed for each quantity', 'Only the quantity sold', 'Consumer satisfaction', 'The cost of production only'], 0, 'Both readings are valid.', 'c3', 'moderate'),
        Q('m11', 'The market supply curve is obtained by:', ['Horizontal summation of individual supply curves', 'Vertical summation', 'Taking the average', 'Multiplying price by quantity'], 0, 'Add quantities at each price.', 'c3'),
        Q('m12', 'An exception to the law of supply is often seen in:', ['Supply of labour at very high wages', 'Supply of wheat', 'Supply of cloth', 'Supply of steel'], 0, 'Workers may choose more leisure beyond a certain income.', 'c3'),
        Q('m13', 'Three firms supply 30, 25 and 15 units at ₹40. Market supply at ₹40 is:', ['70', '30', '23.33', '55'], 0, '30 + 25 + 15 = 70. 23.33 is the average, not the sum.', 'c3', 'core', '30+25+15'),
        Q('m14', 'A rise in the price of a good, other things constant, causes:', ['Expansion of supply — upward movement along the curve', 'Increase in supply — rightward shift', 'Decrease in supply', 'Contraction of supply'], 0, 'Own-price change = movement along the curve.', 'c4'),
        Q('m15', 'A rise in the GST rate on a product will:', ['Shift the supply curve to the left', 'Shift the supply curve to the right', 'Cause expansion of supply', 'Make supply perfectly elastic'], 0, 'A tax raises effective cost.', 'c4'),
        Q('m16', 'An increase in supply means:', ['More is offered at each price', 'More is offered only because price has risen', 'Less is offered at each price', 'The supply curve becomes vertical'], 0, 'A rightward shift.', 'c4', 'moderate'),
        Q('m17', 'A vertical supply curve indicates elasticity of supply equal to:', ['0', '1', 'Infinity', 'Greater than 1'], 0, 'Perfectly inelastic supply.', 'c5'),
        Q('m18', 'A horizontal supply curve shows:', ['Perfectly elastic supply', 'Perfectly inelastic supply', 'Unitary elastic supply', 'Relatively less elastic supply'], 0, 'Es = ∞.', 'c5'),
        Q('m19', 'A straight-line supply curve passing through the origin has elasticity:', ['Equal to 1 at every point', 'Greater than 1', 'Less than 1', 'Zero'], 0, 'q/p and dq/dp are equal along such a line.', 'c5', 'moderate'),
        Q('m20', 'A straight-line supply curve that cuts the quantity axis has elasticity:', ['Less than 1', 'Greater than 1', 'Equal to 1', 'Infinite'], 0, 'Positive intercept on the quantity axis → Es < 1.', 'c5', 'hard'),
        Q('m21', 'Price rises from ₹500 to ₹550; quantity supplied rises from 2,400 to 3,000. Es is:', ['2.5', '0.4', '1.2', '10'], 0, '(600/2,400) ÷ (50/500) = 0.25 ÷ 0.10 = 2.5. 0.4 inverts the ratio.', 'c6', 'core', '((3000-2400)/2400)/((550-500)/500)'),
        Q('m22', 'Supply function q = −200 + 30P. Elasticity of supply at P = ₹20 is:', ['1.5', '30', '0.67', '1'], 0, 'q = 400; Es = 30 × 20 ÷ 400 = 1.5. 0.67 inverts; 30 is only dq/dp.', 'c6', 'hard', '30*20/(-200+30*20)'),
        Q('m23', 'Price rises from ₹45 to ₹60 and supply from 600 to 900 kg. Arc elasticity of supply is:', [str(es_arc), '1.5', '2', '0.67'], 0, '(300/1,500) × (105/15) = 0.2 × 7 = 1.4. 1.5 uses the original values as base.', 'c6', 'moderate', '((900-600)/(900+600))*((60+45)/(60-45))'),
        Q('m24', 'Elasticity of supply is generally greater in the:', ['Long run', 'Short run', 'Market period', 'It does not depend on time'], 0, 'More time to adjust capacity and entry.', 'c7'),
        Q('m25', 'Supply is likely to be more elastic when:', ['Firms have spare capacity', 'Inputs are scarce and specialised', 'Costs rise sharply with output', 'Production takes a long time'], 0, 'Spare capacity allows output to rise without extra cost.', 'c7'),
        Q('m26', 'Supply of aircraft is less elastic than supply of motorbikes mainly because:', ['Production is complex and takes longer', 'Aircraft are cheaper', 'There are more aircraft makers', 'Demand for aircraft is elastic'], 0, 'Complex, long processes reduce elasticity.', 'c7'),
        Q('m27', 'If factors of production are occupationally mobile, elasticity of supply is:', ['Higher', 'Lower', 'Zero', 'Unaffected'], 0, 'Factors can switch quickly between products.', 'c7'),
        Q('m28', 'Qd = 500 − 10P and Qs = 50 + 5P. Equilibrium price is:', ['₹30', '₹45', '₹15', '₹200'], 0, '500 − 10P = 50 + 5P → P = 450/15 = 30. ₹45 wrongly divides 450 by 10.', 'c8', 'moderate', '(500-50)/(10+5)'),
        Q('m29', 'At a price above equilibrium, there is:', ['Excess supply, pushing price down', 'Excess demand, pushing price up', 'No change', 'Equilibrium'], 0, 'Sellers cut prices to clear stocks.', 'c8'),
        Q('m30', 'Producer surplus is:', ['Price received minus the minimum price at which the seller would supply', 'Price minus consumer\'s willingness to pay', 'Total cost minus revenue', 'Same as consumer surplus'], 0, 'Area above the supply curve and below the price.', 'c8'),
    ]

    questions = [
        {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'The price of cement rises from ₹1,000 to ₹1,250 a tonne and supply rises from 4,000 to 5,600 tonnes a week. Compute elasticity of supply, classify it, and state two determinants that may explain the result.',
         'model': [p(f'% change in q = 1,600 ÷ 4,000 = 40%; % change in p = 250 ÷ 1,000 = 25%. Es = 40 ÷ 25 = {q1_es} — relatively greater elastic.'),
                   p('Possible reasons: spare capacity in cement plants; easy availability of limestone and fuel; many producers competing; the period considered long enough to adjust output.')],
         'scheme': [{'id': 's1', 'pt': 'Percentage changes', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'Es = 1.6', 'm': 1, 'skill': 'computation'}, {'id': 's3', 'pt': 'Classification', 'm': 0.5, 'skill': 'analysis'}, {'id': 's4', 'pt': 'Two relevant determinants', 'm': 1.5, 'skill': 'application'}],
         'remarks': ['Determinants must be of elasticity of supply, not of supply itself.'], 'mistakes': ['Listing "price of the good" as a determinant of elasticity.'], 'tips': ['Classify using the five types: 0, <1, 1, >1, ∞.'], 'checks': cq1},
        {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'The supply function of a firm is q = −50 + 10P. (a) Find point elasticity of supply at P = ₹15. (b) Find arc elasticity between ₹15 and ₹20. (c) Is supply elastic throughout? Explain using the intercept rule.',
         'model': [table(['Part', 'Working', 'Result'], [['(a)', f'q = −50 + 150 = {q2_q}; Es = 10 × 15 ÷ 100', q2_es], ['(b)', f'q at ₹20 = {q2_q20}; [(150 − 100)/(150 + 100)] × [(20 + 15)/(20 − 15)] = 0.2 × 7', q2_arc]]),
                   p('(c) Yes. The line q = −50 + 10P cuts the price axis at P = 5 (q = 0), so it starts from the price axis; such a linear supply curve has Es > 1 at every point, approaching 1 as price rises.')],
         'scheme': [{'id': 's1', 'pt': 'q at ₹15 and point Es', 'm': 2, 'skill': 'computation'}, {'id': 's2', 'pt': 'Arc Es with q at ₹20', 'm': 2, 'skill': 'computation'}, {'id': 's3', 'pt': 'Intercept-rule explanation', 'm': 1, 'skill': 'concept'}],
         'remarks': ['Good answers state dq/dp = 10 before substituting.'], 'mistakes': ['Using the percentage method in (b) instead of the arc formula.'], 'tips': ['Price-axis intercept → elastic; through origin → unitary; quantity-axis intercept → inelastic.'], 'checks': cq2},
        {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'text',
         'q': 'In a market Qd = 1,200 − 20P and Qs = 300 + 10P. (a) Find equilibrium price and quantity. (b) A new technology raises supply by 150 units at every price. Find the new equilibrium. (c) Is (b) an increase in supply or an expansion of supply? Explain.',
         'model': [p(f'(a) 1,200 − 20P = 300 + 10P → 30P = 900 → P = ₹{q3_p}; Q = 1,200 − 600 = {q3_q}.'),
                   p(f'(b) New Qs = 450 + 10P. 1,200 − 20P = 450 + 10P → 30P = 750 → P = ₹{q3_p2}; Q = 1,200 − 500 = {q3_q2}. Price falls (₹30 → ₹25) and quantity rises (600 → 700).'),
                   p('(c) It is an increase in supply — the whole supply curve shifts to the right because a non-price determinant (technology) changed. Expansion would mean more supplied only because the good\'s own price rose. Here the price actually fell while quantity rose.')],
         'scheme': [{'id': 's1', 'pt': 'Equilibrium price and quantity', 'm': 2, 'skill': 'computation'}, {'id': 's2', 'pt': 'New supply function and new equilibrium', 'm': 2.5, 'skill': 'computation'}, {'id': 's3', 'pt': 'Shift vs movement correctly explained', 'm': 1.5, 'skill': 'concept'}],
         'remarks': ['Write the new supply function explicitly — it shows the shift.'], 'mistakes': ['Adding 150 to the equilibrium quantity directly.', 'Calling it "expansion of supply".'], 'tips': ['Price falls and quantity rises after a rightward supply shift.'], 'checks': cq3},
    ]

    viva = [
        V('v1', 'State the law of supply.',
          'The law of supply states that, other things remaining constant, the quantity supplied of a good rises when its price rises and falls when its price falls. Price and quantity supplied are directly related, so the supply curve slopes upward.',
          [P('p1', 'Price up → quantity supplied up (direct relationship)', 6, ALT('{p} {u} {q} {u}', '{q} {u} {p} {u}', p=['price'], u=['rise', 'rises', 'increase', 'increases', 'goes up', 'higher', 'more'], q=['quantity supplied', 'supply', 'quantity', 'supplied']) + '|direct relation|directly relat|positive relation|positively relat|direct relationship|same direction|more at a higher price|more at higher price'),
           P('p2', 'Other things remaining constant', 2, 'other things|ceteris paribus|constant|same|unchanged'),
           P('p3', 'Supply curve slopes upward', 2, 'upward|positive slope|slopes up|rising curve|left to right upward|positively sloped')], 'c3'),
        V('v2', 'What is the difference between an increase in supply and an expansion of supply?',
          'An expansion of supply is a rise in quantity supplied caused only by a rise in the good\'s own price; it is an upward movement along the same supply curve. An increase in supply is caused by a change in some other factor, such as lower costs or better technology, and the whole supply curve shifts to the right so that more is offered at every price.',
          [P('p1', 'Expansion = due to rise in own price, movement along the curve', 5, ALT('{e} {x} {p}', '{e} {p}', e=['expansion', 'extension'], x=['caused', 'due', 'because', 'result', 'when', 'only', 'is', 'means', 'happens', 'rise'], p=['own price', 'its price', 'price of the good', 'price rise', 'rise in price', 'increase in price', 'price increase', 'price of good', 'its own price', 'price itself', 'price']) + '|movement along'),
           P('p2', 'Increase = other factors (cost, technology), curve shifts right', 5, ALT('{i} {x} {o}', '{i} {o}', i=['increase in supply'], x=['caused', 'due', 'because', 'result', 'when', 'is', 'means', 'happens'], o=['other', 'cost', 'technology', 'subsidy', 'input', 'non price', 'shift', 'tax']) + '|curve shifts right|shifts to the right|rightward shift|whole curve shift|whole supply curve shift')], 'c4'),
        V('v3', 'What is elasticity of supply, and when is supply perfectly inelastic?',
          'Elasticity of supply is the degree of responsiveness of quantity supplied to a change in price; we measure it as percentage change in quantity supplied over percentage change in price. Supply is perfectly inelastic when quantity supplied does not change at all whatever the price, so elasticity is zero and the supply curve is vertical.',
          [P('p1', 'Responsiveness of quantity supplied to price change', 3, 'responsive|response|sensitiv|reacts|reaction|degree of change', min=1),
           P('p2', '% change in quantity supplied ÷ % change in price', 3, 'per cent change in quantity|per cent change quantity|percentage change in quantity|percent change in quantity|proportionate change in quantity|percentage change in supply|change in quantity supplied divided|quantity supplied divided|delta q|percentage change of quantity'),
           P('p3', 'Perfectly inelastic: no change in quantity, Es = 0, vertical curve', 4, 'zero|0|vertical', 'no change|does not change|unchanged|remains same|remains the same|fixed|not change|not respond|stays the same|same quantity', min=1)], 'c5'),
        V('v4', 'Name any four determinants of elasticity of supply.',
          'Elasticity of supply depends on the time period, since supply is more elastic in the long run; on spare capacity; on how costs behave as output expands; on the availability and mobility of inputs and how easily factors can be substituted; on the number of producers and ease of entry; on stocks and storability; and on the complexity of production.',
          [P('p1', 'Names at least two determinants (time period, spare capacity, cost behaviour/complexity, inputs and factor mobility, number of producers/entry, storability)', 5, 'time|long run|short run|period', 'spare capacity|excess capacity|unused capacity|idle capacity|capacity', 'cost|complex|production process|difficult to produce', 'raw material|input|factor|mobil|substitut', 'number of producer|number of firm|entry|competition|many producer', 'stock|storab|storage|store|storing|inventor|perishab', min=2),
           P('p2', 'Names four determinants in all', 5, 'time|long run|short run|period', 'spare capacity|excess capacity|unused capacity|idle capacity|capacity', 'cost|complex|production process|difficult to produce', 'raw material|input|factor|mobil|substitut', 'number of producer|number of firm|entry|competition|many producer', 'stock|storab|storage|store|storing|inventor|perishab', min=4)], 'c7'),
        V('v5', 'Why does a straight-line supply curve passing through the origin have unit elasticity?',
          'For a straight line through the origin, quantity is proportional to price, so q by p equals dq by dp at every point. Since elasticity equals dq by dp multiplied by p by q, the two ratios cancel and elasticity equals one everywhere.',
          [P('p1', 'Quantity proportional to price (q/p = slope dq/dp)', 4, 'proportional|proportion|same ratio|q by p|q over p|q p equal|constant ratio|slope equal|equal to slope|ratio is constant|same percentage|equal percentage', min=1),
           P('p2', 'Es = (dq/dp)(p/q) → ratios cancel', 3, 'cancel|multiply|formula|dq dp|dq by dp|times p by q|into p by q|reciprocal|p by q', min=1),
           P('p3', 'So elasticity = 1 at every point', 3, 'one|1|unit|unity|unitary')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Strawberry season in Mahabaleshwar', 'difficulty': 'moderate',
              'case': ('Strawberry growers in a hill district supply 10,000 kg a week at ₹50 a kg. A heat wave elsewhere raises the price to ₹60. In the first week growers can only pick a little more fruit and supply rises to 10,500 kg. By the end of the season, after extra plots were brought into picking and labour was hired, weekly supply reached 13,000 kg at ₹60. '
                       'The state government is also considering a subsidy on drip irrigation for growers.'),
              'mcqs': [
                  Q('k1a', 'Elasticity of supply in the first week (percentage method) is:', [str(k_es_sr), '4', '0.05', '1.5'], 0, '(500/10,000) ÷ (10/50) = 0.05 ÷ 0.2 = 0.25 — inelastic. 4 inverts the ratio.', 'c6', 'moderate', '((10500-10000)/10000)/((60-50)/50)'),
                  Q('k1b', 'Elasticity of supply by the end of the season (percentage method) is:', [str(k_es), '0.67', '0.3', '1'], 0, '(3,000/10,000) ÷ (10/50) = 0.3 ÷ 0.2 = 1.5 — elastic.', 'c6', 'moderate', '((13000-10000)/10000)/((60-50)/50)'),
                  Q('k1c', 'The difference between (a) and (b) is best explained by:', ['The time period available to adjust supply', 'A change in consumer tastes', 'A change in the number of buyers', 'The law of diminishing marginal utility'], 0, 'Supply is more elastic in the longer run.', 'c7', 'core'),
                  Q('k1d', 'Arc elasticity of supply over the season (₹50/10,000 kg to ₹60/13,000 kg) is:', [str(k_arc), '1.5', '1.3', '0.7'], 0, '(3,000/23,000) × (110/10) ≈ 0.1304 × 11 = 1.43.', 'c6', 'hard', 'round(((13000-10000)/(13000+10000))*((60+50)/(60-50)),2)'),
                  Q('k1e', 'A subsidy on drip irrigation would:', ['Shift the supply curve of strawberries to the right', 'Cause expansion of supply along the same curve', 'Shift the demand curve to the right', 'Make supply perfectly inelastic'], 0, 'It lowers cost — a non-price determinant — so supply increases.', 'c4', 'core'),
              ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch02', 'n': 3, 'title': 'Supply',
        'outcomes': ['Explain the meaning of supply and distinguish it from stock.', 'List the determinants of supply and state the law of supply with its exception.',
                     'Distinguish movements along the supply curve from shifts of the curve.', 'Classify, measure (percentage, point, arc) and explain the determinants of elasticity of supply; find market equilibrium.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 45}, 'prereq': ['fnd-p4-ch02-u01'],
                 'exam_tip': 'MCQs often test the shift-vs-movement distinction (tax, subsidy, technology), the five types of supply elasticity and an Es calculation. The straight-line intercept rule is a quick win.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {'summary': ['Supply = quantity offered for sale at a price per period; needs willingness and ability; is a flow; ≠ stock.', 'Determinants: own price, related goods\' prices, factor prices, technology, government policy, competition/industry size, expectations, number of sellers.',
                                 'Law of supply: direct price–quantity relation, ceteris paribus; exception — labour at very high wages.', 'Own price → expansion/contraction (movement); other factors → increase/decrease (shift).',
                                 'Es = (Δq/q)/(Δp/p); point = (dq/dp)(p/q); arc = [(Q2−Q1)/(Q2+Q1)] × [(P2+P1)/(P2−P1)].', 'Types: 0 (vertical), <1, 1, >1, ∞ (horizontal). Line through origin = 1; from price axis > 1; from quantity axis < 1.'],
                     'remember': ['Supply is more elastic in the long run, with spare capacity, mobile and available inputs, many producers, storable goods.', 'Equilibrium: Qd = Qs; above it excess supply, below it excess demand.'],
                     'traps': ['A tax or input-cost rise is a leftward shift, not a contraction.', 'Market supply is a horizontal sum.', 'Do not confuse stock with supply.']},
        'quickref': [{'k': 'Es (percentage)', 'v': '(Δq/q) ÷ (Δp/p)'}, {'k': 'Es (point)', 'v': '(dq/dp) × p/q'}, {'k': 'Es (arc)', 'v': '[(Q2−Q1)/(Q2+Q1)] × [(P2+P1)/(P2−P1)]'},
                     {'k': 'Intercept rule', 'v': 'Origin → 1; price axis → >1; quantity axis → <1'}, {'k': 'Equilibrium', 'v': 'Qd = Qs'}],
        'viva': viva, 'cases': cases,
    }
