"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 10 Review of Financial Information.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch10-u01'
T1 = 'Review engagements on historical statements (SRE 2400)'
T2 = 'Review of interim financial information by the entity\'s auditor (SRE 2410)'
T3 = 'Review procedures: enquiry and analytics'
T4 = 'Review conclusions and reports'


def build():
    ck = Checks()
    gm1 = ck.add('round(30/100*100,2)', 'Gross margin in prior quarters (%)')
    gm2 = ck.add('round(45/110*100,2)', 'Gross margin in current quarter (%)')
    i1 = {'id': 'i1', 'title': 'An unexplained margin jump', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'While reviewing a listed company\'s quarterly results, the auditor notes gross profit of ₹45 crore on revenue of ₹110 crore this quarter, against ₹30 crore on ₹100 crore in earlier quarters, with no change in prices or product mix. What should the auditor do?',
          'solution': [table(['Step', 'Working / Action', 'Result'], [
              ['Previous margin', '30 ÷ 100', inr(gm1) + '%'],
              ['Current margin', '45 ÷ 110', inr(gm2) + '%'],
              ['Enquire', 'Ask management to explain the jump (cut-off, inventory valuation, cost allocation)', '—'],
              ['Additional procedures', 'If explanations are unsatisfactory, perform further procedures', '—'],
              ['Conclusion', 'If misstatement is confirmed and uncorrected, modify the conclusion', '—']], title='SRE 2410 analytics')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Choosing the review conclusion', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'In a review: (a) nothing has come to attention suggesting misstatement; (b) a material, non-pervasive misstatement exists; (c) a misstatement is material and pervasive; (d) management imposes a pervasive scope limitation. Give the conclusion in each.',
          'solution': [table(['Case', 'Conclusion'], [
              ['(a)', 'Unmodified (negative form) conclusion'],
              ['(b)', 'Qualified conclusion'],
              ['(c)', 'Adverse conclusion'],
              ['(d)', 'Disclaimer of conclusion']], title='Review conclusions')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'A review of historical financial statements (SRE 2400) gives limited assurance, worded negatively: the practitioner says they found no reason to think the statements depart from the framework.',
            'Procedures are primarily enquiry and analytical procedures, designed to reduce engagement risk to a level acceptable for limited assurance — much less work than an audit.',
            'The practitioner must comply with ethics, apply professional skepticism and judgement, and perform additional procedures if matters suggest material misstatement.'],
          'Reviews give limited assurance through enquiry and analytics.',
          'A small company\'s lender may accept reviewed rather than audited statements.'),
        C('c2', T2, [
            'SRE 2410 applies when the entity\'s own auditor reviews interim financial information (e.g. quarterly results of listed companies under SEBI LODR). The auditor\'s knowledge from the annual audit helps focus enquiries.',
            'The auditor updates understanding of the entity and internal control, reads minutes, considers prior misstatements, and checks that interim information agrees with records.',
            'Written representations are obtained; matters found are communicated to management and TCWG, including possible fraud or non-compliance.'],
          'The annual auditor reviews quarterly results using what they already know.',
          'A listed company\'s auditor issues a limited review report on quarterly results.'),
        C('c3', T3, [
            'Review procedures: enquiries of persons responsible for financial and accounting matters (on recording, changes in policies, unusual transactions, subsequent events, going concern, fraud and non-compliance), analytical procedures (comparisons with prior periods, budgets, expected relationships), and reading the information for consistency.',
            'If something suggests material misstatement, the practitioner performs additional procedures sufficient to conclude.',
            'Procedures are not designed to test controls or obtain corroborating evidence as in an audit.'],
          'Ask the right people and compare the right numbers.',
          'A sudden margin jump triggers follow-up enquiries.'),
        C('c4', T4, [
            'Conclusions: unmodified (negative assurance), qualified (material but not pervasive misstatement or limitation), adverse (material and pervasive misstatement) and disclaimer (material and pervasive limitation).',
            'The report identifies the information reviewed, responsibilities of management and the practitioner, explains that a review covers far less ground than an audit so no audit opinion is given, and gives the conclusion.',
            'If management refuses to correct misstatements, the practitioner communicates with TCWG and may need to consider withdrawal or modification.'],
          'Review conclusions mirror audit opinions but in negative form.',
          'A report says: "nothing has come to our attention..." for an unmodified conclusion.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Quarterly limited review', 'role': 'Audit senior',
             'situation': 'A listed client\'s Q2 results are due in 10 days.',
             'steps': ['Update understanding and read minutes.', 'Perform enquiries and analytics.', 'Follow up unusual items.', 'Obtain representations and draft the review report.'],
             'takeaway': 'Analytics plus sharp enquiries drive a good review.'}]

    mcqs = [
        Q('m1', 'A review engagement provides:', ['Limited assurance', 'Reasonable assurance', 'No assurance', 'Absolute assurance'], 0,
          'Negative form. In practice: less than audit.', 'c1', T1),
        Q('m2', 'Review of interim information by the entity\'s auditor is governed by:', ['SRE 2410', 'SRE 2400', 'SA 700', 'SRS 4400'], 0,
          'Entity\'s auditor. In practice: quarterly results.', 'c2', T2),
        Q('m3', 'Primary review procedures are:', ['Enquiry and analytical procedures', 'Confirmations and inspection', 'Tests of controls', 'Inventory counts'], 0,
          'Limited scope. In practice: follow up anomalies.', 'c3', T3),
        Q('m4', 'A material and pervasive misstatement in a review leads to:', ['An adverse conclusion', 'A qualified conclusion', 'A disclaimer', 'An unmodified conclusion'], 0,
          'Mirrors SA 705. In practice: describe basis.', 'c4', T4),
        Q('m5', 'The review report states that a review is:', ['Substantially less in scope than an audit', 'Equal to an audit', 'More than an audit', 'Not an assurance engagement'], 0,
          'Clarifies limits. In practice: no audit opinion.', 'c4', T4),
        Q('m6', 'If enquiries suggest material misstatement, the practitioner should:', ['Perform additional procedures', 'Ignore it', 'Issue unmodified conclusion', 'Resign immediately'], 0,
          'Sufficient to conclude. In practice: document.', 'c3', T3),
        Q('m7', 'A pervasive scope limitation imposed by management leads to:', ['A disclaimer of conclusion', 'An adverse conclusion', 'An unmodified conclusion', 'A qualified conclusion always'], 0,
          'Cannot conclude. In practice: communicate to TCWG.', 'c4', T4),
        Q('m8', 'Under SRE 2410, the auditor obtains:', ['Written representations from management', 'No representations', 'Bank confirmations always', 'Court orders'], 0,
          'Supports review. In practice: dated with report.', 'c2', T2),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Margins', 2, 'computation', 'margin', nums=[gm1, gm2]), S('s2', 'Enquiry', 1.5, 'concept', 'enquir|explain'), S('s3', 'Further action', 1.5, 'concept', 'additional|modify')],
          ['Quantify the change.'], ['Accepting the change unquestioned.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Unmodified and qualified', 2, 'concept', 'unmodified|qualified'), S('s2', 'Adverse and disclaimer', 2, 'concept', 'adverse|disclaimer')],
          ['Use the matrix.'], ['Giving positive opinion wording.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What assurance does a review give?', 'Limited assurance, expressed in negative form that nothing has come to attention suggesting the statements are misstated.',
          [P('p1', 'Limited assurance', 5, 'limited'), P('p2', 'Negative form', 5, 'negative|nothing has come')], 'c1'),
        V('v2', 'Why is SRE 2410 different from SRE 2400?', 'SRE 2410 is performed by the entity\'s own auditor, who uses knowledge from the annual audit; SRE 2400 is for other practitioners.',
          [P('p1', 'Entity\'s auditor', 5, 'own auditor|entity\'s auditor'), P('p2', 'Annual audit knowledge', 5, 'annual audit|knowledge')], 'c2'),
        V('v3', 'Name typical review enquiries.', 'Recording of transactions, changes in policies, unusual transactions, subsequent events, going concern and fraud or non-compliance.',
          [P('p1', 'Policies and transactions', 5, 'polic|transaction'), P('p2', 'Going concern or fraud', 5, 'going concern|fraud')], 'c3'),
        V('v4', 'What forms can a review conclusion take?', 'Unmodified, qualified, adverse or a disclaimer of conclusion.',
          [P('p1', 'Unmodified and qualified', 5, 'unmodified|qualified'), P('p2', 'Adverse and disclaimer', 5, 'adverse|disclaimer')], 'c4'),
        V('v5', 'What if management refuses to correct a misstatement found in a review?', 'Communicate with those charged with governance, modify the conclusion, and consider withdrawal if needed.',
          [P('p1', 'Governance', 5, 'governance'), P('p2', 'Modify or withdraw', 5, 'modify|withdraw')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Track Analytics Ltd.', 'difficulty': 'moderate',
              'case': 'The statutory auditor of Track Analytics, a listed company, reviews its Q3 results. Management has not recognised an impairment the auditor estimates at ₹12 crore (materiality ₹8 crore), confined to one asset. Management also declines to provide access to board minutes for the quarter.',
              'mcqs': [
                  M('k1a', 'This engagement is governed by:', ['SRE 2410', 'SRE 2400', 'SA 700', 'SAE 3400'], 0,
                    'Entity\'s auditor reviewing interim results. In practice: SEBI LODR.', 'core', topic=T2),
                  M('k1b', 'The unrecognised impairment alone leads to:', ['A qualified conclusion', 'An adverse conclusion', 'A disclaimer', 'Unmodified'], 0,
                    'Material, confined to one item. In practice: quantify.', 'core', topic=T4),
                  M('k1c', 'Refusal of access to minutes is:', ['A scope limitation to discuss with TCWG', 'Acceptable', 'Irrelevant', 'An emphasis of matter'], 0,
                    'May lead to modified conclusion. In practice: assess pervasiveness.', 'moderate', topic=T4),
                  M('k1d', 'The main procedures for this review are:', ['Enquiry and analytics', 'Confirmations', 'Physical verification', 'Tests of controls'], 0,
                    'Limited scope. In practice: plus representations.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch10', 1, 'Review of Financial Information',
                ['Perform reviews of historical statements under SRE 2400.',
                 'Review interim financial information under SRE 2410.',
                 'Apply enquiry and analytical review procedures.',
                 'Form and report review conclusions.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 15}, 'prereq': ['fin-p3-ch09-u01'],
                 'exam_tip': 'Use negative-form wording in review conclusions.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Review = limited assurance.',
                             'SRE 2400 other practitioners; SRE 2410 entity\'s auditor.',
                             'Enquiry and analytics.',
                             'Unmodified, qualified, adverse, disclaimer.',
                             'Representations and TCWG communication.'],
                 'remember': ['Review is much less than an audit.'],
                 'traps': ['Using audit-opinion wording.']},
                [('SRE 2400', 'Other practitioner'), ('SRE 2410', 'Entity\'s auditor'), ('Assurance', 'Limited'), ('Form', 'Negative')],
                viva, cases)
