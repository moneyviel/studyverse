"""CA Final · Paper 4 · Chapter 13 Deduction, Collection and Recovery of Tax.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch13-u01'
T1 = 'Framework of tax deduction at source'
T2 = 'Key TDS provisions for residents'
T3 = 'Tax collection at source'
T4 = 'Consequences of default and higher rates'
T5 = 'Advance tax and self-assessment'


def build():
    ck = Checks()
    a = ck.add('(25000+28000+60000)*0.01', '(a) TDS on contractor (₹)')
    c = ck.add('70000*12*0.10', '(c) TDS on rent of building (₹)')
    d = ck.add('(8000000-5000000)*0.001', '(d) TDS on purchase of goods (₹)')
    tot = ck.add('(25000+28000+60000)*0.01+70000*12*0.10+(8000000-5000000)*0.001', 'Total TDS (₹)')
    i1 = {'id': 'i1', 'title': 'TDS for a company payer', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'Sarovar Ltd (turnover ₹60 crore last year) pays in T.Y. 2026-27: (a) to Mohan, an individual contractor, ₹25,000, ₹28,000 and ₹60,000 under one contract; (b) professional fees of ₹45,000 to Dr. Rao (only payment); (c) office rent of ₹70,000 a month to Lata, an individual; (d) ₹80,00,000 to one supplier for goods. All payees furnished PAN. Compute TDS.',
          'solution': [table(['Payment', 'Reason', '₹'], [
              ['(a) Contractor', 'Aggregate ₹1,13,000 exceeds ₹1,00,000: 1% on all', inr(a)],
              ['(b) Professional fees', 'Within ₹50,000 threshold', '—'],
              ['(c) Rent', '10% for building (specified person payer), above ₹50,000 a month', inr(c)],
              ['(d) Goods', '0.1% on amount exceeding ₹50 lakh', inr(d)],
              ['Total', '', inr(tot)]], title='Section 393(1)')],
          'checks': list(ck)}

    c2 = Checks()
    i_a = c2.add('20000*0.01*2', 'Interest for late deduction: 2 months at 1% (₹)')
    i_b = c2.add('20000*0.015*2', 'Interest for late payment: 2 months at 1.5% (₹)')
    i_t = c2.add('20000*0.01*2+20000*0.015*2', 'Total interest (₹)')
    i2 = {'id': 'i2', 'title': 'Interest on TDS default', 'difficulty': 'core', 'minutes': 5,
          'q': 'Tax of ₹20,000 was deductible on 10 June 2026 but was deducted on 10 August 2026 and paid to the government on 20 September 2026. Compute interest under section 398 (count each month or part).',
          'solution': [table(['Period', 'Working', '₹'], [
              ['10 June – 10 August', '2 months × 1%', inr(i_a)],
              ['10 August – 20 September', '1 month + part = 2 × 1.5%', inr(i_b)],
              ['Total interest', '', inr(i_t)]], title='Section 398')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Chapter XIX of the Income-tax Act, 2025 collects tax as income arises. Section 392 covers TDS on salary at average rates; section 393 consolidates other TDS in tables — Table 1 for residents (393(1)), Table 2 for non-residents (393(2)) and Table 3 for others (393(3)) — with exemptions in 393(4). Section 394 covers TCS.',
            'Tax is generally deducted on the earlier of crediting the payee and paying him (subject to specific rules), and deposited within prescribed time. Deductors obtain TAN (section 397), file quarterly statements and issue certificates; payees claim credit through Form 26AS/AIS.',
            'A "specified person" (non-individuals, and individuals/HUFs with prior-year business turnover above ₹1 crore or professional receipts above ₹50 lakh) is liable to deduct under several entries; other individuals deduct only under specific ones (e.g. high rent, property purchase).'],
          'Deduct when you pay or credit, deposit on time, report quarterly.',
          'A salaried individual buying a flat for ₹60 lakh must deduct 1% though not otherwise a deductor.'),
        C('c2', T2, [
            'Common entries: insurance commission (2% individuals, 10% companies); rent — 2% where payer is not a specified person and rent exceeds ₹50,000 a month, and for specified persons 2% on plant and machinery or 10% on land and buildings; 1% on purchase of immovable property of ₹50 lakh or more (using the higher of consideration and stamp value).',
            'Contractors: 1% (individual/HUF) or 2% (others) above ₹30,000 per payment or ₹1,00,000 aggregate; professional fees, royalty and non-compete fees 10% and fees for technical services or call centres 2% above ₹50,000; directors\' remuneration 10% with no threshold; dividends 10% above ₹10,000 to individuals by non-cash modes; bank interest 10% above ₹50,000 (₹1,00,000 for senior citizens); interest by others 10% above ₹10,000.',
            'Purchase of goods: buyers with prior-year turnover above ₹10 crore deduct 0.1% on purchases from a seller exceeding ₹50 lakh. VDA transfers: 1%. Lottery winnings 30%. Life insurance payouts: 2% on the income component.'],
          'Know the payer, the rate and the threshold.',
          'Office rent of ₹70,000 a month paid by a company bears 10% TDS.'),
        C('c3', T3, [
            'Section 394 makes sellers collect tax: on scrap, tendu leaves, forest produce and minerals at specified rates; and 1% on sale of a motor vehicle or notified luxury goods (watches, art, yachts, designer bags and others) worth more than ₹10 lakh each.',
            'Authorised dealers collect TCS on LRS remittances above ₹10 lakh in aggregate: 2% for education or medical treatment and 20% for other purposes; none where remittance is out of an education loan from a financial institution. Sellers of overseas tour packages collect 2%.',
            'TCS is collected at the time of debit or receipt, whichever is earlier, and is credited to the buyer\'s tax account.'],
          'Sellers and dealers collect tax at source on specified receipts.',
          'A car sold for ₹12 lakh attracts TCS of ₹12,000.'),
        C('c4', T4, [
            'A payer who fails to deduct or pay is an assessee in default (section 398) — unless the payee has filed a return, included the income and paid tax, certified by an accountant. Interest is 1% a month from when tax was deductible to deduction, and 1.5% a month from deduction to payment.',
            'Non-furnishing of PAN (section 397) means deduction at the higher of the specified rate and 20% (with specific caps for some items), and TCS at the higher of twice the rate and 5% (max 20%). For specified non-filers, higher TDS/TCS rates may apply.',
            'Expenditure where TDS is not deducted suffers disallowance — 30% for resident payments and full disallowance for non-resident payments — until the tax is paid.'],
          'Defaults cost interest, disallowance and possibly penalty.',
          'A two-month delay in deducting ₹20,000 costs ₹400 of interest.'),
        C('c5', T5, [
            'Advance tax is payable where estimated tax after TDS/TCS is ₹10,000 or more: 15%, 45%, 75% and 100% by 15 June, 15 September, 15 December and 15 March. Presumptive taxpayers under section 58 may pay the whole by 15 March. Resident senior citizens with no business income are exempt.',
            'Interest is charged for default in payment of advance tax and for deferment of instalments; self-assessment tax with interest is payable before filing the return.',
            'Recovery provisions allow the AO and TRO to attach bank accounts and property, recover from debtors and from directors of private companies in specified cases.'],
          'Pay as you earn, quarter by quarter.',
          'A consultant with estimated tax of ₹2 lakh pays ₹30,000 by 15 June.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Monthly TDS review', 'role': 'Accounts manager',
             'situation': 'The company\'s vendor payments for the month need TDS checks.',
             'steps': ['Classify each payment by table entry.', 'Check thresholds and PAN status.', 'Deposit by due date.', 'Reconcile with quarterly statement.'],
             'takeaway': 'Classification errors are the commonest TDS defaults.'}]

    mcqs = [
        Q('m1', 'TDS on a contractor (individual) applies when aggregate payments in the year exceed:', ['One lakh rupees', 'Thirty thousand rupees', 'Fifty thousand rupees', 'Two lakh rupees'], 0,
          'Or ₹30,000 single payment. In practice: 1%.', 'c2', T2),
        Q('m2', 'TDS rate on purchase of immovable property of ₹50 lakh or more is:', ['One percent', 'Two percent', 'Ten percent', 'Zero point one percent'], 0,
          'Higher of consideration and stamp value. In practice: no TAN needed for individuals.', 'c2', T2),
        Q('m3', 'Bank interest to a senior citizen attracts TDS only above:', ['One lakh rupees', 'Fifty thousand rupees', 'Ten thousand rupees', 'Forty thousand rupees'], 0,
          'Threshold for seniors. In practice: others ₹50,000.', 'c2', T2),
        Q('m4', 'TCS on sale of a motor car worth more than ₹10 lakh is:', ['One percent', 'Two percent', 'Five percent', 'Zero point one percent'], 0,
          'Per vehicle. In practice: credited to buyer.', 'c3', T3),
        Q('m5', 'TCS on LRS remittance above ₹10 lakh for investment is:', ['Twenty percent', 'Two percent', 'Five percent', 'Ten percent'], 0,
          'Non-education, non-medical. In practice: credit in return.', 'c3', T3),
        Q('m6', 'Interest from date of deduction to date of payment of TDS is:', ['One and a half percent per month', 'One percent per month', 'Two percent per month', 'Twelve percent per year'], 0,
          'Section 398. In practice: month or part.', 'c4', T4),
        Q('m7', 'If PAN is not furnished, TDS is generally at the higher of the normal rate and:', ['Twenty percent', 'Ten percent', 'Thirty percent', 'Five percent'], 0,
          'Section 397. In practice: TCS rule differs.', 'c4', T4),
        Q('m8', 'The first advance tax instalment (non-presumptive) is due by 15 June at:', ['Fifteen percent', 'Twenty-five percent', 'Forty-five percent', 'Ten percent'], 0,
          'Cumulative schedule. In practice: interest on shortfall.', 'c5', T5),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Contractor and fees', 3, 'computation', 'contractor', nums=[a]), S('s2', 'Rent', 3, 'computation', 'rent', nums=[c]), S('s3', 'Goods and total', 2, 'computation', 'goods', nums=[d, tot])],
          ['Cite table entries.'], ['Deducting on fees below ₹50,000.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Late deduction', 2, 'computation', '1%', nums=[i_a]), S('s2', 'Late payment', 2, 'computation', '1.5%', nums=[i_b, i_t])],
          ['Count part months.'], ['Using 1.5% for the whole period.'], ['Two periods.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Who is a specified person for TDS?', 'Any person other than an individual or HUF, and individuals or HUFs whose prior-year business turnover exceeded ₹1 crore or professional receipts ₹50 lakh.',
          [P('p1', 'Other than individual', 5, 'other than'), P('p2', 'Turnover limits', 5, '1 crore|50 lakh')], 'c1'),
        V('v2', 'When is a payer not an assessee in default despite not deducting?', 'When the payee has filed a return including the income and paid the tax, supported by an accountant\'s certificate.',
          [P('p1', 'Payee return', 5, 'return'), P('p2', 'Accountant certificate', 5, 'accountant')], 'c4'),
        V('v3', 'What is the TCS on an overseas tour package?', 'Two percent of the amount.',
          [P('p1', 'Two percent', 5, '2%|two percent'), P('p2', 'Amount', 5, 'amount')], 'c3'),
        V('v4', 'What disallowance follows non-deduction on a resident payment?', 'Thirty percent of the expense, allowed in the year the tax is paid.',
          [P('p1', 'Thirty percent', 5, '30%|thirty'), P('p2', 'Year paid', 5, 'paid')], 'c4'),
        V('v5', 'Who need not pay advance tax?', 'Resident senior citizens whose income is only from heads other than business or profession.',
          [P('p1', 'Senior citizens', 5, 'senior'), P('p2', 'Other heads', 5, 'other heads')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Dhillon family purchases', 'difficulty': 'core',
              'case': 'In T.Y. 2026-27 Amrit Dhillon buys a car for ₹14,00,000 and remits ₹18,00,000 under LRS to invest in foreign shares (no other LRS remittances). His daughter remits ₹6,00,000 for her university fees out of an education loan from a bank.',
              'mcqs': [
                  M('k1a', 'TCS on the car (₹):', ['14,000', '4,000', '28,000', 'Nil'], 0,
                    '1% × 14,00,000. In practice: whole amount.', 'core', check=14000, topic=T3),
                  M('k1b', 'TCS on the LRS remittance for investment (₹):', ['1,60,000', '3,60,000', '16,000', '36,000'], 0,
                    '20% × (18,00,000 − 10,00,000). In practice: credit claimable.', 'core', check=160000, topic=T3),
                  M('k1c', 'TCS on the daughter\'s loan-funded fee remittance (₹):', ['0', '12,000', '1,20,000', '6,000'], 0,
                    'Education loan exclusion. In practice: keep loan papers.', 'core', check=0, topic=T3),
                  M('k1d', 'How does Amrit use the TCS collected?', ['As credit against his tax liability', 'It is a final tax', 'It is refunded to the seller', 'It is lost'], 0,
                    'Credit in return. In practice: verify in AIS.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch13', 1, 'Deduction, Collection and Recovery of Tax',
                ['Describe the TDS framework under sections 392 to 398.',
                 'Apply key TDS rates and thresholds for residents.',
                 'Apply TCS provisions.',
                 'Compute consequences of default and higher rates.',
                 'Apply advance tax and recovery provisions.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 50, 'practice': 35}, 'prereq': ['fin-p4-ch12-u01'],
                 'exam_tip': 'For each payment state payer status, table entry, threshold and rate in one line.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 392 salary; 393 tables; 394 TCS.', 'Rent 2%/10%; property 1%; contractors 1%/2%; professional 10%.', 'TCS: car 1%, LRS 2%/20%, tour 2%.',
                             'Section 398: 1% and 1.5% interest.', 'Advance tax 15/45/75/100.'],
                 'remember': ['PAN missing: at least 20% TDS.'],
                 'traps': ['Deducting TDS on goods below ₹50 lakh.']},
                [('Salary TDS', 'Section 392'), ('Other TDS', 'Section 393'), ('TCS', 'Section 394'), ('PAN', 'Section 397'), ('Default', 'Section 398')],
                viva, cases)
