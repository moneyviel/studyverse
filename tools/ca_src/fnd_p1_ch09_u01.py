"""CA Foundation · Paper 1 Accounting · Chapter 9 Accounts from Incomplete Records (single unit).
Original explanations, names and numbers; scope and topic order follow the ICAI study material (May 2027 onwards)."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p1-ch09-u01'


def two_side(title, left, right, lh='Dr', rh='Cr', note_=None):
    n = max(len(left), len(right))
    rows = []
    for i in range(n):
        l = left[i] if i < len(left) else ('', None)
        r = right[i] if i < len(right) else ('', None)
        rows.append([l[0], inr(l[1]) if l[1] is not None else '', r[0], inr(r[1]) if r[1] is not None else ''])
    tl = round(sum(a for _, a in left if a is not None), 2)
    tr = round(sum(a for _, a in right if a is not None), 2)
    assert tl == tr, (title, tl, tr)
    rows.append(['Total', inr(tl), 'Total', inr(tr)])
    return table([lh, '₹', rh, '₹'], rows, num=[1, 3], total=True, title=title, note=note_)


def stmt(title, rows, note_=None):
    return table(['Particulars', '₹'], [[a, inr(b) if isinstance(b, (int, float)) else b] for a, b in rows], title=title, note=note_)


def ledger(ac, dr, cr):
    """Simple balanced T-account from (part, amt) lists; asserts sides agree."""
    assert sum(a for _, a in dr) == sum(a for _, a in cr), (ac, sum(a for _, a in dr), sum(a for _, a in cr))
    return {'t': 'ledger', 'ac': ac, 'dr': [{'date': '', 'part': p_, 'amt': a} for p_, a in dr], 'cr': [{'date': '', 'part': p_, 'amt': a} for p_, a in cr]}


def build():
    # ============ Illustration 1: capital comparison ============
    c1 = Checks()
    oc = c1.add('6500+48000+125000+62000+40000+80000-(54000+3000)', 'Opening capital (1 April 2025)')
    fu = c1.add('40000-40000*10/100', 'Furniture after 10% depreciation')
    eq = c1.add('80000+30000-(80000*15/100+30000*15/100*6/12)', 'Equipment after depreciation (new item for 6 months)')
    cc = c1.add('9200+71500+148000+79000+36000+95750+2400-(66500+50000+1500)', 'Closing capital (31 March 2026)')
    dr1 = c1.add('12000*12+8000', 'Drawings: cash ₹12,000 a month + goods ₹8,000')
    pr1 = c1.add('323850+152000-60000-304500', 'Profit for 2025-26')
    c1.add('50000*12/100*3/12', 'Interest on bank loan for January–March outstanding')
    SA1 = table(['Particulars', '1 Apr 2025 (₹)', '31 Mar 2026 (₹)'], [
        ['Cash in hand', '6,500', '9,200'], ['Cash at bank', '48,000', '71,500'], ['Stock', '1,25,000', '1,48,000'], ['Debtors', '62,000', '79,000'],
        ['Furniture (2026: less 10% depreciation)', '40,000', inr(fu)], ['Equipment (2026: 80,000 + 30,000 − depreciation 14,250)', '80,000', inr(eq)],
        ['Prepaid insurance', '—', '2,400'], ['Total assets', '3,61,500', inr(441850)],
        ['Less: Creditors', '54,000', '66,500'], ['Less: Outstanding rent', '3,000', '—'], ['Less: Bank loan', '—', '50,000'], ['Less: Interest on loan outstanding', '—', '1,500'],
        ['Capital (assets − liabilities)', inr(oc), inr(cc)]], title='Statements of Affairs of Meenal Boutique (summarised)')
    PR1 = stmt('Statement of Profit for the year to 31 March 2026', [
        ('Capital on 31 March 2026', cc), ('Add: Drawings (cash 1,44,000 + goods 8,000)', '1,52,000'), ('Less: Fresh capital introduced (sale of personal gold)', '(60,000)'),
        ('Adjusted closing capital', 415850), ('Less: Capital on 1 April 2025', '(3,04,500)'), ('Profit for the year', pr1)])

    # ============ Illustration 2: conversion method ============
    c2 = Checks()
    cs = c2.add('(362000+28000+46000+36000+54000+17500+60000+50000+31500)-(22000+485000+40000+3000)', 'Cash sales (balancing figure of cash and bank summary)')
    crs = c2.add('485000+6500+3000+5000+96500-88000', 'Credit sales (balancing figure of total debtors)')
    crp = c2.add('362000+4200+3800+70500-61000', 'Credit purchases (balancing figure of total creditors)')
    ts = c2.add('508000+135000', 'Total sales')
    tp = c2.add('379500+28000', 'Total purchases')
    wg = c2.add('46000-4000+5500', 'Wages for the year')
    rent_b = c2.add('36000*3/4', 'Business share of rent')
    drw = c2.add('60000+36000/4', 'Total drawings (cash + residential share of rent)')
    dep = c2.add('120000*10/100+50000*10/100*6/12', 'Depreciation on machinery')
    gp = c2.add('(643000-5000)+82000-(74000+(407500-3800)+47500)', 'Gross profit')
    np_ = c2.add('194800+4200-(27000+54000+17500+6500+3000+14500)', 'Net profit')
    ocap = c2.add('22000+88000+74000+120000-(61000+4000)', 'Opening capital')
    ccap = c2.add('239000+40000+3000+76500-69000', 'Closing capital')
    CBS = two_side('Cash and Bank Summary (combined)', [
        ('To Balance b/d', 22000), ('To Debtors (collections)', 485000), ('To Capital (fresh capital)', 40000), ('To Capital (interest on private FD)', 3000), ('To Cash sales (balancing figure)', cs)],
        [('By Creditors', 362000), ('By Cash purchases', 28000), ('By Wages', 46000), ('By Rent', 36000), ('By Salaries', 54000), ('By General expenses', 17500),
         ('By Drawings', 60000), ('By Machinery', 50000), ('By Balance c/d', 31500)], 'Receipts', 'Payments')
    TD = ledger('Total Debtors Account', [('To Balance b/d', 88000), ('To Credit sales (balancing figure)', crs)],
                [('By Cash/Bank', 485000), ('By Discount allowed', 6500), ('By Bad debts', 3000), ('By Sales returns', 5000), ('By Balance c/d', 96500)])
    TC = ledger('Total Creditors Account', [('To Cash/Bank', 362000), ('To Discount received', 4200), ('To Purchase returns', 3800), ('To Balance c/d', 70500)],
                [('By Balance b/d', 61000), ('By Credit purchases (balancing figure)', crp)])
    TR = two_side('Trading Account of Rohit Hardware for the year to 31 March 2026', [
        ('To Opening stock', 74000), ('To Purchases 4,07,500 less returns 3,800', 403700), ('To Wages (46,000 − 4,000 + 5,500)', wg), ('To Gross profit c/d', gp)],
        [('By Sales 6,43,000 less returns 5,000', 638000), ('By Closing stock', 82000)])
    PL = two_side('P&L Account for the year to 31 March 2026', [
        ('To Rent (business share 3/4)', rent_b), ('To Salaries', 54000), ('To General expenses', 17500), ('To Discount allowed', 6500), ('To Bad debts', 3000),
        ('To Depreciation on machinery', dep), ('To Net profit transferred to capital', np_)],
        [('By Gross profit b/d', gp), ('By Discount received', 4200)])
    BS2 = two_side('Balance Sheet of Rohit Hardware as at 31 March 2026', [
        ('Capital: opening 2,39,000 + fresh capital 40,000 + FD interest 3,000 + net profit 76,500 − drawings 69,000', ccap), ('Creditors', 70500), ('Outstanding wages', 5500)],
        [('Machinery (1,20,000 + 50,000 − 14,500)', 155500), ('Stock', 82000), ('Debtors', 96500), ('Cash and bank', 31500)], 'Liabilities', 'Assets')

    # ============ Illustration 3: gross profit technique ============
    c3 = Checks()
    cost_sales = c3.add('560000*(100-25)/100', 'Cost of goods sold at 25% gross profit on sales')
    cl_stock = c3.add('85000+436000-420000', 'Estimated closing stock')
    on_sales = c3.add('25/125*100', '25% on cost expressed as % of sales')
    gp_wrong = c3.add('560000*25/100', 'Gross profit if 25% were wrongly taken on sales')
    gp_right = c3.add('560000*25/125', 'Gross profit at 25% on cost')
    cl2 = c3.add('85000+436000-(560000-112000)', 'Closing stock at 25% on cost')
    MC = table(['Item', 'Gross profit 25% on sales', 'Gross profit 25% on cost'], [
        ['Sales', '5,60,000', '5,60,000'], ['Gross profit', inr(gp_wrong), inr(gp_right) + ' (= 1/5 of sales)'],
        ['Cost of goods sold', inr(cost_sales), inr(560000 - gp_right)], ['Opening stock + purchases', '5,21,000', '5,21,000'],
        ['Estimated closing stock', inr(cl_stock), inr(cl2)]], title='Memorandum Trading Account — working both ways')

    # ============ Illustration 4: debtors with bills receivable ============
    c4 = Checks()
    br_recd = c4.add('64000+5000+22000-18000', 'Bills received from debtors (balancing figure of Bills Receivable A/c)')
    cs4 = c4.add('290000+73000+4000+2500+82000-70000-5000', 'Credit sales (balancing figure of Total Debtors A/c)')
    BR = ledger('Bills Receivable Account', [('To Balance b/d', 18000), ('To Debtors — bills received (balancing figure)', br_recd)],
                [('By Cash/Bank — bills collected', 64000), ('By Debtors — bills dishonoured', 5000), ('By Balance c/d', 22000)])
    TD4 = ledger('Total Debtors Account', [('To Balance b/d', 70000), ('To Bills Receivable — dishonoured', 5000), ('To Credit sales (balancing figure)', cs4)],
                 [('By Cash/Bank', 290000), ('By Bills Receivable', br_recd), ('By Discount allowed', 4000), ('By Bad debts', 2500), ('By Balance c/d', 82000)])

    # ============ Q1: income verification ============
    q1 = Checks()
    q1_o = q1.add('12000+60000+45000+200000-(30000+38000)', 'Capital on 1 April 2024')
    q1_c = q1.add('18000+95000+70000+200000+240000-52000', 'Capital on 1 April 2026')
    q1_d = q1.add('15000*24', 'Household drawings for 24 months')
    q1_i = q1.add('571000+360000-249000', 'Income actually earned in the two years')
    q1_x = q1.add('682000-(190000+210000)', 'Income not declared')

    # ============ Q2: Priya Stores ============
    q2 = Checks()
    q2_cl = q2.add('15000+320000+60000-(245000+20000+38000+30000+24000+12000)', 'Closing cash and bank')
    q2_cs = q2.add('320000+3000+2000+61000-52000', 'Credit sales')
    q2_cp = q2.add('245000+2500+41500-34000', 'Credit purchases')
    q2_gp = q2.add('(334000+60000)+53000-(46000+255000+20000)', 'Gross profit')
    q2_np = q2.add('126000+2500-((38000-6000)+(30000+2500)+3000+2000+(30000+12000)*10/100)', 'Net profit')
    q2_oc = q2.add('15000+52000+46000+30000-34000', 'Opening capital')
    q2_cc = q2.add('109000+54800-(24000+6000)', 'Closing capital')
    Q2T = two_side('Trading and P&L Account of Priya Stores for the year to 31 March 2026', [
        ('To Opening stock', 46000), ('To Purchases (credit 2,55,000 + cash 20,000)', 275000), ('To Gross profit c/d', q2_gp),
        ('To Expenses (38,000 − 6,000 household)', 32000), ('To Salaries (30,000 + 2,500 outstanding)', 32500), ('To Discount allowed', 3000), ('To Bad debts', 2000),
        ('To Depreciation on furniture (42,000 × 10%)', 4200), ('To Net profit', q2_np)],
        [('By Sales (credit 3,34,000 + cash 60,000)', 394000), ('By Closing stock', 53000), ('By Gross profit b/d', q2_gp), ('By Discount received', 2500)],
        'Dr', 'Cr', note_='Trading and P&L shown in one table: the gross profit appears once as "c/d" (debit) and once as "b/d" (credit), so the two totals still agree.')
    Q2B = two_side('Balance Sheet of Priya Stores as at 31 March 2026', [
        ('Capital: 1,09,000 + net profit 54,800 − drawings 30,000', q2_cc), ('Creditors', 41500), ('Outstanding salaries', 2500)],
        [('Furniture (30,000 + 12,000 − 4,200)', 37800), ('Stock', 53000), ('Debtors', 61000), ('Cash and bank', q2_cl)], 'Liabilities', 'Assets')

    # ============ Q4: creditors with bills payable ============
    q4 = Checks()
    q4_bp = q4.add('48000+20000-15000', 'Bills payable accepted during the year')
    q4_cp = q4.add('210000+53000+3500+4500+55000-42000', 'Credit purchases')
    q4_tp = q4.add('284000+26000', 'Total purchases')
    Q4BP = ledger('Bills Payable Account', [('To Cash/Bank — bills paid', 48000), ('To Balance c/d', 20000)],
                  [('By Balance b/d', 15000), ('By Creditors — bills accepted (balancing figure)', q4_bp)])
    Q4TC = ledger('Total Creditors Account', [('To Cash/Bank', 210000), ('To Bills Payable', q4_bp), ('To Discount received', 3500), ('To Purchase returns', 4500), ('To Balance c/d', 55000)],
                  [('By Balance b/d', 42000), ('By Credit purchases (balancing figure)', q4_cp)])

    # ============ Case ============
    k = Checks()
    k_cs = k.add('(150000+12000+9000+18000+6000)-(5000+124000)', 'cash sales')
    k_cr = k.add('124000+1500+2000+47000-38000', 'credit sales')
    k_tot = k.add('136500+66000', 'total sales')
    k_gp = k.add('202500*20/100', 'gross profit at 20% on sales')

    concepts = [
        {'id': 'c1', 'title': 'Why records are incomplete — the "single entry" situation',
         'body': ['Many small traders and some partnership firms never keep full double-entry books. They usually note cash received and paid, keep personal accounts of customers and suppliers, and rely on the bank statement. Records can also be incomplete because books were destroyed (for example in a fire) or because a key figure such as stock is unknown.',
                  '"Single entry" is not a real system: it is simply incomplete double entry — some transactions are recorded in full, some only on one side, and some not at all. The accountant\'s job is to connect the scraps of information and finish the accounts.',
                  'Features: unscientific and unsystematic; real and nominal accounts are generally missing; business and personal cash are mixed; no uniformity between firms; a trial balance cannot be drawn up, so arithmetical accuracy cannot be proved; profit and financial position are only estimates.'],
         'analogy': 'It is like a diary in which you note who owes you money and how much cash you spent, but never what you bought or sold. You can still guess how the month went — but only roughly.',
         'work': 'CAs regularly prepare accounts of small shops, freelancers and family businesses from bank statements, bill files and the owner\'s notebook — and tax authorities use the same techniques to test whether declared income is believable.'},
        {'id': 'c2', 'title': 'Types of single entry',
         'body': ['Pure single entry: only personal accounts are kept — nothing about cash, sales or purchases. It exists mostly in theory.',
                  'Simple single entry: personal accounts and a cash book. Cash book items are posted only to personal accounts; nothing else is in the ledger.',
                  'Quasi single entry: personal accounts, a cash book and some subsidiary books (typically a sales book, purchases book and bills book), plus scattered notes on major expenses like wages and rent. Discounts are usually entered only in personal accounts. This is the most common form used as a substitute for double entry.'],
         'analogy': 'Pure = only an IOU list; simple = IOU list + cash diary; quasi = IOU list + cash diary + sales and purchase registers.',
         'work': 'Before quoting a fee for "writing up the books", a CA first finds out which of these records the client has — it decides whether the conversion method is possible or only the statement of affairs method.'},
        {'id': 'c3', 'title': 'Capital comparison (net worth / statement of affairs) method',
         'body': ['When only lists of assets and liabilities can be obtained, profit is found by comparing capital at two dates: Profit = Closing capital + Drawings − Fresh capital introduced − Opening capital. A negative answer is a loss.',
                  'Drawings are added back because they reduced closing capital without being a business loss; fresh capital is deducted because it raised closing capital without being a business profit.',
                  'Capital at each date = assets − liabilities, shown in a Statement of Affairs. Sources: cash book (cash), bank pass book/statement (bank), personal ledger (debtors, creditors), physical count and valuation (stock), and a list of fixed assets at cost less reasonable depreciation.',
                  'Remember outstanding expenses (liability), prepaid expenses and accrued income (assets), and depreciation on fixed assets in the closing statement.'],
         'analogy': 'Weigh yourself on 1 April and again on 31 March; adjust for the extra meals you were given (fresh capital) and the gym sessions you skipped (drawings) — the rest is the real change.',
         'work': 'Income-tax officers and banks use the net-worth approach: if a person\'s wealth grew far more than his declared income plus savings would allow, the gap points to undisclosed income.'},
        {'id': 'c4', 'title': 'Statement of Affairs vs Balance Sheet',
         'body': ['Both list assets and liabilities, but they are built differently and serve different purposes.'],
         'blocks': [table(['Basis', 'Statement of Affairs', 'Balance Sheet'], [
             ['Source', 'Partly records, partly estimates, inquiries and memory', 'Ledger balances under complete double entry, backed by documents'],
             ['Capital', 'A balancing figure (assets − liabilities)', 'Taken from the capital account in the ledger'],
             ['Omissions', 'Assets or liabilities can easily be left out without anyone noticing', 'An omission is noticed because the two sides will not agree'],
             ['Valuation', 'Often arbitrary; no stated method', 'On a recognised basis (e.g. cost less depreciation), changes disclosed'],
             ['Purpose', 'To find capital at the beginning and end of a period', 'To show the financial position on a date'],
         ])],
         'analogy': 'A balance sheet is a photograph from the official camera; a statement of affairs is a sketch drawn from memory and a few notes.',
         'work': 'When a client\'s figures are estimates, a CA\'s report must say so; presenting a statement of affairs as if it were an audited balance sheet would mislead lenders.'},
        {'id': 'c5', 'title': 'Conversion method: completing double entry from the records',
         'body': ['Better than the net-worth method whenever enough data exist: rebuild the double entry and prepare a proper trading and profit and loss account and balance sheet.',
                  'Steps: (1) Find opening capital with an opening statement of affairs. (2) Prepare a cash and bank summary; a missing figure (often cash sales or closing cash) is the balancing figure. (3) Prepare Total Debtors and Total Creditors accounts (and Bills Receivable / Bills Payable accounts) to find credit sales, credit purchases or missing balances as balancing figures. (4) Post the remaining items to nominal and real accounts, make adjustments, and draw up a trial balance and the final accounts.',
                  'Total Debtors: Dr — opening balance, credit sales, bills dishonoured; Cr — cash received, discount allowed, sales returns, bad debts, bills received, closing balance. Total Creditors: Dr — cash paid, discount received, purchase returns, bills accepted, closing balance; Cr — opening balance, credit purchases, bills payable dishonoured.',
                  'Treatments while converting: private receipts paid into the business (interest on personal investments, legacies, owner\'s money) are credited to capital; personal payments are drawings; unexplained cash shortages are drawings; expenses shared by home and business (rent of a shop-cum-house) are split on a fair basis such as floor area.'],
         'analogy': 'You have a jigsaw with a few pieces missing. Each account (cash, debtors, creditors) is a frame; once every other piece is in place, the shape of the hole tells you the missing piece.',
         'work': 'Bookkeepers working from bank statements do exactly this every year for small clients: the debtors account reveals sales that never went through the bank, which matters for both GST and income tax.'},
        {'id': 'c6', 'title': 'Spotting drawings and fresh capital',
         'body': ['Typical hidden drawings: residential share of a common rent, electricity or telephone bill; the owner\'s life insurance premium paid by the business; household expenses or private loans repaid from business cash; personal gifts; goods or services taken for personal use; collections from customers spent directly on personal needs.',
                  'Typical hidden fresh capital: maturity proceeds of the owner\'s life insurance policy put into the business; interest or dividends on the owner\'s private investments credited to the business account; rent from non-business property paid in; business creditors paid from the owner\'s personal money.',
                  'Getting these right matters: wrongly treating drawings as expenses understates profit; wrongly treating fresh capital as sales overstates it.'],
         'analogy': 'Think of two wallets — "shop" and "home". Every rupee that crosses from shop to home is drawings; every rupee crossing from home to shop is fresh capital.',
         'work': 'In tax scrutiny, the assessee must explain every large credit in the business bank account; a maturity receipt from an insurance policy is fresh capital, not unexplained income — but it needs documentary proof.'},
        {'id': 'c7', 'title': 'Gross profit technique for missing stock or sales',
         'body': ['When the business earns a steady gross profit percentage, a memorandum trading account fills in a missing figure: Closing stock = Opening stock + Purchases (+ direct expenses) − Cost of goods sold, where Cost of goods sold = Net sales − Gross profit.',
                  'Convert carefully: gross profit of x% on cost = x/(100 + x) of sales. So 25% on cost = 20% of sales; 20% on cost = 1/6 of sales; 33⅓% on cost = 25% of sales.',
                  'Use net sales (after returns) and net purchases (after returns); carriage inwards and other direct expenses form part of cost.'],
         'analogy': 'If every ₹100 of goods you sell earns ₹20, then from total sales you can work back to how much stock must have left the shelves.',
         'work': 'The same technique estimates stock lost in a fire or theft and checks whether a client\'s physical stock figure is plausible.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Profit by capital comparison with depreciation, fresh capital and drawings', 'difficulty': 'moderate', 'minutes': 15,
         'q': ('Meenal runs a boutique without proper books. On 1 April 2025: cash ₹6,500; bank ₹48,000; stock ₹1,25,000; debtors ₹62,000; furniture ₹40,000; equipment ₹80,000; creditors ₹54,000; outstanding rent ₹3,000. '
               'On 31 March 2026: cash ₹9,200; bank ₹71,500; stock ₹1,48,000; debtors ₹79,000; prepaid insurance ₹2,400; creditors ₹66,500; a bank loan of ₹50,000 taken on 1 January 2026 at 12% p.a. (no interest paid yet). '
               'She bought more equipment for ₹30,000 on 1 October 2025. Depreciate furniture at 10% and equipment at 15% p.a. She withdrew ₹12,000 a month and took goods costing ₹8,000 for her family; she brought in ₹60,000 from the sale of her personal gold. Find the profit for 2025-26.'),
         'solution': [SA1, PR1, wn('Workings', f'Equipment depreciation: 80,000 × 15% = 12,000; 30,000 × 15% × 6/12 = 2,250; total 14,250. Interest outstanding on loan: 50,000 × 12% × 3/12 = ₹1,500 (a liability). Drawings ₹{inr(dr1)}.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Conversion into double entry — full final accounts', 'difficulty': 'hard', 'minutes': 30,
         'q': ('Rohit Hardware keeps only a cash book (cash and bank combined) and personal ledgers. Summary for 2025-26 — receipts: opening balance ₹22,000; collections from debtors ₹4,85,000; fresh capital ₹40,000; interest on Rohit\'s private fixed deposit credited to the business account ₹3,000; cash sales — not recorded. '
               'Payments: creditors ₹3,62,000; cash purchases ₹28,000; wages ₹46,000; rent ₹36,000 (one-fourth of the premises is Rohit\'s residence); salaries ₹54,000; general expenses ₹17,500; drawings ₹60,000; machinery bought on 1 October 2025 ₹50,000; closing balance ₹31,500. '
               'Balances (1 April 2025 / 31 March 2026): debtors ₹88,000 / ₹96,500; creditors ₹61,000 / ₹70,500; stock ₹74,000 / ₹82,000; machinery ₹1,20,000 / ?; wages outstanding ₹4,000 / ₹5,500. '
               'Other: discount allowed ₹6,500; discount received ₹4,200; bad debts ₹3,000; sales returns ₹5,000; purchase returns ₹3,800. Depreciate machinery at 10% p.a. Prepare the Trading and P&L Account and the Balance Sheet.'),
         'solution': [CBS, TD, TC, TR, PL, BS2,
                      wn('Key figures', f'Cash sales ₹{inr(cs)}; credit sales ₹{inr(crs)}; total sales ₹{inr(ts)}. Credit purchases ₹{inr(crp)}; total purchases ₹{inr(tp)}. Opening capital = assets 3,04,000 − liabilities 65,000 = ₹{inr(ocap)}. The FD interest is Rohit\'s private income paid into the business — credited to capital, not to P&L. Drawings = 60,000 + residential rent 9,000 = ₹{inr(drw)}.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Estimating closing stock with the gross profit ratio', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'Jai\'s stock was not counted on 31 March 2026. Opening stock ₹85,000, purchases ₹4,36,000, sales ₹5,60,000. Estimate closing stock if the gross profit is (a) 25% on sales and (b) 25% on cost.',
         'solution': [MC, wn('Conversion', f'25% on cost = 25/125 = {inr(on_sales)}% of sales. Using 25% "on sales" when the business means "on cost" overstates gross profit by ₹{inr(gp_wrong - gp_right)} and therefore overstates the estimated closing stock by the same amount (₹1,01,000 instead of ₹73,000).')],
         'checks': c3},
        {'id': 'i4', 'title': 'Credit sales through Debtors and Bills Receivable accounts', 'difficulty': 'moderate', 'minutes': 10,
         'q': 'From these figures for 2025-26 find the bills received from customers and the credit sales: debtors — opening ₹70,000, closing ₹82,000; bills receivable — opening ₹18,000, closing ₹22,000; cash received from debtors ₹2,90,000; bills collected on maturity ₹64,000; bills dishonoured ₹5,000; discount allowed ₹4,000; bad debts ₹2,500.',
         'solution': [BR, TD4, p(f'Work the Bills Receivable account first: it gives bills received ₹{inr(br_recd)}, which then goes to the credit of Total Debtors. Credit sales = ₹{inr(cs4)}.'),
                      note('A dishonoured bill is debited back to debtors (the customer owes again) and credited to Bills Receivable.')],
         'checks': c4},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Preparing a kirana store\'s accounts for its loan file', 'role': 'Junior accountant at a CA firm',
         'situation': 'A grocery owner needs audited-style accounts for a bank loan. He has a sales notebook for credit customers, bank statements, supplier bills and a rough cash diary. No sales total is recorded for cash customers.',
         'steps': ['List opening assets and liabilities (from last year\'s return and the owner\'s confirmation) to find opening capital.',
                   'Prepare a cash and bank summary; the shortfall on the receipts side is the probable cash sales.',
                   'Build Total Debtors and Total Creditors accounts from the notebook and supplier statements to find credit sales and purchases.',
                   'Separate household items paid from the shop (school fees, home electricity) as drawings.',
                   'Prepare the trading and profit and loss account and balance sheet; compare the gross profit ratio with similar shops as a reasonableness check.'],
         'takeaway': 'Every balancing figure is an inference — test it. A gross profit far above the trade average often means some cash expenses or drawings were missed.',
         'think': 'The cash summary shows cash sales of ₹14 lakh but the GST returns show ₹9 lakh of cash sales. What do you do?',
         'answer': 'Do not simply accept either figure. Look for unrecorded receipts (fresh capital, loans, private income) that were wrongly treated as sales, and discuss the gap with the client — under-reported sales also have tax consequences.'},
        {'id': 'j2', 'title': 'Net-worth test in a tax scrutiny', 'role': 'Tax assistant preparing a reply to a scrutiny notice',
         'situation': 'The assessing officer says a trader\'s net worth rose by ₹9 lakh in two years while declared income was only ₹5 lakh, and proposes to add the difference as undisclosed income.',
         'steps': ['Rebuild statements of affairs on both dates with the client\'s documents.',
                   'Add realistic household drawings for the period; the officer\'s estimate may be too high or too low.',
                   'Identify fresh capital with proof: gifts from relatives, insurance maturity, sale of an inherited asset.',
                   'Recompute the income by capital comparison and compare it with declared income.'],
         'takeaway': 'The capital comparison method cuts both ways: properly documented fresh capital and realistic drawings can explain an apparent gap.',
         'think': 'Why are household expenses added back when testing declared income?',
         'answer': 'They were paid out of income, so they reduced the closing net worth. Unless added back, the income earned would be understated.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'Under which type of single entry are personal accounts, a cash book and some subsidiary books maintained?', 'options': ['Quasi single entry', 'Pure single entry', 'Simple single entry', 'Double entry'], 'answer': 0, 'explain': "Quasi single entry is the most developed form: besides personal accounts and a cash book, the trader keeps some subsidiary books such as sales, purchases and bills books. Simple single entry keeps only personal accounts and a cash book; pure single entry keeps personal accounts alone. The trap is 'simple single entry', which lacks the subsidiary books. In practice: many small Indian traders fall in this category — a cash book and party ledgers, often in a basic app, but no full double entry.", 'topic': "Types of single entry", 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'Opening capital ₹2,40,000; closing capital ₹2,95,000; drawings ₹36,000; fresh capital introduced ₹25,000. Profit for the year is:', 'options': ['₹66,000', '₹91,000', '₹44,000', '₹55,000'], 'answer': 0, 'check': '295000+36000-25000-240000', 'explain': "Profit = closing capital + drawings − fresh capital − opening capital = 2,95,000 + 36,000 − 25,000 − 2,40,000 = ₹66,000. Drawings are added back because they reduced capital without being a loss; fresh capital is deducted because it raised capital without being a profit. The trap ₹91,000 forgets to deduct the fresh capital. In practice: tax officers use this net-worth comparison to estimate income when a small trader has no proper books.", 'topic': "Capital comparison (net worth / statement of affairs) method", 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm3', 'q': 'In a Statement of Affairs, capital is:', 'options': ['The balancing figure (assets − liabilities)', 'Taken from the capital account in the ledger', 'Always equal to the opening capital', 'Not shown'], 'answer': 0, 'explain': "A Statement of Affairs is prepared from incomplete records, so there is no reliable capital account to copy. Capital is found as the balancing figure — total assets minus total liabilities. The trap is 'taken from the capital account in the ledger'; that is how a Balance Sheet gets its capital, because complete double-entry books exist. In practice: a CA helping a small shopkeeper apply for a bank loan first builds a statement of affairs from his bank statements, stock list and party balances.", 'topic': "Statement of Affairs vs Balance Sheet", 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'Debtors: opening ₹45,000, closing ₹52,000; cash received ₹3,10,000; discount allowed ₹4,000; sales returns ₹6,000; bad debts ₹3,000. Credit sales are:', 'options': ['₹3,30,000', '₹3,16,000', '₹3,23,000', '₹3,17,000'], 'answer': 0, 'check': '310000+4000+6000+3000+52000-45000', 'explain': "Rebuild the total debtors account. Credit side: cash received 3,10,000 + discount 4,000 + sales returns 6,000 + bad debts 3,000 + closing debtors 52,000 = ₹3,75,000. Debit side has opening debtors 45,000, so credit sales (the balancing figure) = 3,75,000 − 45,000 = ₹3,30,000. The trap ₹3,17,000 counts only cash received, omitting discount, returns and bad debts. In practice: when a client's sales register is incomplete, accountants reconstruct sales from the debtors' movement and bank receipts.", 'topic': "Conversion method: completing double entry from the records", 'concept': 'c5', 'difficulty': 'moderate'},
        {'id': 'm5', 'q': 'Sales are ₹6,00,000 and gross profit is 20% on cost. Gross profit is:', 'options': ['₹1,00,000', '₹1,20,000', '₹1,50,000', '₹80,000'], 'answer': 0, 'check': '600000*20/120', 'explain': "Gross profit of 20% on cost means cost 100, profit 20, sales 120. So profit is 20/120 = 1/6 of sales: 6,00,000 × 1/6 = ₹1,00,000. The trap ₹1,20,000 applies 20% directly to sales, which is the rate on cost, not on selling price. In practice: retailers often quote markup on cost while accountants work with margin on sales, so converting between the two is a daily skill.", 'topic': "Gross profit technique for missing stock or sales", 'concept': 'c7', 'difficulty': 'moderate'},
        {'id': 'm6', 'q': 'Maturity proceeds of the proprietor\'s life insurance policy deposited in the business bank account should be treated as:', 'options': ['Fresh capital introduced', 'Business income', 'Cash sales', 'A liability of the business'], 'answer': 0, 'explain': "Maturity proceeds of the proprietor's personal life insurance policy are his private money. When deposited in the business account, they are fresh capital introduced and credited to his capital account. The trap is treating them as business income or sales, which would overstate profit. In practice: when reconstructing accounts, a CA asks the owner to explain large unusual bank credits — LIC maturities, gifts or loans — so they are not taxed as business receipts.", 'topic': "Spotting drawings and fresh capital", 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm7', 'q': 'Rent of ₹48,000 is paid for premises, one-third of which is used as the owner\'s residence. The amount charged to the profit and loss account is:', 'options': ['₹32,000', '₹48,000', '₹16,000', '₹36,000'], 'answer': 0, 'check': '48000*2/3', 'explain': "Only the business share of rent is a business expense. The owner lives in one-third, so the business uses two-thirds: 48,000 × 2/3 = ₹32,000 charged to profit and loss. The residential one-third, ₹16,000, is drawings. The trap ₹48,000 charges the owner's housing cost to the business. In practice: shop-cum-residence arrangements are very common in Indian towns, and the income-tax law also allows only the business part of such expenses.", 'topic': "Conversion method: completing double entry from the records", 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm8', 'q': 'Which statement about books kept on single entry is correct?', 'options': ['A trial balance cannot be prepared from them', 'Nominal accounts are always fully maintained', 'Profit worked out is exact', 'The system is uniform for all firms'], 'answer': 0, 'explain': "Under single entry, only some accounts (mainly cash and personal accounts) are kept, so the two aspects of every transaction are not recorded. Without a complete ledger, a trial balance cannot be prepared. The trap 'profit worked out is exact' is wrong — profit under single entry is only an estimate. In practice: a small trader with only a cash diary cannot produce a trial balance, so a CA reconstructs the accounts before filing his return.", 'topic': "Why records are incomplete — the \"single entry\" situation", 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm9', 'q': 'Cash and bank summary: opening balance ₹8,000; collections from debtors ₹1,90,000; payments ₹2,40,000; closing balance ₹12,000. Cash sales (not recorded) must be:', 'options': ['₹54,000', '₹62,000', '₹38,000', '₹46,000'], 'answer': 0, 'check': '240000+12000-8000-190000', 'explain': "In the cash summary, total payments side = payments 2,40,000 + closing balance 12,000 = ₹2,52,000. Known receipts = opening balance 8,000 + collections 1,90,000 = ₹1,98,000. The missing receipt, cash sales, = 2,52,000 − 1,98,000 = ₹54,000. The trap ₹62,000 forgets the opening balance, which was also available to make payments. In practice: retailers who don't record counter sales have them reconstructed this way from the cash and bank movement.", 'topic': "Conversion method: completing double entry from the records", 'concept': 'c5', 'difficulty': 'moderate'},
        {'id': 'm10', 'q': 'Opening stock ₹40,000; purchases ₹2,60,000; sales ₹3,20,000; gross profit 25% on sales. Closing stock is:', 'options': ['₹60,000', '₹40,000', '₹44,000', '₹20,000'], 'answer': 0, 'check': '40000+260000-320000*75/100', 'explain': "Gross profit is 25% on sales, so cost of sales = 3,20,000 × 75% = ₹2,40,000. Closing stock = opening stock 40,000 + purchases 2,60,000 − cost of sales 2,40,000 = ₹60,000. The trap is taking 25% as a markup on cost (cost = 2,56,000, stock 44,000). In practice: after a fire or theft, insurers and accountants use this gross-profit method to estimate the stock that should have been on hand.", 'topic': "Gross profit technique for missing stock or sales", 'concept': 'c7', 'difficulty': 'moderate'},
        {'id': 'm11', 'q': 'Creditors: opening ₹30,000, closing ₹36,000; cash paid ₹1,80,000; bills payable accepted ₹20,000; discount received ₹2,000. Credit purchases are:', 'options': ['₹2,08,000', '₹1,96,000', '₹1,88,000', '₹2,02,000'], 'answer': 0, 'check': '180000+20000+2000+36000-30000', 'explain': "Rebuild the total creditors account. Debit side: cash paid 1,80,000 + bills payable accepted 20,000 + discount received 2,000 + closing creditors 36,000 = ₹2,38,000. Less opening creditors 30,000 on the credit side: credit purchases = ₹2,08,000. The trap ₹1,88,000 forgets that accepting bills payable also reduces creditors. In practice: when purchase invoices are missing, accountants rebuild purchases from supplier payments and balance confirmations.", 'topic': "Conversion method: completing double entry from the records", 'concept': 'c5', 'difficulty': 'hard'},
        {'id': 'm12', 'q': 'Which of these is NOT a drawing?', 'options': ['Wages paid to shop staff from business cash', 'Owner\'s life insurance premium paid from business cash', 'Goods taken home by the owner', 'Residential share of a common electricity bill'], 'answer': 0, 'explain': "Wages paid to shop staff are a normal business expense charged to profit and loss. The owner's personal life insurance premium, goods taken home and the residential share of electricity all benefit the owner personally, so they are drawings. The trap is the residential electricity share — it is drawings even though it is paid as part of a business bill. In practice: tax audits of proprietors often find personal expenses booked as business costs, and such items are disallowed.", 'topic': "Spotting drawings and fresh capital", 'concept': 'c6', 'difficulty': 'core'},
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
         'q': ('Harish, a trader, declared income of ₹1,90,000 for 2024-25 and ₹2,10,000 for 2025-26. On 1 April 2024 his business had: cash ₹12,000; stock ₹60,000; debtors ₹45,000; shop premises ₹2,00,000; loan from a friend ₹30,000; creditors ₹38,000. '
               'On 1 April 2026: cash ₹18,000; stock ₹95,000; debtors ₹70,000; shop premises ₹2,00,000; delivery van ₹2,40,000; creditors ₹52,000 (the friend\'s loan was repaid). His household expenses were ₹15,000 a month throughout. Is his declared income reasonable? Show workings.'),
         'model': [table(['Particulars', '1 Apr 2024 (₹)', '1 Apr 2026 (₹)'], [
             ['Cash', '12,000', '18,000'], ['Stock', '60,000', '95,000'], ['Debtors', '45,000', '70,000'], ['Shop premises', '2,00,000', '2,00,000'], ['Delivery van', '—', '2,40,000'],
             ['Total assets', '3,17,000', '6,23,000'], ['Less: Loan from friend', '30,000', '—'], ['Less: Creditors', '38,000', '52,000'], ['Capital', inr(q1_o), inr(q1_c)]], title='Statements of Affairs'),
             stmt('Income for the two years', [('Capital on 1 April 2026', q1_c), ('Add: Household drawings (15,000 × 24)', q1_d), ('Less: Capital on 1 April 2024', '(2,49,000)'),
                                               ('Income earned in two years', q1_i), ('Less: Income declared (1,90,000 + 2,10,000)', '(4,00,000)'), ('Income not declared', q1_x)]),
             p(f'Conclusion: on these figures Harish earned ₹{inr(q1_i)} in two years but declared only ₹4,00,000, so ₹{inr(q1_x)} appears undisclosed unless he can show fresh capital (gifts, loans, sale of private assets) for it.')],
         'checks': q1,
         'scheme': [{'id': 's1', 'pt': 'Opening capital ₹2,49,000 via statement of affairs', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's2', 'pt': 'Closing capital ₹5,71,000 (van included, loan removed)', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Drawings ₹3,60,000 added back; income ₹6,82,000', 'm': 1, 'skill': 'computation'},
                    {'id': 's4', 'pt': 'Comparison with declared income and conclusion (₹2,82,000 undisclosed)', 'm': 1, 'skill': 'conclusion'}],
         'remarks': ['Candidates who forgot to add back household expenses concluded wrongly that Harish had over-declared income.', 'A clear one-line conclusion is expected — the question asks whether the declared income is reasonable.'],
         'mistakes': ['Deducting drawings instead of adding them back.', 'Leaving the repaid loan in the closing statement.', 'Taking drawings for 12 months instead of 24.'],
         'tips': ['Prepare both statements of affairs side by side in one table — it saves time.', 'End with a conclusion sentence; it carries a mark.']},
        {'id': 'q2', 'marks': 10, 'minutes': minutes(10), 'difficulty': 'hard', 'pad': 'table',
         'q': ('Priya Stores keeps incomplete records. Cash and bank summary for 2025-26: opening balance ₹15,000; received from debtors ₹3,20,000; cash sales ₹60,000; paid to creditors ₹2,45,000; cash purchases ₹20,000; expenses ₹38,000 (including Priya\'s household electricity ₹6,000); salaries ₹30,000; drawings ₹24,000; furniture bought on 1 April 2025 ₹12,000. '
               'Balances (1 April 2025 / 31 March 2026): debtors ₹52,000 / ₹61,000; creditors ₹34,000 / ₹41,500; stock ₹46,000 / ₹53,000; furniture ₹30,000 / ?; salaries outstanding nil / ₹2,500. Discount allowed ₹3,000, discount received ₹2,500, bad debts ₹2,000. Depreciate furniture at 10%. '
               'Prepare the Trading and P&L Account for the year to 31 March 2026 and the Balance Sheet on that date.'),
         'model': [wn('WN 1 — Opening capital', f'Cash 15,000 + debtors 52,000 + stock 46,000 + furniture 30,000 − creditors 34,000 = ₹{inr(q2_oc)}.'),
                   wn('WN 2 — Closing cash', f'Receipts 3,95,000 − payments 3,69,000 = ₹{inr(q2_cl)}.'),
                   wn('WN 3 — Credit sales and purchases', f'Credit sales = 3,20,000 + 3,000 + 2,000 + 61,000 − 52,000 = ₹{inr(q2_cs)}. Credit purchases = 2,45,000 + 2,500 + 41,500 − 34,000 = ₹{inr(q2_cp)}.'),
                   Q2T, Q2B],
         'checks': q2,
         'scheme': [{'id': 's1', 'pt': 'Opening capital ₹1,09,000', 'm': 1, 'skill': 'computation'},
                    {'id': 's2', 'pt': 'Closing cash and bank ₹26,000', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Credit sales ₹3,34,000 through Total Debtors', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's4', 'pt': 'Credit purchases ₹2,55,000 through Total Creditors', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's5', 'pt': 'Trading account — gross profit ₹1,26,000', 'm': 1.5, 'skill': 'presentation'},
                    {'id': 's6', 'pt': 'Household electricity as drawings; salary outstanding added; depreciation ₹4,200', 'm': 1.5, 'skill': 'classification'},
                    {'id': 's7', 'pt': 'Net profit ₹54,800', 'm': 0.5, 'skill': 'computation'},
                    {'id': 's8', 'pt': 'Balance sheet with capital ₹1,33,800, totals ₹1,77,800', 'm': 1.5, 'skill': 'balancing'}],
         'remarks': ['Well-prepared candidates showed the total debtors and creditors accounts as working notes and earned step marks even where later figures went wrong.',
                     'The household electricity bill was frequently left inside expenses, overstating expenses and understating drawings.'],
         'mistakes': ['Forgetting cash sales/cash purchases when totalling sales and purchases.', 'Depreciating only the opening furniture.', 'Omitting outstanding salary from the balance sheet.'],
         'tips': ['Order of work: opening capital → cash summary → debtors → creditors → final accounts.', 'Label every balancing figure clearly in the working accounts.']},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
         'q': 'Distinguish between a Statement of Affairs and a Balance Sheet (any four points).',
         'model': [table(['Basis', 'Statement of Affairs', 'Balance Sheet'], [
             ['Source of figures', 'Incomplete records, estimates and inquiries', 'Ledger balances under double entry'],
             ['Capital', 'Balancing figure', 'Taken from the capital account'],
             ['Omissions', 'Difficult to detect', 'Detected because totals will not agree'],
             ['Purpose', 'To ascertain opening/closing capital', 'To show the financial position'],
             ['Valuation', 'Often arbitrary', 'On recognised, disclosed bases']])],
         'scheme': [{'id': f's{i}', 'pt': t, 'm': 1, 'skill': 'concept'} for i, t in enumerate(['Source of figures', 'Capital — balancing figure vs ledger', 'Omissions', 'Purpose or valuation'], 1)],
         'remarks': ['Tabular answers with matched pairs score best.', 'Several candidates wrote only the meaning of each statement without contrasting them.'],
         'mistakes': ['Saying both are prepared under double entry.', 'Calling the statement of affairs a balance sheet of a sole trader.'],
         'tips': ['Four rows, one contrast per row — no long paragraphs needed.']},
        {'id': 'q4', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'ledger',
         'q': 'From the following, find the total purchases for 2025-26: creditors — opening ₹42,000, closing ₹55,000; bills payable — opening ₹15,000, closing ₹20,000; cash paid to creditors ₹2,10,000; bills payable paid on maturity ₹48,000; discount received ₹3,500; purchase returns ₹4,500; cash purchases ₹26,000.',
         'model': [Q4BP, Q4TC, p(f'Bills accepted ₹{inr(q4_bp)}; credit purchases ₹{inr(q4_cp)}; total purchases = {inr(q4_cp)} + 26,000 = ₹{inr(q4_tp)}.')],
         'checks': q4,
         'scheme': [{'id': 's1', 'pt': 'Bills Payable account — bills accepted ₹53,000', 'm': 2, 'skill': 'posting'},
                    {'id': 's2', 'pt': 'Total Creditors account with bills, discount, returns', 'm': 2, 'skill': 'posting'},
                    {'id': 's3', 'pt': 'Total purchases ₹3,10,000 (credit + cash)', 'm': 1, 'skill': 'computation'}],
         'remarks': ['Candidates who tried to find credit purchases before bills accepted got stuck; the bills account must be done first.'],
         'mistakes': ['Debiting creditors with bills paid on maturity (₹48,000) instead of bills accepted.', 'Forgetting cash purchases in the final total.'],
         'tips': ['When bills are given, always open the bills account first.']},
    ]

    viva = [
        V('v1', 'What do we mean by single entry system, and what are its main features?',
          'Single entry is not really a system; it is incomplete double entry, where some transactions are recorded fully, some only on one side and some not at all. Usually only cash and personal accounts are kept and real and nominal accounts are missing. Business and personal cash get mixed, there is no uniformity, a trial balance cannot be prepared, and the profit worked out is only an estimate.',
          [P('p1', 'Incomplete double entry — not a proper system', 3, 'incomplete|not complete|not proper|improper|not a system|not really a system|partly|partial'),
           P('p2', 'Usually only cash book and personal accounts; real and nominal accounts missing', 3, 'personal', 'cash', 'nominal|real', min=2),
           P('p3', 'No trial balance; profit only an estimate', 4, 'trial balance', 'estimate|not accurate|inaccurate|not exact|approximate|rough', min=1)], 'c1'),
        V('v2', 'Name and explain the three types of single entry.',
          'In pure single entry only personal accounts are kept. In simple single entry personal accounts and a cash book are kept. In quasi single entry personal accounts, a cash book and some subsidiary books like the sales book, purchases book and bills book are kept; this is the form most commonly used.',
          [P('p1', 'Pure — only personal accounts', 3, 'pure only personal|pure entry only personal|pure keep only personal|pure entry keep only personal|pure personal account only|pure entry personal account only|pure just personal|pure maintain only personal|pure only personal account maintain'),
           P('p2', 'Simple — personal accounts and cash book', 3, 'simple personal account cash book|simple entry personal account cash book|simple entry keep personal account cash book|simple keep personal account cash book|simple cash book|simple entry cash book|simple personal cash book|simple personal account cashbook'),
           P('p3', 'Quasi — personal accounts, cash book and subsidiary books', 4, 'quasi subsidiary|quasi personal cash book subsidiary|quasi entry personal account cash book subsidiary|quasi personal account cash book subsidiary|quasi entry keep personal account cash book subsidiary|quasi keep personal account cash book subsidiary|quasi personal account cash book some subsidiary|quasi sales book|quasi entry sales book|quasi single entry subsidiary|quasi entry subsidiary|quasi single entry adds subsidiary|quasi add subsidiary|quasi single entry also subsidiary')], 'c2'),
        V('v3', 'How is profit found under the capital comparison method?',
          'Under the capital comparison or net worth method, we find capital at the beginning and at the end by preparing statements of affairs, where capital is assets minus liabilities. Profit equals closing capital plus drawings minus fresh capital introduced minus opening capital. Drawings are added back and fresh capital is deducted.',
          [P('p1', 'Capital at two dates via statements of affairs (assets − liabilities)', 3, 'statement of affairs|assets minus liabilities|assets less liabilities|net worth|excess of assets', 'opening|beginning|start|two dates', min=1),
           P('p2', 'Add drawings to closing capital', 3, 'add drawings|plus drawings|drawings added|drawings are added|add back drawings|adding drawings|drawings add'),
           P('p3', 'Deduct fresh capital and opening capital', 4, 'minus fresh|less fresh|deduct fresh|fresh capital deducted|subtract fresh|fresh capital is deducted|fresh capital subtracted|minus additional|less additional|deduct additional|deduct capital introduced|less capital introduced|minus capital introduced', 'minus opening|less opening|deduct opening|subtract opening|opening capital deducted|opening capital is deducted')], 'c3'),
        V('v4', 'Give the main differences between a statement of affairs and a balance sheet.',
          'A statement of affairs is prepared from incomplete records and estimates, and capital in it is just a balancing figure; omissions are hard to detect. Its purpose is to find capital at the beginning and end of a period. A balance sheet is prepared from ledger balances under double entry, capital comes from the capital account, omissions are detected because it would not agree, and it shows the financial position.',
          [P('p1', 'SoA from incomplete records/estimates; BS from double-entry ledger', 3, 'incomplete|estimate|memory', 'double entry|ledger', min=2),
           P('p2', 'Capital: balancing figure vs capital account', 4, 'balancing figure|balancing|difference between assets|assets minus liabilities|residual', 'capital account|ledger', min=1),
           P('p3', 'Omissions hard to detect vs detected; purpose — capital vs financial position', 3, 'omission|omit|missed|left out|purpose|financial position|find capital|ascertain capital', min=1)], 'c4'),
        V('v5', 'How would you find credit sales when the sales figure is missing?',
          'Prepare a total debtors account. On the debit side put the opening balance of debtors and bills dishonoured; on the credit side put cash received, discount allowed, sales returns, bad debts, bills received and the closing balance of debtors. The balancing figure on the debit side is credit sales. Adding cash sales from the cash summary gives total sales.',
          [P('p1', 'Prepare a Total Debtors account', 4, 'total debtors|debtors account|debtor account|sundry debtors account|receivables account'),
           P('p2', 'Credits: cash received, discount, returns, bad debts, closing balance', 3, 'cash received|cash collected|collection|received from debtors', 'discount|return|bad debt|closing', min=2),
           P('p3', 'Credit sales = balancing figure (on the debit side)', 3, 'balancing figure|balancing|difference|missing figure|balance figure')], 'c5'),
        V('v6', 'Give examples of hidden drawings and hidden fresh capital in incomplete records.',
          'Hidden drawings include the residential share of rent or electricity, the owner\'s life insurance premium paid by the business, household expenses paid from business cash and goods taken for personal use. Hidden fresh capital includes the maturity amount of the owner\'s insurance policy, interest or dividend on his private investments, or rent from private property put into the business, and business creditors paid from his personal money.',
          [P('p1', 'Drawings: residential rent/electricity, owner\'s insurance premium, household expenses, goods for personal use', 5, 'drawing', 'residential|residence|household|personal use|life insurance premium|insurance premium|home|family|goods taken', min=2),
           P('p2', 'Fresh capital: insurance maturity, private interest/dividend, private rent, creditors paid privately', 5, 'fresh capital|additional capital|capital introduced|capital brought', 'maturity|private investment|dividend|interest on private|interest on his|personal investment|private property|non business|paid from personal|personal money|own money|private money', min=2)], 'c6'),
    ]

    cases_ = [{
        'id': 'k1', 'title': 'Anand Electricals — reconstructing sales', 'difficulty': 'hard',
        'case': ('Anand Electricals does not record cash sales. Its cash and bank summary for 2025-26 shows: opening balance ₹5,000; collections from debtors ₹1,24,000; cash sales not recorded. Payments: creditors ₹1,50,000; rent ₹12,000; salaries ₹9,000; drawings ₹18,000; closing balance ₹6,000. '
                 'Debtors were ₹38,000 at the start and ₹47,000 at the end; discount allowed ₹1,500 and bad debts ₹2,000. The trade earns a uniform gross profit of 25% on cost.'),
        'mcqs': [
            M('k1a', 'Cash sales for the year are:', [R(k_cs), R(71000), R(61000), R(76000)], 0,
              "Payments side of the cash summary = creditors 1,50,000 + rent 12,000 + salaries 9,000 + drawings 18,000 + closing balance 6,000 = ₹1,95,000. Known receipts = opening balance 5,000 + collections from debtors 1,24,000 = ₹1,29,000. Cash sales = 1,95,000 − 1,29,000 = ₹66,000. The trap ₹71,000 ignores the opening balance. In practice: when a dealer doesn't record counter sales, the accountant reconstructs them from the cash and bank movement.", 'moderate', '(150000+12000+9000+18000+6000)-(5000+124000)') | {'topic': "Conversion method: completing double entry from the records"},
            M('k1b', 'Credit sales are:', [R(k_cr), R(133000), R(115000), R(130000)], 0,
              "Rebuild the debtors account. Credits: collections 1,24,000 + discount 1,500 + bad debts 2,000 + closing debtors 47,000 = ₹1,74,500. Less opening debtors 38,000: credit sales = ₹1,36,500. The trap ₹1,33,000 forgets the discount and bad debts, which also reduce debtors without cash coming in. In practice: an electricals dealer's credit sales can be checked this way against GST returns filed for the year.", 'hard', '124000+1500+2000+47000-38000') | {'topic': "Conversion method: completing double entry from the records"},
            M('k1c', 'Gross profit on total sales is:', [R(k_gp), R(50625), R(33750), R(60750)], 0,
              "Total sales = cash 66,000 + credit 1,36,500 = ₹2,02,500. A gross profit of 25% on cost equals 25/125 = 20% of sales: 2,02,500 × 20% = ₹40,500. The trap ₹50,625 applies 25% directly to sales, mixing up markup on cost with margin on sales. In practice: a uniform markup lets an accountant cross-check whether the reconstructed sales and purchases make commercial sense.", 'hard', '(136500+66000)*20/100') | {'topic': "Gross profit technique for missing stock or sales"},
            M('k1d', 'If ₹3,000 of the "drawings" was actually rent for the shop, net profit would:', ['Decrease by ₹3,000', 'Increase by ₹3,000', 'Not change', 'Decrease by ₹6,000'], 0,
              "If ₹3,000 of the 'drawings' was really rent for the shop, it is a business expense. Moving it from drawings to rent increases expenses by ₹3,000, so net profit decreases by ₹3,000 (capital is unchanged overall, since drawings fall by the same amount). The trap 'not change' forgets that drawings never pass through profit and loss. In practice: misclassifying payments between drawings and expenses changes taxable profit, so a CA checks every large debit.", 'moderate') | {'topic': "Spotting drawings and fresh capital"},
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch09', 'n': 1,
        'title': 'Accounts from Incomplete Records',
        'outcomes': [
            'Explain why records may be incomplete and describe the features and types of single entry (pure, simple, quasi).',
            'Find profit or loss by the capital comparison (statement of affairs / net worth) method and distinguish a statement of affairs from a balance sheet.',
            'Convert incomplete records into double entry using a cash and bank summary, total debtors, total creditors and bills accounts.',
            'Identify hidden drawings and fresh capital, and use the gross profit ratio to estimate missing stock or sales.',
            'Draw up final accounts — trading account, P&L account and balance sheet — when the books are incomplete.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 70}, 'prereq': ['fnd-p1-ch06-u01'],
                 'exam_tip': 'Write the opening statement of affairs, cash summary and total accounts as numbered working notes. Examiners give step marks for each, even when the final balance sheet does not agree.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Single entry = incomplete double entry; no trial balance; profit is an estimate.',
                        'Types: pure (personal accounts only), simple (+ cash book), quasi (+ subsidiary books).',
                        'Capital comparison: Profit = Closing capital + Drawings − Fresh capital − Opening capital.',
                        'Conversion method: opening statement of affairs → cash and bank summary → total debtors/creditors (and bills accounts) → final accounts.',
                        'Gross profit technique fills in missing stock or sales; convert "on cost" to "on sales" first.'],
            'remember': ['Statement of affairs: capital is the balancing figure.', 'Bills accepted go to the debit of creditors; bills received go to the credit of debtors.', 'Private receipts into the business = capital; private payments = drawings.', 'x% on cost = x/(100 + x) of sales.'],
            'traps': ['Don\'t forget cash sales/purchases when totalling sales and purchases.', 'Don\'t deduct drawings in the capital comparison — add them back.', 'Don\'t leave household bills inside business expenses.', 'Don\'t apply "on cost" percentages directly to sales.'],
        },
        'quickref': [
            {'k': 'Capital comparison', 'v': 'Profit = Closing capital + Drawings − Fresh capital − Opening capital'},
            {'k': 'Capital (statement of affairs)', 'v': 'Total assets − total liabilities (balancing figure)'},
            {'k': 'Credit sales', 'v': 'Closing debtors + cash received + discount + returns + bad debts + bills received − opening debtors − bills dishonoured'},
            {'k': 'Credit purchases', 'v': 'Closing creditors + cash paid + discount received + returns + bills accepted − opening creditors'},
            {'k': 'Bills received', 'v': 'Closing B/R + bills collected + bills dishonoured − opening B/R'},
            {'k': 'Gross profit on cost → on sales', 'v': 'x% on cost = x/(100 + x) × 100 % of sales (25% on cost = 20% of sales)'},
            {'k': 'Closing stock (estimate)', 'v': 'Opening stock + net purchases + direct expenses − (net sales − gross profit)'},
        ],
        'viva': viva, 'cases': cases_,
    }


# ---- offline auto-check: kw/min (viva matcher), nums (figures that must appear), rows ([account, side, amount]) ----
AUTO = {
    'q1': {'extra_ok': False,
           's1': {'nums': [249000]},
           's2': {'nums': [571000]},
           's3': {'nums': [360000, 682000]},
           's4': {'kw': ['undisclos|not declared|not reasonable|understat|conceal|unreasonable|under declared|underdeclared|suppress|not disclosed|under reported|underreported|unexplained|not justified|less than earned|lower than'],
                  'nums': [400000, 282000],
                  'wrong': [{'kw': ['income is reasonable|declared income reasonable|declaration reasonable'], 'say': 'He earned ₹6,82,000 but declared ₹4,00,000 — the declaration is not reasonable unless the ₹2,82,000 is explained.'}]}},
    'q2': {'extra_ok': False,
           's1': {'nums': [109000]},
           's2': {'nums': [26000]},
           's3': {'nums': [334000]},
           's4': {'nums': [255000]},
           's5': {'nums': [126000]},
           's6': {'kw': ['drawing|household|personal'], 'nums': [32000, 32500, 4200]},
           's7': {'nums': [54800]},
           's8': {'nums': [133800, 177800]}},
    'q3': {'extra_ok': True,
           's1': {'kw': ['incomplete record|estimat|inquir|enquir|memory|single entry|guess|available information', 'ledger|double entry|complete record|books of account|proper records|accounts books'], 'min': 2},
           's2': {'kw': ['capital', 'balancing figure|difference between|balancing|derived|residual|excess of assets|assets minus|assets less|assets over liabilit'], 'min': 2},
           's3': {'kw': ['omission|omitted|error|mistake', 'difficult|not detect|cannot detect|detect|easily|not possible|not found|located|disagree|not agree|totals'], 'min': 2},
           's4': {'kw': ['ascertain capital|find capital|opening capital|closing capital|calculate capital|determine capital|know capital|valuation|value|arbitrary|financial position|true and fair|true fair|position of business']}},
    'q4': {'extra_ok': False,
           's1': {'kw': ['bills payable|bill payable|b p'], 'nums': [53000]},
           's2': {'rows': [['bills payable|bill payable|b p|bills accepted|acceptance', 'dr', 53000], ['discount', 'dr', 3500], ['return', 'dr', 4500], ['cash|bank', 'dr', 210000],
                           ['purchase|balancing', 'cr', 284000]]},
           's3': {'nums': [310000]}},
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
