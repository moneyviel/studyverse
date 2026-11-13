"""CA Final · Paper 1 Financial Reporting · Chapter 8 Unit 1 Ind AS 24 Related Party Disclosures.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch08-u01'
T1 = 'Who is a related party: persons'
T2 = 'Who is a related party: entities'
T3 = 'Disclosures required'
T4 = 'Government-related entities and exclusions'


def build():
    ck = Checks()
    kmp = ck.add('120+30+50', 'Total KMP compensation to disclose (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Key management compensation', 'difficulty': 'core', 'minutes': 6,
          'q': 'Opal Ltd.\'s directors received salaries ₹120 lakh, post-employment benefit contributions ₹30 lakh and share-based payments ₹50 lakh. A director\'s spouse sold goods worth ₹15 lakh to Opal on normal terms. What must be disclosed?',
          'solution': [table(['Item', 'Category', '₹ lakh'], [
              ['Short-term employee benefits', 'KMP compensation', inr(120)],
              ['Post-employment benefits', 'KMP compensation', inr(30)],
              ['Share-based payment', 'KMP compensation', inr(50)],
              ['Total KMP compensation', 'Disclose in total and by category', inr(kmp)],
              ['Purchases from director\'s spouse', 'Close family member of KMP — related party transaction', inr(15)]], title='Ind AS 24')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Mapping a group', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'P Ltd. owns 80% of S1 Ltd. and 30% of A Ltd. (an associate). S1 owns 25% of A2 Ltd. (its associate). Mr X, a director of P, controls Z Ltd. Identify related parties of S1 Ltd. in its own financial statements.',
          'solution': [table(['Party', 'Related to S1?', 'Reason'], [
              ['P Ltd.', 'Yes', 'Parent'],
              ['A Ltd.', 'Yes', 'Associate of S1\'s parent — same group'],
              ['A2 Ltd.', 'Yes', 'S1\'s own associate'],
              ['Mr X', 'Yes', 'KMP of the parent'],
              ['Z Ltd.', 'Yes', 'Controlled by KMP of the parent']], title='Related parties of S1')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Ind AS 24 makes users aware that an entity\'s position and results may be affected by related parties and transactions with them, which may not occur on terms that unrelated parties would accept.',
            'An individual (or that individual\'s close relative) is a related party of the reporting entity if the person has control or joint control over it, has significant influence over it, or is a member of key management personnel (KMP) of the entity or its parent.',
            'Close family means relatives likely to sway, or be swayed by, that individual when dealing with the entity — including children, spouse or domestic partner, siblings, parents, children of spouse and dependants. KMP are those having authority and responsibility for planning, directing and controlling activities, including directors.'],
          'Look at power and family ties, not at legal form.',
          'A director\'s brother supplying goods is a related party.'),
        C('c2', T2, [
            'An entity is related to the reporting entity if: they are members of the same group (parents, subsidiaries, fellow subsidiaries all related); one is an associate or joint venture of the other or of a member of its group; both are joint ventures of the same third party; one is a joint venture and the other an associate of the same third party.',
            'Also related: a post-employment benefit plan for employees of either entity; an entity controlled or jointly controlled by a related person; an entity over which a person with control of the reporting entity has significant influence or is KMP; and an entity (or group member) that provides KMP services to the reporting entity or its parent.',
            'Two associates of the same investor are not related to each other merely because of that; two entities sharing a director are not automatically related.'],
          'Draw the group chart; relationships run through control and joint control.',
          'A management company providing a CEO to the entity is related.'),
        C('c3', T3, [
            'Relationships between parents and subsidiaries are disclosed regardless of transactions, naming the parent and ultimate controlling party (and the next most senior parent producing public statements, if neither does).',
            'KMP compensation is disclosed in total and for each category: short-term pay, post-employment benefits, share-based payment, termination benefits, and other long-term benefits. Amounts for KMP services from a management entity are disclosed.',
            'For transactions: nature of the relationship, amount of transactions, outstanding balances with terms, security and guarantees, impairment allowances and bad-debt expense. Disclosures are by category (parent, entities with joint control, subsidiaries, associates, joint ventures, KMP, others). A claim of arm\'s-length terms is made only if it can be substantiated.'],
          'Disclose the relationship always; the transactions when they occur.',
          'Loan given to an associate with balance and interest is disclosed.'),
        C('c4', T4, [
            'Not related merely because of: two entities having a common director or KMP; two joint venturers sharing joint control; providers of finance, trade unions, public utilities and government departments in normal dealings; a major customer, supplier or agent on whom the entity depends economically.',
            'Government-related entities: an entity may be exempt from detailed disclosure of transactions with a government that controls, jointly controls or significantly influences it, and with other entities related to that same government. It must still disclose the name of the government, nature of relationship, and nature and amount of each individually significant transaction, plus a qualitative or quantitative indication of collectively significant ones.',
            'Indian law (Companies Act, SEBI LODR) may impose further related party approvals and disclosures beyond Ind AS 24.'],
          'Economic dependence is not the same as a related-party relationship.',
          'A public sector bank need not list every deposit from other PSUs.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Compiling the related party note', 'role': 'Company secretary',
             'situation': 'Year-end disclosures must match board approvals.',
             'steps': ['Gather declarations from directors and KMP.', 'Map group entities.', 'Extract transactions and balances.', 'Present by category with KMP compensation split.'],
             'takeaway': 'Declarations from directors are the starting point of completeness.'}]

    mcqs = [
        Q('m1', 'Two entities with a common director are:', ['Not related merely for that reason', 'Always related', 'Related if both are listed', 'Related if in the same city'], 0,
          'More is needed, such as control. In practice: check other links.', 'c4', T4),
        Q('m2', 'Relationships between a parent and its subsidiaries are disclosed:', ['Whether or not transactions occurred', 'Only if transactions occurred', 'Only if material', 'Never'], 0,
          'The relationship itself matters. In practice: name the ultimate controlling party.', 'c3', T3),
        Q('m3', 'KMP compensation is disclosed:', ['In total and by each category', 'Only in total', 'Only for the CEO', 'Not at all'], 0,
          'Five categories are listed. In practice: include share-based payments.', 'c3', T3),
        Q('m4', 'A post-employment benefit plan for the entity\'s employees is:', ['A related party', 'Not a related party', 'A customer', 'Government'], 0,
          'Expressly included. In practice: disclose contributions.', 'c2', T2),
        Q('m5', 'A single customer providing 60% of revenue is:', ['Not a related party merely due to dependence', 'A related party', 'A parent', 'An associate'], 0,
          'Economic dependence is excluded. In practice: Ind AS 108 may require disclosure.', 'c4', T4),
        Q('m6', 'A director\'s spouse is:', ['A close member of the family of KMP — related', 'Not related', 'Related only if a shareholder', 'An associate'], 0,
          'Spouse is listed as close family. In practice: obtain declarations.', 'c1', T1),
        Q('m7', 'The government-related entity exemption removes:', ['Detailed disclosure of transactions with the government and its related entities', 'All disclosures', 'KMP disclosures', 'Parent disclosures'], 0,
          'Significant transactions still need disclosure. In practice: PSUs use it.', 'c4', T4),
        Q('m8', 'An entity providing key management personnel services is:', ['A related party', 'Not a related party', 'A supplier only', 'Excluded'], 0,
          'Management entities are included. In practice: disclose fees paid.', 'c2', T2),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Categories', 2, 'concept', 'short-term|post-employment|share'), S('s2', 'Total', 1, 'computation', 'total', nums=[kmp]), S('s3', 'Spouse', 1, 'concept', 'family|spouse')],
          ['Split by category.'], ['Missing the spouse.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Group entities', 2, 'concept', 'parent|group'), S('s2', 'Associates', 1.5, 'concept', 'associate'), S('s3', 'KMP links', 1.5, 'concept', 'kmp|controlled')],
          ['Draw a chart.'], ['Ignoring parent\'s KMP.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Why are related party disclosures needed?', 'Because related parties can influence results and may transact on terms unrelated parties would reject, so users need to know.',
          [P('p1', 'Influence', 5, 'influence'), P('p2', 'Terms', 5, 'terms')], 'c1'),
        V('v2', 'Who are key management personnel?', 'People with authority and responsibility for planning, directing and controlling the entity\'s activities, including directors.',
          [P('p1', 'Planning and controlling', 6, 'planning|controlling'), P('p2', 'Directors', 4, 'director')], 'c1'),
        V('v3', 'List the categories of KMP compensation.', 'Short-term pay, post-employment benefits, share-based payment, termination benefits, and other long-term benefits.',
          [P('p1', 'Short-term and post-employment', 5, 'short-term|post-employment'), P('p2', 'Termination and share-based', 5, 'termination|share')], 'c3'),
        V('v4', 'Name parties excluded from being related merely by normal dealings.', 'Providers of finance, trade unions, public utilities, government departments, and major customers or suppliers on whom the entity depends.',
          [P('p1', 'Finance and utilities', 5, 'finance|utilit'), P('p2', 'Major customers', 5, 'customer|supplier')], 'c4'),
        V('v5', 'What remains disclosed under the government-related exemption?', 'The government\'s name, the nature of the relationship and the nature and amount of individually significant transactions with an indication of collectively significant ones.',
          [P('p1', 'Name and relationship', 5, 'name|relationship'), P('p2', 'Significant transactions', 5, 'significant')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Saffron Foods Ltd.', 'difficulty': 'moderate',
              'case': 'Saffron Foods Ltd. buys packaging from Bright Packs Ltd., whose MD is the brother of Saffron\'s CFO. It also sells 70% of its output to a supermarket chain. Its holding company is Indigo Holdings, itself 60% owned by Mr R. A director of Saffron is also on the board of an unrelated bank that lends to it.',
              'mcqs': [
                  M('k1a', 'Bright Packs is a related party only if:', ['The CFO\'s brother controls or jointly controls it', 'It supplies goods', 'It is profitable', 'It is listed'], 0,
                    'Being MD alone of another firm does not create the link unless control or KMP-of-reporting-entity tests are met. In practice: check ownership.', 'hard', topic=T2),
                  M('k1b', 'The supermarket chain is:', ['Not a related party merely due to dependence', 'A related party', 'A parent', 'A joint venture'], 0,
                    'Economic dependence is excluded. In practice: segment disclosure may apply.', 'core', topic=T4),
                  M('k1c', 'The ultimate controlling party to be named is:', ['Mr R', 'Indigo Holdings', 'The bank', 'The CFO'], 0,
                    'Mr R controls the parent. In practice: disclose regardless of transactions.', 'core', topic=T3),
                  M('k1d', 'The bank with a common director is:', ['Not related merely due to the common director', 'Related', 'A parent', 'An associate'], 0,
                    'Common directorships alone do not create relationships. In practice: still check other links.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch08', 1, 'Ind AS 24 "Related Party Disclosures"',
                ['Identify persons who are related parties.',
                 'Identify entities that are related parties.',
                 'Prepare related party disclosures including KMP compensation.',
                 'Apply exclusions and the government-related exemption.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 20}, 'prereq': ['fin-p1-ch07-u02'],
                 'exam_tip': 'Draw the group chart first, then test each party against control, joint control, significant influence and KMP.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Persons: control, significant influence, KMP and close family.',
                             'Entities: group members, associates, JVs, benefit plans.',
                             'Parent relationships disclosed always.',
                             'KMP compensation in five categories.',
                             'Government-related entities: reduced disclosure.'],
                 'remember': ['Economic dependence is not a relationship.'],
                 'traps': ['Treating common directors as automatically related.']},
                [('KMP', 'Plan, direct, control'), ('Close family', 'Spouse, children, dependants'), ('Common director', 'Not alone'), ('Govt-related', 'Reduced disclosure')],
                viva, cases)
