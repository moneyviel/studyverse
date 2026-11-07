"""CA Foundation · Paper 1 Accounting · Chapter 1 Theoretical Framework · Unit 1 Meaning and Scope of Accounting.
Original explanations, examples and questions (structure and scope follow the ICAI study material)."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p1-ch01-u01'


def build():
    # ---------------- Illustration 1: transactions, events and the surplus ----------------
    c1 = Checks()
    sur = c1.add('210000+25000-180000-8000-2000', 'Surplus of Ritu Mobile Accessories for May')
    c1.add('210000+25000', 'Value of goods sold plus goods still in hand')
    c1.add('180000+8000+2000', 'Total outgoings charged')
    surplus_tbl = table(['Particulars', 'Amount (₹)'], [
        ['Goods sold during May', '2,10,000'],
        ['Add: Goods still lying in the shop on 31 May', '25,000'],
        ['Less: Goods bought during May', '-1,80,000'],
        ['Less: Shop rent for May', '-8,000'],
        ['Less: Electricity for May', '-2,000'],
        ['Surplus (profit) for May', inr(sur)],
    ], num=[1], total=True, title='Statement of surplus — Ritu Mobile Accessories, May 2026')
    te_tbl = table(['Item', 'Transaction or event?', 'Reason'], [
        ['Ritu brings ₹3,00,000 into the business', 'Transaction', 'An exchange/agreement between Ritu and her business'],
        ['Goods bought and goods sold', 'Transaction', 'Dealings with suppliers and customers'],
        ['Rent and electricity paid', 'Transaction', 'Payments made under an agreement'],
        ['Goods worth ₹25,000 still in hand on 31 May', 'Event', 'A result (a position) that follows from the purchases and sales'],
        ['Surplus of ₹' + inr(sur) + ' earned', 'Event', 'The outcome of all the month\'s transactions'],
    ], title='Transactions versus events')

    # ---------------- Illustration 2: the six steps of the accounting procedure ----------------
    steps_tbl = table(['Stage', 'What Sahil Caterers does', 'Book / output'], [
        ['1. Recording', 'Enters each catering bill, supplier invoice and wage slip in date order', 'Journal / subsidiary books'],
        ['2. Classifying', 'Collects all wage payments under one head, all gas bills under another, and so on', 'Ledger'],
        ['3. Summarising', 'Prepares the trial balance and then the profit and loss account and balance sheet', 'Financial statements'],
        ['4. Analysing', 'Groups items (fixed assets together, current assets together) and works out relationships such as food cost to sales', 'Analysed statements, ratios'],
        ['5. Interpreting', 'Explains why food cost rose from 38% to 45% of sales and what it means for profit', 'Comments and explanations'],
        ['6. Communicating', 'Sends a short report with charts to the owners and the bank', 'Reports to users'],
    ], title='Generating and using financial information', note='Stages 1–2 (with the trial balance) are book-keeping; stages 3–6 are accounting proper.')

    # ---------------- Illustration 3: users and their questions ----------------
    users_tbl = table(['User', 'Internal / external', 'What they want to know from the accounts of Nimbus Foods Ltd'], [
        ['Management (directors, managers)', 'Internal', 'Which product line earns most, whether to open a new plant, where costs can be cut'],
        ['Employees', 'Internal', 'Is the company stable enough to pay salaries, bonus and retirement benefits and to grow jobs?'],
        ['Investors (present and prospective shareholders)', 'External', 'Should we buy, hold or sell the shares? Can the company keep paying dividends?'],
        ['Lenders (banks, debenture holders)', 'External', 'Will interest and the loan principal be repaid on time?'],
        ['Suppliers and trade creditors', 'External', 'Can the company pay our bills? How much credit, at what terms?'],
        ['Customers', 'External', 'Will the company keep supplying us — is it likely to survive?'],
        ['Government and its agencies', 'External', 'Tax payable, compliance with regulations, data for policy'],
        ['Public', 'External', 'Local employment, purchases from local suppliers, environmental impact'],
    ], title='Users of accounting information')

    # ---------------- Question models ----------------
    q1_tbl = table(['Basis', 'Book-keeping', 'Accounting'], [
        ['Stage', 'Recording phase — journal, ledger and trial balance', 'Summarising, analysing, interpreting and communicating phase'],
        ['Relationship', 'The base on which accounting rests', 'Begins where book-keeping ends; called the language of business'],
        ['Financial statements', 'Not prepared at this stage', 'Prepared from book-keeping records'],
        ['Use for decisions', 'Records alone do not support managerial decisions', 'Management takes decisions on the basis of accounting reports'],
        ['Sub-fields', 'None', 'Financial, management, cost, social responsibility and human resource accounting'],
        ['Financial position', 'Cannot be known from the books alone', 'Shown by the balance sheet prepared in accounting'],
    ])
    q3_tbl = table(['Discipline', 'How it connects with accounting'], [
        ['Economics', 'Both deal with scarce resources and decisions. Accountants borrowed ideas of value, income and capital from economists but made them workable — e.g. an asset is recorded at acquisition cost instead of the present value of all its future earnings, which cannot be estimated reliably. Accounting data of firms (micro) add up to the national (macro) data economists use.'],
        ['Statistics', 'Accounts are exact to the paisa; decisions often need only approximations, averages and trends. Ratios, time-series and cross-section comparisons and models that predict sickness of a firm rest on statistical methods applied to accounting data.'],
        ['Mathematics', 'Double entry can be written algebraically. Interest, annuities, depreciation, instalments, lease rentals, sinking funds and ratios all need arithmetic and algebra; computers allow matrix methods; graphs need geometry.'],
        ['Law', 'Transactions are governed by the Contract Act, Sale of Goods Act, Negotiable Instruments Act, etc. The Companies Act prescribes the format of company financial statements; banks, insurers and electricity companies follow their own Acts. Law shapes accounting, and accounting knowledge shapes the law.'],
        ['Management', 'Much accounting information is produced for management decisions; accountants sit in the management team and design the system to serve its needs.'],
    ])

    concepts = [
        {'id': 'c1', 'title': 'Transactions, events and why we keep accounts',
         'body': ['Every person and organisation — a household, a club, a shop, a company, a municipal body, the government — carries on economic activity. That activity happens through transactions (dealings such as buying, selling, paying, borrowing) and events (results that follow from transactions, such as a profit for the year or goods remaining in stock).',
                  'Anyone running such an activity wants to know its result and position, and to decide what to do next. Accounting grew up to meet exactly this need: it measures inflows and outflows of economic resources and turns them into information for decisions. Because it is the common medium through which business results are conveyed, accounting is called the language of business.'],
         'blocks': [te_tbl],
         'analogy': 'A cricket match is made of balls bowled (transactions); the score at the end of an over or the result of the match is an event. You need the ball-by-ball record to know the result.',
         'work': 'When a CA starts a new engagement, the first question is: which transactions and events of this client must be captured, and from which documents? Missing a category (say, credit card sales) means the result you report is wrong.'},
        {'id': 'c2', 'title': 'Meaning of accounting — from record-keeping to communication',
         'body': ['Early definition (AICPA Committee on Terminology, 1961): accounting was described as an art — the art of putting on record, grouping and condensing, in money terms, those transactions and events which are at least partly financial, and then interpreting what they show. It treats accounting mainly as record keeping that ends with interpretation.',
                  'Wider definition (American Accounting Association, 1966): accounting is the process of identifying, measuring and communicating economic information so that users can make informed judgements and decisions. Communication was added because ownership and management separated, business became global and society took more interest in enterprises.',
                  'APB (AICPA), 1970, stated the function of accounting as providing quantitative, mainly financial, information about economic entities that is useful for economic decisions.',
                  'Working definition: accounting is the process of recording, classifying, summarising, analysing and interpreting financial transactions and communicating the results to persons interested in them. Only items measurable in money and of a financial character are recorded — opening a new bank branch is not recorded, but the business it brings in is.'],
         'analogy': 'Old view: a diary-writer who records and comments. Modern view: a news reporter who also has to make sure the right audience gets the story in a form it can use.',
         'work': 'Clients rarely ask a CA for "books"; they ask "can I afford this loan?" or "why did profit fall?". The modern definition — information for decisions — is what the profession is paid for.'},
        {'id': 'c3', 'title': 'Procedure, objectives and functions of accounting',
         'body': ['Procedure — generating information: (1) recording in the journal or subsidiary books, from documents such as bills, pass books, salary slips; (2) classifying into ledger accounts; (3) summarising into financial statements. Using information: (4) analysing — methodically regrouping the figures and establishing relationships; (5) interpreting — explaining what the relationships mean, why things happened and what may happen; (6) communicating — sending reports, ratios, graphs and statements to users.',
                  'Objectives: systematic recording of transactions; ascertaining the result (profit or loss) through the profit and loss account; ascertaining the financial position through the balance sheet; providing information to users for rational decisions; and knowing the liquidity (short-run) and solvency (long-run) position.',
                  'Functions: measurement of past performance and present position; forecasting; decision-making; comparison and evaluation against targets; control (spotting weaknesses and checking that corrective steps work); and supporting government regulation and taxation.'],
         'blocks': [steps_tbl],
         'analogy': 'A doctor\'s visit: recording symptoms, sorting them, summarising in a report, analysing test results, interpreting the diagnosis and finally explaining it to the patient.',
         'work': 'In month-end closing at a company, accountants record and classify (book-keeping); the finance manager summarises and analyses; the CFO interprets and communicates to the board. Knowing which stage you are responsible for tells you what output is expected of you.'},
        {'id': 'c4', 'title': 'Evolution of accounting as a social science',
         'body': ['History: around 4000 BC Egyptian treasury keepers sent daily reports to Wazirs and monthly reports to the king; Babylonia used accounts to detect losses from fraud and inefficiency; Greece used them to divide revenue among treasuries; Rome kept memorandum or day books of receipts and payments (700 BC–400 AD); China had advanced government accounting by about 2000 BC. In India, Kautilya\'s Arthashastra described how records should be kept.',
                  'Luca Pacioli, a Franciscan friar, published Summa de Arithmetica, Geometria, Proportioni et Proportionalita in Venice in 1494 — regarded as the first printed book on double-entry book-keeping. Debit comes from the Italian debito (Latin debere — owed), credit from credito (Latin credo — trust or belief).',
                  'Phases: (1) stewardship accounting — stewards accounting to wealthy owners, the root of financial accounting; (2) financial accounting — joint stock companies separated ownership from management, so law required disclosure of the profit and loss account and balance sheet to protect investors; (3) management accounting — a 20th-century development serving management decisions; (4) social responsibility accounting — still forming, it aims to report the social costs (pollution, use of society\'s resources) and social benefits (employment, better products) of a business.',
                  'Why a social science: social sciences study people in society and the results of social relationships. Accounting is judged by its usefulness to society as a whole — it produces information for social good, contributes to social progress and keeps changing as society changes.'],
         'analogy': 'Like language itself: it began as simple tally marks for a few people and grew, as society grew, into a shared system everyone relies on.',
         'work': 'Today\'s sustainability and CSR reports that listed companies publish are the modern face of social responsibility accounting; CAs are increasingly asked to prepare and assure them.'},
        {'id': 'c5', 'title': 'Book-keeping, accounting and accountancy; sub-fields',
         'body': ['Book-keeping is the orderly recording of financial data — the procedural, record-keeping part. Its objectives are a complete, permanent record of all transactions and knowing their combined effect on the business. Recording and classifying (with the trial balance) are book-keeping; preparing, analysing, interpreting and communicating financial statements are accounting. Accounting starts where book-keeping ends. Accountancy is the widest term, containing accounting, which in turn contains book-keeping.',
                  'Legal angle: companies keep books and prepare statements under the Companies Act; banks and insurers under their special Acts. There is no specific statute prescribing books or formats for sole proprietors and partnership firms. (Write this in the exam. In practice, tax laws — income-tax and GST — do require many such businesses and professionals to keep books and records, but they do not lay down a format for the financial statements.)',
                  'Sub-fields: financial accounting (historical; ends in the profit and loss account and balance sheet), management accounting (internal reports for planning, control and decisions), cost accounting (ascertaining and controlling costs), social responsibility accounting (social costs and benefits) and human resource accounting (identifying, valuing and reporting the investment in people, which conventional accounts ignore).'],
         'blocks': [q1_tbl],
         'analogy': 'Book-keeping is collecting and labelling the ingredients; accounting is cooking the meal, tasting it and serving it; accountancy is the whole kitchen.',
         'work': 'Data-entry staff or software do most book-keeping today; employers hire CAs for the accounting part — judgement, analysis and communication. That is why your training focuses on the "why" behind every entry.'},
        {'id': 'c6', 'title': 'Users of accounting information',
         'body': ['Internal users: management (owners, directors, managers, partners) who use detailed, often confidential reports for decisions; employees are usually also counted as internal in the sense that they work inside the business.',
                  'External users rely on published financial statements: investors (buy, hold or sell; ability to pay dividends; owners of non-corporate firms decide whether to continue), lenders (repayment of principal and interest), suppliers and creditors (ability to pay; credit terms), customers (continuity of supply), government and its agencies (regulation, resource allocation, price control, taxes) and the public (contribution to the local economy).',
                  'Useful information stresses economic substance over technical form, is relevant, material and unbiased, and lets users judge its reliability and compare it with alternatives and past experience.'],
         'blocks': [users_tbl],
         'analogy': 'One set of accounts is like one X-ray seen by several specialists — each looks for what matters to their own decision.',
         'work': 'Before a bank sanctions a loan, its credit team reads the borrower\'s statements; before a vendor gives 60 days\' credit, it asks for the latest balance sheet. CAs prepare statements knowing who will read them and what they will look for.'},
        {'id': 'c7', 'title': 'Relationship with other disciplines and limitations of accounting',
         'body': ['Accounting overlaps economics, statistics, mathematics, law and management. A good accountant needs working knowledge of each, to use it directly or to know when to seek expert advice.',
                  'Limitations: (1) factors that cannot be measured in money — staff skill and loyalty — are left out; (2) the balance sheet shows the position on one date, while users want the future; (3) changes in the value of money (inflation) are ignored; (4) accounting principles sometimes conflict; (5) many figures rest on personal judgement — provision for doubtful debts, depreciation method, capital vs revenue, inventory valuation method; (6) human resources are not shown as assets for lack of an accepted valuation formula; (7) alternative policies for the same item open the door to manipulation — standards reduce, but cannot eliminate, the options.'],
         'blocks': [q3_tbl],
         'analogy': 'A photograph is accurate about the moment it was taken, but it cannot show what happens next or how the people in it feel. Financial statements have the same strengths and blind spots.',
         'work': 'An analyst reading two companies\' results first checks their accounting policies (depreciation, inventory) — the limitation "different policies for the same item" can make one company look better simply because of a choice of method.'},
        {'id': 'c8', 'title': 'Role of the accountant in society',
         'body': ['The profession is respected because it serves the public interest — turning silent figures into information that helps businesses plan and society progress. Goethe is said to have called it one of the finest inventions of the human mind.',
                  'Areas of service: maintenance of books of account; statutory audit (every company must appoint a CA or a firm of CAs to report whether the statements give a true and fair view; co-operatives and others under their laws or by choice); internal audit (reviewing systems, safeguards against leakage and misappropriation, and efficiency); taxation (compliance, representation before authorities, planning, and views on tax policy); management accounting and consultancy (MIS, cost control, investment appraisal, working capital, corporate planning); financial advice (investments, insurance, business expansion and mergers, investigations — e.g. why profits fell, whether fraud occurred, valuing a business or shares — and pension schemes); and other services such as secretarial work, share registration, company formation, receiverships and liquidations, and arbitration.'],
         'analogy': 'A CA is like a family doctor for money matters — routine check-ups (books, audit), specialist treatment (tax, investigations) and advice on healthy habits (planning).',
         'work': 'A typical small CA practice does all of these in a single week: GST returns for a trader, tax audit for a doctor, internal audit of a hospital, a valuation for a family settlement and advice on a startup\'s fund-raising.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Spotting transactions and events, and finding the surplus', 'difficulty': 'core', 'minutes': 8,
         'q': 'Ritu opened Ritu Mobile Accessories on 1 May 2026 with ₹3,00,000 of her own money. During May she bought goods for ₹1,80,000, sold goods for ₹2,10,000, paid shop rent ₹8,000 and electricity ₹2,000. On 31 May goods costing ₹25,000 remained unsold. (a) Classify the items as transactions or events. (b) Work out the surplus for May.',
         'solution': [te_tbl, surplus_tbl,
                      wn('Why the unsold goods are added', f'Goods bought (₹1,80,000) are charged in full, so the goods still in hand (₹25,000) are added back — otherwise the cost of unsold goods would reduce May\'s result. Surplus = 2,10,000 + 25,000 − 1,80,000 − 8,000 − 2,000 = ₹{inr(sur)}.'),
                      note('The ₹3,00,000 brought in by Ritu is capital, not income, so it does not enter the surplus.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Following the accounting procedure in a small business', 'difficulty': 'core', 'minutes': 6,
         'q': 'Sahil Caterers wants to understand what its accountant actually does. Explain, with an example of the firm\'s work at each stage, the six stages through which financial information is generated and used, and say which stages are book-keeping.',
         'solution': [steps_tbl, p('Book-keeping covers recording and classifying (and preparing the trial balance). Summarising into financial statements, analysing, interpreting and communicating form accounting.')]},
        {'id': 'i3', 'title': 'Who reads the accounts, and why', 'difficulty': 'core', 'minutes': 6,
         'q': 'Nimbus Foods Ltd is about to publish its annual accounts. Identify eight groups of users, state whether each is internal or external, and give the main question each group wants answered.',
         'solution': [users_tbl, note('In a non-corporate business (sole proprietor, partnership) ownership and management are usually the same people, but owners still use the accounts to decide whether to continue or close the business.')]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Explaining the accounts to a first-time borrower', 'role': 'Article assistant at a CA firm, supporting a loan application for a small manufacturer',
         'situation': 'Mr. Bansal runs a small packaging unit. The bank has asked for audited statements and projections. He asks you: "My books are written up every day by my clerk — why do I need you?"',
         'steps': ['Explain that his clerk does book-keeping — recording and classifying — and that the bank needs accounting: summarised statements, analysis and interpretation.',
                   'List what the bank (a lender) will look for: ability to repay principal and interest, liquidity, and the trend in profit.',
                   'Point out limitations he should be ready to explain: figures based on estimates (depreciation, doubtful debts) and items not in the books (his skilled staff, a long-standing customer base).',
                   'Prepare a short covering note that communicates the key numbers in plain words with a simple chart.'],
         'takeaway': 'Book-keeping produces data; accounting turns it into information a particular user can act on. The CA adds the summarising, analysis, interpretation and communication.',
         'think': 'Which two objectives of accounting matter most to the bank in this case?',
         'answer': 'Ascertaining the financial position (balance sheet) and knowing the liquidity and solvency position — the bank wants to know whether the loan can be repaid.'},
        {'id': 'j2', 'title': 'Choosing what to report to different users', 'role': 'Junior accountant in the finance team of a listed company',
         'situation': 'The CFO asks you to draft two reports from the same quarter\'s data: one for the board and one summary for publication.',
         'steps': ['For the board (internal users): product-wise margins, department costs, budget versus actual, cash forecasts — detailed and confidential.',
                   'For publication (external users): the statutory statements and key disclosures — summarised, in the prescribed format, without sensitive internal detail.',
                   'Check that both reports agree with the same ledger data so that the story told is consistent.'],
         'takeaway': 'Internal users get detailed management reports; external users get structured financial statements. Same data, different presentation.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'Which definition of accounting added "communicating" economic information to permit informed judgements and decisions?', 'options': ['American Accounting Association, 1966', 'AICPA Committee on Terminology, 1961', 'Luca Pacioli, 1494', 'Kautilya\'s Arthashastra'], 'answer': 0, 'explain': 'The 1966 American Accounting Association definition described accounting as identifying, measuring and communicating economic information so that users can make informed judgements and decisions. The trap is the 1961 AICPA definition: it was a big step forward but stopped at recording, classifying, summarising and interpreting — it did not stress communication to users. In practice: a CA preparing an annual report for a bank or investors is judged on how clearly the numbers communicate, not merely on whether they were recorded.', 'topic': 'Introduction', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'The book in which classified information is kept under separate account heads is the:', 'options': ['Ledger', 'Journal', 'Cash book', 'Trial balance'], 'answer': 0, 'explain': "Classification means grouping transactions of the same nature under one account head — all rent payments in Rent Account, all dealings with one customer in that customer's account — and this is done in the ledger. The tempting wrong answer is the journal: it is the book of original entry, where transactions are recorded date-wise, not grouped by head. In practice: when a Tally user opens a ledger such as 'Electricity Charges', the software is showing exactly this classified record.", 'topic': 'Book-keeping', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm3', 'q': 'Which of the following is an event rather than a transaction?', 'options': ['Profit earned for the year', 'Goods purchased on credit', 'Rent paid for the shop', 'Loan taken from a bank'], 'answer': 0, 'explain': "A transaction is an exchange with another party that can be measured in money, such as a purchase, a rent payment or a bank loan. Profit for the year is not an exchange with anyone; it is the result of all the year's transactions, so it is an event. The trap is to call anything with a money figure a transaction. In practice: an accountant records each invoice and payment as a transaction, while profit only appears when the books are closed at year end.", 'topic': 'Introduction', 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'The first printed book on double-entry book-keeping was written by:', 'options': ['Luca Pacioli', 'Kautilya', 'Goethe', 'R. J. Chambers'], 'answer': 0, 'explain': 'Luca Pacioli, an Italian mathematician, published Summa de Arithmetica in Venice in 1494; it contained the first printed description of double-entry book-keeping, which is why he is called the father of modern accounting. The tempting distractor is Kautilya: his Arthashastra describes how accounts should be kept, but it is an ancient Indian treatise, not a printed book on double entry. In practice: every Tally or ERP system used by Indian businesses today still follows the debit-credit logic Pacioli described.', 'topic': 'Evolution of Accounting as a Social Science', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm5', 'q': 'Management accounting as a branch of accounting is a development of the:', 'options': ['Twentieth century', 'Fifteenth century', 'Eighteenth century', 'Ancient Roman period'], 'answer': 0, 'explain': "Accounting began as stewardship (owners checking managers), grew into financial accounting with joint stock companies after the industrial revolution, and only in the twentieth century did management accounting develop to give managers information for planning, control and decisions. The trap is the fifteenth century — that is when double entry was first printed, not when management accounting arose. In practice: budgets, variance reports and product-wise profitability prepared in an Indian company's finance team are management accounting tools.", 'topic': 'Evolution of Accounting as a Social Science', 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm6', 'q': 'Accounting is treated as a social science mainly because:', 'options': ['Its usefulness to society as a whole is the basic test of its worth', 'It is exact to the last paisa', 'It uses mathematics', 'It is governed by the Companies Act'], 'answer': 0, 'explain': "A social science studies people living in society, and accounting is judged by how useful its information is to society — owners, lenders, employees, government and the public — so usefulness to society is the basic test of its worth. The tempting option is 'it uses mathematics': arithmetic is a tool, but using numbers does not make a subject a science of society. In practice: CSR spending disclosures required of large Indian companies show accounting adapting to what society expects.", 'topic': 'Evolution of Accounting as a Social Science', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm7', 'q': 'Which statement about book-keeping is correct?', 'options': ['It is the recording phase and provides the base for accounting', 'It includes preparation and interpretation of financial statements', 'It has several sub-fields such as cost accounting', 'Management decisions are taken directly from book-keeping records'], 'answer': 0, 'explain': 'Book-keeping is the recording phase — journalising, posting and balancing accounts — and it supplies the data on which accounting builds. Preparing and interpreting financial statements, the sub-fields such as cost accounting, and decision support all belong to accounting, which begins where book-keeping ends. The trap is thinking book-keeping includes preparing statements. In practice: a data-entry accountant in a small firm does the book-keeping, while the CA who finalises the accounts and advises the owner does the accounting.', 'topic': 'Book-keeping', 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm8', 'q': 'Lenders are mainly interested in accounting information to know:', 'options': ['Whether principal and interest will be repaid when due', 'The rate of dividend to be declared', 'The salary structure of employees', 'The local contribution of the enterprise'], 'answer': 0, 'explain': 'Lenders such as banks and debenture holders want to know whether the business can pay interest on time and repay the principal, so they study liquidity, solvency and cash flows. The tempting option, the rate of dividend, interests investors (shareholders), not lenders, who earn a fixed interest whatever the dividend. In practice: before sanctioning a working-capital loan, an Indian bank asks for audited accounts and checks ratios such as the debt-service coverage ratio.', 'topic': 'Users of Accounting Information', 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm9', 'q': 'The attempt to identify, quantify and report the investment made in an organisation\'s people is called:', 'options': ['Human resource accounting', 'Social responsibility accounting', 'Cost accounting', 'Stewardship accounting'], 'answer': 0, 'explain': "Human resource accounting tries to identify, measure and report the investment made in an organisation's people — recruitment, training and development — which conventional accounts ignore because people are not owned assets. The tempting option, social responsibility accounting, deals with the costs and benefits of a business's activities for society, not the value of its own staff. In practice: some Indian IT companies, Infosys being a well-known example, have voluntarily published human resource value figures alongside their annual reports.", 'topic': 'Book-keeping', 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm10', 'q': 'Which of these is a limitation of accounting?', 'options': ['It ignores changes in the purchasing power of money', 'It records transactions in money terms', 'It is based on documentary evidence', 'It helps in ascertaining profit'], 'answer': 0, 'explain': "Accounting records assets at the rupee amounts paid in different years and adds them together as if a rupee always had the same value, so it ignores changes in purchasing power caused by inflation. The tempting option is 'records transactions in money terms' — that is a basic feature (money measurement) that makes accounts possible, not a limitation in itself. In practice: land bought in 1995 for ₹5 lakh still appears at ₹5 lakh in many Indian balance sheets, though it may be worth crores today.", 'topic': 'Relationship of Accounting with Other Disciplines', 'concept': 'c7', 'difficulty': 'core'},
        {'id': 'm11', 'q': 'Every company must appoint a chartered accountant (or a firm) to report on whether its financial statements give a true and fair view. This service is:', 'options': ['Statutory audit', 'Internal audit', 'Management consultancy', 'Investigation'], 'answer': 0, 'explain': "Statutory audit is required by law: under the Companies Act, 2013, every company must appoint a chartered accountant or firm to report to the members whether its financial statements give a true and fair view. The tempting option, internal audit, is arranged by management to review internal controls and operations; it does not replace the statutory report. In practice: listed Indian companies publish the statutory auditor's report with their annual results, and banks rely on it before lending.", 'topic': 'Role of Accountant in the Society', 'concept': 'c8', 'difficulty': 'core'},
        {'id': 'm12', 'q': 'Statistical methods are used with accounting data mainly because:', 'options': ['Decisions often need trends and averages rather than exact individual figures', 'Accounting records are never exact', 'Accounting covers a period longer than statistics', 'The Companies Act requires statistical formats'], 'answer': 0, 'explain': "Accounting figures are exact to the rupee, but many decisions need broad patterns — averages, trends, ratios over several years — and statistical methods turn accounting data into such information. The trap is the option saying accounting records are never exact; in fact accounts aim for precision, which statistics does not require. In practice: an analyst forecasting a company's sales will use the past five years' accounting figures to compute growth trends and averages before building a valuation model.", 'topic': 'Relationship of Accounting with Other Disciplines', 'concept': 'c7', 'difficulty': 'moderate'},
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'table',
         'q': 'Distinguish between book-keeping and accounting.',
         'model': [q1_tbl, p('In short, book-keeping provides the data and accounting starts where book-keeping ends. Accountancy is the wider body of knowledge that contains both.')],
         'scheme': [
             {'id': 's1', 'pt': 'Book-keeping = recording phase; accounting = summarising/analysing/interpreting/communicating phase', 'm': 1, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Book-keeping is the base; accounting begins where book-keeping ends / language of business', 'm': 1, 'skill': 'concept'},
             {'id': 's3', 'pt': 'Financial statements and financial position come from accounting, not book-keeping', 'm': 1, 'skill': 'concept'},
             {'id': 's4', 'pt': 'Decisions taken on accounting reports; book-keeping records alone do not support them', 'm': 1, 'skill': 'concept'},
             {'id': 's5', 'pt': 'Sub-fields exist only in accounting (financial, management, cost etc.); answer presented as a table', 'm': 1, 'skill': 'presentation'},
         ],
         'remarks': ['Most candidates give two or three points and stop; five distinct bases are needed for five marks.', 'Points written as "book-keeping is narrow, accounting is wide" without explanation earn little.'],
         'mistakes': ['Treating the two terms as synonyms.', 'Putting the trial balance under accounting instead of book-keeping.', 'Writing the same idea twice in different words.'],
         'tips': ['Use a three-column table: Basis | Book-keeping | Accounting.', 'One mark per clear basis — aim for five or six bases.']},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': '"Accounting is the language of business, but like every language it has its limitations." Explain any four limitations of accounting.',
         'model': [ul(['Items not measurable in money — the skill, loyalty and morale of staff or the reputation of the management — are not recorded, even though they may be the most valuable resources of the business.',
                       'Historical and dated: the balance sheet shows the position on one particular date, while users want to judge the near and long-term future.',
                       'Ignores changes in the value of money: assets bought in different years at different price levels are added together as if a rupee were always worth the same.',
                       'Subjectivity: depreciation method, provision for doubtful debts, inventory valuation and the capital/revenue split depend on the accountant\'s judgement, so two accountants can show different profits.',
                       'Alternative policies for the same item increase the chance of manipulation; Accounting Standards reduce the choices but cannot bring them down to one.',
                       'Accounting principles sometimes conflict with one another.']),
                   p('Hence financial statements should be read carefully, keeping these factors in mind.')],
         'scheme': [
             {'id': 's1', 'pt': 'Non-monetary factors (e.g. human resources) not recorded', 'm': 1, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Position on a past date — not the future', 'm': 1, 'skill': 'concept'},
             {'id': 's3', 'pt': 'Inflation / changing value of money ignored', 'm': 1, 'skill': 'concept'},
             {'id': 's4', 'pt': 'Personal judgement or alternative policies / conflicting principles (any one, explained)', 'm': 1, 'skill': 'concept'},
         ],
         'remarks': ['Answers that only list headings without a line of explanation are awarded half marks per point.', 'Good answers give an example for each limitation, such as depreciation method for subjectivity.'],
         'mistakes': ['Writing objectives or functions of accounting instead of limitations.', 'Giving "it is time-consuming" or "it is costly" — these are not the limitations the examiner is looking for.'],
         'tips': ['Number each limitation and bold the key phrase.', 'Close with one line on why users must interpret statements carefully.']},
        {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'Explain the relationship of accounting with (a) economics, (b) statistics, (c) mathematics, (d) law and (e) management.',
         'model': [q3_tbl],
         'scheme': [
             {'id': 's1', 'pt': 'Economics: scarce resources/decisions; concepts of value, income, capital adapted (acquisition cost example); micro to macro data', 'm': 1.5, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Statistics: precision vs approximation; trends, ratios, comparisons', 'm': 1, 'skill': 'concept'},
             {'id': 's3', 'pt': 'Mathematics: algebra of double entry; interest, annuity, depreciation, instalments', 'm': 1, 'skill': 'concept'},
             {'id': 's4', 'pt': 'Law: transactions governed by laws; formats prescribed by Companies Act and special Acts; two-way influence', 'm': 1.5, 'skill': 'concept'},
             {'id': 's5', 'pt': 'Management: accounting data as the base for management decisions; accountant in the management team', 'm': 1, 'skill': 'concept'},
         ],
         'remarks': ['The economics part carries the most weight; the best answers mention the gap between the economist\'s and the accountant\'s idea of value with an example.', 'Many candidates write only "accounting uses law" — the two-way influence is what earns the full mark.'],
         'mistakes': ['Writing a general essay on each subject without linking it to accounting.', 'Leaving out management, which is the easiest mark.'],
         'tips': ['Use sub-headings (a) to (e) — examiners award marks part by part.', 'Give one concrete example under each discipline.']},
    ]

    viva = [
        V('v1', 'What is accounting according to the widely accepted modern definition?',
          'Accounting is the process of identifying, measuring and recording financial transactions, classifying and summarising them, analysing and interpreting the results, and communicating that information to users so that they can make informed judgements and decisions.',
          [P('p1', 'Identifying / recording transactions of financial character', 2, 'identif|record'),
           P('p2', 'Classifying and summarising (measuring)', 2, 'classif|summar|measur', min=1),
           P('p3', 'Analysing and interpreting the results', 2, 'analy|interpret', min=1),
           P('p4', 'Communicating the information to users', 2, 'communicat|report|convey|pass on|give|provide|present'),
           P('p5', 'So that users can make informed judgements and decisions', 2, 'decision|judgement|judgment|decide')], 'c2'),
        V('v2', 'How is book-keeping different from accounting?',
          'Book-keeping is the recording phase: it records and classifies transactions up to the trial balance and forms the base. Accounting starts where book-keeping ends; it prepares the financial statements, analyses and interprets them and communicates the results, and management takes decisions on that basis.',
          [P('p1', 'Book-keeping is the recording phase', 4, 'book keep record|bookkeep record|book keep only record|book keep concern record|book keep deal record|book keep mean record|book keep just record'),
           P('p2', 'Accounting summarises / prepares statements, analyses, interprets and communicates', 4, 'summar|financial statement|final account|analy|interpret|communicat'),
           P('p3', 'Accounting begins where book-keeping ends (book-keeping is its base)', 2, 'account start where book keep end|account begin where book keep end|book keep end account start|book keep end account begin|book keep base|base account|basis account|foundation|after book keep|book keep end', min=1)], 'c5'),
        V('v3', 'Name the users of accounting information and say what lenders and investors look for.',
          'Users are internal, like management and employees, and external, like investors, lenders, suppliers, customers, government and the public. Lenders want to know whether the principal and interest will be repaid on time. Investors want to decide whether to buy, hold or sell and whether the business can pay dividends.',
          [P('p1', 'Internal users: management, employees', 2, 'management|manager|owner|director|employee|staff|internal', min=1),
           P('p2', 'External users: investors, lenders, suppliers, customers, government, public', 2, 'supplier|creditor|vendor', 'customer|buyer', 'government|tax', 'public|society|community', 'external|outside', min=2),
           P('p3', 'Lenders: repayment of principal and interest on time', 3, 'interest|repay|pay back|paid back|return loan|loan back|principal', min=1),
           P('p4', 'Investors: buy, hold or sell; ability to pay dividends', 3, 'dividend|buy|sell|hold|return on investment|survive|prosper', min=1)], 'c6'),
        V('v4', 'Why is accounting called a social science, and what are the phases of its evolution?',
          'Accounting is a social science because its usefulness to society as a whole is the test of its value; it produces information for social good and changes as society changes. It evolved from stewardship accounting to financial accounting with joint stock companies, then management accounting in the twentieth century, and now social responsibility accounting.',
          [P('p1', 'Usefulness to society / social good is the basic test', 3, 'society|social good|social purpose|social progress|people|public', min=1),
           P('p2', 'Stewardship accounting came first', 2, 'steward'),
           P('p3', 'Financial accounting with joint stock companies', 2, 'financial account|joint stock|company|companies', min=1),
           P('p4', 'Management accounting, then social responsibility accounting', 3, 'management account|managerial account', 'social responsib|social cost|social account|csr', min=2)], 'c4'),
        V('v5', 'State any four limitations of accounting.',
          'First, things that cannot be measured in money, like the skill and loyalty of staff, are not recorded. Second, the balance sheet shows the position on a past date, not the future. Third, accounting ignores inflation, that is changes in the value of money. Fourth, many figures depend on personal judgement and different accounting policies can be chosen, which allows manipulation.',
          [P('p1', 'Non-monetary items (staff skill, loyalty, human resources) not recorded', 3, 'money|monetary|human resource|human asset|skill|loyalty|employee|staff', 'not record|not shown|not includ|ignor|left out|cannot|can t|exclud|not measur|not appear|no place', min=2),
           P('p2', 'Shows position on a past date, not the future', 2, 'past|histor|one date|particular date|certain date|old|future'),
           P('p3', 'Ignores inflation / change in value of money', 2, 'inflation|price level|price change|purchasing power|value of money|changing value'),
           P('p4', 'Personal judgement / estimates / alternative policies allow manipulation', 3, 'judg|estimat|subjectiv|alternative|different polic|different method|manipulat|choice|conflict', min=1)], 'c7'),
        V('v6', 'What services does a chartered accountant render to society?',
          'A chartered accountant maintains books of account, conducts statutory audit and internal audit, handles taxation matters including planning and representation, provides management accounting and consultancy, gives financial advice on investments, insurance, expansion and investigations, and does other work like company formation, liquidation and arbitration.',
          [P('p1', 'Maintenance of books of account', 2, 'books|book keep|maintain|maintenance|bookkeep|accounting record', min=1),
           P('p2', 'Statutory audit and internal audit', 3, 'audit'),
           P('p3', 'Taxation', 2, 'tax|taxation|taxes|income tax|gst'),
           P('p4', 'Management consultancy / financial advice / investigations, liquidation, arbitration etc.', 3, 'consult|management account', 'advice|advis|investment|insurance', 'investigat|fraud|valuation', 'liquidat|insolvency|receiver|arbitrat|secretarial|company formation|share registration', min=2)], 'c8'),
    ]

    c = Checks()
    cases = [{
        'id': 'k1', 'title': 'Green Leaf Organics — one set of accounts, many readers', 'difficulty': 'moderate',
        'case': ('Green Leaf Organics Pvt Ltd sells packaged organic food. Its accountant enters every invoice and payment daily and posts them to ledger accounts. At the year end, the finance head prepares the profit and loss account and balance sheet, calculates ratios, explains why margins fell and sends a report to the directors and to the company\'s bank. '
                 'A local NGO asks for the accounts to see how many farmers in the district supply the company. The directors also wonder whether to show the value of their highly trained team in the balance sheet.'),
        'mcqs': [
            dict(M('k1a', 'The daily entry of invoices and posting to ledger accounts is an example of:', ['Book-keeping', 'Interpreting', 'Communicating', 'Analysing'], 0,
              "Entering invoices and payments daily and posting them to ledger accounts are the recording and classifying stages; these steps, up to balancing the accounts, make up book-keeping. Interpreting, analysing and communicating come later, when statements are prepared and explained, so they belong to accounting. The trap is to treat every task done by the accounts team as 'accounting'. In practice: many Indian businesses outsource daily book-keeping in Tally to a junior, while a CA handles finalisation and reporting.", 'core'), topic='Book-keeping'),
            dict(M('k1b', 'Explaining why margins fell is which stage of the accounting procedure?', ['Interpreting', 'Recording', 'Classifying', 'Summarising'], 0,
              'Analysis breaks figures down and relates them, for example by calculating ratios; interpreting goes one step further and explains what those relationships mean and why they changed — such as why margins fell. The tempting option, summarising, only arranges the data into the profit and loss account and balance sheet; it does not give reasons. In practice: when a finance head tells the board that margins fell because raw material prices rose faster than selling prices, that is interpretation.', 'core'), topic='Introduction'),
            dict(M('k1c', 'The NGO interested in the company\'s purchases from local farmers is best described as:', ['The public — an external user', 'Management — an internal user', 'A lender — an external user', 'An investor — an external user'], 0,
              "The public at large is an external user interested in an enterprise's contribution to the local economy — employment, purchases from local suppliers and community impact — which is exactly what the NGO wants to know. The trap is to call any outsider a lender or investor; the NGO neither lends money nor holds shares. In practice: NGOs, journalists and local bodies in India often study companies' annual reports and CSR disclosures to judge their impact on farmers and communities.", 'moderate'), topic='Users of Accounting Information'),
            dict(M('k1d', 'Can the trained team be shown as an asset in the balance sheet under conventional accounting?', ['No — human resources cannot be measured reliably in money, which is a recognised limitation', 'Yes — at the salaries paid during the year', 'Yes — at a value fixed by the directors', 'No — because employees are external users'], 0,
              "Conventional accounting records only items that can be measured reliably in money, and there is no generally accepted method of valuing a trained workforce, so the team cannot appear as an asset — a recognised limitation of accounting. The tempting option values the team at salaries paid; salaries are an expense for services already received, not an asset. In practice: an Indian IT company's most valuable resource, its engineers, appears nowhere in its balance sheet; only salary costs appear in the profit and loss account.", 'hard'), topic='Relationship of Accounting with Other Disciplines'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch01', 'n': 1,
        'title': 'Meaning and Scope of Accounting',
        'outcomes': [
            'Explain what accounting is, how its definition widened from record-keeping to communication of information for decisions, and why it is called the language of business.',
            'Describe the six stages of the accounting procedure and the objectives and functions of accounting.',
            'Trace the evolution of accounting from ancient times through Pacioli to social responsibility accounting, and justify treating it as a social science.',
            'Distinguish book-keeping from accounting and name the sub-fields of accounting.',
            'Identify the internal and external users of accounting information and what each needs.',
            'Explain the links between accounting and economics, statistics, mathematics, law and management, the limitations of accounting, and the services an accountant renders to society.',
        ],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 35}, 'prereq': [],
                 'exam_tip': 'Theory questions from this unit (book-keeping vs accounting, users, limitations, relationship with other disciplines) are regular 4–5 mark items. Answer in points or tables with one example each.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Accounting: recording, classifying, summarising, analysing, interpreting and communicating financial information for users\' decisions — the language of business.',
                        'Definitions: AICPA 1961 (art of recording … interpreting), AAA 1966 (identifying, measuring, communicating), APB 1970 (quantitative information useful for economic decisions).',
                        'Objectives: record, find result (P&L), find position (balance sheet), inform users, know liquidity/solvency. Functions: measurement, forecasting, decision-making, comparison & evaluation, control, government regulation & taxation.',
                        'Evolution: stewardship → financial → management (20th century) → social responsibility accounting. Pacioli, Venice, 1494. Social science because it serves society.',
                        'Book-keeping = recording phase; accounting begins where it ends. Sub-fields: financial, management, cost, social responsibility, human resource accounting.',
                        'Users: internal (management, employees) and external (investors, lenders, suppliers, customers, government, public).'],
            'remember': ['Trial balance is still book-keeping; financial statements are accounting.', 'No specific law prescribes books for sole proprietors and partnership firms; companies, banks and insurers have their Acts.', 'Seven limitations: non-monetary items, past date, inflation, conflicting principles, judgement, human resources, alternative policies.'],
            'traps': ['Do not call profit for the year a transaction — it is an event.', 'Do not confuse internal audit (management tool) with statutory audit (required by law).', 'Do not say standards eliminate all alternative treatments — they only reduce them.'],
        },
        'quickref': [
            {'k': 'Language of business', 'v': 'Accounting — it communicates the results of business to users'},
            {'k': 'Six stages', 'v': 'Recording → Classifying → Summarising → Analysing → Interpreting → Communicating'},
            {'k': 'AICPA 1961', 'v': 'Art of recording, classifying, summarising in money terms … and interpreting'},
            {'k': 'AAA 1966', 'v': 'Identifying, measuring and communicating economic information for informed decisions'},
            {'k': 'Pacioli', 'v': 'Summa de Arithmetica, Venice, 1494 — first printed book on double entry'},
            {'k': 'Phases', 'v': 'Stewardship → Financial → Management → Social responsibility accounting'},
            {'k': 'Accountancy ⊃ Accounting ⊃ Book-keeping', 'v': 'Accounting starts where book-keeping ends'},
            {'k': 'Users', 'v': 'Internal: management, employees · External: investors, lenders, suppliers, customers, government, public'},
        ],
        'viva': viva, 'cases': cases,
    }


# ---------- Auto-check data for the Write tab ----------
# Per scheme point: kw (viva-matcher keyword groups, "|" = alternatives) + min (groups needed), nums (figures that must
# appear), rows ([particular keywords, side, amount] for table answers), wrong (common wrong statements → remark),
# ai_only (not checkable offline). Per question: extra_ok (may points beyond the model earn credit).
AUTO = {
    'q1': {'extra_ok': True,
           's1': {'kw': ['record|journal|ledger', 'summar|analys|interpret|communicat'], 'min': 2,
                  'wrong': [{'kw': ['book keeping summar|bookkeeping summar|book keeping analys|bookkeeping analys|book keeping interpret|accounting record phase|accounting record stage|accounting only record'],
                             'say': 'Roles reversed: book-keeping is the recording phase; accounting summarises, analyses, interprets and communicates.'}]},
           's2': {'kw': ['foundation|base book keeping|book keeping base|bookkeeping base|basis accounting|begin where|begins where|start where|starts where|language business|rests book keeping|rests bookkeeping|end where|ends where'], 'min': 1},
           's3': {'kw': ['financial statement|final account|balance sheet|financial position|profit loss|position business'], 'min': 1,
                  'wrong': [{'kw': ['book keeping prepare financial|bookkeeping prepare financial|book keeping shows financial position|bookkeeping shows financial position'],
                             'say': 'Financial statements and the financial position come from accounting, not from book-keeping records alone.'}]},
           's4': {'kw': ['decision'], 'min': 1},
           's5': {'kw': ['management accounting|cost accounting|financial accounting|sub field|subfield|branch|human resource accounting|social responsibility|tax accounting'], 'min': 1}},
    'q2': {'extra_ok': True,
           's1': {'kw': ['non monetary|nonmonetary|not measurable money|cannot measured money|cannot expressed money|not expressed money|not recorded money|money measurement|qualitative|human resource|skill|loyalty|morale|reputation|efficiency staff'], 'min': 1},
           's2': {'kw': ['historical|historic|past date|particular date|one date|single date|dated|past events|future'], 'min': 1},
           's3': {'kw': ['inflation|price level|value money|purchasing power|price change|changing prices|change prices|prices change|money value'], 'min': 1},
           's4': {'kw': ['judgement|judgment|subjectiv|personal bias|personal opinion|alternative polic|alternative method|alternative treatment|manipulat|conflict|window dressing|estimate|different methods'], 'min': 1}},
    'q3': {'extra_ok': True,
           's1': {'kw': ['economic', 'scarce|value|income|capital|acquisition cost|historical cost|micro|macro|resources|utility'], 'min': 2},
           's2': {'kw': ['statistic', 'approximat|average|trend|ratio|precision|precise|exact|time series|regression|sampling|correlation|forecast|predict'], 'min': 2},
           's3': {'kw': ['mathemat|arithmetic|algebra', 'algebra|interest|annuit|depreciation|instalment|installment|matrix|equation|formula|calculation|geometry|graph'], 'min': 2},
           's4': {'kw': ['law|act|legal|statute', 'contract|companies act|company law|negotiable|sale goods|format|prescrib|banking|insurance|electricity|income tax|gst|partnership act|legislation'], 'min': 2},
           's5': {'kw': ['management|manager', 'decision|planning|control|team|information'], 'min': 2}},
}


def _attach_auto(u):
    """Merge AUTO into the questions: every scheme point gets its auto-check fields; every question gets extra_ok."""
    for q in u.get('questions', []):
        a = AUTO[q['id']]
        q['extra_ok'] = a.get('extra_ok', False)
        for s in q['scheme']: s.update(a[s['id']])
        extra = set(a) - {'extra_ok'} - {s['id'] for s in q['scheme']}
        assert not extra, f"AUTO[{q['id']}] has unknown scheme ids {extra}"
    return u


_build_core = build


def build(): return _attach_auto(_build_core())
