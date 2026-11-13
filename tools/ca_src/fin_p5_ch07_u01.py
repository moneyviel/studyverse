"""CA Final · Paper 5 · Chapter 7 Input Tax Credit.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch07-u01'
T1 = 'Eligibility and conditions for ITC'
T2 = 'Blocked credits'
T3 = 'Apportionment of common credit'
T4 = 'ITC in special circumstances and ISD'


def build():
    ck = Checks()
    c1 = ck.add('1000000-50000-100000-50000', 'C1: credit after removing non-business, exempt and blocked (₹)')
    c2 = ck.add('1000000-50000-100000-50000-400000', 'C2: common credit (₹)')
    d1 = ck.add('400000*20/100', 'D1: common credit attributable to exempt supplies (₹)')
    d2 = ck.add('400000*0.05', 'D2: common credit for non-business use at 5% (₹)')
    el = ck.add('400000+400000-400000*20/100-400000*0.05', 'Total eligible ITC (₹)')
    i1 = {'id': 'i1', 'title': 'Rule 42 apportionment', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Indira Foods Ltd has total ITC of ₹10,00,000 for a month: exclusively for non-business ₹50,000; exclusively for exempt supplies ₹1,00,000; blocked under section 17(5) ₹50,000; exclusively for taxable supplies ₹4,00,000; the rest is common. Exempt turnover is ₹20 crore out of total turnover of ₹100 crore. Compute eligible ITC.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['C1', 'T − (T1 + T2 + T3)', inr(c1)],
              ['C2 (common)', 'C1 − M (exclusive taxable)', inr(c2)],
              ['D1 (exempt share)', 'C2 × 20/100', inr(d1)],
              ['D2 (non-business)', '5% of C2', inr(d2)],
              ['Eligible ITC', 'M + (C2 − D1 − D2)', inr(el)]], title='Rule 42')],
          'checks': list(ck)}

    c2c = Checks()
    al = c2c.add('90000+18000', 'Eligible ITC: machinery and goods truck (₹)')
    i2 = {'id': 'i2', 'title': 'Which credits are blocked?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Mehta Industries paid GST on: plant and machinery ₹90,000; a goods transport truck ₹18,000; a 5-seater car for directors ₹1,40,000; outdoor catering for an annual party ₹12,000; construction of a factory shed (works contract) ₹2,50,000; club membership for the MD ₹9,000. Compute eligible ITC.',
          'solution': [table(['Item', 'Treatment', 'ITC (₹)'], [
              ['Plant and machinery', 'Eligible', '90,000'],
              ['Goods truck', 'Eligible — used for transport of goods', '18,000'],
              ['Car for directors', 'Blocked — motor vehicle ≤ 13 seats', '—'],
              ['Outdoor catering', 'Blocked — food and beverages', '—'],
              ['Factory shed', 'Blocked — construction of immovable property', '—'],
              ['Club membership', 'Blocked', '—'],
              ['Total eligible', '', inr(al)]], title='Section 17(5)')],
          'checks': list(c2c)}

    concepts = [
        C('c1', T1, [
            'Section 16(1) allows a registered person to take credit of tax charged on inward supplies that serve, or are meant to serve, its business. Section 16(2) conditions: possession of a tax invoice or debit note; the details furnished by the supplier and appearing in GSTR-2B; receipt of goods or services (including bill-to-ship-to and delivery to agents); tax actually paid by the supplier; and the recipient having filed its return.',
            'Payment must be made to the supplier within 180 days of the invoice; otherwise the ITC is reversed with interest and re-availed on payment (RCM, deemed supplies without consideration excluded). Goods received in lots: credit on the last lot. ITC is not available on tax component if depreciation is claimed on it.',
            'Section 16(4): ITC for a financial year must be taken by 30 November of the next year or the annual return date, whichever earlier (with specific relaxations for earlier years and revocation cases). Rule 86B restricts use of credit to 99% of output tax for certain high-value taxpayers.'],
          'Invoice, 2B, receipt, tax paid, return filed — and pay within 180 days.',
          'An invoice for October 2026 must be claimed by 30 November 2027.'),
        C('c2', T2, [
            'Section 17(5) blocks credit on: motor vehicles for transport of persons with seating up to 13 (unless used for further supply, passenger transport, driving training, or transport of goods), and their repair, insurance and servicing; vessels and aircraft (with exceptions); eatables and drinks, catering, beauty and health services, cosmetic and plastic surgery, life and health cover, club and fitness memberships, and leave or home travel for staff — unless obligatory for employers under law or used for the same category of outward supply.',
            'Also blocked: works contract services and inputs used to build immovable property on own account (plant and machinery apart), even when used in business; composition tax; goods or services received by non-residents (except imports); goods or services for personal consumption; goods lost, stolen, destroyed, written off or gifted; tax paid under sections 74, 129 and 130.',
            '"Plant and machinery" includes foundations and structural supports but excludes land, buildings, civil structures, telecom towers and pipelines laid outside factory premises.'],
          'Personal-type and construction expenses are blocked.',
          'GST on a car for directors is blocked; on a goods truck it is allowed.'),
        C('c3', T3, [
            'Section 17(1) and (2) restrict credit to the extent of business use and taxable (including zero-rated) supplies. Rule 42 apportions common input and input service credit monthly: remove credits for non-business (T1), exempt (T2) and blocked (T3) items; the remainder C1 less exclusive taxable credit (M) gives common credit C2; then D1 = (exempt turnover ÷ total turnover) × C2 and D2 = 5% of C2 are reversed.',
            'Rule 43 apportions ITC on capital goods: credit on goods used exclusively for exempt or non-business purposes is not taken; for common capital goods, credit is spread over 60 months (5% per quarter) and the share attributable to exempt supplies reversed monthly.',
            'Final reversal is computed for the whole year by the due date of the September return, with interest on excess claimed. Exempt supplies include specified transactions such as securities (1% of value) and land (value as stamp duty).'],
          'Common credit is shared by turnover ratio, with 5% deemed non-business.',
          'With 20% exempt turnover, ₹4 lakh of common credit yields ₹3 lakh eligible.'),
        C('c4', T4, [
            'Section 18: credit on stock and capital goods on new registration (within 30 days), on switching from composition to regular scheme, or when exempt supplies become taxable. On switching to composition or supplies becoming exempt, credit on stock is reversed. On sale of capital goods, tax payable is the higher of ITC taken less 5% per quarter and tax on transaction value.',
            'Section 20: an Input Service Distributor must distribute credit of common input services (including RCM services from 1 April 2025) to units in the ratio of turnover, through ISD invoices, in the same month; excess distribution is recoverable with interest.',
            'Section 41 and rule 37: credit is availed self-assessed; non-payment of supplier dues within 180 days, or mismatches, lead to reversal.'],
          'Credit follows registration changes, transfers and distribution.',
          'A newly registered dealer can claim ITC on stock held on the day before registration.'),
    ]

    jobs = [{'id': 'j1', 'title': 'ITC reconciliation', 'role': 'GST manager',
             'situation': 'A company with exempt and taxable supplies prepares its monthly return.',
             'steps': ['Match purchase register with GSTR-2B.', 'Remove blocked credits.', 'Apply rule 42 and 43.', 'Track 180-day payment and 30 November deadline.'],
             'takeaway': 'Credit errors often surface only in audit — reconcile monthly.'}]

    mcqs = [
        Q('m1', 'Payment to the supplier must be made within how many days of invoice to retain ITC?', ['One hundred eighty', 'Ninety', 'Sixty', 'Three hundred sixty-five'], 0,
          'Second proviso to section 16(2). In practice: reverse with interest.', 'c1', T1),
        Q('m2', 'ITC for 2026-27 must be availed by the earlier of the annual return date and:', ['30 November 2027', '31 March 2027', '30 September 2027', '31 December 2027'], 0,
          'Section 16(4). In practice: track invoices.', 'c1', T1),
        Q('m3', 'ITC on a motor car with seating up to thirteen used by directors is:', ['Blocked', 'Allowed', 'Allowed at 50%', 'Allowed if registered'], 0,
          'Section 17(5)(a). In practice: exceptions for specified uses.', 'c2', T2),
        Q('m4', 'ITC on works contract for constructing a factory building is:', ['Blocked', 'Allowed', 'Allowed if plant', 'Allowed at 5%'], 0,
          'Section 17(5)(c). In practice: plant and machinery excepted.', 'c2', T2),
        Q('m5', 'Under rule 42, the deemed non-business portion of common credit is:', ['Five percent', 'Ten percent', 'Two percent', 'Nil'], 0,
          'D2. In practice: monthly.', 'c3', T3),
        Q('m6', 'Capital goods credit under rule 43 is spread over:', ['Sixty months', 'Thirty-six months', 'Twelve months', 'One hundred twenty months'], 0,
          'Useful life. In practice: 5% per quarter.', 'c3', T3),
        Q('m7', 'On new registration, ITC on stock can be claimed if application is made within:', ['Thirty days of liability', 'Ninety days', 'One year', 'Seven days'], 0,
          'Section 18(1)(a). In practice: stock held day before.', 'c4', T4),
        Q('m8', 'Rule 86B restricts use of ITC for output tax to:', ['Ninety-nine percent', 'Ninety percent', 'Eighty percent', 'Fifty percent'], 0,
          'High-value taxpayers. In practice: exceptions apply.', 'c1', T1),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'C1 and C2', 3, 'computation', 'common', nums=[c1, c2]), S('s2', 'D1 and D2', 3, 'computation', 'exempt', nums=[d1, d2]), S('s3', 'Eligible ITC', 2, 'computation', 'eligible', nums=[el])],
          ['Use rule notation.'], ['Applying turnover ratio to total ITC.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Blocked items', 3, 'analysis', 'blocked'), S('s2', 'Eligible total', 2, 'computation', 'eligible', nums=[al])],
          ['Cite clauses.'], ['Blocking plant and machinery.'], ['Table.'], pad='table', checks=list(c2c)),
    ]

    viva = [
        V('v1', 'Can ITC be taken without the invoice appearing in GSTR-2B?', 'It is barred: the supplier\'s details must appear in GSTR-2B under section 16(2)(aa).',
          [P('p1', 'Barred', 5, 'barred'), P('p2', 'GSTR-2B', 5, '2b')], 'c1'),
        V('v2', 'When is ITC on food and beverages allowed?', 'When provision to employees is obligatory under a law, or when used for making an outward supply of the same category.',
          [P('p1', 'Obligatory under law', 5, 'obligatory'), P('p2', 'Same category', 5, 'same category')], 'c2'),
        V('v3', 'What happens when capital goods with ITC are sold?', 'Tax payable is the higher of ITC taken less 5% per quarter of use and tax on the transaction value.',
          [P('p1', 'Five percent per quarter', 5, '5% per quarter'), P('p2', 'Transaction value', 5, 'transaction value')], 'c4'),
        V('v4', 'How does an ISD distribute credit?', 'To units using the services, in the ratio of their turnover, through ISD invoices in the same month.',
          [P('p1', 'Turnover ratio', 5, 'turnover'), P('p2', 'ISD invoices', 5, 'isd invoice')], 'c4'),
        V('v5', 'Can depreciation be claimed on the GST component along with ITC?', 'ITC is denied on the tax portion if depreciation is claimed on it.',
          [P('p1', 'Denied', 5, 'denied'), P('p2', 'Depreciation', 5, 'depreciation')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Late payment to supplier', 'difficulty': 'core',
              'case': 'Rana Textiles took ITC of ₹54,000 on a supplier invoice dated 1 April 2026 for ₹3,00,000 plus GST. By 1 October 2026 it had not paid the supplier. It pays in full on 15 December 2026.',
              'mcqs': [
                  M('k1a', 'ITC to be reversed after 180 days (₹):', ['54,000', '27,000', 'Nil', '3,00,000'], 0,
                    'Unpaid in full. In practice: next return.', 'core', check=54000, topic=T1),
                  M('k1b', 'Is interest payable on the reversal?', ['Yes', 'No', 'Only if fraud', 'Only above ₹1 lakh'], 0,
                    'Section 50. In practice: from date of availment.', 'core', topic=T1),
                  M('k1c', 'Can ITC be re-availed after payment on 15 December?', ['Yes', 'No', 'Only in the next year', 'Only with officer approval'], 0,
                    'Third proviso to section 16(2). In practice: subject to time limit.', 'core', topic=T1),
                  M('k1d', 'Days in the 180-day window from 1 April 2026:', ['180', '90', '365', '60'], 0,
                    'Statutory period. In practice: track ageing.', 'core', check=180, topic=T1),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch07', 1, 'Input Tax Credit',
                ['Apply eligibility conditions and time limits for ITC.',
                 'Identify blocked credits.',
                 'Apportion common credit under rules 42 and 43.',
                 'Apply ITC in special circumstances and ISD rules.'],
                {'difficulty': 'hard', 'minutes': {'learn': 60, 'practice': 40}, 'prereq': ['fin-p5-ch06-u01'],
                 'exam_tip': 'Strip blocked and exclusive credits first; apportion only the common pool.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 16 conditions; 2B; 180-day payment; 30 November limit.', 'Section 17(5) blocked credits.', 'Rule 42: C1, C2, D1, D2; rule 43 capital goods.',
                             'Section 18 special cases; section 20 ISD.', 'Rule 86B: 99% cap.'],
                 'remember': ['Goods truck ITC is allowed.'],
                 'traps': ['Blocking ITC on plant and machinery foundations.']},
                [('Eligibility', 'Section 16'), ('Apportionment', 'Section 17(1)–(2)'), ('Blocked', 'Section 17(5)'), ('Special cases', 'Section 18'), ('ISD', 'Section 20')],
                viva, cases)
