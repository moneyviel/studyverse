"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 15 Returns.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch15-u01'
T1 = 'Outward supplies and auto-drafted inward details (ss. 37–38)'
T2 = 'Monthly/quarterly returns and QRMP (s. 39)'
T3 = 'Annual and final returns (ss. 44–45) and late fee (s. 47)'
T4 = 'Other returns and GST practitioners'


def build():
    ck = Checks()
    fee1 = ck.add('min(50*25, 2000)', 'Late fee for GSTR-3B (CGST + SGST), turnover up to ₹1.5 crore')
    fee2 = ck.add('min(20*40, 500)', 'Late fee for a nil GSTR-3B, capped at ₹500')
    i1 = {'id': 'i1', 'title': 'Late returns', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Compute late fee (CGST + SGST combined): (a) Asha Stores (turnover ₹1.2 crore) files GSTR-3B 25 days late with tax payable; (b) Bina Traders files a nil GSTR-3B 40 days late.',
          'solution': [table(['Case', 'Rate', 'Working', 'Fee ₹'], [
              ['(a)', '₹50 a day (₹25 + ₹25)', '25 × 50 = 1,250; cap ₹2,000 for turnover up to ₹1.5 crore', inr(fee1)],
              ['(b)', '₹20 a day (₹10 + ₹10) for nil return', '40 × 20 = 800; cap ₹500', inr(fee2)]], title='Section 47'),
              note('Interest under section 50 is separate and applies only where tax is paid late.')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Return calendar', 'difficulty': 'core', 'minutes': 6,
          'q': 'State the form and due date for May 2027: (a) a monthly filer\'s outward supply details; (b) its summary return with payment; (c) a QRMP taxpayer wanting to pass B2B credit to buyers for May; (d) a composition dealer\'s statement for April–June; (e) an ISD; (f) a TDS deductor.',
          'solution': [table(['Case', 'Form', 'Due date'], [
              ['(a)', 'GSTR-1', '11 June'],
              ['(b)', 'GSTR-3B', '20 June'],
              ['(c)', 'Invoice Furnishing Facility (IFF)', '1–13 June'],
              ['(d)', 'CMP-08', '18 July'],
              ['(e)', 'GSTR-6', '13 June'],
              ['(f)', 'GSTR-7', '10 June']], title='Return due dates')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Section 37: GSTR-1 reports outward supplies — by the 11th of the next month for monthly filers, by the 13th after the quarter for QRMP filers. QRMP filers may upload B2B invoices for the first two months through the Invoice Furnishing Facility (IFF) by the 13th.',
            'Details flow to recipients as GSTR-2B, an auto-drafted, static statement of available ITC each month. The Invoice Management System lets recipients accept, reject or keep invoices pending before 2B is finalised.',
            'Errors in GSTR-1 are corrected in a later return (or GSTR-1A for the same period) — but not after 30 November following the year or the annual return, whichever is earlier. A return cannot be filed after three years from its due date.'],
          'GSTR-1 is what the seller tells; GSTR-2B is what the buyer can claim from it.',
          'If a supplier misses an invoice in GSTR-1, the buyer cannot claim its ITC until it appears in 2B.'),
        C('c2', T2, [
            'Section 39: GSTR-3B is the summary return of outward supplies, ITC and tax paid — by the 20th of the next month for monthly filers; by the 22nd or 24th after the quarter (by State group) for QRMP filers.',
            'QRMP: available to registered persons with aggregate turnover up to ₹5 crore; returns quarterly, payment monthly (by the 25th for the first two months).',
            'Tax must be paid by the due date of the return. Nil returns can be filed by SMS. GSTR-3B cannot be filed unless GSTR-1 for the period is filed, and the system now restricts ITC claims that exceed what is in GSTR-2B.'],
          'One summary return for tax, with quarterly ease for small taxpayers but monthly cash.',
          'A ₹3 crore trader may choose QRMP and file only four GSTR-3Bs a year.'),
        C('c3', T3, [
            'Section 44: annual return GSTR-9 by 31 December following the year; optional for taxpayers with aggregate turnover up to ₹2 crore. Those above ₹5 crore also file a self-certified reconciliation statement GSTR-9C. Composition taxpayers file GSTR-4 by 30 April following the year.',
            'Section 45: a person whose registration is cancelled files a final return (GSTR-10) within three months of the date of cancellation or the cancellation order, whichever is later.',
            'Section 47 late fee: GSTR-1 and GSTR-3B — ₹50 a day (₹20 for nil returns) of CGST and SGST combined, with caps of ₹500 (nil), ₹2,000 (turnover up to ₹1.5 crore), ₹5,000 (₹1.5–5 crore) and ₹10,000 (above ₹5 crore). GSTR-9 — ₹200 a day, subject to a cap based on turnover in the State.'],
          'The annual return closes the year; the final return closes the registration.',
          'A ₹1.8 crore taxpayer may skip GSTR-9 altogether.'),
        C('c4', T4, [
            'Other returns: GSTR-5 by non-resident taxable persons; GSTR-5A by OIDAR suppliers; GSTR-6 by ISDs (13th); GSTR-7 by TDS deductors (10th); GSTR-8 by ECOs collecting TCS (10th); CMP-08 quarterly by composition taxpayers (18th after the quarter).',
            'Section 48: a GST practitioner, enrolled after meeting qualification conditions (for example, a CA, CS, cost accountant or advocate, or a graduate in specified subjects), may prepare and file returns and appear before authorities on behalf of a registered person who authorises him; responsibility for correctness remains with the taxpayer.'],
          'Each special category of taxpayer has its own return; practitioners help, but the taxpayer remains responsible.',
          'A non-resident exhibitor files GSTR-5 for its period of registration.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Compliance calendar', 'role': 'Article assistant',
             'situation': 'A firm handles 25 GST clients — monthly, QRMP and composition.',
             'steps': ['Classify clients by filing scheme.', 'Set reminders for 10th, 11th, 13th, 18th, 20th and 25th.', 'Reconcile GSTR-2B and IMS before GSTR-3B.', 'Track annual return thresholds.'],
             'takeaway': 'Filing dates differ by scheme — a calendar prevents late fees.'}]

    mcqs = [
        Q('m1', 'GSTR-1 for a monthly filer is due by:', ['11th of the next month', '20th of the next month', '13th of the next month', '10th of the next month'], 0,
          'Monthly filers file GSTR-1 by the 11th; QRMP filers by the 13th after the quarter. In practice: buyers\' credit depends on it.', 'c1', T1, check=11),
        Q('m2', 'GSTR-2B is:', ['An auto-drafted statement of ITC available', 'A return filed by the recipient', 'An annual return', 'A payment challan'], 0,
          'GSTR-2B is generated from suppliers\' filings and is the basis for ITC claims. In practice: reconcile it monthly.', 'c1', T1),
        Q('m3', 'QRMP is available to taxpayers with aggregate turnover up to:', ['₹5 crore', '₹2 crore', '₹1.5 crore', '₹10 crore'], 0,
          'The QRMP scheme covers registered persons with turnover up to ₹5 crore. In practice: payment remains monthly.', 'c2', T2, check=5),
        Q('m4', 'GSTR-9 is optional for taxpayers with aggregate turnover up to:', ['₹2 crore', '₹5 crore', '₹1.5 crore', '₹50 lakh'], 0,
          'The annual return is optional up to ₹2 crore; GSTR-9C applies above ₹5 crore. In practice: many small taxpayers skip it.', 'c3', T3, check=2),
        Q('m5', 'A final return after cancellation is filed within:', ['Three months of cancellation date or order, whichever is later', '30 days', 'One year', '6 months'], 0,
          'Section 45 gives three months. In practice: pay any stock reversal with it.', 'c3', T3),
        Q('m6', 'Late fee for a nil GSTR-3B is capped at:', ['₹500', '₹2,000', '₹5,000', '₹10,000'], 0,
          'Nil return late fee is ₹20 a day (combined), up to ₹500. In practice: file nil returns by SMS.', 'c3', T3, check=500),
        Q('m7', 'Composition taxpayers file their annual return in:', ['GSTR-4 by 30 April', 'GSTR-9 by 31 December', 'CMP-08 by 18th', 'GSTR-3B'], 0,
          'GSTR-4 is the annual return for composition taxpayers, due 30 April after the year; CMP-08 is the quarterly payment statement. In practice: both are required.', 'c4', T4),
        Q('m8', 'A GST return cannot be filed after:', ['Three years from its due date', 'One year', 'Five years', 'No limit'], 0,
          'Sections 37, 39, 44 and 52 bar filing after three years from the due date. In practice: old defaults may become unfixable.', 'c1', T1),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Rate', 1, 'concept', '50|20'), S('s2', 'Fee (a)', 1, 'computation', '2,000', nums=[fee1]), S('s3', 'Nil cap', 2, 'computation', '500', nums=[fee2])],
          ['Apply the cap.'], ['Charging ₹200 a day.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'GSTR-1', 1, 'concept', '11'), S('s2', 'GSTR-3B', 1, 'concept', '20'), S('s3', 'IFF', 1, 'concept', 'iff|13'),
           S('s4', 'CMP-08', 1, 'concept', '18'), S('s5', 'GSTR-6', 1, 'concept', 'gstr-6'), S('s6', 'GSTR-7', 1, 'concept', 'gstr-7')],
          ['Give form and date.'], ['Mixing up GSTR-7 and GSTR-8.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is IFF?', 'The Invoice Furnishing Facility that lets QRMP taxpayers upload B2B invoices for the first two months of a quarter so buyers get credit monthly.',
          [P('p1', 'QRMP', 5, 'qrmp|quarter'), P('p2', 'B2B invoices', 5, 'b2b|invoice')], 'c1'),
        V('v2', 'Who can opt for QRMP?', 'Registered persons with aggregate turnover up to ₹5 crore who file GSTR-3B.',
          [P('p1', '₹5 crore', 6, '5 crore'), P('p2', 'Turnover', 4, 'turnover')], 'c2'),
        V('v3', 'Who must file GSTR-9C?', 'Taxpayers with aggregate turnover above ₹5 crore, as a self-certified reconciliation statement with the annual return.',
          [P('p1', 'Above ₹5 crore', 6, '5 crore'), P('p2', 'Self-certified', 4, 'self-certif|reconcil')], 'c3'),
        V('v4', 'What is the late fee for GSTR-3B with tax payable?', '₹50 a day combining CGST and SGST, capped according to turnover from ₹2,000 to ₹10,000.',
          [P('p1', '₹50 a day', 6, '50'), P('p2', 'Cap by turnover', 4, 'cap|2,000|10,000')], 'c3'),
        V('v5', 'What does a GST practitioner do?', 'Prepares and files returns and appears before authorities for a registered person who authorises him, while the taxpayer stays responsible.',
          [P('p1', 'Files returns', 5, 'return'), P('p2', 'Authorised', 5, 'authoris')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Arya Textiles', 'difficulty': 'moderate',
              'case': 'Arya Textiles (aggregate turnover ₹4 crore, Maharashtra) has opted for QRMP. Its largest buyer insists on monthly ITC. Arya forgot to report an April invoice in its April–June GSTR-1 and noticed it in December.',
              'mcqs': [
                  M('k1a', 'To give the buyer April credit, Arya should use:', ['IFF by 13 May', 'GSTR-3B for April', 'GSTR-9', 'GSTR-1A in July'], 0,
                    'IFF lets QRMP taxpayers upload B2B invoices monthly for the first two months. In practice: total IFF value is limited per month.', 'core', topic=T1),
                  M('k1b', 'Quarterly GSTR-3B is due for Arya (Maharashtra) by:', ['22nd after the quarter', '20th after the quarter', '24th after the quarter', '25th after the quarter'], 0,
                    'Maharashtra falls in the group with the 22nd as due date. In practice: payment for months one and two is by the 25th.', 'moderate', check=22, topic=T2),
                  M('k1c', 'Can the missed April invoice still be reported in December?', ['Yes, before 30 November of the next year or the annual return', 'No, never', 'Only through GSTR-9', 'Only with the officer\'s approval'], 0,
                    'Corrections are allowed till 30 November after the year or the annual return, whichever is earlier. In practice: report it in the next GSTR-1 with interest on any tax.', 'moderate', topic=T1),
                  M('k1d', 'Is GSTR-9 compulsory for Arya?', ['Yes, turnover exceeds ₹2 crore', 'No, it is optional', 'Only GSTR-9C', 'Only if audited'], 0,
                    'The annual return is optional only up to ₹2 crore; at ₹4 crore Arya must file GSTR-9 (but not 9C). In practice: due 31 December.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch15', 1, 'Returns',
                ['Explain GSTR-1, GSTR-2B and IFF.',
                 'Apply GSTR-3B and QRMP due dates.',
                 'Explain annual and final returns and compute late fees.',
                 'Identify special returns and the role of GST practitioners.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 25}, 'prereq': ['int-p3-b-ch14-u01'],
                 'exam_tip': 'Memorise the due-date ladder: 10 (GSTR-7/8), 11 (GSTR-1), 13 (IFF, GSTR-6), 18 (CMP-08), 20 (GSTR-3B), 25 (QRMP payment).'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['GSTR-1: 11th / 13th (QRMP); IFF 1–13; GSTR-2B auto-drafted.',
                             'GSTR-3B: 20th; QRMP 22nd/24th; QRMP up to ₹5 crore.',
                             'GSTR-9 by 31 December (optional ≤ ₹2 crore); 9C > ₹5 crore; GSTR-4 by 30 April.',
                             'GSTR-10 within 3 months of cancellation.',
                             'Late fee ₹50/day (₹20 nil), capped ₹500–₹10,000.'],
                 'remember': ['Returns barred after 3 years from due date.', 'Corrections till 30 November or annual return.'],
                 'traps': ['GSTR-3B blocked if GSTR-1 not filed.', 'CMP-08 is quarterly; GSTR-4 annual.']},
                [('GSTR-1', '11th'), ('GSTR-3B', '20th'), ('GSTR-9', '31 December'), ('CMP-08', '18th')],
                viva, cases)
