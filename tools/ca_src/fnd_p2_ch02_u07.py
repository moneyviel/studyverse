"""CA Foundation · Paper 2 Business Laws · Chapter 2 The Indian Contract Act, 1872 · Unit 7 Contract of Indemnity and Guarantee.
Original explanations and problems; Sections 124-147 cited by number, leading cases by name only. Co-surety shares are computed."""
from lib import *
from ca_viva import V, P, ALT
from ca_cases import M

UID = 'fnd-p2-ch02-u07'


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


def shares(default, caps):
    """Sections 146-147: co-sureties share equally, but nobody pays more than his own limit (water-filling)."""
    left, out, open_ = default, {k: 0 for k in caps}, sorted(caps, key=lambda k: caps[k])
    while open_ and left > 0:
        eq = left / len(open_)
        k = open_[0]
        if caps[k] <= eq:
            out[k] = caps[k]; left -= caps[k]; open_.pop(0)
        else:
            for k in open_: out[k] = eq
            left = 0
    return {k: int(v) if v == int(v) else round(v, 2) for k, v in out.items()}


def build():
    caps = {'Arora': 150000, 'Bose': 300000, 'Chawla': 450000}
    # ---------- Illustration 3: co-sureties in different sums ----------
    c3 = Checks()
    s1 = shares(360000, caps); s2 = shares(600000, caps); s3 = shares(900000, caps); s4 = shares(1000000, caps)
    e1 = c3.add('360000/3', 'default ₹3,60,000 — equal share, within every limit')
    assert s1 == {k: e1 for k in caps}
    e2b = c3.add('(600000-150000)/2', 'default ₹6,00,000 — Arora capped at ₹1,50,000; Bose and Chawla share the rest')
    assert s2 == {'Arora': 150000, 'Bose': e2b, 'Chawla': e2b}
    e3 = c3.add('150000+300000+450000', 'default ₹9,00,000 — equals the total of all limits; each pays his full limit')
    assert sum(s3.values()) == e3
    e4 = c3.add('1000000-900000', 'default ₹10,00,000 — creditor cannot recover this excess from the sureties')
    assert sum(s4.values()) == 900000
    t3 = table(['Default by principal debtor', 'Arora (limit ₹1,50,000)', 'Bose (limit ₹3,00,000)', 'Chawla (limit ₹4,50,000)', 'Total from sureties'], [
        ['₹3,60,000', s1['Arora'], s1['Bose'], s1['Chawla'], sum(s1.values())],
        ['₹6,00,000', s2['Arora'], s2['Bose'], s2['Chawla'], sum(s2.values())],
        ['₹9,00,000', s3['Arora'], s3['Bose'], s3['Chawla'], sum(s3.values())],
        ['₹10,00,000', s4['Arora'], s4['Bose'], s4['Chawla'], sum(s4.values())],
    ], num=[1, 2, 3, 4], title='Contribution of co-sureties (₹)', note='Each row is a separate situation, so no column total is struck.')

    # ---------- Illustration 2: continuing guarantee revoked ----------
    c2 = Checks()
    before = c2.add('65000+48000+27000', 'supplies before the notice of revocation')
    after = c2.add('38000+22000', 'supplies after the notice — surety not liable')
    liab2 = c2.add('65000+48000+27000', 'surety liable for pre-notice supplies (within the ₹2,00,000 limit)')

    # ---------- Illustration 4: set-off and insolvency of the debtor ----------
    c4 = Checks()
    setoff = c4.add('800000-75000', 'surety\'s liability after the debtor\'s set-off of ₹75,000')
    divid = c4.add('800000*40/100', 'amount realised from the insolvent debtor at 40 paise in the rupee')
    sur_ins = c4.add('800000-320000', 'surety\'s liability after the creditor\'s receipt from the insolvent estate')

    # ---------- Illustration 1: Section 125 ----------
    c1 = Checks()
    rec1 = c1.add('180000+22000', 'damages + costs recoverable from the indemnifier')

    # ---------- MCQ / case numbers ----------
    cm = Checks()
    m_eq = cm.add('900000/3', 'equal contribution of three co-sureties for ₹9,00,000')
    m_q = cm.add('400000*1/4', 'one-quarter share of ₹4,00,000')
    kc = Checks()
    k_arj = kc.add('(500000-100000)/2', 'share of each of the other two co-sureties')
    k_cont = kc.add('120000+90000', 'supplies before revocation')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch02', 'n': 7, 'title': 'Contract of Indemnity and Guarantee',
        'outcomes': ['Define a contract of indemnity (Section 124), state the rights of the indemnity-holder (Section 125) and explain when the indemnifier\'s liability begins.',
                     'Define a contract of guarantee (Sections 126–127), identify its three parties and essentials, and classify guarantees as specific or continuing (Section 129).',
                     'Distinguish indemnity from guarantee, explain the co-extensive nature of the surety\'s liability (Section 128) and Section 132.',
                     'Apply the rules on discharge of a surety (Sections 130–139, 142–144) and the rights of a surety (Sections 140, 141, 145–147), computing co-sureties\' contributions.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 50, 'practice': 50}, 'prereq': ['fnd-p2-ch02-u06'],
                 'exam_tip': 'Discharge of surety (especially Sections 133, 134, 135 and 139) and co-surety contribution (Sections 146–147) are asked almost every year. For co-sureties, show a small working table.'},
        'concepts': [
            {'id': 'c1', 'title': 'Contract of indemnity (Section 124)',
             'body': ['Indemnity means protection against loss. Under Section 124 it is a contract by which one party (the indemnifier) promises to save the other (the indemnity-holder or indemnified) from loss caused to him either by the indemnifier\'s own conduct or by the conduct of any other person.',
                      'Because the Indian definition speaks of loss caused by human conduct, loss from accidents or natural events not caused by anyone falls outside Section 124 — though such promises can still be enforced as ordinary contracts. Fire and marine insurance are contracts of indemnity; life insurance is not, because a life cannot be valued and replaced.',
                      'An indemnity may be express (stated in words) or implied (from conduct or circumstances). Like any contract, it needs all the essentials of Section 10 — a promise to indemnify someone for committing an unlawful act is void.'],
             'analogy': 'An indemnity is an umbrella someone else holds over you: if rain (loss) falls because of what they or others do, they keep you dry.',
             'work': 'Share-purchase agreements carry indemnity clauses for pre-sale tax demands, and companies indemnify directors and auditors in some situations. CAs evaluate them when estimating provisions and disclosing contingent assets or liabilities.'},
            {'id': 'c2', 'title': 'Rights of the indemnity-holder and when liability starts (Section 125)',
             'body': ['When sued, an indemnity-holder who acted within the scope of his authority can recover from the indemnifier: (a) all damages he is compelled to pay in a suit on a matter covered by the promise; (b) all costs he is compelled to pay in that suit, if he did not disobey the indemnifier\'s orders and acted as a prudent person would, or if the indemnifier authorised him to bring or defend the suit; and (c) all sums paid under a compromise of the suit, if the compromise was prudent or authorised by the indemnifier.',
                      'The Act is silent on when the indemnifier\'s liability begins. Courts have held that the indemnity-holder need not first pay and then claim: once his liability has become absolute and certain, he can call on the indemnifier to put him in funds to meet it (Gajanan Moreshwar v. Moreshwar Madan, Bombay High Court).'],
             'analogy': 'A promise to "keep you safe from loss" is worthless if you must first be ruined before it works — so the law lets you call on it as soon as the loss is certain.',
             'work': 'When a tax demand against an acquired business becomes final, the buyer\'s CA raises the indemnity claim on the seller immediately rather than waiting for the buyer to pay the tax.'},
            {'id': 'c3', 'title': 'Contract of guarantee — parties and essentials (Sections 126, 127)',
             'body': ['Section 126: a guarantee is a promise to make good the promise or the liability of a third person if that person fails. It involves three parties — the surety (who gives the guarantee), the principal debtor (whose default is covered) and the creditor (who receives the guarantee). A guarantee may be oral or written.',
                      'It is a tripartite arrangement made up of three contracts: creditor–principal debtor (the main contract), creditor–surety (the guarantee), and an implied contract by which the principal debtor will indemnify the surety if the surety pays.',
                      'Essentials: (1) an existing, legally enforceable debt or promise (not time-barred); (2) consideration — under Section 127 anything done or promised for the benefit of the principal debtor is enough for the surety, but past consideration will not do; (3) the surety must be competent — a guarantee for a minor\'s debt is valid and the surety is liable, but a minor cannot be a surety; (4) the guarantee must not be obtained by misrepresentation (Section 142) or concealment of material facts (Section 143); and (5) if the surety agreed that the creditor should not act until a co-surety joins, the guarantee is not valid unless that person joins (Section 144).'],
             'analogy': 'A guarantee is a safety net under a tightrope walker: it is there only in case the walker (the debtor) falls.',
             'work': 'Bank loans to companies are routinely backed by personal guarantees of promoters. In audits and due diligence, CAs disclose such guarantees and check whether the promoter has actually signed for the facility in question.'},
            {'id': 'c4', 'title': 'Specific and continuing guarantees (Section 129)',
             'body': ['A specific guarantee covers a single debt or transaction; it ends when that debt is paid. A continuing guarantee (Section 129) extends to a series of transactions — for example, supplies on credit from time to time up to a limit.',
                      'Under a continuing guarantee with a limit, the surety\'s liability is capped at the limit on the outstanding balance, however large the total business done over time.',
                      'A continuing guarantee may be revoked by the surety, for future transactions, by notice to the creditor (Section 130), and the surety\'s death, unless otherwise agreed, also revokes it for future transactions (Section 131). In both cases liability for transactions already entered into remains. A specific guarantee cannot be revoked once the liability has arisen.'],
             'analogy': 'A specific guarantee is a single bus ticket; a continuing guarantee is a monthly pass that you can cancel for the coming days but not for trips already taken.',
             'work': 'Distributors\' credit limits are often secured by a continuing guarantee. When a guarantor writes to withdraw, the credit team must freeze the balance as at the date of notice — that is the guarantor\'s maximum exposure.'},
            {'id': 'c5', 'title': 'Indemnity vs guarantee',
             'body': ['Parties: indemnity has two (indemnifier and indemnity-holder); guarantee has three (creditor, principal debtor, surety). Nature of liability: the indemnifier\'s liability is primary; the surety\'s is secondary — it arises only on the principal debtor\'s default.',
                      'Number of contracts: one in indemnity; three in guarantee. Purpose: indemnity reimburses a loss; guarantee secures a debt or performance for the creditor. Request: a surety usually acts at the principal debtor\'s request; an indemnifier need not act at anyone\'s request.',
                      'Right against third parties: after paying, a surety steps into the creditor\'s shoes and can sue the principal debtor in his own right; an indemnifier can proceed against a third party only through the indemnity-holder\'s rights (e.g. by assignment). Competency: in indemnity all parties must be competent; in guarantee, the principal debtor may be a minor and the guarantee is still valid.'],
             'analogy': 'An indemnifier is a first-line goalkeeper; a surety is the reserve keeper who plays only if the first one fails.',
             'work': 'Drafting matters: "I will pay if he does not" is a guarantee; "I will keep you harmless from any loss on this deal" is an indemnity. The label decides which rights and discharges apply.'},
            {'id': 'c6', 'title': 'Nature and extent of the surety\'s liability (Sections 128, 132)',
             'body': ['Section 128: unless the contract provides otherwise, the surety\'s liability is co-extensive with that of the principal debtor — he is liable for the same amount, including interest and charges, but no more.',
                      'The liability is secondary in the sense that it arises on the debtor\'s default, but the creditor need not first sue the principal debtor: unless otherwise agreed, he may proceed directly against the surety. Where the principal debtor\'s liability fails because of a defect in the document itself, the surety\'s liability also falls away.',
                      'Section 132: where two persons both undertake a liability to a third person and agree between themselves that one will be liable only if the other defaults, the third person is not affected by that private arrangement — he can hold each liable under the main contract, even if he knew of the arrangement.'],
             'analogy': 'The surety\'s liability is the shadow of the debtor\'s: same shape and size, never bigger — unless the contract says otherwise.',
             'work': 'Banks invoke guarantees without first suing the borrower. CAs advising guarantors explain that the guarantee covers interest and charges too, not only the principal.'},
            {'id': 'c7', 'title': 'Discharge of the surety (Sections 130–139, 142–144, 62)',
             'body': ['By revocation: notice for future transactions under a continuing guarantee (Section 130); death of the surety for future transactions (Section 131); novation — a new contract replacing the old one (Section 62).',
                      'By the creditor\'s conduct: any variance in the terms of the main contract made without the surety\'s consent discharges him as to transactions after the variance (Section 133); release of the principal debtor, or any act or omission of the creditor whose legal result is the debtor\'s discharge (Section 134); composition with, promise to give time to, or promise not to sue the principal debtor without the surety\'s consent (Section 135); and any act of the creditor inconsistent with the surety\'s rights, or omission of a duty owed to him, which impairs the surety\'s eventual remedy against the debtor (Section 139).',
                      'Not a discharge: a promise to give time made with a third person rather than with the debtor (Section 136); mere forbearance to sue (Section 137); release of one co-surety — it does not free the others (Section 138).',
                      'By invalidation: guarantee obtained by misrepresentation (Section 142), by concealment (Section 143), or failure of a co-surety to join where that was a condition (Section 144). In State Bank of Saurashtra v. Chitranjan Rangnath Raja, a surety was discharged to the extent of pledged stock lost through the bank\'s negligence.'],
             'analogy': 'The surety signed for a particular game; if the creditor changes the rules, lets the debtor off, or throws away the surety\'s fallback, the surety walks off the field.',
             'work': 'Before restructuring a loan (rescheduling, waiver of interest), lenders take the guarantors\' written consent. CAs reviewing recoverability check for that consent; without it the guarantee may be unenforceable.'},
            {'id': 'c8', 'title': 'Rights of the surety (Sections 140, 141, 145–147)',
             'body': ['Against the principal debtor: subrogation — after paying, the surety gets all the rights the creditor had against the debtor (Section 140); and an implied promise by the debtor to indemnify the surety for sums rightfully paid (Section 145).',
                      'Against the creditor: the benefit of every security the creditor held against the debtor when the guarantee was given, whether or not the surety knew of it — if the creditor loses or parts with it without consent, the surety is discharged to that value (Section 141); the right to use any set-off the debtor had against the creditor; and, if the debtor is insolvent, the creditor must give credit for what he receives from the insolvent estate.',
                      'Against co-sureties: unless otherwise agreed, co-sureties share the unpaid debt equally (Section 146). Where they are bound in different sums, they share equally so far as their respective limits allow (Section 147).'],
             'blocks': [t3],
             'analogy': 'Once the surety pays, he stands where the creditor stood — holding the same keys to the debtor\'s door.',
             'work': 'When a promoter-guarantor pays a bank, his CA ensures he is assigned the bank\'s securities and records a claim on the company and on co-guarantors for their shares.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'What can an indemnity-holder recover?', 'difficulty': 'core', 'minutes': 6,
             'q': 'Rhea agrees to indemnify Sameer against any claims arising from Sameer\'s sale of goods supplied by Rhea under her trademark. A buyer sues Sameer for defects. Sameer, with Rhea\'s approval, defends the suit, loses, and pays damages of ₹1,80,000 and legal costs of ₹22,000. How much can Sameer recover from Rhea?',
             'solution': [legal('Section 125: an indemnity-holder acting within the scope of his authority may recover from the indemnifier all damages he is compelled to pay in a suit on a matter covered by the indemnity, and all costs of that suit if he acted prudently or was authorised to defend it.',
                                'Sameer was sued on a matter covered by the indemnity, defended with Rhea\'s approval, and paid damages of ₹1,80,000 and costs of ₹22,000.',
                                'Both the damages and the costs fall within Section 125 — the suit concerned the indemnified matter and the defence was authorised.',
                                f'Sameer can recover {R(rec1)} (₹1,80,000 + ₹22,000) from Rhea.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Continuing guarantee revoked midway', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'Kunal guarantees payment, up to ₹2,00,000, for paint that Harsh Distributors may supply to Lalit on credit from time to time during 2026-27. Supplies: 10 May ₹65,000, 2 July ₹48,000, 20 August ₹27,000. On 1 September Kunal gives written notice to Harsh revoking the guarantee. Further supplies: 15 September ₹38,000, 10 October ₹22,000. Lalit pays nothing. What is Kunal\'s liability?',
             'solution': [legal('Section 129: a guarantee extending to a series of transactions is a continuing guarantee. Section 130: the surety may, at any time, cancel it for transactions after his notice reaches the creditor; liability for earlier transactions continues.',
                                f'Supplies before notice: {R(before)}. Supplies after notice: {R(after)}. Limit: ₹2,00,000.',
                                f'Kunal remains liable for the supplies made before 1 September, which total {R(before)} and are within the limit. The supplies of {R(after)} after the notice are outside the guarantee.',
                                f'Kunal is liable for {R(liab2)}. Harsh must recover the balance of {R(after)} from Lalit alone.'),
                          table(['Date', 'Supply (₹)', 'Covered by guarantee?'], [['10 May', 65000, 'Yes'], ['2 July', 48000, 'Yes'], ['20 August', 27000, 'Yes'], ['15 September', 38000, 'No — after notice'], ['10 October', 22000, 'No — after notice']], num=[1], title='Supplies')],
             'checks': c2},
            {'id': 'i3', 'title': 'Co-sureties bound in different sums', 'difficulty': 'hard', 'minutes': 10,
             'q': 'Arora, Bose and Chawla sign separate guarantees for a loan given by Prime Bank to Dinesh, limited to ₹1,50,000, ₹3,00,000 and ₹4,50,000 respectively. There is no agreement among them about sharing. Compute how much each must contribute, as between themselves, if Dinesh defaults to the extent of (a) ₹3,60,000, (b) ₹6,00,000, (c) ₹9,00,000, (d) ₹10,00,000.',
             'solution': [legal('Section 146: unless otherwise agreed, co-sureties contribute equally. Section 147: co-sureties bound in different sums contribute equally so far as the limits of their respective obligations permit — no one pays beyond his limit.',
                                'Limits: Arora ₹1,50,000; Bose ₹3,00,000; Chawla ₹4,50,000; total ₹9,00,000.',
                                f'(a) ₹3,60,000 ÷ 3 = {R(e1)} each — within every limit. (b) An equal share would be ₹2,00,000, above Arora\'s limit, so Arora pays ₹1,50,000 and the remaining ₹4,50,000 is shared by Bose and Chawla at {R(e2b)} each. (c) ₹9,00,000 equals the sum of the limits, so each pays his full limit. (d) The sureties together pay at most ₹9,00,000; the excess of {R(e4)} must be recovered from Dinesh.',
                                'Contributions are as shown in the table.'),
                          t3],
             'checks': c3},
            {'id': 'i4', 'title': 'Set-off and the insolvent debtor', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'Mohan borrowed ₹8,00,000 from Nikhil; Pooja guaranteed it. (a) Nikhil separately owes Mohan ₹75,000 for goods supplied. Mohan defaults and Nikhil sues Pooja. How much can Nikhil recover from her? (b) Instead, assume no set-off but Mohan is declared insolvent and his estate pays creditors 40 paise in the rupee. How much is Pooja liable for?',
             'solution': [legal('A surety, when sued, can use any set-off the principal debtor has against the creditor. Where the principal debtor is insolvent, the creditor must give credit for the amount he receives from the insolvent estate; the surety is liable only for the balance (Section 128 — liability co-extensive with the debtor\'s).',
                                f'(a) Debt ₹8,00,000; Mohan\'s claim against Nikhil ₹75,000. (b) Dividend 40% of ₹8,00,000 = {R(divid)}.',
                                f'(a) Pooja can set off ₹75,000: ₹8,00,000 − ₹75,000 = {R(setoff)}. (b) Nikhil receives {R(divid)} from the estate; Pooja is liable for ₹8,00,000 − {R(divid)} = {R(sur_ins)}.',
                                f'(a) {R(setoff)}. (b) {R(sur_ins)}.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Loan rescheduled without the guarantor', 'role': 'CA in a bank\'s credit-monitoring team', 'situation': 'A branch extended the repayment period of a ₹50 lakh term loan by two years at the borrower\'s request. The promoter-guarantor was not asked to sign anything.',
             'steps': ['Identify the change: a promise to give time to the principal debtor (Section 135) and a variance in the terms (Section 133).', 'Without the surety\'s consent, either provision can discharge the guarantor.',
                       'Obtain the guarantor\'s written consent to the rescheduling immediately; if refused, re-assess the security cover.', 'Flag the lapse in the inspection report and recommend a checklist step: "guarantor\'s consent obtained" before any restructuring.'],
             'takeaway': 'A guarantee is lost more often by careless changes than by the guarantor\'s refusal to pay.', 'think': 'Would the guarantor be discharged if the branch had simply not chased the borrower for a year after default, without promising anything?',
             'answer': 'No. Mere forbearance to sue, without a binding promise to give time, does not discharge the surety (Section 137).'},
            {'id': 'j2', 'title': 'Guarantee commission and disclosure', 'role': 'Statutory audit senior', 'situation': 'A private company has guaranteed a ₹2 crore loan taken by its sister concern. The loan agreement says the bank may proceed against the guarantor "without first proceeding against the borrower".',
             'steps': ['Confirm the guarantee document and limit, and whether it is specific or continuing.', 'Note that under Section 128 the company\'s liability is co-extensive with the borrower\'s, including interest.',
                       'Disclose the guarantee as a contingent liability unless default makes an outflow probable.', 'Check the sister concern\'s repayment record to assess whether a provision is needed.'],
             'takeaway': 'Section 128 makes a guarantor answerable for the full debt with interest — the disclosure must show that exposure.', 'think': 'Is the clause about proceeding directly against the guarantor unusual?',
             'answer': 'No — even without it, unless the contract provides otherwise, a creditor may sue the surety without first suing the principal debtor.'},
            {'id': 'j3', 'title': 'Three partners as co-guarantors', 'role': 'CA advising a family business', 'situation': 'Three brothers guaranteed a ₹90 lakh overdraft of the family company. The bank recovered the entire ₹90 lakh from the eldest brother.',
             'steps': ['Under Section 140, the eldest brother is subrogated to the bank\'s rights against the company.', 'Under Section 145 the company must indemnify him.', 'Under Section 146, absent any agreement, he can recover ₹30 lakh each from the other two brothers.', 'Document the claims and any securities transferred by the bank (Section 141).'],
             'takeaway': 'A guarantor who pays more than his share has three routes: the debtor, the securities and the co-sureties.', 'think': 'If the brothers had agreed to share 50:25:25 with the eldest bearing 50%, what could he claim from each of the others?',
             'answer': 'His agreed share is ₹45 lakh, so he can claim ₹22.5 lakh from each of the other two.',
             'checks': [{'expr': '9000000/3', 'value': 3000000, 'label': 'equal share of ₹90 lakh'}, {'expr': '9000000*25/100', 'value': 2250000, 'label': '25% share of ₹90 lakh'}]},
        ],
        'mcqs': [
            MC('m1', 'A contract in which one party promises to protect the other against loss arising from the promisor\'s own conduct or anyone else\'s conduct is a:', ['Contract of indemnity', 'Contract of guarantee', 'Contract of bailment', 'Contingent contract only'], 0, 'This is the Section 124 definition.', 'c1'),
            MC('m2', 'Which of the following is NOT a contract of indemnity?', ['Life insurance', 'Fire insurance', 'Marine insurance', 'A promise to make good any loss from a lawsuit'], 0, 'A life cannot be valued and restored, so life insurance is a contingent contract but not one of indemnity.', 'c1'),
            MC('m3', 'Under Section 125, an indemnity-holder who is sued can recover from the indemnifier:', ['Damages, costs and sums paid under a prudent or authorised compromise', 'Only damages', 'Only costs', 'Nothing until the indemnifier is sued'], 0, 'All three heads are recoverable, subject to the conditions in Section 125.', 'c2'),
            MC('m4', 'In a contract of guarantee, the person in respect of whose default the guarantee is given is the:', ['Principal debtor', 'Surety', 'Creditor', 'Indemnifier'], 0, 'Section 126 — surety gives the guarantee, creditor receives it, principal debtor is the one whose default is covered.', 'c3'),
            MC('m5', 'Under Section 127, the consideration for the surety\'s promise:', ['May be anything done for the benefit of the principal debtor', 'Must move directly from the creditor to the surety', 'Is not required at all', 'May be past consideration'], 0, 'Benefit to the principal debtor is sufficient consideration; past consideration is not.', 'c3', 'moderate'),
            MC('m6', 'A guarantee which extends to a series of transactions is called:', ['A continuing guarantee', 'A specific guarantee', 'A fidelity bond only', 'An indemnity'], 0, 'Section 129.', 'c4'),
            MC('m7', 'The liability of a surety, unless the contract provides otherwise, is:', ['Co-extensive with that of the principal debtor', 'Greater than that of the principal debtor', 'Limited to half the debt', 'Only for the principal amount, never for interest'], 0, 'Section 128 — same extent, including interest and charges.', 'c6'),
            MC('m8', 'A continuing guarantee is revoked as to future transactions by:', ['Notice by the surety or the surety\'s death', 'Only by the creditor\'s consent', 'Only by the principal debtor\'s death', 'Nothing — it can never be revoked'], 0, 'Sections 130 and 131.', 'c4'),
            MC('m9', 'The creditor, without the surety\'s consent, agrees with the principal debtor to give him six more months to pay. The surety is:', ['Discharged', 'Still liable', 'Liable for half the debt', 'Liable only for interest'], 0, 'Section 135 — a promise to give time to the principal debtor discharges the surety unless he consents.', 'c7', 'moderate'),
            MC('m10', 'The creditor simply does not sue the principal debtor for a year after the debt falls due. The surety is:', ['Not discharged — mere forbearance to sue', 'Discharged under Section 135', 'Discharged under Section 133', 'Discharged under Section 139'], 0, 'Section 137 — forbearance alone is not a promise to give time.', 'c7', 'moderate'),
            MC('m11', 'Section 143 deals with a guarantee obtained by:', ['Concealment of material circumstances', 'Free consent', 'Coercion', 'Undue influence'], 0, 'Section 142 covers misrepresentation; Section 143 covers keeping silent about material facts.', 'c7'),
            MC('m12', 'Three co-sureties guarantee a debt of ₹9,00,000 without any agreement about shares. The debtor defaults on the whole amount. As between themselves, each must pay:', [R(m_eq), '₹9,00,000', '₹4,50,000', '₹1,50,000'], 0, f'Section 146 — equal contribution: ₹9,00,000 ÷ 3 = {R(m_eq)}.', 'c8', 'core', '900000/3'),
            MC('m13', 'Co-sureties agree that A bears one-quarter, B one-quarter and C one-half of a ₹4,00,000 debt. The debtor defaults fully. A must pay:', [R(m_q), '₹1,33,333', '₹2,00,000', '₹50,000'], 0, f'Section 146 applies only "unless otherwise agreed"; the agreed share governs: ₹4,00,000 × 1/4 = {R(m_q)}.', 'c8', 'moderate', '400000*1/4'),
            MC('m14', 'The right of a surety, on payment, to step into the shoes of the creditor is called:', ['Subrogation (Section 140)', 'Set-off', 'Lien', 'Novation'], 0, 'Section 140 gives the surety all rights the creditor had against the principal debtor.', 'c8'),
            MC('m15', 'Two persons jointly sign a promissory note in favour of Ravi; between themselves, one is only a surety for the other, and Ravi knows this. Ravi sues the "surety" first. Under Section 132:', ['Ravi can sue him — the private arrangement does not affect Ravi', 'Ravi must sue the other first', 'The surety is discharged because Ravi knew', 'The note is void'], 0, 'The arrangement between the two promisors does not affect their liability to the third person, even if he knew of it.', 'c6', 'hard'),
        ],
        'questions': [
            Q('q1', 5, 'core', 'table',
              'Differentiate a contract of indemnity from a contract of guarantee on any five bases.',
              [table(['Basis', 'Indemnity', 'Guarantee'], [
                  ['Parties', 'Two — indemnifier and indemnity-holder', 'Three — creditor, principal debtor and surety'],
                  ['Number of contracts', 'One', 'Three (creditor–debtor, creditor–surety, implied debtor–surety)'],
                  ['Nature of liability', 'Primary and independent', 'Secondary — arises only on the principal debtor\'s default'],
                  ['Purpose', 'To make good a loss', 'To secure a debt or the performance of a promise'],
                  ['Request', 'Indemnifier need not act at anyone\'s request', 'Surety usually acts at the principal debtor\'s request'],
                  ['Rights after payment', 'Cannot sue third parties in his own name unless rights are assigned', 'Steps into the creditor\'s shoes against the principal debtor (Section 140)'],
                  ['Competency', 'All parties must be competent', 'Valid even if the principal debtor is a minor'],
              ])],
              [('Parties and number of contracts', 1, 'concept'), ('Nature of liability', 1, 'concept'), ('Purpose', 1, 'concept'), ('Rights after payment', 1, 'analysis'), ('Any fifth valid point', 1, 'analysis')],
              ['Tables score better than paragraphs here.', 'Mentioning Sections 124 and 126 in the "meaning" row is appreciated.'],
              ['Saying the surety\'s liability is primary.', 'Saying a guarantee must be in writing (it may be oral).'],
              ['Five clean rows are enough for five marks.']),
            Q('q2', 6, 'hard', 'table',
              'Pranav, Qadir and Rohit are co-sureties for a loan given by Sigma Bank to Tanvi, under separate guarantees limited to ₹1,00,000, ₹2,00,000 and ₹4,00,000 respectively. There is no agreement among them about shares. Tanvi defaults. Compute the contribution of each, as between themselves, if the default is (i) ₹2,40,000; (ii) ₹4,00,000; (iii) ₹7,00,000. State the provision applied.',
              [p('Provision: Section 146 — co-sureties contribute equally unless otherwise agreed. Section 147 — co-sureties bound in different sums contribute equally as far as their respective limits permit.'),
               table(['Default', 'Pranav (₹1,00,000)', 'Qadir (₹2,00,000)', 'Rohit (₹4,00,000)', 'Total'], [
                   ['(i) ₹2,40,000'] + [shares(240000, {'P': 100000, 'Q': 200000, 'R': 400000})[k] for k in 'PQR'] + [240000],
                   ['(ii) ₹4,00,000'] + [shares(400000, {'P': 100000, 'Q': 200000, 'R': 400000})[k] for k in 'PQR'] + [400000],
                   ['(iii) ₹7,00,000'] + [shares(700000, {'P': 100000, 'Q': 200000, 'R': 400000})[k] for k in 'PQR'] + [700000],
               ], num=[1, 2, 3, 4], note='Each row is a separate situation.'),
               wn('Working', '(i) 2,40,000 ÷ 3 = 80,000 each, all within limits. (ii) Equal share 1,33,333 exceeds Pranav\'s limit, so Pranav pays 1,00,000; balance 3,00,000 ÷ 2 = 1,50,000 each for Qadir and Rohit (both within limits). (iii) 7,00,000 equals the total of all limits, so each pays his full limit.')],
              [('Sections 146 and 147 stated', 1.5, 'provision'), ('(i) correct shares', 1, 'computation'), ('(ii) Pranav capped; balance shared equally', 2, 'computation'), ('(iii) each pays full limit', 1, 'computation'), ('Presentation in a table', 0.5, 'presentation')],
              ['Most errors come from splitting in proportion to the limits (1:2:4) instead of equally subject to limits.'],
              ['Proportionate sharing in (ii).', 'Making Pranav pay more than his limit.'],
              ['Show the "equal share" test first, then cap and redistribute.'],
              checks=[{'expr': '240000/3', 'value': 80000, 'label': '(i) equal share'}, {'expr': '(400000-100000)/2', 'value': 150000, 'label': '(ii) Qadir and Rohit each'}, {'expr': '100000+200000+400000', 'value': 700000, 'label': '(iii) sum of limits'}]),
            Q('q3', 4, 'moderate', 'legal',
              'Usha guarantees the performance of a contract by which Vijay is to build a warehouse for Wasim within six months, Wasim agreeing to supply the steel. Wasim fails to supply the steel, and Vijay cannot complete the work. Wasim sues Usha. Is she liable?',
              [legal('Section 134: the surety is freed if the creditor makes a contract with the principal debtor that releases the debtor, or if the creditor does or omits anything whose legal result is that the debtor stands discharged. Section 139 also discharges a surety where the creditor omits a duty owed to the surety and the surety\'s eventual remedy is impaired.',
                     'Wasim (creditor) promised to supply the steel; he did not. Because of this, Vijay (principal debtor) could not perform.',
                     'Wasim\'s omission excuses Vijay\'s non-performance, so Vijay is discharged. Since the surety\'s liability depends on the debtor\'s liability, Usha is also discharged.',
                     'Usha is not liable to Wasim.')],
              [('Section 134 (and/or 139) stated', 1.5, 'provision'), ('Facts linked: creditor\'s omission excused the debtor', 1, 'analysis'), ('Surety\'s liability follows the debtor\'s', 0.5, 'analysis'), ('Conclusion', 1, 'conclusion')],
              ['The examiner looks for the link: creditor\'s omission → debtor discharged → surety discharged.'],
              ['Treating it as a variance under Section 133 without explaining the change.', 'Holding Usha liable because "guarantee is unconditional".'],
              ['Name the creditor, debtor and surety in the facts paragraph — it shows you have mapped the parties.']),
            Q('q4', 4, 'moderate', 'legal',
              'Yash, a clerk with Zenith Traders, had earlier misappropriated cash, which Zenith knew. Zenith asked Yash to furnish a guarantee for honest conduct. Anil gave the guarantee without being told of the past misappropriation. Yash again misappropriated ₹60,000. Zenith sues Anil. Advise Anil.',
              [legal('Section 143: any guarantee obtained by the creditor by keeping silent about material circumstances is invalid.',
                     'Zenith knew of Yash\'s earlier misappropriation but did not tell Anil when obtaining his guarantee. Yash later misappropriated ₹60,000.',
                     'Yash\'s past dishonesty was a material fact that would affect Anil\'s decision to stand surety. Zenith\'s silence about it was concealment within Section 143.',
                     'The guarantee is invalid. Anil is not liable for the ₹60,000.')],
              [('Section 143 stated', 1.5, 'provision'), ('Material fact identified', 1, 'analysis'), ('Concealment by creditor applied', 0.5, 'analysis'), ('Conclusion', 1, 'conclusion')],
              ['Strong answers name Section 143 and explain why the fact was material.'],
              ['Citing Section 142 (misrepresentation) when the facts show silence.'],
              ['Distinguish: 142 = false statement; 143 = keeping quiet.']),
        ],
        'revision': {'summary': ['Indemnity (Section 124): promise to save another from loss caused by the promisor or any other person; two parties; primary liability.',
                                 'Section 125: indemnity-holder recovers damages, costs and prudent/authorised compromise sums. Liability starts once the holder\'s liability is absolute (Gajanan Moreshwar).',
                                 'Guarantee (Section 126): surety, principal debtor, creditor; three contracts; may be oral; consideration under Section 127 may be benefit to the debtor (not past).',
                                 'Specific vs continuing (Section 129); revocation by notice (130) or death (131) for future transactions.',
                                 'Surety\'s liability co-extensive (128); Section 132 private arrangement does not bind the creditor.',
                                 'Discharge: 130, 131, 62, 133, 134, 135, 139, 142, 143, 144. Not discharge: 136, 137, 138.',
                                 'Rights: subrogation 140, securities 141, indemnity 145, set-off, credit for insolvency dividend, co-sureties 146–147.'],
                     'remember': ['Equal shares among co-sureties, but never above a surety\'s own limit (147).', 'Variance without consent discharges for transactions after the variance (133).', 'Minor can be principal debtor (guarantee valid), not surety.'],
                     'traps': ['Do not split co-surety liability in proportion to limits.', 'Do not treat forbearance to sue as giving time.', 'Do not say a guarantee must be written.', 'Do not call life insurance an indemnity.']},
        'quickref': [{'k': 'Section 124', 'v': 'Contract of indemnity'}, {'k': 'Section 125', 'v': 'Rights of indemnity-holder when sued'}, {'k': 'Section 126', 'v': 'Guarantee, surety, principal debtor, creditor'},
                     {'k': 'Section 127', 'v': 'Consideration for guarantee'}, {'k': 'Section 128', 'v': 'Surety\'s liability co-extensive'}, {'k': 'Section 129', 'v': 'Continuing guarantee'},
                     {'k': 'Sections 130 / 131', 'v': 'Revocation by notice / by surety\'s death (future transactions)'}, {'k': 'Section 132', 'v': 'Two primarily liable — private arrangement no defence'},
                     {'k': 'Sections 133–135', 'v': 'Variance; release of debtor; composition, time, not to sue'}, {'k': 'Sections 136–138', 'v': 'NOT discharge: time via third person; forbearance; release of a co-surety'},
                     {'k': 'Section 139', 'v': 'Creditor impairs surety\'s eventual remedy'}, {'k': 'Sections 140 / 141', 'v': 'Subrogation / benefit of creditor\'s securities'},
                     {'k': 'Sections 142–144', 'v': 'Misrepresentation; concealment; co-surety not joining'}, {'k': 'Section 145', 'v': 'Implied promise of debtor to indemnify surety'},
                     {'k': 'Sections 146 / 147', 'v': 'Co-sureties equal / equal within different limits'}],
        'viva': [
            V('v1', 'How does a contract of indemnity differ from a contract of guarantee? Give the main points.',
              'Indemnity has two parties, the indemnifier and the indemnity holder, while a guarantee has three: creditor, principal debtor and surety. The indemnifier\'s liability is primary, but the surety\'s liability is secondary, arising only when the principal debtor defaults. Indemnity is to make good a loss; a guarantee is to secure a debt.',
              [P('p1', 'Indemnity: two parties; guarantee: three parties', 4, 'two parties|two party|2 parties|2 party|two persons|2 persons|two people|2 people', 'three parties|three party|3 parties|3 party|three persons|3 persons|three people|3 people|creditor principal debtor surety|creditor debtor surety|surety creditor'),
               P('p2', 'Indemnifier\'s liability primary; surety\'s secondary (on default)', 4, ALT('indemnifier {p}', 'indemnity {p}', 'indemnifier liability {p}', 'indemnity liability {p}', p=('primary', 'is primary', 'primarily', 'first')), ALT('surety {s}', 'surety liability {s}', 'guarantee {s}', 'guarantor {s}', s=('secondary', 'is secondary', 'only on default', 'only when debtor default', 'arises on default', 'only if principal debtor default', 'after default'))),
               P('p3', 'Purpose: make good a loss vs secure a debt', 2, 'loss|reimburse|compensat', 'secur|debt|default', min=2)], 'c5'),
            V('v2', 'What can an indemnity holder recover from the indemnifier when he is sued?',
              'Under Section 125 the indemnity holder can recover all damages he is compelled to pay in the suit, all costs of the suit if he acted prudently or with authority, and all sums paid under a compromise if the compromise was prudent or authorised.',
              [P('p1', 'All damages paid in the suit', 3, 'damage'),
               P('p2', 'All costs of the suit (prudent/authorised)', 3, 'cost'),
               P('p3', 'Sums paid under a prudent or authorised compromise', 3, 'compromise|settle'),
               P('p4', 'Section 125', 1, 'section 125|125')], 'c2'),
            V('v3', 'What is meant by the rule that a surety\'s liability is co-extensive with the principal debtor\'s?',
              'Under Section 128, unless the contract says otherwise, the surety is liable to the same extent as the principal debtor, including interest and charges, but not more. The creditor can sue the surety directly without first suing the principal debtor.',
              [P('p1', 'Same extent as the principal debtor — not more (unless contract otherwise)', 5, 'same extent|same amount|same as the principal|same as principal debtor|equal to the principal|equal to principal debtor|same as debtor|equal to debtor|as much as the principal|as much as the debtor|whatever the debtor|same liability|not more|no more'),
               P('p2', 'Includes interest and charges', 2, 'interest|charge'),
               P('p3', 'Creditor may sue the surety directly / Section 128', 3, 'directly|without first suing|without suing|not need to sue|need not sue|first against surety|proceed against surety|section 128|128')], 'c6'),
            V('v4', 'In what ways does the conduct of the creditor discharge a surety?',
              'The surety is discharged if the creditor varies the terms of the contract without his consent, under Section 133; if he releases the principal debtor, under Section 134; if he makes a composition with the principal debtor, promises him extra time, or promises not to sue him, under Section 135; or if he impairs the surety\'s eventual remedy, under Section 139. Mere forbearance to sue does not discharge the surety.',
              [P('p1', 'Variance in terms without consent (133)', 3, 'varian|vary|vari|change in term|change the term|alter|section 133|133'),
               P('p2', 'Release or discharge of the principal debtor (134)', 2, 'release|discharge principal|discharge of principal|discharge the principal|discharg debtor|section 134|134'),
               P('p3', 'Composition, giving time, promise not to sue (135)', 3, 'composition|compound|give time|giving time|gives time|extra time|more time|extend time|extension|not to sue|not sue|section 135|135'),
               P('p4', 'Impairing surety\'s eventual remedy (139)', 2, 'impair|eventual remedy|loses security|lose security|lost security|section 139|139|inconsistent with the right|prejudice')], 'c7'),
            V('v5', 'How do co-sureties share the liability when the principal debtor defaults?',
              'Under Section 146, unless otherwise agreed, co-sureties contribute equally to the unpaid debt. Under Section 147, if they are bound in different sums, they still contribute equally, but no one has to pay more than his own limit.',
              [P('p1', 'Equally, unless otherwise agreed (146)', 5, 'equal|equally|same share|same amount|in equal|share alike', 'unless otherwise agreed|unless agreed|no agreement|absence of agreement|subject to agreement|unless contract|section 146|146', min=1),
               P('p2', 'Different limits: equally, but not beyond each one\'s limit (147)', 5, 'limit|maximum|cap|bound in different|different sum|section 147|147', 'not more than|not beyond|not exceed|up to|within|no more than|as far as|so far as|subject to|no one pay more|no one pay beyond|no one has to pay more|nobody pay more|nobody pay beyond|none pay more|not pay more|not pay beyond|not liable beyond|not liable for more|never more than|beyond his limit|beyond limit|exceed his limit|exceed limit|above his limit', min=2)], 'c8'),
            V('v6', 'What is a continuing guarantee and how can it be revoked?',
              'A continuing guarantee under Section 129 extends to a series of transactions. It can be revoked by the surety for future transactions by giving notice to the creditor, under Section 130, and the surety\'s death also revokes it for future transactions under Section 131. Liability for past transactions continues.',
              [P('p1', 'Extends to a series of transactions (129)', 3, 'series|number of transaction|many transaction|several transaction|repeated|from time to time|section 129|129'),
               P('p2', 'Revoked by notice for future transactions (130)', 3, 'notice', 'future|later|subsequent|after|coming', min=2),
               P('p3', 'Death of surety revokes for the future (131)', 2, 'death|dies|died|section 131|131'),
               P('p4', 'Past transactions remain covered', 2, 'past|earlier|already|before the notice|previous|prior|still liable')], 'c4'),
            V('v7', 'What rights does a surety have against the principal debtor after paying the debt?',
              'After paying, the surety is subrogated to all the rights the creditor had against the principal debtor, under Section 140. He also has an implied right to be indemnified by the principal debtor for whatever he has rightfully paid, under Section 145.',
              [P('p1', 'Subrogation — steps into creditor\'s shoes (140)', 5, 'subrogat|creditor shoes|shoes of the creditor|place of the creditor|rights of the creditor|creditor rights|all the rights|section 140|140'),
               P('p2', 'Implied indemnity from the debtor (145)', 5, 'indemn|reimburs|recover from the debtor|recover from principal|claim from the debtor|repay|section 145|145')], 'c8'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Three guarantors and a bakery loan', 'difficulty': 'hard',
            'case': ('Elite Bank lends ₹5,00,000 to Fresh Crust Bakery. Gauri, Hemant and Ira each sign separate guarantees, limited to ₹1,00,000, ₹3,00,000 and ₹3,00,000. Gauri also gives a separate continuing guarantee to Javed Flour Mills for flour supplied to the bakery on credit; supplies of ₹1,20,000 and ₹90,000 are made before she sends a notice of revocation, and ₹70,000 after it. Later, without asking any guarantor, the bank agrees with the bakery to extend the repayment date by one year in return for a higher interest rate. The bakery then defaults on the entire loan.'),
            'mcqs': [
                M('k1a', 'Ignoring the extension of time, how much would Hemant contribute, as between the co-sureties, if the default were ₹5,00,000?', [R(k_arj), '₹1,66,667', '₹2,14,286', '₹3,00,000'], 0,
                  f'Equal share ₹1,66,667 exceeds Gauri\'s limit of ₹1,00,000, so she pays ₹1,00,000. Hemant and Ira share ₹4,00,000 equally = {R(k_arj)} each (Section 147).', 'hard', '(500000-100000)/2'),
                M('k1b', 'What is the effect of the bank\'s agreement with the bakery to extend the repayment date?', ['All three guarantors are discharged (Sections 133 and 135)', 'No effect, as it was only an extension', 'Only Gauri is discharged', 'The guarantors become liable for the higher interest'], 0,
                  'A binding promise to give time to the principal debtor, and a variance in terms, made without the sureties\' consent, discharge them.', 'hard'),
                M('k1c', 'For how much is Gauri liable to Javed Flour Mills?', [R(k_cont), '₹2,80,000', '₹70,000', '₹1,20,000'], 0,
                  f'Revocation by notice under Section 130 covers only future transactions; she remains liable for supplies before the notice: ₹1,20,000 + ₹90,000 = {R(k_cont)}.', 'moderate', '120000+90000'),
                M('k1d', 'Gauri\'s guarantee to Javed Flour Mills is an example of a:', ['Continuing guarantee', 'Specific guarantee', 'Contract of indemnity', 'Contingent agreement that is void'], 0,
                  'It covers a series of supplies over time — Section 129.', 'core'),
            ]}],
    }


# ---------- teaching explanations + topic tags for every MCQ (override the short drafts above) ----------
TIND, TGUA, TTYP, TNAT = 'Contract of Indemnity', 'Contract of Guarantee', 'Types of Guarantees', 'Nature and Extent of Surety’s Liability [Section 128]'
TTWO, TDS, TRS = 'Liability of Two Persons, Primarily Liable, Not Affected by Arrangement', 'Discharge of a Surety', 'Rights of a Surety'
EXPLAIN = {
    'm1': (TIND, 'Section 124 defines a contract of indemnity as one where a party promises to save the other from loss caused by the conduct of the promisor himself or of any other person. It has two parties: indemnifier and indemnity-holder. The tempting trap is "contract of guarantee" — a guarantee has three parties and covers a third person\'s default, not general loss. In practice: indemnity clauses in share purchase agreements protect a buyer against undisclosed tax demands relating to the seller\'s period.'),
    'm2': (TIND, 'Indemnity means making good an actual, measurable loss. Fire and marine insurance compensate the actual loss to property, and a promise to cover loss from a lawsuit is a classic indemnity. Life insurance pays a fixed sum on death, because a life cannot be valued or restored, so it is a contingent contract, not indemnity. The tempting trap is marine insurance, which students sometimes think pays fixed sums. In practice: insurers settle fire claims based on surveyed loss, but life claims for the full sum assured.'),
    'm3': (TIND, 'Section 125 lets an indemnity-holder acting within the scope of his authority recover from the indemnifier: all damages he is compelled to pay in a suit, all costs he is compelled to pay, and all sums paid under a compromise that was prudent or authorised by the indemnifier. The tempting trap is "only damages" — costs and compromise sums are also covered. In practice: a director indemnified by a company recovers legal costs and settlement amounts paid in suits arising from his duties.'),
    'm4': (TGUA, 'Section 126: in a contract of guarantee the surety gives the guarantee, the creditor receives it, and the principal debtor is the person in respect of whose default it is given. The tempting trap is "surety" — the surety promises to pay if the principal debtor defaults; he is not the person whose default is covered. In practice: when a bank lends to a private company, the company is the principal debtor and its directors who sign personal guarantees are the sureties.'),
    'm5': (TGUA, 'Section 127: any act or promise that benefits the principal debtor is enough consideration to support the surety\'s promise. The surety need not personally gain anything. The tempting trap is "is not required at all" — consideration is required, but benefit to the principal debtor satisfies it. Past consideration is not enough. In practice: a director\'s personal guarantee is supported by the bank granting the loan to his company.'),
    'm6': (TTYP, 'Section 129: a guarantee that extends to a series of transactions is a continuing guarantee. A guarantee for a single debt or transaction is a specific guarantee, which ends once that debt is repaid. The trap is "a fidelity bond only" — a fidelity guarantee for an employee\'s honesty is one example of a continuing guarantee, not the general term. In practice: banks take continuing guarantees for cash credit and overdraft limits, which cover a running balance.'),
    'm7': (TNAT, 'Section 128: unless the guarantee limits it, the surety owes as much as the principal debtor owes — the same amount, including interest and charges. The tempting trap is "only for the principal amount, never for interest"; the surety is liable for everything the debtor owes unless the guarantee limits it. The creditor can also sue the surety without first suing the debtor. In practice: banks demand outstanding loans plus interest from guarantors when borrowers default.'),
    'm8': (TDS, 'A continuing guarantee may be revoked as to future transactions by notice from the surety to the creditor (Section 130) and, unless the contract provides otherwise, by the surety\'s death (Section 131). The surety remains liable for transactions already entered into. The tempting trap is "only by the creditor\'s consent" — the surety can revoke unilaterally for the future. In practice: a retiring director sends written notice to the bank revoking his guarantee for future advances to the company.'),
    'm9': (TDS, 'Section 135: if the creditor binds himself by agreement to give the principal debtor more time, a surety who has not agreed is released. The surety did not agree to the six-month extension, so he is discharged. The tempting trap is "still liable" — the extension changes the risk the surety accepted, so the law releases him. In practice: banks obtain guarantors\' written consent before restructuring or rescheduling a loan.'),
    'm10': (TDS, 'Section 137: a creditor who simply holds back from suing the debtor, or from using other remedies, does not release the surety, unless the guarantee says otherwise. Here there is no promise to give time — the creditor simply delayed. The tempting trap is "discharged under Section 135", which requires a binding agreement to give time. In practice: lenders can wait before enforcing a loan without losing their claim against guarantors, although limitation periods still apply.'),
    'm11': (TDS, 'Section 143: a guarantee obtained by the creditor by keeping silent about a material circumstance is invalid. Section 142 deals with guarantees obtained by misrepresentation. The tempting trap is "coercion", which is a general vitiating factor but not what Section 143 specifically covers. In practice: if a bank takes a guarantee for an employee\'s honesty while hiding that the employee has already committed fraud, the guarantee is invalid.'),
    'm12': (TRS, 'Section 146: co-sureties for one debt, with no agreement to the contrary, share the burden equally among themselves when the debtor defaults. ₹9,00,000 ÷ 3 = ₹3,00,000 each. The tempting trap is ₹9,00,000 — each co-surety may be sued by the creditor for the whole, but among themselves they share equally. In practice: when directors jointly guarantee a company loan and one pays, he recovers contributions from the others.'),
    'm13': (TRS, 'Section 146 applies only "in the absence of any contract to the contrary". Here the co-sureties agreed shares, so A pays his agreed one-quarter: ₹4,00,000 × 1/4 = ₹1,00,000. The tempting trap is ₹1,33,333, dividing equally among three as if there were no agreement. In practice: shareholders giving joint guarantees often sign a contribution agreement matching their shareholding.'),
    'm14': (TRS, 'Section 140: when a surety pays the guaranteed debt on default, he is invested with all the rights the creditor had against the principal debtor — he steps into the creditor\'s shoes. This is subrogation. Section 141 adds his right to securities held by the creditor. The tempting trap is "lien", which is a right to retain goods until payment. In practice: a guarantor who repays a defaulted business loan can enforce the bank\'s mortgage over the borrower\'s property.'),
    'm15': (TTWO, 'Section 132: where two persons contract with a third to undertake a liability, and between themselves one is liable only if the other fails, this arrangement does not affect their liability to the third person, even if he knows of it. So Ravi may sue the "surety" first. The tempting trap is "the surety is discharged because Ravi knew" — knowledge makes no difference. In practice: co-signers on a loan cannot rely on a private understanding to escape the lender\'s claim.'),
    'k1/k1a': (TRS, 'Section 147: co-sureties bound in different sums pay equally, as far as their limits permit. Equal share = ₹5,00,000 ÷ 3 = ₹1,66,667, which exceeds Gauri\'s ₹1,00,000 limit, so she pays ₹1,00,000. The remaining ₹4,00,000 is split equally between Hemant and Ira: ₹2,00,000 each, within their ₹3,00,000 limits. The tempting trap is ₹1,66,667, ignoring Gauri\'s cap. In practice: CAs computing guarantors\' contingent liabilities apply these limits when disclosing exposure.'),
    'k1/k1b': (TDS, 'Without the guarantors\' consent, the bank agreed to extend repayment by a year and raised the interest rate. Section 135 (promise to give time to the principal debtor) and Section 133 (variance in terms) both discharge sureties who did not consent. All three guarantors are discharged. The tempting trap is "no effect, as it was only an extension" — any binding extension changes the surety\'s risk. In practice: banks take guarantors\' written consent to every loan restructuring.'),
    'k1/k1c': (TDS, 'Section 130: revocation of a continuing guarantee by notice operates only for future transactions. Supplies before the notice were ₹1,20,000 + ₹90,000 = ₹2,10,000, so Gauri remains liable for that amount; the ₹70,000 supplied later is not covered. The tempting trap is ₹2,80,000, ignoring the revocation. In practice: suppliers who receive a guarantor\'s revocation notice must tighten credit or obtain fresh security for future supplies.'),
    'k1/k1d': (TTYP, 'Gauri\'s guarantee covers flour supplied on credit over time, a series of transactions, so it is a continuing guarantee under Section 129. That is why notice could revoke it for future supplies. The tempting trap is "specific guarantee", which covers one transaction and ends when it is paid off. In practice: distributors and wholesalers commonly ask for continuing guarantees to support running credit accounts.'),
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
