"""CA Foundation · Paper 2 Business Laws · Chapter 3 The Sale of Goods Act, 1930 · Unit 2 Conditions & Warranties.
Original explanations, facts and questions; sections and well-known cases are cited by name only."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p2-ch03-u02'


def build():
    c = Checks()
    # i1 — marine paint: refund + incidental loss
    drums, rate = 40, 3250
    paid = c.add('40*3250', 'price paid for 40 drums at 3,250')
    redo = c.add('62000', 'cost of scraping and repainting the hull')
    claim = c.add('40*3250+62000', 'refund of price + damages for repainting')
    # i5 — non-severable contract accepted: damages only (s13(2))
    q_tonnes, r_grade_a, r_grade_b = 25, 41000, 37500
    dmg = c.add('25*(41000-37500)', 'damages = 25 t × (grade A price − grade B value)')
    # case — tiles
    boxes, box_rate = 600, 1150
    k_price = c.add('600*1150', 'price of 600 boxes of tiles')
    k_dmg = c.add('600*(1150-900)', 'damages if buyer keeps the tiles: value difference 250 per box')

    cw_table = table(['Basis', 'Condition', 'Warranty'], [
        ['Meaning (Section 12)', 'A term vital to the main object of the contract', 'A stipulation collateral (subsidiary) to the main purpose'],
        ['Importance', 'Goes to the root of the contract', 'Of secondary importance'],
        ['Remedy on breach', 'Repudiate (reject the goods) and also claim damages', 'Damages only — cannot reject the goods (Section 59)'],
        ['Conversion', 'A breach of condition may be treated as a breach of warranty (Section 13)', 'A breach of warranty can never be treated as a breach of condition'],
    ], title='Condition vs warranty')

    implied = table(['Implied term', 'Section', 'Condition or warranty', 'In one line'], [
        ['Title — seller has the right to sell', '14(a)', 'Condition', 'In a sale: he has the right now; in an agreement to sell: he will have it when property is to pass'],
        ['Quiet possession', '14(b)', 'Warranty', 'Buyer will enjoy the goods undisturbed'],
        ['No undisclosed charge or encumbrance', '14(c)', 'Warranty', 'Goods free from any charge in favour of a third party not known to the buyer'],
        ['Correspondence with description', '15', 'Condition', 'Goods must match the description; in sale by sample and description, both'],
        ['Fitness for a particular purpose', '16(1)', 'Condition', 'Purpose made known, buyer relies on seller\'s skill, seller deals in such goods'],
        ['Merchantable quality', '16(2)', 'Condition', 'Goods bought by description from a dealer must be saleable under that description'],
        ['Fitness by usage of trade', '16(3)', 'Condition or warranty', 'Annexed by trade usage'],
        ['Sale by sample', '17', 'Condition', 'Bulk = sample; chance to compare; no hidden defect making goods unmerchantable'],
        ['Wholesomeness of eatables', '16(2) (judicial)', 'Condition', 'Food and provisions must be fit for consumption'],
    ], title='Implied conditions and warranties at a glance')

    concepts = [
        {'id': 'c1', 'title': 'Stipulation as to time (Section 11)', 'body': [
            'A stipulation is a term of the contract. Section 11: unless the contract shows a different intention, a term about the time of payment of the price is not treated as of the essence of a contract of sale. So late payment alone does not let the seller cancel; he can claim interest or damages and use his unpaid-seller rights.',
            'Whether any other time term — usually the time of delivery — is of the essence depends on the terms of the contract. In commercial contracts, the delivery date is normally treated as essential, especially for seasonal or price-sensitive goods.'],
         'analogy': 'Paying a few days late is like arriving late to dinner — annoying but the dinner goes on. Delivering diwali crackers after Diwali is like arriving after the dinner is over — the whole purpose is lost.',
         'work': 'While reviewing supply contracts, a CA checks whether the delivery date is expressly "of the essence"; it decides whether the client can cancel a late order or only claim damages.'},
        {'id': 'c2', 'title': 'Condition and warranty (Section 12)', 'body': [
            'Section 12(1): a term of a sale contract that relates to the goods is either a condition or a warranty.',
            'Condition (Section 12(2)): a stipulation so essential to the main purpose of the contract that its breach gives the buyer a right to treat the contract as repudiated.',
            'Warranty (Section 12(3)): a term that is only collateral (side-line) to the main object; if it is broken the buyer can claim damages but cannot throw back the goods or end the contract.',
            'Section 12(4): whether a stipulation is a condition or a warranty depends on the construction of the contract in each case — the label used by the parties is not conclusive.'],
         'blocks': [cw_table],
         'analogy': 'In a car purchase, "the car has a working engine" is a condition — without it there is no car worth buying. "It comes with free floor mats" is a warranty — if missing, you claim the cost of mats, you do not return the car.',
         'work': 'When a customer rejects a consignment, the finance team must know whether the breach was of a condition (rejection allowed — reverse the sale) or a warranty (sale stands — only a price reduction or damages).'},
        {'id': 'c3', 'title': 'When a condition is treated as a warranty (Section 13)', 'body': [
            'A breach of condition is "downgraded" to a breach of warranty — the buyer loses the right to reject and can claim only damages — in these cases:',
            '(a) Voluntary waiver: the buyer gives up the condition altogether.',
            '(b) Election: the buyer chooses to treat the breach of condition as a breach of warranty — keeps the goods and claims damages.',
            '(c) Non-severable contract and acceptance: where the contract cannot be split and the buyer has accepted the goods or part of them, he can no longer reject, unless the contract says otherwise.',
            '(d) Excused by law: where performance of the condition is excused by law because of impossibility or otherwise.',
            'The first two are voluntary on the buyer\'s part; the last two are compulsory — they happen by operation of law.'],
         'analogy': 'A red-card offence (condition) can be let off with a yellow card (warranty) — by the referee\'s choice or the rules — but a yellow card is never upgraded to a red card later.',
         'work': 'Clients often keep and use defective goods while "disputing" them. A CA advises that use or acceptance under a non-severable contract usually leaves only a damages claim — so the dispute should be raised before acceptance.'},
        {'id': 'c4', 'title': 'Implied conditions (Sections 14 to 17)', 'body': [
            'Implied terms are read into every contract of sale by law unless the parties agree otherwise. Express terms are those the parties actually state.',
            'Title — Section 14(a): in a sale, the seller has the right to sell; in an agreement to sell, he will have the right when property is to pass. If he has no title, the buyer can recover the full price even after using the goods (Rowland v. Divall — a stolen car).',
            'Description — Section 15: goods sold by description must correspond with it. If sold by sample as well as description, the bulk must match both (Varley v. Whipp — a "new, one-season-old" reaping machine that turned out to be very old).',
            'Fitness for purpose — Section 16(1): normally there is no implied condition of fitness, but there is one where (i) the buyer makes known, expressly or by implication, the particular purpose, (ii) in a way that shows he is depending on the seller\'s expertise, and (iii) the seller deals in that kind of goods (whether or not he is the manufacturer). There is no such condition if the buyer orders an article under its patent or trade name in a way that shows he is not relying on the seller. Where goods have only one obvious use (a hot-water bottle — Priest v. Last), the purpose is made known by implication.',
            'Merchantability — Section 16(2): when a buyer purchases by description from a dealer in such goods, the goods must be of merchantable quality — saleable under that description at the full price. If the buyer has examined the goods, there is no implied condition about defects that the examination ought to have revealed.',
            'Wholesomeness: for food and provisions, a further condition that they are fit for human consumption (Frost v. Aylesbury Dairy — milk carrying typhoid germs).',
            'Sale by sample — Section 17: the bulk must correspond with the sample in quality; the buyer must have a reasonable opportunity to compare the bulk with the sample; and the goods must be free from any defect making them unmerchantable that would not be apparent on a reasonable examination of the sample.',
            'Usage of trade — Section 16(3): an implied condition or warranty about quality or fitness may be attached by the usage of trade.'],
         'blocks': [implied],
         'analogy': 'Implied conditions are the fine print the law writes for you — the shopkeeper does not have to say "this milk is drinkable" for the law to insist it is.',
         'work': 'Product-liability and warranty-claim provisions in a manufacturer\'s books depend on these implied terms; a CA estimating the provision must know what the law presumes the seller promised.'},
        {'id': 'c5', 'title': 'Implied warranties', 'body': [
            'Quiet possession — Section 14(b): the buyer shall have and enjoy undisturbed possession of the goods. If a third party with a better right disturbs him, he may claim damages from the seller.',
            'Freedom from encumbrance — Section 14(c): the goods are free from any charge or encumbrance in favour of a third party which was not declared or known to the buyer when the contract was made. If the buyer has to pay off such a charge, he recovers it from the seller.',
            'Usage of trade — Section 16(3): a warranty about quality or fitness may be annexed by trade usage.',
            'In addition, where goods are dangerous and the buyer is unaware of the danger, the seller is under a duty to warn; failure to warn makes him liable in damages (implied warranty recognised by courts).',
            'Remedy for breach of warranty — Section 59: the buyer cannot reject the goods but may set up the breach to reduce or extinguish the price, or sue for damages.'],
         'analogy': 'A warranty is a promise on the side of the main deal — breaking it gets you compensation, not your money back.',
         'work': 'In asset purchases, due-diligence teams check registers of charges; an undisclosed bank charge on machinery is a breach of the Section 14(c) warranty and a ground for a price adjustment.'},
        {'id': 'c6', 'title': 'Caveat emptor — "let the buyer beware" (Section 16)', 'body': [
            'Section 16 opens with the rule that, subject to the Act and any other law, there is no implied condition about the quality or fitness of goods for any particular purpose. The buyer must examine the goods and judge for himself; if he makes a bad choice, he bears the loss. The seller, of course, must not actively hide defects or mislead.',
            'Exceptions — the rule does not apply: (1) fitness for purpose where the buyer relied on the seller\'s skill [16(1)]; (2) merchantable quality in a sale by description from a dealer [16(2)]; (3) quality or fitness annexed by trade usage [16(3)]; (4) sale by description — goods must match [15]; (5) sale by sample — bulk must match sample and be free from hidden defects [17]; (6) sale by sample and description [15]; (7) where the seller obtains the buyer\'s consent by fraud or actively conceals a defect; (8) food and provisions — wholesomeness. The ICAI list also includes goods bought under a patent or brand name: strictly, that is the case where exception (1) does not apply, because the buyer relies on the brand rather than on the seller — mention it in that sense.'],
         'analogy': 'At a flea market you test the gadget yourself — caveat emptor. At a specialist store you tell the expert exactly what you need and rely on him — the exception kicks in.',
         'work': 'CAs advising on purchase of second-hand plant insist on inspection and written specifications precisely because caveat emptor puts the risk of a poor choice on the buyer.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Paint that fails at sea: fitness for purpose', 'difficulty': 'moderate', 'minutes': 8,
         'q': f'Coastal Boats writes to Sagar Paints, a dealer in industrial coatings: "We need an anti-corrosion paint for the hulls of our fishing trawlers, which stay in salt water for weeks. Please supply what you recommend." Sagar Paints supplies {drums} drums of its "ProCoat" at {R(rate)} a drum. Within a month the paint peels off under salt water. Re-scraping and repainting cost {R(redo)}. Advise Coastal Boats and quantify its claim.',
         'solution': [legal('Section 16(1): the law implies a condition that the goods will be reasonably fit for the buyer\'s purpose if he discloses that purpose, depends on the seller\'s expertise, and the seller trades in goods of that kind. Section 12(2): breach of a condition entitles the buyer to treat the contract as repudiated; damages may also be claimed (Section 59 / Section 73 of the Contract Act).',
                            'Coastal Boats told the dealer the exact purpose (hulls in salt water for weeks) and asked it to recommend a product. Sagar Paints deals in industrial coatings. The paint failed for that purpose.',
                            'All three requirements of Section 16(1) are met; the patent/trade-name exception does not apply because the buyer did not choose "ProCoat" itself. Caveat emptor is excluded. There is a breach of the implied condition of fitness.',
                            f'There is a breach of condition. As the paint has already been applied to the hulls (accepted and used under a single contract), rejection is no longer practical and the breach is treated as a breach of warranty under Section 13(2); Coastal Boats can claim damages — the price of {R(paid)} paid for paint worthless for its purpose plus {R(redo)} for re-scraping and repainting, a total of {R(claim)}. (Unused drums, if any, could have been rejected before acceptance.)'),
                      table(['Item', 'Amount (₹)'], [['Damages: price paid for unfit paint (40 × ₹3,250)', inr(paid)], ['Damages: scraping and repainting', inr(redo)], ['Total claim', inr(claim)]], num=[1], total=True)],
         'checks': c[0:3]},
        {'id': 'i2', 'title': 'Bulk matches the sample, but a hidden defect', 'difficulty': 'moderate', 'minutes': 6,
         'q': 'Sonal Garments buys 2,000 metres of shirting by sample from Mehra Mills. The bulk looks exactly like the sample. After stitching, every shirt shrinks by two sizes in the first wash. A normal visual and hand check of the sample would not have revealed the shrinkage. Can Sonal Garments recover its loss?',
         'solution': [legal('Section 17(2): when goods are sold by sample, three conditions are implied — (a) the quality of the bulk matches the sample, (b) the buyer gets a fair chance to check the bulk against the sample, and (c) the goods carry no hidden defect, undiscoverable by a reasonable look at the sample, that makes them unsaleable.',
                            'The bulk matched the sample in appearance. The cloth had a shrinkage defect that made it unfit for sale as shirting, and an ordinary examination of the sample would not have revealed it.',
                            'Conditions (a) and (b) are satisfied, but condition (c) is broken: the defect was latent and made the goods unmerchantable.',
                            'Mehra Mills is in breach of an implied condition. Sonal Garments can claim damages for its loss (having already cut and stitched the cloth, it will normally be left with a damages claim under Section 13, rather than rejection).')]},
        {'id': 'i3', 'title': 'Seller without title', 'difficulty': 'core', 'minutes': 6,
         'q': 'Tarun buys a used SUV from Vinod for ₹9,00,000 and uses it for five months. Police then seize it, as it had been stolen from its true owner before Vinod got it. Vinod argues that Tarun enjoyed five months\' use and should get only part of his money back. Advise Tarun.',
         'solution': [legal('Section 14(a): every contract of sale carries an implied condition about the seller\'s title — that he is entitled to sell. Breach of a condition allows the buyer to treat the contract as repudiated and recover the price. In Rowland v. Divall the buyer of a stolen car recovered the full price despite months of use, because he never received what he paid for — ownership.',
                            'Vinod sold a stolen SUV; he had no title. Tarun used it for five months before it was seized.',
                            'The implied condition as to title was broken at the time of sale. The use Tarun had is irrelevant: the essence of a sale is transfer of ownership, which never happened.',
                            'Tarun can recover the full ₹9,00,000 from Vinod, and may also claim damages for any further loss.')]},
        {'id': 'i4', 'title': 'Caveat emptor applies', 'difficulty': 'core', 'minutes': 5,
         'q': 'Harish visits a furniture showroom, spends an hour inspecting a solid-wood dining table, chooses it himself and pays ₹38,000. He never mentions what he needs it for. At home he finds it is too tall for his dining chairs. He asks for a refund. Advise.',
         'solution': [legal('Section 16: apart from the listed exceptions, the law does not imply any promise about quality, or about suitability for the buyer\'s special purpose — the rule of caveat emptor. Section 16(1) applies only if the buyer makes known the purpose and relies on the seller\'s skill or judgment.',
                            'Harish inspected the table, chose it himself and did not disclose any special requirement. The table has no defect; it simply does not suit his chairs.',
                            'There is no reliance on the seller and no defect, so none of the exceptions applies. The buyer was expected to check the height himself.',
                            'Caveat emptor applies. Harish cannot claim a refund as of right (the showroom may still choose to exchange the table as a goodwill gesture).')]},
        {'id': 'i5', 'title': 'Accepting goods under a non-severable contract', 'difficulty': 'hard', 'minutes': 8,
         'q': f'Gupta Steels contracts to buy {q_tonnes} tonnes of grade-A steel rods at {R(r_grade_a)} per tonne, in a single delivery and a single payment. Gupta accepts the delivery and uses part of it before discovering that the rods are grade-B, worth {R(r_grade_b)} per tonne. Can Gupta reject the remaining rods? What can it claim?',
         'solution': [legal('Section 15: goods must correspond with their description — a condition. Section 13(2): where the contract is not severable and the buyer has accepted the goods or part of them, a breach of condition can be treated only as a breach of warranty, unless otherwise agreed. Section 59: for breach of warranty the buyer may claim damages or a reduction in price.',
                            'The contract was for one lot of grade-A rods (non-severable). Gupta accepted delivery and used part of it before finding the rods were grade-B.',
                            'There was a breach of the condition of description. But the contract is not severable and Gupta has accepted the goods, so the right to reject is lost; the breach is treated as a breach of warranty.',
                            f'Gupta cannot reject the remaining rods. It may claim damages (or deduct from the price) of {R(dmg)}.'),
                      wn('Damages', f'{q_tonnes} tonnes × ({R(r_grade_a)} − {R(r_grade_b)}) = {R(dmg)}')],
         'checks': c[3:4]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Customer rejects a consignment — reverse the sale?', 'role': 'Finance controller in a speciality chemicals company',
         'situation': 'A customer bought solvent "for cleaning printed circuit boards", relying on your technical team\'s recommendation. It has damaged the boards and the customer has returned the unused drums and claims losses.',
         'steps': ['Map the facts to Section 16(1): purpose made known, reliance on your team\'s advice, and you deal in such solvents — an implied condition of fitness arises.',
                   'If the condition is broken, the customer can reject and claim damages; the sale must be reversed in the books and a provision made for the damages claim.',
                   'Check the contract for any valid exclusion clause and whether the customer has accepted part of a non-severable lot (Section 13).',
                   'Brief the legal team and the auditors; disclose a contingent liability if the outcome is uncertain.'],
         'takeaway': 'Whether the term broken is a condition or a warranty decides whether revenue is reversed or merely reduced.',
         'think': 'Would it change the answer if the customer had insisted on a particular branded solvent by name, rejecting your team\'s suggestion?',
         'answer': 'Yes. Buying under a trade name in a way that shows no reliance on the seller\'s skill removes the implied condition of fitness under Section 16(1); the claim would weaken considerably.'},
        {'id': 'j2', 'title': 'Buying second-hand plant for a client', 'role': 'CA in practice advising an SME on an asset purchase',
         'situation': 'The client wants to buy a used CNC machine from a dealer, "as is where is".',
         'steps': ['Explain caveat emptor: an "as is" purchase after inspection leaves little scope for implied conditions of quality.',
                   'Ask the client to have an engineer inspect and test the machine, and to get the key specifications written into the purchase order (so Section 15 applies).',
                   'Check for charges on the machine (Section 14(c) warranty) and obtain an indemnity.'],
         'takeaway': 'Put the buyer\'s purpose and the key specifications in writing — that converts caveat emptor into enforceable conditions.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'Unless a different intention appears, a stipulation as to the time of payment in a contract of sale is:', 'options': ['Not of the essence of the contract', 'Always of the essence', 'A condition', 'Void'], 'answer': 0,
         'explain': 'Section 11: time of payment is not deemed to be of the essence unless the contract shows otherwise.', 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'A stipulation essential to the main purpose of a contract of sale is a:', 'options': ['Condition', 'Warranty', 'Guarantee', 'Representation'], 'answer': 0,
         'explain': 'Section 12(2) — breach of a condition allows the buyer to treat the contract as repudiated.', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm3', 'q': 'For breach of a warranty, the buyer can:', 'options': ['Claim damages only', 'Reject the goods and claim damages', 'Reject the goods only', 'Neither reject nor claim damages'], 'answer': 0,
         'explain': 'Section 12(3) and Section 59: damages or reduction of price, but no right to reject.', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'Which of the following is NOT a case where a breach of condition is treated as a breach of warranty?', 'options': ['The seller elects to treat it as a warranty', 'The buyer waives the condition', 'The buyer accepts goods under a non-severable contract', 'Performance of the condition is excused by law'], 'answer': 0,
         'explain': 'Under Section 13 the election belongs to the buyer, not the seller.', 'concept': 'c3', 'difficulty': 'moderate'},
        {'id': 'm5', 'q': 'The implied term about the seller\'s title (his right to sell) is:', 'options': ['A condition — Section 14(a)', 'A warranty — Section 14(b)', 'A warranty — Section 14(c)', 'Not implied at all'], 'answer': 0,
         'explain': 'Title is an implied condition; quiet possession and freedom from encumbrance are implied warranties.', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm6', 'q': 'Which is an implied WARRANTY under the Act?', 'options': ['Undisturbed (quiet) possession of the goods', 'Goods correspond with their description', 'Goods are of merchantable quality', 'Bulk corresponds with the sample'], 'answer': 0,
         'explain': 'Section 14(b). The other three are implied conditions (Sections 15, 16(2), 17).', 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm7', 'q': 'In a sale by sample, which is NOT an implied condition?', 'options': ['The goods shall be of the best quality available in the market', 'The bulk corresponds with the sample in quality', 'The buyer has a reasonable opportunity to compare bulk with sample', 'Goods are free from latent defects not apparent on reasonable examination of the sample'], 'answer': 0,
         'explain': 'Section 17(2) lists the other three. There is no promise of "best quality".', 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm8', 'q': 'The implied condition of fitness for a particular purpose does NOT arise when:', 'options': ['The buyer orders the goods under their trade name, showing no reliance on the seller', 'The buyer tells the seller the purpose', 'The seller deals in goods of that description', 'The seller is not the manufacturer'], 'answer': 0,
         'explain': 'Section 16(1) proviso (as explained in the study material): buying under a patent or trade name without reliance excludes the condition. It does not matter that the seller did not manufacture the goods.', 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm9', 'q': 'A buyer examined the goods before buying. Under Section 16(2), there is no implied condition of merchantability as regards:', 'options': ['Defects which that examination ought to have revealed', 'Any defect at all', 'Latent defects', 'Defects in title'], 'answer': 0,
         'explain': 'Only defects that the examination should have revealed are excluded; hidden defects remain covered.', 'concept': 'c4', 'difficulty': 'hard'},
        {'id': 'm10', 'q': 'The doctrine of caveat emptor means:', 'options': ['Let the buyer beware', 'Let the seller beware', 'The buyer is always protected', 'Goods must always be fit for purpose'], 'answer': 0,
         'explain': 'The buyer must use his own judgment; the seller is not answerable for quality or fitness unless an exception applies.', 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm11', 'q': 'Which situation is an exception to caveat emptor?', 'options': ['Seller obtains the buyer\'s consent by fraud', 'Buyer inspects and chooses the goods himself', 'Buyer gives no information about his purpose', 'Defect was obvious on examination'], 'answer': 0,
         'explain': 'Fraud or active concealment by the seller takes the case out of caveat emptor; the other three are classic cases where the rule applies.', 'concept': 'c6', 'difficulty': 'core'},
        {'id': 'm12', 'q': 'Milk sold by a dairy contains germs that make the buyer ill. The dairy has broken the implied condition of:', 'options': ['Wholesomeness', 'Title', 'Quiet possession', 'Correspondence with sample'], 'answer': 0,
         'explain': 'Food and provisions must be fit for human consumption (Frost v. Aylesbury Dairy).', 'concept': 'c4', 'difficulty': 'core'},
    ]

    questions = [
        {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'core', 'pad': 'text',
         'q': 'Distinguish between a condition and a warranty. State the circumstances in which a breach of condition is treated as a breach of warranty.',
         'model': [p('Section 12: a stipulation with reference to goods may be a condition or a warranty. A condition is essential to the main purpose of the contract — its breach gives the buyer a right to treat the contract as repudiated. A warranty is collateral to the main purpose — its breach gives only a claim for damages. Whether a term is one or the other depends on the construction of the contract (Section 12(4)).'),
                   table(['Basis', 'Condition', 'Warranty'], [
                       ['Importance', 'Essential to the main purpose', 'Collateral to the main purpose'],
                       ['Remedy', 'Repudiate and claim damages', 'Damages only'],
                       ['Conversion', 'May be treated as a warranty (Section 13)', 'Cannot be treated as a condition'],
                   ]),
                   p('Section 13 — a breach of condition is treated as a breach of warranty where:'),
                   ul(['the buyer waives the condition;', 'the buyer elects to treat the breach as a breach of warranty;', 'the contract cannot be split up and the buyer has already accepted all or part of the goods;', 'the law excuses performance of the condition, e.g. because it has become impossible.'])],
         'scheme': [{'id': 's1', 'pt': 'Meaning of condition and warranty (Section 12)', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's2', 'pt': 'Differences — importance, remedy, conversion', 'm': 1.5, 'skill': 'concept'},
                    {'id': 's3', 'pt': 'Waiver and election by the buyer', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's4', 'pt': 'Non-severable contract accepted; excused by law', 'm': 1.5, 'skill': 'provision'}],
         'remarks': ['Answers that state the Section 13 cases without the word "buyer" (waiver/election by whom?) lose half a mark each.', 'A short table for the distinction saves time.'],
         'mistakes': ['Saying a warranty can be treated as a condition.', 'Saying the seller can elect to treat the breach as a warranty.'],
         'tips': ['Two parts — two headings. Do not mix the distinction with the Section 13 list.']},
        {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'text',
         'q': 'Explain the doctrine of "caveat emptor". State the exceptions to it under the Sale of Goods Act, 1930.',
         'model': [p('Meaning: caveat emptor means "let the buyer beware". Section 16 lays down that, except as the Act or another law provides, the seller gives no implied promise about the quality of the goods or their suitability for the buyer\'s purpose. The buyer must examine the goods and rely on his own judgment; if they turn out unsuitable, he cannot hold the seller responsible.'),
                   p('Exceptions — the seller is responsible in the following cases:'),
                   ul(['Fitness for purpose — buyer discloses the purpose, relies on seller\'s skill, seller deals in such goods [Section 16(1)].',
                       'Merchantable quality — goods bought by description from a dealer [Section 16(2)]; if the buyer examined them, only defects the examination should have shown are excluded.',
                       'Usage of trade — condition or warranty annexed by trade usage [Section 16(3)].',
                       'Sale by description — goods must correspond with the description [Section 15].',
                       'Sale by sample — bulk to match sample; reasonable chance to compare; no latent defect [Section 17].',
                       'Sale by sample as well as description — goods must match both [Section 15].',
                       'Fraud or concealment by the seller.',
                       'Wholesomeness of food and provisions.'])],
         'scheme': [{'id': 's1', 'pt': 'Meaning with Section 16 reference', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's2', 'pt': 'Fitness for purpose and merchantability exceptions', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's3', 'pt': 'Description, sample, sample + description', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's4', 'pt': 'Trade usage, fraud, wholesomeness', 'm': 1.5, 'skill': 'provision'}],
         'remarks': ['Strong answers list at least six exceptions with section numbers.'],
         'mistakes': ['Translating caveat emptor as "let the seller beware".', 'Listing the exceptions without stating the general rule first.'],
         'tips': ['Rule first, then exceptions as a numbered list with section numbers.']},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'legal',
         'q': 'Raghav tells a hardware dealer that he needs a pump "to lift water to my third-floor tank". The dealer recommends model P-200, which Raghav buys. The pump cannot lift water beyond the first floor. In a second transaction, Kirti walks into the same shop and insists on buying "a P-200 pump, nothing else", without telling the dealer her purpose; it also fails to reach her third-floor tank. Advise Raghav and Kirti.',
         'model': [legal('Section 16(1): the condition of fitness is implied when the buyer discloses his particular purpose, depends on the seller\'s expertise, and the seller deals in such goods. There is no such condition where the buyer insists on goods under their trade name without relying on the seller. Otherwise caveat emptor applies (Section 16).',
                         'Raghav disclosed the purpose and bought the model the dealer recommended. Kirti chose the P-200 herself, by name, without disclosing her purpose. The dealer deals in pumps.',
                         'For Raghav all three requirements of Section 16(1) are met and the pump is unfit for the disclosed purpose — breach of condition. For Kirti, there was no disclosure of purpose and no reliance; she bought under the trade name, so caveat emptor applies.',
                         'Raghav may reject the pump, recover the price and claim damages. Kirti has no remedy for unfitness (unless the pump is defective as a pump, which is not the case).')],
         'scheme': [{'id': 's1', 'pt': 'Section 16(1) requirements and trade-name exclusion', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's2', 'pt': 'Application to Raghav', 'm': 1, 'skill': 'analysis'},
                    {'id': 's3', 'pt': 'Application to Kirti (caveat emptor)', 'm': 1, 'skill': 'analysis'},
                    {'id': 's4', 'pt': 'Conclusion for both', 'm': 0.5, 'skill': 'conclusion'}],
         'remarks': ['The question tests the contrast between reliance and no reliance — answers must treat the two buyers separately.'],
         'mistakes': ['Giving the same answer for both buyers.', 'Saying the dealer is not liable because he did not manufacture the pump.'],
         'tips': ['Use sub-headings "Raghav" and "Kirti" inside Analysis and Conclusion.']},
        {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'legal',
         'q': 'Mohan buys from a dealer 50 bags of "Grade-1 Sona Masoori rice" after seeing a sample. The bags delivered match the sample, but the rice is Grade-2 Sona Masoori. Can Mohan reject the goods?',
         'model': [legal('Section 15: if a sale is by both sample and description, the goods must satisfy both tests — matching the sample is not enough when they do not fit the description. Correspondence with description is an implied condition.',
                         'The rice was sold both by sample and by the description "Grade-1 Sona Masoori". The bulk matched the sample but not the description.',
                         'Matching the sample alone does not satisfy the seller\'s duty; the goods must also answer the description. Since the description (Grade-1) is not met, the implied condition is broken. Mohan has not yet accepted the goods in a way that bars rejection.',
                         'Mohan can reject the rice and recover any price paid, and may claim damages.')],
         'scheme': [{'id': 's1', 'pt': 'Section 15 — sample and description both to be satisfied', 'm': 1.5, 'skill': 'provision'},
                    {'id': 's2', 'pt': 'Facts identified: matches sample, not description', 'm': 0.5, 'skill': 'analysis'},
                    {'id': 's3', 'pt': 'Analysis — breach of implied condition', 'm': 1, 'skill': 'analysis'},
                    {'id': 's4', 'pt': 'Conclusion — right to reject', 'm': 1, 'skill': 'conclusion'}],
         'remarks': ['Many candidates stop at "bulk matches sample, so no breach" — read the description too.'],
         'mistakes': ['Treating it as a breach of warranty only.'],
         'tips': ['Quote the rule that both sample and description must be satisfied, then apply.']},
    ]

    viva = [
        V('v1', 'What is the difference between a condition and a warranty?',
          'A condition is essential to the main purpose of the contract; on breach of a condition the buyer can reject the goods, treating the contract as repudiated, and also claim damages. A warranty is collateral to the main purpose; for breach of warranty the buyer gets damages only and cannot reject the goods.',
          [P('p1', 'Condition: essential to the main purpose', 2, ALT('condition {e}', 'condition is {e}', e=('essential', 'main purpose', 'root', 'vital', 'fundamental', 'very important')) ),
           P('p2', 'Breach of condition: buyer may repudiate/reject and claim damages', 3,
             'reject|repudiat|rescind|cancel the contract|terminat|treat contract as ended|end the contract'),
           P('p3', 'Warranty: collateral to the main purpose', 2, ALT('warranty {e}', 'warranty is {e}', e=('collateral', 'subsidiary', 'secondary', 'minor', 'less important', 'ancillary'))),
           P('p4', 'Breach of warranty: damages only, no rejection', 3,
             ALT('warranty {d}', 'warranty only {d}', 'breach warranty {d}', 'warranty breach {d}', 'warranty gives {d}', 'warranty buyer {d}', 'warranty can only claim {d}', 'warranty buyer can only claim {d}', 'warranty cannot reject', 'warranty not reject', 'warranty no right reject', 'warranty buyer cannot reject',
                 d=('damages only', 'only damages', 'only claim damages', 'damages not reject', 'claim damages only', 'damages but not reject', 'only compensation', 'compensation only')))], 'c2'),
        V('v2', 'When is a breach of condition treated as a breach of warranty?',
          'Under Section 13 there are four cases: the buyer waives the condition; the buyer elects to treat the breach as a breach of warranty; the contract is non-severable and the goods, or some of them, have been accepted by the buyer; or the law excuses the condition, for example on impossibility.',
          [P('p1', 'Buyer waives the condition', 3, 'waive|waiver|give up|gives up|forgo'),
           P('p2', 'Buyer elects to treat it as a warranty', 2, 'elect|choose|chooses|opt|decide'),
           P('p3', 'Non-severable contract and buyer has accepted goods', 3, 'non severable|not severable|indivisible|cannot be split|non-severable|not divisible', 'accept|not severable accept|cannot be split accept|not divisible accept', min=2),
           P('p4', 'Excused by law (impossibility)', 2, 'excused|impossib|by law|law excuses')], 'c3'),
        V('v3', 'When does an implied condition of fitness for a particular purpose arise?',
          'Under Section 16(1) three things are needed: the buyer tells the seller the particular purpose he needs the goods for, he relies on the skill or judgment of the seller, and the seller deals in that kind of goods. There is no such condition if the buyer orders by patent or trade name without relying on the seller.',
          [P('p1', 'Buyer makes known the particular purpose', 3, 'purpose', 'known|tell|tells|told|disclos|inform|mention|explain|state', min=2),
           P('p2', 'Buyer relies on the seller\'s skill or judgment', 3, 'rely|relies|relied|relying|reliance|depend|trust', 'skill|judgment|judgement|expertise|advice', min=2),
           P('p3', 'Seller deals in goods of that description', 2, 'deal|dealer|trade|business|sells such|sell such'),
           P('p4', 'Not where bought by trade/patent name without reliance', 2, 'trade name|patent|brand|brand name|by name')], 'c4'),
        V('v4', 'What are the implied conditions in a sale by sample?',
          'Three conditions are implied. The bulk must match the sample in quality. The buyer must get a reasonable chance to compare the two. And the goods must have no hidden defect, not apparent on a reasonable examination of the sample, that makes them unmerchantable.',
          [P('p1', 'Bulk corresponds with the sample in quality', 4, 'bulk', 'correspond|match|same as|similar|agree|conform', min=2),
           P('p2', 'Reasonable opportunity to compare bulk with sample', 3, 'opportunity|chance|compare|comparing|comparison|check', min=1),
           P('p3', 'Free from latent defect not apparent on reasonable examination', 3, 'free from defect|free from any defect|free from latent|free from hidden|free of defect|no hidden defect|no latent defect|no hidden|no latent|latent defect|hidden defect|defect not apparent|defect not visible|not apparent|not visible|not discoverable|cannot be seen|unmerchantable')], 'c4'),
        V('v5', 'Explain caveat emptor and give any three exceptions.',
          'Caveat emptor means let the buyer beware. Under Section 16 there is no implied condition as to quality or fitness, so the buyer must examine the goods and use his own judgment. Exceptions include fitness for a purpose where the buyer relies on the seller, merchantable quality in a sale by description, sale by sample, sale by description, usage of trade, and fraud by the seller.',
          [P('p1', 'Meaning: let the buyer beware', 3, 'buyer beware|let buyer beware|buyer must beware|buyer should beware|buyer careful|buyer take care'),
           P('p2', 'No implied condition of quality/fitness — buyer uses own judgment', 3, 'no implied|not implied|own judgment|own judgement|examine|inspect|check himself|own risk|own skill', min=1),
           P('p3', 'Any three exceptions', 4, 'fitness|particular purpose|rely|relies|reliance', 'merchantab|saleable', 'sample', 'description', 'usage|custom', 'fraud|conceal|misrepresent', 'wholesome|food|eatable', min=3)], 'c6'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Anti-skid tiles for a hospital', 'difficulty': 'hard',
        'case': ('Arogya Hospital told Tilecraft, a dealer in tiles, that it needed "anti-skid tiles for wet operation-theatre floors" and asked Tilecraft to recommend a product. '
                 f'Tilecraft recommended and supplied {boxes} boxes of its "GripMax" tiles at {R(box_rate)} per box, in one delivery and for one price. The hospital\'s contractor laid all '
                 'the tiles. Within a week, two nurses slipped: tests show the tiles are slippery when wet. Similar ordinary tiles are worth ₹900 per box.'),
        'mcqs': [
            M('k1a', 'Which implied term has Tilecraft broken?', ['Condition of fitness for a particular purpose — Section 16(1)', 'Warranty of quiet possession — Section 14(b)', 'Condition as to title — Section 14(a)', 'No term — caveat emptor applies'], 0,
              'The purpose was disclosed, the hospital relied on the dealer\'s recommendation and the dealer deals in tiles.', 'moderate'),
            M('k1b', 'The hospital has accepted and laid all the tiles under a single, non-severable contract. Its remedy now is:', ['Damages only — breach treated as warranty (Section 13)', 'Reject the tiles and recover the full price', 'No remedy at all', 'Specific performance'], 0,
              'Acceptance under a non-severable contract turns the breach of condition into a breach of warranty — damages only.', 'hard'),
            M('k1c', f'What is the total price of the tiles supplied?', [R(k_price), '₹5,40,000', '₹6,00,000', '₹1,50,000'], 0,
              f'{boxes} × {R(box_rate)} = {R(k_price)}.', 'core', '600*1150'),
            M('k1d', 'If damages are measured as the difference between the price paid and the value of the tiles actually supplied (₹900 per box), the hospital can claim:', [R(k_dmg), R(k_price), '₹5,40,000', '₹250'], 0,
              f'{boxes} × (1,150 − 900) = {R(k_dmg)}. (Further losses, such as relaying costs, may be claimed if they are within Section 73 of the Contract Act.)', 'hard', '600*(1150-900)'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch03', 'n': 2, 'title': 'Conditions & Warranties',
        'outcomes': ['Explain stipulations as to time (Section 11) and distinguish a condition from a warranty (Section 12).',
                     'State when a breach of condition is treated as a breach of warranty (Section 13).',
                     'List and apply the implied conditions and warranties in Sections 14 to 17, with well-known cases.',
                     'Explain caveat emptor and its exceptions, and solve problems in Provision → Facts → Analysis → Conclusion form.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 45, 'practice': 50}, 'prereq': ['fnd-p2-ch03-u01'],
                 'exam_tip': 'Problems on fitness for purpose (Section 16(1)), sample and description, and caveat emptor appear in most attempts. Name the implied term, test each requirement against the facts, then give the remedy.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Section 11: time of payment not of essence unless intended; time of delivery depends on the contract.',
                        'Condition = essential → reject + damages. Warranty = collateral → damages only. Construction of the contract decides (Section 12(4)).',
                        'Section 13: condition becomes warranty on waiver, buyer\'s election, acceptance under non-severable contract, or legal excuse.',
                        'Implied conditions: title 14(a), description 15, fitness 16(1), merchantability 16(2), sample 17, sample + description 15, wholesomeness.',
                        'Implied warranties: quiet possession 14(b), no encumbrance 14(c), trade usage 16(3), warning of dangerous goods.',
                        'Caveat emptor (Section 16): buyer beware — except reliance on seller, description, sample, merchantability, trade usage, fraud, food.'],
            'remember': ['Fitness for purpose needs: purpose known + reliance on seller\'s skill + seller deals in such goods; excluded for trade-name purchase without reliance.',
                         'Cases: Rowland v. Divall (title), Varley v. Whipp (description), Priest v. Last (fitness — single obvious purpose), Frost v. Aylesbury Dairy (wholesomeness).'],
            'traps': ['A warranty can never become a condition.', 'Only the buyer can elect under Section 13.', 'Examination before purchase removes only the defects that examination ought to reveal.',
                      'Matching the sample is not enough if the goods were also sold by description.']},
        'quickref': [{'k': 'Section 11', 'v': 'Time of payment not of essence unless intended; other time terms per contract'},
                     {'k': 'Section 12', 'v': 'Condition (essential → repudiate) vs warranty (collateral → damages)'},
                     {'k': 'Section 13', 'v': 'Waiver · election · non-severable + accepted · excused by law'},
                     {'k': 'Section 14', 'v': '(a) title — condition; (b) quiet possession, (c) no encumbrance — warranties'},
                     {'k': 'Section 15', 'v': 'Description — goods must match; sample + description → both'},
                     {'k': 'Section 16', 'v': 'Caveat emptor; (1) fitness for purpose; (2) merchantability; (3) trade usage'},
                     {'k': 'Section 17', 'v': 'Sample: bulk = sample · chance to compare · no latent defect'},
                     {'k': 'Section 59', 'v': 'Breach of warranty: reduce price or sue for damages; no rejection'}],
        'viva': viva, 'cases': cases,
    }
