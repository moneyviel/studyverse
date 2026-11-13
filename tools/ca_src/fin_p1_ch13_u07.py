"""CA Final · Paper 1 Financial Reporting · Chapter 13 Unit 7 Ind AS 27 Separate Financial Statements.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch13-u07'
T1 = 'What separate statements are'
T2 = 'Measuring investments in separate statements'
T3 = 'Dividends and impairment indicators'
T4 = 'Group reorganisations and disclosures'


def build():
    ck = Checks()
    cost = ck.add('500', 'Investment at cost (₹ crore)')
    div = ck.add('0.8*50', 'Dividend income from subsidiary (₹ crore)')
    imp = ck.add('500-430', 'Impairment loss (₹ crore)')
    i1 = {'id': 'i1', 'title': 'A subsidiary at cost', 'difficulty': 'core', 'minutes': 7,
          'q': 'Mango Ltd. carries its 80% investment in Pine Ltd. at cost of ₹500 crore in its separate statements. Pine declares a dividend of ₹50 crore, which exceeds Pine\'s total comprehensive income for the year. An impairment test then gives a recoverable amount of ₹430 crore. Show Mango\'s entries.',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Investment at cost', 'Ind AS 27 policy choice', inr(cost)],
              ['Dividend income in profit or loss', '80% × 50 when right established', inr(div)],
              ['Impairment indicator', 'Dividend exceeds total comprehensive income', 'Test required'],
              ['Impairment loss', '500 − 430', inr(imp)],
              ['Carrying amount', 'After impairment', inr(430)]], title='Separate statements')],
          'checks': list(ck)}

    ck2 = Checks()
    nc = ck2.add('1.0*1200', 'New parent\'s cost of investment (₹ crore)')
    i2 = {'id': 'i2', 'title': 'Inserting a new holding company', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Shareholders of Old Co. exchange all their shares for shares of a newly formed New Co., in the same proportions; Old Co.\'s assets and liabilities are unchanged. Old Co.\'s equity in its separate statements is ₹1,200 crore; the fair value of New Co.\'s shares issued is ₹2,000 crore. New Co. measures the investment at cost. What is that cost?',
          'solution': [table(['Case', 'Working', '₹ crore'], [
              ['Conditions met', 'No change in assets, liabilities or owners\' relative interests', 'Reorganisation rule'],
              ['Cost of investment', '100% × Old Co. equity carrying amount (not ₹2,000 crore fair value)', inr(nc)]], title='Reorganisation cost')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Separate financial statements are presented by a parent, or an investor with joint control or significant influence, in addition to consolidated or equity-accounted statements (or as its only statements if exempt), with investments in subsidiaries, joint ventures and associates carried at cost, under Ind AS 109 or using the equity method.',
            'Whether an entity must publish separate statements is not decided by Ind AS 27 — that is left to law (in India, the Companies Act requires standalone statements).',
            'Statements of an entity without subsidiaries, associates or joint ventures are not separate statements; nor are equity-accounted statements of an investor with only associates.'],
          'Separate statements show the investor\'s own books, with investees as investments.',
          'A listed parent files both standalone and consolidated accounts.'),
        C('c2', T2, [
            'Investments in subsidiaries, joint ventures and associates are accounted for at cost, in accordance with Ind AS 109, or using the equity method under Ind AS 28 — the same choice for each category of investments.',
            'Investments held for sale follow Ind AS 105 if at cost or equity method; those under Ind AS 109 stay under it.',
            'Venture capital organisations and similar entities that measure investments at FVTPL in consolidated statements must do the same in separate statements. Investment entities measure subsidiaries at FVTPL in separate statements too.'],
          'Pick cost, fair value or equity method per category and stick with it.',
          'All subsidiaries at cost, all associates at FVOCI is a valid policy set.'),
        C('c3', T3, [
            'Dividends from subsidiaries, joint ventures or associates are recognised in profit or loss when the right to receive them is established; under the equity method, they reduce the carrying amount.',
            'Indicators of impairment for an investment include: the dividend exceeds the investee\'s total comprehensive income for the period, or the carrying amount in separate statements exceeds the carrying amount of the investee\'s net assets (including goodwill) in consolidated statements.',
            'Impairment is assessed under Ind AS 36 for investments at cost.'],
          'Generous dividends may signal that the investment is now worth less.',
          'A subsidiary paying out more than it earns triggers an impairment test.'),
        C('c4', T4, [
            'When a new parent is established through a share exchange, with no change to the original parent\'s assets, liabilities or owners\' relative interests, and the new parent uses cost, it measures cost at the carrying amount of its share of equity in the original parent\'s separate statements at the reorganisation date.',
            'The same applies when an entity that is not a parent becomes one in this manner.',
            'Disclosures include: the fact that statements are separate, the reason if consolidation exemption is used, a list of significant investments with name, place of business, ownership and voting rights, and the method used to account for them.'],
          'Reorganisations carry over book values, not fair values.',
          'A new holding company over an existing group records cost at the old parent\'s equity.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Standalone investment review', 'role': 'Financial controller',
             'situation': 'The holding company carries 12 subsidiaries at cost.',
             'steps': ['Confirm policy per category.', 'Book dividends when declared.', 'Check impairment indicators.', 'Prepare investment disclosures.'],
             'takeaway': 'Standalone carrying amounts need periodic impairment checks.'}]

    mcqs = [
        Q('m1', 'In separate statements, investments in subsidiaries may be measured:', ['At cost, under Ind AS 109, or by equity method', 'Only at cost', 'Only at fair value', 'By proportionate consolidation'], 0,
          'Same choice per category. In practice: most use cost.', 'c2', T2),
        Q('m2', 'Dividend from a subsidiary carried at cost is:', ['Income in profit or loss', 'Reduction in investment', 'OCI', 'Equity'], 0,
          'Recognised when the right is established. In practice: check for impairment.', 'c3', T3),
        Q('m3', 'An impairment indicator for an investment is a dividend that:', ['Exceeds the investee\'s total comprehensive income', 'Is paid in cash', 'Is small', 'Is declared annually'], 0,
          'Suggests value is being distributed. In practice: also compare with consolidated net assets.', 'c3', T3),
        Q('m4', 'In a qualifying reorganisation, the new parent\'s cost is:', ['Its share of the original parent\'s equity carrying amount', 'Fair value of shares issued', 'Nominal value', 'Market value'], 0,
          'Book value carryover. In practice: no goodwill.', 'c4', T4),
        Q('m5', 'Which entities must prepare separate statements is decided by:', ['Law or regulation', 'Ind AS 27', 'Auditors', 'Board choice'], 0,
          'Ind AS 27 does not mandate. In practice: Companies Act.', 'c1', T1),
        Q('m6', 'Statements of an entity with no investees are:', ['Not separate statements', 'Separate statements', 'Consolidated statements', 'Combined statements'], 0,
          'Separate requires investees. In practice: just standalone.', 'c1', T1),
        Q('m7', 'A venture capital organisation measuring associates at FVTPL in consolidated statements must, in separate statements:', ['Also use FVTPL', 'Use cost', 'Use equity method', 'Choose freely'], 0,
          'Consistency required. In practice: same measurement.', 'c2', T2),
        Q('m8', 'Separate statements disclose for significant investments:', ['Name, place of business, ownership and method used', 'Only names', 'Only fair values', 'Nothing'], 0,
          'Ind AS 27 disclosures. In practice: include voting rights.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Dividend', 1.5, 'computation', 'dividend', nums=[div]), S('s2', 'Indicator', 1.5, 'concept', 'indicator|exceeds'), S('s3', 'Impairment', 2, 'computation', 'impairment', nums=[imp])],
          ['Name the indicator.'], ['Reducing investment by dividend.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Rule', 1.5, 'concept', 'carrying amount|equity'), S('s2', 'Amount', 1.5, 'computation', 'cost', nums=[nc])],
          ['State conditions.'], ['Using fair value.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What are separate financial statements?', 'Statements of a parent or investor in which investments in subsidiaries, joint ventures and associates are carried at cost, under Ind AS 109 or using the equity method.',
          [P('p1', 'Parent or investor', 5, 'parent|investor'), P('p2', 'Measurement choices', 5, 'cost|109|equity method')], 'c1'),
        V('v2', 'When is dividend income recognised?', 'In profit or loss when the right to receive it is established.',
          [P('p1', 'Right established', 6, 'right'), P('p2', 'Profit or loss', 4, 'profit or loss')], 'c3'),
        V('v3', 'Name two impairment indicators for investments.', 'Dividend exceeding total comprehensive income, and separate carrying amount exceeding the investee\'s consolidated net assets including goodwill.',
          [P('p1', 'Dividend exceeds income', 5, 'exceed'), P('p2', 'Net assets comparison', 5, 'net assets')], 'c3'),
        V('v4', 'How does a new parent measure cost in a reorganisation?', 'At its share of the original parent\'s equity carrying amount in separate statements at the reorganisation date.',
          [P('p1', 'Share of equity', 5, 'equity'), P('p2', 'Carrying amount', 5, 'carrying')], 'c4'),
        V('v5', 'Must the same method be used for all subsidiaries?', 'Yes, the chosen method is applied consistently to each category of investments.',
          [P('p1', 'Consistent', 5, 'consistent'), P('p2', 'Each category', 5, 'category')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Olive Holdings Ltd.', 'difficulty': 'core',
              'case': 'Olive Holdings Ltd. carries its subsidiary Peach Ltd. at cost ₹300 crore and its associate Plum Ltd. at FVOCI under Ind AS 109 (fair value ₹90 crore, cost ₹70 crore). Peach declares a dividend of ₹25 crore and Plum ₹5 crore.',
              'mcqs': [
                  M('k1a', 'Total dividend income in Olive\'s profit or loss (₹ crore):', ['30', '25', '5', 'Nil'], 0,
                    'Both dividends are income in separate statements. In practice: FVOCI equity dividends go to P&L.', 'core', check=30, topic=T3),
                  M('k1b', 'Plum\'s fair value gain of ₹20 crore goes to:', ['OCI', 'Profit or loss', 'Investment cost', 'Capital reserve'], 0,
                    'FVOCI election. In practice: never recycled.', 'core', topic=T2),
                  M('k1c', 'Peach is carried at (₹ crore), absent impairment:', ['300', '275', '325', 'Fair value'], 0,
                    'Cost is unchanged by dividends. In practice: test for impairment if indicated.', 'core', check=300, topic=T2),
                  M('k1d', 'These standalone statements are:', ['Separate financial statements', 'Consolidated statements', 'Combined statements', 'Interim statements'], 0,
                    'Parent with investees. In practice: Companies Act standalone.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch13', 7, 'Ind AS 27 "Separate Financial Statements"',
                ['Explain what separate financial statements are.',
                 'Measure investments in subsidiaries, joint ventures and associates.',
                 'Recognise dividends and identify impairment indicators.',
                 'Apply reorganisation rules and disclosures.'],
                {'difficulty': 'core', 'minutes': {'learn': 20, 'practice': 15}, 'prereq': ['fin-p1-ch13-u06'],
                 'exam_tip': 'In separate statements, dividends are income — then check whether they signal impairment.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Separate statements: investor\'s own view.',
                             'Cost, Ind AS 109 or equity method per category.',
                             'Dividends to profit when right established.',
                             'Impairment indicators from dividends.',
                             'Reorganisation: carry over book equity.'],
                 'remember': ['Law decides who prepares separate statements.'],
                 'traps': ['Eliminating dividends in standalone accounts.']},
                [('Measurement', 'Cost / 109 / equity'), ('Dividend', 'P&L'), ('Indicator', 'Dividend > TCI'), ('Reorganisation', 'Book equity')],
                viva, cases)
