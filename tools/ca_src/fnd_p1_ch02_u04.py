"""CA Foundation · Paper 1 · Chapter 2 · Unit 4 Subsidiary Books (original content)."""
from lib import *

UID = 'fnd-p1-ch02-u04'


def book(title, rows, note_=None, inv='Invoice No.'):
    """rows: (date, particulars, invoice, amount) -> table with total row"""
    tot = sum(r[3] for r in rows)
    body = [[d, part, ino, '', inr(a)] for d, part, ino, a in rows] + [['', 'Total (posted to the ledger)', '', '', inr(tot)]]
    return table(['Date', 'Particulars', inv, 'L.F.', 'Amount (₹)'], body, num=[4], total=True, title=title, note=note_), tot


def build():
    # ---------- Illustration 1: purchases and sales books ----------
    c1 = Checks()
    p1 = c1.add('(200*260+50*180)*90/100', 'Modern Paper Mills, 2 Oct (less 10% trade discount)')
    p2 = c1.add('100*45', 'Sharma Office Supplies, 5 Oct')
    p3 = c1.add('80*260*90/100', 'Modern Paper Mills, 18 Oct')
    pb, ptot = book('Purchases Book of Vinayak Stationers (October 2026)', [
        ('Oct 2', 'Modern Paper Mills — 200 reams A4 @ ₹260 = ₹52,000; 50 boxes pens @ ₹180 = ₹9,000; less trade discount 10% ₹6,100', 'P-118', p1),
        ('Oct 5', 'Sharma Office Supplies — 100 files @ ₹45', 'SOS-77', p2),
        ('Oct 18', 'Modern Paper Mills — 80 reams A4 @ ₹260 = ₹20,800; less trade discount 10% ₹2,080', 'P-131', p3)])
    c1.add('54900+4500+18720', 'Purchases book total')
    s1 = c1.add('(120*300+30*220)*95/100', 'Greenfield School, 7 Oct (less 5%)')
    s2 = c1.add('60*60', 'Lotus Coaching, 15 Oct')
    s3 = c1.add('40*300*95/100', 'Greenfield School, 26 Oct (less 5%)')
    sb, stot = book('Sales Book of Vinayak Stationers (October 2026)', [
        ('Oct 7', 'Greenfield School — 120 reams @ ₹300 = ₹36,000; 30 boxes pens @ ₹220 = ₹6,600; less trade discount 5% ₹2,130', 'VS-201', s1),
        ('Oct 15', 'Lotus Coaching — 60 files @ ₹60', 'VS-202', s2),
        ('Oct 26', 'Greenfield School — 40 reams @ ₹300 = ₹12,000; less trade discount 5% ₹600', 'VS-203', s3)])
    c1.add('40470+3600+11400', 'Sales book total')
    jp = journal([je('Oct 9', [('Photocopier A/c', 85000)], [('Copytech Ltd', 85000)], 'Being photocopier bought on credit for office use'),
                  je('Oct 21', [('Raj', 5000)], [('Furniture A/c', 5000)], 'Being old office furniture sold on credit at book value')], 'Journal Proper (entries that fit no other book)', 'jp1')
    post1 = table(['Ledger account', 'Debit (₹)', 'Credit (₹)'], [
        ['Purchases A/c (monthly total)', inr(ptot), ''], ['Modern Paper Mills', '', inr(p1 + p3)], ['Sharma Office Supplies', '', inr(p2)],
        ['Greenfield School', inr(s1 + s3), ''], ['Lotus Coaching', inr(s2), ''], ['Sales A/c (monthly total)', '', inr(stot)],
        ['Total', inr(ptot + s1 + s3 + s2), inr(p1 + p3 + p2 + stot)]], num=[1, 2], total=True, title='How the books are posted')

    # ---------- Illustration 2: returns books ----------
    c2 = Checks()
    r1 = c2.add('10*260*90/100', 'Debit note to Modern Paper Mills (10 reams at net price)')
    r2 = c2.add('5*300*95/100', 'Credit note to Greenfield School (5 reams at net price)')
    rob, _ = book('Purchase Returns (Returns Outward) Book', [('Oct 20', 'Modern Paper Mills — 10 reams A4 found damp, @ ₹260 less 10%', 'DN-07', r1)], inv='Debit Note No.')
    rib, _ = book('Sales Returns (Returns Inward) Book', [('Oct 28', 'Greenfield School — 5 reams returned, @ ₹300 less 5%', 'CN-03', r2)], inv='Credit Note No.')

    # ---------- Illustration 3: sales book with GST ----------
    c3 = Checks()
    g = [('Oct 4', 'Mehul Traders (same State)', 'SE-41', 40000, 'intra'), ('Oct 11', 'Delta Retail (another State)', 'SE-42', 60000, 'inter'), ('Oct 22', 'Kiran & Sons (same State)', 'SE-43', 25000, 'intra')]
    rows, T = [], [0, 0, 0, 0, 0]
    for d, n, ino, v, k in g:
        cg = sg = ig = 0
        if k == 'intra': cg = sg = c3.add(f'{v}*9/100', f'CGST (= SGST) on {inr(v)}')
        else: ig = c3.add(f'{v}*18/100', f'IGST on {inr(v)}')
        tot = v + cg + sg + ig
        for i, x in enumerate([v, cg, sg, ig, tot]): T[i] += x
        rows.append([d, n, ino, inr(v), inr(cg) if cg else '–', inr(sg) if sg else '–', inr(ig) if ig else '–', inr(tot)])
    rows.append(['', 'Total', '', *[inr(x) for x in T]])
    c3.add('40000+60000+25000', 'Taxable value total (credited to Sales A/c)')
    c3.add('3600+2250', 'Output CGST total')
    c3.add('47200+70800+29500', 'Total receivable from customers')
    gst_book = table(['Date', 'Customer', 'Invoice', 'Taxable value (₹)', 'Output CGST 9% (₹)', 'Output SGST 9% (₹)', 'Output IGST 18% (₹)', 'Total (₹)'], rows, num=[3, 7], total=True,
                     title='Sales Book of Sanvi Electronics with GST columns (October 2026)', note='Tax columns with "–" have no tax of that kind. Their totals: CGST ₹5,850, SGST ₹5,850, IGST ₹10,800.')

    # ---------- Q1 ----------
    q1c = Checks()
    a = q1c.add('(300*40)*95/100', 'Jai Hind Mills, 3 Nov')
    b = q1c.add('150*120', 'Bose & Co., 10 Nov')
    c = q1c.add('(80*55+40*90)*90/100', 'Parmar Stores, 6 Nov')
    d = q1c.add('120*55*90/100', 'Mittal Bros., 19 Nov')
    e = q1c.add('20*40*95/100', 'Return to Jai Hind Mills, 8 Nov')
    f = q1c.add('10*55*90/100', 'Return from Parmar Stores, 12 Nov')
    qp, qpt = book('Purchases Book of Harsh Traders (November 2026)', [('Nov 3', 'Jai Hind Mills — 300 metres cotton cloth @ ₹40; less 5% trade discount', '—', a), ('Nov 10', 'Bose & Co. — 150 metres silk @ ₹120', '—', b)])
    qs, qst = book('Sales Book of Harsh Traders (November 2026)', [('Nov 6', 'Parmar Stores — 80 metres cotton @ ₹55, 40 metres silk @ ₹90; less 10% trade discount', '—', c), ('Nov 19', 'Mittal Bros. — 120 metres cotton @ ₹55; less 10% trade discount', '—', d)])
    qro, _ = book('Purchase Returns Book', [('Nov 8', 'Jai Hind Mills — 20 metres cotton @ ₹40 less 5%', '—', e)], inv='Debit Note No.')
    qri, _ = book('Sales Returns Book', [('Nov 12', 'Parmar Stores — 10 metres cotton @ ₹55 less 10%', '—', f)], inv='Credit Note No.')
    q1c.add('11400+18000', 'Purchases book total')
    q1c.add('7200+5940', 'Sales book total')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch02', 'n': 4, 'title': 'Subsidiary Books',
        'outcomes': ['Explain why the journal is split into subsidiary books and how this helps division of work and control.', 'Record credit purchases, credit sales and returns in the purchases, sales and returns books at net (after trade discount) values.',
                     'Post the subsidiary books: monthly totals to the nominal accounts and individual amounts to the parties.', 'Identify transactions that belong in the journal proper, and add GST columns to subsidiary books.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 45}, 'prereq': ['fnd-p1-ch02-u02'],
                 'exam_tip': 'The most common trap: putting a credit purchase of an asset, or a cash purchase, into the purchases book. Only credit purchases of goods go there.'},
        'concepts': [
            {'id': 'c1', 'title': 'Why split the journal?', 'body': ['A busy business has hundreds of similar transactions. Recording them all in one journal is slow and hard to post. So similar transactions are grouped into separate "subsidiary" (special) books.',
                                                                   'Benefits: work can be divided among staff; posting is faster because only totals go to the nominal account; errors are easier to locate; and each book gives instant information (total credit sales this month, for example).'],
             'analogy': 'A hospital has separate counters for registration, pharmacy and billing instead of one long queue — faster, and everyone knows where to look.', 'work': 'Modern software keeps "registers" — purchase register, sales register, debit note register. These are subsidiary books under another name, and auditors download them first.'},
            {'id': 'c2', 'title': 'Purchases book', 'body': ['Records only credit purchases of goods (goods bought for resale or for production). Entries are made from supplier invoices, at the net amount after trade discount.',
                                                         'Posting: each supplier\'s account is credited with its invoice amount; the monthly total is debited to Purchases Account.',
                                                         'Not recorded here: cash purchases (cash book) and purchases of assets on credit (journal proper).'],
             'analogy': 'A list of everything you bought on "khata" (credit) for your shop shelves.', 'work': 'Before an invoice is entered, accounts teams match it with the purchase order and the goods received note — the "three-way match" that prevents paying for goods never received.'},
            {'id': 'c3', 'title': 'Sales book', 'body': ['Records only credit sales of goods, from copies of the invoices issued, at net value after trade discount.',
                                                     'Posting: each customer\'s account is debited; the monthly total is credited to Sales Account. Cash sales go to the cash book; credit sale of an old asset goes to the journal proper.'],
             'analogy': 'The mirror image of the purchases book — what customers took on credit.', 'work': 'At the year end auditors check "cut-off": invoices dated 31 March must relate to goods actually dispatched by 31 March, otherwise sales are overstated.'},
            {'id': 'c4', 'title': 'Returns books, debit notes and credit notes', 'body': ['Purchase Returns (Returns Outward) Book: goods returned to suppliers. The buyer sends a debit note — "we are debiting your account". Posting: supplier debited; total credited to Purchase Returns Account.',
                                                                                        'Sales Returns (Returns Inward) Book: goods returned by customers. The seller issues a credit note — "we are crediting your account". Posting: customer credited; total debited to Sales Returns Account.',
                                                                                        'Returns are valued at the same net price at which the goods were bought or sold.'],
             'analogy': 'A debit note says "I am reducing what I owe you"; a credit note says "I am reducing what you owe me".', 'work': 'Unmatched debit notes are a frequent cause of differences in supplier balance confirmations — the supplier simply has not recorded the return yet.'},
            {'id': 'c5', 'title': 'Journal proper', 'body': ['Entries that do not fit any subsidiary book still go to the journal: opening and closing entries, adjustment entries (outstanding, prepaid, depreciation), rectification entries, transfer entries, and credit purchase or sale of assets.',
                                                         'Also: goods withdrawn by the owner, goods lost by fire or theft, bad debts written off and interest on capital or drawings.'],
             'analogy': 'The "miscellaneous" drawer — small, but you cannot run the house without it.', 'work': 'Auditors look closely at journal entries passed at the year end, because unusual adjustments here can change profit significantly.'},
            {'id': 'c6', 'title': 'GST columns in subsidiary books', 'body': ['A GST-registered business adds columns for the taxable value and each tax: CGST and SGST (supply within the State) or IGST (supply to another State).',
                                                                          'Posting: taxable value total to Sales (or Purchases); tax column totals to the Output (or Input) tax accounts; the full invoice value to each party.'],
             'blocks': [gst_book], 'analogy': 'Same book, a few more columns — like a restaurant bill that shows the food total and the taxes separately.', 'work': 'GST returns are built from these registers. If the sales register and the GST return do not match, the department asks why.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Purchases book, sales book and journal proper', 'difficulty': 'core', 'minutes': 15,
             'q': 'Vinayak Stationers, October 2026. Record in the proper books: Oct 2 — bought from Modern Paper Mills on credit 200 reams A4 @ ₹260 and 50 boxes of pens @ ₹180, trade discount 10%. Oct 5 — bought 100 files @ ₹45 from Sharma Office Supplies on credit. Oct 7 — sold to Greenfield School on credit 120 reams @ ₹300 and 30 boxes of pens @ ₹220, trade discount 5%. Oct 9 — bought a photocopier on credit from Copytech Ltd ₹85,000. Oct 12 — bought envelopes for cash ₹3,000. Oct 15 — sold 60 files @ ₹60 to Lotus Coaching on credit. Oct 18 — bought 80 reams @ ₹260 from Modern Paper Mills, trade discount 10%. Oct 21 — sold old furniture to Raj on credit for its book value ₹5,000. Oct 26 — sold 40 reams @ ₹300 to Greenfield School, trade discount 5%.',
             'solution': [pb, sb, jp, note('The cash purchase of envelopes (12 Oct) is recorded in the cash book, not in the purchases book.'), post1], 'checks': c1},
            {'id': 'i2', 'title': 'Returns books', 'difficulty': 'core', 'minutes': 6,
             'q': 'Continuing: Oct 20 — returned 10 reams from the 18 October lot to Modern Paper Mills as damp. Oct 28 — Greenfield School returned 5 reams from the 26 October sale. Record in the returns books and show the posting.',
             'solution': [rob, rib, ul([f'Modern Paper Mills debited ₹{inr(r1)}; Purchase Returns A/c credited ₹{inr(r1)} (month total).', f'Greenfield School credited ₹{inr(r2)}; Sales Returns A/c debited ₹{inr(r2)} (month total).'])], 'checks': c2},
            {'id': 'i3', 'title': 'Sales book with GST columns', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'Sanvi Electronics made these credit sales in October 2026 (GST 18%): Oct 4 — Mehul Traders, same State, ₹40,000; Oct 11 — Delta Retail, another State, ₹60,000; Oct 22 — Kiran & Sons, same State, ₹25,000. Prepare the sales book with GST columns.',
             'solution': [gst_book, ul(['Sales A/c credited ₹1,25,000 (taxable value).', 'Output CGST A/c and Output SGST A/c credited ₹5,850 each; Output IGST A/c credited ₹10,800.', 'Each customer debited with the invoice total.'])], 'checks': c3},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Entering supplier invoices the right way', 'role': 'Accounts payable executive in a manufacturing company', 'situation': 'A stack of 40 supplier invoices arrives. Two have no purchase order, one bills 500 units though the stores received 480, and one is for a new air conditioner for the office.',
             'steps': ['Match each invoice with its purchase order and goods received note (three-way match).', 'Hold the invoices without a purchase order and ask the buyer to confirm.', 'For the short supply, enter the full invoice and raise a debit note for 20 units — or ask the supplier for a revised invoice.',
                       'The air conditioner is an asset: it goes through the journal (or asset register), not the purchases register.'],
             'takeaway': 'Subsidiary book rules are internal controls in disguise — they stop wrong or fake purchases from reaching the accounts.', 'think': 'Why should the person who enters invoices not be the person who approves payments?',
             'answer': 'Separating duties means one person alone cannot both create a liability and pay it — it reduces the chance of fraud or error going unnoticed.'},
            {'id': 'j2', 'title': 'Sales cut-off test at the year end', 'role': 'Articled assistant (statutory audit)', 'situation': 'Your senior asks you to test sales cut-off for a distributor. You select invoices dated 28 March to 4 April.',
             'steps': ['For each invoice, check the dispatch document (delivery challan, transport receipt) date.', 'Invoices dated before 31 March but goods sent in April overstate this year\'s sales.', 'Also check credit notes issued in April for goods returned that were sold in March.', 'Summarise misstatements and propose adjustments.'],
             'takeaway': 'The sales book records invoices — the auditor checks that each invoice really belongs to the year.', 'think': 'An invoice for ₹2,00,000 is dated 31 March but the goods left on 2 April. What is the effect on this year\'s accounts?',
             'answer': 'Sales and debtors are overstated by ₹2,00,000 (and closing stock understated by its cost), so profit is overstated by the margin on that sale.'},
        ],
        'mcqs': [
            {'id': 'm1', 'q': 'Credit purchase of furniture for office use is recorded in the:', 'options': ['Journal proper', 'Purchases book', 'Cash book', 'Purchase returns book'], 'answer': 0, 'explain': 'The purchases book is only for goods bought on credit. An asset bought on credit goes to the journal proper.', 'concept': 'c5', 'difficulty': 'core'},
            {'id': 'm2', 'q': 'The total of the sales book is posted to:', 'options': ['The credit side of Sales Account', 'The debit side of Sales Account', 'The credit side of each customer\'s account', 'The debit side of Cash Account'], 'answer': 0, 'explain': 'Customers are debited individually; the period total is credited to Sales Account.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm3', 'q': 'When goods are returned to a supplier, the buyer sends a:', 'options': ['Debit note', 'Credit note', 'Invoice', 'Receipt'], 'answer': 0, 'explain': 'The buyer debits the supplier\'s account and informs the supplier through a debit note.', 'concept': 'c4', 'difficulty': 'core'},
            {'id': 'm4', 'q': 'Goods with a list price of ₹24,000 are sold on credit at 15% trade discount. The amount entered in the sales book is:', 'options': ['₹20,400', '₹24,000', '₹3,600', '₹27,600'], 'answer': 0, 'check': '24000*85/100', 'explain': 'Trade discount is deducted before recording: 24,000 × 85% = ₹20,400.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm5', 'q': 'Which transaction is recorded in the purchases book of a furniture dealer?', 'options': ['Furniture bought on credit for resale', 'Furniture bought for cash for resale', 'A computer bought on credit for the office', 'Furniture returned to the supplier'], 'answer': 0, 'explain': 'For a furniture dealer, furniture is stock-in-trade. Bought on credit, it goes to the purchases book.', 'concept': 'c2', 'difficulty': 'moderate'},
            {'id': 'm6', 'q': 'The total of the sales returns book is posted to:', 'options': ['The debit side of Sales Returns Account', 'The credit side of Sales Returns Account', 'The debit side of Sales Account', 'The credit side of Purchases Account'], 'answer': 0, 'explain': 'Sales returns reduce sales, so Sales Returns Account is debited with the total; customers are credited.', 'concept': 'c4', 'difficulty': 'core'},
            {'id': 'm7', 'q': 'An intra-State credit sale of ₹50,000 attracts CGST and SGST of 6% each. The customer is debited with:', 'options': ['₹56,000', '₹53,000', '₹50,000', '₹62,000'], 'answer': 0, 'check': '50000+50000*6/100*2', 'explain': 'CGST 3,000 + SGST 3,000 = 6,000; invoice total ₹56,000.', 'concept': 'c6', 'difficulty': 'core'},
            {'id': 'm8', 'q': 'An entry for depreciation on machinery is made in the:', 'options': ['Journal proper', 'Purchases book', 'Sales book', 'Cash book'], 'answer': 0, 'explain': 'Adjustment entries like depreciation fit no special book, so they go to the journal proper.', 'concept': 'c5', 'difficulty': 'core'},
        ],
        'questions': [
            {'id': 'q1', 'marks': 8, 'minutes': minutes(8), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Harsh Traders deal in cloth. Record the following in the appropriate subsidiary books for November 2026: Nov 3 — bought from Jai Hind Mills 300 metres of cotton cloth @ ₹40, trade discount 5%. Nov 6 — sold to Parmar Stores 80 metres cotton @ ₹55 and 40 metres silk @ ₹90, trade discount 10%. Nov 8 — returned 20 metres of cotton to Jai Hind Mills. Nov 10 — bought from Bose & Co. 150 metres silk @ ₹120. Nov 12 — Parmar Stores returned 10 metres cotton. Nov 19 — sold to Mittal Bros. 120 metres cotton @ ₹55, trade discount 10%. All transactions are on credit.',
             'model': [qp, qs, qro, qri],
             'scheme': [{'id': 's1', 'pt': 'Purchases book: ₹11,400 and ₹18,000, total ₹29,400', 'm': 2, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Sales book: ₹7,200 and ₹5,940, total ₹13,140', 'm': 2, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Purchase returns ₹760 at net price, with debit note', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Sales returns ₹495 at net price, with credit note', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's5', 'pt': 'Proper columns (Date, Particulars, Invoice/Note No., L.F., Amount) and totals', 'm': 1, 'skill': 'presentation'}],
             'checks': q1c,
             'remarks': ['Returns valued at the gross price (without the trade discount) are the most common error.', 'Candidates who show details (quantity × rate − discount) in the particulars get step marks even if the final figure is wrong.'],
             'mistakes': ['Valuing returns at list price.', 'Recording the trade discount as a separate amount in the total.', 'Mixing returns into the purchases or sales book.'],
             'tips': ['Show the calculation inside the particulars column.', 'Total every book and write "Total" clearly.']},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
             'q': 'Name the book of original entry for each transaction of a garment dealer: (a) shirts bought on credit; (b) shirts bought for cash; (c) a sewing machine bought on credit for repairs; (d) goods returned by a customer; (e) cash sale of trousers; (f) goods returned to a supplier; (g) depreciation on furniture; (h) jackets sold on credit.',
             'model': [table(['Transaction', 'Book'], [['(a) Shirts bought on credit', 'Purchases book'], ['(b) Shirts bought for cash', 'Cash book'], ['(c) Sewing machine on credit', 'Journal proper'], ['(d) Return by a customer', 'Sales returns book'],
                                                       ['(e) Cash sale of trousers', 'Cash book'], ['(f) Return to a supplier', 'Purchase returns book'], ['(g) Depreciation on furniture', 'Journal proper'], ['(h) Jackets sold on credit', 'Sales book']])],
             'scheme': [{'id': f's{i+1}', 'pt': f'({chr(97+i)}) correct book', 'm': 0.5, 'skill': 'classification'} for i in range(8)],
             'remarks': ['Most errors come from (c): a sewing machine is an asset for a garment dealer, not stock.'], 'mistakes': ['Putting cash purchases in the purchases book.', 'Putting depreciation in the cash book.'], 'tips': ['Ask two questions: is it goods? Is it on credit?']},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': 'What is the journal proper? Give four kinds of entries that are recorded in it, with one example each.',
             'model': [p('The journal proper is the book in which transactions that cannot be recorded in any subsidiary book (cash book, purchases, sales, returns books) are entered.'),
                       ul(['Opening entry — bringing forward last year\'s asset and liability balances.', 'Adjustment entries — outstanding salary, prepaid insurance, depreciation.', 'Rectification entries — correcting a sale wrongly posted to another customer.', 'Credit purchase or sale of assets — machinery bought on credit.', 'Transfer and closing entries — transferring expenses to the Profit and Loss Account.'])],
             'scheme': [{'id': 's1', 'pt': 'Meaning of journal proper', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': 'Four kinds of entries', 'm': 2, 'skill': 'concept'}, {'id': 's3', 'pt': 'An example for each', 'm': 1, 'skill': 'application'}],
             'remarks': ['Answers without examples lose a quarter of the marks.'], 'mistakes': ['Listing cash transactions as journal proper entries.'], 'tips': ['Name the entry type in bold, then give the example.']},
        ],
        'revision': {'summary': ['Subsidiary books group similar transactions: purchases, sales, purchase returns, sales returns (plus the cash book).', 'Purchases and sales books record only credit transactions in goods, at net value after trade discount.',
                                 'Parties are posted individually; the period total goes to the nominal account.', 'Returns: debit note (to supplier), credit note (to customer), valued at net price.', 'Everything else goes to the journal proper.'],
                     'remember': ['Purchases book → total debited to Purchases A/c.', 'Sales book → total credited to Sales A/c.', 'Returns outward → supplier debited; Returns inward → customer credited.'],
                     'traps': ["Don't record assets or cash transactions in the purchases or sales book.", "Don't value returns at list price.", "Don't show trade discount as a separate posting."]},
        'quickref': [{'k': 'Purchases book', 'v': 'Credit purchases of goods only'}, {'k': 'Sales book', 'v': 'Credit sales of goods only'}, {'k': 'Debit note', 'v': 'Sent by buyer when goods are returned to the supplier'},
                     {'k': 'Credit note', 'v': 'Issued by seller when a customer returns goods'}, {'k': 'Journal proper', 'v': 'Opening, adjustment, rectification, transfer, closing entries; credit purchase/sale of assets'},
                     {'k': 'GST columns', 'v': 'Taxable value | CGST | SGST | IGST | Total'}],
    }
