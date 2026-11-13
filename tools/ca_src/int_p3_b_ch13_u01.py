"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 13 Payment of Tax.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch13-u01'
T1 = 'Electronic ledgers and modes of payment (s. 49)'
T2 = 'Order of discharge and due dates'
T3 = 'Interest on delayed payment (s. 50)'


def build():
    ck = Checks()
    i_late = ck.add('round(40000*18/100*30/365)', 'Interest on cash portion paid 30 days late')
    i_itc = ck.add('round(25000*18/100*73/365)', 'Interest on ITC wrongly availed and utilised, 73 days')
    i1 = {'id': 'i1', 'title': 'Paying late', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'For a month, Kavi Industries (monthly filer) had output tax of ₹1,00,000, of which ₹60,000 was set off by ITC and ₹40,000 was payable in cash. It filed GSTR-3B and paid 30 days after the due date. Separately, it had wrongly availed and used ITC of ₹25,000, reversed 73 days later. Compute interest (round to the nearest rupee).',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Late payment', '18% on the cash portion only: 40,000 × 18% × 30/365', inr(i_late)],
              ['Wrong ITC availed and utilised', '18% (notified rate): 25,000 × 18% × 73/365', inr(i_itc)]], title='Section 50'),
              note('Interest on late payment is on the net cash liability where the return is filed before any proceedings begin.')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Which ledger pays what?', 'difficulty': 'core', 'minutes': 5,
          'q': 'State which ledger can be used: (a) output IGST for the month; (b) reverse charge tax on legal fees; (c) interest under section 50; (d) late fee for GSTR-3B; (e) a penalty imposed by the officer.',
          'solution': [table(['Item', 'Ledger'], [
              ['(a)', 'Electronic credit ledger or cash ledger'],
              ['(b)', 'Electronic cash ledger only'],
              ['(c)', 'Electronic cash ledger only'],
              ['(d)', 'Electronic cash ledger only'],
              ['(e)', 'Electronic cash ledger only']], title='Section 49'),
              note('The credit ledger is used only for output tax under forward charge (and output tax payable by ECOs as suppliers).')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Each registered person has three electronic records on the portal: the cash ledger (deposits), the credit ledger (ITC) and the liability register (all dues).',
            'Deposits into the cash ledger use a challan (valid 15 days) paid by internet banking, debit or credit card, NEFT/RTGS, UPI or over the counter (up to ₹10,000 per challan per period); the date of credit to the Government account is the date of deposit.',
            'The cash ledger pays tax, interest, penalty, fees and other amounts; the credit ledger pays only output tax. Amounts can be transferred between heads in the cash ledger and, for CGST and IGST, to a distinct person with the same PAN. Unused balances in the cash ledger can be refunded.'],
          'Cash is the universal key; credit opens only the output-tax door.',
          'A trader with ₹5 lakh of ITC must still pay a ₹2,000 late fee in cash.'),
        C('c2', T2, [
            'Section 49(8) order: first, self-assessed tax and other dues for previous periods; then the current period; then any amount payable under a demand (sections 73 or 74).',
            'Due dates: monthly filers pay by the 20th of the next month with GSTR-3B. Quarterly (QRMP) filers pay for the first two months by the 25th of the following month (either 35% of last quarter\'s cash tax, or actual tax), and for the quarter with GSTR-3B by the 22nd or 24th depending on the State.',
            'Reverse charge tax is paid in cash. TDS and TCS deducted by others are credited to the cash ledger of the supplier once accepted.'],
          'Old dues are cleared before new ones, so a short payment always shows up as a current-period default.',
          'A QRMP taxpayer with low sales in April may pay actual tax by 25 May instead of 35% of the earlier quarter\'s cash.'),
        C('c3', T3, [
            'Section 50(1): interest at 18% a year on tax not paid by the due date, from the day after the due date until payment. Where the return is filed late but before proceedings, interest is on the cash portion only.',
            'Section 50(3): where ITC is wrongly availed and utilised, interest is payable at the notified rate (18%) from the date of utilisation to the date of reversal or payment; credit merely availed but not used attracts no interest.',
            'ITC is treated as utilised when the balance in the credit ledger falls below the wrongly availed amount. Interest is paid in cash and is not deductible from ITC.'],
          'Interest charges only for the time the Government was actually short of cash.',
          'Wrong credit of ₹10,000 sitting unused in the ledger costs nothing; once used, interest starts.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Payment calendar for a QRMP client', 'role': 'Article assistant',
             'situation': 'A small trader on QRMP keeps missing the monthly payment.',
             'steps': ['Explain the 25th deadline for months one and two.', 'Choose fixed-sum or self-assessment method.', 'Generate challan early; it is valid 15 days.', 'Reconcile in the quarterly GSTR-3B.'],
             'takeaway': 'Quarterly returns still mean monthly payments.'}]

    mcqs = [
        Q('m1', 'Late fee under GST can be paid from:', ['Electronic cash ledger only', 'Electronic credit ledger', 'Either ledger', 'Liability register'], 0,
          'The credit ledger pays only output tax; fees, interest and penalties are paid in cash. In practice: keep cash for these.', 'c1', T1),
        Q('m2', 'A GST challan is valid for:', ['15 days', '7 days', '30 days', '24 hours'], 0,
          'A challan generated on the portal must be paid within 15 days. In practice: generate it close to payment.', 'c1', T1, check=15),
        Q('m3', 'Over-the-counter payment is allowed up to:', ['₹10,000 per challan per tax period', '₹50,000', '₹1 lakh', 'No limit'], 0,
          'Cash or cheque payments at the bank counter are capped at ₹10,000 per challan per period (with exceptions for Government recoveries). In practice: use online modes.', 'c1', T1, check=10000),
        Q('m4', 'Which dues are discharged first under section 49(8)?', ['Self-assessed dues of previous periods', 'Current period tax', 'Demand under section 74', 'Penalty'], 0,
          'Order: previous periods, then current period, then demands. In practice: arrears eat into current payments.', 'c2', T2),
        Q('m5', 'Monthly payment under QRMP for the first two months of a quarter is due by:', ['25th of the next month', '20th of the next month', '11th of the next month', '30th of the next month'], 0,
          'QRMP taxpayers deposit by the 25th using Form PMT-06. In practice: the fixed-sum option is 35% of last quarter\'s cash tax.', 'c2', T2, check=25),
        Q('m6', 'Interest on delayed payment of tax is:', ['18% per annum', '24% per annum', '12% per annum', '1.5% per month'], 0,
          'Section 50(1) and the notification set 18% per annum. In practice: compute by days.', 'c3', T3),
        Q('m7', 'Interest on ITC wrongly availed applies when:', ['It is availed and utilised', 'It is merely availed', 'It is reported in GSTR-1', 'It is in GSTR-2B'], 0,
          'Section 50(3) charges interest only on credit both availed and utilised. In practice: reverse early.', 'c3', T3),
        Q('m8', 'For a return filed late (no proceedings), interest is charged on:', ['The cash portion of the tax', 'The gross tax liability', 'The ITC only', 'Nothing'], 0,
          'The proviso to section 50(1) limits interest to the part paid in cash. In practice: ITC available in the ledger reduces the base.', 'c3', T3),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Cash portion base', 1, 'concept', 'cash'), S('s2', 'Late interest', 1, 'computation', '18%', nums=[i_late]), S('s3', 'Utilised ITC interest', 2, 'computation', 'utilised|availed', nums=[i_itc])],
          ['Use days/365.'], ['Charging interest on gross tax.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Output tax', 1, 'concept', 'credit ledger'), S('s2', 'RCM and interest', 1, 'concept', 'cash'), S('s3', 'Fees and penalty', 1, 'concept', 'cash')],
          ['Name the ledger.'], ['Paying RCM through ITC.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is the electronic liability register?', 'The portal record of all amounts payable by a taxpayer — tax, interest, penalty, fee — and how they are discharged.',
          [P('p1', 'All dues', 5, 'tax|interest|penalty'), P('p2', 'Record', 5, 'record|register')], 'c1'),
        V('v2', 'What can the credit ledger pay?', 'Only output tax; interest, penalty, fees and reverse charge tax must be paid from the cash ledger.',
          [P('p1', 'Output tax', 6, 'output tax'), P('p2', 'Cash for rest', 4, 'cash')], 'c1'),
        V('v3', 'What is the order of discharge?', 'Previous periods\' self-assessed dues, then the current period, then demands raised under sections 73 or 74.',
          [P('p1', 'Previous first', 6, 'previous'), P('p2', 'Demands last', 4, 'demand')], 'c2'),
        V('v4', 'When is interest charged on ITC?', 'When ITC is wrongly availed and utilised, at 18% from utilisation till reversal.',
          [P('p1', 'Availed and utilised', 6, 'utilis'), P('p2', '18%', 4, '18%')], 'c3'),
        V('v5', 'What is the date of deposit in the cash ledger?', 'The date on which the amount is credited to the Government account in the authorised bank, as shown by the challan identification number.',
          [P('p1', 'Credit to Government', 6, 'credit|government'), P('p2', 'CIN', 4, 'challan identification|cin')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Bloom Florists', 'difficulty': 'core',
              'case': 'Bloom Florists, a QRMP taxpayer, had cash tax of ₹20,000 in the last quarter. For April it chooses the fixed-sum method. It has ITC of ₹30,000 but owes a late fee of ₹1,000 and reverse charge tax of ₹4,000 on rent.',
              'mcqs': [
                  M('k1a', 'April payment under the fixed-sum method:', ['₹7,000', '₹20,000', '₹6,667', '₹10,000'], 0,
                    '35% of last quarter\'s cash tax: 35% × ₹20,000 = ₹7,000, due by 25 May. In practice: it is adjusted in the quarterly return.', 'moderate', check=7000, topic=T2),
                  M('k1b', 'The late fee is paid from:', ['Cash ledger', 'Credit ledger', 'Either', 'Not payable'], 0,
                    'Fees are paid only in cash. In practice: ITC cannot pay fees.', 'core', topic=T1),
                  M('k1c', 'Reverse charge tax on rent is paid from:', ['Cash ledger', 'Credit ledger', 'Either', 'Liability register'], 0,
                    'RCM tax must be paid in cash. In practice: it can then be claimed as ITC.', 'core', topic=T1),
                  M('k1d', 'If Bloom pays the quarter\'s tax 10 days late on a cash liability of ₹18,250, interest is:', ['₹90', '₹900', '₹182', '₹50'], 0,
                    '₹18,250 × 18% × 10/365 = ₹90. In practice: interest is in cash.', 'moderate', check=90, topic=T3),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch13', 1, 'Payment of Tax',
                ['Explain the electronic ledgers and modes of deposit.',
                 'Apply the order of discharge and payment due dates.',
                 'Compute interest on delayed payment and wrong ITC.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 25}, 'prereq': ['int-p3-b-ch12-u01'],
                 'exam_tip': 'In interest sums, check whether the base is the cash portion and whether ITC was actually utilised.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Cash ledger, credit ledger, liability register.',
                             'Credit ledger: output tax only; RCM, interest, fees, penalty in cash.',
                             'Order: previous periods → current → demands.',
                             'Monthly by 20th; QRMP months by 25th (35% or actual).',
                             'Interest 18%; on cash portion; wrong ITC only if utilised.'],
                 'remember': ['Challan valid 15 days; OTC up to ₹10,000.'],
                 'traps': ['Merely availed wrong ITC: no interest.', 'TDS/TCS credit goes to cash ledger.']},
                [('Interest', '18% p.a.'), ('Challan validity', '15 days'), ('OTC limit', '₹10,000'), ('QRMP monthly', '25th')],
                viva, cases)
