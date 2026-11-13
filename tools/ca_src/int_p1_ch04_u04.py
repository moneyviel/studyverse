"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 4 Unit 4 — AS 18 Related Party Disclosures.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch04-u04'
T1 = 'Why related party disclosures matter'
T2 = 'Control, significant influence and who is a related party'
T3 = 'Parties that are not related merely because of dealings'
T4 = 'Exemptions from disclosure'
T5 = 'What must be disclosed'


def build():
    ck = Checks()
    fam = ck.add('12+10', 'Voting power of Mr. Sethi with his wife (%)')
    ind = ck.add('80*30/100', 'Effective interest of Alpha in Gamma through Beta (%)')
    i1 = {'id': 'i1', 'title': 'Mapping the related parties', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Alpha Ltd. holds 80% of Beta Ltd.; Beta holds 30% of Gamma Ltd. Mr. Sethi holds 12% of Alpha and his wife 10%. Mr. Rao is Alpha\'s managing director; his brother owns Delta Traders, which supplies Alpha. Alpha also sells 35% of its output to Omega Ltd., an unrelated buyer. Identify Alpha\'s related parties.',
          'solution': [table(['Party', 'Reason', 'Related?'], [
              ['Beta Ltd.', 'Alpha controls it (80%)', 'Yes — subsidiary'],
              ['Gamma Ltd.', f'Beta, controlled by Alpha, holds 30% — significant influence (Alpha\'s effective interest {R(ind)}%)', 'Yes — associate'],
              ['Mr. Sethi', f'With his wife he holds {R(fam)}% — significant influence', 'Yes — individual and his relative'],
              ['Mr. Rao', 'Key management personnel', 'Yes'],
              ['Delta Traders', 'Owned by a relative of KMP; can be influenced', 'Yes'],
              ['Omega Ltd.', 'Only a major customer — economic dependence is not a relationship', 'No']], title='AS 18 relationships')],
          'checks': list(ck)}

    ck2 = Checks()
    pct = ck2.add('40*100/800', 'Sales to Beta as % of Alpha\'s sales')
    i2 = {'id': 'i2', 'title': 'Drafting the disclosure', 'difficulty': 'core', 'minutes': 6,
          'q': 'During the year Alpha Ltd. (total sales ₹800 lakh) sold goods worth ₹40 lakh to Beta Ltd., of which ₹6 lakh is outstanding; paid Mr. Rao remuneration of ₹30 lakh; and bought goods worth ₹15 lakh from Delta Traders. Outline the disclosure.',
          'solution': [table(['Related party', 'Relationship', 'Transaction', 'Volume', 'Outstanding'], [
              ['Beta Ltd.', 'Subsidiary', 'Sale of goods', f'₹40 lakh ({R(pct)}% of sales)', '₹6 lakh receivable'],
              ['Mr. Rao', 'Key management personnel', 'Remuneration', '₹30 lakh', '—'],
              ['Delta Traders', 'Enterprise of a relative of KMP', 'Purchase of goods', '₹15 lakh', '—']], title='Related party transactions'),
              p('Also disclose names and nature of relationships where control exists (Beta Ltd.), even if there were no transactions. In Alpha\'s consolidated statements, the sale to Beta is eliminated and need not be disclosed.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Related party relationships can affect an enterprise\'s results and position: prices may not be at arm\'s length, and transactions may occur that would not happen between unrelated parties.',
            'AS 18 requires disclosure of these relationships and transactions so that users can understand their effect. It applies to reporting enterprises other than those exempted (smaller enterprises get relief in certain disclosures).'],
          'Readers need to know when the other side of a deal is not really a stranger.',
          'A subsidiary buying raw material from its parent at above-market prices shifts profit between them.'),
        C('c2', T2, [
            'Parties are related if, at any time in the period, one can control the other or exercise significant influence over its financial and operating decisions.',
            'Control: owning (directly or through subsidiaries) more than half the voting power; or controlling the composition of the board; or a substantial voting interest with power by statute or agreement to direct financial and operating policies.',
            'Significant influence: participating in financial and operating policy decisions without control — through board representation, policy participation, material inter-company transactions, interchange of managers or dependence on technical information. Holding 20% or more of voting power, directly or indirectly, is presumed to give significant influence.',
            'AS 18 covers: holding companies, subsidiaries and fellow subsidiaries; associates and joint ventures; individuals with control or significant influence and their relatives; key management personnel (KMP) and their relatives; and enterprises over which any of these individuals has significant influence.',
            'Relative: the spouse, parents, children and siblings (brother, sister) of the individual, where they could sway, or be swayed by, the individual in dealings with the enterprise.'],
          'Look for anyone who can steer or substantially sway the enterprise\'s decisions — and their close family.',
          'A director\'s sister\'s firm that sells to the company is a related party.'),
        C('c3', T3, [
            'The following are not related parties merely because of their dealings: two companies that merely share a director (a link arises only if that director can shape the policies of both); a single customer, supplier, franchisor, distributor or agent with whom a significant volume of business is done; and providers of finance, trade unions, public utilities and government departments in normal dealings.'],
          'Economic dependence is not the same as a relationship.',
          'A bank that lends to the company and insists on covenants is not a related party.'),
        C('c4', T4, [
            'No disclosure is required in consolidated financial statements for intra-group transactions, which are eliminated.',
            'State-controlled enterprises need not disclose relationships and transactions with other state-controlled enterprises.',
            'Disclosure is not required where it would conflict with a duty of confidentiality under a statute, regulator or similar authority — such as a bank\'s duty about customer accounts.'],
          'Some relationships are already visible or legally confidential.',
          'A public sector bank does not list its dealings with other public sector undertakings.'),
        C('c5', T5, [
            'Where control exists, disclose the name of the related party and the nature of the relationship, whether or not there were transactions.',
            'If there were transactions, disclose: name of the party; description of the relationship; description of the transactions; volume, as an amount or proportion; other elements needed to understand them; year-end balances (as amounts or proportions) with any doubtful debt provision against them; and amounts written off or written back.',
            'Items of a similar nature may be aggregated by type of related party, except where separate disclosure is needed to understand the effect.',
            'Typical transactions: purchases or sales of goods and fixed assets, rendering or receiving services, agency arrangements, leasing, transfer of research, licences, finance (loans and equity), guarantees and management contracts.'],
          'Name, relationship, transaction, amount, balance — the five things to tell.',
          'A loan to a director\'s firm must be disclosed with the year-end balance even if interest-free.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Building the related party list', 'role': 'Audit assistant',
             'situation': 'A client gives a list of five related parties, but board minutes mention several other entities.',
             'steps': ['Get shareholding and directorship details.', 'Identify KMP and their relatives\' businesses.', 'Match the ledger for transactions with each party.', 'Check balances and write-offs for disclosure.'],
             'takeaway': 'The completeness of the related party list is the auditor\'s first test.'}]

    mcqs = [
        Q('m1', 'Holding 20% or more of voting power of an enterprise is presumed to give:', ['Significant influence', 'Control', 'Joint control', 'No relationship'], 0,
          'Under AS 18 an investing party holding, directly or indirectly, 20% or more of voting power is presumed to have significant influence unless it is clearly shown otherwise. More than half usually gives control. In practice: count indirect holdings too.', 'c2', T2),
        Q('m2', 'Which relative is included in the AS 18 definition?', ['Brother', 'Cousin', 'Uncle', 'Brother-in-law'], 0,
          'AS 18 defines relative as the spouse, parents, children and siblings of the individual, where they could sway or be swayed by the individual in dealings with the enterprise. Wider family members are excluded. In practice: list only these relations.', 'c2', T2),
        Q('m3', 'Two companies with a common director are:', ['Not related merely for that reason', 'Always related', 'Related if both are listed', 'Related only if the director is MD of both'], 0,
          'A common director alone does not create a related party relationship; the facts must show control or significant influence. AS 18 lists this as an example of parties not necessarily related. In practice: examine actual influence.', 'c3', T3),
        Q('m4', 'A company sells 60% of its output to one distributor. The distributor is:', ['Not a related party merely because of economic dependence', 'A related party', 'An associate', 'A joint venture'], 0,
          'A single customer or distributor with whom a significant volume of business is done is not a related party simply because of that dependence. Some other link of control or influence is needed. In practice: disclose dependence elsewhere if material.', 'c3', T3),
        Q('m5', 'In consolidated financial statements, intra-group sales:', ['Need not be disclosed as related party transactions', 'Must be disclosed in full', 'Are disclosed only if over 10%', 'Are disclosed as segment revenue'], 0,
          'AS 18 exempts intra-group transactions from disclosure in consolidated statements because they are eliminated on consolidation. They are still disclosed in the separate statements of each group company. In practice: check which set you are preparing.', 'c4', T4),
        Q('m6', 'Where control exists, the name of the related party and nature of relationship are disclosed:', ['Whether or not there were transactions', 'Only if there were transactions', 'Only if material', 'Only for listed companies'], 0,
          'AS 18 requires disclosure of the name and nature of the relationship wherever control exists, irrespective of transactions, because control itself can affect the enterprise. In practice: always name the parent and subsidiaries.', 'c5', T5),
        Q('m7', 'Mr. Kumar holds 9% of a company and his father 13%. Together they hold:', ['22%, giving significant influence', '13%, giving no influence', '9%, giving no influence', 'Control, as family holdings are doubled'], 0,
          'The holdings of an individual and his relatives are considered together: 9% + 13% = 22%, which is over the 20% presumption for significant influence, though not control. In practice: aggregate family holdings.', 'c2', T2, 'moderate'),
        Q('m8', 'Which is NOT a related party of a company?', ['A trade union representing its workers', 'Its managing director', 'Its fellow subsidiary', 'Its associate'], 0,
          'Trade unions, providers of finance, public utilities and government departments in the ordinary course are not related parties merely because of their dealings. KMP, fellow subsidiaries and associates are. In practice: apply the list.', 'c3', T3),
        Q('m9', 'Which element must be disclosed for related party transactions?', ['Amounts outstanding at the balance sheet date', 'The related party\'s profit', 'The market price of shares', 'The tax paid by the related party'], 0,
          'AS 18 requires disclosure of amounts or proportions outstanding at the balance sheet date and related doubtful debt provisions, together with name, relationship, transaction description and volume. In practice: reconcile balances with the party.', 'c5', T5),
        Q('m10', 'A public sector undertaking need not disclose its transactions with:', ['Other state-controlled enterprises', 'Its own subsidiaries in separate statements', 'Its key management personnel', 'Its associates'], 0,
          'AS 18 exempts state-controlled enterprises from disclosing relationships and transactions with other state-controlled enterprises. Other related parties still require disclosure. In practice: the exemption is narrow.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Subsidiary and associate', 2, 'concept', 'subsidiary', 'associate'),
           S('s2', 'Individual with relative', 1.5, 'computation', 'significant', nums=[fam]),
           S('s3', 'KMP and relative\'s enterprise', 1.5, 'concept', 'key management'),
           S('s4', 'Major customer not related', 1, 'concept', 'economic|customer')],
          ['Justify each relationship.'], ['Treating a big customer as related.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Name, relationship, transaction', 2, 'concept', 'subsidiary'),
           S('s2', 'Volume and outstanding balance', 1, 'computation', 'outstanding', nums=[pct]),
           S('s3', 'Control disclosure and consolidation', 1, 'concept', 'control|consolidat')],
          ['Use the AS 18 columns.'], ['Omitting balances.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'When are two parties related under AS 18?', 'When at any time during the period one party can control the other or exercise significant influence over its financial and operating decisions.',
          [P('p1', 'Control', 5, 'control'), P('p2', 'Significant influence', 5, 'significant influence')], 'c2'),
        V('v2', 'What is significant influence?', 'Participation in the financial and operating policy decisions of an enterprise without control; 20% or more of voting power is presumed to give it.',
          [P('p1', 'Participation without control', 6, 'participat|without control'), P('p2', '20%', 4, '20')], 'c2'),
        V('v3', 'Name some parties that are not related merely by dealings.', 'Two companies with a common director, a major single customer or supplier, providers of finance, trade unions, public utilities and government departments.',
          [P('p1', 'Common director', 4, 'director'), P('p2', 'Customer, finance, unions', 6, 'customer|supplier|finance|union')], 'c3'),
        V('v4', 'What must be disclosed where control exists?', 'The name of the related party and the nature of the relationship, irrespective of whether there were any transactions.',
          [P('p1', 'Name and relationship', 6, 'name', 'relationship'), P('p2', 'Even without transactions', 4, 'irrespective|whether or not|without')], 'c5'),
        V('v5', 'Who is a relative under AS 18?', 'The individual\'s spouse, parents (father, mother), children (son, daughter) and siblings, where they could sway or be swayed by the individual in dealings with the enterprise.',
          [P('p1', 'Listed family members', 6, 'spouse|son|daughter|father|mother'), P('p2', 'Influence test', 4, 'sway|influence')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Shree Ganesh Mills Ltd.', 'difficulty': 'moderate',
              'case': 'Shree Ganesh Mills Ltd. buys cotton worth ₹2 crore from a firm owned by the CFO\'s wife, gives an interest-free loan of ₹50 lakh to its 70% subsidiary (outstanding at year end), and borrows ₹10 crore from a public sector bank. Its chairman is also on the board of an unrelated supplier.',
              'mcqs': [
                  M('k1a', 'The purchase from the CFO\'s wife\'s firm is:', ['A related party transaction, as the CFO is KMP and his wife a relative', 'Not related, as the firm is separate', 'Related only if above ₹5 crore', 'Exempt'], 0,
                    'Key management personnel and their relatives are related parties, and so are enterprises over which they have significant influence. The wife\'s firm qualifies. In practice: disclose the ₹2 crore with balances.', 'core', topic=T2),
                  M('k1b', 'The bank loan of ₹10 crore is:', ['Not a related party transaction', 'A related party transaction because the bank is state-owned', 'Related because it is large', 'Exempt only in consolidated accounts'], 0,
                    'Providers of finance in the ordinary course are not related parties merely because of their dealings with the enterprise, whatever the amount. In practice: disclose the loan under borrowings, not AS 18.', 'core', topic=T3),
                  M('k1c', 'Amount outstanding to be disclosed for the subsidiary loan in the separate statements:', ['₹50 lakh', 'Nil, as it is interest-free', '₹35 lakh', '₹2 crore'], 0,
                    'The full ₹50 lakh outstanding with the subsidiary must be disclosed in the company\'s separate statements; being interest-free makes disclosure more, not less, important. It is eliminated only on consolidation. In practice: also state terms.', 'moderate', check=50, topic=T5),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch04', 4, 'Accounting Standard 18 Related Party Disclosures',
                ['Explain why related party relationships need disclosure.',
                 'Identify related parties using control and significant influence.',
                 'Recognise parties that are not related and the exemptions.',
                 'Prepare the required disclosures.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 25}, 'prereq': ['int-p1-ch04-u03'],
                 'exam_tip': 'For each party, write the link (control, significant influence, KMP, relative) before deciding; aggregate family holdings.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Related: control or significant influence at any time in the period.',
                             'Control > 50% votes, board control, or substantial interest with power; significant influence presumed at 20%.',
                             'Covers group, associates, JVs, individuals, KMP, relatives and their enterprises.',
                             'Not related merely by dealings: common director, big customer, financiers, unions, utilities.',
                             'Exemptions: intra-group in CFS; state-controlled with each other; statutory confidentiality.',
                             'Disclose name, relationship, transaction, volume, balances, write-offs; control always.'],
                 'remember': ['Relative = spouse, children, siblings, parents.'],
                 'traps': ['Economic dependence is not a relationship.']},
                [('Significant influence', '≥ 20% voting power'), ('Control', '> 50% / board control'), ('Relative', 'Spouse, son, daughter, brother, sister, father, mother')],
                viva, cases)
