"""CA Final · Paper 1 Financial Reporting · Chapter 3 Unit 1 Ind AS 1 Presentation of Financial Statements.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch03-u01'
T1 = 'Purpose and complete set of financial statements'
T2 = 'General features: fair presentation, going concern, materiality, offsetting, comparatives'
T3 = 'Current and non-current classification'
T4 = 'Profit or loss, OCI, changes in equity and notes'


def build():
    i1 = {'id': 'i1', 'title': 'Current or non-current?', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Reporting date 31 March 2027; statements approved 20 May 2027. Classify: (a) a term loan of ₹50 crore due on 30 November 2027, refinanced for five years on 10 April 2027; (b) a loan covenant breached on 15 March 2027 making the loan repayable on demand; on 5 May 2027 the bank agreed not to demand payment; (c) the same breach, but on 25 March 2027 the bank granted a grace period up to 30 June 2028 during which it will not demand repayment; (d) a ₹20 crore drawing under a 5-year committed facility, repayable in 6 months but which the entity has the right and expectation to roll over; (e) trade payables due in 14 months within the 18-month operating cycle.',
          'solution': [table(['Item', 'Classification', 'Reason'], [
              ['(a)', 'Current', 'Due within 12 months; refinancing agreed after the reporting date does not change classification'],
              ['(b)', 'Non-current (Ind AS 1 carve-out)', 'Under Ind AS, a lender\'s agreement before approval of the statements not to demand payment following a breach allows non-current classification (IAS 1 would require current)'],
              ['(c)', 'Non-current', 'Grace period agreed by the reporting date ends more than 12 months later and the lender cannot demand repayment meanwhile'],
              ['(d)', 'Non-current', 'Entity expects and has the discretion under an existing facility to roll over for at least 12 months'],
              ['(e)', 'Current', 'Operating items settled within the normal operating cycle are current even if due after 12 months']], title='Ind AS 1 — liabilities')],
          'checks': []}

    ck = Checks()
    oci = ck.add('-4+2.5+1.5', 'Total OCI (₹ crore)')
    tci = ck.add('60-4+2.5+1.5', 'Total comprehensive income (₹ crore)')
    i2 = {'id': 'i2', 'title': 'Splitting OCI', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Profit for the year ₹60 crore. Other items (net of tax): actuarial loss on defined benefit plan ₹4 crore; gain on equity investments designated at FVOCI ₹2.5 crore; exchange gain on translating a foreign operation ₹1.5 crore. Present OCI showing the two required groups and compute total comprehensive income.',
          'solution': [table(['Item', '₹ crore'], [
              ['Profit for the year', inr(60)],
              ['A. OCI that never moves to profit or loss', ''],
              ['   Remeasurement of defined benefit plan', '(4.0)'],
              ['   Equity instruments through OCI', '2.5'],
              ['B. OCI that moves to profit or loss later', ''],
              ['   Exchange differences on foreign operation', '1.5'],
              ['Other comprehensive income', str(oci)],
              ['Total comprehensive income', str(tci)]], title='Statement of profit and loss (extract)')],
          'checks': list(ck)}

    concepts = [
        C('c1', T1, [
            'Ind AS 1 sets the overall requirements for presenting general purpose financial statements, their structure and minimum content, so that they are comparable over time and with other entities.',
            'A complete set comprises: balance sheet at period end; a profit and loss statement (with OCI) for the period; a statement of equity movements; a cash flow statement; notes giving material accounting policy information and other explanations; comparative information; and a balance sheet as at the beginning of the earliest comparative period when an accounting policy is applied retrospectively, or items are restated or reclassified, with a material effect on that opening position.',
            'In India the statements are presented in the Schedule III Division II format, which builds on Ind AS 1. A single statement of profit and loss (with OCI) is presented under Schedule III.'],
          'Ind AS 1 is the frame of the picture; other standards decide the paint.',
          'A material error corrected retrospectively requires a third balance sheet at the start of the comparative year.'),
        C('c2', T2, [
            'Fair presentation: faithful representation of transactions under the Framework, achieved by complying with Ind AS, with an explicit unreserved statement of compliance. In extremely rare cases where compliance would be so misleading that it conflicts with the objective, an entity departs and discloses the reasons and effect, if the regulatory framework permits.',
            'Going concern: management assesses ability to continue for at least 12 months from the reporting date; material uncertainties are disclosed; if not a going concern, another basis is used and disclosed. Accrual basis applies except for cash flow information.',
            'Materiality and aggregation: each material class of similar items is presented separately; information is material when leaving it out, getting it wrong or hiding it among other details could be expected to sway users\' decisions. Offsetting of assets and liabilities, or income and expenses, is not allowed unless an Ind AS requires or permits it.',
            'Reporting is at least annual; if the period changes, the reason is disclosed and amounts are not fully comparable. At least one year of comparatives is given for amounts and, where relevant, narratives. Presentation and classification are consistent between periods unless a change gives more relevant information or an Ind AS requires it.'],
          'True and fair comes from following Ind AS and saying so clearly.',
          'Showing trade receivables net of a related loan from the same customer would be prohibited offsetting.'),
        C('c3', T3, [
            'Assets and liabilities are split into current and non-current unless a liquidity-based presentation is more reliable and relevant (e.g. for financial institutions).',
            'Current assets: expected to be realised, sold or consumed in the normal operating cycle; held mainly for trading; expected to be realised within 12 months; or unrestricted cash and cash equivalents. The operating cycle runs from buying inputs for processing to collecting cash; where it cannot be identified, 12 months is used.',
            'Current liabilities: expected to be settled in the normal operating cycle; held mainly for trading; due within 12 months; or where there is no right, existing at the reporting date and having substance, to defer settlement for at least 12 months. Settlement through equity at the counterparty\'s option does not affect classification. Covenants to be complied with only after the reporting date do not affect classification, but are disclosed.',
            'Refinancing after the reporting date does not make a loan non-current; but where the entity has discretion under an existing facility to roll it over for 12 months, it is non-current. Ind AS carve-out: a breach-related loan stays non-current if, after the reporting date and before approval, the lender agrees not to demand payment.'],
          'Classification depends on rights and expectations at the reporting date, not on what happens after it — except for the Ind AS carve-out on breaches.',
          'Whisky maturing for 3 years in a distillery\'s normal cycle is a current asset.'),
        C('c4', T4, [
            'Statement of profit and loss: profit or loss section, followed by OCI, then total comprehensive income; with profit and total comprehensive income attributed to owners of the parent and non-controlling interests. Expenses are analysed by nature under Schedule III. No item is presented as "extraordinary".',
            'OCI is shown in two groups: items that stay out of profit or loss for good (e.g. revaluation surplus, remeasurement of defined benefit plans, equity investments at FVOCI) and items that later move into profit or loss (e.g. foreign operation translation differences, cash flow hedges, debt instruments at FVOCI). Income tax on OCI and reclassification adjustments are disclosed.',
            'Statement of changes in equity shows total comprehensive income, effects of retrospective changes, and transactions with owners (contributions, distributions, ownership changes) for each component of equity.',
            'Notes present the basis of preparation and material accounting policy information, judgements made in applying policies, key sources of estimation uncertainty, capital management, and other required information.'],
          'Profit tells performance; OCI holds remeasurements that standards keep out of profit.',
          'An actuarial loss on gratuity goes to OCI and never returns to profit or loss.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Year-end classification review', 'role': 'Audit senior',
             'situation': 'The client has several loans with covenants and some breaches near year end.',
             'steps': ['List each borrowing with maturity and covenant status at the reporting date.', 'Check rights to defer settlement and their substance.', 'Apply the Ind AS carve-out for post-year-end waivers.', 'Disclose covenant information for non-current loans.'],
             'takeaway': 'Read the loan agreements and dates — classification turns on them.'}]

    mcqs = [
        Q('m1', 'A third balance sheet is required when:', ['A retrospective change has a material effect on the opening balance sheet of the comparative period', 'Any new standard is issued', 'The company is listed', 'Profit falls'], 0,
          'Ind AS 1 requires a balance sheet at the beginning of the earliest comparative period in such cases. In practice: notes for it are not always needed.', 'c1', T1),
        Q('m2', 'Offsetting a receivable against a payable is allowed when:', ['An Ind AS requires or permits it', 'Both are with the same party', 'Amounts are small', 'Management prefers it'], 0,
          'Offsetting is prohibited unless a standard allows it (e.g. Ind AS 32 conditions). In practice: gross presentation is the rule.', 'c2', T2),
        Q('m3', 'Going concern assessment covers at least:', ['Twelve months from the end of the reporting period', 'Six months', 'Three years', 'Until the next AGM'], 0,
          'Ind AS 1 sets 12 months as the minimum horizon. In practice: consider events after it too.', 'c2', T2),
        Q('m4', 'Where an entity cannot clearly identify its operating cycle, Ind AS 1 presumes it to be:', ['Twelve months', 'Six months', 'Twenty-four months', 'The audit period'], 0,
          'Ind AS 1 presumes 12 months. In practice: disclose the cycle used.', 'c3', T3),
        Q('m5', 'A loan due in 4 months is refinanced on a long-term basis after the reporting date but before approval. Classification:', ['Current', 'Non-current', 'Equity', 'Contingent liability'], 0,
          'Refinancing after the reporting date does not create a right that existed at that date. In practice: disclose the refinancing as a non-adjusting event.', 'c3', T3),
        Q('m6', 'Under the Ind AS carve-out, a loan payable on demand due to a pre-year-end breach is non-current if:', ['The lender agrees, before the statements are approved, not to demand payment', 'The entity intends to repay later', 'The breach is small', 'The bank is a related party'], 0,
          'Ind AS 1 departs from IAS 1 here. In practice: document the lender\'s letter and its date.', 'c3', T3),
        Q('m7', 'Which OCI item will be reclassified to profit or loss later?', ['Exchange differences on translating a foreign operation', 'Remeasurement of defined benefit plans', 'Revaluation surplus', 'Equity instruments designated at FVOCI'], 0,
          'Translation differences are recycled on disposal of the foreign operation. The others are not. In practice: present the two groups separately.', 'c4', T4),
        Q('m8', 'Under Ind AS 1, presenting items as "extraordinary":', ['Is prohibited', 'Is required for rare events', 'Is allowed in notes only', 'Is optional'], 0,
          'No income or expense may be called extraordinary. In practice: disclose material items separately instead.', 'c4', T4),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Refinancing after date', 1.5, 'concept', 'after the reporting|current'), S('s2', 'Carve-out', 2, 'concept', 'carve'),
           S('s3', 'Grace period', 1.5, 'concept', 'grace'), S('s4', 'Roll-over discretion', 1.5, 'concept', 'discretion|roll'), S('s5', 'Operating cycle', 1.5, 'concept', 'operating cycle')],
          ['Anchor each answer on the reporting date.'], ['Ignoring the Ind AS carve-out.'], ['Table.'], pad='table'),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Never-recycled group', 2, 'concept', 'never moves'), S('s2', 'Recycled group', 1, 'concept', 'moves to profit or loss later'), S('s3', 'Totals', 1, 'computation', 'total', nums=[tci])],
          ['Show both groups.'], ['Putting actuarial losses in the recycled group.'], ['Extract.'], pad='table', checks=list(ck)),
    ]

    viva = [
        V('v1', 'List the components of a complete set of financial statements.', 'Balance sheet, profit and loss with OCI, statement of equity movements, cash flow statement, notes and comparatives, plus an opening balance sheet in certain retrospective cases.',
          [P('p1', 'Statements', 5, 'balance sheet|cash flows'), P('p2', 'Notes and comparatives', 5, 'notes|comparative')], 'c1'),
        V('v2', 'When is information material?', 'When leaving it out, misstating it or burying it could be expected to influence the decisions primary users make from the statements.',
          [P('p1', 'Omit, misstate, obscure', 5, 'omit|misstat|obscur'), P('p2', 'Influence decisions', 5, 'influence|decision')], 'c2'),
        V('v3', 'When is a liability current?', 'When it is expected to be settled in the operating cycle, held for trading, due within 12 months, or the entity lacks a substantive right at the reporting date to defer settlement for 12 months.',
          [P('p1', 'Cycle or 12 months', 5, 'cycle|12 months|twelve'), P('p2', 'Right to defer', 5, 'defer')], 'c3'),
        V('v4', 'What is the Ind AS 1 carve-out on loan breaches?', 'If the lender agrees after the reporting date but before approval of the statements not to demand payment, the liability is not reclassified as current, unlike IAS 1.',
          [P('p1', 'Lender agreement', 5, 'lender|agree'), P('p2', 'Before approval', 5, 'approval')], 'c3'),
        V('v5', 'Give two items of OCI that are never reclassified.', 'Remeasurements of defined benefit plans and changes in revaluation surplus, as well as fair value changes on equity instruments designated at FVOCI.',
          [P('p1', 'Defined benefit', 5, 'defined benefit|remeasure'), P('p2', 'Revaluation or equity', 5, 'revaluation|equity')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Kaveri Infra Ltd.', 'difficulty': 'hard',
              'case': 'Kaveri Infra Ltd. (Ind AS; year end 31 March 2027; approval 25 May 2027) builds roads with a 3-year operating cycle. It holds retention money receivable in 30 months on an ongoing project; a debenture repayable in 9 months; a ₹100 crore term loan whose interest-cover covenant is tested only on 30 September 2027; and it discovered that 2025-26 revenue was overstated by a material amount.',
              'mcqs': [
                  M('k1a', 'Retention money receivable within the 3-year operating cycle is:', ['Current', 'Non-current', 'Equity', 'Contingent asset'], 0,
                    'Assets realised in the normal operating cycle are current even beyond 12 months. In practice: disclose the amount due after 12 months.', 'moderate', topic=T3),
                  M('k1b', 'The debenture repayable in 9 months is:', ['Current', 'Non-current due to the long cycle', 'Equity', 'Off balance sheet'], 0,
                    'Financing liabilities due within 12 months are current regardless of the operating cycle. In practice: show as current maturities.', 'moderate', topic=T3),
                  M('k1c', 'The term loan with a covenant tested only after the reporting date:', ['Is non-current if otherwise due after 12 months, with covenant disclosures', 'Must be current', 'Is equity', 'Is ignored'], 0,
                    'Covenants to be complied with after the reporting date do not affect classification, but information about them is disclosed. In practice: note the risk of breach.', 'hard', topic=T3),
                  M('k1d', 'Correcting the 2025-26 revenue error retrospectively with material effect requires:', ['A third balance sheet as at 1 April 2025', 'Only a note', 'Restating only 2026-27', 'No change'], 0,
                    'A material retrospective restatement affecting the opening comparative balance sheet needs a balance sheet at the beginning of the comparative period. In practice: Ind AS 8 governs the correction.', 'hard', topic=T1),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch03', 1, 'Ind AS 1 "Presentation of Financial Statements"',
                ['Identify the components of a complete set of financial statements.',
                 'Apply the general features of presentation.',
                 'Classify assets and liabilities as current or non-current, including the Ind AS carve-out.',
                 'Present profit or loss, OCI, changes in equity and notes.'],
                {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 35}, 'prereq': ['fin-p1-ch02-u01'],
                 'exam_tip': 'For loan classification, write the reporting date, approval date and when each event happened before concluding.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Complete set incl. third balance sheet on material retrospective changes.',
                             'Fair presentation, going concern (12 months), accrual, materiality, no offsetting, comparatives, consistency.',
                             'Current: operating cycle, trading, 12 months, no substantive right to defer.',
                             'Ind AS carve-out on post-year-end lender waivers.',
                             'OCI in two groups; no extraordinary items.'],
                 'remember': ['Refinancing after year end does not change classification.'],
                 'traps': ['Operating items stay current beyond 12 months; financing items do not.']},
                [('Operating cycle unclear', '12 months'), ('Going concern horizon', '≥ 12 months'), ('Third balance sheet', 'Material retrospective change'), ('Breach carve-out', 'Waiver before approval → non-current')],
                viva, cases)
