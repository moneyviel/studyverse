"""CA Foundation · Paper 1 Accounting · Chapter 1 Theoretical Framework · Unit 2 Accounting Concepts, Principles and Conventions.
Original explanations, figures and questions (structure and scope follow the ICAI study material)."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p1-ch01-u02'


def build():
    # ---------------- Illustration 1: accounting equation and profit ----------------
    c1 = Checks()
    a0 = c1.add('240000+90000+55000+15000', 'Total assets on 31 March 2026')
    l0 = c1.add('150000+60000', 'Total outside liabilities on 31 March 2026')
    e0 = c1.add('400000-210000', 'Capital on 31 March 2026 = Assets − Liabilities')
    a1 = c1.add('225000+104000+68000+21000', 'Total assets on 31 March 2027')
    l1 = c1.add('150000+72000', 'Total outside liabilities on 31 March 2027')
    e1 = c1.add('418000-222000', 'Capital on 31 March 2027 = Assets − Liabilities')
    pr = c1.add('196000-190000+12000', 'Profit = Closing capital − Opening capital + Drawings')
    eq_tbl = table(['Item', '31 Mar 2026 (₹)', '31 Mar 2027 (₹)'], [
        ['Fixed assets', '2,40,000', '2,25,000'],
        ['Trade receivables', '90,000', '1,04,000'],
        ['Inventory', '55,000', '68,000'],
        ['Cash and bank', '15,000', '21,000'],
        ['Total assets (A)', inr(a0), inr(a1)],
    ], num=[1, 2], total=True, title='Assets')
    li_tbl = table(['Item', '31 Mar 2026 (₹)', '31 Mar 2027 (₹)'], [
        ['10% Term loan', '1,50,000', '1,50,000'],
        ['Trade payables', '60,000', '72,000'],
        ['Total outside liabilities (L)', inr(l0), inr(l1)],
    ], num=[1, 2], total=True, title='Outside liabilities')
    bs1 = table(['Liabilities', '₹', 'Assets', '₹'], [
        ['Capital (opening)', '1,90,000', 'Fixed assets', '2,25,000'],
        ['Add: Profit', inr(pr), 'Trade receivables', '1,04,000'],
        ['Less: Drawings', '-12,000', 'Inventory', '68,000'],
        ['10% Term loan', '1,50,000', 'Cash and bank', '21,000'],
        ['Trade payables', '72,000', '', ''],
        ['Total', inr(a1), 'Total', inr(a1)],
    ], num=[1, 3], total=True, title='Balance Sheet of Arora Traders as at 31 March 2027')

    # ---------------- Illustration 2: cash basis vs accrual + matching ----------------
    c2 = Checks()
    rev = c2.add('4500*300', 'Revenue: 4,500 units sold @ ₹300')
    pur = c2.add('6000*200', 'Purchases: 6,000 units @ ₹200')
    cogs = c2.add('4500*200', 'Cost of 4,500 units sold (matched expense)')
    rent = c2.add('5000*12', 'Rent for 12 months (accrued)')
    cashp = c2.add('1100000-950000-50000', 'Cash-basis "profit" = receipts − payments')
    nomatch = c2.add('1350000-1200000-60000', 'Accrual without matching (all purchases charged)')
    prof = c2.add('1350000-900000-60000', 'Profit under accrual + matching')
    inv = c2.add('(6000-4500)*200', 'Closing inventory 1,500 units @ ₹200')
    deb = c2.add('1350000-1100000', 'Trade receivables')
    cash = c2.add('1100000-950000-50000', 'Cash balance')
    cred = c2.add('1200000-950000', 'Trade payables')
    rentdue = c2.add('60000-50000', 'Rent payable')
    c2.add('300000+250000+100000', 'Total assets')
    c2.add('250000+10000+390000', 'Total liabilities + capital (profit)')
    cmp_tbl = table(['Basis', 'Revenue (₹)', 'Expenses (₹)', 'Result (₹)'], [
        ['Cash basis (receipts − payments)', '11,00,000', '10,00,000', inr(cashp)],
        ['Accrual, but all purchases charged (no matching)', inr(rev), '12,60,000', inr(nomatch)],
        ['Accrual + matching (correct)', inr(rev), '9,60,000', inr(prof)],
    ], title='Three ways of measuring the same year')
    pos_tbl = table(['Item', '₹'], [
        ['Inventory (1,500 units × ₹200)', inr(inv)],
        ['Trade receivables (13,50,000 − 11,00,000)', inr(deb)],
        ['Cash (11,00,000 − 9,50,000 − 50,000)', inr(cash)],
        ['Total assets', '6,50,000'],
    ], num=[1], total=True, title='Assets on 31 March 2027')
    pos2_tbl = table(['Item', '₹'], [
        ['Trade payables (12,00,000 − 9,50,000)', inr(cred)],
        ['Rent payable (60,000 − 50,000)', inr(rentdue)],
        ['Capital (profit for the year)', inr(prof)],
        ['Total', '6,50,000'],
    ], num=[1], total=True, title='Liabilities and capital on 31 March 2027')

    # ---------------- Illustration 3: money measurement and conservatism ----------------
    c3 = Checks()
    usd = c3.add('50000*84', 'Export sales: USD 50,000 @ ₹84')
    tot_sales = c3.add('4000000+4200000', 'Total sales in one currency')
    cost50 = c3.add('50*45000', 'Laptops at cost: 50 × ₹45,000')
    mkt_up = c3.add('50*52000', 'Laptops at market price ₹52,000')
    mkt_dn = c3.add('50*41000', 'Laptops at market price ₹41,000')
    loss = c3.add('2250000-2050000', 'Loss to be provided when market falls to ₹41,000')
    cons_tbl = table(['Situation on 31 March', 'Cost (₹)', 'Market value (₹)', 'Value in books (₹)', 'Reason'], [
        ['Market price ₹52,000 per laptop', inr(cost50), inr(mkt_up), inr(cost50), 'Expected gain ₹3,50,000 not recognised until sale (realisation, conservatism)'],
        ['Market price ₹41,000 per laptop', inr(cost50), inr(mkt_dn), inr(mkt_dn), f'Expected loss ₹{inr(loss)} provided now (conservatism)'],
    ], title='Valuing 50 unsold laptops')

    # ---------------- Dual aspect table (concept block) ----------------
    c4 = Checks()
    dual = table(['Transaction', 'Assets (₹)', 'Liabilities (₹)', 'Capital (₹)'], [
        ['Opening position', '5,00,000', '2,00,000', '3,00,000'],
        ['Machine bought for cash ₹60,000 (asset up, asset down)', '0', '0', '0'],
        ['Machine bought on credit ₹40,000 (asset up, liability up)', '40,000', '40,000', '0'],
        ['Bank loan repaid ₹30,000 (asset down, liability down)', '-30,000', '-30,000', '0'],
        ['New loan of ₹50,000 used to pay a creditor (liability up, liability down)', '0', '0', '0'],
        ['Closing position', '5,10,000', '2,10,000', '3,00,000'],
    ], num=[1, 2, 3], total=True, note='Every transaction has two aspects, so Assets = Liabilities + Capital holds after each one: 5,10,000 = 2,10,000 + 3,00,000.')
    c4.add('510000-210000', 'Capital = Assets − Liabilities at the end')

    concepts = [
        {'id': 'c1', 'title': 'Why accounts need agreed rules (GAAP)',
         'body': ['If five accountants each used their own ideas, the same books could show five different profits. To give accounting a common understanding and approach, a body of generally accepted accounting principles (GAAP) has developed — called concepts, conventions, postulates or principles. They are the ground rules within which financial statements are prepared, and with the Accounting Standards they form the theory base of accounting.',
                  'Globally, IFRS provide a common framework; countries may use their own GAAP. In India companies follow AS or Ind AS as applicable.',
                  'Accounting concepts are the basic assumptions on which statements are prepared — broad agreements, not laws of nature. Accounting principles are a body of doctrines that explain current practice and guide the choice of method where alternatives exist; they should be based on real assumptions, be simple and understandable, be followed consistently, be able to reflect future predictions and be informative to users. Accounting conventions arise from practice and usage over time, may be changed by accounting bodies and need not apply universally. The study material uses the three terms interchangeably.'],
         'analogy': 'Traffic rules: drive on the left, stop at red. Without shared rules every driver would follow his own logic and chaos would follow — so too with accounts.',
         'work': 'When a client asks why his "profit" in the accounts differs from the cash he has in the bank, the CA explains the agreed rules (accrual, matching, cost) behind the number. GAAP is the answer to "says who?".'},
        {'id': 'c2', 'title': 'Entity and money measurement — the two basic concepts',
         'body': ['Entity concept: the business is treated as separate from its owner. Only business transactions go into the business books. If the owner pays his child\'s school fee from his own pocket, nothing is recorded; if he takes the money from the business, it is recorded as drawings, which reduce his capital. Capital is the amount the business owes the owner; profit belongs to him. The concept applies to sole proprietors, firms and companies alike.',
                  'Money measurement concept: only transactions and events that can be expressed in money are recorded. Land, buildings, computers and machines are all shown in rupees, not in acres, floors or units. Foreign-currency amounts are converted into one currency before being added. Limitations: employees\' skill is not recorded, and money is treated as a stable yardstick — land bought years ago at a low price and similar land bought now at a high price are added at their old and new prices, ignoring changes in purchasing power.'],
         'analogy': 'Entity: a shop is a separate "person" with its own wallet; the owner\'s wallet is another. Money measurement: a common ruler — you cannot add 3 acres and 20 computers, but you can add their rupee values.',
         'work': 'In tax audits of proprietors, CAs regularly find personal expenses (house rent, family travel) booked as business expenses. Applying the entity concept — reclassifying them as drawings — changes the taxable profit.'},
        {'id': 'c3', 'title': 'Periodicity, accrual and matching — how profit for a period is measured',
         'body': ['Periodicity (definite accounting period): the life of a business is indefinite, so performance is measured for short, workable periods — usually a year (in India, 1 April to 31 March), sometimes 6, 9 or 15 months. It allows comparison between periods, uniform treatment and matching of revenue with expenses; it also gives meaning to "accrued" and "outstanding", which exist only with reference to a period.',
                  'Accrual (mercantile) concept: revenue and expenses are recognised when earned or incurred, not when cash is received or paid. Revenue is the gross inflow from sale of goods, rendering of services and use of the enterprise\'s resources by others (interest, royalty, dividend). Expense is a cost relating to the period\'s operations or revenue, or whose benefit does not go beyond the period. Profit = Revenue − Expenses. Timing gaps create balances: cash received before revenue → liability (advance from customer); after → trade receivable; cash paid before the expense → asset (advance/prepaid); after → liability (payable/outstanding).',
                  'Matching concept: once revenue of a period is recognised, the expenses incurred to earn it must be charged in the same period. Periodic profit = periodic revenue − matched expenses. Some costs match directly with sales (cost of goods sold, selling commission); others are matched with time (rent, salaries). Matching leads to adjustments for prepaid and outstanding expenses and accrued and unearned income.'],
         'analogy': 'A monthly electricity bill: you used the power in March even if you pay in April. March\'s cost belongs to March (accrual) and is set against what you earned in March (matching).',
         'work': 'At every year-end close, accountants pass accrual entries — salaries payable, interest accrued, expenses prepaid — precisely because of these concepts. Auditors test "cut-off" to make sure sales and costs land in the right year.'},
        {'id': 'c4', 'title': 'Going concern, cost, realisation — the valuation trio',
         'body': ['Going concern: statements are normally prepared on the assumption that the enterprise will continue to operate for the foreseeable future, with neither the intention nor the need to liquidate or materially curtail its operations. Fixed assets are therefore shown at cost less depreciation, not at what they would fetch in a forced sale. If liquidation is intended or necessary, a different basis is used and that basis is disclosed. Entities must assess this each time statements are prepared and tell stakeholders if continuation is in doubt.',
                  'Cost concept: assets are recorded at historical (acquisition) cost — the price paid plus costs to bring them into use. Preferred for objectivity: current cost is hard to find, realisable value is hypothetical until sale, and present value depends on an uncertain future. Weaknesses: in inflation, cost loses relevance; results of assets bought in different years are not comparable; and assets without a cost (human assets) are not recognised.',
                  'Realisation concept: a change in value is recorded only when it is realised (or its materialisation is certain). Accountants, being conservative, provide for probable losses but ignore probable gains until realised. Permanent increases in value are, however, increasingly recognised by revaluation, the gain going to a revaluation (capital) reserve.'],
         'analogy': 'Buying a house to live in: you think of what you paid (cost), you do not count the rise in its price as income until you actually sell it (realisation), and you do not value it at a distress-sale price because you are not moving out (going concern).',
         'work': 'Auditors must evaluate whether the going-concern assumption is appropriate — heavy losses, loan defaults or loss of a key customer can cast doubt. When it does, the audit report and the financial statements must say so.'},
        {'id': 'c5', 'title': 'Dual aspect — the accounting equation',
         'body': ['Every transaction has two aspects: it may increase one asset and decrease another, increase an asset and a liability, decrease an asset and a liability, or increase one liability and decrease another. This is the core of double entry.',
                  'Accounting equation: Equity (E) + Liabilities (L) = Assets (A), or E = A − L. Expanded: Fixed assets + Current assets = Capital + Long-term liabilities + Current liabilities; rearranged, Capital = Fixed assets + Working capital − Long-term liabilities (working capital being current assets less current liabilities).',
                  'Profit for a period can be found from two balance sheets: Closing equity − Opening equity (+ drawings − fresh capital, if any).'],
         'blocks': [dual],
         'analogy': 'A balance scale: anything put on the asset pan must be matched by an equal claim (liability or capital) on the other pan.',
         'work': 'When records are incomplete (small traders with only a cash book), CAs work out profit by comparing opening and closing capital using exactly this equation.'},
        {'id': 'c6', 'title': 'Conservatism, consistency and materiality',
         'body': ['Conservatism (prudence): do not anticipate income, but provide for all possible losses; where an asset has alternative values, choose the lower. The rule "cost or market price, whichever is lower" for current assets comes from it. It goes further than realisation — unrealised gains are ignored, but probable losses are recognised. It needs prudence, neutrality and faithful representation. Critics say it understates income and wealth; prudence does not permit hidden reserves or excessive provisions.',
                  'Consistency: once an accounting policy is chosen (e.g. depreciation method, inventory method), it is followed from period to period so that statements are comparable over time. Valuing inventory at cost in one year and at market price in another under "lower of cost or market" is not inconsistency — it is applying the same rule. Consistency is not rigidity: a policy may be changed only (a) to comply with an Accounting Standard, (b) to comply with law, or (c) when the new method gives a truer and fairer view.',
                  'Materiality: an item is material if its omission or misstatement could influence users\' decisions. Insignificant items may be treated in the simplest way — stationery bought is expensed in the year even if some is unused; a calculator or a book may be fully written off in the year of purchase. Materiality is a matter of judgement and depends on the amount, the nature of the item, the size of the business and who is deciding. It is an exception to the full-disclosure principle.'],
         'analogy': 'Conservatism: a careful traveller carries an umbrella when rain is possible but does not spend the bonus he only hopes to get. Consistency: measuring your height with the same tape every year. Materiality: nobody records the cost of a pen as a fixed asset.',
         'work': 'Audit firms set a "materiality threshold" (often a percentage of profit or revenue) to decide which errors must be corrected. Consistency is checked by comparing this year\'s accounting policies note with last year\'s.'},
        {'id': 'c7', 'title': 'Fundamental accounting assumptions',
         'body': ['Three assumptions are fundamental: going concern, consistency and accrual.',
                  'If nothing is said about them in the financial statements, users may assume they have been followed. If any one of them is not followed, that fact must be specifically disclosed.'],
         'analogy': 'Like the default settings of a phone: no one mentions them while they are on; if you switch one off, you must tell the user.',
         'work': 'A company being wound up prepares statements on a realisable (break-up) basis, not going concern — and the notes must say so clearly. An auditor would qualify or modify the report if this disclosure were missing.'},
        {'id': 'c8', 'title': 'Financial statements and their qualitative characteristics',
         'body': ['Financial statements — balance sheet, profit and loss account, cash flow statement with notes — are the structured way an enterprise communicates its financial position and performance to users. Qualitative characteristics are the attributes that make that information useful.',
                  'Understandability (users with reasonable knowledge and diligence should be able to understand it; complex but relevant items are not left out); Relevance (it influences decisions by helping evaluate past, present or future events — predictive and confirmatory roles; showing unusual items separately improves prediction); Reliability (free from material error and bias, faithfully representing what it claims — a highly uncertain damages claim may be disclosed rather than recognised); Comparability (over time and across enterprises; users must be told the policies used and changes in them; corresponding previous-period figures are shown; comparability is not mere uniformity and must not block improvements). These four are the principal characteristics.',
                  'Also: Materiality (a threshold or cut-off rather than a primary characteristic); Faithful representation (some items, like internally generated goodwill, cannot be measured reliably); Substance over form (record economic reality — e.g. property whose rights and benefits have passed is treated as transferred though registration is pending); Neutrality (no selective presentation to reach a predetermined result); Prudence (caution in estimates so that assets and income are not overstated and liabilities and expenses not understated — without hidden reserves); Full, fair and adequate disclosure (nothing material omitted, true and fair treatment, enough detail — hence notes and schedules); Completeness (within the limits of materiality and cost — an omission can make information misleading).'],
         'analogy': 'A good weather forecast: easy to understand, about your city (relevant), usually right (reliable), in the same format every day (comparable), and honest about uncertainty (prudence, disclosure).',
         'work': 'Notes to accounts, the accounting policies note and comparative figures in every annual report exist because of these characteristics. When drafting accounts, CAs ask: is this disclosure material, complete and neutral?'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Profit from two balance sheets (accounting equation)', 'difficulty': 'moderate', 'minutes': 12,
         'q': 'From the following information of Arora Traders, find the capital at the beginning and end of the year, the profit for 2026-27 and prepare the balance sheet as at 31 March 2027. The proprietor withdrew ₹12,000 during the year and introduced no fresh capital. On 31 March 2026: fixed assets ₹2,40,000; trade receivables ₹90,000; inventory ₹55,000; cash and bank ₹15,000; 10% term loan ₹1,50,000; trade payables ₹60,000. On 31 March 2027: fixed assets ₹2,25,000; trade receivables ₹1,04,000; inventory ₹68,000; cash and bank ₹21,000; 10% term loan ₹1,50,000; trade payables ₹72,000.',
         'solution': [eq_tbl, li_tbl,
                      wn('Capital (Equity = Assets − Liabilities)', f'Opening: {inr(a0)} − {inr(l0)} = ₹{inr(e0)}. Closing: {inr(a1)} − {inr(l1)} = ₹{inr(e1)}.'),
                      wn('Profit', f'Closing capital {inr(e1)} − Opening capital {inr(e0)} = 6,000. Drawings reduced capital by 12,000, so profit = 6,000 + 12,000 = ₹{inr(pr)}.'),
                      bs1],
         'checks': c1},
        {'id': 'i2', 'title': 'Cash basis versus accrual and matching', 'difficulty': 'moderate', 'minutes': 12,
         'q': 'Kabir Footwear started on 1 April 2026. During 2026-27 it bought 6,000 pairs at ₹200 each and sold 4,500 pairs at ₹300 each. It paid suppliers ₹9,50,000 and collected ₹11,00,000 from customers. Shop rent is ₹5,000 a month; rent for 10 months was paid. Compute the result under (a) the cash basis, (b) accrual without matching, and (c) accrual with matching, and show the assets and liabilities on 31 March 2027 under (c).',
         'solution': [cmp_tbl,
                      wn('Correct profit', f'Revenue = 4,500 × 300 = ₹{inr(rev)}. Matched cost of goods sold = 4,500 × 200 = ₹{inr(cogs)} (not the full purchases of ₹{inr(pur)}). Rent for the period = 12 × 5,000 = ₹{inr(rent)} (not ₹50,000 paid). Profit = {inr(rev)} − {inr(cogs)} − {inr(rent)} = ₹{inr(prof)}.'),
                      pos_tbl, pos2_tbl,
                      note('Periodicity fixed the year; accrual measured revenue and rent of that year; matching charged only the cost of the pairs actually sold. The unsold 1,500 pairs are an asset carried forward.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Money measurement and conservatism in figures', 'difficulty': 'core', 'minutes': 8,
         'q': '(a) Zenith Exports sold goods worth ₹40,00,000 in India and USD 50,000 abroad when USD 1 = ₹84. What are its total sales? (b) It holds 50 unsold laptops bought at ₹45,000 each. At what amount should they be shown if the market price on 31 March is (i) ₹52,000 each, (ii) ₹41,000 each?',
         'solution': [wn('(a) Money measurement', f'"₹40 lakh plus USD 50,000" cannot be added. Converting into rupees: 50,000 × 84 = ₹{inr(usd)}. Total sales = 40,00,000 + {inr(usd)} = ₹{inr(tot_sales)}.'),
                      cons_tbl,
                      note('This is the lower of cost and market value rule — a direct result of conservatism.')],
         'checks': c3},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Personal expenses in a proprietor\'s books', 'role': 'Article assistant on a tax audit of a retail store',
         'situation': 'While vouching expenses you find: the owner\'s family holiday ₹85,000 booked as "Travelling", his daughter\'s college fee ₹1,20,000 as "Staff Welfare", and a ₹600 desk calculator debited to "Office Expenses".',
         'steps': ['Apply the entity concept: the holiday and the college fee are personal — reclassify both as Drawings (they reduce capital, not profit).',
                   'Recompute the profit: expenses fall by ₹2,05,000, so profit rises by that amount.',
                   'Apply materiality to the calculator: although it lasts more than a year, ₹600 is immaterial; expensing it is acceptable.',
                   'Record the adjustments in your working papers and discuss them with the client and your principal.'],
         'takeaway': 'Entity and materiality are applied every day in audit — one changes profit, the other saves pointless work.',
         'think': 'If the owner had paid the college fee from his personal bank account, what entry would the business pass?',
         'answer': 'None. Under the entity concept, a payment from the owner\'s own pocket for a personal purpose is not a business transaction.'},
        {'id': 'j2', 'title': 'A going-concern warning', 'role': 'Audit senior reviewing a small manufacturing company',
         'situation': 'The company has made losses for three years, its bank has recalled a loan and its main customer has left. Management has prepared statements on the going-concern basis as usual.',
         'steps': ['List the indicators that cast doubt on continuation: recurring losses, loan recall, loss of a key customer.',
                   'Ask management for its plans (new funding, new customers) and test whether they are realistic.',
                   'If doubt remains, ensure the uncertainty is disclosed; if the company clearly cannot continue, statements must be prepared on a different (realisable) basis and that basis disclosed.',
                   'Consider the effect on the audit report.'],
         'takeaway': 'Going concern is assumed, not guaranteed. When the assumption fails, assets move from cost-based values to what they can realise, and users must be told.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'The concept that keeps the owner\'s personal affairs out of the business books is the:', 'options': ['Business entity concept', 'Matching concept', 'Money measurement concept', 'Going concern concept'], 'answer': 0, 'explain': 'The entity concept treats the business as separate from its owner.', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'The three fundamental accounting assumptions are:', 'options': ['Going concern, consistency and accrual', 'Entity, money measurement and cost', 'Prudence, materiality and consistency', 'Going concern, matching and realisation'], 'answer': 0, 'explain': 'Going concern, consistency and accrual are the fundamental accounting assumptions; their non-observance must be disclosed.', 'concept': 'c7', 'difficulty': 'core'},
        {'id': 'm3', 'q': 'Valuing inventory at cost or market price, whichever is lower, follows from:', 'options': ['Conservatism', 'Consistency', 'Dual aspect', 'Periodicity'], 'answer': 0, 'explain': 'Conservatism: provide for possible losses, do not anticipate gains — hence the lower of the two values.', 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'A firm has assets of ₹8,40,000 and outside liabilities of ₹3,15,000. Its capital is:', 'options': ['₹5,25,000', '₹11,55,000', '₹3,15,000', '₹8,40,000'], 'answer': 0, 'check': '840000-315000', 'explain': 'Capital = Assets − Liabilities = 8,40,000 − 3,15,000 = ₹5,25,000.', 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm5', 'q': 'Opening capital ₹2,50,000; closing capital ₹3,10,000; drawings during the year ₹30,000; fresh capital introduced ₹20,000. Profit for the year is:', 'options': ['₹70,000', '₹60,000', '₹90,000', '₹50,000'], 'answer': 0, 'check': '310000-250000+30000-20000', 'explain': 'Profit = Closing − Opening + Drawings − Fresh capital = 3,10,000 − 2,50,000 + 30,000 − 20,000 = ₹70,000.', 'concept': 'c5', 'difficulty': 'moderate'},
        {'id': 'm6', 'q': 'Goods costing ₹6,00,000 were bought and 70% of them were sold during the year. Under the matching concept, the cost to be charged against the year\'s sales is:', 'options': ['₹4,20,000', '₹6,00,000', '₹1,80,000', '₹5,00,000'], 'answer': 0, 'check': '600000*70/100', 'explain': 'Only the cost of goods actually sold (70% × 6,00,000 = ₹4,20,000) is matched with revenue; the rest is closing inventory.', 'concept': 'c3', 'difficulty': 'moderate'},
        {'id': 'm7', 'q': 'Rent of ₹9,000 a month; rent for 10 months paid during the year. Rent expense for the year under the accrual concept is:', 'options': ['₹1,08,000', '₹90,000', '₹18,000', '₹99,000'], 'answer': 0, 'check': '9000*12', 'explain': 'Expense is recognised when incurred — 12 months × 9,000 = ₹1,08,000; ₹18,000 is outstanding.', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm8', 'q': 'A machine bought for ₹5,00,000 now has a market value of ₹7,00,000. The business, which plans to continue using it, keeps it in the books at ₹5,00,000. Which concepts justify this?', 'options': ['Cost, going concern and realisation', 'Money measurement and entity', 'Matching and periodicity', 'Materiality and consistency'], 'answer': 0, 'explain': 'Historical cost is used; the asset is held for use, not sale (going concern); and the gain is not realised.', 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm9', 'q': 'A calculator costing ₹500, which will last three years, is written off fully in the year of purchase. This is justified by:', 'options': ['Materiality', 'Conservatism', 'Consistency', 'Going concern'], 'answer': 0, 'explain': 'The amount is too small to influence users; materiality allows the simple treatment.', 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm10', 'q': 'Which of these is NOT a valid reason for changing an accounting policy?', 'options': ['To show a higher profit this year', 'To comply with an Accounting Standard', 'To comply with a law', 'To give a more true and fair view'], 'answer': 0, 'explain': 'A policy may be changed only for a standard, a statute or a more appropriate (true and fair) presentation — never to manage profit.', 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm11', 'q': 'The four principal qualitative characteristics of financial statements are:', 'options': ['Understandability, relevance, reliability and comparability', 'Prudence, neutrality, materiality and completeness', 'Accrual, consistency, going concern and prudence', 'Relevance, timeliness, cost and uniformity'], 'answer': 0, 'explain': 'Understandability, relevance, reliability and comparability are the four principal characteristics.', 'concept': 'c8', 'difficulty': 'core'},
        {'id': 'm12', 'q': 'A firm uses a machine taken on a long-term arrangement in which it bears all the risks and enjoys all the benefits, although legal title remains with the supplier. Showing it as the firm\'s asset reflects:', 'options': ['Substance over form', 'Money measurement', 'Realisation', 'Entity concept'], 'answer': 0, 'explain': 'Economic reality (risks and benefits) prevails over the legal form of the arrangement.', 'concept': 'c8', 'difficulty': 'hard'},
        {'id': 'm13', 'q': 'Sales at home ₹30,00,000 and abroad EUR 20,000 when EUR 1 = ₹90. Total sales to be recorded are:', 'options': ['₹48,00,000', '₹30,20,000', '₹18,00,000', '₹30,00,000'], 'answer': 0, 'check': '3000000+20000*90', 'explain': 'Money measurement needs one currency: 20,000 × 90 = ₹18,00,000; total ₹48,00,000.', 'concept': 'c2', 'difficulty': 'core'},
    ]

    # ---------------- Questions ----------------
    q2c = Checks()
    qa0 = q2c.add('180000+60000+45000+10000', 'Assets 1 April 2026')
    ql0 = q2c.add('100000+40000', 'Liabilities 1 April 2026')
    qe0 = q2c.add('295000-140000', 'Opening capital')
    qa1 = q2c.add('170000+75000+62000+18000', 'Assets 31 March 2027')
    ql1 = q2c.add('100000+35000', 'Liabilities 31 March 2027')
    qe1 = q2c.add('325000-135000', 'Closing capital')
    qp = q2c.add('190000-155000+24000-10000', 'Profit = closing − opening + drawings − fresh capital')
    q2_tbl = table(['Particulars', '1 Apr 2026 (₹)', '31 Mar 2027 (₹)'], [
        ['Machinery', '1,80,000', '1,70,000'],
        ['Trade receivables', '60,000', '75,000'],
        ['Inventory', '45,000', '62,000'],
        ['Cash', '10,000', '18,000'],
        ['Total assets', inr(qa0), inr(qa1)],
    ], num=[1, 2], total=True)
    q2_tbl2 = table(['Particulars', '1 Apr 2026 (₹)', '31 Mar 2027 (₹)'], [
        ['Loan from bank', '1,00,000', '1,00,000'],
        ['Trade payables', '40,000', '35,000'],
        ['Total liabilities', inr(ql0), inr(ql1)],
    ], num=[1, 2], total=True)

    q3c = Checks()
    q3_rev = q3c.add('8000*250', 'Revenue 8,000 units @ ₹250')
    q3_cogs = q3c.add('8000*160', 'Cost of 8,000 units sold @ ₹160')
    q3_sal = q3c.add('15000*12', 'Salary for 12 months')
    q3_ins = q3c.add('24000*9/12', 'Insurance for 9 months of a 12-month policy paid ₹24,000 on 1 July')
    q3_prof = q3c.add('2000000-1280000-180000-18000', 'Profit under accrual and matching')
    q3_cashp = q3c.add('1750000-1500000-165000-24000', 'Cash-basis surplus')
    q3_tbl = table(['Particulars', '₹'], [
        ['Revenue (8,000 × 250)', inr(q3_rev)],
        ['Less: Cost of goods sold (8,000 × 160)', '-' + inr(q3_cogs)],
        ['Less: Salary (12 × 15,000)', '-' + inr(q3_sal)],
        ['Less: Insurance (24,000 × 9/12)', '-' + inr(q3_ins)],
        ['Profit for the year', inr(q3_prof)],
    ], num=[1], total=True, title='Profit under accrual and matching')

    questions = [
        {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'core', 'pad': 'text',
         'q': 'What are the fundamental accounting assumptions? Explain each briefly and state what happens if any of them is not followed.',
         'model': [ul(['Going concern — the enterprise is assumed to continue operating for the foreseeable future, with no intention or need to liquidate or materially curtail its operations. Assets are therefore carried at cost-based amounts, not break-up values. If liquidation is intended or required, another basis is used and disclosed.',
                       'Consistency — the same accounting policies are applied from one period to the next so that the statements are comparable over time. A policy is changed only to comply with a standard or a statute, or to give a more appropriate presentation, and the change and its effect are disclosed.',
                       'Accrual — revenues and costs are recognised as they are earned or incurred, not when cash is received or paid, and recorded in the period to which they relate.']),
                   p('These assumptions are taken for granted: if the statements are silent, users may assume they have been followed. If any of them is not followed, the fact must be specifically disclosed.')],
         'scheme': [
             {'id': 's1', 'pt': 'Names the three assumptions correctly', 'm': 1, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Going concern explained (foreseeable future; no intention/need to liquidate)', 'm': 1.5, 'skill': 'concept'},
             {'id': 's3', 'pt': 'Consistency explained (same policies; comparability; change only for valid reasons)', 'm': 1.5, 'skill': 'concept'},
             {'id': 's4', 'pt': 'Accrual explained (when earned/incurred, not when cash moves)', 'm': 1, 'skill': 'concept'},
             {'id': 's5', 'pt': 'Not disclosed if followed; must be disclosed if not followed', 'm': 1, 'skill': 'application'},
         ],
         'remarks': ['Many candidates list entity or money measurement as fundamental assumptions — that loses the first mark straight away.', 'The disclosure rule is often missed although it is a full mark.'],
         'mistakes': ['Listing "prudence, substance over form, materiality" — those guide the selection of accounting policies, they are not the fundamental assumptions.', 'Explaining accrual as "recording only cash transactions".'],
         'tips': ['Write the three names as headings, two lines under each.', 'End with the disclosure rule in a separate sentence.']},
        {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'Meher Enterprises gives you the following. 1 April 2026: machinery ₹1,80,000; trade receivables ₹60,000; inventory ₹45,000; cash ₹10,000; bank loan ₹1,00,000; trade payables ₹40,000. 31 March 2027: machinery ₹1,70,000; trade receivables ₹75,000; inventory ₹62,000; cash ₹18,000; bank loan ₹1,00,000; trade payables ₹35,000. During the year the proprietor withdrew ₹24,000 and brought in additional capital of ₹10,000. Using the accounting equation, find the opening and closing capital and the profit for the year.',
         'model': [q2_tbl, q2_tbl2,
                   wn('Capital', f'Opening capital = {inr(qa0)} − {inr(ql0)} = ₹{inr(qe0)}. Closing capital = {inr(qa1)} − {inr(ql1)} = ₹{inr(qe1)}.'),
                   wn('Profit', f'Profit = Closing capital − Opening capital + Drawings − Additional capital = {inr(qe1)} − {inr(qe0)} + 24,000 − 10,000 = ₹{inr(qp)}.')],
         'scheme': [
             {'id': 's1', 'pt': f'Total assets ₹{inr(qa0)} and ₹{inr(qa1)}', 'm': 1, 'skill': 'computation'},
             {'id': 's2', 'pt': f'Total liabilities ₹{inr(ql0)} and ₹{inr(ql1)}', 'm': 1, 'skill': 'computation'},
             {'id': 's3', 'pt': f'Opening capital ₹{inr(qe0)} and closing capital ₹{inr(qe1)} using E = A − L', 'm': 1, 'skill': 'computation'},
             {'id': 's4', 'pt': 'Drawings added back and additional capital deducted', 'm': 1, 'skill': 'concept'},
             {'id': 's5', 'pt': f'Profit ₹{inr(qp)} with working shown', 'm': 1, 'skill': 'presentation'},
         ],
         'remarks': ['Candidates who forget the additional capital overstate profit by ₹10,000 and lose two marks.', 'Show the equation for each date — step marks are given even if the final figure is wrong.'],
         'mistakes': ['Deducting drawings instead of adding them back.', 'Treating the bank loan as part of capital.'],
         'tips': ['Write "E = A − L" before each computation.', 'Present assets and liabilities in two short tables side by side for both dates.']},
        {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'Devika Traders (year ending 31 March 2027) bought 10,000 units at ₹160 each and sold 8,000 units at ₹250 each. It received ₹17,50,000 from customers and paid ₹15,00,000 to suppliers. Salary is ₹15,000 a month; ₹1,65,000 was paid. A one-year insurance premium of ₹24,000 was paid on 1 July 2026. Compute (a) the surplus on cash basis and (b) the profit applying accrual and matching concepts. Explain the difference briefly.',
         'model': [wn('(a) Cash basis', f'Receipts 17,50,000 − payments (15,00,000 + 1,65,000 + 24,000) = ₹{inr(q3_cashp)}.'),
                   q3_tbl,
                   p('The difference arises because accrual recognises the full sales of ₹20,00,000 (not just cash collected) and the full salary for 12 months; matching charges only the cost of the 8,000 units sold (the 2,000 unsold units are inventory) and only 9 months\' insurance (₹6,000 is prepaid for next year).')],
         'scheme': [
             {'id': 's1', 'pt': f'Cash-basis surplus ₹{inr(q3_cashp)}', 'm': 1, 'skill': 'computation'},
             {'id': 's2', 'pt': f'Revenue ₹{inr(q3_rev)} and cost of goods sold ₹{inr(q3_cogs)}', 'm': 1.5, 'skill': 'computation'},
             {'id': 's3', 'pt': f'Salary ₹{inr(q3_sal)} and insurance ₹{inr(q3_ins)}', 'm': 1, 'skill': 'computation'},
             {'id': 's4', 'pt': f'Profit ₹{inr(q3_prof)}', 'm': 0.5, 'skill': 'computation'},
             {'id': 's5', 'pt': 'Explanation linking the difference to accrual and matching (unsold stock, outstanding salary, prepaid insurance)', 'm': 1, 'skill': 'concept'},
         ],
         'remarks': ['The commonest error is deducting all purchases of ₹16,00,000 instead of the cost of units sold.', 'Several candidates charge the full insurance premium; only 9 of the 12 months fall in this year.'],
         'mistakes': ['Taking cash received as revenue under the accrual basis.', 'Charging only the salary actually paid.'],
         'tips': ['Show each figure with its formula (e.g. 8,000 × 160).', 'A two-line explanation of the difference earns the concept mark.']},
        {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'Explain the concepts of conservatism and consistency with an example of each. Does valuing inventory at cost in one year and at market price in the next violate consistency?',
         'model': [p('Conservatism (prudence): the accountant should not anticipate income but should provide for all possible losses; where alternative values exist, the lower value is chosen. Example: goods costing ₹2,00,000 with a market value of ₹1,70,000 are shown at ₹1,70,000, but if the market value were ₹2,40,000 they would still be shown at ₹2,00,000.'),
                   p('Consistency: accounting policies once adopted are applied from period to period so that results are comparable. Example: a firm using the straight-line method of depreciation continues to use it every year unless a valid reason for change exists (a standard, a law, or a more appropriate presentation).'),
                   p('No. Under the rule "cost or market price, whichever is lower", the same rule is applied every year; it simply produces cost in one year and market price in another. That is application of the policy, not inconsistency.')],
         'scheme': [
             {'id': 's1', 'pt': 'Conservatism explained with example', 'm': 1.5, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Consistency explained with example and valid reasons for change', 'm': 1.5, 'skill': 'concept'},
             {'id': 's3', 'pt': 'Correct conclusion: no violation — same rule applied', 'm': 1, 'skill': 'conclusion'},
         ],
         'remarks': ['The last part is a classic trap; candidates who say "yes, it is inconsistent" lose the conclusion mark.'],
         'mistakes': ['Saying consistency means a policy can never be changed.', 'Saying conservatism allows recording expected profits.'],
         'tips': ['Give a small numerical example for conservatism — it shows understanding quickly.']},
    ]

    viva = [
        V('v1', 'Explain the business entity concept with an example.',
          'Under the entity concept the business is treated as separate from its owner, so only business transactions are recorded in the business books. For example, if the owner takes cash from the business to pay his son\'s school fee, it is recorded as drawings and reduces his capital; if he pays from his own pocket, nothing is recorded in the business books.',
          [P('p1', 'Business is separate / distinct from its owner', 5, 'separate|distinct|different from|differ from|are different|is different|apart from owner|own identity|separate person'),
           P('p2', 'Only business transactions are recorded; personal ones are not', 2, 'business transaction|personal|private|own pocket|household', min=1),
           P('p3', 'Owner\'s withdrawals are drawings; capital is owed to the owner', 3, 'drawing|capital|owe owner|liable owner|withdraw', min=1)], 'c2'),
        V('v2', 'What is the accrual concept, and how does it differ from the cash basis?',
          'Under the accrual concept revenue and expenses are recognised when they are earned or incurred, not when cash is received or paid, and they are shown in the period to which they relate. Under the cash basis, only actual receipts and payments are recorded, so outstanding and prepaid items are ignored.',
          [P('p1', 'Recognised when earned or incurred', 4, 'earn|incur|occur|when they happen|when it happen|relate'),
           P('p2', 'Not when cash is received or paid', 4, ALT('{n} when cash', '{n} cash receiv', '{n} cash paid', '{n} receiv paid', '{n} on receipt', '{n} receipt payment', '{n} actual cash', '{n} depend cash', '{n} matter when cash', 'irrespective cash', 'regardless cash', 'whether cash', 'even if cash', 'even cash', n=('not', 'no', 'never', 'rather than', 'instead of', 'not only', 'doesn t', 'does not'))),
           P('p3', 'Cash basis records only actual receipts and payments', 2, 'cash basis|cash system|cash accounting', 'actual|only|receipt|payment', min=2)], 'c3'),
        V('v3', 'What is the going concern concept and why is it important for valuing assets?',
          'Going concern means the enterprise is assumed to continue in operation for the foreseeable future, with no intention or need to liquidate or materially curtail its operations. Because of this, fixed assets are shown at cost less depreciation and not at their forced sale or realisable value. If liquidation is intended, a different basis is used and disclosed.',
          [P('p1', 'Business assumed to continue for the foreseeable future', 4, 'continu|carry on|keep running|keep operat|indefinite|foreseeable|long time|not close'),
           P('p2', 'No intention or need to liquidate / curtail operations', 2, ALT('{n} liquidat', '{n} intention liquidat', '{n} need liquidat', '{n} close', '{n} wind', '{n} shut', '{n} curtail', n=('no', 'not', 'neither', 'nor', 'without', 'never'))),
           P('p3', 'Assets shown at cost, not realisable/forced-sale value', 4, 'cost|book value|historical|depreciat', 'not realisable|not sale|not forced|not market|not break|not resale|not selling|rather than sale|instead of sale|not what fetch|not liquidat|not current|not distress', min=1)], 'c4'),
        V('v4', 'State the conservatism concept with an example.',
          'Conservatism means the accountant should not anticipate any income or profit but should provide for all possible losses. Where there are alternative values, the lower one is chosen. For example, inventory is valued at cost or market price, whichever is lower.',
          [P('p1', 'Do not anticipate profits / gains', 4, ALT('{n} anticipat', '{n} expect profit', '{n} record future profit', '{n} recognis unrealis', '{n} count unrealis', '{n} unrealis gain', '{n} record unrealis', '{n} recognis profit', '{n} book profit', 'ignor unrealis', 'ignor expect', 'ignor future profit', 'ignor profit', 'profit not record', 'profit not recognis', 'profit not anticipat', 'profit not count', 'profit not book', 'profit ignor', 'gain not record', 'gain not recognis', 'gain ignor', 'income not anticipat', 'income not record', n=('not', 'no', 'never', 'don t', 'do not', 'shouldn t'))),
           P('p2', 'Provide for all possible losses', 4, 'provide loss|provide all loss|provide all possible loss|provide for possible|loss provid|loss recognis|recognis loss|record loss|loss record|account loss|losses provid|losses recognis|losses are provided|all possible loss|all losses'),
           P('p3', 'Choose the lower value — cost or market price whichever is lower', 2, 'lower|lesser|lowest|less of')], 'c6'),
        V('v5', 'Which are the fundamental accounting assumptions, and when must they be disclosed?',
          'The fundamental accounting assumptions are going concern, consistency and accrual. If they are followed, no disclosure is needed because they are assumed. If any of them is not followed, that fact must be disclosed in the financial statements.',
          [P('p1', 'Going concern', 2, 'going concern'),
           P('p2', 'Consistency', 2, 'consisten'),
           P('p3', 'Accrual', 2, 'accrual|accru|mercantile'),
           P('p4', 'Disclosure required only if not followed', 4, 'disclos|mention|state|report|reveal|tell|not follow disclos|not follow mention|not follow state|not follow report|not compl disclos|not adher disclos',
             ALT('{n} {f}', n=('not', 'never'), f=('follow', 'adher', 'compl', 'observ', 'appli', 'used')) + '|' + ALT('{v}', v=('depart', 'deviat', 'violat', 'non complian', 'non observ', 'ignor', 'break')))], 'c7'),
        V('v6', 'Explain the matching concept.',
          'The matching concept says that when revenue of a period is recognised, all the expenses incurred to earn that revenue must be charged in the same period. So only the cost of goods sold, not all purchases, is matched with sales, and adjustments are made for outstanding and prepaid expenses. Periodic profit equals periodic revenue minus matched expenses.',
          [P('p1', 'Expenses matched with the revenue they helped earn', 5, 'expens|cost', 'revenue|income|sale'),
           P('p2', 'In the same accounting period', 3, 'same period|same year|same accounting period|that period|that year|period|same time'),
           P('p3', 'Leads to cost of goods sold / outstanding and prepaid adjustments', 2, 'cost of goods sold|goods sold|outstanding|prepaid|accrued|unearned|adjust|closing stock|closing inventory|unsold', min=1)], 'c3'),
        V('v7', 'Does the consistency concept mean that an accounting policy can never be changed?',
          'No. Consistency means the same policies are followed from year to year for comparability, but it does not mean rigidity. A policy can be changed to comply with an Accounting Standard, to comply with a law, or when the new policy gives a more true and fair presentation.',
          [P('p1', 'No — consistency is not rigidity; change is allowed', 3, 'not rigid|no rigid|not inflexib|can be changed|can change|may be changed|can be change|allowed change|change allowed|change is allowed|can still|does not mean never|not mean never|not never|no it can|not absolute|isn t rigid|flexib|permitted|not forever', min=1),
           P('p2', 'Purpose: same policies year to year for comparability', 2, 'same|compar|year to year|period to period|every year|consistently', min=1),
           P('p3', 'Change for Accounting Standard / law / more true and fair view', 5, 'standard|accounting standard', 'law|statute|legal|act|regulat', 'true and fair|true fair|better present|more appropriate|appropriate present|fairer|better picture|truer|improv', min=2)], 'c6'),
    ]

    c = Checks()
    k_cogs = c.add('900*1200', 'Cost of 900 jackets sold @ ₹1,200')
    k_close = c.add('(1200-900)*1200', 'Closing inventory 300 jackets @ ₹1,200')
    k_nrv = c.add('300*1000', 'Closing inventory at market ₹1,000')
    k_rev = c.add('900*2000', 'Revenue 900 jackets @ ₹2,000')
    k_prof = c.add('1800000-1080000-60000-(360000-300000)', 'Profit after matched cost, expenses and inventory write-down')
    cases = [{
        'id': 'k1', 'title': 'Winter Wear Co. — applying the concepts at year end', 'difficulty': 'hard',
        'case': ('Winter Wear Co. bought 1,200 jackets at ₹1,200 each during 2026-27 and sold 900 of them at ₹2,000 each, all on credit; customers have paid ₹15,00,000 so far. Shop expenses for the year are ₹60,000. '
                 'On 31 March 2027, a rival\'s clearance sale has pushed the market price of the remaining jackets down to ₹1,000 each. The owner also paid ₹40,000 from the shop\'s cash for a family function. He believes the shop\'s brand name is worth ₹5,00,000 and wants it shown as an asset.'),
        'mcqs': [
            M('k1a', 'What cost of jackets should be matched against the year\'s sales?', [R(k_cogs), '₹14,40,000', '₹15,00,000', '₹9,00,000'], 0,
              f'Matching: only the 900 jackets sold — 900 × 1,200 = {R(k_cogs)}. The 300 unsold jackets are inventory.', 'moderate', '900*1200'),
            M('k1b', 'At what amount should the closing inventory be shown?', [R(k_nrv), R(k_close), '₹6,00,000', '₹3,30,000'], 0,
              f'Conservatism (lower of cost and market): cost {R(k_close)}, market {R(k_nrv)}; the lower, {R(k_nrv)}, is taken.', 'hard', '300*1000'),
            M('k1c', 'What is the profit for the year (ignoring the family function and the brand)?', [R(k_prof), '₹6,60,000', '₹3,60,000', '₹1,80,000'], 0,
              f'Revenue {R(k_rev)} (accrual — not the ₹15,00,000 collected) − cost of goods sold {R(k_cogs)} − expenses ₹60,000 − inventory write-down ₹60,000 = {R(k_prof)}.', 'hard', '1800000-1080000-60000-60000'),
            M('k1d', 'How should the ₹40,000 for the family function and the "brand worth ₹5,00,000" be treated?', ['₹40,000 as drawings; brand not recorded', '₹40,000 as an expense; brand shown as an asset', '₹40,000 ignored; brand shown as goodwill', '₹40,000 as drawings; brand shown at ₹5,00,000'], 0,
              'Entity concept: a personal payment from business cash is drawings. Cost and realisation concepts: a self-estimated brand value with no cost and no transaction is not recorded.', 'moderate'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch01', 'n': 2,
        'title': 'Accounting Concepts, Principles and Conventions',
        'outcomes': [
            'Explain why GAAP is needed and distinguish accounting concepts, principles and conventions.',
            'Explain and apply the entity, money measurement, periodicity, accrual, matching, going concern, cost, realisation, dual aspect, conservatism, consistency and materiality concepts.',
            'Use the accounting equation to find capital and profit from balance sheet data.',
            'State the three fundamental accounting assumptions and the disclosure rule.',
            'Describe the qualitative characteristics that make financial statements useful.',
        ],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 50, 'practice': 45}, 'prereq': ['fnd-p1-ch01-u01'],
                 'exam_tip': 'Expect short theory (explain a concept with an example), "which concept is applied?" MCQs and small accounting-equation or accrual computations. Always quote the concept by name and give a one-line example.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['GAAP = concepts (assumptions), principles (doctrines guiding choice) and conventions (practice) — used interchangeably.',
                        'Entity and money measurement are the base concepts; periodicity, accrual and matching measure periodic profit; going concern, cost and realisation give valuation; dual aspect gives A = L + E.',
                        'Conservatism: anticipate no profit, provide for all losses (lower of cost or market). Consistency: same policies each year; change only for a standard, a law or a truer view. Materiality: ignore the trivial.',
                        'Fundamental accounting assumptions: going concern, consistency, accrual — disclose only if not followed.',
                        'Qualitative characteristics: understandability, relevance, reliability, comparability (principal four) + prudence, neutrality, faithful representation, substance over form, materiality, completeness, and full, fair and adequate disclosure.'],
            'remember': ['Profit = Closing capital − Opening capital + Drawings − Fresh capital.', 'Cash before revenue → liability; cash after revenue → receivable; cash before expense → prepaid asset; cash after expense → outstanding liability.', 'Lower of cost or market in different years is not inconsistency.'],
            'traps': ['Do not charge all purchases against sales — only the cost of goods sold.', 'Prudence never allows secret reserves or excessive provisions.', 'Materiality is a threshold, not a primary qualitative characteristic.'],
        },
        'quickref': [
            {'k': 'Accounting equation', 'v': 'Equity + Liabilities = Assets; Equity = Fixed assets + Working capital − Long-term liabilities'},
            {'k': 'Profit from capital', 'v': 'Closing capital − Opening capital + Drawings − Additional capital'},
            {'k': 'Periodic profit', 'v': 'Periodic revenue − Matched expenses'},
            {'k': 'Fundamental assumptions', 'v': 'Going concern, Consistency, Accrual'},
            {'k': 'Valuation trio', 'v': 'Going concern + Cost + Realisation'},
            {'k': 'Policy change allowed', 'v': 'Accounting Standard · Statute · More true and fair presentation'},
            {'k': 'Principal qualitative characteristics', 'v': 'Understandability, Relevance, Reliability, Comparability'},
        ],
        'viva': viva, 'cases': cases,
    }
