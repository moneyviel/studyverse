"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 5 Unit 3 — AS 13 Accounting for Investments.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch05-u03'
T1 = 'Meaning and classification of investments'
T2 = 'Cost of investments; interest, dividends, bonus and rights'
T3 = 'Carrying amount of current and long-term investments'
T4 = 'Reclassification, disposal and investment property'
T5 = 'Disclosure'


def build():
    ck = Checks()
    paid = ck.add('1000*104', 'Price paid cum-interest (₹)')
    acc = ck.add('1000*100*12/100*4/12', 'Accrued interest for April–July (₹)')
    cost = ck.add('104000-4000', 'Cost of investment (₹)')
    sep = ck.add('1000*100*12/100*6/12', 'Interest received on 30 September (₹)')
    inc = ck.add('6000-4000', 'Interest income for the holding period (₹)')
    i1 = {'id': 'i1', 'title': 'Buying debentures cum-interest', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'On 1 August 2026 Ritu Ltd. bought 1,000 12% debentures of ₹100 each at ₹104 cum-interest. Interest is paid on 31 March and 30 September. Compute the cost of investment and the interest income to 30 September.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Price paid', '1,000 × 104', inr(paid)],
              ['Less: accrued interest (1 April – 31 July)', '1,00,000 × 12% × 4/12', inr(acc)],
              ['Cost of investment', '', inr(cost)],
              ['Interest received on 30 September', '1,00,000 × 12% × 6/12', inr(sep)],
              ['Less: pre-acquisition part (recovery of amount paid)', '', inr(acc)],
              ['Interest income (August–September)', '', inr(inc)]], title='Cum-interest purchase')],
          'checks': list(ck)}

    ck2 = Checks()
    ind = ck2.add('min(50000,42000)+min(30000,38000)+min(20000,19000)', 'Individual basis (₹)')
    cat = ck2.add('min(50000+30000+20000, 42000+38000+19000)', 'Category basis — equity shares as one category (₹)')
    i2 = {'id': 'i2', 'title': 'Valuing current investments', 'difficulty': 'core', 'minutes': 6,
          'q': 'Nidhi Ltd. holds three equity shares as current investments: A (cost ₹50,000, fair value ₹42,000), B (₹30,000, ₹38,000), C (₹20,000, ₹19,000). Value them on an individual basis and on a category basis. Is a "global" basis acceptable?',
          'solution': [table(['Basis', 'Working', '₹'], [
              ['Individual', '42,000 + 30,000 + 19,000', inr(ind)],
              ['Category (all equity shares)', 'Lower of 1,00,000 and 99,000', inr(cat)]], title='Lower of cost and fair value'),
              p('Both individual and category-wise valuation are acceptable under AS 13; the individual basis is more prudent. Valuation on an overall (global) basis across all current investments is not allowed.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Investments are assets kept to earn dividends, interest or rent, to gain in value, or to bring some other advantage to the investing enterprise. Inventories and PPE are not investments.',
            'A current investment can be sold easily and is meant to be kept for a year or less after purchase. All others are long-term investments.',
            'Investment property is land or a building held for rent or capital growth rather than mainly for the investor\'s own occupation or operations.',
            'AS 13 does not deal with interest and dividend recognition (AS 9), operating or finance leases, investments of retirement benefit plans and insurance enterprises, or mutual funds and venture capital funds.'],
          'An investment works for its holder by earning or growing, not by being used in operations.',
          'Treasury bills bought to park surplus cash for three months are a current investment.'),
        C('c2', T2, [
            'Cost includes acquisition charges such as brokerage, fees and duties. If acquired by issuing shares or other securities, cost is the fair value of the securities issued; if in exchange for another asset, the fair value of the asset given up (or of the investment acquired if clearer).',
            'Interest, dividends and rentals that relate to the period before acquisition are deducted from cost, not taken as income. Accrued interest paid on a cum-interest purchase is excluded from cost.',
            'Bonus shares add no cost; the original cost is spread over the larger number of shares.',
            'Rights subscribed add their cost. If rights are sold, the proceeds go to profit and loss; but if shares were bought cum-right and the market value falls ex-right, the sale proceeds may be applied to reduce cost.'],
          'Pay only for what you own; any income that belonged to the earlier period is a refund of price.',
          'Dividend received soon after purchase out of pre-acquisition profits reduces the cost of shares.'),
        C('c3', T3, [
            'Current investments are carried at the lower of cost and fair value, determined either on an individual basis or by category (equity shares, preference shares, debentures and so on), but not on an overall basis.',
            'Long-term investments are carried at cost. A provision is made for a decline in value that is other than temporary, determined for each investment individually; it is reversed when the decline ends or the value recovers.',
            'Indicators of permanent decline include persistent losses of the investee, negative net worth, a market value well below cost for a long time, or adverse changes in its business.'],
          'Current: watch the market; long-term: worry only about lasting falls.',
          'A long-term holding down 5% in a market dip needs no provision; one whose investee has collapsed does.'),
        C('c4', T4, [
            'Long-term investments reclassified as current are transferred at the lower of cost and carrying amount. When a current investment becomes long-term, it moves at its cost or its fair value on that day, whichever is less.',
            'On disposal, the difference between net disposal proceeds and carrying amount is recognised in profit and loss. On partial disposal of a holding, the carrying amount allocated is based on the average carrying amount of the total holding.',
            'Investment property is accounted for as a long-term investment, at cost less any permanent decline.'],
          'When an investment changes its label, it moves at the more conservative figure.',
          'A long-term share carried at cost ₹50 with a provision of ₹10 moves to current at ₹40.'),
        C('c5', T5, [
            'Disclose the accounting policies for determining carrying amounts; classification of investments; amounts in profit and loss for interest, dividends and rentals (separately for current and long-term), profits and losses on disposal, and changes in carrying amounts; significant restrictions on realisation or remittance; aggregate amounts of quoted and unquoted investments and the market value of quoted ones; and other disclosures required by the relevant statute.'],
          'Readers should be able to see what is held, how it is valued and what it earned.',
          'Quoted shares are disclosed with their market value as well as their carrying amount.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Investment register at year end', 'role': 'Accounts executive',
             'situation': 'The company holds shares, debentures and mutual fund units, some for trading and some strategic.',
             'steps': ['Classify each holding as current or long-term.', 'Value current ones at lower of cost and fair value (individually or by category).', 'Test long-term holdings for permanent decline.', 'Separate pre-acquisition income from cost.'],
             'takeaway': 'Classification decides the valuation rule.'}]

    mcqs = [
        Q('m1', 'An easily saleable investment bought to be kept for twelve months or less is:', ['A current investment', 'A long-term investment', 'Investment property', 'Inventory'], 0,
          'AS 13 classifies an investment as current if, by its nature, it can be sold easily and is meant to be kept for a year or less after purchase. All other investments are long-term. In practice: record intent at purchase.', 'c1', T1),
        Q('m2', 'Brokerage paid on purchase of shares is:', ['Added to the cost of the investment', 'Expensed immediately', 'Deducted from dividend', 'Shown as a deferred expense'], 0,
          'What it cost to buy the investment — brokerage, fees and duties — forms part of its cost. They are part of what it took to acquire the investment. In practice: include stamp duty too.', 'c2', T2),
        Q('m3', 'Dividend received out of profits earned before the shares were bought is:', ['Deducted from the cost of the investment', 'Credited to profit and loss', 'Credited to capital reserve as profit', 'Ignored'], 0,
          'Income relating to the pre-acquisition period is a recovery of cost rather than income, so it reduces the carrying cost of the investment. Only post-acquisition income goes to profit and loss. In practice: check the period of the dividend.', 'c2', T2),
        Q('m4', 'Bonus shares received on an investment are recorded:', ['At nil cost, reducing the average cost per share', 'At face value as income', 'At market value as income', 'At market value as capital reserve'], 0,
          'Bonus shares involve no outlay, so no cost is added; the original cost is spread over the increased number of shares, lowering the average cost per share. In practice: update the holding quantity.', 'c2', T2),
        Q('m5', 'Current investments may be valued at lower of cost and fair value on:', ['An individual or category basis, but not overall', 'An overall basis only', 'An individual basis only', 'Any basis the company chooses'], 0,
          'AS 13 allows the comparison to be made for each investment or for each category of investments, but not on a global basis that would let gains on some offset losses on others across categories. In practice: individual is the prudent choice.', 'c3', T3),
        Q('m6', 'Long-term investments are carried at:', ['Cost less provision for other-than-temporary decline', 'Market value', 'Lower of cost and market value always', 'Face value'], 0,
          'Long-term investments are usually held at cost, with a provision only for a decline in value that is not temporary, assessed for each investment separately. Temporary market dips are ignored. In practice: document indicators.', 'c3', T3),
        Q('m7', 'A current investment (cost ₹80,000; fair value ₹70,000) is reclassified as long-term. Transfer value:', ['₹70,000', '₹80,000', '₹75,000', '₹10,000'], 0,
          'A move from current to long-term uses cost or fair value at the transfer date, whichever is less: lower of ₹80,000 and ₹70,000 is ₹70,000. In practice: the new carrying amount becomes its cost for later tests.', 'c4', T4, 'moderate', check=70000),
        Q('m8', 'On selling part of a holding, the carrying amount of the part sold is based on:', ['The average carrying amount of the total holding', 'FIFO', 'The highest cost lot', 'Market value'], 0,
          'AS 13 states that when part of a holding is sold, the amount removed is worked out from the average carrying value per unit of the whole holding. In practice: maintain an average cost register.', 'c4', T4),
        Q('m9', '500 debentures of ₹100 (10% p.a., interest 31 March and 30 September) bought on 1 June at ₹102 cum-interest. Cost of investment:', ['₹50,166.67', '₹51,000', '₹50,000', '₹49,166.67'], 0,
          'Accrued interest for April–May is 50,000 × 10% × 2/12 = ₹833.33. Cost = 51,000 − 833.33 = ₹50,166.67. Accrued interest is excluded from cost and set against the next interest receipt. In practice: compute days precisely.', 'c2', T2, 'hard', check=50166.67),
        Q('m10', 'Which disclosure is required by AS 13?', ['Market value of quoted investments', 'Name of the broker', 'Tax paid on dividends', 'The investee\'s profit'], 0,
          'AS 13 asks for aggregate amounts of quoted and unquoted investments with the market value of quoted ones, together with policies, classification and related income. In practice: follow Schedule III too.', 'c5', T5),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Accrued interest excluded', 2, 'computation', 'accrued', nums=[acc, cost]),
           S('s2', 'Income for holding period', 2, 'computation', 'income', nums=[inc]),
           S('s3', 'Pre-acquisition part as recovery', 1, 'concept', 'pre-acquisition|recovery')],
          ['Split the interest by period.'], ['Including accrued interest in cost.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Individual basis', 1.5, 'computation', 'individual', nums=[ind]),
           S('s2', 'Category basis', 1.5, 'computation', 'category', nums=[cat]),
           S('s3', 'Global basis not allowed', 1, 'concept', 'global|overall')],
          ['Show both permitted bases.'], ['Netting across categories.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a current investment?', 'One that can be sold easily and that the holder means to keep for a year or less from purchase.',
          [P('p1', 'Easily sold', 5, 'sold|realis'), P('p2', 'One year', 5, 'a year|one year|1 year')], 'c1'),
        V('v2', 'How are long-term investments valued?', 'At cost, with a provision for any decline in value that is other than temporary, assessed for each investment.',
          [P('p1', 'At cost', 5, 'cost'), P('p2', 'Permanent decline provision', 5, 'temporary|permanent')], 'c3'),
        V('v3', 'How is pre-acquisition dividend treated?', 'It is treated as a recovery of cost and reduces the carrying amount of the investment rather than being taken as income.',
          [P('p1', 'Recovery of cost', 6, 'cost'), P('p2', 'Not income', 4, 'income')], 'c2'),
        V('v4', 'At what amount is a long-term investment moved to current?', 'At the lower of its cost and carrying amount at the date of transfer.',
          [P('p1', 'Lower of', 5, 'lower'), P('p2', 'Cost and carrying amount', 5, 'carrying')], 'c4'),
        V('v5', 'What is investment property?', 'Land or buildings held mainly to earn rent or for capital appreciation and not substantially occupied by the enterprise for its own operations; it is accounted for as a long-term investment.',
          [P('p1', 'Land or buildings for rent or appreciation', 6, 'land|building'), P('p2', 'Long-term investment', 4, 'long-term')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Varun Holdings Ltd.', 'difficulty': 'moderate',
              'case': 'Varun Holdings Ltd. bought 2,000 shares of X Ltd. at ₹150 each (brokerage ₹6,000) as a long-term investment. It later received a 1:4 bonus issue. X Ltd. has had heavy losses for three years and its net worth is negative; the market price is ₹40.',
              'mcqs': [
                  M('k1a', 'Cost of the investment:', ['₹3,06,000', '₹3,00,000', '₹2,94,000', '₹3,60,000'], 0,
                    'Cost includes the purchase price of ₹3,00,000 plus brokerage of ₹6,000, giving ₹3,06,000. Acquisition charges form part of cost under AS 13. In practice: capitalise duties too.', 'core', check=306000, topic=T2),
                  M('k1b', 'Average cost per share after the bonus:', ['₹122.40', '₹153', '₹120', '₹150'], 0,
                    'The bonus adds 500 shares at nil cost, so ₹3,06,000 is spread over 2,500 shares, giving ₹122.40 a share. In practice: average cost matters for later partial sales.', 'moderate', check=122.4, topic=T2),
                  M('k1c', 'Is a provision for diminution required?', ['Yes, as the decline appears other than temporary', 'No, long-term investments are never written down', 'Only if sold', 'Only in the consolidated accounts'], 0,
                    'Persistent losses and negative net worth indicate a decline that is not temporary, so a provision is needed for this long-term investment. In practice: estimate the recoverable value carefully.', 'moderate', topic=T3),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch05', 3, 'Accounting Standard 13 Accounting for Investments',
                ['Classify investments as current or long-term.',
                 'Determine the cost of investments, including cum-interest, bonus and rights.',
                 'Value current and long-term investments and handle reclassifications and disposals.',
                 'State the disclosure requirements.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 30}, 'prereq': ['int-p1-ch05-u02'],
                 'exam_tip': 'Prepare an investment account with columns for nominal value, income and cost; strip pre-acquisition income out of cost.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Current: readily realisable, ≤ 1 year; others long-term.', 'Cost includes brokerage and duties; exclude pre-acquisition income and accrued interest.',
                             'Bonus: nil cost; rights: add cost.', 'Current at lower of cost and FV (individual or category, never global).',
                             'Long-term at cost less permanent decline.', 'Reclassify LT→C at lower of cost and carrying; C→LT at lower of cost and FV.'],
                 'remember': ['Partial disposal uses average carrying amount.'],
                 'traps': ['Do not net gains and losses across all current investments.']},
                [('Current', 'Lower of cost and FV'), ('Long-term', 'Cost less permanent decline'), ('Bonus shares', 'Nil cost')],
                viva, cases)
