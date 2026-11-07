"""CA Foundation · Paper 1 Accounting · Chapter 7 Final Accounts of Sole Proprietors · Unit 1 Non-manufacturing entities.
Original explanations, names and numbers (structure and scope follow the ICAI study material)."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p1-ch07-u01'


def tacc(ac, dr, cr):
    """Two-sided final account (Trading / P&L) shown as a T-account; both sides must total the same."""
    sd, sc = sum(a for _, a in dr), sum(a for _, a in cr)
    assert abs(sd - sc) < 0.01, (ac, sd, sc)
    return {'t': 'ledger', 'ac': ac, 'dr': [{'date': '', 'part': p_, 'amt': a} for p_, a in dr], 'cr': [{'date': '', 'part': p_, 'amt': a} for p_, a in cr]}


def bsheet(title, L, A, note_=None):
    n = max(len(L), len(A))
    L = L + [('', None)] * (n - len(L)); A = A + [('', None)] * (n - len(A))
    rows = [[l, inr(la) if la is not None else '', a, inr(aa) if aa is not None else ''] for (l, la), (a, aa) in zip(L, A)]
    tl, ta = sum(x for _, x in L if x), sum(x for _, x in A if x)
    assert abs(tl - ta) < 0.01, (title, tl, ta)
    rows.append(['Total', inr(tl), 'Total', inr(ta)])
    return table(['Liabilities', '₹', 'Assets', '₹'], rows, num=[1, 3], total=True, title=title, note=note_)


def build():
    # =============== Illustration 1: Rao Stores — complete final accounts ===============
    c = Checks()
    TBR = [('Capital', -500000), ('Opening stock (1 April 2026)', 120000), ('Purchases', 640000), ('Sales', -1120000), ('Sales returns', 15000), ('Purchase returns', -10000),
           ('Carriage inwards', 18000), ('Godown wages', 36000), ('Salaries', 144000), ('Rent', 66000), ('Insurance', 12000), ('Advertisement', 25000),
           ('Bad debts', 4000), ('Discount allowed', 6000), ('Commission received', -9000), ('Trade receivables', 180000), ('Provision for doubtful debts', -7000),
           ('Trade payables', -126000), ('10% Bank loan (taken 1 October 2026)', -150000), ('Furniture', 80000), ('Motor van', 200000), ('Cash in hand', 22000), ('Drawings', 60000)]
    bank = -sum(v for _, v in TBR)
    TBR.insert(-1, ('Cash at bank', bank))
    c.add('500000+1120000+10000+9000+7000+126000+150000', 'Credit total of the trial balance')
    c.add('120000+640000+15000+18000+36000+144000+66000+12000+25000+4000+6000+180000+80000+200000+22000+294000+60000', 'Debit total of the trial balance (bank 2,94,000)')
    assert bank == 294000
    pur = c.add('640000-10000-4000-6000', 'Purchases less returns, drawings of goods and goods lost by fire')
    sal = c.add('1120000-15000', 'Sales less returns')
    tr_dr = c.add('120000+620000+18000+36000', 'Trading account debits before gross profit')
    gp = c.add('1105000+145000-794000', 'Gross profit')
    s_sal = c.add('144000+12000', 'Salaries including outstanding')
    s_rent = c.add('66000-6000', 'Rent less prepaid for April 2027')
    s_ins = c.add('12000-3000', 'Insurance less prepaid')
    newp = c.add('(180000-5000)*5/100', 'New provision: 5% of debtors after further bad debts')
    s_bd = c.add('4000+5000+8750-7000', 'Charge for bad and doubtful debts')
    d_f = c.add('80000*10/100', 'Depreciation on furniture @10%')
    d_v = c.add('200000*20/100', 'Depreciation on motor van @20%')
    s_int = c.add('150000*10/100*6/12', 'Interest on loan for 6 months (Oct-Mar), outstanding')
    s_fire = c.add('6000-4500', 'Loss by fire not covered by insurance')
    com = c.add('9000+2000', 'Commission including accrued')
    pl_dr = c.add('156000+60000+9000+25000+6000+10750+8000+40000+7500+1500', 'Profit and loss account debits')
    np = c.add('456000+11000-323750', 'Net profit')
    cap = c.add('500000+143250-60000-4000', 'Closing capital')
    c.add('579250+150000+7500+12000+126000', 'Balance sheet total — liabilities side')
    c.add('72000+160000+145000+166250+4500+6000+3000+2000+22000+294000', 'Balance sheet total — assets side')
    trading1 = tacc('Trading Account of Rao Stores for the year ended 31 March 2027', [
        ('To Opening stock', 120000), ('To Purchases 6,40,000 − returns 10,000 − drawings 4,000 − fire 6,000', pur),
        ('To Carriage inwards', 18000), ('To Godown wages', 36000), ('To Gross profit c/d', gp)],
        [('By Sales 11,20,000 − returns 15,000', sal), ('By Closing stock', 145000)])
    pl1 = tacc('Profit and Loss Account of Rao Stores for the year ended 31 March 2027', [
        ('To Salaries 1,44,000 + outstanding 12,000', s_sal), ('To Rent 66,000 − prepaid 6,000', s_rent), ('To Insurance 12,000 − prepaid 3,000', s_ins),
        ('To Advertisement', 25000), ('To Discount allowed', 6000), ('To Bad debts 4,000 + 5,000 + new provision 8,750 − old provision 7,000', s_bd),
        ('To Depreciation: furniture 8,000; motor van 40,000', d_f + d_v), ('To Interest on bank loan (outstanding)', s_int), ('To Loss by fire (6,000 − claim 4,500)', s_fire),
        ('To Net profit transferred to Capital A/c', np)],
        [('By Gross profit b/d', gp), ('By Commission received 9,000 + accrued 2,000', com)])
    bs1 = bsheet('Balance Sheet of Rao Stores as at 31 March 2027', [
        ('Capital 5,00,000 + net profit 1,43,250 − drawings 64,000 (60,000 + goods 4,000)', cap), ('10% Bank loan', 150000), ('Interest on loan outstanding', s_int),
        ('Outstanding salaries', 12000), ('Trade payables', 126000)], [
        ('Furniture 80,000 − depreciation 8,000', 72000), ('Motor van 2,00,000 − depreciation 40,000', 160000), ('Closing stock', 145000),
        ('Trade receivables 1,80,000 − bad debts 5,000 − provision 8,750', 166250), ('Insurance claim receivable', 4500), ('Prepaid rent', 6000),
        ('Prepaid insurance', 3000), ('Accrued commission', 2000), ('Cash in hand', 22000), ('Cash at bank', bank)])

    # =============== Illustration 2: manager's commission ===============
    c2 = Checks()
    cb = c2.add('220000*10/100', 'Commission on profit before charging it')
    ca = c2.add('220000*10/110', 'Commission on profit after charging it')
    c2.add('220000-20000', 'Profit after commission (case b)')
    c2.add('200000*10/100', 'Proof: 10% of profit after commission equals the commission')

    # =============== Illustration 3: goods on approval and stock taken after year end ===============
    c3 = Checks()
    pend = c3.add('48000-12000', 'Goods still awaiting approval at selling price')
    pend_cost = c3.add('36000*100/120', 'Their cost (selling price is cost + 20%)')
    cos = c3.add('60000*75/100', 'Cost of goods sold 1-10 April (gross profit 25% on sales)')
    stk = c3.add('240000+45000-30000', 'Stock at 31 March from the 10 April count')
    stk_tot = c3.add('255000+30000', 'Closing stock including goods with the customer')
    EAPP = [je('2027 Mar 31', [('Sales A/c', pend)], [('Trade Receivables (customer) A/c', pend)], 'Being sale reversed for goods still awaiting approval'),
            je('Mar 31', [('Stock with Customer on Approval A/c', pend_cost)], [('Trading A/c', pend_cost)], 'Being goods on approval brought into closing stock at cost')]

    # =============== Illustration 4: opening entry for 1 April 2027 (from Illustration 1) ===============
    OPEN = [je('2027 Apr 1', [('Furniture A/c', 72000), ('Motor Van A/c', 160000), ('Stock A/c', 145000), ('Trade Receivables A/c', 175000), ('Insurance Claim A/c', 4500),
                              ('Prepaid Rent A/c', 6000), ('Prepaid Insurance A/c', 3000), ('Accrued Commission A/c', 2000), ('Cash A/c', 22000), ('Bank A/c', bank)],
               [('Provision for Doubtful Debts A/c', newp), ('10% Bank Loan A/c', 150000), ('Interest Outstanding A/c', s_int), ('Outstanding Salaries A/c', 12000),
                ('Trade Payables A/c', 126000), ('Capital A/c', cap)], 'Being balances of assets, liabilities and capital brought forward from 31 March 2027')]
    c4 = Checks()
    c4.add('72000+160000+145000+175000+4500+6000+3000+2000+22000+294000', 'Total of assets debited (debtors at gross 1,75,000)')
    c4.add('8750+150000+7500+12000+126000+579250', 'Total credited (provision shown separately)')

    # =============== Question 1: Kapoor Mart ===============
    q1 = Checks()
    TBQ = [('Capital', -300000), ('Opening stock', 80000), ('Purchases', 420000), ('Sales', -690000), ('Wages', 24000), ('Freight inwards', 9000), ('Salaries', 90000),
           ('Rent and rates', 36000), ('Office expenses', 21000), ('Bad debts', 3000), ('Discount received', -6000), ('Trade receivables', 120000), ('Machinery', 150000),
           ('Furniture', 40000), ('Trade payables', -85000), ('Cash at bank', 58000), ('Drawings', 30000)]
    assert sum(v for _, v in TBQ) == 0
    q1.add('80000+420000+24000+9000+90000+36000+21000+3000+120000+150000+40000+58000+30000', 'Debit total')
    q1.add('300000+690000+6000+85000', 'Credit total')
    qgp = q1.add('690000+95000-(80000+420000+24000+9000)', 'Gross profit')
    qpdd = q1.add('120000*5/100', 'Provision for doubtful debts @5%')
    qdm = q1.add('150000*10/100', 'Depreciation on machinery')
    qdf = q1.add('40000*10/100', 'Depreciation on furniture')
    qnp = q1.add('252000+6000-(100000+30000+21000+3000+6000+15000+4000)', 'Net profit')
    qcap = q1.add('300000+79000-30000', 'Closing capital')
    q1.add('349000+85000+10000', 'Balance sheet total')
    q1.add('135000+36000+95000+114000+6000+58000', 'Balance sheet total — assets')
    trq = tacc('Trading Account of Kapoor Mart for the year ended 31 March 2027', [('To Opening stock', 80000), ('To Purchases', 420000), ('To Wages', 24000), ('To Freight inwards', 9000), ('To Gross profit c/d', qgp)],
               [('By Sales', 690000), ('By Closing stock', 95000)])
    plq = tacc('Profit and Loss Account of Kapoor Mart for the year ended 31 March 2027', [('To Salaries 90,000 + outstanding 10,000', 100000), ('To Rent and rates 36,000 − prepaid 6,000', 30000), ('To Office expenses', 21000),
               ('To Bad debts', 3000), ('To Provision for doubtful debts (5% of 1,20,000)', qpdd), ('To Depreciation: machinery 15,000; furniture 4,000', qdm + qdf), ('To Net profit transferred to Capital A/c', qnp)],
               [('By Gross profit b/d', qgp), ('By Discount received', 6000)])
    bsq = bsheet('Balance Sheet of Kapoor Mart as at 31 March 2027', [('Capital 3,00,000 + net profit 79,000 − drawings 30,000', qcap), ('Trade payables', 85000), ('Outstanding salaries', 10000)],
                 [('Machinery 1,50,000 − depreciation 15,000', 135000), ('Furniture 40,000 − depreciation 4,000', 36000), ('Closing stock', 95000), ('Trade receivables 1,20,000 − provision 6,000', 114000), ('Prepaid rent', 6000), ('Cash at bank', 58000)])

    # =============== Question 3: Trading account with adjustments ===============
    q3 = Checks()
    q3p = q3.add('500000-8000-15000-5000-3000', 'Net purchases after returns, fire, drawings and free samples')
    q3s = q3.add('720000-12000-24000', 'Net sales after returns and goods on approval')
    q3cs = q3.add('75000+24000*100/120', 'Closing stock including goods on approval at cost')
    q3gp = q3.add('684000+95000-(60000+469000+30000+7000)', 'Gross profit')
    q3.add('15000-10000', 'Loss by fire charged to P&L')
    trq3 = tacc('Trading Account of Mehul Traders for the year ended 31 March 2027', [('To Opening stock', 60000), ('To Purchases 5,00,000 − returns 8,000 − fire 15,000 − drawings 5,000 − samples 3,000', q3p),
               ('To Wages', 30000), ('To Carriage inwards', 7000), ('To Gross profit c/d', q3gp)],
                [('By Sales 7,20,000 − returns 12,000 − on approval 24,000', q3s), ('By Closing stock 75,000 + goods on approval at cost 20,000', q3cs)])

    # =============== MCQ figures ===============
    mc = Checks()
    m_gp = mc.add('450000-(50000+300000+10000-70000)', 'GP')
    m_com = mc.add('330000*10/110', 'commission after')
    m_pdd = mc.add('4000+10000+(200000-10000)*5/100-6000', 'P&L charge')
    m_fire = mc.add('50000-35000', 'fire loss to P&L')
    m_app = mc.add('50000*100/125', 'goods on approval at cost')

    # =============== Case ===============
    kc = Checks()
    k_gp = kc.add('900000+110000-(90000+580000+20000)', 'GP')
    k_bd = kc.add('3000+3000+(150000-3000)*4/100-2500', 'charge for bad and doubtful debts')
    k_np = kc.add('320000+5000-(126000+30000+9380+18000)', 'NP')
    k_deb = kc.add('150000-3000-5880', 'net debtors')
    cases = [{
        'id': 'k1', 'title': 'Year-end at Saanvi Fashions', 'difficulty': 'hard',
        'case': ('Saanvi Fashions\' trial balance at 31 March 2027 shows: opening stock ₹90,000; purchases ₹5,80,000; carriage inwards ₹20,000; sales ₹9,00,000; salaries ₹1,26,000; '
                 'rent ₹30,000; bad debts ₹3,000; provision for doubtful debts (credit) ₹2,500; interest received ₹5,000; trade receivables ₹1,50,000; depreciation for the year ₹18,000 (already worked out). '
                 'Closing stock is ₹1,10,000. Additional information: further bad debts ₹3,000 are to be written off and the provision is to be kept at 4% of debtors.'),
        'mcqs': [
            M('k1a', 'What is the gross profit?', [R(k_gp), '₹2,90,000', '₹4,30,000', '₹2,20,000'], 0,
              f'Credit side 9,00,000 + 1,10,000 = 10,10,000; debit side 90,000 + 5,80,000 + 20,000 = 6,90,000; GP = {R(k_gp)}. Salaries and rent are indirect and go to P&L.', 'moderate', '900000+110000-(90000+580000+20000)'),
            M('k1b', 'What is the net amount charged to P&L for bad and doubtful debts?', [R(k_bd), '₹8,880', '₹6,000', '₹11,380'], 0,
              f'Bad debts 3,000 + 3,000 + new provision 4% of 1,47,000 = 5,880 − old provision 2,500 = {R(k_bd)}.', 'hard', '3000+3000+5880-2500'),
            M('k1c', 'What is the net profit?', [R(k_np), '₹1,34,500', '₹1,47,500', '₹1,39,620'], 0,
              f'GP 3,20,000 + interest 5,000 − salaries 1,26,000 − rent 30,000 − bad debts/provision 9,380 − depreciation 18,000 = {R(k_np)}.', 'hard', '320000+5000-126000-30000-9380-18000'),
            M('k1d', 'At what amount do trade receivables appear in the balance sheet?', [R(k_deb), '₹1,47,000', '₹1,44,500', '₹1,50,000'], 0,
              f'1,50,000 − further bad debts 3,000 − new provision 5,880 = {R(k_deb)}.', 'moderate', '150000-3000-5880'),
        ]}]

    adj_tbl = table(['Adjustment (given outside the trial balance)', 'First effect', 'Second effect'], [
        ['Closing stock', 'Credit of Trading A/c', 'Asset in Balance Sheet'],
        ['Outstanding expense', 'Added to that expense (Trading or P&L debit)', 'Current liability'],
        ['Prepaid expense', 'Deducted from that expense', 'Current asset'],
        ['Accrued income', 'Added to that income (P&L credit)', 'Current asset'],
        ['Income received in advance', 'Deducted from that income', 'Current liability'],
        ['Further bad debts', 'P&L debit', 'Deducted from debtors'],
        ['Provision for doubtful debts', 'P&L debit (new provision less old)', 'Deducted from debtors after further bad debts'],
        ['Provision for discount on debtors', 'P&L debit', 'Deducted from debtors after bad debts and doubtful-debt provision'],
        ['Depreciation', 'P&L debit', 'Deducted from the asset'],
        ['Interest on capital', 'P&L debit', 'Added to capital'],
        ['Interest on drawings', 'P&L credit', 'Deducted from capital'],
        ['Goods lost by fire', 'Purchases reduced (or Trading credit) by full cost; uninsured part to P&L', 'Insurance claim admitted shown as asset'],
        ['Goods taken by proprietor', 'Purchases reduced (or Trading credit)', 'Added to drawings, so deducted from capital'],
        ['Free samples', 'Purchases reduced (or Trading credit)', 'Advertisement — P&L debit'],
        ['Goods on approval not yet accepted', 'Sales reduced by selling price; closing stock raised by cost', 'Debtors reduced by selling price; stock in Balance Sheet includes cost'],
    ], title='Every adjustment hits two places')

    viva = [
        V('v1', 'What is the difference between the Trading Account and the Profit and Loss Account?',
          'The Trading Account works out gross profit. It contains opening stock, net purchases, direct expenses such as carriage inwards and godown wages, net sales and closing stock. The Profit and Loss Account works out net profit, starting from the gross profit. It is debited with indirect expenses such as office, selling and finance expenses and losses, and credited with other incomes. The net profit is transferred to the capital account.',
          [P('p1', 'Trading Account finds gross profit', 3, ALT('trading {g}', '{g} trading', 'trading account {g}', g=['gross', 'gross profit', 'gross loss'])),
           P('p2', 'Trading Account carries direct expenses, purchases, sales and stock', 2, 'direct|carriage inward|wages|purchas|stock', min=1),
           P('p3', 'Profit and Loss Account finds net profit', 3, 'loss account net|loss net|net profit found profit loss|net found profit loss|net comes profit loss|net profit shown profit loss|net profit calculated profit loss|net profit ascertained profit loss|net profit worked profit loss|net from profit loss|loss account works out net|loss account calculates net|loss account gives net|loss account shows net'),
           P('p4', 'P&L carries indirect expenses and other incomes', 2, 'indirect|office|selling|administrat|financ|other incom', min=1)], 'c4'),
        V('v2', 'Explain the matching principle and how it affects the year-end adjustments.',
          'The matching principle says that the expenses incurred to earn the revenue of a period must be charged in the same period. So outstanding expenses of the year are added even if not paid, prepaid expenses relating to next year are carried forward as an asset, and income received in advance is shown as a liability and not as this year\'s income.',
          [P('p1', 'Expenses are matched with the revenue of the same period', 4, 'expens|cost', 'revenue|income|sales', 'same period|same year|that period|period|year', min=3),
           P('p2', 'Outstanding expenses are included even if unpaid', 2, 'outstanding|unpaid|accrued|not paid|due but not paid|not yet paid'),
           P('p3', 'Prepaid expenses are carried forward as an asset', 2, 'prepaid|paid in advance|advance payment|paid for next year|advance expens'),
           P('p4', 'Income received in advance is a liability, not current income', 2, 'income received in advance|received in advance|advance income|income in advance|unearned|advance receipt')], 'c2'),
        V('v3', 'How is closing stock valued and where is it shown in the final accounts?',
          'Closing stock is taken at cost or net realisable value, whichever is less. If it is given outside the trial balance, it is credited to the Trading Account and also shown as a current asset in the Balance Sheet. If it already appears in the trial balance, it has been adjusted against purchases, so it is shown only in the Balance Sheet.',
          [P('p1', 'Lower of cost and net realisable value', 4, 'cost', 'net realisable|net realizable|realisable|realizable|nrv|market', 'lower|less|lesser|whichever is lower|lowest', min=3),
           P('p2', 'Outside the trial balance: credit of Trading Account and asset in Balance Sheet', 3, 'credit trading|trading credit|credit side trading|trading account credit|credited trading|credited to trading|trading account and balance sheet|trading and balance sheet', 'balance sheet|asset', min=2),
           P('p3', 'Inside the trial balance: shown only in the Balance Sheet', 3, 'trial balance', 'only balance sheet|balance sheet only|only in balance sheet|just balance sheet|only shown balance sheet|only asset|not trading|not in trading|not again trading|not credited to trading', min=2)], 'c3'),
        V('v4', 'Distinguish between a provision and a reserve.',
          'A provision is a charge against profit made for a known liability or a fall in the value of an asset whose amount cannot be fixed exactly, like a provision for doubtful debts or depreciation. A reserve is an appropriation of profit, set aside to strengthen the business or for a future purpose, and not for any known liability. A provision must be made even if there is a loss, but a reserve is created only out of profits.',
          [P('p1', 'Provision is a charge against profit', 3, 'provision charg|provision is a charg|provision debit|charg provision|provision is charged|provision expens|provision is an expens'),
           P('p2', 'Provision is for a known liability or fall in asset value, amount estimated', 2, 'known liabilit|known loss|diminution|fall in value|decline in value|reduction in value|depreciation|doubtful debt|estimat|cannot be fixed|uncertain amount', min=1),
           P('p3', 'Reserve is an appropriation of profit', 3, 'reserv appropriat|reserv is appropriat|appropriat reserv|reserv out of profit|reserv set aside profit|reserv divis profit|reserv is set aside out of profit|reserv is a part of profit'),
           P('p4', 'Reserve is not for a known liability; created only from profits', 2, 'not for known|no known|not for any known|not for a known|strengthen|future|only profit|only out of profit|only from profit|only when profit|only if profit|general purpose|specific purpose', min=1)], 'c10'),
        V('v5', 'How do you calculate a manager\'s commission on net profit before and after charging such commission?',
          'If the commission is on net profit before charging it, commission equals the profit before commission multiplied by the rate over 100. If the commission is on net profit after charging it, commission equals the profit before commission multiplied by the rate over 100 plus the rate. For example, at 10 percent after charging, it is profit into 10 by 110.',
          [P('p1', 'Before charging: profit before commission × rate/100', 5, ALT('before {x} rate {o} 100', 'before {x} 10 percent', x=['', 'charging', 'charging commission'], o=['', 'over', 'by', 'divided by', 'upon', 'out of'])),
           P('p2', 'After charging: profit before commission × rate/(100 + rate)', 5, '100 plus rate|100 plus the rate|hundred plus rate|100 add rate|100 rate|10 by 110|10 110|10 over 110|10 upon 110|10 divided by 110', min=1)], 'c7'),
        V('v6', 'What is an opening entry and how is it passed?',
          'An opening entry is the first entry in the journal at the start of a new accounting year. It brings forward the closing balances of the previous year from the balance sheet. All asset accounts are debited, and all liabilities and the capital account are credited.',
          [P('p1', 'First entry of the new year bringing forward last year\'s balances', 4, 'first entry|beginning|start|new year|next year|opening', 'balance|balance sheet|previous year|last year|brought forward|carried forward', min=2),
           P('p2', 'Assets are debited', 3, 'asset debit|debit asset|assets are debited|debit all asset|asset accounts are debited|asset account debit'),
           P('p3', 'Liabilities and capital are credited', 3, 'liabilit', 'capital', 'credit', min=3)], 'c9'),
        V('v7', 'State the main limitations of financial statements.',
          'Financial statements are based on historical cost, so they ignore later changes in the value of money and prices. They do not show intangible strengths and weaknesses such as the skill and loyalty of staff. Because the business is assumed to continue but accounts are prepared every year, many costs are spread over years on an estimated basis, so the figures are not exact. And different businesses may follow different accounting policies, which makes comparison difficult.',
          [P('p1', 'Historical cost — ignores changes in the value of money', 3, 'historical|original cost|past cost|inflation|value of money|price change|price level'),
           P('p2', 'Intangible strengths and weaknesses (staff loyalty, skill) not shown', 2, 'intangible|staff|employee|loyalty|skill|human|reputation|not shown|non monetary|qualitative', min=1),
           P('p3', 'Periodic accounts of a going concern need estimates/arbitrary allocation', 2, 'estimat|arbitrar|spread|allocat|approximat|not exact|not absolutely correct|judgement|judgment', min=1),
           P('p4', 'Different accounting policies make comparison difficult', 3, 'polic|method|different practice', 'compar|different|differ', min=2)], 'c11'),
    ]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch07', 'n': 1,
        'title': 'Final Accounts of Non-Manufacturing Entities',
        'outcomes': [
            'Explain what final accounts are and how the income statement (Trading and Profit and Loss Account) and the position statement (Balance Sheet) fit together.',
            'Apply the basic rules for preparing final accounts — capital vs revenue, business vs personal, period cut-off and the matching principle.',
            'Prepare a Trading Account, a Profit and Loss Account and a Balance Sheet of a sole trader from a trial balance with year-end adjustments.',
            'Handle the common adjustments: outstanding, prepaid, accrued and advance items; bad debts and provisions; depreciation; fire loss; goods taken, given away or on approval; manager\'s commission.',
            'Pass closing entries and the opening entry, distinguish provisions from reserves, and explain the limitations of financial statements.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 50, 'practice': 90}, 'prereq': ['fnd-p1-ch02-u03', 'fnd-p1-ch02-u05'],
                 'exam_tip': 'A final-accounts question is a marks bank: every adjustment carries step marks in two places. Tick each adjustment twice (P&L side and Balance Sheet side) as you use it, and show workings for debtors, depreciation and capital.'},
        'concepts': [
            {'id': 'c1', 'title': 'Final accounts of a trading business',
             'body': ['A non-manufacturing (trading) entity buys goods and sells them in the same form — it does not process them. At the year end it prepares financial statements to learn two things: how much it earned (performance) and what it owns and owes (position).',
                      'The income statement is in two stages — the Trading Account (gross profit or gross loss) and the Profit and Loss Account (net profit or net loss). The position statement is the Balance Sheet. Together they are traditionally called "final accounts", though the Balance Sheet is a statement, not an account.',
                      'The income statement covers a period ("for the year ended"); the Balance Sheet speaks of one moment ("as at"). Larger entities may add a cash flow statement and other statements; these are not compulsory for a sole trader.'],
             'analogy': 'The income statement is a video of the year\'s business; the Balance Sheet is a photograph taken at the closing moment.',
             'work': 'Banks ask small traders for final accounts before sanctioning a working-capital limit, and income-tax returns of proprietors are built on these figures. Preparing them is bread-and-butter work for a CA in practice.'},
            {'id': 'c2', 'title': 'Ground rules and the matching principle',
             'body': ['Before drafting final accounts: (a) keep the proprietor\'s personal income and expenses out of the business figures; (b) separate capital from revenue, for both receipts and payments; (c) disclose every material item (an unusual bonus to staff, a big inventory write-off); (d) cut off the year\'s transactions from the next year\'s; (e) record only transactions completed by the year end — goods awaiting the buyer\'s inspection are not yet sales.',
                      'The two statements are linked: of the money spent, part is charged to P&L and the unused part sits in the Balance Sheet (machinery less depreciation; salaries paid plus outstanding salaries as a liability).',
                      'Matching principle: charge against revenue all the expenses incurred to earn it, paid or not (hence outstanding expenses and opening stock in the Trading Account); carry forward costs that will earn next year\'s revenue (prepaid expenses, unexpired cost of assets); and treat money received for next year\'s work as income received in advance (a liability).',
                      'Exception: losses that earn no revenue — uninsured fire loss, stock falling below cost, debts turning bad — are still charged at once, or profit would be overstated.'],
             'analogy': 'Like a cricket scorecard for one match: runs scored and balls bowled in this match only — not the next match\'s practice sessions.',
             'work': 'Cut-off testing is a standard audit procedure: the auditor checks invoices dated just before and after 31 March to make sure sales and purchases are booked in the right year.'},
            {'id': 'c3', 'title': 'The Trading Account',
             'body': ['Debit side: opening stock; purchases less purchase returns; direct expenses — every cost of bringing goods to their present location and condition (carriage/freight inwards, godown wages, customs duty, dock charges, octroi, royalty on goods). Credit side: sales less sales returns; closing stock. Balancing figure: gross profit (debit side, carried to P&L credit) or gross loss.',
                      'Freight or wages spent on installing a fixed asset is added to that asset\'s cost, not charged to Trading. Goods received at year end without an invoice are still recorded as purchases.',
                      'Closing stock is taken at the lower of its cost and its net realisable value, and includes goods with agents on consignment and goods sent on approval. If stock is counted a few days before or after the year end, adjust it to the closing date (sales after the year end are added back at cost, purchases after the year end are deducted).',
                      'If closing stock already appears in the trial balance (adjusted through purchases), it goes only to the Balance Sheet. Closing entries: Trading A/c Dr, To Opening Stock, To Purchases, To direct expenses; Sales A/c Dr and Closing Stock A/c Dr, To Trading A/c; then Trading A/c Dr, To P&L A/c (gross profit).'],
             'analogy': 'The Trading Account is a shopkeeper\'s counter view — what did the goods cost me to get on the shelf, and what did I sell them for?',
             'work': 'Gross profit ratio is the first number an analyst or lender looks at. A sudden fall usually means stock was undervalued, purchases were booked in the wrong year, or there was theft — all things a CA probes.'},
            {'id': 'c4', 'title': 'The Profit and Loss Account',
             'body': ['Starts with gross profit (credit) or gross loss (debit). Debit: all indirect expenses and losses of the year, grouped by function — administration (office salaries, rent, audit fees, legal charges, printing and stationery, electricity), selling and distribution (advertisement, carriage outwards, selling commission, bad debts and provision), finance (interest on loans, bank charges, discount allowed) and abnormal losses (loss by fire, loss on sale of assets). Credit: other incomes — discount received, commission, interest, rent from property let out, dividends, profit on sale of assets.',
                      'Balancing figure: net profit (debit side), transferred to Capital A/c — P&L A/c Dr, To Capital A/c; net loss — Capital A/c Dr, To P&L A/c.',
                      'Not charged to P&L: drawings (they reduce capital); the proprietor\'s income tax (his personal liability, so it is drawings); trade discount (already netted in the invoice). Rebate given to customers who cross a sales target is debited to Rebate A/c and closed to P&L. Bad debts recovered are a gain, credited to P&L, not to the customer.'],
             'analogy': 'If the Trading Account is the counter, the P&L is the whole shop: rent, staff, electricity and interest all come out of the counter\'s gross profit before the owner sees his net profit.',
             'work': 'Disallowances in tax audits often start here — personal expenses of the proprietor booked as business expenses. A CA must reclassify them as drawings before signing.'},
            {'id': 'c5', 'title': 'Adjustments for outstanding, prepaid, accrued and advance items',
             'body': ['Outstanding (accrued) expense: Expense A/c Dr, To Outstanding Expense A/c — added to the expense, shown as a liability.',
                      'Prepaid expense: Prepaid Expense A/c Dr, To Expense A/c — deducted from the expense, shown as an asset.',
                      'Accrued income: Accrued Income A/c Dr, To Income A/c — added to the income, shown as an asset.',
                      'Income received in advance: Income A/c Dr, To Income Received in Advance A/c — deducted from the income, shown as a liability.',
                      'Stock of stationery or similar materials unused at year end is deducted from that expense and shown as an asset. "Outstanding" is used when payment is already due; "accrued" when it relates to the year but falls due later. All these entries are reversed at the start of the next year.'],
             'blocks': [adj_tbl],
             'analogy': 'You pay a year\'s gym membership in February: by 31 March only two months are "used". The remaining ten months are still yours — a prepaid asset.',
             'work': 'Year-end "provisions for expenses" (audit fee, electricity bill not yet received, interest due) are a standard closing checklist item in every accounts department.'},
            {'id': 'c6', 'title': 'Bad debts, provision for doubtful debts and provision for discount',
             'body': ['Bad debt: an amount certainly irrecoverable — Bad Debts A/c Dr, To Debtor; closed to P&L (or set against an existing provision).',
                      'Provision for doubtful debts: a prudent estimate of debts that may not be collected — P&L A/c Dr, To Provision for Doubtful Debts. Customers\' accounts are not touched until a debt actually goes bad.',
                      'Order of working in exams: (1) write off further bad debts from debtors; (2) compute the new provision on the remaining debtors; (3) P&L charge = bad debts (old + further) + new provision − old provision (a negative result is a credit to P&L); (4) Balance Sheet: debtors less further bad debts less new provision.',
                      'Provision for discount on debtors is calculated on debtors after deducting further bad debts and the doubtful-debts provision.'],
             'analogy': 'An umbrella: you buy it (create the provision) before it rains; when rain (an actual bad debt) comes, it falls on the umbrella first, not on your clothes (this year\'s profit).',
             'work': 'Ageing analysis of receivables — how long each invoice has been unpaid — is the usual basis for the provision. Auditors challenge a provision that has not moved while overdue balances have grown.'},
            {'id': 'c7', 'title': 'Other common adjustments',
             'body': ['Depreciation: P&L debit; deducted from the asset in the Balance Sheet. Interest on capital: P&L debit, added to capital. Interest on drawings: P&L credit, deducted from capital.',
                      'Abnormal loss of stock by fire or accident: Loss by Fire A/c Dr, To Purchases (or Trading A/c) with the full cost; then Insurance Claim A/c Dr (admitted amount) and P&L A/c Dr (balance), To Loss by Fire A/c. The claim is an asset until received.',
                      'Goods used other than for sale are removed from purchases at cost and debited to the right head: Drawings (personal use), Advertisement (free samples), Charity/Donation, the asset account (used to build an asset) or Repairs (used in maintenance).',
                      'Goods on approval at year end, still unaccepted: Sales A/c Dr, To Debtor (selling price); and Stock on Approval A/c Dr, To Trading A/c (cost), so they enter closing stock.',
                      'Manager\'s commission on net profit: before charging it = profit before commission × rate/100; after charging it = profit before commission × rate/(100 + rate). Commission A/c Dr, To Commission Payable A/c — P&L debit and a liability.'],
             'analogy': 'Commission "after charging" is like a 10% service charge that is itself part of the bill — you cannot just take 10% of the total; you must take 10/110 of it.',
             'work': 'Profit-linked incentives are common in family businesses. The CA must compute them on the agreed basis; using the wrong formula overpays the manager and understates profit.'},
            {'id': 'c8', 'title': 'The Balance Sheet',
             'body': ['A statement of assets, liabilities and capital as at a particular date — true only for that moment, which is why it says "as at". It is prepared after the P&L, because closing capital needs the net profit. Since capital = assets − liabilities, the two sides must agree; if not, there is an error.',
                      'Order of presentation: by liquidity (cash first, land and building last; current liabilities first, capital last) or by permanence (fixed assets first, cash last; capital first). Investments may be placed by the owner\'s intention.',
                      'Classification: current assets (expected to turn into cash within about a year — stock, debtors, bank, cash, prepaid expenses); non-current or fixed assets (machinery, building, long-term investments); intangible assets (patents, copyrights, goodwill). Liabilities: current (payable within a year — creditors, bills payable, outstanding expenses) and long-term (term loans).',
                      'Sole traders usually use the horizontal form: capital and liabilities on the left, assets on the right. Capital is shown as opening balance + net profit (− net loss) − drawings.'],
             'analogy': 'A Balance Sheet is a selfie of the business at the stroke of midnight on 31 March — one second later, something has changed.',
             'work': 'Lenders compute ratios like current ratio and debt–equity straight off the Balance Sheet. Misclassifying a long-term loan as current can push a client into a loan-covenant breach.'},
            {'id': 'c9', 'title': 'The accounting cycle and the opening entry',
             'body': ['Sequence: record transactions in the journal (and subsidiary books) → post to the ledger → prepare the trial balance → prepare the Trading and Profit and Loss Account → prepare the Balance Sheet. Next year the cycle restarts.',
                      'Opening entry: the first journal entry of a new year, bringing the previous Balance Sheet\'s balances into the new books — all asset accounts debited; all liability accounts, provisions and capital credited. Nominal accounts never appear in it because they were closed to Trading/P&L.'],
             'analogy': 'Closing a school year and opening a new notebook: the first page lists what you are carrying over from last year.',
             'work': 'When a CA takes over books from a previous accountant, the first check is that the opening balances in the software agree with last year\'s audited Balance Sheet.'},
            {'id': 'c10', 'title': 'Provisions and reserves',
             'body': ['Provision: an amount charged to cover depreciation, renewal or a fall in asset values, or a liability that is known to exist but cannot be measured precisely — e.g. provision for doubtful debts, for tax not yet assessed, for discounts. It is a charge against profit and must be made whether there is profit or loss.',
                      'Reserve: an appropriation of profit (revenue or capital) set aside for a general or specific purpose, other than covering a known liability or a fall in asset values. Types: revenue reserves (from trading profits) and capital reserves (from capital profits). Any excess provision beyond what is needed is in substance a reserve.',
                      'Reserve fund: a reserve whose amount is invested outside the business in readily saleable securities, for example to replace an asset in future.'],
             'analogy': 'A provision is money you keep aside because a bill is surely coming; a reserve is savings you choose to keep for a rainy day.',
             'work': 'Under-providing for doubtful debts or tax inflates profit; over-providing creates "secret reserves". Both distort the accounts — auditors test provisions for adequacy and for excess.'},
            {'id': 'c11', 'title': 'Limitations of financial statements',
             'body': ['Historical cost: items are recorded at the money value when the transaction happened; later price changes are ignored, so an old building may appear at a fraction of its present worth.',
                      'Intangible strengths and weaknesses — such as the skill and loyalty of staff — do not appear at all.',
                      'Going concern versus yearly accounts: the business is assumed to last indefinitely, yet results are cut into years, so many costs (depreciation, deferred items) are spread on estimates — the figures are not exact.',
                      'Different accounting policies (valuation methods, treatment of retirement benefits or intangibles) are allowed within limits, so comparing two businesses can mislead unless both follow the same basis. Management\'s own policies also shape the figures.'],
             'analogy': 'A Balance Sheet is like a family photo from years ago kept in today\'s album — accurate for when it was taken, but not a picture of today.',
             'work': 'When advising on a business purchase or a loan, a CA adjusts reported figures (revaluing property, aligning accounting policies) before drawing conclusions.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Complete final accounts with ten adjustments', 'difficulty': 'hard', 'minutes': 40,
             'q': 'From the trial balance of Rao Stores and the information below, prepare for the year ended 31 March 2027 the Trading Account, the Profit and Loss Account and, as at that date, the Balance Sheet. (1) Closing stock at cost ₹1,45,000 (its net realisable value is higher). (2) Salaries outstanding ₹12,000. (3) Rent includes ₹6,000 for April 2027. (4) Insurance prepaid ₹3,000. (5) Write off further bad debts ₹5,000 and keep the provision for doubtful debts at 5% of debtors. (6) Depreciate furniture at 10% and the motor van at 20%. (7) Interest on the bank loan is unpaid. (8) Commission earned but not received ₹2,000. (9) Goods costing ₹4,000 taken by the proprietor were not recorded. (10) Goods costing ₹6,000 were destroyed by fire; the insurer admitted a claim of ₹4,500 (not yet recorded).',
             'given': [tb(TBR, '31 March 2027', 'Trial Balance of Rao Stores as at 31 March 2027')],
             'solution': [trading1, pl1, bs1,
                          wn('Working notes', f'Purchases: 6,40,000 − 10,000 − 4,000 − 6,000 = {R(pur)}. New provision = 5% × (1,80,000 − 5,000) = {R(newp)}; P&L charge = 4,000 + 5,000 + 8,750 − 7,000 = {R(s_bd)}. Interest = 1,50,000 × 10% × 6/12 = {R(s_int)} (loan taken on 1 October). Drawings = 60,000 + 4,000 goods = ₹64,000. Capital = 5,00,000 + {inr(np)} − 64,000 = {R(cap)}.'),
                          note('Fire loss can instead be shown on the credit side of the Trading Account at ₹6,000 (with purchases unchanged); gross profit then rises by ₹6,000 and the ₹1,500 uninsured part still goes to P&L — net profit is the same either way.')],
             'checks': c},
            {'id': 'i2', 'title': "Manager's commission — before and after charging", 'difficulty': 'core', 'minutes': 6,
             'q': 'Net profit of Gupta Electronics before charging the manager\'s commission is ₹2,20,000. Compute the commission at 10% if it is payable (a) on net profit before charging such commission, (b) on net profit after charging such commission. Give the journal entry for case (b).',
             'solution': [table(['Case', 'Formula', 'Commission (₹)', 'Net profit after commission (₹)'], [
                 ['(a) Before charging', '2,20,000 × 10/100', inr(cb), inr(220000 - cb)],
                 ['(b) After charging', '2,20,000 × 10/110', inr(ca), inr(220000 - ca)]]),
                 journal([je('2027 Mar 31', [('Commission A/c', ca)], [('Commission Payable A/c', ca)], 'Being 10% commission on net profit after charging such commission, profit before commission ₹2,20,000')], 'Journal entry — case (b)', 'jc2'),
                 wn('Proof for (b)', f'Profit after commission = 2,20,000 − {inr(ca)} = ₹2,00,000, and 10% of ₹2,00,000 = {R(ca)} — the commission. Commission Payable is a current liability in the Balance Sheet.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Goods on approval and stock counted after the year end', 'difficulty': 'moderate', 'minutes': 12,
             'q': 'Lata Traders counted stock on 10 April 2027 and found ₹2,40,000 at cost. Between 1 and 10 April sales were ₹60,000 (gross profit 25% on sales) and purchases ₹30,000. In March, goods were sent to a customer on approval for ₹48,000 (cost plus 20%) and recorded as a sale; by 31 March the customer had approved goods worth ₹12,000 and the rest were with him, not counted in the stock. Find the closing stock at 31 March 2027 and pass the adjustment entries for the goods on approval.',
             'solution': [table(['Particulars', '₹'], [
                 ['Stock counted on 10 April 2027', '2,40,000'], ['Add: cost of goods sold 1–10 April (60,000 × 75%)', inr(cos)], ['Less: purchases 1–10 April', '-30,000'],
                 ['Stock at 31 March 2027 (in godown)', inr(stk)], ['Add: goods with customer on approval at cost (36,000 × 100/120)', inr(pend_cost)], ['Closing stock for final accounts', inr(stk_tot)]],
                 title='Closing stock as at 31 March 2027'),
                 journal(EAPP, 'Adjustment entries for goods on approval', 'ja3'),
                 wn('Why', f'Only ₹12,000 of the goods were approved, so ₹{inr(pend)} is not yet a sale: reverse it from sales and debtors, and bring the goods back into stock at cost ₹{inr(pend_cost)}. Goods sold after 31 March were in stock on 31 March, so their cost is added back; goods bought after 31 March were not, so they are deducted.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Opening entry for the new year', 'difficulty': 'core', 'minutes': 8,
             'q': 'Using the Balance Sheet of Rao Stores as at 31 March 2027 (Illustration 1), pass the opening entry on 1 April 2027. Show trade receivables at the gross figure with the provision as a separate credit.',
             'solution': [journal(OPEN, 'Opening entry — Rao Stores', 'jo4'), note('Nominal accounts (sales, salaries, rent and so on) do not appear: they were closed to Trading and P&L. The adjustment items (prepaid, outstanding, accrued) are reversed into their expense or income accounts early in the new year.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Closing the books of a retail client', 'role': 'Audit assistant at a CA firm preparing accounts for a proprietor',
             'situation': 'A garment retailer hands you his trial balance on 15 April with a note: "rent of April paid in March, electricity bill for March not received, I took some shirts for my family, and one customer has shut shop owing ₹18,000." He wants final accounts by the month end for his bank.',
             'steps': ['List each item as an adjustment with its two effects: prepaid rent (P&L less, asset), electricity outstanding (P&L more, liability), goods taken (purchases less, drawings more), bad debt (P&L, debtors less).',
                       'Get the stock sheet signed by the proprietor; value at lower of cost and net realisable value — old-season stock may need a write-down.',
                       'Review debtors for further doubtful amounts and agree the provision rate with him.',
                       'Prepare Trading, P&L and Balance Sheet; check that capital closes as opening + profit − drawings.',
                       'Explain to the proprietor why personal items reduce capital rather than appear as expenses.'],
             'takeaway': 'Every adjustment is a pair of entries; missing either half breaks the Balance Sheet.',
             'think': 'The proprietor says, "Show the shirts as advertisement — it saves tax." What should you do?',
             'answer': 'Refuse. Goods for personal use are drawings; recording them as a business expense misstates profit and is improper. Explain the treatment and record them correctly.'},
            {'id': 'j2', 'title': 'Reading final accounts for a loan proposal', 'role': 'Credit analyst at a bank',
             'situation': 'A trader\'s balance sheet shows land bought in 2009 at ₹6 lakh, rising profits and very low provisions for doubtful debts although debtors have doubled.',
             'steps': ['Remember the historical-cost limitation: the land may be worth far more today, so get a valuation if it is offered as security.',
                       'Compare the provision with an ageing of debtors; a stale provision may be inflating profit.',
                       'Check whether stock is valued at cost or NRV and whether any slow-moving stock is included.',
                       'Ask about intangible factors the statements cannot show — key customers, staff, licences.'],
             'takeaway': 'Final accounts are the starting point of analysis, not the end — know their limitations.',
             'think': 'Why might two traders with identical sales and costs report different profits?',
             'answer': 'They may use different accounting policies — e.g. different depreciation methods or provisioning rates — which change reported profit without any change in actual business.'},
        ],
        'mcqs': [
            {'id': 'm1', 'q': 'Opening stock ₹50,000; purchases ₹3,00,000; carriage inwards ₹10,000; sales ₹4,50,000; closing stock ₹70,000. Gross profit is:', 'options': [R(m_gp), '₹1,70,000', '₹90,000', '₹1,20,000'], 'answer': 0, 'check': '450000-(50000+300000+10000-70000)', 'explain': f'Cost of goods sold = 50,000 + 3,00,000 + 10,000 − 70,000 = 2,90,000; GP = 4,50,000 − 2,90,000 = {R(m_gp)}. Ignoring carriage inwards gives ₹1,70,000.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm2', 'q': 'When closing stock appears in the trial balance, it is shown:', 'options': ['Only in the Balance Sheet', 'Only on the credit side of the Trading Account', 'In the Trading Account and the Balance Sheet', 'On the debit side of the Trading Account'], 'answer': 0, 'explain': 'It has already been adjusted against purchases, so crediting it to Trading again would count it twice.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm3', 'q': 'Net profit before the manager\'s commission is ₹3,30,000. Commission at 10% on net profit after charging such commission is:', 'options': [R(m_com), '₹33,000', '₹36,300', '₹29,700'], 'answer': 0, 'check': '330000*10/110', 'explain': f'3,30,000 × 10/110 = {R(m_com)}. ₹33,000 would be the "before charging" figure.', 'concept': 'c7', 'difficulty': 'moderate'},
            {'id': 'm4', 'q': 'Debtors ₹2,00,000; bad debts in the trial balance ₹4,000; further bad debts ₹10,000; provision to be 5% of debtors; old provision ₹6,000. The P&L charge for bad and doubtful debts is:', 'options': [R(m_pdd), '₹18,000', '₹13,500', '₹23,500'], 'answer': 0, 'check': '4000+10000+(200000-10000)*5/100-6000', 'explain': f'4,000 + 10,000 + 5% of 1,90,000 (9,500) − 6,000 = {R(m_pdd)}. Using 5% of 2,00,000 gives ₹18,000.', 'concept': 'c6', 'difficulty': 'hard'},
            {'id': 'm5', 'q': 'The income tax of a sole proprietor paid out of the business bank account is:', 'options': ['Treated as drawings and deducted from capital', 'Debited to the Profit and Loss Account', 'Debited to the Trading Account', 'Shown as an asset'], 'answer': 0, 'explain': 'A sole trader\'s income tax depends on his total income — it is his personal liability, so it is drawings.', 'concept': 'c4', 'difficulty': 'core'},
            {'id': 'm6', 'q': 'Carriage outwards is shown in:', 'options': ['Profit and Loss Account (debit)', 'Trading Account (debit)', 'Balance Sheet (asset)', 'Trading Account (credit)'], 'answer': 0, 'explain': 'Carriage on goods sent to customers is a selling expense, not a cost of bringing goods to the godown.', 'concept': 'c4', 'difficulty': 'core'},
            {'id': 'm7', 'q': 'Which statement is correct?', 'options': ['A provision is a charge against profit; a reserve is an appropriation of profit', 'A reserve is a charge against profit; a provision is an appropriation of profit', 'Both are appropriations of profit', 'A provision is created only when there is profit'], 'answer': 0, 'explain': 'Provisions must be made even in a loss year because they cover known liabilities or falls in asset value; reserves are set aside out of profits.', 'concept': 'c10', 'difficulty': 'core'},
            {'id': 'm8', 'q': 'Goods costing ₹50,000 were destroyed by fire and the insurer admitted ₹35,000. The amount debited to the P&L Account is:', 'options': [R(m_fire), '₹50,000', '₹35,000', '₹85,000'], 'answer': 0, 'check': '50000-35000', 'explain': f'Only the uninsured part {R(m_fire)} is a loss; the admitted claim is an asset until received.', 'concept': 'c7', 'difficulty': 'core'},
            {'id': 'm9', 'q': 'In a Balance Sheet arranged in order of liquidity, the first asset is:', 'options': ['Cash in hand', 'Land and building', 'Stock', 'Trade receivables'], 'answer': 0, 'explain': 'Liquidity order starts with the most liquid asset — cash — and ends with the least liquid.', 'concept': 'c8', 'difficulty': 'core'},
            {'id': 'm10', 'q': 'Goods sent on approval for ₹50,000 (cost plus 25%) are unapproved at the year end. They are added to closing stock at:', 'options': [R(m_app), '₹50,000', '₹37,500', '₹62,500'], 'answer': 0, 'check': '50000*100/125', 'explain': f'Cost = 50,000 × 100/125 = {R(m_app)}. ₹37,500 wrongly deducts 25% of the selling price.', 'concept': 'c7', 'difficulty': 'moderate'},
            {'id': 'm11', 'q': 'Wages paid for installing a new machine should be:', 'options': ['Added to the cost of the machine', 'Debited to the Trading Account', 'Debited to the P&L Account', 'Deducted from capital'], 'answer': 0, 'explain': 'Costs of getting a fixed asset ready for use are part of its cost (capital expenditure).', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm12', 'q': 'Stock at cost is ₹80,000 and its net realisable value is ₹72,000. Closing stock is shown at:', 'options': ['₹72,000', '₹80,000', '₹76,000', '₹8,000'], 'answer': 0, 'check': 'min(80000,72000)', 'explain': 'Lower of cost and net realisable value — ₹72,000.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm13', 'q': 'The correct sequence of the accounting cycle is:', 'options': ['Journal → Ledger → Trial balance → Trading and P&L → Balance Sheet', 'Ledger → Journal → Trial balance → Balance Sheet → P&L', 'Journal → Trial balance → Ledger → P&L → Balance Sheet', 'Trial balance → Journal → Ledger → Balance Sheet → P&L'], 'answer': 0, 'explain': 'Record, post, test, then prepare the income statement and finally the position statement.', 'concept': 'c9', 'difficulty': 'core'},
            {'id': 'm14', 'q': 'In the opening entry:', 'options': ['Assets are debited; liabilities and capital are credited', 'Assets are credited; liabilities and capital are debited', 'Expenses are debited; incomes are credited', 'Only cash and capital are recorded'], 'answer': 0, 'explain': 'Assets have debit balances and liabilities/capital credit balances, so they are brought forward on the same sides.', 'concept': 'c9', 'difficulty': 'core'},
            {'id': 'm15', 'q': 'Rent received includes ₹8,000 for the next year. The ₹8,000 is shown as:', 'options': ['A liability (income received in advance)', 'An asset (accrued income)', 'An addition to rent received in P&L', 'An expense in P&L'], 'answer': 0, 'explain': 'It is not yet earned — deduct it from rent received and show it as a liability.', 'concept': 'c5', 'difficulty': 'core'},
        ],
        'questions': [
            {'id': 'q1', 'marks': 10, 'minutes': minutes(10), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'From the trial balance of Kapoor Mart, prepare for the year ended 31 March 2027 the Trading Account, the Profit and Loss Account and, as at that date, the Balance Sheet, after considering: (1) closing stock ₹95,000; (2) salaries outstanding ₹10,000; (3) rent prepaid ₹6,000; (4) depreciation on machinery and furniture at 10%; (5) provision for doubtful debts at 5% of debtors.',
             'given': [tb(TBQ, '31 March 2027', 'Trial Balance of Kapoor Mart as at 31 March 2027')],
             'model': [trq, plq, bsq],
             'scheme': [{'id': 's1', 'pt': 'Trading Account items and closing stock', 'm': 2, 'skill': 'classification'},
                        {'id': 's2', 'pt': 'Gross profit ₹2,52,000', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'P&L: outstanding salaries and prepaid rent adjusted', 'm': 1, 'skill': 'application'},
                        {'id': 's4', 'pt': 'P&L: provision ₹6,000 and depreciation ₹19,000', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's5', 'pt': 'Net profit ₹79,000', 'm': 1, 'skill': 'computation'},
                        {'id': 's6', 'pt': 'Capital: opening + profit − drawings = ₹3,49,000', 'm': 1, 'skill': 'computation'},
                        {'id': 's7', 'pt': 'Assets net of depreciation/provision; prepaid rent and outstanding salaries shown', 'm': 1.5, 'skill': 'presentation'},
                        {'id': 's8', 'pt': 'Balance Sheet totals agree at ₹4,44,000 with proper headings', 'm': 1, 'skill': 'presentation'}],
             'remarks': ['Most candidates get the Trading Account right; marks slip in the Balance Sheet, where only one half of an adjustment is shown.', 'Drawings debited to P&L is still seen every attempt — it costs both the net-profit and capital marks.'],
             'mistakes': ['Showing prepaid rent as a liability.', 'Calculating the provision on debtors after deducting it twice.', 'Leaving drawings out of the capital working.'],
             'tips': ['Head each statement fully: "… for the year ended 31 March 2027" and "Balance Sheet as at …".', 'Use inner columns for "less depreciation" and "add outstanding" so the examiner sees each adjustment.'],
             'checks': q1},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'table',
             'q': 'Distinguish between a provision and a reserve.',
             'model': [table(['Basis', 'Provision', 'Reserve'], [
                 ['Nature', 'A charge against profit', 'An appropriation of profit'],
                 ['Purpose', 'To meet a known liability or a fall in the value of an asset whose amount is not exactly known', 'To strengthen the business or meet a general/specific future need; not for a known liability'],
                 ['Need for profit', 'Must be made even if there is a loss', 'Created only when there is profit'],
                 ['Effect on profit', 'Reduces net profit (shown on the debit of P&L)', 'Does not reduce net profit; set aside out of it'],
                 ['Presentation', 'Usually deducted from the asset concerned or shown as a liability', 'Shown with capital / under reserves on the liabilities side'],
                 ['Examples', 'Provision for doubtful debts, depreciation, tax', 'General reserve, capital reserve, reserve fund'],
             ])],
             'scheme': [{'id': 's1', 'pt': 'Charge vs appropriation', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Purpose', 'm': 1, 'skill': 'concept'},
                        {'id': 's3', 'pt': 'Profit needed or not', 'm': 1, 'skill': 'concept'}, {'id': 's4', 'pt': 'Effect on profit / presentation', 'm': 1, 'skill': 'concept'},
                        {'id': 's5', 'pt': 'Correct examples', 'm': 1, 'skill': 'application'}],
             'remarks': ['The "charge vs appropriation" line is expected in every answer — candidates who miss it rarely score above half.'],
             'mistakes': ['Calling provision for doubtful debts a reserve.', 'Saying a reserve reduces net profit.'],
             'tips': ['Use a table with five or six bases.', 'Give one example on each side.']},
            {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'ledger',
             'q': 'Mehul Traders: opening stock ₹60,000; purchases ₹5,00,000; purchase returns ₹8,000; sales ₹7,20,000; sales returns ₹12,000; wages ₹30,000; carriage inwards ₹7,000. Closing stock counted ₹75,000 (excluding goods with a customer). Not yet recorded: (a) goods costing ₹15,000 destroyed by fire, claim admitted ₹10,000; (b) goods costing ₹5,000 taken by the proprietor; (c) goods costing ₹3,000 distributed as free samples. Also, goods sent on approval for ₹24,000 (cost plus 20%) were recorded as a sale; approval is still awaited. Prepare the Trading Account for the year ended 31 March 2027 and state where the other effects appear.',
             'model': [trq3, wn('Other effects', 'P&L debit: loss by fire ₹5,000 (15,000 − 10,000) and advertisement ₹3,000. Balance Sheet: insurance claim ₹10,000 (asset); drawings increase by ₹5,000 (deducted from capital); debtors reduced by ₹24,000; closing stock ₹95,000.')],
             'scheme': [{'id': 's1', 'pt': 'Purchases net ₹4,69,000 (returns, fire, drawings, samples deducted)', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Sales net ₹6,84,000 (returns and goods on approval)', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Closing stock ₹95,000 including goods on approval at cost', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Gross profit ₹2,13,000', 'm': 1, 'skill': 'computation'},
                        {'id': 's5', 'pt': 'Other effects: fire loss, samples, claim, drawings, debtors', 'm': 1.5, 'skill': 'application'}],
             'remarks': ['The goods-on-approval adjustment has two parts; many answers reduce sales but forget to add the goods to stock at cost.', 'Valuing the goods at selling price instead of cost is a common slip.'],
             'mistakes': ['Adding goods on approval to stock at ₹24,000.', 'Charging the whole ₹15,000 fire loss to P&L.', 'Not reducing purchases for drawings and samples.'],
             'tips': ['Show deductions from purchases in an inner column.', 'Write a one-line note of the P&L and Balance Sheet effects — it carries marks.'],
             'checks': q3},
            {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': 'Explain any four limitations of financial statements.',
             'model': [ul(['Historical cost: assets are carried at what they cost when bought, so price changes since then are ignored and old assets look understated.',
                           'Intangible strengths and weaknesses — staff skill, customer loyalty, management quality — are not shown at all.',
                           'Periodic accounts of a continuing business: costs such as depreciation are spread over years on estimates, so annual figures are approximations.',
                           'Different accounting policies (stock valuation, depreciation methods, treatment of retirement benefits) are permitted, so comparison between businesses can mislead; management policies also influence the figures.'])],
             'scheme': [{'id': f's{i}', 'pt': t, 'm': 1, 'skill': 'concept'} for i, t in enumerate(['Historical cost', 'Intangibles not shown', 'Estimates / arbitrary allocation', 'Different accounting policies'], 1)],
             'remarks': ['Each point should be explained in one or two lines; one-word lists earn little.'],
             'mistakes': ['Listing errors of book-keeping (which a trial balance may catch) as limitations of statements.'],
             'tips': ['Number your points and give a short example for each.']},
        ],
        'revision': {
            'summary': ['Trading A/c → gross profit (opening stock, net purchases, direct expenses vs net sales, closing stock). P&L → net profit (indirect expenses vs other incomes). Balance Sheet → position as at the year end.',
                        'Matching: charge all expenses of the year (paid or not), carry forward costs for next year, defer income received in advance; losses are charged immediately.',
                        'Each adjustment has two effects — one in Trading/P&L and one in the Balance Sheet.',
                        'Bad debts → new provision on remaining debtors → charge = bad debts + new − old provision; discount provision comes after.',
                        'Commission on profit: before = P × r/100; after = P × r/(100 + r).',
                        'Provision = charge against profit; reserve = appropriation of profit. Opening entry: assets Dr, liabilities and capital Cr.'],
            'remember': ['Closing stock in the trial balance → Balance Sheet only.', 'Drawings and proprietor\'s income tax never go to P&L.', 'Stock is taken at cost or net realisable value, whichever is less.'],
            'traps': ["Don't value goods on approval at selling price — use cost.", "Don't calculate the new provision before deducting further bad debts.", "Don't forget to add goods taken by the proprietor to drawings when reducing purchases."],
        },
        'quickref': [
            {'k': 'Cost of goods sold', 'v': 'Opening stock + net purchases + direct expenses − closing stock'},
            {'k': 'Gross profit', 'v': 'Net sales − cost of goods sold'},
            {'k': 'Net profit', 'v': 'Gross profit + other incomes − indirect expenses and losses'},
            {'k': 'Closing capital', 'v': 'Opening capital + net profit (− net loss) + fresh capital − drawings'},
            {'k': 'Bad & doubtful debts charge', 'v': 'Bad debts (old + further) + new provision − old provision'},
            {'k': 'Commission on profit', 'v': 'Before charging: P × r/100; after charging: P × r/(100 + r)'},
            {'k': 'Fire loss', 'v': 'Purchases (or Trading Cr) full cost; P&L = cost − claim admitted; claim = asset'},
            {'k': 'Goods on approval', 'v': 'Sales Dr To Debtor (selling price); Stock on Approval Dr To Trading (cost)'},
            {'k': 'Stock counted after year end', 'v': 'Count + cost of sales since year end − purchases since year end'},
            {'k': 'Opening entry', 'v': 'Assets Dr. To Liabilities, Provisions, Capital'},
        ],
        'viva': viva, 'cases': cases,
    }
