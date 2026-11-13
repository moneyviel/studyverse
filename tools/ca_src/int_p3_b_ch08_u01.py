"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 8 Input Tax Credit.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch08-u01'
T1 = 'Eligibility and conditions (s. 16)'
T2 = 'Apportionment and blocked credits (s. 17)'
T3 = 'Special cases (s. 18) and input service distributor (s. 20)'
T4 = 'Utilisation of ITC (ss. 49, 49A, 49B)'


def build():
    ck = Checks()
    itc = ck.add('180000+36000+9000+27000', 'Eligible ITC')
    i1 = {'id': 'i1', 'title': 'Sorting a month\'s purchases', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'Prime Fabricators (manufacturer, all supplies taxable) paid GST in a month on: raw material ₹1,80,000; a forklift used in the factory ₹36,000; a car (5 seats) for directors ₹1,40,000; canteen food for staff (not required by any law) ₹12,000; repairs to factory machinery ₹9,000; construction of a new office building ₹2,50,000; freight paid to a GTA under forward charge ₹27,000. All invoices appear in GSTR-2B. Compute eligible ITC.',
          'solution': [table(['Item', 'Eligible?', 'ITC ₹'], [
              ['Raw material', 'Yes — input used in business', inr(180000)],
              ['Forklift', 'Yes — capital goods; not a motor vehicle for transport of persons', inr(36000)],
              ['Directors\' car', 'No — blocked u/s 17(5)(a)', '0'],
              ['Canteen food', 'No — blocked u/s 17(5)(b) (not obligatory under law)', '0'],
              ['Machinery repairs', 'Yes — plant and machinery', inr(9000)],
              ['Office building construction', 'No — blocked u/s 17(5)(d)', '0'],
              ['GTA freight', 'Yes — input service', inr(27000)],
              ['Eligible ITC', '', inr(itc)]], title='Sections 16 and 17')],
          'checks': list(ck)}

    ck2 = Checks()
    i_i = ck2.add('70000', 'IGST liability met from IGST credit')
    i_c = ck2.add('90000-70000', 'Balance IGST credit used for CGST')
    c_c = ck2.add('50000-20000', 'CGST still payable, met from CGST credit')
    s_s = ck2.add('50000-0', 'SGST payable, met from SGST credit')
    cash = ck2.add('max(0,30000-30000)+max(0,50000-40000)', 'Cash payable')
    i2 = {'id': 'i2', 'title': 'Setting off credits', 'difficulty': 'hard', 'minutes': 9,
          'q': 'Output tax for the month: IGST ₹70,000, CGST ₹50,000, SGST ₹50,000. Opening ITC: IGST ₹90,000, CGST ₹30,000, SGST ₹40,000. Show the utilisation and the cash payable.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['IGST credit → IGST liability', '', inr(i_i)],
              ['Balance IGST credit (₹20,000) → CGST (or SGST)', 'IGST must be exhausted first', inr(i_c)],
              ['CGST balance liability', '50,000 − 20,000; paid from CGST credit 30,000', inr(c_c)],
              ['SGST liability', 'Paid from SGST credit 40,000; balance 10,000 in cash', inr(s_s)],
              ['Cash payable', 'SGST 10,000', inr(cash)]], title='Order under ss. 49, 49A and 49B'),
              note('CGST credit can never pay SGST, and SGST credit can never pay CGST.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Section 16(1): a registered person may take credit of tax charged on goods or services used or intended to be used in the course or furtherance of business.',
            'Section 16(2) conditions: he holds a tax invoice or debit note; the details are furnished by the supplier and communicated in GSTR-2B; he has received the goods or services (including delivery to another person on his direction); the supplier has actually paid the tax; and he has filed his own return. For goods in lots, credit is taken on receipt of the last lot.',
            'If the recipient does not pay the supplier within 180 days of the invoice (except reverse charge cases), the credit is added to his output tax with interest; it can be reclaimed on payment. No ITC is allowed on the tax component if depreciation has been claimed on it.',
            'Section 16(4): ITC for a year cannot be taken after 30 November following the end of that financial year or the filing of the annual return, whichever is earlier.'],
          'Credit flows only if the paper trail, the goods and the supplier\'s tax payment all line up.',
          'An invoice dated 5 March 2026 missed in the books can still be claimed until 30 November 2026, if the annual return is not filed earlier.'),
        C('c2', T2, [
            'Section 17(1)–(2): where inputs are used partly for business and partly for other purposes, or partly for taxable and partly for exempt supplies, only the business/taxable share is allowed (Rules 42–43).',
            'Section 17(5) blocks credit on: motor vehicles for transport of persons with up to 13 seats (including driver), and their insurance, repair and maintenance — unless used for further supply of vehicles, passenger transport or driving training, or (for repairs/insurance) by a manufacturer or insurer of such vehicles; vessels and aircraft with similar exceptions.',
            'Also blocked: food and beverages, outdoor catering, beauty treatment, health services, cosmetic surgery, renting of vehicles, life and health insurance — unless used for an outward supply of the same category or as part of a composite or mixed supply, or obligatory for an employer under law; club and fitness memberships; travel benefits to employees on vacation; works contracts and goods or services for construction of immovable property on own account (other than plant or machinery), even if capitalised; tax paid under composition; goods lost, stolen, destroyed, written off, gifted or given as free samples; goods or services for personal consumption; tax paid on demands involving fraud; and expenses on corporate social responsibility obligations.',
            '"Plant and machinery" means apparatus, equipment and machinery fixed to earth by foundation or structural support and used for outward supply, including such foundations; it excludes land, buildings, other civil structures, telecom towers and pipelines laid outside the factory.'],
          'Blocked credits target personal-type consumption and immovable property — not genuine production inputs.',
          'A cab operator can take credit on cars it buys for passenger transport; a software firm cannot for its managers\' cars.'),
        C('c3', T3, [
            'Section 18: a person applying for registration within 30 days of becoming liable can take credit on inputs held in stock (and in semi-finished or finished goods) on the day before liability; a voluntary registrant on the day before registration; a person leaving composition or whose exempt supply becomes taxable on the day before the change (plus capital goods less 5 percentage points per quarter). This credit must be claimed within one year of the invoice date.',
            'On a change in constitution (merger, sale, lease or transfer of business) with transfer of liabilities, unused credit passes to the transferee. On sale of capital goods, the supplier pays the higher of ITC taken less 5 percentage points per quarter and tax on transaction value.',
            'Section 20: an input service distributor is an office that receives tax invoices for input services (including those under reverse charge) on behalf of distinct persons with the same PAN and distributes the credit to them. From 1 April 2025 registration as ISD is mandatory for such common services; distribution is in proportion to the turnover of the recipient units in the State.'],
          'Section 18 lets new or changing taxpayers carry the tax in their opening stock; ISD spreads common credit to the right branches.',
          'A trader registering on day 25 after crossing the threshold can claim credit on the stock in hand the day before he became liable.'),
        C('c4', T4, [
            'The electronic credit ledger is used only for output tax, not for interest, penalty, fees or reverse charge tax (which are paid in cash).',
            'Order: IGST credit is used first for IGST, then for CGST and SGST/UTGST in any order and proportion; CGST credit for CGST, then IGST; SGST credit for SGST, then IGST. CGST credit cannot pay SGST or UTGST, and vice versa. IGST credit must be fully used before CGST or SGST credit is used.',
            'Rule 86B requires certain registered persons whose monthly taxable supply exceeds ₹50 lakh to pay at least 1% of output tax in cash, subject to exclusions.'],
          'Credit is ring-fenced: the Centre\'s credit pays the Centre, the State\'s pays the State, and IGST bridges both.',
          'With IGST credit of ₹1 lakh and CGST liability of ₹40,000 left after IGST, the IGST credit pays the CGST first.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Monthly ITC reconciliation', 'role': 'Article assistant',
             'situation': 'The purchase register shows more credit than GSTR-2B.',
             'steps': ['Match each invoice with GSTR-2B.', 'Follow up suppliers for missing invoices.', 'Remove blocked and personal items.', 'Track invoices unpaid beyond 180 days.'],
             'takeaway': 'Only credit that is both eligible and reflected in GSTR-2B may be claimed.'}]

    mcqs = [
        Q('m1', 'ITC cannot be claimed unless the invoice details are reflected in:', ['GSTR-2B', 'GSTR-9', 'Form ITC-04', 'E-way bill'], 0,
          'Section 16(2)(aa) requires the details to be communicated to the recipient through GSTR-2B. In practice: chase suppliers to file GSTR-1 on time.', 'c1', T1),
        Q('m2', 'If the supplier is not paid within 180 days, the recipient must:', ['Add the ITC to output tax with interest; reclaim on payment', 'Lose the credit permanently', 'Pay a penalty only', 'Do nothing'], 0,
          'The second proviso to section 16(2) reverses the credit with interest, but it can be re-availed once payment is made. In practice: monitor creditor ageing.', 'c1', T1),
        Q('m3', 'ITC for FY 2025-26 (annual return not yet filed) can be taken up to:', ['30 November 2026', '31 March 2026', '31 December 2026', '30 September 2026'], 0,
          'Section 16(4): the earlier of 30 November following the year and the annual return date. In practice: claim before that date.', 'c1', T1),
        Q('m4', 'ITC on a 7-seater car is allowed to:', ['A taxi operator using it for passenger transport', 'A CA firm for partners\' travel', 'A manufacturer for staff pick-up not required by law', 'A trader for personal use'], 0,
          'Vehicles of up to 13 seats are blocked unless used for further supply, passenger transport or driving training. In practice: goods carriers are not blocked.', 'c2', T2),
        Q('m5', 'ITC on construction of a factory shed is:', ['Blocked', 'Allowed fully', 'Allowed 50%', 'Allowed if capitalised'], 0,
          'Goods and services for construction of immovable property on own account (other than plant or machinery) are blocked even if capitalised. In practice: machinery foundations are allowed.', 'c2', T2),
        Q('m6', 'Which is NOT blocked under section 17(5)?', ['Food provided to employees where a law obliges the employer', 'Club membership', 'Vacation travel for employees', 'Free samples'], 0,
          'Food, health and similar items are allowed where provision is obligatory for an employer under any law. In practice: check the Factories Act requirement.', 'c2', T2),
        Q('m7', 'Credit on opening stock under section 18 must be claimed within:', ['One year from the invoice date', '30 days', '180 days', 'No limit'], 0,
          'Section 18(2) bars credit after one year from the date of the invoice for the goods. In practice: older stock gives no credit.', 'c3', T3),
        Q('m8', 'CGST credit can be used to pay:', ['CGST and IGST', 'SGST and IGST', 'Any tax', 'Interest'], 0,
          'CGST credit pays CGST first and then IGST; it can never pay SGST/UTGST, and no credit pays interest. In practice: plan inter-State purchases accordingly.', 'c4', T4),
        Q('m9', 'Input service distributor registration is mandatory, from 1 April 2025, for:', ['Common input services, including reverse charge services, for distinct persons', 'All traders', 'Exporters only', 'Composition taxpayers'], 0,
          'Section 20 now requires ISD registration where common input services are used by distinct persons under the same PAN. In practice: distribute by turnover ratio.', 'c3', T3),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Inputs and capital goods', 2, 'concept', 'capital|input'), S('s2', 'Blocked items', 2, 'concept', '17(5)'), S('s3', 'Total', 2, 'computation', 'eligible', nums=[itc])],
          ['Give the clause for each disallowance.'], ['Allowing building construction credit.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'IGST first', 1, 'computation', 'IGST', nums=[i_i]), S('s2', 'Balance IGST to CGST', 1, 'computation', 'balance', nums=[i_c]),
           S('s3', 'CGST and SGST', 2, 'computation', 'CGST|SGST', nums=[c_c]), S('s4', 'Cash', 1, 'computation', 'cash', nums=[cash])],
          ['Exhaust IGST first.'], ['Using CGST credit for SGST.'], ['Step table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'List the conditions of section 16(2).', 'Possession of a tax invoice or debit note, details reflected in GSTR-2B, receipt of goods or services, actual payment of tax by the supplier and filing of the recipient\'s return.',
          [P('p1', 'Invoice and 2B', 5, 'invoice|2b'), P('p2', 'Receipt and supplier payment', 5, 'receipt|paid')], 'c1'),
        V('v2', 'Why is credit on immovable property blocked?', 'Because buildings and civil structures are not part of the taxable supply chain like plant or machinery; section 17(5)(c) and (d) block works contracts and goods or services for own construction.',
          [P('p1', '17(5)', 5, '17(5)'), P('p2', 'Construction', 5, 'construction|works contract')], 'c2'),
        V('v3', 'What is plant and machinery for section 17?', 'Apparatus, equipment and machinery fixed to earth by foundation or structural support and used for making outward supplies, including the foundation, but excluding land, buildings and other civil structures.',
          [P('p1', 'Fixed to earth', 5, 'fixed|foundation'), P('p2', 'Exclusions', 5, 'land|building|civil')], 'c2'),
        V('v4', 'What is an input service distributor?', 'An office that receives invoices for input services used by distinct persons with the same PAN and distributes the credit to them.',
          [P('p1', 'Receives invoices', 5, 'invoice'), P('p2', 'Distributes', 5, 'distribut')], 'c3'),
        V('v5', 'In what order is IGST credit used?', 'First against IGST, and then against CGST and SGST or UTGST in any order and proportion, before any CGST or SGST credit is used.',
          [P('p1', 'IGST first', 6, 'first'), P('p2', 'Then CGST/SGST', 4, 'cgst|sgst')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Nova Hotels', 'difficulty': 'moderate',
              'case': 'Nova Hotels (registered, taxable outward supply of rooms and restaurant services with ITC) buys: (i) food ingredients for its restaurant; (ii) a 12-seater van to ferry guests for a fee; (iii) membership of a golf club for its CEO; (iv) a commercial kitchen exhaust system bolted to a foundation.',
              'mcqs': [
                  M('k1a', 'ITC on food ingredients (i):', ['Allowed', 'Blocked as food', 'Allowed 50%', 'Blocked for hotels'], 0,
                    'Food is blocked only when not used for an outward supply of the same category; here it is used to supply restaurant services. In practice: check the outward supply is taxable with ITC.', 'moderate', topic=T2),
                  M('k1b', 'ITC on the van (ii):', ['Allowed, as used for passenger transport', 'Blocked as a vehicle under 13 seats', 'Allowed only on insurance', 'Blocked always'], 0,
                    'Vehicles up to 13 seats are blocked unless used for transport of passengers, which is the case here. In practice: keep proof of the guest transfer service.', 'moderate', topic=T2),
                  M('k1c', 'ITC on golf club membership (iii):', ['Blocked', 'Allowed', 'Allowed if the CEO is a director', 'Allowed 50%'], 0,
                    'Membership of clubs and fitness centres is blocked under section 17(5)(b). In practice: treat it as a cost.', 'core', topic=T2),
                  M('k1d', 'ITC on the exhaust system (iv):', ['Allowed as plant and machinery', 'Blocked as immovable property', 'Blocked as a civil structure', 'Allowed only if not capitalised'], 0,
                    'Equipment fixed by foundation and used for outward supply is plant and machinery, which is outside the block. In practice: civil works around it are blocked.', 'hard', topic=T2),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch08', 1, 'Input Tax Credit',
                ['Apply the eligibility conditions and time limits for ITC.',
                 'Identify blocked credits and apportion common credit.',
                 'Apply special cases, ISD and the utilisation order.'],
                {'difficulty': 'hard', 'minutes': {'learn': 55, 'practice': 45}, 'prereq': ['int-p3-b-ch07-u01'],
                 'exam_tip': 'For every purchase in a question, write "allowed" or "blocked" with the exact clause of section 17(5).'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['s. 16(2): invoice, GSTR-2B, receipt, supplier paid, own return; 180-day payment rule.',
                             's. 16(4): by 30 November after the year or annual return, if earlier.',
                             's. 17(5): vehicles ≤ 13 seats, food/health/clubs, own construction, free samples, CSR.',
                             's. 18: stock credit on registration within one year of invoice; s. 20 ISD mandatory.',
                             'Utilisation: IGST first; CGST ↔ SGST never.'],
                 'remember': ['No ITC on tax component if depreciation is claimed on it.', 'RCM tax is paid in cash.'],
                 'traps': ['Plant and machinery excludes buildings and telecom towers.', 'Food allowed when obligatory under law for employer.']},
                [('Payment to supplier', '180 days'), ('ITC time limit', '30 November / annual return'), ('Vehicle block', '≤ 13 seats'), ('Stock credit', '1 year from invoice')],
                viva, cases)
