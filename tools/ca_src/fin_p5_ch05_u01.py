"""CA Final · Paper 5 · Chapter 5 Time of Supply.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch05-u01'
T1 = 'Time of supply of goods'
T2 = 'Time of supply of services'
T3 = 'Reverse charge time of supply'
T4 = 'Change in rate of tax'


def build():
    ck = Checks()
    adv = ck.add('50000*0.18', 'GST on advance for services at 18% (₹)')
    bal = ck.add('(300000-50000)*0.18', 'GST on balance at 18% (₹)')
    i1 = {'id': 'i1', 'title': 'Forward charge — goods and services', 'difficulty': 'core', 'minutes': 7,
          'q': 'Prism Consultants (registered, regular) agrees a ₹3,00,000 consultancy (18%). It receives an advance of ₹50,000 on 1 May 2026, completes the service on 10 June 2026 and issues the invoice on 20 July 2026. Separately, a goods supplier receives an advance on 5 May and invoices on 25 May. Determine time of supply and tax due.',
          'solution': [table(['Event', 'Time of supply', 'GST (₹)'], [
              ['Advance for services', '1 May 2026 (date of receipt)', inr(adv)],
              ['Balance service', 'Invoice not within 30 days of completion → 10 June 2026', inr(bal)],
              ['Goods advance', 'No GST on advance for goods (Notification 66/2017); time is invoice date 25 May', '—']], title='Sections 12 and 13')],
          'checks': list(ck)}

    c2 = Checks()
    d1 = c2.add('30+1', 'Day count: 31 days after invoice dated 1 Aug ends on 1 Sep (goods RCM)')
    d2 = c2.add('60+1', 'Day count for services RCM: 61st day after invoice (1 Oct)')
    i2 = {'id': 'i2', 'title': 'Reverse charge', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Raghav Ltd receives (a) cashew nuts from an agriculturist (RCM goods) with invoice dated 1 August 2026, received 3 August, paid 15 September; (b) legal services (RCM) with invoice dated 1 August 2026, paid 15 October 2026. Determine the time of supply.',
          'solution': [table(['Supply', 'Candidates', 'Time of supply'], [
              ['(a) Goods', f'Receipt 3 Aug; payment 15 Sep; day after 30 days of invoice (day {d1}) = 1 Sep', '3 August 2026 (earliest)'],
              ['(b) Services', f'Payment 15 Oct; day after 60 days of invoice (day {d2}) = 1 Oct', '1 October 2026 (earlier)']], title='Sections 12(3) and 13(3)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 12(2): time of supply of goods under forward charge is whichever comes first — the invoice date (or the last date by which section 31 required it) or the payment receipt date. However, Notification 66/2017 relieves regular suppliers of goods (not composition suppliers or suppliers of specified actionable claims) from paying GST on advances — tax is due at the invoice date.',
            'Where an amount up to ₹1,000 is received in excess of the invoice value, the supplier may take the invoice date as time of supply for that excess.',
            'Section 12(5) residual: the due date of filing the periodical return, or else the date of payment of tax. Section 12(6): interest, late fee or penalty charged for late payment is treated as supplied on the date it is received.'],
          'Goods: invoice date usually decides; advances are not taxed.',
          'An advance for goods received in May but invoiced later is taxed at invoice.'),
        C('c2', T2, [
            'Section 13(2): for services under forward charge — if the invoice is issued within the prescribed period (30 days of supply, 45 days for banks and insurers), the earlier of invoice date and payment date; if not, the earlier of the date of provision of service and the date of payment; if neither applies, the date the recipient records the receipt in its books.',
            'Advances for services are taxable on receipt, with the ₹1,000 excess-payment option. Continuous supply of services follows invoice timing under section 31(5): due date of payment, or completion of event-linked milestones.',
            'Date of receipt of payment is the earlier of the date it is entered in the supplier\'s books and the date credited to its bank account.'],
          'Services: late invoices shift the time back to performance.',
          'A service completed on 10 June and invoiced on 20 July is taxed as of 10 June.'),
        C('c3', T3, [
            'Section 12(3) goods under RCM: earliest of the date of receipt of goods, the date of payment, and the date immediately following 30 days from the supplier\'s invoice; if none can be determined, the date of entry in the recipient\'s books.',
            'Section 13(3) services under RCM: earlier of the date of payment and the date immediately following 60 days from the supplier\'s invoice; else the date of entry in the recipient\'s books.',
            'For services imported from associated enterprises abroad, time of supply is the earlier of the date of entry in the books of the recipient and the date of payment.'],
          'RCM: 30 days for goods, 60 days for services.',
          'Legal services invoiced on 1 August and paid on 15 October are taxable on 1 October.'),
        C('c4', T4, [
            'Section 14 applies when the rate of tax changes. If the supply was made before the change: invoice and payment both after → date of the earlier of invoice and payment; invoice before and payment after → invoice date; payment before and invoice after → payment date.',
            'If the supply is made after the change: payment and invoice both after → the earlier; invoice before and payment after → payment date (with new rate); payment before and invoice after → invoice date.',
            'In short, where two of the three events (supply, invoice, payment) fall after the change, the new rate applies; where two fall before, the old rate applies. If the bank credit comes more than four working days after the rate change, the bank credit date is taken as the payment date.'],
          'Two out of three events decide the applicable rate.',
          'Service supplied before a rate cut but invoiced and paid after attracts the new rate.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Month-end tax point review', 'role': 'GST accountant',
             'situation': 'A services firm has many advances, late invoices and RCM bills.',
             'steps': ['Tax all service advances received.', 'Check invoices beyond 30 days of completion.', 'Apply RCM 60-day rule.', 'Handle any rate change using section 14.'],
             'takeaway': 'Wrong time of supply means interest on delayed tax.'}]

    mcqs = [
        Q('m1', 'GST on advances received for supply of goods by a regular taxpayer is:', ['Not payable until invoice', 'Payable on receipt', 'Payable at 50%', 'Never payable'], 0,
          'Notification 66/2017. In practice: services differ.', 'c1', T1),
        Q('m2', 'Excess receipt over invoice value for which invoice date may be the time of supply is up to:', ['One thousand rupees', 'Five thousand rupees', 'Ten thousand rupees', 'Five hundred rupees'], 0,
          'Option to supplier. In practice: small excesses.', 'c1', T1),
        Q('m3', 'Invoice for services (other than banks) should be issued within:', ['Thirty days of supply', 'Forty-five days', 'Sixty days', 'Fifteen days'], 0,
          'Rule 47. In practice: banks 45 days.', 'c2', T2),
        Q('m4', 'If a service invoice is issued late, time of supply is the earlier of payment and:', ['Date of provision of service', 'Date of invoice', 'Date of contract', 'Return due date'], 0,
          'Section 13(2)(b). In practice: interest risk.', 'c2', T2),
        Q('m5', 'For RCM on services, time of supply is the earlier of payment and the date following:', ['Sixty days from invoice', 'Thirty days from invoice', 'Forty-five days', 'Ninety days'], 0,
          'Section 13(3). In practice: goods 30 days.', 'c3', T3),
        Q('m6', 'For RCM on goods, time of supply is the earliest of receipt of goods, payment and:', ['The day following thirty days from invoice', 'Sixty days from invoice', 'Invoice date', 'Return due date'], 0,
          'Section 12(3). In practice: track receipts.', 'c3', T3),
        Q('m7', 'Interest for delayed payment received by a supplier is supplied:', ['When received', 'At original invoice date', 'Never', 'At year-end'], 0,
          'Section 12(6)/13(6). In practice: invoice on receipt.', 'c1', T1),
        Q('m8', 'Supply before a rate change, invoice and payment after: the rate applied is:', ['New rate', 'Old rate', 'Average rate', 'Lower rate'], 0,
          'Section 14. In practice: two of three after.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Service advance and balance', 4, 'computation', 'advance', nums=[adv, bal]), S('s2', 'Goods advance', 2, 'analysis', 'invoice')],
          ['Explain late invoice rule.'], ['Taxing goods advances.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Goods RCM', 2.5, 'analysis', '30 days', nums=[d1]), S('s2', 'Services RCM', 2.5, 'analysis', '60 days', nums=[d2])],
          ['List all candidates.'], ['Using invoice date as time of supply.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is the date of receipt of payment?', 'The earlier of the date entered in the supplier\'s books and the date credited to its bank account.',
          [P('p1', 'Books', 5, 'books'), P('p2', 'Bank account', 5, 'bank')], 'c2'),
        V('v2', 'What is the residual rule for goods?', 'The due date of the periodical return, or else the date tax is paid.',
          [P('p1', 'Return due date', 5, 'return'), P('p2', 'Date tax is paid', 5, 'paid')], 'c1'),
        V('v3', 'How is time of supply fixed for services imported from an associated enterprise?', 'The earlier of the date of entry in the recipient\'s books and the date of payment.',
          [P('p1', 'Entry in books', 5, 'entry'), P('p2', 'Payment', 5, 'payment')], 'c3'),
        V('v4', 'State the shortcut for section 14.', 'If two of supply, invoice and payment fall after the rate change the new rate applies; otherwise the old rate.',
          [P('p1', 'Two of three', 5, 'two of'), P('p2', 'New rate', 5, 'new rate')], 'c4'),
        V('v5', 'What is the invoice period for banks?', 'Forty-five days from the date of supply.',
          [P('p1', 'Forty-five days', 5, 'forty-five'), P('p2', 'Supply', 5, 'supply')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Rate change at Lumen Interiors', 'difficulty': 'moderate',
              'case': 'The GST rate on a service supplied by Lumen Interiors was reduced from 18% to 5% on 22 September 2026 (assume). Lumen completed a job on 15 September 2026, issued the invoice on 25 September and received ₹2,00,000 on 30 September.',
              'mcqs': [
                  M('k1a', 'How many of the three events occurred after the change?', ['2', '1', '3', '0'], 0,
                    'Invoice and payment after. In practice: count events.', 'core', check=2, topic=T4),
                  M('k1b', 'Applicable rate (%):', ['5', '18', '12', '11.5'], 0,
                    'Supply before, invoice and payment after → earlier of invoice/payment. In practice: new rate.', 'core', check=5, topic=T4),
                  M('k1c', 'Time of supply:', ['25 September 2026', '15 September 2026', '30 September 2026', '22 September 2026'], 0,
                    'Earlier of invoice and payment. In practice: section 14(a)(i).', 'core', topic=T4),
                  M('k1d', 'GST on ₹2,00,000 (₹):', ['10,000', '36,000', '24,000', '5,000'], 0,
                    '5% × 2 lakh. In practice: invoice at new rate.', 'core', check=10000, topic=T4),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch05', 1, 'Time of Supply',
                ['Determine time of supply of goods.',
                 'Determine time of supply of services.',
                 'Determine time of supply under reverse charge.',
                 'Apply section 14 on change in rate of tax.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 35, 'practice': 25}, 'prereq': ['fin-p5-ch04-u01'],
                 'exam_tip': 'List every candidate date in a table, then pick the earliest as the law requires.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 12(2) goods; no GST on goods advances.', 'Section 13(2) services; 30/45-day invoice rule.', 'RCM: goods 30 days, services 60 days.',
                             'Section 12(6)/13(6) interest and late fee on receipt.', 'Section 14 two-of-three rule.'],
                 'remember': ['₹1,000 excess receipt option.'],
                 'traps': ['Ignoring late invoices for services.']},
                [('Goods', 'Section 12'), ('Services', 'Section 13'), ('Rate change', 'Section 14')],
                viva, cases)
