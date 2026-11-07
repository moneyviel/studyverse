"""CA Foundation · Paper 2 Business Laws · Chapter 5 The Limited Liability Partnership Act, 2008 (implicit single unit).
Original explanations and problems; sections cited by number. Penalties, time limits and financial-year spans are computed."""
from datetime import date
from lib import *
from ca_viva import V, P, ALT
from ca_cases import M

UID = 'fnd-p2-ch05-u01'


def Q(qid, marks, diff, pad, q, model, scheme, remarks, mistakes, tips, checks=None):
    d = {'id': qid, 'marks': marks, 'minutes': minutes(marks), 'difficulty': diff, 'pad': pad, 'q': q, 'model': model,
         'scheme': [{'id': f's{i+1}', 'pt': pt, 'm': m, 'skill': sk} for i, (pt, m, sk) in enumerate(scheme)],
         'remarks': remarks, 'mistakes': mistakes, 'tips': tips}
    if checks: d['checks'] = checks
    return d


def MC(mid, q, options, answer, explain, concept, diff='core', check=None, topic=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': diff}
    if check: d['check'] = check
    if topic: d['topic'] = topic
    return d


def build():
    # ---------- Illustration 3: Section 13 penalty ----------
    c3 = Checks()
    p72 = c3.add('500*72', '72 days of default at ₹500 a day — below the ₹50,000 cap')
    tot72 = c3.add('36000*4', 'LLP + 3 partners, each liable separately (72 days)')
    raw130 = c3.add('500*130', '130 days at ₹500 a day before applying the cap')
    cap = c3.add('50000', 'maximum per person under Section 13(4)')
    tot130 = c3.add('50000*4', 'LLP + 3 partners, each capped at ₹50,000 (130 days)')
    t3 = table(['Days of default', 'Per day (₹)', 'Computed (₹)', 'Payable by LLP (₹)', 'Payable by each partner (₹)', 'Total for LLP + 3 partners (₹)'], [
        [72, 500, p72, p72, p72, tot72],
        [130, 500, raw130, cap, cap, tot130],
    ], num=[1, 2, 3, 4, 5], title='Penalty under Section 13(4)', note='Each row is a separate situation, so no total row is struck.')

    # ---------- Illustration 4: first financial year of an LLP incorporated after 30 September ----------
    c4 = Checks()
    inc = date(2026, 11, 10); fy_end = date(2028, 3, 31)
    days = (fy_end - inc).days + 1
    d_chk = c4.add('21+31+365+31+29+31', 'days from 10 Nov 2026 to 31 Mar 2028, both inclusive (2028 is a leap year)')
    assert d_chk == days, (d_chk, days)
    months = c4.add('12+4+21/30', 'about 16 months and 21 days')

    # ---------- MCQ / case numbers ----------
    cm = Checks()
    m_pen = cm.add('500*40', 'penalty for 40 days of default')
    kc = Checks()
    k_pen = kc.add('500*150', 'computed penalty for 150 days')

    diff_pf = table(['Basis', 'LLP', 'Partnership firm'], [
        ['Governing law', 'LLP Act, 2008', 'Indian Partnership Act, 1932'],
        ['Legal status', 'Body corporate and separate legal entity', 'Not a body corporate; no separate legal entity'],
        ['Creation and registration', 'Created by registration, which is compulsory', 'Created by agreement; registration optional (but an unregistered firm cannot sue third parties)'],
        ['Perpetual succession', 'Yes — partners\' death, insolvency, retirement do not affect its existence', 'No — such events may dissolve or reconstitute the firm'],
        ['Liability of partners', 'Limited to agreed contribution (except for wilful fraud)', 'Unlimited, extends to personal assets'],
        ['Mutual agency', 'Partner is agent of the LLP only, not of other partners', 'Partner is agent of the firm and of other partners'],
        ['Name', 'Must end with "Limited Liability Partnership" or "LLP"', 'No such requirement'],
        ['Designated partners', 'At least two individuals, one resident in India', 'No such concept'],
        ['Annual filings', 'Statement of account and solvency, and annual return with the Registrar', 'No annual filing with the Registrar of Firms'],
        ['Foreign nationals / minors', 'Foreign nationals may be partners; minors cannot be admitted to benefits', 'Foreign nationals cannot be partners (the ICAI position — write this; in practice FEMA rules restrict rather than wholly bar it, e.g. NRIs/OCIs may invest on a non-repatriation basis); a minor may be admitted to benefits with consent of all partners'],
    ], title='LLP vs partnership firm')

    diff_co = table(['Basis', 'LLP', 'Company'], [
        ['Governing law', 'LLP Act, 2008', 'Companies Act, 2013'],
        ['Owners called', 'Partners (who contribute)', 'Members / shareholders (who hold shares)'],
        ['Internal governance', 'By the LLP agreement — flexible', 'By the Act and the articles — prescriptive'],
        ['Name ending', '"LLP" / "Limited Liability Partnership"', '"Limited" (public) or "Private Limited" (private)'],
        ['Number of owners', 'Minimum 2 partners; no maximum', 'Private: 2 to 200 members; public: minimum 7, no maximum'],
        ['Liability', 'Limited to agreed contribution (except wilful fraud)', 'Limited to the unpaid amount on shares (for a company limited by shares)'],
        ['Management', 'Partners, including designated partners, as the agreement provides', 'Board of directors elected by shareholders'],
        ['Minimum managers', '2 designated partners', 'Private: 2 directors; public: 3 directors'],
    ], title='LLP vs company')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch05', 'n': 1, 'title': 'The Limited Liability Partnership Act, 2008',
        'outcomes': ['Explain the concept of a Limited Liability Partnership as a hybrid of a company and a partnership, and its key definitions under Section 2.',
                     'State the rules on who may be a partner, the minimum number of partners and designated partners (Sections 4–7), and apply them to fact situations.',
                     'Describe the characteristics and advantages of an LLP, the incorporation process, registered office and effects of registration (Sections 11–14), and the rules on name (Sections 15–17).',
                     'Distinguish an LLP from a partnership firm and from a company, and compute time limits and penalties under the Act.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 40}, 'prereq': ['fnd-p2-ch04-u01', 'fnd-p2-ch04-u03'],
                 'exam_tip': 'Expect a 4–6 mark question on designated partners (Section 7), minimum partners (Section 6), incorporation (Sections 11–12) or LLP vs partnership firm. Problem questions often test the 120-day residency rule and "business for profit".'},
        'concepts': [
            {'id': 'c1', 'title': 'What is an LLP?',
             'body': ['A Limited Liability Partnership is a form of business entity that combines the limited liability of a company with the internal flexibility of a partnership. All the LLP\'s own assets are available to its creditors, but a partner risks only the contribution he agreed to bring in. Because it carries features of both, it is often called a hybrid between a company and a partnership.',
                      'Section 2(1)(n): an LLP is a partnership formed and registered under the LLP Act, 2008. Section 3: it is a body corporate, a legal entity separate from its partners, with perpetual succession.',
                      'Section 4: unless the Act says otherwise, the Indian Partnership Act, 1932 does not apply to an LLP.',
                      'Who uses it: professionals such as Chartered Accountants, Company Secretaries, Cost Accountants, advocates, engineers and consultants; knowledge-based and technology ventures; venture capital funds; small enterprises.'],
             'analogy': 'An LLP is a partnership wearing a company\'s raincoat: partners still run it among themselves, but the rain (business debts) falls on the LLP, not on their personal property.',
             'work': 'Many CA firms practise as LLPs. When advising clients on choosing a business form, CAs compare LLPs with partnerships and private companies on liability, compliance cost and taxation.'},
            {'id': 'c2', 'title': 'Important definitions (Section 2)',
             'body': ['Body corporate [2(1)(d)]: a company as defined in the Companies Act, 2013, and includes an LLP registered under this Act, an LLP incorporated outside India and a company incorporated outside India; it excludes a corporation sole, a registered co-operative society and any other body notified by the Central Government.',
                      'Business [2(1)(e)]: every trade, profession, service and occupation, except activities excluded by notification. Designated partner [2(1)(j)]: a partner designated as such under Section 7. Entity [2(1)(k)]: any body corporate and, for certain conversion and amalgamation provisions, a firm under the Partnership Act.',
                      'Financial year [2(1)(l)]: 1 April to 31 March; but an LLP incorporated after 30 September of a year may close its first financial year on 31 March of the year after the next. (For income-tax purposes the year always runs 1 April to 31 March.)',
                      'Foreign LLP [2(1)(m)]: an LLP formed outside India that establishes a place of business in India. LLP agreement [2(1)(o)]: a written agreement among the partners, or between the LLP and its partners, setting out their mutual rights and duties. Partner [2(1)(q)]: a person who becomes a partner in accordance with the LLP agreement.',
                      'Small LLP [2(1)(ta)]: an LLP whose contribution does not exceed ₹25 lakh (or a higher prescribed amount up to ₹5 crore) and whose turnover for the preceding year, as per its Statement of Accounts and Solvency, does not exceed ₹40 lakh (or a higher prescribed amount up to ₹50 crore), or which meets other prescribed conditions.'],
             'analogy': 'Definitions are the dictionary of the Act — learn the key words and every section reads more easily.',
             'work': 'Classification as a small LLP reduces filing fees and penalties. CAs check contribution and turnover against the limits in force each year before advising on compliance.'},
            {'id': 'c3', 'title': 'Partners, minimum number and designated partners (Sections 5–7)',
             'body': ['Section 5: both individuals and bodies corporate can be partners. Three kinds of individuals are barred: (a) a person declared of unsound mind by a competent court, while that declaration stands; (b) an insolvent who has not been discharged; and (c) a person whose own petition to be declared insolvent is still pending.',
                      'Section 6: every LLP must have at least two partners; there is no maximum. Should the partners drop to one and the LLP keep trading that way for over six months, that partner — if he knows he is carrying on alone — is personally liable for the LLP\'s obligations incurred during the period after those six months.',
                      'Section 7: each LLP needs a minimum of two designated partners, all of them individuals, with one or more resident in India. If all partners are bodies corporate (or some are bodies corporate), at least two individuals who are partners or nominees of the bodies corporate must act as designated partners. For this purpose a person counts as "resident in India" if he spent 120 days or more in India in the financial year.',
                      'Designated partners are responsible for the LLP\'s legal compliances and are answerable for penalties under the Act.'],
             'analogy': 'An LLP needs at least two players on the field (partners) and at least two captains (designated partners), with one captain living in India.',
             'work': 'When a client forms an LLP with NRI relatives, the CA checks the 120-day stay of the proposed designated partners and, if necessary, adds a resident individual as a second designated partner.'},
            {'id': 'c4', 'title': 'Characteristics of an LLP',
             'body': ['(1) Body corporate with a separate legal entity — it can own property, sue and be sued in its own name; its creditors are its own, not the partners\'. (2) Perpetual succession — death, insanity, retirement or insolvency of partners does not affect its existence. (3) Limited liability — partners are liable only up to their agreed contribution, which may be tangible or intangible.',
                      '(4) Mutual agency limited — every partner is an agent of the LLP, but not of the other partners, so one partner is not liable for another partner\'s independent or unauthorised acts or misconduct. (5) LLP agreement governs mutual rights and duties; where there is none, the Act\'s provisions apply. (6) Artificial legal person — created by law; it cannot marry, take an oath or be sent to jail.',
                      '(7) Common seal is optional [Section 14(c)]; if adopted, it is kept in safe custody and affixed in the presence of at least two designated partners. (8) Partners manage the business, but designated partners are responsible for compliance. (9) Minimum two partners, no maximum. (10) It must carry on a lawful business with a view to profit — an LLP cannot be formed for charitable or non-economic purposes.',
                      '(11) The Central Government may investigate its affairs. (12) Compromises, arrangements, mergers and amalgamations follow the LLP Act. (13) A partnership firm, a private company or an unlisted public company may convert into an LLP. (14) Documents are filed electronically on the MCA portal with a digital signature. (15) A foreign LLP may set up business in India and can be a partner in an Indian LLP.',
                      'Advantages: organised on the basis of an agreement, flexible without heavy procedure, easy to form and to dissolve, limited liability for all partners, flexible capital structure.'],
             'analogy': 'Think of an LLP as a company body (separate person, never dies, limited liability) with a partnership heart (run by agreement among partners).',
             'work': 'Lenders dealing with an LLP check its contribution and LLP agreement, since partners\' personal assets are not automatically available. CAs often prepare the Statement of Account and Solvency that lenders and the Registrar rely on.'},
            {'id': 'c5', 'title': 'Incorporation, registered office and effect of registration (Sections 11–14)',
             'body': ['Section 11: two or more persons associated for running a lawful business to earn profit subscribe their names to an incorporation document, which is filed with the Registrar of the State where the registered office will be situated, with the prescribed fee. It must be accompanied by a statement — by an advocate, Company Secretary, Chartered Accountant or Cost Accountant engaged in the formation, and by one of the subscribers — that all requirements of the Act and rules have been complied with.',
                      'The incorporation document states the LLP\'s name, its proposed business, the address of its registered office, the names and addresses of the persons who will be partners and designated partners on incorporation, and other prescribed information. A person who makes that statement knowing it to be false, or not believing it to be true, is punishable with imprisonment up to 2 years and a fine of not less than ₹10,000, extending up to ₹5 lakh.',
                      'Section 12: once the filing requirements are met, the Registrar registers the document within 14 days and issues a certificate of incorporation, signed and authenticated by his official seal. The certificate is conclusive evidence that the LLP is incorporated by that name.',
                      'Section 13: every LLP must have a registered office to which communications may be addressed; documents may be served there by post under certificate of posting, registered post or other prescribed manner. A change of registered office takes effect only when notice is filed with the Registrar. Default attracts a penalty of ₹500 a day on the LLP and on every partner, up to ₹50,000 each.',
                      'Section 14: on registration, the LLP can, in its own name, sue and be sued; acquire, own, hold, develop or dispose of property, movable or immovable, tangible or intangible; have a common seal if it chooses; and do whatever bodies corporate may lawfully do.'],
             'blocks': [t3],
             'analogy': 'Incorporation is the LLP\'s birth certificate: once the Registrar signs it, no one can argue that the LLP was not born.',
             'work': 'CAs are among the professionals who certify compliance at incorporation. Signing a false statement is a criminal offence — so the CA verifies identities, consents and addresses before certifying.'},
            {'id': 'c6', 'title': 'Name of an LLP (Sections 15–17)',
             'body': ['Section 15: the name must end with the words "limited liability partnership" or the acronym "LLP". The Central Government will not register a name that, in its opinion, is undesirable, or is identical with or too closely resembles the name of another LLP, a company or a registered trade mark.',
                      'Section 16: a name may be reserved, on application and fee, for a proposed LLP or for an existing LLP that wants to change its name; if the Registrar is satisfied that the name is not objectionable under Section 15, he reserves it for 3 months from the date of his intimation.',
                      'Section 17: if an LLP is registered (by oversight or otherwise) with a name identical with or too like that of an existing LLP, company or registered trade mark, the Central Government may, on application, direct it to change the name within 3 months. An application by a trade-mark owner must be made within 3 years of the LLP\'s incorporation, registration or change of name. After changing its name, the LLP must notify the Registrar within 15 days (with the Government\'s order) and amend its LLP agreement within 30 days of the change in the certificate. If it does not comply, the Government allots a new name and the Registrar issues a fresh certificate.'],
             'analogy': 'Section 15 is the "surname rule" — every LLP\'s name must end with its family name, LLP.',
             'work': 'Before filing for incorporation, CAs run name searches against company, LLP and trade-mark databases, because an approved name can still be challenged later under Section 17.'},
            {'id': 'c7', 'title': 'LLP compared with partnership firm and company',
             'body': ['Against a partnership firm, the LLP offers a separate legal personality, perpetual succession and limited liability, at the cost of compulsory registration and annual filings. Against a company, the LLP offers flexible internal governance by agreement, no limit on partners and lighter procedure, while giving similar limited liability.',
                      'Common exam bases: governing law, legal status, creation and registration, perpetual succession, liability, mutual agency, name, designated partners, compliance responsibility, annual filings, foreign partners and minors (versus a firm); and owners, governance, name, number of members, liability, management and minimum directors (versus a company).'],
             'blocks': [diff_pf, diff_co],
             'analogy': 'Firm: friends sharing a car with joint liability for every dent. Company: passengers on a bus run by a board. LLP: friends sharing a car, but each has insured only his own seat.',
             'work': 'Start-up founders often ask, "firm, LLP or private company?" The CA weighs liability, investor expectations (equity investors prefer companies), compliance cost and tax.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Choosing designated partners', 'difficulty': 'core', 'minutes': 6,
             'q': 'Five friends — Aman and Bilal (who live in Dubai and spent 40 and 65 days in India this financial year) and Chhavi, Dhara and Eshwar (all living in India) — are forming "Pinewood Analytics LLP". They want to appoint Aman and Bilal as the only designated partners. Advise.',
             'solution': [legal('Section 7: each LLP needs a minimum of two designated partners, all of them individuals, with one or more resident in India — that is, someone who spent 120 days or more in India in the financial year.',
                                'Aman stayed 40 days and Bilal 65 days in India — neither meets the 120-day test. Chhavi, Dhara and Eshwar live in India.',
                                'Appointing only Aman and Bilal would give two designated partners but no resident designated partner, which Section 7 does not allow.',
                                'The proposal is not valid. At least one of Chhavi, Dhara or Eshwar must be a designated partner (for example, Aman and Chhavi, or any two of the residents).')],
             'checks': [{'expr': '120-65', 'value': 55, 'label': 'Bilal falls short of the 120-day test by 55 days'}]},
            {'id': 'i2', 'title': 'An LLP for a charity?', 'difficulty': 'core', 'minutes': 5,
             'q': 'Some retired teachers want to register "Bright Minds LLP" to run free tuition classes for poor children, with no intention of earning profit. Can they?',
             'solution': [legal('Section 11(1)(a): an LLP is incorporated by two or more persons associated for running a lawful business to earn profit.',
                                'The proposed activity is free tuition with no profit motive.',
                                'Running a lawful business to earn profit is an essential condition. A charitable or non-economic purpose does not satisfy this requirement.',
                                'Bright Minds LLP cannot be incorporated for this purpose. The teachers may consider a trust, a society or a Section 8 company instead.')]},
            {'id': 'i3', 'title': 'Penalty for not maintaining a registered office', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'Silverline LLP has three partners. It shifted its registered office but did not file the notice of change with the Registrar as required by Section 13. Compute the maximum penalty on the LLP and on each partner if the default continues for (a) 72 days, (b) 130 days.',
             'solution': [legal('Section 13(4): if an LLP contravenes Section 13, the LLP and every partner are liable to a penalty of ₹500 for each day of continuing default, capped at ₹50,000 for the LLP and ₹50,000 for each partner.',
                                'Default periods: (a) 72 days; (b) 130 days. Three partners.',
                                f'(a) ₹500 × 72 = {R(p72)} each — below the cap; for the LLP and three partners together {R(tot72)}. (b) ₹500 × 130 = {R(raw130)}, which exceeds the cap, so each pays {R(cap)}; together {R(tot130)}. Also, under Section 13(3), the change takes effect only on filing.',
                                f'(a) {R(p72)} each (total {R(tot72)}); (b) {R(cap)} each (total {R(tot130)}).'),
                          t3],
             'checks': c3},
            {'id': 'i4', 'title': 'First financial year of an LLP', 'difficulty': 'moderate', 'minutes': 5,
             'q': 'Harbour Ventures LLP is incorporated on 10 November 2026. Up to what date may its first financial year run under the LLP Act, and how long is that period? Would income-tax law accept the same year?',
             'solution': [legal('Section 2(1)(l): an LLP\'s financial year runs from 1 April to 31 March; but for an LLP incorporated after 30 September, the financial year may end on 31 March of the year following the next year.',
                                'Incorporation: 10 November 2026, which is after 30 September 2026.',
                                f'The first financial year may run from 10 November 2026 to 31 March 2028 — {d_chk} days, a little over 16 months. For income tax, however, the previous year always ends on 31 March, so the LLP must compute income for 10 November 2026 to 31 March 2027 separately.',
                                'Under the LLP Act the first year may end on 31 March 2028; for income-tax purposes the year ends on 31 March 2027, so in practice LLPs follow the April–March year.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Converting a CA firm into an LLP', 'role': 'Partner in a CA firm', 'situation': 'Your four-partner CA firm wants to convert into an LLP to limit partners\' liability for business debts.',
             'steps': ['Confirm eligibility: a partnership firm may convert into an LLP under the Act.', 'Choose at least two designated partners who are individuals, one of them resident in India (120-day test).',
                       'Reserve the name ending in "LLP" (valid for 3 months) after checking it does not resemble another LLP, company or trade mark.', 'Draft the LLP agreement covering contributions, profit sharing, admission and retirement — otherwise the Act\'s default provisions apply.',
                       'File the incorporation and conversion documents electronically with digital signatures; inform clients, banks and the regulator of the change.'],
             'takeaway': 'Conversion gives limited liability for business debts, but partners remain personally liable for their own professional misconduct or wilful fraud.', 'think': 'After conversion, can a client sue a partner personally for another partner\'s negligent audit?',
             'answer': 'Not merely because he is a partner — a partner is not liable for another partner\'s independent or unauthorised acts; the claim lies against the LLP (and the negligent partner).'},
            {'id': 'j2', 'title': 'One partner left', 'role': 'CA advising a two-partner LLP', 'situation': 'One of the two partners of Orbit Designs LLP died on 1 June 2026. The surviving partner continues the business alone and asks whether there is any urgency to admit a new partner.',
             'steps': ['Section 6 requires at least two partners.', 'If the LLP carries on business with one partner for more than six months — here beyond 1 December 2026 — and he knows it, he becomes personally liable for the LLP\'s obligations incurred after that date.',
                       'Advise admitting a new partner (and designated partner, since Section 7 also needs two designated partners) well before 1 December 2026.', 'File the change in partners with the Registrar.'],
             'takeaway': 'The six-month window in Section 6 protects a lone partner only temporarily.', 'think': 'Is the surviving partner personally liable for debts incurred in July 2026?',
             'answer': 'No. Personal liability under Section 6 attaches only to obligations incurred after the six months, i.e. after 1 December 2026, while he knowingly carries on alone.'},
        ],
        'mcqs': [
            MC('m1', 'Does the Indian Partnership Act, 1932 apply to an LLP?', ['No, unless the LLP Act provides otherwise (Section 4)', 'Yes, fully', 'Yes, for all internal matters', 'Only to small LLPs'], 0, 'Section 4 of the LLP Act, 2008 says the Indian Partnership Act, 1932 does not apply to an LLP, except where the LLP Act itself provides otherwise. An LLP is a body corporate with its own legal identity, governed by its own Act and the LLP agreement. "Yes, for all internal matters" is the trap: internal relations are governed by the LLP agreement and the First Schedule of the LLP Act, not the Partnership Act. In practice: when a firm converts into an LLP, a CA drafts a fresh LLP agreement instead of relying on the old partnership deed.', 'c1', topic='What is an LLP?'),
            MC('m2', 'Which statement about the liability of partners in an LLP is correct?', ['Every partner\'s liability is limited to his agreed contribution (except for wilful fraud)', 'All partners have unlimited liability', 'Only designated partners have limited liability', 'Partners are jointly liable for each other\'s misconduct'], 0, 'In an LLP, every partner\'s liability is limited to the contribution he agreed to bring in. A partner is not personally liable for the LLP\'s debts or for other partners\' wrongful acts, though liability becomes unlimited where there is intent to defraud. "Only designated partners have limited liability" is the trap: limited liability protects every partner, and designated partners only carry extra compliance duties. In practice: professionals such as CAs and architects choose the LLP form so that one partner\'s negligence claim does not reach the other partners\' homes and savings.', 'c4', topic='Characteristics of an LLP'),
            MC('m3', 'Which of the following CANNOT be converted into an LLP?', ['A listed company', 'A partnership firm', 'A private company', 'An unlisted public company'], 0, 'The LLP Act allows conversion of a partnership firm (Second Schedule), a private company (Third Schedule) and an unlisted public company (Fourth Schedule) into an LLP. A listed company cannot convert, as its shares are traded publicly and its investors need the protection of company and securities law. An unlisted public company is the trap: it can convert, provided it meets the conditions. In practice: small private companies with low turnover often convert to LLPs to reduce compliance, but a listed company would first have to delist.', 'c4', topic='Characteristics of an LLP'),
            MC('m4', 'A name reserved under Section 16 remains reserved for:', ['3 months from the Registrar\'s intimation', '6 months', '1 year', '30 days'], 0, 'Section 16(2): once the Registrar approves an application to reserve a name, the name stays reserved for three months from the date the Registrar intimates the applicant. If the LLP is not incorporated in that time, the name lapses. Six months is the trap, often confused with other filing periods. In practice: CAs file the name reservation and the incorporation documents close together, so that the approved name does not lapse while the LLP agreement is still being finalised.', 'c6', topic='Name of an LLP (Sections 15–17)'),
            MC('m5', 'The name of every LLP must end with:', ['"Limited Liability Partnership" or "LLP"', '"Limited"', '"Private Limited"', '"OPC"'], 0, 'Section 15(1): the name of every LLP must end with "limited liability partnership" or its short form "LLP". This warns everyone dealing with it that the partners\' liability is limited. "Limited" is the trap: that ending belongs to a public company. "Private Limited" belongs to private companies and "OPC" to one person companies. In practice: invoices, letterheads and websites of an LLP must show the full name ending in "LLP", or creditors may argue that they were misled.', 'c6', topic='Name of an LLP (Sections 15–17)'),
            MC('m6', 'For Section 7, a person is treated as "resident in India" if, during the financial year, he spent in India at least:', ['120 days', '182 days', '180 days', '60 days'], 0, 'The Explanation to Section 7 treats a person as resident in India if he has stayed in India for at least 120 days during the financial year. At least one designated partner must meet this test. 182 days is the trap: that is a figure from income-tax residence rules, not the LLP Act. In practice: when foreign promoters set up an Indian LLP, a CA makes sure at least one designated partner actually spends 120 days a year in India, or the LLP will not comply.', 'c3', 'core', '120', topic='Partners, minimum number and designated partners (Sections 5–7)'),
            MC('m7', 'Every LLP must have at least:', ['Two partners and two designated partners who are individuals, one resident in India', 'Seven partners', 'Two partners and one designated partner', 'Three designated partners'], 0, 'Section 6 requires every LLP to have at least two partners, and Section 7 requires at least two designated partners who are individuals, at least one of whom is resident in India. "Two partners and one designated partner" is the trap: the law requires two designated partners, not one. Seven is the minimum for a public company, not an LLP. In practice: two people starting an LLP usually become both partners and designated partners, which satisfies both sections at once.', 'c3', topic='Partners, minimum number and designated partners (Sections 5–7)'),
            MC('m8', 'An individual is NOT capable of becoming a partner of an LLP if he:', ['Is an undischarged insolvent', 'Is a foreign national', 'Is a Chartered Accountant', 'Holds shares in a company'], 0, 'Section 5 says an individual cannot become an LLP partner if a competent court has found him of unsound mind and the finding is in force, if he is an undischarged insolvent, or if he has applied to be declared insolvent and the application is pending. A foreign national is the trap: foreigners can be partners, and only one designated partner must be resident in India. Being a CA or a shareholder is no bar. In practice: CAs check personal declarations from proposed partners before filing the incorporation documents.', 'c3', topic='Partners, minimum number and designated partners (Sections 5–7)'),
            MC('m9', 'If the number of partners falls below two and business continues beyond six months, the sole partner is:', ['Personally liable for obligations incurred after six months, if he knows he is alone', 'Never personally liable', 'Liable for all obligations from the date of incorporation', 'Liable only to the Registrar for a fine'], 0, 'Section 6(2): if the LLP is left with fewer than two partners and keeps doing business beyond six months, the remaining partner is personally liable for obligations incurred after those six months, if he knows that he is the only partner. "Never personally liable" is the trap: limited liability is lost to stop one person using the LLP indefinitely. Liability does not go back to incorporation. In practice: when a partner exits or dies, the remaining partner should admit a new partner within six months.', 'c3', 'moderate', topic='Partners, minimum number and designated partners (Sections 5–7)'),
            MC('m10', 'On receiving a complete incorporation document, the Registrar must register it and issue a certificate within:', ['14 days', '7 days', '30 days', '3 months'], 0, 'Section 12(1): when the incorporation document complies with the Act, the Registrar must register it and issue a certificate of incorporation within 14 days of filing. 30 days is the trap: it is a common period elsewhere in law, but this provision gives 14 days. The certificate states that the LLP is incorporated under the name given. In practice: in reality the MCA processes LLP incorporation online through the FiLLiP form, and approval often comes within a few working days.', 'c5', 'core', '14', topic='Incorporation, registered office and effect of registration (Sections 11–14)'),
            MC('m11', 'The certificate of incorporation issued by the Registrar is:', ['Conclusive proof that the LLP has been incorporated under that name', 'Only prima facie evidence', 'Valid for 3 years', 'Required to be renewed annually'], 0, 'Under Section 12, the certificate of incorporation issued by the Registrar is conclusive evidence that the LLP has been incorporated under the name stated in it. Nobody can later challenge the fact of incorporation on the ground of a defect in the process. "Only prima facie evidence" is the trap: prima facie evidence could be rebutted, but conclusive evidence cannot. The certificate never needs renewal. In practice: banks and clients accept the certificate of incorporation as final proof that the LLP legally exists.', 'c5', topic='Incorporation, registered office and effect of registration (Sections 11–14)'),
            MC('m12', 'An LLP fails to comply with Section 13 for 40 days. The penalty on each partner is:', [R(m_pen), '₹500', '₹50,000', '₹40,000'], 0, 'Under Section 13, if an LLP fails to comply with the registered-office requirements, the LLP and every partner are each liable to a penalty of ₹500 for each day of default, up to ₹50,000. For 40 days: ₹500 × 40 = ₹20,000, which is below the cap, so it is fully payable. ₹50,000 is the trap: the maximum applies only when the daily total exceeds it. In practice: CAs file the change of registered office on time, because a short delay costs every partner separately.', 'c5', 'moderate', '500*40', topic='Incorporation, registered office and effect of registration (Sections 11–14)'),
            MC('m13', 'Which statement about LLPs is INCORRECT?', ['A listed company can convert into an LLP', 'An LLP has a legal personality separate from its partners', 'The liability of each partner is limited', 'A foreign LLP can be a partner in an Indian LLP'], 0, "The question asks for the wrong statement. A listed company cannot convert into an LLP; conversion is open only to firms, private companies and unlisted public companies. The other three statements are correct: an LLP is a separate legal entity, each partner's liability is limited, and a body corporate, including an LLP incorporated outside India, can be a partner. The trap is the foreign-LLP statement, which looks wrong but is true. In practice: foreign consulting firms often become partners in Indian LLPs.", 'c4', 'moderate', topic='Characteristics of an LLP'),
            MC('m14', 'An LLP can be formed for:', ['A lawful business with a view to profit', 'Charitable purposes only', 'Any purpose, profit or not', 'Social clubs'], 0, 'Section 11(1)(a): to incorporate an LLP, two or more persons must subscribe to an incorporation document to run a lawful business aimed at earning profit. So an LLP cannot be formed for purely charitable or social purposes. "Any purpose, profit or not" is the trap: the profit motive is essential. Charities usually use a trust, society or Section 8 company. In practice: an NGO wanting limited liability registers as a Section 8 company, not an LLP.', 'c4', topic='Characteristics of an LLP'),
            MC('m15', 'A trade-mark owner who objects to an LLP\'s name must apply to the Central Government within:', ['3 years of incorporation, registration or change of name', '3 months', '1 year', '15 days'], 0, "Under the proviso to Section 17(1), a registered trade-mark owner who believes an LLP's name is identical to, or too similar to, its trade mark must apply to the Central Government within three years of the LLP's incorporation, registration or change of name. Three months is the trap: it is the period for name reservation. In practice: brand owners run regular searches of the MCA database to spot similar LLP names early and object within the three-year window.", 'c6', 'moderate', topic='Name of an LLP (Sections 15–17)'),
        ],
        'questions': [
            Q('q1', 4, 'core', 'text',
              'What is a "designated partner"? Is it compulsory for an LLP to appoint designated partners? Explain with reference to the LLP Act, 2008.',
              [p('Section 2(1)(j): a designated partner is a partner designated as such under Section 7.'),
               p('Section 7 makes it compulsory: each LLP needs a minimum of two designated partners, all of them individuals, with one or more resident in India.'),
               p('Where all the partners are bodies corporate, or some partners are bodies corporate and some individuals, at least two individuals who are partners or nominees of the bodies corporate must act as designated partners.'),
               p('A person counts as "resident in India" if he spent 120 days or more in India during the financial year.'),
               p('Designated partners are responsible for the LLP\'s compliance with the Act and are liable to penalties for non-compliance. Hence appointing them is mandatory.')],
              [('Meaning under Section 2(1)(j)', 1, 'concept'), ('Section 7: two individuals, one resident', 1.5, 'provision'), ('Body-corporate partners and nominees', 0.5, 'provision'), ('120-day residency and conclusion', 1, 'conclusion')],
              ['Full marks need both the definition and the Section 7 requirements, including residency.'],
              ['Writing "182 days" for residency.', 'Forgetting that designated partners must be individuals.'],
              ['Start with the definition, then "Yes, it is compulsory because…".']),
            Q('q2', 5, 'moderate', 'legal',
              'Five friends — Mr. P and Mr. Q (non-residents) and Ms. R, Ms. S and Ms. T (residents) — decide to form "Learn Free LLP" to run an online school for underprivileged children on a non-profit basis. They propose that Mr. P and Mr. Q be its designated partners. Answer with reasons: (i) Can the LLP be formed for this purpose? (ii) Can Mr. P and Mr. Q be the designated partners?',
              [p('(i)'), legal('Section 11(1)(a): to incorporate an LLP, two or more persons must be associated for running a lawful business to earn profit.',
                               'The friends intend to run a non-profit online school.',
                               'A non-profit, charitable activity does not meet the requirement of carrying on business with a view to profit.',
                               'Learn Free LLP cannot be formed for this purpose.'),
               p('(ii)'), legal('Section 7: each LLP needs a minimum of two designated partners, all of them individuals, with one or more resident in India (stayed at least 120 days during the financial year).',
                                'Mr. P and Mr. Q are non-residents; Ms. R, Ms. S and Ms. T are residents.',
                                'If only Mr. P and Mr. Q are designated partners, there is no resident designated partner.',
                                'They cannot both be the only designated partners; at least one of Ms. R, Ms. S or Ms. T must be a designated partner.')],
              [('(i) Section 11 — business with a view to profit', 1, 'provision'), ('(i) Application and conclusion', 1.5, 'conclusion'), ('(ii) Section 7 requirements', 1, 'provision'), ('(ii) Application and conclusion', 1.5, 'conclusion')],
              ['Both parts must cite the section; many candidates answer only "No" without reasons.'],
              ['Saying an LLP can be formed for charity.', 'Saying non-residents can never be designated partners (one non-resident is fine if another designated partner is resident).'],
              ['Treat each sub-part as a short PFAC answer.']),
            Q('q3', 6, 'moderate', 'table',
              'Distinguish between a Limited Liability Partnership and a partnership firm on any six bases.',
              [diff_pf],
              [('Legal status / separate entity', 1, 'concept'), ('Registration and creation', 1, 'concept'), ('Perpetual succession', 1, 'concept'), ('Liability of partners', 1, 'concept'), ('Mutual agency', 1, 'analysis'), ('Any sixth valid point', 1, 'analysis')],
              ['A clean table with six bases scores full marks. Liability and separate legal entity are must-have points.'],
              ['Saying registration of a partnership firm is compulsory.', 'Saying an LLP partner is an agent of other partners.'],
              ['Write the governing Act in the first row — it frames the whole comparison.']),
            Q('q4', 4, 'core', 'text',
              'State the effects of registration of an LLP under Section 14, and list who cannot become a partner under Section 5.',
              [p('Section 14 — on registration, an LLP by its name is capable of:'),
               ul(['suing and being sued;', 'acquiring, holding, developing and selling property of every kind — movable, immovable, tangible or intangible;', 'adopting a common seal, which is optional;', 'doing anything else that a body corporate is legally permitted to do.']),
               p('Section 5 — individuals and bodies corporate can be partners, but these individuals are barred:'),
               ul(['a competent court has found him to be of unsound mind and the finding is in force;', 'he is an undischarged insolvent; or', 'he has applied to be adjudicated an insolvent and the application is pending.'])],
              [('Section 14 effects (any three or four)', 2, 'provision'), ('Section 5 disqualifications (all three)', 2, 'provision')],
              ['Easy marks — list format is ideal.'],
              ['Saying a common seal is compulsory.', 'Adding "minor" to Section 5 as if it were a listed disqualification (minors simply cannot contract; the Act lists the three cases above).'],
              ['Two headed lists; no long paragraphs needed.']),
        ],
        'revision': {'summary': ['LLP: hybrid of company and partnership; body corporate, separate legal entity, perpetual succession (Section 3); Partnership Act does not apply (Section 4).',
                                 'Partners (5): individual or body corporate; disqualified — unsound mind (court finding), undischarged insolvent, pending insolvency application.',
                                 'Minimum 2 partners; sole partner beyond 6 months personally liable for later obligations (6). No maximum.',
                                 'Designated partners (7): at least 2 individuals, at least 1 resident (120 days in the financial year).',
                                 'Incorporation (11): two or more persons, lawful business with a view to profit; professional\'s compliance statement; false statement — up to 2 years and fine ₹10,000 to ₹5 lakh. Registrar registers within 14 days; certificate conclusive (12).',
                                 'Registered office (13): change effective on filing; penalty ₹500/day, max ₹50,000 each. Effects of registration (14).',
                                 'Name (15) ends with LLP; reservation 3 months (16); direction to change within 3 months, trade-mark objection within 3 years, notice in 15 days, agreement change in 30 days (17).'],
                     'remember': ['Small LLP: contribution up to ₹25 lakh (or prescribed up to ₹5 crore) and turnover up to ₹40 lakh (or prescribed up to ₹50 crore).', 'Financial year: 1 April–31 March; incorporated after 30 September — first year may end 31 March of the year after next.', 'Listed companies cannot convert into LLPs.'],
                     'traps': ['120 days, not 182 days, for designated-partner residency.', 'Common seal is optional.', 'LLP cannot be formed for charity.', 'A partner is an agent of the LLP, not of other partners.']},
        'quickref': [{'k': 'Section 2(1)(n)', 'v': 'LLP = partnership formed and registered under the Act'}, {'k': 'Section 2(1)(ta)', 'v': 'Small LLP — contribution and turnover limits'},
                     {'k': 'Section 3', 'v': 'Body corporate, separate legal entity, perpetual succession'}, {'k': 'Section 4', 'v': 'Partnership Act, 1932 not applicable'},
                     {'k': 'Section 5', 'v': 'Who may be a partner; three disqualifications'}, {'k': 'Section 6', 'v': 'Minimum 2 partners; 6-month rule'},
                     {'k': 'Section 7', 'v': '2 designated partners (individuals), 1 resident — 120 days'}, {'k': 'Section 11', 'v': 'Incorporation document; compliance statement; false statement penalty'},
                     {'k': 'Section 12', 'v': 'Registration within 14 days; certificate conclusive'}, {'k': 'Section 13', 'v': 'Registered office; ₹500/day up to ₹50,000'},
                     {'k': 'Section 14', 'v': 'Effects of registration'}, {'k': 'Sections 15 / 16 / 17', 'v': 'Name ends with LLP; reservation 3 months; change of name (3 months, 3 years, 15 days, 30 days)'}],
        'viva': [
            V('v1', 'What is a Limited Liability Partnership?',
              'An LLP is a body corporate formed and registered under the LLP Act, 2008. It is a separate legal entity with perpetual succession; the LLP answers for its debts with all its assets, while each partner\'s liability is limited to his agreed contribution. It combines the limited liability of a company with the flexibility of a partnership, so it is called a hybrid.',
              [P('p1', 'Body corporate / separate legal entity', 3, 'body corporate|separate legal|separate entity|legal entity|legal person|artificial person'),
               P('p2', 'Partners\' liability limited to agreed contribution', 4, 'limited liability|liability limited|limited to|limit liability|liability is limited|liability of partners is limited|limited', 'contribution|agreed|extent|capital', min=1),
               P('p3', 'Hybrid of company and partnership / perpetual succession', 3, 'hybrid|company and partnership|company and a partnership|both company|perpetual|flexibility')], 'c1'),
            V('v2', 'What is the minimum number of partners in an LLP, and what happens if it falls below that number?',
              'Every LLP must have at least two partners. If it is left with a single partner and keeps doing business like that beyond six months, that lone partner, if he knows he is carrying on alone, becomes personally liable for the obligations incurred after those six months.',
              [P('p1', 'At least two partners (Section 6)', 3, 'two|2|section 6'),
               P('p2', 'Business continues for more than six months', 3, 'six month|6 month|half year'),
               P('p3', 'Sole partner personally liable for obligations after that period (with knowledge)', 4, 'personally liable|personal liability|personally responsible|liable personally|personally bound|own pocket|personal assets')], 'c3'),
            V('v3', 'What are the requirements regarding designated partners in an LLP?',
              'Each LLP needs a minimum of two designated partners, all of them individuals, with one or more resident in India; a resident here is someone who has stayed in India for at least 120 days in the financial year. If partners are bodies corporate, their individual nominees can act as designated partners.',
              [P('p1', 'At least two designated partners', 3, 'two|2', 'designated', min=2),
               P('p2', 'Must be individuals (or nominees of bodies corporate)', 2, 'individual|natural person|nominee|human'),
               P('p3', 'At least one resident in India', 3, 'resident|reside|living in india|lives in india'),
               P('p4', 'Resident = stayed 120 days in the financial year', 2, '120')], 'c3'),
            V('v4', 'Which individuals cannot become partners of an LLP?',
              'Under Section 5, an individual cannot be a partner if a competent court has found him to be of unsound mind and the finding is in force, if he is an undischarged insolvent, or if he has applied to be adjudicated insolvent and his application is pending.',
              [P('p1', 'Found of unsound mind by a court', 4, 'unsound|insane|mental|lunatic|' + ALT('{n} {x}', n=('not', 'no', 'nor', 'neither'), x=('unsound', 'insane', 'mental', 'lunatic'))),
               P('p2', 'Undischarged insolvent', 3, 'undischarged|not discharged|insolvent|bankrupt|' + ALT('{n} {x}', n=('not', 'no', 'nor', 'neither'), x=('undischarged', 'insolvent', 'bankrupt'))),
               P('p3', 'Insolvency application pending', 3, 'pending|applied|application')], 'c3'),
            V('v5', 'What are the requirements for incorporating an LLP under Section 11?',
              'Two or more persons running a lawful business to earn profit must subscribe their names to an incorporation document and file it with the Registrar of the State where the registered office is to be, with the fee. A statement of compliance by an advocate, company secretary, chartered accountant or cost accountant engaged in the formation, and by one subscriber, must be filed with it.',
              [P('p1', 'Two or more persons', 2, 'two or more|2 or more|at least two|at least 2|minimum two|minimum 2'),
               P('p2', 'Lawful business with a view to profit', 3, 'profit'),
               P('p3', 'Incorporation document filed with the Registrar', 3, 'incorporation document|document|registrar|file|filed'),
               P('p4', 'Compliance statement by a professional and a subscriber', 2, 'statement|advocate|chartered accountant|company secretary|cost accountant|professional|certif')], 'c5'),
            V('v6', 'How does an LLP differ from a partnership firm?',
              'An LLP is a body corporate and separate legal entity, while a firm is not. Registration is compulsory for an LLP but optional for a firm. An LLP has perpetual succession; a firm does not. The liability of LLP partners is limited, while firm partners have unlimited liability. And an LLP partner is an agent only of the LLP, not of the other partners.',
              [P('p1', 'LLP separate legal entity; firm is not', 2, 'separate|body corporate|legal entity|legal person'),
               P('p2', 'Registration compulsory for LLP; optional for a firm', 2, 'compulsory firm optional|compulsory firm voluntary|mandatory firm optional|mandatory firm voluntary|compulsory llp optional firm|mandatory llp optional firm|compulsory llp voluntary firm|mandatory llp voluntary firm|firm optional llp compulsory|firm voluntary llp compulsory|firm optional llp mandatory|firm voluntary llp mandatory'),
               P('p3', 'LLP limited liability; firm unlimited', 4, 'limit firm unlimit|limit firm partner unlimit|limited whereas firm unlimited|firm unlimit llp limit|firm partner unlimit llp partner limit|firm partner unlimit llp limit'),
               P('p4', 'Perpetual succession / mutual agency differences', 2, 'perpetual|succession|agent|agency')], 'c7'),
            V('v7', 'What are the rules regarding the name of an LLP?',
              'Under Section 15 the name must end with the words limited liability partnership or LLP, and it must not be undesirable or identical with or too similar to another LLP, a company or a registered trade mark. Under Section 16 a name can be reserved for three months.',
              [P('p1', 'Must end with "Limited Liability Partnership" or "LLP"', 4, 'end|last word|suffix|ends', 'llp|limited liability partnership', min=2),
               P('p2', 'Not undesirable or similar to another LLP / company / trade mark', 3, 'undesirable|identical|similar|resembl|trade mark|trademark'),
               P('p3', 'Reservation for three months (Section 16)', 3, 'three month|3 month|reserv')], 'c6'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Kaveri Design Studio LLP', 'difficulty': 'hard',
            'case': ('Four architects — Kunal and Lavanya (living in India), and Mihir and Neeraj (living in Singapore, each spending about 90 days a year in India) — incorporate "Kaveri Design Studio LLP" on 5 January 2026 with Kunal and Mihir as designated partners. In 2026 the LLP moves its registered office but files the notice of change only after 150 days. Later, a client sues the LLP for a design defect caused solely by Neeraj\'s negligence, claiming more than the LLP\'s assets.'),
            'mcqs': [
                dict(M('k1a', 'Is the choice of Kunal and Mihir as designated partners valid?', ['Yes — two individuals, and Kunal is resident in India', 'No — both must be resident', 'No — Mihir stays less than 182 days', 'No — designated partners must be bodies corporate'], 0,
                  'Section 7 needs at least two designated partners who are individuals, with at least one resident in India (120 days in the financial year). Kunal lives in India and is resident, and Mihir is an individual, so the pair is valid. "Mihir stays less than 182 days" is the trap: 182 days is an income-tax test, and only one designated partner needs to be resident anyway. Designated partners need not be bodies corporate. In practice: LLPs with foreign partners usually appoint at least one India-based designated partner to handle filings.', 'moderate'), topic='Partners, minimum number and designated partners (Sections 5–7)'),
                dict(M('k1b', 'What is the computed penalty (before applying the cap) for 150 days of default under Section 13?', [R(k_pen), '₹50,000', '₹15,000', '₹7,500'], 0,
                  'Under Section 13, the penalty is ₹500 for each day of default. For 150 days: ₹500 × 150 = ₹75,000 before applying the cap. ₹50,000 is the trap: it is the maximum actually payable, not the computed figure the question asks for. ₹7,500 and ₹15,000 come from wrong daily rates. In practice: when a client files late, the CA first works out the daily penalty, then compares it with the cap, to show the client what is actually payable.', 'moderate', '500*150'), topic='Incorporation, registered office and effect of registration (Sections 11–14)'),
                dict(M('k1c', 'What is the maximum penalty payable by Lavanya personally for that default?', ['₹50,000', '₹75,000', '₹500', 'Nil — only designated partners are liable'], 0,
                  'Section 13 makes the LLP and every partner separately liable, each subject to a maximum of ₹50,000. The computed amount of ₹75,000 exceeds the cap, so Lavanya personally pays at most ₹50,000. ₹75,000 is the trap: it ignores the cap. "Nil, as only designated partners are liable" is also wrong: this section covers every partner, not just designated ones. In practice: partners who are not designated sometimes assume compliance penalties do not touch them, and a CA must correct that belief.', 'hard', '50000'), topic='Incorporation, registered office and effect of registration (Sections 11–14)'),
                dict(M('k1d', 'Can the client recover the excess over the LLP\'s assets from Kunal personally?', ['No — a partner is not liable for another partner\'s independent wrongful act; liability is limited to contribution', 'Yes — all partners are jointly liable as in a firm', 'Yes — because Kunal is a designated partner', 'Yes — but only up to ₹50,000'], 0,
                  'In an LLP, each partner is an agent of the LLP but not of the other partners (Section 26), and Section 28(2) says a partner is not personally liable for another partner\'s wrongful act. Kunal did nothing wrong, so the client cannot reach his personal assets. Neeraj stays liable for his own negligence. "All partners are jointly liable as in a firm" is the trap: that is the rule for a general partnership, which the LLP replaces. In practice: professional LLPs also buy indemnity insurance to cover such claims.', 'hard'), topic='Characteristics of an LLP'),
            ]}],
    }


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
    'q1': {'extra_ok': False,
           's1': _k('partner designated|2 1 j|2(1)(j)|designated under section 7|designated as a designated partner|designated in the incorporation document|named as designated'),
           's2': _k('minimum of two designated|minimum two designated|at least two designated|least two designated|two individuals as designated|designated partners who are individuals|two individuals as designated partners', 'at least one resident|one resident|one must be resident|one shall be resident|at least one of them|one or more resident|least one of them must be resident'),
           's3': _k('body corporate|bodies corporate', 'nominee|nominees'),
           's4': _k('120 days|120', 'compulsory|mandatory|obligatory|yes|must appoint|required to appoint'),
           },
    'q2': {'extra_ok': False,
           's1': _k('section 11|lawful business|business with a view|carry on a lawful business|carrying on lawful business|carrying on a lawful business|carry on lawful business|business for profit', 'profit'),
           's2': _k('cannot be formed|cannot be incorporated|not be formed|not possible|cannot be registered|cannot form|not permitted|cannot incorporate|not be incorporated|cannot be set up|not allowed|not valid|cannot be created'),
           's3': _k('section 7', 'two|2|minimum', 'individual|individuals', 'resident', n=3),
           's4': _k('no resident|neither is resident|both non resident|both are non-residents|non resident|non-resident|not resident|non residents',
                    'cannot both|not both|cannot be the only|at least one|one of r s t|one of ms r|ms r|ms s|ms t|one resident|must include|cannot alone|not alone|alone cannot|cannot be sole|not sufficient|not enough|one of the residents'),
           },
    'q3': {'extra_ok': True,
           's1': _k('body corporate|separate legal entity|separate legal|legal entity|separate entity', 'not a body corporate|no separate|not separate|not a separate|not a legal entity|not body corporate'),
           's2': _k('registration compulsory|compulsory registration|registration is compulsory|created by registration|registration mandatory|mandatory registration|incorporation|registration is mandatory', 'optional|not compulsory|not mandatory|agreement'),
           's3': _k('perpetual succession|perpetual', 'dissolve|dissolution|reconstitut|no perpetual|not perpetual|affected|death'),
           's4': _k('contribution|liability is limited|liability limited|limited to the agreed|limited to their contribution|limited to agreed', 'unlimited|personal assets|personal property'),
           's5': _k('agent of the llp|agent of llp|not of other partners|llp only|not agent of other partners|only agent of the llp', 'agent of the firm and|agent of other partners|agent of the other partners|agent of firm and|other partners'),
           's6': _k('name|designated partner|annual return|statement of account|solvency|foreign|minor|filing|llp act 2008|partnership act 1932|governing law'),
           },
    'q4': {'extra_ok': False,
           's1': _k('sue and be sued|suing and being sued|sue|sued', 'property|acquire|own|hold', 'common seal|seal', 'body corporate|anything|other acts|lawfully do', n=3),
           's2': _k('unsound mind', 'undischarged insolvent|undischarged', 'applied|application pending|pending|applied to be adjudicated'),
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
