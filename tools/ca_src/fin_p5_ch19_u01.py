"""CA Final · Paper 5 · Chapter 19 Demands and Recovery.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch19-u01'
T1 = 'Determination of tax under section 74A'
T2 = 'Penalty and its reduction'
T3 = 'General provisions on demands'
T4 = 'Recovery, instalments and provisional attachment'


def build():
    ck = Checks()
    nf = ck.add('max(800000*0.10,20000)', 'Non-fraud penalty under IGST (₹)')
    f1 = ck.add('800000*0.15', 'Fraud: penalty if paid before SCN at 15% (₹)')
    f2 = ck.add('800000*0.25', 'Fraud: penalty if paid within 60 days of SCN at 25% (₹)')
    f3 = ck.add('800000*0.50', 'Fraud: penalty if paid within 60 days of order at 50% (₹)')
    f4 = ck.add('800000*1.00', 'Fraud: full penalty (₹)')
    i1 = {'id': 'i1', 'title': 'Penalty under section 74A', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'An IGST short payment of ₹8,00,000 relating to FY 2025-26 is detected. Compute the penalty (a) in a non-fraud case and (b) in a fraud case where the taxpayer pays tax and interest (i) before SCN, (ii) within 60 days of SCN, (iii) within 60 days of the order, (iv) later.',
          'solution': [table(['Case', 'Rule', '₹'], [
              ['(a) Non-fraud', 'Higher of 10% of tax and ₹20,000 (IGST); nil if paid before SCN or within 60 days of SCN', inr(nf)],
              ['(b)(i) Fraud, before SCN', '15%', inr(f1)],
              ['(b)(ii) Fraud, within 60 days of SCN', '25%', inr(f2)],
              ['(b)(iii) Fraud, within 60 days of order', '50%', inr(f3)],
              ['(b)(iv) Fraud, otherwise', '100%', inr(f4)]], title='Section 74A')],
          'checks': list(ck)}

    c2 = Checks()
    sc = c2.add('42', 'Months from annual return due date to issue SCN')
    od = c2.add('12+6', 'Maximum months from SCN to issue order')
    i2 = {'id': 'i2', 'title': 'Time limits for a FY 2025-26 demand', 'difficulty': 'core', 'minutes': 6,
          'q': 'For FY 2025-26, the annual return was due on 31 December 2026. Determine the last date for the SCN and for the order if the SCN is issued on 1 March 2030.',
          'solution': [table(['Step', 'Rule', 'Date'], [
              ['SCN', f'{sc} months from due date of annual return', '30 June 2030'],
              ['Order', f'12 months from SCN, extendable by 6 (max {od})', '28 February 2031 (or 31 August 2031 if extended)'],
              ['Minimum', 'No SCN if amount below ₹1,000 a year', '—']], title='Section 74A(2) and (7)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'For FY 2024-25 onwards, section 74A replaces sections 73 and 74 with a single procedure for tax not paid, short paid, erroneously refunded, or ITC wrongly availed — whether or not fraud is involved. Sections 73 and 74 continue for periods up to FY 2023-24.',
            'The SCN must be issued within 42 months from the due date of the annual return (or date of erroneous refund) and the order within 12 months of the SCN, extendable by up to six months with recorded reasons. A statement for subsequent periods on the same grounds is treated as an SCN. No SCN is issued if the amount is below ₹1,000 in a financial year.',
            'A pre-SCN intimation (DRC-01A) gives the taxpayer a chance to pay and close the matter.'],
          'One section, one timeline, two penalty tracks.',
          'A FY 2025-26 demand needs an SCN by 30 June 2030.'),
        C('c2', T2, [
            'Non-fraud cases: penalty is the higher of 10% of tax and ₹10,000 (₹20,000 under IGST); waived if tax and interest are paid before SCN or within 60 days of it.',
            'Fraud, wilful misstatement or suppression cases: penalty equal to tax, reduced to 15% if tax, interest and penalty are paid before SCN, 25% if within 60 days of SCN, and 50% if within 60 days of the order.',
            'Self-assessed tax or tax collected but not paid within 30 days of the due date attracts the non-fraud penalty compulsorily, without the waiver option.'],
          'Paying early cuts penalties sharply.',
          'In a fraud case, paying within 60 days of SCN reduces penalty from 100% to 25%.'),
        C('c3', T3, [
            'Section 75: where the demand under fraud is not sustained for want of fraud, it is redetermined as non-fraud; a hearing must be given if requested or adverse action is proposed, with up to three adjournments; the order cannot exceed the SCN amount or grounds; interest is payable whether or not mentioned.',
            'Where a court or tribunal sets aside an order on limitation grounds, or periods are stayed by courts, those periods are excluded in computing limitation. Penalty is not imposed separately for the same act under different provisions.',
            'Section 76: whoever collects money from customers in the name of tax must deposit it with the Government, with interest and penalty, even if the supply itself was not taxable.'],
          'Procedural safeguards bind the adjudicating officer.',
          'An order cannot demand more than the amount in the SCN.'),
        C('c4', T4, [
            'Section 78: amounts under an order are payable within three months of service, or a shorter period if revenue so requires. Section 79 recovery modes: deduction from refunds or amounts owed by the Government, detention and sale of goods, garnishee notices to debtors or banks, distraint and sale of movable or immovable property, recovery as arrears of land revenue, and through a magistrate.',
            'Section 80: the Commissioner may allow payment of amounts (other than self-assessed tax) in up to 24 monthly instalments with interest; default in any instalment makes the balance payable at once. Section 81 voids transfers made to defraud revenue during pending proceedings.',
            'Section 83: the Commissioner may provisionally attach property, including bank accounts, during proceedings to protect revenue; the attachment lapses after one year from the order.'],
          'Recovery is backed by strong powers, softened by instalments.',
          'A demand can be paid in up to 24 instalments with interest.'),
    ]

    jobs = [{'id': 'j1', 'title': 'SCN response strategy', 'role': 'GST litigation associate',
             'situation': 'A client receives a DRC-01A pre-SCN intimation.',
             'steps': ['Check limitation under section 74A.', 'Evaluate fraud allegation strength.', 'Compare penalty savings from early payment.', 'Reply or pay and close the matter.'],
             'takeaway': 'Timing of payment decides the penalty bill.'}]

    mcqs = [
        Q('m1', 'Section 74A applies to tax for periods from:', ['FY 2024-25 onwards', 'FY 2017-18 onwards', 'FY 2026-27 only', 'FY 2023-24 only'], 0,
          'Unified procedure. In practice: 73/74 for earlier.', 'c1', T1),
        Q('m2', 'SCN under section 74A must be issued within:', ['Forty-two months from annual return due date', 'Three years', 'Five years', 'Thirty months'], 0,
          'Section 74A(2). In practice: also from erroneous refund.', 'c1', T1),
        Q('m3', 'Order under section 74A must be issued within:', ['Twelve months of SCN, extendable by six', 'Six months', 'Two years', 'Three months'], 0,
          'Section 74A(7). In practice: reasons recorded.', 'c1', T1),
        Q('m4', 'Non-fraud penalty under CGST is the higher of 10% of tax and:', ['Ten thousand rupees', 'Twenty thousand rupees', 'Five thousand rupees', 'One lakh rupees'], 0,
          'Section 74A(5). In practice: IGST ₹20,000.', 'c2', T2),
        Q('m5', 'In fraud cases, penalty if paid within 60 days of SCN is:', ['Twenty-five percent', 'Fifteen percent', 'Fifty percent', 'Nil'], 0,
          'Section 74A(9). In practice: with tax and interest.', 'c2', T2),
        Q('m6', 'Amounts due under an order must be paid within:', ['Three months of service', 'Thirty days', 'One year', 'Seven days'], 0,
          'Section 78. In practice: shorter if revenue at risk.', 'c4', T4),
        Q('m7', 'Maximum monthly instalments under section 80:', ['Twenty-four', 'Twelve', 'Thirty-six', 'Six'], 0,
          'Rule 158. In practice: not for self-assessed tax.', 'c4', T4),
        Q('m8', 'Provisional attachment under section 83 lapses after:', ['One year from the order', 'Six months', 'Three years', 'Ninety days'], 0,
          'Section 83(2). In practice: fresh order needed.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Non-fraud', 2, 'computation', '10%', nums=[nf]), S('s2', 'Fraud slabs', 4, 'computation', 'fraud', nums=[f1, f2, f3, f4])],
          ['Show each stage.'], ['Using ₹10,000 minimum for IGST.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'SCN date', 2, 'analysis', '42 months', nums=[sc]), S('s2', 'Order date', 2, 'analysis', '12 months', nums=[od])],
          ['Count from annual return due date.'], ['Counting from end of financial year.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What happens if fraud is not established in a fraud SCN?', 'The demand is redetermined as a non-fraud case under section 75(2).',
          [P('p1', 'Redetermined', 5, 'redetermin'), P('p2', 'Non-fraud', 5, 'non-fraud')], 'c3'),
        V('v2', 'How many adjournments are allowed?', 'Up to three adjournments during proceedings.',
          [P('p1', 'Three', 5, 'three'), P('p2', 'Adjournments', 5, 'adjournment')], 'c3'),
        V('v3', 'What is a garnishee notice?', 'A notice requiring a debtor or bank of the defaulter to pay amounts owed directly to the Government.',
          [P('p1', 'Debtor', 5, 'debtor'), P('p2', 'Pay to Government', 5, 'government')], 'c4'),
        V('v4', 'When is the non-fraud penalty compulsory?', 'Where self-assessed tax or tax collected is unpaid beyond 30 days of the due date.',
          [P('p1', 'Self-assessed', 5, 'self-assessed'), P('p2', 'Thirty days', 5, '30 days')], 'c2'),
        V('v5', 'What does section 76 require?', 'Money collected from customers in the name of tax must be deposited with the Government, with interest and penalty.',
          [P('p1', 'Collected', 5, 'collected'), P('p2', 'Deposited', 5, 'deposited')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Suppressed turnover', 'difficulty': 'moderate',
              'case': 'Ganesh Traders suppressed turnover for FY 2025-26, short-paying CGST ₹3,00,000 and SGST ₹3,00,000. It pays tax, interest and penalty within 60 days of the SCN.',
              'mcqs': [
                  M('k1a', 'Total tax short paid (₹):', ['6,00,000', '3,00,000', '9,00,000', '1,50,000'], 0,
                    'CGST + SGST. In practice: plus interest.', 'core', check=600000, topic=T1),
                  M('k1b', 'Penalty rate applicable (%):', ['25', '15', '50', '100'], 0,
                    'Fraud, within 60 days of SCN. In practice: section 74A(9).', 'core', check=25, topic=T2),
                  M('k1c', 'Total penalty payable (₹):', ['1,50,000', '90,000', '3,00,000', '6,00,000'], 0,
                    '25% × 6 lakh. In practice: proceedings concluded.', 'core', check=150000, topic=T2),
                  M('k1d', 'After payment, proceedings are:', ['Deemed concluded except for other noticees', 'Continued', 'Transferred to court', 'Reopened'], 0,
                    'Section 74A(10). In practice: co-noticees separate.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch19', 1, 'Demands and Recovery',
                ['Apply section 74A for determination of tax.',
                 'Compute penalties and reductions.',
                 'Apply general provisions on demands.',
                 'Apply recovery, instalments and provisional attachment.'],
                {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p5-ch18-u01'],
                 'exam_tip': 'Identify period (pre or post FY 2024-25), then fraud or non-fraud, then payment timing.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 74A from FY 2024-25: SCN 42 months; order 12 + 6 months.', 'Non-fraud: higher of 10% and ₹10,000; waived if paid early.', 'Fraud: 100%, reduced to 15%/25%/50%.',
                             'Section 75 safeguards; 76 tax collected not paid.', 'Sections 78–83: recovery in 3 months; 24 instalments; attachment one year.'],
                 'remember': ['No SCN below ₹1,000 a year.'],
                 'traps': ['Applying section 73/74 to FY 2025-26.']},
                [('Demand', 'Section 74A'), ('General provisions', 'Section 75'), ('Recovery', 'Section 79'), ('Instalments', 'Section 80'), ('Attachment', 'Section 83')],
                viva, cases)
