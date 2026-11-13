"""CA Intermediate · Paper 2 Corporate and Other Laws · Chapter 8 Declaration and Payment of Dividend (ss. 123–127).
Scope follows the ICAI study material; provisions are explained in original words; examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p2-ch08-u01'
T1 = 'Meaning and types of dividend'
T2 = 'Sources of dividend and conditions (s. 123)'
T3 = 'Interim dividend and payment mechanics'
T4 = 'Unpaid Dividend Account and IEPF (ss. 124–125)'
T5 = 'Right to dividend pending transfer and punishment (ss. 126–127)'


def build():
    ck = Checks()
    avail = ck.add('4200000-1500000-300000', 'Profit available for dividend after setting off past loss and arrear depreciation (₹)')
    i1 = {'id': 'i1', 'title': 'Can the company pay this dividend?', 'difficulty': 'core', 'minutes': 7,
          'q': 'Divya Ltd. earned ₹42,00,000 this year after current depreciation. It carries forward a loss of ₹15,00,000 from earlier years and had not provided depreciation of ₹3,00,000 in an earlier year. The Board wants to declare equity dividend of ₹25,00,000 out of current profit. Advise.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Current year profit after depreciation', '', inr(4200000)],
              ['Less: carried-over loss', '', '(15,00,000)'],
              ['Less: depreciation not provided earlier', '', '(3,00,000)'],
              ['Available for dividend', '', inr(avail)]], title='Section 123(1)'),
              p('Since ₹24,00,000 is available, a dividend of ₹25,00,000 out of current profits is not permissible; the company may pay up to ₹24,00,000 (or use accumulated profits under the rules if conditions are met).')],
          'checks': list(ck)}

    ck2 = Checks()
    intr = ck2.add('500000*12/100*3/12', 'Interest for 3 months\' delay in transfer to UDA (₹)')
    i2 = {'id': 'i2', 'title': 'Late transfer to the Unpaid Dividend Account', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Kamal Ltd. declared a dividend on 10 August. ₹5,00,000 remained unpaid when the 30-day payment period ended, but the company transferred it to the Unpaid Dividend Account three months after the due date. What are the consequences?',
          'solution': [legal('Section 124',
                             'Unpaid dividend not transferred within the time allowed; delay of three months.',
                             'Unpaid or unclaimed dividend must be transferred to a special Unpaid Dividend Account in a scheduled bank within seven days from the end of the 30-day period. On default, the company pays interest at 12% per annum on the amount not transferred, from the date of default, and the interest goes to the members in proportion to the amount remaining unpaid.',
                             f'Kamal Ltd. must pay interest of {inr(intr)} (₹5,00,000 × 12% × 3/12) for the benefit of the members concerned, besides any penalty.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Section 2(35): dividend includes interim dividend. It is the portion of profits distributed to shareholders.',
            'A final dividend is recommended by the Board and declared by members at the AGM; once declared it becomes a debt of the company. An interim dividend is declared by the Board between two AGMs.',
            'Dividend is paid only in cash (including cheque, warrant or electronic mode) — but capitalising profits by issuing fully paid bonus shares or paying up unpaid amounts on shares is allowed.'],
          'Dividend is a share of profit paid in money.',
          'Bonus shares are not dividend; they capitalise profits.'),
        C('c2', T2, [
            'Section 123(1): dividend may be declared or paid only out of (a) profits of the current year after providing depreciation under Schedule II; (b) undistributed profits of earlier years after depreciation; (c) both; or (d) money provided by the Central or State Government for dividend under a guarantee.',
            'A company may transfer such part of profits to reserves as it thinks fit before declaring dividend.',
            'Before declaring dividend out of current profits, losses and arrears of depreciation of earlier years carried forward must be set off against the current profit (or the lower of the two).',
            'Unrealised gains, notional gains and revaluation of assets, and changes in carrying amounts of assets or liabilities measured at fair value, are excluded from profits for dividend. Free reserves cannot be used except as the rules on inadequate profit allow (average rate, one-tenth cap, losses set off first, and remaining reserves condition).',
            'No dividend can be declared by a company that has failed to comply with the deposit provisions of sections 73 and 74, as long as the failure continues.'],
          'Dividends come only from real profits, after old losses and depreciation are covered.',
          'Revaluation surplus on land cannot fund a dividend.'),
        C('c3', T3, [
            'The Board may declare interim dividend during a financial year or before the AGM, out of surplus in profit and loss and profits of the year up to the quarter preceding declaration.',
            'If the company has incurred a loss in the current year up to the quarter-end just before the declaration, interim dividend cannot exceed the average rate of the three preceding years.',
            'The dividend money (interim included) goes into a separate scheduled-bank account no later than five days after declaration, and paid only to the registered shareholder, to his order or his banker.',
            'Dividend must be paid or warrants posted within thirty days of declaration.'],
          'Interim dividends are the Board\'s decision, but limited when the year looks weak.',
          'A Board declaring interim dividend in November after losses in Q1 and Q2 must cap the rate at the three-year average.'),
        C('c4', T4, [
            'Section 124: dividend declared but not paid or claimed within 30 days is transferred to an "Unpaid Dividend Account" in a scheduled bank within seven days after those 30 days.',
            'The company prepares a statement of the names, addresses and unpaid amounts and places it on its website (and any website approved by the government) within ninety days of the transfer.',
            'Default in transfer attracts interest at 12% per annum from the date of default, for the benefit of members.',
            'Amounts in the Unpaid Dividend Account unpaid or unclaimed for seven years are transferred, with interest, to the Investor Education and Protection Fund (IEPF). Shares on which dividend has not been paid or claimed for seven consecutive years are also transferred to the IEPF; claimants may later reclaim them from the Fund.',
            'Section 125: the IEPF is used to refund unclaimed amounts, promote investor education and awareness, and protect investors\' interests.'],
          'Unclaimed dividend moves first to a special account and after seven years to the government fund.',
          'A shareholder who forgot to claim dividends for eight years can still claim from the IEPF authority.'),
        C('c5', T5, [
            'Section 126: where a transfer of shares has been lodged but not registered, the dividend is transferred to the Unpaid Dividend Account (unless the registered holder authorises payment to the transferee), and rights or bonus shares are kept in abeyance.',
            'Section 127: if a declared dividend is not paid or warrants not posted within 30 days, every director knowingly party to the default faces imprisonment up to two years and a fine of at least ₹1,000 for each day of default, and the company pays simple interest at 18% per annum during the default.',
            'No offence arises where the dividend could not be paid because of operation of law, the shareholder\'s directions could not be complied with, there was a dispute about the right to receive it, it was lawfully adjusted against a sum due from the shareholder, or the failure was not due to the company\'s default.'],
          'Late dividend payment can mean jail for directors and interest for the company.',
          'A dividend withheld because of a court order freezing the shares is not a default.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Dividend compliance checklist', 'role': 'Secretarial associate',
             'situation': 'A company has declared a final dividend at its AGM.',
             'steps': ['Deposit the amount in a separate bank account within five days.', 'Pay within thirty days.', 'Move unpaid sums to the Unpaid Dividend Account within seven days after that.', 'Upload the unpaid list on the website within ninety days.'],
             'takeaway': 'Each step after declaration has its own deadline.'}]

    mcqs = [
        Q('m1', 'Which is NOT a permitted source of dividend?', ['Revaluation reserve', 'Current year profits after depreciation', 'Undistributed past profits after depreciation', 'Money provided by government under a guarantee'], 0,
          'Section 123 excludes unrealised gains and revaluation from profits available for dividend. The other three sources are expressly allowed. In practice: check the reserve composition.', 'c2', T2),
        Q('m2', 'Before declaring dividend out of current profits, a company must set off:', ['Carried-forward losses and arrears of depreciation', 'Future losses', 'Contingent liabilities', 'Dividend of the next year'], 0,
          'Losses and depreciation not provided in earlier years, carried forward, must be set off against current profits before dividend. In practice: use the lower of the two amounts.', 'c2', T2),
        Q('m3', 'Interim dividend is declared by:', ['The Board of Directors', 'Members at the AGM', 'The Registrar', 'Auditors'], 0,
          'The Board may declare interim dividend during the year or before the AGM; final dividend is declared by members on the Board\'s recommendation. In practice: record the Board resolution.', 'c3', T3),
        Q('m4', 'Dividend declared must be deposited in a separate bank account within:', ['5 days of declaration', '7 days', '30 days', '15 days'], 0,
          'Section 123(4) requires the dividend money to be placed in a separate scheduled-bank account no later than five days after declaration. Payment follows within thirty days. In practice: arrange funds beforehand.', 'c3', T3, 'core', check=5),
        Q('m5', 'Unpaid dividend must be transferred to the Unpaid Dividend Account within:', ['7 days after expiry of 30 days from declaration', '30 days of declaration', '90 days', 'One year'], 0,
          'Section 124 requires transfer of amounts unpaid or unclaimed within thirty days of declaration to the Unpaid Dividend Account within seven days after those thirty days. In practice: open the account in advance.', 'c4', T4),
        Q('m6', 'Interest payable for delay in transferring to the Unpaid Dividend Account is:', ['12% per annum', '18% per annum', '9% per annum', '15% per annum'], 0,
          'Default in transfer to the Unpaid Dividend Account attracts interest at 12% per annum from the date of default, for the benefit of members. Delay in paying dividend itself attracts 18%. In practice: avoid both.', 'c4', T4),
        Q('m7', 'Amounts in the Unpaid Dividend Account unclaimed for seven years go to:', ['The Investor Education and Protection Fund', 'General reserve', 'Profit and loss', 'The Registrar'], 0,
          'After seven years, unpaid or unclaimed amounts, with interest, are transferred to the IEPF, along with shares on which dividends were unclaimed for seven consecutive years. In practice: send reminders before transfer.', 'c4', T4),
        Q('m8', 'If dividend is not paid within 30 days, the company pays simple interest at:', ['18% per annum', '12% per annum', '10% per annum', '24% per annum'], 0,
          'Section 127 makes the company liable to pay simple interest at 18% per annum for the period of default, besides punishment of directors knowingly party to it. In practice: settle quickly.', 'c5', T5),
        Q('m9', 'A director knowingly party to failure to pay declared dividend is punishable with:', ['Imprisonment up to two years and fine of at least ₹1,000 per day', 'Fine only', 'Disqualification only', 'Imprisonment up to six months'], 0,
          'Section 127 prescribes imprisonment up to two years and a minimum fine of ₹1,000 for every day the default continues. In practice: directors must monitor payment.', 'c5', T5),
        Q('m10', 'No offence under section 127 arises when dividend is not paid because:', ['There is a dispute about the right to receive it', 'The company has no cash', 'The director is busy', 'Bank charges are high'], 0,
          'Exceptions include operation of law, shareholder\'s directions that cannot be complied with, disputes about entitlement, lawful adjustment against dues, and failure not due to the company\'s default. Lack of funds is not an exception. In practice: document the reason.', 'c5', T5),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Set off loss and arrear depreciation', 2, 'computation', 'loss', nums=[avail]),
           S('s2', 'Conclusion on permissibility', 2, 'conclusion', 'not permissible|cannot|up to')],
          ['Set off before declaring.'], ['Ignoring earlier losses.'], ['Table + advice.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Seven-day rule', 1.5, 'concept', 'seven|7'),
           S('s2', '12% interest', 1.5, 'application', '12%'),
           S('s3', 'Amount', 1, 'computation', 'interest', nums=[intr])],
          ['State the rule, then compute.'], ['Applying 18% here.'], ['Provision → facts → analysis → conclusion.'], checks=list(ck2)),
    ]

    viva = [
        V('v1', 'From what sources can dividend be paid?', 'Current year profits after depreciation, undistributed profits of earlier years after depreciation, both, or money provided by government under a guarantee.',
          [P('p1', 'Profits after depreciation', 6, 'depreciation'), P('p2', 'Government guarantee', 4, 'government|guarantee')], 'c2'),
        V('v2', 'Within how many days must dividend be paid?', 'Within thirty days from the date of declaration.',
          [P('p1', 'Thirty days', 6, 'thirty|30'), P('p2', 'From declaration', 4, 'declar')], 'c3'),
        V('v3', 'What is the Unpaid Dividend Account?', 'A special account in a scheduled bank to which dividend unpaid or unclaimed within 30 days is transferred within the next seven days.',
          [P('p1', 'Special bank account', 5, 'account'), P('p2', '30 and 7 days', 5, '30|seven|7')], 'c4'),
        V('v4', 'What happens after seven years in the Unpaid Dividend Account?', 'The amount with interest, and shares with dividends unclaimed for seven consecutive years, are transferred to the Investor Education and Protection Fund.',
          [P('p1', 'IEPF', 6, 'iepf|investor education'), P('p2', 'Shares too', 4, 'shares')], 'c4'),
        V('v5', 'What is the company\'s liability for late payment of dividend?', 'Simple interest at 18% per annum for the period of default, besides punishment of directors.',
          [P('p1', '18%', 6, '18'), P('p2', 'Simple interest', 4, 'interest')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Shubham Ltd.', 'difficulty': 'moderate',
              'case': 'Shubham Ltd. declared a final dividend on 15 September 2026, deposited the amount in a separate bank account on 25 September and posted warrants on 20 October. It also has a pending default in repaying public deposits.',
              'mcqs': [
                  M('k1a', 'The deposit of dividend money on 25 September was:', ['Late, as it was due within five days', 'In time', 'Not required', 'Early'], 0,
                    'Section 123(4) requires deposit within five days of declaration, i.e. by 20 September; 25 September is late. In practice: arrange funds before the AGM.', 'core', topic=T3),
                  M('k1b', 'Posting warrants on 20 October was:', ['Late, as the 30-day period ended on 15 October', 'Within time', 'Premature', 'Irrelevant'], 0,
                    'Thirty days from declaration on 15 September ended on 15 October, so posting on 20 October breaches the time limit and attracts section 127, including 18% interest. In practice: plan dispatch early.', 'moderate', topic=T5),
                  M('k1c', 'Given the deposit default, could Shubham Ltd. declare dividend at all?', ['No, while the failure under sections 73–74 continues', 'Yes, with special resolution', 'Yes, interim only', 'Yes, if profits exist'], 0,
                    'A company that has failed to comply with sections 73 and 74 on deposits cannot declare any dividend on equity shares as long as the failure continues. In practice: clear deposit defaults first.', 'moderate', topic=T2),
              ]}]

    return unit(UID, 'p2', 'int-p2-ch08', 1, 'Declaration and Payment of Dividend',
                ['Explain the meaning and types of dividend.',
                 'Apply the sources and conditions for declaring dividend.',
                 'Apply interim dividend and payment rules.',
                 'Explain the Unpaid Dividend Account, IEPF and penalties for default.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 25}, 'prereq': ['int-p2-ch07-u01'],
                 'exam_tip': 'Keep the time chain clear: 5 days (deposit) → 30 days (payment) → 7 days (UDA) → 90 days (website) → 7 years (IEPF); 12% vs 18% interest.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Dividend includes interim; payable in cash only.', 'Sources: profits after depreciation (current/past), government guarantee.',
                             'Set off past losses and arrear depreciation first; no unrealised gains.', 'Interim by Board; capped at 3-year average after interim losses.',
                             'Deposit 5 days; pay 30 days; UDA 7 days; 12% interest on delay in UDA transfer.', 'IEPF after 7 years; 18% interest and director punishment for non-payment.'],
                 'remember': ['No dividend while deposit defaults continue.'],
                 'traps': ['12% (UDA delay) vs 18% (non-payment).']},
                [('Deposit', '5 days'), ('Payment', '30 days'), ('UDA', '7 days after 30'), ('IEPF', '7 years'), ('Interest', '12% UDA · 18% non-payment')],
                viva, cases)
