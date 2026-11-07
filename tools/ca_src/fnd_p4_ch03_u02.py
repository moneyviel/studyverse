"""CA Foundation · Paper 4 Business Economics · Chapter 3 · Unit 2 Theory of Cost.
Original explanations, examples and questions (ICAI structure and scope only). Every figure is computed below."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch03-u02'


def Q(mid, q, opts, ans, ex, c, d='core', check=None):
    x = {'id': mid, 'q': q, 'options': opts, 'answer': ans, 'explain': ex, 'concept': c, 'difficulty': d}
    if check: x['check'] = check
    return x


def build():
    # ---------- i1 accounting vs economic cost ----------
    c1 = Checks()
    rev = 2500000; expl = 1700000
    acc = c1.add('2500000-1700000', 'accounting profit')
    imp = c1.add('480000+0.09*2000000+60000', 'implicit costs: own salary + interest on own capital + rent of own premises')
    eco = c1.add('800000-720000', 'economic profit')

    # ---------- i2 short-run cost schedule ----------
    c2 = Checks()
    TFC = 600
    Qs = list(range(0, 9))
    TVC = [0, 100, 180, 240, 320, 420, 540, 700, 900]
    TC = [c2.add(f'{TFC}+{v}', f'TC at Q = {q}') for q, v in zip(Qs, TVC)]
    AFC = ['—'] + [c2.add(f'round({TFC}/{q},2)', f'AFC at Q = {q}') for q in Qs[1:]]
    AVC = ['—'] + [c2.add(f'round({TVC[q]}/{q},2)', f'AVC at Q = {q}') for q in Qs[1:]]
    ATC = ['—'] + [c2.add(f'round({TC[q]}/{q},2)', f'ATC at Q = {q}') for q in Qs[1:]]
    MC = ['—'] + [c2.add(f'{TC[q]}-{TC[q-1]}', f'MC of unit {q}') for q in Qs[1:]]
    rows2 = [[q, TFC, TVC[q], TC[q], AFC[q], AVC[q], ATC[q], MC[q]] for q in Qs]
    avc_min_q = min(Qs[1:], key=lambda q: AVC[q]); atc_min_q = min(Qs[1:], key=lambda q: ATC[q])

    # ---------- i3 cost function ----------
    c3 = Checks()
    # TC = 500 + 20Q + 2Q^2
    tc10 = c3.add('500+20*10+2*10*10', 'TC at Q = 10'); tc11 = c3.add('500+20*11+2*11*11', 'TC at Q = 11')
    mc11 = c3.add(f'{tc11}-{tc10}', 'MC of 11th unit'); afc10 = c3.add('500/10', 'AFC at Q = 10')
    avc10 = c3.add('(20*10+2*10*10)/10', 'AVC at Q = 10'); atc10 = c3.add(f'{tc10}/10', 'ATC at Q = 10')
    qmin = c3.add('(500/2)**0.5', 'output where ATC is minimum: 500/Q = 2Q → Q = √250')
    qmin_r = round(qmin, 2)

    # ---------- i4 choosing the plant (LAC) ----------
    c4 = Checks()
    plants = {'Small (SAC1)': (200000, 60), 'Medium (SAC2)': (500000, 40), 'Large (SAC3)': (1000000, 30)}
    outs = [10000, 20000, 40000, 60000]
    plant_rows = []
    for qo in outs:
        acs = {n: c4.add(f'round(({f}+{v}*{qo})/{qo},2)', f'{n} AC at {qo}') for n, (f, v) in plants.items()}
        best = min(acs, key=acs.get)
        plant_rows.append([inr(qo)] + list(acs.values()) + [best])

    # ---------- questions ----------
    cq1 = Checks()
    q1_tvc = [0, 40, 70, 96, 130, 175, 234, 320, 430]
    q1_tc = [cq1.add(f'300+{v}', f'q1 TC {q}') for q, v in enumerate(q1_tvc)]
    q1_mc = [cq1.add(f'{q1_tc[q]}-{q1_tc[q-1]}', f'q1 MC {q}') for q in range(1, 9)]
    q1_atc = [cq1.add(f'round({q1_tc[q]}/{q},2)', f'q1 ATC {q}') for q in range(1, 9)]
    q1_avc = [cq1.add(f'round({q1_tvc[q]}/{q},2)', f'q1 AVC {q}') for q in range(1, 9)]
    cq2 = Checks()
    q2_acc = cq2.add('1800000-1150000', 'q2 accounting profit'); q2_imp = cq2.add('600000+0.08*1500000', 'q2 implicit cost')
    q2_eco = cq2.add('650000-720000', 'q2 economic profit')
    cq3 = Checks()
    q3_tc = cq3.add('1000+50*20+0.5*20*20', 'q3 TC at 20'); q3_tc21 = cq3.add('1000+50*21+0.5*21*21', 'q3 TC at 21')
    q3_mc = cq3.add(f'{q3_tc21}-{q3_tc}', 'q3 MC of 21st unit'); q3_atc = cq3.add(f'{q3_tc}/20', 'q3 ATC at 20'); q3_afc = cq3.add('1000/20', 'q3 AFC at 20')
    q3_q = cq3.add('(1000/0.5)**0.5', 'q3 Q at min ATC'); q3_qr = round(q3_q, 2)

    # ---------- case ----------
    k = Checks()
    k_afc = k.add('120000/400', 'case AFC at 400'); k_avc = k.add('80000/400', 'case AVC at 400')
    k_atc = k.add('(120000+80000)/400', 'case ATC at 400'); k_mc = k.add('(120000+84500)-(120000+80000)', 'case extra total cost of 10 more units')
    k_mc_u = k.add('4500/10', 'case MC per unit for 10 extra units')

    concepts = [
        {'id': 'c1', 'title': 'Accounting cost, economic cost and profit',
         'body': ['Accounting (explicit) costs are actual payments to outside suppliers of factors — wages, materials, fuel, rent paid, interest on borrowed money. They are recorded in the books.',
                  'Economic cost = explicit costs + implicit costs. Implicit costs are the value of the entrepreneur\'s own factors used in the business: normal return (interest) on own capital, the salary he could have earned elsewhere, rent of his own premises. They are not paid in cash and not recorded.',
                  'Accounting profit = revenue − explicit costs. Economic profit = revenue − (explicit + implicit costs), so it is normally lower. Normal profit is part of implicit cost — the minimum needed to keep the entrepreneur in the business; when revenue just covers explicit and implicit costs, economic profit is zero. Supernormal (abnormal, positive economic) profit arises only when revenue exceeds both.'],
         'analogy': 'Accounting cost is the bill you pay; economic cost is the bill plus what you gave up to be there.',
         'work': 'A CA advising a family business on whether to continue a loss-making unit must include implicit costs — the owner\'s time and capital have alternative uses.'},
        {'id': 'c2', 'title': 'Other cost concepts',
         'body': ['Outlay cost vs opportunity cost: outlay costs involve actual spending (recorded in books); opportunity cost is the value of the next best alternative given up, usually not recorded. Example: when a textile company uses yarn made in its own spinning unit for weaving, the yarn should be valued at the market price it could have fetched if sold outside; the cost of higher education includes the earnings given up.',
                  'Direct (traceable) vs indirect (non-traceable) costs: direct costs can be readily identified with a product, process or department; indirect costs (power, common administration) cannot be traced easily but are allocated. Whether a cost is direct depends on the purpose — an overhead can be direct to a department.',
                  'Incremental vs sunk costs: incremental cost is the additional cost caused by a decision (new product line, new machine); sunk costs are already incurred and cannot be recovered (past advertising, R&D, specialised equipment, railway lines). Sunk costs are irrelevant for future decisions and act as a barrier to entry.',
                  'Historical vs replacement costs: historical cost is what an asset cost when bought; replacement cost is what it would cost to replace it now. With rising prices, replacement cost exceeds historical cost.',
                  'Private vs social costs: private costs are borne by the firm (explicit or implicit); social cost = private cost + external cost borne by society (pollution, congestion, use of rivers and air without paying).',
                  'Fixed vs variable costs: fixed costs do not vary with output within capacity (rent, property tax, interest on loans, time-based depreciation, managers\' salaries); they are inescapable while the business runs and vary only with plant size. Shut-down costs continue even when operations stop (storing idle machines); programmed or discretionary fixed costs depend on management\'s choice (advertising). Variable costs vary with output (materials, casual wages, power).'],
         'analogy': 'Sunk cost is spilt milk — crying over it (or counting it in a decision) does not bring it back.',
         'work': 'These distinctions run through cost accounting, decision-making and Ind AS: incremental costs for make-or-buy, opportunity cost for transfer pricing, replacement cost for inflation analysis, social cost in ESG reporting.'},
        {'id': 'c3', 'title': 'Cost function; short run and long run',
         'body': ['A cost function is the mathematical relation between cost and its determinants. Cost (total or unit) is the dependent variable; output, factor prices, technology, capacity utilisation, efficiency and the time period are the independent variables. It is derived from the production function and the supply of inputs, and is shown by cost curves. There are short-run and long-run cost functions.',
                  'Fixed factors (building, machinery, top management) cannot be varied quickly; variable factors (labour, raw material) can. The short run is the period in which only variable factors can be changed; the long run is the period in which all factors can be changed. Hence fixed costs exist only in the short run; in the long run all costs are variable.'],
         'analogy': 'In the short run you rent more chairs for a party; in the long run you can move to a bigger hall.',
         'work': 'Budgets split costs into fixed and variable so that flexible budgets can be prepared for different activity levels — a short-run cost function in practice.'},
        {'id': 'c4', 'title': 'Short-run total costs: TFC, TVC, TC (and semi-variable, stair-step)',
         'body': ['Total fixed cost (TFC) stays the same at every output, even at zero output — a horizontal line starting on the Y-axis. Total variable cost (TVC) is zero at zero output and rises with output — first at a decreasing rate (increasing returns to the variable factor) and then at an increasing rate (diminishing returns). TC = TFC + TVC; the TC curve has the same shape and slope as TVC, shifted up by TFC; the vertical gap between them is TFC everywhere.',
                  'Semi-variable costs have a fixed part and a variable part (electricity: fixed charge + charge per unit). Stair-step costs stay fixed over a range of output and then jump to a higher level (a new supervisor once output crosses a limit).'],
         'analogy': 'TFC is the monthly rent of a shop; TVC is the stock you buy as sales grow; TC is the total of both.',
         'work': 'Break-even and CVP analysis — a staple of CA exams and practice — rests on this split between fixed and variable cost.'},
        {'id': 'c5', 'title': 'Short-run average and marginal costs',
         'body': ['AFC = TFC ÷ Q; it falls continuously as output rises (the same fixed cost is spread over more units) — a rectangular hyperbola that approaches but never touches the X-axis.',
                  'AVC = TVC ÷ Q; it falls at first (increasing returns to the variable factor), reaches a minimum at normal capacity, then rises (diminishing returns) — U-shaped.',
                  'ATC = TC ÷ Q = AFC + AVC. It falls sharply at first (both AFC and AVC fall); keeps falling for a while even after AVC starts rising because the fall in AFC outweighs the rise in AVC; then rises when AVC rises faster than AFC falls — U-shaped. The minimum of ATC lies to the right of the minimum of AVC.',
                  'MC = ΔTC ÷ ΔQ, or MCn = TCn − TCn−1. MC is independent of fixed cost (MC = ΔTVC/ΔQ). It falls, reaches a minimum at the point of inflexion of the TC curve, and then rises — U-shaped, mirroring the marginal product (MP up → MC down; MP down → MC up).',
                  'AC–MC relationship: when AC falls, MC < AC; when AC rises, MC > AC; when AC is minimum, MC = AC — the MC curve cuts the AC curve (and the AVC curve) at its minimum point. The output at minimum ATC is the optimum output.'],
         'blocks': [table(['Cost', 'Formula', 'Shape'], [['AFC', 'TFC ÷ Q', 'Falls throughout (rectangular hyperbola)'], ['AVC', 'TVC ÷ Q', 'U-shaped'], ['ATC', 'TC ÷ Q = AFC + AVC', 'U-shaped; minimum to the right of AVC minimum'], ['MC', 'TCn − TCn−1 = ΔTVC ÷ ΔQ', 'U-shaped; cuts AVC and ATC at their minima']], title='Short-run unit costs')],
         'analogy': 'Your average marks rise when a new test score (marginal) is above your average and fall when it is below — the same rule links MC and AC.',
         'work': 'Pricing special orders on marginal cost, and knowing that average cost per unit falls with volume (spreading fixed cost), are everyday CA tools.'},
        {'id': 'c6', 'title': 'Long-run average cost curve',
         'body': ['In the long run all inputs are variable, so the firm can choose any plant size. Long-run cost is the least possible cost of producing each output when all factors can be varied. The firm operates in the short run (on a given plant) but plans for the long run.',
                  'Each plant has its own short-run average cost curve (SAC, a "plant curve"). For each output the firm picks the plant with the lowest SAC: small outputs are cheapest with small plants, large outputs with large plants. With infinitely many plant sizes, the LAC curve is a smooth curve that touches (is tangent to) every SAC from below — the envelope curve.',
                  'The LAC is not tangent to the minimum points of the SACs (except one). On its falling part it touches the falling parts of SACs (plants operated below their optimum capacity); on its rising part it touches the rising parts (plants operated beyond optimum capacity). Only at the minimum point of LAC is the corresponding SAC also at its minimum — the optimum output with the optimum plant.',
                  'The LAC is called the planning curve because it helps the firm choose the plant size for an expected output. Its U-shape is due not to variable proportions but to returns to scale: increasing returns (economies of scale) make LAC fall, a range of constant returns keeps it flat, and decreasing returns (diseconomies) make it rise. Traditional theory draws a flattened U; empirical studies show many modern firms face an L-shaped LAC — costs fall quickly with scale and then stay low over a wide range because technology keeps improving.'],
         'analogy': 'SACs are shoes of different sizes; the LAC is a smooth line through the most comfortable fit for every foot size.',
         'work': 'Capacity decisions in project appraisal (what size plant to build for forecast demand) use the planning-curve idea; over-building leaves the plant on the falling part of its SAC for years.'},
        {'id': 'c7', 'title': 'Internal economies and diseconomies of scale',
         'body': ['Internal economies are cost savings that accrue to a firm from its own expansion, due to its own efficiency, management or technology; they are available only to that firm. Beyond an optimum scale they turn into internal diseconomies.',
                  '(1) Technical — more efficient and specialised machinery, composite (integrated) technology, greater division of labour, and linked processes from input to final output. Diseconomies: beyond a point, plant size outruns management\'s ability to coordinate. (2) Managerial — specialist departments (production, sales, finance) and further sub-division, decentralisation and mechanised management functions. Diseconomies: communication gaps, delays, bureaucracy, red tape, loss of control. (3) Commercial — bulk buying at lower prices, fuller use of sales staff, lower advertising cost per unit, profitable use of by-products, transport and storage savings. Diseconomies: marketing overheads rise more than proportionately past the optimum. (4) Financial — better security and goodwill, easier and cheaper loans, readily marketable shares. Diseconomies: more dependence on external finance raises its cost. (5) Risk-bearing — diversification across products and markets helps withstand ups and downs. Diseconomies: risk rises if diversification adds to disturbances instead of covering them.'],
         'analogy': 'A big family cooking together saves per head on gas and groceries — until the kitchen gets so crowded that nothing gets done on time.',
         'work': 'Due diligence on mergers tests claimed "synergies" — which are mostly internal economies of scale (bulk buying, shared overheads, cheaper finance).'},
        {'id': 'c8', 'title': 'External economies and diseconomies of scale',
         'body': ['External economies accrue to all firms in an industry when the industry as a whole expands; they do not depend on the size of any single firm. Examples: cheaper raw materials and capital equipment (new sources, competitive supply industries); technological external economies (new knowledge and better processes spreading through the industry); a pool of trained, skilled labour; growth of ancillary and supporting industries (repair shops, component suppliers); better transport, banking and marketing facilities; shared information services (trade journals, research institutes).',
                  'External diseconomies arise when industry expansion raises costs for all firms: rising prices of scarce inputs and wages, congestion, pressure on transport and power, pollution and the cost of controlling it.',
                  'Internal economies move a firm down its LAC curve; external economies shift the whole LAC curve of every firm downward (external diseconomies shift it upward).'],
         'analogy': 'When many IT firms cluster in one city, each gains from the talent pool and suppliers (external economies) — but all suffer the traffic jams (external diseconomies).',
         'work': 'Location advice for clients (industrial clusters, SEZs) weighs these external economies and diseconomies.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Accounting vs economic profit', 'difficulty': 'core', 'minutes': 6,
         'q': f'Nikhil runs a printing press in his own building. Revenue {R(rev)}; explicit costs {R(expl)}. He could earn {R(480000)} a year as a manager, could let out his building for {R(60000)} a year, and has {R(2000000)} of his own capital in the business that could earn 9%. Compute accounting and economic profit.',
         'solution': [table(['Item', 'Amount (₹)'], [['Revenue', rev], ['Less: explicit costs', expl], ['Accounting profit', acc]], title='Accounting view'),
                      table(['Implicit cost', 'Amount (₹)'], [['Salary foregone', 480000], ['Interest foregone (9% of ₹20,00,000)', 180000], ['Rent foregone on own building', 60000], ['Total implicit cost', imp]], num=[1], total=True, title='Implicit costs'),
                      p(f'Economic profit = {R(acc)} − {R(imp)} = {R(eco)}. Positive, so Nikhil earns more than normal profit (supernormal profit of {R(eco)}).')],
         'checks': c1},
        {'id': 'i2', 'title': 'Complete short-run cost schedule', 'difficulty': 'moderate', 'minutes': 12,
         'q': f'TFC is ₹{TFC}. TVC at outputs 0 to 8 is given. Prepare the full cost schedule and comment on the AC–MC relationship.',
         'given': [table(['Q', 'TVC (₹)'], [[q, v] for q, v in zip(Qs, TVC)])],
         'solution': [table(['Q', 'TFC', 'TVC', 'TC', 'AFC', 'AVC', 'ATC', 'MC'], rows2, title='Short-run costs (₹)'),
                      p(f'AFC falls throughout. AVC is lowest ({AVC[avc_min_q]}) at Q = 3–4, and the MC of the 4th unit ({MC[4]}) equals it — MC cuts AVC at its minimum; ATC is lowest ({ATC[atc_min_q]}) at Q = {atc_min_q} — to the right of the AVC minimum. MC is lowest ({min(MC[1:])}) at Q = 3.'),
                      p(f'Check the rule: at Q = {atc_min_q}, MC = {MC[atc_min_q]} is still below ATC ({ATC[atc_min_q]}) and at the next unit MC = {MC[atc_min_q+1]} exceeds ATC — so MC cuts ATC near its minimum. While ATC falls, MC < ATC; once MC > ATC, ATC rises.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Working with a cost function', 'difficulty': 'hard', 'minutes': 8,
         'q': 'A firm\'s total cost function is TC = 500 + 20Q + 2Q². (a) Identify TFC and TVC. (b) At Q = 10 find TC, AFC, AVC, ATC. (c) Find the MC of the 11th unit. (d) At what output is ATC minimum?',
         'solution': [p('(a) TFC = ₹500 (does not depend on Q); TVC = 20Q + 2Q².'),
                      table(['Measure', 'Working', 'Value (₹)'], [['TC (Q = 10)', '500 + 200 + 200', tc10], ['AFC', '500 ÷ 10', afc10], ['AVC', '(200 + 200) ÷ 10', avc10], ['ATC', f'{tc10} ÷ 10', atc10], ['MC of 11th unit', f'TC(11) − TC(10) = {tc11} − {tc10}', mc11]], title='Costs'),
                      p(f'(d) ATC = 500/Q + 20 + 2Q. It is minimum where the falling AFC part and the rising part balance: 500/Q = 2Q → Q² = 250 → Q ≈ {qmin_r} units. (At this output MC = ATC.)')],
         'checks': c3},
        {'id': 'i4', 'title': 'Choosing the plant — deriving points on the LAC', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'A firm can build one of three plants. Small: fixed cost ₹2,00,000 a year, variable cost ₹60 a unit; Medium: ₹5,00,000 and ₹40; Large: ₹10,00,000 and ₹30. Which plant gives the lowest average cost at outputs of 10,000, 20,000, 40,000 and 60,000 units a year?',
         'solution': [table(['Output', 'Small AC (₹)', 'Medium AC (₹)', 'Large AC (₹)', 'Best plant'], plant_rows, title='Average cost = (fixed + variable × Q) ÷ Q'),
                      p('The lowest AC at each output is a point on the long-run average cost curve. Small outputs are cheapest with the small plant and large outputs with the large plant — the LAC is the "envelope" of the lowest parts of the plant curves, and helps the firm plan which plant to build.')],
         'checks': c4},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Accepting a special export order', 'role': 'CA in industry — cost controller',
         'situation': 'A buyer offers ₹210 a unit for 2,000 extra units. Full cost per unit is ₹250 (fixed ₹70 + variable ₹180). The plant has spare capacity.',
         'steps': ['Identify relevant cost: with spare capacity, fixed costs do not change, so the incremental (marginal) cost is ₹180 a unit.', 'Incremental revenue ₹210 > incremental cost ₹180 → extra contribution ₹30 × 2,000 = ₹60,000.', 'Ignore sunk and unchanged fixed costs; check that the order does not undercut regular prices.', 'Recommend acceptance.'],
         'takeaway': 'Decisions are taken on incremental (marginal) cost, not on average full cost.',
         'checks': [{'expr': '(210-180)*2000', 'value': 60000, 'label': 'extra contribution'}]},
        {'id': 'j2', 'title': 'Should we scrap the half-built project?', 'role': 'CA advising a board',
         'situation': '₹3 crore has already been spent on a project; ₹2 crore more is needed; expected value of the finished project is ₹2.5 crore.',
         'steps': ['Treat the ₹3 crore as sunk — it is gone whatever the decision.', 'Compare incremental cost (₹2 crore) with incremental benefit (₹2.5 crore).', 'Since benefit > cost, completing adds ₹0.5 crore of value; recommend completion despite the large past spend.'],
         'takeaway': 'Sunk costs must not drive future decisions; only incremental costs and benefits matter.',
         'checks': [{'expr': '2.5-2', 'value': 0.5, 'label': 'net incremental benefit (₹ crore)'}]},
        {'id': 'j3', 'title': 'Choosing plant capacity for a new unit', 'role': 'Articled assistant in project appraisal',
         'situation': 'Demand forecast is 40,000 units a year, possibly growing to 60,000.',
         'steps': ['Cost the plant options at both outputs (like Illustration 4).', 'Pick the plant on the LAC for the expected output; consider flexibility if growth is uncertain.', 'Note economies of scale (bulk buying, cheaper finance) and the risk of diseconomies if the plant is too large to manage.'],
         'takeaway': 'The LAC is a planning curve — it guides the size of plant to build.'},
    ]

    mcqs = [
        Q('m1', 'Accounting costs are also known as:', ['Explicit costs', 'Implicit costs', 'Opportunity costs', 'Social costs'], 0, 'Actual payments recorded in the books.', 'c1'),
        Q('m2', 'Economic cost includes:', ['Explicit costs plus implicit costs', 'Only explicit costs', 'Only implicit costs', 'Only sunk costs'], 0, 'It adds the value of own factors used.', 'c1'),
        Q('m3', 'Revenue ₹25 lakh, explicit costs ₹17 lakh, implicit costs ₹7.2 lakh. Economic profit is:', [R(80000), R(800000), R(720000), R(1520000)], 0, '25,00,000 − 17,00,000 − 7,20,000 = ₹80,000. ₹8,00,000 is accounting profit.', 'c1', 'core', '2500000-1700000-720000'),
        Q('m4', 'Normal profit is:', ['A part of implicit cost', 'Profit above all costs', 'Always equal to accounting profit', 'A sunk cost'], 0, 'It is the minimum return to keep the entrepreneur in business.', 'c1'),
        Q('m5', 'The cost of the next best alternative foregone is:', ['Opportunity cost', 'Outlay cost', 'Sunk cost', 'Historical cost'], 0, 'Definition.', 'c2'),
        Q('m6', 'Expenditure on R&D already incurred and not recoverable is a:', ['Sunk cost', 'Incremental cost', 'Replacement cost', 'Variable cost'], 0, 'Past, irreversible.', 'c2'),
        Q('m7', 'Sunk costs are relevant for future decisions.', ['False — they cannot be changed by any decision', 'True — they must always be recovered', 'True only for variable costs', 'True only in the long run'], 0, 'Only incremental costs matter.', 'c2', 'moderate'),
        Q('m8', 'In a period of rising prices:', ['Replacement cost exceeds historical cost', 'Historical cost exceeds replacement cost', 'Both are equal', 'Replacement cost is zero'], 0, 'Assets cost more to replace.', 'c2'),
        Q('m9', 'Social cost equals:', ['Private cost + external cost', 'Private cost − external cost', 'Explicit cost only', 'Implicit cost only'], 0, 'Includes costs borne by society.', 'c2'),
        Q('m10', 'Costs that continue even after operations are suspended, such as storing idle machines, are:', ['Shut-down costs', 'Variable costs', 'Incremental costs', 'Replacement costs'], 0, 'They remain after closure of operations.', 'c2', 'moderate'),
        Q('m11', 'Advertising expenses that depend on management\'s discretion are called:', ['Programmed (discretionary) fixed costs', 'Sunk costs', 'Variable costs', 'Social costs'], 0, 'Management decides whether to incur them.', 'c2', 'moderate'),
        Q('m12', 'In the long run:', ['All costs are variable', 'All costs are fixed', 'Fixed costs exceed variable costs', 'Only fixed costs exist'], 0, 'All factors can be varied.', 'c3'),
        Q('m13', 'The TFC curve is:', ['A horizontal line starting from the Y-axis', 'Upward sloping from the origin', 'U-shaped', 'A rectangular hyperbola'], 0, 'Fixed costs exist even at zero output.', 'c4'),
        Q('m14', 'The vertical distance between the TC and TVC curves equals:', ['TFC', 'MC', 'AVC', 'Zero'], 0, 'TC − TVC = TFC at every output.', 'c4'),
        Q('m15', 'Electricity charges with a fixed monthly charge plus a per-unit charge are an example of:', ['Semi-variable cost', 'Fixed cost', 'Stair-step cost', 'Sunk cost'], 0, 'Part fixed, part variable.', 'c4'),
        Q('m16', 'Supervisors\' salaries that jump when output crosses a limit are:', ['Stair-step costs', 'Semi-variable costs', 'Purely variable costs', 'Opportunity costs'], 0, 'Fixed over a range, then a jump.', 'c4'),
        Q('m17', 'TFC is ₹600. AFC at 8 units is:', ['75', '4800', '600', '8'], 0, '600 ÷ 8 = 75.', 'c5', 'core', '600/8'),
        Q('m18', 'TC at 4 and 5 units is ₹920 and ₹1,020. MC of the 5th unit is:', ['100', '204', '1020', '230'], 0, '1,020 − 920 = 100. 204 is ATC at 5 units.', 'c5', 'core', '1020-920'),
        Q('m19', 'The AFC curve:', ['Falls continuously but never touches the X-axis', 'Is U-shaped', 'Rises continuously', 'Is horizontal'], 0, 'Same fixed cost spread over more units.', 'c5'),
        Q('m20', 'Marginal cost is independent of:', ['Fixed cost', 'Variable cost', 'Output', 'Factor prices'], 0, 'MC = ΔTVC/ΔQ.', 'c5'),
        Q('m21', 'When average cost is falling, marginal cost is:', ['Less than average cost', 'Greater than average cost', 'Equal to average cost', 'Zero'], 0, 'MC below AC pulls AC down.', 'c5'),
        Q('m22', 'The MC curve cuts the ATC curve:', ['At the minimum point of ATC', 'At the maximum point of ATC', 'Where ATC is falling', 'Never'], 0, 'MC = ATC at minimum ATC.', 'c5'),
        Q('m23', 'The minimum point of ATC lies:', ['To the right of the minimum point of AVC', 'To the left of the minimum point of AVC', 'At the same output as AVC minimum', 'On the X-axis'], 0, 'AFC keeps falling after AVC starts rising.', 'c5', 'moderate'),
        Q('m24', 'TC = 500 + 20Q + 2Q². MC of the 11th unit is:', ['62', '90', '42', '962'], 0, 'TC(11) = 962 and TC(10) = 900, so MC = 62. 90 is ATC at 10 units; 42 is AVC at 11 units; 962 is TC itself.', 'c5', 'hard', '(500+20*11+2*11*11)-(500+20*10+2*10*10)'),
        Q('m25', 'The long-run average cost curve is also called:', ['Planning curve / envelope curve', 'Plant curve', 'Demand curve', 'Isocost line'], 0, 'It envelopes the SACs and guides plant choice.', 'c6'),
        Q('m26', 'The LAC curve is tangent to:', ['Each SAC curve, but not at their minimum points (except at the optimum)', 'The minimum points of all SAC curves', 'Only the largest SAC', 'None of the SACs'], 0, 'Falling part touches falling SACs; rising part touches rising SACs.', 'c6', 'moderate'),
        Q('m27', 'The U-shape of the LAC curve is due to:', ['Returns to scale (economies and diseconomies of scale)', 'The law of variable proportions', 'Fixed costs', 'Consumer preferences'], 0, 'In the long run all factors vary.', 'c6'),
        Q('m28', 'Empirical studies suggest many modern firms face an LAC curve that is:', ['L-shaped', 'Inverted U-shaped', 'Vertical', 'Upward sloping throughout'], 0, 'Costs fall and then stay low over a wide range.', 'c6'),
        Q('m29', 'Bulk purchase of raw materials at lower prices by a large firm is a:', ['Commercial economy', 'Technical economy', 'Financial economy', 'External economy'], 0, 'Buying and selling advantages.', 'c7'),
        Q('m30', 'Delays, red tape and loss of control in a very large firm are:', ['Managerial diseconomies', 'Financial economies', 'External economies', 'Technical economies'], 0, 'Management becomes complex.', 'c7'),
        Q('m31', 'Raising capital at lower cost because of the firm\'s goodwill is a:', ['Financial economy', 'Commercial economy', 'Risk-bearing economy', 'External economy'], 0, 'Better security and investor confidence.', 'c7'),
        Q('m32', 'Growth of ancillary industries and a pool of skilled labour when an industry expands are:', ['External economies', 'Internal economies', 'Managerial diseconomies', 'Technical diseconomies'], 0, 'They accrue to all firms in the industry.', 'c8'),
        Q('m33', 'External economies of scale cause the LAC curve of each firm to:', ['Shift downward', 'Shift upward', 'Become vertical', 'Remain unchanged'], 0, 'Internal economies move the firm along its LAC; external ones shift it.', 'c8', 'hard'),
    ]

    questions = [
        {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'TFC of a firm is ₹300. TVC for 0 to 8 units is ₹0, 40, 70, 96, 130, 175, 234, 320 and 430. (a) Compute TC, AVC, ATC and MC. (b) At what output is ATC minimum? (c) Verify the AC–MC relationship. Show steps.',
         'model': [table(['Q', 'TVC', 'TC', 'AVC', 'ATC', 'MC'], [[q, q1_tvc[q], q1_tc[q], q1_avc[q - 1], q1_atc[q - 1], q1_mc[q - 1]] for q in range(1, 9)]),
                   p(f'(b) ATC is lowest at Q = {min(range(1, 9), key=lambda q: q1_atc[q - 1])} (₹{min(q1_atc)}).'),
                   p(f'(c) Up to Q = 7 every MC ({", ".join(str(x) for x in q1_mc[1:7])}) is below the ATC of the previous output, so ATC keeps falling. At Q = 8, MC = {q1_mc[7]} exceeds ATC at Q = 7 (₹{q1_atc[6]}), so ATC rises to ₹{q1_atc[7]}. MC crosses ATC at its minimum, between Q = 7 and 8.')],
         'scheme': [{'id': 's1', 'pt': 'TC column', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'AVC and ATC columns', 'm': 2, 'skill': 'computation'}, {'id': 's3', 'pt': 'MC column', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'Minimum ATC and AC–MC check', 'm': 2, 'skill': 'analysis'}],
         'remarks': ['Many candidates compute MC from TVC correctly — that is fine since MC is independent of TFC.'], 'mistakes': ['Dividing TC by Q for AVC.', 'Treating MC as TC ÷ Q.'], 'tips': ['Lay out all columns in one table; it also helps with ICAI MCQs that ask one figure.'], 'checks': cq1},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'Revenue of a firm is ₹18,00,000 and explicit costs are ₹11,50,000. The owner left a job paying ₹6,00,000 and has invested ₹15,00,000 of own funds that could earn 8%. Compute accounting and economic profit and advise.',
         'model': [p(f'Accounting profit = 18,00,000 − 11,50,000 = {R(q2_acc)}.'), p(f'Implicit costs = 6,00,000 + 8% × 15,00,000 = {R(q2_imp)}.'),
                   p(f'Economic profit = {R(q2_acc)} − {R(q2_imp)} = −{R(-q2_eco)} (an economic loss). The firm does not even earn normal profit; the owner would be better off in his old job with the money invested elsewhere, unless the business is expected to improve.')],
         'scheme': [{'id': 's1', 'pt': 'Accounting profit', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'Implicit costs', 'm': 1, 'skill': 'computation'}, {'id': 's3', 'pt': 'Economic profit (negative)', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'Advice based on economic profit', 'm': 1, 'skill': 'conclusion'}],
         'remarks': ['A positive accounting profit with a negative economic profit is a classic exam twist.'], 'mistakes': ['Omitting interest on own capital.'], 'tips': ['State the sign of economic profit clearly.'], 'checks': cq2},
        {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'hard', 'pad': 'text',
         'q': 'TC = 1,000 + 50Q + 0.5Q². (a) At Q = 20, compute TC, AFC and ATC. (b) Find MC of the 21st unit. (c) Find the output at which ATC is minimum.',
         'model': [p(f'(a) TC = 1,000 + 1,000 + 200 = {R(q3_tc)}; AFC = 1,000 ÷ 20 = {R(q3_afc)}; ATC = {inr(q3_tc)} ÷ 20 = {R(q3_atc)}.'),
                   p(f'(b) TC(21) = 1,000 + 1,050 + 220.5 = {R(q3_tc21)}; MC = {inr(q3_tc21)} − {inr(q3_tc)} = {R(q3_mc)}.'),
                   p(f'(c) ATC = 1,000/Q + 50 + 0.5Q. Minimum where 1,000/Q = 0.5Q → Q² = 2,000 → Q ≈ {q3_qr} units.')],
         'scheme': [{'id': 's1', 'pt': 'TC, AFC, ATC at 20', 'm': 2, 'skill': 'computation'}, {'id': 's2', 'pt': 'MC of 21st unit', 'm': 1.5, 'skill': 'computation'}, {'id': 's3', 'pt': 'Output at minimum ATC', 'm': 1.5, 'skill': 'computation'}],
         'remarks': ['Separate fixed (constant) and variable terms first.'], 'mistakes': ['Including fixed cost in MC.'], 'tips': ['For TC = a + bQ + cQ², ATC is minimum at Q = √(a/c).'], 'checks': cq3},
    ]

    viva = [
        V('v1', 'What is the difference between accounting cost and economic cost?',
          'Accounting cost includes only explicit costs, the actual payments made to outsiders and recorded in the books. Economic cost includes explicit costs plus implicit costs, such as interest on the owner\'s own capital and the salary he could have earned elsewhere. So economic cost is higher and economic profit is lower than accounting profit.',
          [P('p1', 'Accounting cost = explicit costs only (actual payments recorded)', 4, ALT('{a} {x} {e}', a=['accounting cost', 'accounting'], x=['', 'only', 'include only', 'includes only', 'is', 'are', 'means', 'consider only', 'considers only', 'take only', 'takes only'], e=['explicit', 'actual payment', 'cash payment', 'paid out', 'recorded'])),
           P('p2', 'Economic cost = explicit + implicit costs', 4, ALT('{a} {x} {e}', a=['economic cost', 'economic'], x=['', 'include', 'includes', 'is', 'are', 'means', 'also include', 'also includes', 'explicit plus', 'explicit and', 'both explicit and', 'adds'], e=['implicit', 'opportunity', 'own capital', 'own factor'])),
           P('p3', 'Implicit cost examples (interest on own capital, foregone salary)', 2, 'interest|salary|own capital|rent of own|foregone|forgone|could have earned', min=1)], 'c1'),
        V('v2', 'State the relationship between average cost and marginal cost.',
          'Marginal cost is less than average cost when average cost is falling. Marginal cost is greater than average cost when average cost is rising. Marginal cost equals average cost when average cost is at its minimum; that is, the marginal cost curve cuts the average cost curve at its lowest point.',
          [P('p1', 'AC falling → MC < AC', 3, ALT('{a} {f} {m} {l}', '{m} {l} {a} {f}', '{m} {l} {a} {w} {a} {f}', w=['when', 'while'], a=['average cost', 'ac', 'atc'], f=['fall', 'falls', 'falling', 'decreas', 'declin'], m=['marginal cost', 'mc'], l=['less', 'below', 'lower', 'smaller'])),
           P('p2', 'AC rising → MC > AC', 3, ALT('{a} {r} {m} {g}', '{m} {g} {a} {r}', '{m} {g} {a} {w} {a} {r}', w=['when', 'while'], a=['average cost', 'ac', 'atc'], r=['rise', 'rises', 'rising', 'increas'], m=['marginal cost', 'mc'], g=['more', 'greater', 'above', 'higher', 'exceed'])),
           P('p3', 'AC minimum → MC = AC (MC cuts AC at its minimum)', 4, ALT('{m} {c} {a} {x}', '{a} {x} {m} {e}', m=['marginal cost', 'mc', 'mc curve', 'marginal cost curve'], c=['cut', 'cuts', 'intersect', 'equal', 'equals', 'meet'], a=['average cost', 'ac', 'atc'], x=['minimum', 'lowest', 'min'], e=['equal', 'equals', 'same']))], 'c5'),
        V('v3', 'Why is the long-run average cost curve called an envelope or planning curve?',
          'It is called an envelope curve because it touches each short-run average cost curve from below and so envelopes the whole family of plant curves. It is called a planning curve because the firm uses it to plan which size of plant to build for the output it expects to produce, at the lowest possible cost.',
          [P('p1', 'Envelope: tangent to / envelopes all SAC curves from below', 5, 'envelop|tangent|touch|wrap|cover', 'short run|sac|plant curve|short-run|all the curves|each curve', min=2),
           P('p2', 'Planning: helps choose plant size for expected output', 5, 'plan|choose|choice|select|decide', 'plant|size|scale|capacity', min=2)], 'c6'),
        V('v4', 'What is the difference between internal and external economies of scale?',
          'Internal economies arise within a firm when that firm itself expands, from its own technical, managerial, commercial, financial and risk-bearing advantages, and are available only to it. External economies arise outside the firm when the whole industry expands, such as cheaper inputs, skilled labour and ancillary industries, and are available to all firms in the industry.',
          [P('p1', 'Internal: from the firm\'s own expansion, available only to it', 5, ALT('{i} {x} {f}', i=['internal'], x=['', 'arise', 'economies arise', 'economies', 'come', 'due', 'are', 'within'], f=['firm', 'within', 'own', 'itself', 'inside', 'individual'])),
           P('p2', 'External: from expansion of the whole industry, available to all firms', 5, ALT('{e} {x} {f}', e=['external'], x=['', 'arise', 'economies arise', 'economies', 'come', 'due', 'are', 'from', 'when'], f=['industry', 'outside', 'all firm', 'whole industry']))], 'c7'),
        V('v5', 'Should sunk costs be considered while taking a business decision?',
          'No, sunk costs should not be considered. They have already been incurred and cannot be recovered whatever we decide, so they are irrelevant; only incremental costs and benefits of the decision matter.',
          [P('p1', 'No — sunk costs are irrelevant', 4, 'not be considered|not considered|should not|irrelevant|not relevant|ignore|no|never|not be taken|not taken into account|not consider|not count', min=1),
           P('p2', 'Already incurred and cannot be recovered', 3, 'already incurred|already spent|past|cannot be recovered|not recoverable|irrecoverable|cannot recover|can t be recovered|gone', min=1),
           P('p3', 'Only incremental costs and benefits matter', 3, 'incremental|future cost|additional cost|marginal|relevant cost|extra cost', min=1)], 'c2'),
        V('v6', 'Why is the short-run average total cost curve U-shaped?',
          'In the beginning both average fixed cost and average variable cost fall, so average total cost falls; average variable cost falls because of increasing returns to the variable factor. Later, diminishing returns set in and average variable cost rises faster than average fixed cost falls, so average total cost rises. Hence the curve is U-shaped, because of the law of variable proportions.',
          [P('p1', 'Initially falls: AFC falls and AVC falls (increasing returns)', 4, 'afc|average fixed|fixed cost spread|spread', 'increasing return|avc fall|average variable cost fall|both fall', min=1),
           P('p2', 'Later rises: diminishing returns make AVC rise faster than AFC falls', 4, 'diminishing return|avc rise|average variable cost rise|rises faster|more than offset'),
           P('p3', 'Due to law of variable proportions', 2, 'variable proportion|diminishing return|increasing return', min=1)], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Kumar Castings — cost review', 'difficulty': 'moderate',
              'case': ('Kumar Castings produces 400 castings a month. Monthly fixed costs (rent, interest, supervisors\' salaries) are ₹1,20,000 and variable costs are ₹80,000. If output is raised to 410 castings, variable costs rise to ₹84,500. '
                       'The company is also considering joining a newly formed foundry cluster where a common testing lab, a pool of trained moulders and nearby component suppliers are available to all member units.'),
              'mcqs': [
                  Q('k1a', 'Average fixed cost at 400 castings is:', [R(k_afc), R(200), R(500), R(120000)], 0, '1,20,000 ÷ 400 = ₹300. ₹200 is AVC; ₹500 is ATC.', 'c5', 'core', '120000/400'),
                  Q('k1b', 'Average total cost at 400 castings is:', [R(k_atc), R(300), R(200), R(450)], 0, '(1,20,000 + 80,000) ÷ 400 = ₹500.', 'c5', 'core', '(120000+80000)/400'),
                  Q('k1c', 'Marginal cost per casting for the extra 10 castings is:', [R(k_mc_u), R(500), R(4500), R(206)], 0, 'ΔTC = 4,500 for 10 units → ₹450 per unit. Fixed cost does not change.', 'c5', 'moderate', '4500/10'),
                  Q('k1d', 'Since MC (₹450) is below ATC (₹500) at this output, ATC is:', ['Falling', 'Rising', 'At its maximum', 'Equal to AFC'], 0, 'MC below AC pulls AC down.', 'c5', 'moderate'),
                  Q('k1e', 'The common testing lab, trained workers and nearby suppliers in the cluster are:', ['External economies of scale', 'Internal technical economies', 'Managerial diseconomies', 'Sunk costs'], 0, 'They arise from the growth of the industry/cluster and benefit all member firms.', 'c8', 'core'),
              ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch03', 'n': 2, 'title': 'Theory of Cost',
        'outcomes': ['Distinguish the cost concepts used in economic decisions (accounting/economic, outlay/opportunity, direct/indirect, incremental/sunk, historical/replacement, private/social, fixed/variable).',
                     'Explain the cost function and short-run total costs, including semi-variable and stair-step costs.', 'Compute and interpret AFC, AVC, ATC and MC and their relationships.',
                     'Explain the derivation and shape of the LAC curve.', 'Explain internal and external economies and diseconomies of scale.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 60, 'practice': 60}, 'prereq': ['fnd-p4-ch03-u01'],
                 'exam_tip': 'Expect cost-schedule computations (AFC, AVC, ATC, MC), the MC–AC relationship, LAC as an envelope/planning curve, and classification of economies of scale. Read whether the question gives TC or TVC.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {'summary': ['Economic cost = explicit + implicit; economic profit = revenue − economic cost; normal profit is part of cost.', 'Opportunity cost — next best alternative; sunk cost — irrelevant; incremental cost — relevant; social = private + external.',
                                 'Short run: TC = TFC + TVC; TFC horizontal; TVC from origin, first at decreasing then increasing rate.', 'AFC falls throughout; AVC, ATC, MC U-shaped; MC cuts AVC and ATC at their minima; ATC minimum right of AVC minimum.',
                                 'LAC: envelope of SACs, planning curve; tangent to SACs but not at their minima except at optimum; U-shape due to returns to scale; modern firms often L-shaped.', 'Internal economies: technical, managerial, commercial, financial, risk-bearing. External economies: industry expansion — cheaper inputs, skills, ancillaries, infrastructure, information.'],
                     'remember': ['MC = TCn − TCn−1 = ΔTVC/ΔQ (independent of TFC).', 'ATC = AFC + AVC.', 'For TC = a + bQ + cQ², ATC is minimum at Q = √(a/c).'],
                     'traps': ['LAC is not tangent to the minimum points of all SACs.', 'U-shape of SAC = variable proportions; U-shape of LAC = returns to scale.', 'External economies shift the LAC; internal economies move the firm along it.']},
        'quickref': [{'k': 'TC', 'v': 'TFC + TVC'}, {'k': 'AFC / AVC / ATC', 'v': 'TFC/Q; TVC/Q; TC/Q = AFC + AVC'}, {'k': 'MC', 'v': 'TCn − TCn−1 = ΔTC/ΔQ'},
                     {'k': 'AC–MC rule', 'v': 'AC falls: MC < AC; AC rises: MC > AC; AC min: MC = AC'}, {'k': 'Economic profit', 'v': 'Revenue − explicit − implicit costs'}],
        'viva': viva, 'cases': cases,
    }
