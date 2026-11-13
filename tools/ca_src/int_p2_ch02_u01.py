"""CA Intermediate · Paper 2 Corporate and Other Laws · Chapter 2 Incorporation of Company and Matters Incidental Thereto (ss. 3–22).
Scope follows the ICAI study material; provisions are explained in original words; examples are original."""
from ikit import *

UID = 'int-p2-ch02-u01'
T1 = 'Promoters and formation of companies (s. 3, 3A)'
T2 = 'One Person Company'
T3 = 'Incorporation procedure (s. 7) and effect of registration (s. 9)'
T4 = 'Section 8 companies'
T5 = 'Memorandum of association and ultra vires'
T6 = 'Articles of association and entrenchment'
T7 = 'Constructive notice and indoor management'
T8 = 'Binding effect and overriding effect (s. 6, 10)'
T9 = 'Altering memorandum, name and articles (s. 13–16)'
T10 = 'Registered office and commencement of business (s. 12, 10A)'
T11 = 'Conversion, subsidiary holding shares, documents (s. 18–22)'


def build():
    ro = table(['Shift of registered office', 'Approval needed', 'Key time limits'], [
        ['Within the same city, town or village', 'Board resolution', 'Notice to ROC within 30 days of the change'],
        ['Outside local limits, same ROC', 'Special resolution', 'Notice to ROC within 30 days'],
        ['To another ROC within the same State', 'Special resolution + confirmation by Regional Director', 'RD communicates within 30 days of application; company files within 60 days; ROC certifies within 30 days'],
        ['To another State', 'Special resolution + approval of Central Government (Regional Director)', 'Advertise not earlier than 30 days before applying; disposal within 60 days; file order with ROCs within 30 days; fresh certificate'],
    ], title='Changing the registered office')
    moa_aoa = table(['Basis', 'Memorandum', 'Articles'], [
        ['Nature', 'Charter — fundamental conditions; defines relations with outsiders', 'Internal rules; governs company–member and member–member relations'],
        ['Supremacy', 'Subordinate only to the Act', 'Subordinate to the Act and the memorandum; memorandum prevails on conflict'],
        ['Acts beyond it', 'Ultra vires the company — void, cannot be ratified even by all members', 'Can be ratified by members if within the memorandum'],
        ['Model forms', 'Tables A–E of Schedule I', 'Tables F–J of Schedule I'],
    ], title='Memorandum vs articles')
    s8 = table(['Matter', 'Rule'], [
        ['Objects', 'Education, research, sports, art, science, commerce, social welfare, environment protection, religion, charity and similar aims'],
        ['Profits', 'Applied only to promote objects; no dividend to members'],
        ['Name', 'Need not end with "Limited" or "Private Limited"'],
        ['Licence', 'Granted by the Central Government (delegated to ROC); application with MOA, AOA, professional declaration, 3-year income–expenditure estimate'],
        ['Altering MOA / AOA', 'Prior approval — Regional Director for MOA; ROC for AOA'],
        ['Conversion to another kind', 'Special resolution, application to RD in INC-18, notices to tax, charity and State authorities, newspaper notice within a week'],
        ['Revocation', 'For breach of conditions or fraudulent/prejudicial conduct; may be wound up or amalgamated with a similar section 8 company'],
        ['Penalty', 'Company ₹10 lakh to ₹1 crore; directors and officers in default ₹25,000 to ₹25 lakh; fraud — section 447'],
    ], title='Section 8 company at a glance')

    illus = [
        {'id': 'i1', 'title': 'Constructive notice or indoor management?', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'Decide each claim. (a) Kaveri Ltd.\'s articles say cheques above ₹1 lakh need two directors\' signatures. A supplier accepts a ₹3 lakh cheque signed by one director; it bounces. (b) The articles let directors borrow up to any limit approved by a general meeting resolution. A lender gives ₹50 lakh on the directors\' word without seeing the resolution; no resolution was ever passed. (c) A lender relied on a board resolution later found to be forged by the company secretary. (d) A director\'s brother lent money knowing the required shareholder approval had not been obtained.',
         'solution': [table(['Case', 'Doctrine', 'Result'], [
             ['(a) Single-signature cheque', 'Constructive notice', 'Supplier is deemed to know the articles — no claim against the company'],
             ['(b) Borrowing without resolution', 'Indoor management (Turquand\'s rule)', 'Lender may assume the internal resolution was passed — company bound'],
             ['(c) Forged resolution', 'Exception — forgery', 'Nothing validates forgery — company not bound'],
             ['(d) Lender knew of irregularity', 'Exception — knowledge', 'No protection — company not bound']], title='Answer')]},
        {'id': 'i2', 'title': 'Members below the minimum (s. 3A)', 'difficulty': 'core', 'minutes': 5,
         'q': 'Godavari Ltd., a public company, had 7 members. Two died on 1 June 2025; the remaining five knew this and carried on business without adding members. On 15 January 2026 the company borrowed ₹20 lakh and later defaulted. Who can the lender sue?',
         'solution': [legal('Section 3A — reduction of membership below the statutory minimum',
                            'Members fell to 5 (below 7) on 1 June 2025; business continued; loan taken on 15 January 2026.',
                            'If business continues for more than six months with fewer than seven members (two for a private company), every member who knows this is severally liable for the whole of the debts contracted after those six months. Six months expired on 1 December 2025; the loan came later.',
                            'The lender may sue the company or any of the five members individually for the full ₹20 lakh.')]},
    ]

    concepts = [
        C('c1', T1, [
            'Promoters are those who take the steps needed to bring a company into existence and set it going; they stand in a fiduciary position. Section 2(69) treats as promoter a person named as such in a prospectus or annual return, a person controlling the company\'s affairs, or one on whose instructions the Board acts — excluding those acting purely professionally. One who later helps float capital can also be a promoter.',
            'Section 3: any lawful object can be pursued through a company formed by 7 or more persons (public), 2 or more (private) or 1 person (OPC, a private company), by subscribing to the memorandum and complying with registration requirements. It may be limited by shares, limited by guarantee or unlimited.',
            'Section 3A: if membership falls below 7 (public) or 2 (private) and business continues for more than six months, every member aware of it is severally liable for all debts contracted after those six months and may be sued individually.'],
          'Promoters are the architects and builders of the company; section 3A says that if the house runs on too few owners for too long, the knowing owners pay its new bills personally.',
          'Start-up founders who incorporate a company and arrange its first funding are its promoters.'),
        C('c2', T2, [
            'Only a natural person who is an Indian citizen (resident in India or not), and not a minor, can form an OPC or be its nominee. Resident means stayed in India at least 120 days in the preceding financial year.',
            'The memorandum names a nominee (with prior written consent) who becomes the member on the subscriber\'s death or incapacity to contract. A person can be member of only one OPC and nominee of only one OPC; if a member becomes member of another OPC as a nominee, he must comply within 180 days.',
            'Nominee may withdraw consent by notice; the member then names a new nominee within 15 days. The member may change the nominee anytime with prior consent. When a nominee becomes the member, he names a new nominee within 15 days. The company files each change with the ROC within 30 days; such changes are not alterations of the memorandum.',
            'An OPC cannot be a section 8 company or carry on non-banking financial investment activities.',
            'Relaxations: no cash flow statement; annual return may be signed by a director; financial statements signed by one director; no AGM; one Board meeting in each half of a calendar year; financial statements filed within 180 days of year-end.'],
          'An OPC is a one-person band with an understudy (nominee) ready to take the stage.',
          'Professionals and small traders use OPCs to get limited liability without a co-founder.'),
        C('c3', T3, [
            'Steps: decide the type; reserve the name; draft and sign MOA and AOA; file with the ROC of the State of the proposed registered office through SPICe+ (INC-32) with e-MOA (INC-33) and e-AOA (INC-34); pay fees and stamp duty; obtain the certificate of incorporation.',
            'Documents: declaration of compliance (INC-8) by an advocate, CA, cost accountant or CS in practice engaged in formation and by a director, manager or secretary whom the articles name; declaration (INC-9) by each subscriber and first director that information is correct and that he has not been convicted in connection with company promotion or management or found guilty of fraud, misfeasance or breach of duty in the last five years; address for correspondence; particulars and consent (DIR-2) of first directors; particulars of subscribers; regulator approvals for regulated objects.',
            'Subscribers sign MOA and AOA before a witness; a body corporate signs through an authorised director, officer or employee; foreign subscribers\' documents are notarised (and authenticated where required).',
            'The ROC registers the documents and issues the certificate of incorporation (INC-11) with a 21-character Corporate Identity Number. Copies of filed documents are kept at the registered office until dissolution. The certificate is not conclusive proof that everything before incorporation was in order.',
            'False information or suppression at or after incorporation exposes the persons concerned (promoters, first directors, declarants) to action for fraud under section 447; the NCLT may regulate management, make members\' liability unlimited, remove the name or order winding up, after hearing the company.',
            'Section 9: from the date in the certificate, the subscribers and later members become a body corporate with perpetual succession, able to hold and dispose of property and to contract, sue and be sued in its own name.'],
          'Incorporation is a birth certificate for the company — but a false birth certificate can still be cancelled.',
          'A CIN beginning with "L" signals a listed company; "U" an unlisted one.'),
        C('c4', T4, [
            'Section 8 lets the Central Government (through the ROC) license a person or association as a limited company if its objects promote education, research, sports, art, science, commerce, social welfare, environment protection, religion, charity or similar aims; it applies income only to those objects; and it prohibits dividends.',
            'Such companies need not use "Limited" or "Private Limited" yet enjoy the privileges of limited companies. A firm may be a member. An OPC cannot be a section 8 company.',
            'Changes to the memorandum need prior approval of the Regional Director and to the articles of the ROC. Conversion into another kind of company requires a special resolution, application to the RD, notices to tax, charity and State authorities (who may object within 60 days), a newspaper notice within a week, and up-to-date filings.',
            'The licence may be revoked for breach of conditions or fraudulent or prejudicial conduct, after a hearing; the company may then be wound up (surplus to a similar section 8 company or sold with proceeds to the Insolvency and Bankruptcy Fund) or amalgamated with a similar section 8 company. Penalties are in the table.',
            'Relaxations include 14 clear days\' notice for general meetings and exemption from certain board and committee requirements.'],
          'A section 8 company is a charity wearing a company\'s suit — limited liability, but every rupee must go to the cause.',
          'Many hospitals, schools, think-tanks and CSR foundations are section 8 companies (CIN contains "NPL").',
          blocks=[s8]),
        C('c5', T5, [
            'The memorandum is the company\'s charter. Clauses: name, situation (State of registered office), objects, liability, capital (for share companies), subscription/association, and nomination (OPC).',
            'Name: ends with "Limited" or "Private Limited" (not for section 8). It must not be identical with or too similar to an existing name, an offence under any law, or undesirable; words suggesting government patronage or terms like Board, Commission, National, Union, Republic, President, Bureau, Statutory need Central Government approval. Names "resemble" if they differ only by plural, spacing, punctuation, tense, spelling variation, translation, domain extension, word order, articles, an added place name or numerals.',
            'Name reservation: 20 days for a new company (extendable by fee to 40 or 60 days); 60 days for an existing company changing its name. If reserved on wrong information: before incorporation, the name is cancelled and the applicant faces penalty up to ₹1 lakh; after incorporation, the ROC may direct a change within three months by ordinary resolution, strike off the name or seek winding up.',
            'Objects clause and ultra vires: acts beyond the objects are void and cannot be ratified even by all members (Ashbury Railway Carriage v. Riche); members can seek injunctions; neither side can enforce such a contract. Acts incidental to the objects are valid. Acts beyond directors\' powers but within objects can be ratified by members. Widening objects later operates only prospectively.',
            'Liability clause: limited by shares — unpaid amount on shares; by guarantee — amount each member undertakes to contribute if wound up while a member or within one year after ceasing. Capital clause: authorised capital and its division into shares; each subscriber takes at least one share.'],
          'The objects clause is the fence around the company\'s field — anything outside the fence is no-man\'s land that no vote can claim.',
          'Modern memoranda list objects widely and include incidental powers so routine diversification stays within the fence.',
          blocks=[moa_aoa]),
        C('c6', T6, [
            'Articles contain the regulations for management and the matters prescribed; they form a contract between the company and members and among members.',
            'Entrenchment (s. 5(3)–(5)): articles may require stricter conditions than a special resolution to alter specified provisions. It can be included only on formation, or later by agreement of all members (private company) or by special resolution (public company). Notice goes to the ROC in SPICe+ at incorporation, or in MGT-14 within 30 days for existing companies.',
            'Model articles are in Tables F–J of Schedule I; a company may adopt any of them. For companies registered under this Act, model provisions apply automatically unless the registered articles exclude or modify them.'],
          'Entrenchment is a double lock on certain clauses — the usual key (special resolution) is not enough.',
          'Investors in start-ups often entrench their veto rights in the articles.'),
        C('c7', T7, [
            'Constructive notice (Ernest v. Nicholls): the memorandum and articles are public documents, so anyone dealing with the company is deemed to know their contents, whether read or not. A member may obtain copies of MOA, AOA and certain resolutions within seven days of request (s. 17).',
            'The doctrine is criticised as unrealistic, so courts developed indoor management (Royal British Bank v. Turquand): outsiders acting in good faith may assume that internal procedures — resolutions, approvals — have been duly carried out. It is an exception to constructive notice.',
            'Indoor management does not protect an outsider who knew of the irregularity, was negligent where enquiry was called for, relied on a forged document, where the very existence of the agent\'s authority is in question, or where the act is beyond the company\'s own powers.'],
          'Constructive notice says "read the rulebook"; indoor management says "you need not check whether the referee actually blew the whistle inside the locker room".',
          'Banks lending to companies ask for certified board resolutions, but need not verify how the meeting was conducted.'),
        C('c8', T8, [
            'Section 6: the Act overrides anything in the memorandum, articles, agreements or resolutions (whenever made); conflicting provisions are void — unless the Act itself says otherwise (e.g. some sections apply to private companies subject to their articles).',
            'Section 10: once registered, the memorandum and articles bind the company and its members as if signed by each — member to company (Borland\'s Trustee v. Steel Bros), company to member (Wood v. Odessa Waterworks) and member to member (Rayfield v. Hands).',
            'They do not create a contract with outsiders (Browne v. La Trinidad) even if the articles mention them. Money payable by a member under them is a debt due to the company.'],
          'The articles are a family agreement — binding on the family members, not on the neighbours named in it.',
          'A promoter named in the articles as permanent solicitor cannot enforce that clause as an outsider.'),
        C('c9', T9, [
            'Memorandum (s. 13): altered by special resolution, filed with the ROC, effective on registration.',
            'Name change: special resolution plus Central Government (ROC) approval, except merely adding/deleting "Private" on conversion. Not allowed while annual returns or financial statements are pending or deposits/debentures or interest are in default. Effective on issue of a fresh certificate.',
            'Rectification (s. 16): if a name is identical with or too similar to an existing name — on the RD\'s own motion or a registered trade-mark owner\'s application within three years — the company must change it within three months by ordinary resolution and notify the ROC within 15 days; otherwise the Central Government allots a new name.',
            'Registered office to another State: special resolution plus Central Government (RD) approval; creditors\' interests protected; see table.',
            'Objects change where prospectus money remains unutilised: special resolution by postal ballot with detailed notice, newspaper and website advertisement, and an exit offer to dissenting shareholders as per SEBI rules. The ROC certifies registration of altered objects within 30 days.',
            'Articles (s. 14): altered by special resolution, subject to the Act and memorandum; public-to-private conversion needs Central Government (RD) approval on application within 60 days of the resolution; altered articles filed with the ROC within 15 days. A private company whose altered articles drop the private-company restrictions ceases to be private. Every copy issued must show alterations (s. 15) — penalty ₹1,000 per copy.'],
          'Changing the memorandum is renovating the foundation — more approvals; changing the articles is rearranging the furniture — a special resolution usually does.',
          'ITC Limited changed its name several times as its ownership and business changed.'),
        C('c10', T10, [
            'Section 12: within 30 days of incorporation and always thereafter, the company must have a registered office able to receive communications, and verify it with the ROC within 30 days.',
            'It must display its name and registered office outside every place of business (in local language too), engrave its name on its seal (if any), print name, registered office, CIN, phone, e-mail and website on letters, bills and notices, and print its name on negotiable instruments. Former names used in the last two years must also be shown; an OPC adds "One Person Company" below its name.',
            'Changes need ROC notice within 30 days; approvals depend on how far it moves (table). The ROC may physically verify the office if he suspects no business is carried on. Default: penalty ₹1,000 per day up to ₹1 lakh.',
            'Section 10A: a company with share capital incorporated after the 2019 Ordinance may commence business or borrow only after (a) verifying its registered office and (b) a director files a declaration (INC-20A) within 180 days of incorporation, verified by a practising CS, CA or cost accountant, that every subscriber has paid for shares agreed to be taken (with regulator approvals attached where needed). Default: company ₹50,000; officers ₹1,000 per day up to ₹1 lakh; and the ROC may strike off the name.'],
          'The registered office is the company\'s legal home address — courts, regulators and creditors must always be able to knock on its door.',
          'Letterheads of Indian companies show the CIN and registered office because section 12 requires it.',
          blocks=[ro]),
        C('c11', T11, [
            'Section 18: a company may convert to another class by altering its memorandum and articles; the ROC closes the old registration and issues a fresh certificate. Debts, liabilities and contracts made before conversion are unaffected.',
            'Section 19: a subsidiary (or its nominee) cannot hold shares in its holding company; allotment or transfer to it is void. Exceptions: as legal representative of a deceased member, as trustee, or where it held the shares before becoming a subsidiary (it may keep them and vote only as permitted). It may also receive shares under a court- or Tribunal-sanctioned amalgamation.',
            'Section 20: documents may be served on a company at its registered office by registered post, speed post, courier, hand delivery or prescribed electronic mode; on the ROC or members by post, registered or speed post, courier, delivery or electronic mode. A member may ask for a particular mode on paying the fee fixed at the AGM. Notice of a meeting sent by post is deemed served 48 hours after posting.',
            'Section 21: documents, proceedings and contracts may be authenticated by any KMP or an officer or employee authorised by the Board. Section 22: bills, hundis and notes signed on the company\'s behalf by an authorised person bind it; deeds and powers of attorney are executed under the common seal or, without a seal, by two directors or a director and the company secretary.'],
          'A subsidiary buying its parent\'s shares would be a child holding a stake in its own parent — the law forbids it to avoid circular ownership.',
          'For a 21-clear-day AGM notice sent by post, companies post it at least 23 days before the meeting.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Incorporating a client\'s company', 'role': 'Practising CA',
         'situation': 'Two friends want a private company for a software business.',
         'steps': ['Check the name for resemblance and reserve it through SPICe+.', 'Draft MOA (objects wide enough) and AOA; collect subscriber and director KYC, DIR-2 consents and INC-9 declarations.', 'Sign INC-8 as the professional; after incorporation, file INC-20A within 180 days before business starts.'],
         'takeaway': 'Incorporation is followed by section 10A compliance before commencing business.'},
        {'id': 'j2', 'title': 'Shifting a registered office to another State', 'role': 'Company secretary',
         'situation': 'A company moves its registered office from Pune to Bengaluru.',
         'steps': ['Pass a special resolution altering the situation clause.', 'Advertise and serve notice; apply to the Regional Director in INC-23 with creditor list.', 'File the order with both ROCs within 30 days and obtain a fresh certificate.'],
         'takeaway': 'Inter-State shifts need Central Government (RD) approval and creditor protection.'},
    ]

    mcqs = [
        Q('m1', 'A private company can be formed by a minimum of:', ['Two persons', 'Seven persons', 'One person in all cases', 'Three persons'], 0,
          'Under section 3, a public company needs seven or more persons, a private company two or more, and an OPC one person. So the minimum for an ordinary private company is two. In practice: most family businesses start with two shareholder-directors.', 'c1', T1),
        Q('m2', 'Under section 3A, members become severally liable when business continues with fewer than the minimum members for more than:', ['Six months', 'Three months', 'One year', 'Thirty days'], 0,
          'If membership falls below seven (public) or two (private) and business continues for more than six months, members who know this are severally liable for debts contracted after those six months. The liability covers the whole of such debts. In practice: companies replace departing members promptly.', 'c1', T1),
        Q('m3', 'Who can incorporate a One Person Company?', ['A natural person who is an Indian citizen, resident or not, and not a minor', 'Any company', 'A foreign citizen resident in India', 'A minor through a guardian'], 0,
          'Only an Indian citizen who is a natural person and not a minor may form an OPC; residence in India is not required. Companies, foreigners and minors are excluded. In practice: NRIs who are Indian citizens can form OPCs.', 'c2', T2),
        Q('m4', 'When an OPC\'s nominee withdraws consent, the member must nominate a new person within:', ['15 days', '30 days', '60 days', '180 days'], 0,
          'On receiving the nominee\'s withdrawal notice, the sole member must nominate another person within fifteen days; the company then files the change with the ROC within thirty days. The 180-day period relates to holding membership in more than one OPC. In practice: keep a willing backup nominee.', 'c2', T2, 'moderate', check=15),
        Q('m5', 'The declaration of compliance in INC-8 at incorporation is given by:', ['A professional engaged in formation together with a director, manager or secretary whom the articles name', 'The Registrar', 'All shareholders', 'The statutory auditor only'], 0,
          'INC-8 is signed by an advocate, CA, cost accountant or CS in practice engaged in formation and by a director, manager or secretary whom the articles name. Subscribers and first directors file separate INC-9 declarations. In practice: professionals must verify documents before signing.', 'c3', T3),
        Q('m6', 'Which is NOT a result of registration under section 9?', ['Members become personally liable for all company debts', 'Perpetual succession', 'Power to hold property', 'Capacity to sue and be sued'], 0,
          'Registration creates a body corporate with perpetual succession, power to acquire and dispose of property and capacity to contract, sue and be sued. Members\' liability is governed by the type of company, not made unlimited by registration. In practice: the company owns its assets in its own name.', 'c3', T3),
        Q('m7', 'A section 8 company must:', ['Apply its income to its objects and not pay dividends', 'Use "Limited" in its name', 'Be formed only as an OPC', 'Distribute surplus to members on winding up'], 0,
          'Section 8 companies apply profits only to promote their objects and prohibit dividends; they need not use "Limited", cannot be OPCs, and surplus on winding up goes to a similar section 8 company or the Insolvency and Bankruptcy Fund. In practice: donors rely on these restrictions.', 'c4', T4),
        Q('m8', 'Penalty on a section 8 company for default in complying with the section is a fine of:', ['₹10 lakh to ₹1 crore', '₹25,000 to ₹25 lakh', '₹1,000 per day', '₹50,000 only'], 0,
          'The company faces a fine from ten lakh rupees to one crore rupees; directors and officers in default face ₹25,000 to ₹25 lakh, and fraud attracts section 447. The other amounts relate to different provisions. In practice: these heavy fines deter misuse of charitable status.', 'c4', T4, 'moderate'),
        Q('m9', 'In Ashbury Railway Carriage v. Riche, the contract to finance a railway in Belgium was held:', ['Ultra vires the company and void, incapable of ratification even by all shareholders', 'Valid because shareholders ratified it', 'Voidable at the option of Riche', 'Within the objects as "general contractors"'], 0,
          'The House of Lords held that the contract was beyond the objects clause and void; even unanimous shareholder approval could not ratify it. "General contractors" was read narrowly with the mechanical engineering business. In practice: objects clauses are now drafted widely.', 'c5', T5),
        Q('m10', 'An act beyond the directors\' authority but within the company\'s objects:', ['Can be ratified by the members', 'Is void and can never be ratified', 'Is a criminal offence in all cases', 'Requires Tribunal approval to ratify'], 0,
          'Acts ultra vires the directors but intra vires the company can be ratified by shareholders; only acts beyond the company\'s objects are incurably void. In practice: a director exceeding a cheque-signing limit can have the act ratified by the company.', 'c5', T5),
        Q('m11', 'A name reserved for an existing company proposing to change its name is valid for:', ['60 days from approval', '20 days from approval', '6 months', '1 year'], 0,
          'The ROC may reserve a name for twenty days for a new company and sixty days where an existing company is changing its name. New-company reservations can be extended for a fee. In practice: plan the general meeting within the reservation period.', 'c5', T5, 'moderate', check=60),
        Q('m12', 'An existing public company wishes to insert entrenchment provisions in its articles. It needs:', ['A special resolution', 'Consent of all members', 'Central Government approval', 'Only a Board resolution'], 0,
          'After formation, entrenchment requires agreement of all members in a private company and a special resolution in a public company. Notice is filed with the ROC in MGT-14 within thirty days. In practice: investors often negotiate entrenched rights.', 'c6', T6, 'moderate'),
        Q('m13', 'The doctrine of indoor management is:', ['An exception to the doctrine of constructive notice', 'The same as constructive notice', 'An extension of ultra vires', 'Unrelated to constructive notice'], 0,
          'Indoor management (Turquand\'s rule) protects outsiders by letting them assume internal procedures were followed, limiting the harsh effect of constructive notice. It does not apply where the outsider knew of the irregularity, was negligent or relied on forgery. In practice: lenders need not verify internal meetings.', 'c7', T7),
        Q('m14', 'An outsider cannot claim protection under indoor management where:', ['He relied on a document forged by an officer', 'He assumed a resolution was passed', 'He acted in good faith without knowledge', 'He dealt with an authorised director'], 0,
          'Forgery is an exception — a forged document is a nullity and binds no one. Indoor management protects outsiders who act in good faith assuming internal formalities were met. In practice: banks verify signatures to guard against forgery.', 'c7', T7),
        Q('m15', 'Under section 10, the articles do NOT bind:', ['The company to an outsider named in them', 'Members to the company', 'The company to members', 'Members to each other'], 0,
          'Registered memorandum and articles bind the company and members and members among themselves, but create no contract with outsiders, as in Browne v. La Trinidad. Money due from a member under them is a debt. In practice: outsiders need a separate contract.', 'c8', T8),
        Q('m16', 'A company is directed under section 16 to change a name that too nearly resembles another\'s. It must do so within:', ['Three months, by ordinary resolution', 'Thirty days, by special resolution', 'Six months, by Board resolution', 'One year, by Tribunal order'], 0,
          'On direction by the Central Government (Regional Director), the company must change its name within three months after passing an ordinary resolution and notify the ROC within fifteen days. Otherwise the Government allots a new name. In practice: trade-mark owners can apply within three years.', 'c9', T9, 'moderate'),
        Q('m17', 'Conversion of a public company into a private company requires:', ['Special resolution and approval of the Central Government (Regional Director)', 'Only a Board resolution', 'Only an ordinary resolution', 'NCLT approval in all cases'], 0,
          'Altering articles to convert a public company into a private one needs a special resolution and Central Government approval on application within sixty days; the altered articles are filed within fifteen days. In practice: minority protection is checked before approval.', 'c9', T9),
        Q('m18', 'A company must have a registered office within how many days of incorporation?', ['30 days', '15 days', '60 days', '180 days'], 0,
          'Section 12 requires a registered office capable of receiving communications within thirty days of incorporation and at all times thereafter, with verification filed within thirty days. The 180-day period relates to the section 10A declaration. In practice: verification is often done in SPICe+ itself.', 'c10', T10, check=30),
        Q('m19', 'The section 10A declaration about payment for subscribed shares must be filed within:', ['180 days of incorporation', '30 days', '1 year', '90 days'], 0,
          'A director files INC-20A within one hundred and eighty days of incorporation, verified by a practising professional, declaring that subscribers have paid for their shares; without it the company cannot commence business or borrow. In practice: delay attracts penalties and possible strike-off.', 'c10', T10, check=180),
        Q('m20', 'A subsidiary held 2% of its holding company\'s shares before becoming its subsidiary. It may:', ['Continue to hold those shares but not acquire more', 'Increase its holding freely', 'Must sell all shares immediately', 'Hold them only with Tribunal approval'], 0,
          'Section 19 bars a subsidiary from holding shares in its holding company, but an existing holding acquired before the relationship can be retained; it cannot be increased. In practice: groups review existing cross-holdings carefully before acquisitions.', 'c11', T11, 'moderate'),
        Q('m21', 'A notice of general meeting sent by post is deemed served:', ['48 hours after posting', 'On the day of posting', '7 days after posting', 'When actually read'], 0,
          'Section 20(2) deems a meeting notice served at the expiry of forty-eight hours after posting; other documents are served when they would be delivered in ordinary course. In practice: for 21 clear days\' notice, post at least 23 days before the meeting.', 'c11', T11, check=48),
    ]

    questions = [
        W('q1', 5, 'Explain the doctrine of indoor management and its exceptions.',
          [p('Under the rule in Royal British Bank v. Turquand, persons dealing with a company in good faith may assume that its internal requirements (such as resolutions and approvals) have been complied with; they are not bound to enquire into the regularity of internal proceedings. It is an exception to the doctrine of constructive notice.'),
           ul(['Knowledge of the irregularity.', 'Negligence, or suspicious circumstances that called for enquiry.', 'Forgery — nothing validates a forged document.', 'Where the very existence of the agent\'s authority is in question.', 'Where the act is beyond the company\'s own powers.'])],
          [S('s1', 'Meaning and case (Turquand)', 2, 'concept', 'turquand|indoor management', 'assume|presume'),
           S('s2', 'Exception to constructive notice', 0.5, 'concept', 'constructive notice'),
           S('s3', 'Exceptions — knowledge, negligence, forgery, others', 2.5, 'concept', 'knowledge', 'negligen|enquir|inquir', 'forg', n=2)],
          ['Cite the case and give at least four exceptions.'], ['Confusing it with ultra vires.'], ['Meaning, then a bulleted list of exceptions.']),
        W('q2', 4, 'Shubh Ltd. has its registered office in Nagpur and wants to shift it (a) to another place in Nagpur city, (b) to Pune (another ROC in Maharashtra), (c) to Hyderabad. State the approvals needed.',
          [ro],
          [S('s1', 'Within city — Board resolution, ROC notice in 30 days', 1, 'application', 'board resolution', '30 days'),
           S('s2', 'Different ROC same State — SR + RD confirmation', 1.5, 'application', 'special resolution', 'regional director'),
           S('s3', 'Another State — SR + Central Government (RD) approval', 1.5, 'application', 'central government|another state', 'special resolution|approval')],
          ['Answer each part separately.'], ['Saying the Tribunal approves inter-State shifts.'], ['Use the table.'], pad='table'),
        W('q3', 4, 'Distinguish between the memorandum and the articles of association.',
          [moa_aoa],
          [S('s1', 'Nature / relations governed', 1, 'concept', 'charter|fundamental|outsider', 'internal|member'),
           S('s2', 'Supremacy', 1, 'concept', 'subordinate|prevail|supreme'),
           S('s3', 'Effect of acts beyond them', 1, 'concept', 'ultra vires|ratif'),
           S('s4', 'Model forms / alteration', 1, 'concept', 'table|schedule|alter')],
          ['Four rows of contrast earn full marks.'], ['Saying articles prevail over memorandum.'], ['Use a table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is the effect of registration of a company under section 9?',
          'From the date in the certificate of incorporation, the subscribers and members become a body corporate with perpetual succession, with power to acquire, hold and dispose of property, and to contract and to sue and be sued in its own name.',
          [P('p1', 'Body corporate from date of certificate', 3, 'body corporate'), P('p2', 'Perpetual succession', 3, 'perpetual'), P('p3', 'Property, contract, sue and be sued', 4, 'property|contract|sue')], 'c3'),
        V('v2', 'Who can form an OPC and what is a nominee?',
          'Only a natural person who is an Indian citizen and not a minor, resident in India or abroad. The nominee, named in the memorandum with consent, becomes the member if the subscriber dies or becomes incapable of contracting.',
          [P('p1', 'Natural person, Indian citizen, not minor', 5, 'citizen|natural person'), P('p2', 'Nominee becomes member on death or incapacity', 5, 'nominee', 'death|incapacit|dies')], 'c2'),
        V('v3', 'What is the doctrine of ultra vires?',
          'An act beyond the objects in the memorandum is ultra vires the company and void; it cannot be ratified even by all the shareholders, as held in Ashbury Railway Carriage v. Riche.',
          [P('p1', 'Beyond objects in memorandum', 4, 'object|memorandum|beyond'), P('p2', 'Void, cannot be ratified', 4, 'void|ratif'), P('p3', 'Ashbury case', 2, 'ashbury')], 'c5'),
        V('v4', 'How can entrenchment provisions be added to articles?',
          'Only at formation, or later by agreement of all members in a private company or by special resolution in a public company, with notice to the Registrar.',
          [P('p1', 'At formation', 2, 'formation'), P('p2', 'All members — private', 3, 'all members|all the members'), P('p3', 'Special resolution — public', 3, 'special resolution'), P('p4', 'Notice to ROC', 2, 'registrar|roc|notice')], 'c6'),
        V('v5', 'What does section 10A require before a company commences business?',
          'Verification of the registered office with the Registrar and a declaration by a director within 180 days of incorporation that every subscriber has paid for the shares agreed to be taken.',
          [P('p1', 'Registered office verification', 4, 'registered office'), P('p2', 'Director declaration within 180 days', 3, '180'), P('p3', 'Subscribers paid for shares', 3, 'subscriber|paid')], 'c10'),
    ]

    cases = [{'id': 'k1', 'title': 'Starting up Saffron Wellness', 'difficulty': 'moderate',
              'case': 'Ritu, an Indian citizen working in Dubai, wants to form an OPC named "Saffron Wellness" with her 16-year-old son as nominee. Later the OPC will convert into a private company with her brother. A separate charitable arm, "Saffron Care Foundation", is planned as a section 8 company. The company\'s articles require two directors to sign cheques above ₹5 lakh.',
              'mcqs': [
                  M('k1a', 'Can Ritu form the OPC while living in Dubai?', ['Yes — an Indian citizen may form an OPC whether resident in India or not', 'No — only residents can', 'Only with RBI approval', 'Only after returning to India for 182 days'], 0,
                    'The rules allow any natural person who is an Indian citizen and not a minor, resident in India or otherwise, to incorporate an OPC. Residence matters only for other purposes. In practice: NRI citizens use OPCs for Indian ventures.', 'core', topic=T2),
                  M('k1b', 'Can her 16-year-old son be the nominee?', ['No — a nominee must not be a minor', 'Yes — any relative can', 'Yes, with court permission', 'Yes, if resident in India'], 0,
                    'The nominee must be a natural person, Indian citizen and not a minor, so a 16-year-old cannot be nominated; she can name another adult such as her brother. In practice: nominee consent in writing is filed with the incorporation documents.', 'core', topic=T2),
                  M('k1c', 'Saffron Care Foundation as a section 8 company:', ['Need not use "Limited" in its name and cannot pay dividends', 'Must be formed as an OPC', 'Can distribute profits to Ritu', 'Must have objects of trade only'], 0,
                    'A section 8 company is licensed for charitable-type objects, applies income to those objects, pays no dividends and need not use "Limited"; an OPC cannot be a section 8 company. In practice: such foundations often run CSR programmes.', 'moderate', topic=T4),
                  M('k1d', 'A supplier accepts a ₹7 lakh cheque signed by one director, which bounces. The supplier:', ['Cannot claim against the company, being deemed to know the articles', 'Can claim under indoor management', 'Can sue the bank', 'Can claim if the director was the MD'], 0,
                    'The two-signature rule is in the articles, a public document; under constructive notice the supplier is deemed to know it, so indoor management does not help where the restriction is visible on the face of the articles. In practice: check signing authority for large cheques.', 'moderate', topic=T7),
              ]}]

    return unit(UID, 'p2', 'int-p2-ch02', 1, 'Incorporation of Company and Matters Incidental Thereto',
                ['Explain promoters, modes of forming companies, OPC rules and section 3A liability.',
                 'Describe the incorporation procedure, effect of registration and section 8 companies.',
                 'Explain the memorandum and articles, ultra vires, entrenchment, constructive notice and indoor management.',
                 'Apply provisions on alteration of memorandum and articles, change of name and registered office.',
                 'Explain section 10A, conversion, section 19 and service and authentication of documents.'],
                {'difficulty': 'core', 'minutes': {'learn': 60, 'practice': 35}, 'prereq': ['int-p2-ch01-u01'],
                 'exam_tip': 'Frequent questions: OPC eligibility and nominee, section 8 features, ultra vires, indoor management exceptions, shifting of registered office, section 3A and section 19.'},
                concepts, illus, jobs, mcqs, questions,
                {'summary': ['Public 7, private 2, OPC 1 member; s.3A — severally liable after 6 months below minimum.',
                             'OPC: Indian citizen, not minor; nominee; one OPC only; relaxations.', 'Incorporation via SPICe+; INC-8, INC-9; certificate INC-11 with CIN.',
                             'Section 8: no dividend; no "Ltd" needed; RD/ROC approvals; heavy penalties.', 'MOA: name, situation, objects, liability, capital, subscription, nomination.',
                             'Ultra vires the company — void (Ashbury). Indoor management (Turquand) is an exception to constructive notice.',
                             'Alterations: MOA/AOA by special resolution; name change needs ROC approval; inter-State RO shift needs RD approval.',
                             's.10A declaration within 180 days; s.19 subsidiary cannot hold parent shares.'],
                 'remember': ['Name reservation 20 days (new) / 60 days (existing).', 'Meeting notice by post served after 48 hours.'],
                 'traps': ['Indoor management fails on forgery or knowledge.', 'A minor can never be an OPC nominee.']},
                [('Min. members', 'Public 7 · Private 2 · OPC 1'), ('s.3A trigger', 'Below minimum > 6 months'), ('Ultra vires case', 'Ashbury v. Riche'),
                 ('Indoor management', 'Royal British Bank v. Turquand'), ('s.10A declaration', 'Within 180 days')],
                viva, cases,
                topics=['Introduction to Incorporation of Companies & Promoter', 'Formation of Company', 'Members Severally Liable in Certain Cases', 'Incorporation of Company',
                        'Formation of Companies with Charitable Objects', 'Effect of Registration', 'Memorandum of Association', 'Articles of Association',
                        'Doctrine of Constructive Notice and Doctrine of Indoor Management', 'Act to Override Memorandum, Articles, etc.', 'Effect of Memorandum and Articles',
                        'Alteration of Memorandum', 'Alteration of Articles', 'Registered Office of Company', 'Commencement of Business', 'Conversion of Companies Already Registered',
                        'Subsidiary Company not to Hold Shares in its Holding Company', 'Service of Documents', 'Authentication of Documents', 'Execution of Bills of Exchange'])
