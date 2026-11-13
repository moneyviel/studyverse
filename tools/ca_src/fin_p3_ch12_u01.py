"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 12 Digital Auditing & Assurance.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch12-u01'
T1 = 'Digital audit and auditing digitally'
T2 = 'Understanding the IT environment and IT risks'
T3 = 'Cyber risk and remote audit'
T4 = 'Emerging technologies and next-generation audit'


def build():
    ck = Checks()
    pct = ck.add('round(37/2400*100,2)', 'Exceptions as a share of journal entries tested (%)')
    i1 = {'id': 'i1', 'title': 'Full-population journal testing', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Using a data analytics tool, the auditor tests all 2,400 manual journal entries of Kite Ltd. against criteria: posted on weekends, posted by senior management, round amounts, or just below approval limits. 37 entries meet one or more criteria. Compute the exception rate and outline follow-up.',
          'solution': [table(['Step', 'Working / Action', 'Result'], [
              ['Exception rate', '37 ÷ 2,400', inr(pct) + '%'],
              ['Follow-up', 'Inspect support and approvals for each flagged entry', '—'],
              ['Fraud angle', 'Responds to management override risk (SA 240)', '—'],
              ['Data integrity', 'Confirm completeness of extracted data before testing', '—']], title='Data analytics')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'IT risk and control', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Identify the IT risk and a control: (a) developers can change production code directly; (b) ex-employees\' user IDs remain active; (c) no backups are tested; (d) users can override system-calculated discounts without approval.',
          'solution': [table(['Issue', 'Risk', 'Control'], [
              ['(a)', 'Unauthorised program changes', 'Change management with segregation of development and production'],
              ['(b)', 'Unauthorised access', 'Timely access removal and periodic user reviews'],
              ['(c)', 'Data loss and continuity', 'Regular backup and restoration testing'],
              ['(d)', 'Inappropriate manual overrides', 'Approval workflow and override logs']], title='IT general and application controls')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'A digital audit uses technology across the audit — paperless workflows, data analytics, automated tools — to examine entire populations, increase speed and focus on risk. Auditing digitally refers to auditing an entity whose processes, records and controls are digital, requiring the auditor to understand and test IT systems.',
            'Advantages: wider coverage, real-time or continuous auditing, better anomaly detection, efficiency and documentation. Challenges: data quality and access, cyber security, skills, tool reliability, cost and evidence of data completeness.',
            'Professional skepticism and judgement remain central; tools support but do not replace the auditor.'],
          'Technology expands what auditors can see — judgement still decides.',
          'Testing 100% of transactions replaces small samples.'),
        C('c2', T2, [
            'Understanding the IT environment covers applications, databases, operating systems, networks, IT processes (access, change, operations) and outsourced services.',
            'Risks arising from IT: unauthorised access, unauthorised changes to data or programs, failure to update systems, inappropriate manual intervention, data loss, and reliance on inaccurate system reports. IT general controls (access, change management, operations) support application controls.',
            'The auditor identifies IT dependencies — automated controls, calculations, reports used in the audit, interfaces — and tests related controls or the data itself.'],
          'Know the systems before trusting their output.',
          'A system-generated ageing report needs testing before relying on it.'),
        C('c3', T3, [
            'Cyber risk is the risk of loss from failure or breach of information systems — malware, ransomware, phishing, data theft, denial of service — threatening confidentiality, integrity and availability.',
            'Cyber security frameworks (e.g. identify, protect, detect, respond, recover) guide controls: access management, encryption, patching, monitoring, incident response, backups and awareness training. The auditor considers effects of cyber incidents on statements and going concern.',
            'Remote audits use secure document sharing and video tools; auditors must ensure authenticity of documents, confidentiality, and sufficiency of evidence, sometimes using live observation by video.'],
          'Cyber incidents are audit risks, not just IT problems.',
          'A ransomware attack may require evaluating data integrity and disclosures.'),
        C('c4', T4, [
            'Emerging technologies: data analytics (e.g. ACL, IDEA), artificial intelligence and machine learning for anomaly detection and document reading, robotic process automation for repetitive testing, Internet of Things for real-time asset data, blockchain for tamper-resistant records, and drones for inventory observation.',
            'Control objectives in such environments: accuracy, completeness, authorisation, data integrity and security; auditors must understand how tools and models work and validate their outputs.',
            'Next-generation audit moves toward continuous auditing, full-population testing and predictive insights, requiring new skills and quality controls over tools.'],
          'New tools, same objectives: reliable evidence.',
          'Drones counting coal stockpiles support inventory observation.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Setting up an analytics-led audit', 'role': 'IT audit specialist',
             'situation': 'A retail client processes 10 million transactions annually on an ERP.',
             'steps': ['Map IT environment and dependencies.', 'Test IT general controls.', 'Extract full data and verify completeness.', 'Run analytics and follow up exceptions.'],
             'takeaway': 'Reliable data plus tested controls make analytics trustworthy.'}]

    mcqs = [
        Q('m1', 'A key advantage of digital audit is:', ['Testing entire populations', 'Eliminating judgement', 'Avoiding documentation', 'No need for skepticism'], 0,
          'Wider coverage. In practice: analytics tools.', 'c1', T1),
        Q('m2', 'IT general controls include:', ['Access, change management and operations controls', 'Sales discounts', 'Credit limits', 'Price lists'], 0,
          'Support application controls. In practice: test first.', 'c2', T2),
        Q('m3', 'Active user IDs of ex-employees indicate risk of:', ['Unauthorised access', 'Inventory loss only', 'Tax evasion', 'None'], 0,
          'Access control failure. In practice: user reviews.', 'c2', T2),
        Q('m4', 'The CIA triad in cyber security stands for:', ['Confidentiality, integrity, availability', 'Control, inspection, audit', 'Cost, impact, accuracy', 'Compliance, independence, assurance'], 0,
          'Security objectives. In practice: frameworks.', 'c3', T3),
        Q('m5', 'In a remote audit, a key concern is:', ['Authenticity of documents received', 'Travel costs', 'Office space', 'Printing'], 0,
          'Evidence reliability. In practice: secure portals.', 'c3', T3),
        Q('m6', 'RPA in audit is best used for:', ['Repetitive rule-based tasks', 'Judgement on estimates', 'Signing reports', 'Client acceptance'], 0,
          'Automation. In practice: reconciliations.', 'c4', T4),
        Q('m7', 'Before relying on a system report, the auditor should:', ['Test its accuracy and completeness', 'Accept it', 'Ignore it', 'Print it'], 0,
          'Information produced by entity. In practice: test ITGCs.', 'c2', T2),
        Q('m8', 'Continuous auditing is a feature of:', ['Next-generation audit', 'Manual audit', 'Compilation', 'Agreed procedures'], 0,
          'Real-time insights. In practice: data feeds.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Rate', 1.5, 'computation', 'exception', nums=[pct]), S('s2', 'Follow-up', 2, 'concept', 'support|approval'), S('s3', 'Data integrity', 1.5, 'concept', 'completeness')],
          ['Link to SA 240.'], ['Skipping data completeness checks.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Change and access', 3, 'concept', 'change|access'), S('s2', 'Backup and override', 3, 'concept', 'backup|override')],
          ['Risk and control pairs.'], ['Naming risks without controls.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Distinguish digital audit and auditing digitally.', 'Digital audit uses technology to perform the audit; auditing digitally means auditing an entity whose processes and records are digital.',
          [P('p1', 'Uses technology', 5, 'technology'), P('p2', 'Digital entity', 5, 'digital')], 'c1'),
        V('v2', 'Name risks arising from IT.', 'Unauthorised access, unauthorised program or data changes, inappropriate manual intervention and data loss.',
          [P('p1', 'Access and changes', 5, 'access|change'), P('p2', 'Data loss or intervention', 5, 'loss|intervention')], 'c2'),
        V('v3', 'What are the stages of a cyber security framework?', 'Identify, protect, detect, respond and recover.',
          [P('p1', 'Identify and protect', 5, 'identify|protect'), P('p2', 'Detect, respond, recover', 5, 'detect|respond|recover')], 'c3'),
        V('v4', 'Give examples of emerging audit technologies.', 'Data analytics, artificial intelligence, robotic process automation, blockchain, IoT and drones.',
          [P('p1', 'Analytics and AI', 5, 'analytics|artificial'), P('p2', 'RPA or blockchain', 5, 'robotic|blockchain')], 'c4'),
        V('v5', 'Why must data completeness be checked before analytics?', 'Because conclusions from analytics are only reliable if the extracted data is complete and accurate.',
          [P('p1', 'Complete and accurate', 5, 'complete'), P('p2', 'Reliable conclusions', 5, 'reliab')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'CloudKart Ltd.', 'difficulty': 'moderate',
              'case': 'CloudKart, an e-commerce company, suffered a ransomware attack in February; systems were restored from backups within a week. The audit is performed remotely. Developers have admin access to production. The auditor plans to use AI to read 50,000 vendor invoices.',
              'mcqs': [
                  M('k1a', 'The ransomware attack requires the auditor to consider:', ['Data integrity, completeness and disclosures', 'Nothing as systems restored', 'Only insurance', 'Only fees'], 0,
                    'Cyber risk affects evidence. In practice: test restored data.', 'core', topic=T3),
                  M('k1b', 'Developers\' admin access to production is a weakness in:', ['Change management and access controls', 'Sales controls', 'Payroll', 'Treasury'], 0,
                    'ITGC failure. In practice: substantive testing increases.', 'core', topic=T2),
                  M('k1c', 'In the remote audit, documents should be:', ['Obtained via secure channels and checked for authenticity', 'Accepted as emailed', 'Ignored', 'Printed only'], 0,
                    'Evidence reliability. In practice: live video verification.', 'core', topic=T3),
                  M('k1d', 'Before relying on the AI tool, the auditor should:', ['Understand and validate its outputs', 'Trust it fully', 'Let it sign the report', 'Avoid documenting it'], 0,
                    'Tool reliability. In practice: test a sample manually.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch12', 1, 'Digital Auditing & Assurance',
                ['Explain digital audit and auditing digitally.',
                 'Understand IT environments, risks and dependencies.',
                 'Assess cyber risks and conduct remote audits.',
                 'Apply emerging technologies in audit.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 15}, 'prereq': ['fin-p3-ch11-u01'],
                 'exam_tip': 'Pair each IT weakness with an ITGC or application control.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Digital audit vs auditing digitally.',
                             'ITGCs: access, change, operations.',
                             'IT dependencies and system reports.',
                             'Cyber risk: CIA triad; frameworks.',
                             'Analytics, AI, RPA, blockchain, IoT, drones.'],
                 'remember': ['Tools support, not replace, judgement.'],
                 'traps': ['Relying on unverified system reports.']},
                [('ITGC', 'Access, change, ops'), ('CIA', 'Confidentiality, integrity, availability'), ('RPA', 'Repetitive tasks'), ('Remote audit', 'Authenticity')],
                viva, cases)
