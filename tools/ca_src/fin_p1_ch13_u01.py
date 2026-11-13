"""CA Final · Paper 1 Financial Reporting · Chapter 13 Unit 1 Introduction to Consolidated and Separate Financial Statements.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch13-u01'
T1 = 'Why groups prepare consolidated statements'
T2 = 'Consolidated versus separate statements'
T3 = 'The standards that make up group reporting'
T4 = 'Legal requirement in India'


def build():
    ck = Checks()
    rev = ck.add('500+300-50', 'Consolidated revenue (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Group revenue is not a simple sum', 'difficulty': 'core', 'minutes': 5,
          'q': 'Parent Ltd. reports revenue of ₹500 crore and its wholly owned subsidiary ₹300 crore. Parent sold goods of ₹50 crore to the subsidiary during the year. What is group revenue?',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Parent revenue', 'Separate statements', inr(500)],
              ['Subsidiary revenue', 'Separate statements', inr(300)],
              ['Less intra-group sales', 'The group cannot sell to itself', inr(50)],
              ['Consolidated revenue', '500 + 300 − 50', inr(rev)]], title='Single economic entity')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Which standard applies?', 'difficulty': 'core', 'minutes': 5,
          'q': 'Indicate the governing Ind AS for: (a) deciding whether Investor controls Target; (b) accounting for a 30% stake carrying significant influence in consolidated statements; (c) classifying a 50:50 arrangement as joint operation or joint venture; (d) measuring a subsidiary investment in the parent\'s own statements; (e) disclosures about interests in unconsolidated structured entities.',
          'solution': [table(['Item', 'Standard'], [
              ['(a)', 'Ind AS 110'], ['(b)', 'Ind AS 28 (equity method)'], ['(c)', 'Ind AS 111'],
              ['(d)', 'Ind AS 27 — cost, Ind AS 109 or equity method'], ['(e)', 'Ind AS 112']], title='Group standards map')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Many businesses operate through several companies. Looking only at the parent\'s own accounts hides the assets, debts and profits sitting in subsidiaries it controls.',
            'Consolidated statements combine the parent and its subsidiaries line by line, treating them as one economic entity, so investors and lenders see the whole group\'s resources and results.',
            'Restructurings, holding company structures and tax or operational reasons often create layers of entities — making group statements essential for a fair picture.'],
          'One group, one set of numbers.',
          'A parent with a thin balance sheet may control billions through subsidiaries.'),
        C('c2', T2, [
            'Consolidated statements present the group\'s assets, liabilities, equity, income, expenses and cash flows as if it were a single entity, eliminating intra-group transactions and balances.',
            'Separate statements are the parent\'s (or investor\'s) own statements, in which investments in subsidiaries, joint ventures and associates are carried at cost, under Ind AS 109, or using the equity method.',
            'Both may be presented; consolidated statements are not a substitute for separate statements under company law, and separate statements do not replace consolidation.'],
          'Consolidated is the group view; separate is the parent\'s own view.',
          'Dividends from a subsidiary are income in separate accounts but eliminated in consolidated accounts.'),
        C('c3', T3, [
            'Ind AS 110 sets the control test and consolidation procedure for subsidiaries. Ind AS 111 classifies joint arrangements as joint operations or joint ventures. Ind AS 28 applies the equity method to associates and joint ventures.',
            'Ind AS 27 governs separate financial statements. Ind AS 112 sets disclosures about interests in subsidiaries, joint arrangements, associates and unconsolidated structured entities.',
            'Ind AS 103 covers how a subsidiary is first acquired; Ind AS 21 covers translating foreign subsidiaries.'],
          'Each relationship type has its own standard.',
          'A 30% stake with board seats points to Ind AS 28.'),
        C('c4', T4, [
            'Under section 129(3) of the Companies Act, 2013, a company with one or more subsidiaries, associates or joint ventures must prepare consolidated financial statements in the same form and manner as its own, in addition to its standalone statements.',
            'The Companies (Accounts) Rules provide limited exemptions, for example certain intermediate wholly owned or partly owned subsidiaries whose parent prepares consolidated statements, subject to conditions.',
            'Listed entities must also publish consolidated results under SEBI requirements.'],
          'Law makes consolidation compulsory for most groups.',
          'A listed company with one associate still prepares consolidated accounts.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Planning a group close', 'role': 'Group reporting trainee',
             'situation': 'The group has 6 subsidiaries, 2 associates and a joint venture.',
             'steps': ['Map each entity to its relationship and standard.', 'Collect reporting packs with intra-group balances.', 'Prepare separate and consolidated statements.', 'Draft Ind AS 112 disclosures.'],
             'takeaway': 'A clear group chart drives the whole consolidation.'}]

    mcqs = [
        Q('m1', 'Consolidated statements present a group as:', ['A single economic entity', 'Separate legal entities', 'A partnership', 'A branch'], 0,
          'Line-by-line combination. In practice: eliminate intra-group items.', 'c2', T2),
        Q('m2', 'In separate statements, investments in subsidiaries may be measured:', ['At cost, under Ind AS 109, or by equity method', 'Only at fair value', 'Only at cost', 'Not at all'], 0,
          'Ind AS 27 allows a choice. In practice: apply per category.', 'c2', T2),
        Q('m3', 'The control test is found in:', ['Ind AS 110', 'Ind AS 28', 'Ind AS 27', 'Ind AS 112'], 0,
          'Ind AS 110 defines control. In practice: three elements.', 'c3', T3),
        Q('m4', 'The equity method is prescribed by:', ['Ind AS 28', 'Ind AS 110', 'Ind AS 111', 'Ind AS 27'], 0,
          'For associates and joint ventures. In practice: one-line consolidation.', 'c3', T3),
        Q('m5', 'The Companies Act requirement for consolidated statements is in:', ['Section 129(3)', 'Section 133', 'Section 135', 'Section 186'], 0,
          'Applies to companies with subsidiaries, associates or JVs. In practice: rules give exemptions.', 'c4', T4),
        Q('m6', 'Intra-group sales are:', ['Eliminated on consolidation', 'Added twice', 'Shown as other income', 'Ignored in separate statements'], 0,
          'The group cannot trade with itself. In practice: also eliminate unrealised profit.', 'c1', T1),
        Q('m7', 'Disclosures about unconsolidated structured entities are in:', ['Ind AS 112', 'Ind AS 110', 'Ind AS 27', 'Ind AS 24'], 0,
          'Ind AS 112 covers interests in other entities. In practice: risks are disclosed.', 'c3', T3),
        Q('m8', 'Dividend from a subsidiary is, in consolidated statements:', ['Eliminated', 'Income', 'Revenue', 'OCI'], 0,
          'It is an internal transfer. In practice: income in separate statements.', 'c2', T2),
    ]

    questions = [
        W('q1', 3, i1['q'], i1['solution'],
          [S('s1', 'Elimination', 1.5, 'concept', 'intra-group'), S('s2', 'Revenue', 1.5, 'computation', 'consolidated', nums=[rev])],
          ['Explain elimination.'], ['Adding all revenue.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Ind AS 110 and 28', 2, 'concept', '110|28'), S('s2', 'Ind AS 111 and 27', 2, 'concept', '111|27'), S('s3', 'Ind AS 112', 1, 'concept', '112')],
          ['One standard each.'], ['Confusing 27 and 28.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Why are consolidated statements needed?', 'Because the parent controls resources held in subsidiaries, and only a combined single-entity view shows the group\'s full position and results.',
          [P('p1', 'Control of subsidiaries', 5, 'control'), P('p2', 'Single entity view', 5, 'single')], 'c1'),
        V('v2', 'What are separate financial statements?', 'An entity\'s own statements in which investments in subsidiaries, joint ventures and associates are carried at cost, under Ind AS 109 or by the equity method.',
          [P('p1', 'Own statements', 5, 'own'), P('p2', 'Cost or Ind AS 109', 5, 'cost|109')], 'c2'),
        V('v3', 'Which standards make up group reporting?', 'Ind AS 110, 111, 28, 27 and 112, supported by Ind AS 103 and 21.',
          [P('p1', '110, 111, 28', 5, '110|111|28'), P('p2', '27 and 112', 5, '27|112')], 'c3'),
        V('v4', 'What does section 129(3) require?', 'A company with subsidiaries, associates or joint ventures must also prepare consolidated statements in the same form as its own.',
          [P('p1', 'Subsidiaries, associates, JVs', 5, 'subsidiar|associate'), P('p2', 'Consolidated statements', 5, 'consolidated')], 'c4'),
        V('v5', 'What happens to intra-group transactions on consolidation?', 'They are eliminated in full along with related balances and unrealised profits.',
          [P('p1', 'Eliminated', 6, 'eliminat'), P('p2', 'Unrealised profits', 4, 'unrealised')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Rana Group', 'difficulty': 'core',
              'case': 'Rana Ltd. owns 100% of Sun Ltd. and 35% of Moon Ltd. (significant influence). During the year Sun paid a dividend of ₹20 crore to Rana, and Rana lent ₹50 crore to Sun.',
              'mcqs': [
                  M('k1a', 'In Rana\'s separate statements, the dividend from Sun is:', ['Income', 'Eliminated', 'Reserve', 'OCI'], 0,
                    'Separate statements show it as income. In practice: eliminated in consolidation.', 'core', topic=T2),
                  M('k1b', 'In consolidated statements, the ₹50 crore loan is:', ['Eliminated', 'Shown as asset and liability', 'Shown as equity', 'Disclosed only'], 0,
                    'Intra-group balances cancel. In practice: interest also eliminated.', 'core', topic=T2),
                  M('k1c', 'Moon Ltd. is accounted for in consolidated statements by:', ['The equity method', 'Line-by-line consolidation', 'Cost', 'Fair value'], 0,
                    'Associate under Ind AS 28. In practice: one line.', 'core', topic=T3),
                  M('k1d', 'Rana must prepare consolidated statements because of:', ['Section 129(3) of the Companies Act', 'SEBI only', 'Voluntary choice', 'Income tax law'], 0,
                    'It has a subsidiary and an associate. In practice: listed entities also file quarterly.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch13', 1, 'Introduction to Consolidated and Separate Financial Statements',
                ['Explain why groups prepare consolidated statements.',
                 'Distinguish consolidated and separate statements.',
                 'Map group relationships to Ind AS 110, 111, 28, 27 and 112.',
                 'State the Companies Act requirement.'],
                {'difficulty': 'core', 'minutes': {'learn': 15, 'practice': 10}, 'prereq': ['fin-p1-ch12-u01'],
                 'exam_tip': 'Before any consolidation, draw the group chart and label each entity with its standard.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Consolidated: group as single entity.',
                             'Separate: investor\'s own statements.',
                             'Ind AS 110 control; 111 joint arrangements; 28 equity method.',
                             'Ind AS 27 separate; 112 disclosures.',
                             'Section 129(3) makes consolidation compulsory.'],
                 'remember': ['Eliminate intra-group items.'],
                 'traps': ['Treating consolidated statements as a substitute for standalone.']},
                [('Ind AS 110', 'Control'), ('Ind AS 111', 'Joint arrangements'), ('Ind AS 28', 'Equity method'), ('Ind AS 27', 'Separate statements')],
                viva, cases)
