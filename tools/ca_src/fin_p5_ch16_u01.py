"""CA Final · Paper 5 · Chapter 16 Job Work.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch16-u01'
T1 = 'Meaning of job work and the principal\'s option'
T2 = 'Time limits for return of goods'
T3 = 'ITC on goods sent for job work'
T4 = 'Supplies from job worker premises and compliance'


def build():
    ck = Checks()
    t = ck.add('400000*0.18', 'Tax payable on inputs deemed supplied at 18% (₹)')
    i1 = {'id': 'i1', 'title': 'Inputs not returned in time', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Uday Industries sent inputs worth ₹4,00,000 (18%) to a job worker on 15 August 2026 under section 143 and capital goods on the same day. Neither has returned by 15 August 2027. State the consequences for inputs and the time left for capital goods.',
          'solution': [table(['Item', 'Rule', 'Result'], [
              ['Inputs', 'Not returned within one year — deemed supplied on the day they were sent', f'Tax ₹{inr(t)} with interest from 15 August 2026'],
              ['Capital goods', 'Three years allowed', 'Return by 15 August 2029'],
              ['Later return', 'A registered job worker returning them later makes its own taxable supply back', 'Tax on return']], title='Section 143')],
          'checks': list(ck)}

    c2 = Checks()
    f = c2.add('4', 'Number of permitted cases for supplying directly from job worker premises discussed')
    i2 = {'id': 'i2', 'title': 'Direct supply and waste', 'difficulty': 'core', 'minutes': 6,
          'q': 'Vimal Ltd (registered principal) sends fabric to a job worker. (a) Can finished garments be sold directly from the job worker\'s premises? (b) Who pays GST on fabric waste sold by the job worker? (c) Must Vimal file ITC-04 if its turnover is ₹3 crore?',
          'solution': [table(['Point', 'Rule', 'Answer'], [
              ['(a)', 'Allowed if the principal declares the job worker\'s premises as additional place of business, or the job worker is registered, or goods are notified', 'Yes — invoice by Vimal'],
              ['(b)', 'Waste sold by a registered job worker is taxed in its hands; otherwise by the principal', 'Job worker if registered'],
              ['(c)', 'Turnover up to ₹5 crore: annual ITC-04 by 25 April', 'Yes, annually']], title='Section 143 and rule 45')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Under section 2(68), job work means a person processing or treating goods that a different registered person owns. The job worker supplies a service; the principal retains ownership of the goods.',
            'Section 143 lets a registered principal send inputs and capital goods to a job worker without paying tax, under a delivery challan, and bring them back or supply them from the job worker\'s place within time limits. Using section 143 is optional — the principal may instead supply goods on payment of tax.',
            'Goods may move directly from the supplier to the job worker, and from one job worker to another, under section 143.'],
          'Job work moves goods without tax as long as the principal keeps ownership.',
          'A garment maker sends fabric to a stitching unit on a challan.'),
        C('c2', T2, [
            'Inputs must be brought back or supplied within one year, and capital goods within three years, of being sent; extendable by the Commissioner by up to one year and two years respectively. Moulds and dies, jigs and fixtures and tools are exempt from the time limit.',
            'If not returned or supplied within time, the law treats the principal as having supplied the inputs or capital goods to the job worker on the original dispatch date, with interest from then.',
            'Where goods are sent directly from the supplier to the job worker, the period runs from the date the job worker receives them.'],
          'One year for inputs, three for capital goods — or tax as deemed supply.',
          'Inputs sent on 15 August 2026 must return by 15 August 2027.'),
        C('c3', T3, [
            'Section 19: the principal may take ITC on inputs and capital goods sent to a job worker, including where they are sent directly from the supplier without first reaching the principal.',
            'If inputs are not returned within one year (capital goods three years), ITC is effectively recovered through the deemed supply tax; the principal can take credit again when the goods return.',
            'There is no time limit for moulds, dies, jigs, fixtures or tools, so no deemed supply arises for them.'],
          'Credit stays with the principal even when goods sit with the job worker.',
          'Capital goods delivered straight to a job worker still qualify for ITC.'),
        C('c4', T4, [
            'Goods can be supplied directly from the job worker\'s place — within India on payment of tax or for export with or without tax — if the principal declares the job worker\'s premises as an additional place of business, or the job worker is registered, or the goods are notified.',
            'Waste and scrap generated during job work may be supplied by a registered job worker on payment of tax, or by the principal where the job worker is not registered.',
            'The principal must furnish Form GST ITC-04 with details of goods sent and received: half-yearly by 25 October and 25 April for turnover above ₹5 crore, and annually by 25 April otherwise. The job worker must register if its own turnover crosses the threshold, and inter-State movement to a job worker requires an e-way bill irrespective of value.'],
          'Direct sales and waste follow the job worker\'s registration status.',
          'A ₹3 crore principal files ITC-04 once a year by 25 April.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Job work tracker', 'role': 'Plant accountant',
             'situation': 'A manufacturer uses ten job workers across States.',
             'steps': ['Issue delivery challans for each dispatch.', 'Track one-year and three-year deadlines.', 'Pay tax on overdue items with interest.', 'File ITC-04 on time.'],
             'takeaway': 'Ageing reports prevent deemed supplies.'}]

    mcqs = [
        Q('m1', 'Job work means processing of goods belonging to:', ['Another registered person', 'The job worker', 'Any unregistered person', 'The Government'], 0,
          'Section 2(68). In practice: ownership stays with principal.', 'c1', T1),
        Q('m2', 'Inputs sent for job work must be returned within:', ['One year', 'Three years', 'Six months', 'Two years'], 0,
          'Section 143(1)(a). In practice: extendable by one year.', 'c2', T2),
        Q('m3', 'Capital goods sent for job work must be returned within:', ['Three years', 'One year', 'Five years', 'Two years'], 0,
          'Section 143(1)(b). In practice: extendable by two years.', 'c2', T2),
        Q('m4', 'Which items have no time limit for return?', ['Moulds and dies, jigs and fixtures, tools', 'Raw materials', 'Packing materials', 'Semi-finished goods'], 0,
          'Proviso to section 143. In practice: no deemed supply.', 'c2', T2),
        Q('m5', 'If inputs are not returned in time, they are deemed supplied on:', ['The day they were sent', 'The day of expiry', 'The return date', 'Year-end'], 0,
          'Section 143(3). In practice: interest from that day.', 'c2', T2),
        Q('m6', 'Can the principal take ITC on inputs sent directly from supplier to job worker?', ['Yes', 'No', 'Only after return', 'Only for capital goods'], 0,
          'Section 19. In practice: conditions apply.', 'c3', T3),
        Q('m7', 'ITC-04 for a principal with turnover of ₹8 crore is filed:', ['Half-yearly', 'Annually', 'Monthly', 'Quarterly'], 0,
          'Rule 45(3). In practice: 25 October and 25 April.', 'c4', T4),
        Q('m8', 'Waste generated at an unregistered job worker\'s premises is supplied by:', ['The principal', 'The job worker', 'Nobody', 'The transporter'], 0,
          'Section 143(5). In practice: principal pays tax.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Inputs', 3, 'computation', 'deemed', nums=[t]), S('s2', 'Capital goods', 2, 'analysis', 'three years')],
          ['Mention interest.'], ['Using the expiry date as the deemed date.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Direct supply and waste', 2, 'analysis', 'registered', nums=[f]), S('s2', 'ITC-04', 2, 'analysis', 'annual')],
          ['State conditions.'], ['Making the job worker invoice the principal\'s sales.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Is section 143 mandatory for job work?', 'It is optional; the principal may instead send goods on payment of tax.',
          [P('p1', 'Optional', 5, 'optional'), P('p2', 'Payment of tax', 5, 'payment of tax')], 'c1'),
        V('v2', 'From when does the time limit run for goods sent directly by a supplier to a job worker?', 'From the date the job worker receives them.',
          [P('p1', 'Date received', 5, 'receive'), P('p2', 'Job worker', 5, 'job worker')], 'c2'),
        V('v3', 'What document accompanies goods sent for job work?', 'A delivery challan issued by the principal.',
          [P('p1', 'Delivery challan', 5, 'delivery challan'), P('p2', 'Principal', 5, 'principal')], 'c4'),
        V('v4', 'Can goods be exported directly from the job worker\'s premises?', 'Yes, exports may go straight from there, with or without payment of tax, subject to conditions.',
          [P('p1', 'Exports', 5, 'exports'), P('p2', 'With or without tax', 5, 'with or without')], 'c4'),
        V('v5', 'What happens to ITC when inputs come back after deemed supply?', 'The principal can take credit again on the return.',
          [P('p1', 'Credit again', 5, 'again'), P('p2', 'Return', 5, 'return')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Precision Moulds', 'difficulty': 'core',
              'case': 'Kiran Auto sends moulds worth ₹10,00,000 and raw steel worth ₹6,00,000 to a job worker on 1 April 2026. The steel is not returned by 1 April 2027; the moulds remain with the job worker in 2029.',
              'mcqs': [
                  M('k1a', 'Tax payable on steel deemed supplied at 18% (₹):', ['1,08,000', '1,80,000', 'Nil', '2,88,000'], 0,
                    '18% × 6 lakh. In practice: plus interest.', 'core', check=108000, topic=T2),
                  M('k1b', 'Deemed supply date for steel:', ['1 April 2026', '1 April 2027', '31 March 2027', '2 April 2027'], 0,
                    'Day sent out. In practice: interest from then.', 'core', topic=T2),
                  M('k1c', 'Tax on moulds still at the job worker in 2029:', ['Nil — no time limit', '18% deemed supply', 'Customs duty', '5%'], 0,
                    'Exception. In practice: record in ITC-04.', 'core', topic=T2),
                  M('k1d', 'Kiran\'s turnover is ₹12 crore. ITC-04 frequency:', ['Half-yearly', 'Annual', 'Monthly', 'Not required'], 0,
                    'Above ₹5 crore. In practice: 25 October/25 April.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch16', 1, 'Job Work',
                ['Explain job work and the principal\'s option under section 143.',
                 'Apply time limits and deemed supply rules.',
                 'Apply ITC rules for goods sent for job work.',
                 'Apply direct supply, waste and compliance provisions.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 20}, 'prereq': ['fin-p5-ch15-u01'],
                 'exam_tip': 'Count the time limit from dispatch (or receipt by the job worker) and state the deemed supply date.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 2(68) job work; section 143 optional procedure.', 'Inputs 1 year, capital goods 3 years; moulds exempt.', 'Deemed supply on date sent out.',
                             'Section 19 ITC including direct dispatch.', 'ITC-04: half-yearly > ₹5 crore, annual otherwise.'],
                 'remember': ['Inter-State job work needs EWB regardless of value.'],
                 'traps': ['Taxing moulds after three years.']},
                [('Job work', 'Section 143'), ('ITC', 'Section 19'), ('ITC-04', 'Rule 45')],
                viva, cases)
