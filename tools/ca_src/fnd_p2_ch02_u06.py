"""CA Foundation · Paper 2 Business Laws · Chapter 2 The Indian Contract Act, 1872 · Unit 6 Contingent and Quasi Contracts.
Original explanations and problems; sections and leading cases are cited by name only. Sections 31-36 and 68-72."""
from lib import *
from ca_viva import V, P, ALT
from ca_cases import M

UID = 'fnd-p2-ch02-u06'


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
    # ---------- Illustration 3: claim against a minor's estate under Section 68 ----------
    c3 = Checks()
    items = [('Hostel rent for 5 months (₹6,400 a month)', 'Necessary — shelter suited to a student', 6400 * 5, True),
             ('Mess bills', 'Necessary — food', 21500, True),
             ('Prescribed medicines', 'Necessary — health', 4300, True),
             ('Semester textbooks', 'Necessary — education suited to his station', 5800, True),
             ('Gaming console', 'Not a necessary — a luxury', 38000, False),
             ('Designer jacket', 'Not a necessary — beyond his needs', 12500, False)]
    rent = c3.add('6400*5', 'hostel rent for five months')
    nec = c3.add('32000+21500+4300+5800', 'value of necessaries recoverable from the minor\'s property')
    lux = c3.add('38000+12500', 'value of non-necessaries — not recoverable')
    tot3 = c3.add('63600+50500', 'total supplied')
    t3 = table(['Item supplied', 'Nature', 'Amount (₹)', 'Recoverable from property (₹)'],
               [[a, b, x, x if ok else 0] for a, b, x, ok in items] + [['Total', '', tot3, nec]], num=[2, 3], total=True,
               title='Working: claim of Ravi Stores against Kabir (a minor)')

    # ---------- Illustration 4: money paid by mistake (Section 72) ----------
    c4 = Checks()
    due = c4.add('250000*18/100', 'GST actually due at 18%')
    paid = c4.add('250000*28/100', 'amount paid at 28% by mistake')
    refund = c4.add('70000-45000', 'excess to be refunded under Section 72')

    # ---------- Case set numbers ----------
    ck = Checks()
    k_rent = ck.add('12000*3', 'three months of rent paid by the sub-tenant')

    timeline = table(['Type of condition', 'When can it be enforced?', 'When does it become void?', 'Section'], [
        ['Event happens', 'Only after the event has happened', 'When the event becomes impossible', '32'],
        ['Event does not happen', 'When the happening of the event becomes impossible', 'If the event happens', '33'],
        ['Future conduct of a living person', 'Treated as impossible once that person makes it impossible within any definite time', '—', '34'],
        ['Event happens within a fixed time', 'If the event happens within that time', 'If the time runs out without it, or it becomes impossible earlier', '35 (first part)'],
        ['Event does not happen within a fixed time', 'When the time runs out without it, or earlier once it is certain it will not happen', 'If the event happens within the time', '35 (second part)'],
        ['Impossible event', 'Never', 'Void from the start, whether or not the parties knew', '36'],
    ], title='Enforcement rules at a glance')

    quasi = table(['Section', 'Situation', 'Who must pay whom'], [
        ['68', 'Necessaries supplied to a person who cannot contract (minor, person of unsound mind) or to his dependants', 'Supplier is reimbursed out of the incapable person\'s property — no personal liability'],
        ['69', 'A person interested in a payment pays money that another is legally bound to pay', 'The person who was bound to pay reimburses the payer'],
        ['70', 'A person lawfully does something or delivers something, not as a gift, and the other enjoys the benefit', 'The one who benefits pays compensation or returns the thing'],
        ['71', 'A person finds goods belonging to another and takes them into custody', 'Finder has the responsibilities of a bailee'],
        ['72', 'Money paid or a thing delivered by mistake or under coercion', 'Receiver must repay or return it'],
    ], title='The five quasi-contracts in the Act')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch02', 'n': 6, 'title': 'Contingent and Quasi Contracts',
        'outcomes': ['Define a contingent contract (Section 31), list its essentials and tell it apart from an absolute contract and from a wagering agreement.',
                     'Apply the enforcement rules of Sections 32 to 36 to dated fact situations, including events tied to a fixed time and events that are impossible.',
                     'Explain why the law creates quasi-contractual obligations and state the five situations in Sections 68 to 72 with their conditions.',
                     'Solve problem questions on contingent and quasi contracts in the Provision → Facts → Analysis → Conclusion format, computing the amount recoverable where needed.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 45}, 'prereq': ['fnd-p2-ch02-u01', 'fnd-p2-ch02-u05'],
                 'exam_tip': 'Section 68 (necessaries to a minor or a person of unsound mind), Section 70 (non-gratuitous act) and Section 72 (payment by mistake) are favourite 4-mark problems. Always say whose property is liable and how much is recoverable.'},
        'concepts': [
            {'id': 'c1', 'title': 'Absolute and contingent contracts (Section 31)',
             'body': ['An absolute contract must be performed in all events — the promisor\'s duty does not hang on anything outside the bargain. A contingent contract is different: under Section 31 the promisor agrees to do (or not to do) something only if some outside (collateral) event occurs or fails to occur.',
                      'Insurance, indemnity and guarantee are common contingent contracts: the insurer pays only if the loss occurs; the surety pays only if the debtor defaults.',
                      'A "collateral" event is one that is outside the core bargain — it is not itself something either party has promised to perform, nor is it the price paid for the promise. If a buyer agrees to pay only after the seller delivers, delivery is the seller\'s own promised performance, so the deal is an ordinary conditional contract, not a contingent one.'],
             'analogy': 'An absolute contract is a train that leaves on time whatever happens. A contingent contract is a train that leaves only if a signal outside the train turns green.',
             'work': 'Share-purchase deals and loan sanctions are often "subject to" regulatory approval or a bank loan. A CA reviewing such a deal checks whether the condition is a true collateral event, because no obligation (and no liability to record) arises until it is met.'},
            {'id': 'c2', 'title': 'Essentials of a contingent contract',
             'body': ['(1) Performance depends on an event happening or not happening — the condition may be precedent (must occur first) or subsequent. (2) The event is collateral to the contract. (3) The event is uncertain — if it is bound to happen, the contract is simply one to be performed at a future date. (4) The event must not be the mere will or wish of the promisor.',
                      'On point (4): "I will pay you ₹50,000 if I feel like it" creates no obligation at all. But an event that is partly within the promisor\'s control and partly not (for example, "if I travel to Pune and it rains there on 1 July") can still be a contingent event.',
                      'A contingent contract is a valid contract. Its enforcement simply waits for the condition.'],
             'analogy': 'Think of a checklist: future? uncertain? outside the main bargain? not just the promisor\'s whim? Four ticks make it contingent.',
             'work': 'When auditors see a "contingent consideration" clause in an acquisition agreement, the first question is exactly this: what is the event, is it uncertain, and who controls it?'},
            {'id': 'c3', 'title': 'Rules of enforcement (Sections 32 to 36)',
             'body': ['Section 32 — contingent on an event happening: cannot be enforced until the event has happened; if the event becomes impossible, the contract becomes void.',
                      'Section 33 — contingent on an event not happening: becomes enforceable only once it is impossible for the event to occur — not earlier.',
                      'Section 34 — where the event is how a living person will act at an unspecified time, the event is treated as impossible once that person does something that makes it impossible for him to act so within any definite time, or except under further contingencies (for example, the person marries someone else).',
                      'Section 35 — fixed time: if the event must happen within a fixed time, the contract becomes void when the time expires without it or when it becomes impossible earlier. If the event must not happen within a fixed time, the contract can be enforced once the time expires without it, or earlier once it becomes certain it will not happen.',
                      'Section 36 — a contingent agreement to do something if an impossible event happens is void, whether or not the parties knew of the impossibility when they made it.'],
             'blocks': [timeline],
             'analogy': '"Happen" contracts wait for a yes; "not happen" contracts wait until a yes is no longer possible.',
             'work': 'In practice these rules decide the date on which an obligation becomes enforceable — which matters for limitation periods, provisioning and disclosure of contingent liabilities.'},
            {'id': 'c4', 'title': 'Contingent contract vs wagering agreement',
             'body': ['A wagering agreement is a promise to pay money or money\'s worth depending on an uncertain event, where neither side has any real interest in the event except winning or losing the bet. Section 30 makes such agreements void.',
                      'Key differences: a wager always consists of reciprocal promises (each side promises to pay if it loses), a contingent contract need not; in a wager the uncertain event is the whole point, in a contingent contract it is collateral; the parties to a contingent contract have a real interest in the subject matter, wagering parties have none; and a contingent contract is valid while a wager is void.',
                      'Every wager is contingent in nature, but not every contingent contract is a wager — insurance is the classic contingent contract that is not a wager, because the insured has an insurable interest.'],
             'analogy': 'Insurance protects something you own; a bet only gives you something to lose.',
             'work': 'Derivative and incentive structures are sometimes challenged as "wagers". The CA\'s analysis turns on whether the parties have a genuine commercial interest in the underlying event.'},
            {'id': 'c5', 'title': 'Quasi contracts — meaning and features',
             'body': ['Sometimes the law imposes an obligation as if there were a contract, though there was no offer, acceptance or consent. These are quasi contracts — the Act calls them "certain relations resembling those created by contract" (Sections 68 to 72). They rest on equity and on the idea that no one should be unjustly enriched at another\'s expense.',
                      'Features: (1) the right is usually a right to receive money; (2) it arises by operation of law, not by agreement; (3) it is available against a particular person, not against the whole world; (4) the person entitled may sue as if a contract existed.',
                      'Under the last paragraph of Section 73, a person who fails to discharge an obligation resembling a contractual one must compensate the other party in the same way as for a breach of contract.'],
             'blocks': [quasi],
             'analogy': 'A quasi contract is the law writing a contract on behalf of parties who never wrote one, so that fairness is done.',
             'work': 'Excess payments to vendors, amounts collected by mistake, and payments made to protect one\'s own property are all recovered on quasi-contract principles. CAs identify them during reconciliations and recovery reviews.'},
            {'id': 'c6', 'title': 'Necessaries and payments by an interested person (Sections 68 and 69)',
             'body': ['Section 68: if a person who cannot contract (a minor or a person of unsound mind), or someone he is legally bound to support, receives necessaries suited to his condition in life, the supplier can be reimbursed from the property of the incapable person. There is no personal liability — only his property is answerable.',
                      'The supplier must prove that (i) the goods or services were necessaries suited to that person\'s station in life, and (ii) the person was not already adequately supplied at the time. Luxuries are not covered.',
                      'Section 69: a person who has an interest in seeing a payment made, and who pays money that someone else is legally bound to pay, is entitled to be reimbursed by that other person. The payer must not be a volunteer — he must pay to protect his own interest — and the other person must have been bound by law to pay.'],
             'analogy': 'Section 68 is like a canteen that feeds a child on credit: the bill is settled out of the child\'s own savings, never from his future pocket money.',
             'work': 'A tenant who pays the landlord\'s overdue municipal tax to stop the property being attached can recover it from the landlord (or adjust it, if the lease allows). CAs see this regularly in property and estate matters.'},
            {'id': 'c7', 'title': 'Non-gratuitous acts, finder of goods, mistake and coercion (Sections 70 to 72)',
             'body': ['Section 70: if a person lawfully does something for another, or delivers something to him, not intending it as a gift, and the other enjoys the benefit, the other must pay compensation or return the thing. Three conditions: the act was lawful; it was not meant to be gratuitous; and the other person enjoyed the benefit (he had the option of refusing it). In State of West Bengal v. B.K. Mondal and Sons, the State was held liable to pay for work done by a contractor and accepted by it, even though the formal contract requirements were not met.',
                      'Section 71: someone who picks up goods that belong to somebody else and keeps them in his possession carries the responsibility of a bailee — he must take reasonable care, must not use them as his own, and must try to trace and return them to the owner.',
                      'Section 72: whoever receives money or goods because of a mistake or coercion has to give it back. The mistake may be one of fact or of law — in Sales Tax Officer v. Kanhaiya Lal Mukundlal Saraf, tax paid under a mistake of law was held recoverable. "Coercion" here is read widely, beyond the narrow definition in Section 15.'],
             'analogy': 'If the courier drops your neighbour\'s parcel at your door and you open it and use it, you pay for it — the law will not let a mistake become your gift.',
             'work': 'Excess tax deposits, duplicate payments to suppliers and wrong bank credits are recovered under Section 72. Auditors also check that a company is not quietly retaining money credited to it by mistake.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'A purchase that depends on a bank loan', 'difficulty': 'core', 'minutes': 6,
             'q': 'Neha agrees to buy Arjun\'s office unit for ₹80,00,000 "provided the bank sanctions a loan of ₹60,00,000 to me by 31 August". On 20 August the bank formally rejects her application. Arjun says Neha must still buy the unit. Advise Neha.',
             'solution': [legal('Section 31: a contract to do something if a collateral event happens is a contingent contract. Section 35 (first part): a contract contingent on an event happening within a fixed time becomes void if the event becomes impossible before that time, or if the time expires without the event.',
                                'Neha\'s promise to buy depends on the bank sanctioning a loan by 31 August. The bank rejected the loan on 20 August.',
                                'The loan sanction is an uncertain event outside the core bargain, so the contract is contingent. Once the bank rejected the application, the event could no longer happen within the fixed time.',
                                'The contract became void on 20 August. Neha is not bound to buy the office unit, and Arjun cannot enforce the sale.')]},
            {'id': 'i2', 'title': 'Contingent on a ship not returning', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'Kiran promises to pay Dev ₹3,00,000 if the vessel MV Sagar does not return to Kochi port before 31 December. (a) On 10 October the vessel is lost at sea. Can Dev demand payment immediately? (b) Would your answer differ if the vessel safely reached Kochi on 15 November?',
             'solution': [legal('Section 35 (second part): a contract contingent on an event not happening within a fixed time can be enforced when the time expires without the event, or before that time if it becomes certain that the event will not happen. If the event happens within the time, the contract becomes void.',
                                'The promise depends on the vessel not returning before 31 December. In (a) the vessel is lost on 10 October; in (b) it returns on 15 November.',
                                '(a) Once the vessel is lost, it is certain that it cannot return before 31 December, so Dev need not wait for that date. (b) The vessel returned within the fixed time, so the event on which the promise depended can no longer occur.',
                                '(a) Dev can enforce payment of ₹3,00,000 from 10 October. (b) The contract becomes void and Dev can claim nothing.')]},
            {'id': 'i3', 'title': 'Necessaries supplied to a minor — how much can be recovered?', 'difficulty': 'moderate', 'minutes': 9,
             'q': 'Kabir, aged 17, lives in a college hostel. Over five months Ravi Stores supplies him the items below on credit and Kabir does not pay. Kabir owns a fixed deposit inherited from his grandfather. Ravi sues Kabir personally for the full amount. Advise Ravi, showing how much is recoverable and from what.',
             'given': [table(['Item', 'Amount (₹)'], [[a, x] for a, _, x, _ in items], num=[1])],
             'solution': [legal('Section 68: a person who supplies necessaries suited to the condition in life of a person incapable of contracting (such as a minor) is entitled to be reimbursed from the property of that person. The minor is not personally liable, and goods that are not necessaries cannot be claimed.',
                                f'Kabir is a minor. Ravi supplied rent, food, medicines and textbooks worth {R(nec)}, and luxury items worth {R(lux)}. Kabir has property in the form of a fixed deposit.',
                                f'Hostel rent, food, medicines and textbooks are necessaries suited to a student\'s life. The gaming console and designer jacket are luxuries. Ravi\'s claim survives only for the necessaries, and only against Kabir\'s property — not against Kabir personally.',
                                f'Ravi can recover {R(nec)} out of Kabir\'s fixed deposit. He cannot recover {R(lux)} for the luxury items, and he cannot hold Kabir personally liable for any amount.'),
                          t3],
             'checks': c3},
            {'id': 'i4', 'title': 'Tax paid at the wrong rate', 'difficulty': 'moderate', 'minutes': 6,
             'q': 'Sunrise Traders paid tax of ₹70,000 on a transaction value of ₹2,50,000, applying a rate of 28%. The correct rate was 18%. Can it recover the excess, and how much? (Ignore any procedure under the tax law; answer under the Contract Act.)',
             'solution': [legal('Section 72: whoever receives a payment by mistake must give it back. A mistake of law is covered as well as a mistake of fact (Sales Tax Officer v. Kanhaiya Lal Mukundlal Saraf).',
                                f'Tax due at 18% on {R(250000)} = {R(due)}. Tax paid at 28% = {R(paid)}.',
                                f'The excess of {R(paid)} − {R(due)} = {R(refund)} was paid only because of a mistake about the applicable rate. The receiver has no right to keep it.',
                                f'Sunrise Traders can recover {R(refund)} under Section 72.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Is this a contingent liability?', 'role': 'CA in industry (financial controller)', 'situation': 'Your company has agreed to pay a consultant a success fee of ₹15,00,000 "if the State Government approves our new plant before 31 March". Approval is still pending at the year end.',
             'steps': ['Identify the event: government approval within a fixed time — uncertain and outside the company\'s control, so the agreement is a contingent contract (Section 31).', 'Under Section 35 the fee becomes payable only if approval comes before 31 March; if the date passes without approval, the promise is void.',
                       'At the reporting date no present obligation exists, so the fee is evaluated for disclosure as a contingent liability rather than booked as an expense.', 'Track the approval date: if approval is received before 31 March, recognise the liability in that period.'],
             'takeaway': 'Contract law tells you when an obligation is born; accounting then tells you how to show it.', 'think': 'What happens to the success fee if the approval is granted on 5 April?',
             'answer': 'The event had to happen within a fixed time. Once 31 March passes without approval, the contract becomes void under Section 35, so a 5 April approval does not revive the fee (unless the parties make a fresh agreement).'},
            {'id': 'j2', 'title': 'Duplicate payment to a vendor', 'role': 'Articled assistant in an internal audit', 'situation': 'While reconciling a vendor ledger you find the same invoice of ₹2,36,000 was paid twice, a month apart. The vendor has not refunded it.',
             'steps': ['Confirm the duplication from the bank statement and the invoice number.', 'Section 72 obliges the vendor to repay money received by mistake; no separate agreement is needed.', 'Draft a recovery letter quoting the payment details, and propose adjustment against the next invoice if the vendor relationship continues.', 'Recommend a control: block duplicate invoice numbers in the payment system.'],
             'takeaway': 'A mistaken payment does not become the vendor\'s money — the law creates an obligation to refund.', 'think': 'Does it matter that the mistake was the company\'s own carelessness?',
             'answer': 'No. Section 72 applies to any payment made by mistake; the payer\'s negligence does not give the receiver a right to keep it.'},
            {'id': 'j3', 'title': 'Paying the landlord\'s dues to save the lease', 'role': 'CA advising a retail client', 'situation': 'Your client runs a shop on leased premises. The landlord has not paid property tax of ₹1,80,000, and the municipality has issued a notice to seal the building. The client pays the tax to keep trading.',
             'steps': ['Check that the landlord was legally bound to pay the tax and that the client paid to protect its own interest (its business would be sealed).', 'Section 69 entitles the client to be reimbursed by the landlord.', 'Write to the landlord claiming reimbursement or set-off against future rent, attaching the municipal receipt.'],
             'takeaway': 'A payment made to protect your own interest, of a debt someone else owed by law, is recoverable from that person.', 'think': 'Would the client recover if it had paid the landlord\'s personal income tax out of goodwill?',
             'answer': 'No. The client had no interest to protect in that payment; it would be a voluntary payment, and Section 69 would not apply.'},
        ],
        'mcqs': [
            MC('m1', 'A contract under which a party must act (or refrain from acting) only if an uncertain collateral event occurs or does not occur is a:', ['Contingent contract', 'Wagering agreement', 'Quasi contract', 'Void agreement'], 0, 'This is the definition in Section 31.', 'c1'),
            MC('m2', 'Which of the following is NOT an essential of a contingent contract?', ['There must be reciprocal promises', 'The event must be uncertain', 'The event must be collateral to the contract', 'The event must not be the mere will of the promisor'], 0, 'Reciprocal promises are a feature of a wager. A contingent contract may be one-sided, like insurance.', 'c2'),
            MC('m3', 'A contract of fire insurance is an example of a:', ['Contingent contract', 'Wagering agreement', 'Quasi contract', 'Void agreement'], 0, 'The insurer pays only if the fire (an uncertain collateral event) occurs, and the insured has an insurable interest — so it is contingent, not a wager.', 'c4'),
            MC('m4', 'Under Section 32, a contract contingent on the happening of an uncertain future event:', ['Cannot be enforced until the event happens, and becomes void if the event becomes impossible', 'Can be enforced immediately', 'Can be enforced when the event becomes impossible', 'Is void from the beginning'], 0, 'Section 32 — enforcement waits for the event; impossibility makes the contract void.', 'c3'),
            MC('m5', 'Tara promises to pay Ishan ₹1,00,000 if a particular cargo ship does not return. The ship sinks. The contract:', ['Becomes enforceable now', 'Becomes void', 'Can be enforced only after one year', 'Was void from the start'], 0, 'Section 33: a contract contingent on an event not happening is enforceable once the happening becomes impossible — the sinking makes the return impossible.', 'c3', 'moderate'),
            MC('m6', 'Ajay agrees to pay Bela ₹50,000 if the sun rises in the west tomorrow. The agreement is:', ['Void under Section 36', 'A valid contingent contract', 'Voidable at Bela\'s option', 'A quasi contract'], 0, 'Contingent agreements on impossible events are void, whether or not the parties knew of the impossibility.', 'c3'),
            MC('m7', 'Wagering agreements are:', ['Void', 'Voidable', 'Valid', 'Illegal and punishable in every case'], 0, 'Section 30 declares wagering agreements void. They are not illegal in general (except where a specific law makes them so), so collateral transactions are not necessarily tainted.', 'c4'),
            MC('m8', 'Which statement about quasi contracts is INCORRECT?', ['They are created voluntarily by the parties', 'They are imposed by law', 'They rest on the principle against unjust enrichment', 'The right is usually a right to money'], 0, 'Quasi-contractual obligations arise by operation of law, not by agreement.', 'c5'),
            MC('m9', 'Necessaries supplied to a person of unsound mind can be recovered:', ['Only from his property', 'From him personally', 'From his relatives personally', 'Not at all'], 0, 'Section 68 gives reimbursement out of the incapable person\'s property only.', 'c6'),
            MC('m10', 'A finder of lost goods who takes them into custody has the responsibility of a:', ['Bailee', 'Owner', 'Insurer', 'Agent'], 0, 'Section 71 places the finder in the position of a bailee.', 'c7'),
            MC('m11', 'A food delivery is wrongly handed to Mr. Paul, who knows it is not his order and eats it. Under which section must he pay?', ['Section 70 — enjoying the benefit of a non-gratuitous act', 'Section 68 — necessaries to an incapable person', 'Section 69 — payment by an interested person', 'Section 71 — finder of goods'], 0, 'The food was delivered lawfully, not as a gift, and Mr. Paul enjoyed it — the three conditions of Section 70.', 'c7', 'moderate'),
            MC('m12', 'Money paid under a mistake of law:', ['Is recoverable under Section 72', 'Is never recoverable', 'Is recoverable only if the mistake is of foreign law', 'Is recoverable only if both parties were mistaken'], 0, 'Section 72 covers any mistake; the Supreme Court allowed recovery of tax paid under a mistake of law (Sales Tax Officer v. Kanhaiya Lal Mukundlal Saraf).', 'c7', 'moderate'),
            MC('m13', 'Megha promises Rohan ₹2,00,000 "if Rohan marries Simran". Simran marries Vikram. Under Section 34 the event is treated as:', ['Impossible, so the contract becomes void', 'Still possible, so Rohan must wait', 'Happened, so payment is due', 'Irrelevant to the contract'], 0, 'Where the event depends on how a living person will act at an unspecified time, it is treated as impossible once that person makes it impossible within any definite time.', 'c3', 'moderate'),
            MC('m14', 'A tenant pays the landlord\'s overdue municipal tax to stop the building from being sealed. He can recover it from the landlord under:', ['Section 69', 'Section 70', 'Section 72', 'Section 68'], 0, 'He was interested in the payment (to protect his tenancy), and the landlord was bound by law to pay.', 'c6'),
        ],
        'questions': [
            Q('q1', 4, 'moderate', 'legal',
              'Dhruv, a minor, lives with his widowed mother. Shreya, a tailor, stitches school uniforms worth ₹9,000 and two party suits worth ₹26,000 for him on credit. Dhruv owns a house inherited from his father. Shreya sues Dhruv for ₹35,000. Decide, with reference to the Indian Contract Act, 1872.',
              [legal('Section 68: where a person incapable of contracting is supplied with necessaries suited to his condition in life, the supplier may be repaid out of that person\'s property. The incapable person is not personally liable, and only necessaries are covered.',
                     'Dhruv is a minor. Shreya supplied school uniforms worth ₹9,000 and party suits worth ₹26,000. Dhruv owns inherited property.',
                     'School uniforms are necessaries for a school-going child. Two party suits are not necessaries suited to his actual needs. Shreya can claim only for the uniforms, and only out of Dhruv\'s property.',
                     'Shreya can recover ₹9,000 from Dhruv\'s property (the house). She cannot recover ₹26,000 for the party suits, and Dhruv is not personally liable.')],
              [('Section 68 stated correctly — reimbursement from property, not personal liability', 1.5, 'provision'), ('Identifies necessaries vs non-necessaries', 1, 'analysis'),
               ('Amount recoverable ₹9,000 computed', 0.5, 'computation'), ('Conclusion: recover from property only; suits not recoverable', 1, 'conclusion')],
              ['Good answers separate the items and state the amount; weak answers say "the minor\'s agreement is void, so nothing can be recovered".', 'Quoting "Section 68" and the words "from his property" earns most of the provision marks.'],
              ['Holding the minor personally liable.', 'Allowing recovery for luxuries.', 'Treating the case under minors\' contracts (void ab initio) and stopping there.'],
              ['List the items and mark each as necessary or not.', 'End with the figure and the source of recovery: "₹9,000 out of Dhruv\'s property".'],
              checks=[{'expr': '9000+26000', 'value': 35000, 'label': 'total claim'}]),
            Q('q2', 5, 'moderate', 'table',
              'Distinguish between a contingent contract and a wagering agreement. (Any five points)',
              [table(['Basis', 'Contingent contract', 'Wagering agreement'], [
                  ['Meaning', 'A contract to do or not do something if a collateral event happens or does not happen (Section 31)', 'A promise to pay money or money\'s worth on the outcome of an uncertain event, in which the parties have no other interest'],
                  ['Reciprocal promises', 'Need not contain reciprocal promises', 'Always reciprocal — each side promises to pay if it loses'],
                  ['Role of the event', 'Collateral to the main bargain', 'The uncertain event is the whole substance of the agreement'],
                  ['Interest of parties', 'Parties have a real interest in the subject matter (e.g. insurable interest)', 'No interest except winning or losing'],
                  ['Nature', 'May or may not be wagering in nature', 'Is always contingent in nature'],
                  ['Validity', 'Valid and enforceable when the condition is met', 'Void under Section 30'],
              ])],
              [('Meaning of both', 1, 'concept'), ('Reciprocal promises', 1, 'concept'), ('Nature of the event / interest of parties', 1, 'analysis'), ('Relationship (every wager is contingent, not vice versa)', 1, 'analysis'), ('Validity — valid vs void (Section 30)', 1, 'provision')],
              ['A neat table with five bases scores full marks quickly; long paragraphs lose time.', 'The validity point must mention Section 30.'],
              ['Saying wagering agreements are "illegal" rather than void.', 'Calling insurance a wager.'],
              ['Use one line per cell.', 'Lead with the meaning, end with validity.']),
            Q('q3', 4, 'moderate', 'legal',
              'Manav finds a gold chain on a bus and keeps it at home. He makes no effort to trace the owner. A month later he wears it to a wedding and the clasp breaks. The owner, Leela, traces the chain to him and claims damages for the broken clasp. Is Manav liable? State the duties of a finder of goods.',
              [legal('Section 71: someone who picks up goods that belong to somebody else and keeps them in his possession carries the responsibility of a bailee. He must take the care a person of ordinary prudence would take of his own goods, must not use them for himself, and must make reasonable efforts to find the owner and return them.',
                     'Manav found and kept the chain, made no effort to trace Leela, and wore it, which caused the clasp to break.',
                     'By taking the chain into custody Manav became responsible like a bailee. Using the chain for himself was unauthorised use, and he also failed in his duty to look for the owner. The damage arose from that use.',
                     'Manav is liable to return the chain and compensate Leela for the broken clasp.')],
              [('Section 71 — finder treated as bailee', 1, 'provision'), ('Duties: care, no personal use, trace the owner and return', 1.5, 'provision'), ('Applies: unauthorised use, no effort to trace', 0.5, 'analysis'), ('Conclusion: liable to return and compensate', 1, 'conclusion')],
              ['Candidates who list the three duties and then apply them score well.'],
              ['Saying "finders keepers" or treating the finder as the owner.', 'Forgetting the duty to trace the owner.'],
              ['Write the duties as a short list inside your provision paragraph.']),
            Q('q4', 6, 'hard', 'legal',
              'Answer the following with reasons under the Indian Contract Act, 1872: (a) Asha promises to pay Bimal ₹1,00,000 if it rains in Jaipur on 1 June and Bimal reaches Jaipur that day. Is this a contingent contract? (3 marks) (b) Chirag, a contractor, by mistake renovates the house of Deepa, believing it to be the house of his client next door. Deepa was away and returns to find the renovation complete. Must she pay Chirag? (3 marks)',
              [p('(a)'), legal('Section 31: a contingent contract depends on a collateral event that is uncertain. The event must not be merely the will of the promisor, though an event partly within a party\'s control may still be contingent.',
                               'Payment depends on rain in Jaipur on 1 June and on Bimal being there.',
                               'Rain is uncertain and outside both parties\' control. Bimal\'s travel is within his control, but the event as a whole is not merely the will of the promisor (Asha). It is collateral to the promise to pay.',
                               'Yes, it is a contingent contract; Asha must pay only if both conditions are fulfilled.'),
               p('(b)'), legal('Section 70: a person must pay for a thing done for him only if it was done lawfully, not intending to do so gratuitously, and he enjoyed the benefit of it — that is, he had the choice to accept or reject it.',
                               'Chirag renovated Deepa\'s house by mistake while she was away. She had no say in the work.',
                               'Chirag did not intend a gift, but Deepa had no opportunity to accept or refuse the work; the benefit was thrust upon her. Liability under Section 70 requires voluntary acceptance of the benefit.',
                               'Deepa is not bound to pay for the renovation under Section 70.')],
              [('(a) Section 31 and the essentials', 1, 'provision'), ('(a) Analysis of "not mere will" and uncertainty', 1, 'analysis'), ('(a) Conclusion', 1, 'conclusion'),
               ('(b) Section 70 with three conditions', 1, 'provision'), ('(b) Analysis — no choice to accept, benefit not voluntarily enjoyed', 1, 'analysis'), ('(b) Conclusion', 1, 'conclusion')],
              ['In (b) many candidates jump to "she enjoyed the benefit so must pay". Examiners reward the point that enjoyment must be voluntary — she must have been able to reject it.'],
              ['Treating every benefit received as attracting Section 70.', 'In (a), calling it "not contingent because travel is within Bimal\'s will".'],
              ['Label sub-parts clearly and give each its own four-step answer.']),
        ],
        'revision': {'summary': ['Contingent contract (Section 31): promise depends on an uncertain, collateral, future event that is not merely the promisor\'s will. Insurance, indemnity and guarantee are examples. It is valid.',
                                 'Section 32: "happen" contracts — enforce only after the event; void if it becomes impossible. Section 33: "not happen" contracts — enforce once the event becomes impossible.',
                                 'Section 34: event depending on a living person\'s conduct is impossible once he makes it so. Section 35: fixed-time events. Section 36: impossible events — void.',
                                 'Wager (Section 30) = void; reciprocal promises, no interest except winning; every wager is contingent but not vice versa.',
                                 'Quasi contracts (Sections 68–72): imposed by law to prevent unjust enrichment — necessaries, interested-person payment, non-gratuitous act, finder of goods, mistake or coercion.'],
                     'remember': ['Section 68: recover from the PROPERTY of a minor or person of unsound mind — necessaries only.', 'Section 70: lawful act + not gratuitous + benefit enjoyed (with a choice to refuse).', 'Section 72: mistake of fact or law, and coercion in a wide sense — repay or return.', 'Section 73 (last paragraph): breach of a quasi-contractual obligation is compensated like a breach of contract.'],
                     'traps': ['Do not call a contingent contract void or voidable — it is valid.', 'Do not mix up Sections 32 and 33: "happen" waits for the event; "not happen" waits for impossibility.', 'Do not make a minor personally liable for necessaries.', 'Do not treat a thrust-upon benefit as "enjoyed" under Section 70.']},
        'quickref': [{'k': 'Section 30', 'v': 'Wagering agreements are void'}, {'k': 'Section 31', 'v': 'Contingent contract — promise depends on a collateral event happening or not happening'},
                     {'k': 'Section 32', 'v': 'Event happening — enforce after it happens; void if impossible'}, {'k': 'Section 33', 'v': 'Event not happening — enforce when happening becomes impossible'},
                     {'k': 'Section 34', 'v': 'Conduct of a living person — impossible once he makes it impossible'}, {'k': 'Section 35', 'v': 'Fixed-time events (happen within time / not happen within time)'},
                     {'k': 'Section 36', 'v': 'Agreement contingent on an impossible event is void'}, {'k': 'Section 68', 'v': 'Necessaries to an incapable person — from his property'},
                     {'k': 'Section 69', 'v': 'Interested person paying another\'s legal dues — reimbursed'}, {'k': 'Section 70', 'v': 'Non-gratuitous lawful act, benefit enjoyed — pay or return'},
                     {'k': 'Section 71', 'v': 'Finder of goods = bailee\'s responsibility'}, {'k': 'Section 72', 'v': 'Money/thing delivered by mistake or coercion — repay/return'}],
        'viva': [
            V('v1', 'What is a contingent contract? State its essentials.',
              'A contingent contract under Section 31 is one in which a party promises to do or refrain from doing something only if some collateral event happens or fails to happen. Its essentials are: performance depends on a future event, the event is uncertain, the event is collateral to the contract, and the event is not merely the will of the promisor.',
              [P('p1', 'Promise depends on an event happening or not happening (Section 31)', 3, 'happen|occur|section 31|31', 'depend|condition|if|contingent', min=2),
               P('p2', 'The event is uncertain', 2, 'uncertain|not certain|not sure|may or may not'),
               P('p3', 'The event is collateral to the contract', 3, 'collateral|outside the contract|not part of the contract|incidental|independent'),
               P('p4', 'Not the mere will of the promisor', 2, 'not mere will|not merely the will|not just the will|not only the will|not merely will|not mere wish|not merely wish|not at the will|not depend on the will|not his own will|not dependent on will|not discretion|not the will|not merely on will|not whim')], 'c2'),
            V('v2', 'Explain the rules in Sections 32 and 33 for enforcing contingent contracts.',
              'Under Section 32, a contract contingent on an event happening cannot be enforced until the event happens, and it becomes void if the event becomes impossible. Under Section 33, a contract contingent on an event not happening becomes enforceable only when it is impossible for that event to happen.',
              [P('p1', 'Section 32: "happening" contract enforced only after the event happens', 4,
                 ALT('happen {e} until {h}', 'happen {e} after {h}', 'happen {e} when {h}', 'happen {e} only when {h}', 'happen {e} once {h}', 'happen not {e} until {h}', 'happen cannot {e} until {h}', 'happen not {e} unless {h}', 'happen cannot {e} unless {h}', 'happen wait {h}', 'section 32 {e} after {h}', 'section 32 {e} when {h}', 'section 32 {e} until {h}', 'section 32 {e} once {h}', 'section 32 not {e} until {h}', 'section 32 cannot {e} until {h}', e=('enforc', 'enforced', 'enforceable', 'sued', 'sue', 'claim'), h=('happen', 'event happen', 'occur', 'event occur'))),
               P('p2', 'Section 32: becomes void if the event becomes impossible', 2, 'void', 'impossible'),
               P('p3', 'Section 33: "not happening" contract enforced when the happening becomes impossible', 4,
                 ALT('not happen {e} when {i}', 'not happen {e} only when {i}', 'not happen {e} once {i}', 'not happen {e} after {i}', 'not happen {e} {i}', 'not occur {e} when {i}', 'not occur {e} once {i}', 'section 33 {e} when {i}', 'section 33 {e} only when {i}', 'section 33 {e} once {i}', 'section 33 {e} {i}', e=('enforc', 'enforced', 'enforceable', 'sued', 'sue', 'claim'), i=('impossible', 'happen impossible', 'happening becomes impossible', 'event becomes impossible', 'cannot happen', 'no longer possible')))], 'c3'),
            V('v3', 'How does a contingent contract differ from a wagering agreement?',
              'A wagering agreement is void under Section 30, while a contingent contract is valid. A wager always has reciprocal promises and the parties have no interest except winning or losing, whereas in a contingent contract the parties have a real interest and the event is only collateral. Every wager is contingent, but every contingent contract is not a wager — insurance is an example.',
              [P('p1', 'Wager void (Section 30); contingent contract valid', 4, ALT('wager {v}', 'wagering {v}', 'bet {v}', 'section 30 {v}', v=('void', 'is void', 'not valid', 'unenforceable', 'not enforceable')), 'contingent contract valid|contingent valid|contingent is valid|contingent contract is valid|contingent contract enforceable|contingent enforceable|contingent contract is enforceable'),
               P('p2', 'Wager has reciprocal promises / no interest except winning or losing', 3, 'reciprocal|mutual promise|no interest|not interest|winning|win or lose|gain or lose|losing'),
               P('p3', 'Every wager is contingent, but not every contingent contract is a wager — e.g. insurance', 3, 'insurance|insurable|every wager contingent|all wager contingent|not every contingent|not all contingent|every contingent not|all contingent not')], 'c4'),
            V('v4', 'What are quasi contracts? Name the situations covered by the Contract Act.',
              'Quasi contracts are obligations imposed by law, not created by agreement, to prevent unjust enrichment. The Act covers five: necessaries supplied to a person incapable of contracting, payment by an interested person, benefit of a non-gratuitous act, finder of goods, and money paid by mistake or under coercion.',
              [P('p1', 'Imposed by law, not by agreement', 3, 'imposed by law|created by law|law imposes|operation of law|by law|not by agreement|no agreement|without agreement|not agreement|no contract|not voluntary|not created by the parties'),
               P('p2', 'Based on preventing unjust enrichment / equity', 2, 'unjust|enrich|equity|fairness|good conscience|no one should grow rich|benefit at another'),
               P('p3', 'Situations: necessaries, interested person, non-gratuitous act, finder, mistake or coercion (Sections 68–72)', 5, 'necessar', 'interested', 'gratuitous', 'finder|finds|found|lost goods', 'mistake|coercion', min=4)], 'c5'),
            V('v5', 'A person of unsound mind is supplied necessaries on credit. Can the supplier recover? From whom?',
              'Yes. Under Section 68 the supplier of necessaries suited to the condition in life of a person incapable of contracting can be reimbursed, but only from that person\'s property. He is not personally liable, and luxuries cannot be claimed.',
              [P('p1', 'Yes — recoverable under Section 68', 3, 'yes|can recover|recoverable|reimbursed|section 68|68'),
               P('p2', 'Only from his property — no personal liability', 5, 'only from his property|from his property|out of his property|only from property|from property|property of|his property|estate|assets', 'not personal|no personal|not personally|never personal|not from him personally', min=1),
               P('p3', 'Only necessaries suited to his condition in life, not luxuries', 2, 'suited|suitable|condition in life|station|luxur|not luxury|necessaries only|only necessaries')], 'c6'),
            V('v6', 'State the conditions for a claim under Section 70 of the Contract Act.',
              'Under Section 70 the claimant must show three things: he did the act or delivered the thing lawfully, he did not intend to do it gratuitously, and the other person enjoyed the benefit of it. Then the other person must pay compensation or return the thing.',
              [P('p1', 'Act done or thing delivered lawfully', 3, 'lawful|legal|legally'),
               P('p2', 'Not intended to be gratuitous', 3, 'not gratuitous|not gratuitously|not intend gratuitous|not intend to do it gratuitously|not as a gift|not a gift|not free|not free of charge|non gratuitous|not intending gratuitous|not intending to do so gratuitously|intended to be paid|expect payment|expecting payment'),
               P('p3', 'The other person enjoyed the benefit', 3, 'enjoy|benefit|accepted the benefit|took the benefit|used'),
               P('p4', 'Result: compensate or return the thing', 1, 'compensat|pay|return|restore')], 'c7'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Farhan, the lease and the unpaid tax', 'difficulty': 'hard',
            'case': ('Farhan runs a bakery from premises leased from Gopal at ₹12,000 a month. Gopal has not paid property tax for two years, and the municipality announces that the premises will be sealed. To keep the bakery open, Farhan pays the arrears of ₹36,000 directly to the municipality. The same week, a wholesaler mistakenly delivers 20 trays of eggs meant for the shop next door; Farhan, knowing they were not ordered by him, uses them in his baking. Separately, Gopal had earlier promised Farhan a rent-free month "if the new metro station opens within 500 metres by 31 March"; the metro authority has just cancelled the project.'),
            'mcqs': [
                M('k1a', 'Under which provision can Farhan recover the ₹36,000 paid to the municipality?', ['Section 69 — payment by an interested person', 'Section 70 — non-gratuitous act', 'Section 72 — payment by mistake', 'Section 68 — necessaries'], 0,
                  'Farhan paid a sum Gopal was legally bound to pay, in order to protect his own interest in the lease.', 'moderate'),
                M('k1b', 'How many months of rent does the ₹36,000 represent if Farhan adjusts it against rent?', ['3', '2', '4', '36'], 0,
                  f'₹36,000 ÷ ₹12,000 a month = 3 months ({R(k_rent)} equals three months\' rent).', 'core', '36000/12000'),
                M('k1c', 'Is Farhan liable to pay the wholesaler for the eggs?', ['Yes, under Section 70 — he knowingly used goods delivered non-gratuitously', 'No, because he never ordered them', 'No, because there is no contract with the wholesaler', 'Yes, but only under Section 71 as a finder'], 0,
                  'The delivery was lawful and not intended as a gift, and Farhan chose to use the eggs — all three Section 70 conditions are met.', 'hard'),
                M('k1d', 'What is the status of Gopal\'s promise of a rent-free month?', ['Void — the event can no longer happen within the fixed time (Section 35)', 'Enforceable now', 'Enforceable on 31 March regardless', 'Voidable at Farhan\'s option'], 0,
                  'The promise depended on the metro station opening within a fixed time; once the project was cancelled, the event became impossible, so the contract became void.', 'hard'),
            ]}],
    }


# ---------- teaching explanations + topic tags for every MCQ (override the short drafts above) ----------
TCC, TRE, TQC = 'Contingent Contracts', 'Rules Relating to Enforcement', 'Quasi Contracts'
EXPLAIN = {
    'm1': (TCC, 'Section 31: a contingent contract is one where a party\'s obligation to act or refrain depends on whether some collateral event occurs. The duty to perform depends on an uncertain collateral event. The tempting trap is "wagering agreement" — a wager also turns on an uncertain event, but there the parties have no interest except winning or losing. In practice: insurance policies, performance bonuses tied to targets and success-fee arrangements are all contingent contracts.'),
    'm2': (TCC, 'A contingent contract needs a valid contract, performance depending on an uncertain future event, an event collateral to the contract (not part of the main promise), and an event not left to the mere will of the promisor. Reciprocal promises are not required — a contingent contract may be one-sided, like an insurer\'s promise. The trap is "the event must be collateral", which is in fact essential. In practice: guarantee-like undertakings such as "we will pay if the buyer defaults" are valid contingent contracts.'),
    'm3': (TCC, 'In fire insurance the insurer must pay only if a fire, an uncertain collateral event, occurs, so it is a contingent contract. The insured has an insurable interest in the property and is merely indemnified for the actual loss. The tempting trap is "wagering agreement" — a wager has no interest beyond winning, whereas insurance protects a real interest. In practice: CAs account for insurance claims only when the insured event has occurred and the claim is reasonably certain.'),
    'm4': (TRE, 'Section 32: a contract contingent on an uncertain future event happening cannot be enforced until that event has happened, and it becomes void if the event becomes impossible. The tempting trap is "can be enforced immediately"; the promise is conditional until the event occurs. In practice: a broker\'s commission payable "on registration of the sale deed" cannot be claimed until registration happens, and is lost if the deal collapses for good.'),
    'm5': (TRE, 'Section 33: a contract contingent on an event not happening can be enforced once the happening of that event becomes impossible. Tara\'s promise depended on the ship not returning; once it sank, its return became impossible, so the promise is enforceable now. The tempting trap is "becomes void" — that is the Section 32 rule for events that must happen. In practice: marine insurance claims for total loss become payable once the vessel is confirmed lost.'),
    'm6': (TRE, 'Section 36: an agreement that depends on an impossible event is void, even if the parties did not realise the event was impossible. The sun rising in the west is impossible, so the agreement is void. The tempting trap is "a valid contingent contract" — contingency requires an uncertain event, not an impossible one. In practice: contracts tied to conditions that can never be met give no enforceable rights, so drafters avoid unrealistic conditions.'),
    'm7': (TCC, 'Section 30 declares wagering agreements void — courts will not enforce them, so no suit lies to recover a bet or winnings. They are not illegal in general, except where a specific law prohibits gambling, so related transactions are not automatically tainted. The tempting trap is "illegal and punishable in every case", which overstates the position under the Contract Act. In practice: betting winnings cannot be recovered through courts, while income from lawful gaming is still taxed under the Income-tax Act.'),
    'm8': (TQC, 'Quasi contracts are not created by agreement; the law imposes the obligation to prevent unjust enrichment, as in Sections 68 to 72. They usually give a right to money, often a liquidated sum, and are available against specific persons. So "created voluntarily by the parties" is incorrect. The trap is "the right is usually a right to money", which is a true feature. In practice: when a customer pays twice by mistake, the business must refund the extra under quasi-contract even though there is no agreement to do so.'),
    'm9': (TQC, 'Section 68: a person who supplies necessaries suited to the condition in life of someone incapable of contracting, such as a person of unsound mind, is entitled to reimbursement from that person\'s property. There is no personal liability. The tempting trap is "from him personally"; the claim lies only against his property. Relatives are not liable unless they agreed to pay. In practice: hospitals treating patients lacking mental capacity recover bills from the patient\'s estate managed by a guardian.'),
    'm10': (TQC, 'Section 71: someone who picks up another\'s lost goods and keeps them carries the responsibilities of a bailee. He must take reasonable care, try to find the owner and return the goods. The tempting trap is "owner" — finding does not give ownership as against the true owner. In practice: shops and malls that collect items left by customers must keep them safely and record them in a lost-property register.'),
    'm11': (TQC, 'Section 70 applies when a person lawfully does something for another, not intending to do it gratuitously, and the other enjoys the benefit. The food was delivered lawfully, not as a gift, and Mr. Paul knowingly ate it, so he must pay for it. The tempting trap is "Section 71 — finder of goods"; the food was delivered to him, not found. In practice: a business that knowingly uses goods wrongly delivered to it must pay for them.'),
    'm12': (TQC, 'Section 72: whoever receives money or goods because of a mistake or coercion has to give them back. The Supreme Court held this covers mistakes of law as well as of fact, allowing refund of tax paid under a mistaken view of law (Sales Tax Officer v. Kanhaiya Lal Mukundlal Saraf). The tempting trap is "never recoverable", confusing Section 21 with Section 72. In practice: businesses claim refunds of taxes later found to be wrongly levied.'),
    'm13': (TRE, 'Section 34: where the contingency is how a living person will behave at some unfixed time, the event is treated as impossible once that person\'s own act rules it out for any definite period. Simran marrying Vikram makes the event impossible, so the contract becomes void. The tempting trap is "still possible, so Rohan must wait" — the law does not wait for a possible divorce. In practice: conditional promises based on someone\'s future conduct end when that person acts otherwise.'),
    'm14': (TQC, 'Section 69: someone with an interest in a payment that another person is legally obliged to make can, after paying it, recover the amount from that person. The tenant had an interest in avoiding sealing of his premises, and the landlord was legally bound to pay the municipal tax. The tempting trap is "Section 70" — that covers lawful non-gratuitous acts generally; payment by an interested person is the specific rule. In practice: tenants adjust such payments against rent with proper receipts.'),
    'k1/k1a': (TQC, 'Section 69 applies: Gopal was legally bound to pay the property tax, and Farhan, interested in keeping the bakery premises from being sealed, paid it. So Farhan can recover ₹36,000 from Gopal. The tempting trap is "Section 72 — payment by mistake" — Farhan paid deliberately, knowing exactly why. In practice: a tenant paying a landlord\'s statutory dues keeps the municipal receipt so that the amount can be adjusted against rent.'),
    'k1/k1b': (TQC, 'Months of rent = amount paid ÷ monthly rent = ₹36,000 ÷ ₹12,000 = 3 months. Farhan can adjust the Section 69 reimbursement against three months\' rent. The tempting trap is 36, confusing the number of thousands with the number of months. In practice: when tenants adjust such payments, the accountant records a debit to the landlord\'s account rather than to rent expense, so both books agree.'),
    'k1/k1c': (TQC, 'Section 70 has three conditions: the act was done lawfully, it was not intended to be gratuitous, and the other person enjoyed the benefit. The wholesaler delivered the eggs lawfully and not as a gift, and Farhan knowingly used them, so he must pay. The tempting trap is "no, because there is no contract with the wholesaler" — quasi-contractual liability arises without any contract. In practice: a business receiving goods it did not order should return them or pay if it uses them.'),
    'k1/k1d': (TRE, 'Section 35: a contract contingent on a specified event happening within a fixed time becomes void if the event does not happen in that time, or if it becomes impossible before the time expires. The metro project was cancelled before 31 March, so the event is impossible and the promise is void. The tempting trap is "enforceable on 31 March regardless" — the condition, not the date, decides. In practice: lease incentives tied to future events lapse when those events become impossible.'),
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
           's1': _k('section 68', 'necessaries|necessary|necessities', 'property|estate|reimburse|reimbursed', 'not personally liable|no personal liability|not personally|not liable personally|personally not liable|cannot be personally|not personal', n=3,
                    wrong=[{'kw': ['personally liable|dhruv must pay 35000|liable for 35000'], 'say': 'Section 68 gives only reimbursement out of the minor\'s property, never personal liability — and only for necessaries.'}]),
           's2': _k('uniform necessar|uniforms are necessar|uniforms necessar|necessaries uniforms|uniforms are necessities|uniforms are necessary|necessary uniform', 'suits not|suits are not|suit not|suits luxur|suits are luxur|luxury|luxuries'),
           's3': _k('recover 9000|9000 recoverable|9000 only|only 9000|claim 9000|get 9000|entitled 9000|9000 out of|limited to 9000|reimbursed 9000|entitled to 9000|recovers 9000'),
           's4': _k('dhruv s property|dhruv property|inherited house|dhruv s house|dhruv s estate|out of dhruv|minor s house', 'cannot recover 26000|suits are not recoverable|not liable for the suits|not liable for suits|not 26000|26000 not|suits not recoverable|cannot claim 26000|not recover 26000|not for the suits|suits cannot|26000 cannot|not for suits|nothing for the suits'),
           },
    'q2': {'extra_ok': True,
           's1': _k('collateral|section 31', 'money|stake|win|lose|bet|uncertain'),
           's2': _k('reciprocal', 'need not|not necessarily|not necessary|always|mutual'),
           's3': _k('collateral|incidental', 'interest|insurable|substance|whole|core'),
           's4': _k('always contingent|every wager is contingent|every wagering agreement is contingent|all wagers are contingent|wager contingent|wagers contingent|wagering contingent|wagering agreement contingent', 'may or may not be wagering|may or may not be a wager|not vice versa|not every contingent|not all contingent|not necessarily|need not be wagering|contingent not wager|contingent contract not wager|contingent contracts are not wager|not always wager|not always a wager'),
           's5': _k('wager void|wagering void|wagering agreement void|wagering agreements are void|void section 30|section 30 void|void under section 30|wagers void|wagers are void', 'contingent valid|contingent contract valid|contingent enforceable|valid enforceable|valid and enforceable|contingent contracts are valid|contingent contract is valid'),
           },
    'q3': {'extra_ok': False,
           's1': _k('section 71|finder', 'bailee|responsibility of a bailee|position of bailee|position of a bailee|same responsibility'),
           's2': _k('care|ordinary prudence|prudence|reasonable care', 'not use|no personal use|must not use|should not use|not for his own use|cannot use|refrain from using|not to use|without using|not entitled to use', 'trace|find the owner|search|locate|reasonable efforts|return'),
           's3': _k('wore|wearing|wear|used|unauthorised use|using', 'no effort|not try|did not try|no attempt|failed to trace|didnt trace|never tried|made no|did not trace|no efforts|not trace|not search|not traced'),
           's4': _k('manav liable|manav is liable|liable to compensate|liable to pay|liable for the damage|must compensate|liable to return|must pay|bound to compensate|manav must|liable for damages|liable for the broken|liable to leela', n=1),
           },
    'q4': {'extra_ok': False,
           's1': _k('section 31|collateral', 'uncertain|contingent', 'will of the promisor|mere will|promisor s will|not merely|collateral', n=2),
           's2': _k('rain', 'uncertain|beyond control|outside|not within|no control|not in control', 'not merely|not mere|not solely|not entirely|partly|not only|not purely|not just'),
           's3': _k('yes contingent|contract contingent|agreement contingent|qualifies contingent|only if both|pay only if|amounts to contingent|becomes contingent|constitutes contingent|valid contingent|hence contingent|therefore contingent|thus contingent'),
           's4': _k('section 70', 'lawful|lawfully', 'gratuitous|gratuitously|free|gift', 'enjoy|enjoyed|benefit|accept|accepted', n=3),
           's5': _k('no choice|no opportunity|no option|could not accept|could not reject|not voluntarily|thrust|forced|without her consent|no say|did not ask|not request|no chance|unable to reject|not given a chance|not an option|chance to reject|option to reject|not asked|not choose'),
           's6': _k('deepa not bound|deepa is not bound|deepa need not pay|not bound to pay|not liable to pay|need not pay|deepa not liable|deepa is not liable|deepa does not have to pay|chirag cannot recover|chirag cannot claim|no obligation to pay|not required to pay|deepa not required|not obliged to pay|deepa need not'),
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
