"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 3 Audit Planning, Strategy and Execution.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch03-u01'
T1 = 'Commencing the audit, strategy and plan (SA 300)'
T2 = 'Audit programme and execution'
T3 = 'Using the work of others: SA 600, SA 610 and SA 620'
T4 = 'Accounting estimates (SA 540)'
T5 = 'Evaluating misstatements (SA 450)'


def build():
    ck = Checks()
    tot = ck.add('18+12+15', 'Total uncorrected misstatements (₹ lakh)')
    ct = ck.add('50*0.05', 'Clearly trivial threshold at 5% of materiality (₹ lakh)')
    head = ck.add('50-(18+12+15)', 'Headroom below overall materiality (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Accumulating misstatements', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Overall materiality for Vega Ltd. is ₹50 lakh; the auditor treats amounts below 5% of materiality as clearly trivial. Uncorrected misstatements: a factual cut-off error of ₹18 lakh, a judgemental difference on a provision of ₹12 lakh, and a projected misstatement from sampling of ₹15 lakh. Management refuses to correct them. Evaluate under SA 450.',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Clearly trivial threshold', '50 × 5%', inr(ct)],
              ['Total uncorrected', '18 + 12 + 15', inr(tot)],
              ['Headroom', '50 − 45', inr(head)],
              ['Evaluation', 'Close to materiality — consider qualitative factors and risk of undetected misstatements; ask management to correct', '—'],
              ['Actions', 'Communicate to TCWG; obtain written representation on uncorrected misstatements', '—']], title='SA 450')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Can we use their work?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'The auditor of Nova Ltd. wants to (a) use the internal audit team\'s inventory counts; (b) ask internal auditors to directly assist in testing payables; (c) rely on a property valuer appointed by management; (d) use another firm\'s audit of a branch. Which SA applies and what must be evaluated?',
          'solution': [table(['Item', 'SA', 'Evaluate'], [
              ['(a)', 'SA 610', 'Objectivity, competence, systematic and disciplined approach; perform own procedures on that work'],
              ['(b)', 'SA 610 (direct assistance)', 'Possible unless law or regulation prohibits it; evaluate objectivity and competence; not for significant judgements or high-risk work; direct, supervise and review'],
              ['(c)', 'SA 500 (management\'s expert)', 'Competence, capabilities, objectivity; understand and evaluate the work'],
              ['(d)', 'SA 600', 'Other auditor\'s competence and independence; communicate and review as needed']], title='Using others\' work')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Planning (SA 300) develops an overall audit strategy (scope, timing, direction, reporting objectives, resources) and an audit plan (nature, timing and extent of risk assessment procedures, further procedures and other procedures). Planning is continuous and updated as the audit proceeds; extent depends on size, complexity, experience with the entity and changes.',
            'Before starting: agree terms of engagement (SA 210), perform acceptance and continuance procedures, evaluate ethics and independence, and in an initial audit communicate with the predecessor auditor.',
            'Documentation includes the strategy, plan, significant changes and reasons. Direction, supervision and review of the team are planned according to risk.'],
          'Strategy sets the direction; the plan sets the steps.',
          'A first-year audit needs more planning time than a recurring one.'),
        C('c2', T2, [
            'An audit programme lists procedures for each area, aligned to assertions and risks; it guides staff, records work done and supports review. It must be flexible enough to respond to new findings.',
            'Execution covers planning the fieldwork, understanding and evaluating risks and controls (SA 315), testing controls and performing substantive procedures (SA 330), and reporting.',
            'Other considerations during execution include materiality (SA 320), communications, written representations and documentation (SA 230).'],
          'Programme the work, then execute it to the risks.',
          'A receivables programme includes confirmations, ageing review and cut-off tests.'),
        C('c3', T3, [
            'SA 600 (using the work of another auditor): the principal auditor is responsible for the opinion; considers the other auditor\'s professional competence and independence, communicates requirements, and may review their work; generally no reference to the other auditor is made unless law or practice permits, in which case responsibility is not divided.',
            'SA 610 (internal auditors): evaluate objectivity, competence and systematic approach; decide the extent of use based on risk and judgement involved; perform audit procedures on work used. Internal auditors may provide direct assistance under the external auditor\'s direction, supervision and review unless law or regulation prohibits it; they cannot be used for work involving significant judgement, higher assessed risks or areas they were involved in.',
            'SA 620 (auditor\'s expert): evaluate competence, capabilities and objectivity; agree scope and objectives in writing; evaluate adequacy of findings. No reference to the expert in an unmodified report.'],
          'Use others\' work, but never hand over responsibility.',
          'An auditor uses an actuary for gratuity but still owns the conclusion.'),
        C('c4', T4, [
            'Accounting estimates (provisions, fair values, impairment, ECL, useful lives) involve estimation uncertainty, complexity and subjectivity. SA 540 (Revised) requires understanding how management makes estimates and assessing inherent risk factors.',
            'Responses: test how management made the estimate (methods, data, assumptions), develop an auditor\'s point estimate or range, or use events up to the report date. Evaluate management bias indicators and adequacy of disclosures about uncertainty.',
            'Retrospective review of prior-period estimates helps identify bias and the effectiveness of management\'s process.'],
          'Estimates are judgements — audit the method, data and assumptions.',
          'Comparing last year\'s warranty provision with actual claims tests estimation quality.'),
        C('c5', T5, [
            'SA 450 requires accumulating misstatements other than clearly trivial ones. Types: factual (no doubt), judgemental (differences in estimates or policies) and projected (extrapolated from samples).',
            'Misstatements are communicated to management for correction; if uncorrected, the auditor considers their size and nature individually and in aggregate, qualitative factors, and effect on materiality.',
            'Uncorrected misstatements are communicated to TCWG, a written representation obtained that management believes their effect is immaterial, and documentation kept. If material, the opinion is modified.'],
          'Add up what is wrong, ask for correction, and judge what remains.',
          'Uncorrected errors of ₹45 lakh against ₹50 lakh materiality leave little headroom.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Planning a group audit kick-off', 'role': 'Audit senior',
             'situation': 'A new manufacturing client with two branches audited by other firms.',
             'steps': ['Agree engagement terms and communicate with predecessor.', 'Draft overall strategy and plan.', 'Decide use of internal audit and experts.', 'Set misstatement tracking thresholds.'],
             'takeaway': 'Good planning decides how much reliance on others is safe.'}]

    mcqs = [
        Q('m1', 'The overall audit strategy sets:', ['Scope, timing and direction of the audit', 'Detailed procedures only', 'Fees only', 'The opinion'], 0,
          'Audit plan details procedures. In practice: both documented.', 'c1', T1),
        Q('m2', 'Planning under SA 300 is:', ['A continual process throughout the audit', 'Done only at the start', 'Optional for small audits', 'Done after fieldwork'], 0,
          'Updated as needed. In practice: document changes.', 'c1', T1),
        Q('m3', 'Under SA 610, internal auditors providing direct assistance cannot be used for:', ['Procedures involving significant judgement', 'Routine low-risk tests', 'Work supervised by the auditor', 'Any procedure'], 0,
          'Also excluded: higher-risk areas and work they were involved in. In practice: only if not prohibited by law.', 'c3', T3),
        Q('m4', 'Under SA 620, an unmodified report:', ['Does not refer to the auditor\'s expert', 'Names the expert', 'Attaches the expert report', 'Shares responsibility'], 0,
          'No division of responsibility. In practice: reference only if relevant to modification.', 'c3', T3),
        Q('m5', 'Misstatements arising from extrapolating sample errors are:', ['Projected misstatements', 'Factual', 'Judgemental', 'Trivial'], 0,
          'SA 450 types. In practice: add to aggregate.', 'c5', T5),
        Q('m6', 'SA 540 requires the auditor to evaluate:', ['Methods, data and assumptions behind estimates', 'Only arithmetic', 'Only disclosures', 'Nothing if management is honest'], 0,
          'Plus bias indicators. In practice: retrospective review.', 'c4', T4),
        Q('m7', 'Under SA 600, responsibility for the opinion on the whole statements rests with:', ['The principal auditor', 'Both auditors equally', 'The other auditor', 'Management'], 0,
          'Principal auditor\'s report. In practice: assess other auditor\'s competence.', 'c3', T3),
        Q('m8', 'An audit programme helps by:', ['Guiding staff, recording work done and aiding review', 'Replacing judgement', 'Fixing fees', 'Avoiding documentation'], 0,
          'Control tool. In practice: tailor to risks.', 'c2', T2),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Threshold and total', 2, 'computation', 'trivial|total', nums=[ct, tot]), S('s2', 'Evaluation', 2, 'concept', 'qualitative|close'), S('s3', 'Actions', 2, 'concept', 'representation|governance')],
          ['Classify each misstatement.'], ['Ignoring projected errors.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'SA 610', 2, 'concept', '610'), S('s2', 'Experts', 2, 'concept', 'expert|500'), S('s3', 'SA 600', 2, 'concept', '600')],
          ['Cite each SA.'], ['Using direct assistance for significant judgements.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Distinguish the overall audit strategy and the audit plan.', 'The strategy sets scope, timing and direction; the plan details the nature, timing and extent of procedures.',
          [P('p1', 'Scope and direction', 5, 'scope|direction'), P('p2', 'Nature timing extent', 5, 'nature|timing|extent')], 'c1'),
        V('v2', 'What does the auditor evaluate before using internal audit work?', 'The internal audit function\'s objectivity, competence and systematic and disciplined approach.',
          [P('p1', 'Objectivity', 5, 'objectivity'), P('p2', 'Competence and approach', 5, 'competence|systematic')], 'c3'),
        V('v3', 'What are the three types of misstatement under SA 450?', 'Factual, judgemental and projected misstatements.',
          [P('p1', 'Factual and judgemental', 5, 'factual|judgemental'), P('p2', 'Projected', 5, 'projected')], 'c5'),
        V('v4', 'How can an auditor respond to risks in estimates?', 'Test management\'s process, develop an independent point estimate or range, or use events up to the report date.',
          [P('p1', 'Test process', 5, 'process|test'), P('p2', 'Own estimate or later events', 5, 'estimate|events')], 'c4'),
        V('v5', 'Does using an expert reduce the auditor\'s responsibility?', 'It leaves the auditor solely responsible for the opinion.',
          [P('p1', 'Sole responsibility', 6, 'solely'), P('p2', 'Opinion', 4, 'opinion')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Lotus Hotels Ltd.', 'difficulty': 'moderate',
              'case': 'Lotus Hotels has properties revalued by an external valuer appointed by management. The statutory auditor engages its own IT specialist. A branch in Goa is audited by another firm. Internal auditors offer to test room revenue directly under the statutory auditor\'s supervision.',
              'mcqs': [
                  M('k1a', 'The valuer appointed by Lotus is:', ['A management\'s expert', 'An auditor\'s expert', 'An internal auditor', 'A component auditor'], 0,
                    'Evaluate under SA 500. In practice: assess objectivity.', 'core', topic=T3),
                  M('k1b', 'The IT specialist engaged by the auditor is governed by:', ['SA 620', 'SA 610', 'SA 600', 'SA 402'], 0,
                    'Auditor\'s expert. In practice: written agreement.', 'core', topic=T3),
                  M('k1c', 'The offer of direct assistance on room revenue testing can be accepted only if:', ['Not prohibited by law, objectivity and competence are adequate, and the work is supervised and reviewed', 'Management insists', 'Internal auditors sign the report', 'The fee is reduced'], 0,
                    'SA 610 conditions. In practice: avoid significant judgement areas.', 'moderate', topic=T3),
                  M('k1d', 'Work of the Goa branch auditor is considered under:', ['SA 600', 'SA 299', 'SA 220', 'SA 260'], 0,
                    'Using work of another auditor. In practice: Companies Act section 143(8).', 'core', topic=T3),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch03', 1, 'Audit Planning, Strategy and Execution',
                ['Plan the audit with an overall strategy and audit plan.',
                 'Design and use audit programmes during execution.',
                 'Use the work of other auditors, internal auditors and experts.',
                 'Audit accounting estimates under SA 540.',
                 'Evaluate misstatements under SA 450.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p3-ch02-u01'],
                 'exam_tip': 'When others\' work is involved, identify the right SA first — 600, 610, 620 or 500.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['SA 300: strategy + plan, continuous.',
                             'Audit programme tied to risks and assertions.',
                             'SA 600, 610, 620 — responsibility stays with auditor.',
                             'SA 540: methods, data, assumptions, bias.',
                             'SA 450: factual, judgemental, projected.'],
                 'remember': ['Direct assistance is allowed only if law does not prohibit it, and never for significant judgements.'],
                 'traps': ['Referring to the expert in an unmodified report.']},
                [('SA 300', 'Planning'), ('SA 610', 'Internal auditors'), ('SA 620', 'Auditor\'s expert'), ('SA 450', 'Misstatements')],
                viva, cases)
