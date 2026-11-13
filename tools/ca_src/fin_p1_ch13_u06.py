"""CA Final · Paper 1 Financial Reporting · Chapter 13 Unit 6 Ind AS 28 Investments in Associates and Joint Ventures.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch13-u06'
T1 = 'Significant influence and scope'
T2 = 'Applying the equity method'
T3 = 'Transactions, losses and impairment'
T4 = 'Exemptions, discontinuance and changes in interest'


def build():
    ck = Checks()
    gw = ck.add('300-0.3*900', 'Notional goodwill within the investment (₹ crore)')
    share = ck.add('0.3*100', 'Share of profit (₹ crore)')
    div = ck.add('0.3*40', 'Dividend received (₹ crore)')
    oci = ck.add('0.3*20', 'Share of OCI (₹ crore)')
    urp = ck.add('20*0.3', 'Unrealised profit eliminated on downstream sale (₹ crore)')
    cv = ck.add('300+0.3*100-0.3*40+0.3*20-20*0.3', 'Carrying amount at year end (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Equity accounting in year one', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Ivy Ltd. buys 30% of Jade Ltd. for ₹300 crore when Jade\'s identifiable net assets have a fair value of ₹900 crore. During the year Jade earns profit of ₹100 crore, has OCI gains of ₹20 crore and pays dividends of ₹40 crore. Ivy sold goods to Jade at a profit of ₹20 crore; Jade still holds them. Compute the carrying amount at year end.',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Cost', 'Includes goodwill of 300 − 270', inr(300)],
              ['Goodwill (not separately recognised)', '300 − 30% × 900', inr(gw)],
              ['Add share of profit', '30% × 100', inr(share)],
              ['Add share of OCI', '30% × 20', inr(oci)],
              ['Less dividend received', '30% × 40', inr(div)],
              ['Less unrealised profit (downstream)', '30% × 20', inr(urp)],
              ['Carrying amount', '300 + 30 + 6 − 12 − 6', inr(cv)]], title='Equity method')],
          'checks': list(ck)}

    ck2 = Checks()
    rec = ck2.add('min(0.4*500,60+30)', 'Losses recognised by investor (₹ crore)')
    unrec = ck2.add('0.4*500-min(0.4*500,60+30)', 'Unrecognised losses carried forward (₹ crore)')
    i2 = {'id': 'i2', 'title': 'Losses beyond the investment', 'difficulty': 'hard', 'minutes': 8,
          'q': 'Ivy holds 40% of Opal Ltd., carried at ₹60 crore, and has also given Opal a long-term loan of ₹30 crore that forms part of its net investment (no repayment planned). Opal makes a loss of ₹500 crore. Ivy has no obligation to fund further losses. How much loss does Ivy recognise?',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Share of loss', '40% × 500', inr(200)],
              ['Interest in associate', 'Investment 60 + long-term loan 30', inr(90)],
              ['Loss recognised', 'Limited to interest', inr(rec)],
              ['Unrecognised losses (memorandum)', '200 − 90', inr(unrec)]], title='Losses limited to the interest')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Ind AS 28 covers every investor that either shares control of an investee jointly or can significantly influence it. Significant influence is presumed at 20% or more of voting power (direct or through subsidiaries) unless clearly shown otherwise.',
            'Evidence of significant influence: board representation; participation in policy-making including dividend decisions; material transactions; interchange of managerial staff; provision of essential technical information. Potential voting rights currently exercisable are considered but the share of profit is based on present ownership.',
            'Loss of significant influence can happen without a change in ownership, e.g. when the associate comes under the control of a government, court or regulator.'],
          'Influence shows in the boardroom and in the business relationship.',
          'An investor supplying essential technology may have significant influence at 15%.'),
        C('c2', T2, [
            'Under the equity method the investment is first recognised at cost; afterwards it moves up or down with the investor\'s share of the investee\'s profit or loss (in the investor\'s profit) and OCI (in the investor\'s OCI). Distributions reduce the carrying amount.',
            'On acquisition, the difference between cost and the investor\'s share of the net fair value of identifiable assets is accounted for as: goodwill included in the carrying amount (not amortised); or, if negative, recognised directly in equity as capital reserve (Indian modification). Share of profits is adjusted for extra depreciation on fair value uplifts.',
            'The most recent available statements are used; reporting date gaps cannot exceed three months. Uniform accounting policies are applied. Cumulative preference dividends held by others are deducted before computing the share.'],
          'One line in the balance sheet, one line in profit — tracking the investor\'s slice.',
          'Dividends received reduce the investment, not profit.'),
        C('c3', T3, [
            'Gains and losses from upstream (associate to investor) and downstream (investor to associate) transactions are recognised only to the extent of unrelated investors\' interests; the investor\'s share is eliminated. Losses that evidence impairment are recognised in full.',
            'When the investor\'s share of losses equals or exceeds its interest (the carrying amount plus long-term interests that form part of the net investment, such as long-term loans), it stops recognising further losses. Additional losses are provided only to the extent of legal or constructive obligations or payments made on behalf of the associate. Later profits are recognised only after the unrecognised losses are covered.',
            'After applying the equity method, the net investment is tested for impairment under Ind AS 36 as a single asset; goodwill inside is not tested separately, and impairment reversals are allowed.'],
          'Eliminate your own share of internal profits; stop at zero unless you are on the hook.',
          'A long-term loan to an associate absorbs losses after the investment hits nil.'),
        C('c4', T4, [
            'The equity method need not be applied if the investor is a parent exempt from consolidation, or a wholly or partly owned subsidiary meeting exemption conditions. Venture capital organisations, mutual funds and similar entities may elect FVTPL for investments in associates and joint ventures.',
            'Investments meeting held-for-sale criteria apply Ind AS 105. Use of the equity method ends when the investment ceases to be an associate or joint venture: if it becomes a subsidiary, Ind AS 103 applies; if a financial asset, the retained interest is measured at fair value and the difference with carrying amount (plus disposal proceeds) is recognised in profit or loss, with OCI reclassified as if disposed of.',
            'A change from associate to joint venture (or vice versa) continues the equity method without remeasurement. A reduction in ownership interest that keeps the equity method reclassifies a proportionate share of OCI.'],
          'Exit the equity method at fair value unless switching between associate and JV.',
          'Selling down from 30% to 10% triggers a fair value remeasurement of the 10%.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Equity method schedule', 'role': 'Group accountant',
             'situation': 'The group holds four associates with different year ends.',
             'steps': ['Align policies and reporting dates.', 'Compute share of profit with fair value adjustments.', 'Eliminate share of internal profits.', 'Test the investment for impairment.'],
             'takeaway': 'The equity method is a mini-consolidation on one line.'}]

    mcqs = [
        Q('m1', 'Under the equity method, dividends received from an associate:', ['Reduce the carrying amount', 'Are income', 'Increase the investment', 'Go to OCI'], 0,
          'Distributions return part of the investment. In practice: income in separate statements.', 'c2', T2),
        Q('m2', 'Goodwill on acquiring an associate is:', ['Included in the carrying amount, not amortised', 'Shown separately', 'Amortised', 'Written off'], 0,
          'Not tested separately for impairment. In practice: whole investment tested.', 'c2', T2),
        Q('m3', 'Negative goodwill on acquiring an associate is, in India:', ['Recognised directly in equity as capital reserve', 'Income in profit or loss', 'Deducted from cost', 'Ignored'], 0,
          'Indian modification to Ind AS 28. In practice: reassess fair values first.', 'c2', T2),
        Q('m4', 'Unrealised profit on a downstream sale to a 30% associate is eliminated to the extent of:', ['The investor\'s 30% share', '100%', '70%', 'Nil'], 0,
          'Only own share is eliminated. In practice: reduce investment.', 'c3', T3),
        Q('m5', 'After the investment reaches nil, further losses are recognised:', ['Only for legal or constructive obligations', 'Always', 'Never', 'In OCI'], 0,
          'Long-term interests absorb first. In practice: track unrecognised losses.', 'c3', T3),
        Q('m6', 'Venture capital organisations may measure associates at:', ['FVTPL by election', 'Cost only', 'Equity method only', 'Amortised cost'], 0,
          'Exemption from equity method. In practice: per investment.', 'c4', T4),
        Q('m7', 'When an associate becomes a joint venture, the investor:', ['Continues the equity method without remeasurement', 'Remeasures at fair value', 'Consolidates', 'Applies Ind AS 109'], 0,
          'Same method continues. In practice: no gain.', 'c4', T4),
        Q('m8', 'The reporting date gap between investor and associate may not exceed:', ['Three months', 'Six months', 'One month', 'Twelve months'], 0,
          'Adjust for significant events. In practice: same as subsidiaries.', 'c2', T2),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Goodwill', 1.5, 'computation', 'goodwill', nums=[gw]), S('s2', 'Profit and OCI', 2, 'computation', 'profit|oci', nums=[share, oci]), S('s3', 'Dividend and URP', 2, 'computation', 'dividend|unrealised', nums=[div, urp]), S('s4', 'Carrying amount', 2.5, 'computation', 'carrying', nums=[cv])],
          ['Show each movement.'], ['Treating dividends as income.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Interest', 2, 'computation', 'interest', nums=[90]), S('s2', 'Recognised', 1.5, 'computation', 'recognised', nums=[rec]), S('s3', 'Unrecognised', 1.5, 'computation', 'unrecognised', nums=[unrec])],
          ['Include the long-term loan.'], ['Recognising full loss.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Describe the equity method.', 'The investment starts at cost and is adjusted for the investor\'s share of the investee\'s profit, OCI and distributions.',
          [P('p1', 'Starts at cost', 4, 'cost'), P('p2', 'Share of profit and OCI', 6, 'share')], 'c2'),
        V('v2', 'What evidence indicates significant influence?', 'Board representation, policy participation, material transactions, interchange of managers and provision of essential technical information.',
          [P('p1', 'Board representation', 5, 'board'), P('p2', 'Transactions and personnel', 5, 'transaction|manager')], 'c1'),
        V('v3', 'How are losses limited?', 'Losses are recognised until the investment and long-term interests reach zero; further losses only to the extent of obligations or payments made.',
          [P('p1', 'Down to zero', 5, 'zero'), P('p2', 'Obligations', 5, 'obligation')], 'c3'),
        V('v4', 'How is the investment tested for impairment?', 'As a single asset under Ind AS 36 after applying the equity method, with goodwill inside it not tested separately.',
          [P('p1', 'Single asset', 5, 'single asset'), P('p2', 'Ind AS 36', 5, '36')], 'c3'),
        V('v5', 'What happens when an associate becomes a financial asset?', 'The retained interest is measured at fair value, the difference goes to profit or loss and OCI is reclassified as if the investee were disposed of.',
          [P('p1', 'Fair value', 5, 'fair value'), P('p2', 'Profit or loss', 5, 'profit or loss')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Kiwi Ltd.', 'difficulty': 'moderate',
              'case': 'Kiwi Ltd. buys 25% of Lime Ltd. for ₹200 crore; Lime\'s identifiable net assets have a fair value of ₹840 crore. Lime\'s plant has a fair value ₹40 crore above book value, remaining life 10 years. Lime\'s reported profit for the year is ₹80 crore. Lime sold goods to Kiwi at a profit of ₹12 crore; all are still in Kiwi\'s inventory.',
              'mcqs': [
                  M('k1a', 'Capital reserve on acquisition (₹ crore):', ['10', '40', 'Nil', '25'], 0,
                    'Share of net assets 210 − cost 200 = 10, taken to equity. In practice: reassess first.', 'moderate', check=10, topic=T2),
                  M('k1b', 'Adjusted profit of Lime for equity accounting (₹ crore):', ['76', '80', '84', '40'], 0,
                    '80 − extra depreciation 4. In practice: fair value uplifts reduce profit.', 'moderate', check=76, topic=T2),
                  M('k1c', 'Kiwi\'s share of unrealised profit to eliminate (₹ crore):', ['3', '12', '9', 'Nil'], 0,
                    '25% × 12 upstream. In practice: reduce share of profit.', 'core', check=3, topic=T3),
                  M('k1d', 'Kiwi\'s share of profit recognised (₹ crore):', ['16', '19', '20', '21'], 0,
                    '25% × 76 − 3 = 16. In practice: one line in P&L.', 'hard', check=16, topic=T2),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch13', 6, 'Ind AS 28 "Investments in Associates and Joint Ventures"',
                ['Identify significant influence and the scope of Ind AS 28.',
                 'Apply the equity method including acquisition adjustments.',
                 'Account for transactions, losses and impairment.',
                 'Apply exemptions and account for discontinuing the equity method.'],
                {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 35}, 'prereq': ['fin-p1-ch13-u05'],
                 'exam_tip': 'Prepare an investment account: cost, + share of profit and OCI, − dividends, − share of URP, − impairment.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['20% presumption; evidence-based.',
                             'Cost, then share of profit/OCI, less dividends.',
                             'Goodwill inside; negative goodwill to capital reserve.',
                             'Eliminate own share of internal profits.',
                             'Stop losses at nil unless obligated.'],
                 'remember': ['Impairment test on the whole investment.'],
                 'traps': ['Eliminating 100% of URP for associates.']},
                [('Dividends', 'Reduce investment'), ('URP', 'Investor share only'), ('Negative goodwill', 'Capital reserve'), ('Losses', 'Stop at nil')],
                viva, cases)
