"""CA Intermediate · Paper 2 Corporate and Other Laws · Chapter 1 Preliminary (Companies Act, 2013 — sections 1 and 2).
Scope follows the ICAI study material; statutory definitions are explained in original words; examples are original."""
from ikit import *

UID = 'int-p2-ch01-u01'
T1 = 'The Companies Act, 2013 and its application'
T2 = 'Kinds of companies by liability and ownership'
T3 = 'Small company and One Person Company'
T4 = 'Holding, subsidiary and associate companies'
T5 = 'Government company and listed company'
T6 = 'Capital terms and net worth'
T7 = 'Financial statements and financial year'
T8 = 'Managerial terms: KMP, MD, manager, officer in default'
T9 = 'Related party and relative'
T10 = 'Other key definitions'


def build():
    app = table(['Applies to', 'Condition'], [
        ['Companies formed under this Act or any earlier company law', 'Fully'],
        ['Insurance companies', 'Except where inconsistent with the Insurance Act, 1938 or the IRDA Act, 1999'],
        ['Banking companies', 'Except where inconsistent with the Banking Regulation Act, 1949'],
        ['Electricity generation or supply companies', 'Except where inconsistent with the Electricity Act, 2003'],
        ['Companies governed by any other special Act', 'Except where inconsistent with that Act'],
        ['Bodies corporate under other Acts notified by the Central Government', 'With notified exceptions and modifications'],
    ], title='Section 1 — application of the Act')
    pvt = table(['Feature', 'Private company (s. 2(68))', 'Public company (s. 2(71))'], [
        ['Transfer of shares', 'Articles restrict transfer', 'Freely transferable'],
        ['Members', 'Up to 200 (OPC: one); joint holders count as one; current and certain former employee-members excluded', 'No upper limit'],
        ['Invitation to public', 'Prohibited', 'Allowed'],
        ['Minimum paid-up capital', 'None prescribed at present', 'None prescribed at present'],
        ['Special rule', '—', 'A subsidiary of a public company is deemed public even if its articles say private'],
    ], title='Private vs public company')
    small = table(['Test', 'Limit (current rules)'], [
        ['Paid-up share capital', 'Not more than ₹10 crore'],
        ['Turnover of the immediately preceding financial year', 'Not more than ₹100 crore'],
        ['Must not be', 'A public company, a holding or subsidiary company, a section 8 company, or one governed by a special Act'],
    ], title='Small company — s. 2(85) read with the definition rules')
    kmp = table(['Key managerial personnel (s. 2(51))'], [
        ['CEO, or managing director, or manager'], ['Company secretary'], ['Whole-time director'], ['Chief Financial Officer'],
        ['Any other whole-time officer not more than one level below the directors, designated as KMP by the Board'], ['Any other officer prescribed (none so far)']], title='KMP')
    rel = table(['Relatives of a person (s. 2(77) and the rules)'], [
        ['Members of the same HUF; husband and wife'], ['Father (incl. step-father) and mother (incl. step-mother)'], ['Son (incl. step-son) and son\'s wife'],
        ['Daughter and daughter\'s husband'], ['Brother (incl. step-brother) and sister (incl. step-sister)']], title='Relatives')

    illus = [
        {'id': 'i1', 'title': 'Is it a small company?', 'difficulty': 'core', 'minutes': 6,
         'q': 'Decide whether each is a small company: (a) Kosi Pvt. Ltd., paid-up capital ₹6 crore, last year\'s turnover ₹85 crore, no group links; (b) Mahi Pvt. Ltd., capital ₹9 crore, turnover ₹130 crore; (c) Tawa Pvt. Ltd., capital ₹2 crore, turnover ₹20 crore, a subsidiary of Kosi Pvt. Ltd.; (d) Seva Foundation, a section 8 private company, capital ₹1 crore, turnover ₹5 crore; (e) Bhima Ltd., a public company, capital ₹3 crore, turnover ₹30 crore.',
         'solution': [table(['Company', 'Result', 'Reason'], [
             ['(a) Kosi Pvt. Ltd.', 'Small company', 'Both limits met (₹10 crore capital, ₹100 crore turnover) and no exclusion applies'],
             ['(b) Mahi Pvt. Ltd.', 'Not small', 'Turnover exceeds ₹100 crore — both tests must be satisfied'],
             ['(c) Tawa Pvt. Ltd.', 'Not small', 'Subsidiary companies are excluded'],
             ['(d) Seva Foundation', 'Not small', 'Section 8 companies are excluded'],
             ['(e) Bhima Ltd.', 'Not small', 'A public company can never be a small company']], title='Answer'),
             note('Kosi Pvt. Ltd. also loses small-company status once it becomes the holding company of Tawa.')]},
        {'id': 'i2', 'title': 'Group relationships and government company', 'difficulty': 'moderate', 'minutes': 7,
         'q': '(a) Alpha Ltd. holds 45% of the votes in Beta Ltd. but can appoint 4 of Beta\'s 7 directors. (b) Alpha holds 23% of Gamma Ltd.\'s votes and has no board control. (c) Delta Ltd. is owned 30% by the Central Government, 15% by the Gujarat government and 10% by a Central Government–Gujarat joint holding. (d) Omega Pvt. Ltd. is a wholly owned subsidiary of Alpha Ltd. and wants private-company exemptions. Classify each.',
         'solution': [table(['Case', 'Conclusion', 'Basis'], [
             ['(a) Beta Ltd.', 'Subsidiary of Alpha', 'Controls the composition of the Board (can appoint a majority) — voting power below half does not matter'],
             ['(b) Gamma Ltd.', 'Associate of Alpha', 'At least 20% voting power gives significant influence; not a subsidiary'],
             ['(c) Delta Ltd.', 'Government company', 'Government holdings total 55% (30 + 15 + 10) — at least 51% of paid-up capital'],
             ['(d) Omega Pvt. Ltd.', 'Deemed public company', 'A subsidiary of a non-private company is treated as public; private-company exemptions are not available']], title='Answer')]},
    ]

    concepts = [
        C('c1', T1, [
            'The Companies Act, 2013 consolidates and amends company law to modernise regulation, improve governance and protect investors. It received Presidential assent on 29 August 2013 and its provisions were brought into force in stages by notification (section 1 itself from 30 August 2013). It has 470 sections and seven Schedules in 29 chapters, backed by Rules.',
            'Section 1 gives the short title, extends the Act to the whole of India, and provides for commencement of different provisions on different notified dates.',
            'Application (table): companies formed under this or earlier law apply it fully; insurance, banking, electricity and special-Act companies apply it except where it conflicts with their own Act; notified statutory corporations apply it with modifications. Where the two conflict, the special Act prevails.',
            'Section 2 is the definition clause — an internal aid to interpretation; a defined meaning must be applied unless the context requires otherwise. Words not defined here but defined in the SCRA, 1956, SEBI Act, 1992 or Depositories Act, 1996 take those meanings (s. 2(95)).'],
          'The Companies Act is the general rulebook; special Acts for banks or insurers are house rules that win wherever they clash.',
          'A bank formed as a company follows the Banking Regulation Act on, say, accounts formats, and the Companies Act on matters that Act does not cover.',
          blocks=[app]),
        C('c2', T2, [
            'By liability: a company limited by shares — members liable only for any unpaid amount on their shares (s. 2(22)); limited by guarantee — liable up to the amount they undertake to contribute on winding up (s. 2(21)); unlimited — no limit on members\' liability (s. 2(92)).',
            'A contributory is anyone liable to contribute to assets on winding up; a holder of fully paid shares is also treated as a contributory (s. 2(26)).',
            'Private company (s. 2(68)): articles restrict transfer of shares, cap members at 200 (except OPC) and bar any public invitation to subscribe for securities. Joint holders count as one member; present employees and former employees who became members while employed are not counted. No minimum paid-up capital is prescribed now.',
            'Public company (s. 2(71)): one that is not private. A subsidiary of a company that is not private is deemed public even if its articles are those of a private company.'],
          'A private company is a members-only club with a guest limit and a closed door; a public company is an open stadium.',
          'Many Indian subsidiaries of listed groups carry "Pvt. Ltd." in their name but are treated as public companies for compliance.',
          blocks=[pvt]),
        C('c3', T3, [
            'Small company (s. 2(85)): a non-public company whose paid-up capital and previous-year turnover are both within prescribed limits — currently ₹10 crore and ₹100 crore (the Act allows the rules to set these within ceilings of ₹10 crore and ₹100 crore).',
            'Excluded even if within limits: holding or subsidiary companies, section 8 companies, and companies or bodies corporate governed by a special Act.',
            'One Person Company (s. 2(62)): a company with only one member. OPCs and small companies get several relaxations (e.g. cash flow statement not mandatory).'],
          'Small-company status is a lighter backpack for genuinely small, standalone private companies — not for members of a group.',
          'Founders often start as an OPC or small private company to keep compliance light in early years.',
          blocks=[small]),
        C('c4', T4, [
            'Subsidiary (s. 2(87)): Company S is a subsidiary of H if H controls the composition of S\'s board (can appoint or remove all or most directors at its discretion) or exercises or controls more than half of the total voting power, alone or with its other subsidiaries. Control through another subsidiary also counts; "company" includes any body corporate. Holding company (s. 2(46)) is the mirror term.',
            'Prescribed classes of holding companies cannot have subsidiaries beyond the permitted number of layers.',
            'Associate company (s. 2(6)): a company over which another has significant influence but which is not its subsidiary, including a joint venture company. Significant influence means holding at least 20% of the total votes, or having an agreement that lets it control or take part in business decisions.',
            'Shares held in a fiduciary capacity are ignored when testing subsidiary or associate relationships. The Companies Act meaning of "associate" differs from that in the accounting standards.',
            'Control (s. 2(27)) is an inclusive term: the right to appoint a majority of directors or to control management or policy decisions, directly or indirectly, by shareholding, management rights or agreements.'],
          'A holding company is the driver who controls the car (board or majority votes); an associate is a passenger with a strong say in the route (20% influence).',
          'Group structures are mapped each year to identify subsidiaries for consolidation and related-party disclosures.'),
        C('c5', T5, [
            'Government company (s. 2(45)): at least 51% of the paid-up capital is owned by the Central Government, any State Government(s), or jointly by the Centre and one or more States; its subsidiaries are also government companies. Where shares with differential voting rights exist, "paid-up share capital" is read as total voting power.',
            'Listed company (s. 2(52)): has any of its securities listed on a recognised stock exchange. Under the definition rules, some companies are not treated as listed — e.g. public companies that list only privately placed non-convertible debt securities or non-convertible redeemable preference shares (without listing equity), private companies listing only privately placed non-convertible debt, and public companies whose equity is listed only on a permitted foreign exchange.'],
          'Government company status is about who owns the majority stake — the State, not the name on the door.',
          'Public sector undertakings such as oil and power companies are government companies; their subsidiaries are too.'),
        C('c6', T6, [
            'Authorised (nominal) capital: the maximum share capital allowed by the memorandum. Issued capital: offered for subscription. Subscribed capital: taken up by members. Called-up capital: the part called for payment. Paid-up capital: amounts received or credited as paid-up on shares issued — excluding any other amount (such as premium).',
            'Free reserves (s. 2(43)): reserves available for dividend as per the latest audited balance sheet — excluding unrealised or notional gains, revaluation, and fair-value changes recognised in equity.',
            'Net worth (s. 2(57)): paid-up capital + reserves created out of profits + securities premium ± profit and loss balance, minus accumulated losses and any deferred or miscellaneous expenditure still to be written off, taken from the audited balance sheet — leaving out reserves arising from asset revaluation, from writing back depreciation, or on amalgamation.',
            'Share includes stock (s. 2(84)); debenture includes debenture stock, bonds and any instrument evidencing debt, secured or not, except certain RBI-regulated money market instruments and others prescribed (s. 2(30)). Sweat equity shares are issued to directors or employees at a discount or for non-cash consideration for know-how, IPR or value additions (s. 2(88)).'],
          'Capital terms are like a ladder: authorised (permission) ≥ issued (offered) ≥ subscribed (taken) ≥ called-up (asked) ≥ paid-up (received).',
          'Net worth matters for thresholds like CSR, Ind AS applicability and auditor certificates — revaluation gains must be removed.'),
        C('c7', T7, [
            'Financial statement (s. 2(40)) includes the balance sheet, profit and loss account (income and expenditure account for not-for-profit companies), cash flow statement, statement of changes in equity if applicable, and explanatory notes. A cash flow statement is optional for OPCs, small companies, dormant companies and private companies that are recognised start-ups (if not in default of filings).',
            'Financial year (s. 2(41)): the period ending 31 March each year. A company incorporated on or after 1 January closes its first financial year on 31 March of the following year (so it can be up to about 15 months). A holding, subsidiary or associate of a foreign company needing a different year for consolidation abroad may apply to the Central Government to adopt another period.',
            'Books of account (s. 2(13)) record receipts and payments, sales and purchases of goods and services, and assets and liabilities, plus cost items for companies covered by section 148. Book and paper include records kept on paper or electronically (s. 2(12)).',
            'Turnover (s. 2(91)): gross revenue recognised in the profit and loss account from sale, supply or distribution of goods or services during the financial year.'],
          'The financial year is the company\'s school year — always ending in March, with late joiners after 1 January getting a longer first year.',
          'A company incorporated on 10 February 2026 prepares its first accounts up to 31 March 2027.'),
        C('c8', T8, [
            'Key managerial personnel (table).',
            'Managing director (s. 2(54)): a director entrusted with substantial powers of management by the articles, an agreement, a general-meeting resolution or the Board. Routine administrative powers (affixing the seal, signing cheques, share certificates, registering transfers) are not "substantial powers". Only a director can be an MD.',
            'Manager (s. 2(53)): an individual who, under the Board\'s superintendence, manages the whole or substantially the whole of the company\'s affairs. Whole-time director includes a director in the company\'s whole-time employment.',
            'Officer (s. 2(59)) includes directors, managers, KMP and anyone on whose instructions the Board is accustomed to act.',
            'Officer who is in default (s. 2(60)) includes: whole-time directors; KMP; where there is no KMP, directors specified by the Board (with consent), or all directors if none is specified; persons charged under the Board or KMP with maintaining or filing records who participate in, permit or fail to prevent the default; persons on whose advice the Board acts (other than professional advisers); every director aware of the contravention through Board proceedings without objecting, or who consented or connived; and share transfer agents, registrars and merchant bankers in respect of issue or transfer of shares.'],
          '"Officer in default" decides whose name goes on the charge sheet when the company breaks the law.',
          'Where a company has no KMP and the Board has named no director, all directors may be treated as officers in default.',
          blocks=[kmp]),
        C('c9', T9, [
            'Related party (s. 2(76)) of a company includes: a director or KMP or their relatives; a firm in which a director, manager or relative is a partner; a private company in which a director, manager or relative is a member or director; a public company on whose board a director or manager of this company sits and where he, together with relatives, owns over 2% of the paid-up capital; bodies corporate whose board or MD acts on a director\'s or manager\'s advice, and persons on whose advice a director or manager acts (professional advice excepted); holding, subsidiary or associate companies, fellow subsidiaries, and investing companies or venturers; and a director (other than an independent director) or KMP of the holding company, or their relative (by rule).',
            'For section 188 (related party transactions), the holding/subsidiary/associate limb does not apply to private companies — but other limbs (e.g. common directors) may still make them related.',
            'Relative (s. 2(77)): members of the same HUF, husband and wife, and those listed in the rules (table) — the list does not include, for example, a brother\'s wife or grandparents.'],
          'Related parties are the people close enough to the company to tempt it into deals that are not at arm\'s length.',
          'Audit committees approve related party contracts such as leasing property from a director\'s relative.',
          blocks=[rel]),
        C('c10', T10, [
            'Articles and memorandum include the original documents as altered; alteration includes additions, omissions and substitutions.',
            'Accounting standards are those prescribed under section 133 (Central Government, after examining NFRA\'s recommendations) — either the Accounting Standards Rules notified in 2021 or, for companies covered by the roadmap, the Ind AS Rules of 2015. Auditing standards are under section 143(10).',
            'Body corporate includes a company incorporated outside India but excludes co-operative societies and other notified bodies. Chartered accountant means a CA holding a certificate of practice. Expert includes an engineer, valuer, CA, CS, cost accountant and others empowered to certify under law.',
            'Charge: an interest or lien on property or assets as security, including a mortgage. Promoter: named as such in a prospectus or annual return, or in control of affairs, or on whose instructions the Board acts (not a mere professional adviser).',
            'Prospectus includes red herring and shelf prospectuses and any document inviting public offers for securities. Employees\' stock option: a right for directors, officers or employees (of the company, its holding or subsidiary) to buy shares later at a set price. Remuneration includes perquisites under the Income-tax Act. Tribunal means the NCLT. Postal ballot includes electronic voting.'],
          'Definitions are the dictionary at the front of the rulebook — check them before applying any section.',
          'Whether a person is a "promoter" affects prospectus liability and disclosures in an IPO.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Checking small-company eligibility', 'role': 'Company secretary trainee',
         'situation': 'A client private company wants to file accounts without a cash flow statement.',
         'steps': ['Check paid-up capital (≤ ₹10 crore) and last year\'s turnover (≤ ₹100 crore).', 'Confirm it is not a holding, subsidiary, section 8 or special-Act company.', 'If eligible, apply the small-company relaxations; otherwise prepare full statements.'],
         'takeaway': 'Both numeric tests and all exclusions must be checked together.'},
        {'id': 'j2', 'title': 'Mapping related parties', 'role': 'Audit assistant',
         'situation': 'A director\'s son-in-law\'s firm supplies goods to the company.',
         'steps': ['Daughter\'s husband is a "relative" under the rules.', 'A firm in which a director\'s relative is a partner is a related party.', 'Check whether the contract needed Board or shareholder approval under section 188.'],
         'takeaway': 'Apply the relative list exactly; it is narrower than everyday family.'},
    ]

    mcqs = [
        Q('m1', 'Narmada Ltd. was incorporated on 3 February 2026. Its first financial year will end on:', ['31 March 2027', '31 March 2026', '31 December 2026', '2 February 2027'], 0,
          'Under section 2(41), a company incorporated on or after 1 January closes its first financial year on 31 March of the following year, so the year ends on 31 March 2027. Ending on 31 March 2026 would apply only to incorporation before 1 January. In practice: this gives about 14 months for the first accounts.', 'c7', T7),
        Q('m2', 'A public company with paid-up capital of ₹5 crore and turnover of ₹40 crore:', ['Cannot be a small company because it is public', 'Is a small company', 'Becomes small after two years', 'Is small if members agree'], 0,
          'Section 2(85) defines a small company as one other than a public company, so a public company cannot qualify whatever its size. Meeting the numeric limits is not enough. In practice: the company would have to convert to private to seek small-company status.', 'c3', T3),
        Q('m3', 'Which of the following can never be a small company?', ['A company registered under section 8', 'A private company with capital ₹2 crore and turnover ₹15 crore and no group links', 'An OPC with capital ₹1 lakh', 'A private company with turnover ₹99 crore and capital ₹9 crore'], 0,
          'Section 8 companies, holding or subsidiary companies and special-Act companies are excluded from the definition even if within limits. The other options satisfy both numeric tests without any exclusion. In practice: charitable section 8 companies get separate relaxations instead.', 'c3', T3),
        Q('m4', '"Significant influence" for an associate company means control of at least:', ['20% of total voting power, or participation in business decisions under an agreement', '10% of share capital', '26% of share capital', 'More than 50% of voting power'], 0,
          'Under section 2(6), significant influence means controlling at least 20% of total voting power or controlling or participating in business decisions under an agreement. More than 50% voting power indicates a subsidiary instead. In practice: a 22% stake with board representation usually creates an associate.', 'c4', T4),
        Q('m5', 'X Ltd. holds 40% of the votes in Y Ltd. but can appoint a majority of its directors. Y Ltd. is X Ltd.\'s:', ['Subsidiary', 'Associate', 'Joint venture only', 'Unrelated company'], 0,
          'A company is a subsidiary if the holding company controls the composition of its board or more than half its voting power; either test is enough. Board control alone makes Y a subsidiary despite 40% votes. In practice: shareholder agreements granting board-appointment rights create subsidiaries.', 'c4', T4, 'moderate'),
        Q('m6', 'XYZ Ltd. is held 51% by the Central Government, 10% by a State Government, 15% by X Ltd. and 24% by the public. It is a:', ['Government company', 'Private company', 'Associate company of X Ltd. only', 'Dormant company'], 0,
          'Government holdings total 61%, above the 51% threshold in section 2(45), so XYZ Ltd. is a government company. X Ltd. with 15% has no significant influence on that basis. In practice: government companies have special audit arrangements through the C&AG.', 'c5', T5),
        Q('m7', 'A private company that is a subsidiary of a public company is:', ['Deemed to be a public company', 'Always a small company', 'Free to use all private-company exemptions', 'A government company'], 0,
          'The proviso to section 2(71) treats a subsidiary of a company that is not private as a public company even if its articles are those of a private company. So it cannot claim private-company exemptions. In practice: group subsidiaries must check their parent\'s status.', 'c2', T2),
        Q('m8', 'For counting the 200-member limit of a private company, which are excluded?', ['Present employees and former employees who became members while employed', 'Directors\' relatives', 'Joint holders counted separately', 'Corporate shareholders'], 0,
          'Section 2(68) excludes present employees and former employees who were members while employed and continued afterwards; joint holders count as one member. Directors\' relatives and corporate members are counted. In practice: this lets employee-shareholders hold shares without breaching the limit.', 'c2', T2, 'moderate'),
        Q('m9', 'Which of these is NOT included in net worth under section 2(57)?', ['Revaluation reserve', 'Securities premium', 'Paid-up share capital', 'General reserve created out of profits'], 0,
          'Net worth includes paid-up capital, reserves from profits and securities premium, but leaves out reserves arising from asset revaluation, from writing back depreciation, or on amalgamation. So a revaluation reserve is excluded even if shown within retained earnings. In practice: CSR and Ind AS thresholds use this net worth.', 'c6', T6),
        Q('m10', 'Which is NOT a key managerial personnel under section 2(51)?', ['An independent director', 'Company secretary', 'Chief Financial Officer', 'Whole-time director'], 0,
          'KMP comprise the CEO/MD/manager, company secretary, whole-time director, CFO, and other designated whole-time officers one level below directors. Independent directors are non-executive and are not KMP. In practice: KMP details are filed with the Registrar.', 'c8', T8),
        Q('m11', 'Signing cheques and affixing the common seal on the Board\'s authority:', ['Are routine powers, not substantial powers of management', 'Make a person a managing director', 'Make a person a manager', 'Make a person a promoter'], 0,
          'The explanation to section 2(54) excludes routine administrative acts such as affixing the seal and signing cheques from substantial powers of management; such powers alone do not make someone a managing director. In practice: MDs are appointed by specific resolution or agreement.', 'c8', T8),
        Q('m12', 'If a company has no KMP and the Board has not specified any director, the officer in default for a contravention is:', ['All the directors', 'Only the chairman', 'The statutory auditor', 'The largest shareholder'], 0,
          'Under section 2(60), where there is no KMP and no director has been specified by the Board, all the directors may be treated as officers in default. Auditors and shareholders are not officers in default on that basis. In practice: Boards designate a responsible director to avoid this.', 'c8', T8, 'moderate'),
        Q('m13', 'Which of these is a "relative" under the Companies Act?', ['Daughter\'s husband', 'Brother\'s wife', 'Grandfather', 'Cousin'], 0,
          'The relative list includes the daughter\'s husband and son\'s wife, along with parents, children and siblings (including step-relations), spouses and HUF members. A brother\'s wife, grandparents and cousins are not listed. In practice: apply the list strictly when identifying related parties.', 'c9', T9),
        Q('m14', 'A public company is a related party if one of our directors sits on its board and, with relatives, owns what share of its paid-up capital?', ['More than 2%', 'More than 10%', 'At least 20%', 'More than 50%'], 0,
          'Section 2(76)(v) treats a public company as a related party where a director or manager of the company is its director and holds, together with relatives, more than 2% of its paid-up capital. In practice: directors disclose their holdings so these relationships can be tracked.', 'c9', T9, 'moderate'),
        Q('m15', 'A cash flow statement is not mandatory for:', ['One person companies, small companies and dormant companies', 'All listed companies', 'Banking companies', 'Government companies'], 0,
          'The proviso to section 2(40) allows OPCs, small companies and dormant companies (and private start-ups, by exemption, if not in default) to omit the cash flow statement. Listed, banking and government companies must include it. In practice: this lightens compliance for small entities.', 'c7', T7),
        Q('m16', 'Where a provision of the Companies Act conflicts with the Banking Regulation Act for a banking company:', ['The Banking Regulation Act prevails', 'The Companies Act prevails', 'Both are ignored', 'The company may choose'], 0,
          'Section 1 applies the Act to banking companies except where inconsistent with the Banking Regulation Act, 1949, so the special Act prevails on conflicting matters. The same approach applies to insurance and electricity companies. In practice: banks follow RBI formats for financial statements.', 'c1', T1),
        Q('m17', 'Under section 2(22), in a company limited by shares, a member\'s liability is limited to:', ['The amount unpaid on shares held', 'The face value of all shares of the company', 'The guarantee amount', 'Nothing at all'], 0,
          'In a company limited by shares, members are liable only for any amount unpaid on their shares; once fully paid, no further liability. A guarantee amount applies to companies limited by guarantee. In practice: a member who paid ₹75 on a ₹100 share can be called for ₹25 more.', 'c2', T2),
    ]

    questions = [
        W('q1', 4, 'Define "small company". Pragati Pvt. Ltd. has paid-up capital ₹8 crore and turnover ₹120 crore; would your answer change if turnover were ₹70 crore?',
          [legal('Section 2(85) read with the Companies (Specification of Definitions Details) Rules, 2014',
                 'Pragati Pvt. Ltd.: paid-up capital ₹8 crore; turnover ₹120 crore (alternatively ₹70 crore).',
                 'A small company is a company other than a public company whose paid-up capital does not exceed ₹10 crore and whose turnover for the preceding year does not exceed ₹100 crore, both tests being required; holding, subsidiary, section 8 and special-Act companies are excluded. With turnover ₹120 crore the turnover test fails. With turnover ₹70 crore both tests are met.',
                 'At ₹120 crore turnover it is not a small company; at ₹70 crore it is a small company, provided it is not a holding or subsidiary company or otherwise excluded.')],
          [S('s1', 'Definition — both limits and exclusions', 1.5, 'concept', '10 crore', '100 crore', 'public|holding|subsidiary|section 8', n=2),
           S('s2', '₹120 crore — not small', 1.25, 'application', '120 crore', 'not a small|cannot|fails'),
           S('s3', '₹70 crore — small (if not excluded)', 1.25, 'application', '70 crore', 'small company|met|satisf')],
          ['Quote both limits and the exclusions.'], ['Thinking one test is enough.'], ['Provision → facts → analysis → conclusion.']),
        W('q2', 4, 'Shanti Ltd., a public company, has 230 members: directors and relatives 50, employees 15, former employees who got shares while employed 10, five couples holding jointly 10, others 145. Can it convert into a private company without reducing members?',
          [legal('Section 2(68) — limit of 200 members for a private company',
                 'Total 230 members including employees, former employees and joint holders.',
                 'Employees (15) and former employees who became members while employed (10) are not counted. Each joint holding counts as one member, so the five couples count as 5, not 10. Countable members = 50 + 5 + 145 = 200.',
                 'Countable members are 200, within the limit, so no reduction is needed; it can convert subject to the conversion procedure and other conditions.')],
          [S('s1', 'Exclude employees and former employees', 1.5, 'application', 'employee', 'exclud|not counted|not be counted|ignored'),
           S('s2', 'Joint holders count as one', 1, 'application', 'joint', 'one|single'),
           S('s3', 'Count 200 and conclude no reduction', 1.5, 'conclusion', '200', 'no reduction|not necessary|not required|can convert', nums=[200])],
          ['Show the count step by step.'], ['Counting each joint holder separately.'], ['Use provision–facts–analysis–conclusion.']),
        W('q3', 4, 'Explain "officer who is in default" under section 2(60).',
          [ul(['Whole-time directors and key managerial personnel.', 'If there is no KMP: directors specified by the Board who have consented, or all directors if none is specified.',
               'Persons responsible under the Board or KMP for maintaining, filing or distributing records who authorise, participate in, knowingly permit or fail to prevent the default.',
               'Persons on whose advice the Board acts, other than professional advisers.', 'Every director aware of the contravention through Board proceedings without objecting, or with whose consent or connivance it occurred.',
               'For issue or transfer of shares: share transfer agents, registrars and merchant bankers.'])],
          [S('s1', 'WTD and KMP', 1, 'concept', 'whole-time|whole time', 'key managerial|kmp', n=1),
           S('s2', 'No KMP — specified or all directors', 1, 'concept', 'all the directors|all directors|specified'),
           S('s3', 'Persons charged with records / advisers', 1, 'concept', 'advice|record|responsib'),
           S('s4', 'Directors aware without objecting; RTAs and merchant bankers', 1, 'concept', 'object|consent|conniv|merchant|registrar|transfer agent', n=1)],
          ['List each category in one line.'], ['Including professional advisers.'], ['Bulleted list.']),
    ]

    viva = [
        V('v1', 'When is a company a subsidiary of another?',
          'When the holding company controls the composition of its Board of Directors or exercises or controls more than half of its total voting power, either alone or with its other subsidiaries.',
          [P('p1', 'Controls composition of Board', 5, 'board', 'composition|appoint|control'), P('p2', 'More than half of voting power', 5, 'half|50|majority', 'voting')], 'c4'),
        V('v2', 'What are the current limits for a small company?',
          'Paid up share capital of up to ten crore rupees and turnover of the preceding year of up to one hundred crore rupees, and it must not be a public, holding, subsidiary, section 8 or special Act company.',
          [P('p1', 'Capital up to ₹10 crore', 3, '10 crore'), P('p2', 'Turnover up to ₹100 crore', 3, '100 crore'), P('p3', 'Exclusions', 4, 'public|holding|subsidiary|section 8')], 'c3'),
        V('v3', 'What is excluded from net worth?',
          'Reserves arising from revaluing assets, from writing back depreciation and on amalgamation are left out, and accumulated losses, deferred and miscellaneous expenditure not written off are deducted.',
          [P('p1', 'Revaluation, write-back of depreciation, amalgamation reserves', 6, 'revaluation'), P('p2', 'Losses and deferred expenditure deducted', 4, 'loss|deferred|miscellaneous')], 'c6'),
        V('v4', 'Who are key managerial personnel?',
          'The CEO or managing director or manager, the company secretary, the whole-time director, the CFO, and any other whole-time officer one level below directors designated by the Board.',
          [P('p1', 'CEO/MD/manager', 2, 'ceo|managing director|manager'), P('p2', 'Company secretary', 2, 'secretary'), P('p3', 'Whole-time director', 2, 'whole-time|whole time'), P('p4', 'CFO', 2, 'cfo|chief financial'), P('p5', 'Designated officer', 2, 'designat|one level')], 'c8'),
        V('v5', 'Define a government company.',
          'At least fifty one percent of its paid up capital must be owned by the Central Government, one or more State Governments, or the two together; a subsidiary of such a company also counts.',
          [P('p1', 'At least 51%', 5, '51|fifty one|fifty-one'), P('p2', 'Central and/or State Governments', 3, 'central|state'), P('p3', 'Includes its subsidiary', 2, 'subsidiar')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Structuring Ruchi Foods', 'difficulty': 'moderate',
              'case': 'Ruchi Foods Pvt. Ltd. (capital ₹4 crore, turnover ₹60 crore) plans to buy 60% of Tasty Snacks Pvt. Ltd. and 25% of Spice Route Ltd. Ruchi\'s director\'s brother\'s wife owns a firm that supplies packaging. Ruchi was incorporated on 15 January 2025.',
              'mcqs': [
                  M('k1a', 'After buying 60% of Tasty Snacks, Ruchi Foods:', ['Loses small-company status as it becomes a holding company', 'Remains a small company', 'Becomes a public company', 'Becomes a government company'], 0,
                    'Holding and subsidiary companies are excluded from the small-company definition even if within the capital and turnover limits, so Ruchi loses that status. Tasty Snacks also cannot be a small company as a subsidiary. In practice: acquisitions change compliance status for both companies.', 'moderate', topic=T3),
                  M('k1b', 'With a 25% stake in Spice Route Ltd. and no board control, Spice Route is Ruchi\'s:', ['Associate company', 'Subsidiary', 'Holding company', 'Unrelated company'], 0,
                    'At least 20% of voting power gives significant influence; without board control or majority votes, it is an associate company, not a subsidiary. In practice: associates are related parties of each other under section 2(76).', 'core', topic=T4),
                  M('k1c', 'Is the packaging firm owned by the director\'s brother\'s wife a related party on the "relative" basis?', ['No — a brother\'s wife is not a relative under the rules', 'Yes — all in-laws are relatives', 'Yes — any family member counts', 'Only if she is a director'], 0,
                    'The prescribed list includes brother and sister but not a brother\'s wife, so the firm is not related through the relative test. Other links, such as common control, could still matter. In practice: check the list rather than assuming family ties.', 'moderate', topic=T9),
                  M('k1d', 'Ruchi Foods\' first financial year ended on:', ['31 March 2026', '31 March 2025', '31 December 2025', '14 January 2026'], 0,
                    'Incorporated on 15 January 2025, i.e. on or after 1 January, its first financial year runs to 31 March of the following year, 2026. In practice: this longer first year avoids preparing accounts for a few weeks only.', 'core', topic=T7),
              ]}]

    return unit(UID, 'p2', 'int-p2-ch01', 1, 'Preliminary',
                ['Explain the short title, extent, commencement and application of the Companies Act, 2013.',
                 'Apply key definitions to classify companies — private, public, small, OPC, government, listed, holding, subsidiary and associate.',
                 'Interpret capital-related terms, net worth, free reserves, financial statement and financial year.',
                 'Identify KMP, managing director, manager, officer in default, related parties and relatives.'],
                {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 30}, 'prereq': [],
                 'exam_tip': 'Case questions test small company, subsidiary/associate, government company, financial year and the 200-member count; quote the section number.'},
                concepts, illus, jobs, mcqs, questions,
                {'summary': ['Act applies to all companies; special Acts prevail on conflict for banks, insurers, power and special-Act companies.',
                             'Private: restricts transfer, ≤ 200 members (excl. employees), no public invitation; subsidiary of public = public.',
                             'Small company: non-public, capital ≤ ₹10 cr and turnover ≤ ₹100 cr; not holding/subsidiary/s.8/special Act.',
                             'Subsidiary: board control or > 50% votes; associate: ≥ 20% votes or decision participation.', 'Government company: ≥ 51% held by governments.',
                             'Net worth excludes revaluation, depreciation write-back and amalgamation reserves.', 'FY ends 31 March; incorporation on/after 1 Jan → next 31 March.',
                             'KMP: CEO/MD/manager, CS, WTD, CFO, designated officer.'],
                 'remember': ['Joint holders count as one member.', 'Relative list excludes brother\'s wife and grandparents.'],
                 'traps': ['A public company can never be small.', 'Board control alone makes a subsidiary.']},
                [('Small company', 'Capital ≤ ₹10 cr; turnover ≤ ₹100 cr'), ('Associate', '≥ 20% voting power'), ('Subsidiary', 'Board control or > 50% votes'),
                 ('Government company', '≥ 51% paid-up capital'), ('Private company members', '≤ 200 (excl. employees)')],
                viva, cases,
                topics=['Introduction', 'Short Title, Extent, Commencement and Application', 'Definitions'])
