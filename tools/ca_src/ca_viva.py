"""Viva (speak & revise) questions for every built CA unit — original wording.
Each question: id, q (read aloud), model (a spoken-style model answer), concept (optional), points[] key points.
Key point: id, pt (shown to the student), w (weight), kw (keyword groups, '|' = synonyms), min (groups needed; default all).
The matcher is tools/ca_vivamatch.py (twin of the JS one). tools/ca_validate.py proves each model answer scores 100%."""
import re



def P(pid, pt, w, *kw, min=None):
    d = {'id': pid, 'pt': pt, 'w': w, 'kw': list(kw)}
    if min is not None: d['min'] = min
    return d


def ALT(*templates, **subs):
    """Expand '{x}' slots in phrase templates with every synonym given for x, joined by '|'."""
    out = []
    for t in templates:
        combos = ['']
        parts = re.split(r'\{(\w+)\}', t)
        for i, part in enumerate(parts):
            opts = subs[part] if i % 2 else [part]
            combos = [c + o for c in combos for o in opts]
        out += combos
    return '|'.join(dict.fromkeys(out))


COME = ('come in', 'comes in', 'coming in', 'came in')
GO = ('go out', 'goes out', 'going out', 'went out')
PROP = ('proposer', 'offeror', 'promisor')


def V(vid, q, model, points, concept=None):
    d = {'id': vid, 'q': q, 'model': model, 'points': points}
    if concept: d['concept'] = concept
    return d


VIVA = {
    # ------------------------------------------------------------------ P1 Ch2 U1 Journal entries
    'fnd-p1-ch02-u01': [
        V('v1', 'What is the double entry system of book-keeping?',
          'Under the double entry system every transaction has two aspects, so at least two accounts are affected. One account is debited and another is credited with the same amount. Because every debit has an equal credit, the total of all debits equals the total of all credits, which lets us check arithmetical accuracy through a trial balance.',
          [P('p1', 'Every transaction has two aspects / affects at least two accounts', 3, 'two aspect|dual aspect|two account|two effect|twofold|both aspect'),
           P('p2', 'One account is debited and another credited with an equal amount', 4, 'debit', 'credit', 'same amount|equal amount|equal|same'),
           P('p3', 'Total debits equal total credits — a check on arithmetical accuracy (trial balance)', 3, 'total debit|total of all debit|all debit', 'trial balance|arithmetical accuracy|arithmetic|accuracy', min=1)], 'c1'),
        V('v2', 'State the three golden rules of the traditional approach.',
          'For a personal account, debit the receiver and credit the giver. For a real account, debit what comes in and credit what goes out. For a nominal account, debit all expenses and losses and credit all incomes and gains.',
          [P('p1', 'Personal account: debit the receiver, credit the giver', 4, 'personal', 'debit receiver credit giver|receiver debit giver credit|debit receiver credit the giver|credit giver debit receiver'),
           P('p2', 'Real account: debit what comes in, credit what goes out', 3, 'real', ALT('debit {c} credit {g}', 'debit what {c} credit what {g}', '{c} debit {g} credit', c=COME, g=GO)),
           P('p3', 'Nominal account: debit expenses and losses, credit incomes and gains', 3, 'nominal', 'debit expens|debit all expens|expens loss debit|expens debit|expens and loss debit', 'credit incom|credit all incom|incom gain credit|incom credit|incom and gain credit')], 'c4'),
        V('v3', 'How are trade discount and cash discount treated in the books of account?',
          'Trade discount is not recorded at all; the transaction is entered at the net price after deducting it. Cash discount is recorded. The seller debits it to Discount Allowed Account as a loss, and the buyer credits it to Discount Received Account as a gain.',
          [P('p1', 'Trade discount is not recorded — entry at the net price', 4, 'trade discount not record|trade discount never record|trade discount no entry|trade discount not enter|trade discount not shown|trade discount ignor|not record trade discount|net price|net amount|net invoice'),
           P('p2', 'Cash discount is recorded in the books', 2, 'cash discount record|cash discount enter|cash discount shown|cash discount journalis|record cash discount'),
           P('p3', 'Seller: Discount Allowed (loss); buyer: Discount Received (gain)', 4, 'seller discount allow|discount allow seller|allowed by seller', 'buyer discount receiv|discount receiv buyer|received by buyer')], 'c5'),
        V('v4', 'Goods costing five thousand rupees are taken by the proprietor for his own use. What entry is passed, and why?',
          'Drawings Account is debited and Purchases Account is credited with 5,000 rupees, the cost price. The proprietor is the receiver, so Drawings is debited, and the goods have gone out of the business, so they are credited to Purchases at cost and not to Sales.',
          [P('p1', 'Drawings Account debited, Purchases Account credited (not Sales)', 6, 'drawing debit purchas|debit drawing credit purchas|purchas credit drawing debit|credit purchas debit drawing|drawing account debit purchas'),
           P('p2', 'Recorded at cost — ₹5,000', 2, 'cost|5000', min=1),
           P('p3', 'Reason: proprietor receives the goods; goods leave the business', 2, 'receiver|receives|personal use|own use|reduce capital|reduces capital|gone out|go out|goes out|leave', min=1)], 'c5'),
        V('v5', 'Explain input tax, output tax and set-off under GST in the books of a registered trader.',
          'Input tax is the GST paid on purchases; it is recoverable, so the Input CGST and Input SGST accounts are debited like an asset. Output tax is the GST charged on sales; it is payable to the government, so the Output tax accounts are credited as a liability. At the end of the period input tax is set off against output tax, and only the balance is paid. CGST credit cannot be used to pay SGST and SGST credit cannot be used to pay CGST.',
          [P('p1', 'Input tax = GST paid on purchases — debited, recoverable (asset)', 3, 'input paid|input purchas|input gst paid|input tax gst paid|input tax on purchas', 'debit|asset|recoverable'),
           P('p2', 'Output tax = GST charged on sales — credited, payable (liability)', 3, 'output charg|output collect|output sale|output tax gst charg|output tax gst collect|output tax on sale', 'credit|liability|payable'),
           P('p3', 'Input set off against output; only the balance is paid', 2, 'set off|setoff|adjust|offset', 'balance|net|remaining|difference', min=1),
           P('p4', 'CGST credit cannot pay SGST, and vice versa', 3, 'sgst', 'cgst cannot|cgst not|cgst can t|cgst cant|cannot cgst|not cgst|cannot cross|not cross|no cross')], 'c6'),
    ],
    # ------------------------------------------------------------------ P1 Ch2 U2 Ledgers
    'fnd-p1-ch02-u02': [
        V('v1', 'What is a ledger, and why is it called the principal book of account?',
          'A ledger is a book that groups all transactions account by account, so each account shows its complete history in one place, while the journal keeps them in date order. It is called the principal book because the trial balance and the final accounts are prepared from the ledger balances.',
          [P('p1', 'Groups transactions account by account (classified record)', 4, 'account by account|account wise|accountwise|each account|every account|classified|grouped|groups'),
           P('p2', 'Journal is chronological; ledger is by account', 2, 'journal', 'date order|chronological|date wise|datewise|order of date|date', min=2),
           P('p3', 'Trial balance and final accounts are prepared from it', 4, 'trial balance|final account|financial statement|balance sheet|profit loss', min=1)], 'c1'),
        V('v2', 'Explain the rules for posting a journal entry into the ledger.',
          'The account debited in the journal is posted on its debit side, writing To and the name of the account credited. The account credited in the journal is posted on its credit side, writing By and the name of the account debited. Each posting carries the date, the journal folio and the amount.',
          [P('p1', 'Debited account: entry on its debit side with "To" + name of the credited account', 4, 'debit side name account credit|debit side name credit account|debit side account debit write credit account|debit side account debit credit account|debit side credit account name|debit side credited account name'),
           P('p2', 'Credited account: entry on its credit side with "By" + name of the debited account', 4, 'credit side name account debit|credit side name debit account|credit side account credit write debit account|credit side account credit debit account|credit side debit account name|credit side debited account name'),
           P('p3', 'Date, journal folio and amount are written', 2, 'date|folio|jf|journal folio|amount', min=1)], 'c2'),
        V('v3', 'What does balancing an account mean? Describe the steps.',
          'Balancing means finding the difference between the two sides of an account. First total both sides. Write the difference on the side with the smaller total as Balance carried down, so the totals agree. Then bring the same amount down on the opposite side as Balance brought down at the start of the next period.',
          [P('p1', 'Total both sides and find the difference', 3, 'total|add|difference', 'both side|two side|each side|debit and credit', min=1),
           P('p2', 'Difference written on the lighter (smaller) side as Balance c/d', 4, 'smaller|lighter|lesser|shorter|less', 'carried down|c d|cd|carried forward', min=2),
           P('p3', 'Brought down on the opposite side as Balance b/d next period', 3, 'brought down|b d|bd|brought forward', 'opposite|other side|next period|next year|beginning|start', min=2)], 'c3'),
        V('v4', 'At the year end, which accounts are balanced and carried forward, and which are closed?',
          'Personal and real accounts are balanced and carried forward — debtors, creditors, capital, cash and other assets — and each balance becomes the opening figure of the next year. Nominal accounts are not carried forward; expenses, losses, incomes and gains are closed by transferring them to the Trading or Profit and Loss Account.',
          [P('p1', 'Personal and real accounts are balanced and carried forward', 5, 'personal', 'real account balanc|real account carried forward|real account carry forward|real carried forward|real balanc|real account continu|real account are balanc'),
           P('p2', 'Nominal accounts are closed by transfer to Trading / Profit and Loss Account', 5, 'nominal account clos|nominal clos|nominal transfer|nominal account transfer|nominal not carried|nominal account not carried|nominal account are not carried|nominal account are clos')], 'c4'),
        V('v5', 'What does a debit balance in an account show? And a credit balance?',
          'A debit balance means the debit side total is more than the credit side; assets, expenses, losses and debtors show debit balances. A credit balance means the credit side total is more than the debit side; liabilities, capital, incomes, gains and creditors show credit balances.',
          [P('p1', 'Debit balance: debit side heavier than the credit side', 4, 'debit balanc debit side|debit balanc mean debit|debit balanc debit total|debit balanc debit exceed|debit balanc debit more|debit balanc debit heavier', 'more|heavier|greater|exceed|bigger|larger|excess'),
           P('p2', 'Credit balance: credit side heavier than the debit side', 4, 'credit balanc credit side|credit balanc mean credit|credit balanc credit total|credit balanc credit exceed|credit balanc credit more|credit balanc credit heavier', 'more|heavier|greater|exceed|bigger|larger|excess'),
           P('p3', 'Examples — debit: assets, expenses, losses, debtors; credit: liabilities, capital, incomes, gains, creditors', 3, 'asset|expense|debtor|loss', 'liabilit|capital|income|creditor|gain')], 'c3'),
    ],
    # ------------------------------------------------------------------ P1 Ch2 U3 Trial balance
    'fnd-p1-ch02-u03': [
        V('v1', 'What is a trial balance and what are its objectives?',
          'A trial balance is a statement listing the balances or totals of all ledger accounts on a particular date. Its objectives are to check the arithmetical accuracy of posting and balancing, to give a summary of the ledger, and to serve as the base for preparing the financial statements.',
          [P('p1', 'A statement of all ledger balances (or totals) on a particular date', 3, 'statement|list|schedule', 'ledger|account', 'balance|total', min=2),
           P('p2', 'Checks arithmetical accuracy of posting and balancing', 3, 'arithmetical accuracy|arithmetic|accuracy|check|verify'),
           P('p3', 'Summary of the ledger', 2, 'summary|summarise|summarize|overview|glance'),
           P('p4', 'Base for preparing final accounts / financial statements', 2, 'final account|financial statement|profit loss|balance sheet|base|basis', min=1)], 'c1'),
        V('v2', 'Name the methods of preparing a trial balance. Which one is used most?',
          'There are three methods: the total method, the balance method, and the total-cum-balance method. The balance method is the most commonly used, because final accounts are prepared from balances.',
          [P('p1', 'Total method', 2, 'total method|totals method|gross method|total'),
           P('p2', 'Balance method', 2, 'balance method|balances method|net method'),
           P('p3', 'Total-cum-balance (compound) method', 2, 'cum|total and balance|totals and balances|compound|both|combined|four column', min=1),
           P('p4', 'Balance method is used most / for final accounts', 4, 'balanc method most|balanc method common|balanc method popular|balanc method wide|balanc method general|balanc method usual|balanc method prefer|most balanc method|most common balanc|commonly use balanc')], 'c2'),
        V('v3', 'Does agreement of the trial balance prove that the accounts are correct? Give examples.',
          'No, agreement is not conclusive proof of accuracy. Several errors do not affect the agreement: an error of complete omission, an error of principle such as machinery debited to purchases, compensating errors that cancel each other, and an error of commission where the posting goes to the wrong account on the correct side.',
          [P('p1', 'No — agreement is not conclusive proof', 4, 'no|not conclusive|not proof|not a proof|not prove|not guarantee|not always|does not', min=1),
           P('p2', 'Names at least two errors not revealed (omission, principle, compensating, wrong account)', 6, 'omission|omitted|left out', 'principle|capital expenditure|revenue expenditure', 'compensating|cancel|offset', 'commission|wrong account|wrong person', min=2)], 'c4'),
        V('v4', 'What is a suspense account and when is it opened?',
          'A suspense account is a temporary account opened when the trial balance does not agree and accounts must still be prepared. The difference is put into it so the totals agree for the time being. When the errors are found and rectified, the suspense account closes automatically.',
          [P('p1', 'A temporary account', 3, 'temporary|temporarily|for the time being|interim|provisional'),
           P('p2', 'The trial balance difference is placed in it', 4, 'difference|disagree|does not agree|not agree|mismatch|tally', 'trial balance|tb|totals', min=1),
           P('p3', 'It closes when the errors are rectified', 3, 'close|closes|closed|eliminat|disappear|nil|zero', 'error|rectif|correct', min=2)], 'c5'),
        V('v5', 'On which side of the trial balance would you show sales returns, bank overdraft, drawings and outstanding expenses?',
          'Sales returns are debit. Bank overdraft is credit. Drawings are debit. Outstanding expenses are credit.',
          [P('p1', 'Sales returns — debit', 3, 'sales return debit|sale return debit|return inward debit|returns inward debit|debit sales return|debit side sales return'),
           P('p2', 'Bank overdraft — credit', 3, 'overdraft credit|overdraft outstand credit|overdraft outstand expens credit|credit bank overdraft|credit side bank overdraft|credit overdraft'),
           P('p3', 'Drawings — debit', 2, 'drawing debit|debit drawing|debit side drawing'),
           P('p4', 'Outstanding expenses — credit', 2, 'outstanding expense credit|outstanding credit|credit outstanding|credit side outstanding')], 'c3'),
    ],
    # ------------------------------------------------------------------ P1 Ch2 U4 Subsidiary books
    'fnd-p1-ch02-u04': [
        V('v1', 'Why does a business keep subsidiary books instead of only one journal?',
          'Subsidiary books group similar transactions together. This allows division of work among staff, saves time because only the periodic totals are posted to the nominal accounts, makes errors easier to locate, and gives quick information such as the total credit sales of the month.',
          [P('p1', 'Division of work among staff', 3, 'division of work|divide the work|divided among|several clerk|staff|different people|many people|distribute', min=1),
           P('p2', 'Saves time — only totals posted', 3, 'save time|saves time|time saving|faster|quick posting|total', min=1),
           P('p3', 'Errors easier to locate / better control', 2, 'error|mistake|fraud|control|check'),
           P('p4', 'Quick information (e.g. monthly credit sales)', 2, 'information|readily available|instant|at a glance|know|report', min=1)], 'c1'),
        V('v2', 'What is recorded in the purchases book, and what is not recorded there?',
          'The purchases book records only credit purchases of goods meant for resale, at the net amount after trade discount, from supplier invoices. Cash purchases are not recorded there; they go to the cash book. Credit purchases of assets such as furniture go to the journal proper.',
          [P('p1', 'Only credit purchases of goods', 4, 'credit purchas|purchas on credit|goods bought on credit|bought on credit', 'goods|resale|trade|deal'),
           P('p2', 'At net amount after trade discount (from invoices)', 2, 'net|after trade discount|less trade discount|invoice', min=1),
           P('p3', 'Cash purchases go to the cash book', 2, 'cash purchas|purchas for cash|cash', 'cash book'),
           P('p4', 'Credit purchase of assets goes to the journal proper', 2, 'asset|furniture|machinery|fixed asset', 'journal proper|journal')], 'c2'),
        V('v3', 'Distinguish between a debit note and a credit note.',
          'A debit note is sent by the buyer to the supplier when goods are returned, informing that the supplier\'s account has been debited; it is the basis of the purchase returns book. A credit note is issued by the seller to the customer for goods returned by the customer, informing that the customer\'s account has been credited; it is the basis of the sales returns book.',
          [P('p1', 'Debit note: sent by the buyer for goods returned to the supplier (supplier debited)', 4, 'debit note buyer|debit note purchaser|debit note purchas return|debit note return outward|buyer send debit note|buyer issu debit note|purchaser send debit note|purchaser issu debit note'),
           P('p2', 'Credit note: issued by the seller for goods returned by the customer (customer credited)', 4, 'credit note seller|credit note sale return|credit note return inward|seller issu credit note|seller send credit note'),
           P('p3', 'Recorded in purchase returns / sales returns books', 2, 'purchase return|returns outward', 'sales return|returns inward', min=1)], 'c4'),
        V('v4', 'How is the sales book posted to the ledger?',
          'Each customer\'s account is debited individually with the amount of the invoice. The total of the sales book for the period is credited to the Sales Account.',
          [P('p1', 'Each customer (debtor) account debited individually', 5, 'customer account debit|customer debit|debtor debit|debtor account debit|party debit|buyer debit|debit customer|debit each customer|debit debtor'),
           P('p2', 'Periodic total credited to Sales Account', 5, 'total', 'credit sale account|sale account credit|total credit|sale credit|credit total')], 'c3'),
        V('v5', 'Which transactions are recorded in the journal proper? Give examples.',
          'The journal proper records transactions that do not fit into any other subsidiary book. Examples are the opening entry, closing entries, adjustment entries, rectification entries, transfer entries, credit purchase or sale of assets, goods withdrawn by the owner and loss of goods by fire.',
          [P('p1', 'Transactions that do not fit any other book', 3, 'not fit|no other book|not recorded in any|none of the|any other|other subsidiary|other book', min=1),
           P('p2', 'At least three examples (opening, closing, adjustment, rectification, transfer, credit asset deal, drawings of goods, loss by fire…)', 7,
             'opening entry|opening', 'closing entry|closing', 'adjustment|outstanding|prepaid|depreciation', 'rectification|rectify|correct', 'transfer', 'asset|furniture|machinery', 'withdrawn|drawing|personal use', 'fire|theft|loss of goods|bad debt', min=3)], 'c5'),
    ],
    # ------------------------------------------------------------------ P1 Ch2 U5 Cash book
    'fnd-p1-ch02-u05': [
        V('v1', 'Why is the cash book both a book of original entry and a principal book?',
          'All cash and bank transactions are first recorded in the cash book, so it is a book of original entry. It also takes the place of the Cash Account and Bank Account in the ledger, and its balances go straight to the trial balance, so it is a principal book as well.',
          [P('p1', 'Transactions are first recorded in it (original entry)', 5, 'first recorded|recorded first|first entered|first record|first|initially', min=1),
           P('p2', 'It replaces the Cash and Bank accounts in the ledger (principal book)', 5, 'cash account|bank account|ledger|principal', 'replace|instead|serve|no separate|acts as|works as|place', min=2)], 'c1'),
        V('v2', 'What is a contra entry?',
          'A contra entry is a transaction that affects both the cash column and the bank column of the cash book, such as cash deposited into the bank or cash withdrawn from the bank for office use. It is recorded on both sides of the cash book, marked with the letter C in the ledger folio column, and it is not posted to the ledger.',
          [P('p1', 'Affects both cash and bank', 3, 'cash', 'bank', 'both|deposit|withdraw', min=3),
           P('p2', 'Recorded on both sides of the cash book', 2, 'both side|two side|debit and credit side|either side', min=1),
           P('p3', 'Marked "C" in the folio column', 1, 'c|letter c|contra mark|folio'),
           P('p4', 'Not posted to the ledger', 4, 'not posted|no posting|no ledger posting|not post|nothing is posted', min=1)], 'c4'),
        V('v3', 'In a three-column cash book, why are the discount columns totalled and not balanced?',
          'Discount is not cash; no money actually moves, so there is nothing to balance. The discount allowed column on the debit side is totalled and debited to Discount Allowed Account, and the discount received column on the credit side is totalled and credited to Discount Received Account.',
          [P('p1', 'Discount is not cash — no money moves', 4, 'not cash|no cash|no money|nominal|not actual|not a cash|memorandum', min=1),
           P('p2', 'Debit-side total goes to Discount Allowed Account', 3, 'debit side discount allow|discount allow column debit side|debit side total discount allow|debit side column discount allow|debit side column total discount allow'),
           P('p3', 'Credit-side total goes to Discount Received Account', 3, 'credit side discount receiv|discount receiv column credit side|credit side total discount receiv|credit side column discount receiv|credit side column total discount receiv')], 'c3'),
        V('v4', 'Explain the imprest system of petty cash.',
          'Under the imprest system the petty cashier is given a fixed amount, called the imprest, at the start of the period. At the end of the period the petty cashier shows the vouchers for the money spent, and the main cashier reimburses exactly that amount, so the petty cashier again starts with the full imprest.',
          [P('p1', 'A fixed amount (imprest) is given to the petty cashier', 4, 'fixed amount|fixed sum|definite amount|fixed|imprest', 'petty cashier|petty cash', min=1),
           P('p2', 'At the end of the period the amount spent is reimbursed', 4, 'reimburse|repay|replenish|refund|make good|restore|top up', 'spent|expens|used|paid', min=1),
           P('p3', 'Petty cashier starts again with the full imprest (vouchers support spending)', 2, 'full|same amount|original|again|voucher', min=1)], 'c5'),
        V('v5', 'A shop sells goods for ten thousand rupees through a credit card and the bank charges two per cent commission. How does the seller record this?',
          'Bank Account is debited and Sales Account is credited with the full 10,000 rupees. Then the bank commission of 200 rupees, which is two per cent, is recorded separately: Commission Account is debited and Bank Account is credited. The commission is a selling expense.',
          [P('p1', 'Bank debited and Sales credited with the full ₹10,000', 4, 'bank debit sale|bank account debit sale|debit bank credit sale|debit bank 10000 credit sale|credit sale debit bank|sale credit bank debit', '10000|full'),
           P('p2', 'Commission ₹200 debited, Bank credited', 4, 'commission debit|debit commission|commission account debit|bank charg debit|debit bank charg', '200'),
           P('p3', 'Commission is an expense (selling expense)', 2, 'expense|loss|cost', min=1)], 'c6'),
    ],
    # ------------------------------------------------------------------ P1 Ch2 U6 Rectification
    'fnd-p1-ch02-u06': [
        V('v1', 'Name the four kinds of errors in accounting.',
          'The four kinds are errors of omission, errors of commission, errors of principle and compensating errors. For example, a sale left out completely is an omission, posting to Sumit instead of Amit is commission, machinery debited to purchases is principle, and two errors of the same amount on opposite sides are compensating.',
          [P('p1', 'Errors of omission', 3, 'omission|omit'),
           P('p2', 'Errors of commission', 3, 'commission'),
           P('p3', 'Errors of principle', 2, 'principle'),
           P('p4', 'Compensating errors', 2, 'compensat|offsetting|cancel')], 'c2'),
        V('v2', 'Distinguish between one-sided and two-sided errors.',
          'A one-sided error affects only one account, so it disturbs the agreement of the trial balance. A two-sided error affects two accounts equally, so the trial balance still agrees, and it is corrected by a journal entry between the two accounts.',
          [P('p1', 'One-sided error affects only one account', 3, 'one sided|single sided|one side', 'one account|single account|only one'),
           P('p2', 'One-sided error disturbs the trial balance', 2, 'disturb|affect|not agree|disagree|difference', 'trial balance|tb', min=2),
           P('p3', 'Two-sided error affects two accounts; trial balance still agrees', 3, 'two sided|both sided|two side', 'two account|both account|still agree|agree|not affect|no effect', min=2),
           P('p4', 'Two-sided error corrected by a journal entry', 2, 'journal entry|journal|rectifying entry')], 'c3'),
        V('v3', 'How is a one-sided error rectified before the trial balance is prepared?',
          'No journal entry is passed. A correcting posting is made only in the affected account, on the required side, with an explanatory narration such as by under-casting of the sales book.',
          [P('p1', 'No journal entry is passed', 4, 'no journal|without journal|not journalised|no entry|journal entry is not', min=1),
           P('p2', 'Correcting posting made in the affected account only', 4, 'affected account|that account|one account|account concerned|concerned account|the account', 'post|posting|record|entry|correct', min=2),
           P('p3', 'Explanatory narration (e.g. "By under-casting of…")', 2, 'narration|explanation|explanatory|under casting|undercasting|over casting|overcasting', min=1)], 'c4'),
        V('v4', 'What is the role of the suspense account when errors are found after the trial balance?',
          'The difference in the trial balance is first placed in the suspense account. When errors are found, one-sided errors are rectified through the suspense account, which takes the other side of the entry, while two-sided errors are rectified between the two accounts. Once all errors are rectified the suspense account closes.',
          [P('p1', 'The trial balance difference is placed in suspense', 3, 'difference', 'suspense'),
           P('p2', 'One-sided errors are rectified through the suspense account', 4, 'one sided|single sided|one side', 'suspense'),
           P('p3', 'Suspense closes once all errors are rectified', 3, 'close|closes|closed|nil|zero|eliminat|disappear')], 'c5'),
        V('v5', 'Wages of nine thousand rupees paid for installing a new machine were debited to Wages Account. Name the error and state the effect of rectifying it on profit, ignoring depreciation.',
          'It is an error of principle, because capital expenditure was treated as revenue expenditure. The rectifying entry debits Machinery Account and credits Wages Account with 9,000 rupees. Profit increases by 9,000 rupees, because an expense is reduced.',
          [P('p1', 'Error of principle (capital expenditure treated as revenue)', 3, 'principle'),
           P('p2', 'Machinery debited, Wages credited', 4, 'machin debit wage|debit machin credit wage|machin account debit wage|credit wage debit machin|wage credit machin debit'),
           P('p3', 'Profit increases by ₹9,000', 3, 'profit', 'increase|increases|rise|goes up|higher|more', '9000', min=3)], 'c6'),
    ],
    # ------------------------------------------------------------------ P2 Ch2 U1 Nature of contracts
    'fnd-p2-ch02-u01': [
        V('v1', 'Distinguish between an agreement and a contract.',
          'An agreement is a promise or set of promises forming consideration for each other under Section 2(e); in short, offer plus acceptance. A contract is an agreement enforceable by law under Section 2(h). So every contract is an agreement but every agreement is not a contract; social and domestic agreements like the one in Balfour versus Balfour are not enforceable.',
          [P('p1', 'Agreement = offer + acceptance / promises (Section 2(e))', 3, 'agreement', 'offer|acceptance|promise|2 e', min=2),
           P('p2', 'Contract = agreement enforceable by law (Section 2(h))', 4, 'contract', 'enforceable|enforced|enforce|binding|2 h', min=2),
           P('p3', 'All contracts are agreements, not vice versa — e.g. social/domestic (Balfour)', 3, 'every contract agreement|all contract agreement|every contract is agreement|not every agreement|not all agreement|every agreement not|all agreement not|social|domestic|balfour', min=1)], 'c1'),
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
             ALT('{p} complet when put', '{p} complet when post', '{p} complet when sent', '{p} complet post', '{p} post', '{p} sent', '{p} when put', '{p} put course', '{p} course transmiss', '{p} transmiss', 'post against {p}', 'sent against {p}', p=PROP)),
           P('p2', 'Against the acceptor: only when it comes to the knowledge of the proposer', 5,
             ALT('{a} {p} know', '{a} {p} learn', '{a} {p} receiv', '{a} come knowledg {p}', '{a} complet when come knowledg', '{a} complet when {p} know', '{a} complet when {p} learn', '{a} knowledg {p}', a=('acceptor', 'offeree'), p=PROP))], 'c7'),
    ],
}
