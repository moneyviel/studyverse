"""CA Foundation · Paper 2 Business Laws · Chapter 2 The Indian Contract Act, 1872 · Unit 1 Nature of Contracts.
Original explanations and problems; sections and leading cases are cited by name only."""
from lib import *
from ca_viva import P, ALT, V, PROP

UID = 'fnd-p2-ch02-u01'


def viva():
    """Own copy of this unit's viva (overrides tools/ca_src/ca_viva.py) — keywords re-tested under the negation matcher."""
    return [
        V('v1', 'Distinguish between an agreement and a contract.',
          'An agreement is a promise or set of promises forming consideration for each other under Section 2(e); in short, offer plus acceptance. A contract is an agreement enforceable by law under Section 2(h). So every contract is an agreement but every agreement is not a contract; social and domestic agreements like the one in Balfour versus Balfour are not enforceable.',
          [P('p1', 'Agreement = offer + acceptance / promises (Section 2(e))', 3, 'agreement', 'offer|acceptance|promise|2 e', min=2),
           P('p2', 'Contract = agreement enforceable by law (Section 2(h))', 4, 'contract', 'enforceable|enforced|enforce|binding|2 h', min=2),
           P('p3', 'Not every agreement is a contract — e.g. social/domestic agreements (Balfour v. Balfour)', 3,
             'not every agreement|not all agreement|every agreement not|all agreement not|agreement not always contract|agreement not necessarily contract|agreement need not contract|agreement may not contract|agreement not every contract|agreement is not always|agreement not always|social agreement not|domestic agreement not|social not enforc|domestic not enforc|not enforceable|not legally binding|not binding|balfour', min=1)], 'c1'),
        V('v2', 'State the essentials of a valid contract under Section 10 of the Indian Contract Act.',
          'Under Section 10 an agreement becomes a contract when the parties are competent, their consent is free, the consideration and the object are both lawful, and the Act does not expressly declare that kind of agreement void.',
          [P('p1', 'Competent parties', 2, 'competent|capacity|major|sound mind'),
           P('p2', 'Free consent', 2, 'free consent|consent'),
           P('p3', 'Lawful consideration', 2, 'consideration'),
           P('p4', 'Lawful object', 2, 'object|purpose'),
           P('p5', 'Not expressly declared void', 2, 'void|not prohibited|not declared')], 'c2'),
        V('v3', 'What is the difference between an offer and an invitation to offer?',
          'An offer shows willingness to be bound, so its acceptance creates a contract. An invitation to offer only invites others to make offers, for example a price list, a catalogue, goods displayed in a shop, an advertisement or a notice inviting tenders. In Pharmaceutical Society versus Boots, display of goods was held to be only an invitation to offer.',
          [P('p1', 'Offer: willingness to be bound; acceptance makes a contract', 4, 'offer', 'bound|accept|acceptance|contract|willingness', min=2),
           P('p2', 'Invitation to offer only invites others to make offers', 3, 'invitation|invite|inviting', 'make offer|to offer|offers|negotiat', min=2),
           P('p3', 'Example — price list, catalogue, display, advertisement, tender (Boots, Harvey v Facey)', 3, 'price list|catalogue|catalog|display|advertisement|tender|boots|harvey|auction|prospectus', min=1)], 'c5'),
        V('v4', 'Can silence amount to acceptance of an offer? Explain.',
          'No. Acceptance must be communicated, and mere silence is not acceptance. The offeror cannot say that silence will be treated as acceptance. In Felthouse versus Bindley the uncle\'s statement that he would treat silence as acceptance did not create a contract.',
          [P('p1', 'No — silence is not acceptance', 4, 'not acceptance|no|not amount|cannot|not an acceptance', 'silence', min=2),
           P('p2', 'Acceptance must be communicated', 3, 'communicat|express|convey|informed'),
           P('p3', 'Felthouse v Bindley', 3, 'felthouse|bindley')], 'c6'),
        V('v5', 'When is communication of an acceptance complete under Section 4?',
          'As against the proposer, the acceptance is complete when it is posted, that is, sent on its way so that the acceptor can no longer recall it. As against the acceptor, it is complete only when the proposer comes to know of it.',
          [P('p1', 'Against the proposer: once put in the course of transmission (posted), beyond the acceptor\'s recall', 5,
             ALT('{p} complet when put', '{p} complet when post', '{p} complet when sent', '{p} complet post', '{p} post', '{p} sent', '{p} when put', '{p} put course', '{p} course transmiss', '{p} transmiss', '{p} acceptance complet {w} {x}', '{p} complet {w} {x}', '{p} {w} {x}', w=('when', 'once', 'soon', 'as soon as'), x=('post', 'sent', 'put', 'dispatch'), p=PROP)),
           P('p2', 'Against the acceptor: only when it comes to the knowledge of the proposer', 5,
             ALT('{a} {p} know', '{a} {p} learn', '{a} {p} receiv', '{a} come knowledg {p}', '{a} complet when come knowledg', '{a} complet when {p} know', '{a} complet when {p} learn', '{a} knowledg {p}', '{a} complet {w} {p} {k}', '{a} {w} {p} {k}', '{a} {w} reach {p}', '{a} complet {w} reach {p}', '{a} {w} it reach {p}', a=('acceptor', 'offeree'), p=PROP, w=('when', 'only when', 'once'), k=('know', 'learn', 'receiv', 'get', 'read')))], 'c7'),
    ]


def build():
    timeline = table(['Date', 'Event', 'What the law says'], [
        ['1 June', 'Offer posted by A', '—'],
        ['3 June', 'Offer reaches B', 'Communication of the offer is complete (B now knows of it) — Section 4'],
        ['5 June', 'B posts his acceptance', 'Acceptance complete as against A: A is bound; A can no longer revoke the offer — Sections 4 and 5'],
        ['7 June', 'Acceptance reaches A', 'Acceptance complete as against B: until now B could revoke his acceptance — Sections 4 and 5'],
    ], title='Postal contract timeline')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch02', 'n': 1, 'title': 'Nature of Contracts',
        'outcomes': ['Tell an agreement from a contract and list every essential of a valid contract.', 'Classify contracts by validity (valid, void, voidable, illegal, unenforceable), by formation (express, implied, quasi) and by performance (executed, executory, unilateral, bilateral).',
                     'Explain a proposal (offer), its kinds and legal rules, and separate it from an invitation to offer.', 'Apply the rules on acceptance, communication and revocation (Sections 3 to 9) to problems, written as Provision → Facts → Analysis → Conclusion.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 45}, 'prereq': ['fnd-p2-ch01-u01'],
                 'exam_tip': 'Problem questions on offer, acceptance and revocation are asked almost every attempt. Quote the section, apply it to the facts, and end with a one-line conclusion.'},
        'concepts': [
            {'id': 'c1', 'title': 'Agreement vs contract', 'body': ['An agreement is a promise (or a set of promises that are consideration for each other) — Section 2(e). In simple terms: offer + acceptance = agreement.',
                                                                  'A contract is an agreement that the law will enforce — Section 2(h). So: agreement + enforceability = contract.',
                                                                  'Every contract is an agreement, but some agreements are not contracts: social or domestic arrangements made without any intention to create legal obligations (Balfour v. Balfour — a husband\'s promise of a monthly allowance to his wife was not enforceable).'],
             'analogy': 'An agreement is a handshake. A contract is a handshake the court will back up.', 'work': 'Clients often sign a "memorandum of understanding" and later ask whether it binds them. A CA first checks the intention — many MoUs say in writing that they are not legally binding.'},
            {'id': 'c2', 'title': 'Essentials of a valid contract', 'body': ['Section 10: an agreement becomes a contract when the parties are competent, their consent is free, both the consideration and the object are lawful, and the Act does not expressly declare that kind of agreement void. Where another law requires writing, witnesses or registration, that must also be complied with.',
                                                                           'Section 11: a person is competent if he has reached the age of majority under the law that applies to him, is of sound mind, and is not disqualified by any law.',
                                                                           'Other essentials recognised by courts: there must be two parties; the parties must intend legal consequences; the terms must be certain (not vague); and performance must be possible.'],
             'analogy': 'A checklist before take-off: free consent, competent parties, lawful consideration, lawful object, not declared void, formalities, intention, certainty, possibility. Miss one and the plane stays on the ground.', 'work': 'In due diligence, CAs and lawyers review key contracts against these essentials — for example, whether the person who signed for a company had authority, or whether a required document was stamped.'},
            {'id': 'c3', 'title': 'Types of contracts', 'body': ['By validity: valid (all essentials present); void agreement — not enforceable from the start (Section 2(g)); void contract — enforceable when made but later ceases to be (Section 2(j)), e.g. performance becomes impossible; voidable — enforceable at the option of one party only (Section 2(i)), e.g. consent obtained by coercion or fraud; illegal — forbidden by law, so void, and agreements connected with it are also tainted; unenforceable — valid in substance but cannot be enforced because of a technical defect such as want of a required stamp.',
                                                                 'By formation: express (terms in words, spoken or written); implied (inferred from conduct — Section 9); quasi-contract (not a real agreement; the law imposes an obligation to prevent unjust benefit).',
                                                                 'By performance: executed (both sides have performed); executory (something remains to be done); unilateral (only one side still has to perform); bilateral (both sides still have to perform).'],
             'analogy': 'Valid = green light; voidable = amber (one driver may choose to stop); void = red; unenforceable = a car that is fine but has no papers.', 'work': 'Auditors ask whether a disputed contract is void or voidable, because it decides whether a receivable or a liability should be recognised at all.'},
            {'id': 'c4', 'title': 'Proposal (offer) and its kinds', 'body': ['Section 2(a): a person makes a proposal when he signifies to another his willingness to do or not to do something, intending to obtain that person\'s assent. The person making it is the offeror (promisor); the person to whom it is made is the offeree.',
                                                                           'General offer — made to the public; anyone who performs the conditions accepts it (Carlill v. Carbolic Smoke Ball Co.). Specific offer — made to a particular person; only that person can accept.',
                                                                           'Cross offers — two identical offers that cross each other without either party knowing of the other: no contract until one of them accepts. Counter offer — a reply that changes the terms; it rejects the original offer (Hyde v. Wrench). Standing (continuing) offer — open for a period, e.g. to supply goods as and when ordered; each order is an acceptance that creates a separate contract.'],
             'analogy': 'A general offer is a notice on the gate; a specific offer is a letter with your name on it.', 'work': 'Online platforms and reward schemes are designed as general offers — their terms are drafted carefully because any member of the public who performs the conditions can claim.'},
            {'id': 'c5', 'title': 'Rules of a valid offer — and what is not an offer', 'body': ['An offer must be capable of creating legal relations; be certain and definite; be communicated to the offeree (a person who acts without knowing of the offer cannot claim — Lalman Shukla v. Gauri Datt); be made to obtain assent; may be conditional; and must not state that silence will be taken as acceptance.',
                                                                                             'Not offers: a statement of intention; a reply giving information or a price (Harvey v. Facey — stating the lowest price was not an offer to sell); and an invitation to offer — price lists, catalogues, goods displayed with price tags (Pharmaceutical Society v. Boots), advertisements, auction notices, a company\'s prospectus and a notice inviting tenders. In these cases the customer, bidder or applicant makes the offer.'],
             'analogy': 'A restaurant menu is an invitation; your order is the offer; the waiter writing it down is the acceptance.', 'work': 'When a client\'s website shows a wrong price, the "invitation to offer" principle is the starting point of the legal analysis (consumer protection laws may add further duties).'},
            {'id': 'c6', 'title': 'Acceptance', 'body': ['Section 2(b): when the offeree signifies assent, the proposal is accepted; an accepted proposal becomes a promise.',
                                                         'Rules: acceptance must be absolute and unqualified (Section 7); expressed in the usual and reasonable manner unless the offer prescribes a manner — if the prescribed manner is not followed, the offeror may insist on it within a reasonable time, failing which he is bound; it must be communicated — mere silence is not acceptance (Felthouse v. Bindley); it must come from the offeree or someone authorised by him (Powell v. Lee); it must be given while the offer is still open; and the acceptor must know of the offer.',
                                                         'Section 8: performing the conditions of an offer, or accepting the consideration offered, is acceptance.'],
             'analogy': 'Acceptance is a mirror: it must reflect the offer exactly. A mirror that changes the picture is a new picture — a counter offer.', 'work': 'Purchase orders and order acknowledgements often contain different printed terms. Whose terms apply depends on who made the last offer and who accepted it — a real question in contract and revenue reviews.'},
            {'id': 'c7', 'title': 'Communication and revocation (Sections 3 to 6)', 'body': ['Section 4: an offer is communicated only when the offeree comes to know of it. An acceptance binds the offeror once the acceptor has sent it on its way so that he can no longer recall it (put in the course of transmission); it binds the acceptor only when the offeror comes to know of it.',
                                                                                          'Section 5: an offer may be revoked at any time before communication of acceptance is complete as against the offeror, but not afterwards. An acceptance may be revoked at any time before communication of acceptance is complete as against the acceptor, but not afterwards.',
                                                                                          'Section 6: an offer is revoked by notice of revocation; by lapse of the prescribed time or, if none, a reasonable time; by failure of the acceptor to fulfil a condition precedent; or by the death or insanity of the offeror if the acceptor learns of it before accepting. An offer also ends by a counter offer, by rejection, by non-acceptance in the prescribed manner and by subsequent illegality.',
                                                                                          'Instantaneous communication (telephone): the contract is made where and when the acceptance is heard by the offeror (Bhagwandas Goverdhandas Kedia v. Girdharilal Parshottamdas & Co.).'],
             'blocks': [timeline],
             'analogy': 'Once the acceptance letter drops into the post box, the offeror\'s door is shut; the acceptor\'s door stays open until the letter is read.', 'work': 'In disputes over which date a contract was formed (for tax, revenue or limitation purposes), these timing rules decide the answer.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'A reward notice: knowledge of the offer', 'difficulty': 'core', 'minutes': 7,
             'q': 'Mr. Desai publishes a notice: "₹10,000 to anyone who returns my lost dog, Bruno." Ritu, unaware of the notice, finds Bruno and returns him. Later she sees the notice and claims the reward. Kunal, in a similar case the next month, had read the notice before returning a lost cat for the same kind of reward. Can Ritu and Kunal claim?',
             'solution': [legal('A general offer is made to the public at large and can be accepted by anyone who performs its conditions (Section 8; Carlill v. Carbolic Smoke Ball Co.). But an offer can be accepted only by a person who knows of it (Lalman Shukla v. Gauri Datt).',
                                'Ritu returned the dog without knowing of the reward notice. Kunal knew of the notice and then performed the condition.',
                                'Ritu\'s act was not done in response to the offer, so there was no acceptance. Kunal performed the condition with knowledge of the offer; performance itself is acceptance and no separate communication was needed.',
                                'Ritu cannot claim the reward. Kunal can claim it.')]},
            {'id': 'i2', 'title': 'Revoking an offer after the acceptance is posted', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'On 1 May Anand offers by letter to sell his car to Bhavna for ₹4,50,000. The letter reaches her on 3 May. Bhavna posts her acceptance on 10 May. On 11 May Anand emails Bhavna withdrawing the offer; she reads the email the same day. Her letter reaches Anand on 12 May. Is there a contract?',
             'solution': [legal('Section 4: an acceptance binds the offeror once it is sent on its way (put in the course of transmission) beyond the acceptor\'s recall. Section 5: an offer can be withdrawn only until the acceptance has become binding on the offeror.',
                                'Bhavna posted her acceptance on 10 May. Anand\'s revocation was sent and read on 11 May, before her letter reached him.',
                                'As against Anand, the acceptance was complete on 10 May when it was posted. His revocation on 11 May came after that moment, so it is too late, even though he had not yet received the acceptance.',
                                'The revocation is not valid. A binding contract exists for the sale of the car at ₹4,50,000.'),
                         table(['Date', 'Event', 'What the law says'], [
                             ['1 May', 'Offer posted by Anand', '—'],
                             ['3 May', 'Offer reaches Bhavna', 'Communication of the offer is complete — Section 4'],
                             ['10 May', 'Bhavna posts her acceptance', 'Acceptance complete as against Anand; from now he cannot revoke the offer — Sections 4 and 5'],
                             ['11 May', 'Anand emails a revocation', 'Too late — the offer could be revoked only before 10 May'],
                             ['12 May', 'Acceptance reaches Anand', 'Acceptance complete as against Bhavna'],
                         ], title='Date line')]},
            {'id': 'i3', 'title': 'Counter offer kills the original offer', 'difficulty': 'core', 'minutes': 6,
             'q': 'Sona Rice Mills offers 200 bags of rice to Kapoor Stores at ₹2,500 a bag. Kapoor replies, "We will take them at ₹2,350." The mill refuses. Kapoor then writes, "All right, we accept your price of ₹2,500." The mill has meanwhile sold the rice elsewhere. Can Kapoor enforce a contract?',
             'solution': [legal('Section 7: acceptance must be absolute and unqualified. A reply that changes the terms is a counter offer and amounts to a rejection of the original offer (Hyde v. Wrench).',
                                'Kapoor first replied with a lower price, which the mill refused. Only later did Kapoor try to accept ₹2,500.',
                                'Kapoor\'s reply at ₹2,350 was a counter offer that ended the mill\'s original offer. The later letter accepting ₹2,500 was therefore a fresh offer by Kapoor, which the mill never accepted.',
                                'There is no contract; Kapoor cannot enforce it.')]},
            {'id': 'i4', 'title': 'A wrong price tag in a shop', 'difficulty': 'core', 'minutes': 5,
             'q': 'A watch in a showroom window carries a tag of ₹999 instead of ₹9,999. Neel walks in and insists on buying it at ₹999. The shopkeeper refuses. Has the shopkeeper broken a contract?',
             'solution': [legal('Display of goods with a price tag is an invitation to offer, not an offer (Pharmaceutical Society of Great Britain v. Boots Cash Chemists). A contract arises only when an offer is accepted (Section 2(b)).',
                                'The watch was displayed with a wrong price. Neel offered to buy at ₹999 and the shopkeeper refused.',
                                'Neel\'s request at the counter was the offer. The shopkeeper was free to accept or reject it, and he rejected it.',
                                'No contract was formed, so the shopkeeper has not broken any contract. (Any consumer-protection angle is a separate question, outside this unit.)')]},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Purchase order with changed terms', 'role': 'CA in industry (finance controller of a manufacturer)', 'situation': 'Your sales team quoted a customer 30-day credit. The customer\'s purchase order says 60 days and the team has already started production.',
             'steps': ['Identify the offer and the reply: if the quotation was an offer, the purchase order with 60 days is a counter offer that rejects it; if the quotation was only an invitation to offer, the purchase order is itself the offer. Either way, the 60-day term is now on the table.', 'Check whether your company accepted the 60 days — by an acknowledgement, or by conduct such as starting supply.',
                       'Advise the team to send a written acknowledgement stating the agreed terms before dispatch.', 'Record the agreed credit terms in the customer master so invoicing and collections follow the contract.'],
             'takeaway': 'Offer, counter offer and acceptance decide which terms bind the company — and the cash-flow impact can be large.', 'think': 'If your company dispatches the goods without saying anything about the 60 days, which terms are likely to apply?',
             'answer': 'Dispatching in response to the purchase order is acceptance by conduct of the customer\'s terms (its counter offer, or its offer if the quotation was only an invitation), so the 60-day term is likely to apply.'},
            {'id': 'j2', 'title': 'Withdrawing a tender bid', 'role': 'CA advising an SME contractor', 'situation': 'Your client submitted a bid in response to a municipal tender notice, then found a costing error and wants to withdraw before the bids are opened.',
             'steps': ['The tender notice is an invitation to offer; your client\'s bid is the offer.', 'Under Section 5 an offer can be revoked before acceptance is communicated, so withdrawal is possible in principle.', 'Read the tender conditions: they may provide consequences such as forfeiture of earnest money for withdrawal during the validity period.', 'Send the withdrawal in writing by the fastest permitted mode and keep proof of delivery.'],
             'takeaway': 'The Contract Act gives the basic right; the tender document may add conditions the client has agreed to.', 'think': 'Why must the withdrawal reach the authority before it communicates acceptance?',
             'answer': 'Once acceptance is communicated (as against the offeror), Section 5 no longer allows the offer to be revoked and a contract exists.'},
            {'id': 'j3', 'title': 'Annual rate contract with a supplier', 'role': 'Articled assistant reviewing procurement', 'situation': 'A company has a rate contract with a stationery supplier: "We will supply any quantity you order during 2026-27 at these rates."',
             'steps': ['Recognise the supplier\'s promise as a standing offer.', 'Each purchase order is an acceptance that creates a separate contract for that order.', 'The supplier may withdraw the standing offer for future orders, but must honour orders already placed.'],
             'takeaway': 'A "rate contract" is often not one contract but a standing offer plus many small contracts.', 'think': 'The supplier writes in October that it will not supply any more at the old rates. What about an order placed in September but not yet delivered?',
             'answer': 'That order was accepted in September, so a binding contract exists and must be performed; the withdrawal affects only future orders.'},
        ],
        'mcqs': [
            {'id': 'm1', 'q': 'An agreement enforceable by law is a:', 'options': ['Contract', 'Promise', 'Proposal', 'Void agreement'], 'answer': 0, 'explain': 'Section 2(h) defines a contract as an agreement enforceable by law.', 'concept': 'c1', 'difficulty': 'core'},
            {'id': 'm2', 'q': 'A contract that is enforceable at the option of one party but not the other is:', 'options': ['Voidable', 'Void', 'Illegal', 'Unenforceable'], 'answer': 0, 'explain': 'Section 2(i) — e.g. where consent was obtained by coercion, the aggrieved party may choose to enforce or avoid it.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm3', 'q': 'Display of goods with price tags in a shop window is:', 'options': ['An invitation to offer', 'A general offer', 'A specific offer', 'A standing offer'], 'answer': 0, 'explain': 'The customer makes the offer at the counter; the shopkeeper may accept or reject it.', 'concept': 'c5', 'difficulty': 'core'},
            {'id': 'm4', 'q': 'A reply to an offer that introduces new terms is:', 'options': ['A counter offer and a rejection of the original offer', 'A valid acceptance', 'A cross offer', 'An invitation to offer'], 'answer': 0, 'explain': 'Acceptance must be absolute (Section 7). A changed reply is a counter offer (Hyde v. Wrench).', 'concept': 'c6', 'difficulty': 'core'},
            {'id': 'm5', 'q': 'Communication of acceptance by post is complete as against the offeror when:', 'options': ['The letter is posted', 'The letter reaches the offeror', 'The offeror reads the letter and replies', 'The acceptor writes the letter'], 'answer': 0, 'explain': 'Section 4: as against the offeror, when the acceptance is put in the course of transmission and is out of the acceptor\'s power.', 'concept': 'c7', 'difficulty': 'core'},
            {'id': 'm6', 'q': 'An acceptance sent by post can be revoked:', 'options': ['Before the letter of acceptance reaches the offeror', 'Only before it is posted', 'At any time before performance', 'Never'], 'answer': 0, 'explain': 'Section 5: before communication of acceptance is complete as against the acceptor — i.e. before it comes to the offeror\'s knowledge.', 'concept': 'c7', 'difficulty': 'moderate'},
            {'id': 'm7', 'q': 'Two identical offers made by two parties to each other, each without knowing of the other\'s offer, are:', 'options': ['Cross offers — no contract until one accepts', 'A concluded contract', 'Counter offers', 'Standing offers'], 'answer': 0, 'explain': 'Cross offers do not amount to acceptance of each other.', 'concept': 'c4', 'difficulty': 'core'},
            {'id': 'm8', 'q': '"If I do not hear from you by Monday, I shall take it that you have accepted." The offeree says nothing. Result:', 'options': ['No contract — silence is not acceptance', 'Contract on Monday', 'Contract only if the offeree is a merchant', 'Voidable contract'], 'answer': 0, 'explain': 'An offeror cannot impose silence as acceptance (Felthouse v. Bindley).', 'concept': 'c6', 'difficulty': 'core'},
            {'id': 'm9', 'q': 'Which is NOT a mode of revocation of an offer under Section 6?', 'options': ['The offeror merely changing his mind without telling anyone', 'Lapse of the time prescribed', 'Failure of the acceptor to fulfil a condition precedent', 'Death of the offeror known to the acceptor before acceptance'], 'answer': 0, 'explain': 'Revocation by notice requires communication; an uncommunicated change of mind does not revoke an offer.', 'concept': 'c7', 'difficulty': 'moderate'},
            {'id': 'm10', 'q': 'Social and domestic agreements are usually not contracts because:', 'options': ['There is no intention to create legal relations', 'There is no offer', 'They are always oral', 'The parties are never competent'], 'answer': 0, 'explain': 'Balfour v. Balfour — such arrangements are presumed not intended to be legally binding.', 'concept': 'c1', 'difficulty': 'core'},
        ],
        'questions': [
            {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'legal',
             'q': 'Mr. Arora offers by letter to sell his flat to Ms. Bedi. The letter reaches her on 3 March. She posts her letter of acceptance on 5 March. On 6 March she changes her mind and sends an email revoking her acceptance, which Mr. Arora reads the same day. Her letter of acceptance reaches him on 8 March. Mr. Arora claims that a contract exists. Advise Ms. Bedi with reference to the Indian Contract Act, 1872.',
             'model': [legal('Section 4: the acceptor is bound by his acceptance only when it reaches the offeror\'s knowledge. Section 5: an acceptance may be revoked at any time before communication of the acceptance is complete as against the acceptor, but not afterwards. Under Section 4, a revocation takes effect against the other party once he comes to know of it.',
                             'Ms. Bedi posted her acceptance on 5 March. Her revocation by email came to Mr. Arora\'s knowledge on 6 March. Her letter of acceptance reached him only on 8 March.',
                             'As against Ms. Bedi, her acceptance would have been complete only on 8 March, when it came to Mr. Arora\'s knowledge. Her revocation reached him on 6 March, before that date, so it was made in time.',
                             'The revocation of acceptance is valid and no contract exists. Mr. Arora\'s claim will fail.')],
             'scheme': [{'id': 's1', 'pt': 'Section 4 timing of acceptance as against the acceptor', 'm': 1, 'skill': 'provision'},
                        {'id': 's2', 'pt': 'Section 5 — acceptance revocable before that moment', 'm': 1, 'skill': 'provision'},
                        {'id': 's3', 'pt': 'Applies dates: revocation on 6 March reached before acceptance on 8 March', 'm': 1, 'skill': 'analysis'},
                        {'id': 's4', 'pt': 'Clear conclusion: revocation valid, no contract', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Many candidates apply the rule for revoking an offer (complete on posting) instead of the rule for revoking an acceptance.', 'Answers that quote the section number and then apply each date score full marks; answers that only state a conclusion score very little.'],
             'mistakes': ['Saying the contract was complete when Ms. Bedi posted her letter "for both parties".', 'Confusing the offeror\'s and the acceptor\'s positions under Section 4.', 'No conclusion line.'],
             'tips': ['Use four headings: Provision, Facts, Analysis, Conclusion.', 'Draw a small date line in rough work before writing.', 'Answer in the voice the question asks for: "Ms. Bedi is advised that …".']},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': '"Every contract is an agreement, but not every agreement is a contract." Explain.',
             'model': [p('Section 2(e) treats a promise — or a set of promises that are consideration for one another — as an agreement. Under Section 2(h), only an agreement that the law will enforce is a contract.'),
                       p('A contract therefore needs an agreement plus enforceability. Enforceability comes from the essentials in Section 10 — free consent, competent parties, lawful consideration and object, not expressly declared void — and an intention to create legal relations.'),
                       ul(['Agreements without legal intention, such as social or domestic arrangements (Balfour v. Balfour), are not contracts.', 'Agreements expressly declared void, or made by incompetent parties, are not contracts.']),
                       p('Hence every contract is an agreement, but only those agreements that satisfy the legal requirements become contracts.')],
             'scheme': [{'id': 's1', 'pt': 'Definition of agreement — Section 2(e)', 'm': 1, 'skill': 'provision'}, {'id': 's2', 'pt': 'Definition of contract — Section 2(h)', 'm': 1, 'skill': 'provision'},
                        {'id': 's3', 'pt': 'Enforceability: Section 10 essentials / legal intention', 'm': 1, 'skill': 'analysis'}, {'id': 's4', 'pt': 'Example of an agreement that is not a contract, and conclusion', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Strong answers use both definitions and a clear example.'], 'mistakes': ['Explaining only offer and acceptance without enforceability.'], 'tips': ['Formula: agreement = offer + acceptance; contract = agreement + enforceability.']},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'legal',
             'q': 'Rakesh writes to Sanjay: "I offer you my used printer for ₹8,000. If I hear nothing from you by Friday, I shall treat the printer as sold to you." Sanjay does not reply. On Saturday Rakesh demands ₹8,000. Is Sanjay bound to pay?',
             'model': [legal('Section 2(b) and Section 7: acceptance must be signified and communicated in the usual and reasonable manner. The offeror cannot make the offeree\'s silence amount to acceptance (Felthouse v. Bindley).',
                             'Rakesh offered the printer and declared that silence until Friday would be treated as acceptance. Sanjay did not reply at all.',
                             'Sanjay never signified assent. Rakesh cannot impose a duty on Sanjay to reply, and silence does not communicate acceptance.',
                             'There is no contract. Sanjay is not bound to pay ₹8,000.')],
             'scheme': [{'id': 's1', 'pt': 'Acceptance must be communicated — Sections 2(b)/7', 'm': 1.5, 'skill': 'provision'}, {'id': 's2', 'pt': 'Silence is not acceptance (case law)', 'm': 0.5, 'skill': 'provision'},
                        {'id': 's3', 'pt': 'Application to Sanjay\'s silence', 'm': 1, 'skill': 'analysis'}, {'id': 's4', 'pt': 'Conclusion: no contract, not bound to pay', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Most candidates reach the right conclusion; marks are lost for not citing the provision.'], 'mistakes': ['Treating Sanjay\'s silence as acceptance by conduct.'], 'tips': ['A case name is a bonus, the section is a must.']},
            {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
             'q': 'Distinguish between an offer and an invitation to offer, with examples.',
             'model': [table(['Basis', 'Offer', 'Invitation to offer'], [
                 ['Meaning', 'Final expression of willingness to be bound on stated terms (Section 2(a))', 'A step before an offer — inviting others to make offers'],
                 ['Result of a "yes"', 'Acceptance creates a binding agreement', 'A "yes" is only an offer, which may be accepted or rejected'],
                 ['Intention', 'To obtain assent and be bound', 'To start negotiations or attract offers'],
                 ['Examples', 'A reward notice; a letter offering a car at a stated price', 'Price lists, catalogues, goods displayed with price tags, tender notices, a company\'s prospectus'],
             ])],
             'scheme': [{'id': 's1', 'pt': 'Meaning of each', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Effect of response', 'm': 1, 'skill': 'analysis'}, {'id': 's3', 'pt': 'Intention', 'm': 1, 'skill': 'concept'}, {'id': 's4', 'pt': 'Examples on both sides', 'm': 1, 'skill': 'application'}],
             'remarks': ['A table with 3–4 bases and correct examples earns full marks quickly.'], 'mistakes': ['Calling an advertisement for sale an offer (unless it is a reward-type general offer).'], 'tips': ['Keep each cell to one line.']},
        ],
        'revision': {'summary': ['Agreement = offer + acceptance; contract = agreement enforceable by law (Sections 2(e), 2(h)).', 'Section 10 essentials: free consent, competent parties, lawful consideration and object, not declared void, plus legal formalities.',
                                 'Offer: general, specific, cross, counter, standing. Invitations to offer are not offers.', 'Acceptance: absolute, communicated, in the prescribed or usual manner, by the offeree, while the offer is open; silence is not acceptance.',
                                 'Postal rule: acceptance binds the offeror on posting; binds the acceptor on reaching the offeror. Revocation must be in time (Section 5).'],
                     'remember': ['Section 2(a) proposal · 2(b) acceptance · 2(e) agreement · 2(h) contract · 2(g) void agreement · 2(i) voidable contract · 2(j) void contract.', 'Section 4 completion of communication; Section 5 revocation; Section 6 modes of revocation; Section 7 rules of acceptance; Section 8 acceptance by performance.'],
                     'traps': ["Don't call a price list or a tender notice an offer.", "Don't apply the offer-revocation rule to the revocation of an acceptance.", "Don't treat a counter offer as acceptance."]},
        'quickref': [{'k': 'Section 2(h)', 'v': 'Contract = agreement enforceable by law'}, {'k': 'Section 10', 'v': 'Free consent, competent parties, lawful consideration & object, not expressly void'},
                     {'k': 'Section 4 — acceptance', 'v': 'Complete v. offeror on posting; v. acceptor when it reaches the offeror'}, {'k': 'Section 5', 'v': 'Offer revocable till acceptance is posted; acceptance revocable till it reaches the offeror'},
                     {'k': 'Section 6', 'v': 'Notice · lapse of time · failure of condition precedent · death/insanity of offeror known to acceptor'}, {'k': 'Section 7', 'v': 'Acceptance absolute and unqualified; prescribed or usual manner'},
                     {'k': 'Section 8', 'v': 'Performing conditions or accepting consideration = acceptance'}, {'k': 'Answer format', 'v': 'Provision → Facts → Analysis → Conclusion'}],
        'viva': viva(),
    }


# ---------- teaching explanations + topic tags for every MCQ (override the short drafts above) ----------
TC, TE, TT, TP = 'What is a Contract?', 'Essentials of a Valid Contract', 'Types of Contracts', 'Proposal / Offer [Section 2(a) of the Indian Contract Act, 1872]'
TA, TCM, TR = 'Acceptance', 'Communication of Offer and Acceptance', 'Revocation of Offer and Acceptance'
EXPLAIN = {
    'm1': (TC, 'Section 2(h) defines a contract as an agreement enforceable by law: agreement (offer plus acceptance) plus enforceability. The tempting trap is "promise" — under Section 2(b) an accepted proposal becomes a promise, and a promise or set of promises forms an agreement, but it becomes a contract only if the law will enforce it. In practice: a CA checks that a client\'s purchase order and acceptance meet legal requirements before treating the deal as a binding contract for revenue recognition.'),
    'm2': (TT, 'Section 2(i): a voidable contract is enforceable at the option of one party (the aggrieved one, for example whose consent was caused by coercion, undue influence, fraud or misrepresentation) but not at the option of the other. The tempting trap is "unenforceable" — that means neither party can enforce it, often for a technical defect such as lack of stamping. A void contract binds no one. In practice: a business pressured into signing a supply deal can choose to cancel or continue it.'),
    'm3': (TP, 'Goods displayed with price tags are only an invitation to offer: the shop invites customers to make offers. The customer offers at the billing counter and the shopkeeper is free to accept or refuse. The trap is "a general offer", which assumes anyone picking up the item creates a contract the shop must honour. In practice: if a supermarket shelf shows a wrong low price, the store can decline to sell at that price, though consumer-protection rules on unfair practices still apply.'),
    'm4': (TA, 'Section 7 requires acceptance to be absolute and unqualified. A reply that adds or changes terms is a counter offer, which rejects the original offer, so the original cannot later be accepted (Hyde v. Wrench). The tempting trap is "a valid acceptance", treating a small change as acceptance — it is not. A cross offer is two identical offers made unknowingly. In practice: when a buyer returns a quotation with a changed payment term, the seller must accept that new term before any contract exists.'),
    'm5': (TCM, 'Section 4: the offeror becomes bound the moment the acceptor sends the acceptance off beyond recall — for a letter, the moment it is posted. The tempting trap is "when the letter reaches the offeror"; that is the moment it becomes complete as against the acceptor. In practice: when a tender acceptance is dispatched by post or courier, the date of dispatch can decide when the offeror became bound.'),
    'm6': (TR, 'Section 5: an acceptance can be revoked any time before communication of acceptance is complete as against the acceptor — before the letter comes to the offeror\'s knowledge — and not afterwards. The tempting trap is "only before it is posted"; posting binds the offeror, but the acceptor can still revoke by a faster mode, such as a phone call or email that arrives first. In practice: a supplier who posts an acceptance and then discovers a costing error can send an email revocation that reaches the buyer before the letter.'),
    'm7': (TP, 'Cross offers are identical offers that cross each other, each party unaware of the other\'s offer. Neither is an acceptance of the other, because acceptance must be made in response to a known offer — so no contract arises until one party accepts. The tempting trap is "a concluded contract", since the terms match. In practice: when two businesses email identical purchase and sale terms at the same moment, one still needs to confirm acceptance before either can enforce the deal.'),
    'm8': (TA, 'Acceptance must be communicated; an offeror cannot impose on the offeree a duty to reply by declaring that silence will count as acceptance (Felthouse v. Bindley). The offeree\'s silence is therefore not acceptance and there is no contract. The trap is "contract on Monday", which treats the deadline as binding. In practice: a supplier who emails "unless you object by Friday, we will ship and invoice" cannot force payment if the customer simply ignores the email.'),
    'm9': (TR, 'Section 6 revokes an offer by notice communicated to the other party, lapse of the prescribed or a reasonable time, failure of the acceptor to fulfil a condition precedent, or death or insanity of the offeror known to the acceptor before acceptance. A mere change of mind kept to oneself revokes nothing. The trap is the death option — it is a valid mode, but only if the acceptor knows of it before accepting. In practice: a client withdrawing a quotation must actually inform the customer, preferably in writing.'),
    'm10': (TE, 'An essential of a valid contract is an intention to create legal relations. In social and domestic arrangements the law presumes no such intention, so they are not contracts (Balfour v. Balfour). The tempting trap is "they are always oral" — oral contracts are perfectly valid unless a statute requires writing. In practice: a CA advising a family-owned business insists that loans between relatives be recorded in written agreements, so that the intention to be legally bound is clear.'),
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
