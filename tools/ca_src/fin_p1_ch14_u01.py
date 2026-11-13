"""CA Final · Paper 1 Financial Reporting · Chapter 14 Ind AS 101 First-time Adoption of Ind AS.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch14-u01'
T1 = 'Key dates and the opening Ind AS balance sheet'
T2 = 'Mandatory exceptions'
T3 = 'Optional exemptions'
T4 = 'Presentation, reconciliations and disclosures'


def build():
    ck = Checks()
    ppe = ck.add('650-500', 'PPE uplift to deemed cost (₹ crore)')
    dt = ck.add('(650-500)*0.25', 'Deferred tax on PPE uplift (₹ crore)')
    adj = ck.add('(650-500)+40-10-(650-500)*0.25', 'Net adjustment to retained earnings (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Opening Ind AS balance sheet adjustments', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Cedar Ltd. prepares its first Ind AS statements for the year ending 31 March 2026, with one year of comparatives. At the transition date: (a) it elects fair value of ₹650 crore as deemed cost for PPE carried at ₹500 crore under previous GAAP; (b) a proposed dividend of ₹40 crore was recorded as a liability under previous GAAP; (c) expected credit losses on receivables are ₹10 crore (none under previous GAAP). Tax rate 25% (deferred tax only on the PPE uplift). State the transition date and the net retained earnings adjustment.',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Date of transition', 'Start of earliest comparative period', '1 April 2024'],
              ['PPE to deemed cost', '650 − 500', inr(ppe)],
              ['Proposed dividend reversed', 'Not a liability until declared', inr(40)],
              ['ECL allowance', 'Reduce receivables', inr(-10)],
              ['Deferred tax on PPE uplift', '150 × 25%', inr(-dt)],
              ['Net increase in retained earnings', '150 + 40 − 10 − 37.5', inr(adj)]], title='Ind AS 101 transition')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Exception or exemption?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Classify each as a mandatory exception or an optional exemption: (a) not restating past business combinations; (b) using estimates consistent with previous GAAP unless they were in error; (c) using previous GAAP carrying amounts of PPE as deemed cost; (d) applying derecognition rules prospectively; (e) resetting cumulative translation differences to zero; (f) assessing hedge relationships only from transition.',
          'solution': [table(['Item', 'Type'], [
              ['(a)', 'Optional exemption'], ['(b)', 'Mandatory exception'], ['(c)', 'Optional exemption'],
              ['(d)', 'Mandatory exception'], ['(e)', 'Optional exemption'], ['(f)', 'Mandatory exception']], title='Exceptions vs exemptions')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'An entity\'s first Ind AS financial statements are the first annual statements in which it adopts Ind AS and says so clearly and without any reservation. The date of transition is the beginning of the earliest period for which full comparative information is presented under Ind AS.',
            'At the transition date, the entity prepares an opening Ind AS balance sheet: recognising all assets and liabilities Ind AS requires; derecognising items Ind AS does not permit; reclassifying items as required; and measuring all recognised items under Ind AS.',
            'The same accounting policies (the Ind AS effective at the end of the first Ind AS reporting period) are applied throughout all periods presented, subject to exceptions and exemptions. Adjustments arising from transition are recognised directly in retained earnings (or another equity category) at the transition date.'],
          'Pretend Ind AS always applied — except where the standard says not to.',
          'For first Ind AS statements at 31 March 2026 with one comparative year, transition is 1 April 2024.'),
        C('c2', T2, [
            'Mandatory exceptions prohibit retrospective application in certain areas: estimates (Ind AS estimates at transition must be consistent with previous GAAP estimates, after adjusting for policy differences, unless there is objective evidence of error); derecognition of financial assets and liabilities (prospective from transition, with an option for earlier application); and hedge accounting (only relationships qualifying under Ind AS 109 at transition).',
            'Other exceptions: NCI allocations (prospective from transition); classification and measurement of financial assets (based on facts at transition); impairment of financial assets (use reasonable information without undue cost; compare credit risk at transition if needed); embedded derivatives (assessed on conditions at the later of when first party and when reassessment required); government loans (previous GAAP carrying amount for below-market loans unless information was obtained earlier).',
            'These exceptions prevent use of hindsight.'],
          'Exceptions are compulsory and stop hindsight.',
          'You cannot revise a provision estimate using information that came later.'),
        C('c3', T3, [
            'Optional exemptions provide relief: past business combinations need not be restated (if restated, all later ones must be); deemed cost for PPE, investment property and intangibles — fair value at transition, a previous GAAP revaluation, or (specifically in Ind AS 101) previous GAAP carrying amount for all PPE, with decommissioning adjustments.',
            'Other exemptions: cumulative translation differences may be reset to zero; investments in subsidiaries, joint ventures and associates in separate statements at deemed cost (fair value or previous GAAP carrying amount); designation of previously recognised financial instruments based on facts at transition; share-based payments vested before transition; leases assessed at transition; and long-term foreign currency monetary items continuing previous GAAP policy.',
            'A subsidiary adopting later than its parent may measure assets at carrying amounts in the parent\'s consolidated statements.'],
          'Exemptions are choices that reduce cost and effort.',
          'Most Indian companies used previous GAAP carrying amounts as deemed cost for PPE.'),
        C('c4', T4, [
            'First Ind AS statements include at least three balance sheets (including the opening one), two statements of profit and loss, two cash flow statements, two statements of changes in equity and related notes.',
            'Reconciliations are required: equity under previous GAAP to Ind AS at transition and at the end of the latest previous GAAP period; total comprehensive income for the latest previous GAAP period; and material adjustments to the cash flow statement. Errors discovered must be distinguished from policy changes.',
            'Other disclosures: exemptions used, impairment losses recognised at transition, fair values used as deemed cost, and the aggregate adjustments.'],
          'Reconciliations bridge old and new numbers for users.',
          'An equity reconciliation shows each adjustment line by line.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Transition project', 'role': 'Ind AS conversion consultant',
             'situation': 'A company crosses the net worth threshold and must adopt Ind AS.',
             'steps': ['Fix the transition date.', 'Choose optional exemptions.', 'Prepare the opening balance sheet with adjustments.', 'Draft reconciliations and disclosures.'],
             'takeaway': 'Exemption choices made early shape every later number.'}]

    mcqs = [
        Q('m1', 'The date of transition is:', ['Beginning of the earliest comparative period presented', 'End of the first Ind AS period', 'Date of board approval', 'Date of incorporation'], 0,
          'Opening balance sheet date. In practice: one comparative year in India.', 'c1', T1),
        Q('m2', 'Transition adjustments are generally recognised in:', ['Retained earnings at the transition date', 'Profit or loss of the first year', 'OCI', 'Capital reserve'], 0,
          'Directly in equity. In practice: show in reconciliation.', 'c1', T1),
        Q('m3', 'Using hindsight for estimates at transition is:', ['Prohibited by a mandatory exception', 'Allowed', 'Required', 'Optional'], 0,
          'Estimates stay consistent unless in error. In practice: document.', 'c2', T2),
        Q('m4', 'Not restating past business combinations is:', ['An optional exemption', 'Mandatory', 'Prohibited', 'Required only for listed'], 0,
          'If one is restated, later ones must be too. In practice: commonly used.', 'c3', T3),
        Q('m5', 'Cumulative translation differences at transition may be:', ['Reset to zero', 'Recycled', 'Tax-adjusted only', 'Added to goodwill'], 0,
          'Optional exemption. In practice: simplifies records.', 'c3', T3),
        Q('m6', 'First Ind AS statements include how many balance sheets at minimum?', ['Three', 'Two', 'One', 'Four'], 0,
          'Including the opening balance sheet. In practice: transition, comparative, current.', 'c4', T4),
        Q('m7', 'Hedge accounting at transition applies to:', ['Relationships qualifying under Ind AS 109 at transition', 'All previous GAAP hedges', 'None', 'Only fair value hedges'], 0,
          'Mandatory exception. In practice: no retrospective designation.', 'c2', T2),
        Q('m8', 'A proposed dividend recorded as a liability under previous GAAP is, at transition:', ['Derecognised', 'Retained', 'Moved to OCI', 'Disclosed only'], 0,
          'No obligation until declared. In practice: increases equity.', 'c1', T1),
    ]

    questions = [
        W('q1', 7, i1['q'], i1['solution'],
          [S('s1', 'Transition date', 1, 'concept', 'transition'), S('s2', 'Adjustments', 3, 'computation', 'deemed|dividend|ecl', nums=[ppe]), S('s3', 'Deferred tax', 1, 'computation', 'deferred', nums=[dt]), S('s4', 'Net', 2, 'computation', 'net', nums=[adj])],
          ['Show each adjustment.'], ['Missing deferred tax.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Exceptions', 3, 'concept', 'mandatory'), S('s2', 'Exemptions', 3, 'concept', 'optional')],
          ['Classify each.'], ['Treating estimates as optional.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What are first Ind AS financial statements?', 'The first annual statements that state clearly and without qualification that they comply with Ind AS.',
          [P('p1', 'First annual', 4, 'first'), P('p2', 'Clear compliance statement', 6, 'without qualification|clearly')], 'c1'),
        V('v2', 'What four actions build the opening Ind AS balance sheet?', 'Recognise required items, derecognise disallowed items, reclassify items and measure everything under Ind AS.',
          [P('p1', 'Recognise and derecognise', 5, 'recognise'), P('p2', 'Reclassify and measure', 5, 'reclassify|measure')], 'c1'),
        V('v3', 'Why do mandatory exceptions exist?', 'To stop entities using hindsight when applying Ind AS retrospectively.',
          [P('p1', 'Hindsight', 6, 'hindsight'), P('p2', 'Retrospective', 4, 'retrospective')], 'c2'),
        V('v4', 'What deemed cost options exist for PPE?', 'Fair value at transition, a previous GAAP revaluation, or previous GAAP carrying amounts for all PPE.',
          [P('p1', 'Fair value', 5, 'fair value'), P('p2', 'Previous GAAP carrying amount', 5, 'carrying')], 'c3'),
        V('v5', 'Which reconciliations are required?', 'Equity at transition and at the latest previous GAAP period end, and total comprehensive income for the latest previous GAAP period.',
          [P('p1', 'Equity', 5, 'equity'), P('p2', 'Total comprehensive income', 5, 'comprehensive')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Birch Industries Ltd.', 'difficulty': 'moderate',
              'case': 'Birch Industries Ltd. adopts Ind AS with first statements for the year ending 31 March 2027 (one comparative year). Under previous GAAP it had a foreign subsidiary with a translation reserve of ₹25 crore and an acquisition in 2019 that it does not want to restate. It discovers that a previous GAAP provision was understated by ₹8 crore due to an arithmetic mistake.',
              'mcqs': [
                  M('k1a', 'Birch\'s date of transition is:', ['1 April 2025', '31 March 2027', '1 April 2026', '31 March 2025'], 0,
                    'Start of the comparative year. In practice: opening balance sheet date.', 'core', topic=T1),
                  M('k1b', 'If Birch resets translation differences, the ₹25 crore reserve at transition becomes:', ['Nil', '25', '50', 'Negative'], 0,
                    'Optional exemption resets to zero. In practice: transferred to retained earnings.', 'core', check=0, topic=T3),
                  M('k1c', 'The 2019 acquisition can be:', ['Left unrestated using the exemption', 'Must be restated', 'Deconsolidated', 'Treated as an asset purchase'], 0,
                    'Business combinations exemption. In practice: goodwill tested for impairment at transition.', 'core', topic=T3),
                  M('k1d', 'The ₹8 crore understatement is shown in the reconciliation as:', ['An error correction, separately identified', 'A policy change', 'An estimate change', 'Ignored'], 0,
                    'Errors are distinguished from policy changes. In practice: explain.', 'moderate', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch14', 1, 'Ind AS 101 "First-time Adoption of Ind AS"',
                ['Identify the transition date and prepare the opening Ind AS balance sheet.',
                 'Apply the mandatory exceptions to retrospective application.',
                 'Select and apply optional exemptions.',
                 'Prepare reconciliations and transition disclosures.'],
                {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 30}, 'prereq': ['fin-p1-ch13-u08'],
                 'exam_tip': 'Start every first-time adoption answer by fixing the transition date.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Transition date: start of earliest comparative period.',
                             'Opening balance sheet: recognise, derecognise, reclassify, measure.',
                             'Adjustments to retained earnings.',
                             'Mandatory exceptions stop hindsight.',
                             'Optional exemptions give relief; reconciliations required.'],
                 'remember': ['Three balance sheets in first Ind AS statements.'],
                 'traps': ['Using hindsight for estimates.']},
                [('Transition date', 'Start of comparatives'), ('Adjustments', 'Retained earnings'), ('Exceptions', 'Mandatory'), ('Exemptions', 'Optional')],
                viva, cases)
