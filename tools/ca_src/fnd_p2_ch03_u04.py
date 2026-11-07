"""CA Foundation · Paper 2 Business Laws · Chapter 3 The Sale of Goods Act, 1930 · Unit 4 Unpaid Seller.
Original explanations, facts and questions; sections are cited, never quoted at length."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p2-ch03-u04'


def build():
    c = Checks()
    # i1 — is the seller unpaid?
    price1, paid1 = 275000, 250000
    due1 = c.add('275000-250000', 'balance unpaid')
    # i4 — resale after notice (Section 54(2))
    qty, crate, rrate, rexp = 300, 2150, 1980, 7500
    contract_val = c.add('300*2150', 'contract value')
    resale_val = c.add('300*1980', 'resale proceeds')
    loss_resale = c.add('300*2150-300*1980+7500', 'loss recoverable = contract value − resale proceeds + resale expenses')
    # i5 — damages for non-delivery (Section 57)
    q5, c5, m5 = 80, 46500, 49800
    dmg_nd = c.add('80*(49800-46500)', 'damages = quantity × (market price on delivery date − contract price)')
    # i6 — Section 64A
    base6, old6, new6 = 800000, 12, 18
    tax_old = c.add('800000*12/100', 'GST at the old rate')
    tax_new = c.add('800000*18/100', 'GST at the new rate')
    extra = c.add('800000*18/100-800000*12/100', 'increase the seller may add to the price')
    total6 = c.add('800000+800000*18/100', 'amount payable by the buyer')
    # i2 — part delivery lien
    units2, rate2, deliv2 = 50, 18000, 20
    lien_val = c.add('(50-20)*18000', 'value of goods still held under lien')
    # case — non-acceptance
    k_q, k_c, k_m = 500, 1240, 1105
    k_dmg = c.add('500*(1240-1105)', 'damages for non-acceptance')
    k_resale_profit = c.add('500*(1300-1240)', 'surplus on resale above contract price')

    lien_vs_stop = table(['Basis', 'Lien (Sections 47–49)', 'Stoppage in transit (Sections 50–52)'], [
        ['Essence', 'Right to retain possession', 'Right to regain possession'],
        ['Possession', 'Seller must be in possession', 'Seller has parted with possession; goods are with a carrier or other bailee in transit'],
        ['Buyer\'s insolvency', 'Not necessary (available on cash sale, expired credit, or insolvency)', 'Essential — buyer must be insolvent'],
        ['When it starts/ends', 'Ends when goods leave the seller\'s possession', 'Starts where lien ends; ends when the buyer or his agent takes delivery'],
    ], title='Lien vs stoppage in transit')

    concepts = [
        {'id': 'c1', 'title': 'Who is an unpaid seller? (Section 45)', 'body': [
            'A seller counts as unpaid when (a) any part of the price is still outstanding (neither paid nor tendered) and he is entitled to sue for it right now; or (b) he has received a bill of exchange, cheque or other negotiable instrument as conditional payment, and the condition has failed because the instrument was dishonoured or otherwise.',
            'Even a part of the price remaining unpaid makes him an unpaid seller. But if goods were sold on credit and the credit period is still running, he has no immediate right of action, so he is not yet an unpaid seller for most purposes (the insolvency of the buyer changes this for lien).',
            '"Seller" here extends to anyone standing in the seller\'s shoes — for example the seller\'s agent holding an endorsed bill of lading, or a consignor or agent who has himself paid the price or is directly answerable for it.'],
         'analogy': 'An unpaid seller is a shopkeeper who has your money missing from the till — whether you never paid, paid only part, or paid with a cheque that bounced.',
         'work': 'Credit controllers rely on unpaid-seller rights to protect receivables — holding stock (lien) or stopping consignments in transit when a customer goes into insolvency proceedings.'},
        {'id': 'c2', 'title': 'Rights of an unpaid seller — overview (Section 46)', 'body': [
            'Even after property has passed to the buyer, the law gives the unpaid seller: (a) a lien — the right to hold on to the goods for the price as long as he has them; (b) on the buyer\'s insolvency, a right of stopping the goods in transit after parting with possession; and (c) a limited right of resale.',
            'Where property has not yet passed, he can also simply refuse to deliver — a right that works just like lien and stoppage and is as wide as they are (sometimes called a quasi-lien).',
            'Against the buyer personally, he has: suit for price (Section 55), suit for damages for non-acceptance (Section 56), suit on repudiation before the due date (Section 60) and suit for interest / special damages (Section 61).'],
         'analogy': 'Think of two toolkits: one works on the goods (keep them, stop them, resell them), the other works on the buyer (sue him).',
         'work': 'When a customer defaults, a CA advising the seller first checks where the goods are — in the godown, in transit or with the buyer — because that decides which toolkit is available.'},
        {'id': 'c3', 'title': 'Lien (Sections 47 to 49)', 'body': [
            'Section 47: the unpaid seller in possession may retain the goods until the price is paid or tendered where (a) the goods were sold without any stipulation as to credit; (b) they were sold on credit but the credit period has expired; or (c) the buyer has become insolvent. He may exercise lien even if he holds the goods as the buyer\'s agent or bailee. Lien is only for the price — not for storage charges or other costs.',
            'Section 48: after a part delivery, the seller may retain the rest, unless the part delivery shows an agreement to waive the lien.',
            'Section 49: lien is lost when (a) the seller hands the goods to a carrier or other bailee to be sent to the buyer and keeps no right of disposal; (b) the buyer or his agent lawfully obtains possession; or (c) the seller waives it (expressly or by conduct, e.g. agreeing to a sub-sale). The seller does not lose his lien merely because he has obtained a court decree for the price.'],
         'analogy': 'Lien is the shopkeeper keeping your parcel behind the counter until you pay — he cannot keep it once he hands it to the courier.',
         'work': 'In warehousing and job-work arrangements, the client\'s lien over customer stock is a key credit-risk mitigant that auditors consider when assessing expected credit losses.'},
        {'id': 'c4', 'title': 'Stoppage in transit (Sections 50 to 52)', 'body': [
            'Section 50: when the buyer becomes insolvent, the unpaid seller who has parted with possession may resume possession of the goods while they are in the course of transit and retain them until paid. Conditions: seller unpaid; possession parted with; goods in transit; buyer insolvent.',
            'Section 51 — duration of transit: from delivery to a carrier or other bailee for transmission until the buyer or his agent takes delivery from that carrier or bailee. Transit ends earlier if: the buyer or his agent obtains delivery before arrival at the destination (interception); after arrival the carrier acknowledges to the buyer that he now holds the goods for him; the carrier wrongfully refuses to deliver to the buyer; the goods are put on a vessel the buyer has chartered, so that the master is the buyer\'s agent; or part delivery is made in circumstances showing an agreement to give up possession of the whole. If the buyer rejects the goods and the carrier keeps them, transit is not ended.',
            'Section 52: stoppage is effected by taking actual possession or by giving notice of the claim to the carrier or bailee in possession (or to his principal, in time to prevent delivery). The carrier must then redeliver to the seller or as he directs, at the seller\'s expense.',
            'Exercising stoppage does not rescind the contract; the buyer (or his insolvency administrator) can still take the goods on paying the price.'],
         'blocks': [lien_vs_stop],
         'analogy': 'Stoppage in transit is phoning the courier to turn the parcel round because you have just heard the buyer has gone bankrupt.',
         'work': 'Exporters\' finance teams track customer insolvency news and act quickly through the shipping line, because the right ends the moment the buyer takes delivery.'},
        {'id': 'c5', 'title': 'Effect of sub-sale or pledge, and right of resale (Sections 53 and 54)', 'body': [
            'Section 53: the unpaid seller\'s lien or stoppage is not affected by the buyer\'s sale or pledge of the goods, unless the seller has assented to it. But if a document of title has been lawfully transferred to the buyer and the buyer transfers it to a person who takes it in good faith and for consideration: if by way of sale, the lien/stoppage is defeated; if by way of pledge, the seller\'s rights are subject to the pledgee\'s rights (the seller may ask the pledgee to look first to the buyer\'s other securities).',
            'Section 54 — resale: (1) mere lien or stoppage does not rescind the contract. (2) The unpaid seller who has exercised lien or stoppage may resell where the goods are perishable, or where he gives notice of his intention to resell and the buyer does not pay or tender the price within a reasonable time. As per the study material, if he resells after notice he may recover from the original buyer the loss on resale and may keep any surplus; if he resells without notice, he cannot recover any loss and must account to the buyer for any surplus. (3) The new buyer gets good title against the original buyer even if no notice of resale was given. (4) Where the contract expressly reserves a right of resale on the buyer\'s default, the seller may resell and the original contract is rescinded, without prejudice to his claim for damages.'],
         'analogy': 'Resale is the shopkeeper finally selling your uncollected, unpaid parcel to someone else — and billing you for any shortfall if he warned you first.',
         'work': 'Commodity traders routinely send resale notices before disposing of uncollected lots; a CA checks that notice was given before the client books a claim for the shortfall against the defaulting buyer.'},
        {'id': 'c6', 'title': 'Seller\'s rights against the buyer (Sections 55, 56, 60, 61)', 'body': [
            'Section 55 — suit for price: (1) where property has passed and the buyer wrongfully neglects or refuses to pay, the seller may sue for the price; (2) where the contract fixes a definite date for payment regardless of delivery, the seller may sue for the price on default even if ownership has not passed and no goods have yet been set aside for the contract.',
            'Section 56 — damages for non-acceptance: where the buyer wrongfully refuses to accept and pay, the seller may sue for damages, measured under Section 73 of the Contract Act — usually the contract price minus the market price on the date fixed for acceptance.',
            'Section 60 — repudiation before the due date (anticipatory breach): the other party may treat the contract as subsisting and wait till the due date, or treat it as rescinded and sue for damages at once.',
            'Section 61 — interest and special damages: the Act does not affect the right to recover interest or special damages where recoverable by law. In the absence of a contract, the court may award interest at a rate it thinks fit on the price, from the date of tender of the goods or from the date the price was payable.'],
         'analogy': 'If property has passed, the seller sues for his money (price); if not, he sues for what he lost (damages).',
         'work': 'Litigation provisioning: a claim for the price is a receivable already earned; a claim for damages is a contingent asset that is not recognised until virtually certain.'},
        {'id': 'c7', 'title': 'Buyer\'s remedies against the seller (Sections 57 to 61)', 'body': [
            'Section 57 — damages for non-delivery: a buyer whose seller wrongfully fails or declines to deliver may sue for damages — usually the market price on the delivery date minus the contract price (and special damages if the seller knew of special circumstances, e.g. a resale contract).',
            'Section 58 — specific performance: in a suit for breach of a contract to deliver specific or ascertained goods, the court may order the seller to deliver, subject to the Specific Relief Act, 1963 — typically where damages would not be adequate, e.g. unique or rare goods.',
            'Section 59 — breach of warranty (or breach of condition treated as warranty): the buyer cannot reject, but may set up the breach to reduce or extinguish the price, or sue for damages (and both, if his loss exceeds the price reduction).',
            'Section 60 — anticipatory breach by the seller: wait till the due date or sue at once.',
            'Section 61 — interest and refund: the buyer may recover interest or special damages, and money paid where the consideration has failed; in a suit for refund of the price after the seller\'s breach, the court may award interest from the date of payment.'],
         'analogy': 'Damages put the buyer where he would have been with the goods; specific performance actually hands him the goods — used only when money cannot do the job.',
         'work': 'Procurement teams quantify non-delivery claims as the extra cost of buying substitute goods in the market — exactly the Section 57 measure.'},
        {'id': 'c8', 'title': 'Auction sales (Section 64) and change in taxes (Section 64A)', 'body': [
            'Section 64: (1) each lot is prima facie a separate contract; (2) the sale is complete on the fall of the hammer or other customary announcement — until then any bidder may withdraw his bid; (3) the seller may expressly keep a right to bid, and only then may he, or one person for him, bid; (4) where the sale is not notified as subject to such a right, the seller may not bid or employ anyone to bid, nor may the auctioneer knowingly take such a bid — a sale in breach may be treated as fraudulent by the buyer; (5) the sale may be notified as subject to a reserve or upset price; (6) if the seller uses sham bidders (puffers) to push the price up, the buyer may avoid the sale. The auctioneer is the seller\'s agent.',
            'Section 64A: where, after the contract is made but before it is performed, a duty of customs or excise, or a tax on the sale or purchase of goods, is imposed, increased, decreased or remitted, then unless the contract provides otherwise — the seller may add the new or increased tax to the price, and the buyer may deduct the decrease or remission. Parties can exclude this by agreement.'],
         'analogy': 'Section 64A is a thermostat on the price: if the government turns the tax up after you sign, the price goes up by that much; if it turns it down, the price comes down.',
         'work': 'When GST rates change between order and invoice, CAs advise whether the client can pass on the increase — Section 64A says yes unless the contract fixed a tax-inclusive price.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Is the seller "unpaid"?', 'difficulty': 'core', 'minutes': 6,
         'q': f'Decide whether the seller is an unpaid seller: (a) Goods sold for {R(price1)}; buyer paid {R(paid1)}. (b) Goods sold for ₹1,40,000; buyer gave a cheque for the full amount, which was dishonoured. (c) Goods sold on 90 days\' credit; 30 days have passed and the buyer is solvent.',
         'solution': [legal('Section 45(1): a seller is unpaid when the whole price has not been paid or tendered and he has an immediate right of action for it, or when a negotiable instrument received as conditional payment has been dishonoured.',
                            f'(a) {R(due1)} remains unpaid. (b) The cheque was dishonoured. (c) Credit period is still running and the buyer is solvent.',
                            '(a) Even part of the price unpaid is enough. (b) A cheque is conditional payment; on dishonour the condition fails. (c) No immediate right of action exists during the credit period.',
                            '(a) Unpaid seller. (b) Unpaid seller. (c) Not yet an unpaid seller — he becomes one when the credit expires unpaid (or may exercise lien earlier if the buyer becomes insolvent).')],
         'checks': c[0:1]},
        {'id': 'i2', 'title': 'Lien after part delivery (Sections 47–48)', 'difficulty': 'moderate', 'minutes': 6,
         'q': f'Zenith Motors sells {units2} electric scooters to RideNow at {R(rate2)} each, cash on delivery. It delivers {deliv2} scooters (no payment received) and then learns that RideNow has stopped paying its creditors. Can Zenith refuse to deliver the rest? What is the value of the goods it can hold?',
         'solution': [legal('Section 47: an unpaid seller in possession may retain the goods until payment where they were sold without credit, or the buyer becomes insolvent. Section 48: after part delivery, he may exercise lien on the remainder unless the part delivery shows an agreement to waive the lien.',
                            f'The sale was for cash. {deliv2} scooters were delivered without payment; {units2 - deliv2} remain with Zenith. RideNow has stopped paying its debts — it is insolvent within Section 2(8).',
                            'Zenith is an unpaid seller in possession of the balance. Nothing shows that the part delivery was meant to waive the lien.',
                            f'Zenith can retain the remaining {units2 - deliv2} scooters (worth {R(lien_val)}) until the price is paid or tendered.'),
                      wn('Working', f'({units2} − {deliv2}) × {R(rate2)} = {R(lien_val)}')],
         'checks': [c[9]]},
        {'id': 'i3', 'title': 'Has transit ended? (Sections 50–51)', 'difficulty': 'hard', 'minutes': 7,
         'q': 'Rao Exports of Chennai sends 400 cartons of machine parts to Delhi Engineering by a road transporter. While the goods are on the way, Delhi Engineering is admitted into insolvency proceedings. Rao gives the transporter notice to stop the goods. Consider two alternatives: (a) the goods have reached the transporter\'s Delhi depot but have not yet been handed over; (b) Delhi Engineering\'s agent met the truck at Agra and took delivery there before the notice was given.',
         'solution': [legal('Section 50: an unpaid seller who has parted with possession may stop the goods in transit when the buyer becomes insolvent. Section 51: goods are in transit from delivery to the carrier until the buyer or his agent takes delivery; if the buyer or his agent obtains delivery before the destination, transit ends.',
                            'Rao is unpaid, parted with possession to a carrier, and the buyer is insolvent. In (a) the goods are still with the carrier at the destination depot; in (b) the buyer\'s agent took delivery at Agra before notice.',
                            '(a) The carrier still holds the goods and has not acknowledged holding them for the buyer, so transit continues; a notice under Section 52 is effective. (b) The buyer\'s agent intercepted the goods — transit ended at Agra, so the right of stoppage was lost before notice.',
                            '(a) Rao can stop the goods and the transporter must redeliver them to Rao (at Rao\'s expense). (b) Rao cannot stop the goods; he can only prove as a creditor for the price.')]},
        {'id': 'i4', 'title': 'Resale after notice — recovering the loss (Section 54)', 'difficulty': 'moderate', 'minutes': 8,
         'q': f'Gopal sells {qty} quintals of wheat to Amar at {R(crate)} per quintal. Amar fails to pay and take delivery. Gopal, holding the wheat under lien, sends Amar written notice of his intention to resell. Amar still does not pay within a reasonable time. Gopal resells at {R(rrate)} per quintal, incurring resale expenses of {R(rexp)}. How much can Gopal recover from Amar?',
         'solution': [legal('Section 54(2): an unpaid seller who has exercised his lien may resell the goods if he gives notice of his intention to resell and the buyer does not pay or tender the price within a reasonable time; on such resale he may recover from the original buyer damages for any loss occasioned by the breach.',
                            f'Gopal exercised lien, gave notice and waited a reasonable time. Resale at {R(rrate)} was below the contract rate of {R(crate)}; expenses were {R(rexp)}.',
                            'Notice was given, so Gopal is entitled to recover the shortfall on resale together with the reasonable expenses of the resale.',
                            f'Gopal can recover {R(loss_resale)} from Amar.'),
                      table(['Particulars', 'Amount (₹)'], [[f'Contract price ({qty} × ₹2,150)', inr(contract_val)], [f'Less: resale proceeds ({qty} × ₹1,980)', '(' + inr(resale_val) + ')'], ['Shortfall on resale', inr(contract_val - resale_val)], ['Add: resale expenses', inr(rexp)], ['Amount recoverable', inr(loss_resale)]])],
         'checks': c[1:4]},
        {'id': 'i5', 'title': 'Damages for non-delivery (Section 57)', 'difficulty': 'core', 'minutes': 6,
         'q': f'Fabtex agrees to supply {q5} bales of yarn to Loom Works at {R(c5)} per bale, delivery on 15 July. Fabtex refuses to deliver. On 15 July the market price is {R(m5)} per bale, and Loom Works buys substitute yarn at that price. What damages can Loom Works claim?',
         'solution': [legal('Section 57: a buyer may claim damages for non-delivery when the seller wrongfully fails or declines to deliver. Under Section 73 of the Contract Act, damages are the loss naturally arising — ordinarily the excess of the market price on the delivery date over the contract price.',
                            f'Contract price {R(c5)}; market price on the delivery date {R(m5)}; quantity {q5} bales.',
                            f'Loss per bale = {R(m5)} − {R(c5)} = {R(m5 - c5)}. This is the extra cost of putting Loom Works in the position it would have been in had the contract been performed.',
                            f'Loom Works can claim damages of {R(dmg_nd)}.')],
         'checks': c[4:5]},
        {'id': 'i6', 'title': 'Tax rate rises after the contract (Section 64A)', 'difficulty': 'core', 'minutes': 6,
         'q': f'On 1 June, Vikas Appliances contracts to sell goods to Neha Stores for {R(base6)} plus GST; GST is then {old6}%. Before delivery on 20 June, the GST rate on the goods is raised to {new6}%. The contract says nothing about tax changes. What can Vikas charge?',
         'solution': [legal('Section 64A: where, after the contract and before its performance, any tax on the sale or purchase of the goods is imposed or increased, the seller may add the increase to the contract price (and the buyer may deduct a decrease), unless the contract provides otherwise.',
                            f'The rate rose from {old6}% to {new6}% between contract and delivery. The contract is silent on tax changes.',
                            f'Vikas may add the increased tax. GST at {new6}% = {R(tax_new)}, against {R(tax_old)} at the old rate — an increase of {R(extra)}.',
                            f'Vikas can charge {R(total6)} in all (price {R(base6)} + GST {R(tax_new)}). Neha Stores must pay the increase.')],
         'checks': c[5:9]},
        {'id': 'i7', 'title': 'Seller bidding at an auction (Section 64)', 'difficulty': 'moderate', 'minutes': 6,
         'q': 'An auction of a vintage car is advertised without any mention of a reserved right to bid. The owner secretly asks his cousin to bid to push up the price. Priya, the highest genuine bidder, buys the car at ₹14,00,000 after bidding against the cousin. She later discovers the arrangement. What are her rights?',
         'solution': [legal('Section 64(4): unless the auction was announced as one in which the seller may bid, neither the seller nor anyone engaged by him may bid, and a buyer can treat a sale made in breach of this as fraudulent. Section 64(6): sham bidding to push up the price makes the sale voidable by the buyer.',
                            'No right to bid was notified. The seller planted a bidder who bid against Priya to raise the price.',
                            'This is pretended bidding prohibited by Section 64; Priya was induced to pay more by fraud.',
                            'Priya may treat the sale as fraudulent and avoid it (recover her money), or affirm it and claim damages for the loss caused.')]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Customer goes into insolvency — what can we hold back?', 'role': 'CA in industry, head of credit control at a steel distributor',
         'situation': 'A large customer has been admitted into insolvency proceedings. Three of your consignments to it are: one in your yard (invoiced, unpaid), one on a truck en route, and one delivered last week.',
         'steps': ['Yard consignment: exercise lien under Section 47 — insolvency of the buyer allows lien even if credit had been allowed.',
                   'Truck consignment: give immediate notice of stoppage in transit to the transporter (Sections 50–52) before the customer takes delivery.',
                   'Delivered consignment: lien and stoppage are lost; lodge a claim for the price with the insolvency professional.',
                   'Send notice of intention to resell the retained goods if not paid within a reasonable time (Section 54(2)), so that any shortfall can be claimed.'],
         'takeaway': 'Location of the goods decides the remedy — act fast while the goods are still in your or the carrier\'s hands.',
         'think': 'The customer had already sold the truck consignment to a sub-buyer by endorsing the lorry receipt to him for value in good faith. Can you still stop it?',
         'answer': 'If a document of title was lawfully transferred to the customer and he transferred it by way of sale to a good-faith buyer for value, Section 53 defeats the stoppage. Otherwise the sub-sale does not affect your right unless you assented to it.'},
        {'id': 'j2', 'title': 'GST rate change between order and invoice', 'role': 'Tax and accounts manager of an FMCG company',
         'situation': 'Orders worth ₹2.4 crore were accepted at prices "plus GST at 12%". The rate becomes 18% before dispatch.',
         'steps': ['Check whether the contracts are tax-inclusive or fix the tax at 12% "in all cases". If silent or "plus applicable GST", Section 64A allows the increase to be passed on.',
                   'Compute the increase: 6% of ₹2.4 crore = ₹14.4 lakh, and inform customers before invoicing.',
                   'For any contract with an express fixed-tax clause, the company bears the increase — flag the margin impact to management.'],
         'takeaway': 'Unless the contract says otherwise, the buyer bears a tax increase and gets the benefit of a decrease.',
         'checks': [{'expr': '24000000*6/100', 'value': 1440000, 'label': 'increase passed on: 6% of 2.4 crore'}]},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'A seller who has received a cheque for the full price which is later dishonoured is:', 'options': ['An unpaid seller', 'Not an unpaid seller as he received full payment', 'An unpaid seller only if the buyer is insolvent', 'A secured creditor'], 'answer': 0,
         'explain': 'Section 45(1)(b): a seller who receives a bill of exchange or other negotiable instrument as conditional payment becomes an unpaid seller again if it is dishonoured. A cheque is only conditional payment, so when it bounces the seller is unpaid. "Not unpaid, as he received full payment" is the trap: a cheque counts as payment only if it is honoured. The buyer\'s insolvency is not required. In practice: when a customer\'s cheque bounces, the seller can hold back undelivered goods and may also start Section 138 proceedings under the Negotiable Instruments Act.', 'topic': 'Unpaid Seller', 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'Which is NOT a right of the unpaid seller against the goods?', 'options': ['Suit for price', 'Lien', 'Stoppage in transit', 'Resale'], 'answer': 0,
         'explain': "Section 46 gives the unpaid seller three rights against the goods: lien, stoppage in transit and resale. A suit for the price (Section 55) is a right against the buyer personally, not against the goods. Resale is the trap: students think of it as a remedy against the buyer, but it is exercised on the goods themselves under Section 54. In practice: a CA advising a supplier facing a defaulting customer first lists which goods are still in the supplier's hands or in transit, because those can be held or resold.", 'topic': 'Rights of an Unpaid Seller', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm3', 'q': 'An unpaid seller can exercise lien where:', 'options': ['Goods are sold on credit and the buyer becomes insolvent during the credit period', 'Goods are sold on credit and the credit period has not expired, buyer solvent', 'Goods have been delivered to the buyer', 'Goods have been handed to a carrier without reserving the right of disposal'], 'answer': 0,
         'explain': 'Section 47(1): an unpaid seller in possession has a lien where the goods were sold without credit, where the credit period has expired, or where the buyer becomes insolvent. Insolvency during the credit period revives the lien even though credit has not run out. "Credit not expired and buyer solvent" is the trap: the seller has agreed to wait, so he must deliver. Delivery to the buyer, or to a carrier without reserving disposal, ends the lien (Section 49). In practice: a distributor stops releasing stock as soon as it learns that a dealer has gone into insolvency proceedings.', 'topic': 'Right of Unpaid Seller Against the Goods', 'concept': 'c3', 'difficulty': 'moderate'},
        {'id': 'm4', 'q': 'The unpaid seller does NOT lose his lien merely because:', 'options': ['He has obtained a decree for the price', 'He has delivered the goods to a carrier without reserving the right of disposal', 'The buyer has lawfully obtained possession', 'He has waived it'], 'answer': 0,
         'explain': 'Section 49(2): an unpaid seller who has a lien does not lose it just because he has obtained a decree for the price. The decree is not payment, so he can keep the goods until he is actually paid. Delivery to a carrier without reserving the right of disposal is the trap: under Section 49(1) that, like the buyer lawfully getting possession or the seller waiving the lien, does end it. In practice: a supplier that wins a recovery suit still keeps the goods in its godown until the decree is actually paid.', 'topic': 'Right of Unpaid Seller Against the Goods', 'concept': 'c3', 'difficulty': 'moderate'},
        {'id': 'm5', 'q': 'The right of stoppage in transit can be exercised only when:', 'options': ['The buyer is insolvent', 'The buyer delays payment by a week', 'The seller is in possession of the goods', 'The goods have reached the buyer'], 'answer': 0,
         'explain': 'Section 50: stoppage in transit is available only when the buyer has become insolvent and the goods are still with a carrier or middleman in transit. Unlike lien, mere delay in payment is not enough. "The seller is in possession" is the trap: if the seller still has the goods, his remedy is lien, not stoppage. Once goods reach the buyer, transit has ended. In practice: an exporter who hears that the importer has gone bankrupt instructs the shipping line in writing to hold the cargo.', 'topic': 'Right of Unpaid Seller Against the Goods', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm6', 'q': 'Lien is the right to ___ possession; stoppage in transit is the right to ___ possession.', 'options': ['Retain; regain', 'Regain; retain', 'Transfer; retain', 'Retain; transfer'], 'answer': 0,
         'explain': 'Lien is the right to retain (keep) possession of goods the seller still holds. Stoppage in transit is the right to regain (get back) possession of goods already handed to a carrier but not yet received by the buyer. "Regain; retain" is the trap, simply putting the two the wrong way round. Neither right lets the seller transfer possession to a third party; that needs resale. In practice: lien is used by a seller still holding stock in its warehouse, and stoppage when the truck is on the highway.', 'topic': 'Right of Unpaid Seller Against the Goods', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm7', 'q': 'An unpaid seller resells goods WITHOUT giving notice to the buyer (goods not perishable) and makes a loss. He:', 'options': ['Cannot recover the loss from the original buyer', 'Can recover the loss in full', 'Can recover half the loss', 'Commits a criminal offence'], 'answer': 0,
         'explain': 'Under Section 54(2), an unpaid seller who resells after giving notice of his intention can recover any loss from the original buyer; the same applies for perishable goods. If he resells non-perishable goods without notice, he cannot recover the loss (and per the study material the buyer may claim any profit). "Recover the loss in full" is the trap: without notice, the loss stays with the seller. Resale is not a criminal offence. In practice: a supplier always sends a written resale notice by registered post or email before disposing of the goods.', 'topic': 'Right of Unpaid Seller Against the Goods', 'concept': 'c5', 'difficulty': 'moderate'},
        {'id': 'm8', 'q': 'The seller may sue for the price even though property has not passed when:', 'options': ['The contract fixes a definite payment date regardless of delivery', 'The goods are unascertained', 'The buyer is solvent', 'The goods are in transit'], 'answer': 0,
         'explain': "Section 55(2): where the price is payable on a certain day regardless of delivery and the buyer fails to pay, the seller may sue for the price even though property has not passed and the goods are not appropriated. Unascertained goods are the trap: without a day-certain clause, the seller's remedy for them is damages under Section 56. The buyer's solvency and transit are irrelevant. In practice: advance-payment clauses in supply contracts let the seller sue for the full price, not just damages, if the buyer misses the date.", 'topic': 'Rights of Unpaid Seller Against the Buyer (Sections 55-61)', 'concept': 'c6', 'difficulty': 'moderate'},
        {'id': 'm9', 'q': 'A buyer wrongfully refuses 100 units contracted at ₹900; market price on the due date is ₹820. The seller\'s damages are:', 'options': ['₹8,000', '₹90,000', '₹82,000', '₹17,200'], 'answer': 0,
         'explain': 'Section 56, read with Section 73 of the Contract Act, gives damages for non-acceptance: the loss is the contract price minus the market price on the due date. (₹900 − ₹820) × 100 units = ₹80 × 100 = ₹8,000. ₹90,000 is the trap: it is the full contract price, which is recoverable only in a suit for the price, not as damages. ₹82,000 is the market value of the goods. In practice: a CA quantifies such a claim using market quotations or exchange prices on the delivery date as evidence.', 'topic': 'Rights of Unpaid Seller Against the Buyer (Sections 55-61)', 'concept': 'c6', 'difficulty': 'core', 'check': '(900-820)*100'},
        {'id': 'm10', 'q': 'Specific performance under Section 58 is ordinarily granted for:', 'options': ['Specific or ascertained goods of a unique nature where damages are inadequate', 'Any unascertained goods', 'Goods freely available in the market', 'Future goods by description'], 'answer': 0,
         'explain': 'Section 58 (read with the Specific Relief Act) lets the court order specific performance for specific or ascertained goods, usually where they are unique and money damages would not be adequate. Goods freely available in the market are the trap: there the buyer can simply buy elsewhere and claim the extra cost. Unascertained or future goods are not identified, so the court cannot order them delivered. In practice: buyers of rare artworks, antiques or custom-built machinery ask for specific performance, while buyers of steel or cement claim damages.', 'topic': 'Remedies of Buyer Against the Seller', 'concept': 'c7', 'difficulty': 'core'},
        {'id': 'm11', 'q': 'At an auction, a bidder may withdraw his bid:', 'options': ['Any time before the fall of the hammer', 'Never once made', 'Only with the auctioneer\'s consent', 'Within 24 hours after the hammer falls'], 'answer': 0,
         'explain': 'Section 64(2): an auction sale is complete when the auctioneer announces it, for example by the fall of the hammer. Until then any bidder may withdraw his bid, because a bid is only an offer. "Never once made" is the trap: an offer can be revoked before acceptance, and here acceptance is the fall of the hammer. There is no 24-hour window after the sale. In practice: at a tea auction in Kolkata or a used-vehicle auction, a bidder can call back his bid until the auctioneer knocks the lot down; after that he is bound.', 'topic': 'Remedies of Buyer Against the Seller', 'concept': 'c8', 'difficulty': 'core'},
        {'id': 'm12', 'q': 'Goods contracted at ₹5,00,000 plus GST at 5%. Before delivery the rate is raised to 12%; the contract is silent. The buyer must pay in all:', 'options': ['₹5,60,000', '₹5,25,000', '₹5,35,000', '₹5,00,000'], 'answer': 0,
         'explain': 'Section 64A: unless the contract says otherwise, if a tax on the goods is newly imposed or increased after the contract, the seller may add the increase to the price; if reduced, the buyer may deduct it. GST at the new 12% applies: ₹5,00,000 + 12% = ₹5,60,000. ₹5,25,000 is the trap: it uses the old 5% rate, ignoring Section 64A. In practice: when GST rates change mid-contract, suppliers revise the tax on invoices for undelivered goods, and contracts often state that the rate on the invoice date applies.', 'topic': 'Inclusion of Increased or Decreased Taxes in Contract of Sale (Section 64A)', 'concept': 'c8', 'difficulty': 'moderate', 'check': '500000*112/100'},
    ]

    questions = [
        {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'core', 'pad': 'text',
         'q': 'Who is an unpaid seller? Briefly explain the rights of an unpaid seller against the goods.',
         'model': [p('Section 45: a seller is an unpaid seller when the whole price has not been paid or tendered and he has an immediate right of action for it, or when a bill of exchange or other negotiable instrument taken as conditional payment has been dishonoured. "Seller" includes anyone in the position of a seller, such as an agent to whom the bill of lading is endorsed.'),
                   p('Rights against the goods (Section 46):'),
                   ul(['Lien (Sections 47–49): retain goods in his possession until paid — on a cash sale, on expiry of credit, or on the buyer\'s insolvency; lost on delivery to a carrier without reserving disposal, on the buyer lawfully getting possession, or on waiver.',
                       'Stoppage in transit (Sections 50–52): on the buyer\'s insolvency, resume possession of goods in the hands of a carrier until the buyer takes delivery — by actual possession or notice to the carrier.',
                       'Resale (Section 54): after lien or stoppage, if goods are perishable or after notice and default; recover loss from the buyer (if notice given); new buyer gets good title.',
                       'Withholding delivery where property has not passed (Section 46(2)).'])],
         'scheme': [{'id': 's1', 'pt': 'Definition — Section 45, both limbs', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's2', 'pt': 'Lien — when available and when lost', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's3', 'pt': 'Stoppage in transit — conditions and mode', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's4', 'pt': 'Resale and withholding delivery', 'm': 1.5, 'skill': 'provision'}],
         'remarks': ['Many answers mix up rights against the goods with suits against the buyer; keep them separate.'],
         'mistakes': ['Saying stoppage in transit is available whenever the buyer delays payment.', 'Omitting the dishonoured-instrument limb of the definition.'],
         'tips': ['Use the headings Lien / Stoppage / Resale and cite sections.']},
        {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'legal',
         'q': f'Sharma sells 200 tins of ghee to Varun at ₹4,800 per tin, the price payable on delivery. Varun does not pay or take delivery. Ghee being perishable, Sharma resells the tins after a week at ₹4,500 per tin, without notice to Varun. Can Sharma recover the loss from Varun? Compute the amount.',
         'model': [legal('Section 54(2): an unpaid seller who has exercised his lien may resell the goods where they are of a perishable nature, or after notice and the buyer\'s failure to pay within a reasonable time; on resale he may recover from the original buyer damages for loss occasioned by the breach.',
                         'Sharma held the ghee under lien (cash sale, unpaid). Ghee is perishable. He resold without notice at ₹4,500 against the contract rate of ₹4,800.',
                         'For perishable goods, notice is not required before resale, so Sharma\'s right to recover the loss is not affected by the absence of notice.',
                         f'Sharma can recover the loss of {R(c.add("200*(4800-4500)", "loss on resale of 200 tins"))} from Varun.')],
         'scheme': [{'id': 's1', 'pt': 'Section 54(2) — resale of perishable goods / after notice', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's2', 'pt': 'Analysis — perishable, notice not needed', 'm': 1, 'skill': 'analysis'},
                    {'id': 's3', 'pt': 'Computation 200 × 300', 'm': 1, 'skill': 'computation'},
                    {'id': 's4', 'pt': 'Conclusion', 'm': 0.5, 'skill': 'conclusion'}],
         'remarks': ['The perishable nature of the goods is the key fact — candidates who ignore it wrongly deny recovery for want of notice.'],
         'mistakes': ['Computing on the resale price instead of the difference.'],
         'tips': ['Show the computation separately in one line.'],
         'checks': [c[-1]]},
        {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'Distinguish between the right of lien and the right of stoppage in transit. When does the transit come to an end?',
         'model': [table(['Basis', 'Lien', 'Stoppage in transit'], [
             ['Nature', 'Right to retain possession', 'Right to regain possession'],
             ['Possession', 'Seller in possession', 'Seller has parted with possession to a carrier/bailee'],
             ['Insolvency of buyer', 'Not essential', 'Essential'],
             ['Commencement and end', 'Ends when goods leave seller\'s possession', 'Begins when lien ends; ends when buyer takes delivery'],
         ]),
                   p('Transit ends (Section 51) when:'),
                   ul(['the buyer or his agent takes delivery from the carrier at the destination;', 'the buyer or his agent obtains delivery before the goods reach the destination;',
                       'after arrival, the carrier tells the buyer that he is now holding the goods for him;', 'the carrier wrongfully refuses to deliver to the buyer;',
                       'the goods are loaded on a vessel chartered by the buyer whose master acts as the buyer\'s agent;', 'part delivery is made showing an agreement to give up possession of the whole.'])],
         'scheme': [{'id': 's1', 'pt': 'Four distinctions (0.75 each)', 'm': 3, 'skill': 'concept'},
                    {'id': 's2', 'pt': 'End of transit — any four situations (0.75 each)', 'm': 3, 'skill': 'provision'}],
         'remarks': ['A neat table and a numbered list for Section 51 earn full marks.'],
         'mistakes': ['Saying transit ends when goods reach the destination city even though the carrier still holds them.'],
         'tips': ['Lien = retain; stoppage = regain — make it your first row.']},
        {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'legal',
         'q': 'Ritu agrees to buy from Kunal a rare first-edition manuscript for ₹6,00,000. Before delivery Kunal finds another buyer willing to pay more and refuses to deliver to Ritu. Ritu does not want money — she wants the manuscript. Advise Ritu.',
         'model': [legal('Section 58: in a suit for breach of contract to deliver specific or ascertained goods, the court may direct that the contract be performed specifically, subject to the Specific Relief Act, 1963 — typically where damages would not be an adequate remedy because the goods are unique.',
                         'The manuscript is a specific, rare article. Kunal refused to deliver. Ritu wants the goods, not compensation.',
                         'Money cannot buy Ritu an identical manuscript in the market, so damages are inadequate. The goods are specific. These are the classic grounds for specific performance.',
                         'Ritu may sue for specific performance and the court may order Kunal to deliver the manuscript on payment of ₹6,00,000. Alternatively she may claim damages under Section 57.')],
         'scheme': [{'id': 's1', 'pt': 'Section 58 and Specific Relief Act condition', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's2', 'pt': 'Analysis — unique goods, damages inadequate', 'm': 1.5, 'skill': 'analysis'},
                    {'id': 's3', 'pt': 'Conclusion — specific performance / damages as alternative', 'm': 1, 'skill': 'conclusion'}],
         'remarks': ['Good answers explain why damages are inadequate.'], 'mistakes': ['Offering only damages for non-delivery.'],
         'tips': ['Mention that specific performance is discretionary.']},
    ]

    viva = [
        V('v1', 'Who is an unpaid seller under Section 45?',
          'A seller is unpaid when some or all of the price remains unpaid, with no tender made, and he has an immediate right to sue for it; or when a bill of exchange or other negotiable instrument received as conditional payment has been dishonoured.',
          [P('p1', 'Whole price not paid or tendered', 4, 'whole price|full price|entire price|price not paid|price unpaid|price remains unpaid|price outstanding|not been paid|part of price|not paid|not tendered|partly paid|part payment', min=1),
           P('p2', 'Immediate right of action for the price', 2, 'immediate|right of action|due|credit expired|credit period expired', min=1),
           P('p3', 'Negotiable instrument taken as conditional payment dishonoured', 4, 'cheque|bill of exchange|negotiable instrument|bill|instrument', 'dishonour|bounce|returned|not honour|not paid', min=2)], 'c1'),
        V('v2', 'When can an unpaid seller exercise his right of lien, and when does he lose it?',
          'He can exercise lien while in possession when the goods are sold without credit, when the credit period has expired, or when the buyer becomes insolvent. He loses it when he delivers the goods to a carrier without reserving the right of disposal, when the buyer lawfully obtains possession, or when he waives the lien.',
          [P('p1', 'Available: no credit / credit expired / buyer insolvent', 5, 'without credit|no credit|cash sale|cash', 'credit expired|credit period expired|credit period is over|credit over|term of credit expired|expiry of credit', 'insolvent|insolvency|bankrupt', min=2),
           P('p2', 'Lost: delivery to carrier without reserving disposal / buyer gets possession / waiver', 5, 'carrier|transporter|bailee', 'buyer obtains possession|buyer gets possession|buyer lawfully|buyer takes possession|possession to buyer|buyer gets the goods|buyer obtains the goods|lawfully obtains', 'waive|waiver|gives up|give up', min=2)], 'c3'),
        V('v3', 'What are the conditions for exercising the right of stoppage in transit?',
          'The seller must be unpaid, he must have parted with possession of the goods, the goods must be in the course of transit with a carrier, and the buyer must have become insolvent.',
          [P('p1', 'Seller is unpaid', 2, 'unpaid|not paid|not been paid'),
           P('p2', 'Seller has parted with possession', 2, 'parted|part with|handed|delivered to carrier|given to carrier|no longer in possession|lost possession|not in possession'),
           P('p3', 'Goods are in transit', 3, 'transit|on the way|in course of transit|with the carrier|with carrier|carrier'),
           P('p4', 'Buyer is insolvent', 3, 'insolvent|insolvency|bankrupt')], 'c4'),
        V('v4', 'When can an unpaid seller resell the goods, and what happens to the loss on resale?',
          'After exercising lien or stoppage in transit, he can resell if the goods are perishable, or if he gives notice of his intention to resell and the buyer does not pay within a reasonable time, or if the contract expressly reserves a right of resale. If he resells after notice, he can recover the loss from the original buyer; without notice he cannot recover the loss. The new buyer gets a good title.',
          [P('p1', 'Perishable goods', 2, 'perishable|perish'),
           P('p2', 'After notice and buyer\'s failure to pay within a reasonable time', 3, 'notice|inform|intimat', 'reasonable time|fails to pay|does not pay|not pay|default|still unpaid', min=2),
           P('p3', 'Loss recoverable only if notice given', 3, ALT('{l} notice', '{l} after notice', '{l} if notice', 'notice {l}', 'without notice cannot recover', 'no notice cannot recover', 'without notice no recovery', l=('recover loss', 'recover the loss', 'claim loss', 'claim the loss', 'recover shortfall', 'claim shortfall', 'recover difference', 'claim difference'))),
           P('p4', 'New buyer gets good title / express reservation of resale', 2, 'good title|valid title|new buyer|second buyer|subsequent buyer|expressly reserved|reserved right|reserves', min=1)], 'c5'),
        V('v5', 'What does Section 64A provide about changes in taxes after a contract of sale?',
          'If, after the contract is made but before it is performed, a tax or duty on the goods is imposed, increased, decreased or remitted, then unless the contract says otherwise, the seller may add the increase to the price and the buyer may deduct the decrease.',
          [P('p1', 'Change after the contract but before performance', 2, 'after contract|after the contract|before performance|before delivery|before it is performed|between contract', min=1),
           P('p2', 'Seller may add an increase to the price', 4, ALT('seller {a} {i}', 'seller {a} the {i}', '{i} added', '{i} borne buyer', '{i} paid buyer', 'buyer pay {i}', 'buyer bears {i}', a=('add', 'adds', 'can add', 'pass on', 'charge', 'recover'), i=('increase', 'increased tax', 'higher tax', 'extra tax', 'new tax', 'tax increase'))),
           P('p3', 'Buyer may deduct a decrease', 2, ALT('buyer {d} {r}', 'buyer {d} the {r}', '{r} benefit buyer', '{r} passed buyer', 'buyer gets {r}', 'buyer get benefit', 'buyer gets benefit', 'buyer benefit', d=('deduct', 'deducts', 'can deduct', 'reduce', 'pays less'), r=('decrease', 'reduction', 'lower tax', 'reduced tax', 'remission', 'decreased tax'))),
           P('p4', 'Unless the contract provides otherwise', 2, 'unless|otherwise|contrary|agreement|exclude|contract says', min=1)], 'c8'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Cement bags for Shree Builders', 'difficulty': 'hard',
        'case': (f'On 1 November, Ultra Cement agreed to sell {k_q} bags of cement to Shree Builders at {R(k_c)} per bag, delivery and payment on 15 November at Ultra\'s depot. '
                 'On 15 November, Shree Builders refused to take delivery or pay, saying it no longer needed the cement. The market price that day was ₹1,105 per bag. '
                 'Ultra kept the bags and sent Shree Builders a written notice that it would resell them if not paid within 10 days. Shree did not respond.'),
        'mcqs': [
            dict(M('k1a', 'On 15 November, Ultra Cement is:', ['An unpaid seller in possession, entitled to a lien', 'Not an unpaid seller as no credit was given', 'Entitled only to stoppage in transit', 'Bound to deliver the goods to Shree\'s site'], 0,
              'Under Section 45, Ultra is an unpaid seller: the whole price was due on 15 November and has not been paid. It still holds the goods, and the sale was without credit, so Section 47(1)(a) gives it a lien. "Not an unpaid seller as no credit was given" is the trap: a cash sale makes the right of lien stronger, not weaker. Stoppage in transit needs goods in transit, which these are not. In practice: a cement company simply refuses to load the trucks until payment is received.', 'moderate'), topic='Unpaid Seller'),
            dict(M('k1b', 'If Ultra sues for damages for non-acceptance on the basis of the market price on 15 November, it can claim:', [R(k_dmg), '₹6,20,000', '₹5,52,500', '₹1,35,000'], 0,
              "Section 56 damages for non-acceptance = contract price − market price on the due date, multiplied by quantity: (₹1,240 − ₹1,105) × 500 bags = ₹135 × 500 = ₹67,500. ₹6,20,000 is the trap: it is the full contract price, which damages do not give. ₹1,35,000 doubles the difference by mistake, and ₹5,52,500 is the market value of the bags. In practice: the seller's accountant supports the claim with dealer price lists or invoices for 15 November.", 'hard', '500*(1240-1105)'), topic='Rights of Unpaid Seller Against the Buyer (Sections 55-61)'),
            dict(M('k1c', 'Ultra waits the notice period and resells at ₹1,300 per bag. As per the study material, the surplus over the contract price:', ['May be retained by Ultra, as resale followed notice', 'Must be paid to Shree Builders', 'Must be shared equally', 'Goes to the government'], 0,
              'Ultra gave written notice of resale and waited, so the resale is under Section 54(2). The surplus is (₹1,300 − ₹1,240) × 500 = ₹30,000. As the study material states, a seller who resells after notice may keep any profit, while one who resells without notice must account for it to the buyer. "Must be paid to Shree Builders" is the trap: that applies to resale without notice. In practice: suppliers keep proof of the notice and the resale invoices on file, in case the original buyer later disputes the account.', 'hard'), topic='Right of Unpaid Seller Against the Goods'),
            dict(M('k1d', 'Who gets title to the bags on Ultra\'s resale to a new buyer?', ['The new buyer, as against Shree Builders', 'Shree Builders, as the original buyer', 'No one until Shree consents', 'Ultra retains title'], 0,
              'Section 54(3): when an unpaid seller who has exercised his lien resells the goods, the new buyer gets good title as against the original buyer, even if no notice of resale was given. So the new buyer owns the bags. "Shree Builders, as the original buyer" is the trap: Shree\'s rights were cut off by its default and the lawful resale. Shree\'s consent is not needed. In practice: the second buyer of the cement can use it freely without fearing a claim from Shree Builders.', 'moderate'), topic='Right of Unpaid Seller Against the Goods'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch03', 'n': 4, 'title': 'Unpaid Seller',
        'outcomes': ['Identify an unpaid seller under Section 45 and list his rights under Section 46.',
                     'Explain and apply the rights against the goods — lien, stoppage in transit and resale (Sections 47 to 54), including the effect of sub-sale or pledge.',
                     'Explain the seller\'s suits against the buyer and the buyer\'s remedies against the seller (Sections 55 to 61), and compute damages.',
                     'State the rules of auction sales (Section 64) and the effect of tax changes on the contract price (Section 64A).'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 55, 'practice': 55}, 'prereq': ['fnd-p2-ch03-u03'],
                 'exam_tip': 'Expect a problem on lien/stoppage/resale or on auction rules, and a theory question on rights of an unpaid seller. Locate the goods first — with the seller, with a carrier, or with the buyer.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Unpaid seller (45): whole price not paid/tendered with immediate right of action, or conditional instrument dishonoured.',
                        'Against goods (46): lien (47–49), stoppage in transit on insolvency (50–52), resale (54); withholding delivery if property not passed.',
                        'Lien: no credit / credit expired / insolvency; lost by delivery to carrier without reservation, buyer lawfully getting possession, waiver — not by decree for price.',
                        'Transit: from delivery to carrier until buyer/agent takes delivery; ends early on interception, attornment, wrongful refusal by carrier, buyer\'s chartered ship.',
                        'Resale: perishable or after notice; with notice — recover loss (and keep surplus as per the study material); without notice — no loss recovery; new buyer gets good title.',
                        'Against buyer: suit for price (55), damages for non-acceptance (56), anticipatory breach (60), interest (61). Buyer\'s remedies: non-delivery (57), specific performance (58), breach of warranty (59), 60, 61.',
                        'Auction (64): lot = separate contract; complete on fall of hammer; seller\'s bidding only if notified; reserve price; pretended bidding → voidable. Section 64A: tax increase added, decrease deducted unless contract excludes.'],
            'remember': ['Lien = retain; stoppage = regain.', 'Damages for non-acceptance = contract price − market price; for non-delivery = market price − contract price (on the due date).'],
            'traps': ['Stoppage needs the buyer\'s insolvency; lien does not.', 'Stoppage does not rescind the contract.', 'A buyer\'s sub-sale does not defeat lien/stoppage unless the seller assented or a document of title was transferred to a good-faith buyer for value.',
                      'Section 64A can be excluded by the contract.']},
        'quickref': [{'k': 'Section 45', 'v': 'Unpaid seller: price unpaid with immediate right of action, or instrument dishonoured'},
                     {'k': 'Section 46', 'v': 'Lien · stoppage in transit · resale · withholding delivery'},
                     {'k': 'Sections 47–49', 'v': 'Lien: cash sale / credit expired / insolvency; lost by carrier delivery, buyer\'s possession, waiver'},
                     {'k': 'Sections 50–52', 'v': 'Stoppage in transit on insolvency; duration of transit; by possession or notice'},
                     {'k': 'Section 53', 'v': 'Sub-sale/pledge does not affect rights unless assent or document of title to bona fide buyer'},
                     {'k': 'Section 54', 'v': 'Resale: perishable or after notice; new buyer gets good title'},
                     {'k': 'Sections 55–56', 'v': 'Suit for price · damages for non-acceptance'},
                     {'k': 'Sections 57–59', 'v': 'Non-delivery damages · specific performance · breach of warranty'},
                     {'k': 'Sections 60–61', 'v': 'Anticipatory breach · interest and special damages'},
                     {'k': 'Section 64 / 64A', 'v': 'Auction rules · tax changes after contract adjust the price'}],
        'viva': viva, 'cases': cases,
    }
