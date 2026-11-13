"""CA Intermediate · Paper 3A Income-tax Law · Chapter 3 Heads of Income · Unit 1 Salaries (Income-tax Act, 2025; tax year 2026-27).
Scope follows the ICAI study material; section numbers and limits are taken from it; explanations and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-a-ch03-u01'
T1 = 'When salary is taxed (s. 15) and employer–employee relation'
T2 = 'Salary, perquisites and profits in lieu (ss. 16–18)'
T3 = 'Allowances and their exemptions'
T4 = 'Valuing perquisites: accommodation and car'
T5 = 'Other perquisites and specified employees'
T6 = 'Provident funds, NPS and employer contributions'
T7 = 'Retirement benefits: gratuity, pension, leave salary, VRS'
T8 = 'Deductions u/s 19 and computing income under both regimes'


def build():
    ck = Checks()
    sal = ck.add('12*(50000+10000)', 'Salary for HRA = basic + DA (forming part) for 12 months')
    a = ck.add('12*20000', 'HRA received')
    b = ck.add('12*22000-0.10*720000', 'Rent paid − 10% of salary')
    c = ck.add('0.50*720000', '50% of salary (Pune is in the 8-city list)')
    ex = ck.add('min(240000,192000,360000)', 'HRA exempt = least')
    tx = ck.add('240000-192000', 'Taxable HRA (optional regime)')
    i1 = {'id': 'i1', 'title': 'HRA under the optional regime', 'difficulty': 'core', 'minutes': 6,
          'q': 'Neha works in Pune: basic ₹50,000 p.m., DA ₹10,000 p.m. (forms part of retirement benefits), HRA ₹20,000 p.m.; she pays rent of ₹22,000 p.m. for the whole year. Compute taxable HRA if she opts out of the default regime. What if she stays under the default regime?',
          'solution': [table(['Limit', 'Working', '₹'], [
              ['(i) HRA actually received', '20,000 × 12', inr(a)],
              ['(ii) Rent paid − 10% of salary', '2,64,000 − 10% of ' + inr(sal), inr(b)],
              ['(iii) 50% of salary (Pune)', '50% of ' + inr(sal), inr(c)],
              ['Exempt — least', '', inr(ex)],
              ['Taxable HRA', '2,40,000 − 1,92,000', inr(tx)]], title='HRA exemption (Rule 279)'),
              p('Under the default regime (s. 202(1)) no HRA exemption is available, so the full ₹2,40,000 is taxable.')],
          'checks': list(ck)}

    ck2 = Checks()
    g1 = ck2.add('round(15/26*(80000+20000)*25)', 'Covered by Gratuity Act: 15/26 × last salary (basic+DA) × 25 years (24 y 7 m rounds up)')
    gd1 = ck2.add('min(2400000, 2000000, 1442308)', 'Deduction = least of actual, ₹20 lakh, formula')
    g2 = ck2.add('0.5*100000*24', 'Not covered: ½ × average salary of last 10 months × completed years (24)')
    gd2 = ck2.add('min(2400000, 2000000, 1200000)', 'Deduction = least')
    i2 = {'id': 'i2', 'title': 'Gratuity deduction u/s 19(1)', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Ravi retires from a private company after 24 years 7 months and receives gratuity of ₹24,00,000. Last drawn basic ₹80,000 and DA ₹20,000 p.m. (DA forms part of retirement benefits; average of last 10 months is the same, ₹1,00,000). Compute the deduction if (a) he is covered by the Payment of Gratuity Act, 1972; (b) he is not covered; (c) he is a Central Government employee.',
          'solution': [table(['Case', 'Formula limit ₹', 'Deduction ₹', 'Taxable ₹'], [
              ['(a) Covered (Table Sl. No. 5)', inr(g1), inr(gd1), inr(2400000 - gd1)],
              ['(b) Not covered (Table Sl. No. 6)', inr(g2), inr(gd2), inr(2400000 - gd2)],
              ['(c) Government employee (Table Sl. No. 3)', '—', inr(2400000), 'Nil']], title='Answer'),
              note('Covered: 15 days\' salary per year, month = 26 days, part-year over 6 months counts as a full year. Not covered: half a month\'s average salary per completed year (fraction ignored). Statutory ceiling ₹20 lakh.')],
          'checks': list(ck2)}

    ck3 = Checks()
    rfa = ck3.add('0.10*(12*90000+120000)', 'RFA owned by employer in a city > 40 lakh population: 10% of salary')
    gross = ck3.add('1080000+120000+36000+120000', 'Gross salary = basic+DA + bonus + utilities + RFA')
    sd_new = ck3.add('min(1356000,75000)', 'Standard deduction (default regime)')
    net_new = ck3.add('1356000-75000', 'Income under "Salaries" — default regime')
    sd_old = ck3.add('min(1356000,50000)', 'Standard deduction (optional regime)')
    net_old = ck3.add('1356000-50000-2500', 'Optional regime: less standard deduction and professional tax ₹2,500')
    i3 = {'id': 'i3', 'title': 'Salary income under both regimes', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Arjun, manager in Mumbai: basic + DA (part of retirement benefits) ₹90,000 p.m.; bonus ₹1,20,000; rent-free flat owned by the employer (Mumbai population above 40 lakh); employer pays his gas and electricity bills of ₹36,000; he pays professional tax ₹2,500. Compute income under "Salaries" under (a) the default regime, (b) the optional regime.',
          'solution': [table(['Particulars', 'Default ₹', 'Optional ₹'], [
              ['Basic + DA', inr(1080000), inr(1080000)],
              ['Bonus', inr(120000), inr(120000)],
              ['Gas & electricity paid by employer (specified employee — salary > ₹4 lakh)', inr(36000), inr(36000)],
              ['Rent-free accommodation: 10% × (10,80,000 + 1,20,000)', inr(rfa), inr(rfa)],
              ['Gross salary', inr(gross), inr(gross)],
              ['Less: standard deduction', inr(sd_new), inr(sd_old)],
              ['Less: professional tax', '— (not allowed)', inr(2500)],
              ['Income under "Salaries"', inr(net_new), inr(net_old)]], title='Computation'),
              note('Salary for RFA includes basic, DA forming part of retirement benefits, bonus and other monetary payments, but excludes perquisites and exempt allowances.')],
          'checks': list(ck3)}

    rfa_t = table(['Who provides', 'Perquisite value (unfurnished)'], [
        ['Government (to its employees)', 'Licence fee fixed by Government − rent paid by employee'],
        ['Other employer — own accommodation, city population > 40 lakh (2011 census)', '10% of salary for the period − rent paid by employee'],
        ['Population > 15 lakh up to 40 lakh', '7.5% of salary − rent paid'],
        ['Other places', '5% of salary − rent paid'],
        ['Accommodation hired by employer', 'Lower of rent paid by employer and 10% of salary − rent paid by employee'],
        ['Furnished', 'Add 10% p.a. of cost of furniture (or actual hire charges) − amount recovered'],
    ], title='Accommodation perquisite')
    car = table(['Car owned/hired by', 'Expenses met by', 'Partly personal use — per month'], [
        ['Employer', 'Employer', 'Up to 1.6 litre or electric ₹5,000; above 1.6 litre ₹7,000; + ₹3,000 for chauffeur'],
        ['Employer', 'Employee (personal running)', 'Up to 1.6 litre or electric ₹2,000; above ₹3,000; + ₹3,000 for chauffeur'],
        ['Employee', 'Employer', 'Actual expenditure by employer − the value in row 1'],
        ['Employer car, wholly personal use', 'Employer', 'Actual running cost + 10% p.a. of car cost as wear and tear − recovery'],
        ['Wholly official use (with records and certificate)', '—', 'Nil'],
    ], title='Motor car perquisite (specified employees)')
    allow = table(['Allowance', 'Default regime', 'Optional regime'], [
        ['Dearness allowance, city compensatory, overtime, entertainment (non-Government), others', 'Fully taxable', 'Fully taxable'],
        ['House rent allowance', 'Fully taxable', 'Least of: HRA received; rent − 10% of salary; 50% of salary (Mumbai, Kolkata, Delhi, Chennai, Hyderabad, Pune, Ahmedabad, Bengaluru) or 40% elsewhere'],
        ['Children education allowance', 'Fully taxable', 'Exempt ₹3,000 p.m. per child, max 2 children'],
        ['Children hostel allowance', 'Fully taxable', 'Exempt ₹9,000 p.m. per child, max 2 children'],
        ['Travelling, transfer, daily, conveyance allowance', 'Exempt to the extent spent for the purpose', 'Same'],
        ['Helper, research, uniform allowance', 'Taxable', 'Exempt to the extent spent'],
        ['Transport allowance to blind / deaf and dumb / orthopaedically handicapped employee', 'Exempt ₹15,000 p.m. + DA (metro) or ₹8,000 + DA (other)', 'Same'],
        ['Field-area / high-altitude type allowances', 'Taxable', 'Exempt up to prescribed limits'],
        ['Leave travel concession', 'Taxable', 'Exempt for 2 journeys in a block of 4 calendar years (block 2026-29), within prescribed fares, for employee and family'],
    ], title='Allowances (Schedule III)')
    ret = table(['Benefit', 'Deduction u/s 19(1)'], [
        ['Gratuity — Government employees', 'Whole amount'],
        ['Gratuity — covered by Gratuity Act', 'Least of: actual; ₹20 lakh; 15/26 × last salary × years (part > 6 months = 1)'],
        ['Gratuity — not covered', 'Least of: actual; ₹20 lakh; ½ × average salary of last 10 months × completed years'],
        ['Commuted pension — Government and similar', 'Whole amount'],
        ['Commuted pension — others', 'With gratuity: ⅓ of full commuted value; without gratuity: ½ of full commuted value'],
        ['Uncommuted pension', 'No deduction — fully taxable'],
        ['Leave salary on retirement — non-Government', 'Least of: ₹25 lakh; actual; cash equivalent of leave (max 30 days per year of service); 10 months\' average salary'],
        ['Retrenchment compensation', 'Least of: actual; ₹5 lakh; 15 days\' average pay × years (part > 6 months = 1)'],
        ['Voluntary retirement compensation', 'Least of: actual; ₹5 lakh; 3 months\' salary × completed years; last salary × months of service left'],
        ['Standard deduction', '₹75,000 (default) / ₹50,000 (optional) or salary if less'],
        ['Professional tax paid', 'Allowed only in the optional regime'],
    ], title='Deductions from gross salary')

    concepts = [
        C('c1', T1, [
            'Under section 15, salary is caught in the year it falls due or the year it is paid, if that comes first. Advance salary is taxed when received and not again when due; arrears taxed on due basis are not taxed again on receipt. Arrears that were never due earlier (e.g. retrospective pay revision) are taxed on receipt. Relief u/s 157 spreads the extra tax burden of arrears or advance salary over the years concerned.',
            'A loan or advance against salary is not salary. Employer includes a former employer.',
            'An employer–employee relationship is essential: an artist employed by a film company earns salary from it, but fees from producers directly are professional income. A director\'s commission is salary only if he is an employee. A partner\'s salary from his firm is business income. MPs\' and MLAs\' remuneration is income from other sources.',
            'Part-time or multiple employments are all salary. Salary waived after accrual is still taxable (application of income); salary surrendered to the Government under the Voluntary Surrender of Salaries Act is exempt. Tax paid by the employer on salary is added to salary, but tax paid by the employer on non-monetary perquisites is exempt (Schedule III, Table Sl. No. 10).',
            'Non-citizens: embassy officials (reciprocity), employees of foreign enterprises not doing business in India staying ≤ 90 days, non-resident foreign-ship crew staying ≤ 90 days, and foreign-government trainees are exempt under Schedule IV — in both regimes.'],
          'Salary is caught at the earlier of two gates — when it is due or when it is paid — but only once.',
          'March salary paid on 2 April 2027 is income of tax year 2026-27.'),
        C('c2', T2, [
            'Salary (s. 16) includes wages, annuity or pension, gratuity, fees, commission, perquisites, profits in lieu of salary, advance salary, leave encashment, taxable portion of provident fund accretions and transfers, and contributions by the Central Government or any employer to the employee\'s pension account under s. 124.',
            'Perquisites (s. 17) are benefits in cash or kind in addition to salary — accommodation, car, services, free education, concessional loans, gifts, employer contributions to PF/NPS/superannuation above ₹7.5 lakh, etc. Reimbursement of official expenses is not a perquisite.',
            'Profits in lieu of salary (s. 18) include compensation on termination or modification of employment terms, payments from unrecognised funds (employer\'s share), keyman insurance sums received, and amounts received before joining or after leaving employment.',
            'Fees and commission (fixed or as % of turnover/profits) are fully taxable.'],
          'Salary is the cash; perquisites are the perks; profits in lieu are the "goodbye" or "hello" cheques.',
          'A joining bonus paid before the employee starts work is profit in lieu of salary.'),
        C('c3', T3, [
            'Allowances are fixed cash amounts. Their treatment is summarised in the table. Under the default regime only the travel/transfer/daily/conveyance allowances (to the extent spent) and transport allowance for disabled employees are exempt; others become fully taxable.',
            'HRA (Rule 279) is exempt only in the optional regime and only if the employee pays rent for a house he does not own. "Salary" for HRA = basic + DA forming part of retirement benefits + turnover-based commission, for the period of occupation.',
            'LTC (Schedule III, Table Sl. No. 8; Rule 278) covers travel within India on leave or after retirement for the employee and family (spouse, children; dependent parents, brothers, sisters), limited to actual expense and to air economy-class entitlement, first-class AC rail, deluxe bus, or ₹30/km where no public transport exists; two journeys in a block of four calendar years with one carry-forward; children limit of two born after 30 September 1998 (multiple births after the first child excepted).'],
          'Allowances are labelled envelopes — some envelopes are tax-free only if spent on what the label says.',
          'Salaried people often shift to the optional regime mainly to use HRA and LTC exemptions.',
          blocks=[allow]),
        C('c4', T4, [
            'Accommodation (table): value depends on who provides it and city population (2011 census) for employer-owned houses; leased houses take the lower of lease rent and 10% of salary. Furniture adds 10% p.a. of cost. "Salary" here includes all monetary payments (basic, DA forming part of retirement benefits, bonus, commission, taxable allowances) but excludes perquisites, exempt allowances, employer\'s PF contribution and lump-sum terminal benefits.',
            'Judges of the High Court and Supreme Court: rent-free official residence and LTC are tax-free (if they opt out of the default regime).',
            'Motor car (table): taxable only for specified employees, except where the employee\'s own car is used wholly for personal purposes and the employer reimburses running costs — then taxable for all employees.'],
          'Housing perquisites are a percentage of salary because the value of a company flat grows with seniority.',
          'A manager living in a company-owned flat in Mumbai is taxed on 10% of salary less any rent he pays.',
          blocks=[rfa_t, car]),
        C('c5', T5, [
            'Specified employee: a director, a person holding 20% or more of voting power, or one whose monetary salary exceeds ₹4 lakh. For them only: car (normal cases), sweeper/gardener/watchman/attendant (employer\'s cost − recovery), gas, electricity and water (amount paid to supplier or manufacturing cost if self-produced − recovery), free or concessional education for household members (cost, or cost in a similar nearby institution where employer-run — no perquisite up to ₹3,000 p.m. per child).',
            'For all employees: interest-free or concessional loans above ₹2 lakh (SBI rate on 1st day of the tax year on maximum monthly balance − interest paid); free food beyond ₹200 per meal during office hours or via paid vouchers; gifts or vouchers of ₹15,000 or more (whole value); use of movable assets; transfer of movable assets (cost − wear and tear − recovery); life insurance or annuity premium paid by employer; obligations of the employee paid by the employer (e.g. professional tax).',
            'Tax-free for all: training and refresher-course expenses, and the specified medical facilities as per the rules.'],
          'Some perks are taxed only for the bosses (specified employees); others — loans, gifts, food — for everyone.',
          'A ₹14,000 Diwali gift voucher is tax-free; a ₹16,000 one is fully taxable.'),
        C('c6', T6, [
            'Kinds of provident fund: recognised (RPF, including EPF), unrecognised (URPF), statutory (SPF) and public (PPF).',
            'Employer\'s aggregate contribution to RPF, NPS (s. 124(1)) and approved superannuation funds exceeding ₹7.5 lakh in a tax year is a taxable perquisite (s. 17(1)(h)), along with income accrued on that excess.',
            'Interest credited to RPF above 9.5% p.a. is taxable as salary. Interest on an employee\'s own contribution above ₹2.5 lakh a year (₹5 lakh where the employer does not contribute), made on or after 1 April 2021, is taxable (Rule 277, separate taxable account).',
            'Withdrawal from RPF is exempt if 5 years\' continuous service, or earlier exit due to ill-health, closure or reasons beyond control, or transfer to a new employer\'s RPF or to NPS. From URPF: employer\'s share and interest are salary; interest on own contribution is other sources; own contribution not taxable.',
            'Employer contributions to NPS are included in salary but deductible u/s 124(1)/(2) up to 14% of salary (Government, and any employer under the default regime) or 10% (other employers, optional regime) — in both regimes. Employee\'s own contribution deductions (ss. 123, 124(3)/(4)) need the optional regime.'],
          'Retirement funds are tax-friendly up to a point — the law caps very large employer contributions and very large employee savings.',
          'A CEO whose employer puts ₹8 lakh into NPS pays tax on ₹50,000 as a perquisite beyond the ₹7.5 lakh cap.'),
        C('c7', T7, [
            'Under the 2025 Act, retirement benefits are included in gross salary and relief is given as deductions u/s 19(1) (table).',
            'Gratuity received during service is fully taxable. "Salary" for gratuity: basic + DA (covered employees); basic + DA forming part of retirement benefits + turnover-based commission (not covered; average of 10 months before the retirement month). Gratuity received by widow, children or dependants on death is exempt to the same extent (Schedule III, Table Sl. No. 38).',
            'Pension: uncommuted pension is fully taxable; commuted pension is deductible fully for Government-type employees, and for others up to one-third (if gratuity received) or one-half (if not) of the full commuted value. Gallantry-award pensions and family pensions, and disability pensions of invalided armed-forces personnel, are exempt.',
            'Leave encashment during service is fully taxable; on retirement, fully deductible for Government employees and limited for others.',
            'Retrenchment and voluntary retirement compensation have separate ₹5 lakh-capped deductions.'],
          'Retirement benefits enter gross salary first and then leave through the deduction door — fully for Government employees, partly for others.',
          'A private employee with ₹24 lakh gratuity can deduct at most ₹20 lakh.',
          blocks=[ret]),
        C('c8', T8, [
            'Gross salary less deductions u/s 19(1) gives income under "Salaries": standard deduction ₹75,000 (default) or ₹50,000 (optional); professional tax (optional regime only); and the retirement-benefit deductions (both regimes).',
            'Proforma: basic, fees, commission, bonus, allowances (net of exemptions), taxable PF interest and employer NPS contribution, perquisites, LTC (net), gratuity, pension, retrenchment and VRS compensation, leave encashment → gross salary → deductions → net.',
            'To move from the default to the optional regime figure: add back the extra ₹25,000 standard deduction, then subtract professional tax, HRA, education/hostel allowance, helper/research/uniform, field-area allowances and LTC exemptions.'],
          'The same pay slip gives two different salary incomes depending on which regime\'s lens you use.',
          'Payroll software computes TDS under the default regime unless the employee declares the optional regime.',
          blocks=[]),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Year-end salary TDS check', 'role': 'Payroll executive',
         'situation': 'An employee asks whether to declare the optional regime to the employer.',
         'steps': ['Compute salary under both regimes (HRA, LTC, professional tax, standard deduction).', 'Add other income and Chapter VIII deductions available only in the optional regime.', 'Compare tax and advise; remind that salaried employees can switch while filing the return.'],
         'takeaway': 'Regime choice is a computation, not a guess.'},
        {'id': 'j2', 'title': 'Retirement settlement', 'role': 'Tax consultant',
         'situation': 'A private-sector employee receives gratuity, leave encashment and commutes one-third of pension.',
         'steps': ['Include each in gross salary.', 'Apply 19(1) deductions: gratuity (Gratuity Act formula, ₹20 lakh), leave (₹25 lakh limit), commuted pension (⅓ of full value as gratuity received).', 'Note uncommuted pension remains fully taxable.'],
         'takeaway': 'Each terminal benefit has its own limit — compute them separately.'},
    ]

    mcqs = [
        Q('m1', 'Salary is chargeable to tax on:', ['Due or receipt basis, whichever is earlier', 'Receipt basis only', 'Due basis only', 'Accrual basis at year-end'], 0,
          'Section 15 taxes salary in the year it becomes due or is paid, if payment comes first, and never twice. Advance salary is taxed on receipt; March salary paid in April is taxed on due basis. In practice: payroll years follow the tax year.', 'c1', T1),
        Q('m2', 'Remuneration received by a Member of Parliament is taxable as:', ['Income from other sources', 'Salaries', 'Business income', 'Exempt income'], 0,
          'MPs and MLAs are not Government employees, so there is no employer–employee relationship; their remuneration is income from other sources. Constituency and daily allowances have their own treatment. In practice: such income is shown under other sources in the return.', 'c1', T1),
        Q('m3', 'Salary drawn by a partner from his firm is taxable as:', ['Profits and gains of business or profession', 'Salaries', 'Income from other sources', 'Exempt'], 0,
          'A partner is not an employee of his firm; his salary, bonus or commission from the firm is an appropriation of profit taxed as business income, as section 15 expressly provides. In practice: partners report it under business income.', 'c1', T1),
        Q('m4', 'Under the default regime, house rent allowance is:', ['Fully taxable', 'Exempt up to 50% of salary', 'Exempt up to rent paid', 'Fully exempt'], 0,
          'Section 202(2) denies the HRA exemption in the default regime, so the whole allowance is taxable; the Rule 279 exemption is available only to those who opt out. In practice: tenants with high rent often prefer the optional regime.', 'c3', T3),
        Q('m5', 'HRA exemption at 50% of salary applies to accommodation in:', ['Mumbai, Kolkata, Delhi, Chennai, Hyderabad, Pune, Ahmedabad and Bengaluru', 'Only Mumbai, Kolkata, Delhi and Chennai', 'All State capitals', 'Any city with population over 25 lakh'], 0,
          'Rule 279 lists eight cities for the 50% limit — Mumbai, Kolkata, Delhi, Chennai, Hyderabad, Pune, Ahmedabad and Bengaluru; elsewhere 40% applies. In practice: check the city of residence, not of office.', 'c3', T3, 'moderate'),
        Q('m6', 'Children education allowance under the optional regime is exempt up to:', ['₹3,000 per month per child, for up to two children', '₹100 per month per child', '₹9,000 per month per child', 'Fully exempt'], 0,
          'Children education allowance is exempt up to ₹3,000 per month per child for a maximum of two children; hostel allowance up to ₹9,000 per month per child. Both are fully taxable under the default regime. In practice: payroll restricts the exempt part automatically.', 'c3', T3),
        Q('m7', 'LTC exemption under the optional regime is available for:', ['Two journeys in a block of four calendar years', 'One journey every year', 'Any number of journeys in India', 'Journeys abroad too'], 0,
          'Rule 278 allows two journeys in a block of four calendar years (current block 2026-29), with one unavailed journey carried forward into the first year of the next block, for travel within India only. In practice: keep tickets as proof.', 'c3', T3),
        Q('m8', 'Rent-free accommodation owned by the employer in a city with population 30 lakh (2011 census) is valued at:', ['7.5% of salary', '10% of salary', '5% of salary', '15% of salary'], 0,
          'For employer-owned accommodation, the rate is 10% above 40 lakh population, 7.5% above 15 lakh up to 40 lakh, and 5% elsewhere, less rent paid by the employee. In practice: always use the 2011 census population of the city, not current estimates.', 'c4', T4, 'moderate'),
        Q('m9', 'A company car above 1.6 litres, used partly for personal purposes with all expenses met by the employer and a chauffeur provided, has a monthly perquisite value of:', ['₹10,000', '₹7,000', '₹5,000', '₹3,000'], 0,
          'The value is ₹7,000 per month for cars above 1.6 litres plus ₹3,000 for the chauffeur, i.e. ₹10,000; smaller or electric cars take ₹5,000. Only specified employees are taxed on it. In practice: logbooks support the official-use claim.', 'c4', T4, 'moderate', check=10000),
        Q('m10', 'Which employee is NOT a "specified employee"?', ['A non-director employee with monetary salary of ₹3.5 lakh and no shareholding', 'A director of the company', 'An employee holding 20% voting power', 'An employee with monetary salary of ₹6 lakh'], 0,
          'Specified employees are directors, holders of 20% or more voting power, and those whose monetary salary exceeds ₹4 lakh. An employee earning ₹3.5 lakh with no such status is not specified. In practice: most managers today are specified employees.', 'c5', T5),
        Q('m11', 'A gift voucher given by an employer is a taxable perquisite if its value is:', ['₹15,000 or more', 'More than ₹5,000', 'Any amount', 'More than ₹50,000'], 0,
          'Gifts or vouchers below ₹15,000 are not a perquisite; at ₹15,000 or more, the whole value is taxable for all employees. In practice: festival vouchers are often kept below this limit to avoid tax for staff.', 'c5', T5, 'core', check=15000),
        Q('m12', 'An interest-free loan from an employer is a taxable perquisite where the loan exceeds:', ['₹2,00,000', '₹20,000', '₹50,000', '₹10,00,000'], 0,
          'Loans above ₹2 lakh are valued at the SBI rate on the first day of the tax year on the maximum monthly outstanding balance, less interest paid, for all employees. Smaller loans are ignored altogether. In practice: housing loans by employers often cross this limit.', 'c5', T5, 'core', check=200000),
        Q('m13', 'Employer\'s aggregate contribution to RPF, NPS and superannuation fund is a taxable perquisite to the extent it exceeds:', ['₹7,50,000 in a tax year', '₹1,50,000', '12% of salary', '₹2,50,000'], 0,
          'Section 17(1)(h) treats the excess over ₹7.5 lakh of combined employer contributions as a perquisite, with accretions on that excess also taxable. Employee contributions have separate interest thresholds. In practice: high earners\' CTC structures watch this cap.', 'c6', T6, 'core', check=750000),
        Q('m14', 'Interest credited to a recognised provident fund is taxable to the extent it exceeds:', ['9.5% per annum', '8.25% per annum', '12% per annum', 'Nil — always exempt'], 0,
          'Interest credited to RPF above 9.5% p.a. is taxable as salary; in addition, interest on employee contributions above the ₹2.5 lakh/₹5 lakh yearly thresholds is taxable. In practice: EPF rates are currently below 9.5%, so this rarely bites ordinary employees.', 'c6', T6),
        Q('m15', 'Deduction u/s 124(1) for employer\'s NPS contribution, for a private employer under the default regime, is up to:', ['14% of salary', '10% of salary', '12% of salary', 'No deduction'], 0,
          'Employer NPS contribution is deductible up to 14% of salary for Government employers, and for any employer when the employee is in the default regime; 10% for other employers under the optional regime. In practice: NPS is popular in default-regime pay structures.', 'c6', T6, 'hard'),
        Q('m16', 'The maximum deduction for gratuity of a non-Government employee is:', ['₹20,00,000', '₹10,00,000', '₹25,00,000', '₹5,00,000'], 0,
          'Gratuity deductions for non-Government employees are capped at ₹20 lakh (along with actual amount and formula); Government employees deduct the whole amount. ₹25 lakh is the leave-salary cap. In practice: large gratuities above ₹20 lakh are partly taxable.', 'c7', T7, 'core', check=2000000),
        Q('m17', 'A private employee who received gratuity commutes part of pension. The deduction for commuted pension is:', ['One-third of the full commuted value of pension', 'One-half of the full commuted value', 'The entire commuted amount', 'Nil'], 0,
          'For non-Government employees, the deduction is one-third of the full commuted value if gratuity is also received, and one-half if not; Government employees deduct it fully. Uncommuted pension is fully taxable. In practice: compute full value = commuted amount ÷ commutation %.', 'c7', T7),
        Q('m18', 'Leave salary of a non-Government employee on retirement is deductible up to a maximum of:', ['₹25,00,000', '₹3,00,000', '₹20,00,000', '₹5,00,000'], 0,
          'Leave encashment on retirement is deductible to the least of ₹25 lakh, amount received, cash value of leave (30 days per year max) and ten months\' average salary. Encashment during service is fully taxable. In practice: compute all four limits.', 'c7', T7, 'core', check=2500000),
        Q('m19', 'Standard deduction under the default regime is:', ['₹75,000 or salary, whichever is less', '₹50,000', '₹1,00,000', 'Not allowed'], 0,
          'Section 19(1) allows standard deduction of ₹75,000 under the default regime and ₹50,000 under the optional regime, limited to salary. Professional tax is deductible only in the optional regime. In practice: pensioners also get standard deduction.', 'c8', T8, 'core'),
        Q('m20', 'Professional tax paid by a salaried employee is deductible:', ['Only if he opts out of the default regime', 'Under both regimes', 'Only under the default regime', 'Never'], 0,
          'Section 202(2) disallows the professional tax deduction under the default regime; it is allowed under the optional regime (Table Sl. No. 1). Where the employer pays it, it is first added as a perquisite. In practice: the amount is small but should not be missed.', 'c8', T8),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Three limits', 2, 'computation', 'least|rent|50%', nums=[a, b, c]),
           S('s2', 'Exempt and taxable HRA', 1, 'computation', 'exempt|taxable', nums=[ex, tx]),
           S('s3', 'Default regime — fully taxable', 1, 'concept', 'default', 'fully taxable|full|2,40,000')],
          ['Define salary for HRA first.'], ['Using 40% for Pune.'], ['Table of limits.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Covered — 15/26 formula with 25 years', 2.5, 'computation', '15/26|covered', nums=[g1, gd1]),
           S('s2', 'Not covered — half-month × 24 years', 2.5, 'computation', 'not covered|half', nums=[g2, gd2]),
           S('s3', 'Government — full deduction', 1, 'computation', 'government', 'full|entire|24,00,000')],
          ['Show the year rounding rule clearly.'], ['Rounding 24 y 7 m to 24 for covered employees.'], ['Three-row table.'], pad='table', checks=list(ck2)),
        W('q3', 6, i3['q'], i3['solution'],
          [S('s1', 'RFA at 10% of salary', 2, 'computation', 'accommodation|rent-free|10%', nums=[rfa]),
           S('s2', 'Gross salary', 1.5, 'computation', 'gross', nums=[gross]),
           S('s3', 'Default regime net', 1.25, 'computation', 'default|75,000', nums=[net_new]),
           S('s4', 'Optional regime net with professional tax', 1.25, 'computation', 'optional|professional', nums=[net_old])],
          ['Two columns side by side.'], ['Including perquisites in salary for RFA.', 'Deducting professional tax under the default regime.'], ['Columnar table.'], pad='table',
          checks=list(ck3)),
    ]

    viva = [
        V('v1', 'How is HRA exemption computed?',
          'It is the least of the HRA received, rent paid less 10% of salary, and 50% of salary in the eight listed cities or forty percent elsewhere, and is available only under the optional regime.',
          [P('p1', 'HRA received', 2, 'received'), P('p2', 'Rent − 10% of salary', 3, 'rent paid less|rent minus|excess of rent'), P('p3', '50% / 40% of salary', 3, 'fifty|50%|forty|40%'), P('p4', 'Optional regime only', 2, 'optional|opt')], 'c3'),
        V('v2', 'Who is a specified employee?',
          'A director of the company, an employee holding twenty percent or more of the voting power, or an employee whose monetary salary exceeds four lakh rupees.',
          [P('p1', 'Director', 3, 'director'), P('p2', '20% voting power', 3, 'twenty|20%|20 percent'), P('p3', 'Monetary salary > ₹4 lakh', 4, 'four lakh|4 lakh')], 'c5'),
        V('v3', 'What is the deduction for commuted pension of a private employee?',
          'One third of the full commuted value of pension if gratuity is also received, and one half if no gratuity is received.',
          [P('p1', 'One-third with gratuity', 5, 'one third|1/3|one-third'), P('p2', 'One-half without gratuity', 5, 'one half|half|1/2')], 'c7'),
        V('v4', 'What are the limits for voluntary retirement compensation?',
          'Least of compensation received, five lakh rupees, three months salary for each completed year of service, and last salary multiplied by the months of service left.',
          [P('p1', '₹5 lakh', 3, 'five lakh|5 lakh'), P('p2', '3 months × years', 4, 'three months|3 months'), P('p3', 'Salary × months left', 3, 'months left|remaining|left')], 'c7'),
        V('v5', 'What standard deduction is allowed under each regime?',
          '₹75,000 under the default regime and ₹50,000 under the optional regime, but never more than the salary itself.',
          [P('p1', '₹75,000 default', 5, '75,000|75000'), P('p2', '₹50,000 optional', 5, '50,000|50000')], 'c8'),
    ]

    cases = [{'id': 'k1', 'title': 'Pay package at Orbit Systems', 'difficulty': 'moderate',
              'case': 'Priya (monetary salary ₹18 lakh) gets: a company-leased flat in Chennai (lease ₹45,000 p.m.); a 1.5-litre company car used partly for personal purposes, all expenses by the company, no chauffeur; an interest-free loan of ₹1,50,000; Diwali vouchers of ₹12,000; and the company contributes ₹8,20,000 in aggregate to her PF and NPS. She pays tax under the default regime.',
              'mcqs': [
                  M('k1a', 'The flat (leased by the employer) is valued at:', ['Lower of lease rent and 10% of salary, less rent paid by her', '7.5% of salary', 'Actual lease rent always', 'Nil, as it is leased'], 0,
                    'For accommodation taken on lease by the employer, the perquisite is the lower of the lease rent and 10% of salary, minus any rent recovered. Here 10% of ₹18 lakh (₹1.8 lakh) is lower than ₹5.4 lakh lease rent. In practice: city population matters only for employer-owned houses.', 'moderate', topic=T4),
                  M('k1b', 'The company car perquisite per month is:', ['₹5,000', '₹7,000', '₹2,000', 'Nil'], 0,
                    'A car of up to 1.6 litres with expenses met by the employer and used partly for personal purposes is valued at ₹5,000 per month; ₹3,000 is added only if a chauffeur is provided. She is a specified employee. In practice: engine capacity sets the slab.', 'core', check=5000, topic=T4),
                  M('k1c', 'The interest-free loan of ₹1,50,000 and vouchers of ₹12,000 are:', ['Both not taxable', 'Both taxable', 'Only the loan is taxable', 'Only the vouchers are taxable'], 0,
                    'Loans up to ₹2 lakh and gifts or vouchers below ₹15,000 are not perquisites, so neither is taxed. Crossing either threshold makes them taxable perquisites. In practice: companies design benefits around these limits.', 'core', topic=T5),
                  M('k1d', 'Of the employer\'s ₹8,20,000 contribution, the amount taxable as perquisite (before any s. 124 deduction effects) is:', ['₹70,000 plus accretions on it', 'Nil', '₹8,20,000', '₹1,50,000'], 0,
                    'Employer contributions to RPF, NPS and superannuation above ₹7.5 lakh in a year are a perquisite; the excess here is ₹70,000, and income accrued on that excess is also taxable. In practice: CTC planning keeps contributions under ₹7.5 lakh.', 'moderate', check=70000, topic=T6),
              ]}]

    return unit(UID, 'p3', 'int-p3-a-ch03', 1, 'Salaries',
                ['Explain the basis of charge and the meaning of salary, perquisites and profits in lieu of salary.',
                 'Determine exempt and taxable allowances under both regimes, including HRA and LTC.',
                 'Value accommodation, car and other perquisites; identify specified employees.',
                 'Apply provisions on provident funds, NPS and employer contributions.',
                 'Compute deductions for retirement benefits and income under "Salaries" in both regimes.'],
                {'difficulty': 'core', 'minutes': {'learn': 70, 'practice': 50}, 'prereq': ['int-p3-a-ch02-u01'],
                 'exam_tip': 'A full salary computation under both regimes is almost certain; know HRA, RFA, car, gratuity, commuted pension, leave encashment limits and the ₹75,000/₹50,000 standard deduction.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Salary taxed when due or when paid, if earlier (s. 15).', 'Employer–employee relationship essential; partners and MPs excluded.',
                             'Default regime: HRA, LTC, CEA, professional tax not allowed; standard deduction ₹75,000.', 'HRA: least of HRA, rent − 10%, 50% (8 cities)/40% of salary.',
                             'RFA: 10% / 7.5% / 5% of salary by population; leased: lower of rent and 10%.', 'Specified employee: director, 20% voter or salary > ₹4 L.',
                             'Employer PF/NPS/superannuation > ₹7.5 L taxable; RPF interest > 9.5% taxable.', 'Gratuity cap ₹20 L; leave ₹25 L; VRS and retrenchment ₹5 L.'],
                 'remember': ['Covered gratuity: 15/26, part-year > 6 months counts.', 'Commuted pension: ⅓ with gratuity, ½ without.'],
                 'traps': ['Gratuity during service is fully taxable.', 'Car rules apply mostly to specified employees only.']},
                [('Standard deduction', '₹75,000 default · ₹50,000 optional'), ('HRA cities at 50%', 'Mumbai, Kolkata, Delhi, Chennai, Hyderabad, Pune, Ahmedabad, Bengaluru'),
                 ('Gratuity cap', '₹20 lakh'), ('Leave encashment cap', '₹25 lakh'), ('Employer contribution cap', '₹7.5 lakh'), ('Gift voucher limit', 'Below ₹15,000')],
                viva, cases,
                topics=['Introduction', 'Basis of Charge', 'Salary, Perquisite and Profits in lieu of Salary', 'Deductions from Salary', 'Relief under Section 157'])
