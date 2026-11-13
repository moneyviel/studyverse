"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 6 Time of Supply.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch06-u01'
T1 = 'Time of supply of goods (s. 12)'
T2 = 'Time of supply of services (s. 13)'
T3 = 'Reverse charge, vouchers and residual cases'
T4 = 'Change in rate of tax (s. 14)'


def build():
    i1 = {'id': 'i1', 'title': 'Advance, service and invoice', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Determine the time of supply for a registered consultant (not under composition): (a) service completed 10 June, invoice issued 25 June, payment received 15 July; (b) advance received 1 May, service completed 20 May, invoice issued 22 May; (c) service completed 2 August, invoice issued 15 September, payment received 20 September; (d) a trader of goods receives an advance on 5 March and issues the invoice and dispatches goods on 20 March.',
          'solution': [table(['Case', 'Time of supply', 'Reason'], [
              ['(a)', '25 June', 'Invoice issued within 30 days of completion; earlier of invoice and payment'],
              ['(b)', '1 May (for the advance)', 'Receipt of payment is earlier than the invoice'],
              ['(c)', '2 August', 'Invoice not issued within 30 days, so earlier of completion and payment'],
              ['(d)', '20 March', 'For goods, advances are not taxed (Notification); time of supply is the invoice date']], title='Sections 12 and 13'),
              note('Section 31 gives 30 days from supply to issue a service invoice (45 days for banks and insurers).')],
          'checks': []}

    i2 = {'id': 'i2', 'title': 'Rate changed mid-way', 'difficulty': 'hard', 'minutes': 7,
          'q': 'The GST rate on a service rose from 12% to 18% on 1 October. Determine the applicable rate: (a) service before 1 October, invoice 3 October, payment 5 October; (b) service before 1 October, invoice 25 September, payment 4 October; (c) service after 1 October, invoice 28 September, payment 30 September; (d) service after 1 October, invoice 2 October, payment 25 September.',
          'solution': [table(['Case', 'Service / Invoice / Payment', 'Rate', 'Rule u/s 14'], [
              ['(a)', 'Before / After / After', '18%', 'Invoice and payment after change: earlier of the two'],
              ['(b)', 'Before / Before / After', '12%', 'Invoice before change: date of invoice'],
              ['(c)', 'After / Before / Before', '12%', 'Invoice and payment before change: earlier of the two'],
              ['(d)', 'After / After / Before', '18%', 'Invoice after change: date of invoice']], title='Change in rate'),
              note('Shortcut: whichever side (before or after the change) has two of the three events decides the rate.')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Time of supply fixes when the liability to pay tax arises; tax is then paid with the return for that period.',
            'Section 12(2): for goods, the earlier of the date of issue of the invoice (or the last date by which it should have been issued under section 31) and the date of receipt of payment. However, by notification, registered persons other than composition taxpayers pay tax on goods only at the invoice stage — advances for goods are not taxed.',
            'Section 31: a goods invoice is issued before or at removal (where movement is involved) or delivery; for continuous supply of goods, when each statement or payment falls due. Excess payment of up to ₹1,000 over the invoice value may, at the supplier\'s option, be taxed on the invoice date.'],
          'For goods the invoice date is the anchor; the advance does not trigger tax.',
          'A furniture maker receiving a booking advance in January pays tax only when it invoices the furniture in February.'),
        C('c2', T2, [
            'Section 13(2): for services, (a) if the invoice is issued within the time under section 31 — the earlier of the invoice date and payment receipt; (b) if not issued in time — the earlier of the date of provision of service and payment; (c) if neither applies — the date the recipient records the receipt in his books.',
            'Section 31: invoice within 30 days from the supply of service (45 days for insurers, banks and financial institutions); for continuous supply, by the due date of payment or on completion of the milestone event.',
            'Date of receipt of payment is the earlier of the entry in the supplier\'s books and the credit in his bank account. Advances for services are taxable.'],
          'For services, tax follows the earliest of the invoice and the money, unless the invoice is late.',
          'Advance of ₹50,000 received on 10 April for a June workshop: tax on ₹50,000 is due with April\'s return.'),
        C('c3', T3, [
            'Reverse charge on goods (s. 12(3)): earliest of receipt of goods, payment, and the date immediately after 30 days from the supplier\'s invoice. On services (s. 13(3)): earlier of payment and the date immediately after 60 days from the supplier\'s invoice; for an associated enterprise abroad, the earlier of the book entry and payment.',
            'Vouchers (ss. 12(4), 13(4)): if the supply is identifiable when the voucher is issued — the date of issue; otherwise — the date of redemption.',
            'Residual (ss. 12(5), 13(5)): the due date of the periodical return, or else the date tax is paid. Additions for interest, late fee or penalty for delayed payment (ss. 12(6), 13(6)): the date of their receipt.'],
          'Special cases have their own clocks — reverse charge counts 30 or 60 days from the invoice.',
          'A company paying an advocate 75 days after his invoice: time of supply is day 61, not the payment date.'),
        C('c4', T4, [
            'Section 14 applies when the rate changes. Three events are compared: provision of supply, issue of invoice, receipt of payment.',
            'Supply before the change: invoice and payment after — earlier of the two (new rate); invoice before, payment after — invoice date (old rate); payment before, invoice after — payment date (old rate).',
            'Supply after the change: payment after, invoice before — payment date (new rate); invoice and payment before — earlier of the two (old rate); invoice after, payment before — invoice date (new rate).',
            'Receipt of payment here is the earlier of book entry and bank credit, but the bank credit date applies if credited more than four working days after the change.'],
          'Rate change follows the majority: two of three events on one side of the change date win.',
          'Service in September, invoice and payment in October after a cut from 18% to 5%: the lower rate applies.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Advance tracker', 'role': 'Article assistant',
             'situation': 'A services firm receives many advances and pays tax only when invoicing.',
             'steps': ['List advances by date of receipt.', 'Issue receipt vouchers for each advance.', 'Pay tax on advances in the month received.', 'Adjust when the final invoice is issued.'],
             'takeaway': 'Service advances are taxable on receipt; goods advances are not.'}]

    mcqs = [
        Q('m1', 'Time of supply for goods (non-composition supplier) is ordinarily the:', ['Date of invoice or last date for issuing it', 'Date of receipt of advance', 'Date of order', 'Date of payment'], 0,
          'Section 12(2) read with the notification removes tax on advances for goods; liability arises on the invoice date or the date it should have been issued. In practice: composition suppliers are treated differently.', 'c1', T1),
        Q('m2', 'A service invoice must normally be issued within:', ['30 days of supply', '45 days of supply', '60 days of supply', '7 days of supply'], 0,
          'Section 31 and Rule 47 give 30 days for services; banks, insurers and financial institutions get 45 days. In practice: late invoices shift time of supply to the service date.', 'c2', T2, check=30),
        Q('m3', 'Advance received for services on 3 April; service rendered and invoice issued on 18 May. Time of supply for the advance:', ['3 April', '18 May', '30 April', '20 May'], 0,
          'For services, payment received before the invoice triggers tax on that date. In practice: issue a receipt voucher.', 'c2', T2),
        Q('m4', 'Under reverse charge on services, if payment is not made, time of supply is the date immediately after:', ['60 days from the supplier\'s invoice', '30 days from the supplier\'s invoice', '90 days', 'the end of the quarter'], 0,
          'Section 13(3): earlier of payment and the day after 60 days from the invoice. For goods it is 30 days. In practice: track RCM invoices by date.', 'c3', T3),
        Q('m5', 'A gift voucher valid for any product in a store: time of supply is the date of:', ['Redemption', 'Issue', 'Purchase of goods by the store', 'Expiry'], 0,
          'If the supply is not identifiable when the voucher is issued, the redemption date applies. In practice: product-specific vouchers are taxed on issue.', 'c3', T3),
        Q('m6', 'Late payment interest charged by a supplier: time of supply is the date of:', ['Receipt of the interest', 'Original invoice', 'Original supply', 'Return filing'], 0,
          'Sections 12(6) and 13(6) make the date of receipt of interest, late fee or penalty the time of supply. In practice: tax it at the rate of the original supply.', 'c3', T3),
        Q('m7', 'Rate rises on 1 July. Service in June, invoice 2 July, payment 28 June. Rate applicable:', ['Old rate', 'New rate', 'Average rate', 'Lower of the two'], 0,
          'Supply before change, payment before, invoice after: date of payment governs — old rate. In practice: two of three events fell before the change.', 'c4', T4),
        Q('m8', 'Date of receipt of payment for section 13 is:', ['Earlier of book entry and bank credit', 'Later of the two', 'Date of cheque', 'Date of invoice'], 0,
          'Sections 12 and 13 use the earlier of the entry in the supplier\'s books and the credit to his bank account. In practice: record advances promptly.', 'c2', T2),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Case (a)', 1, 'concept', '25 june'), S('s2', 'Case (b)', 1, 'concept', '1 may'), S('s3', 'Case (c)', 1, 'concept', '2 august'), S('s4', 'Case (d)', 1, 'concept', '20 march')],
          ['Check the 30-day invoice rule.'], ['Taxing the goods advance.'], ['Table.'], pad='table'),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Case (a)', 1, 'concept', '18%'), S('s2', 'Case (b)', 1, 'concept', '12%'), S('s3', 'Case (c)', 1, 'concept', 'earlier'), S('s4', 'Case (d)', 1, 'concept', 'invoice')],
          ['Tabulate the three events.'], ['Using only the supply date.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Why is time of supply important?', 'It fixes the point at which the liability to pay tax arises and hence the return period in which tax is paid.',
          [P('p1', 'Liability arises', 6, 'liability'), P('p2', 'Return period', 4, 'return|period')], 'c1'),
        V('v2', 'Are advances for goods taxable?', 'For registered persons other than composition taxpayers, tax on goods is payable only at the invoice stage, so advances for goods attract tax only when the invoice is raised.',
          [P('p1', 'Invoice stage', 6, 'invoice'), P('p2', 'Composition exception', 4, 'composition')], 'c1'),
        V('v3', 'What if a service invoice is issued late?', 'Time of supply becomes the earlier of the date of provision of service and the date of receipt of payment.',
          [P('p1', 'Provision of service', 6, 'provision'), P('p2', 'Payment', 4, 'payment')], 'c2'),
        V('v4', 'What is the time of supply under reverse charge for goods?', 'The earliest of the date of receipt of goods, the date of payment, and the date immediately following 30 days from the supplier\'s invoice.',
          [P('p1', 'Receipt of goods', 5, 'receipt of goods'), P('p2', '30 days', 5, '30 days')], 'c3'),
        V('v5', 'How does section 14 decide the rate?', 'By comparing the dates of supply, invoice and payment with the date of change; the rate on the side where two of the three events fall applies.',
          [P('p1', 'Three events', 5, 'supply|invoice|payment'), P('p2', 'Two of three', 5, 'two')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Brightline Services', 'difficulty': 'moderate',
              'case': 'Brightline Services, a registered security agency, supplied services to a factory throughout March, completing them on 31 March. It issued its invoice on 20 April and received payment on 25 May. It also received ₹40,000 in advance on 28 March for April services. The factory pays reverse charge on some purchases from an unregistered transporter whose invoice is dated 1 April and is paid on 20 June.',
              'mcqs': [
                  M('k1a', 'Was the March invoice issued in time?', ['Yes, it is within 30 days of completing the supply', 'No, it had to be issued by 31 March', 'No, only 15 days are allowed', 'Time limits do not apply to services'], 0,
                    'A service invoice is due within 30 days of supply; 20 April is 20 days after 31 March. In practice: time of supply is then the invoice date, 20 April.', 'moderate', topic=T2),
                  M('k1b', 'Time of supply for the ₹40,000 advance:', ['28 March', '20 April', '30 April', '25 May'], 0,
                    'Advances for services are taxed on receipt. In practice: show it in March\'s return.', 'core', check=28, topic=T2),
                  M('k1c', 'Time of supply for the factory\'s reverse charge transport service:', ['31 May (day after 60 days from invoice)', '20 June', '1 April', '30 April'], 0,
                    'Earlier of payment (20 June) and the day after 60 days from 1 April (31 May) — so 31 May. In practice: pay RCM tax with May\'s return.', 'hard', topic=T3),
                  M('k1d', 'If the security service rate changed on 1 April, the March supply invoiced in April and paid in May is taxed at:', ['The new rate', 'The old rate', 'Either at option', 'The lower rate'], 0,
                    'Supply before the change, invoice and payment after: the earlier of invoice and payment, both after the change — new rate. In practice: two of three events fall after.', 'moderate', topic=T4),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch06', 1, 'Time of Supply',
                ['Determine time of supply of goods and services under forward charge.',
                 'Apply the rules for reverse charge, vouchers and residual cases.',
                 'Determine the rate applicable when the rate changes.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 30}, 'prereq': ['int-p3-b-ch05-u01'],
                 'exam_tip': 'Draw a three-column date line (supply, invoice, payment) for every time-of-supply or rate-change question.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Goods: invoice date (advances not taxed for non-composition suppliers).',
                             'Services: earlier of invoice (if in time) and payment; else earlier of service and payment.',
                             'RCM: goods 30 days, services 60 days after invoice.',
                             'Vouchers: identifiable → issue; else redemption.',
                             'Rate change: two of three events decide.'],
                 'remember': ['Service invoice within 30 days (45 for banks/insurers).', 'Interest for late payment: taxed on receipt.'],
                 'traps': ['Advance for services is taxable on receipt.', 'Bank credit date used if more than 4 working days after rate change.']},
                [('Service invoice', '30 days'), ('RCM goods', '30 days after invoice'), ('RCM services', '60 days after invoice'), ('Excess up to ₹1,000', 'Invoice date option')],
                viva, cases)
