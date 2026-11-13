"""CA Final · Paper 4 · Chapter 18 Miscellaneous Provisions.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch18-u01'
T1 = 'Restrictions on cash loans, deposits and receipts'
T2 = 'Electronic payment facility and repayments'
T3 = 'Protection of revenue: void transfers and attachment'
T4 = 'Reporting, representation and general provisions'


def build():
    ck = Checks()
    p1 = ck.add('25000', 'Penalty for cash loan taken (₹)')
    p2 = ck.add('250000', 'Penalty for cash receipt of ₹2.5 lakh (₹)')
    p3 = ck.add('30000', 'Penalty for cash repayment of deposit (₹)')
    tot = ck.add('25000+250000+30000', 'Total penalties (₹)')
    i1 = {'id': 'i1', 'title': 'Cash transactions and penalties', 'difficulty': 'core', 'minutes': 6,
          'q': 'Rakesh, a trader, in T.Y. 2026-27: (a) accepts a cash loan of ₹25,000 from a friend; (b) receives ₹2,50,000 in cash from one buyer for a single sale of goods; (c) repays a customer deposit of ₹30,000 in cash. Compute the maximum penalties.',
          'solution': [table(['Transaction', 'Provision', '₹'], [
              ['(a) Loan', 'Section 185 / penalty u/s 450 — equal to loan', inr(p1)],
              ['(b) Receipt', 'Section 186 / penalty u/s 451 — equal to receipt', inr(p2)],
              ['(c) Repayment', 'Section 188 / penalty u/s 453 — equal to repayment', inr(p3)],
              ['Total', '', inr(tot)]], title='Cash restrictions')],
          'checks': list(ck)}

    c2 = Checks()
    agg = c2.add('80000*3', 'Aggregate cash received for one event (₹)')
    dp = c2.add('5000*20', 'Penalty for 20 days without e-payment facility (₹)')
    i2 = {'id': 'i2', 'title': 'One event, many days; missing e-payment facility', 'difficulty': 'moderate', 'minutes': 5,
          'q': '(a) A caterer receives ₹80,000 in cash on each of three different days from one family for one wedding. (b) A retailer with turnover of ₹60 crore last year fails to provide the prescribed electronic payment facility for 20 days. Determine the consequences.',
          'solution': [table(['Item', 'Rule', 'Result'], [
              ['(a) Wedding receipts', 'Aggregate for one event or occasion from a person', f'₹{inr(agg)} — penalty equal to amount'],
              ['(b) E-payment facility', 'Section 187; penalty ₹5,000 per day (section 452)', f'₹{inr(dp)}']], title='Sections 186 and 187')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 185: no person may take or accept a loan, deposit or specified sum (advance for transfer of immovable property) of ₹20,000 or more — counting the new amount, any outstanding balance, or both — otherwise than by account payee cheque or draft, ECS or prescribed electronic modes. A ₹2 lakh limit applies to transactions between primary agricultural credit societies or rural development banks and their members. Government, banks, post office savings banks, government companies and notified institutions are excluded, as are transactions where both parties have only agricultural income and no taxable income.',
            'Section 186: no person may receive ₹2 lakh or more in cash in aggregate from a person in a day, for a single transaction, or for one event or occasion where the money comes from the same person. Receipts by Government, banks and specified bodies, and receipts covered by section 185, are excluded.',
            'Penalties equal to the amount involved are levied under sections 450 and 451 respectively.'],
          'Large cash loans and receipts cost the full amount as penalty.',
          'Cash of ₹2.4 lakh received over three days for one wedding is caught by section 186.'),
        C('c2', T2, [
            'Section 187: a person carrying on business with turnover above ₹50 crore in the preceding year must provide prescribed electronic payment facilities; it does not apply where at least 95% of receipts are in non-cash modes and the business is B2B. Failure attracts ₹5,000 per day (section 452).',
            'Section 188: no branch of a bank, co-operative society, firm or other person may repay a loan, deposit or specified advance of ₹20,000 or more (including interest, and aggregated with the person\'s other such amounts) otherwise than by specified modes; ₹2 lakh for PACS/PCARD transactions with members.',
            'Penalty under section 453 equals the amount repaid. Prescribed electronic modes include credit and debit cards, net banking, IMPS, UPI, RTGS, NEFT, BHIM Aadhaar Pay and specified CBDC wallets.'],
          'Big businesses must accept digital payments; big repayments must be digital.',
          'A retailer that skips e-payment facilities for 20 days faces ₹1 lakh of penalty.'),
        C('c3', T3, [
            'Section 499: during pending proceedings or after their completion before notice of demand, a charge or transfer by the assessee of assets (exceeding ₹10,000 in value) is void against tax claims, unless made for adequate consideration without notice of the proceedings, or with the AO\'s permission.',
            'Section 500: the AO may provisionally attach property during assessment or reassessment proceedings to protect revenue, with approval of the PCIT/CIT and other specified authorities; the attachment lasts six months, extendable to two years, and can be revoked on furnishing a bank guarantee. The AO may refer the property to a Valuation Officer.',
            'Sections 501 to 504 deal with service of notices, including on HUFs after partition, dissolved firms and discontinued businesses.'],
          'The revenue can freeze assets to protect a likely demand.',
          'A transfer of a flat to a relative for no consideration during scrutiny is void against tax claims.'),
        C('c4', T4, [
            'Section 507 requires specified persons to file statements of reportable financial transactions (e.g. large cash deposits, mutual fund and property purchases) within prescribed time; section 508 covers reportable accounts under international exchange agreements; crypto-asset service providers report under section 509. Penalties apply for non-filing or inaccurate statements.',
            'Section 515: an assessee may appear through an authorised representative — a relative, regular employee, banking company officer, chartered accountant, legal practitioner, income-tax practitioner or other prescribed person — subject to disqualifications such as government service dismissal or professional misconduct.',
            'Section 523: notices are not invalid merely because of a mistake or defect, if in substance they conform to the Act; participation in proceedings bars challenging service. Section 536 repeals the 1961 Act with savings for pending matters.'],
          'Reporting, representation and procedural fairness complete the framework.',
          'A CA can appear on behalf of a client before the AO.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Cash-compliance audit', 'role': 'Tax auditor',
             'situation': 'A dealer\'s ledger shows several cash loans and customer receipts.',
             'steps': ['List cash loans and deposits at or above ₹20,000.', 'Aggregate receipts per day, transaction and event.', 'Check repayments in cash.', 'Report in the tax audit and advise the client.'],
             'takeaway': 'Aggregation rules catch split cash transactions.'}]

    mcqs = [
        Q('m1', 'Section 185 is triggered when a loan taken in cash is:', ['Twenty thousand rupees or more', 'Above fifty thousand rupees', 'Two lakh rupees or more', 'Ten thousand rupees or more'], 0,
          'Including outstanding balance. In practice: use bank modes.', 'c1', T1),
        Q('m2', 'Section 186 applies to cash receipts of:', ['Two lakh rupees or more', 'Twenty thousand rupees or more', 'Fifty thousand rupees or more', 'Ten lakh rupees or more'], 0,
          'Per day, transaction or event. In practice: aggregate.', 'c1', T1),
        Q('m3', 'Penalty for contravening section 186 equals:', ['The amount received', 'Ten percent of the amount', 'Twice the amount', 'Ten thousand rupees'], 0,
          'Section 451. In practice: no tax effect needed.', 'c1', T1),
        Q('m4', 'Electronic payment facility is mandatory for businesses with prior-year turnover above:', ['Fifty crore rupees', 'Ten crore rupees', 'One crore rupees', 'Hundred crore rupees'], 0,
          'Section 187. In practice: B2B exception.', 'c2', T2),
        Q('m5', 'Penalty for not providing the e-payment facility is:', ['Five thousand rupees per day', 'One lakh rupees flat', 'Equal to turnover', 'Ten thousand rupees per day'], 0,
          'Section 452. In practice: daily.', 'c2', T2),
        Q('m6', 'Repayment of a deposit of ₹25,000 in cash attracts penalty under:', ['Section 453', 'Section 450', 'Section 451', 'Section 452'], 0,
          'Section 188 contravention. In practice: equal to repayment.', 'c2', T2),
        Q('m7', 'A transfer during pending proceedings is void against tax claims if assets exceed:', ['Ten thousand rupees in value', 'One lakh rupees', 'Ten lakh rupees', 'Any value'], 0,
          'Section 499. In practice: adequate consideration exception.', 'c3', T3),
        Q('m8', 'Who can be an authorised representative?', ['A chartered accountant', 'A dismissed government servant', 'A person convicted of tax fraud', 'An insolvent person'], 0,
          'Section 515. In practice: written authority.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Loan and receipt', 3, 'computation', 'penalty', nums=[p1, p2]), S('s2', 'Repayment and total', 2, 'computation', 'repay', nums=[p3, tot])],
          ['Name sections.'], ['Applying percentage penalties.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Event aggregation', 2, 'analysis', 'event', nums=[agg]), S('s2', 'Daily penalty', 2, 'computation', 'per day', nums=[dp])],
          ['Explain aggregation.'], ['Treating each day separately.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is a specified sum for section 185?', 'Any advance taken for an immovable property deal, even if the deal later falls through.',
          [P('p1', 'Advance', 5, 'advance'), P('p2', 'Immovable property', 5, 'immovable property')], 'c1'),
        V('v2', 'Name three ways section 186 aggregates receipts.', 'Per person per day, per single transaction, and per event or occasion from a person.',
          [P('p1', 'Per day', 5, 'day'), P('p2', 'Event or occasion', 5, 'event')], 'c1'),
        V('v3', 'When can provisional attachment be revoked?', 'When the assessee furnishes a bank guarantee of the required amount.',
          [P('p1', 'Bank guarantee', 5, 'bank guarantee'), P('p2', 'Assessee furnishes', 5, 'furnish')], 'c3'),
        V('v4', 'What is a statement of reportable financial transactions?', 'A statement filed by specified persons reporting large transactions such as cash deposits and property purchases.',
          [P('p1', 'Specified persons', 5, 'specified persons'), P('p2', 'Large transactions', 5, 'transactions')], 'c4'),
        V('v5', 'Is a notice invalid due to a minor defect?', 'It remains valid if in substance it conforms to the Act, under section 523.',
          [P('p1', 'Valid', 5, 'valid'), P('p2', 'Substance', 5, 'substance')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Sunrise Jewellers', 'difficulty': 'core',
              'case': 'Sunrise Jewellers (turnover last year ₹72 crore, mostly retail) receives ₹1,50,000 in cash from Mr. Arora on 5 May and ₹90,000 on 5 May for a separate bill, and repays a scheme deposit of ₹40,000 in cash.',
              'mcqs': [
                  M('k1a', 'Aggregate cash from Mr. Arora on 5 May (₹):', ['2,40,000', '1,50,000', '90,000', '60,000'], 0,
                    'Same person, same day. In practice: aggregate.', 'core', check=240000, topic=T1),
                  M('k1b', 'Penalty under section 451 (₹):', ['2,40,000', '40,000', '24,000', 'Nil'], 0,
                    'Equal to receipt. In practice: receiver liable.', 'core', check=240000, topic=T1),
                  M('k1c', 'Penalty for the cash repayment of deposit (₹):', ['40,000', '20,000', 'Nil', '4,000'], 0,
                    'Section 453. In practice: use bank transfer.', 'core', check=40000, topic=T2),
                  M('k1d', 'Must Sunrise provide prescribed e-payment facilities?', ['Yes, turnover exceeds ₹50 crore', 'No, jewellers are exempt', 'Only if customers ask', 'Only for GST'], 0,
                    'Section 187. In practice: retail business.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch18', 1, 'Miscellaneous Provisions',
                ['Apply restrictions on cash loans, deposits and receipts.',
                 'Apply e-payment facility and repayment rules.',
                 'Apply provisions on void transfers and provisional attachment.',
                 'Apply reporting, representation and procedural provisions.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['fin-p4-ch17-u01'],
                 'exam_tip': 'Identify whether the cash is a loan, a receipt or a repayment; each has its own section and penalty.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 185 loans ≥ ₹20,000; penalty u/s 450.', 'Section 186 receipts ≥ ₹2 lakh; penalty u/s 451.', 'Section 187 e-payment; ₹5,000/day.',
                             'Section 188 repayments; penalty u/s 453.', 'Sections 499–500 protection of revenue; 507 reporting; 515 representatives.'],
                 'remember': ['Penalties equal the amount involved.'],
                 'traps': ['Missing event-wise aggregation under section 186.']},
                [('Cash loans', 'Section 185'), ('Cash receipts', 'Section 186'), ('E-payment', 'Section 187'), ('Repayments', 'Section 188'), ('Attachment', 'Section 500')],
                viva, cases)
