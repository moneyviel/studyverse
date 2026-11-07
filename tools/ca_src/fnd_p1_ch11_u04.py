"""CA Foundation · Paper 1 Accounting · Chapter 11 Company Accounts · Unit 4 Accounting for Bonus Issue and Right Issue.
Original explanations, names and numbers (structure and scope follow the ICAI study material)."""
from lib import *
from ca_viva import P, ALT, V
from ca_cases import M

UID = 'fnd-p1-ch11-u04'


def mcq(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check: d['check'] = check
    return d


def S(sid, pt, m, skill): return {'id': sid, 'pt': pt, 'm': m, 'skill': skill}


def build():
    # ---------------- Illustration 1: bonus with minimum use of free reserves (listed) ----------------
    c1 = Checks()
    nb = c1.add('60000/3', 'Bonus shares 1 for 3 on 60,000 shares')
    vb = c1.add('20000*10', 'Value of bonus shares')
    gr = c1.add('200000-40000-30000', 'General reserve needed after CRR and cash-realised premium')
    c1.add('180000-130000', 'General reserve left')
    E1 = [
        je('Jun 30', [('Capital Redemption Reserve A/c', 40000), ('Securities Premium A/c', 30000), ('General Reserve A/c', gr)], [('Bonus to Shareholders A/c', vb)], 'Being bonus of one share for every three held sanctioned, using CRR, premium realised in cash and general reserve'),
        je('Jun 30', [('Bonus to Shareholders A/c', vb)], [('Equity Share Capital A/c', vb)], 'Being 20,000 fully paid bonus shares of ₹10 each issued'),
    ]
    rs_before = table(['Reserve', 'Balance ₹', 'Used for bonus ₹', 'Left ₹'], [
        ['Capital redemption reserve', inr(40000), inr(40000), '0'],
        ['Securities premium — realised in cash', inr(30000), inr(30000), '0'],
        ['Securities premium — on shares issued to a vendor (not realised in cash)', inr(20000), '0', inr(20000)],
        ['General reserve', inr(180000), inr(gr), inr(50000)],
        ['Surplus (profit and loss)', inr(70000), '0', inr(70000)],
        ['Revaluation reserve', inr(60000), '0', inr(60000)],
        ['Total', inr(400000), inr(vb), inr(200000)],
    ], num=[1, 2, 3], total=True, title='Reserves used (minimum reduction in free reserves)')
    c1.add('40000+30000+20000+180000+70000+60000', 'Total reserves before bonus')

    # ---------------- Illustration 2: partly paid shares made fully paid, then bonus ----------------
    c2 = Checks()
    fc = c2.add('40000*2', 'Final call ₹2 on 40,000 shares made out of general reserve')
    b2 = c2.add('40000/4*10', 'Bonus 1 for 4 on 40,000 shares at ₹10')
    c2.add('100000-60000', 'General reserve used for bonus after securities premium')
    c2.add('150000-80000-40000', 'General reserve left')
    E2 = [
        je('(1)', [('General Reserve A/c', fc)], [('Bonus to Shareholders A/c', fc)], 'Being bonus sanctioned to make partly paid shares fully paid'),
        je('(2)', [('Equity Share Final Call A/c', fc)], [('Equity Share Capital A/c', fc)], 'Being final call of ₹2 per share made'),
        je('(3)', [('Bonus to Shareholders A/c', fc)], [('Equity Share Final Call A/c', fc)], 'Being bonus applied in payment of the final call'),
        je('(4)', [('Securities Premium A/c', 60000), ('General Reserve A/c', 40000)], [('Bonus to Shareholders A/c', b2)], 'Being bonus of one fully paid share for every four held sanctioned'),
        je('(5)', [('Bonus to Shareholders A/c', b2)], [('Equity Share Capital A/c', b2)], 'Being 10,000 bonus shares of ₹10 each issued as fully paid'),
    ]

    # ---------------- Illustration 3: rights issue — TERP and value of right ----------------
    c3 = Checks()
    rs = c3.add('100000/4', 'Rights shares 1 for 4')
    terp = c3.add('(100000*60+25000*45)/(100000+25000)', 'Theoretical ex-right price')
    vr_e = c3.add('60-57', 'Value of right per existing share')
    vr_r = c3.add('57-45', 'Value of right per right share')
    cash3 = c3.add('25000*45', 'Cash from rights issue')
    c3.add('25000*10', 'Share capital credited')
    c3.add('25000*35', 'Securities premium credited')
    E3 = [je('Sep 15', [('Bank A/c', cash3)], [('Equity Share Capital A/c', 250000), ('Securities Premium A/c', 875000)], 'Being 25,000 rights shares of ₹10 each issued at ₹45 (1 for 4)')]

    # ---------------- Illustration 4: shareholder's choices ----------------
    c4 = Checks()
    before = c4.add('400*60', 'Value before rights: 400 × ₹60')
    sub_hold = c4.add('500*57', 'Subscribe: 500 shares × ₹57')
    sub_pay = c4.add('100*45', 'Subscribe: cash paid')
    c4.add('28500-4500', 'Subscribe: net wealth')
    ren_hold = c4.add('400*57', 'Renounce or ignore: 400 × ₹57')
    ren_sale = c4.add('100*12', 'Renounce: sale of 100 rights @ ₹12')
    c4.add('22800+1200', 'Renounce: wealth')
    c4.add('24000-22800', 'Ignore: loss')
    ch = table(['Choice', 'Shares held after', 'Value of shares ₹', 'Cash in (+) / out (−) ₹', 'Wealth ₹'], [
        ['Before the issue', '400', inr(before), '0', inr(before)],
        ['Subscribe for 100 rights shares', '500', inr(sub_hold), '−' + inr(sub_pay), inr(24000)],
        ['Renounce rights to a buyer', '400', inr(ren_hold), '+' + inr(ren_sale), inr(24000)],
        ['Ignore the offer', '400', inr(ren_hold), '0', inr(22800)],
    ], title='Effect on Vani, who holds 400 shares (cum-right ₹60, issue price ₹45, ex-right ₹57)')

    # ---------------- Question 1 model ----------------
    q1c = Checks()
    q1_b = q1c.add('80000*2/5*10', 'Bonus 2 for 5 on 80,000 shares')
    q1_gr = q1c.add('320000-90000-50000', 'General reserve used')
    q1c.add('250000-180000', 'General reserve left')
    Q1 = [
        je('(i)', [('Capital Redemption Reserve A/c', 90000), ('Securities Premium A/c', 50000), ('General Reserve A/c', q1_gr)], [('Bonus to Shareholders A/c', q1_b)], 'Being bonus of 2 shares for every 5 held sanctioned with minimum use of free reserves'),
        je('(ii)', [('Bonus to Shareholders A/c', q1_b)], [('Equity Share Capital A/c', q1_b)], 'Being 32,000 bonus shares of ₹10 each issued as fully paid'),
    ]

    # ---------------- Question 3 model ----------------
    q3c = Checks()
    q3_r = q3c.add('240000*1/6', 'Rights shares 1 for 6')
    q3_t = q3c.add('(240000*120+40000*85)/(240000+40000)', 'TERP')
    q3_ve = q3c.add('120-115', 'Value of right per existing share')
    q3_vr = q3c.add('115-85', 'Value of right per right share')
    q3_cash = q3c.add('40000*85', 'Cash raised')
    q3c.add('40000*10', 'Capital credited')
    q3c.add('40000*75', 'Premium credited')

    viva = [
        V('v1', 'What is a bonus issue, and why is it called capitalisation of profits?',
          'A bonus issue is an issue of fully paid shares to existing shareholders free of cost, in proportion to the shares they already hold. No new money comes into the company. It is called capitalisation of profits because accumulated profits or reserves, which could otherwise be paid as dividend, are converted into paid-up share capital. Net worth does not change, and each shareholder\'s percentage holding stays the same.',
          [P('p1', 'Free (no cost) fully paid shares to existing shareholders in proportion to holding', 4, 'free|no cost|without payment|without any payment|no payment|not pay|gift|nothing', 'existing|present|current|proportion|ratio', min=2),
           P('p2', 'Reserves/profits converted into share capital (capitalisation)', 4, 'reserve|profit', 'capital|capitalis|convert|transfer', min=2),
           P('p3', 'No new funds; net worth and proportion of holding unchanged', 2, 'no new fund|no new money|no fresh fund|no cash|net worth|same proportion|proportion remain|unchanged|does not change|doesn t change|no change', min=1)], 'c1'),
        V('v2', 'Out of which reserves can bonus shares be issued under section 63(1)?',
          'Under section 63(1), fully paid bonus shares may be issued out of free reserves, the securities premium account, or the capital redemption reserve account. Reserves created by revaluation of assets cannot be capitalised for bonus. For a listed company, securities premium can be used only if it was realised in cash, as per SEBI.',
          [P('p1', 'Free reserves', 2, 'free reserve'),
           P('p2', 'Securities premium', 2, 'securities premium|share premium|premium'),
           P('p3', 'Capital redemption reserve', 2, 'capital redemption|crr'),
           P('p4', 'Not out of revaluation reserve', 4, ALT('{n} revaluation', 'revaluation {x} not', 'revaluation {x} cannot', 'revaluation {x} excluded', 'revaluation {x} never', n=('not', 'cannot', 'never', 'excluding', 'except', 'no', 'excluded'), x=('reserve', 'reserves', 'reserve is', 'reserves are', 'of assets', 'of asset', 'asset')))], 'c2'),
        V('v3', 'State the conditions in section 63(2) that a company must satisfy before issuing bonus shares.',
          'The company must be authorised by its articles; the issue must be authorised in a general meeting on the board\'s recommendation; it must not have defaulted in paying interest or principal on fixed deposits or debt securities; it must not have defaulted on statutory dues of employees like provident fund, gratuity and bonus; and partly paid shares must be made fully paid on the date of allotment. Any other prescribed conditions must also be met. Bonus shares cannot be issued in lieu of dividend, and an announced bonus cannot be withdrawn.',
          [P('p1', 'Authorised by the articles', 2, 'articles'),
           P('p2', 'Authorised in general meeting on board recommendation', 2, 'general meeting|shareholders meeting|members meeting|agm|egm|shareholder approval|approved by shareholders'),
           P('p3', 'No default on deposits / debt securities (interest or principal)', 2, ALT('{n} default {x}', n=('no', 'not', 'never', 'without'), x=('deposit', 'deposits', 'debt', 'debenture', 'debentures', 'interest', 'principal', 'repaying', 'paying', 'repayment', 'payment', 'lender', 'lenders'))),
           P('p4', 'No default on employees\' statutory dues (PF, gratuity, bonus)', 2, ALT('{n} default {y}', n=('no', 'not', 'never', 'without'), y=('provident', 'pf', 'gratuity', 'employee', 'employees', 'statutory', 'bonus', 'staff'))),
           P('p5', 'Partly paid shares made fully paid', 2, 'partly paid|partly-paid|partly', 'fully paid|fully', min=2)], 'c3'),
        V('v4', 'What is a rights issue, and what does section 62(1)(a) require in the letter of offer?',
          'A rights issue is an offer of new shares to existing equity shareholders in proportion to their present holding, so that they can keep their percentage in the company. Under section 62(1)(a) the offer is made by a notice stating the number of shares offered and a time limit of not less than fifteen days and not more than thirty days, after which it is treated as declined. Unless the articles say otherwise, the shareholder can renounce the shares in favour of anyone else. After the period, the board may dispose of unaccepted shares in a way not disadvantageous to the shareholders and the company.',
          [P('p1', 'New shares offered first to existing shareholders in proportion to holding', 3, 'existing|present|current', 'proportion|ratio|pro rata|first', min=2),
           P('p2', 'Offer open for 15 to 30 days', 3, '15|fifteen', '30|thirty'),
           P('p3', 'Right to renounce in favour of another person (unless articles prohibit)', 2, 'renounce|renunciation|transfer the right|sell the right|give up in favour|pass the right'),
           P('p4', 'Board may dispose of unaccepted shares (not disadvantageously)', 2, 'board|director', 'dispose|allot|sell|issue', 'unaccepted|declined|not taken|not accepted|unsubscribed|remaining|left', min=2)], 'c5'),
        V('v5', 'How do you calculate the theoretical ex-right price and the value of a right?',
          'The theoretical ex-right price equals the cum-right market value of the existing shares plus the amount paid for the rights shares, divided by the total number of shares after the issue, that is existing plus rights shares. The value of a right per existing share is the cum-right price minus the ex-right price. Per rights share, it is the ex-right price minus the issue price.',
          [P('p1', 'TERP = (cum-right value of existing shares + rights shares × issue price) ÷ total shares after issue', 5, 'cum right|cum-right|market value|market price', 'issue price|amount paid|price paid|subscription', 'divided|total number|total shares|after the issue|existing plus|existing and rights|total|number of shares', min=3),
           P('p2', 'Value of right per existing share = cum-right price − ex-right price', 3, 'existing share cum right|existing cum right|existing share difference between cum|per existing share cum|existing share is cum', ALT('cum right {m} ex right', 'cum right price {m} ex right', 'difference between cum right price and ex right', 'difference between cum right and ex right', m=('minus', 'less', 'less the', 'minus the', 'reduced by'))),
           P('p3', 'Per rights share = ex-right price − issue price', 2, 'rights share ex right|right share ex right|per rights share ex|per right share ex|rights share is ex|rights share difference between ex', ALT('ex right {m} issue price', 'ex right price {m} issue price', 'ex right price {m} subscription price', 'difference between ex right price and issue price', m=('minus', 'less', 'less the', 'minus the')))], 'c6'),
        V('v6', 'What are the effects of a bonus issue on the company\'s accounts and on per-share figures?',
          'Share capital increases and reserves decrease by the same amount, so net worth and total assets do not change. The number of shares goes up, so earnings per share, book value per share and the market price per share fall, though each shareholder\'s total holding value is broadly the same. The market generally sees a bonus issue as a favourable signal.',
          [P('p1', 'Share capital increases and reserves decrease equally', 4, ALT('{c} {u}', c=('share capital', 'capital', 'paid up capital'), u=('increase', 'increases', 'goes up', 'rises', 'up')), ALT('{r} {d}', r=('reserve', 'reserves', 'accumulated profit', 'profits', 'free reserves'), d=('decrease', 'decreases', 'reduce', 'reduced', 'reduces', 'go down', 'goes down', 'fall', 'falls', 'down'))),
           P('p2', 'Net worth / total assets unchanged; no cash', 3, 'net worth|total assets|shareholders fund|no cash|no fund|no money', 'same|unchanged|not change|no change|doesn t change|does not change|don t change|dont change|remains|remain|no effect|unaffected|not affected|constant', min=2),
           P('p3', 'EPS and per-share values fall; market price adjusts', 3, 'eps|earnings per share|book value per share|per share|market price', 'fall|falls|reduce|decrease|lower|go down|goes down|drop|adjust|dilute', min=2)], 'c4'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Arohi Electronics — bonus followed by rights', 'difficulty': 'hard',
        'case': ('Arohi Electronics Ltd (listed) has 3,00,000 equity shares of ₹10 each, fully paid. Reserves: general reserve ₹9,00,000, securities premium (all realised in cash) '
                 '₹4,00,000, revaluation reserve ₹5,00,000. It first issues bonus shares of 1 for 5, using securities premium first. After the bonus, it offers rights shares of 1 for 4 '
                 'at ₹40 each. The market price just before the rights issue (cum-right) is ₹65. Kabir holds 1,500 shares before the bonus.'),
        'mcqs': [
            M('k1a', 'How many bonus shares does Kabir receive and how many does he hold after the bonus?', ['300 bonus; 1,800 in all', '375 bonus; 1,875 in all', '300 bonus; 1,500 in all', '500 bonus; 2,000 in all'], 0,
              "A bonus of 1 for 5 means one bonus share for every 5 held. Kabir's bonus = 1,500 ÷ 5 = 300 shares, so his holding becomes 1,500 + 300 = 1,800 shares. The trap '375 bonus' reads the ratio as 1 for 4, which is the later rights ratio, not the bonus ratio. In practice: demat accounts are credited with bonus shares after the record date, and the share price adjusts to reflect the larger number of shares.", 'core') | {'topic': "Bonus issue — capitalisation of profits"},
            M('k1b', 'How much general reserve is used for the bonus?', [R(200000), R(600000), R(100000), 'Nil'], 0,
              "Bonus shares = 3,00,000 ÷ 5 = 60,000 × ₹10 = ₹6,00,000. Securities premium (₹4,00,000, all realised in cash) is used first, so general reserve needed = 6,00,000 − 4,00,000 = ₹2,00,000. Revaluation reserve cannot be used under section 63(1). The trap ₹6,00,000 uses general reserve for the whole bonus. In practice: companies preserve free reserves, which can pay dividends, by using securities premium first.", 'moderate', '300000/5*10-400000') | {'topic': "Journal entries and effects of a bonus issue"},
            M('k1c', 'What is the theoretical ex-right price?', ['₹60', '₹65', '₹52.50', '₹40'], 0,
              "After the bonus, shares = 3,60,000. Rights 1 for 4 = 90,000 shares at ₹40. TERP = (3,60,000 × 65 + 90,000 × 40) ÷ 4,50,000 = (2,34,00,000 + 36,00,000) ÷ 4,50,000 = ₹60. The trap ₹52.50 simply averages 65 and 40, ignoring that existing shares outnumber rights shares 4 : 1. In practice: the share price adjusts on the ex-right date towards this theoretical value.", 'hard', '(360000*65+90000*40)/450000') | {'topic': "Pricing a rights issue — book value, cum-right, ex-right and value of right"},
            M('k1d', 'What can Kabir obtain by renouncing all his rights?', [R(9000), R(2250), R(11250), R(4500)], 0,
              "Kabir holds 1,800 shares after the bonus, so he gets 1,800 ÷ 4 = 450 rights. Value of each right = TERP − issue price = 60 − 40 = ₹20. Renouncing all gives 450 × 20 = ₹9,000 — the same as 1,800 × ₹5 lost per existing share (65 − 60). The trap ₹11,250 values each right at cum-right price minus issue price (65 − 40 = ₹25). In practice: shareholders can sell their rights entitlements on the exchange during the rights period.", 'hard', '450*(60-40)') | {'topic': "Pricing a rights issue — book value, cum-right, ex-right and value of right"},
            M('k1e', 'The rights issue entry for the whole company credits Securities Premium with:', [R(2700000), R(3600000), R(900000), R(2250000)], 0,
              "Rights shares = 3,60,000 ÷ 4 = 90,000. Premium per share = 40 − 10 = ₹30. Securities premium = 90,000 × 30 = ₹27,00,000; share capital credited ₹9,00,000. The trap ₹36,00,000 is the total amount received (90,000 × 40); ₹9,00,000 is share capital. In practice: rights issues at a premium build securities premium, which can later fund bonus issues or write off issue expenses.", 'moderate', '90000*30') | {'topic': "Accounting for rights issue; advantages and disadvantages"},
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch11', 'n': 4,
        'title': 'Accounting for Bonus Issue and Right Issue',
        'outcomes': [
            'Explain a bonus issue as capitalisation of profits and compute bonus entitlements.',
            'Apply section 63 — permitted sources, conditions and restrictions — and journalise bonus issues, including making partly paid shares fully paid.',
            'Explain the effects of a bonus issue on capital, reserves and per-share figures.',
            'Explain a rights issue under section 62(1)(a), its exceptions and the right of renunciation.',
            'Compute book value, theoretical ex-right price and value of a right, and journalise a rights issue.',
            'Evaluate the advantages and disadvantages of a rights issue.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 45, 'practice': 55}, 'prereq': ['fnd-p1-ch11-u02'],
                 'exam_tip': 'Bonus questions usually say "minimum reduction in free reserves" — use CRR and (cash-realised) securities premium first. Rights questions test the ex-right price and value of right.'},
        'concepts': [
            {'id': 'c1', 'title': 'Bonus issue — capitalisation of profits',
             'body': ['A bonus issue gives existing shareholders additional fully paid shares at no cost, in proportion to their present holding (e.g., 2 bonus shares for every 3 held: a holder of 6,000 gets 4,000 and ends with 10,000).',
                      'No new money is raised. Reserves that could have been paid out as dividend are converted into paid-up capital — hence "capitalisation of profits". The number of shares rises, but net worth is unchanged and each holder\'s percentage stays the same.',
                      'If the bonus would take paid-up capital beyond authorised capital, the company first increases its authorised capital by resolution in general meeting. A return of allotment with a copy of the resolution is filed with the Registrar.'],
             'analogy': 'Cutting a pizza into more slices: you have more pieces, but not more pizza.',
             'work': 'For listed clients a CA checks the bonus ratio, the record date and the sources used, and recomputes EPS for all periods presented, since a bonus changes share count retrospectively.'},
            {'id': 'c2', 'title': 'Sources for bonus — section 63(1) and Table F',
             'body': ['Fully paid bonus shares may be issued out of free reserves, the securities premium balance, or the capital redemption reserve. Reserves created by revaluation of assets can never be capitalised.',
                      'Free reserves (s. 2(43)) are reserves available for dividend as per the latest audited balance sheet; unrealised or notional gains, revaluation, and fair-value changes recognised in equity are excluded.',
                      'Securities premium and CRR may be used only for issuing unissued shares as fully paid bonus shares — not for paying up unpaid amounts on existing partly paid shares. Free reserves can be used for both (Table F, para 39).',
                      'SEBI requires a listed company to use only securities premium realised in cash; an unlisted company may use premium arising from non-cash issues too.'],
             'analogy': 'Three wallets may pay for bonus shares (free reserves, securities premium, CRR); the "revaluation" wallet holds only paper gains, so it is locked.',
             'work': 'A typical audit check: did the company use revaluation reserve or non-cash premium (if listed) for a bonus? Either is a violation that must be reported.'},
            {'id': 'c3', 'title': 'Conditions for a bonus issue — section 63(2) and (3)',
             'body': ['A company may capitalise profits or reserves for bonus only if: (a) its articles authorise it; (b) it is authorised in general meeting on the board\'s recommendation; (c) there is no default in paying interest or principal on fixed deposits or debt securities; (d) it has not defaulted on statutory dues of employees such as PF, gratuity and bonus; (e) partly paid shares outstanding on the allotment date are made fully paid; (f) it meets any other prescribed conditions.',
                      'Bonus shares cannot be issued in lieu of dividend (s. 63(3)). Once the board has announced a bonus recommendation, it cannot be withdrawn.'],
             'analogy': 'A bonus is like a family celebration — you must first clear the dues you owe to lenders and to the staff before you can hand out gifts.',
             'work': 'Before certifying a bonus, the company secretary and auditors check default status on deposits, debt securities and PF/gratuity — a single default blocks the issue.'},
            {'id': 'c4', 'title': 'Journal entries and effects of a bonus issue',
             'body': ['Fully paid bonus: (1) Capital Redemption Reserve / Securities Premium / General Reserve / Profit and Loss A/c Dr, To Bonus to Shareholders A/c; (2) Bonus to Shareholders A/c Dr, To Share Capital A/c.',
                      'Making partly paid shares fully paid (free reserves only): (1) General Reserve / Profit and Loss Dr, To Bonus to Shareholders; (2) Share Final Call Dr, To Share Capital; (3) Bonus to Shareholders Dr, To Share Final Call.',
                      '"Minimum reduction in free reserves" means use CRR and (eligible) securities premium first, then free reserves.',
                      'Effects: share capital up, accumulated reserves down by the same amount; net worth unchanged; EPS and other per-share values fall; market price adjusts downward; the market usually treats a bonus as a favourable sign.'],
             'analogy': 'Moving money from your savings jar to a locked jar labelled "capital" — your total money is the same, only the label changes.',
             'work': 'After a bonus, analysts restate per-share data (EPS, dividend per share) so trends remain comparable — a routine task in equity research.'},
            {'id': 'c5', 'title': 'Rights issue — section 62(1)(a) and its exceptions',
             'body': ['When a company (public or private) wants to increase subscribed capital by issuing further shares, it must first offer them to existing equity shareholders in proportion to their holding, so their control and governance rights are not diluted.',
                      'Letter of offer: states the number of shares and a period of not less than 15 days and not more than 30 days, after which the offer is deemed declined. Unless the articles provide otherwise, the shareholder may renounce the shares in favour of any other person. After the period (or on an earlier refusal), the board may dispose of the shares in a manner not disadvantageous to the shareholders and the company.',
                      'Exceptions (further shares need not be offered to existing holders): with a special resolution, to employees under an ESOP scheme; with a special resolution, to any persons for cash or other consideration at a price fixed by a registered valuer\'s report; on exercise of a conversion option attached to debentures or loans, if the terms were approved by special resolution before the issue (s. 62(3)); and where the Government directs conversion of its loans or debentures into shares in public interest (s. 62(4)).'],
             'analogy': 'Like a housing society offering a new parking slot first to existing residents in proportion to their flats before advertising it outside.',
             'work': 'Company law advisers draft the letter of offer, track the 15–30 day window, and record renunciations — errors here can make the allotment invalid.'},
            {'id': 'c6', 'title': 'Pricing a rights issue — book value, cum-right, ex-right and value of right',
             'body': ['Book value per share = net worth ÷ number of shares. Net worth (s. 2(57)) is paid-up capital plus reserves from profits and securities premium, less accumulated losses and unwritten-off deferred or miscellaneous expenditure; revaluation reserves, write-back of depreciation and amalgamation reserves are excluded. Market value can differ from book value.',
                      'Cum-right price: market price before the rights issue. Rights are usually offered below market price to attract response and reward existing holders.',
                      'Theoretical ex-right price (TERP) = (cum-right price × existing shares + issue price × rights shares) ÷ (existing shares + rights shares).',
                      'Value of right per existing share = cum-right price − TERP. Value of right per rights share = TERP − issue price. A holder who renounces sells this value; one who subscribes keeps it in the shares; one who ignores the offer loses it.'],
             'analogy': 'If a fruit seller mixes 4 mangoes worth ₹60 each with 1 mango bought at ₹45, the "average" mango is worth ₹57 — that is the ex-right price.',
             'work': 'Investment bankers and research analysts compute TERP to advise clients whether to subscribe, renounce or sell entitlements in the market.'},
            {'id': 'c7', 'title': 'Accounting for rights issue; advantages and disadvantages',
             'body': ['Entry: debit Bank A/c; credit Equity Share Capital A/c with face value and Securities Premium A/c with any premium. If money is collected in instalments, application/allotment accounts are used exactly as for any share issue.',
                      'A rights issue raises net worth and cash by (rights shares × issue price). Shares cannot be issued at a discount except as the law permits.',
                      'Advantages: existing holders keep their proportion and control; it deters management from issuing shares to friendly parties; holders are compensated for dilution by the lower price (or by selling the right); it saves the heavy expenses of a public issue; it is viewed positively; it has a better chance of success and is easier to handle.',
                      'Disadvantages: it dilutes the market value per share; the attractive price must be judged against the share\'s true worth.'],
             'analogy': 'A rights issue is a "members first" sale: discounted for those already in, with the option to hand your coupon to someone else.',
             'work': 'In due-diligence, the CA confirms that rights shares were allotted in the offer ratio and that renunciations were recorded correctly in the register of members.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Bonus issue with minimum reduction in free reserves (listed company)', 'difficulty': 'moderate', 'minutes': 12,
             'q': 'Sunrise Ltd (listed) has 60,000 equity shares of ₹10 each fully paid. Reserves: capital redemption reserve ₹40,000; securities premium ₹50,000 (₹30,000 collected in cash and ₹20,000 on shares issued to a vendor); general reserve ₹1,80,000; surplus ₹70,000; revaluation reserve ₹60,000. It decides to issue bonus shares of one for every three held, with the minimum reduction in free reserves. Journalise.',
             'solution': [rs_before, journal(E1, 'Journal of Sunrise Ltd', 'j1'),
                          wn('Working', f'Bonus shares = 60,000 ÷ 3 = {inr(nb)} = ₹{inr(vb)}. Use CRR ₹40,000 and cash-realised premium ₹30,000 first (not free reserves). Balance ₹{inr(gr)} from general reserve. Non-cash premium cannot be used by a listed company (SEBI) and revaluation reserve cannot be used by any company.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Making partly paid shares fully paid, then a bonus', 'difficulty': 'moderate', 'minutes': 12,
             'q': 'Kanak Ltd has 40,000 equity shares of ₹10 each, ₹8 paid up. Securities premium ₹60,000; general reserve ₹1,50,000. The company decides (i) to make the shares fully paid by a final call of ₹2 met out of general reserve, and (ii) then to issue fully paid bonus shares of one for every four held, using securities premium first. Journalise.',
             'solution': [journal(E2, 'Journal of Kanak Ltd', 'j2'),
                          wn('Why general reserve for step (i)?', 'Securities premium and CRR can be applied only to issue new fully paid bonus shares, not to pay unpaid amounts on existing shares. Free reserves such as general reserve can do both.'),
                          wn('Bonus', f'One for four on 40,000 = 10,000 shares = ₹{inr(b2)}: securities premium ₹60,000 + general reserve ₹40,000. General reserve left = 1,50,000 − 80,000 − 40,000 = ₹30,000.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Rights issue — ex-right price, value of right and the entry', 'difficulty': 'moderate', 'minutes': 10,
             'q': 'Vistar Ltd has 1,00,000 equity shares of ₹10 each quoted at ₹60 (cum-right). It offers rights shares of one for every four held at ₹45. Compute the theoretical ex-right price and the value of a right, and pass the entry assuming full subscription.',
             'solution': [wn('Ex-right price', f'Rights shares = 1,00,000 ÷ 4 = {inr(rs)}. TERP = (1,00,000 × 60 + 25,000 × 45) ÷ 1,25,000 = (60,00,000 + 11,25,000) ÷ 1,25,000 = ₹{inr(terp)}.'),
                          wn('Value of right', f'Per existing share = 60 − 57 = ₹{inr(vr_e)}. Per rights share = 57 − 45 = ₹{inr(vr_r)} (four existing shares × ₹3 = one rights share × ₹12).'),
                          journal(E3, 'Journal of Vistar Ltd', 'j3')],
             'checks': c3},
            {'id': 'i4', 'title': 'Subscribe, renounce or ignore? — the shareholder\'s view', 'difficulty': 'core', 'minutes': 8,
             'q': 'Continuing the previous illustration, Vani holds 400 shares. Show her position if she (a) subscribes, (b) renounces her rights at their value, (c) ignores the offer.',
             'solution': [ch, p('Subscribing or renouncing keeps her wealth at ₹24,000; ignoring the offer costs her ₹1,200 — the value of her 100 rights.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Board note on a proposed bonus issue', 'role': 'Finance manager of a listed mid-cap company',
             'situation': 'The board wants a 1:1 bonus. Equity capital is ₹20 crore; CRR ₹2 crore; securities premium ₹12 crore (of which ₹3 crore arose on a share-swap acquisition); general reserve ₹15 crore; revaluation reserve ₹8 crore. Authorised capital is ₹30 crore.',
             'steps': ['Bonus needed = ₹20 crore.',
                       'Eligible sources for a listed company: CRR ₹2 crore + cash-realised premium ₹9 crore + general reserve ₹9 crore.',
                       'Exclude revaluation reserve and the ₹3 crore non-cash premium.',
                       'Authorised capital must rise to at least ₹40 crore before allotment — propose the resolution.',
                       'Confirm no default on deposits, debt securities or employee statutory dues, and that there are no partly paid shares.'],
             'takeaway': 'A bonus note must show both the arithmetic of sources and the legal checklist of s. 63.',
             'checks': [{'expr': '20-2-9', 'value': 9, 'label': 'General reserve needed (₹ crore)'}, {'expr': '20+20', 'value': 40, 'label': 'Minimum authorised capital after bonus (₹ crore)'}]},
            {'id': 'j2', 'title': 'Advising a client on a rights entitlement', 'role': 'Practising CA advising an individual investor',
             'situation': 'A client holds 2,000 shares of a company announcing a 1:5 rights issue at ₹180 when the share trades at ₹240. She has no spare cash and asks what to do.',
             'steps': ['Compute TERP = (5 × 240 + 1 × 180) ÷ 6 = ₹230.',
                       'Value per rights share = 230 − 180 = ₹50; she is entitled to 400 rights.',
                       'If she ignores the offer, her shares lose ₹10 each (₹20,000 in all).',
                       'Advise her to renounce (sell) the entitlement for about ₹20,000, which offsets the fall.',
                       'Mention tax treatment of sale of rights entitlement as a separate point to check.'],
             'takeaway': 'Doing nothing in a rights issue is the only option that loses money.',
             'checks': [{'expr': '(5*240+180)/6', 'value': 230, 'label': 'TERP'}, {'expr': '400*(230-180)', 'value': 20000, 'label': 'Value of entitlement'}]},
        ],
        'mcqs': [
            mcq('m1', 'A shareholder holding 9,000 shares receives bonus shares in the ratio 2 : 3. Her holding after the bonus is:', ['15,000 shares', '6,000 shares', '13,500 shares', '12,000 shares'], 0,
                "A bonus ratio of 2 : 3 means 2 bonus shares for every 3 shares held. Bonus = 9,000 × 2/3 = 6,000 shares, so the holding becomes 9,000 + 6,000 = 15,000 shares. The trap 6,000 is only the bonus received, not the total holding; 13,500 reads the ratio as 1 for 2. In practice: when a listed company announces a bonus, demat accounts are credited automatically on the record date, and the share price adjusts downward.", 'c1', 'core', '9000+9000*2/3') | {'topic': "Bonus issue — capitalisation of profits"},
            mcq('m2', 'Bonus shares cannot be issued out of:', ['Revaluation reserve', 'Capital redemption reserve', 'Securities premium', 'General reserve'], 0,
                "Section 63(1) allows bonus shares out of free reserves, securities premium and capital redemption reserve. Its proviso forbids capitalising reserves created by revaluation of assets, because such gains are unrealised. The trap 'capital redemption reserve' is a permitted source even though it is a capital reserve. In practice: a company that revalues its land cannot use that revaluation gain to issue bonus shares, however large the reserve looks.", 'c2') | {'topic': "Sources for bonus — section 63(1) and Table F"},
            mcq('m3', 'Unpaid amounts on existing partly paid shares can be paid up out of:', ['Free reserves only', 'Securities premium', 'Capital redemption reserve', 'Revaluation reserve'], 0,
                "Securities premium and capital redemption reserve can be used only for issuing fully paid bonus shares. Paying up unpaid amounts on existing partly paid shares can be done only out of free reserves (as Table F permits). The trap 'securities premium' is allowed for new fully paid bonus shares, not for paying calls on existing ones. In practice: companies with partly paid shares usually make them fully paid before a bonus issue, as section 63(2) requires.", 'c2', 'moderate') | {'topic': "Sources for bonus — section 63(1) and Table F"},
            mcq('m4', 'For a listed company, securities premium can be used for a bonus issue only if:', ['It was realised in cash', 'It is more than ₹1 crore', 'It arose on a debenture issue', 'The bonus ratio is 1 : 1'], 0,
                "SEBI's ICDR Regulations allow a listed company to use securities premium for a bonus issue only if the premium was realised in cash. Premium arising, for example, on shares issued for assets or on amalgamation cannot be capitalised. The trap '₹1 crore' invents a limit. The Companies Act itself has no cash-realisation condition. In practice: merchant bankers check the source of securities premium before a listed company announces a bonus.", 'c2', 'moderate') | {'topic': "Sources for bonus — section 63(1) and Table F"},
            mcq('m5', 'Which of the following prevents a company from issuing bonus shares?', ['Default in payment of PF contribution to employees', 'Having a revaluation reserve', 'Having preference shares', 'Being an unlisted company'], 0,
                "Under section 63(2)(d), a company cannot issue bonus shares if it has defaulted in paying statutory dues of employees, such as PF contribution, gratuity or bonus. The trap 'having a revaluation reserve' does not bar a bonus — it only cannot be the source of one. Preference shares and being unlisted are also irrelevant. In practice: auditors and company secretaries confirm that statutory employee dues are up to date before the board recommends a bonus.", 'c3') | {'topic': "Conditions for a bonus issue — section 63(2) and (3)"},
            mcq('m6', 'Bonus shares under section 63(3):', ['Cannot be issued in lieu of dividend', 'May replace the final dividend', 'Can be withdrawn after announcement', 'Can be partly paid'], 0,
                "Section 63(3) says bonus shares cannot be issued in lieu of dividend. SEBI rules for listed companies add that, once announced, a bonus cannot be withdrawn. Bonus shares are always fully paid. The trap 'may replace the final dividend' is exactly what the law forbids — a bonus does not distribute cash, so it cannot substitute for one. In practice: companies often announce both a dividend and a bonus, but the bonus never replaces the cash payout.", 'c3') | {'topic': "Conditions for a bonus issue — section 63(2) and (3)"},
            mcq('m7', 'Capital ₹5,00,000 (₹10 shares); CRR ₹30,000; securities premium (cash) ₹45,000; general reserve ₹2,00,000. For a 1 : 2 bonus with minimum reduction in free reserves, general reserve used is:', ['₹1,75,000', '₹2,00,000', '₹2,50,000', '₹1,30,000'], 0,
                "Existing shares = 5,00,000 ÷ 10 = 50,000. A 1 : 2 bonus = 25,000 shares × ₹10 = ₹2,50,000. To minimise use of free reserves, first use CRR ₹30,000 and securities premium ₹45,000 (realised in cash). General reserve needed = 2,50,000 − 30,000 − 45,000 = ₹1,75,000. The trap ₹2,50,000 uses general reserve for the whole bonus. In practice: companies preserve free reserves, which can pay dividends, by capitalising capital reserves first.", 'c4', 'moderate', '250000-30000-45000') | {'topic': "Journal entries and effects of a bonus issue"},
            mcq('m8', 'The effect of a bonus issue on net worth is:', ['No change', 'Increase by the bonus amount', 'Decrease by the bonus amount', 'Increase by the premium'], 0,
                "A bonus issue transfers reserves to share capital: reserves fall and share capital rises by the same amount. No cash comes in or goes out, so net worth (shareholders' funds) is unchanged. The trap 'increase by the bonus amount' counts the capital increase but forgets the matching fall in reserves. In practice: after a bonus, each shareholder holds more shares but the total value of the holding is the same, as the share price adjusts.", 'c4') | {'topic': "Journal entries and effects of a bonus issue"},
            mcq('m9', 'Under section 62(1)(a), the rights offer must remain open for:', ['Not less than 15 days and not more than 30 days', 'Exactly 21 days', 'Not less than 30 days', 'Up to 60 days'], 0,
                "Section 62(1)(a)(i) requires the rights offer notice to give shareholders a period of not less than 15 days and not more than 30 days to accept (the law allows a shorter period where prescribed). The trap 'exactly 21 days' is the general meeting notice period, not the rights offer period. In practice: shareholders receive a letter of offer stating the opening and closing dates; failure to respond within the window treats the offer as declined.", 'c5') | {'topic': "Rights issue — section 62(1)(a) and its exceptions"},
            mcq('m10', 'Shares are quoted at ₹90 cum-right. A rights issue of 1 for 2 at ₹60 is made. The theoretical ex-right price is:', ['₹80', '₹75', '₹85', '₹70'], 0,
                "Theoretical ex-right price = (market value of existing shares + money paid for rights shares) ÷ total shares. For every 2 shares at ₹90, 1 new share at ₹60: (2 × 90 + 1 × 60) ÷ 3 = 240 ÷ 3 = ₹80. The trap ₹75 simply averages 90 and 60, ignoring that existing shares outnumber rights shares 2 : 1. In practice: stock exchanges adjust a share's price on the ex-right date roughly to this theoretical value.", 'c6', 'moderate', '(2*90+60)/3') | {'topic': "Pricing a rights issue — book value, cum-right, ex-right and value of right"},
            mcq('m11', 'In the previous question, the value of a right per existing share is:', ['₹10', '₹20', '₹30', '₹15'], 0,
                "Value of a right per existing share = cum-right price − ex-right price = 90 − 80 = ₹10. Per rights share, it is ex-right price − issue price = 80 − 60 = ₹20, and since 1 rights share comes with 2 existing shares, ₹20 ÷ 2 = ₹10 per existing share. The trap ₹20 is the value per rights share. In practice: shareholders who don't want to invest can sell (renounce) their rights entitlements on the exchange for roughly this value.", 'c6', 'moderate', '90-80') | {'topic': "Pricing a rights issue — book value, cum-right, ex-right and value of right"},
            mcq('m12', '50,000 rights shares of ₹10 each are issued at ₹32. Securities Premium is credited with:', ['₹11,00,000', '₹16,00,000', '₹5,00,000', '₹32,00,000'], 0,
                "Premium per share = issue price 32 − face value 10 = ₹22. Securities premium = 22 × 50,000 = ₹11,00,000. Share capital is credited with ₹5,00,000. The trap ₹16,00,000 is the total amount received (32 × 50,000); ₹5,00,000 is the face value. In practice: rights issues by established companies are usually priced at a premium but at a discount to market, to attract existing shareholders.", 'c7', 'core', '50000*22') | {'topic': "Accounting for rights issue; advantages and disadvantages"},
            mcq('m13', 'Net worth ₹1,50,00,000 and 6,00,000 equity shares. Book value per share is:', ['₹25', '₹2.50', '₹15', '₹40'], 0,
                "Book value per share = net worth ÷ number of equity shares = 1,50,00,000 ÷ 6,00,000 = ₹25. The trap ₹2.50 is a decimal slip from miscounting the zeros in ₹1.5 crore. In practice: analysts compare book value with market price (price-to-book ratio) when judging whether a rights issue price is reasonable.", 'c6', 'core', '15000000/600000') | {'topic': "Pricing a rights issue — book value, cum-right, ex-right and value of right"},
        ],
        'questions': [
            {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'journal',
             'q': 'The balance sheet of Tarang Ltd (listed) shows: 80,000 equity shares of ₹10 each fully paid ₹8,00,000; capital redemption reserve ₹90,000; securities premium ₹75,000 (of which ₹25,000 arose on shares issued for a machine); general reserve ₹2,50,000; revaluation reserve ₹1,00,000. The company decides to issue bonus shares of 2 for every 5 held, with the minimum reduction in free reserves. Pass journal entries and state the balance of general reserve after the bonus.',
             'model': [journal(Q1, 'Journal of Tarang Ltd', 'jq1'),
                       wn('Working', f'Bonus shares = 80,000 × 2/5 = 32,000 = ₹{inr(q1_b)}. Sources in order: CRR ₹90,000; securities premium realised in cash ₹50,000 (the ₹25,000 non-cash premium cannot be used by a listed company); general reserve ₹{inr(q1_gr)}. Revaluation reserve is not available. General reserve left = ₹70,000.')],
             'checks': q1c,
             'scheme': [S('s1', 'Number and value of bonus shares (32,000; ₹3,20,000)', 1, 'computation'),
                        S('s2', 'CRR used fully and only cash-realised premium ₹50,000 used', 1.5, 'concept'),
                        S('s3', 'General reserve ₹1,80,000; revaluation reserve excluded', 1.5, 'computation'),
                        S('s4', 'Two journal entries through Bonus to Shareholders A/c with narrations', 1, 'posting'),
                        S('s5', 'Closing general reserve ₹70,000', 1, 'computation')],
             'remarks': ['Most candidates used the full ₹75,000 premium — the SEBI cash-realisation condition was overlooked.', 'Some debited revaluation reserve; this is never allowed.'],
             'mistakes': ['Using general reserve before CRR when minimum reduction in free reserves is asked.', 'Crediting share capital directly without the Bonus to Shareholders account (acceptable but loses the narration mark if unexplained).'],
             'tips': ['List reserves in the order: CRR → eligible premium → free reserves.', 'State why each excluded reserve is excluded — it earns concept marks.']},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'text',
             'q': 'State the sources out of which bonus shares can be issued and the conditions a company must satisfy under section 63 of the Companies Act, 2013.',
             'model': [p('Sources (s. 63(1)): free reserves; securities premium account; capital redemption reserve account. Reserves created by revaluation of assets cannot be capitalised.'),
                       ul(['Authorised by the articles.', 'Authorised in general meeting on the recommendation of the board.', 'No default in payment of interest or principal on fixed deposits or debt securities.',
                           'No default in statutory dues of employees such as PF, gratuity and bonus.', 'Partly paid shares outstanding on the date of allotment made fully paid.', 'Other prescribed conditions complied with.',
                           'Bonus shares cannot be issued in lieu of dividend; a bonus announced by the board cannot be withdrawn.'])],
             'scheme': [S('s1', 'Three sources', 1.5, 'provision'), S('s2', 'Revaluation reserve excluded', 0.5, 'provision'), S('s3', 'At least five conditions of s. 63(2)', 2.5, 'provision'), S('s4', 'Not in lieu of dividend / no withdrawal', 0.5, 'provision')],
             'remarks': ['Answers that list only sources lose half the marks.'],
             'mistakes': ['Listing "capital reserve" or "revaluation reserve" as a source.'],
             'tips': ['Separate the answer into "sources" and "conditions" with sub-headings.']},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'journal',
             'q': 'Pragati Ltd has 2,40,000 equity shares of ₹10 each quoted at ₹120 cum-right. It makes a rights issue of 1 share for every 6 held at ₹85. Calculate (a) the number of rights shares, (b) the theoretical ex-right price, (c) the value of right per existing share and per rights share, and (d) pass the journal entry for the rights issue, assuming full subscription.',
             'model': [p(f'(a) Rights shares = 2,40,000 ÷ 6 = {inr(q3_r)}.'),
                       p(f'(b) TERP = (2,40,000 × 120 + 40,000 × 85) ÷ 2,80,000 = (2,88,00,000 + 34,00,000) ÷ 2,80,000 = ₹{inr(q3_t)}.'),
                       p(f'(c) Per existing share = 120 − 115 = ₹{inr(q3_ve)}; per rights share = 115 − 85 = ₹{inr(q3_vr)} (6 × ₹5 = ₹30).'),
                       journal([je('(d)', [('Bank A/c', q3_cash)], [('Equity Share Capital A/c', 400000), ('Securities Premium A/c', 3000000)], 'Being 40,000 rights shares of ₹10 each issued at ₹85')], 'Journal of Pragati Ltd', 'jq3')],
             'checks': q3c,
             'scheme': [S('s1', 'Rights shares 40,000', 0.5, 'computation'), S('s2', 'TERP ₹115 with formula', 1.5, 'computation'),
                        S('s3', 'Value of right ₹5 per existing share and ₹30 per rights share', 1.5, 'computation'), S('s4', 'Entry: Bank ₹34,00,000; Capital ₹4,00,000; Premium ₹30,00,000', 1.5, 'posting')],
             'remarks': ['Candidates often average the two prices (₹102.50) instead of weighting by number of shares.'],
             'mistakes': ['Crediting the whole ₹85 to share capital.', 'Confusing value per existing share with value per rights share.'],
             'tips': ['Write the TERP formula before substituting figures.']},
            {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
             'q': 'Distinguish between a bonus issue and a rights issue (four points).',
             'model': [table(['Basis', 'Bonus issue', 'Rights issue'], [
                 ['Consideration', 'Free of cost to shareholders', 'Shareholders pay the issue price'],
                 ['Funds', 'No new funds; reserves capitalised', 'Raises fresh cash for the company'],
                 ['Provision', 'Section 63', 'Section 62(1)(a)'],
                 ['Renunciation', 'No right to renounce in favour of others', 'Right to renounce unless the articles prohibit'],
                 ['Net worth', 'Unchanged', 'Increases by rights shares × issue price'],
                 ['Nature of shares', 'Always fully paid', 'May be partly paid, payable in instalments']])],
             'scheme': [S('s1', 'Point 1', 1, 'concept'), S('s2', 'Point 2', 1, 'concept'), S('s3', 'Point 3', 1, 'concept'), S('s4', 'Point 4', 1, 'concept')],
             'remarks': ['The effect on net worth is the most frequently missed point.'],
             'mistakes': ['Saying bonus shares raise capital funds for the company.'],
             'tips': ['Use a three-column table; quote the sections.']},
        ],
        'viva': viva,
        'cases': cases,
        'revision': {
            'summary': ['Bonus = free fully paid shares to existing holders pro rata; capitalisation of profits; net worth unchanged.',
                        'Sources (s. 63(1)): free reserves, securities premium, CRR — never revaluation reserve. Listed companies: only cash-realised premium (SEBI).',
                        'Partly paid shares can be made fully paid only from free reserves.',
                        'Conditions (s. 63(2)): articles, GM approval on board recommendation, no default on deposits/debt securities or employee dues, partly paid shares made fully paid; not in lieu of dividend; no withdrawal once announced.',
                        'Rights (s. 62(1)(a)): offer to existing holders pro rata, 15–30 days, renounceable unless articles prohibit.',
                        'TERP = (cum-right price × existing + issue price × rights) ÷ total shares; value of right = cum-right − TERP (per existing share).'],
            'remember': ['Bonus entry passes through Bonus to Shareholders A/c.', '"Minimum reduction in free reserves" → CRR and eligible premium first.', 'A rights issue increases net worth; a bonus issue does not.'],
            'traps': ['Using revaluation reserve or non-cash premium (listed) for bonus.', 'Using securities premium to pay up partly paid shares.', 'Simple average instead of weighted average for TERP.'],
        },
        'quickref': [
            {'k': 'Bonus shares', 'v': 'Existing shares × bonus ratio'},
            {'k': 'Sources — s. 63(1)', 'v': 'Free reserves, securities premium, CRR; not revaluation reserve'},
            {'k': 'Bonus entries', 'v': 'Reserves Dr To Bonus to Shareholders; Bonus to Shareholders Dr To Share Capital'},
            {'k': 'Partly paid → fully paid', 'v': 'Free reserves Dr To Bonus to Shareholders; Final Call Dr To Share Capital; Bonus to Shareholders Dr To Final Call'},
            {'k': 'Rights offer — s. 62(1)(a)', 'v': '15–30 days; renounceable unless articles prohibit; board disposes of unaccepted shares'},
            {'k': 'TERP', 'v': '(Cum-right price × existing shares + issue price × rights shares) ÷ (existing + rights shares)'},
            {'k': 'Value of right', 'v': 'Per existing share = cum-right − TERP; per rights share = TERP − issue price'},
            {'k': 'Book value per share', 'v': 'Net worth (s. 2(57)) ÷ number of shares'},
            {'k': 'Rights entry', 'v': 'Bank Dr To Equity Share Capital To Securities Premium'},
        ],
    }


# ---- offline auto-check: kw/min (viva matcher), nums (figures that must appear), rows ([account, side, amount]) ----
# "any N" question: every point carries the same groups with min = 1 … N (N distinct correct points earn N marks).
_BR = ['free of cost|free|without payment|no payment|pay|price|consideration|cost', 'fresh cash|new funds|raise funds|raises funds|no funds|fresh funds|capitalis|capitaliz|cash inflow|funds',
       '63|62', 'renounce|renunciation', 'net worth|networth', 'fully paid|partly paid']
AUTO = {
    'q1': {'extra_ok': False,
           's1': {'nums': [32000, 320000]},
           's2': {'rows': [['capital redemption|crr', 'dr', 90000], ['premium', 'dr', 50000]],
                  'wrong': [{'kw': ['155000|95000'], 'say': 'A listed company cannot use the ₹25,000 premium that arose on shares issued for a machine (not realised in cash); only ₹50,000 of premium is available.'}]},
           's3': {'rows': [['general reserve', 'dr', 180000]],
                  'wrong': [{'kw': ['revaluation reserve dr|revaluation reserve 100000 dr|revaluation reserve account dr'], 'say': 'Revaluation reserve cannot be used for a bonus issue.'}]},
           's4': {'kw': ['bonus to shareholders|bonus shareholders|bonus to equity shareholders'], 'rows': [['bonus', 'cr', 320000], ['bonus', 'dr', 320000], ['capital', 'cr', 320000]]},
           's5': {'nums': [70000]}},
    'q2': {'extra_ok': True,
           's1': {'kw': ['free reserve', 'securities premium|premium', 'capital redemption reserve|crr'], 'min': 3},
           's2': {'kw': ['revaluation not|not revaluation|revaluation cannot|cannot revaluation|revaluation excluded|excluding revaluation|except revaluation|other than revaluation|revaluation not allowed|revaluation reserve not|no revaluation']},
           's3': {'kw': ['articles', 'general meeting|recommendation of board|board', 'default fixed deposit|default interest|default principal|fixed deposit|debt securities|default repayment|no default deposit|no default fixed|not defaulted deposit|not defaulted fixed|no default debt|no default interest',
                         'statutory dues|provident fund|gratuity|employees|no default provident|no default statutory|no default pf|not defaulted provident|no default employee|not defaulted statutory|no default gratuity', 'partly paid', 'prescribed|other conditions'], 'min': 5},
           's4': {'kw': ['not lieu dividend|cannot lieu dividend|not in lieu|not instead dividend|not substitute dividend|cannot instead dividend|not withdrawn|cannot withdrawn|not be withdrawn|irrevocable']}},
    'q3': {'extra_ok': False,
           's1': {'nums': [40000]},
           's2': {'kw': ['280000|28800000|3400000|32200000'], 'nums': [115],
                  'wrong': [{'kw': ['102.5'], 'say': 'TERP is a weighted average by number of shares: (2,40,000 × 120 + 40,000 × 85) ÷ 2,80,000 = ₹115, not a simple average.'}]},
           's3': {'kw': ['115 5|120 115 5|5 per existing|5 per share|right 5|existing share 5|5 per old share', '85 30|30 per right|rights share 30|right share 30|6 5 30|30 per new share'], 'min': 2},
           's4': {'rows': [['bank', 'dr', 3400000], ['capital', 'cr', 400000], ['premium', 'cr', 3000000]]}},
    'q4': dict({'extra_ok': True}, **{f's{n}': {'kw': _BR, 'min': n} for n in range(1, 5)}),
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
