"""CA Final · Paper 5 · Chapter 15 Refunds.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch15-u01'
T1 = 'Situations and time limit for refund'
T2 = 'Refund of unutilised ITC — exports and inverted duty'
T3 = 'Procedure, provisional refund and withholding'
T4 = 'Unjust enrichment, interest and Consumer Welfare Fund'


def build():
    ck = Checks()
    r = ck.add('6000000*900000/10000000', 'Refund under rule 89(4) (₹)')
    p = ck.add('6000000*900000/10000000*0.90', 'Provisional refund at 90% (₹)')
    i1 = {'id': 'i1', 'title': 'Refund on exports under LUT', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Tanya Exports made zero-rated supplies of goods under LUT of ₹60,00,000 and domestic supplies of ₹40,00,000 in a quarter. Net ITC on inputs and input services was ₹9,00,000. Compute the refund and the provisional amount.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Adjusted total turnover', '60,00,000 + 40,00,000', '1,00,00,000'],
              ['Refund', 'Zero-rated turnover × Net ITC ÷ ATT', inr(r)],
              ['Provisional refund', '90% within 7 days of acknowledgement', inr(p)]], title='Rule 89(4) and section 54(6)')],
          'checks': list(ck)}

    c2 = Checks()
    m = c2.add('round(10000000*1200000/10000000-500000*1200000/1400000,2)', 'Maximum refund under inverted duty formula (₹)')
    i2 = {'id': 'i2', 'title': 'Inverted duty structure', 'difficulty': 'hard', 'minutes': 9,
          'q': 'Pankaj Fabrics sells fabric taxed at 5% (turnover ₹1,00,00,000; tax payable ₹5,00,000). Inputs (yarn, chemicals) attract higher rates; Net ITC on inputs is ₹12,00,000; total ITC on inputs and input services is ₹14,00,000. Adjusted total turnover is ₹1,00,00,000. Compute the maximum refund.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Part A', 'Turnover of inverted rated supply × Net ITC ÷ ATT = 1 crore × 12 lakh ÷ 1 crore', '12,00,000'],
              ['Part B', 'Tax payable × (Net ITC ÷ ITC on inputs and input services) = 5,00,000 × 12/14', '4,28,571.43'],
              ['Maximum refund', 'A − B', f'{m}']], title='Rule 89(5)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 54 allows refund of tax, interest or other amounts, including excess balance in the cash ledger, tax on zero-rated supplies, unutilised ITC on exports without tax or on inverted duty structure, tax on deemed exports, tax paid on supplies not provided, wrongly paid tax under section 77, and tax on supplies to UN bodies and embassies.',
            'Refund of unutilised ITC is barred where goods exported are subject to export duty, or where the supplier claims drawback of central tax. Inverted duty refund is not available for notified goods or services.',
            'An application in RFD-01 must be filed within two years from the relevant date — e.g. date of shipment for goods exports, date of receipt of payment for services exports, due date of return for inverted duty claims. The two-year limit does not apply to excess balance in the cash ledger.'],
          'Refund is available in listed situations within two years.',
          'An exporter of goods files for refund within two years of the shipping date.'),
        C('c2', T2, [
            'Rule 89(4) for zero-rated supplies without tax: refund equals Net ITC multiplied by the share that zero-rated turnover forms of adjusted total turnover. Zero-rated goods turnover is capped at 1.5 times the value of like goods supplied domestically.',
            'Rule 89(5) for inverted duty: maximum refund = (turnover of inverted rated supply × Net ITC ÷ adjusted total turnover) − (tax payable on such supply × Net ITC ÷ ITC on inputs and input services). Net ITC here covers inputs only, not input services or capital goods.',
            'Credit used for computing the refund is debited from the credit ledger and restored if the claim is rejected.'],
          'Formulas share refund by turnover proportion.',
          'Exports of ₹60 lakh out of ₹1 crore turnover with ₹9 lakh ITC yield ₹5.4 lakh refund.'),
        C('c3', T3, [
            'The proper officer acknowledges a complete application within 15 days and decides within 60 days of receipt. For zero-rated supplies, 90% is refunded provisionally within 7 days of acknowledgement, unless the applicant was prosecuted for a specified offence in the preceding five years.',
            'Refunds below ₹1,000 are not paid. IGST paid on exported goods is refunded automatically once the shipping bill and GSTR-3B are validated, treating the shipping bill as the application.',
            'Section 54(10)–(12): refund can be withheld or adjusted against unpaid demands, or withheld where an appeal is pending and fraud is suspected — with 6% interest payable if the taxpayer ultimately succeeds.'],
          'Fast provisional refunds for exporters; safeguards for revenue.',
          'An exporter receives 90% of its refund within a week.'),
        C('c4', T4, [
            'Unjust enrichment: refund is paid to the applicant only if the incidence of tax has not been passed on; otherwise it goes to the Consumer Welfare Fund (section 57). Exceptions where it is paid to the applicant include exports, deemed exports, unutilised ITC, tax on supplies not made, and wrongly paid tax under section 77.',
            'For claims above ₹2 lakh, a CA or cost accountant certificate that incidence has not been passed on is required; for smaller claims, a self-declaration suffices. Every amount of tax paid is presumed passed on unless proved otherwise.',
            'Section 56: interest at 6% per annum is payable if refund is not paid within 60 days of receipt of the application; 9% where refund arises from an appellate order and is paid more than 60 days after the application consequent to that order.'],
          'No double benefit — unjust enrichment goes to consumers.',
          'A refund delayed beyond 60 days earns 6% interest.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Refund claim preparation', 'role': 'GST associate',
             'situation': 'A textile exporter has both export and inverted duty credits.',
             'steps': ['Classify claims by type and relevant date.', 'Compute refund using rule 89(4) and 89(5).', 'Prepare CA certificate if above ₹2 lakh.', 'Track 60-day processing and interest.'],
             'takeaway': 'Correct relevant dates prevent time-barred claims.'}]

    mcqs = [
        Q('m1', 'Refund application must be filed within how long from the relevant date?', ['Two years', 'One year', 'Three years', 'Six months'], 0,
          'Section 54(1). In practice: cash ledger excess excluded.', 'c1', T1),
        Q('m2', 'Relevant date for export of services refund is:', ['Date of receipt of payment in foreign exchange', 'Invoice date', 'Shipping bill date', 'Return due date'], 0,
          'Explanation to section 54. In practice: or invoice if advance.', 'c1', T1),
        Q('m3', 'Provisional refund for zero-rated supplies is:', ['Ninety percent within seven days', 'Fifty percent within thirty days', 'Full within sixty days', 'Ten percent within seven days'], 0,
          'Section 54(6). In practice: rest after verification.', 'c3', T3),
        Q('m4', 'Refunds below which amount are not paid?', ['One thousand rupees', 'Five hundred rupees', 'Ten thousand rupees', 'One hundred rupees'], 0,
          'Section 54(14). In practice: minor amounts.', 'c3', T3),
        Q('m5', 'Net ITC for inverted duty refund includes:', ['ITC on inputs only', 'ITC on capital goods', 'ITC on input services', 'All ITC'], 0,
          'Rule 89(5). In practice: services excluded.', 'c2', T2),
        Q('m6', 'A CA certificate on unjust enrichment is needed when refund exceeds:', ['Two lakh rupees', 'Five lakh rupees', 'One lakh rupees', 'Fifty thousand rupees'], 0,
          'Rule 89(2)(m). In practice: else self-declaration.', 'c4', T4),
        Q('m7', 'Interest on delayed refund beyond 60 days is:', ['Six percent per annum', 'Nine percent', 'Eighteen percent', 'Twelve percent'], 0,
          'Section 56. In practice: 9% for appellate orders.', 'c4', T4),
        Q('m8', 'Unjust-enrichment amounts are credited to the:', ['Consumer Welfare Fund', 'Consolidated Fund', 'Applicant', 'GST Council'], 0,
          'Section 57. In practice: used for consumers.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Refund', 3, 'computation', 'Net ITC', nums=[r]), S('s2', 'Provisional', 2, 'computation', '90%', nums=[p])],
          ['Show formula.'], ['Using total ITC for zero-rated share.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Part A', 2, 'computation', 'inverted'), S('s2', 'Part B and result', 4, 'computation', 'maximum refund', nums=[m])],
          ['Write rule 89(5).'], ['Including input services in Net ITC.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'When is refund of unutilised ITC on exports barred?', 'When exported goods suffer export duty or the supplier claims drawback of central tax.',
          [P('p1', 'Export duty', 5, 'export duty'), P('p2', 'Drawback', 5, 'drawback')], 'c1'),
        V('v2', 'What is the cap on turnover of zero-rated goods?', 'Value up to 1.5 times the domestic value of like goods supplied by the same or similar suppliers.',
          [P('p1', 'One and a half times', 5, '1.5'), P('p2', 'Domestic value', 5, 'domestic')], 'c2'),
        V('v3', 'How is IGST paid on exported goods refunded?', 'Automatically, with the shipping bill treated as the refund application once validated.',
          [P('p1', 'Shipping bill', 5, 'shipping bill'), P('p2', 'Automatically', 5, 'automatic')], 'c3'),
        V('v4', 'What is presumed about tax paid?', 'That its incidence has been passed on to the buyer unless proved otherwise.',
          [P('p1', 'Passed on', 5, 'passed on'), P('p2', 'Proved otherwise', 5, 'proved')], 'c4'),
        V('v5', 'When can refund be withheld with interest at 6%?', 'When an appeal is pending and the Commissioner believes grant may hurt revenue due to fraud; interest applies if the taxpayer later succeeds.',
          [P('p1', 'Appeal pending', 5, 'appeal'), P('p2', 'Fraud', 5, 'fraud')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Excess cash ledger balance', 'difficulty': 'core',
              'case': 'Ojas Ltd deposited ₹3,50,000 in its cash ledger in 2023 by mistake and wants it back in December 2026.',
              'mcqs': [
                  M('k1a', 'Is the claim time-barred under the two-year rule?', ['No, excess cash ledger balance is outside the two-year limit', 'Yes', 'Only partly', 'Only for IGST'], 0,
                    'Clarification. In practice: claim via return or RFD-01.', 'core', topic=T1),
                  M('k1b', 'Is unjust enrichment relevant?', ['No, tax was not passed on', 'Yes', 'Only above ₹2 lakh', 'Only for exports'], 0,
                    'Deposit not used as tax. In practice: certificate not needed.', 'core', topic=T4),
                  M('k1c', 'Refund amount (₹):', ['3,50,000', '3,15,000', 'Nil', '1,750'], 0,
                    'Full balance. In practice: subject to dues adjustment.', 'core', check=350000, topic=T1),
                  M('k1d', 'If paid after 60 days of application, interest rate (%):', ['6', '9', '18', '12'], 0,
                    'Section 56. In practice: from day 61.', 'core', check=6, topic=T4),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch15', 1, 'Refunds',
                ['Identify refund situations and time limits.',
                 'Compute refund of unutilised ITC on exports and inverted duty.',
                 'Apply procedure, provisional refund and withholding.',
                 'Apply unjust enrichment, interest and Consumer Welfare Fund.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 30}, 'prereq': ['fin-p5-ch14-u01'],
                 'exam_tip': 'Write the rule 89 formula before substituting numbers.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 54: situations; two years from relevant date.', 'Rule 89(4) exports; rule 89(5) inverted duty.', 'Provisional 90% in 7 days; decide in 60 days; < ₹1,000 not paid.',
                             'Unjust enrichment; CA certificate > ₹2 lakh; CWF.', 'Section 56: 6% / 9% interest.'],
                 'remember': ['Inverted duty Net ITC is inputs only.'],
                 'traps': ['Applying the two-year limit to cash ledger excess.']},
                [('Refund', 'Section 54'), ('Interest', 'Section 56'), ('CWF', 'Section 57'), ('Formulas', 'Rule 89')],
                viva, cases)
