"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 7 Value of Supply.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch07-u01'
T1 = 'Transaction value (s. 15(1))'
T2 = 'Inclusions and discounts (s. 15(2)–(3))'
T3 = 'Valuation rules where transaction value cannot be used (Rules 27–31)'
T4 = 'Special rules and pure agent (Rules 32–33)'


def build():
    ck = Checks()
    val = ck.add('500000+20000+15000+8000+12000-25000', 'Value of supply')
    tax = ck.add('530000*18/100', 'GST at 18%')
    i1 = {'id': 'i1', 'title': 'Building up the value', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Vega Machines sells a machine to an unrelated buyer. Contract price ₹5,00,000 (excluding GST at 18%). Additional facts: (i) packing charged separately ₹20,000; (ii) a municipal tax of ₹15,000 levied on the supplier is paid by the buyer; (iii) design charges of ₹8,000 paid by the buyer directly to a consultant engaged by Vega; (iv) interest for late payment ₹12,000 received later; (v) a discount of ₹25,000 shown on the invoice. Compute the value and GST.',
          'solution': [table(['Item', 'Treatment', '₹'], [
              ['Contract price', 'Transaction value', inr(500000)],
              ['Packing', 'Incidental expense charged by supplier — include', inr(20000)],
              ['Municipal tax', 'Tax other than GST — include', inr(15000)],
              ['Design charges paid by buyer', 'Supplier\'s liability met by recipient — include', inr(8000)],
              ['Late payment interest', 'Include (taxed when received)', inr(12000)],
              ['Discount on invoice', 'Given at the time of supply and shown on invoice — exclude', '(25,000)'],
              ['Value of supply', '', inr(val)],
              ['GST @18%', '', inr(tax)]], title='Section 15'),
              note('GST itself is never part of the value.')],
          'checks': list(ck)}

    ck2 = Checks()
    r28 = ck2.add('90/100*100000', 'Rule 28 option: 90% of the price charged by the related recipient to its customers')
    r27 = ck2.add('60000+15000', 'Rule 27: money + monetary value of goods exchanged')
    i2 = {'id': 'i2', 'title': 'When price is not enough', 'difficulty': 'hard', 'minutes': 8,
          'q': '(a) Akash Ltd. supplies goods to its related company, which resells them as such to unrelated customers at ₹1,00,000. Akash opts for the value under the second proviso to Rule 28. (b) A dealer sells a new phone for ₹60,000 plus the customer\'s old phone; the price without exchange would be ₹75,000 and the old phone\'s value is known as ₹15,000. Determine the value in each case.',
          'solution': [table(['Case', 'Rule', 'Value ₹'], [
              ['(a)', 'Related person reselling as such: at supplier\'s option, 90% of the price charged to the unrelated customer', inr(r28)],
              ['(b)', 'Non-monetary consideration: open market value ₹75,000, which equals money (60,000) + monetary value of the old phone (15,000)', inr(r27)]], title='Rules 27 and 28'),
              note('Where the related recipient can take full ITC, the invoice value is accepted as the open market value under Rule 28.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Section 15(1): value is the transaction value — the price actually paid or payable — where supplier and recipient are not related and price is the sole consideration.',
            'Related persons include officers or directors of each other\'s businesses, partners, employer and employee, persons controlling or controlled by a common third person, holders of 25% or more of each other\'s voting shares, and members of the same family.',
            'Where these conditions fail, value is found under the Valuation Rules.'],
          'Normal arm\'s-length price is the starting point; the rules step in only when that price is unreliable.',
          'A sale between a father\'s firm and his son\'s company is between related persons, so the rules may apply.'),
        C('c2', T2, [
            'Section 15(2) includes: taxes, duties, cesses, fees and charges under other laws (but not GST); amounts the supplier is liable to pay but that the recipient pays and that are not already in the price; incidental expenses such as commission and packing charged by the supplier, and anything done by the supplier at or before delivery; interest, late fee or penalty for delayed payment; and subsidies directly linked to the price, except subsidies from the Central and State Governments.',
            'Section 15(3)(a): a discount given before or at the time of supply and recorded in the invoice is excluded.',
            'Section 15(3)(b): a post-supply discount was traditionally excluded only if agreed before the supply, linked to specific invoices and reversed by the recipient as ITC. The Finance Act, 2026 simplifies this, from the notified date, to require only a credit note under section 34 with the recipient reversing the corresponding ITC.'],
          'Value is everything the buyer pays for the supply, directly or on the supplier\'s behalf — but never GST itself.',
          'A Government subsidy on solar panels is not added to value; a private manufacturer\'s subsidy to its dealer\'s price is.'),
        C('c3', T3, [
            'Rule 27 — consideration not wholly in money: open market value; if not available, money plus the monetary value of the non-money part; then value of like kind and quality; then cost plus 10% or residual method.',
            'Rule 28 — distinct or related persons (other than through an agent): open market value; then like kind and quality; then cost plus 10% or residual. At the supplier\'s option, where the recipient resells the goods as such, 90% of the price charged to an unrelated customer. Where the recipient is eligible for full ITC, the invoice value is deemed open market value.',
            'Rule 29 — supply through an agent: open market value or, at the supplier\'s option, 90% of the price charged by the recipient to unrelated customers. Rule 30 — cost of production plus 10%. Rule 31 — residual reasonable means consistent with section 15 (for services, Rule 30 may be skipped).'],
          'The rules form a ladder: try each step in order and stop when one works.',
          'Free stock transfer to a branch where the branch is entitled to full ITC: whatever value is invoiced is accepted.'),
        C('c4', T4, [
            'Rule 32 gives special values: buying or selling foreign currency (difference between buying or selling rate and RBI reference rate, or notified slabs); air travel agents (5% of basic fare for domestic, 10% for international bookings); life insurance (premium less investment portion, or set percentages); second-hand goods dealers without ITC (selling price minus purchase price, ignoring negative margin); and tokens or vouchers (money value redeemable).',
            'Rule 33 — pure agent: expenditure incurred as a pure agent of the recipient is excluded from value if the agent contracts on the recipient\'s behalf, does not use the procured supply for itself, recovers the exact amount, and shows it separately on the invoice.',
            'Inter-branch supplies of services and supplies between distinct persons are valued under Rule 28.'],
          'Some trades have their own measuring sticks, and genuine reimbursements of a pure agent stay out of value.',
          'A customs broker recovering the exact port charges paid in the client\'s name, shown separately, excludes them from value.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Invoice value review', 'role': 'Article assistant',
             'situation': 'A client recovers freight, packing and "reimbursements" from customers but charges GST only on the base price.',
             'steps': ['List each additional recovery.', 'Test each against section 15(2) and Rule 33.', 'Add non-pure-agent recoveries to value.', 'Correct the invoices and pay any short tax with interest.'],
             'takeaway': 'Most "reimbursements" are part of value unless every pure-agent condition is met.'}]

    mcqs = [
        Q('m1', 'Transaction value is accepted when:', ['Parties are unrelated and price is the sole consideration', 'The supplier is registered', 'Price is above cost', 'Payment is in cash'], 0,
          'Section 15(1) needs both conditions; otherwise the Valuation Rules apply. In practice: check relationships carefully.', 'c1', T1),
        Q('m2', 'Which is NOT included in value?', ['CGST and SGST', 'Packing charged by supplier', 'Interest for late payment', 'Municipal tax paid by buyer on supplier\'s behalf'], 0,
          'GST under the GST laws is excluded; other taxes, incidentals and late payment interest are included. In practice: show GST separately.', 'c2', T2),
        Q('m3', 'A subsidy directly linked to price is included in value unless given by:', ['Central or State Government', 'A manufacturer', 'An NGO', 'A trade association'], 0,
          'Section 15(2)(e) excludes Central and State Government subsidies. In practice: private subsidies add to value.', 'c2', T2),
        Q('m4', 'A discount shown on the invoice at the time of supply is:', ['Excluded from value', 'Included in value', 'Taxed separately', 'Allowed only with prior approval'], 0,
          'Section 15(3)(a) excludes discounts given before or at the time of supply and recorded in the invoice. In practice: no credit note is needed.', 'c2', T2),
        Q('m5', 'Under Rule 28, if the related recipient is eligible for full ITC, value is:', ['The invoice value', '110% of cost', '90% of resale price', 'Open market value as certified'], 0,
          'The second proviso deems the invoice value to be open market value where the recipient can take full credit. In practice: this simplifies branch transfers.', 'c3', T3),
        Q('m6', 'Rule 30 values a supply at:', ['110% of cost of production or acquisition', '90% of selling price', 'Open market value', 'Cost alone'], 0,
          'Rule 30 uses cost of production, manufacture or acquisition plus 10%. In practice: it is used only when earlier rules fail.', 'c3', T3),
        Q('m7', 'Value for an air travel agent on a domestic booking (basic fare ₹10,000), at the agent\'s option:', ['₹500', '₹1,000', '₹10,000', '₹250'], 0,
          'Rule 32(3) allows 5% of the basic fare for domestic tickets (10% for international). In practice: the agent\'s own commission is not added separately under this method.', 'c4', T4, check=500),
        Q('m8', 'For a pure agent, which is NOT a condition?', ['The agent must charge a mark-up on the expense', 'Contract authorising the agent to pay', 'Agent does not use the supply himself', 'Exact amount recovered and shown separately'], 0,
          'A pure agent recovers only the actual amount — no mark-up. In practice: his own fee for the service is still taxable.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Inclusions identified', 2, 'concept', 'incidental|tax other'), S('s2', 'Discount excluded', 1, 'concept', 'discount'),
           S('s3', 'Value', 1, 'computation', 'value', nums=[val]), S('s4', 'GST', 1, 'computation', '18%', nums=[tax])],
          ['Give the clause for each item.'], ['Adding GST to the value.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Rule 28 option', 2, 'computation', '90%', nums=[r28]), S('s2', 'Rule 27', 2, 'computation', 'money', nums=[r27])],
          ['Name the rule.'], ['Using cost plus 10% first.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Who are related persons for valuation?', 'Persons such as directors or officers of each other\'s businesses, partners, employer and employee, those under common control, holders of 25% or more voting shares in each other, and family members.',
          [P('p1', 'Common examples', 5, 'partner|employer|director'), P('p2', '25%', 5, '25%')], 'c1'),
        V('v2', 'When is a post-supply discount excluded?', 'When a credit note is issued under section 34 and the recipient reverses the related ITC; earlier law also needed a prior agreement linked to invoices.',
          [P('p1', 'Credit note', 5, 'credit note'), P('p2', 'ITC reversal', 5, 'revers')], 'c2'),
        V('v3', 'What is the order of rules for non-monetary consideration?', 'Open market value, then money plus monetary value of the non-money part, then like kind and quality, then cost plus 10% or the residual method.',
          [P('p1', 'Open market value first', 5, 'open market'), P('p2', 'Later steps', 5, 'like kind|cost|residual')], 'c3'),
        V('v4', 'How does a second-hand goods dealer value supplies?', 'Where no ITC is taken on purchase, value is the difference between selling and purchase price, and a negative margin is ignored.',
          [P('p1', 'Margin', 6, 'difference|margin'), P('p2', 'Negative margin ignored', 4, 'ignored|negative')], 'c4'),
        V('v5', 'Is late payment interest part of value?', 'Yes, interest, late fee or penalty for delayed payment is included under section 15(2)(d) and taxed when received.',
          [P('p1', 'Included', 6, 'include'), P('p2', 'Clause', 4, '15(2)|received')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Orion Logistics', 'difficulty': 'moderate',
              'case': 'Orion Logistics, a customs broker, bills a client: service fee ₹50,000; customs duty paid on the client\'s behalf ₹2,00,000 (exact, shown separately, paid in the client\'s name); its own office expenses ₹10,000 recovered as "reimbursement"; and interest of ₹3,000 for the client\'s delay.',
              'mcqs': [
                  M('k1a', 'Customs duty recovered is:', ['Excluded as pure agent expense', 'Included in value', 'Taxed at 5%', 'Exempt'], 0,
                    'It meets the pure-agent tests: paid in the client\'s name, exact amount, shown separately, not used by Orion. In practice: keep the challan in the client\'s name.', 'core', topic=T4),
                  M('k1b', 'Office expenses "reimbursed" are:', ['Included in value', 'Excluded', 'Not a supply', 'Exempt'], 0,
                    'These are Orion\'s own costs, not incurred as agent of the client, so they form part of the consideration. In practice: label does not decide treatment.', 'core', topic=T4),
                  M('k1c', 'Value of supply for GST:', ['₹63,000', '₹60,000', '₹2,63,000', '₹50,000'], 0,
                    'Fee 50,000 + office expenses 10,000 + interest 3,000 = 63,000; customs duty is excluded. In practice: interest is taxed when received.', 'moderate', check=63000, topic=T2),
                  M('k1d', 'GST at 18% on that value:', ['₹11,340', '₹10,800', '₹47,340', '₹9,000'], 0,
                    '18% of ₹63,000 = ₹11,340. In practice: charge IGST or CGST+SGST by place of supply.', 'core', check=11340, topic=T2),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch07', 1, 'Value of Supply',
                ['Determine transaction value and the related-person test.',
                 'Apply inclusions and discount rules.',
                 'Apply the Valuation Rules, special methods and pure agent rule.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 40}, 'prereq': ['int-p3-b-ch06-u01'],
                 'exam_tip': 'Present value questions as a table with "include/exclude" and the clause for every item.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Transaction value: unrelated parties, price sole consideration.',
                             'Include: other taxes, supplier\'s liabilities paid by buyer, incidentals, interest, non-Govt subsidies.',
                             'Exclude: GST; invoice discounts; post-supply discounts with credit note and ITC reversal.',
                             'Rules 27–31 ladder; Rule 32 special cases; Rule 33 pure agent.'],
                 'remember': ['Rule 28: invoice value accepted if recipient gets full ITC.', 'Air travel agent: 5% domestic, 10% international.'],
                 'traps': ['Government subsidies excluded; private ones included.', 'Pure agent cannot add a mark-up.']},
                [('Rule 28/29 option', '90% of resale price'), ('Rule 30', 'Cost + 10%'), ('Air agent', '5% / 10% of basic fare'), ('Related person', '25% voting shares')],
                viva, cases)
