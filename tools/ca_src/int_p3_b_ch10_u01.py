"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 10 Tax Invoice; Credit and Debit Notes.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch10-u01'
T1 = 'Tax invoice: when and how (s. 31)'
T2 = 'Other documents: bill of supply, vouchers, self-invoice, delivery challan'
T3 = 'E-invoicing and invoice contents'
T4 = 'Credit and debit notes (s. 34)'


def build():
    ck = Checks()
    out = ck.add('(500000-60000)*18/100', 'Net output tax after credit note')
    i1 = {'id': 'i1', 'title': 'Returns and price cuts', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Lotus Electronics invoiced goods for ₹5,00,000 + 18% GST in July 2026. In September 2026 the buyer returned goods worth ₹60,000. Which document is issued, by when, and what is the net taxable value and tax? Also, how is an undercharged freight of ₹10,000 billed later?',
          'solution': [table(['Point', 'Answer'], [
              ['Goods returned', 'Credit note u/s 34(1)'],
              ['Last date to declare it', '30 November 2027 (following FY 2026-27) or annual return date, if earlier'],
              ['Net taxable value', '₹5,00,000 − ₹60,000 = ₹4,40,000'],
              ['Net tax', inr(out)],
              ['Undercharged freight', 'Debit note u/s 34(3) for ₹10,000 + GST, declared in the return for the month it is issued']], title='Section 34'),
              note('The supplier can reduce its tax only if the recipient has not passed on the incidence; the recipient must reverse the matching ITC.')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Choosing the document', 'difficulty': 'core', 'minutes': 6,
          'q': 'Which document should be issued? (a) A composition dealer sells goods; (b) a registered consultant receives an advance; (c) a company pays reverse charge on goods bought from an unregistered dealer; (d) goods sent to a job worker; (e) a retailer\'s sale of ₹150 to an unregistered customer who does not ask for an invoice.',
          'solution': [table(['Case', 'Document'], [
              ['(a)', 'Bill of supply'],
              ['(b)', 'Receipt voucher (refund voucher if the supply does not happen)'],
              ['(c)', 'Self-invoice and payment voucher'],
              ['(d)', 'Delivery challan'],
              ['(e)', 'No invoice needed; a consolidated tax invoice at day-end for such sales']], title='Documents under GST')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Section 31(1): for goods, a tax invoice is issued before or at the time of removal (where supply involves movement) or delivery; for continuous supply of goods, before or when each statement is issued or payment is received.',
            'Section 31(2) and Rule 47: for services, within 30 days of supply (45 days for insurers, banks and NBFCs); for continuous supply of services, on or before the due date of payment, or when payment is received, or on completion of the linked event.',
            'Revised invoices: within one month of the grant of registration, for supplies made between the effective date and the grant. Goods sent on approval: invoice before or at supply, or six months from removal, whichever is earlier.'],
          'The invoice is the anchor of GST — it creates both the supplier\'s liability and the buyer\'s credit.',
          'Consulting completed on 10 May must be invoiced by 9 June.'),
        C('c2', T2, [
            'Bill of supply: for exempt supplies or by a composition taxpayer; no tax shown. Receipt voucher: on receiving an advance; refund voucher if no supply follows. Payment voucher: for payments under reverse charge.',
            'Self-invoice: a recipient paying reverse charge on supplies from an unregistered supplier issues an invoice on himself.',
            'Delivery challan: for transport not amounting to supply (job work, goods on approval), supply of liquid gas where quantity is unknown, and movement in semi-knocked-down condition.',
            'For a supply below ₹200 to an unregistered person who does not ask for an invoice, a consolidated invoice for the day may be issued.'],
          'Each situation has its own document; using the right one keeps credit and liability in step.',
          'Sending moulds to a job worker needs a delivery challan, not a tax invoice.'),
        C('c3', T3, [
            'Contents (Rule 46): name, address and GSTIN of supplier; serial number (unique per year, up to 16 characters); date; recipient\'s name, address and GSTIN if registered; HSN or SAC code; description and quantity; value and discount; rate and amount of each tax; place of supply and State name for inter-State supplies; whether reverse charge applies; signature.',
            'HSN digits: 4 digits for taxpayers with aggregate turnover up to ₹5 crore (on B2B invoices), 6 digits above ₹5 crore.',
            'E-invoicing: registered persons whose aggregate turnover in any year from 2017-18 exceeded ₹5 crore must report B2B invoices to the Invoice Registration Portal and get an IRN and QR code; an invoice without an IRN is not a valid invoice. Those with turnover of ₹10 crore and above must report within 30 days of the invoice date.',
            'Copies: goods — triplicate (original for recipient, duplicate for transporter, triplicate for supplier); services — duplicate.'],
          'An e-invoice is a normal invoice validated by the Government portal before it counts.',
          'A company with ₹7 crore turnover issuing a B2B invoice without an IRN gives its customer no valid basis for ITC.'),
        C('c4', T4, [
            'Section 34(1): a credit note is issued where the taxable value or tax charged exceeds what is payable, goods are returned, services are found deficient, or (after the Finance Act, 2026, from the notified date) a post-supply discount under section 15(3)(b) is allowed.',
            'It must be declared in the return by 30 November following the end of the financial year of supply or the date of the annual return, whichever is earlier; the supplier\'s tax is reduced only if the incidence has not been passed on.',
            'Section 34(3): a debit note is issued where taxable value or tax charged is less than payable; it is declared in the return for the month of issue, with no outer time limit for the supplier.'],
          'Credit notes reduce, debit notes increase — and both must be traceable to an earlier supply.',
          'A price cut agreed in March for goods supplied in October can be passed through a credit note before 30 November of the next year.'),
    ]

    jobs = [{'id': 'j1', 'title': 'E-invoice readiness', 'role': 'Article assistant',
             'situation': 'A client\'s turnover crossed ₹5 crore last year.',
             'steps': ['Confirm the turnover in any year since 2017-18.', 'Configure the billing system for IRP upload.', 'Print IRN and QR code on B2B invoices.', 'Report within 30 days if turnover is ₹10 crore or more.'],
             'takeaway': 'Once the limit is crossed in any year, e-invoicing continues even if turnover falls later.'}]

    mcqs = [
        Q('m1', 'A tax invoice for goods involving movement must be issued:', ['Before or at the time of removal', 'Within 30 days of removal', 'At the time of payment', 'At month end'], 0,
          'Section 31(1)(a) ties the goods invoice to removal where there is movement. In practice: the e-way bill uses the invoice details.', 'c1', T1),
        Q('m2', 'A bank must issue a tax invoice for services within:', ['45 days', '30 days', '60 days', '15 days'], 0,
          'Rule 47 gives insurers, banks and NBFCs 45 days; others 30 days. In practice: monthly consolidated invoices are common for banks.', 'c1', T1, check=45),
        Q('m3', 'A composition dealer issues:', ['A bill of supply', 'A tax invoice', 'A receipt voucher', 'A delivery challan'], 0,
          'Composition taxpayers cannot collect tax and issue bills of supply. In practice: they must mention their status.', 'c2', T2),
        Q('m4', 'Goods sent for job work move under a:', ['Delivery challan', 'Tax invoice', 'Bill of supply', 'Credit note'], 0,
          'Movement that is not a supply, like sending goods to a job worker, is covered by a delivery challan. In practice: an e-way bill may also be needed.', 'c2', T2),
        Q('m5', 'E-invoicing applies to registered persons whose aggregate turnover in any year since 2017-18 exceeded:', ['₹5 crore', '₹10 crore', '₹20 crore', '₹1.5 crore'], 0,
          'The current limit is ₹5 crore, applied to B2B invoices and exports. In practice: once applicable, it continues.', 'c3', T3, check=5),
        Q('m6', 'A taxpayer with turnover of ₹3 crore must show HSN on B2B invoices at:', ['4 digits', '6 digits', '8 digits', 'Not required'], 0,
          'Up to ₹5 crore, 4-digit HSN on B2B invoices; above ₹5 crore, 6 digits. In practice: B2C invoices of small taxpayers may omit it.', 'c3', T3),
        Q('m7', 'A credit note for FY 2026-27 supplies must be declared by:', ['30 November 2027 or annual return date, if earlier', '31 March 2027', '31 December 2027', 'No limit'], 0,
          'Section 34(2) uses the earlier of 30 November after the year end and the annual return date. In practice: plan year-end settlements early.', 'c4', T4),
        Q('m8', 'A debit note is issued when:', ['Tax charged is less than tax payable', 'Goods are returned', 'Services are deficient', 'A discount is given'], 0,
          'Debit notes increase value or tax; the other cases call for credit notes. In practice: declare it in the month of issue.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Credit note', 1, 'concept', 'credit note'), S('s2', 'Time limit', 1, 'concept', '30 november'), S('s3', 'Net tax', 1, 'computation', 'net', nums=[out]), S('s4', 'Debit note', 1, 'concept', 'debit note')],
          ['State both documents.'], ['Issuing a fresh invoice for the return.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Bill of supply', 1, 'concept', 'bill of supply'), S('s2', 'Receipt voucher', 1, 'concept', 'receipt voucher'), S('s3', 'Self-invoice', 1, 'concept', 'self-invoice'),
           S('s4', 'Delivery challan', 1, 'concept', 'delivery challan'), S('s5', 'Below ₹200', 1, 'concept', 'consolidated')],
          ['Name the document.'], ['Using tax invoice everywhere.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'When must a service invoice be issued?', 'Within 30 days from the date of supply of service, or 45 days for insurers, banks and financial institutions.',
          [P('p1', '30 days', 6, '30 days'), P('p2', '45 days exception', 4, '45')], 'c1'),
        V('v2', 'What is a self-invoice?', 'An invoice the recipient issues on himself for supplies received from an unregistered supplier on which he pays tax under reverse charge.',
          [P('p1', 'Recipient issues', 5, 'recipient'), P('p2', 'Unregistered supplier', 5, 'unregistered')], 'c2'),
        V('v3', 'What is an IRN?', 'The invoice reference number generated by the Invoice Registration Portal when an e-invoice is reported, printed with a QR code on the invoice.',
          [P('p1', 'Registration portal', 5, 'portal|irp'), P('p2', 'QR code', 5, 'qr')], 'c3'),
        V('v4', 'When is a credit note issued?', 'When value or tax charged is more than payable, goods are returned, services are deficient, or a qualifying post-supply discount is given.',
          [P('p1', 'Excess value or tax', 5, 'excess|more than'), P('p2', 'Return or deficiency', 5, 'return|deficient')], 'c4'),
        V('v5', 'How many copies of a goods invoice are made?', 'Three: original for the recipient, duplicate for the transporter and triplicate for the supplier.',
          [P('p1', 'Triplicate', 5, 'three|triplicate'), P('p2', 'Transporter copy', 5, 'transporter')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Peak Pharma', 'difficulty': 'moderate',
              'case': 'Peak Pharma (aggregate turnover ₹12 crore) supplies medicines to hospitals and pharmacies. It receives an advance from a hospital, sends goods on approval to a new pharmacy, and later finds that it charged 5% instead of 12% on one batch.',
              'mcqs': [
                  M('k1a', 'For B2B invoices, Peak must:', ['Generate e-invoices and report within 30 days', 'Issue only paper invoices', 'Issue bills of supply', 'Report within 90 days'], 0,
                    'Turnover above ₹5 crore requires e-invoicing; at ₹10 crore or more, reporting within 30 days. In practice: late reporting invalidates the invoice.', 'moderate', topic=T3),
                  M('k1b', 'Goods sent on approval move under:', ['A delivery challan', 'A tax invoice at dispatch', 'A bill of supply', 'A self-invoice'], 0,
                    'Goods on approval are not yet supplied; they move under a delivery challan, and the invoice follows on approval or within six months. In practice: track the six-month limit.', 'moderate', topic=T2),
                  M('k1c', 'To correct the undercharged rate, Peak issues:', ['A debit note', 'A credit note', 'A refund voucher', 'A revised invoice'], 0,
                    'Tax charged was less than payable, so a debit note is issued. In practice: the hospital can take credit on it.', 'core', topic=T4),
                  M('k1d', 'For the hospital\'s advance on goods, Peak issues:', ['A receipt voucher', 'A tax invoice', 'A debit note', 'No document'], 0,
                    'A receipt voucher is issued on receiving any advance, though tax on advances for goods is not payable. In practice: adjust it in the final invoice.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch10', 1, 'Tax Invoice; Credit and Debit Notes',
                ['Determine when a tax invoice must be issued.',
                 'Choose the right document for each situation.',
                 'Apply invoice content, HSN and e-invoicing rules.',
                 'Apply the rules for credit and debit notes.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 25}, 'prereq': ['int-p3-b-ch09-u01'],
                 'exam_tip': 'Questions often hide a document choice — read for advance, return, job work or composition cues.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Goods: invoice at removal/delivery; services: 30 days (45 for banks).',
                             'Bill of supply; receipt/refund/payment vouchers; self-invoice; delivery challan.',
                             'E-invoice above ₹5 crore; 30-day reporting at ₹10 crore+; HSN 4/6 digits.',
                             'Credit note by 30 November or annual return; debit note in month of issue.'],
                 'remember': ['Below ₹200 to unregistered: consolidated daily invoice.', 'Revised invoices within one month of registration.'],
                 'traps': ['Invoice without IRN is invalid when e-invoicing applies.', 'Goods on approval: invoice within six months.']},
                [('Service invoice', '30 / 45 days'), ('E-invoice', '> ₹5 crore'), ('Credit note limit', '30 November'), ('Small sale', '< ₹200')],
                viva, cases)
