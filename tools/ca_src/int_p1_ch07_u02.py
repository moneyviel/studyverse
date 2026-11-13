"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 7 Unit 2 — AS 5 Net Profit or Loss for the Period, Prior Period Items and Changes in Accounting Policies.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch07-u02'
T1 = 'Net profit, ordinary activities and extraordinary items'
T2 = 'Separately disclosed items within ordinary activities'
T3 = 'Prior period items'
T4 = 'Changes in accounting estimates'
T5 = 'Changes in accounting policies'


def build():
    ck = Checks()
    carry = ck.add('1000000-1000000/10*4', 'Carrying amount after 4 years (₹)')
    newdep = ck.add('600000/4', 'Revised annual depreciation (₹)')
    i1 = {'id': 'i1', 'title': 'Prior period item or estimate change?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'In 2026-27 Tanvi Ltd. found that (a) depreciation of ₹1,20,000 on a machine was omitted in 2025-26 by mistake; and (b) another machine (cost ₹10,00,000, life 10 years, no residual value, used for 4 years) now has only 4 more years of useful life. Show the treatment for 2026-27.',
          'solution': [table(['Item', 'Nature', 'Treatment'], [
              ['(a) Omitted depreciation', 'Prior period item — an error in last year\'s statements', 'Charge ₹1,20,000 in 2026-27 profit and loss, shown separately with its nature'],
              ['(b) Revised life', 'Change in estimate — new information, not an error', f'Carrying amount {inr(carry)} ÷ 4 = {inr(newdep)} a year from 2026-27']], title='AS 5')],
          'checks': list(ck)}

    ck2 = Checks()
    eff = ck2.add('980000-860000', 'Increase in closing inventory from the policy change (₹)')
    i2 = {'id': 'i2', 'title': 'Classifying unusual items', 'difficulty': 'core', 'minutes': 6,
          'q': 'Classify for Gauri Ltd.\'s 2026-27 statement of profit and loss: (a) its warehouse was compulsorily acquired by the government with compensation ₹40 lakh below book value; (b) inventory written down by ₹15 lakh to NRV; (c) a lawsuit settled for ₹6 lakh; (d) a switch from FIFO to weighted average required by a new standard, raising closing stock from ₹8,60,000 to ₹9,80,000.',
          'solution': [table(['Item', 'Classification', 'Treatment'], [
              ['(a) Compulsory acquisition', 'Extraordinary item', 'Show separately with nature and amount'],
              ['(b) Inventory write-down', 'Ordinary, but separately disclosed (size)', 'Disclose nature and amount'],
              ['(c) Lawsuit settlement', 'Ordinary, separately disclosed', 'Disclose nature and amount'],
              ['(d) Policy change', 'Change in accounting policy (required by standard)', f'Disclose and quantify the effect: profit higher by {inr(eff)}']], title='AS 5 classification')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'All items of income and expense recognised in a period are included in net profit or loss for that period unless a standard requires or permits otherwise.',
            'Net profit or loss has two parts: profit or loss from ordinary activities and extraordinary items, each presented in the statement of profit and loss itself.',
            'Ordinary activities are those undertaken as part of the business, plus related activities incidental to or arising from them.',
            'Extraordinary items arise from events clearly distinct from ordinary activities and are not expected to recur frequently or regularly — for example, attachment of property by the government or an earthquake. Their nature and amount are disclosed separately. Whether an item is extraordinary depends on the business: a flood loss is extraordinary for most firms but not for one that insures against floods.'],
          'Almost everything is ordinary; extraordinary items are rare and genuinely outside the business.',
          'A pharma company\'s loss on government seizure of its land is extraordinary; a fall in drug prices is not.'),
        C('c2', T2, [
            'Some ordinary items need separate disclosure of nature and amount because of their size, nature or incidence, so performance can be understood.',
            'Examples: write-down of inventories to NRV or of fixed assets to recoverable amount and reversals; restructurings and reversal of related provisions; disposals of fixed assets or long-term investments; legislative changes with retrospective effect; litigation settlements; and other reversals of provisions.'],
          'Ordinary, but big or odd enough to be pointed out.',
          'A large one-time inventory write-down appears as a separate line or note.'),
        C('c3', T3, [
            'Prior period items are income or expenses that arise in the current period because of errors or omissions in preparing one or more earlier periods\' statements.',
            'They are included in the current period\'s profit and loss, with their nature and amount disclosed separately, so their effect on current profit can be seen. They may be shown after ordinary profit or within the relevant expense with disclosure.',
            'They are rare. Items that relate to earlier periods but arise from new information or estimates — such as arrears of pay from a wage revision agreed this year — are not prior period items.'],
          'A prior period item is last year\'s mistake corrected this year, openly.',
          'A sales invoice of last year never recorded and discovered now is a prior period item.'),
        C('c4', T4, [
            'Many items need estimates — bad debts, inventory obsolescence, useful lives of assets, warranty costs. Estimates are revised as new information or experience arrives.',
            'The effect of a change in estimate is included in profit and loss of the period of change if it affects only that period, or of the period of change and later periods if it affects both — that is, prospectively.',
            'It is shown under the same classification used for the estimate before. A change in estimate is not a prior period item or an extraordinary item. Where it is hard to tell a policy change from an estimate change, it is treated as an estimate change with disclosure.'],
          'New information changes the future, not the past.',
          'Revising warranty cost per unit after better data affects this year\'s and future provisions only.'),
        C('c5', T5, [
            'A change in accounting policy is made only if required by statute, required by an accounting standard, or if it gives a more appropriate presentation of the financial statements.',
            'Adopting a policy for events that differ in substance from earlier ones, or for events not occurring before, is not a change in policy.',
            'Any change with a material effect is disclosed; its impact on the financial statements is quantified, or if not ascertainable, that fact is stated. A change with no material effect now but expected later is disclosed in the period of change.'],
          'Change a policy only for law, a standard or better presentation — and show the cost of the change.',
          'Switching inventory formula because a new standard requires it is a permitted policy change.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Closing review of the profit and loss', 'role': 'Audit assistant',
             'situation': 'The draft accounts show a "miscellaneous adjustments" line mixing last year\'s errors, revised estimates and a one-off natural disaster loss.',
             'steps': ['Separate errors (prior period) from new estimates.', 'Identify any truly extraordinary item.', 'Pick out large ordinary items for separate disclosure.', 'Check reasons for any policy change.'],
             'takeaway': 'Each kind of unusual item has its own presentation rule.'}]

    mcqs = [
        Q('m1', 'An extraordinary item arises from events that are:', ['Clearly distinct from ordinary activities and not expected to recur frequently', 'Large in amount', 'Related to prior years', 'Due to estimate revisions'], 0,
          'AS 5 defines extraordinary items by their nature: clearly distinct from ordinary activities and not expected to recur frequently or regularly. Size alone does not make an item extraordinary. In practice: they are rare.', 'c1', T1),
        Q('m2', 'Which is most likely an extraordinary item?', ['Loss from attachment of property by the government', 'Loss on sale of an old machine', 'Bad debts written off', 'Inventory write-down'], 0,
          'Government attachment of property is outside the normal business and not expected to recur. Sale of machinery, bad debts and inventory write-downs arise in ordinary activities. In practice: judge from the enterprise\'s viewpoint.', 'c1', T1),
        Q('m3', 'A large write-down of inventory to NRV is:', ['An ordinary item disclosed separately', 'An extraordinary item', 'A prior period item', 'A change in policy'], 0,
          'Write-downs are part of ordinary activities, but their size or nature may warrant separate disclosure of nature and amount under AS 5. In practice: show it in the notes or on the face.', 'c2', T2),
        Q('m4', 'Prior period items arise because of:', ['Errors or omissions in earlier periods\' financial statements', 'Revisions of estimates', 'New accounting standards', 'Wage arrears agreed this year'], 0,
          'Prior period items are incomes or expenses that surface this year because earlier statements contained mistakes or left something out. Estimate revisions and current agreements are not prior period items. In practice: they should be rare.', 'c3', T3),
        Q('m5', 'Prior period items under AS 5 are shown:', ['In the current period\'s profit and loss, disclosed separately', 'By restating last year\'s accounts', 'Directly in reserves', 'Only in the directors\' report'], 0,
          'AS 5 requires prior period items to be included in current profit and loss with their nature and amount disclosed separately, so their effect on current results is visible. In practice: show them after ordinary profit if helpful.', 'c3', T3),
        Q('m6', 'A change in the estimated useful life of an asset is applied:', ['Prospectively, in the current and future periods', 'Retrospectively', 'As a prior period item', 'As an extraordinary item'], 0,
          'A change in estimate affects the period of change and future periods where relevant; earlier figures are not restated. It is shown under the same classification as before. In practice: spread the remaining carrying amount.', 'c4', T4),
        Q('m7', 'Cost ₹6,00,000, life 6 years, no residual value; after 2 years the remaining life is revised to 2 years. New annual depreciation:', ['₹2,00,000', '₹1,00,000', '₹1,50,000', '₹3,00,000'], 0,
          'Carrying amount after 2 years is ₹4,00,000; spread over the revised remaining 2 years gives ₹2,00,000 a year. Nothing is restated for earlier years. In practice: disclose a material estimate change.', 'c4', T4, 'moderate', check=200000),
        Q('m8', 'A change in accounting policy is permitted when:', ['Required by statute or a standard, or it gives a more appropriate presentation', 'Profit needs to increase', 'The auditor changes', 'The tax rate changes'], 0,
          'AS 5 allows a policy change only for statute, an accounting standard, or a more appropriate presentation of events. Managing profits is never a valid reason. In practice: document the justification.', 'c5', T5),
        Q('m9', 'Adopting a policy for a new type of transaction not undertaken before is:', ['Not a change in accounting policy', 'A change in policy', 'A prior period item', 'An extraordinary item'], 0,
          'Picking a policy for transactions that are new, or substantially different from earlier ones, is not a change in policy. Only replacing an existing policy is. In practice: disclose the new policy.', 'c5', T5),
        Q('m10', 'Arrears of salary for earlier years paid under a wage agreement signed this year are:', ['Not prior period items, since the obligation arose this year', 'Prior period items', 'Extraordinary items', 'Changes in estimate'], 0,
          'The liability arises from an agreement made in the current period, not from an error in earlier statements, so it is a current expense, though it may be disclosed separately. In practice: explain it in notes.', 'c3', T3, 'moderate'),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Prior period item', 2, 'concept', 'prior period'),
           S('s2', 'Estimate change prospective', 2, 'computation', 'estimate', nums=[carry, newdep])],
          ['Ask: error or new information?'], ['Restating last year.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Extraordinary item', 1, 'concept', 'extraordinary'),
           S('s2', 'Separate disclosure items', 1.5, 'concept', 'separately'),
           S('s3', 'Policy change quantified', 1.5, 'computation', 'policy', nums=[eff])],
          ['Classify each item.'], ['Calling the write-down extraordinary.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What are extraordinary items?', 'Income or expenses from events clearly distinct from ordinary activities that happen only rarely.',
          [P('p1', 'Distinct from ordinary', 6, 'distinct'), P('p2', 'Rare', 4, 'rare')], 'c1'),
        V('v2', 'What are prior period items?', 'Income or expenses arising in the current period from errors or omissions in preparing earlier periods\' financial statements.',
          [P('p1', 'Errors or omissions', 6, 'error|omission'), P('p2', 'Earlier periods', 4, 'earlier|prior')], 'c3'),
        V('v3', 'How is a change in estimate accounted for?', 'Prospectively, in the profit and loss of the period of change and of future periods if they are also affected, under the same classification as before.',
          [P('p1', 'Prospectively', 6, 'prospective|future'), P('p2', 'Same classification', 4, 'classification')], 'c4'),
        V('v4', 'When may an accounting policy be changed?', 'When required by statute or an accounting standard, or when the change gives a more appropriate presentation of the financial statements.',
          [P('p1', 'Statute or standard', 6, 'statute|standard'), P('p2', 'Better presentation', 4, 'appropriate|presentation')], 'c5'),
        V('v5', 'Give two items within ordinary activities that may need separate disclosure.', 'Write-downs of inventory or fixed assets, restructuring costs, disposals of fixed assets or long-term investments, litigation settlements and reversals of provisions.',
          [P('p1', 'Write-downs or restructuring', 5, 'write-down|restructur'), P('p2', 'Disposals or litigation', 5, 'dispos|litigation|reversal')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Hemant Engineering Ltd.', 'difficulty': 'moderate',
              'case': 'Hemant Engineering Ltd. found in 2026-27 that a purchase invoice of ₹2,50,000 for 2025-26 had not been recorded. It also raised its bad debt estimate from 2% to 3% of debtors (₹40 lakh) after new market data, and changed its depreciation method on vehicles to better reflect usage.',
              'mcqs': [
                  M('k1a', 'The unrecorded invoice of ₹2,50,000 is:', ['A prior period item shown separately in 2026-27', 'Adjusted in 2025-26 accounts by reopening them', 'An extraordinary item', 'A change in estimate'], 0,
                    'An omission in last year\'s statements surfacing now is a prior period item, charged in the current year with separate disclosure of nature and amount. In practice: do not reopen approved accounts.', 'core', topic=T3),
                  M('k1b', 'Additional bad debt provision from the estimate change:', ['₹40,000', '₹1,20,000', '₹80,000', 'Nil'], 0,
                    'Raising the rate from 2% to 3% on ₹40 lakh adds 1% = ₹40,000, charged in the current year as a change in estimate under the same head as before. In practice: disclose if material.', 'moderate', check=40000, topic=T4),
                  M('k1c', 'The change in depreciation method is treated (under AS 10, consistent with AS 5) as:', ['A change in estimate, applied prospectively', 'A change in policy with restatement', 'A prior period item', 'An extraordinary item'], 0,
                    'AS 10 treats a change in depreciation method to reflect the pattern of consumption as a change in accounting estimate, applied prospectively; AS 5 then governs its disclosure. In practice: quantify the effect.', 'moderate', topic=T4),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch07', 2, 'Accounting Standard 5 Net Profit or Loss for the Period, Prior Period Items and Changes in Accounting Policies',
                ['Present ordinary and extraordinary items correctly.',
                 'Identify ordinary items needing separate disclosure.',
                 'Account for prior period items and changes in estimates.',
                 'Apply the rules for changes in accounting policies.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 20}, 'prereq': ['int-p1-ch07-u01'],
                 'exam_tip': 'Sort each unusual item: error (prior period), new information (estimate), outside business (extraordinary), or big ordinary item (separate disclosure).'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['All income and expense in net profit unless a standard says otherwise.', 'Extraordinary: distinct and rare; shown separately.',
                             'Separate disclosure for large or unusual ordinary items.', 'Prior period items: errors of earlier periods; in current P&L, disclosed.',
                             'Estimate changes: prospective, same classification.', 'Policy changes: statute, standard or better presentation; quantify effect.'],
                 'remember': ['Estimate changes are never prior period items.'],
                 'traps': ['Size alone does not make an item extraordinary.']},
                [('Prior period item', 'Current P&L, disclosed'), ('Estimate change', 'Prospective'), ('Policy change', 'Statute · standard · better presentation')],
                viva, cases)
