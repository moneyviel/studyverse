"""CA Final · Paper 4 · Chapter 20 Tax Audit and Ethical Compliances.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch20-u01'
T1 = 'Applicability of tax audit'
T2 = 'Form No. 26 and the auditor\'s approach'
T3 = 'Key reporting clauses'
T4 = 'Fees, penalties and professional ethics'


def build():
    ck = Checks()
    a = ck.add('80000000', 'Turnover of trader A (₹)')
    b = ck.add('120000000', 'Turnover of trader B (₹)')
    d = ck.add('15000000*0.20', 'Cash receipts of trader D (₹)')
    i1 = {'id': 'i1', 'title': 'Who needs a tax audit?', 'difficulty': 'core', 'minutes': 7,
          'q': 'For T.Y. 2026-27 determine whether tax audit applies: (A) trader with turnover ₹8 crore, cash receipts 3% and cash payments 4%; (B) trader with turnover ₹12 crore and the same cash ratios; (C) doctor with gross receipts ₹60 lakh declaring actual profit; (D) trader with turnover ₹1.5 crore and 20% cash receipts.',
          'solution': [table(['Case', 'Reason', 'Audit?'], [
              ['A', f'₹{inr(a)} ≤ ₹10 crore and both cash ratios ≤ 5%', 'No'],
              ['B', f'₹{inr(b)} exceeds ₹10 crore', 'Yes'],
              ['C', 'Professional receipts exceed ₹50 lakh; not on presumptive basis', 'Yes'],
              ['D', f'Above ₹1 crore and cash receipts ₹{inr(d)} exceed 5%', 'Yes']], title='Section 63')],
          'checks': list(ck)}

    c2 = Checks()
    f1 = c2.add('75000', 'Fee for delay up to one month (₹)')
    f2 = c2.add('150000', 'Fee for delay beyond one month (₹)')
    i2 = {'id': 'i2', 'title': 'Fees for late audit report', 'difficulty': 'core', 'minutes': 4,
          'q': 'Two assessees required to furnish tax audit reports by the specified date furnish them (a) 20 days late and (b) two months late. Compute the fees under section 428(c).',
          'solution': [table(['Case', 'Delay', '₹'], [
              ['(a)', 'Up to one month', inr(f1)],
              ['(b)', 'Beyond one month', inr(f2)]], title='Section 428(c)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 63 requires accounts to be audited by a chartered accountant where business turnover exceeds ₹1 crore in the tax year — raised to ₹10 crore if cash receipts and cash payments each do not exceed 5% (non-account-payee cheques and drafts count as cash) — or professional gross receipts exceed ₹50 lakh.',
            'Persons eligible for presumptive taxation under sections 58(2) or 61(2) who claim profits lower than the deemed profits (and whose income exceeds the basic exemption limit) must also get audited; those declaring presumptive income need not.',
            'The audit must be completed and the report furnished one month before the due date of the return (the specified date). Other reports by CAs include those for RNPOs (Form 112), section 46 and Part C deductions (Form 32), MAT (Form 66) and AMT (Form 67).'],
          'Turnover, cash and presumptive choices decide audit applicability.',
          'A trader with ₹8 crore turnover and minimal cash need not be audited.'),
        C('c2', T2, [
            'Form No. 26 has four parts: Part A where accounts are audited under another law (e.g. Companies Act), Part B for other persons, and Parts C and D containing the particulars common to all, such as nature of business, method of accounting, depreciation, disallowances, TDS compliance, loans and deposits, and quantitative details.',
            'Following the ICAI Guidance Note, the auditor should avoid duplicating information across clauses, state both viewpoints where he differs with the assessee, apply the law of the relevant year even if the form lags, and qualify the report rather than withhold it where information is incomplete.',
            'The auditor reports whether particulars in Part D are true and correct, giving qualifications where necessary.'],
          'Report fairly, qualify where needed, never withhold.',
          'If the client refuses to share a related-party list, the auditor qualifies the report.'),
        C('c3', T3, [
            'Key clauses include: amounts inadmissible under sections 35 and 36 (including TDS defaults and cash payments above ₹10,000), sums covered by section 37 paid or not paid within time, deemed dividends under section 2(40)(e), loans and deposits taken or repaid in cash (sections 185 and 188), and receipts covered by section 186.',
            'Other clauses cover depreciation by blocks, brought-forward losses and shareholding changes, TDS and TCS compliance (with reference to quarterly statements), statements of financial transactions, penalties or fines for violations of law, and principal items of goods traded or manufactured (items above about 10% of value).',
            'The auditor must verify each item with evidence and, where he cannot verify, state so specifically.'],
          'Clauses mirror the Act\'s disallowances and compliance rules.',
          'An unpaid March bonus not paid before the return date is reported under the section 37 clause.'),
        C('c4', T4, [
            'Section 428(c): failure to furnish the tax audit report as required attracts a fee of ₹75,000 for delay up to one month and ₹1,50,000 beyond that.',
            'Section 463: an accountant furnishing incorrect information in any report or certificate under the Act or Rules is liable to a penalty of ₹10,000 per report.',
            'Under the Chartered Accountants Act, a CA in practice is guilty of professional misconduct if he accepts more tax audit assignments than the ICAI-specified limit (60 per partner per year, excluding specified presumptive cases), fails to report material misstatements, is grossly negligent or certifies without verification.'],
          'Late reports cost fees; careless reports cost auditors.',
          'A report filed 20 days late attracts a fee of ₹75,000.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Tax audit planning', 'role': 'Audit senior',
             'situation': 'A new client with ₹15 crore turnover appoints the firm.',
             'steps': ['Confirm applicability and specified date.', 'Check partner\'s audit-count limit.', 'Plan verification of Part D clauses.', 'Draft qualifications where data is missing.'],
             'takeaway': 'Planning early avoids fees and qualified reports.'}]

    mcqs = [
        Q('m1', 'Tax audit is required for a business with turnover above ₹1 crore unless cash ratios are within 5% and turnover does not exceed:', ['Ten crore rupees', 'Five crore rupees', 'Three crore rupees', 'Two crore rupees'], 0,
          'Section 63(1). In practice: both conditions.', 'c1', T1),
        Q('m2', 'Tax audit for professionals applies when gross receipts exceed:', ['Fifty lakh rupees', 'Seventy-five lakh rupees', 'One crore rupees', 'Twenty-five lakh rupees'], 0,
          'Section 63(1)(ii). In practice: presumptive alternative.', 'c1', T1),
        Q('m3', 'Tax audit report must be furnished:', ['One month before the return due date', 'On the return due date', 'Within six months of year-end', 'Any time before assessment'], 0,
          'Specified date. In practice: plan early.', 'c1', T1),
        Q('m4', 'Part A of Form No. 26 applies where:', ['Accounts are audited under another law', 'The assessee is an individual', 'Turnover is below ₹1 crore', 'The assessee is non-resident'], 0,
          'Companies and LLPs. In practice: Part B otherwise.', 'c2', T2),
        Q('m5', 'Where information is incomplete, the auditor should:', ['Qualify the report', 'Withhold the report', 'Resign', 'Report nil'], 0,
          'Guidance Note. In practice: specify items.', 'c2', T2),
        Q('m6', 'Fee for furnishing the audit report more than one month late is:', ['One lakh fifty thousand rupees', 'Seventy-five thousand rupees', 'Ten thousand rupees', 'Half percent of turnover'], 0,
          'Section 428(c). In practice: per year.', 'c4', T4),
        Q('m7', 'Penalty on an accountant for incorrect information in a report is:', ['Ten thousand rupees per report', 'One lakh rupees', 'Fifty thousand rupees', 'Nil'], 0,
          'Section 463. In practice: plus disciplinary action.', 'c4', T4),
        Q('m8', 'The ICAI limit on tax audits per partner per year is:', ['Sixty', 'Forty', 'Thirty', 'One hundred'], 0,
          'Ethical guideline. In practice: presumptive audits excluded.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Business cases', 4, 'analysis', '10 crore', nums=[a, b, d]), S('s2', 'Professional case', 2, 'analysis', '50 lakh')],
          ['Test both cash ratios.'], ['Ignoring the ₹10 crore ceiling.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Fees', 3, 'computation', 'fee', nums=[f1, f2])],
          ['Cite section.'], ['Using the old percentage penalty.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Is a non-account-payee cheque treated as cash for the 5% test?', 'Yes, receipts or payments by non-account-payee cheques or drafts are deemed cash.',
          [P('p1', 'Deemed cash', 5, 'deemed cash'), P('p2', 'Non-account-payee', 5, 'non-account-payee')], 'c1'),
        V('v2', 'What should an auditor do when he disagrees with the assessee on a clause?', 'State both viewpoints with relevant information so the AO can decide.',
          [P('p1', 'Both viewpoints', 5, 'both viewpoints'), P('p2', 'AO decides', 5, 'decide')], 'c2'),
        V('v3', 'What are principal items for quantitative reporting?', 'Items normally forming more than about ten percent of the value of purchases, consumption or turnover.',
          [P('p1', 'Ten percent', 5, 'ten percent'), P('p2', 'Value', 5, 'value')], 'c3'),
        V('v4', 'Which presumptive assessees need audit?', 'Those claiming profits lower than the deemed rate, where income exceeds the basic exemption limit.',
          [P('p1', 'Lower profits', 5, 'lower'), P('p2', 'Deemed rate', 5, 'deemed')], 'c1'),
        V('v5', 'What fee applies for a report delayed by two weeks?', 'Seventy-five thousand rupees under section 428(c).',
          [P('p1', 'Seventy-five thousand', 5, 'seventy-five thousand'), P('p2', 'Section 428', 5, '428')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Audit findings at Ganga Agro', 'difficulty': 'moderate',
              'case': 'During tax audit of Ganga Agro Pvt Ltd, the auditor finds: cash payments of ₹15,000 each to a supplier on four days; a cash loan of ₹50,000 from a director; employees\' PF contribution for March remitted after the return due date; and a loan of ₹8 lakh to a 12% shareholder when reserves were ₹20 lakh.',
              'mcqs': [
                  M('k1a', 'Total cash payments to the supplier reportable as inadmissible (₹):', ['60,000', '15,000', '45,000', 'Nil'], 0,
                    'Each day exceeds ₹10,000. In practice: section 36(4).', 'core', check=60000, topic=T3),
                  M('k1b', 'The cash loan from the director is reportable under:', ['Section 185', 'Section 186', 'Section 188', 'Section 187'], 0,
                    'Loan of ₹20,000 or more. In practice: penalty exposure.', 'core', topic=T3),
                  M('k1c', 'The loan to the 12% shareholder is reportable as deemed dividend of (₹):', ['8,00,000', '20,00,000', '96,000', 'Nil'], 0,
                    'Within accumulated profits. In practice: section 2(40)(e).', 'core', check=800000, topic=T3),
                  M('k1d', 'The late PF remittance is reported as:', ['Inadmissible for the year', 'Fully allowable', 'Capital expenditure', 'Prior-period item'], 0,
                    'Employee contributions. In practice: deposit by due date.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch20', 1, 'Tax Audit and Ethical Compliances',
                ['Determine applicability of tax audit.',
                 'Apply Form No. 26 structure and the auditor\'s approach.',
                 'Report key disallowances and compliance items.',
                 'Apply fees, penalties and ethical limits.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 20}, 'prereq': ['fin-p4-ch19-u01'],
                 'exam_tip': 'Link each audit clause to the section it tests, and state how it affects income.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 63: ₹1 crore / ₹10 crore with 5% cash; ₹50 lakh for professions.', 'Specified date: one month before return due date.', 'Form No. 26 Parts A–D.',
                             'Fee u/s 428(c): ₹75,000 / ₹1,50,000.', 'Section 463: ₹10,000 per incorrect report; 60-audit limit.'],
                 'remember': ['Qualify, do not withhold.'],
                 'traps': ['Applying the ₹10 crore limit without checking cash payments too.']},
                [('Tax audit', 'Section 63'), ('Audit report', 'Form No. 26'), ('Fee for default', 'Section 428(c)'), ('Incorrect report', 'Section 463')],
                viva, cases)
