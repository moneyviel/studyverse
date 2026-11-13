"""CA Intermediate · Paper 2 Corporate and Other Laws · Chapter 5 Acceptance of Deposits by Companies (ss. 73–76A and Deposit Rules, 2014).
Scope follows the ICAI study material; provisions are explained in original words; examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p2-ch05-u01'
T1 = 'Meaning of deposit and amounts excluded'
T2 = 'Depositor, eligible company and exempt companies'
T3 = 'Deposits from members (s. 73) and exemptions for private companies'
T4 = 'Deposits from the public by eligible companies (s. 76)'
T5 = 'Limits, tenure, trustees and procedural rules'
T6 = 'Default, Tribunal remedy and punishment (ss. 73(4), 74, 76A)'


def build():
    # i1 — limits for an eligible company
    ck = Checks()
    base = ck.add('40+60+20', 'Paid-up capital + free reserves + securities premium (₹ crore)')
    mem = ck.add('120*10/100', 'Eligible company: from members — 10% (₹ crore)')
    pub = ck.add('120*25/100', 'Eligible company: from others — 25% (₹ crore)')
    st = ck.add('120*10/100', 'Short-term deposits below six months — 10% (₹ crore)')
    ne = ck.add('120*35/100', 'A non-eligible public company: members only — 35% (₹ crore)')
    i1 = {'id': 'i1', 'title': 'How much can Kaveri borrow?', 'difficulty': 'core', 'minutes': 7,
          'q': 'Kaveri Ltd., a public company with turnover of ₹640 crore, has paid-up capital ₹40 crore, free reserves ₹60 crore and securities premium ₹20 crore. (a) Is it an eligible company? (b) What are its limits for deposits from members and from others? (c) How much may be repayable in under six months? (d) What would the members\' limit be if it were not eligible?',
          'solution': [table(['Point', 'Working', 'Answer'], [
              ['(a) Eligibility', 'Turnover ₹640 crore ≥ ₹500 crore', 'Eligible, after a special resolution filed with the Registrar'],
              ['Base', '40 + 60 + 20', f'₹{R(base)} crore'],
              ['(b) From members', '10% of base', f'₹{R(mem)} crore'],
              ['(b) From others', '25% of base', f'₹{R(pub)} crore'],
              ['(c) Short-term', '10% of base, repayable after at least 3 months', f'₹{R(st)} crore'],
              ['(d) If not eligible', '35% of base, members only', f'₹{R(ne)} crore']], title='Deposit limits')],
          'checks': list(ck)}

    # i2 — premature repayment and penal interest
    ck2 = Checks()
    rate = ck2.add('8.25-1', 'Rate for the period run (18 months counted as 2 years) less 1%')
    intr = ck2.add('200000*7.25/100*18/12', 'Interest for the 18 months actually run')
    pen = ck2.add('500000*18/100*73/365', 'Penal interest at 18% for 73 overdue days')
    i2 = {'id': 'i2', 'title': 'Early exit and late repayment', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Bharat Pumps Ltd. offers deposit rates of 7.5% for 1 year, 8.25% for 2 years and 9% for 3 years. (a) Meena placed ₹2,00,000 for 3 years and asks for repayment after 18 months. What rate and interest apply? (b) Another depositor\'s ₹5,00,000 matured and was claimed but paid 73 days late. What extra interest is due?',
          'solution': [table(['Part', 'Working', 'Answer'], [
              ['(a) Period counted', '1 year 6 months: the 6-month part counts as a full year', '2 years'],
              ['(a) Rate', '2-year rate 8.25% less 1%', f'{R(rate)}%'],
              ['(a) Interest', '2,00,000 × 7.25% × 18/12', inr(intr)],
              ['(b) Penal interest', '5,00,000 × 18% × 73/365', inr(pen)]], title='Rules 15 and 17'),
              note('Had the part year been under six months it would have been ignored. The 1% cut does not apply where the company repays early to come within the legal limits.')],
          'checks': list(ck2)}

    excl = table(['Not a deposit (examples)', 'Condition'], [
        ['From Government, local or statutory authority; guaranteed by Government', '—'],
        ['Loans from banks, PFIs, insurance companies; from another company', '—'],
        ['Share application money', 'Allotted within 60 days or refunded within the next 15 days'],
        ['From a director (or, for a private company, a director\'s relative)', 'Written declaration that it is not borrowed money; disclosed in Board\'s report'],
        ['Secured bonds/debentures (first or pari passu charge on non-intangible assets); bonds compulsorily convertible within 10 years; listed unsecured NCDs', 'Secured amount ≤ market value of assets'],
        ['Employee\'s non-interest security deposit', 'Not more than annual salary'],
        ['Trade advances for goods or services', 'Adjusted within 365 days'],
        ['Warranty or maintenance advance', 'Period within business practice or 5 years, whichever is less'],
        ['Promoters\' unsecured loan required by a lender', 'Only until the bank or FI loan is repaid'],
        ['Start-up convertible note', '₹25 lakh or more in a single tranche from one person']], title='Rule 2(1)(c) exclusions')

    concepts = [
        C('c1', T1, [
            'Section 2(31): "deposit" covers any money received by a company by way of deposit, loan or in any other form, except categories prescribed in consultation with the RBI. The definition is inclusive, so the label used does not matter.',
            'Many receipts are excluded (see table). If excluded advances for goods, property or capital goods become refundable because the company lacks the required approval, they become deposits 15 days after falling due for refund.',
            'Deposits may be secured (fully, by a charge on tangible assets) or unsecured. A partly secured deposit is treated as unsecured and must be described so in every circular and advertisement.'],
          'A company borrowing from the public is treated like a bank in miniature, so the law looks at substance, not names.',
          'An employee required to keep a ₹7 lakh interest-free security deposit on a ₹6 lakh salary has made a deposit.',
          blocks=[excl]),
        C('c2', T2, [
            'Depositor: a member who deposits under section 73(2), or any person who deposits with a public company under section 76.',
            'Eligible company: a public company with net worth of at least ₹100 crore or turnover of at least ₹500 crore that has passed a special resolution and filed it with the Registrar before inviting public deposits. Within the borrowing limits of section 180(1)(c), an ordinary resolution is enough.',
            'Banking companies, NBFCs, housing finance companies registered with the NHB and other notified companies are outside these provisions. The deposit rules therefore govern non-financial companies such as manufacturers and traders.',
            'A private company can accept deposits only from its members. A public company that is not eligible can also accept only from its members.'],
          'Only big, approved public companies can knock on the general public\'s door.',
          'A public company with turnover of ₹420 crore and net worth of ₹80 crore may borrow only from its members.'),
        C('c3', T3, [
            'Section 73(2): a company accepting deposits from members must pass a resolution in general meeting; issue a circular in Form DPT-1 to members showing financial position, credit rating, number of depositors and dues; file it with the Registrar 30 days before issue; keep at least 20% of deposits maturing in the next year in a deposit repayment reserve account in a scheduled bank by 30 April; and certify that there has been no default in repaying deposits (or, if there was, that five years have passed since it was made good).',
            'The circular is valid until the earlier of six months after the close of the financial year or the date of the AGM (or its last due date); a fresh one is needed each year.',
            'Private companies are exempt from the circular, filing, reserve and certification steps if they accept from members up to 100% of paid-up capital, free reserves and securities premium; or are start-ups for five years from incorporation; or are not associate or subsidiary companies, have borrowings below twice paid-up capital or ₹50 crore (whichever is lower) and are not in default. They still file details in DPT-3.'],
          'Even borrowing from your own members needs transparency and a repayment cushion.',
          'A 3-year-old private start-up taking money from its members skips the DPT-1 circular but files DPT-3.'),
        C('c4', T4, [
            'Section 76: an eligible company may also accept deposits from the public, applying sections 73 and 74 with necessary changes.',
            'It must obtain a credit rating each year from an approved agency (at least investment grade) and state it in the invitation; publish its DPT-1 circular as a newspaper advertisement, in English and in the regional language, (and its website), filed with the Registrar at least 30 days earlier.',
            'Secured deposits need a charge on tangible assets (not intangibles) within 30 days, worth at least the deposits and interest, valued by a registered valuer, in favour of a trustee for depositors.',
            'Limits: from members 10% and from others 25% of paid-up capital, free reserves and securities premium; an eligible Government company 35% overall.'],
          'Public money comes with ratings, advertisements and a trustee watching.',
          'An eligible company offering secured deposits must create the charge within 30 days of acceptance.'),
        C('c5', T5, [
            'Tenure: not repayable on demand or within six months, and not longer than 36 months. Up to 10% of paid-up capital, free reserves and securities premium may be raised for short-term needs if repayable after at least three months.',
            'A company that is not eligible may accept up to 35% of that base from members; private companies up to 100%, and start-ups (10 years) and some small private companies without limit.',
            'Trustee for depositors: written consent, deposit trust deed in DPT-2 at least seven days before the circular, and independence from the company. Removal before the term ends needs consent of all directors present at a Board meeting, with an independent director present where required. The trustee calls a depositors\' meeting on requisition by one-tenth in value, or on a default.',
            'Other rules: interest and brokerage within RBI limits for NBFCs; brokerage only to authorised agents; depositor\'s declaration that the money is not borrowed; up to three joint holders; nomination; deposit receipt within 21 days; register kept for eight years; DPT-3 return by 30 June; penal interest of 18% p.a. on overdue claimed deposits; terms cannot be changed to the depositor\'s disadvantage.',
            'Premature repayment after six months: interest at 1% below the rate for the period actually run (a part year of six months or more counts as a full year; less is ignored).'],
          'Six months to 36 months, 21 days for the receipt, 18% if you are late.',
          'A deposit of 1 year 5 months is treated as 1 year for the premature repayment rate.'),
        C('c6', T6, [
            'Section 73(4): if a company fails to repay a deposit or interest, the depositor may apply to the Tribunal for payment and compensation for loss.',
            'Section 74: deposits accepted before 1 April 2014 that remained unpaid had to be reported to the Registrar within 3 months and repaid within three years or by maturity, whichever was earlier; the Tribunal may allow more time on the company\'s application. Default attracts a fine of ₹1 crore to ₹10 crore for the company and, for officers, imprisonment up to 7 years or fine of ₹25 lakh to ₹2 crore, or both.',
            'Section 76A: for accepting deposits in breach of sections 73 or 76, or failing to repay on time, the company pays the deposit and interest and a fine of at least ₹1 crore or twice the deposit (whichever is lower), up to ₹10 crore. Every officer in default faces imprisonment up to 7 years and a fine of ₹25 lakh to ₹2 crore; a wilful breach intended to deceive attracts section 447.',
            'Breach of a rule with no specific punishment: fine up to ₹5,000, plus up to ₹500 for each day a continuing breach lasts.'],
          'Taking deposits illegally is punished more harshly than most company law breaches.',
          'A company that illegally accepts ₹30 lakh faces a minimum fine of ₹60 lakh, as twice the deposit is lower than ₹1 crore.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Is this a deposit?', 'role': 'Audit assistant',
         'situation': 'While auditing a manufacturer, you find advances from customers, a loan from a director\'s brother and share application money held for five months.',
         'steps': ['Check whether customer advances were adjusted within 365 days.', 'Note the company type: a director\'s relative is excluded only for private companies.', 'Check allotment within 60 days or refund within 15 more days.', 'Report deposits in DPT-3 and the CARO comment.'],
         'takeaway': 'Test each receipt against the specific exclusion and its condition.'},
        {'id': 'j2', 'title': 'Planning a deposit scheme', 'role': 'Secretarial associate',
         'situation': 'A public company with net worth of ₹150 crore plans to raise public deposits.',
         'steps': ['Pass and file the special resolution.', 'Obtain credit rating and appoint a trustee with DPT-2.', 'File the DPT-1 advertisement 30 days before publication.', 'Fund the 20% repayment reserve by 30 April.'],
         'takeaway': 'Sequence matters: approvals and filings come before the advertisement.'},
    ]

    mcqs = [
        Q('m1', 'Share application money becomes a deposit if allotment is not made within 60 days and it is not refunded within:', ['15 days after those 60 days', '30 days after those 60 days', '7 days after those 60 days', '60 more days'], 0,
          'Application money is excluded only while it is appropriated against allotment. If securities are not allotted within 60 days and the money is not refunded within the next 15 days, it becomes a deposit. Adjusting it for another purpose is not a refund. In practice: diarise both dates.', 'c1', T1),
        Q('m2', 'An employee\'s non-interest-bearing security deposit is excluded from deposits only if it does not exceed:', ['His annual salary', 'Six months\' salary', '₹1,00,000', 'Twice his annual salary'], 0,
          'The rules exclude a non-interest-bearing security deposit taken from an employee under the contract of employment only up to the employee\'s annual salary. Anything larger is treated as a deposit. In practice: compare with current salary.', 'c1', T1),
        Q('m3', 'Money received by a public company from a director\'s relative is:', ['A deposit', 'Not a deposit if a declaration is given', 'Never a deposit', 'A loan outside the rules'], 0,
          'The exclusion covers money from a director of any company, but money from a director\'s relative is excluded only for a private company. For a public company it is a deposit. In practice: check who actually paid the money.', 'c1', T1, 'moderate'),
        Q('m4', 'A public company is an eligible company if it has net worth of at least:', ['₹100 crore or turnover of at least ₹500 crore', '₹50 crore or turnover of ₹250 crore', '₹500 crore and turnover of ₹100 crore', '₹10 crore'], 0,
          'Rule 2(1)(e) defines an eligible company as a public company with net worth of not less than ₹100 crore or turnover of not less than ₹500 crore that has the required shareholders\' approval filed with the Registrar. In practice: either test is enough.', 'c2', T2),
        Q('m5', 'Which company is NOT governed by the deposit provisions of the Companies Act?', ['A non-banking financial company', 'A listed manufacturing company', 'A private trading company', 'An unlisted public company'], 0,
          'Banking companies, NBFCs, NHB-registered housing finance companies and notified companies are excluded, because other regulators govern them. The rules target non-financial companies such as manufacturers and traders. In practice: check the RBI registration.', 'c2', T2),
        Q('m6', 'The deposit repayment reserve account must hold, by 30 April each year, at least:', ['20% of deposits maturing in the following financial year', '15% of all outstanding deposits', '10% of deposits accepted', '25% of deposits maturing'], 0,
          'Section 73(2)(c) requires at least 20% of deposits maturing in the next financial year to be kept in a separate scheduled bank account, used only for repaying deposits, and never allowed to fall below that level. In practice: plan the April cash need.', 'c3', T3),
        Q('m7', 'A private company is exempt from issuing the DPT-1 circular if it accepts from members not more than:', ['100% of paid-up capital, free reserves and securities premium', '35% of that aggregate', '25% of that aggregate', '10% of that aggregate'], 0,
          'Private companies accepting member money within 100% of paid-up capital, free reserves and securities premium are spared the circular, filing, reserve and certification steps, though they still report in DPT-3. Start-ups and some small companies get similar relief. In practice: compute the aggregate first.', 'c3', T3),
        Q('m8', 'The longest tenure for which a company may accept deposits is:', ['36 months', '24 months', '12 months', '60 months'], 0,
          'Deposits cannot be repayable on demand or within six months, and cannot be accepted for more than 36 months. Short-term deposits up to 10% of the base may run for three to six months. In practice: set scheme tenures between these limits.', 'c5', T5, 'core', check=36),
        Q('m9', 'An eligible company may accept deposits from persons other than members up to:', ['25% of paid-up capital, free reserves and securities premium', '10% of that aggregate', '35% of that aggregate', '50% of that aggregate'], 0,
          'For eligible companies the rules allow 10% from members and 25% from others, each measured on paid-up capital, free reserves and securities premium. An eligible Government company may go up to 35% overall. In practice: track the two limits separately.', 'c4', T4),
        Q('m10', 'A deposit receipt must be issued within:', ['21 days of receiving the money or realising the cheque', '7 days', '30 days', '45 days'], 0,
          'The rules require a receipt signed by an authorised officer within 21 days from receipt of money, realisation of the cheque or renewal, showing date, name, amount, rate and maturity. In practice: build this into the deposit process.', 'c5', T5, 'core', check=21),
        Q('m11', 'Penal interest payable on matured deposits claimed but not repaid is:', ['18% per annum for the overdue period', '12% per annum', '15% per annum', 'The contract rate only'], 0,
          'Rule 17 requires a penal rate of 18% per annum for the overdue period on deposits, secured or unsecured, that have matured and been claimed but remain unpaid. This is in addition to the punishment provisions. In practice: repay on time.', 'c5', T5),
        Q('m12', 'A deposit trust deed in Form DPT-2 must be executed:', ['At least 7 days before issuing the circular', 'Within 30 days after the circular', 'At the time of repayment', 'Within 21 days of acceptance'], 0,
          'Where secured deposits are invited, the company must appoint trustees with their written consent and execute the deposit trust deed at least seven days before issuing the circular or advertisement. In practice: the advertisement states the trustee\'s consent.', 'c5', T5),
        Q('m13', 'A company illegally accepts deposits of ₹40 lakh. The minimum fine on the company under section 76A is:', ['₹80 lakh', '₹1 crore', '₹40 lakh', '₹10 crore'], 0,
          'The minimum fine is ₹1 crore or twice the deposit accepted, whichever is lower: twice ₹40 lakh is ₹80 lakh, which is lower than ₹1 crore. The maximum is ₹10 crore, and the deposit with interest must also be repaid. In practice: officers face separate punishment.', 'c6', T6, 'hard', check=80),
        Q('m14', 'If a company fails to repay a deposit, the depositor can apply to:', ['The National Company Law Tribunal', 'The Registrar only', 'The RBI', 'The civil court only'], 0,
          'Section 73(4) lets the depositor apply to the Tribunal for an order directing payment of the sum due and compensation for any loss caused by non-payment. The Tribunal may pass other orders it thinks fit. In practice: keep the deposit receipt and claim letters.', 'c6', T6),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Eligibility test', 1, 'concept', 'turnover'),
           S('s2', 'Members and others limits', 2, 'computation', '10%|25%', nums=[mem, pub]),
           S('s3', 'Short-term limit', 1, 'computation', 'short', nums=[st]),
           S('s4', 'Non-eligible 35%', 1, 'computation', '35%', nums=[ne])],
          ['Show the common base first.'], ['Applying 35% to an eligible company.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, 'Sudha Pvt. Ltd. received ₹12 lakh from the brother of its managing director without any declaration, and ₹8 lakh as customer advance for machines delivered after 14 months. Are these deposits?',
          [legal('Rule 2(1)(c)(viii) and (xii)(a), Companies (Acceptance of Deposits) Rules, 2014',
                 'Money from a director\'s relative of a private company; trade advance adjusted after 14 months.',
                 'Money from a director\'s relative is excluded for a private company only if the relative declares in writing at the time that it is not borrowed money, and the Board\'s report discloses it. A trade advance is excluded only if adjusted against supply within 365 days, unless the advance is the subject of legal proceedings.',
                 'Without the declaration, ₹12 lakh is a deposit. The ₹8 lakh adjusted after 14 months also becomes a deposit.')],
          [S('s1', 'Relative exclusion and declaration', 1.5, 'concept', 'declaration'),
           S('s2', '365-day rule', 1.5, 'concept', '365'),
           S('s3', 'Conclusion', 1, 'conclusion', 'deposit')],
          ['Apply each exclusion with its condition.'], ['Ignoring the declaration requirement.'], ['Provision → facts → analysis → conclusion.']),
        W('q3', 5, i2['q'], i2['solution'],
          [S('s1', 'Period counted', 1, 'concept', '2 years|full year'),
           S('s2', 'Reduced rate', 1, 'computation', '1%', nums=[rate]),
           S('s3', 'Interest for period run', 1.5, 'computation', '18/12', nums=[intr]),
           S('s4', 'Penal interest', 1.5, 'computation', '18%', nums=[pen])],
          ['State the rounding rule for part years.'], ['Using the 3-year rate.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What makes a public company an eligible company?',
          'A public company with net worth of at least ₹100 crore or turnover of at least ₹500 crore, which has passed a special resolution and filed it with the Registrar before inviting deposits from the public.',
          [P('p1', 'Size tests', 6, 'net worth|turnover'), P('p2', 'Resolution filed', 4, 'resolution')], 'c2'),
        V('v2', 'What is the deposit repayment reserve account?',
          'A separate scheduled bank account in which a company keeps, by 30 April each year, at least 20% of deposits maturing in the next financial year, to be used only for repaying deposits.',
          [P('p1', '20% of maturing deposits', 6, '20'), P('p2', '30 April / separate account', 4, 'april|separate')], 'c3'),
        V('v3', 'What are the tenure limits for deposits?',
          'Deposits must be for at least six months and at most 36 months; up to 10% of capital, free reserves and premium may be taken for three to six months for short-term needs.',
          [P('p1', 'Six to 36 months', 6, '36|six'), P('p2', 'Short-term exception', 4, '10%|three months|3 months')], 'c5'),
        V('v4', 'When can a trustee for depositors be removed?',
          'Only with the consent of all directors present at a Board meeting, with at least one independent director present where the company must have independent directors.',
          [P('p1', 'All directors present', 6, 'all'), P('p2', 'Independent director', 4, 'independent')], 'c5'),
        V('v5', 'What punishment applies to officers for accepting deposits illegally?',
          'Imprisonment up to seven years and a fine of ₹25 lakh to ₹2 crore; if the breach was wilful and meant to deceive, action for fraud under section 447.',
          [P('p1', 'Seven years and fine', 6, 'seven|7'), P('p2', 'Fraud under 447', 4, '447|fraud')], 'c6'),
    ]

    cases = [{'id': 'k1', 'title': 'Sunshine Appliances Pvt. Ltd.', 'difficulty': 'moderate',
              'case': 'Sunshine Appliances Pvt. Ltd., incorporated 7 years ago, is a subsidiary of a listed company. Its paid-up capital is ₹5 crore, free reserves ₹3 crore and securities premium ₹2 crore. It wants to accept deposits from its members and from some customers\' relatives, offering 6-month and 48-month schemes and a cash gift to whoever brings in depositors.',
              'mcqs': [
                  M('k1a', 'Deposits from customers\' relatives who are not members are:', ['Not allowed, as a private company may accept deposits only from members', 'Allowed up to 25%', 'Allowed with a special resolution', 'Allowed if secured'], 0,
                    'A private company can accept deposits only from its members. Only an eligible public company can take deposits from the public. In practice: the scheme must be restricted to members.', 'core', topic=T2),
                  M('k1b', 'Maximum member deposits Sunshine may accept:', ['₹10 crore', '₹3.5 crore', '₹2.5 crore', 'No limit'], 0,
                    'A private company may accept from members up to 100% of paid-up capital, free reserves and securities premium: ₹5 + 3 + 2 = ₹10 crore. Being a subsidiary, it does not get the unlimited relief for small companies. In practice: report in DPT-3.', 'moderate', check=10, topic=T5),
                  M('k1c', 'The 48-month scheme is:', ['Not permitted, as tenure cannot exceed 36 months', 'Permitted for members', 'Permitted if secured', 'Permitted with Tribunal approval'], 0,
                    'The rules cap the tenure of any deposit at 36 months; a 48-month deposit cannot be accepted or renewed. The 6-month scheme is within limits. In practice: redesign to 36 months or less.', 'core', topic=T5),
                  M('k1d', 'The cash gift to people who bring in depositors is:', ['Brokerage allowed only to persons authorised in writing who actually procure deposits, within RBI limits', 'Always allowed', 'Allowed only to directors', 'Never allowed in any form'], 0,
                    'Brokerage may be paid only to a person authorised in writing to solicit deposits and through whom deposits are actually procured, within the rates prescribed for NBFCs. Gifts to anyone else breach the rules. In practice: appoint authorised agents.', 'moderate', topic=T5),
              ]}]

    return unit(UID, 'p2', 'int-p2-ch05', 1, 'Acceptance of Deposits by Companies',
                ['Explain the meaning of deposit and identify amounts excluded from it.',
                 'Distinguish depositors, eligible companies and exempt companies.',
                 'Apply the procedure and limits for deposits from members and from the public.',
                 'Explain trustee, tenure, interest and procedural rules.',
                 'Explain the remedies and punishments for default.'],
                {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 35}, 'prereq': ['int-p2-ch04-u01'],
                 'exam_tip': 'Exclusions come with conditions — always state the condition (60+15 days, annual salary, 365 days, 5 years, ₹25 lakh single tranche).'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Deposit = any receipt by way of deposit, loan or otherwise, less prescribed exclusions.',
                             'Eligible company: public, net worth ≥ ₹100 crore or turnover ≥ ₹500 crore, special resolution filed.',
                             'Members: resolution, DPT-1 circular filed 30 days earlier, 20% reserve by 30 April, no-default certificate.',
                             'Limits: 35% (members of non-eligible), 10% + 25% (eligible), 100% (private).',
                             'Tenure 6–36 months; short-term 10% for 3–6 months.',
                             'Receipt 21 days; register 8 years; DPT-3 by 30 June; penal 18%.',
                             's. 76A: company ₹1 crore or 2× deposit (lower) to ₹10 crore; officers 7 years + ₹25 lakh–₹2 crore.'],
                 'remember': ['Director\'s relative excluded only for private companies.', 'Partly secured = unsecured.'],
                 'traps': ['Eligible company member limit is 10%, not 35%.', 'Premature rate is 1% below the rate for the period run, not the contracted period.']},
                [('Eligible company', '₹100 crore NW or ₹500 crore turnover'), ('Tenure', '6–36 months'), ('Repayment reserve', '20% by 30 April'), ('Penal interest', '18% p.a.'), ('Receipt', '21 days')],
                viva, cases)
