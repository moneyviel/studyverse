"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 10 Unit 1 — AS 21 Consolidated Financial Statements.
Scope follows the ICAI study material (single subsidiary); explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch10-u01'
T1 = 'Parent, subsidiary, control and scope of consolidation'
T2 = 'Cost of control: goodwill or capital reserve'
T3 = 'Minority interest and pre/post-acquisition profits'
T4 = 'Eliminating intra-group items and unrealised profit'
T5 = 'Reporting dates, uniform policies and presentation'


def build():
    ck = Checks()
    na = ck.add('800000+200000', 'Net assets of S at acquisition (₹)')
    sh = ck.add('1000000*80/100', 'Parent\'s share of net assets (₹)')
    gw = ck.add('1000000-800000', 'Goodwill (₹)')
    post = ck.add('300000-200000', 'Post-acquisition profit of S (₹)')
    grp = ck.add('100000*80/100', 'Parent\'s share of post-acquisition profit (₹)')
    mi = ck.add('(800000+300000)*20/100', 'Minority interest at year end (₹)')
    i1 = {'id': 'i1', 'title': 'Goodwill and minority interest', 'difficulty': 'core', 'minutes': 9,
          'q': 'H Ltd. bought 80% of S Ltd. for ₹10,00,000 on 1 April 2026, when S had share capital ₹8,00,000 and reserves ₹2,00,000. On 31 March 2027 S\'s reserves are ₹3,00,000. Compute goodwill, the group\'s share of post-acquisition profit and minority interest.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Net assets of S at acquisition', '8,00,000 + 2,00,000', inr(na)],
              ['H\'s share (80%)', '', inr(sh)],
              ['Goodwill', 'Cost 10,00,000 − 8,00,000', inr(gw)],
              ['Post-acquisition profit of S', '3,00,000 − 2,00,000', inr(post)],
              ['H\'s share to consolidated reserves', '80%', inr(grp)],
              ['Minority interest', '20% × (8,00,000 + 3,00,000)', inr(mi)]], title='AS 21 basics')],
          'checks': list(ck)}

    ck2 = Checks()
    up = ck2.add('100000*25/125', 'Unrealised profit in H\'s closing stock (₹)')
    hsh = ck2.add('20000*80/100', 'Borne by the group (80%) (₹)')
    msh = ck2.add('20000*20/100', 'Borne by minority (20%) (₹)')
    i2 = {'id': 'i2', 'title': 'Unrealised profit on upstream sales', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'S Ltd. (80% held by H Ltd.) sells goods to H at cost plus 25%. At year end H holds such goods invoiced at ₹1,00,000. H also owes S ₹40,000 for these purchases. Show the consolidation adjustments.',
          'solution': [table(['Adjustment', 'Working', '₹'], [
              ['Unrealised profit in stock', '1,00,000 × 25/125', inr(up)],
              ['Reduce consolidated stock', '', inr(up)],
              ['Charge to group reserves (upstream, 80%)', '', inr(hsh)],
              ['Charge to minority interest (20%)', '', inr(msh)],
              ['Intra-group payable/receivable', 'Cancel both sides', inr(40000)]], title='Eliminations'),
              note('For downstream sales (parent to subsidiary) the whole unrealised profit is removed from the parent\'s profit.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Consolidated financial statements present a parent and its subsidiaries as a single economic entity. A parent presenting them must consolidate all subsidiaries, domestic and foreign.',
            'Control means owning, directly or through subsidiaries, more than half the voting power of an enterprise, or controlling the composition of its board (or governing body) so as to obtain economic benefits from its activities.',
            'A subsidiary is excluded from consolidation if control is intended to be temporary — it was bought and is held only to be sold in the near future — or if tough long-lasting restrictions seriously limit its ability to send funds to the parent. Such investments are accounted for under AS 13.',
            'Consolidated statements usually include a consolidated balance sheet, statement of profit and loss, cash flow statement and notes, in the same format as the parent\'s separate statements.'],
          'Control, not legal form, decides who is in the group.',
          'A company holding 45% of shares but appointing a majority of the board controls the investee.'),
        C('c2', T2, [
            'On consolidation, the parent\'s cost of investment is eliminated against its share of the subsidiary\'s equity at the date of investment.',
            'Excess of cost over that share of equity is goodwill; a shortfall is capital reserve. Where shares are bought at different dates, the comparison is made on each date (step-by-step), though ICAI\'s scope here is a single acquisition.',
            'Equity at acquisition includes share capital and reserves (and the balance of profit and loss) existing at that date. Dividends received out of pre-acquisition profits reduce the cost of investment.'],
          'Goodwill is what the parent paid above its share of the subsidiary\'s worth on day one.',
          'Paying ₹9 lakh for 60% of net assets of ₹16 lakh creates a capital reserve of ₹0.6 lakh.'),
        C('c3', T3, [
            'Minority interest is the part of a subsidiary\'s net results and net assets belonging to shareholders other than the parent (directly or through other subsidiaries).',
            'In the consolidated balance sheet it is shown separately from liabilities and parent shareholders\' equity; it equals the minority\'s share of equity at acquisition plus its share of movements in equity since.',
            'The minority\'s share of profit for the year is deducted from group profit to arrive at profit attributable to the parent\'s owners.',
            'Losses applicable to the minority that exceed its interest in equity are absorbed by the parent unless the minority has a binding obligation and is able to make good the losses. Later profits go to the parent until those losses are recovered.',
            'Profits of the subsidiary before acquisition are capital profits (part of cost of control); profits after acquisition are revenue profits shared between group and minority.'],
          'Outside shareholders own a slice of the subsidiary, shown on its own line.',
          'With 75% ownership, a subsidiary\'s profit of ₹20 lakh adds ₹15 lakh to group profit and ₹5 lakh to minority interest.'),
        C('c4', T4, [
            'Intra-group balances (debtors and creditors, loans, bills) and intra-group transactions (sales, purchases, interest, dividends, management fees) are eliminated in full.',
            'Unrealised profits on intra-group transfers still held in inventory or fixed assets at the year end are eliminated in full. In upstream transactions (subsidiary to parent), ICAI shares the elimination between the group and minority in proportion to holding; in downstream transactions (parent to subsidiary), it is removed from the parent\'s profit in full.',
            'Unrealised losses are eliminated too, unless the cost cannot be recovered.',
            'Revaluation of the subsidiary\'s assets at acquisition is shared between parent (capital profit) and minority, with additional depreciation adjusted after acquisition.'],
          'The group cannot trade with itself at a profit.',
          'Parent sells goods to its subsidiary at a ₹10,000 margin, still unsold: the ₹10,000 is removed from consolidated profit.'),
        C('c5', T5, [
            'Statements of the parent and subsidiaries are usually prepared to the same date. If not, adjustments are made for significant transactions between the dates, and the difference must not exceed six months.',
            'Uniform accounting policies are used for like transactions. If not practicable, the fact is disclosed with the proportions of items to which different policies were applied.',
            'Results of a subsidiary are included from the date control begins and up to the date it ends. On disposal, the difference between proceeds and the carrying amount of net assets is recognised in the consolidated profit and loss.'],
          'Consolidate on the same date and the same rules, as far as possible.',
          'A subsidiary with a December year end can be consolidated into a March-end parent with adjustments, as the gap is within six months.'),
    ]

    jobs = [{'id': 'j1', 'title': 'First-year consolidation', 'role': 'Reporting analyst',
             'situation': 'Your company has bought 70% of a supplier during the year and must present consolidated statements.',
             'steps': ['Fix acquisition-date equity and compute goodwill.', 'Split profits into pre- and post-acquisition.', 'Eliminate intra-group sales, balances and unrealised profits.', 'Compute minority interest.'],
             'takeaway': 'Cost of control, minority interest and eliminations are the three pillars.'}]

    mcqs = [
        Q('m1', 'Control under AS 21 exists when the parent:', ['Owns more than half the voting power or controls the board composition', 'Owns 20% or more of shares', 'Has a common director', 'Is the main customer'], 0,
          'AS 21 defines control as ownership of more than half the voting power, directly or through subsidiaries, or control of the composition of the board so as to obtain economic benefits. Significant influence at 20% concerns associates. In practice: check board rights too.', 'c1', T1),
        Q('m2', 'A subsidiary is excluded from consolidation when:', ['Control is intended to be temporary as it is held for disposal in the near future', 'Its business is different from the parent\'s', 'It makes losses', 'It is located abroad'], 0,
          'Exclusions are temporary control (bought and held only for near-term disposal) and severe long-term restrictions on transferring funds. Different business or losses are not grounds. In practice: account for excluded ones under AS 13.', 'c1', T1),
        Q('m3', 'Cost of investment ₹12 lakh for 75% of a subsidiary whose net assets are ₹14 lakh at acquisition. Goodwill:', ['₹1.5 lakh', '₹2 lakh', '₹3.5 lakh', 'Capital reserve ₹0.5 lakh'], 0,
          'Parent\'s share of net assets = 75% × ₹14 lakh = ₹10.5 lakh; cost ₹12 lakh exceeds it by ₹1.5 lakh, which is goodwill. In practice: compare at the acquisition date.', 'c2', T2, 'moderate', check=1.5),
        Q('m4', 'Dividend received by the parent out of the subsidiary\'s pre-acquisition profits is:', ['Deducted from the cost of investment', 'Credited to consolidated profit', 'Credited to minority interest', 'Ignored'], 0,
          'Pre-acquisition profits belong to what the parent paid for, so dividends from them are a return of cost and reduce the investment, affecting goodwill. In practice: trace the profit period.', 'c2', T2),
        Q('m5', 'Minority interest in the consolidated balance sheet is shown:', ['Separately from liabilities and from the parent\'s shareholders\' equity', 'As a current liability', 'As part of reserves', 'Deducted from assets'], 0,
          'AS 21 presents minority interest as a separate item, distinct from liabilities and from the equity of the parent\'s shareholders. In practice: show its share of profit in the P&L too.', 'c3', T3),
        Q('m6', 'Subsidiary\'s post-acquisition profit ₹10 lakh; parent holds 60%. Minority share:', ['₹4 lakh', '₹6 lakh', '₹10 lakh', '₹1.6 lakh'], 0,
          'The minority owns 40%, so its share of post-acquisition profit is ₹4 lakh, added to minority interest; the parent\'s ₹6 lakh goes to consolidated reserves. In practice: compute after eliminations.', 'c3', T3, 'core', check=4),
        Q('m7', 'Intra-group sales and purchases are:', ['Eliminated in full', 'Eliminated to the extent of the parent\'s holding', 'Kept in full', 'Shown as other income'], 0,
          'AS 21 eliminates intra-group balances and transactions in full, regardless of the percentage held, since the group cannot sell to itself. In practice: reconcile intra-group accounts first.', 'c4', T4),
        Q('m8', 'Parent sells goods costing ₹80,000 to its subsidiary for ₹1,00,000; all unsold at year end. Unrealised profit eliminated:', ['₹20,000 in full from the parent\'s profit', '₹16,000', '₹4,000', 'Nil'], 0,
          'This is a downstream sale; the whole unrealised profit of ₹20,000 is removed from the parent\'s profit and from consolidated inventory, whatever the holding. In practice: track stock at year end.', 'c4', T4, 'moderate'),
        Q('m9', 'The maximum difference between the reporting dates of parent and subsidiary is:', ['Six months', 'Three months', 'Nine months', 'One year'], 0,
          'Where reporting dates differ, adjustments are made for significant events, but the difference must not exceed six months. In practice: subsidiaries often prepare special statements.', 'c5', T5),
        Q('m10', 'Losses of a subsidiary attributable to the minority that exceed the minority\'s equity are:', ['Absorbed by the parent unless the minority has a binding obligation and ability to make good', 'Shown as a negative minority interest always', 'Ignored', 'Charged to goodwill'], 0,
          'AS 21 allocates such excess losses to the parent, except where the minority is bound and able to make them good; later profits go to the parent until the losses are recovered. In practice: track the recovery.', 'c3', T3),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Goodwill', 2, 'computation', 'goodwill', nums=[gw]),
           S('s2', 'Post-acquisition profit split', 2, 'computation', 'post-acquisition', nums=[post, grp]),
           S('s3', 'Minority interest', 2, 'computation', 'minority', nums=[mi])],
          ['Separate pre- and post-acquisition.'], ['Including pre-acquisition reserves in consolidated reserves.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Unrealised profit', 2, 'computation', '25/125', nums=[up]),
           S('s2', 'Upstream sharing', 1, 'computation', 'minority', nums=[hsh, msh]),
           S('s3', 'Cancel balances', 1, 'concept', 'cancel|eliminat')],
          ['Use margin on selling price.'], ['Using 25% of selling price.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is control under AS 21?', 'Ownership of more than half the voting power of an enterprise, directly or through subsidiaries, or control over the composition of its board to obtain economic benefits.',
          [P('p1', 'More than half', 5, 'half'), P('p2', 'Board composition', 5, 'board|composition')], 'c1'),
        V('v2', 'How is goodwill on consolidation computed?', 'As the excess of the parent\'s cost of investment over its share of the subsidiary\'s equity on the date of investment; a shortfall is capital reserve.',
          [P('p1', 'Cost over share of equity', 6, 'cost', 'equity'), P('p2', 'Capital reserve', 4, 'capital reserve')], 'c2'),
        V('v3', 'What is minority interest?', 'The portion of a subsidiary\'s net results and net assets that belongs to shareholders other than the parent and its subsidiaries.',
          [P('p1', 'Results and net assets', 5, 'net assets|results'), P('p2', 'Not owned by parent', 5, 'other than|outside')], 'c3'),
        V('v4', 'When may a subsidiary be excluded from consolidation?', 'When control is temporary because it is held only for near-term disposal, or it faces severe long-term restrictions on transferring funds to the parent.',
          [P('p1', 'Temporary control', 5, 'temporary'), P('p2', 'Severe restrictions', 5, 'restriction')], 'c1'),
        V('v5', 'How are unrealised profits on intra-group stock treated?', 'They are eliminated from consolidated inventory and profit; upstream eliminations are shared with the minority, downstream ones fall wholly on the parent.',
          [P('p1', 'Eliminated', 5, 'eliminat'), P('p2', 'Upstream/downstream', 5, 'upstream|downstream')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Prabhat Ltd. group', 'difficulty': 'moderate',
              'case': 'Prabhat Ltd. bought 90% of Sandhya Ltd. for ₹27 lakh when Sandhya had capital ₹20 lakh and reserves ₹5 lakh. At the year end Sandhya\'s reserves are ₹9 lakh. Prabhat owes Sandhya ₹3 lakh.',
              'mcqs': [
                  M('k1a', 'Goodwill on consolidation:', ['₹4.5 lakh', '₹2 lakh', '₹7 lakh', '₹0.5 lakh'], 0,
                    'Prabhat\'s share of net assets at acquisition = 90% × ₹25 lakh = ₹22.5 lakh; cost ₹27 lakh − ₹22.5 lakh = ₹4.5 lakh goodwill. In practice: post-acquisition reserves do not affect it.', 'core', check=4.5, topic=T2),
                  M('k1b', 'Minority interest at year end:', ['₹2.9 lakh', '₹2.5 lakh', '₹0.9 lakh', '₹2.6 lakh'], 0,
                    'Minority owns 10% of closing net assets (₹20 + 9 = ₹29 lakh) = ₹2.9 lakh, including its share of post-acquisition profit. In practice: show it separately.', 'moderate', check=2.9, topic=T3),
                  M('k1c', 'The ₹3 lakh owed by Prabhat to Sandhya is:', ['Eliminated from both consolidated payables and receivables', 'Shown as a receivable', 'Reduced by 10% for minority', 'Added to goodwill'], 0,
                    'Intra-group balances are cancelled in full on consolidation, as the group cannot owe money to itself. In practice: reconcile any cash in transit first.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch10', 1, 'Accounting Standard 21 Consolidated Financial Statements',
                ['Identify control and the scope of consolidation.',
                 'Compute goodwill or capital reserve on acquisition.',
                 'Compute minority interest and split pre- and post-acquisition profits.',
                 'Eliminate intra-group balances, transactions and unrealised profits.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 50}, 'prereq': ['int-p1-ch09-u02'],
                 'exam_tip': 'Prepare four workings: analysis of the subsidiary\'s profits, cost of control, minority interest and consolidated reserves.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Control: > half votes or board control; exclude temporary or restricted subsidiaries.',
                             'Goodwill = cost − share of equity at acquisition; shortfall = capital reserve.',
                             'Minority interest shown separately; excess losses borne by parent.', 'Eliminate intra-group items in full; upstream profit shared, downstream on parent.',
                             'Reporting dates within six months; uniform policies.'],
                 'remember': ['Pre-acquisition dividends reduce cost of investment.'],
                 'traps': ['Do not add pre-acquisition reserves to group reserves.']},
                [('Control', '> 50% votes / board'), ('Goodwill', 'Cost − share of equity'), ('Reporting gap', '≤ 6 months')],
                viva, cases)
