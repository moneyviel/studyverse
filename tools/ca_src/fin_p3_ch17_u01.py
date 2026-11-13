"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 17 Due Diligence, Investigation & Forensic Accounting.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch17-u01'
T1 = 'Due diligence: types, approach and report'
T2 = 'Investigation: nature, steps and audit compared'
T3 = 'Types of investigation'
T4 = 'Forensic accounting and investigation standards'


def build():
    ck = Checks()
    avg = ck.add('round((60+72+78-6)/3,2)', 'Average maintainable profit after removing a one-off gain (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Maintainable profit for an incoming partner', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A prospective partner investigates a firm whose profits for three years were ₹60 lakh, ₹72 lakh and ₹78 lakh. The last year includes a one-off gain of ₹6 lakh on sale of a vehicle. Compute average maintainable profit and list other matters to investigate.',
          'solution': [table(['Item', 'Working / Matter', 'Result'], [
              ['Adjusted average profit', '(60 + 72 + 78 − 6) ÷ 3', '₹' + inr(avg) + ' lakh'],
              ['Partnership deed', 'Profit sharing, capital, retirement terms', '—'],
              ['Liabilities', 'Hidden or contingent liabilities, pending suits', '—'],
              ['Assets and goodwill', 'Realistic values; customer dependence', '—']], title='Investigation for incoming partner')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Spotting fraud red flags', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A forensic accountant reviews a company: (a) many vendor bank accounts match employee accounts; (b) invoices just below approval limits; (c) round-sum journal entries posted at night by a senior manager; (d) sudden lifestyle change of a purchase officer. Classify the signal and next step.',
          'solution': [table(['Signal', 'Likely issue', 'Next step'], [
              ['(a)', 'Shell/ghost vendors', 'Match master data; trace payments'],
              ['(b)', 'Split purchases to bypass approval', 'Analyse invoice patterns (Benford, thresholds)'],
              ['(c)', 'Management override', 'Examine support and approvals; interview'],
              ['(d)', 'Possible kickbacks', 'Background and asset checks within law']], title='Forensic indicators')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Due diligence is an investigation of a business before a transaction (acquisition, merger, investment, lending) to confirm facts, find risks and support valuation and negotiation.',
            'Types: financial, tax, legal, commercial/operational, human resources, IT, environmental and others. Financial due diligence examines quality of earnings, working capital, net debt, contingent liabilities, projections and accounting policies.',
            'Approach: agree scope, obtain data room information, analyse, interview management, and report. The report contains executive summary, scope and limitations, key findings and deal issues, quality of earnings adjustments, and recommendations for price or protections.'],
          'Due diligence turns a seller\'s story into verified facts.',
          'Normalising earnings removes one-off gains before valuation.'),
        C('c2', T2, [
            'Investigation is a critical, in-depth examination of records for a specific purpose (fraud, valuation, loan, partnership), often with no fixed scope, unlike an audit which gives an opinion on statements under standards.',
            'Steps: define objective and scope; plan; gather and examine evidence (documents, interviews, analytics); evaluate findings; report facts with supporting evidence — the investigator reports facts, not opinions beyond the mandate.',
            'Special issues: investigation period, reliance on audited statements, legal considerations, confidentiality, and need for experts.'],
          'Audit opines on statements; investigation finds facts for a purpose.',
          'A lender\'s investigation focuses on repayment capacity and security.'),
        C('c3', T3, [
            'Investigations for an incoming partner (profit trend, maintainable profit, deed terms, liabilities), for valuation of shares in private companies (maintainable profit, assets, restrictions), for a bank or financial institution considering a loan (purpose, financial position, management, security, cash flows), and for a buyer of a business.',
            'Fraud investigations: misappropriation of cash or goods, manipulation of accounts, fictitious payroll, purchase frauds; review of profit forecasts.',
            'Each type adjusts focus and procedures to the client\'s decision.'],
          'Same skills, different questions for each client.',
          'A bank asks: can the borrower repay and is the security adequate?'),
        C('c4', T4, [
            'Forensic accounting applies accounting, auditing and investigative skills to legal matters — fraud detection, disputes, insolvency, valuation for litigation — producing evidence that can withstand court scrutiny.',
            'Process: initial meeting and scoping, planning, evidence collection (documents, digital forensics, data analytics, interviews), analysis (including Benford\'s law, trend and ratio analysis), reporting and possibly expert testimony.',
            'ICAI\'s Forensic Accounting and Investigation Standards (FAIS) guide engagements: independence and objectivity, engagement acceptance, planning, evidence gathering and documentation, using experts, and reporting. Forensic professionals need skepticism, legal awareness and confidentiality.'],
          'Forensic work must be evidence-grade for courts.',
          'Data analytics flags vendors sharing bank accounts with employees.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Buy-side due diligence', 'role': 'Transaction advisory associate',
             'situation': 'A PE fund is buying a 60% stake in a food company.',
             'steps': ['Agree scope and data list.', 'Analyse quality of earnings and working capital.', 'Identify contingent and tax exposures.', 'Report deal issues and price adjustments.'],
             'takeaway': 'Findings must translate into price or protection.'}]

    mcqs = [
        Q('m1', 'Due diligence is primarily performed:', ['Before a transaction to verify facts and risks', 'After an audit', 'For tax filing', 'For peer review'], 0,
          'Supports decisions. In practice: data room.', 'c1', T1),
        Q('m2', 'Quality of earnings analysis adjusts for:', ['One-off and non-recurring items', 'Only taxes', 'Only depreciation', 'Nothing'], 0,
          'Maintainable profits. In practice: normalisation.', 'c1', T1),
        Q('m3', 'A key difference between audit and investigation is that investigation:', ['Has a specific purpose and reports facts', 'Always gives a true and fair opinion', 'Is mandatory by law for all', 'Has fixed scope'], 0,
          'Purpose-driven. In practice: scope from client.', 'c2', T2),
        Q('m4', 'An investigation for a bank considering a loan focuses on:', ['Repayment capacity, purpose and security', 'Only dividends', 'Only HR policies', 'Only marketing'], 0,
          'Lender\'s risk. In practice: cash flows.', 'c3', T3),
        Q('m5', 'Forensic accounting findings must be:', ['Capable of withstanding legal scrutiny', 'Informal', 'Opinion-based', 'Unsupported'], 0,
          'Court-grade evidence. In practice: chain of custody.', 'c4', T4),
        Q('m6', 'Benford\'s law is used to:', ['Detect unusual patterns in digit frequencies', 'Compute tax', 'Value shares', 'Set materiality'], 0,
          'Fraud analytics. In practice: test leading digits.', 'c4', T4),
        Q('m7', 'ICAI\'s standards for forensic engagements are called:', ['Forensic Accounting and Investigation Standards (FAIS)', 'SQC', 'SRE', 'SIA only'], 0,
          'Issued by ICAI. In practice: guide engagements.', 'c4', T4),
        Q('m8', 'For an incoming partner, the investigator examines:', ['Maintainable profits, deed terms and hidden liabilities', 'Only bank balance', 'Only GST', 'Only customers'], 0,
          'Decision-focused. In practice: goodwill.', 'c3', T3),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Average profit', 2.5, 'computation', 'average', nums=[avg]), S('s2', 'Other matters', 2.5, 'concept', 'deed|liabilit|goodwill')],
          ['Remove one-offs.'], ['Using unadjusted profits.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Vendors and splitting', 3, 'concept', 'vendor|split'), S('s2', 'Override and kickbacks', 3, 'concept', 'override|kickback')],
          ['Signal and step.'], ['Accusing without evidence.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is due diligence?', 'An independent examination of a business before a transaction to verify facts, identify risks and support valuation.',
          [P('p1', 'Before a transaction', 5, 'transaction'), P('p2', 'Risks and valuation', 5, 'risk|valuation')], 'c1'),
        V('v2', 'Distinguish audit and investigation.', 'Audit gives an opinion on statements under standards with a defined scope; investigation is a purpose-specific in-depth examination reporting facts.',
          [P('p1', 'Opinion', 5, 'opinion'), P('p2', 'Purpose-specific facts', 5, 'purpose|facts')], 'c2'),
        V('v3', 'What does a bank\'s investigation cover?', 'The purpose of the loan, the borrower\'s financial position and management, cash flows for repayment and adequacy of security.',
          [P('p1', 'Repayment capacity', 5, 'repayment|cash'), P('p2', 'Security', 5, 'security')], 'c3'),
        V('v4', 'What is forensic accounting?', 'Applying accounting and investigative skills to produce evidence for legal matters such as fraud and disputes.',
          [P('p1', 'Investigative skills', 5, 'investigative'), P('p2', 'Legal matters', 5, 'legal')], 'c4'),
        V('v5', 'Name stages of a forensic engagement.', 'Scoping, planning, evidence collection, analysis, reporting and expert testimony.',
          [P('p1', 'Planning and evidence', 5, 'planning|evidence'), P('p2', 'Reporting and testimony', 5, 'reporting|testimony')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Kalpa Constructions', 'difficulty': 'moderate',
              'case': 'An investor plans to buy Kalpa Constructions. Due diligence finds revenue recognised on uncompleted flats, a pending tax demand of ₹4 crore, and payments to a contractor whose address matches a director\'s relative. The investor also asks for a forensic review.',
              'mcqs': [
                  M('k1a', 'Revenue on uncompleted flats affects:', ['Quality of earnings', 'Only HR', 'Nothing', 'Only tax'], 0,
                    'Normalise for policy errors. In practice: adjust price.', 'core', topic=T1),
                  M('k1b', 'The pending tax demand should be:', ['Reported as a contingent exposure with deal protection', 'Ignored', 'Paid by investor', 'Capitalised'], 0,
                    'Indemnity or escrow. In practice: tax due diligence.', 'core', topic=T1),
                  M('k1c', 'The contractor payments suggest:', ['A related party or fraud red flag for forensic review', 'Normal business', 'Audit not needed', 'Tax saving'], 0,
                    'Investigate. In practice: trace payments.', 'core', topic=T4),
                  M('k1d', 'The forensic review should follow:', ['ICAI\'s FAIS', 'SA 810', 'SRE 2410', 'SAE 3402'], 0,
                    'Forensic standards. In practice: evidence handling.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch17', 1, 'Due Diligence, Investigation & Forensic Accounting',
                ['Plan and report due diligence reviews.',
                 'Conduct investigations and distinguish them from audits.',
                 'Apply different types of investigation.',
                 'Perform forensic accounting under FAIS.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 20}, 'prereq': ['fin-p3-ch16-u01'],
                 'exam_tip': 'Identify the client and decision — that defines the investigation\'s focus.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Due diligence types and report contents.',
                             'Quality of earnings and contingent exposures.',
                             'Investigation: purpose-specific facts.',
                             'Investigations for partner, valuation, bank, buyer, fraud.',
                             'Forensic accounting and FAIS; analytics like Benford.'],
                 'remember': ['Investigators report facts, not opinions beyond mandate.'],
                 'traps': ['Treating investigation as an audit.']},
                [('Due diligence', 'Pre-transaction'), ('Investigation', 'Specific purpose'), ('Forensic', 'Court-grade'), ('FAIS', 'ICAI standards')],
                viva, cases)
