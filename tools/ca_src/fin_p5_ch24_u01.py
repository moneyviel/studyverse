"""CA Final · Paper 5 · Chapter 24 Miscellaneous Provisions under GST.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch24-u01'
T1 = 'Information, documents and evidence'
T2 = 'Saving of proceedings, rectification and rounding off'
T3 = 'Service of notices and computation of time'
T4 = 'Special procedures and other provisions'


def build():
    ck = Checks()
    r1 = ck.add('-(-48213.50//1)', 'Rounded tax where paise are fifty or more (₹)')
    r2 = ck.add('7305.49//1', 'Rounded interest where paise are below fifty (₹)')
    i1 = {'id': 'i1', 'title': 'Rounding off under section 170', 'difficulty': 'core', 'minutes': 4,
          'q': 'Varsha Traders computes tax payable of ₹48,213.50 and interest of ₹7,305.49. Round off both under section 170.',
          'solution': [table(['Amount', 'Paise', 'Rule', 'Rounded ₹'], [
              ['Tax ₹48,213.50', '50', 'Fifty paise or more: raise to next rupee', inr(r1)],
              ['Interest ₹7,305.49', '49', 'Below fifty paise: drop', inr(r2)]], title='Section 170')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Was the notice validly served?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'A show cause notice to Dhruv Exports was uploaded on the common portal on 4 March and also sent by speed post the same day. Dhruv says it never opened the portal. It later replied to the notice on merits. Can it now challenge the service?',
          'solution': [table(['Point', 'Rule', 'Conclusion'], [
              ['Portal upload', 'Section 169(1)(d) recognises it as a mode', 'Valid mode'],
              ['Date of service', 'Date on which it is made available', '4 March'],
              ['Replying on merits', 'Section 160(2): service acted upon cannot be questioned', 'Challenge barred']], title='Sections 160 and 169')]}

    concepts = [
        C('c1', T1, [
            'Sections 144 and 145 presume documents produced or seized to be true and signed by the person named, and admit microfilms, facsimiles and computer printouts as evidence subject to conditions. Section 155 places the burden of proving ITC eligibility on the person claiming it.',
            'Under section 151 the Commissioner may direct any person to furnish information on matters connected with the Act. Section 152 bars publishing such information in a way that identifies a person without written consent, or using it in proceedings without hearing the person; class-wise publication in public interest is allowed.',
            'Section 158A permits consent-based sharing of registration, return, invoice and e-way bill particulars with notified systems. Section 154 allows officers to take samples against a receipt.'],
          'Evidence rules favour records; the claimant proves ITC.',
          'A buyer claiming ITC must show invoice, receipt of goods and payment to supplier.'),
        C('c2', T2, [
            'Section 160 keeps assessments, notices, summons, appeals and similar proceedings alive despite a mistake, defect or omission, if in substance they conform to the Act. Service of a notice cannot be questioned once the person has acted on it or has not objected at the earliest stage.',
            'Under section 161 any authority may correct an error apparent on the face of record in its decision, order, notice or certificate, on its own, on an officer\'s pointing out, or on the affected person\'s request made within 3 months. The outer limit is 6 months from issue, except for purely clerical or arithmetical slips. A debatable point of law is outside its reach, and natural justice applies if the change is adverse.',
            'Section 170 rounds tax, interest, penalty, fine, refund and other sums to the nearest rupee: fifty paise or more go up, less than fifty paise are dropped. Invoices themselves need no rounding.'],
          'Substance over form; errors fixable within limits.',
          'A wrongly spelt name in a notice does not void the proceedings.'),
        C('c3', T3, [
            'Section 169 lists modes of serving notices: delivery to the person or an authorised representative, adult family member or employee; registered or speed post or courier with acknowledgement; e-mail given at registration; making it available on the common portal; newspaper publication; and, failing these, affixing at the last known place of business or on the office notice board.',
            'Service is deemed on the date of tendering, publication or affixing. Communication by registered or speed post is deemed received at the end of the normal transit period unless proven otherwise.',
            'Section 9 of the General Clauses Act, 1897: in counting periods, exclude the first day (the word "from") and include the last day (the word "to"). Section 172 lets the Government remove difficulties by order within 5 years of commencement.'],
          'Portal upload counts as valid service.',
          'Thirty days from 1 June ends on 1 July.'),
        C('c4', T4, [
            'Section 148 allows special procedures for registration, returns, payment and administration for notified classes. Examples include exemption from tax on advances for goods and the corporate insolvency procedure, under which a corporate debtor under CIRP (where it has defaulted in GSTR-1 or returns) takes fresh registration as a distinct person within 30 days of the IRP/RP\'s appointment.',
            'Section 149 provides for compliance ratings placed in the public domain. Section 156 treats officers as public servants; section 157 protects acts in good faith; section 162 bars civil courts, though appeals to High Courts and the Supreme Court remain.',
            'Section 164 allows rules (with penalty up to ₹10,000 for breach), section 168 lets the Board issue instructions for uniformity, and section 17 of the IGST Act apportions IGST between the Centre and States.'],
          'Enabling provisions keep the system flexible and fair.',
          'An IRP takes over GST compliance of a corporate debtor during insolvency.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Notice tracking', 'role': 'Compliance executive',
             'situation': 'Notices arrive on the portal, by e-mail and by post.',
             'steps': ['Check the portal daily.', 'Log date of service for each mode.', 'Compute reply deadline excluding the first day.', 'Seek rectification of obvious errors within 3 months.'],
             'takeaway': 'Missed portal notices still count as served.'}]

    mcqs = [
        Q('m1', 'Burden of proving ITC eligibility lies on:', ['The person claiming the credit', 'The proper officer', 'The supplier', 'The GST Council'], 0,
          'Section 155. In practice: keep documents.', 'c1', T1),
        Q('m2', 'Outer time limit for rectification under section 161 is:', ['Six months from issue', 'Three months', 'One year', 'Two years'], 0,
          'Clerical slips excepted. In practice: request within 3 months.', 'c2', T2),
        Q('m3', 'Under section 170, ₹1,234.50 becomes:', ['₹1,235', '₹1,234', '₹1,230', '₹1,240'], 0,
          'Fifty paise rounds up. In practice: invoices excluded.', 'c2', T2, check=1235),
        Q('m4', 'Which is a valid mode of service under section 169?', ['Making the notice available on the common portal', 'Text message only', 'Phone call', 'Social media post'], 0,
          'Section 169(1)(d). In practice: check portal.', 'c3', T3),
        Q('m5', 'Maximum penalty for breach of rules under section 164 is:', ['Ten thousand rupees', 'Twenty-five thousand rupees', 'Fifty thousand rupees', 'One lakh rupees'], 0,
          'Rule-making power. In practice: residual.', 'c4', T4),
        Q('m6', 'A corporate debtor under CIRP takes new registration within:', ['Thirty days of appointment of IRP or RP', 'Ninety days', 'Seven days', 'Six months'], 0,
          'Section 148 notification. In practice: distinct person.', 'c4', T4),
        Q('m7', 'Can a civil court decide a GST levy dispute?', ['No, section 162 bars it', 'Yes, always', 'Only below one lakh rupees', 'Only on consent'], 0,
          'Bar on civil courts. In practice: statutory appeals.', 'c4', T4),
        Q('m8', 'When counting a period "from" a date, the first day is:', ['Excluded', 'Included', 'Counted twice', 'Ignored only for holidays'], 0,
          'General Clauses Act. In practice: include last day.', 'c3', T3),
    ]

    questions = [
        W('q1', 3, i1['q'], i1['solution'],
          [S('s1', 'Tax rounding', 2, 'computation', 'fifty', nums=[r1]), S('s2', 'Interest rounding', 1, 'computation', 'below', nums=[r2])],
          ['State rule.'], ['Rounding invoices.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Mode and date', 2, 'analysis', 'portal'), S('s2', 'Bar on challenge', 2, 'analysis', 'acted upon')],
          ['Cite both sections.'], ['Assuming portal service needs reading.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What does section 160 protect?', 'It keeps proceedings valid despite a mistake, defect or omission when they conform in substance to the Act.',
          [P('p1', 'Substance', 5, 'substance'), P('p2', 'Defect', 5, 'defect')], 'c2'),
        V('v2', 'When can information under section 151 be published?', 'Identifying publication needs written consent of the person; class-wise publication in public interest is permitted.',
          [P('p1', 'Consent', 5, 'consent'), P('p2', 'Public interest', 5, 'public interest')], 'c1'),
        V('v3', 'What is a GST compliance rating?', 'A rating under section 149 based on compliance record, revised periodically and placed in the public domain.',
          [P('p1', 'Public domain', 5, 'public domain'), P('p2', 'Compliance record', 5, 'compliance record')], 'c4'),
        V('v4', 'Is a debatable legal point rectifiable under section 161?', 'Rectification covers only errors apparent on the face of record; debatable points of law fall outside it.',
          [P('p1', 'Apparent', 5, 'apparent'), P('p2', 'Debatable', 5, 'debatable')], 'c2'),
        V('v5', 'When is a speed-post notice deemed received?', 'At the end of the normal transit period, unless the contrary is proved.',
          [P('p1', 'Transit', 5, 'transit'), P('p2', 'Contrary', 5, 'contrary')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Arithmetic slip in an order', 'difficulty': 'core',
              'case': 'An order dated 2 January shows interest totalled wrongly by ₹9,000. The taxpayer notices it on 20 August.',
              'mcqs': [
                  M('k1a', 'Is this a clerical or arithmetical error?', ['Yes', 'No', 'Only if above ₹10,000', 'Only if adverse'], 0,
                    'Totalling slip. In practice: section 161 proviso.', 'core', topic=T2),
                  M('k1b', 'Does the six-month limit bar rectification?', ['No, arithmetical slips are excepted', 'Yes', 'Only for refunds', 'Only for penalties'], 0,
                    'Proviso to section 161. In practice: still apply.', 'core', topic=T2),
                  M('k1c', 'If the correction increases liability, the authority must:', ['Give a hearing', 'Correct silently', 'Refer to Tribunal', 'Seek court order'], 0,
                    'Natural justice. In practice: notice.', 'core', topic=T2),
                  M('k1d', 'Who can rectify the order?', ['The authority that passed it', 'Any civil court', 'The GST Council', 'The supplier'], 0,
                    'Section 161. In practice: same office.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch24', 1, 'Miscellaneous Provisions under GST',
                ['Apply provisions on information, evidence and burden of proof.',
                 'Apply saving of proceedings, rectification and rounding off.',
                 'Determine valid service of notices and compute time.',
                 'Explain special procedures and other enabling provisions.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['fin-p5-ch23-u01'],
                 'exam_tip': 'For service questions, identify the mode, its deemed date and whether the person acted on the notice.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 155: claimant proves ITC.', 'Section 160 saves defective proceedings.', 'Section 161: request 3 months, limit 6 months.',
                             'Section 169 modes include portal and e-mail.', 'Section 170 rounding to nearest rupee.'],
                 'remember': ['CIRP: fresh registration within 30 days of IRP/RP appointment.'],
                 'traps': ['Rounding individual invoices.']},
                [('Burden of proof', 'Section 155'), ('Saving', 'Section 160'), ('Rectification', 'Section 161'), ('Service', 'Section 169'), ('Rounding', 'Section 170')],
                viva, cases)
