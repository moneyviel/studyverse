"""CA Foundation · Paper 1 Accounting · Chapter 1 Theoretical Framework · Unit 3 Capital and Revenue Expenditures and Receipts.
Original explanations, figures and questions (structure and scope follow the ICAI study material)."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p1-ch01-u03'


def build():
    # ---------------- Illustration 1: setting up a restaurant ----------------
    c1 = Checks()
    oven = c1.add('160000+25000+5000', 'Oven: price + overhaul to make it usable + installation wages')
    ins_exp = c1.add('12000*3/12', 'Insurance for Jan–Mar (3 months of 12)')
    ins_pre = c1.add('12000*9/12', 'Insurance prepaid for Apr–Dec')
    capt = c1.add('190000+30000+18000+600000', 'Total capital expenditure')
    revt = c1.add('2000+3000+84000', 'Revenue expenditure charged to 2026-27')
    pre = c1.add('6000+9000', 'Prepaid expenses (asset) on 31 March 2027')
    c1.add('838000+89000+15000', 'Total spent = capital + revenue + prepaid')
    c1.add('160000+25000+5000+30000+2000+6000+12000+18000+600000+84000', 'Total of all payments')
    r_tbl = table(['Item', 'Amount (₹)', 'Capital (₹)', 'Revenue — this year (₹)', 'Prepaid (₹)'], [
        ['Second-hand oven', '1,60,000', '1,60,000', '0', '0'],
        ['Overhaul of the oven before first use', '25,000', '25,000', '0', '0'],
        ['Wages of own staff for installing the oven', '5,000', '5,000', '0', '0'],
        ['Licence fee to start the restaurant', '30,000', '30,000', '0', '0'],
        ['Fine for breaking municipal rules', '2,000', '0', '2,000', '0'],
        ['Licence renewal fee for 2027-28 paid in advance', '6,000', '0', '0', '6,000'],
        ['Fire insurance for calendar year 2027 paid 1 Jan 2027', '12,000', '0', inr(ins_exp), inr(ins_pre)],
        ['Temporary shed for building material (demolished later)', '18,000', '18,000', '0', '0'],
        ['Construction of restaurant building', '6,00,000', '6,00,000', '0', '0'],
        ['Gas, salaries and other running costs', '84,000', '0', '84,000', '0'],
        ['Total', '9,42,000', inr(capt), inr(revt), inr(pre)],
    ], num=[1, 2, 3, 4], total=True, title='Classification for the year ending 31 March 2027')

    # ---------------- Illustration 2: receipts ----------------
    c2 = Checks()
    prof_m = c2.add('520000-450000', 'Profit on sale of machine')
    to_pl = c2.add('70000+24000+200000+15000', 'Total credited to profit and loss account')
    cap_rec = c2.add('520000+300000+100000+1000000+80000', 'Total capital receipts')
    rc_tbl = table(['Receipt', 'Amount (₹)', 'Nature', 'Amount credited to P&L (₹)'], [
        ['Sale proceeds of machine (book value ₹4,50,000)', '5,20,000', 'Capital receipt', inr(prof_m)],
        ['Fixed deposit repaid on maturity', '3,00,000', 'Capital receipt (return of the deposit)', '0'],
        ['Interest on the fixed deposit', '24,000', 'Revenue receipt', '24,000'],
        ['Premium on issue of shares', '1,00,000', 'Capital receipt', '0'],
        ['Term loan from a bank', '10,00,000', 'Capital receipt', '0'],
        ['Cash sales of goods', '2,00,000', 'Revenue receipt', '2,00,000'],
        ['Insurance claim for a machine destroyed by fire', '80,000', 'Capital receipt', '0'],
        ['Commission earned on agency sales', '15,000', 'Revenue receipt', '15,000'],
        ['Total', '22,39,000', '', inr(to_pl)],
    ], num=[1, 3], total=True, title='Receipts of Prism Industries Ltd, 2026-27')
    c2.add('520000+300000+24000+100000+1000000+200000+80000+15000', 'Total receipts')

    # ---------------- Illustration 3: repairs vs improvements ----------------
    c3 = Checks()
    exp3 = c3.add('35000+8000+6000', 'Amount to be expensed')
    capz = c3.add('320000+22000+14000', 'Amount to be capitalised')
    rep_tbl = table(['Expenditure', 'Amount (₹)', 'Expense (₹)', 'Capitalise (₹)', 'Reason'], [
        ['Repairs to the existing office building', '35,000', '35,000', '0', 'Maintains the asset; no extra benefit'],
        ['Repainting the existing building', '8,000', '8,000', '0', 'Routine upkeep'],
        ['Adding a new floor to the building', '3,20,000', '0', '3,20,000', 'Extension — enlarges capacity for years'],
        ['Upgrading electrical wiring to carry more load', '22,000', '0', '22,000', 'Improvement that increases future benefit'],
        ['Replacing a worn-out belt of a machine', '6,000', '6,000', '0', 'Keeps the machine working as before'],
        ['New fuel-saving burners fitted to the boiler', '14,000', '0', '14,000', 'Reduces running cost in future years'],
        ['Total', '4,05,000', inr(exp3), inr(capz), ''],
    ], num=[1, 2, 3], total=True, title='Repairs or improvements?')

    diff_tbl = table(['Basis', 'Capital expenditure', 'Revenue expenditure'], [
        ['Period of benefit', 'Benefit lasts for more than one accounting period', 'Benefit used up within the current period'],
        ['Purpose', 'Increases earning capacity, or reduces costs, of the business', 'Maintains the existing earning capacity'],
        ['Frequency', 'Usually non-recurring', 'Usually recurring'],
        ['Where shown', 'Asset side of the balance sheet; charged to P&L gradually (depreciation/amortisation) as the benefit is used', 'Profit and loss account of the year in which incurred'],
        ['Examples', 'Machine, car, furniture for use, building, licence to start business, installation and freight on an asset', 'Salaries, rent, repairs and maintenance, cost of goods sold, power'],
    ], title='Capital versus revenue expenditure')
    rec_tbl = table(['Basis', 'Capital receipt', 'Revenue receipt'], [
        ['Source', 'Not from the normal operations: loans, owners\' capital, share premium, sale of fixed assets or investments, return of deposits, insurance claim on a fixed asset', 'Normal operations: sale of goods or services, interest, commission, rent, dividend received'],
        ['Treatment', 'Not credited directly to the P&L account; shown in the balance sheet (only a profit or loss on sale of an asset goes to P&L)', 'Credited to the P&L account of the period'],
        ['Recurrence', 'Usually non-recurring', 'Usually recurring'],
        ['Effect', 'Increases a liability or capital, or reduces an asset', 'Increases profit'],
    ], title='Capital versus revenue receipts')

    concepts = [
        {'id': 'c1', 'title': 'Why the capital/revenue split matters',
         'body': ['To measure the result of a period, every payment and receipt must be classified as capital or revenue. Revenue expenditure relates to the operations of the period, or to revenue earned in the period, or gives benefits that do not extend beyond the period. Capital expenditure produces enduring benefits — it helps earn revenue over more than one period.',
                  'Revenue expenditure goes to the profit and loss account of the year it is incurred. Capital expenditure is shown as an asset in the balance sheet and is transferred to the profit and loss account in the years in which its benefit is used up (through depreciation or amortisation). So both kinds eventually reach the profit and loss account — the difference is timing. Matching decides when and how much is charged.',
                  'The line between the two is often thin, and a wrong classification misstates both profit and assets: capitalising a revenue item overstates profit and assets; expensing a capital item understates them.'],
         'analogy': 'Buying a bicycle is like capital expenditure — you ride it for years. Paying for a tyre puncture repair is revenue — it only keeps today\'s ride going.',
         'work': 'Tax officers and auditors look closely at "repairs" — large repairs that really improve an asset are often wrongly expensed to cut taxable profit, while some companies capitalise routine costs to show higher profit.'},
        {'id': 'c2', 'title': 'Considerations in deciding capital or revenue',
         'body': ['(a) Nature of business: furniture bought by a furniture dealer for resale is revenue (purchases); the same furniture bought by a bank for its office is capital.',
                  '(b) Recurring nature: expenses incurred frequently within a year (monthly salary, rent) are revenue; infrequent outlays like buying an asset are capital — unless the amount is so small that materiality makes it revenue.',
                  '(c) Purpose: normal maintenance and ordinary repairs are revenue; a major repair or overhaul that increases productive capacity is capital. Telling them apart is not always simple.',
                  '(d) Effect on revenue-generating capacity: outlay that helps earn revenue only in the current period is revenue; outlay that helps over more than one period is capital. Repairs or improvements are added to the asset only if they increase its expected future benefits; otherwise they are charged to profit and loss.',
                  '(e) Materiality: the relative size of the amount — a ₹400 stapler is expensed even though it lasts years.'],
         'analogy': 'A five-question test before you file a payment: Who am I (nature of business)? How often (recurring)? Why (purpose)? For how long (capacity)? How big (materiality)?',
         'work': 'Companies write a "capitalisation policy" — e.g. items below ₹5,000 are expensed — which is a practical application of materiality and consistency. As an auditor you test entries against it.'},
        {'id': 'c3', 'title': 'Capital expenditure — what goes into the cost of an asset',
         'body': ['Capital expenditure includes the purchase price of a fixed asset plus all costs needed to bring it to a usable condition: freight and transport, installation (including wages of own workers who install it), legal fees to acquire property, overhaul or repainting of a second-hand asset before first use, the first repairs and whitewash of an old building bought, temporary huts or sheds needed during construction, and travelling expenses incurred to buy a capital asset.',
                  'Also capital: expenditure to acquire a right to carry on business (licence to start a factory or cinema); expenditure that increases capacity (adding cabins, an extra floor) or reduces running costs (new rings and pistons for fuel efficiency); demolition of an old building to construct a bigger one on the same site; wages paid to workers for making a tool or asset to be used in the business.',
                  'Not expenditure at all: a security deposit (for example, with a telephone or electricity company) is an asset recoverable or adjustable later.'],
         'blocks': [diff_tbl],
         'analogy': 'The cost of a new phone includes the delivery charge and the setup fee — everything needed before you can use it.',
         'work': 'When a client installs a new plant, the CA collects freight, insurance-in-transit, installation and trial-run costs and adds them to the asset — and makes sure routine items do not slip in.'},
        {'id': 'c4', 'title': 'Revenue expenditure — keeping the business running',
         'body': ['Revenue expenditure maintains the existing earning capacity: salaries, wages, rent, power, cost of goods sold, routine repairs and maintenance, replacement of worn-out parts, carriage on goods sold, and so on. Some revenue expenses relate directly to sales (cost of goods sold); others relate to the period (rent).',
                  'Tricky revenue items: legal fees to defend the title to an existing asset (it protects what you already have — no new benefit); legal expenses to recover dues from customers; fines and penalties; removal of inventory to a new site; inauguration expenses of a new unit (no enduring benefit); compensation paid to workers under voluntary retirement (no asset created).',
                  'Amounts paid in advance for the next period (renewal fee, insurance) are revenue in nature but are shown as prepaid expenses (an asset) at the year end.'],
         'analogy': 'Fuel, servicing and the parking fee for your car — none of them makes the car better, they just keep it on the road.',
         'work': 'At year end, accountants review the "repairs and maintenance" ledger; any big-ticket item gets a second look to decide whether it should be capitalised.'},
        {'id': 'c5', 'title': 'Capital receipts and revenue receipts',
         'body': ['Revenue receipts arise in the normal course of business — sale of goods or services, interest, commission, rent, dividends, a government subsidy given for working capital. They are credited to the profit and loss account. They are recognised on the accrual basis when the right to receive arises, so revenue is not the same as cash received.',
                  'Capital receipts are receipts that are not revenue in nature — sale proceeds of fixed assets or investments, secured or unsecured loans, capital contributed by owners, premium on issue of shares, return of a deposit on maturity, an insurance claim for a fixed asset destroyed. They are not credited directly to the profit and loss account.',
                  'Sale of a fixed asset: the whole proceeds are a capital receipt; only the profit (proceeds − book value) or loss is taken to profit and loss account.'],
         'blocks': [rec_tbl],
         'analogy': 'Your salary is a revenue receipt; selling your old car or taking a home loan is a capital receipt — money comes in, but you are not "earning" it.',
         'work': 'In GST and income-tax work, classifying receipts correctly decides what is taxable as income. For a company, share premium credited to profit would be a serious misstatement.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Classifying the first year\'s spending of a restaurant', 'difficulty': 'moderate', 'minutes': 14,
         'q': 'Spice Route Restaurant (year ending 31 March 2027) made the following payments: second-hand oven ₹1,60,000; overhaul of the oven before first use ₹25,000; wages of its own staff for installing the oven ₹5,000; licence fee to start the restaurant ₹30,000; fine for breaking municipal rules ₹2,000; licence renewal fee for 2027-28 paid in advance ₹6,000; fire insurance for calendar year 2027 paid on 1 January 2027 ₹12,000; temporary shed for building material, demolished when the building was ready ₹18,000; construction of the building ₹6,00,000; gas, salaries and other running costs ₹84,000. Classify each payment and find the total capital expenditure, the revenue expenditure for 2026-27 and the prepaid amount.',
         'solution': [r_tbl,
                      wn('Oven', f'Price, overhaul and installation are all needed before the oven can be used: 1,60,000 + 25,000 + 5,000 = ₹{inr(oven)} is capitalised. If the overhaul and wages had been debited to Repairs and Wages, those accounts would be credited and the Oven (Equipment) account debited.'),
                      wn('Insurance', f'Only January–March 2027 falls in this year: 12,000 × 3/12 = ₹{inr(ins_exp)}. The balance ₹{inr(ins_pre)} is prepaid.'),
                      note('The fine is revenue (a penalty, no future benefit); the advance renewal fee is revenue in nature but belongs to next year, so it is prepaid.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Sorting receipts and finding what goes to profit and loss', 'difficulty': 'core', 'minutes': 10,
         'q': 'Prism Industries Ltd received the following in 2026-27: ₹5,20,000 on sale of a machine with a book value of ₹4,50,000; ₹3,00,000 on maturity of a fixed deposit plus interest ₹24,000; premium on issue of shares ₹1,00,000; a term loan of ₹10,00,000 from a bank; cash sales ₹2,00,000; insurance claim ₹80,000 for a machine destroyed by fire; commission ₹15,000. Classify each receipt and compute the amount credited to the profit and loss account.',
         'solution': [rc_tbl,
                      wn('Machine', f'The proceeds of ₹5,20,000 are a capital receipt. Only the profit of 5,20,000 − 4,50,000 = ₹{inr(prof_m)} is credited to profit and loss.'),
                      wn('Total to P&L', f'Profit on sale {inr(prof_m)} + interest 24,000 + sales 2,00,000 + commission 15,000 = ₹{inr(to_pl)}.'),
                      note('The insurance claim would be compared with the book value of the destroyed machine; the resulting loss or gain (not the whole claim) affects profit. Book value is not given here, so only the classification is asked.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Repairs versus improvements', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'Rana Textiles spent the following during the year: repairs to the existing office building ₹35,000; repainting the existing building ₹8,000; adding a new floor ₹3,20,000; upgrading electrical wiring to carry more load ₹22,000; replacing a worn-out belt of a machine ₹6,000; new fuel-saving burners fitted to the boiler ₹14,000. How much should be charged to profit and loss and how much capitalised?',
         'solution': [rep_tbl, p(f'Charged to profit and loss: ₹{inr(exp3)}. Capitalised: ₹{inr(capz)}. The test is whether the expected future benefit from the asset increases (capitalise) or stays the same (expense).')],
         'checks': c3},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Reviewing a "Repairs" ledger at year end', 'role': 'Article assistant on the statutory audit of a manufacturing company',
         'situation': 'The repairs ledger shows ₹18 lakh against ₹6 lakh last year. Among the entries: ₹9 lakh for a complete rebuild of a press that raises its output by 30%, ₹1.5 lakh for routine servicing, and ₹40,000 legal fees paid to defend a claim over the factory land.',
         'steps': ['List large and unusual items and obtain invoices and work orders.',
                   'Rebuild raising output by 30% — increases productive capacity: propose capitalising ₹9 lakh (and depreciating it).',
                   'Routine servicing — revenue, correctly expensed.',
                   'Legal fees to defend title to existing land — revenue (protects an existing asset; no new benefit).',
                   'Compute the effect: profit and fixed assets were understated by ₹9 lakh before depreciation; raise the point with the client.'],
         'takeaway': 'The label on the ledger does not decide the nature of a payment — its purpose and effect on future benefit do.',
         'think': 'Why would a company want to treat a capital item as repairs?',
         'answer': 'Expensing reduces profit and therefore income tax for the year; it may also hide large spending from the board. Both are reasons auditors look closely at repairs.'},
        {'id': 'j2', 'title': 'Advising a gym owner on start-up costs', 'role': 'Practising CA advising a small business client',
         'situation': 'A client opening a gym asks which costs will reduce her first-year profit: equipment ₹12 lakh, its transport and installation ₹60,000, trade licence ₹25,000, an opening-day event ₹80,000, monthly rent and salaries ₹4.8 lakh for the year.',
         'steps': ['Equipment with transport and installation — capital; only depreciation will reduce profit each year.',
                   'Trade licence — needed to start the business; capitalised (and written off over its period of benefit).',
                   'Opening-day event — inauguration expenses give no enduring benefit; revenue.',
                   'Rent and salaries — revenue.',
                   'Explain that her first-year profit will be reduced by ₹5.6 lakh of revenue expenses plus depreciation/amortisation, not by the full ₹18.45 lakh spent.'],
         'takeaway': 'Clients think in cash spent; accounts think in benefit periods. Explaining the difference avoids nasty surprises when profit is reported.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'A furniture dealer buys tables for resale. In his books this is:', 'options': ['Revenue expenditure', 'Capital expenditure', 'Capital receipt', 'A prepaid expense'], 'answer': 0, 'explain': 'Whether an expense is capital or revenue depends on the nature of the business. For a furniture dealer, tables are stock-in-trade bought for resale, so their purchase is revenue expenditure charged through purchases. The trap is capital expenditure: furniture is a fixed asset only for a business that keeps it for use, such as an office buying tables for its staff. In practice: the same laptop is inventory for a Croma store but a fixed asset, depreciated over years, for a CA firm.', 'topic': 'Considerations in Determining Capital and Revenue Expenditures', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'A firm pays a lawyer to fight a case in which a neighbour says the land under the firm\'s factory is his. The fee is:', 'options': ['Revenue expenditure', 'Capital expenditure', 'Part of the cost of land', 'A capital receipt'], 'answer': 0, 'explain': 'Legal fees to defend the title to land the firm already owns only protect an existing asset; they add no new or enduring benefit, so they are revenue expenditure charged to profit and loss. The tempting option, adding the fee to the cost of land, confuses this with legal fees paid to acquire a property, which are capitalised. In practice: Indian companies routinely charge legal expenses on title and boundary disputes to the profit and loss account as legal and professional charges.', 'topic': 'Capital Expenditures and Revenue Expenditures', 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm3', 'q': 'Legal fees paid to acquire a property are:', 'options': ['Capital expenditure', 'Revenue expenditure', 'A prepaid expense', 'A capital receipt'], 'answer': 0, 'explain': "Legal fees paid to acquire a property are part of the cost of obtaining ownership of it, so they are capital expenditure and are added to the cost of the property, along with stamp duty and registration charges. The trap is revenue expenditure: legal fees are revenue only when they are routine or defend an asset already owned. In practice: when a company buys an office in Mumbai, its accountant capitalises stamp duty, registration and lawyer's fees as part of the building's cost.", 'topic': 'Capital Expenditures and Revenue Expenditures', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'Cost of replacing a worn-out part of a machine is:', 'options': ['Revenue expenditure', 'Capital expenditure', 'A capital receipt', 'Not recorded'], 'answer': 0, 'explain': "Replacing a worn-out part only keeps the machine working at its existing capacity; it does not increase output, life or efficiency, so the cost is revenue expenditure (maintenance). The tempting option, capital expenditure, would apply only if the replacement improved the machine — for example, a part that raises output or extends its life significantly. In practice: factories in India book such costs under 'repairs and maintenance — plant and machinery' in the profit and loss account.", 'topic': 'Capital Expenditures and Revenue Expenditures', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm5', 'q': 'Compensation paid to workers who opted for voluntary retirement is treated as:', 'options': ['Revenue expenditure', 'Capital expenditure', 'An intangible asset', 'A capital receipt'], 'answer': 0, 'explain': 'Voluntary retirement compensation is paid to end employment; it does not create any asset or enduring benefit that the business controls, so it is revenue expenditure charged to profit and loss. The tempting option, an intangible asset, assumes future savings in salary make it an asset, but accounting standards do not allow such payments to be capitalised. In practice: Indian public sector banks and companies have charged VRS payouts to profit and loss, often disclosing them as exceptional items.', 'topic': 'Capital Expenditures and Revenue Expenditures', 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm6', 'q': 'A government subsidy received by a manufacturer to meet working capital needs is a:', 'options': ['Revenue receipt', 'Capital receipt', 'Loan receipt', 'Capital expenditure'], 'answer': 0, 'explain': 'A receipt is revenue if it is linked to day-to-day operations. A subsidy given to meet working capital needs helps the business run its routine operations, so it is a revenue receipt credited to profit and loss. The tempting option, capital receipt, applies to a grant for buying fixed assets or contributing to capital, not to one supporting running costs. In practice: State governments in India give such operating subsidies to MSMEs, and the units show them as other operating income.', 'topic': 'Capital Receipts and Revenue Receipts', 'concept': 'c5', 'difficulty': 'moderate'},
        {'id': 'm7', 'q': 'A medium-term loan received from a bank is a:', 'options': ['Capital receipt', 'Revenue receipt', 'Revenue expenditure', 'Capital expenditure'], 'answer': 0, 'explain': 'Borrowed money must be repaid, so it creates a liability, not income; any loan from a bank is a capital receipt and goes to the balance sheet, not to profit and loss. The trap is revenue receipt — cash coming into the business is not automatically income. In practice: when a business takes a ₹20 lakh term loan to expand, its accountant credits the bank loan account; only the interest paid on it later reaches the profit and loss account, as an expense.', 'topic': 'Capital Receipts and Revenue Receipts', 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm8', 'q': 'Repairs to a building in use ₹40,000; whitewash of the same building ₹6,000; extension of the building ₹3,00,000; improvement of electrical wiring ₹25,000. The amount to be charged to profit and loss is:', 'options': ['₹46,000', '₹71,000', '₹3,71,000', '₹3,25,000'], 'answer': 0, 'check': '40000+6000', 'explain': "Repairs (₹40,000) and whitewash (₹6,000) merely maintain the building, so ₹46,000 is revenue expenditure charged to profit and loss. The extension (₹3,00,000) adds capacity and the wiring improvement (₹25,000) increases future benefit, so both are capitalised. The tempting ₹71,000 wrongly treats the wiring improvement as a repair; an improvement goes beyond restoring the original condition. In practice: auditors check large 'repairs' bills to see whether any of them are really improvements that should be capitalised.", 'topic': 'Considerations in Determining Capital and Revenue Expenditures', 'concept': 'c2', 'difficulty': 'hard'},
        {'id': 'm9', 'q': 'A machine with a book value of ₹2,40,000 is sold for ₹2,75,000. The amount credited to the profit and loss account is:', 'options': ['₹35,000', '₹2,75,000', '₹2,40,000', '₹5,15,000'], 'answer': 0, 'check': '275000-240000', 'explain': "Sale proceeds of a fixed asset are a capital receipt. Only the profit on sale — ₹2,75,000 − ₹2,40,000 book value = ₹35,000 — is credited to profit and loss; the book value of ₹2,40,000 simply removes the asset from the books. The tempting ₹2,75,000 treats the whole sale proceeds as income, overstating profit by the book value. In practice: Indian companies show such gains under 'other income' as profit on sale of fixed assets.", 'topic': 'Capital Receipts and Revenue Receipts', 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm10', 'q': 'Wages paid to the firm\'s own workers for installing a new machine are:', 'options': ['Capital expenditure', 'Revenue expenditure', 'A prepaid expense', 'A deferred receipt'], 'answer': 0, 'explain': "All costs needed to bring an asset to working condition for its intended use form part of its cost. Wages paid to the firm's own workers for installing the machine are therefore capitalised as part of the machine. The trap is revenue expenditure — wages are normally a revenue expense, but here they are spent creating an asset, not running the business. In practice: companies transfer such in-house installation wages from the wages account to the asset account by a journal entry.", 'topic': 'Capital Expenditures and Revenue Expenditures', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm11', 'q': 'A security deposit paid to an electricity company for a new connection is:', 'options': ['An asset — not an expenditure', 'Revenue expenditure', 'Capital expenditure to be depreciated', 'A capital receipt'], 'answer': 0, 'explain': "A security deposit is not spent; it remains recoverable when the connection is closed or is adjusted against future bills, so it is shown as an asset (usually a deposit under other assets) and is neither expensed nor depreciated. The tempting option, revenue expenditure, would treat a refundable deposit as if it were consumed. In practice: rent, electricity and telephone deposits appear as 'security deposits' in the balance sheets of Indian businesses, sometimes for decades.", 'topic': 'Capital Expenditures and Revenue Expenditures', 'concept': 'c3', 'difficulty': 'moderate'},
        {'id': 'm12', 'q': 'An annual insurance premium of ₹18,000 is paid on 1 October 2026. For the year ending 31 March 2027, the revenue expense and the prepaid amount are:', 'options': ['₹9,000 expense; ₹9,000 prepaid', '₹18,000 expense; nil prepaid', '₹4,500 expense; ₹13,500 prepaid', '₹13,500 expense; ₹4,500 prepaid'], 'answer': 0, 'explain': 'Only the portion of the premium relating to the current year is an expense. Cover from 1 October 2026 to 31 March 2027 is 6 months: ₹18,000 × 6/12 = ₹9,000 expense; the remaining ₹9,000 covers April–September 2027 and is shown as prepaid insurance, an asset. The tempting ₹18,000 expense charges the full cash payment, ignoring accrual. In practice: year-end adjustments in every Indian company include prepaid expenses for insurance, AMCs and subscriptions.', 'topic': 'Capital Expenditures and Revenue Expenditures', 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm13', 'q': 'Amount spent on demolishing an old building to construct a bigger one on the same site is:', 'options': ['Capital expenditure', 'Revenue expenditure', 'A loss to be written off immediately', 'A capital receipt'], 'answer': 0, 'explain': 'Demolishing the old building is a necessary step in constructing the new, bigger building on the site, so its cost is part of the capital cost of the new building. The tempting option, writing it off as a loss, treats the demolition as wasted money, but it is incurred to obtain an enlarged asset with enduring benefit. In practice: real estate developers redeveloping old housing societies in Mumbai include demolition costs in the cost of the new project.', 'topic': 'Capital Expenditures and Revenue Expenditures', 'concept': 'c3', 'difficulty': 'moderate'},
    ]

    q3c = Checks()
    q3_furn = q3c.add('48000+4000+1500', 'Furniture: price + repainting + fitting wages')
    q3_lic = q3c.add('40000', 'Licence to start the coaching centre')
    q3_rev = q3c.add('3000+7500', 'Revenue: fine + insurance for 6 months (15,000 × 6/12)')
    q3_pre = q3c.add('5000+7500', 'Prepaid: renewal fee for next year + insurance for 6 months')
    q3_cap = q3c.add('53500+40000+9000', 'Total capital expenditure incl. temporary partition used during construction')
    q3_tbl = table(['Item', 'Capital (₹)', 'Revenue (₹)', 'Prepaid (₹)'], [
        ['Second-hand furniture ₹48,000 + repainting ₹4,000 + fitting by own staff ₹1,500', inr(q3_furn), '0', '0'],
        ['Licence to start the centre', '40,000', '0', '0'],
        ['Fine for violating local rules', '0', '3,000', '0'],
        ['Licence renewal fee for next year', '0', '0', '5,000'],
        ['Insurance ₹15,000 for one year from 1 October 2026', '0', '7,500', '7,500'],
        ['Temporary partitions needed during construction, later removed', '9,000', '0', '0'],
        ['Total', inr(q3_cap), inr(q3_rev), inr(q3_pre)],
    ], num=[1, 2, 3], total=True)

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'text',
         'q': 'Explain, with examples, the factors you would weigh when deciding whether a particular outlay should be treated as capital expenditure or revenue expenditure.',
         'model': [ul(['Nature of business — furniture bought by a furniture dealer is revenue (stock-in-trade), but furniture bought by any other business for its own use is capital.',
                       'Recurring nature — frequent outlays within the year (salary, rent) are revenue; infrequent outlays such as purchase of an asset are capital, unless the amount is immaterial.',
                       'Purpose — normal maintenance and ordinary repairs are revenue; a major repair or overhaul that increases productive capacity is capital.',
                       'Effect on revenue-generating capacity — if the benefit is limited to the current period, it is revenue; if it helps earn revenue over more than one period, it is capital. Improvements are capitalised only when expected future benefits increase.',
                       'Materiality of the amount — small items (a stapler, a calculator) are expensed even if they last long.'])],
         'scheme': [
             {'id': 's1', 'pt': 'Nature of business with example', 'm': 1, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Recurring nature with example', 'm': 1, 'skill': 'concept'},
             {'id': 's3', 'pt': 'Purpose (maintenance vs capacity increase)', 'm': 1, 'skill': 'concept'},
             {'id': 's4', 'pt': 'Effect on revenue-generating capacity / period of benefit', 'm': 1, 'skill': 'concept'},
             {'id': 's5', 'pt': 'Materiality', 'm': 1, 'skill': 'concept'},
         ],
         'remarks': ['Answers that give the five headings with one example each score full marks quickly.', 'Many candidates simply define capital and revenue expenditure — that is not what is asked.'],
         'mistakes': ['Omitting materiality.', 'Saying "all repairs are revenue".'],
         'tips': ['Use the five headings as bold points.', 'One example per point — examples are what convince the examiner.']},
        {'id': 'q2', 'marks': 8, 'minutes': minutes(8), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'State with reasons whether each of the following is capital or revenue: (1) overhaul of a second-hand truck just bought, to make it roadworthy; (2) money spent on a new process that cuts power cost every year; (3) legal fees to recover instalments due from customers; (4) cost of shifting inventory to a new godown; (5) travelling expenses of directors abroad to buy a new plant; (6) inauguration expenses of a new branch; (7) premium received on issue of shares; (8) wages paid to own workers for making a tool to be used in the factory.',
         'model': [table(['Item', 'Nature', 'Reason'], [
             ['(1) Overhaul of second-hand truck before use', 'Capital expenditure', 'Needed to put the asset into working condition; part of its cost'],
             ['(2) New process reducing power cost', 'Capital expenditure', 'Gives an enduring benefit by reducing future costs'],
             ['(3) Legal fees to recover customer dues', 'Revenue expenditure', 'Normal recurring expense; no increase in future earning capacity'],
             ['(4) Shifting inventory to a new godown', 'Revenue expenditure', 'Neither brings enduring benefit nor adds to the value of an asset'],
             ['(5) Directors\' travel to buy a plant', 'Capital expenditure', 'Incurred to acquire a capital asset; added to its cost'],
             ['(6) Inauguration of a new branch', 'Revenue expenditure', 'May attract customers but gives no enduring benefit beyond the period'],
             ['(7) Share premium received', 'Capital receipt', 'Not from normal operations; shown under reserves, not credited to P&L'],
             ['(8) Wages for making a tool for own use', 'Capital expenditure', 'Creates an asset to be used in the business for several periods'],
         ])],
         'scheme': [{'id': f's{i}', 'pt': f'Item ({i}) correct nature with reason', 'm': 1, 'skill': 'classification'} for i in range(1, 9)],
         'remarks': ['Marks are given only when the reason supports the classification — a bare "capital" earns nothing.', 'Item (2) and item (6) are the most frequently missed.'],
         'mistakes': ['Treating inauguration expenses as capital because they relate to a new unit.', 'Calling share premium a revenue receipt because it is "extra" money.'],
         'tips': ['Answer in a three-column table: Item | Nature | Reason.', 'Keep reasons to one line each — the reason is the mark.']},
        {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'Bright Minds Coaching Centre was set up during 2026-27 (year ending 31 March 2027). It bought second-hand furniture for ₹48,000, spent ₹4,000 on repainting it and paid its own staff ₹1,500 for fitting it. It paid ₹40,000 for a licence to start the centre, a fine of ₹3,000 for violating local rules and a licence renewal fee of ₹5,000 for next year. A one-year insurance premium of ₹15,000 was paid on 1 October 2026. Temporary partitions costing ₹9,000, necessary while the premises were being built, were removed afterwards. Classify the items and show the totals.',
         'model': [q3_tbl,
                   wn('Notes', f'Furniture cost = 48,000 + 4,000 + 1,500 = ₹{inr(q3_furn)} — all needed before use. Insurance: 6 months (October–March) = ₹7,500 expense; ₹7,500 prepaid. Partitions are incidental to construction and capitalised.')],
         'scheme': [
             {'id': 's1', 'pt': f'Furniture capitalised at ₹{inr(q3_furn)}', 'm': 1.5, 'skill': 'classification'},
             {'id': 's2', 'pt': 'Licence capital; fine revenue', 'm': 1, 'skill': 'classification'},
             {'id': 's3', 'pt': 'Renewal fee shown as prepaid', 'm': 1, 'skill': 'application'},
             {'id': 's4', 'pt': 'Insurance split ₹7,500 / ₹7,500', 'm': 1, 'skill': 'computation'},
             {'id': 's5', 'pt': 'Temporary partitions capitalised; totals correct', 'm': 1.5, 'skill': 'presentation'},
         ],
         'remarks': ['The repainting and fitting wages are often expensed — they are part of the furniture\'s cost.', 'Candidates who show the whole insurance premium as expense lose the computation mark.'],
         'mistakes': ['Treating the renewal fee as capital because it relates to the licence.', 'Charging the temporary partitions to profit and loss because they were removed.'],
         'tips': ['Use columns Capital | Revenue | Prepaid and total them.', 'Write a one-line note for each judgement item.']},
        {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'Define revenue receipts and capital receipts with examples. How is the sale of a fixed asset dealt with in the accounts?',
         'model': [p('Revenue receipts arise in the normal course of business — sale of goods or services, interest, commission, rent, dividends received. They are recognised on accrual basis when the right to receive is established and are credited to the profit and loss account.'),
                   p('Capital receipts are receipts that are not revenue in nature — loans raised, capital introduced by owners, premium on shares, sale proceeds of fixed assets or investments, return of deposits. They are not credited directly to the profit and loss account; they affect the balance sheet.'),
                   p('On sale of a fixed asset, the whole sale price is a capital receipt. The profit (sale price − book value) or loss is computed and only that amount is taken to the profit and loss account. Example: book value ₹1,10,000, sold for ₹1,25,000 — ₹15,000 profit to P&L.')],
         'scheme': [
             {'id': 's1', 'pt': 'Revenue receipt defined with examples; credited to P&L', 'm': 1.5, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Capital receipt defined with examples; not credited to P&L', 'm': 1.5, 'skill': 'concept'},
             {'id': 's3', 'pt': 'Sale of fixed asset: only profit/loss to P&L', 'm': 1, 'skill': 'application'},
         ],
         'remarks': ['A numerical example for the sale of an asset makes the last part crystal clear.'],
         'mistakes': ['Crediting the full sale proceeds to P&L.', 'Equating revenue receipts with cash received.'],
         'tips': ['Two short paragraphs and a one-line example are enough for 4 marks.']},
    ]

    viva = [
        V('v1', 'Distinguish between capital expenditure and revenue expenditure.',
          'Capital expenditure gives benefit over more than one accounting period and increases the earning capacity of the business, like buying a machine; it is shown as an asset in the balance sheet. Revenue expenditure gives benefit only in the current period and maintains the earning capacity, like salaries or repairs; it is charged to the profit and loss account of that year.',
          [P('p1', 'Capital: benefit over more than one period / increases capacity', 3,
             ALT('capital {x}', 'capital benefit {x}', 'capital expenditure benefit {x}', x=('more than one', 'several', 'long', 'many year', 'enduring', 'future', 'increas', 'enhanc', 'improv', 'earning capacity', 'capitalis', 'asset', 'last', 'not consum', 'not used up', 'not exhaust'))),
           P('p2', 'Capital shown as asset in balance sheet', 2, 'asset|balance sheet', min=1),
           P('p3', 'Revenue: benefit within current period / maintains capacity', 3,
             ALT('revenue {x}', 'revenue benefit {x}', 'revenue expenditure benefit {x}', x=('current', 'only', 'same year', 'one year', 'one period', 'that year', 'within', 'maintain', 'day to day', 'running', 'routine', 'short', 'recurring', 'charg', 'profit loss', 'written off'))),
           P('p4', 'Revenue charged to profit and loss account', 2, 'profit loss|profit and loss|income statement|charg|expens', min=1)], 'c1'),
        V('v2', 'What factors do you consider in deciding whether an expenditure is capital or revenue?',
          'I look at five factors: the nature of the business, whether the expenditure is recurring, its purpose such as maintenance or increase in capacity, its effect on the revenue earning capacity over one or more periods, and the materiality of the amount.',
          [P('p1', 'Nature of business', 2, 'nature business|type business|kind business|nature of the business|business nature'),
           P('p2', 'Recurring nature / frequency', 2, 'recurr|frequen|regular|repeat|often'),
           P('p3', 'Purpose — maintenance vs capacity increase', 2, 'purpose|maintenance|maintain|capacity|reason'),
           P('p4', 'Effect on revenue-generating capacity / period of benefit', 2, 'earning capacity|revenue earning|revenue generat|earn capacity|period|benefit|future'),
           P('p5', 'Materiality of amount', 2, 'material|amount|size|small|big|significan')], 'c2'),
        V('v3', 'Is every repair a revenue expenditure? Explain.',
          'No, not every repair is revenue. Ordinary repairs and maintenance that only keep the asset working as before are revenue expenditure. But a major repair or overhaul that increases the productive capacity or life of the asset, or reduces running costs, is capital expenditure. Repairs to put a second-hand asset into working condition are also capital.',
          [P('p1', 'Not every repair is revenue', 2, 'not every|not all|no not|not always|isn t always|not necessarily|depend|no|some repair capital|can be capital'),
           P('p2', 'Ordinary repairs / maintenance — revenue', 4, 'ordinary|routine|normal|maintenance|maintain|minor|regular|small|keep working|as before', 'revenue|expens|profit loss', min=2),
           P('p3', 'Major repair increasing capacity or reducing cost — capital', 4, 'major|overhaul|increas|improv|enhanc|extend|life|reduc|second hand|working condition|capacity|efficien', 'capital|capitalis|asset', min=2)], 'c2'),
        V('v4', 'Distinguish between capital receipts and revenue receipts with examples.',
          'Revenue receipts come from the normal operations of the business, like sale of goods, interest or commission received, and are credited to the profit and loss account. Capital receipts are not from normal operations, like loans, capital introduced, share premium or sale of fixed assets, and are not credited to the profit and loss account; they appear in the balance sheet.',
          [P('p1', 'Revenue receipts: from normal/ordinary operations', 3, ALT('revenue receipt {x}', 'revenue receipt {y}', '{x} revenue receipt', '{x} are revenue', x=('normal', 'ordinary', 'regular', 'day to day', 'operation', 'routine', 'interest', 'commission'), y=('sale', 'sale of goods', 'from sale', 'arise sale'))),
           P('p2', 'Revenue receipts credited to P&L', 2, 'profit loss|profit and loss|income statement|credit p|credited to profit'),
           P('p3', 'Capital receipts: loans, capital, share premium, sale of fixed assets', 3, 'capital receipt|capital in nature|capital nature', 'loan|borrow|premium|capital introduc|introduc capital|owner capital|fixed asset|sale of asset|sale of machine|investment|insurance claim|deposit'),
           P('p4', 'Capital receipts not credited to P&L / shown in balance sheet', 2, ALT('{n} credit profit', '{n} credited profit', '{n} go profit', '{n} goes profit', '{n} taken profit', '{n} shown profit', '{n} profit loss', n=('not', 'no', 'never', 'don t', 'doesn t', 'aren t', 'isn t')) + '|balance sheet|liabilit')], 'c5'),
        V('v5', 'A fixed asset is sold. How is the sale proceeds treated in the accounts?',
          'The whole sale proceeds are a capital receipt and are not credited to the profit and loss account. Only the profit or loss on sale, that is the difference between the sale price and the book value, is taken to the profit and loss account.',
          [P('p1', 'Sale proceeds are a capital receipt', 3, 'capital receipt|capital in nature|capital nature'),
           P('p2', 'Whole proceeds NOT credited to P&L', 3, ALT('{n} credit', '{n} credited', '{n} taken', '{n} go', '{n} goes', '{n} shown', '{n} directly', '{n} entire', '{n} whole', '{n} full', 'not revenue', 'isn t revenue', 'not a revenue', n=('not', 'no', 'never', 'don t', 'doesn t', 'isn t', 'aren t', 'only')), min=1),
           P('p3', 'Only profit/loss = sale price − book value goes to P&L', 4, 'profit|loss|gain', 'book value|cost|written down|carrying|difference|minus|less', min=2)], 'c5'),
        V('v6', 'Is the purchase of furniture always a capital expenditure?',
          'No, it is not always capital. It depends on the nature of the business. For a furniture dealer who buys it for resale, it is revenue expenditure, that is purchases. For any other business that buys furniture for its own use, it is capital expenditure.',
          [P('p1', 'Not always — depends on the nature of business', 3, 'not always|no|depend|nature of business|nature business|not necessarily|isn t always', min=1),
           P('p2', 'Furniture dealer buying for resale — revenue', 4, 'dealer|trader|resale|resell|sell|stock in trade|stock|trading|deals', 'revenue|purchas|expens', min=2),
           P('p3', 'Other business buying for own use — capital', 3, 'own use|office use|use in business|use|using|office|other business|for itself', 'capital|asset|fixed asset', min=2)], 'c2'),
    ]

    c = Checks()
    k_proj = c.add('850000+45000+30000+20000', 'Projector system: price + freight + installation by own technicians + trial run')
    k_rev = c.add('15000+60000+4000', 'Revenue expenses: legal fee to defend title + opening show + removal of old seats')
    k_cap = c.add('945000+120000+250000', 'Total capital: projector + licence + extra seats')
    cases = [{
        'id': 'k1', 'title': 'Galaxy Cinemas — upgrading the screen', 'difficulty': 'hard',
        'case': ('Galaxy Cinemas (year ending 31 March 2027) bought a new digital projection system for ₹8,50,000, paid freight of ₹45,000, paid its own technicians ₹30,000 to install it and spent ₹20,000 on a trial run before the first show. It paid ₹1,20,000 for a fresh licence needed to screen 3-D films, '
                 'spent ₹2,50,000 on remodelling that increased seating from 180 to 220, paid ₹15,000 to a lawyer to defend a neighbour\'s claim over part of its land, ₹60,000 on an inaugural show for the new screen and ₹4,000 to remove old seats to a store-room. It also sold its old projector (book value ₹70,000) for ₹95,000.'),
        'mcqs': [
            dict(M('k1a', 'At what amount should the new projection system be capitalised?', [R(k_proj), '₹8,50,000', '₹8,95,000', '₹9,25,000'], 0,
              'Every cost needed to bring the projector to working condition is capitalised: price ₹8,50,000 + freight ₹45,000 + installation ₹30,000 + trial run ₹20,000 = ₹9,45,000. The tempting ₹9,25,000 leaves out the trial run, but testing before first use is part of making the asset ready. The inaugural show is not included — it is promotion after the asset is ready. In practice: auditors check that only pre-use costs are capitalised and that launch events are expensed.', 'moderate', '850000+45000+30000+20000'), topic='Capital Expenditures and Revenue Expenditures'),
            dict(M('k1b', 'The ₹2,50,000 remodelling that increased seats from 180 to 220 is:', ['Capital expenditure — it increases earning capacity', 'Revenue expenditure — it is a repair', 'A prepaid expense', 'A capital receipt'], 0,
              "Increasing seating from 180 to 220 raises the cinema's capacity to earn revenue in future years, so the remodelling is capital expenditure added to the building or fit-out cost. The tempting option calls it a repair; a repair only restores the existing condition, while here capacity has grown by 40 seats. In practice: multiplex operators in India capitalise renovations that add screens or seats but expense routine repainting and seat repairs.", 'moderate'), topic='Capital Expenditures and Revenue Expenditures'),
            dict(M('k1c', 'Total revenue expenditure among the items listed is:', [R(k_rev), '₹75,000', '₹64,000', '₹1,99,000'], 0,
              "Revenue items: legal fee defending existing land ₹15,000 + inaugural show ₹60,000 + removing old seats ₹4,000 = ₹79,000. The tempting ₹75,000 misses the ₹4,000 removal cost, which creates no asset. The projector costs, the 3-D licence and the remodelling are capital, and the trial run is part of the projector's cost. In practice: a CA finalising a cinema's accounts would list each such item and decide capital or revenue before computing depreciation.", 'hard', '15000+60000+4000'), topic='Capital Expenditures and Revenue Expenditures'),
            dict(M('k1d', 'How much of the ₹95,000 received for the old projector is credited to the profit and loss account?', ['₹25,000', '₹95,000', '₹70,000', 'Nil'], 0,
              "The ₹95,000 sale proceeds are a capital receipt. Only the profit on sale — ₹95,000 − ₹70,000 book value = ₹25,000 — is credited to profit and loss; the ₹70,000 removes the old projector from the books. The tempting ₹95,000 treats the whole sale price as income. In practice: companies disclose this ₹25,000 under 'other income' as profit on sale of assets, while the full proceeds appear in the cash flow statement under investing activities.", 'core', '95000-70000'), topic='Capital Receipts and Revenue Receipts'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch01', 'n': 3,
        'title': 'Capital and Revenue Expenditures and Receipts',
        'outcomes': [
            'Explain why expenditure and receipts must be classified as capital or revenue, and how each reaches the financial statements.',
            'Apply the five considerations — nature of business, recurrence, purpose, effect on earning capacity and materiality — to classify expenditure.',
            'Identify the costs that form part of an asset\'s cost and the borderline items that are revenue.',
            'Distinguish capital receipts from revenue receipts and treat the sale of a fixed asset correctly.',
        ],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 45}, 'prereq': ['fnd-p1-ch01-u02'],
                 'exam_tip': '"State with reasons whether capital or revenue" is a favourite. A classification without a reason earns nothing — give the one-line reason every time.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Capital expenditure: enduring benefit (more than one period), increases capacity or cuts costs; shown as an asset and charged to P&L as the benefit is used.',
                        'Revenue expenditure: benefit within the period, maintains capacity; charged to P&L of the year. Advance payments for next year are prepaid assets.',
                        'Considerations: nature of business, recurring nature, purpose, effect on revenue-generating capacity, materiality.',
                        'Asset cost includes freight, installation (even by own staff), legal fees to acquire, overhaul/repairs before first use, temporary huts during construction, travel to buy the asset.',
                        'Capital receipts (loans, capital, share premium, sale of fixed assets/investments, return of deposits, insurance claim on asset) are not credited to P&L; revenue receipts (sales, interest, commission, working-capital subsidy) are.'],
            'remember': ['Defending title to an existing asset — revenue; acquiring title — capital.', 'Replacement of a worn-out part — revenue; improvement for fuel efficiency — capital.', 'Sale of fixed asset — only profit or loss to P&L.'],
            'traps': ['Do not decide by the ledger name ("repairs") — decide by effect on future benefit.', 'Inauguration expenses of a new unit and VRS compensation are revenue, though large.', 'A security deposit is an asset, not an expense.'],
        },
        'quickref': [
            {'k': 'Capital expenditure', 'v': 'Benefit > one period; increases capacity / reduces cost → Balance sheet (asset)'},
            {'k': 'Revenue expenditure', 'v': 'Benefit ≤ current period; maintains capacity → P&L of the year'},
            {'k': 'Five considerations', 'v': 'Nature of business · Recurrence · Purpose · Effect on capacity · Materiality'},
            {'k': 'Profit on sale of asset', 'v': 'Sale proceeds − Book value (only this goes to P&L)'},
            {'k': 'Prepaid expense', 'v': 'Revenue in nature, relates to next period → shown as an asset'},
            {'k': 'Capital receipts', 'v': 'Loans, capital, share premium, sale of fixed assets/investments, deposit refund, insurance claim on asset'},
        ],
        'viva': viva, 'cases': cases,
    }


# ---------- Auto-check data for the Write tab ----------
# Per scheme point: kw (viva-matcher keyword groups, "|" = alternatives) + min (groups needed), nums (figures that must
# appear), rows ([particular keywords, side, amount] for table answers; side may be dr/cr/add/less or a column-header
# keyword such as "capital"), wrong (common wrong statements → remark), ai_only (not checkable offline).
# Per question: extra_ok (may points beyond the model earn credit).
def _item(keys, verdict):
    """item keywords next to its verdict, in either order (one table row / one sentence)"""
    return '|'.join([f'{k} {verdict}' for k in keys] + [f'{verdict} {k}' for k in keys])


AUTO = {
    'q1': {'extra_ok': True,
           's1': {'kw': ['nature business|type business|kind business|nature trade|business nature|line business|dealer', 'furniture|stock trade|dealer|computer|vehicle|car|example|e g'], 'min': 2},
           's2': {'kw': ['recurring|recur|frequent|regular|repetitive|repeated|routine'], 'min': 1},
           's3': {'kw': ['purpose|maintenance|maintain|repair|overhaul', 'maintenance|maintain|repair|productive capacity|increase capacity|capacity|improve|efficiency'], 'min': 2},
           's4': {'kw': ['more than one|one period|several years|long term benefit|enduring|future benefit|future period|current period|accounting period|period benefit|benefit period|earning capacity|revenue generating|earn revenue|generate revenue|lasting benefit'], 'min': 1},
           's5': {'kw': ['material|immaterial|small amount|small items|small value|insignificant|minor amount|petty'], 'min': 1}},
    'q2': {'extra_ok': False,
           's1': {'kw': [_item(['truck', 'overhaul', 'roadworthy', 'second hand', '1'], 'capital'),
                         'working condition|roadworthy|part cost|cost truck|cost asset|ready use|put use|usable|condition use|before use|fit use|cost vehicle'], 'min': 2},
           's2': {'kw': [_item(['new process', 'process', 'power cost', 'power', '2'], 'capital'),
                         'enduring|long term|future|every year|reduce cost|reduces cost|reducing cost|saving|permanent|lasting|several years'], 'min': 2},
           's3': {'kw': [_item(['legal fee', 'legal', 'instalment', 'recover', 'recovery', '3'], 'revenue'),
                         'recurring|normal|routine|no enduring|not increase|no increase|day to day|ordinary|regular|not create'], 'min': 2},
           's4': {'kw': [_item(['shifting', 'shift', 'godown', 'inventory', '4'], 'revenue'),
                         'not add|no enduring|not enduring|not increase|no increase|no benefit|neither|routine|normal|recurring|no value|not improve|no lasting|not create'], 'min': 2},
           's5': {'kw': [_item(['travel', 'travelling', 'traveling', 'director', 'abroad', '5'], 'capital'),
                         'acquire|acquisition|cost plant|part cost|added cost|add cost|purchase plant|buy plant|buying plant|capital asset|cost asset|new plant'], 'min': 2},
           's6': {'kw': [_item(['inauguration', 'inaugural', 'opening ceremony', 'new branch', '6'], 'revenue'),
                         'no enduring|not enduring|no lasting|not lasting|current period|one time|publicity|advertis|attract|not create|no asset|not asset|beyond period|no long term'], 'min': 2},
           's7': {'kw': [_item(['premium', 'share premium', 'securities premium', '7'], 'capital'),
                         'not normal|not operation|reserve|not credited|balance sheet|issue share|not revenue|shareholder|owner|not business operation|not trading'], 'min': 2},
           's8': {'kw': [_item(['wages', 'wage', 'tool', '8'], 'capital'),
                         'asset|several|long|more than one|years|own use|create|construct|cost tool'], 'min': 2}},
    'q3': {'extra_ok': False,
           's1': {'rows': [['furniture', 'capital', 53500]]},
           's2': {'rows': [['licence|license', 'capital', 40000], ['fine|penalty', 'revenue', 3000]]},
           's3': {'rows': [['renewal|next year', 'prepaid', 5000]]},
           's4': {'rows': [['insurance', 'revenue', 7500], ['insurance', 'prepaid', 7500]]},
           's5': {'rows': [['partition', 'capital', 9000]], 'nums': [102500, 10500, 12500]}},
    'q4': {'extra_ok': False,
           's1': {'kw': ['revenue receipt', 'sale goods|sales|sale service|interest|commission|rent|dividend|discount received|fees', 'profit loss|p l|income statement|credited|normal course|ordinary course'], 'min': 3},
           's2': {'kw': ['capital receipt', 'loan|capital introduced|premium|sale fixed asset|sale asset|investment|capital brought|deposit',
                         'not credited|balance sheet|not profit loss|not taken profit|not shown profit|not p l|liabilit|not normal|not revenue nature'], 'min': 3},
           's3': {'kw': ['profit|loss|gain', 'sale|sold|disposal|dispose', 'only profit|profit only|only loss|only gain|difference|book value|carrying amount|written down|wdv'], 'min': 3,
                  'wrong': [{'kw': ['whole sale price profit loss|entire sale proceeds profit loss|sale proceeds credited profit loss|sale price credited profit loss'], 'say': 'Only the profit or loss on sale (sale price − book value) goes to P&L; the sale proceeds themselves are a capital receipt.'}]}},
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
