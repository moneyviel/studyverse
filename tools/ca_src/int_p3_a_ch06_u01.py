"""CA Intermediate · Paper 3A Income-tax Law · Chapter 6 Deductions from Gross Total Income (Income-tax Act, 2025; tax year 2026-27).
Scope follows the ICAI study material; section numbers are taken from it; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-a-ch06-u01'
T1 = 'General rules for Chapter VIII deductions (s. 122) and the default regime'
T2 = 'Investments and savings (s. 123) and pension schemes (ss. 124-125)'
T3 = 'Health: insurance, disability of dependants, specified diseases (ss. 126-128)'
T4 = 'Interest on education, house and electric vehicle loans (ss. 129-132)'
T5 = 'Donations and political contributions (ss. 133, 135-137)'
T6 = 'Rent paid without HRA (s. 134)'
T7 = 'Income-based deductions: royalty, deposit interest, disability (ss. 151-154)'


def build():
    # i1 — section 123 cap and section 124(3)
    ck = Checks()
    lic = ck.add('min(36000, 300000*10/100)', 'LIC premium allowed (10% of sum assured)')
    tui = ck.add('30000+25000', 'Tuition fees for the two eligible children')
    s123 = ck.add('min(30000+60000+55000+40000, 150000)', 'Section 123 deduction (cap ₹1,50,000)')
    s124 = ck.add('min(70000, 50000)', 'Own NPS contribution under section 124(3)')
    tot = ck.add('150000+50000', 'Total deduction')
    i1 = {'id': 'i1', 'title': 'Too many savings for one cap', 'difficulty': 'core', 'minutes': 8,
          'q': 'Mr. Arjun (salary including DA ₹8,00,000; opts out of the default regime) paid in tax year 2026-27: LIC premium ₹36,000 on his own policy issued in 2018 (sum assured ₹3,00,000); PPF ₹60,000; tuition fees for three children ₹30,000, ₹25,000 and ₹20,000; housing loan principal ₹40,000; and his own NPS contribution ₹70,000. Compute the maximum deduction under sections 123 and 124(3).',
          'solution': [table(['Item', 'Working', '₹'], [
              ['LIC premium', '10% of ₹3,00,000 (policy after 31.3.2013)', inr(lic)],
              ['PPF', '', inr(60000)],
              ['Tuition fees', 'Only two children; choose the larger two', inr(tui)],
              ['Housing loan principal', '', inr(40000)],
              ['Section 123 (excluding NPS)', '1,85,000 restricted to', inr(s123)],
              ['Own NPS under section 124(3)', '₹70,000 restricted to', inr(s124)],
              ['Total deduction', '', inr(tot)]], title='Sections 123 and 124(3)'),
              p('Because the other items already fill the ₹1,50,000 cap, the NPS contribution is better claimed under section 124(3). The same rupee cannot be claimed under both sections; the ₹20,000 NPS balance gives no further benefit this year.')],
          'checks': list(ck)}

    # i2 — section 126
    ck2 = Checks()
    own = ck2.add('min(22000+min(6000,5000), 25000)', 'Self and family: premium + check-up, cap ₹25,000')
    par = ck2.add('min(30000+28000, 50000)', 'Parents (senior citizens): premium + medical expenditure, cap ₹50,000')
    t2 = ck2.add('25000+50000', 'Total under section 126')
    i2 = {'id': 'i2', 'title': 'Health cover for two generations', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Ms. Leena, aged 40, opts out of the default regime. In tax year 2026-27 she paid by card a health premium of ₹22,000 for herself and her husband and spent ₹6,000 in cash on their preventive health check-ups. She paid a health premium of ₹30,000 for her mother (68) and spent ₹28,000 on medical treatment of her father (72), who has no health insurance. Compute the deduction under section 126.',
          'solution': [table(['Group', 'Working', '₹'], [
              ['Self and spouse', 'Premium 22,000 + check-up 5,000 (₹5,000 sub-limit) = 27,000, capped at 25,000', inr(own)],
              ['Parents', 'Mother\'s premium 30,000 + father\'s medical expenditure 28,000 = 58,000, capped at 50,000', inr(par)],
              ['Total', '', inr(t2)]], title='Section 126'),
              note('Cash is acceptable only for preventive check-ups. Medical expenditure counts only for a senior citizen with no health insurance.')],
          'checks': list(ck2)}

    # i3 — section 133 with qualifying limit
    ck3 = Checks()
    adj = ck3.add('1200000-100000-50000-150000-25000', 'Adjusted gross total income')
    lim = ck3.add('875000*10/100', '10% of adjusted GTI')
    q = ck3.add('min(15000+140000, 87500)', 'Qualifying amount (lower of limit and Category II + IV donations)')
    lim_part = ck3.add('15000+(87500-15000)*50/100', 'Deduction within the limit: 100% donation first, then 50% of the balance')
    free = ck3.add('30000+20000*50/100', 'Donations without limit: PMNRF 100% + PM Drought Relief Fund 50%')
    d133 = ck3.add('51250+40000', 'Total deduction under section 133')
    i3 = {'id': 'i3', 'title': 'Donations and the 10% ceiling', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Mr. Ravi (optional regime) has GTI of ₹12,00,000, which includes long-term capital gain on land of ₹1,00,000 (s. 197) and short-term capital gain on STT-paid shares of ₹50,000 (s. 196). His deductions under sections 123 and 126 are ₹1,50,000 and ₹25,000. By cheque he donated: Prime Minister\'s National Relief Fund ₹30,000; Prime Minister\'s Drought Relief Fund ₹20,000; an approved charitable trust ₹1,40,000; Government for promoting family planning ₹15,000. He also gave ₹5,000 in cash to another approved trust. Compute the deduction under section 133.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Adjusted GTI', 'GTI less s. 197 gain, s. 196 gain and deductions under ss. 123 and 126', inr(adj)],
              ['10% of adjusted GTI', '', inr(lim)],
              ['Category II + IV donations', 'Family planning 15,000 + trust 1,40,000 = 1,55,000', inr(q)],
              ['Deduction within the limit', '15,000 at 100% + (87,500 − 15,000) × 50%', inr(lim_part)],
              ['Donations without limit', 'PMNRF 30,000 + 50% of 20,000', inr(free)],
              ['Cash donation of ₹5,000', 'Above ₹2,000 in cash — not allowed', 'Nil'],
              ['Deduction under section 133', '', inr(d133)]], title='Section 133')],
          'checks': list(ck3)}

    over = table(['Section', 'For', 'Limit (optional regime)'], [
        ['123', 'LIC, PPF, tuition fees, housing loan principal, own NPS etc.', '₹1,50,000'],
        ['124(1)/(2)', 'Employer\'s NPS contribution', '14% of salary (Govt); 10% (others; 14% in default regime)'],
        ['124(3)/(4)', 'Own NPS and NPS Vatsalya', '₹50,000 in aggregate'],
        ['126', 'Health insurance, check-up, medical expenditure', '₹25,000 / ₹50,000 per group'],
        ['127 / 154', 'Disabled dependant / own disability', '₹75,000; ₹1,25,000 if severe'],
        ['128', 'Specified diseases', '₹40,000; ₹1,00,000 for senior citizen'],
        ['129', 'Education loan interest', 'No ceiling; 8 tax years'],
        ['134', 'Rent without HRA', 'Least of three; ₹5,000 p.m.'],
        ['153', 'Deposit interest', '₹10,000; ₹50,000 for senior citizen']], title='Main deductions')

    concepts = [
        C('c1', T1, [
            'Exempt incomes under section 11 and the Schedules never enter gross total income. Chapter VIII deductions work differently: the income is first included in GTI, and the deduction is then subtracted to reach total income.',
            'Section 122(2): total deductions cannot exceed GTI, so total income can be nil but never negative, and no "loss" arises from deductions. Deductions are not allowed against short-term gains u/s 196, long-term gains u/s 197 and 198, or lottery-type winnings in GTI.',
            'Under the default regime of section 202(1), only these are allowed: employer\'s NPS contribution (s. 124(1)/(2)), Central Government contribution to the Agniveer Corpus Fund (s. 125(2)) and additional employee cost (s. 146). All other deductions need the taxpayer to opt out.',
            'Part C deductions for certain incomes (such as section 146) require the return to be filed by the due date u/s 263(1) with the claim made in it.'],
          'An exemption keeps income out of the total; a deduction lets it in and then takes some back.',
          'With GTI of ₹3,00,000 and eligible deductions of ₹3,40,000, only ₹3,00,000 is allowed.',
          blocks=[over]),
        C('c2', T2, [
            'Section 123 (individual or HUF, optional regime): up to ₹1,50,000 for items in Schedule XV — life insurance premium (self, spouse, any child; any member for HUF), PPF, recognised or statutory PF, NSC VIII, ULIP, Sukanya Samriddhi deposits for a girl child, 5-year bank or post office term deposits, Senior Citizens Savings Scheme, tuition fees for full-time education in India of up to two children, and repayment of a housing loan principal with stamp duty and registration charges.',
            'Life insurance premium counts only up to a percentage of the actual capital sum assured: 20% for policies issued up to 31.3.2012, 10% for 2012-13 policies and later ones, and 15% for policies from 1.4.2013 on the life of a person with disability (s. 154) or a specified disease (s. 128).',
            'Own NPS contribution is part of section 123 up to 10% of salary (employees) or 20% of GTI (others). Section 124(3) gives a further ₹50,000 for own NPS (together with NPS Vatsalya for a minor under s. 124(4)); the same amount cannot be claimed under both.',
            'Employer\'s NPS contribution (s. 124(1)/(2)) is deductible in both regimes. Early surrender of policies, transfer of the house within 5 years or early withdrawals can reverse the benefit by taxing it later.'],
          'Section 123 is one bucket of ₹1,50,000; NPS has a small extra bucket beside it.',
          'Tuition fees for three children: only two qualify, and development fees or donations never do.'),
        C('c3', T3, [
            'Section 126 (individual or HUF, optional regime): for self, spouse and dependent children — health premium (non-cash), CGHS contribution and preventive check-ups up to ₹25,000; ₹50,000 if any of them is a senior citizen. A separate limit of ₹25,000 (₹50,000 if senior citizen) applies for parents.',
            'Preventive check-ups are capped at ₹5,000 in total and may be paid in cash. Medical expenditure qualifies only for a senior citizen without health insurance. A lump-sum premium covering several years is spread equally over those years.',
            'Section 127 (resident individual or HUF): expenditure on a dependant with disability or a deposit in an approved scheme for the dependant\'s maintenance — ₹75,000, or ₹1,25,000 for severe disability (80% or more).',
            'Section 128 (resident individual or HUF): treatment of specified diseases for self or dependant — actual amount up to ₹40,000 (₹1,00,000 for a senior citizen), reduced by any insurance or employer reimbursement.'],
          'Each family group has its own health ceiling; check-ups get a small sub-limit inside it.',
          'A son who pays ₹40,000 premium for his 65-year-old mother can deduct it fully under the parents\' ₹50,000 limit.'),
        C('c4', T4, [
            'Section 129 (individual): interest — not principal — on a loan from a financial institution or approved charitable institution for higher education (any course after Class XII) of self, spouse, children or a student under his guardianship. No monetary limit; allowed for the year interest payments begin and the next 7 tax years, or until paid off if sooner.',
            'Section 130: up to ₹50,000 of interest on a loan sanctioned in 2016-17 (loan ≤ ₹35 lakh, house ≤ ₹50 lakh, no other house on sanction date), in addition to section 22.',
            'Section 131: up to ₹1,50,000 of interest on a loan sanctioned between 1.4.2019 and 31.3.2022 for a house with stamp duty value ≤ ₹45 lakh, for a first-time owner not eligible under section 130.',
            'Section 132: up to ₹1,50,000 of interest on a loan from a bank or NBFC sanctioned between 1.4.2019 and 31.3.2023 for buying an electric vehicle. Interest allowed under sections 130–132 cannot be claimed again elsewhere.'],
          'These deductions reward borrowing for study, a first home or a clean vehicle — and they cover interest only.',
          'A father paying ₹1,80,000 interest on his daughter\'s MBA loan can deduct all of it.'),
        C('c5', T5, [
            'Section 133: donations in money to approved funds and institutions fall into four groups — 100% without limit (e.g. PM National Relief Fund, PM CARES Fund, National Defence Fund); 100% within a limit (e.g. Government for family planning); 50% without limit (PM Drought Relief Fund); and 50% within a limit (approved charitable institutions, Government for other charitable purposes).',
            'The limit is 10% of adjusted GTI: GTI less other Chapter VIII deductions, gains under sections 196, 197 and 198, and income on which no tax is payable. The 100% donations are fitted into this limit first.',
            'Cash donations above ₹2,000 are not deductible, and gifts in kind never qualify. Individuals, HUFs, AOPs and BOIs need the optional regime.',
            'Section 135: donations for scientific, social science or statistical research by a person with no business income. Section 136: an Indian company\'s contributions to a political party or electoral trust. Section 137: such contributions by any person (except a local authority and a Government-funded artificial juridical person). No deduction for cash contributions.'],
          'Generosity is rewarded, but only through traceable payments and within a ceiling for most charities.',
          'A ₹10,000 cash donation to an approved trust gives no deduction; the same sum by UPI would.'),
        C('c6', T6, [
            'Section 134 (individual, optional regime): for rent paid for one\'s own residence when no exempt house rent allowance is received.',
            'Neither the taxpayer, spouse, minor child nor an HUF in which he is a member should own a house where he ordinarily resides, works or carries on business; a house elsewhere is fine if it is not in his occupation and not treated as self-occupied.',
            'Deduction = least of: rent paid less 10% of total income; 25% of total income; ₹5,000 a month. "Total income" here is after all other Chapter VIII deductions but before this one.'],
          'For those without HRA, a small rent relief replaces the allowance.',
          'With total income of ₹4,80,000 and rent of ₹96,000, the deduction is ₹48,000 — rent less 10% of income.'),
        C('c7', T7, [
            'Section 151: royalty of resident authors of books other than textbooks; section 152: royalty on patents for resident patentees. Both need the return to be filed in time.',
            'Section 153 (optional regime): interest on deposits with banks, co-operative banks and post offices — up to ₹10,000 on savings accounts for individuals (not senior citizens) and HUFs; up to ₹50,000 on all deposits, including term deposits, for a senior citizen.',
            'Section 154 (resident individual, optional regime): a fixed ₹75,000 for a person with disability and ₹1,25,000 for severe disability, on producing the medical authority\'s certificate.'],
          'Some deductions follow the income earned rather than the money spent.',
          'A 66-year-old with FD interest of ₹62,000 can deduct ₹50,000.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Year-end tax planning', 'role': 'Tax associate',
         'situation': 'A salaried client asks in February how to cut tax for the year.',
         'steps': ['Compare tax under the default and optional regimes.', 'If optional, list what already fills section 123.', 'Use section 124(3), 126 and 153 room before buying more products.', 'Make sure all payments except check-ups are non-cash.'],
         'takeaway': 'Fill each bucket only to its limit and only if the optional regime wins.'},
        {'id': 'j2', 'title': 'Donation receipts', 'role': 'Article assistant',
         'situation': 'A client hands over a pile of donation receipts for the return.',
         'steps': ['Sort receipts into the four section 133 groups.', 'Reject cash above ₹2,000 and gifts in kind.', 'Work out adjusted GTI and the 10% limit.', 'Fit 100% donations into the limit first.'],
         'takeaway': 'The order of computing the limit changes the result.'},
    ]

    mcqs = [
        Q('m1', 'GTI is ₹4,20,000 and eligible Chapter VIII deductions total ₹4,70,000. Allowable deduction:', ['₹4,20,000', '₹4,70,000', '₹50,000', 'Nil'], 0,
          'Section 122(2) says aggregate deductions cannot exceed gross total income, so the claim is cut to ₹4,20,000 and total income becomes nil. The excess cannot be carried forward as a loss. In practice: plan payments to the income available.', 'c1', T1, 'core', check=420000),
        Q('m2', 'Under the default regime, which deduction is still available to a salaried employee?', ['Employer\'s contribution to NPS', 'LIC premium', 'Health insurance premium', 'Donation to PM National Relief Fund'], 0,
          'Only the employer\'s NPS contribution, the Central Government\'s Agniveer contribution and additional employee cost survive in the default regime. All the others require the taxpayer to opt out. In practice: check the payslip for employer NPS.', 'c1', T1),
        Q('m3', 'Premium on a life policy issued in 2020 on the life of the assessee (sum assured ₹4,00,000), premium ₹55,000. Deduction under section 123:', ['₹40,000', '₹55,000', '₹80,000', '₹60,000'], 0,
          'For ordinary policies issued on or after 1.4.2013, premium qualifies only up to 10% of the actual capital sum assured: 10% of ₹4,00,000 = ₹40,000. The 15% rate is for disability or specified disease cases. In practice: read the policy schedule.', 'c2', T2, 'moderate', check=40000),
        Q('m4', 'Which payment does NOT qualify under section 123?', ['Development fee paid to a school', 'Tuition fee for a full-time course in India', 'PPF deposit in spouse\'s name', 'Sukanya Samriddhi deposit for a daughter'], 0,
          'Only tuition fees for full-time education in India of up to two children qualify; development fees, donations and similar payments are excluded. PPF for the spouse and Sukanya Samriddhi for a girl child qualify. In practice: ask for a split fee receipt.', 'c2', T2),
        Q('m5', 'The extra deduction for an individual\'s own NPS contribution under section 124(3) is up to:', ['₹50,000', '₹1,50,000', '₹25,000', '₹2,00,000'], 0,
          'Section 124(3) gives up to ₹50,000 for the individual\'s own NPS contribution, shared with NPS Vatsalya for a minor under section 124(4). It is in addition to the section 123 cap, but the same amount cannot be claimed twice. In practice: use it after section 123 is full.', 'c2', T2, 'core', check=50000),
        Q('m6', 'Under section 126, preventive health check-up expenses qualify up to:', ['₹5,000 in aggregate, payable even in cash', '₹25,000, non-cash only', '₹10,000 per person', '₹50,000'], 0,
          'Check-ups for self, family and parents together are capped at ₹5,000 within the overall section 126 limits, and are the only payment that may be made in cash. Premiums must be paid by other modes. In practice: keep the lab bill.', 'c3', T3),
        Q('m7', 'Mr. Dev (45) pays health premium of ₹40,000 for his father, aged 63. Deduction for this payment:', ['₹40,000', '₹25,000', '₹50,000', 'Nil'], 0,
          'The father is a senior citizen, so the parents\' limit rises to ₹50,000. The premium of ₹40,000 falls within it and is fully deductible, provided it is not paid in cash. In practice: age is checked during the tax year.', 'c3', T3, 'moderate', check=40000),
        Q('m8', 'Section 128 deduction for a senior citizen dependant, where ₹1,30,000 was spent and ₹20,000 was reimbursed by insurance:', ['₹1,00,000', '₹1,10,000', '₹1,30,000', '₹40,000'], 0,
          'The ceiling for a senior citizen is ₹1,00,000, and the deduction is reduced by insurance or employer reimbursement. Net spending is ₹1,10,000, so the cap of ₹1,00,000 applies. In practice: keep the prescribed specialist certificate.', 'c3', T3, 'hard', check=100000),
        Q('m9', 'Interest on an education loan under section 129 is deductible:', ['Without a monetary limit, for up to 8 tax years', 'Up to ₹1,50,000 a year', 'Only for studies in India', 'For both principal and interest'], 0,
          'Section 129 allows the whole interest, without a ceiling, for the year repayment of interest starts and the next 7 tax years. Recognised courses abroad qualify; principal does not. In practice: the loan must come from an approved lender.', 'c4', T4),
        Q('m10', 'Which loan can give interest deduction under section 132?', ['A bank loan sanctioned in June 2022 for an electric car', 'A loan from a friend for an electric scooter', 'A bank loan sanctioned in 2024 for an electric car', 'A loan for a petrol car'], 0,
          'Section 132 covers interest on a loan from a bank or NBFC sanctioned between 1.4.2019 and 31.3.2023 for buying an electric vehicle, up to ₹1,50,000 a year. Loans from friends or later sanctions do not qualify. In practice: check the sanction letter date.', 'c4', T4),
        Q('m11', 'A cash donation of ₹3,000 to the PM National Relief Fund is:', ['Not deductible', 'Deductible in full', 'Deductible at 50%', 'Deductible up to ₹2,000'], 0,
          'Section 133(5) denies any deduction for a donation above ₹2,000 paid in cash, even to a fund that otherwise gets 100% without limit. The whole ₹3,000 is lost, not just the excess. In practice: pay by cheque or UPI.', 'c5', T5),
        Q('m12', 'In computing the 10% qualifying limit for donations, adjusted GTI excludes:', ['Long-term capital gains taxable under section 197', 'Salary income', 'Interest on fixed deposits', 'Rent from a let-out house'], 0,
          'Adjusted GTI is GTI less other Chapter VIII deductions, gains taxed under sections 196, 197 and 198, and income not chargeable to tax. Salary, interest and rent stay in. In practice: compute it before applying the 10% cap.', 'c5', T5),
        Q('m13', 'Section 137 does not allow a deduction for contribution to a political party when:', ['It is paid in cash', 'It is made by an individual', 'It is made to an electoral trust', 'It exceeds ₹10,000'], 0,
          'Contributions by any person to a registered political party or electoral trust are deductible, except where paid in cash. Individuals qualify under the optional regime, and there is no fixed amount limit. In practice: keep the party\'s receipt.', 'c5', T5),
        Q('m14', 'Total income before section 134 is ₹3,60,000; rent paid ₹54,000; no HRA. Deduction under section 134:', ['₹18,000', '₹54,000', '₹60,000', '₹90,000'], 0,
          'Least of: rent less 10% of total income (54,000 − 36,000 = ₹18,000), 25% of total income (₹90,000) and ₹60,000 (₹5,000 a month). So ₹18,000. In practice: low rent relative to income gives little relief.', 'c6', T6, 'hard', check=18000),
        Q('m15', 'A senior citizen earns ₹42,000 FD interest and ₹12,000 savings interest. Deduction under section 153:', ['₹50,000', '₹10,000', '₹54,000', '₹42,000'], 0,
          'For senior citizens, interest on all bank, co-operative bank and post office deposits, including term deposits, qualifies up to ₹50,000. Total interest of ₹54,000 is capped at ₹50,000. In practice: others get ₹10,000 on savings only.', 'c7', T7, 'moderate', check=50000),
        Q('m16', 'Section 154 deduction for a resident individual with 85% disability:', ['₹1,25,000', '₹75,000', 'Actual expenditure', '₹50,000'], 0,
          'Section 154 gives a fixed ₹75,000 for disability and ₹1,25,000 for severe disability, meaning over 80%, whatever the expenditure. A medical authority certificate must be produced. In practice: renew the certificate when required.', 'c7', T7, 'core', check=125000),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'LIC premium at 10% of sum assured', 1, 'computation', '10%', nums=[lic]),
           S('s2', 'Tuition fees for two children', 1, 'computation', 'two children', nums=[tui]),
           S('s3', 'Cap of ₹1,50,000', 1, 'computation', '1,50,000', nums=[s123]),
           S('s4', 'NPS under section 124(3)', 2, 'computation', '124(3)', nums=[s124, tot])],
          ['Apply each sub-limit before the overall cap.'], ['Allowing three children\'s fees.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Check-up sub-limit', 1, 'concept', '5,000'),
           S('s2', 'Self and family cap', 1, 'computation', '25,000', nums=[own]),
           S('s3', 'Parents senior citizen cap', 2, 'computation', '50,000', nums=[par, t2])],
          ['Treat each group separately.'], ['Pooling all payments under one limit.'], ['Table.'], pad='table', checks=list(ck2)),
        W('q3', 6, i3['q'], i3['solution'],
          [S('s1', 'Adjusted GTI', 2, 'computation', 'adjusted', nums=[adj]),
           S('s2', 'Qualifying limit', 1, 'computation', '10%', nums=[lim]),
           S('s3', 'Order within the limit', 2, 'computation', '100%', nums=[lim_part]),
           S('s4', 'Unlimited donations and cash rule', 1, 'computation', 'cash', nums=[d133])],
          ['Exclude special-rate gains.'], ['Applying 50% before fitting the 100% donation.'], ['Step table.'], pad='table', checks=list(ck3)),
    ]

    viva = [
        V('v1', 'How does a deduction differ from an exemption?',
          'An exempt income is excluded and never forms part of gross total income, while income eligible for a deduction is first included in GTI and the deduction is then subtracted from it to get total income.',
          [P('p1', 'Exempt kept out', 5, 'exclud|never'), P('p2', 'Deduction from GTI', 5, 'gross total income|gti')], 'c1'),
        V('v2', 'Can Chapter VIII deductions create a loss?',
          'Total deductions are restricted to gross total income, so total income can fall to nil but cannot become negative, and nothing is carried forward.',
          [P('p1', 'Restricted to GTI', 6, 'gross total income|gti'), P('p2', 'Nil at most', 4, 'nil|negative')], 'c1'),
        V('v3', 'What qualifies under section 123 for a housing loan?',
          'Repayment of the principal on a loan from a specified lender for buying or building a residential house, together with stamp duty, registration fee and other transfer expenses; interest is dealt with under house property.',
          [P('p1', 'Principal', 5, 'principal'), P('p2', 'Stamp duty and registration', 5, 'stamp|registration')], 'c2'),
        V('v4', 'How is the deduction for rent paid without HRA computed?',
          'It is the least of rent paid minus 10% of total income, 25% of total income, and ₹5,000 a month, with total income taken after all other Chapter VIII deductions.',
          [P('p1', 'Three limits', 6, '10%|25%|5,000'), P('p2', 'Total income basis', 4, 'total income')], 'c6'),
        V('v5', 'Which payment modes are accepted for section 126?',
          'Health insurance premium and other payments must be made by a mode other than cash, but preventive health check-ups up to ₹5,000 may be paid in any mode, including cash.',
          [P('p1', 'Non-cash for premium', 5, 'other than cash|non-cash'), P('p2', 'Check-up cash allowed', 5, 'check')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'The Menon household', 'difficulty': 'moderate',
              'case': 'Mrs. Menon, 62, a retired teacher, opts out of the default regime. Her GTI is ₹9,00,000, all from pension and interest, including FD interest of ₹70,000. In tax year 2026-27 she paid a health premium of ₹45,000 for herself, PPF ₹1,00,000, interest of ₹90,000 on her son\'s education loan taken in her name, and donated ₹10,000 by cheque to an approved charitable trust.',
              'mcqs': [
                  M('k1a', 'Deduction under section 126 for her own health premium:', ['₹45,000', '₹25,000', '₹50,000', 'Nil'], 0,
                    'She is a senior citizen, so the limit for self and family rises to ₹50,000, and her ₹45,000 premium paid by non-cash mode is fully deductible. In practice: the higher limit depends on age in the tax year.', 'core', check=45000, topic=T3),
                  M('k1b', 'Deduction under section 153 for her FD interest:', ['₹50,000', '₹10,000', '₹70,000', 'Nil'], 0,
                    'As a senior citizen she may deduct interest on all deposits, including fixed deposits, up to ₹50,000. FD interest of ₹70,000 is therefore capped at ₹50,000. In practice: others would get only savings interest.', 'core', check=50000, topic=T7),
                  M('k1c', 'Education loan interest for her son is:', ['Fully deductible under section 129', 'Not deductible as the son is an adult', 'Deductible up to ₹50,000', 'Deductible under section 123'], 0,
                    'Section 129 covers interest on a loan taken by the individual for higher education of self, spouse, children or a ward, with no age bar on the child and no ceiling. In practice: the loan must be in the parent\'s name.', 'moderate', topic=T4),
                  M('k1d', 'Total of these four deductions (donation within its limit):', ['₹2,90,000', '₹2,85,000', '₹2,95,000', '₹2,70,000'], 0,
                    'Section 126 ₹45,000 + section 123 ₹1,00,000 + section 129 ₹90,000 + section 153 ₹50,000 = ₹2,85,000; the donation adds 50% of ₹10,000, which is well within 10% of adjusted GTI. Total ₹2,90,000. In practice: show each section separately.', 'hard', check=290000, topic=T5),
              ]}]

    return unit(UID, 'p3', 'int-p3-a-ch06', 1, 'Deductions from Gross Total Income',
                ['Distinguish deductions from exemptions and apply section 122 and the default regime rule.',
                 'Compute deductions for savings, pension and health payments.',
                 'Compute interest-based deductions and donation deductions with the qualifying limit.',
                 'Apply the rent, deposit interest and disability deductions.'],
                {'difficulty': 'core', 'minutes': {'learn': 50, 'practice': 50}, 'prereq': ['int-p3-a-ch05-u01'],
                 'exam_tip': 'First confirm the regime — almost every deduction needs the optional regime. Then apply each sub-limit, then the overall cap, and finally the GTI ceiling.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Deduction ≠ exemption; deductions ≤ GTI (s. 122).',
                             'Default regime: only s. 124(1)/(2), 125(2) and 146.',
                             's. 123: ₹1,50,000; s. 124(3): extra ₹50,000 for own NPS.',
                             's. 126: ₹25,000 / ₹50,000 per group; check-up ₹5,000.',
                             's. 129–132: interest only; s. 133: four groups, 10% of adjusted GTI.',
                             's. 134: least of three; s. 153: ₹10,000 / ₹50,000; s. 154: ₹75,000 / ₹1,25,000.'],
                 'remember': ['Cash kills most deductions (except check-ups).', 'Special-rate capital gains get no Chapter VIII deduction.'],
                 'traps': ['Only two children for tuition fees.', 'Insurance premium capped at % of sum assured.']},
                [('s. 123', '₹1,50,000'), ('s. 124(3)', '₹50,000'), ('s. 153 senior', '₹50,000'), ('Donation qualifying limit', '10% of adjusted GTI')],
                viva, cases)
