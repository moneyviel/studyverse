"""CA Final · Paper 1 Financial Reporting · Chapter 15 Analysis of Financial Statements.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch15-u01'
T1 = 'Qualities of good financial statements'
T2 = 'Best practices in presentation and disclosure'
T3 = 'Reviewing statements for Ind AS compliance'
T4 = 'Common errors spotted in published accounts'


def build():
    ck = Checks()
    eq = ck.add('500+30', 'Corrected equity (₹ crore)')
    cl = ck.add('220-30', 'Corrected current liabilities before reclassification (₹ crore)')
    cl2 = ck.add('220-30+60', 'Corrected current liabilities after loan reclassification (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Correcting a draft balance sheet', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'Draft statements of Maple Ltd. at 31 March 2027 show equity ₹500 crore and current liabilities ₹220 crore. Review notes: (1) a final dividend of ₹30 crore, proposed by the board in May (after year end), is included in current liabilities; (2) a term loan of ₹60 crore is shown as non-current, but a covenant was breached on 31 March, making it repayable on demand; the lender has not agreed to waive the breach even by the date the accounts are approved; (3) the accounting policy says "balances of trade receivables are subject to confirmation". Correct the figures and comment.',
          'solution': [table(['Issue', 'Correction', '₹ crore'], [
              ['Proposed dividend', 'Non-adjusting event — remove liability, disclose in notes', inr(30)],
              ['Corrected equity', '500 + 30', inr(eq)],
              ['Current liabilities after dividend', '220 − 30', inr(cl)],
              ['Covenant breach', 'Loan repayable on demand at year end → current', inr(60)],
              ['Corrected current liabilities', '190 + 60', inr(cl2)],
              ['Confirmation wording', 'Vague — disclose actual status and any impact', '—']], title='Ind AS 1 and 10 review')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Spot the non-compliance', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'An annual report includes: (a) "Extraordinary items" in profit and loss; (b) "Investments in subsidiaries — at cost; associates — at fair value" in consolidated statements; (c) leasehold land under operating lease shown in PPE without a right-of-use label; (d) an impairment reversal of goodwill; (e) EPS shown only in the notes. Identify each issue.',
          'solution': [table(['Item', 'Issue', 'Standard'], [
              ['(a)', 'Extraordinary items are prohibited', 'Ind AS 1'],
              ['(b)', 'Subsidiaries are consolidated; associates use equity method', 'Ind AS 110 / 28'],
              ['(c)', 'Lease rights are right-of-use assets, presented or disclosed separately', 'Ind AS 116'],
              ['(d)', 'Goodwill impairment cannot be reversed', 'Ind AS 36'],
              ['(e)', 'Basic and diluted EPS on the face', 'Ind AS 33']], title='Compliance review')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Good financial statements give a true and fair view — the overriding quality that users rely on.',
            'They are relevant (useful for decisions by investors, lenders, employees), understandable (clear enough for a non-expert to grasp the main story), consistent (regular periods, standard formats prescribed by law), compliant with regulations, and comparable across companies and countries.',
            'These qualities drove global convergence of standards — Ind AS being India\'s converged set notified by the MCA.'],
          'True and fair first; then useful, clear, consistent, compliant and comparable.',
          'Two steel makers\' accounts should be readable side by side.'),
        C('c2', T2, [
            'Best practices: comply with standards and law while communicating clearly; give complete information without leaving obvious questions; keep disclosures consistent across sections; tailor accounting policies to the entity rather than copying boilerplate.',
            'Use materiality to cut clutter, cross-reference notes, explain significant judgements and estimates, and highlight new standards and their impact.',
            'Avoid vague statements (e.g. "balances are subject to confirmation") — state facts and quantify effects where known.'],
          'Say what is specific, material and true — skip the boilerplate.',
          'A revenue policy should describe the entity\'s actual contracts, not generic text.'),
        C('c3', T3, [
            'Analysing statements for compliance means reading each primary statement and note against Ind AS requirements: classification (current vs non-current), recognition, measurement, presentation and disclosure.',
            'A practical approach: start with accounting policies; check primary statement line items against Schedule III; cross-check notes to statements; test key judgements (control, revenue timing, leases, financial instruments); look at subsequent events and contingencies.',
            'Case studies often involve listed company extracts with deliberate errors; answers should identify the issue, cite the standard, explain the correct treatment and, where possible, quantify the correction.'],
          'Issue, standard, correct treatment, numbers — a four-part answer.',
          'From FY 2026-27, a loan made repayable on demand by a breach at year end is current unless, by the reporting date, the lender granted a grace period of at least 12 months; a later waiver no longer helps.'),
        C('c4', T4, [
            'Frequent errors: proposed dividends recognised as liabilities; extraordinary items; incorrect offsetting of assets and liabilities; current/non-current misclassification; missing EPS or segment disclosures; incorrect related party disclosures.',
            'Measurement errors: not discounting long-term provisions; reversing goodwill impairment; using fair value model for investment property; not recognising ECL; failing to separate lease and non-lease components.',
            'Consolidation errors: not eliminating intra-group items, measuring associates at fair value in consolidated statements without an exemption, or omitting NCI.'],
          'Most errors repeat — learn the usual suspects.',
          'Investment property revalued upward in the balance sheet is a red flag in India.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Pre-issue review of annual accounts', 'role': 'Quality reviewer',
             'situation': 'Draft annual report of a listed company before board approval.',
             'steps': ['Read policies for boilerplate and gaps.', 'Check statements against Schedule III and Ind AS.', 'Test judgements and subsequent events.', 'List corrections with quantification.'],
             'takeaway': 'A structured review catches errors before the market does.'}]

    mcqs = [
        Q('m1', 'The most important quality of financial statements is:', ['A true and fair view', 'Brevity', 'Colourful presentation', 'Tax savings'], 0,
          'Users rely on reliability. In practice: overrides other features.', 'c1', T1),
        Q('m2', 'A dividend proposed after year end should be:', ['Disclosed, not recognised as a liability', 'Recognised as a liability', 'Charged to profit', 'Ignored'], 0,
          'Non-adjusting event under Ind AS 10. In practice: note disclosure.', 'c4', T4),
        Q('m3', '"Extraordinary items" in Ind AS statements are:', ['Prohibited', 'Required', 'Optional', 'Shown in OCI'], 0,
          'Ind AS 1 bans them. In practice: disclose material items separately.', 'c4', T4),
        Q('m4', 'For FY 2026-27, a loan in breach at year end that the lender waives after year end but before approval is:', ['Current', 'Non-current', 'Equity', 'Contingent'], 0,
          'The Indian carve-out for later waivers was withdrawn for periods from 1 April 2026. In practice: disclose the waiver as a non-adjusting event.', 'c3', T3),
        Q('m5', 'Boilerplate accounting policies are:', ['Discouraged; policies should be entity-specific', 'Best practice', 'Required', 'Mandatory by SEBI'], 0,
          'Users need specifics. In practice: tailor text.', 'c2', T2),
        Q('m6', 'Reversal of a goodwill impairment is:', ['Not permitted', 'Permitted', 'Required', 'Shown in OCI'], 0,
          'Ind AS 36 prohibits it. In practice: a common review error.', 'c4', T4),
        Q('m7', 'A good compliance answer should include:', ['Issue, standard, correct treatment and quantification', 'Only the error', 'Only the standard number', 'A general comment'], 0,
          'Structured answers score. In practice: show revised figures.', 'c3', T3),
        Q('m8', 'Comparability means statements:', ['Can be compared across entities and periods', 'Are identical', 'Use the same auditor', 'Are in one currency'], 0,
          'Supports investor decisions. In practice: consistent policies.', 'c1', T1),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Dividend', 2, 'computation', 'dividend', nums=[eq]), S('s2', 'Covenant', 3, 'computation', 'covenant|current', nums=[cl2]), S('s3', 'Wording', 1, 'concept', 'confirm|vague'), S('s4', 'Standards', 2, 'concept', 'ind as 1|ind as 10|non-adjusting')],
          ['Cite standards.'], ['Keeping the loan non-current.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Presentation issues', 2, 'concept', 'extraordinary|face'), S('s2', 'Measurement issues', 3, 'concept', 'goodwill|equity method|right-of-use')],
          ['One line each.'], ['Missing the consolidation error.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'List the key qualities of good financial statements.', 'True and fair view, relevance, understandability, consistency, regulatory compliance and comparability.',
          [P('p1', 'True and fair', 5, 'true and fair'), P('p2', 'Relevance and comparability', 5, 'relevan|compar')], 'c1'),
        V('v2', 'What is wrong with "balances subject to confirmation"?', 'It is vague and raises doubt about whether balances are fairly stated, so facts and effects should be disclosed instead.',
          [P('p1', 'Vague', 5, 'vague'), P('p2', 'Disclose facts', 5, 'fact|effect')], 'c2'),
        V('v3', 'How should a compliance case study be answered?', 'Identify the issue, cite the standard, explain the right treatment and quantify the correction.',
          [P('p1', 'Issue and standard', 5, 'issue|standard'), P('p2', 'Treatment and amount', 5, 'treatment|quantif')], 'c3'),
        V('v4', 'Name three common presentation errors.', 'Proposed dividends as liabilities, extraordinary items, and wrong current versus non-current classification.',
          [P('p1', 'Dividends and extraordinary', 5, 'dividend|extraordinary'), P('p2', 'Classification', 5, 'classification')], 'c4'),
        V('v5', 'Why did standards converge globally?', 'To achieve comparability and consistent quality of financial statements across countries.',
          [P('p1', 'Comparability', 5, 'compar'), P('p2', 'Across countries', 5, 'countr')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Willow Ltd. annual report', 'difficulty': 'moderate',
              'case': 'Willow Ltd.\'s report shows: investment property at fair value with gains in profit of ₹12 crore; trade receivables with no loss allowance though 8% are over a year old; a provision for site restoration of ₹50 crore due in 10 years shown undiscounted; and a bank deposit of ₹20 crore netted against an unrelated bank\'s overdraft.',
              'mcqs': [
                  M('k1a', 'The investment property treatment breaches:', ['Ind AS 40, which allows only the cost model', 'Ind AS 16', 'Ind AS 113', 'Nothing'], 0,
                    'Fair value is disclosed, not recognised. In practice: reverse ₹12 crore gain.', 'core', topic=T4),
                  M('k1b', 'Receivables without loss allowance breach:', ['Ind AS 109 ECL requirements', 'Ind AS 2', 'Ind AS 115', 'Ind AS 37'], 0,
                    'Lifetime ECL under simplified approach. In practice: provision matrix.', 'core', topic=T4),
                  M('k1c', 'The undiscounted restoration provision should be:', ['Discounted as time value is material', 'Left as is', 'Expensed', 'Disclosed only'], 0,
                    'Ind AS 37 requires discounting. In practice: unwind as finance cost.', 'core', topic=T4),
                  M('k1d', 'Netting the deposit with another bank\'s overdraft is:', ['Not allowed — no legal right of set-off', 'Allowed', 'Required', 'Optional'], 0,
                    'Different counterparties. In practice: present gross.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch15', 1, 'Analysis of Financial Statements',
                ['Describe the qualities of good financial statements.',
                 'Apply best practices in presentation and disclosure.',
                 'Review published statements for Ind AS compliance.',
                 'Recognise and correct common errors.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 30}, 'prereq': ['fin-p1-ch14-u01'],
                 'exam_tip': 'For each extract item: issue → standard → correct treatment → revised figure.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['True and fair is paramount.',
                             'Entity-specific, complete, consistent disclosures.',
                             'Review policies, statements, notes, judgements.',
                             'Common errors: dividends, offsetting, classification.',
                             'Quantify corrections.'],
                 'remember': ['Loan breach at year end → current from FY 2026-27, unless a 12-month grace period was agreed by the reporting date.'],
                 'traps': ['Accepting fair value model for investment property.']},
                [('Dividend proposed later', 'Disclose'), ('Breach at year end', 'Current unless 12-month grace by year end'), ('Extraordinary', 'Prohibited'), ('Offset', 'Right + intent')],
                viva, cases)
