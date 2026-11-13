"""CA Final · Paper 5 · Chapter 9 Tax Invoice, Credit and Debit Notes.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch09-u01'
T1 = 'Time and contents of tax invoice'
T2 = 'E-invoicing and QR code'
T3 = 'Other documents: bill of supply, vouchers, revised invoice'
T4 = 'Credit and debit notes'


def build():
    ck = Checks()
    cn = ck.add('500000*0.10', 'Value reduction by credit note (₹)')
    tx = ck.add('500000*0.10*0.18', 'Output tax reduced (₹)')
    i1 = {'id': 'i1', 'title': 'Credit note for a price cut', 'difficulty': 'core', 'minutes': 6,
          'q': 'Om Electricals supplied goods worth ₹5,00,000 + 18% GST on 10 January 2027 (FY 2026-27). In August 2027 it agrees a 10% price reduction and issues a credit note; the buyer reverses the ITC. Its annual return for 2026-27 is filed on 31 October 2027. Compute the reduction and the last date to declare the credit note.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Value reduced', '10% × 5,00,000', inr(cn)],
              ['Output tax reduced', '18% × 50,000', inr(tx)],
              ['Last date', 'Earlier of 30 November 2027 and annual return date', '31 October 2027'],
              ['Condition', 'Tax burden must not be passed on — recipient reverses ITC', 'Met']], title='Section 34')],
          'checks': list(ck)}

    c2 = Checks()
    at = c2.add('80000000', 'Aggregate turnover of Sanvi Ltd (₹)')
    i2 = {'id': 'i2', 'title': 'Invoicing obligations by turnover', 'difficulty': 'core', 'minutes': 6,
          'q': 'Sanvi Ltd had aggregate turnover of ₹8 crore in 2025-26. (a) How many HSN digits must it show on invoices? (b) Must it issue e-invoices for B2B supplies? (c) Must its B2C invoices carry a dynamic QR code? (d) When must it invoice goods sent on approval?',
          'solution': [table(['Point', 'Rule', 'Answer'], [
              ['(a) HSN', f'Turnover ₹{inr(at)} exceeds ₹5 crore', '6 digits for all supplies'],
              ['(b) E-invoice', 'Notified for turnover above ₹5 crore', 'Yes, with IRN'],
              ['(c) Dynamic QR', 'Only above ₹500 crore', 'No'],
              ['(d) Approval basis', 'Before or at supply, or within six months of removal', 'Within six months']], title='Section 31 and rule 46/48')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 31: for goods, the tax invoice is issued before or at the time of removal (where movement is involved) or delivery; for continuous supply of goods, at the time of each statement or payment. For services, within 30 days of supply (45 days for banks, insurers and NBFCs). Goods sent on approval: before or at supply or within six months of removal, whichever earlier.',
            'Rule 46 prescribes contents: supplier\'s name, address and GSTIN; a consecutive serial number up to 16 characters unique for the financial year; date; recipient details; HSN or SAC; description, quantity, value, rate and amount of tax; place of supply (with State name for inter-State supplies); reverse charge indication; and signature.',
            'HSN digits: 4 digits for B2B supplies where turnover is up to ₹5 crore (optional for B2C), and 6 digits for all supplies above ₹5 crore. Invoices for goods are issued in triplicate and for services in duplicate.'],
          'Invoice timing depends on goods or services; contents are prescribed.',
          'A security agency must invoice within 30 days of providing the service.'),
        C('c2', T2, [
            'E-invoicing applies to notified registered persons — currently those with aggregate turnover in any year from 2017-18 above ₹5 crore — for B2B supplies, exports and credit or debit notes. The invoice is reported to the Invoice Registration Portal, which returns an Invoice Reference Number (IRN) and a signed QR code; an invoice without a valid IRN is not a valid invoice.',
            'Exempted from e-invoicing: SEZ units, insurers, banks and NBFCs, GTAs, passenger transport services, multiplex admission services and specified others.',
            'Taxpayers with turnover above ₹500 crore must show a dynamic QR code on B2C invoices; digital display with payment cross-reference is treated as compliance.'],
          'E-invoicing validates B2B invoices through IRN.',
          'A ₹8 crore turnover company must generate IRNs for its B2B invoices.'),
        C('c3', T3, [
            'A bill of supply is issued for exempt supplies and by composition dealers; a combined invoice-cum-bill of supply may be used for mixed taxable and exempt supplies to unregistered persons.',
            'A receipt voucher is issued on receiving an advance; a refund voucher if no supply follows; a payment voucher by the recipient under reverse charge; and a self-invoice where the supplier is unregistered. Revised tax invoices can be issued within one month of the registration certificate for supplies made between the date of liability and grant of registration.',
            'Delivery challans are used for transport not involving supply (job work, approval basis, goods in SKD/CKD condition in lots, liquid gas without known quantity).'],
          'Each situation has its own document.',
          'A composition dealer issues a bill of supply, never a tax invoice.'),
        C('c4', T4, [
            'Section 34: a credit note may be issued where taxable value or tax in an invoice is excessive, goods are returned, or services are found deficient; a debit note where value or tax is less than due. Credit notes must be declared in the return by the earlier of 30 November after the financial year of supply and the date of the annual return.',
            'Output tax can be reduced by a credit note only if the incidence has not been passed on — i.e. the recipient reverses the corresponding ITC. Debit notes have no time limit and the recipient takes ITC on them.',
            'Credit and debit notes contain prescribed particulars, including reference to the original invoices, and must be reported through e-invoicing where applicable.'],
          'Credit notes have deadlines and ITC conditions; debit notes do not.',
          'A 10% price cut on a ₹5 lakh supply reduces output tax by ₹9,000.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Invoice compliance review', 'role': 'GST associate',
             'situation': 'An audit finds invoices with missing fields and late credit notes.',
             'steps': ['Check rule 46 fields and HSN digits.', 'Verify IRN generation where required.', 'Check credit note deadlines.', 'Confirm ITC reversal by recipients.'],
             'takeaway': 'Defective documents risk ITC denial for customers.'}]

    mcqs = [
        Q('m1', 'Invoice for services by a bank must be issued within:', ['Forty-five days of supply', 'Thirty days', 'Sixty days', 'Seven days'], 0,
          'Rule 47. In practice: others 30 days.', 'c1', T1),
        Q('m2', 'Invoice serial number can have up to:', ['Sixteen characters', 'Ten characters', 'Twenty characters', 'Eight characters'], 0,
          'Rule 46. In practice: unique per year.', 'c1', T1),
        Q('m3', 'Taxpayers with turnover above ₹5 crore must show HSN at:', ['Six digits', 'Four digits', 'Eight digits', 'Two digits'], 0,
          'Rule 46 notification. In practice: B2B and B2C.', 'c1', T1),
        Q('m4', 'Current e-invoicing threshold of aggregate turnover is above:', ['Five crore rupees', 'Ten crore rupees', 'Twenty crore rupees', 'Five hundred crore rupees'], 0,
          'Notification. In practice: any year since 2017-18.', 'c2', T2),
        Q('m5', 'Dynamic QR code on B2C invoices applies above turnover of:', ['Five hundred crore rupees', 'Five crore rupees', 'Fifty crore rupees', 'One hundred crore rupees'], 0,
          'Rule 46. In practice: digital display allowed.', 'c2', T2),
        Q('m6', 'Recipient paying tax under RCM to an unregistered supplier issues:', ['A self-invoice and payment voucher', 'A bill of supply', 'A credit note', 'A receipt voucher'], 0,
          'Section 31(3)(f)/(g). In practice: same day as payment.', 'c3', T3),
        Q('m7', 'Credit note for 2026-27 supplies must be declared by the earlier of the annual return date and:', ['30 November 2027', '31 March 2027', '30 September 2027', '31 December 2027'], 0,
          'Section 34(2). In practice: track deadlines.', 'c4', T4),
        Q('m8', 'Goods sent on approval must be invoiced within:', ['Six months of removal', 'Thirty days', 'One year', 'Ninety days'], 0,
          'Section 31(7). In practice: or on acceptance.', 'c1', T1),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Reduction', 2, 'computation', 'credit note', nums=[cn, tx]), S('s2', 'Deadline and condition', 2, 'analysis', '30 November')],
          ['State incidence condition.'], ['Ignoring annual return date.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'HSN and e-invoice', 3, 'analysis', '5 crore', nums=[at]), S('s2', 'QR and approval basis', 2, 'analysis', 'six months')],
          ['Cite thresholds.'], ['Applying QR code to ₹8 crore turnover.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is an IRN?', 'An Invoice Reference Number generated by the registration portal that validates an e-invoice.',
          [P('p1', 'Invoice Reference Number', 5, 'invoice reference number'), P('p2', 'Validates', 5, 'valid')], 'c2'),
        V('v2', 'When is a revised tax invoice issued?', 'For supplies made between the date of liability and grant of registration, within one month of the registration certificate.',
          [P('p1', 'Between liability and registration', 5, 'between'), P('p2', 'One month', 5, 'one month')], 'c3'),
        V('v3', 'Is there a time limit for debit notes?', 'Debit notes can be issued at any time; the recipient takes ITC on them within the section 16(4) limit.',
          [P('p1', 'Any time', 5, 'any time'), P('p2', 'Recipient ITC', 5, 'recipient')], 'c4'),
        V('v4', 'When is a delivery challan used?', 'For movement not involving supply, such as job work or goods sent on approval.',
          [P('p1', 'Job work', 5, 'job work'), P('p2', 'Approval', 5, 'approval')], 'c3'),
        V('v5', 'How many copies of an invoice for goods?', 'Triplicate: original for recipient, duplicate for transporter, triplicate for supplier.',
          [P('p1', 'Triplicate', 5, 'triplicate'), P('p2', 'Transporter', 5, 'transporter')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Deficient service refund', 'difficulty': 'core',
              'case': 'Vista IT Services billed ₹10,00,000 + 18% GST in December 2026. In May 2027 the client reports deficiency and Vista agrees to refund 20% of value; the client reverses ITC accordingly.',
              'mcqs': [
                  M('k1a', 'Value of credit note (₹):', ['2,00,000', '1,00,000', '2,36,000', '20,000'], 0,
                    '20% × 10 lakh. In practice: plus tax.', 'core', check=200000, topic=T4),
                  M('k1b', 'Tax reduced (₹):', ['36,000', '18,000', '1,80,000', '3,600'], 0,
                    '18% × 2 lakh. In practice: in return of issue.', 'core', check=36000, topic=T4),
                  M('k1c', 'Ground for credit note:', ['Services found deficient', 'Late payment', 'Change in rate', 'Bad debt'], 0,
                    'Section 34(1). In practice: document reasons.', 'core', topic=T4),
                  M('k1d', 'If the client did not reverse ITC, Vista\'s output tax:', ['Cannot be reduced', 'Is reduced anyway', 'Is refunded', 'Is doubled'], 0,
                    'Incidence condition. In practice: financial credit note.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch09', 1, 'Tax Invoice, Credit and Debit Notes',
                ['Apply time limits and contents for tax invoices.',
                 'Apply e-invoicing and QR code requirements.',
                 'Identify other documents under GST.',
                 'Apply credit and debit note provisions.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['fin-p5-ch08-u01'],
                 'exam_tip': 'Match each document to its triggering event and deadline.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 31: goods at removal; services 30/45 days; approval 6 months.', 'Rule 46: contents; HSN 4/6 digits.', 'E-invoice above ₹5 crore; QR above ₹500 crore.',
                             'Bill of supply, receipt/refund/payment vouchers, revised invoices.', 'Section 34: credit note deadline 30 November/annual return.'],
                 'remember': ['No IRN, no valid e-invoice.'],
                 'traps': ['Reducing tax without recipient\'s ITC reversal.']},
                [('Invoice', 'Section 31'), ('Contents', 'Rule 46'), ('Credit/debit notes', 'Section 34')],
                viva, cases)
