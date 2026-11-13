"""CA Final · Paper 5 · Chapter 23 Advance Ruling under GST.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch23-u01'
T1 = 'Scope of advance ruling and authorities'
T2 = 'Procedure before the AAR'
T3 = 'Appeal, rectification and binding effect'
T4 = 'Void rulings and the national appellate mechanism'


def build():
    ck = Checks()
    d1 = ck.add('30+30', 'Outer limit for appeal to AAAR including condonation (days)')
    d2 = ck.add('90', 'Time for AAR ruling from receipt of application (days)')
    i1 = {'id': 'i1', 'title': 'Advance ruling timeline', 'difficulty': 'core', 'minutes': 6,
          'q': 'Lumen Agro, a registered person, seeks an advance ruling on whether its drone-spraying service is a composite supply. Map the timeline from application to appeal.',
          'solution': [table(['Stage', 'Rule', 'Time'], [
              ['Application', 'Form on common portal, ₹5,000 fee each under CGST and SGST', '—'],
              ['Ruling', 'From receipt of application', f'{inr(d2)} days'],
              ['Appeal to AAAR', '30 days, extendable by 30 days', f'Up to {inr(d1)} days'],
              ['AAAR decision', 'From filing of appeal', '90 days']], title='Sections 98 to 101')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Is the question admissible?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Classify each question as admissible or not: (a) classification of a new snack; (b) rate on an item already under a pending show cause notice for the applicant; (c) whether the applicant must register; (d) place of supply of an inter-State consultancy service.',
          'solution': [table(['Question', 'Admissible?', 'Reason'], [
              ['(a)', 'Yes', 'Classification is listed in section 97(2)'],
              ['(b)', 'No', 'Issue is pending in proceedings for the applicant'],
              ['(c)', 'Yes', 'Registration requirement is a listed question'],
              ['(d)', 'No', 'Place of supply is outside the listed questions']], title='Section 97(2)')]}

    concepts = [
        C('c1', T1, [
            'An advance ruling is a binding decision by the Authority for Advance Ruling (AAR) or the Appellate Authority (AAAR) on listed questions about supplies proposed or already undertaken by the applicant. The applicant may be registered or seeking registration.',
            'Questions allowed under section 97(2): classification; applicability of a notification; time and value of supply; admissibility of ITC; liability to pay tax; whether registration is required; and whether a particular activity amounts to a supply. Place of supply is outside the list.',
            'Each State or UT has an AAR with one Central and one State member and an AAAR with the Chief Commissioner of Central Tax and the Commissioner of State tax. Rulings give certainty and help avoid costly disputes.'],
          'A pre-clearance on tax treatment, binding on both sides.',
          'A start-up can ask whether its subscription bundle is a mixed supply before launch.'),
        C('c2', T2, [
            'The application is made online with a fee of ₹5,000 each under CGST and SGST. The AAR sends a copy to the concerned officer, may call for records, and after hearing both sides passes an order admitting or rejecting it.',
            'An application is rejected where the question is already pending or decided in proceedings concerning the applicant; rejection requires a speaking order after hearing.',
            'Once admitted, the ruling must be pronounced within 90 days of receipt of the application after hearing both sides. If the two AAR members differ, the points go to the AAAR; if the AAAR members also differ, no ruling is given on that question.'],
          'Admission, hearing, ruling within ninety days.',
          'A query already part of an audit notice for the applicant will be rejected.'),
        C('c3', T3, [
            'The applicant, or the concerned or jurisdictional officer, may appeal to the AAAR within 30 days of receiving the ruling, extendable by another 30 days for sufficient cause. The AAAR decides within 90 days of filing after hearing the parties.',
            'Under section 102, the AAR or AAAR may correct an error apparent on the record within 6 months of its order, on its own or when pointed out; if the correction raises tax or cuts ITC, the applicant must be heard first.',
            'Under section 103, a ruling binds only the applicant and the concerned or jurisdictional officer for that applicant, and continues to bind until the law, facts or circumstances on which it rests change. It does not bind other similarly placed persons.'],
          'A ruling is personal to the applicant and lasts until the basis changes.',
          'A competitor cannot rely on another firm\'s advance ruling as binding.'),
        C('c4', T4, [
            'Section 104: where a ruling was obtained by fraud, suppression or misrepresentation of material facts, the authority may declare it void ab initio after hearing the applicant. The Act then applies as if no ruling existed, and the period from the ruling to the void order is excluded when computing limitation for demands.',
            'Sections 101A to 101D provided for a National Appellate Authority to settle conflicting rulings of different States, but it was never set up.',
            'From 1 April 2026, section 101A(1A) lets the Government, on Council recommendation, empower an existing authority, including a Tribunal, to hear such appeals in the interim; the study material notes the Principal Bench of the GST Appellate Tribunal for this role.'],
          'Rulings obtained by deception are wiped out retrospectively.',
          'A ruling based on hidden facts about sales channels can be declared void.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Drafting an advance ruling application', 'role': 'GST advisor',
             'situation': 'A client is launching a new product bundle.',
             'steps': ['Check the question falls in section 97(2).', 'Confirm no pending proceedings on it.', 'Disclose all facts fully.', 'Track the 90-day window.'],
             'takeaway': 'Full disclosure protects the ruling from being voided.'}]

    mcqs = [
        Q('m1', 'Advance ruling cannot be sought on:', ['Place of supply', 'Classification', 'Admissibility of ITC', 'Need for registration'], 0,
          'Not in section 97(2). In practice: frequent exam trap.', 'c1', T1),
        Q('m2', 'Fee for an advance ruling application is:', ['Five thousand rupees each under CGST and SGST', 'One thousand rupees total', 'Ten thousand under IGST only', 'No fee'], 0,
          'Rule 104. In practice: paid online.', 'c2', T2),
        Q('m3', 'The AAR must pronounce its ruling within:', ['Ninety days of receipt of the application', 'Thirty days', 'Six months', 'One year'], 0,
          'Section 98(6). In practice: after hearing.', 'c2', T2),
        Q('m4', 'Appeal against an AAR ruling must be filed within:', ['Thirty days, extendable by thirty days', 'Ninety days', 'Three months', 'Sixty days, no extension'], 0,
          'Section 100(2). In practice: sufficient cause.', 'c3', T3),
        Q('m5', 'Rectification under section 102 is allowed within:', ['Six months from the order', 'Three months', 'One year', 'Thirty days'], 0,
          'Error apparent on record. In practice: hearing if adverse.', 'c3', T3),
        Q('m6', 'An advance ruling binds:', ['Only the applicant and the concerned or jurisdictional officer', 'All taxpayers in the State', 'All taxpayers in India', 'Only the department'], 0,
          'Section 103. In practice: personal ruling.', 'c3', T3),
        Q('m7', 'A ruling obtained by misrepresentation may be declared:', ['Void ab initio', 'Valid prospectively', 'Suspended for a year', 'Binding on others'], 0,
          'Section 104. In practice: hearing needed.', 'c4', T4),
        Q('m8', 'If AAAR members differ on a referred point:', ['No advance ruling is given on that question', 'The Chairman decides', 'The applicant chooses', 'The High Court decides'], 0,
          'Section 98(5)/101(3). In practice: deemed no ruling.', 'c2', T2),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Application and ruling', 2, 'analysis', '90'), S('s2', 'Appeal window', 2, 'computation', '30', nums=[d1])],
          ['Mention fee.'], ['Using 90 days for appeal filing.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Admissible items', 2, 'analysis', 'classification'), S('s2', 'Inadmissible items', 2, 'analysis', 'pending')],
          ['Cite section 97(2).'], ['Treating place of supply as admissible.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'How long does an advance ruling stay binding?', 'Until the law, facts or circumstances supporting the ruling change.',
          [P('p1', 'Law', 5, 'law'), P('p2', 'Circumstances', 5, 'circumstances')], 'c3'),
        V('v2', 'What happens to limitation after a ruling is declared void?', 'The period from the ruling to the void order is excluded when computing limitation.',
          [P('p1', 'Excluded', 5, 'excluded'), P('p2', 'Limitation', 5, 'limitation')], 'c4'),
        V('v3', 'Who may appeal against an AAR ruling?', 'The applicant, or the concerned or jurisdictional officer.',
          [P('p1', 'Applicant', 5, 'applicant'), P('p2', 'Jurisdictional officer', 5, 'jurisdictional')], 'c3'),
        V('v4', 'Why was section 101A(1A) inserted?', 'Because the national appellate body for conflicting rulings was never set up, the Government may empower an existing authority, including a Tribunal, to hear those appeals.',
          [P('p1', 'Existing authority', 5, 'existing authority'), P('p2', 'Tribunal', 5, 'tribunal')], 'c4'),
        V('v5', 'Can a ruling be sought on an already completed transaction?', 'Yes, rulings cover supplies proposed or already undertaken by the applicant.',
          [P('p1', 'Proposed', 5, 'proposed'), P('p2', 'Undertaken', 5, 'undertaken')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Ruling and later change', 'difficulty': 'core',
              'case': 'Orchid Foods got a ruling that its packaged mix attracts 5% GST. A year later the rate notification is amended.',
              'mcqs': [
                  M('k1a', 'Does the ruling still bind after the amendment?', ['No, the law has changed', 'Yes, rulings are permanent', 'Only for two years', 'Only if renewed'], 0,
                    'Section 103(2). In practice: seek a fresh ruling.', 'core', topic=T3),
                  M('k1b', 'Can a competitor rely on this ruling as binding?', ['No', 'Yes', 'Only in the same State', 'Only if registered'], 0,
                    'Personal ruling. In practice: persuasive only.', 'core', topic=T3),
                  M('k1c', 'Where would Orchid appeal an adverse ruling?', ['Appellate Authority for Advance Ruling', 'High Court directly', 'Commissioner (Appeals)', 'Supreme Court'], 0,
                    'Section 100. In practice: within 30 days.', 'core', topic=T3),
                  M('k1d', 'If facts were suppressed, the ruling may be:', ['Declared void ab initio', 'Rectified only', 'Extended', 'Ignored by the applicant'], 0,
                    'Section 104. In practice: after hearing.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch23', 1, 'Advance Ruling under GST',
                ['Identify questions on which an advance ruling can be sought.',
                 'Apply the procedure before the AAR.',
                 'Apply appeal, rectification and binding-effect rules.',
                 'Explain void rulings and the national appellate mechanism.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['fin-p5-ch22-u01'],
                 'exam_tip': 'Check first whether the question is in section 97(2) and not pending for the applicant.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Seven listed questions; place of supply excluded.', 'Fee ₹5,000 each CGST and SGST; ruling in 90 days.', 'Appeal 30 + 30 days; AAAR in 90 days.',
                             'Rectification within 6 months.', 'Binding on applicant only; void if obtained by fraud.'],
                 'remember': ['Interim national appellate role under section 101A(1A) from 1 April 2026.'],
                 'traps': ['Assuming rulings bind all taxpayers.']},
                [('Questions', 'Section 97'), ('Procedure', 'Section 98'), ('Appeal', 'Sections 100–101'), ('Binding effect', 'Section 103'), ('Void', 'Section 104')],
                viva, cases)
