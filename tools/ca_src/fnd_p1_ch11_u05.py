"""CA Foundation · Paper 1 Accounting · Chapter 11 Company Accounts · Unit 5 Redemption of Preference Shares.
Original explanations, names and numbers (structure and scope follow the ICAI study material).
Convention used (as in the study material): companies are taken to follow the accounting standards under s. 133,
so premium on redemption is written off out of profits, not out of securities premium."""
from lib import *
from ca_viva import P, ALT, V
from ca_cases import M

UID = 'fnd-p1-ch11-u05'


def mcq(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check: d['check'] = check
    return d


def S(sid, pt, m, skill): return {'id': sid, 'pt': pt, 'm': m, 'skill': skill}


def build():
    # ---------------- Illustration 1: wholly out of profits ----------------
    c1 = Checks()
    pv = c1.add('20000*100', 'Preference capital: 20,000 × ₹100')
    pr = c1.add('2000000*5/100', 'Premium on redemption @5%')
    pay = c1.add('2000000+100000', 'Amount payable')
    c1.add('2500000-2100000', 'Bank left')
    c1.add('3000000-2000000', 'General reserve left')
    c1.add('600000-100000', 'Surplus left after writing off premium')
    E1 = [
        je('Mar 31', [('9% Preference Share Capital A/c', pv), ('Premium on Redemption of Preference Shares A/c', pr)], [('Preference Shareholders A/c', pay)], 'Being amount due on redemption of 20,000 preference shares at 5% premium'),
        je('Mar 31', [('Profit and Loss A/c (Surplus)', pr)], [('Premium on Redemption of Preference Shares A/c', pr)], 'Being premium on redemption written off out of profits'),
        je('Mar 31', [('General Reserve A/c', pv)], [('Capital Redemption Reserve A/c', pv)], 'Being nominal value of shares redeemed out of profits transferred to CRR as required by s. 55'),
        je('Mar 31', [('Preference Shareholders A/c', pay)], [('Bank A/c', pay)], 'Being preference shareholders paid'),
    ]

    # ---------------- Illustration 2: combination, minimum fresh issue at a premium ----------------
    c2 = Checks()
    avail = c2.add('240000-40000', 'General reserve available (₹40,000 to be retained)')
    minp = c2.add('500000-200000', 'Minimum proceeds (face value) needed from fresh issue')
    nsh = c2.add('300000/10', 'Minimum number of equity shares (face value ₹10)')
    cash2 = c2.add('30000*12', 'Cash from fresh issue @ ₹12')
    pr2 = c2.add('500000*10/100', 'Premium on redemption @10%')
    pay2 = c2.add('500000+50000', 'Amount payable')
    c2.add('200000+360000-550000', 'Bank left = opening ₹2,00,000 + issue − payment')
    E2 = [
        je('(1)', [('Bank A/c', cash2)], [('Equity Share Capital A/c', minp), ('Securities Premium A/c', 60000)], 'Being 30,000 equity shares of ₹10 issued at ₹12 for the purpose of redemption'),
        je('(2)', [('10% Preference Share Capital A/c', 500000), ('Premium on Redemption of Preference Shares A/c', pr2)], [('Preference Shareholders A/c', pay2)], 'Being amount due on redemption at 10% premium'),
        je('(3)', [('Profit and Loss A/c (Surplus)', pr2)], [('Premium on Redemption of Preference Shares A/c', pr2)], 'Being premium on redemption written off out of profits'),
        je('(4)', [('General Reserve A/c', avail)], [('Capital Redemption Reserve A/c', avail)], 'Being transfer to CRR: ₹5,00,000 redeemed less ₹3,00,000 face value of fresh issue'),
        je('(5)', [('Preference Shareholders A/c', pay2)], [('Bank A/c', pay2)], 'Being payment to preference shareholders'),
    ]

    # ---------------- Illustration 3: two tests for minimum fresh issue + sale of investments ----------------
    c3 = Checks()
    t1 = c3.add('(800000-550000)/10', 'Test 1 (s. 55): shares needed = (8,00,000 − 5,50,000) ÷ face value ₹10')
    funds = c3.add('150000+220000', 'Funds available = bank + sale of investments')
    short = c3.add('800000-370000', 'Shortfall of funds')
    t2 = c3.add('430000/12', 'Test 2 (funds): shares = shortfall ÷ issue price ₹12')
    n3 = 35900
    cap3 = c3.add('35900*10', 'Equity share capital issued')
    prem3 = c3.add('35900*2', 'Securities premium')
    cash3 = c3.add('35900*12', 'Cash raised')
    crr3 = c3.add('800000-359000', 'CRR = redeemed − face value of fresh issue')
    c3.add('150000+220000+430800-800000', 'Bank left')
    gain3 = c3.add('220000-200000', 'Profit on sale of investments')
    E3 = [
        je('(1)', [('Bank A/c', 220000)], [('Investments A/c', 200000), ('Profit and Loss A/c', gain3)], 'Being investments sold at a profit to provide funds for redemption'),
        je('(2)', [('Bank A/c', cash3)], [('Equity Share Capital A/c', cap3), ('Securities Premium A/c', prem3)], 'Being 35,900 equity shares of ₹10 issued at ₹12'),
        je('(3)', [('8% Preference Share Capital A/c', 800000)], [('Preference Shareholders A/c', 800000)], 'Being amount due on redemption at par'),
        je('(4)', [('General Reserve A/c', crr3)], [('Capital Redemption Reserve A/c', crr3)], 'Being transfer to CRR for the part not covered by fresh issue'),
        je('(5)', [('Preference Shareholders A/c', 800000)], [('Bank A/c', 800000)], 'Being preference shareholders paid'),
    ]

    # ---------------- Illustration 4: partly called and partly paid shares ----------------
    c4 = Checks()
    fcall = c4.add('30000*20', 'Final call ₹20 on 30,000 shares')
    recd = c4.add('29000*20', 'Final call received on 29,000 shares')
    arr = c4.add('1000*20', 'Calls in arrears on 1,000 shares')
    forf = c4.add('1000*100-20000', 'Forfeited amount (₹80 paid on 1,000 shares)')
    red = c4.add('29000*100', 'Shares redeemed: 29,000 × ₹100')
    crr4 = c4.add('2900000-1000000', 'CRR = redeemed − fresh issue')
    E4 = [
        je('(1)', [('8% Preference Share Final Call A/c', fcall)], [('8% Preference Share Capital A/c', fcall)], 'Being final call of ₹20 made to make the shares fully paid before redemption'),
        je('(2)', [('Bank A/c', recd), ('Calls in Arrears A/c', arr)], [('8% Preference Share Final Call A/c', fcall)], 'Being final call received except on 1,000 shares'),
        je('(3)', [('8% Preference Share Capital A/c', 100000)], [('Calls in Arrears A/c', arr), ('Forfeited Shares A/c', forf)], 'Being 1,000 preference shares forfeited for non-payment of final call'),
        je('(4)', [('Forfeited Shares A/c', forf)], [('Capital Reserve A/c', forf)], 'Being forfeited amount transferred to capital reserve as the shares will not be re-issued'),
        je('(5)', [('Bank A/c', 1000000)], [('Equity Share Capital A/c', 1000000)], 'Being 1,00,000 equity shares of ₹10 issued at par for redemption'),
        je('(6)', [('8% Preference Share Capital A/c', red)], [('Preference Shareholders A/c', red)], 'Being amount due on redemption of 29,000 fully paid preference shares at par'),
        je('(7)', [('General Reserve A/c', crr4)], [('Capital Redemption Reserve A/c', crr4)], 'Being transfer to CRR'),
        je('(8)', [('Preference Shareholders A/c', red)], [('Bank A/c', red)], 'Being preference shareholders paid'),
    ]

    # ---------------- Question 1 model: Om Chemicals Ltd ----------------
    q1c = Checks()
    q1_cash_iss = q1c.add('15000*12', 'Fresh issue: 15,000 × ₹12')
    q1_prem = q1c.add('400000*10/100', 'Premium on redemption 10%')
    q1_pay = q1c.add('400000+40000', 'Payable to preference shareholders')
    q1_crr = q1c.add('400000-150000', 'CRR = redeemed − face value of fresh issue')
    q1_gain = q1c.add('270000-250000', 'Profit on sale of investments')
    q1_bank = q1c.add('150000+270000+180000-440000', 'Closing bank')
    q1_pl = q1c.add('80000+20000-40000', 'Closing surplus')
    q1_gr = q1c.add('320000-250000', 'Closing general reserve')
    q1_sp = q1c.add('50000+30000', 'Closing securities premium')
    q1_rs = q1c.add('80000+250000+70000+60000', 'Reserves and surplus after redemption')
    q1_el = q1c.add('1150000+460000+150000', 'Total equity and liabilities after')
    q1_as = q1c.add('1200000+260000+140000+160000', 'Total assets after')
    Q1 = [
        je('(1)', [('Bank A/c', 270000)], [('Investments A/c', 250000), ('Profit and Loss A/c', q1_gain)], 'Being investments sold'),
        je('(2)', [('Bank A/c', q1_cash_iss)], [('Equity Share Capital A/c', 150000), ('Securities Premium A/c', 30000)], 'Being 15,000 equity shares of ₹10 issued at ₹12'),
        je('(3)', [('10% Preference Share Capital A/c', 400000), ('Premium on Redemption of Preference Shares A/c', q1_prem)], [('Preference Shareholders A/c', q1_pay)], 'Being amount due on redemption at 10% premium'),
        je('(4)', [('Profit and Loss A/c (Surplus)', q1_prem)], [('Premium on Redemption of Preference Shares A/c', q1_prem)], 'Being premium on redemption written off out of profits'),
        je('(5)', [('General Reserve A/c', q1_crr)], [('Capital Redemption Reserve A/c', q1_crr)], 'Being transfer to CRR'),
        je('(6)', [('Preference Shareholders A/c', q1_pay)], [('Bank A/c', q1_pay)], 'Being preference shareholders paid'),
    ]
    q1bs = table(['Particulars', '₹'], [
        ['EQUITY AND LIABILITIES', ''],
        ['Shareholders\' funds: Share capital (1,15,000 equity shares of ₹10 each)', inr(1150000)],
        ['Reserves and surplus: Securities premium ₹80,000; CRR ₹2,50,000; General reserve ₹70,000; Surplus ₹60,000', inr(q1_rs)],
        ['Current liabilities: Trade payables', inr(150000)],
        ['Total', inr(q1_el)],
        ['ASSETS', ''],
        ['Non-current assets: Property, plant and equipment', inr(1200000)],
        ['Current assets: Inventories', inr(260000)],
        ['Trade receivables', inr(140000)],
        ['Cash and cash equivalents', inr(q1_bank)],
        ['Total', inr(q1_as)],
    ], title='Balance Sheet of Om Chemicals Ltd after redemption (summarised)')

    # ---------------- Question 2 model ----------------
    q2c = Checks()
    q2_t1 = q2c.add('(1200000-700000)/10', 'Test 1 shares (face value ₹10)')
    q2_funds = q2c.add('1200000*105/100-(300000+260000)', 'Test 2 shortfall = payable 12,60,000 − funds 5,60,000')
    q2_t2 = q2c.add('700000/14', 'Test 2 shares at issue price ₹14')
    q2c.add('1200000*5/100', 'Premium on redemption')

    viva = [
        V('v1', 'State the main conditions of section 55 for redemption of preference shares.',
          'Preference shares must be redeemable within twenty years from issue, except for notified infrastructure projects. Shares can be redeemed only out of divisible profits or out of money raised by a fresh share issue made for that purpose. Only fully paid shares can be redeemed. When shares are redeemed out of profits, a sum equal to their nominal value must be transferred to the capital redemption reserve. Any premium on redemption must be provided out of profits, or for companies not covered by the prescribed accounting standards, out of profits or securities premium, before redemption.',
          [P('p1', 'Out of divisible profits or proceeds of a fresh issue of shares', 3, 'profit', 'fresh issue|new issue|new shares|fresh shares'),
           P('p2', 'Only fully paid shares can be redeemed', 2, 'fully paid'),
           P('p3', 'Transfer to CRR equal to nominal value redeemed out of profits', 3, 'capital redemption|crr', 'nominal|face value|equal|par', min=2),
           P('p4', 'Premium on redemption provided out of profits (or securities premium for other companies)', 1, 'premium'),
           P('p5', 'Redeemable within 20 years', 1, '20|twenty')], 'c3'),
        V('v2', 'Why is a capital redemption reserve created, and for what can it be used?',
          'When preference shares are redeemed out of profits, the capital that leaves the company must be replaced, so that the funds available to protect creditors are not reduced. An amount equal to the nominal value redeemed out of profits is moved from divisible profits to the capital redemption reserve, which then cannot be paid as dividend and is treated like paid-up capital for reduction purposes. Its only permitted use is issuing fully paid bonus shares.',
          [P('p1', 'Replaces redeemed capital so creditors\' security is not reduced', 4, 'creditor|outsider|lender|replace|protect|security|maintain capital|capital is not reduced|capital not reduced', min=1),
           P('p2', 'Created out of divisible profits equal to nominal value redeemed', 3, 'divisible|distributable|available for dividend|general reserve|profit', min=1),
           P('p3', 'Can be used only for fully paid bonus shares', 3, 'bonus')], 'c4'),
        V('v3', 'In deciding the transfer to CRR, why is the premium on a fresh issue ignored, and can debenture proceeds be used?',
          'Section 55 counts only the proceeds of a fresh issue of shares, and only the face value part replaces the capital redeemed. Securities premium can be applied only for the purposes allowed by section 52, so premium on the fresh issue is not treated as proceeds for replacing capital. Proceeds of debentures cannot be used either, because debentures are borrowings, not share capital.',
          [P('p1', 'Only the face value (nominal) of the fresh issue counts', 4, 'face value|nominal|par value|share capital part|capital portion', 'fresh|new', min=2),
           P('p2', 'Premium excluded — usable only for s. 52 purposes', 3, 'premium', 'section 52|52|not count|excluded|ignored|not included|cannot|not part|not used', min=2),
           P('p3', 'Debenture proceeds cannot be used (borrowing, not share capital)', 3, ALT('{d} {n}', '{n} {d}', d=('debenture', 'debentures'), n=('cannot', 'not', 'not allowed', 'never', 'no')))], 'c5'),
        V('v4', 'How do you calculate the minimum number of fresh shares to be issued for redemption?',
          'First find the maximum divisible profits available for redemption, after any amount the board wants to retain and after providing the premium on redemption out of profits. Minimum proceeds needed equals the nominal value of preference shares redeemed minus those available profits. Divide it by the face value of one new share and round up to the next whole share or the required multiple. Separately, if funds are short, divide the shortfall in cash by the full issue price including premium, and issue the larger number.',
          [P('p1', 'Nominal value redeemed minus divisible profits available', 4, 'nominal|face value|redeemed|redeem', 'less|minus|deduct|subtract', 'profit|reserve', min=3),
           P('p2', 'Divide by the face value of one new share (premium excluded)', 3, 'face value|par value|nominal value', 'divid|per share|one share|each share', min=1),
           P('p3', 'Round up to next whole share / multiple', 1, 'round|next higher|whole|multiple|fraction', min=1),
           P('p4', 'Funds test: shortfall ÷ issue price; take the higher', 2, 'fund|cash|shortfall|liquid', 'issue price|including premium|higher|greater|larger', min=2)], 'c6'),
        V('v5', 'How are partly called or partly paid preference shares dealt with on redemption?',
          'Only fully paid shares can be redeemed. If shares are partly called up, the company first makes the final call and collects it before redemption; if both fully paid and partly paid shares exist and nothing is said, only the fully paid shares are redeemed. If calls are in arrears, the company either collects the arrears or forfeits the shares after notice. Forfeited shares are not re-issued; they are cancelled, the number redeemed falls, and the forfeited amount goes to capital reserve.',
          [P('p1', 'Only fully paid shares can be redeemed', 3, 'fully paid'),
           P('p2', 'Final call made and collected first (or arrears collected)', 3, 'final call|call|arrear', 'collect|received|receive|paid|made|demand', min=2),
           P('p3', 'Defaulters\' shares forfeited and cancelled; forfeited amount to capital reserve', 4, 'forfeit', 'capital reserve|cancel|not reissued|not re issued|not re-issued|fewer|reduced', min=2)], 'c7'),
        V('v6', 'Why might a company issue redeemable preference shares?',
          'They help raise money when the primary market is dull, and investors are more willing to invest in an unlisted company if they know the shares will be bought back. The company can repay them when it has surplus funds it cannot use profitably. Also, dividend need not be paid in a loss year, unlike debenture interest, because preference dividend is an appropriation of profit and not a charge.',
          [P('p1', 'Raise finance in a dull market / attract investors to unlisted shares', 3, 'dull|difficult|unlisted|not traded|not listed|attract|easy to raise|raise finance|raise money|investors', min=1),
           P('p2', 'Repay when surplus funds exist', 3, 'surplus|excess|idle|repay|return'),
           P('p3', 'No dividend needed in a loss year — appropriation, not a charge like interest', 4, 'loss|no profit|appropriation|not a charge|not compulsory|not obligatory|need not', min=1)], 'c2'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Navya Pharma Ltd — planning a redemption', 'difficulty': 'hard',
        'case': ('Navya Pharma Ltd (a company following the notified accounting standards) must redeem 60,000 9% preference shares of ₹10 each at a premium of 10% on 31 March 2027. '
                 'It has a general reserve of ₹4,00,000, of which the board wants to keep at least ₹1,00,000, a surplus in profit and loss of ₹60,000 and securities premium of ₹50,000. '
                 'The premium on redemption is to be met from the surplus. Bank balance is ₹3,30,000. It will issue equity shares of ₹10 each at ₹15.'),
        'mcqs': [
            M('k1a', 'Out of which balance must the premium on redemption be provided?', ['Surplus in profit and loss (profits)', 'Securities premium', 'Capital reserve', 'Capital redemption reserve'], 0,
              "Navya follows the notified accounting standards, so section 55(2)(d)(i) requires the premium on redemption to be provided out of profits before redemption. Here the surplus in profit and loss is used. The trap 'securities premium' is not allowed for such companies. In practice: CAs check that the premium on redemption is charged to profits, not reserves like securities premium.", 'moderate') | {'topic': "Provisions of the Companies Act (Section 55)"},
            M('k1b', 'What is the minimum number of equity shares to satisfy section 55?', ['30,000', '20,000', '40,000', '24,000'], 0,
              "Nominal value redeemed = 60,000 × ₹10 = ₹6,00,000. Divisible profits available for CRR: general reserve 4,00,000 − 1,00,000 kept = ₹3,00,000 (the whole surplus of ₹60,000 is used for the 10% premium). Minimum fresh issue at face value = 6,00,000 − 3,00,000 = ₹3,00,000 → 30,000 shares of ₹10. The trap 20,000 divides the gap by issue price ₹15. In practice: the company issues at least this many shares to satisfy section 55.", 'hard', '(600000-300000)/10') | {'topic': "Methods of Redemption of Fully Paid-up Shares"},
            M('k1c', 'Is that issue enough for funds? Cash needed is the redemption amount; cash available is bank plus issue proceeds. What is the bank balance after paying the shareholders?', [R(120000), R(30000), R(330000), R(270000)], 0,
              "Amount payable = 6,00,000 + 10% premium 60,000 = ₹6,60,000. Cash available = bank 3,30,000 + 30,000 shares × ₹15 = 3,30,000 + 4,50,000 = ₹7,80,000. Balance after payment = 7,80,000 − 6,60,000 = ₹1,20,000, so the issue gives enough funds. The trap ₹3,30,000 is just the opening bank balance, ignoring both the issue and the payment. In practice: CAs check both the legal minimum issue and the cash requirement before finalising the issue size.", 'hard', '330000+30000*15-660000') | {'topic': "Methods of Redemption of Fully Paid-up Shares"},
            M('k1d', 'What amount is transferred to capital redemption reserve?', [R(300000), R(600000), R(150000), R(450000)], 0,
              "CRR = nominal value redeemed − face value of fresh issue = 6,00,000 − 3,00,000 = ₹3,00,000, transferred from general reserve. The premium on the fresh issue is ignored for CRR. The trap ₹6,00,000 ignores the fresh issue; ₹1,50,000 deducts the full issue proceeds of ₹4,50,000, including premium. In practice: the CRR protects creditors by keeping capital intact after preference shares are repaid.", 'moderate', '600000-300000') | {'topic': "Methods of Redemption of Fully Paid-up Shares"},
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch11', 'n': 5,
        'title': 'Redemption of Preference Shares',
        'outcomes': [
            'Explain why companies issue redeemable preference shares and what redemption means.',
            'State the provisions of section 55 and the role of the capital redemption reserve.',
            'Journalise redemption out of a fresh issue, out of divisible profits and by a combination, including premium on redemption and sale of investments.',
            'Compute the minimum fresh issue needed to comply with section 55 and to provide funds.',
            'Deal with partly called-up and fully called but partly paid preference shares before redemption.',
            'Prepare the balance sheet after redemption.',
        ],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 80}, 'prereq': ['fnd-p1-ch11-u02', 'fnd-p1-ch11-u04'],
                 'exam_tip': 'Remember three rules: CRR = nominal value redeemed − face value of fresh issue; premium on redemption comes out of profits; only fully paid shares are redeemed.'},
        'concepts': [
            {'id': 'c1', 'title': 'What redemption means',
             'body': ['Redemption is the repayment of preference share capital at a pre-agreed amount and time. The redemption date (maturity) is usually printed on the share certificate. Holders receive dividends while the shares are outstanding and their capital back on redemption.',
                      'Redemption also lets a company reshape its capital structure — for example, replacing costly preference capital with equity or other securities when that suits its growth.',
                      'Since the Companies Act, 2013 prohibits irredeemable preference shares, every preference share must eventually be redeemed (normally within 20 years).'],
             'analogy': 'Like a fixed-term rental agreement with a date on which the deposit must be returned.',
             'work': 'Finance teams keep a redemption calendar and plan funding (fresh issue, profits, sale of investments) months ahead of each due date.'},
            {'id': 'c2', 'title': 'Purpose of issuing redeemable preference shares',
             'body': ['They are a practical way to raise finance when the primary market is dull.',
                      'Investors may hesitate to buy shares of a company whose shares are not traded; knowing the company will buy them back makes them easier to sell.',
                      'The company can redeem them when it has surplus capital that it cannot use profitably.',
                      'Unlike interest on debentures or loans, preference dividend need not be paid in a loss year — it is an appropriation of profit, not a charge against profit.'],
             'analogy': 'A "return-guaranteed" ticket: easier to sell because the buyer knows when the money comes back.',
             'work': 'Start-ups and family companies often use redeemable preference shares in funding rounds; CAs model the redemption cash outflow in projections.'},
            {'id': 'c3', 'title': 'Section 55 — the legal conditions',
             'body': ['A company limited by shares, if its articles allow, may issue preference shares redeemable within 20 years of issue (longer only for notified infrastructure projects).',
                      '(a) Redemption only out of divisible profits (profits otherwise available for dividend) or out of money raised by a fresh share issue made specially for this. (b) Only fully paid shares can be redeemed.',
                      '(c) Premium on redemption: companies of the prescribed class whose statements follow the accounting standards under s. 133 must provide it out of profits before redemption (for shares issued before the Act, out of profits or securities premium); other companies may use profits or securities premium. This unit, like the study material, assumes companies follow s. 133 standards — so premium is written off out of profits.',
                      '(d) Where shares are redeemed out of profits, an amount equal to the nominal value redeemed is transferred from divisible profits to Capital Redemption Reserve (CRR). CRR is treated like paid-up share capital for reduction of capital, and may be used only for fully paid bonus shares.'],
             'analogy': 'Section 55 is the rule that if you take a brick out of the wall (capital), you must put another brick in — either a new brick (fresh issue) or one made from your own savings (CRR).',
             'work': 'Auditors verify every redemption against s. 55: fully paid status, source of funds, CRR transfer and premium treatment. A shortfall in CRR is a reportable non-compliance.'},
            {'id': 'c4', 'title': 'Why the capital "gap" must be filled — and the CRR',
             'body': ['Creditors and lenders rely on the company\'s capital as a cushion. Redemption pays capital out, so s. 55 requires the gap to be filled by (a) proceeds of a fresh issue of shares, (b) capitalisation of undistributed profits through CRR, or (c) a mix of both.',
                      'With a fresh issue, both capital and assets are replaced directly. With profits, the replacement is indirect: profits that could have gone out as dividend are locked in CRR and kept in the business; since CRR can only become bonus shares, those profits ultimately turn into share capital.',
                      'Only divisible profits (general reserve, surplus in profit and loss, other revenue reserves available for dividend) can be used for CRR. Capital reserve, securities premium, revaluation reserve and existing CRR cannot.'],
             'analogy': 'CRR is a locked locker inside the company: profits moved there can never be taken home as dividend.',
             'work': 'When reviewing reserves, a CA tags each one as divisible or not — the same tagging is used for dividend declaration, bonus issue and redemption.'},
            {'id': 'c5', 'title': 'Method 1 — redemption out of a fresh issue of shares',
             'body': ['New equity or preference shares can be issued; their proceeds replace the redeemed capital. Debenture proceeds cannot be used, since debentures are borrowings.',
                      'If the fresh issue is at a premium, only the face value counts as "proceeds" for replacing capital; the premium is credited to securities premium and can be used only for s. 52 purposes.',
                      'Reasons to issue fresh equity: the capital is needed permanently (and equity carries no fixed dividend); profits available for dividend are insufficient; liquidity is weak. Advantages: no net cash outflow; new shares may command a premium; shareholders keep an equity interest. Disadvantages: future earnings are diluted; shareholding pattern changes if outsiders subscribe (a rights issue avoids this).',
                      'Entries: Bank Dr, To Share Capital (To Securities Premium); Preference Share Capital Dr (and Premium on Redemption Dr), To Preference Shareholders; Preference Shareholders Dr, To Bank.'],
             'analogy': 'Refinancing a home loan: take a new loan to repay the old one — the house (capital base) is unchanged.',
             'work': 'In practice, the fresh issue and the redemption are timed so the new money arrives before the payout date.'},
            {'id': 'c6', 'title': 'Method 2 and combinations — profits, minimum fresh issue, sale of investments',
             'body': ['Out of profits: Divisible profits Dr, To CRR (nominal value redeemed). Advantages: equity percentages unchanged; surplus funds used. Disadvantage: liquidity falls, and assets such as investments may need to be sold.',
                      'Combination: CRR = nominal value redeemed − face value of fresh issue.',
                      'Minimum fresh issue (s. 55 test): (1) find the maximum divisible profits available (after amounts the board wants retained and after providing the redemption premium out of profits); (2) minimum proceeds = nominal value redeemed − that amount; (3) minimum shares = minimum proceeds ÷ face value of one share; (4) round up to the next whole share or required multiple.',
                      'Funds test: shortfall = amount payable − cash available (bank + sale of investments); shares = shortfall ÷ issue price (face value + premium); issue the higher of the two tests. Profit or loss on sale of investments goes to the statement of profit and loss.'],
             'analogy': 'Two separate locks: the "law lock" (s. 55 capital replacement) and the "cash lock" (enough money to pay). The fresh issue must open both.',
             'work': 'Treasury and secretarial teams run exactly these two tests when proposing a redemption plan to the board.'},
            {'id': 'c7', 'title': 'Partly called-up and partly paid preference shares',
             'body': ['Only fully paid shares can be redeemed. If shares are partly called up and the question says they are to be redeemed, assume the final call is made and collected first.',
                      'If both fully paid and partly paid preference shares exist and nothing is said, redeem only the fully paid shares and leave the partly paid ones.',
                      'Fully called but partly paid (calls in arrears): if arrears are collected (Bank Dr, To Calls in Arrears) the shares become fully paid and are redeemed normally. If not paid despite notice, the shares may be forfeited: Preference Share Capital Dr (called up), To Calls in Arrears, To Forfeited Shares. Being due for redemption, they are not re-issued; the number redeemed falls and Forfeited Shares is transferred to Capital Reserve.'],
             'analogy': 'You can only return a full deposit — if someone has not finished paying theirs, they must pay up first or lose what they paid.',
             'work': 'Before a redemption, the registrar\'s list of partly paid holders is checked; reminder and forfeiture notices are issued as per the articles.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Redemption wholly out of profits', 'difficulty': 'core', 'minutes': 10,
             'q': 'Sneh Ltd has 20,000 9% redeemable preference shares of ₹100 each fully paid, redeemable on 31 March 2027 at a premium of 5%. It has a general reserve of ₹30,00,000, surplus of ₹6,00,000 and bank balance of ₹25,00,000. The shares are redeemed out of profits. Journalise.',
             'solution': [journal(E1, 'Journal of Sneh Ltd', 'j1'),
                          wn('After redemption', f'CRR ₹{inr(pv)}; general reserve ₹10,00,000; surplus ₹5,00,000; bank ₹4,00,000. Shareholders\' funds fall only by the cash paid out (₹{inr(pay)}), and capital plus CRR still total the original preference capital.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Combination: minimum fresh issue at a premium', 'difficulty': 'moderate', 'minutes': 14,
             'q': 'Tara Ltd will redeem 50,000 10% preference shares of ₹10 each at a premium of 10%. Balances: general reserve ₹2,40,000 (the board wants to keep ₹40,000); surplus ₹50,000 (to meet the premium); bank ₹2,00,000. It will issue the minimum number of equity shares of ₹10 each at ₹12 needed to comply with s. 55. Compute the issue and journalise.',
             'solution': [wn('Minimum fresh issue', f'Divisible profits available for CRR = 2,40,000 − 40,000 = ₹{inr(avail)} (premium is met from the surplus). Minimum face value from fresh issue = 5,00,000 − 2,00,000 = ₹{inr(minp)}. Shares = ₹{inr(minp)} ÷ ₹10 = {inr(nsh)}. Cash raised = {inr(nsh)} × ₹12 = ₹{inr(cash2)}.'),
                          wn('Funds check', f'Bank 2,00,000 + 3,60,000 = ₹5,60,000 ≥ amount payable ₹{inr(pay2)} — enough.'),
                          journal(E2, 'Journal of Tara Ltd', 'j2')],
             'checks': c2},
            {'id': 'i3', 'title': 'Two tests for the fresh issue, with sale of investments', 'difficulty': 'hard', 'minutes': 15,
             'q': 'Ekam Ltd must redeem 8% preference shares of ₹8,00,000 at par. Divisible profits available (general reserve) ₹5,50,000. Bank ₹1,50,000. Investments costing ₹2,00,000 are sold for ₹2,20,000. Equity shares of ₹10 each will be issued at ₹12, in multiples of 100, in the minimum number needed both to comply with s. 55 and to provide funds. Compute and journalise.',
             'solution': [table(['Test', 'Working', 'Shares'], [
                 ['1. Section 55', f'(8,00,000 − 5,50,000) ÷ face value ₹10', inr(t1)],
                 ['2. Funds', f'Shortfall = 8,00,000 − (1,50,000 + 2,20,000) = {inr(short)}; ÷ issue price ₹12 = {inr(t2)}', '35,834 → 35,900 (multiple of 100)'],
             ], title='Minimum fresh issue'),
                          wn('Decision', f'Issue the higher: {inr(n3)} shares = capital ₹{inr(cap3)} + premium ₹{inr(prem3)} = cash ₹{inr(cash3)}. CRR = 8,00,000 − {inr(cap3)} = ₹{inr(crr3)}.'),
                          journal(E3, 'Journal of Ekam Ltd', 'j3'),
                          note('Bank after redemption = 1,50,000 + 2,20,000 + 4,30,800 − 8,00,000 = ₹800.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Partly paid preference shares — call, default, forfeiture, redemption', 'difficulty': 'hard', 'minutes': 15,
             'q': 'Bela Ltd has 30,000 8% redeemable preference shares of ₹100 each, ₹80 called and paid. To redeem them at par it makes the final call of ₹20; holders of 1,000 shares fail to pay and their shares are forfeited. It issues 1,00,000 equity shares of ₹10 each at par and uses general reserve for the balance. Journalise (calls in arrears account used).',
             'solution': [journal(E4, 'Journal of Bela Ltd', 'j4'),
                          wn('Working', f'Shares redeemed = 29,000 × ₹100 = ₹{inr(red)}. CRR = {inr(red)} − 10,00,000 = ₹{inr(crr4)}. Forfeited ₹80 × 1,000 = ₹{inr(forf)} → capital reserve, because the forfeited shares are cancelled rather than re-issued.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Redemption plan for a board meeting', 'role': 'Company secretary and finance controller of an unlisted company',
             'situation': 'Preference shares of ₹5 crore fall due in three months at a 5% premium. Free reserves are ₹3.2 crore; the board wants to keep at least ₹1 crore. Cash is tight.',
             'steps': ['Premium ₹25 lakh to be met out of profits — reserve available for CRR = 3.2 − 1 − 0.25 = ₹1.95 crore.',
                       'Minimum face value of fresh issue = 5 − 1.95 = ₹3.05 crore.',
                       'Compare with cash shortfall and issue price to find the funds requirement; take the higher.',
                       'Check the shares are fully paid; plan final calls or forfeiture if any are not.',
                       'Draft resolutions for the fresh issue and for the CRR transfer.'],
             'takeaway': 'A good redemption note shows the law test, the cash test and the reserve impact on one page.',
             'checks': [{'expr': '3.2-1-0.25', 'value': 1.95, 'label': 'Reserve available for CRR (₹ crore)'}, {'expr': '5-1.95', 'value': 3.05, 'label': 'Minimum face value of fresh issue (₹ crore)'}]},
            {'id': 'j2', 'title': 'Audit check: was the CRR right?', 'role': 'Audit senior',
             'situation': 'A client redeemed ₹40 lakh preference shares, financed by issuing equity of face value ₹15 lakh at a premium of ₹10 lakh. It transferred ₹15 lakh to CRR, arguing that the fresh issue brought in ₹25 lakh.',
             'steps': ['Recall: only the face value of the fresh issue counts; premium is ignored.',
                       'Required CRR = ₹40 lakh − ₹15 lakh = ₹25 lakh.',
                       'Shortfall in CRR = ₹10 lakh.',
                       'Propose: General Reserve Dr ₹10 lakh, To CRR ₹10 lakh; check divisible profits are available.',
                       'Report non-compliance if the client refuses.'],
             'takeaway': 'Premium on a fresh issue never reduces the CRR requirement.',
             'checks': [{'expr': '40-15', 'value': 25, 'label': 'Required CRR (₹ lakh)'}, {'expr': '25-15', 'value': 10, 'label': 'Shortfall (₹ lakh)'}]},
        ],
        'mcqs': [
            mcq('m1', 'Preference shares can be redeemed only if they are:', ['Fully paid', 'Partly paid', 'Listed', 'Cumulative'], 0, "Section 55(2)(a) of the Companies Act, 2013 allows redemption only of fully paid preference shares. Partly paid shares must first be made fully paid (by calls) before they can be redeemed. The trap 'cumulative' describes the dividend right, which has nothing to do with eligibility for redemption. In practice: before a redemption date, the company secretary checks that all calls on the preference shares have been received.", 'c3') | {'topic': "Provisions of the Companies Act (Section 55)"},
            mcq('m2', 'Which of the following can be used for redemption of preference shares?', ['Proceeds of a fresh issue of equity shares', 'Proceeds of an issue of debentures', 'Revaluation reserve', 'Capital reserve'], 0,
                "Section 55 allows redemption only out of divisible profits or the proceeds of a fresh issue of shares made for that purpose. A fresh equity issue therefore qualifies. The trap 'proceeds of debentures' is wrong — debentures are borrowings, and replacing share capital with debt would weaken creditors' protection. Revaluation and capital reserves are not divisible profits. In practice: companies often refinance redeemable preference shares with a fresh equity issue or a rights issue.", 'c5') | {'topic': "Methods of Redemption of Fully Paid-up Shares"},
            mcq('m3', 'Preference shares of ₹6,00,000 are redeemed out of a fresh issue of equity of face value ₹2,00,000 issued at a 20% premium, and the rest out of profits. Transfer to CRR is:', ['₹4,00,000', '₹3,60,000', '₹6,00,000', '₹2,40,000'], 0,
                "CRR = nominal value of shares redeemed − face value of the fresh issue = 6,00,000 − 2,00,000 = ₹4,00,000. The premium on the fresh issue (20% of 2,00,000 = ₹40,000) is ignored because only face value replaces capital. The trap ₹3,60,000 deducts the issue proceeds including premium. In practice: auditors verify the CRR transfer, since capital lost on redemption must be replaced either by new capital or by locking up profits.", 'c6', 'moderate', '600000-200000') | {'topic': "Methods of Redemption of Fully Paid-up Shares"},
            mcq('m4', 'Capital redemption reserve can be used for:', ['Issuing fully paid bonus shares', 'Paying dividend', 'Writing off preliminary expenses', 'Paying up partly paid shares'], 0,
                "Section 55 says the capital redemption reserve may be applied only in paying up unissued shares to be issued as fully paid bonus shares. It cannot pay dividends, write off expenses or pay calls on partly paid shares. The trap 'paying up partly paid shares' is allowed only from free reserves. In practice: companies with a large CRR often use it later for a bonus issue to existing shareholders.", 'c4') | {'topic': "Provisions of the Companies Act (Section 55)"},
            mcq('m5', 'For a company following the accounting standards under s. 133, premium on redemption of preference shares is provided out of:', ['Profits of the company', 'Securities premium only', 'Capital reserve', 'Proceeds of fresh issue'], 0,
                "For companies following the accounting standards prescribed under section 133, section 55(2)(d)(i) requires the premium on redemption to be provided out of profits before the shares are redeemed. Securities premium cannot be used for this by such companies — that is the trap. In practice: a company planning a redemption at a premium sets aside the premium from its profits well before the due date.", 'c3', 'moderate') | {'topic': "Provisions of the Companies Act (Section 55)"},
            mcq('m6', 'Which reserve is a divisible profit for creating CRR?', ['General reserve', 'Securities premium', 'Capital reserve', 'Revaluation reserve'], 0, "Divisible profits are profits available for dividend. General reserve is a revenue reserve built from profits, so it can be transferred to CRR. Securities premium, capital reserve and revaluation reserve are not available for dividend, so they cannot be used. The trap 'securities premium' looks like a reserve but is capital in nature. In practice: companies use general reserve or retained earnings for the CRR transfer on redemption.", 'c4') | {'topic': "Provisions of the Companies Act (Section 55)"},
            mcq('m7', 'Preference shares of ₹5,00,000 are to be redeemed. Divisible profits available ₹3,00,000. Minimum number of equity shares of ₹10 each to be issued at ₹10 to comply with s. 55:', ['20,000', '30,000', '50,000', '25,000'], 0,
                "Section 55 requires the nominal value redeemed to be covered by divisible profits or by a fresh issue. Gap = 5,00,000 − 3,00,000 = ₹2,00,000, which must be raised by fresh shares at face value. Shares at ₹10 = 2,00,000 ÷ 10 = 20,000. The trap 50,000 ignores the available profits; 30,000 confuses profits with the shortfall. In practice: CAs compute this minimum issue first, then check whether it also gives enough cash.", 'c6', 'core', '(500000-300000)/10') | {'topic': "Methods of Redemption of Fully Paid-up Shares"},
            mcq('m8', 'The minimum face value to be raised by a fresh issue is ₹2,05,005. Shares of ₹10 each must be issued in multiples of 50. The minimum number of shares is:', ['20,550', '20,501', '20,500', '20,600'], 0,
                "Minimum face value needed = ₹2,05,005. Shares needed = 2,05,005 ÷ 10 = 20,500.5, rounded up to 20,501 whole shares. Since shares must be in multiples of 50, the next multiple is 20,550. The trap 20,500 rounds down and leaves a shortfall; 20,501 ignores the multiple-of-50 rule. In practice: companies set issue lots such as multiples of 50 or 100 for administrative convenience.", 'c6', 'hard', '-(-20501//50)*50') | {'topic': "Methods of Redemption of Fully Paid-up Shares"},
            mcq('m9', 'Amount payable on redemption ₹7,20,000; bank ₹1,20,000; investments sold for ₹1,80,000. Equity shares issued at ₹15 (face value ₹10). Minimum shares to provide funds:', ['28,000', '42,000', '48,000', '30,000'], 0,
                "Cash needed = ₹7,20,000. Available = bank 1,20,000 + investments sold 1,80,000 = ₹3,00,000. Shortfall = ₹4,20,000. Each new share brings ₹15 (face value plus premium), so shares needed = 4,20,000 ÷ 15 = 28,000. The trap 42,000 divides by face value ₹10, ignoring the premium received in cash. In practice: treasury teams plan redemptions by listing every source of cash before deciding the size of a fresh issue.", 'c6', 'moderate', '(720000-300000)/15') | {'topic': "Methods of Redemption of Fully Paid-up Shares"},
            mcq('m10', 'Investments costing ₹3,00,000 are sold for ₹2,70,000 to fund redemption. The loss of ₹30,000 is:', ['Debited to the statement of profit and loss', 'Debited to CRR', 'Debited to securities premium', 'Added to the cost of redemption'], 0,
                "Loss on sale of investments is a revenue item, debited to the statement of profit and loss. It does not affect the redemption amount, CRR or securities premium. The trap 'debited to CRR' wrongly uses a reserve that can be applied only for bonus shares. In practice: companies selling investments to fund redemptions report any profit or loss on sale in the profit and loss statement for that year.", 'c6') | {'topic': "Methods of Redemption of Fully Paid-up Shares"},
            mcq('m11', 'A company has both fully paid and partly paid redeemable preference shares and the question is silent. It should:', ['Redeem only the fully paid shares', 'Redeem all shares at their paid-up value', 'Redeem the partly paid shares first', 'Not redeem any shares'], 0,
                "Only fully paid preference shares can be redeemed under section 55. When a company has both fully paid and partly paid shares and the question is silent, it redeems only the fully paid ones; partly paid shares remain until they are made fully paid. The trap 'redeem all at paid-up value' is not allowed under section 55. In practice: before redemption, a company calls the unpaid amount on partly paid shares or forfeits shares if calls are not met.", 'c7') | {'topic': "Redemption of Fully Called But Partly Paid-up Preference Shares"},
            mcq('m12', '2,000 preference shares of ₹100 (fully called, ₹75 paid) are forfeited before redemption. The amount transferred to capital reserve is:', ['₹1,50,000', '₹50,000', '₹2,00,000', '₹75,000'], 0,
                "Shares that are fully called but only ₹75 paid are forfeited for non-payment. The amount received, ₹75 × 2,000 = ₹1,50,000, is credited to forfeited shares. Since forfeited preference shares are cancelled rather than re-issued, this is transferred to capital reserve. The trap ₹50,000 is the unpaid call. In practice: forfeiture before redemption removes defaulting holders, and their paid amount becomes a capital reserve.", 'c7', 'moderate', '2000*75') | {'topic': "Redemption of Fully Called But Partly Paid-up Preference Shares"},
            mcq('m13', 'Preference shares must ordinarily be redeemed within:', ['Twenty years of issue', 'Ten years of issue', 'Five years of issue', 'Thirty years of issue'], 0,
                "Section 55 requires preference shares to be redeemable within 20 years of issue. Companies engaged in notified infrastructure projects may issue preference shares for longer than 20 years (up to 30 years), subject to redeeming a minimum 10% each year from the 21st year. The trap 'ten years' is too short. In practice: infrastructure companies financing long-gestation projects often use this extended redemption window.", 'c3') | {'topic': "Provisions of the Companies Act (Section 55)"},
        ],
        'questions': [
            {'id': 'q1', 'marks': 10, 'minutes': minutes(10), 'difficulty': 'hard', 'pad': 'journal',
             'q': 'The summarised balance sheet of Om Chemicals Ltd on 31 March 2027 shows: Equity share capital (1,00,000 shares of ₹10) ₹10,00,000; 10% redeemable preference shares (40,000 of ₹10, fully paid) ₹4,00,000; Securities premium ₹50,000; General reserve ₹3,20,000; Surplus ₹80,000; Trade payables ₹1,50,000 — total ₹20,00,000. Assets: PPE ₹12,00,000; Investments ₹2,50,000; Inventories ₹2,60,000; Trade receivables ₹1,40,000; Bank ₹1,50,000. The preference shares are redeemed at a premium of 10%. For this purpose: investments are sold for ₹2,70,000; 15,000 equity shares of ₹10 each are issued at ₹12, fully paid; the premium on redemption is met from the surplus; and the balance needed for CRR comes from general reserve. Pass journal entries and prepare the balance sheet after redemption.',
             'model': [journal(Q1, 'Journal of Om Chemicals Ltd', 'jq1'),
                       wn('Workings', f'CRR = 4,00,000 − 1,50,000 (face value of fresh issue) = ₹{inr(q1_crr)}. Bank = 1,50,000 + 2,70,000 + 1,80,000 − 4,40,000 = ₹{inr(q1_bank)}. Surplus = 80,000 + 20,000 − 40,000 = ₹{inr(q1_pl)}. General reserve = ₹{inr(q1_gr)}. Securities premium = ₹{inr(q1_sp)}.'),
                       q1bs],
             'checks': q1c,
             'scheme': [S('s1', 'Sale of investments with profit ₹20,000 to P&L', 1, 'posting'),
                        S('s2', 'Fresh issue: capital ₹1,50,000 and premium ₹30,000', 1, 'posting'),
                        S('s3', 'Redemption due incl. premium ₹40,000; premium written off from surplus', 1.5, 'concept'),
                        S('s4', 'CRR ₹2,50,000 from general reserve (premium on fresh issue ignored)', 2, 'computation'),
                        S('s5', 'Payment ₹4,40,000', 0.5, 'posting'),
                        S('s6', 'Balance sheet: share capital ₹11,50,000; reserves ₹4,60,000 correctly itemised', 2, 'presentation'),
                        S('s7', 'Bank ₹1,60,000 and totals ₹17,60,000 agree', 2, 'balancing')],
             'remarks': ['Many answers transfer only ₹2,20,000 to CRR by counting the ₹30,000 premium — this is wrong.', 'Some write off the redemption premium against securities premium, which the s. 133 convention does not allow.', 'Balance sheets without the reserves break-up lose presentation marks.'],
             'mistakes': ['Omitting the profit on sale of investments from the surplus.', 'Showing preference share capital after redemption.', 'Forgetting to add the fresh issue to share capital.'],
             'tips': ['Do the CRR and bank working before writing entries.', 'Present reserves item by item in a note, even in a summarised balance sheet.']},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'Disha Ltd will redeem preference shares of ₹12,00,000 at a premium of 5%. Divisible profits available for CRR (after meeting the premium) are ₹7,00,000. Bank balance is ₹3,00,000 and investments will realise ₹2,60,000. Equity shares of ₹10 each are to be issued at ₹14. Find the minimum number of equity shares to be issued (a) to comply with section 55, and (b) to provide sufficient funds. How many will be issued?',
             'model': [p(f'(a) Section 55: (12,00,000 − 7,00,000) ÷ ₹10 = {inr(q2_t1)} shares.'),
                       p(f'(b) Funds: amount payable = 12,00,000 + 5% = ₹12,60,000; funds available = 3,00,000 + 2,60,000 = ₹5,60,000; shortfall ₹{inr(q2_funds)}; shares = {inr(q2_funds)} ÷ ₹14 = {inr(q2_t2)}.'),
                       p('Both tests give 50,000 shares, so 50,000 equity shares of ₹10 each at ₹14 will be issued (capital ₹5,00,000, premium ₹2,00,000).')],
             'checks': q2c,
             'scheme': [S('s1', 'Section 55 test using face value — 50,000', 2, 'computation'), S('s2', 'Amount payable including premium ₹12,60,000', 1, 'computation'),
                        S('s3', 'Funds test using issue price — 50,000', 1.5, 'computation'), S('s4', 'Conclusion: issue the higher (here equal) number', 0.5, 'conclusion')],
             'remarks': ['Candidates often divide the s. 55 shortfall by the issue price ₹14 — the face value must be used for that test.'],
             'mistakes': ['Ignoring the redemption premium in the funds test.', 'Using the issue price for the s. 55 test.'],
             'tips': ['Label the two tests clearly and write the rule for each.']},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'text',
             'q': 'State the provisions of section 55 of the Companies Act, 2013 relating to the redemption of preference shares.',
             'model': [ul(['A company limited by shares may, if authorised by its articles, issue preference shares redeemable within 20 years of issue (longer only for notified infrastructure projects); irredeemable preference shares are not allowed.',
                           'Redemption only out of profits otherwise available for dividend, or out of money raised by a fresh share issue made specially for this.',
                           'Only fully paid shares can be redeemed.',
                           'Premium on redemption: for prescribed companies following s. 133 accounting standards, out of profits before redemption; for other companies, out of profits or securities premium.',
                           'Where redeemed out of profits, a sum equal to the nominal value redeemed is transferred to Capital Redemption Reserve; CRR is treated as paid-up capital for reduction purposes and can be used only for fully paid bonus shares.'])],
             'scheme': [S('s1', '20-year limit / no irredeemable shares', 1, 'provision'), S('s2', 'Sources: divisible profits or fresh issue', 1, 'provision'),
                        S('s3', 'Fully paid shares only', 1, 'provision'), S('s4', 'Treatment of redemption premium', 1, 'provision'), S('s5', 'CRR — amount and use', 1, 'provision')],
             'remarks': ['The CRR point is often written without saying the amount (nominal value redeemed out of profits).'],
             'mistakes': ['Saying debenture proceeds can be used.', 'Saying CRR can be used to pay dividend.'],
             'tips': ['Five numbered points, each one line, quoting the section.']},
            {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'journal',
             'q': 'Ruchi Ltd has 10,000 9% redeemable preference shares of ₹100 each, fully called. Holders of 400 shares have not paid the final call of ₹30. Despite notice they do not pay, and the shares are forfeited. Pass the journal entries for the forfeiture and its aftermath, and state how many shares will be redeemed.',
             'model': [journal([je('(1)', [('9% Preference Share Capital A/c', 40000)], [('Calls in Arrears A/c', 12000), ('Forfeited Shares A/c', 28000)], 'Being 400 preference shares forfeited for non-payment of final call'),
                                je('(2)', [('Forfeited Shares A/c', 28000)], [('Capital Reserve A/c', 28000)], 'Being forfeited amount transferred to capital reserve as the shares will not be re-issued')], 'Journal of Ruchi Ltd', 'jq4'),
                       p('Shares to be redeemed = 10,000 − 400 = 9,600 shares (₹9,60,000).')],
             'checks': [{'expr': '400*100', 'value': 40000, 'label': 'Called-up value of forfeited shares'}, {'expr': '400*30', 'value': 12000, 'label': 'Calls in arrears'}, {'expr': '40000-12000', 'value': 28000, 'label': 'Forfeited amount'}, {'expr': '(10000-400)*100', 'value': 960000, 'label': 'Shares redeemed'}],
             'scheme': [S('s1', 'Forfeiture entry with correct amounts', 1.5, 'posting'), S('s2', 'Transfer to capital reserve (not re-issued)', 1.5, 'concept'), S('s3', 'Shares redeemed 9,600', 1, 'conclusion')],
             'remarks': ['Some candidates redeem all 10,000 shares — forfeited shares are cancelled.'],
             'mistakes': ['Leaving the forfeited amount in Forfeited Shares Account.'],
             'tips': ['Explain why the forfeited shares are not re-issued.']},
        ],
        'viva': viva,
        'cases': cases,
        'revision': {
            'summary': ['Redemption = repayment of preference capital; irredeemable preference shares are not allowed; normally within 20 years.',
                        'Section 55: only fully paid shares; out of divisible profits or fresh issue of shares; CRR = nominal value redeemed out of profits; premium on redemption out of profits (s. 133 companies).',
                        'CRR = nominal value redeemed − face value of fresh issue; usable only for bonus shares.',
                        'Minimum fresh issue: (nominal redeemed − available divisible profits) ÷ face value; funds test: shortfall ÷ issue price; take the higher, round up.',
                        'Partly called: make final call first. Arrears unpaid: forfeit, cancel, forfeited amount → capital reserve.'],
            'remember': ['Premium on a fresh issue is not "proceeds" for CRR.', 'Debenture proceeds can never fund redemption under s. 55.', 'Profit/loss on sale of investments goes to P&L.'],
            'traps': ['Using securities premium or capital reserve to create CRR.', 'Dividing the s. 55 shortfall by the issue price.', 'Redeeming forfeited shares.', 'Forgetting the redemption premium in the cash requirement.'],
        },
        'quickref': [
            {'k': 'Section 55 sources', 'v': 'Divisible profits or proceeds of a fresh issue of shares (not debentures)'},
            {'k': 'CRR', 'v': 'Nominal value redeemed − face value of fresh issue; out of divisible profits; only for bonus'},
            {'k': 'Redemption entry', 'v': 'Pref. Share Capital Dr + Premium on Redemption Dr To Pref. Shareholders; Pref. Shareholders Dr To Bank'},
            {'k': 'Premium on redemption', 'v': 'Written off out of profits (s. 133 companies): P&L / General Reserve Dr To Premium on Redemption'},
            {'k': 'Minimum shares (s. 55)', 'v': '(Nominal redeemed − divisible profits available) ÷ face value per share; round up'},
            {'k': 'Minimum shares (funds)', 'v': '(Amount payable − cash available) ÷ issue price per share; round up'},
            {'k': 'Forfeited pref. shares', 'v': 'Capital Dr To Calls in Arrears, To Forfeited Shares; Forfeited Shares Dr To Capital Reserve'},
        ],
    }
