"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 12 — Buy-back of Securities.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch12-u01'
T1 = 'Meaning of buy-back and its sources'
T2 = 'Legal conditions for buy-back (s. 68–70)'
T3 = 'Three tests for the maximum buy-back'
T4 = 'Accounting entries and capital redemption reserve'
T5 = 'Presentation after buy-back'


def build():
    ck = Checks()
    res = ck.add('(5000000+7000000)*25/100/40', 'Resource test: shares (25% of capital + free reserves ÷ ₹40)')
    sot = ck.add('500000*25/100', 'Shares outstanding test: shares')
    x = ck.add('(12000000-7500000)/5', 'Debt-equity test: amount to CRR, x, from (120 − x) − 75 = 4x (₹)')
    y = ck.add('900000*4', 'Debt-equity test: maximum buy-back, y = 4x (₹)')
    de = ck.add('3600000/40', 'Debt-equity test: shares')
    mx = ck.add('min(75000, 125000, 90000)', 'Maximum shares (least of the three)')
    i1 = {'id': 'i1', 'title': 'How many shares can be bought back?', 'difficulty': 'hard', 'minutes': 12,
          'q': 'Swastik Ltd. (unlisted) has equity capital ₹50,00,000 (₹10 shares), free reserves ₹70,00,000 (general reserve ₹40 lakh, securities premium ₹15 lakh, profit and loss ₹15 lakh) and loan funds ₹1,50,00,000. It offers to buy back at ₹40 per share. Find the maximum number of shares by the three tests.',
          'solution': [table(['Test', 'Working', 'Shares'], [
              ['Resource test', '25% × (50 + 70) lakh = ₹30 lakh ÷ ₹40', R(res)],
              ['Shares outstanding test', '25% × 5,00,000 shares', R(sot)],
              ['Debt-equity test', f'Minimum equity = 150 ÷ 2 = 75 lakh; (120 − x) − 75 = y and y = 4x → x = {inr(x)}, y = {inr(y)}', R(de)],
              ['Maximum (least)', '', R(mx)]], title='Maximum buy-back'),
              note('x is the nominal value transferred to capital redemption reserve; y is the amount paid. Since price is 4 times face value, y = 4x.')],
          'checks': list(ck)}

    ck2 = Checks()
    paid = ck2.add('75000*40', 'Amount paid to shareholders (₹)')
    nom = ck2.add('75000*10', 'Nominal value cancelled (₹)')
    prem = ck2.add('3000000-750000', 'Premium on buy-back (₹)')
    gr = ck2.add('2250000-1500000', 'Premium charged to general reserve after securities premium (₹)')
    crr = ck2.add('750000', 'Transfer to capital redemption reserve (₹)')
    i2 = {'id': 'i2', 'title': 'Journal entries for the buy-back', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Swastik Ltd. buys back 75,000 shares of ₹10 at ₹40 out of free reserves, paying in cash. Securities premium of ₹15,00,000 is used first for the premium. Show the main entries.',
          'solution': [table(['Entry', 'Debit', 'Credit', '₹'], [
              ['Amount due on buy-back', 'Equity share capital (nominal) + Premium on buy-back', 'Equity shareholders', inr(paid)],
              ['', 'of which nominal value', '', inr(nom)],
              ['', 'of which premium', '', inr(prem)],
              ['Payment', 'Equity shareholders', 'Bank', inr(paid)],
              ['Write off premium', 'Securities premium ₹15,00,000; General reserve', 'Premium on buy-back', inr(prem)],
              ['', 'General reserve portion', '', inr(gr)],
              ['Capital redemption reserve', 'General reserve (or P&L)', 'Capital redemption reserve', inr(crr)]], title='Buy-back entries')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Buy-back means a company purchasing its own shares or other specified securities from its holders; the shares bought back are extinguished.',
            'Reasons include returning surplus cash, improving earnings per share and return on equity, supporting share price, and changing the capital structure.',
            'Section 68(1) lists three funding sources: free reserves, the securities premium account, and money raised by issuing shares or other specified securities. Money raised from a past issue of the very same kind of security cannot be used.'],
          'A buy-back returns capital to shareholders and shrinks the share base.',
          'A cash-rich company buying back 10% of its shares at above market price.'),
        C('c2', T2, [
            'Conditions: the articles authorise it; a special resolution is passed (a Board resolution suffices for up to 10% of paid-up equity capital and free reserves); the amount does not exceed 25% of paid-up capital and free reserves; buy-back of equity in a year does not exceed 25% of paid-up equity capital; debt after buy-back does not exceed twice paid-up capital and free reserves; shares are fully paid; it is completed within one year of the resolution; and there is a gap of at least one year from closure of the previous buy-back.',
            'After buy-back the company cannot issue the same kind of shares for six months (except bonus issues and existing obligations); the shares are extinguished within seven days of completion.',
            'Section 70 bars buy-back through subsidiaries or investment companies, or where there is a default in repaying deposits, debentures, preference shares, term loans or dividends (unless remedied and three years have passed).'],
          'Limits on size, debt, approvals and timing keep buy-backs from hurting creditors.',
          'A company that defaulted on a term loan two years ago and has since repaid it must still wait a full three years.'),
        C('c3', T3, [
            'ICAI computes the maximum number of shares as the least of three tests.',
            'Resource test: 25% of paid-up capital plus free reserves ÷ buy-back price.',
            'Shares outstanding test: 25% of the number of equity shares in issue.',
            'Debt-equity test: equity after buy-back must be at least half the debt. Since an amount equal to the nominal value bought back (x) goes to capital redemption reserve, ICAI solves: (present equity − x) − minimum equity = y, with y = x × (price ÷ face value). Free reserves exclude revaluation reserve and statutory reserves.'],
          'The smallest of the three answers wins.',
          'If debt is already more than twice equity, the debt-equity test allows no buy-back at all.'),
        C('c4', T4, [
            'On buy-back, equity share capital is debited with the nominal value and a "premium on buy-back" account with the excess; the shareholders\' account is credited and then paid.',
            'The premium is written off against securities premium first and then free reserves.',
            'Section 69: where shares are bought back out of free reserves or securities premium, a sum equal to their nominal value is transferred to the capital redemption reserve; this reserve may be used only to issue fully paid bonus shares.',
            'If the buy-back is financed by a fresh issue of a different kind of shares, no transfer to CRR is needed to the extent of those proceeds. Assets may be sold (for example investments) to fund the buy-back, with any profit or loss recognised.'],
          'Capital that leaves the company is replaced by an untouchable reserve.',
          'Buying back ₹5 lakh of face value out of general reserve requires ₹5 lakh in CRR.'),
        C('c5', T5, [
            'The balance sheet after buy-back shows reduced share capital, reduced reserves (premium written off and CRR transfer), the new capital redemption reserve under reserves and surplus, and reduced cash or investments.',
            'The notes give details of shares bought back in the last five years where required by Schedule III.'],
          'The balance sheet shows the smaller company and the reserve that protects its capital.',
          'Share capital falls from ₹50 lakh to ₹42.5 lakh after buying back 75,000 shares of ₹10.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Buy-back feasibility note', 'role': 'Accounts executive',
             'situation': 'The CFO wants to know how many shares can be bought back at a proposed price and what entries will follow.',
             'steps': ['Identify free reserves, excluding revaluation and statutory reserves.', 'Run the three tests.', 'Check approvals, timing and default restrictions.', 'Draft entries including CRR.'],
             'takeaway': 'Run all three tests and pick the lowest.'}]

    mcqs = [
        Q('m1', 'Buy-back of shares cannot be made out of:', ['Money from a past issue of that very class of shares', 'Free reserves', 'Securities premium', 'Proceeds of a different kind of shares'], 0,
          'Section 68 allows buy-back from free reserves, securities premium or proceeds of shares or securities, but never from money raised by a past issue of that same class. In practice: check the funding source.', 'c1', T1),
        Q('m2', 'The amount of buy-back cannot exceed what share of paid-up capital and free reserves?', ['25%', '10%', '50%', '20%'], 0,
          'The total buy-back must not exceed 25% of paid-up capital and free reserves; up to 10% may be approved by the Board, beyond that a special resolution is needed. In practice: this is the resource test.', 'c2', T2, 'core', check=25),
        Q('m3', 'After buy-back, the debt of the company should not exceed:', ['Twice its paid-up capital and free reserves', 'Its paid-up capital', 'Three times its free reserves', 'Its total assets'], 0,
          'Section 68 requires a debt–equity ratio of not more than 2:1 after buy-back, unless a higher ratio is prescribed for a class of companies. In practice: compute with the CRR adjustment.', 'c2', T2),
        Q('m4', 'Paid-up equity ₹80 lakh (₹10 shares), free reserves ₹40 lakh, price ₹30. Shares by the resource test:', ['1,00,000', '2,00,000', '4,00,000', '1,33,333'], 0,
          '25% of (₹80 lakh + ₹40 lakh) = ₹30 lakh; at ₹30 per share this allows 1,00,000 shares. The other two tests may give a lower answer. In practice: compare all three.', 'c3', T3, 'moderate', check=100000),
        Q('m5', 'Under the shares outstanding test, a company with 8,00,000 equity shares can buy back at most:', ['2,00,000 shares', '80,000 shares', '4,00,000 shares', '1,60,000 shares'], 0,
          'Buy-back of equity shares in a financial year cannot exceed 25% of paid-up equity capital, i.e. 25% of 8,00,000 = 2,00,000 shares. In practice: count only equity shares.', 'c3', T3, 'core', check=200000),
        Q('m6', 'When shares are bought back out of free reserves, the company must transfer to capital redemption reserve:', ['The nominal value of shares bought back', 'The premium paid', 'The total amount paid', 'Nothing'], 0,
          'Section 69 requires a sum equal to the nominal value of the shares bought back out of free reserves or securities premium to be transferred to CRR. In practice: premium is written off separately.', 'c4', T4),
        Q('m7', 'Capital redemption reserve may be used to:', ['Issue fully paid bonus shares', 'Pay dividends', 'Write off losses', 'Buy back shares again'], 0,
          'CRR is treated like paid-up capital; the only permitted use is issuing fully paid bonus shares to members. In practice: it is not a free reserve.', 'c4', T4),
        Q('m8', 'Which is NOT a free reserve for buy-back calculations?', ['Revaluation reserve', 'General reserve', 'Securities premium', 'Surplus in profit and loss'], 0,
          'Revaluation reserves and statutory reserves are not free reserves; ICAI includes general reserve, securities premium and profit and loss surplus for buy-back limits. In practice: exclude unrealised gains.', 'c3', T3),
        Q('m9', 'The minimum gap between two buy-back offers is:', ['One year from closure of the previous buy-back', 'Six months', 'Three years', 'No gap'], 0,
          'A company cannot make a fresh buy-back offer within one year from the date of closure of the previous offer. In practice: plan buy-backs annually at most.', 'c2', T2),
        Q('m10', 'Shares bought back must be extinguished and physically destroyed within:', ['Seven days after the buy-back is completed', 'Thirty days', 'Six months', 'One year'], 0,
          'The rules require bought-back securities to be extinguished and physically destroyed within seven days of completing the buy-back. In practice: update the register promptly.', 'c2', T2),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Resource and outstanding tests', 2, 'computation', 'resource', nums=[res, sot]),
           S('s2', 'Debt-equity simultaneous equation', 3, 'computation', 'debt', nums=[x, y, de]),
           S('s3', 'Least of three', 1, 'computation', 'least', nums=[mx])],
          ['Show the equation for the debt test.'], ['Ignoring the CRR adjustment.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Nominal and premium split', 2, 'computation', 'premium', nums=[nom, prem]),
           S('s2', 'Premium written off', 1.5, 'computation', 'securities premium', nums=[gr]),
           S('s3', 'CRR transfer', 1.5, 'computation', 'redemption', nums=[crr])],
          ['Use securities premium first.'], ['Forgetting the CRR transfer.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'From which sources can a company buy back shares?', 'Free reserves, the securities premium account, or money raised by a fresh issue of a different class of shares or securities.',
          [P('p1', 'Free reserves and premium', 6, 'free reserve', 'premium'), P('p2', 'Proceeds of other issue', 4, 'raised|proceeds')], 'c1'),
        V('v2', 'Name the three ICAI tests for maximum buy-back.', 'The resource test, the shares outstanding test and the debt-equity ratio test; the lowest result is the maximum.',
          [P('p1', 'Resource and outstanding', 5, 'resource', 'outstanding'), P('p2', 'Debt-equity', 5, 'debt')], 'c3'),
        V('v3', 'Why is a capital redemption reserve created?', 'To replace the share capital cancelled out of free reserves or premium, so that the capital base available to creditors is not reduced.',
          [P('p1', 'Replace capital', 6, 'capital'), P('p2', 'Protect creditors', 4, 'creditor')], 'c4'),
        V('v4', 'When is a special resolution needed?', 'When the buy-back exceeds 10% of paid-up equity capital and free reserves; up to 10% a Board resolution is enough.',
          [P('p1', 'Above 10%', 6, '10'), P('p2', 'Board resolution', 4, 'board')], 'c2'),
        V('v5', 'What restriction applies after buy-back?', 'The company cannot issue the same kind of shares for six months, except bonus issues and existing obligations such as conversions and stock options.',
          [P('p1', 'Six months', 6, 'six months|6 months'), P('p2', 'Exceptions', 4, 'bonus')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Unnat Ltd.', 'difficulty': 'moderate',
              'case': 'Unnat Ltd. has equity capital ₹1 crore (₹10 shares), general reserve ₹60 lakh, securities premium ₹20 lakh, revaluation reserve ₹30 lakh and loans ₹4 crore. It proposes to buy back at ₹25 per share.',
              'mcqs': [
                  M('k1a', 'Free reserves for buy-back purposes:', ['₹80 lakh', '₹110 lakh', '₹60 lakh', '₹50 lakh'], 0,
                    'General reserve ₹60 lakh plus securities premium ₹20 lakh = ₹80 lakh; revaluation reserve is excluded. In practice: list each reserve.', 'core', check=80, topic=T3),
                  M('k1b', 'Under the debt-equity test, the buy-back possible is:', ['Nil, as debt already exceeds twice equity', '₹45 lakh', '₹20 lakh', '₹90 lakh'], 0,
                    'Equity is ₹1.8 crore and the minimum required is half of ₹4 crore = ₹2 crore; equity is already below that, so no buy-back is possible. In practice: reduce debt first.', 'hard', topic=T3),
                  M('k1c', 'If the test had allowed a buy-back out of general reserve, the CRR transfer would equal:', ['The nominal value of shares bought back', 'The premium paid', 'The total price', 'Nothing'], 0,
                    'Section 69 requires a transfer to CRR equal to the nominal value of shares bought back out of free reserves or premium. In practice: pass it along with the buy-back entries.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch12', 1, 'Buyback of Securities',
                ['Explain buy-back and its permitted sources.',
                 'Apply the legal conditions for buy-back.',
                 'Compute the maximum buy-back using the three tests.',
                 'Pass accounting entries including the capital redemption reserve.'],
                {'difficulty': 'hard', 'minutes': {'learn': 30, 'practice': 40}, 'prereq': ['int-p1-ch11-u02'],
                 'exam_tip': 'Always run all three tests; set up the simultaneous equation for the debt-equity test with x = CRR and y = buy-back amount.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Sources: free reserves, premium, proceeds of other issues.', 'Limits: 25% amount, 25% equity shares, debt ≤ 2× equity.',
                             'Board up to 10%, otherwise special resolution; complete in 1 year; 1-year gap.', 'Maximum = least of three tests.',
                             'Premium written off against premium then free reserves.', 'CRR = nominal value bought back from reserves.'],
                 'remember': ['Revaluation and statutory reserves are not free reserves.'],
                 'traps': ['Forgetting CRR in the debt-equity equation.']},
                [('Resource test', '25% of capital + free reserves'), ('Shares test', '25% of equity shares'), ('Debt test', 'Debt ≤ 2 × equity')],
                viva, cases)
