"""CA Foundation · Paper 2 Business Laws · Chapter 2 The Indian Contract Act, 1872 · Unit 5 Breach of Contract and its Remedies.
Original explanations and problems; sections and leading cases are cited by name only; all figures computed below."""
from lib import *
from ca_viva import P, ALT, V
from ca_cases import M

UID = 'fnd-p2-ch02-u05'


def Q(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check: d['check'] = check
    return d


def S(sid, pt, m, skill): return {'id': sid, 'pt': pt, 'm': m, 'skill': skill}


def build():
    # ---- Illustration 1: ordinary damages = market price - contract price ----
    c1 = Checks()
    bags, kp, mp = 400, 2800, 3150
    diff = c1.add('3150-2800', 'rise in price per bag on the due date')
    dmg = c1.add('400*(3150-2800)', 'ordinary damages = quantity x (market price - contract price)')

    # ---- Illustration 2: Section 74 cap ----
    c2 = Checks()
    named = 500000
    lossA, lossB = 320000, 700000
    awardA = c2.add('320000', 'case (a): reasonable compensation = loss proved, within the named sum')
    awardB = c2.add('500000', 'case (b): award capped at the sum named in the contract')
    excessB = c2.add('700000-500000', 'case (b): loss that cannot be recovered beyond the cap')

    # ---- Illustration 3: mitigation ----
    c3 = Checks()
    qty, cprice, mkt, paid = 250, 1200, 1340, 1460
    claim_buyer = c3.add('250*(1460-1200)', 'buyer\'s claim based on the price he actually paid')
    allowed = c3.add('250*(1340-1200)', 'damages allowed: market price available on the due date')
    disallowed = c3.add('65000-35000', 'loss due to failure to mitigate — not recoverable')

    # ---- Illustration 4: quantum meruit for a divisible contract ----
    c4 = Checks()
    bales, rate, inst = 120, 1500, 40
    qm = c4.add('40*1500', 'value of the first instalment accepted by the buyer')

    # ---- Question 2 figures ----
    cq = Checks()
    q_qty, q_kp, q_mp = 600, 950, 1080
    q_dmg = cq.add('600*(1080-950)', 'ordinary damages for the steel rods')

    # ---- Question 3 figures ----
    cq3 = Checks()
    q3_named = 300000
    q3_a = cq3.add('180000', 'loss of ₹1,80,000 is within the named sum')
    q3_b = cq3.add('300000', 'loss of ₹4,10,000 — capped at the named sum')

    # ---- case figures ----
    cc = Checks()
    k_ord = cc.add('1000*(78-60)', 'ordinary damages: 1,000 kg x (₹78 - ₹60)')
    k_cap = cc.add('50000', 'Section 74 cap on the delay clause')

    kinds = table(['Kind', 'When awarded', 'Example'], [
        ['Ordinary (general)', 'Loss arising naturally, in the usual course of things, from the breach', 'Difference between the contract price and the market price on the due date'],
        ['Special', 'Loss arising from special circumstances communicated to the defaulting party when the contract was made', 'Loss of profit of a mill, where the carrier was told the mill is idle for want of the part'],
        ['Exemplary (vindictive)', 'To punish, not merely compensate — only for (a) breach of promise to marry, (b) wrongful dishonour of a customer\'s cheque by a banker', 'A trader\'s cheque wrongly dishonoured although funds were sufficient'],
        ['Nominal', 'Breach proved but no real loss — a token sum to recognise the right', 'One rupee'],
        ['Deterioration caused by delay', 'Recoverable from a carrier even without notice; includes loss of a special opportunity to sell', 'Fruit that rots because of a late delivery'],
        ['Pre-fixed (liquidated damages / penalty)', 'Sum named in the contract — Section 74: reasonable compensation not exceeding that sum', 'Delay clause of ₹10,000 a week'],
    ], title='Kinds of damages')

    concepts = [
        {'id': 'c1', 'title': 'Breach of contract — meaning and kinds', 'body': [
            'Breach of contract means a party\'s failure to carry out his obligation under the contract, without lawful excuse.',
            'It may be (1) actual — failure to perform on the due date, or during performance (e.g. stopping halfway); or (2) anticipatory — refusing, or disabling oneself from performing, before the due date.',
            'Whatever the kind, the injured party is discharged from his own obligations and gets the remedies described in this unit.'],
         'analogy': 'Actual breach is not turning up for the match; anticipatory breach is announcing a week earlier that you will not come — or selling your kit to someone else.',
         'work': 'When a customer cancels a confirmed order before the delivery date, a CA in industry recognises an anticipatory breach and advises on the claim and on the accounting for the cancelled order.'},
        {'id': 'c2', 'title': 'Anticipatory breach — Section 39', 'body': [
            'Section 39: if one party refuses to perform the whole of his promise, or puts himself in a position where he cannot perform it, the other party is entitled to terminate the contract — unless his own words or conduct show that he has agreed to let it continue.',
            'It may be express (a clear statement: "I will not deliver") or implied by conduct (e.g. A agrees to sell his horse to B on 1 September, but sells it to C in August).',
            'Effect: the promisee is excused from further performance and may choose either (1) to treat the contract as ended at once and sue for damages immediately, without waiting for the due date (Hochster v. De La Tour), or (2) to keep the contract alive and wait for the due date, then hold the other party liable. If he waits, he keeps the contract alive for both sides — the promisor may still perform, and if some later event (e.g. a change in law) excuses performance, the promisee may lose his claim (Frost v. Knight discussed the promisee\'s option to wait or sue at once).'],
         'analogy': 'If the caterer tells you in March he won\'t serve your May wedding, you can book another caterer and sue now — or hold him to it and wait, with the risk that comes with waiting.',
         'work': 'Commodity buyers facing a supplier\'s cancellation often book a replacement at once — choosing option (1) — to limit price risk; the CA documents the date of acceptance of the repudiation, as damages are measured with reference to it.'},
        {'id': 'c3', 'title': 'Actual breach', 'body': [
            'Actual breach occurs when a party fails to perform on the due date (e.g. supplier does not deliver on 1 June), or during performance (e.g. a contractor abandons the building midway, or a singer engaged for twelve nights stays away from the sixth night).',
            'The injured party may treat the contract as ended (Section 39 applies to refusal during performance too), is discharged from his own obligations, and may claim compensation. Where time was not of the essence (Section 55), he may instead allow extra time and claim compensation for the delay.'],
         'analogy': 'The bell has rung and the student has not written the paper — that is actual breach.',
         'work': 'A CA preparing a claim for a client whose supplier failed to deliver gathers market rates on the due date — the starting point for damages.'},
        {'id': 'c4', 'title': 'Suit for damages — Section 73 and Hadley v. Baxendale', 'body': [
            'Section 73: the injured party may recover compensation for loss or damage (a) that arose naturally in the usual course of things from the breach, or (b) that both parties, at the time of contracting, foresaw as a likely result of such a breach. No compensation is given for remote and indirect loss or damage.',
            'Duty to mitigate: in assessing the loss, the court takes into account the means of remedying the inconvenience that were reasonably available — the injured party must take reasonable steps to reduce his loss and cannot recover loss he could have avoided.',
            'Hadley v. Baxendale: a mill\'s broken crankshaft was handed to a carrier for delivery to the makers as a pattern. The carrier delayed. The mill-owner claimed loss of profits for the extra days the mill stood idle. Held: the loss of profit was not recoverable, because the carrier had not been told that the mill would be idle until the shaft returned — such loss was neither a natural consequence nor within the parties\' contemplation.',
            'Usual measure for goods: (market price on the due date − contract price) × quantity. Compensation is to make good the loss, not to punish.'],
         'analogy': 'Damages pay for the ripples you could foresee when you threw the stone, not for every wave that later reached a distant shore.',
         'work': 'Claims for "consequential loss" (lost profits, penalties under other contracts) succeed only where the special circumstances were communicated at the time of contract — which is why CAs advise clients to state critical deadlines and end-uses in purchase orders.'},
        {'id': 'c5', 'title': 'Kinds of damages', 'body': [
            'Ordinary damages compensate for the natural, direct loss. Special damages require notice of the special circumstances at the time of contracting (if a carrier is told the mill is idle, it is liable for the mill\'s normal profit for the period of delay — but not for loss of an unusually profitable contract it was never told about).',
            'Exemplary damages are awarded only in two cases: breach of promise to marry, and wrongful dishonour of a customer\'s cheque by a banker. A trader whose credit suffers may get substantial damages even without proof of money loss; a non-trader gets only nominal damages unless special loss is pleaded and proved (Gibbons v. Westminster Bank).',
            'Nominal damages recognise a breach that caused no real loss. Where goods deteriorate because a carrier was late, damages are payable even though no notice was given. Pre-fixed damages are governed by Section 74 (next card).'],
         'blocks': [kinds],
         'analogy': 'Ordinary damages refill the glass you spilt; special damages also pay for the carpet — but only if you warned them about the carpet.',
         'work': 'In claims against logistics providers, CAs separate ordinary loss (value of goods, deterioration) from special loss (production stoppage), because each needs different proof.'},
        {'id': 'c6', 'title': 'Penalty and liquidated damages — Section 74', 'body': [
            'Parties often name in the contract the sum payable on breach. English law distinguishes liquidated damages (a genuine pre-estimate of loss — recoverable in full) from a penalty (an extravagant sum fixed to frighten the other party into performing — not enforced beyond actual loss).',
            'Indian law (Section 74) does not draw this distinction. Whether the sum is called a penalty or liquidated damages, the injured party gets reasonable compensation not exceeding the amount named. The court will never award more than the named sum, but may award less.',
            'Example: named sum ₹5,00,000. If the loss is ₹3,20,000, the award is ₹3,20,000; if the loss is ₹7,00,000, the award is limited to ₹5,00,000.',
            'Guides to spotting a penalty: a sum far larger than any probable loss; an extra sum payable merely for delay in paying an amount (delay alone rarely causes such loss); a clause raising the interest rate once a default occurs can also be a penalty. The label used by the parties is not conclusive. A clause that the whole loan becomes due on default of one instalment is not a penalty.',
            'Exception: where a person gives a bond or similar instrument to the Central or a State Government for performing a public duty or an act in which the public is interested, he is liable to pay the whole sum named on breach.'],
         'analogy': 'The named sum is a ceiling, not a price tag: the court fills the room with reasonable compensation up to, but never above, that ceiling.',
         'work': 'Delay (LD) clauses in construction and IT contracts are routinely negotiated by CAs and finance teams; when deliveries slip, they estimate the provision on the basis of reasonable compensation capped at the clause amount.'},
        {'id': 'c7', 'title': 'Other remedies — rescission, quantum meruit, specific performance, injunction', 'body': [
            'Rescission: the injured party may treat the contract as rescinded; he is freed from his own obligations and, under Section 75, a person who rightfully rescinds is entitled to compensation for damage sustained through non-performance.',
            'Quantum meruit ("as much as he has earned"): a claim for the value of work done or goods supplied. Conditions: the original contract must have been discharged (e.g. by the other party\'s breach), and the claim is made by the party not in default. It is restitutory (pays for value received), whereas damages are compensatory. Typical cases: an agreement discovered to be void or a contract that becomes void; work done not intended to be gratuitous; services rendered with no agreed fee; one party abandons or refuses to perform; a divisible contract partly performed and the benefit enjoyed; and a lump-sum contract fully but badly performed (lump sum payable, less a deduction for bad work).',
            'Specific performance: where damages are not an adequate remedy (e.g. a contract for a unique painting or a particular piece of land), the court may, in its discretion, order the party in breach to perform the contract as agreed.',
            'Injunction: where a party is doing something he promised not to do, the court may issue an order restraining him (e.g. an actor who agreed to act exclusively for one producer during a period may be restrained from acting for another producer during that period, though he cannot be forced to act for the first).'],
         'analogy': 'Damages pay for the broken promise; quantum meruit pays for the work already done; specific performance says "keep your promise"; an injunction says "stop breaking it".',
         'work': 'When a client\'s contractor walks off a half-finished job, the CA helps value the work done (quantum meruit), the extra cost of completion (damages) and any liquidated damages (Section 74).'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Damages for non-delivery — market price rule', 'difficulty': 'core', 'minutes': 6,
         'q': f'Gopal agrees to supply {bags} bags of sugar to Rekha at {R(kp)} a bag on 15 March. On 15 March the market price is {R(mp)} a bag and Gopal refuses to deliver. What damages can Rekha claim?',
         'solution': [legal('Section 73: compensation for loss arising naturally, in the usual course of things, from the breach. For non-delivery of goods, the natural loss is the excess of the market price on the due date over the contract price.',
                            f'Contract price {R(kp)}; market price on the due date {R(mp)}; {bags} bags not delivered.',
                            f'Rekha would have to pay {R(diff)} more per bag to buy the same sugar in the market.',
                            f'Rekha can claim ordinary damages of {R(dmg)}.'),
                      wn('Working', f'{bags} × ({R(mp)} − {R(kp)}) = {bags} × {R(diff)} = {R(dmg)}.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Section 74 — named sum as a ceiling', 'difficulty': 'moderate', 'minutes': 7,
         'q': f'A software contract provides that the vendor will pay {R(named)} as "liquidated damages" if the system is not live by 1 April. It goes live in July. Find the amount recoverable if the client\'s proved loss is (a) {R(lossA)}; (b) {R(lossB)}.',
         'solution': [legal('Section 74: if the contract fixes a sum to be paid on breach, the injured party is entitled to reasonable compensation not exceeding the amount so named; Indian law does not distinguish between penalty and liquidated damages.',
                            f'Named sum {R(named)}. Proved loss: (a) {R(lossA)}; (b) {R(lossB)}.',
                            'In (a) reasonable compensation equals the loss, which is below the cap. In (b) the loss exceeds the cap, so the award stops at the named sum.',
                            f'(a) {R(awardA)}; (b) {R(awardB)} — the remaining {R(excessB)} of loss cannot be recovered.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Failure to mitigate', 'difficulty': 'hard', 'minutes': 8,
         'q': f'Sana agrees to buy {qty} units of packing material from Tushar at {R(cprice)} each, delivery on 10 June. Tushar fails to deliver. On 10 June the material is freely available in the market at {R(mkt)}, but Sana waits two weeks and then buys at {R(paid)}. She claims {R(claim_buyer)}. How much can she recover?',
         'solution': [legal('Section 73: compensation for loss arising naturally from the breach; in estimating it, the means available for remedying the inconvenience must be taken into account — the injured party must take reasonable steps to mitigate the loss.',
                            f'Contract price {R(cprice)}; market price on the due date {R(mkt)}; Sana delayed and paid {R(paid)}.',
                            'Sana could have bought at the market price on 10 June. The extra cost caused by her own delay is not a loss arising from the breach.',
                            f'Sana can recover {R(allowed)}; {R(disallowed)} of her claim fails for want of mitigation.'),
                      table(['Particulars', 'Amount (₹)'], [['Claimed: 250 × (1,460 − 1,200)', claim_buyer], ['Allowed: 250 × (1,340 − 1,200)', allowed], ['Not recoverable (failure to mitigate)', disallowed]])],
         'checks': c3},
        {'id': 'i4', 'title': 'Quantum meruit — instalment contract', 'difficulty': 'moderate', 'minutes': 6,
         'q': f'Ajay agrees to deliver {bales} bales of cotton to Bimal at {R(rate)} a bale in three instalments of {inst} bales. He delivers the first instalment, which Bimal accepts and uses, and then fails to deliver the rest. Bimal refuses to pay anything. Decide.',
         'solution': [legal('Quantum meruit: where a divisible contract is partly performed and the other party has accepted and enjoyed the benefit of that part, he must pay for it. Ajay remains liable in damages for his own breach.',
                            f'The contract was divisible into instalments. Bimal accepted and used {inst} bales; Ajay defaulted on the remaining instalments.',
                            'Bimal cannot keep the benefit without paying for it. His remedy for the undelivered bales is a claim for damages against Ajay, which may be set off.',
                            f'Bimal must pay {R(qm)} for the bales received ({inst} × {R(rate)}); he may claim damages from Ajay for non-delivery of the rest.')],
         'checks': c4},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Customer cancels a confirmed order', 'role': 'CA in industry — commercial finance', 'situation': 'A customer cancels, in writing, a ₹40 lakh custom-machinery order two months before delivery. Production is 30% complete.',
         'steps': ['Treat the cancellation as an anticipatory breach (Section 39).', 'Decide promptly: accept the repudiation and claim now, or keep the contract alive. Usually accept, to stop incurring further cost (mitigation).', 'Quantify: costs incurred and loss of profit arising naturally; any special loss communicated at the time of contract; the cancellation clause amount if any (Section 74 cap).', 'Stop further production, try to resell or reuse the work-in-progress, and document every step.'],
         'takeaway': 'Speed matters — every rupee spent after a clear repudiation may be a rupee you cannot recover.', 'think': 'Why should the company stop production even though it believes it will win?',
         'answer': 'Because the duty to mitigate (Explanation to Section 73) means costs that could reasonably have been avoided after the breach are not recoverable.'},
        {'id': 'j2', 'title': 'Provision for liquidated damages', 'role': 'Statutory auditor', 'situation': 'Your client, a contractor, is 10 weeks late on a project. The contract provides ₹2 lakh per week of delay, capped at 10% of the ₹1.5 crore contract value.',
         'steps': ['Compute the contractual figure: 10 weeks × ₹2 lakh = ₹20 lakh; the cap of 10% of ₹1.5 crore = ₹15 lakh.', 'Under Section 74 the employer can get reasonable compensation not exceeding the named sum — so the maximum exposure is ₹15 lakh.', 'Assess with management whether a provision or a contingent-liability disclosure is appropriate, considering extensions of time and the employer\'s actual loss.'],
         'takeaway': 'Section 74 gives the ceiling; the accounting standard decides how much to provide within it.', 'checks': [{'expr': '10*200000', 'value': 2000000, 'label': 'delay amount before the cap'}, {'expr': '15000000*10/100', 'value': 1500000, 'label': 'cap at 10% of contract value'}]},
    ]

    mcqs = [
        Q('m1', 'When a party refuses to perform his promise before the due date, it is:', ['Anticipatory breach', 'Actual breach', 'Novation', 'Remission'], 0, 'Section 39.', 'c2'),
        Q('m2', 'On an anticipatory breach, the promisee may:', ['Either rescind and sue at once, or wait for the due date', 'Only wait for the due date', 'Only sue after the due date', 'Not claim anything'], 0, 'He has an option under Section 39.', 'c2'),
        Q('m3', 'A agrees to sell his car to B on 1 July but sells it to C on 10 June. This is:', ['Anticipatory breach by conduct', 'Actual breach', 'No breach until 1 July', 'Frustration'], 0, 'Disabling oneself from performing before the due date.', 'c2', 'moderate'),
        Q('m4', 'Damages for loss arising naturally in the usual course of things are:', ['Ordinary damages', 'Special damages', 'Exemplary damages', 'Nominal damages'], 0, 'Section 73, first limb.', 'c4'),
        Q('m5', 'Remote and indirect losses are:', ['Not recoverable', 'Always recoverable', 'Recoverable with interest', 'Recoverable only by traders'], 0, 'Section 73 — no compensation for remote or indirect loss.', 'c4'),
        Q('m6', 'The rule in Hadley v. Baxendale concerns:', ['Remoteness of damages', 'Capacity of minors', 'Wagering agreements', 'Appropriation of payments'], 0, 'Only natural or contemplated losses are recoverable.', 'c4'),
        Q('m7', f'Contract: 400 bags at {R(kp)}; market price on the due date {R(mp)}; seller fails to deliver. Damages are:', [R(dmg), R(1120000), R(1260000), R(350)], 0, 'Quantity × (market − contract).', 'c4', 'moderate', check='400*(3150-2800)'),
        Q('m8', 'Exemplary damages may be awarded for:', ['Wrongful dishonour of a cheque by a banker', 'Non-delivery of goods', 'Late payment of rent', 'Breach of a sale of land'], 0, 'Only breach of promise to marry and wrongful dishonour of a cheque.', 'c5'),
        Q('m9', 'Where breach is proved but no actual loss is suffered, the court awards:', ['Nominal damages', 'Exemplary damages', 'Special damages', 'Nothing at all'], 0, 'A token amount recognising the right.', 'c5'),
        Q('m10', f'A contract names {R(named)} payable on breach. Actual loss is {R(lossB)}. The court may award at most:', [R(awardB), R(lossB), R(excessB), R(1200000)], 0, 'Section 74 — reasonable compensation not exceeding the named sum.', 'c6', 'moderate', check='500000'),
        Q('m11', 'Under Indian law, the distinction between penalty and liquidated damages:', ['Is not made — reasonable compensation up to the named sum is awarded', 'Is strictly followed as in English law', 'Makes penalties fully recoverable', 'Makes liquidated damages unrecoverable'], 0, 'Section 74.', 'c6'),
        Q('m12', 'A person who gives a bond to the Government for a public duty and breaks it is liable for:', ['The whole sum named in the bond', 'Reasonable compensation only', 'Nominal damages', 'Nothing'], 0, 'Exception to Section 74.', 'c6', 'moderate'),
        Q('m13', '"Quantum meruit" means:', ['As much as he has earned', 'Let the buyer beware', 'Stand by what is decided', 'Hear the other side'], 0, 'Payment for the value of work done.', 'c7'),
        Q('m14', 'A claim on quantum meruit can be made by:', ['The party not in default, after the contract is discharged', 'The party in default only', 'Either party, while the contract continues', 'Only a minor'], 0, 'Two conditions: original contract discharged; claimant not in default.', 'c7', 'moderate'),
        Q('m15', 'Where damages are not an adequate remedy, the court may order the defaulting party to perform. This is:', ['Specific performance', 'Injunction', 'Rescission', 'Quantum meruit'], 0, 'Discretionary remedy for unique subject-matter.', 'c7'),
        Q('m16', 'An actor who agreed to act only for producer P during 2026 starts shooting for Q. P\'s appropriate remedy against acting for Q is:', ['Injunction', 'Specific performance forcing him to act for P', 'Exemplary damages', 'Quantum meruit'], 0, 'A court restrains breach of a negative promise; it will not force personal service.', 'c7', 'moderate'),
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'text',
         'q': '"An anticipatory breach of contract is a breach before the time fixed for performance." Explain, stating the rights of the aggrieved party.',
         'model': [p('Anticipatory breach occurs when, before the due date, a party refuses to perform or disables himself from performing his promise in its entirety. It may be express (a clear refusal) or implied from conduct (e.g. selling to someone else the specific goods agreed to be sold).'),
                   p('Section 39 lets the promisee terminate the contract, except where he has, by what he said or did, accepted that it should go on.'),
                   ul(['He is excused from his own performance.', 'Option 1: treat the contract as rescinded and sue for damages at once, without waiting for the due date.', 'Option 2: keep the contract alive and wait for the due date; he then holds the other party liable for non-performance — but the contract stays alive for both sides, and if a later event excuses performance, the promisor may escape liability.']),
                   p('Damages are assessed under Section 73 — loss arising naturally from the breach, subject to the duty to mitigate.')],
         'scheme': [S('s1', 'Meaning — refusal/disablement before due date; express or implied', 1.5, 'concept'), S('s2', 'Section 39', 1, 'provision'), S('s3', 'Option to rescind and sue immediately', 1, 'analysis'), S('s4', 'Option to wait and its risk', 1, 'analysis'), S('s5', 'Damages under Section 73 / mitigation', 0.5, 'provision')],
         'remarks': ['The risk of waiting (the contract remains alive for both sides) separates good answers from average ones.'],
         'mistakes': ['Saying the promisee must always wait for the due date.', 'Confusing anticipatory breach with impossibility.'],
         'tips': ['Give one express and one implied example.']},
        {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'legal',
         'q': f'Prakash Engineering agreed to buy {q_qty} steel rods from Vardhan Steels at {R(q_kp)} each, delivery on 1 August, for use in a bridge project with the State Government. Prakash did not mention the Government project to Vardhan. Vardhan failed to deliver; the market price on 1 August was {R(q_mp)}. Prakash bought rods in the market at that price, but the delay cost it a bonus of ₹2,00,000 under the Government contract. Prakash claims both the price difference and the lost bonus. Decide.',
         'model': [legal('Section 73: the injured party may recover compensation for loss that arose naturally in the usual course of things from the breach, or that both parties knew, when contracting, to be likely to result from it; not for remote or indirect loss. Hadley v. Baxendale: loss arising from special circumstances is recoverable only if those circumstances were communicated at the time of the contract.',
                         f'Contract price {R(q_kp)}; market price on the due date {R(q_mp)}; {q_qty} rods not delivered. Prakash bought at the market price (it mitigated). Vardhan was never told of the Government contract or the bonus.',
                         f'The price difference arises naturally from non-delivery: {q_qty} × ({R(q_mp)} − {R(q_kp)}) = {R(q_dmg)}. The lost bonus arises from special circumstances unknown to Vardhan, so it is remote and not within the parties\' contemplation.',
                         f'Prakash can recover {R(q_dmg)} as ordinary damages; the claim for the lost bonus of ₹2,00,000 fails.')],
         'scheme': [S('s1', 'Section 73 — natural/contemplated loss; no remote loss', 1.5, 'provision'), S('s2', 'Hadley v. Baxendale / need for notice of special circumstances', 1, 'provision'), S('s3', 'Computation of ordinary damages', 1.5, 'computation'), S('s4', 'Bonus is special loss without notice — not recoverable', 1, 'analysis'), S('s5', 'Conclusion', 1, 'conclusion')],
         'checks': cq,
         'remarks': ['Many candidates award the bonus because the loss "was caused" by the breach — causation alone is not enough; foreseeability at the time of contract is required.'],
         'mistakes': ['Using the price Prakash finally paid instead of the market price on the due date.', 'Not citing Hadley v. Baxendale or the notice requirement.'],
         'tips': ['Separate the two heads of claim in the analysis and conclude on each.']},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'legal',
         'q': f'A lease of a warehouse provides that if the tenant vacates before 3 years he will pay the landlord {R(q3_named)} "by way of penalty". The tenant leaves after 1 year. What can the landlord recover if his loss is (a) ₹1,80,000; (b) ₹4,10,000?',
         'model': [legal('Section 74: if the contract fixes a sum payable on breach (or contains any penalty stipulation), the injured party is entitled to reasonable compensation not exceeding the amount so named, whether the clause is called a penalty or liquidated damages.',
                         f'Named sum {R(q3_named)} "by way of penalty"; tenant broke the lease; landlord\'s loss (a) ₹1,80,000 or (b) ₹4,10,000.',
                         'The word "penalty" does not matter in India. The landlord gets reasonable compensation, but never more than the named sum.',
                         f'(a) {R(q3_a)}; (b) {R(q3_b)} only.')],
         'scheme': [S('s1', 'Section 74 — reasonable compensation not exceeding named sum', 1.5, 'provision'), S('s2', 'No distinction penalty / liquidated damages in India', 1, 'analysis'), S('s3', 'Answers (a) and (b)', 1.5, 'conclusion')],
         'checks': cq3,
         'remarks': ['Part (b) tests whether candidates know the named sum is a ceiling.'], 'mistakes': ['Awarding ₹4,10,000 in part (b).', 'Holding the clause void because it says "penalty".'], 'tips': ['Show both parts on separate lines in the conclusion.']},
        {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'Explain the doctrine of quantum meruit and state the conditions for its application.',
         'model': [p('Quantum meruit means "as much as he has earned". Where one party has done work or supplied goods under a contract and the contract is later discharged, the law allows him reasonable payment for what he has done. The remedy is restitutory, whereas damages are compensatory.'),
                   p('Conditions: (1) the original contract must have been discharged; (2) the claim must be made by the party who is not in default.'),
                   ul(['When an agreement is discovered to be void or a contract becomes void.', 'When something is done without any intention of doing it gratuitously.', 'When services are rendered under an express or implied contract but the fee is not fixed.', 'When one party abandons or refuses to perform.', 'Where a divisible contract is partly performed and the other party enjoys the benefit.', 'Where a lump-sum contract is completely but badly performed — lump sum less deduction for bad work.'])],
         'scheme': [S('s1', 'Meaning', 1, 'concept'), S('s2', 'Two conditions', 1.5, 'concept'), S('s3', 'Cases where it applies (any three)', 1.5, 'application')],
         'remarks': ['Both conditions must be stated to earn the middle mark.'], 'mistakes': ['Allowing the party in default to claim on quantum meruit.'], 'tips': ['Define in one line, then list the conditions as (1), (2).']},
    ]

    viva = [
        V('v1', 'What is anticipatory breach of contract, and what options does the promisee have?',
          'Anticipatory breach happens when, before the due date, a party refuses to perform or disables himself from performing his promise. Under Section 39 the promisee may end the contract at once and sue for damages immediately, or he may keep the contract alive and wait till the due date and then hold the other party liable.',
          [P('p1', 'Refusal or disablement before the due date', 4, 'before due date|before the due date|before the date|before time|before the time|prior to|in advance|before performance|ahead of|before it is due|before the day|earlier than'),
           P('p2', 'Option 1: rescind and sue immediately', 3, 'rescind|rescission|put an end|end the contract|terminat|sue immediately|sue at once|immediately sue|sue right away|sue straight away|sue now|claim damages immediately|claim damages at once|sue for damages immediately|without waiting'),
           P('p3', 'Option 2: keep the contract alive and wait for the due date', 3, 'wait|keep alive|keep the contract alive|keep it alive|treat as subsisting|treat it as operative|still operative|continue|until due date|till due date|till the due date|until the due date')], 'c2'),
        V('v2', 'What damages can be claimed under Section 73?',
          'Under Section 73 the injured party can claim compensation for loss that arose naturally in the usual course of things from the breach, and for loss which both parties knew at the time of contracting was likely to follow from such a breach. No compensation is given for remote or indirect loss, and the injured party must take reasonable steps to mitigate his loss.',
          [P('p1', 'Loss arising naturally in the usual course of things', 3, 'natural|naturally|usual course|ordinary course|direct loss|direct'),
           P('p2', 'Loss both parties knew to be likely when contracting', 3, 'knew|know|known|contemplat|foresee|foreseeab|aware|notice|special circumstance|likely to result'),
           P('p3', 'No compensation for remote or indirect loss', 3, 'not remote|no remote|remote not|remote is not|remote loss is not|remote losses are not|remote loss not|not for remote|not for any remote|not indirect|no indirect|excluding remote|except remote|remote or indirect loss not|cannot claim remote|can t claim remote|not recover remote|remote damages are not|remote damage not|no compensation for remote|not compensat remote'),
           P('p4', 'Duty to mitigate', 1, 'mitigat|minimi|reduce loss|reduce the loss|reasonable step')], 'c4'),
        V('v3', 'What principle was laid down in Hadley versus Baxendale?',
          'In Hadley versus Baxendale the carrier delayed delivery of a broken mill shaft. The court held that the mill owner could not recover his loss of profits, because the carrier was not told that the mill would stay idle. Only losses that arise naturally or that both parties contemplated at the time of the contract can be recovered; remote loss cannot.',
          [P('p1', 'Facts: carrier delayed delivery of a broken mill shaft', 2, 'shaft|crankshaft|mill|carrier'),
           P('p2', 'Loss of profit not recoverable — carrier not told the mill would be idle', 4, 'not told|not inform|no notice|not aware|did not know|didn t know|not know|unaware|not communicat|not made known|wasn t told|was not told|without notice|no knowledge'),
           P('p3', 'Only natural or contemplated losses recoverable; remote loss not', 4, 'natural|naturally|contemplat|usual course|foresee|remote|indirect')], 'c4'),
        V('v4', 'How does Indian law treat penalty and liquidated damages?',
          'Section 74 makes no distinction between penalty and liquidated damages. Whatever the clause is called, the court awards reasonable compensation not exceeding the amount named in the contract. The only exception is a bond given to the Government for a public duty, where the whole sum is payable.',
          [P('p1', 'No distinction between penalty and liquidated damages', 3, 'no distinction|not distinguish|does not distinguish|doesn t distinguish|no difference|not differentiat|does not differentiat|treated alike|treats them alike|treats both alike|treats both the same|treated the same|treated same|whatever it is called|whatever the clause is called|label does not matter|name does not matter|called penalty or'),
           P('p2', 'Reasonable compensation', 3, 'reasonable'),
           P('p3', 'Not exceeding the sum named — a ceiling', 4, 'not exceed|not exceeding|not more than|no more than|cannot exceed|can t exceed|up to|upto|maximum|ceiling|cap|capped|limit|within the amount|within the sum|less than or equal|never more')], 'c6'),
        V('v5', 'Explain quantum meruit and its conditions.',
          'Quantum meruit means as much as he has earned. A person who has done work or supplied goods under a contract that has been discharged can claim reasonable payment for what he has done. Two conditions apply: the original contract must have been discharged, and the claim must be made by the party who is not in default.',
          [P('p1', 'Meaning — as much as he has earned; payment for work done', 4, 'as much as|earned|deserved|value of work|work done|value of the work|reasonable payment|reasonable price|payment for work|paid for work|value of service|for what he has done'),
           P('p2', 'Original contract must have been discharged', 3, 'discharg|ended|terminat|broken|come to an end|repudiat|no longer exist'),
           P('p3', 'Claim by the party not in default', 3, 'not in default|not at fault|party not in breach|innocent party|non defaulting|not default|who has not defaulted|not the one in default|aggrieved party|injured party|not responsible for the breach')], 'c7'),
        V('v6', 'Name the kinds of damages that may be awarded for breach of contract.',
          'Damages may be ordinary damages for natural loss, special damages where special circumstances were made known, exemplary or vindictive damages for breach of promise to marry or wrongful dishonour of a cheque, nominal damages where no real loss is suffered, damages for deterioration caused by delay, and pre-fixed or liquidated damages.',
          [P('p1', 'Ordinary and special damages', 4, 'ordinary|general', 'special', min=2),
           P('p2', 'Exemplary / vindictive damages', 2, 'exemplary|vindictive|punitive'),
           P('p3', 'Nominal damages', 2, 'nominal|token'),
           P('p4', 'Deterioration by delay / pre-fixed (liquidated) damages', 2, 'deteriorat|liquidat|pre fixed|prefixed|penalty|delay')], 'c5'),
        V('v7', 'Distinguish specific performance from injunction as remedies for breach.',
          'Specific performance is an order of the court directing the party in breach to actually perform the contract, given where damages are not an adequate remedy. An injunction is an order of the court restraining a party from doing what he promised not to do.',
          [P('p1', 'Specific performance: court orders the party to perform the contract', 4, 'specific performance order|specific performance is an order|specific performance direct|specific performance compel|specific performance requir|specific performance force|specific performance court order|specific performance means court order|specific performance perform|specific performance carry out|specific performance actually perform|specific performance make'),
           P('p2', 'Injunction: court restrains the party from doing what he promised not to do', 4, 'injunction restrain|injunction stop|injunction prevent|injunction prohibit|injunction forbid|injunction refrain|injunction not to|injunction negative|injunction court restrain|injunction is an order restrain|injunction order restrain|injunction order stop|injunction order not|injunction order prevent|injunction order prohibit'),
           P('p3', 'Specific performance where damages are not an adequate remedy', 2, 'damages not adequate|damages are not adequate|damages inadequate|damages would not be adequate|damages not sufficient|damages are not sufficient|damages not enough|damages are not enough|money not adequate|money is not adequate|not an adequate remedy|not adequate remedy|inadequate remedy|money cannot compensate|unique|discretion')], 'c7'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Spice exporter\'s failed shipment', 'difficulty': 'hard',
        'case': ('Malabar Spices agreed to buy 1,000 kg of cardamom from Kerala Growers at ₹60 per kg for delivery on 1 March, to fulfil an export order. Malabar told Kerala Growers about the export order but not that the buyer would pay a special premium. '
                 'On 10 February Kerala Growers wrote that it would not deliver. Malabar accepted the refusal the same day and, on 1 March, the market price was ₹78 per kg. '
                 'The contract also said Kerala Growers would pay ₹50,000 "as penalty" for any default; Malabar\'s total proved loss (price difference plus lost premium) is ₹70,000.'),
        'mcqs': [
            M('k1a', 'The letter of 10 February is:', ['An anticipatory breach — Section 39', 'An actual breach', 'A counter offer', 'Not a breach until 1 March'], 0, 'Refusal before the due date.', 'core'),
            M('k1b', 'Ordinary damages measured on the price difference are:', [R(k_ord), R(78000), R(60000), R(12000)], 0, 'Quantity × (market price on the due date − contract price) = 1,000 × (78 − 60).', 'moderate', '1000*(78-60)'),
            M('k1c', 'The lost special premium is:', ['Not recoverable as ordinary loss — the special circumstance was not communicated', 'Always recoverable', 'Recoverable as exemplary damages', 'Recoverable as nominal damages'], 0, 'Hadley v. Baxendale — special loss needs notice at the time of contracting.', 'hard'),
            M('k1d', 'Under Section 74, the upper limit (ceiling) on the compensation Malabar can be awarded under the clause is:', [R(k_cap), R(70000), R(18000), 'Nothing — penalties are void'], 0, 'Reasonable compensation not exceeding the named sum: the ceiling is ₹50,000 (the court fixes a reasonable amount within it and may award less). The word "penalty" does not make the clause void, and a loss above the named sum cannot lift the ceiling.', 'hard', '50000'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch02', 'n': 5, 'title': 'Breach of Contract and its Remedies',
        'outcomes': ['Distinguish actual breach from anticipatory breach and state the promisee\'s options under Section 39.', 'Compute damages under Section 73, applying the rule in Hadley v. Baxendale, the duty to mitigate and the kinds of damages.',
                     'Apply Section 74 to penalty and liquidated-damages clauses, including the Government-bond exception.', 'Explain the other remedies — rescission, quantum meruit, specific performance and injunction — and when each is available.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 50}, 'prereq': ['fnd-p2-ch02-u04'],
                 'exam_tip': 'Damages problems are frequent: compute the price difference neatly, then decide each head of special loss on the notice test (Hadley v. Baxendale). For any "penalty" clause, write "reasonable compensation not exceeding the sum named — Section 74".'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {'summary': ['Breach: actual (on or during performance) or anticipatory (before the due date — Section 39).', 'Anticipatory breach: rescind and sue at once, or keep alive and wait (risk of later discharge).',
                                 'Section 73: natural loss or loss contemplated by both parties; no remote/indirect loss; mitigation (Hadley v. Baxendale).', 'Kinds: ordinary, special, exemplary (marriage promise, cheque dishonour), nominal, deterioration by delay, pre-fixed.',
                                 'Section 74: no penalty/liquidated distinction; reasonable compensation not exceeding the named sum; Government bond for public duty — whole sum.', 'Other remedies: rescission (Section 75 compensation), quantum meruit (contract discharged, claimant not in default), specific performance, injunction.'],
                     'remember': ['Section 39 anticipatory breach · 73 compensation · 74 named sum · 75 compensation on rightful rescission.', 'Damages for goods = quantity × (market price on due date − contract price).'],
                     'traps': ['Special loss needs notice at the time of contracting — not after.', 'The named sum is a ceiling: never award more, may award less.', 'Quantum meruit is not available to the party in default.', 'Courts do not force personal service — they may grant an injunction on a negative promise.']},
        'quickref': [{'k': 'Section 39', 'v': 'Refusal/disablement before due date → promisee may end the contract'}, {'k': 'Section 73', 'v': 'Natural or contemplated loss; no remote loss; mitigate'},
                     {'k': 'Hadley v. Baxendale', 'v': 'Special loss recoverable only if communicated at contract time'}, {'k': 'Section 74', 'v': 'Reasonable compensation ≤ sum named; Government bond: whole sum'},
                     {'k': 'Section 75', 'v': 'Party rightfully rescinding gets compensation'}, {'k': 'Exemplary damages', 'v': 'Breach of promise to marry · wrongful dishonour of cheque'},
                     {'k': 'Quantum meruit', 'v': 'Contract discharged + claimant not in default'}, {'k': 'Damages formula', 'v': 'Qty × (market price on due date − contract price)'}],
        'viva': viva, 'cases': cases,
    }
