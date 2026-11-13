"""CA Final · Paper 1 Financial Reporting · Chapter 3 Unit 2 Ind AS 34 Interim Financial Reporting.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch03-u02'
T1 = 'Scope and content of an interim financial report'
T2 = 'Periods to be presented'
T3 = 'Recognition and measurement: the year-to-date approach'
T4 = 'Taxes, estimates and seasonal items in interim periods'


def build():
    ck = Checks()
    annual = ck.add('20*20/100 + 20*30/100', 'Estimated annual tax (₹ crore) on ₹40 crore')
    rate = ck.add('10/40*100', 'Weighted average annual effective rate (%)')
    q = ck.add('10*25/100', 'Tax charge for each quarter (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Tax in each quarter', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Zen Ltd. expects pre-tax profit of ₹10 crore in each quarter of the year (₹40 crore total). Tax is 20% on the first ₹20 crore of annual profit and 30% on the rest. Compute the tax expense for each quarterly report under Ind AS 34.',
          'solution': [table(['Step', 'Working', 'Answer'], [
              ['Estimated annual tax', '20% × 20 + 30% × 20', '₹' + str(annual) + ' crore'],
              ['Effective annual rate', '10 ÷ 40', str(rate) + '%'],
              ['Tax for each quarter', '25% × ₹10 crore', '₹' + str(q) + ' crore']], title='Ind AS 34 — income tax'),
              note('Charging 20% in Q1–Q2 and 30% in Q3–Q4 would be wrong: tax is applied using the estimated weighted average annual rate.')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Which statements, which dates?', 'difficulty': 'core', 'minutes': 6,
          'q': 'A company with a 31 March year end publishes its half-yearly report for the period ended 30 September 2027. State the periods for each statement in the interim report.',
          'solution': [table(['Statement', 'Current', 'Comparative'], [
              ['Balance sheet', 'As at 30 September 2027', 'As at 31 March 2027'],
              ['Profit and loss (with OCI)', 'Six months to 30 September 2027', 'Six months to 30 September 2026'],
              ['Changes in equity', 'Six months to 30 September 2027 (year to date)', 'Six months to 30 September 2026'],
              ['Cash flows', 'Six months to 30 September 2027 (year to date)', 'Six months to 30 September 2026']], title='Periods presented'),
              note('For a quarterly reporter, the profit and loss statement shows both the quarter and the year-to-date, each with the matching prior-year period.')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Ind AS 34 prescribes the minimum content of an interim financial report and the recognition and measurement principles for complete or condensed statements for a period shorter than a full financial year. Whether and how often to publish is decided by regulators (in India, SEBI\'s listing regulations require quarterly results).',
            'Minimum components: a condensed balance sheet, condensed statement of profit and loss, condensed statement of changes in equity, condensed statement of cash flows, and selected explanatory notes. Condensed statements include each heading and subtotal from the latest annual statements, plus basic and diluted EPS.',
            'Notes focus on events and transactions significant to understanding changes since the last annual report: a statement that the same policies are used (or what changed), seasonality, unusual items, changes in estimates, debt and equity issues or repayments, dividends, segment information, events after the interim period, changes in composition of the entity, and fair value disclosures for financial instruments.'],
          'An interim report is an update to the last annual report, not a replacement for it.',
          'A note explaining that sales peak in the winter quarter helps users read a weak summer quarter.'),
        C('c2', T2, [
            'Balance sheet: at the end of the current interim period and at the end of the immediately preceding financial year.',
            'Profit and loss: both the latest interim period on its own and the year so far, each set beside the matching periods of last year.',
            'Statements of changes in equity and cash flows: year-to-date, compared with the comparable year-to-date period of the preceding year. Highly seasonal businesses are encouraged to add twelve-month rolling information.'],
          'Balance sheets compare with the last year-end; performance statements compare like-for-like periods.',
          'A Q3 report shows Q3 and nine-month profit and loss, each against last year\'s Q3 and nine months.'),
        C('c3', T3, [
            'The same accounting policies as in annual statements are applied, except policy changes made after the last annual report that will apply at year end.',
            'Measurement is on a year-to-date basis, so annual results do not depend on how often the entity reports. Changes in estimates in a later interim period adjust that period; the earlier interim amounts are not restated.',
            'Assets and liabilities are recognised only if they meet the definitions at the interim date. Costs incurred unevenly are anticipated or deferred only if that would be appropriate at the end of the financial year.',
            'Materiality is assessed in relation to the interim period\'s data, while recognising that interim measurements rely more on estimates.'],
          'Treat each interim period as part of the year, measured as if the year ended on that date.',
          'Major repair costs planned for March are not accrued in the June quarter, since there is no obligation yet.'),
        C('c4', T4, [
            'Income tax expense for an interim period uses the best estimate of the weighted average annual effective tax rate applied to the interim pre-tax income; where different rates apply to categories of income or jurisdictions, separate rates are used.',
            'Seasonal, cyclical or occasional revenue is not anticipated or deferred at an interim date if that would not be appropriate at year end — e.g. dividend income is recognised when the right to receive arises.',
            'Year-end bonuses are accrued in interim periods if there is a legal or constructive obligation and a reliable estimate; contingent lease payments and volume rebates are accrued when it is probable the target will be achieved. An impairment loss on goodwill recognised in an earlier interim period is not reversed.',
            'Inventories, depreciation, foreign exchange and provisions follow the same principles as at year end, applying measurement on the interim date.'],
          'Taxes and bonuses are spread by estimating the year; one-off seasonal revenue is not smoothed.',
          'A retailer\'s Diwali sales boost its October–December quarter; they are not spread across the year.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Quarterly results pack', 'role': 'Audit senior (limited review)',
             'situation': 'A listed client prepares its Q2 results for the Board.',
             'steps': ['Check periods presented in each statement.', 'Recompute tax at the estimated annual effective rate.', 'Review accruals for bonuses and rebates.', 'Read notes for seasonality and significant events.'],
             'takeaway': 'Most interim errors come from wrong periods or tax rates, not complex standards.'}]

    mcqs = [
        Q('m1', 'Which is NOT a minimum component of an interim report under Ind AS 34?', ['A directors\' report', 'Condensed balance sheet', 'Condensed statement of cash flows', 'Selected explanatory notes'], 0,
          'Minimum components are condensed statements and selected notes. In practice: listed entities also follow SEBI formats.', 'c1', T1),
        Q('m2', 'In a Q3 interim report, the balance sheet comparative is as at:', ['The end of the immediately preceding financial year', 'The end of Q3 of last year', 'The end of Q2', 'The date of incorporation'], 0,
          'Balance sheets compare with the last annual reporting date. In practice: e.g. 31 March.', 'c2', T2),
        Q('m3', 'Interim tax expense is computed by:', ['Applying the estimated weighted average annual effective rate to interim pre-tax income', 'Applying the year-end statutory rate only', 'Ignoring tax until year end', 'Using last year\'s actual tax'], 0,
          'Ind AS 34 integrates tax over the year. In practice: re-estimate each period.', 'c4', T4),
        Q('m4', 'Measurement in interim reports should be on a:', ['Year-to-date basis', 'Discrete-quarter basis only', 'Cash basis', 'Rolling 12-month basis only'], 0,
          'Year-to-date measurement keeps annual results independent of reporting frequency. In practice: later estimate changes adjust the current period.', 'c3', T3),
        Q('m5', 'Dividend income received seasonally in Q1 should be:', ['Recognised when the right to receive arises, not spread over the year', 'Spread evenly over four quarters', 'Deferred to year end', 'Recognised only in Q4'], 0,
          'Seasonal revenue is not anticipated or deferred. In practice: disclose seasonality.', 'c4', T4),
        Q('m6', 'A goodwill impairment recognised in Q1 is:', ['Not reversed in a later interim or annual period', 'Reversed if Q2 results improve', 'Reversed at year end', 'Spread over the year'], 0,
          'Ind AS 34 guidance prohibits reversal of goodwill impairment recognised in an interim period. In practice: consistent with Ind AS 36.', 'c4', T4),
        Q('m7', 'Materiality for an interim report is assessed in relation to:', ['The interim period\'s financial data', 'Annual budgeted data only', 'Last year\'s annual data only', 'Market capitalisation'], 0,
          'Interim materiality uses interim data, recognising greater use of estimates. In practice: smaller thresholds than annual.', 'c3', T3),
        Q('m8', 'A year-end bonus is accrued in interim periods if:', ['There is a legal or constructive obligation and it can be reliably estimated', 'Management may decide to pay it', 'Employees request it', 'It was paid last year regardless of obligation'], 0,
          'Only present obligations are accrued. In practice: past practice may create a constructive obligation.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Annual tax', 1, 'computation', 'annual', nums=[annual]), S('s2', 'Effective rate', 1.5, 'computation', 'effective', nums=[rate]), S('s3', 'Quarterly charge', 1.5, 'computation', 'quarter', nums=[q])],
          ['Estimate the full year first.'], ['Applying slab rates quarter by quarter.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Balance sheet dates', 1, 'concept', '31 march 2027'), S('s2', 'P&L periods', 1.5, 'concept', 'six months'), S('s3', 'SCE and cash flow', 1.5, 'concept', 'year to date')],
          ['Tabulate statements and periods.'], ['Comparing the balance sheet with last September.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What are the minimum components of an interim report?', 'Condensed balance sheet, condensed profit and loss, condensed changes in equity, condensed cash flows and selected explanatory notes.',
          [P('p1', 'Condensed statements', 6, 'condensed'), P('p2', 'Notes', 4, 'notes')], 'c1'),
        V('v2', 'What periods does the interim profit and loss cover?', 'The current interim period and the year-to-date, each compared with the same periods of the preceding financial year.',
          [P('p1', 'Current and YTD', 6, 'year-to-date|year to date'), P('p2', 'Comparatives', 4, 'preceding|previous')], 'c2'),
        V('v3', 'What is the year-to-date approach?', 'Measuring interim amounts as if the reporting period ended at the interim date, so annual results are the same whatever the reporting frequency.',
          [P('p1', 'Measure to date', 5, 'date'), P('p2', 'Frequency', 5, 'frequency')], 'c3'),
        V('v4', 'How is interim income tax measured?', 'By applying the estimated weighted average annual effective tax rate to the interim period\'s pre-tax income.',
          [P('p1', 'Annual effective rate', 6, 'annual effective|effective'), P('p2', 'Interim income', 4, 'interim')], 'c4'),
        V('v5', 'Are costs incurred unevenly smoothed across interim periods?', 'They are anticipated or deferred only where that would also be appropriate at the financial year end.',
          [P('p1', 'Year-end test', 6, 'year end'), P('p2', 'Anticipate or defer', 4, 'anticipat|defer')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Monsoon Fans Ltd.', 'difficulty': 'moderate',
              'case': 'Monsoon Fans Ltd. (listed) earns 60% of its sales in April–June. In Q1 it expects an annual sales-volume rebate from a supplier if annual purchases exceed a target, which is probable; it plans a factory overhaul in February; and it estimates an annual effective tax rate of 24%, revised to 26% in Q2.',
              'mcqs': [
                  M('k1a', 'High Q1 sales should be:', ['Reported as earned, with seasonality explained in notes', 'Spread equally over the year', 'Deferred to Q4', 'Shown net of expected returns for the year'], 0,
                    'Seasonal revenue is not deferred; notes explain seasonality. In practice: consider 12-month rolling data.', 'core', topic=T4),
                  M('k1b', 'The probable annual volume rebate is:', ['Accrued in interim periods as it is probable', 'Ignored until received', 'Recognised only in Q4', 'Shown as contingent asset only'], 0,
                    'Rebates are anticipated when it is probable the target will be met. In practice: base on purchases to date and forecasts.', 'moderate', topic=T4),
                  M('k1c', 'The planned February overhaul cost in Q1 is:', ['Not accrued, as there is no obligation at the interim date', 'Accrued one-quarter each quarter', 'Accrued fully in Q1', 'Capitalised in Q1'], 0,
                    'An intention to spend later is not a liability. In practice: recognise when incurred.', 'moderate', topic=T3),
                  M('k1d', 'The rate revision to 26% in Q2 means:', ['Q2 year-to-date tax is recalculated at 26%, with the catch-up in Q2; Q1 is not restated', 'Q1 is restated', 'Ignore until year end', 'Use 24% for the whole year'], 0,
                    'Changes in estimates adjust the current interim period on a year-to-date basis. In practice: disclose if material.', 'hard', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch03', 2, 'Ind AS 34 "Interim Financial Reporting"',
                ['Identify the minimum content of an interim financial report.',
                 'Determine the periods presented in each statement.',
                 'Apply the year-to-date recognition and measurement principles.',
                 'Measure interim income tax, seasonal items and accruals.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 25}, 'prereq': ['fin-p1-ch03-u01'],
                 'exam_tip': 'Ask "would this be recognised if the year ended today?" for every interim recognition question.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Minimum: condensed BS, P&L, SCE, CF + selected notes.',
                             'BS vs last year-end; P&L current + YTD vs same prior periods; SCE and CF YTD.',
                             'Same policies; year-to-date measurement.',
                             'Tax at estimated annual effective rate.',
                             'Seasonal revenue not smoothed; bonuses/rebates accrued if obligation/probable.'],
                 'remember': ['Goodwill impairment from an interim period is not reversed.'],
                 'traps': ['Do not restate earlier quarters for estimate changes.']},
                [('Tax', 'Annual effective rate × interim PBT'), ('BS comparative', 'Last year-end'), ('Measurement', 'Year-to-date')],
                viva, cases)
