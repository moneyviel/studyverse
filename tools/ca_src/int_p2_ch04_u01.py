"""CA Intermediate · Paper 2 Corporate and Other Laws · Chapter 4 Share Capital and Debentures (ss. 43–72).
Scope follows the ICAI study material; provisions are explained in original words; examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p2-ch04-u01'
T1 = 'Kinds of share capital, DVRs and voting rights (ss. 43, 44, 47)'
T2 = 'Share certificates and variation of class rights (ss. 45, 46, 48)'
T3 = 'Calls, securities premium, discount and sweat equity (ss. 49-54)'
T4 = 'Preference shares and their redemption (s. 55)'
T5 = 'Transfer, transmission and refusal (ss. 56-59)'
T6 = 'Alteration, further issue and bonus shares (ss. 61-64)'
T7 = 'Reduction, financial assistance and buy-back (ss. 66-70)'
T8 = 'Debentures and nomination (ss. 71-72)'


def build():
    # i1 — buy-back limits
    ck = Checks()
    agg = ck.add('8+12', 'Paid-up equity capital + free reserves (₹ crore)')
    lim = ck.add('20*25/100', 'Maximum buy-back amount: 25% of aggregate (₹ crore)')
    brd = ck.add('20*10/100', 'Board-only limit: 10% (₹ crore)')
    shs = ck.add('5*10000000/50', 'Shares bought back at ₹50 each')
    cap = ck.add('8*10000000/10*25/100', 'Equity limit: 25% of 80,00,000 shares in the year')
    post = ck.add('2*(20-5)', 'Twice capital and free reserves after the buy-back (₹ crore)')
    crr = ck.add('1000000*10/10000000', 'Transfer to capital redemption reserve: nominal value of shares bought (₹ crore)')
    i1 = {'id': 'i1', 'title': 'How large a buy-back?', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'Sarovar Ltd. has paid-up equity capital of ₹8 crore (₹10 shares), free reserves including securities premium of ₹12 crore and total debts of ₹24 crore. It wants to buy back shares at ₹50 each out of free reserves. (a) What is the maximum amount? (b) Who must approve it? (c) Is the debt condition met at the maximum? (d) What must be transferred to the capital redemption reserve?',
          'solution': [table(['Test', 'Working', 'Result'], [
              ['Aggregate base', '₹8 crore + ₹12 crore', f'₹{R(agg)} crore'],
              ['(a) 25% limit', '25% × ₹20 crore', f'₹{R(lim)} crore = {R(shs)} shares at ₹50'],
              ['Equity share count limit', '25% of 80,00,000 shares', f'{R(cap)} shares — not breached'],
              ['(b) Approval', f'Above the Board-only limit of ₹{R(brd)} crore', 'Special resolution in general meeting (articles must permit)'],
              ['(c) Debt test', f'Debts ₹24 crore vs 2 × ₹15 crore = ₹{R(post)} crore', 'Met'],
              ['(d) CRR (s. 69)', '10,00,000 shares × ₹10', f'₹{R(crr)} crore']], title='Section 68 and 69 limits'),
              note('The offer must stay open for 15 to 30 days, the buy-back must finish within one year of the resolution, and the company cannot issue the same kind of shares for six months afterwards (bonus issues and existing obligations excepted).')],
          'checks': list(ck)}

    # i2 — redemption of preference shares
    ck2 = Checks()
    crr2 = ck2.add('60-35', 'Redeemed out of profits (₹ lakh) = amount to capital redemption reserve')
    prem = ck2.add('60*5/100', 'Premium on redemption at 5% (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Redeeming preference shares', 'difficulty': 'core', 'minutes': 6,
          'q': 'Nilgiri Foods Ltd. must redeem fully paid preference shares of ₹60 lakh at a 5% premium. It raises ₹35 lakh by a fresh equity issue for the purpose and uses profits for the rest. How much goes to the capital redemption reserve, how much premium is payable and where may it come from?',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Out of fresh issue', '', R(35)],
              ['Out of profits → capital redemption reserve', '60 − 35', R(crr2)],
              ['Premium on redemption', '5% × 60', R(prem)]], title='Section 55'),
              p('The premium is provided out of profits or, as allowed for the class of company, the securities premium account. The capital redemption reserve may later be used only to issue fully paid bonus shares.')],
          'checks': list(ck2)}

    cert = table(['Event', 'Certificates to be delivered within'], [
        ['Subscribers to the memorandum', '2 months of incorporation'],
        ['Allotment of shares', '2 months of allotment'],
        ['Transfer or transmission', '1 month of receiving the transfer instrument or intimation'],
        ['Allotment of debentures', '6 months of allotment']], title='Section 46 / 56(4) timelines')
    bb = table(['Condition', 'Rule'], [
        ['Source', 'Free reserves, securities premium, or proceeds of a different kind of issue'],
        ['Approval', 'Articles must permit; Board resolution up to 10%, otherwise special resolution'],
        ['Size', 'Up to 25% of paid-up capital + free reserves; equity bought back ≤ 25% of paid-up equity in a year'],
        ['Debt', 'Debts not more than twice paid-up capital + free reserves after buy-back'],
        ['Shares', 'Only fully paid shares'],
        ['Time', 'Complete within 1 year of the resolution; next offer only after 1 year'],
        ['After', 'Extinguish the shares; no fresh issue of same kind for 6 months; transfer nominal value to CRR if paid from reserves']], title='Buy-back at a glance (s. 68)')

    concepts = [
        C('c1', T1, [
            'Section 43: share capital of a company limited by shares is of two kinds — equity and preference. Preference shares carry a preferential right to a fixed dividend and to repayment of capital in a winding up. Equity shares may carry ordinary voting rights or differential rights as to dividend, voting or otherwise (DVRs).',
            'DVRs need authority in the articles, an ordinary resolution of shareholders (postal ballot for a listed company), voting power of DVRs not above 74% of total voting power, and no default in filing annual accounts and returns or in repaying deposits, debentures or dividend.',
            'Section 44: shares are movable property, transferable as the articles provide. Section 47: an equity holder votes in proportion to paid-up equity. A preference holder votes only on resolutions directly affecting his rights (including winding up and reduction of capital), and on every resolution if his dividend has been unpaid for two years or more.'],
          'Equity owns the risk and the vote; preference trades the vote for priority.',
          'A preference holder may vote on a reduction of capital but not on appointing an auditor — unless dividends are two years in arrears.'),
        C('c2', T2, [
            'Section 45: every share has a distinguishing number, except shares held with a depository. Section 46: a certificate issued under the common seal (if any) or signed by two directors, or a director and the company secretary, is prima facie evidence of title. Duplicates can be issued if the original is lost, destroyed, defaced or surrendered.',
            'Issuing a duplicate certificate to defraud is punishable as fraud under section 447.',
            'Section 48: class rights may be varied with written consent of holders of three-fourths of the issued shares of that class, or by a special resolution at a separate class meeting, if the memorandum or articles allow it (or the terms of issue do not prohibit it). Holders of at least 10% of the class who did not consent may apply to the Tribunal within 21 days; the variation then waits for confirmation.'],
          'A certificate proves ownership; class rights cannot be changed without the class agreeing.',
          'A three-fourths consent of preference holders allows the dividend rate to be cut, unless 10% dissenters win at the Tribunal.',
          blocks=[cert]),
        C('c3', T3, [
            'Section 49: calls on shares of a class must be made uniformly on all shares of that class. Section 50: a company may accept unpaid amounts in advance if the articles allow, but the member gets no voting rights on that advance until it is called. Section 51: if the articles allow, dividend may follow the paid-up value of each share rather than its face value.',
            'Section 52: premium received goes to the securities premium account and may be used only to issue fully paid bonus shares, write off preliminary expenses, write off issue expenses or commission or discount on shares or debentures, provide the premium on redemption of preference shares or debentures, and buy back securities.',
            'Section 53: shares cannot be issued at a discount; such an issue is void. Exceptions: sweat equity shares, and shares issued to creditors on converting debt under a statutory restructuring scheme.',
            'Section 54: sweat equity shares are issued to directors or employees at a discount or for non-cash consideration for know-how or value addition. Conditions include a special resolution stating the number, price and recipients, and compliance with SEBI rules (listed) or the prescribed rules (unlisted). They rank equally with other equity shares.'],
          'Premium is capital in disguise, so its uses are tightly limited.',
          'Using securities premium to pay an equity dividend is not allowed.'),
        C('c4', T4, [
            'Section 55: a company cannot issue irredeemable preference shares. Redeemable preference shares must be redeemed within 20 years of issue; companies in infrastructure projects may go up to 30 years if at least 10% are redeemed every year from the 21st year (or earlier).',
            'Redemption is allowed only for fully paid shares and only out of profits available for dividend or the proceeds of a fresh issue made for the purpose.',
            'When redemption is made out of profits, an equal amount is transferred to the capital redemption reserve, which may be used only to issue fully paid bonus shares. Premium on redemption comes from profits or, where allowed, the securities premium account.',
            'If a company cannot redeem, it may, with consent of holders of three-fourths in value of those shares and the Tribunal\'s approval, issue fresh redeemable preference shares for the sum still owed, dividend included. The unredeemed shares are then treated as redeemed.'],
          'A preference share always has an exit date.',
          'A road-building company may issue 25-year preference shares if it redeems a tenth each year from year 21.'),
        C('c5', T5, [
            'Section 56: a transfer of securities (other than in a depository) is registered only on a proper instrument of transfer, duly stamped and executed by both parties, delivered within 60 days of execution with the certificate. Transmission by operation of law (death, insolvency) needs only an intimation.',
            'If partly paid shares are transferred on the transferor\'s application, the company must give notice to the transferee, who may object within two weeks.',
            'Section 58: if a private company refuses to register, or a public company refuses for sufficient cause, notice of refusal must be sent within 30 days. The transferee may appeal to the Tribunal within 30 days of receiving the notice, or within 60 days of delivering the instrument if no notice is sent.',
            'Section 59: if a name is entered or omitted in the register without sufficient cause, the aggrieved person or the company may apply to the Tribunal (or a foreign authority for a foreign register) for rectification. Section 57: personating a shareholder to obtain securities or dividend is punishable.'],
          'Transfer is a voluntary act; transmission happens by law.',
          'A buyer whose transfer is refused without notice has 60 days from delivery to approach the Tribunal.'),
        C('c6', T6, [
            'Section 61: if the articles permit, a company may by ordinary resolution increase authorised capital, consolidate or divide shares (consolidation that changes voting percentages needs the Tribunal), convert fully paid shares into stock and back, sub-divide shares, and cancel unissued shares. Section 64 requires notice to the Registrar within 30 days; default costs ₹500 a day up to ₹5 lakh for the company and ₹1 lakh for an officer.',
            'Section 62: further shares go first to existing equity holders as a rights offer in proportion to their holding, open for at least 15 and at most 30 days, with a right to renounce unless the articles say otherwise. Shares may also be issued to employees under a stock option scheme or to any persons, by special resolution, subject to valuation where required.',
            'Section 63: bonus shares can be issued only from free reserves, securities premium or capital redemption reserve — never from revaluation reserves — and never in lieu of dividend. Conditions: articles authorise; Board recommends and the general meeting approves; no default on deposits, debt securities or statutory employee dues; partly paid shares made fully paid first. Once announced, the issue cannot be withdrawn.'],
          'New shares are first offered to existing owners, and bonuses must come from genuine reserves.',
          'A company that has defaulted on PF dues cannot issue bonus shares until the default is cleared.'),
        C('c7', T7, [
            'Section 66: a company may reduce share capital by special resolution confirmed by the Tribunal — for example extinguishing uncalled liability, cancelling lost capital or returning surplus capital. The Tribunal notifies the Central Government, the Registrar, SEBI (for listed companies) and creditors, who have three months to object. No reduction is allowed while deposits or interest on them are in arrears.',
            'Section 67: a company cannot buy its own shares except under the Act, and a public company cannot give financial assistance to anyone for buying its shares or its holding company\'s shares. Exceptions include lending by a bank in the ordinary course, funding an employee share trust, and loans to employees (other than directors or KMP) of up to six months\' salary to buy fully paid shares.',
            'Sections 68–70: buy-back conditions are summarised in the table. When shares are bought back out of free reserves or securities premium, their nominal value is transferred to the capital redemption reserve (s. 69). No buy-back is allowed through subsidiaries or investment companies, or while there is a default in repaying deposits, debentures, term loans or dividends (s. 70).'],
          'Capital can be returned only through doors the Act opens, with creditors watching.',
          'A company still defaulting on a bank term loan cannot launch a buy-back, even with surplus cash.',
          blocks=[bb]),
        C('c8', T8, [
            'Section 71: a company may issue debentures, convertible in whole or part with a special resolution, but debentures carry no voting rights.',
            'A debenture trustee must be appointed before a prospectus or offer of debentures to the public or to more than 500 persons; the trust deed is executed in Form SH-12 within three months of the closure of the issue. A debenture redemption reserve is created out of profits where the rules require; for partly convertible debentures, only the non-convertible portion counts.',
            'If a company fails to redeem debentures on maturity or pay interest, the Tribunal may order redemption on application by the trustee or holders.',
            'Section 72: every holder of securities may nominate a person to whom the securities pass on death; a nominee for a minor holder can be named, and the nomination overrides other claims on the securities.'],
          'A debenture holder is a lender with a trustee, not an owner with a vote.',
          'A company offering debentures to 800 investors must appoint a trustee before the offer.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Planning a buy-back', 'role': 'Secretarial associate',
         'situation': 'A client company with surplus cash wants to buy back shares.',
         'steps': ['Check articles and any default in deposits, loans or dividends.', 'Compute the 25% and debt limits.', 'Decide Board vs special resolution.', 'Plan the 15–30 day offer, 1-year completion and 6-month bar on fresh issue.'],
         'takeaway': 'Limits and defaults decide whether a buy-back is possible at all.'},
        {'id': 'j2', 'title': 'Refused transfer', 'role': 'Article assistant',
         'situation': 'An investor\'s share transfer in a private company was neither registered nor refused for six weeks.',
         'steps': ['Note the date the instrument was delivered.', 'Confirm whether notice of refusal was sent within 30 days.', 'Advise appeal within 60 days of delivery if no notice.'],
         'takeaway': 'Time limits under section 58 run from notice or delivery.'},
    ]

    mcqs = [
        Q('m1', 'The voting power of equity shares with differential rights cannot exceed what share of total voting power?', ['74%', '26%', '51%', '50%'], 0,
          'The rules for DVRs cap their voting power at 74% of the total voting power, including DVRs issued at any time. The issue also needs authority in the articles and an ordinary resolution. In practice: compute the post-issue voting split.', 'c1', T1, 'core', check=74),
        Q('m2', 'A preference shareholder can vote on all resolutions when:', ['His dividend has been unpaid for two years or more', 'He holds more than 10% of preference capital', 'The company is private', 'The articles say so'], 0,
          'Normally preference holders vote only on resolutions directly affecting their rights, such as winding up or reduction of capital. If their dividend remains unpaid for two years or more, they vote on every resolution. In practice: track dividend arrears.', 'c1', T1),
        Q('m3', 'Share certificates on allotment of shares must be delivered within:', ['Two months of allotment', 'One month of allotment', 'Six months of allotment', 'Fifteen days of allotment'], 0,
          'Section 46 read with section 56(4) requires certificates within two months of allotment and of incorporation for subscribers, one month for transfers and transmissions, and six months for debentures. In practice: dematerialised holdings are credited instead.', 'c2', T2),
        Q('m4', 'Holders of what minimum proportion of a class who did not consent to a variation may apply to the Tribunal?', ['10% of the issued shares of that class', '25% of the class', '5% of total capital', 'Any single holder'], 0,
          'Section 48 lets holders of at least 10% of the issued shares of the class, who did not consent or vote for the variation, apply to the Tribunal within 21 days. The variation then waits for the Tribunal\'s confirmation. In practice: count dissenters early.', 'c2', T2),
        Q('m5', 'Money paid in advance of calls by a member:', ['Carries no voting rights until called', 'Carries full voting rights', 'Must be refunded', 'Is treated as a loan to a director'], 0,
          'Section 50 allows a company, if its articles permit, to accept unpaid share money in advance, but the member cannot vote on the advance until it becomes payable through a call. Interest may be paid as the articles provide. In practice: record advances separately.', 'c3', T3),
        Q('m6', 'Securities premium may be used for:', ['Writing off preliminary expenses', 'Paying an equity dividend', 'Writing off bad debts', 'Paying directors\' fees'], 0,
          'Section 52 restricts the premium to fully paid bonus shares, preliminary expenses, issue expenses and discounts, premium on redemption of preference shares or debentures, and buy-back. Dividends and operating costs are excluded. In practice: treat premium like capital.', 'c3', T3),
        Q('m7', 'An issue of shares at a discount, other than permitted cases, is:', ['Void', 'Valid if approved by special resolution', 'Valid for private companies', 'Voidable at the shareholder\'s option'], 0,
          'Section 53 prohibits issuing shares at a discount and declares such an issue void. The exceptions are sweat equity shares and shares issued to creditors when debt is converted under a statutory restructuring. In practice: price at or above face value.', 'c3', T3),
        Q('m8', 'The longest tenure for redeemable preference shares of a non-infrastructure company is:', ['20 years', '10 years', '30 years', 'No limit'], 0,
          'Section 55 requires redemption within 20 years. Only companies in infrastructure projects may go up to 30 years, provided they redeem at least 10% each year from the 21st year. In practice: plan the redemption fund.', 'c4', T4, 'core', check=20),
        Q('m9', 'Preference shares of ₹40 lakh are redeemed: ₹15 lakh from a fresh issue and the rest from profits. Transfer to capital redemption reserve:', ['₹25 lakh', '₹40 lakh', '₹15 lakh', 'Nil'], 0,
          'When redemption is out of profits, a sum equal to the nominal value so redeemed goes to the capital redemption reserve: ₹40 lakh less ₹15 lakh funded by the fresh issue = ₹25 lakh. In practice: this keeps creditors\' cushion intact.', 'c4', T4, 'moderate', check=25),
        Q('m10', 'An instrument of transfer must be delivered to the company within:', ['60 days of its execution', '30 days of execution', '6 months of execution', 'One year of execution'], 0,
          'Section 56 requires the stamped and executed instrument to be delivered with the certificate within 60 days of execution. A late or lost instrument may still be accepted on indemnity terms set by the Board. In practice: lodge transfers promptly.', 'c5', T5, 'core', check=60),
        Q('m11', 'If no notice of refusal is sent, the transferee may appeal to the Tribunal within:', ['60 days of delivering the instrument', '30 days of delivering the instrument', '90 days of execution', 'One year of execution'], 0,
          'Section 58 gives 30 days from receiving a notice of refusal, and where no notice has been sent, 60 days from the date the instrument of transfer or intimation of transmission was delivered. In practice: keep proof of delivery.', 'c5', T5, 'core', check=60),
        Q('m12', 'A rights offer under section 62 must remain open for:', ['Not less than 15 days and not more than 30 days', 'Exactly 7 days', 'At least 45 days', 'Up to 60 days'], 0,
          'The offer to existing equity holders states the number of shares offered and a period of at least 15 and at most 30 days, after which it is deemed declined. Renunciation is allowed unless the articles say otherwise. In practice: shorter periods need specific rules.', 'c6', T6),
        Q('m13', 'Bonus shares cannot be issued out of:', ['Revaluation reserve', 'Free reserves', 'Securities premium account', 'Capital redemption reserve'], 0,
          'Section 63 allows bonus shares from free reserves, securities premium and capital redemption reserve, but not from reserves created by revaluing assets. Bonus shares also cannot replace dividends. In practice: check reserve composition first.', 'c6', T6),
        Q('m14', 'A company with paid-up capital ₹30 crore and free reserves ₹50 crore can buy back at most:', ['₹20 crore', '₹8 crore', '₹7.5 crore', '₹80 crore'], 0,
          'Section 68 limits a buy-back to 25% of paid-up capital plus free reserves: 25% of ₹80 crore = ₹20 crore, which also needs a special resolution because it exceeds the 10% Board limit of ₹8 crore. In practice: test the debt ratio too.', 'c7', T7, 'hard', check=20),
        Q('m15', 'After a buy-back, a company cannot issue the same kind of shares for:', ['Six months, except bonus issues and existing obligations', 'One year, with no exceptions', 'Three months', 'Two years'], 0,
          'Section 68(8) bars a further issue of the same kind of securities for six months after completing a buy-back, but bonus issues and existing obligations such as conversion of warrants, stock options or sweat equity are allowed. In practice: time capital raising carefully.', 'c7', T7),
        Q('m16', 'A debenture trustee must be appointed before offering debentures to the public or to more than:', ['500 persons', '200 persons', '50 persons', '1,000 persons'], 0,
          'Section 71 requires one or more debenture trustees before issuing a prospectus or offer of debentures to the public or to members exceeding 500. The trust deed follows within three months of the issue closing. In practice: the trustee protects holders.', 'c8', T8, 'core', check=500),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', '25% limit computed', 2, 'computation', '25%', nums=[lim]),
           S('s2', 'Special resolution beyond 10%', 1, 'concept', 'special resolution'),
           S('s3', 'Debt test', 1, 'computation', 'twice|2 ×', nums=[post]),
           S('s4', 'Capital redemption reserve', 1, 'computation', 'redemption reserve|crr', nums=[crr])],
          ['Show each limit separately.'], ['Using paid-up capital alone as the base.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, 'Pragati Ltd. made a rights issue. Rakesh renounced his rights in favour of his sister. The articles are silent. Later the company wants to issue bonus shares out of its revaluation reserve and announce them in lieu of the year\'s dividend. Advise.',
          [legal('Sections 62(1)(a) and 63',
                 'Rights renounced in favour of a sister; articles silent; bonus proposed from revaluation reserve and in place of dividend.',
                 'A rights offer includes the right to renounce in favour of any other person unless the articles provide otherwise. Bonus shares may be issued only from free reserves, securities premium or capital redemption reserve, not from revaluation reserves, and cannot be issued in lieu of dividend.',
                 'Rakesh\'s renunciation is valid. The proposed bonus issue is not permitted on either ground.')],
          [S('s1', 'Right to renounce', 1.5, 'concept', 'renounce|renunciation'),
           S('s2', 'Revaluation reserve barred', 1, 'application', 'revaluation'),
           S('s3', 'Not in lieu of dividend', 1, 'application', 'lieu|instead|dividend'),
           S('s4', 'Conclusion', 0.5, 'conclusion', 'valid|not permitted|cannot')],
          ['Answer each issue separately.'], ['Assuming renunciation needs articles\' permission.'], ['Provision → facts → analysis → conclusion.']),
        W('q3', 5, 'State the conditions for issue of bonus shares under section 63.', [p('Bonus shares may be issued only out of free reserves, the securities premium account or the capital redemption reserve account, with revaluation reserves excluded.'),
                                                                                      ul(['The articles authorise it.', 'The Board recommends it and the general meeting approves it.', 'Interest and principal on fixed deposits and debt securities are paid up to date.', 'Statutory dues of employees such as PF, gratuity and bonus are fully paid.', 'Partly paid shares are made fully paid before the issue.', 'Bonus shares cannot replace a dividend.', 'Once announced by the Board, the decision cannot be withdrawn.'])],
          [S('s1', 'Permitted sources', 1.5, 'concept', 'free reserves', 'premium'),
           S('s2', 'Revaluation excluded', 1, 'concept', 'excluded'),
           S('s3', 'Approval', 1, 'concept', 'general meeting|articles'),
           S('s4', 'No defaults / partly paid / lieu', 1.5, 'concept', 'up to date|fully paid', 'partly paid')],
          ['List conditions crisply.'], ['Forgetting the partly paid shares rule.'], ['Numbered list.']),
    ]

    viva = [
        V('v1', 'What is the difference between transfer and transmission of shares?',
          'Transfer is a voluntary act of the holder, made by an instrument of transfer executed by both parties; transmission happens by operation of law on death or insolvency and needs only an intimation with proof.',
          [P('p1', 'Transfer voluntary', 5, 'voluntary'), P('p2', 'Transmission by law', 5, 'operation of law|death|insolv')], 'c5'),
        V('v2', 'From which sources may a company buy back its shares?',
          'Out of free reserves, the securities premium account, or the proceeds of an issue of shares or securities of a different kind from those being bought back.',
          [P('p1', 'Free reserves and premium', 6, 'free reserve', 'premium'), P('p2', 'Proceeds of different issue', 4, 'proceeds|different')], 'c7'),
        V('v3', 'Why can a company not issue irredeemable preference shares?',
          'Section 55 requires every preference share to be redeemable within a fixed period, normally 20 years, so that preference capital has a definite exit and is not locked in permanently.',
          [P('p1', 'Must be redeemable', 5, 'redeem'), P('p2', '20 years', 5, '20|twenty')], 'c4'),
        V('v4', 'Do debenture holders have voting rights?',
          'Debentures carry no voting rights; debenture holders are creditors, protected through a debenture trustee, trust deed and redemption reserve.',
          [P('p1', 'Creditors without vote', 6, 'creditor|lender'), P('p2', 'Trustee protection', 4, 'trustee')], 'c8'),
        V('v5', 'What is sweat equity?',
          'Equity shares given to directors or staff below face value or against a non-cash return, in exchange for providing know-how or making available intellectual property rights or value additions.',
          [P('p1', 'Directors or employees', 4, 'director|employee'), P('p2', 'Discount or non-cash for know-how', 6, 'know-how|discount|value addition')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Vikram Textiles Ltd.', 'difficulty': 'moderate',
              'case': 'Vikram Textiles Ltd. (unlisted public company) has paid-up equity capital of ₹10 crore, free reserves ₹14 crore and a revaluation reserve of ₹6 crore. It has an unpaid bank term loan instalment overdue for 4 months. The Board wants a buy-back of ₹2 crore, followed by bonus shares from the revaluation reserve, and also wishes to cut the dividend rate on its preference shares.',
              'mcqs': [
                  M('k1a', 'Can the company proceed with the buy-back now?', ['No, because of the default in repaying the term loan', 'Yes, as it is within 10%', 'Yes, with a special resolution', 'Only with SEBI approval'], 0,
                    'Section 70 bars a buy-back while a company is in default in repaying a term loan, deposits, debentures or dividends. The default must be remedied and three years must pass from then. In practice: clear defaults before planning a buy-back.', 'core', topic=T7),
                  M('k1b', 'The maximum buy-back the Board alone could approve, once eligible:', ['₹2.4 crore', '₹6 crore', '₹3 crore', '₹1 crore'], 0,
                    'The Board can approve a buy-back of up to 10% of paid-up equity capital and free reserves: 10% of ₹24 crore = ₹2.4 crore. The revaluation reserve is not a free reserve. In practice: anything above needs a special resolution.', 'moderate', check=2.4, topic=T7),
                  M('k1c', 'The bonus issue from the revaluation reserve is:', ['Not permitted', 'Permitted with a special resolution', 'Permitted if fully paid', 'Permitted for unlisted companies'], 0,
                    'Section 63 permits bonus shares only from free reserves, securities premium or capital redemption reserve; reserves created by revaluation of assets cannot be capitalised. In practice: the company may use free reserves instead.', 'core', topic=T6),
                  M('k1d', 'To cut the preference dividend rate, the company needs:', ['Written consent of three-fourths of the preference shareholders or a special resolution at their class meeting', 'Only a Board resolution', 'An ordinary resolution of equity holders', 'Tribunal approval in every case'], 0,
                    'Changing class rights requires consent in writing of three-fourths of the issued shares of the class or a special resolution at a separate meeting of that class, as section 48 provides. Dissenters with 10% can approach the Tribunal. In practice: hold a class meeting.', 'moderate', topic=T2),
              ]}]

    return unit(UID, 'p2', 'int-p2-ch04', 1, 'Share Capital and Debentures',
                ['Explain kinds of share capital, DVRs, voting rights, certificates and variation of class rights.',
                 'Apply provisions on calls, securities premium, discount, sweat equity and preference shares.',
                 'Apply rules on transfer, transmission, refusal and rectification.',
                 'Explain alteration, further issue, bonus shares, reduction, financial assistance and buy-back.',
                 'Explain issue of debentures and nomination.'],
                {'difficulty': 'core', 'minutes': {'learn': 60, 'practice': 40}, 'prereq': ['int-p2-ch03-u01'],
                 'exam_tip': 'Numbers decide marks here: 74%, 2 years, 2 months / 1 month / 6 months, 10%, 21 days, 20/30 years, 60 days, 30/60 days, 15–30 days, 25%, 2:1, 6 months, 500.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Two kinds of capital; DVRs ≤ 74% of voting power.', 'Preference holders vote on all resolutions after 2 years\' unpaid dividend.',
                             'Certificates: 2 months (allotment), 1 month (transfer), 6 months (debentures).', 'Class rights: 3/4 consent; 10% dissenters → Tribunal in 21 days.',
                             'Premium uses limited; discount issues void except sweat equity and debt conversion.', 'Preference shares redeemable within 20 (infra 30) years; CRR on redemption out of profits.',
                             'Transfer deed within 60 days; refusal notice 30 days; appeal 30/60 days.', 'Rights offer 15–30 days; bonus only from free reserves, premium, CRR.',
                             'Reduction: special resolution + Tribunal. Buy-back: 25%, 2:1 debt, 1 year, 6-month bar.', 'Debentures: no vote; trustee if > 500; SH-12 within 3 months.'],
                 'remember': ['Revaluation reserve is not a free reserve.', 'Advance calls carry no vote.'],
                 'traps': ['Board limit is 10%, not 25%.', 'Bonus shares never in lieu of dividend.']},
                [('DVR voting cap', '74%'), ('Certificates on allotment', '2 months'), ('Class rights', '3/4; 10% → Tribunal in 21 days'), ('Preference tenure', '20 yrs (infra 30)'),
                 ('Buy-back', '25% · Board 10% · debt 2:1'), ('Rights offer', '15–30 days')],
                viva, cases)
