"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 2 Framework for Preparation and Presentation of Financial Statements.
Scope follows the ICAI study material (May 2027 onwards); explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch02-u01'
T1 = 'What the Framework is for, and its status'
T2 = 'Components, objective and users of financial statements'
T3 = 'Fundamental accounting assumptions'
T4 = 'Qualitative characteristics and their constraints'
T5 = 'The five elements: asset, liability, equity, income, expense'
T6 = 'Recognition and the equity equation'
T7 = 'Four measurement bases'
T8 = 'Capital and capital maintenance'


def build():
    ck = Checks()
    # ---------- i1: capital maintenance (original figures) ----------
    open_cap = ck.add('8000*3', 'opening capital: 8,000 units at ₹3')
    sales = ck.add('8000*4.5', 'sales: 8,000 units at ₹4.50')
    close_cap = ck.add('8000*4.5-10000', 'closing capital = sales − drawings ₹10,000')
    ret_hc = ck.add('8000*4.5-10000-8000*3', 'retained profit at historical cost')
    open_cpp = ck.add('8000*3*115/100', 'opening capital restated at general index 115')
    ret_cpp = ck.add('8000*4.5-10000-8000*3*115/100', 'retained profit at current purchasing power')
    draw_cpp = ck.add('10000+(8000*4.5-10000-8000*3*115/100)', 'maximum drawings to maintain CPP capital')
    repl = ck.add('8000*3.6', 'cost to replace 8,000 units at ₹3.60')
    ret_phy = ck.add('8000*4.5-10000-8000*3.6', 'retained profit / (shortfall) on physical capital')
    draw_phy = ck.add('10000+(8000*4.5-10000-8000*3.6)', 'maximum drawings to maintain physical capital')
    i1 = {'id': 'i1', 'title': 'Was capital maintained? Three answers to one question', 'difficulty': 'moderate', 'minutes': 10,
          'q': f'Meenal starts a trading business on 1 April with {R(open_cap)} — 8,000 units of a product bought at ₹3 each. During the year she sells all 8,000 units at ₹4.50 and withdraws ₹10,000. At the year-end the general price index has risen from 100 to 115 and the replacement price of the product has risen to ₹3.60 per unit. Test whether capital is maintained under (a) financial capital maintenance at historical cost, (b) financial capital maintenance at current purchasing power and (c) physical capital maintenance at current cost. State the maximum drawings that would have kept capital intact under (b) and (c).',
          'solution': [
              table(['Working', '₹'], [['Sales (8,000 × ₹4.50)', inr(sales)], ['Less: drawings', '10,000'], ['Closing capital (all cash)', inr(close_cap)]], title='Closing capital'),
              table(['Basis', 'Closing capital', 'Capital to be maintained', 'Retained profit / (shortfall)', 'Maintained?'], [
                  ['(a) Historical cost', inr(close_cap), inr(open_cap), inr(ret_hc), 'Yes'],
                  ['(b) Current purchasing power (×115/100)', inr(close_cap), inr(open_cpp), f'({inr(-ret_cpp)})', 'No'],
                  ['(c) Physical capital at current cost (8,000 × ₹3.60)', inr(close_cap), inr(repl), f'({inr(-ret_phy)})', 'No'],
              ], title='Test of capital maintenance'),
              wn('Maximum drawings', f'(b) ₹10,000 − {R(-ret_cpp)} = {R(draw_cpp)}; (c) ₹10,000 − {R(-ret_phy)} = {R(draw_phy)}. Withdrawing more than this leaves too little to buy back the same purchasing power or the same 8,000 units.'),
              note('Same facts, three verdicts: the answer depends on which concept of capital is being maintained.')],
          'checks': None}
    i1['checks'] = list(ck)

    # ---------- i2: equity equation ----------
    ck2 = Checks()
    oa, ol = 800000, 300000
    oe = ck2.add('800000-300000', 'opening equity')
    a1 = ck2.add('800000+50000', 'assets after capital introduced ₹50,000')
    a2 = ck2.add('800000+50000+12000', 'assets after interest received ₹12,000')
    a3 = ck2.add('800000+50000+12000-38500', 'assets after paying ₹38,500 to settle a ₹40,000 creditor')
    l3 = ck2.add('300000-40000', 'liabilities after creditor settled')
    a4 = ck2.add('800000+50000+12000-38500-6000', 'assets after wages paid ₹6,000')
    l5 = ck2.add('300000-40000+2500', 'liabilities after rent outstanding ₹2,500')
    a6 = ck2.add('800000+50000+12000-38500-6000-9000', 'assets after drawings ₹9,000')
    ce = ck2.add('(800000+50000+12000-38500-6000-9000)-(300000-40000+2500)', 'closing equity')
    profit = ck2.add('(800000+50000+12000-38500-6000-9000)-(300000-40000+2500)-(800000-300000)-50000+9000', 'profit = CE − OE − C + D')
    profit2 = ck2.add('12000+1500-6000-2500', 'profit = interest + discount − wages − rent')
    rows = [['Opening', inr(oa), inr(ol), inr(oe)],
            ['(a) Capital introduced ₹50,000', inr(a1), inr(ol), inr(a1 - ol)],
            ['(b) Interest received ₹12,000', inr(a2), inr(ol), inr(a2 - ol)],
            ['(c) ₹40,000 creditor settled for ₹38,500', inr(a3), inr(l3), inr(a3 - l3)],
            ['(d) Wages paid ₹6,000', inr(a4), inr(l3), inr(a4 - l3)],
            ['(e) Rent outstanding ₹2,500', inr(a4), inr(l5), inr(a4 - l5)],
            ['(f) Drawings ₹9,000', inr(a6), inr(l5), inr(ce)]]
    i2 = {'id': 'i2', 'title': 'Tracking A − L = E transaction by transaction', 'difficulty': 'core', 'minutes': 8,
          'q': 'Kiran\'s business starts the year with assets of ₹8,00,000 and liabilities of ₹3,00,000. During the year: (a) she introduces capital of ₹50,000; (b) receives interest of ₹12,000; (c) settles a creditor of ₹40,000 by paying ₹38,500; (d) pays wages of ₹6,000; (e) rent of ₹2,500 is outstanding; (f) withdraws ₹9,000. Show assets, liabilities and equity after each transaction and compute the profit in two ways.',
          'solution': [table(['Transaction', 'Assets ₹', 'Liabilities ₹', 'Equity ₹'], rows, title='A − L = E after each step'),
                       wn('Profit', f'CE − OE − C + D = {inr(ce)} − {inr(oe)} − 50,000 + 9,000 = {R(profit)}. Check: income (interest ₹12,000 + discount ₹1,500) − expenses (wages ₹6,000 + rent ₹2,500) = {R(profit2)}.'),
                       note('Income always comes with an increase in an asset or a decrease in a liability; expenses with the reverse. Capital and drawings change equity but are not income or expense.')],
          'checks': list(ck2)}

    # ---------- i3: value in use ----------
    ck3 = Checks()
    f1, f2, f3, f4 = (round(1 / 1.12 ** k, 3) for k in (1, 2, 3, 4))   # discount factors at 12%, three decimals
    viu = ck3.add('15000*(round(1/1.12,3)+round(1/1.12**2,3)+round(1/1.12**3,3)+round(1/1.12**4,3))', 'value in use')
    rec = ck3.add('max(15000*(round(1/1.12,3)+round(1/1.12**2,3)+round(1/1.12**3,3)+round(1/1.12**4,3)),48000)', 'recoverable amount = higher of VIU and NSP')
    over = ck3.add('60000-max(15000*(round(1/1.12,3)+round(1/1.12**2,3)+round(1/1.12**3,3)+round(1/1.12**4,3)),48000)', 'overstatement')
    i3 = {'id': 'i3', 'title': 'Present value in action: value in use', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A machine is carried at ₹60,000. It will produce net cash inflows of ₹15,000 at the end of each of the next 4 years. It could be sold today for ₹48,000 net. The required rate of return is 12%. Using discount factors rounded to three decimals, find the value in use, the recoverable amount and by how much the machine is overstated.',
          'solution': [table(['Year', 'Cash inflow ₹', 'Factor at 12%', 'Present value ₹'], [
              ['1', '15,000', str(f1), inr(round(15000 * f1))], ['2', '15,000', str(f2), inr(round(15000 * f2))],
              ['3', '15,000', str(f3), inr(round(15000 * f3))], ['4', '15,000', str(f4), inr(round(15000 * f4))], ['Total', '60,000', '', inr(viu)]], num=[1, 3], total=True, title='Value in use'),
              wn('Recoverable amount', f'Higher of value in use {R(viu)} and net selling price ₹48,000 = {R(rec)}. Overstatement = ₹60,000 − {R(rec)} = {R(over)}.'),
              note('Under the present value basis an asset is carried at the discounted future net cash inflows; no asset should be carried above its recoverable amount.')],
          'checks': list(ck3)}

    concepts = [
        C('c1', T1, [
            'ICAI\'s Accounting Standards Board issued the Framework in July 2000. It is the conceptual foundation used to develop new standards and to review existing ones.',
            'It covers: components and objectives of financial statements, the underlying assumptions, qualitative characteristics, the elements, recognition criteria, measurement bases, and the concepts of capital and capital maintenance.',
            'It helps: enterprises (applying standards and handling topics no standard covers yet), ASB (developing and reviewing standards and narrowing permitted alternatives), auditors (forming an opinion on compliance), users (interpreting statements) and anyone following ASB\'s work.',
            'Status and scope: it applies to general-purpose financial statements — usually annual, for external users — of all commercial, industrial and business enterprises, public or private. Special-purpose reports such as tax computations are outside its scope, though it may be used for them where consistent. It is not itself an Accounting Standard and never overrides one: if a standard and the Framework conflict, the standard wins.'],
          'The Framework is the constitution of accounting standards — standards are the detailed laws made under it, and a specific law prevails over the general principle when they clash.',
          'When a client meets a transaction no standard addresses (say, a new kind of loyalty arrangement), the CA reasons from the Framework\'s definitions and recognition criteria.'),
        C('c2', T2, [
            'A complete set normally has a Balance Sheet, a Statement of Profit and Loss, a Cash Flow Statement, plus notes and explanations that are part of the statements. For companies, components follow the Companies Act, 2013 and its exemptions.',
            'Each statement shows a different side of the same events, so none serves every purpose alone: the Balance Sheet shows resources controlled and the claims on them (liquidity and solvency); the Statement of Profit and Loss shows performance for the period; the Cash Flow Statement shows how cash was generated and used across operating, investing and financing activities; notes add supporting detail (accounting policies, segments, related parties, EPS and the like).',
            'Objective: information about financial position, performance and cash flows that helps a wide range of users make economic decisions. Statements meet common needs; they do not give all information (for example non-financial data).',
            'Seven user groups: investors (risk and return, ability to pay dividends), employees (stability, pay, retirement benefits), lenders (repayment of loans and interest), suppliers and trade creditors (payment of dues — usually a shorter horizon than lenders), customers (continuance of supply), government and its agencies (resource allocation, regulation, taxation, national statistics) and the public (local contribution, trends).'],
          'Financial statements are a health report: the balance sheet is the body scan, the profit and loss statement is the fitness test for the year, and the cash flow statement is the record of what came in and went out.',
          'A banker reading a loan proposal focuses on cash flows and debt-service ability; a supplier extending 60-day credit looks at liquidity — the same report serves both.'),
        C('c3', T3, [
            'There are three fundamental accounting assumptions: going concern, accrual and consistency. Because users take them for granted, following them needs no disclosure — but departing from any of them must be disclosed.',
            'Going concern: the enterprise is expected to continue operating in the foreseeable future with no intention or necessity to liquidate or materially curtail operations. That is why assets are carried at cost less depreciation rather than break-up values. If statements are prepared on another basis (for example net realisable values), that basis must be disclosed.',
            'Accrual: revenues and costs are recognised when earned or incurred, not when cash moves, and recorded in the period to which they relate. Section 128(1) of the Companies Act, 2013 requires companies to keep accounts on accrual basis. If any item is on cash basis, say so.',
            'Consistency: policies stay the same from period to period, which makes comparisons over time meaningful. A policy may change only if required by statute, required by an Accounting Standard, or if the change gives a more appropriate presentation.'],
          'The three assumptions are the default settings of a phone — nobody mentions them unless they have been changed, but if you change one you must tell the user.',
          'Auditors weigh going concern every year; a lender recalling loans or a key licence expiring can force statements onto a break-up basis with full disclosure.'),
        C('c4', T4, [
            'Four qualitative characteristics make information useful, within a reasonable cost–benefit balance: understandability, relevance, reliability and comparability.',
            'Understandability: clear to users who have reasonable knowledge of business, economics and accounting.',
            'Relevance: information that can influence users\' economic decisions — helping them evaluate past, present or future events, or confirm or correct earlier evaluations. More is not always better; a flood of irrelevant data confuses. Relevance is judged through materiality — an item is material if omitting or misstating it could influence decisions; it depends on the size and nature of the item. Materiality is a threshold, not a characteristic in itself.',
            'Constraints: timeliness (late information loses relevance; waiting for every detail improves reliability but may be too late — balance the two) and benefit vs cost (benefits of information should exceed the cost of providing it, a matter of judgement).',
            'Reliability: free from material error and bias — faithful representation, substance over form, neutrality, prudence in uncertain outcomes, and completeness.',
            'Comparability: inter-firm and intra-firm comparison, which needs disclosure of the effect of policy changes. Comparability is not mere uniformity — an enterprise should not keep an outdated policy when more relevant and reliable alternatives exist.',
            'True and fair view: the Framework does not define it directly, but applying the qualitative characteristics and the appropriate standards normally produces statements that give a true and fair view.'],
          'Good financial information is like a good map: easy to read (understandable), showing the roads you need (relevant), drawn accurately (reliable) and in the same scale as other maps (comparable).',
          'Materiality is a working tool: auditors set a materiality threshold before an audit to decide which misstatements matter.'),
        C('c5', T5, [
            'The five elements are asset, liability, equity, income and expense. Gains and losses are not separate elements: economically they are income and expenses, differing only in that they can arise inside or outside the normal course of business; they are shown separately because that helps assess performance.',
            'Asset: something the enterprise controls because of past events and from which it expects future economic benefits. It need not be physical (patents, receivables); control, not legal ownership, decides (a lessee recognises an asset under a finance lease; the lessor does not). Insufficient control (an employee\'s talent) means no asset. Benefits expiring within the current period mean an expense (machinery bought by a dealer for resale is inventory and becomes cost of goods sold when sold; unsold items at year-end are closing stock). The cost or value must be reliably measurable.',
            'Liability: a present obligation, created by past events, that the enterprise expects to settle by giving up resources that carry economic benefits. Obligations may be legal (contract, statute) or arise from business practice and custom. A pending damages suit is provided for if loss is more likely than not and the amount can be estimated reliably; otherwise it is a contingent liability, not a liability. Provisions for doubtful debts, depreciation and impairment reduce asset values and are not liabilities. A mere decision to buy assets in future is not a liability — the obligation usually arises on delivery or an irrevocable agreement.',
            'Equity: the residual interest in assets after deducting all liabilities — the owners\' claim (capital and reserves). It changes through owners\' contributions and distributions, and through income and expenses.',
            'Income: a rise in economic benefits during the period — through more or better assets or smaller liabilities — that lifts equity, excluding what owners contribute. It includes revenue (ordinary activities) and gains (e.g. profit on sale of PPE). Expense: decrease in economic benefits — outflows, depletion of assets or incurrence of liabilities — that decreases equity, other than distributions to owners; it includes losses.'],
          'An asset is a tap you control that will keep pouring money; a liability is a tap you must open for someone else; equity is what is left in your bucket.',
          'An onerous purchase commitment — a custom machine ordered but no longer needed — is recognised as a liability and an expense, even before delivery, because the contract is binding.'),
        C('c6', T6, [
            'An element is recognised when (i) it is probable that the related future economic benefit will flow to or from the enterprise, and (ii) its cost or value can be measured reliably.',
            'Income is recognised only when a related increase in an asset or decrease in a liability can be recognised. Example: a bank does not book interest on a non-performing loan because the increase in the asset is not probable.',
            'Expenses are recognised with the related decrease in assets or increase in liabilities, matched with revenue; when benefits extend over several periods they are allocated systematically (depreciation); they are recognised at once when an item stops qualifying as an asset or a liability arises without an asset (warranty). Matching must never create an asset or liability that fails the definitions.',
            'The equation: Assets − Liabilities = Equity. So Closing equity = Opening equity + Capital introduced + (Income − Expenses) − Drawings, and Profit = (Closing assets − Closing liabilities) − (Opening assets − Opening liabilities) − Capital introduced + Drawings.',
            'Since profit is derived from asset and liability values, a change in the valuation basis changes reported profit — the starting point for the idea of capital maintenance.'],
          'Equity is a water tank: owners pour in capital and take out drawings; income is rain that raises the level, expenses are leaks that lower it.',
          'Analysts reconcile the change in net worth with reported profit, capital raised and dividends — a gap signals something passed directly through reserves.'),
        C('c7', T7, [
            'Measurement means fixing the money amount at which an element is recognised. The Framework allows four bases, used in various combinations subject to the standards; standards mostly use historical cost, with exceptions (inventory at lower of cost and net realisable value).',
            'Historical cost: assets at the cash paid (or fair value given) at acquisition, including costs to make them usable; liabilities at proceeds received for the obligation or, in some cases (income-tax), the cash expected to be paid.',
            'Current cost: assets at what it would cost to acquire the same or an equivalent asset now; liabilities at the undiscounted cash needed to settle the obligation now.',
            'Realisable (settlement) value: assets at what they would fetch in an orderly sale now; liabilities at the undiscounted cash expected to be paid in the normal course of business.',
            'Present value: assets at the discounted future net cash inflows they will generate; liabilities at the discounted net cash outflows needed to settle them. PV = A ÷ (1 + r)ⁿ; 1 ÷ (1 + r)ⁿ is the discount factor. Value in use of an asset is its present value; an asset should not be carried above its recoverable amount (the higher of value in use and net selling price).'],
          'Four ways to price your car: what you paid (historical cost), what a new one costs today (current cost), what a buyer would pay you now (realisable value) and what the rides it will give you are worth today (present value).',
          'Impairment testing under AS 28 uses the present-value idea; inventory valuation uses realisable value — a CA moves between bases item by item.'),
        C('c8', T8, [
            'Capital means net assets. A business must keep its net assets intact so that it can operate at least at the same level each year; distributions should not exceed profit after providing for replacement of assets consumed. In rising prices, historical-cost profit may not be enough to do this.',
            'Retained profit = Profit − Drawings = Closing equity − (Opening equity + Capital introduced). Capital is maintained if retained profit is zero or positive. Its value depends on the basis used.',
            'Financial capital maintenance at historical cost: opening and closing equity at historical cost; fine while prices are stable.',
            'Financial capital maintenance at current purchasing power: opening equity restated to closing prices using a general (average) price index. A positive result means funds suffice to replace assets at average closing prices — but individual assets may rise faster than the average.',
            'Physical capital maintenance at current cost: assets (and liabilities) restated to closing current cost using specific price indices. A positive result means the business can replace each asset at its own closing price — preserving operating capacity.'],
          'Maintaining capital is like refilling a car\'s tank: under historical cost you check you have the rupees you started with; under current purchasing power you check those rupees still buy as much in general; under physical capital you check you can buy the same litres of fuel today.',
          'Dividend policy in inflationary times uses this thinking: boards may hold back distributable profit to fund replacement of plant at today\'s prices.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'A going-concern doubt at year-end', 'role': 'Audit manager',
         'situation': 'A client\'s main customer (70% of sales) has gone into insolvency in February. Bank covenants are breached and the bank has recalled its loan.',
         'steps': ['Assess whether the going-concern assumption still holds — is there intention or necessity to liquidate or materially curtail operations?', 'If not a going concern, statements move to a realisable-value basis: assets at NRV, liabilities at settlement amounts including penalties, deferred costs written off.', 'Whatever basis is used, it must be disclosed because a fundamental assumption is not followed.', 'Consider the effect on the audit opinion.'],
         'takeaway': 'Going concern is assumed silently — the moment it fails, both the numbers and the disclosures change.',
         'think': 'Would deferred expenditure still appear as an asset if the business were not a going concern?',
         'answer': 'No — it has no realisable value on a break-up basis, so it is written off in full.'},
        {'id': 'j2', 'title': 'Is it an asset at all?', 'role': 'Accountant at a manufacturing company',
         'situation': 'The CEO wants to show (a) a star engineer\'s know-how and (b) a machine taken on a finance lease as assets, and (c) the decision to buy new plant next year as a liability.',
         'steps': ['(a) Talent is not sufficiently controlled — not an asset.', '(b) Finance-leased machine is controlled — the lessee recognises it even without ownership.', '(c) A future purchase decision is not a present obligation — no liability until delivery or an irrevocable agreement.'],
         'takeaway': 'Apply the definitions literally: control, past event, probable future benefit, reliable measurement.'},
    ]

    mcqs = [
        Q('m1', 'If an Accounting Standard conflicts with the Framework:', ['The Accounting Standard prevails', 'The Framework prevails', 'The enterprise chooses', 'Both are disregarded'], 0,
          'The Framework is not itself an Accounting Standard and nothing in it overrides a specific standard, so in a conflict the standard\'s requirement applies. The trap is to treat the Framework as a higher law because it is conceptual; in fact ASB uses it to write and review standards, and those standards govern. In practice: the Framework is used to fill gaps where no standard deals with an item.', 'c1', T1),
        Q('m2', 'Which of the following is outside the scope of the Framework?', ['A computation of income prepared for tax purposes', 'Annual financial statements of a private company', 'Annual financial statements of a public sector undertaking', 'General-purpose statements of a partnership firm'], 0,
          'The Framework covers general-purpose financial statements prepared for external users by commercial, industrial and business enterprises in both public and private sectors. Special-purpose reports such as tax computations are outside its scope, though it can be applied to them where consistent with their requirements. The trap is the public sector undertaking, which is covered. In practice: a tax computation follows the Income-tax Act, not the Framework.', 'c1', T1),
        Q('m3', 'Which user group usually has a SHORTER time horizon in an enterprise than lenders do?', ['Suppliers and other trade creditors', 'Employees', 'Investors', 'Government'], 0,
          'Trade creditors want to know whether their dues will be paid on time; because credit periods are short, they usually look less far ahead than lenders do — unless the enterprise is a major customer they depend on. The trap is employees, who care about long-term stability and retirement benefits. In practice: suppliers watch liquidity ratios, while banks study long-term cash flows and security.', 'c2', T2),
        Q('m4', 'Which of these is NOT a fundamental accounting assumption?', ['Prudence', 'Going concern', 'Accrual', 'Consistency'], 0,
          'The three fundamental accounting assumptions are going concern, accrual and consistency. Prudence is an aspect of reliability among the qualitative characteristics, not an assumption. The trap is that prudence is also discussed in AS 1 as a consideration in selecting policies. In practice: notes to accounts never need to say "we followed accrual and going concern" — only a departure is disclosed.', 'c3', T3),
        Q('m5', 'Financial statements of an enterprise follow all three fundamental accounting assumptions. Disclosure is:', ['Not required', 'Required for each assumption', 'Required only for going concern', 'Required only for companies'], 0,
          'Users assume these assumptions have been followed, so no disclosure is necessary when they are; only a departure from any of them must be disclosed. The trap is to think every assumption must be stated in the notes. In practice: a statement that a company is no longer a going concern, or that some income is on cash basis, is a red flag that readers must see.', 'c3', T3),
        Q('m6', 'Under the accounting standards framework, an accounting policy may be changed when:', ['Required by statute, by an Accounting Standard, or for a more appropriate presentation', 'The management wants higher profit', 'The auditor changes', 'The enterprise changes its bankers'], 0,
          'Consistency requires the same policies over time; a change is allowed only if a statute requires it, an Accounting Standard requires it, or it results in a more appropriate presentation of the financial statements. The trap is a change to improve reported profit, which is creative accounting. In practice: the effect of any policy change must be disclosed so that comparisons remain meaningful.', 'c3', T3),
        Q('m7', 'Section 128(1) of the Companies Act, 2013 requires companies to keep accounts on:', ['Accrual basis', 'Cash basis', 'Either basis at their choice', 'Hybrid basis'], 0,
          'Section 128(1) makes accrual-basis books of account mandatory for companies, in line with the accrual assumption of the Framework and AS 1. The trap is "either basis", which some non-corporate entities may effectively have. In practice: a company cannot record salaries only when paid; unpaid salary for March is an outstanding liability at 31 March.', 'c3', T3),
        Q('m8', 'Materiality, according to the Framework, is best described as:', ['A threshold or cut-off point for relevance', 'A primary qualitative characteristic', 'A fundamental accounting assumption', 'An element of financial statements'], 0,
          'Relevance is judged through materiality: an item is material if its omission or misstatement could influence users\' economic decisions, depending on the item\'s size and nature. The Framework treats materiality as a threshold or cut-off point rather than a primary characteristic. The trap is calling it a qualitative characteristic. In practice: an auditor sets overall materiality before planning tests.', 'c4', T4, 'moderate'),
        Q('m9', 'Which is NOT one of the aspects of reliability under the Framework?', ['Timeliness', 'Substance over form', 'Neutrality', 'Completeness'], 0,
          'Reliability needs faithful representation, substance over form, neutrality (freedom from bias), prudence and completeness. Timeliness is a constraint that has to be balanced against relevance and reliability, not an aspect of reliability. The trap is substance over form, which the Framework expressly treats as part of reliability. In practice: reporting a finance lease as an asset of the lessee reflects substance over form.', 'c4', T4, 'moderate'),
        Q('m10', 'Under the Framework, gains and losses are:', ['Not separate elements; they are included in income and expenses', 'Separate elements in addition to the five', 'Shown only in the notes', 'Part of equity contributions'], 0,
          'Gains share the economic characteristics of income and losses those of expenses; the only difference is whether they come from routine operations or from outside them. So the Framework does not treat them as separate elements, though they are shown separately for analysis. The trap is to count seven elements. In practice: profit on sale of a used machine is a gain shown separately from sales revenue.', 'c5', T5),
        Q('m11', 'A lessee takes a machine on a finance lease. Under the Framework, the machine is:', ['An asset of the lessee because it controls the machine', 'An asset of the lessor because it owns the machine', 'An asset of both', 'An asset of neither'], 0,
          'What makes an asset is control by the enterprise; legal ownership is not essential. Under a finance lease the lessee controls the asset and recognises it, while the lessor, despite ownership, does not control it and does not show it as its asset. The trap is "the lessor, because it owns it". In practice: lease accounting standards build on this control idea.', 'c5', T5),
        Q('m12', 'Provision for doubtful debts is:', ['A reduction in the value of an asset, not a liability', 'A liability', 'Part of equity', 'Income'], 0,
          'Provisions for doubtful debts, depreciation and impairment losses represent a fall in the value of assets, not obligations to pay anyone, so they are not liabilities under the Framework. The trap is to classify every "provision" as a liability; only provisions that are present obligations requiring an outflow qualify. In practice: the doubtful-debt provision is deducted from trade receivables in the balance sheet.', 'c5', T5, 'moderate'),
        Q('m13', 'A business opens with equity of ₹5,00,000. During the year capital introduced is ₹50,000, drawings ₹9,000 and closing equity ₹5,46,000. Profit for the year is:', ['₹5,000', '₹46,000', '₹55,000', '₹4,000'], 0,
          'Profit = Closing equity − Opening equity − Capital introduced + Drawings = 5,46,000 − 5,00,000 − 50,000 + 9,000 = ₹5,000. The tempting ₹46,000 is just the change in equity, ignoring capital and drawings. In practice: this is how profit is found from a statement of affairs when books are incomplete.', 'c6', T6, 'moderate', check='546000-500000-50000+9000'),
        Q('m14', 'Interest on a non-performing advance is NOT recognised by a bank as income because:', ['The related increase in the asset is not probable', 'Banks cannot earn interest', 'Interest is always a capital receipt', 'The advance is a liability'], 0,
          'Income can be recognised only when a corresponding increase in an asset or decrease in a liability can be recognised. For a non-performing loan the flow of benefit is not probable, so the asset (interest receivable) cannot be recognised and neither can the income. The trap is to think the interest is not legally due — it is due, but not probable of collection. In practice: banking norms stop interest accrual on NPAs for the same reason.', 'c6', T6, 'moderate'),
        Q('m15', 'Under the current cost basis, liabilities are carried at:', ['The undiscounted amount needed to settle the obligation currently', 'The discounted amount of future outflows', 'The proceeds originally received', 'Nil'], 0,
          'Current cost carries assets at the price to acquire them now and liabilities at the undiscounted cash needed to settle them now. The discounted amount is the present value basis — the usual trap. Proceeds originally received describe historical cost. In practice: a foreign-currency liability on current cost uses today\'s exchange rate without discounting.', 'c7', T7, 'moderate'),
        Q('m16', 'The present value of ₹11,200 receivable after one year at 12% is:', ['₹10,000', '₹11,200', '₹9,856', '₹12,544'], 0,
          'PV = A ÷ (1 + r)ⁿ = 11,200 ÷ 1.12 = ₹10,000. The trap ₹9,856 is 11,200 × 0.88, which wrongly deducts 12% instead of discounting. ₹12,544 compounds forward instead of discounting back. In practice: value in use for impairment testing is built from exactly these discounting steps.', 'c7', T7, check='11200/1.12'),
        Q('m17', 'A trader\'s opening capital is ₹24,000 and the general price index rises from 100 to 115. Under financial capital maintenance at current purchasing power, the capital to be maintained is:', ['₹27,600', '₹24,000', '₹28,800', '₹20,870'], 0,
          'Opening capital is restated with the general index: 24,000 × 115 ÷ 100 = ₹27,600. ₹24,000 is the historical-cost figure; ₹28,800 would come from a specific price index of 120 (physical capital). In practice: this restatement shows how much of reported profit is only inflation.', 'c8', T8, 'moderate', check='24000*115/100'),
        Q('m18', 'Which capital maintenance concept ensures funds to replace EACH asset at its own closing price?', ['Physical capital maintenance at current cost', 'Financial capital maintenance at historical cost', 'Financial capital maintenance at current purchasing power', 'Cash basis capital maintenance'], 0,
          'Physical capital maintenance restates assets and liabilities using specific price indices for each item, so a positive retained profit means each asset can be replaced at its own closing price, preserving operating capacity. Current purchasing power uses a general average index, which is the trap — individual prices may rise faster than the average. In practice: capital-intensive businesses think in these terms when setting dividends.', 'c8', T8),
    ]

    ckq = Checks()
    q_open = ckq.add('5000*4', 'q2 opening capital'); q_close = ckq.add('5000*6-9000', 'q2 closing capital')
    q_cpp = ckq.add('5000*4*110/100', 'q2 opening capital at general index 110'); q_rcpp = ckq.add('5000*6-9000-5000*4*110/100', 'q2 retained (CPP)')
    q_rep = ckq.add('5000*4.6', 'q2 replacement of 5,000 units at ₹4.60'); q_rphy = ckq.add('5000*6-9000-5000*4.6', 'q2 retained (physical)')
    q_hc = ckq.add('5000*6-9000-5000*4', 'q2 retained (historical)')
    questions = [
        W('q1', 5, 'Explain the three fundamental accounting assumptions. When is disclosure needed in respect of them?',
          [p('The Framework recognises three fundamental accounting assumptions — going concern, accrual and consistency.'),
           ul(['Going concern: the enterprise is expected to keep operating for the foreseeable future; it neither plans nor is forced to wind up or sharply cut back its operations. If statements are prepared on another basis, such as realisable values, that basis must be disclosed.',
               'Accrual: revenues and costs are recognised as they are earned or incurred, not as cash is received or paid, and recorded in the periods to which they relate. Section 128(1) of the Companies Act, 2013 requires companies to keep accounts on accrual basis.',
               'Consistency: accounting policies are applied consistently from one period to another; a change is permitted only if required by statute or an Accounting Standard, or for a more appropriate presentation.']),
           p('Disclosure: if these assumptions are followed, no disclosure is required because users presume them. If any of them is not followed, that fact must be disclosed.')],
          [S('s1', 'Going concern explained', 1.5, 'concept', 'going concern', 'foreseeable future|continue|liquidat|curtail'),
           S('s2', 'Accrual explained (s.128(1))', 1.5, 'concept', 'accrual', 'earned|incurred|not when cash|not as cash|period'),
           S('s3', 'Consistency explained and when policy may change', 1, 'concept', 'consisten', 'statute|accounting standard|appropriate presentation|from one period|same polic'),
           S('s4', 'Disclosure only on departure', 1, 'concept', 'disclos', 'not followed|departure|not required|no disclosure|deviat')],
          ['Most students explain the assumptions well but forget the disclosure rule, which carries a full mark.'],
          ['Listing prudence or materiality as an assumption.', 'Saying the assumptions must always be disclosed.'],
          ['One numbered point per assumption, then one line on disclosure.']),
        W('q2', 6, 'Rohan started business with 5,000 units of a product bought at ₹4 each. He sold all the units at ₹6 each and withdrew ₹9,000. At the year-end the general price index rose from 100 to 110 and the replacement price of the product became ₹4.60. Ascertain whether capital is maintained under the three concepts of capital maintenance.',
          [table(['Basis', 'Closing capital ₹', 'Capital to be maintained ₹', 'Retained profit / (shortfall) ₹', 'Result'], [
              ['Financial — historical cost', inr(q_close), inr(q_open), inr(q_hc), 'Maintained'],
              ['Financial — current purchasing power (×110/100)', inr(q_close), inr(q_cpp), f'({inr(-q_rcpp)})', 'Not maintained'],
              ['Physical — current cost (5,000 × ₹4.60)', inr(q_close), inr(q_rep), f'({inr(-q_rphy)})', 'Not maintained'],
          ]), wn('Closing capital', f'Sales 5,000 × ₹6 = ₹30,000 less drawings ₹9,000 = {R(q_close)} (all cash).')],
          [S('s1', 'Closing capital ₹21,000', 1, 'computation', nums=[q_close]),
           S('s2', 'Historical cost — maintained (retained ₹1,000)', 1.5, 'computation', 'maintain', nums=[q_hc]),
           S('s3', 'CPP — capital to maintain ₹22,000, shortfall ₹1,000', 1.5, 'computation', 'not maintain|shortfall|loss|deficit', nums=[q_cpp]),
           S('s4', 'Physical — replacement ₹23,000, shortfall ₹2,000', 2, 'computation', 'not maintain|shortfall|loss|deficit', nums=[q_rep, -q_rphy])],
          ['Candidates often restate the closing capital instead of the opening capital under CPP.'],
          ['Using the specific price for the CPP test or the general index for physical capital.'],
          ['Present all three tests in one table with the same columns.'], pad='table', difficulty='moderate', checks=list(ckq)),
        W('q3', 5, 'Define "asset" and "liability" as per the Framework. Explain, with one example each, why (a) control rather than ownership decides an asset and (b) a decision to buy an asset next year is not a liability.',
          [p('Asset: a resource that the enterprise controls as a consequence of past events and which is expected to bring it future economic benefits.'),
           p('Liability: a present obligation of the enterprise that has arisen from past events and whose settlement is expected to need an outflow of resources carrying economic benefits.'),
           p('(a) Control: a machine taken on a finance lease is controlled by the lessee, which enjoys its benefits and bears its risks; the lessee recognises it as an asset although the lessor owns it. The lessor does not recognise it because it no longer controls it.'),
           p('(b) Future purchase: a board decision to buy plant next year creates no present obligation arising from a past event; the enterprise can still change its mind. A liability arises only when the plant is delivered or an irrevocable agreement is signed.')],
          [S('s1', 'Asset definition — control, past events, future economic benefits', 1.5, 'concept', 'control', 'past event', 'future economic benefit|economic benefit', n=2),
           S('s2', 'Liability definition — present obligation, past events, outflow', 1.5, 'concept', 'present obligation', 'past event', 'outflow', n=2),
           S('s3', 'Finance lease example — lessee recognises', 1, 'application', 'lease', 'lessee'),
           S('s4', 'Future decision not a present obligation — arises on delivery / irrevocable agreement', 1, 'application', 'no present obligation|not a present obligation|not present obligation|no liability|not a liability', 'deliver|irrevocable')],
          ['Definitions must contain all three parts to earn the marks.'], ['Saying the lessor shows the leased asset because it owns it.'],
          ['Quote the definitions word-perfect in meaning, then give the example.'], difficulty='moderate'),
    ]

    viva = [
        V('v1', 'What is the status of the Framework and what happens if it conflicts with an Accounting Standard?',
          'The Framework is not an Accounting Standard. It applies to general purpose financial statements, and if it conflicts with an Accounting Standard, the Accounting Standard prevails.',
          [P('p1', 'Not itself an Accounting Standard', 4, 'not an accounting standard|not a standard|not itself|not accounting standard'),
           P('p2', 'Accounting Standard prevails in a conflict', 4, 'standard prevail|standard override|standard wins|standard will prevail|standard apply|standard applies'),
           P('p3', 'Applies to general purpose statements', 2, 'general purpose|external user')], 'c1'),
        V('v2', 'Name the three fundamental accounting assumptions and state the disclosure rule.',
          'The three assumptions are going concern, accrual and consistency. No disclosure is needed when they are followed, but if any one is not followed, that fact must be disclosed.',
          [P('p1', 'Going concern', 2, 'going concern'), P('p2', 'Accrual', 2, 'accrual'), P('p3', 'Consistency', 2, 'consisten'),
           P('p4', 'Disclose only if not followed', 4, 'not followed|departure|deviat|not follow', 'disclos')], 'c3'),
        V('v3', 'What are the four qualitative characteristics of financial statements?',
          'They are understandability, relevance, reliability and comparability.',
          [P('p1', 'Understandability', 2, 'understandab'), P('p2', 'Relevance', 3, 'relevan'), P('p3', 'Reliability', 3, 'reliab'), P('p4', 'Comparability', 2, 'comparab')], 'c4'),
        V('v4', 'Define an asset as per the Framework.',
          'An asset is a resource that the enterprise controls because of past events, and from which it expects future economic benefits to flow in.',
          [P('p1', 'Resource controlled', 4, 'control'), P('p2', 'Result of past events', 3, 'past event'), P('p3', 'Future economic benefits expected', 3, 'future economic benefit|future benefit|economic benefit')], 'c5'),
        V('v5', 'Explain the three concepts of capital maintenance.',
          'Financial capital maintenance at historical cost compares closing and opening equity at historical cost. Financial capital maintenance at current purchasing power restates opening equity using a general price index. Physical capital maintenance at current cost restates assets using specific price indices so each asset can be replaced at its current price.',
          [P('p1', 'Historical cost — compare at historical cost', 3, 'historical cost'), P('p2', 'Current purchasing power — general price index', 3, 'purchasing power', 'general|average'),
           P('p3', 'Physical capital — specific price indices / replacement', 4, 'physical', 'specific|replace|current cost')], 'c8'),
    ]

    cases = [{'id': 'k1', 'title': 'Year-end questions at Banyan Traders', 'difficulty': 'moderate',
              'case': 'Banyan Traders opens the year with assets ₹6,00,000 and liabilities ₹2,00,000. During the year: the proprietor brings in ₹40,000; a pending damages claim of ₹75,000 is, in the lawyer\'s view, more likely than not to be lost and the amount is reliably estimated; the proprietor plans to buy a delivery van next year; and a ₹30,000 creditor is settled for ₹28,000. Closing equity is ₹4,62,000 and drawings were ₹18,000.',
              'mcqs': [
                  M('k1a', 'The damages claim should be:', ['Recognised as a liability (provision) with a charge to profit', 'Disclosed only as a contingent liability', 'Ignored until the court decides', 'Shown as a reduction of equity directly'], 0,
                    'Loss is more likely than not and the amount can be estimated reliably, so there is a present obligation from a past event and a probable outflow — a provision is recognised by a charge to profit. It would only be a contingent liability if the loss were not probable or not measurable. The trap is waiting for the court\'s decision, which ignores the accrual and prudence logic. In practice: lawyers\' confirmations are a standard audit procedure for such claims.', 'moderate', topic=T5),
                  M('k1b', 'The plan to buy a van next year is:', ['Not a liability — there is no present obligation yet', 'A liability for the expected price', 'A contingent liability', 'An asset'], 0,
                    'A management decision to acquire assets in future does not by itself create a present obligation; one normally arises on delivery or an irrevocable agreement. So nothing is recognised now. The trap is the contingent liability, which needs a possible obligation from past events. In practice: capital commitments under signed contracts may be disclosed, but a mere plan is not.', 'core', topic=T5),
                  M('k1c', 'The ₹2,000 saved on settling the creditor is:', ['Income — a decrease in a liability that increases equity', 'Capital introduced', 'A reduction of drawings', 'Not recorded'], 0,
                    'Income includes decreases in liabilities that increase equity other than owners\' contributions. The liability fell by ₹30,000 while assets fell by only ₹28,000, so equity rose by ₹2,000 — discount earned. The trap is calling it capital introduced; the proprietor did not contribute it. In practice: such discounts appear as "discount received" in the profit and loss account.', 'core', topic=T5),
                  M('k1d', 'Profit for the year is:', ['₹40,000', '₹62,000', '₹22,000', '₹58,000'], 0,
                    'Opening equity = 6,00,000 − 2,00,000 = ₹4,00,000. Profit = Closing equity − Opening equity − Capital introduced + Drawings = 4,62,000 − 4,00,000 − 40,000 + 18,000 = ₹40,000. The trap ₹62,000 is the raw change in equity; ₹22,000 forgets to add back drawings. In practice: this equation is the backbone of single-entry profit computation.', 'hard', check='462000-(600000-200000)-40000+18000', topic=T6),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch02', 1, 'Framework for Preparation and Presentation of Financial Statements',
                ['Explain the purpose, status and scope of the Framework and its relationship with Accounting Standards.',
                 'Describe the components and objective of financial statements and the information needs of the seven user groups.',
                 'Apply the fundamental accounting assumptions and the qualitative characteristics, including materiality and their constraints.',
                 'Define the five elements, apply the recognition criteria and use the equation Profit = CE − OE − C + D.',
                 'Compare the four measurement bases and test capital maintenance under historical cost, current purchasing power and physical capital.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 45, 'practice': 40}, 'prereq': ['int-p1-ch01-u01'],
                 'exam_tip': 'Capital maintenance and going-concern vs NRV numericals are set regularly; in theory, definitions of elements and the qualitative characteristics carry marks only when stated completely.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Framework (ASB, July 2000): basis for standards; not itself a standard; a standard prevails in conflict; covers general-purpose statements only.',
                             'Components: Balance Sheet, Statement of Profit and Loss, Cash Flow Statement, notes. Seven user groups.',
                             'Assumptions: going concern, accrual (s.128(1) for companies), consistency — disclose only departures.',
                             'Qualitative characteristics: understandability, relevance (materiality = threshold), reliability (faithful, substance over form, neutral, prudent, complete), comparability. Constraints: timeliness, benefit > cost.',
                             'Elements: asset, liability, equity, income, expense. Recognise when benefit is probable and measurable.',
                             'Profit = CE − OE − C + D. Measurement: historical cost, current cost, realisable value, present value.',
                             'Capital maintenance: financial (historical cost), financial (current purchasing power, general index), physical (current cost, specific index).'],
                 'remember': ['Control, not ownership, makes an asset.', 'Provisions for depreciation/doubtful debts/impairment are not liabilities.', 'Current cost and realisable value carry liabilities undiscounted.'],
                 'traps': ['Prudence is part of reliability, not an assumption.', 'Gains and losses are not separate elements.', 'CPP restates opening equity with a GENERAL index; physical capital uses SPECIFIC prices.']},
                [('Framework', 'ASB, July 2000; not a standard; standard prevails'), ('Assumptions', 'Going concern · Accrual · Consistency'),
                 ('Qualitative', 'Understandability · Relevance · Reliability · Comparability'), ('Elements', 'Asset · Liability · Equity · Income · Expense'),
                 ('Profit', 'CE − OE − C + D'), ('Present value', 'A ÷ (1 + r)ⁿ'), ('Measurement', 'Historical cost · Current cost · Realisable value · Present value'),
                 ('Capital maintenance', 'Historical cost · CPP (general index) · Physical (specific prices)')],
                viva, cases,
                topics=['Introduction', 'Purpose of the Framework', 'Status and Scope of the Framework', 'Components of Financial Statements', 'Objectives and Users of Financial Statements',
                        'Fundamental Accounting Assumptions', 'Qualitative Characteristics of Financial Statements', 'True and Fair View', 'Elements of Financial Statements',
                        'Measurement of Elements of Financial Statements', 'Capital Maintenance'])
