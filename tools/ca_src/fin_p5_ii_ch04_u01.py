"""CA Final · Paper 5 · Part II Customs · Chapter 4 Valuation under the Customs Act, 1962.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ii-ch04-u01'
T1 = 'Section 14: transaction value, exchange rate and tariff value'
T2 = 'Import valuation rules: methods in sequence'
T3 = 'Additions under rule 10 and freight and insurance'
T4 = 'Rejection of declared value and export valuation'


def build():
    ck = Checks()
    fob = ck.add('10000+500+300', 'Price plus buyer-supplied design and royalty — adjusted FOB (US$)')
    fr = ck.add('(10000+500+300)*0.20', 'Freight at 20% of FOB when not ascertainable (US$)')
    ins = ck.add('(10000+500+300)*0.01125', 'Insurance at 1.125% of FOB when not ascertainable (US$)')
    cif = ck.add('(10000+500+300)*1.21125', 'CIF value (US$)')
    av = ck.add('(10000+500+300)*1.21125*84', 'Assessable value at CBIC rate ₹84 (₹)')
    i1 = {'id': 'i1', 'title': 'Assessable value of imported machinery', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Teesta Machines imports a machine at a price of US$10,000 FOB. The buyer separately paid: US$500 for design work done abroad and supplied free to the seller; US$300 royalty payable as a condition of sale; US$200 buying commission to its own agent. Freight and insurance are not known. The CBIC exchange rate on the date of filing the bill of entry is ₹84 per US$ (RBI rate ₹83.6). Compute the assessable value.',
          'solution': [table(['Item', 'Working', 'Amount'], [
              ['Price', 'FOB', 'US$10,000'],
              ['Add: design work abroad', 'Rule 10(1)(b)(iv)', 'US$500'],
              ['Add: royalty, condition of sale', 'Rule 10(1)(c)', 'US$300'],
              ['Buying commission', 'Excluded by rule 10(1)(a)(i)', 'Nil'],
              ['Adjusted FOB', '', f'US${inr(fob)}'],
              ['Freight', '20% of FOB', f'US${fr:,.2f}'],
              ['Insurance', '1.125% of FOB', f'US${ins:,.2f}'],
              ['CIF', '', f'US${cif:,.2f}'],
              ['Assessable value', 'CIF × ₹84 (CBIC rate)', f'₹{inr(av)}']], title='Section 14 and rule 10')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Are the parties related?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Decide whether the following are related under rule 2(2): (a) Kaveri Ltd. holds 6% voting shares in both the Indian importer and the foreign supplier; (b) the importer is sole distributor of the supplier but has no other link; (c) the supplier\'s director is the importer\'s director.',
          'solution': [table(['Case', 'Test', 'Related?'], [
              ['(a)', 'A person holds 5% or more of voting stock of both', 'Yes'],
              ['(b)', 'Sole distributor is related only if a rule 2(2) criterion is met', 'No'],
              ['(c)', 'Officers or directors of one another\'s businesses', 'Yes']], title='Rule 2(2)')]}

    concepts = [
        C('c1', T1, [
            'Section 14(1): the value of imported and export goods is the transaction value — the price actually paid or payable for delivery at the time and place of importation (or exportation), where buyer and seller are unrelated and price is the sole consideration, subject to rules. It includes amounts paid for costs and services such as commissions, assists, royalties, licence fees, freight, insurance, loading, unloading and handling to the extent set by rules.',
            'Conversion uses the exchange rate notified by CBIC (not RBI or FEDAI) on the date of filing the bill of entry for imports, and of the shipping bill or bill of export for exports. Rates are published through ICEGATE and revised twice a month.',
            'Section 14(2) lets the Board fix tariff values for classes of goods (e.g. edible oils, gold) considering value trends; duty is then charged on the tariff value regardless of the transaction value.'],
          'Price actually paid, adjusted, converted at the CBIC rate.',
          'A contract price holds even if world prices rise before import.'),
        C('c2', T2, [
            'Rule 3: value is the transaction value adjusted under rule 10, provided there are no restrictions on use (other than legal or geographical ones not affecting value), no unquantifiable conditions, no undisclosed proceeds to the seller, and the parties are unrelated or the relationship did not influence price (tested by circumstances of sale or test values).',
            'If not, methods apply in order: rule 4 identical goods, rule 5 similar goods (both imported at or about the same time, using the lowest value if several), rule 7 deductive value (resale price in India less profit, transport, duties), rule 8 computed value (cost plus profit plus rule 10(2) costs), and rule 9 residual method. On the importer\'s request, rule 8 may be applied before rule 7 (rule 6).',
            'Rule 9 forbids values based on Indian selling prices of Indian goods, the higher of two alternatives, exporting-country domestic prices, export prices to other countries, minimum or arbitrary values. Related persons under rule 2(2) include directors of each other, partners, employer-employee, a common 5% voting holder, control relationships and family members.'],
          'Six methods, strictly in sequence.',
          'If no identical goods data exist, look at similar goods before going to deductive value.'),
        C('c3', T3, [
            'Rule 10(1) adds, if borne by the buyer and not in the price: commissions and brokerage except buying commission; containers treated as one with the goods; packing; assists (materials, tools, dies, moulds, consumables and design or engineering done outside India) supplied free or cheaply; royalties and licence fees related to the goods payable as a condition of sale; resale proceeds accruing to the seller; and other payments made as a condition of sale. Post-import processes paid as a condition of sale are also added.',
            'Rule 10(2) adds transport, loading, unloading and handling to the place of importation and insurance. If transport cost is unknown, it is 20% of FOB; if insurance is unknown, 1.125% of FOB. For air imports, transport cannot exceed 20% of FOB. Transshipment costs within India are excluded; demurrage on chartered vessels, lighterage and barge charges are included.',
            'Assessable value = adjusted FOB + freight + insurance, converted at the CBIC rate.'],
          'Add what the buyer pays to get the goods; exclude buying commission.',
          'Moulds sent free to an overseas supplier add their value to the imported goods.'),
        C('c4', T4, [
            'Rule 12 lets the proper officer doubt a declared value — e.g. much higher contemporaneous values, abnormal discounts, exclusive-agent discounts, misdeclaration of quality or origin, undisclosed brand or specification, or manipulated documents — ask for evidence, and on persisting doubt treat the transaction value as undeterminable. On request he must give written grounds and a hearing. The rule only allows rejection; value is then fixed under rules 4 to 9.',
            'Rule 11 requires the importer to declare full and accurate value details, and the manufacturer\'s invoice where goods are bought through an intermediary. Wrong declarations attract confiscation, penalty and prosecution.',
            'Export valuation rules: transaction value (accepted even between related persons if price is unaffected); else comparison with like goods exported at about the same time, computed value (cost, design or brand charges and profit), and residual method, in order. The local market price cannot be the sole basis, and rule 8 mirrors the rejection mechanism.'],
          'Doubt must be reasoned; rejection is not a valuation method.',
          'An unexplained 40% discount to one buyer may justify enquiry.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Valuation review before filing', 'role': 'Customs compliance officer',
             'situation': 'An import involves royalty and tooling paid by the buyer.',
             'steps': ['Identify rule 10 additions.', 'Exclude buying commission.', 'Use actual or deemed freight and insurance.', 'Convert at the CBIC rate on the bill of entry date.'],
             'takeaway': 'Missed assists are a common cause of short levy.'}]

    mcqs = [
        Q('m1', 'Exchange rate for valuing imports is the rate notified by:', ['CBIC on the bill of entry filing date', 'RBI on invoice date', 'FEDAI on payment date', 'SBI on arrival date'], 0,
          'Section 14 proviso. In practice: ICEGATE.', 'c1', T1),
        Q('m2', 'If freight is not ascertainable, it is taken as:', ['Twenty percent of FOB', 'Ten percent of FOB', 'One point one two five percent of FOB', 'Fifteen percent of CIF'], 0,
          'Rule 10(2). In practice: air cap also 20%.', 'c3', T3),
        Q('m3', 'Which is not added to the transaction value?', ['Buying commission', 'Selling commission paid by buyer', 'Packing cost', 'Royalty as a condition of sale'], 0,
          'Rule 10(1)(a)(i). In practice: own agent.', 'c3', T3),
        Q('m4', 'After transaction value fails, the next method is:', ['Identical goods', 'Deductive value', 'Computed value', 'Residual method'], 0,
          'Rule 4. In practice: sequential.', 'c2', T2),
        Q('m5', 'Rule 8 can be applied before rule 7 when:', ['The importer requests it', 'The officer decides', 'Goods are exported', 'Goods are tariff-valued'], 0,
          'Rule 6. In practice: rarely chosen.', 'c2', T2),
        Q('m6', 'Persons are related when one holds at least what share of voting stock in both?', ['Five percent', 'Twenty-six percent', 'Fifty-one percent', 'Ten percent'], 0,
          'Rule 2(2)(iv). In practice: direct or indirect.', 'c2', T2),
        Q('m7', 'Rule 12 of the import valuation rules:', ['Provides a mechanism to reject declared value', 'Is a valuation method', 'Fixes tariff values', 'Applies only to exports'], 0,
          'Explanation to rule 12. In practice: then rules 4–9.', 'c4', T4),
        Q('m8', 'Export goods valuation after transaction value starts with:', ['Comparison with like goods', 'Computed value', 'Residual method', 'Deductive value'], 0,
          'Export rule 4. In practice: same destination.', 'c4', T4),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Additions and exclusions', 3, 'analysis', 'royalty', nums=[fob]), S('s2', 'Freight and insurance', 3, 'computation', '20%', nums=[fr, ins, cif]), S('s3', 'Conversion', 2, 'computation', 'CBIC', nums=[av])],
          ['Show deemed rates.'], ['Adding buying commission; using RBI rate.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Shareholding', 2, 'analysis', '5%'), S('s2', 'Sole distributor and directors', 2, 'analysis', 'sole distributor')],
          ['Quote criteria.'], ['Treating sole agency as automatically related.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Does a price rise after contract change the value?', 'The contract price actually paid remains the transaction value, unless legally unacceptable.',
          [P('p1', 'Contract price', 5, 'contract price'), P('p2', 'Actually paid', 5, 'actually paid')], 'c1'),
        V('v2', 'What is a tariff value?', 'A value fixed by the Board for a class of goods on which duty is charged instead of transaction value.',
          [P('p1', 'Board', 5, 'board'), P('p2', 'Class of goods', 5, 'class')], 'c1'),
        V('v3', 'Which costs are excluded for transshipment within India?', 'Insurance, transport, loading, unloading and handling linked to transshipment to another Indian customs station.',
          [P('p1', 'Transshipment', 5, 'transshipment'), P('p2', 'Customs station', 5, 'customs station')], 'c3'),
        V('v4', 'Name two grounds for doubting declared value.', 'Abnormal discount from competitive price, and significantly higher contemporaneous values of identical goods.',
          [P('p1', 'Abnormal discount', 5, 'abnormal discount'), P('p2', 'Contemporaneous', 5, 'contemporaneous')], 'c4'),
        V('v5', 'What does computed value for imports include?', 'Cost of materials and fabrication, profit and general expenses of the exporting country, and the rule 10(2) costs.',
          [P('p1', 'Cost', 5, 'cost'), P('p2', 'Profit', 5, 'profit')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Air consignment with known freight', 'difficulty': 'moderate',
              'case': 'Goods worth US$5,000 FOB are imported by air. Actual air freight is US$1,400 and insurance is unknown.',
              'mcqs': [
                  M('k1a', 'Freight to be included (US$):', ['1,000', '1,400', '700', '1,200'], 0,
                    'Capped at 20% of FOB for air. In practice: 5,000 × 20%.', 'moderate', check=1000, topic=T3),
                  M('k1b', 'Insurance to be included (US$):', ['56.25', '50', '100', '0'], 0,
                    '1.125% of FOB. In practice: deemed.', 'moderate', check=56.25, topic=T3),
                  M('k1c', 'CIF value (US$):', ['6,056.25', '6,456.25', '6,000', '5,056.25'], 0,
                    'Sum of components. In practice: then convert.', 'moderate', check=6056.25, topic=T3),
                  M('k1d', 'Exchange rate applied is that on:', ['Date of filing the bill of entry', 'Date of shipment', 'Date of payment', 'Date of invoice'], 0,
                    'Section 14. In practice: CBIC rate.', 'moderate', topic=T1),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ii-ch04', 1, 'Valuation under the Customs Act, 1962',
                ['Apply section 14, exchange rate rules and tariff values.',
                 'Apply import valuation methods in sequence.',
                 'Compute assessable value with rule 10 additions.',
                 'Apply rejection of declared value and export valuation rules.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 30}, 'prereq': ['fin-p5-ii-ch03-u01'],
                 'exam_tip': 'Build the FOB with additions first, then apply deemed freight and insurance, then convert at the CBIC rate.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Transaction value under section 14.', 'CBIC exchange rate on BoE or shipping bill date.', 'Rules 4, 5, 7, 8, 9 in sequence; 8 before 7 on request.',
                             'Rule 10 additions; buying commission excluded.', 'Deemed freight 20%, insurance 1.125%.'],
                 'remember': ['Rule 12 is rejection, not valuation.'],
                 'traps': ['Using RBI rate instead of CBIC rate.']},
                [('Value', 'Section 14'), ('Transaction value', 'Rule 3'), ('Identical/similar', 'Rules 4–5'), ('Additions', 'Rule 10'), ('Rejection', 'Rule 12')],
                viva, cases)
