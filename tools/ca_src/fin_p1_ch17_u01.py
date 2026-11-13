"""CA Final · Paper 1 Financial Reporting · Chapter 17 Accounting and Technology.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch17-u01'
T1 = 'Automation, cloud and ERP in accounting'
T2 = 'Cyber security in accounting'
T3 = 'Blockchain and artificial intelligence'
T4 = 'Ind AS reporting controls (ICOFR) in an ERP'


def build():
    ck = Checks()
    hrs = ck.add('12000*(5-1)/60', 'Hours saved per year by automating invoice entry')
    cost = ck.add('12000*(5-1)/60*600/100000', 'Annual staff cost saved at ₹600 per hour (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Business case for automation', 'difficulty': 'core', 'minutes': 6,
          'q': 'Fern Ltd. processes 12,000 supplier invoices a year. Manual entry takes 5 minutes each; an OCR-and-RPA tool cuts this to 1 minute for review. Staff cost is ₹600 per hour. Compute hours and cost saved, and list two controls the tool still needs.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Hours saved', '12,000 × 4 ÷ 60', inr(hrs) + ' hours'],
              ['Cost saved', '800 × ₹600', '₹' + inr(cost) + ' lakh'],
              ['Controls still needed', 'Exception review of unmatched invoices; access control and change logs for the bot', '—']], title='Automation benefits and controls')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Control gaps in an ERP close', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'In Fern Ltd.\'s ERP: (a) the same user can create vendors and approve payments; (b) Ind AS 116 lease calculations are done in spreadsheets outside the ERP with no review; (c) month-end journal entries above ₹1 crore need no approval; (d) generic "admin" log-ins are shared. Identify the risk and a control for each.',
          'solution': [table(['Gap', 'Risk', 'Control'], [
              ['(a)', 'Fictitious vendor fraud', 'Segregation of duties enforced by ERP roles'],
              ['(b)', 'Calculation errors in lease liabilities', 'Reviewed and locked models, or a lease module with reconciliations'],
              ['(c)', 'Unauthorised or erroneous adjustments', 'Workflow approval thresholds for manual journals'],
              ['(d)', 'No accountability for changes', 'Unique user IDs, periodic access reviews, audit logs']], title='ICOFR in ERP')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Accounting has moved from manual books to computerised systems and now to automation. Robotic process automation (RPA) and optical character recognition handle rule-based, repetitive tasks such as invoice capture, bank reconciliations and journal postings.',
            'Cloud computing delivers software, platforms and infrastructure over the internet (SaaS, PaaS, IaaS), offering scalability, remote access and lower upfront costs, while raising data security, vendor dependence and data residency questions.',
            'Enterprise resource planning (ERP) systems integrate finance, procurement, sales, inventory and HR on one database, enabling real-time reporting and consistent master data; success needs process redesign, data migration and user training.'],
          'Automate the routine, integrate the data, and keep humans for judgement.',
          'A bot can match 95% of bank lines; staff review the rest.'),
        C('c2', T2, [
            'Accounting data is a target for cyber attacks. Common threats: phishing, ransomware, malware, insider threats, business email compromise (fake payment instructions) and weak passwords.',
            'Proactive measures: strong access controls and multi-factor authentication, encryption, regular patching, backups tested for restoration, network monitoring, vendor risk assessments, employee awareness training and an incident response plan.',
            'For finance teams, verification of bank detail changes through independent call-backs and dual approvals for payments are critical defences.'],
          'Most breaches start with people, so train them and verify payment changes.',
          'An email from a "supplier" changing bank details should be confirmed by phone.'),
        C('c3', T3, [
            'Blockchain is a shared, append-only ledger secured by cryptography. Benefits for reporting include transparency, data integrity, easier reconciliation between parties, a complete audit trail and near real-time information; challenges include scalability, regulation, integration and accounting for crypto assets.',
            'Artificial intelligence and machine learning help with data extraction, anomaly and fraud detection, forecasting, expense classification, and tax compliance.',
            'Challenges of AI: data quality, bias, explainability of outputs, privacy, cost and the need for human oversight — professional judgement remains with the accountant.'],
          'New tools improve speed and evidence, but judgement and accountability stay human.',
          'An ML model flags unusual journal entries for review.'),
        C('c4', T4, [
            'Internal control over financial reporting (ICOFR) in an ERP environment addresses risks such as: no documented close process; unapproved changes to the process; unclear roles; staff lacking Ind AS knowledge; unapproved choice of accounting alternatives; unmonitored user profiles; and missing data for non-routine transactions.',
            'Controls: documented close calendars and checklists; change management in the ERP; role-based access with segregation of duties; training records; approval workflows for policy choices and manual journals; periodic user access reviews; and audit trails (mandatory under Indian rules for accounting software).',
            'Ind AS calculations (leases, ECL, fair values, deferred tax) are often done outside the ERP; spreadsheet controls — version control, review, reconciliation to the ledger — are essential.'],
          'Configure controls into the system and check what lives outside it.',
          'Every company using accounting software must keep an audit trail that cannot be disabled.'),
    ]

    jobs = [{'id': 'j1', 'title': 'ERP implementation finance lead', 'role': 'Finance transformation manager',
             'situation': 'The company is moving from legacy software to a cloud ERP.',
             'steps': ['Map Ind AS processes and data needs.', 'Design role-based access and segregation of duties.', 'Set up audit trail, approval workflows and close checklist.', 'Test controls and train users before go-live.'],
             'takeaway': 'Technology helps only when controls are designed in from day one.'}]

    mcqs = [
        Q('m1', 'RPA is best suited to:', ['Rule-based repetitive tasks', 'Complex judgements', 'Strategic planning', 'Negotiations'], 0,
          'Bots follow rules. In practice: invoice capture and reconciliations.', 'c1', T1),
        Q('m2', 'SaaS means:', ['Software delivered over the internet as a service', 'Hardware leasing', 'On-premise licences only', 'Security as a service only'], 0,
          'Cloud delivery model. In practice: subscription pricing.', 'c1', T1),
        Q('m3', 'A key defence against business email compromise is:', ['Independent call-back to verify bank detail changes', 'Faster payments', 'Shared passwords', 'Disabling logs'], 0,
          'Verification breaks the fraud. In practice: dual approval.', 'c2', T2),
        Q('m4', 'Blockchain improves financial reporting mainly through:', ['An immutable shared ledger and audit trail', 'Higher costs', 'Manual reconciliations', 'Paper records'], 0,
          'Data integrity and transparency. In practice: inter-company ledgers.', 'c3', T3),
        Q('m5', 'A challenge of AI in accounting is:', ['Explainability of outputs and data quality', 'Faster processing', 'Fewer errors', 'Lower costs'], 0,
          'Human oversight remains needed. In practice: validate models.', 'c3', T3),
        Q('m6', 'The same ERP user creating vendors and approving payments is a failure of:', ['Segregation of duties', 'Encryption', 'Backup', 'Training'], 0,
          'Fraud risk. In practice: enforce via roles.', 'c4', T4),
        Q('m7', 'Lease calculations held in unreviewed spreadsheets create a risk of:', ['Misstated lease liabilities', 'Cyber attack only', 'Tax evasion', 'None'], 0,
          'End-user computing risk. In practice: review and reconcile.', 'c4', T4),
        Q('m8', 'Multi-factor authentication helps mitigate:', ['Unauthorised access from stolen passwords', 'Inventory loss', 'Currency risk', 'Credit risk'], 0,
          'Adds a second check. In practice: for ERP and banking portals.', 'c2', T2),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Hours', 1.5, 'computation', 'hours', nums=[hrs]), S('s2', 'Cost', 1.5, 'computation', 'cost', nums=[cost]), S('s3', 'Controls', 1, 'concept', 'exception|access')],
          ['Mention controls.'], ['Assuming bots need no oversight.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'SoD and access', 2, 'concept', 'segregation|access'), S('s2', 'Spreadsheet control', 2, 'concept', 'spreadsheet|review'), S('s3', 'Journal approval', 2, 'concept', 'approval|journal')],
          ['Risk and control each.'], ['Listing controls without risks.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What are the benefits of ERP for financial reporting?', 'An integrated database across functions gives consistent data, real-time reporting and built-in controls.',
          [P('p1', 'Integrated data', 5, 'integrat'), P('p2', 'Real-time reporting', 5, 'real-time')], 'c1'),
        V('v2', 'Name three common cyber threats to finance teams.', 'Phishing, ransomware and business email compromise asking for payments to new bank accounts.',
          [P('p1', 'Phishing and ransomware', 5, 'phishing|ransomware'), P('p2', 'Email compromise', 5, 'email')], 'c2'),
        V('v3', 'How can blockchain help reconciliation?', 'Parties share the same tamper-resistant ledger, so balances agree automatically and differences reduce.',
          [P('p1', 'Shared ledger', 5, 'shared'), P('p2', 'Tamper-resistant', 5, 'tamper')], 'c3'),
        V('v4', 'Why does AI still need human oversight?', 'Because outputs depend on data quality and may be biased or hard to explain, so accountants must validate and take responsibility.',
          [P('p1', 'Data quality or bias', 5, 'data|bias'), P('p2', 'Accountant responsibility', 5, 'responsib|validate')], 'c3'),
        V('v5', 'Give two ICOFR controls in an ERP.', 'Role-based access with segregation of duties, and approval workflows with audit trails for manual journals.',
          [P('p1', 'Segregation of duties', 5, 'segregation'), P('p2', 'Approval and audit trail', 5, 'approval|audit trail')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Glide Retail Ltd.', 'difficulty': 'core',
              'case': 'Glide Retail Ltd. moved to a cloud ERP. An employee received an email, apparently from a supplier, changing bank details; ₹40 lakh was paid before the fraud was noticed. The audit trail feature had been switched off to improve speed. Expected credit losses are computed by an AI model no one reviews.',
              'mcqs': [
                  M('k1a', 'The fraud is an example of:', ['Business email compromise', 'Ransomware', 'Denial of service', 'Malware on ERP'], 0,
                    'Fake instructions by email. In practice: call-back verification.', 'core', topic=T2),
                  M('k1b', 'Switching off the audit trail is:', ['A control failure and a breach of Indian requirements', 'Acceptable for speed', 'Required on cloud', 'Irrelevant'], 0,
                    'Audit trail must be maintained. In practice: cannot be disabled.', 'core', topic=T4),
                  M('k1c', 'The unreviewed AI ECL model creates a risk of:', ['Misstated loss allowance without accountability', 'Faster closing only', 'No risk', 'Lower tax'], 0,
                    'Models need validation. In practice: review outputs.', 'core', topic=T3),
                  M('k1d', 'A cloud ERP shifts which of these to the service provider?', ['Infrastructure management', 'Responsibility for financial statements', 'Ind AS judgements', 'Board approval'], 0,
                    'Management remains responsible for reporting. In practice: vendor assurance reports.', 'moderate', topic=T1),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch17', 1, 'Accounting and Technology',
                ['Explain automation, cloud computing and ERP in accounting.',
                 'Identify cyber threats and protective measures.',
                 'Assess blockchain and AI for financial reporting.',
                 'Design ICOFR controls for Ind AS reporting in an ERP.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 20}, 'prereq': ['fin-p1-ch16-u01'],
                 'exam_tip': 'For technology cases, pair every risk with a specific control.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['RPA for routine tasks; ERP integrates data.',
                             'Cloud: scalable but needs security and vendor oversight.',
                             'Cyber: phishing, ransomware, BEC — train and verify.',
                             'Blockchain and AI improve evidence; judgement stays human.',
                             'ICOFR: SoD, approvals, access reviews, audit trail.'],
                 'remember': ['Audit trail must stay enabled.'],
                 'traps': ['Assuming technology removes management responsibility.']},
                [('RPA', 'Rule-based tasks'), ('BEC defence', 'Call-back'), ('ERP control', 'Segregation of duties'), ('Spreadsheets', 'Review and reconcile')],
                viva, cases)
