"""CA Intermediate · Paper 3A Income-tax Law · Chapter 1 Basic Concepts (Income-tax Act, 2025; tax year 2026-27).
Scope follows the ICAI study material; section numbers and rates are taken from it; explanations and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-a-ch01-u01'
T1 = 'Components of income-tax law'
T2 = 'Charge of tax, person and assessee'
T3 = 'Kinds of companies and other persons'
T4 = 'Tax year and income assessed in the same year'
T5 = 'Meaning of income; capital vs revenue'
T6 = 'Unexplained income (ss. 102–106, 195)'
T7 = 'Agricultural income'
T8 = 'Steps to compute total income'
T9 = 'Tax regimes and slab rates for individuals'
T10 = 'Rebate, surcharge, cess and special rates'
T11 = 'Partial integration of agricultural income'
T12 = 'Rates for firms, companies and co-operatives'


def slab_new(x):
    t = 0
    for lo, hi, r in [(400000, 800000, .05), (800000, 1200000, .10), (1200000, 1600000, .15), (1600000, 2000000, .20), (2000000, 2400000, .25), (2400000, 10**12, .30)]:
        if x > lo: t += (min(x, hi) - lo) * r
    return round(t)


def build():
    ck = Checks()
    t1 = ck.add('400000*0.05+400000*0.10+400000*0.15+240000*0.20', 'Default regime: tax on ₹18,40,000')
    c1 = ck.add('round(168000*0.04)', 'Cess @4%')
    tot1 = ck.add('168000+6720', 'Tax payable')
    t2 = ck.add('400000*0.05+400000*0.10+40000*0.15', 'Default regime: tax on ₹12,40,000')
    rb2 = ck.add('66000-40000', 'Marginal rebate u/s 156 = tax − excess over ₹12 lakh')
    tot2 = ck.add('round((66000-26000)*1.04)', 'Tax after rebate + cess')
    t3 = ck.add('200000*0.05+450000*0.20', 'Optional regime, age 65: tax on ₹9,50,000 (BEL ₹3 lakh)')
    tot3 = ck.add('round(100000*1.04)', 'Tax with cess')
    i1 = {'id': 'i1', 'title': 'Tax under both regimes', 'difficulty': 'core', 'minutes': 12,
          'q': 'Compute tax for tax year 2026-27: (a) Ananya, 32, resident, total income ₹18,40,000, default regime; (b) Bharat, 40, resident, total income ₹12,40,000, default regime; (c) Chitra, 65, resident, total income ₹9,50,000, has opted out of the default regime.',
          'solution': [table(['Case', 'Working', 'Tax ₹'], [
              ['(a) Ananya — slab tax', '5% × 4 L + 10% × 4 L + 15% × 4 L + 20% × 2.4 L', inr(t1)],
              ['(a) Add cess @4%', '', inr(c1)],
              ['(a) Tax payable', '', inr(tot1)],
              ['(b) Bharat — slab tax', '5% × 4 L + 10% × 4 L + 15% × 40,000', inr(t2)],
              ['(b) Less marginal rebate u/s 156', 'Tax ₹66,000 exceeds excess income ₹40,000 → rebate = 66,000 − 40,000', inr(rb2)],
              ['(b) Tax payable incl. cess', '(66,000 − 26,000) × 1.04', inr(tot2)],
              ['(c) Chitra — slab tax (senior: BEL ₹3 lakh)', '5% × 2 L + 20% × 4.5 L', inr(t3)],
              ['(c) Tax payable incl. cess (no rebate — income above ₹5 lakh)', '', inr(tot3)]], title='Computation'),
              note('Under the default regime, a resident individual just above ₹12 lakh never pays more tax than the income above ₹12 lakh (marginal rebate).')],
          'checks': list(ck)}

    ck2 = Checks()
    agg = ck2.add('1400000+300000', 'Aggregate income = total income + net agricultural income')
    xn = ck2.add('400000*0.05+400000*0.10+400000*0.15+100000*0.20', 'Xn: tax on ₹17,00,000 (default regime)')
    yn = ck2.add('300000*0.05', 'Yn: tax on ₹3,00,000 + ₹4,00,000 = ₹7,00,000')
    zn = ck2.add('140000-15000', 'Zn = Xn − Yn')
    tz = ck2.add('round(125000*1.04)', 'Tax with cess (no rebate: total income above ₹12 lakh and tax < excess)')
    i2 = {'id': 'i2', 'title': 'Partial integration of agricultural income', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Deepak, 50, resident, has non-agricultural total income of ₹14,00,000 and net agricultural income of ₹3,00,000 for tax year 2026-27. He pays tax under the default regime. Compute his tax.',
          'solution': [p('Conditions met: net agricultural income exceeds ₹5,000 and non-agricultural income exceeds the basic exemption limit (₹4,00,000).'),
                       table(['Step', 'Working', '₹'], [
                           ['Aggregate income', '14,00,000 + 3,00,000', inr(agg)],
                           ['Xn — tax on aggregate income', 'Slabs up to ₹17,00,000', inr(xn)],
                           ['Yn — tax on agricultural income + BEL', 'Tax on ₹7,00,000', inr(yn)],
                           ['Zn = Xn − Yn', '', inr(zn)],
                           ['Rebate u/s 156', 'Total income ₹14 lakh > ₹12 lakh; tax ₹1,25,000 < excess ₹2,00,000', 'Nil'],
                           ['Tax with cess @4%', '', inr(tz)]], title='Computation'),
                       note('The agricultural income itself stays exempt; integration only pushes the non-agricultural income into higher slabs.')],
          'checks': list(ck2)}

    ck3 = Checks()
    bus = ck3.add('3200000-2400000-200000', 'Sugar: business income = sale − market value of cane used − manufacturing cost')
    ag1 = ck3.add('2400000-1500000', 'Agricultural income on cane used = market value − cultivation cost')
    tea_ag = ck3.add('0.6*2000000', 'Tea grown and manufactured: 60% agricultural')
    tea_bu = ck3.add('0.4*2000000', 'Tea: 40% business')
    i3 = {'id': 'i3', 'title': 'Splitting composite income (Rules 270 and 271)', 'difficulty': 'core', 'minutes': 7,
          'q': '(a) Ela grows sugarcane (cultivation cost ₹15 lakh, market value ₹24 lakh) and uses all of it in her sugar factory; manufacturing costs ₹2 lakh and sugar sells for ₹32 lakh. (b) Farhan grows tea and manufactures it in India; profit on sale of tea is ₹20 lakh. Split each into agricultural and business income.',
          'solution': [table(['Case', 'Agricultural income ₹', 'Business income ₹'], [
              ['(a) Sugar (Rule 270 — market value of cane deducted)', inr(ag1), inr(bus)],
              ['(b) Tea grown and manufactured (Rule 271 — 60:40)', inr(tea_ag), inr(tea_bu)]], title='Answer'),
              note('Rule 271 percentages: rubber 65% agricultural; coffee grown and cured 75%; coffee grown, cured, roasted and ground 60%; tea 60%.')],
          'checks': list(ck3)}

    urban = table(['Population of municipality / cantonment', 'Land treated as urban if within (aerial distance from its limits)'], [
        ['Within the municipality/cantonment itself, population 10,000 or more', 'The local limits'],
        ['More than 10,000 up to 1,00,000', '2 km'],
        ['More than 1,00,000 up to 10,00,000', '6 km'],
        ['More than 10,00,000', '8 km'],
    ], title='Urban agricultural land — s. 2(22)(iii)(A)/(B)')
    slabs = table(['Default regime — s. 202(1)', 'Rate', 'Optional regime (below 60)', 'Rate'], [
        ['Up to ₹4,00,000', 'Nil', 'Up to ₹2,50,000', 'Nil'],
        ['₹4,00,001 – ₹8,00,000', '5%', '₹2,50,001 – ₹5,00,000', '5%'],
        ['₹8,00,001 – ₹12,00,000', '10%', '₹5,00,001 – ₹10,00,000', '20%'],
        ['₹12,00,001 – ₹16,00,000', '15%', 'Above ₹10,00,000', '30%'],
        ['₹16,00,001 – ₹20,00,000', '20%', 'Senior (60–79): BEL ₹3,00,000', ''],
        ['₹20,00,001 – ₹24,00,000', '25%', 'Very senior (80+): BEL ₹5,00,000; then 20% up to ₹10 L', ''],
        ['Above ₹24,00,000', '30%', '', ''],
    ], title='Slab rates — tax year 2026-27')
    special = table(['Section', 'Income', 'Rate'], [
        ['197', 'Long-term capital gains (general)', '12.5% (resident individual/HUF: land or building acquired before 23.7.2024 — tax capped at 20% with indexation)'],
        ['198', 'LTCG on STT-paid equity shares, equity-oriented fund units, business trust units', '12.5% on gains above ₹1.25 lakh'],
        ['196', 'STCG on STT-chargeable equity shares and units', '20%'],
        ['194 (Table Sl. 1)', 'Winnings from lotteries, crosswords, races, card games, gambling, betting', '30%'],
        ['194 (Table Sl. 5)', 'Net winnings from online games', '30%'],
        ['194 (Table Sl. 4)', 'Income from transfer of virtual digital assets', '30%'],
        ['195', 'Unexplained credits, investments, assets, expenditure, hundi borrowings', '30% + surcharge 25% + cess — effective 39%'],
    ], title='Special rates (both regimes)')
    sur = table(['Total income', 'Default regime', 'Optional regime'], [
        ['Above ₹50 lakh up to ₹1 crore', '10%', '10%'],
        ['Above ₹1 crore up to ₹2 crore', '15%', '15%'],
        ['Above ₹2 crore up to ₹5 crore', '25%', '25%'],
        ['Above ₹5 crore', '25%', '37%'],
        ['Tax on dividends and capital gains u/s 196/197/198', 'Surcharge capped at 15%', 'Surcharge capped at 15%'],
    ], title='Surcharge for individuals/HUF/AOP/BOI/AJP (marginal relief available)')
    ent = table(['Assessee', 'Income-tax rate', 'Surcharge'], [
        ['Firm / LLP / local authority', '30%', '12% if total income > ₹1 crore'],
        ['Co-operative society (normal)', '10% up to ₹10,000; 20% next ₹10,000; 30% above ₹20,000 (or 22% under s. 203)', '7% (₹1–10 crore); 12% above ₹10 crore; 10% flat under s. 203'],
        ['Domestic company — turnover in TY 2024-25 ≤ ₹400 crore', '25%', '7% (₹1–10 crore); 12% above ₹10 crore'],
        ['Domestic company opting for s. 200', '22%', '10% flat'],
        ['Other domestic companies', '30%', '7% / 12%'],
        ['Foreign company', '35% (50% on certain old approved royalty/FTS agreements)', '2% (₹1–10 crore); 5% above ₹10 crore'],
    ], title='Rates for other assessees (plus cess 4%)')

    concepts = [
        C('c1', T1, [
            'Article 265: no tax can be levied or collected except by authority of law. Entry 82 of the Union List lets Parliament tax income other than agricultural income.',
            'Direct taxes (income-tax) cannot be shifted to others; indirect taxes (GST, customs) are passed on.',
            'Income-tax law has five components: the Income-tax Act, 2025 (in force from 1 April 2026; whole of India; 23 chapters, 536 sections, 16 Schedules — replacing the 1961 Act); the annual Finance Act (First Schedule Part IB — rates for the current tax year; Part II — TDS rates; Part III — rates for salary TDS and advance tax for those leaving the default regime; Part IV — rules for net agricultural income); the Income-tax Rules, 2026 ("prescribed" means prescribed by rules — s. 2(80)); CBDT circulars (binding on the department, not on assessees, who may use beneficial ones) and notifications; and court decisions (Supreme Court law binds all; a High Court binds its State).',
            'Structure: section → sub-section (1) → clause (a) → sub-clause (i). Definitions are mostly in section 2 (e.g. clause (5) agricultural income).'],
          'The Act is the rulebook, the Finance Act sets this year\'s prices, the Rules give procedures, circulars explain, and courts settle disputes.',
          'Budget day changes rates through the Finance Act without touching the main Act\'s structure.'),
        C('c2', T2, [
            'Charging section 4: income-tax (including any additional income-tax) is charged at rates fixed by the Finance Act and/or the Act (e.g. s. 202(1)), on every person, on the total income of the tax year (and in specified cases income of other periods), subject to the Act.',
            'Person (s. 2(77)): individual, HUF, company, firm, AOP or BOI (whether or not formed to earn income), local authority, and artificial juridical person — seven categories, each a separate tax entity.',
            'Assessee (s. 2(11)): a person by whom tax or any sum is payable, and includes a person in respect of whom proceedings are taken for his own or another\'s income, loss or refund, a deemed assessee and an assessee in default. Every assessee is a person; not every person is an assessee.',
            'Assessment (s. 2(13)) is the procedure of determining income by the Assessing Officer and includes reassessment and recomputation.'],
          'Section 4 is the engine of the Act — without it no tax could be charged at all.',
          'A minor\'s income is assessed through a guardian; a deceased person\'s through the legal representative.'),
        C('c3', T3, [
            'Individual: a natural person, including a minor or a person of unsound mind (assessed through guardian/manager).',
            'HUF: not defined in the Act; under Hindu law, all males lineally descended from a common ancestor with their wives and daughters. Coparceners (within four degrees including the Karta) acquire interest by birth; since 6 September 2005 daughters are coparceners equal to sons; wives and daughters-in-law are members, not coparceners. Mitakshara (rest of India) — right by birth; Dayabhaga (West Bengal, Assam) — right only on father\'s death. No minimum of two male members is needed.',
            'Company (s. 2(28)): Indian company, foreign body corporate, bodies assessed as companies under the 1961 Act, and bodies declared by CBDT. Domestic company (s. 2(42)): Indian company, or one that has made prescribed arrangements to declare and pay dividends in India. Indian company (s. 2(53)): formed and registered under Indian company law with registered or principal office in India (also certain statutory corporations and declared bodies). Foreign company (s. 2(46)): not domestic.',
            'Company in which the public are substantially interested (s. 2(29)) includes government/RBI-owned (40%+) companies, section 8 companies, CBDT-declared companies without share capital, Nidhis, companies 50%+ held by co-operatives, and non-private companies whose equity is listed at year-end or 50% (40% for manufacturing, shipbuilding, mining, power) held by government, statutory corporations or widely held companies. All others (including all private companies) are closely held.',
            'Firm, partner and partnership include LLPs and their partners; a minor admitted to benefits is a partner. AOP: persons (any kind) joining for a common purpose to produce income; BOI: only individuals. Local authority: taxable on business income except from supplying commodities or services within its own area (water and electricity supply even outside is exempt). Artificial juridical persons: deities, universities, bar councils, etc.'],
          'The seven "persons" are seven different taxpayer boxes; each fills its own return.',
          'A joint venture of a firm, a company and an individual for one project is assessed as an AOP.'),
        C('c4', T4, [
            'Tax year (s. 3): the financial year of twelve months from 1 April. For a business, profession or source of income newly started, it runs from the date of start to the following 31 March.',
            'Income of a tax year is assessed after the year ends — except where the revenue may be at risk, when it is taxed in the same year: shipping by non-residents (s. 316 — 7.5% of freight etc. deemed income; ship cleared only after tax arrangement), individuals leaving India with no intention to return (s. 317), AOP/BOI/AJP formed for a particular event and likely to dissolve (s. 318), persons likely to transfer assets to avoid tax (s. 319), and discontinued business at the AO\'s discretion (s. 320).',
            'Under the 2025 Act the single term "tax year" replaces the earlier pair "previous year/assessment year".'],
          'The tax year is the season in which runs are scored; the assessment is the scorecard written after the season — unless the player is about to leave the ground.',
          'A CA starting practice on 1 July 2026 has a first tax year from 1 July 2026 to 31 March 2027.'),
        C('c5', T5, [
            'Income (s. 2(49)) is an inclusive definition covering, among others: profits and gains; dividends; perquisites and profits in lieu of salary; special allowances; benefits to directors and substantial shareholders; business receipts deemed income; capital gains; winnings from lotteries, crosswords, races, card games and gambling (including TV and online game shows); employees\' PF/ESI contributions received by the employer; keyman insurance sums; non-compete receipts; FMV of inventory converted to capital asset; forfeited advances for capital assets; gifts without or for inadequate consideration; compensation on termination of employment; taxable life-insurance receipts; and government subsidies or grants (unless reduced from the cost of depreciable assets).',
            'Concepts: casual receipts can be income; some capital receipts are specifically included; income is net of allowable expenditure; due or receipt basis per method of accounting; diversion of income by overriding title is not income of the assessee, but application of income is.',
            'Capital vs revenue: fixed capital (capital receipt) vs circulating capital (revenue); sale of capital asset (capital gains) vs trading asset (business income); motive decides profit on shares (investor vs dealer); even a single transaction can be an adventure in the nature of trade; liquidated damages for delay in acquiring a capital asset and compensation for sterilising the profit-earning source are capital; compensation for losing the only agency is capital but taxable under s. 26(2)(b), while losing one of many agencies is revenue; gifts are generally capital but taxed in specified cases (s. 92(2)(m)).',
            'Securities held by FPIs and investment funds as per SEBI rules are always capital assets.'],
          'Income is like a river — regular flows are clearly income, and the law also names certain floods (lottery wins, capital gains) as income.',
          'A builder\'s flats are stock-in-trade; the same flats held by a doctor are capital assets.'),
        C('c6', T6, [
            'Unexplained credits (s. 102): a credit in the books without a satisfactory explanation of nature and source is income. For loans, the lender must also explain the source; for share capital or premium in a closely held company, each resident shareholder must explain the source.',
            'Unexplained investments (s. 103), assets — including money, bullion, jewellery, virtual digital assets (s. 104), expenditure (s. 105), and amounts borrowed or repaid on a hundi or negotiable instrument otherwise than by account-payee cheque or specified mode (s. 106) — are deemed income of that tax year (hundi amount taxed only once).',
            'Section 195: such deemed income is taxed at 30% plus 25% surcharge plus cess — effectively 39% — with no deduction, allowance or set-off of loss.'],
          'Money that cannot explain where it came from pays the heaviest toll.',
          'Gold found worth ₹42 lakh against recorded cost of ₹21.5 lakh can lead to ₹20.5 lakh being added as income.'),
        C('c7', T7, [
            'Agricultural income (s. 2(5)) is exempt and includes: (1) rent or revenue from land in India used for agriculture (ownership not needed — a tenant sub-letting also earns it); (2) income from such land by agricultural operations, by processes ordinarily employed by a cultivator to make produce marketable (threshing, winnowing, cleaning, drying), or by selling such produce; (3) income from a farm building on or near the land, used as dwelling, store or out-house because of connection with the land, if the land is assessed to land revenue or local rate, or else is not urban; (4) income from saplings or seedlings grown in a nursery.',
            'Agriculture means basic operations (tilling, sowing) and subsequent operations done with them. Not agricultural: dairy, poultry, fisheries, livestock breeding, spontaneously grown forest trees, butter making in a factory, commission computed on a company\'s profits, letting land or buildings for non-agricultural use, and gains on transfer of urban agricultural land (taxable as capital gains u/s 67).',
            'Composite income: Rule 270 — where produce grown by the assessee is used in his business, deduct its market value (average market price if ordinarily sold raw; otherwise cultivation cost + land revenue/rent + reasonable profit). Rule 271 — rubber 65% agricultural; coffee grown and cured 75%; coffee grown, cured, roasted and ground 60%; tea 60%.'],
          'Agricultural income is the farmer\'s harvest — the moment it becomes a factory product, part of the profit belongs to business.',
          'Tea estates report 60% of their profit as exempt agricultural income and 40% as taxable business income.',
          blocks=[urban]),
        C('c8', T8, [
            'Steps: (1) residential status; (2) classify income under five heads — Salaries, House property, Profits and gains of business or profession, Capital gains, Other sources (s. 13); (3) compute each head with exemptions and deductions (expenditure on exempt income disallowed — s. 14 and Rule 14, even if no exempt income arose that year); (4) club income of spouse, minor child etc.; (5) set off and carry forward losses; (6) gross total income; (7) Chapter VIII deductions (mostly only if the default regime is given up); (8) total income rounded to nearest ₹10 (s. 516).',
            '(9) Apply rates; (10) rebate u/s 156 / surcharge; (11) health and education cess 4%; (12) alternate minimum tax under s. 206(2) where applicable (not for those under the default regime); (13) compare regimes; (14) adjust advance tax (15 June, 15 September, 15 December, 15 March; presumptive-income residents by 15 March), TDS and TCS; (15) tax payable or refundable rounded to ₹10.',
            'Companies and firms must file returns even without taxable income; others file when conditions apply.'],
          'Computing total income is a recipe with fixed order — skip a step and the dish fails.',
          'Salary TDS is deducted at payment; most other TDS at credit or payment, whichever is earlier.'),
        C('c9', T9, [
            'The default (new) regime under section 202 applies to individuals, HUFs, AOPs (other than co-operative societies), BOIs and AJPs unless they opt out (s. 202(4)).',
            'Under it, certain items are not allowed (s. 202(2)): LTC, HRA, most special allowances (except prescribed ones, e.g. transport for disabled employees), professional tax, minor-child income exemption, interest on self-occupied property, additional depreciation, scientific research donations under s. 45(3)(a)–(c), s. 46 incentives, and Chapter VIII deductions except employer\'s NPS contribution (s. 124(1)/(2)), Agnipath contribution (s. 125(2)) and new employees (s. 146). House property loss cannot be set off against other heads; related brought-forward losses lapse.',
            'Opting out: business or professional income — by the due date of return; applies to later years; can be withdrawn only once (after which re-entry is barred unless business income ceases). Others — choose every year with the return.',
            'Slab rates are in the table. Under the optional regime, senior citizens (60–79) have ₹3 lakh and very senior citizens (80+) ₹5 lakh basic exemption; a person born on 1 April is treated as attaining the age on the previous 31 March.'],
          'The default regime is a fixed-price meal with lower rates but no extras; the optional regime lets you order deductions at a higher base price.',
          'Salaried people with large home-loan interest and 80C-type investments often find the optional regime cheaper.',
          blocks=[slabs]),
        C('c10', T10, [
            'Rebate (s. 156) for resident individuals: default regime — up to ₹60,000 (i.e. no tax) if total income ≤ ₹12 lakh; just above ₹12 lakh, marginal rebate = tax minus the excess over ₹12 lakh, when positive; not available against tax on special-rate income like s. 196/197/198 gains. Optional regime — up to ₹12,500 if total income ≤ ₹5 lakh (not against tax on s. 198 LTCG); no marginal rebate.',
            'Surcharge (table) with marginal relief so that tax plus surcharge never rises by more than the income above each threshold.',
            'Health and education cess: 4% of income-tax as reduced by rebate or increased by surcharge — for all assessees.',
            'Special rates apply to specific incomes in both regimes; slab rates apply to the rest after using any unused basic exemption.'],
          'Rebate is a discount for the small bill; surcharge is a premium on the big one; cess is the service charge on every bill.',
          'A resident with ₹12.15 lakh income under the default regime pays just ₹15,600 because of marginal rebate.',
          blocks=[special, sur]),
        C('c11', T11, [
            'Agricultural income is exempt, but for individuals, HUFs, AOPs, BOIs and AJPs it is aggregated for rate purposes if net agricultural income exceeds ₹5,000 and non-agricultural income exceeds the basic exemption limit (₹4 lakh default; ₹2.5/3/5 lakh optional by age).',
            'Formula: Zn = Xn − Yn, where Xn is tax on (total income + net agricultural income) and Yn is tax on (net agricultural income + basic exemption limit). Then add surcharge, deduct rebate u/s 156 if eligible, and add 4% cess.',
            'Not applicable to companies, firms, LLPs, co-operatives or local authorities.'],
          'Partial integration lets the farm income stand on the first steps of the slab ladder so that other income starts higher up.',
          'A salaried person with family farm income pays a higher marginal rate on salary though the farm income itself is not taxed.'),
        C('c12', T12, [
            'Other assessees pay flat rates (table), with surcharge and marginal relief, plus 4% cess. Special capital gains rates under ss. 196–198 also apply to them.',
            'Firms and LLPs: 30%, surcharge 12% above ₹1 crore.',
            'Domestic companies: 25% if turnover or gross receipts of tax year 2024-25 ≤ ₹400 crore; 22% under s. 200 (with 10% surcharge, no thresholds); otherwise 30%. Foreign companies: 35%.',
            'Co-operative societies: slab of 10/20/30% on small bands, or 22% under s. 203.'],
          'Individuals climb a slab staircase; firms and companies take a flat lift.',
          'Most mid-sized Indian companies pay 25% plus surcharge and cess.',
          blocks=[ent]),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Choosing a regime for a salaried client', 'role': 'Tax consultant',
         'situation': 'A client earns ₹16 lakh salary and has deductions available only under the optional regime.',
         'steps': ['Compute tax under the default regime (with standard deduction and only allowed items).', 'Compute tax under the optional regime with all eligible exemptions and deductions.', 'Recommend the lower; remind that a salaried person can switch every year with the return.'],
         'takeaway': 'Always compute both regimes before advising.'},
        {'id': 'j2', 'title': 'Farm house income question', 'role': 'Article assistant',
         'situation': 'A client\'s farm building is 5 km from a municipality of 3.5 lakh population.',
         'steps': ['Population above 1 lakh up to 10 lakh → urban if within 6 km.', '5 km is within 6 km → urban agricultural land.', 'Income from the farm building is not agricultural income (unless the land is assessed to land revenue).'],
         'takeaway': 'Check population band and aerial distance together.'},
    ]

    mcqs = [
        Q('m1', 'The Income-tax Act, 2025 came into force on:', ['1 April 2026', '1 April 2025', '1 October 2025', '1 January 2026'], 0,
          'The 2025 Act came into force on 1 April 2026, replacing the Income-tax Act, 1961, which governed income up to 31 March 2026. It extends to the whole of India. In practice: tax year 2026-27 is the first year under the new Act.', 'c1', T1),
        Q('m2', 'Circulars issued by the CBDT are:', ['Binding on the department; assessees may take benefit of beneficial ones', 'Binding on assessees but not the department', 'Not binding on anyone', 'Binding only on courts'], 0,
          'Circulars guide officers and bind the income-tax department; they are not binding on assessees, who can rely on them when beneficial. Courts are not bound by circulars. In practice: taxpayers cite favourable circulars in assessments.', 'c1', T1),
        Q('m3', 'Which of these is NOT a separate "person" under section 2(77)?', ['A branch office of a company', 'A Hindu undivided family', 'A local authority', 'An artificial juridical person'], 0,
          'Section 2(77) lists seven categories: individual, HUF, company, firm, AOP or BOI, local authority and artificial juridical person. A branch is only part of the company and is not a separate person. In practice: the company files one return covering all its branches.', 'c2', T2, 'moderate'),
        Q('m4', 'Since 6 September 2005, a daughter in a Hindu family governed by Mitakshara law:', ['Is a coparcener by birth, with rights equal to a son', 'Is only a member, not a coparcener', 'Becomes a coparcener only on marriage', 'Is a coparcener only in West Bengal'], 0,
          'Daughters became coparceners by birth with rights equal to sons from 6 September 2005; wives and daughters-in-law remain members only. Dayabhaga law prevails in West Bengal and Assam. In practice: a daughter can claim partition of HUF property.', 'c3', T3),
        Q('m5', 'A company incorporated outside India which has made prescribed arrangements to declare and pay dividends in India is:', ['A domestic company', 'An Indian company', 'Always a foreign company', 'Not a company for tax purposes'], 0,
          'Section 2(42) treats as domestic both Indian companies and any other company that has made prescribed arrangements in India for declaring and paying dividends. It is not an Indian company because it was not formed under Indian law. In practice: this affects the rate of tax.', 'c3', T3, 'moderate'),
        Q('m6', 'Ms. R starts her CA practice on 1 September 2026. Her first tax year is:', ['1.9.2026 to 31.3.2027', '1.4.2026 to 31.3.2027', '1.9.2026 to 31.8.2027', 'Calendar year 2026'], 0,
          'For a profession newly set up, the tax year starts on the date of setting up and ends on the following 31 March under section 3. Later years are full financial years. In practice: the first year is shorter than twelve months.', 'c4', T4),
        Q('m7', 'Which is NOT a case where income is assessed in the same tax year?', ['A salaried employee changing jobs within India', 'Shipping business of a non-resident', 'Individual leaving India with no intention to return', 'AOP formed for a particular event likely to dissolve'], 0,
          'Sections 316–320 cover non-resident shipping, persons leaving India, AOP/BOI formed for an event, persons likely to transfer assets to avoid tax, and discontinued business. A job change is routine. In practice: these exceptions protect revenue.', 'c4', T4),
        Q('m8', 'Under section 316, the deemed income of a non-resident shipping company carrying goods from an Indian port is:', ['7.5% of the amount paid or payable for carriage', '10% of freight', '5% of freight', 'Actual profit only'], 0,
          'Section 316 deems 7.5% of amounts paid or payable on account of such carriage, including demurrage and handling charges, as income taxable in the same year. The ship may leave only after tax is paid or arranged. In practice: port clearance depends on it.', 'c4', T4, 'moderate'),
        Q('m9', 'Compensation received by an assessee on termination of his only agency is:', ['A capital receipt, but taxable under section 26(2)(b)', 'An exempt capital receipt', 'Always revenue income', 'Income from other sources'], 0,
          'Loss of the only source of business makes the compensation capital in nature, but the Act specifically taxes it as business income under section 26(2)(b). Losing one of many agencies gives a revenue receipt. In practice: read the specific provision before treating a receipt as exempt.', 'c5', T5, 'moderate'),
        Q('m10', 'Unexplained investments deemed as income under section 103 are taxed at:', ['30% plus 25% surcharge plus cess — effectively 39%', 'Slab rates', '20%', '15%'], 0,
          'Section 195 taxes income deemed under sections 102–106 at 30%, with surcharge of 25% and cess, giving an effective 39%, and allows no deduction or set-off. Slab rates do not apply. In practice: unexplained cash deposits face this rate.', 'c6', T6),
        Q('m11', 'A farm building 5 km from a municipality with population 3,50,000 (land not assessed to land revenue). Income from it is:', ['Not agricultural income, as the land is urban', 'Agricultural income', 'Exempt only if used as dwelling', 'Agricultural income because it is beyond 2 km'], 0,
          'For population above 1 lakh up to 10 lakh, land within 6 km is urban; 5 km falls inside, so farm-building income is not agricultural income. The 2 km limit applies to smaller towns. In practice: check both population and distance.', 'c7', T7, 'moderate'),
        Q('m12', 'Which is agricultural income?', ['Income from saplings grown in a nursery', 'Income from poultry farming', 'Income from dairy farming', 'Income from sale of spontaneously grown forest trees'], 0,
          'Section 2(5) specifically includes income from saplings or seedlings grown in a nursery. Poultry, dairy, fisheries and spontaneously grown trees involve no agricultural operation on land and are not agricultural income. In practice: nursery owners enjoy exemption.', 'c7', T7),
        Q('m13', 'Income from tea grown and manufactured in India is treated as agricultural to the extent of:', ['60%', '40%', '65%', '75%'], 0,
          'Rule 271 treats 60% of income from tea grown and manufactured by the seller as agricultural and 40% as business. Rubber is 65%, and coffee grown and cured 75%. In practice: tea companies show 40% taxable.', 'c7', T7, 'core', check=60),
        Q('m14', 'Expenditure incurred in relation to exempt income is:', ['Not allowable under section 14', 'Fully allowable', 'Allowable only under the default regime', 'Allowable at the assessee\'s option'], 0,
          'Section 14 disallows expenditure relating to income that does not form part of total income, using the method in Rule 14, even if no exempt income arose that year. In practice: interest on borrowings used to buy shares yielding exempt income may be disallowed.', 'c8', T8),
        Q('m15', 'Total income is rounded off to the nearest multiple of ₹10 under section:', ['516', '202', '156', '4'], 0,
          'Section 516 requires total income, and tax payable or refundable, to be rounded to the nearest multiple of ten rupees. Section 202 is the default regime, 156 is rebate and 4 is the charging section. In practice: returns show rounded totals.', 'c8', T8, 'core', check=516),
        Q('m16', 'Under the default regime, the basic exemption limit for tax year 2026-27 is:', ['₹4,00,000', '₹3,00,000', '₹2,50,000', '₹5,00,000'], 0,
          'Section 202(1) sets nil tax up to ₹4,00,000, then 5% up to ₹8 lakh rising in ₹4 lakh steps to 30% above ₹24 lakh. ₹2.5, 3 and 5 lakh are optional-regime limits by age. In practice: with rebate, residents pay no tax up to ₹12 lakh.', 'c9', T9, 'core', check=400000),
        Q('m17', 'A person having business income who opts out of the default regime:', ['Must opt by the return due date; the choice continues and can be withdrawn only once', 'Can switch every year freely', 'Can never opt out', 'Must opt out at the start of the year'], 0,
          'Under section 202(4), business or professional taxpayers exercise the option by the due date of return; it applies to later years and can be withdrawn only once, after which they cannot opt out again unless business income ceases. Others choose yearly. In practice: plan the choice carefully.', 'c9', T9, 'moderate'),
        Q('m18', 'Mr. X, resident, was born on 1 April 1967. For tax year 2026-27 under the optional regime he is:', ['A senior citizen, treated as 60 on 31 March 2027', 'Not a senior citizen', 'A very senior citizen', 'Eligible only from tax year 2027-28'], 0,
          'CBDT Circular 28/2016 treats a person born on 1 April as attaining an age on the preceding 31 March, so he turns 60 within tax year 2026-27 and gets the ₹3 lakh limit. In practice: check birthdays falling on 1 April.', 'c9', T9, 'moderate'),
        Q('m19', 'A resident individual has total income of ₹12,40,000 under the default regime. Tax (before cess) after rebate is:', [R(40000), R(66000), 'Nil', R(26000)], 0,
          f'Tax on ₹12,40,000 is ₹66,000; excess over ₹12 lakh is ₹40,000; marginal rebate = 66,000 − 40,000 = ₹26,000; tax = ₹40,000 before cess (₹41,600 with cess). In practice: marginal rebate prevents a cliff at ₹12 lakh.', 'c10', T10, 'hard', check=40000),
        Q('m20', 'Under the optional regime, the maximum rebate under section 156 is:', ['₹12,500 for total income up to ₹5 lakh', '₹60,000 for income up to ₹12 lakh', '₹25,000 for income up to ₹7 lakh', 'No rebate'], 0,
          'A resident individual opting out gets rebate of tax up to ₹12,500 if total income does not exceed ₹5 lakh, with no marginal relief; the ₹60,000/₹12 lakh rebate belongs to the default regime. In practice: compare both regimes near these thresholds.', 'c10', T10),
        Q('m21', 'The highest surcharge for an individual with income above ₹5 crore under the default regime is:', ['25%', '37%', '15%', '10%'], 0,
          'Under the default regime surcharge is capped at 25%; the 37% rate applies only under the optional regime above ₹5 crore. Surcharge on dividend and specified capital gains is capped at 15% in both. In practice: very high earners often prefer the default regime.', 'c10', T10, 'moderate', check=25),
        Q('m22', 'Partial integration of agricultural income applies only when net agricultural income exceeds:', ['₹5,000 and non-agricultural income exceeds the basic exemption limit', '₹50,000', '₹1 lakh', 'The basic exemption limit alone'], 0,
          'Both conditions are needed: net agricultural income above ₹5,000 and non-agricultural income above the applicable basic exemption limit. It applies to individuals, HUFs, AOPs, BOIs and AJPs only. In practice: companies and firms are outside it.', 'c11', T11),
        Q('m23', 'A domestic company whose turnover in tax year 2024-25 was ₹350 crore (not opting for s. 200) pays income-tax at:', ['25%', '30%', '22%', '35%'], 0,
          'Domestic companies with turnover or gross receipts in tax year 2024-25 up to ₹400 crore pay 25%; those opting for section 200 pay 22%; others 30%. 35% applies to foreign companies. In practice: check the reference year turnover.', 'c12', T12, 'core', check=25),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Ananya — slab tax and cess', 2, 'computation', 'ananya|18,40,000|default', nums=[t1, tot1]),
           S('s2', 'Bharat — marginal rebate', 2.5, 'computation', 'rebate|marginal', nums=[t2, rb2, tot2]),
           S('s3', 'Chitra — senior slabs', 1.5, 'computation', 'senior|3,00,000|chitra', nums=[t3, tot3])],
          ['Show slab-wise working.'], ['Giving full rebate at ₹12.4 lakh.', 'Using ₹2.5 lakh limit for a 65-year-old.'], ['One table per person.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Conditions for integration', 1, 'concept', '5,000', 'exemption|4,00,000'),
           S('s2', 'Xn — tax on aggregate', 1.5, 'computation', 'aggregate|xn', nums=[xn]),
           S('s3', 'Yn — tax on agri + BEL', 1.5, 'computation', 'yn|7,00,000', nums=[yn]),
           S('s4', 'Zn and final tax', 1, 'computation', 'zn|cess', nums=[zn, tz])],
          ['Write the formula Zn = Xn − Yn.'], ['Adding the BEL to total income instead of agricultural income.'], ['Step table.'], pad='table', checks=list(ck2)),
        W('q3', 4, 'Explain with reasons whether the following are agricultural income: (a) rent from agricultural land in Nepal; (b) income from sale of rice processed by the cultivator by cleaning and packing; (c) income from a dairy on agricultural land; (d) income from a farm building 9 km from a city with population 15 lakh.',
          [table(['Item', 'Agricultural?', 'Reason'], [
              ['(a) Land in Nepal', 'No', 'Land must be situated in India'],
              ['(b) Rice cleaned and packed', 'Yes', 'Processes ordinarily employed to make produce fit for market'],
              ['(c) Dairy', 'No', 'Dairy farming is not agriculture'],
              ['(d) Farm building 9 km from a 15-lakh city', 'Yes (if other conditions met)', 'Beyond 8 km, so land is not urban']], title='Answer')],
          [S('s1', 'Foreign land not agricultural', 1, 'application', 'india|nepal|foreign'),
           S('s2', 'Ordinary process — agricultural', 1, 'application', 'process|market'),
           S('s3', 'Dairy not agricultural', 1, 'application', 'dairy'),
           S('s4', '8 km rule — rural', 1, 'application', '8 km|beyond|rural|not urban')],
          ['Give one reason per item.'], ['Treating all land-related income as agricultural.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What does the charging section 4 provide?',
          'Income-tax is charged at rates fixed by the Finance Act or the Act, on every person, on the total income of the tax year, subject to the provisions of the Act.',
          [P('p1', 'Rates by Finance Act or the Act', 3, 'finance act|rate'), P('p2', 'Every person', 3, 'person'), P('p3', 'Total income of tax year', 4, 'total income|tax year')], 'c2'),
        V('v2', 'What is the tax year for a business set up on 1 November 2026?',
          'It begins on the day the business starts and runs only up to the end of that financial year, that is the thirty first of March 2027.',
          [P('p1', 'Starts on date of setting up', 5, 'day the business starts|date of setting|starts'), P('p2', 'Ends 31 March 2027', 5, 'thirty first of march|31 march|march 2027')], 'c4'),
        V('v3', 'Name the four parts of agricultural income under section 2(5).',
          'Rent or revenue from agricultural land in India, income from agricultural operations, processing and sale of produce, income from farm buildings, and income from saplings or seedlings in a nursery.',
          [P('p1', 'Rent or revenue', 2, 'rent|revenue'), P('p2', 'Agriculture, processing and sale', 3, 'operation|process|sale'), P('p3', 'Farm building', 3, 'building'), P('p4', 'Nursery', 2, 'nursery|sapling|seedling')], 'c7'),
        V('v4', 'What are the conditions for rebate under section 156 in the default regime?',
          'The individual must be resident; if total income is up to twelve lakh rupees, rebate equals tax up to sixty thousand rupees; slightly above twelve lakh, marginal rebate equals tax minus the income above twelve lakh.',
          [P('p1', 'Resident individual', 2, 'resident'), P('p2', '₹12 lakh / ₹60,000', 4, '12 lakh|twelve lakh|60,000|sixty thousand'), P('p3', 'Marginal rebate', 4, 'marginal|minus|excess')], 'c10'),
        V('v5', 'State the default regime slab rates for tax year 2026-27.',
          'Nil up to four lakh, five percent up to eight lakh, ten percent up to twelve lakh, fifteen percent up to sixteen lakh, twenty percent up to twenty lakh, twenty five percent up to twenty four lakh and thirty percent above.',
          [P('p1', 'Nil up to ₹4 lakh', 3, 'four lakh|4 lakh|4,00,000'), P('p2', 'Steps of ₹4 lakh, 5%–25%', 4, 'five|ten|fifteen|twenty'), P('p3', '30% above ₹24 lakh', 3, 'thirty|30')], 'c9'),
    ]

    cases = [{'id': 'k1', 'title': 'The Gill family\'s tax questions', 'difficulty': 'moderate',
              'case': 'Harpreet Gill (resident, 45) has salary income giving total income of ₹11,80,000 under the default regime and net agricultural income of ₹2 lakh from Punjab farmland. Her father (resident, born 1 April 1946) earns ₹9 lakh of interest and has opted out of the default regime. The family also earns income from a dairy and from the sale of tea grown and processed on their Assam estate.',
              'mcqs': [
                  M('k1a', 'Harpreet\'s tax before cess, after partial integration and rebate, is:', ['₹17,000', 'Nil', '₹77,000', '₹27,000'], 0,
                    'Xn = tax on ₹13,80,000 = ₹87,000; Yn = tax on ₹6,00,000 = ₹10,000; Zn = ₹77,000. Total income ₹11.8 lakh is within ₹12 lakh, so rebate = lower of tax and ₹60,000 = ₹60,000, leaving ₹17,000 (₹17,680 with cess). In practice: integration can leave tax even below ₹12 lakh total income.', 'hard', check=17000, topic=T11),
                  M('k1b', 'Her father, born on 1 April 1946, for tax year 2026-27 is treated as:', ['A very senior citizen (80 on 31 March 2027) with ₹5 lakh exemption', 'A senior citizen with ₹3 lakh exemption', 'Not a senior citizen', 'Eligible for the default slabs only'], 0,
                    'Born on 1 April 1946, he attains 80 on 31 March 2027 under the CBDT clarification, so the very senior basic exemption of ₹5 lakh applies under the optional regime. In practice: 1 April birthdays shift age one day earlier.', 'moderate', topic=T9),
                  M('k1c', 'Income from the dairy is:', ['Not agricultural income — taxable', 'Exempt agricultural income', 'Agricultural if on farmland', 'Partly agricultural under Rule 271'], 0,
                    'Dairy farming is not an agricultural operation on land, so its income is taxable even if carried out on agricultural land. Rule 271 covers only rubber, coffee and tea. In practice: dairy income is business income.', 'core', topic=T7),
                  M('k1d', 'Income from tea grown and manufactured on the Assam estate is:', ['60% agricultural and 40% business', '100% agricultural', '65% agricultural', '75% agricultural'], 0,
                    'Rule 271 treats income from tea grown and manufactured by the seller in India as 60% agricultural and 40% business income. In practice: the 40% business portion is taxed at normal rates applicable to the assessee.', 'core', topic=T7),
              ]}]

    return unit(UID, 'p3', 'int-p3-a-ch01', 1, 'Basic Concepts',
                ['Explain the components of income-tax law, the charge of tax and key definitions under the Income-tax Act, 2025.',
                 'Determine the tax year and cases assessed in the same year.',
                 'Distinguish capital and revenue receipts and explain unexplained income provisions.',
                 'Identify agricultural income, apply Rules 270/271 and partial integration.',
                 'Compute tax under the default and optional regimes with rebate, surcharge and cess.'],
                {'difficulty': 'core', 'minutes': {'learn': 60, 'practice': 45}, 'prereq': [],
                 'exam_tip': 'Expect slab computations under both regimes, marginal rebate, partial integration, urban agricultural land and section numbers of the 2025 Act (2(5), 2(77), 3, 4, 156, 202).'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Income-tax Act, 2025 effective 1 April 2026; tax year replaces previous/assessment year.', 'Section 4 charges every person on total income of the tax year.',
                             'Seven persons: individual, HUF, company, firm, AOP/BOI, local authority, AJP.', 'Same-year assessment: ss. 316–320.',
                             'Unexplained income (ss. 102–106) taxed at 30% + 25% surcharge + cess (s. 195).', 'Agricultural income exempt; urban land by population/distance; Rules 270/271.',
                             'Default regime s. 202: nil to ₹4 L, then 5% steps per ₹4 L to 30% above ₹24 L; rebate ≤ ₹60,000 to ₹12 L with marginal rebate.',
                             'Optional regime: ₹2.5/3/5 L limits; 5/20/30%; rebate ≤ ₹12,500 to ₹5 L.', 'Cess 4% on all assessees.'],
                 'remember': ['Born on 1 April → age reached on 31 March.', 'Business taxpayers can withdraw opt-out only once.'],
                 'traps': ['Rebate not available against special-rate tax.', 'Agricultural income is outside total income for rebate tests.']},
                [('Charging section', 's. 4'), ('Agricultural income', 's. 2(5)'), ('Default regime', 's. 202'), ('Rebate', 's. 156'), ('Unexplained income rate', '39% effective (s. 195)'),
                 ('Rounding', 's. 516')],
                viva, cases,
                topics=['Introduction', 'Charge of Income Tax', 'Important Definitions', 'Steps for Computation of Total Income and Tax Payable', 'Rates of Tax, Surcharge & Cess',
                        'Rebate for Resident Individuals', 'Partial Integration of Agricultural Income with Non-agricultural Income'])
