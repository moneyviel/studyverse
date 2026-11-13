"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 4 Materiality, Risk Assessment and Internal Control.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch04-u01'
T1 = 'Materiality and performance materiality (SA 320)'
T2 = 'Risk-based audit approach (SA 315 and SA 330)'
T3 = 'Internal control: nature, components and limitations'
T4 = 'Evaluating and reporting on internal control (SA 265, IFC frameworks)'


def build():
    ck = Checks()
    om = ck.add('400*0.05', 'Overall materiality at 5% of profit before tax (₹ lakh)')
    pm = ck.add('400*0.05*0.75', 'Performance materiality at 75% (₹ lakh)')
    ct = ck.add('400*0.05*0.05', 'Clearly trivial threshold at 5% of materiality (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Setting materiality', 'difficulty': 'core', 'minutes': 6,
          'q': 'Sun Ltd. has a stable profit before tax of ₹400 lakh. The auditor uses 5% of profit before tax as overall materiality, sets performance materiality at 75% of overall materiality, and treats 5% of overall materiality as clearly trivial. Compute the three amounts and explain why performance materiality is lower.',
          'solution': [table(['Measure', 'Working', '₹ lakh'], [
              ['Overall materiality', '400 × 5%', inr(om)],
              ['Performance materiality', '20 × 75%', inr(pm)],
              ['Clearly trivial', '20 × 5%', inr(ct)],
              ['Why lower', 'Reduces risk that aggregate uncorrected and undetected misstatements exceed overall materiality', '—']], title='SA 320')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Classify the control weakness', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Identify the internal control component affected: (a) the board never reviews ethics policies; (b) management has no process to identify new business risks; (c) one clerk both records and approves payments; (d) the ERP produces unreliable reports; (e) no one follows up on internal audit findings.',
          'solution': [table(['Weakness', 'Component'], [
              ['(a)', 'Control environment'],
              ['(b)', 'Entity\'s risk assessment process'],
              ['(c)', 'Control activities (segregation of duties)'],
              ['(d)', 'Information system and communication'],
              ['(e)', 'Monitoring of controls']], title='Five components')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Misstatements are material if, individually or together, they could reasonably influence economic decisions of users. Materiality is a matter of judgement, considering size and nature, and is applied in planning, performing and evaluating the audit (SA 320).',
            'Overall materiality uses a benchmark (profit before tax, revenue, total assets, equity) and a percentage suited to the entity; specific materiality applies to particular items (e.g. related party or director remuneration disclosures).',
            'Performance materiality is set below overall materiality to reduce aggregation risk. Materiality is revised if information during the audit would have led to a different amount.'],
          'Materiality is the line between what matters and what does not.',
          'A loss-making year may require revenue or assets as the benchmark.'),
        C('c2', T2, [
            'Audit risk = risk of material misstatement (inherent risk × control risk) × detection risk. The auditor assesses risks at the financial statement and assertion levels through risk assessment procedures — enquiry, analytical procedures, observation and inspection — and understanding the entity, its environment, framework and internal control (SA 315).',
            'Significant risks need special audit attention. Responses (SA 330): overall responses (team, skepticism, unpredictability) and further audit procedures — tests of controls when relying on controls, and substantive procedures for all material classes, always including substantive procedures for significant risks.',
            'Higher assessed risk calls for more persuasive evidence: more extensive, closer to year end, and more reliable procedures.'],
          'Assess risks first, then design responses to fit them.',
          'If control risk is high, detection risk must be kept low through more substantive work.'),
        C('c3', T3, [
            'Internal control is the process designed and maintained by those charged with governance, management and others to provide reasonable assurance about reliable reporting, effective and efficient operations and compliance with laws.',
            'Components: control environment, entity\'s risk assessment process, information system and communication, control activities (authorisation, reconciliation, verification, physical controls, segregation of duties) and monitoring of controls.',
            'Inherent limitations: human error, collusion, management override, cost-benefit constraints and controls designed for routine transactions.'],
          'Five components work together — and none is foolproof.',
          'Collusion between two employees can defeat segregation of duties.'),
        C('c4', T4, [
            'The auditor reviews controls using narratives, flowcharts and questionnaires, evaluates design and implementation, and tests operating effectiveness where relying on them (walkthroughs, re-performance, inspection).',
            'SA 265 requires communicating significant deficiencies in internal control in writing to those charged with governance, and other deficiencies of sufficient importance to management, on a timely basis.',
            'Frameworks: COSO internal control framework, and in India the Companies Act requirement (section 143(3)(i)) for auditors of applicable companies to state whether internal financial controls over financial reporting are adequate and working effectively, guided by ICAI\'s Guidance Note.'],
          'Evaluate controls, then report weaknesses to the right people.',
          'A significant deficiency must be communicated in writing to the audit committee.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Risk assessment for a new client', 'role': 'Audit senior',
             'situation': 'A fast-growing e-commerce company with high revenue pressure.',
             'steps': ['Set materiality and performance materiality.', 'Identify significant risks such as revenue and returns.', 'Evaluate key controls and IT systems.', 'Design responses and communicate deficiencies.'],
             'takeaway': 'Materiality and risk drive the amount and type of work.'}]

    mcqs = [
        Q('m1', 'Performance materiality is set:', ['Below overall materiality', 'Above overall materiality', 'Equal to it', 'At zero'], 0,
          'Reduces aggregation risk. In practice: 50–75% common.', 'c1', T1),
        Q('m2', 'Audit risk is a function of:', ['Risk of material misstatement and detection risk', 'Fees and time', 'Materiality only', 'Sampling only'], 0,
          'RMM = inherent × control. In practice: detection risk controllable.', 'c2', T2),
        Q('m3', 'For significant risks, the auditor must perform:', ['Substantive procedures specifically responsive to the risk', 'Only tests of controls', 'Only analytical procedures', 'Nothing extra'], 0,
          'SA 330. In practice: plus controls if relying.', 'c2', T2),
        Q('m4', 'Segregation of duties is part of:', ['Control activities', 'Control environment', 'Monitoring', 'Risk assessment'], 0,
          'Prevents errors and fraud. In practice: authorise, record, custody separated.', 'c3', T3),
        Q('m5', 'A limitation of internal control is:', ['Collusion and management override', 'Too much assurance', 'Absolute certainty', 'No cost'], 0,
          'Only reasonable assurance. In practice: auditors stay skeptical.', 'c3', T3),
        Q('m6', 'Significant deficiencies must be communicated:', ['In writing to those charged with governance', 'Orally to staff', 'Only to shareholders', 'Never'], 0,
          'SA 265. In practice: timely.', 'c4', T4),
        Q('m7', 'Reporting on internal financial controls is required by:', ['Section 143(3)(i) of the Companies Act', 'Section 134 only', 'SEBI LODR only', 'Income-tax Act'], 0,
          'For applicable companies. In practice: ICAI Guidance Note.', 'c4', T4),
        Q('m8', 'Risk assessment procedures include:', ['Enquiry, analytical procedures, observation and inspection', 'Only confirmations', 'Only recalculation', 'Only sampling'], 0,
          'SA 315. In practice: understand the entity.', 'c2', T2),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Amounts', 3, 'computation', 'materiality|trivial', nums=[om, pm, ct]), S('s2', 'Reason', 2, 'concept', 'aggregat|undetected')],
          ['Justify benchmark.'], ['Setting performance materiality above overall.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Environment and risk', 2, 'concept', 'environment|risk assessment'), S('s2', 'Activities and information', 2, 'concept', 'activities|information'), S('s3', 'Monitoring', 1, 'concept', 'monitoring')],
          ['One component each.'], ['Confusing monitoring with control activities.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is materiality?', 'Misstatements are material if, alone or together, they could reasonably influence users\' economic decisions.',
          [P('p1', 'Influence decisions', 6, 'influence'), P('p2', 'Users', 4, 'user')], 'c1'),
        V('v2', 'State the audit risk model.', 'Audit risk equals inherent risk times control risk times detection risk.',
          [P('p1', 'Inherent and control', 5, 'inherent|control'), P('p2', 'Detection', 5, 'detection')], 'c2'),
        V('v3', 'Name the five components of internal control.', 'Control environment, risk assessment, information system and communication, control activities and monitoring.',
          [P('p1', 'Environment and risk', 5, 'environment|risk'), P('p2', 'Activities and monitoring', 5, 'activities|monitoring')], 'c3'),
        V('v4', 'What does SA 265 require?', 'Written communication of significant deficiencies in internal control to those charged with governance on a timely basis.',
          [P('p1', 'Significant deficiencies', 5, 'significant deficienc'), P('p2', 'In writing', 5, 'written|writing')], 'c4'),
        V('v5', 'What is performance materiality?', 'An amount below overall materiality used to reduce the risk that total uncorrected and undetected misstatements exceed materiality.',
          [P('p1', 'Below overall', 5, 'below'), P('p2', 'Aggregation risk', 5, 'undetected|total')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Ruby Textiles Ltd.', 'difficulty': 'moderate',
              'case': 'Ruby Textiles had revenue of ₹200 crore and a small loss this year. The auditor chose 1% of revenue as overall materiality. The CFO can approve and release payments alone. Internal audit reported weaknesses that management ignored.',
              'mcqs': [
                  M('k1a', 'Overall materiality (₹ crore):', ['2', '20', '0.2', '1'], 0,
                    '200 × 1%. In practice: revenue benchmark in loss years.', 'core', check=2, topic=T1),
                  M('k1b', 'CFO approving and releasing payments alone is a weakness in:', ['Segregation of duties', 'Monitoring', 'Risk assessment', 'Information system'], 0,
                    'Control activity. In practice: dual authorisation.', 'core', topic=T3),
                  M('k1c', 'Ignoring internal audit findings reflects weakness in:', ['Monitoring and control environment', 'Only control activities', 'Nothing', 'Materiality'], 0,
                    'No follow-up. In practice: communicate to TCWG.', 'moderate', topic=T3),
                  M('k1d', 'These weaknesses, if significant, are communicated under:', ['SA 265', 'SA 320', 'SA 530', 'SA 700'], 0,
                    'In writing to TCWG. In practice: also management letter.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch04', 1, 'Materiality, Risk Assessment and Internal Control',
                ['Determine materiality and performance materiality.',
                 'Apply the risk-based audit approach.',
                 'Explain components and limitations of internal control.',
                 'Evaluate controls and report deficiencies.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p3-ch03-u01'],
                 'exam_tip': 'Link each weakness to a COSO component and a risk, then propose a control.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['SA 320: overall, specific and performance materiality.',
                             'AR = IR × CR × DR.',
                             'SA 315 risk assessment; SA 330 responses.',
                             'Five components of internal control.',
                             'SA 265 deficiencies; IFC reporting under 143(3)(i).'],
                 'remember': ['Substantive procedures always for significant risks.'],
                 'traps': ['Relying on controls without testing them.']},
                [('Benchmark', 'PBT, revenue, assets'), ('PM', '< overall materiality'), ('Significant risk', 'Substantive procedures'), ('SA 265', 'Written to TCWG')],
                viva, cases)
