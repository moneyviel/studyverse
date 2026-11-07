"""Case-study MCQ sets (a short case + 3–5 linked MCQs) for every built CA unit — original cases, figures computed.
Schema (unit key "cases"): {id, title, difficulty, case, given?[blocks], mcqs:[{id, q, options[4], answer, explain, difficulty, check?}]}
MCQ ids are unique inside the unit (stats key: "<unit>#<mcq id>")."""
from lib import Checks, R, inr, table


def M(mid, q, options, answer, explain, difficulty='hard', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'difficulty': difficulty}
    if check: d['check'] = check
    return d


def cases():
    out = {}
    # ---------------- U1 Journal entries ----------------
    c = Checks()
    pur = c.add('100000*85/100', 'purchases after 15% trade discount')
    paid = c.add('85000*98/100', 'paid after 2% cash discount')
    disc = c.add('85000-83300', 'discount received')
    cash = c.add('200000-83300', 'cash left')
    out['fnd-p1-ch02-u01'] = [{
        'id': 'k1', 'title': 'Meera Traders — first week of business', 'difficulty': 'hard',
        'case': ('Meera starts a stationery business on 1 August 2026 with cash of ₹2,00,000. On 2 August she buys goods from Vinay & Sons with a list price of '
                 '₹1,00,000 at a trade discount of 15%, on credit. On 6 August she pays Vinay & Sons in cash and, because she pays within the week, receives a '
                 'cash discount of 2% on the amount due. On 8 August she donates goods costing ₹5,000 to a local school. No other cash transaction takes place.'),
        'mcqs': [
            M('k1a', 'At what amount will the purchase of 2 August be recorded?', [R(pur), R(100000), R(paid), R(98000)], 0,
              f'Trade discount is deducted on the invoice and never recorded: 1,00,000 × 85% = {R(pur)}.', 'moderate', '100000*85/100'),
            M('k1b', 'How much cash does Meera pay Vinay & Sons on 6 August?', [R(paid), R(pur), R(83000), R(98000)], 0,
              f'Cash discount is calculated on the amount due after trade discount: {R(pur)} × 98% = {R(paid)}; the discount of {R(disc)} is credited to Discount Received.', 'hard', '85000*98/100'),
            M('k1c', 'Which entry records the donation of 8 August?', ['Charity A/c Dr. To Purchases A/c', 'Purchases A/c Dr. To Charity A/c', 'Drawings A/c Dr. To Purchases A/c', 'Charity A/c Dr. To Cash A/c'], 0,
              'Donated goods are an expense of the business (charity), and the goods leave at cost, so Purchases is credited. Drawings would be used only if the owner took the goods for herself.'),
            M('k1d', 'What is the cash balance after 8 August?', [R(cash), R(115000), R(100000), R(118400)], 0,
              f'Cash 2,00,000 − payment {R(paid)} = {R(cash)}. The donation was of goods, not cash.', 'hard', '200000-83300'),
        ]}]

    # ---------------- U2 Ledgers ----------------
    c = Checks()
    dr_tot = c.add('12000+30000', 'debit side before balance')
    cr_tot = c.add('25000+2000+500', 'credit side before balance')
    bal = c.add('42000-27500', 'balance')
    out['fnd-p1-ch02-u02'] = [{
        'id': 'k1', 'title': "Sunil's account in the books of Ojas Traders", 'difficulty': 'hard',
        'case': ('On 1 April 2026 Sunil owed Ojas Traders ₹12,000. During April, Ojas Traders sold goods to Sunil on credit for ₹30,000, received ₹25,000 from him in cash, '
                 'accepted goods worth ₹2,000 returned by him, and allowed him a cash discount of ₹500. Sunil\'s account is balanced on 30 April.'),
        'mcqs': [
            M('k1a', "On which side of Sunil's account is the cash of ₹25,000 posted, and how?", ['Credit side — "By Cash"', 'Debit side — "To Cash"', 'Credit side — "To Cash"', 'Debit side — "By Cash"'], 0,
              "Sunil is the giver, so his account is credited; credit-side postings begin with \"By\" followed by the other account — Cash.", 'moderate'),
            M('k1b', "What is the balance of Sunil's account on 30 April?", [f'{R(bal)} Dr', f'{R(bal)} Cr', '₹17,500 Dr', '₹15,000 Dr'], 0,
              f'Debit side {R(dr_tot)} (opening balance + sales); credit side {R(cr_tot)} (cash + returns + discount). Debit is heavier by {R(bal)}, so Sunil still owes the business — a debit balance.', 'hard', '12000+30000-25000-2000-500'),
            M('k1c', 'Where is "Balance c/d" written when the account is closed on 30 April?', ['On the credit side', 'On the debit side', 'On both sides', 'It is not written; only b/d is shown'], 0,
              'Balance c/d goes on the lighter side — here the credit side — so that both totals become equal.', 'moderate'),
            M('k1d', 'What will be the first entry in the account on 1 May?', [f'To Balance b/d {R(bal)} on the debit side', f'By Balance b/d {R(bal)} on the credit side', 'To Sales ₹30,000 on the debit side', 'By Cash ₹25,000 on the credit side'], 0,
              'The balance carried down on the credit side is brought down on the opposite (debit) side at the start of the next period.', 'moderate'),
        ]}]

    # ---------------- U3 Trial balance ----------------
    c = Checks()
    drs = [('Cash', 18000), ('Debtors', 60000), ('Purchases', 150000), ('Salaries', 36000), ('Furniture', 50000), ('Drawings', 12000), ('Sales returns', 4000), ('Rent', 15000)]
    crs = [('Bank overdraft', 25000), ('Creditors', 42000), ('Sales', 240000), ('Purchase returns', 3000)]
    dtot = c.add('+'.join(str(v) for _, v in drs), 'debit total')
    cap = c.add(f"{dtot}-({'+'.join(str(v) for _, v in crs)})", 'capital (balancing figure)')
    out['fnd-p1-ch02-u03'] = [{
        'id': 'k1', 'title': "Asha's ledger balances on 31 March 2027", 'difficulty': 'hard',
        'case': ('Asha runs a small trading business. Her ledger shows these balances on 31 March 2027: ' + ', '.join(f'{n} {R(v)}' for n, v in drs + crs) +
                 '. Her capital account balance is not given and is to be found as the balancing figure of the trial balance.'),
        'mcqs': [
            M('k1a', 'What is the total of the debit column of the trial balance?', [R(dtot), '₹3,10,000', '₹3,70,000', '₹3,41,000'], 0,
              'Debit balances: cash, debtors, purchases, salaries, furniture, drawings, sales returns and rent — they add up to ' + R(dtot) + '.', 'moderate', '+'.join(str(v) for _, v in drs)),
            M('k1b', "What is Asha's capital (balancing figure)?", [R(cap), '₹60,000', '₹85,000', '₹10,000'], 0,
              f'Credit balances other than capital total ₹3,10,000. Capital = {R(dtot)} − 3,10,000 = {R(cap)}.', 'hard', f"{dtot}-310000"),
            M('k1c', 'On which side does the bank overdraft appear?', ['Credit — it is a liability', 'Debit — bank is an asset', 'Debit — it is an expense', 'It is not shown in the trial balance'], 0,
              'An overdraft means the business owes the bank, so it is a liability with a credit balance.', 'moderate'),
            M('k1d', 'Capital is entered at the figure found in the previous question. A clerk then shows sales returns of ₹4,000 on the credit side by mistake. By how much will the two totals differ?', ['₹8,000', '₹4,000', '₹2,000', '₹12,000'], 0,
              'The debit side loses 4,000 and the credit side gains 4,000 — a difference of twice the amount.', 'hard', '4000*2'),
        ]}]

    # ---------------- U4 Subsidiary books ----------------
    c = Checks()
    a_val = c.add('50000*118/100', 'invoice to Amit incl. CGST+SGST 9% each')
    igst = c.add('30000*18/100', 'IGST on Bhavna')
    tv = c.add('50000+30000', 'taxable value total')
    net_cgst = c.add('(50000-5000)*9/100', 'net output CGST after return')
    out['fnd-p1-ch02-u04'] = [{
        'id': 'k1', 'title': 'Raj Electricals — sales book with GST', 'difficulty': 'hard',
        'case': ('Raj Electricals of Jaipur (Rajasthan) is registered under GST. In October 2026 it sells goods on credit to Amit of Kota (Rajasthan) for ₹50,000 plus CGST 9% '
                 'and SGST 9%, and to Bhavna of Indore (Madhya Pradesh) for ₹30,000 plus IGST 18%. Later in the month Amit returns goods with a taxable value of ₹5,000 '
                 '(with the related tax).'),
        'mcqs': [
            M('k1a', "With what amount is Amit's account debited for the sale?", [R(a_val), '₹50,000', '₹54,500', '₹59,500'], 0,
              f'The customer is debited with the full invoice value: 50,000 + CGST 4,500 + SGST 4,500 = {R(a_val)}.', 'moderate', '50000*118/100'),
            M('k1b', 'How much IGST is charged to Bhavna?', [R(igst), '₹2,700', '₹10,800', '₹3,600'], 0,
              'The supply goes to another State, so IGST applies instead of CGST + SGST: 30,000 × 18% = ' + R(igst) + '.', 'moderate', '30000*18/100'),
            M('k1c', 'Which total from the sales book is credited to Sales Account?', [R(tv), '₹94,400', '₹85,400', '₹50,000'], 0,
              'Only the taxable value goes to Sales; the tax columns go to the Output tax accounts: 50,000 + 30,000 = ' + R(tv) + '.', 'hard', '50000+30000'),
            M('k1d', 'Which document and book record Amit\'s return?', ['Credit note issued by Raj; Sales Returns Book', 'Debit note issued by Raj; Purchases Returns Book', 'Credit note issued by Amit; Sales Book', 'Debit note issued by Raj; Sales Returns Book'], 0,
              'The seller issues a credit note to the customer (it is crediting the customer\'s account) and records it in the Sales Returns (Returns Inward) Book.', 'moderate'),
            M('k1e', 'What is the net Output CGST for October after the return?', [R(net_cgst), '₹4,500', '₹4,950', '₹7,200'], 0,
              'Output CGST is reduced on the returned goods: (50,000 − 5,000) × 9% = ' + R(net_cgst) + '. The IGST sale has no CGST.', 'hard', '(50000-5000)*9/100'),
        ]}]

    # ---------------- U5 Cash book ----------------
    c = Checks()
    da = c.add('20000-19600', 'discount allowed')
    cash = c.add('12000-9750+5000', 'closing cash')
    comm = c.add('20000*1.5/100', 'card commission')
    bank = c.add('40000+19600-5000+20000-300', 'closing bank')
    out['fnd-p1-ch02-u05'] = [{
        'id': 'k1', 'title': 'Navya Stores — a week in the three-column cash book', 'difficulty': 'hard',
        'case': ('On 1 June 2026 Navya Stores has cash in hand of ₹12,000 and a bank balance of ₹40,000. On 2 June it receives a cheque of ₹19,600 from Kiran in full settlement of '
                 '₹20,000 and deposits it the same day. On 3 June it pays Lata ₹9,750 in cash in full settlement of ₹10,000. On 4 June it withdraws ₹5,000 from the bank for office use. '
                 'On 5 June it sells goods for ₹20,000 through debit and credit cards; the bank deducts commission at 1.5%.'),
        'mcqs': [
            M('k1a', 'What is the total of the discount column on the debit side?', [R(da), '₹250', '₹650', '₹600'], 0,
              'Only Kiran\'s discount (20,000 − 19,600 = ' + R(da) + ') is allowed by Navya; Lata\'s ₹250 is discount received, on the credit side.', 'moderate', '20000-19600'),
            M('k1b', 'What is the cash balance on 5 June?', [R(cash), '₹2,250', '₹7,000', '₹17,000'], 0,
              'Cash: 12,000 − 9,750 paid to Lata + 5,000 withdrawn from the bank = ' + R(cash) + '. The discount of ₹250 is not cash, so it does not reduce the cash column.', 'hard', '12000-9750+5000'),
            M('k1c', 'What is the bank balance on 5 June?', [R(bank), '₹74,600', '₹79,300', '₹54,600'], 0,
              f'Bank: 40,000 + 19,600 − 5,000 + 20,000 card sales − commission {R(comm)} = {R(bank)}.', 'hard', '40000+19600-5000+20000-300'),
            M('k1d', 'How is the withdrawal of 4 June treated?', ['Contra entry — on both sides, marked C, not posted to the ledger', 'Debited to Drawings Account', 'Recorded only in the bank column', 'Posted to Cash Account and Bank Account in the ledger'], 0,
              'It affects the cash column and the bank column, both inside the cash book, so it is a contra entry and needs no ledger posting. It is for office use, so it is not drawings.', 'moderate'),
        ]}]

    # ---------------- U6 Rectification ----------------
    c = Checks()
    susp = c.add('2700-2000', 'suspense opening (credit)')
    eff = c.add('15000-2000', 'net effect on profit')
    out['fnd-p1-ch02-u06'] = [{
        'id': 'k1', 'title': 'Kabir & Co. — errors found after the trial balance', 'difficulty': 'hard',
        'case': ('The trial balance of Kabir & Co. on 31 March 2027 did not agree and the difference was put to a Suspense Account. Later these errors were found: '
                 '(a) the Sales Book was overcast by ₹2,000; (b) furniture bought for ₹15,000 for office use was debited to Purchases Account; '
                 '(c) cash of ₹3,000 received from Ravi was credited to his account as ₹300. After rectifying these errors the Suspense Account closed.'),
        'mcqs': [
            M('k1a', 'What was the opening balance of the Suspense Account?', [f'{R(susp)} Cr', f'{R(susp)} Dr', '₹4,700 Cr', '₹2,000 Cr'], 0,
              'Error (a) made the credit side ₹2,000 too large; error (c) made it ₹2,700 too small. Net, the credit side was short by ₹700, so the suspense account was credited with ₹700.', 'hard', '2700-2000'),
            M('k1b', 'Error (b) is an error of:', ['Principle', 'Omission', 'Commission', 'Compensation'], 0,
              'A capital expenditure (furniture) was treated as a revenue item (purchases) — the accounting principle was broken.', 'moderate'),
            M('k1c', 'What is the rectifying entry for error (c)?', ['Suspense A/c Dr. To Ravi ₹2,700', 'Ravi Dr. To Suspense A/c ₹2,700', 'Cash A/c Dr. To Ravi ₹2,700', 'Suspense A/c Dr. To Ravi ₹3,000'], 0,
              'Ravi needs a further credit of ₹2,700. Only one side was wrong, so the other side of the entry goes to Suspense.', 'hard'),
            M('k1d', 'What is the combined effect of the three rectifications on net profit (ignore depreciation)?', [f'{R(eff)} increase', '₹17,000 increase', '₹2,000 decrease', '₹15,000 increase'], 0,
              'Rectifying (a) reduces sales — profit falls by ₹2,000. Rectifying (b) reduces purchases — profit rises by ₹15,000. (c) is between personal and suspense accounts — no effect. Net: ₹13,000 increase.', 'hard', '15000-2000'),
        ]}]

    # ---------------- P2 U1 Nature of contracts ----------------
    out['fnd-p2-ch02-u01'] = [{
        'id': 'k1', 'title': 'Anil, Bina and a letter in the post', 'difficulty': 'hard',
        'case': ('On 1 March Anil posts a letter offering to sell his car to Bina for ₹4,50,000. The letter reaches Bina on 3 March. On 5 March Bina posts her letter of acceptance, '
                 'which reaches Anil on 8 March. On 6 March Bina changes her mind and telephones Anil to revoke her acceptance; Anil receives the call the same day.'),
        'mcqs': [
            M('k1a', 'When is the communication of Anil\'s offer complete?', ['On 3 March, when it comes to Bina\'s knowledge', 'On 1 March, when Anil posts it', 'On 5 March, when Bina replies', 'On 8 March, when Anil receives the reply'], 0,
              'Section 4: an offer counts as communicated only once the person it is addressed to comes to know of it — posting it is not enough.', 'moderate'),
            M('k1b', 'When is communication of the acceptance complete as against Anil?', ['On 5 March, when the letter is posted', 'On 3 March', 'On 8 March, when Anil reads it', 'On 6 March'], 0,
              'As against the proposer, it is complete when the acceptance is put in the course of transmission so that it is out of the acceptor\'s power — when Bina posts it.', 'hard'),
            M('k1c', 'When is communication of the acceptance complete as against Bina?', ['On 8 March, when it comes to Anil\'s knowledge', 'On 5 March', 'On 3 March', 'On 1 March'], 0,
              'For the acceptor, the acceptance is complete only when Anil actually learns of it — that is, when he reads the letter on 8 March.', 'hard'),
            M('k1d', 'Is Bina\'s revocation by telephone on 6 March valid?', ['Yes — it reached Anil before her acceptance came to his knowledge', 'No — the contract became binding on 5 March', 'No — an acceptance can never be revoked', 'Yes — but only because the offer was made by post'], 0,
              'Under Section 5, an acceptance may be revoked before its communication is complete as against the acceptor (8 March). The call on 6 March is in time, so there is no contract.', 'hard'),
        ]}]
    return out
