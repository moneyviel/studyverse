"""CA Final · Paper 1 Financial Reporting · Chapter 4 Unit 1 Ind AS 8 Accounting Policies, Changes in Accounting Estimates and Errors.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch04-u01'
T1 = 'Selecting and applying accounting policies'
T2 = 'Changes in accounting policies'
T3 = 'Changes in accounting estimates'
T4 = 'Prior period errors'


def build():
    ck = Checks()
    cv = ck.add('100-3*10', 'Carrying amount at start of year 4 (₹ lakh)')
    dep = ck.add('70/(8-3)', 'Revised annual depreciation (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Life of a machine revised', 'difficulty': 'core', 'minutes': 6,
          'q': 'A machine cost ₹100 lakh, life 10 years, nil residual, straight-line. At the start of year 4 management concludes the total useful life is only 8 years. Compute depreciation for year 4 and explain the treatment.',
          'solution': [table(['Step', 'Working', '₹ lakh'], [
              ['Carrying amount at start of year 4', '100 − 3 × 10', inr(cv)],
              ['Remaining life', '8 − 3', '5 years'],
              ['Depreciation from year 4', '70 ÷ 5', inr(dep)]], title='Change in accounting estimate'),
              note('This is a change in estimate — applied prospectively from year 4. Earlier years are not restated; the effect is disclosed.')],
          'checks': list(ck)}

    ck2 = Checks()
    pat = ck2.add('10*(1-25/100)', 'Reduction in 2025-26 profit after tax (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Correcting last year\'s error', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'While preparing 2026-27 statements, Ruby Ltd. discovers that depreciation of ₹10 lakh for 2025-26 was omitted (material). Tax rate 25%; assume the tax effect is a deferred tax adjustment. How is it corrected and what is the effect on retained earnings at 1 April 2026?',
          'solution': [table(['Item', 'Correction in comparative 2025-26 figures'], [
              ['Depreciation expense', 'Increase by ₹10 lakh'],
              ['Property, plant and equipment', 'Decrease by ₹10 lakh'],
              ['Deferred tax', 'Reduce deferred tax liability (or create asset) by ₹2.5 lakh; tax expense down ₹2.5 lakh'],
              ['Profit after tax 2025-26', 'Lower by ₹' + str(pat) + ' lakh'],
              ['Retained earnings at 1 April 2026', 'Lower by ₹' + str(pat) + ' lakh']], title='Retrospective restatement'),
              note('The correction is made in the first statements approved after discovery by restating comparatives; it is not passed through 2026-27 profit. A third balance sheet may be needed if the opening position of the comparative period is materially affected.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Accounting policies are the particular principles and practices an entity has chosen for preparing and presenting its statements. Where an Ind AS applies to an item, its requirements (with application guidance that forms part of it) are followed.',
            'Where no Ind AS applies, management uses judgement to develop a policy that gives relevant and reliable information, referring in order to: Ind AS dealing with similar issues; then the definitions, recognition criteria and measurement concepts in the Conceptual Framework. Management may also consider the most recent pronouncements of the IASB, and of other standard-setters with a similar framework, accepted industry practice and literature, if consistent with the above.',
            'Policies are applied consistently to similar transactions unless an Ind AS requires or permits categorisation with different policies.'],
          'When the rulebook is silent, Ind AS 8 tells you where to look and in what order.',
          'A company accounting for a new kind of carbon credit first looks for a similar Ind AS before using the Framework.'),
        C('c2', T2, [
            'A policy is changed only if an Ind AS requires it, or if the change results in reliable and more relevant information. Applying a policy to new transactions that differ in substance, or that were immaterial before, is not a change in policy.',
            'A change from an Ind AS is applied using its transitional provisions; otherwise retrospectively, by adjusting the opening equity of the earliest period presented and restating comparatives, as if the new policy had always applied.',
            'If retrospective application is impracticable for particular periods, the change is applied from the earliest period for which it is practicable; if not practicable at all, prospectively from the earliest practicable date. Disclosures include the nature, reasons and amounts of adjustment. The initial application of a revaluation policy under Ind AS 16 or Ind AS 38 is dealt with as a revaluation under those standards, not under Ind AS 8.'],
          'A policy change rewrites history so that every period presented is on the same basis.',
          'Switching from FIFO to weighted average cost requires restating comparative inventory and cost of sales.'),
        C('c3', T3, [
            'Accounting estimates are monetary amounts in the statements subject to measurement uncertainty — e.g. expected credit losses, net realisable value, fair values, useful lives and depreciation patterns, warranty provisions. They are developed using measurement techniques and inputs.',
            'A change in estimate results from new information or developments and is not a correction of an error. Its effect is recognised prospectively in profit or loss of the period of change and future periods affected, or by adjusting the related asset, liability or equity item.',
            'When it is difficult to tell whether a change is in policy or estimate, it is treated as a change in estimate. Changing a measurement technique or input is a change in estimate unless it corrects an error.'],
          'Estimates are updated going forward; they never reopen past periods.',
          'Revising the expected warranty rate from 2% to 3% affects this year\'s provision only.'),
        C('c4', T4, [
            'Prior period errors are omissions or misstatements in past statements from failure to use, or misuse of, reliable information that was available and could reasonably have been obtained — including mathematical mistakes, misapplying policies, oversights, misinterpretation and fraud.',
            'Material errors are corrected retrospectively in the first set of statements approved after discovery: restating comparatives for the period in which the error occurred, or, where the error is older, adjusting the opening assets, liabilities and equity of the first period shown.',
            'If impracticable, correction is from the earliest practicable date. Disclosures cover the nature of the error, the correction for each line item and EPS for each prior period presented, and the correction at the beginning of the earliest period. Hindsight is not used when estimating amounts for prior periods.'],
          'Errors are fixed in the past where they happened, not hidden in this year\'s profit.',
          'An unrecorded sales return discovered next year is corrected by restating last year\'s revenue.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Is it a policy, estimate or error?', 'role': 'Audit senior',
             'situation': 'The client proposes several year-end "adjustments" to last year\'s figures.',
             'steps': ['Classify each as policy change, estimate change or error.', 'Check the justification for any policy change.', 'Apply retrospective or prospective treatment.', 'Draft the required disclosures.'],
             'takeaway': 'Classification decides whether comparatives are restated — get it right first.'}]

    mcqs = [
        Q('m1', 'Where no Ind AS applies, management first refers to:', ['Ind AS dealing with similar and related issues', 'US GAAP', 'Industry practice', 'Tax rules'], 0,
          'The hierarchy starts with analogous Ind AS, then the Framework; other sources may be considered if consistent. In practice: document the judgement.', 'c1', T1),
        Q('m2', 'A voluntary change in accounting policy is allowed only if it:', ['Gives reliable and more relevant information', 'Increases profit', 'Is simpler', 'Matches tax rules'], 0,
          'Ind AS 8 permits voluntary changes only on this ground. In practice: disclose reasons.', 'c2', T2),
        Q('m3', 'Changing a depreciation method from straight-line to diminishing balance is treated as:', ['A change in accounting estimate', 'A change in accounting policy', 'An error', 'A prior period item'], 0,
          'Ind AS 16 treats it as a change in estimate, applied prospectively. In practice: reflects changed pattern of consumption.', 'c3', T3),
        Q('m4', 'A change in accounting estimate is applied:', ['Prospectively', 'Retrospectively with restatement', 'Through opening retained earnings only', 'Not at all'], 0,
          'Effects are recognised in the current and future periods. In practice: disclose the effect if practicable.', 'c3', T3),
        Q('m5', 'A material prior period error is corrected:', ['Retrospectively in the first statements approved after discovery', 'In current year profit', 'Only in notes', 'Prospectively'], 0,
          'Comparatives or opening balances are restated. In practice: disclose line-item effects.', 'c4', T4),
        Q('m6', 'Applying a policy to transactions that differ in substance from earlier ones is:', ['Not a change in accounting policy', 'A change in policy', 'An error', 'A change in estimate'], 0,
          'New kinds of transactions need a policy; that is not a change. In practice: disclose the new policy.', 'c2', T2),
        Q('m7', 'If it is unclear whether a change is in policy or estimate, it is treated as:', ['A change in estimate', 'A change in policy', 'An error', 'Not disclosed'], 0,
          'Ind AS 8 resolves doubt in favour of estimate treatment. In practice: prospective application.', 'c3', T3),
        Q('m8', 'First adoption of the revaluation model for PPE is accounted for:', ['As a revaluation under Ind AS 16, not under Ind AS 8', 'Retrospectively under Ind AS 8', 'As an error', 'As a change in estimate'], 0,
          'Ind AS 8 excludes this from its retrospective rules. In practice: revaluation surplus goes to OCI.', 'c2', T2),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Carrying amount', 1, 'computation', 'carrying', nums=[cv]), S('s2', 'Remaining life', 1, 'concept', 'remaining'), S('s3', 'Depreciation and treatment', 2, 'computation', 'prospective', nums=[dep])],
          ['Use remaining life.'], ['Restating earlier years.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Retrospective restatement', 2, 'concept', 'restat|retrospective'), S('s2', 'Tax effect', 1.5, 'concept', 'deferred tax'), S('s3', 'Retained earnings', 1.5, 'computation', 'retained', nums=[pat])],
          ['Show both comparative and opening effects.'], ['Charging the error to current profit.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'When can an entity change an accounting policy?', 'When an Ind AS requires it, or when the change produces reliable and more relevant information.',
          [P('p1', 'Required by Ind AS', 5, 'requir'), P('p2', 'More relevant', 5, 'relevant')], 'c2'),
        V('v2', 'How is a change in policy applied?', 'Retrospectively, adjusting opening equity of the earliest period presented and restating comparatives, unless transitional provisions or impracticability apply.',
          [P('p1', 'Retrospective', 5, 'retrospective'), P('p2', 'Opening equity and comparatives', 5, 'opening|comparative')], 'c2'),
        V('v3', 'What is an accounting estimate?', 'A monetary amount in the statements that involves measurement uncertainty, such as an expected credit loss, useful life or provision.',
          [P('p1', 'Measurement uncertainty', 6, 'uncertain'), P('p2', 'Examples', 4, 'credit loss|useful life|provision|fair value')], 'c3'),
        V('v4', 'What is a prior period error?', 'An omission or misstatement in earlier statements caused by failing to use, or misusing, reliable information that was available when those statements were approved.',
          [P('p1', 'Omission or misstatement', 5, 'omission|misstat'), P('p2', 'Information available', 5, 'available|reliable')], 'c4'),
        V('v5', 'Can hindsight be used when restating prior periods?', 'Hindsight is avoided; estimates for prior periods reflect information that existed at that time.',
          [P('p1', 'Avoided', 5, 'avoid'), P('p2', 'Information then', 5, 'existed|at that time')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Granite Pharma Ltd.', 'difficulty': 'moderate',
              'case': 'Granite Pharma Ltd. (year ending 31 March 2027) finds: (i) the expected credit loss rate on receivables needs revision from 2% to 4% due to new market data; (ii) last year\'s inventory was overstated by ₹15 crore owing to a counting error (material); (iii) it decides to change from FIFO to weighted average because it reflects consumption better; (iv) it starts leasing out a building for the first time and adopts the cost model for investment property.',
              'mcqs': [
                  M('k1a', 'Point (i) is:', ['A change in estimate, applied prospectively', 'A policy change', 'An error', 'No change'], 0,
                    'New information changes the estimate. In practice: adjust the current-year allowance.', 'core', topic=T3),
                  M('k1b', 'Point (ii) is corrected by:', ['Restating 2025-26 comparatives and opening balances', 'Charging 2026-27 profit', 'A note only', 'Prospective adjustment'], 0,
                    'A material prior period error is corrected retrospectively. In practice: last year\'s cost of sales rises.', 'moderate', topic=T4),
                  M('k1c', 'Point (iii) is:', ['A voluntary change in accounting policy applied retrospectively', 'A change in estimate', 'An error', 'Not permitted'], 0,
                    'Inventory cost formula is a policy; voluntary change needs more relevant information and is retrospective. In practice: disclose reasons.', 'moderate', topic=T2),
                  M('k1d', 'Point (iv) is:', ['Not a change in policy — a new type of transaction', 'A change in policy', 'An error', 'A change in estimate'], 0,
                    'Applying a policy to transactions not previously occurring is not a change. In practice: disclose the new policy.', 'moderate', topic=T2),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch04', 1, 'Ind AS 8 "Accounting Policies, Changes in Accounting Estimates and Errors"',
                ['Select accounting policies, including where no Ind AS applies.',
                 'Account for changes in accounting policies.',
                 'Account for changes in accounting estimates.',
                 'Correct prior period errors.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 30}, 'prereq': ['fin-p1-ch03-u03'],
                 'exam_tip': 'First label the item — policy, estimate or error — and the treatment follows almost automatically.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Hierarchy: Ind AS → similar Ind AS → Framework → other pronouncements (if consistent).',
                             'Policy change: required or more relevant; retrospective unless impracticable.',
                             'Estimate change: prospective; doubt → estimate.',
                             'Errors: retrospective in first statements after discovery.'],
                 'remember': ['New types of transactions are not policy changes.'],
                 'traps': ['Depreciation method change is an estimate change.']},
                [('Policy change', 'Retrospective'), ('Estimate change', 'Prospective'), ('Error', 'Retrospective restatement'), ('Doubt', 'Treat as estimate')],
                viva, cases)
