"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 10 Unit 3 — AS 27 Financial Reporting of Interests in Joint Ventures.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch10-u03'
T1 = 'Joint venture, joint control and its forms'
T2 = 'Jointly controlled operations and assets'
T3 = 'Jointly controlled entities: proportionate consolidation'
T4 = 'Transactions between a venturer and the joint venture'
T5 = 'Exceptions, operators and disclosure'


def build():
    ck = Checks()
    a = ck.add('500*40/100', 'Share of assets (₹ lakh)')
    l = ck.add('200*40/100', 'Share of liabilities (₹ lakh)')
    r = ck.add('300*40/100', 'Share of revenue (₹ lakh)')
    e = ck.add('220*40/100', 'Share of expenses (₹ lakh)')
    p = ck.add('120-88', 'Share of profit (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Proportionate consolidation', 'difficulty': 'core', 'minutes': 7,
          'q': 'Gaurav Ltd. holds 40% of a jointly controlled entity whose assets are ₹500 lakh, liabilities ₹200 lakh, revenue ₹300 lakh and expenses ₹220 lakh. What does Gaurav include in its consolidated statements?',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Assets', '40% × 500', R(a)],
              ['Liabilities', '40% × 200', R(l)],
              ['Revenue', '40% × 300', R(r)],
              ['Expenses', '40% × 220', R(e)],
              ['Share of profit', '120 − 88', R(p)]], title='AS 27 — proportionate consolidation'),
              note('The investment in the JV in Gaurav\'s books is eliminated against its share of the JV\'s equity, any difference being goodwill or capital reserve.')],
          'checks': list(ck)}

    ck2 = Checks()
    g = ck2.add('16-10', 'Gain on sale to the JV (₹ lakh)')
    rec = ck2.add('6*70/100', 'Gain recognised — share of other venturers (₹ lakh)')
    de = ck2.add('6*30/100', 'Gain eliminated — own share (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Selling an asset to the joint venture', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Harsh Ltd. holds 30% of a jointly controlled entity and sells it a machine with carrying amount ₹10 lakh for ₹16 lakh. The JV still holds the machine. How much gain does Harsh recognise in its consolidated statements?',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Total gain', '16 − 10', R(g)],
              ['Recognised (other venturers\' 70%)', '70% × 6', R(rec)],
              ['Not recognised (own 30%)', '30% × 6', R(de)]], title='Venturer–JV transaction'),
              note('Had the sale shown a loss that indicated impairment of the machine, the full loss would be recognised.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A joint venture is a contractual arrangement under which two or more parties undertake an economic activity that is subject to joint control.',
            'Joint control means control of an activity that is shared by agreement in a contract; no single venturer can control it alone. The contract is what distinguishes a joint venture from an associate.',
            'AS 27 identifies three forms: jointly controlled operations, jointly controlled assets and jointly controlled entities.'],
          'In a joint venture, important decisions need everyone\'s agreement under a contract.',
          'Two firms building an aircraft, each making different parts and sharing revenue, have a joint venture without forming a company.'),
        C('c2', T2, [
            'Jointly controlled operations use each venturer\'s own assets and resources without a separate entity. Each venturer recognises the assets it controls, the liabilities and expenses it incurs, and its share of income from the joint sale of goods or services — in both its separate and consolidated statements.',
            'Jointly controlled assets are assets jointly owned or controlled, such as a pipeline or a property. Each venturer recognises its share of those assets (classified by nature), liabilities it has incurred, its share of joint liabilities, income from sale or use of its share of output with its share of expenses, and expenses it incurs on its interest.',
            'No adjustment or consolidation is needed for these two forms, since the venturer\'s own books already include the items.'],
          'Where there is no separate entity, each venturer records its own part directly.',
          'Three oil companies sharing a pipeline each show their share of the pipeline as PPE.'),
        C('c3', T3, [
            'A jointly controlled entity is a separate vehicle — a company, firm or other body — in which every venturer holds a stake.',
            'In the venturer\'s separate financial statements, the interest is accounted for as an investment under AS 13.',
            'In consolidated financial statements, the venturer uses proportionate consolidation: its share of each of the entity\'s assets, liabilities, income and expenses is combined line by line with similar items, or shown as separate line items.',
            'Procedures are similar to AS 21: eliminate the investment against the share of equity (goodwill or capital reserve), eliminate the share of intra-group balances and transactions, and use uniform policies. Assets and liabilities of the JV are not offset against other items unless a legal right exists.'],
          'Take your slice of every line in the JV\'s accounts.',
          'A 50% venturer adds half of the JV\'s debtors to its consolidated debtors.'),
        C('c4', T4, [
            'When a venturer contributes or sells assets to a joint venture, it recognises only the portion of any gain attributable to the other venturers, as long as the JV retains the assets and significant risks and rewards have passed. The full loss is recognised if the transaction gives evidence of reduced net realisable value or impairment.',
            'When a venturer buys assets from a joint venture, it does not recognise its share of the JV\'s profit on that sale until it resells the assets to an independent party. Losses are recognised immediately if they show impairment.'],
          'You cannot profit from selling to yourself — only the other venturers\' share counts.',
          'A 50% venturer selling land to its JV at a ₹20 lakh gain recognises ₹10 lakh.'),
        C('c5', T5, [
            'Proportionate consolidation is not used where the interest is acquired and held exclusively for disposal in the near future, or the JV operates under severe long-term restrictions impairing fund transfers; such interests are accounted for under AS 13.',
            'An operator or manager of a joint venture accounts for fees received as revenue under AS 9; the JV treats them as expenses.',
            'Disclose a list and description of interests in significant joint ventures with proportion of ownership; the totals of assets, liabilities, income and expenses coming from jointly controlled entities; contingent liabilities and capital commitments relating to JVs; and the venturer\'s share in them.'],
          'Exceptions and disclosures complete the picture.',
          'A venturer that manages a JV for a fee records the fee as revenue.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Consolidating a JV interest', 'role': 'Reporting analyst',
             'situation': 'Your company has a 50% joint venture company and a share in a jointly owned warehouse.',
             'steps': ['Classify each arrangement by form.', 'Record warehouse share directly in own books.', 'Proportionately consolidate the JV company in CFS.', 'Eliminate own share of gains on sales to the JV.'],
             'takeaway': 'The form of the joint venture decides the accounting.'}]

    mcqs = [
        Q('m1', 'The feature that distinguishes a joint venture from an associate is:', ['A contractual arrangement establishing joint control', 'Holding of 20% or more', 'Board representation', 'Material transactions'], 0,
          'Joint control must rest on a contractual arrangement under which decisions need the agreement of the venturers. An associate involves only significant influence. In practice: read the shareholders\' agreement.', 'c1', T1),
        Q('m2', 'In consolidated statements, an interest in a jointly controlled entity is accounted for by:', ['Proportionate consolidation', 'Equity method', 'Cost method', 'Full consolidation'], 0,
          'AS 27 requires proportionate consolidation in consolidated statements, combining the venturer\'s share of each line item. The equity method applies to associates under AS 23. In practice: watch for exceptions.', 'c3', T3),
        Q('m3', 'In the venturer\'s separate statements, an interest in a jointly controlled entity is:', ['An investment under AS 13', 'Proportionately consolidated', 'Equity accounted', 'Not shown'], 0,
          'Separate statements show the interest as an investment under AS 13; proportionate consolidation applies only in consolidated statements. In practice: two different presentations.', 'c3', T3),
        Q('m4', 'In jointly controlled operations, each venturer recognises:', ['The assets it controls, liabilities and expenses it incurs, and its share of income', 'A share of a separate entity\'s net assets', 'Only an investment', 'Nothing until profits are distributed'], 0,
          'Without a separate entity, each venturer records its own assets, liabilities and expenses and its share of joint income directly in its own books. In practice: no consolidation adjustment is needed.', 'c2', T2),
        Q('m5', 'A venturer with 25% interest sells goods to the JV at a gain of ₹8 lakh, still held by the JV. Gain recognised:', ['₹6 lakh', '₹8 lakh', '₹2 lakh', 'Nil'], 0,
          'Only the portion attributable to other venturers (75% × ₹8 lakh = ₹6 lakh) is recognised; the venturer\'s own 25% is eliminated until the JV sells to outsiders. In practice: losses showing impairment are recognised fully.', 'c4', T4, 'moderate', check=6),
        Q('m6', 'When a venturer buys goods from the JV, it recognises its share of the JV\'s profit on that sale:', ['When it resells the goods to an independent party', 'Immediately', 'Never', 'When it pays the JV'], 0,
          'The venturer\'s share of profit on such a purchase is deferred until the goods are sold outside; immediate recognition would mean profiting from itself. In practice: adjust year-end inventory.', 'c4', T4),
        Q('m7', 'Proportionate consolidation is not applied when the JV interest is:', ['Held exclusively for disposal in the near future', 'More than 50%', 'In a partnership firm', 'Loss-making'], 0,
          'Temporary interests held for near-term disposal, and JVs under severe long-term restrictions on transferring funds, are accounted for under AS 13 instead. In practice: document the intention.', 'c5', T5),
        Q('m8', 'Fees received by a venturer for managing the joint venture are:', ['Revenue under AS 9', 'Deducted from its investment', 'Eliminated fully', 'Credited to reserves'], 0,
          'An operator or manager treats such fees as revenue under AS 9, while the JV treats them as expenses. In practice: proportionate consolidation may eliminate the venturer\'s share.', 'c5', T5),
        Q('m9', 'A jointly owned oil pipeline used by three companies is an example of:', ['Jointly controlled assets', 'A jointly controlled entity', 'Jointly controlled operations', 'An associate'], 0,
          'Assets jointly owned and used without a separate entity are jointly controlled assets; each venturer shows its share of the pipeline classified by nature. In practice: record it as PPE.', 'c2', T2),
        Q('m10', 'Which disclosure is required by AS 27?', ['Contingent liabilities and capital commitments relating to joint ventures', 'The other venturers\' profits', 'The JV\'s tax returns', 'The JV\'s share price'], 0,
          'Venturers disclose interests in significant JVs, aggregate assets, liabilities, income and expenses of jointly controlled entities, and related contingent liabilities and capital commitments. In practice: show own share separately.', 'c5', T5),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Share of assets and liabilities', 2, 'computation', 'assets', nums=[a, l]),
           S('s2', 'Share of revenue and expenses', 2, 'computation', 'revenue', nums=[r, e, p])],
          ['Apply the share line by line.'], ['Using the equity method.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Total gain', 1, 'computation', 'gain', nums=[g]),
           S('s2', 'Recognise other venturers\' share', 2, 'computation', 'other venturers', nums=[rec]),
           S('s3', 'Eliminate own share', 1, 'computation', 'own', nums=[de])],
          ['Split by ownership.'], ['Recognising the full gain.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is joint control?', 'Control of an activity shared under a contract, so that decisions need the venturers\' agreement and none controls alone.',
          [P('p1', 'Contractual sharing', 6, 'contract'), P('p2', 'Shared control', 4, 'shar')], 'c1'),
        V('v2', 'Name the three forms of joint venture.', 'Jointly controlled operations, jointly controlled assets and jointly controlled entities.',
          [P('p1', 'Operations', 3, 'operations'), P('p2', 'Assets', 3, 'assets'), P('p3', 'Entities', 4, 'entit')], 'c1'),
        V('v3', 'What is proportionate consolidation?', 'A method in which the venturer\'s share of each asset, liability, income and expense of the jointly controlled entity is combined with similar items or shown in separate lines.',
          [P('p1', 'Share of each item', 6, 'share'), P('p2', 'Combined line by line', 4, 'combin|line')], 'c3'),
        V('v4', 'How is a gain on selling assets to a JV treated?', 'Only the part attributable to the other venturers is recognised while the JV keeps the assets; the venturer\'s own share is eliminated.',
          [P('p1', 'Other venturers\' share', 6, 'other venturers'), P('p2', 'Own share eliminated', 4, 'eliminat')], 'c4'),
        V('v5', 'How does a venturer account for its JV interest in separate statements?', 'As an investment under AS 13.',
          [P('p1', 'Investment', 6, 'investment'), P('p2', 'AS 13', 4, 'as 13')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Indu Ltd.\'s joint ventures', 'difficulty': 'moderate',
              'case': 'Indu Ltd. has: (1) a 50% stake in a joint venture company that earned ₹40 lakh profit; (2) a one-third share in a jointly owned warehouse costing ₹90 lakh; (3) a 40% JV interest bought exclusively to sell within six months.',
              'mcqs': [
                  M('k1a', 'Indu\'s share of the JV company\'s profit in its CFS:', ['₹20 lakh, through proportionate consolidation', '₹40 lakh', '₹20 lakh via equity method', 'Nil'], 0,
                    'Proportionate consolidation adds 50% of the JV\'s revenue and expenses, so ₹20 lakh of profit enters the consolidated statements line by line. In practice: eliminate the investment too.', 'core', topic=T3),
                  M('k1b', 'Indu\'s share of the warehouse shown in its own books:', ['₹30 lakh', '₹90 lakh', '₹45 lakh', 'Nil'], 0,
                    'A jointly controlled asset is recognised by each venturer at its share: one-third of ₹90 lakh = ₹30 lakh, as PPE. In practice: depreciate it like owned assets.', 'core', check=30, topic=T2),
                  M('k1c', 'The 40% interest held for sale within six months is:', ['Accounted for under AS 13', 'Proportionately consolidated', 'Equity accounted', 'Fully consolidated'], 0,
                    'Interests held exclusively for near-term disposal are excluded from proportionate consolidation and accounted for under AS 13. In practice: show as a current investment.', 'moderate', topic=T5),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch10', 3, 'Accounting Standard 27 Financial Reporting of Interests in Joint Ventures',
                ['Identify joint control and the three forms of joint venture.',
                 'Account for jointly controlled operations and assets.',
                 'Apply proportionate consolidation for jointly controlled entities.',
                 'Account for venturer–JV transactions and give disclosures.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 30, 'practice': 25}, 'prereq': ['int-p1-ch10-u02'],
                 'exam_tip': 'Identify the form first; only jointly controlled entities need proportionate consolidation.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['JV: contractual joint control.', 'Operations and assets: record own share directly.',
                             'Entities: AS 13 in separate statements; proportionate consolidation in CFS.', 'Sales to JV: recognise only other venturers\' share of gain.',
                             'Purchases from JV: defer own share of profit until resale.', 'Exclusions follow AS 13; operator fees are revenue.'],
                 'remember': ['Losses showing impairment are recognised in full.'],
                 'traps': ['Do not use the equity method for JVs under AS 27.']},
                [('Form', 'Operations · Assets · Entities'), ('CFS method', 'Proportionate consolidation'), ('Separate FS', 'AS 13')],
                viva, cases)
