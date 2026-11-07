"""CA Foundation · Paper 2 Business Laws · Chapter 2 The Indian Contract Act, 1872 · Unit 8 Bailment and Pledge.
Original explanations and problems; Sections 148-181 cited by number. Pledge sale surplus/deficit and mixing shares are computed."""
from lib import *
from ca_viva import V, P, ALT
from ca_cases import M

UID = 'fnd-p2-ch02-u08'


def Q(qid, marks, diff, pad, q, model, scheme, remarks, mistakes, tips, checks=None):
    d = {'id': qid, 'marks': marks, 'minutes': minutes(marks), 'difficulty': diff, 'pad': pad, 'q': q, 'model': model,
         'scheme': [{'id': f's{i+1}', 'pt': pt, 'm': m, 'skill': sk} for i, (pt, m, sk) in enumerate(scheme)],
         'remarks': remarks, 'mistakes': mistakes, 'tips': tips}
    if checks: d['checks'] = checks
    return d


def MC(mid, q, options, answer, explain, concept, diff='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': diff}
    if check: d['check'] = check
    return d


def build():
    # ---------- Illustration 3: pawnee sells on default (Section 176) ----------
    c3 = Checks()
    interest = c3.add('300000*12/100*9/12', 'interest at 12% p.a. for 9 months')
    exp = c3.add('4500', 'necessary expenses of preserving the goods (Section 173)')
    dueamt = c3.add('300000+27000+4500', 'total amount due to the pawnee')
    sale_cost = c3.add('3500', 'cost of conducting the sale')
    net_a = c3.add('310000-3500', '(a) net sale proceeds')
    deficit = c3.add('331500-306500', '(a) deficit recoverable from the pawnor')
    net_b = c3.add('370000-3500', '(b) net sale proceeds')
    surplus = c3.add('366500-331500', '(b) surplus payable to the pawnor')
    t3 = table(['Particulars', '(a) Sold for ₹3,10,000', '(b) Sold for ₹3,70,000'], [
        ['Gross sale proceeds', 310000, 370000],
        ['Less: cost of sale', -3500, -3500],
        ['Net proceeds', net_a, net_b],
        ['Less: amount due (loan ₹3,00,000 + interest ₹27,000 + preservation ₹4,500)', -dueamt, -dueamt],
        ['Deficit (−) recoverable from pawnor / surplus (+) payable to pawnor', -deficit, surplus],
    ], num=[1, 2], title='Settlement after sale (₹)')

    # ---------- Illustration 4: mixing with consent and accidental loss (Section 155) ----------
    c4 = Checks()
    tot_bags = c4.add('40+60', 'bags in the mixture')
    left = c4.add('100-25', 'bags left after the accidental fire')
    share = c4.add('75*40/100', 'bailor\'s proportionate share of the remaining bags')

    # ---------- Illustration 2: finder may sell (Section 169) ----------
    c2 = Checks()
    two3 = c2.add('36000*2/3', 'two-thirds of the value of the found thing')
    charges = c2.add('14500+9800', 'finder\'s lawful charges (stabling and feed + veterinary care)')

    # ---------- Illustration 5: pledge by a person with limited interest (Section 179) ----------
    c5 = Checks()
    int5 = c5.add('120000*10/100*6/12', 'interest at 10% p.a. for 6 months on the original pledge')
    redeem = c5.add('120000+6000', 'amount the owner must pay to get the jewellery back')

    # ---------- MCQ / case numbers ----------
    cm = Checks()
    m_two3 = cm.add('45000*2/3', 'two-thirds of ₹45,000')
    kc = Checks()
    k_due = kc.add('500000+500000*9/100*1/2', 'loan plus 6 months\' interest at 9% p.a.')
    k_def = kc.add('522500-480000', 'deficit after sale')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch02', 'n': 8, 'title': 'Bailment and Pledge',
        'outcomes': ['Define bailment (Section 148), list its essentials and types, and test whether a given arrangement is a bailment.',
                     'State the duties and rights of the bailor and the bailee, the rights of both against a wrongdoer, and the modes of termination of bailment.',
                     'Explain the position of a finder of lost goods and distinguish particular lien (Section 170) from general lien (Section 171).',
                     'Define pledge (Section 172), state the rights and duties of pawnor and pawnee including sale on default (Section 176), explain pledge by non-owners, and distinguish bailment from pledge.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 55, 'practice': 50}, 'prereq': ['fnd-p2-ch02-u07'],
                 'exam_tip': 'Problems on the bailee\'s duty of care (Sections 151–152), faulty goods (Section 150), delay in return (Section 161), mixing (Sections 155–157), lien and pledge by non-owners are regular. Compute surplus/deficit whenever a pledged article is sold.'},
        'concepts': [
            {'id': 'c1', 'title': 'What is bailment? (Section 148)',
             'body': ['Bailment is the handing over of goods by one person (the bailor) to another (the bailee) for a purpose, on a contract that the goods will be returned, or dealt with as the bailor directs, once the purpose is over (Section 148).',
                      'Essentials: (1) a contract, express or implied — consideration is not necessary; (2) delivery of goods — actual (physical hand-over) or constructive (e.g. handing over the keys of a godown); (3) the delivery is for a purpose; (4) only possession passes, ownership stays with the bailor; (5) the same goods must come back, in original or altered form as agreed; and (6) only movable goods can be bailed — not land, and not money deposited in a bank, because the bank returns different notes.',
                      'Custody is not possession: a servant holding the master\'s goods is not a bailee; a car parked in a lot with the owner keeping the keys is not bailed; a bank locker whose key stays with the customer is not a bailment of its contents. Goods seized by customs authorities, however, pass into their possession, so a bailment arises.'],
             'analogy': 'Bailment is lending the steering wheel, not selling the car: someone else drives for a while, but the car is still yours.',
             'work': 'Inventory held by job workers, goods sent on consignment and stock in third-party warehouses are all bailments. Auditors confirm such stock with the bailee because it belongs to the client though it is not on the client\'s premises.'},
            {'id': 'c2', 'title': 'Types of bailment',
             'body': ['By benefit: (a) for the bailor\'s sole benefit — leaving jewellery with a neighbour for safe keeping free of charge; (b) for the bailee\'s sole benefit — lending your scooter free to a friend; (c) for mutual benefit — giving a phone for paid repair, or hiring a car.',
                      'By reward: gratuitous (no charge — types (a) and (b)) and non-gratuitous or for reward (type (c)). Many duties differ between the two, for example the bailor\'s duty to disclose faults and the effect of death on the bailment.'],
             'analogy': 'Who gets the benefit decides the type — like asking who is paying for the ride.',
             'work': 'Whether a warehouse or job worker is paid decides the standard of care the client can expect and which party bears expenses — a point CAs check in service and warehousing agreements.'},
            {'id': 'c3', 'title': 'Duties of the bailor',
             'body': ['Disclose faults (Section 150): in a gratuitous bailment the bailor must disclose faults he knows of that materially interfere with use or expose the bailee to extraordinary risk; if goods are bailed for hire, the bailor is liable for damage from such faults whether or not he knew of them.',
                      'Bear necessary expenses (Section 158): if the bailee is to keep, carry or work on the goods without payment, the bailor must repay necessary expenses incurred for the purpose.',
                      'Indemnify on early recall of a gratuitous loan (Section 159): the lender can demand the thing back at any time, but if the bailee has acted on the loan so that an early return causes him loss exceeding the benefit he had, the bailor must make it good.',
                      'Bear loss from defective title (Section 164): the bailor must compensate the bailee for loss suffered because the bailor had no right to bail the goods, or to receive them back or give directions about them.'],
             'analogy': 'A bailor is like a host lending his car: he must mention the faulty brakes, pay for the fuel he asked you to use for his errand, and not lend a car that is not his.',
             'work': 'Equipment rental agreements: Section 150 makes the lessor liable for defects in hired equipment even if unknown — a key risk CAs flag when reviewing rental income and warranty provisions.'},
            {'id': 'c4', 'title': 'Duties of the bailee',
             'body': ['Reasonable care (Sections 151–152): the bailee must take as much care of the goods as a person of ordinary prudence would take of his own goods of similar quantity, quality and value. If he takes that care, he is not liable for loss, destruction or deterioration — unless a special contract makes him liable.',
                      'No inconsistent or unauthorised use (Sections 153–154): an act inconsistent with the terms makes the bailment voidable at the bailor\'s option; unauthorised use makes the bailee liable for any damage arising from that use.',
                      'No mixing (Sections 155–157): mixing with the bailor\'s consent makes them co-owners in proportion to their shares; mixing without consent where the goods can be separated — the bailee bears the cost of separating and any damage; where they cannot be separated — the bailee must compensate the bailor for the goods.',
                      'Return (Sections 160–161): return or deliver the goods as directed when the time expires or the purpose is accomplished; if he fails to return at the proper time, he bears any loss, destruction or deterioration from that time, even without negligence.',
                      'Return accretions (Section 163) — any increase or profit from the goods (e.g. a calf born to a bailed cow) belongs to the bailor; and do not set up a title adverse to the bailor\'s.'],
             'analogy': 'Treat the bailed goods as a careful person treats his own — but remember they are only on loan, so do not use, mix or keep them beyond what was agreed.',
             'work': 'When a client\'s stock at a third-party warehouse is damaged, the claim against the warehouse turns on Sections 151–152: was reasonable care taken? CAs collect evidence (storage conditions, fire safety) before booking an insurance or recovery claim.'},
            {'id': 'c5', 'title': 'Rights of bailor and bailee; action against a wrongdoer; termination',
             'body': ['Bailor\'s rights: terminate the bailment on an inconsistent act (Section 153); demand back a gratuitous loan at any time (Section 159); claim accretions (Section 163); sue the bailee to enforce his duties and claim compensation for loss from negligence or unauthorised use; sue a wrongdoer (Section 180).',
                      'Bailee\'s rights: deliver to any one of joint bailors (Section 165); protection where he returns the goods in good faith to a bailor who had no title (Section 166); compensation for faulty goods (Section 150) and necessary expenses (Section 158); apply to court to stop delivery and decide title where a third person claims the goods (Section 167); lien (Sections 170–171).',
                      'Against a wrongdoer (Sections 180–181): if an outsider wrongfully takes the goods away, interferes with the bailee\'s use of them, or harms them, the bailee has the same remedies as the owner; either bailor or bailee may sue, and the compensation is shared according to their respective interests.',
                      'Termination: on expiry of the agreed period; on fulfilment of the purpose; by the bailor on an inconsistent act; at any time for a gratuitous bailment (subject to Section 159); on the death of either party in a gratuitous bailment (Section 162); and on destruction of the goods.'],
             'analogy': 'A thief who steals a hired car wrongs both the owner and the hirer — either can chase him, and the recovery is split by their interests.',
             'work': 'When a carrier loses goods in transit, the consignor (bailor) and the consignee or forwarding agent may both have claims. CAs ensure only one recovery is booked and shared correctly.'},
            {'id': 'c6', 'title': 'Finder of lost goods (Sections 71, 168, 169)',
             'body': ['A finder who takes goods into custody has a bailee\'s responsibility (Section 71). He must try to trace the owner and return the goods.',
                      'Section 168: the finder cannot sue the owner for the trouble and expense he voluntarily incurred in preserving the goods and tracing the owner, but he can retain the goods until he is compensated. Where the owner has offered a specific reward, the finder may sue for it and keep the goods until paid.',
                      'Section 169: if the thing is commonly sold, the finder may sell it where the owner cannot be found with reasonable diligence, or refuses on demand to pay his lawful charges, and (1) the thing is likely to perish or to lose most of its worth, or (2) the lawful charges in respect of the thing reach two-thirds of its value.'],
             'analogy': 'A finder is a temporary caretaker: he can hold the goods until his costs are paid, but he cannot send the owner a bill through the court — unless a reward was promised.',
             'work': 'Hotels, airports and malls run lost-property procedures built on these rules — keep, trace, return; sell only perishables or where costs mount, and account for the proceeds.'},
            {'id': 'c7', 'title': 'Right of lien — particular and general (Sections 170, 171)',
             'body': ['Lien is the right to keep possession of another person\'s goods until a claim is paid. It is a right to retain, not a right to sell.',
                      'Particular lien (Section 170): a bailee who, in line with the purpose of the bailment, has rendered services involving labour or skill on the goods may keep those goods until paid for those services, unless otherwise agreed. A tailor keeps the stitched suit; a jeweller keeps the polished stone. It is available only for the goods worked on, and arises automatically.',
                      'General lien (Section 171): bankers, factors, wharfingers, attorneys of a High Court and policy-brokers may, unless otherwise agreed, retain any goods bailed to them as security for a general balance of account — not just for charges on those particular goods. Others have a general lien only under an express contract.',
                      'Lien is lost if possession is given up, and may be waived or excluded by contract.'],
             'analogy': 'Particular lien: "I keep this suit until you pay for this suit." General lien: "I keep whatever of yours I hold until you clear your whole account with me."',
             'work': 'Banks rely on general lien to hold securities and deposits against overdue loans; CAs reviewing a borrower\'s liquidity note that such assets may not be freely available.'},
            {'id': 'c8', 'title': 'Pledge — meaning, rights and duties (Sections 172–177)',
             'body': ['A pledge is a bailment in which goods are handed over to secure the repayment of a debt or the carrying out of a promise (Section 172). The bailor is the pawnor (pledgor), the bailee the pawnee (pledgee). All essentials of bailment apply, plus: the purpose is security, the goods must exist, and delivery (actual or constructive) is essential.',
                      'Pawnee\'s rights: retain the goods for the debt, interest and necessary expenses of possession or preservation (Section 173); retain for other debts only under a contract — though such a contract is presumed for later advances by the pawnee (Section 174); recover extraordinary preservation expenses by suit, but not retain the goods for them (Section 175); on default, either sue on the debt and keep the goods as collateral, or sell the goods after reasonable notice to the pawnor — any shortfall remains payable by the pawnor and any surplus must be paid to him (Section 176).',
                      'Pawnor\'s right to redeem (Section 177): even after default, he may redeem the goods at any time before the actual sale by paying the debt plus expenses arising from his default. Pawnor\'s duties mirror a bailor\'s: pay the debt, disclose faults, bear extraordinary expenses, indemnify for defects in title and pay any deficit after sale. Pawnee\'s duties mirror a bailee\'s: care, no unauthorised use, no mixing, return on repayment, return accretions.'],
             'blocks': [t3],
             'analogy': 'A pledge is a bailment with a job: the goods sit with the lender as a guarantee, and can be sold only after a fair warning.',
             'work': 'Loans against gold, warehouse receipts and pledged shares all follow these rules. CAs auditing NBFCs check that sale notices were served before auctioning pledged gold, and that surpluses were refunded to borrowers.'},
            {'id': 'c9', 'title': 'Pledge by non-owners and bailment vs pledge',
             'body': ['Normally only the owner or his authorised agent can pledge. Exceptions protect good-faith pawnees: (a) a mercantile agent in possession of goods or documents of title with the owner\'s consent, acting in the ordinary course of business (Section 178); (b) a person in possession under a contract voidable for coercion, undue influence, fraud or misrepresentation, which the owner had not yet cancelled when the pledge was made (Section 178A); (c) a person holding only a limited interest — the pledge binds the owner only up to that interest (Section 179); (d) a co-owner in sole possession with the others\' consent; and (e) a seller left in possession after sale, or a buyer who obtained possession with the seller\'s consent before the sale is complete. In (a), (b) and (e) the pawnee must act in good faith without notice of the defect.',
                      'Bailment vs pledge: purpose — any purpose vs security for a debt; parties — bailor/bailee vs pawnor/pawnee; consideration — may be gratuitous vs always for consideration; right of sale — a bailee has none (even with a lien he can only retain) vs a pawnee can sell after notice on default; right of use — a bailee may use the goods if the contract allows vs a pawnee has no right to use; termination — on the purpose being achieved vs on repayment of the debt.'],
             'analogy': 'A bailee holds goods because of a job; a pawnee holds them because of a loan — and only the pawnee can sell them if the loan is not repaid.',
             'work': 'Commodity finance against goods held by collateral managers depends on who had power to pledge. A CA reviewing such a loan checks the warehouse receipt chain and whether the pledgor was a mercantile agent or a buyer in possession.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Hired car with faulty brakes', 'difficulty': 'core', 'minutes': 6,
             'q': 'Pooja hires a car from Quick Wheels for a weekend for ₹6,000. The brakes fail on a hill road and she is injured. Quick Wheels proves it did not know about the defect. Is it liable?',
             'solution': [legal('Section 150: the bailor must disclose faults that materially interfere with the use of the goods or expose the bailee to extraordinary risk. When the bailment is for hire, the bailor must answer for harm caused by such faults even if he did not know of them.',
                                'The car was bailed for hire at ₹6,000. Its brakes were defective, causing Pooja\'s injury. Quick Wheels did not know of the defect.',
                                'Since this is a bailment for reward, lack of knowledge is no defence. The defect exposed Pooja to extraordinary risk and caused the injury.',
                                'Quick Wheels is liable to compensate Pooja for her injuries.')]},
            {'id': 'i2', 'title': 'A lost pony and the finder\'s costs', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'Raghav finds a stray pony worth ₹36,000. He advertises for the owner, stables and feeds it (₹14,500) and pays a vet ₹9,800. After three months the owner, Sana, turns up but refuses to pay anything. (a) Can Raghav sue Sana for his expenses? (b) Can he keep the pony? (c) Could he have sold it?',
             'solution': [legal('Section 168: a finder cannot bring a suit against the owner to recover the trouble and cost he chose to take on, though he may keep the goods until compensated. Section 169: a finder may sell a thing commonly the subject of sale if the owner cannot be found or refuses to pay lawful charges, and the charges amount to two-thirds of its value (or the thing is perishing).',
                                f'Value ₹36,000; two-thirds = {R(two3)}. Raghav\'s charges = ₹14,500 + ₹9,800 = {R(charges)}. Sana refuses to pay.',
                                f'(a) No reward was offered, so Raghav cannot sue for expenses. (b) He may retain the pony until Sana pays his lawful charges. (c) His charges of {R(charges)} exceed two-thirds of the value ({R(two3)}), and Sana has refused to pay on demand, so a sale is permitted.',
                                f'Raghav cannot sue, but he may keep the pony until paid; and since the charges have crossed {R(two3)} and the owner has refused, he may sell it, accounting to Sana for any surplus after recovering his charges.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Pledged goods sold on default — surplus or deficit?', 'difficulty': 'hard', 'minutes': 10,
             'q': 'Tara pledges 50 bales of cotton with Unity Finance for a loan of ₹3,00,000 at 12% p.a. for 9 months. Unity spends ₹4,500 on fumigation (a necessary preservation expense). Tara defaults. After reasonable notice, Unity sells the bales, incurring ₹3,500 on the sale. Compute the amount payable by or to Tara if the bales fetch (a) ₹3,10,000; (b) ₹3,70,000.',
             'solution': [legal('Section 173: the pawnee may retain the goods for the debt, interest and necessary expenses of preservation. Section 176: on default, the pawnee may sell after reasonable notice; if the proceeds fall short of the amount due, the pawnor remains liable for the balance; any surplus must be paid to the pawnor.',
                                f'Loan ₹3,00,000; interest 12% for 9 months = {R(interest)}; preservation ₹4,500; amount due = {R(dueamt)}. Sale cost ₹3,500.',
                                f'(a) Net proceeds {R(net_a)} are less than {R(dueamt)}, leaving a shortfall of {R(deficit)}. (b) Net proceeds {R(net_b)} exceed the amount due by {R(surplus)}.',
                                f'(a) Tara must pay Unity {R(deficit)}. (b) Unity must pay Tara {R(surplus)}.'),
                          t3],
             'checks': c3},
            {'id': 'i4', 'title': 'Goods mixed with consent, then a fire', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'Varun stores 40 bags of basmati rice with Wasim, a trader, and allows him to mix them with Wasim\'s own 60 identical bags. A fire caused by lightning (no negligence) destroys 25 bags. How many bags is Varun entitled to?',
             'solution': [legal('Section 155: where the bailee, with the bailor\'s consent, mixes the bailor\'s goods with his own, both have an interest in the mixture in proportion to their respective shares. Section 152: a bailee who has taken reasonable care is not liable for accidental loss.',
                                f'Mixture = 40 + 60 = {tot_bags} bags; destroyed 25; remaining {left}. Varun\'s share 40%.',
                                f'The mixing was with consent, so the loss is borne proportionately. Wasim was not negligent, so he is not personally liable for the destroyed bags. Varun\'s share: {left} × 40/100 = {share} bags.',
                                f'Varun is entitled to {share} bags.')],
             'checks': c4},
            {'id': 'i5', 'title': 'Re-pledge by a pawnee (limited interest)', 'difficulty': 'moderate', 'minutes': 6,
             'q': 'Xavier pledges jewellery worth ₹2,50,000 with Yamini for ₹1,20,000 at 10% p.a. Yamini, without authority, re-pledges it with Zubin for ₹1,60,000. Six months later Xavier wants his jewellery back. What must he pay Zubin?',
             'solution': [legal('Section 179: a person who pledges goods in which he holds only a partial (limited) interest creates a pledge that is good only up to the value of that interest.',
                                f'Yamini\'s interest in the jewellery = ₹1,20,000 + interest for 6 months {R(int5)} = {R(redeem)}. She pledged it for ₹1,60,000.',
                                f'Zubin\'s security is good only up to Yamini\'s interest of {R(redeem)}. The extra ₹40,000 lent by Zubin is a matter between Zubin and Yamini.',
                                f'Xavier can recover his jewellery from Zubin by paying {R(redeem)}.')],
             'checks': c5},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Stock lying with a job worker', 'role': 'Statutory audit assistant', 'situation': 'Your client, a garment exporter, has fabric worth ₹38 lakh lying with three job workers for stitching on the balance-sheet date.',
             'steps': ['Recognise the arrangement as a bailment for mutual benefit: possession with the job workers, ownership with the client.', 'Obtain direct confirmations of quantities from each job worker and reconcile with the client\'s challans.',
                       'Check whether any job worker is claiming a lien for unpaid charges (Section 170) — those goods may not be released until paid.', 'Ensure the stock is included in the client\'s inventory and insured.'],
             'takeaway': 'Goods out on bailment are still the client\'s assets — but a bailee\'s lien can block access to them.', 'think': 'Can a job worker hold back the fabric of a new order because an earlier invoice is unpaid?',
             'answer': 'Not under Section 170 — a particular lien covers only the goods on which the labour was done. Unless the contract gives a general lien, the job worker cannot hold the new fabric for the old dues.'},
            {'id': 'j2', 'title': 'Gold loan auction', 'role': 'CA auditing a gold-loan NBFC', 'situation': 'The NBFC auctioned 120 overdue gold-loan accounts during the year. In 18 cases the auction proceeds exceeded the dues.',
             'steps': ['Verify that reasonable notice of sale was served on each borrower before the auction (Section 176).', 'Check that the surplus in the 18 cases was refunded or held as a liability payable to the borrowers, not taken to income.',
                       'For accounts with a shortfall, confirm that recovery steps continue against the borrowers.', 'Test that borrowers who paid before the actual auction were allowed to redeem (Section 177).'],
             'takeaway': 'A pawnee may sell — but only after notice, and the surplus belongs to the pawnor.', 'think': 'If a borrower offers full dues plus expenses an hour before the auction, must the NBFC accept?',
             'answer': 'Yes. Under Section 177 the pawnor may redeem at any time before the actual sale by paying the debt and the expenses caused by his default.'},
            {'id': 'j3', 'title': 'Damaged goods in a warehouse', 'role': 'CA in industry (plant accountant)', 'situation': 'Rain water entered a hired warehouse through a broken roof and damaged packaging material worth ₹6 lakh. The warehouse keeper says the rain was an "act of God".',
             'steps': ['Apply Sections 151–152: the keeper is liable unless he took the care a prudent person would take of his own goods.', 'Gather evidence: was the roof damage known and unrepaired? Were tarpaulins and drains provided?',
                       'If negligence is likely, lodge a written claim; if not, claim under the company\'s insurance.', 'Record the expected recovery as a claim receivable only when it is virtually certain.'],
             'takeaway': 'Heavy rain does not excuse a bailee who ignored a broken roof — the test is the care of a prudent owner.', 'think': 'Would the answer change if the keeper had signed a clause making him liable "for all loss howsoever caused"?',
             'answer': 'Yes. Section 152 allows a special contract to increase the bailee\'s liability; such a clause would make him liable even without negligence.'},
        ],
        'mcqs': [
            MC('m1', 'Under Section 148, bailment involves the delivery of:', ['Goods, for a purpose, to be returned or disposed of as directed', 'Goods, with transfer of ownership', 'Immovable property for a fixed period', 'Money to a bank for safe custody'], 0, 'Only possession of movable goods passes, for a purpose; ownership stays with the bailor.', 'c1'),
            MC('m2', 'Which is NOT an essential of bailment?', ['Transfer of ownership of the goods', 'Delivery of goods', 'A contract', 'Return of the same goods'], 0, 'In bailment only possession is transferred; ownership remains with the bailor.', 'c1'),
            MC('m3', 'Arun parks his car in a mall parking lot, locks it and keeps the keys. This is:', ['Not a bailment — there is no delivery of possession', 'A gratuitous bailment', 'A bailment for reward', 'A pledge'], 0, 'Custody of the space is not possession of the car; the owner keeps control through the keys.', 'c1', 'moderate'),
            MC('m4', 'The standard of care expected of a bailee is that of:', ['A person of ordinary prudence caring for his own goods of similar quantity, quality and value', 'An insurer', 'The highest possible care in all cases', 'The bailor himself'], 0, 'Section 151.', 'c4'),
            MC('m5', 'If goods are bailed for hire and the bailor did not know of a dangerous defect, the bailor is:', ['Liable for damage caused by the defect', 'Not liable as he did not know', 'Liable only for half the damage', 'Liable only if the bailee was careful'], 0, 'Section 150 — for hire, the bailor is responsible whether or not he was aware of the faults.', 'c3'),
            MC('m6', 'A bailee who fails to return goods at the agreed time is responsible for their loss:', ['From that time, even without negligence', 'Only if he was negligent', 'Only if the bailor sues within a week', 'Never, if the loss was accidental'], 0, 'Section 161.', 'c4', 'moderate'),
            MC('m7', 'Where there are joint bailors, the bailee may deliver the goods to:', ['Any one of them, unless otherwise agreed', 'All of them together only', 'The eldest of them', 'None until a court order'], 0, 'Section 165.', 'c5'),
            MC('m8', 'A right to retain goods only for charges for labour or skill spent on those very goods is:', ['A particular lien (Section 170)', 'A general lien (Section 171)', 'A right of stoppage', 'A pledge'], 0, 'Particular lien attaches to the goods worked upon.', 'c7'),
            MC('m9', 'Which of the following does NOT have a general lien under Section 171?', ['A tailor', 'A banker', 'A wharfinger', 'A factor'], 0, 'Section 171 lists bankers, factors, wharfingers, attorneys of a High Court and policy-brokers. A tailor has only a particular lien.', 'c7'),
            MC('m10', 'A finder may sell a lost thing commonly sold if the owner refuses to pay his lawful charges and those charges reach:', ['Two-thirds of its value', 'One-half of its value', 'One-third of its value', 'Its full value'], 0, 'Section 169(2).', 'c6'),
            MC('m11', 'A finder spends ₹31,000 caring for a found horse worth ₹45,000; the owner refuses to pay. Two-thirds of the value is:', [R(m_two3), '₹15,000', '₹22,500', '₹31,000'], 0, f'₹45,000 × 2/3 = {R(m_two3)}; the charges of ₹31,000 exceed this, so a sale is permitted under Section 169.', 'c6', 'moderate', '45000*2/3'),
            MC('m12', 'A bailment of goods made to secure repayment of a loan is called:', ['Pledge', 'Hypothecation', 'Mortgage', 'Lien'], 0, 'Section 172.', 'c8'),
            MC('m13', 'A pawnee incurs extraordinary expenses to preserve the pledged goods. He may:', ['Recover them from the pawnor but not retain the goods for them', 'Retain the goods until they are paid', 'Sell the goods immediately', 'Not recover them at all'], 0, 'Section 175 — recoverable by suit; no right of retention for extraordinary expenses.', 'c8', 'moderate'),
            MC('m14', 'After default, the pawnor may redeem the goods:', ['At any time before the actual sale, paying the debt and expenses of default', 'Only within 7 days of default', 'Never after default', 'Only after the sale, by paying the buyer'], 0, 'Section 177.', 'c8'),
            MC('m15', 'A obtains a ring from B by fraud and, before B rescinds the contract, pledges it with C who acts in good faith. The pledge is:', ['Valid — Section 178A', 'Void — A was not the owner', 'Voidable at C\'s option', 'Valid only if B consents'], 0, 'A pledge by a person in possession under a voidable contract not yet rescinded gives a good-faith pawnee a good title.', 'c9', 'hard'),
        ],
        'questions': [
            Q('q1', 4, 'core', 'legal',
              'Bhavesh gives his diamond ring to Chitra, his friend, for safe custody, on the condition that she keeps it in her bank locker. Chitra keeps it in a cupboard at home, from where it is stolen in a burglary. Chitra argues that she kept her own jewellery in the same cupboard and lost it too. Is she liable?',
              [legal('Section 151: a bailee must take as much care of the goods as a person of ordinary prudence would take of his own goods of similar bulk, quality and value. Section 152: a bailee who has taken such care is not liable, in the absence of a special contract. A bailee must also follow the terms of the bailment.',
                     'The ring was bailed on the condition that it be kept in a bank locker. Chitra kept it at home, and it was stolen along with her own jewellery.',
                     'Chitra departed from the agreed term about where the ring was to be kept. The special condition defined the care she had to take; her own carelessness with her jewellery does not lower that standard. The loss arose from her breach of the condition.',
                     'Chitra is liable to compensate Bhavesh for the value of the ring.')],
              [('Sections 151–152 standard of care', 1.5, 'provision'), ('Special condition of bailment noted', 1, 'analysis'), ('Rejects "same care as own goods" defence on these facts', 0.5, 'analysis'), ('Conclusion: liable', 1, 'conclusion')],
              ['Candidates often accept the "own goods were stolen too" argument without noticing the special term about the bank locker.'],
              ['Ignoring the agreed place of safe keeping.', 'Saying a gratuitous bailee is never liable.'],
              ['Mention both Section 151 and Section 152.']),
            Q('q2', 5, 'core', 'table',
              'Differentiate a bailment from a pledge on any five bases.',
              [table(['Basis', 'Bailment', 'Pledge'], [
                  ['Meaning', 'Delivery of goods for any purpose, to be returned when the purpose is over (Section 148)', 'Bailment of goods as security for a debt or promise (Section 172)'],
                  ['Parties', 'Bailor and bailee', 'Pawnor (pledgor) and pawnee (pledgee)'],
                  ['Consideration', 'May be gratuitous', 'Always supported by consideration (the loan or promise)'],
                  ['Right of sale', 'No right to sell; even a lien is only a right to retain', 'May sell after reasonable notice on default (Section 176)'],
                  ['Right to use', 'May use if the terms allow', 'No right to use the pledged goods'],
                  ['Termination', 'On expiry of time or fulfilment of purpose', 'On repayment of the debt or performance of the promise'],
              ])],
              [('Meaning', 1, 'concept'), ('Parties', 1, 'concept'), ('Consideration', 1, 'concept'), ('Right of sale', 1, 'analysis'), ('Use / termination', 1, 'analysis')],
              ['The right of sale is the single most important distinction — never leave it out.'],
              ['Saying a bailee with a lien can sell.', 'Saying pledge can be gratuitous.'],
              ['Keep to six crisp rows; quote Sections 148, 172 and 176.']),
            Q('q3', 4, 'moderate', 'legal',
              'Divya lends her laptop free of cost to Ehsan for one week to prepare a project report. Ehsan keeps it for three weeks. In the third week, a short circuit in the building (not caused by Ehsan) damages the laptop. Divya claims compensation. Advise Ehsan.',
              [legal('Section 160: the bailee must return the goods when the time for which they were bailed has expired. Section 161: a bailee who, by his own default, keeps the goods beyond the proper time bears any loss, destruction or deterioration happening after that time.',
                     'The laptop was lent for one week. Ehsan kept it for three weeks. The damage happened in the third week, after the agreed period.',
                     'Ehsan was in default from the end of the first week. Any loss from then on is his responsibility, even though he did not cause the short circuit and even though the bailment was gratuitous.',
                     'Ehsan is liable to compensate Divya for the damage.')],
              [('Sections 160–161 stated', 1.5, 'provision'), ('Default after one week identified', 1, 'analysis'), ('Liability without negligence explained', 0.5, 'analysis'), ('Conclusion', 1, 'conclusion')],
              ['Good answers point out that negligence is irrelevant once the bailee is late.'],
              ['Using Sections 151–152 (reasonable care) and concluding he is not liable.'],
              ['Fix the date from which the bailee is in default.']),
            Q('q4', 6, 'hard', 'legal',
              '(a) Fatima gives her car to Gautam\'s garage for repairs. The bill is ₹42,000. Fatima also owes Gautam ₹15,000 for an earlier repair to her scooter, which she collected without paying. Can Gautam retain the car until both amounts are paid? (3 marks) (b) Harish, a mercantile agent, is entrusted with 200 mobile phones by Indu Electronics for sale. He pledges them with Javed Finance for a loan; Javed acts in good faith and has no notice that Harish had no authority to pledge. Is the pledge valid? (3 marks)',
              [p('(a)'), legal('Section 170: a bailee who has rendered services involving labour or skill on the goods bailed may retain those goods until paid for those services — a particular lien. A general lien (Section 171) is available only to bankers, factors, wharfingers, attorneys of a High Court and policy-brokers, or under an express contract.',
                               'Gautam repaired the car (bill ₹42,000). The earlier ₹15,000 relates to the scooter, which Fatima has already taken back.',
                               'Gautam\'s particular lien attaches to the car only for the work done on the car. A garage is not among the persons given a general lien, and no contract for a general lien is stated.',
                               'Gautam can retain the car until ₹42,000 is paid, but not for the ₹15,000 scooter dues, which he must recover by suit.'),
               p('(b)'), legal('Section 178: a mercantile agent who, with the owner\'s consent, is in possession of goods or documents of title can pledge them in the normal course of his business as such an agent, and the pledge then binds the owner as if he had authorised it, provided the pawnee acts in good faith without notice of the agent\'s lack of authority.',
                               'Harish, a mercantile agent, was in possession of the phones with Indu\'s consent and pledged them with Javed, who acted in good faith without notice.',
                               'All conditions of Section 178 are met: mercantile agent, possession with consent, ordinary course of business, good faith of the pawnee.',
                               'The pledge is valid. Indu\'s remedy lies against Harish.')],
              [('(a) Section 170 particular lien', 1, 'provision'), ('(a) No general lien for a garage (Section 171)', 1, 'analysis'), ('(a) Conclusion with amounts', 1, 'conclusion'),
               ('(b) Section 178 and its conditions', 1.5, 'provision'), ('(b) Application and conclusion', 1.5, 'conclusion')],
              ['In (a), state the amount for which the lien is available — examiners look for ₹42,000.', 'In (b), list the conditions before applying them.'],
              ['Giving a general lien to a repairer.', 'Holding the pledge void because Harish was not the owner.'],
              ['Answer each sub-part as a separate mini-PFAC.'],
              checks=[{'expr': '42000+15000', 'value': 57000, 'label': 'total dues — only ₹42,000 covered by lien'}]),
        ],
        'revision': {'summary': ['Bailment (148): delivery of movable goods for a purpose, to be returned/disposed of as directed; possession, not ownership; consideration not needed.',
                                 'Types: for bailor / bailee / both; gratuitous / for reward.',
                                 'Bailor duties: disclose faults (150 — strict for hire), necessary expenses (158), indemnify early recall (159), defective title (164).',
                                 'Bailee duties: care (151–152), no inconsistent/unauthorised use (153–154), no mixing (155–157), return on time (160–161), accretions (163).',
                                 'Bailee rights: joint bailors (165), good-faith redelivery (166), interpleader to court (167), lien (170–171); both may sue wrongdoer (180–181).',
                                 'Finder: keep till paid (168), sue only for offered reward, sell under 169 (perishing or charges ≥ two-thirds of value).',
                                 'Pledge (172): retain for debt + interest + necessary expenses (173); sale after notice, deficit/surplus (176); redeem before sale (177); non-owners 178, 178A, 179.'],
                     'remember': ['Particular lien: goods worked on (170). General lien: bankers, factors, wharfingers, High Court attorneys, policy-brokers (171).', 'Gratuitous bailment ends on death of either party (162).', 'Extraordinary expenses of pawnee: sue, but no retention (175).'],
                     'traps': ['A bank deposit of money is not a bailment.', 'Lien is a right to retain, not to sell (except pawnee under 176 and finder under 169).', 'A late bailee is liable even without negligence (161).', 'Do not forget to deduct sale costs and add interest when computing surplus/deficit.']},
        'quickref': [{'k': 'Section 148', 'v': 'Bailment, bailor, bailee'}, {'k': 'Section 150', 'v': 'Bailor\'s duty to disclose faults'}, {'k': 'Sections 151–152', 'v': 'Bailee\'s care; not liable if reasonable care taken'},
                     {'k': 'Sections 153–154', 'v': 'Inconsistent act — voidable; unauthorised use — liable'}, {'k': 'Sections 155–157', 'v': 'Mixing with consent / separable / inseparable'},
                     {'k': 'Sections 158–159', 'v': 'Necessary expenses; gratuitous loan recall'}, {'k': 'Sections 160–161', 'v': 'Return; liability for delay'}, {'k': 'Section 162', 'v': 'Gratuitous bailment ends on death'},
                     {'k': 'Section 163', 'v': 'Accretions to bailor'}, {'k': 'Sections 165–167', 'v': 'Joint bailors; good-faith redelivery; court to decide title'},
                     {'k': 'Sections 168–169', 'v': 'Finder: retain, reward, sale (two-thirds rule)'}, {'k': 'Sections 170 / 171', 'v': 'Particular lien / general lien'},
                     {'k': 'Sections 172–177', 'v': 'Pledge; retention; subsequent debts; extraordinary expenses; sale on default; redemption'},
                     {'k': 'Sections 178, 178A, 179', 'v': 'Pledge by mercantile agent; under voidable contract; limited interest'}, {'k': 'Sections 180–181', 'v': 'Suit against wrongdoer; apportionment'}],
        'viva': [
            V('v1', 'Define bailment and state its essential features.',
              'Section 148 describes bailment as handing over goods to another person for a particular purpose, on a contract that they will be returned or disposed of as directed when the purpose is accomplished. Its essentials are a contract, delivery of possession of movable goods, a purpose, return of the same goods, and no transfer of ownership.',
              [P('p1', 'Delivery of goods for a purpose (Section 148)', 3, 'deliver|hand over|handing over|possession', 'purpose|section 148|148', min=2),
               P('p2', 'Based on a contract', 2, 'contract|agreement'),
               P('p3', 'Same goods to be returned / disposed of as directed', 3, 'return|give back|given back|giving back|hand back|handed back|restor|disposed|dispose'),
               P('p4', 'Possession passes, not ownership; movable goods only', 2, 'not ownership|ownership not|no transfer of ownership|ownership remains|ownership stays|without ownership|only possession|owner remains|movable|moveable')], 'c1'),
            V('v2', 'What degree of care must a bailee take, and when is he not liable for loss?',
              'Under Section 151 a bailee must take as much care of the goods as a person of ordinary prudence would take of his own goods of similar quantity, quality and value. Under Section 152, if he has taken that care, he is not liable for loss, destruction or deterioration, unless there is a special contract.',
              [P('p1', 'Care of an ordinary prudent person for his own goods (151)', 5, 'prudent|prudence|reasonable care|reasonable person', 'own goods|his own|similar goods|same bulk|similar quantity|section 151|151', min=2),
               P('p2', 'Not liable if he took that care (152)', 3, 'not liable|not responsible|no liability|not be liable|not held liable|section 152|152'),
               P('p3', 'Unless a special contract says otherwise', 2, 'special contract|unless agreed|contract otherwise|contrary|specific contract')], 'c4'),
            V('v3', 'Distinguish between a particular lien and a general lien.',
              'A particular lien under Section 170 lets a bailee retain only the goods on which he has spent labour or skill, until paid for that work; it is automatic. A general lien under Section 171 lets bankers, factors, wharfingers, attorneys of a High Court and policy brokers retain any goods of the bailor for a general balance of account.',
              [P('p1', 'Particular lien: only the goods worked on, for that work (170)', 5, 'particular lien only|particular only|particular keep only|particular retain only|particular hold only|particular lien keep only|particular lien retain only|particular lien hold only|particular lien goods worked|particular lien those goods|particular lien labour|particular lien skill|particular lien specific goods|particular lien same goods|particular lien goods on which|particular goods worked|section 170|170'),
               P('p2', 'General lien: any goods for a general balance of account (171)', 3, 'general lien general balance|general lien balance of account|general general balance|general balance of account|general lien whole account|general retain any|general keep any|general hold any|section 171|171|general lien any goods|general lien all goods|general lien other debt|general lien any debt|general any goods|general all goods|general any debt'),
               P('p3', 'General lien holders: bankers, factors, wharfingers, attorneys, policy-brokers', 2, 'banker|bank|factor|wharfinger|attorney|policy broker')], 'c7'),
            V('v4', 'What are the rights of a pawnee if the pawnor makes default?',
              'Under Section 176, if the pawnor defaults, the pawnee may sue the pawnor on the debt and retain the goods as collateral security, or he may sell the goods after giving the pawnor reasonable notice. If the sale proceeds are less than the amount due, the pawnor must pay the balance; if they are more, the pawnee must pay the surplus to the pawnor.',
              [P('p1', 'Sue on the debt and retain the goods as collateral', 3, 'sue|suit|file a case', 'retain|keep|hold|collateral', min=2),
               P('p2', 'Sell after reasonable notice', 4, 'sell|sale|auction', 'notice|inform|intimat|warn', min=2),
               P('p3', 'Deficit from pawnor; surplus to pawnor', 3, 'balance|deficit|shortfall|short|less|remaining', 'surplus|excess|extra|more', min=2)], 'c8'),
            V('v5', 'When can a person who is not the owner make a valid pledge?',
              'A valid pledge can be made by a mercantile agent who holds the goods with the owner\'s consent and pledges them in the normal course of his business, under Section 178; by a person in possession under a voidable contract not yet rescinded, under Section 178A; by a person with a limited interest, to the extent of that interest, under Section 179; by a co-owner in sole possession; and by a seller or buyer in possession. The pawnee must act in good faith.',
              [P('p1', 'Mercantile agent (178)', 2, 'mercantile|agent|section 178|178'),
               P('p2', 'Possession under a voidable contract not rescinded (178A)', 2, 'voidable|fraud|not rescinded|not cancelled|178a'),
               P('p3', 'Limited interest — valid to that extent (179)', 2, 'limited interest|limit interest|to the extent|extent of|section 179|179'),
               P('p4', 'Co-owner in possession; seller or buyer in possession', 2, 'co owner|coowner|joint owner|seller|buyer'),
               P('p5', 'Pawnee must act in good faith without notice', 2, 'good faith|bona fide|bonafide|honest|without notice|no notice')], 'c9'),
            V('v6', 'Give the main differences between bailment and pledge.',
              'Bailment may be for any purpose, while a pledge is a bailment only as security for a debt. A bailment may be gratuitous, but a pledge always has consideration. A bailee cannot sell the goods, whereas a pawnee can sell them after reasonable notice on default. A bailee may use the goods if allowed, but a pawnee cannot use them.',
              [P('p1', 'Purpose: any purpose vs security for a debt', 3, 'security|secure|guarantee|collateral', 'debt|loan|repayment|promise', min=2),
               P('p2', 'Bailment may be gratuitous; pledge always for consideration', 2, 'gratuitous|free|without consideration|no consideration|always consideration|consideration|need not consideration|not need consideration|not necessary consideration|consideration not necessary|consideration not needed|consideration not required|no need consideration|need no consideration'),
               P('p3', 'Bailee cannot sell; pawnee can sell after notice on default', 4, ALT('bailee {n} sell', 'bailee {n} sale', 'bailment {n} sell', 'bailment {n} sale', 'bailment no right to sell', 'bailee no right to sell', n=('cannot', 'can not', 'not', 'no right', 'has no right', 'not allowed')), ALT('pawnee {c} sell', 'pledgee {c} sell', 'pledge {c} sell', 'pawnee sell', 'pledgee sell', 'pawnee sale', 'pledgee sale', 'pledge right to sell', 'pledge right of sale', c=('can', 'may', 'right to', 'allowed to', 'has right to'))),
               P('p4', 'Use of goods: bailee may if allowed; pawnee cannot', 1, 'use|cannot use|not use|no right to use|not allowed to use|not entitled to use')], 'c9'),
            V('v7', 'What are the rights of a finder of lost goods?',
              'The finder cannot sue the owner for his trouble and expenses, but under Section 168 he can retain the goods until he is compensated, and he can sue for a specific reward if one was offered. Under Section 169 he may sell a thing commonly sold if the owner cannot be found or refuses to pay, when the thing is perishing or his charges reach two thirds of its value.',
              [P('p1', 'Retain the goods until compensated (168)', 3, 'retain|keep|hold', 'until|till|compensat|paid|section 168|168', min=2),
               P('p2', 'Cannot sue for expenses, but can sue for an offered reward', 3, 'reward'),
               P('p3', 'May sell: perishing, or charges reach two-thirds of value (169)', 4, 'sell|sale', 'perish|two third|2 third|2 3|two thirds|section 169|169', min=2)], 'c6'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Krishna Jewellers and a gold loan', 'difficulty': 'hard',
            'case': ('Lata pledges gold bangles with Metro Gold Finance for a loan of ₹5,00,000 at 9% p.a., repayable in 6 months. When the loan falls due, Lata does not pay. Metro sends her a letter giving 15 days\' notice of sale, then auctions the bangles for ₹4,80,000 (no sale costs). Separately, Lata had left a necklace with Krishna Jewellers for re-polishing; the polishing charge is ₹3,200. She also owes Krishna ₹8,000 for a ring bought on credit last year. Krishna refuses to return the necklace until she pays ₹11,200.'),
            'mcqs': [
                M('k1a', 'What was the total amount due to Metro on the date of default?', [R(k_due), '₹5,45,000', '₹5,00,000', '₹5,09,000'], 0,
                  f'Loan ₹5,00,000 + interest at 9% for 6 months ₹22,500 = {R(k_due)} (Section 173 allows retention for interest).', 'moderate', '500000+500000*9/100*1/2'),
                M('k1b', 'After the auction, what is the position between Lata and Metro?', [f'{R(k_def)} payable by Lata to Metro', '₹20,000 payable by Metro to Lata', 'Nothing is payable either way', '₹20,000 payable by Lata to Metro'], 0,
                  f'Proceeds ₹4,80,000 fall short of {R(k_due)} by {R(k_def)}; Section 176 keeps the pawnor liable for the balance.', 'hard', '522500-480000'),
                M('k1c', 'Could Lata have stopped the auction?', ['Yes, by paying the dues and default expenses before the actual sale (Section 177)', 'No, once she defaulted the right was lost', 'Only by obtaining a court order', 'Only within 7 days of default'], 0,
                  'The right to redeem continues until the actual sale.', 'moderate'),
                M('k1d', 'For what amount can Krishna Jewellers retain the necklace?', ['₹3,200 — particular lien for the polishing only', '₹11,200 — general lien for all dues', '₹8,000 only', 'Nothing — a jeweller has no lien'], 0,
                  'Section 170 gives a particular lien for labour or skill on the necklace. A jeweller does not have a general lien under Section 171 without a contract.', 'hard'),
            ]}],
    }


# ---------- teaching explanations + topic tags for every MCQ (override the short drafts above) ----------
TWB, TDBR, TDBE, TRBE = 'What is Bailment?', 'Duties of a Bailor', 'Duties of a Bailee', 'Rights of a Bailee'
TFIND, TLIEN, TPLG, TPNO = 'Finder of Lost Goods', 'Right of Lien', 'Pledge', 'Pledge by Non-owners'
EXPLAIN = {
    'm1': (TWB, 'Section 148: in a bailment, goods are handed over for a purpose under a contract that, once the purpose is served, they will be returned or dealt with as the bailor directs. Only possession of movable goods passes; ownership stays with the bailor. The tempting trap is "money to a bank for safe custody" — a deposit makes the bank a debtor, not a bailee, since the same notes are not returned. In practice: goods sent to a job-worker for processing are a bailment.'),
    'm2': (TWB, 'The essentials of bailment are a contract, delivery of possession of goods, a purpose, and return or disposal of the same goods as directed. Ownership does not pass; if it did, the transaction would be a sale. The tempting trap is "return of the same goods" — that is essential; returning equivalent goods would be a different transaction. In practice: when a CA audits inventory, goods held for others on job work or consignment are excluded because ownership never passed.'),
    'm3': (TWB, 'Bailment needs delivery of possession. Arun locked the car and kept the keys, so the mall never got possession or control; it only provided space. There is no bailment. The tempting trap is "a bailment for reward", since a parking fee may be paid — paying for space does not hand over possession. Valet parking, where keys are handed over, would be different. In practice: parking operators distinguish self-parking from valet services when setting their liability terms.'),
    'm4': (TDBE, 'Section 151: a bailee must look after the goods as carefully as a reasonably prudent person would look after his own goods of similar quantity, quality and value. The tempting trap is "an insurer" — the bailee is not liable for every loss; if he takes that care, he is not responsible for loss or damage. In practice: warehouses document fire safety, security and pest control to show they met this standard when goods are damaged.'),
    'm5': (TDBR, 'Section 150: a bailor must disclose known faults, and where goods are bailed for hire, he is responsible for damage from faults whether or not he knew of them. The bailor here hired out the goods, so he is liable even though unaware. The tempting trap is "not liable as he did not know"; that defence works only in gratuitous bailment. In practice: equipment-rental firms carry out safety checks and insurance because they are liable for defects in hired machinery.'),
    'm6': (TDBE, 'Section 161: if, by the bailee\'s default, goods are not returned at the proper time, he is responsible for any loss, destruction or deterioration from that time, even without negligence. The tempting trap is "only if he was negligent" — after the agreed return date, the bailee bears the risk of accidents too. In practice: a hirer who keeps a rented car beyond the due date is liable if it is damaged in a flood the next day.'),
    'm7': (TRBE, 'Section 165: where goods are owned by several persons jointly and bailed by them, the bailee may deliver them to, or according to the directions of, one joint owner without the consent of all, unless there is an agreement to the contrary. The tempting trap is "all of them together only" — the law does not require all joint owners to be present. In practice: banks holding jointly deposited articles follow the mandate in the joint account documents.'),
    'm8': (TLIEN, 'Section 170: where a bailee renders a service involving labour or skill on the goods bailed, he may retain them until paid for that service. This particular lien attaches only to the goods worked upon and only for charges on them. The tempting trap is "a general lien" — that allows retention for a general balance of account and is limited to certain persons under Section 171. In practice: a car repairer can keep a car until repair charges on that car are paid.'),
    'm9': (TLIEN, 'Section 171 gives a general lien — retention for a general balance of account — only to bankers, factors, wharfingers, attorneys of a High Court and policy-brokers, unless there is a contract. A tailor has only a particular lien for work on the cloth given. The tempting trap is the wharfinger, a less familiar term — a wharfinger owns a wharf and is expressly listed. In practice: banks exercise general lien over securities in a customer\'s name for all dues owed.'),
    'm10': (TFIND, 'Section 169: when a lost thing commonly sold cannot be returned because the owner cannot be found or refuses to pay lawful charges, the finder may sell it if it is in danger of perishing or losing most of its value, or if the charges amount to two-thirds of its value. The tempting trap is "one-half", a common misremembering. In practice: lost-property departments at railways sell perishable or long-unclaimed items as per their rules and keep records of proceeds.'),
    'm11': (TFIND, 'Two-thirds of value = ₹45,000 × 2/3 = ₹30,000. The finder\'s charges of ₹31,000 exceed that, so under Section 169 he may sell the horse after the owner refuses to pay. The tempting trap is ₹31,000, confusing the charges with the threshold. In practice: when a finder or bailee sells goods to recover charges, he must account for any surplus to the owner, so records of expenses matter.'),
    'm12': (TPLG, 'Section 172: when goods are bailed to secure a loan or the performance of a promise, the bailment is a pledge. The pawnor delivers possession to the pawnee. The tempting trap is "hypothecation" — there the borrower keeps possession and the lender only has a charge, so it is not a bailment. A mortgage relates to immovable property and lien is a right to retain. In practice: gold loans from banks and NBFCs are pledges, since the gold is physically handed over.'),
    'm13': (TPLG, 'Section 175: a pawnee may recover from the pawnor any extraordinary expenses he incurs to preserve the pledged goods. But under Section 174 he can retain the goods only for the debt, interest and necessary expenses of possession or preservation, not for extraordinary expenses. The tempting trap is "retain the goods until they are paid". In practice: a lender that pays for special repairs to pledged machinery must sue separately rather than hold it for that cost.'),
    'm14': (TPLG, 'Section 177: where a time for payment is fixed and the pawnor defaults, he may still redeem the goods at any later time before their actual sale, but he must also pay any expenses arising from his default. The tempting trap is "never after default" — default alone does not end the right to redeem. In practice: gold-loan customers can redeem pledged jewellery up to the auction date by paying the dues and charges.'),
    'm15': (TPNO, 'Section 178A: someone holding goods under a voidable contract that has not yet been set aside can pledge them validly to a pawnee who takes them honestly and unaware of the defect. A got the ring by fraud, but B had not rescinded, and C acted in good faith, so C gets a good title as pawnee. The tempting trap is "void — A was not the owner". In practice: pawnbrokers and gold lenders protect themselves by documenting good-faith checks.'),
    'k1/k1a': (TPLG, 'Interest = ₹5,00,000 × 9% × 6/12 = ₹22,500. Total due on default = ₹5,00,000 + ₹22,500 = ₹5,22,500. Section 173 lets a pawnee retain the goods for the debt and interest. The tempting trap is ₹5,45,000, taking a full year\'s interest instead of six months. In practice: gold-loan statements show principal and accrued interest separately, and the CA checks interest accruals at the period end.'),
    'k1/k1b': (TPLG, 'Section 176: after reasonable notice, the pawnee may sell the goods; if the proceeds are less than the amount due, the pawnor remains liable for the balance. Shortfall = ₹5,22,500 − ₹4,80,000 = ₹42,500, so Lata owes Metro ₹42,500. The tempting trap is ₹20,000, comparing proceeds with the principal alone. If there were a surplus, Metro would have to pay it to Lata. In practice: lenders send borrowers a statement after auction showing any shortfall or surplus.'),
    'k1/k1c': (TPLG, 'Section 177 lets a defaulting pawnor redeem the pledged goods at any time before the actual sale by paying the amount due and any expenses caused by the default. Lata could have stopped the auction this way. The tempting trap is "no, once she defaulted the right was lost" — default starts the sale process but does not end redemption rights. In practice: gold-loan borrowers often repay just before the auction date to recover their jewellery.'),
    'k1/k1d': (TLIEN, 'Krishna\'s right is a particular lien under Section 170 for labour or skill spent on the necklace: ₹3,200. A jeweller is not among the persons given a general lien by Section 171, and there is no contract granting one, so the old ₹8,000 for the ring must be recovered separately. The tempting trap is ₹11,200 — that would require a general lien. In practice: service businesses can hold the item serviced only for that job\'s charges, not for old credit dues.'),
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
           's1': _k('section 151|ordinary prudence|prudence', 'own goods|his own|her own|similar bulk|bulk', 'section 152|not liable|special contract', n=2),
           's2': _k('locker|bank locker', 'condition|term|terms|agreed|special|instruction|breach|violate|violated|departed|contrary|disobey'),
           's3': _k('own jewellery|her own|own goods|same cupboard|same care', 'no defence|not a defence|not defence|does not help|irrelevant|not lower|not reduce|not enough|not sufficient|no excuse|does not excuse|not excuse|not save|of no help|does not lower|cannot rely|cannot take shelter|cannot plead|cannot escape|cannot argue|not protect|no use'),
           's4': _k('chitra liable|chitra is liable|liable to compensate|liable to pay|must compensate|liable for the loss|liable for the ring|bound to compensate|chitra must|chitra has to compensate|chitra responsible',
                    wrong=[{'kw': ['chitra not liable|chitra is not liable|not liable for the loss'], 'say': 'The special condition (bank locker) fixed the care required; breaking it makes Chitra liable even though she lost her own jewellery too.'}]),
           },
    'q2': {'extra_ok': True,
           's1': _k('any purpose|purpose|section 148|delivery', 'security|section 172|debt'),
           's2': _k('bailor and bailee|bailor bailee|bailee bailor', 'pawnor and pawnee|pawnor pawnee|pledgor pledgee|pledgor and pledgee|pawnee pawnor|pledgee pledgor|pawnor pledgor|pledgor pawnor'),
           's3': _k('gratuitous|free of charge|without consideration|need not|gratuitously', 'always|loan'),
           's4': _k('no right to sell|cannot sell|not sell|no right of sale|right to retain|lien|retain', 'sell|sale|section 176|notice'),
           's5': _k('may use|right to use|no right to use|cannot use|not use|use the goods|use goods', 'repayment|repaid|expiry|fulfilment|terminate|terminates|termination|ends on|purpose is over|accomplish', n=1),
           },
    'q3': {'extra_ok': False,
           's1': _k('section 160|return|returned', 'section 161|beyond the proper time|beyond the agreed time|beyond the time|after expiry|after the expiry|after the agreed period|after the period|beyond the period|beyond agreed|beyond the stipulated|after the time|beyond proper time'),
           's2': _k('one week|first week|1 week|7 days|after a week|end of the week', 'default|overstay|kept beyond|beyond|late|delay|wrongfully|three weeks|3 weeks'),
           's3': _k('not caused|not his fault|without negligence|no negligence|even though|even if|irrespective|regardless|not negligent|though|accident|absolute|no fault|whether or not'),
           's4': _k('ehsan liable|ehsan is liable|liable to compensate|liable to pay|liable for the damage|must compensate|bound to compensate|ehsan must|ehsan has to pay|liable for the loss|ehsan responsible|ehsan is responsible|ehsan bears|bear the loss',
                    wrong=[{'kw': ['ehsan not liable|ehsan is not liable|not liable for the damage'], 'say': 'A bailee who keeps goods beyond the agreed time bears any loss after that time, even without his fault (Section 161).'}]),
           },
    'q4': {'extra_ok': False,
           's1': _k('section 170|particular lien|labour or skill|labour|skill', 'retain|lien|keep|hold'),
           's2': _k('general lien|section 171', 'garage not|not available|not entitled|not among|no general lien|only bankers|only to bankers|bankers factors|bankers|wharfinger|cannot claim general|not have general|no such contract|not a banker|banker'),
           's3': _k('not 15000|not for 15000|cannot retain 15000|15000 not|not for the scooter|scooter dues cannot|cannot retain for scooter|not for scooter|separate suit|by suit|15000 by suit|15000 suit|not 57000|cannot 57000|cannot retain for both|not both|not for both|only for 42000|only 42000|42000 only', nums=[42000],
                    wrong=[{'kw': ['57000|retain for both|both amounts are paid'], 'say': 'A particular lien covers only the work done on the goods retained — the car, ₹42,000. The ₹15,000 scooter dues need a separate suit.'}]),
           's4': _k('section 178|mercantile agent', 'consent|possession', 'good faith|bona fide|without notice|no notice', 'ordinary course|normal course|course of business', n=3),
           's5': _k('pledge valid|pledge is valid|pledge binds|binding on indu|binds indu|pledge is binding|indu bound|javed gets good title|javed valid|valid and binding|javed can retain|javed retain|indu cannot recover|pledge good|pledge binding',
                    wrong=[{'kw': ['pledge invalid|pledge is invalid|pledge void|pledge is void|not a valid pledge'], 'say': 'All conditions of Section 178 are met, so the pledge by the mercantile agent binds the owner.'}]),
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
