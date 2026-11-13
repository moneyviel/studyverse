"""CA Final · Paper 4 · Chapter 5 Income from Other Sources.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch05-u01'
T1 = 'Scope of the residuary head and dividends'
T2 = 'Gifts and inadequate consideration'
T3 = 'Casual income and online games'
T4 = 'Deductions allowed and disallowed'


def build():
    ck = Checks()
    g1 = ck.add('60000', 'Cash gift from friend (₹)')
    g2 = ck.add('800000-700000', 'Land: SDV minus consideration (₹)')
    tot = ck.add('60000+(800000-700000)', 'Taxable under section 92(2)(m) (₹)')
    i1 = {'id': 'i1', 'title': 'Gifts received by an individual', 'difficulty': 'core', 'minutes': 7,
          'q': 'In T.Y. 2026-27 Ravi receives: (a) ₹60,000 cash from a college friend on his birthday; (b) a plot from a friend for ₹7,00,000 whose stamp duty value is ₹8,00,000; (c) jewellery worth ₹2,00,000 from his father\'s brother. Compute income under section 92(2)(m).',
          'solution': [table(['Item', 'Reason', '₹'], [
              ['(a) Cash', 'Exceeds ₹50,000 from a non-relative — whole sum taxable', inr(g1)],
              ['(b) Plot', 'Shortfall ₹1,00,000 exceeds higher of ₹50,000 and 10% of consideration (₹70,000)', inr(g2)],
              ['(c) Jewellery', 'From a relative — outside the provision', '—'],
              ['Total', '', inr(tot)]], title='Section 92(2)(m)')],
          'checks': list(ck)}

    c2 = Checks()
    ic = c2.add('600000*0.50', 'Interest on enhanced compensation after 50% deduction (₹)')
    fd = c2.add('min(72000/3,25000)', 'Family pension deduction (₹)')
    fp = c2.add('72000-min(72000/3,25000)', 'Taxable family pension (₹)')
    t2 = c2.add('600000*0.50+72000-min(72000/3,25000)', 'Total income from other sources (₹)')
    i2 = {'id': 'i2', 'title': 'Deductions under section 93', 'difficulty': 'core', 'minutes': 6,
          'q': 'Lata, under the default regime, receives in T.Y. 2026-27 interest of ₹6,00,000 on enhanced compensation for land acquired by the State, covering three earlier years, and family pension of ₹72,000. Compute income from other sources.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Interest on compensation', 'Taxed on receipt less 50%', inr(ic)],
              ['Family pension deduction', 'Lower of one-third and ₹25,000', inr(fd)],
              ['Family pension taxable', '72,000 − deduction', inr(fp)],
              ['Total', '', inr(t2)]], title='Section 93')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 92 charges income not falling under any other head. Section 92(2) lists specific items: dividends; casual income such as lotteries and puzzles; employee PF recoveries; interest on securities; hiring of plant with buildings where inseparable; keyman insurance sums; interest on compensation; gifts; and others. Income is computed under the accounting method regularly employed, with ICDS under section 276.',
            'Dividend includes deemed dividends under section 2(40): distributions releasing company assets, debentures or bonus preference shares to the extent of accumulated profits, distributions on liquidation or capital reduction, and loans by a closely held company to a shareholder holding at least 10% voting power, to a concern in which he has at least 20% interest, or for his benefit — each limited to accumulated profits.',
            'Dividends are taxed in the shareholder\'s hands; no deduction is allowed for expenses (including interest) against dividends or mutual fund units.'],
          'The residuary head catches what the others miss.',
          'A closely held company lending ₹5 lakh to a 15% shareholder with reserves of ₹6 lakh creates a deemed dividend of ₹5 lakh.'),
        C('c2', T2, [
            'Section 92(2)(m) taxes money or property received without or for inadequate consideration. Money: whole amount if aggregate exceeds ₹50,000 in the year. Immovable property: stamp duty value without consideration, or the shortfall where it exceeds the higher of ₹50,000 and 10% of consideration (stamp value on agreement date if part paid other than in cash earlier).',
            'Specified movable property (shares, jewellery, art, bullion, etc.): FMV if received free and aggregate exceeds ₹50,000; for inadequate consideration, the shortfall if it exceeds ₹50,000.',
            'Exclusions: receipts from relatives, on marriage, by will or inheritance, in contemplation of death, from local authorities, from registered non-profit organisations (subject to conditions), under specified non-transfer transactions, and by a trust solely for relatives. Cost of the asset for later capital gains is the value taxed.'],
          'Free money above ₹50,000 from non-relatives is income.',
          'A plot worth ₹8 lakh bought for ₹7 lakh from a friend gives ₹1 lakh of income.'),
        C('c3', T3, [
            'Winnings from lotteries, crossword puzzles, races, card games, gambling and betting are taxed at a flat 30% under section 194 (plus surcharge and cess), whatever head they fall under.',
            'No expenses, Chapter VIII deductions or basic-exemption adjustment are allowed against such winnings; a lottery distributor\'s prize on unsold tickets is still taxed at the flat rate.',
            'Net winnings from online games are separately taxed at 30% under section 194, with TDS on net winnings.'],
          'Winnings bear a flat 30% with no relief.',
          'A ₹5 lakh lottery prize bears tax of ₹1.5 lakh before cess even with no other income.'),
        C('c4', T4, [
            'Section 93 allows: banker\'s commission for collecting interest on securities; employee contributions remitted by the return due date; repairs, taxes, insurance and depreciation for hired plant and buildings; family pension deduction of the lower of one-third and ₹25,000 (default regime) or ₹15,000 (optional regime); 50% of interest on compensation (nothing else); and other revenue expenditure wholly and exclusively for earning the income.',
            'Section 94 disallows: personal expenses; interest or salary payable outside India without TDS; excessive payments to related persons; payments above ₹10,000 (₹35,000 for transporters) a day otherwise than through specified modes; 30% of sums payable to residents where TDS defaults; expenses against casual income (except owners of race horses).',
            'Section 95 deems recoveries of earlier allowed expenses or liabilities as income in the year received.'],
          'Deduct only what is permitted, never against dividends or winnings.',
          'Interest on enhanced compensation of ₹6 lakh is taxed at ₹3 lakh.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Gift documentation review', 'role': 'Tax associate',
             'situation': 'A client received several gifts and a discounted property during the year.',
             'steps': ['Identify relatives under the definition.', 'Compare stamp value and consideration.', 'Aggregate money and movable gifts.', 'Record cost for future capital gains.'],
             'takeaway': 'Relationship and value tests decide taxability.'}]

    mcqs = [
        Q('m1', 'A loan by a closely held company is deemed dividend if the shareholder holds at least:', ['Ten percent voting power', 'Twenty percent voting power', 'Five percent voting power', 'Fifty percent voting power'], 0,
          'Section 2(40)(e). In practice: limited to accumulated profits.', 'c1', T1),
        Q('m2', 'Interest expense against dividend income is:', ['Not deductible', 'Deductible up to twenty percent', 'Fully deductible', 'Deductible if shares are listed'], 0,
          'No deduction against dividends. In practice: plan borrowings.', 'c1', T1),
        Q('m3', 'Cash gifts from a non-relative totalling ₹48,000 in the year are:', ['Not taxable', 'Fully taxable', 'Taxable above ₹25,000', 'Taxable at thirty percent'], 0,
          'Must exceed ₹50,000. In practice: aggregate test.', 'c2', T2),
        Q('m4', 'Shortfall on purchase of land is taxable when it exceeds:', ['The higher of ₹50,000 and ten percent of consideration', '₹50,000 only', 'Five percent of consideration', '₹1 lakh'], 0,
          'Tolerance band. In practice: per property.', 'c2', T2),
        Q('m5', 'Gifts on the occasion of an individual\'s marriage are:', ['Outside the gift provision', 'Taxable above ₹50,000', 'Taxable at thirty percent', 'Taxable as salary'], 0,
          'Specific exclusion. In practice: keep evidence.', 'c2', T2),
        Q('m6', 'Lottery winnings are taxed at:', ['Thirty percent flat', 'Slab rates', 'Twenty percent', 'Twelve and a half percent'], 0,
          'Section 194. In practice: TDS by payer.', 'c3', T3),
        Q('m7', 'Under the default regime, family pension deduction is the lower of one-third and:', ['Twenty-five thousand rupees', 'Fifteen thousand rupees', 'Fifty thousand rupees', 'Seventy-five thousand rupees'], 0,
          'Section 93. In practice: optional regime ₹15,000.', 'c4', T4),
        Q('m8', 'Interest on enhanced compensation is taxed:', ['In the year of receipt, less fifty percent', 'Year-wise when it accrued', 'As capital gains', 'Fully exempt'], 0,
          'Section 92(2)(i). In practice: no other deduction.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Cash and jewellery', 3, 'analysis', 'relative', nums=[g1]), S('s2', 'Immovable property', 3, 'computation', 'stamp duty', nums=[g2, tot])],
          ['Give reasons.'], ['Taxing only the excess over ₹50,000.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Compensation interest', 2.5, 'computation', 'compensation', nums=[ic]), S('s2', 'Family pension', 2.5, 'computation', 'pension', nums=[fp, t2])],
          ['Mention year of taxability.'], ['Spreading interest over earlier years.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is the treatment of money received without consideration from a friend?', 'The whole amount is income from other sources if the aggregate in the year exceeds ₹50,000.',
          [P('p1', 'Whole amount', 5, 'whole'), P('p2', 'Fifty thousand', 5, '50,000')], 'c2'),
        V('v2', 'Can basic exemption limit be adjusted against lottery winnings?', 'The adjustment is barred; winnings bear a flat 30% with no deductions.',
          [P('p1', 'Barred', 5, 'barred'), P('p2', 'Thirty percent', 5, '30%')], 'c3'),
        V('v3', 'Which loans by a closely held company are deemed dividend?', 'Loans to a shareholder with at least 10% voting power, to a concern in which he has substantial interest, or for his benefit, to the extent of accumulated profits.',
          [P('p1', 'Ten percent', 5, '10%'), P('p2', 'Accumulated profits', 5, 'accumulated')], 'c1'),
        V('v4', 'What deduction is allowed for interest on compensation?', 'Fifty percent of the interest, with no other deduction.',
          [P('p1', 'Fifty percent', 5, '50%|fifty'), P('p2', 'Only deduction', 5, 'no other|only')], 'c4'),
        V('v5', 'What does section 95 provide?', 'Amounts later recovered for expenses or liabilities earlier allowed are deemed income in the year of receipt.',
          [P('p1', 'Recovered', 5, 'recover'), P('p2', 'Deemed income', 5, 'deemed')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Sameer\'s windfall', 'difficulty': 'core',
              'case': 'Sameer, a resident student with no other income, wins ₹5,00,000 in a state lottery in T.Y. 2026-27. He spent ₹2,000 on tickets.',
              'mcqs': [
                  M('k1a', 'Taxable lottery income (₹):', ['5,00,000', '4,98,000', '1,00,000', 'Nil'], 0,
                    'No expenses allowed. In practice: gross winnings.', 'core', check=500000, topic=T3),
                  M('k1b', 'Tax before cess (₹):', ['1,50,000', '5,000', '25,000', 'Nil'], 0,
                    '30% flat. In practice: no slab benefit.', 'core', check=150000, topic=T3),
                  M('k1c', 'Tax including 4% cess (₹):', ['1,56,000', '1,50,000', '1,62,000', '1,55,000'], 0,
                    '1,50,000 × 1.04. In practice: TDS adjusted.', 'core', check=156000, topic=T3),
                  M('k1d', 'Can Sameer claim the section 156 rebate?', ['Not against such winnings', 'Yes fully', 'Yes, half', 'Only if he is a senior citizen'], 0,
                    'Special-rate income. In practice: plan advance tax.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch05', 1, 'Income from Other Sources',
                ['Identify income under the residuary head including deemed dividends.',
                 'Apply the gift provisions.',
                 'Tax casual income and online game winnings.',
                 'Apply allowable and disallowed deductions.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 30}, 'prereq': ['fin-p4-ch04-u01'],
                 'exam_tip': 'For gifts, test relative status first, then the threshold for the asset type.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 92 charge; deemed dividend section 2(40).', 'Gifts section 92(2)(m).', 'Winnings 30% under section 194.',
                             'Section 93 deductions; section 94 disallowances.'],
                 'remember': ['Interest on compensation: 50% deduction.'],
                 'traps': ['Allowing interest against dividends.']},
                [('Charge', 'Section 92'), ('Deductions', 'Section 93'), ('Disallowances', 'Section 94'), ('Winnings rate', 'Section 194')],
                viva, cases)
