"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 1 Quality Control.
Scope follows the ICAI study material (status of SQM 1/SQM 2 updated to ICAI's March 2026 deferment); explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch01-u01'
T1 = 'Audit quality and SQC 1 at firm level'
T2 = 'SA 220: quality control on each audit'
T3 = 'Engagement quality control review and documentation'
T4 = 'External review: Peer Review Board, Quality Review Board and NFRA'


def build():
    i1 = {'id': 'i1', 'title': 'Which SQC 1 element is weak?', 'difficulty': 'core', 'minutes': 7,
          'q': 'In R & Co., (a) partners push for fee growth regardless of risk; (b) a staff member holds shares in an audit client; (c) a client with doubtful integrity was accepted without enquiry; (d) juniors with no bank experience are sent to a bank audit; (e) working papers are not reviewed before signing; (f) no one checks whether firm policies are followed. Map each to the element of quality control.',
          'solution': [table(['Issue', 'SQC 1 element'], [
              ['(a)', 'Leadership responsibilities for quality within the firm'],
              ['(b)', 'Relevant ethical requirements (independence)'],
              ['(c)', 'Acceptance and continuance of client relationships'],
              ['(d)', 'Human resources (assignment of teams)'],
              ['(e)', 'Engagement performance (supervision and review)'],
              ['(f)', 'Monitoring']], title='Six elements of SQC 1')],
          'checks': []}

    i2 = {'id': 'i2', 'title': 'When is an EQCR needed?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Decide whether an engagement quality control review is required: (a) audit of a listed company; (b) audit of a small private company with no special risk; (c) audit of an unlisted public interest entity the firm\'s policy designates for EQCR; (d) tax audit of a proprietor.',
          'solution': [table(['Engagement', 'EQCR?', 'Reason'], [
              ['(a)', 'Yes', 'Mandatory for audits of listed entities'],
              ['(b)', 'No (unless firm criteria apply)', 'Firm sets criteria for others'],
              ['(c)', 'Yes', 'Meets firm\'s criteria'],
              ['(d)', 'Only if firm criteria apply', 'Not a listed audit']], title='EQCR')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Audit quality means a rigorous process that complies with laws and professional standards, giving users trust in the opinion. SQC 1 sets the firm-wide system of quality control for audits, reviews, other assurance and related services; SA 220 applies it to each audit engagement.',
            'SQC 1 elements: leadership responsibilities for quality (tone at the top, quality over commercial pressure); relevant ethical requirements including independence (annual confirmations, threats and safeguards, rotation for long associations with listed clients); acceptance and continuance of clients (integrity, competence, ability to comply with ethics); human resources (recruitment, training, assignment); engagement performance (direction, supervision, review, consultation, differences of opinion, EQCR); and monitoring (periodic inspection of completed engagements).',
            'Status: ICAI issued SQM 1, SQM 2 and revised SA 220 in October 2024, but in March 2026 it deferred their mandatory date until further announcement, so SQC 1 continues to apply.'],
          'Quality starts at the top and runs through six linked elements.',
          'A firm rewarding partners only for fee growth fails the leadership element.'),
        C('c2', T2, [
            'The engagement partner takes responsibility for overall audit quality: complying with ethics and independence, being satisfied with acceptance and continuance procedures, ensuring the team collectively has the right competence and time, and directing, supervising and reviewing the work.',
            'The partner ensures appropriate consultation on difficult or contentious matters, that conclusions are implemented, and that differences of opinion are resolved before the report is dated.',
            'Monitoring results from the firm are considered, and the partner remains alert to non-compliance with ethical requirements by team members.'],
          'Each audit has one partner accountable for its quality.',
          'A partner must consult the firm\'s technical team on a contentious Ind AS issue.'),
        C('c3', T3, [
            'An engagement quality control review (EQCR) is an objective evaluation, before the report is issued, of significant judgements made by the team and conclusions reached. It is required for audits of listed entities and other engagements meeting the firm\'s criteria.',
            'The reviewer considers the team\'s independence evaluation, significant risks and responses, judgements on materiality and significant risks, consultations, the appropriateness of the report, and documentation. The reviewer must be objective and suitably qualified, not part of the team.',
            'Documentation shows compliance with ethics and independence, acceptance conclusions, consultations, and that the EQCR was completed before the report date. Audit files are assembled within 60 days of the report date and retained for at least seven years (SQC 1).'],
          'A second, independent senior look before signing.',
          'The report cannot be dated before the EQCR is completed.'),
        C('c4', T4, [
            'The Peer Review Board of ICAI reviews practice units periodically to check compliance with technical standards and quality control, issuing a peer review certificate; certain audits (e.g. listed entities) require a valid certificate.',
            'The Quality Review Board (set up by the Central Government under the CA Act) reviews the quality of audit services and recommends improvements, guiding members.',
            'The National Financial Reporting Authority (NFRA), under the Companies Act, recommends accounting and auditing standards, monitors compliance, oversees the quality of service of auditors of listed and large companies, and can investigate and impose penalties.'],
          'Firms are reviewed by peers, by QRB and, for big companies, by NFRA.',
          'NFRA can debar an auditor for professional misconduct in a listed company audit.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Preparing for peer review', 'role': 'Quality manager in an audit firm',
             'situation': 'The firm\'s peer review is due in three months.',
             'steps': ['Map policies to the six SQC 1 elements.', 'Collect independence confirmations.', 'Run internal file inspections.', 'Fix gaps and document remediation.'],
             'takeaway': 'Quality systems must be documented and actually followed.'}]

    mcqs = [
        Q('m1', 'SQC 1 applies at the level of:', ['The firm', 'Each audit only', 'The client', 'Regulators'], 0,
          'SA 220 applies at engagement level. In practice: both work together.', 'c1', T1),
        Q('m2', 'An engagement quality control review is mandatory for:', ['Audits of listed entities', 'All audits', 'Tax audits only', 'Internal audits'], 0,
          'Plus others per firm criteria. In practice: before report is dated.', 'c3', T3),
        Q('m3', 'Audit files should normally be assembled within:', ['Sixty days of the report date', 'Thirty days', 'One year', 'Seven days'], 0,
          'SQC 1 guidance. In practice: retain 7 years.', 'c3', T3),
        Q('m4', 'Accepting a client without assessing management integrity breaches:', ['Acceptance and continuance procedures', 'Monitoring', 'Human resources', 'Documentation only'], 0,
          'One of the six elements. In practice: obtain background checks.', 'c1', T1),
        Q('m5', 'Under SA 220, overall responsibility for audit quality rests with:', ['The engagement partner', 'The client', 'The EQCR reviewer', 'Article assistants'], 0,
          'Partner accountability. In practice: direct and review.', 'c2', T2),
        Q('m6', 'As of 2026, firms in India must apply:', ['SQC 1, as SQM 1 and SQM 2 are deferred', 'SQM 1 only', 'ISQM of IAASB directly', 'No standard'], 0,
          'ICAI deferred SQMs in March 2026. In practice: watch for new date.', 'c1', T1),
        Q('m7', 'NFRA was constituted under:', ['The Companies Act, 2013', 'The CA Act, 1949', 'SEBI Act', 'RBI Act'], 0,
          'Section 132. In practice: oversees listed company audits.', 'c4', T4),
        Q('m8', 'Monitoring under SQC 1 includes:', ['Periodic inspection of completed engagements', 'Signing reports', 'Billing', 'Marketing'], 0,
          'Checks that the system works. In practice: cyclical file review.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Leadership and ethics', 2, 'concept', 'leadership|ethical'), S('s2', 'Acceptance and HR', 2, 'concept', 'acceptance|human'), S('s3', 'Performance and monitoring', 2, 'concept', 'performance|monitoring')],
          ['Name each element.'], ['Mixing monitoring with review.'], ['Table.'], pad='table'),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Listed', 2, 'concept', 'listed'), S('s2', 'Firm criteria', 2, 'concept', 'criteria')],
          ['Cite the rule.'], ['Saying EQCR is needed for every audit.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'List the elements of SQC 1.', 'Leadership, ethical requirements, acceptance and continuance, human resources, engagement performance and monitoring.',
          [P('p1', 'Leadership and ethics', 5, 'leadership|ethical'), P('p2', 'Performance and monitoring', 5, 'performance|monitoring')], 'c1'),
        V('v2', 'What does an EQCR reviewer evaluate?', 'Significant judgements, significant risks and responses, independence, consultations and whether the proposed report is appropriate.',
          [P('p1', 'Significant judgements', 5, 'judgement'), P('p2', 'Report appropriateness', 5, 'report')], 'c3'),
        V('v3', 'What are the engagement partner\'s responsibilities under SA 220?', 'Overall audit quality, ethics and independence, acceptance, team competence, direction, supervision, review and consultation.',
          [P('p1', 'Overall quality', 5, 'quality'), P('p2', 'Supervision and review', 5, 'supervision|review')], 'c2'),
        V('v4', 'What is the current status of SQM 1 and SQM 2?', 'ICAI issued them in October 2024 but deferred their mandatory date in March 2026, so SQC 1 still applies.',
          [P('p1', 'Deferred', 5, 'deferred'), P('p2', 'SQC 1 applies', 5, 'sqc 1')], 'c1'),
        V('v5', 'What is NFRA\'s role?', 'It recommends standards, monitors compliance, oversees audit quality of listed and large companies and investigates and penalises misconduct.',
          [P('p1', 'Standards and monitoring', 5, 'standard|monitor'), P('p2', 'Investigation', 5, 'investigat|penal')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Sharma & Associates', 'difficulty': 'moderate',
              'case': 'Sharma & Associates audits a listed textile company. The engagement partner signed the report on 20 May; the EQCR reviewer completed her review on 22 May. A team senior\'s spouse holds shares in the client. The firm\'s last peer review certificate expired in March.',
              'mcqs': [
                  M('k1a', 'Signing the report before EQCR completion is:', ['Not permitted — the report cannot be dated before EQCR', 'Acceptable', 'Required', 'Optional for listed companies'], 0,
                    'EQCR must be complete. In practice: re-date after review.', 'core', topic=T3),
                  M('k1b', 'The spouse\'s shareholding is a threat to:', ['Independence (self-interest)', 'Competence', 'Confidentiality', 'Monitoring'], 0,
                    'Financial interest of immediate family. In practice: remove the senior.', 'core', topic=T1),
                  M('k1c', 'Audit of a listed entity requires a firm to hold:', ['A valid peer review certificate', 'NFRA licence', 'SEBI registration', 'ISO certificate'], 0,
                    'ICAI requirement. In practice: renew in time.', 'core', topic=T4),
                  M('k1d', 'Overall responsibility for audit quality lies with:', ['The engagement partner', 'The EQCR reviewer', 'The client\'s audit committee', 'The senior'], 0,
                    'SA 220. In practice: EQCR does not reduce it.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch01', 1, 'Quality Control',
                ['Explain audit quality and the SQC 1 system of quality control.',
                 'Apply SA 220 responsibilities at engagement level.',
                 'Describe engagement quality control review and documentation.',
                 'Explain peer review, QRB and NFRA oversight.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': [],
                 'exam_tip': 'Case studies: identify the element breached, cite SQC 1 or SA 220, and state the corrective step.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['SQC 1 (firm) + SA 220 (engagement).',
                             'Six elements: leadership, ethics, acceptance, HR, performance, monitoring.',
                             'EQCR for listed entities before report date.',
                             'Assemble files in 60 days; retain 7 years.',
                             'Peer Review Board, QRB, NFRA.'],
                 'remember': ['SQM 1/2 deferred (March 2026): SQC 1 continues.'],
                 'traps': ['Dating the report before EQCR completion.']},
                [('SQC 1', 'Firm level'), ('SA 220', 'Engagement level'), ('EQCR', 'Listed + firm criteria'), ('File assembly', '60 days')],
                viva, cases)
