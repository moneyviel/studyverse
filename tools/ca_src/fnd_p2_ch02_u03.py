"""CA Foundation · Paper 2 Business Laws · Chapter 2 The Indian Contract Act, 1872 · Unit 3 Other Essential Elements of a Contract.
Original explanations and problems; sections and leading cases are cited by name only."""
from lib import *
from ca_viva import P, ALT, V
from ca_cases import M

UID = 'fnd-p2-ch02-u03'


def Q(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check: d['check'] = check
    return d


def S(sid, pt, m, skill): return {'id': sid, 'pt': pt, 'm': m, 'skill': skill}


def build():
    # ---- figures ----
    ci = Checks()
    books, coat_bill, coat_fair, phone = 9000, 7500, 6000, 52000
    nec = ci.add('9000+6000', 'reasonable price of necessaries recoverable from the minor\'s property')
    bill = ci.add('9000+7500+52000', 'total bill raised by the shop')
    lost = ci.add('68500-15000', 'part of the bill not recoverable')

    cu = Checks()
    principal, rate = 80000, 12
    fair = cu.add('80000+80000*12/100', 'principal plus one year\'s interest at the 12% the court considers fair')

    cc = Checks()
    k_nec = cc.add('4500+3000', 'reasonable price of the necessaries (tuition fee and spectacles)')

    minor_tbl = table(['Rule', 'Effect'], [
        ['Agreement with a minor', 'Void from the beginning (Mohori Bibi v. Dharmodas Ghose); the minor cannot be made to repay or compensate — but property or money still traceable in his hands (unspent) may be ordered to be restored (restitution)'],
        ['Ratification on attaining majority', 'Not possible — a fresh contract (with fresh consideration) is needed'],
        ['Minor as promisee / beneficiary', 'Can enforce a contract that benefits him, e.g. a promissory note in his favour'],
        ['Plea of minority', 'Can always be raised by the minor, even if he lied about his age — no estoppel against a minor'],
        ['Necessaries supplied (Section 68)', 'Supplier reimbursed from the minor\'s property; the minor is not personally liable'],
        ['Contract by guardian', 'Valid if within the guardian\'s competence and for the minor\'s benefit; but a guardian cannot bind the minor to buy immovable property'],
        ['Specific performance', 'Not available for or against a minor on a void agreement'],
        ['Insolvency', 'A minor cannot be declared insolvent'],
        ['Partnership', 'Cannot be a partner; may be admitted to the benefits with the consent of all partners'],
        ['Agent', 'May act as an agent (principal is bound), but is not personally liable to the principal'],
        ['Parents / guardians', 'Not bound by the minor\'s agreements, except where the minor acts as their authorised agent'],
        ['Joint contract with an adult', 'The adult is liable; the minor is not'],
        ['Adult surety for a minor', 'The surety is liable to the creditor'],
        ['Shares', 'Cannot subscribe; may hold fully paid shares received by transfer or transmission through a guardian'],
        ['Torts', 'Liable for civil wrongs, unless the wrong is really a breach of contract in disguise'],
    ], title='Position of a minor — 15 rules')

    cvu = table(['Basis', 'Coercion (Section 15)', 'Undue influence (Section 16)'], [
        ['Nature', 'Physical or criminal pressure — threat of an act forbidden by penal law, or unlawful detention of property', 'Mental or moral pressure — misuse of a position of dominance'],
        ['Relationship', 'No relationship between the parties is needed', 'A relationship enabling one party to dominate the will of the other is essential'],
        ['Who may use it', 'Any person, against any person (even a stranger to the contract)', 'A party to the contract who is in the dominant position'],
        ['Object', 'To make a person enter into an agreement', 'To obtain an unfair advantage over the other'],
        ['Effect', 'Voidable (Section 19); money or goods received must be returned (Section 72)', 'Voidable (Section 19A); may be set aside absolutely or on just terms'],
    ], title='Coercion vs undue influence')

    fvm = table(['Basis', 'Fraud (Section 17)', 'Misrepresentation (Section 18)'], [
        ['Intention', 'Intention to deceive', 'No intention to deceive — the maker believes the statement is true'],
        ['Knowledge', 'Maker knows the statement is false (or is reckless)', 'Maker honestly believes it, though without sufficient grounds'],
        ['Remedies', 'Rescission and also damages; or affirm and insist on being put in the position he would have been in', 'Rescission; or affirm on the same terms — generally no damages'],
        ['Silence', 'Silence is fraud only where there is a duty to speak or silence is equivalent to speech', 'Not applicable in that form'],
        ['Defence of ordinary diligence', 'Available, except for active fraud', 'Available — not voidable if the truth could be discovered with ordinary diligence'],
    ], title='Fraud vs misrepresentation')

    concepts = [
        {'id': 'c1', 'title': 'Capacity to contract — Section 11', 'body': [
            'Section 10 needs competent parties. Section 11 sets three tests of competence: the person must be a major under the personal law that governs him, must have a sound mind, and must not be barred from contracting by any law.',
            'Under the Indian Majority Act, 1875, a person domiciled in India attains majority on completing 18 years. A person who is even one day short of 18 is a minor for contract purposes.'],
         'analogy': 'Capacity is the driving licence for contracts: age, a clear mind and no ban.',
         'work': 'Before accepting a customer, banks and NBFCs check age and identity; a loan document signed by a minor gives the lender no contractual claim.'},
        {'id': 'c2', 'title': 'Agreements with or by a minor', 'body': [
            'A minor\'s agreement is void from the very beginning (void ab initio). In Mohori Bibi v. Dharmodas Ghose (1903), a minor mortgaged his house for a loan; the mortgage was held void and the lender could not even recover the money advanced.',
            'Because the agreement is void, a minor cannot ratify it on attaining majority. A minor may, however, be a beneficiary — he can enforce a contract under which he is entitled to receive something, and he can always plead minority as a defence.',
            'Necessaries (Section 68): where a person supplies a minor (or someone dependent on him) with necessaries suited to his condition in life, the supplier is entitled to be reimbursed from the minor\'s property. The minor is not personally liable. The supplier must show the goods were reasonably necessary and that the minor did not already have a sufficient supply.',
            'Other rules are summarised in the table: guardian contracts, partnership, agency, shares, surety, joint contracts and liability in tort.'],
         'blocks': [minor_tbl],
         'analogy': 'The law puts a protective glass wall around a minor: he can receive benefits through it, but nobody can reach in and hold him to a bargain.',
         'work': 'When a client\'s customer turns out to be a minor, the CA advises that unpaid invoices cannot be recovered from him personally — only the reasonable price of necessaries from his property.'},
        {'id': 'c3', 'title': 'Persons of unsound mind and disqualified persons', 'body': [
            'Section 12: a person is of sound mind for making a contract if, at the time he makes it, he can understand it and form a rational judgment about its effect on his interests.',
            'A person usually of unsound mind but occasionally sound (e.g. a patient with lucid intervals) may contract while sound. A person usually sound but occasionally unsound (e.g. heavily drunk or delirious with fever) may not contract while unsound. An agreement by a person of unsound mind is void; Section 68 (necessaries) applies to him as it does to a minor.',
            'Disqualified persons: some persons are barred, fully or partly, by their status — foreign sovereigns and ambassadors (cannot be sued without Central Government consent, though they may sue), alien enemies (during war), companies and other corporations (only within their objects and powers), convicts (while serving sentence) and insolvents (cannot deal with their property, which vests in the official assignee/receiver).'],
         'analogy': 'The question is not "is he a patient?" but "was his mind clear at the moment he signed?"',
         'work': 'In a family business, if an elderly partner signs documents during a period of serious illness, a CA flags the risk that those documents may be challenged as void.'},
        {'id': 'c4', 'title': 'Consent and free consent — Sections 13, 14, 19, 19A', 'body': [
            'Section 13: there is consent only when the parties understand and accept the same thing in an identical sense — a meeting of minds (consensus ad idem).',
            'Section 14: consent is free when it is not caused by coercion (Section 15), undue influence (Section 16), fraud (Section 17), misrepresentation (Section 18) or mistake (Sections 20, 21 and 22).',
            'Effects: where coercion, fraud or misrepresentation produced the consent, the affected party may choose to avoid the contract — it is voidable at his option (Section 19); consent caused by undue influence also makes it voidable (Section 19A); a bilateral mistake of fact essential to the agreement makes it void (Section 20).',
            'Where there is no consent at all (e.g. a person signs a document believing it to be something entirely different), there is no agreement. Where consent exists but is not free, the contract is generally voidable.'],
         'analogy': 'Consent is saying "yes"; free consent is saying "yes" with no gun to your head, no puppet strings, no lies and no misunderstanding.',
         'work': 'Auditors who find that a supplier contract was signed under pressure or on false information note that it may be avoided — affecting provisions and contingent liabilities.'},
        {'id': 'c5', 'title': 'Coercion — Section 15', 'body': [
            'Coercion means doing, or threatening to do, an act that the penal law prohibits (the section refers to the Indian Penal Code, now replaced by the Bharatiya Nyaya Sanhita), or wrongfully holding back — or threatening to hold back — someone\'s property to his harm, in order to make a person agree to a contract.',
            'Points: it may be employed by any person (not necessarily a party) against any person (not necessarily the party contracting); it does not matter whether the penal law is in force in the place where the coercion is used.',
            'A threat to commit suicide has been treated as coercion, since suicide is an act forbidden by penal law (e.g. a release deed obtained from wife and son by such a threat was set aside). An agent who refuses to hand over the principal\'s account books unless released from liability coerces by unlawful detention of property.',
            'Effects: the contract is voidable at the option of the coerced party (Section 19). Whoever receives money or goods because of coercion is bound to give them back (Section 72).'],
         'blocks': [cvu],
         'analogy': 'Coercion is "sign, or else" — the "or else" being a crime or the holding back of your property.',
         'work': 'A vendor who refuses to release a client\'s goods unless the client signs a new, harsher price agreement may be using coercion; the CA documents the facts for the client\'s lawyer.'},
        {'id': 'c6', 'title': 'Undue influence — Section 16 and 19A', 'body': [
            'Undue influence exists where the relationship lets one party control the other\'s decisions, and that party exploits this control to secure an unfair benefit for himself.',
            'The law presumes such control where the stronger party (a) holds real or apparent authority over him (employer–employee, income-tax officer–assessee), (b) stands in a fiduciary relation (guardian–ward, doctor–patient, lawyer–client, spiritual guru–disciple), or (c) contracts with a person whose mental capacity is affected by age, illness or mental or bodily distress.',
            'Burden of proof: if the dominant party enters into a transaction that appears unconscionable, he must prove that he did not use undue influence.',
            'Effect (Section 19A): voidable at the option of the influenced party; the court may set it aside absolutely, or, if that party has received a benefit, on such terms as are just — e.g. ordering return of the principal with reasonable interest instead of the inflated sum.'],
         'analogy': 'Undue influence is a quiet push from someone you trust or depend on, used to tilt the deal in his favour.',
         'work': 'Gifts or loans from elderly clients to their advisers, carers or managers are a classic red flag; CAs advising families watch for transactions that benefit the person in the dominant position.'},
        {'id': 'c7', 'title': 'Fraud — Section 17', 'body': [
            'Fraud covers the following acts by a contracting party, his agent or someone acting with his knowledge, done to deceive the other side or to persuade it to contract: (1) asserting as a fact something false that the maker himself does not believe; (2) active concealment of a fact by one who knows or believes it; (3) making a promise with no intention of performing it; (4) any other act designed to deceive; and (5) anything done or omitted that a law specifically labels as fraudulent.',
            'Essentials: a false representation (or concealment) of a fact — not a mere opinion or sales talk; made before or at the time of the contract; with knowledge of its falsity or recklessly; with intent to deceive; the other party actually relied on it; and suffered loss.',
            'Mere silence is not fraud. It becomes fraud where (a) there is a duty to speak (e.g. contracts of utmost good faith such as insurance, or a fiduciary relationship), or (b) the silence is, in itself, equivalent to speech (e.g. the buyer says "If you say nothing, I shall take it the horse is sound").',
            'Remedies of the deceived party: rescind the contract; claim damages; or affirm the contract and insist that he be put in the position he would have been in if the representation had been true. Exceptions (Section 19): no right to avoid where the consent was not caused by the fraud, or (for fraud by silence) where the party could have discovered the truth with ordinary diligence.'],
         'blocks': [fvm],
         'analogy': 'Fraud is a lie told on purpose to win the deal; misrepresentation is an honest mistake that still misleads.',
         'work': 'Forensic and due-diligence work by CAs often turns on whether a seller knowingly hid a liability (fraud — damages possible) or innocently misstated it (misrepresentation — usually rescission only).'},
        {'id': 'c8', 'title': 'Misrepresentation — Section 18', 'body': [
            'Misrepresentation is an innocent false statement. It covers: (1) a positive assertion of something untrue, made in a manner not warranted by the information of the person making it, though he believes it to be true; (2) any breach of duty which, without intent to deceive, gains an advantage for the person committing it by misleading the other to his prejudice; (3) causing, however innocently, the other party to make a mistake about the substance of the thing that is the subject of the agreement.',
            'Remedies: the misled party may rescind the contract, or affirm it and insist on being placed in the position he would have been in had the statement been true. Damages are generally not available for innocent misrepresentation. If the truth could have been discovered with ordinary diligence, the contract is not voidable (Exception to Section 19).'],
         'analogy': 'The seller who says "this car runs 25 km a litre" because the last owner told him so — wrong, but not a liar.',
         'work': 'Information memoranda for business sales include disclaimers precisely to manage misrepresentation risk.'},
        {'id': 'c9', 'title': 'Mistake — Sections 20, 21 and 22', 'body': [
            'Mistake of law: a mistake about Indian law gives no relief — everyone is presumed to know the law of the land (Section 21). A mistake about a foreign law is treated as a mistake of fact.',
            'Bilateral mistake of fact (Section 20): where both parties are mistaken about a matter of fact essential to the agreement, the agreement is void. It may relate to the subject-matter — its existence (e.g. goods already destroyed when the contract is made), identity, title, quantity, quality or price — or to the possibility of performance. An erroneous opinion about the value of the thing is not a mistake of fact.',
            'Unilateral mistake (Section 22): a contract is not voidable merely because one party was mistaken about a fact. Exceptions recognised by courts: mistake as to the identity of the person contracted with where identity matters, and mistake as to the nature of the document signed (where the signer was not careless).'],
         'analogy': 'If both of you are wrong about the same vital fact, the deal never stood on its feet; if only you were wrong, that is your risk.',
         'work': 'When both buyer and seller value goods that, unknown to both, had already been destroyed in a warehouse fire, the CA treats the sale as void — no revenue and no receivable.'},
        {'id': 'c10', 'title': 'Legality of object and consideration — Sections 23 and 24', 'body': [
            'Section 23: consideration or object is unlawful if it (a) is forbidden by law; (b) is of such a nature that, if permitted, it would defeat the provisions of any law; (c) is fraudulent; (d) involves or implies injury to the person or property of another; or (e) is regarded by the court as immoral or opposed to public policy. Every agreement with an unlawful object or consideration is void.',
            'Agreements opposed to public policy include: trading with an enemy; stifling prosecution (agreeing to drop a criminal case for money); maintenance and champerty (financing another\'s litigation for a share of the proceeds, where unfair); trafficking in public offices and titles (paying to procure a government post or an award); agreements creating monopolies; marriage brokerage (arranging a marriage for a reward); interfering with the course of justice; and agreements creating an interest against duty (e.g. an agent secretly taking a commission from the other side).',
            'Section 24: where one consideration supports several objects, or several considerations support one object, and any part of it is unlawful, the entire agreement fails — unless the lawful part can be separated, in which case the lawful part may be enforced.'],
         'analogy': 'An unlawful object is poison in the well: the whole water is unusable unless the poisoned bucket can be lifted out separately.',
         'work': 'Payments to "facilitators" for licences or contracts are void agreements and also expose the company to criminal liability; CAs flag such entries in audit.'},
        {'id': 'c11', 'title': 'Void agreements — Sections 26 to 30 and 56', 'body': [
            'Agreements expressly declared void: by incompetent parties (Section 11); under a bilateral mistake of fact (Section 20); with unlawful consideration or object (Section 23) or unlawful in part (Section 24); without consideration (Section 25); in restraint of marriage (Section 26); in restraint of trade (Section 27); in restraint of legal proceedings (Section 28); uncertain in meaning (Section 29); by way of wager (Section 30); and to do an impossible act (Section 56).',
            'Restraint of marriage (Section 26): any agreement restraining the marriage of a person other than a minor is void.',
            'Restraint of trade (Section 27): an agreement restraining anyone from carrying on a lawful profession, trade or business is void to that extent. Exceptions: (i) the seller of goodwill may agree not to carry on a similar business within specified, reasonable local limits so long as the buyer carries on a like business there; (ii) under the Partnership Act, partners may agree not to carry on a competing business during the partnership (Section 11), and an outgoing partner may agree not to compete within a specified period or local limits if reasonable (Section 36). A service agreement restraining an employee from competing during the term of employment is not a restraint of trade; a restraint after the employment ends is void.',
            'Restraint of legal proceedings (Section 28): void if it absolutely restricts a party from enforcing his rights through courts, or shortens the time for doing so. Valid exception: agreements to refer present or future disputes to arbitration (must be in writing).',
            'Uncertainty (Section 29): an agreement whose meaning is not certain or capable of being made certain is void ("100 tonnes of oil" is void unless the context shows which oil).',
            'Wager (Section 30): an agreement under which one party will pay the other money (or something worth money) depending on how an uncertain future event turns out, each side standing to gain or lose, and neither caring about the event except for the stake. Essentials: a promise to pay money or money\'s worth; conditional on an uncertain event; mutual chances of gain or loss; common intention to bet; no control over the event; no insurable interest. Lotteries, and prize competitions that depend on chance, are wagers (State of Bombay v. R.M.D. Chamarbaugwala). Not wagers: chit funds, genuine commercial and share transactions intended to be settled by delivery, games of skill, and contracts of insurance. Section 30 does not affect an agreement to subscribe or contribute towards a horse-race prize (a plate, prize or money award for the winner) worth ₹500 or more; a horse-race prize below ₹500 is treated as a wager.'],
         'analogy': 'Void agreements are blank cheques — they look like contracts but no court will cash them.',
         'work': 'Non-compete clauses in employment and business-sale agreements are reviewed against Section 27; CAs valuing a business acquisition check that the seller\'s non-compete falls within the goodwill exception.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Bill raised on a minor student', 'difficulty': 'moderate', 'minutes': 8,
         'q': f'Rhea, aged 17, a college student with no other supply of such items, buys on credit from Gupta Stores: textbooks {R(books)}, a winter coat billed at {R(coat_bill)} (fair price {R(coat_fair)}), and a premium mobile phone {R(phone)}. She does not pay. Rhea owns a fixed deposit inherited from her grandfather. What can Gupta Stores recover, and from whom?',
         'solution': [legal('A minor\'s agreement is void (Mohori Bibi v. Dharmodas Ghose). Section 68: a person who supplies necessaries suited to the condition in life of a minor is entitled to be reimbursed from the minor\'s property — the reasonable price only; the minor is not personally liable.',
                            'Textbooks and a winter coat are necessaries for a college student who had no supply; a premium phone is a luxury, not a necessary. Rhea has property (a fixed deposit).',
                            f'Recovery is limited to the reasonable price of necessaries: books {R(books)} + coat at fair price {R(coat_fair)} = {R(nec)}. Nothing for the phone, and the excess billed on the coat is not recoverable.',
                            f'Gupta Stores can recover {R(nec)} from Rhea\'s property (her fixed deposit), not from her personally. Of the bill of {R(bill)}, {R(lost)} cannot be recovered.'),
                      table(['Item', 'Necessary?', 'Billed (₹)', 'Recoverable (₹)'], [['Textbooks', 'Yes', books, books], ['Winter coat', 'Yes — fair price only', coat_bill, coat_fair], ['Premium phone', 'No — luxury', phone, 0], ['Total', '', bill, nec]], num=[2, 3], total=True)],
         'checks': ci},
        {'id': 'i2', 'title': 'Is silence fraud?', 'difficulty': 'core', 'minutes': 6,
         'q': 'Manoj sells his second-hand car to Priya. He knows that the gearbox has a defect but says nothing; Priya does not ask, and a basic test drive would have revealed the problem. Later Priya wants to avoid the contract for fraud. Advise.',
         'solution': [legal('Section 17, Explanation: mere silence about facts likely to affect a person\'s willingness to contract is not fraud, unless there is a duty to speak or the silence is in itself equivalent to speech. Exception to Section 19: where consent was caused by silence amounting to fraud, the contract is not voidable if the party could have discovered the truth with ordinary diligence.',
                            'Manoj stayed silent about the defect; Priya asked nothing; there was no fiduciary relation; an ordinary test drive would have revealed the defect.',
                            'A seller of goods has no general duty to disclose defects to the buyer, and Priya did not ask a question that would make silence equal to speech. Besides, ordinary diligence would have revealed the truth.',
                            'Manoj\'s silence is not fraud; Priya cannot avoid the contract on that ground. (Had she asked and he said "the gearbox is fine", it would be fraud.)')]},
        {'id': 'i3', 'title': 'Money-lender and a distressed borrower', 'difficulty': 'hard', 'minutes': 8,
         'q': f'Balwant, a farmer whose crop has failed and whose daughter is in hospital, borrows {R(principal)} from a money-lender who makes him sign a bond for repayment of ₹1,60,000 after one year. Balwant pleads undue influence. If the court sets the bond aside on terms and treats {rate}% a year as fair interest, how much must Balwant repay?',
         'solution': [legal('Section 16: a person is deemed to dominate the will of another who contracts with him while his mental capacity is affected by distress; if the transaction appears unconscionable, the burden of proving no undue influence is on the dominant party. Section 19A: the contract is voidable and may be set aside absolutely or, where the party has received a benefit, on just terms.',
                            f'Balwant was in severe distress; the money-lender doubled the loan in one year; Balwant actually received {R(principal)}.',
                            'The bond appears unconscionable, so the money-lender must prove he did not use undue influence — which he cannot. Balwant has received a benefit, so the court will set the bond aside on terms: repayment of the principal with fair interest.',
                            f'Balwant must repay {R(fair)} (principal {R(principal)} + interest at {rate}%), not ₹1,60,000.'),
                      wn('Working', f'{R(principal)} + {R(principal)} × {rate}% = {R(fair)}.')],
         'checks': cu},
        {'id': 'i4', 'title': 'Non-compete after the sale of a business', 'difficulty': 'moderate', 'minutes': 7,
         'q': 'Nikhil sells his bakery in Indore along with its goodwill to Arora Foods and agrees not to run a bakery within 5 km of the shop for 4 years. Separately, Nikhil\'s former employee Sameer had agreed in his appointment letter not to work for any bakery anywhere in India for 3 years after leaving. Are these restraints valid?',
         'solution': [legal('Section 27: an agreement in restraint of a lawful trade, profession or business is void to that extent. Exception: when goodwill is sold, the seller may promise the buyer not to run a similar business within stated local limits while the buyer runs such a business there, if those limits are reasonable.',
                            'Nikhil sold goodwill and accepted a 5 km, 4-year restriction. Sameer\'s restriction applies after his employment ends, all over India.',
                            'Nikhil\'s restraint falls within the sale-of-goodwill exception and is limited to a reasonable area and period. Sameer\'s restraint operates after the service has ended; post-employment restraints are not saved by any exception.',
                            'Nikhil\'s non-compete is valid and enforceable; Sameer\'s is void.')]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'KYC fails: the customer is a minor', 'role': 'CA in industry — credit controller of an electronics retailer', 'situation': 'A store sold a ₹70,000 laptop on an EMI plan. The buyer has defaulted and turns out to be 17.',
         'steps': ['The EMI agreement is void — no personal claim against the buyer.', 'Check whether the laptop could be a necessary for this buyer (unlikely at that price unless required for studies and no other supply).', 'If not a necessary, recovery depends on getting the goods back, not on the contract.', 'Fix the process: verify age in KYC before approving credit; require a guardian or adult co-applicant (an adult co-borrower or surety is liable).'],
         'takeaway': 'Lending to a minor is lending without a contract.', 'think': 'If the boy\'s father had signed as guarantor, could the store recover from the father?',
         'answer': 'Yes — an adult surety for a minor is personally liable under his own contract of guarantee.'},
        {'id': 'j2', 'title': 'Unusual payments in the ledger', 'role': 'Statutory audit senior', 'situation': 'You find a "consultancy fee" of ₹5 lakh paid to a person who promised to get the company empanelled with a government department through "contacts".',
         'steps': ['The object — influencing a public office — is opposed to public policy and unlawful (Section 23).', 'The agreement is void; the company cannot enforce it, and the payment may also be an offence.', 'Report to management and consider reporting obligations under auditing standards and company law.'],
         'takeaway': 'Section 23 is not only a law exam topic — it is a fraud-risk indicator in audit.'},
        {'id': 'j3', 'title': 'Contract signed after a threat', 'role': 'CA advising an MSME', 'situation': 'A transporter holding the client\'s goods refuses to release them unless the client signs a revised rate agreement 30% higher. The client signs.',
         'steps': ['Unlawfully detaining property to force an agreement is coercion (Section 15).', 'The revised agreement is voidable at the client\'s option (Section 19); excess amounts paid can be recovered (Section 72).', 'The client must act promptly — delay or acceptance of benefits may be treated as affirmation.'],
         'takeaway': 'Act quickly and keep evidence — the right to avoid can be lost by conduct.'},
    ]

    mcqs = [
        Q('m1', 'A person domiciled in India attains majority on completing:', ['18 years', '21 years', '16 years', '25 years'], 0, 'Indian Majority Act, 1875.', 'c1', check='18'),
        Q('m2', 'An agreement with a minor is:', ['Void ab initio', 'Voidable at the minor\'s option', 'Valid', 'Illegal'], 0, 'Mohori Bibi v. Dharmodas Ghose.', 'c2'),
        Q('m3', 'For necessaries supplied to a minor, the supplier is:', ['Entitled to be reimbursed from the minor\'s property', 'Entitled to sue the minor personally', 'Entitled to sue the minor\'s parents', 'Not entitled to anything'], 0, 'Section 68 — reimbursement from the property, not personal liability.', 'c2'),
        Q('m4', 'A minor may:', ['Be admitted to the benefits of a partnership with the consent of all partners', 'Become a full partner', 'Be declared insolvent', 'Ratify his agreement on majority'], 0, 'A minor cannot be a partner or insolvent and cannot ratify.', 'c2', 'moderate'),
        Q('m5', 'A patient who is usually of unsound mind but has lucid intervals:', ['May contract during a lucid interval', 'Can never contract', 'Can contract only through a court', 'Can contract only for necessaries'], 0, 'Section 12.', 'c3'),
        Q('m6', 'Two persons consent when they agree upon:', ['The same thing in the same sense', 'Different things', 'The same thing in different senses', 'The price only'], 0, 'Section 13 — consensus ad idem.', 'c4'),
        Q('m7', 'Consent obtained by coercion makes the contract:', ['Voidable at the option of the coerced party', 'Void', 'Illegal', 'Valid'], 0, 'Section 19.', 'c5'),
        Q('m8', 'A threat to commit suicide to obtain a release deed amounts to:', ['Coercion', 'Undue influence', 'Misrepresentation', 'No vitiating factor'], 0, 'Suicide is an act forbidden by penal law; threatening it to obtain consent is coercion.', 'c5', 'moderate'),
        Q('m9', 'Which relationship is NOT presumed to give a position to dominate the will under Section 16?', ['Two strangers bargaining at a market', 'Doctor and patient', 'Guardian and ward', 'Spiritual adviser and disciple'], 0, 'Undue influence needs a relationship of authority, fiduciary character or impaired capacity.', 'c6'),
        Q('m10', 'Which of the following is NOT fraud under Section 17?', ['An honest but mistaken statement believed to be true', 'Active concealment of a fact', 'A promise made without intention of performing it', 'A false statement made knowingly'], 0, 'An honest false statement is misrepresentation (Section 18), not fraud.', 'c7'),
        Q('m11', 'Mere silence as to facts amounts to fraud when:', ['There is a duty to speak', 'The buyer does not ask', 'The goods are cheap', 'Never, in any situation'], 0, 'Explanation to Section 17 — also where silence is equivalent to speech.', 'c7', 'moderate'),
        Q('m12', 'Damages are generally NOT available for:', ['Innocent misrepresentation', 'Fraud', 'Breach of contract', 'Wrongful dishonour of a cheque'], 0, 'For misrepresentation the remedy is rescission (or affirmation).', 'c8', 'moderate'),
        Q('m13', 'A agrees to buy a cargo that, unknown to both, had sunk before the agreement. The agreement is:', ['Void — bilateral mistake of fact', 'Voidable at A\'s option', 'Valid — A bears the risk', 'Illegal'], 0, 'Section 20 — mistake as to existence of the subject-matter.', 'c9'),
        Q('m14', 'A party cannot avoid a contract on the ground of a mistake about:', ['Indian law', 'Foreign law', 'Existence of the subject-matter, shared by both parties', 'Identity of the subject-matter, shared by both parties'], 0, 'Section 21 — ignorance of the law of the land is no excuse; foreign law is treated as fact.', 'c9'),
        Q('m15', 'An agreement to pay a fee to a person for arranging a marriage is:', ['Void — opposed to public policy', 'Valid', 'Voidable', 'Valid if in writing'], 0, 'Marriage brokerage agreements are void under Section 23.', 'c10'),
        Q('m16', 'Under Section 24, where part of a single consideration is unlawful and cannot be separated:', ['The whole agreement is void', 'Only the unlawful part is void', 'The agreement is voidable', 'The lawful part is always enforceable'], 0, 'Lawful parts are enforced only where severable.', 'c10', 'moderate'),
        Q('m17', 'Which agreement in restraint of trade is valid?', ['A seller of goodwill agreeing not to compete within reasonable local limits', 'An employee agreeing never to work in the same industry after leaving', 'Traders agreeing that one of them will close down for money', 'A doctor agreeing never to practise anywhere'], 0, 'Exception to Section 27.', 'c11'),
        Q('m18', 'An agreement to refer future disputes to arbitration is:', ['Valid, if in writing', 'Void under Section 28', 'Void under Section 27', 'Voidable'], 0, 'An exception to Section 28.', 'c11', 'moderate'),
        Q('m19', 'Which of these is a wagering agreement?', ['A bet on the result of a cricket match', 'A contract of fire insurance', 'A chit fund', 'A share purchase intended to be settled by delivery'], 0, 'Insurance, chit funds and genuine commercial transactions are not wagers.', 'c11'),
        Q('m20', 'An agreement restraining the marriage of a major person is:', ['Void — Section 26', 'Valid', 'Voidable', 'Void only if oral'], 0, 'Section 26 saves only restraints on the marriage of a minor.', 'c11'),
    ]

    questions = [
        {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'legal',
         'q': 'Arnav, aged 17, borrowed ₹1,20,000 from Mr. Kohli by mortgaging his share in a house, falsely stating that he was 19. On attaining majority he refused to repay, pleading minority. Mr. Kohli argues that (i) Arnav should be stopped from pleading minority since he lied about his age, and (ii) at least the money should be refunded. Decide.',
         'model': [legal('Section 11: a minor is not competent to contract; an agreement with a minor is void ab initio (Mohori Bibi v. Dharmodas Ghose). A minor can always plead minority, even where he misrepresented his age — the rule of estoppel does not apply against a minor. Since the agreement is void, the minor cannot be made to repay the loan or compensate the lender. Under the doctrine of restitution, however, if the money or property obtained by the misrepresentation is still traceable in the minor\'s hands (not spent), the court may order him to restore it.',
                         'Arnav was 17 when he mortgaged his share and took ₹1,20,000, falsely claiming to be 19.',
                         '(i) The mortgage and loan agreement were void from the start. A false statement of age does not make a minor competent, so Arnav is not estopped and may plead minority. (ii) Mr. Kohli cannot recover the loan as a debt or claim compensation. Only if the ₹1,20,000 (or what it was used to buy) is still traceable with Arnav can the court direct him to restore it; money already spent cannot be recovered.',
                         'Arnav is not liable to repay the loan, and the mortgage is void. Argument (i) fails. Argument (ii) succeeds only to the extent that the money is still traceable in Arnav\'s hands.')],
         'scheme': [S('s1', 'Section 11 — minor incompetent; agreement void ab initio', 1.5, 'provision'), S('s2', 'Mohori Bibi v. Dharmodas Ghose cited', 1, 'provision'), S('s3', 'Minor can plead minority despite misrepresenting age', 1.5, 'analysis'), S('s4', 'No repayment or compensation; restitution only of traceable benefit', 1, 'analysis'), S('s5', 'Conclusion', 1, 'conclusion')],
         'remarks': ['This is the Mohori Bibi fact pattern; examiners expect the case name, the no-estoppel point and the limited restitution point (only what is still traceable with the minor).'],
         'mistakes': ['Saying the contract is voidable at the minor\'s option.', 'Applying estoppel against the minor.', 'Saying the minor may ratify on attaining majority.', 'Saying the minor must refund the loan in every case — restitution applies only to money or property still traceable with him.'],
         'tips': ['Deal with each of the lender\'s arguments separately in the analysis.']},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
         'q': 'Distinguish between coercion and undue influence.',
         'model': [cvu],
         'scheme': [S('s1', 'Nature of pressure', 1, 'concept'), S('s2', 'Relationship requirement', 1, 'concept'), S('s3', 'Who can use it / object', 1, 'concept'), S('s4', 'Effect with sections (19, 19A, 72)', 1, 'provision')],
         'remarks': ['Four clear bases with section numbers score full marks.'], 'mistakes': ['Calling undue influence "void".'], 'tips': ['Put section numbers in the heading row.']},
        {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'What is a wagering agreement? State its essentials and name two transactions that resemble wagers but are not wagers.',
         'model': [p('Section 30 declares agreements by way of wager void. A wager is a promise to pay money or money\'s worth on the determination of an uncertain future event, where each party may win or lose depending on the outcome and neither has any interest in the event apart from the stake.'),
                   ul(['A promise to pay money or money\'s worth.', 'The promise depends on an uncertain event.', 'Mutual chances of gain or loss for the parties.', 'Common intention to bet at the time of the agreement.', 'Neither party controls the event.', 'No interest in the event other than the stake (no insurable interest).']),
                   p('Not wagers: (i) contracts of insurance — the insured has an insurable interest and the contract indemnifies loss; (ii) chit funds; also genuine share or commodity transactions intended to be settled by delivery, and competitions involving skill.')],
         'scheme': [S('s1', 'Meaning with Section 30', 1, 'provision'), S('s2', 'Essentials (any five)', 2.5, 'concept'), S('s3', 'Two non-wager transactions with reason', 1.5, 'application')],
         'remarks': ['A reason must accompany each non-wager example.'], 'mistakes': ['Listing insurance as a wager.', 'Listing a lottery as a game of skill.'], 'tips': ['Number the essentials.']},
        {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'legal',
         'q': 'Kunal agrees to buy from Tanvi a painting that both believe to be by a famous artist. In fact it is a copy. Separately, Raj buys a plot believing (wrongly, and without asking) that a highway will pass next to it; the seller knew nothing of Raj\'s belief. Advise Kunal and Raj.',
         'model': [legal('Section 20: where both parties are under a mistake of fact essential to the agreement, the agreement is void. Section 22: a contract is not voidable merely because one party was under a mistake of fact.',
                         'Kunal and Tanvi both believed the painting was an original. Only Raj held the mistaken belief about the highway; the seller neither shared nor induced it.',
                         'For the painting, both parties were mistaken about the quality and identity of the subject-matter, which was essential — a bilateral mistake. Raj\'s mistake was unilateral and not caused by the seller.',
                         'The agreement for the painting is void; Kunal can recover any price paid. Raj\'s contract is valid and binding on him.')],
         'scheme': [S('s1', 'Section 20 bilateral mistake', 1, 'provision'), S('s2', 'Section 22 unilateral mistake', 1, 'provision'), S('s3', 'Application to both facts', 1, 'analysis'), S('s4', 'Conclusions', 1, 'conclusion')],
         'remarks': ['Separate the two fact situations clearly.'], 'mistakes': ['Calling a bilateral mistake "voidable".'], 'tips': ['Use "Part (a)" and "Part (b)" sub-headings in Analysis.']},
    ]

    viva = [
        V('v1', 'What is the legal position of an agreement with a minor?',
          'An agreement with a minor is void ab initio, as held in Mohori Bibi versus Dharmodas Ghose. The minor cannot ratify it on attaining majority. For necessaries supplied to him, the supplier is reimbursed from the minor\'s property under Section 68, but the minor is not personally liable.',
          [P('p1', 'Void from the beginning (Mohori Bibi v. Dharmodas Ghose)', 4, 'void ab initio|void abinitio|void from the beginning|void from the start|void from start|absolutely void|altogether void|completely void|totally void|mohori|dharmodas|void from inception'),
           P('p2', 'Cannot be ratified on attaining majority', 3, 'cannot ratif|cannot be ratif|can not ratif|not ratif|no ratif|cannot confirm|not be ratif|not possible to ratif|ratification is not|ratification not'),
           P('p3', 'Necessaries — reimbursed from his property (Section 68), not personally liable', 3, 'necessar|section 68')], 'c2'),
        V('v2', 'Define coercion under Section 15.',
          'Coercion means committing, or threatening to commit, an act forbidden by the penal law, or unlawfully detaining, or threatening to detain, someone\'s property, with the intention of making a person enter into an agreement. A contract caused by coercion is voidable at the option of the coerced party.',
          [P('p1', 'Committing or threatening an act forbidden by penal law', 3, 'forbidden|penal|criminal|crime|offence|illegal act|unlawful act|bns|ipc|nyaya'),
           P('p2', 'Unlawfully detaining or threatening to detain property', 3, 'detain|detention|withhold|holding property|hold property|keep property|keeping property'),
           P('p3', 'Intention of making a person enter into an agreement', 2, 'enter into agreement|enter into an agreement|enter into contract|into agreement|enter agreement|make contract|make agreement|sign agreement|sign the agreement|sign contract|to contract|intention'),
           P('p4', 'Voidable at the option of the coerced party', 2, 'voidable')], 'c5'),
        V('v3', 'When is a contract said to be induced by undue influence?',
          'When one party, because of their relationship, can dominate the other\'s will, and uses that power to obtain an unfair advantage. Such a position is presumed where there is real or apparent authority, a fiduciary relation, or the other party\'s mental capacity is affected by age, illness or distress. The contract is voidable under Section 19A.',
          [P('p1', 'One party can dominate the other\'s will', 4, 'dominate|domination|dominant|control the will|control will|position of power|power over'),
           P('p2', 'Uses that position to obtain an unfair advantage', 3, 'unfair advantage|undue advantage|take advantage|takes advantage|taking advantage|misuse|abuse|exploit|unfairly'),
           P('p3', 'Presumed cases: authority, fiduciary relation, impaired mental capacity', 1, 'authority|fiduciary|trust|age|illness|distress|doctor|guardian|teacher|employer', min=1),
           P('p4', 'Voidable (Section 19A)', 2, 'voidable|19a|19 a|set aside')], 'c6'),
        V('v4', 'Does mere silence amount to fraud?',
          'No, mere silence is not fraud. It becomes fraud only where there is a duty to speak, for example in a fiduciary relationship or a contract of utmost good faith, or where the silence is in itself equivalent to speech.',
          [P('p1', 'Mere silence is not fraud', 4, 'silence is not fraud|silence not fraud|silence is not a fraud|not fraud|not a fraud|is not fraud|does not amount|not amount|silence alone is not|no fraud|mere silence not|not always fraud|not necessarily fraud|not by itself fraud|silence by itself is not'),
           P('p2', 'Unless there is a duty to speak', 3, 'duty to speak|duty speak|duty to disclose|duty disclose|bound to speak|bound to disclose|obliged to speak|obliged to disclose|obligation to disclose|obligation to speak|utmost good faith|fiduciary'),
           P('p3', 'Or the silence is equivalent to speech', 3, 'equivalent to speech|equivalent speech|silence itself speech|amounts to speech|same as speech|equal to speech|like speech|as good as speech|silence is speech|silence speaks|silence itself equivalent|equivalent to saying')], 'c7'),
        V('v5', 'Distinguish between fraud and misrepresentation.',
          'In fraud the false statement is made knowingly, with intention to deceive. In misrepresentation the person making it honestly believes it to be true, so there is no intention to deceive. In fraud the aggrieved party can claim damages as well as rescind, while for misrepresentation the remedy is generally only rescission.',
          [P('p1', 'Fraud: made knowingly with intent to deceive', 4, 'fraud made knowingly|fraud knowingly|fraud statement made knowingly|fraud false statement made knowingly|fraud intent|fraud intention|fraud statement made knowing|fraud made knowing|fraud knowing|fraud know|fraud deliberat|fraud wilful|fraud willful|fraud dishonest|fraud deceiv|fraud purpose|fraud on purpose|fraud conscious|fraud aware|fraud false statement made knowing|fraud is intentional|fraud there is intention|fraud is deliberate'),
           P('p2', 'Misrepresentation: honest belief, no intent to deceive', 3, 'misrepresent innocent|misrepresent honest|misrepresent believ|misrepresent without intent|misrepresent no intent|misrepresent not intent|misrepresent unintent|misrepresent good faith|misrepresent bona fide|misrepresent think|misrepresent thinks|misrepresent person believ|misrepresent maker believ|misrepresent there is no intent|misrepresent is innocent|misrepresent is unintentional|misrepresent is honest'),
           P('p3', 'Damages available for fraud; misrepresentation — generally rescission only', 3, 'fraud damag|fraud also damag|fraud claim damag|fraud sue damag|fraud compens|fraud can claim damag|fraud entitl damag|fraud recover damag|fraud party claim damag|fraud party can claim|fraud aggrieved party claim|fraud aggrieved party can claim|fraud victim claim|fraud rescind and claim|fraud rescission and damag|fraud rescind damag|fraud both|only rescission|rescission only|only rescind|no damag')], 'c8'),
        V('v6', 'What is a wagering agreement, and is it valid?',
          'A wagering agreement is a promise to pay money, or something worth money, depending on an uncertain future event, where each party may win or lose and neither has any interest except the stake. Under Section 30 it is void. Insurance contracts and chit funds are not wagers.',
          [P('p1', 'Promise to pay money on an uncertain future event', 3, 'uncertain|uncertain event|chance|future event'),
           P('p2', 'Each party stands to win or lose; no interest other than the stake', 3, 'win or lose|win lose|gain or lose|gain or loss|win or loss|lose or win|stake|no interest|bet'),
           P('p3', 'Void under Section 30', 4, 'void|void section 30|section 30 void|void under section 30|section 30 declares void')], 'c11'),
        V('v7', 'Is an agreement in restraint of trade valid? State the exceptions.',
          'Under Section 27 an agreement in restraint of trade is void to that extent. The exceptions are: a seller of goodwill may agree not to carry on a similar business within reasonable local limits, and under the Partnership Act partners may agree not to compete during the partnership, and an outgoing partner may agree not to compete within a reasonable period or area.',
          [P('p1', 'Void under Section 27', 4, 'void|void section 27|section 27 void|void under section 27'),
           P('p2', 'Exception: sale of goodwill within reasonable local limits', 4, 'goodwill'),
           P('p3', 'Exception: partners under the Partnership Act', 2, 'partner|partnership')], 'c11'),
        V('v8', 'What is the effect of a mistake on a contract?',
          'If both parties are under a mistake of fact essential to the agreement, that is, a bilateral mistake, the agreement is void under Section 20. A unilateral mistake, where only one party is mistaken, does not make the contract voidable under Section 22. A mistake of Indian law gives no relief, but a mistake of foreign law is treated as a mistake of fact.',
          [P('p1', 'Bilateral mistake of essential fact — agreement void (Section 20)', 4, 'bilateral void|bilateral mistak void|bilateral mistak agreement void|bilateral mistak fact void|bilateral mistak fact agreement void|bilateral mistak makes void|bilateral mistak make void|bilateral mistak render void|bilateral mistak contract void|bilateral agreement void|bilateral contract void|both party mistak void|both party mistak agreement void|both party mistak contract void|both party mistak fact void|both party mistak fact agreement void|both party mistaken fact void|void if both|void when both|void where both|mutual mistak void|mutual mistak agreement void|section 20'),
           P('p2', 'Unilateral mistake — contract not voidable (Section 22)', 4, 'unilateral not voidabl|unilateral not void|unilateral does not|unilateral mistak does not|unilateral mistak not|unilateral mistak valid|unilateral valid|unilateral contract valid|unilateral no effect|unilateral mistak no effect|unilateral binding|unilateral mistak binding|one party mistak not|one party mistak valid|one party mistak contract valid|only one party mistak not|only one party mistak contract valid|section 22'),
           P('p3', 'Mistake of Indian law — no relief; foreign law treated as fact', 2, 'indian law|foreign law|mistake of law|law of the land|ignorance of law')], 'c9'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Trouble at Zoya\'s boutique', 'difficulty': 'hard',
        'case': ('Zoya, 16, lives with her aunt and has money in a savings account left by her late parents. A coaching centre enrolled her and billed a tuition fee of ₹4,500; an optician supplied spectacles worth ₹3,000; a jeweller sold her a diamond pendant for ₹60,000 on credit — none paid. '
                 'Separately, Zoya\'s aunt, who manages her money, persuaded Zoya on her 18th birthday to gift her half the savings, while Zoya was recovering from a serious illness. '
                 'A neighbour also offered Zoya ₹2,000 if she would never marry.'),
        'mcqs': [
            M('k1a', 'How much can the suppliers together recover from Zoya\'s savings?', [R(k_nec), R(67500), R(63000), 'Nothing'], 0,
              f'Section 68 — only necessaries suited to her condition: tuition ₹4,500 + spectacles ₹3,000 = {R(k_nec)}. The pendant is a luxury; the agreement is void.', 'hard', '4500+3000'),
            M('k1b', 'Can the jeweller sue Zoya personally for ₹60,000?', ['No — the agreement is void and the pendant is not a necessary', 'Yes — she enjoyed the benefit', 'Yes — after she turns 18 she must ratify it', 'Yes, but only for half the price'], 0, 'Mohori Bibi; no personal liability and no ratification.', 'moderate'),
            M('k1c', 'The gift to the aunt is likely to be:', ['Voidable for undue influence — the aunt was in a fiduciary position and Zoya\'s capacity was affected by illness', 'Void for coercion', 'Valid — Zoya was a major', 'Void for bilateral mistake'], 0, 'Section 16 presumes domination in fiduciary relations and where capacity is affected by illness; Section 19A makes it voidable.', 'hard'),
            M('k1d', 'The neighbour\'s offer, if accepted after Zoya turns 18, is:', ['Void — agreement in restraint of marriage (Section 26)', 'Valid', 'Voidable', 'Void — wagering agreement'], 0, 'Every agreement restraining the marriage of a person other than a minor is void.', 'core'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch02', 'n': 3, 'title': 'Other Essential Elements of a Contract',
        'outcomes': ['Determine capacity to contract under Sections 11 and 12, and apply the 15 rules on minors\' agreements including Section 68.', 'Explain free consent and identify coercion, undue influence, fraud, misrepresentation and mistake, with their legal effects (Sections 13–22).',
                     'Test whether the object and consideration of an agreement are lawful under Sections 23 and 24, including agreements opposed to public policy.', 'Identify agreements expressly declared void — restraint of marriage, trade and legal proceedings, uncertain and wagering agreements (Sections 26–30).'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 60, 'practice': 60}, 'prereq': ['fnd-p2-ch02-u02'],
                 'exam_tip': 'Minor\'s agreements, fraud by silence, undue influence and restraint of trade are favourite problem areas. Always state whether the agreement is void or voidable — that word alone often decides the marks.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {'summary': ['Competent = major (18), sound mind (Section 12), not disqualified (Section 11). Minor\'s agreement void ab initio (Mohori Bibi); no ratification; Section 68 necessaries from property.',
                                 'Free consent (Section 14): no coercion (15), undue influence (16), fraud (17), misrepresentation (18), mistake (20–22).',
                                 'Coercion, fraud, misrepresentation → voidable (Section 19); undue influence → voidable, may be set aside on terms (19A); bilateral mistake of fact → void (20); unilateral → valid (22); mistake of Indian law → no relief (21).',
                                 'Silence is not fraud unless duty to speak or silence equals speech. Fraud = intent to deceive (damages too); misrepresentation = innocent (rescission).',
                                 'Section 23: unlawful object/consideration — forbidden by law, defeats law, fraudulent, injurious, immoral, against public policy → void. Section 24: unlawful in part → void unless severable.',
                                 'Void: restraint of marriage (26), trade (27, goodwill & partnership exceptions), legal proceedings (28, arbitration exception), uncertainty (29), wager (30), impossible act (56).'],
                     'remember': ['Sections: 11 competence · 12 sound mind · 13 consent · 14 free consent · 15 coercion · 16 undue influence · 17 fraud · 18 misrepresentation · 19/19A effects · 20–22 mistake · 23–24 legality · 26–30 void agreements · 68 necessaries · 72 money paid under coercion.'],
                     'traps': ['Minor\'s agreement is VOID, not voidable.', 'Coercion can be by a stranger against a stranger; undue influence needs a relationship.', 'Insurance and chit funds are not wagers.', 'Non-compete during employment is valid; after employment it is void.']},
        'quickref': [{'k': 'Section 11', 'v': 'Major · sound mind · not disqualified'}, {'k': 'Section 68', 'v': 'Necessaries to minor/lunatic — reimbursed from their property'},
                     {'k': 'Section 15 coercion', 'v': 'Threat of act forbidden by penal law or unlawful detention of property'}, {'k': 'Section 16 undue influence', 'v': 'Position to dominate will + unfair advantage'},
                     {'k': 'Section 17 / 18', 'v': 'Fraud (intent to deceive) / misrepresentation (innocent)'}, {'k': 'Sections 19 / 19A / 20', 'v': 'Voidable / voidable on terms / void (bilateral mistake)'},
                     {'k': 'Section 23', 'v': 'Unlawful object or consideration → void'}, {'k': 'Sections 26–30', 'v': 'Restraint of marriage, trade, legal proceedings; uncertainty; wager → void'},
                     {'k': 'Leading cases', 'v': 'Mohori Bibi v. Dharmodas Ghose · State of Bombay v. R.M.D. Chamarbaugwala'}],
        'viva': viva, 'cases': cases,
    }
