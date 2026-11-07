"""CA Foundation · Paper 1 Accounting · Chapter 11 Company Accounts · Unit 3 Issue of Debentures.
Original explanations, names and numbers (structure and scope follow the ICAI study material)."""
from lib import *
from ca_viva import P, ALT, V
from ca_cases import M

UID = 'fnd-p1-ch11-u03'


def mcq(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check: d['check'] = check
    return d


def S(sid, pt, m, skill): return {'id': sid, 'pt': pt, 'm': m, 'skill': skill}


def build():
    # ---------------- Illustration 1: six issue/redemption combinations ----------------
    c1 = Checks()
    n = 10000
    fv = c1.add('10000*100', 'Face value of 10,000 debentures of ₹100')
    b_cash = c1.add('10000*95', '(b) cash at ₹95'); b_disc = c1.add('10000*5', '(b) discount')
    c_cash = c1.add('10000*105', '(c) cash at ₹105'); c_prem = c1.add('10000*5', '(c) securities premium')
    d_loss = c1.add('10000*10', '(d) loss = premium on redemption ₹10')
    e_cash = c1.add('10000*96', '(e) cash at ₹96'); e_loss = c1.add('10000*(4+5)', '(e) loss = discount ₹4 + redemption premium ₹5')
    e_prp = c1.add('10000*5', '(e) premium on redemption')
    f_cash = c1.add('10000*104', '(f) cash at ₹104'); f_sp = c1.add('10000*4', '(f) securities premium'); f_prp = c1.add('10000*6', '(f) premium on redemption = loss')
    E1 = [
        je('(a)', [('Bank A/c', fv)], [('10% Debentures A/c', fv)], 'Being 10,000 debentures issued at par, redeemable at par'),
        je('(b)', [('Bank A/c', b_cash), ('Discount on Issue of Debentures A/c', b_disc)], [('10% Debentures A/c', fv)], 'Being debentures issued at ₹95, redeemable at par'),
        je('(c)', [('Bank A/c', c_cash)], [('10% Debentures A/c', fv), ('Securities Premium A/c', c_prem)], 'Being debentures issued at ₹105, redeemable at par'),
        je('(d)', [('Bank A/c', fv), ('Loss on Issue of Debentures A/c', d_loss)], [('10% Debentures A/c', fv), ('Premium on Redemption of Debentures A/c', d_loss)], 'Being debentures issued at par, redeemable at ₹110'),
        je('(e)', [('Bank A/c', e_cash), ('Loss on Issue of Debentures A/c', e_loss)], [('10% Debentures A/c', fv), ('Premium on Redemption of Debentures A/c', e_prp)], 'Being debentures issued at ₹96, redeemable at ₹105'),
        je('(f)', [('Bank A/c', f_cash), ('Loss on Issue of Debentures A/c', f_prp)], [('10% Debentures A/c', fv), ('Securities Premium A/c', f_sp), ('Premium on Redemption of Debentures A/c', f_prp)], 'Being debentures issued at ₹104, redeemable at ₹106'),
    ]

    # ---------------- Illustration 2: instalments with oversubscription ----------------
    c2 = Checks()
    app = c2.add('26000*40', 'Application money on 26,000 debentures @ ₹40')
    ref = c2.add('2000*40', 'Refund on 2,000 rejected')
    tod = c2.add('20000*40', 'Application money transferred to debentures')
    exc = c2.add('4000*40', 'Excess on pro-rata applicants adjusted to allotment')
    allot = c2.add('20000*55', 'Allotment money due @ ₹55')
    disc = c2.add('20000*5', 'Discount @ ₹5')
    rec = c2.add('1100000-160000', 'Allotment money received')
    c2.add('800000+1200000', 'Total credited to debentures = 20,000 × ₹100')
    E2 = [
        je('Jan 10', [('Bank A/c', app)], [('12% Debenture Application A/c', app)], 'Being application money received on 26,000 debentures @ ₹40'),
        je('Jan 25', [('12% Debenture Application A/c', app)], [('12% Debentures A/c', tod), ('12% Debenture Allotment A/c', exc), ('Bank A/c', ref)], 'Being application money transferred on allotment of 20,000 debentures, excess adjusted and balance refunded'),
        je('Jan 25', [('12% Debenture Allotment A/c', allot), ('Discount on Issue of Debentures A/c', disc)], [('12% Debentures A/c', 1200000)], 'Being allotment money due @ ₹55 and discount @ ₹5 on 20,000 debentures'),
        je('Feb 10', [('Bank A/c', rec)], [('12% Debenture Allotment A/c', rec)], 'Being balance allotment money received'),
    ]

    # ---------------- Illustration 3: collateral security ----------------
    c3 = Checks()
    coll = c3.add('12000*100', 'Debentures issued as collateral: 12,000 × ₹100')
    c3.add('1000000*11/100', 'Annual interest on loan ₹10,00,000 @11% (none on collateral debentures)')
    m1 = table(['Particulars', '₹'], [
        ['Long-term borrowings — Term loan from Vardhan Bank (secured by issue of 12,000 9% debentures of ₹100 each as collateral security)', inr(1000000)],
    ], title='Method 1 — no entry; disclosed with the loan')
    m2 = table(['Particulars', '₹', '₹'], [
        ['Term loan from Vardhan Bank (secured)', '', inr(1000000)],
        ['12,000 9% Debentures of ₹100 each (issued as collateral security)', inr(coll), ''],
        ['Less: Debenture Suspense Account', '(' + inr(coll) + ')', 'Nil'],
    ], title='Method 2 — Long-term borrowings note')
    E3 = [je('Apr 1', [('Debenture Suspense A/c', coll)], [('9% Debentures A/c', coll)], 'Being 12,000 debentures issued to Vardhan Bank as collateral security for a term loan of ₹10,00,000')]

    # ---------------- Illustration 4: write-off of discount ----------------
    c4 = Checks()
    d_a = c4.add('50000*3', '(a) discount: 50,000 × ₹3')
    y_a = c4.add('150000/5', '(a) yearly write-off (5 years, straight line)')
    d_b = c4.add('120000*2', '(b) discount: 1,20,000 × ₹2')
    w1 = c4.add('240000*4/10', 'Year 1 (outstanding ₹60 lakh, ratio 4/10)')
    w2 = c4.add('240000*3/10', 'Year 2 (₹45 lakh, 3/10)')
    w3 = c4.add('240000*2/10', 'Year 3 (₹30 lakh, 2/10)')
    w4 = c4.add('240000*1/10', 'Year 4 (₹15 lakh, 1/10)')
    tb_ = table(['Year', 'Debentures outstanding during the year (₹)', 'Ratio', 'Discount written off (₹)'], [
        ['1', inr(6000000), '4', inr(w1)], ['2', inr(4500000), '3', inr(w2)], ['3', inr(3000000), '2', inr(w3)], ['4', inr(1500000), '1', inr(w4)],
        ['Total', inr(15000000), '10', inr(d_b)]], num=[1, 2, 3], total=True, title='(b) Debentures redeemed in four equal yearly instalments')

    # ---------------- Illustration 5: debentures to a vendor ----------------
    c5 = Checks()
    na = c5.add('900000-100000', 'Net assets')
    gw5 = c5.add('840000-800000', 'Goodwill')
    nd = c5.add('840000/105', 'Debentures @ ₹105')
    c5.add('8000*100', 'Debentures credited at face value')
    c5.add('8000*5', 'Securities premium')
    E5 = [
        je('Oct 1', [('Sundry Assets A/c', 900000), ('Goodwill A/c', gw5)], [('Sundry Liabilities A/c', 100000), ('Ojas Enterprises (Vendor) A/c', 840000)], 'Being assets and liabilities of Ojas Enterprises taken over'),
        je('Oct 1', [('Ojas Enterprises (Vendor) A/c', 840000)], [('10% Debentures A/c', 800000), ('Securities Premium A/c', 40000)], 'Being 8,000 10% debentures of ₹100 issued at ₹105 to the vendor'),
    ]

    # ---------------- Illustration 6: interest and TDS ----------------
    c6 = Checks()
    hi = c6.add('1000000*10/100*6/12', 'Half-yearly interest on ₹10,00,000 @10%')
    tds = c6.add('50000*10/100', 'TDS @10%')
    netp = c6.add('50000-5000', 'Net paid to debenture holders')
    yr = c6.add('50000*2', 'Annual interest transferred to P&L')
    E6 = [
        je('Sep 30', [('Debenture Interest A/c', hi)], [('Debenture Holders A/c', hi)], 'Being half-yearly interest due on 10% debentures'),
        je('Sep 30', [('Debenture Holders A/c', hi)], [('TDS Payable A/c', tds), ('Bank A/c', netp)], 'Being interest paid after deducting tax at source @10%'),
        je('Oct 7', [('TDS Payable A/c', tds)], [('Bank A/c', tds)], 'Being tax deducted at source deposited with the Government'),
        je('Mar 31', [('Debenture Interest A/c', hi)], [('Debenture Holders A/c', hi)], 'Being interest due for the second half-year'),
        je('Mar 31', [('Debenture Holders A/c', hi)], [('TDS Payable A/c', tds), ('Bank A/c', netp)], 'Being interest paid after deducting TDS'),
        je('Mar 31', [('Profit and Loss A/c', yr)], [('Debenture Interest A/c', yr)], 'Being debenture interest for the year transferred to profit and loss'),
    ]

    # ---------------- Question 1 model ----------------
    q1c = Checks()
    a_cash = q1c.add('5000*94', '(i) cash @ ₹94'); a_d = q1c.add('5000*6', '(i) discount')
    b_l = q1c.add('5000*8', '(ii) loss = redemption premium ₹8')
    c_cash = q1c.add('5000*97', '(iii) cash @ ₹97'); c_l = q1c.add('5000*(3+5)', '(iii) loss = discount ₹3 + premium ₹5'); c_p = q1c.add('5000*5', '(iii) premium on redemption')
    q1c.add('5000*100', 'Face value of 5,000 debentures')
    Q1 = [
        je('(i)', [('Bank A/c', a_cash), ('Discount on Issue of Debentures A/c', a_d)], [('11% Debentures A/c', 500000)], 'Being 5,000 debentures issued at ₹94, redeemable at par'),
        je('(ii)', [('Bank A/c', 500000), ('Loss on Issue of Debentures A/c', b_l)], [('11% Debentures A/c', 500000), ('Premium on Redemption of Debentures A/c', b_l)], 'Being 5,000 debentures issued at par, redeemable at ₹108'),
        je('(iii)', [('Bank A/c', c_cash), ('Loss on Issue of Debentures A/c', c_l)], [('11% Debentures A/c', 500000), ('Premium on Redemption of Debentures A/c', c_p)], 'Being 5,000 debentures issued at ₹97, redeemable at ₹105'),
    ]

    # ---------------- Question 2 model ----------------
    q2c = Checks()
    q2d = q2c.add('100000*100*4/100', 'Discount 4% on ₹1,00,00,000')
    q2w = [q2c.add(f'400000*{k}/15', f'Year {6 - k} write-off ({k}/15)') for k in (5, 4, 3, 2, 1)]
    q2t = table(['Year ending', 'Outstanding (₹)', 'Ratio', 'Write-off (₹)'], [
        ['31 Mar 2027', inr(10000000), '5', inr(q2w[0])], ['31 Mar 2028', inr(8000000), '4', inr(q2w[1])], ['31 Mar 2029', inr(6000000), '3', inr(q2w[2])],
        ['31 Mar 2030', inr(4000000), '2', inr(q2w[3])], ['31 Mar 2031', inr(2000000), '1', inr(q2w[4])], ['Total', inr(30000000), '15', inr(q2d)]], num=[1, 2, 3], total=True)
    q2c.add('400000/5', 'If redeemed in one lot after 5 years: yearly write-off')

    viva = [
        V('v1', 'What is a debenture? State its main features.',
          'Under section 2(30), the term debenture covers debenture stock, bonds and every other instrument by which a company acknowledges a debt, whether or not it creates a charge on the company\'s assets. Its features: it is evidence of a loan to the company; it carries interest at a fixed rate on fixed dates, payable whether or not there is profit; the principal is repaid on a specified date or converted into shares; it may be secured by a charge or unsecured; and it can usually be traded on a stock exchange. Debentures cannot carry voting rights.',
          [P('p1', 'An instrument evidencing a debt / loan to the company (s. 2(30)), with or without a charge', 4, 'debt|loan|borrow|creditor|acknowledg'),
           P('p2', 'Fixed rate of interest, payable irrespective of profit', 3, 'interest', 'fixed|whether or not|irrespective|even if|regardless|even when', min=2),
           P('p3', 'Repaid on a specified date or converted; may be secured or unsecured; no voting rights', 3, 'repa|redeem|redemption|convert|secur|charge|no voting|not voting|without voting|voting')], 'c1'),
        V('v2', 'Give four differences between debentures and shares.',
          'Debenture holders are creditors of the company, while shareholders are its owners. Debenture holders have no voting rights; shareholders vote. Debenture interest is a charge against profit, payable at a fixed rate even in a loss year, while dividend is an appropriation of profit. Debentures are shown under long-term borrowings, shares under shareholders\' funds. Debentures cannot be forfeited, but shares can, and on winding up debenture holders are paid before shareholders.',
          [P('p1', 'Debenture holders are creditors; shareholders are owners', 3, 'debenture holder creditor|debentureholder creditor|debenture holder lender|debentureholder lender|debentures are loan|debenture is a loan|debenture holders lend', 'shareholder owner|shareholders are owner|shareholder is owner|shares are ownership|share is ownership|shareholders own'),
           P('p2', 'No voting rights for debenture holders', 2, 'voting|vote|no voting|not vote|not get vote|cannot vote|no vote|without voting|not have voting|without vote|not carry voting'),
           P('p3', 'Interest is a charge against profit; dividend is an appropriation', 3, 'interest', 'dividend', 'charge|appropriation|expense|deductible|even in loss|whether profit|loss', min=2),
           P('p4', 'Other: forfeiture, balance-sheet head, priority on winding up, convertibility', 2, 'forfeit|long term borrowing|borrowings|winding up|liquidation|paid first|priority|before shareholder|convert', min=1)], 'c3'),
        V('v3', 'What is meant by issue of debentures as collateral security, and how is it shown?',
          'Collateral security is a secondary or additional security given to a lender besides the main security. When a company issues its own debentures as collateral security for a loan, the lender can use them only if the loan is not repaid. Interest is payable only on the loan, not on these debentures. One method is to pass no entry and only mention the fact below the loan in the balance sheet. The other is to debit Debenture Suspense Account and credit Debentures Account, and show the suspense balance as a deduction from the debentures.',
          [P('p1', 'Secondary/additional security besides the main security; used only on default', 3, 'secondary|additional|subsidiary|supporting|extra|second', 'default|not repaid|fail|only if|cannot repay|unpaid|non payment|if the loan', min=1),
           P('p2', 'Interest only on the loan, not on the collateral debentures', 3, ALT('{n} interest {o} debentur', 'interest only {o} loan', 'interest {o} loan only', 'interest payable only {o} loan', 'interest only payable {o} loan', 'interest is paid only {o} loan', n=('no', 'not'), o=('on', 'for'))),
           P('p3', 'Method 1: no entry — note under the loan', 2, 'no entry|no journal|not record|only a note|note below|note under|mention|disclos|footnote'),
           P('p4', 'Method 2: Debenture Suspense Dr, To Debentures; suspense deducted', 2, 'suspense')], 'c7'),
        V('v4', 'Debentures are issued at a discount and are redeemable at a premium. What entry is passed at the time of issue?',
          'Bank Account is debited with the cash received, and Loss on Issue of Debentures Account is debited with the total of the discount on issue and the premium payable on redemption. Debentures Account is credited with the face value, and Premium on Redemption of Debentures Account is credited with the premium payable on redemption, which is a liability.',
          [P('p1', 'Bank debited with the amount received', 2, 'bank|cash', 'debit|received', min=2),
           P('p2', 'Loss on Issue of Debentures debited with discount + redemption premium', 4, 'loss on issue', 'discount', 'premium'),
           P('p3', 'Debentures credited at face value', 2, 'debentur', 'face value|nominal|par|credit', min=2),
           P('p4', 'Premium on Redemption of Debentures credited (a liability)', 2, 'premium on redemption|redemption premium|premium payable on redemption|premium payable')], 'c6'),
        V('v5', 'How is discount on issue of debentures written off?',
          'The discount is spread over the life of the debentures. If the debentures are redeemed in one lot at the end of a fixed period, it is written off equally every year, which is the straight line method. If they are redeemed in instalments, it is written off in the ratio of the debentures outstanding in each year, so that years using more of the borrowed money bear more of the discount. The entry is Profit and Loss Account debited and Discount on Issue of Debentures credited; the unwritten-off balance is shown as a non-current or current asset.',
          [P('p1', 'Written off over the life of the debentures', 2, 'life|period|term|tenure|over the years|years', min=1),
           P('p2', 'Lump-sum redemption: equal amounts each year (straight line)', 3, 'equal|straight line|evenly|same amount|equally|uniform', min=1),
           P('p3', 'Instalment redemption: in the ratio of debentures outstanding', 3, ALT('{i} {r}', '{r} {i}', i=('instal', 'instalment', 'instalments', 'annual drawing', 'annual drawings', 'drawings', 'every year', 'yearly', 'different dates', 'in parts'), r=('ratio', 'outstanding', 'proportion'))),
           P('p4', 'Profit and Loss Dr, To Discount on Issue of Debentures', 2, 'profit loss|profit and loss|p l|statement of profit')], 'c8'),
        V('v6', 'How is interest on debentures recorded when tax is deducted at source?',
          'When interest falls due, Debenture Interest Account is debited and Debenture Holders Account credited with the gross interest. On payment, Debenture Holders Account is debited, TDS Payable is credited with the tax deducted and Bank with the net amount. When the TDS is deposited, TDS Payable is debited and Bank credited. At the year end, interest is transferred to the Profit and Loss Account, because it is a charge against profit.',
          [P('p1', 'Interest due: Debenture Interest Dr, To Debenture Holders (gross)', 3, 'interest', 'debenture holder|debentureholder', 'debit|due|gross', min=3),
           P('p2', 'Payment: Debenture Holders Dr, To TDS Payable and To Bank (net)', 3, 'tds|tax deducted|deducted at source', 'net|bank'),
           P('p3', 'TDS deposited: TDS Payable Dr, To Bank', 2, 'deposit|remit|paid to government|pay the tds|pay tds|paid to the government|government|income tax'),
           P('p4', 'Interest transferred to Profit and Loss (charge against profit)', 2, 'profit loss|profit and loss|charge against|p l|statement of profit')], 'c9'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Shaurya Infra Ltd — a ₹50 lakh debenture issue', 'difficulty': 'hard',
        'case': ('On 1 April 2026, Shaurya Infra Ltd issued 50,000 9% debentures of ₹100 each at ₹95, redeemable at ₹104 at the end of 5 years in one lot. The issue was fully subscribed '
                 'and the money received in full on application. Interest is paid yearly on 31 March, and tax is deducted at source at 10%. The company has a securities premium '
                 'balance of ₹1,00,000 and decides to write off the loss on issue first against securities premium (as allowed by s. 52) and the rest equally over the 5 years.'),
        'mcqs': [
            M('k1a', 'What amount is debited to Loss on Issue of Debentures Account?', [R(50000 * 9), R(250000), R(200000), R(50000 * 4 + 50000 * 9)], 0,
              "Discount = 100 − 95 = ₹5; redemption premium = 104 − 100 = ₹4; total loss = ₹9 per debenture × 50,000 = ₹4,50,000. The trap ₹2,50,000 counts only the discount; ₹2,00,000 counts only the redemption premium. In practice: an infrastructure company issuing long-dated debentures records this loss upfront and writes it off over the life of the debentures.", 'moderate', '50000*(5+4)') | {'topic': "Treatment of Discount/loss on Issue of Debentures"},
            M('k1b', 'At what amount is Premium on Redemption of Debentures credited?', [R(200000), R(450000), R(250000), R(5000000)], 0,
              "Premium payable on redemption = ₹4 × 50,000 = ₹2,00,000, credited to Premium on Redemption of Debentures — a liability until redemption. The trap ₹4,50,000 is the total loss on issue, not the premium payable; ₹50,00,000 is the face value of the issue. In practice: this premium appears as a non-current liability until the year of redemption.", 'core', '50000*4') | {'topic': "Issue of Debentures"},
            M('k1c', 'How much loss is written off to the statement of profit and loss each year?', [R(70000), R(90000), R(50000), R(350000)], 0,
              "Total loss = ₹4,50,000. First, ₹1,00,000 is written off against securities premium (as section 52 allows), leaving 4,50,000 − 1,00,000 = ₹3,50,000. This is written off equally over 5 years: 3,50,000 ÷ 5 = ₹70,000 per year to the statement of profit and loss. The trap ₹90,000 spreads the whole loss over 5 years, ignoring the use of securities premium. In practice: companies often use securities premium to absorb issue losses, protecting reported profit.", 'hard', '(450000-100000)/5') | {'topic': "Treatment of Discount/loss on Issue of Debentures"},
            M('k1d', 'How much cash is paid to debenture holders as interest on 31 March 2027?', [R(405000), R(450000), R(427500), R(45000)], 0,
              "Interest is on face value: 9% × (50,000 × ₹100) = ₹4,50,000. TDS at 10% = ₹45,000. Net cash paid to debenture holders = 4,50,000 − 45,000 = ₹4,05,000. The trap ₹4,27,500 calculates interest on the issue price of ₹95. In practice: the company deposits the TDS with the government and issues TDS certificates to holders, who claim credit in their tax returns.", 'hard', '5000000*9/100*90/100') | {'topic': "Interest on Debentures"},
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch11', 'n': 3,
        'title': 'Issue of Debentures',
        'outcomes': [
            'Define a debenture under section 2(30), list its features and distinguish debentures from shares.',
            'Classify debentures by security, convertibility, permanence, negotiability and priority.',
            'Journalise issue of debentures at par, discount or premium and redeemable at par or premium, including issue by instalments and oversubscription.',
            'Account for debentures issued as collateral security (both methods) and for consideration other than cash.',
            'Write off discount or loss on issue by the straight-line and outstanding-balance methods.',
            'Record debenture interest with tax deducted at source.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 50, 'practice': 70}, 'prereq': ['fnd-p1-ch11-u02'],
                 'exam_tip': 'The six issue/redemption combinations and the discount write-off table are favourites for 5–6 mark questions; Loss on Issue of Debentures appears whenever redemption is at a premium.'},
        'concepts': [
            {'id': 'c1', 'title': 'Meaning of a debenture',
             'body': ['Companies supplement share capital by borrowing through debentures. A debenture is a written acknowledgement of debt issued by the company, setting out the terms for interest and repayment of principal.',
                      'Section 2(30): the term covers debenture stock, bonds and every other instrument by which a company acknowledges a debt, whether it creates a charge on the company\'s assets or not. So debentures may be secured or unsecured.',
                      'Where a charge is created, the bond describes the charge and the assets; a charge is valid only when registered with the Registrar. For secured (mortgage) debentures a debenture trustee is usually appointed to protect the holders. No company may issue debentures carrying voting rights (s. 71(2)).'],
             'analogy': 'A debenture is a formal IOU that a company hands to thousands of lenders at once — each piece has the same terms and can be passed on to someone else.',
             'work': 'Debt covenants, charge filings with the Registrar and trustee agreements are checked by auditors and lenders\' advisers whenever a company issues secured debentures.'},
            {'id': 'c2', 'title': 'Features of debentures',
             'body': ['It is a document evidencing a loan to the company.',
                      'Interest is at a fixed (coupon) rate on specified dates and is payable whether the company earns a profit or not.',
                      'The principal is repaid on a stated future date, or converted into shares or other debentures as per the terms.',
                      'It may be backed by a charge on the company\'s assets, or be unsecured.',
                      'It is usually transferable and can be bought or sold on a stock exchange at a price above or below face value.'],
             'analogy': 'Like a fixed deposit made with a company instead of a bank — fixed interest on fixed dates and a fixed maturity date.',
             'work': 'Treasury teams track interest dates and maturity of each debenture series; missing an interest date is a default that can trigger action under s. 71.'},
            {'id': 'c3', 'title': 'Debentures versus shares',
             'body': ['Status: debenture holders are creditors; shareholders are owners.',
                      'Voting: debenture holders cannot vote; shareholders vote and control the company.',
                      'Return: debenture interest is at a fixed rate and payable even in a loss year — a charge against profit and deductible for tax. Equity dividend varies with profits (preference dividend is fixed) and is an appropriation of profit, not deductible.',
                      'Kinds: debentures come in many kinds (secured/unsecured, redeemable/irredeemable, registered/bearer, convertible/non-convertible); shares are only equity and preference.',
                      'Presentation: debentures under long-term borrowings; shares under shareholders\' funds — share capital.',
                      'Other: debentures can be converted as per terms and cannot be forfeited; shares can be forfeited for unpaid calls. Debenture holders get their money back on maturity and are paid before shareholders on winding up; equity is repaid only on liquidation (preference shares may be redeemed earlier).'],
             'analogy': 'A shareholder is a partner in the restaurant who shares in good and bad nights; a debenture holder is the bank that lent for the kitchen and expects its EMI whatever the takings.',
             'work': 'Choosing between debt and equity funding (cost, tax shield, control, risk) is a classic advisory question CAs answer for clients.'},
            {'id': 'c4', 'title': 'Types of debentures',
             'body': ['By security: secured debentures carry a charge — fixed (on specific assets, which cannot be sold without the holders\' consent) or floating (on all assets, present and future, generally); unsecured or naked debentures carry no charge and are riskier for investors.',
                      'By convertibility: convertible (fully or partly, into equity after a period, at par, premium or discount) or non-convertible (repaid as per terms).',
                      'By permanence: redeemable (repayable as per terms, e.g. after 7 years) or irredeemable / perpetual (repaid only on liquidation).',
                      'By negotiability: registered (names recorded in the register of debenture holders; transfer needs a transfer deed as per the Act) or bearer (transferable by mere delivery; interest paid to whoever holds the coupon).',
                      'By priority: first mortgage debentures (paid first out of the charged property) and second mortgage debentures (paid after the first).'],
             'analogy': 'Secured debentures are a loan against your car (the lender can take the car); naked debentures are a personal loan (only your promise).',
             'work': 'Credit-rating agencies and investors price debentures differently by security and priority — the type decides the coupon a client must offer.'},
            {'id': 'c5', 'title': 'Issue of debentures — instalments, oversubscription and the accounts used',
             'body': ['Debentures can be paid in full with the application or in instalments (application, allotment, calls). A separate application account is kept for each class (e.g., 12% Debenture Application A/c), and on allotment its balance is transferred to the Debentures Account.',
                      'Oversubscription is handled as for shares: refund to rejected applicants; excess from pro-rata applicants adjusted towards allotment.',
                      'Debentures are always credited at face value. Premium on issue → Securities Premium. Discount on issue → Discount on Issue of Debentures (debit). Premium payable on redemption → Premium on Redemption of Debentures (credit, a liability).'],
             'analogy': 'Whatever price the debenture is sold at, the "label" on the Debentures Account is always its face value — the difference goes to a side account.',
             'work': 'In practice most debentures today are issued fully paid on application through private placement; the instalment entries still matter for exams and older issues.'},
            {'id': 'c6', 'title': 'The six issue–redemption combinations',
             'body': ['Issued at par / discount / premium and redeemable at par: Bank Dr (cash), [Discount on Issue Dr], To Debentures, [To Securities Premium].',
                      'Redeemable at a premium: the redemption premium is a known future liability, so it is recorded at issue — Loss on Issue of Debentures Dr, To Premium on Redemption of Debentures.',
                      'Issued at a discount and redeemable at a premium: Bank Dr, Loss on Issue Dr (discount + redemption premium), To Debentures, To Premium on Redemption.',
                      'Issued at a premium and redeemable at a premium: Bank Dr, Loss on Issue Dr (redemption premium), To Debentures, To Securities Premium (issue premium), To Premium on Redemption. Redemption at a discount is rare in practice.'],
             'analogy': 'If you promise to repay ₹110 for every ₹100 borrowed, the extra ₹10 is a cost you have already committed to — so it is booked on day one.',
             'work': 'Effective-interest computations for bond pricing start from exactly these components — issue price, coupon and redemption premium.'},
            {'id': 'c7', 'title': 'Debentures as collateral security',
             'body': ['Collateral security is a secondary security given in addition to the main (primary) security, which the lender can realise only if the loan is not repaid.',
                      'A company may hand its own debentures to a bank as collateral for a loan or overdraft. If the loan is repaid, the debentures come back; if not, the lender becomes a debenture holder with full rights. Interest is payable only on the loan, not on the debentures.',
                      'Method 1: no entry; a note under the loan states that it is secured by the issue of debentures as collateral. Method 2: Debenture Suspense A/c Dr, To Debentures A/c; in the balance sheet the suspense balance is deducted from the debentures. On repayment of the loan, the entry is reversed.'],
             'analogy': 'Like giving your landlord a signed but undated cheque as a back-up: it is used only if you fail to pay the rent.',
             'work': 'Auditors confirm with the bank that debentures held as collateral have not been invoked, and check the disclosure so readers are not misled into thinking there is double borrowing.'},
            {'id': 'c8', 'title': 'Debentures for consideration other than cash; treatment of discount and loss',
             'body': ['Debentures can be issued to a vendor for land, machinery or a business: Sundry Assets Dr, To Sundry Liabilities, To Vendor; then Vendor Dr, To Debentures (and To Securities Premium, or with Discount on Issue Dr). Number of debentures = purchase consideration ÷ issue price (face value, face value + premium, or face value − discount).',
                      'Discount (and loss) on issue is a capital loss, amortised over the period from issue to redemption: if redeemed in one lot after a fixed period — equally every year (straight line); if redeemed in instalments — in the ratio of debentures outstanding each year. Entry: Profit and Loss Dr, To Discount (or Loss) on Issue of Debentures.',
                      'Section 52 also permits writing off such discount or loss against securities premium. The unwritten-off balance is shown as other non-current / current assets depending on when it will be written off. (AS 16 allows discounts related to borrowings to be amortised over the loan period.)'],
             'analogy': 'If you borrow ₹100 but receive only ₹96, the ₹4 is extra interest in disguise — so it is spread over the years you use the money.',
             'work': 'Amortisation schedules for debenture discount are recomputed by auditors every year; a common error is writing off the whole discount in the year of issue.'},
            {'id': 'c9', 'title': 'Interest on debentures and TDS',
             'body': ['Interest is calculated at the coupon rate on the face (nominal) value, not on the issue price, and is a charge against profit.',
                      'The company deducts tax at source as per the Income-tax Act and pays interest net of tax. Entries: Debenture Interest Dr, To Debenture Holders (gross due); Debenture Holders Dr, To TDS Payable, To Bank (payment); TDS Payable Dr, To Bank (deposit with Government); at year end Profit and Loss Dr, To Debenture Interest.',
                      'Interest accrued and due or accrued but not due at the balance sheet date is shown under other current liabilities.'],
             'analogy': 'The company acts like an employer deducting tax from salary: it pays the lender the net amount and sends the tax to the Government.',
             'work': 'TDS compliance (deduction, deposit and quarterly returns) on debenture interest is checked in tax audits; delays attract interest and disallowance.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Journal entries for the six issue–redemption cases', 'difficulty': 'moderate', 'minutes': 15,
             'q': 'Akash Ltd issues 10,000 10% debentures of ₹100 each. Pass the entry on issue (cash received in full) when they are: (a) issued at par, redeemable at par; (b) issued at ₹95, redeemable at par; (c) issued at ₹105, redeemable at par; (d) issued at par, redeemable at ₹110; (e) issued at ₹96, redeemable at ₹105; (f) issued at ₹104, redeemable at ₹106.',
             'solution': [journal(E1, 'Journal of Akash Ltd', 'j1'),
                          wn('Rule of thumb', 'Debentures are always credited at face value (₹10,00,000). Issue premium → Securities Premium; issue discount → Discount on Issue; redemption premium → Premium on Redemption (credit) with an equal amount added to Loss on Issue (debit).')],
             'checks': c1},
            {'id': 'i2', 'title': 'Debentures payable in instalments, oversubscribed', 'difficulty': 'moderate', 'minutes': 12,
             'q': 'Kavach Ltd invited applications for 20,000 12% debentures of face value ₹100 at ₹95 (5% discount), redeemable at par: ₹40 on application and ₹55 on allotment. Applications were received for 26,000 debentures; applications for 2,000 were rejected and the rest were allotted pro rata, the excess application money being adjusted on allotment. All money due was received. Journalise.',
             'solution': [journal(E2, 'Journal of Kavach Ltd', 'j2'),
                          wn('Working', f'Pro-rata applicants applied for 24,000 and got 20,000; excess 4,000 × ₹40 = ₹{inr(exc)}. Allotment due ₹{inr(allot)} − ₹{inr(exc)} = ₹{inr(rec)} received. Debentures credited ₹8,00,000 + ₹12,00,000 = ₹20,00,000 (face value); discount ₹{inr(disc)}.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Debentures issued as collateral security', 'difficulty': 'core', 'minutes': 8,
             'q': 'Neel Ltd took a term loan of ₹10,00,000 at 11% from Vardhan Bank on 1 April 2026 and, besides a mortgage of its factory, issued 12,000 9% debentures of ₹100 each to the bank as collateral security. Show the treatment under both methods.',
             'solution': [m1, journal(E3, 'Method 2 — journal entry', 'j3'), m2,
                          note('Interest is paid only on the loan: ₹10,00,000 × 11% = ₹1,10,000 a year. No interest is paid on the collateral debentures. When the loan is repaid, the Method 2 entry is reversed.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Writing off discount — one lot vs instalments', 'difficulty': 'moderate', 'minutes': 10,
             'q': '(a) Diya Ltd issued 50,000 debentures of ₹100 at ₹97, redeemable at par after 5 years. (b) Ira Ltd issued 1,20,000 debentures of ₹50 at ₹48, one-fourth redeemable at the end of each year for 4 years. Compute the discount to be written off each year.',
             'solution': [p(f'(a) Discount = 50,000 × ₹3 = ₹{inr(d_a)}. Redeemed in one lot, so written off equally: ₹{inr(y_a)} a year for 5 years.'),
                          p(f'(b) Discount = 1,20,000 × ₹2 = ₹{inr(d_b)}. Redeemed in instalments, so written off in the ratio of debentures outstanding: 60 : 45 : 30 : 15 lakh = 4 : 3 : 2 : 1.'), tb_],
             'checks': c4},
            {'id': 'i5', 'title': 'Debentures issued to a vendor', 'difficulty': 'core', 'minutes': 8,
             'q': 'Dhruv Ltd bought the business of Ojas Enterprises on 1 October 2026: assets ₹9,00,000 and liabilities ₹1,00,000, for ₹8,40,000 payable by issuing 10% debentures of ₹100 each at a premium of 5%. Journalise.',
             'solution': [journal(E5, 'Journal of Dhruv Ltd', 'j5'),
                          wn('Working', f'Net assets ₹{inr(na)}; goodwill ₹{inr(gw5)}. Debentures = 8,40,000 ÷ 105 = {inr(nd)}.')],
             'checks': c5},
            {'id': 'i6', 'title': 'Debenture interest with TDS', 'difficulty': 'core', 'minutes': 8,
             'q': 'Mira Ltd has ₹10,00,000 10% debentures. Interest is paid half-yearly on 30 September and 31 March; TDS is 10%. TDS for September is deposited on 7 October. Journalise for 2026-27, including the year-end transfer.',
             'solution': [journal(E6, 'Journal of Mira Ltd (2026-27)', 'j6'),
                          wn('Working', f'Half-yearly interest = ₹10,00,000 × 10% × 6/12 = ₹{inr(hi)}; TDS ₹{inr(tds)}; net ₹{inr(netp)}. Charged to profit and loss for the year ₹{inr(yr)}.'),
                          note('The March TDS is deposited in April of the next year (shown as TDS payable under other current liabilities at year end). TDS rate is assumed for practice.')],
             'checks': c6},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Booking a private placement of NCDs', 'role': 'Finance executive in an unlisted manufacturing company',
             'situation': 'The company has privately placed 2,000 non-convertible debentures of ₹1,00,000 each at ₹98,500, redeemable at par after 3 years in one lot. The CFO asks for entries and the amortisation plan.',
             'steps': ['Record the issue: Bank Dr ₹19.70 crore, Discount on Issue Dr ₹30 lakh, To NCDs ₹20 crore.',
                       'Prepare a straight-line schedule: ₹10 lakh a year for 3 years (one-lot redemption).',
                       'Check whether the board wants to use securities premium (s. 52) instead of profit and loss.',
                       'Classify the unamortised discount: the part to be written off within 12 months as current, the rest non-current.',
                       'Diary the interest dates and TDS deposit dates.'],
             'takeaway': 'Every debenture issue needs an amortisation schedule from day one; the classification of the unamortised balance changes each year.',
             'checks': [{'expr': '2000*(100000-98500)', 'value': 3000000, 'label': 'Total discount'}, {'expr': '3000000/3', 'value': 1000000, 'label': 'Yearly amortisation'}]},
            {'id': 'j2', 'title': 'Spotting double-counted borrowings', 'role': 'Audit assistant',
             'situation': 'A client\'s draft balance sheet shows a bank loan of ₹50 lakh and also 9% debentures of ₹60 lakh issued to the same bank as collateral, both added into long-term borrowings, and it has provided debenture interest of ₹5.4 lakh.',
             'steps': ['Read the loan sanction letter: the debentures are collateral security only.',
                       'Explain that the company owes only the loan; showing both doubles the borrowing.',
                       'Propose presentation: either a note under the loan (Method 1) or debentures less Debenture Suspense (Method 2).',
                       'Reverse the ₹5.4 lakh interest on the debentures — interest is payable only on the loan.',
                       'Re-check debt–equity and interest cover after the correction.'],
             'takeaway': 'Collateral debentures are a contingent arrangement, not a second loan.',
             'checks': [{'expr': '6000000*9/100', 'value': 540000, 'label': 'Wrongly provided interest'}]},
        ],
        'mcqs': [
            mcq('m1', 'As per section 2(30), a debenture includes:', ['Debenture stock, bonds or any other instrument evidencing a debt, whether or not it creates a charge', 'Only secured instruments evidencing a debt', 'Equity shares with a fixed dividend', 'Only instruments listed on a stock exchange'], 0,
                "Section 2(30) of the Companies Act, 2013 gives an inclusive definition: the term covers debenture stock, bonds and any other company instrument that evidences a debt, whether or not it creates a charge on the company's assets. So both secured and unsecured instruments are covered. The trap 'only secured instruments' adds a condition the law does not contain. In practice: companies issue both secured non-convertible debentures and unsecured bonds, and both are debentures under the Act.", 'c1') | {'topic': "Meaning"},
            mcq('m2', 'Which statement about debenture holders is correct?', ['They are creditors and have no voting rights', 'They are owners and vote at general meetings', 'They receive interest only when there are profits', 'Their debentures can be forfeited for unpaid calls'], 0,
                "Debenture holders are lenders (creditors) of the company, not owners. Section 71(2) prohibits issuing debentures with voting rights, and interest is payable whether or not the company earns a profit. The trap 'interest only when there are profits' describes dividends on shares. Debentures are also not forfeited for unpaid calls. In practice: investors in listed NCDs receive fixed coupon interest regardless of the company's profit for the year.", 'c3') | {'topic': "Distinction between Debentures and Shares"},
            mcq('m3', 'Debentures that are transferable by mere delivery are:', ['Bearer debentures', 'Registered debentures', 'Mortgage debentures', 'Convertible debentures'], 0,
                "Bearer debentures are payable to whoever holds them and are transferable by mere delivery, like negotiable instruments; the company keeps no register of holders. Registered debentures need a proper transfer instrument and registration with the company — that is the trap. In practice: almost all Indian debentures today are held in demat form with depositories such as NSDL and CDSL, so bearer debentures are rare.", 'c4') | {'topic': "Types of Debentures"},
            mcq('m4', 'A charge that covers all the assets of a company, present and future, is a:', ['Floating charge', 'Fixed charge', 'Second charge', 'Collateral charge'], 0,
                "A floating charge covers a class of assets, present and future, such as stock and receivables, which the company can keep dealing with in the normal course; it 'crystallises' on default. A fixed charge attaches to specific, identified assets like a building — that is the trap. In practice: banks lending working capital to a manufacturer take a floating charge on its current assets and a fixed charge on its plant, registered with the ROC.", 'c4') | {'topic': "Types of Debentures"},
            mcq('m5', '8,000 debentures of ₹100 are issued at ₹98 and redeemable at ₹105. Loss on Issue of Debentures is:', ['₹56,000', '₹16,000', '₹40,000', '₹24,000'], 0,
                "When debentures are issued at a discount and redeemable at a premium, both are losses for the company. Discount = 100 − 98 = ₹2; redemption premium = 105 − 100 = ₹5. Loss on issue = (2 + 5) × 8,000 = ₹56,000. The trap ₹16,000 counts only the discount; ₹40,000 counts only the redemption premium. In practice: such losses are written off over the life of the debentures, often first against securities premium as section 52 allows.", 'c6', 'moderate', '8000*7') | {'topic': "Treatment of Discount/loss on Issue of Debentures"},
            mcq('m6', '6,000 debentures of ₹100 are issued at ₹103 and redeemable at ₹107. Securities Premium is credited with:', ['₹18,000', '₹42,000', '₹24,000', 'Nil'], 0,
                "Only the premium received at issue goes to Securities Premium: issue price 103 − face value 100 = ₹3 × 6,000 = ₹18,000. The redemption premium of ₹7 per share is payable later, so it is credited to Premium on Redemption of Debentures (a liability) and debited to Loss on Issue. The trap ₹42,000 credits the redemption premium to securities premium. In practice: companies show premium payable on redemption as a liability until debentures are repaid.", 'c6', 'moderate', '6000*3') | {'topic': "Issue of Debentures"},
            mcq('m7', 'Premium on Redemption of Debentures Account is shown in the balance sheet as:', ['A liability (non-current until the year of redemption)', 'Part of reserves and surplus', 'A deduction from debentures', 'Income in the statement of profit and loss'], 0,
                "Premium on Redemption of Debentures is an amount the company must pay to debenture holders when debentures are redeemed, so it is a liability. It is shown as non-current until the year of redemption, when it becomes current. The trap 'part of reserves and surplus' treats an obligation as owners' funds. In practice: auditors check that premium payable on redemption is recorded as a liability from the date of issue, not only on redemption.", 'c6') | {'topic': "Issue of Debentures"},
            mcq('m8', 'A loan of ₹8,00,000 is secured by 10,000 10% debentures of ₹100 each issued as collateral. Annual interest payable at 12% on the loan and nil on debentures equals:', ['₹96,000', '₹1,96,000', '₹1,00,000', '₹2,16,000'], 0,
                "Debentures issued as collateral security are only a back-up for the loan; the company owes the lender only the loan. Interest is therefore paid only on the loan: 8,00,000 × 12% = ₹96,000. No interest is paid on collateral debentures unless the lender enforces them. The trap ₹1,96,000 adds 10% interest on the debentures. In practice: banks sometimes take debentures as extra security for term loans, but they don't earn interest on them.", 'c7', 'moderate', '800000*12/100') | {'topic': "Issue of Debentures as Collateral Security"},
            mcq('m9', 'Under Method 2 for collateral debentures, the entry is:', ['Debenture Suspense A/c Dr, To Debentures A/c', 'Debentures A/c Dr, To Bank Loan A/c', 'Bank A/c Dr, To Debentures A/c', 'No entry is ever passed'], 0,
                "Under the second method, collateral debentures are recorded: Debenture Suspense A/c Dr, To Debentures A/c. In the balance sheet, the suspense account is deducted from debentures, so the net effect is nil while the issue is disclosed. The trap 'Bank A/c Dr, To Debentures' records cash that was never received. Under the first method, no entry is passed and a note is given. In practice: the note discloses the collateral debentures to inform readers about the extra security given.", 'c7') | {'topic': "Issue of Debentures as Collateral Security"},
            mcq('m10', 'Discount of ₹90,000 on debentures redeemable in one lot after 3 years is written off each year at:', ['₹30,000', '₹45,000', '₹90,000', '₹15,000'], 0,
                "When debentures are redeemed in one lot at the end of the term, the discount is written off equally over the life: 90,000 ÷ 3 = ₹30,000 per year. The trap ₹90,000 writes off the entire discount in year 1, which mismatches the cost with the period of borrowing. In practice: companies spread debenture discount and issue costs over the term of the debt, so each year's profit bears a fair share of the cost.", 'c8', 'core', '90000/3') | {'topic': "Treatment of Discount/loss on Issue of Debentures"},
            mcq('m11', 'Discount of ₹60,000 on debentures redeemed in three equal yearly instalments (end of each year) is written off in year 1 at:', ['₹30,000', '₹20,000', '₹10,000', '₹40,000'], 0,
                "When debentures are redeemed in equal instalments at the end of each year, the discount is written off in proportion to the amount outstanding each year: 3 : 2 : 1. Year 1 = 60,000 × 3/6 = ₹30,000. The trap ₹20,000 spreads it equally over 3 years, ignoring that more debt is outstanding in year 1. In practice: this outstanding-balance method matches the cost of borrowing with the amount actually borrowed each year.", 'c8', 'moderate', '60000*3/6') | {'topic': "Treatment of Discount/loss on Issue of Debentures"},
            mcq('m12', 'A vendor is paid ₹4,75,000 by issue of debentures of ₹100 each at a 5% discount. Number of debentures issued:', ['5,000', '4,750', '4,524', '5,250'], 0,
                "Issue price = face value 100 − 5% discount = ₹95. Number of debentures = purchase consideration ÷ issue price = 4,75,000 ÷ 95 = 5,000. The trap 4,750 divides by face value ₹100, ignoring the discount. In practice: when a company buys assets from a vendor and pays in debentures, the debentures issued at a discount carry a loss on issue to be written off.", 'c8', 'core', '475000/95') | {'topic': "Issue of Debentures in Consideration Other Than for Cash"},
            mcq('m13', 'Interest on ₹5,00,000 12% debentures issued at ₹96 for a full year is:', ['₹60,000', '₹57,600', '₹48,000', '₹62,500'], 0,
                "Interest on debentures is always calculated on the face (nominal) value, not on the issue price: 5,00,000 × 12% = ₹60,000. The trap ₹57,600 calculates interest on the issue price of ₹96 (4,80,000 × 12%). In practice: an NCD's coupon is fixed on face value, so issuing at a discount raises the effective yield to the investor.", 'c9', 'core', '500000*12/100') | {'topic': "Interest on Debentures"},
        ],
        'questions': [
            {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'journal',
             'q': 'Pass journal entries for the issue of 5,000 11% debentures of ₹100 each by Ishan Ltd (cash received in full) when they are: (i) issued at ₹94 and redeemable at par; (ii) issued at par and redeemable at ₹108; (iii) issued at ₹97 and redeemable at ₹105.',
             'model': [journal(Q1, 'Journal of Ishan Ltd', 'jq1')],
             'checks': q1c,
             'scheme': [S('s1', '(i) Bank ₹4,70,000 and Discount ₹30,000; Debentures ₹5,00,000', 2, 'posting'),
                        S('s2', '(ii) Loss on Issue ₹40,000; Premium on Redemption ₹40,000', 2, 'concept'),
                        S('s3', '(iii) Bank ₹4,85,000; Loss on Issue ₹40,000 (₹15,000 + ₹25,000); Premium on Redemption ₹25,000', 2, 'computation')],
             'remarks': ['In (ii) many candidates pass only Bank Dr, To Debentures and forget the redemption premium.', 'Debentures credited at issue price instead of face value is a costly error.'],
             'mistakes': ['Crediting Securities Premium with the redemption premium.', 'Debiting Discount on Issue with ₹8 in (ii).'],
             'tips': ['Write the face value line first, then fill the side accounts.']},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'On 1 April 2026, Rhea Ltd issued 1,00,000 debentures of face value ₹100 at 4% below par, redeemable at par by five equal annual drawings on 31 March each year starting 31 March 2027. Show the discount to be written off each year. What would the yearly write-off be if the debentures were redeemable in one lot after 5 years?',
             'model': [q2t, p('If redeemed in one lot after 5 years, the discount is written off equally: ₹4,00,000 ÷ 5 = ₹80,000 a year.')],
             'checks': q2c,
             'scheme': [S('s1', 'Total discount ₹4,00,000', 1, 'computation'), S('s2', 'Outstanding amounts and ratio 5:4:3:2:1', 1.5, 'computation'),
                        S('s3', 'Yearly write-offs ₹1,33,333 … ₹26,667 (total ₹4,00,000)', 1.5, 'computation'), S('s4', 'One-lot alternative ₹80,000', 1, 'concept')],
             'remarks': ['Many divide the discount equally even though redemption is by instalments.'],
             'mistakes': ['Using the debentures redeemed (not outstanding) as the ratio.', 'Rounding so that the total does not equal the discount.'],
             'tips': ['Show the outstanding amount for each year in a table and add a total row.']},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
             'q': 'Distinguish between debentures and shares (any four points).',
             'model': [table(['Basis', 'Debentures', 'Shares'], [
                 ['Status of holder', 'Creditor (lender)', 'Owner'], ['Voting rights', 'None (s. 71(2))', 'Equity shares carry voting rights'],
                 ['Return', 'Fixed interest, payable even in a loss year — charge against profit, tax-deductible', 'Dividend — appropriation of profit; equity rate varies'],
                 ['Balance sheet', 'Long-term borrowings', 'Shareholders\' funds — share capital'],
                 ['Forfeiture', 'Cannot be forfeited', 'Can be forfeited for unpaid calls'],
                 ['Repayment / winding up', 'Repaid on maturity; paid before shareholders on winding up', 'Equity repaid only on winding up, after creditors']])],
             'scheme': [S('s1', 'Point 1', 1, 'concept'), S('s2', 'Point 2', 1, 'concept'), S('s3', 'Point 3', 1, 'concept'), S('s4', 'Point 4', 1, 'concept')],
             'remarks': ['Points must contrast both sides; one-sided statements get half marks.'],
             'mistakes': ['Saying debenture interest is an appropriation of profit.'],
             'tips': ['Three-column table with clear bases.']},
            {'id': 'q4', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'journal',
             'q': 'Arya Ltd obtained a loan of ₹6,00,000 from a bank and issued 7,000 10% debentures of ₹100 each as collateral security. Explain the meaning of collateral security and show how the debentures will appear in the balance sheet under both methods. Is any interest payable on these debentures?',
             'model': [p('Collateral security is an additional (secondary) security given to a lender besides the primary security; it is used only if the borrower defaults.'),
                       p('Method 1: No entry. Under Long-term borrowings: "Bank loan ₹6,00,000 (secured by issue of 7,000 10% debentures of ₹100 each as collateral security)".'),
                       journal([je('—', [('Debenture Suspense A/c', 700000)], [('10% Debentures A/c', 700000)], 'Being 7,000 debentures issued as collateral security for the bank loan')], 'Method 2 entry', 'jq4'),
                       p('Method 2 presentation under Long-term borrowings: Bank loan ₹6,00,000; 10% Debentures ₹7,00,000 less Debenture Suspense ₹7,00,000 = Nil.'),
                       p('No interest is payable on the collateral debentures; interest is paid only on the loan of ₹6,00,000.')],
             'checks': [{'expr': '7000*100', 'value': 700000, 'label': 'Collateral debentures at face value'}],
             'scheme': [S('s1', 'Meaning of collateral security', 1, 'concept'), S('s2', 'Method 1 disclosure', 1, 'presentation'),
                        S('s3', 'Method 2 journal entry', 1, 'posting'), S('s4', 'Method 2 balance sheet presentation', 1, 'presentation'), S('s5', 'No interest on collateral debentures', 1, 'concept')],
             'remarks': ['Many candidates add ₹7,00,000 to borrowings — the company has borrowed only ₹6,00,000.'],
             'mistakes': ['Providing interest on the collateral debentures.', 'Showing Debenture Suspense as an asset.'],
             'tips': ['Answer both methods side by side and end with the interest point.']},
        ],
        'viva': viva,
        'cases': cases,
        'revision': {
            'summary': ['Debenture (s. 2(30)): instrument evidencing a debt, secured or not; no voting rights (s. 71(2)).',
                        'Features: fixed interest regardless of profit, repayment/conversion on a date, may carry a charge, tradable.',
                        'Types: secured (fixed/floating) or naked; convertible or not; redeemable or perpetual; registered or bearer; first or second mortgage.',
                        'Debentures always credited at face value; issue premium → Securities Premium; discount → Discount on Issue; redemption premium → Premium on Redemption (liability) with Loss on Issue (debit).',
                        'Collateral: no entry (note) or Debenture Suspense Dr / Debentures Cr; interest only on the loan.',
                        'Discount/loss written off: equally (one-lot) or in outstanding ratio (instalments); may be set off against securities premium (s. 52).',
                        'Interest on face value; TDS deducted; transferred to P&L as a charge.'],
            'remember': ['Loss on Issue = discount on issue + premium on redemption.', 'Interest is on face value, not issue price.', 'Collateral debentures do not increase borrowings.'],
            'traps': ['Crediting debentures at issue price.', 'Writing off the whole discount in year 1.', 'Paying interest on collateral debentures.', 'Calling debenture interest an appropriation of profit.'],
        },
        'quickref': [
            {'k': 'Definition', 'v': 's. 2(30) — debenture stock, bonds or any instrument evidencing a debt, charge or no charge'},
            {'k': 'Voting', 'v': 's. 71(2) — debentures cannot carry voting rights'},
            {'k': 'Issue at discount, redeem at premium', 'v': 'Bank Dr + Loss on Issue Dr (disc + prem) To Debentures To Premium on Redemption'},
            {'k': 'Issue at premium, redeem at premium', 'v': 'Bank Dr + Loss on Issue Dr (red. prem) To Debentures To Securities Premium To Premium on Redemption'},
            {'k': 'Collateral (Method 2)', 'v': 'Debenture Suspense A/c Dr To Debentures A/c; shown as deduction'},
            {'k': 'Debentures to vendor', 'v': 'Number = purchase consideration ÷ issue price'},
            {'k': 'Discount write-off', 'v': 'One lot → equal yearly; instalments → ratio of debentures outstanding'},
            {'k': 'Interest with TDS', 'v': 'Interest Dr To Debenture holders; Debenture holders Dr To TDS Payable, To Bank; TDS Payable Dr To Bank; P&L Dr To Interest'},
        ],
    }


# ---- offline auto-check: kw/min (viva matcher), nums (figures that must appear), rows ([account, side, amount]) ----
# "any N" question: every point carries the same groups with min = 1 … N (N distinct correct points earn N marks).
_DIFF = ['creditor|lender|borrowed|loan capital|borrowed capital', 'voting|vote', 'interest|dividend|fixed return', 'borrowing|share capital|shareholders funds|liabilit|owned capital',
         'forfeit', 'repaid|repayment|redeem|redemption|winding up|maturity', 'secured|charge on assets|security|mortgage', 'convert']
AUTO = {
    'q1': {'extra_ok': False,
           's1': {'rows': [['bank', 'dr', 470000], ['discount', 'dr', 30000], ['debenture', 'cr', 500000]]},
           's2': {'rows': [['loss', 'dr', 40000], ['premium', 'cr', 40000]],
                  'wrong': [{'kw': ['discount on issue 40000'], 'say': 'Debentures issued at par give no discount; the ₹40,000 premium payable on redemption is a loss on issue (Loss on Issue of Debentures A/c).'}]},
           's3': {'rows': [['bank', 'dr', 485000], ['loss|discount', 'dr', 40000], ['premium', 'cr', 25000]]}},
    'q2': {'extra_ok': False,
           's1': {'nums': [400000]},
           's2': {'kw': ['5 4 3|4 3 2|3 2 1|8000000']},
           's3': {'nums': [133333, 106667, 53333, 26667]},
           's4': {'kw': ['equal|equally|400000 5|straight line|one lot 80000|lot 80000|80000 each year|80000 per year|80000 every year'], 'nums': [80000]}},
    'q3': dict({'extra_ok': True}, **{f's{n}': {'kw': _DIFF, 'min': n} for n in range(1, 5)}),
    'q4': {'extra_ok': False,
           's1': {'kw': ['additional security|secondary security|subsidiary security|extra security|security in addition|besides primary|addition to primary|over and above|supplementary security|further security',
                         'default|fails|failure|not repaid|unable|not paid|non payment|non-payment'], 'min': 2},
           's2': {'kw': ['no entry|not recorded|no journal|without entry|disclos|by way of note|note|not passed'], 'nums': [600000]},
           's3': {'rows': [['suspense', 'dr', 700000], ['debenture', 'cr', 700000]]},
           's4': {'kw': ['less|deduct|minus|nil', 'suspense'], 'min': 2, 'nums': [700000]},
           's5': {'kw': ['no interest|not payable|interest not|interest is not|interest only on loan|not entitled interest|nil interest|no interest payable|interest only paid loan'],
                  'wrong': [{'kw': ['70000'], 'say': 'No interest is paid on debentures issued as collateral security; interest is paid only on the loan.'}]}},
}


def _attach_auto(u):
    """Merge AUTO into the questions: every scheme point gets its auto-check fields; every question gets extra_ok."""
    for q in u.get('questions', []):
        a = AUTO[q['id']]
        q['extra_ok'] = a.get('extra_ok', False)
        for s in q['scheme']: s.update(a[s['id']])
        extra = set(a) - {'extra_ok'} - {s['id'] for s in q['scheme']}
        assert not extra, f"AUTO[{q['id']}] has unknown scheme ids {extra}"
    return u


_build_core = build


def build(): return _attach_auto(_build_core())
