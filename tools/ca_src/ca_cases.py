"""Case-study MCQ sets (a short case + 3–5 linked MCQs) for every built CA unit — original cases, figures computed.
Schema (unit key "cases"): {id, title, difficulty, case, given?[blocks], mcqs:[{id, q, options[4], answer, explain, difficulty, check?}]}
MCQ ids are unique inside the unit (stats key: "<unit>#<mcq id>")."""
from lib import Checks, R, inr, table


def M(mid, q, options, answer, explain, difficulty='hard', check=None, topic=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'difficulty': difficulty}
    if check: d['check'] = check
    if topic: d['topic'] = topic
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
            dict(M('k1a', 'At what amount will the purchase of 2 August be recorded?', [R(pur), R(100000), R(paid), R(98000)], 0,
              'Trade discount is a reduction in the list price given on the invoice and is never recorded in the books. The purchase is recorded at the invoice value: ₹1,00,000 × 85% = ₹85,000. The tempting ₹1,00,000 records the list price, but that amount is never owed to the supplier. In practice: GST is also calculated on the price after trade discount, so the invoice figure is the base used throughout the books.', 'moderate', '100000*85/100'), topic='Journal'),
            dict(M('k1b', 'How much cash does Meera pay Vinay & Sons on 6 August?', [R(paid), R(pur), R(83000), R(98000)], 0,
              'Cash discount is calculated on the amount actually due after trade discount: ₹85,000 × 98% = ₹83,300 paid. The discount of ₹1,700 (2% of ₹85,000) is credited to Discount Received as a gain. The tempting ₹83,000 deducts 2% of the list price (₹2,000) instead of 2% of the amount due. In practice: suppliers in wholesale trade often allow such prompt-payment discounts to speed up cash collection.', 'hard', '85000*98/100'), topic='Journal'),
            dict(M('k1c', 'Which entry records the donation of 8 August?', ['Charity A/c Dr. To Purchases A/c', 'Purchases A/c Dr. To Charity A/c', 'Drawings A/c Dr. To Purchases A/c', 'Charity A/c Dr. To Cash A/c'], 0,
              'Goods donated to a school are an expense of the business, recorded as charity. The goods leave at cost, so Purchases is credited: Charity A/c Dr. To Purchases A/c ₹5,000. The tempting option debits Drawings, which would apply only if Meera took the goods for her own use. The entry crediting Cash is wrong because no cash was paid. In practice: under GST, input tax credit on goods given away free is generally blocked, so it is reversed.'), topic='Journal'),
            dict(M('k1d', 'What is the cash balance after 8 August?', [R(cash), R(115000), R(100000), R(118400)], 0,
              'The only cash movements are capital introduced of ₹2,00,000 and the payment of ₹83,300 to Vinay & Sons, so the cash balance is ₹2,00,000 − ₹83,300 = ₹1,16,700. The tempting ₹1,15,000 assumes ₹85,000 was paid, ignoring the cash discount. The donation of goods does not affect cash at all. In practice: a cash book is prepared from actual receipts and payments only, so non-cash entries such as the donation never appear in it.', 'hard', '200000-83300'), topic='Journal'),
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
            dict(M('k1a', "On which side of Sunil's account is the cash of ₹25,000 posted, and how?", ['Credit side — "By Cash"', 'Debit side — "To Cash"', 'Credit side — "To Cash"', 'Debit side — "By Cash"'], 0,
              "Sunil gives the cash, so under the personal account rule his account is credited. Credit-side postings start with 'By' followed by the name of the other account in the entry, so the posting reads 'By Cash ₹25,000'. The tempting option, 'Credit side — To Cash', has the correct side but the wrong prefix; 'To' is used only on the debit side. In practice: a customer's ledger shows each receipt as a credit with the cash or bank account named.", 'moderate'), topic='Posting'),
            dict(M('k1b', "What is the balance of Sunil's account on 30 April?", [f'{R(bal)} Dr', f'{R(bal)} Cr', '₹17,500 Dr', '₹15,000 Dr'], 0,
              "Debit side: opening balance ₹12,000 + credit sales ₹30,000 = ₹42,000. Credit side: cash ₹25,000 + returns ₹2,000 + discount ₹500 = ₹27,500. Balance = ₹42,000 − ₹27,500 = ₹14,500 Dr, meaning Sunil still owes the business. The tempting ₹15,000 Dr forgets the ₹500 discount allowed, which also reduces what Sunil owes. In practice: this closing balance is what Ojas Traders would show as Sunil's outstanding amount in its receivables ageing report.", 'hard', '12000+30000-25000-2000-500'), topic='Balancing an Account'),
            dict(M('k1c', 'Where is "Balance c/d" written when the account is closed on 30 April?', ['On the credit side', 'On the debit side', 'On both sides', 'It is not written; only b/d is shown'], 0,
              "Balance c/d is written on the lighter side to make both totals equal. Here the credit side (₹27,500) is lighter than the debit side (₹42,000), so 'By Balance c/d ₹14,500' goes on the credit side. The tempting option, the debit side, is where the balance will be brought down next month, not where it is carried down. In practice: when accounts are closed monthly, every customer account with a debit balance shows Balance c/d on its credit side.", 'moderate'), topic='Balancing an Account'),
            dict(M('k1d', 'What will be the first entry in the account on 1 May?', [f'To Balance b/d {R(bal)} on the debit side', f'By Balance b/d {R(bal)} on the credit side', 'To Sales ₹30,000 on the debit side', 'By Cash ₹25,000 on the credit side'], 0,
              "The balance carried down on the credit side on 30 April is brought down on the opposite side on 1 May: 'To Balance b/d ₹14,500' on the debit side, showing that Sunil owes this amount at the start of the new period. The tempting option, 'By Balance b/d on the credit side', would turn Sunil into a creditor. In practice: opening balances in accounting software carry forward automatically on the same side as the closing balance.", 'moderate'), topic='Balancing an Account'),
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
            dict(M('k1a', 'What is the total of the debit column of the trial balance?', [R(dtot), '₹3,10,000', '₹3,70,000', '₹3,41,000'], 0,
              "Debit balances are assets, expenses, drawings and sales returns: Cash ₹18,000 + Debtors ₹60,000 + Purchases ₹1,50,000 + Salaries ₹36,000 + Furniture ₹50,000 + Drawings ₹12,000 + Sales returns ₹4,000 + Rent ₹15,000 = ₹3,45,000. The tempting ₹3,10,000 is the credit total excluding capital. Bank overdraft is not a debit even though 'bank' sounds like an asset. In practice: accountants classify every ledger balance by its nature before extracting the trial balance.", 'moderate', '+'.join(str(v) for _, v in drs)), topic='Rules of Preparing the Trial Balance'),
            dict(M('k1b', "What is Asha's capital (balancing figure)?", [R(cap), '₹60,000', '₹85,000', '₹10,000'], 0,
              'Credit balances other than capital: Bank overdraft ₹25,000 + Creditors ₹42,000 + Sales ₹2,40,000 + Purchase returns ₹3,000 = ₹3,10,000. Capital = Debit total − Other credits = ₹3,45,000 − ₹3,10,000 = ₹35,000. The tempting ₹85,000 treats the bank overdraft as a debit. In practice: small traders often do not know their capital balance, and accountants derive it in exactly this way when setting up their books.', 'hard', f"{dtot}-310000"), topic='Rules of Preparing the Trial Balance'),
            dict(M('k1c', 'On which side does the bank overdraft appear?', ['Credit — it is a liability', 'Debit — bank is an asset', 'Debit — it is an expense', 'It is not shown in the trial balance'], 0,
              "A bank overdraft means the business has withdrawn more than its deposit, so it owes money to the bank. It is a liability and has a credit balance in the trial balance. The tempting option, 'Debit — bank is an asset', is true only when the account has a positive balance; an overdrawn account reverses this. In practice: working-capital overdraft and cash credit facilities used by Indian businesses appear under short-term borrowings in the balance sheet.", 'moderate'), topic='Rules of Preparing the Trial Balance'),
            dict(M('k1d', 'Capital is entered at the figure found in the previous question. A clerk then shows sales returns of ₹4,000 on the credit side by mistake. By how much will the two totals differ?', ['₹8,000', '₹4,000', '₹2,000', '₹12,000'], 0,
              'Sales returns of ₹4,000 should be on the debit side. Showing them on the credit side removes ₹4,000 from the debit total and adds ₹4,000 to the credit total, so the totals differ by 2 × ₹4,000 = ₹8,000. The tempting ₹4,000 counts only one side of the effect. In practice: when a trial balance differs by an even amount, accountants first look for a balance of half that amount placed on the wrong side.', 'hard', '4000*2'), topic='Rules of Preparing the Trial Balance'),
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
            dict(M('k1a', "With what amount is Amit's account debited for the sale?", [R(a_val), '₹50,000', '₹54,500', '₹59,500'], 0,
              'Amit is in Rajasthan, the same State as Raj, so CGST and SGST apply: CGST 9% = ₹4,500 and SGST 9% = ₹4,500. Amit is debited with the full invoice value: ₹50,000 + ₹4,500 + ₹4,500 = ₹59,000. The tempting ₹54,500 adds only one tax. In practice: the customer owes the whole invoice including tax, and the seller later pays the tax collected to the government.', 'moderate', '50000*118/100'), topic='Sales Book'),
            dict(M('k1b', 'How much IGST is charged to Bhavna?', [R(igst), '₹2,700', '₹10,800', '₹3,600'], 0,
              'Bhavna is in Madhya Pradesh, so the supply is inter-State and IGST is charged instead of CGST and SGST: ₹30,000 × 18% = ₹5,400. The tempting ₹2,700 is 9%, wrongly splitting the rate as if it were an intra-State supply. IGST is a single tax at the combined rate. In practice: the place of supply decides whether an invoice carries IGST or CGST plus SGST, and getting it wrong means paying the correct tax again.', 'moderate', '30000*18/100'), topic='Sales Book'),
            dict(M('k1c', 'Which total from the sales book is credited to Sales Account?', [R(tv), '₹94,400', '₹85,400', '₹50,000'], 0,
              'Sales Account is credited only with the taxable value; GST collected is a liability to the government and goes to the Output CGST, SGST and IGST accounts. Total taxable sales = ₹50,000 + ₹30,000 = ₹80,000. The tempting ₹94,400 includes the tax collected, which would overstate sales by ₹14,400 (₹9,000 + ₹5,400). In practice: GST returns report taxable value and tax separately, and the books must match them.', 'hard', '50000+30000'), topic='Sales Book'),
            dict(M('k1d', 'Which document and book record Amit\'s return?', ['Credit note issued by Raj; Sales Returns Book', 'Debit note issued by Raj; Purchases Returns Book', 'Credit note issued by Amit; Sales Book', 'Debit note issued by Raj; Sales Returns Book'], 0,
              "When a customer returns goods, the seller credits the customer's account and informs the customer through a credit note. Raj records the return in its Sales Returns (Returns Inward) Book. The tempting option, a debit note issued by Raj, is wrong because a debit note is sent by the party returning goods, here Amit. In practice: under GST, the supplier's credit note reduces its output tax liability and must be reported in its returns.", 'moderate'), topic='Sales Returns Book or Returns Inward Book'),
            dict(M('k1e', 'What is the net Output CGST for October after the return?', [R(net_cgst), '₹4,500', '₹4,950', '₹7,200'], 0,
              "Output CGST on Amit's sale was 9% of ₹50,000 = ₹4,500. The return of ₹5,000 reduces it by 9% of ₹5,000 = ₹450, so net output CGST = ₹4,050. The IGST sale to Bhavna carries no CGST. The tempting ₹4,500 ignores the credit note's tax reversal. In practice: GST-registered businesses adjust output tax for credit notes in the return of the month in which the note is issued.", 'hard', '(50000-5000)*9/100'), topic='Sales Returns Book or Returns Inward Book'),
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
            dict(M('k1a', 'What is the total of the discount column on the debit side?', [R(da), '₹250', '₹650', '₹600'], 0,
              "The debit-side discount column records discount allowed to customers. Kiran paid ₹19,600 to settle ₹20,000, so discount allowed = ₹400. Lata's ₹250 (₹10,000 − ₹9,750) is discount received, recorded on the credit side. The tempting ₹650 adds both discounts into one column. In practice: the two discount totals are posted separately — discount allowed as an expense and discount received as income.", 'moderate', '20000-19600'), topic='Kinds of Cash Book'),
            dict(M('k1b', 'What is the cash balance on 5 June?', [R(cash), '₹2,250', '₹7,000', '₹17,000'], 0,
              "Cash column: opening ₹12,000 − cash paid to Lata ₹9,750 + cash withdrawn from bank ₹5,000 = ₹7,250. Kiran's cheque was deposited directly, so it never touches the cash column, and card sales go to the bank. The tempting ₹7,000 deducts the full ₹10,000 owed to Lata instead of ₹9,750 actually paid. In practice: a shop's cash balance is checked daily against the cash physically counted in the till.", 'hard', '12000-9750+5000'), topic='Kinds of Cash Book'),
            dict(M('k1c', 'What is the bank balance on 5 June?', [R(bank), '₹74,600', '₹79,300', '₹54,600'], 0,
              "Bank column: opening ₹40,000 + Kiran's cheque ₹19,600 − withdrawal ₹5,000 + card sales ₹20,000 − commission 1.5% × ₹20,000 = ₹300, so balance = ₹74,300. The tempting ₹74,600 forgets the bank's commission on card sales. In practice: card settlements reach the merchant's bank account net of commission, so the accountant records gross sales and the commission separately.", 'hard', '40000+19600-5000+20000-300'), topic='Entries for Sale through Credit/Debit Cards'),
            dict(M('k1d', 'How is the withdrawal of 4 June treated?', ['Contra entry — on both sides, marked C, not posted to the ledger', 'Debited to Drawings Account', 'Recorded only in the bank column', 'Posted to Cash Account and Bank Account in the ledger'], 0,
              "Withdrawing cash from the bank for office use affects only the cash and bank columns, both inside the cash book: cash is debited and bank credited, marked 'C'. Because both sides of the entry are already in the cash book, nothing is posted to the ledger. The tempting option, Drawings, applies only when the owner takes money for personal use. In practice: contra vouchers in Tally record such cash withdrawals and deposits.", 'moderate'), topic='Posting the Cash Book Entries'),
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
            dict(M('k1a', 'What was the opening balance of the Suspense Account?', [f'{R(susp)} Cr', f'{R(susp)} Dr', '₹4,700 Cr', '₹2,000 Cr'], 0,
              "Error (a): the Sales Book overcast makes the credit side ₹2,000 too large. Error (c): Ravi was credited ₹300 instead of ₹3,000, making the credit side ₹2,700 too small. Net, the credit side was short by ₹2,700 − ₹2,000 = ₹700, so Suspense was credited with ₹700. Error (b) is two-sided. The tempting ₹700 Dr gets the side wrong. In practice: accountants work out each error's effect on each side before netting.", 'hard', '2700-2000'), topic='Rectification of Errors'),
            dict(M('k1b', 'Error (b) is an error of:', ['Principle', 'Omission', 'Commission', 'Compensation'], 0,
              'Furniture for office use is a capital asset, but debiting Purchases treats it as goods for resale (revenue). Treating capital expenditure as revenue breaks a basic accounting principle, so this is an error of principle. The tempting option, error of commission, involves posting to the wrong account of the same class, such as the wrong customer. In practice: such errors understate both fixed assets and profit, so auditors review large purchase entries for capital items.', 'moderate'), topic='Types of Errors'),
            dict(M('k1c', 'What is the rectifying entry for error (c)?', ['Suspense A/c Dr. To Ravi ₹2,700', 'Ravi Dr. To Suspense A/c ₹2,700', 'Cash A/c Dr. To Ravi ₹2,700', 'Suspense A/c Dr. To Ravi ₹3,000'], 0,
              'Ravi was credited with ₹300 instead of ₹3,000, so his account needs a further credit of ₹3,000 − ₹300 = ₹2,700. Cash was recorded correctly, so the other side of the rectifying entry goes to Suspense: Suspense A/c Dr. To Ravi ₹2,700. The tempting ₹3,000 credits the full amount again, ignoring the ₹300 already credited. In practice: customer statement disputes often reveal such short postings.', 'hard'), topic='Rectification of Errors'),
            dict(M('k1d', 'What is the combined effect of the three rectifications on net profit (ignore depreciation)?', [f'{R(eff)} increase', '₹17,000 increase', '₹2,000 decrease', '₹15,000 increase'], 0,
              'Rectifying (a) debits Sales ₹2,000, so profit falls by ₹2,000. Rectifying (b) moves ₹15,000 from Purchases to Furniture, reducing expenses, so profit rises by ₹15,000. Rectifying (c) affects only Ravi and Suspense, not profit. Net = ₹15,000 − ₹2,000 = ₹13,000 increase. The tempting ₹15,000 forgets the sales overcast. In practice: before finalising accounts, a CA prepares this profit impact summary for all rectifications found.', 'hard', '15000-2000'), topic='Rectification of Errors'),
        ]}]

    # ---------------- P2 U1 Nature of contracts ----------------
    out['fnd-p2-ch02-u01'] = [{
        'id': 'k1', 'title': 'Anil, Bina and a letter in the post', 'difficulty': 'hard',
        'case': ('On 1 March Anil posts a letter offering to sell his car to Bina for ₹4,50,000. The letter reaches Bina on 3 March. On 5 March Bina posts her letter of acceptance, '
                 'which reaches Anil on 8 March. On 6 March Bina changes her mind and telephones Anil to revoke her acceptance; Anil receives the call the same day.'),
        'mcqs': [
            M('k1a', 'When is the communication of Anil\'s offer complete?', ['On 3 March, when it comes to Bina\'s knowledge', 'On 1 March, when Anil posts it', 'On 5 March, when Bina replies', 'On 8 March, when Anil receives the reply'], 0,
              'Section 4: an offer is communicated only once the offeree actually learns of it. Bina learnt of it on 3 March. The tempting trap is 1 March, the posting date — posting completes an acceptance against the offeror, not an offer. In practice: when a client emails a quotation, it is an offer only once the customer receives it, so a reply sent before that is not an acceptance.', 'moderate', topic='Communication of Offer and Acceptance'),
            M('k1b', 'When is communication of the acceptance complete as against Anil?', ['On 5 March, when the letter is posted', 'On 3 March', 'On 8 March, when Anil reads it', 'On 6 March'], 0,
              'Section 4: the proposer is bound once the acceptance leaves the acceptor\'s control on its way to him — here when Bina posts it on 5 March. Anil is bound from then. The tempting trap is 8 March, when Anil reads it; that is the moment it binds Bina. In practice: an offeror who has invited acceptance by post cannot ignore a posted acceptance merely because the letter is still in transit.', 'hard', topic='Communication of Offer and Acceptance'),
            M('k1c', 'When is communication of the acceptance complete as against Bina?', ['On 8 March, when it comes to Anil\'s knowledge', 'On 5 March', 'On 3 March', 'On 1 March'], 0,
              'Section 4: the acceptor is bound only once the proposer actually learns of the acceptance — when the letter reaches Anil on 8 March. The tempting trap is 5 March, the posting date, which binds only Anil. Until 8 March Bina still has a window to revoke. In practice: a business that has posted an acceptance can still withdraw it by a faster channel, such as email, that arrives before the letter.', 'hard', topic='Communication of Offer and Acceptance'),
            M('k1d', 'Is Bina\'s revocation by telephone on 6 March valid?', ['Yes — it reached Anil before her acceptance came to his knowledge', 'No — the contract became binding on 5 March', 'No — an acceptance can never be revoked', 'Yes — but only because the offer was made by post'], 0,
              'Section 5: an acceptor may withdraw the acceptance until it binds her — here, until 8 March. Bina\'s call reached Anil on 6 March, so the revocation is valid and no contract arises. The tempting trap is "the contract became binding on 5 March"; posting binds only the offeror, not the acceptor. In practice: urgent revocations are sent by phone or email and then confirmed in writing to prove they arrived first.', 'hard', topic='Revocation of Offer and Acceptance'),
        ]}]
    return out
