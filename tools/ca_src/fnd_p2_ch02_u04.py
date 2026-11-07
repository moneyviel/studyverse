"""CA Foundation · Paper 2 Business Laws · Chapter 2 The Indian Contract Act, 1872 · Unit 4 Performance of Contract.
Original explanations and problems; sections are cited by number; all figures computed below."""
from lib import *
from ca_viva import P, ALT, V
from ca_cases import M

UID = 'fnd-p2-ch02-u04'


def Q(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check: d['check'] = check
    return d


def S(sid, pt, m, skill): return {'id': sid, 'pt': pt, 'm': m, 'skill': skill}


def build():
    # ---- Illustration 1: joint promisors, one insolvent (Section 43) ----
    c1 = Checks()
    debt = 450000
    share = c1.add('450000/3', 'equal share of each joint promisor')
    from_a = c1.add('150000*40/100', 'recovered from A\'s insolvent estate (40% of A\'s share)')
    short = c1.add('150000-60000', 'shortfall in A\'s contribution')
    each_short = c1.add('90000/2', 'shortfall borne equally by B and C')
    from_b = c1.add('150000+45000', 'C recovers from B')
    c_bears = c1.add('150000+45000', 'loss finally borne by C')
    tot = c1.add('60000+195000+195000', 'proof: contributions add up to the debt')

    # ---- Illustration 2: appropriation where neither party appropriates (Section 61) ----
    c2 = Checks()
    d1, d2, d3, pay = 30000, 45000, 25000, 60000
    to_d1 = c2.add('30000', 'applied to debt 1 (oldest, though time-barred)')
    to_d2 = c2.add('60000-30000', 'balance applied to debt 2')
    left_d2 = c2.add('45000-30000', 'debt 2 still outstanding')
    left_tot = c2.add('15000+25000', 'total still outstanding after the payment')

    # ---- Section 41 part payment by a stranger ----
    c3 = Checks()
    s41 = c3.add('200000-120000', 'balance B can still claim from A')

    # ---- Question 1 figures ----
    cq = Checks()
    q_share = cq.add('360000/3', 'equal share of X, Y and Z')
    q_from_z = cq.add('120000*25/100', 'Y recovers from Z\'s insolvent estate (25%)')
    q_short = cq.add('120000-30000', 'Z\'s shortfall')
    q_from_x = cq.add('120000+90000/2', 'Y recovers from X: own share + half the shortfall')
    q_y_bears = cq.add('120000+45000', 'Y finally bears')
    q_proof = cq.add('165000+165000+30000', 'proof: X + Y + Z\'s estate = debt')

    # ---- Question 2 figures (appropriation) ----
    cq2 = Checks()
    a1, a2, a3 = 18000, 32000, 20000
    q2_p1, q2_p2 = 24000, 40000
    q2_r1 = cq2.add('32000-24000', 'debt 2 left after the cheque the debtor earmarked for it')
    q2_after1 = cq2.add('40000-18000', 'second cheque: oldest debt 1 cleared, remainder carried on')
    q2_after2 = cq2.add('22000-8000', 'then the balance of debt 2 is cleared')
    q2_left3 = cq2.add('20000-14000', 'debt 3 left outstanding')

    # ---- case figures ----
    cc = Checks()
    k_pay_first = cc.add('50000', 'old debt cleared first')
    k_left = cc.add('50000+70000+30000-100000', 'total still due after ₹1,00,000 paid')

    tender = table(['Condition', 'Meaning / example'], [
        ['Unconditional', 'Offering to repay a loan only if the lender returns an unrelated document is not a valid tender'],
        ['Whole obligation', 'Offering 80 of 100 bags, or the principal without the interest due, is not a valid tender'],
        ['Proper time and place', 'Delivery at midnight, or at a place other than agreed, is not valid unless so agreed'],
        ['Reasonable opportunity to inspect', 'The promisee must be able to check the goods are as contracted (quality and quantity)'],
        ['To the proper person', 'Made to the promisee or his authorised agent; tender to one of several joint promisees is enough'],
        ['By a person able and willing', 'The promisor must be in a position to perform at that moment'],
    ], title='A valid tender (offer to perform)')

    time_tbl = table(['Section', 'Situation', 'Rule'], [
        ['46', 'No application needed; no time fixed', 'Perform within a reasonable time (a question of fact)'],
        ['47', 'Day fixed; no application needed', 'Perform on that day during usual business hours, at the proper place'],
        ['48', 'Day fixed; promisee must apply', 'Promisee must apply at a proper place within usual business hours'],
        ['49', 'No application needed; no place fixed', 'Promisor must ask the promisee to appoint a reasonable place and perform there'],
        ['50', 'Promisee prescribes or approves a manner or time', 'Performance in that manner or at that time is good performance'],
    ], title='Time and place of performance (Sections 46–50)')

    recip = table(['Section', 'Rule'], [
        ['51', 'Simultaneous reciprocal promises: a promisor need not perform unless the promisee is ready and willing to perform'],
        ['52', 'Perform in the order fixed by the contract; if none, in the order the nature of the transaction requires'],
        ['53', 'A party who is prevented from performing by the other may choose to avoid the contract, and may claim compensation'],
        ['54', 'If the party who must perform first fails, he cannot claim the other\'s performance and must compensate the other'],
        ['55', 'Time of essence: failure makes the contract voidable at the promisee\'s option. Not of essence: not voidable, but compensation for loss. Accepting late performance bars compensation unless notice is given at the time of acceptance'],
        ['56', 'Agreement to do an impossible act is void; a contract becomes void when performance later becomes impossible or unlawful; a promisor who knew (or should have known) of the impossibility must compensate the promisee who did not'],
        ['57', 'Reciprocal promises to do legal things and also illegal things: the legal part is a valid contract, the illegal part is void'],
        ['58', 'Alternative promise with one branch illegal: only the legal branch can be enforced'],
    ], title='Reciprocal promises (Sections 51–58)')

    concepts = [
        {'id': 'c1', 'title': 'Performance — Section 37; actual and attempted', 'body': [
            'Performance means carrying out the obligations under the contract. Section 37: the parties must perform, or offer to perform, their respective promises, unless performance is dispensed with or excused under the Contract Act or any other law.',
            'Actual performance: the promisor does exactly what he undertook, at the time and in the manner agreed (e.g. a borrower repays on the due date). The obligation is discharged.',
            'Attempted performance (tender): the promisor offers to perform, but the promisee refuses. Under Section 38, when a proper offer to perform is turned down, the promisor is not liable for the failure to perform, and his own rights under the contract remain intact.',
            'Section 37 also binds the promisor\'s legal representatives after his death, unless the contract shows a contrary intention (e.g. it depends on personal skill).'],
         'blocks': [tender],
         'analogy': 'Tender is knocking on the door with the goods in hand at the agreed hour. If the buyer refuses to open, the seller has done his part.',
         'work': 'Where a customer refuses delivery, a finance controller asks the logistics team for proof of a valid tender (time, place, full quantity, chance to inspect) before booking a claim against the customer.'},
        {'id': 'c2', 'title': 'By whom must a contract be performed? (Sections 40–42)', 'body': [
            'Promisor himself (Section 40): where the parties intended personal performance — contracts involving personal skill, taste or confidence (a portrait, a concert, a surgery) — only the promisor can perform.',
            'Agent: where personal skill is not the basis, the promisor (or his representative) can get the work done through any capable person.',
            'Legal representatives: on the promisor\'s death, contracts not depending on personal skill bind his legal representatives — but only up to the value of the estate they inherit. A personal-skill contract ends on the promisor\'s death.',
            'Third person (Section 41): once the promisee has accepted performance from an outsider, he loses the right to demand it again from the promisor — the promisor stands discharged to that extent, even if he never authorised the third person.',
            'Joint promisors (Section 42): unless the contract says otherwise, joint promisors must perform jointly during their lives; after one dies, his legal representative performs jointly with the survivors; after the last survivor dies, the representatives of all must perform.'],
         'analogy': 'If you hire a famous singer, you get the singer — not her cousin. If you order cement, any reliable delivery van will do.',
         'work': 'On a partner\'s death, a CA checks which of the firm\'s contracts depend on that partner\'s personal skill (they end) and which bind his estate (they continue).'},
        {'id': 'c3', 'title': 'Succession vs assignment', 'body': [
            'Succession is transfer by operation of law (e.g. on death): both rights and liabilities pass to the legal heirs, but liabilities only up to the value of the property inherited. A son inheriting ₹10 lakh of assets is not liable for his father\'s debts beyond ₹10 lakh.',
            'Assignment is transfer by act of the parties: only the benefit (rights) of a contract can be assigned — a creditor may assign a debt, and the assignee can recover it from the debtor. Liabilities cannot be assigned without the creditor\'s consent, since that would bring in a new debtor (which needs novation). Benefits coupled with liabilities, or founded on personal skill or confidence, cannot be assigned.'],
         'analogy': 'Succession hands over the whole bag — gifts and bills — but you never pay more bills than the gifts are worth. Assignment hands over only the gifts.',
         'work': 'In receivable financing, a company assigns its book debts to a bank or factor — the right to collect is transferred; the company\'s own obligations to its suppliers are not.'},
        {'id': 'c4', 'title': 'Joint promisors and joint promisees (Sections 43–45)', 'body': [
            'Section 43: where several persons have promised jointly, the promisee (unless the contract says otherwise) can require any one or more of them to carry out the entire promise. Liability is therefore joint and several.',
            'Contribution: each joint promisor may compel every other to contribute equally, unless the contract shows a different intention. If one of them defaults in contributing, the others bear the loss from that default in equal shares.',
            'The rule does not stop a surety from recovering from the principal debtor what he paid, nor allow the principal to recover from the surety.',
            'Section 44: release of one joint promisor by the promisee does not discharge the others, and does not free the released promisor from his liability to the other joint promisors (for contribution).',
            'Section 45: when a promise is made to two or more persons jointly, the right to claim performance rests with all of them jointly during their lives; after one dies, with his representative jointly with the survivors; after the last survivor, with the representatives of all jointly.'],
         'analogy': 'Joint promisors are climbers on one rope: the creditor can pull on any one of them for the whole weight; they then settle among themselves.',
         'work': 'When a lender recovers a joint loan from one co-borrower, the CA computes that co-borrower\'s contribution claims against the others, including the loss from an insolvent co-borrower.'},
        {'id': 'c5', 'title': 'Time and place for performance (Sections 46–50)', 'body': [
            'The rules depend on whether a time or place is fixed and whether the promisee must first apply (ask) for performance. See the table.',
            'Example under Section 47: goods to be delivered "on 10 March" must be offered during usual business hours that day at the usual place; delivery tendered at 10 p.m. after the business has closed can be refused.'],
         'blocks': [time_tbl],
         'analogy': 'If no clock is set, the law reads "reasonable time"; if a day is set, it reads "business hours on that day".',
         'work': 'Cut-off for revenue recognition and penalty clauses often turns on whether delivery was tendered at the proper time and place.'},
        {'id': 'c6', 'title': 'Reciprocal promises (Sections 51–58)', 'body': [
            'Reciprocal promises are promises that form the consideration for each other. They may be mutual and concurrent (performed together — payment against delivery), mutual and dependent (one must be performed first — build the house, then get paid), or mutual and independent (each performs regardless of the other).',
            'Section 55 is very important for problems: decide first whether time was of the essence (look at the terms and the nature of the contract — e.g. seasonal goods, a fixed event). If yes, delay makes the contract voidable at the promisee\'s option; if no, the promisee only gets compensation. A promisee who accepts late performance must give notice then and there to keep his right to compensation.',
            'Section 56: initial impossibility (e.g. discovering treasure by magic) makes the agreement void. Supervening impossibility — performance becoming impossible or unlawful after the contract, by an event the promisor could not prevent (destruction of subject-matter, change of law, outbreak of war, death or incapacity in a personal contract) — makes the contract void from then. A promisor who knew, or with reasonable diligence could have known, of the impossibility must compensate a promisee who did not know.'],
         'blocks': [recip],
         'analogy': 'Reciprocal promises are a dance: who leads, who follows, and what happens if one partner never turns up.',
         'work': 'Force majeure and "time is of the essence" clauses in supply contracts are tested against Sections 55 and 56 when deliveries are delayed or become impossible.'},
        {'id': 'c7', 'title': 'Appropriation of payments (Sections 59–61)', 'body': [
            'When a debtor owes several separate debts to the same creditor and pays an amount that does not cover all of them, the payment must be adjusted (appropriated) in this order of rules:',
            'Section 59 — debtor\'s choice: if the debtor expressly says, or circumstances show, which debt the payment is for, and the creditor accepts it, it must be applied to that debt.',
            'Section 60 — creditor\'s choice: if the debtor gives no indication, the creditor is free to adjust it against any lawful debt then due and payable to him — even a debt barred by limitation. He cannot apply it to a disputed or not-yet-due debt.',
            'Section 61 — neither appropriates: the payment is applied to the debts in order of time, whether or not they are time-barred. If the debts are of equal standing, it is applied to each proportionately.'],
         'analogy': 'First the payer chooses the pocket; if he is silent, the receiver chooses; if both are silent, the oldest pocket is filled first.',
         'work': 'Receivables ageing and interest claims depend on which invoices a payment was applied to. CAs check remittance advices (debtor\'s appropriation) before allocating receipts in the ledger.'},
        {'id': 'c8', 'title': 'Contracts that need not be performed (Sections 62–67)', 'body': [
            'Section 62 — novation, rescission, alteration: where the parties agree to replace the contract with a new one, or to cancel or change it, the old contract no longer has to be performed. Novation replaces an existing contract with a new one (between the same or different parties) — it must be agreed before the time for performance expires. Alteration changes some terms between the same parties. Rescission cancels the contract (by agreement, or by the aggrieved party after breach).',
            'Section 63 — remission and waiver: a promisee may dispense with or remit performance wholly or partly, extend the time, or accept any satisfaction he thinks fit instead. Accepting a smaller sum in full settlement discharges the whole debt — even without fresh consideration.',
            'Section 64: when a person entitled to avoid a voidable contract rescinds it, the other party need not perform; the rescinding party must restore any benefit he received.',
            'Section 65: where an agreement turns out to be void, or a contract later becomes void, whoever has received a benefit under it must give it back or pay for it (e.g. an advance paid to a singer who falls ill must be refunded).',
            'Section 66: rescission of a voidable contract is communicated or revoked in the same way, and subject to the same rules, as a proposal.',
            'Section 67: if the promisee neglects or refuses to give the promisor reasonable facilities for performance, the promisor is excused for non-performance caused by it.'],
         'analogy': 'Novation is a new rule book; alteration is crossing out a few lines; rescission is tearing up the book; remission is the referee saying "that\'s enough, call it done".',
         'work': 'Debt restructuring (new lender, new terms) is novation; extending a payment date is alteration or remission; a one-time settlement for less than the dues is remission under Section 63 — each has a different accounting effect.'},
        {'id': 'c9', 'title': 'Discharge of a contract — the modes', 'body': [
            'By performance — actual or attempted (valid tender).',
            'By mutual agreement — novation, rescission, alteration, remission (Sections 62–63).',
            'By impossibility of performance — initial or supervening (Section 56).',
            'By lapse of time — if the promisee does not sue within the limitation period (generally three years for money claims under the Limitation Act, 1963), the remedy is lost.',
            'By operation of law — death (in personal contracts), insolvency, merger, unauthorised material alteration of a written document.',
            'By breach — actual or anticipatory; the injured party is discharged from his own performance and may claim damages.',
            'Also: remission (Section 63), neglect of the promisee to afford facilities (Section 67), and merger — where an inferior right and a superior right meet in the same person (a tenant who buys the house: the lease merges into ownership).'],
         'analogy': 'A contract can end because it was kept, called off, made impossible, left too late, ended by law, or broken.',
         'work': 'Before writing back a liability, the CA must identify the mode of discharge — paid, waived, settled, time-barred or otherwise — and keep evidence for it.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Joint promisors — one insolvent', 'difficulty': 'hard', 'minutes': 10,
         'q': f'A, B and C jointly promise to pay D {R(debt)}. D compels C to pay the whole amount. A becomes insolvent and his estate pays 40 paise in the rupee. How much can C recover from A\'s estate and from B, and what loss does C finally bear?',
         'solution': [legal('Section 43: the promisee may compel any one of the joint promisors to perform the whole. Each joint promisor may compel the others to contribute equally; if one defaults, the remaining promisors bear the loss from that default in equal shares.',
                            f'C paid the whole {R(debt)}. Each one\'s equal share is {R(share)}. A\'s estate can pay only 40%.',
                            'C recovers A\'s share to the extent of A\'s estate; the unpaid part of A\'s share is shared equally by B and C.',
                            f'C recovers {R(from_a)} from A\'s estate and {R(from_b)} from B, and finally bears {R(c_bears)} himself.'),
                      table(['Particulars', 'Amount (₹)'], [['Equal share of each (4,50,000 ÷ 3)', share], ['Recovered from A\'s estate (40% of 1,50,000)', from_a], ['Shortfall in A\'s share', short], ['Shortfall borne by B and C each (½)', each_short], ['C recovers from B (1,50,000 + 45,000)', from_b], ['C bears finally (1,50,000 + 45,000)', c_bears]]),
                      wn('Proof', f'A\'s estate {R(from_a)} + B {R(from_b)} + C {R(c_bears)} = {R(tot)} = debt paid.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Appropriation — neither party appropriates', 'difficulty': 'moderate', 'minutes': 8,
         'q': f'Kapil owes Mehra & Co. three separate debts: debt 1 {R(d1)} due in January 2021 (now time-barred), debt 2 {R(d2)} due in March 2024, and debt 3 {R(d3)} due in August 2025. In 2026 he sends {R(pay)} without saying which debt it is for, and Mehra & Co. also makes no appropriation. How is the payment applied?',
         'solution': [legal('Section 61: where neither the debtor nor the creditor appropriates, the payment is applied to the debts in order of time, whether or not they are barred by limitation.',
                            f'Three debts in date order: {R(d1)} (time-barred), {R(d2)}, {R(d3)}. Payment {R(pay)}; no appropriation by either side.',
                            'Apply first to the oldest debt (the time-barred debt counts), then to the next in time.',
                            f'Debt 1 is fully paid ({R(to_d1)}); {R(to_d2)} goes to debt 2, leaving {R(left_d2)} of debt 2 and the whole of debt 3 ({R(d3)}) outstanding — {R(left_tot)} in all.'),
                      table(['Debt', 'Due', 'Amount (₹)', 'Applied (₹)', 'Outstanding (₹)'], [['Debt 1 (time-barred)', 'Jan 2021', d1, to_d1, 0], ['Debt 2', 'Mar 2024', d2, to_d2, left_d2], ['Debt 3', 'Aug 2025', d3, 0, d3], ['Total', '', d1 + d2 + d3, pay, left_tot]], num=[2, 3, 4], total=True)],
         'checks': c2},
        {'id': 'i3', 'title': 'Personal-skill contract and the death of the promisor', 'difficulty': 'moderate', 'minutes': 7,
         'q': 'Ms. Rao pays a well-known sculptor ₹1,50,000 in advance for a bust of her late father. The sculptor dies before starting. Ms. Rao asks the sculptor\'s son, also a sculptor, to complete the work; alternatively she wants her advance back. Advise.',
         'solution': [legal('Section 37 and Section 40: a contract involving personal skill or founded on personal confidence must be performed by the promisor himself and comes to an end on his death; legal representatives are not bound to perform it. Section 65: when a contract becomes void, a person who received an advantage under it must restore it.',
                            'The contract was for the sculptor\'s own artistic skill. He died before performance. He had received ₹1,50,000 in advance.',
                            'The son is not bound to make the bust, and Ms. Rao cannot insist that he do so. The contract became void on the sculptor\'s death, so the advance must be restored out of his estate.',
                            'Ms. Rao cannot compel the son to complete the work, but she can recover the advance of ₹1,50,000 from the sculptor\'s legal representatives (to the extent of the estate inherited).')]},
        {'id': 'i4', 'title': 'Time of the essence — late delivery of festival stock', 'difficulty': 'moderate', 'minutes': 7,
         'q': 'Diya Crackers Ltd. agrees to deliver fireworks to a retailer "by 25 October, time being of the essence", for the Diwali season. It delivers on 3 November. The retailer accepts the goods without any comment and later claims compensation for lost Diwali sales. Decide.',
         'solution': [legal('Section 55: if time is of the essence and the promisor fails to perform in time, the contract becomes voidable at the promisee\'s option. A promisee who accepts the late performance loses his claim for compensation for the delay, unless he tells the promisor, when accepting, that he will claim it.',
                            'Time was expressly of the essence. Delivery was late. The retailer accepted the goods without giving any notice reserving a claim.',
                            'The retailer could have rejected the late delivery and avoided the contract. By accepting without notice, it lost the right to compensation for the delay.',
                            'The retailer\'s claim for compensation fails.')]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Allocating a lump-sum receipt', 'role': 'Accounts executive in a distribution company', 'situation': 'A dealer with three overdue invoices sends ₹2 lakh by NEFT with no remittance advice.',
         'steps': ['Ask the dealer whether he intends the payment for particular invoices (Section 59).', 'If he gives no indication, the company may choose — e.g. the oldest invoice, even a time-barred one (Section 60) — but not a disputed invoice.', 'Record the appropriation decision in writing and communicate it to the dealer.', 'If nobody appropriates, the law applies it in order of time (Section 61).'],
         'takeaway': 'The ledger allocation of a receipt is a legal choice — record who made it.', 'think': 'Why might a creditor prefer to apply the money to a time-barred invoice?',
         'answer': 'Because the time-barred invoice cannot be recovered through a suit; applying the receipt there keeps the newer, enforceable invoices alive for recovery.'},
        {'id': 'j2', 'title': 'One-time settlement with a customer', 'role': 'CA in industry — credit control', 'situation': 'A customer owes ₹12 lakh and offers ₹9 lakh in full and final settlement. Management agrees.',
         'steps': ['Accepting a smaller sum in satisfaction is remission under Section 63 — no fresh consideration is needed.', 'Once accepted, the balance ₹3 lakh is discharged; it cannot be claimed later.', 'Get a written settlement letter stating it is in full and final settlement.', 'Write off the ₹3 lakh with proper approval.'],
         'takeaway': 'A settlement letter is not a formality — it discharges the balance in law.'},
    ]

    mcqs = [
        Q('m1', 'Under Section 37, the parties to a contract must:', ['Perform or offer to perform their promises, unless excused by law', 'Always perform personally', 'Perform only if the court orders', 'Perform within 30 days'], 0, 'Section 37 — performance or offer to perform.', 'c1'),
        Q('m2', 'Which is NOT a requirement of a valid tender?', ['It may be for part of the obligation', 'It must be unconditional', 'It must be at the proper time and place', 'The promisee must have a reasonable chance to inspect'], 0, 'A tender must be for the whole obligation.', 'c1'),
        Q('m3', 'A promises to paint a portrait for B and dies before painting it. The contract:', ['Comes to an end; A\'s heirs are not bound', 'Must be performed by A\'s heirs', 'Must be performed by any painter B chooses at A\'s heirs\' cost', 'Becomes voidable at B\'s option'], 0, 'Personal-skill contracts end on the promisor\'s death.', 'c2'),
        Q('m4', f'A owes B ₹2,00,000. C, without A\'s knowledge, pays B ₹1,20,000 on A\'s behalf and B accepts it. B can now claim from A:', [R(s41), R(200000), R(120000), 'Nothing'], 0, 'Section 41 — accepted performance by a third person discharges the promisor to that extent.', 'c2', 'moderate', check='200000-120000'),
        Q('m5', 'Which of the following can be assigned?', ['The right to receive a debt', 'The liability to repay a loan', 'A contract to sing at a concert', 'A benefit coupled with a personal liability'], 0, 'Only benefits can be assigned; liabilities and personal contracts cannot.', 'c3'),
        Q('m6', 'X, Y and Z jointly promise to pay ₹90,000 to W. W may:', ['Compel any one of them to pay the whole ₹90,000', 'Recover only ₹30,000 from each', 'Sue only all three together', 'Recover only from the eldest'], 0, 'Section 43 — joint and several liability.', 'c4'),
        Q('m7', 'P, Q and R jointly owe ₹3,00,000. The creditor releases P. Then:', ['Q and R remain liable for the whole; P remains liable to Q and R for contribution', 'All three are discharged', 'Only P\'s share is reduced from the debt', 'P is free from every liability'], 0, 'Section 44.', 'c4', 'moderate'),
        Q('m8', 'A, B and C jointly owe ₹4,50,000. C pays it all; A is insolvent and his estate pays 40 paise in the rupee. C can recover from B:', [R(from_b), R(150000), R(225000), R(90000)], 0, 'B\'s own share ₹1,50,000 + half of A\'s shortfall ₹45,000.', 'c4', 'hard', check='150000+90000/2'),
        Q('m9', 'Where no time is fixed and no application is needed, a promise must be performed:', ['Within a reasonable time', 'Immediately', 'Within 7 days', 'Only when the promisee asks'], 0, 'Section 46.', 'c5'),
        Q('m10', 'A buyer prevents a contractor from starting work. Under Section 53 the contract is:', ['Voidable at the contractor\'s option, with compensation', 'Void', 'Valid and must still be performed', 'Illegal'], 0, 'Section 53.', 'c6', 'moderate'),
        Q('m11', 'Time is NOT of the essence and the promisor is late. The promisee:', ['Cannot avoid the contract but can claim compensation for loss', 'Can always avoid the contract', 'Has no remedy', 'Can claim only nominal damages'], 0, 'Section 55.', 'c6'),
        Q('m12', 'A contract to sell a specific horse becomes void when the horse dies before delivery, without fault. This is:', ['Supervening impossibility — Section 56', 'Anticipatory breach', 'Novation', 'Remission'], 0, 'Destruction of the subject-matter.', 'c6'),
        Q('m13', 'If the debtor does not indicate which debt a payment is for, the creditor may apply it to:', ['Any lawful debt due, even a time-barred one', 'Only the latest debt', 'A disputed debt', 'A debt not yet due'], 0, 'Section 60.', 'c7'),
        Q('m14', f'Debts of ₹30,000 (oldest, time-barred), ₹45,000 and ₹25,000; ₹60,000 paid, no appropriation by either. The outstanding balance of the second debt is:', [R(left_d2), R(45000), R(0), R(5000)], 0, 'Section 61 — order of time; the oldest (even time-barred) is cleared first.', 'c7', 'moderate', check='45000-(60000-30000)'),
        Q('m15', 'Substitution of a new contract for an existing one is:', ['Novation', 'Alteration', 'Remission', 'Waiver'], 0, 'Section 62.', 'c8'),
        Q('m16', 'A creditor accepts a smaller sum in full satisfaction of a larger debt. The debt is:', ['Discharged in full — Section 63', 'Discharged only to the amount paid', 'Not discharged without fresh consideration', 'Void'], 0, 'Remission needs no consideration.', 'c8', 'moderate'),
        Q('m17', 'A tenant buys the house he occupies. His lease ends by:', ['Merger', 'Novation', 'Breach', 'Rescission'], 0, 'The lesser right merges in ownership.', 'c9'),
        Q('m18', 'Rescission of a voidable contract is communicated or revoked:', ['In the same manner as a proposal — Section 66', 'Only through a court', 'Only in writing', 'Only by registered post'], 0, 'Section 66.', 'c8'),
    ]

    questions = [
        {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'legal',
         'q': f'X, Y and Z jointly borrowed {R(360000)} from Bank P. On the due date Bank P recovered the entire amount from Y. Z has since been declared insolvent and his estate pays 25 paise in the rupee. Explain, with reference to the Indian Contract Act, 1872, how much Y can recover from X and from Z\'s estate, and the loss Y finally bears.',
         'model': [legal('Section 43: where persons have made a joint promise, the promisee can require any one or more of them to carry out the entire promise. Each joint promisor may compel every other joint promisor to contribute equally; if any one defaults in contributing, the remaining joint promisors bear the loss arising from the default in equal shares.',
                         f'Bank P recovered the full {R(360000)} from Y. Each borrower\'s equal share is {R(q_share)}. Z\'s estate pays only 25%.',
                         f'Y can claim from Z\'s estate 25% of {R(q_share)} = {R(q_from_z)}. The shortfall of {R(q_short)} in Z\'s contribution is shared equally by X and Y. So Y recovers from X: X\'s own share {R(q_share)} + half the shortfall {R(q_short // 2)} = {R(q_from_x)}.',
                         f'Y recovers {R(q_from_x)} from X and {R(q_from_z)} from Z\'s estate, and finally bears {R(q_y_bears)} himself. (Check: {R(q_from_x)} + {R(q_y_bears)} + {R(q_from_z)} = {R(q_proof)}.)')],
         'scheme': [S('s1', 'Section 43 — promisee may compel any one', 1, 'provision'), S('s2', 'Equal contribution and sharing of default', 1, 'provision'), S('s3', 'Equal share and recovery from insolvent estate', 1.5, 'computation'), S('s4', 'Recovery from X including half the shortfall', 1.5, 'computation'), S('s5', 'Conclusion with Y\'s final burden', 1, 'conclusion')],
         'checks': cq,
         'remarks': ['Most errors are in sharing the shortfall — it is borne equally by the solvent promisors, not by the one who paid alone.'],
         'mistakes': ['Ignoring the 25% received from the insolvent estate.', 'Making Y bear the entire shortfall.'],
         'tips': ['Show a mini-table of shares in the analysis.', 'Add a one-line arithmetic proof that totals equal the debt.']},
        {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
         'q': f'Mr. Vora owes Mr. Kale three debts: {R(a1)} due in June 2021 (time-barred), {R(a2)} due in May 2024 and {R(a3)} due in January 2026. He sends (i) a cheque of {R(q2_p1)} stating it is "towards the May 2024 bill", and later (ii) a cheque of {R(q2_p2)} without any instruction; Mr. Kale makes no appropriation. Explain how the payments will be applied.',
         'model': [p('Section 59: where the debtor indicates the debt to which a payment is to be applied, and the creditor accepts it, it must be so applied. Section 61: where neither party appropriates, the payment is applied to the debts in order of time, whether or not time-barred.'),
                   table(['Step', 'Debt 1 — Jun 2021 (₹)', 'Debt 2 — May 2024 (₹)', 'Debt 3 — Jan 2026 (₹)'], [
                       ['Opening', a1, a2, a3],
                       [f'Cheque (i) {R(q2_p1)} — debtor\'s appropriation (S. 59)', a1, q2_r1, a3],
                       [f'Cheque (ii) {R(q2_p2)} — order of time (S. 61): debt 1 cleared, then debt 2', 0, 0, q2_left3],
                   ]),
                   p(f'Result: debts 1 and 2 are fully discharged; {R(q2_left3)} of debt 3 remains outstanding. (Cheque (ii): {R(q2_p2)} − {R(a1)} = {R(q2_after1)}; {R(q2_after1)} − {R(q2_r1)} = {R(q2_after2)} applied to debt 3.)')],
         'scheme': [S('s1', 'Section 59 applied to cheque (i)', 1.5, 'provision'), S('s2', 'Section 61 — order of time incl. time-barred debt', 1.5, 'provision'), S('s3', 'Correct computation of balances', 1.5, 'computation'), S('s4', 'Final outstanding stated', 0.5, 'conclusion')],
         'checks': cq2,
         'remarks': ['Candidates must respect the debtor\'s instruction for the first cheque before applying the order-of-time rule to the second.'],
         'mistakes': ['Applying cheque (i) to the oldest debt despite the debtor\'s instruction.', 'Skipping the time-barred debt under Section 61.'],
         'tips': ['A running table of balances makes the answer easy to mark.']},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
         'q': 'Distinguish between novation and alteration of a contract.',
         'model': [table(['Basis', 'Novation', 'Alteration'], [
             ['Meaning', 'Substitution of a new contract for the existing one', 'Change in one or more terms of the existing contract'],
             ['Parties', 'May be the same or new parties', 'Always the same parties'],
             ['Original contract', 'Extinguished and replaced', 'Continues with modified terms'],
             ['Example', 'A owes B; by agreement of all three, C becomes B\'s debtor instead of A', 'B agrees with A to extend the repayment date by three months'],
         ]), p('Both require mutual consent and are covered by Section 62; novation must take place before the time for performance expires.')],
         'scheme': [S('s1', 'Meaning', 1, 'concept'), S('s2', 'Parties', 1, 'concept'), S('s3', 'Effect on original contract', 1, 'concept'), S('s4', 'Examples / Section 62', 1, 'application')],
         'remarks': ['The point that novation may involve new parties earns a separate mark.'], 'mistakes': ['Saying alteration can bring in a new party.'], 'tips': ['Use a 3-column table.']},
        {'id': 'q4', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'text',
         'q': 'State the various modes by which a contract may be discharged.',
         'model': [ul(['By performance — actual, or attempted through a valid tender (Sections 37, 38).', 'By mutual agreement — novation, rescission, alteration (Section 62) and remission (Section 63).', 'By impossibility — initial or supervening (Section 56).',
                       'By lapse of time — expiry of the limitation period under the Limitation Act, 1963.', 'By operation of law — death in personal contracts, insolvency, unauthorised material alteration.', 'By breach — actual or anticipatory.',
                       'By the promisee\'s neglect to afford reasonable facilities (Section 67).', 'By merger of an inferior right into a superior right.'])],
         'scheme': [S('s1', 'Performance', 0.5, 'concept'), S('s2', 'Mutual agreement (with forms)', 1, 'concept'), S('s3', 'Impossibility', 1, 'concept'), S('s4', 'Lapse of time and operation of law', 1, 'concept'), S('s5', 'Breach', 0.5, 'concept'), S('s6', 'Section 67 / merger', 1, 'concept')],
         'remarks': ['A brief line with an example under each mode is ideal.'], 'mistakes': ['Listing only performance and breach.'], 'tips': ['Number the modes; give section numbers where they exist.']},
    ]

    viva = [
        V('v1', 'What are the conditions of a valid tender of performance?',
          'A valid tender must be unconditional, must be for the whole obligation, must be made at the proper time and place, and must give the promisee a reasonable opportunity to inspect the goods. It must be made to the proper person by a person able and willing to perform.',
          [P('p1', 'Unconditional', 3, 'unconditional|without condition|no condition|not conditional'),
           P('p2', 'For the whole obligation', 3, 'whole|entire|full|complete|all the goods|total'),
           P('p3', 'At the proper time and place', 2, 'proper time|right time|proper place|right place|time and place|agreed time|agreed place|business hour'),
           P('p4', 'Reasonable opportunity to inspect', 2, 'inspect|examin|check|opportunity|verify')], 'c1'),
        V('v2', 'What is the liability of joint promisors under Section 43?',
          'The promisee may compel any one of the joint promisors, or more than one, to perform the whole promise. The one who pays can compel the others to contribute equally. If one of them defaults in contributing, the remaining joint promisors share that loss equally.',
          [P('p1', 'Promisee can compel any one of them to perform the whole', 4, 'compel any|any one|anyone|any of them|any of the joint|any 1|any single|sue any|recover from any|demand from any|claim from any|whole from any|entire amount from any|either of them|one or more'),
           P('p2', 'Right to equal contribution from the others', 3, 'contribut|reimburs|equal share|share equal|equally'),
           P('p3', 'Loss from a defaulting promisor shared equally by the rest', 3, 'default|insolven|unable to pay|cannot pay|fails to pay|doesn t pay|does not pay|loss shared|share the loss|share loss|bear the loss|bear loss|remaining|others bear')], 'c4'),
        V('v3', 'Explain the rules for appropriation of payments.',
          'First, if the debtor indicates which debt the payment is for, it must be applied to that debt, under Section 59. If the debtor does not indicate, the creditor may apply it to any lawful debt due, even a time-barred debt, under Section 60. If neither of them appropriates, it is applied in order of time under Section 61, and proportionately if the debts are of equal standing.',
          [P('p1', 'Debtor\'s indication comes first (Section 59)', 3, 'debtor indicat|debtor specif|debtor direct|debtor express|debtor intimat|debtor tell|debtor say|debtor mention|debtor instruct|debtor choos|debtor decid|debtor first|first debtor|debtor has first|debtor right|debtor option|section 59|debtor wish|debtor want|debtor state'),
           P('p2', 'If he does not, the creditor may appropriate — even to a time-barred debt (Section 60)', 3, 'creditor', 'debtor not|debtor fail|debtor silent|debtor does not|debtor doesn t|debtor omit|no indicat|not indicat|not specif|if he does not|if not|otherwise|discret|time barred|section 60', min=2),
           P('p3', 'If neither appropriates — order of time (Section 61); proportionate if equal standing', 4, 'order of time|order time|chronolog|oldest|earliest|first in time|date order|order of date|order in which|section 61|proportion')], 'c7'),
        V('v4', 'Distinguish between novation and alteration.',
          'Novation means substituting a new contract for the existing one, and it may be between the same or new parties, so the original contract is extinguished. Alteration means changing one or more terms of the existing contract, always between the same parties, and the original contract continues.',
          [P('p1', 'Novation: a new contract substituted; may involve new parties', 5, 'novation substitut|novation new|novation is a new|novation means new|novation means substitut|novation replac|novation means replac|novation existing contract replac|novation old contract replac|novation entire|novation whole|novation change of party|novation new party|novation third party|novation different party|novation another'),
           P('p2', 'Alteration: change of terms; same parties; contract continues', 5, 'alteration chang|alteration modif|alteration term|alteration same|alteration amend|alteration vary|alteration variat|alteration means chang|alteration means modif|alteration only|alteration some|alteration few|alteration certain|alteration part|alteration existing contract|alter chang|alter modif|alter term|alter some')], 'c8'),
        V('v5', 'What are the different modes of discharge of a contract?',
          'A contract may be discharged by performance, by mutual agreement such as novation, rescission or alteration, by impossibility of performance, by lapse of time, by operation of law such as death or insolvency, and by breach of contract.',
          [P('p1', 'Performance', 2, 'perform'),
           P('p2', 'Mutual agreement (novation, rescission, alteration, remission)', 2, 'mutual|agreement|consent|novation|rescission|alteration|remission|waiver'),
           P('p3', 'Impossibility', 2, 'impossib|frustrat'),
           P('p4', 'Lapse of time / operation of law', 2, 'lapse|limitation|time barred|operation of law|death|insolven|merger|by law'),
           P('p5', 'Breach', 2, 'breach|break')], 'c9'),
        V('v6', 'What happens when performance becomes impossible after the contract is made?',
          'Under Section 56, when performance becomes impossible or unlawful after the contract is made, because of an event the promisor could not prevent, the contract becomes void. Examples are destruction of the subject-matter, change of law, war, or death or illness in a personal contract. If the promisor knew of the impossibility and the promisee did not, the promisor must compensate the promisee.',
          [P('p1', 'Contract becomes void (Section 56)', 4, 'becomes void|become void|became void|becoming void|void from|void after|void when|contract is void|contract void|contract becomes void|it is void|it becomes void|treated as void|section 56'),
           P('p2', 'Causes — destruction, change of law, war, death or incapacity', 3, 'destruct|destroy|change in law|change of law|law chang|war|death|die|ill|incapacit|unlawful|perish|burn|fire|flood|accident', min=1),
           P('p3', 'Promisor who knew of impossibility must compensate', 3, 'promisor knew|promisor know|promisor who knew|knew impossib|knew it was impossible|known to promisor|known to the promisor|promisor aware|aware impossib|aware of the impossib|promisor had knowledge|knowledge of impossib|promisor knowing|reasonable diligence|could have known|should have known')], 'c6'),
        V('v7', 'What is the effect of failure to perform at the fixed time under Section 55?',
          'If time is of the essence, the contract becomes voidable at the option of the promisee. If time is not of the essence, the contract is not voidable, but the promisee can claim compensation for the loss. If the promisee accepts late performance, he cannot claim compensation unless he gives notice at the time of acceptance.',
          [P('p1', 'Time of essence — voidable at the promisee\'s option', 4, 'essence voidabl|essence contract voidabl|essence contract become voidabl|essence becom voidabl|essence promisee avoid|essence promisee can avoid|essence promisee may avoid|essence promisee rescind|essence promisee may rescind|essential voidabl|essential contract voidabl|essence option promisee|essence option of promisee'),
           P('p2', 'Not of essence — not voidable; compensation for loss', 4, 'not essence compens|not of essence compens|not essential compens|not essence not voidabl|not essence contract not voidabl|not essence contract is not voidabl|not essence only compens|not essence promisee compens|not essence promisee claim compens|not essence promisee can claim|not essence claim compens|not essence damag|not essence promisee only|not essence not avoid|not essence cannot avoid|not essence can t avoid'),
           P('p3', 'Accepting late performance — no compensation unless notice given at acceptance', 2, 'notice|inform|intimat')], 'c6'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Shah Brothers settle their accounts', 'difficulty': 'hard',
        'case': ('Shah Brothers, a wholesaler, is owed three separate amounts by Pinto Stores: ₹50,000 due in 2021 (now time-barred), ₹70,000 due in 2024 and ₹30,000 due in 2025. '
                 'Pinto sends ₹1,00,000 with no instructions, and Shah Brothers does not appropriate it either. '
                 'Shah Brothers also had a contract to supply Pinto 500 crates of mangoes "by 15 May, time being of the essence"; it delivered on 25 May and Pinto accepted, writing on the delivery note: "Accepted late — we reserve our claim for loss." '
                 'Separately, three partners of Pinto had jointly borrowed ₹3,00,000 from Shah Brothers, which has now released one of them.'),
        'mcqs': [
            M('k1a', 'How much of the ₹1,00,000 goes to the 2021 debt?', [R(k_pay_first), R(0), R(33333), R(100000)], 0,
              'Section 61 — order of time, including time-barred debts: the 2021 debt of ₹50,000 is cleared first.', 'moderate', '50000'),
            M('k1b', 'What total remains due from Pinto after the payment?', [R(k_left), R(100000), R(30000), R(70000)], 0,
              f'Total ₹1,50,000 − ₹1,00,000 = {R(k_left)} (₹20,000 of the 2024 debt and ₹30,000 of the 2025 debt).', 'hard', '50000+70000+30000-100000'),
            M('k1c', 'Can Pinto claim compensation for the late mango delivery?', ['Yes — it gave notice at the time of accepting late performance', 'No — accepting late performance always bars compensation', 'No — time was of the essence, so only rescission was possible', 'Yes, but only nominal damages'], 0, 'Section 55 — notice at acceptance preserves the claim.', 'moderate'),
            M('k1d', 'After Shah Brothers releases one of the three borrowing partners:', ['The other two remain liable for the whole ₹3,00,000', 'All three are discharged', 'The debt is reduced by ₹1,00,000 automatically', 'The released partner must still pay Shah Brothers'], 0, 'Section 44 — release of one joint promisor does not discharge the others (and he remains liable to them for contribution).', 'moderate'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch02', 'n': 4, 'title': 'Performance of Contract',
        'outcomes': ['Explain the duty to perform (Section 37), actual and attempted performance, and the conditions of a valid tender.', 'Decide who must perform (Sections 40–42), distinguish succession from assignment, and compute the liabilities of joint promisors (Sections 43–45).',
                     'Apply the rules on time and place (Sections 46–50), reciprocal promises and impossibility (Sections 51–58) and appropriation of payments (Sections 59–61).', 'Explain contracts that need not be performed (Sections 62–67) and every mode of discharge of a contract.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 55, 'practice': 60}, 'prereq': ['fnd-p2-ch02-u03'],
                 'exam_tip': 'Numerical-style law problems come from this unit: joint promisors with an insolvent co-promisor (Section 43) and appropriation of payments (Sections 59–61). Show the arithmetic in a small table and end with a clear conclusion.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {'summary': ['Section 37: perform or offer to perform. Valid tender: unconditional, whole, proper time and place, chance to inspect, proper person (Section 38).',
                                 'Who performs: promisor (personal skill), agent, legal representatives (up to estate), third person accepted by promisee (Section 41), joint promisors jointly (Section 42).',
                                 'Succession passes rights and liabilities (liability limited to estate); assignment passes only benefits.',
                                 'Section 43: promisee may sue any joint promisor for the whole; equal contribution; default shared equally. Section 44: release of one does not discharge others. Section 45: joint promisees.',
                                 'Sections 46–50 time and place; 51–54 order of reciprocal promises; 55 time of essence; 56 impossibility; 57–58 legal and illegal parts.',
                                 'Appropriation: debtor (59) → creditor, even time-barred (60) → order of time / proportionate (61).',
                                 'Sections 62–67: novation, rescission, alteration, remission, restoration of benefits (64, 65), communication of rescission (66), promisee\'s neglect (67). Discharge: performance, agreement, impossibility, lapse of time, operation of law, breach.'],
                     'remember': ['37 duty to perform · 38 tender · 40 personal performance · 41 third-party performance · 42–45 joint rights and liabilities · 46–50 time/place · 51–58 reciprocal promises · 59–61 appropriation · 62 novation etc. · 63 remission · 64–65 restoration · 66 rescission communication · 67 neglect of promisee.'],
                     'traps': ['A tender of part is not a valid tender.', 'Shortfall of an insolvent joint promisor is shared equally by the solvent ones — not borne by the payer alone.', 'Under Section 61 even a time-barred debt is paid first if oldest.', 'Accepting late performance without notice loses the compensation claim.']},
        'quickref': [{'k': 'Section 37/38', 'v': 'Perform or offer to perform; refused valid tender protects promisor'}, {'k': 'Section 41', 'v': 'Performance by third person accepted → promisor discharged to that extent'},
                     {'k': 'Section 43', 'v': 'Any joint promisor liable for whole; equal contribution; default shared equally'}, {'k': 'Section 44', 'v': 'Release of one joint promisor does not discharge others'},
                     {'k': 'Section 55', 'v': 'Time of essence → voidable; not essence → compensation; late acceptance needs notice'}, {'k': 'Section 56', 'v': 'Initial impossibility void; supervening impossibility → contract void'},
                     {'k': 'Sections 59/60/61', 'v': 'Debtor appropriates → creditor appropriates → order of time'}, {'k': 'Section 62/63', 'v': 'Novation, rescission, alteration / remission without consideration'},
                     {'k': 'Joint promisor formula', 'v': 'Payer recovers from each solvent co-promisor: own share + (shortfall ÷ number of solvent promisors)'}],
        'viva': viva, 'cases': cases,
    }


# ---------- teaching explanations + topic tags for every MCQ (override the short drafts above) ----------
TPERF, TTEN, TWHO, TSA, TJ = 'Performance of Contract', 'Conditions to be Satisfied for a Valid Tender or Attempted Performance', 'By Whom a Contract May be Performed (Section 40, 41 and 42)', 'Distinction between Succession and Assignment', 'Liability of Joint Promisor & Promisee'
TTP, TREC, TAPP, TNP, TDIS = 'Time and Place for Performance of the Promise', 'Performance of Reciprocal Promise', 'Appropriation of Payments', 'Contracts, Which Need Not be Performed – with the Consent of Both the Parties', 'Discharge of a Contract'
EXPLAIN = {
    'm1': (TPERF, 'Section 37 obliges the parties to perform, or offer to perform, their respective promises unless performance is dispensed with or excused under the Act or any other law. Promises bind the parties\' legal representatives after death too, unless the contract shows otherwise. The tempting trap is "always perform personally" — only contracts needing personal skill must be performed personally (Section 40). In practice: a company\'s supply obligations continue even after its founder dies, and the business must keep delivering.'),
    'm2': (TTEN, 'A valid tender (attempted performance) must be unconditional, for the whole obligation, at the proper time and place, made to the proper person, and must give the promisee a reasonable chance to inspect goods. So "it may be for part of the obligation" is not a requirement — part tender is not valid. The trap is the inspection condition, which students forget is required. In practice: a debtor who offers only half the instalment due cannot claim he tendered payment and avoid default interest.'),
    'm3': (TWHO, 'Where a contract depends on the promisor\'s personal skill or taste, it must be performed by him personally (Section 40), and his death before performance ends the contract — his legal representatives are not bound. A portrait depends on A\'s own artistic skill. The tempting trap is "must be performed by A\'s heirs"; heirs are bound only for non-personal contracts such as paying a debt or delivering goods. In practice: contracts with a named consultant or artist usually include a clause on what happens if that person cannot perform.'),
    'm4': (TWHO, 'Section 41: once the promisee accepts performance offered by a stranger, he loses the right to claim that part again from the promisor. B accepted ₹1,20,000 from C, so A\'s debt falls by that amount: ₹2,00,000 − ₹1,20,000 = ₹80,000. The tempting trap is ₹2,00,000, assuming C\'s payment does not count because A did not authorise it. In practice: when a group company pays a supplier on behalf of another, the supplier\'s ledger for the debtor must be reduced accordingly.'),
    'm5': (TSA, 'Contractual rights or benefits, such as the right to receive a debt, can be assigned, so the assignee can collect it. Liabilities cannot be assigned without the creditor\'s consent, and contracts involving personal skill cannot be assigned at all. The tempting trap is "the liability to repay a loan" — a borrower cannot pass his debt to someone else without the lender\'s agreement (that would need novation). In practice: businesses assign their trade receivables to banks or factoring companies to raise working capital.'),
    'm6': (TJ, 'Section 43: unless the contract says otherwise, a promisee holding a joint promise can make any single promisor, or several of them, perform it in full. So W may recover the full ₹90,000 from any one of X, Y and Z. The tempting trap is "recover only ₹30,000 from each" — equal shares matter only for contribution among the promisors themselves. In practice: when partners jointly borrow, the bank can recover the entire loan from whichever partner has assets.'),
    'm7': (TJ, 'Section 44: when one of joint promisors is released by the promisee, the others are not discharged, and the released promisor is not released from his liability to the other joint promisors for contribution. So Q and R remain liable for the whole ₹3,00,000. The tempting trap is "only P\'s share is reduced from the debt" — the creditor\'s claim against Q and R is not cut down. In practice: a lender settling with one co-borrower should document carefully, because the remaining co-borrowers still owe the full amount.'),
    'm8': (TJ, 'Each share = ₹4,50,000 ÷ 3 = ₹1,50,000. A\'s estate pays 40 paise in the rupee: ₹1,50,000 × 0.40 = ₹60,000, leaving a shortfall of ₹90,000. Under Section 43 the solvent promisors bear that loss equally: ₹45,000 each. C recovers from B ₹1,50,000 + ₹45,000 = ₹1,95,000. The tempting trap is ₹1,50,000, ignoring B\'s share of A\'s shortfall. In practice: partners settling a joint debt after one partner\'s insolvency share the deficiency equally.'),
    'm9': (TTP, 'Section 46: where no time for performance is specified and the promisor need not wait for an application from the promisee, the promise must be performed within a reasonable time. What is reasonable is a question of fact in each case. The tempting trap is "immediately" — the law does not demand instant performance. In practice: when a purchase order gives no delivery date, the supplier must deliver within the period customary in that trade.'),
    'm10': (TREC, 'Section 53: if one side stops the other from performing a reciprocal contract, the obstructed party may choose to end the contract and also claim compensation for his loss. The buyer\'s obstruction gives the contractor that option. The tempting trap is "void" — the contract is not automatically dead; the innocent party chooses. In practice: a contractor denied site access by the client can terminate and claim costs incurred plus lost profit.'),
    'm11': (TREC, 'Section 55: if time is not of the essence, failure to perform on time does not make the contract voidable, but the promisee is entitled to compensation for any loss caused by the delay. The tempting trap is "can always avoid the contract" — that right exists only where time is of the essence. In practice: when a vendor delivers office furniture a week late under a contract without a strict deadline, the buyer must accept it but can deduct proven losses.'),
    'm12': (TREC, 'Section 56: a contract to do an act that, after it is made, becomes impossible through an event the promisor could not prevent becomes void. The specific horse died before delivery without anyone\'s fault — the subject-matter was destroyed, a case of supervening impossibility. The tempting trap is anticipatory breach, which needs a party refusing to perform before the due date. In practice: force majeure clauses in commercial contracts deal with events like fire or floods that destroy the goods.'),
    'm13': (TAPP, 'Section 60: where the debtor does not say which debt a payment is for, the creditor can choose to adjust it against any lawful debt that is due, even one whose recovery is time-barred. The tempting trap is "a disputed debt" — the debt must be lawful and actually due; a debt not yet due cannot be chosen either. In practice: creditors often apply unallocated receipts to the oldest invoices, and auditors check such allocations when testing debtor ageing.'),
    'm14': (TAPP, 'Section 61: when neither party appropriates, payment is applied in order of time, whether or not the debts are time-barred. ₹60,000 first clears the oldest ₹30,000 debt; the remaining ₹30,000 goes to the second debt of ₹45,000, leaving ₹45,000 − ₹30,000 = ₹15,000 outstanding. The tempting trap is ₹45,000, skipping the time-barred debt. In practice: a debtor wanting a payment to reduce a particular invoice must specify it in the remittance advice.'),
    'm15': (TNP, 'Section 62: novation is substitution of a new contract for an existing one, by agreement — either between the same parties or with a new party — and the original contract need not be performed. The tempting trap is "alteration", which changes some terms of the same contract between the same parties without replacing it. In practice: when a borrower\'s loan is taken over by a new company with the lender\'s agreement, the old contract is replaced by novation.'),
    'm16': (TNP, 'Section 63: a promisee may remit, wholly or partly, the performance promised, or accept any satisfaction he thinks fit. Accepting a smaller sum in full satisfaction discharges the whole debt, and no fresh consideration is needed. The tempting trap is "not discharged without fresh consideration" — that is the English rule; Indian law under Section 63 does not require it. In practice: one-time settlements of loans, where a bank accepts a reduced amount, rely on this principle.'),
    'm17': (TDIS, 'Merger occurs when an inferior right and a superior right come to the same person; the inferior right ends. As tenant the occupant held a lease (lesser right); buying the house gives him ownership (superior right), so the lease merges and ends. The tempting trap is "novation" — no new contract replaces the lease; it simply disappears into ownership. In practice: when a company buys premises it was leasing, the lease liability is derecognised and the property recorded as an owned asset.'),
    'm18': (TNP, 'Section 66 says the rescission of a voidable contract may be communicated or revoked in the same manner, and subject to the same rules, as a proposal. Communication is complete when it comes to the other party\'s knowledge. The tempting trap is "only in writing" — no particular form is prescribed. In practice: a party rescinding a contract induced by misrepresentation should still give written notice, because proof of communication will matter in any dispute.'),
    'k1/k1a': (TAPP, 'Neither Pinto nor Shah Brothers appropriated the payment, so Section 61 applies: payment goes to debts in order of time, whether or not time-barred. The oldest debt is the 2021 amount of ₹50,000, so ₹50,000 of the ₹1,00,000 clears it fully. The tempting trap is ₹0, assuming time-barred debts are skipped. In practice: CAs reconciling old customer accounts know an unallocated receipt may revive recovery of an otherwise time-barred balance.'),
    'k1/k1b': (TAPP, 'Total owed = ₹50,000 + ₹70,000 + ₹30,000 = ₹1,50,000. After the ₹1,00,000 payment, ₹1,50,000 − ₹1,00,000 = ₹50,000 remains — ₹20,000 of the 2024 debt and the whole ₹30,000 of the 2025 debt. The tempting trap is ₹30,000, forgetting that only ₹50,000 of the payment is left for the 2024 debt after clearing 2021. In practice: debtor ageing schedules show this split, which affects provisions for doubtful debts.'),
    'k1/k1c': (TREC, 'Section 55: where time is of the essence and the promisee accepts late performance, he cannot claim compensation for the delay unless, at the time of acceptance, he gives notice of his intention to do so. Pinto wrote "we reserve our claim for loss" on the delivery note, so it preserved the claim. The tempting trap is "accepting late performance always bars compensation" — notice at acceptance saves it. In practice: purchase teams note reservations on goods received notes when accepting late deliveries.'),
    'k1/k1d': (TJ, 'Section 44: releasing one joint promisor does not discharge the others, so the two remaining partners stay liable to Shah Brothers for the whole ₹3,00,000. The released partner is free from Shah Brothers\' claim but still owes contribution to his co-promisors. The tempting trap is "the debt is reduced by ₹1,00,000 automatically" — the creditor\'s claim against the others is not reduced. In practice: lenders use such releases when settling with one co-borrower while pursuing the rest.'),
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
    'q1': {'extra_ok': False,
           's1': _k('section 43|joint promis', 'any one|any of|entire|whole|full|all'),
           's2': _k('contribute|contribution', 'equal|equally', 'default|insolvent|insolvency|loss|shortfall|deficiency'),
           's3': _k('25 percent 120000|120000 25 percent|30000 from z|30000 z|z 30000|estate 30000|30000 estate|z pays 30000|z will pay 30000|25 paise 120000|120000 25 paise|z estate 30000|z s estate 30000', nums=[120000, 30000]),
           's4': _k('half|shortfall|90000|equally|share', nums=[45000, 165000]),
           's5': _k('bear|bears|borne|loss|himself|own pocket|final|finally|net', nums=[165000, 30000]),
           },
    'q2': {'extra_ok': False,
           's1': _k('section 59|debtor appropriat|debtor indicat|debtor specif|debtor s appropriation|instruction|indicated by the debtor|as directed|debtor direct|appropriated by debtor|debtor chose|specified', 'may 2024|second debt|debt 2|2024 bill|2024 debt'),
           's2': _k('section 61|order of time|chronological|order in which|earliest|oldest|first in time|order they fell due', 'even if time barred|even time barred|whether or not time barred|whether time barred or not|including time barred|includes time barred|time barred debt first|2021 debt first|first to the 2021|first 18000|18000 first|first to the june 2021|first to the time barred|irrespective|even though time barred|although time barred|though time barred|even if barred|even barred by limitation|whether or not barred',
                    wrong=[{'kw': ['cannot be applied to the time barred|cannot be applied to time barred|excluding the time barred|except the time barred|ignore the time barred|time barred debt cannot be paid|cannot appropriate to time barred|not to the time barred debt'], 'say': 'Under Section 61 the payment goes to debts in order of time, whether or not barred by limitation — the June 2021 debt is paid first.'}]),
           's3': _k('balance|outstanding|remain|left|due', nums=[8000, 6000]),
           's4': _k('6000 outstanding|6000 remains|outstanding 6000|balance 6000|6000 due|6000 of debt 3|remains 6000|6000 balance|remaining 6000|6000 still|due 6000|6000 unpaid|6000 left|6000 jan|6000 january|6000 payable', nums=[6000]),
           },
    'q3': {'extra_ok': True,
           's1': _k('new contract|substitut|replace', 'change|modif|vary|variation|altered|alter terms|terms changed'),
           's2': _k('new parties|new party|different parties|third party|same or new|may change|parties may change|change of parties', 'same parties|always same|parties remain same|parties same|parties remain the same'),
           's3': _k('extinguish|ends|terminated|discharged|replaced|cease|no longer|comes to an end', 'continues|continue|remains|subsist|survive|still exists'),
           's4': _k('section 62', 'debtor|extend|repayment|creditor|instead of|interest rate|reduce|price|date|example', n=1),
           },
    'q4': {'extra_ok': True,
           's1': _k('performance|tender'),
           's2': _k('mutual agreement|agreement|consent', 'novation|rescission|alteration|remission|section 62|section 63'),
           's3': _k('impossibility|impossible|frustration|section 56'),
           's4': _k('lapse of time|limitation|time barred|lapse', 'operation of law|death|insolvency|material alteration'),
           's5': _k('breach'),
           's6': _k('section 67|reasonable facilities|neglect|facility|merger|superior right|inferior right|merge'),
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
