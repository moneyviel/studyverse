"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 2 General Auditing Principles and Auditors Responsibilities.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch02-u01'
T1 = 'SA 240: fraud in an audit of financial statements'
T2 = 'SA 250: laws and regulations'
T3 = 'SA 260: communication with those charged with governance'
T4 = 'SA 299: joint audits'
T5 = 'SA 402: entities using service organisations'


def build():
    ck = Checks()
    limit = ck.add('1', 'Threshold for reporting fraud to the Central Government (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Fraud found during the audit', 'difficulty': 'hard', 'minutes': 9,
          'q': 'During the audit of Zenith Ltd., the auditor finds that the purchase manager has diverted ₹1.4 crore through fictitious vendors, and that the CFO recorded fictitious sales near year end to meet targets. What should the auditor do under SA 240 and section 143(12) of the Companies Act?',
          'solution': [table(['Step', 'Action'], [
              ['Classify', 'Misappropriation of assets (vendors) and fraudulent financial reporting (sales)'],
              ['Evaluate', 'Reassess risks, management representations and reliability of evidence; management override involved'],
              ['Communicate', 'Inform appropriate level of management and those charged with governance promptly'],
              ['Report to Government', 'Fraud of ₹' + inr(limit) + ' crore or more by officers/employees → report to the Central Government (within prescribed timelines, after seeking board/audit committee reply)'],
              ['Consider', 'Effect on opinion; whether to withdraw if law permits']], title='SA 240 response')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Joint audit responsibilities', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Auditors A and B are joint auditors of Delta Ltd. A audits sales and receivables; B audits purchases and inventory. B discovers that inventory valuation is overstated. Who is responsible for what, and how is the report issued if A disagrees with B\'s conclusion?',
          'solution': [table(['Point', 'Position under SA 299'], [
              ['Allocated areas', 'Each auditor responsible for the work allocated to them'],
              ['Joint responsibility', 'Both jointly responsible for areas not divided, and for the audit report and compliance matters'],
              ['Communication', 'B informs A of matters affecting A\'s work and the overall opinion'],
              ['Disagreement', 'Each auditor may issue a separate report expressing their own opinion']], title='Joint audit')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Fraud is an intentional act involving deception to gain an unjust or illegal advantage. Two types matter to auditors: fraudulent financial reporting (manipulating records, misapplying policies, omitting transactions) and misappropriation of assets (theft, embezzlement, fictitious payments). Fraud risk factors: incentive or pressure, opportunity, and rationalisation (the fraud triangle).',
            'Prevention and detection is primarily the responsibility of management and those charged with governance. The auditor obtains reasonable assurance that statements are free from material misstatement due to fraud or error, maintaining professional skepticism, holding team discussions, and always treating revenue recognition as a presumed fraud risk (rebuttable) and management override as a risk in every audit — responding by testing journal entries, reviewing estimates for bias and evaluating unusual transactions.',
            'If fraud is found: evaluate implications, communicate to management and TCWG, consider withdrawal, and report as required. Under section 143(12), fraud of ₹1 crore or more by officers or employees is reported to the Central Government; smaller frauds are reported to the audit committee or board and disclosed in the board report.'],
          'Skepticism, the fraud triangle and management override are the core of SA 240.',
          'Fictitious year-end sales to hit targets are fraudulent financial reporting.'),
        C('c2', T2, [
            'Management ensures compliance with laws and regulations. The auditor distinguishes laws with a direct effect on amounts and disclosures (tax, company law, pension) — obtain sufficient evidence of compliance — and other laws fundamental to operations (licences, environmental, regulatory) — perform specified procedures such as enquiries and inspecting correspondence.',
            'If non-compliance is identified or suspected, the auditor understands its nature, discusses with management and TCWG, considers legal advice, evaluates the effect on the opinion and on management representations, and considers reporting to regulators where required (overriding confidentiality).',
            'Documentation covers identified non-compliance and discussions held.'],
          'Direct-effect laws need evidence; other laws need targeted procedures.',
          'Operating without a pollution licence could threaten going concern.'),
        C('c3', T3, [
            'SA 260 requires two-way communication with those charged with governance (board, audit committee): the auditor\'s responsibilities, planned scope and timing, significant findings (qualitative aspects of accounting practices, significant difficulties, significant matters discussed with management, written representations sought, circumstances affecting the report form), and for listed entities, independence.',
            'Communication should be timely and, for significant findings that the auditor judges inadequate orally, in writing.',
            'If two-way communication is inadequate, the auditor evaluates the effect on risk assessment and evidence and may modify the opinion or withdraw.'],
          'Talk to the board early and openly — and in writing when it matters.',
          'An auditor communicates a disagreement on revenue policy to the audit committee.'),
        C('c4', T4, [
            'Under SA 299 (Revised), joint auditors plan together, agree the overall strategy and materiality, and divide work in writing. Each is responsible for the work allocated to them; work not divided is jointly carried out and is a joint responsibility.',
            'Joint responsibilities include: deciding the nature and extent of procedures, reviewing statements for compliance with law, communication with TCWG, ensuring the report complies with law, and issues raised by any joint auditor that affect the opinion.',
            'Joint auditors normally issue a common report; if they disagree, each may issue a separate report. They are not responsible for each other\'s errors in allocated areas, but must report matters coming to notice.'],
          'Divide the work clearly, but sign the report together.',
          'If two joint auditors disagree on a qualification, separate reports are issued.'),
        C('c5', T5, [
            'When an entity uses a service organisation (payroll processor, data centre, custodian), the user auditor must understand the services and their effect on internal control relevant to the audit.',
            'Evidence may come from the user entity\'s controls, visiting the service organisation, or a service auditor\'s report: Type 1 (description and design of controls at a point in time) or Type 2 (design and operating effectiveness over a period). Only Type 2 supports reliance on operating effectiveness.',
            'The user auditor evaluates the service auditor\'s competence and independence and the report\'s adequacy; the user auditor does not refer to the service auditor\'s report in an unmodified opinion.'],
          'Outsourced processes still need audit evidence.',
          'A Type 2 report on a payroll processor\'s controls can reduce substantive testing.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Responding to a whistle-blower tip', 'role': 'Audit manager',
             'situation': 'An anonymous email alleges inflated sales at a client branch.',
             'steps': ['Reassess fraud risk and plan targeted procedures.', 'Test journal entries and cut-off.', 'Communicate findings to TCWG.', 'Assess section 143(12) reporting.'],
             'takeaway': 'Treat allegations seriously and follow the reporting chain.'}]

    mcqs = [
        Q('m1', 'The primary responsibility to prevent and detect fraud rests with:', ['Management and those charged with governance', 'The auditor', 'The regulator', 'Shareholders'], 0,
          'Auditor gives reasonable assurance only. In practice: SA 240.', 'c1', T1),
        Q('m2', 'SA 240 presumes a fraud risk in:', ['Revenue recognition', 'Fixed assets', 'Share capital', 'Cash only'], 0,
          'Rebuttable presumption. In practice: document if rebutted.', 'c1', T1),
        Q('m3', 'Fraud by employees of one crore rupees or more must be reported by the auditor to:', ['The Central Government', 'Only the board', 'SEBI', 'Police directly'], 0,
          'Section 143(12). In practice: smaller frauds to audit committee.', 'c1', T1),
        Q('m4', 'For laws with a direct effect on financial statements, the auditor must:', ['Obtain sufficient appropriate evidence of compliance', 'Ignore them', 'Only enquire', 'Rely on management'], 0,
          'E.g. tax laws. In practice: test computations.', 'c2', T2),
        Q('m5', 'For listed entities, SA 260 requires communication on:', ['Auditor independence', 'Fee negotiations', 'Staff salaries', 'Marketing plans'], 0,
          'Independence statement. In practice: annually.', 'c3', T3),
        Q('m6', 'Under SA 299, work not divided among joint auditors is:', ['The joint responsibility of all', 'Nobody\'s responsibility', 'The senior auditor\'s', 'Management\'s'], 0,
          'Joint responsibility. In practice: document allocation.', 'c4', T4),
        Q('m7', 'A Type 2 report on a service organisation covers:', ['Design and operating effectiveness of controls over a period', 'Only design at a point in time', 'Financial statements', 'Tax compliance'], 0,
          'Supports reliance. In practice: check period covered.', 'c5', T5),
        Q('m8', 'If joint auditors disagree on the opinion:', ['Each may issue a separate report', 'The larger firm decides', 'No report is issued', 'Management decides'], 0,
          'SA 299. In practice: rare.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Types', 1.5, 'concept', 'misappropriation|fraudulent'), S('s2', 'Communication', 1.5, 'concept', 'governance|management'), S('s3', 'Government reporting', 2, 'computation', 'central government', nums=[limit]), S('s4', 'Opinion', 1, 'concept', 'opinion|withdraw')],
          ['Cite section 143(12).'], ['Reporting only to the board.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Allocated work', 2, 'concept', 'allocated'), S('s2', 'Joint responsibility', 2, 'concept', 'jointly'), S('s3', 'Separate report', 1, 'concept', 'separate')],
          ['Cite SA 299.'], ['Making A liable for B\'s area.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What are the two types of fraud relevant to auditors?', 'Fraudulent financial reporting and misappropriation of assets.',
          [P('p1', 'Fraudulent reporting', 5, 'fraudulent financial reporting'), P('p2', 'Misappropriation', 5, 'misappropriation')], 'c1'),
        V('v2', 'What is the fraud triangle?', 'Incentive or pressure, opportunity, and rationalisation, which together make fraud more likely.',
          [P('p1', 'Pressure and opportunity', 5, 'pressure|opportunity'), P('p2', 'Rationalisation', 5, 'rationali')], 'c1'),
        V('v3', 'Which significant findings are communicated under SA 260?', 'Qualitative aspects of accounting practices, significant difficulties, significant matters discussed with management, written representations sought and matters affecting the report form.',
          [P('p1', 'Accounting practices', 5, 'accounting practice'), P('p2', 'Difficulties and representations', 5, 'difficult|representation')], 'c3'),
        V('v4', 'What are the joint responsibilities of joint auditors?', 'Deciding nature and extent of procedures, reviewing statements for legal compliance, communicating with governance, and the audit report.',
          [P('p1', 'Procedures and compliance', 5, 'procedure|complian'), P('p2', 'Report', 5, 'report')], 'c4'),
        V('v5', 'Distinguish Type 1 and Type 2 service organisation reports.', 'Type 1 covers description and design of controls at a date; Type 2 also covers operating effectiveness over a period.',
          [P('p1', 'Design at a date', 5, 'design'), P('p2', 'Operating effectiveness', 5, 'operating effectiveness')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Orbit Chemicals Ltd.', 'difficulty': 'moderate',
              'case': 'Orbit Chemicals outsources payroll to PayServe Ltd. Its auditor finds that the factory was operating without a renewed pollution licence, and that an accountant embezzled ₹40 lakh. Revenue recognition was treated as a fraud risk, but the auditor rebutted it for scrap sales.',
              'mcqs': [
                  M('k1a', 'The ₹40 lakh embezzlement is reported by the auditor to:', ['The audit committee or board (below ₹1 crore)', 'The Central Government', 'SEBI', 'No one'], 0,
                    'Below threshold. In practice: board report discloses.', 'core', topic=T1),
                  M('k1b', 'The expired pollution licence falls under:', ['Other laws fundamental to operations (SA 250)', 'Direct-effect laws', 'SA 402', 'SA 299'], 0,
                    'Specified procedures; possible going concern impact. In practice: legal advice.', 'core', topic=T2),
                  M('k1c', 'To rely on PayServe\'s controls\' operating effectiveness, the auditor needs:', ['A Type 2 report', 'A Type 1 report', 'Management representation', 'Nothing'], 0,
                    'Type 2 covers effectiveness. In practice: check period.', 'core', topic=T5),
                  M('k1d', 'Rebutting the revenue fraud presumption requires:', ['Documenting the reasons', 'No action', 'Board approval', 'Regulator approval'], 0,
                    'SA 240 documentation. In practice: limited cases.', 'moderate', topic=T1),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch02', 1, 'General Auditing Principles and Auditors Responsibilities',
                ['Apply SA 240 on fraud, including section 143(12) reporting.',
                 'Apply SA 250 on laws and regulations.',
                 'Communicate with those charged with governance under SA 260.',
                 'Apply SA 299 to joint audits.',
                 'Apply SA 402 to entities using service organisations.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p3-ch01-u01'],
                 'exam_tip': 'For fraud cases, follow: classify → evaluate → communicate → report under 143(12) → opinion.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Fraud: reporting vs misappropriation; triangle.',
                             'Revenue fraud presumption; management override always.',
                             '143(12): ≥ ₹1 crore to Central Government.',
                             'SA 250: direct-effect laws vs other laws.',
                             'SA 260 TCWG; SA 299 joint audit; SA 402 Type 1/2.'],
                 'remember': ['Primary fraud responsibility: management and TCWG.'],
                 'traps': ['Assuming auditors must detect all fraud.']},
                [('Fraud ≥ ₹1 crore', 'Report to Central Govt'), ('Revenue', 'Presumed fraud risk'), ('Joint audit', 'Allocated + joint'), ('Type 2', 'Operating effectiveness')],
                viva, cases)
