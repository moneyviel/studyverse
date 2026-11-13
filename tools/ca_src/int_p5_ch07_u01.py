"""CA Intermediate · Paper 5 Auditing and Ethics · Chapter 7 Completion and Review.
Scope follows the ICAI study material; explanations, names and figures are original."""
from ikit import *

UID = 'int-p5-ch07-u01'
T1 = 'Subsequent events (SA 560)'
T2 = 'Going concern (SA 570)'
T3 = 'Evaluating misstatements (SA 450) and written representations (SA 580)'
T4 = 'Communicating with those charged with governance (SA 260, SA 265)'


def build():
    i1 = {'id': 'i1', 'title': 'Events after the year end', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'The audit of Narmada Textiles Ltd. for the year ended 31 March 2027 is in progress; the report is expected on 25 May 2027. Classify and state the auditor\'s response: (a) on 20 April a major customer, owing ₹80 lakh at 31 March, is declared insolvent; its losses had been mounting for a year; (b) on 5 May a fire destroys a warehouse with stock of ₹1.2 crore; (c) on 10 June, after the report is signed but before the financial statements are issued, the auditor learns that a 31 March inventory count sheet was duplicated.',
          'solution': [table(['Event', 'Type', 'Auditor\'s response'], [
              ['(a) Customer insolvency', 'Adjusting — gives evidence of a condition (doubtful recovery) existing at 31 March', 'Ensure the receivable is written down or provided for; obtain evidence of the condition'],
              ['(b) Warehouse fire', 'Non-adjusting — the condition arose after 31 March', 'Ensure disclosure of the nature and estimated effect if material'],
              ['(c) Duplicate count sheet found after report date', 'Fact that, had it been known, might have changed the report', 'Discuss with management; if the statements are amended, audit the change, extend subsequent-event procedures to the new report date and issue a new report']], title='SA 560')],
          'checks': []}

    i2 = {'id': 'i2', 'title': 'Can the company carry on?', 'difficulty': 'hard', 'minutes': 8,
          'q': 'Kaveri Airlines Ltd. has net current liabilities, a term loan due in four months without a renewal agreement, and has defaulted on lease rentals. Management prepares accounts on a going concern basis and discloses these facts fully, with plans to raise equity. The auditor concludes the going concern basis is appropriate but a material uncertainty exists. How should the auditor report? What if disclosure were inadequate, or if the auditor concluded the basis was inappropriate?',
          'solution': [table(['Situation', 'Report'], [
              ['Basis appropriate, material uncertainty adequately disclosed', 'Unmodified opinion, plus a separate going-concern uncertainty section that points readers to the relevant note'],
              ['Basis appropriate, material uncertainty not adequately disclosed', 'Qualified or adverse opinion, explaining the uncertainty in the basis for opinion'],
              ['Going concern basis inappropriate but used', 'Adverse opinion']], title='SA 570 reporting'),
              note('Management\'s assessment should cover at least twelve months from the balance sheet date; if it covers less, the auditor asks management to extend it.')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'SA 560 covers events between the balance sheet date and the auditor\'s report, and facts that become known after the report date. Two kinds: events that throw light on conditions already present on the balance sheet date (adjusting), and events showing conditions that arose afterwards (non-adjusting, disclosed if material).',
            'Up to the report date the auditor performs procedures to identify such events: understanding management\'s procedures, inquiry, reading minutes of meetings held after the year end, reviewing the latest interim figures, and obtaining written representations.',
            'After the report date the auditor has no duty to keep searching. If a fact becomes known before the statements are issued that might have changed the report, the auditor discusses it with management; if the statements are amended, he extends procedures and issues a new report. After issue, similar steps apply, and the auditor acts to prevent reliance if management does not amend.'],
          'The audit opinion speaks as of its date — events up to then must be considered.',
          'A court judgment in May confirming a liability that existed at 31 March requires a provision, not just a note.'),
        C('c2', T2, [
            'Under the going concern basis, an entity is assumed to continue in business for the foreseeable future, with assets realised and liabilities met in the normal course. Management assesses this; the auditor evaluates it under SA 570.',
            'Indicators: financial — net liabilities or net current liabilities, fixed-term borrowings near maturity without prospects of renewal, negative operating cash flows, heavy losses, arrears in dividends, inability to pay creditors; operating — loss of key management, key markets, licences or major suppliers, labour problems; other — non-compliance with capital or statutory requirements, pending legal cases that cannot be met.',
            'The auditor evaluates management\'s assessment (covering at least twelve months from the balance sheet date), considers events beyond that period, performs further procedures where doubt exists (evaluating plans, cash-flow forecasts, debt agreements, minutes), and obtains written representations.',
            'Reporting: appropriate basis with adequately disclosed material uncertainty — unmodified opinion plus a "Material Uncertainty Related to Going Concern" section; inadequate disclosure — qualified or adverse; inappropriate basis — adverse; management unwilling to assess — consider implications.'],
          'Going concern is the quiet assumption under every balance sheet; the auditor must test it.',
          'An entity that has lost its only operating licence faces a serious going concern doubt.'),
        C('c3', T3, [
            'SA 450: the auditor accumulates misstatements identified, other than clearly trivial ones, and considers whether the overall strategy and plan need revision if misstatements suggest others may exist or near materiality.',
            'All accumulated misstatements are communicated to the appropriate level of management with a request to correct them. For uncorrected ones, the auditor re-assesses materiality, judges whether they are material individually or in aggregate (considering size, nature and circumstances), communicates them to those charged with governance, and obtains a written representation that management believes their effect is immaterial.',
            'SA 580: written representations are a letter from management to the auditor confirming responsibility for preparing the financial statements, providing all relevant information and recording all transactions, and other matters required by SAs. Its date should be close to the report date and never later than it.',
            'Representations do not replace other evidence. If management refuses the representations required by SA 580, or the auditor doubts management\'s integrity so that they are unreliable, the auditor disclaims an opinion.'],
          'Uncorrected errors are weighed together, and management\'s promises are written down — but never treated as proof on their own.',
          'Ten small cut-off errors that are individually trivial can together be material.'),
        C('c4', T4, [
            'SA 260: the auditor communicates with those charged with governance (TCWG) about: the auditor\'s responsibilities; planned scope and timing of the audit; significant findings (views on accounting practices, significant difficulties, significant matters discussed with management, written representations requested, and other significant matters); and, for listed entities, independence.',
            'Communication should be timely and two-way; significant findings are communicated in writing where oral communication would not be adequate, and oral communications are documented.',
            'SA 265: deficiencies in internal control identified during the audit are evaluated; significant deficiencies are communicated in writing to TCWG on a timely basis, and to management too (unless inappropriate); other deficiencies of sufficient importance are communicated to management. The communication explains the deficiencies, their potential effects, and that the audit was not designed to express an opinion on internal control.'],
          'Governance needs the auditor\'s honest view — in writing when it matters.',
          'A lack of review over journal entries posted by the CFO is a significant deficiency to report in writing to the audit committee.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Completion checklist', 'role': 'Audit senior',
             'situation': 'The partner asks for a completion memo before signing.',
             'steps': ['Run subsequent-event procedures up to the report date.', 'Document the going concern evaluation.', 'Summarise uncorrected misstatements against materiality.', 'Obtain the representation letter dated close to the report.', 'Confirm communications with TCWG and on control deficiencies.'],
             'takeaway': 'Completion procedures bridge the year-end and the report date.'}]

    mcqs = [
        Q('m1', 'An event after the balance sheet date that provides evidence of conditions existing at that date is:', ['An adjusting event', 'A non-adjusting event', 'A contingent asset', 'Irrelevant to the audit'], 0,
          'Such events require adjustment of amounts. Events arising after the date are disclosed if material. In practice: insolvency of a debtor with a long history of losses is adjusting.', 'c1', T1),
        Q('m2', 'After the report date, the auditor\'s duty to perform procedures on subsequent events:', ['Ends, but he must act on facts that come to his notice', 'Continues for a year', 'Continues until the AGM', 'Never existed'], 0,
          'SA 560 places no obligation to search after the report date; facts that become known must still be considered. In practice: discuss with management.', 'c1', T1),
        Q('m3', 'Management\'s going concern assessment should cover at least:', ['Twelve months from the balance sheet date', 'Six months', 'Three years', 'The audit period only'], 0,
          'SA 570 refers to at least twelve months from the date of the financial statements. In practice: ask management to extend a shorter assessment.', 'c2', T2),
        Q('m4', 'Going concern basis appropriate, material uncertainty adequately disclosed. Opinion:', ['Unmodified, with a separate material uncertainty section', 'Qualified', 'Adverse', 'Disclaimer'], 0,
          'Adequate disclosure keeps the opinion unmodified; the separate section draws attention. In practice: refer to the specific note.', 'c2', T2),
        Q('m5', 'Which is a financial indicator of going concern doubt?', ['Negative operating cash flows', 'Loss of a key supplier', 'Labour unrest', 'Pending changes in law'], 0,
          'Negative operating cash flows are a financial indicator; the others are operating or other indicators. In practice: look at trends.', 'c2', T2),
        Q('m6', 'Under SA 450, the auditor accumulates misstatements other than those that are:', ['Clearly trivial', 'Below materiality', 'Corrected by management', 'Judgemental'], 0,
          'Only clearly trivial items are excluded from accumulation. In practice: set a trivial threshold at planning.', 'c3', T3),
        Q('m7', 'The written representation letter should be dated:', ['Close to the auditor\'s report date and not later than it', 'On the balance sheet date', 'After the report date', 'At the start of the audit'], 0,
          'SA 580 requires the date to be close to the report date and never later. In practice: obtain it on signing day.', 'c3', T3),
        Q('m8', 'If management refuses the representations required by SA 580, the auditor:', ['Disclaims an opinion', 'Issues an unmodified opinion', 'Issues an emphasis of matter', 'Ignores it'], 0,
          'Refusal of fundamental representations leads to a disclaimer. In practice: consider management integrity too.', 'c3', T3),
        Q('m9', 'Significant deficiencies in internal control are communicated to TCWG:', ['In writing, on a timely basis', 'Orally only', 'Only if management agrees', 'In the auditor\'s report'], 0,
          'SA 265 requires written communication of significant deficiencies. In practice: other deficiencies go to management.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Adjusting event', 2, 'concept', 'adjusting|existed'), S('s2', 'Non-adjusting event', 2, 'concept', 'disclos|arose after'),
           S('s3', 'Fact after report date', 2, 'concept', 'new report|amend')],
          ['State the type, then the action.'], ['Adjusting accounts for the fire loss.'], ['Table.'], pad='table'),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Material uncertainty section', 2, 'concept', 'material uncertainty'), S('s2', 'Inadequate disclosure', 1.5, 'concept', 'qualified|adverse'),
           S('s3', 'Inappropriate basis', 1.5, 'concept', 'adverse')],
          ['Separate the three situations.'], ['Issuing an emphasis of matter for going concern.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What are the two types of subsequent events?', 'Events giving evidence of conditions existing at the balance sheet date, which need adjustment, and events showing conditions arising later, which need disclosure if material.',
          [P('p1', 'Adjusting', 5, 'existing|adjust'), P('p2', 'Non-adjusting', 5, 'arising|disclos')], 'c1'),
        V('v2', 'Give two operating indicators of going concern doubt.', 'Loss of key management without replacement and loss of a major market, licence or principal supplier.',
          [P('p1', 'Key management', 5, 'management'), P('p2', 'Market or supplier', 5, 'market|licence|supplier')], 'c2'),
        V('v3', 'What does SA 450 require for uncorrected misstatements?', 'The auditor assesses whether they are material individually or in aggregate, communicates them to those charged with governance and obtains a written representation about them.',
          [P('p1', 'Aggregate assessment', 5, 'aggregate|material'), P('p2', 'Communication and representation', 5, 'governance|representation')], 'c3'),
        V('v4', 'Can written representations replace audit evidence?', 'Representations are necessary evidence but are insufficient on their own; the auditor still obtains other sufficient appropriate evidence.',
          [P('p1', 'Insufficient alone', 6, 'insufficient|on their own'), P('p2', 'Other evidence', 4, 'other')], 'c3'),
        V('v5', 'What matters does SA 260 require to be communicated?', 'The auditor\'s responsibilities, planned scope and timing, significant findings from the audit, and independence for listed entities.',
          [P('p1', 'Responsibilities and scope', 5, 'responsibilit|scope'), P('p2', 'Findings and independence', 5, 'finding|independence')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Godavari Pharma Ltd.', 'difficulty': 'moderate',
              'case': 'During the audit of Godavari Pharma Ltd. for 2026-27, the auditor finds: (i) uncorrected misstatements of ₹6 lakh against materiality of ₹10 lakh; (ii) its drug licence for the main plant was suspended in May 2027 for six months; (iii) the CFO alone approves and posts all journals; (iv) management refuses to confirm in writing that all transactions have been recorded.',
              'mcqs': [
                  M('k1a', 'Point (i) requires the auditor to:', ['Request correction and obtain a written representation on the uncorrected items', 'Ignore them as below materiality', 'Issue an adverse opinion', 'Resign'], 0,
                    'All accumulated misstatements are communicated with a request to correct; uncorrected ones are evaluated and covered by representation. In practice: consider qualitative factors too.', 'moderate', topic=T3),
                  M('k1b', 'Point (ii) is relevant mainly to:', ['Going concern assessment and disclosure', 'Inventory count', 'Related party disclosures', 'Payroll'], 0,
                    'Loss of a key licence is an operating indicator of going concern doubt. In practice: evaluate management plans.', 'core', topic=T2),
                  M('k1c', 'Point (iii) should be communicated:', ['In writing to those charged with governance as a significant deficiency', 'Only orally to the CFO', 'In the audit report only', 'Not at all'], 0,
                    'Lack of segregation over journals is a significant deficiency under SA 265. In practice: also inform management.', 'moderate', topic=T4),
                  M('k1d', 'Point (iv) leads to:', ['A disclaimer of opinion', 'An unmodified opinion', 'An emphasis of matter', 'A qualified opinion only on revenue'], 0,
                    'Refusal of a fundamental SA 580 representation results in a disclaimer. In practice: document the refusal.', 'moderate', topic=T3),
              ]}]

    return unit(UID, 'p5', 'int-p5-ch07', 1, 'Completion and Review',
                ['Apply SA 560 to events after the balance sheet date.',
                 'Evaluate going concern and report under SA 570.',
                 'Evaluate misstatements and obtain written representations.',
                 'Communicate with those charged with governance and on control deficiencies.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 30}, 'prereq': ['int-p5-ch06-u01'],
                 'exam_tip': 'For case questions, name the SA, classify the issue, and end with the reporting consequence.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['SA 560: adjusting vs non-adjusting; procedures up to report date.',
                             'SA 570: indicators; 12-month assessment; MURGC section / qualified / adverse.',
                             'SA 450: accumulate beyond clearly trivial; request correction; aggregate.',
                             'SA 580: letter dated near report; refusal → disclaimer.',
                             'SA 260 / 265: communicate findings; significant deficiencies in writing.'],
                 'remember': ['Representations complement, never replace, evidence.'],
                 'traps': ['Going concern uncertainty is not reported as emphasis of matter.']},
                [('SA 560', 'Subsequent events'), ('SA 570', 'Going concern'), ('SA 450', 'Misstatements'), ('SA 580', 'Written representations')],
                viva, cases)
