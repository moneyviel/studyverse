"""CA Foundation · Paper 1 Accounting · Chapter 1 Theoretical Framework · Unit 5 Accounting Policies.
Original explanations, figures and questions (structure and scope follow the ICAI study material)."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p1-ch01-u05'


def build():
    # ---------------- Illustration 1: weighted average to FIFO ----------------
    c1 = Checks()
    tot_cost = c1.add('1000*50+1500*56+1500*60', 'Cost of 4,000 units purchased')
    avg = c1.add('224000/4000', 'Weighted average cost per unit')
    ci_wa = c1.add('1000*56', 'Closing inventory — weighted average')
    ci_fifo = c1.add('1000*60', 'Closing inventory — FIFO (latest purchases remain)')
    sales = c1.add('3000*90', 'Sales 3,000 units @ ₹90')
    gp_wa = c1.add('270000-(224000-56000)', 'Gross profit — weighted average')
    gp_fifo = c1.add('270000-(224000-60000)', 'Gross profit — FIFO')
    eff1 = c1.add('106000-102000', 'Increase in profit due to the change')
    wa_tbl = table(['Particulars', 'Weighted average (₹)', 'FIFO (₹)'], [
        ['Sales (3,000 × 90)', inr(sales), inr(sales)],
        ['Less: Purchases (4,000 units)', '-' + inr(tot_cost), '-' + inr(tot_cost)],
        ['Add: Closing inventory (1,000 units)', inr(ci_wa), inr(ci_fifo)],
        ['Gross profit', inr(gp_wa), inr(gp_fifo)],
    ], num=[1, 2], total=True, title='Effect of changing the cost formula — Nova Electricals, 2026-27')

    # ---------------- Illustration 2: including production overheads ----------------
    c2 = Checks()
    old = c2.add('2000*150', 'Closing inventory — old policy (material + labour)')
    new = c2.add('2000*(150+30)', 'Closing inventory — new policy (with production overheads)')
    eff2 = c2.add('360000-300000', 'Increase in closing inventory and profit')
    oh_tbl = table(['Basis', 'Old policy', 'New policy'], [
        ['Cost included per unit', 'Material + labour ₹150', 'Material + labour ₹150 + production overheads ₹30'],
        ['Closing inventory (2,000 units)', R(old), R(new)],
        ['Effect on profit for the year', '—', f'Higher by {R(eff2)}'],
        ['Effect on balance sheet', '—', f'Inventory (current assets) higher by {R(eff2)}'],
    ], title='Omkar Foods — change in inventory valuation policy')

    sel_tbl = table(['Consideration', 'What it means when choosing a policy', 'Example'], [
        ['Prudence', 'Under uncertainty, choose the treatment that does not overstate assets or income, without creating secret reserves', 'Finished goods valued at lower of cost and net realisable value'],
        ['Substance over form', 'Account for the economic reality, not merely the legal form', 'Asset whose risks and rewards have passed recorded as purchased although registration is pending'],
        ['Materiality', 'Policies should deal properly with every item that could influence users\' decisions; trivial items may be treated simply', 'Small tools below a set limit expensed on purchase'],
    ], title='Three considerations in selecting accounting policies')

    concepts = [
        {'id': 'c1', 'title': 'What accounting policies are',
         'body': ['Accounting policies are the particular accounting principles an enterprise picks, together with the methods it uses to apply them, in preparing and presenting its financial statements. They rest on the concepts, principles and conventions of Unit 2.',
                  'There is no single list of policies that suits every enterprise in every situation: businesses work in varied and complex conditions, so management has to use careful judgement to choose the policy that fits its circumstances. ICAI, with the government, regulators and progressive managements, has been narrowing the range of acceptable policies through Accounting Standards and Guidance Notes.',
                  'Areas where different policies are often found include valuation of inventories and valuation of investments (the list is illustrative, not exhaustive — depreciation is another familiar example). For instance, an enterprise holding shares may value them using FIFO or the average method; the method chosen is its accounting policy.'],
         'analogy': 'Two cooks follow the same recipe principle ("cook till done") but choose different methods — oven or stove. The method each picks, and sticks to, is like an accounting policy.',
         'work': 'Every annual report begins its notes with "Significant accounting policies". Analysts and auditors read it first, because the same transactions can give different profits under different policies.'},
        {'id': 'c2', 'title': 'Selecting accounting policies',
         'body': ['The choice of policy is an important management decision: it affects both the measured performance and the financial position. An inappropriate policy can understate or overstate both, so policies must be chosen with care, looking at their effect from the angle of the various users.',
                  'Three major considerations govern selection and application: prudence, substance over form and materiality. The aim is that the financial statements present the position in the balance sheet and the result in the profit and loss account truly and fairly.',
                  'Typical policy statements: inventories valued at cost, except finished goods at the lower of cost and market value and by-products at net realisable value; long-term investments valued at acquisition cost with provision for permanent fall in value where necessary.',
                  'Disclosure of the policy adopted is always necessary — but disclosure cannot cure a wrong or inappropriate treatment. A wrong policy must be corrected, not merely disclosed.'],
         'blocks': [sel_tbl],
         'analogy': 'Telling a passenger "I drive on the wrong side of the road" (disclosure) does not make the journey safe; you have to drive on the correct side (correct policy).',
         'work': 'When advising a new company, a CA drafts its accounting policies manual — inventory method, depreciation method and rates, revenue recognition — choosing options that are prudent, reflect substance and are consistent with Accounting Standards.'},
        {'id': 'c3', 'title': 'Changing an accounting policy',
         'body': ['A change in accounting policy should be made only if (a) it is required by a statute or for compliance with an Accounting Standard, or (b) the change would result in a more appropriate presentation of the financial statements.',
                  'A change may materially affect items in the financial statements — for example, switching the inventory cost formula from weighted average to FIFO, starting to capitalise interest that was earlier expensed, or starting to include a share of interest or production overheads in inventory. Each can raise or lower the net profit.',
                  'Unless the effect of the change is quantified, users cannot compare the figures with those of earlier years. Therefore the effect of the change on assets, liabilities and profit or loss must be worked out and disclosed.'],
         'analogy': 'If a cricket board changes the size of the boundary mid-season, it must tell everyone how many extra sixes that produced — otherwise run totals cannot be compared with last season.',
         'work': 'When a client changes its inventory method, the auditor checks the reason (standard, law or better presentation — not profit management), recalculates the effect and verifies the disclosure in the notes.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Weighted average to FIFO — quantifying the effect', 'difficulty': 'moderate', 'minutes': 12,
         'q': 'Nova Electricals had no opening inventory on 1 April 2026. It bought 1,000 units at ₹50 in April, 1,500 units at ₹56 in July and 1,500 units at ₹60 in December, and sold 3,000 units at ₹90 each. Until now it used the weighted average cost formula (periodic). It decides to change to FIFO because it believes this gives a more appropriate presentation. Compute the gross profit under both formulas and the effect of the change that must be disclosed.',
         'solution': [wn('Weighted average', f'Total cost 50,000 + 84,000 + 90,000 = ₹{inr(tot_cost)} for 4,000 units → ₹{inr(avg)} per unit. Closing inventory 1,000 × {inr(avg)} = ₹{inr(ci_wa)}.'),
                      wn('FIFO', f'The earliest units are sold first, so the 1,000 units left come from the December lot at ₹60: closing inventory ₹{inr(ci_fifo)}.'),
                      wa_tbl,
                      p(f'Effect of the change: closing inventory and gross profit are higher by ₹{inr(eff1)} under FIFO. The note on accounting policies must state the change, the reason and this effect.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Including production overheads in inventory', 'difficulty': 'core', 'minutes': 8,
         'q': 'Omkar Foods valued its closing inventory of 2,000 units of finished goods at material and labour cost of ₹150 per unit. From 2026-27 it decides to include production overheads of ₹30 per unit, believing that this gives a more appropriate presentation. Show the effect of the change.',
         'solution': [oh_tbl, wn('Working', f'Old: 2,000 × 150 = ₹{inr(old)}. New: 2,000 × 180 = ₹{inr(new)}. Difference ₹{inr(eff2)} raises both profit and current assets.'),
                      note('The change is permitted because it gives a more appropriate presentation; the effect must be quantified and disclosed so that this year\'s profit can be compared fairly with last year\'s.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Is the change allowed?', 'difficulty': 'core', 'minutes': 6,
         'q': 'State whether each proposed change in accounting policy is acceptable: (1) a company changes its depreciation method because a newly notified Accounting Standard requires it; (2) a company switches its inventory formula in a bad year only to report a higher profit; (3) a company starts valuing by-products at net realisable value because it gives a more appropriate presentation; (4) a company keeps a wrong policy but explains it fully in the notes.',
         'solution': [table(['Proposal', 'Acceptable?', 'Reason'], [
             ['(1) Change to comply with an Accounting Standard', 'Yes', 'Compliance with a standard is a valid ground'],
             ['(2) Change only to show higher profit', 'No', 'Not required by law or a standard and not a more appropriate presentation — it is profit management'],
             ['(3) By-products at net realisable value for better presentation', 'Yes', 'A more appropriate presentation is a valid ground; effect must be quantified'],
             ['(4) Wrong policy disclosed in notes', 'No', 'Disclosure cannot rectify a wrong or inappropriate treatment'],
         ])]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'A client wants to "improve" profit', 'role': 'Practising CA finalising a private company\'s accounts',
         'situation': 'Sales have fallen. The managing director suggests changing the depreciation method from written-down value to straight-line this year "to show better profit to the bank".',
         'steps': ['Explain the permitted grounds for a change: a statute, an Accounting Standard, or a more appropriate presentation.',
                   'Ask whether the pattern in which the assets\' benefits are consumed has genuinely changed; if not, the reason given is profit management.',
                   'If a change is justified, compute its effect on depreciation, profit and asset values and disclose it.',
                   'Explain that the bank will read the policy note — an unexplained jump in profit from a policy change damages credibility.'],
         'takeaway': 'Policies are chosen for a true and fair view, not for a target profit. Every change must be justified and its effect disclosed.',
         'think': 'If the change were justified, why must its effect be quantified?',
         'answer': 'Without the figure, users cannot tell how much of the change in profit came from operations and how much from the new policy, so comparison with earlier years would mislead.'},
        {'id': 'j2', 'title': 'Drafting the policy note for a new business', 'role': 'Accounts manager at a start-up trading company',
         'situation': 'The company\'s first annual accounts are due. The auditor asks for a draft "significant accounting policies" note.',
         'steps': ['List the material areas: revenue recognition, inventory valuation (cost formula, lower of cost and net realisable value), depreciation (method and rates), investments, foreign currency.',
                   'For each, choose a policy that is prudent, reflects substance over form and follows the applicable Accounting Standard.',
                   'Write each policy in plain words so that a reader with reasonable business knowledge can understand it.',
                   'Agree the note with the auditor; future years must follow it consistently.'],
         'takeaway': 'The first set of policies becomes the benchmark for consistency in every later year — choose carefully.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'Accounting policies are:', 'options': ['The particular accounting principles chosen by an enterprise and the methods it uses to apply them', 'The rules framed by the Income-tax Department', 'The internal control procedures of a business', 'The auditor\'s report on the financial statements'], 'answer': 0, 'explain': "Accounting policies are the specific accounting principles an enterprise chooses, together with the methods of applying them, when preparing and presenting its financial statements — for example, FIFO for inventory or straight-line depreciation. The tempting option, rules framed by the Income-tax Department, confuses tax computation rules with accounting choices; tax rules decide taxable income, not how accounts are presented. In practice: the first note in every Indian company's annual report is 'Significant Accounting Policies'.", 'topic': 'Meaning of Accounting Policies', 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'The three major considerations governing the selection of accounting policies are:', 'options': ['Prudence, substance over form and materiality', 'Going concern, consistency and accrual', 'Entity, money measurement and periodicity', 'Relevance, reliability and comparability'], 'answer': 0, 'explain': 'The three major considerations in selecting accounting policies are prudence, substance over form and materiality. The trap is going concern, consistency and accrual — these are the fundamental accounting assumptions that are presumed to be followed, not the considerations used to choose between alternative policies. Relevance, reliability and comparability are qualitative characteristics of statements. In practice: when choosing a revenue recognition policy, a finance team considers prudence and economic substance, not just legal form.', 'topic': 'Selection of Accounting Policies', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm3', 'q': 'A change in accounting policy should be made:', 'options': ['If required by statute or an Accounting Standard, or for a more appropriate presentation', 'Whenever profits fall', 'Every five years', 'Only when the auditor changes'], 'answer': 0, 'explain': "A change in accounting policy is allowed only if a statute requires it, an Accounting Standard requires it, or the change gives a more appropriate presentation of the financial statements. The tempting option, 'whenever profits fall', describes profit management, which is exactly what the consistency convention guards against. Changing on a fixed timetable or with a new auditor has no basis. In practice: companies moving to Ind AS changed many policies because the new standards required it.", 'topic': 'Change in Accounting Policies', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'A company has followed an inappropriate accounting treatment but has disclosed it fully in the notes. Which statement is correct?', 'options': ['Disclosure cannot rectify a wrong or inappropriate treatment', 'Full disclosure makes the treatment acceptable', 'The treatment becomes correct after auditor approval', 'No disclosure was required'], 'answer': 0, 'explain': "Disclosure of accounting policies is always required, but disclosure cannot rectify a wrong or inappropriate treatment; the treatment itself must be correct. The tempting option, 'full disclosure makes the treatment acceptable', is the classic misconception — a note explaining an error is still an error. Auditor approval does not cure it either. In practice: if a company wrongly capitalises routine expenses, a statutory auditor will qualify the report even if the note describes the policy clearly.", 'topic': 'Selection of Accounting Policies', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm5', 'q': 'Which of these is an example of an area where different accounting policies are commonly found?', 'options': ['Valuation of inventories', 'Recording of a cash sale', 'Payment of salary', 'Posting from journal to ledger'], 'answer': 0, 'explain': 'Different accounting policies are commonly found where accounting standards allow more than one acceptable method, and valuation of inventories is a standard example (FIFO or weighted average), along with depreciation and valuation of investments. The tempting options — a cash sale, salary payment or posting — are routine recording steps with only one correct treatment, so no policy choice arises. In practice: two FMCG companies may report different profits partly because one uses FIFO and the other weighted average.', 'topic': 'Meaning of Accounting Policies', 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm6', 'q': 'Closing inventory under weighted average is ₹84,000 and under FIFO ₹91,500. If a company changes from weighted average to FIFO, profit for the year will:', 'options': ['Increase by ₹7,500', 'Decrease by ₹7,500', 'Increase by ₹91,500', 'Not change'], 'answer': 0, 'explain': "Closing inventory reduces cost of goods sold. A higher closing inventory under FIFO (₹91,500 instead of ₹84,000) lowers cost of goods sold by ₹7,500 and therefore increases profit by ₹91,500 − ₹84,000 = ₹7,500. The tempting option, 'decrease by ₹7,500', reverses the link between closing inventory and profit. In practice: when prices are rising, FIFO usually shows higher inventory and profit than weighted average, which is why such a change must be justified and its effect disclosed.", 'topic': 'Change in Accounting Policies', 'concept': 'c3', 'difficulty': 'moderate'},
        {'id': 'm7', 'q': 'Purchases: 400 units @ ₹100 and 600 units @ ₹110; 700 units sold; no opening inventory. Closing inventory under FIFO is:', 'options': ['₹33,000', '₹32,100', '₹30,000', '₹31,800'], 'answer': 0, 'check': '300*110', 'explain': 'Under FIFO, the earliest goods are treated as sold first. The 700 units sold use up all 400 units at ₹100 and 300 of the ₹110 lot, so the 300 units left are from the latest lot: 300 × ₹110 = ₹33,000. The tempting ₹31,800 is the weighted average figure (300 × ₹106), not FIFO. In practice: FIFO often matches the physical flow of goods in businesses such as pharmaceuticals and groceries, where older stock must be sold first.', 'topic': 'Change in Accounting Policies', 'concept': 'c3', 'difficulty': 'moderate'},
        {'id': 'm8', 'q': 'Same data: 400 units @ ₹100 and 600 units @ ₹110; 700 units sold. Closing inventory under the weighted average method (periodic) is:', 'options': ['₹31,800', '₹33,000', '₹30,000', '₹32,100'], 'answer': 0, 'check': '300*(400*100+600*110)/1000', 'explain': 'Under the periodic weighted average method, average cost = total cost ÷ total units = (₹40,000 + ₹66,000) ÷ 1,000 = ₹106 per unit, so closing inventory = 300 × ₹106 = ₹31,800. The tempting ₹33,000 values all 300 units at the latest price of ₹110, which is FIFO. A simple average of ₹105 would also be wrong, because the lots are of different sizes. In practice: many Indian manufacturers use weighted average costing in their ERP systems for raw materials.', 'topic': 'Change in Accounting Policies', 'concept': 'c3', 'difficulty': 'moderate'},
        {'id': 'm9', 'q': 'Closing inventory of 1,500 units was valued at ₹200 per unit. A new policy adds production overheads of ₹24 per unit. The increase in profit is:', 'options': ['₹36,000', '₹3,36,000', '₹3,00,000', '₹24,000'], 'answer': 0, 'check': '1500*24', 'explain': "Adding production overheads of ₹24 per unit raises closing inventory by 1,500 × ₹24 = ₹36,000. Higher closing inventory means lower cost of goods sold, so profit rises by ₹36,000 in the year of change. The tempting ₹3,36,000 is the new total inventory value (1,500 × ₹224), not the change in profit. In practice: when a company starts absorbing overheads into inventory, as AS 2 requires, it must disclose the effect of this change on the year's profit.", 'topic': 'Change in Accounting Policies', 'concept': 'c3', 'difficulty': 'moderate'},
        {'id': 'm10', 'q': 'Why must the effect of a change in accounting policy be quantified?', 'options': ['So that users can compare the statements with earlier periods', 'To calculate the auditor\'s fee', 'Because tax law prohibits changes', 'To avoid preparing a cash flow statement'], 'answer': 0, 'explain': "A change in policy alters reported profit even if business performance is unchanged. Quantifying its effect lets users separate the impact of the change from real performance and compare the current statements with earlier periods. The tempting option, 'because tax law prohibits changes', is false; tax law does not prohibit accounting policy changes. In practice: analysts reading a listed company's results look for the note quantifying any policy change before comparing year-on-year profit growth.", 'topic': 'Change in Accounting Policies', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm11', 'q': 'Selecting an inappropriate accounting policy may lead to:', 'options': ['Overstatement or understatement of performance and financial position', 'Higher sales volume', 'Lower tax rates', 'Automatic qualification of the auditor'], 'answer': 0, 'explain': "The choice of accounting policy affects both the measured performance (profit) and the financial position (balance sheet), so an inappropriate policy can overstate or understate both. The tempting option, 'higher sales volume', confuses accounting with real business activity — a policy changes how results are reported, not what customers buy. In practice: overly aggressive revenue recognition policies have led to inflated profits in corporate frauds, which is why auditors scrutinise policy choices closely.", 'topic': 'Selection of Accounting Policies', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm12', 'q': 'Which body, working with the government and regulators, issues Accounting Standards and Guidance Notes that narrow down the choice of acceptable policies?', 'options': ['ICAI, along with the government and regulators', 'The Reserve Bank of India alone', 'Each company\'s auditors individually', 'The stock exchanges alone'], 'answer': 0, 'explain': "The Institute of Chartered Accountants of India, working with the government, regulators and progressive managements, issues Accounting Standards and Guidance Notes that narrow the range of acceptable policies. The tempting option, the RBI alone, is a regulator for banks and NBFCs; it prescribes some norms for them but does not issue the general accounting standards. In practice: standards are formulated by ICAI's Accounting Standards Board and notified for companies by the Central Government.", 'topic': 'Meaning of Accounting Policies', 'concept': 'c1', 'difficulty': 'core'},
    ]

    q2c = Checks()
    q2_cost = q2c.add('2000*80+3000*86+1000*92', 'Total cost of 6,000 units')
    q2_avg = q2c.add('510000/6000', 'Weighted average cost per unit')
    q2_wa = q2c.add('1500*85', 'Closing inventory — weighted average')
    q2_fifo = q2c.add('1000*92+500*86', 'Closing inventory — FIFO (1,000 @ 92 + 500 @ 86)')
    q2_eff = q2c.add('135000-127500', 'Increase in closing inventory and profit')
    q2_sales = q2c.add('4500*130', 'Sales 4,500 units @ ₹130')
    q2_gpw = q2c.add('585000-510000+127500', 'Gross profit — weighted average')
    q2_gpf = q2c.add('585000-510000+135000', 'Gross profit — FIFO')
    q2_tbl = table(['Particulars', 'Weighted average (₹)', 'FIFO (₹)'], [
        ['Sales (4,500 × 130)', inr(q2_sales), inr(q2_sales)],
        ['Less: Purchases (6,000 units)', '-' + inr(q2_cost), '-' + inr(q2_cost)],
        ['Add: Closing inventory (1,500 units)', inr(q2_wa), inr(q2_fifo)],
        ['Gross profit', inr(q2_gpw), inr(q2_gpf)],
    ], num=[1, 2], total=True)

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'text',
         'q': 'What are accounting policies? Explain the considerations that should govern their selection, with examples.',
         'model': [p('Accounting policies are the particular accounting principles an enterprise picks, along with the methods it uses to apply them, in preparing and presenting its financial statements. No single set suits all enterprises; management must use judgement to choose policies suited to its circumstances. Common areas: valuation of inventories and of investments.'),
                   sel_tbl,
                   p('The choice affects measured profit and financial position, so it must be made with care, keeping users in view, so that the statements show a true and fair view. Disclosure of the policy is necessary, but disclosure cannot make a wrong treatment right.')],
         'scheme': [
             {'id': 's1', 'pt': 'Meaning of accounting policies', 'm': 1, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Prudence explained with example', 'm': 1, 'skill': 'concept'},
             {'id': 's3', 'pt': 'Substance over form explained with example', 'm': 1, 'skill': 'concept'},
             {'id': 's4', 'pt': 'Materiality explained with example', 'm': 1, 'skill': 'concept'},
             {'id': 's5', 'pt': 'True and fair view / effect on profit and position; disclosure cannot rectify wrong treatment', 'm': 1, 'skill': 'application'},
         ],
         'remarks': ['Candidates frequently name going concern, consistency and accrual as the selection criteria — those are fundamental assumptions, not the selection considerations.', 'Examples are what earn the marks for each consideration.'],
         'mistakes': ['Confusing accounting policies with accounting standards.', 'Omitting the meaning and starting directly with the considerations.'],
         'tips': ['Start with a one-line definition, then a small table of the three considerations with an example each.']},
        {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'Crest Traders had no opening inventory. During 2026-27 it purchased 2,000 units at ₹80, 3,000 units at ₹86 and 1,000 units at ₹92, and sold 4,500 units at ₹130. It used the weighted average (periodic) formula and now changes to FIFO for a more appropriate presentation. Compute the closing inventory and gross profit under both formulas and state the effect of the change. Is the change permitted?',
         'model': [wn('Weighted average', f'Total cost ₹{inr(q2_cost)} ÷ 6,000 = ₹{inr(q2_avg)} per unit; closing inventory 1,500 × {inr(q2_avg)} = ₹{inr(q2_wa)}.'),
                   wn('FIFO', f'Units left are the latest: 1,000 @ ₹92 + 500 @ ₹86 = ₹{inr(q2_fifo)}.'),
                   q2_tbl,
                   p(f'Effect: closing inventory and gross profit are higher by ₹{inr(q2_eff)} under FIFO. The change is permitted because it is made for a more appropriate presentation; the change, its reason and its effect of ₹{inr(q2_eff)} must be disclosed.')],
         'scheme': [
             {'id': 's1', 'pt': f'Weighted average rate ₹{inr(q2_avg)} and closing inventory ₹{inr(q2_wa)}', 'm': 1.5, 'skill': 'computation'},
             {'id': 's2', 'pt': f'FIFO closing inventory ₹{inr(q2_fifo)}', 'm': 1.5, 'skill': 'computation'},
             {'id': 's3', 'pt': 'Gross profit under both formulas', 'm': 1, 'skill': 'computation'},
             {'id': 's4', 'pt': f'Effect ₹{inr(q2_eff)} increase identified', 'm': 1, 'skill': 'analysis'},
             {'id': 's5', 'pt': 'Change permitted (more appropriate presentation) with disclosure of effect', 'm': 1, 'skill': 'conclusion'},
         ],
         'remarks': ['Under FIFO many candidates take all 1,500 units at ₹92, forgetting that only 1,000 units were bought at that price.', 'The conclusion mark requires both the permission ground and the disclosure requirement.'],
         'mistakes': ['Using a simple average of the three prices (₹86) instead of the weighted average (₹85).', 'Stating the effect as a decrease.'],
         'tips': ['Show both computations side by side.', 'Finish with a clear one-line conclusion.']},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'When can an enterprise change its accounting policy? Why should the effect of the change be quantified? Give two examples of such changes.',
         'model': [p('A change in accounting policy should be made only when (a) it is required by a statute or for compliance with an Accounting Standard, or (b) it would result in a more appropriate presentation of the financial statements.'),
                   p('A change can materially increase or decrease profit and alter assets and liabilities. Unless its effect is quantified, users cannot compare the current figures with earlier periods or know how much of the change in profit is due to the policy rather than performance. So the effect on assets, liabilities and profit or loss is quantified and disclosed.'),
                   ul(['Changing the inventory cost formula from weighted average to FIFO.', 'Starting to include production overheads (or a share of interest) in the cost of inventory, or to capitalise interest that was earlier expensed.'])],
         'scheme': [
             {'id': 's1', 'pt': 'Statute / Accounting Standard', 'm': 1, 'skill': 'provision'},
             {'id': 's2', 'pt': 'More appropriate presentation', 'm': 1, 'skill': 'provision'},
             {'id': 's3', 'pt': 'Reason for quantifying effect (comparability)', 'm': 1, 'skill': 'concept'},
             {'id': 's4', 'pt': 'Two valid examples', 'm': 1, 'skill': 'application'},
         ],
         'remarks': ['Good answers keep the grounds to the two listed; adding "to increase profit" as a ground is a serious error.'],
         'mistakes': ['Saying a policy can never be changed.', 'Giving a change in an estimate (useful life) as a change in policy.'],
         'tips': ['Number the two grounds; write the reason for quantifying in one sentence.']},
    ]

    viva = [
        V('v1', 'What do you mean by accounting policies?',
          'Accounting policies are the particular accounting principles an enterprise chooses, along with the methods it uses to apply them, when preparing and presenting its financial statements. For example, valuing inventory using FIFO or weighted average is an accounting policy.',
          [P('p1', 'Specific accounting principles', 3, 'principle|rule|basis'),
           P('p2', 'Methods of applying them', 3, 'method|way|manner|how'),
           P('p3', 'Adopted by the enterprise for preparing/presenting financial statements', 2, 'financial statement|final account|preparing|presentation|presenting|prepar', min=1),
           P('p4', 'Example: inventory/investment valuation method', 2, 'inventor|stock|fifo|average|investment|depreciation', min=1)], 'c1'),
        V('v2', 'Which considerations govern the selection of accounting policies?',
          'Three major considerations govern the selection of accounting policies: prudence, substance over form and materiality. The aim is that the financial statements give a true and fair view.',
          [P('p1', 'Prudence', 3, 'prudence|prudent|conservat|caution'),
           P('p2', 'Substance over form', 3, 'substance'),
           P('p3', 'Materiality', 3, 'material'),
           P('p4', 'True and fair view', 1, 'true and fair|true fair|fair view|true picture|fair picture')], 'c2'),
        V('v3', 'When is a change in accounting policy permitted?',
          'A change in accounting policy is permitted only if it is required by a statute or for compliance with an Accounting Standard, or if the change will result in a more appropriate presentation of the financial statements.',
          [P('p1', 'Required by statute / law', 3, 'statute|statutory|law|legal|act|regulat'),
           P('p2', 'Required to comply with an Accounting Standard', 3, 'accounting standard|standard'),
           P('p3', 'More appropriate presentation of financial statements', 4, 'more appropriate|appropriate present|better present|better presentation|improv|truer|true and fair|true fair|fairer|better picture|better view')], 'c3'),
        V('v4', 'If a wrong accounting treatment is fully disclosed in the notes, does that make it acceptable?',
          'No. Disclosure of the accounting policy adopted is always necessary, but disclosure cannot rectify a wrong or inappropriate treatment. The wrong treatment has to be corrected.',
          [P('p1', 'No — disclosure cannot rectify a wrong treatment', 6, ALT('{d} {n} rectif', '{d} {n} correct', '{d} {n} cure', '{d} {n} make it right', '{d} {n} make it correct', '{d} {n} justif', '{d} {n} acceptable', '{d} {n} fix', '{d} {n} remedy', '{d} {n} valid', '{d} {n} enough', '{d} {n} sufficient', '{d} alone {n}', d=('disclos', 'disclosure'), n=('cannot', 'can not', 'can t', 'does not', 'doesn t', 'will not', 'won t', 'not', 'never'))),
           P('p2', 'Disclosure is still necessary', 2, 'always necessary|still necessary|necessary|required|must be disclos|always disclos|need disclos|still disclos', min=1),
           P('p3', 'The wrong treatment must be corrected', 2, 'correct|rectif|change|fix|right treatment|proper treatment|appropriate treatment', min=1)], 'c2'),
        V('v5', 'Why must the effect of a change in accounting policy be quantified? Give an example of such a change.',
          'Because a change in policy can increase or decrease profit and change assets and liabilities, the effect must be quantified so that users can compare the statements with earlier years and see how much of the change is due to the policy. An example is changing the inventory formula from weighted average to FIFO.',
          [P('p1', 'Policy change can raise/lower profit and alter assets/liabilities', 3, 'profit|loss|asset|liabilit|figure|result', min=1),
           P('p2', 'Quantifying enables comparison with earlier periods / understanding effect', 4, 'compar|not misled|not mislead|avoid mislead|prevent mislead|mislead|understand|earlier year|previous year|past year|earlier period|how much', min=1),
           P('p3', 'Example: weighted average to FIFO / overheads in inventory / capitalising interest', 3, 'fifo|weighted average|average|overhead|interest|depreciation method|inventory|stock', min=1)], 'c3'),
    ]

    c = Checks()
    k_cost = c.add('500*400+700*420+800*450', 'Cost of 2,000 units')
    k_avg = c.add('854000/2000', 'Weighted average rate')
    k_wa = c.add('600*427', 'Closing inventory — weighted average')
    k_fifo = c.add('600*450', 'Closing inventory — FIFO')
    k_eff = c.add('270000-256200', 'Increase in profit due to change')
    cases = [{
        'id': 'k1', 'title': 'Lotus Paints — a change of cost formula', 'difficulty': 'hard',
        'case': ('Lotus Paints had no opening inventory on 1 April 2026. It bought 500 tins at ₹400, 700 tins at ₹420 and 800 tins at ₹450 during the year, and 600 tins remained unsold on 31 March 2027. Until last year it used the weighted average formula. '
                 'The finance director wants to switch to FIFO and argues that "it will lift profit, and anyway we will mention it in the notes".'),
        'mcqs': [
            dict(M('k1a', 'What is the closing inventory under the weighted average formula?', [R(k_wa), R(k_fifo), '₹2,52,000', '₹2,54,000'], 0,
              'Weighted average cost = total cost ÷ total tins. Total cost = (500 × 400) + (700 × 420) + (800 × 450) = ₹8,54,000 for 2,000 tins, so average = ₹427. Closing inventory = 600 × ₹427 = ₹2,56,200. The tempting ₹2,52,000 uses a simple average of the three prices (₹420), ignoring the different quantities. In practice: paint and chemical manufacturers often use weighted average because tins from different lots are physically mixed in the warehouse.', 'moderate', '600*854000/2000'), topic='Change in Accounting Policies'),
            dict(M('k1b', 'What is the closing inventory under FIFO?', [R(k_fifo), R(k_wa), '₹2,40,000', '₹2,52,000'], 0,
              'Under FIFO the oldest tins are treated as sold first, so the 600 tins left are from the latest purchase of 800 tins at ₹450: 600 × ₹450 = ₹2,70,000. The tempting ₹2,56,200 is the weighted average figure. When prices are rising, FIFO leaves the most recent, higher-cost goods in inventory. In practice: during periods of rising input costs, FIFO inventory figures are closer to current replacement cost than weighted average figures.', 'moderate', '600*450'), topic='Change in Accounting Policies'),
            dict(M('k1c', 'By how much will profit change if FIFO is adopted?', [f'Increase of {R(k_eff)}', f'Decrease of {R(k_eff)}', 'Increase of ₹27,000', 'No change'], 0,
              'Closing inventory reduces cost of goods sold. FIFO inventory ₹2,70,000 − weighted average inventory ₹2,56,200 = ₹13,800 higher inventory, so cost of goods sold falls and profit rises by ₹13,800. The tempting option, a decrease of ₹13,800, reverses the link: higher closing inventory raises profit, not lowers it. In practice: this effect would reverse in the following year when the higher opening inventory flows into cost of goods sold.', 'hard'), topic='Change in Accounting Policies'),
            dict(M('k1d', 'Evaluate the finance director\'s reasoning.', ['A change is allowed only for a statute, a standard or a more appropriate presentation — not to lift profit; disclosure does not cure an improper change', 'Any change is fine if it is mentioned in the notes', 'Changes are never allowed once a policy is chosen', 'The change is allowed because FIFO always gives higher profit'], 0,
              'A change in accounting policy is allowed only if a statute or Accounting Standard requires it or the change gives a more appropriate presentation. Lifting profit is not a valid ground, and disclosure does not cure an improper change. The tempting option says any change is fine if noted — that confuses disclosure with justification. If a valid ground exists, the effect must be quantified and disclosed. In practice: auditors challenge policy changes made near year end that conveniently improve profit.', 'hard'), topic='Change in Accounting Policies'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch01', 'n': 5,
        'title': 'Accounting Policies',
        'outcomes': [
            'Explain what accounting policies are and why no single set suits every enterprise.',
            'Apply prudence, substance over form and materiality in selecting accounting policies, and explain why disclosure cannot cure a wrong treatment.',
            'State when a change in accounting policy is permitted and quantify the effect of a change on profit and assets.',
        ],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 20, 'practice': 35}, 'prereq': ['fnd-p1-ch01-u02'],
                 'exam_tip': 'Two lists to learn cold: selection — prudence, substance over form, materiality; change — statute/Accounting Standard or more appropriate presentation. Practise one FIFO vs weighted-average effect computation.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Accounting policies = specific principles + methods of applying them adopted by an enterprise for its financial statements.',
                        'No universal list; management judgement needed. ICAI narrows choices through Accounting Standards and Guidance Notes.',
                        'Selection: prudence, substance over form, materiality — aiming at a true and fair view.',
                        'Change only if required by statute/Accounting Standard or for a more appropriate presentation; quantify and disclose the effect.',
                        'Disclosure is always needed but cannot rectify a wrong treatment.'],
            'remember': ['Typical areas: inventories, investments (also depreciation).', 'Higher closing inventory after a change → higher profit by the same amount.', 'FIFO: closing stock from the latest lots; weighted average: total cost ÷ total units.'],
            'traps': ['Going concern, consistency, accrual are the fundamental assumptions — not the selection criteria.', 'A revision of useful life is a change in estimate, not a change in policy.', '"To show higher profit" is never a valid reason for change.'],
        },
        'quickref': [
            {'k': 'Accounting policies', 'v': 'Specific accounting principles + methods of applying them'},
            {'k': 'Selection', 'v': 'Prudence · Substance over form · Materiality'},
            {'k': 'Change permitted', 'v': 'Statute / Accounting Standard, or more appropriate presentation'},
            {'k': 'After a change', 'v': 'Quantify effect on assets, liabilities and profit; disclose'},
            {'k': 'Disclosure', 'v': 'Always necessary — but cannot rectify a wrong treatment'},
            {'k': 'Weighted average rate', 'v': 'Total cost of units ÷ Total units'},
        ],
        'viva': viva, 'cases': cases,
    }


# ---------- Auto-check data for the Write tab ----------
# Per scheme point: kw (viva-matcher keyword groups, "|" = alternatives) + min (groups needed), nums (figures that must
# appear), rows ([particular keywords, side, amount] for table answers; side may be dr/cr/add/less or a column-header
# keyword such as "provision"), wrong (common wrong statements → remark), ai_only (not checkable offline).
# Per question: extra_ok (may points beyond the model earn credit).
AUTO = {
    'q1': {'extra_ok': True,
           's1': {'kw': ['principle|method|rule|bases|practice', 'prepar|present|financial statement'], 'min': 2},
           's2': {'kw': ['prudence|prudent|conservat', 'lower cost|nrv|net realisable|net realizable|overstat|not overstat|understat|not anticipat|uncertain|loss|lower'], 'min': 2},
           's3': {'kw': ['substance over form|substance form|economic reality|substance', 'legal form|form|hire purchase|lease|registration|risk reward|example'], 'min': 2},
           's4': {'kw': ['material', 'decision|influence|small|trivial|immaterial|insignificant|tool|example|stapler'], 'min': 2},
           's5': {'kw': ['true fair|profit|financial position|position', 'disclosure cannot|cannot rectify|not rectify|cannot correct|cannot cure|not cure|cannot make|not make|wrong treatment|not justify|cannot justify|not substitute'], 'min': 2}},
    'q2': {'extra_ok': False,
           's1': {'nums': [85, 127500]},
           's2': {'nums': [135000]},
           's3': {'nums': [202500, 210000]},
           's4': {'nums': [7500]},
           's5': {'kw': ['permitted|allowed|permissible|can changed|valid|justified|acceptable|permit|allow', 'appropriate|better presentation|fair presentation|true fair', 'disclos'], 'min': 3,
                  'wrong': [{'kw': ['not permitted|not allowed|cannot changed|not permissible|violat consisten'], 'say': 'A change made for a more appropriate presentation is permitted; its reason and effect must be disclosed.'}]}},
    'q3': {'extra_ok': False,
           's1': {'kw': ['statute|law|legal requirement|accounting standard|standard|act'], 'min': 1},
           's2': {'kw': ['appropriate presentation|better presentation|more appropriate|fair presentation|better reflect|appropriate'], 'min': 1},
           's3': {'kw': ['compar|cannot compar|not compar|earlier period|previous year|past period|performance|mislead|understand|users|increase decrease|material effect'], 'min': 1},
           's4': {'kw': ['fifo|weighted average|inventor|stock valuation|cost formula|lifo',
                         'overhead|interest|capitalis|capitaliz|borrowing|investment|revenue recognition|cash basis|accrual basis|depreciation|straight line|written down|slm|wdv|production cost'], 'min': 2}},
}


def _attach_auto(u):
    """Merge AUTO into the questions: every scheme point gets its auto-check fields; every question gets extra_ok."""
    for q in u.get('questions', []):
        a = AUTO[q['id']]
        q['extra_ok'] = a.get('extra_ok', False)
        for s in q['scheme']: s.update(a[s['id']])
        extra = set(a) - {'extra_ok'} - {s['id'] for s in q['scheme']}
        assert not extra, f"AUTO[{q['id']}] has unknown scheme ids {extra}"
    return u


_build_core = build


def build(): return _attach_auto(_build_core())
