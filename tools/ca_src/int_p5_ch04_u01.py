"""CA Intermediate · Paper 5 Auditing and Ethics · Chapter 4 Audit Evidence.
Scope follows the ICAI study material (SA 500, 501, 505, 510, 520, 530, 550, 610); explanations, names and figures are original."""
from ikit import *

UID = 'int-p5-ch04-u01'
T1 = 'Audit evidence: sufficiency, appropriateness, sources (SA 500)'
T2 = 'Audit procedures and assertions'
T3 = 'Information produced by the entity, selecting items, management\'s expert'
T4 = 'Specific items: inventory, litigation, segments (SA 501)'
T5 = 'External confirmations (SA 505)'
T6 = 'Opening balances in initial engagements (SA 510)'
T7 = 'Analytical procedures (SA 520)'
T8 = 'Audit sampling (SA 530)'
T9 = 'Related parties (SA 550)'
T10 = 'Using the work of internal auditors (SA 610)'


def build():
    # i1 — projecting a sample misstatement
    ck = Checks()
    rate = ck.add('round(9000/180000*100,2)', 'Misstatement rate in the sample, %')
    proj = ck.add('round(9000/180000*4500000)', 'Projected misstatement in the population (ratio method)')
    i1 = {'id': 'i1', 'title': 'Projecting a misstatement found in a sample', 'difficulty': 'core', 'minutes': 6,
          'q': 'Auditing trade receivables of ₹45,00,000 at Varuna Distributors, CA Nisha tests a sample with book value ₹1,80,000 and finds overstatements of ₹9,000 (none of them an anomaly). Tolerable misstatement is ₹1,50,000. Project the misstatement and state her next step.',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['Misstatement rate', '9,000 ÷ 1,80,000', f'{rate}%'],
              ['Projected misstatement', '5% × 45,00,000', inr(proj)],
              ['Compare with tolerable misstatement', inr(proj) + ' vs ₹1,50,000', 'Projected exceeds tolerable']], title='Projection'),
              p('Because the projected misstatement exceeds tolerable misstatement, the sample does not give a reasonable basis to conclude on the population. She should discuss with management, ask them to investigate and correct the misstatements, and extend testing or perform additional procedures before concluding (SA 530, SA 450).')],
          'checks': list(ck)}

    # i2 — substantive analytical procedure on interest cost
    ck2 = Checks()
    exp_int = ck2.add('((4000000+6000000)/2)*0.10', 'Expected interest = average loan × rate')
    diff = ck2.add('560000-500000', 'Difference from recorded interest')
    i2 = {'id': 'i2', 'title': 'A substantive analytical procedure on interest', 'difficulty': 'core', 'minutes': 5,
          'q': 'Jhelum Tiles had a 10% term loan of ₹40,00,000 at the start of the year and ₹60,00,000 at the end (the increase was drawn evenly through the year). Recorded interest is ₹5,60,000. Develop an expectation and evaluate.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Expected interest', 'Average loan (40 + 60) ÷ 2 lakh × 10%', inr(exp_int)],
              ['Recorded interest', '', inr(560000)],
              ['Difference', '', inr(diff)]], title='Reasonableness test'),
              p('A 12% gap is significant if it exceeds the amount the auditor can accept without further investigation. She would ask management (e.g. penal interest, other loans, misposting), then corroborate the answer with loan statements and the bank\'s interest certificate before concluding (SA 520).')],
          'checks': list(ck2)}

    rel = table(['Generalisation (subject to exceptions)', 'More reliable', 'Less reliable'], [
        ['Source', 'Independent external sources', 'Internal records'],
        ['Controls', 'Internal evidence where controls are effective', 'Where controls are weak'],
        ['How obtained', 'Directly by the auditor (observation of a control)', 'Indirectly or by inference (inquiry about a control)'],
        ['Form', 'Documents (paper or electronic), contemporaneous minutes', 'Later oral representations'],
        ['Copy', 'Original documents', 'Photocopies, faxes, digitised copies']], title='Reliability of audit evidence (SA 500)')
    asr = table(['Classes of transactions and events', 'Account balances'], [
        ['Occurrence — transactions happened and relate to the entity', 'Existence — assets, liabilities and equity exist'],
        ['Completeness — all transactions recorded', 'Rights and obligations — entity holds or controls the assets; liabilities are its obligations'],
        ['Accuracy — amounts and data recorded correctly', 'Completeness — all balances recorded'],
        ['Cut-off — recorded in the correct period', 'Accuracy, valuation and allocation — at appropriate amounts'],
        ['Classification — recorded in the proper accounts', 'Classification — in the proper accounts'],
        ['Presentation — appropriately aggregated and disclosed', 'Presentation — appropriately aggregated and disclosed']], title='Assertions')
    proc = table(['Procedure', 'Example'], [
        ['Inspection', 'Examining a title deed or a purchase invoice; physically examining a machine'],
        ['Observation', 'Watching the inventory count'],
        ['External confirmation', 'Bank or debtor confirmation received directly by the auditor'],
        ['Recalculation', 'Re-computing depreciation'],
        ['Reperformance', 'Independently re-running a bank reconciliation'],
        ['Analytical procedures', 'Comparing gross margin across months'],
        ['Inquiry', 'Asking management about slow-moving stock — never sufficient alone']], title='Audit procedures')
    conf = table(['Point', 'Positive request', 'Negative request'], [
        ['Reply', 'In all cases — agree or give details', 'Only if the confirming party disagrees'],
        ['Evidence', 'Stronger', 'Weaker; no reply does not prove the balance'],
        ['Use alone', 'Normal choice', 'Only if: risk of material misstatement assessed low with controls tested; large number of small, similar balances; very low exception rate expected; and no reason to think recipients will ignore requests']],
        title='Positive and negative confirmations (SA 505)')

    concepts = [
        C('c1', T1, [
            'Audit evidence is information used by the auditor to reach conclusions on which the opinion rests; it includes accounting records and other information.',
            'Sufficiency is the quantity of evidence (more needed where risk is higher, less where quality is higher); appropriateness is its quality — relevance (logical link to the assertion) and reliability (source, nature, circumstances).',
            'Sources: the entity\'s records and other sources inside or outside the entity, the auditor\'s own procedures, and prior audits (with checks for changes).'],
          'Evidence is judged like witnesses: how many, how independent, and how closely they saw what happened.',
          'A bank confirmation received directly by the auditor beats a photocopied bank statement from the client.',
          blocks=[rel]),
        C('c2', T2, [
            'Procedures are used for three purposes: assessing risk, testing controls, and substantive testing (tests of details and substantive analytical procedures).',
            'Assertions are management\'s claims embedded in the financial statements; the auditor designs procedures for each relevant assertion (table).',
            'Nature and timing of procedures may be affected by when information is available (e.g. electronic data overwritten), and an audit trail allows tracing from source document to statements and back.'],
          'Every figure in the accounts makes silent promises; assertions name them so the auditor can test each one.',
          'Physical verification tests existence of stock but not ownership — rights need documents.',
          blocks=[asr, proc]),
        C('c3', T3, [
            'Information produced by the entity must be checked for accuracy and completeness and be precise and detailed enough for the auditor\'s purpose.',
            'Ways of selecting items: all items (100% — small populations of large items, or automated recalculation), specific items (high value, key or unusual items, items for information), or audit sampling.',
            'Using management\'s expert: evaluate the expert\'s competence, capabilities and objectivity; understand their work; and evaluate its appropriateness as evidence.',
            'If evidence from one source is inconsistent with another, or doubts arise about reliability, the auditor modifies or adds procedures and considers the effect on other aspects of the audit.'],
          'Even the client\'s own reports must be audited before they can be relied on.',
          'A system-generated ageing report is tested for completeness before it supports the bad-debt provision.'),
        C('c4', T4, [
            'Inventory (SA 501): if material, attend the physical count (unless impracticable) to evaluate management\'s instructions, observe procedures, inspect inventory and perform test counts; then test the final records.',
            'If the count is on another date, perform procedures to confirm changes between that date and the year-end. If unable to attend due to unforeseen circumstances, count on an alternative date. If attendance is impracticable, perform alternative procedures; if none work, modify the opinion.',
            'Inventory held by third parties: obtain confirmation of quantities and condition, or inspect/perform other procedures.',
            'Litigation and claims: inquiry, minutes of meetings, legal expense accounts; if a risk is identified, write directly to the company\'s outside lawyers through a letter prepared by management and sent by the auditor. If management refuses permission, or counsel refuses to respond, and no alternative evidence exists, modify the opinion.',
            'Segment information: understand how management determines segments and test the methods.'],
          'For inventory, the auditor goes to see; for litigation, the auditor asks the lawyers.',
          'If a warehouse is flooded on count day, the auditor attends a recount soon after and rolls back to year-end.'),
        C('c5', T5, [
            'An external confirmation is evidence in the form of a written reply sent straight to the auditor by an outside party, on paper or electronically.',
            'The auditor controls the process: decides information to confirm, selects the confirming party, designs and sends requests and follows up non-responses.',
            'Positive versus negative requests (table). For non-responses, perform alternative procedures (e.g. subsequent receipts, shipping documents).',
            'If management refuses to let the auditor send a request: inquire about the reasons and seek evidence of their validity, evaluate implications for risks including fraud, and perform alternative procedures. If the refusal is unreasonable or alternatives fail, communicate with those charged with governance (SA 260) and consider the opinion (SA 705).'],
          'A confirmation is the third party talking straight to the auditor, with the client kept out of the line.',
          'Replies sent to the client\'s office and then forwarded are less reliable than those sent directly to the auditor.',
          blocks=[conf]),
        C('c6', T6, [
            'Opening balances are account balances at the start of the period, including disclosures of contingencies and commitments; SA 510 applies in initial audit engagements.',
            'Procedures: check prior period closing balances are correctly brought forward (or restated); check appropriate accounting policies are applied consistently; review the predecessor auditor\'s working papers where possible; evaluate whether current-period procedures give evidence (e.g. later receipts for opening debtors); perform specific procedures where needed (e.g. for non-current assets, examine records underlying the opening balances).',
            'Reporting: no sufficient evidence → qualified or disclaimer; material misstatement not properly dealt with → qualified or adverse; policies not consistently applied or change not properly accounted → qualified or adverse; predecessor\'s modification still relevant → modify the current opinion.'],
          'A new auditor must make sure the year started on solid ground.',
          'Collection of opening receivables in April helps prove them without asking the old auditor.'),
        C('c7', T7, [
            'Analytical procedures evaluate financial information by analysing plausible relationships among financial and non-financial data, and investigate fluctuations that are inconsistent or differ from expectations.',
            'They are used in planning (SA 315), may be used as substantive procedures, and must be used near the end of the audit to form an overall conclusion on whether the statements are consistent with the auditor\'s understanding.',
            'For substantive analytical procedures: assess suitability for the assertion, evaluate reliability of data (source, comparability, nature, controls), develop a precise expectation, and set the acceptable difference.',
            'Techniques: trend analysis, ratio analysis, reasonableness tests and structural modelling. Investigate differences by inquiry of management and corroborating the replies.'],
          'Analytical procedures ask: does this number make sense given everything we know?',
          'A sudden rise in wages without more workers or rate changes may signal ghost employees.'),
        C('c8', T8, [
            'Audit sampling applies procedures to less than 100% of a population so that every sampling unit has a chance of selection, giving a basis for conclusions on the whole population.',
            'Approaches: statistical (random selection and probability theory to evaluate results) or non-statistical (judgment).',
            'Sampling risk: for tests of controls — concluding controls are more effective than they are (affects effectiveness) or less effective (affects efficiency); for tests of details — concluding no material misstatement exists when it does, or that it exists when it does not. Non-sampling risk arises from other causes, like wrong procedures or misreading evidence.',
            'Design considers purpose, population (appropriate and complete), stratification and value-weighted selection; sample size rises with risk and lower tolerable misstatement or deviation rate.',
            'Selection methods: random, systematic, monetary unit sampling, haphazard; block selection is rarely appropriate.',
            'Evaluate: investigate the nature and cause of deviations, treat genuine anomalies separately, project misstatements to the population and compare with tolerable misstatement.'],
          'A sample is a window, not the whole room — it must be representative and its findings scaled up.',
          'Under monetary unit sampling, a ₹5 lakh invoice is far more likely to be picked than a ₹500 one.'),
        C('c9', T9, [
            'Related parties may be defined by the applicable framework; where the framework sets minimal requirements, SA 550 treats as related a person or entity with control or significant influence, or under common control or influence, and entities under dominant influence of key management.',
            'Many related party transactions are normal, but the relationship can create higher risk: complex structures, information systems that do not identify such transactions, and transactions not at arm\'s length.',
            'The auditor understands the relationships and transactions, inquires of management, remains alert when inspecting records (minutes, contracts, bank confirmations), and evaluates identification, accounting and disclosure.'],
          'Related parties can bend the normal rules of give and take, so the auditor looks harder.',
          'A large sale to a director\'s company near year-end needs scrutiny of terms and substance.'),
        C('c10', T10, [
            'The internal audit function performs assurance and consulting activities on governance, risk management and internal control.',
            'The opinion remains the external auditor\'s sole responsibility; relying on internal audit does not reduce it.',
            'Before relying on internal audit: evaluate the function\'s objectivity (organisational status, policies), the competence of its staff, and whether it applies a systematic and disciplined approach including quality control. Do not use the work if any of these is lacking.',
            'Use less of the work, and do more directly, where significant judgments are involved, risks are higher, or objectivity and competence are weaker. Reperform some of the work used.',
            'Direct assistance by internal auditors, where not prohibited by law or regulation, must be under the external auditor\'s direction, supervision and review.'],
          'The external auditor may borrow the internal auditor\'s tools, but signs the report alone.',
          'An internal audit team reporting to the CFO whose bonus depends on results has weak objectivity.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Inventory count attendance', 'role': 'Audit assistant',
         'situation': 'You attend the client\'s year-end stock count at two warehouses.',
         'steps': ['Review count instructions before the day.', 'Observe teams and cut-off at receiving and dispatch.', 'Do test counts both ways (floor to sheet, sheet to floor).', 'Note damaged and slow-moving items; trace counts to final records later.'],
         'takeaway': 'Test both existence and completeness during the count.'},
        {'id': 'j2', 'title': 'Debtor confirmations', 'role': 'Audit senior',
         'situation': 'Management refuses confirmation to one large customer.',
         'steps': ['Ask for reasons and evidence (e.g. a legal dispute).', 'Assess fraud risk implications.', 'Perform alternatives: post year-end receipts, contracts, delivery notes.', 'If unreasonable or no alternatives, inform those charged with governance and consider the opinion.'],
         'takeaway': 'A refusal is itself evidence to evaluate.'},
    ]

    mcqs = [
        Q('m1', 'Sufficiency of audit evidence refers to its:', ['Quantity', 'Relevance', 'Reliability', 'Source'], 0,
          'Sufficiency measures how much evidence is obtained; appropriateness measures its quality through relevance and reliability. The quantity needed rises with assessed risk and falls as quality improves. In practice: more weak evidence cannot fully replace good evidence.', 'c1', T1),
        Q('m2', 'Which audit evidence is generally the most reliable?', ['A confirmation received directly by the auditor from the bank', 'A photocopy of the bank statement provided by the client', 'An oral explanation by the accountant', 'An internal memo prepared after year-end'], 0,
          'Evidence from an independent external source obtained directly by the auditor ranks highest. Photocopies, oral explanations and internal documents prepared later are less reliable. In practice: send and receive confirmations yourself.', 'c1', T1),
        Q('m3', 'Physical verification of a machine mainly provides evidence of:', ['Existence', 'Rights and obligations', 'Valuation', 'Completeness'], 0,
          'Seeing an asset proves it exists, but not that the entity owns it or that it is correctly valued; ownership needs title documents and valuation needs cost and depreciation checks. In practice: pair inspection with document checks.', 'c2', T2),
        Q('m4', 'Recording a sale made on 2 April in the year ending 31 March relates to the assertion of:', ['Cut-off', 'Existence', 'Rights and obligations', 'Classification'], 0,
          'Cut-off concerns recording transactions in the correct accounting period. A sale on 2 April belongs to the next year. Occurrence and existence concern whether things happened or exist. In practice: test invoices and dispatch notes around year-end.', 'c2', T2),
        Q('m5', 'Inquiry alone is:', ['Not sufficient to provide evidence of operating effectiveness of controls or absence of material misstatement', 'Always sufficient', 'Sufficient for cash balances', 'More reliable than inspection'], 0,
          'Inquiry is useful but must be combined with other procedures such as inspection, observation or reperformance; on its own it does not give sufficient appropriate evidence. In practice: corroborate every important answer.', 'c2', T2),
        Q('m6', 'If attendance at the physical inventory count is impracticable, the auditor shall:', ['Perform alternative audit procedures; if not possible, modify the opinion', 'Issue an unmodified opinion', 'Rely on management representations only', 'Resign immediately'], 0,
          'SA 501 requires alternative procedures, such as inspecting documentation of subsequent sales of specific items, to obtain evidence about existence and condition. If that is not possible, the auditor modifies the opinion as per SA 705. In practice: impracticability is not mere inconvenience.', 'c4', T4, 'moderate'),
        Q('m7', 'A letter of inquiry to the entity\'s external legal counsel is:', ['Prepared by management and sent by the auditor', 'Prepared and sent by management', 'Sent by the lawyer to the client', 'Not used in an audit'], 0,
          'SA 501 requires direct communication: management prepares the letter, and the auditor sends it, with the reply going straight to the auditor. If management refuses, the opinion may need modification. In practice: track replies closely.', 'c4', T4, 'moderate'),
        Q('m8', 'A negative confirmation request asks the confirming party to respond:', ['Only if they disagree with the information', 'In all cases', 'Only if they agree', 'Only by e-mail'], 0,
          'Negative requests seek a reply only on disagreement, so non-replies give weaker evidence; positive requests require a reply in all cases. Negative requests alone are acceptable only under strict conditions. In practice: combine them with other procedures.', 'c5', T5),
        Q('m9', 'If management\'s refusal to allow a confirmation request is unreasonable, the auditor shall:', ['Communicate with those charged with governance and determine implications for the opinion', 'Ignore the account', 'Send the request anyway without telling management', 'Accept management\'s balance'], 0,
          'SA 505 requires the auditor to inquire into reasons, evaluate them, and if unreasonable or alternative procedures fail, communicate with those charged with governance (SA 260) and consider the effect on the opinion (SA 705). In practice: document the refusal.', 'c5', T5, 'moderate'),
        Q('m10', 'In an initial engagement, the auditor cannot obtain sufficient evidence on opening balances. The opinion should be:', ['Qualified or disclaimer', 'Adverse', 'Unmodified with emphasis of matter', 'Unmodified'], 0,
          'SA 510 calls for either qualifying the opinion or disclaiming one, depending on pervasiveness, where sufficient appropriate evidence on opening balances is not available. An adverse opinion is for material, pervasive misstatement. In practice: early planning avoids this.', 'c6', T6),
        Q('m11', 'Analytical procedures are MANDATORY under SA 520:', ['Near the end of the audit to form an overall conclusion', 'Only as substantive procedures', 'Only in initial audits', 'Never'], 0,
          'SA 520 requires analytical procedures near the end of the audit to assess whether the statements are consistent with the auditor\'s understanding; their use as substantive procedures is a choice. Risk assessment use is required by SA 315. In practice: final analytical review catches overlooked issues.', 'c7', T7),
        Q('m12', 'Comparing this year\'s salary expense with several earlier years is an example of:', ['Trend analysis', 'Recalculation', 'External confirmation', 'Observation'], 0,
          'Trend analysis compares current figures with prior periods to spot unusual movements, such as a jump in salaries without more staff. Recalculation checks arithmetic; confirmation and observation are other procedures. In practice: investigate unexplained spikes.', 'c7', T7),
        Q('m13', 'In tests of controls, concluding that controls are more effective than they actually are affects audit:', ['Effectiveness', 'Efficiency only', 'Neither', 'Materiality'], 0,
          'This sampling risk may lead the auditor to rely wrongly on controls and do too little substantive work, so an inappropriate opinion could result — it affects effectiveness. Concluding controls are less effective only causes extra work (efficiency). In practice: guard against over-reliance.', 'c8', T8, 'moderate'),
        Q('m14', 'Under monetary unit sampling, the sampling unit is:', ['Each rupee in the population', 'Each invoice', 'Each customer', 'Each page of the ledger'], 0,
          'MUS treats every monetary unit as a sampling unit, so larger items have a higher chance of selection — a value-weighted approach suited to overstatement testing. Invoices and customers are physical units. In practice: very small items may never be selected.', 'c8', T8),
        Q('m15', 'Sample misstatement ₹4,000 in items worth ₹80,000; population ₹20,00,000. Projected misstatement is:', ['₹1,00,000', '₹4,000', '₹40,000', '₹80,000'], 0,
          'Misstatement rate = 4,000 ÷ 80,000 = 5%; projected = 5% × 20,00,000 = ₹1,00,000. The projection, not the sample figure, is compared with tolerable misstatement. In practice: exclude proven anomalies before projecting.', 'c8', T8, 'core', check=100000),
        Q('m16', 'Before relying on internal audit, the statutory auditor must evaluate the function\'s:', ['Objectivity, competence and systematic and disciplined approach', 'Size and cost', 'Reporting line to the auditor', 'Number of reports issued'], 0,
          'SA 610 requires evaluating whether the function\'s status and policies support objectivity, whether it is competent, and whether it applies a systematic and disciplined approach including quality control. Without these, its work cannot be used. In practice: document the evaluation.', 'c10', T10),
        Q('m17', 'Responsibility for the audit opinion when the internal auditor\'s work is used rests with:', ['The external auditor alone', 'The internal auditor', 'Both jointly', 'Management'], 0,
          'The external auditor has sole responsibility for the opinion expressed, and relying on internal audit, or on direct help from internal auditors, does not reduce it. In practice: reperform part of the work used.', 'c10', T10),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Projection', 2, 'computation', 'project', nums=[proj]),
           S('s2', 'Compare with tolerable', 1, 'concept', 'tolerable'),
           S('s3', 'Next steps', 1, 'concept', 'management|additional|extend')],
          ['Project before concluding.'], ['Comparing the sample misstatement directly with tolerable misstatement.'], ['Table + conclusion.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Expectation', 2, 'computation', 'average|expect', nums=[exp_int]),
           S('s2', 'Difference', 1, 'computation', 'difference', nums=[diff]),
           S('s3', 'Investigate and corroborate', 1, 'concept', 'inquir|corroborat|certificate')],
          ['Use average balance.'], ['Accepting management\'s explanation without evidence.'], ['Table + note.'], pad='table', checks=list(ck2)),
        W('q3', 5, 'CA Rohan is appointed auditor of Gomti Ltd. for the first time. Explain the procedures he should perform on opening balances and the reporting consequences if problems arise.',
          [ul(['Check that prior period closing balances are correctly carried forward or restated.', 'Check that appropriate accounting policies are applied consistently.', 'Review the predecessor auditor\'s working papers where possible.', 'Use current-period evidence, e.g. collections of opening receivables and payment of opening payables.', 'Perform specific procedures, such as examining records underlying opening non-current assets.']),
           p('Reporting (SA 510 with SA 705): no sufficient evidence — qualified opinion or disclaimer; material misstatement not properly accounted or disclosed — qualified or adverse; inconsistent policies — qualified or adverse; a predecessor\'s modification still relevant — modify the current opinion.')],
          [S('s1', 'Carried forward', 1, 'concept', 'carried forward|brought forward'),
           S('s2', 'Policies', 0.75, 'concept', 'polic'),
           S('s3', 'Predecessor papers', 0.75, 'concept', 'predecessor'),
           S('s4', 'Current-period evidence', 0.75, 'concept', 'collection|current'),
           S('s5', 'Reporting', 1.75, 'concept', 'qualified', 'disclaimer|adverse')],
          ['Procedures then reporting.'], ['Forgetting the reporting consequences.'], ['List + paragraph.']),
        W('q4', 4, 'Distinguish positive and negative confirmation requests and state when negative requests may be the sole substantive procedure.',
          [conf],
          [S('s1', 'Positive', 1, 'concept', 'all cases|positive'),
           S('s2', 'Negative', 1, 'concept', 'disagree|negative'),
           S('s3', 'Conditions', 2, 'concept', 'low', 'small|homogeneous|similar', 'exception', n=2)],
          ['Use a table.'], ['Missing the four conditions.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What two qualities make audit evidence appropriate?',
          'Relevance to the assertion being tested and reliability, which depends on the source, nature and circumstances of the evidence.',
          [P('p1', 'Relevance', 5, 'relevan'), P('p2', 'Reliability', 5, 'reliab')], 'c1'),
        V('v2', 'When must the auditor attend the physical inventory count?',
          'When inventory is material to the financial statements, unless attendance is impracticable, in which case alternative procedures are performed.',
          [P('p1', 'When material', 6, 'material'), P('p2', 'Unless impracticable', 4, 'impracticable|alternative')], 'c4'),
        V('v3', 'Name three methods of selecting a sample.',
          'Random selection, systematic selection and monetary unit sampling; haphazard selection is also used, while block selection is rarely appropriate.',
          [P('p1', 'Random', 3, 'random'), P('p2', 'Systematic', 3, 'systematic'), P('p3', 'MUS or haphazard', 4, 'monetary|haphazard')], 'c8'),
        V('v4', 'What is an anomaly in audit sampling?',
          'An error or deviation that is shown to be a one-off, not representative of errors in the rest of the population.',
          [P('p1', 'Not representative', 7, 'not representative'), P('p2', 'Of population', 3, 'population')], 'c8'),
        V('v5', 'Who is responsible for the audit opinion when internal audit work is used?',
          'The external auditor alone; relying on internal audit does not dilute that responsibility.',
          [P('p1', 'External auditor alone', 7, 'external auditor|sole'), P('p2', 'Not reduced', 3, 'not reduced|not shared|alone')], 'c10'),
    ]

    cases = [{'id': 'k1', 'title': 'Narmada Retail audit', 'difficulty': 'moderate',
              'case': 'Narmada Retail Ltd. holds material stock at 40 stores. The new auditor, CA Kavya, takes over from a predecessor. Management refuses to let her confirm the balance of its largest supplier, citing a pending dispute. Debtors are thousands of small balances, and controls over sales have been tested and found effective.',
              'mcqs': [
                  M('k1a', 'For the 40 stores, the most appropriate approach is to:', ['Attend counts at selected stores based on risk and test the overall records', 'Rely only on management\'s count sheets', 'Visit no store as it is impracticable', 'Count every item herself'], 0,
                    'Where inventory is at many locations, the auditor plans attendance at locations selected on materiality and risk, observes procedures and test counts, and tests the final inventory records. Relying solely on management\'s sheets gives weak evidence. In practice: rotate locations each year.', 'moderate', topic=T4),
                  M('k1b', 'Regarding the supplier confirmation refused by management, Kavya should first:', ['Inquire about the reasons and seek evidence of their validity', 'Issue an adverse opinion', 'Send the request secretly', 'Ignore the supplier balance'], 0,
                    'SA 505 requires her to inquire into management\'s reasons, seek evidence for them, evaluate the implications for risk, and perform alternative procedures. Escalation to governance and opinion effects come only if the refusal is unreasonable or alternatives fail. In practice: a pending dispute may be a valid reason.', 'moderate', topic=T5),
                  M('k1c', 'Negative confirmations alone may be suitable for her debtors because:', ['Balances are many, small and similar, and controls are effective with low expected exceptions', 'Debtors are large in value', 'Management prefers it', 'Positive requests are banned'], 0,
                    'SA 505 allows negative confirmations as the sole substantive procedure only when risk is low with tested controls, the population has many small homogeneous balances, a low exception rate is expected, and recipients are not expected to ignore requests. Her facts largely fit these conditions. In practice: still consider fraud risk.', 'hard', topic=T5),
                  M('k1d', 'For opening balances, a useful procedure is to:', ['Review the predecessor auditor\'s working papers', 'Ignore them since the predecessor audited them', 'Rely only on the prior audit report', 'Issue a disclaimer automatically'], 0,
                    'SA 510 lets the incoming auditor review the predecessor\'s working papers, alongside checking balances carried forward and policy consistency, to gain evidence on opening balances. The prior report alone is not enough. In practice: ask management to request access early.', 'core', topic=T6),
              ]}]

    return unit(UID, 'p5', 'int-p5-ch04', 1, 'Audit Evidence',
                ['Explain sufficiency and appropriateness of audit evidence, audit procedures and assertions (SA 500).',
                 'Apply SA 501 to inventory, litigation and segment information.',
                 'Design and evaluate external confirmations (SA 505) and audit opening balances (SA 510).',
                 'Use analytical procedures (SA 520) and audit sampling (SA 530).',
                 'Address related parties (SA 550) and use the work of internal auditors (SA 610).'],
                {'difficulty': 'hard', 'minutes': {'learn': 80, 'practice': 50}, 'prereq': ['int-p5-ch03-u01'],
                 'exam_tip': 'Case-based questions dominate: identify the SA, state the requirement, and give the reporting consequence. Learn the conditions for negative confirmations and the SA 510 reporting rules.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Evidence: sufficient (quantity) and appropriate (relevance + reliability).', 'Procedures: inspection, observation, confirmation, recalculation, reperformance, analytics, inquiry.',
                             'Assertions for transactions and balances.', 'SA 501: count attendance; legal counsel letter; segments.', 'SA 505: positive vs negative; management refusal steps.',
                             'SA 510: opening balances procedures and reporting.', 'SA 520: mandatory at the end; techniques: trend, ratio, reasonableness, modelling.',
                             'SA 530: sampling risk, selection methods, projection.', 'SA 550: related party risks; SA 610: evaluate IA, sole responsibility stays.'],
                 'remember': ['Inquiry alone is never sufficient.', 'Negative confirmations need all four conditions.'],
                 'traps': ['Inspection proves existence, not ownership.', 'Using IA work never shares responsibility.']},
                [('SA 500', 'Audit evidence'), ('SA 501', 'Specific items'), ('SA 505', 'External confirmations'), ('SA 510', 'Opening balances'),
                 ('SA 520', 'Analytical procedures'), ('SA 530', 'Sampling'), ('SA 550', 'Related parties'), ('SA 610', 'Internal auditors')],
                viva, cases,
                topics=['Audit Evidence', 'Audit Evidence - Specific Considerations for Selected Items', 'External Confirmations', 'Initial Audit Engagements - Opening Balances',
                        'Analytical Procedures', 'Audit Sampling', 'Related Parties', 'Using the Work of Internal Auditors'])
