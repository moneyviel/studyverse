"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 4 Unit 1 — AS 1 Disclosure of Accounting Policies.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch04-u01'
T1 = 'Fundamental accounting assumptions'
T2 = 'What accounting policies are'
T3 = 'Choosing a policy: prudence, substance over form, materiality'
T4 = 'Disclosing policies and changes in them'
T5 = 'Departures from the fundamental assumptions'


def build():
    ck = Checks()
    eff = ck.add('1240000-1160000', 'Fall in closing inventory on moving to weighted average (₹)')
    prof = ck.add('5600000-80000', 'Revised profit (₹)')
    i1 = {'id': 'i1', 'title': 'A change in the inventory formula', 'difficulty': 'core', 'minutes': 6,
          'q': 'Kalpana Ltd. switched from FIFO to weighted average cost for inventory in 2026-27 to match its group. Closing inventory is ₹12,40,000 under FIFO and ₹11,60,000 under weighted average; profit after the change is ₹55,20,000. What must be disclosed under AS 1?',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Effect on closing inventory', '12,40,000 − 11,60,000', inr(eff)],
              ['Profit had FIFO continued', '55,20,000 + 80,000', inr(5600000)],
              ['Profit reported', '', inr(prof)]], title='Quantifying the change'),
              p('Disclose the change from FIFO to weighted average, the reason, and that profit for the year and inventory are lower by ₹80,000. If the effect could not be worked out, the fact would be stated instead.')],
          'checks': list(ck)}

    ck2 = Checks()
    dep = ck2.add('900000*10/100', 'Depreciation on the old basis (₹)')
    i2 = {'id': 'i2', 'title': 'Is it a policy change?', 'difficulty': 'moderate', 'minutes': 5,
          'q': 'Classify each as a change in accounting policy or not, and say what to disclose: (a) Sutlej Ltd. now values inventory at lower of cost and NRV instead of at cost, (b) it starts leasing vans for the first time, (c) it revises the useful life of machinery (cost ₹9,00,000) from 10 to 8 years.',
          'solution': [table(['Case', 'Policy change?', 'Treatment'], [
              ['(a) Cost → lower of cost and NRV', 'Yes', 'Disclose the change, reason and quantified effect'],
              ['(b) New type of transaction', 'No — first adoption for a new event', 'Disclose the policy adopted'],
              ['(c) Useful life revision', f'No — a change in estimate (old charge ₹{R(dep)} a year)', 'Account prospectively; disclose as an estimate change']], title='Policy vs not'),
              note('A policy for events that did not occur before, or that differ in substance from earlier ones, is not a change in policy.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'AS 1 names three fundamental accounting assumptions: going concern (the business will continue for the foreseeable future, with no need or intention to liquidate or sharply cut operations), consistency (policies stay the same from period to period) and accrual (revenues and costs are recorded when earned or incurred, not when cash moves).',
            'If these assumptions are followed, they need not be disclosed — users take them for granted. Only a departure must be disclosed.'],
          'The three assumptions are the ground rules every reader takes for granted.',
          'A company that is closing down next month cannot value its machinery as if it will run for ten more years.'),
        C('c2', T2, [
            'Accounting policies are the specific principles and methods of applying them that an enterprise adopts in preparing and presenting financial statements.',
            'There is no single list for every situation. Common areas where enterprises choose differently: depreciation methods, inventory cost formulas, valuation of investments, treatment of goodwill, retirement benefits, translation of foreign currency items, recognition of profit on long-term contracts and fixed assets valuation.',
            'Because policies differ, comparisons between enterprises are meaningful only if the policies used are disclosed.'],
          'Two companies with identical trade can report different profits simply through different policies.',
          'One retailer uses FIFO and another weighted average: their margins are not directly comparable without disclosure.'),
        C('c3', T3, [
            'The overriding aim in selecting a policy is that the statements present the financial position and results truly and fairly.',
            'Prudence: gains are booked only once realised (cash need not have arrived), never in advance; all known liabilities and losses are provided for, even if only estimated.',
            'Substance over form: transactions are accounted for by their substance and financial reality, not merely their legal form.',
            'Materiality: statements should disclose all items whose knowledge might influence the decisions of users.'],
          'Choose the policy that tells the truth fairly — cautiously, by substance, and leaving out nothing that matters.',
          'A hire-purchase asset is shown as the buyer\'s asset even before legal title passes — substance over form.'),
        C('c4', T4, [
            'All significant accounting policies adopted should be disclosed, normally in one place, as part of the financial statements.',
            'Disclosing a policy does not cure a wrong or inappropriate treatment in the accounts.',
            'A change in policy that has a material effect in the current period is disclosed with the amount of its effect on the financial statements, to the extent it can be determined; if it cannot, that fact is stated.',
            'If a change hardly affects this year but will clearly matter in future years, it is disclosed in the year the change is made.'],
          'Show your rules in one place, and if you change one, show the price of the change.',
          'A note saying "depreciation not provided" does not make the omission acceptable.'),
        C('c5', T5, [
            'Where any of the three assumptions has been set aside, the statements must say so and explain why.',
            'For example, if going concern is no longer valid, assets are shown at realisable values and the basis is explained.'],
          'Silence means the assumptions hold; any departure must be spelt out.',
          'A company preparing accounts on a cash basis for one year must disclose that accrual was not followed.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Drafting the policies note', 'role': 'Audit assistant',
             'situation': 'A client\'s draft accounts have policies scattered across several notes and one change not quantified.',
             'steps': ['Gather all significant policies into one note.', 'Identify the change and compute its effect.', 'Check whether any assumption was departed from.'],
             'takeaway': 'One clear note with quantified changes is what AS 1 expects.'}]

    mcqs = [
        Q('m1', 'Which is NOT a fundamental accounting assumption under AS 1?', ['Prudence', 'Going concern', 'Consistency', 'Accrual'], 0,
          'AS 1 treats going concern, consistency and accrual as fundamental assumptions. Prudence is one of the considerations used to select accounting policies, along with substance over form and materiality. In practice: keep the two lists apart.', 'c1', T1),
        Q('m2', 'If the fundamental accounting assumptions are followed, they:', ['Need not be disclosed', 'Must be disclosed in one place', 'Must be disclosed with reasons', 'Must be disclosed by the auditor'], 0,
          'They are assumed by users, so following them needs no mention; only a departure must be disclosed, with reasons. Accounting policies, by contrast, must always be disclosed. In practice: look for any note of departure.', 'c1', T1),
        Q('m3', 'Accounting policies are best described as:', ['Specific principles and methods of applying them adopted in preparing statements', 'Estimates of useful lives', 'Assumptions about the future', 'Legal requirements under the Companies Act'], 0,
          'AS 1 defines accounting policies as the specific principles and the methods of applying them that an enterprise adopts in preparing and presenting its financial statements. Estimates and assumptions are different matters. In practice: check what can vary between firms.', 'c2', T2),
        Q('m4', 'Recognising a loss as soon as it is foreseen, but not a profit until realised, reflects:', ['Prudence', 'Materiality', 'Consistency', 'Substance over form'], 0,
          'Prudence means gains are booked only once realised, never in advance, while all known liabilities and losses are provided for even when estimated. It guards against overstating results. In practice: it does not permit secret reserves.', 'c3', T3),
        Q('m5', 'Showing a leased asset by its economic reality rather than its legal ownership reflects:', ['Substance over form', 'Prudence', 'Going concern', 'Accrual'], 0,
          'Substance over form requires transactions to be accounted for by their substance and financial reality, not merely their legal form. This is why the economic owner may show the asset. In practice: read contracts for real risks and rewards.', 'c3', T3),
        Q('m6', 'Disclosure of a wrong accounting treatment:', ['Does not make the treatment correct', 'Cures the error', 'Is required only for listed companies', 'Is optional'], 0,
          'AS 1 states that disclosing a policy does not remedy an incorrect or inappropriate treatment in the accounts. The treatment itself must be corrected. In practice: auditors qualify such cases despite the note.', 'c4', T4),
        Q('m7', 'A change in policy with a material effect is disclosed with its effect:', ['Quantified to the extent ascertainable; otherwise the fact is stated', 'Only in words', 'Only if it increases profit', 'Only in the next year'], 0,
          'The amount by which items are affected is disclosed to the extent it can be determined; where it cannot, the enterprise states that fact. Reasons for the change are also given. In practice: show the before-and-after figure.', 'c4', T4, 'moderate'),
        Q('m8', 'A change in policy with no material effect now but a likely material effect later is disclosed:', ['In the period in which the change is adopted', 'Only when the effect becomes material', 'Never', 'In the directors\' report only'], 0,
          'AS 1 requires disclosure in the period of adoption where a change will probably matter in future years though not now, so users are alerted early. In practice: describe the expected impact.', 'c4', T4, 'moderate'),
        Q('m9', 'Revising the estimated useful life of a machine is:', ['A change in accounting estimate, not policy', 'A change in accounting policy', 'A departure from consistency', 'A prior period item'], 0,
          'Useful life is an estimate that is reviewed as conditions change; revising it is a change in estimate, accounted for prospectively. A change of depreciation method, by contrast, follows AS 10 rules. In practice: disclose material estimate changes.', 'c4', T4),
        Q('m10', 'If accounts are not prepared on a going concern basis, the enterprise must:', ['Disclose the fact with reasons', 'Do nothing special', 'Restate the previous year', 'Obtain court approval'], 0,
          'Any departure from a fundamental accounting assumption must be disclosed, with reasons. Assets would usually be shown at realisable values and the basis explained. In practice: this is a key audit matter.', 'c5', T5),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Effect computed', 2, 'computation', 'weighted', nums=[eff]),
           S('s2', 'Disclosure of change and reason', 2, 'concept', 'disclose', 'reason')],
          ['Quantify the effect.'], ['Disclosing only in words.'], ['Table + note.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'NRV change is a policy change', 1.5, 'concept', 'nrv'),
           S('s2', 'New transaction not a change', 1, 'concept', 'new'),
           S('s3', 'Useful life is an estimate', 1.5, 'concept', 'estimate')],
          ['Classify before treating.'], ['Treating new events as policy changes.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Name the fundamental accounting assumptions.', 'Going concern, consistency and accrual.',
          [P('p1', 'Going concern', 4, 'going concern'), P('p2', 'Consistency and accrual', 6, 'consistency', 'accrual')], 'c1'),
        V('v2', 'What three considerations guide the selection of accounting policies?', 'Prudence, substance over form and materiality.',
          [P('p1', 'Prudence', 3, 'prudence'), P('p2', 'Substance over form', 4, 'substance'), P('p3', 'Materiality', 3, 'material')], 'c3'),
        V('v3', 'Where should significant accounting policies be disclosed?', 'All significant policies should be disclosed together in one place as part of the financial statements.',
          [P('p1', 'One place', 6, 'one place'), P('p2', 'Part of statements', 4, 'financial statements')], 'c4'),
        V('v4', 'Why must accounting policies be disclosed?', 'Because enterprises may choose different acceptable policies, users need to know them to understand and compare financial statements.',
          [P('p1', 'Differing policies', 5, 'different|differ'), P('p2', 'Comparability', 5, 'compar|understand')], 'c2'),
        V('v5', 'What is the rule for a change in accounting policy?', 'Disclose any change with a material effect along with the amount of the effect, or state that it cannot be determined; disclose in the year of change if a material effect is expected later.',
          [P('p1', 'Amount of effect', 6, 'amount|effect'), P('p2', 'Later material effect', 4, 'later')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Meghna Traders Ltd.', 'difficulty': 'moderate',
              'case': 'Meghna Traders Ltd. changed its depreciation method on office equipment, increasing depreciation by ₹1,20,000. It did not provide for a disputed customs duty claim of ₹3,00,000 that is likely to be payable, but disclosed it in a note. Its policies note is spread across five separate notes.',
              'mcqs': [
                  M('k1a', 'Not providing for the likely customs duty, while disclosing it, is:', ['Not acceptable — prudence requires a provision, and disclosure does not cure it', 'Acceptable because it is disclosed', 'Required by consistency', 'A change in policy'], 0,
                    'Known liabilities and losses must be provided for even if estimated. AS 1 states that disclosure of a wrong treatment does not remedy it. In practice: provide ₹3,00,000.', 'core', topic=T3),
                  M('k1b', 'The effect of the depreciation method change to be disclosed:', ['₹1,20,000', '₹3,00,000', 'Nil', '₹4,20,000'], 0,
                    'A change with a material effect is disclosed with the amount by which the statements are affected — here the additional depreciation of ₹1,20,000. In practice: state the reason as well.', 'moderate', check=120000, topic=T4),
                  M('k1c', 'Spreading the policies over five notes:', ['Is contrary to AS 1, which expects them in one place', 'Is required', 'Is acceptable for listed companies only', 'Has no bearing'], 0,
                    'AS 1 requires significant accounting policies to be disclosed in one place, so readers can see them together. Separate scattered notes should be consolidated. In practice: use a single "Significant accounting policies" note.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch04', 1, 'Accounting Standard 1 Disclosure of Accounting Policies',
                ['Explain the three fundamental accounting assumptions and when they must be disclosed.',
                 'Explain what accounting policies are and the considerations in selecting them.',
                 'Apply the disclosure rules for policies and changes in them.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 20}, 'prereq': ['int-p1-ch03-u01'],
                 'exam_tip': 'Separate assumptions (going concern, consistency, accrual) from selection considerations (prudence, substance over form, materiality).'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Assumptions: going concern, consistency, accrual — disclose only if not followed.',
                             'Policies: principles + methods; disclose all significant ones in one place.',
                             'Selection: prudence, substance over form, materiality; aim for true and fair view.',
                             'Changes: disclose with quantified effect, or state it cannot be determined.'],
                 'remember': ['Disclosure does not cure a wrong treatment.'],
                 'traps': ['A change in estimate is not a change in policy.']},
                [('Assumptions', 'Going concern · consistency · accrual'), ('Selection', 'Prudence · substance · materiality'), ('Change', 'Disclose with amount')],
                viva, cases)
