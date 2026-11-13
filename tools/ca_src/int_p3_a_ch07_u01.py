"""CA Intermediate · Paper 3A Income-tax Law · Chapter 7 TDS, TCS and Advance Tax (Income-tax Act, 2025; tax year 2026-27).
Scope follows the ICAI study material; section numbers are taken from it; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-a-ch07-u01'
T1 = 'How tax is recovered during the year (ss. 390-391) and TDS on salary (s. 392)'
T2 = 'TDS on payments to residents (s. 393(1))'
T3 = 'TDS on payments to any person (s. 393(3)) and the PAN rule (s. 397)'
T4 = 'Tax collection at source (s. 394)'
T5 = 'Defaults: interest and assessee-in-default (s. 398)'
T6 = 'Advance tax (ss. 403-410) and interest (ss. 424-425)'


def build():
    # i1 — rent paid by a salaried individual
    ck = Checks()
    t9 = ck.add('60000*2/100*9', 'TDS on 9 months\' rent at 2%')
    nopan = ck.add('min(60000*20/100*9, 60000)', 'TDS without PAN, capped at last month\'s rent')
    i1 = {'id': 'i1', 'title': 'A salaried tenant as deductor', 'difficulty': 'core', 'minutes': 6,
          'q': 'Ms. Kavya, a salaried employee with no business income, rents a flat from Mr. Rohan at ₹60,000 a month from 1 July 2026 and stays on beyond March 2027. Is TDS required? If so, when and how much? What if Mr. Rohan does not give his PAN?',
          'solution': [table(['Point', 'Answer'], [
              ['Provision', 'Section 393(1) [Table: Sl. No. 2(i)] — an individual who is not a specified person paying rent above ₹50,000 a month'],
              ['Rate', '2%'],
              ['When', 'Once, from the rent for March 2027 (the last month of the tax year)'],
              ['Amount', '₹60,000 × 2% × 9 months = ' + inr(t9)],
              ['Without PAN', '20% gives ₹1,08,000, but the deduction cannot go beyond one month\'s rent: ' + inr(nopan)],
              ['TAN', 'Not needed for this deduction']], title='Rent TDS by an individual')],
          'checks': list(ck)}

    # i2 — contractor threshold
    ck2 = Checks()
    agg = ck2.add('25000+28000+30000+22000', 'Aggregate payments to the contractor firm')
    tds2 = ck2.add('105000*2/100', 'TDS at 2% on the whole aggregate')
    i2 = {'id': 'i2', 'title': 'Small bills that add up', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Nimbus Ltd. paid a firm of painters for four separate jobs in tax year 2026-27: ₹25,000, ₹28,000, ₹30,000 and ₹22,000 (the last in February 2027). No single bill crossed ₹30,000. Is TDS needed and how much?',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Single-payment limit', 'No bill is above ₹30,000', '—'],
              ['Aggregate limit', 'Total for the year', inr(agg)],
              ['Result', 'Aggregate above ₹1,00,000, so TDS applies to the whole amount', ''],
              ['Rate', 'Payee is a firm (not individual/HUF): 2%', inr(tds2)]], title='Section 393(1) [Table: Sl. No. 6(i)]'),
              note('Once the yearly aggregate crosses ₹1,00,000, tax is due on all the payments, including the earlier small ones; in practice the shortfall is recovered from the bill that crosses the limit.')],
          'checks': list(ck2)}

    # i3 — advance tax and section 425
    ck3 = Checks()
    j1 = ck3.add('(240000*15/100-20000)*3/100', 'Shortfall at 15 June × 3%')
    d1 = ck3.add('(240000*75/100-150000)*3/100', 'Shortfall at 15 December × 3%')
    tot3 = ck3.add('480+900', 'Total interest under section 425')
    i3 = {'id': 'i3', 'title': 'Missing two instalments', 'difficulty': 'hard', 'minutes': 9,
          'q': 'Orbit Pvt. Ltd. has tax due on returned income (after TDS) of ₹2,40,000 for tax year 2026-27. Its cumulative advance tax payments were: by 15 June ₹20,000; by 15 September ₹1,08,000; by 15 December ₹1,50,000; by 15 March ₹2,40,000. Compute interest under section 425.',
          'solution': [table(['Date', 'Due (cumulative)', 'Paid', 'Shortfall', 'Interest ₹'], [
              ['15 June', '15% = 36,000', '20,000 (8.3%, below the 12% safe level)', '16,000', inr(j1)],
              ['15 September', '45% = 1,08,000', '1,08,000', 'Nil', '0'],
              ['15 December', '75% = 1,80,000', '1,50,000', '30,000', inr(d1)],
              ['15 March', '100% = 2,40,000', '2,40,000', 'Nil', '0'],
              ['Total', '', '', '', inr(tot3)]], title='Section 425 (3% for each of the first three dates, 1% for March)'),
              note('No section 424 interest arises, because advance tax paid equals the assessed tax (well above 90%).')],
          'checks': list(ck3)}

    concepts = [
        C('c1', T1, [
            'Section 390: during the tax year the Government recovers tax in three ways — deduction or collection at source, advance tax, and tax an employer pays on non-monetary perquisites under section 392(2)(a). Tax so paid is credited to the person whose income it relates to.',
            'Section 391: where nothing is deducted (no provision, or a failure to deduct), the payee pays directly. A deductor who neither deducts nor pays, where the payee has also not paid, is treated as an assessee-in-default.',
            'Section 392(1): when salary is paid, the employer withholds tax using the average rate of tax on the employee\'s estimated income. The employee tells the employer each year which regime he intends to use; if he says nothing, the default regime of section 202(1) is assumed.',
            'An employer may choose to bear tax on non-monetary perquisites at the same average rate; that tax is exempt for the employee but not deductible for the employer. Section 392(7): trustees deduct 10% from a taxable premature PF withdrawal of ₹50,000 or more.'],
          'TDS on salary spreads the year\'s tax evenly over pay days, based on the employer\'s best estimate.',
          'Salary ₹8,50,000 with tax of ₹75,400 gives an average rate of about 9.4%, applied to each payment.'),
        C('c2', T2, [
            'Section 393(1) lists payments to residents. Unless stated otherwise, tax is deducted on the whole amount once the threshold is crossed, at the earlier of credit (including a suspense account) and payment.',
            'Key rows: insurance commission (2%, or 10% for a domestic company payee; ₹20,000); other commission or brokerage (2%; ₹20,000); rent by individuals/HUFs outside the turnover test (2%; ₹50,000 a month); rent by specified persons (2% plant and machinery, 10% land, building or furniture; ₹50,000 a month); transfer of non-agricultural immovable property (1% of the higher of consideration and stamp duty value; ₹50 lakh); compulsory acquisition (10%; ₹5 lakh).',
            'Further rows: units of mutual funds (10%; ₹10,000); interest from banks and notified post-office deposits (10%; ₹1,00,000 for senior citizens, ₹50,000 others) and from other specified persons (₹10,000); contract work (1% individual/HUF, 2% others; ₹30,000 single or ₹1,00,000 a year); work, professional fees or commission paid by individuals/HUFs not otherwise covered (2%; ₹50 lakh); professional and technical fees, royalty and non-compete fees (10%, or 2% for technical services and film royalty; ₹50,000 each; nil limit for directors\' fees); dividend (10%); life policy proceeds (2% of the income part; ₹1,00,000); purchase of goods by a buyer with turnover above ₹10 crore (0.1% of the amount above ₹50 lakh); business perquisites (10%; ₹20,000).',
            'A "specified person" is anyone other than an individual or HUF, or an individual/HUF whose turnover in the preceding year exceeded ₹1 crore (business) or ₹50 lakh (profession). Individuals deducting on rent, property purchase and the ₹50-lakh contract row need no TAN.'],
          'Think of the Table as a menu: find the row, then check payer, payee, rate and limit — in that order.',
          'A small shopkeeper with ₹60 lakh turnover paying ₹25,000 brokerage deducts nothing; a company paying the same must deduct 2%.'),
        C('c3', T3, [
            'Section 393(3) covers payments to any person, resident or not: winnings from lotteries, crosswords, card games and betting (30%; above ₹10,000 per transaction); online game winnings (30%, on net winnings at withdrawal or year end, no threshold); horse-race winnings (30%; ₹10,000); lottery ticket commission (2%; ₹20,000); cash withdrawals from banks (2% above ₹1 crore, or ₹3 crore for co-operative societies); and partner\'s salary, commission, bonus or interest paid by a firm (10%; ₹20,000).',
            'Section 397(2): a payee who does not furnish a valid PAN suffers TDS at the highest of the specified rate, the rate in force and 20% (5% for the purchase-of-goods row). For rent by individuals, this higher deduction is still capped at the last month\'s rent. Where the normal rate already exceeds 20%, as for winnings at 30%, nothing changes.',
            'For TCS without PAN the rate is the higher of twice the normal rate and 5%, but not above 20%.'],
          'Missing PAN is expensive: the law pushes the rate up so that the payee has every reason to give it.',
          'A machinery lessor without PAN suffers 20% instead of 2% on rent.'),
        C('c4', T4, [
            'Section 394 makes certain sellers and others collect tax from the buyer at the time of debit or receipt, whichever is earlier.',
            'Sale of alcoholic liquor, tendu leaves, forest produce, scrap and coal, lignite or iron ore, and grant of a parking lot, toll plaza, mine or quarry: 2% for minerals and others as per the Table. Buyers who use such goods for manufacture or power (not trading) can give a declaration to avoid collection.',
            'Motor vehicles and notified goods above ₹10 lakh: 1%. Remittances under the Liberalised Remittance Scheme above ₹10 lakh: 2% for education or medical treatment, 20% for other purposes, on the excess over ₹10 lakh; overseas tour packages: 2% up to ₹10 lakh and 20% above.'],
          'TCS works like TDS in reverse — the seller adds the tax to the bill and passes it on to the Government.',
          'A student remitting ₹13 lakh for foreign tuition suffers TCS of 2% on ₹3 lakh, i.e. ₹6,000.'),
        C('c5', T5, [
            'Section 398: a person who fails to deduct or collect, or after doing so fails to pay, is treated as an assessee-in-default for that tax.',
            'Interest is simple: 1% a month or part of a month from the date tax was deductible or collectible to the date it is actually deducted or collected; 1.5% a month or part of a month from the date of deduction or collection to the date of payment. It must be paid before the quarterly statement is filed.',
            'Relief: if the payee has filed his return, included the income and paid the tax on it, and an accountant certifies this, the payer is not treated as in default; interest at 1% then runs only until the payee\'s return date. Unpaid tax collected or deducted, with interest, is a charge on all the payer\'s assets.'],
          'Late deduction costs 1% a month; holding the Government\'s money costs 1.5% a month.',
          'Tax deducted on 10 May but paid on 20 July attracts 1.5% × 3 months.'),
        C('c6', T6, [
            'Sections 403–404: advance tax is paid during the financial year on the current year\'s income when the tax payable (after TDS/TCS) is ₹10,000 or more. A resident individual aged 60 or more with no business or professional income is exempt.',
            'Section 408: instalments by 15 June (15%), 15 September (45%), 15 December (75%) and 15 March (100%), cumulatively. Presumptive-income taxpayers under section 58(2) pay the whole by 15 March. Payment up to 31 March still counts as advance tax for that year.',
            'Section 424: if advance tax paid is less than 90% of assessed tax, simple interest at 1% a month runs from 1 April after the tax year on the shortfall until the date of determination of income (reduced for self-assessment tax paid).',
            'Section 425: for deferment, 3% (three months at 1%) on each shortfall at 15 June, 15 September and 15 December, and 1% at 15 March. No interest arises on the first two dates if at least 12% and 36% respectively were paid.'],
          'Advance tax means "pay as you earn" for income that has no deductor watching it.',
          'If 13% of the year\'s tax is paid by 15 June, no section 425 interest arises for June.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Vendor master review', 'role': 'Article assistant',
         'situation': 'An accounts head asks which new vendor payments need TDS.',
         'steps': ['Classify each vendor by nature of payment and Table row.', 'Check whether the company is a "specified" or "designated" person.', 'Track single and yearly thresholds in the ERP.', 'Collect PAN before the first payment.'],
         'takeaway': 'Most TDS errors come from the wrong row or a missing PAN, not from arithmetic.'},
        {'id': 'j2', 'title': 'Advance tax reminder', 'role': 'Tax associate',
         'situation': 'A consultant with rising fee income asks how much to pay by 15 December.',
         'steps': ['Estimate the year\'s income and tax.', 'Deduct TDS expected on fees.', 'Pay up to 75% of the balance, net of earlier instalments.', 'Re-estimate before 15 March.'],
         'takeaway': 'A quarterly re-estimate avoids most section 425 interest.'},
    ]

    mcqs = [
        Q('m1', 'If an employee does not tell the employer which tax regime he intends to use, the employer deducts tax:', ['Under the default regime of section 202(1)', 'Under the optional regime', 'At a flat 10%', 'Not at all until told'], 0,
          'The law presumes the employee stays in the default regime when no intimation is given, and the employer computes TDS on that basis. In practice: collect the declaration in April.', 'c1', T1),
        Q('m2', 'Rent of ₹55,000 a month paid by a private company for an office building attracts TDS at:', ['10%', '2%', '1%', '20%'], 0,
          'A company is a specified person; for land, building, furniture or fittings the rate is 10%, while plant and machinery attract 2%. In practice: split composite rent if the agreement shows both.', 'c2', T2, check=10),
        Q('m3', 'A flat is bought for ₹48 lakh but its stamp duty value is ₹52 lakh. TDS by the buyer:', ['₹52,000', '₹48,000', 'Nil', '₹5,200'], 0,
          'TDS applies when either consideration or stamp duty value is ₹50 lakh or more, at 1% of the higher figure: 1% of ₹52 lakh = ₹52,000. In practice: the buyer needs no TAN.', 'c2', T2, 'moderate', check=52000),
        Q('m4', 'A bank pays FD interest of ₹70,000 in the year to a resident aged 66. TDS:', ['Nil', '₹7,000', '₹2,000', '₹1,400'], 0,
          'For senior citizens, banks deduct only when interest exceeds ₹1,00,000 in the year; ₹70,000 is below that, so nothing is deducted. In practice: the limit is ₹50,000 for others.', 'c2', T2, 'moderate'),
        Q('m5', 'A company with turnover of ₹40 crore buys goods worth ₹80 lakh from one seller in the year. TDS:', ['₹3,000', '₹8,000', '₹80,000', 'Nil'], 0,
          'The buyer deducts 0.1% only on the amount above ₹50 lakh: 0.1% × ₹30 lakh = ₹3,000. In practice: track purchases per seller.', 'c2', T2, 'moderate', check=3000),
        Q('m6', 'A firm pays a partner interest on capital of ₹25,000 during the year. TDS:', ['10% of ₹25,000', 'Nil, as partners are owners', '2% of ₹25,000', '10% of ₹5,000'], 0,
          'Section 393(3) requires a firm to deduct 10% on salary, remuneration, commission, bonus or interest to a partner when the yearly total exceeds ₹20,000, and then on the whole amount. In practice: interest credited to capital account counts.', 'c3', T3),
        Q('m7', 'A machinery lessor gives no PAN. TDS on ₹1,00,000 monthly lease rent by a company is at:', ['20%', '2%', '4%', '10%'], 0,
          'The rate becomes the highest of the normal 2%, the rate in force and 20%, so 20% applies. In practice: ask for PAN before the first credit.', 'c3', T3, check=20),
        Q('m8', 'TCS on an LRS remittance of ₹15 lakh for a holiday (not a tour package) is:', ['₹1,00,000', '₹3,00,000', '₹10,000', 'Nil'], 0,
          'For purposes other than education or medical treatment, 20% applies to the amount above ₹10 lakh: 20% × ₹5 lakh = ₹1,00,000. In practice: the bank collects it at the time of remittance.', 'c4', T4, 'moderate', check=100000),
        Q('m9', 'Tax deducted on 5 June is paid to the Government on 12 August. Interest under section 398:', ['1.5% for 3 months', '1% for 2 months', '1.5% for 2 months', '1% for 3 months'], 0,
          'After deduction, delay in payment attracts 1.5% for every month or part of a month. 5 June to 12 August covers parts of three months. In practice: remit by the due date.', 'c5', T5, 'moderate'),
        Q('m10', 'Advance tax is NOT payable by:', ['A resident aged 70 with only pension and interest income', 'A company with tax of ₹50,000', 'A doctor aged 62 with professional income', 'A firm with tax of ₹12,000'], 0,
          'A resident individual aged 60 or more without income from business or profession is exempt. The doctor has professional income, and the others owe ₹10,000 or more. In practice: such seniors pay self-assessment tax instead.', 'c6', T6),
        Q('m11', 'By 15 September, a non-presumptive taxpayer must have paid, cumulatively:', ['45% of the tax', '30% of the tax', '60% of the tax', '75% of the tax'], 0,
          'The schedule is 15%, 45%, 75% and 100% by June, September, December and March. Paying at least 36% by September avoids section 425 interest for that date. In practice: compute cumulatively.', 'c6', T6),
        Q('m12', 'Section 424 interest applies when advance tax paid is less than what share of assessed tax?', ['90%', '75%', '100%', '80%'], 0,
          'Interest at 1% a month from 1 April after the tax year arises only if advance tax falls below 90% of assessed tax, and is then charged on the shortfall. In practice: assessed tax is after TDS and relief.', 'c6', T6, check=90),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Correct row and payer', 1, 'concept', '2(i)|individual'),
           S('s2', 'Timing in last month', 1, 'concept', 'march|last month'),
           S('s3', 'TDS amount', 1, 'computation', '2%', nums=[t9]),
           S('s4', 'Higher rate capped', 1, 'computation', '20%', nums=[nopan])],
          ['The cap applies only to this row.'], ['Deducting every month.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Single limit tested', 1, 'concept', '30,000'),
           S('s2', 'Aggregate', 1, 'computation', '1,00,000', nums=[agg]),
           S('s3', 'Rate and TDS', 2, 'computation', '2%', nums=[tds2])],
          ['Test both limits.'], ['Deducting only on the last bill.'], ['Step table.'], pad='table', checks=list(ck2)),
        W('q3', 5, i3['q'], i3['solution'],
          [S('s1', 'Instalment dues', 1, 'computation', '15%|45%|75%'),
           S('s2', '12% safe harbour tested', 1, 'concept', '12%'),
           S('s3', 'Interest by date', 2, 'computation', '3%', nums=[j1, d1]),
           S('s4', 'Total', 1, 'computation', 'total', nums=[tot3])],
          ['Shortfall is cumulative.'], ['Charging 1% for June.'], ['Date-wise table.'], pad='table', checks=list(ck3)),
    ]

    viva = [
        V('v1', 'At what rate does an employer deduct tax from salary?',
          'At the average rate of income-tax, worked out on the employee\'s estimated income for the year under the regime he has intimated, and applied at each payment.',
          [P('p1', 'Average rate', 6, 'average'), P('p2', 'Estimated income', 4, 'estimat')], 'c1'),
        V('v2', 'Who is a specified person for TDS on commission or interest?',
          'Any person other than an individual or HUF, and an individual or HUF whose turnover in the preceding year was above ₹1 crore for a business or ₹50 lakh for a profession.',
          [P('p1', 'Non-individuals', 5, 'other than|hUF'), P('p2', 'Turnover test', 5, '1 crore|50 lakh')], 'c2'),
        V('v3', 'What happens if the payee does not furnish PAN?',
          'Tax is deducted at the highest of the specified rate, the rate in force and 20%, and collected at the higher of twice the rate and 5% capped at 20%.',
          [P('p1', '20% for TDS', 6, '20%'), P('p2', 'TCS rule', 4, 'twice|5%')], 'c3'),
        V('v4', 'What interest applies for late deposit of TDS?',
          'Simple interest of 1.5% for every month or part of a month from the date of deduction to the date of payment, and 1% a month for late deduction.',
          [P('p1', '1.5% after deduction', 6, '1.5%'), P('p2', '1% for late deduction', 4, '1%')], 'c5'),
        V('v5', 'When does advance tax become payable?',
          'When the tax payable for the year after TDS and TCS is ₹10,000 or more, in four cumulative instalments by 15 June, 15 September, 15 December and 15 March.',
          [P('p1', '₹10,000', 5, '10,000'), P('p2', 'Instalment dates', 5, '15 june|15 march')], 'c6'),
    ]

    cases = [{'id': 'k1', 'title': 'Mehta Traders\' year-end', 'difficulty': 'moderate',
              'case': 'Mehta Traders, a partnership firm with last year\'s turnover of ₹14 crore, made these payments in tax year 2026-27: legal fees to a resident advocate ₹45,000 and ₹20,000 (two matters); rent for a warehouse ₹70,000 a month; interest on capital to partner Ravi ₹60,000; and goods purchased from Leela Mills ₹1.1 crore. All payees have given PAN.',
              'mcqs': [
                  M('k1a', 'TDS on the advocate\'s fees:', ['₹6,500', 'Nil', '₹4,500', '₹1,300'], 0,
                    'Professional fees above ₹50,000 in the year attract 10% on the whole amount; ₹65,000 in total gives ₹6,500. In practice: aggregate all matters for the same payee.', 'moderate', check=6500, topic=T2),
                  M('k1b', 'Monthly TDS on the warehouse rent:', ['₹7,000', '₹1,400', '₹3,500', 'Nil'], 0,
                    'A firm is a specified person and a warehouse is a building, so 10% applies to ₹70,000 a month. In practice: deduct at credit or payment, whichever is earlier.', 'core', check=7000, topic=T2),
                  M('k1c', 'TDS on Ravi\'s interest on capital:', ['₹6,000', '₹4,000', 'Nil', '₹1,200'], 0,
                    'A firm deducts 10% on interest to a partner once the year\'s total exceeds ₹20,000: 10% × ₹60,000 = ₹6,000. In practice: credit to capital account also triggers TDS.', 'core', check=6000, topic=T3),
                  M('k1d', 'TDS on purchases from Leela Mills:', ['₹6,000', '₹11,000', '₹1,10,000', 'Nil'], 0,
                    'The firm\'s turnover is above ₹10 crore, so it deducts 0.1% on purchases above ₹50 lakh: 0.1% × ₹60 lakh = ₹6,000. In practice: TDS takes priority over the seller\'s TCS.', 'moderate', check=6000, topic=T2),
              ]}]

    return unit(UID, 'p3', 'int-p3-a-ch07', 1, 'Tax Deduction or Collection at Source and Advance Tax',
                ['Explain how tax is recovered during the year and compute TDS on salary.',
                 'Identify the Table row, rate and threshold for common payments to residents and any person.',
                 'Apply TCS and the higher rates for missing PAN.',
                 'Compute advance tax instalments and interest under sections 398, 424 and 425.'],
                {'difficulty': 'core', 'minutes': {'learn': 60, 'practice': 55}, 'prereq': ['int-p3-a-ch06-u01'],
                 'exam_tip': 'For every payment, write the row, payer status, payee status, rate and threshold before computing. For advance tax, always work cumulatively.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Recovery during the year: TDS/TCS, advance tax, employer-paid perquisite tax (s. 390).',
                             'Salary: average rate on estimated income (s. 392).',
                             's. 393(1): residents; s. 393(3): any person; s. 394: TCS.',
                             'No PAN: TDS at least 20% (5% for goods); TCS higher of 2× and 5%, max 20%.',
                             'Defaults: 1% (late deduction), 1.5% (late payment) per month.',
                             'Advance tax ≥ ₹10,000: 15/45/75/100%; s. 424 below 90%; s. 425 3%/1%.'],
                 'remember': ['Rent cap: higher TDS cannot exceed last month\'s rent for individuals.', 'Seniors 60+ without business income pay no advance tax.'],
                 'traps': ['Contract limits: ₹30,000 single or ₹1,00,000 yearly.', 'Purchase of goods TDS only on the excess over ₹50 lakh.']},
                [('Contract work', '1% / 2%; ₹30,000 or ₹1,00,000'), ('Professional fees', '10%; ₹50,000'), ('Bank interest', '₹50,000; ₹1,00,000 senior'), ('Advance tax', '15/45/75/100%')],
                viva, cases)
