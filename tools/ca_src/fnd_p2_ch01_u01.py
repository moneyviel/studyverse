"""CA Foundation · Paper 2 Business Laws · Chapter 1 Indian Regulatory Framework (single implicit unit).
Original explanations and questions; Articles of the Constitution and statutes are cited by number only."""
from lib import *
from ca_viva import P, ALT, V
from ca_cases import M

UID = 'fnd-p2-ch01-u01'


def Q(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check: d['check'] = check
    return d


def S(sid, pt, m, skill): return {'id': sid, 'pt': pt, 'm': m, 'skill': skill}


def build():
    steps = table(['Stage', 'What happens', 'Status of the proposal'], [
        ['1', 'A draft law is introduced in a House of Parliament', 'Bill'],
        ['2', 'Debated and passed by the Lok Sabha', 'Bill'],
        ['3', 'Debated and passed by the Rajya Sabha', 'Bill'],
        ['4', 'Assent of the President of India', 'Assented Bill'],
        ['5', 'Notified in the Official Gazette of India with an effective date', 'Act of Parliament (operative from the notified date)'],
    ], title='From Bill to Act')
    courts = table(['Level', 'Court', 'Key points to remember'], [
        ['1 (top)', 'Supreme Court of India', 'Set up on 26 January 1950; headed by the Chief Justice of India (Article 126 as per ICAI material); principal bench of seven, now 34 judges including the CJI; writs for fundamental rights under Article 32; its law binds all courts (Article 141)'],
        ['2', 'High Courts', 'Article 214 — a High Court for each State (some States share one); 25 High Courts; writs under Article 226; decisions bind courts in that State and are only persuasive elsewhere; oldest — Calcutta (1862)'],
        ['3', 'District / Subordinate Courts', 'District Judge for civil matters (contracts, damages claims); Sessions Court for criminal matters; jurisdiction fixed by territory and value of the suit'],
    ], title='Hierarchy of courts')
    ministries = table(['Body', 'Main laws / areas it handles'], [
        ['Ministry of Finance', 'Taxation, Union Budget, financial institutions, capital markets; income-tax administered through the CBDT under the Department of Revenue'],
        ['Ministry of Corporate Affairs (MCA)', 'Companies Act, 2013 (and the 1956 Act), LLP Act, 2008, Insolvency and Bankruptcy Code, 2016'],
        ['Ministry of Home Affairs', 'Internal security and domestic policy'],
        ['Ministry of Law and Justice', 'Legal advice to ministries, drafting of Central legislation, administration of justice'],
        ['SEBI', 'Securities and commodity derivatives markets — statutory body under the SEBI Act, 1992'],
        ['RBI', 'Central bank — banking regulation, issue of currency, payment systems'],
        ['IBBI', 'Insolvency professionals, their agencies and information utilities under the IBC, 2016'],
    ], title='Who enforces what')

    concepts = [
        {'id': 'c1', 'title': 'Why a CA studies law, and what law is', 'body': [
            'Clients and employers usually go to their CA first when a legal question touches money — a contract, a notice from a regulator, a dispute with a customer. A CA is not expected to argue cases, but must recognise the legal issue, give basic (threshold-level) advice and know when to call a lawyer.',
            'Law can be understood as the set of duties and obligations that the State lays down and enforces so that society is orderly, welfare is protected and justice is done. A regulatory framework gives everyone the same rules for dealing with each other, in personal life and in business.',
            'Written law is very old. The Code of Hammurabi of ancient Babylon (18th century BC), carved on stone and displayed in public, is the best-known early written code; Rome\'s Twelve Tables (about 450 BC) set out citizens\' rights and remedies on bronze tablets.'],
         'analogy': 'Law is the rule book of a game that everyone in the country plays together; regulators are the referees and courts are the appeal panel.',
         'work': 'A CA reviewing a client\'s books regularly meets contract terms, tax provisions and company-law requirements — spotting the legal angle early saves the client penalties and disputes.'},
        {'id': 'c2', 'title': 'Sources of law in India', 'body': [
            'The main sources are: (1) the Constitution of India — the supreme law and the source of every other law; (2) statutes made by Parliament and by the State Legislatures; (3) judicial precedents — decisions of the courts; and (4) in some matters, long-established customs and usages.',
            'India is a parliamentary democracy. Citizens elect representatives to Parliament and to State Legislative Assemblies, and those representatives make laws. A Central law may extend to the whole or any part of India; a State law operates only within that State.',
            'Background: the Government of India Act, 1935, passed by the British Parliament, moved India from a unitary to a federal design and divided powers between the Centre and the provinces. It created the Federal Court (1937), which was later replaced by the Supreme Court.',
            'The Constitution was adopted on 26 November 1949 and came into force on 26 January 1950. It guarantees Fundamental Rights, lists Fundamental Duties and sets out the powers of the Central and State Governments.'],
         'analogy': 'The Constitution is the trunk of a tree; statutes are its branches, court decisions are the new shoots that shape the branches, and customs are the old roots that still feed some parts.',
         'work': 'When a client asks "which rule applies?", the CA checks the statute first, then the latest binding court decisions that interpret it.'},
        {'id': 'c3', 'title': 'Division of law-making power: three lists', 'body': [
            'The Constitution divides subjects between the Centre and the States in three lists — the Union (Central) List, the State List and the Concurrent (Joint) List.',
            'A subject in the Union List is legislated by Parliament alone — income-tax is an example, so there is one income-tax law for the whole country, administered by the Ministry of Finance. A subject in the State List is legislated by the State. On a Concurrent List subject both can legislate.',
            'Stamp duty is a well-known example of a subject on which both the Centre and the States have laws, which is why stamp duty on the same type of document can differ between States.',
            'Because power is shared between the Centre and the States, India follows a federal system.'],
         'analogy': 'Three cupboards: one key with the Centre, one with each State, and a shared cupboard to which both have keys.',
         'work': 'Before advising on stamp duty for a property deal or a loan document, a CA checks the stamp law of the State where the document is executed.'},
        {'id': 'c4', 'title': 'How a law is made', 'body': [
            'A proposed law placed before Parliament is called a Bill. It is discussed and passed by the Lok Sabha and the Rajya Sabha, and then needs the assent of the President of India.',
            'The Government then publishes it in the Official Gazette of India. It becomes operative from the date mentioned in the notification. Once notified and in force it is called an Act of Parliament.',
            'Note: a Bill has no force of law. Even an Act binds people only from its notified effective date — this is why professionals always check the "date of enforcement" of a new provision.'],
         'blocks': [steps],
         'analogy': 'A Bill is a recipe still being tested in the kitchen; the President\'s assent is the head chef\'s approval; Gazette notification is putting the dish on the menu with a start date.',
         'work': 'Finance Acts often notify different sections from different dates; a CA applies a new tax rule only from the date it is actually in force.'},
        {'id': 'c5', 'title': 'Types of law: criminal and civil', 'body': [
            'Criminal law deals with public wrongs — acts that harm society as a whole — and with their punishment. The Bharatiya Nyaya Sanhita, 2023 (BNS) defines offences and their punishments; the Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) lays down the procedure for investigation, trial and punishment. Examples: murder, theft, cheating, fraud, assault.',
            'Civil law deals with disputes between individuals or organisations about their rights and obligations. Its aim is to settle the dispute and give a remedy (such as compensation, recovery or an injunction), not to punish. Proceedings start with a civil suit and are governed by the Code of Civil Procedure, 1908. Branches include the law of contract, family law, property law and the law of torts. Examples: a supplier failing to deliver goods, a borrower not repaying, a breach of contract, disputes between landlord and tenant, claims for defamation.'],
         'analogy': 'Criminal law asks "what punishment does society impose?"; civil law asks "what does one party owe the other?"',
         'work': 'A client\'s unpaid invoice is a civil recovery matter; a cheque-signing employee who siphons funds may also face criminal proceedings — the CA\'s evidence (books, audit trail) may be needed in both.'},
        {'id': 'c6', 'title': 'Common law, precedent and stare decisis', 'body': [
            'Common law here means judge-made law — principles laid down in judicial precedents (case law).',
            'Article 141 of the Constitution: the law declared by the Supreme Court binds all courts within India.',
            'The doctrine of stare decisis (Latin: "to stand by what has been decided") requires courts to follow earlier decisions when a new case has substantially the same facts. This keeps the law predictable.',
            'A later judgment can refine or change judge-made principles, but a court cannot amend a statute — it can only interpret it (or strike it down if it violates the Constitution). Changing a statute is the legislature\'s job.'],
         'analogy': 'Precedent is the answer key the courts keep: similar question, similar answer.',
         'work': 'Tax and company-law advice relies heavily on decided cases; a CA must know whether a decision is from the Supreme Court (binding everywhere) or from a High Court (binding only in that State).'},
        {'id': 'c7', 'title': 'Principles of natural justice', 'body': [
            'Natural justice is a set of basic fairness rules that apply even where no statute spells them out. Every authority deciding a person\'s rights — a court, a tribunal or a tax officer — must follow them.',
            'Nemo judex in causa sua — no one should be a judge in his own cause (the rule against bias).',
            'Audi alteram partem — hear the other side: a person must get notice and a fair opportunity to present his case before an adverse decision.',
            'Reasoned decision — the authority must record the reasons for its decision (a "speaking order"), so that it can be tested on appeal.'],
         'analogy': 'A referee who owns one of the teams, who gives a red card without letting the player speak, or who refuses to say why, has broken all three rules.',
         'work': 'When a tax or regulatory order is passed without giving the client a hearing, the CA can challenge it as a violation of natural justice — one of the most common grounds of appeal.'},
        {'id': 'c8', 'title': 'Enforcing the law: the executive and key ministries', 'body': [
            'Passing a law is not enough — someone must monitor compliance and act against violations. This is the job of the executive. The Central Government enforces Central laws and State Governments enforce State laws, through ministries headed by ministers and staffed by civil servants.',
            'Ministry of Finance: the Treasury of India — taxation, financial laws and institutions, capital markets, the finances of the Centre and the States, and the Union Budget. Its departments are Economic Affairs, Expenditure, Revenue, Financial Services, Investment and Public Asset Management (DIPAM), and Public Enterprises. Income-tax is administered by the Central Board of Direct Taxes (CBDT) under the Department of Revenue, through officers of the Indian Revenue Service.',
            'Ministry of Corporate Affairs (MCA): administers the Companies Act, 2013 (and the earlier 1956 Act), the LLP Act, 2008 and the Insolvency and Bankruptcy Code, 2016; mainly regulates corporate enterprises in industry and services. It is staffed largely by the Indian Corporate Law Service (ICLS), recruited through the UPSC Civil Services Examination; the top post is the Director General of Corporate Affairs.',
            'Ministry of Home Affairs: the interior ministry — internal security and domestic policy; departments include Border Management, Internal Security, States, Official Language, Home, and Jammu, Kashmir and Ladakh Affairs.',
            'Ministry of Law and Justice: Department of Legal Affairs (advises other ministries), Legislative Department (drafts principal Central legislation) and Department of Justice (administration of justice).'],
         'blocks': [ministries],
         'analogy': 'Parliament writes the traffic rules; the ministries are the traffic police posted at different junctions.',
         'work': 'A CA files income-tax returns on the CBDT\'s portal and company forms on the MCA portal — knowing which ministry owns which law tells you where to file, whom to write to and whose circulars to follow.'},
        {'id': 'c9', 'title': 'Major regulators: SEBI, RBI and IBBI', 'body': [
            'SEBI (Securities and Exchange Board of India) regulates the securities and commodity derivatives markets. It was set up on 12 April 1988 as a non-statutory body and received statutory powers on 30 January 1992 under the SEBI Act, 1992. It works within the administrative purview of the Ministry of Finance.',
            'The Reserve Bank of India (RBI) is the country\'s central bank and the regulator of the banking system; the study material places it under the ownership of the Ministry of Finance. It controls the issue and supply of the rupee, runs and oversees the principal payment systems and supports the growth of the economy.',
            'Learn these points as the ICAI material states them (they are asked in this form): RBI prints currency notes through a specialised division, Bharatiya Reserve Bank Note Mudran (BRBNM), at two presses — Nashik (western India) and Dewas (central India); RBI set up the National Payments Corporation of India (NPCI) as a specialised division for regulating payment and settlement systems; and RBI set up the Deposit Insurance and Credit Guarantee Corporation (DICGC) to insure deposits and guarantee credit facilities of banks.',
            'Real-world note (for understanding, not for changing your exam answer): BRBNM is a wholly owned subsidiary company of RBI whose presses are at Mysuru and Salboni; the Nashik and Dewas presses belong to the Government-owned Security Printing and Minting Corporation of India (SPMCIL), and coins are minted by the Government, not by RBI. NPCI is a not-for-profit company promoted by RBI and the Indian Banks\' Association that operates retail payment systems such as UPI — RBI itself remains the regulator of payment systems. DICGC is a wholly owned subsidiary of RBI working under the DICGC Act, 1961.',
            'IBBI (Insolvency and Bankruptcy Board of India) was established on 1 October 2016 under the Insolvency and Bankruptcy Code, 2016. It regulates insolvency professionals, insolvency professional agencies and information utilities. The Code covers companies, LLPs, partnership firms and individuals; cases are decided by the National Company Law Tribunal (companies and LLPs) and the Debt Recovery Tribunal (individuals and partnership firms). The Code aims at faster, simpler resolution of stressed assets.'],
         'analogy': 'SEBI guards the stock market, RBI guards the money and the banks, IBBI guards the process when a debtor cannot pay.',
         'work': 'Audits of listed companies (SEBI listing rules), banks and NBFCs (RBI directions) and insolvency assignments (IBBI regulations — many insolvency professionals are CAs) all depend on these regulators\' rules.'},
        {'id': 'c10', 'title': 'Structure of the Indian judicial system', 'body': [
            'The judiciary resolves disputes between citizens and between citizens and the Government. Its functions: interpreting Acts and Codes, resolving disputes and promoting fairness.',
            'Supreme Court: the apex court, established on 26 January 1950. Its highest authority is the Chief Justice of India — the ICAI material describes the CJI as appointed under Article 126. The material gives the principal bench as seven members including the CJI; the strength has since grown to 34 including the CJI because of the rising workload. A person can approach it directly for enforcement of fundamental rights by a writ petition under Article 32. Its decisions bind all courts (Article 141) and are the final word.',
            'Article note: in the exam, reproduce the material\'s reference (CJI — Article 126). In the text of the Constitution, Article 124 establishes the Supreme Court and provides for appointment of the CJI and the other judges (originally the CJI and up to seven other judges), while Article 126 provides for appointment of an acting Chief Justice; you may add the Article 124 point to show depth.',
            'High Courts: the highest court in each State; Article 214 provides for a High Court for every State, though some States share a common High Court. There are 25 High Courts. They have original, appellate and supervisory jurisdiction and can issue writs under Article 226. Supervision of subordinate courts is linked to Article 227 (the material mentions it as limiting that supervisory power). A High Court decision binds courts in that State and is only persuasive in other States. The Calcutta High Court (1862) is the oldest.',
            'District Courts: below the High Courts. The District Judge hears civil matters such as contract disputes and damages claims; the Sessions Court hears criminal matters. The study material states that, under pecuniary jurisdiction, a civil judge can try suits valued at not more than ₹2 crore (in practice the money limits are fixed State by State and differ).',
            'Jurisdiction means the authority of a court to hear a case. Territorial jurisdiction depends on the local limits where the parties reside or where the disputed property is situated; pecuniary jurisdiction depends on the money value of the suit.',
            'Metropolitan courts: the study material describes courts of the Chief Metropolitan Magistrate and Metropolitan Magistrates for cities with a population of ten lakh or more, set up in consultation with the High Court.'],
         'blocks': [courts],
         'analogy': 'A three-storey building: the ground floor (district courts) handles most cases; the first floor (High Courts) hears appeals for the State; the top floor (Supreme Court) has the final word for the whole country.',
         'work': 'Appeals in tax matters can travel up to the High Court and the Supreme Court; a CA tracking a client\'s case must know which court\'s ruling is binding in the client\'s State.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Which court, which law?', 'difficulty': 'core', 'minutes': 6,
         'q': 'Classify each matter as civil or criminal and name the main procedural law: (a) Nimbus Traders sues a buyer for ₹3,40,000 unpaid for goods supplied; (b) an employee of Nimbus forges signatures to withdraw money from the firm\'s bank account; (c) a tenant refuses to vacate a shop after the lease ends.',
         'solution': [table(['Matter', 'Nature', 'Why', 'Procedure'], [
             ['(a) Unpaid price', 'Civil', 'Private dispute; the remedy sought is recovery of money', 'Code of Civil Procedure, 1908'],
             ['(b) Forgery and withdrawal', 'Criminal', 'Public wrong (forgery, cheating); the State prosecutes and punishes', 'BNS defines the offence; BNSS governs the procedure'],
             ['(c) Tenant not vacating', 'Civil', 'Dispute over property rights between landlord and tenant', 'Code of Civil Procedure, 1908'],
         ]), note('The same facts can give rise to both: in (b) the firm can also file a civil suit to recover the money.')]},
        {'id': 'i2', 'title': 'Is the new rule in force?', 'difficulty': 'core', 'minutes': 5,
         'q': 'A Bill amending a Central law was passed by the Lok Sabha in February, by the Rajya Sabha in March, received the President\'s assent on 28 March and was notified in the Official Gazette with an effective date of 1 July. A client wants to know whether the new rule applies to a transaction made on 15 May.',
         'solution': [legal('A Bill becomes an Act after passage by both Houses and the President\'s assent; it operates from the effective date stated in its Gazette notification.',
                            'Both Houses passed it, assent was given on 28 March, and the notified effective date is 1 July. The transaction took place on 15 May.',
                            'On 15 May the amendment, though an Act, had not yet come into force, because its notified effective date is 1 July.',
                            'The old rule applies to the 15 May transaction; the new rule applies to transactions on or after 1 July.')]},
        {'id': 'i3', 'title': 'An order passed without a hearing', 'difficulty': 'moderate', 'minutes': 6,
         'q': 'A licensing officer cancels Jyoti Enterprises\' trade licence on a complaint by a competitor, without giving Jyoti any notice. It later emerges that the officer\'s brother is a partner in the competing firm, and the order gives no reasons. Which principles of natural justice are violated?',
         'solution': [legal('Natural justice requires: (i) no one shall be a judge in his own cause (nemo judex in causa sua); (ii) the affected party must be heard (audi alteram partem); (iii) the decision must be reasoned.',
                            'The officer had a family interest in the competitor, gave Jyoti no notice or hearing, and recorded no reasons.',
                            'The officer\'s interest shows bias; denial of notice breaches the hearing rule; absence of reasons breaches the requirement of a reasoned decision.',
                            'All three principles are violated; the order is liable to be set aside, for example in a writ petition before the High Court under Article 226.')]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Reading a court ruling for a client', 'role': 'Articled assistant in a tax practice', 'situation': 'Your principal hands you two decisions on the same tax point: one from the Bombay High Court in the client\'s favour and one from the Supreme Court against it. The client is in Pune.',
         'steps': ['Note the hierarchy: the Supreme Court is at the top; its law binds every court (Article 141).', 'A High Court decision binds courts in its own State but is overridden by a Supreme Court decision on the same point.', 'Check whether the facts are really the same — stare decisis applies where facts are substantially similar.', 'Report: unless the facts differ, the Supreme Court view governs.'],
         'takeaway': 'Always check the court level and the facts before relying on a precedent.', 'think': 'If only the Bombay High Court decision existed, would it bind an officer in Pune? In Chennai?',
         'answer': 'Pune is within the Bombay High Court\'s jurisdiction, so it would bind there; in Chennai (Madras High Court) it would only be persuasive.'},
        {'id': 'j2', 'title': 'Mapping a new client\'s regulators', 'role': 'CA in practice onboarding a listed NBFC client', 'situation': 'A listed non-banking finance company appoints your firm. You prepare a compliance map.',
         'steps': ['MCA — Companies Act filings, board and auditor matters.', 'SEBI — listing obligations and disclosure requirements, because its shares are listed.', 'RBI — NBFC registration and prudential directions.', 'Ministry of Finance / CBDT — income-tax; plus State laws such as stamp duty on loan documents.'],
         'takeaway': 'One business can answer to several regulators; a compliance calendar starts with knowing who they are.'},
    ]

    mcqs = [
        Q('m1', 'A Chartered Accountant needs knowledge of law mainly because:', ['He is often the first point of contact and must advise clients at a basic level', 'He must argue cases in the Supreme Court', 'He must draft every Bill for Parliament', 'He replaces the need for a lawyer'], 0, 'A CA gives threshold-level legal advice and recognises when an expert is needed.', 'c1'),
        Q('m2', 'Which of these is NOT a main source of law in India?', ['Textbooks written by legal authors', 'The Constitution of India', 'Statutes passed by State Legislatures', 'Judicial precedents'], 0, 'Textbooks may explain law but do not make it. The Constitution, statutes, precedents and customs are the sources.', 'c2'),
        Q('m3', 'The Constitution of India was adopted in:', ['1949', '1950', '1947', '1935'], 0, 'Adopted on 26 November 1949; it came into force on 26 January 1950.', 'c2', check='1949'),
        Q('m4', 'India\'s federal system means that:', ['Law-making powers are divided between the Centre and the States', 'All power rests with the President', 'States have unlimited powers', 'Only the Centre can make laws'], 0, 'The Union, State and Concurrent Lists divide subjects between the two levels.', 'c3'),
        Q('m5', 'Income-tax (other than on agricultural income) is a subject of the:', ['Union List', 'State List', 'Concurrent List', 'None of the lists'], 0, 'That is why one income-tax law applies throughout India, administered by the Ministry of Finance.', 'c3', 'moderate'),
        Q('m6', 'A proposed law while it is being considered by Parliament is called:', ['A Bill', 'An Act', 'A notification', 'An ordinance'], 0, 'It becomes an Act only after both Houses pass it, the President assents and it is notified.', 'c4'),
        Q('m7', 'A new Act of Parliament becomes operative from:', ['The effective date stated in its Gazette notification', 'The date the Lok Sabha passes it', 'The date it is introduced as a Bill', 'The first day of the next financial year, always'], 0, 'Applicability follows the notified effective date.', 'c4', 'moderate'),
        Q('m8', 'Which of the following is NOT a civil matter?', ['Theft of goods from a warehouse', 'Breach of a supply contract', 'Non-payment of a loan instalment', 'A landlord–tenant dispute'], 0, 'Theft is a public wrong punished under criminal law (BNS).', 'c5'),
        Q('m9', 'The procedure in civil cases is mainly governed by:', ['Code of Civil Procedure, 1908', 'Bharatiya Nyaya Sanhita, 2023', 'Bharatiya Nagarik Suraksha Sanhita, 2023', 'Companies Act, 2013'], 0, 'BNS defines offences, BNSS is criminal procedure; the CPC governs civil suits.', 'c5'),
        Q('m10', '"Stare decisis" means:', ['Stand by what has been decided', 'Hear the other side', 'No one should judge his own cause', 'Let the buyer beware'], 0, 'It is the principle behind following precedents.', 'c6'),
        Q('m11', 'Under Article 141 of the Constitution, the law declared by the Supreme Court is:', ['Binding on all courts within India', 'Binding only on the High Court from which the appeal came', 'Merely persuasive', 'Binding only on civil courts'], 0, 'Article 141 makes Supreme Court law binding throughout India.', 'c6'),
        Q('m12', '"Audi alteram partem" requires that:', ['The affected party be given a fair hearing', 'The judge have no interest in the case', 'The decision be published in the Gazette', 'The case be decided within a year'], 0, 'It is the hearing rule; the rule against bias is nemo judex in causa sua.', 'c7'),
        Q('m13', 'Which of these is NOT a department of the Ministry of Finance?', ['Department of States', 'Department of Revenue', 'Department of Expenditure', 'Department of Financial Services'], 0, 'The Department of States is under the Ministry of Home Affairs.', 'c8', 'moderate'),
        Q('m14', 'The Insolvency and Bankruptcy Code, 2016 and the LLP Act, 2008 are administered by the:', ['Ministry of Corporate Affairs', 'Ministry of Home Affairs', 'Reserve Bank of India', 'Ministry of Law and Justice'], 0, 'MCA administers the Companies Acts, the LLP Act and the IBC.', 'c8'),
        Q('m15', 'SEBI received statutory powers through the SEBI Act in the year:', ['1992', '1988', '2016', '1950'], 0, 'Set up in 1988 as a non-statutory body; statutory status from 30 January 1992.', 'c9', 'moderate', check='1992'),
        Q('m16', 'Which body regulates insolvency professionals and information utilities?', ['IBBI', 'SEBI', 'RBI', 'NCLT'], 0, 'IBBI is the regulator; NCLT is an adjudicating authority (a tribunal), not the regulator.', 'c9'),
        Q('m17', 'A person whose fundamental right is violated can move the Supreme Court directly under:', ['Article 32', 'Article 226', 'Article 141', 'Article 214'], 0, 'Article 32 — writ jurisdiction of the Supreme Court; Article 226 is the High Courts\' writ power.', 'c10', 'moderate'),
        Q('m18', 'A decision of the Madras High Court, for a court in Gujarat, is:', ['Only persuasive', 'Binding', 'Binding only in criminal cases', 'Of no value at all'], 0, 'High Court decisions bind within their own State only.', 'c10'),
        Q('m19', 'Territorial jurisdiction of a civil court generally depends on:', ['Where the parties reside or where the disputed property is situated', 'The age of the parties', 'The religion of the parties', 'The date the contract was signed'], 0, 'Courts get jurisdiction by local limits — residence of the parties or location of the property.', 'c10'),
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'text',
         'q': 'What is meant by law? Describe the process by which a Bill becomes an Act of Parliament.',
         'model': [p('Meaning: law is the body of obligations and duties laid down and enforced by the State to maintain order, protect welfare and do justice in society. India\'s legal framework reflects its social, political, economic and cultural diversity.'),
                   ul(['A proposed law introduced in Parliament is called a Bill.', 'It is debated and passed by the Lok Sabha.', 'It is then debated and passed by the Rajya Sabha.', 'It receives the assent of the President of India.', 'The Government notifies it in the Official Gazette of India; it applies from the effective date stated in the notification.', 'Once notified and in force, it is known as an Act of Parliament.'])],
         'scheme': [S('s1', 'Meaning of law', 1, 'concept'), S('s2', 'Bill — meaning', 0.5, 'concept'), S('s3', 'Passage by both Houses', 1.5, 'provision'), S('s4', 'Assent of the President', 1, 'provision'), S('s5', 'Gazette notification and effective date → Act', 1, 'provision')],
         'remarks': ['Most candidates list the stages correctly but forget that the Act applies only from the notified effective date.'],
         'mistakes': ['Writing that the Act is effective from the date of the President\'s assent in every case.', 'Saying the Governor gives assent to Central Bills.'],
         'tips': ['Write the stages as numbered points — examiners award marks per stage.', 'End with the line "it is then called an Act of Parliament".']},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
         'q': 'Distinguish between criminal law and civil law.',
         'model': [table(['Basis', 'Criminal law', 'Civil law'], [
             ['Concern', 'Public wrongs — acts harmful to society', 'Private rights and obligations between persons or organisations'],
             ['Object', 'Punishment of the offender', 'Settlement of the dispute and a remedy (compensation, recovery, injunction)'],
             ['Governing law', 'Bharatiya Nyaya Sanhita, 2023 (offences) and Bharatiya Nagarik Suraksha Sanhita, 2023 (procedure)', 'Code of Civil Procedure, 1908 (procedure); substantive laws of contract, property, family, torts'],
             ['Examples', 'Murder, theft, cheating, assault', 'Breach of contract, non-payment of dues, landlord–tenant disputes'],
         ])],
         'scheme': [S('s1', 'Nature/concern', 1, 'concept'), S('s2', 'Object — punishment vs remedy', 1, 'concept'), S('s3', 'Governing laws named correctly', 1, 'provision'), S('s4', 'Examples', 1, 'application')],
         'remarks': ['A four-row table earns full marks quickly; naming BNS/BNSS (not IPC/CrPC) is expected from the 2023 laws onwards.'],
         'mistakes': ['Citing the repealed Indian Penal Code instead of the BNS.', 'Listing defamation only as a crime — as a claim for damages it is civil.'],
         'tips': ['Use "Basis" as the first column.', 'Keep each cell to one line.']},
        {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'Write short notes on: (a) the Supreme Court and the High Courts in the Indian judicial system; (b) the Ministry of Corporate Affairs.',
         'model': [p('(a) Supreme Court: the apex court, established on 26 January 1950. The Chief Justice of India is its highest authority, appointed under Article 126. Its principal bench consisted of seven members including the CJI; the number has now increased to 34 including the CJI because of the growing workload. A person may approach it by a writ petition under Article 32 for enforcement of fundamental rights. Under Article 141 its decisions bind all courts in India and are final.'),
                   p('High Courts: the highest court of each State (Article 214); some States share one, and there are 25 in all. They have original, appellate and supervisory jurisdiction and issue writs under Article 226. Their decisions bind subordinate courts in the State and are persuasive in other States. The Calcutta High Court (1862) is the oldest.'),
                   p('(b) Ministry of Corporate Affairs: a Ministry of the Government of India that administers the Companies Act, 2013, the Companies Act, 1956, the LLP Act, 2008 and the Insolvency and Bankruptcy Code, 2016, and regulates corporate enterprises in the industrial and services sectors. It is staffed mainly by officers of the Indian Corporate Law Service recruited through the UPSC Civil Services Examination; the highest post is the Director General of Corporate Affairs.')],
         'scheme': [S('s1', 'Supreme Court — apex, CJI (Article 126), strength 7 → 34', 1, 'concept'), S('s2', 'Article 32 and Article 141', 1, 'provision'), S('s3', 'High Courts — Article 214, jurisdiction', 1, 'concept'), S('s4', 'Article 226; binding within State, persuasive outside', 1, 'provision'), S('s5', 'MCA — laws administered', 1.5, 'provision'), S('s6', 'MCA — staffing (ICLS) / role', 0.5, 'concept')],
         'remarks': ['Marks go to the Article numbers and the binding-vs-persuasive point. Quote the CJI as appointed under Article 126, as in the ICAI material; adding that Article 124 governs the appointment of judges is accurate and shows depth.'],
         'mistakes': ['Mixing up Article 32 (Supreme Court) with Article 226 (High Courts).', 'Listing SEBI Act as administered by MCA.'],
         'tips': ['Use sub-headings (a) and (b); 5–6 lines each is enough.']},
    ]

    viva = [
        V('v1', 'What are the main sources of law in India?',
          'The main sources are the Constitution of India, statutes made by Parliament and the State Legislatures, judicial precedents or court decisions, and in some cases established customs and usages.',
          [P('p1', 'The Constitution', 3, 'constitution'),
           P('p2', 'Statutes / Acts of Parliament and State Legislatures', 3, 'statut|parliament|legislat|act pass|state assembl'),
           P('p3', 'Judicial precedents / court decisions', 2, 'precedent|judicial decision|court decision|decision court|case law|judgment|judgement|decided case'),
           P('p4', 'Customs and usages', 2, 'custom|usage')], 'c2'),
        V('v2', 'Explain the stages through which a Bill becomes an Act of Parliament.',
          'A proposed law is introduced as a Bill. It must be passed by both Houses, the Lok Sabha and the Rajya Sabha. Then the President of India gives assent. Finally it is notified in the Official Gazette and comes into force from the effective date in the notification, after which it is called an Act.',
          [P('p1', 'Passed by both Houses — Lok Sabha and Rajya Sabha', 3, 'lok sabha|both house|lower house|house of the people', 'rajya sabha|both house|upper house|council of state', min=2),
           P('p2', 'Assent of the President of India', 3, 'president'),
           P('p3', 'Notified in the Official Gazette', 2, 'gazette|notif|publish'),
           P('p4', 'Applies from the notified effective date', 2, 'effective date|date mention|date in notif|date notif|date stat|from date|date specif|come into force|comes into force|came into force|into effect|into force|enforce date|date of enforc|effect from')], 'c4'),
        V('v3', 'How does criminal law differ from civil law?',
          'Criminal law deals with public wrongs against society and their punishment, under the Bharatiya Nyaya Sanhita and the Bharatiya Nagarik Suraksha Sanhita. Civil law deals with private disputes between individuals or organisations and aims at a remedy such as compensation, under the Code of Civil Procedure.',
          [P('p1', 'Criminal law: public wrongs / offences against society, punished by the State', 4,
             'crimin public wrong|crimin law public|crimin wrong against societ|crimin offenc|crimin crime|crimin societ|crimin punish|crimin law punish|crimin law deal offenc|crimin law deal crime|crimin state prosecut|crimin law state|crimin law concern public|crimin law about public|crimin law about crime|crimin law about offenc|crimin wrong against state'),
           P('p2', 'Civil law: private disputes, aims at a remedy (compensation), not punishment', 4,
             'civil privat|civil law privat|civil disput|civil law disput|civil individu|civil law individu|civil compens|civil law compens|civil remed|civil law remed|civil right|civil law right|civil person|civil law between|civil between|civil law settl|civil settl|civil law concern privat|civil law about privat|civil law about disput|civil law resolv|civil resolv'),
           P('p3', 'Governing laws: BNS/BNSS for criminal, CPC for civil', 2, 'nyaya|bns|bnss|nagarik|code civil procedur|cpc|civil procedur', min=1)], 'c5'),
        V('v4', 'What are the principles of natural justice?',
          'First, nemo judex in causa sua: no one should be a judge in his own cause, which is the rule against bias. Second, audi alteram partem: hear the other side, so a person gets a fair hearing before a decision against him. Third, the decision must be a reasoned decision.',
          [P('p1', 'No one should be a judge in his own cause (nemo judex) — rule against bias', 4, 'nemo judex|judge in own cause|judge in his own|judge own cause|judge his own|judge in their own|judge their own|own case|own cause|against bias|no bias|against prejudic|not be biased|unbias|impartial'),
           P('p2', 'Hear the other side (audi alteram partem) — fair hearing', 4, 'audi alteram|alteram partem|hear other|hear the other|hear both|fair hear|right to be heard|opportun heard|opportun of hear|chance to be heard|give hear|heard before'),
           P('p3', 'Reasoned decision', 2, 'reason decision|reasoned|give reason|record reason|state reason|speaking order|reasons for decision|reason for decision|reason for the decision|reasons for the decision')], 'c7'),
        V('v5', 'What is the doctrine of stare decisis, and how binding are Supreme Court and High Court decisions?',
          'Stare decisis means to stand by what has been decided, so courts follow earlier decisions in cases with similar facts. Under Article 141, the law declared by the Supreme Court binds all courts in India. A High Court decision binds courts in its own State but is only persuasive in other States.',
          [P('p1', 'Stare decisis: stand by what has been decided — follow earlier decisions on similar facts', 3, 'stand by|follow earlier|follow previous|follow past|follow precedent|fact same|facts are similar|fact similar|follow decid|earlier decision|previous decision|past decision|similar fact|same fact|decided before|already decided'),
           P('p2', 'Supreme Court decisions bind all courts (Article 141)', 4, 'supreme court bind|supreme court decision bind|supreme court law bind|supreme court binding|141|supreme court decision binding|supreme court judgment bind|supreme court all court|bind all court|binding on all court|binding all court'),
           P('p3', 'High Court decision: binding in its State, only persuasive elsewhere', 3, 'persuasive|persuad')], 'c6'),
        V('v6', 'Name the regulator for each: the securities market, banks and currency, and insolvency professionals.',
          'SEBI regulates the securities market under the SEBI Act, 1992. The Reserve Bank of India regulates banks and issues the currency. The Insolvency and Bankruptcy Board of India, IBBI, regulates insolvency professionals under the Insolvency and Bankruptcy Code, 2016.',
          [P('p1', 'SEBI — securities market', 4, ALT('{s} secur', '{s} stock', '{s} capit market', '{s} share market', '{s} regul secur', '{s} regul stock', '{s} regul capit', '{s} regul share', '{s} market', s=('sebi', 'securities and exchange board')) + '|securities market under sebi|securities under sebi|stock market under sebi|capital market under sebi|stock market regul sebi|securit market regul sebi|capital market regul sebi|share market regul sebi|stock regul sebi|securit regul sebi'),
           P('p2', 'RBI — banks and currency', 3, ALT('{r} bank', '{r} regul bank', '{r} currenc', '{r} regul currenc', '{r} issu', '{r} money', '{r} central bank', 'bank regul {r}', 'bank system {r}', 'bank sector {r}', 'currenc issu {r}', 'issu currenc {r}', 'currenc regul {r}', r=('rbi', 'reserve bank'))),
           P('p3', 'IBBI — insolvency professionals', 3, 'ibbi|insolvency and bankruptcy board|insolvency board|bankruptcy board')], 'c9'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Arjun\'s first week at a CA firm', 'difficulty': 'moderate',
        'case': ('Arjun, a new articled assistant, receives four files. File 1: a client, Saffron Foods Ltd., has received a show-cause notice under a Central law and the officer passed the final order the next day without hearing the company. '
                 'File 2: Saffron\'s former accountant is accused of forging cheques. File 3: Saffron wants to recover ₹6,20,000 from a distributor for goods supplied. '
                 'File 4: a 2-year-old decision of the Supreme Court and a recent contrary decision of a High Court of another State on the same tax point.'),
        'mcqs': [
            M('k1a', 'In File 1, the strongest ground to challenge the order is:', ['Violation of audi alteram partem — no hearing was given', 'The doctrine of stare decisis', 'Article 141', 'Lack of territorial jurisdiction'], 0, 'An adverse order without a hearing breaches the hearing rule of natural justice.', 'moderate'),
            M('k1b', 'File 2 will be dealt with under:', ['Criminal law — BNS for the offence and BNSS for procedure', 'Only the Code of Civil Procedure', 'The Companies Act alone', 'The SEBI Act'], 0, 'Forgery is a public wrong; criminal law and its procedure apply (Saffron may separately sue to recover money).', 'core'),
            M('k1c', 'File 3 is:', ['A civil suit for recovery of money', 'A criminal prosecution', 'A writ petition under Article 32', 'An insolvency matter before IBBI'], 0, 'Non-payment for goods supplied is a civil dispute; IBBI is a regulator, not a forum for recovery suits.', 'core'),
            M('k1d', 'In File 4, which decision should Arjun treat as binding on Saffron\'s assessing officer?', ['The Supreme Court decision', 'The more recent High Court decision', 'Neither — both are persuasive only', 'Whichever favours the client'], 0, 'Article 141 — Supreme Court law binds all courts and authorities; another State\'s High Court is only persuasive.', 'hard'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch01', 'n': 1, 'title': 'Indian Regulatory Framework',
        'outcomes': ['Explain what law is, why a CA needs it, and the sources of law in India.', 'Describe how a Bill becomes an Act and how law-making power is divided between the Centre and the States.',
                     'Distinguish criminal law, civil law, common law (precedent) and the principles of natural justice.', 'Identify the ministries and regulators (Ministry of Finance, MCA, MHA, Ministry of Law and Justice, SEBI, RBI, IBBI) and the laws they enforce.',
                     'Outline the structure of the Indian judiciary — Supreme Court, High Courts and district courts — and the binding force of their decisions.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 30}, 'prereq': [],
                 'exam_tip': 'This chapter is asked as short notes and MCQ-style one-liners: learn the stages of a Bill, the civil/criminal distinction, the three natural-justice rules and the Article numbers (32, 126, 141, 214, 226).'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {'summary': ['Sources of law: Constitution, statutes (Parliament and State Legislatures), judicial precedents, customs.', 'Union, State and Concurrent Lists divide law-making power — a federal system. Income-tax: Union; stamp duty: both levels.',
                                 'Bill → passed by Lok Sabha and Rajya Sabha → President\'s assent → Gazette notification → Act, effective from the notified date.',
                                 'Criminal law: public wrongs, punishment (BNS, BNSS). Civil law: private disputes, remedies (CPC). Common law: precedent; Article 141; stare decisis.',
                                 'Natural justice: no bias (nemo judex in causa sua), fair hearing (audi alteram partem), reasoned decision.',
                                 'Ministries enforce laws: Finance (tax, budget), MCA (Companies Act, LLP Act, IBC), Home (internal security), Law and Justice. Regulators: SEBI, RBI, IBBI.',
                                 'Courts: Supreme Court → High Courts → District Courts; SC binding everywhere, HC binding in its State.'],
                     'remember': ['Constitution adopted 26 Nov 1949; in force 26 Jan 1950.', 'SEBI 1988 (statutory 1992); IBBI 1 Oct 2016.', 'Article 32 SC writs · 126 CJI (as per ICAI material; appointment of judges is in Article 124) · 141 SC law binding · 214 HC for each State · 226 HC writs.', 'RBI as per ICAI material: notes printed by BRBNM at Nashik and Dewas; NPCI and DICGC set up by RBI (see the real-world note in the RBI card).'],
                     'traps': ['A Bill is not law; an Act may still not be in force until its notified date.', 'NCLT/DRT decide insolvency cases; IBBI regulates — it does not adjudicate.', 'High Court decisions are only persuasive outside their State.']},
        'quickref': [{'k': 'Sources of law', 'v': 'Constitution · statutes · precedents · customs'}, {'k': 'Bill → Act', 'v': 'Lok Sabha + Rajya Sabha → President\'s assent → Official Gazette → effective date'},
                     {'k': 'Criminal law', 'v': 'BNS 2023 (offences) · BNSS 2023 (procedure)'}, {'k': 'Civil procedure', 'v': 'Code of Civil Procedure, 1908'},
                     {'k': 'Article 141', 'v': 'Supreme Court law binds all courts in India'}, {'k': 'Articles 32 / 226', 'v': 'Writs — Supreme Court / High Courts'},
                     {'k': 'Natural justice', 'v': 'Nemo judex in causa sua · audi alteram partem · reasoned decision'}, {'k': 'MCA administers', 'v': 'Companies Acts 2013/1956 · LLP Act 2008 · IBC 2016'},
                     {'k': 'SEBI / RBI / IBBI', 'v': 'Securities market / banks & currency / insolvency professionals'}],
        'viva': viva, 'cases': cases,
    }


# ---------- teaching explanations + topic tags for every MCQ (override the short drafts above) ----------
T1, T2, T3, T4, T5 = 'Why a CA studies law, and what law is', 'Sources of law in India', 'Division of law-making power: three lists', 'How a law is made', 'Types of law: criminal and civil'
T6, T7, T8, T9, T10 = 'Common law, precedent and stare decisis', 'Principles of natural justice', 'Enforcing the law: the executive and key ministries', 'Major regulators: SEBI, RBI and IBBI', 'Structure of the Indian judicial system'
EXPLAIN = {
    'm1': (T1, 'Clients usually bring money-related legal questions to their CA first, so a CA must spot the legal issue, give basic threshold-level advice and know when to bring in a lawyer. The tempting trap is "replaces the need for a lawyer" — a CA recognises and advises, but does not conduct litigation in court or take over a lawyer\'s role. In practice: a CA who reads a supplier contract can warn a client about a penalty clause before signing, then refer the dispute to an advocate if it escalates.'),
    'm2': (T2, 'Law is made, not merely described. The sources that actually create binding law in India are the Constitution, statutes of Parliament and State Legislatures, judicial precedents and, in some matters, customs. A textbook only explains the law, however respected its author. The trap is to treat "judicial precedents" as non-law because judges do not legislate — but decided cases do bind lower courts. In practice: a CA quotes a section of the Act or a court ruling in a reply to a tax notice, never a commentary alone.'),
    'm3': (T2, 'The Constituent Assembly adopted the Constitution on 26 November 1949 (now observed as Constitution Day), and it came into force on 26 January 1950. The tempting wrong answer is 1950, which confuses the date of commencement (Republic Day) with the date of adoption. 1947 is Independence and 1935 is the Government of India Act. In practice: professionals cite the Constitution as the supreme law from which every tax and corporate statute draws its validity.'),
    'm4': (T3, 'Federalism means law-making power is shared: the Constitution splits subjects into the Union List, the State List and the Concurrent List, so both the Centre and the States legislate in their own fields. The trap is "only the Centre can make laws" — that describes a unitary system; States make their own laws on State subjects. In practice: a business pays Central income-tax under one national Act but follows each State\'s own stamp law on property documents.'),
    'm5': (T3, 'Taxes on income other than agricultural income fall in the Union List, so only Parliament legislates on them — one Income-tax Act applies across India, administered by the CBDT under the Ministry of Finance. The tempting trap is the Concurrent List; income-tax is not shared. Agricultural income is the exception, being a State subject. In practice: a salaried employee in Kolkata and one in Pune file the same ITR forms on the same national e-filing portal.'),
    'm6': (T4, 'A draft law introduced in Parliament is a Bill. It turns into an Act only after both Houses pass it, the President gives assent and it is notified in the Official Gazette. The trap is "an Act" — a Bill under debate has no legal force. An ordinance is a temporary law issued by the President when Parliament is not in session, not a draft under discussion. In practice: CAs track Finance Bill proposals each February but advise clients only once the provisions are enacted and notified.'),
    'm7': (T4, 'An Act binds people only from the effective date stated in its Official Gazette notification; different sections may even be notified from different dates. The tempting trap is "the date the Lok Sabha passes it" — at that stage it is still a Bill, needing Rajya Sabha passage and the President\'s assent. Nor does every Act start on 1 April. In practice: before applying a new tax rule to a transaction, a CA checks the notified date of enforcement for that exact section.'),
    'm8': (T5, 'Theft harms society as a whole, so it is a public wrong prosecuted by the State and punished under criminal law — the Bharatiya Nyaya Sanhita, 2023 defines the offence. The other three are private disputes where the aim is a remedy such as recovery or eviction, so they are civil. The trap is a loan default, which feels like wrongdoing but is a civil recovery matter. In practice: a warehouse theft is reported to the police (FIR), while an unpaid invoice is chased by legal notice and civil suit.'),
    'm9': (T5, 'Civil suits — for recovery of money, breach of contract, property disputes — are governed procedurally by the Code of Civil Procedure, 1908. The tempting trap is the Bharatiya Nagarik Suraksha Sanhita, 2023, which is also a procedure code but for criminal cases; the Bharatiya Nyaya Sanhita defines offences and punishments. In practice: when a client sues a distributor for unpaid dues, the plaint, summons and decree all follow the CPC.'),
    'm10': (T6, 'Stare decisis is Latin for "to stand by what has been decided": courts follow earlier decisions when a new case has substantially the same facts, which keeps law predictable. The tempting trap is "hear the other side" — that is audi alteram partem, a rule of natural justice, not of precedent. In practice: a CA advising on a tax point first checks how courts have already decided similar facts, because the officer and tribunal are expected to follow them.'),
    'm11': (T6, 'Article 141 says the law declared by the Supreme Court binds all courts within the territory of India — civil, criminal, tribunals and High Courts alike. The trap is "binding only on the High Court from which the appeal came"; the ruling is a declaration of law for the whole country, not just the parties. In practice: once the Supreme Court settles a GST or income-tax issue, CAs across every State apply that view in returns and appeals.'),
    'm12': (T7, 'Audi alteram partem means "hear the other side": before an adverse decision, the affected person must get notice and a fair chance to present his case. The tempting trap is "the judge have no interest in the case" — that is the separate rule against bias, nemo judex in causa sua. In practice: if a tax officer passes an order without granting the hearing requested in reply to a show-cause notice, the CA challenges it as a breach of natural justice.'),
    'm13': (T8, 'The Department of States belongs to the Ministry of Home Affairs, which handles internal security and Centre–State matters. The Ministry of Finance\'s departments include Revenue, Expenditure, Economic Affairs, Financial Services, DIPAM and Public Enterprises. The trap is that "States" sounds like Centre–State finances, which tempts students to place it in Finance. In practice: a CA dealing with an income-tax issue knows the CBDT sits under Finance\'s Department of Revenue, so its circulars govern.'),
    'm14': (T8, 'The Ministry of Corporate Affairs administers the Companies Act, 2013 (and the 1956 Act), the LLP Act, 2008 and the Insolvency and Bankruptcy Code, 2016. The tempting trap is the Ministry of Law and Justice — it drafts legislation and advises ministries but does not administer these business laws. RBI regulates banks, not company or LLP law. In practice: a CA files LLP and company annual returns on the MCA portal and follows MCA notifications for insolvency matters.'),
    'm15': (T9, 'SEBI was set up on 12 April 1988 as a non-statutory body and gained statutory powers on 30 January 1992 under the SEBI Act, 1992. The tempting trap is 1988, which is its date of formation, not of statutory status. 2016 relates to IBBI. In practice: SEBI\'s statutory powers let it frame binding regulations, such as the listing obligations a CA checks during the audit of a listed company.'),
    'm16': (T9, 'The Insolvency and Bankruptcy Board of India, set up on 1 October 2016 under the IBC, regulates insolvency professionals, their agencies and information utilities. The tempting trap is NCLT — it is the adjudicating tribunal that decides insolvency cases of companies and LLPs, not the regulator of professionals. In practice: many CAs register with IBBI as insolvency professionals and act as resolution professionals in cases admitted by the NCLT.'),
    'm17': (T10, 'Article 32 lets a person go straight to the Supreme Court by writ petition to enforce a fundamental right — itself a fundamental right. The tempting trap is Article 226, which gives the High Courts writ power (wider, covering legal rights too). Article 141 is about binding precedent and Article 214 provides for High Courts. In practice: businesses usually file writs in the High Court under Article 226 first; Article 32 is used for issues of national importance.'),
    'm18': (T10, 'A High Court\'s decision binds the courts within its own State only; for courts in any other State it is merely persuasive. Gujarat courts follow the Gujarat High Court and the Supreme Court. The trap is "binding", from thinking all High Courts are equal so each binds the others — it does not. In practice: a CA in Ahmedabad may cite a favourable Madras High Court ruling before a tax officer, but the officer is not bound to follow it.'),
    'm19': (T10, 'Territorial jurisdiction depends on local limits — where the defendant resides or carries on business, or where the disputed property is situated. The tempting trap is "the date the contract was signed", which affects limitation, not which court can hear the case. Age and religion are irrelevant to jurisdiction. In practice: before filing a recovery suit, a CA and lawyer check where the debtor is located and where the contract was performed, and often include a jurisdiction clause in the contract.'),
    'k1/k1a': (T7, 'The officer passed the final order the day after the show-cause notice without hearing Saffron, so the strongest ground is breach of audi alteram partem — the right to a fair hearing. The tempting trap is lack of territorial jurisdiction, but nothing in the facts suggests the officer acted outside his area. Stare decisis and Article 141 concern precedent. In practice: tax appellate authorities regularly set aside orders passed without a personal hearing and send the matter back for fresh decision.'),
    'k1/k1b': (T5, 'Forging cheques is a public wrong, so it is a criminal matter: the Bharatiya Nyaya Sanhita, 2023 defines the offence and the Bharatiya Nagarik Suraksha Sanhita, 2023 governs investigation and trial. The trap is "only the Code of Civil Procedure" — Saffron may also sue civilly to recover the money, but that does not make the forgery a civil matter. In practice: the company files an FIR, and its CA preserves bank statements and the audit trail as evidence.'),
    'k1/k1c': (T5, 'Recovering ₹6,20,000 for goods supplied is a private dispute where the remedy sought is payment, so it is a civil suit for recovery of money under the CPC. The tempting trap is an insolvency matter before IBBI — IBBI is a regulator and does not decide recovery claims; insolvency petitions go to the NCLT. In practice: a CA prepares the ledger account and invoices that support the recovery suit, usually after a legal notice demanding payment.'),
    'k1/k1d': (T6, 'Under Article 141 the Supreme Court\'s law binds all courts and authorities in India, whatever its date. A High Court of another State binds only courts in that State; elsewhere it is just persuasive. The tempting trap is "the more recent High Court decision" — being newer does not let a lower court override the Supreme Court. In practice: a CA drafting a reply to an assessing officer must follow the Supreme Court view even if a later High Court ruling elsewhere favours the client.'),
}


_build_core = build


def build():
    """Applies the teaching explanation and topic tag to every MCQ (unit set and case-study sets)."""
    u = _build_core()
    for q in u['mcqs']:
        q['topic'], q['explain'] = EXPLAIN[q['id']]
    for cs in u.get('cases') or []:
        for q in cs['mcqs']:
            q['topic'], q['explain'] = EXPLAIN[cs['id'] + '/' + q['id']]
    return u


# ---------------------------------------------------------------------------------------------
# Offline auto-check data for the Write tab (matched by tools/ca_vivamatch.py / js/ca-tools.js).
# Per scheme point: kw = keyword groups ("a|b" = alternatives), min = groups needed, nums = figures
# that must appear, wrong/say = remark for a common wrong statement, ai_only = left to AI examiners.
# ---------------------------------------------------------------------------------------------
def _k(*groups, n=None, **extra):
    d = {'kw': list(groups), 'min': len(groups) if n is None else n}
    d.update(extra)
    return d


AUTO = {
    'q1': {'extra_ok': True,
           's1': _k('law', 'rules|obligations|duties|body|principles|norms', 'state|government|society|enforce|enforced|order|justice'),
           's2': _k('bill', 'proposed|draft|proposal|introduced|introduce'),
           's3': _k('lok sabha|lower house|house of the people', 'rajya sabha|upper house|council of states', 'pass|passed|debate|approve|approved|vote'),
           's4': _k('president', 'assent|approve|approval|sign|signs|consent'),
           's5': _k('gazette|notified|notification', 'act|effective date|in force|into force|enforce|commence'),
           },
    'q2': {'extra_ok': True,
           's1': _k('public|society|state|community', 'private|individual|individuals|persons|between parties|organisations'),
           's2': _k('punish|punishment|imprisonment|jail|penalty', 'compensation|compensate|remedy|damages|settle|settlement|relief|injunction|recovery'),
           's3': _k('bharatiya nyaya sanhita|nyaya sanhita|bns|bharatiya nagarik suraksha sanhita|nagarik suraksha|bnss', 'civil procedure|cpc|code civil',
                    wrong=[{'kw': ['indian penal code|ipc|criminal procedure 1973|crpc'], 'say': 'The IPC and CrPC have been replaced by the Bharatiya Nyaya Sanhita, 2023 and the Bharatiya Nagarik Suraksha Sanhita, 2023 — name the new codes.'}]),
           's4': _k('murder|theft|cheating|assault|robbery|kidnapping|dacoity|rape|hurt', 'breach of contract|breach contract|non payment|unpaid|dues|landlord|tenant|property dispute|divorce|recovery|defamation|partition|tort'),
           },
    'q3': {'extra_ok': True,
           's1': _k('supreme court', 'apex|highest court|top court|highest judicial', 'chief justice|cji', '34|thirty four|article 126|7 judges|seven', n=3),
           's2': _k('article 32|art 32|writ petition', 'article 141|art 141|binding on all|binds all|bind all|binding|final'),
           's3': _k('high court', 'article 214|214|each state|every state|state', 'original|appellate|supervisory|jurisdiction|25'),
           's4': _k('article 226|art 226|226|writ|writs', 'persuasive|subordinate|binding|bind'),
           's5': _k('companies act', 'llp|limited liability partnership', 'insolvency|bankruptcy|ibc', n=2),
           's6': _k('indian corporate law service|icls|corporate law service|director general|upsc|civil services|regulates|regulation|regulating'),
           },
}


_build_noauto = build


def build():
    """Adds the offline auto-check fields (kw/min/nums/wrong) to every scheme point."""
    u = _build_noauto()
    for q in u['questions']:
        a = AUTO[q['id']]
        q['extra_ok'] = a.get('extra_ok', False)
        if '_scheme' in a: q['scheme'] = a['_scheme']        # "any N points" split into N one-mark points
        for s in q['scheme']:
            s.update(a[s['id']])
    return u
