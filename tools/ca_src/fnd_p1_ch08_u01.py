"""CA Foundation · Paper 1 Accounting · Chapter 8 Financial Statements of Not-for-Profit Organisations (single unit).
Original explanations, names and numbers; scope and topic order follow the ICAI study material (May 2027 onwards)."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p1-ch08-u01'


def two_side(title, left, right, lh='Expenditure', rh='Income', note_=None):
    """Two-sided account / balance sheet as a table. left/right: [(text, amount or None)]. Totals computed and asserted equal."""
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
    """Vertical working: rows [(text, amount-or-text)] — no automatic total."""
    return table(['Particulars', '₹'], [[a, inr(b) if isinstance(b, (int, float)) else b] for a, b in rows], title=title, note=note_)


def build():
    # ============ Illustration 1: Receipts and Payments Account ============
    c1 = Checks()
    rec = [('To Balance b/d — Cash in hand', 4500), ('To Balance b/d — Cash at bank', 26000), ('To Subscriptions', 185000),
           ('To Entrance fees', 12000), ('To Donation for building', 150000), ('To Sale of old newspapers', 2300),
           ('To Interest on fixed deposit', 6200), ('To Sale of old furniture', 8000), ('To Locker rent', 9500)]
    pay = [('By Salaries', 72000), ('By Electricity charges', 18400), ('By Sports equipment purchased', 45000),
           ('By Building construction', 160000), ('By Fixed deposit with bank', 50000), ('By Honorarium to secretary', 12000),
           ('By Printing and stationery', 6800), ('By Sundry expenses', 4300)]
    tot_r = c1.add('4500+26000+185000+12000+150000+2300+6200+8000+9500', 'Total of the receipts side (with opening balances)')
    tot_p = c1.add('72000+18400+45000+160000+50000+12000+6800+4300', 'Total payments before closing balance')
    close_bal = c1.add('403500-368500', 'Closing cash and bank balance (balancing figure)')
    bank_close = c1.add('35000-6200', 'Closing bank balance (cash in hand counted at ₹6,200)')
    RP1 = two_side('Green Valley Residents\' Club — Receipts and Payments Account for the year ended 31 March 2026', rec,
                   pay + [('By Balance c/d — Cash in hand', 6200), ('By Balance c/d — Cash at bank', bank_close)], 'Receipts', 'Payments')

    # ============ Illustration 2: subscription ============
    c2 = Checks()
    subs_inc = c2.add('246000-9000-7500+5000+14000', 'Subscription income for 2025-26')
    os_close = c2.add('3000+14000', 'Subscription outstanding carried forward (old ₹3,000 + current ₹14,000)')
    c2.add('12000+248500+7500', 'Debit side total of Subscription Account')
    c2.add('5000+246000+17000', 'Credit side total of Subscription Account')
    L2 = {'t': 'ledger', 'ac': 'Subscription Account', 'dr': [
        {'date': '2025 Apr 1', 'part': 'To Balance b/d (outstanding for 2024-25)', 'amt': 12000, 'ob': True},
        {'date': '2026 Mar 31', 'part': 'To Income and Expenditure A/c (transfer)', 'amt': subs_inc},
        {'date': '2026 Mar 31', 'part': 'To Balance c/d (received in advance for 2026-27)', 'amt': 7500}],
        'cr': [
        {'date': '2025 Apr 1', 'part': 'By Balance b/d (received in advance for 2025-26)', 'amt': 5000, 'ob': True},
        {'date': '2025-26', 'part': 'By Cash / Bank (Receipts and Payments A/c)', 'amt': 246000},
        {'date': '2026 Mar 31', 'part': 'By Balance c/d (outstanding: 2024-25 ₹3,000 + 2025-26 ₹14,000)', 'amt': os_close}]}
    S2 = stmt('Short-cut working', [('Subscriptions received during 2025-26', 246000), ('Less: relating to 2024-25 (arrears collected)', '(9,000)'),
                                     ('Less: relating to 2026-27 (received in advance)', '(7,500)'), ('Add: advance received last year for 2025-26', '5,000'),
                                     ('Add: still to be received for 2025-26', '14,000'), ('Income for 2025-26 (to I & E A/c)', subs_inc)])

    # ============ Illustration 3: full R&P -> I&E + Balance Sheet ============
    c3 = Checks()
    op_assets = c3.add('8000+42000+120000+60000+15000+9000+100000', 'Opening assets')
    op_liab = c3.add('100000+6000+4000', 'Opening liabilities (prize fund, salary outstanding, subscription in advance)')
    op_cf = c3.add('354000-110000', 'Opening capital fund')
    s3 = c3.add('210000-12000-6000+4000+18000', 'Subscription income 2025-26')
    sal3 = c3.add('54000-6000+7000', 'Salaries for the year')
    sm3 = c3.add('9000+36000-11000', 'Sports material consumed')
    tour3 = c3.add('28000-22000', 'Net tournament expense (expenses less ticket sales)')
    loss3 = c3.add('7000-5000', 'Loss on sale of old sports equipment')
    dep_se = c3.add('(120000-7000)*15/100', 'Depreciation on sports equipment @15%')
    dep_fu = c3.add('60000*10/100+20000*10/100*6/12', 'Depreciation on furniture (new furniture for 6 months)')
    se_close = c3.add('120000-7000-16950', 'Sports equipment at year end')
    fu_close = c3.add('60000+20000-7000', 'Furniture at year end')
    pf3 = c3.add('100000+8000-6500', 'Prize fund at year end')
    inc3 = c3.add('214000+15000', 'Total income')
    exp3 = c3.add('55000+34000+6000+14000+9000+7500+3000+2000+16950+7000', 'Total expenditure')
    sur3 = c3.add('229000-154450', 'Surplus for the year')
    cash3 = c3.add('8000+42000+(210000+20000+80000+15000+8000+22000+5000+30000)-(54000+36000+28000+6500+14000+20000+50000+9000+7500)', 'Closing cash and bank')
    cf3 = c3.add('244000+20000+30000+74550', 'Closing capital fund')
    c3.add('368550+101500+80000+7000+6000', 'Balance sheet total')
    IE3 = two_side('Sunrise Sports Club — Income and Expenditure Account for the year ended 31 March 2026', [
        ('To Salaries (54,000 − 6,000 + 7,000)', sal3), ('To Sports material consumed (9,000 + 36,000 − 11,000)', sm3),
        ('To Tournament expenses less ticket sales (28,000 − 22,000)', tour3), ('To Electricity', 14000), ('To Honorarium', 9000),
        ('To Repairs', 7500), ('To Old subscriptions written off', 3000), ('To Loss on sale of sports equipment (7,000 − 5,000)', loss3),
        ('To Depreciation — sports equipment', dep_se), ('To Depreciation — furniture', dep_fu), ('To Surplus — excess of income over expenditure', sur3)],
        [('By Subscriptions (WN 1)', s3), ('By General donation', 15000)])
    BS3 = two_side('Sunrise Sports Club — Balance Sheet as at 31 March 2026', [
        ('Capital Fund: opening 2,44,000 + entrance fees 20,000 + life membership 30,000 + surplus 74,550', cf3),
        ('Prize Fund: 1,00,000 + interest 8,000 − prizes 6,500', pf3), ('Pavilion Fund (specific donation)', 80000),
        ('Salaries outstanding', 7000), ('Subscriptions received in advance', 6000)],
        [('Sports equipment (1,20,000 − 7,000 − 16,950)', se_close), ('Furniture (60,000 + 20,000 − 7,000)', fu_close),
         ('Pavilion under construction', 50000), ('Prize Fund investments', 100000), ('Stock of sports material', 11000),
         ('Subscriptions outstanding (2025-26)', 18000), ('Cash in hand', 12000), ('Cash at bank', cash3 - 12000)], 'Liabilities', 'Assets')
    OB3 = two_side('Working Note 2 — Opening Balance Sheet as at 1 April 2025 (to find the capital fund)', [
        ('Prize Fund', 100000), ('Salaries outstanding', 6000), ('Subscriptions received in advance', 4000), ('Capital Fund (balancing figure)', op_cf)],
        [('Cash in hand', 8000), ('Cash at bank', 42000), ('Sports equipment', 120000), ('Furniture', 60000), ('Subscriptions outstanding', 15000),
         ('Stock of sports material', 9000), ('Prize Fund investments', 100000)], 'Liabilities', 'Assets')

    # ============ Illustration 4: special funds and life membership (method 2) ============
    c4 = Checks()
    pf4 = c4.add('50000+4500+3000-6200', 'Prize Fund at year end')
    lm_tr = c4.add('25*1200', 'Life membership transferred to I & E A/c (25 members × ₹1,200 annual rate)')
    lm_bal = c4.add('25*10000-30000', 'Life Membership Fund carried forward')
    tf_excess = c4.add('47000-(30000+12000)', 'Tournament expenses in excess of the Tournament Fund (charged to I & E)')
    F4 = two_side('Extract of Balance Sheet (liabilities side) and I & E Account items', [
        ('Prize Fund: opening 50,000 + bond interest 4,500 + fresh donation 3,000 − prizes 6,200', pf4),
        ('Life Membership Fund: 2,50,000 − 30,000 transferred', lm_bal), ('Tournament Fund (fully used up, closed)', 0)],
        [('9% Prize Fund bonds (asset side)', 50000), ('Amount of funds not invested — held in cash/bank', pf4 + lm_bal - 50000)],
        'Funds (liabilities)', 'Represented by (assets)')

    # ============ Q1: library ============
    q1 = Checks()
    q1_cf = q1.add('18000+240000+50000+5000+2000-4000', 'Opening capital fund')
    q1_sub = q1.add('96000-5000-3000+7000', 'Subscription income')
    q1_rent = q1.add('31000-4000+3000', 'Rent for the year')
    q1_st = q1.add('2000+4500-1500', 'Stationery consumed')
    q1_db = q1.add('(240000+55000)*10/100', 'Depreciation on books @10% on closing book value before depreciation')
    q1_df = q1.add('50000*10/100', 'Depreciation on furniture')
    q1_inc = q1.add('95000+8000+1800+2200+1500', 'Total income')
    q1_exp = q1.add('30000+42000+5000+9000+6300+29500+5000', 'Total expenditure')
    q1_def = q1.add('126800-108500', 'Deficit')
    q1_cash = q1.add('18000+96000+8000+40000+1800+2200+1500-(31000+42000+55000+4500+9000+6300)', 'Closing cash and bank')
    q1_ccf = q1.add('311000-18300', 'Closing capital fund')
    Q1IE = two_side('City Public Library — Income and Expenditure Account for the year ended 31 March 2026', [
        ('To Rent (31,000 − 4,000 + 3,000)', q1_rent), ('To Salaries', 42000), ('To Stationery consumed (2,000 + 4,500 − 1,500)', q1_st),
        ('To Newspapers and magazines', 9000), ('To Electricity', 6300), ('To Depreciation — books', q1_db), ('To Depreciation — furniture', q1_df)],
        [('By Subscriptions (96,000 − 5,000 − 3,000 + 7,000)', q1_sub), ('By Entrance fees (revenue under the library\'s rules)', 8000),
         ('By Sale of old newspapers', 1800), ('By Fines from members', 2200), ('By Interest on savings account', 1500),
         ('By Deficit — excess of expenditure over income', q1_def)])
    Q1BS = two_side('City Public Library — Balance Sheet as at 31 March 2026', [
        ('Capital Fund: 3,11,000 − deficit 18,300', q1_ccf), ('Book Fund (specific donation)', 40000), ('Rent outstanding', 3000),
        ('Subscriptions received in advance', 3000)],
        [('Books (2,40,000 + 55,000 − 29,500)', 240000 + 55000 - q1_db), ('Furniture (50,000 − 5,000)', 50000 - q1_df), ('Stock of stationery', 1500),
         ('Subscriptions outstanding', 7000), ('Cash and bank', q1_cash)], 'Liabilities', 'Assets')

    # ============ Q3: hospital medicines + tournament fund ============
    q3 = Checks()
    q3_cp = q3.add('140000-9000+12500', 'Credit purchases of medicines')
    q3_tp = q3.add('143500+6000', 'Total purchases of medicines')
    q3_med = q3.add('18000+149500-22000', 'Medicines consumed (to I & E A/c)')
    q3_tf = q3.add('47000-30000-12000', 'Excess tournament expenditure charged to I & E A/c')

    # ============ Case ============
    k = Checks()
    k_sub = k.add('180000-8000-5000+3000+10000', 'subscription income')
    k_cf = k.add('20000+300000+8000-3000', 'opening capital fund')
    k_net = k.add('30000-24000', 'net match expense')

    concepts = [
        {'id': 'c1', 'title': 'Not-for-profit organisations and their three statements',
         'body': ['A not-for-profit organisation (NPO) — a club, a charitable hospital, a school trust, a library, a temple trust — exists to serve its members or society, not to earn returns for owners. Any surplus stays inside the organisation and is used for its objects; it is never distributed to members.',
                  'Instead of a trading and profit and loss account, an NPO prepares (1) a Receipts and Payments Account (a summary of cash and bank), (2) an Income and Expenditure Account (the accrual-based result of the year) and (3) a Balance Sheet.',
                  'Vocabulary changes: profit is called Surplus (income more than expenditure), loss is Deficit, and the owners\' capital is the Capital Fund (also called the Accumulated Fund when members never contributed capital as such).',
                  'An NPO registered as a company under section 8 of the Companies Act, 2013 must present its Income and Expenditure Account and Balance Sheet in the Schedule III format. The clubs and societies in exam questions are usually not companies, so the simpler two-sided format is used.'],
         'analogy': 'A housing society is like a family kitty: everyone pays in, the money is spent on common needs, and whatever is left over is kept for next year — nobody takes a "dividend".',
         'work': 'CA firms audit thousands of trusts, societies and clubs. The first job is usually to turn the treasurer\'s cash summary into proper accrual accounts that donors, members and the tax department can rely on.'},
        {'id': 'c2', 'title': 'Receipts and Payments Account — the cash summary',
         'body': ['It is a classified summary of the cash book for the year, without dates. It opens with the cash and bank balances at the start, shows every receipt on the debit side and every payment on the credit side, and closes with the cash and bank balances at the end.',
                  'Everything that passed through cash or bank is included — capital or revenue, and whether it belongs to last year, this year or next year. Non-cash items such as depreciation, outstanding expenses or accrued income are not included.',
                  'Its closing balance is normally a debit (cash in hand plus bank). A credit balance can appear only for a bank overdraft.',
                  'Limitations: it does not show the surplus or deficit, mixes capital and revenue items, ignores items not yet received or paid, and says nothing about assets and liabilities. It is adequate on its own only for a very small body whose only asset is cash and which carries nothing forward from one year to the next.'],
         'analogy': 'It is the passbook view of the year — it tells you how much money came and went, not whether the club actually did well.',
         'work': 'Treasurers of small societies often hand over only a receipts and payments statement. A CA must not mistake its closing cash balance for the surplus — a large building donation sitting in the bank is not income.'},
        {'id': 'c3', 'title': 'Income and Expenditure Account — accrual result of the year',
         'body': ['It is the NPO\'s version of the profit and loss account and is prepared on the accrual basis. Only revenue items of the current year appear: revenue expenses on the debit side, revenue incomes on the credit side.',
                  'Adjustments are made for outstanding and prepaid expenses and for income accrued or received in advance. Non-cash charges such as depreciation, and gains or losses on selling fixed assets, are included. Capital receipts and capital payments are left out.',
                  'Main incomes: subscriptions, general donations, entrance fees where treated as revenue, grants for running expenses, interest and dividends on general investments, sale of old newspapers, locker rent, hall hire.',
                  'Activity netting: income raised for a particular activity is set against that activity\'s cost — for example, tournament ticket sales are deducted from tournament expenses and only the net figure is shown.',
                  'There is no opening balance. The balancing figure is the surplus or deficit, which is added to (or deducted from) the capital fund in the balance sheet.'],
         'analogy': 'If the receipts and payments account is the bank passbook, the income and expenditure account is the honest report card: it counts what was earned and used this year, whether or not cash moved.',
         'work': 'Grant-giving bodies and donors judge an NPO on its income and expenditure account — a society showing repeated deficits may lose recognition or funding.'},
        {'id': 'c4', 'title': 'Receipts and Payments vs Income and Expenditure',
         'body': ['Both are prepared by NPOs, but they answer different questions: "how much cash moved?" versus "did the year produce a surplus?". Examiners regularly ask for the differences.'],
         'blocks': [table(['Basis', 'Receipts and Payments Account', 'Income and Expenditure Account'], [
             ['Nature', 'Summary of the cash book (real account)', 'Like a profit and loss account (nominal account)'],
             ['Basis', 'Cash basis', 'Accrual basis'],
             ['Items included', 'Capital and revenue items of any year, if paid or received in cash', 'Only revenue items of the current year, whether received/paid or not'],
             ['Sides', 'Receipts debited, payments credited', 'Expenditure debited, income credited'],
             ['Opening balance', 'Starts with opening cash and bank balances', 'No opening balance'],
             ['Closing balance', 'Cash and bank in hand (usually debit)', 'Surplus or deficit, taken to the capital fund'],
             ['Non-cash items', 'Excluded (no depreciation, no outstanding items)', 'Included (depreciation, outstanding, accrued, prepaid)'],
         ])],
         'analogy': 'Same club, two cameras: one films the cash box, the other films the club\'s performance.',
         'work': 'In practice you prepare the receipts and payments account first (it is the easiest to reconcile with the bank) and then build the income and expenditure account from it.'},
        {'id': 'c5', 'title': 'Subscriptions and consumable items — computing the year\'s figure',
         'body': ['Subscription income for the year = subscriptions received − arrears of earlier years collected − advance for later years received + advance received last year for this year + amount still due for this year.',
                  'Outstanding subscriptions are an asset in the balance sheet; subscriptions received in advance are a liability. Old arrears that will never be collected are written off as an expense in the income and expenditure account.',
                  'The same logic applies to expenses: salary for the year = paid − last year\'s outstanding paid now + this year\'s outstanding − prepaid at year end + prepaid last year.',
                  'Consumable stocks (sports material, stationery, medicines, food): consumption = opening stock + purchases − closing stock. Purchases include credit purchases worked out from the creditors\' account (paid to creditors − opening creditors + closing creditors).'],
         'analogy': 'A gym\'s membership: fees collected in March for April belong to April, and the member who has not yet paid for March still counts as March income.',
         'work': 'Members\' outstanding schedules are a key audit area — CAs check them against the membership register and question old arrears that should be written off.'},
        {'id': 'c6', 'title': 'Capital or revenue? Treatment of special receipts and payments',
         'body': ['General donation (no purpose stated): revenue — credit to the I & E Account. Large donations without a stated purpose may be capitalised if the question says so.',
                  'Specific donation (for a building, books, a prize): capital — credited to a separate fund on the liabilities side, never to income.',
                  'Legacy (money left to the NPO under a deceased person\'s will): capital — added to the capital fund.',
                  'Entrance (admission) fees: if the question is silent, treat as capital and add to the capital fund. They are revenue only when they are small/normal or when the rules of the body say they are income — follow the question.',
                  'Life membership fees: capital, because they are paid once and are not recurring — added to the capital fund (or a life membership fund). Alternatives used only if the question says so: (i) hold the full amount in a fund until the member dies and then move it to the capital fund; (ii) transfer an amount equal to the annual subscription to income every year until exhausted, moving any balance to the capital fund on death; (iii) transfer an amount worked out on age and life expectancy each year.',
                  'Endowment donation: the donation itself is capital (kept intact); only the income it earns may be spent on the stated purpose.',
                  'Sale of old newspapers and periodicals: revenue income. Sale of an old fixed asset: the proceeds are a capital receipt; only the profit or loss on sale goes to the I & E Account.',
                  'Honorarium: a payment to a person who is not an employee (a visiting artist, an honorary secretary) for services — a revenue expense.'],
         'analogy': 'Ask: "Will this receipt come again next year in the normal course?" Subscriptions — yes (revenue). A one-time building donation or life membership — no (capital).',
         'work': 'Misclassifying a capital donation as income inflates the surplus and can affect the income-tax exemption conditions of a charitable trust — a real audit risk.'},
        {'id': 'c7', 'title': 'Fund accounting — specific funds',
         'body': ['A specific (special) fund is shown separately on the liabilities side: e.g. Building Fund, Prize Fund, Tournament Fund, Scholarship Fund.',
                  'Income earned on the fund\'s investments and fresh donations for that purpose are added to the fund; expenses on that purpose are deducted from the fund. They do not pass through the I & E Account.',
                  'If the purpose\'s expenses exceed the fund, the fund is closed and the excess is charged to the I & E Account (debit). The excess is not shown as an asset.',
                  'When an asset is bought out of a fund (e.g. a building from the Building Fund), the asset appears on the assets side; the fund stays on the liabilities side (or is transferred to the capital fund once the purpose is fulfilled, if the question says so).',
                  'Strictly, the word "Fund" fits amounts that are kept invested separately (Prize Fund, Scholarship Fund); where collections are not separately invested, the heading "Account" is more apt (Building Account, Tournament Account). A donated security or other asset is credited to the fund at its valuation.'],
         'analogy': 'A fund is a labelled envelope inside the club\'s safe. Money in the "prize" envelope can be spent only on prizes — and the interest earned on it goes back into the same envelope.',
         'work': 'Donors increasingly demand utilisation certificates for restricted funds. Fund-wise accounting is what lets a CA certify that money was spent only on the purpose for which it was given.'},
        {'id': 'c8', 'title': 'From Receipts and Payments to I & E Account and Balance Sheet — the method',
         'body': ['Step 1 — Opening capital fund: prepare an opening balance sheet; capital fund = opening assets (including accrued income, prepaid expenses, stocks) − opening liabilities (including outstanding expenses, income received in advance, specific funds).',
                  'Step 2 — Revenue items: for each income and expense, adjust the cash figure for opening and closing outstanding/advance/prepaid amounts and transfer the result to the I & E Account. Add depreciation, profit/loss on sale of assets, and consumption of stocks.',
                  'Step 3 — Capital items: take capital receipts (specific donations, legacies, entrance fees if capital, life membership) to the funds, and capital payments (purchase of assets, investments) to the asset accounts.',
                  'Step 4 — Balance sheet: capital fund (opening + capitalised receipts ± surplus/deficit), specific funds, current liabilities; fixed assets (opening + additions − sales − depreciation), investments, stocks, receivables, closing cash and bank (overdraft on the liabilities side).'],
         'analogy': 'You are re-sorting a shoebox of cash slips into three piles: "this year\'s running costs and income", "long-term things" and "what we own and owe today".',
         'work': 'This is exactly the conversion a CA does for a society\'s annual general meeting: the members approve the I & E Account and Balance Sheet, not the cash summary.'},
        {'id': 'c9', 'title': 'Educational institutions',
         'body': ['Most schools and colleges in India are run by societies registered under the Societies Registration Act, 1860; in States with public trust laws (for example Maharashtra, under the Bombay Public Trust Act, 1950) they are also registered as trusts. They follow the financial year.',
                  'Governance: office bearers (president, secretary, treasurer), an executive committee and a general body; each school or college run by the trust usually has a governing body that includes its principal or head.',
                  'Funds come from three main sources: (1) donations from the public (recurring or one-time, in cash or kind — land, buildings, securities, furniture); (2) fees — tuition, term, admission, laboratory and similar; (3) government grants — maintenance, equipment and building grants, and other special grants.',
                  'Laboratory and library deposits are refundable when the student leaves — they are liabilities, not income. Term fees are tracked in a separate account and spent on specified student activities (sports, magazine, medical inspection, library books, excursions, cultural events, examinations); any unspent balance is carried forward. Admission/capitation collections are regulated and in many places restricted.'],
         'analogy': 'A school\'s laboratory deposit is like a hotel room security deposit: you hold it, but it is not your money.',
         'work': 'Auditors of school trusts check that grants are used as sanctioned and that refundable deposits are not quietly treated as income.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Preparing a Receipts and Payments Account', 'difficulty': 'core', 'minutes': 10,
         'q': 'Green Valley Residents\' Club gives you the following for the year ended 31 March 2026. Opening balances on 1 April 2025: cash in hand ₹4,500, cash at bank ₹26,000. Receipts: subscriptions ₹1,85,000; entrance fees ₹12,000; donation for building ₹1,50,000; sale of old newspapers ₹2,300; interest on fixed deposit ₹6,200; sale of old furniture ₹8,000; locker rent ₹9,500. Payments: salaries ₹72,000; electricity ₹18,400; sports equipment ₹45,000; building construction ₹1,60,000; fixed deposit made ₹50,000; honorarium to secretary ₹12,000; printing and stationery ₹6,800; sundry expenses ₹4,300. Cash in hand on 31 March 2026 is ₹6,200. Prepare the Receipts and Payments Account.',
         'solution': [RP1, wn('Closing balance', f'Total receipts with opening balances ₹{inr(tot_r)} − total payments ₹{inr(tot_p)} = ₹{inr(close_bal)}. Cash in hand is ₹6,200, so the bank balance is ₹{inr(bank_close)}.'),
                      note('Every cash item goes in — capital (building donation, fixed deposit, sale of furniture) as well as revenue. No adjustment is made for outstanding items or depreciation in this account.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Subscription for the year with arrears and advances', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'Riverside Club received ₹2,46,000 as subscriptions during 2025-26. This includes ₹9,000 for 2024-25 and ₹7,500 for 2026-27. On 1 April 2025, subscriptions outstanding were ₹12,000 and subscriptions received in advance (for 2025-26) were ₹5,000. Subscriptions due for 2025-26 but not received by 31 March 2026 are ₹14,000; the remaining arrears of 2024-25 are still considered recoverable. Work out the subscription income of 2025-26 and show the Subscription Account.',
         'solution': [S2, L2, p(f'Balance sheet on 31 March 2026: Subscriptions outstanding ₹{inr(os_close)} (asset); Subscriptions received in advance ₹7,500 (liability).'),
                      note('If the remaining ₹3,000 of old arrears were irrecoverable, it would be written off — debited to the I & E Account — instead of being carried forward.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Full problem: I & E Account and Balance Sheet from a Receipts and Payments Account', 'difficulty': 'hard', 'minutes': 28,
         'q': ('Sunrise Sports Club — balances on 1 April 2025: cash ₹8,000; bank ₹42,000; sports equipment ₹1,20,000; furniture ₹60,000; subscriptions outstanding ₹15,000; stock of sports material ₹9,000; Prize Fund ₹1,00,000 invested in 8% bonds ₹1,00,000; salaries outstanding ₹6,000; subscriptions received in advance ₹4,000.\n'
               'Receipts during 2025-26: subscriptions ₹2,10,000 (including ₹12,000 for 2024-25 and ₹6,000 for 2026-27); entrance fees ₹20,000; donation for pavilion ₹80,000; general donation ₹15,000; interest on Prize Fund bonds ₹8,000; tournament ticket sales ₹22,000; sale of old sports equipment (book value ₹7,000) ₹5,000; life membership fees ₹30,000.\n'
               'Payments: salaries ₹54,000; sports material ₹36,000; tournament expenses ₹28,000; prizes awarded ₹6,500; electricity ₹14,000; furniture bought on 1 October 2025 ₹20,000; pavilion construction (in progress) ₹50,000; honorarium ₹9,000; repairs ₹7,500. Cash in hand on 31 March 2026 ₹12,000.\n'
               'Further information: subscriptions due for 2025-26 not yet received ₹18,000; the balance of 2024-25 arrears is irrecoverable; salaries outstanding ₹7,000; stock of sports material ₹11,000; depreciation — sports equipment 15% on the closing book value, furniture 10% p.a. Prepare the Income and Expenditure Account for 2025-26 and the Balance Sheet as at 31 March 2026.'),
         'solution': [OB3, wn('Working Note 1 — Subscriptions', f'2,10,000 − 12,000 (2024-25) − 6,000 (2026-27) + 4,000 (advance received last year) + 18,000 (due) = ₹{inr(s3)}. Of the opening arrears of ₹15,000 only ₹12,000 came in; ₹3,000 is written off.'),
                      IE3, BS3,
                      wn('Treatment decisions', 'Entrance fees and life membership fees — capital, added to the capital fund (the question gives no other instruction). Pavilion donation — specific, so a Pavilion Fund. Bond interest and prizes go through the Prize Fund, not the I & E Account. Ticket sales are netted against tournament expenses. Sale proceeds of equipment are capital; only the ₹2,000 loss is charged.'),
                      wn('Cash check', f'Opening 50,000 + receipts 3,90,000 − payments 2,25,000 = ₹{inr(cash3)}; cash ₹12,000, bank ₹{inr(cash3 - 12000)}.')],
         'checks': c3},
        {'id': 'i4', 'title': 'Specific funds and a life-membership policy', 'difficulty': 'moderate', 'minutes': 10,
         'q': 'Hillview Club: (a) Prize Fund on 1 April 2025 ₹50,000, invested in 9% bonds of ₹50,000. During the year bond interest ₹4,500 and a fresh donation for prizes ₹3,000 were received; prizes of ₹6,200 were awarded. (b) 25 new life members paid ₹10,000 each. The club\'s rules say life membership is to be taken to income at the normal annual subscription of ₹1,200 per member each year, the balance being carried forward. (c) Tournament Fund ₹30,000 at the start; tournament donations ₹12,000; tournament expenses ₹47,000. Show how each item appears in the final accounts.',
         'solution': [F4, ul([f'Prize Fund closes at ₹{inr(pf4)} — interest and donations added, prizes deducted; nothing passes through the I & E Account.',
                              f'Life membership: ₹{inr(lm_tr)} is credited to the I & E Account this year (because the rules say so); ₹{inr(lm_bal)} remains in the Life Membership Fund. Without such a rule the whole ₹2,50,000 would be capitalised.',
                              f'Tournament: expenses exceed the fund and donations by ₹{inr(tf_excess)}. The fund is closed and ₹{inr(tf_excess)} is debited to the I & E Account — it is not shown as an asset.'])],
         'checks': c4},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Turning a society treasurer\'s cash summary into final accounts', 'role': 'Audit assistant, CA firm (audit of a co-operative housing society\'s club)',
         'situation': 'The treasurer has prepared only a receipts and payments statement and calls the ₹3.2 lakh increase in bank balance "this year\'s profit". Among the receipts are a ₹2 lakh donation for a new gym, ₹40,000 of next year\'s maintenance collected in advance, and sale proceeds of an old generator.',
         'steps': ['Prepare the opening balance sheet from last year\'s audited accounts to fix the opening capital fund.',
                   'Move the gym donation to a Gym Fund (specific donation — capital).',
                   'Remove the advance maintenance from income and show it as a liability; add maintenance still due from members as an asset.',
                   'Take the generator\'s sale proceeds to the asset account; only the profit or loss on sale goes to the I & E Account.',
                   'Charge depreciation and outstanding expenses, then prepare the I & E Account and the balance sheet for the AGM.'],
         'takeaway': 'Growth in the bank balance is not the surplus. Accrual adjustments and capital/revenue separation can turn an apparent "profit" into a modest surplus or even a deficit.',
         'think': 'The treasurer says, "The gym donation is our income — we received it this year." How do you respond?',
         'answer': 'It is a specific donation given for a capital purpose, so it is credited to a Gym Fund on the liabilities side, not to income. Treating it as income would overstate the surplus.'},
        {'id': 'j2', 'title': 'Reviewing a school trust\'s accounts', 'role': 'Article assistant on the audit of an education society',
         'situation': 'The school has shown laboratory deposits collected from new students (₹1.8 lakh) as income, and has spent part of a building grant on staff salaries.',
         'steps': ['Reclassify laboratory deposits as a liability — they are refundable when students leave.',
                   'Trace the building grant to its sanction letter; spending it on salaries breaches its conditions and must be reported.',
                   'Check that term fees are kept in a separate account and spent only on permitted student activities, with any balance carried forward.',
                   'Prepare a note for management and the governing body listing the corrections.'],
         'takeaway': 'In educational institutions the question is not only "income or capital?" but also "whose money is this, and what may it be spent on?"',
         'think': 'Why is a refundable library deposit not income even though the cash has been received?',
         'answer': 'Because the institution must return it when the student leaves; it is an obligation (liability), not something earned.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'A Receipts and Payments Account is best described as:', 'options': ['A summary of the cash book for the period', 'An account prepared on the accrual basis', 'An account showing only revenue items', 'A statement of assets and liabilities'], 'answer': 0, 'explain': "A Receipts and Payments Account is simply a classified summary of the cash book: it starts with the opening cash and bank balance, lists every receipt and payment of the year — capital or revenue, relating to any period — and ends with the closing balance. The trap is 'prepared on the accrual basis'; that describes the Income and Expenditure Account. In practice: the treasurer of a housing society presents this cash summary at the annual general meeting before the audited accounts.", 'topic': "Receipts and Payments Account — the cash summary", 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'Subscriptions received in 2025-26 ₹80,000 include ₹4,000 for 2024-25 and ₹2,500 for 2026-27. Subscriptions due for 2025-26 not yet received: ₹6,000. Subscriptions received in advance last year for 2025-26: ₹1,500. Income from subscriptions for 2025-26 is:', 'options': ['₹81,000', '₹79,500', '₹73,500', '₹84,500'], 'answer': 0, 'check': '80000-4000-2500+6000+1500', 'explain': "Start with cash received and adjust to the year: 80,000 − 4,000 (belongs to last year) − 2,500 (belongs to next year) + 6,000 (due for this year, not yet received) + 1,500 (received last year in advance for this year) = ₹81,000. The trap ₹79,500 forgets the advance received last year, which is income of this year. In practice: a gymkhana's accountant keeps a member-wise subscription register so outstanding and advance amounts at each year-end are known exactly.", 'topic': "Subscriptions and consumable items — computing the year's figure", 'concept': 'c5', 'difficulty': 'moderate'},
        {'id': 'm3', 'q': 'A club receives entrance fees of ₹25,000. The question gives no instruction on their treatment. They should be:', 'options': ['Added to the capital fund', 'Credited to the I & E Account', 'Shown as a current liability', 'Deducted from subscriptions'], 'answer': 0, 'explain': "Entrance (admission) fees are paid once, on joining, and are treated as a capital receipt added to the capital fund unless the question gives a different instruction (for example, capitalise only a part). The trap is crediting them to the Income and Expenditure Account as if they were recurring revenue like annual subscriptions. In practice: a new golf or gymkhana club collecting large one-time membership entry fees capitalises them because they are not part of yearly running income.", 'topic': "Capital or revenue? Treatment of special receipts and payments", 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'Sale of old newspapers by a library is shown as:', 'options': ['Income in the I & E Account', 'A capital receipt added to the capital fund', 'A deduction from the cost of books', 'A liability'], 'answer': 0, 'explain': "Sale of old newspapers and periodicals is a small, recurring receipt arising from the normal running of a library, so it is revenue income credited to the Income and Expenditure Account. The trap is calling it a capital receipt simply because something was 'sold' — the newspapers were never capital assets. In practice: reading rooms and residents' welfare associations routinely show scrap and raddi sales as miscellaneous income.", 'topic': "Capital or revenue? Treatment of special receipts and payments", 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm5', 'q': 'An amount received by a charitable hospital under the will of a deceased donor is called:', 'options': ['A legacy, treated as capital', 'An honorarium, treated as revenue', 'A subscription, treated as revenue', 'An endowment expense'], 'answer': 0, 'explain': "A legacy is an amount received under the will of a deceased person. It is non-recurring, so it is capitalised and added to the capital fund on the liabilities side, not credited to Income and Expenditure. The trap is 'honorarium', which is a payment made to a non-employee for services — an expense, not a receipt. In practice: charitable trusts and hospitals in India receive bequests under wills and add them to their corpus.", 'topic': "Capital or revenue? Treatment of special receipts and payments", 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm6', 'q': 'On 1 April a club had: cash ₹12,000, furniture ₹90,000, subscriptions outstanding ₹8,000, outstanding salaries ₹5,000 and a Building Fund of ₹40,000. Its capital fund was:', 'options': ['₹65,000', '₹1,05,000', '₹1,10,000', '₹57,000'], 'answer': 0, 'check': '12000+90000+8000-5000-40000', 'explain': "Capital fund = assets − outside liabilities. Assets: cash 12,000 + furniture 90,000 + subscriptions outstanding 8,000 = ₹1,10,000. Liabilities: outstanding salaries 5,000 + Building Fund 40,000 = ₹45,000. Capital fund = 1,10,000 − 45,000 = ₹65,000. The trap ₹1,05,000 deducts only salaries and treats the Building Fund as part of capital. In practice: an NPO's opening statement of affairs separates earmarked funds from its general capital fund.", 'topic': "From Receipts and Payments to I & E Account and Balance Sheet — the method", 'concept': 'c8', 'difficulty': 'moderate'},
        {'id': 'm7', 'q': 'Opening stock of sports material ₹6,000; amount paid for sports material ₹42,000 (including ₹3,000 owed for last year); ₹2,500 is owed for this year\'s purchases; closing stock ₹7,500. Sports material consumed is:', 'options': ['₹40,000', '₹43,000', '₹42,000', '₹37,500'], 'answer': 0, 'check': '6000+(42000-3000+2500)-7500', 'explain': "First find this year's purchases: paid 42,000 − 3,000 (last year's dues) + 2,500 (owed for this year) = ₹41,500. Consumed = opening stock 6,000 + 41,500 − closing stock 7,500 = ₹40,000. The trap ₹42,000 takes cash paid as the year's expense, ignoring both creditors and stock. In practice: sports clubs track kit and ball stocks this way so the Income and Expenditure Account shows what was actually used during the season.", 'topic': "Subscriptions and consumable items — computing the year's figure", 'concept': 'c5', 'difficulty': 'hard'},
        {'id': 'm8', 'q': 'A donation received specifically for building a hall is:', 'options': ['Credited to a Building Fund on the liabilities side', 'Credited to the I & E Account', 'Shown on the assets side', 'Deducted from the capital fund'], 'answer': 0, 'explain': "A donation given for a specific purpose, such as building a hall, must be used only for that purpose. It is a capital receipt credited to a separate Building Fund, shown among the liabilities in the balance sheet. The trap is crediting it to Income and Expenditure, which would show a false surplus. In practice: temples, schools and trusts maintain separate earmarked funds, and auditors check that the money is spent only for the stated purpose.", 'topic': "Fund accounting — specific funds", 'concept': 'c7', 'difficulty': 'core'},
        {'id': 'm9', 'q': 'Tournament Fund ₹20,000; tournament expenses for the year ₹26,000. The excess of ₹6,000 will be:', 'options': ['Debited to the I & E Account', 'Shown as an asset in the balance sheet', 'Deducted from the capital fund directly without passing through I & E', 'Carried forward as a negative fund balance'], 'answer': 0, 'explain': "Expenses of ₹26,000 are first set against the Tournament Fund of ₹20,000, which is used up. The excess of ₹6,000 has no fund left to absorb it, so it is charged to the Income and Expenditure Account as an expense. The trap is showing it as an asset or a negative fund balance — a specific fund cannot have a debit balance. In practice: when a club's event costs overshoot the sponsorship collected, the shortfall is met from general funds and reported as an expense.", 'topic': "Fund accounting — specific funds", 'concept': 'c7', 'difficulty': 'moderate'},
        {'id': 'm10', 'q': 'Old furniture with a book value of ₹18,000 is sold for ₹15,000. In the I & E Account the club will show:', 'options': ['Loss on sale ₹3,000 on the debit side', 'Sale proceeds ₹15,000 on the credit side', 'Book value ₹18,000 on the debit side', 'Nothing — it is a capital item'], 'answer': 0, 'explain': "The sale proceeds of a fixed asset are a capital receipt and do not go to Income and Expenditure. Only the result matters: book value 18,000 − sale price 15,000 = loss of ₹3,000, debited to the Income and Expenditure Account. The trap is crediting the ₹15,000 proceeds as income. In practice: when a society sells old furniture or a vehicle, its accounts show only the profit or loss on sale, while the asset is removed from the balance sheet.", 'topic': "Capital or revenue? Treatment of special receipts and payments", 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm11', 'q': 'Which of these does NOT appear in an Income and Expenditure Account?', 'options': ['Purchase of furniture', 'Depreciation on furniture', 'Outstanding salary for the year', 'Subscriptions due but not received'], 'answer': 0, 'explain': "The Income and Expenditure Account shows only revenue items of the year, on an accrual basis. Purchase of furniture is capital expenditure, so it is added to assets in the balance sheet. Depreciation, outstanding salary and subscriptions due are all revenue items of the year — the trap is thinking unpaid or unreceived amounts are excluded. In practice: auditors of trusts check that capital purchases are not wrongly charged as expenses to show a lower surplus.", 'topic': "Income and Expenditure Account — accrual result of the year", 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm12', 'q': 'A token payment to a visiting expert who is not an employee of the NPO is called:', 'options': ['Honorarium', 'Legacy', 'Endowment', 'Subscription'], 'answer': 0, 'explain': "An honorarium is a payment made to a person who is not an employee — such as a visiting expert, guest lecturer or examiner — for services rendered. It is a revenue expense. The trap is 'legacy', which is money received under a will. In practice: colleges and professional bodies like ICAI branches pay honoraria to guest faculty, and TDS provisions on professional fees may apply.", 'topic': "Capital or revenue? Treatment of special receipts and payments", 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm13', 'q': 'An NPO registered under section 8 of the Companies Act, 2013 prepares its Income and Expenditure Account and Balance Sheet:', 'options': ['In the format of Schedule III to the Companies Act, 2013', 'Only as a Receipts and Payments Account', 'In any format the members choose', 'Only on the cash basis'], 'answer': 0, 'explain': "A not-for-profit organisation registered as a company under section 8 of the Companies Act, 2013 must prepare its financial statements in the format of Schedule III, like any other company, with its Income and Expenditure Account in place of a Statement of Profit and Loss. The trap is 'any format the members choose' — that freedom applies only to unincorporated clubs and societies. In practice: CAs auditing section 8 foundations of corporate groups present Schedule III statements filed with the Registrar.", 'topic': "Not-for-profit organisations and their three statements", 'concept': 'c1', 'difficulty': 'moderate'},
        {'id': 'm14', 'q': 'Laboratory deposits collected from students by a college are shown as:', 'options': ['A liability', 'Income of the year', 'A capital fund addition', 'A reduction of laboratory expenses'], 'answer': 0, 'explain': "Laboratory (caution) deposits are collected from students and must be refunded when they leave, after deducting damages if any. Because the college owes this money back, the deposits are a liability. The trap is treating them as income of the year — only forfeited or deducted amounts become income. In practice: schools and colleges keep student-wise deposit registers and auditors confirm that unrefunded deposits are shown as liabilities.", 'topic': "Educational institutions", 'concept': 'c9', 'difficulty': 'core'},
    ]

    questions = [
        {'id': 'q1', 'marks': 10, 'minutes': minutes(10), 'difficulty': 'hard', 'pad': 'table',
         'q': ('City Public Library — balances on 1 April 2025: cash and bank ₹18,000; books ₹2,40,000; furniture ₹50,000; subscriptions outstanding ₹5,000; stock of stationery ₹2,000; rent outstanding ₹4,000.\n'
               'Receipts and Payments for 2025-26 — Receipts: subscriptions ₹96,000 (including ₹5,000 for 2024-25 and ₹3,000 for 2026-27); entrance fees ₹8,000; donation for purchase of books ₹40,000; sale of old newspapers ₹1,800; fines from members ₹2,200; interest on savings account ₹1,500. Payments: rent ₹31,000; salaries ₹42,000; books purchased ₹55,000; stationery ₹4,500; newspapers and magazines ₹9,000; electricity ₹6,300.\n'
               'Information: subscriptions of ₹7,000 for 2025-26 are still due; rent outstanding on 31 March 2026 is ₹3,000; stock of stationery on 31 March 2026 is ₹1,500; the library\'s rules treat entrance fees as revenue; depreciate books by 10% and furniture by 10% (on the closing book value before depreciation). Prepare the Income and Expenditure Account for the year ended 31 March 2026 and the Balance Sheet on that date.'),
         'model': [wn('WN 1 — Opening capital fund', f'Assets 18,000 + 2,40,000 + 50,000 + 5,000 + 2,000 = 3,15,000 − rent outstanding 4,000 = ₹{inr(q1_cf)}.'),
                   Q1IE, Q1BS,
                   wn('WN 2 — Key adjustments', f'Subscriptions ₹{inr(q1_sub)}; rent ₹{inr(q1_rent)}; stationery consumed ₹{inr(q1_st)}; depreciation on books ₹{inr(q1_db)}, on furniture ₹{inr(q1_df)}. Closing cash and bank: 18,000 + 1,49,500 − 1,47,800 = ₹{inr(q1_cash)}. The book donation is a specific donation → Book Fund.')],
         'checks': q1,
         'scheme': [
             {'id': 's1', 'pt': 'Opening capital fund ₹3,11,000 computed', 'm': 1, 'skill': 'computation'},
             {'id': 's2', 'pt': 'Subscription income ₹95,000', 'm': 1, 'skill': 'computation'},
             {'id': 's3', 'pt': 'Rent ₹30,000 and stationery consumed ₹5,000', 'm': 1, 'skill': 'computation'},
             {'id': 's4', 'pt': 'Depreciation on books ₹29,500 and furniture ₹5,000', 'm': 1, 'skill': 'computation'},
             {'id': 's5', 'pt': 'Entrance fees as revenue (per rules); old newspapers, fines, interest as income', 'm': 1, 'skill': 'classification'},
             {'id': 's6', 'pt': 'Deficit ₹18,300 correctly found and shown', 'm': 1.5, 'skill': 'presentation'},
             {'id': 's7', 'pt': 'Book donation shown as Book Fund (not income)', 'm': 1, 'skill': 'classification'},
             {'id': 's8', 'pt': 'Capital fund ₹2,92,700 after deducting deficit; outstanding rent and advance subscriptions as liabilities', 'm': 1.5, 'skill': 'presentation'},
             {'id': 's9', 'pt': 'Assets side: books, furniture, stationery, subscriptions outstanding, cash ₹19,700; totals agree ₹3,38,700', 'm': 1, 'skill': 'balancing'},
         ],
         'remarks': ['Most candidates computed subscriptions correctly but many forgot to deduct last year\'s outstanding rent paid this year.',
                     'A frequent error was crediting the donation for books to income, which turned the deficit into a surplus — examiners penalise this heavily.',
                     'Candidates who showed the opening capital fund as a separate working scored step marks even when the final balance sheet did not agree.'],
         'mistakes': ['Treating entrance fees as capital even though the question says the rules treat them as revenue.', 'Charging stationery purchased instead of stationery consumed.', 'Showing purchase of books in the I & E Account.', 'Adding the deficit to the capital fund instead of deducting it.'],
         'tips': ['Always start with the opening balance sheet — it gives the capital fund and the opening outstanding figures you need later.', 'Write the computation for every adjusted figure inside the particulars or as a working note.', 'Read the "treatment" instructions (entrance fees, life membership) before deciding capital or revenue.']},
        {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'table',
         'q': 'Distinguish between a Receipts and Payments Account and an Income and Expenditure Account (any five points).',
         'model': [table(['Basis', 'Receipts and Payments Account', 'Income and Expenditure Account'], [
             ['1. Nature', 'Summary of the cash book; a real account', 'Equivalent of a profit and loss account; a nominal account'],
             ['2. Basis of accounting', 'Cash basis', 'Accrual basis'],
             ['3. Capital/revenue', 'Includes both capital and revenue receipts and payments', 'Only revenue incomes and expenses'],
             ['4. Period', 'Includes items of past, current and future periods if paid or received in cash', 'Only items relating to the current period, whether paid/received or not'],
             ['5. Opening and closing balance', 'Starts with opening cash/bank and ends with closing cash/bank', 'No opening balance; closing balance is the surplus or deficit transferred to the capital fund'],
             ['6. Non-cash items', 'Depreciation, outstanding and accrued items excluded', 'Such items are included'],
         ])],
         'scheme': [{'id': f's{i}', 'pt': t, 'm': 1, 'skill': 'concept'} for i, t in enumerate(['Nature (cash summary vs P&L equivalent)', 'Cash basis vs accrual basis', 'Capital and revenue vs revenue only', 'Any period vs current period only', 'Balances: cash/bank vs surplus/deficit (or non-cash items point)'], 1)],
         'remarks': ['Answers in a tabular form with a clear "basis" column scored best.', 'Some candidates wrote that the Receipts and Payments Account shows the surplus — this is incorrect and lost the mark.'],
         'mistakes': ['Saying the Receipts and Payments Account is part of the double entry system like a ledger account — it is only a summary.', 'Mixing up which account has an opening balance.'],
         'tips': ['Five clear bases in a table earn full marks in about nine minutes.', 'Use contrasting words in each row: cash/accrual, all periods/current period, capital and revenue/revenue only.']},
        {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
         'q': '(a) Shanti Charitable Hospital: stock of medicines on 1 April 2025 ₹18,000 and on 31 March 2026 ₹22,000; creditors for medicines ₹9,000 (1 April 2025) and ₹12,500 (31 March 2026); paid to creditors for medicines ₹1,40,000; cash purchases of medicines ₹6,000. Find the medicines consumed to be charged to the I & E Account. (3 marks)\n(b) The hospital\'s Tournament (sports day) Fund stood at ₹30,000; donations for sports day ₹12,000 were received and sports-day expenses were ₹47,000. Show the treatment. (2 marks)',
         'model': [stmt('(a) Medicines consumed', [('Paid to creditors for medicines', 140000), ('Less: opening creditors', '(9,000)'), ('Add: closing creditors', '12,500'),
                                                  ('Credit purchases', q3_cp), ('Add: cash purchases', '6,000'), ('Total purchases', q3_tp),
                                                  ('Add: opening stock', '18,000'), ('Less: closing stock', '(22,000)'), ('Medicines consumed', q3_med)]),
                   p(f'(b) Fund available = 30,000 + 12,000 = ₹42,000; expenses ₹47,000. The fund is fully used and closed (shown at nil). The excess of ₹{inr(q3_tf)} is debited to the Income and Expenditure Account — it is not carried as an asset.')],
         'checks': q3,
         'scheme': [{'id': 's1', 'pt': 'Credit purchases ₹1,43,500 via creditors', 'm': 1, 'skill': 'computation'},
                    {'id': 's2', 'pt': 'Total purchases ₹1,49,500 including cash purchases', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Consumption ₹1,45,500 using opening and closing stock', 'm': 1, 'skill': 'computation'},
                    {'id': 's4', 'pt': 'Donations added to the fund; expenses set off against it', 'm': 1, 'skill': 'concept'},
                    {'id': 's5', 'pt': 'Excess ₹5,000 debited to I & E Account (not an asset)', 'm': 1, 'skill': 'application'}],
         'remarks': ['Many candidates charged only the amount paid to creditors, forgetting both the creditors adjustment and the stock adjustment.', 'In part (b), showing a negative fund on the liabilities side or an asset for the excess was a common error.'],
         'mistakes': ['Adding opening creditors instead of deducting them.', 'Charging the entire ₹47,000 of sports-day expenses to income and leaving the fund untouched.'],
         'tips': ['Do purchases first (creditors), then consumption (stock) — two clear steps.', 'For fund questions write: fund + additions − expenses = balance (or excess to I & E).']},
    ]

    viva = [
        V('v1', 'What is a Receipts and Payments Account, and what are its main features?',
          'It is a yearly, date-free summary of the cash book. It starts with the opening cash and bank balances, records all receipts on the debit side and all payments on the credit side, and ends with the closing cash and bank balances. It includes both capital and revenue items of past, current and future periods, follows the cash basis, and does not show the surplus or deficit.',
          [P('p1', 'Summary of the cash book (cash and bank)', 3, 'summary cash book|summary of cash|cash book summary|summarises cash|summarizes cash|summary of all cash|summary of cash and bank'),
           P('p2', 'Opening and closing cash/bank balances; receipts debit, payments credit', 2, 'opening', 'closing', 'receipt debit|debit receipt|receipts on debit|receipts left', min=2),
           P('p3', 'Includes capital and revenue items of any period', 3, 'capital', 'revenue', 'past|previous|future|any period|all period|every period', min=2),
           P('p4', 'Cash basis — does not show surplus or deficit', 2, 'not show surplus|not show the surplus|no surplus|cannot show surplus|not give surplus|does not show surplus|doesn t show surplus|surplus not|cash basis|not accrual|no accrual|not on accrual')], 'c2'),
        V('v2', 'How does an Income and Expenditure Account differ from a Receipts and Payments Account?',
          'The Income and Expenditure Account is like a profit and loss account and is prepared on the accrual basis, while the Receipts and Payments Account is a cash summary on the cash basis. The income and expenditure account includes only revenue items of the current year, whether received or not, while receipts and payments includes capital and revenue items of any period. The income and expenditure account has no opening balance and its balance is the surplus or deficit, whereas receipts and payments starts and ends with cash and bank balances.',
          [P('p1', 'I & E = like profit and loss, accrual basis; R & P = cash summary, cash basis', 4, 'accrual', 'cash basis|cash summary|summary of cash|cash book|on cash|cash only', min=2),
           P('p2', 'I & E only current-year revenue items; R & P has capital and revenue of any period', 3, 'revenue', 'current year|current period|this year|relating to year|only to year|current', 'capital|no capital|not capital|without capital|excludes capital|excluding capital', min=3),
           P('p3', 'I & E: no opening balance, ends in surplus/deficit; R & P: cash/bank balances', 3, 'surplus|deficit', 'no opening|without opening|not have opening|not start|opening balance|cash and bank balance|bank balance|not a cash balance|not cash balance|instead of cash balance', min=2)], 'c4'),
        V('v3', 'How are entrance fees treated in the accounts of a club?',
          'Entrance fees are normally treated as a capital receipt and added to the capital fund, because they are not recurring and give the member no extra privilege. If the question is silent, we always capitalise them. They are treated as revenue and credited to the Income and Expenditure Account only when the amount is small or normal, or when the rules of the club say they are income.',
          [P('p1', 'Normally capital — added to the capital fund', 4, ALT('{c} receipt|{c} fund|capitalis|capitaliz|treat as {c}|treated as {c}|{c} in nature', c=['capital'])),
           P('p2', 'If the question is silent — capitalise', 3, 'silent|no instruction|not stated|not given|nothing is said|nothing said|not mentioned|no information|not specified|doesn t say|does not say'),
           P('p3', 'Revenue only if small/normal or the rules say so', 3, 'revenue|income and expenditure|i e account|income', 'small|normal|rules|bye law|bylaw|rule|question says|unless|if specified|specified', min=2)], 'c6'),
        V('v4', 'Distinguish between a general donation, a specific donation and a legacy, and state their treatment.',
          'A general donation is revenue income credited to the Income and Expenditure Account, because it is received without any stated purpose. A specific donation is capitalised in a separate fund on the liabilities side, because it is given for a particular purpose such as a building. A legacy is an amount received under the will of a deceased person; it is a capital receipt added to the capital fund.',
          [P('p1', 'General donation — no purpose — revenue, credited to I & E', 3, 'general', 'income and expenditure|revenue|income|i e', 'no purpose|without purpose|no specific|not for any|not for specific|any purpose|without any|no stated|no particular|not for a particular'),
           P('p2', 'Specific donation — for a purpose — separate fund on the liabilities side', 4, 'specific donation capitalis|specific donation capitaliz|specific donation is capitalised|specific donation fund|specific donation special fund|specific donation separate fund|specific donation liabilit|specific donation capital|specific fund|specific capitalis|specific capitaliz|specific donation goes fund|specific donation taken fund|specific donation kept fund|specific purpose fund|specific purpose capitalis|building fund|building capitalis|capitalis separate fund|separate fund liabilit|special fund liabilit|not income but a separate fund|not income but separate fund|not income but a fund|not revenue but a fund|not revenue but a separate fund'),
           P('p3', 'Legacy — under a will — capital, added to the capital fund', 3, 'legacy|legacies', 'testament|death|deceased|died|passed away', 'capital', min=2)], 'c6'),
        V('v5', 'How are life membership fees treated? Mention the alternative methods.',
          'Life membership fees are a capital receipt because they are received only once and do not recur, so they are added to the capital fund or a life membership fund. Alternatively, if the rules say so, an amount equal to the annual subscription can be transferred to income every year until the amount is used up, the balance going to the capital fund when the member dies; or the whole amount can be held in a fund until the member dies; or an amount based on the age and life expectancy of the member can be transferred to income each year.',
          [P('p1', 'Capital receipt (non-recurring) — capital fund / life membership fund', 4, 'capital|capitalis|capitaliz|life membership fund', 'once|one time|onetime|non recurring|nonrecurring|not recur|single|lump sum|lumpsum', min=1),
           P('p2', 'Alternative: annual-subscription amount transferred to income each year', 3, 'annual subscription|yearly subscription|normal subscription|every year|each year|annually', 'income|income and expenditure|revenue|transfer'),
           P('p3', 'Balance to capital fund on the member\'s death (or held till death / age-based)', 3, 'death|dies|died|life expectancy|age')], 'c6'),
        V('v6', 'Explain fund accounting. What happens when expenses on a specific fund exceed the fund?',
          'Under fund accounting, money received for a specific purpose is kept in a separate fund on the liabilities side, such as a prize fund or a building fund. Income from the fund\'s investments and fresh donations for the purpose are added to the fund, and expenses on that purpose are deducted from the fund, not charged to the Income and Expenditure Account. If the expenses exceed the fund, the fund is closed and the excess is debited to the Income and Expenditure Account; it is not shown as an asset.',
          [P('p1', 'Separate fund on the liabilities side for a specific purpose', 3, 'separate fund|specific fund|special fund|separately|own fund|fund for each', 'liabilit|specific purpose|particular purpose|purpose', min=1),
           P('p2', 'Fund income added, purpose expenses deducted from the fund (not through I & E)', 3, 'income added|interest added|added to fund|add to fund|added to the fund|credited to fund|credit to fund', 'deduct|subtract|reduc|set off|charged to fund|debited to fund'),
           P('p3', 'Excess expenses → debited to I & E Account, not an asset', 4, 'excess|more than|exceed|over and above|beyond', 'income and expenditure|i e account|debit|charged to income|charge to income|revenue', min=2)], 'c7'),
    ]

    cases_ = [{
        'id': 'k1', 'title': 'Lakeside Club — closing the books for 2025-26', 'difficulty': 'hard',
        'case': ('Lakeside Club started 2025-26 with cash ₹20,000, a clubhouse worth ₹3,00,000 and subscriptions outstanding of ₹8,000; it owed ₹3,000 for electricity. '
                 'During the year it received subscriptions of ₹1,80,000 (of which ₹8,000 related to 2024-25 and ₹5,000 to 2026-27); ₹3,000 had been received in advance last year for 2025-26, and ₹10,000 is still due for 2025-26. '
                 'It also received a donation of ₹1,00,000 for a swimming pool, entrance fees of ₹15,000 (no instruction given) and ₹24,000 from the sale of tickets for an inter-club match whose expenses were ₹30,000.'),
        'mcqs': [
            M('k1a', 'What is the club\'s opening capital fund?', [R(k_cf), R(328000), R(320000), R(331000)], 0,
              "Opening capital fund = opening assets − outside liabilities. Assets: cash 20,000 + clubhouse 3,00,000 + subscriptions outstanding 8,000 = ₹3,28,000. Liability: electricity owed 3,000. Capital fund = 3,28,000 − 3,000 = ₹3,25,000. The trap ₹3,28,000 forgets the outstanding electricity bill; ₹3,20,000 leaves out the subscriptions receivable. In practice: an auditor taking over a club's audit rebuilds this opening statement of affairs before checking the year's figures.", 'moderate', '20000+300000+8000-3000') | {'topic': "From Receipts and Payments to I & E Account and Balance Sheet — the method"},
            M('k1b', 'Subscription income for 2025-26 is:', [R(k_sub), R(177000), R(167000), R(185000)], 0,
              "Subscription income = received 1,80,000 − 8,000 (for 2024-25) − 5,000 (for 2026-27) + 3,000 (received last year for 2025-26) + 10,000 (still due for 2025-26) = ₹1,80,000. The trap ₹1,77,000 forgets the advance received last year, which belongs to this year. In practice: the coincidence that income equals cash received is common, which is why accountants still work out every adjustment rather than assuming it.", 'hard', '180000-8000-5000+3000+10000') | {'topic': "Subscriptions and consumable items — computing the year's figure"},
            M('k1c', 'The swimming-pool donation and the entrance fees are shown as:', ['Pool donation — Swimming Pool Fund; entrance fees — added to capital fund', 'Both credited to the I & E Account', 'Pool donation — I & E Account; entrance fees — capital fund', 'Both shown as current liabilities'], 0,
              "The ₹1,00,000 donation is earmarked for a swimming pool, so it goes to a separate Swimming Pool Fund on the liabilities side. Entrance fees of ₹15,000 are capitalised and added to the capital fund because the question gives no other instruction. The trap is crediting both to Income and Expenditure, which would show a misleading surplus. In practice: clubs raising money for a new facility keep the collections in a separate fund and often a separate bank account.") | {'topic': "Capital or revenue? Treatment of special receipts and payments"},
            M('k1d', 'How is the inter-club match shown in the I & E Account?', [f'{R(k_net)} net expense on the debit side', 'Ticket sales ₹24,000 as income and expenses ₹30,000 as expenditure, separately, is the only acceptable method', 'Excess ₹6,000 shown as an asset', 'Not shown — it is a capital item'], 0,
              "Ticket sales of ₹24,000 were raised for the match, so they are set against its ₹30,000 cost. The net result, 30,000 − 24,000 = ₹6,000, is shown as a net expense on the debit side. The trap is claiming that only separate presentation is acceptable — netting activity income against activity cost is the usual, clearer presentation. In practice: clubs report each event's net cost so that members can see what the tournament actually cost the club.", 'moderate', '30000-24000') | {'topic': "Income and Expenditure Account — accrual result of the year"},
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch08', 'n': 1,
        'title': 'Financial Statements of Not-for-Profit Organisations',
        'outcomes': [
            'Explain what a not-for-profit organisation is and how its accounts differ from those of a business (surplus, deficit, capital fund).',
            'Prepare a Receipts and Payments Account and state its limitations.',
            'Prepare an Income and Expenditure Account on the accrual basis and distinguish it from a Receipts and Payments Account.',
            'Decide the correct treatment of subscriptions, donations, legacies, entrance fees, life membership, endowments, special funds, sale of assets and honorarium.',
            'Prepare the opening and closing Balance Sheet of an NPO and describe the special features of educational institutions.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 45, 'practice': 75}, 'prereq': ['fnd-p1-ch06-u01'],
                 'exam_tip': 'A 10–15 mark NPO question appears often. Marks are lost on classification (capital vs revenue) far more than on arithmetic — decide the treatment of every receipt before you draw up the accounts.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['NPOs prepare a Receipts and Payments Account (cash summary), an Income and Expenditure Account (accrual result) and a Balance Sheet.',
                        'Surplus = income > expenditure; Deficit = expenditure > income; Capital (Accumulated) Fund = assets − liabilities.',
                        'R & P includes capital and revenue items of any period; I & E includes only revenue items of the current period.',
                        'Opening capital fund comes from the opening balance sheet; the surplus is added to it, the deficit deducted.',
                        'Specific donations and special funds stay on the liabilities side; their income and expenses are dealt with inside the fund.'],
            'remember': ['Entrance fees: capital if the question is silent.', 'Life membership and legacy: capital.', 'General donation and sale of old newspapers: revenue.',
                         'Sale of fixed asset: only profit/loss to I & E.', 'Consumption = opening stock + purchases − closing stock.', 'Excess of fund expenses over the fund → debit I & E.'],
            'traps': ['Don\'t treat the increase in cash as surplus.', 'Don\'t forget last year\'s advance subscription (it is this year\'s income).', 'Don\'t put a specific fund\'s investment income into the I & E Account.', 'Don\'t show refundable deposits as income.'],
        },
        'quickref': [
            {'k': 'Subscription income', 'v': 'Received − arrears collected − advance for next year + advance received last year + due for this year'},
            {'k': 'Opening capital fund', 'v': 'Opening assets (incl. accrued, prepaid, stock) − opening liabilities (incl. outstanding, advance income, specific funds)'},
            {'k': 'Closing capital fund', 'v': 'Opening fund + capitalised receipts (entrance fees, legacy, life membership) ± surplus/deficit'},
            {'k': 'Consumables used', 'v': 'Opening stock + purchases (paid − opening creditors + closing creditors + cash purchases) − closing stock'},
            {'k': 'Special fund balance', 'v': 'Opening + donations + investment income − purpose expenses (excess → debit I & E)'},
            {'k': 'Capital receipts', 'v': 'Specific donations, legacies, life membership, entrance fees (if silent), sale proceeds of assets'},
            {'k': 'Revenue receipts', 'v': 'Subscriptions, general donations, interest on general investments, sale of old newspapers, locker rent'},
            {'k': 'Section 8 companies', 'v': 'I & E Account and Balance Sheet in Schedule III format (Companies Act, 2013)'},
        ],
        'viva': viva, 'cases': cases_,
    }


# ---- offline auto-check: kw/min (viva matcher), nums (figures that must appear), rows ([account, side, amount]) ----
AUTO = {
    'q1': {'extra_ok': False,
           's1': {'nums': [311000]},
           's2': {'nums': [95000]},
           's3': {'rows': [['rent', '', 30000], ['stationery', '', 5000]]},
           's4': {'kw': ['furniture'], 'nums': [29500]},
           's5': {'rows': [['entrance', '', 8000], ['newspaper|old paper|scrap', '', 1800], ['fine', '', 2200], ['interest', '', 1500]]},
           's6': {'kw': ['deficit|excess of expenditure over income|excess expenditure over income'], 'nums': [18300]},
           's7': {'kw': ['book fund|fund for books|books fund|specific fund|library fund|book donation fund|fund for purchase of books'], 'rows': [['fund', '', 40000]],
                  'wrong': [{'kw': ['21700'], 'say': 'A surplus of ₹21,700 means the ₹40,000 book donation was taken as income; it is a specific donation — credit it to a Book Fund (liabilities side).'}]},
           's8': {'kw': ['outstanding|unpaid|due', 'advance|prepaid|unearned'], 'nums': [292700]},
           's9': {'nums': [265500, 45000, 7000, 19700, 338700]}},
    'q2': {'extra_ok': True,
           's1': {'kw': ['summary cash|summary of cash|cash book|real account|cash account', 'profit loss|nominal account|nominal'], 'min': 2},
           's2': {'kw': ['cash basis|cash system|actual receipt|cash received|cash receipts', 'accrual|mercantile|accrued|due basis'], 'min': 2},
           's3': {'kw': ['capital and revenue|capital as well as revenue|both capital|capital nature|capital receipt|capital payment|capital item|capital expenditure|capital receipts',
                         'only revenue|revenue only|revenue nature|revenue item|revenue income|revenue expense|revenue expenditure'], 'min': 2},
           's4': {'kw': ['past|previous|future|any period|other period|whichever period|all periods|preceding|succeeding',
                         'current period|current year|relating period|relevant period|this year|accounting period|only items relating|relates current|same period'], 'min': 2},
           's5': {'kw': ['opening|closing|balance', 'surplus|deficit|depreciation|outstanding|non cash|accrued|excess of income'], 'min': 2}},
    'q3': {'extra_ok': False,
           's1': {'nums': [143500]},
           's2': {'nums': [149500]},
           's3': {'nums': [145500]},
           's4': {'kw': ['fund'], 'nums': [42000]},
           's5': {'kw': ['income expenditure|expenditure account|i e account|i e a c|ie account'], 'nums': [5000],
                  'wrong': [{'kw': ['shown as asset|carried as asset|asset side|shown on assets|shown assets side|treated as asset'], 'say': 'The excess spending over the fund is a revenue charge to the Income and Expenditure Account; it is not an asset.'}]}},
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
