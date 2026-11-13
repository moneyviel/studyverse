"""CA Final · Paper 1 Financial Reporting · Chapter 13 Unit 5 Ind AS 111 Joint Arrangements.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch13-u05'
T1 = 'Identifying joint control'
T2 = 'Classifying: joint operation or joint venture'
T3 = 'Accounting by joint operators'
T4 = 'Accounting by joint venturers and other parties'


def build():
    ck = Checks()
    a = ck.add('500*0.4', 'Share of plant (₹ crore)')
    l = ck.add('200*0.4', 'Share of liabilities (₹ crore)')
    r = ck.add('300*0.4', 'Share of revenue (₹ crore)')
    e = ck.add('200*0.4', 'Share of expenses (₹ crore)')
    i1 = {'id': 'i1', 'title': 'A joint operation', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Alpha Ltd. and Beta Ltd. share joint control (40:60) of an unincorporated refinery arrangement. Each has rights to its share of the plant and output and is liable for its share of debts. The arrangement\'s plant is ₹500 crore, liabilities ₹200 crore, revenue ₹300 crore and expenses ₹200 crore. What does Alpha recognise?',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Classification', 'No separate vehicle; rights to assets, obligations for liabilities', 'Joint operation'],
              ['Share of plant', '40% × 500', inr(a)],
              ['Share of liabilities', '40% × 200', inr(l)],
              ['Share of revenue', '40% × 300', inr(r)],
              ['Share of expenses', '40% × 200', inr(e)]], title='Joint operator accounting')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Classifying arrangements', 'difficulty': 'hard', 'minutes': 8,
          'q': 'Classify: (a) a company jointly owned 50:50; its legal form shields owners from its liabilities and contracts give no rights to specific assets; (b) the same company, but owners must buy all output and their payments are its only source of cash; (c) two parties sharing a bridge construction contract with each building specific sections; (d) a 50:50 company where one party holds a casting vote.',
          'solution': [table(['Item', 'Classification', 'Reason'], [
              ['(a)', 'Joint venture', 'Separate vehicle with rights to net assets'],
              ['(b)', 'Joint operation', 'Other facts: parties take all output and fund liabilities'],
              ['(c)', 'Joint operation', 'Not structured through a separate vehicle'],
              ['(d)', 'Not a joint arrangement', 'Casting vote gives one party control']], title='Classification')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Ind AS 111 applies to all entities that are parties to a joint arrangement. A joint arrangement has two features: the parties are bound by a contractual arrangement, and that arrangement gives two or more of them joint control.',
            'To test joint control: first, does the contract give all the parties, or a group of them, collective control? Then, do decisions about relevant activities require the unanimous consent of the parties that collectively control it?',
            'An arrangement can be joint even if not all parties have joint control. A party with a casting vote or the ability to decide alone has control, not joint control.'],
          'Joint control = collective control + unanimity.',
          'Three parties with 50:30:20 and a rule needing 75% approval: the 50 and 30 share joint control only if they are the only combination that can reach 75%.'),
        C('c2', T2, [
            'Classification depends on rights and obligations. In a joint operation, each party owns its share of the assets and owes its share of the debts. A joint venture: parties have rights to the net assets.',
            'If no separate vehicle is used, the arrangement is automatically a joint operation. If structured through a separate vehicle, consider: the legal form of the vehicle (does it confer rights to assets and obligations to parties?); the contractual terms; and other facts and circumstances (e.g. parties take substantially all output and are the only source of cash, meaning they effectively fund liabilities).',
            'Classification is reassessed when facts and circumstances change.'],
          'No vehicle → joint operation; vehicle → look through legal form, contract and other facts.',
          'An output-sharing company funded only by its owners is a joint operation.'),
        C('c3', T3, [
            'A joint operator recognises, in relation to its interest: its assets (including its share of jointly held assets), its liabilities (including its share of joint liabilities), its revenue from selling its share of output, its share of revenue from sale of output by the operation, and its expenses including its share of joint expenses.',
            'These are accounted for under the relevant Ind AS — in both separate and consolidated statements.',
            'On sales by the operator to the joint operation, gains are recognised only to the extent of other parties\' interests; on purchases from the operation, the operator\'s share of gains is not recognised until resale to a third party. Acquisition of an interest in a joint operation that is a business applies Ind AS 103 principles.'],
          'Joint operators book their slices line by line.',
          'A 40% operator books 40% of the shared plant.'),
        C('c4', T4, [
            'A joint venturer recognises its interest as an investment and accounts for it using the equity method under Ind AS 28 (unless exempt). In separate statements, it applies Ind AS 27 (cost, Ind AS 109 or equity method).',
            'A participant in a joint operation who lacks joint control accounts like a joint operator if it has rights to assets and obligations for liabilities; otherwise by the relevant Ind AS.',
            'A party to a joint venture without joint control applies Ind AS 109, or Ind AS 28 if it has significant influence.'],
          'Joint venturers use one line — the equity method.',
          'A 50:50 company with net asset rights is equity-accounted by each owner.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Reviewing a JV agreement', 'role': 'Accounting policy analyst',
             'situation': 'The company signed a 50:50 agreement to set up a manufacturing company.',
             'steps': ['Confirm joint control from decision rules.', 'Check whether a separate vehicle exists.', 'Analyse legal form, contract terms and other facts.', 'Apply equity method or line-by-line share.'],
             'takeaway': 'Rights and obligations, not legal form alone, decide classification.'}]

    mcqs = [
        Q('m1', 'An arrangement not structured through a separate vehicle is:', ['A joint operation', 'A joint venture', 'A subsidiary', 'An associate'], 0,
          'Parties have direct rights. In practice: line-by-line share.', 'c2', T2),
        Q('m2', 'A joint venturer accounts for its interest using:', ['The equity method', 'Proportionate consolidation', 'Full consolidation', 'Cost only'], 0,
          'Ind AS 28 applies. In practice: one-line.', 'c4', T4),
        Q('m3', 'A party with a casting vote in a 50:50 company has:', ['Control', 'Joint control', 'Significant influence', 'Nothing'], 0,
          'It can decide alone. In practice: consolidate.', 'c1', T1),
        Q('m4', 'Parties taking substantially all output and being the only cash source suggests:', ['Joint operation', 'Joint venture', 'Subsidiary', 'Financial asset'], 0,
          'Other facts override legal form. In practice: they fund liabilities.', 'c2', T2),
        Q('m5', 'A joint operator recognises:', ['Its share of assets, liabilities, revenue and expenses', 'One investment line', 'Dividends only', 'Fair value changes'], 0,
          'Line-by-line in both statements. In practice: own assets too.', 'c3', T3),
        Q('m6', 'Joint control requires decisions about relevant activities to be:', ['Unanimous among parties sharing control', 'By majority', 'By the manager', 'By auditors'], 0,
          'Unanimity is essential. In practice: check agreement.', 'c1', T1),
        Q('m7', 'A party in a joint venture without joint control but with significant influence applies:', ['Ind AS 28', 'Ind AS 111 joint venturer rules', 'Ind AS 110', 'Ind AS 27 only'], 0,
          'Equity method as associate. In practice: else Ind AS 109.', 'c4', T4),
        Q('m8', 'Acquiring an interest in a joint operation that is a business applies:', ['Ind AS 103 principles', 'Ind AS 109', 'Ind AS 40', 'Ind AS 16 only'], 0,
          'Goodwill may arise. In practice: fair value share of assets.', 'c3', T3),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Classification', 1, 'concept', 'joint operation'), S('s2', 'Assets and liabilities', 2, 'computation', 'plant|liabilit', nums=[a, l]), S('s3', 'Revenue and expenses', 2, 'computation', 'revenue|expense', nums=[r, e])],
          ['Line by line.'], ['Using equity method.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'JV', 1.5, 'concept', 'joint venture'), S('s2', 'JO cases', 3, 'concept', 'joint operation'), S('s3', 'Control', 1.5, 'concept', 'casting|control')],
          ['Apply the steps.'], ['Relying only on legal form.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What are the features of a joint arrangement?', 'Parties are bound by a contractual arrangement that gives two or more of them joint control.',
          [P('p1', 'Contractual arrangement', 5, 'contractual'), P('p2', 'Joint control', 5, 'joint control')], 'c1'),
        V('v2', 'How is a joint arrangement classified?', 'By the parties\' rights and obligations: rights to assets and obligations for liabilities make it a joint operation; rights to net assets make it a joint venture.',
          [P('p1', 'Rights and obligations', 5, 'rights'), P('p2', 'Net assets', 5, 'net assets')], 'c2'),
        V('v3', 'Which factors are considered for a separate vehicle?', 'Its legal form, the terms of the contractual arrangement and other facts and circumstances.',
          [P('p1', 'Legal form', 4, 'legal form'), P('p2', 'Contract and other facts', 6, 'contract|facts')], 'c2'),
        V('v4', 'How does a joint operator account in separate statements?', 'The same as in consolidated statements — recognising its share of assets, liabilities, revenue and expenses.',
          [P('p1', 'Same treatment', 5, 'same'), P('p2', 'Share of items', 5, 'share')], 'c3'),
        V('v5', 'How does a joint venturer account?', 'It recognises an investment and applies the equity method under Ind AS 28.',
          [P('p1', 'Investment', 4, 'investment'), P('p2', 'Equity method', 6, 'equity method')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Delta–Echo arrangement', 'difficulty': 'moderate',
              'case': 'Delta Ltd. and Echo Ltd. form Fox Pvt Ltd. (50:50) to make components. All relevant decisions need both parties\' approval. Fox sells all output to Delta and Echo at cost, and they pay Fox\'s debts as needed. Delta sells raw materials to Fox for ₹20 crore at a profit of ₹4 crore; Fox still holds them.',
              'mcqs': [
                  M('k1a', 'Fox is best classified as:', ['A joint operation', 'A joint venture', 'A subsidiary of Delta', 'An associate'], 0,
                    'Parties take output and fund liabilities. In practice: other facts override legal form.', 'moderate', topic=T2),
                  M('k1b', 'Delta accounts for Fox by:', ['Recognising its 50% share of assets, liabilities, income and expenses', 'Equity method', 'Full consolidation', 'Cost'], 0,
                    'Joint operator accounting. In practice: both statements.', 'core', topic=T3),
                  M('k1c', 'Profit Delta recognises on the raw material sale (₹ crore):', ['2', '4', 'Nil', '20'], 0,
                    'Only to the extent of Echo\'s 50% interest. In practice: defer own share.', 'moderate', check=2, topic=T3),
                  M('k1d', 'If the agreement allowed Delta alone to decide, Fox would be:', ['A subsidiary of Delta', 'A joint venture', 'A joint operation', 'An associate of Echo'], 0,
                    'Sole decision power is control. In practice: consolidate.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch13', 5, 'Ind AS 111 "Joint Arrangements"',
                ['Identify joint control.',
                 'Classify joint arrangements as joint operations or joint ventures.',
                 'Account for interests in joint operations.',
                 'Account for interests in joint ventures and by non-controlling parties.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 25}, 'prereq': ['fin-p1-ch13-u04'],
                 'exam_tip': 'Use the decision steps: separate vehicle? legal form? contract? other facts?'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Joint control: collective control + unanimity.',
                             'JO: rights to assets, obligations for liabilities.',
                             'JV: rights to net assets.',
                             'JO: line-by-line share; JV: equity method.',
                             'Reassess classification when facts change.'],
                 'remember': ['Output-sharing vehicles can be joint operations.'],
                 'traps': ['Proportionate consolidation for joint ventures.']},
                [('No vehicle', 'JO'), ('Net assets', 'JV'), ('JO accounting', 'Share of items'), ('JV accounting', 'Equity method')],
                viva, cases)
