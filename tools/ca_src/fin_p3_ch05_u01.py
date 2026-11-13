"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 5 Audit Evidence.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch05-u01'
T1 = 'Sufficient appropriate evidence (SA 500) and specific items (SA 501)'
T2 = 'External confirmations (SA 505)'
T3 = 'Initial engagements and opening balances (SA 510)'
T4 = 'Audit sampling (SA 530)'
T5 = 'Related parties (SA 550)'


def build():
    ck = Checks()
    rate = ck.add('0.4/10', 'Misstatement rate in sample')
    proj = ck.add('0.4/10*200', 'Projected misstatement in population (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Projecting sample misstatements', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Sales invoices total ₹200 lakh. The auditor tests a sample of invoices worth ₹10 lakh and finds overstatements of ₹0.4 lakh. Tolerable misstatement for sales is ₹10 lakh. Project the misstatement using the ratio method and conclude.',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['Misstatement rate', '0.4 ÷ 10', inr(rate)],
              ['Projected misstatement', '4% × 200', '₹' + inr(proj) + ' lakh'],
              ['Comparison', '8 vs tolerable 10', 'Below but close — consider sampling risk'],
              ['Action', 'Extend testing or ask management to investigate and correct', '—']], title='SA 530 projection')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Confirmation problems', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Handle each: (a) management refuses to let the auditor confirm a major customer; (b) a positive confirmation is not returned; (c) a reply comes from a personal email address; (d) a customer reports a lower balance due to goods returned at year end.',
          'solution': [table(['Situation', 'Response under SA 505'], [
              ['(a)', 'Enquire about reasons, assess effect on fraud risk, perform alternative procedures; if unreasonable, communicate with TCWG and consider opinion'],
              ['(b)', 'Perform alternative procedures — subsequent receipts, shipping documents, invoices'],
              ['(c)', 'Doubt reliability; verify the source directly'],
              ['(d)', 'Exception — investigate; may indicate cut-off error or misstatement']], title='External confirmations')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Audit evidence must be sufficient (quantity) and appropriate (quality: relevance and reliability). Reliability increases when evidence comes from independent external sources, when controls are effective, when obtained directly by the auditor, when documentary, and when original.',
            'Audit procedures: inspection, observation, external confirmation, recalculation, reperformance, analytical procedures and enquiry. Information produced by the entity must be tested for accuracy and completeness.',
            'SA 501 specifics: attend physical inventory counting when material (observe, inspect, test counts); for litigation and claims, enquire, review minutes and legal expenses, and communicate with external legal counsel where risks exist; for segment information, evaluate methods and disclosures.'],
          'Better evidence is external, direct, documentary and original.',
          'An auditor attends the stock count rather than relying on management\'s count sheets.'),
        C('c2', T2, [
            'External confirmations are direct written responses from third parties (banks, customers, suppliers, lawyers). The auditor controls the requests: selecting parties, designing and sending requests, and receiving replies directly.',
            'Positive confirmations ask for a reply in every case; negative confirmations ask for a reply only if the recipient disagrees — used only when risk is low, controls effective, population large and homogeneous, and low exception rates are expected.',
            'If management refuses to allow confirmations, the auditor enquires into reasons, evaluates implications, and performs alternative procedures; unreasonable refusal may lead to communication with TCWG and a modified opinion. Non-responses require alternative procedures; exceptions are investigated.'],
          'The auditor, not the client, controls confirmations.',
          'A missing bank confirmation is a red flag that needs follow-up.'),
        C('c3', T3, [
            'In an initial audit engagement, the auditor obtains sufficient evidence that opening balances do not contain misstatements that materially affect current statements, and that accounting policies are applied consistently.',
            'Procedures: read the prior period statements and predecessor\'s report; review predecessor\'s working papers; evaluate whether current procedures provide evidence on opening balances; perform specific procedures (e.g. inventory roll-back).',
            'If evidence is insufficient, the opinion is qualified or disclaimed; if prior period report was modified and the matter remains relevant, the current opinion is modified.'],
          'You inherit last year\'s closing numbers — verify them.',
          'Opening inventory misstated affects current year profit.'),
        C('c4', T4, [
            'Audit sampling applies procedures to less than 100% of items so that every sampling unit has a chance of selection. Sampling risk (conclusion differs from testing the whole population) and non-sampling risk (wrong procedures, misinterpretation) must be managed.',
            'Design considers the purpose, population, stratification and value-weighted selection; selection methods include random, systematic and monetary unit sampling (haphazard and block selection are less suited to statistical sampling).',
            'Deviations in tests of controls and misstatements in tests of details are evaluated; misstatements are projected to the population and compared with tolerable misstatement. Anomalies may be excluded only with a high degree of certainty that they are not representative.'],
          'Test part, project to the whole, and allow for sampling risk.',
          'A 4% error rate in sample implies about ₹8 lakh error on ₹200 lakh.'),
        C('c5', T5, [
            'SA 550 requires understanding related party relationships and transactions, remaining alert for undisclosed ones, and evaluating whether they are properly accounted for and disclosed under the framework.',
            'Risk assessment includes enquiring of management, inspecting records (minutes, contracts, shareholder registers, tax returns), and treating significant related party transactions outside the normal course of business as significant risks.',
            'If new related parties are found, the auditor communicates to the team, asks management to identify all transactions, re-evaluates fraud risk, and performs substantive procedures. Written representations are obtained that all related parties have been disclosed.'],
          'Related parties can hide transactions not at arm\'s length.',
          'A large unsecured loan to a director\'s firm is a significant risk.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Receivables audit', 'role': 'Audit assistant',
             'situation': 'Receivables of ₹50 crore across 2,000 customers.',
             'steps': ['Stratify and select a sample.', 'Send positive confirmations to large balances.', 'Do alternative procedures for non-replies.', 'Project misstatements and report.'],
             'takeaway': 'Good sampling plus confirmations gives strong evidence.'}]

    mcqs = [
        Q('m1', 'Evidence is generally more reliable when obtained:', ['From independent external sources', 'Orally from management', 'From photocopies', 'Indirectly'], 0,
          'SA 500 reliability hierarchy. In practice: confirmations.', 'c1', T1),
        Q('m2', 'Attendance at physical inventory counting is required when inventory is:', ['Material', 'Small', 'Held abroad only', 'Fully insured'], 0,
          'SA 501. In practice: unless impracticable.', 'c1', T1),
        Q('m3', 'Negative confirmations are appropriate when:', ['Risk is low and population is large and homogeneous', 'Risk is high', 'Few large balances exist', 'Controls are weak'], 0,
          'All conditions needed. In practice: combine with other procedures.', 'c2', T2),
        Q('m4', 'If management refuses a confirmation request, the auditor should first:', ['Enquire into the reasons and their validity', 'Accept silently', 'Resign immediately', 'Ignore the balance'], 0,
          'Then alternative procedures. In practice: fraud risk.', 'c2', T2),
        Q('m5', 'In an initial engagement, the auditor must gather evidence on:', ['Opening balances and consistency of policies', 'Only closing balances', 'Fees', 'Board minutes only'], 0,
          'SA 510. In practice: predecessor papers.', 'c3', T3),
        Q('m6', 'Sampling risk is the risk that:', ['The conclusion from a sample differs from testing the whole population', 'Wrong procedures are used', 'Staff are untrained', 'Documents are lost'], 0,
          'Non-sampling risk differs. In practice: larger sample reduces it.', 'c4', T4),
        Q('m7', 'Significant related party transactions outside the normal course of business are treated as:', ['Significant risks', 'Trivial', 'Not auditable', 'Management issues only'], 0,
          'SA 550. In practice: examine contracts.', 'c5', T5),
        Q('m8', 'Monetary unit sampling selects items with probability:', ['Proportional to their value', 'Equal for all', 'Based on date', 'Based on customer name'], 0,
          'Value-weighted. In practice: large balances favoured.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Rate', 1.5, 'computation', 'rate', nums=[rate]), S('s2', 'Projection', 2, 'computation', 'projected', nums=[proj]), S('s3', 'Conclusion', 1.5, 'concept', 'tolerable|sampling risk')],
          ['Compare with tolerable.'], ['Looking only at sample error.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Refusal', 2, 'concept', 'reasons|alternative'), S('s2', 'Non-reply', 1.5, 'concept', 'alternative'), S('s3', 'Reliability and exceptions', 2.5, 'concept', 'reliab|exception')],
          ['Cite SA 505.'], ['Accepting refusal without enquiry.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What makes audit evidence appropriate?', 'Its relevance and reliability for the assertion being tested.',
          [P('p1', 'Relevance', 5, 'relevan'), P('p2', 'Reliability', 5, 'reliab')], 'c1'),
        V('v2', 'Distinguish positive and negative confirmations.', 'Positive confirmations ask the party to reply in all cases; negative ones ask for a reply only if they disagree.',
          [P('p1', 'Reply always', 5, 'all cases'), P('p2', 'Reply if disagree', 5, 'disagree')], 'c2'),
        V('v3', 'What procedures apply to opening balances in an initial audit?', 'Reading prior statements and report, reviewing predecessor working papers, and performing specific procedures to obtain evidence.',
          [P('p1', 'Predecessor papers', 5, 'predecessor'), P('p2', 'Specific procedures', 5, 'specific')], 'c3'),
        V('v4', 'How are sample misstatements evaluated?', 'They are projected to the population and compared with tolerable misstatement, considering sampling risk.',
          [P('p1', 'Projected', 5, 'project'), P('p2', 'Tolerable', 5, 'tolerable')], 'c4'),
        V('v5', 'What written representation is needed under SA 550?', 'That management has disclosed all known related parties and transactions and accounted for them properly.',
          [P('p1', 'All related parties', 5, 'related parties'), P('p2', 'Properly accounted', 5, 'accounted|disclosed')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Prime Distributors Ltd.', 'difficulty': 'moderate',
              'case': 'Prime Distributors stores 30% of its inventory with a third-party warehouse. It faces a ₹5 crore lawsuit from a customer. This is the first year of audit by the current firm; the predecessor issued a qualified opinion on inventory last year. A company owned by the MD\'s brother bought goods at a 25% discount.',
              'mcqs': [
                  M('k1a', 'For third-party held inventory, the auditor should:', ['Confirm with the custodian and/or inspect', 'Ignore it', 'Rely on management', 'Only enquire'], 0,
                    'SA 501. In practice: consider custodian\'s integrity.', 'core', topic=T1),
                  M('k1b', 'For the lawsuit, the auditor should:', ['Seek direct communication with external legal counsel', 'Only review the ledger', 'Ignore unless settled', 'Ask the customer'], 0,
                    'SA 501 litigation procedures. In practice: letter of enquiry.', 'core', topic=T1),
                  M('k1c', 'The predecessor\'s qualification on inventory means:', ['Opening balance evidence and possible current modification must be considered', 'No effect', 'Automatic disclaimer', 'Restatement required'], 0,
                    'SA 510. In practice: closing inventory of prior year affects profit.', 'moderate', topic=T3),
                  M('k1d', 'The discounted sale to the brother\'s company is:', ['A related party transaction needing scrutiny', 'Normal trade', 'Irrelevant', 'Fraud automatically'], 0,
                    'SA 550 and Ind AS 24. In practice: check approvals.', 'core', topic=T5),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch05', 1, 'Audit Evidence',
                ['Obtain sufficient appropriate evidence including for specific items.',
                 'Use external confirmations correctly.',
                 'Audit opening balances in initial engagements.',
                 'Design and evaluate audit samples.',
                 'Audit related party relationships and transactions.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p3-ch04-u01'],
                 'exam_tip': 'Name the SA, the procedure and the conclusion — in that order.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['SA 500: sufficient and appropriate evidence.',
                             'SA 501: inventory count, litigation, segments.',
                             'SA 505: positive/negative, refusals, non-replies.',
                             'SA 510: opening balances; SA 530: sampling.',
                             'SA 550: related parties as significant risks.'],
                 'remember': ['Auditor controls confirmation process.'],
                 'traps': ['Using negative confirmations for high-risk balances.']},
                [('SA 501', 'Inventory, litigation, segments'), ('SA 505', 'Confirmations'), ('SA 530', 'Sampling'), ('SA 550', 'Related parties')],
                viva, cases)
