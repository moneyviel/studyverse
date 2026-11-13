"""CA Final · Paper 1 Financial Reporting · Chapter 13 Unit 4 Ind AS 110: Consolidation Procedure for Subsidiaries.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch13-u04'
T1 = 'Combining, eliminating and goodwill'
T2 = 'Intra-group transactions and unrealised profit'
T3 = 'Non-controlling interests and changes in ownership'
T4 = 'Loss of control and other procedures'


def build():
    ck = Checks()
    gw = ck.add('500+0.2*550-550', 'Goodwill (₹ crore)')
    urp = ck.add('40*0.25/1.25*0.5', 'Unrealised profit in closing stock (₹ crore)')
    nci_p = ck.add('(100-40*0.25/1.25*0.5)*0.2', 'NCI share of adjusted post-acquisition profit (₹ crore)')
    nci = ck.add('0.2*550+(100-40*0.25/1.25*0.5)*0.2', 'NCI at year end (₹ crore)')
    res = ck.add('800+(100-40*0.25/1.25*0.5)*0.8', 'Consolidated reserves (₹ crore)')
    i1 = {'id': 'i1', 'title': 'A full consolidation', 'difficulty': 'hard', 'minutes': 14,
          'q': 'Polar Ltd. acquired 80% of Sky Ltd. for ₹500 crore when Sky\'s share capital was ₹300 crore and reserves ₹200 crore; land was worth ₹50 crore more than book value. NCI is measured at proportionate share. Since acquisition Sky earned ₹100 crore. During the year Sky sold goods to Polar for ₹40 crore at cost plus 25%; half remain in Polar\'s stock. Polar\'s own reserves are ₹800 crore. Compute goodwill, unrealised profit, NCI and consolidated reserves.',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Net assets at acquisition', '300 + 200 + 50', inr(550)],
              ['Goodwill', '500 + 20% × 550 − 550', inr(gw)],
              ['Unrealised profit (seller is Sky)', '40 × 25/125 × ½', inr(urp)],
              ['Adjusted post-acquisition profit', '100 − 4', inr(96)],
              ['NCI share of post-acquisition profit', '96 × 20%', inr(nci_p)],
              ['NCI at year end', '110 + 19.2', inr(nci)],
              ['Consolidated reserves', '800 + 96 × 80%', inr(res)]], title='Consolidation workings')],
          'checks': list(ck)}

    ck2 = Checks()
    gain = ck2.add('540+180+120-(600+60)', 'Gain on loss of control (₹ crore)')
    i2 = {'id': 'i2', 'title': 'Losing control', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Polar holds 80% of Rain Ltd. At the disposal date, Rain\'s net assets are ₹600 crore, goodwill ₹60 crore and NCI ₹120 crore. Polar sells 60% of Rain for ₹540 crore; the retained 20% has a fair value of ₹180 crore and gives significant influence. Compute the gain in consolidated profit or loss.',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Proceeds', 'Cash received', inr(540)],
              ['Fair value of retained interest', 'New cost of associate', inr(180)],
              ['NCI derecognised', 'Carrying amount', inr(120)],
              ['Less net assets and goodwill derecognised', '600 + 60', inr(660)],
              ['Gain in profit or loss', '540 + 180 + 120 − 660', inr(gain)]], title='Loss of control')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Consolidation adds together matching line items of the parent and its subsidiaries; eliminates the parent\'s investment against its share of each subsidiary\'s equity (with goodwill under Ind AS 103); and eliminates intra-group balances and transactions in full.',
            'Consolidation starts from the date control is obtained and ends when control is lost. Income and expenses are based on acquisition-date fair values (e.g. extra depreciation on fair value uplifts).',
            'Uniform accounting policies are applied; subsidiaries\' statements are adjusted if they differ. Reporting dates should be the same; if not, additional statements are prepared unless impracticable, and the difference cannot exceed three months, with adjustments for significant events.'],
          'Add across, cancel the investment, remove intra-group items.',
          'Fair value uplift on land stays in consolidated assets; on buildings it adds depreciation.'),
        C('c2', T2, [
            'Intra-group balances (loans, receivables, payables), income and expenses (sales, interest, dividends, management fees) are eliminated in full.',
            'Profits and losses on intra-group transactions recognised in assets such as inventory and PPE are eliminated in full. When the subsidiary is the seller (upstream), the elimination is shared between parent and NCI; when the parent is the seller (downstream), it is borne by the parent.',
            'Intra-group losses may indicate impairment that is recognised. Deferred tax arises on temporary differences from eliminating unrealised profits (Ind AS 12). Unrealised profit on PPE transfers is reduced through excess depreciation over the asset\'s life.'],
          'Profit only counts when the group sells to outsiders.',
          'Stock bought from a subsidiary at a mark-up carries hidden profit to remove.'),
        C('c3', T3, [
            'NCI is presented within equity, separately from the parent\'s owners\' equity. Profit or loss and each component of OCI are attributed to owners of the parent and NCI, even if this results in a deficit balance for NCI.',
            'Cumulative preference shares classified as equity held by NCI: the parent computes its share after adjusting for preference dividends, whether declared or not.',
            'When the parent\'s stake changes but control is kept, the change is an equity transaction: carrying amounts of controlling and non-controlling interests are adjusted, and any difference between the adjustment to NCI and consideration paid or received is recognised directly in equity attributable to the parent. No change to goodwill.'],
          'NCI is equity; trades with NCI stay in equity.',
          'Buying another 10% of a subsidiary creates no new goodwill.'),
        C('c4', T4, [
            'On loss of control, the parent derecognises the subsidiary\'s assets (including goodwill) and liabilities, and the carrying amount of NCI; recognises consideration received and any retained interest at fair value; reclassifies amounts in OCI to profit or loss or retained earnings as if the assets were disposed of; and recognises the resulting gain or loss in profit or loss.',
            'The retained interest\'s fair value becomes its initial carrying amount as an associate, joint venture or financial asset. Multiple arrangements may be treated as a single transaction when they are linked (designed together, interdependent).',
            'Other procedures: potential voting rights normally do not affect profit allocation; a change in investment entity status is accounted for prospectively.'],
          'Losing control is like selling everything and buying back the retained stake at fair value.',
          'Selling 60% of an 80% subsidiary realises a gain on the whole holding.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Year-end consolidation worksheet', 'role': 'Consolidation accountant',
             'situation': 'Three subsidiaries with intra-group trading and loans.',
             'steps': ['Align policies and reporting dates.', 'Eliminate investment and compute goodwill.', 'Remove intra-group balances and unrealised profits.', 'Allocate profit and OCI to NCI.'],
             'takeaway': 'A clean elimination schedule makes the consolidation reconcile.'}]

    mcqs = [
        Q('m1', 'Intra-group balances are eliminated:', ['In full', 'To the parent\'s share', 'To the NCI share', 'Not at all'], 0,
          'Full elimination regardless of ownership. In practice: match balances first.', 'c2', T2),
        Q('m2', 'Unrealised profit where the subsidiary sold to the parent is borne by:', ['Parent and NCI in proportion', 'Parent only', 'NCI only', 'Nobody'], 0,
          'Upstream sale affects subsidiary profit. In practice: adjust NCI share.', 'c2', T2),
        Q('m3', 'NCI is presented in the consolidated balance sheet:', ['Within equity, separately from parent\'s equity', 'As a liability', 'As a provision', 'Outside the balance sheet'], 0,
          'Ind AS 110 requirement. In practice: also in P&L attribution.', 'c3', T3),
        Q('m4', 'Buying additional shares from NCI without change of control is:', ['An equity transaction', 'A business combination', 'A gain or loss in P&L', 'Goodwill adjustment'], 0,
          'Difference goes to parent equity. In practice: no remeasurement.', 'c3', T3),
        Q('m5', 'On loss of control, a retained interest is measured at:', ['Fair value', 'Carrying amount', 'Cost', 'Nil'], 0,
          'Gain includes revaluation of retained interest. In practice: becomes associate cost.', 'c4', T4),
        Q('m6', 'The maximum gap between parent and subsidiary reporting dates is:', ['Three months', 'Six months', 'One month', 'Twelve months'], 0,
          'Adjust for significant events. In practice: prepare additional statements if practicable.', 'c1', T1),
        Q('m7', 'Losses attributable to NCI that exceed its equity are:', ['Still allocated to NCI, giving a deficit', 'Absorbed by the parent', 'Ignored', 'Deferred'], 0,
          'Ind AS 110 allows deficits. In practice: disclose.', 'c3', T3),
        Q('m8', 'OCI of a subsidiary on loss of control is:', ['Reclassified as if the assets were disposed of', 'Left in equity always', 'Reversed', 'Moved to NCI'], 0,
          'Some to P&L, some to retained earnings. In practice: translation reserve recycles.', 'c4', T4),
    ]

    questions = [
        W('q1', 10, i1['q'], i1['solution'],
          [S('s1', 'Goodwill', 2, 'computation', 'goodwill', nums=[gw]), S('s2', 'URP', 2, 'computation', 'unrealised', nums=[urp]), S('s3', 'NCI', 3, 'computation', 'nci', nums=[nci]), S('s4', 'Reserves', 3, 'computation', 'reserves', nums=[res])],
          ['Show adjusted profit.'], ['Charging all URP to parent.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Inflows', 2, 'concept', 'proceeds|fair value'), S('s2', 'Derecognition', 2, 'concept', 'derecognis'), S('s3', 'Gain', 2, 'computation', 'gain', nums=[gain])],
          ['Include NCI.'], ['Ignoring retained interest.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What are the three basic consolidation steps?', 'Combine like items, eliminate the investment against the parent\'s share of equity with goodwill, and eliminate intra-group items in full.',
          [P('p1', 'Combine like items', 4, 'combine'), P('p2', 'Eliminate investment and intra-group', 6, 'eliminat')], 'c1'),
        V('v2', 'How is unrealised profit handled for upstream sales?', 'It is eliminated in full, with the reduction shared between parent and NCI in proportion to ownership.',
          [P('p1', 'Eliminated in full', 5, 'full'), P('p2', 'Shared with NCI', 5, 'nci')], 'c2'),
        V('v3', 'How are changes in ownership without loss of control treated?', 'As equity transactions: NCI and parent equity are adjusted, profit is unaffected and goodwill stays the same.',
          [P('p1', 'Equity transaction', 6, 'equity transaction'), P('p2', 'Goodwill same', 4, 'goodwill stays')], 'c3'),
        V('v4', 'What happens on loss of control?', 'The subsidiary\'s assets, liabilities, goodwill and NCI are derecognised, consideration and retained interest at fair value are recognised, OCI is reclassified, and the gain or loss goes to profit.',
          [P('p1', 'Derecognise', 5, 'derecognis'), P('p2', 'Retained at fair value', 5, 'fair value')], 'c4'),
        V('v5', 'Why are uniform accounting policies needed?', 'Because the group is presented as one entity, so like transactions must be accounted for alike across all members.',
          [P('p1', 'Single entity', 5, 'one entity'), P('p2', 'Like transactions', 5, 'like transactions')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Mira Group', 'difficulty': 'moderate',
              'case': 'Mira Ltd. owns 70% of Neo Ltd. Mira sold machinery to Neo for ₹60 crore (carrying amount ₹40 crore) at the start of the year; remaining life 5 years. Neo owes Mira ₹15 crore. Later, Mira buys another 10% of Neo from NCI for ₹35 crore when NCI\'s carrying amount for that 10% is ₹30 crore.',
              'mcqs': [
                  M('k1a', 'Unrealised profit at transfer (₹ crore):', ['20', '14', '6', '60'], 0,
                    '60 − 40 = 20, borne by parent (downstream). In practice: reduce PPE.', 'core', check=20, topic=T2),
                  M('k1b', 'Unrealised profit remaining at year end (₹ crore):', ['16', '20', '4', '12'], 0,
                    '20 − 20/5 = 16 via excess depreciation. In practice: realised over life.', 'moderate', check=16, topic=T2),
                  M('k1c', 'The ₹15 crore balance is:', ['Eliminated', 'Shown gross', 'Shown as NCI', 'Disclosed only'], 0,
                    'Intra-group balance. In practice: reconcile differences first.', 'core', topic=T2),
                  M('k1d', 'The ₹5 crore excess paid to NCI is debited to:', ['Parent\'s equity', 'Goodwill', 'Profit or loss', 'NCI'], 0,
                    'Equity transaction. In practice: no goodwill change.', 'moderate', topic=T3),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch13', 4, 'Ind AS 110: Consolidation Procedure for Subsidiaries',
                ['Combine statements, eliminate investments and compute goodwill.',
                 'Eliminate intra-group transactions and unrealised profit.',
                 'Account for NCI and ownership changes without loss of control.',
                 'Account for loss of control.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 50}, 'prereq': ['fin-p1-ch13-u03'],
                 'exam_tip': 'Prepare standard workings: net assets, goodwill, NCI, consolidated reserves, then the statements.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Combine, eliminate investment, eliminate intra-group items.',
                             'Upstream URP shared with NCI; downstream borne by parent.',
                             'NCI in equity; deficits allowed.',
                             'Ownership changes without loss of control: equity.',
                             'Loss of control: gain in P&L; retained at fair value.'],
                 'remember': ['Reporting date gap max three months.'],
                 'traps': ['Recognising goodwill on buying out NCI.']},
                [('Intra-group', 'Eliminate fully'), ('Upstream URP', 'Share with NCI'), ('Buy NCI', 'Equity'), ('Lose control', 'Gain in P&L')],
                viva, cases)
