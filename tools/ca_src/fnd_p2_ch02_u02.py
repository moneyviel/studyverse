"""CA Foundation · Paper 2 Business Laws · Chapter 2 The Indian Contract Act, 1872 · Unit 2 Consideration.
Original explanations and problems; sections and leading cases are cited by name only."""
from lib import *
from ca_viva import P, ALT, V
from ca_cases import M

UID = 'fnd-p2-ch02-u02'


def Q(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check: d['check'] = check
    return d


def S(sid, pt, m, skill): return {'id': sid, 'pt': pt, 'm': m, 'skill': skill}


def build():
    # ---- figures ----
    c2 = Checks()
    debt = 240000
    promised = 180000
    recover = c2.add('180000', 'enforceable amount = amount promised in writing (not the old debt)')
    unrec = c2.add('240000-180000', 'part of the old debt that stays irrecoverable')

    ck = Checks()
    ck_spent = ck.add('210000+65000', 'liability incurred by the committee on the faith of the promise')
    ck_rec = ck.add('250000', 'amount recoverable: the promised sum (liability of 2,75,000 incurred on its faith exceeds it)')

    cq3 = Checks()
    q3_amt = cq3.add('300000', 'amount recoverable under the written promise')

    cc = Checks()
    k_bal = cc.add('500000-125000', 'loan balance outstanding when it became time-barred')
    k_pay = cc.add('375000*60/100', 'amount promised in writing (60% of the balance)')

    exceptions = table(['Exception', 'Provision', 'Conditions'], [
        ['Natural love and affection', 'Section 25(1)', 'Expressed in writing; registered; parties in near relation; made out of natural love and affection'],
        ['Compensation for past voluntary service', 'Section 25(2)', 'Service done voluntarily, for the promisor, who existed then (or did something the promisor was legally bound to do); promise to compensate wholly or partly'],
        ['Promise to pay a time-barred debt', 'Section 25(3)', 'In writing; signed by the debtor or his authorised agent; to pay the debt wholly or in part'],
        ['Completed gift', 'Explanation 1 to Section 25', 'A gift actually made is valid between donor and donee without consideration'],
        ['Agency', 'Section 185', 'No consideration is needed to create an agency'],
        ['Bailment', 'Section 148 (gratuitous bailment)', 'Delivery of goods for a purpose can be made without any charge'],
        ['Charity / subscription', 'Kedarnath v. Gorie Mohammad', 'Binding where the promisee has incurred a liability on the faith of the promise'],
    ], title='Agreements valid without consideration')

    concepts = [
        {'id': 'c1', 'title': 'What is consideration? — Section 2(d)', 'body': [
            'Consideration is the "something in return" (quid pro quo) for a promise — the price for which the promise is bought. In Misa v. Currie it was explained as either a benefit to one side (a right, interest or profit) or a detriment to the other (a loss, forbearance or responsibility undertaken).',
            'Section 2(d) in plain words: if the promisor wants something done (or not done), and the promisee or some other person has done it, is doing it, or promises to do it (or to refrain), then that act, forbearance or promise is the consideration for the promise.',
            'So consideration may be: an act (doing something — e.g. supplying goods on credit), an abstinence or forbearance (not doing something — e.g. agreeing not to file a suit, or not to open a rival shop nearby), or a promise to do or not to do something.',
            'Key elements of the definition: (1) at the desire of the promisor; (2) by the promisee or any other person; (3) past ("has done"), present ("does") or future ("promises to do"); (4) an act, abstinence or promise. Consideration need not be money.'],
         'analogy': 'A promise without consideration is a gift voucher with no shop behind it — nice words, nothing the law will cash.',
         'work': 'When a client signs a "comfort letter" or a waiver, the CA asks: what did the client get in return? If nothing, the letter may not be enforceable unless an exception under Section 25 applies.'},
        {'id': 'c2', 'title': 'Legal rules — who gives it, and when', 'body': [
            'Must move at the desire of the promisor: an act done at the request of a third party, or done voluntarily without any request, is not consideration. In Durga Prasad v. Baldeo, a market was built at the Collector\'s request, not the defendant\'s; the defendant\'s later promise of commission was without consideration and void.',
            'May move from the promisee or any other person: under Indian law consideration need not come from the promisee himself. In Chinnaya v. Ramayya, a mother gifted property to her daughter on the condition that the daughter would pay an annual sum to the mother\'s brother; the daughter promised the brother, and he could enforce it although the consideration (the property) came from the mother. There can be a stranger to the consideration, but not a stranger to the contract.',
            'Executed and executory: consideration already performed is executed (e.g. advance paid); consideration still to be performed is executory (e.g. a promise to deliver next month). One side\'s may be executed and the other\'s executory.',
            'Past, present or future: past consideration supports a promise in India if the past act was done at the desire of the promisor (e.g. work done last month at B\'s request, for which B now promises to pay). A cash sale is present consideration; promises to be performed later are future consideration.'],
         'analogy': 'Consideration is like a ticket the promisor asks for: anyone may buy it for you (any other person), but it must be the ticket the promisor asked for (desire of the promisor).',
         'work': 'In group companies, a parent often pays or guarantees for a subsidiary. Because consideration may move from "any other person", the bank\'s contract with the guarantor is valid even though the loan money goes to the subsidiary.'},
        {'id': 'c3', 'title': 'Legal rules — what qualifies as consideration', 'body': [
            'Need not be adequate: the law does not weigh whether the bargain is fair; it is enough that there is something of value. Explanation 2 to Section 25: an agreement freely consented to does not become void just because the price is low — but the court may consider gross inadequacy as evidence when deciding whether consent was really free (e.g. a ₹50 lakh flat sold for ₹5 lakh may point to coercion, undue influence or fraud).',
            'Doing what one is already legally bound to do is not consideration: e.g. a promise to pay a witness extra for giving evidence, or to pay a doctor in a government hospital extra for treatment that is his duty. But doing more than the legal duty can be good consideration, if not against public policy.',
            'Must be real, not illusory: physically impossible (bringing the dead back to life), legally impossible or uncertain promises are no consideration.',
            'Must be lawful: consideration that is illegal, immoral or opposed to public policy makes the agreement void (Section 23) — e.g. money paid to get someone a government job through influence.'],
         'analogy': 'The law checks that there is a price tag, not whether the price is right.',
         'work': 'In related-party transactions at very low prices, CAs know the contract is not void for inadequacy, but tax and company law (transfer pricing, related-party approvals) may still require arm\'s-length pricing.'},
        {'id': 'c4', 'title': 'Suit by a third party — doctrine of privity of contract', 'body': [
            'General rule: only a party to a contract can sue on it. A person who is not a party — a stranger to the contract — cannot enforce it, even if the contract was made for his benefit. Example: P owes money to Q, sells his car to R, and R promises P to pay Q. If R does not pay, Q cannot sue R; Q is a stranger to the contract between P and R (Q can still sue P on the original debt).',
            'Stranger to consideration ≠ stranger to contract: in India consideration may come from a third person (Chinnaya v. Ramayya), and a party to the contract can sue even if he did not furnish the consideration. But someone outside the contract altogether generally has no right to sue on it.'],
         'analogy': 'Only the people who signed the deal can walk into court about it; the neighbour who would have benefited stays outside, unless the law opens a special door.',
         'work': 'When a customer\'s contract is with a distributor, the customer usually cannot sue the manufacturer on that contract — which is why CAs review warranty terms and back-to-back contracts in supply chains.'},
        {'id': 'c5', 'title': 'Exceptions — when a stranger to the contract can sue', 'body': [
            'Trust: a beneficiary can enforce the trust against the trustee, though not a party to the arrangement between the settlor and the trustee.',
            'Family settlement: where a family arrangement is reduced to writing, family members for whose benefit it is made can enforce it (e.g. two sons agree on partition to pay their mother a monthly allowance; she can sue them).',
            'Marriage arrangements: a person (e.g. a wife) for whose benefit provision is made in an arrangement connected with marriage can enforce it.',
            'Assignment: an assignee of the benefit of a contract (e.g. a son to whom an insurance policy is assigned, or a buyer of book debts) can enforce it, provided no personal skill is involved.',
            'Acknowledgement or estoppel: where the promisor acknowledges, by conduct or words, that he holds money for the third party, he becomes liable to that party (L gives M ₹20,000 for N; M tells N he holds it for him; N can recover from M).',
            'Covenant running with the land: a buyer of land who takes it with notice of a restriction or duty attached to the land is bound by it, and it can be enforced against him.',
            'Contracts through an agent: the principal can enforce a contract made by his agent within his authority, though the principal did not personally deal with the other side.'],
         'analogy': 'Seven side doors into the courtroom for people who did not sign: Trust, Family, Marriage, Assignment, Acknowledgement, Land, Agent.',
         'work': 'Receivable factoring and securitisation rely on assignment: the factor (assignee) collects directly from the debtor. CAs check the assignment deed and notice to the debtor.'},
        {'id': 'c6', 'title': 'No consideration, no contract — and the Section 25 exceptions', 'body': [
            'Section 25: an agreement made without consideration is void, except in the cases below.',
            'Natural love and affection [Section 25(1)]: the agreement must be (i) made out of natural love and affection, (ii) between parties standing in a near relation, (iii) expressed in writing and (iv) registered. All four are needed — a promise between friends, or an unregistered promise between brothers, fails.',
            'Compensation for past voluntary services [Section 25(2)]: a promise to pay (fully or partly) someone who has already, of his own accord, done something for the promisor (or something the promisor was legally compellable to do). Conditions: the service was voluntary, done for the promisor, the promisor was in existence at that time, and the promisor now promises to compensate. Example: Tara finds Raghav\'s lost laptop and returns it; Raghav promises her ₹5,000 — enforceable.',
            'Promise to pay a time-barred debt [Section 25(3)]: a written promise, signed by the debtor or his authorised agent, to pay wholly or in part a debt that the creditor could have enforced but for the law of limitation, is enforceable — for the amount promised.'],
         'blocks': [exceptions],
         'analogy': 'Section 25 is a locked door ("void") with three keys cut in the section itself — love-and-affection in registered writing, past voluntary service, written promise for a time-barred debt — and a few master keys outside it.',
         'work': 'A CA confirming balances notices a debt over three years old. A fresh signed written promise from the debtor to pay (Section 25(3)) makes it enforceable again — relevant to whether the receivable is still good.'},
        {'id': 'c7', 'title': 'Other cases where consideration is not needed', 'body': [
            'Agency — Section 185: an agency can be created without any consideration.',
            'Completed gift — Explanation 1 to Section 25: a gift actually made (delivered or transferred according to law) is valid between donor and donee; the donor cannot take it back for want of consideration. A mere promise to make a gift in future is not enforceable unless Section 25(1) applies.',
            'Bailment — Section 148: goods may be delivered for a purpose without any charge (gratuitous bailment), e.g. leaving your goods in a friend\'s godown.',
            'Charity: a promise to subscribe to a charitable cause becomes enforceable where the promisee, relying on it, has undertaken a liability (Kedarnath v. Gorie Mohammad).'],
         'analogy': 'Gifts already handed over, favours by agents, goods left for safe keeping and charity relied upon — four places where the law does not ask "what did you get?"',
         'work': 'NGO and trust audits often involve pledged donations; a CA may treat a pledge as recoverable where the trust has committed expenditure on the strength of it.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Promise to pay a third party — privity', 'difficulty': 'core', 'minutes': 6,
         'q': 'Vikram owes ₹90,000 to Farah. Vikram sells his motorcycle to Neeraj, who promises Vikram that he will pay ₹90,000 to Farah out of the price. Neeraj does not pay. Can Farah sue Neeraj?',
         'solution': [legal('Doctrine of privity: only a party to a contract can sue on it; a stranger to the contract cannot, unless the case falls within a recognised exception (trust, family settlement, marriage arrangement, assignment, acknowledgement/estoppel, covenant running with land, agency).',
                            'The contract is between Vikram and Neeraj. Farah is not a party to it. Nothing shows that Neeraj acknowledged to Farah that he held money for her, and no exception applies.',
                            'Farah is a stranger to the contract, so she cannot enforce Neeraj\'s promise. Vikram, a party, can sue Neeraj; Farah\'s own claim is against Vikram on the original debt.',
                            'Farah cannot sue Neeraj. She may recover ₹90,000 from Vikram, and Vikram may sue Neeraj for breach.')]},
        {'id': 'i2', 'title': 'Written promise for part of a time-barred debt', 'difficulty': 'moderate', 'minutes': 7,
         'q': f'Kiran lent {R(debt)} to Om. Om never paid and the debt became time-barred. Om now signs a letter: "I will pay you {R(promised)} in full settlement by 30 June." He then refuses to pay. How much can Kiran recover?',
         'solution': [legal('Section 25(3): a promise in writing, signed by the debtor or his authorised agent, to pay wholly or in part a debt barred by limitation is a valid contract, though without fresh consideration.',
                            f'The original debt of {R(debt)} is time-barred. Om has signed a written promise to pay {R(promised)}.',
                            'All conditions are met: written, signed by the debtor, a promise to pay part of a debt barred only by limitation. The contract is for the amount promised, not for the original debt.',
                            f'Kiran can recover {R(recover)}. The balance of {R(unrec)} remains irrecoverable.'),
                      wn('Working', f'Enforceable amount = amount promised in writing = {R(recover)}; old debt {R(debt)} − {R(recover)} = {R(unrec)} not recoverable.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Pledge to a school library fund', 'difficulty': 'moderate', 'minutes': 6,
         'q': 'Mr. Bansal promises the managing committee of a local school ₹2,50,000 for a new library. Relying on the promise the committee orders furniture worth ₹2,10,000 and books worth ₹65,000. Mr. Bansal then withdraws. Can the committee recover anything, and how much?',
         'solution': [legal('Section 25: an agreement without consideration is void. But where the promisee has incurred a liability on the faith of a promise to contribute to a charitable cause, the promise is enforceable (Kedarnath v. Gorie Mohammad).',
                            f'The committee placed orders worth {R(ck_spent)} relying on Mr. Bansal\'s promise of ₹2,50,000.',
                            'The committee changed its position by incurring liabilities on the faith of the promise, so the promise becomes enforceable. The claim cannot exceed the sum promised.',
                            f'The committee can recover the promised {R(ck_rec)} from Mr. Bansal; the further {R(ck_spent - ck_rec)} it committed beyond the promise is its own responsibility.'),
                      wn('Working', f'Liability incurred: ₹2,10,000 + ₹65,000 = {R(ck_spent)}, which is more than the ₹2,50,000 promised; recoverable = the promised {R(ck_rec)}.')],
         'checks': ck},
        {'id': 'i4', 'title': 'Extra payment for a legal duty', 'difficulty': 'core', 'minutes': 5,
         'q': 'A trader promises a police constable ₹10,000 if he investigates a theft in the trader\'s shop. Later the trader refuses to pay. Can the constable recover?',
         'solution': [legal('Performance of what a person is already legally bound to do is not consideration for a promise; such a promise is also opposed to public policy.',
                            'Investigating a reported theft is the constable\'s official duty.',
                            'The constable gave nothing beyond his legal duty, so there is no consideration for the trader\'s promise.',
                            'The agreement is void; the constable cannot recover ₹10,000.')]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'A debtor\'s balance confirmation', 'role': 'Audit assistant in a CA firm', 'situation': 'A client has a ₹6 lakh receivable from a customer, unpaid for four years. The customer has just signed and returned a balance confirmation letter that says "we confirm and will pay the balance of ₹6 lakh".',
         'steps': ['Note that the debt is likely time-barred (limitation for recovery of money is generally three years).', 'A written, signed promise to pay a time-barred debt wholly or in part is enforceable under Section 25(3).', 'Check that the letter is signed by the customer or its authorised signatory and clearly promises payment.', 'Record the conclusion in the working papers for assessing whether the receivable is recoverable.'],
         'takeaway': 'A simple balance confirmation can revive the legal enforceability of an old debt.', 'think': 'What if the letter only said "we note your balance of ₹6 lakh" without any promise?',
         'answer': 'A mere acknowledgement without a promise to pay does not satisfy Section 25(3), which requires a promise to pay.'},
        {'id': 'j2', 'title': 'Family settlement deed', 'role': 'CA advising a family business', 'situation': 'Two brothers are dividing the family business. Their sister wants the deed to provide her a monthly payment, though she is not signing it.',
         'steps': ['Explain privity: normally a non-party cannot sue.', 'A written family settlement is an exception — family members for whose benefit it is made can enforce it.', 'Advise that the settlement be in writing and clearly state her entitlement.'],
         'takeaway': 'Putting the family arrangement in writing protects the beneficiary who does not sign it.'},
    ]

    mcqs = [
        Q('m1', 'Under Section 2(d), consideration must be given at the desire of:', ['The promisor', 'The promisee', 'A third party', 'The court'], 0, 'An act done at anyone else\'s desire is not consideration (Durga Prasad v. Baldeo).', 'c2'),
        Q('m2', 'Which statement about consideration is FALSE?', ['It must be adequate', 'It may move from any other person', 'It may be past, present or future', 'It must be real and not illusory'], 0, 'Explanation 2 to Section 25 — inadequacy alone does not make an agreement void.', 'c3'),
        Q('m3', 'In Chinnaya v. Ramayya it was held that:', ['Consideration may move from a third person', 'A stranger to a contract can always sue', 'Past consideration is invalid', 'Consideration must be adequate'], 0, 'The brother could enforce the daughter\'s promise although the consideration came from the mother.', 'c2', 'moderate'),
        Q('m4', 'Bhanu saves Chetan\'s goods from a fire without being asked. Chetan does not promise anything. Bhanu:', ['Cannot claim any reward — the act was voluntary and not at Chetan\'s desire', 'Can claim reasonable reward under Section 2(d)', 'Can claim under Section 25(3)', 'Can claim double the value saved'], 0, 'No desire of the promisor and no promise to compensate, so no contract. (Had Chetan later promised a reward, Section 25(2) could apply.)', 'c2'),
        Q('m5', 'A promise to pay a sum to a witness for giving evidence in court is:', ['Void — no consideration, as giving evidence is a legal duty', 'Valid', 'Voidable at the witness\'s option', 'Valid if in writing'], 0, 'Doing what one is legally bound to do is not consideration.', 'c3'),
        Q('m6', 'A promise to pay a time-barred debt is enforceable if it is:', ['In writing and signed by the debtor or his authorised agent', 'Oral but made before witnesses', 'Registered but not signed', 'Made by the creditor'], 0, 'Section 25(3).', 'c6'),
        Q('m7', 'Which is NOT required for an agreement under Section 25(1)?', ['Adequate consideration', 'Natural love and affection', 'Near relationship', 'Writing and registration'], 0, 'Section 25(1) is precisely a case of no consideration.', 'c6', 'moderate'),
        Q('m8', 'Raju, out of affection, promises in a written and registered deed to give his friend Sohan ₹1 lakh. The promise is:', ['Not enforceable — friends are not in near relation', 'Enforceable under Section 25(1)', 'Enforceable as past consideration', 'Enforceable because it is registered'], 0, 'All conditions, including near relationship, must be satisfied.', 'c6', 'moderate'),
        Q('m9', 'No consideration is necessary to create an agency under:', ['Section 185', 'Section 25(2)', 'Section 148', 'Section 2(d)'], 0, 'Section 185 of the Contract Act.', 'c7'),
        Q('m10', '"A stranger to a contract cannot sue" is known as the doctrine of:', ['Privity of contract', 'Stare decisis', 'Quantum meruit', 'Caveat emptor'], 0, 'Privity of contract — subject to exceptions such as trust and family settlement.', 'c4'),
        Q('m11', 'Which of these is NOT an exception to the doctrine of privity?', ['A creditor of a seller suing the buyer who promised the seller to pay him', 'Beneficiary under a trust', 'Assignee of an insurance policy', 'Covenant running with land'], 0, 'The creditor is a plain stranger to the contract unless the buyer acknowledged the debt to him.', 'c5', 'moderate'),
        Q('m12', f'A debt of {R(350000)} is time-barred. The debtor signs a written promise to pay {R(300000)}. The creditor can recover:', [R(q3_amt), R(350000), R(50000), 'Nothing'], 0, 'Section 25(3) — the contract is for the amount promised in writing.', 'c6', 'moderate', check='min(350000, 300000)'),
        Q('m13', 'A cash sale of goods over the counter is an example of:', ['Present consideration', 'Past consideration', 'Future consideration', 'No consideration'], 0, 'Payment and delivery happen together.', 'c2'),
    ]

    questions = [
        {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': '"Consideration must be adequate to form a valid contract." Comment, with reference to the Indian Contract Act, 1872.',
         'model': [p('The statement is not correct. A contract must be supported by consideration, but the law does not require the consideration to be equal in value to the promise.'),
                   p('Explanation 2 to Section 25 provides that an agreement to which the promisor has freely consented is not void merely because the consideration is inadequate. The adequacy of the bargain is for the parties to judge when they contract, not for the court later (Bolton v. Madden).'),
                   p('However, the consideration must have some value in the eyes of the law — it must be real, not illusory. And gross inadequacy may be taken into account by the court as evidence when deciding whether the promisor\'s consent was free, i.e. not caused by coercion, undue influence or fraud.'),
                   p('Conclusion: consideration need not be adequate; it must merely exist and be of some value, and inadequacy matters only as evidence on free consent.')],
         'scheme': [S('s1', 'States the statement is incorrect', 0.5, 'conclusion'), S('s2', 'Explanation 2 to Section 25', 1.5, 'provision'), S('s3', 'Must have some value / real', 1, 'concept'), S('s4', 'Inadequacy as evidence of lack of free consent', 1, 'analysis')],
         'remarks': ['Good answers cite Explanation 2 to Section 25 and the free-consent link; weak answers just say "inadequacy does not matter".'],
         'mistakes': ['Saying grossly inadequate consideration makes the agreement void automatically.', 'Citing Section 2(d) only.'],
         'tips': ['Start with "The statement is incorrect", then provision, then the exception, then conclusion.']},
        {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'legal',
         'q': 'Mrs. Kamala transfers her shop to her son Dev by a gift deed on the condition that Dev will pay ₹15,000 a month to Kamala\'s brother Hari for life. On the same day Dev executes a writing in Hari\'s favour agreeing to pay. Dev pays for a few months and then stops, pleading that Hari gave him no consideration and that Hari is not a party to the gift. Decide.',
         'model': [legal('Section 2(d): consideration may be furnished by the promisee or any other person, at the desire of the promisor. So a person who has not himself furnished consideration may still enforce a promise made to him (Chinnaya v. Ramayya). Only a stranger to the contract — not a stranger to the consideration — is barred from suing.',
                         'Kamala gifted the shop to Dev on a condition, which Dev accepted, that he would pay Hari. Dev made a written promise directly to Hari to pay ₹15,000 a month.',
                         'Dev\'s promise to Hari is a contract between Dev and Hari. The consideration for it — the shop — moved from Kamala, a third person, which is permitted under Section 2(d). Hari is a party to the promise (Dev promised him in writing), so he is only a stranger to the consideration, not to the contract.',
                         'Dev\'s plea fails. Hari can sue Dev for the arrears and future payments of ₹15,000 a month.')],
         'scheme': [S('s1', 'Section 2(d) — consideration may move from any other person', 1.5, 'provision'), S('s2', 'Stranger to consideration vs stranger to contract / privity', 1.5, 'provision'), S('s3', 'Application: shop from Kamala is consideration; Dev promised Hari', 1.5, 'analysis'), S('s4', 'Conclusion: Hari can recover', 1, 'conclusion'), S('s5', 'Case law cited (Chinnaya v. Ramayya)', 0.5, 'provision')],
         'remarks': ['This is a classic ICAI-type problem; the distinction between stranger to consideration and stranger to contract carries most of the marks.'],
         'mistakes': ['Applying privity to deny Hari\'s claim.', 'Treating the gift as without consideration and therefore void.'],
         'tips': ['Use the four-part Provision → Facts → Analysis → Conclusion layout.', 'Name the case once; do not narrate its facts at length.']},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'legal',
         'q': 'Explain with reasons whether the following are enforceable: (a) Anu, out of love, promises orally to give her brother ₹2 lakh on his birthday; (b) Anu gives her friend a gold chain on her birthday and later wants it back because she received nothing in return.',
         'model': [legal('Section 25: an agreement without consideration is void, except, among others, (i) under Section 25(1) a written and registered agreement made out of natural love and affection between near relatives, and (ii) under Explanation 1, a gift actually made.',
                         '(a) Anu\'s promise to her brother is oral and not registered. (b) The chain has actually been handed over to the friend as a gift.',
                         '(a) Though brother and sister are near relatives and the promise is out of love, the writing and registration conditions are not met, so Section 25(1) does not apply. (b) A completed gift needs no consideration; Explanation 1 protects it.',
                         '(a) Not enforceable. (b) The gift is valid; Anu cannot take the chain back.')],
         'scheme': [S('s1', 'Section 25 rule and Section 25(1) conditions', 1, 'provision'), S('s2', 'Explanation 1 — completed gift', 1, 'provision'), S('s3', '(a) applied and concluded', 1, 'analysis'), S('s4', '(b) applied and concluded', 1, 'conclusion')],
         'remarks': ['Candidates often miss that all four conditions of Section 25(1) are cumulative.'],
         'mistakes': ['Treating near relationship alone as sufficient.', 'Treating a completed gift as revocable for want of consideration.'],
         'tips': ['Answer each part separately with its own one-line conclusion.']},
        {'id': 'q4', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
         'q': '"No consideration, no contract." Discuss the exceptions to this rule.',
         'model': [p('Section 25 lays down that an agreement made without consideration is void. The exceptions are:'),
                   ul(['Natural love and affection — Section 25(1): written, registered, between parties in near relation, out of natural love and affection.',
                       'Compensation for past voluntary services — Section 25(2): a promise to compensate a person who voluntarily did something for the promisor, or something he was legally compellable to do.',
                       'Promise to pay a time-barred debt — Section 25(3): in writing, signed by the debtor or his authorised agent, wholly or in part.',
                       'Completed gift — Explanation 1 to Section 25: a gift actually made is valid.',
                       'Agency — Section 185: no consideration needed to create an agency.',
                       'Bailment — gratuitous bailment needs no consideration.',
                       'Charity — enforceable where the promisee has incurred liability on the faith of the promise (Kedarnath v. Gorie Mohammad).'])],
         'scheme': [S('s1', 'General rule — Section 25', 0.5, 'provision'), S('s2', 'Section 25(1) with conditions', 1, 'provision'), S('s3', 'Section 25(2) with conditions', 1, 'provision'), S('s4', 'Section 25(3) with conditions', 1, 'provision'), S('s5', 'Gift, agency, bailment, charity', 1.5, 'concept')],
         'remarks': ['Listing only names without conditions earns about half marks.'],
         'mistakes': ['Omitting "registered" under Section 25(1).', 'Writing that an oral promise revives a time-barred debt.'],
         'tips': ['Give the sub-section number with each exception — examiners look for it.']},
    ]

    viva = [
        V('v1', 'Define consideration as per Section 2(d) of the Indian Contract Act.',
          'Consideration is an act, abstinence or promise done or made at the desire of the promisor, by the promisee or any other person. It may be past, present or future, that is, something that has been done, is being done or is promised to be done.',
          [P('p1', 'At the desire of the promisor', 3, ALT('desire {p}', 'request {p}', '{p} desire', '{p} request', '{p} ask', '{p} want', 'desire of the {p}', 'asked by the {p}', 'wish of the {p}', p=('promisor', 'proposer', 'offeror'))),
           P('p2', 'By the promisee or any other person', 3, 'any other person|other person|third person|third party|anyone else|someone else|any person'),
           P('p3', 'An act, abstinence (forbearance) or promise', 2, 'act|doing', 'abstin|abstain|forbear|not doing|refrain', 'promise', min=2),
           P('p4', 'Past, present or future', 2, 'past', 'present|future', min=2)], 'c1'),
        V('v2', 'Must consideration be adequate for a valid contract?',
          'No. Consideration need not be adequate. Under Explanation 2 to Section 25, an agreement freely consented to is not void merely because the consideration is inadequate. It must only have some value. But inadequacy can be taken as evidence on whether consent was free.',
          [P('p1', 'Consideration need not be adequate', 5, 'need not adequate|not need adequate|need not be adequate|not necessarily adequate|not have to be adequate|not to be adequate|does not need to be adequate|not required to be adequate|inadequacy does not|inadequate consideration does not|not void merely|not void just|not void only|not void because inadequate|not void inadequate|does not matter|adequacy not|adequacy is not|adequacy does not|not equal value|need not be equal|need not equal|not necessarily equal'),
           P('p2', 'Explanation 2 to Section 25', 2, 'explanation 2|section 25|explanation two'),
           P('p3', 'Inadequacy may be evidence of lack of free consent', 3, 'evidence|free consent|freely|coercion|undue influence|fraud|consent free|consent not free|consent was not free|not free consent|lack of free consent|not freely|consent was free|whether consent')], 'c3'),
        V('v3', 'Can a stranger to a contract sue? How is that different from a stranger to consideration?',
          'Under the doctrine of privity, a stranger to the contract cannot sue on it. But in India consideration may move from the promisee or any other person, so a stranger to the consideration who is a party to the contract can sue, as in Chinnaya versus Ramayya. Exceptions to privity include trust, family settlement and assignment.',
          [P('p1', 'A stranger to the contract cannot sue (privity)', 4, 'stranger to contract cannot sue|stranger to the contract cannot sue|stranger contract cannot sue|stranger to a contract cannot sue|third party cannot sue|non party cannot|not a party cannot|only party can sue|only parties can sue|only a party|only the parties|only those who are parties|cannot sue on the contract|privity'),
           P('p2', 'Consideration may move from a third person — a stranger to consideration who is a party can sue (Chinnaya v. Ramayya)', 4, 'consideration move from any other|consideration move from third|consideration move from another|consideration move from someone|consideration move from stranger|consideration need not move from promisee|need not move from the promisee|not necessarily from the promisee|consideration from third|consideration from any other|consideration come from third|consideration come from another|consideration come from someone|consideration from someone else|consideration from another person|chinnaya|chinnayya|ramayya'),
           P('p3', 'Exceptions — trust, family settlement, marriage, assignment, estoppel, land covenant, agency', 2, 'trust|family|marriage|assign|acknowledg|estoppel|covenant|agent|agency', min=1)], 'c4'),
        V('v4', 'State the exceptions under Section 25 where an agreement without consideration is valid.',
          'First, a written and registered agreement made out of natural love and affection between near relatives. Second, a promise to compensate someone for past voluntary services. Third, a written and signed promise to pay a time-barred debt. Also completed gifts, agency under Section 185, bailment and charity where liability was incurred.',
          [P('p1', 'Natural love and affection — written, registered, near relatives', 4, 'love|affection', 'regist', 'near relat|close relat|relative|near relation', min=2),
           P('p2', 'Past voluntary services', 3, 'past voluntary|voluntary service|voluntarily done|past service|voluntarily did|voluntary act|did voluntarily|done voluntarily'),
           P('p3', 'Time-barred debt — written promise', 3, 'time barred|barred debt|limitation|time-barred')], 'c6'),
        V('v5', 'When is a promise to pay a time-barred debt enforceable?',
          'Under Section 25(3), a promise to pay a time-barred debt is enforceable without fresh consideration if it is made in writing and signed by the debtor or his authorised agent. It may be to pay the debt wholly or in part, and the creditor can recover the amount promised.',
          [P('p1', 'Promise must be in writing', 3, 'must be in writing|must be written|should be in writing|should be written|has to be in writing|has to be written|in writing and signed|written and signed|written promise|promise in writing|promise made in writing|made in writing|put in writing|reduced to writing|writing signed|signed writing'),
           P('p2', 'Signed by the debtor or his authorised agent', 4, 'signed by debtor|signed by the debtor|signed by him|signed by the person|debtor sign|signed by his agent|signed by agent|authorised agent|authorized agent|debtor must sign|debtor has signed|debtor signs|sign it'),
           P('p3', 'To pay wholly or in part — recoverable to the amount promised', 3, 'wholly|in part|partly|part of|amount promised|promised amount|whole or part|full or part|part payment|amount he promised|amount stated')], 'c6'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Loose ends after Mr. Saxena\'s retirement', 'difficulty': 'moderate',
        'case': (f'Mr. Saxena lent ₹5,00,000 to his former employee Pawan, who repaid ₹1,25,000 and then stopped. The balance became time-barred. Pawan now signs a letter promising to pay 60% of the balance. '
                 'Separately, Mr. Saxena\'s neighbour Leela, without being asked, watered his garden for a month while he was away; on return he promised her ₹3,000. '
                 'Mr. Saxena also orally promised his nephew ₹50,000 out of affection, and a temple committee, relying on his promise to donate ₹1,00,000, contracted for repairs costing ₹1,20,000.'),
        'mcqs': [
            M('k1a', 'How much can Mr. Saxena recover from Pawan?', [R(k_pay), R(k_bal), R(500000), 'Nothing'], 0,
              f'Balance = 5,00,000 − 1,25,000 = {R(k_bal)}; written signed promise for 60% = {R(k_pay)} — Section 25(3) enforces the amount promised.', 'hard', '375000*60/100'),
            M('k1b', 'Mr. Saxena\'s promise to pay Leela ₹3,000 is:', ['Enforceable — compensation for past voluntary services, Section 25(2)', 'Void — no consideration', 'Void — the service was past', 'Enforceable only if registered'], 0, 'Leela voluntarily did something for him; his later promise to compensate is valid without consideration.', 'moderate'),
            M('k1c', 'The oral promise to the nephew is:', ['Not enforceable — not in writing and not registered', 'Enforceable — natural love and affection', 'Enforceable — nephew is a near relative', 'Voidable at the nephew\'s option'], 0, 'Section 25(1) requires writing and registration in addition to love, affection and near relation.', 'core'),
            M('k1d', 'The temple committee can claim from Mr. Saxena:', [R(100000), R(120000), R(20000), 'Nothing'], 0,
              'The committee incurred a liability on the faith of the promise, so the promise to the charity is enforceable (Kedarnath v. Gorie Mohammad) — but only for the ₹1,00,000 promised, not the full ₹1,20,000 spent.', 'hard', 'min(100000, 120000)'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch02', 'n': 2, 'title': 'Consideration',
        'outcomes': ['Explain consideration under Section 2(d) and its elements — act, abstinence or promise, at the promisor\'s desire, by the promisee or any other person.', 'Apply the legal rules on consideration: desire of the promisor, third-party consideration, past/executed/executory, adequacy, legal duty, reality and lawfulness.',
                     'Apply the doctrine of privity of contract and its exceptions to problems.', 'Identify agreements that are valid without consideration — Section 25(1), (2), (3), completed gifts, agency, bailment and charity.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 40}, 'prereq': ['fnd-p2-ch02-u01'],
                 'exam_tip': 'Expect a 4–6 mark problem on Section 25 exceptions (especially time-barred debt and love-and-affection) or on stranger to contract vs stranger to consideration. Quote the sub-section and list every condition.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {'summary': ['Consideration (Section 2(d)): act, abstinence or promise, at the desire of the promisor, by the promisee or any other person; past, present or future.',
                                 'Rules: desire of promisor (Durga Prasad v. Baldeo); may move from a third person (Chinnaya v. Ramayya); need not be adequate (Explanation 2, Section 25); not a pre-existing legal duty; real; lawful.',
                                 'Privity: a stranger to the contract cannot sue — exceptions: trust, family settlement, marriage arrangement, assignment, acknowledgement/estoppel, covenant running with land, agency.',
                                 'Section 25: no consideration, no contract — except love and affection (written + registered + near relation), past voluntary service, written signed promise for a time-barred debt; plus completed gift, agency (Section 185), bailment, charity relied upon.'],
                     'remember': ['Section 2(d) consideration · Section 25 void without consideration · 25(1) love & affection · 25(2) past voluntary service · 25(3) time-barred debt · Explanation 1 gift · Explanation 2 inadequacy · Section 185 agency.'],
                     'traps': ['Stranger to consideration CAN sue; stranger to contract generally cannot.', 'Love and affection needs writing AND registration AND near relation.', 'A time-barred debt revives only to the amount promised in writing.', 'Past consideration is valid in India if the act was at the promisor\'s desire.']},
        'quickref': [{'k': 'Section 2(d)', 'v': 'Act / abstinence / promise at desire of promisor, by promisee or any other person'}, {'k': 'Section 25', 'v': 'Agreement without consideration void — exceptions follow'},
                     {'k': 'Section 25(1)', 'v': 'Natural love & affection · near relation · written · registered'}, {'k': 'Section 25(2)', 'v': 'Compensation for past voluntary service'},
                     {'k': 'Section 25(3)', 'v': 'Written, signed promise to pay time-barred debt wholly or partly'}, {'k': 'Explanations to Section 25', 'v': '1: completed gift valid · 2: inadequacy not fatal, but evidence on free consent'},
                     {'k': 'Section 185', 'v': 'No consideration needed to create agency'}, {'k': 'Leading cases', 'v': 'Durga Prasad v. Baldeo · Chinnaya v. Ramayya · Kedarnath v. Gorie Mohammad · Misa v. Currie'}],
        'viva': viva, 'cases': cases,
    }


# ---------- teaching explanations + topic tags for every MCQ (override the short drafts above) ----------
TW, TL, TS, TV = 'What is Consideration?', 'Legal Rules Regarding Consideration', 'Suit by a Third Party to a Contract', 'Validity of an Agreement Without Consideration'
EXPLAIN = {
    'm1': (TW, 'Section 2(d) says consideration is an act, abstinence or promise done or made at the desire of the promisor. An act done at the request of someone else, or on one\'s own initiative, is not consideration for the promisor\'s promise (Durga Prasad v. Baldeo). The tempting trap is "the promisee" — consideration may move from the promisee or any other person, but the desire must be the promisor\'s. In practice: a contractor who does extra work a client never asked for cannot insist on payment for it.'),
    'm2': (TL, 'The false statement is that consideration must be adequate. Under Explanation 2 to Section 25, an agreement with free consent is not void merely because consideration is inadequate, although inadequacy may be evidence that consent was not free. The trap is "it may move from any other person", which sounds wrong but is true in India (Chinnaya v. Ramayya). In practice: a family member selling a flat below market value can still have a valid contract, though the tax law may apply its own valuation rules.'),
    'm3': (TL, 'In Chinnaya v. Ramayya, a mother gifted property to her daughter on the condition that the daughter pay an annuity to the mother\'s brother. The brother could enforce the daughter\'s promise even though the consideration came from the mother — consideration may move from a third person. The tempting trap is "a stranger to a contract can always sue"; privity still applies, the case only shows a stranger to the consideration can sue. In practice: family arrangements often have one relative providing the consideration and another receiving the benefit.'),
    'm4': (TL, 'Bhanu acted voluntarily, not at Chetan\'s desire, and Chetan promised nothing, so there is no consideration, no promise and no contract — Bhanu cannot claim a reward. The tempting trap is "Section 25(3)", which concerns time-barred debts; the relevant exception, Section 25(2), would apply only if Chetan later promised to compensate him. In practice: a neighbour who helps during an emergency has no legal claim unless the owner later promises payment.'),
    'm5': (TL, 'Consideration must be something the promisee is not already bound by law to do. A witness summoned to give evidence is legally bound to do so, so a promise to pay him for that rests on no consideration and is void. The trap is "valid if in writing" — writing does not create consideration. In practice: payments to witnesses beyond lawful allowances, such as travel expenses, can also look like an attempt to influence evidence, which raises legality concerns.'),
    'm6': (TV, 'Section 25(3) makes a promise to pay a time-barred debt enforceable without fresh consideration if it is in writing and signed by the debtor or his authorised agent, generally or with limited authority. The trap is "oral but made before witnesses" — witnesses cannot replace the written signed promise. In practice: before writing off an old receivable, a CA checks whether the debtor has signed any written promise to pay, because that revives the claim.'),
    'm7': (TV, 'Section 25(1) is an exception where an agreement is valid without consideration, so adequate consideration is the one element not required. It needs writing, registration, natural love and affection and a near relationship between the parties. The trap is to pick "writing and registration" thinking love and affection is enough — all conditions must exist together. In practice: family gift deeds between near relatives are executed in writing and registered so they are enforceable without any price.'),
    'm8': (TV, 'Section 25(1) needs all of: writing, registration, natural love and affection, and parties standing in near relation. Raju and Sohan are only friends, so the near-relationship condition fails and the promise is not enforceable despite the registered deed. The tempting trap is "enforceable because it is registered" — registration alone cannot cure the absence of consideration. In practice: a promise of money to a friend should be completed as an actual gift, since an unfulfilled promise is not legally binding.'),
    'm9': (TV, 'Section 185 provides that no consideration is necessary to create an agency — a person can act as agent without being paid. The tempting trap is Section 25(2), which covers compensation for past voluntary services, a different exception. Section 148 defines bailment and Section 2(d) defines consideration. In practice: a relative who signs documents or collects rent for you under a power of attorney is a valid agent even though he charges nothing.'),
    'm10': (TS, 'The doctrine of privity of contract means only parties to a contract can sue on it; a stranger cannot, even if the contract benefits him. It has exceptions such as trusts, family arrangements, acknowledgement or estoppel, and covenants running with land. The tempting trap is "stare decisis", which is about following precedent, not about who can sue. In practice: a customer of a distributor generally cannot sue the manufacturer on the distributor\'s contract, though consumer law may give separate rights.'),
    'm11': (TS, 'Recognised exceptions to privity include a beneficiary under a trust, an assignee of contractual rights such as an insurance policy, and a buyer of land bound by a covenant running with it. A creditor of the seller suing the buyer is a plain stranger, unless the buyer acknowledged the debt to him or became his agent. The trap is the assignee — assignment transfers rights, so the assignee can sue. In practice: banks enforce assigned insurance policies held as security for loans.'),
    'm12': (TV, 'Section 25(3) enforces a written, signed promise to pay a time-barred debt only to the extent promised. The debt was ₹3,50,000, but the written promise is for ₹3,00,000, so the creditor recovers ₹3,00,000. The tempting trap is ₹3,50,000 — the original debt is no longer enforceable; the new promise is the contract. In practice: when a debtor offers a part-payment settlement on old dues, the CA records the written promise as the recoverable amount and writes off the remaining ₹50,000.'),
    'm13': (TL, 'Consideration may be past, present or future. In a cash sale over the counter, the price and the goods are exchanged at the same time, so the consideration is present (executed). The tempting trap is "future consideration" — that applies when the act or payment is promised for a later date, as in credit sales. In practice: retail cash sales are recorded with immediate receipt of cash, while credit sales create a receivable that reflects future consideration.'),
    'k1/k1a': (TV, 'Balance unpaid = ₹5,00,000 − ₹1,25,000 = ₹3,75,000. Pawan\'s signed written promise covers 60%: 60% × ₹3,75,000 = ₹2,25,000. Under Section 25(3) the time-barred debt is revived only to that extent. The tempting trap is ₹3,75,000, the full balance — but the old debt is unenforceable and only the written promise binds. In practice: a CA reviewing an old loan treats the signed acknowledgement as the recoverable amount and provides for the rest.'),
    'k1/k1b': (TV, 'Section 25(2) upholds, without consideration, a promise to pay someone (fully or partly) for something he earlier did for the promisor of his own accord. Leela watered the garden for Mr. Saxena voluntarily, and he later promised ₹3,000, so the promise is enforceable. The trap is "void — the service was past"; this exception exists exactly for past voluntary services. In practice: a business owner who promises a bonus to a helper after the work is done can be held to that promise.'),
    'k1/k1c': (TV, 'Section 25(1) needs writing and registration as well as natural love and affection between near relatives. The promise to the nephew is oral, so it fails the writing and registration conditions and is not enforceable. The tempting trap is "enforceable — natural love and affection"; affection alone is not enough. In practice: families wanting a binding gift promise execute and register a written deed, or simply complete the gift by transfer.'),
    'k1/k1d': (TV, 'A promise to subscribe to a charity becomes enforceable once the promisee, relying on it, incurs a liability (Kedarnath v. Gorie Mohammad). The committee contracted for repairs on the faith of the promise, so it can claim the promised ₹1,00,000. The tempting trap is ₹1,20,000, the full repair cost — liability cannot exceed the sum actually promised. In practice: trusts and charities record pledged donations, and donors should know a pledge relied upon can be legally enforced.'),
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
           's1': _k('incorrect|not correct|wrong|false|not true|untrue|need not be adequate|not necessary|not required|not need|need not', n=1),
           's2': _k('explanation 2|section 25', 'inadequate|inadequacy|not void|free consent|freely consented|freely'),
           's3': _k('some value|value|real|not illusory|genuine|illusory', n=1),
           's4': _k('evidence|taken into account|take into account|into account|indicate|indication|suggest|presume', 'free consent|coercion|undue influence|fraud|consent'),
           },
    'q2': {'extra_ok': False,
           's1': _k('section 2 d|2(d)|any other person|third party|third person|another person|other person|anyone', 'consideration'),
           's2': _k('stranger to consideration|stranger to the consideration|not furnished consideration|not given consideration|not provide consideration', 'stranger to contract|stranger to the contract|not a stranger to the contract|not stranger to contract|not a stranger to contract|privity|party to the contract|party to contract|party to promise|party to the promise'),
           's3': _k('shop consideration|kamala consideration|gift consideration|consideration kamala|consideration shop|consideration gift|consideration moved|consideration came|consideration for dev', 'hari'),
           's4': _k('hari can sue|hari can recover|hari is entitled|hari entitled|hari succeed|hari can enforce|hari will succeed|dev liable|dev is liable|dev must pay|dev bound|plea fail|plea fails|plea will fail|dev cannot refuse|dev cannot escape|dev has to pay', n=1),
           's5': _k('chinnaya|ramayya'),
           },
    'q3': {'extra_ok': False,
           's1': _k('without consideration|void|section 25', 'written|writing|registered|registration', 'near relation|near relative|relative|relation|natural love|love and affection'),
           's2': _k('explanation 1|actually made|completed|complete|already given|already made|already handed|delivered', 'gift|given|handed'),
           's3': _k('oral|not written|not registered|unregistered|no writing|not in writing', 'not enforceable|unenforceable|void|cannot enforce|cannot be enforced|brother cannot|not binding|cannot claim'),
           's4': _k('cannot take|cannot recover|cannot get|cannot reclaim|cannot demand|cannot ask|not entitled|keep the chain|friend can keep|need not return|not return|not bound to return|no right|chain valid|valid gift|gift is complete|irrevocable', n=1,
                    wrong=[{'kw': ['can take back|can recover the chain|must return|get back the chain'], 'say': 'A gift actually made needs no consideration (Explanation 1 to Section 25) — Anu cannot take it back.'}]),
           },
    'q4': {'extra_ok': True,
           's1': _k('section 25|without consideration void|no consideration void|without consideration is void|without consideration are void', n=1),
           's2': _k('natural love|love and affection|near relation|relative', 'written|writing|registered'),
           's3': _k('voluntar', 'compensat|past|service|legally compellable'),
           's4': _k('time barred|time-barred|barred by limitation|limitation', 'signed debtor|signed by debtor|written signed|writing signed|signed writing|written and signed|signed in writing|signed by the debtor'),
           's5': _k('gift|completed', 'agency|agent|section 185', 'bailment|bailee|bailor', 'charity|charitable|donation|subscription', n=3),
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
