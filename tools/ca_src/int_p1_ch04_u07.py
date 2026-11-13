"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 4 Unit 7 — AS 25 Interim Financial Reporting.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch04-u07'
T1 = 'Scope and minimum content of an interim report'
T2 = 'Periods for which interim statements are presented'
T3 = 'Same accounting policies; year-to-date measurement'
T4 = 'Seasonal revenue, uneven costs and income tax'
T5 = 'Materiality, estimates and changes in policies'


def build():
    ck = Checks()
    tax = ck.add('2000000*20/100+(4000000-2000000)*30/100', 'Estimated annual tax (₹)')
    rate = ck.add('1000000*100/4000000', 'Weighted average annual effective rate (%)')
    q = ck.add('1000000*25/100', 'Tax charge for each quarter (₹)')
    i1 = {'id': 'i1', 'title': 'Interim tax with slab rates', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Divya Ltd. expects profit before tax of ₹10,00,000 in each quarter of 2026-27. Tax is 20% on the first ₹20,00,000 of annual income and 30% above it. Compute the tax expense for each quarter.',
          'solution': [table(['Step', 'Working', 'Amount'], [
              ['Estimated annual income', '4 × 10,00,000', inr(4000000)],
              ['Estimated annual tax', '20% × 20,00,000 + 30% × 20,00,000', inr(tax)],
              ['Effective annual rate', '10,00,000 ÷ 40,00,000', f'{R(rate)}%'],
              ['Tax each quarter', '25% × 10,00,000', inr(q)]], title='AS 25 income tax')],
          'checks': list(ck)}

    ck2 = Checks()
    m = ck2.add('6', 'Months in the year-to-date period at 30 September')
    i2 = {'id': 'i2', 'title': 'Which periods go into the half-year report?', 'difficulty': 'core', 'minutes': 5,
          'q': 'Komal Ltd. (year ends 31 March) publishes a half-yearly report for the period ending 30 September 2026. List the periods for each statement, current and comparative.',
          'solution': [table(['Statement', 'Current', 'Comparative'], [
              ['Balance sheet', 'As at 30 Sept 2026', 'As at 31 March 2026 (end of last full year)'],
              ['Statement of profit and loss', f'Six months to 30 Sept 2026 ({R(m)} months, also year to date)', 'Six months to 30 Sept 2025'],
              ['Cash flow statement', 'Year to date — six months to 30 Sept 2026', 'Six months to 30 Sept 2025']], title='Periods required'),
              note('For a quarterly report at 31 December, the profit and loss would show both the quarter (Oct–Dec) and the nine months year to date, each with last year\'s matching period.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'An interim period is a reporting period shorter than a full financial year, such as a quarter or half-year. AS 25 does not require any enterprise to publish interim reports; it sets the minimum content and principles when an enterprise does so (or is required to by a regulator).',
            'Minimum components: a condensed balance sheet, condensed statement of profit and loss, condensed cash flow statement and selected explanatory notes. A complete set may be given instead.',
            'Condensed statements include each heading and subtotal of the latest annual statements, plus additional items whose omission would mislead. Basic and diluted EPS are shown on the profit and loss statement.',
            'Selected notes cover: same policies as annual or changes; seasonality; unusual items; changes in estimates; issues and repayments of debt and equity; dividends; segment results (if AS 17 applies); material events after the interim date; changes in the composition of the enterprise; and changes in contingent liabilities.'],
          'An interim report is a short update between annual reports, not a mini annual report.',
          'A listed company\'s quarterly results are an interim report.'),
        C('c2', T2, [
            'Balance sheet: as at the end of the current interim period, with comparative as at the end of the immediately preceding financial year.',
            'Statement of profit and loss: for the current interim period and cumulatively for the year to date, with comparatives for the same periods of the preceding year.',
            'Cash flow statement: cumulatively for the year to date, with comparative for the same period of the preceding year.',
            'Highly seasonal businesses are encouraged to give twelve-month data ending on the interim date as well.'],
          'Balance sheet compares with the last year end; flows compare with the same period last year.',
          'A Q3 report shows the quarter and nine months, against the same quarter and nine months last year.'),
        C('c3', T3, [
            'Interim statements apply the same accounting policies as the annual statements, except changes made after the last annual date that will apply in the next annual statements.',
            'Measurements are made on a year-to-date basis, so the frequency of reporting does not affect the annual result. Estimates made in earlier interim periods are revised in later ones; the effect goes into the current interim period.',
            'Assets and liabilities are recognised by the same definitions and criteria as at year end — for example, costs that do not meet the asset definition are not deferred as assets at the interim date.'],
          'Whether you report once or four times a year, the annual answer must be the same.',
          'An inventory write-down in Q1 that reverses by Q2 is reversed in Q2.'),
        C('c4', T4, [
            'Revenue received seasonally, cyclically or occasionally is not anticipated or deferred at an interim date if that would not be appropriate at year end. Dividends, royalties and seasonal sales are recognised when they occur.',
            'Costs incurred unevenly during the year are anticipated or deferred only if it would be appropriate to do so at the year end.',
            'Income tax expense is recognised using the best estimate of the weighted average annual effective tax rate applied to the interim period\'s pre-tax income. Different rates for different jurisdictions or categories of income are applied separately where practicable.'],
          'Do not smooth seasonal income; do smooth the tax rate over the year.',
          'A woollens maker earning most of its profit in Q3 reports low profits in Q1 and Q2.'),
        C('c5', T5, [
            'Materiality for recognition, measurement and disclosure is judged in relation to the interim period\'s financial data, while remembering that interim measurements rely more on estimates.',
            'Interim reporting generally needs greater use of estimates than annual reporting, but the information must still be reliable.',
            'A change in accounting policy (other than one required by a new standard\'s transition rules) is reflected by restating earlier interim periods of the current year and comparable interim periods of prior years, where practicable.',
            'If an estimate reported in an interim period changes significantly in the final interim period and no separate report is published for it, the nature and amount of the change are disclosed in the annual statements.'],
          'Materiality is measured against the interim figures, not the full year.',
          'A ₹50 lakh item may be immaterial for the year but material for a quarter.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Quarterly results review', 'role': 'Audit assistant',
             'situation': 'A listed company\'s draft Q2 results defer a large advertising spend to Q3 and Q4.',
             'steps': ['Check whether deferral would be allowed at year end.', 'Confirm year-to-date measurement.', 'Recompute tax using the annual effective rate.', 'Check comparative periods.'],
             'takeaway': 'Interim figures follow annual recognition rules.'}]

    mcqs = [
        Q('m1', 'The minimum components of an interim financial report include:', ['Condensed balance sheet, profit and loss, cash flow statement and selected notes', 'Only a profit and loss statement', 'Full annual statements', 'Directors\' report and auditor\'s report'], 0,
          'AS 25 sets the minimum as a condensed balance sheet, condensed statement of profit and loss, condensed cash flow statement and selected explanatory notes. A complete set may be presented instead. In practice: follow regulator formats too.', 'c1', T1),
        Q('m2', 'In an interim report, the balance sheet comparative is as at:', ['The end of the immediately preceding financial year', 'The same date last year', 'The beginning of the interim period', 'No comparative is required'], 0,
          'The balance sheet at the interim date is compared with the balance sheet at the end of the last full financial year, while flow statements compare with the same period of the previous year. In practice: watch this difference.', 'c2', T2),
        Q('m3', 'For a Q3 report (year April–March), the profit and loss covers:', ['October–December and April–December, with the same periods last year', 'Only October–December', 'Only April–December', 'January–March'], 0,
          'AS 25 requires the current interim period and the year to date, each with comparatives for the same periods of the preceding year. In practice: show four columns.', 'c2', T2),
        Q('m4', 'The cash flow statement in an interim report covers:', ['The year to date, with the same period last year', 'Only the latest quarter', 'Twelve months to the interim date', 'The full previous year'], 0,
          'The condensed cash flow statement covers the year so far, set against a comparative for the corresponding period of the preceding year. In practice: no separate quarterly cash flow is needed.', 'c2', T2),
        Q('m5', 'Interim measurements are made on:', ['A year-to-date basis', 'A discrete quarter basis ignoring earlier quarters', 'A cash basis', 'A basis chosen each quarter'], 0,
          'AS 25 requires year-to-date measurement so that the frequency of interim reporting does not change the annual result; estimates from earlier quarters are revised in later quarters. In practice: adjust earlier estimates in the current quarter.', 'c3', T3),
        Q('m6', 'Seasonal revenue at an interim date is:', ['Not anticipated or deferred unless that would be appropriate at year end', 'Spread evenly over quarters', 'Deferred to the last quarter', 'Anticipated for the whole year'], 0,
          'Seasonal, cyclical or occasional revenue is recognised when it occurs and is neither anticipated nor deferred at an interim date, unless the same treatment would be appropriate at year end. In practice: explain seasonality in notes.', 'c4', T4),
        Q('m7', 'Interim income tax expense is based on:', ['The estimated weighted average annual effective tax rate', 'The rate for the first slab only', 'The actual tax paid in the quarter', 'The previous year\'s rate'], 0,
          'Tax is accrued at the expected average tax rate for the whole year, as best estimated for the full year, applied to the interim period\'s pre-tax income. In practice: revise the rate each quarter.', 'c4', T4),
        Q('m8', 'Annual profit estimate ₹80 lakh; estimated annual tax ₹22 lakh; Q1 profit ₹15 lakh. Q1 tax expense:', ['₹4.125 lakh', '₹3 lakh', '₹4.5 lakh', '₹5.5 lakh'], 0,
          'The effective rate is 22 ÷ 80 = 27.5%; applied to Q1 profit of ₹15 lakh gives ₹4.125 lakh. Using a marginal or flat rate would distort the quarter. In practice: round only at the end.', 'c4', T4, 'hard', check=4.125),
        Q('m9', 'Materiality for an interim report is assessed in relation to:', ['The interim period\'s financial data', 'The forecast annual data', 'The previous year\'s data', 'Industry averages'], 0,
          'AS 25 requires materiality to be assessed against the interim period figures, recognising that interim measurements rely more on estimates. In practice: an item may be material for a quarter but not the year.', 'c5', T5),
        Q('m10', 'Does AS 25 require every company to publish interim reports?', ['No; it applies when an enterprise prepares or is required to prepare them', 'Yes, quarterly', 'Yes, half-yearly', 'Only unlisted companies'], 0,
          'AS 25 does not mandate interim reporting; regulators or law decide who must publish. When interim reports are prepared, AS 25 governs their minimum content and measurement. In practice: SEBI requires quarterly results from listed entities.', 'c1', T1),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Annual tax estimate', 1.5, 'computation', 'annual', nums=[tax]),
           S('s2', 'Effective rate', 1.5, 'computation', 'effective', nums=[rate]),
           S('s3', 'Quarterly charge', 1, 'computation', 'quarter', nums=[q])],
          ['Use the annual effective rate.'], ['Applying 20% to early quarters and 30% later.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Balance sheet periods', 1.5, 'concept', '31 march'),
           S('s2', 'Profit and loss periods', 1.5, 'concept', 'six months'),
           S('s3', 'Cash flow periods', 1, 'concept', 'year to date')],
          ['Give current and comparative for each.'], ['Comparing balance sheet with 30 Sept last year.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is an interim period?', 'Any reporting period that is shorter than the complete financial year — a quarter or a half-year, for example.',
          [P('p1', 'Shorter than a year', 6, 'shorter|less than'), P('p2', 'Quarter or half-year', 4, 'quarter|half')], 'c1'),
        V('v2', 'What are the minimum components of an interim report?', 'A condensed balance sheet, condensed statement of profit and loss, condensed cash flow statement and selected explanatory notes.',
          [P('p1', 'Condensed statements', 6, 'condensed'), P('p2', 'Selected notes', 4, 'notes')], 'c1'),
        V('v3', 'Why is year-to-date measurement used?', 'So that the frequency of reporting does not affect the measurement of annual results; earlier interim estimates are revised in later periods.',
          [P('p1', 'Frequency neutral', 6, 'frequency|annual'), P('p2', 'Revise estimates', 4, 'revis|estimate')], 'c3'),
        V('v4', 'How is interim tax expense measured?', 'By applying the estimated weighted average annual effective tax rate to the interim period\'s pre-tax income.',
          [P('p1', 'Annual effective rate', 6, 'effective'), P('p2', 'Interim pre-tax income', 4, 'pre-tax|interim')], 'c4'),
        V('v5', 'Are seasonal revenues smoothed across quarters?', 'Seasonal revenue is recognised when it occurs and is anticipated or deferred only if that would be proper at the year end.',
          [P('p1', 'Recognised when occurs', 6, 'when it occurs|occur'), P('p2', 'Year-end test', 4, 'year end|year-end')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Himgiri Woollens Ltd.', 'difficulty': 'moderate',
              'case': 'Himgiri Woollens Ltd. earns 70% of its sales in October–December. In Q1 it spent ₹60 lakh on its annual maintenance shutdown and wants to spread it over four quarters. It expects annual profit of ₹200 lakh with estimated tax of ₹52 lakh.',
              'mcqs': [
                  M('k1a', 'Q3 sales should be:', ['Reported as earned, with seasonality explained in notes', 'Spread evenly over four quarters', 'Deferred to Q4', 'Anticipated in Q1'], 0,
                    'Seasonal revenue is not anticipated or deferred at interim dates; it is recognised in the quarter earned, and the seasonality is explained in the notes. In practice: twelve-month trailing data helps readers.', 'core', topic=T4),
                  M('k1b', 'The ₹60 lakh maintenance cost in Q1:', ['Is expensed in Q1, as deferral would not be allowed at year end', 'Is spread at ₹15 lakh per quarter', 'Is capitalised', 'Is shown as a prepaid asset'], 0,
                    'Costs incurred unevenly are deferred only if deferral would be appropriate at year end. A completed maintenance shutdown is not an asset, so it is expensed when incurred. In practice: disclose if unusual.', 'moderate', topic=T4),
                  M('k1c', 'Effective tax rate for interim periods:', ['26%', '30%', '52%', '20%'], 0,
                    'The estimated annual tax ₹52 lakh divided by estimated annual profit ₹200 lakh gives 26%, applied to each quarter\'s pre-tax profit. In practice: update the estimate every quarter.', 'core', check=26, topic=T4),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch04', 7, 'Accounting Standard 25 Interim Financial Reporting',
                ['State the minimum content of an interim financial report.',
                 'Identify the periods and comparatives to be presented.',
                 'Apply annual policies and year-to-date measurement, including seasonal items and tax.',
                 'Apply materiality, estimates and policy-change rules to interim reports.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 20}, 'prereq': ['int-p1-ch04-u06'],
                 'exam_tip': 'Remember the comparative rule: balance sheet vs last year end; flows vs same period last year.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Minimum: condensed BS, P&L, cash flow + selected notes.', 'BS vs last year end; P&L current + YTD vs same periods; cash flow YTD.',
                             'Same policies as annual; year-to-date measurement.', 'No smoothing of seasonal revenue or uneven costs (unless allowed at year end).',
                             'Tax at estimated annual effective rate.', 'Materiality vs interim data; restate for policy changes.'],
                 'remember': ['AS 25 does not mandate interim reports.'],
                 'traps': ['Balance sheet comparative is the last year end, not the same date last year.']},
                [('Components', 'Condensed BS, P&L, CFS + notes'), ('Tax', 'Annual effective rate'), ('BS comparative', 'Last year end')],
                viva, cases)
