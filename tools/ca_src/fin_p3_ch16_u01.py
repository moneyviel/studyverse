"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 16 Internal Audit.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch16-u01'
T1 = 'Internal audit: meaning, applicability and scope'
T2 = 'Independence, qualities and performing the engagement'
T3 = 'Internal audit reports and the relationship with external audit'
T4 = 'Audit trail under the Companies Act'


def build():
    ck = Checks()
    t = ck.add('260', 'Turnover in the preceding year (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Is internal audit mandatory?', 'difficulty': 'core', 'minutes': 6,
          'q': 'Jade Pvt Ltd. has paid-up capital of ₹40 lakh and no loans; its turnover in the last three years was ₹49 crore, ₹145 crore and ₹260 crore (most recent). Must it appoint an internal auditor under section 138 and rule 13?',
          'solution': [table(['Test (private company)', 'Threshold', 'Jade'], [
              ['Turnover in preceding year', '₹200 crore or more', '₹' + inr(t) + ' crore — met'],
              ['Outstanding borrowings', 'Over ₹100 crore at any time in preceding year', 'Not met'],
              ['Conclusion', 'Either test suffices', 'Internal auditor must be appointed']], title='Section 138 applicability')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Using internal audit work', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'The statutory auditor wants to use the internal audit team\'s work on fixed asset verification. The internal audit head reports to the CFO, whose bonus depends on profit. What should be evaluated?',
          'solution': [table(['Factor', 'Evaluation'], [
              ['Objectivity', 'Reporting to CFO with profit-linked bonus may impair objectivity; check access to audit committee'],
              ['Competence', 'Qualifications, training and resources'],
              ['Systematic approach', 'Documented methodology and quality control'],
              ['Extent of use', 'Lower where judgement or risk is high; perform own procedures']], title='SA 610 evaluation')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Internal audit independently assures the board and management that controls and risk management are working, strengthening governance and helping the organisation achieve its objectives. ICAI\'s Internal Audit Standards Board issues Standards on Internal Audit (SIAs) and guidance.',
            'Section 138 with rule 13 requires internal auditors for listed companies, and unlisted public companies or private companies meeting thresholds (e.g. paid-up capital ₹50 crore or more for public companies, turnover ₹200 crore or more, borrowings over ₹100 crore, or deposits of ₹25 crore or more for public companies). The internal auditor may be a CA, cost accountant or other professional decided by the board, and may be an employee.',
            'Scope covers operational, financial, compliance and IT areas, risk management and governance, as decided by the board or audit committee.'],
          'Internal audit protects the organisation from the inside.',
          'A private company crossing ₹200 crore turnover must appoint an internal auditor.'),
        C('c2', T2, [
            'Integrity, objectivity and independence are essential: the internal auditor should have functional reporting to the audit committee, avoid conflicts, and not perform operational duties they later audit.',
            'Qualities: professional competence, skepticism, communication skills, understanding of business and technology, and ethical conduct.',
            'Performing the engagement: plan based on risk, understand processes, gather and analyse evidence, document work, review and communicate findings, and follow up on implementation.'],
          'Independence of mind and of reporting lines makes internal audit credible.',
          'An internal auditor reporting directly to the audit committee is more independent.'),
        C('c3', T3, [
            'Internal audit reports present observations, root causes, risk ratings, recommendations and management responses, communicated to management and the audit committee; assurance reports state the scope, criteria and conclusion.',
            'The external auditor may use internal audit work (SA 610) after evaluating the function\'s objectivity, competence and systematic approach, and may use internal auditors for direct assistance where not prohibited, under supervision, excluding significant judgements.',
            'Internal audit is a management function supporting governance; it does not replace management\'s responsibility for controls.'],
          'Internal and external auditors cooperate but stay distinct.',
          'Internal audit reports feed the audit committee\'s oversight.'),
        C('c4', T4, [
            'An audit trail (edit log) is a chronological record of changes to accounting data — who changed what, when, and old and new values — enabling tracing from reports back to source.',
            'Companies using accounting software must use software with an audit trail feature that records every transaction and edit, cannot be disabled, and is preserved for the statutory period (Companies (Accounts) Rules, proviso to rule 3(1)); auditors report on this under Rule 11(g).',
            'Internal auditors review audit trail configuration, access to change it, and exceptions such as back-dated or deleted entries.'],
          'Every edit must leave a footprint that cannot be switched off.',
          'An ERP setting that disables edit logs for some users breaches the rules.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Setting up internal audit', 'role': 'Head of internal audit',
             'situation': 'A company has just crossed section 138 thresholds.',
             'steps': ['Get board approval for scope and charter.', 'Build a risk-based annual plan.', 'Execute audits and report to the audit committee.', 'Review audit trail compliance.'],
             'takeaway': 'A charter and risk-based plan make internal audit effective.'}]

    mcqs = [
        Q('m1', 'Internal audit provides:', ['Independent assurance on controls and risk management', 'The statutory opinion', 'Tax filing', 'Marketing support'], 0,
          'Framework definition. In practice: governance support.', 'c1', T1),
        Q('m2', 'A private company must appoint an internal auditor if its preceding-year turnover is at least:', ['Two hundred crore rupees', 'Fifty crore rupees', 'One hundred crore rupees', 'Twenty-five crore rupees'], 0,
          'Rule 13. In practice: or borrowings over ₹100 crore.', 'c1', T1),
        Q('m3', 'The internal auditor under section 138 may be:', ['A CA, cost accountant or other professional decided by the board, including an employee', 'Only a CA firm', 'Only the statutory auditor', 'Only a government official'], 0,
          'Board decides. In practice: independence matters.', 'c1', T1),
        Q('m4', 'Independence of internal audit is strengthened by:', ['Functional reporting to the audit committee', 'Reporting to the CFO only', 'Performing operations', 'Bonus linked to profit'], 0,
          'Reduces pressure. In practice: charter.', 'c2', T2),
        Q('m5', 'An audit trail records:', ['Each change to accounting data with user, time and values', 'Only final balances', 'Only payments', 'Only tax data'], 0,
          'Edit log. In practice: cannot be disabled.', 'c4', T4),
        Q('m6', 'Auditors report on audit trail compliance under:', ['Rule 11(g)', 'CARO clause (i)', 'SA 700 only', 'Section 186'], 0,
          'Companies (Audit and Auditors) Rules. In practice: test settings.', 'c4', T4),
        Q('m7', 'Before using internal audit work, the external auditor evaluates:', ['Objectivity, competence and systematic approach', 'Only fees', 'Only size', 'Nothing'], 0,
          'SA 610. In practice: extent depends on risk.', 'c3', T3),
        Q('m8', 'Internal audit reports are mainly addressed to:', ['Management and the audit committee', 'Shareholders', 'Tax authorities', 'Customers'], 0,
          'Internal users. In practice: follow-up.', 'c3', T3),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Turnover test', 2, 'computation', 'turnover', nums=[t]), S('s2', 'Conclusion', 2, 'concept', 'appointed|must')],
          ['Use preceding year.'], ['Using paid-up capital test for private companies.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Objectivity', 2, 'concept', 'objectivity'), S('s2', 'Competence and approach', 2, 'concept', 'competence|systematic'), S('s3', 'Extent', 1, 'concept', 'extent')],
          ['Cite SA 610.'], ['Ignoring the reporting line.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Define internal audit.', 'An independent check that controls and risk processes work well, which strengthens governance and supports objectives.',
          [P('p1', 'Independent check', 5, 'independent'), P('p2', 'Controls and risk', 5, 'control|risk')], 'c1'),
        V('v2', 'Which companies need internal auditors under section 138?', 'Listed companies and unlisted public or private companies crossing thresholds of capital, turnover, borrowings or deposits.',
          [P('p1', 'Listed', 5, 'listed'), P('p2', 'Thresholds', 5, 'threshold|turnover')], 'c1'),
        V('v3', 'How is internal audit independence protected?', 'Through reporting to the audit committee, avoiding operational roles and conflicts, and unrestricted access.',
          [P('p1', 'Audit committee', 5, 'audit committee'), P('p2', 'Avoid conflicts', 5, 'conflict|operational')], 'c2'),
        V('v4', 'What is an audit trail?', 'A chronological record of changes to accounting data showing who changed what and when, with old and new values.',
          [P('p1', 'Chronological record', 5, 'chronological'), P('p2', 'Old and new values', 5, 'old and new')], 'c4'),
        V('v5', 'What does an internal audit report contain?', 'Observations, root causes, risk ratings, recommendations and management responses.',
          [P('p1', 'Observations and recommendations', 5, 'observation|recommendation'), P('p2', 'Management responses', 5, 'response')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'First Fintech Ltd.', 'difficulty': 'moderate',
              'case': 'First Fintech, a listed company, uses accounting software where the audit trail was switched off for two months during a migration. Its internal audit head also approves vendor payments. The statutory auditor wants to rely on internal audit\'s testing of payables.',
              'mcqs': [
                  M('k1a', 'Switching off the audit trail breaches:', ['The Companies (Accounts) Rules on audit trail', 'Nothing', 'SA 701', 'SEBI insider rules'], 0,
                    'Must not be disabled. In practice: report under Rule 11(g).', 'core', topic=T4),
                  M('k1b', 'The internal audit head approving payments impairs:', ['Objectivity of internal audit', 'Nothing', 'Sales controls', 'Inventory valuation'], 0,
                    'Self-review. In practice: segregate roles.', 'core', topic=T2),
                  M('k1c', 'The statutory auditor\'s reliance on internal audit for payables should be:', ['Limited after evaluating objectivity', 'Full', 'Mandatory', 'Ignored entirely without evaluation'], 0,
                    'SA 610 evaluation. In practice: more own work.', 'moderate', topic=T3),
                  M('k1d', 'As a listed company, First Fintech must:', ['Appoint an internal auditor', 'Avoid internal audit', 'Use only CAs as employees', 'Report to RBI'], 0,
                    'Section 138. In practice: board approves scope.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch16', 1, 'Internal Audit',
                ['Explain internal audit and section 138 applicability.',
                 'Maintain independence and perform internal audit engagements.',
                 'Report findings and relate internal and external audit.',
                 'Evaluate audit trail compliance.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 15}, 'prereq': ['fin-p3-ch15-u01'],
                 'exam_tip': 'Check rule 13 thresholds carefully — public and private companies differ.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Internal audit: assurance on controls and risk.',
                             'Section 138 / rule 13 thresholds.',
                             'Independence via audit committee reporting.',
                             'SA 610 for external auditor\'s use.',
                             'Audit trail: cannot be disabled; Rule 11(g).'],
                 'remember': ['Internal auditor may be an employee.'],
                 'traps': ['Applying the paid-up capital test to private companies.']},
                [('Section 138', 'Internal audit'), ('Turnover', '₹200 crore+'), ('Borrowings', '> ₹100 crore'), ('Audit trail', 'Rule 11(g)')],
                viva, cases)
