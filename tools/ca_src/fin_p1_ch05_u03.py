"""CA Final · Paper 1 Financial Reporting · Chapter 5 Unit 3 Ind AS 23 Borrowing Costs.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch05-u03'
T1 = 'Core principle, borrowing costs and qualifying assets'
T2 = 'Specific and general borrowings'
T3 = 'Commencement, suspension and cessation'
T4 = 'Special issues and disclosure'


def build():
    ck = Checks()
    spec = ck.add('400*9/100 - 6', 'Specific borrowing cost capitalised (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'A loan raised for the project', 'difficulty': 'core', 'minutes': 6,
          'q': 'On 1 April a company borrows ₹400 lakh at 9% specifically to build a warehouse (a qualifying asset). Construction runs the whole year. Funds not yet spent were temporarily invested, earning ₹6 lakh. Compute borrowing cost to capitalise.',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Interest on specific loan', '400 × 9%', inr(36)],
              ['Less: income on temporary investment', '', '(6)'],
              ['Capitalised', '', inr(spec)]], title='Specific borrowings')],
          'checks': list(ck)}

    ck2 = Checks()
    rate = ck2.add('(500*10/100+300*12/100)/(500+300)*100', 'Capitalisation rate (%)')
    wexp = ck2.add('200+100*6/12', 'Weighted average expenditure (₹ lakh)')
    cap = ck2.add('250*10.75/100', 'Borrowing cost capitalised (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Funded from general borrowings', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'General borrowings outstanding all year: ₹500 lakh at 10% and ₹300 lakh at 12%. Expenditure on a qualifying asset funded from these: ₹200 lakh on 1 April and ₹100 lakh on 1 October; construction continues past year end. Compute the borrowing cost to capitalise for the year (31 March year end).',
          'solution': [table(['Step', 'Working', 'Answer'], [
              ['Capitalisation rate', '(50 + 36) ÷ 800', str(rate) + '%'],
              ['Weighted expenditure', '200 × 12/12 + 100 × 6/12', '₹' + inr(wexp) + ' lakh'],
              ['Capitalised', '250 × 10.75%', '₹' + str(cap) + ' lakh']], title='General borrowings'),
              note('Capitalised amount cannot exceed actual borrowing costs on general borrowings for the period (₹86 lakh here).')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Core principle: interest and similar costs that arise because the entity is buying, building or producing a qualifying asset are added to that asset\'s cost; other borrowing costs are expensed.',
            'Borrowing costs are interest and other costs of borrowing funds: interest under the effective interest method, interest on lease liabilities, and exchange differences on foreign currency borrowings to the extent they adjust interest costs.',
            'A qualifying asset necessarily takes a substantial period of time (generally taken as 12 months or more) to get ready for intended use or sale — e.g. manufacturing plants, power stations, investment properties, and inventories made over a long period. Financial assets and inventories produced in short periods are not qualifying; nor are assets ready for use when acquired. Entities need not apply the standard to qualifying assets measured at fair value or to inventories produced repetitively in large quantities.'],
          'If money borrowed is tied up while an asset takes a long time to build, its cost becomes part of the asset.',
          'Interest during the 3-year construction of a hydro plant is capitalised.'),
        C('c2', T2, [
            'Specific borrowings: capitalise what the loan actually cost in the period, after subtracting any income earned by parking unused loan money temporarily.',
            'General borrowings: a capitalisation rate (weighted average of borrowing costs on general borrowings outstanding during the period) is applied to the expenditure on the asset funded from them. Borrowings made specifically for a qualifying asset are excluded from this pool until substantially all activities to prepare that asset are complete — after which they join general borrowings.',
            'The amount capitalised in a period cannot exceed borrowing costs incurred. Expenditures are those resulting in cash payments, transfers of other assets or interest-bearing liabilities, reduced by progress payments and grants received.'],
          'Specific loans are traced exactly; general loans are pooled at an average rate.',
          'A term loan for one plant becomes a general borrowing once that plant is complete.'),
        C('c3', T3, [
            'Commencement: capitalisation begins when expenditure is being incurred, borrowing costs are being incurred, and activities to prepare the asset are in progress (including technical and administrative work before physical construction, such as obtaining permits). Merely holding land without development does not qualify.',
            'Suspension: capitalisation is suspended during extended periods in which active development is interrupted. It is not suspended during substantial technical or administrative work, or when a temporary delay is a necessary part of the process (e.g. high water levels typical in the region).',
            'Cessation: capitalisation stops when substantially all activities to prepare the asset are complete. If completed in parts and each part can be used while others continue, capitalisation stops for each part when it is complete.'],
          'Capitalise only while the asset is actively being made ready.',
          'A six-month halt due to a funding dispute suspends capitalisation; routine monsoon pauses in a flood zone do not.'),
        C('c4', T4, [
            'Exchange differences on foreign currency borrowings are borrowing costs to the extent they adjust interest — compared with the interest that would have been paid on an equivalent local-currency borrowing.',
            'When the carrying amount, including capitalised borrowing costs, exceeds recoverable amount or NRV, it is written down under other standards.',
            'Disclosures: amount of borrowing costs capitalised during the period and the capitalisation rate used.'],
          'Exchange losses count as interest only up to the local-currency interest saved.',
          'A dollar loan at 4% instead of a rupee loan at 10%: exchange loss up to the 6% saving is a borrowing cost.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Capitalisation schedule', 'role': 'Audit senior',
             'situation': 'A company is building two plants with a mix of specific and general loans.',
             'steps': ['Identify qualifying assets and capitalisation periods.', 'Trace specific borrowings and investment income.', 'Compute the general capitalisation rate and weighted expenditure.', 'Check suspension periods and cap at actual cost.'],
             'takeaway': 'Dates drive the answer: commencement, suspension and cessation.'}]

    mcqs = [
        Q('m1', 'A qualifying asset is one that:', ['Necessarily takes a substantial period to get ready for use or sale', 'Costs more than ₹1 crore', 'Is financed by loans', 'Is a financial asset'], 0,
          'Time to get ready, not cost or financing, decides. In practice: 12 months is a common benchmark.', 'c1', T1),
        Q('m2', 'For specific borrowings, capitalised cost is:', ['Actual borrowing costs less income on temporary investment', 'Capitalisation rate × expenditure', 'All interest of the entity', 'Nil'], 0,
          'Specific borrowings are traced directly. In practice: net off interest earned on idle funds.', 'c2', T2),
        Q('m3', 'General borrowings: ₹600 lakh at 8% and ₹400 lakh at 11%. Capitalisation rate:', ['9.2%', '9.5%', '8.0%', '11.0%'], 0,
          '(48 + 44) ÷ 1,000 = 9.2%. In practice: exclude specific borrowings.', 'c2', T2, 'moderate', check=9.2),
        Q('m4', 'Capitalisation is suspended when:', ['Active development is interrupted for an extended period', 'Technical work continues', 'A temporary delay is part of the normal process', 'The year ends'], 0,
          'Long interruptions stop capitalisation. In practice: document reasons for halts.', 'c3', T3),
        Q('m5', 'Capitalisation ceases when:', ['Substantially all activities to prepare the asset are complete', 'The asset starts earning revenue', 'The loan is repaid', 'The auditor certifies the asset'], 0,
          'Minor modifications pending do not continue capitalisation. In practice: parts usable separately stop separately.', 'c3', T3),
        Q('m6', 'Holding land without development activity:', ['Does not qualify for capitalisation', 'Qualifies fully', 'Qualifies for half the interest', 'Qualifies if land prices rise'], 0,
          'Activities to prepare the asset must be in progress. In practice: permits and design count as activities.', 'c3', T3),
        Q('m7', 'Exchange differences on foreign currency borrowings are borrowing costs:', ['To the extent they adjust interest costs', 'Never', 'Always in full', 'Only if gains'], 0,
          'Limited to the interest saved compared with a local-currency loan. In practice: compute the notional local interest.', 'c4', T4),
        Q('m8', 'A specific loan remaining after its asset is complete:', ['Is included in general borrowings for other qualifying assets', 'Stays excluded', 'Is ignored', 'Is reclassified to equity'], 0,
          'The amended Ind AS 23 brings such loans into the general pool. In practice: recompute the capitalisation rate.', 'c2', T2),
    ]

    questions = [
        W('q1', 3, i1['q'], i1['solution'],
          [S('s1', 'Interest', 1, 'computation', 'interest'), S('s2', 'Less investment income', 2, 'computation', 'investment', nums=[spec])],
          ['Net off income.'], ['Using capitalisation rate for specific loans.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Rate', 2, 'computation', 'rate', nums=[rate]), S('s2', 'Weighted expenditure', 1.5, 'computation', 'weighted', nums=[wexp]), S('s3', 'Capitalised', 1.5, 'computation', 'capitalised', nums=[cap])],
          ['Time-weight the expenditure.'], ['Applying the rate to total expenditure without weighting.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is the core principle of Ind AS 23?', 'Borrowing costs directly attributable to building or producing a qualifying asset are capitalised; others are expensed.',
          [P('p1', 'Attributable to qualifying asset', 6, 'qualifying'), P('p2', 'Others expensed', 4, 'expense')], 'c1'),
        V('v2', 'How is the capitalisation rate found?', 'As the weighted average of borrowing costs on general borrowings outstanding during the period, excluding specific borrowings for assets still under construction.',
          [P('p1', 'Weighted average', 5, 'weighted'), P('p2', 'General borrowings', 5, 'general')], 'c2'),
        V('v3', 'What three conditions start capitalisation?', 'Expenditure on the asset is being incurred, borrowing costs are being incurred, and activities to prepare the asset are in progress.',
          [P('p1', 'Expenditure and costs', 5, 'expenditure|borrowing costs'), P('p2', 'Activities', 5, 'activit')], 'c3'),
        V('v4', 'When is capitalisation not suspended despite a pause?', 'When substantial technical or administrative work continues or the delay is a necessary part of getting the asset ready.',
          [P('p1', 'Work continues', 5, 'technical|administrative'), P('p2', 'Necessary delay', 5, 'necessary')], 'c3'),
        V('v5', 'What must be disclosed?', 'The amount of borrowing costs capitalised in the period and the capitalisation rate used.',
          [P('p1', 'Amount', 5, 'amount'), P('p2', 'Rate', 5, 'rate')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Ganga Power Ltd.', 'difficulty': 'moderate',
              'case': 'Ganga Power Ltd. started building a power plant on 1 April 2026 using a specific loan of ₹1,000 crore at 8%; it earned ₹12 crore on idle funds. Work stopped for four months (August–November) due to a court stay. The plant was substantially complete on 31 January 2027, with minor painting work continuing till March.',
              'mcqs': [
                  M('k1a', 'The four-month court stay:', ['Suspends capitalisation for that period', 'Has no effect', 'Ends capitalisation', 'Doubles capitalisation'], 0,
                    'An extended interruption of active development suspends capitalisation. In practice: expense that interest.', 'moderate', topic=T3),
                  M('k1b', 'Capitalisation ceases on:', ['31 January 2027', '31 March 2027', '1 April 2026', 'When the loan is repaid'], 0,
                    'Substantially all activities were complete; minor painting does not extend it. In practice: interest after this is expensed.', 'core', topic=T3),
                  M('k1c', 'Months of active capitalisation (April–January less 4 months suspension):', ['6', '10', '4', '12'], 0,
                    'April to January is 10 months; less 4 suspended months = 6. In practice: compute interest for those months.', 'moderate', check=6, topic=T3),
                  M('k1d', 'Interest on the specific loan for the capitalisation months (₹ crore, before investment income):', ['40', '80', '53.33', '26.67'], 0,
                    '1,000 × 8% × 6/12 = 40. In practice: deduct income earned in those months only.', 'moderate', check=40, topic=T2),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch05', 3, 'Ind AS 23 "Borrowing Costs"',
                ['Identify borrowing costs and qualifying assets.',
                 'Compute capitalised costs for specific and general borrowings.',
                 'Apply commencement, suspension and cessation rules.',
                 'Treat exchange differences and disclose.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 30}, 'prereq': ['fin-p1-ch05-u02'],
                 'exam_tip': 'Draw a timeline with commencement, suspension and cessation dates before computing interest.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Capitalise borrowing costs on qualifying assets.',
                             'Specific: actual cost − temporary investment income.',
                             'General: capitalisation rate × weighted expenditure; cap at actual.',
                             'Start: expenditure + borrowing costs + activities; suspend: extended halt; stop: substantially complete.'],
                 'remember': ['Completed-asset specific loans join general pool.'],
                 'traps': ['Holding land idle does not qualify.']},
                [('Qualifying asset', 'Substantial period to get ready'), ('Specific', 'Actual − investment income'), ('General', 'Rate × weighted spend')],
                viva, cases)
