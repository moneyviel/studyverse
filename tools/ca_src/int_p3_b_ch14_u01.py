"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 14 Tax Deduction at Source and Collection of Tax at Source.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch14-u01'
T1 = 'Who deducts GST TDS and when (s. 51)'
T2 = 'Deposit, returns and certificates for TDS'
T3 = 'TCS by electronic commerce operators (s. 52)'


def build():
    ck = Checks()
    t_a = ck.add('300000*2/100', 'TDS on ₹3,00,000 (intra-State: 1% CGST + 1% SGST)')
    t_c = ck.add('400000*2/100', 'TDS on ₹4,00,000 inter-State (2% IGST)')
    i1 = {'id': 'i1', 'title': 'A municipality pays its contractors', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Pune Municipal Corporation (registered in Maharashtra) pays: (a) a Pune contractor ₹3,00,000 + GST for road repair materials; (b) a Pune supplier ₹2,00,000 + GST for stationery; (c) a Hyderabad firm ₹4,00,000 + IGST for software services where the place of supply is Maharashtra; (d) a Mumbai supplier ₹5,00,000 for exempt goods. Compute GST TDS.',
          'solution': [table(['Case', 'TDS?', 'Working', '₹'], [
              ['(a)', 'Yes', 'Taxable value above ₹2,50,000: 1% CGST + 1% SGST', inr(t_a)],
              ['(b)', 'No', 'Contract value does not exceed ₹2,50,000', '0'],
              ['(c)', 'Yes', 'Inter-State, place of supply in the deductor\'s State: 2% IGST', inr(t_c)],
              ['(d)', 'No', 'TDS applies only to taxable supplies', '0']], title='Section 51')],
          'checks': list(ck)}

    ck2 = Checks()
    net = ck2.add('1500000-100000', 'Net value of taxable supplies through the ECO')
    tcs = ck2.add('1400000*0.5/100', 'TCS at 0.5% (0.25% CGST + 0.25% SGST, or 0.5% IGST)')
    i2 = {'id': 'i2', 'title': 'Marketplace collections', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Sellers on ShopNow (an ECO) made taxable supplies of ₹15,00,000 (excluding tax) through it in June, with returns of ₹1,00,000 in the same month. Compute TCS and state the due date of deposit and of the ECO\'s statement.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Net value', '15,00,000 − 1,00,000 returns', inr(net)],
              ['TCS @0.5%', '', inr(tcs)],
              ['Deposit and GSTR-8', 'By 10 July', '—']], title='Section 52')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Section 51: notified deductors — departments or establishments of the Central or State Government, local authorities, Government agencies and notified persons (such as bodies with 51% or more Government equity or control, and societies or authorities set up by Government) — deduct tax from payments to suppliers of taxable goods or services.',
            'TDS applies when the total value of supply under a contract exceeds ₹2,50,000 (excluding GST). Rate: 2% — 1% CGST + 1% SGST/UTGST for intra-State, or 2% IGST for inter-State.',
            'No TDS where the supplier\'s location and the place of supply are in a State different from the deductor\'s State of registration (as CGST + SGST of another State could not be credited properly). Registered persons buying metal scrap have also been notified to deduct 2% TDS on such supplies above ₹2,50,000.'],
          'GST TDS is a small advance payment by public bodies to keep their suppliers compliant.',
          'A State PSU paying a ₹2 lakh contract: no TDS, as the value is below ₹2.5 lakh.'),
        C('c2', T2, [
            'TDS is deposited by the 10th of the next month and reported in GSTR-7 by the same date; the deductee sees it in his cash ledger once accepted.',
            'The deductor issues a TDS certificate (generated from GSTR-7). Late furnishing attracts a fee of ₹100 a day, up to ₹5,000; non-deposit attracts interest under section 50.',
            'Excess or wrong deduction is refunded to the deductor or deductee under section 54; the deductee can use the credit to pay tax.'],
          'Deducted tax becomes the supplier\'s cash credit — but only after the deductor files on time.',
          'A deductor who files GSTR-7 for May on 20 June is 10 days late.'),
        C('c3', T3, [
            'Section 52: an ECO not being an agent collects tax on the net value of taxable supplies made through it by other suppliers where it collects the consideration. Net value = taxable supplies minus returns in the month (excluding section 9(5) services on which the ECO itself pays tax).',
            'Rate: 0.5% — 0.25% CGST + 0.25% SGST/UTGST, or 0.5% IGST (reduced from 1% in July 2024).',
            'The ECO deposits by the 10th of the next month and files GSTR-8 by then; an annual statement is filed by 31 December after the year. Suppliers claim the TCS in their cash ledger. Officers may seek details from the ECO, and mismatches are communicated to suppliers.'],
          'TCS uses the marketplace as a checkpoint to tie each seller\'s sales to its tax.',
          'A seller with ₹10 lakh of net sales on a marketplace in a month has ₹5,000 collected and credited to it.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Reconciling TDS credit', 'role': 'Article assistant',
             'situation': 'A contractor serving several municipalities sees less TDS in his ledger than his receipts show.',
             'steps': ['Download TDS/TCS credit received on the portal.', 'Match each deductor\'s GSTR-7 entries.', 'Accept correct entries; reject wrong ones.', 'Follow up deductors who have not filed.'],
             'takeaway': 'Credit appears only after the deductor files and the deductee accepts.'}]

    mcqs = [
        Q('m1', 'GST TDS applies when contract value exceeds:', ['₹2,50,000', '₹50,000', '₹5,00,000', '₹1,00,000'], 0,
          'Section 51 uses ₹2,50,000 of total value under a contract, excluding tax. In practice: split contracts are looked at together.', 'c1', T1, check=250000),
        Q('m2', 'Rate of GST TDS on an intra-State supply:', ['1% CGST + 1% SGST', '2% CGST + 2% SGST', '0.5% CGST + 0.5% SGST', '1% IGST'], 0,
          'Total 2%, split equally for intra-State supplies; 2% IGST for inter-State supplies. In practice: show both on the certificate.', 'c1', T1),
        Q('m3', 'Which deductor is NOT covered by section 51?', ['A private limited company', 'A State Government department', 'A local authority', 'A Government agency'], 0,
          'Only Government bodies and notified persons deduct GST TDS (plus notified metal scrap buyers). An ordinary private company is not a deductor. In practice: check the notification.', 'c1', T1),
        Q('m4', 'No GST TDS is deducted where:', ['Supplier location and place of supply are in a State other than the deductor\'s registration State', 'The supply is inter-State', 'Value exceeds ₹2.5 lakh', 'The supplier is a company'], 0,
          'The proviso excludes cases where both supplier and place of supply are in another State. In practice: such supplies attract CGST + SGST of that State.', 'c1', T1),
        Q('m5', 'GSTR-7 is due by:', ['10th of the next month', '20th of the next month', '11th of the next month', '31 December'], 0,
          'Deductors deposit and file by the 10th. In practice: the deductee\'s credit depends on it.', 'c2', T2, check=10),
        Q('m6', 'Late fee for delay in GSTR-7 is capped at:', ['₹5,000', '₹10,000', '₹1,000', '₹25,000'], 0,
          'Section 51(6): ₹100 a day, up to ₹5,000. In practice: interest is separate.', 'c2', T2, check=5000),
        Q('m7', 'TCS rate collected by an ECO on an intra-State supply:', ['0.25% CGST + 0.25% SGST', '0.5% CGST + 0.5% SGST', '1% CGST + 1% SGST', '2% IGST'], 0,
          'Since July 2024 the rate is 0.5% in total. In practice: inter-State supplies bear 0.5% IGST.', 'c3', T3),
        Q('m8', 'TCS is calculated on:', ['Net value of taxable supplies (after returns)', 'Gross value including GST', 'Exempt supplies too', 'The ECO\'s commission'], 0,
          'Net value deducts returns in the month and excludes section 9(5) services. In practice: commission is the ECO\'s own taxable supply.', 'c3', T3),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Threshold', 1, 'concept', '2,50,000'), S('s2', 'Intra-State TDS', 1, 'computation', '1%', nums=[t_a]),
           S('s3', 'Inter-State TDS', 1, 'computation', 'IGST', nums=[t_c]), S('s4', 'Exempt goods', 1, 'concept', 'taxable')],
          ['Test value and taxability.'], ['Deducting on exempt goods.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Net value', 1, 'computation', 'net', nums=[net]), S('s2', 'TCS', 1, 'computation', '0.5%', nums=[tcs]), S('s3', 'Due date', 1, 'concept', '10')],
          ['Deduct returns first.'], ['Using 1%.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Who deducts GST TDS?', 'Government departments, local authorities, Government agencies and notified persons such as bodies with 51% or more Government equity.',
          [P('p1', 'Government bodies', 6, 'government|local authorit'), P('p2', 'Notified persons', 4, 'notified|51%')], 'c1'),
        V('v2', 'What is the TDS rate and threshold?', 'Two per cent on taxable supplies where contract value exceeds ₹2,50,000.',
          [P('p1', '2%', 5, 'two per cent|2%'), P('p2', '₹2,50,000', 5, '2,50,000')], 'c1'),
        V('v3', 'How does the supplier use the TDS?', 'It appears in his electronic cash ledger once accepted and can be used to pay tax.',
          [P('p1', 'Cash ledger', 6, 'cash ledger'), P('p2', 'Accepted', 4, 'accept')], 'c2'),
        V('v4', 'What is the TCS rate for ECOs?', 'Half a per cent of net taxable value — 0.25% each of CGST and SGST, or 0.5% IGST.',
          [P('p1', '0.5%', 6, '0.5%|half'), P('p2', 'Split', 4, '0.25%|igst')], 'c3'),
        V('v5', 'When is the ECO\'s annual statement due?', 'By 31 December following the end of the financial year.',
          [P('p1', '31 December', 6, '31 december'), P('p2', 'Annual', 4, 'year')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Delta Constructions', 'difficulty': 'moderate',
              'case': 'Delta Constructions of Lucknow, Uttar Pradesh, supplies works contracts to the UP Public Works Department (registered in UP) worth ₹10,00,000 + GST in July. It also sells building materials worth ₹3,00,000 through an online marketplace.',
              'mcqs': [
                  M('k1a', 'TDS by the PWD on the July contract:', ['₹20,000', '₹10,000', '₹5,000', 'Nil'], 0,
                    '2% of ₹10,00,000 = ₹20,000 (1% CGST + 1% SGST). In practice: TDS is on value excluding GST.', 'core', check=20000, topic=T1),
                  M('k1b', 'TDS is deposited by:', ['10 August', '20 August', '31 July', '25 August'], 0,
                    'By the 10th of the next month. In practice: GSTR-7 is filed by the same date.', 'core', check=10, topic=T2),
                  M('k1c', 'TCS by the marketplace on ₹3,00,000:', ['₹1,500', '₹3,000', '₹6,000', 'Nil'], 0,
                    '0.5% of ₹3,00,000 = ₹1,500. In practice: shown in Delta\'s cash ledger after acceptance.', 'core', check=1500, topic=T3),
                  M('k1d', 'Delta can use the TDS and TCS credits to:', ['Pay its tax liability', 'Pay only late fees', 'Claim only a refund', 'Nothing'], 0,
                    'Amounts in the cash ledger may be used for tax and other dues. In practice: reconcile monthly.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch14', 1, 'Tax Deduction at Source and Collection of Tax at Source',
                ['Identify GST TDS deductors, threshold and rate.',
                 'Apply deposit, return and certificate rules.',
                 'Compute TCS collected by e-commerce operators.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 20}, 'prereq': ['int-p3-b-ch13-u01'],
                 'exam_tip': 'Check three things for TDS: deductor type, contract value above ₹2.5 lakh, and the State test.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['TDS by Government bodies and notified persons: 2% above ₹2.5 lakh.',
                             'No TDS if supplier and place of supply are in another State.',
                             'GSTR-7 and deposit by 10th; late fee ₹100/day up to ₹5,000.',
                             'TCS by ECO: 0.5% of net value; GSTR-8 by 10th; annual by 31 December.'],
                 'remember': ['TDS/TCS goes to supplier\'s cash ledger.'],
                 'traps': ['TCS rate is now 0.5%, not 1%.', 'TDS only on taxable supplies.']},
                [('TDS', '2%; > ₹2.5 lakh'), ('TCS', '0.5%'), ('GSTR-7/8', '10th'), ('Late fee GSTR-7', '₹100/day, max ₹5,000')],
                viva, cases)
