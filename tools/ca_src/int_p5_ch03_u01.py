"""CA Intermediate · Paper 5 Auditing and Ethics · Chapter 3 Risk Assessment and Internal Control.
Scope follows the ICAI study material; explanations, examples and scenarios are original and machine-checked."""
from ikit import *

UID = 'int-p5-ch03-u01'
T1 = 'Audit risk and its components'
T2 = 'Identifying and assessing risks (SA 315)'
T3 = 'Materiality and performance materiality (SA 320)'
T4 = 'Understanding the entity and its environment'
T5 = 'Internal control: meaning, purpose and limitations'
T6 = 'Five components of internal control'
T7 = 'Significant risks'
T8 = 'Evaluating and testing internal control'
T9 = 'Responses to assessed risks (SA 330)'
T10 = 'Internal financial controls and documentation'
T11 = 'Controls in an automated environment'


def build():
    ck = Checks()
    dr = ck.add('0.05/(0.8*0.5)*100', 'Planned detection risk % = audit risk ÷ (inherent risk × control risk)')
    dr2 = ck.add('0.05/(0.8*0.9)*100', 'Detection risk % if control risk rises to 90%')
    i1 = {'id': 'i1', 'title': 'Using the audit risk model', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'For the inventory of Ganga Retail Ltd., the auditor wants audit risk of 5%. Inherent risk is assessed at 80% (easily stolen goods) and control risk at 50%. (a) What level of detection risk can be accepted? (b) If tests show controls are weak and control risk is reassessed at 90%, what happens?',
          'solution': [wn('Model', 'Audit risk = Inherent risk × Control risk × Detection risk, so DR = AR ÷ (IR × CR).'),
                       p(f'(a) DR = 0.05 ÷ (0.80 × 0.50) = {dr}%. (b) DR = 0.05 ÷ (0.80 × 0.90) = {dr2}%.'),
                       p('A lower acceptable detection risk means the auditor must do more and better substantive work — larger samples, year-end counts, more experienced staff. The auditor cannot change inherent or control risk; only detection risk is in his hands.'),
                       note('SAs usually assess inherent and control risk together as the risk of material misstatement; percentages are one of several acceptable ways to express it.')],
          'checks': list(ck)}

    ck2 = Checks()
    mat = ck2.add('0.05*500000000', 'Overall materiality = 5% of normalised PBT ₹50 crore')
    pm = ck2.add('0.6*25000000', 'Performance materiality at 60% of overall materiality')
    agg = ck2.add('6000000+5500000+5000000+4500000', 'Total of four small misstatements')
    i2 = {'id': 'i2', 'title': 'Setting materiality and performance materiality', 'difficulty': 'core', 'minutes': 7,
          'q': 'Sutlej Engineering Ltd. usually earns profit before tax of about ₹50 crore, but this year a one-time flood loss cut it to ₹9 crore. The auditor uses 5% of profit before tax as the starting point and sets performance materiality at 60% of overall materiality. Four uncorrected misstatements are found: inventory ₹60 lakh, receivables ₹55 lakh, provisions ₹50 lakh, depreciation ₹45 lakh. Determine materiality and evaluate.',
          'solution': [p('Benchmark: the year\'s profit is distorted by a one-off loss, so a normalised profit of ₹50 crore (based on past results and budget) is a better base.'),
                       table(['Item', '₹'], [['Overall materiality (5% × ₹50 crore)', inr(mat)], ['Performance materiality (60%)', inr(pm)],
                                             ['Aggregate of four misstatements', inr(agg)]], title='Working'),
                       p(f'Each misstatement is below overall materiality of {R(mat)}, but together they total {R(agg)}, which is below {R(mat)} — so, on size alone, not material. However, the auditor must still consider their nature and ask management to correct them; performance materiality of {R(pm)} was set precisely so that undetected plus uncorrected errors stay under overall materiality.')],
          'checks': list(ck2)}

    comp = table(['Component', 'Key point'], [
        ['Inherent risk', 'Susceptibility of an assertion to material misstatement before considering controls — e.g. cash, complex estimates'],
        ['Control risk', 'Risk that the entity\'s internal control will not prevent, or detect and correct, the misstatement in time'],
        ['Detection risk', 'Risk that the auditor\'s procedures miss a material misstatement — includes sampling and non-sampling risk'],
        ['Risk of material misstatement (RMM)', 'Inherent risk and control risk together; belongs to the entity'],
    ], title='Audit risk = RMM × detection risk = IR × CR × DR')
    ic5 = table(['Component', 'What the auditor looks at'], [
        ['Control environment', 'Integrity and ethical values, competence, governance participation, management\'s style, organisation structure, authority and responsibility, HR policies'],
        ['Entity\'s risk assessment process', 'How business risks relevant to reporting are identified, sized, judged for likelihood and acted upon'],
        ['Information system and communication', 'Significant transactions, how they are initiated, recorded, processed and reported; journal entry controls; communication of roles'],
        ['Control activities', 'Performance reviews, information processing controls, physical controls, segregation of duties'],
        ['Monitoring of controls', 'Ongoing and separate evaluations; remedial action; external feedback such as complaints and regulator comments'],
    ], title='Five components of internal control (SA 315)')
    methods = table(['Method', 'Features'], [
        ['Narrative record', 'Full written description of the system as operating; suits small entities with no formal system; hard to follow, to spot gaps and to update'],
        ['Check list', 'Instructions/questions to be completed and initialled by staff (Yes/No/NA); reviewed by seniors'],
        ['Internal control questionnaire', 'Comprehensive set of questions — the most widely used; omissions less likely; can be done in sections or at an interim date'],
        ['Flow chart', 'Graphic picture of the flow of documents and processing; shows weaknesses at a glance'],
    ], title='Methods of recording and evaluating internal control')
    itc = table(['Type', 'Meaning', 'Examples'], [
        ['General IT controls', 'Pervasive controls across many applications that support application controls', 'Data centre and network operations, program change, access security, system acquisition and development'],
        ['Application controls', 'Automated or manual controls at business-process level', 'Input edit checks, sequence checks, user limits, mandatory fields'],
        ['IT-dependent controls', 'Manual controls that rely on system-generated reports', 'Review of an exception report produced by the ERP'],
    ], title='Controls in an automated environment')

    concepts = [
        C('c1', T1, [
            'Audit risk means the chance of the auditor issuing a wrong opinion — typically a clean opinion — when the financial statements are materially misstated. SA 200 requires it to be reduced to an acceptably low level through sufficient appropriate evidence.',
            'Audit risk = risk of material misstatement (RMM) × detection risk. RMM, the risk that statements are materially misstated before audit, has two parts — inherent risk and control risk — both belonging to the entity.',
            'Detection risk is the only component the auditor controls; he lowers it by more extensive testing, bigger samples and experienced staff. It includes sampling risk (the sample is not representative) and non-sampling risk (wrong procedure or misreading evidence).',
            'RMM exists at two levels: the financial statements as a whole (pervasive — e.g. dominant management, weak governance, distress) needing overall responses such as more senior staff and unpredictability; and the assertion level (e.g. valuation of obsolete stock) needing specific further procedures.',
            'Audit risk does not include the auditor\'s business risks (litigation, bad publicity) or the risk of wrongly saying statements are misstated when they are not. Risk assessment is a matter of professional judgement.'],
          'Inherent risk is how slippery the road is, control risk is whether the car\'s brakes work, detection risk is whether the driver (auditor) notices the danger in time.',
          'After a fraud surfaces, regulators ask whether the auditor\'s procedures kept detection risk low enough for the assessed risks.',
          blocks=[comp]),
        C('c2', T2, [
            'SA 315 requires the auditor to identify and assess RMM, from fraud or error, at the statement and assertion levels through understanding the entity, its environment and its internal control — as the base for responses.',
            'The auditor identifies risks while understanding the entity, judges whether they are pervasive, links them to what can go wrong in assertions (considering controls to be tested), and considers likelihood and magnitude.',
            'Risk assessment procedures: (a) enquiries of management and others — internal audit, in-house legal counsel (litigation), sales and marketing staff (contract terms), risk management and IT staff; (b) analytical procedures, using financial and non-financial data, to spot unusual relationships; (c) observation and inspection of operations, documents, manuals, management reports, board minutes and premises.',
            'Risk assessment procedures alone do not give sufficient appropriate evidence for the opinion, though the information may be used as evidence and may double as tests of controls or substantive tests.'],
          'Risk assessment is the doctor\'s triage — questions, quick tests and a look around — before deciding which detailed tests to order.',
          'Comparing sales per square foot across stores can reveal a branch reporting implausible revenue.'),
        C('c3', T3, [
            'Under SA 320, misstatements (including omissions) are material if, individually or together, they could reasonably be expected to influence users\' economic decisions. Size and nature both matter — a small fraud can be material because it reveals a control failure.',
            'Materiality is used in planning (risk assessment, nature/timing/extent of procedures), during the audit and in evaluating uncorrected misstatements for the opinion. Items whose disclosure law requires (e.g. Schedule III disclosures) are material regardless of amount.',
            'Overall materiality: a percentage of a benchmark — often profit before tax from continuing operations (about 5% for a manufacturer); revenue, gross profit, expenses or equity when profit is volatile or the entity is not-for-profit (e.g. about 1% of revenue or expenses). One-off events may justify normalised profit.',
            'Performance materiality is set below overall materiality so that the total of uncorrected and undetected misstatements is unlikely to exceed overall materiality. Lower levels may be set for sensitive items (related party transactions, management remuneration, R&D in pharma).',
            'Materiality is revised when circumstances change, and the auditor documents overall, specific and performance materiality, the factors used and any revisions.'],
          'Materiality is the size of the hole in the auditor\'s sieve; performance materiality is a finer mesh used while sieving so that small stones don\'t add up to a big one.',
          'Audit files record the benchmark, percentage and reasoning used for materiality on every engagement.'),
        C('c4', T4, [
            'SA 315 requires understanding: (a) industry, regulatory and other external factors, including the reporting framework; (b) the nature of the entity — operations, ownership and governance, investments (including special-purpose entities), structure and financing; (c) selection and application of accounting policies and reasons for changes; (d) objectives, strategies and related business risks that may cause RMM; (e) measurement and review of financial performance (KPIs, budgets, ratings) — targets create pressure that can lead to misstatement.',
            'Business risk is broader than RMM; the auditor need not assess every business risk, only those with financial-statement consequences.',
            'Understanding the entity is a continuous process. It frames judgements on risk, materiality, accounting policies, related parties, going concern, analytical expectations and evaluating evidence.'],
          'You cannot judge whether a dish is cooked right without knowing what dish it is meant to be — the same with judging accounts without knowing the business.',
          'An auditor of an online seller focuses on revenue cut-off, returns and payment-gateway reconciliations because that is where its business risk lies.'),
        C('c5', T5, [
            'Internal control is a process that those charged with governance, management and other staff design, put in place and keep running, to give reasonable assurance about reliable financial reporting, effective and efficient operations, safeguarding of assets and compliance with laws.',
            'Understanding internal control helps the auditor identify possible misstatements, factors affecting RMM, and the nature, timing and extent of further procedures.',
            'Limitations: only reasonable assurance; human error and faulty judgement; staff not understanding a control\'s purpose; collusion and management override (e.g. side agreements with customers, disabling credit-limit checks); management choosing which controls to have; small entities lacking segregation of duties (though owner oversight may compensate, the owner can also override).'],
          'Internal control is the lock system of a house — useful, but a lock does not help if the keyholders conspire or the owner leaves the door open.',
          'Small family businesses often have one person ordering, receiving and paying — the auditor responds with more substantive testing.'),
        C('c6', T6, [
            'SA 315 groups internal control into five components (table).',
            'Control environment sets the tone at the top; the auditor checks whether management has a culture of honesty and whether the environment is a sound foundation. A good environment helps but is not an absolute deterrent to fraud, and by itself does not prevent or detect misstatement.',
            'Risk assessment process: does the entity identify, size, judge likelihood of and act on business risks relevant to reporting?',
            'Information system and communication: significant transaction classes, their flow to the ledger and statements, records used, capture of events, closing process and journal-entry controls; how roles are communicated.',
            'Control activities: performance reviews, information processing (arithmetical checks, program change controls), physical controls and segregation of duties (authorising, recording and custody kept apart). Monitoring: ongoing supervision and separate evaluations with remedial action.'],
          'The five components are like a body: values (environment), alertness (risk assessment), nervous system (information), muscles (control activities) and regular check-ups (monitoring).',
          'Auditors read board minutes and codes of conduct to assess the control environment, and walk through transactions to understand the information system.',
          blocks=[ic5]),
        C('c7', T7, [
            'A significant risk is an identified RMM that, in the auditor\'s judgement, needs special audit consideration — inherent risks with both higher likelihood and higher magnitude.',
            'Factors: fraud risk; recent significant economic, accounting or regulatory developments; complex transactions; significant related party transactions; high subjectivity or measurement uncertainty; significant unusual transactions outside the normal course of business.',
            'Always significant: RMM due to fraud and significant related party transactions outside the normal course of business.',
            'Non-routine transactions (more management and manual intervention, complex calculations, hard to control) and judgemental matters (estimates, fair values, differing interpretations) carry greater RMM.'],
          'Significant risks are the sharp bends on the route where the driver must slow down regardless of how good the brakes seem.',
          'A one-off sale of a factory to a promoter-controlled company would be treated as a significant risk.'),
        C('c8', T8, [
            'Reviewing internal control tells the auditor whether errors and frauds are likely to be caught, whether controls work as planned, whether internal audit is effective, whether assets are safeguarded, how reliable records are, where controls are weak or excessive, and how deep the testing must be; it also enables useful suggestions to management. The audit programme is framed only after this understanding.',
            'Methods to record and evaluate controls: narrative record, check list, internal control questionnaire (most widely used) and flow chart (table).',
            'For relevant controls, the auditor first evaluates design (can it prevent or detect material misstatement?) and then implementation (does it exist and is it used?) — by enquiry plus observation, inspection or walk-through; enquiry alone is not enough.',
            'Tests of controls gather evidence about operating effectiveness throughout the period: inspecting documents for authorisation, enquiry and observation where no trail exists, re-performance (e.g. bank reconciliation) and testing IT controls. Deviations (from staff changes, seasonal peaks, error) lead to specific enquiries and may raise control risk and the extent of substantive work.'],
          'Studying controls is reading the rule book; testing them is watching the match to see whether players actually follow the rules.',
          'An internal control questionnaire on purchases asks, for example, whether purchase orders are pre-numbered and whether stock records are kept by someone without custody of goods.',
          blocks=[methods]),
        C('c9', T9, [
            'SA 330: design overall responses for statement-level risks and further audit procedures whose nature, timing and extent respond to assertion-level risks; the higher the assessed risk, the more persuasive the evidence needed.',
            'Tests of controls are required when the auditor plans to rely on controls, or when substantive procedures alone cannot give enough evidence. Enquiry must be combined with other procedures; extent depends on frequency of the control, period of reliance, expected deviation rate and evidence from related controls.',
            'Timing: test for the period of intended reliance — point-in-time evidence suffices for, say, year-end stock count controls. Evidence from earlier audits may be reused only after confirming no significant change, considering the control environment, manual vs automated nature, IT general controls and deviations noted earlier.',
            'Misstatements found by substantive tests suggest controls failed; absence of misstatements does not prove controls worked. A material misstatement found by the auditor strongly indicates a significant deficiency.',
            'Whatever the risk assessment, substantive procedures are performed for every material class of transactions, balance and disclosure — tests of details (vouching transactions, verifying balances) and substantive analytical procedures (best for predictable relationships, e.g. rent from units × rate × occupancy).'],
          'Responses are like medicine dosage — the more serious the diagnosis (risk), the stronger the dose (evidence).',
          'When controls over credit sales fail, auditors increase debtor confirmations and cut-off testing.'),
        C('c10', T10, [
            'Internal financial controls (IFC) are policies and procedures for reliable reporting, efficient operations, compliance, safeguarding assets and prevention and detection of frauds.',
            'Companies Act, 2013: Section 134(5)(e) — directors of listed companies state that IFC are laid down, adequate and operating effectively; Section 143(3)(i) — the auditor reports on adequacy and operating effectiveness of IFC over financial reporting (not required for a private company that is a one person company or small company, or that has turnover below ₹50 crore and aggregate borrowings below ₹25 crore); Section 177(4)(vii) — the audit committee evaluates IFC and risk management; Section 149(8) with Schedule IV — independent directors satisfy themselves that financial controls are robust.',
            'Management is primarily responsible for IFC; the auditor evaluates and reports.',
            'Documentation of risks: team discussion and key decisions, key elements of the understanding of the entity and each control component with sources and procedures, the assessed risks at both levels, and risks with related controls understood.'],
          'IFC reporting is a three-way check: directors say "we have controls", the audit committee examines them, and the auditor reports whether they work.',
          'Large listed companies maintain risk-control matrices that both internal and statutory auditors test each year.'),
        C('c11', T11, [
            'In an automated environment, processing, accounting and even decisions run on IT systems (ERP or packaged software), giving speed, accuracy, volume and integration but new risks: inaccurate processing, unauthorised access, direct back-end data changes, excessive privileged access, and weak change management.',
            'Unaddressed IT risks mean the auditor cannot rely on system data or automated controls, so substantive testing increases and IFC reporting may be modified.',
            'Controls: general IT controls (pervasive) support application controls and IT-dependent manual controls (table).',
            'Testing methods: enquiry (efficient but weakest — never alone), observation, inspection and re-performance (strongest but slow); enquiry plus inspection is often the best balance. Walk through an end-to-end transaction and inspect configurations. Manual controls suit judgement areas; automated controls suit high-volume routine processing.',
            'Data analytics through CAATs (spreadsheets, IDEA, ACL) helps test completeness, select samples, recompute balances, re-perform calculations, analyse journal entries and investigate fraud. Control deficiencies found are reported to management, and significant ones in writing to those charged with governance.'],
          'General IT controls are the building\'s security guards and maintenance; application controls are the locks on individual rooms — locks are only as good as the guards.',
          'Auditors routinely extract the full journal-entry file from the ERP to test unusual postings like weekend entries by senior users.',
          blocks=[itc]),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Responding to a dominant promoter', 'role': 'Engagement manager',
         'situation': 'A client is run by one promoter with no internal audit, frequent accountant turnover and late reconciliations.',
         'steps': ['Recognise a pervasive, statement-level RMM.', 'Respond overall: senior staff, more scepticism, surprise procedures, closer review.', 'Reduce reliance on controls and expand substantive tests in revenue, expenses and related parties.'],
         'takeaway': 'Weak control environments call for overall responses, not just more vouching.'},
        {'id': 'j2', 'title': 'Setting materiality after a one-off loss', 'role': 'Audit senior',
         'situation': 'A plant fire slashed this year\'s profit.',
         'steps': ['Use normalised profit from past results and budget as the benchmark.', 'Set performance materiality below overall materiality.', 'Document the benchmark, percentage and reasons; revise if results change.'],
         'takeaway': 'Materiality is judgement anchored to the entity\'s normal performance.'},
    ]

    mcqs = [
        Q('m1', 'Audit risk is a function of:', ['Risk of material misstatement and detection risk', 'Business risk and inherent risk', 'Sampling risk and fee risk', 'Control risk only'], 0,
          'Audit risk combines the risk of material misstatement (inherent and control risk) with detection risk. Business risk is broader and not part of the model, and fee concerns are irrelevant. In practice: auditors lower detection risk when RMM is high to keep audit risk acceptable.', 'c1', T1),
        Q('m2', 'Which component of audit risk can the auditor directly influence?', ['Detection risk', 'Inherent risk', 'Control risk', 'Risk of material misstatement'], 0,
          'Inherent and control risk belong to the entity; the auditor can only change detection risk by altering the nature, timing and extent of his own procedures. In practice: larger samples and experienced staff reduce detection risk.', 'c1', T1),
        Q('m3', f'Acceptable audit risk 5%, inherent risk 80%, control risk 50%. The planned detection risk is:', [f'{dr}%', '2%', '20%', '4%'], 0,
          f'Detection risk = 0.05 ÷ (0.8 × 0.5) = {dr}%. The other figures misapply the formula; for example 2% wrongly multiplies all three risks together. In practice: a lower allowed detection risk means more substantive testing.', 'c1', T1, 'moderate', check=dr),
        Q('m4', 'A start-up operates in an industry where many businesses have recently failed. This mainly indicates:', ['Inherent risk', 'Control risk', 'Detection risk', 'Sampling risk'], 0,
          'Risks arising from the nature of the business and its environment, before considering controls, are inherent risks. Control risk relates to failure of the entity\'s controls, and detection risk to the auditor\'s procedures. In practice: going concern and valuation become focus areas.', 'c1', T1),
        Q('m5', 'Which is NOT a risk assessment procedure under SA 315?', ['External confirmation of all debtors as the sole procedure', 'Enquiries of management and others', 'Analytical procedures', 'Observation and inspection'], 0,
          'SA 315 lists enquiries, analytical procedures, and observation and inspection as risk assessment procedures. Confirming debtors is a substantive procedure performed in response to assessed risks. In practice: enquiries of in-house legal counsel reveal litigation risks.', 'c2', T2),
        Q('m6', 'Under SA 320, misstatements are material if they:', ['Could reasonably be expected to influence users\' economic decisions', 'Exceed ₹1 lakh in all cases', 'Are caused only by fraud', 'Relate only to the balance sheet'], 0,
          'Materiality is judged by whether misstatements, individually or in aggregate, could reasonably influence users\' economic decisions; both size and nature matter. There is no fixed rupee limit, and errors as well as fraud count. In practice: a small fraud can be material in nature.', 'c3', T3),
        Q('m7', 'Performance materiality is set:', ['Below overall materiality', 'Above overall materiality', 'Equal to profit before tax', 'Only at the reporting stage'], 0,
          'Performance materiality is set lower than overall materiality to reduce the chance that undetected and uncorrected misstatements together exceed overall materiality. It is used in planning and performing procedures. In practice: it is often a percentage of overall materiality.', 'c3', T3),
        Q('m8', 'When profit before tax is unusually low because of a one-time fire loss, the auditor may:', ['Use a normalised profit based on past results and budgets', 'Always use the current low profit', 'Skip materiality', 'Use the share price'], 0,
          'SA 320 allows adjusting the benchmark for exceptional events, using normalised profit from prior periods and budgets. Using the distorted figure would make materiality unrealistically low. In practice: the reasoning is documented in the audit file.', 'c3', T3, 'moderate'),
        Q('m9', 'Which is always a significant risk?', ['Risk of material misstatement due to fraud', 'Routine payroll processing', 'Small petty cash payments', 'Depreciation by a consistent method'], 0,
          'SA 315 treats fraud risks and significant related party transactions outside the normal course of business as significant risks. Routine, low-judgement items usually are not significant risks. In practice: significant risks require specific substantive procedures designed for them.', 'c7', T7),
        Q('m10', 'Segregation of duties is an example of which component of internal control?', ['Control activities', 'Control environment', 'Monitoring of controls', 'Risk assessment process'], 0,
          'Control activities include segregation of duties, performance reviews, information processing and physical controls. The control environment covers attitudes and governance; monitoring evaluates controls over time. In practice: the person approving payments should not record them.', 'c6', T6),
        Q('m11', 'Recruitment and training policies of an entity relate to:', ['Control environment — human resource policies', 'Control activities', 'Information system', 'Monitoring'], 0,
          'Human resource policies on hiring, training, evaluation and promotion are an element of the control environment that shows the entity\'s commitment to competent, trustworthy staff. They are not individual control activities. In practice: weak hiring checks raise risk of fraud.', 'c6', T6),
        Q('m12', 'A satisfactory control environment:', ['Helps reduce fraud risk but is not an absolute deterrent', 'Guarantees that no fraud can occur', 'Makes substantive procedures unnecessary', 'Replaces all control activities'], 0,
          'A strong control environment is a positive factor but cannot by itself prevent or detect misstatements and does not eliminate fraud risk. Substantive procedures are always required for material items. In practice: auditors still test journal entries for management override.', 'c6', T6),
        Q('m13', 'Which is a limitation of internal control?', ['Collusion among employees or management override', 'Segregation of duties', 'Regular monitoring', 'Pre-numbered documents'], 0,
          'Controls can be bypassed when two or more people collude or management overrides them; human error and cost-benefit choices are other limitations. The remaining options are features of good control. In practice: side agreements with customers can defeat revenue controls.', 'c5', T5),
        Q('m14', 'The most widely used method of collecting information on internal control is the:', ['Internal control questionnaire', 'Narrative record', 'Flow chart', 'Engagement letter'], 0,
          'The internal control questionnaire is comprehensive, reduces the chance of omissions and can be completed in sections or at an interim date. Narrative records suit small entities, and flow charts show document flows graphically. In practice: firms use standard questionnaires tailored to each client.', 'c8', T8),
        Q('m15', 'Re-performing a bank reconciliation prepared by the client is a:', ['Test of control', 'Risk assessment procedure only', 'Substantive analytical procedure', 'Management representation'], 0,
          'Re-performance means the auditor independently executes a control the entity performed, to check it operated properly — a test of control. Analytical procedures study relationships among data. In practice: re-performance gives strong evidence but takes time.', 'c8', T8),
        Q('m16', 'If substantive testing finds no misstatement, the auditor can conclude that:', ['Nothing about operating effectiveness of the related controls without testing them', 'The controls operated effectively all year', 'Control risk is nil', 'No further audit work is needed anywhere'], 0,
          'Absence of misstatements does not provide evidence that controls are effective; only tests of controls do. Conversely, misstatements found indicate controls may have failed. In practice: inspect approval evidence or system logs to test the control.', 'c9', T9, 'moderate'),
        Q('m17', 'Substantive procedures must be performed for:', ['Every material class of transactions, account balance and disclosure', 'Only high-risk areas', 'Only areas where controls failed', 'No area if controls are strong'], 0,
          'SA 330 requires substantive procedures for each material class of transactions, balance and disclosure regardless of assessed risk, because risk assessment is judgemental and controls have inherent limitations. In practice: even well-controlled revenue gets some substantive testing.', 'c9', T9),
        Q('m18', 'Under Section 143(3)(i), auditor reporting on internal financial controls is NOT required for a private company that:', ['Has turnover below ₹50 crore and aggregate borrowings below ₹25 crore', 'Is listed', 'Has turnover of ₹200 crore', 'Has borrowings of ₹100 crore'], 0,
          'The exemption applies to private companies that are one person or small companies, or whose turnover is below ₹50 crore and aggregate borrowings from banks, financial institutions or bodies corporate are below ₹25 crore. Listed and larger companies are covered. In practice: check both limits.', 'c10', T10, 'moderate'),
        Q('m19', 'Program change and access security controls are examples of:', ['General IT controls', 'Application controls', 'IT-dependent manual controls', 'Substantive procedures'], 0,
          'General IT controls are pervasive policies covering data centre operations, program changes, access security and system development; they support application controls. Edit checks and sequence checks are application controls. In practice: weak access controls undermine reliance on automated controls.', 'c11', T11),
        Q('m20', 'Which testing method gives the least audit evidence and should never be used alone?', ['Enquiry', 'Inspection', 'Re-performance', 'Observation combined with inspection'], 0,
          'Enquiry is efficient but provides the weakest evidence, so it must be combined with observation, inspection or re-performance. Re-performance gives the strongest evidence but is time-consuming. In practice: enquiry plus inspection is often the best balance.', 'c11', T11),
    ]

    questions = [
        W('q1', 5, 'Explain the components of audit risk with an example of each.',
          [comp, ul(['Inherent risk: high-value mobile phones in a retail store are easily stolen.', 'Control risk: the rule that two persons count cash daily is not followed.',
                     'Detection risk: the auditor\'s sample of sales misses fictitious year-end invoices.']),
           p('Audit risk = Inherent risk × Control risk × Detection risk; the auditor controls only detection risk.')],
          [S('s1', 'Inherent risk — meaning and example', 1.5, 'concept', 'inherent', 'before|nature|susceptib'),
           S('s2', 'Control risk — meaning and example', 1.5, 'concept', 'control risk', 'internal control|prevent|detect'),
           S('s3', 'Detection risk — meaning and example', 1.5, 'concept', 'detection', 'procedure|sample|auditor'),
           S('s4', 'Formula / auditor controls detection risk', 0.5, 'concept', 'only|influence|function|formula|product')],
          ['Give one crisp example per component.'], ['Saying the auditor can reduce inherent risk.'], ['Use a table plus examples.'], pad='table'),
        W('q2', 5, 'Describe the components of internal control as per SA 315.',
          [ic5],
          [S('s1', 'Control environment', 1, 'concept', 'control environment'),
           S('s2', 'Risk assessment process', 1, 'concept', 'risk assessment'),
           S('s3', 'Information system and communication', 1, 'concept', 'information system'),
           S('s4', 'Control activities', 1, 'concept', 'control activit'),
           S('s5', 'Monitoring of controls', 1, 'concept', 'monitoring')],
          ['Name and explain all five in one line each.'], ['Mixing limitations with components.'], ['Use a table.'], pad='table'),
        W('q3', 6, i2['q'], i2['solution'],
          [S('s1', 'Choice of normalised benchmark', 1.5, 'judgement', 'normalis|normaliz|one-time|one time|exceptional'),
           S('s2', 'Overall materiality', 1.5, 'computation', 'overall materiality|materiality', nums=[mat]),
           S('s3', 'Performance materiality', 1, 'computation', 'performance materiality', nums=[pm]),
           S('s4', 'Aggregate evaluation and nature', 2, 'conclusion', 'aggregate|together|total', nums=[agg])],
          ['Justify the benchmark before computing.'], ['Using the one-off depressed profit.'], ['Benchmark → materiality → performance materiality → evaluation.'], checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Define detection risk and its two kinds.',
          'Detection risk is the risk that the auditor\'s procedures will fail to detect a material misstatement. It includes sampling risk, where the sample is unrepresentative, and non-sampling risk, such as using an unsuitable procedure.',
          [P('p1', 'Procedures fail to detect material misstatement', 5, 'procedure', 'fail to detect|miss|will fail|could fail'), P('p2', 'Sampling risk', 3, 'sampling risk'), P('p3', 'Non-sampling risk', 2, 'non-sampling|non sampling')], 'c1'),
        V('v2', 'What is performance materiality and why is it needed?',
          'It is an amount set lower than overall materiality so that the total of uncorrected and undetected misstatements is unlikely to exceed overall materiality.',
          [P('p1', 'Lower than overall materiality', 5, 'lower|less|below'), P('p2', 'Aggregate of undetected/uncorrected misstatements', 5, 'undetected|uncorrected|aggregate|total')], 'c3'),
        V('v3', 'Name the five components of internal control.',
          'Control environment, the entity\'s risk assessment process, the information system and communication, control activities, and monitoring of controls.',
          [P('p1', 'Control environment', 2, 'environment'), P('p2', 'Risk assessment process', 2, 'risk assessment'), P('p3', 'Information system', 2, 'information'), P('p4', 'Control activities', 2, 'activit'), P('p5', 'Monitoring', 2, 'monitor')], 'c6'),
        V('v4', 'Which risks are always treated as significant risks?',
          'Risks of material misstatement due to fraud, and significant related party transactions outside the normal course of business.',
          [P('p1', 'Fraud risks', 5, 'fraud'), P('p2', 'Significant related party transactions outside normal course', 5, 'related party')], 'c7'),
        V('v5', 'Distinguish general IT controls from application controls.',
          'General IT controls are pervasive controls over many systems such as program change and access security, and they support application controls. Application controls work at the business process level, such as edit checks and sequence checks.',
          [P('p1', 'General IT controls — pervasive, e.g. access, program change', 5, 'general', 'pervasive|access|program change|many'), P('p2', 'Application controls — process level, e.g. edit checks', 5, 'application', 'process|edit|sequence|input')], 'c11'),
    ]

    cases = [{'id': 'k1', 'title': 'Year-end at Narmada Electronics Ltd.', 'difficulty': 'moderate',
              'case': 'Narmada Electronics Ltd. holds large stocks of fast-ageing components. Sales invoices above ₹10 lakh need electronic approval by the sales head. During testing the auditor finds several such invoices recorded without approval, one of ₹2.5 crore overstating revenue. The company\'s IT team has super-user access to change data directly in the ERP database.',
              'mcqs': [
                  M('k1a', 'The risk that obsolete components are carried above net realisable value relates mainly to the:', ['Valuation assertion — inherent risk', 'Occurrence assertion — detection risk', 'Rights assertion — control risk', 'Presentation — sampling risk'], 0,
                    'Fast-ageing stock is naturally prone to being overvalued, an inherent risk affecting the valuation assertion. The auditor responds with ageing analysis, comparison with net realisable value and review of post year-end sales. In practice: technology inventories are a common valuation risk.', 'core', topic=T1),
                  M('k1b', 'Unapproved high-value invoices and a material revenue misstatement indicate that:', ['The approval control did not operate effectively — a likely significant deficiency', 'Controls are effective', 'Only detection risk increased', 'No change to the audit approach is needed'], 0,
                    'When substantive tests find misstatements, that points to the controls not working as intended, and a material misstatement strongly indicates a significant deficiency. The auditor revises control risk and extends substantive work. In practice: such deficiencies are reported in writing to those charged with governance.', 'moderate', topic=T9),
                  M('k1c', 'Super-user access allowing direct database changes is a weakness in:', ['General IT controls — access security', 'Application input controls', 'Control environment only', 'Substantive analytical procedures'], 0,
                    'Access security is a general IT control; privileged users able to make back-end changes undermine the reliability of data and of automated controls. The auditor may need more substantive testing of system data. In practice: auditors review logs of privileged-user activity.', 'moderate', topic=T11),
                  M('k1d', 'Given these findings, the auditor should:', ['Reassess risks and expand substantive procedures, including journal-entry testing', 'Rely fully on the ERP reports', 'Reduce sample sizes', 'Stop testing controls and issue a clean report'], 0,
                    'SA 330 requires more persuasive evidence as assessed risk rises; failed controls and IT weaknesses call for larger substantive tests and journal-entry analysis. Relying on unverified system reports would be inappropriate. In practice: data analytics can test the full population of entries.', 'moderate', topic=T9),
              ]}]

    return unit(UID, 'p5', 'int-p5-ch03', 1, 'Risk Assessment and Internal Control',
                ['Explain audit risk and its components and apply the audit risk model.',
                 'Describe risk assessment procedures and understanding the entity under SA 315.',
                 'Determine materiality and performance materiality under SA 320.',
                 'Explain internal control, its components, limitations, evaluation methods and tests of controls.',
                 'Describe responses to assessed risks (SA 330), IFC reporting, and controls in an automated environment.'],
                {'difficulty': 'core', 'minutes': {'learn': 60, 'practice': 40}, 'prereq': ['int-p5-ch02-u01'],
                 'exam_tip': 'Very high weightage: identify the risk component in a case, materiality benchmarks, components of internal control, IFC exemptions and general IT vs application controls.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['AR = RMM × DR = IR × CR × DR; auditor controls only DR.', 'Risk assessment procedures: enquiry, analytics, observation and inspection.',
                             'Materiality: % of benchmark (≈5% PBT; ≈1% revenue for NPOs); performance materiality lower; revise and document.',
                             'Five components: environment, risk assessment, information, control activities, monitoring.', 'Always significant: fraud risk; significant unusual related party transactions.',
                             'Tests of controls: inspection, enquiry+observation, re-performance; enquiry alone never enough.', 'Substantive procedures for every material item.',
                             'IFC: s.134(5)(e), s.143(3)(i), s.177(4)(vii), s.149(8).', 'IT: general IT controls support application controls.'],
                 'remember': ['Absence of misstatement ≠ effective controls.', 'Statutory disclosures are material regardless of amount.'],
                 'traps': ['Business risk is not part of audit risk.', 'Inherent and control risk are the entity\'s risks.']},
                [('Audit risk model', 'AR = IR × CR × DR'), ('Materiality standard', 'SA 320'), ('Risk identification', 'SA 315'), ('Responses', 'SA 330'),
                 ('IFC auditor reporting', 'Sec. 143(3)(i)'), ('Weakest test', 'Enquiry (never alone)')],
                viva, cases,
                topics=['Audit Risk', 'Materiality', 'Understanding the Entity and its Environment', 'Internal Control', 'Risks that Require Special Audit Consideration',
                        'Evaluation of Internal Control System', 'Testing of Internal Control', 'The Auditor\'s Responses to Assessed Risks', 'Internal Financial Controls as per Regulatory Requirements',
                        'Documenting the Risks', 'Automated Environment', 'Data Analytics for Audit', 'Digital Audit', 'Assess and Report Audit Findings'])
