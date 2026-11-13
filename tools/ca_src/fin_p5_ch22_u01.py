"""CA Final · Paper 5 · Chapter 22 Appeals and Revision under GST.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch22-u01'
T1 = 'Appeal to the Appellate Authority'
T2 = 'Revision by the Revisional Authority'
T3 = 'Appeals to the Tribunal, High Court and Supreme Court'
T4 = 'Mandatory pre-deposit and monetary limits'


def build():
    ck = Checks()
    adm = ck.add('6+1+0.5', 'Admitted tax, interest and penalty paid in full (₹ crore)')
    disp = ck.add('90-6', 'Remaining CGST in dispute (₹ crore)')
    pd = ck.add('min((90-6)*0.10,20)', 'Ten percent of disputed CGST, capped at ₹20 crore (₹ crore)')
    tot = ck.add('6+1+0.5+min((90-6)*0.10,20)', 'Total CGST-side deposit before the Appellate Authority (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Pre-deposit before the Appellate Authority', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'An order demands CGST ₹90 crore, interest ₹9 crore and penalty ₹90 crore from Navdeep Polymers Ltd. The company accepts CGST ₹6 crore with interest ₹1 crore and penalty ₹0.5 crore relating to it, and appeals against the rest. Compute the CGST-side amount to be deposited for filing the appeal to the Appellate Authority.',
          'solution': [table(['Item', 'Basis', '₹ crore'], [
              ['Admitted amounts', 'Paid in full', inr(adm)],
              ['Disputed tax', '90 − 6', inr(disp)],
              ['10% of disputed tax', 'Cap ₹20 crore', inr(pd)],
              ['Total deposit', 'Admitted + pre-deposit', inr(tot)]], title='Section 107(6)')],
          'checks': list(ck)}

    c2 = Checks()
    t1 = c2.add('min(300*0.10,40)', 'Pre-deposit for IGST appeal before the Tribunal (₹ crore)')
    i2 = {'id': 'i2', 'title': 'Pre-deposit before the Tribunal', 'difficulty': 'core', 'minutes': 5,
          'q': 'The Appellate Authority confirms an IGST demand of ₹300 crore against Sahyadri Logistics, all of which remains in dispute. Compute the further pre-deposit for appealing to the Tribunal.',
          'solution': [table(['Item', 'Basis', '₹ crore'], [
              ['10% of disputed IGST', '₹30 crore', '30'],
              ['Cap under IGST law', '₹40 crore', '40'],
              ['Pre-deposit', 'Lower of the two', inr(t1)]], title='Section 112(8)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'An aggrieved person may appeal against an adjudicating authority\'s order to the Appellate Authority in Form GST APL-01 within 3 months of communication of the order; a further month may be condoned for sufficient cause. The department, through an officer authorised by the Commissioner, may apply within 6 months in Form GST APL-03.',
            'The Appellate Authority hears the appellant, may allow additional grounds where the omission was not wilful, grants at most three adjournments, and may confirm, modify or annul the order. It cannot remand the matter back to the adjudicating authority.',
            'Where the order is likely to increase penalty, fine or confiscation value, or to reduce a refund or ITC, a hearing must be given; a higher tax or wrong ITC demand needs a show cause notice within the time limits of sections 73, 74 or 74A. The authority should try to decide within one year of filing.'],
          'First appeal within three months, one extra month for cause.',
          'An order communicated on 28 September can be appealed until 28 December.'),
        C('c2', T2, [
            'Under section 108, the Revisional Authority may call for records of a subordinate officer\'s proceedings, on his own or on information or request from the State Commissioner, and revise an order that is erroneous and prejudicial to revenue, illegal or improper, ignores material facts, or follows an audit observation by the CAG.',
            'Before an adverse order, the person must be given notice and hearing. The authority may enhance, modify or annul the order and can stay its operation meanwhile.',
            'Revision is barred where the order is under appeal, where the appeal time has not expired (or more than 3 years have passed since the order), or where the issue was already revised. Non-appealable orders listed in section 121 are outside both appeal and revision.'],
          'Revision is the department\'s internal correction route.',
          'An order ignoring an inward invoice register can be revised within three years.'),
        C('c3', T3, [
            'Appeals against orders of the Appellate or Revisional Authority go to the GST Appellate Tribunal in Form GST APL-05 within 3 months of communication, condonable by a further 3 months. For orders communicated before 1 April 2026 the backlog window has been notified, with the last date extended to 31 July 2026. The Tribunal may refuse admission where the tax, ITC, fine, fee or penalty involved is ₹50,000 or less.',
            'Appeals from State Benches lie to the High Court within 180 days, but only for appeals raising a substantial legal question, which the court frames and then answers. Orders of the Principal Bench (place of supply issues) go directly to the Supreme Court.',
            'The Supreme Court also hears appeals from High Court judgments certified as fit. Interest on refund of pre-deposit runs from the date of payment till refund.'],
          'Tribunal, then High Court on law, then Supreme Court.',
          'A place of supply dispute decided by the Principal Bench goes straight to the Supreme Court.'),
        C('c4', T4, [
            'Before the Appellate Authority, the appellant pays in full the tax, interest, fine, fee and penalty admitted, plus 10% of the remaining tax in dispute, capped at ₹20 crore each for CGST and SGST (₹40 crore for IGST). For a penalty-only order the deposit is 10% of the penalty.',
            'Before the Tribunal a further 10% of the remaining tax in dispute is required, capped at ₹20 crore (₹40 crore IGST). Payment of the pre-deposit stays recovery of the balance.',
            'To reduce litigation, the department files appeals only above monetary limits — ₹20 lakh for the Tribunal, ₹1 crore for the High Court and ₹2 crore for the Supreme Court — subject to listed exceptions such as constitutional validity questions.'],
          'Pay ten percent to keep the appeal and freeze recovery.',
          'Disputed CGST of ₹84 crore needs a pre-deposit of ₹8.4 crore.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Appeal filing calendar', 'role': 'Indirect tax manager',
             'situation': 'An adverse adjudication order has just been received.',
             'steps': ['Note date of communication.', 'Compute admitted amount and pre-deposit.', 'File APL-01 within three months.', 'Track hearing and adjournments.'],
             'takeaway': 'Missing the window forfeits the appeal right.'}]

    mcqs = [
        Q('m1', 'Time limit for an aggrieved person to appeal to the Appellate Authority is:', ['Three months from communication', 'Six months from the order', 'Thirty days', 'One year'], 0,
          'Section 107(1). In practice: one month condonable.', 'c1', T1),
        Q('m2', 'The Appellate Authority can grant a maximum of how many adjournments?', ['Three', 'Two', 'Five', 'Unlimited'], 0,
          'Section 107(9). In practice: plan readiness.', 'c1', T1),
        Q('m3', 'Pre-deposit before the Appellate Authority on disputed CGST is:', ['Ten percent capped at twenty crore rupees', 'Twenty percent capped at fifty crore', 'Seven and a half percent', 'Twenty-five percent'], 0,
          'Section 107(6). In practice: plus admitted amount.', 'c4', T4),
        Q('m4', 'Revision is barred after what period from the order?', ['Three years', 'One year', 'Five years', 'Six months'], 0,
          'Section 108(2). In practice: time excluded for stay.', 'c2', T2),
        Q('m5', 'Form for appeal to the GST Appellate Tribunal is:', ['GST APL-05', 'GST APL-01', 'GST APL-03', 'GST DRC-03'], 0,
          'Rule 110. In practice: e-filing.', 'c3', T3),
        Q('m6', 'Appeals to the High Court are allowed when the case involves:', ['A substantial question of law', 'Any question of fact', 'Tax above one lakh rupees', 'Penalty only'], 0,
          'Section 117. In practice: questions are framed.', 'c3', T3),
        Q('m7', 'Monetary limit for department appeals to the Tribunal is:', ['Twenty lakh rupees', 'One crore rupees', 'Two crore rupees', 'Fifty lakh rupees'], 0,
          'Instruction on litigation. In practice: exceptions apply.', 'c4', T4),
        Q('m8', 'Appeals against Principal Bench orders lie to:', ['The Supreme Court', 'The High Court', 'The State Bench', 'The Appellate Authority'], 0,
          'Section 118. In practice: place of supply cases.', 'c3', T3),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Admitted amount', 1, 'computation', 'admitted', nums=[adm]), S('s2', 'Disputed tax', 2, 'computation', '84', nums=[disp]), S('s3', 'Pre-deposit and total', 2, 'computation', '10%', nums=[pd, tot])],
          ['Apply the cap.'], ['Computing 10% on penalty also.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', '10% of IGST', 2, 'computation', '30'), S('s2', 'Cap', 2, 'computation', '40', nums=[t1])],
          ['Use IGST cap.'], ['Using ₹20 crore cap for IGST.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Can the Appellate Authority remand a case?', 'The authority must decide the appeal itself by confirming, modifying or annulling; remand power is absent under section 107.',
          [P('p1', 'Confirm or modify', 5, 'confirm'), P('p2', 'Annul', 5, 'annul')], 'c1'),
        V('v2', 'What triggers revision under section 108?', 'An order erroneous and prejudicial to revenue, illegal or improper, ignoring material facts, or flagged by a CAG observation.',
          [P('p1', 'Prejudicial', 5, 'prejudicial'), P('p2', 'CAG', 5, 'cag')], 'c2'),
        V('v3', 'What is the effect of paying pre-deposit?', 'Recovery of the balance amount is deemed stayed till the appeal is decided.',
          [P('p1', 'Stayed', 5, 'stay'), P('p2', 'Balance', 5, 'balance')], 'c4'),
        V('v4', 'From when is interest on refund of pre-deposit payable?', 'From the date of payment of the deposit till its refund, at the rate under section 56.',
          [P('p1', 'Date of payment', 5, 'date of payment'), P('p2', 'Section 56', 5, '56')], 'c3'),
        V('v5', 'When may the Tribunal refuse to admit an appeal?', 'The Tribunal may refuse admission when the tax, ITC, fine, fee or penalty involved is ₹50,000 or less.',
          [P('p1', 'Fifty thousand', 5, '50,000'), P('p2', 'Refuse', 5, 'refuse')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Delayed appeal', 'difficulty': 'core',
              'case': 'Pavitra Textiles received an order on 10 January. It wants to appeal to the Appellate Authority, and its disputed SGST is ₹40 lakh.',
              'mcqs': [
                  M('k1a', 'Normal last date for appeal is:', ['Tenth of April', 'Tenth of February', 'Tenth of July', 'Tenth of March'], 0,
                    'Three months. In practice: count from communication.', 'core', topic=T1),
                  M('k1b', 'Latest date with condonation is:', ['Tenth of May', 'Tenth of April', 'Tenth of June', 'Tenth of July'], 0,
                    'One extra month. In practice: show sufficient cause.', 'core', topic=T1),
                  M('k1c', 'Pre-deposit on disputed SGST (₹ lakh):', ['4', '8', '10', '2'], 0,
                    '10% of 40. In practice: paid separately for CGST too.', 'core', check=4, topic=T4),
                  M('k1d', 'Form for this appeal:', ['GST APL-01', 'GST APL-05', 'GST APL-03', 'GST RFD-01'], 0,
                    'Taxpayer appeal form. In practice: e-filed.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch22', 1, 'Appeals and Revision under GST',
                ['Apply the appeal procedure before the Appellate Authority.',
                 'Explain revisional powers and their limits.',
                 'Trace appeals to the Tribunal, High Court and Supreme Court.',
                 'Compute mandatory pre-deposits and apply monetary limits.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p5-ch21-u01'],
                 'exam_tip': 'In pre-deposit questions, separate admitted amounts from disputed tax and apply the cap per law.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['AA: 3 months + 1; department 6 months.', 'Revision: section 108; 3-year bar.', 'Tribunal: 3 months + 3; ₹50,000 threshold.',
                             'HC: 180 days, substantial question of law; Principal Bench → SC.', 'Pre-deposit 10%, cap ₹20 crore (₹40 crore IGST).'],
                 'remember': ['Department appeal limits: ₹20 lakh / ₹1 crore / ₹2 crore.'],
                 'traps': ['Applying 10% to admitted amounts.']},
                [('First appeal', 'Section 107'), ('Revision', 'Section 108'), ('Tribunal', 'Section 112'), ('High Court', 'Section 117'), ('Supreme Court', 'Section 118')],
                viva, cases)
