"""CA Foundation · Paper 2 Business Laws · Chapter 4 The Indian Partnership Act, 1932 · Unit 3 Registration and Dissolution of a Firm.
Original explanations, problems and questions; every figure is computed; sections and leading cases cited by name only."""
from lib import *
from ca_viva import P, ALT, V
from ca_cases import M

UID = 'fnd-p2-ch04-u03'


def SAVED(alts):
    """keyword alternatives plus 'does not affect / bar / take away X' forms, so that a spoken answer such as
    'non-registration does not affect a third party's right' still counts under the negation-aware viva matcher"""
    a = alts.split('|')
    pre = ('not affect', 'not take away', 'not bar', 'not barred', 'not stop', 'not prevent', 'no bar')
    return '|'.join(a + [f'{n} {x}' for n in pre for x in a])


def build():
    # ---------------- Illustration 1: Section 48 order of payment ----------------
    c1 = Checks()
    realised = 880000
    after_cred = c1.add('880000-340000', 'left after paying outside creditors')
    after_loan = c1.add('540000-60000', 'left after repaying Bina\'s loan')
    cap_tot = c1.add('240000+180000+120000', 'total capital')
    defic = c1.add('540000-480000', 'deficiency of capital')
    a_loss = c1.add('60000*3/6', 'Amit bears 3/6')
    b_loss = c1.add('60000*2/6', 'Bina bears 2/6')
    c_loss = c1.add('60000*1/6', 'Chirag bears 1/6')
    a_pay = c1.add('240000-30000', 'Amit receives')
    b_pay = c1.add('180000-20000', 'Bina receives towards capital')
    c_pay = c1.add('120000-10000', 'Chirag receives')
    t1 = table(['Order (Section 48(b))', 'Paid to', 'Amount (₹)'], [
        ['(i) Debts of the firm to third parties', 'Outside creditors', 340000],
        ['(ii) Advances by partners (not capital)', 'Bina — loan', 60000],
        ['(iii) Capital, after charging the deficiency in profit ratio', 'Amit', a_pay],
        ['', 'Bina', b_pay],
        ['', 'Chirag', c_pay],
        ['(iv) Residue in profit ratio', '—', 0],
        ['Total', '', realised],
    ], num=[2], total=True, title='Application of ₹8,80,000 realised')
    t1b = table(['Partner', 'Capital (₹)', 'Share of deficiency 3:2:1 (₹)', 'Paid (₹)'], [
        ['Amit', 240000, a_loss, a_pay], ['Bina', 180000, b_loss, b_pay], ['Chirag', 120000, c_loss, c_pay],
        ['Total', cap_tot, defic, after_loan],
    ], num=[1, 2, 3], total=True, title='Working note: deficiency of capital')

    # ---------------- Illustration 2: Section 49 ----------------
    c2 = Checks()
    firm_short = c2.add('620000-500000', 'firm debts not covered by firm property')
    x_surplus = c2.add('300000-140000', 'Xavier\'s private surplus after his separate debts')
    paid_from_x = c2.add('620000-500000', 'part of Xavier\'s surplus used for firm debts (less than his surplus of 1,60,000)')
    y_ratio = c2.add('80000/100000*100', 'Yamini\'s separate creditors recover (%)')
    t2 = table(['Estate', 'Property (₹)', 'Debts paid first (₹)', 'Surplus / (deficit) (₹)'], [
        ['Firm', 500000, 500000, -firm_short],
        ['Xavier (separate)', 300000, 140000, x_surplus],
        ['Yamini (separate)', 80000, 80000, -20000],
    ], num=[1, 2, 3], title='Section 49 — joint and separate estates')

    # ---------------- Question 3 figures (Section 48) ----------------
    q3c = Checks()
    q3_left1 = q3c.add('1200000-450000', 'after outside creditors')
    q3_left2 = q3c.add('750000-100000', 'after Dev\'s loan')
    q3_cap = q3c.add('300000+200000', 'total capital')
    q3_res = q3c.add('650000-500000', 'residue')
    q3_e = q3c.add('150000*3/5', 'Esha\'s share of residue (3/5)')
    q3_d = q3c.add('150000*2/5', 'Dev\'s share of residue (2/5)')
    q3_et = q3c.add('300000+90000', 'Esha total')
    q3_dt = q3c.add('100000+200000+60000', 'Dev total incl. loan')
    q3t = table(['Order', 'Payee', 'Amount (₹)'], [
        ['(a) Third-party debts', 'Creditors', 450000],
        ['(b) Partner\'s advance', 'Dev — loan', 100000],
        ['(c) Capital', 'Esha', 300000],
        ['', 'Dev', 200000],
        ['(d) Residue 3:2', 'Esha', q3_e],
        ['', 'Dev', q3_d],
        ['Total', '', 1200000],
    ], num=[2], total=True)

    kc = Checks()
    k_def = kc.add('500000-380000', 'deficiency of capital in the case')
    k_share = kc.add('120000/2', 'each partner\'s share of the deficiency (equal)')

    modes = table(['Mode', 'Section', 'When'], [
        ['By agreement', '40', 'With the consent of all partners, or under an existing contract between them'],
        ['Compulsory', '41', '(a) all partners, or all but one, are adjudicated insolvent; (b) an event makes the business, or carrying it on in partnership, unlawful (a lawful separate venture of the firm may continue)'],
        ['On contingencies (subject to contract)', '42', 'Expiry of the fixed term; completion of the venture; death of a partner; adjudication of a partner as insolvent'],
        ['By notice', '43', 'Partnership at will — written notice by any partner to all others; effective from the date stated, or else from communication'],
        ['By the court, on a partner\'s suit', '44', 'Unsound mind; permanent incapacity; misconduct; wilful/persistent breach; transfer of whole interest; business possible only at a loss; just and equitable ground'],
    ], title='Modes of dissolution of a firm')
    firm_vs_p = table(['Basis', 'Dissolution of the firm', 'Dissolution of partnership'], [
        ['Meaning', 'Relation ends between all the partners (Section 39)', 'Relation ends between one partner and the others; the rest continue'],
        ['Business', 'Comes to an end', 'Continues — firm is reconstituted'],
        ['Accounts', 'Assets realised, liabilities paid, books closed', 'Assets and liabilities revalued; books continue'],
        ['Court', 'Can be ordered by the court', 'Not a matter for court order'],
        ['Scope', 'Always includes dissolution of partnership', 'May or may not lead to dissolution of the firm'],
    ], title='Dissolution of firm vs dissolution of partnership')

    concepts = [
        {'id': 'c1', 'title': 'Registration of firms (Sections 58 and 59)',
         'body': ['Registration is optional under the Act — there is no penalty for not registering — but the disabilities in Section 69 make it practically necessary.',
                  'Section 58: the firm may register at any time by sending or delivering to the Registrar of Firms of the area where any place of business is (or will be) a statement in the prescribed form with the fee, giving: the firm name; the principal place of business; other places of business; the date each partner joined; full names and permanent addresses of the partners; and the duration of the firm. Every partner (or an agent specially authorised) signs and verifies it.',
                  'The firm name must not contain words such as Crown, Emperor, Empress, Empire, Imperial, King, Queen or Royal, or words suggesting the approval or patronage of Government, unless the State Government consents in writing.',
                  'Section 59: when satisfied, the Registrar records the statement in the Register of Firms and files it. Registration is treated as complete when the proper statement and fee are delivered; the entry is a routine act. Later changes (place of business, name, partners) are notified to the Registrar.'],
         'analogy': 'Registration is like getting a vehicle registration plate: you can drive the car without it, but you cannot complain to the police when someone dents it.',
         'work': 'CAs routinely file Form I with the Registrar of Firms for new firms and the notices of changes on reconstitution, because an unregistered firm cannot sue to recover its dues.'},
        {'id': 'c2', 'title': 'Consequences of non-registration (Section 69) and exceptions',
         'body': ['Disabilities of an unregistered firm: (1) no suit by a partner against the firm or any present or past partner to enforce a right under the partnership contract or the Act; (2) no suit by or on behalf of the firm against a third party to enforce a contractual right — the firm must be registered and the persons suing must be shown in the Register as partners; (3) no claim of set-off or other proceeding to enforce a contractual right.',
                  'Rights NOT affected: outsiders may still sue the firm or any of its partners; the right of a partner to sue for dissolution, for accounts of a dissolved firm or for realising its property; the powers of an official assignee or receiver to realise an insolvent partner\'s property; suits or set-off claims not exceeding ₹100 in value; firms with no place of business in the territories to which the Act applies; and criminal proceedings.',
                  'Courts have held that a registered firm whose constitution changes on a partner\'s death can still sue if the persons suing are shown as partners in the Register; but if a new partner has joined and is not recorded, the firm cannot sue until the Register is updated.'],
         'analogy': 'An unregistered firm is a one-way street: others can drive in (sue the firm), but the firm cannot drive out (sue others).',
         'work': 'Before filing a recovery suit for a client firm, a CA checks the Register of Firms extract: the firm must be registered and every suing partner must appear in it. Updating the Register first can save the suit from dismissal.'},
        {'id': 'c3', 'title': 'Dissolution of a firm and its modes (Sections 39 to 43)',
         'body': ['Section 39: dissolution of the partnership between all the partners is dissolution of the firm. When only one partner leaves and the others carry on, it is dissolution of partnership (reconstitution), not of the firm.',
                  'Without the court: by agreement (Section 40); compulsorily (Section 41); on contingencies such as expiry of term, completion of venture, death or insolvency of a partner, subject to contract (Section 42); by notice in a partnership at will (Section 43).'],
         'blocks': [firm_vs_p, modes],
         'analogy': 'Dissolution of partnership is one passenger getting off the bus; dissolution of the firm is the bus reaching its last stop and everyone getting off.',
         'work': 'Whether an event dissolves the firm or merely reconstitutes it changes the accounting (realisation account vs revaluation account) and the tax position. CAs must read the deed\'s continuation clause first.'},
        {'id': 'c4', 'title': 'Dissolution by the court (Section 44)',
         'body': ['On a suit by a partner, the court may dissolve the firm where: (a) a partner has become of unsound mind (suit by any other partner or by the insane partner\'s next friend) — temporary illness is not enough; (b) a partner other than the one suing has become permanently incapable of performing his duties; (c) a partner other than the one suing is guilty of conduct likely to harm the business, considering its nature — the misconduct need not be in the business itself; (d) a partner other than the one suing wilfully or persistently breaks the agreement on management, or behaves so that it is not reasonably practicable to carry on with him (e.g. embezzlement, false accounts, refusing to show accounts); (e) a partner other than the one suing has transferred his whole interest to a third party, or allowed it to be charged or sold for arrears of land revenue; (f) the business can only be carried on at a loss; (g) any other just and equitable ground — deadlock, partners not on speaking terms, loss of substratum, a partner gambling on the stock exchange.'],
         'analogy': 'The court is the referee who can stop the match when a player is injured for good, plays foul, or the game cannot be won at all.',
         'work': 'In partner disputes, a CA often acts as expert or receiver to establish persistent losses or falsified accounts — facts that support a dissolution suit under Section 44.'},
        {'id': 'c5', 'title': 'Liability, winding-up rights and continuing authority after dissolution (Sections 45 to 47)',
         'body': ['Section 45: even after dissolution, partners remain liable to third parties for acts that would have been acts of the firm, until public notice of the dissolution is given. Exceptions — no liability for acts after the date of ceasing to be a partner for: the estate of a deceased partner, an insolvent partner, and a partner who retired without being known to the third party as a partner. Any partner may give the notice.',
                  'Section 46: every partner or his representative can insist that the firm\'s property be used to pay its debts and liabilities and that the surplus be distributed among partners according to their rights.',
                  'Section 47: after dissolution, each partner\'s authority to bind the firm, and the partners\' mutual rights and duties, continue only so far as needed to wind up the affairs and finish transactions begun but unfinished at dissolution. The firm is never bound by the acts of a partner adjudicated insolvent, though a person who represents himself as a partner of the insolvent remains liable.'],
         'analogy': 'After dissolution the firm is like a shop with its shutters half down: you may finish serving the customers already inside, but you cannot welcome new ones.',
         'work': 'On dissolution, a CA drafts the public notice (newspaper and Official Gazette) at once — every day without it extends the partners\' exposure to new debts incurred by any one of them.'},
        {'id': 'c6', 'title': 'Settlement of accounts (Section 48) and firm vs separate debts (Section 49)',
         'body': ['Section 48 (subject to agreement): (a) losses, including deficiencies of capital, are met first out of profits, then out of capital, and lastly by the partners individually in their profit-sharing ratio; (b) assets, including any sums contributed by partners to make up deficiencies, are applied in this order — (i) debts to third parties, (ii) each partner\'s advances (as distinct from capital), rateably, (iii) each partner\'s capital, rateably, (iv) any residue divided in the profit-sharing ratio.',
                  'Section 49: where there are both firm debts and a partner\'s private debts — firm property goes first to firm debts, and each partner\'s share of any surplus goes to his private debts or to him; a partner\'s private property goes first to his private debts, and any surplus to firm debts.'],
         'blocks': [t1],
         'analogy': 'Section 48 is a queue at a ticket counter: outsiders first, then partners\' loans, then partners\' capital, and whatever is left is shared like profits.',
         'work': 'Preparing the realisation account and partners\' final accounts on dissolution is a classic CA engagement; the law decides the order in which the cash is paid out.'},
        {'id': 'c7', 'title': 'Other consequences of dissolution (Sections 50 to 55)',
         'body': ['Section 50: where the firm is dissolved by the death of a partner, Section 16(a) applies (subject to contract) to transactions of any surviving partner, or of the deceased partner\'s representatives, undertaken before the affairs are completely wound up — a personal profit made from the firm\'s property, name or connections must be accounted for to the firm. A partner or representative who has bought the goodwill keeps the right to use the firm name. Whatever the cause of dissolution, partners still owe each other good faith while the affairs are being wound up, and Section 53 lets any partner restrain misuse of the firm name or property.',
                  'Section 51: if a partner paid a premium to join a firm for a fixed term and the firm is dissolved before the term ends, he is entitled to a reasonable part of the premium back — unless the dissolution was caused mainly by his own misconduct, was by an agreement silent on return of premium, or was due to the death of a partner.',
                  'Section 52: where a partnership contract is rescinded for fraud or misrepresentation, the deceived partner has a lien on surplus assets for amounts he paid, ranks as a creditor of the firm for payments he made on its debts, and is entitled to be indemnified by the guilty partner.',
                  'Section 53: until the affairs are completely wound up, any partner or his representative may restrain the others from carrying on a similar business in the firm name or from using the firm\'s property for their own benefit — except a partner who has bought the goodwill.',
                  'Section 54: partners may, on or in anticipation of dissolution, agree that some or all of them will not carry on a similar business within a specified period or local limits; such restraint is valid if reasonable.',
                  'Section 55: on settlement after dissolution, goodwill (with the right to use the firm name, subject to contract) may be sold separately or with other property. After the sale, any partner may carry on a competing business and advertise it, but may not use the firm name, represent himself as carrying on the firm\'s business, or solicit its former customers, unless agreed; reasonable restraints agreed with the buyer are valid.'],
         'analogy': 'Even after the team breaks up, nobody may wear the old team jersey for his own gain until the trophies and debts are shared out.',
         'work': 'When a professional firm dissolves, the sale of goodwill and non-compete clauses are negotiated with these sections in mind; a CA values the goodwill and advises what restraint is "reasonable".'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Paying out on dissolution — deficiency of capital (Section 48)', 'difficulty': 'moderate', 'minutes': 10,
         'q': 'Amit, Bina and Chirag share profits 3:2:1. On dissolution the firm\'s assets realise ₹8,80,000. Outside creditors are ₹3,40,000; Bina has lent the firm ₹60,000; capitals are Amit ₹2,40,000, Bina ₹1,80,000 and Chirag ₹1,20,000. There is no agreement on settlement. Show how the amount realised will be applied.',
         'solution': [legal('Section 48: subject to agreement, losses including deficiency of capital are borne by the partners in their profit-sharing ratio; assets are applied first to third-party debts, then rateably to partners\' advances, then rateably to capital, and any residue is divided in the profit-sharing ratio.',
                            'Amount realised ₹8,80,000; creditors ₹3,40,000; Bina\'s loan ₹60,000; capitals total ₹5,40,000; ratio 3:2:1.',
                            'After creditors and Bina\'s loan, ₹4,80,000 remains against capital claims of ₹5,40,000 — a deficiency of ₹60,000. It is borne 3:2:1: ₹30,000, ₹20,000 and ₹10,000. Each partner receives capital less his share of the deficiency.',
                            'Creditors ₹3,40,000; Bina loan ₹60,000; then Amit ₹2,10,000, Bina ₹1,60,000 and Chirag ₹1,10,000. Nothing is left as residue.'),
                      t1b, t1],
         'checks': c1},
        {'id': 'i2', 'title': 'Firm debts and private debts (Section 49)', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'Xavier and Yamini, equal partners, have dissolved their firm. Firm property is ₹5,00,000 and firm debts ₹6,20,000. Xavier\'s private property is ₹3,00,000 and his private debts ₹1,40,000. Yamini\'s private property is ₹80,000 and her private debts ₹1,00,000. How will the firm creditors and the private creditors be paid?',
         'solution': [legal('Section 49: firm property is applied first to firm debts; a partner\'s separate property is applied first to his separate debts, and only the surplus goes to firm debts.',
                            'Firm shortfall ₹1,20,000. Xavier has a private surplus of ₹1,60,000; Yamini has a private deficit of ₹20,000.',
                            'Firm creditors take the whole ₹5,00,000 of firm property. For the balance ₹1,20,000 they can look only to the surplus of separate estates: Xavier\'s surplus of ₹1,60,000 covers it fully. Yamini\'s ₹80,000 goes entirely to her private creditors, who recover 80%. Xavier, having paid ₹1,20,000 of a loss to be shared equally, has a claim of ₹60,000 against Yamini.',
                            'Firm creditors are paid in full (₹5,00,000 + ₹1,20,000 from Xavier\'s surplus). Xavier\'s private creditors are paid in full; Yamini\'s private creditors get ₹80,000 (80%).'), t2],
         'checks': c2},
        {'id': 'i3', 'title': 'Unregistered firm sues a customer', 'difficulty': 'core', 'minutes': 6,
         'q': 'Nova Agencies, an unregistered firm, supplied goods worth ₹4,50,000 to Orbit Ltd. Orbit refuses to pay. Nova files a civil suit for recovery. Orbit objects that the suit is not maintainable. Separately, Orbit has sued Nova for ₹1,20,000 for defective goods. Decide both matters.',
         'solution': [legal('Section 69(2): a firm cannot go to court against an outsider to enforce a contractual right unless (i) it is registered and (ii) those suing appear, now or earlier, as partners in the Register of Firms. Outsiders, however, keep their full right to sue an unregistered firm.',
                            'Nova is unregistered. It sues Orbit on a contract of sale. Orbit, a third party, has sued Nova.',
                            'Nova\'s suit is barred by Section 69(2). Orbit\'s suit against Nova is maintainable, because third parties\' rights are expressly preserved. Nova also cannot claim a set-off above ₹100 in Orbit\'s suit (Section 69(3)).',
                            'Nova\'s suit will be dismissed; it should get registered and then file a fresh suit (subject to limitation). Orbit\'s suit against Nova can proceed.')]},
        {'id': 'i4', 'title': 'Is a partner\'s illness a ground for dissolution?', 'difficulty': 'core', 'minutes': 6,
         'q': 'Priya, Quentin and Rohan are partners. (a) Quentin is down with dengue and cannot attend office for five weeks. (b) Rohan, after a road accident, is permanently paralysed and cannot perform any duties. Priya wants the court to dissolve the firm. Advise.',
         'solution': [legal('Section 44: among the grounds on which a court may dissolve a firm at a partner\'s suit is that some other partner has become unable, permanently, to discharge his duties as partner. A passing illness does not qualify.',
                            'Quentin\'s illness is temporary (five weeks). Rohan\'s incapacity is permanent.',
                            'Situation (a) does not meet Section 44 — the incapacity is not permanent. Situation (b) falls squarely within permanent incapacity of a partner other than Priya.',
                            '(a) No dissolution on Quentin\'s illness. (b) The court may dissolve the firm on Priya\'s suit on the ground of Rohan\'s permanent incapacity.')]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Recovery suit for an unregistered client firm', 'role': 'CA in practice', 'situation': 'A client firm, never registered, wants to sue a distributor for ₹18 lakh of unpaid invoices. Limitation runs out in five months.',
         'steps': ['Explain Section 69(2): the suit is barred unless the firm is registered and the suing partners appear in the Register.', 'File the registration statement immediately with all partners\' signatures and the fee; registration dates from delivery.', 'File the suit only after registration, naming partners exactly as in the Register.', 'Meanwhile, consider remedies Section 69 does not bar — for example, criminal complaints where facts justify them.'],
         'takeaway': 'Register before you sue — and check that every suing partner is on the Register.', 'think': 'Would filing the suit first and registering a week later cure the defect?', 'answer': 'No. Registration must exist when the suit is filed; a later registration does not save a suit already filed — a fresh suit is needed.'},
        {'id': 'j2', 'title': 'Closing a firm properly', 'role': 'CA handling dissolution', 'situation': 'Three partners agree to dissolve their trading firm from 31 March.',
         'steps': ['Record the dissolution agreement (Section 40) with the date.', 'Give public notice at once (Section 45) and inform the Registrar, banks, GST and customers.', 'Realise assets; pay creditors, then partners\' loans, then capital, then residue in profit ratio (Section 48).', 'Ensure no partner trades in the firm name for himself until winding up is over (Sections 50 and 53); sell the goodwill if there is a buyer (Section 55).'],
         'takeaway': 'Public notice, the Section 48 order and protection of goodwill are the three pillars of a clean dissolution.'},
        {'id': 'j3', 'title': 'Partner keeps a second set of books', 'role': 'CA engaged by a partner for a forensic review', 'situation': 'Your client suspects his partner of omitting cash receipts and refusing to show the books.',
         'steps': ['Collect evidence of omitted receipts and repeated refusals.', 'Explain the remedies: suit for dissolution under Section 44 (persistent breach / misconduct), and accounts under Section 46/48.', 'Point out that an unregistered firm\'s partner can still sue for dissolution and accounts — Section 69 does not bar it.'],
         'takeaway': 'Falsified accounts and refusal to show books are classic grounds for court dissolution.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'Under the Partnership Act, getting a firm registered is:', 'options': ['Optional, but non-registration carries disabilities', 'Compulsory within 30 days', 'Compulsory for firms with more than 10 partners', 'Required only for particular partnerships'], 'answer': 0, 'explain': 'The Partnership Act does not make registration compulsory and imposes no penalty for not registering. Instead, Section 69 places disabilities on an unregistered firm and its partners, mainly the inability to file suits to enforce contractual rights. "Compulsory within 30 days" is the trap: no such time limit exists for registering a firm. The number of partners and the kind of partnership do not matter either. In practice: most firms register at the start, because without registration they cannot sue customers to recover unpaid bills.', 'topic': 'Registration of Firms', 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'Registration of a firm is treated as complete when:', 'options': ['The statement in the prescribed form with the fee is delivered to the Registrar', 'The Registrar issues the certificate', 'The firm publishes a notice', 'The court confirms the entry'], 'answer': 0, 'explain': "Under Sections 58 and 59, as explained in the study material, registration is complete when the statement in the prescribed form, signed and verified, is delivered to the Registrar with the fee. The Registrar's entry in the Register of Firms is a later administrative step. Waiting for the certificate is the trap: a firm that filed properly is registered from the filing date, even if the entry comes later. No public notice or court order is involved. In practice: a CA keeps the acknowledged copy of the filing, because it proves the registration date if a suit is challenged.", 'topic': 'Registration of Firms', 'concept': 'c1', 'difficulty': 'moderate'},
        {'id': 'm3', 'q': 'An unregistered firm CAN:', 'options': ['Be sued by a third party', 'Sue a customer for the price of goods', 'Claim a set-off of ₹50,000 in a suit against it', 'Sue a partner to enforce rights under the deed while the firm continues'], 'answer': 0, 'explain': 'Section 69 restricts suits by an unregistered firm or its partners, not suits against them. A third party can therefore sue an unregistered firm for what it owes. The firm cannot sue a customer for the price, or a partner to enforce rights under the deed while the firm continues. A set-off above ₹100 is also barred. The ₹50,000 set-off is the trap: set-off is allowed only up to ₹100. In practice: suppliers can sue an unregistered firm for their dues, but the firm cannot sue its own debtors.', 'topic': 'Consequences of Non-registration (Section 69)', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'Section 69 does not bar suits or set-off claims whose value does not exceed:', 'options': ['₹100', '₹1,000', '₹10,000', '₹500'], 'answer': 0, 'check': '100', 'explain': 'Section 69(4) leaves suits and claims of set-off not exceeding ₹100 in value outside the bar, so even an unregistered firm can pursue such tiny claims. ₹1,000 or ₹500 are traps, simply wrong amounts that sound more realistic today. The limit was fixed in 1932 and has never been raised, which is why it seems tiny. In practice: the exception has almost no practical value now, so an unregistered firm effectively cannot sue for its dues until it registers.', 'topic': 'Consequences of Non-registration (Section 69)', 'concept': 'c2', 'difficulty': 'moderate'},
        {'id': 'm5', 'q': 'A firm is compulsorily dissolved when:', 'options': ['Its business becomes unlawful', 'A partner dies', 'A partner becomes of unsound mind', 'The fixed term expires'], 'answer': 0, 'explain': "Section 41 makes dissolution compulsory when all the partners, or all but one, are adjudged insolvent, or when the firm's business becomes unlawful. Death of a partner is the trap: under Section 42 it dissolves the firm only subject to a contrary contract, and many deeds provide for continuation. A partner's unsound mind is a ground for the court to dissolve (Section 44), and a fixed term ending is a contingency under Section 42. In practice: if the law bans a product a firm deals in, the firm is dissolved at once, whatever the deed says.", 'topic': 'Consequences of Dissolution (Sections 45 - 55)', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm6', 'q': 'Which is NOT a ground for dissolution by the court under Section 44?', 'options': ['Temporary illness of a partner', 'Permanent incapacity of a partner', 'Business can be carried on only at a loss', 'Partner transferring his whole interest to a third party'], 'answer': 0, 'explain': "Section 44 lets the court dissolve a firm on grounds such as unsound mind, permanent incapacity, misconduct, persistent breach of the agreement, transfer of a partner's whole interest, business running only at a loss, or other just and equitable reasons. Temporary illness is not a ground: only an incapacity that is permanent counts. Permanent incapacity is the trap because it looks similar, but it is a valid ground. In practice: a partner recovering from a short hospital stay cannot be forced out through a court dissolution.", 'topic': 'Consequences of Dissolution (Sections 45 - 55)', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm7', 'q': 'On settlement after dissolution, the firm\'s assets are first applied to pay:', 'options': ['Debts of the firm to third parties', 'Partners\' loans', 'Partners\' capital', 'Residue in profit ratio'], 'answer': 0, 'explain': "Section 48(b): on settling accounts after dissolution, the firm's assets are applied first to pay the firm's debts to third parties. Then come partners' advances (loans) to the firm, then partners' capital, and any residue is divided in the profit-sharing ratio. Partners' loans are the trap: they rank after outside creditors but before capital. In practice: when preparing the realisation account, a CA pays outside creditors first, then partners' loan accounts, then capital, exactly following this order.", 'topic': 'Consequences of Dissolution (Sections 45 - 55)', 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm8', 'q': 'Losses on dissolution, including deficiency of capital, are borne in the absence of agreement:', 'options': ['First from profits, then capital, then by partners in profit-sharing ratio', 'By partners in capital ratio', 'Equally, regardless of the profit ratio', 'By the partner with the largest capital'], 'answer': 0, 'explain': 'Section 48(a): unless agreed, losses on dissolution, including any deficiency of capital, are met first from profits, then from capital, and finally by partners individually in the ratio in which they share profits. The capital ratio is the trap: it is used only if the deed says so, not by default. Equal sharing applies only where the profit ratio itself is equal. In practice: CAs preparing dissolution accounts often find partners arguing for the capital ratio, and point them to the deed or to Section 48(a).', 'topic': 'Consequences of Dissolution (Sections 45 - 55)', 'concept': 'c6', 'difficulty': 'moderate'},
        {'id': 'm9', 'q': 'After dissolution, partners remain liable for acts of a partner that would have been acts of the firm until:', 'options': ['Public notice of dissolution is given', 'Assets are realised', 'Six months pass', 'The Registrar strikes off the firm'], 'answer': 0, 'explain': 'Section 45: even after dissolution, partners remain liable to third parties for acts of a partner which would have bound the firm had they been done before dissolution, until public notice of the dissolution is given. Realising the assets is the trap: selling assets does not tell outsiders that the firm has ended. No six-month period or Registrar strike-off is involved. In practice: when a firm closes, the CA arranges a public notice in a newspaper and notifies the Registrar, so the former partners are protected.', 'topic': 'Consequences of Dissolution (Sections 45 - 55)', 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm10', 'q': 'The estate of a deceased partner is liable for acts of the firm done after his death:', 'options': ['Never, even without public notice', 'Only if public notice is not given', 'Up to six months', 'Only for acts of the surviving partners in winding up'], 'answer': 0, 'explain': 'The proviso to Section 45 says the estate of a partner who dies is not liable for acts done after the date of death, even if no public notice is given. Death is a fact that ends the partner\'s connection with the firm. "Only if public notice is not given" is the trap: public notice is needed for retirement or dissolution, not for death. In practice: legal heirs of a deceased partner are liable only for the firm\'s dues up to the date of death, and only to the extent of the estate they inherit.', 'topic': 'Consequences of Dissolution (Sections 45 - 55)', 'concept': 'c5', 'difficulty': 'moderate'},
        {'id': 'm11', 'q': 'A partnership at will is dissolved by notice from:', 'options': ['The date stated in the notice, or if none, the date of its communication', 'The date of the court order', 'The end of the financial year', 'Thirty days after the notice'], 'answer': 0, 'explain': 'Section 43(2): a partnership at will is dissolved from the date mentioned in the written notice of dissolution given by a partner to all the others; if no date is mentioned, from the date the notice is communicated. A court order is the trap: dissolution by notice needs no court. There is no thirty-day waiting period or year-end rule. In practice: a partner wanting to exit a partnership at will sends a written notice, often by registered post and email, naming the date of dissolution.', 'topic': 'Consequences of Dissolution (Sections 45 - 55)', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm12', 'q': 'On dissolution, assets realise ₹6,00,000. Creditors ₹2,00,000, partner A\'s loan ₹50,000, capitals A ₹1,50,000 and B ₹1,00,000; profit ratio equal. The residue paid to each partner is:', 'options': ['₹50,000', '₹1,00,000', '₹60,000', '₹75,000'], 'answer': 0, 'check': '(600000-200000-50000-150000-100000)/2', 'explain': "Apply Section 48 in order: assets ₹6,00,000 − creditors ₹2,00,000 = ₹4,00,000; − A's loan ₹50,000 = ₹3,50,000; − capitals (₹1,50,000 + ₹1,00,000) ₹2,50,000 = ₹1,00,000 residue. Residue is shared in the profit ratio, equally: ₹50,000 each. ₹1,00,000 is the trap: that is the total residue, not each partner's share. ₹75,000 forgets to repay A's loan before capital. In practice: this is the final cash distribution a CA prepares on dissolution, as the last step of the realisation account.", 'topic': 'Consequences of Dissolution (Sections 45 - 55)', 'concept': 'c6', 'difficulty': 'moderate'},
        {'id': 'm13', 'q': 'A partner who paid a premium to join a firm for a fixed term is NOT entitled to any return of premium on premature dissolution when the dissolution is caused by:', 'options': ['The death of a partner', 'The misconduct of another partner', 'A court order on just and equitable grounds', 'Losses in business'], 'answer': 0, 'explain': 'Section 51: a partner who paid a premium to join a firm for a fixed term can get back a reasonable part of it if the firm is dissolved early. He gets nothing if the dissolution is caused by the death of a partner, is mainly due to his own misconduct, or is under an agreement with no provision for returning it. Misconduct of another partner is the trap: there he is entitled to a refund. In practice: CAs advising incoming partners suggest a premium-refund clause in the deed so that the outcome is clear.', 'topic': 'Consequences of Dissolution (Sections 45 - 55)', 'concept': 'c7', 'difficulty': 'hard'},
        {'id': 'm14', 'q': 'Under Section 49, a partner\'s separate property is applied:', 'options': ['First to his separate debts; surplus to firm debts', 'First to firm debts', 'Rateably to firm and separate debts', 'Only to firm debts'], 'answer': 0, 'explain': 'Section 49: when firm debts and a partner\'s separate debts both exist, the firm\'s property is applied first to firm debts, and the partner\'s separate property is applied first to his separate debts; only the surplus of each is available for the other kind of debt. "First to firm debts" is the trap: that is the rule for firm property, not for a partner\'s own property. In practice: a partner\'s personal creditors, such as his home-loan bank, get priority over the firm\'s creditors on his personal assets.', 'topic': 'Consequences of Dissolution (Sections 45 - 55)', 'concept': 'c6', 'difficulty': 'core'},
    ]

    questions = [
        {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'legal',
         'q': 'Silver Line Traders is an unregistered firm with partners Tarun, Uma and Varun. (a) Tarun wants to sue Uma for his share of profits while the firm continues. (b) A supplier, Waheed, sues the firm for ₹2,60,000. (c) Varun wants to sue for dissolution and accounts. Examine each under Section 69.',
         'model': [legal('Section 69: (1) a partner of an unregistered firm cannot take the firm or a co-partner to court to enforce rights under the partnership contract or the Act; (2) the firm cannot sue a third party on a contract; (3) no set-off or other proceeding on a contract. Not affected: third parties\' right to sue the firm, and a partner\'s right to sue for dissolution, accounts of a dissolved firm or realisation of its property.',
                         'The firm is unregistered. Tarun sues a co-partner while the firm continues; Waheed, a third party, sues the firm; Varun seeks dissolution and accounts.',
                         '(a) Tarun\'s suit is to enforce a right under the partnership — barred by Section 69(1). (b) A third party\'s right to sue is preserved. (c) A suit for dissolution and accounts is expressly saved.',
                         '(a) Not maintainable. (b) Maintainable — Waheed can sue the firm. (c) Maintainable.')],
         'scheme': [{'id': 's1', 'pt': 'Section 69 disabilities stated', 'm': 1, 'skill': 'provision'}, {'id': 's2', 'pt': 'Exceptions stated', 'm': 1, 'skill': 'provision'},
                    {'id': 's3', 'pt': 'Application to (a), (b), (c)', 'm': 1.5, 'skill': 'application'}, {'id': 's4', 'pt': 'Conclusions', 'm': 0.5, 'skill': 'conclusion'}],
         'remarks': ['Many answers forget that dissolution suits are saved.'], 'mistakes': ['Saying an unregistered firm cannot be sued.'], 'tips': ['Answer each part in a separate line after a common provision paragraph.']},
        {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'State the grounds on which the court may dissolve a partnership firm under Section 44 of the Indian Partnership Act, 1932.',
         'model': [p('At the suit of a partner, the court may dissolve a firm on any of these grounds:'),
                   ul(['Insanity — a partner has become of unsound mind (suit by another partner or the insane partner\'s next friend).', 'Permanent incapacity of a partner other than the one suing.', 'Misconduct of a partner (other than the one suing) likely to affect the business prejudicially, having regard to its nature.',
                       'Wilful or persistent breach of the agreement relating to management, or conduct making it not reasonably practicable to carry on with him.', 'Transfer of his whole interest to a third party, or allowing his share to be charged or sold for arrears of land revenue.',
                       'The business can now run only at a loss.', 'Any other ground the court finds just and equitable — e.g. deadlock, loss of substratum, partners not on speaking terms.'])],
         'scheme': [{'id': 's1', 'pt': 'Insanity', 'm': 1, 'skill': 'provision'}, {'id': 's2', 'pt': 'Permanent incapacity', 'm': 1, 'skill': 'provision'}, {'id': 's3', 'pt': 'Misconduct', 'm': 1, 'skill': 'provision'},
                    {'id': 's4', 'pt': 'Persistent breach / transfer of interest', 'm': 1, 'skill': 'provision'}, {'id': 's5', 'pt': 'Perpetual losses', 'm': 1, 'skill': 'provision'}, {'id': 's6', 'pt': 'Just and equitable with an example', 'm': 1, 'skill': 'provision'}],
         'remarks': ['Write each ground with a one-line explanation; a bare list earns about half marks.'], 'mistakes': ['Listing death or insolvency (Section 42) as court grounds.'], 'tips': ['Memory hook: "I-P-M-B-T-L-J" — Insanity, Permanent incapacity, Misconduct, Breach, Transfer, Loss, Just & equitable.']},
        {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'Esha and Dev share profits 3:2. On dissolution the assets realise ₹12,00,000. Outside creditors are ₹4,50,000; Dev has advanced a loan of ₹1,00,000; capitals are Esha ₹3,00,000 and Dev ₹2,00,000. Applying Section 48, show the order in which the amount will be paid and how much each partner finally receives.',
         'model': [p('Section 48(b): assets go to third-party debts, then partners\' advances rateably, then capital rateably, and the residue in profit-sharing ratio.'),
                   q3t, p('Esha receives ₹3,90,000; Dev receives ₹3,60,000 (loan ₹1,00,000 + capital ₹2,00,000 + residue ₹60,000).')],
         'scheme': [{'id': 's1', 'pt': 'States the Section 48 order', 'm': 1.5, 'skill': 'provision'}, {'id': 's2', 'pt': 'Creditors and loan paid in order', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Capitals repaid; residue ₹1,50,000 in 3:2', 'm': 1.5, 'skill': 'computation'}, {'id': 's4', 'pt': 'Final amounts to each partner', 'm': 1, 'skill': 'presentation'}],
         'remarks': ['Repaying capital before partners\' loans is the most common error.'], 'mistakes': ['Dividing the residue in capital ratio.', 'Adding Dev\'s loan to his capital.'], 'tips': ['Show a three-column table: order, payee, amount.'],
         'checks': q3c},
        {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'legal',
         'q': 'Yash and Zoya dissolved their firm on 1 December 2025 by a deed but gave no public notice. On 20 December Yash borrowed ₹3,00,000 in the firm\'s name from Kabir, who did not know of the dissolution. Kabir seeks to recover from Zoya. Decide.',
         'model': [legal('Section 45: dissolution does not by itself free the partners — until a public notice of it is given, each of them answers to outsiders for anything a partner does that would have counted as an act of the firm before the dissolution. Exceptions: estate of a deceased partner, an insolvent partner, and a retiring partner not known to the third party as a partner.',
                         'The firm was dissolved on 1 December without public notice. Yash borrowed in the firm\'s name on 20 December from Kabir, who was unaware of the dissolution.',
                         'Borrowing in the firm name would have been an act of the firm before dissolution. No public notice had been given, and Zoya does not fall within any exception.',
                         'Zoya is liable to Kabir along with Yash for ₹3,00,000.')],
         'scheme': [{'id': 's1', 'pt': 'Section 45 rule — liability till public notice', 'm': 1.5, 'skill': 'provision'}, {'id': 's2', 'pt': 'Exceptions mentioned', 'm': 0.5, 'skill': 'provision'},
                    {'id': 's3', 'pt': 'Application to facts', 'm': 1, 'skill': 'analysis'}, {'id': 's4', 'pt': 'Conclusion: Zoya liable', 'm': 1, 'skill': 'conclusion'}],
         'remarks': ['A short, clean PFAC answer earns full marks.'], 'mistakes': ['Concluding that the dissolution deed alone protects Zoya.'], 'tips': ['Underline "until public notice is given".']},
    ]

    viva = [
        V('v1', 'Is registration of a partnership firm compulsory? What are the effects of non-registration?',
          'No, registration is not compulsory and there is no penalty, but under Section 69 an unregistered firm cannot sue a third party on a contract, a partner cannot sue the firm or his co-partners to enforce rights under the partnership, and the firm cannot claim a set-off. However, third parties can still sue the firm.',
          [P('p1', 'Not compulsory — optional, no penalty', 2, 'not compulsory|optional|voluntary|not mandatory|no penalty|not necessary|not required'),
           P('p2', 'Firm cannot sue third parties on a contract', 3, 'cannot sue|can not sue|no suit|not sue|not file a suit|cannot file|barred|not maintainable', 'third party|third parties|outsider|customer|debtor|others|' + ALT('{n} {o}', n=('cannot sue', 'not sue', 'no suit against', 'cannot file suit against', 'not file suit against', 'cannot take'), o=('third party', 'third parties', 'outsider', 'outsiders', 'customer', 'debtor', 'others')), min=2),
           P('p3', 'Partner cannot sue the firm or co-partners', 2, 'partner cannot sue|partners cannot sue|partner can not sue|partner not sue|co partner|co-partner|other partner|against the firm|fellow partner'),
           P('p4', 'No set-off; but third parties can sue the firm', 3, 'set off|setoff|set-off|third party can sue|third parties can sue|third party can sue|outsider can sue|others can sue|can be sued|sue the firm', min=1)], 'c2'),
        V('v2', 'Name the rights that are not affected by non-registration of a firm.',
          'Non-registration does not take away an outsider\'s right to sue the firm or a partner, the right of a partner to sue for dissolution, accounts or realisation of property of a dissolved firm, the powers of an official assignee or receiver, suits or set-off up to one hundred rupees, firms having no place of business in India, and criminal proceedings.',
          [P('p1', 'Third parties can sue the firm', 3, SAVED('third party|third parties|outsider|creditor|others'), 'sue|suit|claim|action', min=2),
           P('p2', 'Partner may sue for dissolution / accounts of dissolved firm', 3, SAVED('dissolution|dissolved|account|realis|realiz')),
           P('p3', 'Official assignee / receiver; claims up to ₹100; no place of business in India; criminal proceedings', 4, SAVED('official assignee|receiver|insolvent|100|hundred|place of business|criminal'), min=1)], 'c2'),
        V('v3', 'What is the difference between dissolution of a firm and dissolution of partnership?',
          'Dissolution of the firm means all the partners\' relation ends, the business closes, assets are realised and the books are closed. Dissolution of partnership means only one partner leaves, for example by retirement or death, and the remaining partners continue the business, so the firm is only reconstituted.',
          [P('p1', 'Dissolution of firm — relation ends between all partners; business closes', 5, ALT('firm {x}', x=('all', 'every', 'whole', 'entire', 'mean all', 'close', 'closes', 'wound', 'wind', 'business closes', 'business ends', 'comes to an end', 'ends completely')) + '|relation between all|between all partner|all partners relation|all the partners relation'),
           P('p2', 'Dissolution of partnership — one partner leaves; others continue; reconstitution', 5, ALT('partnership {x}', x=('1 partner', 'only 1', 'mean 1', 'partner retir', 'partner die', 'retir', 'death', 'some partner', 'particular partner', 'certain partner')) + '|others continue|other partners continue|remaining partners continue|rest continue|rest carry on|others carry on|remaining carry on|remaining partners carry|business continues|continue the business|reconstitut')], 'c3'),
        V('v4', 'State the grounds on which a court may dissolve a firm.',
          'Under Section 44 the court may dissolve a firm on a partner\'s suit if a partner becomes of unsound mind, becomes permanently incapable, is guilty of misconduct affecting the business, wilfully or persistently breaches the agreement, transfers his whole interest, if the business can only be carried on at a loss, or on any just and equitable ground.',
          [P('p1', 'At least three Section 44 grounds', 6, 'unsound mind|insan|lunatic|mental', 'permanent|incapab|incapacit|disabled', 'misconduct|misbehav|bad conduct', 'breach|break the agreement|breaking the agreement|violat', 'transfer|sold his share|sells his share|assign', 'loss|losses', 'just and equitable|just equitable|equitable|deadlock', min=3),
           P('p2', 'At least four grounds in all (unsound mind, permanent incapacity, misconduct, persistent breach, transfer of interest, perpetual loss, just and equitable)', 4, 'unsound mind|insan|lunatic|mental', 'permanent|incapab|incapacit|disabled', 'misconduct|misbehav|bad conduct', 'breach|break the agreement|breaking the agreement|violat', 'transfer|sold his share|sells his share|assign', 'loss|losses', 'just and equitable|just equitable|equitable|deadlock', min=4)], 'c4'),
        V('v5', 'In what order are the assets of a firm applied on dissolution under Section 48?',
          'First the debts of the firm to third parties are paid, then each partner\'s advances or loans as distinct from capital, then each partner\'s capital, and finally any residue is divided among the partners in their profit-sharing ratio. Losses, including deficiency of capital, are borne first out of profits, then capital, and then by partners in the profit-sharing ratio.',
          [P('p1', 'First: third-party debts', 3, ALT('first {c}', '{c} first', '{c} paid first', '{c} come first', '{c} are paid first', '{c} get paid first', c=('third party', 'third parties', 'outside creditor', 'outside creditors', 'creditors', 'creditor', 'outsiders', 'external creditor', 'firm debt', 'firm debts', 'debts of the firm', 'debts'))),
           P('p2', 'Then partners\' advances / loans', 3, ALT('{t} {l}', t=('next', 'second', 'secondly', 'after that', 'followed by', 'after creditors', 'after debts', 'thereafter', 'after them', 'paid', 'paying', 'after paying', 'settled'), l=('loan', 'advance', 'partner loan', 'partner advance', 'partners loan', 'partners advance', 'lent')) + '|loans second|advances second|loans next|advances next|loans come second|advances come second'),
           P('p3', 'Then capital', 2, 'capital'),
           P('p4', 'Residue in profit-sharing ratio', 2, 'residue|surplus|balance|remaining|left over|whatever is left', 'profit sharing ratio|profit ratio|profit-sharing|ratio|proportion', min=2)], 'c6'),
        V('v6', 'Until when are partners liable for acts done after dissolution, and who is excepted?',
          'Under Section 45 partners continue to be liable to third parties for acts which would have been acts of the firm until public notice of the dissolution is given. The exceptions are the estate of a deceased partner, an insolvent partner, and a partner who retired without being known to the third party as a partner.',
          [P('p1', 'Liable until public notice of dissolution', 5, 'public notice|notice to the public|published notice|notice in newspaper|gazette'),
           P('p2', 'Exceptions: deceased partner\'s estate, insolvent partner, unknown/dormant retiring partner', 5, 'deceased|death|dead|dies|died|estate', 'insolvent|insolvency|bankrupt', 'dormant|sleeping|not known|unknown|did not know', min=2)], 'c5'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Harbour Exports winds up', 'difficulty': 'hard',
        'case': ('Harbour Exports, a registered firm of equal partners Ira and Jai, is dissolved by agreement on 31 March 2026. Assets realise ₹8,00,000 against outside creditors of ₹3,00,000; Ira had lent the firm ₹1,20,000; capitals are Ira ₹3,00,000 and Jai ₹2,00,000. '
                 'No public notice of the dissolution was given. On 15 April 2026 Jai bought goods worth ₹90,000 in the firm\'s name from Kamal, an old supplier unaware of the dissolution. Ira also discovers that Jai used the firm\'s name in May 2026 to earn a commission of ₹40,000 for himself.'),
        'mcqs': [
            dict(M('k1a', 'After paying creditors and Ira\'s loan, what is the deficiency of capital?', ['₹1,20,000', '₹3,80,000', '₹2,00,000', 'Nil'], 0,
              'Cash available for capital = ₹8,00,000 − creditors ₹3,00,000 − Ira\'s loan ₹1,20,000 = ₹3,80,000. Capitals total ₹3,00,000 + ₹2,00,000 = ₹5,00,000, so the deficiency is ₹5,00,000 − ₹3,80,000 = ₹1,20,000. ₹3,80,000 is the trap: that is the cash left for capital, not the shortfall. "Nil" forgets to repay Ira\'s loan before capital. In practice: this deficiency is the loss a CA posts to the partners\' capital accounts in the realisation account before the final payments.', 'moderate', '500000-380000'), topic='Consequences of Dissolution (Sections 45 - 55)'),
            dict(M('k1b', 'How is the deficiency borne?', ['₹60,000 each — equal profit-sharing ratio', 'In capital ratio 3:2', 'Entirely by Jai', 'Entirely by Ira'], 0,
              'Section 48(a): losses on dissolution, including a deficiency of capital, are borne in the profit-sharing ratio unless the partners agreed otherwise. Ira and Jai share equally, so each bears ₹1,20,000 ÷ 2 = ₹60,000. The capital ratio of 3:2 is the trap: it looks fair but is not the legal default. In practice: Ira then receives ₹3,00,000 − ₹60,000 = ₹2,40,000 and Jai ₹2,00,000 − ₹60,000 = ₹1,40,000, totalling the ₹3,80,000 available, which a CA confirms before paying out.', 'moderate'), topic='Consequences of Dissolution (Sections 45 - 55)'),
            dict(M('k1c', 'Is Ira liable to Kamal for the goods bought by Jai on 15 April?', ['Yes — no public notice of dissolution was given', 'No — the firm was dissolved on 31 March', 'No — only Jai signed the order', 'Only if the firm was unregistered'], 0,
              'Section 45: after dissolution, partners remain liable to third parties for acts of a partner that would have been acts of the firm, until public notice of the dissolution is given. No notice was given, and Kamal, an old supplier, did not know of the dissolution, so Ira is liable for the ₹90,000. "No, the firm was dissolved on 31 March" is the trap: dissolution does not protect partners until outsiders are informed. In practice: a closing firm also writes to its regular suppliers and banks, besides publishing a newspaper notice.', 'hard'), topic='Consequences of Dissolution (Sections 45 - 55)'),
            dict(M('k1d', 'What can Ira do about Jai\'s ₹40,000 commission?', ['Require Jai to account for it to the firm, as winding up is not complete', 'Nothing — the firm was already dissolved', 'Claim it only after six months', 'Report it to the Registrar of Firms'], 0,
              'Until the firm\'s affairs are completely wound up, partners still owe each other good faith, and Section 16(a) requires a partner to hand over profit made from the use of the firm\'s name. Section 53 also lets Ira stop Jai from using the firm name for his own benefit. Section 50 deals specifically with dissolution by death. "Nothing, the firm was already dissolved" is the trap: duties continue during winding up. In practice: a CA handling the winding up credits such secret commissions to the firm before final distribution.', 'hard'), topic='Consequences of Dissolution (Sections 45 - 55)'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch04', 'n': 3, 'title': 'Registration and Dissolution of a Firm',
        'outcomes': ['Describe the procedure and effect of registering a firm (Sections 58 and 59).',
                     'Apply Section 69 to decide which suits an unregistered firm or its partners can and cannot file, including the exceptions.',
                     'Explain dissolution of a firm vs of partnership and the modes of dissolution, including dissolution by the court (Sections 39 to 44).',
                     'Apply the consequences of dissolution (Sections 45 to 55), including the order of settlement of accounts and the treatment of firm and separate debts, to numerical problems.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 45, 'practice': 55}, 'prereq': ['fnd-p2-ch04-u02'],
                 'exam_tip': 'Section 69 problems and Section 44 grounds are asked frequently; Section 48 order of payment can be set as a small numerical. Always state "until public notice" for Section 45.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {'summary': ['Registration optional (no penalty); statement to Registrar (Section 58); complete on filing; entry in Register of Firms (Section 59).',
                                 'Section 69: unregistered firm cannot sue third parties on contract; partner cannot sue firm/partners; no set-off. Saved: third parties suing the firm, dissolution/accounts suits, official assignee, ₹100 claims, criminal cases.',
                                 'Dissolution of firm (all partners) vs of partnership (one partner leaves).',
                                 'Modes: agreement (40), compulsory (41), contingencies (42), notice (43), court (44).',
                                 'After dissolution: liable till public notice (45); right to wind up (46); authority only to wind up (47); order of payment (48); firm vs separate debts (49); Sections 50–55 on personal profits, premium, rescission for fraud, firm name, restraint and goodwill.'],
                     'remember': ['Section 48 order: outsiders → partners\' loans → capital → residue in profit ratio.', 'Section 41 compulsory: all/all-but-one insolvent; business unlawful.', 'Court grounds: unsound mind, permanent incapacity, misconduct, persistent breach, transfer of interest, perpetual loss, just and equitable.'],
                     'traps': ["Don't say an unregistered firm cannot be sued.", "Don't list death or insolvency as court grounds — they are Section 42 contingencies.", "Don't repay capital before partners' loans.", "Don't share deficiency of capital in capital ratio (unless agreed)."]},
        'quickref': [{'k': 'Section 58', 'v': 'Application for registration — contents, signed by all partners'}, {'k': 'Section 59', 'v': 'Registrar records entry in Register of Firms'},
                     {'k': 'Section 69', 'v': 'Disabilities of non-registration and exceptions'}, {'k': 'Section 39', 'v': 'Dissolution of firm = between all partners'},
                     {'k': 'Sections 40–43', 'v': 'Agreement · compulsory · contingencies · notice'}, {'k': 'Section 44', 'v': 'Dissolution by court — seven grounds'},
                     {'k': 'Section 45', 'v': 'Liability till public notice'}, {'k': 'Sections 46–47', 'v': 'Right to wind up; continuing authority'},
                     {'k': 'Section 48', 'v': 'Losses: profits → capital → partners in PSR; assets: outsiders → advances → capital → residue'},
                     {'k': 'Section 49', 'v': 'Firm property to firm debts first; separate property to separate debts first'},
                     {'k': 'Sections 50–55', 'v': 'Personal profits · premium · rescission for fraud · firm name · restraint · goodwill'}],
        'viva': viva, 'cases': cases,
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
           's1': _k('section 69', 'unregistered|not registered', 'cannot sue|no suit|not sue|barred|cannot file|not maintainable|cannot enforce|cannot take|no partner can sue|cannot bring'),
           's2': _k('third party|third parties|outsider', 'dissolution|accounts|realisation|realise|realize'),
           's3': _k('tarun barred|tarun cannot|tarun s suit is barred|suit barred|barred section 69 1|69 1|tarun suit barred|tarun is barred',
                    'third party can sue|third party s right|preserved|third parties can sue|right to sue the firm|third party right|waheed s suit|waheed is a third party',
                    'dissolution saved|dissolution expressly saved|saved|expressly saved|exception|not affected|dissolution is allowed|dissolution allowed|varun s suit'),
           's4': _k('not maintainable|tarun cannot sue|tarun s suit is not maintainable|tarun fails|tarun s suit fails',
                    'waheed maintainable|waheed can sue|b maintainable|waheed s suit maintainable|waheed succeed|waheed s suit is maintainable',
                    'varun maintainable|varun can sue|c maintainable|varun s suit maintainable|varun s suit is maintainable|varun succeed',
                    wrong=[{'kw': ['tarun s suit is maintainable|tarun maintainable|tarun can file|waheed cannot sue|varun cannot sue'], 'say': 'Section 69 bars suits by partners of an unregistered firm to enforce partnership rights (a), but not suits by third parties (b) or suits for dissolution and accounts (c).'}]),
           },
    'q2': {'extra_ok': True,
           's1': _k('insanity|unsound mind|insane|lunatic'),
           's2': _k('permanent incapacity|permanently incapable|incapacity|incapable'),
           's3': _k('misconduct'),
           's4': _k('persistent breach|wilful breach|breach of agreement|breach|transfer of interest|transferred his whole interest|transfer|transfers|transferred'),
           's5': _k('only at a loss|carried on only at a loss|perpetual loss|continuous loss|losses|loss'),
           's6': _k('just and equitable', 'deadlock|substratum|speaking terms|quarrel|dispute|disagreement|talking terms|mistrust|friction|not on speaking terms|not being on speaking terms|not speaking'),
           },
    'q3': {'extra_ok': False,
           's1': _k('third party|outside creditors|creditors|outsiders|outside liabilities', 'advance|advances|loan', 'capital', 'residue|surplus|balance|remaining|remainder', 'first|then|thereafter|next|after'),
           's2': _k('creditors|third party|outside|outsiders', 'loan|advance', nums=[450000, 100000]),
           's3': _k('capital', 'residue|surplus|balance|3:2|3 2', nums=[300000, 200000, 90000, 60000]),
           's4': _k('esha 390000|390000 esha|esha receives 390000|esha gets 390000|esha rs 390000|esha total 390000|esha s total 390000', 'dev 360000|360000 dev|dev receives 360000|dev gets 360000|dev rs 360000|dev total 360000|dev s total 360000', nums=[390000, 360000]),
           },
    'q4': {'extra_ok': False,
           's1': _k('public notice', 'liable|liability|continue|responsible|answer|answerable|bound', 'section 45|dissolution|after dissolution|until|till'),
           's2': _k('deceased|death|estate', 'insolvent|insolvency', 'retiring|retired|not known', n=2),
           's3': _k('no public notice|public notice not|without public notice|no notice|not given public notice|public notice was not|not given|without any public notice', 'did not know|unaware|not aware|without knowledge|no knowledge|no exception|not within any exception|not fall within|act of the firm|firm name|not covered|none of the exceptions'),
           's4': _k('zoya liable|zoya is liable|zoya is also liable|zoya also liable|zoya must pay|zoya bound|zoya jointly|zoya and yash liable|both liable|zoya cannot escape|zoya is bound|zoya will be liable',
                    wrong=[{'kw': ['zoya not liable|zoya is not liable|kabir cannot recover'], 'say': 'Until public notice of dissolution is given, every partner remains liable for acts that would have been acts of the firm (Section 45) — Zoya is liable.'}]),
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
