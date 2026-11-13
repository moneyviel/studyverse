"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 5 Unit 4 — AS 16 Borrowing Costs.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch05-u04'
T1 = 'Borrowing costs and qualifying assets'
T2 = 'Specific borrowings'
T3 = 'General borrowings and the capitalisation rate'
T4 = 'Start, suspension and end of capitalisation'
T5 = 'Disclosure and interaction with other standards'


def build():
    ck = Checks()
    intr = ck.add('5000000*10/100', 'Interest on the specific loan for the year (₹)')
    inv = ck.add('2000000*8/100*3/12', 'Income on temporary investment (₹)')
    cap = ck.add('500000-40000', 'Borrowing cost capitalised (₹)')
    i1 = {'id': 'i1', 'title': 'A loan raised for one project', 'difficulty': 'core', 'minutes': 6,
          'q': 'Shubh Hotels Ltd. borrowed ₹50 lakh at 10% on 1 April 2026 specifically to build a hotel, which took the whole year and more. ₹20 lakh not needed immediately was placed in a deposit for April–June at 8%. Compute the borrowing cost to capitalise for 2026-27.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Interest on specific loan', '50,00,000 × 10%', inr(intr)],
              ['Less: income from temporary investment', '20,00,000 × 8% × 3/12', inr(inv)],
              ['Capitalised', '', inr(cap)]], title='Specific borrowing')],
          'checks': list(ck)}

    ck2 = Checks()
    rate = ck2.add('(10000000*9/100+5000000*12/100)*100/15000000', 'Capitalisation rate (%)')
    amt = ck2.add('4000000*10/100', 'Borrowing cost capitalised (₹)')
    act = ck2.add('900000+600000', 'Total actual interest on general borrowings (₹)')
    i2 = {'id': 'i2', 'title': 'Funding from the general pool', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Prabha Ltd. has general borrowings of ₹1 crore at 9% and ₹50 lakh at 12% outstanding all year. It used general funds for a plant under construction; the weighted average expenditure for the year was ₹40 lakh. Compute the capitalisation rate and the amount to capitalise.',
          'solution': [table(['Step', 'Working', 'Answer'], [
              ['Interest on general borrowings', '9,00,000 + 6,00,000', inr(act)],
              ['Capitalisation rate', '15,00,000 ÷ 1,50,00,000', f'{R(rate)}%'],
              ['Capitalised', '40,00,000 × 10%', inr(amt)]], title='General borrowings'),
              note('The capitalised amount cannot exceed the actual borrowing costs of the year (₹15,00,000) — it does not here.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Borrowing costs are interest and other costs of borrowing funds: interest on loans and overdrafts, commitment charges, amortisation of discounts or premiums on borrowings, amortisation of ancillary costs of arranging loans, finance charges on finance leases, and exchange differences on foreign currency loans to the extent they adjust interest cost.',
            'A qualifying asset is one that necessarily needs a substantial period — ordinarily twelve months or more — to get ready for its intended use or sale, such as a factory, a power plant or inventory that takes a long time to produce.',
            'Borrowing costs directly attributable to acquiring, constructing or producing a qualifying asset are capitalised as part of its cost; other borrowing costs are expensed.',
            'Assets ready for use when bought, and inventories produced routinely in large quantities over short periods, are not qualifying assets.'],
          'Finance cost becomes asset cost only while the asset is still being made ready over a long period.',
          'Interest on a loan for a dam taking three years to build is capitalised; interest on a loan for a ready-made truck is not.'),
        C('c2', T2, [
            'Where funds are borrowed specifically for a qualifying asset, the amount capitalised is the actual borrowing cost incurred on that borrowing in the period, less any income from temporarily investing those funds.',
            'This net cost is the borrowing cost that would have been avoided had the asset not been built.'],
          'Charge the project with its own loan\'s interest, net of what the idle cash earned.',
          'Interest of ₹6 lakh less ₹50,000 earned on parked funds gives ₹5.5 lakh to capitalise.'),
        C('c3', T3, [
            'Where funds come from general borrowings, the amount capitalised = expenditure on the asset × capitalisation rate.',
            'The capitalisation rate is the weighted average of borrowing costs on the enterprise\'s borrowings outstanding during the period, other than those made specifically for a qualifying asset.',
            'The amount capitalised in a period cannot exceed the borrowing costs actually incurred in that period.',
            'Expenditure counts only to the extent it involves payments of cash, transfers of other assets or interest-bearing liabilities, reduced by progress payments and grants received.'],
          'A pooled rate applies to the pooled money spent on the asset.',
          'A firm paying 9% and 12% on equal loans uses 10.5% if both are general.'),
        C('c4', T4, [
            'Capitalisation starts when all three are true: expenditure on the asset is being incurred, borrowing costs are being incurred, and activities to prepare the asset are in progress (including technical and administrative work before physical construction).',
            'Capitalisation pauses for any long stretch in which active work on the asset has stopped. It is not suspended for temporary delays that are a necessary part of the process (such as normal monsoon breaks expected in the region) or while substantial technical work continues.',
            'Capitalisation ceases when substantially all activities needed to prepare the asset are complete, even if minor modifications or routine administrative work remain. If parts are completed and usable separately, capitalisation stops for each completed part.'],
          'Capitalise while the asset is actively being built; pause during long stoppages; stop when it is ready.',
          'A six-month halt due to a funding dispute suspends capitalisation; a two-week rain delay does not.'),
        C('c5', T5, [
            'Disclose the accounting policy for borrowing costs and the amount capitalised during the period.',
            'If the carrying amount, including capitalised borrowing costs, exceeds the recoverable amount, an impairment loss is recognised under AS 28.',
            'Exchange differences on foreign currency borrowings are borrowing costs only to the extent they adjust interest — limited to the difference between interest on local currency and foreign currency borrowings.'],
          'Show how much interest went into assets this year.',
          'A note: "Borrowing costs of ₹1.2 crore capitalised to capital work in progress."'),
    ]

    jobs = [{'id': 'j1', 'title': 'Interest capitalisation schedule', 'role': 'Accounts executive',
             'situation': 'A company built a new plant over 18 months with one specific loan and general borrowings.',
             'steps': ['Identify the qualifying asset and start date.', 'Net specific interest against temporary income.', 'Apply the capitalisation rate to other spending.', 'Identify suspension periods and the completion date.'],
             'takeaway': 'Dates of start, suspension and completion matter as much as rates.'}]

    mcqs = [
        Q('m1', 'A qualifying asset ordinarily takes how long to get ready for use or sale?', ['Twelve months or more', 'Six months or more', 'Three months or more', 'Any period'], 0,
          'AS 16 describes a qualifying asset as one needing a substantial period to be ready, ordinarily twelve months or more, unless a shorter period is justified. In practice: routine short-cycle inventory is excluded.', 'c1', T1),
        Q('m2', 'Which is a borrowing cost under AS 16?', ['Commitment charges on a loan', 'Dividend on equity shares', 'Cost of issuing equity shares', 'Bank charges on collections'], 0,
          'Borrowing costs include interest, commitment charges, amortised discounts or premiums and ancillary costs of borrowing, finance lease charges and some exchange differences. Equity costs are not borrowing costs. In practice: list all loan-related charges.', 'c1', T1),
        Q('m3', 'Income from temporary investment of specific borrowings is:', ['Deducted from the borrowing costs capitalised', 'Credited to profit and loss always', 'Added to the asset cost', 'Credited to capital reserve'], 0,
          'For specific borrowings, the capitalised amount is the actual borrowing cost less any investment income earned on temporarily idle funds. This gives the true net cost. In practice: track deposits of loan funds.', 'c2', T2),
        Q('m4', 'General borrowings: ₹2 crore at 8% and ₹1 crore at 11%. Capitalisation rate:', ['9%', '9.5%', '8%', '11%'], 0,
          'Total interest is ₹16 lakh + ₹11 lakh = ₹27 lakh on ₹3 crore, giving a weighted average rate of 9%. A simple average of the rates would wrongly give 9.5%. In practice: weight by amounts and time outstanding.', 'c3', T3, 'moderate', check=9),
        Q('m5', 'The amount capitalised using the capitalisation rate cannot exceed:', ['Actual borrowing costs incurred in the period', 'The cost of the asset', '10% of expenditure', 'Interest on specific loans'], 0,
          'AS 16 caps borrowing costs capitalised in a period at the borrowing costs actually incurred during that period. Capitalisation cannot create costs that were never borne. In practice: compare with total interest expense.', 'c3', T3),
        Q('m6', 'Capitalisation begins when:', ['Expenditure and borrowing costs are being incurred and preparation activities are in progress', 'The loan is sanctioned', 'The asset is put to use', 'The board approves the project'], 0,
          'All three conditions must be met together: expenditure is being incurred, borrowing costs are being incurred and activities to prepare the asset have begun, including technical and administrative work. In practice: note the first date all three hold.', 'c4', T4),
        Q('m7', 'During a five-month stoppage of construction caused by a legal dispute, capitalisation is:', ['Suspended', 'Continued', 'Doubled', 'Reversed'], 0,
          'Capitalisation is suspended during extended periods when active development is interrupted; the interest for that time is expensed. Temporary delays that are a normal part of the process do not cause suspension. In practice: keep records of stoppages.', 'c4', T4),
        Q('m8', 'Capitalisation ceases when:', ['Substantially all activities needed to prepare the asset are complete', 'All minor modifications are finished', 'The asset earns its first revenue', 'The loan is repaid'], 0,
          'Capitalisation stops once substantially all activities needed to make the asset ready are complete; leftover minor decoration or routine paperwork does not extend it. In practice: use the completion certificate date.', 'c4', T4),
        Q('m9', 'Which is NOT a qualifying asset?', ['Machinery bought ready for use', 'A ship under construction for two years', 'A building under construction for 18 months', 'Whisky that matures over five years'], 0,
          'An asset that is ready for its intended use when acquired is not a qualifying asset, so interest on funds used to buy it is expensed. Long-term construction or maturing inventory qualifies. In practice: judge by the time needed to be ready.', 'c1', T1),
        Q('m10', 'Which disclosure is required by AS 16?', ['The amount of borrowing costs capitalised during the period', 'The lender\'s name', 'The interest rate on each loan', 'Future interest commitments'], 0,
          'AS 16 requires disclosure of the accounting policy adopted for borrowing costs and the amount capitalised during the period. Other loan details come from other requirements. In practice: link the note to capital work in progress.', 'c5', T5),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Interest on specific loan', 1.5, 'computation', 'interest', nums=[intr]),
           S('s2', 'Deduct investment income', 1.5, 'computation', 'temporary', nums=[inv]),
           S('s3', 'Amount capitalised', 1, 'computation', 'capitalised', nums=[cap])],
          ['Net income from idle funds.'], ['Capitalising gross interest.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Weighted rate', 2, 'computation', 'rate', nums=[rate]),
           S('s2', 'Amount and cap', 2, 'computation', 'capitalised', nums=[amt])],
          ['Weight the rate by loan amounts.'], ['Averaging the rates simply.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a qualifying asset?', 'An asset that necessarily takes a substantial period, ordinarily twelve months or more, to get ready for its intended use or sale.',
          [P('p1', 'Substantial period', 6, 'substantial'), P('p2', 'Twelve months', 4, 'twelve|12')], 'c1'),
        V('v2', 'How is the amount for specific borrowings determined?', 'Actual borrowing costs on that borrowing during the period, less income earned by temporarily investing the funds.',
          [P('p1', 'Actual cost', 5, 'actual'), P('p2', 'Less investment income', 5, 'income|investment')], 'c2'),
        V('v3', 'What is the capitalisation rate?', 'The weighted average of borrowing costs on general borrowings outstanding during the period, excluding specific borrowings for qualifying assets.',
          [P('p1', 'Weighted average', 6, 'weighted'), P('p2', 'General borrowings', 4, 'general')], 'c3'),
        V('v4', 'When is capitalisation suspended?', 'During extended periods in which active development of the asset is interrupted; temporary delays that are a normal part of the process do not suspend it.',
          [P('p1', 'Extended interruption', 6, 'extended|interrupt'), P('p2', 'Temporary delays continue', 4, 'temporary')], 'c4'),
        V('v5', 'When does capitalisation cease?', 'Once nearly all the work needed to make the asset ready for its planned use or sale has been finished.',
          [P('p1', 'Substantially complete', 6, 'nearly all|substantially'), P('p2', 'Ready for use', 4, 'ready')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Kaveri Power Ltd.', 'difficulty': 'moderate',
              'case': 'Kaveri Power Ltd. took a specific loan of ₹100 crore at 9% on 1 April 2026 for a power plant. Work stopped from 1 August to 30 November 2026 because of a court stay, resumed on 1 December and continued past 31 March 2027. No funds were invested temporarily.',
              'mcqs': [
                  M('k1a', 'Months of interest to be capitalised in 2026-27:', ['8', '12', '4', '9'], 0,
                    'Capitalisation runs April–July (4 months) and December–March (4 months) = 8 months; the four-month court stay is an extended interruption, so it is suspended. In practice: expense interest for the stay.', 'moderate', check=8, topic=T4),
                  M('k1b', 'Interest capitalised for the year:', ['₹6 crore', '₹9 crore', '₹3 crore', '₹4.5 crore'], 0,
                    'Annual interest is ₹9 crore; for 8 months of capitalisation it is ₹6 crore. The remaining ₹3 crore is charged to profit and loss. In practice: disclose the amount capitalised.', 'moderate', check=6, topic=T2),
                  M('k1c', 'Interest for the stay period is:', ['Charged to profit and loss', 'Capitalised', 'Deferred to next year', 'Charged to reserves'], 0,
                    'Borrowing costs during an extended interruption of active development are not capitalised; they are recognised as an expense in profit and loss. In practice: this is ₹3 crore here.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch05', 4, 'Accounting Standard 16 Borrowing Costs',
                ['Identify borrowing costs and qualifying assets.',
                 'Compute capitalised borrowing costs for specific and general borrowings.',
                 'Apply rules on commencement, suspension and cessation.',
                 'State the disclosure requirements.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 25, 'practice': 30}, 'prereq': ['int-p1-ch05-u03'],
                 'exam_tip': 'Draw a timeline: start, any suspension, completion; then apply specific and general rates to the right months.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Qualifying asset: substantial period (≈ 12 months+).', 'Specific: actual cost less temporary investment income.',
                             'General: expenditure × weighted average rate; capped at actual cost.', 'Start: expenditure + borrowing costs + activities.',
                             'Suspend during extended interruptions; cease when substantially complete.', 'Disclose policy and amount capitalised.'],
                 'remember': ['Exchange differences only to the extent they adjust interest.'],
                 'traps': ['Do not use a simple average of rates.']},
                [('Qualifying asset', '≈ 12 months+'), ('Specific', 'Actual − temporary income'), ('General', 'Expenditure × weighted rate')],
                viva, cases)
