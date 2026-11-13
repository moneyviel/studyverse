"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 4 Unit 6 — AS 24 Discontinuing Operations.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch04-u06'
T1 = 'What counts as a discontinuing operation'
T2 = 'The initial disclosure event'
T3 = 'Recognition and measurement'
T4 = 'Initial and updating disclosures'
T5 = 'Presentation, comparatives and interim reports'


def build():
    ck = Checks()
    pbt = ck.add('450-520', 'Pre-tax result of the discontinuing operation (₹ lakh)')
    tax = ck.add('70*30/100', 'Tax saving at 30% (₹ lakh)')
    net = ck.add('-70+21', 'Post-tax result (₹ lakh)')
    imp = ck.add('260-200', 'Impairment loss under AS 28 (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Figures for the discontinuing division', 'difficulty': 'core', 'minutes': 8,
          'q': 'Tara Ltd. decided to close its footwear division (a separate major line of business). For the year, the division\'s revenue was ₹450 lakh and expenses ₹520 lakh; tax rate is 30%. Its plant has a carrying amount of ₹260 lakh and a recoverable amount of ₹200 lakh. Work out the amounts to be disclosed.',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Revenue', '', R(450)],
              ['Expenses', '', '(520)'],
              ['Pre-tax loss from ordinary activities', '450 − 520', R(pbt)],
              ['Related tax saving', '30% of 70', R(tax)],
              ['Post-tax loss', '', R(net)],
              ['Impairment loss on plant (AS 28)', '260 − 200', R(imp)]], title='AS 24 amounts'),
              p('AS 24 itself does not set measurement rules: the impairment follows AS 28 and any closure provisions follow AS 29. Disclose also the carrying amounts of assets and liabilities to be disposed of and the division\'s net cash flows by activity.')],
          'checks': list(ck)}

    ck2 = Checks()
    days = ck2.add('31-10', 'Days from 10 March to 31 March')
    i2 = {'id': 'i2', 'title': 'When does disclosure start?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Ganga Ltd. (year ends 31 March 2027) approved a detailed formal plan to sell its hotel business on 15 February 2027 and announced it publicly on 10 March 2027. It signed a binding sale agreement on 5 April 2027; the statements were approved on 20 May 2027. In which year\'s statements do AS 24 disclosures begin?',
          'solution': [table(['Date', 'Event', 'Significance'], [
              ['15 Feb 2027', 'Board approves detailed plan', 'Not enough on its own'],
              ['10 Mar 2027', 'Plan announced', f'Initial disclosure event — the plan is both approved and announced ({R(days)} days before year end)'],
              ['5 Apr 2027', 'Binding agreement', 'Later than the announcement'],
              ['20 May 2027', 'Statements approved', '—']], title='Initial disclosure event'),
              p('The initial disclosure event (10 March) falls within 2026-27, so the full initial disclosures are made in the 2026-27 statements. Had both events occurred after 31 March but before approval, only the description of the event would be disclosed then.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A discontinuing operation is a part of the business that, under a single plan, is being disposed of substantially in its entirety (by sale, demerger or spin-off), disposed of piecemeal, or terminated through abandonment.',
            'It must represent a distinct major business line or geographical area of operations, and be distinguishable operationally and for financial reporting — its assets, liabilities, revenue and expenses can be attributed to it.',
            'A gradual phase-out of a product line, a shift in production location, or closing a few outlets without leaving the business line is not a discontinuing operation. A business or geographical segment under AS 17 normally meets the "separate major line" test.'],
          'Leaving a whole line of business under one plan — not trimming it.',
          'Closing all hotels in a group that also runs airlines is discontinuing; shutting two of forty hotels is not.'),
        C('c2', T2, [
            'The initial disclosure event is the earlier of: (a) the enterprise entering into a binding sale agreement for substantially all the assets of the operation; or (b) the board or similar body both approving a detailed formal plan for discontinuance and announcing the plan.',
            'A detailed formal plan identifies the business, main assets, expected sale method, period of completion and principal locations affected.',
            'If the event occurs after the year end but before the Board approves the statements, the statements give only the disclosures about the plan as a non-adjusting event.'],
          'Disclosure starts when the decision becomes binding or public, whichever is first.',
          'A board decision kept confidential does not trigger AS 24 until it is announced or a sale is signed.'),
        C('c3', T3, [
            'AS 24 is a presentation and disclosure standard. Recognition and measurement follow other standards: AS 28 for impairment of assets, AS 29 for provisions such as termination costs, and so on.',
            'A discontinuing operation is not an extraordinary item; its income and expense are part of ordinary activities.'],
          'AS 24 tells you how to show it; other standards tell you how to measure it.',
          'Severance pay for staff of a closing division is provided under AS 29 when an obligation arises.'),
        C('c4', T4, [
            'Initial disclosures, from the period of the initial disclosure event: a description; the business or geographical segment; the date and nature of the event; expected timing of completion; carrying amounts of total assets and liabilities to be disposed of; revenue, expenses and pre-tax profit or loss from ordinary activities with related tax; and net cash flows from operating, investing and financing activities.',
            'When assets are sold or liabilities settled, disclose the gain or loss recognised and the related tax, and the net selling prices from binding agreements with the expected timing of receipts.',
            'Updating disclosures continue in later periods until completion, including significant changes in amount or timing. If the plan is abandoned, that fact and its effect are disclosed.'],
          'Tell the full story when it starts, and keep updating it until it ends.',
          'If a buyer backs out and the plan is dropped, the reversal is disclosed.'),
        C('c5', T5, [
            'The required disclosures are shown separately for each discontinuing operation. The pre-tax gain or loss on disposal of assets or settlement of liabilities, and the related tax, appear in the statement of profit and loss itself; other disclosures may be in notes.',
            'Comparative information for prior periods presented is restated to separate continuing and discontinuing assets, liabilities, income, expenses and cash flows.',
            'Interim financial reports also include the description, date, completion timing and changes during the interim period.'],
          'Readers must be able to compare what continues with what is going away.',
          'Last year\'s revenue is split into continuing and discontinuing parts in this year\'s report.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Board decides to exit a business', 'role': 'Reporting analyst',
             'situation': 'The board has approved selling the logistics division; an announcement is planned next week.',
             'steps': ['Confirm the division is a separate major line.', 'Fix the initial disclosure event date.', 'Gather revenue, expenses, cash flows and carrying amounts.', 'Apply AS 28 and AS 29 for impairment and provisions.'],
             'takeaway': 'Dates and boundaries drive the disclosures.'}]

    mcqs = [
        Q('m1', 'Which is a discontinuing operation?', ['Closing the entire pharmaceuticals business of a diversified group under one plan', 'Phasing out an old model of a car', 'Moving a factory to another state', 'Closing three of fifty retail stores'], 0,
          'A discontinuing operation must be a distinct major business line or geographical area disposed of or abandoned under a single plan. Product phase-outs, relocations and minor closures do not qualify. In practice: check the segment structure.', 'c1', T1),
        Q('m2', 'The initial disclosure event is:', ['The earlier of a binding sale agreement and approval plus announcement of a detailed plan', 'The date the plan is first discussed', 'The date the last asset is sold', 'The year end'], 0,
          'AS 24 fixes the initial disclosure event as whichever comes first: entering a binding sale agreement for substantially all assets, or the board approving and announcing a detailed formal plan. In practice: an unannounced approval is not enough.', 'c2', T2),
        Q('m3', 'Measurement of losses on a discontinuing operation follows:', ['Other standards such as AS 28 and AS 29', 'AS 24\'s own measurement rules', 'Tax rules', 'Market value only'], 0,
          'AS 24 is about presentation and disclosure; it uses the recognition and measurement rules of other standards — impairment under AS 28 and provisions under AS 29. In practice: compute these first.', 'c3', T3),
        Q('m4', 'Income from a discontinuing operation is:', ['Part of ordinary activities, not an extraordinary item', 'An extraordinary item', 'A prior period item', 'Shown in reserves'], 0,
          'AS 24 states that discontinuing operations rarely meet the definition of extraordinary items; their results are part of ordinary activities but disclosed separately. In practice: do not put them below the line.', 'c3', T3),
        Q('m5', 'Which must appear in the statement of profit and loss itself?', ['Pre-tax gain or loss on disposal of assets of the discontinuing operation and related tax', 'Net cash flows of the operation', 'Carrying amount of assets to be sold', 'Expected completion date'], 0,
          'The gain or loss recognised on disposal of assets or settlement of liabilities, with its tax, must be shown in the profit and loss statement itself. Other disclosures may be given in notes. In practice: show a separate line.', 'c5', T5),
        Q('m6', 'Revenue ₹300 lakh, expenses ₹260 lakh, tax 25%. Post-tax profit of the discontinuing operation:', ['₹30 lakh', '₹40 lakh', '₹10 lakh', '₹75 lakh'], 0,
          'Pre-tax profit is ₹300 − 260 = ₹40 lakh; tax at 25% is ₹10 lakh, leaving ₹30 lakh after tax. AS 24 asks for the pre-tax figure and the related tax. In practice: disclose both.', 'c4', T4, 'moderate', check=30),
        Q('m7', 'Comparative figures for earlier periods in a year when an operation is discontinuing are:', ['Restated to separate continuing and discontinuing parts', 'Left unchanged', 'Omitted', 'Shown only for the discontinuing part'], 0,
          'AS 24 requires comparative information to be restated so that continuing and discontinuing operations can be compared across periods. In practice: split last year\'s figures too.', 'c5', T5),
        Q('m8', 'If a plan to discontinue is abandoned, the enterprise:', ['Discloses the fact, reasons and effect', 'Reverses all earlier disclosures silently', 'Makes no disclosure', 'Treats it as a prior period item'], 0,
          'When a planned discontinuance is abandoned or withdrawn, AS 24 requires disclosure of that fact, the reasons and its effect, as updating information. In practice: readers need to know the operation continues.', 'c4', T4),
        Q('m9', 'Board approves a detailed plan on 20 March, announces it on 15 April; year end 31 March; statements approved 25 May. In the year-end statements:', ['Only disclosures about the event as a non-adjusting post balance sheet event are given', 'Full AS 24 disclosures are given', 'Nothing is disclosed', 'The operation is treated as already disposed of'], 0,
          'The initial disclosure event needs both approval and announcement; it occurs on 15 April, after the year end. So the statements describe it as an event after the balance sheet date. In practice: full disclosures follow next year.', 'c2', T2, 'hard'),
        Q('m10', 'Which is NOT required in the initial disclosures?', ['The names of employees affected', 'Expected timing of completion', 'Carrying amounts of assets and liabilities to be disposed of', 'Net cash flows by activity'], 0,
          'AS 24 requires the description, segment, event date, expected completion, carrying amounts, revenue, expenses, pre-tax result and tax, and cash flows. Names of employees are not required. In practice: follow the AS 24 checklist.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Pre-tax result and tax', 2, 'computation', 'pre-tax', nums=[pbt, tax]),
           S('s2', 'Impairment via AS 28', 2, 'computation', 'as 28', nums=[imp]),
           S('s3', 'Other disclosures', 1, 'concept', 'cash flows|carrying')],
          ['Measure under other standards.'], ['Treating the loss as extraordinary.'], ['Table + note.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Approval and announcement test', 2, 'concept', 'announce'),
           S('s2', 'Earlier of the two events', 1, 'concept', 'earlier|10 march'),
           S('s3', 'Year of disclosure', 1, 'conclusion', '2026-27')],
          ['Identify both triggers.'], ['Using the board approval date alone.'], ['Timeline table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a discontinuing operation?', 'A distinct major business line or geographical area, distinguishable operationally and for reporting, that under a single plan is being sold, demerged, disposed of piecemeal or abandoned.',
          [P('p1', 'Major line or area', 5, 'major'), P('p2', 'Single plan, sale or abandonment', 5, 'plan|abandon|dispos')], 'c1'),
        V('v2', 'What is the initial disclosure event?', 'The earlier of a binding sale agreement for substantially all the assets, or the board approving and announcing a detailed formal plan.',
          [P('p1', 'Binding agreement', 5, 'binding'), P('p2', 'Approved and announced plan', 5, 'announc')], 'c2'),
        V('v3', 'Does AS 24 have its own measurement rules?', 'No; it deals with presentation and disclosure, and measurement follows other standards such as AS 28 for impairment and AS 29 for provisions.',
          [P('p1', 'Presentation standard', 4, 'presentation|disclosure'), P('p2', 'Other standards', 6, 'as 28|as 29|other standard')], 'c3'),
        V('v4', 'Is a discontinuing operation an extraordinary item?', 'Its results are part of ordinary activities and are disclosed separately; they are rarely, if ever, extraordinary items.',
          [P('p1', 'Ordinary activities', 6, 'ordinary'), P('p2', 'Disclosed separately', 4, 'separate')], 'c3'),
        V('v5', 'Why are comparatives restated?', 'So that continuing and discontinuing operations can be compared across periods on the same basis.',
          [P('p1', 'Comparability', 6, 'compar'), P('p2', 'Continuing vs discontinuing', 4, 'continuing')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Shakti Industries Ltd.', 'difficulty': 'moderate',
              'case': 'Shakti Industries Ltd. has three segments: steel, cement and power. On 1 February 2027 its board approved and announced a detailed plan to sell the cement segment by December 2027. Cement revenue for 2026-27 was ₹800 crore; it also decided to stop making one grade of steel.',
              'mcqs': [
                  M('k1a', 'The cement segment is:', ['A discontinuing operation from 1 February 2027', 'Not discontinuing until sold', 'An extraordinary item', 'A prior period item'], 0,
                    'Cement is a separate major line of business, and the initial disclosure event occurred when the board approved and announced the detailed plan on 1 February 2027. In practice: disclose in 2026-27 statements.', 'core', topic=T2),
                  M('k1b', 'Stopping one grade of steel is:', ['Not a discontinuing operation', 'A discontinuing operation', 'A geographical discontinuance', 'An abandonment requiring AS 24 disclosures'], 0,
                    'Dropping a product within a continuing line of business is a normal business change, not a discontinuing operation, as the steel segment continues. In practice: no AS 24 disclosures are needed for it.', 'core', topic=T1),
                  M('k1c', 'Revenue of the cement segment to be disclosed for 2026-27:', ['₹800 crore', 'Nil', '₹400 crore', 'Only from 1 February'], 0,
                    'AS 24 requires revenue, expenses and results of the discontinuing operation for the whole period, not just after the event date. Comparatives are also restated. In practice: disclose ₹800 crore.', 'moderate', check=800, topic=T4),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch04', 6, 'Accounting Standard 24 Discontinuing Operations',
                ['Identify a discontinuing operation.',
                 'Determine the initial disclosure event.',
                 'Apply other standards for measurement and prepare the required disclosures.',
                 'Present comparatives and interim information.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 20}, 'prereq': ['int-p1-ch04-u05'],
                 'exam_tip': 'Test the three conditions (single plan, major line, distinguishable) and fix the event date first.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Discontinuing: major line/area, single plan, distinguishable.', 'Initial disclosure event: earlier of binding agreement or approved + announced plan.',
                             'Measurement under AS 28, AS 29 and others; not extraordinary.', 'Disclose description, dates, carrying amounts, results, tax, cash flows.',
                             'Gain/loss on disposal and tax on the face of P&L; restate comparatives.'],
                 'remember': ['Updating disclosures until completion; disclose abandonment.'],
                 'traps': ['A product phase-out is not a discontinuing operation.']},
                [('Trigger', 'Binding agreement or approved + announced plan'), ('Measurement', 'AS 28, AS 29'), ('Face of P&L', 'Disposal gain/loss and tax')],
                viva, cases)
