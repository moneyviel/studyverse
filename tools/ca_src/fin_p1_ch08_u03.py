"""CA Final · Paper 1 Financial Reporting · Chapter 8 Unit 3 Ind AS 108 Operating Segments.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch08-u03'
T1 = 'Identifying operating segments'
T2 = 'Aggregation and quantitative thresholds'
T3 = 'Segment disclosures and measurement'
T4 = 'Entity-wide disclosures and restatement'


def build():
    ck = Checks()
    tot = ck.add('400+250+180+90+50+30', 'Total segment revenue (₹ crore)')
    th = ck.add('(400+250+180+90+50+30)*0.1', '10% revenue threshold (₹ crore)')
    ext = ck.add('380+240+170+85+48+30', 'Total external revenue (₹ crore)')
    cov = ck.add('380+240+170', 'External revenue of segments A, B, C (₹ crore)')
    need = ck.add('(380+240+170+85+48+30)*0.75', '75% of external revenue (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Which segments are reportable?', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Helix Ltd. has six operating segments with total revenue (external + inter-segment) in ₹ crore: A 400, B 250, C 180, D 90, E 50, F 30. External revenue: A 380, B 240, C 170, D 85, E 48, F 30. Profit and asset tests do not change the result. Which segments are reportable, and is the 75% test met?',
          'solution': [table(['Step', 'Working', '₹ crore'], [
              ['Total revenue', 'Sum of all segments', inr(tot)],
              ['10% threshold', '1,000 × 10%', inr(th)],
              ['Reportable by size', 'A, B, C (D at 90 is below 100)', '—'],
              ['Total external revenue', 'Sum', inr(ext)],
              ['External revenue of A, B, C', '380 + 240 + 170', inr(cov)],
              ['75% requirement', '953 × 75%', inr(need)],
              ['Conclusion', '790 ≥ 714.75 — test met; D, E, F go to "all other segments"', '—']], title='Ind AS 108 thresholds')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Is this an operating segment?', 'difficulty': 'core', 'minutes': 5,
          'q': 'Assess: (a) corporate headquarters that earns no revenue; (b) a start-up division with no revenue yet, reviewed monthly by the CEO; (c) a post-employment benefit plan; (d) a retail division whose results are reviewed by the board acting as CODM.',
          'solution': [table(['Item', 'Operating segment?', 'Reason'], [
              ['(a)', 'No', 'Incidental revenue at most; not a business activity earning revenue'],
              ['(b)', 'Yes', 'May earn revenue in future; results reviewed by CODM'],
              ['(c)', 'No', 'Benefit plans are not operating segments'],
              ['(d)', 'Yes', 'Earns revenue; results reviewed by the CODM; discrete information exists']], title='Identification')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Ind AS 108 aims to show users what kinds of business the entity runs, in which economic settings, and what those activities mean financially. It follows a management approach: segments are what the chief operating decision maker (CODM) uses.',
            'An operating segment is a component that engages in business activities which earn (or may earn) revenues and incur expenses, whose operating results are regularly reviewed by the CODM for resource allocation and performance assessment, and for which discrete financial information is available.',
            'The CODM is a function, not a title — it may be the CEO, COO or a group of executives. Corporate headquarters and post-employment benefit plans are not operating segments. Start-up operations can be segments before earning revenue.'],
          'Segments are reported the way management sees the business.',
          'If the CEO\'s monthly pack shows results by region, regions are likely segments.'),
        C('c2', T2, [
            'Segments may be aggregated if aggregation is consistent with the core principle, they have similar economic characteristics (e.g. similar long-term margins) and are similar in products, production processes, customer types, distribution methods and regulatory environment.',
            'A segment is reportable if any one of these is met: its reported revenue (external and inter-segment) is 10% or more of combined revenue of all segments; its profit or loss is 10% or more of the greater of combined profits of profit-making segments and combined losses of loss-making segments; or its assets are 10% or more of combined segment assets.',
            'If external revenue of reportable segments is below 75% of entity revenue, more segments are added until 75% is reached. Remaining segments are combined as "all other segments". Practically, more than ten reportable segments may make information too detailed.'],
          'Apply the 10% tests, then make sure reportable segments cover 75% of outside revenue.',
          'A segment with 9% of revenue but 12% of assets is reportable.'),
        C('c3', T3, [
            'For each reportable segment, disclose general information (factors used to identify segments, types of products and services), a measure of profit or loss, and total assets and liabilities if regularly provided to the CODM.',
            'Also disclose items included in the segment measure reviewed by the CODM: external and inter-segment revenue, interest income and expense, depreciation and amortisation, material items of income and expense, share of associates, tax, and material non-cash items. Basis of measurement and accounting policies are explained.',
            'Measures are those used by the CODM, which may differ from Ind AS figures; reconciliations of totals for revenue, profit or loss, assets, liabilities and other material items to the entity\'s amounts are required.'],
          'Report what management reviews, then reconcile to the accounts.',
          'Segment profit before head office costs, reconciled with unallocated costs.'),
        C('c4', T4, [
            'Entity-wide disclosures apply even to single-segment entities: revenue from external customers for each product/service or group; revenue and non-current assets attributed to the country of domicile and to all foreign countries in total (and individually if material).',
            'Reliance on major customers: if revenue from a single external customer is 10% or more of entity revenue, disclose that fact, the total amount and the segment reporting it (the customer\'s identity need not be disclosed). Entities under common control count as one customer.',
            'If the internal structure changes and segments change, corresponding prior-period information is restated unless impracticable; if not restated, the current period is disclosed on both old and new bases.'],
          'Even one-segment companies disclose products, geography and big customers.',
          'A customer bringing 15% of sales triggers disclosure, without naming it.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Designing segment reporting', 'role': 'Investor relations analyst',
             'situation': 'A listed group restructured into three business verticals.',
             'steps': ['Identify the CODM and the reports reviewed.', 'Test aggregation and thresholds.', 'Prepare segment measures with reconciliations.', 'Restate comparatives for the new structure.'],
             'takeaway': 'Internal reporting drives external segment disclosure.'}]

    mcqs = [
        Q('m1', 'Ind AS 108 follows the:', ['Management approach', 'Risks and returns approach', 'Legal entity approach', 'Geographical approach only'], 0,
          'Segments match internal reporting to the CODM. In practice: read board packs.', 'c1', T1),
        Q('m2', 'A segment is reportable if its revenue is at least what share of combined segment revenue?', ['Ten percent', 'Five percent', 'Fifteen percent', 'Twenty-five percent'], 0,
          'Revenue includes inter-segment sales. In practice: also test profit and assets.', 'c2', T2),
        Q('m3', 'Reportable segments must together account for at least what share of external revenue?', ['Three-quarters', 'One-half', 'Nine-tenths', 'Three-fifths'], 0,
          'Add segments until met. In practice: even below-threshold ones.', 'c2', T2),
        Q('m4', 'Corporate headquarters is:', ['Not an operating segment', 'Always a segment', 'A reportable segment', 'Aggregated with the largest'], 0,
          'It does not earn revenue from business activities. In practice: show in reconciliations.', 'c1', T1),
        Q('m5', 'Revenue from a single customer of 10% or more requires disclosure of:', ['That fact, the amount and segment — not the name', 'The customer\'s name', 'Nothing', 'Contract terms'], 0,
          'Identity need not be disclosed. In practice: group entities count as one.', 'c4', T4),
        Q('m6', 'The CODM is:', ['A function that allocates resources and assesses performance', 'Always the chairman', 'The auditor', 'The CFO only'], 0,
          'It can be a group. In practice: often the CEO or executive committee.', 'c1', T1),
        Q('m7', 'Segment information is measured on:', ['The basis reported to the CODM, with reconciliations', 'Ind AS basis only', 'Tax basis', 'Cash basis'], 0,
          'Reconciliation bridges the gap. In practice: explain differences.', 'c3', T3),
        Q('m8', 'When segments change, prior period information is:', ['Restated unless impracticable', 'Never restated', 'Deleted', 'Shown only in notes'], 0,
          'Comparability matters. In practice: else disclose both bases.', 'c4', T4),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Threshold', 2, 'computation', 'threshold', nums=[th]), S('s2', 'Reportable segments', 2, 'concept', 'reportable'), S('s3', '75% test', 3, 'computation', '75', nums=[cov, need]), S('s4', 'Others', 1, 'concept', 'all other')],
          ['Show the 75% check.'], ['Using external revenue for the 10% test.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'HQ and plan', 2, 'concept', 'headquarters|plan'), S('s2', 'Start-up', 1, 'concept', 'future'), S('s3', 'Retail', 1, 'concept', 'codm')],
          ['Reason each.'], ['Excluding the start-up.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Define an operating segment.', 'A component earning or able to earn revenues and incurring expenses, whose results are regularly reviewed by the CODM and for which discrete financial information exists.',
          [P('p1', 'Revenues and expenses', 4, 'revenue'), P('p2', 'Reviewed by CODM', 6, 'codm')], 'c1'),
        V('v2', 'State the quantitative thresholds.', 'Ten percent of combined revenue, of the greater of combined profits or losses, or of combined assets.',
          [P('p1', 'Ten percent', 5, 'ten percent'), P('p2', 'Revenue, profit, assets', 5, 'revenue|profit|asset')], 'c2'),
        V('v3', 'What are the aggregation criteria?', 'Similar economic characteristics and similarity in products, processes, customers, distribution and regulatory environment.',
          [P('p1', 'Economic characteristics', 5, 'economic'), P('p2', 'Products and customers', 5, 'product|customer')], 'c2'),
        V('v4', 'What reconciliations are required?', 'Totals of segment revenue, profit or loss, assets, liabilities and other material items reconciled to the entity\'s figures.',
          [P('p1', 'Segment totals', 5, 'total'), P('p2', 'Entity figures', 5, 'entity')], 'c3'),
        V('v5', 'What entity-wide disclosures apply?', 'Revenue by products and services, revenue and non-current assets by geography, and reliance on major customers.',
          [P('p1', 'Products and geography', 5, 'product|geograph'), P('p2', 'Major customers', 5, 'major customer')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Arcadia Ltd.', 'difficulty': 'moderate',
              'case': 'Arcadia Ltd. has segments with profits (losses) in ₹ crore: P 60, Q 30, R (40), S 8, T (5). Total profits of profit-making segments = 98; total losses = 45. One government department accounts for 14% of revenue, and two companies under common control together account for 11%.',
              'mcqs': [
                  M('k1a', 'Profit threshold for the 10% test (₹ crore):', ['9.8', '4.5', '5.3', '14.3'], 0,
                    '10% of the greater of 98 and 45. In practice: use absolute amounts.', 'moderate', check=9.8, topic=T2),
                  M('k1b', 'Which segments meet the profit test?', ['P, Q and R', 'P and Q only', 'All five', 'P only'], 0,
                    'R\'s loss of 40 exceeds 9.8; S and T do not. In practice: losses count in absolute terms.', 'moderate', topic=T2),
                  M('k1c', 'The two companies under common control are treated as:', ['A single customer exceeding 10%', 'Two separate customers', 'Related parties', 'Not disclosed'], 0,
                    'Common control entities count as one. In practice: disclose amount and segment.', 'moderate', topic=T4),
                  M('k1d', 'Disclosure about the government department requires:', ['The fact, amount and segment, without naming it', 'Its name', 'Nothing', 'Contract terms'], 0,
                    'Identity is not required. In practice: judge whether government entities are one customer.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch08', 3, 'Ind AS 108 "Operating Segments"',
                ['Identify operating segments using the management approach.',
                 'Apply aggregation criteria and quantitative thresholds.',
                 'Prepare segment disclosures and reconciliations.',
                 'Provide entity-wide disclosures and handle restatement.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 25}, 'prereq': ['fin-p1-ch08-u02'],
                 'exam_tip': 'Run all three 10% tests, then confirm the 75% external revenue test.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Management approach via CODM.',
                             'Segment: revenue activity, CODM review, discrete info.',
                             '10% tests: revenue, profit/loss, assets.',
                             '75% of external revenue must be covered.',
                             'Entity-wide: products, geography, major customers.'],
                 'remember': ['Customer identity is not disclosed.'],
                 'traps': ['Ignoring loss-making segments in the profit test.']},
                [('Approach', 'Management'), ('Threshold', '10%'), ('Coverage', '75% external revenue'), ('Major customer', '10%')],
                viva, cases)
