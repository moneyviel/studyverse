"""CA Intermediate · Paper 5 Auditing and Ethics · Chapter 10 Audit of Banks.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p5-ch10-u01'
T1 = 'Bank audit framework: appointment, powers, reports and approach'
T2 = 'Advances: classification and NPA norms'
T3 = 'Drawing power and review of advances'
T4 = 'Audit of income and expenses'


def build():
    ck = Checks()
    ps = ck.add('100-6-30', 'Paid stock (₹ lakh): stock − obsolete − creditors for goods')
    ds = ck.add('64*75/100', 'Drawing power on stock after 25% margin')
    dd = ck.add('(50-10)*70/100', 'Drawing power on debtors up to 90 days after 30% margin')
    dp = ck.add('48+28', 'Drawing power (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Computing drawing power', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'A borrower has a cash credit limit of ₹80 lakh against paid stock (margin 25%) and debtors up to 90 days (margin 30%). Stock ₹100 lakh includes obsolete items ₹6 lakh; creditors for goods ₹30 lakh; debtors ₹50 lakh include ₹10 lakh over 90 days. Compute drawing power. The outstanding balance is ₹79 lakh — comment.',
          'solution': [table(['Step', 'Working', '₹ lakh'], [
              ['Paid stock', '100 − 6 obsolete − 30 creditors', inr(ps)],
              ['Less 25% margin', '64 × 75%', inr(ds)],
              ['Eligible debtors', '50 − 10 over 90 days', inr(40)],
              ['Less 30% margin', '40 × 70%', inr(dd)],
              ['Drawing power', 'Lower of this and limit ₹80 lakh', inr(dp)]], title='Drawing power'),
              p('Outstanding of ₹79 lakh exceeds the drawing power of ₹76 lakh; if it stays above drawing power continuously for 90 days the account is "out of order" and may become an NPA.')],
          'checks': list(ck)}

    ck2 = Checks()
    p_ss = ck2.add('10*15/100', 'Substandard (₹ lakh) at 15%')
    p_d1 = ck2.add('6*25/100 + 2*100/100', 'Doubtful D1: secured 25% + unsecured 100%')
    p_l = ck2.add('1*100/100', 'Loss asset at 100%')
    tot = ck2.add('1.5+3.5+1', 'Total provision (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Provisioning for NPAs', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A branch\'s NPAs: substandard ₹10 lakh (fully secured); doubtful for 8 months (D1) ₹8 lakh, of which ₹6 lakh is covered by realisable security; loss asset ₹1 lakh. Compute the minimum provision.',
          'solution': [table(['Category', 'Working', '₹ lakh'], [
              ['Substandard', '15% of 10', inr(p_ss)],
              ['Doubtful (D1)', '25% of secured 6 + 100% of unsecured 2', inr(p_d1)],
              ['Loss', '100% of 1', inr(p_l)],
              ['Total', '', inr(tot)]], title='Prudential provisioning')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Auditors of banking companies are appointed at the AGM, and of nationalised banks by the Board — in both cases with RBI\'s prior approval; RRB auditors are appointed with the Central Government\'s approval. Eligibility follows company auditor rules; remuneration of a banking company\'s auditor follows section 142 of the Companies Act, while for nationalised banks and SBI it is fixed by RBI in consultation with the Government. Powers of access are the same as a company auditor\'s.',
            'Reports: the main audit report under the Banking Regulation Act and other laws; the Long Form Audit Report (LFAR) on matters RBI requires (central auditors submit by 30 June); and certificates and reports to RBI on specific matters.',
            'Approach: understand the bank\'s systems (largely core banking software), assess risks (credit, market, operational), evaluate internal controls, rely where possible on internal and concurrent audit and RBI inspection, and focus on high-risk areas — advances, investments, income recognition.'],
          'A bank audit is about trust in lending and the systems that record it.',
          'An auditor visiting a branch reviews the CBS exception reports before testing loans.'),
        C('c2', T2, [
            'Advances comprise loans, cash credits, overdrafts and bills purchased and discounted, disclosed by nature (secured, covered by guarantees, unsecured) and by sector.',
            'A non-performing asset (NPA) is a loan where interest or instalment remains overdue for more than 90 days for a term loan; a cash credit or overdraft account that stays "out of order" for 90 days; bills overdue for more than 90 days; and agricultural loans by crop season tests. Classification is based on record of recovery, not on security.',
            'Categories: standard; substandard (NPA up to 12 months) — 15%; doubtful (substandard for 12 months) — secured portion 25% (D1, up to 1 year), 40% (D2, 1–3 years), 100% (D3, over 3 years), plus 100% on the unsecured portion; loss assets — 100%.',
            'Income on NPAs is not recognised until actually received; interest booked but not received when an account becomes an NPA is reversed.'],
          'NPA rules turn on how long money has been overdue; provisioning rises with age and falls with security.',
          'A term loan with an instalment due on 31 December unpaid till 31 March (90 days) becomes an NPA on the 91st day.'),
        C('c3', T3, [
            'Drawing power is the amount a borrower may draw in a working capital account, based on the value of eligible security (paid stock and eligible debtors) less stipulated margins, limited to the sanctioned limit.',
            'Paid stock means stock less creditors for goods; obsolete or damaged stock and debtors beyond the permitted age are excluded.',
            'An account is out of order if the outstanding balance stays continuously above the sanctioned limit or drawing power, or if there are no credits for 90 days, or credits do not cover interest. Auditors check stock statements, inspection reports, renewal of limits, security documentation and periodic review.'],
          'Drawing power ensures the loan is always backed by current security, not just by the limit on paper.',
          'A borrower whose stock falls sharply loses drawing power even if the sanctioned limit is unchanged.'),
        C('c4', T4, [
            'Income: interest on advances (verify rates, application, non-recognition on NPAs), discount on bills, commission and exchange, fees, and income from investments. Analytical procedures (yield on average advances) help detect errors.',
            'Expenses: interest on deposits (recompute for samples and check rate changes), staff costs, rent, provisions and contingencies; ensure prior period items are disclosed.',
            'Auditors also verify balances with RBI and other banks, inter-branch reconciliation, and suspense and sundry accounts that may hide irregularities.'],
          'Interest income should match the loan book; interest expense should match deposits.',
          'If average advances are ₹100 crore at 10% yield but interest income is ₹8 crore, the gap needs investigation.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Branch audit of advances', 'role': 'Audit assistant',
             'situation': 'You are asked to test 25 large borrower accounts at a branch.',
             'steps': ['Check sanction, documentation and security creation.', 'Recompute drawing power from stock statements.', 'Test overdue status for NPA classification.', 'Recompute provisions and income reversal.'],
             'takeaway': 'Classification first, provision second, income recognition third.'}]

    mcqs = [
        Q('m1', 'A term loan becomes an NPA when interest or instalment remains overdue for more than:', ['90 days', '60 days', '180 days', '30 days'], 0,
          'The 90-day overdue norm applies to term loans. In practice: cash credits use the out-of-order test.', 'c2', T2, check=90),
        Q('m2', 'Provision on a substandard asset is:', ['15%', '25%', '40%', '100%'], 0,
          'Substandard assets need 15% (with higher rates for certain unsecured exposures). In practice: computed on outstanding.', 'c2', T2, check=15),
        Q('m3', 'NPA classification is based on:', ['Record of recovery', 'Value of security', 'Net worth of guarantor', 'Borrower\'s turnover'], 0,
          'Security affects provisioning, not classification. In practice: a well-secured loan can still be an NPA.', 'c2', T2),
        Q('m4', 'The unsecured portion of a doubtful asset is provided at:', ['100%', '25%', '40%', '15%'], 0,
          'Unsecured portions of doubtful assets are fully provided regardless of age. In practice: secured portion varies by age.', 'c2', T2, check=100),
        Q('m5', 'An auditor of a nationalised bank is appointed by:', ['The bank\'s Board with RBI approval', 'Shareholders at AGM', 'C&AG', 'Central Government alone'], 0,
          'Nationalised banks appoint through their Board, with RBI\'s prior approval. In practice: banking companies appoint at the AGM.', 'c1', T1),
        Q('m6', 'Paid stock for drawing power is:', ['Stock less creditors for goods', 'Stock plus debtors', 'Stock less margin', 'Stock at selling price'], 0,
          'Only stock financed by the borrower\'s own funds counts. In practice: exclude obsolete stock.', 'c3', T3),
        Q('m7', 'A cash credit account is "out of order" if:', ['The balance stays above drawing power continuously for 90 days', 'There is one debit a month', 'Interest is charged monthly', 'The limit is renewed'], 0,
          'Continuous excess over limit or drawing power, or no credits for 90 days, or credits insufficient to cover interest. In practice: check daily balances.', 'c3', T3),
        Q('m8', 'Interest on an NPA account is recognised:', ['Only when actually received', 'On accrual', 'At the rate of 15%', 'Never'], 0,
          'Income recognition on NPAs is on a cash basis. In practice: reverse unrealised interest when an account slips.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Paid stock', 1, 'computation', 'paid stock', nums=[ps]), S('s2', 'Margins', 2, 'computation', 'margin', nums=[ds, dd]),
           S('s3', 'Drawing power', 1, 'computation', 'drawing power', nums=[dp]), S('s4', 'Comment', 1, 'concept', 'out of order')],
          ['Exclude ineligible items first.'], ['Applying margin before deducting creditors.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Substandard', 1, 'computation', '15%', nums=[p_ss]), S('s2', 'D1 split', 2, 'computation', '25%|100%', nums=[p_d1]), S('s3', 'Total', 1, 'computation', 'total', nums=[tot])],
          ['Split secured and unsecured.'], ['Applying 25% to the unsecured part.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is an LFAR?', 'A Long Form Audit Report in which bank auditors report to the bank on specific matters required by RBI, in addition to the main audit report.',
          [P('p1', 'Long form', 5, 'long form'), P('p2', 'RBI matters', 5, 'rbi')], 'c1'),
        V('v2', 'How is a doubtful asset provided for?', 'Unsecured portion at 100%; secured portion at 25%, 40% or 100% depending on whether it has been doubtful up to one year, one to three years or more than three years.',
          [P('p1', 'Unsecured 100%', 5, '100%'), P('p2', 'Secured by age', 5, '25%|40%')], 'c2'),
        V('v3', 'When is an account out of order?', 'When the balance stays continuously above the sanctioned limit or drawing power, or there are no credits for 90 days, or credits do not cover interest.',
          [P('p1', 'Above limit or DP', 5, 'limit|drawing power'), P('p2', '90 days credits', 5, '90 days|credits')], 'c3'),
        V('v4', 'Why is security ignored for NPA classification?', 'Because classification depends on the borrower\'s repayment record; security only affects the amount of provision.',
          [P('p1', 'Repayment record', 6, 'record|repayment'), P('p2', 'Provision', 4, 'provision')], 'c2'),
        V('v5', 'Name an analytical check on interest income.', 'Comparing interest income with average advances multiplied by the average yield, and investigating large differences.',
          [P('p1', 'Average advances', 5, 'average'), P('p2', 'Yield', 5, 'yield|rate')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Coastal Co-op Bank branch', 'difficulty': 'moderate',
              'case': 'At 31 March, a branch shows: a term loan of ₹20 lakh with instalments unpaid since 15 November; a cash credit of ₹15 lakh (within its limit) with no credits since 15 December; a doubtful loan in D2 of ₹10 lakh, secured to ₹4 lakh; and interest of ₹1.2 lakh accrued on the term loan this year but not received.',
              'mcqs': [
                  M('k1a', 'Is the term loan an NPA at 31 March?', ['Yes, overdue for more than 90 days', 'No', 'Only if unsecured', 'Only after 12 months'], 0,
                    'Unpaid since 15 November — over 90 days by 31 March. In practice: classify as substandard.', 'core', topic=T2),
                  M('k1b', 'The cash credit with no credits since 15 December is:', ['Out of order, as there have been no credits for over 90 days', 'Regular, as it is within its limit', 'A loss asset', 'Automatically doubtful'], 0,
                    'An account within limit is still out of order if no credits come in for 90 days continuously; at 90 days out of order it becomes an NPA. In practice: classify as substandard.', 'moderate', topic=T3),
                  M('k1c', 'Provision on the D2 loan (₹ lakh):', ['7.6', '6.0', '10.0', '4.0'], 0,
                    'Secured 4 × 40% = 1.6 + unsecured 6 × 100% = 6.0 → 7.6. In practice: check security valuation.', 'moderate', check=7.6, topic=T2),
                  M('k1d', 'Interest of ₹1.2 lakh on the NPA term loan should be:', ['Reversed — recognised only on receipt', 'Kept as income', 'Provided at 15%', 'Capitalised'], 0,
                    'Income on NPAs is recognised on realisation. In practice: reverse unrealised interest.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p5', 'int-p5-ch10', 1, 'Audit of Banks',
                ['Explain the appointment, powers and reporting of bank auditors.',
                 'Apply NPA classification and provisioning norms.',
                 'Compute drawing power and review advances.',
                 'Audit income and expenses of a bank.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 35}, 'prereq': ['int-p5-ch09-u01'],
                 'exam_tip': 'In NPA questions, count days carefully and separate secured and unsecured portions.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Appointment with RBI approval; LFAR by 30 June for central auditors.',
                             'NPA: > 90 days overdue; out-of-order for CC/OD.',
                             'Provisions: SS 15%; D1/D2/D3 secured 25/40/100% + unsecured 100%; loss 100%.',
                             'Drawing power: (paid stock − margin) + (eligible debtors − margin), within limit.',
                             'NPA income on cash basis.'],
                 'remember': ['Security affects provision, not classification.'],
                 'traps': ['Paid stock = stock − creditors for goods.']},
                [('NPA', '> 90 days'), ('Substandard', '15%'), ('D1/D2/D3 secured', '25/40/100%'), ('Unsecured doubtful', '100%')],
                viva, cases)
