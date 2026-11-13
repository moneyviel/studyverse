"""CA Final · Paper 1 Financial Reporting · Chapter 13 Unit 2 Important Definitions.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch13-u02'
T1 = 'Control, power, parent and subsidiary'
T2 = 'Significant influence and associates'
T3 = 'Joint control, joint operations and joint ventures'
T4 = 'Group, NCI and statement types'


def build():
    ck = Checks()
    nci = ck.add('400*0.25', 'NCI share of subsidiary equity (₹ crore)')
    par = ck.add('400*0.75', 'Parent share (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Labelling each investee', 'difficulty': 'core', 'minutes': 7,
          'q': 'Kite Ltd. holds: 75% of A Ltd. (equity ₹400 crore); 30% of B Ltd. with two board seats; 50% of C Ltd. where all key decisions need both owners\' consent and C holds the net assets; 50% of D, an unincorporated arrangement where each party takes its share of output and liabilities; 12% of E Ltd. with no board seat. Classify each and compute NCI in A.',
          'solution': [table(['Investee', 'Classification', 'Note'], [
              ['A Ltd.', 'Subsidiary', 'NCI = 25% × 400 = ' + inr(nci) + '; parent share ' + inr(par)],
              ['B Ltd.', 'Associate', 'Significant influence through board seats'],
              ['C Ltd.', 'Joint venture', 'Joint control; rights to net assets'],
              ['D', 'Joint operation', 'Rights to assets and obligations for liabilities'],
              ['E Ltd.', 'Financial asset (Ind AS 109)', 'No control, joint control or influence']], title='Definitions applied')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Which statements are which?', 'difficulty': 'core', 'minutes': 5,
          'q': 'Identify the statement type: (a) Kite Ltd.\'s accounts in which A Ltd. is shown at cost; (b) Kite group accounts combining A Ltd. line by line; (c) accounts of an investor with only an associate, in which the associate is equity-accounted.',
          'solution': [table(['Item', 'Type'], [
              ['(a)', 'Separate financial statements'],
              ['(b)', 'Consolidated financial statements'],
              ['(c)', 'Not separate statements — equity-accounted financial statements of the investor']], title='Statement types')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Control exists when an investor both has exposure to, or rights over, returns that vary with the investee\'s performance and can use its power over the investee to affect the size of those returns.',
            'Power means currently held rights that let the investor direct the investee\'s relevant activities — those that significantly affect its returns.',
            'A parent is an entity that controls at least one other entity; a subsidiary is an entity controlled by another.'],
          'Power + variable returns + the link between them = control.',
          'Holding 60% of votes usually gives power.'),
        C('c2', T2, [
            'Significant influence is the ability to take part in decisions on the investee\'s financial and operating policies, stopping short of control or joint control.',
            'An associate is an investee over which the investor has significant influence. Holding 20% or more of voting power is presumed to give significant influence, unless clearly shown otherwise; under 20% is presumed not to, unless shown otherwise.',
            'Indicators include board representation, participation in policy-making, material transactions, interchange of managerial personnel and provision of essential technical information.'],
          'Influence is a seat at the table, not the casting vote.',
          'A 15% holder with a board seat may have significant influence.'),
        C('c3', T3, [
            'A joint arrangement is one that two or more parties control jointly. Joint control is contractually agreed sharing of control, which exists only when decisions on relevant activities need the unanimous agreement of the sharing parties.',
            'A joint operation gives the parties with joint control rights to the arrangement\'s assets and obligations for its liabilities. A joint venture gives those parties rights to the arrangement\'s net assets.',
            'A party to a joint arrangement who lacks joint control is accounted for by reference to its actual interest (e.g. its share of assets in a joint operation, or Ind AS 109 / Ind AS 28 for a venture).'],
          'Joint control needs unanimous consent; then ask: assets and liabilities, or net assets?',
          'A shared pipeline where each party takes its share of capacity is a joint operation.'),
        C('c4', T4, [
            'A group is a parent together with its subsidiaries. Non-controlling interest (NCI) is the equity in a subsidiary that does not belong, directly or indirectly, to the parent.',
            'Consolidated financial statements present the group\'s figures as those of one economic entity.',
            'Separate financial statements are those presented by a parent, or by an investor with joint control or significant influence, in which such investments are carried at cost, under Ind AS 109 or by the equity method.'],
          'NCI is the outside owners\' slice of a subsidiary.',
          'A 75%-owned subsidiary has 25% NCI.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Group structure review', 'role': 'Audit trainee',
             'situation': 'The client has nine investees with varied holdings and agreements.',
             'steps': ['Read shareholder agreements for decision rules.', 'Test control, joint control and significant influence.', 'Classify each investee.', 'Compute NCI percentages.'],
             'takeaway': 'Definitions applied correctly decide the accounting method.'}]

    mcqs = [
        Q('m1', 'Joint control exists only when decisions on relevant activities require:', ['Unanimous consent of the parties sharing control', 'A simple majority', 'The largest shareholder\'s approval', 'Board approval'], 0,
          'Unanimity defines joint control. In practice: read the agreement.', 'c3', T3),
        Q('m2', 'A joint venture gives parties rights to:', ['The net assets of the arrangement', 'Individual assets', 'Revenue only', 'Nothing'], 0,
          'Net assets distinguish ventures. In practice: equity method.', 'c3', T3),
        Q('m3', 'Holding 20% or more of voting power is presumed to give:', ['Significant influence', 'Control', 'Joint control', 'Nothing'], 0,
          'Rebuttable presumption. In practice: look at indicators.', 'c2', T2),
        Q('m4', 'Non-controlling interest is:', ['Equity in a subsidiary not attributable to the parent', 'The parent\'s share', 'A liability', 'Minority debt'], 0,
          'Presented within equity. In practice: 100% − parent\'s share.', 'c4', T4),
        Q('m5', 'Power is defined as:', ['Existing rights giving the current ability to direct relevant activities', 'Majority shareholding only', 'Board seats only', 'Past decisions'], 0,
          'Rights, not their exercise. In practice: potential votes may count.', 'c1', T1),
        Q('m6', 'A group consists of:', ['A parent and its subsidiaries', 'All investees', 'Associates and JVs', 'Related parties'], 0,
          'Associates are outside the group. In practice: equity-accounted.', 'c4', T4),
        Q('m7', 'A joint operation gives parties:', ['Rights to assets and obligations for liabilities', 'Rights to net assets', 'Dividends only', 'Nothing'], 0,
          'Parties account for their share. In practice: line-by-line share.', 'c3', T3),
        Q('m8', 'An investee in which a 12% holder has no influence is:', ['A financial asset under Ind AS 109', 'An associate', 'A subsidiary', 'A joint venture'], 0,
          'Below 20% with no indicators. In practice: FVTPL or FVOCI.', 'c2', T2),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Subsidiary and NCI', 2, 'computation', 'subsidiary|nci', nums=[nci]), S('s2', 'Associate', 1, 'concept', 'associate'), S('s3', 'JV and JO', 2, 'concept', 'joint'), S('s4', 'Financial asset', 1, 'concept', '109')],
          ['Classify each.'], ['Confusing JV and JO.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Separate', 1, 'concept', 'separate'), S('s2', 'Consolidated', 1, 'concept', 'consolidated'), S('s3', 'Equity-accounted', 1, 'concept', 'equity-accounted')],
          ['Name each.'], ['Calling (c) separate.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Define control.', 'An investor has control when it is exposed to or has rights over variable returns and can use its power over the investee to affect those returns.',
          [P('p1', 'Variable returns', 5, 'variable'), P('p2', 'Power', 5, 'power')], 'c1'),
        V('v2', 'Define significant influence.', 'The ability to take part in an investee\'s financial and operating policy decisions without controlling them alone or jointly.',
          [P('p1', 'Take part in decisions', 5, 'take part|decision'), P('p2', 'Policies', 5, 'polic')], 'c2'),
        V('v3', 'Distinguish a joint operation and a joint venture.', 'In a joint operation parties have rights to assets and obligations for liabilities; in a joint venture they have rights to net assets.',
          [P('p1', 'Assets and liabilities', 5, 'assets and obligations|liabilities'), P('p2', 'Net assets', 5, 'net assets')], 'c3'),
        V('v4', 'What is non-controlling interest?', 'The part of a subsidiary\'s equity owned by outsiders, that is, not attributable directly or indirectly to the parent.',
          [P('p1', 'Subsidiary equity', 5, 'equity'), P('p2', 'Not the parent\'s', 5, 'outsider')], 'c4'),
        V('v5', 'What are relevant activities?', 'Activities of the investee that significantly affect its returns.',
          [P('p1', 'Significantly affect', 6, 'significantly'), P('p2', 'Returns', 4, 'return')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Zeal Ltd.', 'difficulty': 'moderate',
              'case': 'Zeal Ltd. holds 55% of P Ltd., 22% of Q Ltd. (but a 60% holder ignores Zeal\'s views and Zeal has no board seat), 50% of R Ltd. under an agreement requiring unanimous decisions, and 18% of S Ltd. with two of seven board seats.',
              'mcqs': [
                  M('k1a', 'P Ltd. is a:', ['Subsidiary', 'Associate', 'Joint venture', 'Financial asset'], 0,
                    'Majority voting power usually gives control. In practice: confirm no other arrangements.', 'core', topic=T1),
                  M('k1b', 'Q Ltd. is most likely:', ['Not an associate, as the presumption is rebutted', 'An associate', 'A subsidiary', 'A joint venture'], 0,
                    'Clear evidence of no influence rebuts 20%. In practice: document evidence.', 'moderate', topic=T2),
                  M('k1c', 'R Ltd. is under:', ['Joint control', 'Control', 'Significant influence', 'No influence'], 0,
                    'Unanimity required. In practice: then classify as JO or JV.', 'core', topic=T3),
                  M('k1d', 'S Ltd. is likely:', ['An associate through board representation', 'A financial asset', 'A subsidiary', 'A joint operation'], 0,
                    'Board seats can give significant influence below 20%. In practice: equity method.', 'moderate', topic=T2),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch13', 2, 'Important Definitions',
                ['Define control, power, parent and subsidiary.',
                 'Define significant influence and associate.',
                 'Define joint control, joint operations and joint ventures.',
                 'Define group, NCI and consolidated and separate statements.'],
                {'difficulty': 'core', 'minutes': {'learn': 15, 'practice': 10}, 'prereq': ['fin-p1-ch13-u01'],
                 'exam_tip': 'Classify every investee before any computation — the label decides the method.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Control: power + variable returns + link.',
                             'Significant influence: participate, not control.',
                             'Joint control: unanimous consent.',
                             'JO: assets/liabilities; JV: net assets.',
                             'NCI: outsiders\' share of subsidiary equity.'],
                 'remember': ['20% presumption is rebuttable.'],
                 'traps': ['Treating equity-accounted statements as separate statements.']},
                [('Subsidiary', 'Control'), ('Associate', 'Significant influence'), ('JV', 'Net assets'), ('JO', 'Assets and liabilities')],
                viva, cases)
