"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 6 Completion and Review.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch06-u01'
T1 = 'Subsequent events (SA 560)'
T2 = 'Going concern (SA 570)'
T3 = 'Written representations (SA 580)'
T4 = 'Final review and completion'


def build():
    i1 = {'id': 'i1', 'title': 'Events after the balance sheet', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Year end 31 March; audit report dated 20 May; statements issued 30 May. Decide the auditor\'s duty: (a) on 10 April a major customer owing ₹3 crore at year end goes bankrupt; (b) on 25 May a fire destroys a warehouse; (c) on 15 June the auditor learns of a fraud that existed at year end and would have changed the report.',
          'solution': [table(['Event', 'Period', 'Auditor\'s duty'], [
              ['(a)', 'Before report date', 'Perform procedures to identify; adjusting event — ensure provision made'],
              ['(b)', 'After report date, before issue', 'No duty to search; if known, discuss with management; non-adjusting — ensure disclosure; amend report if statements amended'],
              ['(c)', 'After issue', 'Discuss with management; if statements revised, audit the revision and issue new report; if not, take action to prevent reliance']], title='SA 560 three periods')],
          'checks': []}

    i2 = {'id': 'i2', 'title': 'Going concern doubts', 'difficulty': 'hard', 'minutes': 8,
          'q': 'Arc Ltd. has net losses three years running, current liabilities exceeding current assets, and its main lender has recalled a loan. Management has negotiated a new loan, signed after year end, and disclosed the uncertainty fully. What report applies if (a) disclosure is adequate; (b) disclosure is inadequate; (c) going concern basis is clearly inappropriate?',
          'solution': [table(['Scenario', 'Report'], [
              ['(a) Material uncertainty adequately disclosed', 'Unmodified opinion with a separate "Material Uncertainty Related to Going Concern" section'],
              ['(b) Inadequate disclosure', 'Qualified or adverse opinion'],
              ['(c) Basis inappropriate', 'Adverse opinion']], title='SA 570 reporting')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Subsequent events are events between the date of the financial statements and the auditor\'s report, and facts discovered after the report date. Adjusting events give evidence of conditions at the year end; non-adjusting events relate to conditions arising after it.',
            'Up to the report date, the auditor actively performs procedures to identify subsequent events: enquiries of management, reading minutes and latest interim statements, and obtaining written representations.',
            'After the report date but before issue: no obligation to search, but if a fact becomes known, discuss with management; if statements are amended, extend procedures and issue a new or dual-dated report. After issue: if a fact would have caused a report amendment, discuss with management; if they revise, audit the revision and issue a new report with an emphasis of matter; if not, take action to prevent future reliance.'],
          'Active search before the report; respond to what you learn afterwards.',
          'A debtor bankrupt in April signals a year-end impairment.'),
        C('c2', T2, [
            'Under the going concern basis, an entity is assumed to continue for the foreseeable future. Management assesses this for at least twelve months from the year end; the auditor evaluates management\'s assessment and remains alert to events beyond that period.',
            'Indicators: financial (net liabilities, borrowings nearing maturity without renewal, adverse key ratios, losses, inability to pay creditors), operating (loss of key management, markets, licences or suppliers, labour problems) and other (legal or regulatory non-compliance, pending claims, changes in law).',
            'If events or conditions are identified, the auditor obtains evidence on management\'s plans and their feasibility, considers written representations, and concludes whether a material uncertainty exists, then reports accordingly (unmodified with a separate section, qualified/adverse for inadequate disclosure, or adverse if basis inappropriate).'],
          'Doubts about survival must be tested, disclosed and reported.',
          'A recalled loan with no refinancing points to material uncertainty.'),
        C('c3', T3, [
            'SA 580 requires written representations from management with appropriate responsibilities: that they have fulfilled their responsibility for preparing the statements and providing all information and access, and that all transactions are recorded and reflected.',
            'Other SAs require specific representations (fraud, laws, related parties, subsequent events, going concern, uncorrected misstatements, estimates).',
            'The representation letter carries a date as close as possible to the report date and never later than it. If management refuses or doubts arise about integrity, the auditor reassesses and may disclaim an opinion. Representations do not replace other evidence.'],
          'Written confirmations from management complement, never replace, evidence.',
          'If management refuses to sign the representation letter, a disclaimer may result.'),
        C('c4', T4, [
            'Completion involves final analytical procedures (SA 520) to check overall consistency, evaluation of misstatements (SA 450), review of working papers by the manager and partner, engagement quality control review where applicable, and confirming that sufficient appropriate evidence has been obtained.',
            'The auditor checks that disclosures are complete, subsequent events are addressed, going concern is concluded, and communications to TCWG are complete before dating the report.',
            'The audit file is assembled after the report date; changes afterwards are documented with reasons, and no evidence is deleted.'],
          'Before signing, step back and look at the whole picture.',
          'A final analytical review may reveal an unexplained jump in margins.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Closing the audit file', 'role': 'Audit manager',
             'situation': 'Fieldwork done; the report is due in five days.',
             'steps': ['Update subsequent events review.', 'Conclude on going concern.', 'Obtain signed representation letter.', 'Complete final analytics and partner review.'],
             'takeaway': 'Completion procedures protect the opinion.'}]

    mcqs = [
        Q('m1', 'The auditor\'s active duty to search for subsequent events ends at:', ['The date of the auditor\'s report', 'Year end', 'Date of AGM', 'Date of filing'], 0,
          'After that, respond to facts that become known. In practice: update enquiries.', 'c1', T1),
        Q('m2', 'Management\'s going concern assessment covers at least:', ['Twelve months from the end of the reporting period', 'Six months', 'Three years', 'The audit period only'], 0,
          'Auditor alert to later events. In practice: cash flow forecasts.', 'c2', T2),
        Q('m3', 'If a material uncertainty on going concern is adequately disclosed, the opinion is:', ['Unmodified with a separate material uncertainty section', 'Adverse', 'Disclaimer', 'Qualified always'], 0,
          'SA 570. In practice: not an emphasis of matter.', 'c2', T2),
        Q('m4', 'If the going concern basis is clearly inappropriate but used, the opinion is:', ['Adverse', 'Unmodified', 'Qualified', 'Unmodified with EOM'], 0,
          'Fundamental error. In practice: liquidation basis needed.', 'c2', T2),
        Q('m5', 'Written representations are dated:', ['As near as practicable to, but not after, the report date', 'At year end', 'After the report', 'At AGM'], 0,
          'SA 580. In practice: same day often.', 'c3', T3),
        Q('m6', 'If management refuses to provide written representations about its responsibilities, the auditor:', ['Disclaims an opinion', 'Issues unmodified opinion', 'Ignores', 'Qualifies on that item only'], 0,
          'Fundamental representations. In practice: reassess integrity.', 'c3', T3),
        Q('m7', 'Loss of a key licence is a going concern indicator of type:', ['Operating', 'Financial', 'Other', 'None'], 0,
          'SA 570 categories. In practice: also other indicators.', 'c2', T2),
        Q('m8', 'Final analytical procedures are performed to:', ['Check overall consistency of statements with the auditor\'s understanding', 'Replace substantive tests', 'Set materiality', 'Bill clients'], 0,
          'SA 520 near the end. In practice: investigate surprises.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Before report', 2, 'concept', 'adjusting|procedures'), S('s2', 'Before issue', 2, 'concept', 'no duty|discuss'), S('s3', 'After issue', 2, 'concept', 'revise|reliance')],
          ['Identify the period.'], ['Searching after the report date.'], ['Table.'], pad='table'),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Adequate', 2, 'concept', 'material uncertainty'), S('s2', 'Inadequate', 1.5, 'concept', 'qualified|adverse'), S('s3', 'Inappropriate', 1.5, 'concept', 'adverse')],
          ['Name the section.'], ['Using emphasis of matter.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Distinguish adjusting and non-adjusting subsequent events.', 'Adjusting events give evidence of conditions at the year end; non-adjusting events relate to conditions that arose after it.',
          [P('p1', 'Conditions at year end', 5, 'year end'), P('p2', 'Arose after', 5, 'arose after|after it')], 'c1'),
        V('v2', 'Name financial indicators of going concern doubt.', 'Net liabilities, borrowings nearing maturity without renewal, recurring losses and inability to pay creditors on time.',
          [P('p1', 'Liabilities and borrowings', 5, 'liabilit|borrowing'), P('p2', 'Losses or creditors', 5, 'loss|creditor')], 'c2'),
        V('v3', 'What must the auditor do when going concern doubts exist?', 'Evaluate management\'s plans and their feasibility, obtain evidence and representations, and conclude whether a material uncertainty exists.',
          [P('p1', 'Management plans', 5, 'plan'), P('p2', 'Material uncertainty', 5, 'material uncertainty')], 'c2'),
        V('v4', 'Can written representations replace other evidence?', 'They complement evidence and on their own fall short of sufficient appropriate evidence for matters they address.',
          [P('p1', 'Complement', 5, 'complement'), P('p2', 'Fall short', 5, 'fall short')], 'c3'),
        V('v5', 'What is done when a fact becomes known after the statements are issued?', 'Discuss with management; if they revise the statements, audit the revision and issue a new report; if not, act to prevent reliance on the report.',
          [P('p1', 'Revise and new report', 5, 'revis|new report'), P('p2', 'Prevent reliance', 5, 'reliance')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Wanderlust Travels Ltd.', 'difficulty': 'moderate',
              'case': 'A travel company\'s bookings fell 60% after a regional crisis. It has a term loan due in four months with no refinancing agreed. The board has approved a rights issue, underwritten by the promoter, and disclosed the uncertainty fully in the notes. Management has signed the representation letter.',
              'mcqs': [
                  M('k1a', 'The term loan due without refinancing is:', ['A going concern indicator', 'Irrelevant', 'An adjusting subsequent event', 'A related party issue'], 0,
                    'Financial indicator. In practice: assess plans.', 'core', topic=T2),
                  M('k1b', 'The underwritten rights issue is relevant as:', ['Management\'s plan to mitigate', 'A fraud indicator', 'A subsequent event only', 'Irrelevant'], 0,
                    'Evaluate feasibility, including promoter\'s ability to fund. In practice: obtain evidence.', 'moderate', topic=T2),
                  M('k1c', 'If material uncertainty remains with adequate disclosure, the report includes:', ['A separate Material Uncertainty Related to Going Concern section', 'An adverse opinion', 'A disclaimer', 'Nothing'], 0,
                    'SA 570. In practice: opinion unmodified.', 'core', topic=T2),
                  M('k1d', 'The representation letter should cover:', ['Going concern plans and other required matters', 'Only fees', 'Only inventory', 'Nothing specific'], 0,
                    'SA 580 and SA 570. In practice: dated near report date.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch06', 1, 'Completion and Review',
                ['Respond to subsequent events in each period.',
                 'Evaluate going concern and report accordingly.',
                 'Obtain and evaluate written representations.',
                 'Perform final review and completion procedures.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['fin-p3-ch05-u01'],
                 'exam_tip': 'Draw the timeline: year end → report date → issue date, and place each event on it.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['SA 560: three periods; active search until report date.',
                             'SA 570: 12-month assessment; indicators; reporting choices.',
                             'Material uncertainty adequately disclosed → separate section.',
                             'SA 580: dated near report date; refusal → disclaimer.',
                             'Final analytics and review before signing.'],
                 'remember': ['Going concern basis inappropriate → adverse.'],
                 'traps': ['Using an emphasis of matter for going concern uncertainty.']},
                [('SA 560', 'Subsequent events'), ('SA 570', 'Going concern'), ('SA 580', 'Representations'), ('SA 520', 'Final analytics')],
                viva, cases)
