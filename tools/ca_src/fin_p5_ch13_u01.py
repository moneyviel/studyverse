"""CA Final · Paper 5 · Chapter 13 Returns.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch13-u01'
T1 = 'Outward supply statements — GSTR-1 and IFF'
T2 = 'GSTR-3B and the QRMP scheme'
T3 = 'Annual return, final return and other returns'
T4 = 'Late fee and time-bar'


def build():
    ck = Checks()
    a = ck.add('min(50*40,5000)', 'Late fee for 40 days, turnover ₹3 crore (₹)')
    b = ck.add('min(50*120,5000)', 'Late fee for 120 days, capped (₹)')
    i1 = {'id': 'i1', 'title': 'Late fee on GSTR-3B', 'difficulty': 'core', 'minutes': 6,
          'q': 'Neelam Traders (aggregate turnover ₹3 crore, tax payable not nil) files GSTR-3B for two months late by (a) 40 days and (b) 120 days. Compute total late fee (CGST + SGST).',
          'solution': [table(['Case', 'Working', '₹'], [
              ['(a)', '₹50 per day × 40, cap ₹5,000', inr(a)],
              ['(b)', '₹50 per day × 120 = 6,000, capped', inr(b)]], title='Section 47 read with notifications')],
          'checks': list(ck)}

    c2 = Checks()
    f = c2.add('min(50*30,40000000*0.0004)', 'Late fee for GSTR-9 delayed 30 days (₹)')
    i2 = {'id': 'i2', 'title': 'Annual return obligations', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'For 2026-27: (a) Arya Ltd has turnover of ₹1.8 crore; (b) Bhaskar & Co has turnover of ₹4 crore and files GSTR-9 30 days late; (c) Chirag Ltd has turnover of ₹12 crore. State annual return obligations and compute Bhaskar\'s late fee.',
          'solution': [table(['Entity', 'Rule', 'Result'], [
              ['Arya Ltd', 'GSTR-9 optional up to ₹2 crore', 'Optional'],
              ['Bhaskar & Co', '₹50/day, cap 0.04% of turnover', f'₹{inr(f)}'],
              ['Chirag Ltd', 'GSTR-9 plus self-certified reconciliation GSTR-9C above ₹5 crore', 'Both required by 31 December 2027']], title='Section 44')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 37: details of outward supplies are furnished in GSTR-1 by the 11th of the next month (monthly filers) or 13th of the month after the quarter (QRMP). Optional Invoice Furnishing Facility (IFF) lets QRMP taxpayers upload B2B invoices for the first two months by the 13th of the following month.',
            'GSTR-1A allows amendments or missed details for the same tax period before filing GSTR-3B. GSTR-1 cannot be filed if GSTR-3B for the previous period is pending, and filing of GSTR-1 is a precondition for GSTR-3B of the same period.',
            'HSN details in GSTR-1 depend on turnover (4 digits up to ₹5 crore for B2B; 6 digits above). Errors can be corrected up to 30 November after the year or the annual return date, whichever earlier.'],
          'GSTR-1 tells buyers what you sold; it feeds their ITC.',
          'A monthly filer submits June GSTR-1 by 11 July.'),
        C('c2', T2, [
            'Section 39: GSTR-3B is the summary return with self-assessed tax and payment, due by the 20th of the next month for monthly filers; QRMP filers (turnover up to ₹5 crore) file quarterly by the 22nd or 24th depending on State, paying tax monthly via PMT-06 by the 25th using fixed-sum or self-assessment methods.',
            'A return is valid only if self-assessed tax is paid in full. Returns must be signed with DSC (mandatory for companies and LLPs), e-sign or EVC.',
            'The Invoice Management System lets recipients accept, reject or keep pending invoices before GSTR-2B is generated, affecting ITC.'],
          'GSTR-3B is where tax is actually paid.',
          'A Maharashtra QRMP filer files quarterly GSTR-3B by the 22nd.'),
        C('c3', T3, [
            'Section 44: annual return GSTR-9 by 31 December after the year; optional for taxpayers with turnover up to ₹2 crore; self-certified reconciliation statement GSTR-9C for turnover above ₹5 crore. Composition taxpayers file GSTR-4 annually by 30 April and pay quarterly via CMP-08 by the 18th.',
            'Section 45: a final return GSTR-10 within three months of cancellation or the date of cancellation order, whichever later.',
            'Other returns: GSTR-5 (non-resident taxable persons), GSTR-5A (OIDAR suppliers), GSTR-6 (ISD), GSTR-7 (TDS), GSTR-8 (TCS). Section 46 notices are issued to non-filers, and best judgement assessment can follow.'],
          'Annual, final and special returns complete the cycle.',
          'A firm with ₹12 crore turnover files both GSTR-9 and GSTR-9C.'),
        C('c4', T4, [
            'Section 47: late fee for GSTR-1 and GSTR-3B is reduced by notification to ₹50 per day (₹20 per day for nil returns) with caps of ₹2,000 (turnover up to ₹1.5 crore), ₹5,000 (₹1.5–5 crore) and ₹10,000 (above ₹5 crore) — amounts total CGST and SGST.',
            'GSTR-9 late fee: ₹50 per day up to ₹5 crore turnover and ₹100 per day for ₹5–20 crore, capped at 0.04% of State turnover; higher for larger taxpayers. GSTR-4: ₹50 per day capped at ₹2,000 (₹20 per day and ₹500 cap if nil). GSTR-7: ₹50 per day capped at ₹1,000.',
            'Returns (GSTR-1, 3B, 4, 5, 5A, 6, 7, 8, 9) cannot be filed after three years from their due dates. Late fee may be waived in part or full by notification (section 128).'],
          'Late fees are per day with caps; returns time-bar after three years.',
          'A ₹3 crore trader filing GSTR-3B 120 days late pays a capped ₹5,000.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Return calendar', 'role': 'Compliance associate',
             'situation': 'A client with several registrations keeps missing due dates.',
             'steps': ['Map monthly and quarterly due dates.', 'Use IMS to manage supplier invoices.', 'Pay via PMT-06 for QRMP months.', 'Plan GSTR-9 and 9C by December.'],
             'takeaway': 'A calendar avoids fees and blocked ITC for customers.'}]

    mcqs = [
        Q('m1', 'GSTR-1 for monthly filers is due by:', ['Eleventh of next month', 'Twentieth', 'Thirteenth', 'Tenth'], 0,
          'Section 37. In practice: QRMP 13th.', 'c1', T1),
        Q('m2', 'IFF is available to:', ['QRMP taxpayers for the first two months', 'All taxpayers monthly', 'Composition dealers', 'Non-residents'], 0,
          'Optional B2B upload. In practice: 13th of next month.', 'c1', T1),
        Q('m3', 'QRMP scheme is available up to aggregate turnover of:', ['Five crore rupees', 'Two crore rupees', 'One crore fifty lakh rupees', 'Ten crore rupees'], 0,
          'Rule 61A. In practice: monthly payment.', 'c2', T2),
        Q('m4', 'GSTR-9 is optional for turnover up to:', ['Two crore rupees', 'Five crore rupees', 'One crore rupees', 'Fifty lakh rupees'], 0,
          'Notification. In practice: 9C above ₹5 crore.', 'c3', T3),
        Q('m5', 'Final return GSTR-10 is due within:', ['Three months of cancellation or order, whichever later', 'Thirty days', 'One year', 'Six months'], 0,
          'Section 45. In practice: tax on stock.', 'c3', T3),
        Q('m6', 'Composition taxpayers file their annual return GSTR-4 by:', ['Thirtieth April', 'Thirty-first December', 'Eighteenth of each quarter', 'Thirtieth November'], 0,
          'Section 39(2). In practice: CMP-08 quarterly.', 'c3', T3),
        Q('m7', 'Late fee for a nil GSTR-3B is per day:', ['Twenty rupees', 'Fifty rupees', 'One hundred rupees', 'Ten rupees'], 0,
          'Notification. In practice: capped ₹500.', 'c4', T4),
        Q('m8', 'Returns cannot be filed after how many years from the due date?', ['Three', 'Two', 'Five', 'Six'], 0,
          'Time-bar. In practice: plan pending filings.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', '40-day case', 2, 'computation', 'per day', nums=[a]), S('s2', '120-day case', 2, 'computation', 'cap', nums=[b])],
          ['State cap slab.'], ['Charging ₹200 per day.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Obligations', 3, 'analysis', '2 crore'), S('s2', 'Late fee', 2, 'computation', '0.04', nums=[f])],
          ['Cite thresholds.'], ['Treating GSTR-9C as audited.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is GSTR-1A?', 'An optional form to amend or add outward supply details of a tax period before filing GSTR-3B for it.',
          [P('p1', 'Amend', 5, 'amend'), P('p2', 'Before GSTR-3B', 5, 'before')], 'c1'),
        V('v2', 'When is a GSTR-3B a valid return?', 'When the self-assessed tax shown in it has been paid in full.',
          [P('p1', 'Paid in full', 5, 'paid in full'), P('p2', 'Self-assessed', 5, 'self-assessed')], 'c2'),
        V('v3', 'What does the Invoice Management System do?', 'It lets recipients accept, reject or keep pending supplier invoices before GSTR-2B is generated.',
          [P('p1', 'Accept or reject', 5, 'accept'), P('p2', 'GSTR-2B', 5, '2b')], 'c2'),
        V('v4', 'Who files GSTR-5A?', 'Suppliers of OIDAR services from outside India to non-taxable online recipients.',
          [P('p1', 'OIDAR', 5, 'oidar'), P('p2', 'Non-taxable online recipients', 5, 'non-taxable')], 'c3'),
        V('v5', 'How long after the due date does a return become time-barred?', 'Three years from its due date.',
          [P('p1', 'Three years', 5, 'three years'), P('p2', 'Due date', 5, 'due date')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'QRMP at Meera Garments', 'difficulty': 'core',
              'case': 'Meera Garments (Karnataka, turnover ₹3.5 crore) opts for QRMP for the July–September 2026 quarter. Its July tax liability is ₹60,000.',
              'mcqs': [
                  M('k1a', 'Due date to pay July tax via PMT-06:', ['25 August 2026', '20 August 2026', '22 October 2026', '13 August 2026'], 0,
                    'Monthly payment. In practice: fixed sum or self-assessment.', 'core', topic=T2),
                  M('k1b', 'Quarterly GSTR-1 due date:', ['13 October 2026', '11 October 2026', '22 October 2026', '20 October 2026'], 0,
                    'QRMP. In practice: IFF for July and August.', 'core', topic=T1),
                  M('k1c', 'Quarterly GSTR-3B due date for a Karnataka taxpayer:', ['22 October 2026', '24 October 2026', '20 October 2026', '25 October 2026'], 0,
                    'Category of States. In practice: check notification.', 'core', topic=T2),
                  M('k1d', 'Amount payable for July (₹):', ['60,000', '20,000', '1,80,000', 'Nil'], 0,
                    'Self-assessed liability. In practice: interest if late.', 'core', check=60000, topic=T2),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch13', 1, 'Returns',
                ['Apply GSTR-1, IFF and GSTR-1A provisions.',
                 'Apply GSTR-3B and QRMP provisions.',
                 'Apply annual, final and special returns.',
                 'Compute late fees and apply time-bar.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 20}, 'prereq': ['fin-p5-ch12-u01'],
                 'exam_tip': 'Write due dates as day plus month-after-period to avoid confusion.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['GSTR-1 11th/13th; IFF; GSTR-1A.', 'GSTR-3B 20th; QRMP 22nd/24th; PMT-06 25th.', 'GSTR-9 by 31 December; optional ≤ ₹2 crore; 9C > ₹5 crore.',
                             'GSTR-4 30 April; GSTR-10 within three months.', 'Late fee ₹50/₹20 per day with caps; three-year time-bar.'],
                 'remember': ['IMS shapes GSTR-2B.'],
                 'traps': ['Treating GSTR-9 as mandatory for small taxpayers.']},
                [('GSTR-1', 'Section 37'), ('GSTR-3B', 'Section 39'), ('Annual return', 'Section 44'), ('Final return', 'Section 45'), ('Late fee', 'Section 47')],
                viva, cases)
