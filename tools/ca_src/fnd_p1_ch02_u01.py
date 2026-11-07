"""CA Foundation · Paper 1 Accounting · Chapter 2 Accounting Process · Unit 1 Journal entries.
Original explanations and numbers (structure and scope follow the ICAI study material)."""
from lib import *
from shared import kavya_entries

UID = 'fnd-p1-ch02-u01'


def build():
    # ---------------- Illustration 1: Kavya Traders, April 2026 ----------------
    c1 = Checks()
    net_purchase = c1.add('80000*90/100', 'Mehta & Co. invoice after 10% trade discount')
    disc_rec = c1.add('72000*2/100', 'Cash discount received @2% on 72,000')
    paid_mehta = c1.add('72000-1440', 'Cheque paid to Mehta & Co.')
    disc_all = c1.add('45000*2/100', 'Cash discount allowed @2% on 45,000')
    cash_rohan = c1.add('45000-900', 'Cash received from Rohan')
    c1.add('18000+12000', 'Total cheque for salary and rent')
    E1 = kavya_entries()
    classify = table(['Account', 'Traditional type', 'Rule applied', 'Modern (equation) view'], [
        ['Cash', 'Real (tangible)', 'Debit what comes in, credit what goes out', 'Asset'],
        ['Bank', 'Personal (artificial — the bank)', 'Debit the receiver, credit the giver', 'Asset'],
        ['Capital', 'Personal (the proprietor)', 'Credit the giver', 'Capital'],
        ['Mehta & Co. / Rohan', 'Personal (artificial / natural)', 'Debit the receiver, credit the giver', 'Liability / Asset'],
        ['Purchases / Sales', 'Nominal (goods account)', 'Expense debited, income credited', 'Expense / Revenue'],
        ['Discount Received / Allowed', 'Nominal', 'Credit gains, debit losses', 'Revenue / Expense'],
        ['Drawings', 'Personal (the proprietor)', 'Debit the receiver', 'Reduces capital'],
    ], title='Why each account is debited or credited',
        note='ICAI treats the Bank Account as a personal account (the bank is an artificial person), so for deposits and payments by cheque apply "debit the receiver, credit the giver". Cash is a real account.')

    # ---------------- Illustration 2: GST ----------------
    c2 = Checks()
    pc = c2.add('200000*9/100', 'Input CGST @9% on purchases of 2,00,000')
    pt = c2.add('200000+18000+18000', 'Amount payable to Shree Ganesh Traders')
    sc = c2.add('300000*9/100', 'Output CGST @9% on sales of 3,00,000')
    st = c2.add('300000+27000+27000', 'Amount receivable from Neha Stores')
    ac = c2.add('20000*9/100', 'Input CGST @9% on advertisement of 20,000')
    at = c2.add('20000+1800+1800', 'Cheque for advertisement')
    inc = c2.add('18000+1800', 'Total input CGST (same for SGST)')
    net = c2.add('27000-19800', 'CGST payable in cash after set-off (same for SGST)')
    c2.add('7200*2', 'Total GST paid by cheque')
    E2 = [
        je('May 3', [('Purchases A/c', 200000), ('Input CGST A/c', pc), ('Input SGST A/c', pc)], [('Shree Ganesh Traders', pt)], 'Being goods bought on credit within the State; CGST and SGST @9% each charged'),
        je('May 12', [('Neha Stores', st)], [('Sales A/c', 300000), ('Output CGST A/c', sc), ('Output SGST A/c', sc)], 'Being goods sold on credit within the State; CGST and SGST @9% each charged'),
        je('May 20', [('Advertisement A/c', 20000), ('Input CGST A/c', ac), ('Input SGST A/c', ac)], [('Bank A/c', at)], 'Being newspaper advertisement paid by cheque, GST charged by the agency'),
        je('May 31', [('Output CGST A/c', inc)], [('Input CGST A/c', inc)], 'Being input CGST set off against output CGST'),
        je('May 31', [('Output SGST A/c', inc)], [('Input SGST A/c', inc)], 'Being input SGST set off against output SGST'),
        je('May 31', [('Output CGST A/c', net), ('Output SGST A/c', net)], [('Bank A/c', net * 2)], 'Being balance GST liability for May paid'),
    ]

    # ---------------- Illustration 3: accounting equation ----------------
    c3 = Checks()
    c3.add('300000+40000+5000-5000+0', 'Total assets after five transactions')
    c3.add('0+40000', 'Liabilities after five transactions')
    c3.add('300000+(25000-20000)-5000', 'Capital = opening capital + profit on sale - rent expense')
    eq_rows = [
        ['Started with cash ₹3,00,000', '+3,00,000', '0', '+3,00,000'],
        ['Goods bought on credit ₹40,000', '+40,000', '+40,000', '0'],
        ['Goods costing ₹20,000 sold for ₹25,000 cash', '+5,000', '0', '+5,000'],
        ['Rent paid ₹5,000 in cash', '-5,000', '0', '-5,000'],
        ['Furniture bought for cash ₹15,000', '0', '0', '0'],
        ['Closing position', '3,40,000', '40,000', '3,00,000'],
    ]
    eq = table(['Transaction', 'Assets (₹)', 'Liabilities (₹)', 'Capital (₹)'], eq_rows, num=[1, 2, 3], total=True,
               note='Furniture for cash only swaps one asset for another (cash down, furniture up), so the totals do not move. Sale: stock ₹20,000 goes out, cash ₹25,000 comes in — net assets +₹5,000, and the ₹5,000 profit raises capital.')
    c3.add('340000-40000', 'Assets less liabilities equals capital')

    # ---------------- Question 1 model ----------------
    q1c = Checks()
    q1_disc = q1c.add('60000*5/100', 'Trade discount on list price 60,000 @5%')
    q1_net = q1c.add('60000-3000', 'Invoice value after trade discount')
    Q1 = [
        je('Jun 1', [('Bank A/c', 500000), ('Machinery A/c', 150000)], [('Capital A/c', 650000)], 'Being business started with bank balance and machinery'),
        je('Jun 5', [('Purchases A/c', q1_net)], [('Lakshmi Agencies', q1_net)], 'Being goods bought on credit, list price ₹60,000 less 5% trade discount'),
        je('Jun 9', [('Furniture A/c', 24000)], [('Comfort Furnishers', 24000)], 'Being furniture bought on credit for office use'),
        je('Jun 14', [('Loss by Fire A/c', 9000), ('Insurance Claim A/c', 21000)], [('Purchases A/c', 30000)], 'Being goods costing ₹30,000 destroyed by fire; insurer admitted a claim of ₹21,000'),
        je('Jun 20', [('Drawings A/c', 7500)], [('Bank A/c', 7500)], "Being proprietor's household electricity bill paid from the business bank account"),
        je('Jun 30', [('Salaries A/c', 16000)], [('Outstanding Salary A/c', 16000)], 'Being salary for June due but not yet paid'),
    ]
    q1c.add('30000-21000', 'Loss by fire not covered by insurance')

    q3c = Checks()
    q3_ic = q3c.add('150000*6/100', 'Input CGST @6% on 1,50,000')
    q3_pay = q3c.add('150000+9000+9000', 'Amount payable to supplier')
    q3_oc = q3c.add('240000*6/100', 'Output CGST @6% on 2,40,000')
    q3_rec = q3c.add('240000+14400+14400', 'Amount receivable from customer')
    q3_net = q3c.add('14400-9000', 'Net CGST payable (same for SGST)')
    Q3 = [
        je('Jul 4', [('Purchases A/c', 150000), ('Input CGST A/c', q3_ic), ('Input SGST A/c', q3_ic)], [('Om Textiles', q3_pay)], 'Being goods bought on credit within the State, CGST and SGST @6% each'),
        je('Jul 18', [('Rhea Fashions', q3_rec)], [('Sales A/c', 240000), ('Output CGST A/c', q3_oc), ('Output SGST A/c', q3_oc)], 'Being goods sold on credit within the State, CGST and SGST @6% each'),
        je('Jul 31', [('Output CGST A/c', q3_ic), ('Output SGST A/c', q3_ic)], [('Input CGST A/c', q3_ic), ('Input SGST A/c', q3_ic)], 'Being input tax set off against output tax'),
        je('Jul 31', [('Output CGST A/c', q3_net), ('Output SGST A/c', q3_net)], [('Bank A/c', q3_net * 2)], 'Being net GST for July paid'),
    ]
    q3c.add('5400*2', 'Total GST paid in cash')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch02', 'n': 1,
        'title': 'Basic Accounting Procedures – Journal entries',
        'outcomes': [
            'Explain the two-sided (double entry) effect of every transaction and why it lets you check the books.',
            'Classify accounts as personal (natural, artificial, representative), real or nominal — and under the accounting-equation (modern) approach.',
            'Decide the debit and the credit for any transaction using the golden rules or the accounting equation, and get the same answer both ways.',
            'Write journal entries in the exam format — date, particulars, L.F., amounts and a narration — including compound and special entries.',
            'Record GST on purchases, sales and expenses using input and output tax accounts, set-off and payment.',
        ],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 50}, 'prereq': ['fnd-p1-ch01-u02'],
                 'exam_tip': 'Journal entries appear in almost every Paper 1 question — a wrong debit/credit here costs marks later in ledgers, trial balance and final accounts.'},
        'concepts': [
            {'id': 'c1', 'title': 'Double entry: every rupee has a source and a use',
             'body': ['Every transaction changes at least two accounts, and the total debited always equals the total credited. Buy furniture for cash: furniture goes up, cash goes down — both are recorded.',
                      'Because both sides are always written, the books can be tested (the trial balance), profit can be worked out in detail, and the financial position can be shown at any date.'],
             'analogy': 'A see-saw: whatever weight you put on one side must be matched on the other, or it tips. An entry with unequal sides is a see-saw lying on the ground — something is missing.',
             'work': 'Accounting software refuses to save a voucher whose debits and credits differ. When an auditor finds a difference in the books, the first question is: which entry was only half recorded?'},
            {'id': 'c2', 'title': 'An account, a debit and a credit',
             'body': ['An account is a summary of all increases and decreases in one item — Cash, Rent, Rohan. It is shown in a T shape: left side = debit (Dr), right side = credit (Cr).',
                      'Debit and credit are only positions — left and right. "Credit" is not good news and "debit" is not bad news. Whether an amount goes left or right depends on the type of account.'],
             'analogy': 'Think of the two columns of a cricket scorecard — runs scored and runs given. Neither column is "good"; you need both to know the result.',
             'work': 'A client says "the bank credited my account". From the bank\'s books, your deposit is money it owes you (a liability), so the bank credits you. In your own books, the same deposit is a debit to Bank A/c. Explaining this perspective is daily work for a CA.'},
            {'id': 'c3', 'title': 'The accounting equation (modern approach)',
             'body': ['Assets = Liabilities + Capital. Every transaction keeps this equation true.',
                      'Rules: an increase in an asset, an expense or drawings is debited; an increase in a liability, capital or income is credited. Decreases go the opposite way.'],
             'blocks': [eq],
             'analogy': 'Your business is a bag. What is inside the bag (assets) must always equal what the bag owes to outsiders (liabilities) plus what it owes to the owner (capital).',
             'work': 'Analysts read a balance sheet using exactly this equation. A sudden jump in assets with no rise in liabilities or capital is a red flag that an entry is wrong.'},
            {'id': 'c4', 'title': 'Traditional classification and the three golden rules',
             'body': ['Personal accounts — people and bodies: natural persons (Rohan), artificial or legal persons (a company, a bank, a club) and representative personal accounts that stand for a person (Outstanding Salary, Prepaid Rent, Capital, Drawings). Rule: debit the receiver, credit the giver.',
                      'Real accounts — things owned: tangible (cash, machinery, stock) and intangible (goodwill, patents, trademarks). Rule: debit what comes in, credit what goes out.',
                      'Nominal accounts — expenses, losses, incomes, gains (rent, salary, commission received, discount allowed). Rule: debit all expenses and losses, credit all incomes and gains.'],
             'analogy': 'Personal = who? Real = what? Nominal = why? Ask the three questions and the account type usually becomes obvious.',
             'work': 'When you create ledgers in accounting software you choose a group (Sundry Debtors, Fixed Assets, Indirect Expenses). Picking the wrong group misplaces the item in the financial statements — the same thinking as classifying accounts.'},
            {'id': 'c5', 'title': 'The journal: book of original entry',
             'body': ['Each entry shows: date; the account debited (with "Dr.") and, on the next line, the account credited (starting with "To"); ledger folio (L.F.); debit and credit amounts; and a short narration in brackets beginning "Being …".',
                      'A compound entry has more than one debit or credit (for example, a payment with discount). An opening entry brings last year\'s balances into the new books.',
                      'Special cases: trade discount is never recorded (record the net price); cash discount is recorded (Discount Allowed/Received). Goods taken for personal use: Drawings Dr, To Purchases. Free samples: Advertisement Dr, To Purchases. Goods lost by fire: Loss by Fire Dr (and Insurance Claim Dr for the admitted claim), To Purchases.'],
             'analogy': 'The journal is a diary in date order; the ledger is the same information sorted into folders, one folder per account.',
             'work': 'Every journal entry must be supported by a document — invoice, receipt, debit note, bank statement. "Vouching" (checking entries against documents) is one of the first audit tasks an articled assistant does.'},
            {'id': 'c6', 'title': 'Accounting for GST',
             'body': ['GST paid on purchases and expenses is debited to Input CGST/SGST (supply within the same State) or Input IGST (supply between States). It is not part of the cost when the credit is available — it is an amount recoverable from the government.',
                      'GST collected on sales is credited to Output CGST/SGST or Output IGST — a liability payable to the government.',
                      'At the end of the period, input tax is set off against output tax (Output … A/c Dr, To Input … A/c) and only the balance is paid. Credit of CGST cannot be used to pay SGST and vice versa.'],
             'analogy': 'GST is like a parcel you carry for the government: you collect it from customers, subtract what you already paid to suppliers, and hand over only the difference.',
             'work': 'Every month accountants match input tax in the books with what suppliers have reported, pass the set-off entry and pay the net tax. Errors here lead to interest and notices — a common reason clients call their CA.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Ten everyday transactions', 'difficulty': 'core', 'minutes': 18,
             'q': 'Kavya started Kavya Traders on 1 April 2026. Journalise: (1) Apr 1 — started business with cash ₹4,00,000. (2) Apr 2 — opened a bank account with ₹2,50,000. (3) Apr 4 — bought goods from Mehta & Co. on credit, list price ₹80,000, trade discount 10%. (4) Apr 7 — sold goods to Rohan on credit ₹45,000. (5) Apr 10 — bought a computer for office use by cheque ₹38,000. (6) Apr 15 — paid Mehta & Co. by cheque, getting 2% cash discount. (7) Apr 18 — Rohan paid in cash, 2% discount allowed. (8) Apr 22 — Kavya took goods costing ₹3,500 for home use. (9) Apr 25 — goods costing ₹2,000 given away as free samples. (10) Apr 30 — paid salary ₹18,000 and rent ₹12,000 by cheque.',
             'solution': [journal(E1, 'Journal of Kavya Traders (April 2026)', 'j1'), classify,
                          wn('Working notes', f'Trade discount is not recorded: purchase = 80,000 × 90% = ₹{inr(net_purchase)}. Cash discount on 15 April = 2% × {inr(net_purchase)} = ₹{inr(disc_rec)}, so the cheque is ₹{inr(paid_mehta)}. On 18 April Rohan pays 45,000 − 2% = ₹{inr(cash_rohan)}.')],
             'checks': c1},
            {'id': 'i2', 'title': 'GST on purchases, sales and an expense', 'difficulty': 'moderate', 'minutes': 14,
             'q': 'Arjun Electricals (registered under GST) records the following for May 2026. All supplies are within the same State; CGST and SGST are 9% each. (1) May 3 — bought goods on credit from Shree Ganesh Traders ₹2,00,000 plus GST. (2) May 12 — sold goods on credit to Neha Stores ₹3,00,000 plus GST. (3) May 20 — paid for a newspaper advertisement ₹20,000 plus GST by cheque. Pass journal entries, including the set-off on 31 May and payment of the balance by cheque.',
             'solution': [journal(E2, 'Journal of Arjun Electricals (May 2026)', 'j2'),
                          wn('Set-off', f'Input CGST = {inr(pc)} + {inr(ac)} = ₹{inr(inc)}. Output CGST = ₹{inr(sc)}. CGST payable = {inr(sc)} − {inr(inc)} = ₹{inr(net)}. SGST works out the same, so ₹{inr(net * 2)} is paid in all.'),
                          note('GST rates here are assumed for practice. In real work the rate depends on the goods or services supplied.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Watching the accounting equation stay balanced', 'difficulty': 'core', 'minutes': 8,
             'q': 'Show the effect of these transactions on assets, liabilities and capital: started with cash ₹3,00,000; bought goods on credit ₹40,000; sold goods costing ₹20,000 for ₹25,000 cash; paid rent ₹5,000; bought furniture for cash ₹15,000.',
             'solution': [eq, p('Closing check: Assets ₹3,40,000 = Liabilities ₹40,000 + Capital ₹3,00,000. The sale earned a profit of ₹5,000 (raising capital) and the rent of ₹5,000 is an expense (reducing capital), so capital ends where it started: 3,00,000 + 5,000 − 5,000 = ₹3,00,000.')],
             'checks': c3},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Vouching purchase entries in your first audit', 'role': 'Articled assistant at a CA firm (statutory audit of a wholesaler)',
             'situation': 'Your senior asks you to vouch 25 purchase entries for March. Three things turn up: one entry records the list price and shows the trade discount as "Discount Received"; one supplier invoice has no matching entry; and the proprietor\'s personal phone bill is booked as Telephone Expenses.',
             'steps': ['Pick the sample from the purchase register and pull each supplier invoice.',
                       'Match date, supplier, net amount and GST with the entry. Trade discount should simply reduce the amount — it is not income.',
                       'Search later entries and the supplier\'s statement for the missing invoice; if it is truly missing, it is an unrecorded liability.',
                       'The personal phone bill should be Drawings, not an expense — it overstates expenses and understates the proprietor\'s withdrawals.',
                       'Write each finding in the working paper with the document reference and the correct entry, and discuss with your senior.'],
             'takeaway': 'Journal rules are not just exam rules — auditors test every entry against them. A misclassification changes profit, capital or liabilities.',
             'think': 'Why does recording trade discount as income overstate both purchases and income, even though profit stays the same?',
             'answer': 'Purchases are recorded at the list price (too high) and an equal amount appears as discount income, so both totals are inflated by the same figure and the net effect on profit is nil — but the accounts are misleading.'},
            {'id': 'j2', 'title': 'Month-end GST entries for a small business', 'role': 'Accounts executive in a trading company',
             'situation': 'It is the 5th of the month. Your manager wants the GST payable for last month and the entries posted before the return is filed.',
             'steps': ['Total the Output CGST, SGST and IGST ledgers from the sales side.',
                       'Total the Input tax ledgers and reconcile them with what suppliers have reported, so that credit is taken only where it is available.',
                       'Pass the set-off entries: Output … A/c Dr, To Input … A/c — never using CGST credit against SGST or the other way round.',
                       'Pass the payment entry for the balance and keep the challan as the supporting document.'],
             'takeaway': 'Input tax is an asset until it is set off; output tax is a liability until it is paid. Your ledgers should tell you the GST position on any day.',
             'think': 'Output CGST ₹48,000, Input CGST ₹52,000. What is the CGST payable in cash this month?',
             'answer': 'Nil. Input credit exceeds output tax, so the extra ₹4,000 remains as Input CGST (an asset) to be used later.'},
        ],
        'mcqs': [
            {'id': 'm1', 'q': 'Goods costing ₹6,000 were taken by the proprietor for personal use. The correct entry is:', 'options': ['Drawings A/c Dr. To Purchases A/c', 'Purchases A/c Dr. To Drawings A/c', 'Drawings A/c Dr. To Sales A/c', 'Capital A/c Dr. To Cash A/c'], 'answer': 0, 'explain': 'The proprietor is the receiver (Drawings is debited) and goods have gone out of the business at cost, so Purchases is credited.', 'concept': 'c5', 'difficulty': 'core'},
            {'id': 'm2', 'q': 'Goods with a list price of ₹50,000 are bought at 10% trade discount and 2% cash discount for immediate payment. The cash paid is:', 'options': ['₹44,100', '₹45,000', '₹44,000', '₹49,000'], 'answer': 0, 'check': '50000*0.9*0.98', 'explain': 'Trade discount first: 50,000 × 90% = 45,000. Cash discount 2% on 45,000 = 900. Cash paid = 44,100.', 'concept': 'c5', 'difficulty': 'core'},
            {'id': 'm3', 'q': 'Prepaid Insurance Account is:', 'options': ['A representative personal account', 'A nominal account', 'An intangible real account', 'A natural personal account'], 'answer': 0, 'explain': 'It represents the insurer who owes the business future cover, so it is a representative personal account.', 'concept': 'c4', 'difficulty': 'moderate'},
            {'id': 'm4', 'q': 'Under the accounting-equation approach, an increase in a liability is:', 'options': ['Credited', 'Debited', 'Not recorded', 'Recorded in capital'], 'answer': 0, 'explain': 'Liabilities, capital and incomes increase on the credit side.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm5', 'q': 'Goodwill Account is classified as:', 'options': ['An intangible real account', 'A nominal account', 'An artificial personal account', 'A tangible real account'], 'answer': 0, 'explain': 'Goodwill is something the business owns but cannot touch — an intangible real account.', 'concept': 'c4', 'difficulty': 'core'},
            {'id': 'm6', 'q': 'Output CGST ₹12,500, Output SGST ₹12,500, Input CGST ₹9,000, Input SGST ₹9,000. Total GST to be paid in cash is:', 'options': ['₹7,000', '₹3,500', '₹25,000', '₹43,000'], 'answer': 0, 'check': '(12500-9000)*2', 'explain': 'CGST payable 12,500 − 9,000 = 3,500 and SGST payable 3,500 — total ₹7,000.', 'concept': 'c6', 'difficulty': 'core'},
            {'id': 'm7', 'q': 'Which of these is a nominal account?', 'options': ['Discount Received', 'Bank Overdraft', 'Machinery', 'Outstanding Rent'], 'answer': 0, 'explain': 'Discount received is a gain — nominal. Bank overdraft and outstanding rent are personal; machinery is real.', 'concept': 'c4', 'difficulty': 'core'},
            {'id': 'm8', 'q': 'An entry that debits two accounts and credits one is called:', 'options': ['A compound entry', 'An opening entry', 'A contra entry', 'A rectifying entry'], 'answer': 0, 'explain': 'Any entry with more than one debit or more than one credit is a compound entry.', 'concept': 'c5', 'difficulty': 'core'},
            {'id': 'm9', 'q': 'Capital is ₹3,00,000 and liabilities are ₹1,20,000. Total assets must be:', 'options': ['₹4,20,000', '₹1,80,000', '₹3,00,000', '₹1,20,000'], 'answer': 0, 'check': '300000+120000', 'explain': 'Assets = Liabilities + Capital = 1,20,000 + 3,00,000 = ₹4,20,000.', 'concept': 'c3', 'difficulty': 'core'},
            {'id': 'm10', 'q': 'Goods costing ₹4,000 distributed as free samples are recorded as:', 'options': ['Advertisement A/c Dr. To Purchases A/c', 'Purchases A/c Dr. To Advertisement A/c', 'Drawings A/c Dr. To Purchases A/c', 'No entry is required'], 'answer': 0, 'explain': 'Free samples are a promotion expense; the goods leave the business at cost, so Purchases is credited.', 'concept': 'c5', 'difficulty': 'core'},
        ],
        'questions': [
            {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'core', 'pad': 'journal',
             'q': 'Pass journal entries in the books of Ishaan Enterprises for June 2026: (1) Jun 1 — Ishaan started business with ₹5,00,000 in a bank account and machinery worth ₹1,50,000. (2) Jun 5 — bought goods from Lakshmi Agencies, list price ₹60,000, trade discount 5%, on credit. (3) Jun 9 — bought office furniture on credit from Comfort Furnishers ₹24,000. (4) Jun 14 — goods costing ₹30,000 destroyed by fire; the insurance company admitted a claim of ₹21,000. (5) Jun 20 — paid the proprietor\'s household electricity bill ₹7,500 from the business bank account. (6) Jun 30 — salary of ₹16,000 for June is due but not paid.',
             'model': [journal(Q1, 'Journal of Ishaan Enterprises (June 2026)', 'jq1'),
                       wn('Working notes', f'(2) 60,000 − 5% = ₹{inr(q1_net)}; trade discount ₹{inr(q1_disc)} is not recorded. (4) Loss not covered = 30,000 − 21,000 = ₹9,000.')],
             'scheme': [
                 {'id': 's1', 'pt': 'Opening entry: Bank and Machinery debited, Capital credited ₹6,50,000', 'm': 1, 'skill': 'classification'},
                 {'id': 's2', 'pt': 'Purchases recorded at ₹57,000 (trade discount not shown)', 'm': 1, 'skill': 'computation'},
                 {'id': 's3', 'pt': 'Furniture debited, supplier (not Purchases) credited', 'm': 1, 'skill': 'classification'},
                 {'id': 's4', 'pt': 'Loss by Fire ₹9,000 and Insurance Claim ₹21,000 debited, Purchases credited ₹30,000', 'm': 1, 'skill': 'computation'},
                 {'id': 's5', 'pt': 'Household bill treated as Drawings', 'm': 1, 'skill': 'classification'},
                 {'id': 's6', 'pt': 'Outstanding Salary credited; narrations given for entries', 'm': 1, 'skill': 'presentation'},
             ],
             'remarks': ['Most candidates handle the opening entry well; marks are lost on fire loss, where many debit only the insurance claim or only the loss.',
                         'Several answers credit Purchases for the furniture — furniture is an asset bought on credit, so the supplier is credited.',
                         'Answers without narrations look incomplete; examiners expect a brief "Being …" line for each entry.'],
             'mistakes': ['Recording the list price ₹60,000 and the trade discount as income.', 'Debiting Electricity Expenses for a household bill.', 'Forgetting "Dr." and "To" — the format itself carries presentation marks.'],
             'tips': ['Rule a proper journal: Date | Particulars | L.F. | Dr (₹) | Cr (₹).', 'Write the debit line first, the credit line indented with "To".', 'Show working notes for any computed amount.']},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': 'Distinguish between trade discount and cash discount. How is each treated in the books of account?',
             'model': [table(['Basis', 'Trade discount', 'Cash discount'], [
                 ['Purpose', 'Allowed on the list price to promote bulk or trade purchases', 'Allowed to encourage prompt payment'],
                 ['When given', 'At the time of purchase or sale, shown on the invoice', 'At the time of payment, if paid within the agreed period'],
                 ['Recording', 'Not recorded — the entry is made at the net price', 'Recorded: Discount Allowed (loss) by the seller, Discount Received (gain) by the buyer'],
                 ['Effect on accounts', 'No separate account; no effect on profit and loss account', 'Appears in the profit and loss account'],
             ])],
             'scheme': [
                 {'id': 's1', 'pt': 'Meaning/purpose of trade discount', 'm': 1, 'skill': 'concept'},
                 {'id': 's2', 'pt': 'Meaning/purpose of cash discount', 'm': 1, 'skill': 'concept'},
                 {'id': 's3', 'pt': 'Trade discount not recorded — entry at net price', 'm': 1, 'skill': 'concept'},
                 {'id': 's4', 'pt': 'Cash discount recorded as Discount Allowed/Received in P&L', 'm': 1, 'skill': 'concept'},
             ],
             'remarks': ['Good answers use a two-column table with a clear basis for each point.', 'Weak answers only define the terms and never say how they are recorded — that is half the marks.'],
             'mistakes': ['Saying both discounts are shown in the profit and loss account.', 'Mixing up which party has a gain and which has a loss for cash discount.'],
             'tips': ['For "distinguish" questions, a table with 4 bases is the fastest way to score.', 'End with the accounting treatment — it is usually what the question is really testing.']},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'journal',
             'q': 'Kiran Garments is registered under GST. In July 2026: (1) Jul 4 — bought goods on credit from Om Textiles ₹1,50,000. (2) Jul 18 — sold goods on credit to Rhea Fashions ₹2,40,000. Both supplies are within the State; CGST and SGST are 6% each. Pass journal entries for the two transactions, the set-off on 31 July and the payment of the net tax by cheque.',
             'model': [journal(Q3, 'Journal of Kiran Garments (July 2026)', 'jq3'),
                       wn('Net tax', f'Output CGST ₹{inr(q3_oc)} − Input CGST ₹{inr(q3_ic)} = ₹{inr(q3_net)}; SGST the same. Total paid ₹{inr(q3_net * 2)}.')],
             'scheme': [
                 {'id': 's1', 'pt': 'Purchase entry with Input CGST and SGST ₹9,000 each', 'm': 1, 'skill': 'computation'},
                 {'id': 's2', 'pt': 'Sales entry with Output CGST and SGST ₹14,400 each', 'm': 1, 'skill': 'computation'},
                 {'id': 's3', 'pt': 'Set-off entry: Output debited, Input credited (CGST with CGST, SGST with SGST)', 'm': 1.5, 'skill': 'concept'},
                 {'id': 's4', 'pt': 'Payment of net ₹10,800 with narration', 'm': 1.5, 'skill': 'presentation'},
             ],
             'remarks': ['Candidates who add GST to the cost of purchases lose the marks for the set-off as well.', 'Show the set-off working separately — examiners award step marks for it even if a figure goes wrong.'],
             'mistakes': ['Debiting GST to the Purchases account.', 'Setting off CGST credit against SGST.', 'Crediting Sales with the GST-inclusive amount.'],
             'tips': ['Keep separate Input and Output accounts for each tax.', 'Write the set-off as a working note before the entry.']},
        ],
        'revision': {
            'summary': ['Every transaction has equal debit and credit effects (double entry).', 'Golden rules — Personal: debit the receiver, credit the giver. Real: debit what comes in, credit what goes out. Nominal: debit expenses and losses, credit incomes and gains.',
                        'Modern rule — assets, expenses, drawings increase by debit; liabilities, capital, incomes increase by credit.', 'Journal format: Date | Particulars (Dr line, then "To" line) | L.F. | Dr | Cr, with narration.',
                        'GST: input tax is debited (recoverable), output tax credited (payable); set off, then pay the balance.'],
            'remember': ['Trade discount — never recorded. Cash discount — always recorded.', 'Drawings of goods / free samples / goods lost: always credit Purchases at cost.', 'CGST credit cannot pay SGST and SGST credit cannot pay CGST.'],
            'traps': ["Don't debit Purchases when buying an asset like furniture — debit the asset account.", "Don't record the list price; record the net invoice price.", "Don't forget the insurance claim admitted when goods are lost."],
        },
        'quickref': [
            {'k': 'Personal account', 'v': 'Debit the receiver, credit the giver'},
            {'k': 'Real account', 'v': 'Debit what comes in, credit what goes out'},
            {'k': 'Nominal account', 'v': 'Debit expenses and losses, credit incomes and gains'},
            {'k': 'Accounting equation', 'v': 'Assets = Liabilities + Capital'},
            {'k': 'Goods for personal use', 'v': 'Drawings A/c Dr. To Purchases A/c'},
            {'k': 'Free samples', 'v': 'Advertisement A/c Dr. To Purchases A/c'},
            {'k': 'GST set-off', 'v': 'Output CGST A/c Dr. To Input CGST A/c (same for SGST/IGST)'},
            {'k': 'Exam time', 'v': 'About 1.8 minutes per mark (100 marks in 3 hours)'},
        ],
    }
