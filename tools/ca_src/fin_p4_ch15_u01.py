"""CA Final · Paper 4 · Chapter 15 Assessment Procedure.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch15-u01'
T1 = 'PAN and returns of income'
T2 = 'Self-assessment and updated return'
T3 = 'Types of assessment and DRP'
T4 = 'Income escaping assessment and time limits'
T5 = 'Rectification, block assessment and transition'


def build():
    ck = Checks()
    ad = ck.add('300000*0.50', 'Additional income-tax at 50% (₹)')
    tp = ck.add('300000+300000*0.50', 'Total payable with updated return (₹)')
    i1 = {'id': 'i1', 'title': 'Cost of an updated return', 'difficulty': 'core', 'minutes': 6,
          'q': 'Arvind discovers unreported income for T.Y. 2026-27. Tax and interest on it come to ₹3,00,000. He files an updated return on 15 January 2030 (no notice under section 280). Compute the amount payable.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Reference date', 'End of FY succeeding the tax year: 31 March 2028', '—'],
              ['Filing window', 'After 12 months, before 24 months from that date', '—'],
              ['Additional income-tax', '50% × 3,00,000', inr(ad)],
              ['Total payable', 'Tax and interest + additional tax', inr(tp)]], title='Section 267')],
          'checks': list(ck)}

    c2 = Checks()
    m1 = c2.add('4*12+3', 'Normal limit for notice u/s 280 (months from end of tax year)')
    m2 = c2.add('6*12+3', 'Extended limit for escaped income ≥ ₹50 lakh (months)')
    i2 = {'id': 'i2', 'title': 'Reassessment time limits for T.Y. 2026-27', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'For T.Y. 2026-27 (ending 31 March 2027), state the last dates for (a) a show-cause notice under section 281 and (b) a notice under section 280, in the normal case and where escaped income is ₹50 lakh or more supported by evidence of assets, expenditure or entries.',
          'solution': [table(['Notice', 'Normal case', '≥ ₹50 lakh case'], [
              ['Show-cause u/s 281', '4 years: 31 March 2031', '6 years: 31 March 2033'],
              ['Notice u/s 280', f'4 years 3 months ({m1} months): 30 June 2031', f'6 years 3 months ({m2} months): 30 June 2033'],
              ['Earliest', 'Not within one year from end of tax year', '—']], title='Section 282')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 262 governs PAN: persons with taxable income, businesses above prescribed turnover, entities entering specified transactions and others must obtain PAN; Aadhaar must be quoted and linked, and PAN and Aadhaar are interchangeable for specified purposes.',
            'Section 263(1): companies and firms must file every year; others file if total income (before specified exemptions and deductions) exceeds the basic exemption limit, or on specified high-value conditions. Due dates: 31 October for companies and audited assessees; 30 November where transfer pricing reports apply; 31 August for non-audited business or professional income (and partners of such firms); 31 July for others.',
            'A belated return may be filed within nine months after the tax year closes or before assessment, whichever earlier (section 263(4)). A revised return may be filed within twelve months after the tax year closes or before assessment, with a fee if filed after nine months (section 263(5)). Defective returns must be rectified within 15 days of intimation (section 263(7)). Specified senior citizens aged 75+ with only pension and bank interest are exempt from filing.'],
          'File on time, revise within twelve months, update within four years.',
          'A non-audited trader\'s return for T.Y. 2026-27 is due by 31 August 2027.'),
        C('c2', T2, [
            'Section 266: tax payable on the return after TDS, TCS, advance tax, reliefs and interest must be paid before filing (self-assessment tax), with payments first adjusted towards fees and interest.',
            'Section 263(6) updated return: may be filed within 48 months after the close of the financial year succeeding the tax year, even if no return was filed, but not to declare a loss, reduce tax or increase refund (a loss return filed on time may be updated if it reduces the loss), nor where search, survey or prosecution proceedings are pending, among other bars.',
            'Section 267 additional tax: 25%, 50%, 60% or 70% of the tax and interest on the updated income according to whether filed within 12, 24, 36 or 48 months from the end of that financial year; an extra 10% if filed pursuant to a notice under section 280.'],
          'Updating a return is allowed, but at a price that rises with delay.',
          'Additional tax of ₹1.5 lakh applies when ₹3 lakh of tax is updated in the second year.'),
        C('c3', T3, [
            'Section 270(1): returns are processed summarily for arithmetical errors, incorrect claims apparent from the return and specified mismatches (after giving the assessee a chance to respond) and an intimation is issued. Section 270(8) onwards: scrutiny (regular) assessment after notice under section 268, enquiries, special audit (section 268(6)) and valuation (section 269).',
            'Section 271: best judgment assessment where the assessee fails to file a return, comply with notices or keep proper accounts. Section 273: faceless assessment through the National Faceless Assessment Centre and assessment, verification, technical and review units, with electronic communication.',
            'Section 275: for eligible assessees (transfer pricing cases and foreign companies), the AO first issues a draft order; within 30 days the assessee may accept it or object before the Dispute Resolution Panel, whose directions bind the AO. Section 274 prescribes the GAAR reference procedure to the PCIT and Approving Panel.'],
          'Processing, scrutiny, best judgment and draft orders — each has its own track.',
          'A foreign company with a proposed variation gets a draft order and 30 days to approach the DRP.'),
        C('c4', T4, [
            'Section 279 allows assessment of income that has escaped assessment. Before a notice under section 280, the AO must, except in search-related or specified cases, give the assessee a show-cause opportunity and pass an order (section 281), with prior approval of the specified authority.',
            'Section 282 time limits: show-cause within 4 years after the tax year closes (6 years if escaped income is likely to be ₹50 lakh or more); notice under section 280 within 4 years and 3 months (6 years and 3 months if escaped income of ₹50 lakh or more is evidenced by books, documents or other evidence of assets, expenditure or entries). No notice within one year after the tax year closes.',
            'Section 286 time limits: regular assessment within 1 year after the close of the financial year succeeding the tax year; reassessment within 1 year after the close of the financial year in which notice under section 280 was served, with extensions for transfer pricing references and exclusions of specified periods.'],
          'Reopening needs a hearing first and must respect strict windows.',
          'For T.Y. 2026-27, a large escapement can be reopened until 30 June 2033.'),
        C('c5', T5, [
            'Section 287: mistakes apparent from the record can be rectified within four years after the close of the financial year in which the order was passed; applications by the assessee must be decided within six months from the end of the month of receipt. Only matters not considered and decided in appeal can be rectified by the AO (doctrine of partial merger).',
            'Sections 292 to 300 provide for block assessment after a search or requisition: undisclosed income for the block period (six tax years before the search and the period up to it) is assessed separately and taxed at 60% plus surcharge and cess, with specified interest and penalty.',
            'Section 536 savings: proceedings, assessments and reassessments for tax years beginning before 1 April 2026 continue under the 1961 Act; expired limitation periods are not revived.'],
          'Mistakes get corrected; searches get a block assessment.',
          'An AO can fix an arithmetical error in a 2027 order until 31 March 2032.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Handling a reassessment show-cause', 'role': 'Tax consultant',
             'situation': 'A client receives a show-cause notice under section 281.',
             'steps': ['Check time limits under section 282.', 'Examine the information relied on.', 'File a reply with evidence.', 'Consider an updated return if income was missed.'],
             'takeaway': 'Limitation is the first defence in reassessment.'}]

    mcqs = [
        Q('m1', 'Due date for a company\'s return (no transfer pricing) is:', ['End of October', 'End of July', 'End of August', 'End of November'], 0,
          'Section 263(1). In practice: audited assessees too.', 'c1', T1),
        Q('m2', 'A revised return for T.Y. 2026-27 can be filed up to:', ['31 March 2028', '31 December 2027', '31 March 2027', '31 March 2032'], 0,
          'Twelve months from end of tax year. In practice: fee after nine months.', 'c1', T1),
        Q('m3', 'An updated return filed in the third year attracts additional tax of:', ['Sixty percent', 'Fifty percent', 'Twenty-five percent', 'Seventy percent'], 0,
          'Section 267. In practice: plus 10% if after notice.', 'c2', T2),
        Q('m4', 'An updated return cannot be filed to:', ['Increase a refund', 'Report extra income', 'Correct an omission', 'Pay tax on missed interest'], 0,
          'Restriction. In practice: also not to declare new loss.', 'c2', T2),
        Q('m5', 'An eligible assessee may object to a draft order before the DRP within:', ['Thirty days', 'Sixty days', 'Fifteen days', 'Ninety days'], 0,
          'Section 275. In practice: directions bind AO.', 'c3', T3),
        Q('m6', 'A notice under section 280 cannot be issued within how long after the tax year closes?', ['One year', 'Six months', 'Two years', 'Three months'], 0,
          'Section 282(3). In practice: let returns be processed.', 'c4', T4),
        Q('m7', 'Extended reopening applies where escaped income is at least:', ['Fifty lakh rupees', 'One crore rupees', 'Ten lakh rupees', 'Twenty-five lakh rupees'], 0,
          'Section 282. In practice: needs evidence.', 'c4', T4),
        Q('m8', 'Undisclosed income in block assessment is taxed at:', ['Sixty percent', 'Thirty percent', 'Seventy-five percent', 'Maximum marginal rate'], 0,
          'Section 294 onwards. In practice: plus surcharge and cess.', 'c5', T5),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Window', 2, 'analysis', '24 months'), S('s2', 'Amount', 2, 'computation', 'additional', nums=[ad, tp])],
          ['Identify reference date.'], ['Counting from end of the tax year itself.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Show-cause limits', 2, 'analysis', '281'), S('s2', 'Notice limits', 3, 'analysis', '280')],
          ['State evidence condition.'], ['Mixing 4 years with 4 years 3 months.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Who can file an updated return?', 'Any person, whether or not a return was filed earlier, within 48 months after the close of the financial year succeeding the tax year, subject to restrictions.',
          [P('p1', 'Forty-eight months', 5, '48 months'), P('p2', 'Restrictions', 5, 'restriction')], 'c2'),
        V('v2', 'When is a best judgment assessment made?', 'When the assessee fails to file a return, comply with notices or maintain proper accounts.',
          [P('p1', 'Fails to file', 5, 'fails'), P('p2', 'Accounts', 5, 'account')], 'c3'),
        V('v3', 'What must precede a reassessment notice?', 'A show-cause opportunity and an order under section 281, with approval of the specified authority.',
          [P('p1', 'Show-cause', 5, 'show-cause|show cause'), P('p2', 'Approval', 5, 'approval')], 'c4'),
        V('v4', 'What is the time limit for rectification?', 'Four years after the close of the financial year in which the order was passed.',
          [P('p1', 'Four years', 5, 'four years'), P('p2', 'Order passed', 5, 'order')], 'c5'),
        V('v5', 'Which law governs assessment of T.Y. 2024-25?', 'The Income-tax Act, 1961, under the savings in section 536.',
          [P('p1', '1961 Act', 5, '1961'), P('p2', 'Section 536', 5, '536')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Return choices for Neha', 'difficulty': 'core',
              'case': 'Neha, a salaried individual with no business income, misses the due date for T.Y. 2026-27. Her tax is fully covered by TDS.',
              'mcqs': [
                  M('k1a', 'Her original due date was:', ['31 July 2027', '31 August 2027', '31 October 2027', '31 March 2027'], 0,
                    'Any other assessee. In practice: salaried persons.', 'core', topic=T1),
                  M('k1b', 'Last date for a belated return (if not assessed earlier):', ['31 December 2027', '31 March 2028', '30 September 2027', '31 March 2032'], 0,
                    'Nine months from end of tax year. In practice: fee applies.', 'core', topic=T1),
                  M('k1c', 'If she files the belated return and later finds an error, she can revise it up to:', ['31 March 2028', '31 December 2027', '31 July 2028', 'She cannot revise'], 0,
                    'Belated returns can be revised. In practice: before assessment.', 'core', topic=T1),
                  M('k1d', 'Months from end of the tax year to the belated return deadline:', ['9', '12', '6', '48'], 0,
                    'Nine months. In practice: earlier if assessed.', 'core', check=9, topic=T1),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch15', 1, 'Assessment Procedure',
                ['Apply PAN and return-filing provisions.',
                 'Compute self-assessment and updated-return tax.',
                 'Distinguish types of assessment and the DRP route.',
                 'Apply reassessment conditions and time limits.',
                 'Apply rectification, block assessment and transition rules.'],
                {'difficulty': 'hard', 'minutes': {'learn': 55, 'practice': 35}, 'prereq': ['fin-p4-ch14-u01'],
                 'exam_tip': 'For time-limit questions, write the reference date first, then add the period.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 263 returns: 31 July/31 August/31 October/30 November.', 'Belated 9 months; revised 12 months; updated 48 months.', 'Section 267: 25/50/60/70% additional tax.',
                             'Sections 270, 271, 273, 275 assessments.', 'Sections 279–282 reassessment; 286 time limits; 287 rectification.'],
                 'remember': ['Reassessment notice: 4y3m or 6y3m.'],
                 'traps': ['Using an updated return to raise a refund.']},
                [('Returns', 'Section 263'), ('Updated return tax', 'Section 267'), ('Assessment', 'Section 270'), ('Reassessment', 'Sections 279–282'), ('Rectification', 'Section 287')],
                viva, cases)
