"""CA Foundation · Paper 2 Business Laws · Chapter 3 The Sale of Goods Act, 1930 · Unit 3 Transfer of Ownership and Delivery of Goods.
Original explanations, facts and questions; sections are cited, never quoted at length."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p2-ch03-u03'


def build():
    c = Checks()
    # i1 — specific goods, deliverable state, destroyed after contract
    sofa = c.add('185000', 'price of the sofa set')
    # i4 — wrong quantity (Section 37)
    ordered, delivered_more, delivered_less, rate = 500, 560, 450, 640
    pay_contract = c.add('500*640', 'pay for the 500 cartons contracted')
    pay_whole = c.add('560*640', 'pay for all 560 if the whole is accepted')
    pay_short = c.add('450*640', 'pay for 450 if the short delivery is accepted')
    # i6 — buyer neglects delivery (Section 44)
    days_late, per_day = 18, 1500
    storage = c.add('18*1500', 'reasonable charge for care and custody: 18 days × 1,500')
    fall = c.add('120*(2400-2280)', 'loss from price fall caused by the delay: 120 bags × 120')
    s44_total = c.add('18*1500+120*(2400-2280)', 'total recoverable from the buyer under Section 44')
    # case — sale or return
    k_sarees = c.add('12*7500', 'price of 12 sarees')
    k_kept = c.add('5*7500', 'price of the 5 sarees retained beyond the time fixed')

    prop_table = table(['Situation', 'Section', 'Property passes when'], [
        ['Unascertained goods', '18', 'Never before the goods are ascertained'],
        ['Specific/ascertained goods — general rule', '19', 'When the parties intend (terms, conduct, circumstances)'],
        ['Specific goods in a deliverable state, unconditional contract', '20', 'When the contract is made — even if payment or delivery is postponed'],
        ['Specific goods — seller must do something to make them deliverable', '21', 'When that thing is done and the buyer has notice of it'],
        ['Specific goods — seller must weigh, measure or test to fix the price', '22', 'When that act is done and the buyer has notice of it'],
        ['Unascertained / future goods by description', '23(1)', 'When goods of the right description in a deliverable state are unconditionally appropriated with the other party\'s assent'],
        ['Delivery to buyer or carrier without reserving right of disposal', '23(2)', 'On such delivery — treated as unconditional appropriation'],
        ['Goods on approval / sale or return', '24', 'On approval or act adopting the sale; or on expiry of the fixed (or a reasonable) time without notice of rejection'],
        ['Right of disposal reserved', '25', 'Only when the seller\'s conditions (usually payment) are fulfilled'],
    ], title='When does property pass? (Sections 18 to 25)')

    nemo = table(['Exception to nemo dat', 'Section', 'Requirement for the buyer to get good title'], [
        ['Sale by mercantile agent', '27 proviso', 'Agent in possession of goods/documents with owner\'s consent, selling in ordinary course of business; buyer in good faith without notice of lack of authority'],
        ['Estoppel', '27', 'True owner by conduct led the buyer to believe the seller had authority'],
        ['Sale by one joint owner', '28', 'Others allowed him sole possession; buyer in good faith, no notice'],
        ['Seller in possession under a voidable contract', '29', 'Sale made before the contract is rescinded; buyer in good faith, no notice'],
        ['Seller left in possession after sale', '30(1)', 'Sale/pledge to a person taking in good faith, without notice of the earlier sale'],
        ['Buyer in possession before property passes', '30(2)', 'Buyer has possession with seller\'s consent and resells to a good-faith buyer without notice of seller\'s rights'],
        ['Unpaid seller reselling', '54(3)', 'After exercising lien or stoppage in transit'],
        ['Other laws', 'Contract Act s. 169, 176; official receiver/liquidator', 'Finder of goods, pawnee, court officers selling'],
    ], title='Who can give a better title than he has?')

    concepts = [
        {'id': 'c1', 'title': 'Passing of property in specific and ascertained goods (Sections 18 to 22)', 'body': [
            'Why it matters: whoever has the property (ownership) normally carries the risk, can sue for the goods, and is affected by the other party\'s insolvency.',
            'Section 18: in a contract for unascertained goods, no property passes until the goods are ascertained — you cannot own "500 kg out of a heap".',
            'Section 19: for specific or ascertained goods, property passes when the parties intend it to pass. To find that intention, look at what the contract says, how the parties behaved and the surrounding facts. Sections 20 to 24 are rules to find that intention when the parties have not stated it.',
            'Section 20: unconditional contract + specific goods + deliverable state → property passes the moment the contract is made, even if payment, delivery or both are postponed.',
            'Section 21: if the seller must do something to put specific goods into a deliverable state (repair, assemble, pack), property passes only when it is done and the buyer is informed.',
            'Section 22: if the goods are deliverable but the seller must weigh, measure or test them to work out the price, property passes only after that is done and the buyer is informed.'],
         'blocks': [prop_table],
         'analogy': 'Section 20 is buying a ready cake at the counter — it is yours though you collect it tomorrow. Section 21 is a cake still to be iced — not yours until iced and you are told. Section 22 is a cake priced by weight — not yours until weighed and you are told the price.',
         'work': 'Cut-off testing at the year end is an application of Sections 20 to 22: goods sold but awaiting fitting, weighing or testing usually still belong to the seller.'},
        {'id': 'c2', 'title': 'Unascertained goods, approval and right of disposal (Sections 23 to 25)', 'body': [
            'Section 23(1) — appropriation: where unascertained or future goods are sold by description, property passes when goods of that description, in a deliverable state, are unconditionally appropriated to the contract — by the seller with the buyer\'s assent or by the buyer with the seller\'s assent. Assent may be express or implied and may come before or after the appropriation.',
            'Section 23(2) — delivery to carrier: if, in performing the contract, the seller hands over the goods for transmission to the buyer — to the buyer himself, or to a carrier or other bailee, named by the buyer or not — without reserving the right of disposal, he is taken to have unconditionally appropriated them.',
            'Section 24 — goods on approval or "sale or return": property passes when the buyer (a) signifies approval or acceptance, or does any other act adopting the transaction (for example, sells or pledges the goods); or (b) keeps the goods without giving notice of rejection beyond the time fixed for return, or beyond a reasonable time if none is fixed. But if the terms say the goods remain the seller\'s until paid for, property passes only on payment.',
            'Section 25 — reservation of right of disposal: the seller of specific or appropriated goods may reserve the right to dispose of them until conditions (normally payment) are met; property does not pass until then even if the goods are with the buyer or a carrier. A bill of lading taken to the seller\'s own order is, prima facie, a reservation. Where the seller sends a bill of exchange with the bill of lading, the buyer who does not honour the bill of exchange gets no property by keeping the bill of lading.'],
         'analogy': 'Sale or return is like taking clothes home "on trial": they become yours if you keep the tags off and wear them, or keep them past the return date.',
         'work': 'Jewellers, publishers and FMCG firms send goods "on approval" or "on sale or return". At year end, the auditor checks which of these have been approved or kept past the return date — only those are sales.'},
        {'id': 'c3', 'title': 'Risk prima facie passes with property (Section 26)', 'body': [
            'Unless otherwise agreed, goods stay at the seller\'s risk until property passes to the buyer; once property passes, they are at the buyer\'s risk whether or not delivery has been made. In short: risk follows ownership, not possession.',
            'Exceptions: (1) the parties may agree otherwise; (2) where delivery is delayed through the fault of either party, the goods are at the risk of the party at fault as regards any loss that might not have occurred but for that fault; (3) the duties of a seller or buyer as bailee of the goods for the other remain — a party holding the other\'s goods must take reasonable care of them.'],
         'analogy': 'Risk travels in the same car as ownership, not in the delivery van.',
         'work': 'Insurance cover and claims in transit or warehouse fires hinge on who had the risk under Section 26 — CAs check this before booking an insurance claim receivable.'},
        {'id': 'c4', 'title': 'Transfer of title by non-owners (Sections 27 to 30)', 'body': [
            'Section 27 states the rule nemo dat quod non habet — a person cannot pass on a title he does not himself hold. A buyer from a person who is not the owner, and who does not sell with the owner\'s authority or consent, gets no better title than the seller had.',
            'The rule protects owners; the exceptions protect honest buyers and trade. In each exception the buyer must have acted in good faith and, usually, without notice of the defect.'],
         'blocks': [nemo],
         'analogy': 'You cannot give away a gift you were never given — except where the law steps in to protect an innocent person who trusted the appearance of ownership.',
         'work': 'Before a client buys second-hand vehicles or equipment, a CA verifies the seller\'s title (registration, invoices, charges). Most of the exceptions need good faith — documented checks are evidence of it.'},
        {'id': 'c5', 'title': 'Performance: duties and rules of delivery (Sections 31 to 36)', 'body': [
            'Section 31: the seller must deliver the goods and the buyer must accept and pay for them, according to the contract. Section 32: unless otherwise agreed, delivery and payment are concurrent conditions — the seller must be ready and willing to give possession in exchange for the price, and the buyer ready and willing to pay in exchange for possession.',
            'Section 33: any act the parties have agreed to treat as delivery, or any act that gives the buyer (or a person authorised to hold for him) possession of the goods, is delivery.',
            'Section 34: delivery of part of the goods, in progress of delivery of the whole, has the same effect as delivery of the whole for passing property; but part delivery with intention of separating that part does not count as delivery of the rest.',
            'Section 35: unless otherwise agreed, the seller need not deliver until the buyer applies for delivery.',
            'Section 36: (1) place — as agreed; if not, where the goods are at the time of sale (or, for goods to be made or acquired, where they are made or produced); (2) time — if the seller must send the goods and no time is fixed, within a reasonable time; (3) goods held by a third party — delivery takes place only when that person confirms to the buyer that he now holds the goods for the buyer (attornment); (4) demand or tender of delivery must be at a reasonable hour; (5) unless agreed otherwise, the seller bears the cost of putting the goods into a deliverable state.'],
         'analogy': 'Section 32 is like an exchange at a counter: the cashier holds out the parcel, you hold out the money — neither has to let go first.',
         'work': 'Contract terms like Ex-works, FOR destination or CIF fix the place, time and cost of delivery that Section 36 would otherwise supply — CAs read them to decide when revenue and risk transfer.'},
        {'id': 'c6', 'title': 'Wrong quantity, instalments, carriers, examination (Sections 37 to 41)', 'body': [
            'Section 37 — wrong quantity: (1) less than contracted — buyer may reject; if he accepts, he pays at the contract rate. (2) more than contracted — buyer may accept the contracted quantity and reject the rest, or reject the whole; if he accepts the whole, he pays for it at the contract rate. (3) contracted goods mixed with goods of a different description — buyer may accept the conforming goods and reject the rest, or reject the whole. (4) All this is subject to trade usage, special agreement or course of dealing.',
            'Section 38 — instalments: a buyer need not take delivery in parts unless the contract allows it. Where the contract provides for instalments, the effect of a defective instalment depends on the terms and the circumstances (whether the breach repudiates the whole contract or is severable).',
            'Section 39 — delivery to a carrier for sending to the buyer is prima facie delivery to the buyer. The seller must make a reasonable contract with the carrier; and where goods go by sea in circumstances where insurance is usual, he must inform the buyer in time to insure.',
            'Section 40 — where the seller agrees to deliver at his own risk at a distant place, the buyer still bears the risk of deterioration necessarily incidental to the course of transit.',
            'Section 41 — a buyer who has not previously examined the goods is not deemed to have accepted them until he has had a reasonable opportunity to examine them; the seller must, on request, afford such an opportunity.'],
         'analogy': 'Section 37 is a waiter bringing six samosas when you ordered four: send back two, send back all, or keep all and pay for six at the menu price.',
         'work': 'Goods-received notes and quantity variances are everyday matters in purchase audits; Section 37 tells the client what it may reject and what it must pay for.'},
        {'id': 'c7', 'title': 'Acceptance and its consequences (Sections 42 to 44)', 'body': [
            'Section 42 — the buyer is deemed to have accepted the goods when he (a) tells the seller he has accepted them; (b) after delivery, does an act in relation to the goods inconsistent with the seller\'s ownership (uses, resells, alters them); or (c) keeps them beyond a reasonable time without telling the seller that he rejects them.',
            'Section 43 — a buyer who rightfully refuses delivered goods need not return them; it is enough to inform the seller of his refusal.',
            'Section 44 — if the seller, being ready and willing, calls on the buyer to collect the goods and the buyer fails to collect within a reasonable time, the buyer must make good the loss flowing from his neglect or refusal and also pay a fair amount for looking after and storing the goods. The seller\'s rights where the refusal amounts to repudiation are not affected.'],
         'analogy': 'Using the phone you said you would "think about" is accepting it; you cannot later say you were still deciding.',
         'work': 'When a customer delays lifting goods, the CA in industry raises a Section 44 claim — storage, insurance and any loss on price fall — and books it only when recovery is probable.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Specific goods destroyed after the contract (Section 20 + 26)', 'difficulty': 'core', 'minutes': 6,
         'q': f'On Monday, Farah selects a particular finished teak sofa set displayed at Woodcraft and signs an unconditional order for {R(sofa)}; payment is to be made on delivery, fixed for Friday. On Wednesday night, an electrical fire (no negligence by Woodcraft) destroys the showroom and the sofa set. Who bears the loss?',
         'solution': [legal('Section 20: in an unconditional contract for specific goods in a deliverable state, property passes when the contract is made, even if payment and delivery are postponed. Section 26: unless otherwise agreed, risk passes with property, whether delivery has been made or not.',
                            'The sofa set was identified (specific), finished (deliverable) and the order was unconditional. Only payment and delivery were postponed to Friday. It was destroyed on Wednesday without the seller\'s fault.',
                            'Property passed on Monday when the contract was made; risk passed with it. Woodcraft held the sofa only as a bailee and was not negligent.',
                            f'Farah bears the loss and remains liable to pay {R(sofa)}.')],
         'checks': c[0:1]},
        {'id': 'i2', 'title': 'Goods to be weighed before the price is known (Section 22)', 'difficulty': 'moderate', 'minutes': 6,
         'q': 'Bansal agrees to buy "the entire stock of copper scrap lying in yard no. 3" from Metro Metals at ₹720 per kg. The scrap is ready for removal but has to be weighed by Metro Metals to find the price. Before weighing, the scrap is stolen in a night burglary without Metro\'s negligence. Metro Metals claims the price on an estimated weight. Decide.',
         'solution': [legal('Section 22: where specific goods in a deliverable state are sold but the seller is bound to weigh, measure or test them to ascertain the price, property does not pass until that is done and the buyer has notice. Section 26: risk follows property.',
                            'The scrap was specific (the whole stock in yard no. 3) and ready for removal, but the seller had to weigh it to fix the price. It was stolen before weighing.',
                            'Since weighing had not been done, property had not passed to Bansal, and the risk remained with Metro Metals.',
                            'Metro Metals bears the loss and cannot claim the price from Bansal.')]},
        {'id': 'i3', 'title': 'Sale or return — pledging the goods (Section 24)', 'difficulty': 'moderate', 'minutes': 6,
         'q': 'Kundan Jewellers delivers a diamond necklace worth ₹4,60,000 to Rhea "on sale or return within 7 days". On day 3 Rhea pledges the necklace with a moneylender, Mr. Sethi, for a loan. Kundan wants the necklace back from Mr. Sethi. Advise.',
         'solution': [legal('Section 24(a): when goods are delivered on approval or on sale or return, property passes to the buyer when he signifies approval or does any other act adopting the transaction.',
                            'The necklace was delivered on sale or return. Within the return period, Rhea pledged it with Mr. Sethi.',
                            'Pledging the necklace is an act inconsistent with merely holding it on trial; it adopts the transaction. Property passed to Rhea at that moment, so she could create a valid pledge. (The terms did not say that ownership would stay with the seller until payment.)',
                            'Mr. Sethi holds a valid pledge. Kundan cannot recover the necklace from him; its remedy is to sue Rhea for the price of ₹4,60,000.')]},
        {'id': 'i4', 'title': 'Delivery of the wrong quantity (Section 37)', 'difficulty': 'core', 'minutes': 7,
         'q': f'Prime Retail orders {ordered} cartons of juice at {R(rate)} per carton. (a) The supplier delivers {delivered_more} cartons. (b) In another month, it delivers only {delivered_less} cartons. State Prime Retail\'s options and the amount payable in each case.',
         'solution': [p('Section 37(2): where a larger quantity is delivered, the buyer may accept the contracted quantity and reject the rest, or reject the whole; if he accepts the whole, he pays at the contract rate. Section 37(1): where a smaller quantity is delivered, the buyer may reject; if he accepts, he pays at the contract rate.'),
                      table(['Case', 'Option', 'Amount payable (₹)'], [
                          [f'(a) {delivered_more} delivered', f'Accept {ordered}, reject {delivered_more - ordered}', inr(pay_contract)],
                          [f'(a) {delivered_more} delivered', 'Reject the whole', '0'],
                          [f'(a) {delivered_more} delivered', f'Accept all {delivered_more}', inr(pay_whole)],
                          [f'(b) {delivered_less} delivered', 'Reject the whole', '0'],
                          [f'(b) {delivered_less} delivered', f'Accept {delivered_less}', inr(pay_short)],
                      ]),
                      note('Working: 500 × 640 = 3,20,000; 560 × 640 = 3,58,400; 450 × 640 = 2,88,000. All at the contract rate — the buyer cannot be charged more per carton for extra goods.')],
         'checks': c[1:4]},
        {'id': 'i5', 'title': 'Seller in possession sells twice (Section 30(1))', 'difficulty': 'hard', 'minutes': 7,
         'q': 'On 2 May, Sameer sells his used tractor to Dhruv for ₹5,20,000 and receives payment. Dhruv asks Sameer to keep the tractor in his shed for a week. On 5 May Sameer sells and delivers the same tractor to Komal for ₹5,40,000; Komal knows nothing of the earlier sale. Dhruv claims the tractor from Komal. Decide.',
         'solution': [legal('Section 27: a buyer generally gets no better title than his seller. Section 30(1): if a seller who has already sold goods stays in possession of them and then sells or pledges and delivers them (himself or through a mercantile agent) to someone who takes them honestly and unaware of the first sale, that transfer is as effective as if the owner had authorised it.',
                            'Property passed to Dhruv on 2 May (specific goods, unconditional sale). Sameer stayed in possession and on 5 May sold and delivered the tractor to Komal, who acted in good faith without notice.',
                            'Although Sameer was no longer the owner, he was a seller in possession. Komal took delivery in good faith without notice, so the exception in Section 30(1) applies.',
                            'Komal gets a good title. Dhruv cannot recover the tractor from her; he can sue Sameer for damages / refund of ₹5,20,000.')]},
        {'id': 'i6', 'title': 'Buyer delays taking delivery (Section 44)', 'difficulty': 'moderate', 'minutes': 7,
         'q': f'Annapurna Mills is ready to deliver 120 bags of flour to Hotel Sunrise at ₹2,400 a bag and asks the hotel to collect them on 1 October. The hotel collects them only after {days_late} days, without any valid reason. A reasonable storage charge is {R(per_day)} per day. Because of the delay the mill also had to forgo a resale opportunity and its loss from the fall in price is ₹120 a bag. What can the mill recover besides the price?',
         'solution': [legal('Section 44: a buyer who, despite a request from a seller ready and willing to deliver, fails to take delivery within a reasonable time is answerable for the loss his neglect or refusal causes, plus a fair charge for keeping the goods safe.',
                            f'The mill was ready and asked the hotel to collect on 1 October. The hotel delayed {days_late} days without reason. Storage costs {R(per_day)} a day and the delay caused a loss of ₹120 a bag.',
                            'Both heads are recoverable under Section 44: custody charges and the loss occasioned by the delay.',
                            f'Besides the price, the mill can recover {R(s44_total)}.'),
                      table(['Head', 'Amount (₹)'], [[f'Care and custody: {days_late} days × ₹1,500', inr(storage)], ['Loss caused by delay: 120 bags × ₹120', inr(fall)], ['Total recoverable', inr(s44_total)]], num=[1], total=True)],
         'checks': c[4:7]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Goods "on approval" at the year end', 'role': 'Audit senior at a publishing house',
         'situation': 'Books worth ₹42 lakh were sent to bookshops on "sale or return within 60 days" during February and March. The client has booked all of them as sales in March.',
         'steps': ['List the consignments with dates, return periods and any approvals received.', 'Apply Section 24: property (and therefore a sale) arises only on approval, an act adopting the sale, or expiry of the return period without rejection.',
                   'Consignments still within the 60-day window at 31 March without approval are not sales; reverse them and include the books in closing stock at cost.', 'Check post-year-end returns as evidence.'],
         'takeaway': 'For sale-or-return goods the sale date is decided by Section 24, not by the despatch date.',
         'think': 'A bookshop sold some of the books to its customers in March but had not "approved" anything in writing. Has property passed for those books?',
         'answer': 'Yes. Reselling the books is an act adopting the transaction under Section 24(a), so property passed to the bookshop when it resold them.'},
        {'id': 'j2', 'title': 'Buying vehicles from a dealer — checking title', 'role': 'CA in industry, procurement head of a logistics company',
         'situation': 'A dealer offers ten used trucks at an attractive price. Two of them appear to be under hire purchase with a bank.',
         'steps': ['Recall nemo dat (Section 27): a hirer is not the owner, so a buyer from him generally gets no title.', 'Search the vehicle registration and hypothecation records, and ask for no-objection certificates from the financiers.',
                   'Obtain an indemnity and keep evidence of good faith; buy the two vehicles only after the financier releases them.'],
         'takeaway': 'Documented title checks protect the client — and good faith is the key to most exceptions anyway.'},
        {'id': 'j3', 'title': 'Delivery to the carrier and transit losses', 'role': 'Accounts manager of an e-commerce seller',
         'situation': 'Goods sent through a courier to a business buyer were lost in transit. The buyer refuses to pay.',
         'steps': ['Check the contract terms: who bears transit risk? If silent, delivery to the carrier for sending to the buyer is prima facie delivery to the buyer (Section 39(1)), and unconditional appropriation passes property (Section 23(2)).',
                   'Check whether the seller made a reasonable contract with the courier (Section 39(2)); if not, the buyer may refuse to treat it as delivery.',
                   'Decide whether to pursue the buyer for the price or lodge an insurance/courier claim, and record the receivable accordingly.'],
         'takeaway': 'Unless the contract says otherwise, risk in transit usually sits with the buyer once the seller properly hands the goods to the carrier.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'In a contract for the sale of unascertained goods, property passes:', 'options': ['Only after the goods are ascertained', 'When the contract is made', 'When the price is paid', 'Never'], 'answer': 0,
         'explain': 'Section 18 — no property passes until the goods are ascertained.', 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'Specific goods in a deliverable state are sold under an unconditional contract; delivery and payment are postponed. Property passes:', 'options': ['When the contract is made', 'On delivery', 'On payment', 'On delivery and payment both'], 'answer': 0,
         'explain': 'Section 20 — postponement of payment or delivery is immaterial.', 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm3', 'q': 'Where the seller must weigh specific goods to ascertain the price, property passes when:', 'options': ['The goods are weighed and the buyer has notice of it', 'The goods are weighed', 'The contract is made', 'The buyer pays'], 'answer': 0,
         'explain': 'Section 22 requires both the act and notice to the buyer.', 'concept': 'c1', 'difficulty': 'moderate'},
        {'id': 'm4', 'q': 'Goods are sent on "sale or return" and no time is fixed for return. The buyer keeps them without giving notice of rejection. Property passes:', 'options': ['On expiry of a reasonable time', 'Immediately on delivery', 'Never, until he pays', 'After 30 days by law'], 'answer': 0,
         'explain': 'Section 24(b): if no time is fixed, on the expiry of a reasonable time.', 'concept': 'c2', 'difficulty': 'moderate'},
        {'id': 'm5', 'q': 'A bill of lading taken out to the order of the seller indicates that the seller has prima facie:', 'options': ['Reserved the right of disposal', 'Transferred property to the buyer', 'Waived his lien', 'Made a sale or return'], 'answer': 0,
         'explain': 'Section 25(2).', 'concept': 'c2', 'difficulty': 'moderate'},
        {'id': 'm6', 'q': 'Unless otherwise agreed, risk passes:', 'options': ['With the property in the goods', 'With possession of the goods', 'With payment of the price', 'With the invoice'], 'answer': 0,
         'explain': 'Section 26 — risk prima facie passes with property, whether delivery has been made or not.', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm7', 'q': 'Delivery is delayed through the buyer\'s fault and the goods are damaged in the meantime. The loss caused by the delay falls on:', 'options': ['The buyer', 'The seller', 'Both equally', 'The carrier'], 'answer': 0,
         'explain': 'Section 26 proviso: the party at fault bears any loss that might not have occurred but for the fault.', 'concept': 'c3', 'difficulty': 'moderate'},
        {'id': 'm8', 'q': '"Nemo dat quod non habet" means:', 'options': ['No one can give what he does not have', 'Let the buyer beware', 'Risk follows ownership', 'Possession is nine-tenths of ownership'], 'answer': 0,
         'explain': 'Section 27 — a buyer from a non-owner generally gets no better title than the seller had.', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm9', 'q': 'A buyer in good faith gets a good title from a person who obtained the goods under a voidable contract, provided:', 'options': ['The contract had not been rescinded at the time of sale', 'The contract had already been rescinded', 'The buyer paid more than market price', 'The seller was a mercantile agent'], 'answer': 0,
         'explain': 'Section 29.', 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm10', 'q': 'Unless otherwise agreed, delivery of goods and payment of price are:', 'options': ['Concurrent conditions', 'Independent promises', 'Conditions precedent for the seller only', 'Warranties'], 'answer': 0,
         'explain': 'Section 32.', 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm11', 'q': 'A buyer ordered 200 units at ₹150 each; 240 are delivered and he decides to keep all of them. He must pay:', 'options': ['₹36,000', '₹30,000', '₹6,000', '₹42,000'], 'answer': 0,
         'explain': 'Section 37(2): accepting the whole means paying for it at the contract rate — 240 × 150 = 36,000.', 'concept': 'c6', 'difficulty': 'core', 'check': '240*150'},
        {'id': 'm12', 'q': 'Which of these is NOT a way in which the buyer is deemed to accept goods under Section 42?', 'options': ['He receives the goods and promptly informs the seller that he rejects them', 'He tells the seller he has accepted them', 'He resells the goods after delivery', 'He keeps the goods beyond a reasonable time without intimating rejection'], 'answer': 0,
         'explain': 'Timely notice of rejection is the opposite of acceptance; Section 43 says he need not even return the goods.', 'concept': 'c7', 'difficulty': 'moderate'},
    ]

    questions = [
        {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'text',
         'q': '"A buyer cannot acquire a better title than the seller had." Explain this rule and state the exceptions to it under the Sale of Goods Act, 1930.',
         'model': [p('Rule — Section 27 (nemo dat quod non habet): where goods are sold by a person who is not their owner and who does not sell with the authority or consent of the owner, the buyer gets no better title than the seller had, unless the owner is precluded by his conduct from denying the seller\'s authority.'),
                   p('Exceptions (the honest buyer gets a good title):'),
                   ul(['Estoppel — the owner by conduct led the buyer to believe the seller had authority (Section 27).',
                       'Mercantile agent — in possession of the goods or documents with the owner\'s consent, selling in the ordinary course of business, to a buyer in good faith without notice of want of authority (Section 27 proviso).',
                       'Joint owner in sole possession with the others\' permission — buyer in good faith without notice (Section 28).',
                       'Seller holding under a voidable contract not rescinded at the time of sale — buyer in good faith without notice (Section 29).',
                       'Seller continuing in possession after sale — delivery to a good-faith buyer without notice of the earlier sale (Section 30(1)).',
                       'Buyer in possession with the seller\'s consent before property passes — resale to a good-faith buyer without notice (Section 30(2)).',
                       'Unpaid seller who resells after exercising lien or stoppage in transit (Section 54(3)).',
                       'Sales under other laws — finder of goods (Contract Act s. 169), pawnee (s. 176), official receiver, liquidator or court officer.'])],
         'scheme': [{'id': 's1', 'pt': 'Rule stated with Section 27', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's2', 'pt': 'Mercantile agent and estoppel', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's3', 'pt': 'Joint owner, voidable contract', 'm': 1, 'skill': 'provision'},
                    {'id': 's4', 'pt': 'Seller / buyer in possession (Section 30)', 'm': 1, 'skill': 'provision'},
                    {'id': 's5', 'pt': 'Unpaid seller and other laws', 'm': 1, 'skill': 'provision'}],
         'remarks': ['Most candidates list the exceptions but forget to state that the buyer must act in good faith without notice — that costs marks in each point.'],
         'mistakes': ['Omitting the conditions for the mercantile-agent exception.', 'Writing "rescinded" instead of "not rescinded" for Section 29.'],
         'tips': ['Write each exception with its section number and the "good faith, no notice" condition.']},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'legal',
         'q': 'Sunrise Electronics delivers 10 air-conditioners to Cool Homes "on approval; to be returned within 15 days if not approved". Cool Homes neither approves nor rejects them, and still has them on day 25. Meanwhile 3 units are stolen from its warehouse on day 20. Who bears the loss of the stolen units, and what must Cool Homes pay if each unit is priced at ₹38,000?',
         'model': [legal('Section 24(b): where goods are delivered on approval or sale or return and the buyer retains them without giving notice of rejection, property passes on expiry of the time fixed for return. Section 26: risk passes with property.',
                         'The return period was 15 days. Cool Homes gave no notice of rejection and still held the goods after day 15. Three units were stolen on day 20.',
                         'Property in all 10 units passed to Cool Homes on expiry of 15 days. On day 20 the goods were at its risk.',
                         f'Cool Homes bears the loss of the stolen units and must pay for all 10 units: 10 × ₹38,000 = {R(c.add("10*38000", "price of 10 air-conditioners"))}.')],
         'scheme': [{'id': 's1', 'pt': 'Section 24(b) — retention beyond fixed time', 'm': 1, 'skill': 'provision'},
                    {'id': 's2', 'pt': 'Risk follows property — Section 26', 'm': 1, 'skill': 'provision'},
                    {'id': 's3', 'pt': 'Analysis — property passed on day 15; theft on day 20', 'm': 1, 'skill': 'analysis'},
                    {'id': 's4', 'pt': 'Conclusion with amount', 'm': 1, 'skill': 'conclusion'}],
         'remarks': ['The key is the date: property passed on day 15, before the theft on day 20.'],
         'mistakes': ['Holding the seller liable because Cool Homes "never approved" the goods.'],
         'tips': ['Draw a short time line: day 0 delivery → day 15 property passes → day 20 theft.'],
         'checks': [c[-1]]},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'State the rules regarding delivery of the wrong quantity of goods under Section 37 of the Sale of Goods Act, 1930.',
         'model': [ul(['Short delivery — the buyer may reject the goods; if he accepts them, he must pay at the contract rate [Section 37(1)].',
                       'Excess delivery — the buyer may (i) accept the contracted quantity and reject the excess, (ii) reject the whole, or (iii) accept the whole and pay for it at the contract rate [Section 37(2)].',
                       'Mixed delivery — where contracted goods are mixed with goods of a different description, the buyer may accept the goods that conform and reject the rest, or reject the whole [Section 37(3)].',
                       'All of the above give way to a trade custom, a special agreement or the past course of dealing of the parties [Section 37(4)].'])],
         'scheme': [{'id': 's1', 'pt': 'Short delivery', 'm': 1, 'skill': 'provision'}, {'id': 's2', 'pt': 'Excess delivery — three options', 'm': 1, 'skill': 'provision'},
                    {'id': 's3', 'pt': 'Mixed delivery', 'm': 1, 'skill': 'provision'}, {'id': 's4', 'pt': 'Subject to trade usage / agreement', 'm': 1, 'skill': 'provision'}],
         'remarks': ['The fourth point (trade usage) is often missed.'],
         'mistakes': ['Saying the buyer must pay a higher rate for excess goods.'],
         'tips': ['A small example with figures makes the excess-delivery options clear.']},
        {'id': 'q4', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'core', 'pad': 'text',
         'q': 'Explain any six rules regarding delivery of goods under the Sale of Goods Act, 1930.',
         'model': [ul(['Mode (Section 33): anything agreed as delivery, or which puts the goods in the possession of the buyer or his authorised agent.',
                       'Delivery and payment are concurrent conditions unless otherwise agreed (Section 32).',
                       'Part delivery in progress of delivery of the whole operates as delivery of the whole for passing property, unless intended to sever that part (Section 34).',
                       'The seller is not bound to deliver until the buyer applies for delivery (Section 35).',
                       'Place: as agreed, else where the goods are at the time of sale; time: if seller must send, within a reasonable time (Section 36(1), (2)).',
                       'Goods held by a third party: delivery only when he acknowledges to the buyer that he holds on the buyer\'s behalf (Section 36(3)).',
                       'Demand or tender at a reasonable hour; expenses of putting goods into a deliverable state borne by the seller (Section 36(4), (5)).',
                       'Buyer not bound to accept instalments (Section 38); delivery to a carrier is prima facie delivery to the buyer (Section 39); buyer bears deterioration necessarily incidental to transit (Section 40); right to examine (Section 41).'])],
         'scheme': [{'id': 's1', 'pt': 'Any six rules, one mark each, with section reference', 'm': 6, 'skill': 'provision'}],
         'remarks': ['Answers that write six distinct rules with sections score full marks; vague points like "delivery should be proper" earn nothing.'],
         'mistakes': ['Repeating Section 36 sub-rules as separate "rules" without content.'],
         'tips': ['Number your rules 1 to 6 and put the section in brackets at the end of each.']},
    ]

    viva = [
        V('v1', 'When does property pass in specific goods that are in a deliverable state?',
          'Under Section 20, if the contract is unconditional and the goods are specific and in a deliverable state, property passes to the buyer when the contract is made. It does not matter that payment or delivery or both are postponed.',
          [P('p1', 'Unconditional contract, specific goods, deliverable state', 3, 'unconditional|no condition|without condition', 'specific|identified', 'deliverable|ready', min=2),
           P('p2', 'Property passes when the contract is made', 5, ALT('{pp} when contract made', '{pp} when contract is made', '{pp} at the time of contract', '{pp} on making contract', '{pp} immediately', '{pp} at once', '{pp} at contract', 'contract made {pp}', pp=('property pass', 'property passes', 'ownership pass', 'ownership passes', 'property transfer', 'ownership transfer'))),
           P('p3', 'Even if payment or delivery is postponed', 2, 'postpone|delay|later|deferred|immaterial|does not matter|even if|even though', min=1)], 'c1'),
        V('v2', 'When does property pass where goods are sent on approval or sale or return?',
          'Under Section 24, property passes when the buyer signifies approval or acceptance or does an act adopting the transaction, like reselling or pledging the goods; or when he keeps the goods without giving notice of rejection beyond the time fixed for return, or beyond a reasonable time if no time is fixed.',
          [P('p1', 'Buyer signifies approval / acceptance', 3, 'approv|accept|agree|confirm'),
           P('p2', 'Act adopting the transaction (resale, pledge)', 3, 'adopt|pledge|resell|resale|sell|sold|pledged|use as owner'),
           P('p3', 'Retains beyond the fixed time (or reasonable time) without notice of rejection', 4, 'retain|keep|keeps|kept|hold', 'time fixed|fixed time|reasonable time|return period|time for return|time limit|date fixed|beyond time|after time', min=2)], 'c2'),
        V('v3', 'What is the rule as to passing of risk, and what are its exceptions?',
          'Under Section 26, unless otherwise agreed, risk passes with property, whether or not delivery has been made. Exceptions are: the parties may agree otherwise; where delivery is delayed by the fault of one party, the goods are at that party\'s risk for loss caused by the delay; and a party holding goods as bailee for the other must still take reasonable care.',
          [P('p1', 'Risk passes with property (not possession)', 5, ALT('risk {f}', 'risk passes {f}', 'risk goes {f}', 'risk pass {f}', 'risk is transferred {f}', f=('with property', 'with ownership', 'follows property', 'follows ownership', 'along with property', 'along with ownership', 'property', 'ownership')) + '|passes with property|passes with ownership|goes with property|goes with ownership|follows ownership|follows property|travels with ownership|travels with property'),
           P('p2', 'Delay by fault — party at fault bears the loss', 3, 'fault|delay', 'bear|liable|risk|responsible|loss', min=2),
           P('p3', 'Agreement to the contrary / duties as bailee', 2, 'agree|contrary|otherwise|bailee|care', min=1)], 'c3'),
        V('v4', 'State the rule of nemo dat and name any three exceptions.',
          'Nemo dat quod non habet means no one can give what he does not have, so a buyer from a non-owner gets no better title than the seller. Exceptions include sale by a mercantile agent, sale by one of joint owners, sale under a voidable contract not yet rescinded, sale by a seller or buyer in possession, estoppel, and resale by an unpaid seller.',
          [P('p1', 'No one can give what he does not have — buyer gets no better title', 4, 'no one can give|cannot give|can not give|no better title|not better title|same title|no title', min=1),
           P('p2', 'Any three exceptions', 6, 'mercantile agent|agent', 'joint owner|co owner|joint', 'voidable', 'seller in possession|seller possession|remains in possession|continues in possession', 'buyer in possession|buyer possession', 'estoppel|estopped', 'unpaid seller', 'finder|pawnee|liquidator|official receiver', min=3)], 'c4'),
        V('v5', 'What are the buyer\'s options when the seller delivers more than the contracted quantity?',
          'Under Section 37(2) the buyer may accept the contracted quantity and reject the excess, or reject the whole lot, or accept the whole and pay for it at the contract rate.',
          [P('p1', 'Accept the contracted quantity and reject the rest', 4, ALT('{a} {q} {j} {r}', a=('accept', 'keep', 'take', 'retain'), j=('reject', 'return', 'refuse', 'send back'), q=('contracted', 'contract quantity', 'ordered', 'quantity ordered', 'agreed quantity', 'what he ordered', 'quantity contracted'), r=('rest', 'excess', 'extra', 'balance', 'remaining', 'surplus'))),
           P('p2', 'Reject the whole', 3, 'reject whole|reject the whole|reject all|reject entire|reject everything|return all|refuse whole|refuse all'),
           P('p3', 'Accept the whole and pay at the contract rate', 3, 'accept whole|accept all|keep all|accept entire|accept everything|take all', 'contract rate|contract price|same rate|agreed rate|agreed price', min=2)], 'c6'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Silk sarees on sale or return', 'difficulty': 'hard',
        'case': ('Kanchi Weavers sent 12 silk sarees, priced at ₹7,500 each, to Trends Boutique on 1 March "on sale or return within 10 days". On 4 March the boutique sold 4 sarees '
                 'to its customers. On 8 March it returned 3 sarees with a note rejecting them. It kept the remaining 5 sarees without saying anything until 25 March, when it '
                 'tried to return them. Kanchi Weavers refused to take them back.'),
        'mcqs': [
            M('k1a', 'When did property in the 4 sarees sold to customers pass to Trends Boutique?', ['On 4 March, when it resold them', 'On 1 March, on delivery', 'On 11 March, on expiry of 10 days', 'Never — goods on approval never become the buyer\'s'], 0,
              'Reselling is an act adopting the transaction — Section 24(a).', 'moderate'),
            M('k1b', 'Is Kanchi Weavers bound to take back the 5 sarees on 25 March?', ['No — property passed when the 10 days expired without notice of rejection', 'Yes — the boutique never approved them', 'Yes — goods on sale or return can be returned at any time', 'No — because the boutique sold some other sarees'], 0,
              'Section 24(b): retention beyond the fixed time without notice of rejection passes property.', 'hard'),
            M('k1c', 'How much must Trends Boutique pay Kanchi Weavers in all?', ['₹67,500', '₹90,000', '₹30,000', '₹37,500'], 0,
              f'Pay for 4 sold + 5 retained = 9 sarees × ₹7,500 = ₹67,500. The 3 rejected in time are not paid for (12 × 7,500 = {R(k_sarees)} is the total sent; the 5 retained alone are {R(k_kept)}).', 'hard', '9*7500'),
            M('k1d', 'Had the delivery note said "sarees remain the property of Kanchi Weavers until paid for", the 4 sarees sold to customers on 4 March would have:', ['Remained Kanchi\'s property until payment, the boutique not having become owner first', 'Become the boutique\'s on delivery', 'Become the customers\' automatically as the boutique was the owner', 'Been treated as a hire purchase'], 0,
              'Where the terms reserve ownership until payment, property does not pass merely by an act of adoption; it passes only when the terms are complied with. (Whether the customers get title would then depend on the exceptions to nemo dat, such as Section 30(2).)', 'hard'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch03', 'n': 3, 'title': 'Transfer of Ownership and Delivery of Goods',
        'outcomes': ['Apply Sections 18 to 25 to decide when property in goods passes from seller to buyer — specific, unascertained, approval and reservation cases.',
                     'Explain the rule that risk prima facie passes with property (Section 26) and its exceptions.',
                     'State the rule nemo dat quod non habet and its exceptions (Sections 27 to 30 and others).',
                     'Explain the duties of seller and buyer and the rules of delivery, acceptance and rejection (Sections 31 to 44), and solve related problems.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 55, 'practice': 50}, 'prereq': ['fnd-p2-ch03-u01'],
                 'exam_tip': 'Problems ask "who bears the loss?" — find when property passed (Sections 20–24), then apply Section 26. For title questions, state Section 27 and test the right exception, especially good faith and notice.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Unascertained goods: no property until ascertained (18). Specific goods: when intended (19) — rules in 20 to 24.',
                        '20: deliverable + unconditional → at contract. 21: seller to make deliverable → when done + notice. 22: seller to weigh/measure/test → when done + notice.',
                        '23: unconditional appropriation with assent; delivery to carrier without reserving disposal = appropriation. 24: approval/adoption/retention beyond time. 25: right of disposal reserved → passes on conditions.',
                        '26: risk follows property; exceptions — agreement, delay by fault, bailee\'s duties.',
                        '27: nemo dat; exceptions — mercantile agent, estoppel, joint owner (28), voidable contract (29), seller/buyer in possession (30), unpaid seller (54(3)), other laws.',
                        '31–36: duties, concurrent conditions, modes, part delivery, buyer to apply, place/time/third party/hour/expenses. 37–41: wrong quantity, instalments, carrier, transit deterioration, examination. 42–44: acceptance, no duty to return rejected goods, liability for neglecting delivery.'],
            'remember': ['Sections 21 and 22 need the act done AND notice to the buyer.', 'Section 37: extra goods accepted are paid at the contract rate.', 'Section 43: rightful rejection — just notify, no need to return.'],
            'traps': ['Risk follows ownership, not possession.', 'In Section 29 the contract must NOT have been rescinded at the time of sale.', 'Sale or return with "property till paid" clause: adoption alone does not pass property.',
                      'Delivery to a carrier is only prima facie delivery to the buyer — reserved right of disposal changes it.']},
        'quickref': [{'k': 'Sections 18–19', 'v': 'Unascertained: not until ascertained · Specific: as intended'},
                     {'k': 'Section 20', 'v': 'Specific + deliverable + unconditional → at contract'},
                     {'k': 'Sections 21–22', 'v': 'Thing to be done / weigh-measure-test → when done + buyer has notice'},
                     {'k': 'Section 23', 'v': 'Unconditional appropriation with assent; delivery to carrier'},
                     {'k': 'Section 24', 'v': 'Approval · adopting act · retention beyond time'},
                     {'k': 'Section 26', 'v': 'Risk prima facie passes with property'},
                     {'k': 'Section 27–30', 'v': 'Nemo dat + mercantile agent, estoppel, joint owner, voidable contract, seller/buyer in possession'},
                     {'k': 'Section 37', 'v': 'Short: reject or pay contract rate · Excess: accept contracted / reject all / accept all at contract rate'},
                     {'k': 'Section 42–44', 'v': 'Deemed acceptance · rejected goods need not be returned · buyer liable for delay in taking delivery'}],
        'viva': viva, 'cases': cases,
    }
