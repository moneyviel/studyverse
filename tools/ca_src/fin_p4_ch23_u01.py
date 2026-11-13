"""CA Final · Paper 4 · Chapter 23 Advance Rulings.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch23-u01'
T1 = 'Meaning of advance ruling and eligible applicants'
T2 = 'Board for Advance Rulings and application'
T3 = 'Procedure, exclusions and pronouncement'
T4 = 'Void rulings and appeal'


def build():
    ck = Checks()
    f1 = ck.add('500000', 'Fee for non-resident transaction of ₹250 crore (₹)')
    f2 = ck.add('1000000', 'Fee for resident transaction of ₹400 crore (₹)')
    f3 = ck.add('10000', 'Fee for GAAR determination (other applicant) (₹)')
    i1 = {'id': 'i1', 'title': 'Who can apply and what fee?', 'difficulty': 'core', 'minutes': 6,
          'q': 'Determine eligibility and fee: (a) a non-resident\'s proposed transaction of ₹250 crore; (b) a resident\'s own transaction of ₹400 crore; (c) a resident\'s own transaction of ₹80 crore; (d) a resident seeking a ruling on whether a proposed arrangement is an impermissible avoidance arrangement.',
          'solution': [table(['Case', 'Eligibility', 'Fee (₹)'], [
              ['(a)', 'Non-resident — any amount', inr(f1)],
              ['(b)', 'Resident — ₹100 crore or more', inr(f2)],
              ['(c)', 'Resident below ₹100 crore — not eligible', '—'],
              ['(d)', 'GAAR determination — any person', inr(f3)]], title='Sections 380 and 383, Rule 200')],
          'checks': list(ck)}

    c2 = Checks()
    m = c2.add('6', 'Months available to pronounce ruling')
    d = c2.add('60', 'Days to appeal to the High Court')
    i2 = {'id': 'i2', 'title': 'Timeline of an advance ruling', 'difficulty': 'core', 'minutes': 4,
          'q': 'Zenith BV files an application received by the BAR on 1 June 2026. When must the ruling be pronounced, and within what time can either party appeal?',
          'solution': [table(['Step', 'Rule', 'Date / period'], [
              ['Withdrawal option', 'Within 30 days of application', 'Up to 1 July 2026'],
              ['Ruling', f'Within {m} months of receipt', 'By 1 December 2026'],
              ['Appeal to High Court', f'Within {d} days of communication (extendable for sufficient cause)', '—']], title='Sections 383, 384 and 389')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'An advance ruling (section 380(a)) is a determination by the Board for Advance Rulings on a question of law or fact about (i) a transaction undertaken or proposed by a non-resident; (ii) a resident\'s transaction with a non-resident, regarding the non-resident\'s liability; (iii) a resident\'s own transactions of ₹100 crore or more; (iv) a notified resident\'s (public sector company\'s) pending issue of income computation; or (v) whether an arrangement proposed by any person is an impermissible avoidance arrangement under GAAR.',
            'The applicant must fall in one of these categories; residents below the ₹100 crore threshold (other than public sector companies and GAAR questions) cannot apply.',
            'Advance rulings provide certainty before a transaction and reduce litigation, especially for cross-border structures.'],
          'Certainty upfront for significant or cross-border transactions.',
          'A non-resident planning to sell shares of an Indian company can seek a ruling on taxability.'),
        C('c2', T2, [
            'Section 381: the Central Government constitutes Boards for Advance Rulings, each with two members not below the rank of Chief Commissioner. Proceedings are not invalid merely because of a vacancy or defect in constitution (section 382).',
            'Section 383: application in the prescribed form, stating the question, with fees under Rule 200 — for non-resident transactions, ₹2 lakh (under ₹100 crore), ₹5 lakh (₹100–300 crore) and ₹10 lakh (above ₹300 crore); for resident transactions, ₹5 lakh (₹100–300 crore) and ₹10 lakh (above ₹300 crore); ₹10,000 in other cases.',
            'An application may be withdrawn within 30 days from the date of application.'],
          'Two senior members; fees scale with transaction size.',
          'A ₹250 crore non-resident transaction requires a fee of ₹5 lakh.'),
        C('c3', T3, [
            'Section 384: the BAR sends a copy of the application to the PCIT/CIT and calls for records. It may allow or reject the application but cannot allow it where the question is already pending before an income-tax authority, the Tribunal or a court (except for notified public sector companies), involves determination of fair market value of property, or relates to a transaction or issue designed prima facie for avoidance of tax (except a GAAR determination).',
            'No application is rejected without hearing, and reasons are recorded. If allowed, the BAR examines further material and pronounces its ruling within six months of receipt, giving a hearing if requested (through an authorised representative if desired).',
            'Signed copies of the ruling go to the applicant and the PCIT/CIT. The BAR has civil-court powers and regulates its own procedure (sections 387, 388).'],
          'Pending, valuation and avoidance questions are kept out.',
          'A question already before the CIT(A) cannot be taken to the BAR.'),
        C('c4', T4, [
            'Section 386: if the BAR finds, on its own or on representation of the PCIT/CIT or applicant, that a ruling was obtained by fraud or misrepresentation of facts, it may declare the ruling void ab initio ; the Act then applies as if no ruling had been made.',
            'When the Act is applied after a void ruling, the period from the date of the ruling to the date of the order declaring it void is excluded. The BAR may also rectify mistakes apparent from the record before the AO gives effect to a ruling.',
            'Section 389: the applicant or the PCIT/CIT may appeal to the jurisdictional High Court within 60 days of communication of the ruling or order (condonable for sufficient cause).'],
          'Fraud voids a ruling; appeals go straight to the High Court.',
          'A ruling based on suppressed facts can be declared void from the start.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Advance ruling application', 'role': 'International tax manager',
             'situation': 'A foreign investor plans a ₹350 crore acquisition through a holding structure.',
             'steps': ['Confirm applicant category and fee.', 'Frame precise questions.', 'Check no issue is pending or valuation-based.', 'Prepare facts fully to avoid a void ruling.'],
             'takeaway': 'A well-framed question gets a usable ruling.'}]

    mcqs = [
        Q('m1', 'A resident can seek a ruling on its own transactions if they total at least:', ['One hundred crore rupees', 'Fifty crore rupees', 'Three hundred crore rupees', 'Ten crore rupees'], 0,
          'Section 380. In practice: fee scales up.', 'c1', T1),
        Q('m2', 'Each Board for Advance Rulings has:', ['Two members', 'Three members', 'One member', 'Five members'], 0,
          'Section 381. In practice: not below Chief Commissioner rank.', 'c2', T2),
        Q('m3', 'Fee for a non-resident transaction above ₹300 crore is:', ['Ten lakh rupees', 'Five lakh rupees', 'Two lakh rupees', 'Ten thousand rupees'], 0,
          'Rule 200. In practice: with application.', 'c2', T2),
        Q('m4', 'An application may be withdrawn within:', ['Thirty days of application', 'Sixty days', 'Six months', 'Any time before ruling'], 0,
          'Section 383(3). In practice: fee not refunded.', 'c2', T2),
        Q('m5', 'The BAR cannot allow an application involving:', ['Determination of fair market value of property', 'A proposed transaction', 'A non-resident\'s liability', 'GAAR determination'], 0,
          'Exclusion. In practice: valuation disputes.', 'c3', T3),
        Q('m6', 'The ruling must be pronounced within:', ['Six months of receipt', 'Three months', 'One year', 'Sixty days'], 0,
          'Section 384. In practice: hearing on request.', 'c3', T3),
        Q('m7', 'A ruling obtained by fraud can be:', ['Declared void ab initio', 'Only modified', 'Ignored by the AO without order', 'Appealed only'], 0,
          'Section 386. In practice: after hearing.', 'c4', T4),
        Q('m8', 'Appeal against an advance ruling lies to:', ['The High Court within sixty days', 'The Tribunal', 'The CIT(A)', 'The Supreme Court directly'], 0,
          'Section 389. In practice: delay condonable.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Eligibility', 2, 'analysis', '100 crore'), S('s2', 'Fees', 3, 'computation', 'fee', nums=[f1, f2, f3])],
          ['Cite thresholds.'], ['Allowing small resident transactions.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Ruling time', 1.5, 'analysis', 'six months', nums=[m]), S('s2', 'Appeal time', 1.5, 'analysis', '60 days', nums=[d])],
          ['Mention withdrawal window.'], ['Assuming appeal to Tribunal.'], ['Timeline.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Can a public sector company seek a ruling on a pending issue?', 'Yes, as a notified resident it may apply even if the question is pending before an income-tax authority or the Tribunal.',
          [P('p1', 'Notified resident', 5, 'notified'), P('p2', 'Pending', 5, 'pending')], 'c3'),
        V('v2', 'What happens to limitation after a ruling is declared void?', 'The period from the date of the ruling to the order declaring it void is excluded when applying the time limits.',
          [P('p1', 'Excluded', 5, 'excluded'), P('p2', 'Time limits', 5, 'time limit')], 'c4'),
        V('v3', 'Who receives a copy of the ruling?', 'The applicant and the PCIT or CIT concerned.',
          [P('p1', 'Applicant', 5, 'applicant'), P('p2', 'Commissioner', 5, 'pcit|cit')], 'c3'),
        V('v4', 'Can GAAR questions be referred to the BAR?', 'Yes, any person may seek a determination whether a proposed arrangement is an impermissible avoidance arrangement.',
          [P('p1', 'Any person', 5, 'any person'), P('p2', 'Impermissible avoidance', 5, 'impermissible')], 'c1'),
        V('v5', 'Does a vacancy in the BAR invalidate its ruling?', 'Proceedings remain valid despite a vacancy or defect in its constitution.',
          [P('p1', 'Valid', 5, 'valid'), P('p2', 'Vacancy', 5, 'vacancy')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Harbour Infra Ltd', 'difficulty': 'core',
              'case': 'Harbour Infra Ltd, a resident, plans a series of transactions worth ₹180 crore and wants certainty on the tax treatment. One related issue is already before the CIT(A) for an earlier year.',
              'mcqs': [
                  M('k1a', 'Is Harbour an eligible applicant?', ['Yes, transactions are at least ₹100 crore', 'No, residents cannot apply', 'Only if non-resident is involved', 'Only for GAAR'], 0,
                    'Section 380. In practice: proposed transactions qualify.', 'core', topic=T1),
                  M('k1b', 'Fee payable (₹):', ['5,00,000', '2,00,000', '10,00,000', '10,000'], 0,
                    '₹100–300 crore band. In practice: Rule 200.', 'core', check=500000, topic=T2),
                  M('k1c', 'Can the BAR rule on the issue pending before the CIT(A)?', ['No, pending questions are excluded', 'Yes', 'Only with consent', 'Only after six months'], 0,
                    'Exclusion. In practice: not a PSU.', 'core', topic=T3),
                  M('k1d', 'Months within which the ruling must be pronounced:', ['6', '3', '12', '2'], 0,
                    'Section 384. In practice: from receipt.', 'core', check=6, topic=T3),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch23', 1, 'Advance Rulings',
                ['Explain advance rulings and eligible applicants.',
                 'Describe the BAR and the application process.',
                 'Apply procedure, exclusions and timelines.',
                 'Apply provisions on void rulings and appeals.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 15}, 'prereq': ['fin-p4-ch22-u01'],
                 'exam_tip': 'Test applicant category, exclusions and fee before discussing procedure.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 380 meaning; resident ₹100 crore threshold.', 'Section 381 BAR: two members.', 'Fees ₹2/5/10 lakh; ₹10,000 others.',
                             'Section 384: exclusions; ruling in six months.', 'Section 386 void; section 389 appeal to HC in 60 days.'],
                 'remember': ['Withdraw within 30 days.'],
                 'traps': ['Taking a valuation question to the BAR.']},
                [('Advance ruling', 'Section 380'), ('BAR', 'Section 381'), ('Application', 'Section 383'), ('Procedure', 'Section 384'), ('Appeal', 'Section 389')],
                viva, cases)
