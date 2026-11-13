"""CA Final · Paper 5 · Chapter 11 Payment of Tax.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch11-u01'
T1 = 'Electronic ledgers'
T2 = 'Order of utilisation of ITC'
T3 = 'Interest on delayed payment'
T4 = 'TDS under GST and transfer of credit'


def build():
    ck = Checks()
    ig = ck.add('70000-50000', 'IGST credit left after paying IGST (₹)')
    cg = ck.add('30000-(70000-50000)-10000', 'CGST payable in cash after credits (₹)')
    sg = ck.add('30000-25000', 'SGST payable in cash after SGST credit (₹)')
    cash = ck.add('(30000-(70000-50000)-10000)+(30000-25000)', 'Total cash payment (₹)')
    i1 = {'id': 'i1', 'title': 'Optimal use of credit', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Kirti Ltd has output tax: IGST ₹50,000, CGST ₹30,000, SGST ₹30,000. Credit available: IGST ₹70,000, CGST ₹10,000, SGST ₹25,000. Use credit in the permitted order to minimise cash payment.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['IGST credit to IGST', '50,000 used; balance', inr(ig)],
              ['IGST balance to CGST', '₹20,000 set off against CGST (must be used fully before CGST/SGST credit)', '—'],
              ['CGST credit', '30,000 − 20,000 − 10,000 → cash', inr(cg)],
              ['SGST credit', '30,000 − 25,000 → cash', inr(sg)],
              ['Total cash', '', inr(cash)]], title='Section 49 and rule 88A')],
          'checks': list(ck)}

    c2 = Checks()
    it = c2.add('round(100000*0.18*30/365,2)', 'Interest at 18% for 30 days (₹)')
    i2 = {'id': 'i2', 'title': 'Interest on late return', 'difficulty': 'core', 'minutes': 5,
          'q': 'Rajan files GSTR-3B for August 2026 (due 20 September 2026) on 20 October 2026, 30 days late. Total tax ₹3,00,000, of which ₹2,00,000 is paid by ITC and ₹1,00,000 in cash. No proceedings had started. Compute interest.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Base', 'Only the net cash portion (proviso to section 50(1))', '1,00,000'],
              ['Interest', '18% × 30/365', f'{it}']], title='Section 50')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'The electronic cash ledger records deposits (by challan in Form PMT-06 via net banking, cards, NEFT/RTGS or over the counter up to ₹10,000) and TDS/TCS credits claimed; the date of credit to the Government account is the date of deposit. Amounts can be used for tax, interest, penalty, fee and other dues and may be transferred to the cash ledger of a distinct person.',
            'The electronic credit ledger holds self-assessed ITC and can be used only for output tax — not interest, penalty, fees or reverse charge tax, which must be paid in cash.',
            'The electronic liability register records all liabilities. Order of discharge (section 49(8)): first self-assessed tax and dues of previous periods, then current period self-assessed tax and dues, then demands, including those under sections 73, 74 or 74A.'],
          'Cash ledger pays anything; credit ledger pays only output tax.',
          'RCM tax must be paid from the cash ledger.'),
        C('c2', T2, [
            'IGST credit is used first for IGST, then for CGST and SGST/UTGST in any order or proportion. CGST credit is used for CGST then IGST; SGST credit for SGST then IGST. CGST credit cannot pay SGST and vice versa.',
            'Under section 49A and rule 88A, IGST credit must be fully used before CGST or SGST credit is used to pay IGST, CGST or SGST.',
            'Section 53 transfers amounts between Central and State accounts when credits of one are used for the other\'s tax; section 49B lets the Government prescribe the order and manner of utilisation.'],
          'IGST first, and cross-use only through IGST.',
          'IGST credit left after paying IGST should be set off before using CGST credit.'),
        C('c3', T3, [
            'Section 50(1): interest at 18% per annum is payable on tax paid late, from the day after the due date until payment. Where a return for a period is filed late (not after proceedings start), interest is only on the portion paid in cash.',
            'Section 50(3): where ITC is wrongly availed and utilised, interest at the notified rate (currently 18%) applies from the date of utilisation; wrongly availed credit that stays unused in the ledger attracts no interest. Rule 88B treats credit as utilised when the ledger balance falls below the wrongly availed amount.',
            'Interest is mandatory and compensatory, and is payable even without a demand order.'],
          'Late tax costs 18% a year, mostly on the cash part.',
          'Tax of ₹1 lakh paid 30 days late in cash costs about ₹1,479 in interest.'),
        C('c4', T4, [
            'Section 51: notified deductors — central and State government departments, local authorities, governmental agencies and specified persons — deduct TDS from payments to suppliers where the total value of a contract exceeds the notified threshold; the deductee claims the amount in its cash ledger after accepting it on the portal.',
            'The deductor files GSTR-7, issues a TDS certificate, and pays late fee and interest for delays.',
            'Section 52 (TCS by ECOs) is discussed with e-commerce transactions; amounts deducted or collected credited to the cash ledger can be used for any liability.'],
          'TDS and TCS land in the supplier\'s cash ledger once accepted.',
          'A supplier to a government department sees TDS in its cash ledger after accepting it.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Monthly payment planning', 'role': 'GST accountant',
             'situation': 'A company with all three tax types wants to minimise cash outflow.',
             'steps': ['Compute liabilities by tax head.', 'Apply IGST credit first.', 'Pay RCM and interest in cash.', 'File on time to avoid interest.'],
             'takeaway': 'Correct sequencing of credit can save cash every month.'}]

    mcqs = [
        Q('m1', 'Which can be paid from the electronic credit ledger?', ['Output tax', 'Interest', 'Late fee', 'Tax under reverse charge'], 0,
          'Section 49(4). In practice: others in cash.', 'c1', T1),
        Q('m2', 'CGST credit can be used to pay:', ['CGST and then IGST', 'SGST', 'Penalty', 'UTGST'], 0,
          'Section 49(5)(b). In practice: not SGST.', 'c2', T2),
        Q('m3', 'Before using CGST credit, IGST credit must be:', ['Fully utilised', 'Refunded', 'Transferred to SGST', 'Ignored'], 0,
          'Rule 88A. In practice: sequence matters.', 'c2', T2),
        Q('m4', 'Interest on delayed payment of tax is at:', ['Eighteen percent per annum', 'Twenty-four percent', 'Twelve percent', 'Nine percent'], 0,
          'Section 50(1). In practice: day after due date.', 'c3', T3),
        Q('m5', 'For a late GSTR-3B (no proceedings), interest is charged on:', ['Tax paid in cash', 'Gross tax liability', 'ITC claimed', 'Turnover'], 0,
          'Proviso to section 50(1). In practice: net cash.', 'c3', T3),
        Q('m6', 'Interest on wrongly availed ITC applies only when it is:', ['Utilised', 'Reported', 'Reversed', 'Claimed in GSTR-1'], 0,
          'Section 50(3). In practice: rule 88B.', 'c3', T3),
        Q('m7', 'Over-the-counter cash deposit per challan is allowed up to:', ['Ten thousand rupees', 'Fifty thousand rupees', 'One lakh rupees', 'Two thousand rupees'], 0,
          'Rule 87. In practice: digital modes preferred.', 'c1', T1),
        Q('m8', 'TDS deducted under section 51 is credited to the supplier\'s:', ['Electronic cash ledger', 'Electronic credit ledger', 'Liability register', 'Bank account'], 0,
          'After acceptance. In practice: usable for any due.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'IGST credit use', 3, 'computation', 'IGST', nums=[ig]), S('s2', 'Cash payable', 3, 'computation', 'cash', nums=[cg, sg, cash])],
          ['Show order.'], ['Using CGST credit for SGST.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Interest base and amount', 3, 'computation', 'cash', nums=[it])],
          ['Cite proviso.'], ['Charging interest on ITC portion.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is the order of discharge under section 49(8)?', 'Previous periods\' self-assessed dues first, then current period dues, then demands raised.',
          [P('p1', 'Previous periods', 5, 'previous'), P('p2', 'Demands', 5, 'demand')], 'c1'),
        V('v2', 'Can cash ledger balance be moved to another registration of the same PAN?', 'Yes, to a distinct person\'s cash ledger under section 49(10).',
          [P('p1', 'Distinct person', 5, 'distinct'), P('p2', 'Cash ledger', 5, 'cash ledger')], 'c1'),
        V('v3', 'When does rule 88B treat ITC as utilised?', 'When the credit ledger balance falls below the wrongly availed amount, to that extent.',
          [P('p1', 'Balance falls', 5, 'falls below'), P('p2', 'Wrongly availed', 5, 'wrongly availed')], 'c3'),
        V('v4', 'What does section 53 provide?', 'Transfer of amounts between Central and IGST accounts when credits of one tax pay another.',
          [P('p1', 'Transfer', 5, 'transfer'), P('p2', 'IGST', 5, 'igst')], 'c2'),
        V('v5', 'Who must deduct TDS under GST?', 'Notified government departments, local authorities, government agencies and specified persons.',
          [P('p1', 'Government departments', 5, 'government'), P('p2', 'Local authorities', 5, 'local')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Wrong ITC at Pioneer Paints', 'difficulty': 'moderate',
              'case': 'Pioneer Paints wrongly claimed ITC of ₹2,00,000 in June 2026. Its credit ledger balance stayed above ₹2,00,000 until 31 July 2026, when it fell to ₹50,000. It reversed the wrong credit on 30 September 2026.',
              'mcqs': [
                  M('k1a', 'Wrong ITC treated as utilised on 31 July (₹):', ['1,50,000', '2,00,000', '50,000', 'Nil'], 0,
                    'Balance fell by ₹1.5 lakh below the wrong amount. In practice: rule 88B.', 'core', check=150000, topic=T3),
                  M('k1b', 'Days from 31 July to 30 September:', ['61', '60', '62', '59'], 0,
                    'August 31 + September 30. In practice: interest period.', 'core', check=61, topic=T3),
                  M('k1c', 'Interest at 18% on utilised amount (₹, approx.):', ['4,512', '6,016', '1,504', '9,000'], 0,
                    '1,50,000 × 18% × 61/365. In practice: pay with reversal.', 'core', check=round(150000*0.18*61/365), topic=T3),
                  M('k1d', 'Interest on the unutilised ₹50,000 part:', ['Nil', 'Payable at 18%', 'Payable at 24%', 'Payable at 12%'], 0,
                    'Only utilised credit attracts interest. In practice: reverse promptly.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch11', 1, 'Payment of Tax',
                ['Use electronic cash and credit ledgers correctly.',
                 'Apply the order of utilisation of ITC.',
                 'Compute interest on delayed payment and wrong ITC.',
                 'Explain TDS under GST.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 30, 'practice': 25}, 'prereq': ['fin-p5-ch10-u01'],
                 'exam_tip': 'Show a set-off table by tax head and keep IGST first.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 49 ledgers; cash for RCM, interest, fees.', 'Order: IGST first; no CGST↔SGST.', 'Section 50: 18% on net cash; wrong ITC only if utilised.',
                             'Section 51 TDS; credited to cash ledger.', 'Section 49(8) discharge order.'],
                 'remember': ['Rule 88A: exhaust IGST credit first.'],
                 'traps': ['Paying interest from the credit ledger.']},
                [('Ledgers', 'Section 49'), ('Utilisation', 'Section 49A/rule 88A'), ('Interest', 'Section 50'), ('TDS', 'Section 51')],
                viva, cases)
