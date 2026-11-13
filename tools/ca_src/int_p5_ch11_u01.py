"""CA Intermediate · Paper 5 Auditing and Ethics · Chapter 11 Ethics and Terms of Audit Engagements.
Scope follows the ICAI study material; explanations, names and figures are original."""
from ikit import *

UID = 'int-p5-ch11-u01'
T1 = 'Ethics and the fundamental principles'
T2 = 'Independence: threats and safeguards; professional skepticism'
T3 = 'Agreeing the terms of audit engagements (SA 210)'
T4 = 'Quality control (SQC 1)'


def build():
    i1 = {'id': 'i1', 'title': 'Spot the threat', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Identify the threat to independence and a safeguard: (a) the audit partner\'s spouse holds shares in the client; (b) the firm prepared the client\'s accounts it now audits; (c) the firm defends the client\'s position before a tax tribunal; (d) the same partner has led the audit for many years and is close to the CFO; (e) the client threatens to change auditors unless a provision is dropped.',
          'solution': [table(['Case', 'Threat', 'Possible safeguard'], [
              ['(a)', 'Self-interest', 'Dispose of the interest or remove the partner from the engagement'],
              ['(b)', 'Self-review', 'Separate teams with independent review, or decline the non-audit service where prohibited'],
              ['(c)', 'Advocacy', 'Avoid such representation for audit clients where it compromises objectivity; use different personnel'],
              ['(d)', 'Familiarity', 'Rotate the partner; engagement quality review'],
              ['(e)', 'Intimidation', 'Discuss with those charged with governance; consult; withdraw if necessary']], title='Threats and safeguards')],
          'checks': []}

    i2 = {'id': 'i2', 'title': 'Before saying yes', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A prospective client wants an audit but (a) refuses to acknowledge responsibility for internal control and (b) later, after acceptance, asks to change the engagement to a review because a bank loan is no longer needed. How should the auditor respond under SA 210?',
          'solution': [table(['Situation', 'Response'], [
              ['(a) Preconditions absent', 'Do not accept the engagement unless required by law; management must acknowledge responsibility for preparing the statements, for internal control and for giving access'],
              ['(b) Request to change to a review', 'Consider whether the reason is reasonable: a genuine change in need may justify it; but a change to avoid an unfavourable finding or scope limitation does not. If unjustified and management will not let the audit continue, withdraw where possible and consider communication duties']], title='SA 210')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Ethics is a state of mind guiding conduct; the profession\'s value depends on public trust. The ICAI Code of Ethics follows a principles-based (conceptual framework) approach rather than only fixed rules.',
            'Fundamental principles: integrity (straightforward and honest); objectivity (no bias, conflict of interest or undue influence); professional competence and due care (current knowledge and diligent work); confidentiality (no disclosure or use of information without authority or legal duty); and professional behaviour (comply with laws, avoid discrediting the profession).',
            'Under the conceptual framework, the professional identifies threats to these principles, evaluates them, and applies safeguards to eliminate them or reduce them to an acceptable level — or declines or ends the engagement.'],
          'The Code supplies principles; the professional must apply judgement to each situation.',
          'Using a client\'s confidential merger news to buy shares breaches confidentiality and integrity.'),
        C('c2', T2, [
            'Independence of mind (objective state of mind) and independence in appearance (avoiding facts that a reasonable person would see as compromising) are both required.',
            'Threats: self-interest (financial interest, fee dependence, loans); self-review (auditing one\'s own work); advocacy (promoting the client\'s position); familiarity (long or close relationships); intimidation (pressure or threats).',
            'Safeguards: those created by the profession, law or regulation (education, standards, monitoring, rotation requirements) and those in the work environment (firm policies, independent reviews, separate teams, rotation, communication with TCWG).',
            'Professional skepticism is an attitude of questioning, alert to conditions that may indicate misstatement and to evidence that contradicts other evidence, and a critical assessment of evidence — neither assuming dishonesty nor unquestioned honesty.'],
          'Independence is what gives an audit opinion its value; skepticism is how it is exercised.',
          'Accepting a CFO\'s explanation for unusual year-end sales without corroboration shows a lack of skepticism.'),
        C('c3', T3, [
            'SA 210: the auditor accepts an engagement only if preconditions exist — an acceptable financial reporting framework, and management\'s acknowledgement of responsibility for preparing the statements, for internal control, and for giving access to information and persons.',
            'Terms are recorded in an engagement letter or other written agreement covering objective and scope, auditor\'s and management\'s responsibilities, the framework, and expected form of reports (with a note that content may differ). It may also cover planning, fees, use of experts and arrangements with predecessor auditors.',
            'A limitation of scope imposed by management before acceptance, likely to result in a disclaimer, leads the auditor not to accept (unless required by law).',
            'Change in terms: the auditor agrees only with reasonable justification; a request to change to a lower assurance engagement is not reasonable if it relates to incorrect, incomplete or unsatisfactory information. In recurring audits, the auditor considers whether terms need revising (e.g. change in management, ownership, legal requirements).'],
          'Clear terms prevent misunderstandings about what an audit is and is not.',
          'A new law requiring additional reporting is a reason to revise the engagement letter.'),
        C('c4', T4, [
            'Audit quality depends on the firm\'s system of quality control. SQC 1 requires firms to establish policies covering: leadership responsibilities for quality; relevant ethical requirements (including independence confirmations); acceptance and continuance of client relationships; human resources; engagement performance (direction, supervision, review, consultation, engagement quality control review); and monitoring.',
            'Before accepting, the firm considers integrity of the client, competence and capabilities including time and resources, and compliance with ethical requirements.',
            'Documentation of the system and monitoring of its effectiveness, including inspection of completed engagements, are required. (ICAI\'s newer Standard on Quality Management follows the same objectives with a risk-based approach.)'],
          'Quality is designed into the firm, not inspected into a single file at the end.',
          'A firm that lacks staff with banking knowledge should decline a complex bank audit.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Client acceptance file', 'role': 'Audit senior',
             'situation': 'The firm is invited to audit a fast-growing listed company.',
             'steps': ['Check integrity of owners and management.', 'Confirm independence of every team member.', 'Assess competence, time and resources.', 'Confirm preconditions and issue an engagement letter.'],
             'takeaway': 'Acceptance procedures protect the firm before any audit work starts.'}]

    mcqs = [
        Q('m1', 'Which is NOT a fundamental principle in the Code of Ethics?', ['Profitability', 'Integrity', 'Objectivity', 'Confidentiality'], 0,
          'The five principles cover honesty (integrity), freedom from bias (objectivity), skill with diligence (competence and due care), secrecy (confidentiality) and good conduct (professional behaviour). In practice: profitability is not an ethical principle.', 'c1', T1),
        Q('m2', 'A threat arising when an auditor evaluates his own earlier work is:', ['Self-review threat', 'Self-interest threat', 'Advocacy threat', 'Familiarity threat'], 0,
          'Self-review threats arise when the auditor relies on judgements he made earlier. In practice: separate teams help.', 'c2', T2),
        Q('m3', 'Long association of a senior auditor with a client creates a:', ['Familiarity threat', 'Intimidation threat', 'Advocacy threat', 'Self-review threat'], 0,
          'Closeness reduces objectivity over time. In practice: rotation is a key safeguard.', 'c2', T2),
        Q('m4', 'Professional skepticism means:', ['A questioning mind and critical assessment of evidence', 'Assuming management is dishonest', 'Accepting management explanations', 'Auditing every transaction'], 0,
          'Skepticism neither assumes dishonesty nor unquestioned honesty. In practice: corroborate unusual explanations.', 'c2', T2),
        Q('m5', 'A precondition for an audit under SA 210 is:', ['Management acknowledges responsibility for internal control', 'Audit fee paid in advance', 'No prior auditor', 'Profit for the year'], 0,
          'Management must accept responsibility for the statements, internal control and access. In practice: obtain it in writing.', 'c3', T3),
        Q('m6', 'A request to change an audit to a review because adverse findings are expected is:', ['Not a reasonable justification', 'Always acceptable', 'Required by SA 210', 'A matter for the client only'], 0,
          'Changes to avoid unfavourable outcomes are not reasonable. In practice: withdraw if necessary.', 'c3', T3),
        Q('m7', 'Engagement quality control review is part of which SQC 1 element?', ['Engagement performance', 'Leadership', 'Human resources', 'Monitoring'], 0,
          'Engagement performance covers direction, supervision, review, consultation and EQCR. In practice: required for listed entity audits.', 'c4', T4),
        Q('m8', 'Holding shares in an audit client creates a:', ['Self-interest threat', 'Advocacy threat', 'Familiarity threat', 'Self-review threat'], 0,
          'Financial interest may bias judgement. In practice: dispose of the interest before accepting.', 'c2', T2),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Self-interest', 1, 'concept', 'self-interest'), S('s2', 'Self-review', 1, 'concept', 'self-review'), S('s3', 'Advocacy', 1, 'concept', 'advocacy'),
           S('s4', 'Familiarity', 1, 'concept', 'familiarity'), S('s5', 'Intimidation', 1, 'concept', 'intimidation')],
          ['Name the threat, then the safeguard.'], ['Listing safeguards without threats.'], ['Table.'], pad='table'),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Preconditions', 2, 'concept', 'precondition|acknowledge'), S('s2', 'Change of terms', 2, 'concept', 'reasonable|justif')],
          ['Quote SA 210.'], ['Accepting any change request.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Name the five fundamental principles.', 'Integrity and objectivity; professional competence with due care; confidentiality; and professional behaviour.',
          [P('p1', 'Integrity and objectivity', 5, 'integrity|objectivity'), P('p2', 'Others', 5, 'confidential|competence|behaviour')], 'c1'),
        V('v2', 'What is independence in appearance?', 'Avoiding facts and circumstances so significant that a reasonable and informed third party would conclude the auditor\'s objectivity has been compromised.',
          [P('p1', 'Third party view', 5, 'third party|reasonable'), P('p2', 'Objectivity', 5, 'objectiv')], 'c2'),
        V('v3', 'Give two safeguards against threats.', 'Rotation of senior personnel and an independent review by a partner not involved in the engagement, besides discussing with those charged with governance.',
          [P('p1', 'Rotation', 5, 'rotat'), P('p2', 'Independent review', 5, 'review|governance')], 'c2'),
        V('v4', 'What does an engagement letter contain?', 'Objective and scope, responsibilities of auditor and management, the reporting framework, and the expected form of the auditor\'s reports.',
          [P('p1', 'Scope and responsibilities', 5, 'scope|responsibilit'), P('p2', 'Framework and report', 5, 'framework|report')], 'c3'),
        V('v5', 'Name the elements of SQC 1.', 'Leadership, ethical requirements, acceptance and continuance, human resources, engagement performance and monitoring.',
          [P('p1', 'Leadership and ethics', 5, 'leadership|ethic'), P('p2', 'Others', 5, 'acceptance|human|monitoring|performance')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'CA Meera & Associates', 'difficulty': 'moderate',
              'case': 'CA Meera & Associates audits Indus Foods Ltd. Facts: Meera\'s brother is the CFO of Indus; the firm also maintains Indus\'s books; fees from Indus are 40% of the firm\'s total fees; and the MD hints that the audit will be moved if the inventory provision is not reduced.',
              'mcqs': [
                  M('k1a', 'The brother being CFO creates a:', ['Familiarity threat', 'Advocacy threat', 'Self-review threat', 'No threat'], 0,
                    'A close family member in a key position at the client creates familiarity (and possibly self-interest) threats. In practice: such a relationship may make the threat unacceptable.', 'moderate', topic=T2),
                  M('k1b', 'Maintaining the books creates a:', ['Self-review threat', 'Intimidation threat', 'Advocacy threat', 'No threat'], 0,
                    'Auditing records the firm itself prepared is self-review. In practice: such services are restricted for audit clients.', 'core', topic=T2),
                  M('k1c', 'Fee dependence of 40% creates a:', ['Self-interest threat', 'Familiarity threat', 'Advocacy threat', 'Self-review threat'], 0,
                    'Heavy reliance on one client\'s fees may influence judgement. In practice: consider pre- or post-issuance review.', 'core', topic=T2),
                  M('k1d', 'The MD\'s hint is a(n):', ['Intimidation threat', 'Familiarity threat', 'Self-review threat', 'Ordinary negotiation'], 0,
                    'Pressure to change a judgement under threat of losing the audit is intimidation. In practice: escalate to the audit committee.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p5', 'int-p5-ch11', 1, 'Ethics and Terms of Audit Engagements',
                ['Explain the fundamental ethical principles and the conceptual framework.',
                 'Identify threats to independence and suitable safeguards; apply professional skepticism.',
                 'Apply SA 210 to preconditions, engagement letters and changes in terms.',
                 'Explain the elements of quality control under SQC 1.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 25}, 'prereq': ['int-p5-ch10-u01'],
                 'exam_tip': 'For each fact pattern, name the principle or threat first, then the safeguard or action.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Five principles: integrity; objectivity; competence with due care; confidentiality; professional behaviour.',
                             'Threats: self-interest, self-review, advocacy, familiarity, intimidation.',
                             'Skepticism: questioning mind, critical assessment.',
                             'SA 210: preconditions, engagement letter, changes only with reasonable justification.',
                             'SQC 1: six elements of a quality control system.'],
                 'remember': ['Independence of mind and in appearance are both needed.'],
                 'traps': ['Change to a review to avoid adverse findings is not reasonable.']},
                [('Self-review', 'Auditing own work'), ('Familiarity', 'Long association'), ('Intimidation', 'Pressure'), ('SA 210', 'Terms of engagement')],
                viva, cases)
