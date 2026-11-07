"""CA Foundation · Paper 1 Accounting · Chapter 11 Company Accounts · Unit 2 Issue, Forfeiture and Re-Issue of Shares.
Original explanations, names and numbers (structure and scope follow the ICAI study material)."""
from lib import *
from ca_viva import P, ALT, V
from ca_cases import M

UID = 'fnd-p1-ch11-u02'


def mcq(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check: d['check'] = check
    return d


def S(sid, pt, m, skill): return {'id': sid, 'pt': pt, 'm': m, 'skill': skill}


def build():
    # ---------------- Illustration 1: full subscription at a premium ----------------
    c1 = Checks()
    a1 = c1.add('40000*3', 'Application money: 40,000 × ₹3')
    al1 = c1.add('40000*5', 'Allotment due: 40,000 × ₹5 (₹3 capital + ₹2 premium)')
    al1c = c1.add('40000*3', 'Allotment — capital part')
    al1p = c1.add('40000*2', 'Allotment — premium part')
    cl1 = c1.add('40000*4', 'First and final call: 40,000 × ₹4')
    c1.add('120000+120000+160000', 'Share capital = ₹10 × 40,000')
    c1.add('120000+200000+160000', 'Total cash received = ₹12 × 40,000')
    E1 = [
        je('Apr 10', [('Bank A/c', a1)], [('Equity Share Application A/c', a1)], 'Being application money received on 40,000 shares @ ₹3'),
        je('Apr 25', [('Equity Share Application A/c', a1)], [('Equity Share Capital A/c', a1)], 'Being application money on 40,000 shares transferred to share capital on allotment'),
        je('Apr 25', [('Equity Share Allotment A/c', al1)], [('Equity Share Capital A/c', al1c), ('Securities Premium A/c', al1p)], 'Being allotment money due @ ₹5 per share including premium of ₹2'),
        je('May 15', [('Bank A/c', al1)], [('Equity Share Allotment A/c', al1)], 'Being allotment money received'),
        je('Aug 1', [('Equity Share First and Final Call A/c', cl1)], [('Equity Share Capital A/c', cl1)], 'Being first and final call made @ ₹4 per share'),
        je('Aug 20', [('Bank A/c', cl1)], [('Equity Share First and Final Call A/c', cl1)], 'Being call money received'),
    ]

    # ---------------- Illustration 2: pro-rata, default, forfeiture, re-issue ----------------
    c2 = Checks()
    app = c2.add('70000*3', 'Application money received on 70,000 shares @ ₹3')
    rej = c2.add('10000*3', 'Refund to applicants for 10,000 shares')
    tocap = c2.add('50000*3', 'Application money transferred to capital on 50,000 shares')
    excess = c2.add('10000*3', 'Excess application money on pro-rata applicants (60,000 − 50,000 shares) × ₹3')
    allot = c2.add('50000*5', 'Allotment due: 50,000 × ₹5')
    allot_cap = c2.add('50000*3', 'Allotment — capital part @ ₹3')
    allot_prem = c2.add('50000*2', 'Allotment — premium part @ ₹2')
    aj_paid = c2.add('1200*3', 'Ajay paid on application (1,200 × ₹3)')
    aj_excess = c2.add('3600-1000*3', 'Ajay excess application money adjusted on allotment')
    aj_unpaid = c2.add('1000*5-600', 'Ajay allotment unpaid')
    allot_recd = c2.add('250000-30000-4400', 'Allotment money received in cash')
    call = c2.add('50000*4', 'First and final call due')
    call_recd = c2.add('49000*4', 'Call received (49,000 shares)')
    call_unpaid = c2.add('1000*4', 'Call unpaid by Ajay')
    forf = c2.add('1000*10+1000*2-4400-4000', 'Forfeited shares credit = capital 10,000 + premium 2,000 − amounts unpaid')
    re_bank = c2.add('600*8', 'Re-issue proceeds: 600 × ₹8')
    re_loss = c2.add('600*(10-8)', 'Discount on re-issue debited to Forfeited Shares')
    forf600 = c2.add('3600*600/1000', 'Forfeited amount on the 600 shares re-issued')
    cr = c2.add('2160-1200', 'Transfer to capital reserve')
    forf_left = c2.add('3600-2160', 'Forfeited shares balance on 400 shares not re-issued')
    paidcap = c2.add('49600*10', 'Paid-up capital: 49,600 fully paid shares')
    sp = c2.add('100000-2000', 'Securities premium after cancelling Ajay\'s unpaid premium')
    bank = c2.add('210000-30000+215600+196000+4800', 'Bank balance')
    c2.add('496000+1440+98000+960', 'Shareholders\' funds = bank balance')
    E2 = [
        je('Jun 5', [('Bank A/c', app)], [('Equity Share Application A/c', app)], 'Being application money received on 70,000 shares @ ₹3'),
        je('Jun 20', [('Equity Share Application A/c', rej)], [('Bank A/c', rej)], 'Being application money refunded on 10,000 shares rejected'),
        je('Jun 20', [('Equity Share Application A/c', tocap)], [('Equity Share Capital A/c', tocap)], 'Being application money on 50,000 shares allotted transferred to capital'),
        je('Jun 20', [('Equity Share Application A/c', excess)], [('Equity Share Allotment A/c', excess)], 'Being excess application money on pro-rata allotment adjusted towards allotment'),
        je('Jun 20', [('Equity Share Allotment A/c', allot)], [('Equity Share Capital A/c', allot_cap), ('Securities Premium A/c', allot_prem)], 'Being allotment money due @ ₹5 per share including ₹2 premium'),
        je('Jul 5', [('Bank A/c', allot_recd)], [('Equity Share Allotment A/c', allot_recd)], 'Being allotment money received except from Ajay on 1,000 shares'),
        je('Oct 1', [('Equity Share First and Final Call A/c', call)], [('Equity Share Capital A/c', call)], 'Being first and final call made @ ₹4 per share'),
        je('Oct 20', [('Bank A/c', call_recd)], [('Equity Share First and Final Call A/c', call_recd)], 'Being call money received on 49,000 shares'),
        je('Dec 1', [('Equity Share Capital A/c', 10000), ('Securities Premium A/c', 2000)], [('Equity Share Allotment A/c', aj_unpaid), ('Equity Share First and Final Call A/c', call_unpaid), ('Forfeited Shares A/c', forf)], 'Being 1,000 shares of Ajay forfeited for non-payment of allotment and call money'),
        je('Dec 20', [('Bank A/c', re_bank), ('Forfeited Shares A/c', re_loss)], [('Equity Share Capital A/c', 6000)], 'Being 600 forfeited shares re-issued as fully paid @ ₹8 per share'),
        je('Dec 20', [('Forfeited Shares A/c', cr)], [('Capital Reserve A/c', cr)], 'Being gain on re-issue of 600 forfeited shares transferred to capital reserve'),
    ]
    note2 = table(['Particulars', '₹'], [
        ['Share capital — Issued: 50,000 equity shares of ₹10 each', inr(500000)],
        ['Subscribed and fully paid: 49,600 equity shares of ₹10 each', inr(paidcap)],
        ['Add: Forfeited shares account (400 shares)', inr(forf_left)],
        ['Total share capital', inr(paidcap + forf_left)],
    ], num=[1], total=False, title='Note — Share capital')
    rs2 = table(['Reserves and surplus', '₹'], [
        ['Securities premium (1,00,000 − 2,000)', inr(sp)], ['Capital reserve (gain on re-issue)', inr(cr)], ['Total', inr(sp + cr)]], num=[1], total=True)

    # ---------------- Illustration 3: interest on calls ----------------
    c3 = Checks()
    arr = c3.add('2000*3', 'First call unpaid: 2,000 shares × ₹3')
    i_arr = c3.add('6000*10/100*6/12', 'Interest on calls in arrears @10% for 6 months')
    adv = c3.add('1500*4', 'Final call received in advance: 1,500 × ₹4')
    i_adv = c3.add('6000*12/100*6/12', 'Interest on calls in advance @12% for 6 months')
    fc = c3.add('30000*4', 'Final call due on all 30,000 shares')
    c3.add('120000-6000', 'Cash received on final call date')
    E3 = [
        je('Aug 1', [('Equity Share First Call A/c', 90000)], [('Equity Share Capital A/c', 90000)], 'Being first call made @ ₹3 per share on 30,000 shares'),
        je('Aug 1', [('Bank A/c', 84000), ('Calls in Arrears A/c', arr)], [('Equity Share First Call A/c', 90000)], 'Being first call @ ₹3 received on 28,000 shares; 2,000 shares in arrears'),
        je('Sep 1', [('Bank A/c', adv)], [('Calls in Advance A/c', adv)], 'Being final call received in advance on 1,500 shares'),
        je('Jan 31', [('Bank A/c', arr + i_arr)], [('Calls in Arrears A/c', arr), ('Interest on Calls in Arrears A/c', i_arr)], 'Being arrears received with interest @10% p.a. for 6 months'),
        je('Mar 1', [('Equity Share Final Call A/c', fc)], [('Equity Share Capital A/c', fc)], 'Being final call made @ ₹4 on 30,000 shares'),
        je('Mar 1', [('Bank A/c', fc - adv), ('Calls in Advance A/c', adv)], [('Equity Share Final Call A/c', fc)], 'Being final call received and calls in advance adjusted'),
        je('Mar 1', [('Interest on Calls in Advance A/c', i_adv)], [('Bank A/c', i_adv)], 'Being interest @12% p.a. for 6 months paid on calls in advance'),
    ]
    c3.add('30000*3', 'First call due on 30,000 shares')
    c3.add('28000*3', 'First call received on 28,000 shares')

    # ---------------- Illustration 4: consideration other than cash ----------------
    c4 = Checks()
    net = c4.add('800000-150000', 'Net assets taken over')
    gw = c4.add('715000-650000', 'Goodwill = purchase consideration − net assets')
    bal = c4.add('715000-55000', 'Consideration settled in shares')
    nsh = c4.add('660000/11', 'Number of shares @ ₹11')
    c4.add('60000*10', 'Share capital credited')
    c4.add('60000*1', 'Securities premium credited')
    E4 = [
        je('Jul 1', [('Sundry Assets A/c', 800000), ('Goodwill A/c', gw)], [('Sundry Liabilities A/c', 150000), ('Sharma Brothers (Vendor) A/c', 715000)], 'Being business of Sharma Brothers taken over for ₹7,15,000'),
        je('Jul 1', [('Sharma Brothers (Vendor) A/c', 55000)], [('Bank A/c', 55000)], 'Being part of purchase consideration paid by cheque'),
        je('Jul 1', [('Sharma Brothers (Vendor) A/c', bal)], [('Equity Share Capital A/c', 600000), ('Securities Premium A/c', 60000)], 'Being 60,000 equity shares of ₹10 each issued at ₹11 to the vendor'),
    ]

    # ---------------- Question 1 model ----------------
    q1c = Checks()
    q1_app = q1c.add('160000*2', 'Application money on 1,60,000 shares')
    q1_rej = q1c.add('20000*2', 'Refund on 20,000 shares')
    q1_cap = q1c.add('100000*2', 'Application to capital')
    q1_exc = q1c.add('40000*2', 'Excess on pro-rata applicants')
    q1_allot = q1c.add('100000*3', 'Allotment due')
    q1_sn_exc = q1c.add('2800*2-2000*2', 'Sneha excess application money')
    q1_sn_un = q1c.add('2000*3-1600', 'Sneha allotment unpaid')
    q1_allot_r = q1c.add('300000-80000-4400', 'Allotment received')
    q1_call = q1c.add('100000*3', 'First call due')
    q1_call_r = q1c.add('98000*3', 'First call received')
    q1_forf = q1c.add('2000*8-4400-6000', 'Forfeited shares credit (= amount Sneha paid)')
    q1_re = q1c.add('1500*7', 'Re-issue proceeds')
    q1_f15 = q1c.add('5600*1500/2000', 'Forfeited amount on 1,500 shares')
    q1_cr = q1c.add('4200-1500', 'Capital reserve')
    q1c.add('5600-4200', 'Forfeited shares balance on 500 shares')
    Q1 = [
        je('(i)', [('Bank A/c', q1_app)], [('Equity Share Application A/c', q1_app)], 'Being application money received on 1,60,000 shares @ ₹2'),
        je('(ii)', [('Equity Share Application A/c', q1_app)], [('Equity Share Capital A/c', q1_cap), ('Equity Share Allotment A/c', q1_exc), ('Bank A/c', q1_rej)], 'Being application money transferred to capital, excess adjusted to allotment and refund on rejected applications'),
        je('(iii)', [('Equity Share Allotment A/c', q1_allot)], [('Equity Share Capital A/c', q1_allot)], 'Being allotment money due @ ₹3 per share'),
        je('(iv)', [('Bank A/c', q1_allot_r)], [('Equity Share Allotment A/c', q1_allot_r)], 'Being allotment money received except from Sneha'),
        je('(v)', [('Equity Share First Call A/c', q1_call)], [('Equity Share Capital A/c', q1_call)], 'Being first call made @ ₹3 per share'),
        je('(vi)', [('Bank A/c', q1_call_r)], [('Equity Share First Call A/c', q1_call_r)], 'Being first call received on 98,000 shares'),
        je('(vii)', [('Equity Share Capital A/c', 16000)], [('Equity Share Allotment A/c', q1_sn_un), ('Equity Share First Call A/c', 6000), ('Forfeited Shares A/c', q1_forf)], 'Being 2,000 shares of Sneha (₹8 called up) forfeited'),
        je('(viii)', [('Bank A/c', q1_re), ('Forfeited Shares A/c', 1500)], [('Equity Share Capital A/c', 12000)], 'Being 1,500 forfeited shares re-issued as ₹8 paid up for ₹7 per share'),
        je('(ix)', [('Forfeited Shares A/c', q1_cr)], [('Capital Reserve A/c', q1_cr)], 'Being gain on re-issue of 1,500 shares transferred to capital reserve'),
    ]

    # ---------------- Question 2 model: premium already received ----------------
    q2c = Checks()
    q2_cap = q2c.add('800*10', 'Called-up capital on 800 shares (fully called)')
    q2_unp = q2c.add('800*3', 'Final call unpaid')
    q2_forf = q2c.add('8000-2400', 'Forfeited shares credit = capital paid (premium already received stays)')
    q2_re = q2c.add('500*9', 'Re-issue of 500 shares @ ₹9')
    q2_disc = q2c.add('500*1', 'Discount on re-issue')
    q2_f500 = q2c.add('5600*500/800', 'Forfeited amount on 500 shares')
    q2_cr = q2c.add('3500-500', 'Capital reserve')
    q2_left = q2c.add('5600-3500', 'Balance on 300 shares')
    Q2 = [
        je('(i)', [('Equity Share Capital A/c', q2_cap)], [('Equity Share Final Call A/c', q2_unp), ('Forfeited Shares A/c', q2_forf)], 'Being 800 shares forfeited for non-payment of final call of ₹3'),
        je('(ii)', [('Bank A/c', q2_re), ('Forfeited Shares A/c', q2_disc)], [('Equity Share Capital A/c', 5000)], 'Being 500 forfeited shares re-issued @ ₹9 as fully paid'),
        je('(iii)', [('Forfeited Shares A/c', q2_cr)], [('Capital Reserve A/c', q2_cr)], 'Being gain on re-issue of 500 shares transferred to capital reserve'),
    ]

    viva = [
        V('v1', 'Explain the different categories of share capital that appear in a company\'s share capital note.',
          'Authorised capital is the maximum capital the company may raise, as stated in the capital clause of its memorandum. Issued capital is the part actually offered, for cash or otherwise. Subscribed capital is the part taken up by investors and allotted. Called-up capital is the part of the issue price demanded so far, and paid-up capital is the called-up capital actually received, that is called-up less calls in arrears. Reserve capital is uncalled capital that by special resolution will be called only on winding up.',
          [P('p1', 'Authorised — maximum capital as per the memorandum', 2, 'authoris|authoriz|nominal', 'maximum|memorandum|limit|upper|ceiling', min=2),
           P('p2', 'Issued and subscribed — offered, and taken up/allotted', 2, 'issued', 'subscribed'),
           P('p3', 'Called-up — portion demanded so far', 2, 'called up|called-up|call up', 'demand|asked|called so far|portion|part', min=2),
           P('p4', 'Paid-up — called-up less calls in arrears', 2, 'paid up|paid-up', 'arrear|unpaid|actually received|actually paid|received|less', min=2),
           P('p5', 'Reserve capital — uncalled, callable only on winding up', 2, 'reserve capital', 'winding up|wound up|liquidation|winding-up', min=2)], 'c1'),
        V('v2', 'For what purposes can a company use its securities premium account under section 52?',
          'Under section 52, securities premium can be used to issue fully paid bonus shares to members, to write off preliminary expenses, to write off expenses, commission or discount on issue of any securities or debentures, to provide for the premium payable on redemption of preference shares or debentures, and to buy back its own shares or other securities. Companies that follow the prescribed accounting standards cannot use it for preliminary expenses or redemption premium.',
          [P('p1', 'Issue of fully paid bonus shares', 3, 'bonus'),
           P('p2', 'Write off preliminary expenses', 2, 'preliminary'),
           P('p3', 'Write off expenses, commission or discount on issue of securities/debentures', 2, 'commission|discount|issue expense|expenses of issue|expenses on issue'),
           P('p4', 'Premium on redemption of preference shares or debentures', 2, 'redemption|redeem|redeemable'),
           P('p5', 'Buy-back of its own shares or securities', 1, 'buy back|buyback|buy-back|purchase of its own|purchase own|own shares|buying back')], 'c5'),
        V('v3', 'Can a company issue shares at a discount today? Explain.',
          'Generally no. Section 53 prohibits a company from issuing shares at a discount, and any such issue is void. The exceptions allowed by law are sweat equity shares under section 54, and shares issued at a discount to creditors when debt is converted into shares as part of a statutory resolution plan or debt restructuring scheme, permitted by section 53(2A).',
          [P('p1', 'No — section 53 prohibits issue at a discount', 5, 'prohibit|prohibition|cannot issue|can not issue|cannot be issued|can t issue|not allowed|not permitted|banned|void|barred|generally no|generally not|no generally|illegal|forbidden|ban|bans|disallow|not possible'),
           P('p2', 'Exception: sweat equity shares (section 54)', 3, 'sweat'),
           P('p3', 'Exception: conversion of debt under a resolution plan / restructuring (s. 53(2A))', 2, 'conver|resolution plan|restructur|creditor|debt', min=1)], 'c4'),
        V('v4', 'Distinguish calls in arrears from calls in advance, including the interest rates under Table F.',
          'Calls in arrears is money called by the company but not paid by the shareholder; it is deducted from called-up capital, and interest on calls in arrears, up to ten per cent per annum, may be charged by the company from the due date until payment. Calls in advance is money received before it has been called; it is a liability, not share capital, and interest on calls in advance, up to twelve per cent per annum, is paid by the company from receipt until the call is due. No dividend is paid on calls in advance.',
          [P('p1', 'Calls in arrears: called but not paid (deducted from called-up capital)', 3, 'arrear', 'not paid|unpaid|not received|fail|default|did not pay|didn t pay|outstanding', min=2),
           P('p2', 'Calls in arrears: interest up to 10% p.a. charged by the company', 2, ALT('{a} {n}', '{a} interest {n}', '{n} per cent per annum {a}', '{n} percent per annum {a}', '{n} annum {a}', '{a} up to {n}', a=('arrear', 'arrears'), n=('10', 'ten'))),
           P('p3', 'Calls in advance: received before being called (a liability)', 3, 'advance', 'before|not yet called|not called|ahead|early|prior', min=2),
           P('p4', 'Calls in advance: interest up to 12% p.a. paid by the company', 2, ALT('{a} {n}', '{a} interest {n}', '{n} per cent per annum {a}', '{n} percent per annum {a}', '{n} annum {a}', '{a} up to {n}', a=('advance', 'advances'), n=('12', 'twelve')))], 'c7'),
        V('v5', 'What journal entry is passed when shares issued at a premium are forfeited and the premium has not been received?',
          'Share Capital Account is debited with the called-up amount on the forfeited shares, and Securities Premium Account is debited with the premium that was not received. Share Allotment and Call accounts, or Calls in Arrears, are credited with the amounts unpaid, and Forfeited Shares Account is credited with the amount actually received from the shareholder. If the premium had already been received, it is not cancelled.',
          [P('p1', 'Share Capital debited with the called-up amount', 3, 'share capital', 'called up|called-up|called|debit', min=2),
           P('p2', 'Securities Premium debited with unpaid premium', 3, 'premium debit|debit securities premium|debit premium|securities premium account debit|securities premium debit|premium account debit|premium is debit|cancel premium|premium cancel|reverse premium|premium revers'),
           P('p3', 'Allotment/Calls (or Calls in Arrears) credited with amounts unpaid', 2, 'allotment|call|arrear', 'unpaid|not paid|due|credit', min=2),
           P('p4', 'Forfeited Shares credited with the amount received', 2, 'forfeit', 'received|paid|collected|already|credit', min=2)], 'c8'),
        V('v6', 'What are the rules for re-issue of forfeited shares, and how is the gain treated?',
          'Forfeited shares may be re-issued at any price, provided the total received from the original holder and the new holder is not less than the paid-up value credited. So the discount on re-issue cannot exceed the amount forfeited on those shares; it is debited to Forfeited Shares Account. Any balance left on the shares re-issued is a capital gain and is transferred to Capital Reserve. The balance on shares not yet re-issued stays in Forfeited Shares Account and is added to share capital in the balance sheet. If re-issued above face value, the excess goes to securities premium.',
          [P('p1', 'Discount on re-issue cannot exceed the amount forfeited', 4, 'discount|loss', 'not exceed|cannot exceed|can t exceed|never exceed|limited to|up to|not more than|no more than|maximum|within|restricted to|capped', 'forfeit', min=3),
           P('p2', 'Discount debited to Forfeited Shares Account', 2, 'forfeited share', 'debit'),
           P('p3', 'Remaining gain on re-issued shares → Capital Reserve', 4, 'capital reserve')], 'c9'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Prism Foods Ltd — an oversubscribed issue', 'difficulty': 'hard',
        'case': ('Prism Foods Ltd offered 80,000 equity shares of face value ₹10 at ₹15 (premium ₹5), payable ₹4 on application, ₹6 on allotment (including the premium of ₹5) and ₹5 on '
                 'first and final call. Applications were received for 1,20,000 shares. Applications for 20,000 shares were rejected and money refunded; the remaining applicants '
                 'were allotted shares pro rata. Excess application money was adjusted against allotment. Neha, who had applied for 1,500 shares, paid nothing after application. '
                 'Her shares were forfeited after the call, and later all of them were re-issued at ₹8 per share as fully paid.'),
        'mcqs': [
            M('k1a', 'In what ratio were shares allotted to the applicants who were not rejected?', ['5 : 4 (applied : allotted)', '3 : 2 (applied : allotted)', '6 : 5 (applied : allotted)', '1 : 1'], 0,
              '1,20,000 − 20,000 = 1,00,000 shares applied for by those allotted; 80,000 allotted. Ratio 1,00,000 : 80,000 = 5 : 4.', 'moderate'),
            M('k1b', 'How many shares were allotted to Neha, and how much of her application money was carried to allotment?', ['1,200 shares; ₹1,200', '1,500 shares; nil', '1,200 shares; ₹1,500', '1,000 shares; ₹2,000'], 0,
              'Neha gets 1,500 × 4/5 = 1,200 shares. She paid 1,500 × ₹4 = ₹6,000; required 1,200 × ₹4 = ₹4,800; excess ₹1,200 went to allotment.', 'hard'),
            M('k1c', 'What amount is credited to Forfeited Shares Account when Neha\'s shares are forfeited?', [R(6000), R(4800), R(12000), R(18000)], 0,
              'Forfeited Shares is credited with the money actually received on those shares — her application money ₹6,000 (₹4,800 on application plus ₹1,200 adjusted against allotment, both counting towards capital).', 'hard', '1500*4'),
            M('k1d', 'What amount will be transferred to Capital Reserve after the re-issue?', [R(3600), R(6000), R(2400), R(8400)], 0,
              'Re-issue at ₹8 on 1,200 shares: discount ₹2 × 1,200 = ₹2,400 debited to Forfeited Shares. Gain = 6,000 − 2,400 = ₹3,600.', 'hard', '6000-1200*2'),
            M('k1e', 'While forfeiting Neha\'s shares, Securities Premium Account is debited by:', [R(6000), R(1200), R(7500), 'Nil, because the premium has been received'], 0,
              'Premium of ₹5 on 1,200 shares was due with allotment, and she paid nothing on allotment beyond the adjusted ₹1,200 (which counts first against the capital part per the usual exam assumption). So the premium is unpaid: 1,200 × ₹5 = ₹6,000 is cancelled.', 'hard', '1200*5'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch11', 'n': 2,
        'title': 'Issue, Forfeiture and Re-Issue of Shares',
        'outcomes': [
            'Explain authorised, issued, subscribed, called-up, paid-up and reserve capital, and present them in the share capital note.',
            'Distinguish preference shares (and their kinds) from equity shares.',
            'Journalise the issue of shares for cash at par and at a premium, including full, under and over subscription with pro-rata allotment.',
            'Record calls in arrears and calls in advance with interest under Table F, and explain the legal position on issue at a discount.',
            'Pass entries for forfeiture of shares issued at par or at a premium, and for re-issue, computing the transfer to capital reserve.',
            'Record shares issued to vendors and others for consideration other than cash.',
        ],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 60, 'practice': 90}, 'prereq': ['fnd-p1-ch11-u01'],
                 'exam_tip': 'A full share-issue problem (pro-rata, default, forfeiture, re-issue) is one of the most frequent 10-mark questions in Paper 1. Always prepare a pro-rata working table first.'},
        'concepts': [
            {'id': 'c1', 'title': 'Share capital and its categories',
             'body': ['A company\'s capital is split into small, equal units called shares; the value printed on each is its face (par or nominal) value. Shareholders\' liability is limited to the issue price of their shares. Issue prices today are often fixed by book building — investors bid within a price band and the final price is set from the bids.',
                      'Authorised capital: the ceiling stated in the capital clause of the memorandum. Issued capital: the part offered — for cash, or for other consideration to promoters or others; the rest is un-issued. Subscribed capital: the part applied for by investors and allotted (including shares issued for non-cash consideration).',
                      'Called-up capital: the part of the issue price demanded so far; the rest is uncalled. Paid-up capital: called-up capital actually received. Called-up = paid-up + calls in arrears − calls in advance. Reserve capital (s. 65): uncalled capital which, by special resolution, will be called only on winding up — different from a capital reserve, which is a reserve made out of capital profits.',
                      'Subscribed capital may equal, exceed or fall short of issued capital — full, over or under subscription.'],
             'analogy': 'Authorised capital is the size of the cake you are allowed to bake; issued is the slices you put on the counter; subscribed is what guests take; called-up is what you have asked them to pay for; paid-up is what is actually in the till.',
             'work': 'Before any new issue, a CA checks that authorised capital is large enough — if not, the memorandum must first be altered and the Registrar informed.'},
            {'id': 'c2', 'title': 'Types of shares: preference and equity',
             'body': ['Preference shares (s. 43) carry a preferential right to a fixed dividend and to repayment of capital on winding up, ahead of equity. They usually have no voting rights, but if dividend on cumulative preference shares is in arrears for two years or more, the holders can vote on every resolution (as the study material puts it; s. 47(2) of the Act actually gives this right to any class of preference shares whose dividend has remained unpaid for two years or more).',
                      'Kinds: cumulative (unpaid dividend accumulates; arrears are disclosed in the notes) or non-cumulative; participating (share in surplus profits after equity gets a stated rate) or non-participating; redeemable or irredeemable; convertible or non-convertible. Unless stated otherwise, preference shares are treated as cumulative, non-participating and non-convertible.',
                      'Under s. 55 a company limited by shares cannot issue irredeemable preference shares, or preference shares redeemable after 20 years (except for notified infrastructure projects).',
                      'Equity shares are all shares that are not preference shares. Dividend is recommended by the board and varies with profits; equity holders vote and bear the residual risk. The Act also permits equity shares with differential rights as to dividend or voting, under the rules.'],
             'analogy': 'Preference shareholders are passengers with a confirmed seat and a fixed meal; equity shareholders steer the bus and get whatever is left in the canteen — sometimes a feast, sometimes nothing.',
             'work': 'When structuring funding, a CA compares cumulative preference shares (fixed cost, no dilution of control) with fresh equity (no fixed cost, but dilution).'},
            {'id': 'c3', 'title': 'Issue of shares for cash — process and entries',
             'body': ['Private companies raise money by private placement; public companies issue a prospectus. Money is usually collected in instalments: application, allotment, then calls (first, second … final).',
                      'Section 39: the amount payable with the application cannot be below 5% of the nominal value; SEBI rules require at least 25% of the issue price. Allotment cannot be made unless the minimum subscription stated in the prospectus is received — under SEBI, at least 90% of the issue. If not received, all application money must be refunded within 15 days of closure (non-underwritten issue), or 70 days where an underwritten issue fails to collect minimum subscription within 60 days. Delay attracts interest.',
                      'Entries: Bank Dr, To Share Application (money received); Share Application Dr, To Share Capital (on allotment); Share Allotment Dr, To Share Capital (amount due); Bank Dr, To Share Allotment (received); Share Call Dr, To Share Capital (call made); Bank Dr, To Share Call (received). A combined "Share Application and Allotment Account" may be used instead.',
                      'Undersubscription: if minimum subscription is received, shares are allotted to all applicants. Full subscription: shares applied = shares offered.'],
             'analogy': 'Buying a flat in instalments: booking amount (application), agreement (allotment), then construction-linked payments (calls).',
             'work': 'Issue-related entries are vouched against the board\'s allotment resolution, the bank escrow statement and the registrar\'s basis-of-allotment report.'},
            {'id': 'c4', 'title': 'Issue at a discount — the legal position',
             'body': ['Shares are issued at a discount when the issue price is below face value (₹100 share issued at ₹95 = 5% discount).',
                      'Section 53 generally prohibits issue of shares at a discount. The law allows it only where expressly permitted: sweat equity shares under s. 54, and shares issued at a discount to creditors on conversion of debt under a statutory resolution plan or debt restructuring scheme under s. 53(2A), subject to regulations.'],
             'analogy': 'Face value is the "minimum ticket price" fixed by law — you cannot sell cheaper except in the two special counters the law has opened.',
             'work': 'If a client proposes to allot shares below face value to a friend, the CA must stop it: such an allotment breaks s. 53 and exposes the company and officers to penalties.'},
            {'id': 'c5', 'title': 'Issue at a premium and the securities premium account',
             'body': ['Premium is the excess of the issue price over face value (₹10 share at ₹16 → premium ₹6). It is credited to Securities Premium Account — not to share capital — and shown under Reserves and surplus. Premium is usually collected with allotment, sometimes with application, rarely with a call.',
                      'Section 52 uses: (a) fully paid bonus shares to members; (b) writing off preliminary expenses; (c) writing off expenses, commission or discount on issue of securities or debentures; (d) providing for premium on redemption of redeemable preference shares or debentures; (e) buy-back of own shares or securities. Companies covered by the accounting standards prescribed under s. 133 cannot use it for (b) and (d).',
                      'Premium once received is never cancelled, even if the shares are later forfeited.'],
             'analogy': 'Premium is like the extra price paid for a "front-row" seat — it is not part of the ticket\'s face value, so it is kept in a separate cash box with strict rules on how it can be spent.',
             'work': 'Auditors check that securities premium has been used only for the permitted purposes — paying a dividend out of it is a serious violation.'},
            {'id': 'c6', 'title': 'Oversubscription and pro-rata allotment',
             'body': ['When applications exceed shares offered, the board may (i) reject some applications fully and refund, (ii) allot in full to some, or (iii) allot pro rata — in proportion to shares applied for — or combine these.',
                      'Under pro-rata allotment the extra application money is first adjusted against allotment (and, if the terms allow, against calls); any surplus beyond that is refunded.',
                      'Entries: Share Application Dr, To Bank (refund on rejected applications); Share Application Dr, To Share Allotment (excess adjusted); Share Application Dr, To Calls in Advance (if adjusted against future calls).',
                      'Working for a defaulter: shares allotted = applied × allotment ratio; excess = (applied − allotted) × application money; allotment unpaid = allotment due − excess.'],
             'analogy': 'If 120 guests want 100 seats, each guest gets 5 seats for every 6 requested, and the extra booking money is kept as part payment for the next instalment.',
             'work': 'Registrars to an issue prepare the basis of allotment, and the company\'s accountant must reconcile refunds and adjustments to the rupee before the shares are credited to demat accounts.'},
            {'id': 'c7', 'title': 'Calls in arrears, calls in advance and interest',
             'body': ['Calls in arrears: amounts called but not paid. Entry: Bank Dr (received), Calls in Arrears Dr (unpaid), To Share Allotment / Call (due). Shown as a deduction from called-up capital in the share capital note.',
                      'Calls in advance: money received before it is called. Entry: Bank Dr, To Calls in Advance. When the call is made: Calls in Advance Dr, Bank Dr, To Share Call. Until adjusted it is a liability (other current liabilities), not share capital, and carries no dividend.',
                      'Interest under Table F (when the articles are silent): up to 10% p.a. charged on calls in arrears from the due date to the date of payment (directors may waive it); up to 12% p.a. paid on calls in advance from the date of receipt to the date the call falls due. Interest on arrears is income; interest on advance is an expense (finance cost).'],
             'analogy': 'Calls in arrears = a late EMI (the lender charges a penalty); calls in advance = prepaying an EMI (here the company pays you interest for the early money).',
             'work': 'Companies with Table F articles must compute interest on advance calls — auditors recompute it, and the TDS position on such interest is also checked.'},
            {'id': 'c8', 'title': 'Forfeiture of shares',
             'body': ['Forfeiture cancels the shares of a member who fails to pay allotment or call money, after a proper notice as per the articles. His title ends and the money already paid is not refunded. Directors may cancel a forfeiture before the shares are re-allotted. Fully paid shares may be forfeited only if the articles specifically allow it (e.g., to recover the member\'s debts).',
                      'Issued at par: Share Capital Dr (called-up amount on those shares), To Share Allotment / Calls (or Calls in Arrears) (unpaid), To Forfeited Shares (amount received).',
                      'Issued at a premium, premium not received: also debit Securities Premium with the unpaid premium. Premium already received is NOT cancelled — the entry then debits only Share Capital.',
                      'Forfeited Shares balance on shares not yet re-issued is added to share capital in the balance sheet.'],
             'analogy': 'Forfeiture is like losing your booking amount when you stop paying instalments on a flat — the builder keeps what you paid and can sell the flat to someone else.',
             'work': 'Before forfeiture, a company secretary checks that the notice period and procedure in the articles were followed — a defective forfeiture can be challenged in court.'},
            {'id': 'c9', 'title': 'Re-issue of forfeited shares',
             'body': ['Re-issue is a sale, not a fresh allotment. Shares may be re-issued at any price as long as the total collected from the old and new holder together is not less than the face value (or paid-up value) credited — so the discount on re-issue cannot exceed the forfeited amount on those shares.',
                      'Entry: Bank Dr (received), Forfeited Shares Dr (discount), To Share Capital (amount credited as paid-up). Then Forfeited Shares Dr, To Capital Reserve with the surplus on the shares re-issued.',
                      'Only the surplus relating to the shares actually re-issued goes to capital reserve; the rest stays in Forfeited Shares. If shares are re-issued above face value, the excess goes to Securities Premium. Where shares were forfeited at different paid-up amounts, compute the surplus batch by batch.',
                      'Formula: Capital reserve = (forfeited amount per share − discount per share) × shares re-issued.'],
             'analogy': 'Re-selling a returned concert ticket: you may give the new buyer a discount, but never more than the deposit the first buyer forfeited — otherwise the organiser would be out of pocket.',
             'work': 'A common audit finding: the entire Forfeited Shares balance moved to capital reserve though only some shares were re-issued. The fix is a reversal for the shares still held.'},
            {'id': 'c10', 'title': 'Shares issued for consideration other than cash',
             'body': ['A company may issue shares to vendors for land, buildings, machinery or a whole business, and to promoters or professionals for services in its formation. These are shown separately in the share capital note.',
                      'Within the prescribed time the company must file the written contract for which the shares were allotted with the Registrar. Under accounting standards, an asset acquired for shares is recorded at the fair value of the shares issued (which may differ from par value).',
                      'Entries: Asset A/c Dr, To Vendor; then Vendor Dr, To Share Capital (and To Securities Premium if issued at a premium). Number of shares = amount payable in shares ÷ issue price per share.'],
             'analogy': 'Paying for a car with shares instead of cash — the seller becomes a part-owner of your company.',
             'work': 'Valuation reports and the registrar filing are checked during due diligence; an overstated asset value for shares inflates both assets and capital.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Full subscription — shares issued at a premium', 'difficulty': 'core', 'minutes': 10,
             'q': 'Ruhani Ltd issued 40,000 equity shares of ₹10 each at ₹12, payable ₹3 on application (10 April 2026), ₹5 on allotment including the premium of ₹2 (allotment 25 April), and ₹4 on first and final call (1 August). The issue was fully subscribed and all money was received. Pass journal entries.',
             'solution': [journal(E1, 'Journal of Ruhani Ltd', 'j1'),
                          wn('Check', 'Share capital = 3 + 3 + 4 = ₹10 per share × 40,000 = ₹4,00,000; Securities premium = ₹2 × 40,000 = ₹80,000; cash received = ₹12 × 40,000 = ₹4,80,000.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Pro-rata allotment, default, forfeiture and re-issue', 'difficulty': 'hard', 'minutes': 25,
             'q': 'Tanvi Ltd offered 50,000 equity shares of face value ₹10 at ₹12 (premium ₹2), payable ₹3 on application, ₹5 on allotment (including premium) and ₹4 on first and final call. Applications were received for 70,000 shares. Applications for 10,000 shares were rejected; the remaining applicants were allotted 50,000 shares pro rata, the excess application money being adjusted towards allotment. Ajay, who had applied for 1,200 shares, failed to pay allotment and call money; his shares were forfeited on 1 December. On 20 December, 600 of these shares were re-issued at ₹8 per share as fully paid. Journalise and show share capital and reserves in the balance sheet.',
             'given': [table(['Category', 'Applied', 'Allotted', 'Application money ₹', 'Required ₹', 'Excess ₹', 'Treatment'], [
                 ['Rejected', '10,000', '0', inr(rej), '0', inr(rej), 'Refunded'],
                 ['Pro rata (6 : 5)', '60,000', '50,000', inr(180000), inr(tocap), inr(excess), 'Adjusted to allotment'],
                 ['Total', '70,000', '50,000', inr(app), inr(tocap), inr(rej + excess), ''],
             ], num=[3, 4, 5], total=True, title='Working 1 — pro-rata table')],
             'solution': [journal(E2, 'Journal of Tanvi Ltd', 'j2'),
                          wn('Working 2 — Ajay', f'Allotted 1,200 × 5/6 = 1,000 shares. Paid on application 1,200 × ₹3 = ₹{inr(aj_paid)}; needed 1,000 × ₹3 = ₹3,000; excess ₹{inr(aj_excess)} adjusted. Allotment due 1,000 × ₹5 = ₹5,000 − 600 = ₹{inr(aj_unpaid)} unpaid. Call unpaid 1,000 × ₹4 = ₹{inr(call_unpaid)}.'),
                          wn('Working 3 — allotment received', f'₹{inr(allot)} − adjusted ₹{inr(excess)} − Ajay ₹{inr(aj_unpaid)} = ₹{inr(allot_recd)}.'),
                          wn('Working 4 — capital reserve', f'Forfeited on 1,000 shares ₹{inr(forf)} (all received from Ajay). On 600 shares: ₹{inr(forf600)}. Discount on re-issue 600 × ₹2 = ₹{inr(re_loss)}. Capital reserve = {inr(forf600)} − {inr(re_loss)} = ₹{inr(cr)}. Balance on 400 shares = ₹{inr(forf_left)}.'),
                          note2, rs2,
                          p(f'Bank balance = ₹{inr(bank)}, equal to share capital ₹{inr(paidcap + forf_left)} + reserves ₹{inr(sp + cr)}.'),
                          note('Ajay paid nothing towards allotment except the ₹600 adjusted from application money; following the usual exam convention, money received is applied first to capital, so his premium of ₹2,000 is treated as unpaid and cancelled on forfeiture.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Calls in arrears and calls in advance with interest (Table F)', 'difficulty': 'moderate', 'minutes': 12,
             'q': 'Sitara Ltd has 30,000 equity shares of ₹10 each. The first call of ₹3 was due on 1 August 2026; the holder of 2,000 shares paid it only on 31 January 2027. On 1 September 2026 a holder of 1,500 shares paid the final call of ₹4 in advance; the final call was made on 1 March 2027 and the rest was received that day. The company follows Table F (10% on arrears, 12% on advance). Journalise, using a Calls in Arrears account.',
             'solution': [journal(E3, 'Journal of Sitara Ltd', 'j3'),
                          wn('Interest', f'Arrears ₹{inr(arr)} × 10% × 6/12 (1 Aug to 31 Jan) = ₹{inr(i_arr)}. Advance ₹{inr(adv)} × 12% × 6/12 (1 Sep to 1 Mar) = ₹{inr(i_adv)}.'),
                          note('Interest on calls in arrears is income (credited to the statement of profit and loss); interest on calls in advance is a finance cost. In practice TDS may apply to interest paid; it is ignored here.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Business purchased for shares (consideration other than cash)', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'Lotus Ltd took over the business of Sharma Brothers on 1 July 2026: assets ₹8,00,000 and liabilities ₹1,50,000, for a purchase consideration of ₹7,15,000. It paid ₹55,000 by cheque and the balance by issuing equity shares of ₹10 each at ₹11. Journalise.',
             'solution': [journal(E4, 'Journal of Lotus Ltd', 'j4'),
                          wn('Working', f'Net assets = 8,00,000 − 1,50,000 = ₹{inr(net)}; goodwill = 7,15,000 − {inr(net)} = ₹{inr(gw)}. Shares = ({inr(715000)} − 55,000) ÷ ₹11 = {inr(nsh)} shares.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Reconciling an IPO refund and allotment', 'role': 'Assistant manager, finance team of a company completing its IPO',
             'situation': 'The registrar sends the basis of allotment: 3.2 times oversubscription, some categories allotted pro rata, others by lottery. The escrow bank statement shows application money, and the treasury wants refunds made within the SEBI timeline.',
             'steps': ['Build a category-wise table: applied, allotted, money received, money needed, excess.',
                       'Agree the total refund with the registrar\'s refund file and the escrow bank balance.',
                       'Pass entries: transfer to share capital (and securities premium) for allotted shares; refunds for unsuccessful applicants.',
                       'Check that no interest liability arises from late refunds.',
                       'Prepare the share capital note: shares issued, subscribed, paid-up, and reconciliation of shares at the start and end of the year.'],
             'takeaway': 'A pro-rata working table is the backbone of both the exam answer and the real-life IPO reconciliation.',
             'think': 'Applications for 3,20,000 shares at ₹50 each were received for an issue of 1,00,000 shares, all allotted pro rata, with application money ₹50 (full price). What is the refund?',
             'answer': '(3,20,000 − 1,00,000) × ₹50 = ₹1,10,00,000, since application money already equals the full price and there is nothing left to adjust.',
             'checks': [{'expr': '(320000-100000)*50', 'value': 11000000, 'label': 'Refund'}]},
            {'id': 'j2', 'title': 'Cleaning up an old forfeited-shares balance', 'role': 'Statutory audit senior',
             'situation': 'A client shows "Forfeited Shares ₹29,000" inside share capital. The papers show 3,000 shares of ₹20 each (₹15 paid) forfeited five years ago, giving ₹45,000. Later 2,000 were re-issued at ₹12 as fully paid; the client debited ₹16,000 of discount to Forfeited Shares but never transferred any gain to capital reserve.',
             'steps': ['Recompute: forfeited amount ₹15 per share; discount on re-issue ₹20 − ₹12 = ₹8 per share — within the limit of ₹15.',
                       'Gain on the 2,000 re-issued shares = (15 − 8) × 2,000 = ₹14,000 — this should be in capital reserve.',
                       'Correct Forfeited Shares balance = 1,000 shares not re-issued × ₹15 = ₹15,000 (₹29,000 − ₹14,000).',
                       'Propose the adjusting entry: Forfeited Shares A/c Dr ₹14,000, To Capital Reserve A/c ₹14,000.',
                       'Check the share capital note now shows ₹15,000 as forfeited shares and the capital reserve under reserves and surplus.'],
             'takeaway': 'Forfeited Shares should hold exactly the amounts on shares not yet re-issued; everything else is either absorbed by discount or is capital reserve.',
             'checks': [{'expr': '(15-8)*2000', 'value': 14000, 'label': 'Capital reserve on re-issue'}, {'expr': '1000*15', 'value': 15000, 'label': 'Correct forfeited balance'}]},
        ],
        'mcqs': [
            mcq('m1', 'Under section 39, the minimum application money must be at least:', ['5% of the nominal value of the share', '25% of the nominal value', '10% of the issue price', '50% of the issue price'], 0,
                'Section 39 sets 5% of nominal value; SEBI separately requires at least 25% of the issue price for listed issues.', 'c3'),
            mcq('m2', 'A company issued 20,000 shares of ₹10 at ₹14. Total amount credited to Securities Premium is:', ['₹80,000', '₹2,80,000', '₹2,00,000', '₹40,000'], 0,
                'Premium ₹4 × 20,000 shares.', 'c5', 'core', '20000*4'),
            mcq('m3', 'Securities premium cannot be used for:', ['Paying dividend to shareholders', 'Issuing fully paid bonus shares', 'Writing off commission on issue of shares', 'Buy-back of own shares'], 0,
                'Section 52 lists the permitted uses; dividend is not one of them.', 'c5'),
            mcq('m4', 'Applications for 90,000 shares are received for 60,000 shares offered, all allotted pro rata. Application money is ₹4 and allotment ₹5. The amount adjusted towards allotment is:', ['₹1,20,000', '₹3,00,000', '₹1,80,000', '₹3,60,000'], 0,
                'Excess shares 30,000 × ₹4 = ₹1,20,000, which is less than allotment due ₹3,00,000, so all of it is adjusted.', 'c6', 'moderate', '(90000-60000)*4'),
            mcq('m5', 'Interest on calls in advance under Table F can be paid at a maximum of:', ['12% p.a.', '10% p.a.', '6% p.a.', '18% p.a.'], 0,
                'Table F: up to 12% on calls in advance; up to 10% on calls in arrears.', 'c7'),
            mcq('m6', 'Calls in advance appear in the balance sheet under:', ['Current liabilities — Other current liabilities', 'Shareholders\' funds — Share capital', 'Reserves and surplus', 'Current assets'], 0,
                'Money received before it is called is not share capital; it is a liability until the call is made.', 'c7', 'moderate'),
            mcq('m7', '500 shares of ₹10 each (₹8 called up) were forfeited for non-payment of the second call of ₹2. The amount credited to Forfeited Shares Account is:', ['₹3,000', '₹4,000', '₹1,000', '₹5,000'], 0,
                'Called up ₹8 − unpaid ₹2 = ₹6 received per share × 500 = ₹3,000.', 'c8', 'core', '500*(8-2)'),
            mcq('m8', 'Shares of ₹10 issued at ₹13 (premium payable with allotment) are forfeited after allotment was paid but the first call of ₹3 was not. On forfeiture, Securities Premium Account is:', ['Not debited, since the premium has been received', 'Debited with ₹3 per share', 'Credited with ₹3 per share', 'Transferred to capital reserve'], 0,
                'Premium already received is never cancelled on forfeiture.', 'c8', 'moderate'),
            mcq('m9', '200 shares of ₹10, on which ₹6 had been paid, were forfeited and re-issued at ₹7 as fully paid. The amount transferred to capital reserve is:', ['₹600', '₹1,200', '₹1,400', '₹800'], 0,
                'Forfeited ₹6 × 200 = 1,200; discount ₹3 × 200 = 600; capital reserve = 1,200 − 600 = ₹600.', 'c9', 'moderate', '200*6-200*3'),
            mcq('m10', '300 forfeited shares (₹10 each, ₹4 paid) are to be re-issued as fully paid. The minimum re-issue price per share is:', ['₹6', '₹4', '₹10', '₹2'], 0,
                'Discount on re-issue cannot exceed ₹4 per share (the forfeited amount): 10 − 4 = ₹6.', 'c9', 'moderate', '10-4'),
            mcq('m11', 'Machinery worth ₹4,40,000 is bought by issuing ₹10 equity shares at 10% premium. Number of shares issued:', ['40,000', '44,000', '4,000', '48,400'], 0,
                'Issue price ₹11; 4,40,000 ÷ 11 = 40,000 shares.', 'c10', 'core', '440000/11'),
            mcq('m12', 'Which statement about issue of shares at a discount is correct?', ['It is generally prohibited by section 53, except sweat equity and debt conversion under a resolution plan', 'It is allowed up to 10% with a special resolution', 'It is freely allowed for private companies', 'It is allowed if the company has been in business for one year'], 0,
                'The old "up to 10% after one year" rule belonged to the 1956 Act; s. 53 now prohibits discount issues except as expressly permitted.', 'c4', 'moderate'),
            mcq('m13', 'Called-up capital ₹6,00,000; calls in arrears ₹9,000; calls in advance ₹4,000. Paid-up capital shown in the share capital note is:', ['₹5,91,000', '₹5,95,000', '₹6,04,000', '₹5,87,000'], 0,
                'Paid-up = called-up − calls in arrears = ₹5,91,000. Calls in advance are a liability, not capital.', 'c1', 'moderate', '600000-9000'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 10, 'minutes': minutes(10), 'difficulty': 'hard', 'pad': 'journal',
             'q': 'Mohan Ltd invited applications for 1,00,000 equity shares of ₹10 each at par, payable ₹2 on application, ₹3 on allotment, ₹3 on first call and ₹2 on final call. Applications were received for 1,60,000 shares. Applications for 20,000 shares were rejected and the money refunded. The remaining applicants were allotted shares pro rata; excess application money was adjusted towards allotment. Sneha, who had applied for 2,800 shares, did not pay allotment and first call money; her shares were forfeited after the first call. The final call has not yet been made. 1,500 of the forfeited shares were re-issued as ₹8 paid up for ₹7 per share. Pass journal entries (narrations may be brief).',
             'given': [table(['Category', 'Applied', 'Allotted', 'Money received ₹', 'Required ₹', 'Excess ₹'], [
                 ['Rejected', '20,000', '0', inr(q1_rej), '0', inr(q1_rej)],
                 ['Pro rata (7 : 5)', '1,40,000', '1,00,000', inr(280000), inr(q1_cap), inr(q1_exc)],
                 ['Total', '1,60,000', '1,00,000', inr(q1_app), inr(q1_cap), inr(q1_rej + q1_exc)]], num=[3, 4, 5], total=True, title='Working — pro-rata table')],
             'model': [journal(Q1, 'Journal of Mohan Ltd', 'jq1'),
                       wn('Sneha', f'Allotted 2,800 × 5/7 = 2,000 shares. Excess application money = (2,800 − 2,000) × ₹2 = ₹{inr(q1_sn_exc)}. Allotment unpaid = 2,000 × ₹3 − 1,600 = ₹{inr(q1_sn_un)}. First call unpaid = 2,000 × ₹3 = ₹6,000. Called up on her shares = 2,000 × ₹8 = ₹16,000; received = 5,600 → Forfeited Shares ₹{inr(q1_forf)}.'),
                       wn('Re-issue', f'Discount = (8 − 7) × 1,500 = ₹1,500. Forfeited on 1,500 shares = 5,600 × 1,500/2,000 = ₹{inr(q1_f15)}. Capital reserve = ₹{inr(q1_cr)}; ₹1,400 stays in Forfeited Shares for 500 shares.')],
             'checks': q1c,
             'scheme': [S('s1', 'Pro-rata working: rejected, allotted, excess ₹80,000', 1.5, 'computation'),
                        S('s2', 'Application money received and its transfer to capital / allotment / refund', 1.5, 'posting'),
                        S('s3', 'Allotment due and amount received ₹2,15,600 (net of adjustment and Sneha\'s default)', 1.5, 'computation'),
                        S('s4', 'First call made and received on 98,000 shares', 1, 'posting'),
                        S('s5', 'Forfeiture entry: Capital Dr ₹16,000; Allotment ₹4,400, Call ₹6,000, Forfeited ₹5,600', 2, 'computation'),
                        S('s6', 'Re-issue entry: Bank ₹10,500, Forfeited ₹1,500, Capital ₹12,000', 1, 'posting'),
                        S('s7', 'Capital reserve ₹2,700 on 1,500 shares only', 1.5, 'computation')],
             'remarks': ['Candidates who skip the pro-rata table usually get the allotment cash and the forfeiture figures wrong together.', 'Many debit Share Capital with ₹20,000 (full face value) on forfeiture — only the called-up ₹8 per share is debited.', 'A common slip is transferring the full ₹5,600 to capital reserve although only 1,500 of 2,000 shares were re-issued.'],
             'mistakes': ['Computing Sneha\'s allotment as 2,800 × ₹3.', 'Forgetting to adjust her excess application money of ₹1,600.', 'Crediting share capital with ₹15,000 (₹10 per share) on re-issue though the shares are re-issued as ₹8 paid up.'],
             'tips': ['Start with the pro-rata table and a separate working for the defaulter.', 'Write the forfeiture entry as: Capital (called-up) = unpaid amounts + Forfeited (received).', 'Show the capital reserve calculation in a working note.']},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'journal',
             'q': 'Rana Ltd forfeited 800 equity shares of ₹10 each, issued at ₹12, for non-payment of the final call of ₹3. The premium of ₹2 had been received with allotment. Of these, 500 shares were re-issued at ₹9 per share as fully paid. Pass journal entries for forfeiture and re-issue, and state the balance of Forfeited Shares Account after the re-issue.',
             'model': [journal(Q2, 'Journal of Rana Ltd', 'jq2'),
                       wn('Workings', f'Called up ₹10 × 800 = ₹{inr(q2_cap)}; final call unpaid ₹3 × 800 = ₹{inr(q2_unp)}; capital received ₹7 × 800 = ₹{inr(q2_forf)}. Premium was received, so it is not cancelled. On 500 shares, forfeited amount ₹{inr(q2_f500)}; discount ₹{inr(q2_disc)}; capital reserve ₹{inr(q2_cr)}. Balance on 300 shares = ₹{inr(q2_left)}.')],
             'checks': q2c,
             'scheme': [S('s1', 'Forfeiture: Share Capital Dr ₹8,000 (no debit to securities premium)', 1.5, 'concept'),
                        S('s2', 'Credits: Final call ₹2,400, Forfeited Shares ₹5,600', 1, 'computation'),
                        S('s3', 'Re-issue: Bank ₹4,500 + Forfeited ₹500 = Capital ₹5,000', 1, 'posting'),
                        S('s4', 'Capital reserve ₹3,000 and closing balance ₹2,100', 1.5, 'computation')],
             'remarks': ['Most marks are lost by debiting securities premium although it had already been received.'],
             'mistakes': ['Debiting Securities Premium ₹1,600.', 'Moving the whole ₹5,600 to capital reserve.'],
             'tips': ['Ask first: was the premium received? If yes, it stays.']},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
             'q': 'Distinguish between calls in arrears and calls in advance (four points).',
             'model': [table(['Basis', 'Calls in arrears', 'Calls in advance'], [
                 ['Meaning', 'Amount called but not paid by the shareholder', 'Amount paid by the shareholder before it is called'],
                 ['Interest (Table F)', 'Company may charge up to 10% p.a. from the due date to the date of payment', 'Company pays up to 12% p.a. from receipt to the date the call falls due'],
                 ['Nature of interest', 'Income for the company; directors may waive it', 'Expense (finance cost) for the company; no dividend on such amount'],
                 ['Balance sheet', 'Deducted from called-up capital in the share capital note', 'Shown under other current liabilities'],
                 ['Effect of default', 'Can lead to forfeiture of shares', 'No forfeiture issue; adjusted when the call is made'],
             ])],
             'scheme': [S('s1', 'Meaning', 1, 'concept'), S('s2', 'Interest rates and period', 1, 'concept'), S('s3', 'Treatment of interest / dividend', 1, 'concept'), S('s4', 'Balance sheet presentation', 1, 'presentation')],
             'remarks': ['The rates of 10% and 12% are often swapped — a costly error.'],
             'mistakes': ['Showing calls in advance as part of share capital.', 'Saying interest on calls in arrears is paid by the company.'],
             'tips': ['Use a three-column table and include the period for which interest runs.']},
            {'id': 'q4', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': '(a) State the purposes for which securities premium may be applied under section 52 of the Companies Act, 2013. (3 marks) (b) Can a company issue shares at a discount? (2 marks)',
             'model': [p('(a) Securities premium may be applied: (i) to issue unissued shares as fully paid bonus shares to members; (ii) to write off preliminary expenses; (iii) to write off expenses of, commission paid or discount allowed on issue of any securities or debentures; (iv) to provide for premium payable on redemption of redeemable preference shares or debentures; (v) to buy back its own shares or other securities. Companies whose financial statements follow the accounting standards prescribed under s. 133 cannot use it for (ii) and (iv).'),
                       p('(b) Generally no. Section 53 prohibits issue of shares at a discount and such an issue is void. Exceptions: sweat equity shares under s. 54, and shares issued at a discount to creditors on conversion of debt under a statutory resolution plan or debt restructuring scheme (s. 53(2A)).')],
             'scheme': [S('s1', 'At least five uses listed correctly', 2.5, 'provision'), S('s2', 'Restriction for s. 133 companies', 0.5, 'provision'),
                        S('s3', 'Discount generally prohibited — s. 53', 1, 'provision'), S('s4', 'Exceptions: sweat equity, debt conversion', 1, 'provision')],
             'remarks': ['Candidates still quote the old 10%-discount rule from the 1956 Act — it earns no marks.'],
             'mistakes': ['Listing "payment of dividend" as a use of securities premium.', 'Omitting the sweat equity exception.'],
             'tips': ['Number the uses; quote section numbers.']},
        ],
        'viva': viva,
        'cases': cases,
        'revision': {
            'summary': ['Capital categories: authorised → issued → subscribed → called-up → paid-up; reserve capital is callable only on winding up.',
                        'Preference shares: preferential dividend and capital; cumulative, non-participating, non-convertible by default; no irredeemable issues; max 20 years (s. 55).',
                        'Issue for cash: application (≥5% of nominal value, s. 39; SEBI ≥25% of issue price), minimum subscription 90%, refund within 15 days.',
                        'Premium → Securities Premium (Reserves and surplus); uses only under s. 52. Discount issue prohibited (s. 53) except sweat equity and debt conversion.',
                        'Pro rata: excess application money adjusted to allotment (then calls), surplus refunded.',
                        'Table F interest: arrears ≤10% (income), advance ≤12% (expense).',
                        'Forfeiture: Capital Dr (called up), [Securities Premium Dr if unpaid], To unpaid calls, To Forfeited Shares (received).',
                        'Re-issue: discount ≤ forfeited amount; surplus on re-issued shares → Capital Reserve.'],
            'remember': ['Premium once received is never cancelled.', 'Only the gain on shares actually re-issued goes to capital reserve.', 'Forfeited Shares balance is added to share capital in the balance sheet.', 'Calls in advance are a liability, not capital.'],
            'traps': ['Debiting capital with full face value on forfeiture when shares are only partly called.', 'Swapping the 10% and 12% rates.', 'Forgetting excess application money of the defaulter in pro-rata problems.', 'Crediting share capital with the issue price instead of face value — the premium goes separately.'],
        },
        'quickref': [
            {'k': 'Paid-up capital', 'v': 'Called-up − calls in arrears (calls in advance shown as a liability)'},
            {'k': 'Application money', 'v': '≥5% of nominal value (s. 39); SEBI ≥25% of issue price'},
            {'k': 'Minimum subscription', 'v': '90% of issue (SEBI); refund within 15 days (70 days for underwritten issue failing in 60 days)'},
            {'k': 'Securities premium uses', 'v': 's. 52 — bonus shares, preliminary expenses, issue expenses/commission/discount, redemption premium, buy-back'},
            {'k': 'Discount on issue', 'v': 's. 53 prohibited; exceptions s. 54 sweat equity, s. 53(2A) debt conversion'},
            {'k': 'Interest (Table F)', 'v': 'Arrears ≤10% p.a. (due date → payment); Advance ≤12% p.a. (receipt → due date)'},
            {'k': 'Forfeiture entry', 'v': 'Share Capital Dr (called up) [+ Sec. Premium Dr if unpaid] To Allotment/Calls (unpaid) To Forfeited Shares (received)'},
            {'k': 'Re-issue entry', 'v': 'Bank Dr + Forfeited Shares Dr (discount) To Share Capital; Forfeited Shares Dr To Capital Reserve (surplus)'},
            {'k': 'Capital reserve on re-issue', 'v': '(Forfeited amount per share − discount per share) × shares re-issued'},
            {'k': 'Shares for assets', 'v': 'No. of shares = consideration payable in shares ÷ issue price'},
        ],
    }
