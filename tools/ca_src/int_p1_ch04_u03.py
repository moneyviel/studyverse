"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 4 Unit 3 — AS 17 Segment Reporting.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch04-u03'
T1 = 'Purpose and scope of segment reporting'
T2 = 'Business and geographical segments; primary and secondary formats'
T3 = 'The 10% thresholds and the 75% test'
T4 = 'Segment revenue, expense, result, assets and liabilities'
T5 = 'Disclosures for primary and secondary segments'


def build():
    ck = Checks()
    tot_rev = ck.add('400+120+60+300+50+70', 'Total segment revenue (₹ lakh)')
    prof = ck.add('60+10+70+5', 'Combined profit of profit-making segments (₹ lakh)')
    loss = ck.add('40+5', 'Combined loss of loss-making segments (₹ lakh)')
    rlim = ck.add('max(145,45)*10/100', 'Result threshold: 10% of the larger (₹ lakh)')
    alim = ck.add('(300+100+120+250+30+200)*10/100', 'Asset threshold: 10% of total segment assets (₹ lakh)')
    ext = ck.add('(400+120+60+300+70)*100/1000', 'External revenue of reportable segments as % of total')
    i1 = {'id': 'i1', 'title': 'Which segments must be reported?', 'difficulty': 'hard', 'minutes': 12,
          'q': 'Vistar Ltd. has six business segments (₹ lakh; all revenue external): A — revenue 400, result 60, assets 300; B — 120, (40), 100; C — 60, 10, 120; D — 300, 70, 250; E — 50, (5), 30; F — 70, 5, 200. Identify the reportable segments.',
          'solution': [table(['Test', 'Threshold', 'Segments passing'], [
              ['Revenue ≥ 10% of total', f'10% of {R(tot_rev)} = 100', 'A, B, D'],
              ['Result ≥ 10% of larger of total profits and total losses', f'Profits {R(prof)}, losses {R(loss)} → {R(rlim)}', 'A, B, D'],
              ['Assets ≥ 10% of total', f'{R(alim)}', 'A, B, C, D, F'],
              ['Reportable (any one test)', '', 'A, B, C, D, F'],
              ['75% check', f'External revenue of reportable segments = {R(ext)}%', 'Above 75% — no more needed']], title='AS 17 thresholds'),
              note('E fails every test and may be shown in a reconciling "unallocated/other" item, or reported voluntarily.')],
          'checks': list(ck)}

    ck2 = Checks()
    res = ck2.add('900-620-80', 'Segment result (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'What goes into segment result?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Segment P has external sales ₹900 lakh and directly attributable expenses ₹620 lakh. Head office costs of ₹80 lakh can be allocated to it on a reasonable basis. It also bears interest on general borrowings ₹30 lakh and income tax ₹50 lakh. Compute the segment result.',
          'solution': [table(['Item', 'Treatment', '₹ lakh'], [
              ['Segment revenue', 'Included', R(900)],
              ['Direct expenses', 'Deducted', '(620)'],
              ['Allocable head office costs', 'Deducted (reasonable basis)', '(80)'],
              ['Interest on general borrowings', 'Excluded (not an operating item of the segment)', '—'],
              ['Income tax', 'Excluded', '—'],
              ['Segment result', '', R(res)]], title='Segment result')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'AS 17 asks an enterprise with several products, services or regions to report information by segment, so users can judge the different risks and returns that a single set of totals hides.',
            'It applies where consolidated and separate statements are presented: segment information is given on the basis of the consolidated statements. Smaller enterprises (SMCs and non-Level I entities) are exempt.'],
          'Totals can hide a sick business inside a healthy group.',
          'A firm selling both cement and software faces very different risks in each.'),
        C('c2', T2, [
            'A business segment is a distinguishable component providing a product or service (or a group of related ones) with risks and returns different from other components; factors include nature of products, production processes, type of customers, distribution methods and regulatory environment.',
            'A geographical segment provides products or services within a particular economic environment with different risks and returns — based on location of assets or of customers.',
            'The dominant source of risks and returns decides the primary format (business or geographical); the other is secondary. The internal organisation and management reporting structure is usually the guide.'],
          'Primary format follows what drives risk most; the internal reports usually show it.',
          'An exporter whose margins swing with each country\'s currency may choose geography as primary.'),
        C('c3', T3, [
            'A business or geographical segment is reportable if a majority of its revenue is from external customers and any one of these is 10% or more: its revenue (external and inter-segment) of total segment revenue; its result (profit or loss) of the larger of combined profits of profit-making segments or combined losses of loss-making segments; or its assets of total segment assets.',
            'If reportable segments\' external revenue is less than 75% of total enterprise revenue, more segments are added until 75% is reached, even if below 10%.',
            'A segment reportable last year because it crossed a threshold continues to be reported this year if management judges it of continuing significance. Segments may also be reported voluntarily or combined if similar.'],
          'Any one 10% test is enough; then top up to 75%.',
          'A segment with 6% of revenue but 15% of assets is reportable.'),
        C('c4', T4, [
            'Segment revenue includes external and inter-segment sales directly attributable or reasonably allocable; it excludes extraordinary items, interest or dividend income (unless the segment\'s operations are financial) and gains on sale of investments.',
            'Segment expense is directly attributable or reasonably allocable operating expense; it excludes interest expense (unless financial), losses on investments, income tax, extraordinary items and general administrative expenses relating to the enterprise as a whole.',
            'Segment result = segment revenue − segment expense. Segment assets and liabilities are operating items used by, or arising from, the segment\'s operations; assets include allocable shared assets.',
            'Segment information follows the same accounting policies as the financial statements.'],
          'Segment result is an operating figure before finance costs and tax.',
          'Interest on a general corporate loan is not charged to a segment\'s result.'),
        C('c5', T5, [
            'Primary segments: segment revenue (external and inter-segment separately), segment result, carrying amount of segment assets, segment liabilities, capital expenditure, depreciation and amortisation, and significant non-cash expenses other than depreciation. A reconciliation to enterprise totals is given.',
            'Secondary segments: revenue from external customers, carrying amount of assets and capital expenditure, for each segment above 10% of the relevant totals.',
            'Also disclose the types of products and services in each business segment, the composition of each geographical segment, the basis of inter-segment pricing and any changes in it, and changes in segment accounting policies.'],
          'Primary gets the full picture; secondary gets the outline.',
          'If business is primary, geography gets only revenue, assets and capex.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Testing segments for the annual report', 'role': 'Reporting analyst',
             'situation': 'Management reports seven product lines internally and asks which must appear in the segment note.',
             'steps': ['Confirm majority external revenue for each line.', 'Apply the three 10% tests.', 'Run the 75% check.', 'Prepare the reconciliation to totals.'],
             'takeaway': 'Work the tests systematically and document why a line is or is not reported.'}]

    mcqs = [
        Q('m1', 'The primary reporting format for segments is decided by:', ['The dominant source and nature of risks and returns', 'The largest segment by revenue', 'The auditor\'s choice', 'The legal structure of subsidiaries'], 0,
          'AS 17 says the dominant source and nature of risks and returns governs whether business or geographical segments are primary; the internal organisation and management reporting structure normally indicate it. In practice: look at what management reviews.', 'c2', T2),
        Q('m2', 'A segment is reportable if its revenue (external and inter-segment) is at least what share of total segment revenue?', ['10%', '5%', '15%', '25%'], 0,
          'One of the three tests is revenue of 10% or more of total revenue of all segments, counting both external and inter-segment sales. The other two tests use result and assets. In practice: one test is enough.', 'c3', T3, 'core', check=10),
        Q('m3', 'Reportable segments\' external revenue must reach at least what share of enterprise revenue?', ['75%', '50%', '90%', '100%'], 0,
          'If reportable segments account for less than 75% of total enterprise revenue, further segments are identified as reportable until that level is reached, even if they fail the 10% tests. In practice: add the next-largest segments.', 'c3', T3, 'core', check=75),
        Q('m4', 'Combined profits of profit-making segments ₹300 lakh; combined losses ₹420 lakh. The result threshold is:', ['₹42 lakh', '₹30 lakh', '₹72 lakh', '₹12 lakh'], 0,
          'The result test uses 10% of the greater of combined profits or combined losses in absolute amount: the larger is ₹420 lakh, so the threshold is ₹42 lakh. In practice: compare each segment\'s result, ignoring sign.', 'c3', T3, 'hard', check=42),
        Q('m5', 'A segment with 7% of revenue, 4% of result and 12% of assets is:', ['Reportable', 'Not reportable', 'Reportable only if management chooses', 'Reportable only in the secondary format'], 0,
          'Meeting any one of the three 10% tests makes a segment reportable, provided most of its revenue is external. Here the asset test is met at 12%. In practice: check all three tests.', 'c3', T3, 'moderate'),
        Q('m6', 'Which is excluded from segment expense?', ['Income tax expense', 'Directly attributable selling costs', 'Allocable plant overheads', 'Depreciation on segment assets'], 0,
          'Segment expense excludes income tax, interest (unless the segment is financial), losses on investments, extraordinary items and general enterprise-level administration costs. Direct and allocable operating costs are included. In practice: segment result is pre-tax.', 'c4', T4),
        Q('m7', 'Interest income is included in segment revenue only when:', ['The segment\'s operations are primarily financial', 'It exceeds 10% of revenue', 'It is received in cash', 'It is from a related party'], 0,
          'Interest and dividend income are generally kept out of segment revenue; the exception is a segment whose business is mainly financial, such as lending. In practice: treat a finance arm differently.', 'c4', T4),
        Q('m8', 'Which disclosure is required for secondary segments?', ['Revenue from external customers, assets and capital expenditure', 'Segment result and liabilities', 'Non-cash expenses', 'Depreciation only'], 0,
          'For the secondary format AS 17 requires only revenue from external customers, carrying amount of segment assets and additions to fixed assets for segments over the 10% levels. The primary format carries the fuller list. In practice: keep secondary notes brief.', 'c5', T5),
        Q('m9', 'Segment information is prepared using:', ['The same accounting policies as the financial statements', 'Policies chosen for internal reporting only', 'Tax rules', 'Cash basis'], 0,
          'AS 17 requires segment information to follow the accounting policies adopted for the enterprise\'s financial statements, so it reconciles with the totals. In practice: adjust internal reports where policies differ.', 'c4', T4),
        Q('m10', 'A segment reported last year falls below all thresholds this year. It:', ['Continues to be reported if management judges it of continuing significance', 'Must be dropped', 'Must be merged with another', 'Is reported only as secondary'], 0,
          'If a segment was reportable in the previous period, it continues to be reported in the current period, despite falling below the thresholds, when management judges it to be of continuing significance. In practice: explain the judgement.', 'c3', T3, 'moderate'),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Revenue test', 1.5, 'computation', 'revenue', nums=[tot_rev]),
           S('s2', 'Result test with larger of profit/loss', 2, 'computation', 'loss', nums=[rlim]),
           S('s3', 'Asset test', 1.5, 'computation', 'asset', nums=[alim]),
           S('s4', '75% test', 1, 'computation', '75', nums=[ext])],
          ['Show each threshold.'], ['Using net profit for the result test.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Allocable costs included', 2, 'computation', 'allocat', nums=[res]),
           S('s2', 'Interest and tax excluded', 2, 'concept', 'excluded')],
          ['State each inclusion and exclusion.'], ['Charging income tax to the segment.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a business segment?', 'A distinguishable component of an enterprise that provides a product or service, or group of related ones, and is subject to risks and returns different from other components.',
          [P('p1', 'Product or service', 5, 'product|service'), P('p2', 'Different risks and returns', 5, 'risk')], 'c2'),
        V('v2', 'State the three 10% tests.', 'Revenue, result, or assets of the segment being 10% or more of the respective totals — with the result test measured against the larger of total profits or total losses.',
          [P('p1', 'Revenue, result, assets', 6, 'revenue', 'asset'), P('p2', 'Larger of profit or loss', 4, 'larger|greater')], 'c3'),
        V('v3', 'What is the 75% rule?', 'If reportable segments\' external revenue is below 75% of total enterprise revenue, more segments are identified as reportable until 75% is covered.',
          [P('p1', '75% of revenue', 6, '75'), P('p2', 'Add segments', 4, 'more|additional|add')], 'c3'),
        V('v4', 'What items are excluded from segment expense?', 'Interest expense unless the segment is financial, losses on investments, income tax, extraordinary items and general corporate administrative costs.',
          [P('p1', 'Interest and tax', 6, 'interest', 'tax'), P('p2', 'Corporate costs', 4, 'corporate|general|administrative')], 'c4'),
        V('v5', 'What does the secondary format disclose?', 'Revenue from external customers, carrying amount of segment assets and capital expenditure for each significant secondary segment.',
          [P('p1', 'External revenue', 4, 'revenue'), P('p2', 'Assets and capital expenditure', 6, 'asset', 'capital')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Nirmala Group', 'difficulty': 'moderate',
              'case': 'Nirmala Ltd. has segments Textiles (revenue ₹520 crore, 95% external), Chemicals (₹380 crore, 40% external — mostly supplied to Textiles), and Retail (₹100 crore, all external). Its risks vary mainly with products; internal reports are by product line.',
              'mcqs': [
                  M('k1a', 'The primary format for Nirmala is:', ['Business segments', 'Geographical segments', 'Both equally', 'Neither'], 0,
                    'Risks and returns vary mainly with products, and internal reports are by product line, so business segments form the primary format and geography secondary. In practice: document the basis.', 'core', topic=T2),
                  M('k1b', 'Chemicals, with only 40% external revenue, is:', ['Not separately reportable, as most of its revenue is not from external customers', 'Reportable because its revenue exceeds 10%', 'Always reportable', 'Reportable as secondary'], 0,
                    'A segment is reportable only if a majority of its revenue comes from external customers and it meets a 10% test. Chemicals sells mostly within the group, so it fails the first condition. In practice: it may be reported voluntarily.', 'moderate', topic=T3),
                  M('k1c', 'Retail\'s share of total segment revenue is:', ['10%', '5%', '19%', '20%'], 0,
                    'Total segment revenue is ₹520 + 380 + 100 = ₹1,000 crore, so Retail\'s ₹100 crore is 10%, exactly meeting the revenue test. In practice: the test is "10% or more".', 'moderate', check=10, topic=T3),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch04', 3, 'Accounting Standard 17 Segment Reporting',
                ['Explain the purpose of segment reporting and identify business and geographical segments.',
                 'Choose primary and secondary formats.',
                 'Apply the 10% and 75% tests to identify reportable segments.',
                 'Measure segment results and state the required disclosures.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 30, 'practice': 30}, 'prereq': ['int-p1-ch04-u02'],
                 'exam_tip': 'For the result test, compute total profits and total losses separately and take 10% of the larger.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Business or geographical segments; primary format follows dominant risks.',
                             'Reportable: majority external revenue + any 10% test (revenue, result, assets).',
                             'Top up to 75% of enterprise revenue.', 'Segment result excludes interest, tax, corporate costs.',
                             'Primary: full disclosures with reconciliation; secondary: revenue, assets, capex.'],
                 'remember': ['Continuing significance keeps last year\'s segment.'],
                 'traps': ['Result test uses the larger of profits or losses, not the net.']},
                [('Thresholds', '10% revenue / result / assets'), ('Coverage', '75% of revenue'), ('Primary format', 'Dominant risks and returns')],
                viva, cases)
