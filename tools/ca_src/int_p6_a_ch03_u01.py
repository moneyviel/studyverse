"""CA Intermediate · Paper 6A Financial Management · Chapter 3 Financial Analysis and Planning – Ratio Analysis.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch03-u01'
T1 = 'Ratios and ratio analysis'
T2 = 'Liquidity ratios'
T3 = 'Leverage: capital structure and coverage ratios'
T4 = 'Activity (turnover) ratios'
T5 = 'Profitability ratios: sales and return on investment'
T6 = 'DuPont analysis of ROE'
T7 = 'Owner and market ratios'
T8 = 'Users, applications and limitations'
T9 = 'Building statements from ratios'


def build():
    ck = Checks()
    cr = ck.add('1200000/500000', 'Current ratio = CA 12,00,000 ÷ CL 5,00,000')
    qr = ck.add('(1200000-500000-100000)/500000', 'Quick ratio = (CA − inventory − prepaid) ÷ CL')
    cash = ck.add('200000/500000', 'Cash ratio')
    de = ck.add('800000/1700000', 'Debt-equity (long-term debt ÷ equity of 17,00,000)')
    icr = ck.add('480000/80000', 'Interest coverage = EBIT ÷ interest')
    itr = ck.add('3600000/((300000+500000)/2)', 'Inventory turnover = COGS ÷ average inventory')
    dtr = ck.add('4800000/400000', 'Debtors turnover = credit sales ÷ debtors')
    acp = ck.add('360/12', 'Average collection period (days, 360-day year)')
    tat = ck.add('4800000/3000000', 'Total assets turnover')
    gp = ck.add('1200000/4800000*100', 'Gross profit ratio %')
    np_ = ck.add('300000/4800000*100', 'Net profit ratio %')
    opr = ck.add('(3600000+720000)/4800000*100', 'Operating ratio %')
    roce = ck.add('480000/(1700000+800000)*100', 'ROCE (pre-tax) %')
    roe = ck.add('300000/1700000*100', 'ROE %')
    eps = ck.add('300000/100000', 'EPS (1,00,000 shares)')
    po = ck.add('1.2/3*100', 'Dividend payout %')
    pe = ck.add('36/3', 'P/E ratio')
    dy = ck.add('1.2/36*100', 'Dividend yield %')
    bs = table(['Liabilities', '₹', 'Assets', '₹'], [
        ['Equity share capital (₹10 each)', inr(1000000), 'Fixed assets (net)', inr(1800000)],
        ['Reserves and surplus', inr(700000), 'Inventory', inr(500000)],
        ['10% Debentures', inr(800000), 'Debtors', inr(400000)],
        ['Creditors', inr(300000), 'Cash and bank', inr(200000)],
        ['Outstanding expenses', inr(50000), 'Prepaid expenses', inr(100000)],
        ['Bank overdraft', inr(150000), '', ''],
        ['Total', inr(3000000), 'Total', inr(3000000)]], title='Sahyadri Ltd. — Balance Sheet (31 March)')
    pl = table(['Particulars', '₹'], [
        ['Sales (all credit)', inr(4800000)], ['Less: Cost of goods sold', inr(3600000)], ['Gross profit', inr(1200000)],
        ['Less: Operating expenses', inr(720000)], ['EBIT', inr(480000)], ['Less: Interest on debentures', inr(80000)],
        ['Profit before tax', inr(400000)], ['Less: Tax @ 25%', inr(100000)], ['Profit after tax', inr(300000)]], title='Statement of profit (year)')
    ratios = table(['Ratio', 'Working', 'Result'], [
        ['Current ratio', '12,00,000 ÷ 5,00,000', f'{cr} : 1'],
        ['Quick ratio', '(12,00,000 − 5,00,000 − 1,00,000) ÷ 5,00,000', f'{qr} : 1'],
        ['Cash ratio', '2,00,000 ÷ 5,00,000', f'{cash} : 1'],
        ['Debt-equity', '8,00,000 ÷ 17,00,000', f'{de} : 1'],
        ['Interest coverage', '4,80,000 ÷ 80,000', f'{icr} times'],
        ['Inventory turnover', '36,00,000 ÷ 4,00,000', f'{itr} times'],
        ['Debtors turnover / collection period', '48,00,000 ÷ 4,00,000; 360 ÷ 12', f'{dtr} times; {acp} days'],
        ['Total assets turnover', '48,00,000 ÷ 30,00,000', f'{tat} times'],
        ['Gross profit ratio', '12,00,000 ÷ 48,00,000', f'{gp}%'],
        ['Net profit ratio', '3,00,000 ÷ 48,00,000', f'{np_}%'],
        ['Operating ratio', '(36,00,000 + 7,20,000) ÷ 48,00,000', f'{opr}%'],
        ['ROCE (pre-tax)', '4,80,000 ÷ (17,00,000 + 8,00,000)', f'{roce}%'],
        ['ROE', '3,00,000 ÷ 17,00,000', f'{roe}%'],
        ['EPS', '3,00,000 ÷ 1,00,000 shares', R(eps)],
        ['Dividend payout', '1.20 ÷ 3.00', f'{po}%'],
        ['P/E ratio', '36 ÷ 3', f'{pe} times'],
        ['Dividend yield', '1.20 ÷ 36', f'{dy}%']], title='Ratios computed')
    i1 = {'id': 'i1', 'title': 'A full ratio set from one set of statements', 'difficulty': 'core', 'minutes': 15,
          'q': 'From the statements of Sahyadri Ltd. below, compute the main liquidity, leverage, activity, profitability and market ratios. Opening inventory was ₹3,00,000; dividend ₹1.20 per share; market price ₹36 per share; use a 360-day year.',
          'solution': [bs, pl, ratios,
                       p(f'Comment: liquidity is comfortable (current ratio {cr}, quick ratio {qr}); debt is modest and interest is covered {icr} times. Inventory moves {itr} times a year and customers pay in about {acp} days. ROCE of {roce}% exceeds the 10% debenture rate, so borrowing has helped equity earn {roe}%.'),
                       note('Capital employed here = equity + long-term debt (₹25,00,000) = total assets − current liabilities.')],
          'checks': list(ck)}

    ck2 = Checks()
    nm = 300000 / 4800000; at = 4800000 / 3000000; em = 3000000 / 1700000
    dup = ck2.add('round(300000/4800000*4800000/3000000*3000000/1700000*100,2)', 'ROE by DuPont %')
    nodebt = ck2.add('round(300000/4800000*4800000/3000000*100,2)', 'Return on assets (margin × turnover) %')
    i2 = {'id': 'i2', 'title': 'DuPont breakdown of ROE', 'difficulty': 'core', 'minutes': 6,
          'q': 'Using Sahyadri Ltd. (PAT ₹3,00,000; sales ₹48,00,000; total assets ₹30,00,000; equity ₹17,00,000), break ROE into its DuPont components and explain what drives it.',
          'solution': [table(['Component', 'Formula', 'Value'], [
              ['Net profit margin', 'PAT ÷ Sales', f'{round(nm * 100, 2)}%'],
              ['Asset turnover', 'Sales ÷ Total assets', f'{round(at, 2)} times'],
              ['Equity multiplier', 'Total assets ÷ Equity', f'{round(em, 4)} times'],
              ['ROE', 'Margin × Turnover × Multiplier', f'{dup}%']], title='DuPont'),
              p(f'Margin × turnover alone gives {nodebt}% (return on assets). The equity multiplier of about {round(em, 2)} — the use of borrowed and other outside funds — lifts ROE to {dup}%. A rise in ROE driven only by the multiplier signals more risk, not better operations.')],
          'checks': list(ck2)}

    ck3 = Checks()
    cl = ck3.add('600000/(2.5-1)', 'Current liabilities = WC ÷ (CR − 1)')
    ca = ck3.add('2.5*400000', 'Current assets')
    inv = ck3.add('1000000-1.5*400000', 'Inventory = CA − quick assets')
    cogs = ck3.add('6*400000', 'COGS = inventory turnover × inventory')
    sales = ck3.add('2400000/0.8', 'Sales = COGS ÷ (1 − gross margin 20%)')
    debt = ck3.add('3000000*36/360', 'Debtors = sales × 36 ÷ 360')
    cash3 = ck3.add('1000000-400000-300000', 'Cash = CA − inventory − debtors')
    i3 = {'id': 'i3', 'title': 'Working back from ratios', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Konkan Traders: working capital ₹6,00,000; current ratio 2.5; quick ratio 1.5; inventory turnover (on cost of goods sold, closing stock) 6 times; gross profit 20% of sales; average collection period 36 days (360-day year, all sales on credit). Current assets consist of inventory, debtors and cash only. Find current liabilities, current assets, inventory, sales, debtors and cash.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Current liabilities', 'CA − CL = 6,00,000 and CA = 2.5 CL → 1.5 CL = 6,00,000', inr(cl)],
              ['Current assets', '2.5 × 4,00,000', inr(ca)],
              ['Inventory', 'CA − quick assets (1.5 × 4,00,000)', inr(inv)],
              ['Cost of goods sold', '6 × 4,00,000', inr(cogs)],
              ['Sales', '24,00,000 ÷ 0.80', inr(sales)],
              ['Debtors', '30,00,000 × 36 ÷ 360', inr(debt)],
              ['Cash', '10,00,000 − 4,00,000 − 3,00,000', inr(cash3)]], title='Derived figures'),
              note('Inventory turnover is on cost, so find COGS first and then gross up to sales.')],
          'checks': list(ck3)}

    liq = table(['Ratio', 'Formula', 'Reading'], [
        ['Current ratio', 'Current assets ÷ Current liabilities', 'About 2 : 1 is the traditional norm; depends on the business'],
        ['Quick (acid-test) ratio', '(CA − Inventories − Prepaid expenses) ÷ CL', 'About 1 : 1 considered satisfactory'],
        ['Cash (absolute liquidity) ratio', '(Cash and bank + Marketable securities) ÷ CL', 'Strictest test'],
        ['Basic defence interval', '(Cash + Receivables + Marketable securities) ÷ Daily cash operating expenses', 'Days the firm can run if revenue stops'],
        ['Net working capital', 'CA − CL (excluding short-term bank borrowing)', 'An amount, watched by bankers'],
    ], title='Liquidity ratios')
    lev = table(['Ratio', 'Formula'], [
        ['Equity ratio', 'Shareholders\' equity ÷ Net assets (capital employed)'],
        ['Debt ratio', 'Total debt ÷ Net assets'],
        ['Debt-equity ratio', 'Total debt (or long-term debt) ÷ Shareholders\' equity'],
        ['Debt to total assets', 'Total debt (or outside liabilities) ÷ Total assets'],
        ['Capital gearing', '(Preference capital + Debentures + Other borrowed funds) ÷ (Equity capital + Reserves − Losses)'],
        ['Proprietary ratio', '(Equity + Preference capital + Reserves) ÷ Total assets'],
        ['Debt service coverage (DSCR)', 'Earnings available for debt service ÷ (Interest + Instalments)'],
        ['Interest coverage', 'EBIT ÷ Interest'],
        ['Preference dividend coverage', 'PAT ÷ Preference dividend'],
        ['Fixed charges coverage', '(EBIT + Depreciation) ÷ (Interest + Loan repayment)'],
    ], title='Leverage ratios')
    act = table(['Ratio', 'Formula'], [
        ['Total / fixed / current assets turnover', 'Sales (or COGS) ÷ respective assets'],
        ['Capital (net assets) turnover', 'Sales (or COGS) ÷ Capital employed'],
        ['Working capital turnover', 'Sales (or COGS) ÷ Working capital'],
        ['Inventory turnover', 'COGS ÷ Average inventory (raw material: consumption ÷ average RM stock)'],
        ['Receivables turnover; collection period', 'Credit sales ÷ Average receivables; 360 (or 365) ÷ turnover'],
        ['Payables turnover; payment period', 'Credit purchases ÷ Average payables; 360 (or 365) ÷ turnover'],
    ], title='Activity ratios')
    prof = table(['Ratio', 'Formula'], [
        ['Gross profit ratio', 'Gross profit ÷ Sales × 100'],
        ['Net profit ratio', 'PAT ÷ Sales × 100 (pre-tax version uses PBT)'],
        ['Operating profit ratio', 'EBIT (operating profit) ÷ Sales × 100'],
        ['Operating ratio', '(COGS + Operating expenses) ÷ Sales × 100'],
        ['Return on assets', 'PAT (or PAT + interest, or EBIT(1 − t)) ÷ Average total assets'],
        ['ROCE', 'EBIT ÷ Capital employed × 100 (post-tax: EBIT(1 − t))'],
        ['ROE', '(PAT − Preference dividend) ÷ Equity shareholders\' funds × 100'],
    ], title='Profitability ratios')
    mkt = table(['Ratio', 'Formula'], [
        ['EPS', 'Profit available to equity ÷ Number of equity shares'],
        ['DPS', 'Equity dividend ÷ Number of equity shares'],
        ['Dividend payout', 'DPS ÷ EPS'],
        ['P/E ratio', 'Market price per share ÷ EPS'],
        ['Dividend yield', 'DPS ÷ Market price × 100'],
        ['Earnings yield', 'EPS ÷ Market price × 100'],
        ['Market value / book value', 'Market price ÷ (Net worth ÷ Number of shares)'],
        ['Tobin\'s Q', 'Market value of the firm ÷ Replacement cost of its assets'],
    ], title='Owner and market ratios')
    users = table(['User', 'Main interest', 'Ratios mostly used'], [
        ['Shareholders', 'Profitability and growth', 'EPS, DPS, P/E, payout'],
        ['Investors', 'Overall financial health and outlook', 'Profitability, capital structure, solvency, turnover'],
        ['Lenders', 'Safety of loans', 'Coverage, solvency, turnover, profitability'],
        ['Trade creditors', 'Payment on due date', 'Liquidity ratios'],
        ['Employees', 'Overall strength vs competitors', 'Liquidity, solvency, profitability, ROI'],
        ['Government / regulators', 'Taxes and compliance', 'Profitability'],
        ['Managers', 'Their own function (production, sales, finance)', 'Input-output, turnover, expense, ROI, capital structure'],
    ], title='Who uses which ratios')

    concepts = [
        C('c1', T1, [
            'A financial ratio expresses the relationship between two accounting figures (or groups of figures) that are logically connected — for example current assets and current liabilities.',
            'A single figure says little; related to another figure, compared with past years (intra-firm or trend comparison), with other firms (inter-firm) or with the industry, it becomes informative.',
            'Data sources: annual reports, interim statements, notes to accounts, cash flow statements, business periodicals and credit or investment advisory services.',
            'Ratios fall into four groups: liquidity, leverage (capital structure and coverage), activity (turnover) and profitability (sales-based, return on investment, owner\'s view and market-based). Liquidity should be read together with the turnover ratios.',
            'Working rules: match numerator and denominator (e.g. EBIT with capital employed, PAT with equity); use averages when available; state assumptions when information is incomplete.'],
          'A ratio is like a speedometer reading — 60 means little until you know whether it is km per hour on a highway or in a school zone.',
          'Analysts\' reports on listed companies are built around a page of key ratios compared over five years and against peers.'),
        C('c2', T2, [
            'Liquidity (short-term solvency) is the ability to pay short-term liabilities on time. Too little liquidity damages credit; too much means idle funds.',
            'Current ratio = current assets ÷ current liabilities; traditionally 2 : 1 is acceptable, but the right level depends on the business.',
            'Quick ratio removes inventories and prepaid expenses — inventory may sell only at distress prices in a crisis; about 1 : 1 is considered satisfactory unless most quick assets are slow-paying debtors.',
            'Cash ratio uses only cash, bank and marketable securities. Basic defence interval tells how many days cash operating expenses can be met if revenues stop. Net working capital is an amount, often a loan condition.'],
          'The current ratio asks "can I pay this month\'s bills with everything I own short-term?"; the quick ratio asks "can I pay them without selling my stock?".',
          'Banks set a minimum current ratio (often around 1.33) when sanctioning working-capital limits.',
          blocks=[liq]),
        C('c3', T3, [
            'Leverage ratios show the mix of owners\' and lenders\' funds and the firm\'s ability to pay interest and repay principal.',
            'Capital structure ratios: equity ratio, debt ratio, debt-equity, debt to total assets, capital gearing (fixed-return capital to equity funds) and proprietary ratio. A high debt-equity means less cushion for creditors and higher financial risk.',
            'Coverage ratios compare fixed claims (interest, preference dividend, instalments) with the earnings available to pay them. DSCR = (PAT + depreciation and other non-cash charges + interest ± adjustments) ÷ (interest + instalments); 1.5–2 is usually satisfactory.',
            'Interest coverage = EBIT ÷ interest; EBIT is used because interest is paid before tax. A high ratio means interest is safe even if profits fall.'],
          'Leverage ratios are a lender\'s X-ray: how much of the body is borrowed, and is the heart (earnings) strong enough to pump the EMIs?',
          'Term-loan agreements commonly require a minimum DSCR and a maximum debt-equity.',
          blocks=[lev]),
        C('c4', T4, [
            'Activity ratios show how efficiently assets are used to generate sales — measured in times (or days).',
            'Asset turnovers: total, fixed, current, capital employed and working capital. A very high working capital turnover may mean the firm is short of working capital. Old, depreciated plant can make the fixed assets turnover look high.',
            'Inventory turnover = COGS ÷ average inventory (opening + closing ÷ 2). High = fast-moving stock; low = slow or obsolete stock.',
            'Receivables turnover = credit sales ÷ average receivables; collection period = 360 (or 365) ÷ turnover. Payables turnover uses credit purchases; payment period is the average days taken to pay suppliers. Comparing the two shows whether suppliers are funding customers.'],
          'Turnover ratios are the rotation speed of money: rupee → stock → debtor → cash → rupee; the faster the wheel turns, the less money is needed.',
          'Retail chains track inventory days obsessively; a few extra days of stock can lock up crores.',
          blocks=[act]),
        C('c5', T5, [
            'Sales-based: gross profit ratio, net profit ratio, operating profit ratio (EBIT ÷ sales) and expense ratios (COGS, operating expenses, operating ratio, financial expenses).',
            'Return on investment (ROI) = return ÷ investment = profit margin × investment turnover — ROI can improve through better margins, faster turnover or both.',
            'ROA uses total (or tangible or fixed) assets; ROCE = EBIT ÷ capital employed, where capital employed = total assets − current liabilities = fixed assets + working capital = equity + long-term debt. Include intangibles but exclude fictitious assets. ROCE should exceed the borrowing rate.',
            'ROE = (PAT − preference dividend) ÷ equity shareholders\' funds; it shows the return earned for owners.'],
          'Margin is how much you keep from each sale; turnover is how many times you sell — a kirana store and a jewellery shop can earn the same ROI in opposite ways.',
          'Investors screen for companies whose ROCE comfortably exceeds their cost of capital year after year.',
          blocks=[prof]),
        C('c6', T6, [
            'The DuPont system (developed at E.I. du Pont de Nemours in 1919) splits ROE into three parts: net profit margin × asset turnover × equity multiplier.',
            'Net profit margin = PAT ÷ sales; asset turnover = sales ÷ total assets; equity multiplier = total assets ÷ equity (a measure of financial leverage).',
            'The split shows whether ROE comes from operations (margin, turnover) or from leverage. A high ROE built mainly on borrowing is riskier than one built on margins and asset use.',
            'Margins and turnover are often inversely related — high-volume, low-margin and low-volume, high-margin models can be compared on equal terms.'],
          'DuPont is like splitting a cricket team\'s score into batting, bowling and extras — you see whether the runs came from skill or from luck (borrowed money).',
          'Equity analysts routinely present DuPont tables when comparing banks, retailers and manufacturers.'),
        C('c7', T7, [
            'Owner ratios: EPS (profit for equity ÷ number of shares), DPS, and dividend payout (DPS ÷ EPS) — the balance shows how much is retained.',
            'Market ratios: P/E = market price ÷ EPS (higher can mean expected growth or overvaluation); dividend yield = DPS ÷ market price; earnings yield = EPS ÷ market price; market-to-book = market price ÷ book value per share.',
            'Tobin\'s Q = market value of the firm ÷ replacement cost of its assets; Q = 1 is equilibrium, below 1 may suggest undervaluation and above 1 overvaluation.',
            'Dividend rate (%) is on face value; yield is on market price and is the true return to an investor buying at market.'],
          'P/E tells how many years of current earnings the market is paying for a share today.',
          'Financial websites display P/E, dividend yield and price-to-book for every listed share.',
          blocks=[mkt]),
        C('c8', T8, [
            'Different users stress different ratios (table). Ratios help assess liquidity, long-term solvency, operating efficiency and overall profitability, enable inter-firm comparison and support budgeting and forecasting.',
            'Limitations: diversified product lines make aggregate ratios hard to compare; inflation distorts historical-cost figures; seasonal factors make year-end figures unrepresentative; window dressing at year end; differences in accounting policies and periods; no universal standard ratio; difficulty in judging good or bad (a very high current ratio may mean idle funds); ratios are interrelated and must be read together.',
            'Ratios give clues, not conclusions — interpretation needs judgement.',
            'Horizontal analysis compares statements across years; vertical analysis expresses each item of one year as a percentage of a base (sales, total assets) — useful for inter-firm comparison.'],
          'Ratios are symptoms on a medical report — a doctor still has to examine the patient before diagnosing.',
          'Credit analysts adjust for seasonality and window dressing before relying on a borrower\'s year-end ratios.',
          blocks=[users]),
        C('c9', T9, [
            'Exams often give ratios and ask for the underlying figures. Work from the most direct link first.',
            'Typical chain: working capital and current ratio → current liabilities and current assets; quick ratio → inventory; inventory turnover → cost of goods sold; gross margin → sales; collection period → debtors; balancing figure → cash.',
            'Watch the basis: inventory turnover may be on cost or on sales; collection period may use 360 or 365 days; turnover may use closing or average figures — state the assumption.'],
          'Constructing statements from ratios is like solving a sudoku: fill the cell with only one possible value first and the rest follow.',
          'Analysts use the same logic to project next year\'s balance sheet from target ratios in a budget.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Credit appraisal of a new customer', 'role': 'Credit analyst at a supplier',
         'situation': 'A customer wants 60 days\' credit for ₹40 lakh of goods a month.',
         'steps': ['Compute current, quick and cash ratios and the payables payment period.', 'Check interest coverage and debt-equity for stress.', 'Compare with industry norms and decide limit and terms.'],
         'takeaway': 'Trade creditors rely mainly on liquidity ratios and the payment period.'},
        {'id': 'j2', 'title': 'Explaining a jump in ROE', 'role': 'Analyst preparing a board note',
         'situation': 'ROE rose from 14% to 19% while sales were flat.',
         'steps': ['Run a DuPont split for both years.', 'Find that the equity multiplier rose because of new borrowing; margins and turnover barely moved.', 'Flag higher financial risk in the note.'],
         'takeaway': 'Always ask whether ROE improved through operations or through leverage.'},
    ]

    mcqs = [
        Q('m1', 'Quick ratio is calculated as:', ['(Current assets − Inventories − Prepaid expenses) ÷ Current liabilities', 'Current assets ÷ Current liabilities', 'Cash ÷ Current liabilities', 'Current assets ÷ Total assets'], 0,
          'Quick assets exclude inventories and prepaid expenses because they cannot be turned into cash quickly; the ratio compares these with current liabilities. Current assets ÷ current liabilities is the current ratio. In practice: a quick ratio near 1 : 1 is usually considered satisfactory.', 'c2', T2),
        Q('m2', f'Sahyadri Ltd. has current assets ₹12,00,000 (inventory ₹5,00,000, prepaid ₹1,00,000) and current liabilities ₹5,00,000. Its quick ratio is:',
          [f'{qr} : 1', f'{cr} : 1', '1.4 : 1', '0.4 : 1'], 0,
          f'Quick assets = 12,00,000 − 5,00,000 − 1,00,000 = 6,00,000; 6,00,000 ÷ 5,00,000 = {qr}. The trap {cr} is the current ratio, and 1.4 forgets to remove prepaid expenses. In practice: always check what is inside current assets before computing liquidity.', 'c2', T2, 'moderate'),
        Q('m3', 'Interest coverage ratio uses EBIT in the numerator because:', ['Interest is paid out of profit before tax', 'Tax is paid before interest', 'Depreciation is a cash expense', 'EBIT excludes sales'], 0,
          'Interest is a tax-deductible expense paid before tax, so the earnings available to meet it are earnings before interest and tax. Using PAT would understate the capacity. In practice: lenders want EBIT to cover interest several times over.', 'c3', T3),
        Q('m4', 'Capital gearing ratio compares:', ['Fixed-return capital (preference capital and borrowings) with equity shareholders\' funds', 'Current assets with current liabilities', 'Sales with total assets', 'EBIT with interest'], 0,
          'Capital gearing compares funds carrying a fixed return — preference capital, debentures and other borrowings — with equity funds (equity capital plus reserves less losses). A high ratio means high gearing and more risk for equity. In practice: highly geared firms see larger swings in EPS.', 'c3', T3),
        Q('m5', 'Debt service coverage ratio is:', ['Earnings available for debt service ÷ (Interest + Instalments)', 'EBIT ÷ Interest', 'Total debt ÷ Equity', 'PAT ÷ Preference dividend'], 0,
          'DSCR compares earnings available for debt service — PAT plus non-cash charges such as depreciation plus interest — with the total of interest and loan instalments due. EBIT ÷ interest is interest coverage. In practice: banks usually look for DSCR between 1.5 and 2.', 'c3', T3),
        Q('m6', 'Average inventory is ₹4,00,000 and cost of goods sold is ₹36,00,000. Inventory turnover is:', [f'{itr} times', '12 times', '0.11 times', '7.2 times'], 0,
          f'Inventory turnover = COGS ÷ average inventory = 36,00,000 ÷ 4,00,000 = {itr} times; stock is replaced about every 40 days. 12 would wrongly use sales of ₹48,00,000. In practice: compare with peers, since normal turnover differs widely between industries.', 'c4', T4, 'core', check=itr),
        Q('m7', 'Credit sales are ₹48,00,000 and average debtors ₹4,00,000. With a 360-day year, the average collection period is:', [f'{acp} days', '12 days', '45 days', '60 days'], 0,
          f'Receivables turnover = 48,00,000 ÷ 4,00,000 = 12 times; collection period = 360 ÷ 12 = {acp} days. 12 is the turnover, not days. In practice: compare the collection period with the credit period allowed to customers.', 'c4', T4, 'core', check=acp),
        Q('m8', 'Capital employed can be measured as:', ['Total assets − Current liabilities', 'Total assets + Current liabilities', 'Current assets − Fixed assets', 'Equity − Long-term debt'], 0,
          'Capital employed equals total assets less current liabilities, which also equals fixed assets plus working capital or equity plus long-term debt. Fictitious assets are excluded. In practice: ROCE is computed on this base to judge return on all long-term funds.', 'c5', T5),
        Q('m9', 'ROI can be expressed as:', ['Net profit margin × Investment turnover', 'Net profit margin ÷ Investment turnover', 'Sales × Investment', 'EPS × P/E ratio'], 0,
          'ROI = profit ÷ investment = (profit ÷ sales) × (sales ÷ investment), i.e. margin × turnover, so it can rise through either. EPS × P/E gives market price, not ROI. In practice: discount retailers earn ROI through turnover, luxury brands through margin.', 'c5', T5),
        Q('m10', 'In the DuPont model, the equity multiplier equals:', ['Total assets ÷ Shareholders\' equity', 'Sales ÷ Total assets', 'PAT ÷ Sales', 'Debt ÷ Equity'], 0,
          'The equity multiplier is total assets divided by shareholders\' equity; it measures how far assets are funded by outside money and so captures leverage. Sales ÷ assets is turnover and PAT ÷ sales is margin. In practice: a rising multiplier lifts ROE but also risk.', 'c6', T6),
        Q('m11', 'Net profit margin 6.25%, asset turnover 1.6 times and equity multiplier 1.7647. ROE is approximately:', [f'{dup}%', f'{nodebt}%', '9.40%', '28.24%'], 0,
          f'ROE = 0.0625 × 1.6 × 1.7647 ≈ {dup}%. Margin × turnover alone gives {nodebt}%, the return on assets; the difference comes from leverage. In practice: DuPont tells you how much of ROE is operational and how much is financial.', 'c6', T6, 'moderate', check=dup),
        Q('m12', 'P/E ratio is:', ['Market price per share ÷ EPS', 'EPS ÷ Market price per share', 'DPS ÷ EPS', 'Market price ÷ Book value per share'], 0,
          'P/E = market price per share divided by earnings per share; it shows how many rupees investors pay for each rupee of current earnings. EPS ÷ price is the earnings yield and DPS ÷ EPS is the payout ratio. In practice: high P/E often reflects expected growth.', 'c7', T7),
        Q('m13', 'Tobin\'s Q ratio compares:', ['Market value of the firm with the replacement cost of its assets', 'Market price with EPS', 'Book value with market value of debt', 'Sales with replacement cost'], 0,
          'Tobin\'s Q is the market value of a firm divided by the replacement cost of its assets; Q equal to 1 is equilibrium, below 1 suggests undervaluation and above 1 overvaluation. Market price ÷ EPS is P/E. In practice: Q above 1 encourages firms to invest in new assets.', 'c7', T7, 'moderate'),
        Q('m14', 'Which is a limitation of ratio analysis?', ['Year-end window dressing can distort ratios', 'Ratios always give final conclusions', 'Ratios ignore all accounting data', 'Ratios cannot be compared across years'], 0,
          'Firms may adjust year-end figures to improve popular ratios such as the current ratio, so ratios can mislead; inflation, seasonality and differing policies also distort them. Ratios give clues, not conclusions, and trend comparison across years is a key use. In practice: analysts look at quarterly data to see through window dressing.', 'c8', T8),
        Q('m15', 'Trade creditors are mainly interested in:', ['Liquidity ratios', 'P/E ratio', 'Dividend payout ratio', 'Tobin\'s Q'], 0,
          'Suppliers want to know whether the firm can pay on the due date, so they focus on liquidity (short-term solvency) ratios. P/E, payout and Q interest shareholders and investors. In practice: suppliers also check the customer\'s payables payment period.', 'c8', T8),
        Q('m16', 'Expressing each item of one year\'s profit statement as a percentage of sales is:', ['Vertical analysis', 'Horizontal analysis', 'Trend analysis over years', 'DuPont analysis'], 0,
          'Vertical analysis analyses a single year by expressing items as a percentage of a base — sales for the profit statement and total assets for the balance sheet. Horizontal (trend) analysis compares several years. In practice: common-size statements make firms of different sizes comparable.', 'c8', T8),
        Q('m17', 'Working capital ₹6,00,000 and current ratio 2.5. Current liabilities are:', [R(cl), R(ca), '₹2,40,000', '₹15,00,000'], 0,
          f'CA = 2.5 CL and CA − CL = 6,00,000, so 1.5 CL = 6,00,000 and CL = {R(cl)}; CA = {R(ca)}. Dividing 6,00,000 by 2.5 is the usual trap. In practice: set up the two equations before computing.', 'c9', T9, 'moderate', check=cl),
    ]

    questions = [
        W('q1', 8, i1['q'] + ' (Compute any eight ratios and comment.)', i1['solution'],
          [S('s1', 'Current and quick ratios', 1, 'computation', 'current', nums=[cr, qr]),
           S('s2', 'Debt-equity and interest coverage', 1, 'computation', 'debt|interest', nums=[de, icr]),
           S('s3', 'Inventory turnover', 1, 'computation', 'inventory|stock', nums=[itr]),
           S('s4', 'Debtors turnover / collection period', 1, 'computation', 'debtor|collection|receivable', nums=[acp]),
           S('s5', 'GP and NP ratios', 1, 'computation', 'gross|net profit', nums=[gp, np_]),
           S('s6', 'ROCE and ROE', 1, 'computation', 'roce|capital employed|roe|equity', nums=[roce, roe]),
           S('s7', 'EPS and P/E', 1, 'computation', 'eps|p/e|earning', nums=[eps, pe]),
           S('s8', 'Comment on position', 1, 'interpretation', 'comfortable|satisfactory|good|sound|healthy|adequate')],
          ['Show the formula, the working and the result for each ratio.'], ['Using sales instead of COGS for inventory turnover.', 'Leaving debentures out of capital employed.'], ['Use a three-column table: ratio, working, result.'], pad='table', checks=list(ck)),
        W('q2', 6, i3['q'], i3['solution'],
          [S('s1', 'Current liabilities and current assets', 2, 'computation', 'current liabilit', nums=[cl, ca]),
           S('s2', 'Inventory', 1, 'computation', 'inventory|stock', nums=[inv]),
           S('s3', 'Sales via COGS', 1, 'computation', 'sales', nums=[sales]),
           S('s4', 'Debtors and cash', 2, 'computation', 'debtor|cash', nums=[debt, cash3])],
          ['Follow the chain: WC → CL → CA → inventory → COGS → sales → debtors → cash.'], ['Applying inventory turnover to sales when it is on cost.'], ['One line per derived figure.'], pad='table', difficulty='hard', checks=list(ck3)),
        W('q3', 5, 'Discuss the limitations of financial ratios.',
          [ul(['Diversified product lines make aggregate ratios hard to compare.', 'Inflation distorts historical-cost figures.', 'Seasonal factors make year-end figures unrepresentative.',
               'Window dressing at year end improves popular ratios.', 'Different accounting policies and periods reduce comparability.', 'No universal standard ratio; industry averages may be too high or too low a benchmark.',
               'Hard to say whether a ratio is good or bad — a very high current ratio may mean idle funds.', 'Ratios are interrelated and must be read together; they give clues, not conclusions.'])],
          [S('s1', 'Inflation / historical cost', 1, 'concept', 'inflation|historical'),
           S('s2', 'Seasonal factors', 1, 'concept', 'season'),
           S('s3', 'Window dressing', 1, 'concept', 'window dressing|year end adjust|year-end adjust'),
           S('s4', 'Different accounting policies', 1, 'concept', 'accounting polic|different polic'),
           S('s5', 'No standard / interpretation difficulty / interrelated', 1, 'concept', 'standard|interrelat|inter related|good or bad|clue', n=1)],
          ['Five well-explained points earn full marks.'], ['Listing ratios instead of limitations.'], ['Short bullet points with a one-line explanation each.']),
    ]

    viva = [
        V('v1', 'Why are inventories excluded from quick assets?',
          'Inventories are excluded because they take time to convert into cash, and in a crisis they may sell only at liquidation value. Prepaid expenses are excluded too.',
          [P('p1', 'Not quickly convertible to cash', 6, 'cash', 'take time|takes time|slow|time to convert|time to sell'), P('p2', 'May fetch only distress/liquidation value', 4, 'liquidation|distress|lower value|forced')], 'c2'),
        V('v2', 'State the formula for return on capital employed and the meaning of capital employed.',
          'ROCE is EBIT divided by capital employed multiplied by 100. Capital employed is total assets less current liabilities, which equals equity plus long term debt.',
          [P('p1', 'EBIT ÷ capital employed', 5, 'ebit|earnings before interest'), P('p2', 'Total assets − current liabilities (or equity + long-term debt)', 5, 'current liabilit|long term debt|long-term debt|working capital')], 'c5'),
        V('v3', 'What are the three components of ROE in the DuPont model?',
          'Net profit margin, asset turnover and the equity multiplier. ROE equals their product.',
          [P('p1', 'Net profit margin', 3, 'margin'), P('p2', 'Asset turnover', 3, 'turnover'), P('p3', 'Equity multiplier', 4, 'multiplier|leverage')], 'c6'),
        V('v4', 'What does a high P/E ratio indicate?',
          'A high P/E means investors pay many rupees per rupee of current earnings. It may reflect expectations of high future growth, or that the share is overvalued.',
          [P('p1', 'Expected growth', 5, 'growth'), P('p2', 'Possible overvaluation', 5, 'overvalu|over valu|expensive|costly')], 'c7'),
        V('v5', 'Give any three limitations of ratio analysis.',
          'Inflation distorts historical figures, seasonal factors and window dressing distort year end figures, and different accounting policies make firms hard to compare.',
          [P('p1', 'Inflation', 3, 'inflation|historical'), P('p2', 'Seasonality or window dressing', 4, 'season|window'), P('p3', 'Different accounting policies', 3, 'polic|comparab')], 'c8'),
    ]

    cases = [{'id': 'k1', 'title': 'Two retailers, same ROE', 'difficulty': 'moderate',
              'case': 'Bazaar Mart: net margin 2%, asset turnover 5 times, equity multiplier 1.5. Heritage Silks: net margin 10%, asset turnover 0.75 times, equity multiplier 2.0. Bazaar Mart\'s current ratio is 0.9 but it collects cash at the counter; Heritage Silks\' current ratio is 3.2 with inventory turnover of 1.5 times.',
              'mcqs': [
                  M('k1a', 'ROE of each company is:', ['15% for both', '10% and 15%', '15% and 20%', '3% and 15%'], 0,
                    'Bazaar Mart: 2% × 5 × 1.5 = 15%; Heritage Silks: 10% × 0.75 × 2.0 = 15%. Both earn the same ROE through very different models — low margin, high turnover versus high margin, low turnover. In practice: DuPont reveals these differences behind identical ROEs.', 'moderate', topic=T6),
                  M('k1b', 'Which company relies more on leverage for its ROE?', ['Heritage Silks', 'Bazaar Mart', 'Both equally', 'Neither uses leverage'], 0,
                    'Heritage Silks has the higher equity multiplier (2.0 vs 1.5), so more of its assets are financed by outside funds and leverage contributes more to ROE. Its return on assets is only 7.5% versus Bazaar Mart\'s 10%. In practice: higher leverage means higher financial risk.', 'moderate', topic=T6),
                  M('k1c', 'Bazaar Mart\'s current ratio of 0.9 is:', ['Not necessarily alarming, because it sells for cash and turns stock quickly', 'A sure sign of insolvency', 'Better than 2 : 1 in all cases', 'Irrelevant for retailers'], 0,
                    'Cash-sale businesses with rapid stock turnover can operate safely below the 2 : 1 norm, since cash comes in daily. Liquidity ratios must be read with turnover ratios. In practice: supermarkets often run current ratios below 1.', 'core', topic=T2),
                  M('k1d', 'Heritage Silks\' high current ratio with slow inventory turnover suggests:', ['Funds locked in slow-moving stock rather than strong liquidity', 'Excellent liquidity in all respects', 'Low gearing', 'High P/E'], 0,
                    'A current ratio of 3.2 looks strong, but inventory turning only 1.5 times a year shows much of it is stock that is slow to convert into cash. A high ratio is not always good — it may signal inefficient working capital management. In practice: check the quick ratio too.', 'moderate', topic=T4),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch03', 1, 'Financial Analysis and Planning – Ratio Analysis',
                ['Explain ratio analysis, its data sources and classification.',
                 'Compute and interpret liquidity, leverage, activity, profitability and market ratios.',
                 'Break ROE into DuPont components.',
                 'Identify users\' needs, applications and limitations of ratios; distinguish horizontal and vertical analysis.',
                 'Construct financial figures from given ratios.'],
                {'difficulty': 'core', 'minutes': {'learn': 50, 'practice': 50}, 'prereq': ['int-p6-a-ch01-u01'],
                 'exam_tip': 'Expect a 10-mark computation (compute ratios or prepare statements from ratios) plus short theory on limitations or DuPont. Show formula → working → answer.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Four groups: liquidity, leverage, activity, profitability (incl. market).', 'Current 2 : 1, quick 1 : 1 are traditional norms — business-specific.',
                             'Interest coverage = EBIT ÷ interest; DSCR includes instalments.', 'Inventory turnover on COGS; collection period = 360 ÷ debtors turnover.',
                             'Capital employed = total assets − current liabilities = equity + long-term debt.', 'ROE = margin × turnover × equity multiplier (DuPont).',
                             'Ratios give clues, not conclusions; watch inflation, seasonality, window dressing, policies.'],
                 'remember': ['Match numerator with denominator (EBIT ↔ capital employed; PAT − pref. div ↔ equity).', 'Use averages when available and state assumptions.'],
                 'traps': ['Do not divide working capital by the current ratio to get CL.', 'Prepaid expenses are excluded from quick assets.', 'Inventory turnover on cost vs sales — check the basis.']},
                [('Quick ratio', '(CA − Inventory − Prepaid) ÷ CL'), ('Interest coverage', 'EBIT ÷ Interest'), ('ROCE', 'EBIT ÷ (Total assets − CL)'),
                 ('DuPont ROE', 'Margin × Turnover × Equity multiplier'), ('P/E', 'MPS ÷ EPS'), ('Tobin\'s Q', 'Market value ÷ Replacement cost')],
                viva, cases,
                topics=['Introduction', 'Ratio and Ratio Analysis', 'Types of Ratios', 'Liquidity Ratios', 'Long-term Solvency Ratios / Leverage Ratios', 'Activity Ratios',
                        'Profitability Ratios', 'Users and Objective of Financial Analysis', 'Application of Ratio Analysis in Financial Decision Making', 'Limitations of Financial Ratios',
                        'Financial Analysis', 'Summary of Ratios'])
