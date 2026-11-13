"""CA Intermediate · Paper 3A Income-tax Law · Chapter 3 Heads of Income · Unit 5 Income from Other Sources (Income-tax Act, 2025; tax year 2026-27).
Scope follows the ICAI study material; section numbers and limits are taken from it; explanations and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-a-ch03-u05'
T1 = 'Residuary head and dividends (ss. 92, 2(40))'
T2 = 'Casual income and its tax rate (s. 194)'
T3 = 'Receipts without or for inadequate consideration (s. 92(2)(m))'
T4 = 'Other specific receipts (advance, interest on compensation, insurance)'
T5 = 'Incomes taxed here only if not business income'
T6 = 'Deductions allowed and disallowed (ss. 93-95)'


def build():
    # i1 — gifts and inadequate-consideration purchases
    ck = Checks()
    money = ck.add('40000+30000', 'Cash from two non-relatives — aggregate exceeds ₹50,000, so whole taxable')
    tol = ck.add('max(50000,0.10*4000000)', 'Tolerance for immovable property = higher of ₹50,000 and 10% of consideration')
    land = ck.add('4500000-4000000', 'Stamp duty value − price')
    tot = ck.add('70000+0+0+500000+0', 'Total taxable u/s 92(2)(m)')
    i1 = {'id': 'i1', 'title': 'Gifts and a bargain purchase', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Nikhil, a resident individual, received during tax year 2026-27: (a) ₹40,000 cash from a friend and ₹30,000 from a former colleague; (b) a watch worth ₹90,000 from his father\'s brother; (c) a painting worth ₹45,000 from a neighbour; (d) a plot bought from an unrelated seller for ₹40,00,000 with stamp duty value ₹45,00,000; (e) a car worth ₹6,00,000 from a friend. Compute income under section 92(2)(m).',
          'solution': [table(['Item', 'Reasoning', '₹'], [
              ['(a) Cash', 'Money from non-relatives totals ₹70,000 (> ₹50,000) → entire amount', inr(money)],
              ['(b) Watch', 'Father\'s brother is a relative → outside the provision', 'Nil'],
              ['(c) Painting', 'Movable property; aggregate FMV ₹45,000 does not exceed ₹50,000', 'Nil'],
              ['(d) Plot', 'Gap ₹5,00,000 exceeds tolerance of ' + inr(tol) + ' → whole gap taxable', inr(land)],
              ['(e) Car', 'A car is not "property" for this purpose', 'Nil'],
              ['Total', '', inr(tot)]], title='Computation'),
              note('Once a limit is crossed, the whole amount — not just the excess — is taxed.')],
          'checks': list(ck)}

    # i2 — family pension, interest on enhanced compensation and other items
    ck2 = Checks()
    fp = ck2.add('30000*12', 'Family pension for the year')
    fpd = ck2.add('min(360000/3,25000)', 'Deduction under default regime: lower of 1/3 and ₹25,000')
    ic = ck2.add('400000*0.5', 'Interest on enhanced compensation after 50% deduction')
    total = ck2.add('360000-25000+200000+60000+50000', 'Income from other sources (excluding lottery)')
    lot = ck2.add('0.30*100000', 'Tax on lottery at 30% (before cess)')
    i2 = {'id': 'i2', 'title': 'A widow\'s other-sources income', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Sunita, resident, aged 58, under the default regime, receives in tax year 2026-27: family pension ₹30,000 a month after her husband\'s death; interest of ₹4,00,000 on enhanced compensation for land acquired years ago (relating to earlier years); fixed deposit interest ₹60,000; dividends from an Indian company ₹50,000; and a lottery prize of ₹1,00,000. Compute income from other sources and tax on the lottery.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Family pension', '30,000 × 12', inr(fp)],
              ['Less deduction', 'Lower of 1/3 (1,20,000) and ₹25,000', inr(fpd)],
              ['Interest on enhanced compensation (net)', '4,00,000 − 50%', inr(ic)],
              ['FD interest', '', inr(60000)],
              ['Dividend (no deduction)', '', inr(50000)],
              ['Income from other sources at normal rates', '', inr(total)],
              ['Lottery — taxed separately at 30%', '1,00,000 × 30%', inr(lot)]], title='Computation'),
              note('The lottery is part of total income but no expense, Chapter VIII deduction or basic exemption can be set against it. Under the optional regime the family pension deduction cap would be ₹15,000.')],
          'checks': list(ck2)}

    # i3 — letting of machinery taxed under other sources
    ck3 = Checks()
    dep = ck3.add('0.15*2000000', 'Depreciation on WDV at 15%')
    inc = ck3.add('600000-40000-15000-300000', 'Net hire income')
    i3 = {'id': 'i3', 'title': 'Idle machinery let on hire', 'difficulty': 'core', 'minutes': 5,
          'q': 'Gopal closed his factory but keeps one plant (WDV ₹20,00,000, rate 15%) which he lets on hire to another manufacturer for ₹6,00,000 a year. He spends ₹40,000 on current repairs and ₹15,000 on insurance. The letting is not a business. Compute his income.',
          'solution': [table(['Particulars', '₹'], [
              ['Hire charges', inr(600000)],
              ['Less current repairs', inr(40000)],
              ['Less insurance premium', inr(15000)],
              ['Less depreciation (15% of 20,00,000)', inr(dep)],
              ['Income from other sources', inr(inc)]], title='Computation'),
              note('Had the letting been a business activity, the same items would be computed under business income.')],
          'checks': list(ck3)}

    gift = table(['Received', 'Without consideration — taxable', 'For inadequate consideration — taxable'], [
        ['Money', 'Whole sum if aggregate in the year exceeds ₹50,000', '—'],
        ['Movable property (shares, jewellery, bullion, art, drawings, sculptures, archaeological items)', 'Aggregate FMV if it exceeds ₹50,000', 'FMV − price, if the gap exceeds ₹50,000'],
        ['Land or building (capital asset)', 'Stamp duty value if it exceeds ₹50,000', 'Stamp duty value − price, if the gap exceeds the higher of ₹50,000 and 10% of price']],
        title='Section 92(2)(m) at a glance')
    deds = table(['Income', 'Deduction'], [
        ['Interest on securities', 'Reasonable commission to a banker or agent for realising it'],
        ['Letting of plant, machinery, furniture (with or without building)', 'Current repairs, rates and taxes, insurance, normal depreciation'],
        ['Family pension', 'Lower of 1/3 and ₹25,000 (default) or ₹15,000 (optional)'],
        ['Interest on compensation/enhanced compensation', '50%, and nothing else'],
        ['Employee contributions recovered by employer', 'Allowed if credited by the return due date'],
        ['Commuted pension from LIC; death gratuity under service pension codes', 'Entire amount'],
        ['Dividends and mutual fund income', 'No deduction'],
        ['Other income', 'Revenue expenditure wholly and exclusively to earn it']],
        title='Deductions under section 93')

    concepts = [
        C('c1', T1, [
            'Income from other sources is the residuary head: any taxable income not falling under the other four heads is taxed here (s. 92(1)). Computation follows the cash or mercantile basis regularly employed (s. 276).',
            'Dividends are always taxed here, at normal rates in the hands of residents. Deemed dividend [s. 2(40)] includes distribution of accumulated profits releasing company assets (at market value if in kind); issue of debentures or deposit certificates to members, and bonus shares given to preference holders; distributions on liquidation or capital reduction — each to the extent of accumulated profits.',
            'A loan or advance by a closely held company to a shareholder holding at least 10% of voting power, or to a concern in which he has a substantial interest (20% of income), or for his benefit, is deemed dividend to the extent of accumulated profits. Repayment later does not undo it.',
            'Not dividend: bonus shares to equity shareholders; loans in the ordinary course where lending is a substantial part of business; trade advances of a commercial nature (CBDT circular); shares distributed on demerger; and later dividends set off against a loan already taxed.',
            'Timing [s. 7(2)]: deemed dividend is income of the year it is declared, distributed or paid; interim dividend when unconditionally made available.'],
          'Profits that leave a company for its owners are dividends, whatever the form; the law looks through loans to controlling shareholders.',
          'A family company lends ₹12 lakh to a 15% shareholder while holding ₹9 lakh of accumulated profits — ₹9 lakh is deemed dividend.'),
        C('c2', T2, [
            'Casual income means winnings from lotteries, puzzles, horse and other races, card and other games, betting or gambling; it is taxed under this head.',
            'Such winnings are taxed at a flat 30% (plus surcharge and cess) under s. 194; net winnings from online games are also taxed at 30% under a separate entry.',
            'No expenditure or allowance, no Chapter VIII deduction and no adjustment of unexhausted basic exemption is permitted against these winnings, and no loss can be set off against them.',
            'The owner of race horses can deduct expenses of owning and maintaining them, and that loss can be carried forward under s. 115.'],
          'Luck is taxed at a flat rate with no deductions at all.',
          'A retired person with no other income who wins ₹2 lakh in a quiz contest still pays 30% plus cess on the whole amount.'),
        C('c3', T3, [
            'Money or specified property received by any person without consideration or for inadequate consideration is taxed as shown in the table. Property here means land or building, shares and securities, jewellery, archaeological collections, drawings, paintings, sculptures, works of art, bullion and virtual digital assets held as capital assets — not cars or household goods.',
            'Exclusions: receipts from a relative; on the occasion of the individual\'s marriage; under a will or inheritance; in contemplation of death; from a local authority; from or by registered non-profit organisations (with exceptions); in specified non-transfer transactions under s. 70; and by a trust created solely for relatives of the individual.',
            'Relative of an individual: spouse; brother or sister; spouse\'s brother or sister; brother or sister of either parent; lineal ascendants and descendants of the individual or spouse; and spouses of all these. For an HUF, any member.',
            'For immovable property, the agreement-date stamp duty value can be adopted when consideration was partly paid by a banking or online mode on or before that date. The cost of such property for later capital gains is the value already taxed.'],
          'Free or cheap acquisitions from outsiders are treated as income, because they enrich the recipient as surely as cash would.',
          'An aunt\'s gift of ₹5 lakh is tax-free; the same gift from a family friend is fully taxable.',
          blocks=[gift]),
        C('c4', T4, [
            'An advance received on a capital-asset deal that falls through and is forfeited is taxed here in the year of forfeiture [s. 92(2)(h)]; it then does not reduce cost of acquisition.',
            'Interest on compensation or enhanced compensation is taxed in the year of receipt regardless of the accounting method [s. 278(1)], under this head, with a 50% deduction.',
            'Compensation for termination or modification of employment received from someone other than the employer is taxed here; from the employer it is salary.',
            'Sums from a life insurance policy (other than ULIPs and keyman policies) that do not meet the Schedule II premium-to-sum-assured tests are taxed here. For policies from 1 April 2023, exemption needs premium within 10% of sum assured (15% for specified disabled or ill persons) and aggregate annual premium not above ₹5 lakh; death claims are always exempt.',
            'Keyman insurance receipts are taxed as salary or business income where applicable, otherwise here.'],
          'Several one-off receipts are parked under this head by specific provisions so they cannot escape tax.',
          'A buyer backs out of a plot deal in June 2026 and the ₹6 lakh token money kept by the seller is his income for 2026-27.'),
        C('c5', T5, [
            'Some incomes go to this head only if they are not business income: employee contributions to PF, superannuation, ESI or welfare funds received by an employer; hire income from machinery, plant or furniture; inseparable letting of a building with such assets; and interest on securities.',
            'Interest on securities (government or corporate) is taxed here unless the securities are stock-in-trade; banks holding non-SLR securities as part of business show the interest as business income.',
            'Certain interest is exempt under Schedule III — for example, interest on specified post office deposits and notified tax-free bonds — and is excluded from total income.'],
          'The same receipt can sit in business or other sources depending on whether the activity is a business.',
          'A company that lets its idle machinery once is taxed under other sources; an equipment-rental company is taxed under business.'),
        C('c6', T6, [
            'Deductions [s. 93] are listed in the table; dividends and mutual fund income get none.',
            'Not deductible [s. 94]: personal expenses; interest or salary payable outside India without TDS; excessive payments to related persons; cash payments above ₹10,000 a day (₹35,000 to transporters); 30% of sums payable to residents where TDS was not deducted or paid by the return due date; and any expense against casual winnings.',
            'Deemed income [s. 95]: a later recovery or remission of a loss, expense or liability earlier allowed under this head is taxed in the year received, as under business income.'],
          'This head allows only those expenses that are directly tied to earning the income, with fixed allowances for a few items.',
          'Bank collection charges on bond interest are deductible; interest on a personal loan used for a holiday is not.',
          blocks=[deds]),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Reviewing gifts received', 'role': 'Tax assistant',
         'situation': 'A client lists several gifts and a property purchase during the year.',
         'steps': ['Classify donors as relatives or not using the statutory list.', 'Check whether any receipt was on the occasion of marriage or by will.', 'Aggregate money and movable property from non-relatives against ₹50,000 each.', 'Test immovable property purchases against the higher of ₹50,000 and 10% of price.'],
         'takeaway': 'Get the relationship and the item type right before touching the numbers.'},
        {'id': 'j2', 'title': 'Deemed dividend check', 'role': 'Article assistant',
         'situation': 'During audit you notice a private company has lent money to a director.',
         'steps': ['Check whether the company is closely held and whether lending is its substantial business.', 'Confirm the director\'s voting power (10% or more) or interest in the borrowing concern.', 'Compare the loan with accumulated profits on the date of the loan.', 'Flag the deemed dividend for the director\'s return; trade advances are excluded.'],
         'takeaway': 'The deemed dividend is capped by accumulated profits on the loan date.'},
    ]

    mcqs = [
        Q('m1', 'Income from other sources is described as:', ['The residuary head for income not covered by other heads', 'The head for all investment income only', 'The head for income of non-residents', 'An optional head chosen by the assessee'], 0,
          'Section 92(1) brings to tax under this head any income chargeable under the Act that does not fall under salaries, house property, business or capital gains. It is the last head examined. In practice: classify under specific heads first.', 'c1', T1),
        Q('m2', 'A closely held trading company with accumulated profits of ₹6,00,000 lends ₹8,00,000 to a shareholder holding 12% voting power. Deemed dividend is:', ['₹6,00,000', '₹8,00,000', 'Nil', '₹96,000'], 0,
          'A loan by a closely held company (public not substantially interested) to a shareholder with at least 10% voting power, is deemed dividend up to accumulated profits; ₹8 lakh is capped at ₹6 lakh. In practice: repayment does not reverse it.', 'c1', T1, 'moderate', check=600000),
        Q('m3', 'Bonus shares issued to equity shareholders are:', ['Not dividend', 'Dividend to the extent of accumulated profits', 'Dividend at market value', 'Taxable as casual income'], 0,
          'Bonus shares to preference shareholders are deemed dividend to the extent of accumulated profits, but bonus shares to equity shareholders are not. Their cost later is nil for capital gains. In practice: track the allotment date for holding period.', 'c1', T1),
        Q('m4', 'Interim dividend is taxable in the year in which:', ['It is unconditionally made available to the shareholder', 'The final accounts are approved', 'The board first discusses it', 'It is encashed'], 0,
          'Interim dividend is deemed to be income of the tax year in which the company unconditionally makes it available to the member entitled; deemed dividend is income of the year it is declared, distributed or paid. In practice: check the credit date.', 'c1', T1),
        Q('m5', 'Winnings of ₹1,50,000 from a television quiz by a resident with no other income are taxed at:', ['30% on the whole amount', 'Nil, since income is below the exemption limit', '30% on the amount above the basic exemption', 'Slab rates'], 0,
          'Casual income is taxed at a flat 30% under section 194, and the unexhausted basic exemption limit cannot be adjusted against it; no expense or Chapter VIII deduction is allowed either. In practice: TDS is usually deducted by the payer.', 'c2', T2),
        Q('m6', 'Expenses of owning and maintaining race horses:', ['Are deductible against income from that activity', 'Are never deductible', 'Are deductible only against lottery winnings', 'Are capital expenditure'], 0,
          'The bar on expenses against casual income does not apply to the activity of owning and maintaining race horses; such expenses are allowed even without stake money, and the loss can be carried forward under section 115. In practice: keep the activity\'s accounts separate.', 'c2', T2, 'moderate'),
        Q('m7', 'Arun receives ₹30,000 from a friend and ₹25,000 from a neighbour in the same year. Amount taxable is:', ['₹55,000', '₹5,000', 'Nil', '₹30,000'], 0,
          'Sums of money received without consideration from non-relatives are aggregated for the year; once the total exceeds ₹50,000, the whole ₹55,000 is taxable, not merely the excess. In practice: the friend and neighbour are not relatives.', 'c3', T3, 'core', check=55000),
        Q('m8', 'Which of the following is a relative of an individual for section 92(2)(m)?', ['Spouse of his brother', 'His cousin', 'His friend\'s father', 'His business partner'], 0,
          'Relatives include the spouse of the individual\'s brother or sister, as the spouse of any listed relative counts. Cousins are not in the list. In practice: refer to the statutory list rather than common usage.', 'c3', T3),
        Q('m9', 'A car worth ₹8,00,000 gifted by a friend to an individual is:', ['Not taxable, as a car is not "property" for this provision', 'Taxable at ₹8,00,000', 'Taxable at ₹7,50,000', 'Taxable as capital gains'], 0,
          'The provision covers money and specified property — land or buildings, shares, jewellery, bullion, art and similar assets; a motor car is not included, so its receipt is not taxed. In practice: the list is exhaustive.', 'c3', T3, 'moderate'),
        Q('m10', 'House bought from a stranger for ₹50,00,000; stamp duty value ₹54,00,000. Taxable amount under section 92(2)(m) is:', ['Nil', '₹4,00,000', '₹3,50,000', '₹54,00,000'], 0,
          'For immovable property bought for inadequate consideration, the gap is taxable only if it exceeds the higher of ₹50,000 and 10% of consideration (₹5,00,000 here). A gap of ₹4,00,000 is within the tolerance. In practice: the seller faces a similar 110% test.', 'c3', T3, 'hard'),
        Q('m11', 'Gifts received by an individual on the occasion of his marriage from friends are:', ['Fully outside section 92(2)(m)', 'Taxable above ₹50,000', 'Taxable if in cash', 'Exempt only from relatives'], 0,
          'Receipts on the occasion of the marriage of the individual are excluded without any monetary limit, whether from relatives or others. Anniversary or birthday gifts get no such exclusion. In practice: keep a record linking gifts to the wedding.', 'c3', T3),
        Q('m12', 'An advance of ₹3,00,000 forfeited in August 2026 on a cancelled sale of land is:', ['Taxable as income from other sources in TY 2026-27', 'Reduced from cost of the land', 'Exempt', 'Taxable as capital gains in the year of eventual sale'], 0,
          'Advances forfeited when negotiations for a capital asset fail are taxed under section 92(2)(h) in the year of forfeiture; consequently they are not deducted from cost later. Only advances forfeited before 1 April 2014 reduce cost. In practice: report it in the forfeiture year.', 'c4', T4),
        Q('m13', 'Interest on enhanced compensation of ₹6,00,000 received in TY 2026-27 is taxable in that year at:', ['₹3,00,000', '₹6,00,000', 'Nil', '₹4,00,000'], 0,
          'Such interest is deemed income of the year of receipt irrespective of the accounting method, taxed under other sources with a 50% deduction and no other deduction. So ₹3,00,000 is taxable. In practice: years to which interest relates do not matter.', 'c4', T4, 'core', check=300000),
        Q('m14', 'Maturity proceeds of a non-ULIP life policy issued in 2024 with annual premium ₹6,00,000 (within 10% of sum assured) are:', ['Taxable as income from other sources', 'Exempt', 'Taxable as capital gains', 'Exempt up to ₹5,00,000'], 0,
          'For policies issued on or after 1 April 2023, exemption also requires aggregate premium not exceeding ₹5 lakh in any year of the term; ₹6 lakh breaches it, so the sum received is taxable here. Death claims remain exempt. In practice: insurers report such payouts.', 'c4', T4, 'hard'),
        Q('m15', 'Interest on government securities held as an investment by a salaried person is taxed under:', ['Income from other sources', 'Business income', 'Capital gains', 'Salaries'], 0,
          'Interest on securities is taxed under other sources unless the securities are held as stock-in-trade of a business, in which case it is business income. A salaried investor holds them as investments. In practice: banks treat such interest as business income.', 'c5', T5),
        Q('m16', 'Family pension of ₹1,80,000 a year under the optional regime gets a deduction of:', ['₹15,000', '₹60,000', '₹25,000', 'Nil'], 0,
          'The deduction is one-third of family pension or ₹15,000 (optional regime) or ₹25,000 (default regime), whichever is less; one-third here is ₹60,000, so the ₹15,000 ceiling applies. In practice: switching regime changes this deduction by ₹10,000.', 'c6', T6, 'core', check=15000),
        Q('m17', 'Which of the following is NOT deductible from income from other sources?', ['Interest on a loan taken to buy shares, set against dividend income', 'Commission paid to a bank for collecting bond interest', 'Depreciation on machinery let on hire', 'Current repairs to furniture let on hire'], 0,
          'Section 93 allows no deduction against dividends or mutual fund income, so interest on borrowings for shares is disallowed. Collection commission on interest and hire-related repairs and depreciation are expressly allowed. In practice: such interest gives no tax relief.', 'c6', T6, 'moderate'),
        Q('m18', 'A cash payment of ₹15,000 to one person in a day for expenses of earning hire income is:', ['Disallowed', 'Allowed', 'Allowed up to ₹10,000', 'Allowed at 70%'], 0,
          'Section 94 applies the same rule as for business income: payments exceeding ₹10,000 (₹35,000 to transporters) to a person in a day otherwise than by banking or online modes are disallowed in full. In practice: pay suppliers digitally.', 'c6', T6),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Cash aggregated > ₹50,000', 1.5, 'computation', 'aggregate|exceeds', nums=[money]),
           S('s2', 'Relative exclusion', 1, 'concept', 'relative'),
           S('s3', 'Painting within limit', 1, 'concept', '45,000|does not exceed'),
           S('s4', 'Plot tolerance test', 1.5, 'computation', '10%|tolerance', nums=[tol, land]),
           S('s5', 'Car not property', 1, 'concept', 'car')],
          ['Classify before computing.'], ['Taxing only the excess over ₹50,000.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Family pension deduction', 1.5, 'computation', '1/3|25,000', nums=[fpd]),
           S('s2', 'Interest on enhanced compensation 50%', 1.5, 'computation', '50%', nums=[ic]),
           S('s3', 'Dividend without deduction', 1, 'concept', 'dividend'),
           S('s4', 'Total', 1, 'computation', 'income from other sources', nums=[total]),
           S('s5', 'Lottery at 30%', 1, 'computation', '30%', nums=[lot])],
          ['Keep lottery separate.'], ['Setting basic exemption against lottery.'], ['Table.'], pad='table', checks=list(ck2)),
        W('q3', 3, i3['q'], i3['solution'],
          [S('s1', 'Allowable expenses', 1.5, 'concept', 'repairs', 'insurance'),
           S('s2', 'Depreciation', 0.5, 'computation', 'depreciation', nums=[dep]),
           S('s3', 'Net income', 1, 'computation', 'income', nums=[inc])],
          ['List each deduction.'], ['Claiming capital repairs.'], ['Table.'], pad='table', checks=list(ck3)),
        W('q4', 4, 'When is a loan by a company to a shareholder treated as deemed dividend, and what are the exceptions?',
          [ul(['The lender is a closely held company, i.e. one where the public are not substantially interested in it.', 'The borrower is a shareholder beneficially holding at least 10% of voting power, or a concern in which such shareholder has substantial interest (20%), or the payment is for his benefit.', 'It is dividend only to the extent of accumulated profits on the date of payment.']),
           p('Exceptions: loans in the ordinary course of a business in which money-lending is substantial; trade advances of a commercial nature; and dividends later declared and set off against a loan already taxed.')],
          [S('s1', 'Closely held company', 1, 'concept', 'not substantially interested|closely held'),
           S('s2', '10% voting power / 20% concern', 1, 'concept', '10%'),
           S('s3', 'Limited to accumulated profits', 1, 'concept', 'accumulated profit'),
           S('s4', 'Exceptions', 1, 'concept', 'ordinary course|trade advance')],
          ['Conditions, then cap, then exceptions.'], ['Taxing the full loan beyond accumulated profits.'], ['Bulleted list + paragraph.']),
    ]

    viva = [
        V('v1', 'What is the tax rate on lottery winnings?',
          'A flat 30% plus surcharge and cess, with no expenses, no Chapter VIII deductions and no basic exemption adjustment.',
          [P('p1', '30%', 6, '30'), P('p2', 'No deductions or exemption', 4, 'no expenses|no chapter|no basic')], 'c2'),
        V('v2', 'When is money received without consideration taxable?',
          'When the aggregate received from non-relatives in the year exceeds 50,000 rupees, the whole amount is taxable, unless an exclusion such as marriage or inheritance applies.',
          [P('p1', 'Aggregate > ₹50,000', 6, '50,000|50000'), P('p2', 'Exclusions', 4, 'relative|marriage|inheritance')], 'c3'),
        V('v3', 'How is interest on enhanced compensation taxed?',
          'In the year of receipt under other sources, after a deduction of 50%.',
          [P('p1', 'Year of receipt', 5, 'year of receipt|received'), P('p2', '50% deduction', 5, '50%')], 'c4'),
        V('v4', 'What is the family pension deduction?',
          'One-third of the pension or 25,000 rupees under the default regime (15,000 under the optional regime), whichever is lower.',
          [P('p1', 'One-third', 4, 'one-third|1/3'), P('p2', '₹25,000 / ₹15,000', 6, '25,000|15,000')], 'c6'),
        V('v5', 'Which incomes fall under this head only when not business income?',
          'Employee contributions received by an employer, hire of plant, machinery or furniture, inseparable letting of building with such assets, and interest on securities.',
          [P('p1', 'Hire of machinery', 4, 'machinery|plant'), P('p2', 'Interest on securities', 3, 'securities'), P('p3', 'Employee contributions', 3, 'contribution')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Kapoor family receipts', 'difficulty': 'moderate',
              'case': 'Rohit Kapoor, resident, in tax year 2026-27: received ₹2,00,000 from his wife\'s sister on his birthday; won ₹50,000 in a card game; bought listed shares from a friend at ₹1,00,000 when their market value was ₹1,70,000; received ₹80,000 as gifts from colleagues at his wedding; and his closely held company (he holds 30%) lent him ₹5,00,000 when accumulated profits were ₹7,00,000.',
              'mcqs': [
                  M('k1a', 'The ₹2,00,000 from his wife\'s sister is:', ['Not taxable — she is a relative', 'Taxable in full', 'Taxable above ₹50,000', 'Taxable as casual income'], 0,
                    'The brother or sister of the individual\'s spouse is a relative under the statutory definition, so money from her is excluded from section 92(2)(m) regardless of amount or occasion. In practice: keep proof of relationship.', 'core', topic=T3),
                  M('k1b', 'The share purchase results in taxable income of:', ['₹70,000', 'Nil', '₹20,000', '₹1,70,000'], 0,
                    'For movable property bought for inadequate consideration from a non-relative, the difference between aggregate FMV and price is taxed if it exceeds ₹50,000; the gap of ₹70,000 qualifies in full. The 10% tolerance applies only to immovable property. In practice: his cost for capital gains becomes ₹1,70,000.', 'moderate', check=70000, topic=T3),
                  M('k1c', 'The wedding gifts of ₹80,000 from colleagues are:', ['Not taxable', 'Taxable in full', 'Taxable at ₹30,000', 'Taxable as salary'], 0,
                    'Money received on the occasion of the individual\'s marriage is excluded from the provision without any limit and whoever the donor is. Colleagues\' gifts on other occasions would be counted. In practice: gifts on a later anniversary are taxable if they cross the limit.', 'core', topic=T3),
                  M('k1d', 'The loan from his company is deemed dividend of:', ['₹5,00,000', '₹7,00,000', 'Nil', '₹1,50,000'], 0,
                    'A loan by a closely held company to a shareholder with at least 10% voting power is deemed dividend to the extent of accumulated profits; since the ₹5,00,000 loan is within ₹7,00,000 of accumulated profits, the whole loan is dividend. In practice: it is taxed at normal rates.', 'moderate', check=500000, topic=T1),
              ]}]

    return unit(UID, 'p3', 'int-p3-a-ch03', 5, 'Income from Other Sources',
                ['Identify income chargeable under the residuary head, including dividends and deemed dividends.',
                 'Apply the flat rate on casual income and online game winnings.',
                 'Compute income from receipts without or for inadequate consideration.',
                 'Treat forfeited advances, interest on compensation and insurance receipts correctly.',
                 'Apply allowable and disallowed deductions.'],
                {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 35}, 'prereq': ['int-p3-a-ch03-u04'],
                 'exam_tip': 'Expect a section 92(2)(m) gift computation with relatives and tolerance limits, plus family pension and interest on enhanced compensation deductions.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Residuary head; dividends always here, taxed at normal rates.', 'Deemed dividend: closely held company loan to 10% shareholder, capped at accumulated profits.',
                             'Casual income: flat 30%, no deductions, no exemption-limit adjustment.', 'Gifts: money/movables > ₹50,000 aggregate; immovable gap > higher of ₹50,000 and 10%.',
                             'Exclusions: relatives, marriage, will/inheritance, contemplation of death, local authority.', 'Forfeited advance taxed in year of forfeiture.',
                             'Interest on enhanced compensation: year of receipt, 50% deduction.', 'Family pension: lower of 1/3 and ₹25,000 (default) / ₹15,000 (optional).'],
                 'remember': ['A car is not "property" for gift taxation.', 'No deduction against dividend income.'],
                 'traps': ['Whole amount taxed once ₹50,000 is crossed.', 'Bonus to equity holders is not dividend.']},
                [('Gift limit', '₹50,000 aggregate'), ('Immovable tolerance', 'Higher of ₹50,000 / 10%'), ('Casual income rate', '30%'), ('Deemed dividend shareholding', '10% voting power'),
                 ('Interest on compensation', '50% deduction'), ('Family pension', '1/3 or ₹25,000/₹15,000')],
                viva, cases,
                topics=['Structured Sectional Learning', 'Introduction', 'Method of Accounting', 'Incomes Chargeable under this Head',
                        'Applicable Rate of Tax in respect of Casual Income', 'Applicable Rate of Tax in respect of Winnings from Online Games',
                        'Deductions Allowable', 'Deductions not Allowable', 'Deemed Income Chargeable to Tax'])
