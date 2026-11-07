"""CA Foundation · Paper 1 Accounting · Chapter 1 Theoretical Framework · Unit 7 Accounting Standards.
Original explanations, figures and questions (structure and scope follow the ICAI study material)."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p1-ch01-u07'

AS_LIST = [
    ('AS 1', 'Disclosure of Accounting Policies'), ('AS 2', 'Valuation of Inventories'), ('AS 3', 'Cash Flow Statements'),
    ('AS 4', 'Contingencies and Events Occurring after the Balance Sheet Date'),
    ('AS 5', 'Period Profit or Loss, Prior Period Items and Accounting Policy Changes'),
    ('AS 7', 'Construction Contracts'), ('AS 9', 'Revenue Recognition'), ('AS 10', 'Property, Plant and Equipment'),
    ('AS 11', 'The Effects of Changes in Foreign Exchange Rates'), ('AS 12', 'Government Grants'), ('AS 13', 'Investments'),
    ('AS 14', 'Amalgamations'), ('AS 15', 'Employee Benefits'), ('AS 16', 'Borrowing Costs'), ('AS 17', 'Segment Reporting'),
    ('AS 18', 'Related Party Disclosures'), ('AS 19', 'Leases'), ('AS 20', 'Earnings Per Share'), ('AS 21', 'Consolidated Financial Statements'),
    ('AS 22', 'Taxes on Income'), ('AS 23', 'Investments in Associates in Consolidated Financial Statements'), ('AS 24', 'Discontinuing Operations'),
    ('AS 25', 'Interim Financial Reporting'), ('AS 26', 'Intangible Assets'), ('AS 27', 'Interests in Joint Ventures'),
    ('AS 28', 'Impairment of Assets'), ('AS 29', 'Provisions, Contingent Liabilities and Contingent Assets'),
]


def build():
    # ---------------- Illustration 1: why standards are needed ----------------
    c1 = Checks()
    dep_a = c1.add('1000000*10/100', 'Firm A depreciation: straight-line 10% of ₹10,00,000')
    dep_b = c1.add('1000000*20/100', 'Firm B depreciation: written-down value 20% of ₹10,00,000 (first year)')
    inv_a = c1.add('500*130', 'Firm A closing inventory: 500 units at latest price ₹130 (FIFO)')
    inv_b = c1.add('500*(1000*100+1000*130)/2000', 'Firm B closing inventory: 500 units at weighted average ₹115')
    pa = c1.add('300000-100000+65000-57500', 'Firm A profit relative to common base')
    pb = c1.add('300000-200000+57500-57500', 'Firm B profit relative to common base')
    c1.add('207500-100000', 'Difference in reported profit caused only by policy choices')
    cmp_tbl = table(['Particulars', 'Firm A (₹)', 'Firm B (₹)'], [
        ['Profit before depreciation and inventory difference', '3,00,000', '3,00,000'],
        ['Less: Depreciation', '-' + inr(dep_a), '-' + inr(dep_b)],
        ['Add: Closing inventory above the ₹57,500 common base', inr(inv_a - 57500), inr(inv_b - 57500)],
        ['Reported profit', inr(pa), inr(pb)],
    ], num=[1, 2], total=True, title='Two identical firms, two different profits')

    # ---------------- Illustration 2: which set of standards applies ----------------
    app_tbl = table(['Entity', 'Facts', 'Standards to follow', 'Reason'], [
        ['Arjun Steel Ltd', 'Listed on a stock exchange; net worth ₹90 crore', 'Ind AS', 'All listed companies follow Ind AS, whatever their net worth'],
        ['Bhoomi Agro Pvt Ltd', 'Unlisted; net worth ₹420 crore', 'Ind AS', 'Unlisted company with net worth of ₹250 crore or more'],
        ['Chetna Textiles Pvt Ltd', 'Unlisted; net worth ₹75 crore', 'AS notified under the Companies (Accounting Standards) Rules, 2021', 'Company not covered by Ind AS'],
        ['Dhruv Finance Ltd', 'Listed NBFC', 'Ind AS', 'Listed companies and NBFCs follow Ind AS'],
        ['Ekta & Co.', 'Partnership firm', 'AS issued by ICAI', 'Entities other than companies follow the AS prescribed by ICAI'],
        ['Falcon Designs LLP', 'Limited liability partnership', 'AS issued by ICAI', 'Not a company'],
    ], title='Three sets of standards in India')

    as_tbl = table(['Standard', 'Title (short form)'], [[a, b] for a, b in AS_LIST],
                   title='Accounting Standards (AS) currently applicable — for knowledge only, not part of the syllabus',
                   note='AS 6 and AS 8 no longer appear because their subjects are now covered elsewhere (AS 10 and AS 26).')

    proc_tbl = table(['Step', 'What happens'], [
        ['1', 'ASB identifies broad areas needing a standard'],
        ['2', 'ASB forms study groups that prepare preliminary drafts (objective, scope, definitions, recognition and measurement, presentation and disclosure)'],
        ['3', 'ASB considers and revises the preliminary draft'],
        ['4', 'Revised draft circulated for comments to ICAI Council members and specified outside bodies (e.g. MCA, SEBI, C&AG, CBDT, SCOPE)'],
        ['5', 'ASB meets representatives of these bodies to hear their views'],
        ['6', 'Exposure draft finalised and issued for public comment'],
        ['7', 'ASB considers the comments and finalises the draft for the ICAI Council'],
        ['8', 'Council considers the final draft; any modification is made only in consultation with ASB'],
        ['9', 'Standard issued — by ICAI for non-corporate entities; for companies, notified by the Central Government'],
    ], title='How an Accounting Standard is made in India')

    concepts = [
        {'id': 'c1', 'title': 'What Accounting Standards are',
         'body': ['Left unregulated, financial reporting could become misleading or one-sided. To make reports transparent, consistent, comparable, adequate and reliable, accounting principles and policies need to be standardised.',
                  'Accounting Standards are written policy documents issued by an expert accounting body, the government or another regulator. They deal with four aspects of transactions and events: (i) recognition — whether and when an item enters the financial statements; (ii) measurement — at what amount; (iii) presentation — how it is shown so that it is meaningful and understandable; and (iv) disclosure — what must be told so that stakeholders and potential investors can see what the statements reflect and decide prudently.',
                  'Their aim is to spread timely and useful financial information to investors and others interested in an enterprise\'s performance.'],
         'analogy': 'Like a standard grammar for a language — without it, every writer would spell and punctuate differently and readers would struggle to understand.',
         'work': 'Every audit report states whether the financial statements comply with the applicable Accounting Standards. A CA checks each significant item — inventory, revenue, depreciation, provisions — against the relevant standard.'},
        {'id': 'c2', 'title': 'Objectives, benefits and limitations',
         'body': ['Objective: harmonise the diverse accounting policies and practices of different entities. Standards standardise policies so as to (i) remove non-comparability of financial statements and so improve their reliability, and (ii) lay down a common set of accounting policies, valuation rules and disclosure requirements. They reduce the alternatives within reasonable bounds, making statements of different enterprises comparable.',
                  'Benefits: (i) confusing variations in accounting treatment are reduced or eliminated; (ii) standards may require disclosures beyond what the law demands; (iii) they help, to a limited extent, compare statements of companies within a country and across countries — though differing institutions, traditions and legal systems mean standards differ between countries.',
                  'Limitations: (i) choosing between alternative treatments can be difficult because each may have good arguments; (ii) restricted scope — standards cannot override a statute and must be framed within the existing laws.'],
         'analogy': 'Standard sizes for shoes: you can compare and buy across brands easily (benefit), but feet still differ, and the government\'s rules on materials override the size chart (limitations).',
         'work': 'Analysts comparing two cement companies rely on both following the same standards. When a law prescribes a different treatment, the law prevails and the company discloses the departure.'},
        {'id': 'c3', 'title': 'How standards are formulated in India',
         'body': ['ICAI, as the premier accounting body, constituted the Accounting Standards Board (ASB) in 1977. The process is consultative and transparent. ASB considers International Financial Reporting Standards (IFRS) and tries to integrate them, keeping in view Indian laws, customs, usages and business environment.',
                  'ASB includes representatives of industry (ASSOCHAM, CII, FICCI), regulators, academicians and government departments. Although set up by the ICAI Council, ASB is independent in formulating standards; the Council cannot modify a draft standard without consulting ASB.',
                  'The steps run from identifying the area, through study-group drafts, consultation with outside bodies and an exposure draft for public comment, to final approval by the Council and issue.'],
         'blocks': [proc_tbl],
         'analogy': 'Like drafting a new rule for a housing society: a committee drafts it, circulates it, invites objections from residents and only then adopts it.',
         'work': 'Practising CAs, industry bodies and students can send comments on exposure drafts. Following exposure drafts helps a CA prepare clients early for changes in reporting.'},
        {'id': 'c4', 'title': 'Three sets of standards and the list of AS',
         'body': ['India has three sets of standards for different categories of entities: (i) Indian Accounting Standards (Ind AS) — IFRS-converged standards for all listed companies and NBFCs, and for unlisted companies and unlisted NBFCs with net worth of ₹250 crore or more; (ii) Accounting Standards (AS) notified under the Companies (Accounting Standards) Rules, 2021 — for companies not following Ind AS; (iii) AS prescribed by ICAI — for entities other than companies (sole proprietors, partnership firms, LLPs, trusts and others).',
                  'For companies, the standards are notified by the Central Government; for non-corporate entities, they are issued by ICAI.',
                  'Exam versus practice: for the examination, state the position as given above. In practice the Companies (Indian Accounting Standards) Rules, 2015 add details — for example, companies listed only on an SME exchange are not required to apply Ind AS, and NBFCs are covered by their own net-worth thresholds. You will study these details at the Intermediate level.',
                  'India chose to converge with IFRS (keeping Ind AS close to IFRS with only essential departures for the Indian environment) rather than adopt IFRS as they are. There are also Accounting Standards for Local Bodies (ASLB) for public-service bodies such as municipalities. The lists of AS, Ind AS and ASLB are given for knowledge only and are not part of the syllabus.'],
         'blocks': [as_tbl],
         'analogy': 'Three rulebooks for three leagues — an international league (Ind AS), a national league (Companies AS Rules) and local clubs (ICAI AS for non-corporates) — each suited to its players.',
         'work': 'The first question on any new engagement is "which framework applies?" — the answer depends on listing status, net worth and legal form, and it changes the entire set of rules you apply.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Same business, different profits — the case for standards', 'difficulty': 'moderate', 'minutes': 10,
         'q': 'Firm A and Firm B are identical in every respect. Each earned ₹3,00,000 before depreciation and before the inventory difference, owns a machine costing ₹10,00,000, bought 1,000 units at ₹100 and later 1,000 units at ₹130, and has 500 units in closing inventory. Firm A charges straight-line depreciation at 10% and values inventory on FIFO; Firm B charges written-down-value depreciation at 20% and uses weighted average. Compute each firm\'s profit (taking ₹57,500 as a common inventory base so that only the difference is added) and comment on the role of Accounting Standards.',
         'solution': [wn('Depreciation', f'Firm A: 10% × 10,00,000 = ₹{inr(dep_a)}. Firm B: 20% × 10,00,000 = ₹{inr(dep_b)} in the first year.'),
                      wn('Closing inventory', f'Firm A (FIFO): 500 × 130 = ₹{inr(inv_a)}. Firm B (weighted average ₹115): 500 × 115 = ₹{inr(inv_b)}.'),
                      cmp_tbl,
                      p(f'Identical businesses report ₹{inr(pa)} and ₹{inr(pb)} only because of policy choices. Accounting Standards narrow the acceptable choices and require disclosure of the policies used (AS 1), so that users can compare. They cannot remove every alternative, which is why reading the policy note matters.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Which set of standards applies?', 'difficulty': 'core', 'minutes': 6,
         'q': 'Identify the standards each entity must follow: Arjun Steel Ltd (listed, net worth ₹90 crore); Bhoomi Agro Pvt Ltd (unlisted, net worth ₹420 crore); Chetna Textiles Pvt Ltd (unlisted, net worth ₹75 crore); Dhruv Finance Ltd (listed NBFC); Ekta & Co. (partnership firm); Falcon Designs LLP.',
         'solution': [app_tbl, note('Net worth matters only for unlisted companies; listing alone brings a company under Ind AS (as the study material states it — in practice, companies listed only on an SME exchange are exempt).')]},
        {'id': 'i3', 'title': 'Standard-setting steps in order', 'difficulty': 'core', 'minutes': 5,
         'q': 'Arrange in the correct order: (a) issue of exposure draft for public comment; (b) identification of broad areas by ASB; (c) approval by the ICAI Council; (d) preparation of preliminary draft by a study group; (e) circulation of draft to specified outside bodies and meeting their representatives; (f) consideration of public comments by ASB.',
         'solution': [p('Correct order: (b) → (d) → (e) → (a) → (f) → (c).'), proc_tbl]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Framework check for a growing client', 'role': 'Audit manager at a mid-sized CA firm',
         'situation': 'A private company client\'s net worth has risen from ₹180 crore to ₹270 crore. The CFO assumes the company will keep following the Companies (AS) Rules.',
         'steps': ['Check the applicability criteria: unlisted companies with net worth of ₹250 crore or more come under Ind AS.',
                   'Explain that the company must move to Ind AS (as per the applicability rules and timeline) and that comparatives will need restating.',
                   'Plan the transition: identify major differences (e.g. revenue, financial instruments, leases) and train the accounts team.',
                   'Inform the audit committee/board of the impact.'],
         'takeaway': 'Applicability is not fixed forever — listing status and net worth must be checked every year.',
         'think': 'Would the answer change if the company were a partnership firm with the same net worth?',
         'answer': 'Yes. Entities other than companies follow the AS prescribed by ICAI, not Ind AS.'},
        {'id': 'j2', 'title': 'Responding to an exposure draft', 'role': 'Technical team member at a CA firm',
         'situation': 'ASB has issued an exposure draft revising a standard. Your partner wants comments from the firm.',
         'steps': ['Read the draft and compare it with the existing standard.',
                   'Test it on two or three clients\' real transactions to see the practical effect.',
                   'Draft comments: unclear definitions, transition difficulties, conflict with any law.',
                   'Send the comments before the deadline.'],
         'takeaway': 'The exposure-draft stage gives practitioners a real voice in standard setting.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'Accounting Standards deal with recognition, measurement, presentation and:', 'options': ['Disclosure', 'Taxation', 'Auditing', 'Costing'], 'answer': 0, 'explain': 'The four aspects are recognition, measurement, presentation and disclosure.', 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'The Accounting Standards Board was constituted by ICAI in:', 'options': ['1977', '1949', '1991', '2006'], 'answer': 0, 'check': '1977', 'explain': 'ICAI set up the ASB in 1977. (1949 is the year of the Chartered Accountants Act; 2006 is when ICAI began moving towards IFRS.)', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm3', 'q': 'Which is a limitation of Accounting Standards?', 'options': ['They cannot override the statute', 'They reduce confusing variations in treatment', 'They may require extra disclosure', 'They improve comparability'], 'answer': 0, 'explain': 'Standards must be framed within existing laws — restricted scope. The others are benefits.', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'Ind AS apply to:', 'options': ['All listed companies, and unlisted companies with net worth of ₹250 crore or more', 'All partnership firms', 'Only companies with net worth below ₹250 crore', 'Only local bodies'], 'answer': 0, 'explain': 'Ind AS apply to listed companies and NBFCs and to unlisted companies/NBFCs with net worth of ₹250 crore or more.', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm5', 'q': 'A partnership firm follows:', 'options': ['Accounting Standards prescribed by ICAI', 'Ind AS', 'Companies (Accounting Standards) Rules, 2021', 'ASLB'], 'answer': 0, 'explain': 'Entities other than companies follow the AS prescribed by ICAI.', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm6', 'q': 'Which statement about the ASB is correct?', 'options': ['It is independent in formulating standards, and the Council cannot modify its draft without consulting it', 'It is a government department', 'It issues standards without any public consultation', 'It consists only of practising chartered accountants'], 'answer': 0, 'explain': 'ASB includes industry, regulators, academics and government representatives, and works independently through a consultative process.', 'concept': 'c3', 'difficulty': 'moderate'},
        {'id': 'm7', 'q': 'India decided, in relation to IFRS, to:', 'options': ['Converge with IFRS, keeping departures to the essential minimum', 'Adopt IFRS word for word', 'Ignore IFRS entirely', 'Apply IFRS only to partnership firms'], 'answer': 0, 'explain': 'The Government, in consultation with ICAI, chose convergence (Ind AS) rather than adoption.', 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm8', 'q': 'The main objective of Accounting Standards is to:', 'options': ['Harmonise diverse accounting policies so that financial statements become comparable', 'Increase the tax collected', 'Replace company law', 'Eliminate the need for audit'], 'answer': 0, 'explain': 'Standards remove non-comparability and provide standard policies, valuation norms and disclosures.', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm9', 'q': 'Which standard deals with Valuation of Inventories?', 'options': ['AS 2', 'AS 9', 'AS 10', 'AS 29'], 'answer': 0, 'explain': 'AS 2 — Valuation of Inventories. AS 9 is Revenue Recognition, AS 10 Property, Plant and Equipment, AS 29 Provisions, Contingent Liabilities and Contingent Assets.', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm10', 'q': 'Two identical firms report profits of ₹2,07,500 and ₹1,00,000 only because they use different depreciation and inventory methods. The difference is:', 'options': ['₹1,07,500', '₹3,07,500', '₹1,00,000', '₹2,07,500'], 'answer': 0, 'check': '207500-100000', 'explain': '2,07,500 − 1,00,000 = ₹1,07,500 — a gap caused purely by policy choice, which is why standards narrow alternatives and require disclosure.', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm11', 'q': 'At which stage does the general public get a formal chance to comment on a proposed standard?', 'options': ['Exposure draft', 'Identification of broad areas', 'Study-group preliminary draft', 'Final approval by the Council'], 'answer': 0, 'explain': 'The exposure draft is issued inviting public comments.', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm12', 'q': 'Do Accounting Standards eliminate all alternative accounting treatments?', 'options': ['No — they reduce alternatives within reasonable bounds', 'Yes — only one treatment is ever allowed', 'Yes — but only for partnership firms', 'No — they increase alternatives'], 'answer': 0, 'explain': 'Standards reduce alternatives within the bounds of rationality; some choice remains (e.g. inventory cost formula).', 'concept': 'c2', 'difficulty': 'moderate'},
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'text',
         'q': 'What are Accounting Standards? State the aspects they deal with and their objectives.',
         'model': [p('Accounting Standards are written policy documents issued by an expert accounting body, the government or another regulatory body, laying down how transactions and events are to be treated in financial statements so that statements of different enterprises are comparable.'),
                   ul(['Recognition of transactions and events in the financial statements.', 'Measurement of those transactions and events.', 'Presentation in a meaningful, understandable manner.', 'Disclosure needed for stakeholders and potential investors to understand the statements and take informed decisions.']),
                   p('Objectives: to harmonise diverse accounting policies and practices by (i) eliminating non-comparability of financial statements, thereby improving their reliability, and (ii) providing a common set of accounting policies, valuation rules and disclosure requirements — reducing the alternatives within reasonable limits.')],
         'scheme': [
             {'id': 's1', 'pt': 'Meaning of Accounting Standards', 'm': 1, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Four aspects: recognition, measurement, presentation, disclosure', 'm': 2, 'skill': 'concept'},
             {'id': 's3', 'pt': 'Objective (i): remove non-comparability / improve reliability', 'm': 1, 'skill': 'concept'},
             {'id': 's4', 'pt': 'Objective (ii): standard policies, valuation norms, disclosure requirements', 'm': 1, 'skill': 'concept'},
         ],
         'remarks': ['Most candidates remember three of the four aspects — presentation is the one usually missed.', 'Objectives should be written as two clear points.'],
         'mistakes': ['Saying standards are laws passed by Parliament.', 'Mixing up objectives with benefits.'],
         'tips': ['Definition (1 line) → four aspects (bullets) → two objectives (bullets).']},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'State the benefits and limitations of Accounting Standards.',
         'model': [p('Benefits:'),
                   ul(['They reduce, to a reasonable extent, or eliminate confusing variations in accounting treatments.', 'They may require disclosures beyond those required by law.', 'They help, to a limited extent, to compare financial statements of companies within a country and in different countries (differences in institutions, traditions and legal systems still cause standards to vary).']),
                   p('Limitations:'),
                   ul(['Choosing between alternative treatments can be difficult, since each may have strong arguments.', 'Restricted scope — standards cannot override the statute and must be framed within prevailing laws.'])],
         'scheme': [
             {'id': 's1', 'pt': 'Reduce/eliminate confusing variations', 'm': 1, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Additional disclosure beyond law; comparability (any one more benefit)', 'm': 1, 'skill': 'concept'},
             {'id': 's3', 'pt': 'Difficulty in choosing between alternatives', 'm': 1, 'skill': 'concept'},
             {'id': 's4', 'pt': 'Cannot override statute (restricted scope)', 'm': 1, 'skill': 'concept'},
         ],
         'remarks': ['Candidates often list only benefits; the two limitations carry half the marks.'],
         'mistakes': ['Saying standards make statements fully comparable across all countries.'],
         'tips': ['Use two headings — Benefits and Limitations — with bullets under each.']},
        {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'Describe the procedure followed by the Accounting Standards Board of ICAI in formulating Accounting Standards.',
         'model': [p('ICAI constituted the ASB in 1977. ASB includes representatives of industry (ASSOCHAM, CII, FICCI), regulators, academicians and government departments, considers IFRS and adapts them to Indian law, customs and business conditions. The procedure is:'),
                   proc_tbl,
                   p('ASB is independent in formulating standards; the Council cannot modify a draft without consulting ASB.')],
         'scheme': [
             {'id': 's1', 'pt': 'ASB 1977, composition and independence', 'm': 1, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Identification of areas and study-group preliminary drafts', 'm': 1, 'skill': 'concept'},
             {'id': 's3', 'pt': 'Consideration/revision by ASB and circulation to Council members and outside bodies', 'm': 1, 'skill': 'concept'},
             {'id': 's4', 'pt': 'Meeting representatives; exposure draft for public comment', 'm': 1, 'skill': 'concept'},
             {'id': 's5', 'pt': 'Consideration of comments; submission to Council', 'm': 1, 'skill': 'concept'},
             {'id': 's6', 'pt': 'Council approval (modification only with ASB) and issue — ICAI for non-corporates, Central Government for companies', 'm': 1, 'skill': 'concept'},
         ],
         'remarks': ['The steps must be in the correct sequence; jumbled steps lose marks even if all are mentioned.', 'Naming the outside bodies (SEBI, C&AG, CBDT etc.) adds credibility.'],
         'mistakes': ['Putting the exposure draft before consultation with outside bodies.', 'Saying the Council can change a draft on its own.'],
         'tips': ['Number the steps 1 to 9.', 'Begin with a line on ASB and end with who issues the standard.']},
    ]

    viva = [
        V('v1', 'What are Accounting Standards, and which aspects of transactions do they cover?',
          'Accounting Standards are written policy documents issued by an expert accounting body, the government or a regulator. They cover the recognition, measurement, presentation and disclosure of transactions and events in the financial statements.',
          [P('p1', 'Written policy documents issued by expert body / government / regulator', 2, 'written|document|issued|framework|rules|guidelines|policy', min=1),
           P('p2', 'Recognition', 2, 'recogni'),
           P('p3', 'Measurement', 2, 'measur|valu'),
           P('p4', 'Presentation', 2, 'present'),
           P('p5', 'Disclosure', 2, 'disclos')], 'c1'),
        V('v2', 'What are the objectives of Accounting Standards?',
          'The objective is to harmonise the different accounting policies and practices followed by entities. Standards aim to eliminate the non-comparability of financial statements, which improves their reliability, and to lay down a common set of accounting policies, valuation rules and disclosure requirements.',
          [P('p1', 'Harmonise / standardise diverse policies', 2, 'harmon|standardi|uniform|same polic|reduce alternative|reduce option|reduc', min=1),
           P('p2', 'Eliminate non-comparability / make statements comparable', 4, 'compar'),
           P('p3', 'Improve reliability', 1, 'reliab|trust|credib'),
           P('p4', 'Standard policies, valuation norms and disclosure requirements', 3, 'valuation|norm|rule', 'disclos', 'polic', min=2)], 'c2'),
        V('v3', 'State the benefits and limitations of Accounting Standards.',
          'Benefits are that standards reduce or eliminate confusing variations in accounting treatment, may require disclosure beyond what the law requires, and improve comparability of financial statements within and across countries to some extent. Limitations are that choosing between alternative treatments can be difficult, and that standards cannot override the statute.',
          [P('p1', 'Reduce confusing variations in treatment', 2, 'variation|uniform|reduce alternative|reduce option|standardi|confusion|confusing', min=1),
           P('p2', 'Additional disclosure / comparability', 3, 'disclos|compar', min=1),
           P('p3', 'Difficulty choosing between alternative treatments', 2, 'difficult|hard|choice|choos|alternative', min=1),
           P('p4', 'Cannot override the statute', 3, ALT('{n} overrid', '{n} over ride', '{n} go against', '{n} contrary', '{n} prevail', '{n} above law', '{n} above the law', '{n} overrule', 'within law', 'within the law', 'within statute', 'subject to law', 'subject to statute', 'law prevail', 'statute prevail', 'law overrid', 'statute overrid', 'restricted scope', n=('cannot', 'can not', 'can t', 'not', 'don t', 'do not', 'never')))], 'c2'),
        V('v4', 'Which sets of standards apply to different entities in India?',
          'There are three sets. Ind AS apply to all listed companies and NBFCs and to unlisted companies and NBFCs with net worth of 250 crore rupees or more. Other companies follow the Accounting Standards notified under the Companies (Accounting Standards) Rules, 2021. Entities other than companies, like partnership firms, follow the Accounting Standards issued by ICAI.',
          [P('p1', 'Ind AS: listed companies/NBFCs and unlisted with net worth ≥ ₹250 crore', 4, 'ind as|indian accounting standard|ind', 'listed|250|net worth', min=2),
           P('p2', 'Other companies: AS under Companies (Accounting Standards) Rules, 2021', 3, 'companies accounting standards rules|rules 2021|2021|companies rules|notified|other compan|remaining compan', min=1),
           P('p3', 'Non-company entities: AS issued by ICAI', 3, 'icai|institute', 'partnership|firm|non compan|non corporate|other than compan|sole|llp|entities other', min=2)], 'c4'),
        V('v5', 'Who formulates Accounting Standards in India and how?',
          'The Accounting Standards Board, constituted by ICAI in 1977, formulates them. It identifies areas, forms study groups to prepare drafts, circulates drafts to the Council and outside bodies such as SEBI and the C and AG for comments, issues an exposure draft for public comment, considers the comments and submits the final draft to the ICAI Council for approval. The standard is then issued, by ICAI for non-corporate entities and notified by the Central Government for companies.',
          [P('p1', 'Accounting Standards Board of ICAI (1977)', 3, 'accounting standards board|asb|board', 'icai|institute|1977', min=1),
           P('p2', 'Study groups prepare drafts; circulated to outside bodies', 2, 'study group|draft', 'circulat|outside bod|sebi|cag|cbdt|comment', min=2),
           P('p3', 'Exposure draft for public comment', 3, 'exposure draft|exposure|public comment|public'),
           P('p4', 'Council approval and issue (ICAI / Central Government for companies)', 2, 'council|central government|government|approv|notif|issue', min=1)], 'c3'),
        V('v6', 'Do Accounting Standards remove all alternative accounting treatments?',
          'No, they do not remove all alternatives. Accounting Standards reduce the accounting alternatives within reasonable limits and require disclosure of the policies followed, but some choice still remains, for example in the inventory cost formula.',
          [P('p1', 'No — they do not remove all alternatives', 4, ALT('{n} remov all', '{n} elimin all', '{n} all alternative', '{n} complet', '{n} entirely', '{n} fully', '{n} every', 'not all', 'no not', 'some choice', 'still remain', 'some alternative', n=('not', 'don t', 'do not', 'doesn t', 'cannot', 'can t', 'never'))),
           P('p2', 'They reduce alternatives within reasonable limits', 4, 'reduc|narrow|limit|minimi|fewer|cut down|restrict'),
           P('p3', 'Disclosure of policies; some choice remains (e.g. inventory formula)', 2, 'disclos|inventor|fifo|average|depreciation|choice|option|remain', min=1)], 'c2'),
    ]

    c = Checks()
    cases = [{
        'id': 'k1', 'title': 'Mehra Group — one family, many frameworks', 'difficulty': 'moderate',
        'case': ('The Mehra family controls: Mehra Motors Ltd, listed on the NSE (net worth ₹160 crore); Mehra Realty Pvt Ltd, unlisted (net worth ₹310 crore); Mehra Foods Pvt Ltd, unlisted (net worth ₹60 crore); and Mehra & Sons, a partnership firm. '
                 'The group CFO wants all four to follow "whatever is simplest" and also asks whether a standard can be ignored where the Companies Act requires a different treatment.'),
        'mcqs': [
            M('k1a', 'Which standards apply to Mehra Motors Ltd?', ['Ind AS', 'Companies (Accounting Standards) Rules, 2021', 'AS issued by ICAI', 'ASLB'], 0,
              'All listed companies follow Ind AS regardless of net worth.', 'core'),
            M('k1b', 'Which standards apply to Mehra Realty Pvt Ltd?', ['Ind AS', 'Companies (Accounting Standards) Rules, 2021', 'AS issued by ICAI', 'No standards apply to unlisted companies'], 0,
              'An unlisted company with net worth of ₹250 crore or more follows Ind AS.', 'moderate'),
            M('k1c', 'Which standards apply to Mehra Foods Pvt Ltd and to Mehra & Sons respectively?', ['Companies (AS) Rules, 2021; AS issued by ICAI', 'Ind AS; Ind AS', 'AS issued by ICAI; Companies (AS) Rules, 2021', 'Ind AS; AS issued by ICAI'], 0,
              'A company outside Ind AS follows the AS notified under the Companies (Accounting Standards) Rules, 2021; a partnership firm (non-company) follows ICAI\'s AS.', 'moderate'),
            M('k1d', 'If the Companies Act requires a treatment different from an Accounting Standard, which prevails?', ['The statute — standards cannot override the law', 'The Accounting Standard always', 'Whichever gives higher profit', 'Whichever the CFO prefers'], 0,
              'A limitation of standards is their restricted scope: they are framed within, and cannot override, the statute.', 'core'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch01', 'n': 7,
        'title': 'Accounting Standards',
        'outcomes': [
            'Explain what Accounting Standards are and the four aspects — recognition, measurement, presentation and disclosure — they deal with.',
            'State the objectives, benefits and limitations of Accounting Standards.',
            'Describe how the Accounting Standards Board of ICAI formulates standards.',
            'Identify which set of standards (Ind AS, Companies (AS) Rules 2021, or ICAI AS) applies to an entity, and recognise the main AS by title.',
        ],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 30}, 'prereq': ['fnd-p1-ch01-u05'],
                 'exam_tip': 'Short theory questions on objectives, benefits/limitations and the formulation procedure are common. The list of AS is for knowledge only — know the numbers of the main ones, but do not spend hours memorising titles.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Accounting Standards: written policy documents by an expert body/government/regulator covering recognition, measurement, presentation and disclosure.',
                        'Objectives: harmonise policies — remove non-comparability (improve reliability) and provide standard policies, valuation norms, disclosure requirements.',
                        'Benefits: fewer confusing variations; disclosure beyond law; some comparability within and across countries. Limitations: hard choices between alternatives; cannot override statute.',
                        'ASB set up by ICAI in 1977; consultative process ending in an exposure draft, Council approval and issue (ICAI for non-corporates; Central Government notification for companies).',
                        'Ind AS: listed companies/NBFCs + unlisted with net worth ≥ ₹250 crore. Companies (AS) Rules, 2021: other companies. ICAI AS: non-company entities.'],
            'remember': ['27 AS currently in the list (AS 6 and AS 8 absent).', 'India converged with IFRS (Ind AS), it did not adopt IFRS as is.', 'Lists of AS, Ind AS and ASLB are for knowledge, not syllabus.'],
            'traps': ['Standards reduce alternatives — they do not eliminate all of them.', 'The ICAI Council cannot change an ASB draft without consulting ASB.', 'Listing alone brings a company under Ind AS, regardless of net worth.'],
        },
        'quickref': [
            {'k': 'Four aspects', 'v': 'Recognition · Measurement · Presentation · Disclosure'},
            {'k': 'ASB', 'v': 'Constituted by ICAI in 1977; independent in formulating standards'},
            {'k': 'Ind AS', 'v': 'Listed companies & NBFCs; unlisted companies/NBFCs with net worth ≥ ₹250 crore'},
            {'k': 'Companies (AS) Rules, 2021', 'v': 'Companies not covered by Ind AS'},
            {'k': 'ICAI AS', 'v': 'Entities other than companies (firms, LLPs, proprietors, trusts)'},
            {'k': 'Key AS', 'v': 'AS 1 policies · AS 2 inventories · AS 9 revenue · AS 10 PPE · AS 29 provisions & contingencies'},
            {'k': 'Limitations', 'v': 'Difficult choice between alternatives · Cannot override statute'},
        ],
        'viva': viva, 'cases': cases,
    }
