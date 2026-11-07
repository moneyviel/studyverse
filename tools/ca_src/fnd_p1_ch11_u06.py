"""CA Foundation · Paper 1 Accounting · Chapter 11 Company Accounts · Unit 6 Redemption of Debentures.
Original explanations, names and numbers (structure and scope follow the ICAI study material).
DRR and investment rules follow Rule 18(7) of the Companies (Share Capital and Debentures) Rules as amended in 2019, as given in the study material."""
from lib import *
from ca_viva import P, ALT, V
from ca_cases import M

UID = 'fnd-p1-ch11-u06'


def mcq(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check: d['check'] = check
    return d


def S(sid, pt, m, skill): return {'id': sid, 'pt': pt, 'm': m, 'skill': skill}


def L(ac, dr, cr):
    """A closed ledger account (both sides total the same)."""
    return {'t': 'ledger', 'ac': ac, 'dr': [{'date': d, 'part': p_, 'amt': a} for d, p_, a in dr], 'cr': [{'date': d, 'part': p_, 'amt': a} for d, p_, a in cr]}


def build():
    # ---------------- Illustration 1: lump-sum redemption (unlisted company) ----------------
    c1 = Checks()
    deb = c1.add('20000*100', 'Debentures: 20,000 × ₹100')
    need = c1.add('2000000*10/100', 'DRR required: 10% of outstanding debentures')
    top = c1.add('200000-120000', 'Transfer needed to DRR')
    inv = c1.add('2000000*15/100', 'Investment: 15% of debentures maturing in the year')
    intr = c1.add('300000*6/100*11/12', 'Interest on DRR investment @6% for 11 months (30 Apr – 31 Mar)')
    prem = c1.add('2000000*5/100', 'Premium on redemption @5%')
    pay = c1.add('2000000+100000', 'Amount payable to debenture holders')
    E1 = [
        je('2027 Apr 1', [('Profit and Loss A/c', top)], [('Debenture Redemption Reserve A/c', top)], 'Being DRR brought up to 10% of outstanding debentures'),
        je('2027 Apr 30', [('DRR Investment A/c', inv)], [('Bank A/c', inv)], 'Being 15% of debentures maturing this year deposited with a scheduled bank, free of charge or lien'),
        je('2028 Mar 31', [('Bank A/c', intr)], [('Interest on DRR Investment A/c', intr)], 'Being interest received on DRR investment'),
        je('2028 Mar 31', [('Interest on DRR Investment A/c', intr)], [('Profit and Loss A/c', intr)], 'Being interest on DRR investment transferred to profit and loss'),
        je('2028 Mar 31', [('Bank A/c', inv)], [('DRR Investment A/c', inv)], 'Being DRR investment encashed for redemption'),
        je('2028 Mar 31', [('8% Debentures A/c', deb), ('Premium on Redemption of Debentures A/c', prem)], [('Debenture Holders A/c', pay)], 'Being amount due on redemption at 5% premium (premium provided at issue)'),
        je('2028 Mar 31', [('Debenture Holders A/c', pay)], [('Bank A/c', pay)], 'Being debenture holders paid'),
        je('2028 Mar 31', [('Debenture Redemption Reserve A/c', need)], [('General Reserve A/c', need)], 'Being DRR transferred to general reserve after redemption'),
    ]

    # ---------------- Illustration 2: instalments — investment schedule ----------------
    c2 = Checks()
    yr = c2.add('3000000/3', 'Each yearly instalment')
    i1 = c2.add('1000000*15/100', 'Investment for each year: 15% of debentures maturing')
    drr2 = c2.add('3000000*10/100', 'DRR on issue: 10% of outstanding ₹30,00,000')
    sch = table(['Year ending 31 March', 'Debentures maturing (₹)', 'Investment by 30 April of that year (₹)', 'Debentures outstanding after redemption (₹)'], [
        ['2028', inr(yr), inr(i1), inr(2000000)], ['2029', inr(yr), inr(i1), inr(1000000)], ['2030', inr(yr), inr(i1), '0'],
        ['Total', inr(3000000), inr(450000), '']], num=[1, 2], total=True, title='Investment of DRR amount — Prakash Ltd')
    E2 = [
        je('2026 Apr 1', [('Profit and Loss A/c', drr2)], [('Debenture Redemption Reserve A/c', drr2)], 'Being DRR created at 10% of debentures outstanding'),
        je('2027 Apr 30', [('DRR Investment A/c', i1)], [('Bank A/c', i1)], 'Being 15% of debentures maturing in 2027-28 invested in Central Government securities'),
        je('2028 Mar 31', [('Bank A/c', i1)], [('DRR Investment A/c', i1)], 'Being investment realised for the first instalment'),
        je('2028 Mar 31', [('10% Debentures A/c', yr)], [('Debenture Holders A/c', yr)], 'Being first instalment of debentures due for redemption at par'),
        je('2028 Mar 31', [('Debenture Holders A/c', yr)], [('Bank A/c', yr)], 'Being first instalment paid'),
    ]

    # ---------------- Illustration 3: conversion option on redemption ----------------
    c3 = Checks()
    opted = c3.add('50000/100', 'Debentures held by those opting')
    conv = c3.add('500*30/100', 'Debentures converted (30%)')
    rv_conv = c3.add('150*110', 'Redemption value of converted debentures @ ₹110')
    shares = c3.add('16500/25', 'Equity shares @ ₹25')
    cashd = c3.add('(500-150)*110', 'Cash for the remaining 350 debentures')
    c3.add('660*10', 'Share capital credited')
    c3.add('660*15', 'Securities premium credited')
    E3 = [
        je('(1)', [('9% Convertible Debentures A/c', 50000), ('Premium on Redemption of Debentures A/c', 5000)], [('Debenture Holders A/c', 55000)], 'Being 500 debentures due for redemption at 10% premium'),
        je('(2)', [('Debenture Holders A/c', rv_conv)], [('Equity Share Capital A/c', 6600), ('Securities Premium A/c', 9900)], 'Being 660 equity shares of ₹10 issued at ₹25 on conversion of 150 debentures'),
        je('(3)', [('Debenture Holders A/c', cashd)], [('Bank A/c', cashd)], 'Being cash paid for the remaining 350 debentures'),
    ]

    # ---------------- Question 1 model: ledgers of Sagar Ltd ----------------
    q1c = Checks()
    q1_req = q1c.add('900000*10/100', 'DRR required 10%')
    q1_top = q1c.add('90000-40000', 'Transfer to DRR')
    q1_int = q1c.add('135000*8/100', 'Interest on DRR investment')
    q1_prem = q1c.add('900000*5/100', 'Premium on redemption')
    q1_pay = q1c.add('900000+45000', 'Payable to debenture holders')
    q1_bank = q1c.add('840000+10800+135000-945000', 'Closing bank balance')
    Lq1 = [
        L('11% Debentures Account', [('2027 Mar 31', 'To Debenture Holders A/c', 900000)], [('2026 Apr 1', 'By Balance b/d', 900000)]),
        L('Debenture Redemption Reserve Account', [('2027 Mar 31', 'To General Reserve A/c', q1_req)], [('2026 Apr 1', 'By Balance b/d', 40000), ('2026 Apr 1', 'By Profit and Loss A/c', q1_top)]),
        L('DRR Investment (8% Government Bonds) Account', [('2026 Apr 1', 'To Balance b/d', 135000)], [('2027 Mar 31', 'By Bank A/c', 135000)]),
        L('Debenture Holders Account', [('2027 Mar 31', 'To Bank A/c', q1_pay)], [('2027 Mar 31', 'By 11% Debentures A/c', 900000), ('2027 Mar 31', 'By Premium on Redemption of Debentures A/c', q1_prem)]),
        L('Bank Account', [('2027 Mar 31', 'To Balance b/d', 840000), ('2027 Mar 31', 'To Interest on DRR Investment A/c', q1_int), ('2027 Mar 31', 'To DRR Investment A/c', 135000)],
          [('2027 Mar 31', 'By Debenture Holders A/c', q1_pay), ('2027 Mar 31', 'By Balance c/d', q1_bank)]),
    ]

    # ---------------- Question 3 model: conversion ----------------
    q3c = Checks()
    q3_n = q3c.add('80000/100', 'Debentures of holders opting')
    q3_c = q3c.add('800*25/100', 'Debentures converted (25%)')
    q3_v = q3c.add('200*104', 'Redemption value converted')
    q3_s = q3c.add('20800/40', 'Shares @ ₹40')
    q3_cash = q3c.add('600*104', 'Cash for 600 debentures')
    q3c.add('520*10', 'Share capital')
    q3c.add('520*30', 'Securities premium')

    viva = [
        V('v1', 'What is a debenture redemption reserve and what does section 71(4) say about it?',
          'A debenture redemption reserve is a reserve created out of profits available for dividend, so that funds are set aside for repaying debentures. Section 71(4) requires a company issuing debentures to create such a reserve out of its profits available for payment of dividend, as per the rules, and the amount credited to it cannot be used for any purpose other than redemption of debentures. After the debentures are redeemed, the balance is transferred to general reserve.',
          [P('p1', 'Created out of profits available for dividend', 3, 'profit', 'dividend|distribut|divisible|available', min=2),
           P('p2', 'Meant for redemption of debentures; cannot be used for anything else', 4, ALT('{n} {u} {o}', '{u} only for redemption', 'only for redemption', 'only for redeeming', 'solely for redemption', 'only be used for redemption', n=('not', 'cannot', 'can t', 'never'), u=('used', 'utilised', 'utilized', 'be used', 'be utilised'), o=('other', 'any other', 'for any other', 'other purpose'))),
           P('p3', 'Transferred to general reserve after redemption', 3, 'general reserve')], 'c2'),
        V('v2', 'Which companies must create a debenture redemption reserve under Rule 18(7) as amended in 2019, and how much?',
          'All India Financial Institutions regulated by RBI and banking companies need no DRR. Listed companies need no DRR either, including listed NBFCs and housing finance companies, for public or privately placed debentures. Unlisted NBFCs and HFCs need none for privately placed debentures. Other unlisted companies must keep a DRR of ten per cent of the value of outstanding debentures. Other financial institutions follow the NBFC rule.',
          [P('p1', 'Banks and All India Financial Institutions — no DRR', 2, 'bank|aifi|financial institution', 'no drr|no debenture redemption reserve|not required|not need|no reserve|need no|exempt|nil', min=2),
           P('p2', 'Listed companies (incl. listed NBFCs/HFCs) — no DRR', 3, ALT('listed {x}', 'listed companies {x}', x=('no drr', 'need no', 'needs no', 'need none', 'not required', 'not need', 'do not need', 'does not need', 'exempt', 'nil', 'no debenture redemption reserve', 'no reserve'))),
           P('p3', 'Unlisted companies other than NBFCs/HFCs — DRR of 10% of outstanding debentures', 5, ALT('unlisted {v} {t}', 'unlisted {t}', v=('keep', 'keeps', 'maintain', 'create', 'must', 'need', 'needs', 'require', 'required'), t=('10', 'ten')), ALT('{t} {pc} outstanding', '{t} {pc} value', '{t} {pc} debentur', t=('10', 'ten'), pc=('percent', 'per cent', '')))], 'c3'),
        V('v3', 'What investment must be made in respect of debentures maturing during the year, and by when?',
          'On or before the thirtieth of April each year, the company must deposit or invest at least fifteen per cent of the debentures maturing during the year ending on the thirty-first of March of the next year. It can be in deposits with a scheduled bank free from charge or lien, unencumbered Central or State Government securities, or other unencumbered trust securities and notified bonds. The amount can be used only for redeeming those debentures and must never fall below fifteen per cent of the debentures maturing.',
          [P('p1', 'At least 15% of debentures maturing during the year', 4, '15|fifteen', 'matur|due|redeemed during|falling due', min=2),
           P('p2', 'On or before 30 April', 3, '30 april|april 30|thirtieth april|30th april|april', min=1),
           P('p3', 'In scheduled bank deposits (free of charge) or unencumbered government/trust securities', 2, 'scheduled bank|bank deposit|deposit|government securit|government|trust securit|unencumbered|bond', min=1),
           P('p4', 'Used only for redeeming those debentures', 1, 'only|solely|not for any other|not used for other|other purpose', min=1)], 'c4'),
        V('v4', 'Give the journal entries at the time of redemption of debentures out of a DRR set-up.',
          'First the DRR investment is encashed: Bank debited, DRR Investment credited. Then the amount due is recorded: Debentures debited, and Premium on Redemption debited if any, with Debenture Holders credited. Debenture Holders are then debited and Bank credited on payment. Finally the DRR, no longer needed, is transferred to general reserve: DRR debited, General Reserve credited.',
          [P('p1', 'Encash investments: Bank Dr, To DRR Investment', 2, 'investment', 'encash|realis|sold|sale|bank', min=2),
           P('p2', 'Debentures Dr (and premium), To Debenture Holders', 3, 'debentures debit|debenture account debit|debit debentures|debit debenture account|debenture debit', 'debenture holder|debentureholder'),
           P('p3', 'Debenture Holders Dr, To Bank (payment)', 2, 'pay|paid|payment|bank credit|credit bank', 'debenture holder|debentureholder', min=2),
           P('p4', 'DRR Dr, To General Reserve', 3, 'general reserve')], 'c5'),
        V('v5', 'What are the methods of redeeming debentures?',
          'Debentures can be redeemed by paying the whole amount in a lump sum at maturity or earlier, or by paying in instalments, for example a fixed portion every year by annual drawings. They can also be bought back from the open market and cancelled, which is useful when they quote below face value, though this is outside the Foundation syllabus. Under section 71(1), convertible debentures may be redeemed wholly or partly by conversion into shares.',
          [P('p1', 'Lump-sum payment at maturity', 3, 'lump sum|lumpsum|lump-sum|one lot|one go|single payment|whole amount|at once|full amount'),
           P('p2', 'Payment in instalments / annual drawings', 3, 'instal|drawing|in parts|yearly|annual|periodic|stages'),
           P('p3', 'Purchase in the open market (and cancellation)', 2, 'open market|market purchase|buy back|buyback|purchase from market|from the market|stock exchange'),
           P('p4', 'Conversion into shares', 2, 'convert|conversion')], 'c6'),
        V('v6', 'How is interest earned on DRR investment treated, and can the DRR investment be used for other purposes?',
          'Interest on DRR investment is received in bank and credited to Interest on DRR Investment Account, which is then transferred to the profit and loss account, because it is not reinvested. The investment itself cannot be used for any other purpose; it is kept only for redeeming the debentures maturing in the year, and its balance must not fall below fifteen per cent of those debentures.',
          [P('p1', 'Interest received is credited to profit and loss', 4, 'interest', 'profit loss|profit and loss|p l|statement of profit|income', min=2),
           P('p2', 'Investment cannot be used for any other purpose — only redemption', 4, ALT('{n} {u} {o}', 'only for redemption', 'only for redeeming', 'solely for redemption', 'only be used for redemption', 'only used for redemption', n=('not', 'cannot', 'can t', 'never'), u=('used', 'utilised', 'utilized', 'be used', 'be utilised', 'use'), o=('other', 'any other', 'for any other', 'other purpose'))),
           P('p3', 'Must not fall below 15% of debentures maturing', 2, '15|fifteen|not fall below 15|not fall below fifteen|never fall below 15|never fall below fifteen|not below 15|never below 15|not go below 15|not less than 15')], 'c4'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Nirav Textiles Ltd — getting ready to redeem', 'difficulty': 'hard',
        'case': ('Nirav Textiles Ltd is an unlisted company (not an NBFC or HFC). It has 10% debentures of ₹40,00,000, all maturing on 31 March 2028 at a premium of 4%. On 1 April 2027 '
                 'its DRR balance is ₹2,50,000. The premium on redemption was not provided earlier and is to be charged to profit and loss at redemption. The DRR investment is made '
                 'on 30 April 2027 in a scheduled bank deposit earning 7% a year, and is encashed with interest on 31 March 2028.'),
        'mcqs': [
            M('k1a', 'What additional amount must be transferred to DRR?', [R(150000), R(400000), R(250000), R(600000)], 0,
              "Nirav is unlisted and not an NBFC or HFC, so DRR must be 10% of outstanding debentures: 10% × 40,00,000 = ₹4,00,000. The DRR balance is ₹2,50,000, so additional transfer = 4,00,000 − 2,50,000 = ₹1,50,000, out of profits available for dividend. The trap ₹4,00,000 ignores the existing balance. In practice: auditors check that DRR reaches the required level before debentures are redeemed.", 'moderate', '4000000*10/100-250000') | {'topic': "Debenture Redemption Reserve"},
            M('k1b', 'What is the minimum amount to be deposited by 30 April 2027?', [R(600000), R(400000), R(4000000), R(160000)], 0,
              "The 15% deposit is on debentures maturing during the year ending 31 March 2028: 15% × 40,00,000 = ₹6,00,000, to be deposited by 30 April 2027. The trap ₹4,00,000 uses the 10% DRR rate instead of 15%. In practice: Nirav's finance team opens a fixed deposit with a scheduled bank, free of charge or lien, to meet this rule.", 'moderate', '4000000*15/100') | {'topic': "Debenture Redemption Reserve"},
            M('k1c', 'How much interest on the deposit is credited to profit and loss for 2027-28?', [R(38500), R(42000), R(28000), R(35000)], 0,
              "The deposit of ₹6,00,000 earns 7% from 1 May 2027 to 31 March 2028 (11 months): 6,00,000 × 7% × 11/12 = ₹38,500, credited to profit and loss. The trap ₹42,000 uses a full year's interest; ₹35,000 uses 10 months. In practice: banks credit interest on fixed deposits on maturity, and the company records it as other income.", 'hard', '600000*7/100*11/12') | {'topic': "Debenture Redemption Reserve"},
            M('k1d', 'After redemption, what amount is transferred from DRR to general reserve?', [R(400000), R(250000), R(150000), R(600000)], 0,
              "Once all debentures are redeemed, DRR is no longer needed. The full DRR of ₹4,00,000 (opening 2,50,000 + transfer 1,50,000) is transferred to general reserve. The trap ₹2,50,000 forgets the transfer made during the year; ₹1,50,000 is only the year's addition. In practice: transferring DRR to general reserve frees those profits for future dividends or business use.", 'core', '250000+150000') | {'topic': "Debenture Redemption Reserve"},
            M('k1e', 'How much is paid to debenture holders on 31 March 2028?', [R(4160000), R(4000000), R(4400000), R(4040000)], 0,
              "On redemption, debenture holders receive face value plus the 4% premium: 40,00,000 + 4% × 40,00,000 = 40,00,000 + 1,60,000 = ₹41,60,000. Interest for the year is paid separately. The trap ₹40,00,000 forgets the premium; ₹44,00,000 adds 10%, which is the interest rate, not the premium. In practice: the company pays redemption amounts through the debenture trustee or depository to all holders on the record date.", 'core', '4000000*104/100') | {'topic': "Redemption of Debentures"},
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch11', 'n': 6,
        'title': 'Redemption of Debentures',
        'outcomes': [
            'Explain the provisions of section 71 relating to convertible debentures, voting rights and the debenture redemption reserve.',
            'State when and how redeemable debentures may be redeemed.',
            'Apply Rule 18(7) (as amended in 2019) to decide whether a DRR is needed, how much, and the 15% investment or deposit by 30 April.',
            'Journalise DRR creation, investment, interest on investment, redemption (at par or premium) and transfer of DRR to general reserve.',
            'Account for redemption by lump-sum payment, by instalments and by conversion into shares.',
            'Prepare the related ledger accounts.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 60}, 'prereq': ['fnd-p1-ch11-u03'],
                 'exam_tip': 'In DRR problems first read the type of company. For an unlisted non-NBFC company: DRR = 10% of outstanding debentures; investment = 15% of debentures maturing in the year; DRR goes to general reserve after redemption.'},
        'concepts': [
            {'id': 'c1', 'title': 'Section 71 — the basic provisions',
             'body': ['A debenture is a company\'s written acknowledgement of a debt with terms for interest and repayment; where a charge is created, it is described in the instrument and must be registered with the Registrar. For mortgage debentures a debenture trustee is usually appointed.',
                      'Section 71(1): debentures may carry an option for conversion into shares, wholly or partly, at the time of redemption — but such an issue needs a special resolution in general meeting.',
                      'Section 71(2): no debenture may carry voting rights. Section 71(4): a DRR is to be created out of profits available for dividend, and its balance cannot be used except to redeem debentures.',
                      'If a company fails to redeem debentures on maturity or to pay interest when due, the Tribunal may, on application by any or all debenture holders or the debenture trustee and after hearing the parties, order immediate redemption with interest.'],
             'analogy': 'Section 71 is the rule book of a loan: it fixes what the lender can and cannot have (no votes), and makes the borrower save up for repayment.',
             'work': 'Debenture trustees review compliance with s. 71 and the trust deed every year; a missed redemption can lead to proceedings before the Tribunal.'},
            {'id': 'c2', 'title': 'Redemption of debentures and the purpose of DRR',
             'body': ['Redeemable debentures are repaid after a set number of years, at any time once a minimum period has passed, on giving notice, or by annual drawings. A company may also buy its debentures in the open market — attractive when they quote below face value — but this method is outside the Foundation syllabus.',
                      'A DRR is created out of profits available for dividend and is a part of reserves and surplus. Because those profits are kept back, the company accumulates resources to repay the debentures when due. The amount transferred each year is debited to profit and loss (Profit and Loss Dr, To DRR) and, in practice, matching investments are bought (DRR Investment Dr, To Bank).',
                      'At redemption, the investments are encashed and used to pay holders; the DRR, having served its purpose, is transferred to general reserve.'],
             'analogy': 'A DRR is like a "college fund" a parent builds year by year from savings, so the fee can be paid when it falls due.',
             'work': 'Auditors check that the DRR was created out of distributable profits and that it has not been used for anything other than redemption.'},
            {'id': 'c3', 'title': 'Adequacy of DRR — Rule 18(7) as amended in 2019',
             'body': ['All India Financial Institutions regulated by RBI and banking companies: no DRR, for public or privately placed debentures. Other financial institutions within s. 2(72): as applicable to NBFCs registered with RBI.',
                      'Listed companies: listed NBFCs (registered under s. 45-IA of the RBI Act), listed housing finance companies (registered with the National Housing Bank) and all other listed companies — no DRR, for public or privately placed debentures.',
                      'Unlisted companies: unlisted NBFCs and HFCs — no DRR for privately placed debentures; all other unlisted companies — DRR of 10% of the value of outstanding debentures.',
                      'For partly convertible debentures, DRR is created only for the non-convertible portion. The DRR may be created any time before redemption; for exams, create it right after allotment (or at the start of the year for which accounts are asked) if profits are sufficient.'],
             'analogy': 'Big regulated lenders and listed companies are trusted to manage repayment under their own regulators; smaller unlisted companies must keep a 10% "piggy bank".',
             'work': 'The first question an auditor asks about a debenture issue: listed or unlisted, and is the issuer an NBFC/HFC? The answer decides whether a DRR is required at all.'},
            {'id': 'c4', 'title': 'Investment or deposit of 15% — and interest on it',
             'body': ['Companies covered — all listed NBFCs, all listed HFCs, other listed companies (other than AIFIs, banks and other FIs) and unlisted companies that are not NBFCs or HFCs — must, on or before 30 April each year, deposit or invest at least 15% of the debentures maturing during the year ending 31 March of the next year.',
                      'Permitted forms: scheduled-bank deposits that carry no charge or lien; unencumbered Central or State Government securities; unencumbered securities in s. 20(a)–(d) and (ee) of the Indian Trusts Act, 1882; unencumbered bonds of a company notified under s. 20(f) of that Act.',
                      'The money can be used only to redeem the debentures maturing in that year, and the amount remaining must never fall below 15% of those debentures.',
                      'Interest received on DRR investment: Bank Dr, To Interest on DRR Investment; then Interest on DRR Investment Dr, To Profit and Loss (it is not reinvested, so it is not added to DRR).'],
             'analogy': 'Even listed companies, which need no DRR, must keep 15% of the coming year\'s repayment "parked" in a safe place by 30 April.',
             'work': 'Treasury teams diary the 30 April deadline every year and keep the deposit receipt or demat statement for the auditor.'},
            {'id': 'c5', 'title': 'Journal entries for DRR and redemption',
             'body': ['After allotment: (a) Profit and Loss Dr, To DRR (amount set aside); (b) DRR Investment Dr, To Bank (amount invested); (c) Bank Dr, To Interest on DRR Investment (interest received); (d) Interest on DRR Investment Dr, To Profit and Loss.',
                      'At redemption: (a) Bank Dr, To DRR Investment (encashment, with any profit or loss on realisation to profit and loss); (b) Debentures Dr [and Premium on Redemption of Debentures Dr], To Debenture Holders; (c) Debenture Holders Dr, To Bank; (d) DRR Dr, To General Reserve.',
                      'If the redemption premium was not provided at issue, it is charged to profit and loss at redemption: Profit and Loss Dr, To Premium on Redemption of Debentures.'],
             'analogy': 'Four steps on redemption day: break the piggy bank (encash), write the cheque amount (holders), pay it, then release the savings label (DRR → general reserve).',
             'work': 'A clean redemption file for audit contains the board resolution, DRR working, investment encashment proof, payment register and the satisfaction-of-charge filing with the Registrar.'},
            {'id': 'c6', 'title': 'Methods of redemption — lump sum, instalments, conversion',
             'body': ['Lump sum: the whole issue is repaid in one lot at maturity (or earlier if the terms allow).',
                      'Instalments: a specified portion is repaid at specified intervals, often by drawing lots; the 15% investment is worked out each year on the instalment maturing that year.',
                      'Conversion: holders of convertible debentures receive shares instead of cash for the convertible part. Redemption value of the debentures converted ÷ issue price of a share = number of shares; the balance is paid in cash. Entry: Debenture Holders Dr, To Equity Share Capital, To Securities Premium.',
                      'Open-market purchase and cancellation of own debentures is excluded from the Foundation syllabus.'],
             'analogy': 'Lump sum = repaying a loan in one shot; instalments = EMIs; conversion = settling the loan by handing over part-ownership.',
             'work': 'For convertible issues, the registrar computes shares on conversion and fractional entitlements; the company\'s accountant verifies the arithmetic before allotment.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Lump-sum redemption at a premium (unlisted company)', 'difficulty': 'moderate', 'minutes': 15,
             'q': 'Ganga Steels Ltd, an unlisted company (not an NBFC/HFC), has 20,000 8% debentures of ₹100 each due for redemption in one lot on 31 March 2028 at a 5% premium (the premium was provided at the time of issue). On 1 April 2027 the DRR balance is ₹1,20,000. On 30 April 2027 the required investment is made in a scheduled bank deposit at 6% p.a.; it is encashed with interest on 31 March 2028 and the debentures are redeemed. Journalise for 2027-28 (ignore debenture interest).',
             'solution': [journal(E1, 'Journal of Ganga Steels Ltd', 'j1'),
                          wn('Workings', f'DRR required = 10% × ₹{inr(deb)} = ₹{inr(need)}; existing ₹1,20,000; transfer ₹{inr(top)}. Investment = 15% × ₹{inr(deb)} = ₹{inr(inv)}. Interest = {inr(inv)} × 6% × 11/12 = ₹{inr(intr)}. Payment = ₹{inr(pay)}.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Redemption by yearly instalments — DRR and investment schedule', 'difficulty': 'moderate', 'minutes': 12,
             'q': 'Prakash Ltd (unlisted, not an NBFC/HFC) issued ₹30,00,000 10% debentures on 1 April 2026, redeemable at par in three equal instalments on 31 March 2028, 2029 and 2030. The company creates the required DRR immediately. Prepare the investment schedule and journalise the DRR creation and the first instalment (investments in Central Government securities realised at par).',
             'solution': [wn('DRR', f'10% of outstanding debentures at issue = ₹{inr(drr2)}.'), sch, journal(E2, 'Journal of Prakash Ltd (selected entries)', 'j2'),
                          note('The 15% investment is worked out each year only on the debentures maturing in the following year. Once all debentures are redeemed, the DRR is transferred to general reserve.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Redemption with an option to convert', 'difficulty': 'moderate', 'minutes': 10,
             'q': 'Hira Ltd has 2,000 9% convertible debentures of ₹100 each, redeemable at a 10% premium. At redemption, holders may convert 30% of their holding into equity shares of ₹10 each at ₹25 per share and take the rest in cash. Holders of debentures worth ₹50,000 opt for conversion. Compute the shares issued and cash paid to them, and journalise (premium provided at issue).',
             'solution': [wn('Working', f'Debentures of those opting = 50,000 ÷ 100 = {inr(opted)}. Converted = 30% × 500 = {inr(conv)}; redemption value = 150 × ₹110 = ₹{inr(rv_conv)}; shares = 16,500 ÷ 25 = {inr(shares)}. Cash for 350 debentures × ₹110 = ₹{inr(cashd)}.'),
                          journal(E3, 'Journal of Hira Ltd', 'j3')],
             'checks': c3},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Annual DRR and investment compliance check', 'role': 'Statutory auditor of an unlisted manufacturing company',
             'situation': 'The company has two debenture series: Series A ₹50 lakh (unlisted, maturing 31 March 2028) and Series B ₹1.2 crore, 30% convertible, maturing in 2030. DRR in the books is ₹10 lakh. No deposit was made by 30 April 2027.',
             'steps': ['DRR required: Series A 10% × ₹50 lakh = ₹5 lakh; Series B only on the non-convertible 70% = 10% × ₹84 lakh = ₹8.4 lakh; total ₹13.4 lakh.',
                       'Shortfall in DRR = ₹13.4 lakh − ₹10 lakh = ₹3.4 lakh, subject to availability of distributable profits.',
                       'Investment by 30 April 2027: 15% of debentures maturing in 2027-28 = 15% × ₹50 lakh = ₹7.5 lakh — not made: non-compliance.',
                       'Discuss with management; recommend immediate deposit and the DRR transfer.',
                       'Report the non-compliance as required.'],
             'takeaway': 'DRR (10% of outstanding, non-convertible part) and the 15% deposit are separate tests with separate deadlines.',
             'checks': [{'expr': '5000000*10/100+12000000*70/100*10/100', 'value': 1340000, 'label': 'Total DRR required'}, {'expr': '5000000*15/100', 'value': 750000, 'label': 'Deposit required by 30 April'}]},
            {'id': 'j2', 'title': 'Redemption-day checklist', 'role': 'Treasury executive',
             'situation': 'A ₹25 crore debenture series of your listed company matures next week. As a listed company it has no DRR, but it made the 15% deposit on 30 April.',
             'steps': ['Break the deposit (15% × ₹25 crore = ₹3.75 crore) and arrange the balance funds.',
                       'Get the list of holders on the record date from the registrar.',
                       'Pass entries: Bank Dr, To DRR Investment; Debentures Dr, To Debenture Holders; Debenture Holders Dr, To Bank.',
                       'File satisfaction of charge with the Registrar and inform the stock exchange and debenture trustee.',
                       'No DRR transfer is needed since none was required for a listed company.'],
             'takeaway': 'Listed companies skip the DRR but not the 15% deposit.',
             'checks': [{'expr': '25*15/100', 'value': 3.75, 'label': 'Deposit (₹ crore)'}]},
        ],
        'mcqs': [
            mcq('m1', 'Under section 71(2), debentures:', ['Cannot carry voting rights', 'Carry one vote per debenture', 'Carry votes only if secured', 'Carry votes if interest is in arrears for two years'], 0, "Section 71(2) of the Companies Act, 2013 states plainly that no company shall issue debentures carrying voting rights. Debenture holders are creditors, not owners, so they have no say in general meetings whatever happens to interest payments. The trap 'votes if interest is in arrears for two years' borrows a rule that applies to preference shareholders' dividends. In practice: debenture holders protect themselves through a debenture trustee and security, not through votes.", 'c1') | {'topic': "Introduction"},
            mcq('m2', 'Issue of debentures with an option to convert them into shares requires:', ['A special resolution in general meeting', 'Only a board resolution', 'Approval of the Tribunal', 'An ordinary resolution'], 0, "Section 71(1) allows a company to issue debentures with an option to convert them wholly or partly into shares, but only if approved by a special resolution passed at a general meeting. A board resolution alone is not enough — that is the trap — because conversion can dilute existing shareholders. In practice: companies issuing compulsorily or optionally convertible debentures to investors first pass a special resolution and file it with the ROC.", 'c1') | {'topic': "Introduction"},
            mcq('m3', 'For an unlisted company (other than NBFC/HFC), DRR must be:', ['10% of the value of outstanding debentures', '25% of the value of outstanding debentures', '15% of debentures maturing in the year', 'Not required'], 0, "Under Rule 18(7) of the 2014 Rules on share capital and debentures, as amended in 2019, unlisted companies other than NBFCs and HFCs must maintain DRR of at least 10% of the value of outstanding debentures. The trap 25% was the earlier rate under the pre-2019 rule. Listed companies, NBFCs and HFCs need no DRR now. In practice: auditors of unlisted companies with debentures check this 10% DRR every year.", 'c3') | {'topic': "Debenture Redemption Reserve"},
            mcq('m4', 'A listed company (not an NBFC) issues debentures to the public. DRR required is:', ['Nil', '10% of outstanding debentures', '25% of outstanding debentures', '50% of the issue'], 0, "After the 2019 amendment to Rule 18(7), listed companies (and NBFCs and HFCs, whether listed or not) are not required to create DRR at all. They must still make the 15% deposit or investment for debentures maturing in the year. The trap 25% reflects the old rule before 2019. In practice: the relaxation was meant to make bond issues by listed companies easier, though investor protection continues through trustees and SEBI regulations.", 'c3', 'moderate') | {'topic': "Debenture Redemption Reserve"},
            mcq('m5', 'The 15% investment or deposit must be made on or before:', ['The last day of April each year', 'The last day of March each year', 'The last day of September each year', 'The date of redemption'], 0, "Rule 18(7)(c) requires the company to invest or deposit at least 15% of the debentures maturing during the year ending on the next 31 March, on or before 30 April each year. The trap 'last day of March' confuses the deposit deadline with the financial year end. In practice: finance teams set reminders for 30 April each year so that the deposit for debentures maturing in that year is made on time.", 'c4') | {'topic': "Debenture Redemption Reserve"},
            mcq('m6', 'Debentures of ₹60,00,000 mature on 31 March 2028. The minimum deposit by 30 April 2027 is:', ['₹9,00,000', '₹6,00,000', '₹15,00,000', '₹12,00,000'], 0, "The 15% deposit is calculated on debentures maturing during the year ending next 31 March. Debentures of ₹60,00,000 mature on 31 March 2028, so by 30 April 2027 the company must deposit at least 15% × 60,00,000 = ₹9,00,000. The trap ₹6,00,000 uses 10%, the DRR rate, instead of 15%. In practice: banks often hold such deposits in a separate account, free of any charge or lien.", 'c4', 'core', '6000000*15/100') | {'topic': "Debenture Redemption Reserve"},
            mcq('m7', 'An unlisted company has ₹24,00,000 debentures of which 40% are convertible. DRR required is:', ['₹1,44,000', '₹2,40,000', '₹96,000', '₹3,60,000'], 0, "DRR is needed only on non-convertible debentures, because convertible ones are settled by issuing shares, not cash. Non-convertible portion = 60% × 24,00,000 = ₹14,40,000. DRR = 10% × 14,40,000 = ₹1,44,000. The trap ₹2,40,000 applies 10% to all debentures, including convertible ones. In practice: companies issuing compulsorily convertible debentures to investors avoid DRR because no cash redemption is expected.", 'c3', 'moderate', '2400000*60/100*10/100') | {'topic': "Debenture Redemption Reserve"},
            mcq('m8', 'Interest received on DRR investment (not reinvested) is credited to:', ['Profit and loss account', 'Debenture Redemption Reserve', 'General reserve', 'Debentures account'], 0, "Following the study material, interest earned on the DRR investment, when received and not reinvested, is income of the company and is credited to profit and loss. The trap 'credited to DRR' confuses the deposit's income with the reserve itself — DRR is built only by appropriating profits. In practice: companies show interest on such deposits as other income in their statement of profit and loss.", 'c4') | {'topic': "Debenture Redemption Reserve"},
            mcq('m9', 'After all debentures are redeemed, the DRR balance is:', ['Transferred to general reserve', 'Transferred to capital reserve', 'Credited to profit and loss as income', 'Retained permanently'], 0, "Once all debentures are redeemed, the purpose of DRR is over. The entry is DRR A/c Dr, To General Reserve A/c, so the balance returns to a free reserve. It becomes free reserve again because it was created out of profits. The trap 'capital reserve' is for capital profits like gains on re-issue of forfeited shares. In practice: after redeeming its bonds, a company's general reserve increases by the DRR balance, which may later support dividends.", 'c5') | {'topic': "Debenture Redemption Reserve"},
            mcq('m10', 'DRR balance ₹1,80,000; outstanding debentures ₹25,00,000 of an unlisted manufacturing company. The amount to be transferred to DRR before redemption is:', ['₹70,000', '₹2,50,000', '₹1,80,000', '₹3,75,000'], 0, "Required DRR for an unlisted manufacturing company = 10% × 25,00,000 = ₹2,50,000. The existing balance is ₹1,80,000, so the additional transfer = 2,50,000 − 1,80,000 = ₹70,000. The trap ₹2,50,000 ignores the balance already in DRR; ₹3,75,000 uses 15%, the deposit rate. In practice: companies top up DRR each year out of profits available for dividend until the required level is reached.", 'c3', 'moderate', '2500000*10/100-180000') | {'topic': "Debenture Redemption Reserve"},
            mcq('m11', '400 debentures of ₹100, redeemable at ₹105, are converted into equity shares of ₹10 each issued at ₹21. Number of shares:', ['2,000', '1,905', '4,200', '2,100'], 0, "Redemption value = 400 × ₹105 = ₹42,000. Shares are issued at ₹21 each, so number of shares = 42,000 ÷ 21 = 2,000. The trap 1,905 uses face value ₹100 per debenture and wrongly divides 40,000 by 21; 4,200 divides by the face value of shares (₹10). In practice: when convertible debentures are converted, the company's share capital and securities premium rise and debt falls.", 'c6', 'moderate', '400*105/21') | {'topic': "Methods of Redemption of Debentures"},
            mcq('m12', 'Which of these is NOT a permitted form of the 15% investment?', ['Shares of a listed company', 'Deposit with a scheduled bank free of charge or lien', 'Unencumbered Central Government securities', 'Unencumbered State Government securities'], 0, "Rule 18(7)(c) allows the 15% to be kept in a deposit with a scheduled bank (free of any charge or lien), unencumbered Central or State Government securities, unencumbered securities under the Indian Trusts Act, or unencumbered bonds of companies notified under that Act. Shares of a listed company are not among these. The trap 'deposit with a scheduled bank' is allowed only if it is free of charge or lien. In practice: most companies use fixed deposits with banks for simplicity.", 'c4') | {'topic': "Debenture Redemption Reserve"},
            mcq('m13', 'Which method of redemption is excluded from the Foundation syllabus?', ['Purchase of own debentures in the open market', 'Payment in a lump sum', 'Payment in instalments', 'Conversion into shares'], 0, "At Foundation level, the methods covered are payment in a lump sum, payment in instalments and conversion into shares. Purchase of own debentures in the open market has been specifically excluded from the Foundation syllabus. The trap is 'conversion into shares', which is covered. In practice: companies do buy back their listed bonds in the market, but students meet that method only at later CA levels.", 'c6') | {'topic': "Methods of Redemption of Debentures"},
        ],
        'questions': [
            {'id': 'q1', 'marks': 8, 'minutes': minutes(8), 'difficulty': 'hard', 'pad': 'ledger',
             'q': 'On 1 April 2026 the books of Sagar Ltd (unlisted, not an NBFC/HFC) show: 11% debentures ₹9,00,000 (redeemable at a premium of 5% on 31 March 2027); DRR ₹40,000; DRR investment ₹1,35,000 in 8% Government bonds. The required transfer to DRR is made on 1 April 2026. On 31 March 2027 the bank balance before interest is ₹8,40,000; the investments are realised at par with a year\'s interest, and the debentures are redeemed. The premium on redemption had been provided at issue. Prepare the Debentures, DRR, DRR Investment, Debenture Holders and Bank accounts (ignore debenture interest).',
             'model': Lq1 + [wn('Workings', f'DRR required = 10% × 9,00,000 = ₹{inr(q1_req)}; transfer ₹{inr(q1_top)}. Interest on investment = 1,35,000 × 8% = ₹{inr(q1_int)}. Payable = 9,00,000 + 45,000 = ₹{inr(q1_pay)}. Closing bank = ₹{inr(q1_bank)}.')],
             'checks': q1c,
             'scheme': [S('s1', 'Debentures account closed by transfer to debenture holders', 1, 'posting'),
                        S('s2', 'DRR topped up to ₹90,000 by ₹50,000 from profit and loss', 1.5, 'computation'),
                        S('s3', 'DRR transferred to general reserve ₹90,000', 1, 'concept'),
                        S('s4', 'DRR investment realised ₹1,35,000', 1, 'posting'),
                        S('s5', 'Debenture holders: ₹9,00,000 + premium ₹45,000 = ₹9,45,000 paid', 1.5, 'computation'),
                        S('s6', 'Bank: interest ₹10,800; closing balance ₹40,800', 2, 'balancing')],
             'remarks': ['Many candidates forget to bring the DRR to 10% before redemption.', 'Some credit interest on investment to DRR; the material takes it to profit and loss.'],
             'mistakes': ['Transferring only ₹40,000 to general reserve.', 'Paying holders ₹9,00,000 without the premium.'],
             'tips': ['Prepare the Debenture Holders account first; it gives the payment for the bank account.', 'Write "By/To" correctly and date every posting.']},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'text',
             'q': 'Explain the requirements regarding (a) creation of debenture redemption reserve and (b) investment or deposit of funds in respect of debentures maturing during the year, under Rule 18(7) as amended in 2019.',
             'model': [p('(a) DRR is created out of profits available for dividend. No DRR is required for AIFIs regulated by RBI and banking companies; for all listed companies (including listed NBFCs and HFCs); and for unlisted NBFCs and HFCs on privately placed debentures. Other financial institutions follow the NBFC rule. Other unlisted companies must maintain DRR of 10% of the value of outstanding debentures. For partly convertible debentures, DRR is only on the non-convertible part. DRR can be used only for redemption of debentures.'),
                       p('(b) Listed NBFCs, listed HFCs, other listed companies and unlisted companies other than NBFCs/HFCs must, on or before 30 April each year, deposit or invest at least 15% of the debentures maturing during the year ending 31 March of the next year — in scheduled bank deposits free of charge or lien, unencumbered Central/State Government securities, unencumbered trust securities under s. 20 of the Indian Trusts Act or notified bonds. The amount may be used only for redeeming those debentures and must never fall below 15% of them.')],
             'scheme': [S('s1', 'DRR out of profits available for dividend; use restricted', 1, 'provision'), S('s2', 'Exempt categories (AIFIs/banks, listed, unlisted NBFC/HFC private placement)', 1.5, 'provision'),
                        S('s3', '10% of outstanding for other unlisted companies', 1, 'provision'), S('s4', '15% investment by 30 April, permitted forms and use', 1.5, 'provision')],
             'remarks': ['Answers based on the old 25% DRR rule earn nothing — the 2019 amendment changed it.'],
             'mistakes': ['Saying listed companies must keep 10% DRR.', 'Saying the 15% deposit is calculated on all outstanding debentures.'],
             'tips': ['Answer (a) as a small table: category → DRR.']},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'journal',
             'q': 'Laxmi Ltd\'s 10% convertible debentures of ₹100 each are redeemable at a premium of 4%. Holders may convert 25% of their holding into equity shares of ₹10 each at ₹40 per share. Holders of debentures of ₹80,000 opt to convert. Calculate the number of shares and cash payable to them, and pass journal entries (premium provided at issue).',
             'model': [wn('Working', f'Debentures = 80,000 ÷ 100 = {inr(q3_n)}; converted 25% = {inr(q3_c)}; redemption value = 200 × ₹104 = ₹{inr(q3_v)}; shares = 20,800 ÷ 40 = {inr(q3_s)}. Cash for 600 × ₹104 = ₹{inr(q3_cash)}.'),
                       journal([je('(1)', [('10% Convertible Debentures A/c', 80000), ('Premium on Redemption of Debentures A/c', 3200)], [('Debenture Holders A/c', 83200)], 'Being amount due on redemption of 800 debentures at 4% premium'),
                                je('(2)', [('Debenture Holders A/c', q3_v)], [('Equity Share Capital A/c', 5200), ('Securities Premium A/c', 15600)], 'Being 520 equity shares of ₹10 issued at ₹40 on conversion'),
                                je('(3)', [('Debenture Holders A/c', q3_cash)], [('Bank A/c', q3_cash)], 'Being cash paid for 600 debentures')], 'Journal of Laxmi Ltd', 'jq3')],
             'checks': q3c,
             'scheme': [S('s1', 'Shares 520 computed on redemption value', 1.5, 'computation'), S('s2', 'Cash ₹62,400', 0.5, 'computation'), S('s3', 'Entries with correct split of capital and premium', 2, 'posting')],
             'remarks': ['A frequent error is converting at face value (₹100) instead of redemption value (₹104).'],
             'mistakes': ['Crediting share capital with ₹20,800.', 'Converting 25% of all debentures instead of only those who opted.'],
             'tips': ['Compute shares from redemption value ÷ issue price per share.']},
            {'id': 'q4', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'journal',
             'q': 'Vayu Ltd (unlisted, not an NBFC/HFC) issued ₹15,00,000 9% debentures on 1 April 2026, redeemable at par on 31 March 2028. Pass journal entries for (i) creation of DRR on 1 April 2026, (ii) the deposit required on 30 April 2027, (iii) encashment of the deposit and redemption on 31 March 2028, and (iv) the transfer of DRR afterwards. Ignore interest.',
             'model': [journal([je('2026 Apr 1', [('Profit and Loss A/c', 150000)], [('Debenture Redemption Reserve A/c', 150000)], 'Being DRR created at 10% of outstanding debentures'),
                                je('2027 Apr 30', [('DRR Investment A/c', 225000)], [('Bank A/c', 225000)], 'Being 15% of debentures maturing in 2027-28 deposited with a scheduled bank'),
                                je('2028 Mar 31', [('Bank A/c', 225000)], [('DRR Investment A/c', 225000)], 'Being deposit encashed'),
                                je('2028 Mar 31', [('9% Debentures A/c', 1500000)], [('Debenture Holders A/c', 1500000)], 'Being debentures due for redemption'),
                                je('2028 Mar 31', [('Debenture Holders A/c', 1500000)], [('Bank A/c', 1500000)], 'Being debenture holders paid'),
                                je('2028 Mar 31', [('Debenture Redemption Reserve A/c', 150000)], [('General Reserve A/c', 150000)], 'Being DRR transferred to general reserve')], 'Journal of Vayu Ltd', 'jq4')],
             'checks': [{'expr': '1500000*10/100', 'value': 150000, 'label': 'DRR'}, {'expr': '1500000*15/100', 'value': 225000, 'label': 'Deposit'}],
             'scheme': [S('s1', 'DRR ₹1,50,000 out of profit and loss', 1, 'computation'), S('s2', 'Deposit ₹2,25,000 by 30 April 2027', 1, 'computation'),
                        S('s3', 'Encashment and redemption entries', 1.5, 'posting'), S('s4', 'DRR to general reserve', 1, 'concept'), S('s5', 'Dates and narrations', 0.5, 'presentation')],
             'remarks': ['Some candidates create DRR at 25% (old rule) or invest 15% on 1 April 2026 itself for debentures maturing two years later — the deposit relates to debentures maturing in the following year.'],
             'mistakes': ['Debiting DRR investment to DRR account.', 'Leaving DRR in the books after redemption.'],
             'tips': ['Keep DRR (reserve) and DRR investment (asset) clearly separate.']},
        ],
        'viva': viva,
        'cases': cases,
        'revision': {
            'summary': ['s. 71(1) convertible debentures need a special resolution; s. 71(2) no voting rights; s. 71(4) DRR out of profits available for dividend, used only for redemption.',
                        'DRR (Rule 18(7), 2019): nil for AIFIs/banks, listed companies (incl. NBFCs/HFCs) and unlisted NBFC/HFC private placements; 10% of outstanding debentures for other unlisted companies; only on non-convertible part.',
                        'Deposit/investment: ≥15% of debentures maturing in the next year ending 31 March, by 30 April, in bank deposits or unencumbered government/trust securities; never below 15%.',
                        'Entries: P&L Dr To DRR; DRRI Dr To Bank; interest to P&L; at redemption encash, pay holders, DRR → general reserve.',
                        'Methods: lump sum, instalments, conversion (open-market purchase excluded at Foundation).'],
            'remember': ['DRR is a reserve (equity); DRR investment is an asset.', 'Listed companies need no DRR but must still make the 15% deposit.', 'Conversion: shares = redemption value of debentures converted ÷ issue price.'],
            'traps': ['Using the old 25% DRR rule.', 'Computing the 15% deposit on all outstanding debentures instead of those maturing next year.', 'Crediting interest on DRR investment to DRR.', 'Forgetting to transfer DRR to general reserve after redemption.'],
        },
        'quickref': [
            {'k': 's. 71(1), (2), (4)', 'v': 'Conversion option needs special resolution; no voting rights; DRR out of distributable profits, used only for redemption'},
            {'k': 'DRR — unlisted (non-NBFC/HFC)', 'v': '10% of value of outstanding debentures (non-convertible portion)'},
            {'k': 'DRR — not required', 'v': 'AIFIs and banks; listed companies incl. listed NBFCs/HFCs; unlisted NBFCs/HFCs (private placement)'},
            {'k': '15% deposit', 'v': 'By 30 April: ≥15% of debentures maturing in the year ending next 31 March'},
            {'k': 'Interest on DRRI', 'v': 'Bank Dr To Interest on DRRI; Interest on DRRI Dr To P&L'},
            {'k': 'Redemption entries', 'v': 'Bank Dr To DRRI; Debentures Dr (+ Premium on Redemption Dr) To Debenture Holders; Debenture Holders Dr To Bank; DRR Dr To General Reserve'},
            {'k': 'Conversion', 'v': 'Shares = redemption value of debentures converted ÷ issue price per share'},
        ],
    }


# ---- offline auto-check: kw/min (viva matcher), nums (figures that must appear), rows ([account, side, amount]) ----
AUTO = {
    'q1': {'extra_ok': False,
           's1': {'rows': [['debenture holder|debentureholder|holders', 'dr', 900000]]},
           's2': {'nums': [90000], 'rows': [['profit|p l|surplus', 'cr', 50000]]},
           's3': {'rows': [['general reserve', 'dr', 90000]]},
           's4': {'rows': [['investment|bond', 'dr', 135000]]},
           's5': {'nums': [45000, 945000]},
           's6': {'nums': [10800, 40800]}},
    'q2': {'extra_ok': True,
           's1': {'kw': ['profits available for dividend|profit available dividend|out of profits|profits|profit', 'only for redemption|only redemption|used only|not for any other|solely|only purpose'], 'min': 2},
           's2': {'kw': ['aifi|all india financial|banking compan|bank', 'listed', 'nbfc|hfc|housing finance|privately placed|private placement'], 'min': 3},
           's3': {'kw': ['10 percent|10 per cent|10', 'outstanding|unlisted'], 'min': 2},
           's4': {'kw': ['15 percent|15 per cent|15', '30 april|april 30|30th april|30 apr', 'scheduled bank|government securities|trust securities|deposit|invest|bonds'], 'min': 3}},
    'q3': {'extra_ok': False,
           's1': {'nums': [520],
                  'wrong': [{'kw': ['500 shares|500 equity'], 'say': 'Shares are issued for the redemption value (₹104 per debenture): 200 × ₹104 ÷ ₹40 = 520 shares.'}]},
           's2': {'nums': [62400]},
           's3': {'rows': [['debenture holder|debentureholder|holders', 'dr', 20800], ['capital', 'cr', 5200], ['premium', 'cr', 15600]]}},
    'q4': {'extra_ok': False,
           's1': {'rows': [['profit|p l|surplus', 'dr', 150000], ['redemption reserve|drr', 'cr', 150000]]},
           's2': {'rows': [['investment|deposit', 'dr', 225000], ['bank', 'cr', 225000]]},
           's3': {'rows': [['bank', 'dr', 225000], ['investment|deposit', 'cr', 225000], ['debenture', 'dr', 1500000], ['bank', 'cr', 1500000]]},
           's4': {'rows': [['redemption reserve|drr', 'dr', 150000], ['general reserve', 'cr', 150000]]},
           's5': {'kw': ['30 april|april 30|apr 30|30 apr|30 04', '31 march|march 31|mar 31|31 mar|31 03'], 'min': 2}},
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
