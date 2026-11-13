"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 14 Unit 1 Special Features of Audit of Banks.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch14-u01'
T1 = 'Legal framework, appointment and conducting a bank audit'
T2 = 'Internal controls and CRR/SLR compliance'
T3 = 'Advances: IRAC norms and NPA verification'
T4 = 'Capital, Basel III, reports, LFAR and concurrent audit'


def build():
    ck = Checks()
    days = ck.add('31+29+31', 'Days overdue from 31 December to 31 March in a leap year')
    crar = ck.add('round(1080/10000*100,2)', 'Capital to risk-weighted assets ratio (%)')
    i1 = {'id': 'i1', 'title': 'Is the loan an NPA?', 'difficulty': 'moderate', 'minutes': 8,
          'q': '(a) A term loan instalment fell due on 31 December and is still unpaid at the bank\'s year end of 31 March (in a leap year). Is the loan an NPA? (b) The bank\'s total capital is ₹1,080 crore and risk-weighted assets ₹10,000 crore. Compute CRAR and compare with RBI\'s minimum of 9%.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Days overdue', 'January 31 + February 29 + March 31', inr(days) + ' days'],
              ['NPA status', 'Overdue more than 90 days', 'NPA — substandard'],
              ['CRAR', '1,080 ÷ 10,000', inr(crar) + '%'],
              ['Compliance', '10.8% vs 9% minimum (plus conservation buffer)', 'Meets minimum CRAR']], title='IRAC and capital')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Red flags in a branch audit', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'In a branch audit, the auditor finds: (a) cash credit accounts with drawing power based on stock statements six months old; (b) a large account regularised on 30 March by a fresh loan from the same bank; (c) suspense accounts with old unreconciled entries; (d) gold loans where valuation was not done. Comment.',
          'solution': [table(['Finding', 'Comment'], [
              ['(a)', 'Drawing power based on stale stock statements — irregular; account may need NPA review'],
              ['(b)', 'Ever-greening — regularisation through fresh funds from the bank is not genuine; treat as NPA if criteria met'],
              ['(c)', 'Risk of fraud/misstatement; report in LFAR and to management'],
              ['(d)', 'Security not verified — weakness; check valuations and provisioning']], title='Advances audit')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Banks are governed by the Banking Regulation Act, 1949, RBI Act, and Companies Act (for banking companies); statements follow the Third Schedule forms. Statutory central auditors and branch auditors are appointed with RBI approval; eligibility norms and numbers of auditors depend on asset size, with rotation limits.',
            'RBI requires statutory central auditors to audit top branches covering a minimum proportion of advances (e.g. top 20 branches or top 20% for smaller banks, covering at least 15% of gross advances); section 143(8) applies to branch audits.',
            'Conducting the audit involves understanding the bank\'s systems (core banking), reviewing internal audit, inspection and concurrent audit reports, RBI inspection findings and closing instructions, and assessing risks in advances, investments and treasury.'],
          'Bank audits run on RBI rules as much as on SAs.',
          'Central auditors review branch auditors\' reports before consolidating findings.'),
        C('c2', T2, [
            'Key internal control areas: cash, deposits, advances (sanction, disbursement, monitoring), investments and treasury (segregation of front, mid and back office), foreign exchange, inter-branch reconciliation, suspense accounts, IT and access controls.',
            'CRR (cash reserve ratio) requires a percentage of net demand and time liabilities to be kept with RBI; SLR (statutory liquidity ratio) requires holding liquid assets such as government securities. The auditor verifies computation of NDTL and compliance, reporting defaults.',
            'Weak controls are reported in the Long Form Audit Report (LFAR) and to management.'],
          'Liquidity and control compliance are audit focus areas in banks.',
          'Old unreconciled inter-branch entries signal fraud risk.'),
        C('c3', T3, [
            'Income recognition and asset classification (IRAC) norms: an advance becomes non-performing when interest or instalment remains overdue for more than 90 days (term loans), or the account remains out of order for 90 days (cash credit/overdraft), or bills remain overdue 90 days; agricultural loans follow crop season rules.',
            'NPAs are classified as substandard, doubtful (sub-categories by age) or loss assets; interest on NPAs is not recognised as income until realised; provisions follow RBI percentages on secured and unsecured portions.',
            'Auditors verify sanction, documentation, security, drawing power, stock statements, regularisation near year end, restructuring, ever-greening and provisioning; and the classification is borrower-wise, not facility-wise.'],
          '90 days overdue is the line between performing and non-performing.',
          'Regularising an account by sanctioning a new loan from the same bank is ever-greening.'),
        C('c4', T4, [
            'Capital: Basel III requires minimum CRAR (9% in India) plus capital conservation buffer, with common equity tier 1 and additional tier 1 components; stress testing assesses resilience. Auditors verify capital computation and risk weights.',
            'Reports: the main audit report under the Banking Regulation Act and/or Companies Act; the Long Form Audit Report (LFAR) prescribed by RBI covering detailed matters on advances, deposits, controls; and certificates such as on SLR, CRR, and compliance.',
            'Concurrent audit is a real-time examination of transactions at branches or treasury, covering a specified share of business, appointed by the bank, with reporting systems to management and the audit committee. The bank\'s audit committee oversees audit functions.'],
          'Capital adequacy, LFAR and concurrent audit complete the bank audit picture.',
          'A CRAR of 10.8% exceeds the 9% minimum but must also meet buffers.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Branch statutory audit', 'role': 'Branch auditor',
             'situation': 'Large advances branch with 2,000 borrower accounts.',
             'steps': ['Review RBI closing instructions and prior LFAR.', 'Test top advances for IRAC compliance.', 'Verify CRR/SLR-related returns and cash.', 'Report in main report and LFAR.'],
             'takeaway': 'Focus on advances — that is where most misstatements arise.'}]

    mcqs = [
        Q('m1', 'A term loan becomes an NPA when interest or instalment remains overdue for more than:', ['Ninety days', 'Thirty days', 'One year', 'Sixty days'], 0,
          'IRAC norm. In practice: borrower-wise.', 'c3', T3),
        Q('m2', 'Interest on NPAs is recognised:', ['Only when actually realised', 'On accrual', 'Never', 'At year end'], 0,
          'Income recognition. In practice: reverse unrealised interest.', 'c3', T3),
        Q('m3', 'RBI\'s minimum CRAR for banks in India is:', ['Nine percent plus buffers', 'Eight percent', 'Twelve percent', 'Five percent'], 0,
          'Plus capital conservation buffer. In practice: Basel III.', 'c4', T4),
        Q('m4', 'The Long Form Audit Report is prescribed by:', ['RBI', 'SEBI', 'ICAI only', 'MCA'], 0,
          'Detailed reporting. In practice: separate from main report.', 'c4', T4),
        Q('m5', 'SLR requires banks to hold:', ['Liquid assets such as government securities', 'Cash with RBI only', 'Equity shares', 'Gold only'], 0,
          'CRR is cash with RBI. In practice: verify NDTL.', 'c2', T2),
        Q('m6', 'Regularising an NPA account by a fresh loan from the same bank is:', ['Ever-greening and not genuine', 'Acceptable', 'Required', 'A KAM'], 0,
          'Classification stays NPA. In practice: check source of funds.', 'c3', T3),
        Q('m7', 'Asset classification of a borrower is done:', ['Borrower-wise across facilities', 'Facility-wise only', 'Branch-wise', 'Randomly'], 0,
          'One NPA facility taints all. In practice: check all accounts.', 'c3', T3),
        Q('m8', 'Concurrent audit is:', ['Real-time examination of transactions during the year', 'Year-end audit', 'Tax audit', 'Peer review'], 0,
          'Appointed by bank. In practice: reports to management.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Overdue days', 2, 'computation', 'overdue|days', nums=[days]), S('s2', 'NPA', 1.5, 'concept', 'npa'), S('s3', 'CRAR', 2.5, 'computation', 'crar', nums=[crar])],
          ['Count days carefully.'], ['Treating 90 days exactly as NPA.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Drawing power', 1.5, 'concept', 'drawing power'), S('s2', 'Ever-greening', 2, 'concept', 'ever-greening'), S('s3', 'Suspense and security', 2.5, 'concept', 'suspense|security|valuation')],
          ['Link to IRAC.'], ['Accepting year-end regularisation.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'When does a cash credit account become an NPA?', 'When it remains out of order for 90 days, such as outstanding continuously above the drawing power or with no credits sufficient to cover interest.',
          [P('p1', 'Out of order', 5, 'out of order'), P('p2', '90 days', 5, '90 days')], 'c3'),
        V('v2', 'What are the NPA categories?', 'Substandard, doubtful and loss assets.',
          [P('p1', 'Substandard and doubtful', 5, 'substandard|doubtful'), P('p2', 'Loss', 5, 'loss')], 'c3'),
        V('v3', 'Distinguish CRR and SLR.', 'CRR is cash kept with RBI as a share of NDTL; SLR is liquid assets like government securities held by the bank.',
          [P('p1', 'Cash with RBI', 5, 'cash'), P('p2', 'Liquid assets', 5, 'liquid')], 'c2'),
        V('v4', 'What is the LFAR?', 'A detailed report prescribed by RBI that auditors submit on matters like advances, deposits and controls in addition to the main audit report.',
          [P('p1', 'Prescribed by RBI', 5, 'rbi'), P('p2', 'Detailed matters', 5, 'advances|controls')], 'c4'),
        V('v5', 'What should auditors check in advances?', 'Sanction, documentation, security, drawing power, stock statements, year-end regularisation, restructuring and provisioning.',
          [P('p1', 'Sanction and security', 5, 'sanction|security'), P('p2', 'Provisioning', 5, 'provision')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Unity Co-op Bank branch', 'difficulty': 'moderate',
              'case': 'A branch has a ₹3 crore cash credit to Manish Traders, outstanding above drawing power since 15 November; the bank year end is 31 March. The borrower also has a term loan with the branch that is regular. Interest of ₹18 lakh on the cash credit was credited to income.',
              'mcqs': [
                  M('k1a', 'The cash credit at 31 March is:', ['An NPA, being out of order over 90 days', 'Standard', 'Special mention only', 'Written off'], 0,
                    'Continuously above DP > 90 days. In practice: verify dates.', 'core', topic=T3),
                  M('k1b', 'The regular term loan of the same borrower is:', ['Also classified NPA (borrower-wise)', 'Standard', 'Loss asset', 'Excluded'], 0,
                    'Borrower-wise classification. In practice: check all facilities.', 'moderate', topic=T3),
                  M('k1c', 'The ₹18 lakh interest credited to income should be:', ['Reversed if unrealised', 'Kept', 'Doubled', 'Moved to capital'], 0,
                    'Income recognition on NPAs. In practice: memorandum account.', 'core', topic=T3),
                  M('k1d', 'These matters are also reported in:', ['The LFAR', 'CARO', 'SA 810 report', 'Tax audit report'], 0,
                    'RBI-prescribed. In practice: CARO not applicable to banks.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch14', 1, 'Special Features of Audit of Banks',
                ['Explain the legal framework and appointment of bank auditors.',
                 'Evaluate internal controls and CRR/SLR compliance.',
                 'Apply IRAC norms in auditing advances.',
                 'Verify capital adequacy and prepare LFAR and other reports.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 25}, 'prereq': ['fin-p3-ch13-u01'],
                 'exam_tip': 'For advances, test the 90-day rule, borrower-wise classification and income reversal.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['BR Act, RBI rules, Third Schedule.',
                             'CRR/SLR compliance verified.',
                             'NPA: > 90 days overdue/out of order.',
                             'Borrower-wise; no income on NPAs until realised.',
                             'Basel III CRAR 9%+; LFAR; concurrent audit.'],
                 'remember': ['Watch for ever-greening near year end.'],
                 'traps': ['Classifying facility-wise.']},
                [('NPA', '> 90 days'), ('CRAR', '9% + buffer'), ('LFAR', 'RBI-prescribed'), ('Classification', 'Borrower-wise')],
                viva, cases)
