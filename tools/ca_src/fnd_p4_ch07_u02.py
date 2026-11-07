"""CA Foundation · Paper 4 Business Economics · Chapter 7 Public Finance · Unit 2 Market Failure / Government intervention to correct Market Failure.
Original explanations, numbers and questions."""
from lib import *
from ca_viva import P, ALT, V

UID = 'fnd-p4-ch07-u02'


def M(i, q, o, a, e, c=None, d='core', check=None, topic=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if topic: m['topic'] = topic
    if c: m['concept'] = c
    if check: m['check'] = check
    return m


def build():
    # ---- i1 social cost ----
    c1 = Checks()
    pmc, ext, out = 400, 60, 10000
    smc = c1.add('400+60', 'social cost per unit')
    tec = c1.add('60*10000', 'total external cost')
    tsc = c1.add('460*10000', 'total social cost')

    # ---- i2 externality equilibrium: P = 1000 - 2Q ; MPC = 200 + 2Q ; MEC = 80 ----
    c2 = Checks()
    qm = c2.add('(1000-200)/(2+2)', 'market output')
    pm = c2.add('1000-2*200', 'market price')
    qs = c2.add('(1000-200-80)/(2+2)', 'socially optimal output')
    ps = c2.add('1000-2*180', 'socially optimal price')
    over = c2.add('200-180', 'over-production')
    taxrev = c2.add('80*180', 'Pigouvian tax revenue at the optimum')

    # ---- i3 price ceiling / floor: Qd = 5000 - 20P ; Qs = 1000 + 20P ----
    c3 = Checks()
    pe = c3.add('(5000-1000)/(20+20)', 'equilibrium price')
    qe = c3.add('5000-20*100', 'equilibrium quantity')
    qd80 = c3.add('5000-20*80', 'Qd at ceiling 80')
    qs80 = c3.add('1000+20*80', 'Qs at ceiling 80')
    short = c3.add('3400-2600', 'shortage')
    qd120 = c3.add('5000-20*120', 'Qd at floor 120')
    qs120 = c3.add('1000+20*120', 'Qs at floor 120')
    surp = c3.add('3400-2600', 'surplus at floor')
    proc = c3.add('800*120', 'cost of procuring the surplus')

    # ---- i4 cap and trade ----
    c4 = Checks()
    noTA = c4.add('30*500', 'Firm A abatement cost without trade')
    noTB = c4.add('30*1200', 'Firm B abatement cost without trade')
    noT = c4.add('15000+36000', 'total cost without trade')
    tA = c4.add('60*500', 'Firm A abatement with trade')
    perm = c4.add('30*800', 'value of 30 permits at ₹800')
    netA = c4.add('30000-24000', 'Firm A net cost with trade')
    saving = c4.add('51000-30000', 'saving to society')

    # ---- questions ----
    q1 = Checks()   # P = 900 - 3Q ; MPC = 100 + Q ; MEC = 40
    q1m = q1.add('(900-100)/(3+1)', 'market Q')
    q1p = q1.add('900-3*200', 'market P')
    q1s = q1.add('(900-100-40)/(3+1)', 'optimal Q')
    q1ps = q1.add('900-3*190', 'optimal P')
    q1o = q1.add('200-190', 'over-production')
    q1t = q1.add('40*190', 'tax revenue')

    q2 = Checks()   # Qd = 12000 - 50P ; Qs = 2000 + 50P
    q2pe = q2.add('(12000-2000)/(50+50)', 'eq price')
    q2qe = q2.add('12000-50*100', 'eq qty')
    q2d = q2.add('12000-50*85', 'Qd at 85')
    q2s = q2.add('2000+50*85', 'Qs at 85')
    q2sh = q2.add('7750-6250', 'shortage')
    q2fd = q2.add('12000-50*110', 'Qd at 110')
    q2fs = q2.add('2000+50*110', 'Qs at 110')
    q2su = q2.add('7500-6500', 'surplus')
    q2c = q2.add('1000*110', 'procurement cost')

    q3 = Checks()
    q3a = q3.add('40*300', 'X cost no trade')
    q3b = q3.add('40*900', 'Y cost no trade')
    q3n = q3.add('12000+36000', 'total no trade')
    q3x = q3.add('80*300', 'X abates 80')
    q3r = q3.add('40*600', 'permit receipts')
    q3nx = q3.add('24000-24000', 'X net')
    q3s = q3.add('48000-24000', 'saving')

    k = Checks()
    kq = k.add('(600-100)/(1+1)', 'market Q case')
    ks = k.add('(600-100-50)/(1+1)', 'optimal Q case')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch07', 'n': 2,
        'title': 'Market Failure/ Government intervention to correct Market Failure',
        'outcomes': [
            'Define market failure, tell complete from partial market failure, and name its four main sources.',
            'Explain externalities (positive and negative, in production and in consumption), private versus social cost, public goods and the free-rider problem, and information failures — adverse selection and moral hazard.',
            'Describe how governments correct each kind of failure: competition law, direct controls, Pigouvian taxes, cap-and-trade, subsidies, merit and demerit good policies, price floors and ceilings, disclosure rules and redistribution.',
            'Work simple numerical problems on social cost, the socially optimal output, price controls and tradable permits, and recognise government failure.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 60, 'practice': 60}, 'prereq': ['fnd-p4-ch07-u01'],
                 'exam_tip': 'Expect statement-based MCQs: "adverse selection happens BEFORE the deal, moral hazard AFTER"; "not every good with a negative externality is a demerit good"; "Pigouvian tax = make the polluter pay". Learn the four-cell externality grid with one example each.'},
        'concepts': [
            {'id': 'c1', 'title': 'Introduction and the concept of market failure',
             'body': ['Economists assume people act rationally in their own interest. If markets worked perfectly, prices would send correct signals and the right quantity of every good would be produced at the right price. That does not always happen.',
                      'Market failure is a situation in which a free market allocates society\'s scarce resources inefficiently — producing too much or too little of some goods — so the outcome is less than optimal. It does not mean the market has stopped working; it means the market is not working as it should.',
                      'Complete market failure ("missing market"): the market supplies nothing at all even though people want the good — for example pure public goods such as national defence.',
                      'Partial market failure: the market works but delivers the wrong quantity or charges the wrong price, causing a loss of welfare.'],
             'analogy': 'A complete failure is a shop that never opens; a partial failure is a shop that opens but stocks the wrong amount at the wrong price.',
             'work': 'When a client asks why its industry is heavily regulated (power, telecom, pharma, insurance), the answer usually lies in a specific market failure — natural monopoly, externality or information gap.'},
            {'id': 'c2', 'title': 'Why do markets fail? — and market power',
             'body': ['Perfect competition (many small firms, perfect knowledge, identical products) would send resources to their highest-valued uses, so that no one can be made better off without making someone worse off. Real markets rarely meet these conditions.',
                      'Four major reasons for market failure: (1) market power, (2) externalities, (3) public goods, (4) incomplete information.',
                      'Market power (also called monopoly power) means a firm can push its price above marginal cost and still make a profit. A firm with such power is a price maker: it restricts output below the competitive level and charges a higher price. Its profits come from dominance, not efficiency, so society gets too little of the good at too high a price.'],
             'analogy': 'A single ferry operator on an island can run fewer trips and charge more — not because it is better, but because there is no other boat.',
             'work': 'Competition law practice (an area many CAs work in) asks whether a firm\'s high margins come from efficiency or from abuse of dominance.'},
            {'id': 'c3', 'title': 'Externalities — private cost and social cost',
             'body': ['An externality is an effect of production or consumption on third parties that is not reflected in market prices. Negative externalities impose costs on others; positive externalities confer benefits. They are also called spillover, neighbourhood, third-party or side effects. Because they bypass the price mechanism, nobody pays or is paid for them — they are uninternalised.',
                      'A change that works through prices (for example more people buying organic food pushing its price up) is NOT an externality.',
                      'Production externalities: negative, felt in consumption — a factory\'s effluent makes river water unsafe for families downstream; negative, felt in production — the same effluent reduces fishermen\'s catch; positive, felt in production — a firm trains workers who later join other firms; positive, felt in consumption — a beautiful private garden enjoyed by passers-by.',
                      'Consumption externalities: negative, felt in consumption — smoking in public, a loud music system; negative, felt in production — noisy students disturbing a class, heavy drinking lowering work output; positive, felt in consumption — vaccination protecting others; positive, felt in production — employees using a gym become more productive for the firm.',
                      'Private cost is what the firm pays (wages, materials, power) and records in its books; the market supply curve reflects only private marginal cost. Social cost = private cost + external cost. Likewise, social benefit = private benefit + external benefit.',
                      'Since prices ignore external costs and benefits, they send wrong signals: goods with negative externalities are over-produced and goods with positive externalities under-produced. That is market failure.'],
             'blocks': [table(['', 'Felt by consumers', 'Felt by producers'], [
                 ['Negative, from production', 'Polluted drinking water', 'Smaller fish catch'],
                 ['Positive, from production', 'Garden enjoyed by walkers', 'Trained workers move to other firms'],
                 ['Negative, from consumption', 'Passive smoking, loud music', 'Disruptive students, drunk workers'],
                 ['Positive, from consumption', 'Vaccination protects others', 'Fit employees work better']], title='The externality grid')],
             'analogy': 'A neighbour\'s barbecue party: the smoke in your window is a cost you did not agree to; the free music you enjoy is a benefit you did not pay for. Neither shows up in his bill.',
             'work': 'ESG and BRSR (Business Responsibility and Sustainability Reporting) work by CAs is largely about measuring and disclosing a company\'s externalities — emissions, water use, waste.'},
            {'id': 'c4', 'title': 'Public goods and the free-rider problem',
             'body': ['Paul Samuelson (1954, "The Pure Theory of Public Expenditure") developed the theory of public (collective consumption) goods: goods that all enjoy together, where one person\'s use does not reduce what is left for others.',
                      'Private goods are rival (my eating an apple means you cannot eat it) and excludable (non-payers can be kept out). Markets supply them well — food, clothing, cars, cinema tickets.',
                      'Public goods are non-rival (a street light serves every walker equally), non-excludable (once defence is provided, no resident can be shut out), and indivisible (everyone consumes the same total amount). The extra cost of one more user is zero, and no direct payment is made for pure public goods. Examples: national defence, law enforcement, lighthouses, street lighting, public sanitation, disease prevention, basic research.',
                      'Free-rider problem: since nobody can be excluded, people have no reason to pay — they can enjoy the good without paying. Profit-seeking firms cannot charge a price, so they produce too little or nothing. This is market failure (often complete).'],
             'analogy': 'A fireworks show over the city: everyone looks up for free, so no ticket seller can recover the cost — unless the city pays for it.',
             'work': 'Public-private partnership projects (toll roads, airports) work only when the "public good" can be made excludable — a toll booth or entry fee lets a private operator recover cost.'},
            {'id': 'c5', 'title': 'Incomplete information — adverse selection and moral hazard',
             'body': ['Competitive markets assume buyers and sellers know everything relevant. In reality information is incomplete because products are complex (heart surgery, mutual funds), correct information is hard to get, and some parties deliberately mislead (persuasive advertising).',
                      'Asymmetric information: one side knows more than the other — landlord vs tenant, borrower vs lender, used-car seller vs buyer, a health-insurance buyer vs the insurer, insiders vs ordinary investors.',
                      'Adverse selection arises BEFORE the transaction from hidden information. In health insurance, the insurer cannot tell high-risk from low-risk buyers, so it charges an average premium; high-risk people buy more cover, claims rise, premiums rise, and low-risk people drop out — until mostly unhealthy people remain or the market disappears (a missing market).',
                      'Akerlof\'s "market for lemons": used-car buyers cannot judge quality, so they offer a price based on average quality; owners of good cars withdraw, bad cars ("lemons") dominate, and quality and prices both fall. Asymmetric information drives high-quality goods out.',
                      'Moral hazard arises AFTER the transaction from hidden action: a party protected from the full cost of its behaviour takes more risk. A fully insured driver drives carelessly; a fully insured patient does not care about costly treatment. Insurers cannot watch behaviour cheaply, so premiums rise for everyone, and the market may shrink or vanish.'],
             'blocks': [table(['', 'Adverse selection', 'Moral hazard'], [['Timing', 'Before the deal', 'After the deal'], ['Problem', 'Hidden information (type/quality)', 'Hidden action (behaviour)'], ['Example', 'Only high-risk people buy insurance', 'Insured driver drives carelessly'], ['Typical remedies', 'Screening, mandatory disclosure, warranties', 'Deductibles, co-payment, monitoring']], title='Adverse selection vs moral hazard')],
             'analogy': 'Adverse selection: you cannot see inside the melon before buying. Moral hazard: you lent your bike and the borrower rides it carelessly because the repair bill is yours.',
             'work': 'Credit appraisal by bank CAs is a fight against both: due diligence and collateral reduce adverse selection; covenants and stock audits reduce moral hazard after the loan is given.'},
            {'id': 'c6', 'title': 'Government\'s role and intervention to minimise market power',
             'body': ['A free market still needs the state: physical infrastructure (roads, bridges, airports, waterways), institutional infrastructure (law, regulation, rule of law, property rights, enforcement of contracts) and a suitable competition and consumer law framework.',
                      'Against market power India has the Competition Act, 2002 (amended in 2007); the US has antitrust laws and the UK the Competition Act, 1998. They prohibit anti-competitive agreements, cartels, collusion and predatory pricing.',
                      'Other measures: opening monopoly sectors to competition (energy, telecom); controls on mergers and acquisitions that may create dominance; price caps and price regulation; profit or rate-of-return regulation; support for consumer associations; investigation of cartels and unfair practices; curbs on monopsony power; lower import controls; and nationalisation.',
                      'Sometimes government protects monopoly deliberately — patents and copyrights reward invention. Natural monopolies (electricity, gas, water supply) can supply the whole market at lower cost than several firms; they are allowed but their prices are regulated.'],
             'analogy': 'The referee does not ban strong players; he stops them from fouling. A patent is a temporary "reserved seat" given as a reward for innovation.',
             'work': 'Electricity tariff petitions before regulators are prepared largely by CAs — computing allowed costs and return on equity under rate-of-return regulation of a natural monopoly.'},
            {'id': 'c7', 'title': 'Government intervention to correct externalities',
             'body': ['Goal: internalise the externality — make those who cause it include the external cost (or benefit) in their own decisions.',
                      'Direct controls (command-and-control): emission standards with penalties; licences, production quotas and mandated processes; bans on certain goods; smoking bans in public places; strict rules on tobacco advertising and packaging; environmental laws such as the Environment (Protection) Act, 1986; compulsory pollution-control equipment (which raises firms\' average cost, so new firms enter only if price covers cost plus abatement); special bodies such as the Ministry of Environment and the Central and State Pollution Control Boards.',
                      'Market-based tools work through prices. (1) Pollution (Pigouvian) tax, after A. C. Pigou — the polluter pays per unit of pollution, raising private cost and cutting output. Problems: hard and costly to measure and administer; weak effect if demand is inelastic (firms pass the tax on); may push firms to relocate to low-tax countries, hurting jobs and investment.',
                      '(2) Tradable emission permits (cap-and-trade): the government caps total emissions by issuing a fixed number of permits; firms that cut pollution cheaply sell spare permits, high-cost abaters buy them. Each unit of pollution now has an opportunity cost. The cap fixes the quantity of pollution, and pollution is cut at the least total cost; but firms with inelastic demand can pass on the permit cost. The US used it for sulphur dioxide from 1994.',
                      'India has no explicit carbon price, but has implicit ones: the Perform, Achieve and Trade (PAT) scheme, a cess on coal, lignite and peat (replaced in 2017 by the GST compensation cess), Renewable Purchase Obligations and Renewable Energy Certificates, internal carbon pricing; the Energy Conservation (Amendment) Bill, 2022 empowers the Union to set up a carbon credit trading scheme.',
                      'Positive externalities lead to under-production, so government gives corrective subsidies to producers (e.g. fertiliser subsidy) or consumers (e.g. subsidised education fees), or produces directly (public education, health care, basic research, afforestation, sewage treatment, cleaning toxic sites).'],
             'analogy': 'A Pigouvian tax sets the price of pollution and lets the quantity adjust; cap-and-trade sets the quantity of pollution and lets the price adjust.',
             'work': 'Companies under PAT or carbon-credit schemes need CAs to account for certificates and permits (as assets, liabilities or inventory) and to verify reported savings.'},
            {'id': 'c8', 'title': 'Merit goods and demerit goods',
             'body': ['Merit goods have large positive externalities and are socially desirable — education, health care, housing, fire protection, waste management, libraries, museums, parks. Markets can supply them but under-produce and people under-consume them.',
                      'Responses: regulation (how education is imparted; compulsory insurance; compulsory immunisation; laws on helmets and seat belts), compulsion (the RTE Act, 2009 makes schooling free and compulsory for ages six to fourteen; compulsory treatment for contagious disease), subsidies, direct provision, provision free at the point of use (free hospital treatment), or a public–private combination.',
                      'Demerit goods are socially undesirable — cigarettes, alcohol, intoxicating drugs. Free markets over-produce and over-consume them. Not every good with a negative externality is a demerit good — steel making pollutes but steel is not undesirable.',
                      'Responses: outright ban (narcotics); negative advertising campaigns; bans on advertising and promotion; restricting access, especially for children; spatial and time restrictions (no smoking in public places, no tobacco sale near schools, sale banned at certain hours); very high taxes (see the GST rates on tobacco); a minimum price below which the good may not be sold.',
                      'Limits: demand for cigarettes and alcohol is usually price-inelastic, so taxes reduce consumption less than proportionately and sellers pass taxes on; total bans often push the trade underground into black markets.'],
             'analogy': 'Merit goods are vegetables the market under-serves; demerit goods are junk food it over-serves. The government is the parent adjusting the plate.',
             'work': 'Excise and GST planning for tobacco and liquor clients — some of the most heavily taxed goods in India — is a specialised practice area for CAs.'},
            {'id': 'c9', 'title': 'Public goods and price intervention (non-market pricing)',
             'body': ['Direct provision by government overcomes free-riding: defence, the legal system, fire protection and disease prevention are almost always publicly provided.',
                      'Excludable public goods (parks, universities, museums) may be financed by entry fees, or a licensed private firm may build them and charge users at a regulated fee. Some are funded by voluntary contributions, corporate donations and NGOs. Some goods that could be private are kept public because profit motives could endanger society — drug approval, atomic energy, airport security.',
                      'Price controls are legal limits on prices. A price ceiling (maximum price) is set below equilibrium to keep essentials affordable, e.g. caps on food-grain prices in scarcity or rent control; it creates a shortage (demand exceeds supply), queues and possible black markets.',
                      'A price floor (minimum price) is set above equilibrium to protect sellers, e.g. minimum wages and Minimum Support Price (MSP) for crops with government procurement; it creates a surplus that the government may buy.',
                      'Buffer stocks: the government buys grain in good harvests and releases it in poor years to keep prices and supply stable.'],
             'analogy': 'A ceiling is a low roof — the price cannot rise through it, so demand piles up beneath it (shortage). A floor is a raised platform — the price cannot fall below it, so unsold goods pile up on it (surplus).',
             'work': 'Food-processing and agri-trading clients must plan for MSP and procurement policies; their CAs model the impact on raw material cost.'},
            {'id': 'c10', 'title': 'Correcting information failure, equitable distribution and government failure',
             'body': ['Information failure remedies: compulsory accurate labelling and content disclosure (health warnings on cigarettes, nutrition labels on food); mandatory disclosure in financial markets (SEBI requires accurate information to investors in new issues); public information campaigns; regulation of advertising standards.',
                      'Equitable distribution: progressive income tax, transfer payments and unemployment benefits, subsidies, targeted spending in the budget, social security, reservation in jobs, land reforms and gender budgeting; also action against the black economy. Interventions that reduce efficiency but increase equity are often justified because society values equity.',
                      'Government failure: intervention meant to correct a market failure itself creates inefficiency or misallocation — when it is ineffective and wastes resources, or when it creates new and worse problems. Every intervention has costs and benefits that must be weighed.'],
             'analogy': 'A doctor who prescribes the wrong medicine can make the patient worse — government failure is the economy\'s version of a bad prescription.',
             'work': 'Audit and disclosure rules (Companies Act, SEBI LODR) exist precisely to fix information asymmetry between managers and investors — the auditor is the economy\'s information-failure specialist.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Private cost, external cost and social cost', 'difficulty': 'core', 'minutes': 4,
             'q': f'A dyeing unit\'s private cost is ₹{pmc} per metre of cloth. Its effluent causes health and cleaning costs to villagers estimated at ₹{ext} per metre. It produces {inr(out)} metres. Find the social cost per metre, total external cost and total social cost. What per-unit tax would internalise the externality?',
             'solution': [table(['Item', 'Per metre ₹', 'Total ₹'], [['Private cost', pmc, pmc * out], ['External cost', ext, tec], ['Social cost', smc, tsc]], num=[1, 2], total=True),
                          p(f'Social cost = private cost + external cost = {pmc} + {ext} = ₹{smc} per metre. A Pigouvian tax of ₹{ext} per metre (equal to the marginal external cost) makes the unit bear the full social cost.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Over-production under a negative externality', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'Market demand for a chemical is P = 1000 − 2Q and the industry\'s private marginal cost (supply) is P = 200 + 2Q. Each unit causes external damage of ₹80. Find (a) the market equilibrium, (b) the socially optimal output and price, (c) the over-production, and (d) the tax revenue if a Pigouvian tax of ₹80 per unit is imposed.',
             'solution': [p(f'(a) Market: 1000 − 2Q = 200 + 2Q → 4Q = 800 → Q = {qm} units; P = 1000 − 2×{qm} = ₹{pm}.'),
                          p(f'(b) Social marginal cost = 200 + 2Q + 80 = 280 + 2Q. Optimum: 1000 − 2Q = 280 + 2Q → 4Q = 720 → Q = {qs} units; P = 1000 − 2×{qs} = ₹{ps}.'),
                          p(f'(c) Over-production = {qm} − {qs} = {over} units: the market ignores the ₹80 damage, so too much is produced at too low a price.'),
                          p(f'(d) With a ₹80 tax, supply becomes 280 + 2Q and output falls to the optimum {qs}; tax revenue = 80 × {qs} = ₹{inr(taxrev)}.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Price ceiling and price floor', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'For a pulse, Qd = 5,000 − 20P and Qs = 1,000 + 20P (Q in quintals, P in ₹ per quintal). Find the equilibrium. What happens if (a) the government fixes a maximum price of ₹80, (b) it fixes a support price of ₹120 and buys any surplus? What does procurement cost?',
             'solution': [p(f'Equilibrium: 5,000 − 20P = 1,000 + 20P → P = ₹{pe}; Q = {inr(qe)} quintals.'),
                          table(['Situation', 'Price ₹', 'Qd', 'Qs', 'Result'], [['Equilibrium', pe, qe, qe, 'Market clears'], ['(a) Ceiling', 80, qd80, qs80, f'Shortage of {short}'], ['(b) Floor', 120, qd120, qs120, f'Surplus of {surp}']]),
                          p(f'(b) The government must buy the surplus of {surp} quintals at ₹120 per quintal, an outlay of {surp} × 120 = ₹{inr(proc)}. A ceiling below equilibrium causes shortages and queues; a floor above it causes surpluses.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Why cap-and-trade is cheaper', 'difficulty': 'hard', 'minutes': 10,
             'q': 'Firms A and B each emit 100 tonnes. The government wants total emissions cut by 60 tonnes and issues 70 permits to each firm (cap = 140). A can cut emissions at ₹500 a tonne, B at ₹1,200 a tonne. Compare the cost (a) if each firm must cut 30 tonnes itself, (b) if A cuts 60 tonnes and sells its 30 spare permits to B at ₹800 each.',
             'solution': [table(['', 'No trading ₹', 'With trading ₹'], [['Firm A abatement', noTA, tA], ['Firm B abatement', noTB, 0], ['Total abatement cost to society', noT, tA]], num=[1, 2]),
                          p(f'With trading A earns {inr(perm)} from selling permits, so its net cost is {inr(tA)} − {inr(perm)} = ₹{inr(netA)} (better than ₹{inr(noTA)}). B pays ₹{inr(perm)} for permits instead of ₹{inr(noTB)} of abatement. The same 60 tonnes are cut, but society saves ₹{inr(saving)} because the cheaper abater does the cutting.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Pricing a health-insurance product', 'role': 'CA in an insurer\'s finance and actuarial support team',
             'situation': 'Claims on a new no-medical-test policy are far above expectations.',
             'steps': ['Recognise adverse selection: without tests, high-risk buyers are over-represented.', 'Propose screening — medical tests above an age, waiting periods for pre-existing illness.',
                       'Recognise moral hazard in claims: add co-payment or deductibles so policyholders share costs.', 'Recompute the premium on the revised risk pool.'],
             'takeaway': 'Information-failure theory explains real product design choices — waiting periods, co-pay and medical tests.',
             'think': 'Which of the two problems does a co-payment clause mainly address?', 'answer': 'Moral hazard — it makes the insured bear part of the cost of their behaviour after the policy is bought.'},
            {'id': 'j2', 'title': 'Carbon credits in the books', 'role': 'CA in a steel company',
             'situation': 'The company exceeded its PAT target and received energy-saving certificates it can sell.',
             'steps': ['Identify the scheme as a market-based tool that internalises an externality.', 'Value the certificates and decide whether to sell or hold for future shortfalls.', 'Disclose the scheme and its impact in sustainability reporting.'],
             'takeaway': 'Tradable permits turn pollution reduction into a revenue opportunity for efficient firms — exactly the incentive the theory predicts.'},
            {'id': 'j3', 'title': 'Advising a restaurant chain on a price cap', 'role': 'CA in practice',
             'situation': 'A city caps the price of a staple meal below the market rate.',
             'steps': ['Explain that a ceiling below equilibrium creates excess demand — longer queues and pressure on quality.', 'Estimate the volume increase and cost per plate at the capped price.', 'Advise on whether to continue the item, reduce portion or seek a subsidy.'],
             'takeaway': 'Price controls change behaviour on both sides of the market; the business must plan for the shortage they create.'},
        ],
        'mcqs': [
            M('m1', 'Market failure means that:', ['The market allocates resources inefficiently', 'The market has stopped functioning completely in every case', 'Prices are always zero', 'The government has failed to collect taxes'], 0, "Market failure means the free market allocates resources inefficiently — producing too much of some goods and too little of others compared with what is best for society. The trap is 'the market has stopped functioning completely in every case': total breakdown (a missing market) is only the extreme form; most failures are partial. In practice: economists at SEBI or CCI study markets that still operate but deliver poor outcomes, such as excess pollution or overpricing.", 'c1', topic='The Concept of Market Failure'),
            M('m2', 'When a market does not supply a good at all even though people want it, it is:', ['Complete market failure (missing market)', 'Partial market failure', 'Government failure', 'Moral hazard'], 0, 'When people want a good but the market supplies none of it, that is complete market failure, also called a missing market — pure public goods like national defence are the classic case. Partial market failure is the trap: there the market works but supplies the wrong quantity or price. In practice: no private firm in India would supply lighthouses or national defence for profit, so the state provides them through the budget.', 'c1', topic='The Concept of Market Failure'),
            M('m3', 'Identify the item that is NOT among the four major sources of market failure:', ['Perfect competition', 'Market power', 'Externalities', 'Incomplete information'], 0, 'The four major sources of market failure are market power, externalities, public goods and incomplete information. Perfect competition is not a source of failure; it is the efficient benchmark against which failures are measured. Incomplete information is a tempting pick because it sounds like normal life, but it is a genuine source. In practice: competition and consumer-protection regulators in India target exactly these four problems.', 'c2', topic='Why Do Markets Fail?'),
            M('m4', 'Market power is best described as the ability of a firm to:', ['Profitably raise price above marginal cost', 'Produce at the lowest average cost', 'Sell any quantity at the market price', 'Avoid paying taxes'], 0, "Market power is a firm's ability to raise its price profitably above marginal cost — it restricts output and earns extra profit because buyers lack alternatives. 'Sell any quantity at the market price' is the trap: that describes a price-taking firm in perfect competition, which has no market power. In practice: the Competition Commission of India examines whether dominant platforms or cement makers price above cost due to market power.", 'c2', topic='Why Do Markets Fail?'),
            M('m5', 'A rise in the price of organic vegetables because more people now prefer them is:', ['Not an externality — it works through the price mechanism', 'A negative consumption externality', 'A positive production externality', 'A public good problem'], 0, 'An externality is an effect on third parties that operates outside the price system. When more people want organic vegetables and their price rises, the effect passes through the market price, so it is not an externality (economists call it a pecuniary effect). Calling it a negative consumption externality is the trap. In practice: a restaurant paying more for organic produce cannot claim it is harmed by an externality — that is normal market adjustment.', 'c3', 'hard', topic='Why Do Markets Fail?'),
            M('m6', 'Effluent from a factory reduces the catch of fishermen downstream. This is a:', ['Negative production externality received in production', 'Negative consumption externality received in consumption', 'Positive production externality', 'Negative production externality received in consumption'], 0, "The harm starts in production (the factory's effluent) and falls on another producer (fishermen, whose catch falls), so it is a negative production externality received in production. The tempting 'received in consumption' would apply if households, say, suffered from dirty drinking water. In practice: the National Green Tribunal has ordered polluting industries along Indian rivers to pay compensation to affected fishing and farming communities.", 'c3', 'moderate', topic='Why Do Markets Fail?'),
            M('m7', 'Employees who use a health club become more productive, benefiting their employer. This is a:', ['Positive consumption externality received in production', 'Positive production externality received in consumption', 'Negative consumption externality', 'Merit good failure'], 0, "The activity is consumption (employees using a health club), and the benefit lands on production (the employer gains from more productive workers) — a positive consumption externality received in production. The trap reverses the direction, 'production externality received in consumption'. In practice: many Indian companies subsidise gym memberships or wellness programmes because healthier employees take fewer sick days and work better.", 'c3', 'moderate', topic='Why Do Markets Fail?'),
            M('m8', 'Social cost equals:', ['Private cost + external cost', 'Private cost − external cost', 'External cost only', 'Private cost × external cost'], 0, "Social cost is the full cost to society: private cost (what the producer pays for inputs) plus external cost (damage borne by third parties, such as pollution). 'Private cost − external cost' is the trap — external cost is an extra burden, so it must be added, not subtracted. In practice: environmental impact assessments for Indian projects try to estimate external costs so that decision makers see the true social cost.", 'c3', topic='Why Do Markets Fail?'),
            M('m9', f'A firm\'s private cost is ₹250 per unit and external cost ₹35 per unit. The social cost per unit is:', ['₹285', '₹215', '₹250', '₹35'], 0, 'Social cost = private cost + external cost = ₹250 + ₹35 = ₹285 per unit. The tempting ₹215 subtracts the external cost instead of adding it; ₹250 ignores the externality, which is exactly what an unregulated firm does; ₹35 is the external cost alone. In practice: a Pigouvian tax of ₹35 per unit would make the firm face the full ₹285 social cost when deciding output.', 'c3', 'core', '250+35', topic='Why Do Markets Fail?'),
            M('m10', 'Under a negative production externality, a free market tends to:', ['Over-produce the good at too low a price', 'Under-produce the good at too high a price', 'Produce the socially optimal quantity', 'Produce nothing'], 0, "With a negative production externality, the firm ignores the external cost, so its private supply curve lies below the social cost curve: it produces more than the social optimum and sells at too low a price. 'Under-produce at too high a price' is the trap — that pattern fits positive externalities or market power. In practice: thermal power and cement plants in India would over-pollute without emission norms because they do not pay for the damage.", 'c3', topic='Why Do Markets Fail?'),
            M('m11', 'A good that is non-rival and non-excludable is a:', ['Public good', 'Private good', 'Merit good', 'Club good'], 0, "A pure public good is non-rival (one person's use does not reduce another's) and non-excludable (non-payers cannot be kept out) — national defence or street lighting, for example. 'Club good' is the trap: club goods are non-rival but excludable, like a members-only swimming pool or cable TV. In practice: because public goods cannot charge users, the Union and State budgets fund defence, policing and street lights.", 'c4', topic='Public Goods'),
            M('m12', 'The free-rider problem arises mainly because public goods are:', ['Non-excludable', 'Rival in consumption', 'Produced by monopolies', 'Inferior goods'], 0, "Free riding happens because public goods are non-excludable: if you cannot be stopped from enjoying the good, you have no incentive to pay for it, so private supply collapses. 'Rival in consumption' is the trap — public goods are non-rival; rivalry is a feature of private goods. In practice: a housing society's common security guard suffers free riding when some flats refuse to pay maintenance yet still benefit.", 'c4', topic='Public Goods'),
            M('m13', 'The concept of the "collective consumption good" was developed by:', ['Paul A. Samuelson', 'A. C. Pigou', 'George Akerlof', 'Milton Friedman'], 0, "Paul A. Samuelson introduced the 'collective consumption good' concept in his 1954 paper The Pure Theory of Public Expenditure. Pigou is the tempting trap because he is linked with externalities and Pigouvian taxes, not public goods theory; Akerlof is linked to the lemons problem. In practice: Samuelson's analysis underlies how finance ministries justify tax-funded public goods such as defence and basic research.", 'c4', topic='Public Goods'),
            M('m14', 'The marginal cost of providing a pure public good to one more user is:', ['Zero', 'Equal to the average cost', 'Rising', 'Infinite'], 0, "Because a pure public good is non-rival, letting one more person enjoy it costs nothing extra — the marginal cost of an additional user is zero. 'Equal to the average cost' is the trap: average cost is positive because the good had to be built, but serving one more user adds nothing. In practice: an extra viewer of a public fireworks display or an extra car under a street light adds no cost to the municipality.", 'c4', topic='Public Goods'),
            M('m15', 'Only people with high health risks buying insurance, which pushes premiums up and drives healthy people out, illustrates:', ['Adverse selection', 'Moral hazard', 'Free riding', 'Crowding out'], 0, 'When only high-risk people buy insurance, insurers raise premiums, which drives healthy people out and worsens the pool — adverse selection, caused by hidden information before the contract. Moral hazard is the trap: it concerns behaviour after the contract is signed. In practice: Indian health insurers use waiting periods for pre-existing diseases and medical tests to reduce adverse selection.', 'c5', topic='Incomplete Information'),
            M('m16', 'A person drives carelessly after buying comprehensive motor insurance. This is:', ['Moral hazard', 'Adverse selection', 'A positive externality', 'Price discrimination'], 0, 'Driving carelessly after buying comprehensive motor insurance is moral hazard — hidden action after the contract, because the insured no longer bears the full cost of an accident. Adverse selection is the trap: it involves hidden information before signing. In practice: Indian motor insurers use no-claim bonuses and compulsory deductibles so that policyholders still have an incentive to drive carefully.', 'c5', topic='Incomplete Information'),
            M('m17', 'Akerlof\'s "lemons problem" shows that asymmetric information can:', ['Drive high-quality goods out of the market', 'Raise the average quality of goods', 'Make markets perfectly competitive', 'Eliminate moral hazard'], 0, "In Akerlof's lemons model, buyers cannot tell good used cars from bad ones, so they offer only an average price. Owners of good cars find that too low and withdraw, leaving mostly 'lemons' — high-quality goods are driven out. 'Raise the average quality' is the trap; quality actually falls. In practice: certified pre-owned car programmes run by Indian dealers offer inspections and warranties to counter this problem.", 'c5', 'moderate', topic='Incomplete Information'),
            M('m18', 'Which statement is correct?', ['Adverse selection arises before a transaction; moral hazard after it', 'Moral hazard arises before a transaction; adverse selection after it', 'Both arise only in public goods', 'Both are forms of market power'], 0, 'Adverse selection arises before a transaction, from hidden information (the buyer or seller knows something the other does not). Moral hazard arises after a transaction, from hidden action (behaviour changes once protected). The swapped version is the trap. In practice: banks screen loan applicants to reduce adverse selection and then add covenants and monitoring to curb moral hazard once the loan is disbursed.', 'c5', 'moderate', topic='Incomplete Information'),
            M('m19', 'India\'s main law to promote competition and curb anti-competitive practices is the:', ['Competition Act, 2002', 'Environment (Protection) Act, 1986', 'FRBM Act, 2003', 'RBI Act, 1934'], 0, 'The Competition Act, 2002 (amended in 2007) prohibits anti-competitive agreements, abuse of dominance and harmful combinations, and is enforced by the Competition Commission of India. The FRBM Act, 2003 is the trap — it is a fiscal-discipline law on deficits. The RBI Act, 1934 governs the central bank. In practice: CAs advising on mergers check whether the deal crosses CCI notification thresholds under the Competition Act.', 'c6', topic='Government Intervention to Minimize Market Power'),
            M('m20', 'Governments allow natural monopolies in electricity and water supply but usually:', ['Regulate their prices', 'Ban them after five years', 'Exempt them from all regulation', 'Force them to sell at zero price'], 0, "Natural monopolies — electricity distribution or water supply — can serve a market most cheaply with a single firm, so governments allow them but regulate their prices to stop them exploiting consumers. 'Exempt them from all regulation' is the trap, which would invite monopoly pricing. In practice: State Electricity Regulatory Commissions in India fix power tariffs after examining the distribution company's costs, often with CA firms preparing the tariff petitions.", 'c6', topic='Government Intervention to Minimize Market Power'),
            M('m21', 'A tax levied on a polluter equal to the external damage it causes is called a:', ['Pigouvian tax', 'Progressive tax', 'Lump-sum tax', 'Compensation cess'], 0, "A Pigouvian tax, named after A. C. Pigou, is a per-unit tax on the polluter equal to the external damage it causes, so the polluter faces the full social cost. 'Compensation cess' is the trap: in India that is the GST cess used to compensate States, not a tax sized to external damage. In practice: the coal cess (Clean Environment Cess) once levied in India was designed along these lines.", 'c7', topic='Government Intervention to Correct Externalities'),
            M('m22', 'Which is a limitation of pollution taxes?', ['If demand is inelastic, firms pass on the tax and pollution falls little', 'They put an absolute cap on pollution', 'They need no monitoring', 'They always increase employment'], 0, "If demand for the polluting product is price-inelastic, the firm can pass most of the tax on to buyers, so quantity sold — and pollution — falls only a little. 'They put an absolute cap on pollution' is the trap: a tax fixes the price of pollution, not its quantity; caps come from permits. In practice: fuel taxes in India are high, yet petrol demand falls little because it is inelastic, so emissions barely drop.", 'c7', 'moderate', topic='Government Intervention to Correct Externalities'),
            M('m23', 'Under cap-and-trade, the government directly fixes:', ['The total quantity of emissions', 'The price of each permit', 'The tax rate per unit of pollution', 'Each firm\'s output'], 0, "Under cap-and-trade, the government fixes the total quantity of emissions (the cap) and issues permits; firms then trade permits, and the market sets the permit price. 'The price of each permit' is the trap — that is set by trading, not the government. In practice: the Gujarat Pollution Control Board's particulate-emission trading scheme for industries in Surat, launched in 2019, works on this cap-and-trade principle.", 'c7', 'moderate', topic='Government Intervention to Correct Externalities'),
            M('m24', 'Market demand is P = 1000 − 2Q and private supply P = 200 + 2Q. If external cost is ₹80 per unit, the socially optimal output is:', ['180 units', '200 units', '220 units', '160 units'], 0, 'Social marginal cost = private supply + external cost = 200 + 2Q + 80 = 280 + 2Q. Set demand equal: 1000 − 2Q = 280 + 2Q, so 4Q = 720 and Q = 180 units. The tempting 200 units is the market output that ignores the externality (800 ÷ 4); 220 units wrongly subtracts the ₹80. In practice: environmental economists use this logic to size pollution taxes for industries.', 'c7', 'hard', '(1000-200-80)/(2+2)', topic='Government Intervention to Correct Externalities'),
            M('m25', 'Which of the following is NOT necessarily a demerit good even though it causes a negative externality?', ['Steel', 'Cigarettes', 'Alcohol', 'Narcotic drugs'], 0, 'Steel production pollutes, but steel itself is socially useful, so it is not a demerit good; demerit goods are those whose consumption is harmful to the user and society, such as cigarettes, alcohol and narcotics. Alcohol is a tempting distractor if you think of it as merely a legal product, but it is a classic demerit good. In practice: steel faces pollution norms, while cigarettes face heavy taxes and advertising bans.', 'c8', 'moderate', topic='Government Intervention in the Case of Demerit Goods'),
            M('m26', 'Making education free and compulsory for children aged 6 to 14 is an intervention for a:', ['Merit good', 'Demerit good', 'Pure public good', 'Private good with no externality'], 0, "Education creates large positive externalities and people may under-consume it, so it is a merit good; the RTE Act, 2009 (Right of Children to Free and Compulsory Education) makes it free and compulsory for ages 6 to 14. 'Pure public good' is the trap — schooling is rival and excludable, so it is not a pure public good. In practice: private schools must reserve 25% of entry-level seats for disadvantaged children under the RTE Act.", 'c8', topic='Government Intervention in the Case of Merit Goods'),
            M('m27', 'Heavy taxes on cigarettes may not cut consumption much because:', ['Demand for cigarettes is price-inelastic', 'Cigarettes are public goods', 'Supply is perfectly elastic', 'Cigarettes have positive externalities'], 0, "Smokers are often addicted, so demand for cigarettes is price-inelastic: a large price rise reduces quantity only a little. 'Supply is perfectly elastic' is the trap — supply elasticity does not explain why consumers keep buying. In practice: India levies GST at the top rate plus cess on cigarettes; it raises big revenue, but health experts say taxes must be combined with awareness campaigns to cut smoking.", 'c8', topic='Government Intervention in the Case of Demerit Goods'),
            M('m28', 'For a good, Qd = 5,000 − 20P and Qs = 1,000 + 20P. If a price ceiling of ₹80 is imposed, the shortage is:', ['800 units', '400 units', '3,400 units', '2,600 units'], 0, 'At the ceiling of ₹80: Qd = 5,000 − 20 × 80 = 3,400 and Qs = 1,000 + 20 × 80 = 2,600, so the shortage = 3,400 − 2,600 = 800 units. The tempting 3,400 and 2,600 are the separate quantities, not the gap; 400 compares demand with the equilibrium quantity of 3,000. In practice: when the government caps rents or essential-drug prices below equilibrium, queues and shortages follow.', 'c9', 'hard', '(5000-20*80)-(1000+20*80)', topic='Price Intervention: Non-market Pricing'),
            M('m29', 'Minimum Support Price for crops is an example of a:', ['Price floor', 'Price ceiling', 'Pigouvian tax', 'Cap-and-trade scheme'], 0, "Minimum Support Price is a guaranteed minimum price for crops, set above the market price when it binds — a price floor protecting farmers' incomes. 'Price ceiling' is the trap: a ceiling is a maximum price meant to protect consumers, such as on essential medicines. In practice: the government announces MSPs for kharif and rabi crops, and FCI procurement at MSP leads to large grain stocks.", 'c9', topic='Price Intervention: Non-market Pricing'),
            M('m30', 'Mandatory nutrition labels on packaged food mainly correct:', ['Information failure', 'Market power', 'A public good problem', 'Moral hazard of insurers'], 0, "Consumers cannot easily judge the fat, sugar or calorie content of packaged food, so mandatory labels correct information failure by giving them the facts they lack. Moral hazard is the trap — it concerns changed behaviour after a contract, not missing product information. In practice: FSSAI's labelling regulations require packaged-food companies in India to show nutritional information, and auditors of FMCG firms check compliance.", 'c10', topic='Government Intervention for Correcting Information Failure'),
            M('m31', 'Government failure occurs when:', ['Intervention creates inefficiency or new problems', 'The government runs a budget surplus', 'Markets are perfectly competitive', 'Taxes are progressive'], 0, "Government failure occurs when an intervention meant to fix a market failure creates new inefficiency — through poor information, high costs, corruption or political motives. 'Runs a budget surplus' is the trap: a surplus is a fiscal outcome, not evidence of failed intervention. In practice: leakages in subsidy schemes, which Direct Benefit Transfer has tried to plug, are an Indian example of government failure.", 'c10', topic='Government Intervention for Equitable Distribution'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'text',
             'q': 'Demand for cement in a region is P = 900 − 3Q and private marginal cost is P = 100 + Q. Dust from kilns causes external damage of ₹40 per unit. Find (a) market output and price, (b) socially optimal output and price, (c) the over-production, and (d) the Pigouvian tax and its revenue at the optimum.',
             'model': [p(f'(a) 900 − 3Q = 100 + Q → 4Q = 800 → Q = {q1m}; P = 900 − 3×{q1m} = ₹{q1p}.'),
                       p(f'(b) SMC = 100 + Q + 40 = 140 + Q. 900 − 3Q = 140 + Q → 4Q = 760 → Q = {q1s}; P = 900 − 3×{q1s} = ₹{q1ps}.'),
                       p(f'(c) Over-production = {q1m} − {q1s} = {q1o} units.'),
                       p(f'(d) Pigouvian tax = marginal external cost = ₹40 per unit; revenue = 40 × {q1s} = ₹{inr(q1t)}.')],
             'scheme': [{'id': 's1', 'pt': 'Market equilibrium solved', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Social marginal cost formed correctly (add external cost)', 'm': 1.5, 'skill': 'concept'},
                        {'id': 's3', 'pt': 'Social optimum solved', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Over-production identified', 'm': 1, 'skill': 'analysis'},
                        {'id': 's5', 'pt': 'Tax rate and revenue', 'm': 1, 'skill': 'application'}],
             'remarks': ['Strong answers wrote SMC = PMC + MEC before solving.'], 'mistakes': ['Subtracting the external cost from supply.', 'Computing tax revenue at market output instead of optimum output.'],
             'tips': ['State each equation before solving; show the price by substituting back into demand.'], 'checks': q1},
            {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'For wheat, Qd = 12,000 − 50P and Qs = 2,000 + 50P. (a) Find the equilibrium. (b) What happens if a maximum price of ₹85 is fixed? (c) What happens if instead a support price of ₹110 is fixed, and what does it cost the government to buy the surplus?',
             'model': [p(f'(a) 12,000 − 50P = 2,000 + 50P → P = ₹{q2pe}; Q = {inr(q2qe)}.'),
                       table(['Case', 'P', 'Qd', 'Qs', 'Gap'], [['Ceiling', 85, q2d, q2s, f'Shortage {inr(q2sh)}'], ['Floor', 110, q2fd, q2fs, f'Surplus {inr(q2su)}']]),
                       p(f'(c) Government buys {inr(q2su)} units at ₹110 = ₹{inr(q2c)}.')],
             'scheme': [{'id': 's1', 'pt': 'Equilibrium', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'Ceiling quantities and shortage', 'm': 2, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Floor quantities and surplus', 'm': 2, 'skill': 'computation'}, {'id': 's4', 'pt': 'Procurement cost', 'm': 1, 'skill': 'application'}],
             'remarks': ['Many candidates reversed shortage and surplus.'], 'mistakes': ['Saying a ceiling causes a surplus.', 'Valuing procurement at the equilibrium price.'],
             'tips': ['Remember: ceiling → shortage; floor → surplus.'], 'checks': q2},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'hard', 'pad': 'table',
             'q': 'Firms X and Y each emit 100 tonnes; total emissions must fall by 80 tonnes. X can abate at ₹300 a tonne and Y at ₹900 a tonne. Each receives 60 permits. Compare total abatement cost if (a) each firm cuts 40 tonnes itself, (b) X cuts 80 tonnes and sells 40 permits to Y at ₹600 each. Show each firm\'s position.',
             'model': [table(['', 'No trade ₹', 'Trade ₹'], [['X abatement', q3a, q3x], ['Y abatement', q3b, 0], ['Society\'s abatement cost', q3n, q3x]], num=[1, 2]),
                       p(f'X: abatement {inr(q3x)} less permit receipts {inr(q3r)} = net ₹{inr(q3nx)} (vs ₹{inr(q3a)}). Y: pays ₹{inr(q3r)} for permits (vs ₹{inr(q3b)}). Society saves ₹{inr(q3s)} with the same 80-tonne cut.')],
             'scheme': [{'id': 's1', 'pt': 'No-trade costs', 'm': 1.5, 'skill': 'computation'}, {'id': 's2', 'pt': 'Trade costs and permit receipts', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Each firm better off — shown', 'm': 1, 'skill': 'analysis'}, {'id': 's4', 'pt': 'Conclusion: same cut at least cost', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Permit payments are transfers between firms, not a cost to society — the best answers said so.'], 'mistakes': ['Adding permit payments to society\'s cost.'],
             'tips': ['Separate society\'s resource cost (abatement) from transfers (permit sales).'], 'checks': q3},
        ],
        'revision': {
            'summary': ['Market failure = inefficient allocation; complete (missing market) or partial (wrong quantity/price).',
                        'Four sources: market power, externalities, public goods, incomplete information.',
                        'Externality grid: negative/positive × production/consumption, received by producers or consumers. Social cost = private + external cost.',
                        'Public goods: non-rival, non-excludable, indivisible, zero marginal cost → free riding → under-provision (Samuelson 1954).',
                        'Asymmetric information: adverse selection (before, hidden information; lemons — Akerlof) and moral hazard (after, hidden action).',
                        'Remedies: Competition Act 2002; direct controls; Pigouvian tax (price fixed); cap-and-trade (quantity fixed); subsidies; merit/demerit good policies; price ceilings (shortage) and floors (surplus); buffer stocks; disclosure; redistribution.',
                        'Government failure: intervention that wastes resources or creates new problems.'],
            'remember': ['India: PAT, coal cess → GST compensation cess (2017), RPO/REC, carbon credit trading under the Energy Conservation (Amendment) Bill 2022.', 'RTE Act 2009: ages 6–14.', 'Not every negative-externality good is a demerit good (steel).'],
            'traps': ['A price change through the market is not an externality.', 'Positive externality = under-production (still a failure).', 'Ceiling below equilibrium → shortage; floor above → surplus.', 'Permit payments are transfers, not social cost.'],
        },
        'quickref': [
            {'k': 'Social cost', 'v': 'Private cost + external cost (social benefit = private + external benefit)'},
            {'k': 'Optimum with externality', 'v': 'Set demand = PMC + MEC; Pigouvian tax per unit = MEC'},
            {'k': 'Public good', 'v': 'Non-rival + non-excludable (+ indivisible, zero MC) → free rider'},
            {'k': 'Adverse selection vs moral hazard', 'v': 'Before deal / hidden information vs after deal / hidden action'},
            {'k': 'Price controls', 'v': 'Ceiling (max) below equilibrium → shortage; floor (min, MSP) above → surplus'},
            {'k': 'Tax vs cap-and-trade', 'v': 'Tax fixes the price of pollution; cap fixes its quantity'},
        ],
        'viva': [
            V('v1', 'What is market failure, and what are its two types?',
              'Market failure is when a free market allocates resources inefficiently, producing too much or too little of some goods. Complete market failure means the market does not supply the good at all, a missing market, as with pure public goods. Partial market failure means the market works but gives the wrong quantity or the wrong price.',
              [P('p1', 'Inefficient allocation — over/under production', 4, 'inefficien|misallocat|too much|too little|over produc|under produc|overproduc|underproduc|wrong quantit|not optimal|suboptimal', min=1),
               P('p2', 'Complete failure — missing market, nothing supplied', 3, 'complete|missing|total', 'not suppl|nothing|no supply|at all|missing|public good', min=2),
               P('p3', 'Partial failure — wrong quantity or price', 3, 'partial', 'wrong|quantit|price', min=2)], 'c1'),
            V('v2', 'What are the characteristics of a public good? Why will the market not supply it?',
              'A public good is non-rival, so one person\'s use does not reduce anyone else\'s, and non-excludable, so non-payers cannot be kept out. It is indivisible and the extra cost of one more user is zero. Because people can enjoy it without paying, they free ride, so private firms cannot charge a price and will not produce it.',
              [P('p1', 'Non-rival', 3, 'non rival|nonrival|not rival|no rivalry|does not reduce|doesn t reduce|without reduc', min=1),
               P('p2', 'Non-excludable', 3, 'non exclud|nonexclud|not exclud|cannot exclud|cannot be exclud|can t exclud|cannot be kept out|cannot keep out|cannot stop', min=1),
               P('p3', 'Free-rider problem — no one pays, so firms do not produce', 4, 'free rid|free ride|free rider|free riding|freerid|without pay|not pay|no one pay|nobody pay|no incentive to pay', min=1)], 'c4'),
            V('v3', 'Distinguish between adverse selection and moral hazard.',
              'Adverse selection happens before the transaction because of hidden information, for example only high-risk people buying health insurance or lemons in the used car market. Moral hazard happens after the transaction because of hidden action, for example an insured driver driving carelessly because the insurer bears the loss.',
              [P('p1', 'Adverse selection: before the deal / hidden information', 5, ALT('adverse selection {b}', 'adverse selection happen {b}', 'adverse selection occur {b}', 'adverse selection aris {b}', 'adverse selection is {b}', b=('before', 'prior', 'hidden information', 'pre contract', 'precontract', 'ex ante'))),
               P('p2', 'Moral hazard: after the deal / hidden action', 5, ALT('moral hazard {a}', 'moral hazard happen {a}', 'moral hazard occur {a}', 'moral hazard aris {a}', 'moral hazard is {a}', a=('after', 'later', 'hidden action', 'post contract', 'postcontract', 'ex post', 'once')))], 'c5'),
            V('v4', 'Compare a Pigouvian tax with a cap-and-trade system for controlling pollution.',
              'A Pigouvian tax charges the polluter per unit of pollution, so it fixes the price of pollution and makes the polluter pay; the quantity of pollution then adjusts. Cap-and-trade fixes the total quantity of pollution through a limited number of permits, and firms trade permits so the price adjusts; the cut is achieved at the least cost because cheap abaters sell permits.',
              [P('p1', 'Pigouvian tax fixes the price / polluter pays per unit', 4, ALT('{t} {f} price', '{t} set price', '{t} polluter pay', '{t} per unit', '{t} charg', t=('pigouvian tax', 'pigou tax', 'pollution tax', 'tax'), f=('fix', 'fixes', 'sets', 'set'))),
               P('p2', 'Cap-and-trade fixes the quantity (cap) via permits', 4, ALT('cap {f} quantit', 'cap {f} total', 'cap {f} amount', 'cap and trade {f} quantit', 'cap and trade {f} total', 'limit total', 'fix total quantit', 'fixed number of permit', 'limited number of permit', f=('fix', 'fixes', 'sets', 'set', 'limit', 'limits'))),
               P('p3', 'Permits are traded; least-cost reduction', 2, 'trade|sell|buy|least cost|cheapest|cost effective|lowest cost', min=1)], 'c7'),
            V('v5', 'How does the government deal with merit goods and with demerit goods? Give examples.',
              'Merit goods like education and health care are under-consumed, so the government subsidises them, provides them directly or free, and may make them compulsory, like free and compulsory schooling for children aged six to fourteen. Demerit goods like cigarettes and alcohol are over-consumed, so the government taxes them heavily, bans or restricts them, and bans their advertising.',
              [P('p1', 'Merit goods (education/health) encouraged — subsidy, free provision, compulsion', 5, ALT('merit good {e}', 'merit {e}', '{e} merit', '{e} are merit', e=('education', 'health', 'school', 'hospital', 'vaccin', 'immunis', 'immuniz', 'library', 'park')), 'subsid|free|compulsor|provid|encourag|mandator'),
               P('p2', 'Demerit goods (cigarettes/alcohol) discouraged — high tax, ban, advertising curbs', 5, ALT('demerit good {d}', 'demerit {d}', '{d} demerit', '{d} are demerit', d=('cigarette', 'tobacco', 'alcohol', 'liquor', 'drug', 'smok')), 'tax|ban|restrict|prohibit|discourag|advertis')], 'c8'),
            V('v6', 'What is the effect of a price ceiling and of a price floor? Give one example of each.',
              'A price ceiling is a maximum price set below the equilibrium, for example rent control or capped food prices, and it causes a shortage because demand exceeds supply. A price floor is a minimum price set above the equilibrium, for example minimum support price or minimum wage, and it causes a surplus because supply exceeds demand.',
              [P('p1', 'Ceiling (maximum price) → shortage', 4, ALT('ceiling {x}', 'maximum price {x}', 'max price {x}', x=('shortage', 'below equilibrium shortage', 'cause shortage', 'creat shortage', 'lead shortage', 'result shortage', 'set below', 'below', 'excess demand'))),
               P('p2', 'Floor (minimum price) → surplus', 4, ALT('floor {x}', 'minimum price {x}', 'min price {x}', x=('surplus', 'above equilibrium surplus', 'cause surplus', 'creat surplus', 'lead surplus', 'result surplus', 'set above', 'above', 'excess supply'))),
               P('p3', 'Examples — rent control / MSP or minimum wage', 2, 'rent|food price|ration|cap', 'support price|msp|minimum wage|wage', min=1)], 'c9'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'The tannery cluster on the river', 'difficulty': 'hard',
            'case': ('A cluster of tanneries faces demand P = 600 − Q and private marginal cost P = 100 + Q (Q in thousand hides). Effluent harms farmers downstream by ₹50 per thousand hides. '
                     'The state considers (i) a pollution tax, (ii) issuing a fixed number of tradable effluent permits, or (iii) simply ordering every tannery to install treatment plants.'),
            'mcqs': [
                M('k1a', 'What output will the unregulated market produce?', ['250 thousand hides', '225 thousand hides', '275 thousand hides', '300 thousand hides'], 0, 'The unregulated market ignores the effluent damage, so output is where demand equals private marginal cost: 600 − Q = 100 + Q, so 2Q = 500 and Q = 250 thousand hides. The tempting 225 thousand is the social optimum, which includes the external cost. In practice: without pollution controls, a tannery cluster such as those near the Ganga produces at this higher private-optimum level and passes damage downstream.', 'c3', 'moderate', '(600-100)/(1+1)', topic='Why Do Markets Fail?'),
                M('k1b', 'What is the socially optimal output?', ['225 thousand hides', '250 thousand hides', '275 thousand hides', '200 thousand hides'], 0, 'Add the ₹50 external cost to private cost: social marginal cost = 150 + Q. Then 600 − Q = 150 + Q, so 2Q = 450 and Q = 225 thousand hides. The tempting 275 thousand subtracts the external cost (50 + Q); 250 thousand is the market output ignoring damage. In practice: pollution-control boards aim to bring output or effluent down to this socially efficient level through taxes, permits or norms.', 'c7', 'hard', '(600-100-50)/(1+1)', topic='Government Intervention to Correct Externalities'),
                M('k1c', 'Option (iii), ordering treatment plants, is an example of:', ['Direct control (command-and-control)', 'A market-based instrument', 'A price floor', 'Redistribution'], 0, "Ordering every tannery to install treatment plants mandates a specific action rather than working through prices, so it is direct control (command-and-control). 'A market-based instrument' is the trap: taxes and tradable permits are market-based because they change incentives and leave firms to choose. In practice: State pollution-control boards in India often require effluent treatment plants as a condition of the consent to operate.", 'c7', 'core', topic='Government Intervention to Correct Externalities'),
                M('k1d', 'Which statement about options (i) and (ii) is correct?', ['The tax fixes the price of pollution; permits fix its quantity', 'The tax fixes the quantity; permits fix the price', 'Both fix the quantity of pollution', 'Neither uses the price mechanism'], 0, 'A pollution tax fixes the price of each unit of pollution and lets firms decide how much to emit; tradable permits fix the total quantity of pollution and let the market set the permit price. The swapped version is the trap. In practice: regulators choose a tax when they want cost certainty for firms and a cap with permits when they want certainty about the environmental outcome.', 'c7', 'moderate', topic='Government Intervention to Correct Externalities'),
            ]}],
    }
