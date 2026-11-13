"""CA Intermediate · Paper 5 Auditing and Ethics · Chapter 2 Audit Strategy, Audit Planning and Audit Programme.
Scope follows the ICAI study material; explanations, examples and scenarios are original."""
from ikit import *

UID = 'int-p5-ch02-u01'
T1 = 'Why plan an audit (SA 300)'
T2 = 'Planning is continuous and iterative'
T3 = 'Preliminary engagement activities'
T4 = 'Overall audit strategy'
T5 = 'The audit plan and its link with strategy'
T6 = 'Changes, supervision and documentation'
T7 = 'Audit programme: meaning and construction'
T8 = 'Audit programme: evidence, merits and demerits'


def build():
    benefits = table(['Benefit of planning', 'What it means in practice'], [
        ['Attention to important areas', 'More time and senior staff on high-risk balances'],
        ['Early identification of problems', 'Issues such as missing records surface before the deadline'],
        ['Efficient organisation', 'Work is sequenced and budgeted, avoiding last-minute rush'],
        ['Right team for the risks', 'Experienced members and specialists where needed'],
        ['Direction, supervision and review', 'Clear assignment makes reviewing work easier'],
        ['Co-ordination with others', 'Work of experts and other auditors is lined up in time'],
    ], title='Benefits of planning')
    strat_plan = table(['Basis', 'Overall audit strategy', 'Audit plan'], [
        ['What it sets', 'Scope, timing and direction of the audit', 'Nature, timing and extent of audit procedures'],
        ['Level of detail', 'Broad approach', 'Detailed — how the strategy will be carried out'],
        ['Contents', 'Resources to deploy, how much, when, and how they are managed', 'Risk assessment procedures, further procedures at assertion level, other procedures required by SAs'],
        ['Order', 'Established first, guides the plan', 'Developed from the strategy; changes in either can change the other'],
    ], title='Strategy vs plan')
    prog = table(['Advantages', 'Disadvantages (and remedy)'], [
        ['Clear, complete instructions for assistants', 'Work may become mechanical'],
        ['Total view of the work in big audits', 'Programme may become rigid while the business changes'],
        ['Easier allocation of work by ability', 'Weak assistants may hide behind "not in the programme"'],
        ['Less risk of overlooking books or records', 'Can stifle initiative of good assistants'],
        ['Signed steps fix responsibility for work done', 'Remedy: periodic review and imaginative supervision; encourage assistants to report unusual matters'],
        ['Principal can track progress; guide for next year; evidence of due care if negligence is alleged', ''],
    ], title='Audit programme — merits and demerits')

    illus = [
        {'id': 'i1', 'title': 'Sorting planning activities', 'difficulty': 'core', 'minutes': 6,
         'q': 'An auditor appointed for the first time by Godavari Auto Parts Ltd. does the following. Classify each as a preliminary engagement activity, part of the overall audit strategy, or part of the audit plan: (a) enquires about the integrity of the promoters; (b) checks the team\'s independence; (c) sends an engagement letter; (d) decides to use a valuation expert and to put senior staff on inventory at three plants; (e) fixes the reporting timetable with management; (f) decides to vouch a sample of 60 purchase invoices in December and March.',
         'solution': [table(['Activity', 'Classification'], [
             ['(a) Integrity of promoters', 'Preliminary — acceptance/continuance of client'],
             ['(b) Independence of team', 'Preliminary — compliance with ethical requirements'],
             ['(c) Engagement letter', 'Preliminary — agreeing terms of engagement'],
             ['(d) Expert and senior staff for inventory', 'Overall audit strategy — resources to deploy and where'],
             ['(e) Reporting timetable', 'Overall audit strategy — reporting objectives and timing'],
             ['(f) Sample of 60 invoices in Dec and Mar', 'Audit plan — nature, timing and extent of further procedures']], title='Answer')]},
        {'id': 'i2', 'title': 'A finance head writing the audit strategy', 'difficulty': 'core', 'minutes': 4,
         'q': 'The auditor of Tapi Textiles Ltd. asks the company\'s finance head to prepare the audit strategy and detailed procedures to save time, and adopts them unchanged. Comment.',
         'solution': [legal('SA 300 — the overall audit strategy and audit plan remain the auditor\'s responsibility', 'The auditor adopted a strategy and procedures written by the client\'s finance head.',
                            'The auditor may discuss elements of planning with management, but care is needed not to compromise effectiveness; procedures known in advance lose their element of unpredictability and the client would effectively be auditing itself.',
                            'The approach is wrong — the auditor must establish the strategy and develop the plan himself.')]},
    ]

    concepts = [
        C('c1', T1, [
            'SA 300 requires the auditor to plan the audit so that it is performed effectively.',
            'Adequate planning helps the auditor (table): focus on important areas, spot and solve problems early, organise the engagement efficiently, select a team with the right skills, direct, supervise and review team members, and co-ordinate the work of experts and other auditors.',
            'Good planning keeps audit risk — the risk of giving an inappropriate opinion — at an acceptably low level.'],
          'Planning an audit is like planning a wedding: guest list (scope), budget (resources), schedule (timing) and who handles what (team) — skip it and something important is forgotten.',
          'Audit firms hold planning meetings weeks before year-end to allocate staff and fix inventory-count dates.',
          blocks=[benefits]),
        C('c2', T2, [
            'Planning is not a single phase; it is a continuous, iterative process that often starts soon after the previous audit ends and runs until the current one is completed.',
            'Before identifying risks, planning considers matters such as analytical procedures as risk assessment, understanding the legal and regulatory framework (e.g. RBI rules for banks, TRAI rules for telecom companies), materiality, the need for experts and other risk assessment procedures.',
            'The engagement partner and key team members take part in planning, bringing experience and insight.',
            'The auditor may discuss parts of the plan with management to ease the audit, but must not reveal so much that the audit becomes predictable and less effective.'],
          'Planning is like a GPS route — set at the start but recalculated whenever the road ahead changes.',
          'Auditors often begin next year\'s planning while writing this year\'s management letter.'),
        C('c3', T3, [
            'Before planning proper, the auditor performs preliminary engagement activities.',
            '(A) Acceptance and continuance procedures: consider the integrity of owners and key management, the team\'s competence, and issues from current and earlier audits; for a new client, communicate with the previous auditor.',
            '(B) Ethical requirements and independence: the engagement partner stays alert for breaches, identifies threats to independence, applies safeguards or withdraws where permitted, and reports unresolved matters to the firm.',
            '(C) Terms of engagement: an engagement letter sent before the audit begins avoids misunderstandings.',
            'These steps reveal events or conditions that could affect the auditor\'s ability to plan and perform the audit.'],
          'Before starting a journey with someone, you check whether you trust them, whether you are fit to travel, and agree who pays for what.',
          'Firms run a formal acceptance checklist (with background checks on promoters) before taking a new listed client.'),
        C('c4', T4, [
            'The overall audit strategy decides the audit\'s scope, its timing and its direction, and guides the detailed plan.',
            'It helps decide: which resources to use for specific areas (experienced staff on high-risk areas, experts for complex matters); how much to allocate (team size at inventory counts, review of other auditors in group audits, budget hours); when to deploy them (interim stage or key cut-off dates); and how to manage, direct and supervise them (briefings, reviews, quality reviews).',
            'Factors considered: (a) characteristics defining scope — reporting framework, business segments needing special knowledge, industry reporting rules, use of earlier audit evidence; (b) reporting objectives — the entity\'s reporting timetable, meetings with management, expected reports and communications; (c) significant factors directing the team — materiality, high-risk areas, volume of transactions, industry and legal changes; (d) results of preliminary activities and knowledge from other engagements; (e) nature, timing and extent of resources needed.'],
          'Strategy is the captain\'s match plan: who bowls at the death, which fielder guards the boundary, and when to take the powerplay.',
          'For a company with plants in five states, the strategy decides which plants senior staff visit at year-end.'),
        C('c5', T5, [
            'The audit plan, developed after the strategy, describes: (i) which risk assessment procedures will be done, when and how much; (ii) the same three aspects for further audit procedures at the assertion level; and (iii) any other procedures the SAs require.',
            'Knowledge of the client\'s business is essential to develop a sound plan.',
            'Risk assessment procedures are planned early; further procedures depend on their results, and some may start before all others are planned.',
            'Strategy and plan are closely inter-related, not strictly sequential — a change in one may require a change in the other. Both remain the auditor\'s responsibility.'],
          'If strategy says "attack the opponent\'s weak bowler", the plan says which batsman faces him, in which over and with what shots.',
          'A plan may specify, for example, confirmation of the top 20 debtors as at 31 March and vouching of a sample of March sales.',
          blocks=[strat_plan]),
        C('c6', T6, [
            'The auditor updates the strategy and plan whenever unexpected events, changed conditions or evidence differ significantly from what was expected — e.g. tests of detail contradict tests of controls.',
            'The nature, timing and extent of direction, supervision and review depend on the entity\'s size and complexity, the audit area, assessed risks, and the competence of individual team members.',
            'Documentation: the overall strategy, the audit plan, and any significant changes with reasons. Standard programmes and checklists may be used if tailored to the engagement.'],
          'A plan in a drawer is useless; a plan updated and recorded is a map others can follow and check.',
          'Peer reviewers check whether planning documents were updated when risks changed during the audit.'),
        C('c7', T7, [
            'An audit programme is a detailed, written list of examination and verification steps, arranged to show how they connect, designed with reference to the assertions in the financial statements — in effect a set of instructions for applying audit procedures.',
            'One programme cannot fit all businesses because nature, size, controls and scope differ; the auditor frames a standard programme covering the essential minimum and adapts it with experience.',
            'Assistants should keep an open mind and report significant matters beyond the programme to seniors. The programme must be reviewed periodically; working from an outdated programme may be treated as negligence.',
            'Construction points: stay within the scope of the assignment; write the programme; identify the best available evidence; include only useful steps; state objectives and enough detail for each area; consider all possibilities of error; co-ordinate procedures for related items. Timing is usually flexible, except for things like observing stock counts or verifying cash and securities at year-end.'],
          'An audit programme is a recipe card for the team: ingredients (records), steps (procedures), quantities (sample sizes) — but a good cook still tastes as she goes.',
          'Articled assistants sign off each step on the programme as they complete it.'),
        C('c8', T8, [
            'The programme is designed to obtain audit evidence. Broad sources of evidence: documents, physical examination, explanations of management and staff, third-party statements, the auditor\'s own calculations, internal controls, relationships among accounting data, subsidiary records, minutes, and subsequent actions.',
            'Best evidence depends on the item: for cash in hand, a physical count; for investments pledged with a bank, the bank\'s certificate; for debtors, invoices, credit notes, statements and external confirmations taken together.',
            'Merits and demerits are summarised in the table; the demerits are removed by periodic review, imaginative supervision and encouraging assistants to report unusual matters.'],
          'Evidence is like a jigsaw — no single piece shows the whole picture; the programme tells you which pieces to look for first.',
          'A signed, updated audit programme is often the auditor\'s best defence in a negligence case.',
          blocks=[prog]),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Planning a first-year audit', 'role': 'Audit manager',
         'situation': 'A new client manufactures auto parts at three plants with a large scrap business.',
         'steps': ['Complete acceptance checks and communication with the previous auditor; send an engagement letter.', 'Set the strategy: reporting framework, deadlines, plants to visit, senior staff on inventory and scrap.', 'Write the plan and programme, including steps for scrap sales and stock — and update them when new risks appear.'],
         'takeaway': 'Strategy first, plan next, programme for the team — all living documents.'},
        {'id': 'j2', 'title': 'An assistant finds something not in the programme', 'role': 'Articled assistant',
         'situation': 'While matching sales invoices with e-way bills, many e-way bills are found cancelled within a day in March.',
         'steps': ['Note the pattern with examples.', 'Report it to the senior immediately — it may indicate fictitious year-end sales.', 'The senior updates the plan and programme for cut-off testing.'],
         'takeaway': 'The programme is a minimum, not a limit; report unusual matters.'},
    ]

    mcqs = [
        Q('m1', 'Which Standard on Auditing deals with planning an audit of financial statements?', ['SA 300', 'SA 200', 'SA 230', 'SA 500'], 0,
          'SA 300 deals with the auditor\'s responsibility to plan the audit so it is performed effectively. SA 200 sets overall objectives, SA 230 covers documentation and SA 500 covers audit evidence. In practice: planning memos in audit files refer to SA 300 requirements.', 'c1', T1),
        Q('m2', 'Audit planning is best described as:', ['A continuous and iterative process through the audit', 'A one-time step completed before fieldwork', 'An activity done only at year-end', 'A task delegated to the client'], 0,
          'Planning often begins soon after the previous audit and continues until the current audit is completed; it is revised as new information arrives. It is not a discrete step or a client task. In practice: audit plans are updated after interim visits.', 'c2', T2),
        Q('m3', 'Checking the integrity of a new client\'s promoters is part of:', ['Preliminary engagement activities', 'The audit plan', 'Substantive procedures', 'The audit report'], 0,
          'Before planning, the auditor performs acceptance and continuance procedures, which include considering the integrity of principal owners and key management. The audit plan deals with procedures, not acceptance. In practice: firms decline clients whose promoters have a doubtful record.', 'c3', T3),
        Q('m4', 'The overall audit strategy mainly determines the audit\'s:', ['Scope, timing and direction', 'Exact sample sizes for each account', 'Wording of the audit report', 'Accounting policies of the entity'], 0,
          'The overall audit strategy decides the audit\'s scope, its timing and its direction, and guides the detailed audit plan. Sample sizes belong to the audit plan; accounting policies belong to management. In practice: strategy decides where experienced staff and experts are used.', 'c4', T4),
        Q('m5', 'Deciding to involve a valuation expert for complex derivatives is part of:', ['Establishing the overall audit strategy', 'The engagement letter', 'The audit report', 'Post-audit review only'], 0,
          'The strategy determines which resources to deploy, including experts for complex matters. The engagement letter records terms, not resource decisions. In practice: deciding early on experts avoids delays and cost overruns near the reporting deadline.', 'c4', T4),
        Q('m6', 'The audit plan includes:', ['Nature, timing and extent of risk assessment and further audit procedures', 'Only the audit fee', 'Only the engagement team names', 'The financial statements'], 0,
          'SA 300 requires the audit plan to describe what risk assessment and further audit procedures will be done, when and how much, plus any other procedures the SAs require. It is more detailed than the strategy. In practice: plans specify samples and dates.', 'c5', T5),
        Q('m7', 'Who is responsible for the overall audit strategy and audit plan?', ['The auditor', 'The company\'s finance head', 'The audit committee', 'The internal auditor'], 0,
          'The strategy and plan remain the auditor\'s responsibility; the auditor may discuss parts with management without compromising effectiveness. Letting the client prepare them would undermine independence and unpredictability. In practice: the engagement partner signs off the planning memo.', 'c5', T5),
        Q('m8', 'If tests of detail contradict the results of tests of controls, the auditor should:', ['Revise the strategy and plan and modify further procedures', 'Ignore the detail tests', 'Issue the report immediately', 'Ask management to change the records'], 0,
          'SA 300 requires the auditor to update the strategy and plan when evidence differs significantly from expectations, changing the nature, timing and extent of further procedures. Ignoring contradictory evidence would be negligent. In practice: reliance on controls may be withdrawn and substantive testing increased.', 'c6', T6, 'moderate'),
        Q('m9', 'The extent of supervision of engagement team members depends on all EXCEPT:', ['The audit fee agreed', 'The size and complexity of the entity', 'The assessed risks of material misstatement', 'Competence of individual team members'], 0,
          'Supervision depends on entity size and complexity, the audit area, assessed risks and team members\' capabilities. The fee does not determine how much supervision quality requires. In practice: high-risk areas handled by juniors get closer review.', 'c6', T6),
        Q('m10', 'Which of these must be documented under SA 300?', ['Overall strategy, audit plan and significant changes with reasons', 'Only the final audit report', 'Only the fee and engagement letter', 'Nothing — planning is informal'], 0,
          'The auditor documents the overall audit strategy, the audit plan and significant changes to either with the reasons. This records key decisions, supports review by seniors and explains the final approach. In practice: tailored standard checklists are often used.', 'c6', T6),
        Q('m11', 'An audit programme is:', ['A detailed written set of verification steps and instructions for the audit team', 'The client\'s accounting software', 'The engagement letter', 'The audit report format'], 0,
          'An audit programme lists the examination and verification steps, showing how they relate, with instructions on techniques and extent, so the team can gather evidence for the opinion. It is not the engagement letter or report. In practice: each step is signed by the person who performs it.', 'c7', T7),
        Q('m12', 'Why is one standard audit programme for all businesses not practicable?', ['Businesses differ in nature, size, controls and scope of work', 'ICAI prohibits standard programmes', 'Programmes are not used in audits', 'Clients prepare their own programmes'], 0,
          'Because nature, size, composition, controls and the scope of service vary, a single programme cannot suit all; a standard minimum programme is adapted to each client. Standard programmes are allowed if tailored. In practice: a bank audit programme differs greatly from a retailer\'s.', 'c7', T7),
        Q('m13', 'For which of these does the auditor usually have no discretion over timing?', ['Observing the client\'s physical inventory count', 'Vouching routine expenses', 'Reviewing minutes of meetings', 'Testing payroll calculations'], 0,
          'Observation of stock-taking, and verification of cash and securities at year-end, must happen when the client counts or at the specific date. Other procedures can usually be scheduled flexibly. In practice: count dates are fixed in the strategy well in advance.', 'c7', T7, 'moderate'),
        Q('m14', 'The best evidence for cash in hand is:', ['Physical count', 'Cash book balance', 'Management representation', 'Bank statement'], 0,
          'Counting cash gives direct physical evidence of its existence; the cash book is the client\'s own record and representations are weak evidence. Bank statements relate to bank balances, not cash in hand. In practice: surprise cash counts are a common audit step.', 'c8', T8),
        Q('m15', 'A disadvantage of an audit programme is that:', ['Work may become mechanical and rigid', 'It fixes responsibility on assistants', 'It guides next year\'s audit', 'It is evidence of due care'], 0,
          'The main drawbacks are mechanical work, rigidity, assistants hiding behind it and loss of initiative; fixing responsibility, guiding next year and evidencing due care are advantages. The drawbacks are cured by review and supervision. In practice: managers encourage assistants to question unusual items.', 'c8', T8),
        Q('m16', 'An assistant notices an unusual pattern not covered by the programme. He should:', ['Report it to his senior or partner', 'Ignore it since it is not in the programme', 'Correct the client\'s books himself', 'Discuss it only with client staff'], 0,
          'Assistants should keep an open mind and report significant matters beyond the programme to seniors; the programme is a minimum, not a limit. Correcting the books is management\'s job. In practice: such reports often uncover cut-off manipulation or fraud.', 'c8', T8),
    ]

    questions = [
        W('q1', 4, 'State the benefits of planning an audit as per SA 300.',
          [benefits],
          [S('s1', 'Attention to important areas', 1, 'concept', 'important area|appropriate attention|significant area'),
           S('s2', 'Identify and resolve problems on time', 0.75, 'concept', 'problem'),
           S('s3', 'Efficient organisation and management', 0.75, 'concept', 'efficien|organi'),
           S('s4', 'Team selection and assignment', 0.5, 'concept', 'team|staff'),
           S('s5', 'Direction, supervision, review; co-ordination with experts', 1, 'concept', 'supervis|review|co-ordinat|coordinat|expert')],
          ['Six short points earn full marks.'], ['Writing about audit programme benefits instead.'], ['Use a list or table.']),
        W('q2', 4, 'Distinguish between the overall audit strategy and the audit plan.',
          [strat_plan],
          [S('s1', 'Strategy — scope, timing, direction', 1.5, 'concept', 'scope', 'timing', 'direction', n=2),
           S('s2', 'Plan — nature, timing, extent of procedures', 1.5, 'concept', 'nature', 'extent', 'procedure', n=2),
           S('s3', 'Detail and inter-relation', 1, 'concept', 'detail|inter-related|interrelated|broad')],
          ['Tabulate and add a line on their inter-relationship.'], ['Saying the plan comes before the strategy.'], ['Use a three-column table.'], pad='table'),
        W('q3', 5, 'What are the advantages of an audit programme? How can its disadvantages be overcome?',
          [prog],
          [S('s1', 'Clear instructions / total perspective', 1, 'concept', 'instruction|perspective'),
           S('s2', 'Fixes responsibility / tracks progress', 1, 'concept', 'responsib|progress'),
           S('s3', 'Guide for next year / evidence of due care', 1, 'concept', 'next year|succeeding|negligence|due care|evidence'),
           S('s4', 'Disadvantages — mechanical, rigid, initiative', 1, 'concept', 'mechanical|rigid|initiative'),
           S('s5', 'Remedy — review and supervision', 1, 'application', 'review|supervis')],
          ['Cover both parts of the question.'], ['Listing only disadvantages.'], ['Use a two-column table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What are the three preliminary engagement activities?',
          'First, acceptance or continuance procedures for the client; second, checking that ethics and independence rules are met by the team; third, agreeing the terms of engagement with the client.',
          [P('p1', 'Acceptance / continuance of client', 4, 'acceptance|continuance'), P('p2', 'Ethics and independence', 3, 'ethic|independence'), P('p3', 'Terms of engagement', 3, 'terms|engagement letter')], 'c3'),
        V('v2', 'What does the overall audit strategy set?',
          'It decides the audit\'s scope, its timing and its direction, and guides development of the detailed audit plan.',
          [P('p1', 'Scope', 3, 'scope'), P('p2', 'Timing', 3, 'timing'), P('p3', 'Direction', 2, 'direction'), P('p4', 'Guides the plan', 2, 'plan')], 'c4'),
        V('v3', 'What does SA 300 require the audit plan to describe?',
          'It describes what risk assessment procedures will be done, when and to what extent, the same for further audit procedures at the assertion level, and any other procedures the SAs require.',
          [P('p1', 'Risk assessment procedures', 4, 'risk assessment'), P('p2', 'Further audit procedures at assertion level', 4, 'further', 'assertion'), P('p3', 'Other procedures required by SAs', 2, 'other')], 'c5'),
        V('v4', 'What must be documented about planning?',
          'The overall audit strategy, the audit plan, and any significant changes made to them during the audit along with the reasons.',
          [P('p1', 'Strategy', 3, 'strategy'), P('p2', 'Plan', 3, 'plan'), P('p3', 'Significant changes and reasons', 4, 'change', 'reason')], 'c6'),
        V('v5', 'How can the disadvantages of an audit programme be removed?',
          'By periodic review of the programme, imaginative supervision of assistants, and encouraging them to report significant matters even if not in the programme.',
          [P('p1', 'Periodic review', 4, 'review'), P('p2', 'Supervision', 3, 'supervis'), P('p3', 'Encourage assistants to report', 3, 'encourag|report')], 'c8'),
    ]

    cases = [{'id': 'k1', 'title': 'First audit of Sabari Polymers Ltd.', 'difficulty': 'moderate',
              'case': 'CA Neha accepts the first audit of Sabari Polymers Ltd. after enquiring about its promoters and checking her team\'s skills. She fixes the reporting deadline with management, decides to visit two of four plants and to engage a chemical engineer to assess stock quantities. Her office issues a detailed set of instructions to assistants. Mid-way, an assistant finds large scrap sales not recorded in the books; the instructions are silent on scrap.',
              'mcqs': [
                  M('k1a', 'Enquiring about promoters and checking her team\'s skills are:', ['Preliminary engagement activities', 'Part of the audit plan', 'Substantive procedures', 'Part of the audit report'], 0,
                    'Considering the integrity of owners and the competence of the team are acceptance procedures, which are preliminary engagement activities before planning proper. They do not specify audit procedures, which belong to the plan. In practice: these are recorded in an acceptance checklist.', 'core', topic=T3),
                  M('k1b', 'Fixing the deadline, choosing plants to visit and engaging an engineer relate mainly to:', ['The overall audit strategy', 'The audit programme only', 'Post-audit review', 'The engagement letter'], 0,
                    'Reporting timetable, deployment of resources and use of experts are strategy matters that set scope, timing and direction. The programme gives detailed steps for assistants. In practice: these decisions are made early so the right resources are available.', 'core', topic=T4),
                  M('k1c', 'The detailed set of instructions issued to assistants is the:', ['Audit programme', 'Overall audit strategy', 'Engagement letter', 'Management representation'], 0,
                    'A detailed, written list of verification steps and instructions for the team is the audit programme. The overall strategy is broader and does not list individual steps. In practice: assistants sign each completed step so responsibility can be traced.', 'core', topic=T7),
                  M('k1d', 'On learning about unrecorded scrap sales, CA Neha should:', ['Update the audit plan and programme to cover scrap', 'Continue with the old instructions', 'Withdraw immediately', 'Ignore it as immaterial without assessment'], 0,
                    'SA 300 requires updating the strategy and plan when new information differs significantly from that used in planning; the programme must be revised to cover the risk. Continuing with outdated instructions could be negligent. In practice: scrap is a common area of revenue leakage.', 'moderate', topic=T6),
              ]}]

    return unit(UID, 'p5', 'int-p5-ch02', 1, 'Audit Strategy, Audit Planning and Audit Programme',
                ['Explain the need for and benefits of audit planning under SA 300.',
                 'Describe preliminary engagement activities and planning activities.',
                 'Distinguish the overall audit strategy from the audit plan and explain their documentation and revision.',
                 'Explain the audit programme, its construction, evidence it targets, and its merits and demerits.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 25}, 'prereq': ['int-p5-ch01-u01'],
                 'exam_tip': 'Case MCQs ask you to classify activities as preliminary, strategy or plan; theory asks benefits of planning, strategy vs plan, and audit programme merits.'},
                concepts, illus, jobs, mcqs, questions,
                {'summary': ['SA 300: plan so the audit is effective.', 'Planning is continuous and iterative.',
                             'Preliminary: acceptance/continuance, ethics and independence, terms of engagement.',
                             'Strategy = scope, timing, direction; plan = nature, timing, extent of procedures.',
                             'Update when evidence differs; document strategy, plan and changes with reasons.',
                             'Audit programme = detailed instructions; review periodically and supervise imaginatively.'],
                 'remember': ['Strategy and plan remain the auditor\'s responsibility.', 'Best evidence for cash = count.'],
                 'traps': ['Planning is not a one-time phase.', 'Sharing too much of the plan with management can reduce effectiveness.']},
                [('Planning standard', 'SA 300'), ('Strategy sets', 'Scope · Timing · Direction'), ('Plan describes', 'Nature · Timing · Extent of procedures'),
                 ('Document', 'Strategy, plan, significant changes + reasons'), ('Programme', 'Detailed written verification steps')],
                viva, cases,
                topics=['Auditor\'s Responsibility to Plan an Audit', 'Planning Process — Elements of Planning', 'Relationship between Audit Strategy and Audit Plan',
                        'Overall Audit Strategy and the Audit Plan — Auditor\'s Responsibility', 'Changes to Planning Decisions', 'Planning Supervision and Review', 'Documentation', 'Audit Programme'])
