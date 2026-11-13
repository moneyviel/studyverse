"""CA Final · Paper 5 · Chapter 6 Value of Supply.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch06-u01'
T1 = 'Transaction value and inclusions'
T2 = 'Discounts'
T3 = 'Valuation rules for related, distinct and agent supplies'
T4 = 'Special valuation rules'


def build():
    ck = Checks()
    v = ck.add('100000-5000+2000+3000+500+1500', 'Taxable value (₹)')
    g = ck.add('(100000-5000+2000+3000+500+1500)*0.18', 'GST at 18% (₹)')
    i1 = {'id': 'i1', 'title': 'Building up transaction value', 'difficulty': 'core', 'minutes': 8,
          'q': 'Kaveri Pumps sells a pump: list price ₹1,00,000 less 5% discount shown on the invoice; packing ₹2,000 and freight to the buyer\'s site ₹3,000 charged separately; a local cess of ₹500 (not GST); the buyer pays ₹1,500 directly to a testing agency on Kaveri\'s behalf; a Central Government subsidy of ₹4,000 is received by Kaveri. Compute the value and GST at 18%.',
          'solution': [table(['Item', 'Treatment', '₹'], [
              ['Price after invoice discount', '1,00,000 − 5,000', '95,000'],
              ['Packing and freight', 'Incidental — included', '5,000'],
              ['Local cess', 'Non-GST taxes — included', '500'],
              ['Supplier\'s liability paid by buyer', 'Included', '1,500'],
              ['Government subsidy', 'Excluded (only non-government price-linked subsidies included)', '—'],
              ['Taxable value', '', inr(v)],
              ['GST @18%', '', inr(g)]], title='Section 15')],
          'checks': list(ck)}

    c2 = Checks()
    n = c2.add('60000*0.90', 'Value at 90% of price to unrelated customer (₹)')
    cg = c2.add('100000000*0.01', 'Value of corporate guarantee at 1% per annum (₹)')
    i2 = {'id': 'i2', 'title': 'Distinct and related person supplies', 'difficulty': 'moderate', 'minutes': 7,
          'q': '(a) Arpit Ltd transfers goods from its Delhi unit to its Haryana unit for resale; the Haryana unit sells them to unrelated customers for ₹60,000. Compute value at the supplier\'s option. (b) A parent company gives a corporate guarantee of ₹10 crore to a bank for its Indian subsidiary without charging any fee. Compute value. (c) What if the Haryana unit is eligible for full ITC?',
          'solution': [table(['Case', 'Rule', '₹'], [
              ['(a)', '90% of price charged by recipient to unrelated customer', inr(n)],
              ['(b)', 'Higher of 1% of guarantee per annum and actual consideration', inr(cg)],
              ['(c)', 'Invoice value deemed open market value', 'As invoiced']], title='Rule 28')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 15(1): the value of supply is the transaction value — the price actually paid or payable — where supplier and recipient are unrelated and price is the sole consideration. Related persons include officers or directors of each other\'s business, partners, employer–employee, holders of 25% or more voting shares, persons controlling or controlled by each other, and family members.',
            'Section 15(2) adds: taxes, duties, cesses, fees and charges other than GST and compensation cess; amounts the supplier is liable to pay but which the recipient pays and which are not in the price; incidental expenses like commission and packing charged by the supplier; interest, late fee or penalty for delayed payment; and subsidies linked to price (except government subsidies).',
            'Section 15(4) applies valuation rules when the transaction value cannot be used; section 15(5) lets the Government notify supplies valued only by rules (e.g. specified actionable claims).'],
          'Start with the price; add what the buyer pays for the supply.',
          'A municipal cess charged on the invoice forms part of value.'),
        C('c2', T2, [
            'Section 15(3): a discount granted up to the point of supply and shown on the invoice itself is kept out of value.',
            'Post-supply discounts are excluded only if they were agreed before or at the time of supply, linked to specific invoices, and the recipient reverses the corresponding ITC. Otherwise the supplier may give a financial credit note without reducing tax.',
            'The Finance Act 2026 proposes to remove the requirement of a pre-existing agreement for post-supply discounts once notified, retaining the link to ITC reversal by the recipient.'],
          'Discounts reduce value only with proper documentation and ITC reversal.',
          'A year-end volume rebate agreed in the original contract can reduce taxable value via a credit note.'),
        C('c3', T3, [
            'Rule 27: where consideration is not wholly in money, value is the open market value; else consideration in money plus the money equivalent of non-monetary consideration; else value of like kind and quality; else rules 30 or 31.',
            'Rule 28: supplies between distinct or related persons (other than through agents) are valued at open market value, like kind and quality, or rules 30/31 — with the option of 90% of the price charged by the recipient to unrelated customers for goods meant for resale, and the invoice value accepted where the recipient can take full ITC. Corporate guarantees to banks for related persons in India are valued at the higher of 1% of the guarantee per year and actual consideration.',
            'Rule 29 (through agents): open market value or, at the supplier\'s option, 90% of the price charged by the recipient to unrelated customers. Rule 30: 110% of cost of production or acquisition. Rule 31: reasonable means consistent with section 15 (rule 30 may be skipped for services).'],
          'Related-party values follow market benchmarks or cost-plus.',
          'A ₹10 crore guarantee for a subsidiary is valued at ₹10 lakh a year.'),
        C('c4', T4, [
            'Rule 31A, 31B and 31C value specified actionable claims: lottery at face value or price notified (whichever higher); betting, gambling and horse racing at full face value of bets; online money gaming and casinos at the amount paid or deposited by the player (excluding refunds of unused amounts).',
            'Rule 31D: value of specified goods such as pan masala and tobacco is the retail sale price less tax.',
            'Rule 32: special rules for purchase or sale of foreign currency (spread-based or slab-based), air travel agents (5% or 10% of basic fare), life insurance (premium less investment portion, or slab percentages), second-hand goods dealers (margin), redemption of vouchers and services by pure agents (excluded from value if conditions met).'],
          'Special sectors have prescribed valuation formulas.',
          'A dealer in used cars may pay GST only on its margin.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Valuation audit', 'role': 'GST consultant',
             'situation': 'A group company supplies goods and guarantees to related entities.',
             'steps': ['Identify related and distinct person supplies.', 'Check full ITC eligibility of recipients.', 'Apply rule 28 corporate guarantee valuation.', 'Review discount credit notes for conditions.'],
             'takeaway': 'Undervaluation in group transactions is a common audit point.'}]

    mcqs = [
        Q('m1', 'Transaction value is accepted when parties are unrelated and:', ['Price is the sole consideration', 'Payment is in cash', 'Supply is intra-State', 'Invoice is issued in time'], 0,
          'Section 15(1). In practice: test both.', 'c1', T1),
        Q('m2', 'Persons are related if one holds voting shares of the other of at least:', ['Twenty-five percent', 'Ten percent', 'Fifty-one percent', 'Twenty percent'], 0,
          'Explanation to section 15. In practice: directly or indirectly.', 'c1', T1),
        Q('m3', 'Which is excluded from value?', ['Subsidy from the Central Government', 'Packing charges', 'Interest for late payment', 'Local cess'], 0,
          'Section 15(2)(e). In practice: private subsidies included.', 'c1', T1),
        Q('m4', 'A post-supply discount reduces value only if agreed earlier, linked to invoices, and:', ['The recipient reverses ITC', 'It is paid in cash', 'It is below 10%', 'It is approved by the officer'], 0,
          'Section 15(3)(b). In practice: FA 2026 amendment pending.', 'c2', T2),
        Q('m5', 'Rule 28 option for goods meant for resale is value at:', ['Ninety percent of price to unrelated customers', 'One hundred ten percent of cost', 'Invoice value always', 'Fifty percent of MRP'], 0,
          'Supplier option. In practice: or invoice value with full ITC.', 'c3', T3),
        Q('m6', 'Cost-based valuation under rule 30 is at:', ['One hundred ten percent of cost', 'Cost only', 'Ninety percent of cost', 'Cost plus 5%'], 0,
          'Rule 30. In practice: then rule 31.', 'c3', T3),
        Q('m7', 'Corporate guarantee to a related person is valued at the higher of actual consideration and:', ['One percent of guarantee per annum', 'Two percent', 'Half percent', 'Nil'], 0,
          'Rule 28(2). In practice: not for exports.', 'c3', T3),
        Q('m8', 'Value for a dealer in second-hand goods under the margin scheme is:', ['Selling price less purchase price', 'Full selling price', 'Purchase price', 'One hundred ten percent of cost'], 0,
          'Rule 32(5). In practice: no ITC on purchase.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Inclusions', 3, 'analysis', 'included'), S('s2', 'Value and GST', 3, 'computation', 'value', nums=[v, g])],
          ['Give reason for each item.'], ['Including government subsidy.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Distinct person transfer', 2, 'computation', '90%', nums=[n]), S('s2', 'Corporate guarantee', 3, 'computation', '1%', nums=[cg])],
          ['Cite rule 28.'], ['Ignoring full ITC proviso.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Are interest and late fees part of value?', 'Yes, interest, late fee or penalty for delayed payment of consideration are included.',
          [P('p1', 'Included', 5, 'included'), P('p2', 'Delayed payment', 5, 'delayed')], 'c1'),
        V('v2', 'What is open market value?', 'The full value in money, excluding GST, that an unrelated buyer would pay at the same time for the same supply when price is the sole consideration.',
          [P('p1', 'Unrelated', 5, 'unrelated'), P('p2', 'Sole consideration', 5, 'sole consideration')], 'c3'),
        V('v3', 'When is rule 31 used directly for services?', 'For services the supplier may skip rule 30 and use reasonable means under rule 31.',
          [P('p1', 'Skip rule 30', 5, 'skip'), P('p2', 'Reasonable means', 5, 'reasonable')], 'c3'),
        V('v4', 'How is a lottery ticket valued?', 'At face value or the price notified by the organising State, whichever is higher.',
          [P('p1', 'Face value', 5, 'face value'), P('p2', 'Whichever higher', 5, 'higher')], 'c4'),
        V('v5', 'What is a financial credit note?', 'A credit note for discount that does not reduce the supplier\'s tax because section 15(3) conditions are unmet.',
          [P('p1', 'Discount', 5, 'discount'), P('p2', 'Conditions unmet', 5, 'unmet')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Trident Motors (used cars)', 'difficulty': 'core',
              'case': 'Trident Motors, a dealer in used cars availing no ITC, buys a car for ₹6,00,000 and sells it for ₹6,80,000. Assume GST at 18% on the margin.',
              'mcqs': [
                  M('k1a', 'Taxable value under the margin scheme (₹):', ['80,000', '6,80,000', '6,00,000', '1,22,400'], 0,
                    'Selling price − purchase price. In practice: rule 32(5).', 'core', check=80000, topic=T4),
                  M('k1b', 'GST payable (₹):', ['14,400', '1,22,400', '1,08,000', '8,000'], 0,
                    '18% × 80,000. In practice: if margin negative, no tax.', 'core', check=14400, topic=T4),
                  M('k1c', 'If the car were sold at ₹5,80,000, GST would be:', ['Nil', '₹3,600', '₹1,04,400', '₹18,000'], 0,
                    'Negative margin ignored. In practice: no refund.', 'core', topic=T4),
                  M('k1d', 'A condition for the margin scheme is that the dealer:', ['Has not availed ITC on purchase', 'Is a composition dealer', 'Sells only inter-State', 'Is a manufacturer'], 0,
                    'Rule 32(5). In practice: minor processing allowed.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch06', 1, 'Value of Supply',
                ['Determine transaction value and inclusions.',
                 'Apply discount rules.',
                 'Apply valuation rules for related, distinct and agent supplies.',
                 'Apply special valuation rules.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 30}, 'prereq': ['fin-p5-ch05-u01'],
                 'exam_tip': 'Present a value computation table with a reason for each addition or exclusion.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 15(1) transaction value; related persons.', 'Section 15(2) inclusions; government subsidies excluded.', 'Section 15(3) discounts; FA 2026 change pending.',
                             'Rules 27–31: OMV, 90%, 110%, residual.', 'Rule 28(2) corporate guarantee 1%; rule 32 special cases.'],
                 'remember': ['Full-ITC recipient: invoice value accepted.'],
                 'traps': ['Excluding packing and freight charged by supplier.']},
                [('Value', 'Section 15'), ('Related/distinct', 'Rule 28'), ('Cost-based', 'Rule 30'), ('Special cases', 'Rule 32')],
                viva, cases)
