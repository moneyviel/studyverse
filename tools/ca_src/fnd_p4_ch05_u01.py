"""CA Foundation · Paper 4 Business Economics · Chapter 5 Determination of National Income · Unit 1 National Income Accounting.
Original explanations, numbers and questions. Every figure is computed in code and re-checked by tools/ca_validate.py."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p4-ch05-u01'


def Q(i, q, o, a, e, c, d='core', check=None, topic=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'concept': c, 'difficulty': d}
    if topic: m['topic'] = topic
    if check: m['check'] = check
    return m


def M(i, q, o, a, e, d='moderate', check=None, topic=None):
    m = {'id': i, 'q': q, 'options': o, 'answer': a, 'explain': e, 'difficulty': d}
    if topic: m['topic'] = topic
    if check: m['check'] = check
    return m


def build():
    # ---------- Illustration 1: the aggregates ----------
    c1 = Checks()
    os1 = c1.add('500+400+900', 'operating surplus = rent + interest + profit')
    ndpfc = c1.add('2400+1800+1300', 'NDP at FC = CoE + OS + mixed income')
    gdpfc = c1.add('5500+600', 'GDP at FC = NDP FC + CFC')
    gdpmp = c1.add('6100+700', 'GDP at MP = GDP FC + NIT')
    gnpmp = c1.add('6800+(-90)', 'GNP at MP = GDP MP + NFIA')
    nnpmp = c1.add('6710-600', 'NNP at MP = GNP MP - CFC')
    nnpfc = c1.add('6110-700', 'NNP at FC = NNP MP - NIT (national income)')
    nnpfc2 = c1.add('5500+(-90)', 'cross-check: NI = NDP FC + NFIA')
    t1 = table(['Aggregate', 'How obtained', '₹ crore'], [
        ['Operating surplus', 'Rent 500 + Interest 400 + Profit 900', inr(os1)],
        ['NDP at factor cost', 'CoE 2,400 + OS 1,800 + Mixed income 1,300', inr(ndpfc)],
        ['GDP at factor cost', 'NDP FC + Depreciation 600', inr(gdpfc)],
        ['GDP at market prices', 'GDP FC + Net indirect taxes 700', inr(gdpmp)],
        ['GNP at market prices', 'GDP MP + NFIA (−90)', inr(gnpmp)],
        ['NNP at market prices', 'GNP MP − Depreciation 600', inr(nnpmp)],
        ['NNP at factor cost (National Income)', 'NNP MP − NIT 700', inr(nnpfc)],
    ], title='From factor incomes to every aggregate (₹ crore)')

    # ---------- Illustration 2: GDP deflator ----------
    c2 = Checks()
    yrs = [('Year 1 (base)', 800, 800), ('Year 2', 990, 900), ('Year 3', 1150, 1000), ('Year 4', 1200, 1050)]
    rows2, defl = [], []
    for y, n, r in yrs:
        d = c2.add(f'{n}/{r}*100', f'deflator {y}')
        defl.append(d)
        rows2.append([y, inr(n), inr(r), str(d)])
    inf2 = c2.add('(110-100)/100*100', 'inflation year 2')
    inf3 = c2.add('(115-110)/110*100', 'inflation year 3')
    inf4 = c2.add('(1200/1050*100-115)/115*100', 'inflation year 4')
    t2 = table(['Year', 'Nominal GDP (₹ ’000 crore)', 'Real GDP at base-year prices', 'GDP deflator'], rows2, num=[1, 2, 3], title='GDP deflator')
    realx = c2.add('1452/120*100', 'real GDP when nominal 1452 and deflator 120')

    # ---------- Illustration 3: value added method ----------
    c3 = Checks()
    vo_p = c3.add('1500+(240-200)', 'primary: value of output = sales + change in stock')
    va_p = c3.add('1540-300', 'primary GVA')
    vo_s = c3.add('3200+(150-250)', 'secondary: value of output')
    va_s = c3.add('3100-1400', 'secondary GVA')
    vo_t = c3.add('2100+0', 'tertiary: value of output')
    va_t = c3.add('2100-600', 'tertiary GVA')
    gdp3 = c3.add('1240+1700+1500', 'GDP MP = sum of GVA MP')
    ndp3 = c3.add('4440-380', 'NDP MP')
    ndpfc3 = c3.add('4060-(520-90)', 'NDP FC')
    ni3 = c3.add('3630+40', 'national income')
    t3 = table(['Sector', 'Sales', 'Change in stock', 'Value of output', 'Intermediate consumption', 'GVA at MP'], [
        ['Primary', '1,500', '+40', inr(vo_p), '300', inr(va_p)],
        ['Secondary', '3,200', '−100', inr(vo_s), '1,400', inr(va_s)],
        ['Tertiary', '2,100', '0', inr(vo_t), '600', inr(va_t)],
        ['Total (GDP at MP)', '', '', '', '', inr(gdp3)],
    ], num=[5], total=True, title='Value added by sector (₹ crore)')

    # ---------- Illustration 4: expenditure vs income method ----------
    c4 = Checks()
    gdcf = c4.add('1100+400', 'GDCF = NDCF + CFC')
    gdp4 = c4.add('4200+1300+1500+(-200)', 'GDP MP by expenditure')
    ni4e = c4.add('6800-400-650+50', 'NI by expenditure method')
    os4 = c4.add('400+450+900', 'OS')
    ni4i = c4.add('3100+1750+900+50', 'NI by income method')

    # ---------- Illustration 5: personal and disposable income ----------
    c5 = Checks()
    priv = c5.add('9000-220-80+180+300+120', 'private income')
    pi5 = c5.add('9300-350-400', 'personal income')
    pi5b = c5.add('9000-220-80-350-400+180+300+120', 'personal income direct')
    di5 = c5.add('8550-600-50', 'disposable personal income')

    # ---------- written questions ----------
    w1 = Checks()
    w1_gdpmp = w1.add('3200+1450+1100+500+600', 'GDP MP = CoE + OS + MI + CFC + NIT')
    w1_gnpmp = w1.add('6850+(-60)', 'GNP MP')
    w1_nnpmp = w1.add('6790-500', 'NNP MP')
    w1_ni = w1.add('6290-600', 'NNP FC')
    w2 = Checks()
    w2_vo = w2.add('820+(60-90)', 'value of output')
    w2_gva = w2.add('790-310', 'GVA MP')
    w2_nva = w2.add('480-45', 'NVA MP')
    w2_nvafc = w2.add('435-(70-20)', 'NVA FC')
    w3 = Checks()
    w3_gdp = w3.add('2600+700+(560+140)+(-80)', 'GDP MP by expenditure')
    w3_ni_e = w3.add('3920-140-(210)+30', 'NI by expenditure')
    w3_ni_i = w3.add('1900+(250+300+650)+470+30', 'NI by income')

    # ---------- case ----------
    k = Checks()
    k_gdp = k.add('5400+1800+2100+300', 'case GDP MP')
    k_ni = k.add('9600-900-1100+(-150)', 'case NI')
    k_pc = k.add('7450*10000000/50000000', 'case per capita NI in ₹ (NI ₹7,450 crore, population 5 crore)')
    k_defl = k.add('9600/8000*100', 'case GDP deflator')

    concepts = [
        {'id': 'c1', 'title': 'National income accounting — meaning, who compiles it, why it matters', 'body': [
            'National income accounting is the set of macro-economic accounts that traces the economy from production of goods and services through to their final use. It defines the concepts (GDP, NNP and so on) and builds measures for them. It was pioneered by Simon Kuznets and Richard Stone, both Nobel laureates.',
            'In India the national accounts are compiled by MoSPI\'s Central Statistical Organisation (CSO) (MoSPI = Ministry of Statistics and Programme Implementation); State Directorates of Economics and Statistics (DESs) compile State Domestic Product. (Real-world note: in 2019 the CSO and NSSO were merged into the National Statistical Office (NSO) within MoSPI; the study material uses the name CSO, so answer "CSO" if that is the option offered.)',
            'Uses: (i) businesses use it to forecast demand; (ii) it shows the structure of income by sector and how that structure shifts over time; (iii) government uses sectoral data to frame sector-specific policies; (iv) it gives a quantitative base for macro-economic models and for assessing policies; (v) it throws light on income distribution and allows ratios such as investment, tax or fiscal deficit to GDP; (vi) international comparisons of income and living standards help decide eligibility and terms for loans and aid; (vii) combined with monetary data it guides policy on growth and inflation.'],
         'analogy': 'National accounts are the economy\'s financial statements: GDP is the "turnover", depreciation the wear and tear, NNP the "net" figure.',
         'work': 'Equity analysts, bankers and CFOs read GDP releases to forecast demand; CAs use nominal GDP growth as a sanity check on a client\'s revenue projections.'},
        {'id': 'c2', 'title': 'GDP — nominal, real and the GDP deflator', 'body': [
            'Gross Domestic Product at market prices (GDP MP) is the market value of all final goods and services that are produced inside a country\'s domestic territory over a period (usually a year), before deducting depreciation. Only final goods are counted, to avoid double counting.',
            'Nominal GDP (GDP at current prices) values output at the prices of the same year, so it can rise because output rises or because prices rise. Real GDP (GDP at constant prices) values output at the prices of a chosen base year, so it changes only with quantities.',
            'GDP deflator = (Nominal GDP ÷ Real GDP) × 100. It is a price index: it is 100 in the base year; above 100 means prices are higher than in the base year. Real GDP = Nominal GDP ÷ deflator × 100, and Nominal GDP = Real GDP × deflator ÷ 100.',
            'Inflation between two years = (Deflator in year 2 − Deflator in year 1) ÷ Deflator in year 1 × 100. If the deflator falls from one year to the next, the price level has fallen.'],
         'analogy': 'Nominal GDP is your salary in rupees; real GDP is what that salary can actually buy.',
         'work': 'When a client reports 12% revenue growth in a year of 7% inflation, the CA points out that real growth is only about 5% — the deflator logic applied to a company.'},
        {'id': 'c3', 'title': 'Gross vs net, domestic vs national', 'body': [
            'Gross vs net: the difference is depreciation (consumption of fixed capital). Net = Gross − Depreciation. So NDP MP = GDP MP − Depreciation.',
            'Domestic vs national: the difference is net factor income from abroad (NFIA). National = Domestic + NFIA. GNP MP = GDP MP + NFIA. NFIA = factor income earned by our residents abroad − factor income earned by non-residents in our territory = net income from property and entrepreneurship + net compensation of employees + net retained earnings of resident companies abroad.',
            'GDP counts what is produced inside the country by anyone; GNP counts what is earned by the country\'s normal residents anywhere. Profit of a foreign company\'s factory in India is in India\'s GDP but in its home country\'s GNP.',
            'NNP MP = GNP MP − Depreciation = NDP MP + NFIA = GDP MP + NFIA − Depreciation. If NFIA is positive, GNP > GDP; if negative, GNP < GDP.'],
         'analogy': 'Domestic = "made in India"; national = "made by Indians". The gap between them is NFIA.',
         'work': 'For countries with large remittance or profit outflows, the gap between GDP and GNP changes the picture of income available to residents — relevant in sovereign-risk and country-risk notes.'},
        {'id': 'c4', 'title': 'Market price, factor cost and basic price', 'body': [
            'Market price and factor cost differ by net indirect taxes (indirect taxes − subsidies). Market price = Factor cost + Indirect taxes − Subsidies; Factor cost = Market price − Indirect taxes + Subsidies.',
            'GDP FC = GDP MP − NIT. Built up from incomes it equals CoE + OS + mixed income + depreciation, where OS (operating surplus) is rent, interest and profit taken together.',
            'Basic price sits in between: Basic price = Factor cost + Production taxes − Production subsidies; Market price = Basic price + Product taxes − Product subsidies. Product taxes (like GST) are levied per unit of product; production taxes (like land revenue, stamp duty, professional tax) are paid because of production activity, not per unit. So market price includes both kinds of taxes and excludes both kinds of subsidies. India reports gross value added (GVA) at basic prices.'],
         'blocks': [table(['From', 'To', 'Adjust by'], [['Gross', 'Net', '− Depreciation (CFC)'], ['Domestic', 'National', '+ NFIA'], ['Market price', 'Factor cost', '− Indirect taxes + Subsidies (− NIT)'], ['Factor cost', 'Basic price', '+ Production taxes − Production subsidies'], ['Basic price', 'Market price', '+ Product taxes − Product subsidies']], title='Three switches between aggregates')],
         'analogy': 'Factor cost is what the cook, the landlord and the owner receive; market price is what you pay at the counter after GST and before any subsidy.',
         'work': 'CAs see the same idea in company accounts: revenue is shown net of GST because indirect tax is collected for the government, not earned by the firm.'},
        {'id': 'c5', 'title': 'National income and related aggregates', 'body': [
            'NDP FC = sum of factor incomes earned in the domestic territory = CoE + OS + mixed income. It is also called domestic (factor) income.',
            'National income = NNP FC = factor income of normal residents = NDP FC + NFIA. If NFIA > 0, national income exceeds domestic factor income.',
            'Per capita income = GDP (or national income) ÷ population — a rough indicator of living standards.',
            'Personal income (PI) is the current income actually received by households (including non-profit institutions serving households) from all sources, earned or not. PI = NI + incomes received but not earned (transfer payments such as pensions, scholarships, unemployment allowance, interest on national debt) − incomes earned but not received (undistributed corporate profits, corporate tax, employers\' social-security contributions, government\'s income from property and entrepreneurship and savings of non-departmental enterprises). National income is therefore not the sum of personal incomes.',
            'Disposable personal income (DI) = PI − personal direct taxes − other compulsory payments (fees, fines). It is what households can consume or save.',
            'Private income = private sector\'s factor income from NDP + NFIA + interest on national debt + net transfers from the rest of the world + current transfers received from government. Net National Disposable Income = NNI + other net current transfers from abroad; Gross National Disposable Income = NNDI + depreciation.'],
         'analogy': 'National income is what the family earned; personal income is what actually reached the family\'s hands; disposable income is what is left after paying income tax.',
         'work': 'Consumer-goods firms track personal disposable income, not GDP, when forecasting household spending.'},
        {'id': 'c6', 'title': 'Circular flow and the three methods', 'body': [
            'Production, distribution and disposition go on together: firms produce using factor services (production phase); they pay rent, wages, interest and profit to households (distribution or income phase); households spend that income on consumer and investment goods (expenditure or disposition phase), which calls forth more production.',
            'So national income can be measured three ways: as the sum of value added (product method — shows the contribution of each producing sector); as the sum of factor incomes (income method — shows the share of each factor); and as the sum of final expenditure (expenditure method — shows consumption and investment). In principle all three give the same figure, and each acts as a check on the others.',
            'In India no single method is used throughout: value added (production) method in agriculture, income method in the small-scale (unorganised) sector, and expenditure method in construction. The income method suits economies where incomes are well recorded through tax returns.'],
         'analogy': 'Count the money in a closed room three ways — as it is made, as it is paid out, as it is spent — and you should get the same total.',
         'work': 'Revenue assurance in a company follows the same idea: reconcile production records, payroll and sales — three views of one activity.'},
        {'id': 'c7', 'title': 'Value added (product) method', 'body': [
            'Step 1: identify producing enterprises and classify them into primary, secondary and tertiary sectors (and sub-sectors).',
            'Step 2: find gross value added at market prices: GVA MP = Value of output − Intermediate consumption, where Value of output = Sales + Change in stock (closing − opening). If total purchases are given, imports are already in intermediate consumption; if domestic sales are given separately, exports must be added.',
            'Step 3: Σ GVA MP = GDP MP; less depreciation = NDP MP (net value added); less net indirect taxes = NDP FC; plus NFIA = national income.',
            'Include: own-account production of fixed assets, imputed value of production for self-consumption, imputed rent of owner-occupied houses and change in stocks. Exclude: intermediate goods (to avoid double counting), sale of second-hand goods (only the dealer\'s commission is counted), and purely financial transactions.'],
         'analogy': 'Wheat → flour → bread: count only what each stage adds, not the full price at every stage, or the wheat is counted three times.',
         'work': 'The same "value added" idea underlies GST: tax is effectively paid on the value added at each stage.'},
        {'id': 'c8', 'title': 'Income method', 'body': [
            'Also called the factor payment or distributed-share method: add the factor incomes paid by all producing units in the domestic territory. NDP FC = CoE + OS + mixed income, with OS made up of rent, interest and profit; national income = NDP FC + NFIA.',
            'Compensation of employees covers basic pay, DA, bonus and commission, the employer\'s PF and social-security contribution, and perks given in kind (at imputed value). Profit = corporate tax + dividends + retained earnings. Rent includes imputed rent; royalty is included.',
            'Exclude: transfer incomes (pensions, scholarships, gifts), capital gains and windfall gains, proceeds from selling used goods or shares and bonds, spending out of past savings, interest the government pays on public debt, interest households pay on loans taken for consumption, and inter-firm interest. Include commissions, brokerage and imputed value of owners\' services.',
            'Mixed income: for the self-employed (lawyers, doctors, traders, farmers), labour and capital income cannot be separated, so the combined income is recorded as mixed income.'],
         'analogy': 'Open every producer\'s cash book and add only the payments made to the people who provided land, labour, capital and enterprise.',
         'work': 'Tax data (salary TDS, business returns) feed the income method, which is why better tax compliance improves the quality of national income estimates.'},
        {'id': 'c9', 'title': 'Expenditure method', 'body': [
            'Also called the income disposal approach: GDP MP = sum of final expenditure = Private final consumption expenditure (PFCE) + Government final consumption expenditure (GFCE) + Gross domestic capital formation (GDCF) + Net exports (X − M).',
            'PFCE: purchases of final goods and services by households and non-profit institutions serving households, including produce for own consumption and payments for domestic services; purchase of land and new houses by households is not consumption — it is capital formation. GFCE: since government services (defence, administration, public health) are not sold, they are valued at the cost of providing them; transfer payments (pensions, scholarships, unemployment allowance) are excluded.',
            'GDCF = gross fixed capital formation (machinery, equipment, construction, own-account production of capital goods) + change in stocks + net acquisition of valuables (jewellery, works of art). Gross = net + depreciation.',
            'From GDP MP: GNP MP = GDP MP + NFIA; NNP MP = GNP MP − depreciation; NNP FC = NNP MP − NIT.'],
         'analogy': 'Add up every final bill paid in the economy — by families, government, businesses buying machines, and foreigners buying our exports — and take away what we spent on imports.',
         'work': 'Budget documents and RBI reports discuss "private consumption" and "investment rate" (GDCF/GDP) — the expenditure-side components a CA must read fluently.'},
        {'id': 'c10', 'title': 'The system of regional accounts in India', 'body': [
            'Almost all states and union territories estimate state income and many estimate district income. State income, or Net State Domestic Product (NSDP), is the money value of all goods and services produced within the state in a year, counted without duplication. Per capita state income = NSDP ÷ mid-year projected population of the state.',
            'The State Income Units within each State DES prepare the estimates, with the CSO advising on concepts and methods.',
            'Activities that cut across state boundaries — railways, communications, banking and insurance, central government administration — are called supra-regional sectors. They are estimated for the country as a whole and allocated to states using suitable indicators.'],
         'analogy': 'Each state keeps its own "branch accounts"; head-office items that serve all branches (railways, banks) are allocated by a key.',
         'work': 'State-wise GSDP and per capita income guide location decisions, state finance commission work and credit-rating of state government bonds.'},
        {'id': 'c11', 'title': 'GDP and welfare; limitations of national income computation', 'body': [
            'GDP is not a full measure of welfare. It ignores: the distribution of income (two countries with equal per capita income can differ greatly in well-being); quality improvements from new technology and management; hidden or illegal production; most non-market production and non-economic contributors such as health, education and political participation; the loss of leisure; economic "bads" such as crime, pollution and congestion; unpaid volunteer work; fairness, gender equality and community security; externalities; and the difference between output that makes us better off and output that only prevents us from becoming worse off (e.g. more police spending due to rising crime, or repair bills after accidents, both raise GDP).',
            'Conceptual difficulties: no agreed definition of national income; separating final and intermediate goods; treatment of transfer payments; services of durable goods; incorporating income distribution; valuing new goods at constant prices; valuing government services.',
            'Practical challenges (especially in developing countries): inadequate and unreliable data; a large non-monetised sector; production for self-consumption; incomes not recorded because of illiteracy and ignorance; lack of proper occupational classification; and estimating depreciation accurately.'],
         'analogy': 'GDP is a speedometer: it tells you how fast the car is going, not whether the passengers are comfortable or where the car is heading.',
         'work': 'ESG and sustainability reporting, increasingly assured by CAs, exists precisely because profit and GDP miss externalities like pollution.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Building every aggregate from factor incomes', 'difficulty': 'moderate', 'minutes': 10,
         'q': 'From the data (₹ crore) find NDP FC, GDP FC, GDP MP, GNP MP, NNP MP and national income: compensation of employees 2,400; rent 500; interest 400; profit 900; mixed income of self-employed 1,300; consumption of fixed capital 600; net indirect taxes 700; net factor income from abroad (−) 90.',
         'solution': [t1, p(f'Cross-check: national income = NDP FC + NFIA = 5,500 − 90 = ₹{inr(nnpfc2)} crore. Note that operating surplus already equals rent + interest + profit — do not add them twice.')],
         'checks': c1},
        {'id': 'i2', 'title': 'GDP deflator and inflation', 'difficulty': 'core', 'minutes': 8,
         'q': 'Compute the GDP deflator for each year and the rate of inflation in years 2, 3 and 4. Also find real GDP in a year when nominal GDP is ₹1,452 thousand crore and the deflator is 120.',
         'solution': [t2, ul([f'Inflation year 2 = (110 − 100)/100 × 100 = {inf2}%.', f'Inflation year 3 = (115 − 110)/110 × 100 = {inf3}%.', f'Inflation year 4 = (114.29 − 115)/115 × 100 = {inf4}% — the price level fell slightly.', f'Real GDP = 1,452 ÷ 120 × 100 = ₹{inr(realx)} thousand crore.'])],
         'checks': c2},
        {'id': 'i3', 'title': 'Value added method with stock changes', 'difficulty': 'moderate', 'minutes': 10,
         'q': 'Data (₹ crore): Primary — sales 1,500, opening stock 200, closing stock 240, intermediate consumption 300. Secondary — sales 3,200, opening stock 250, closing stock 150, intermediate consumption 1,400. Tertiary — sales 2,100, no stock, intermediate consumption 600. Depreciation 380, indirect taxes 520, subsidies 90, NFIA 40. Find national income.',
         'solution': [t3, ul([f'NDP MP = 4,440 − 380 = {inr(ndp3)}', f'NDP FC = 4,060 − (520 − 90) = {inr(ndpfc3)}', f'National income = 3,630 + 40 = ₹{inr(ni3)} crore'])],
         'checks': c3},
        {'id': 'i4', 'title': 'Expenditure and income methods give the same answer', 'difficulty': 'moderate', 'minutes': 10,
         'q': 'Data (₹ crore): PFCE 4,200; GFCE 1,300; net domestic capital formation 1,100; depreciation 400; net exports (−) 200; net indirect taxes 650; NFIA 50; compensation of employees 3,100; rent 400; interest 450; profit 900; mixed income 900. Compute national income by both methods.',
         'solution': [wn('Expenditure method', f'GDCF = 1,100 + 400 = {inr(gdcf)}. GDP MP = 4,200 + 1,300 + 1,500 − 200 = {inr(gdp4)}. NI = 6,800 − 400 − 650 + 50 = ₹{inr(ni4e)} crore.'),
                      wn('Income method', f'Operating surplus = 400 + 450 + 900 = {inr(os4)}. NI = 3,100 + 1,750 + 900 + 50 = ₹{inr(ni4i)} crore.'), note('Both methods agree, as they should. Net exports enter with their sign.')],
         'checks': c4},
        {'id': 'i5', 'title': 'Private, personal and disposable income', 'difficulty': 'hard', 'minutes': 10,
         'q': 'National income is ₹9,000 crore. Government administrative departments\' income from property and entrepreneurship 220; savings of non-departmental enterprises 80; interest on national debt 180; current transfers from government 300; net current transfers from the rest of the world 120; undistributed profits of corporations 350; corporate tax 400; personal direct taxes 600; miscellaneous fees and fines paid by households 50. Find private income, personal income and disposable personal income.',
         'solution': [table(['Step', '₹ crore'], [['National income', '9,000'], ['Less: govt. property & entrepreneurial income', '−220'], ['Less: savings of non-departmental enterprises', '−80'], ['Add: interest on national debt', '+180'], ['Add: current transfers from government', '+300'], ['Add: net current transfers from rest of world', '+120'], ['Private income', inr(priv)], ['Less: undistributed profits', '−350'], ['Less: corporate tax', '−400'], ['Personal income', inr(pi5)], ['Less: personal direct taxes', '−600'], ['Less: fees and fines', '−50'], ['Disposable personal income', inr(di5)]], title='Private → personal → disposable income'),
                      p(f'Direct check: PI = 9,000 − 220 − 80 − 350 − 400 + 180 + 300 + 120 = ₹{inr(pi5b)} crore.')],
         'checks': c5},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Is our growth real?', 'role': 'CA in industry — strategy and planning',
         'situation': 'The CEO wants to tell investors that sales grew 14% last year "far ahead of the economy". The latest data show nominal GDP growth of 11% and real GDP growth of 7%.',
         'steps': ['Compare like with like: company sales are nominal, so compare 14% with nominal GDP growth of 11%, not with real growth of 7%.', 'Estimate the company\'s own price increase (say 5%) to find its real volume growth (about 9%).', 'Present both: nominal outperformance of 3 points and real outperformance of about 2 points.', 'Note that the gap between nominal and real GDP growth gives the economy-wide inflation implied by the deflator.'],
         'takeaway': 'Always match nominal with nominal and real with real — the GDP deflator is the bridge.', 'think': 'Approximately what inflation does the GDP deflator imply here?', 'answer': 'About 4% — roughly the gap between 11% nominal and 7% real growth (more precisely 1.11/1.07 − 1 ≈ 3.7%).'},
        {'id': 'j2', 'title': 'Choosing a state for a new plant', 'role': 'CA in practice advising a mid-size manufacturer',
         'situation': 'The client is comparing three states for a new consumer-durables plant and warehouse.',
         'steps': ['Collect GSDP growth, per capita NSDP and the share of manufacturing and services from the State DES releases.', 'Use per capita income as a proxy for local purchasing power, but remember it hides income distribution.', 'Combine with state incentive schemes, logistics and labour data.', 'Flag data limits: supra-regional activities (railways, banking) are allocated to states by indicators, so state figures are estimates.'],
         'takeaway': 'Regional accounts help location decisions, but per capita figures are averages and hide distribution.'},
    ]

    mcqs = [
        Q('m1', 'National income accounting was pioneered by:', ['Simon Kuznets and Richard Stone', 'Keynes and Pigou', 'Marshall and Ricardo', 'Cournot and Bertrand'], 0, 'National income accounting — a systematic set of macro-economic accounts — was pioneered by Simon Kuznets and Richard Stone; Kuznets won the Nobel Prize in 1971 and Stone in 1984. "Keynes and Pigou" is the trap: Keynes built the theory of aggregate demand that uses these accounts, but did not design the accounting system. In practice: India\'s quarterly GDP releases follow the UN System of National Accounts that grew out of this work.', 'c1', topic='Usefulness and Significance of National Income Estimates'),
        Q('m2', 'In India, national accounts statistics are compiled by:', ['The Central Statistical Organisation in MoSPI', 'The Reserve Bank of India', 'The Ministry of Finance', 'NITI Aayog'], 0, 'In India, national accounts are compiled by the Central Statistical Organisation (CSO) under the Ministry of Statistics and Programme Implementation; since 2019 the CSO has been part of the National Statistical Office (NSO). "The Reserve Bank of India" is the trap — RBI uses GDP data heavily for monetary policy but does not compile it. In practice: analysts track the NSO\'s quarterly GDP press releases closely.', 'c1', topic='Usefulness and Significance of National Income Estimates'),
        Q('m3', 'GDP at market prices includes:', ['Depreciation', 'Net factor income from abroad', 'Transfer payments', 'Intermediate consumption'], 0, 'GDP at market prices is gross — it includes depreciation (consumption of fixed capital) — and domestic, covering output within the country\'s economic territory. "Net factor income from abroad" is the trap: adding NFIA turns domestic product into national product (GNP), so GDP excludes it. In practice: India\'s headline GDP growth figure is a gross, domestic measure at constant prices.', 'c2', topic='Different Concepts of National Income'),
        Q('m4', 'Nominal GDP is ₹4,500 crore and real GDP is ₹3,600 crore. The GDP deflator is:', ['125', '80', '112.5', '0.8'], 0, 'GDP deflator = (nominal GDP ÷ real GDP) × 100 = (4,500 ÷ 3,600) × 100 = 125, meaning prices are 25% higher than in the base year. 80 is the trap — it divides real GDP by nominal GDP, inverting the formula. In practice: economists use the deflator as a broad inflation measure covering all goods and services produced, not just a consumer basket.', 'c2', 'core', '4500/3600*100', topic='Different Concepts of National Income'),
        Q('m5', 'Real GDP is ₹600 crore and the price index (deflator) is 125. Nominal GDP is:', ['₹750 crore', '₹480 crore', '₹725 crore', '₹600 crore'], 0, 'Nominal GDP = real GDP × deflator ÷ 100 = 600 × 125 ÷ 100 = ₹750 crore. ₹480 crore is the trap — it divides by 1.25 instead of multiplying, which would convert nominal to real, not real to nominal. In practice: budget makers project nominal GDP by combining expected real growth with expected inflation, because tax revenues depend on nominal values.', 'c2', 'core', '600*125/100', topic='Different Concepts of National Income'),
        Q('m6', 'Nominal GDP is ₹2,400 crore and the deflator is 160. Real GDP is:', ['₹1,500 crore', '₹3,840 crore', '₹2,240 crore', '₹15 crore'], 0, 'Real GDP = nominal GDP ÷ deflator × 100 = 2,400 ÷ 160 × 100 = ₹1,500 crore. ₹3,840 crore is the trap — it multiplies by 1.6 instead of dividing, inflating rather than deflating the value. In practice: to see whether an economy truly produced more, analysts strip out price rises by deflating nominal GDP in this way.', 'c2', 'core', '2400/160*100', topic='Different Concepts of National Income'),
        Q('m7', 'The GDP deflator was 140 last year and 147 this year. The inflation rate is:', ['5%', '7%', '4.76%', '47%'], 0, "Inflation = (change in deflator ÷ previous deflator) × 100 = (147 − 140) ÷ 140 × 100 = 7 ÷ 140 × 100 = 5%. 7% is the trap — it is the change in index points, not the percentage change; 4.76% wrongly divides by this year's index. In practice: economists compare GDP-deflator inflation with CPI inflation to understand price trends across the whole economy.", 'c2', 'moderate', '(147-140)/140*100', topic='Different Concepts of National Income'),
        Q('m8', 'If nominal GDP is less than real GDP in a year, the GDP deflator is:', ['Below 100 — prices lower than in the base year', 'Above 100', 'Exactly 100', 'Negative'], 0, 'Deflator = (nominal GDP ÷ real GDP) × 100. If nominal GDP is less than real GDP, the ratio is below one, so the deflator is below 100 — current prices are lower than base-year prices. "Above 100" is the trap; that happens when prices have risen since the base year. In practice: a deflator below 100 signals deflation relative to the base year, which has happened in some years in countries like Japan.', 'c2', 'moderate', topic='Different Concepts of National Income'),
        Q('m9', 'The basis of distinction between "gross" and "net" is:', ['Depreciation', 'Net factor income from abroad', 'Net indirect taxes', 'Transfer payments'], 0, 'Gross and net differ by depreciation (consumption of fixed capital): net = gross − depreciation. "Net factor income from abroad" is the trap — NFIA separates national from domestic, not gross from net. In practice: a company\'s accounts show depreciation on its machines; at the national level, the same idea separates GDP from NDP.', 'c3', topic='Different Concepts of National Income'),
        Q('m10', 'The basis of distinction between "national" and "domestic" is:', ['Net factor income from abroad', 'Depreciation', 'Net indirect taxes', 'Subsidies'], 0, 'National and domestic differ by net factor income from abroad (NFIA): national = domestic + NFIA. Domestic product covers output within the country\'s territory; national product covers income earned by its residents anywhere. "Depreciation" is the trap — that separates gross from net. In practice: interest and profits earned abroad by Indian residents, and profits sent home by foreign companies operating in India, make India\'s GNI differ from its GDP.', 'c3', topic='Different Concepts of National Income'),
        Q('m11', 'GDP MP is ₹8,200 crore, NFIA is (−) ₹150 crore and depreciation ₹700 crore. NNP MP is:', ['₹7,350 crore', '₹7,650 crore', '₹9,050 crore', '₹7,500 crore'], 0, "NNP MP = GDP MP + NFIA − depreciation = 8,200 + (−150) − 700 = 8,200 − 150 − 700 = ₹7,350 crore. ₹7,650 crore is the trap — it adds NFIA as +150, ignoring the minus sign. In practice: India's NFIA is usually negative, because foreign investors earn more income in India than Indians earn abroad, so GNI is slightly below GDP.", 'c3', 'moderate', '8200+(-150)-700', topic='Different Concepts of National Income'),
        Q('m12', 'Profit earned in India by a branch of a foreign company is included in:', ['India\'s GDP but not India\'s GNP', 'India\'s GNP but not GDP', 'Both India\'s GDP and GNP', 'Neither'], 0, 'The branch produces inside India\'s economic territory, so its profit is part of India\'s GDP; but it is factor income of a non-resident, so it is deducted (as factor income paid abroad) when moving to GNP. "Both India\'s GDP and GNP" is the trap — GNP counts only income of residents. In practice: profits repatriated by foreign companies operating in India are part of the reason India\'s NFIA is negative.', 'c3', 'moderate', topic='Different Concepts of National Income'),
        Q('m13', 'Market price and factor cost differ by:', ['Net indirect taxes (indirect taxes − subsidies)', 'Indirect taxes + subsidies', 'Depreciation', 'NFIA'], 0, 'Market price and factor cost differ by net indirect taxes: market price = factor cost + indirect taxes − subsidies. "Indirect taxes + subsidies" is the trap — subsidies reduce the market price below factor cost, so they are subtracted, not added. In practice: GST raises the price consumers pay above what producers receive, while fertiliser subsidies cut the farmer\'s price below cost.', 'c4', topic='Different Concepts of National Income'),
        Q('m14', 'GDP MP is ₹5,000 crore, indirect taxes ₹600 crore and subsidies ₹150 crore. GDP FC is:', ['₹4,550 crore', '₹4,250 crore', '₹5,450 crore', '₹4,400 crore'], 0, "GDP FC = GDP MP − indirect taxes + subsidies = 5,000 − 600 + 150 = ₹4,550 crore. ₹4,250 crore is the trap — it deducts subsidies instead of adding them back. Subsidies lower market prices, so they must be added to move to factor cost. In practice: India's national accounts present GVA at basic prices and GDP at market prices, linked through product taxes and subsidies.", 'c4', 'moderate', '5000-600+150', topic='Different Concepts of National Income'),
        Q('m15', 'Basic price equals:', ['Factor cost + production taxes − production subsidies', 'Market price + product taxes', 'Factor cost − product taxes', 'Market price + subsidies'], 0, 'Basic price = factor cost + production taxes − production subsidies; then market price = basic price + product taxes − product subsidies. "Market price + product taxes" is the trap — product taxes are already in market price, so basic price excludes them. In practice: since the 2011-12 base revision, India reports sector-wise GVA at basic prices, a practice followed in national accounts worldwide.', 'c4', 'moderate', topic='Different Concepts of National Income'),
        Q('m16', 'National income is:', ['NNP at factor cost', 'GNP at market prices', 'NDP at market prices', 'GDP at factor cost'], 0, 'National income is net national product at factor cost (NNP FC) — the total factor income earned by a country\'s residents, net of depreciation and indirect taxes. "GNP at market prices" is the trap; it includes depreciation and net indirect taxes, so it is larger than national income. In practice: per capita national income figures quoted by the NSO are based on NNP.', 'c5', topic='Different Concepts of National Income'),
        Q('m17', 'NDP FC is ₹6,400 crore and NFIA is ₹120 crore. National income is:', ['₹6,520 crore', '₹6,280 crore', '₹6,400 crore', '₹6,640 crore'], 0, 'National income = NDP FC + NFIA = 6,400 + 120 = ₹6,520 crore. ₹6,280 crore is the trap — it subtracts a positive NFIA instead of adding it; ₹6,400 crore is domestic income only. In practice: for countries that receive large factor income from abroad, national income exceeds domestic income.', 'c5', 'core', '6400+120', topic='Different Concepts of National Income'),
        Q('m18', 'Which of the following is added to national income to arrive at personal income?', ['Transfer payments to households', 'Undistributed corporate profits', 'Corporate profit tax', 'Mixed income of self-employed'], 0, 'Personal income measures income actually received by households. Transfer payments — pensions, scholarships, unemployment benefits — are received though not earned in production, so they are added to national income. "Undistributed corporate profits" is the trap: these are earned but not received by households, so they are subtracted. In practice: government pensions and DBT transfers raise household income without adding to national income.', 'c5', topic='Different Concepts of National Income'),
        Q('m19', 'Disposable personal income equals:', ['Personal income − personal direct taxes − other compulsory payments', 'National income − indirect taxes', 'Personal income + transfer payments', 'GDP − depreciation'], 0, 'Disposable personal income = personal income − personal direct taxes − other compulsory payments, such as fees and fines; it is what households can actually spend or save. "Personal income + transfer payments" is the trap — transfers are already included in personal income, so adding them again double-counts. In practice: take-home pay after TDS is a household-level version of disposable income.', 'c5', topic='Different Concepts of National Income'),
        Q('m20', 'Personal income is ₹4,800 crore, personal income tax ₹520 crore and fines/fees ₹30 crore. Disposable personal income is:', ['₹4,250 crore', '₹4,280 crore', '₹4,310 crore', '₹5,350 crore'], 0, "Disposable personal income = personal income − personal income tax − fines and fees = 4,800 − 520 − 30 = ₹4,250 crore. ₹4,280 crore is the trap — it deducts the income tax but forgets the ₹30 crore of fines and fees. In practice: changes in income-tax rates in the Union Budget directly change households' disposable income and therefore consumer spending.", 'c5', 'core', '4800-520-30', topic='Different Concepts of National Income'),
        Q('m21', 'Which phase of the circular flow involves spending of factor incomes on consumption and investment goods?', ['Disposition (expenditure) phase', 'Production phase', 'Distribution phase', 'Accumulation phase'], 0, 'The circular flow has three phases: production of goods and services, distribution of factor incomes (wages, rent, interest, profit), and disposition — spending those incomes on consumption and investment goods. "Distribution phase" is the trap; that is when incomes are paid, not spent. In practice: the three phases correspond to the product, income and expenditure methods of measuring national income.', 'c6', topic='Measurement of National Income in India'),
        Q('m22', 'Value of output in an industry is calculated as:', ['Sales + change in stock', 'Sales − change in stock', 'Sales + intermediate consumption', 'Sales − depreciation'], 0, 'Value of output = sales + change in stock (closing − opening). If stock rises, some output was produced but not sold, so it is added; if stock falls, some sales came from earlier output, so it is deducted. "Sales − change in stock" is the trap — it reverses the adjustment. In practice: statisticians use company sales and inventory data, like those in audited accounts, to estimate value of output.', 'c7', topic='Measurement of National Income in India'),
        Q('m23', 'Sales ₹900 crore, opening stock ₹120 crore, closing stock ₹80 crore, intermediate consumption ₹400 crore. GVA MP is:', ['₹460 crore', '₹540 crore', '₹500 crore', '₹380 crore'], 0, 'Value of output = 900 + (80 − 120) = 900 − 40 = ₹860 crore; GVA MP = 860 − 400 = ₹460 crore. ₹540 crore is the trap — it adds the ₹40 crore fall in stock instead of deducting it. In practice: GVA, not sales, is what each industry contributes to GDP, because it removes the value of inputs bought from other firms.', 'c7', 'moderate', '900+(80-120)-400', topic='Measurement of National Income in India'),
        Q('m24', 'Which of these is included in national income?', ['Imputed rent of owner-occupied houses', 'Sale of a second-hand car', 'Old-age pension', 'Purchase of shares'], 0, 'Imputed rent of owner-occupied houses is included, because the house provides a housing service even when the owner lives in it. "Sale of a second-hand car" is the trap — it only transfers an existing asset; the car was counted when produced. Pensions are transfers, and share purchases are financial transactions. In practice: imputed rent is a large part of India\'s real estate GVA in the national accounts.', 'c7', topic='Measurement of National Income in India'),
        Q('m25', 'Under the income method, which of the following is excluded?', ['Interest on national (public) debt', 'Employers\' contribution to provident fund', 'Royalty', 'Dividends'], 0, 'Under the income method, interest on national (public) debt is excluded because it is treated as a transfer payment: government borrowing largely funds current spending, not production. "Employers\' contribution to provident fund" is the trap — it is part of compensation of employees and is included. In practice: the large interest bill in the Union Budget is not counted as factor income in national income.', 'c8', topic='Measurement of National Income in India'),
        Q('m26', 'Mixed income of the self-employed means:', ['Combined factor income that cannot be separated into labour and capital income', 'Wages earned outside the business', 'Income from non-economic activity', 'Transfer income'], 0, 'Mixed income of the self-employed is the combined income of people who use their own labour, capital and land together, so it cannot be split into wages, rent, interest and profit. "Wages earned outside the business" is the trap — those are ordinary compensation of employees. In practice: income of farmers, kirana shop owners and practising professionals such as CAs is largely mixed income in India\'s accounts.', 'c8', topic='Measurement of National Income in India'),
        Q('m27', 'PFCE ₹3,000 crore, GFCE ₹900 crore, GDCF ₹1,100 crore, exports ₹400 crore, imports ₹550 crore. GDP MP is:', ['₹4,850 crore', '₹5,950 crore', '₹5,150 crore', '₹5,000 crore'], 0, 'GDP MP = PFCE + GFCE + GDCF + (exports − imports) = 3,000 + 900 + 1,100 + (400 − 550) = 5,000 − 150 = ₹4,850 crore. ₹5,950 crore is the trap — it adds imports instead of deducting them; spending on imports buys foreign, not domestic, output. In practice: India runs a trade deficit, so net exports reduce GDP measured by expenditure.', 'c9', 'moderate', '3000+900+1100+(400-550)', topic='Measurement of National Income in India'),
        Q('m28', 'In the expenditure method, purchase of a new house by a household is treated as:', ['Gross domestic capital formation', 'Private final consumption expenditure', 'Intermediate consumption', 'Transfer payment'], 0, 'In the expenditure method, a household\'s purchase of a new house is treated as gross domestic capital formation (investment in residential buildings), not consumption, because a house gives services over many years. "Private final consumption expenditure" is the trap; houses are an exception to the rule that household purchases are consumption. In practice: housing construction is a major part of India\'s capital formation figures.', 'c9', 'moderate', topic='Measurement of National Income in India'),
        Q('m29', 'Government expenditure on scholarships is:', ['Excluded from GFCE as a transfer payment', 'Part of GFCE', 'Part of GDCF', 'Part of net exports'], 0, 'Scholarships are transfer payments: money paid without any goods or services produced in return. So they are excluded from government final consumption expenditure (GFCE). "Part of GFCE" is the trap — GFCE counts the government\'s purchases of goods and services, such as salaries of teachers and soldiers. In practice: direct benefit transfers under schemes like PM-KISAN are transfers, not government consumption.', 'c9', topic='Measurement of National Income in India'),
        Q('m30', 'Activities like railways, banking and central government administration, whose output cannot be assigned to one state directly, are called:', ['Supra-regional sectors', 'Primary sectors', 'Non-departmental enterprises', 'Unorganised sectors'], 0, 'Activities such as railways, banking, communications and central government administration operate across state boundaries, so their output cannot be assigned directly to one state; they are called supra-regional sectors. Their income is estimated nationally and allocated to states using indicators. "Unorganised sectors" is the trap — that refers to small, unregistered units. In practice: state DESs use these allocations to estimate GSDP.', 'c10', topic='The System of Regional Accounts in India'),
        Q('m31', 'Per capita state income is obtained by dividing NSDP by:', ['The mid-year projected population of the state', 'The national population', 'The number of workers in the state', 'The number of households'], 0, 'Per capita state income = net state domestic product (NSDP) ÷ the mid-year projected population of that state. "The national population" is the trap — dividing state income by the national population would make per capita figures meaningless. In practice: states compare their per capita NSDP to rank prosperity, and the Finance Commission considers such data in devolving funds.', 'c10', topic='The System of Regional Accounts in India'),
        Q('m32', 'Which of the following is a reason why GDP is an imperfect measure of welfare?', ['It ignores income distribution and economic "bads" such as pollution', 'It includes only final goods', 'It is measured in money', 'It includes services'], 0, 'GDP measures market output, but it ignores how income is distributed and does not subtract "bads" such as pollution or environmental damage, so higher GDP need not mean higher welfare. "It is measured in money" is the trap — money measurement is what makes GDP calculable; it is not the main reason GDP fails as a welfare index. In practice: Delhi\'s winter smog shows how output can grow while quality of life falls.', 'c11', topic='GDP and Welfare'),
        Q('m33', 'Increased spending on police because of a rise in crime:', ['Raises GDP although it only prevents people from becoming worse off', 'Lowers GDP', 'Is excluded from GDP', 'Has no effect on GDP'], 0, 'Extra police spending is counted in GDP as government output, so GDP rises — but it only defends people against a rise in crime and does not make them better off than before. "Is excluded from GDP" is the trap; government services are included at cost. In practice: this is why economists caution that rising "defensive" spending, such as on security or pollution masks, can inflate GDP without improving welfare.', 'c11', 'moderate', topic='GDP and Welfare'),
        Q('m34', 'A "resident unit" for GDP purposes means a unit:', ['With its predominant economic interest in the country\'s economic territory for one year or more, whatever its nationality', 'Owned only by citizens', 'Located only in India with Indian owners', 'Composed of citizens living in India'], 0, 'A resident unit is one whose centre of predominant economic interest lies in the country\'s economic territory for one year or more, regardless of nationality. "Owned only by citizens" is the trap — residence, not citizenship, decides inclusion, so a foreign national working in India for years is a resident. In practice: the profits of a foreign company\'s Indian subsidiary are included in India\'s GDP.', 'c3', 'hard', topic='Different Concepts of National Income'),
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'From the following data (₹ crore) calculate GDP MP, GNP MP, NNP MP and national income: compensation of employees 3,200; operating surplus 1,450; mixed income 1,100; consumption of fixed capital 500; net indirect taxes 600; NFIA (−) 60.',
         'model': [table(['Aggregate', 'Working', '₹ crore'], [['GDP MP', '3,200 + 1,450 + 1,100 + 500 + 600', inr(w1_gdpmp)], ['GNP MP', '6,850 − 60', inr(w1_gnpmp)], ['NNP MP', '6,790 − 500', inr(w1_nnpmp)], ['NNP FC (National income)', '6,290 − 600', inr(w1_ni)]])],
         'scheme': [{'id': 's1', 'pt': 'GDP MP = CoE + OS + MI + CFC + NIT', 'm': 2, 'skill': 'computation'}, {'id': 's2', 'pt': 'GNP MP with NFIA sign', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'NNP MP', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'National income', 'm': 1, 'skill': 'computation'}],
         'remarks': ['A step-wise table makes the sequence clear and earns method marks.'], 'mistakes': ['Adding negative NFIA as positive.', 'Deducting NIT twice.'], 'tips': ['Remember the three switches: gross/net (depreciation), domestic/national (NFIA), MP/FC (NIT).'], 'checks': w1},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'For a firm (₹ crore): sales 820; opening stock 90; closing stock 60; intermediate consumption 310; depreciation 45; indirect taxes 70; subsidies 20. Calculate GVA MP, NVA MP and NVA FC.',
         'model': [table(['Item', 'Working', '₹ crore'], [['Value of output', '820 + (60 − 90)', inr(w2_vo)], ['GVA MP', '790 − 310', inr(w2_gva)], ['NVA MP', '480 − 45', inr(w2_nva)], ['NVA FC', '435 − (70 − 20)', inr(w2_nvafc)]])],
         'scheme': [{'id': 's1', 'pt': 'Value of output with change in stock', 'm': 1, 'skill': 'computation'}, {'id': 's2', 'pt': 'GVA MP', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'NVA MP', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'NVA FC with NIT', 'm': 1, 'skill': 'computation'}],
         'remarks': ['A fall in stock reduces the value of output — many candidates add it.'], 'mistakes': ['Ignoring the change in stock.', 'Adding subsidies to market price.'], 'tips': ['Write "change in stock = closing − opening" with its sign.'], 'checks': w2},
        {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'hard', 'pad': 'table',
         'q': 'Compute national income by the expenditure method and by the income method (₹ crore): PFCE 2,600; GFCE 700; net domestic capital formation 560; depreciation 140; net exports (−) 80; net indirect taxes 210; NFIA 30; compensation of employees 1,900; rent 250; interest 300; profit 650; mixed income 470.',
         'model': [wn('Expenditure method', f'GDP MP = 2,600 + 700 + (560 + 140) − 80 = {inr(w3_gdp)}; NI = 3,920 − 140 − 210 + 30 = ₹{inr(w3_ni_e)} crore.'),
                   wn('Income method', f'NI = 1,900 + (250 + 300 + 650) + 470 + 30 = ₹{inr(w3_ni_i)} crore.'), note('Both methods give the same national income.')],
         'scheme': [{'id': 's1', 'pt': 'GDCF = NDCF + depreciation', 'm': 1, 'skill': 'application'}, {'id': 's2', 'pt': 'GDP MP by expenditure', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'NI from GDP MP', 'm': 1, 'skill': 'computation'}, {'id': 's4', 'pt': 'NI by income method', 'm': 1.5, 'skill': 'computation'}, {'id': 's5', 'pt': 'States agreement / presentation', 'm': 0.5, 'skill': 'presentation'}],
         'remarks': ['Strong answers show both methods side by side and note that they agree.'], 'mistakes': ['Using NDCF instead of GDCF in GDP.', 'Forgetting NFIA in the income method.'], 'tips': ['Expenditure method gives GDP MP first; income method gives NDP FC first.'], 'checks': w3},
    ]

    viva = [
        V('v1', 'Distinguish between GDP and GNP.',
          'GDP is the market value of all final goods and services produced inside the country\'s domestic territory in a year, whether by residents or non-residents. GNP is GDP plus net factor income from abroad, so it measures what the country\'s normal residents earn wherever they produce. The difference between the two is net factor income from abroad.',
          [P('p1', 'GDP: final goods & services produced within the domestic territory', 4, 'within|inside|domestic territory|domestic boundar|geographical boundar|in the country', 'final good|final goods|final output|final product|goods and services', min=2),
           P('p2', 'GNP = GDP + NFIA (earned by normal residents)', 4, 'net factor income from abroad|nfia|net factor income', 'resident|national|citizen', min=1),
           P('p3', 'Difference is NFIA', 2, 'difference|differ|distinction|gap|plus|added|add')], 'c3'),
        V('v2', 'What is the GDP deflator and how is it calculated?',
          'The GDP deflator is a price index that measures the current price level compared with the base year. It is calculated as nominal GDP divided by real GDP, multiplied by 100. It is 100 in the base year, and dividing nominal GDP by the deflator and multiplying by 100 gives real GDP.',
          [P('p1', 'A price index comparing prices with the base year', 3, 'price index|price level|measure of inflation|inflation|prices', 'base year|base period', min=2),
           P('p2', 'Deflator = Nominal GDP ÷ Real GDP × 100', 5, ALT('nominal gdp {d} real gdp', 'nominal {d} real', d=['divided by', 'divide by', 'by', 'over', 'upon'])),
           P('p3', 'Equals 100 in the base year / used to get real GDP', 2, '100 in the base year|100 in base year|base year 100|base year is 100|equal 100|equals 100|always 100|real gdp equal|get real gdp|convert nominal|deflate')], 'c2'),
        V('v3', 'What is the difference between market price and factor cost, and how do you convert one into the other?',
          'Market price and factor cost differ by net indirect taxes, that is indirect taxes minus subsidies. Market price equals factor cost plus indirect taxes minus subsidies. To go from market price to factor cost, we deduct indirect taxes and add subsidies.',
          [P('p1', 'Difference is net indirect taxes', 4, 'net indirect tax|nit|indirect taxes minus subsid|indirect tax less subsid|indirect tax minus subsid'),
           P('p2', 'MP = FC + indirect taxes − subsidies', 3, ALT('factor cost plus indirect tax', 'factor cost + indirect tax', 'add indirect tax', 'adding indirect tax'), ALT('minus subsid', 'less subsid', 'deduct subsid', 'subtract subsid', 'subsidies deducted'), min=1),
           P('p3', 'FC = MP − indirect taxes + subsidies', 3, ALT('deduct indirect tax', 'subtract indirect tax', 'minus indirect tax', 'less indirect tax', 'remove indirect tax', 'indirect taxes deducted', 'indirect tax deducted', 'take away indirect tax'), ALT('add subsid', 'plus subsid', 'adding subsid', 'subsidies added', 'subsidy added'), min=2)], 'c4'),
        V('v4', 'Name the three methods of measuring national income and what each adds up.',
          'The three methods are the value added or product method, the income method and the expenditure method. The value added method adds the net value added by all producing units, that is value of output minus intermediate consumption. The income method adds factor incomes — compensation of employees, operating surplus and mixed income. The expenditure method adds final expenditure — private and government final consumption, gross domestic capital formation and net exports.',
          [P('p1', 'Value added / product method — output minus intermediate consumption', 4, 'value added|product method|production method|output method', 'intermediate|value of output|output minus|net value added', min=2),
           P('p2', 'Income method — factor incomes (CoE, OS, mixed income)', 3, 'income method|factor income|factor payment', 'compensation|wage|operating surplus|rent|mixed income|profit', min=2),
           P('p3', 'Expenditure method — C + G + investment + net exports', 3, 'expenditure method|final expenditure|expenditure', 'consumption|capital formation|investment|net export', min=2)], 'c6'),
        V('v5', 'How is personal income derived from national income, and what is disposable income?',
          'Personal income equals national income plus incomes received but not earned, such as transfer payments and interest on national debt, minus incomes earned but not received, such as undistributed corporate profits, corporate tax and social security contributions. Disposable income is personal income minus personal direct taxes and other compulsory payments; it is what households can consume or save.',
          [P('p1', 'Add incomes received but not earned (transfers)', 3, 'received but not earned|transfer payment|transfers|pension|scholarship|interest on national debt'),
           P('p2', 'Deduct incomes earned but not received (undistributed profits, corporate tax, contributions)', 3, 'earned but not received|undistributed|retained|corporate tax|corporation tax|social security contribution'),
           P('p3', 'DI = PI − direct taxes (and compulsory payments)', 4, 'disposable', 'direct tax|income tax|personal tax|personal income tax', min=2)], 'c5'),
        V('v6', 'Why is GDP not a perfect measure of welfare?',
          'GDP ignores how income is distributed, so the same per capita income can mean very different well-being. It leaves out non-market and voluntary work, the value of leisure, and quality improvements. It does not deduct economic bads like pollution, crime and congestion, or other externalities, and it even rises with spending that only prevents us from becoming worse off, such as more police spending or accident repairs.',
          [P('p1', 'Ignores income distribution', 3, 'distribution|inequality|unequal'),
           P('p2', 'Leaves out non-market / voluntary work, leisure, quality', 3, 'non market|nonmarket|household work|voluntary|volunteer|unpaid|leisure|quality'),
           P('p3', 'Ignores bads / externalities (pollution, crime)', 2, 'pollution|crime|congestion|externalit|economic bad|bads'),
           P('p4', 'Counts defensive spending (police, repairs)', 2, 'police|defence spending|defensive|repair|accident|prevent us from becoming worse|worse off')], 'c11'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Republic of Navagram — first national accounts', 'difficulty': 'hard',
        'case': ('Navagram, a small economy, publishes its first accounts (₹ crore): private final consumption expenditure 5,400; government final consumption expenditure 1,800; gross domestic capital formation 2,100; net exports 300; '
                 'consumption of fixed capital 900; net indirect taxes 1,100; net factor income from abroad (−) 150. Population is 5 crore. Real GDP at base-year prices is ₹8,000 crore.'),
        'mcqs': [
            M('k1a', 'Navagram\'s GDP at market prices is:', ['₹9,600 crore', '₹9,000 crore', '₹9,300 crore', '₹8,700 crore'], 0, "By the expenditure method, GDP MP = PFCE + GFCE + GDCF + net exports = 5,400 + 1,800 + 2,100 + 300 = ₹9,600 crore. ₹9,300 crore is the trap — it leaves out net exports of 300. Depreciation and indirect taxes are already included in GDP at market prices. In practice: this is how India's expenditure-side GDP is built from consumption, government spending, investment and trade data.", 'core', '5400+1800+2100+300', topic='Measurement of National Income in India'),
            M('k1b', 'Navagram\'s national income (NNP FC) is:', ['₹7,450 crore', '₹7,750 crore', '₹8,550 crore', '₹7,600 crore'], 0, 'NNP FC = GDP MP − depreciation − net indirect taxes + NFIA = 9,600 − 900 − 1,100 + (−150) = ₹7,450 crore. ₹7,750 crore is the trap — it adds NFIA as +150, though it is negative. In practice: moving from headline GDP to national income requires all three adjustments — for depreciation, taxes and income from abroad.', 'hard', '9600-900-1100+(-150)', topic='Different Concepts of National Income'),
            M('k1c', 'Per capita national income (₹) is:', ['1,490', '1,920', '14,900', '1,550'], 0, "Per capita income = national income ÷ population = (7,450 × 1,00,00,000) ÷ 5,00,00,000 = ₹1,490. ₹1,920 is the trap — it divides GDP (9,600 crore), not national income, by population; ₹14,900 slips a zero. In practice: India's per capita net national income, published by the NSO, is calculated in just this way and compared across years.", 'hard', '7450*10000000/50000000', topic='Different Concepts of National Income'),
            M('k1d', 'The GDP deflator for Navagram is:', ['120', '83.33', '160', '112'], 0, 'GDP deflator = (nominal GDP ÷ real GDP) × 100 = (9,600 ÷ 8,000) × 100 = 120, so prices are 20% above the base year. 83.33 is the trap — it divides real GDP by nominal GDP, inverting the formula. In practice: comparing nominal and real GDP lets analysts separate genuine output growth from price rises when assessing an economy.', 'moderate', '9600/8000*100', topic='Different Concepts of National Income'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch05', 'n': 1, 'title': 'National Income Accounting',
        'outcomes': ['Explain the meaning, compilation and uses of national income estimates.', 'Distinguish and inter-convert GDP, GNP, NDP, NNP at market prices and factor cost, national income, personal and disposable income, and use the GDP deflator.',
                     'Measure national income by the value added, income and expenditure methods and know what is included and excluded.', 'Describe India\'s regional accounts and explain why GDP is not a full measure of welfare, and the limitations of national income computation.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 55, 'practice': 60}, 'prereq': ['fnd-p4-ch01-u01'],
                 'exam_tip': 'Numerical MCQs on aggregates appear every attempt. Learn the three switches (depreciation, NFIA, NIT), watch the signs of NFIA and net exports, and remember operating surplus = rent + interest + profit.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['GDP MP: value of final output produced inside the domestic territory in a year, before depreciation.', 'Gross − Depreciation = Net; Domestic + NFIA = National; Market price − NIT = Factor cost.',
                        'NI = NNP FC = CoE + OS + Mixed income + NFIA.', 'PI = NI + transfers received − incomes earned but not received; DI = PI − direct taxes − compulsory payments.',
                        'GDP deflator = Nominal ÷ Real × 100; inflation = change in deflator ÷ previous deflator × 100.', 'Three methods: value added, income, expenditure — India uses a mix.',
                        'State income = NSDP; supra-regional sectors allocated by indicators.', 'GDP ignores distribution, non-market work, leisure, bads and externalities.'],
            'remember': ['Value of output = Sales + (closing − opening stock).', 'GDP MP = C + G + GDCF + (X − M); GDCF = NDCF + depreciation.', 'Basic price = FC + production taxes − production subsidies; MP = basic price + product taxes − product subsidies.'],
            'traps': ['Second-hand goods, shares, transfer payments and interest on public debt are not in national income.', 'Operating surplus already includes rent, interest and profit.', 'A fall in stock reduces value of output.', 'NI is not the sum of personal incomes.']},
        'quickref': [{'k': 'GNP MP', 'v': 'GDP MP + NFIA'}, {'k': 'NDP MP', 'v': 'GDP MP − Depreciation'}, {'k': 'NNP MP', 'v': 'GNP MP − Depreciation'}, {'k': 'GDP FC', 'v': 'GDP MP − Indirect taxes + Subsidies'},
                     {'k': 'National income', 'v': 'NNP FC = NDP FC + NFIA = CoE + OS + MI + NFIA'}, {'k': 'GDP (expenditure)', 'v': 'PFCE + GFCE + GDCF + (X − M)'}, {'k': 'GVA MP', 'v': 'Sales + change in stock − intermediate consumption'},
                     {'k': 'GDP deflator', 'v': 'Nominal GDP ÷ Real GDP × 100'}, {'k': 'Personal / disposable income', 'v': 'PI = NI + transfers − earned-not-received; DI = PI − direct taxes'}],
        'viva': viva, 'cases': cases,
    }

# ==== AUTO-CHECK: offline marking keys (kw groups / nums / ai_only per scheme point; read by the app's marker) ====
# kw: viva-matcher keyword groups ("a|b" = alternatives), min = groups needed; nums: figures that must appear
# (magnitudes: the matcher drops minus signs, so a sign that matters is carried by a kw group).


def _K(*kw, min=None, nums=None, **x):
    d = {'kw': list(kw), 'min': len(kw) if min is None else min}
    if nums: d['nums'] = list(nums)
    d.update(x)
    return d


def _N(*nums, kw=None, min=None, **x):
    d = {'nums': list(nums)}
    if kw: d.update(kw=list(kw), min=len(kw) if min is None else min)
    d.update(x)
    return d


def _CR(*vals, **x):
    """figures in Rs crore: nums matches '5,690' and '5,690 crore' alike"""
    return _N(*vals, **x)


AUTO = {
    'q1': {'s1': _CR(6850), 's2': _CR(6790), 's3': _CR(6290), 's4': _CR(5690)},
    'q2': {'s1': _CR(790), 's2': _CR(480), 's3': _CR(435), 's4': _CR(385)},
    'q3': {
        's1': _K('560 140 700|560 140|gdcf 700|gross domestic capital formation 700|ndcf depreciation|ndcf plus depreciation'),
        's2': _CR(3920),
        's3': _K('3920 140 210 30|3920 140|3920 210'),
        's4': _K('1900', '470', '3600|36000000000'),
        's5': _K('same|equal|agree|identical|match|tall'),
    },
}


_build_content = build


def build():
    u = _build_content()
    for q in u.get('questions', []):
        a = AUTO.get(q['id'], {})
        q['extra_ok'] = a.get('extra_ok', False)
        for s in q['scheme']:
            s.update(a[s['id']])
    return u
