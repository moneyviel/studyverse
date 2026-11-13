"""CA Intermediate · Paper 3A Income-tax Law · Chapter 3 Heads of Income · Unit 3 Profits and Gains of Business or Profession (Income-tax Act, 2025; tax year 2026-27).
Scope follows the ICAI study material; section numbers and limits are taken from it; explanations and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-a-ch03-u03'
T1 = 'Business, profession and the charge (s. 26)'
T2 = 'Method of accounting and ICDS'
T3 = 'Admissible deductions (ss. 28-32)'
T4 = 'Depreciation (ss. 33, 39, 41)'
T5 = 'Preliminary expenses and scientific research (ss. 44-45)'
T6 = 'Disallowances under s. 35 (taxes, TDS, partners)'
T7 = 'Related-party and cash payments (s. 36)'
T8 = 'Actual payment basis, deemed profits and stamp duty value (ss. 37, 38, 53)'
T9 = 'Books of account and tax audit (ss. 62-63)'
T10 = 'Presumptive taxation (s. 58)'


def build():
    # i1 — depreciation on a plant block with additional depreciation
    ck = Checks()
    wdv = ck.add('4000000+1200000+800000+200000-300000', 'Opening WDV + additions − sale proceeds')
    half = ck.add('800000*0.075', 'Machine used < 180 days: half of 15%')
    rest = ck.add('(5900000-800000)*0.15', 'Balance of block at 15%')
    add1 = ck.add('1200000*0.20', 'Additional depreciation, new machine used ≥ 180 days')
    add2 = ck.add('800000*0.10', 'Additional depreciation, new machine used < 180 days (balance 10% next year)')
    tot = ck.add('60000+765000+240000+80000', 'Total depreciation')
    close = ck.add('5900000-1145000', 'Closing WDV')
    i1 = {'id': 'i1', 'title': 'Plant block with additions, a sale and additional depreciation', 'difficulty': 'hard', 'minutes': 12,
          'q': 'Narmada Polymers Ltd., a manufacturer, has a plant and machinery block (15%) with WDV ₹40,00,000 on 1 April 2026. During tax year 2026-27: (a) new machine bought and installed in the factory on 10 May 2026 for ₹12,00,000; (b) second-hand machine bought on 1 June 2026 for ₹2,00,000; (c) new machine bought and put to use on 5 December 2026 for ₹8,00,000; (d) an old machine of the block sold on 20 January 2027 for ₹3,00,000. Compute depreciation and closing WDV.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['WDV before depreciation', '40,00,000 + 12,00,000 + 2,00,000 + 8,00,000 − 3,00,000', inr(wdv)],
              ['Normal depreciation on machine (c)', '8,00,000 × 7.5% (used under 180 days)', inr(half)],
              ['Normal depreciation on balance', '51,00,000 × 15%', inr(rest)],
              ['Additional depreciation on machine (a)', '12,00,000 × 20%', inr(add1)],
              ['Additional depreciation on machine (c)', '8,00,000 × 10% now; other 10% in 2027-28', inr(add2)],
              ['Total depreciation', '', inr(tot)],
              ['Closing WDV', '59,00,000 − 11,45,000', inr(close)]], title='Computation'),
              note('The second-hand machine gets normal depreciation as part of the block but no additional depreciation.')],
          'checks': list(ck)}

    # i2 — partner remuneration and interest limits u/s 35(e)
    ck2 = Checks()
    np_ = ck2.add('1500000-90000-1050000', 'Net profit after partner interest and salary')
    exint = ck2.add('600000*(0.15-0.12)', 'Interest above 12% disallowed')
    adj = ck2.add('360000+18000', 'Profit as per PGBP before remuneration add-back')
    bp = ck2.add('378000+1050000', 'Book profit = adjusted profit + remuneration debited')
    lim = ck2.add('max(300000,0.9*600000)+0.6*(1428000-600000)', 'Allowable remuneration limit')
    dis = ck2.add('1050000-1036800', 'Remuneration disallowed')
    inc2 = ck2.add('1428000-1036800', 'Business income of the firm')
    i2 = {'id': 'i2', 'title': 'Partner salary and interest in a firm', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Bhosale & Iyer, a firm with two working partners, earned ₹15,00,000 before partner interest and salary. Its deed authorises interest on capital at 15% (eligible capital ₹6,00,000) and total partner salary of ₹10,50,000, both debited to profit and loss. Compute book profit, allowable remuneration and business income for tax year 2026-27.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Net profit as per P&L', '15,00,000 − 90,000 − 10,50,000', inr(np_)],
              ['Add: interest above 12%', '6,00,000 × 3%', inr(exint)],
              ['Profit as per PGBP rules', '', inr(adj)],
              ['Add: partner salary debited', '', inr(1050000)],
              ['Book profit', '', inr(bp)],
              ['Limit on first ₹6,00,000', 'Higher of 3,00,000 and 90% × 6,00,000', inr(540000)],
              ['Limit on balance', '60% × 8,28,000', inr(496800)],
              ['Allowable remuneration', '', inr(lim)],
              ['Disallowed (10,50,000 − 10,36,800)', '', inr(dis)],
              ['Business income', 'Book profit − allowable remuneration', inr(inc2)]], title='Computation'),
              note('Interest is restricted first because book profit is computed after applying the business-income rules; only remuneration is then added back.')],
          'checks': list(ck2)}

    # i3 — presumptive income u/s 58
    ck3 = Checks()
    cap = ck3.add('0.05*26000000', '5% of turnover — cash ceiling for the ₹3 crore limit')
    dig = ck3.add('26000000-900000', 'Turnover received digitally (incl. before return due date)')
    pres = ck3.add('0.06*25100000+0.08*900000', 'Presumptive income')
    i3 = {'id': 'i3', 'title': 'Presumptive income of a retail trader', 'difficulty': 'core', 'minutes': 6,
          'q': 'Kavita, a resident individual running a stationery store, has turnover of ₹2,60,00,000 in tax year 2026-27. Cash receipts total ₹9,00,000; the rest came by UPI, cards and account payee cheques (some debtors paid in May 2027, before the return due date). Her books show profit of ₹14,00,000. Is she eligible for section 58, and what income is deemed?',
          'solution': [table(['Step', 'Working', '₹'], [
              ['5% of turnover', '2,60,00,000 × 5%', inr(cap)],
              ['Cash receipts', 'Within 5%, so the ₹3 crore limit applies — eligible', inr(900000)],
              ['Digital receipts', '2,60,00,000 − 9,00,000', inr(dig)],
              ['Presumptive income', '6% × 2,51,00,000 + 8% × 9,00,000', inr(pres)],
              ['Deemed income', 'Higher of 15,78,000 and actual 14,00,000', inr(pres)]], title='Computation'),
              note('If she declares the lower actual profit, she must keep books (s. 62) and get a tax audit (s. 63) if total income exceeds the basic exemption limit.')],
          'checks': list(ck3)}

    dep = table(['Asset (examples)', 'Rate'], [
        ['Residential buildings (not hotels)', '5%'], ['Other buildings', '10%'], ['Temporary wooden structures', '40%'],
        ['Furniture and fittings', '10%'], ['Plant and machinery — general', '15%'], ['Motor cars (not for hire)', '15%'],
        ['Computers and software; books of professionals', '40%'], ['Intangibles (patents, know-how, licences — not goodwill)', '25%']],
        title='Common depreciation rates (Appendix I)')
    disal = table(['Payment', 'TDS default', 'Disallowance'], [
        ['Sums due to residents that attract TDS', 'Not deducted, or deducted but not paid by return due date', '30%, allowed in the year tax is paid'],
        ['Interest, royalty, technical fees or other sum payable outside India or to a non-resident', 'Same', '100%, allowed in the year tax is paid'],
        ['Salary payable outside India or to a non-resident', 'Not deducted or not paid', 'Whole amount']], title='TDS-linked disallowances (s. 35)')
    pres_t = table(['Who', 'Turnover/receipts limit', 'Deemed profit'], [
        ['Resident individual, HUF or firm (not LLP) in any business except goods carriages', '₹2 crore; ₹3 crore if cash receipts ≤ 5%', '6% of digital receipts + 8% of other receipts, or higher actual profit'],
        ['Owner of up to 10 goods carriages', 'No turnover limit', '₹1,000 per ton per month (heavy vehicle) or ₹7,500 per vehicle per month, or higher actual'],
        ['Resident individual or firm (not LLP) in a specified profession', '₹50 lakh; ₹75 lakh if cash receipts ≤ 5%', '50% of gross receipts, or higher actual']], title='Section 58 at a glance')

    concepts = [
        C('c1', T1, [
            'Business includes any trade, commerce, manufacture or adventure in the nature of trade; profession needs special skill and qualification (law, medicine, accountancy); vocation is any calling pursued for a living.',
            'Section 26 charges profits of any business or profession carried on during the year, plus specific items such as profit on transfer of certain licences, export incentives, value of perquisites from business, sums received for non-compete or not sharing know-how, and interest, salary or commission received by a partner from his firm (only to the extent the firm was allowed it).',
            'The share of a partner in firm profit is exempt in his hands. A speculation business — trading in commodities or shares settled without actual delivery, other than specified hedging and exchange transactions — is treated as distinct from other business; its losses are ring-fenced.',
            'Profits are computed under the rules of this head; income of every business is aggregated except speculation.'],
          'A business is taxed on what it actually earns from its trading activity; the head looks at the activity, not the label.',
          'A doctor\'s fees are professional income; his gains from intraday share trading are speculative income kept in a separate box.'),
        C('c2', T2, [
            'Income under this head (and other sources) is computed on the cash or mercantile basis regularly followed by the assessee (s. 276). A hybrid system is not permitted.',
            'The Government has notified 10 Income Computation and Disclosure Standards (ICDS) for assessees following the mercantile system; they govern the tax computation, not the books. Individuals and HUFs not liable to tax audit are outside ICDS.',
            'Where the method is not correct or complete, or ICDS is not followed, the Assessing Officer may make a best judgment assessment.'],
          'Tax picks up the accounting method the business actually lives by, with ICDS as the tax-time referee.',
          'A trader on accrual basis cannot shift interest receipts to cash basis to delay tax.'),
        C('c3', T3, [
            'Rent, rates, taxes, repairs and insurance for premises and for plant, machinery and furniture used for business are deductible (current repairs only — not capital improvement) [s. 28].',
            'Employee items [s. 29]: insurance on stock and employee health (premium paid other than in cash), bonus or commission not payable as profit dividend, employer contribution to recognised PF, approved superannuation and gratuity funds, and employer NPS contribution up to 14% of salary (salary includes dearness allowance where it forms part of retirement benefits). Employee contributions received by an employer are deductible only if credited by the due date of the return.',
            'Bad debts [s. 31] are deductible when written off as irrecoverable in the books, provided they were earlier taken into income or are money lent in a banking or money-lending business. A later recovery is taxed as business income.',
            'Other items [s. 32]: interest on capital borrowed for business (interest until the asset is first put to use is capitalised), discount on zero coupon bonds over their life, family planning expenditure of a company (capital part over five years), securities transaction tax, and a general residuary deduction for revenue expenditure laid out wholly and exclusively for business — not capital, personal or for an illegal purpose.'],
          'The law lists the usual running costs of a business and then sweeps in the rest through a general test: revenue in nature and wholly for business.',
          'Fines for breaking the law and bribes fail the residuary test even though they are paid in the course of business.'),
        C('c4', T4, [
            'Depreciation [s. 33] is mandatory and computed on the WDV of each block of assets (same class, same rate) for tangible assets — buildings, machinery, plant, furniture — and specified intangibles (know-how, patents, copyrights, trademarks, licences, franchises). Goodwill of a business is not depreciable.',
            'Conditions: the assessee owns the asset (wholly or partly) and uses it for business or profession during the year. If an asset bought this year is used for under 180 days of the year, only half the rate applies.',
            'Block WDV [s. 41] = opening WDV + actual cost of additions − moneys payable (with scrap) for assets of the block sold, discarded or destroyed. If proceeds exceed the block or the block empties, the result is a capital gain (Capital Gains unit), not depreciation.',
            'Additional depreciation of 20% of actual cost is available for new plant and machinery (not second-hand, office appliances, road vehicles, or items installed in offices or residences) acquired by a manufacturer or power business; if used under 180 days, 10% now and 10% the next year. Individuals, HUFs, AOPs, BOIs and artificial juridical persons get it only under the optional regime.',
            'Power undertakings may opt for straight-line rates on each asset [s. 33(2)] and get terminal depreciation on sale below WDV. Unabsorbed depreciation is carried forward without time limit [s. 33(11)]; in a year, current depreciation is set off first, then brought-forward business loss, then unabsorbed depreciation.'],
          'Depreciation spreads the cost of a long-lived asset over its useful life through a pool rather than asset by asset.',
          'A printing press bought new in February gets only 7.5% normal depreciation that year, plus 10% additional now and 10% next year.',
          blocks=[dep]),
        C('c5', T5, [
            'Preliminary expenses [s. 44] — feasibility and project reports, market surveys, engineering services, legal drafting for setting up, and, for companies, drafting the memorandum and articles, registration fees and public-issue costs — are amortised in five equal annual instalments.',
            'The qualifying amount is capped at 5% of the cost of the project; an Indian company may instead use 5% of capital employed. Non-company assessees (other than co-operatives) need their accounts audited and an audit report furnished; a statement of the expenses must be filed.',
            'Scientific research [s. 45] related to the business: revenue and capital expenditure (except land) is deductible in full in the year incurred; spending in the three years before commencement is allowed in the year business starts. If a research asset is later sold, the receipt (up to the deduction allowed) is taxed as business income.'],
          'Set-up costs are written off over five years, but research spending gets an immediate full deduction to encourage innovation.',
          'A start-up\'s market survey of ₹2 lakh is deducted at ₹40,000 a year for five years, within the 5% project-cost cap.'),
        C('c6', T6, [
            'Not deductible for any assessee [s. 35]: income tax (with surcharge and cess), and tax paid by an employer on employees\' non-monetary perquisites (the perquisite is exempt for the employee but the tax is not deductible for the employer).',
            'TDS defaults (table): 30% of a sum payable to a resident and 100% of interest, royalty, fees for technical services or other sums payable to a non-resident or outside India, if tax is not deducted or, after deduction, not paid by the due date of return. The amount is allowed in the year the tax is paid. If the payee has filed a return including the sum and paid tax on it (accountant\'s certificate), tax is deemed deducted and paid on the payee\'s return date.',
            '"Payable" covers amounts paid during the year as well as amounts outstanding at the year end (CBDT view).',
            'Firms and LLPs [s. 35(e)]: remuneration to non-working partners is disallowed; remuneration and interest must be authorised by the deed and cannot relate to a period before the deed; interest above 12% simple p.a. is disallowed; working-partner remuneration is limited by book profit — on the first ₹6 lakh (or a loss) the higher of ₹3 lakh and 90%, and 60% of the balance.'],
          'The law will not let a business deduct its own income tax, or an expense on which it ignored its TDS duty, or an unlimited payout to its own partners.',
          'A firm that signs a deed on 1 October allowing salary from 1 April gets a deduction only for October to March.',
          blocks=[disal]),
        C('c7', T7, [
            'Payments to specified persons [s. 36(2)]: the Assessing Officer may disallow the part he considers excessive or unreasonable having regard to market value, legitimate business needs or benefit derived. Specified persons include relatives (spouse, brother, sister, lineal ascendants and descendants) and persons with or in whom there is a substantial interest — at least 20% of voting power in a company or 20% of profits in other cases.',
            'Cash and other non-specified modes [s. 36(4)]: an expense paid to one person in one day in excess of ₹10,000 (₹35,000 for payments to transport operators for goods carriages) otherwise than by account payee cheque or draft, bank ECS or a prescribed electronic mode (cards, net banking, UPI, IMPS, NEFT, RTGS, BHIM Aadhaar Pay, CBDC wallets) is fully disallowed.',
            'If an expense allowed earlier on accrual basis is paid in a later year in such a mode above the limit, the payment is deemed business income of that later year [s. 36(5)]. Loan repayments and payments by commission agents for consignment goods are outside the rule since they are not deductible expenses; Rule 26 lists further exceptions.'],
          'Paying family generously or paying big bills in cash both invite the taxman to strike out the deduction.',
          'Three cash payments of ₹4,000 each to one supplier in one day add up to ₹12,000 and the whole ₹12,000 is lost.'),
        C('c8', T8, [
            'Actual payment basis [s. 37]: taxes, duties, cess or fees; employer contributions to PF, superannuation, gratuity or welfare funds; leave encashment; bonus or commission to employees; interest to specified financial entities (public financial institutions, state financial corporations, notified NBFCs, scheduled and co-operative banks); and amounts payable to Indian Railways are deductible only when paid. Payment by the return due date allows the deduction in the year of liability.',
            'Interest converted into a fresh loan or debenture is not treated as paid; it is allowed when the converted amount is actually repaid. Dues to micro or small enterprises beyond the MSMED Act time limit are allowed only on payment, and the return-date relief does not apply to them.',
            'Employee contributions to welfare funds are outside section 37: if not credited by the due date of return, they are never deductible.',
            'Deemed profits [s. 38]: remission or cessation of a trading liability earlier deducted, balancing charge, sale of research assets and recovery of bad debts are taxed even if the business has ceased.',
            'Stamp duty value [s. 53]: on transfer of land or building held as stock-in-trade, stamp duty value replaces a lower consideration unless it is within 110% of the consideration; the agreement-date value can be used if part payment was received by banking or online mode on or before the agreement.'],
          'Some liabilities are so often provided and never paid that the law waits for the cheque before allowing them.',
          'Bonus for 2026-27 paid on 25 September 2027, before a 31 October return date, is allowed in 2026-27.'),
        C('c9', T9, [
            'Books of account [s. 62] must be kept by every person in a specified profession (legal, medical, engineering, architectural, accountancy, technical consultancy, interior decoration, information technology, company secretary and notified professions).',
            'Others must keep books if, in any of the three preceding years, income exceeded ₹2,50,000 or turnover exceeded ₹25,00,000 (individual/HUF) or ₹1,20,000 and ₹10,00,000 (others); new businesses test the likely figures. Anyone declaring lower profit than the presumptive amount must also keep books.',
            'Tax audit [s. 63] is required where business turnover exceeds ₹1 crore — raised to ₹10 crore if cash receipts and cash payments each do not exceed 5% of the total — or professional receipts exceed ₹50 lakh, and where a section 58 assessee claims lower profit. A non-account-payee cheque or draft counts as cash.',
            'The report (Form 26) must be furnished by the specified date, one month before the return due date. Failure attracts a fee of ₹75,000, rising to ₹1,50,000 if the delay exceeds one month. A company audited under the Companies Act does not need a second audit but still furnishes the tax audit report.'],
          'Bigger or cash-heavy businesses must show their working to a chartered accountant before the return is filed.',
          'A ₹6 crore trader who collects and pays 98% by bank transfer is below the ₹10 crore threshold and escapes tax audit.'),
        C('c10', T10, [
            'Section 58 lets small resident businesses and professionals declare a fixed percentage as profit without maintaining detailed accounts (table). An eligible business assessee must not claim Part C deductions of Chapter VIII, carry on a specified profession, earn commission or brokerage, or run an agency business.',
            'Receipts by a banking or online mode during the year or by the return due date count as digital; non-account-payee cheques count as cash. For firms, partner salary and interest within s. 35(e) limits are deducted from presumptive income.',
            'No other deduction, allowance or loss is allowed against presumptive income, and assets are treated as if depreciation had been allowed each year.',
            'A business assessee who opts out within the five years after opting in cannot return to the scheme for the next five years and must keep books and get audited if income exceeds the basic exemption limit. Declaring lower profit similarly triggers books and audit.'],
          'Presumptive tax trades accuracy for simplicity: accept a fixed margin and skip the paperwork.',
          'A small cloth trader with ₹1.5 crore of UPI sales can declare ₹9 lakh (6%) and keep only basic records.',
          blocks=[pres_t]),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Year-end disallowance review', 'role': 'Tax audit assistant',
         'situation': 'You review the ledger of a trading firm before the tax audit report is signed.',
         'steps': ['List payments where TDS was due; check deduction and deposit dates against the return due date.', 'Scan cash book for payments to one party in one day above ₹10,000 (₹35,000 for transporters).', 'Check statutory dues, bonus and bank interest paid by the return due date.', 'Test partner salary and interest against the deed and s. 35(e) limits.'],
         'takeaway': 'Most disallowances are timing or mode issues that a dated checklist catches.'},
        {'id': 'j2', 'title': 'Advising on presumptive taxation', 'role': 'Tax consultant',
         'situation': 'A kirana store owner with ₹1.8 crore turnover asks whether to opt for section 58.',
         'steps': ['Confirm eligibility: resident individual, no commission or agency income, no Part C deductions.', 'Split receipts into digital and cash; compute 6% and 8%.', 'Compare with actual profit and compliance cost of books and audit.', 'Explain the five-year lock-in consequence of opting out.'],
         'takeaway': 'Choose presumptive tax with the five-year horizon in view, not just this year.'},
    ]

    mcqs = [
        Q('m1', 'A partner receives ₹6,00,000 salary from a firm, of which the firm was allowed ₹5,20,000. The amount taxable in the partner\'s hands as business income is:', ['₹5,20,000', '₹6,00,000', '₹80,000', 'Nil'], 0,
          'A partner is taxed on salary, bonus, commission or interest from the firm only to the extent the firm was allowed a deduction under section 35(e); the disallowed ₹80,000 is not taxed again. His share of firm profit is exempt. In practice: obtain the firm computation before filing.', 'c1', T1, 'moderate', check=520000),
        Q('m2', 'Which of these is a speculative transaction?', ['A share trade settled by paying the price difference without delivery, not on a recognised exchange or for hedging', 'A delivery-based purchase of shares', 'A hedging contract by a manufacturer for raw material', 'An eligible derivative trade on a recognised exchange'], 0,
          'A speculative transaction is a contract for purchase or sale of commodities or shares settled otherwise than by actual delivery, excluding hedging contracts and eligible exchange-traded derivatives. Speculation is treated as a separate business. In practice: intraday equity trades are the common example.', 'c1', T1),
        Q('m3', 'Under section 276, an assessee may compute business income on:', ['Cash or mercantile system regularly followed', 'A mix of cash and mercantile for different items', 'Any system chosen each year', 'Mercantile system only'], 0,
          'Income under this head is computed on the cash or mercantile system regularly employed; a hybrid system is not recognised. ICDS apply to mercantile-basis assessees, except individuals and HUFs not liable to tax audit. In practice: consistency across years is essential.', 'c2', T2),
        Q('m4', 'Interest on a loan for a new machine, for the period before the machine is first put to use, is:', ['Added to the actual cost of the machine', 'Deductible as revenue expense', 'Disallowed permanently', 'Deductible in five instalments'], 0,
          'Interest on capital borrowed for acquiring an asset, for the period until it is first put to use, is capitalised in its actual cost and recovered through depreciation; later interest is a revenue deduction. In practice: separate the two periods in the loan schedule.', 'c3', T3),
        Q('m5', 'Employer\'s contribution to NPS for an employee is deductible as business expenditure up to:', ['14% of salary', '10% of salary', '12% of salary', 'Any amount'], 0,
          'Section 29 allows an employer\'s NPS contribution to the extent it does not exceed 14% of the employee\'s salary, with dearness allowance counted in salary where it ranks for retirement benefits. Any excess is disallowed. In practice: payroll caps contributions at 14%.', 'c3', T3, 'moderate'),
        Q('m6', 'A bad debt is deductible if:', ['It is written off as irrecoverable in the books and was earlier taken into income (or is money lent in banking/money-lending business)', 'It is merely provided for in the books', 'The debtor is a relative', 'It is a capital loss'], 0,
          'Section 31 requires actual write-off in the books, and the debt must have been included in income earlier or be a loan in the ordinary course of banking or money-lending. A mere provision is not enough. In practice: recoveries later are taxed as income.', 'c3', T3),
        Q('m7', 'A machine bought this year is used for only 120 days of the year. Depreciation is:', ['50% of the normal rate', 'Nil', 'Full normal rate', '75% of the normal rate'], 0,
          'Section 33(4) restricts depreciation to half the prescribed rate for an asset bought in the year whose business use that year falls short of 180 days. Additional depreciation follows the same split, with the balance in the next year. In practice: purchase timing matters.', 'c4', T4),
        Q('m8', 'Additional depreciation is NOT available on:', ['A second-hand machine bought from another manufacturer', 'A new machine installed in a factory', 'New plant for a power-generation business', 'New machinery of a printing company'], 0,
          'Additional depreciation applies to new plant and machinery that nobody used before, installed for manufacture, production or power business; second-hand machinery, office appliances, road vehicles and assets in office or residential premises are excluded. In practice: check the vendor invoice.', 'c4', T4),
        Q('m9', 'An individual manufacturer who pays tax under the default regime claims additional depreciation. The claim is:', ['Not allowed — available only if he opts for the optional regime', 'Allowed at 20%', 'Allowed at 10%', 'Allowed only on cars'], 0,
          'For individuals, HUFs, AOPs (other than co-operatives), BOIs and artificial juridical persons, additional depreciation is allowed only when they opt out of the default regime under section 202. Companies are not affected by this condition. In practice: weigh it when choosing the regime.', 'c4', T4, 'moderate'),
        Q('m10', 'Opening WDV of a 40% block is ₹3,00,000; an asset of the block is sold for ₹3,50,000 and no asset is added. The result is:', ['A short-term capital gain of ₹50,000 and no depreciation', 'Depreciation of ₹1,20,000', 'A balancing charge taxed as business income', 'A business loss'], 0,
          'When moneys payable on sale exceed the block WDV plus additions, the block cannot go negative; the excess of ₹50,000 is taxed as a short-term capital gain and no depreciation is allowed for that block. Balancing charge applies only to power undertakings on straight-line basis. In practice: watch the block balance before selling.', 'c4', T4, 'hard'),
        Q('m11', 'Qualifying preliminary expenses of a non-corporate resident are amortised over five years, subject to a cap of:', ['5% of the cost of the project', '10% of the cost of the project', '5% of turnover', '2.5% of capital employed'], 0,
          'Section 44 limits the aggregate qualifying amount to 5% of cost of the project for non-corporate residents; an Indian company may choose 5% of capital employed instead. One-fifth of the eligible amount is allowed each year. In practice: the excess is simply ignored.', 'c5', T5),
        Q('m12', 'In-house scientific research capital expenditure on a laboratory building (excluding land) related to the business is:', ['Fully deductible in the year incurred', 'Depreciated at 10%', 'Amortised over five years', 'Not deductible'], 0,
          'Section 45 allows the whole of capital expenditure on scientific research related to the business, other than on land, in the year incurred; pre-commencement spending of three years is allowed in the year business starts. No depreciation is then allowed on the asset. In practice: keep research costs coded separately.', 'c5', T5),
        Q('m13', 'Rent of ₹5,00,000 paid to a resident landlord without deducting tax at source (tax still unpaid) leads to a disallowance of:', ['₹1,50,000', '₹5,00,000', 'Nil', '₹50,000'], 0,
          'Section 35(b)(i) disallows 30% of any sum payable to a resident where tax deductible under the TDS chapter is not deducted, or not paid by the return due date; 30% of ₹5,00,000 is ₹1,50,000, allowed later in the year the tax is paid. In practice: deposit TDS before the due date.', 'c6', T6, 'core', check=150000),
        Q('m14', 'Fees for technical services payable to a foreign company without TDS are:', ['Disallowed in full until the tax is paid', 'Disallowed at 30%', 'Allowed fully', 'Disallowed permanently'], 0,
          'For interest, royalty, fees for technical services or other sums payable outside India or to a non-resident, the disallowance is 100% if tax is not deducted or not paid in time; the amount is allowed in the year the tax is paid. In practice: cross-border payments need TDS planning.', 'c6', T6),
        Q('m15', 'A firm\'s book profit is ₹4,00,000. The maximum allowable remuneration to working partners is:', ['₹3,60,000', '₹3,00,000', '₹2,40,000', '₹4,00,000'], 0,
          'On the first ₹6 lakh of book profit the limit is the higher of ₹3,00,000 and 90% of book profit; 90% of ₹4,00,000 is ₹3,60,000, which exceeds ₹3,00,000. There is no balance above ₹6 lakh. In practice: compute book profit after interest restriction.', 'c6', T6, 'moderate', check=360000),
        Q('m16', 'A transporter is paid ₹30,000 in cash in one day for hire of a goods carriage. The disallowance is:', ['Nil, as the limit for transport operators is ₹35,000', '₹30,000', '₹20,000', '₹9,000'], 0,
          'Section 36(6) raises the cash limit to ₹35,000 per day when the payee is a goods-carriage transport operator; the general limit is ₹10,000. ₹30,000 is within the higher limit. In practice: record the operator status in the voucher.', 'c7', T7, 'moderate'),
        Q('m17', 'For section 36(2), substantial interest in a company means beneficial ownership of equity shares with voting power of at least:', ['20% of voting power', '10% of voting power', '26% of voting power', '51% of voting power'], 0,
          'Substantial interest means beneficial ownership of equity shares carrying not less than 20% of voting power in a company, or entitlement to at least 20% of profits in other businesses, at any time during the year. In practice: map the group before reviewing related-party prices.', 'c7', T7),
        Q('m18', 'Employer\'s PF contribution for March 2027 is paid on 15 October 2027; the return due date is 31 October 2027. It is deductible in:', ['Tax year 2026-27', 'Tax year 2027-28', 'Never', 'Spread over two years'], 0,
          'Employer contributions are covered by section 37 but payment by the return due date allows the deduction in the year of liability, 2026-27. Employee contributions are different: deposited late they are never deductible. In practice: separate the two in payroll.', 'c8', T8),
        Q('m19', 'A builder sells a flat (stock-in-trade) for ₹80,00,000; stamp duty value is ₹86,00,000. Sale consideration for business income is:', ['₹80,00,000', '₹86,00,000', '₹83,00,000', '₹88,00,000'], 0,
          'Section 53 substitutes stamp duty value only when it exceeds 110% of the consideration; 110% of ₹80 lakh is ₹88 lakh and ₹86 lakh is within it, so actual consideration stands. In practice: compute the 110% band first.', 'c8', T8, 'hard', check=8000000),
        Q('m20', 'Tax audit for a business assessee (not under s. 58) whose cash receipts and payments are each within 5% of totals is required only when turnover exceeds:', ['₹10 crore', '₹1 crore', '₹2 crore', '₹50 lakh'], 0,
          'Section 63 requires audit when business turnover exceeds ₹1 crore, but the limit rises to ₹10 crore if aggregate cash receipts and cash payments do not exceed 5% each. Professionals face a ₹50 lakh receipts limit. In practice: track cash ratios through the year.', 'c9', T9, 'moderate', check=10),
        Q('m21', 'A resident chartered accountant with gross receipts of ₹70 lakh, cash receipts below 5%, opts for section 58. Deemed profit is:', ['₹35,00,000 or higher actual profit', '₹4,20,000', '₹5,60,000', 'Not eligible'], 0,
          'Specified professionals with receipts up to ₹75 lakh (where cash is within 5%) may declare 50% of gross receipts, or higher actual profit; 50% of ₹70 lakh is ₹35 lakh. The 6%/8% rates apply only to businesses. In practice: professionals rarely have actual margins above 50%.', 'c10', T10, 'moderate', check=3500000),
        Q('m22', 'Which assessee is NOT eligible for presumptive taxation of a business at 6%/8%?', ['A resident LLP', 'A resident HUF', 'A resident partnership firm', 'A resident individual'], 0,
          'Eligible assessees are resident individuals, HUFs and partnership firms, excluding LLPs, who do not claim Part C deductions or earn commission, brokerage or agency income. Companies are also outside the scheme. In practice: an LLP must compute actual profits.', 'c10', T10),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Block WDV', 1, 'computation', 'wdv', nums=[wdv]),
           S('s2', 'Half rate for < 180 days', 1.5, 'computation', '180|half|7.5', nums=[half]),
           S('s3', 'Normal depreciation on balance', 1, 'computation', '15%', nums=[rest]),
           S('s4', 'Additional depreciation', 1.5, 'computation', 'additional', nums=[add1, add2]),
           S('s5', 'Total and closing WDV', 1, 'computation', 'closing|total', nums=[tot, close])],
          ['Show the second-hand machine exclusion.'], ['Giving additional depreciation on the second-hand machine.'], ['Step table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Interest restricted to 12%', 1.5, 'computation', '12%', nums=[exint]),
           S('s2', 'Book profit', 1.5, 'computation', 'book profit', nums=[bp]),
           S('s3', 'Remuneration limit', 2, 'computation', '90%|60%', nums=[lim]),
           S('s4', 'Business income', 1, 'computation', 'business income', nums=[inc2])],
          ['Restrict interest before computing book profit.'], ['Adding back interest in full to book profit.'], ['Step table.'], pad='table', checks=list(ck2)),
        W('q3', 4, i3['q'], i3['solution'],
          [S('s1', 'Eligibility via 5% cash test', 1.5, 'concept', '5%|3 crore', nums=[cap]),
           S('s2', '6% and 8% split', 1.5, 'computation', '6%', '8%', nums=[pres]),
           S('s3', 'Higher of presumptive and actual', 1, 'concept', 'higher')],
          ['Count digital receipts up to the return due date.'], ['Applying the ₹2 crore limit despite low cash receipts.'], ['Table.'], pad='table', checks=list(ck3)),
        W('q4', 4, 'Explain which deductions are allowed only on actual payment under section 37 and when payment after the year end still allows the deduction in the year of liability.',
          [ul(['Taxes, duties, cess or fees under any law.', 'Employer contributions to PF, superannuation, gratuity or welfare funds.', 'Leave encashment, and bonus or commission to employees.', 'Interest to specified financial entities such as scheduled banks and state financial corporations; converted interest only when repaid.', 'Sums payable to Indian Railways for use of its assets.', 'Dues to micro or small enterprises paid beyond the MSMED Act period.']),
           p('Payment of the first five categories after the year end but on or before the due date of the return allows the deduction in the year of liability; otherwise it is allowed in the year of payment. The relief does not extend to delayed MSE dues.')],
          [S('s1', 'Taxes and duties', 0.5, 'concept', 'tax|duty'),
           S('s2', 'Employer fund contributions', 0.75, 'concept', 'provident|fund'),
           S('s3', 'Leave, bonus, commission', 0.75, 'concept', 'bonus|leave'),
           S('s4', 'Interest to specified entities', 0.75, 'concept', 'interest|bank'),
           S('s5', 'Return due date relief', 1.25, 'concept', 'due date|return')],
          ['List categories, then the due-date rule.'], ['Applying the due-date relief to MSE dues.'], ['Bulleted list.']),
    ]

    viva = [
        V('v1', 'When is depreciation restricted?',
          'When an asset bought during the year is put to use for business for under 180 days in that year, only half of the prescribed rate is allowed.',
          [P('p1', 'Used under 180 days', 6, '180'), P('p2', 'Half the rate', 4, 'half|50%')], 'c4'),
        V('v2', 'What are the limits on working-partner remuneration?',
          'On the first 6 lakh rupees of book profit or a loss, the higher of 3 lakh rupees and 90% of book profit; on the remaining book profit, 60%.',
          [P('p1', 'Higher of ₹3 lakh and 90%', 6, '90'), P('p2', '60% of balance', 4, '60')], 'c6'),
        V('v3', 'What happens if tax is not deducted on rent paid to a resident?',
          '30% of the rent is disallowed now; that portion is allowed later, once the TDS is actually deposited.',
          [P('p1', '30% disallowed', 6, '30'), P('p2', 'Allowed when paid', 4, 'later|deposited')], 'c6'),
        V('v4', 'What is the cash payment limit for business expenses?',
          '10,000 rupees to one person in one day otherwise than through banking or prescribed electronic modes, or 35,000 rupees for goods carriage operators.',
          [P('p1', '₹10,000 per person per day', 6, '10,000|10000'), P('p2', '₹35,000 for transporters', 4, '35,000|35000|transport')], 'c7'),
        V('v5', 'What profit is deemed under section 58 for an eligible trader?',
          '6% of turnover received through banking or online modes and 8% of the remaining turnover, or a higher actual profit if declared.',
          [P('p1', '6% digital', 4, '6%'), P('p2', '8% other', 4, '8%'), P('p3', 'Higher actual', 2, 'higher')], 'c10'),
    ]

    cases = [{'id': 'k1', 'title': 'Shah Hardware Traders', 'difficulty': 'moderate',
              'case': 'Rakesh Shah, a resident individual, runs a hardware shop. Tax year 2026-27 turnover is ₹1,40,00,000, all digital except ₹6,00,000 cash. He paid a supplier ₹18,000 in cash on one day, paid rent of ₹3,60,000 to a resident without TDS, and has not deposited GST of ₹40,000 for March 2027 by the return due date. His books show profit of ₹10,20,000.',
              'mcqs': [
                  M('k1a', 'If he opts for section 58, his deemed income is:', ['₹10,20,000', '₹8,52,000', '₹11,20,000', '₹8,40,000'], 0,
                    'Presumptive income is 6% of ₹1,34,00,000 (₹8,04,000) plus 8% of ₹6,00,000 (₹48,000), totalling ₹8,52,000; since his actual profit of ₹10,20,000 is higher, the deemed income is the higher amount. In practice: section 58 sets a floor, not a ceiling.', 'hard', check=1020000, topic=T10),
                  M('k1b', 'Under regular computation, the cash payment of ₹18,000 to the supplier results in a disallowance of:', ['₹18,000', '₹8,000', 'Nil', '₹5,400'], 0,
                    'Where payment to one person in a day exceeds ₹10,000 otherwise than by a specified banking or online mode, the entire expenditure is disallowed, not merely the excess over ₹10,000. In practice: split bills do not help if paid the same day.', 'core', check=18000, topic=T7),
                  M('k1c', 'Whether TDS was required on rent depends on whether he:', ['Had turnover above ₹1 crore in the preceding tax year', 'Is a company', 'Paid rent in cash', 'Owns the premises'], 0,
                    'For individuals and HUFs, many TDS obligations apply only if business turnover exceeded ₹1 crore (or professional receipts ₹50 lakh) in the immediately preceding tax year. If required and not deducted, 30% of the rent is disallowed. In practice: check last year\'s turnover first.', 'moderate', topic=T6),
                  M('k1d', 'The ₹40,000 GST unpaid by the return due date is:', ['Deductible only in the year actually paid', 'Deductible in 2026-27 regardless', 'Never deductible', 'Deductible at 30%'], 0,
                    'Taxes and duties are allowed only on actual payment under section 37; payment after the return due date shifts the deduction to the year of payment rather than losing it permanently. In practice: clear statutory dues before filing.', 'core', topic=T8),
              ]}]

    return unit(UID, 'p3', 'int-p3-a-ch03', 3, 'Profits and Gains of Business or Profession',
                ['Identify income chargeable under business or profession and the method of accounting.',
                 'Apply admissible deductions including depreciation, preliminary expenses and research.',
                 'Apply disallowances for TDS defaults, partner payments, related parties, cash payments and unpaid dues.',
                 'State the requirements for books of account and tax audit.',
                 'Compute presumptive income under section 58.'],
                {'difficulty': 'hard', 'minutes': {'learn': 75, 'practice': 60}, 'prereq': ['int-p3-a-ch03-u02'],
                 'exam_tip': 'Expect a business-income computation from a P&L with depreciation, TDS and cash disallowances, plus a firm remuneration or section 58 question.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Charge s. 26 includes partner salary/interest only to the extent allowed to the firm.', 'Cash or mercantile basis (s. 276); ICDS for mercantile assessees.',
                             'Depreciation on block WDV; half rate under 180 days; additional 20% on new plant for manufacturers.', 'Preliminary expenses: 1/5 a year, capped at 5%.',
                             'TDS default: 30% (resident) or 100% (non-resident) disallowed until paid.', 'Partner interest ≤ 12%; remuneration limit 90%/₹3 lakh on first ₹6 lakh, 60% beyond.',
                             'Cash expense > ₹10,000 a day (₹35,000 transporters) disallowed.', 'Statutory dues, bonus, bank interest allowed on payment (by return due date).',
                             'Audit: ₹1 crore / ₹10 crore (cash ≤ 5%) / ₹50 lakh profession.', 'Presumptive: 6%/8% up to ₹2 crore (₹3 crore); professions 50% up to ₹50 lakh (₹75 lakh).'],
                 'remember': ['Employee welfare contributions deposited late are never deductible.', 'Stamp duty value replaces consideration only beyond 110%.'],
                 'traps': ['Additional depreciation not for second-hand assets.', 'LLPs cannot use section 58.']},
                [('Half-rate depreciation', 'Used < 180 days'), ('Additional depreciation', '20% (10% + 10% if < 180 days)'), ('TDS default — resident', '30% disallowed'),
                 ('Partner interest cap', '12% simple p.a.'), ('Cash payment limit', '₹10,000 / ₹35,000'), ('Tax audit — business', '₹1 crore / ₹10 crore'),
                 ('Presumptive business', '6% digital, 8% other'), ('Presumptive profession', '50% of receipts')],
                viva, cases,
                topics=['Structured Sectional Learning', 'Meaning of Business and Profession', 'Method of Accounting', 'Income Chargeable under this Head', 'Speculation Business',
                        'Manner of Computing Profits and Gains of Business or Profession', 'Admissible Deductions', 'Amounts not Deductible in Certain Circumstances',
                        'Expenses or Payment not Deductible in Certain Circumstances', 'Certain Deductions Allowed on Actual Payment Basis Only',
                        'Certain Sums Deemed as Profits and Gains of Business or Profession', 'Treatment of Foreign Exchange Fluctuations',
                        'Stamp Duty Value of Land and Building', 'Maintenance of Books of Accounts', 'Tax Audit', 'Presumptive Taxation', 'Computation of Business Income'])
