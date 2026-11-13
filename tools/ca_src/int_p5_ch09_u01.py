"""CA Intermediate · Paper 5 Auditing and Ethics · Chapter 9 Special Features of Audit of Different Types of Entities.
Scope follows the ICAI study material; explanations, names and figures are original."""
from ikit import *

UID = 'int-p5-ch09-u01'
T1 = 'Government audit and the C&AG'
T2 = 'Local bodies, NGOs, trusts and co-operative societies'
T3 = 'Sole traders, firms and LLPs'
T4 = 'Educational institutions, hospitals, clubs, hotels and cinemas'
T5 = 'Hire purchase and leasing businesses'


def build():
    i1 = {'id': 'i1', 'title': 'Five lenses on Government spending', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A State department spent ₹3 crore on a new hospital wing. Explain what the C&AG\'s auditors would check under each of the five standards of expenditure audit.',
          'solution': [table(['Standard', 'Question asked'], [
              ['Audit against provision of funds', 'Was money provided in the budget and appropriated for this purpose, and was the limit respected?'],
              ['Audit of sanctions', 'Did a competent authority sanction the expenditure, generally or specially?'],
              ['Audit against rules and orders', 'Was the spending in line with the Constitution, laws and financial rules (tendering, procurement)?'],
              ['Propriety audit', 'Was it prudent — no more than the occasion demanded, not for anyone\'s personal benefit, and not wasteful?'],
              ['Performance audit', 'Is the wing being used and delivering the expected health outcomes economically and efficiently?']], title='Expenditure audit')],
          'checks': []}

    i2 = {'id': 'i2', 'title': 'Entity-specific checks', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'List two special audit checks for each: (a) a school; (b) a hospital; (c) a club; (d) a hotel; (e) a co-operative society.',
          'solution': [table(['Entity', 'Special checks'], [
              ['(a) School', 'Fee receipts traced to class registers and fee concessions approved; Government grants used as per conditions'],
              ['(b) Hospital', 'Bills reconciled with patient register and bed occupancy; medicine stock and expiry controls'],
              ['(c) Club', 'Subscriptions vouched with members\' register and arrears reviewed; bar and catering stock and receipts'],
              ['(d) Hotel', 'Room revenue compared with occupancy records; kitchen consumption against food sales and stock'],
              ['(e) Co-operative society', 'Compliance with the State Co-operative Societies Act, by-laws and bye-law limits on loans; overdue loans and members\' deposits']], title='Special features')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'The Comptroller and Auditor General (C&AG) is appointed by the President under Article 148 and can be removed only like a Supreme Court judge — by both Houses, each with a two-thirds majority of members present and voting, on proven misbehaviour or incapacity. The C&AG (Duties, Powers and Conditions of Service) Act, 1971 fixes tenure and gives a salary equal to a Supreme Court judge, protecting independence.',
            'Expenditure audit has five standards: audit against provision of funds, audit of sanctions, audit against rules and orders, propriety audit and performance audit. The C&AG also audits receipts, stores and inventories, and commercial accounts of Government companies and corporations (appointing their auditors and conducting supplementary audit).',
            'Reports on Union accounts go to the President and on State accounts to the Governor, to be laid before the legislature; the Public Accounts Committee examines them.'],
          'Government audit asks not only "was it legal?" but "was it wise and did it work?"',
          'Buying a costly car for an official\'s private trips may be within budget but fails the propriety test.'),
        C('c2', T2, [
            'Local bodies (municipalities, panchayats) are audited by the Examiner of Local Fund Accounts or other bodies under State laws; checks include budget compliance, collection of taxes and rates, grants used for purpose, and works contracts.',
            'NGOs: verify registration and foreign contribution approvals, utilisation of grants as per donors\' terms, separate funds, and receipts and payments with supporting evidence.',
            'Trusts and societies: check the trust deed or bye-laws, investments as per law, income applied to objects, and approvals for expenditure. Co-operative societies: audit under section 17 of the respective Act or the Multi-State Co-operative Societies Act, 2002; the auditor reports on irregular loans, overdue debts, ultra vires transactions and classifies the society by audit grade.'],
          'For public-interest entities, the auditor checks that money was used for the purpose for which it was given.',
          'A grant for a girls\' hostel used to repair the office building is an irregular diversion.'),
        C('c3', T3, [
            'Sole trader: audit is voluntary (unless required by tax law); the engagement letter defines scope, and the auditor watches for mixing of personal and business transactions.',
            'Partnership firm: read the partnership deed for capital, profit sharing, interest, salaries and authority; check that partners\' drawings and remuneration follow it, and that changes in constitution are properly accounted.',
            'LLP: audit is required under the LLP Act subject to limits; the auditor reads the LLP agreement, checks contributions, designated partners\' compliance and the Statement of Account and Solvency.'],
          'In owner-run businesses, the deed or agreement is the auditor\'s rulebook.',
          'Interest on capital paid at 15% where the deed allows 12% is a non-compliance to report.'),
        C('c4', T4, [
            'Educational institutions: fee receipts against admissions and class registers; scholarships and concessions authorised; grants and their conditions; salaries against appointment orders; hostel and library records.',
            'Hospitals: billing for rooms, procedures and medicines; patient register and discharge records; drug stores and expiry; equipment usage; donations and their utilisation.',
            'Clubs: members\' register, subscriptions and arrears, entrance fees, bar and canteen stock and sales, and approval of expenditure by the committee. Hotels: room occupancy and billing, food and beverage costing and stock, credit to guests, and payments to staff. Cinemas: ticket sales against seating capacity and ticket stubs, entertainment-related taxes, film hire contracts and advertising income.'],
          'Each industry has its own "unit of revenue" — seat, room, patient, student, member — which the auditor reconciles.',
          'A cinema\'s ticket revenue should not exceed seats × shows × average rate.'),
        C('c5', T5, [
            'Hire purchase and leasing businesses: check agreements, credit approval, instalment schedules and recovery, and repossession records.',
            'Recognition of finance income and classification of assets (stock on hire, leased assets) follow applicable accounting standards; overdue instalments and provisioning require attention.',
            'Verify that assets given on hire or lease exist, are insured and are in the hirer\'s or lessee\'s possession.'],
          'In financing businesses, the risk sits in recoverability of instalments.',
          'A rising number of repossessed vehicles signals weak credit approval.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Audit of a charitable trust', 'role': 'Audit assistant',
             'situation': 'A trust receives donations and a foreign grant for a rural school.',
             'steps': ['Read the trust deed and registration documents.', 'Verify donations with receipts and bank credits.', 'Check foreign contribution routed through the designated account.', 'Confirm spending matches the grant\'s purpose.'],
             'takeaway': 'Purpose-restricted money must be traceable from receipt to use.'}]

    mcqs = [
        Q('m1', 'The C&AG is appointed by:', ['The President of India', 'The Prime Minister', 'Parliament', 'The Chief Justice'], 0,
          'Article 148 provides for appointment by the President. In practice: removal is like that of a Supreme Court judge.', 'c1', T1),
        Q('m2', 'Checking that expenditure was not more than the occasion demanded is:', ['Propriety audit', 'Audit of sanctions', 'Audit against provision of funds', 'Performance audit'], 0,
          'Propriety audit applies principles of financial prudence. In practice: it looks beyond legality.', 'c1', T1),
        Q('m3', 'Checking whether a scheme achieved its intended results economically is:', ['Performance audit', 'Propriety audit', 'Audit against rules and orders', 'Receipt audit'], 0,
          'Performance audit evaluates economy, efficiency and effectiveness. In practice: reports go to the legislature.', 'c1', T1),
        Q('m4', 'The C&AG\'s report on the accounts of a State is submitted to:', ['The Governor', 'The President', 'The Chief Minister', 'The High Court'], 0,
          'Reports on State accounts go to the Governor to be laid before the State legislature. In practice: Union reports go to the President.', 'c1', T1),
        Q('m5', 'For a partnership firm, the key document the auditor studies first is:', ['The partnership deed', 'The memorandum of association', 'The trust deed', 'The bye-laws'], 0,
          'The deed governs capital, profit sharing, interest and remuneration. In practice: note authority of partners.', 'c3', T3),
        Q('m6', 'Audit of a co-operative society is conducted under:', ['The relevant Co-operative Societies Act', 'The Companies Act, 2013', 'The LLP Act', 'The Income-tax Act only'], 0,
          'State Acts (or the Multi-State Co-operative Societies Act, 2002) govern audit. In practice: auditors also award grades.', 'c2', T2),
        Q('m7', 'In a hotel audit, room revenue is best tested against:', ['Occupancy records', 'Kitchen stock', 'Fixed asset register', 'Bank loan agreements'], 0,
          'Rooms occupied × tariff should support room revenue. In practice: check complimentary rooms.', 'c4', T4),
        Q('m8', 'In a cinema audit, ticket sales are checked against:', ['Seating capacity, shows and ticket stubs', 'Film hire contracts only', 'Electricity bills', 'Staff attendance'], 0,
          'Capacity and stubs provide an upper limit and a trail for revenue. In practice: online bookings add another source.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Funds and sanctions', 2, 'concept', 'provision|sanction'), S('s2', 'Rules and propriety', 2, 'concept', 'rules|propriety'), S('s3', 'Performance', 1, 'concept', 'performance')],
          ['Explain each standard with the example.'], ['Confusing propriety with legality.'], ['Table.'], pad='table'),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'School', 1, 'concept', 'fee'), S('s2', 'Hospital', 1, 'concept', 'patient|occupancy'), S('s3', 'Club', 1, 'concept', 'subscription|member'),
           S('s4', 'Hotel', 1, 'concept', 'room|occupancy'), S('s5', 'Co-operative', 1, 'concept', 'co-operative|by-law|loan')],
          ['Give two per entity.'], ['Generic points only.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'How is the C&AG\'s independence protected?', 'He is appointed by the President, removable only like a Supreme Court judge, has a fixed tenure and a salary equal to a Supreme Court judge that cannot be varied to his disadvantage.',
          [P('p1', 'Removal like judge', 5, 'judge'), P('p2', 'Tenure and salary', 5, 'tenure|salary')], 'c1'),
        V('v2', 'What is audit against provision of funds?', 'Checking that expenditure is covered by an appropriation authorised by the competent authority and stays within its limit.',
          [P('p1', 'Appropriation', 5, 'appropriation|provision'), P('p2', 'Within limit', 5, 'limit')], 'c1'),
        V('v3', 'Name two special points in an NGO audit.', 'Use of grants as per donor conditions and compliance with registration and foreign contribution requirements.',
          [P('p1', 'Grant utilisation', 5, 'grant|donor'), P('p2', 'Registration', 5, 'registration|foreign')], 'c2'),
        V('v4', 'What does a partnership deed tell the auditor?', 'The capital, profit-sharing ratio, interest on capital, partners\' salaries and powers, which the accounts must follow.',
          [P('p1', 'Profit sharing', 5, 'profit|ratio'), P('p2', 'Interest or salary', 5, 'interest|salar')], 'c3'),
        V('v5', 'Give one revenue check for a hospital.', 'Reconciling patient bills with the admission and discharge register and bed occupancy records.',
          [P('p1', 'Bills', 5, 'bill'), P('p2', 'Register or occupancy', 5, 'register|occupancy')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Green Valley Club', 'difficulty': 'core',
              'case': 'Green Valley Club has 600 members paying ₹6,000 a year. Recorded subscriptions are ₹31 lakh. The bar shows sales of ₹18 lakh against purchases of ₹16 lakh with no closing stock record. The committee approved a ₹5 lakh renovation, but ₹8 lakh was spent.',
              'mcqs': [
                  M('k1a', 'Expected subscriptions:', ['₹36 lakh', '₹31 lakh', '₹30 lakh', '₹6 lakh'], 0,
                    '600 × ₹6,000 = ₹36 lakh; a ₹5 lakh gap needs explanation (arrears, waivers or leakage). In practice: check members\' register.', 'core', check=36, topic=T4),
                  M('k1b', 'The bar figures suggest:', ['Need to verify stock and margins — possible leakage', 'Nothing unusual', 'Over-collection', 'A tax issue only'], 0,
                    'A gross margin of only about 11% with no stock record is a red flag. In practice: count stock and compare expected margins.', 'moderate', topic=T4),
                  M('k1c', 'Spending ₹8 lakh against ₹5 lakh approval is:', ['An unauthorised excess to report', 'Acceptable', 'A capital receipt', 'Irrelevant'], 0,
                    'Expenditure must be approved by the committee; the excess lacks authority. In practice: seek ratification.', 'core', topic=T4),
                  M('k1d', 'The basic register to vouch subscriptions is:', ['The members\' register', 'The stock register', 'The fixed asset register', 'The cash book only'], 0,
                    'The members\' register shows who should pay. In practice: reconcile with receipts.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p5', 'int-p5-ch09', 1, 'Special Features of Audit of Different Type of Entities',
                ['Explain the C&AG\'s role and Government audit standards.',
                 'Identify special audit features of local bodies, NGOs, trusts and co-operatives.',
                 'Audit sole traders, firms and LLPs.',
                 'Apply industry-specific checks for schools, hospitals, clubs, hotels, cinemas and financing businesses.'],
                {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 25}, 'prereq': ['int-p5-ch08-u01'],
                 'exam_tip': 'For entity-specific questions, start with the governing document (Act, deed, bye-laws) and the main revenue source.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['C&AG: Art. 148; 1971 Act; five expenditure audit standards.',
                             'Local bodies, NGOs, trusts: grants used for purpose.',
                             'Co-operatives: State Acts or Multi-State Act 2002; audit grading.',
                             'Firms and LLPs: deed or agreement is the rulebook.',
                             'Industry checks: rooms, seats, patients, students, members.'],
                 'remember': ['Propriety audit tests prudence, not legality.'],
                 'traps': ['C&AG reports on States go to the Governor.']},
                [('Art. 148', 'C&AG'), ('1971 Act', 'Duties and powers'), ('Propriety', 'Prudence'), ('Performance', 'Results')],
                viva, cases)
