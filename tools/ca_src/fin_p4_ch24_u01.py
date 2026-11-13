"""CA Final · Paper 4 · Chapter 24 Transfer Pricing.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch24-u01'
T1 = 'Associated enterprises and covered transactions'
T2 = 'Methods and determination of arm\'s length price'
T3 = 'TPO reference, safe harbour and APA'
T4 = 'Secondary adjustment, documentation and penalties'


def build():
    ck = Checks()
    p35 = ck.add('11', '35th percentile margin (%)')
    p65 = ck.add('19', '65th percentile margin (%)')
    med = ck.add('(13+16)/2', 'Median margin (%)')
    adj = ck.add('1000000000*((13+16)/2-8)/100', 'Transfer pricing adjustment (₹)')
    i1 = {'id': 'i1', 'title': 'Range, median and adjustment', 'difficulty': 'hard', 'minutes': 9,
          'q': 'Indigo Services Pvt Ltd provides software services to its US parent. Its operating cost is ₹100 crore and it earned a margin of 8% on cost. Using TNMM, eight comparables (in ascending order) show margins of 6%, 9%, 11%, 13%, 16%, 19%, 21% and 24%. Determine the arm\'s length range and any adjustment.',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['35th percentile', '8 × 35% = 2.8 → 3rd value', f'{p35}%'],
              ['65th percentile', '8 × 65% = 5.2 → 6th value', f'{p65}%'],
              ['Tested margin', '8% lies outside 11%–19%', 'Adjust'],
              ['Median', '8 × 50% = 4 (whole) → mean of 4th and 5th', f'{med}%'],
              ['Adjustment', '100 crore × (14.5% − 8%)', inr(adj)]], title='Section 165(3), Rule 81')],
          'checks': list(ck)}

    c2 = Checks()
    sa = c2.add('15000000', 'Primary adjustment (₹)')
    i2 = {'id': 'i2', 'title': 'Secondary adjustment', 'difficulty': 'moderate', 'minutes': 5,
          'q': 'Pristine Chemicals Ltd accepts a primary adjustment of ₹1,50,00,000 made by the AO on its export price to a foreign AE. The AE does not remit the excess money. Explain the consequence.',
          'solution': [table(['Item', 'Rule', 'Result'], [
              ['Threshold', f'Primary adjustment ₹{inr(sa)} ≥ ₹1 crore and accepted', 'Secondary adjustment applies'],
              ['Repatriation', 'Excess money to come back within 90 days of the relevant date', 'Not done'],
              ['Consequence', 'Deemed advance to AE; interest computed as prescribed', 'Taxable interest yearly']], title='Section 170, Rule 83')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 161: income from an international transaction or specified domestic transaction must be computed at arm\'s length price (ALP); the rule cannot reduce income or increase loss.',
            'Associated enterprises (section 162): participation in management, control or capital, including 26% or more voting power held directly or indirectly; loans of 51% or more of book value of assets; guarantees of 10% or more of borrowings; appointment of more than half the board; complete dependence on know-how; 90% or more of raw materials supplied by the other at prices it influences; common control and specified firm or AOP interests.',
            'International transactions (section 163) include purchase, sale or lease of tangible or intangible property, services, lending or borrowing, guarantees, cost-sharing and business restructuring between AEs where at least one is non-resident; transactions with third parties under prior arrangement with an AE are deemed international. Specified domestic transactions (section 164) between related parties apply where aggregate value exceeds ₹20 crore.'],
          'Related parties must deal as strangers would.',
          'An Indian subsidiary paying royalty to its foreign parent is in an international transaction.'),
        C('c2', T2, [
            'Section 165 methods: comparable uncontrolled price, resale price, cost plus, profit split, transactional net margin, and other methods prescribed. The most appropriate method is chosen considering the nature of the transaction, functions, assets and risks (FAR), availability and reliability of data and adjustments possible.',
            'Where the method gives one price, that is the ALP; if the actual price varies from it by no more than the notified tolerance (up to 3%), the actual price is accepted. Where there are six or more comparables (and the method is not profit split), the arm\'s length range is the 35th to 65th percentile; a result within the range is accepted, otherwise the median is used. With fewer than six entries the arithmetic mean applies, with the tolerance band.',
            'Percentiles and median are positions found by multiplying the number of values by 35%, 65% or 50%: if the result is a whole number, the mean of that value and the next is taken; otherwise the next higher position. Multiple-year data may be used.'],
          'Find the right method, build the range, adjust to the median if outside.',
          'A margin of 8% against a range of 11%–19% is adjusted to the median of 14.5%.'),
        C('c3', T3, [
            'Section 166: the AO may, with approval, refer computation of ALP to a Transfer Pricing Officer (TPO), who may also examine transactions not reported if they come to notice; the AO computes total income in conformity with the TPO\'s order. Time limits are extended for TP references.',
            'Section 167 safe harbour rules prescribe circumstances in which the department accepts the transfer price declared (e.g. specified margins for IT services or interest rates), for a period of up to five consecutive tax years once opted.',
            'Section 168 Advance Pricing Agreements fix the ALP or method for up to five future years, binding on the assessee and the department for those transactions unless facts or law change; rollback can extend the agreed method to up to four earlier years. APAs may be unilateral, bilateral or multilateral (section 169 on effect).'],
          'Certainty comes through safe harbours or APAs.',
          'An APA signed for five years with rollback covers nine years of transactions.'),
        C('c4', T4, [
            'Section 170: where a primary adjustment of ₹1 crore or more is made suo motu, accepted after AO\'s order, agreed in an APA, under safe harbour, or via MAP, the excess money with the AE must be repatriated within 90 days; otherwise it is deemed an advance and interest is imputed.',
            'Section 171 requires maintenance of prescribed information and documents (Rule 84) where international transactions exceed ₹1 crore, master file, and country-by-country reporting for large groups (section 511). Section 172 requires a CA report (Form No. 48) by one month before the return due date.',
            'Failures attract penalties: 2% of transaction value for not maintaining or furnishing documentation (section 442), fees for not furnishing the report (section 428(d)), 200% penalty for under-reporting from unreported transactions (section 439(11)(f)), and specified penalties for CbCR defaults (section 459).'],
          'Adjust, repatriate, document — or pay more.',
          'An accepted ₹1.5 crore adjustment left abroad becomes a deemed loan earning taxable interest.'),
    ]

    jobs = [{'id': 'j1', 'title': 'TP study for a captive', 'role': 'Transfer pricing consultant',
             'situation': 'An Indian captive service centre bills its foreign parent at cost plus 8%.',
             'steps': ['Perform FAR analysis and pick TNMM.', 'Search comparables and build the range.', 'Assess safe harbour or APA options.', 'Prepare Form No. 48 and documentation.'],
             'takeaway': 'Well-chosen comparables are the strongest defence.'}]

    mcqs = [
        Q('m1', 'Holding voting power of at least how much makes enterprises associated?', ['Twenty-six percent', 'Fifty-one percent', 'Ten percent', 'Twenty percent'], 0,
          'Section 162. In practice: direct or indirect.', 'c1', T1),
        Q('m2', 'Specified domestic transactions are covered when aggregate value exceeds:', ['Twenty crore rupees', 'Five crore rupees', 'One crore rupees', 'Fifty crore rupees'], 0,
          'Section 164. In practice: related parties.', 'c1', T1),
        Q('m3', 'The arm\'s length range is used when the dataset has at least:', ['Six entries', 'Three entries', 'Ten entries', 'Two entries'], 0,
          'Rule 81. In practice: not for PSM.', 'c2', T2),
        Q('m4', 'The arm\'s length range runs from the:', ['Thirty-fifth to sixty-fifth percentile', 'Twenty-fifth to seventy-fifth percentile', 'Minimum to maximum', 'Fortieth to sixtieth percentile'], 0,
          'Rule 81. In practice: median if outside.', 'c2', T2),
        Q('m5', 'Tolerance for single-price ALP cannot exceed:', ['Three percent', 'Five percent', 'One percent', 'Ten percent'], 0,
          'Section 165(3). In practice: notified per sector.', 'c2', T2),
        Q('m6', 'An APA can cover future years up to:', ['Five', 'Three', 'Ten', 'Two'], 0,
          'Section 168. In practice: plus rollback.', 'c3', T3),
        Q('m7', 'Secondary adjustment applies where primary adjustment is at least:', ['One crore rupees', 'Fifty lakh rupees', 'Ten crore rupees', 'Twenty crore rupees'], 0,
          'Section 170. In practice: 90-day repatriation.', 'c4', T4),
        Q('m8', 'Penalty for failure to maintain TP documentation is:', ['Two percent of transaction value', 'Ten thousand rupees', 'Two hundred percent of tax', 'One lakh rupees'], 0,
          'Section 442. In practice: per transaction.', 'c4', T4),
    ]

    questions = [
        W('q1', 7, i1['q'], i1['solution'],
          [S('s1', 'Range', 3, 'computation', 'percentile', nums=[p35, p65]), S('s2', 'Median and adjustment', 4, 'computation', 'median', nums=[med, adj])],
          ['Show positions.'], ['Using the nearest rather than next higher position.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Conditions', 2, 'analysis', '1 crore', nums=[sa]), S('s2', 'Consequence', 2, 'analysis', 'deemed advance')],
          ['State 90-day rule.'], ['Ignoring acceptance condition.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Can transfer pricing reduce taxable income?', 'Section 161 adjustments cannot reduce income or increase loss.',
          [P('p1', 'Cannot reduce', 5, 'cannot reduce'), P('p2', 'Loss', 5, 'loss')], 'c1'),
        V('v2', 'What is a deemed international transaction?', 'A transaction with an unrelated party where a prior agreement or arrangement with an AE determines its terms.',
          [P('p1', 'Unrelated party', 5, 'unrelated'), P('p2', 'Prior arrangement', 5, 'prior')], 'c1'),
        V('v3', 'What does FAR analysis cover?', 'The functions performed, assets used and risks assumed by each party.',
          [P('p1', 'Functions', 5, 'functions'), P('p2', 'Risks', 5, 'risks')], 'c2'),
        V('v4', 'What is rollback in an APA?', 'Applying the agreed method to up to four years before the APA period.',
          [P('p1', 'Earlier years', 5, 'before'), P('p2', 'Four years', 5, 'four years')], 'c3'),
        V('v5', 'By when must Form No. 48 be furnished?', 'One month before the due date of the return.',
          [P('p1', 'One month', 5, 'one month'), P('p2', 'Due date', 5, 'due date')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Delta Auto Components', 'difficulty': 'moderate',
              'case': 'Delta Auto Components Ltd buys parts from its German parent for ₹40 crore. Under CUP, a single comparable price of ₹38.9 crore is found. The notified tolerance for this sector is 3%.',
              'mcqs': [
                  M('k1a', 'Variation between actual and ALP (₹ crore):', ['1.1', '3.0', '0.9', '1.9'], 0,
                    '40 − 38.9. In practice: compare with tolerance.', 'core', check=1.1, topic=T2),
                  M('k1b', 'Variation as a percentage of ALP (approx.):', ['2.83%', '3.5%', '1.1%', '4%'], 0,
                    '1.1 ÷ 38.9 × 100. In practice: within 3%.', 'core', check=round(1.1/38.9*100,2), topic=T2),
                  M('k1c', 'Is an adjustment required?', ['No, variation is within tolerance', 'Yes, ₹1.1 crore', 'Yes, ₹40 crore', 'Only if TPO says'], 0,
                    'Section 165(3). In practice: actual price accepted.', 'core', topic=T2),
                  M('k1d', 'Is the German parent an associated enterprise if it holds 60% of Delta?', ['Yes', 'No', 'Only if it guarantees loans', 'Only if it appoints all directors'], 0,
                    '26% or more. In practice: section 162.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch24', 1, 'Transfer Pricing',
                ['Identify associated enterprises and covered transactions.',
                 'Determine ALP using methods, range and median.',
                 'Apply TPO reference, safe harbour and APA provisions.',
                 'Apply secondary adjustment, documentation and penalty provisions.'],
                {'difficulty': 'hard', 'minutes': {'learn': 55, 'practice': 35}, 'prereq': ['fin-p4-ch23-u01'],
                 'exam_tip': 'For range questions show the position arithmetic explicitly.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 161 ALP; 162 AE (26%); 163 international; 164 SDT ₹20 crore.', 'Section 165: methods; range 35th–65th; median; 3% tolerance.', 'Sections 166–169: TPO, safe harbour, APA (5 + 4 rollback).',
                             'Section 170 secondary adjustment ≥ ₹1 crore; 90 days.', 'Sections 171, 172, 442, 511: documentation, Form 48, penalties, CbCR.'],
                 'remember': ['Whole-number position → average with next value.'],
                 'traps': ['Using arithmetic mean when six or more comparables exist.']},
                [('ALP', 'Section 161'), ('AE', 'Section 162'), ('Methods', 'Section 165'), ('APA', 'Section 168'), ('Secondary adjustment', 'Section 170')],
                viva, cases)
