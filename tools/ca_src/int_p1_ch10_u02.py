"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 10 Unit 2 — AS 23 Accounting for Investments in Associates in Consolidated Financial Statements.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch10-u02'
T1 = 'Associates and significant influence'
T2 = 'The equity method'
T3 = 'Goodwill or capital reserve and adjustments'
T4 = 'Losses, exclusions and impairment'
T5 = 'Disclosure and separate statements'


def build():
    ck = Checks()
    sh = ck.add('1500000*30/100', 'Investor\'s share of net assets at acquisition (₹)')
    gw = ck.add('600000-450000', 'Goodwill included in carrying amount (₹)')
    pr = ck.add('400000*30/100', 'Share of profit for the year (₹)')
    dv = ck.add('100000*30/100', 'Dividend received (₹)')
    ca = ck.add('600000+120000-30000', 'Carrying amount at year end (₹)')
    i1 = {'id': 'i1', 'title': 'Equity method in year 1', 'difficulty': 'core', 'minutes': 8,
          'q': 'Akash Ltd. bought 30% of Bela Ltd. for ₹6,00,000 when Bela\'s net assets were ₹15,00,000. During the year Bela earned ₹4,00,000 and paid a dividend of ₹1,00,000. Show the investment in Akash\'s consolidated statements.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Cost of investment', '', inr(600000)],
              ['Share of net assets at acquisition', '30% × 15,00,000', inr(sh)],
              ['Goodwill (within carrying amount, disclosed)', '', inr(gw)],
              ['Add: share of profit', '30% × 4,00,000', inr(pr)],
              ['Less: dividend received', '30% × 1,00,000', inr(dv)],
              ['Carrying amount at year end', '', inr(ca)]], title='AS 23 equity method')],
          'checks': list(ck)}

    ck2 = Checks()
    unrec = ck2.add('300000-200000', 'Share of loss not recognised in year 1 (₹)')
    y2 = ck2.add('150000-100000', 'Share of profit recognised in year 2 (₹)')
    i2 = {'id': 'i2', 'title': 'When the associate makes losses', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Chirag Ltd.\'s investment in an associate is carried at ₹2,00,000 under the equity method. In year 1 its share of the associate\'s loss is ₹3,00,000; in year 2 its share of profit is ₹1,50,000. Chirag has no obligation to fund losses. Show the effect.',
          'solution': [table(['Year', 'Working', 'Result'], [
              ['1', 'Carrying amount reduced to nil', f'Unrecognised loss {inr(unrec)}'],
              ['2', 'Profit first covers the unrecognised loss', f'Recognise {inr(y2)}']], title='Losses beyond the investment')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'An associate is a business over which the investor holds significant influence, other than one that is its subsidiary or joint venture.',
            'Significant influence is the power to take part in the financial and operating policy decisions of the investee, without control. Holding 20% or more of voting power (directly or through subsidiaries) presumes it unless clearly shown otherwise; below 20% presumes its absence unless clearly shown.',
            'Evidence includes board representation, participation in policy-making, material transactions, interchange of managerial staff and provision of essential technical information. A majority owner elsewhere does not necessarily prevent significant influence.'],
          'An associate is a company you can steer partly but not control.',
          'A 25% shareholder with two directors on a 9-member board usually has significant influence.'),
        C('c2', T2, [
            'In consolidated financial statements, investments in associates are accounted for by the equity method: the investment is first recorded at cost and then adjusted for the investor\'s share of the associate\'s post-acquisition profits or losses.',
            'Distributions received from the associate reduce the carrying amount.',
            'The carrying amount is also adjusted for the investor\'s share of changes in the associate\'s equity not passing through its profit and loss, such as revaluation of fixed assets or foreign exchange translation differences.',
            'The investor\'s share of the associate\'s results is shown in the consolidated profit and loss.'],
          'The investment grows and shrinks with the investor\'s share of the associate\'s results.',
          'A 40% stake in an associate earning ₹50 lakh raises the investment by ₹20 lakh.'),
        C('c3', T3, [
            'On acquisition, the difference between cost and the investor\'s share of the associate\'s equity is goodwill or capital reserve. This amount sits within the investment\'s carrying figure and is shown separately in the notes.',
            'Unrealised profits and losses on transactions between the investor (or its subsidiaries) and the associate are eliminated to the extent of the investor\'s interest. Unrealised losses are not eliminated if the transaction shows the asset is impaired.',
            'The associate\'s statements are prepared to the investor\'s date where practicable; otherwise the most recent statements are used with adjustments for significant events. Uniform policies are used where practicable, or the fact is disclosed.'],
          'Goodwill on an associate sits inside the investment figure.',
          'If the associate sells goods to the investor with ₹1 lakh profit unsold, a 30% investor eliminates ₹30,000.'),
        C('c4', T4, [
            'If the investor\'s share of losses equals or exceeds the carrying amount, the investment is reported at nil. Further losses are provided only to the extent the investor has guaranteed or committed to obligations of the associate.',
            'When the associate later earns profits, the investor resumes recognising its share only after its share of profits equals the unrecognised losses.',
            'The equity method is not used where the investment is acquired and held exclusively for disposal in the near future, or the associate operates under severe long-term restrictions on transferring funds; such investments follow AS 13. The equity method stops when significant influence ends.',
            'The carrying amount is reduced for any decline in value that is other than temporary, assessed individually.'],
          'An associate\'s losses can wipe out the investment, but not take it below zero unless you promised to pay.',
          'An investor guaranteeing an associate\'s bank loan continues to provide for losses beyond nil.'),
        C('c5', T5, [
            'Disclose an appropriate listing and description of associates, including proportion of ownership interest and, if different, voting power; the reasons for not applying the equity method where relevant; goodwill or capital reserve; and the share of contingencies and capital commitments.',
            'In the consolidated balance sheet, associate investments appear as long-term investments on their own line; the share of profits or losses, and of extraordinary or prior period items, is disclosed separately.',
            'In the investor\'s separate financial statements, investments in associates are carried under AS 13, usually at cost less permanent decline.'],
          'Equity method in consolidated accounts; cost in separate accounts.',
          'An investor without subsidiaries does not prepare CFS and so does not apply AS 23.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Equity accounting schedule', 'role': 'Reporting analyst',
             'situation': 'Your group holds 30% of a logistics company and 22% of a software firm.',
             'steps': ['Confirm significant influence for each.', 'Compute goodwill or capital reserve at acquisition.', 'Add share of profits; deduct dividends.', 'Eliminate share of unrealised profits.'],
             'takeaway': 'One line in the balance sheet hides a full working.'}]

    mcqs = [
        Q('m1', 'Significant influence is presumed when the investor holds voting power of at least:', ['20%', '10%', '26%', '51%'], 0,
          'AS 23 presumes significant influence at 20% or more of voting power, held directly or through subsidiaries, unless it can be clearly shown otherwise. Control would need more than half. In practice: weigh other evidence too.', 'c1', T1, 'core', check=20),
        Q('m2', 'Under the equity method, dividends received from an associate:', ['Reduce the carrying amount of the investment', 'Are credited to profit and loss', 'Increase the investment', 'Are ignored'], 0,
          'The investor already recognises its share of profit; a dividend merely converts part of that into cash, so it reduces the carrying amount. In practice: avoid double counting income.', 'c2', T2),
        Q('m3', 'Goodwill on acquiring an associate is:', ['Included in the carrying amount of the investment and disclosed separately', 'Shown as a separate intangible asset', 'Written off immediately', 'Ignored'], 0,
          'AS 23 includes goodwill or capital reserve in the carrying amount of the investment, with separate disclosure. In practice: track it in the working.', 'c3', T3),
        Q('m4', 'Investment ₹10 lakh for 25%; associate\'s profit ₹8 lakh; dividend ₹4 lakh. Carrying amount at year end:', ['₹11 lakh', '₹12 lakh', '₹10 lakh', '₹13 lakh'], 0,
          'Add 25% of profit (₹2 lakh) and deduct 25% of dividend (₹1 lakh): 10 + 2 − 1 = ₹11 lakh. In practice: use post-acquisition figures only.', 'c2', T2, 'moderate', check=11),
        Q('m5', 'Unrealised profit on sales between an investor and its associate is eliminated:', ['To the extent of the investor\'s interest', 'In full', 'Not at all', 'Only for downstream sales'], 0,
          'AS 23 eliminates unrealised profits and losses to the extent of the investor\'s interest in the associate, unlike full elimination for subsidiaries. In practice: multiply by the holding percentage.', 'c3', T3),
        Q('m6', 'When an investor\'s share of losses exceeds the carrying amount and it has no obligations, the investment is:', ['Reported at nil', 'Shown as a negative asset', 'Shown as a liability', 'Written up'], 0,
          'The carrying amount stops at nil; further losses are recorded only if the investor has guaranteed or committed to obligations of the associate. In practice: keep a memo of unrecognised losses.', 'c4', T4),
        Q('m7', 'The equity method is not applied when the investment is:', ['Acquired and held exclusively for disposal in the near future', 'More than 30%', 'In a loss-making company', 'In a foreign company'], 0,
          'AS 23 excludes investments held exclusively for near-term disposal, and associates under severe long-term restrictions on transfer of funds; these follow AS 13. In practice: document the intention.', 'c4', T4),
        Q('m8', 'In the investor\'s separate financial statements, an investment in an associate is carried:', ['Under AS 13, usually at cost less permanent decline', 'Under the equity method', 'At fair value', 'Proportionately'], 0,
          'AS 23 applies only to consolidated financial statements; separate statements carry the investment under AS 13. In practice: two different figures may appear.', 'c5', T5),
        Q('m9', 'An associate revalues its land upward by ₹10 lakh; the investor holds 30%. In the investor\'s CFS:', ['Investment increases by ₹3 lakh with a corresponding reserve', 'Profit increases by ₹3 lakh', 'No effect', 'Investment increases by ₹10 lakh'], 0,
          'Changes in the associate\'s equity not passing through its profit and loss, such as revaluation, are reflected by adjusting the carrying amount for the investor\'s share, with the other side in reserves. In practice: keep it out of profit.', 'c2', T2, 'moderate'),
        Q('m10', 'Which is evidence of significant influence?', ['Representation on the board of directors', 'Being a major supplier', 'Holding 5% of shares with no board seat', 'Lending money'], 0,
          'Board representation, participation in policy-making, material transactions, interchange of managers and providing essential technical information all indicate significant influence. Ordinary trade or lending does not. In practice: look at governance rights.', 'c1', T1),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Goodwill at acquisition', 1.5, 'computation', 'goodwill', nums=[gw]),
           S('s2', 'Share of profit', 1.5, 'computation', 'profit', nums=[pr]),
           S('s3', 'Dividend and carrying amount', 2, 'computation', 'dividend', nums=[ca])],
          ['Track each movement.'], ['Crediting the dividend to profit.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Stop at nil', 2, 'computation', 'nil', nums=[unrec]),
           S('s2', 'Recover unrecognised losses first', 2, 'computation', 'recognise', nums=[y2])],
          ['Keep a memo of unrecognised losses.'], ['Showing a negative investment.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is an associate?', 'A business over which the investor holds significant influence, and which falls outside the subsidiary and joint venture categories.',
          [P('p1', 'Significant influence', 6, 'significant influence'), P('p2', 'Not subsidiary or JV', 4, 'subsidiary|joint')], 'c1'),
        V('v2', 'Describe the equity method.', 'The investment is recorded at cost and adjusted for the investor\'s share of post-acquisition profits or losses and other equity changes, less distributions received.',
          [P('p1', 'Cost then share of results', 6, 'share'), P('p2', 'Less distributions', 4, 'distribution|dividend')], 'c2'),
        V('v3', 'How far are unrealised profits with an associate eliminated?', 'They are eliminated only up to the investor\'s share (interest) in the associate.',
          [P('p1', 'Investor\'s interest', 6, 'interest|extent'), P('p2', 'Eliminated', 4, 'eliminat')], 'c3'),
        V('v4', 'What happens when losses exceed the investment?', 'The investment is reported at nil; further losses are recognised only for guarantees or commitments, and later profits first cover the unrecognised losses.',
          [P('p1', 'Nil', 5, 'nil'), P('p2', 'Guarantees and recovery', 5, 'guarantee|commit|cover')], 'c4'),
        V('v5', 'Where does AS 23 apply?', 'Only in consolidated financial statements; separate statements use AS 13.',
          [P('p1', 'Consolidated', 6, 'consolidat'), P('p2', 'AS 13 separately', 4, 'as 13|separate')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Deepak Ltd. and Esha Ltd.', 'difficulty': 'moderate',
              'case': 'Deepak Ltd. (which has subsidiaries) bought 40% of Esha Ltd. for ₹50 lakh when Esha\'s net assets were ₹110 lakh. In the year Esha earned ₹20 lakh and sold goods to Deepak at a profit of ₹5 lakh, all unsold at year end.',
              'mcqs': [
                  M('k1a', 'Goodwill on acquiring Esha:', ['₹6 lakh', '₹10 lakh', '₹4 lakh', 'Capital reserve of ₹6 lakh'], 0,
                    'Deepak\'s share of net assets is 40% × ₹110 lakh = ₹44 lakh; cost ₹50 lakh exceeds it by ₹6 lakh, which is goodwill included in the carrying amount. In practice: disclose it separately.', 'moderate', check=6, topic=T3),
                  M('k1b', 'Share of Esha\'s profit after eliminating unrealised profit:', ['₹6 lakh', '₹8 lakh', '₹3 lakh', '₹7 lakh'], 0,
                    '40% of ₹20 lakh is ₹8 lakh; less 40% of the unrealised ₹5 lakh (₹2 lakh) gives ₹6 lakh recognised. In practice: eliminate only the investor\'s share.', 'moderate', check=6, topic=T3),
                  M('k1c', 'Carrying amount of the investment at year end:', ['₹56 lakh', '₹58 lakh', '₹50 lakh', '₹54 lakh'], 0,
                    'Cost ₹50 lakh plus share of profit after elimination ₹6 lakh = ₹56 lakh, with no dividends received. In practice: disclose goodwill within it.', 'moderate', check=56, topic=T2),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch10', 2, 'Accounting Standard 23 Accounting for Investments in Associates in Consolidated Financial Statements',
                ['Identify associates through significant influence.',
                 'Apply the equity method including goodwill and adjustments.',
                 'Treat losses, exclusions and impairment.',
                 'State disclosures and the separate-statement treatment.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 30, 'practice': 30}, 'prereq': ['int-p1-ch10-u01'],
                 'exam_tip': 'Build a carrying-amount schedule: cost → + share of profits → − dividends → ± equity changes → − unrealised profit share.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Associate: significant influence (≥ 20% presumption), not subsidiary or JV.', 'Equity method in CFS: cost + share of results − dividends.',
                             'Goodwill/capital reserve inside carrying amount.', 'Unrealised profits eliminated to investor\'s share.',
                             'Stop at nil unless obligations; exclusions follow AS 13.', 'Separate statements: AS 13.'],
                 'remember': ['Later profits first recover unrecognised losses.'],
                 'traps': ['Dividends reduce the investment; they are not income in CFS.']},
                [('Significant influence', '≥ 20% presumed'), ('Method', 'Equity method (CFS)'), ('Losses', 'Stop at nil')],
                viva, cases)
