"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 14 Unit 2 Special Features of Audit of NBFCs.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch14-u02'
T1 = 'NBFCs, registration and scale-based regulation'
T2 = 'Prudential norms: capital, income recognition and provisioning'
T3 = 'Audit procedures, frauds and auditor\'s duties'
T4 = 'Ind AS and Schedule III Division III for NBFCs'


def build():
    ck = Checks()
    nof = ck.add('10', 'Minimum NOF for most NBFCs after the phase-in (₹ crore)')
    days_ok = ck.add('91', 'Days overdue in the case (days)')
    i1 = {'id': 'i1', 'title': 'NPA timing for an NBFC loan', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'An NBFC in the base layer has a loan with an instalment overdue by 91 days at 31 March 2026. Under RBI\'s glide path, NBFCs must move to the 90-day NPA norm by 31 March 2026. Is the loan an NPA? Also state the minimum net owned fund most NBFCs need after the phase-in.',
          'solution': [table(['Point', 'Analysis', 'Result'], [
              ['Overdue period', inr(days_ok) + ' days at 31 March 2026', 'More than 90 days'],
              ['Glide path', '> 90 days norm applies by 31 March 2026', 'NPA'],
              ['Income', 'Unrealised interest reversed', '—'],
              ['Minimum NOF', 'Phased increase from ₹2 crore', '₹' + inr(nof) + ' crore (with stated exceptions)']], title='RBI norms for NBFCs')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Is it an NBFC?', 'difficulty': 'core', 'minutes': 6,
          'q': 'A company\'s financial assets are 55% of total assets and income from financial assets is 60% of gross income. Another company\'s figures are 40% and 70%. Which needs NBFC registration under the principal business criteria?',
          'solution': [table(['Company', 'Test', 'Result'], [
              ['First', 'Both above 50%', 'Principal business is financial — registration needed (if NOF met)'],
              ['Second', 'Assets test not met', 'Not an NBFC under the 50-50 test']], title='Principal business test')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'NBFCs are companies registered under the Companies Act engaged mainly in lending, investing in securities, leasing, hire purchase and similar financial activities (excluding agriculture, industrial and real estate businesses as principal activities). The principal business test: financial assets over 50% of total assets and financial income over 50% of gross income.',
            'Registration with RBI under section 45-IA of the RBI Act requires a minimum net owned fund, being raised in phases from ₹2 crore to ₹10 crore for most existing NBFCs by 31 March 2027; P2P lenders, account aggregators and NBFCs without public funds or customer interface stay at ₹2 crore, while IFCs and IDF-NBFCs need ₹300 crore.',
            'Scale-based regulation classifies NBFCs into base, middle, upper and top layers by size and risk, with stricter capital, governance and prudential norms as layers rise. Banks and NBFCs differ in deposits (NBFCs cannot accept demand deposits), payment systems and deposit insurance.'],
          'NBFCs are lenders without bank licences, regulated by layer.',
          'An NBFC cannot issue cheques drawn on itself like a bank.'),
        C('c2', T2, [
            'Capital requirements: deposit-taking and middle/upper layer NBFCs maintain minimum capital ratios (e.g. CRAR of 15% with Tier 1 at least 10% for applicable NBFCs).',
            'Income recognition: income on NPAs is recognised only on realisation. NPA norms historically used 180 days; RBI\'s glide path moved NBFCs to 90 days in stages (150 days by March 2024, 120 days by March 2025, 90 days by March 2026).',
            'Provisioning follows asset classification (standard, substandard, doubtful, loss) under RBI directions for NBFCs not on Ind AS; Ind AS NBFCs use expected credit loss, with a prudential floor comparison under RBI\'s Ind AS guidance.'],
          'Same IRAC logic as banks, with NBFC-specific timelines.',
          'From March 2026, NBFCs classify loans overdue beyond 90 days as NPAs.'),
        C('c3', T3, [
            'Audit procedures: verify registration and NOF; compliance with prudential norms; loan sanction, disbursement, documentation, security and classification; investments and valuation; borrowings and asset-liability mismatch; and related party exposures.',
            'Frauds in NBFCs are classified and reported to RBI under its directions; auditors report frauds as required by the Companies Act and RBI.',
            'Auditor\'s duties: report under the RBI\'s NBFC Auditor\'s Report Directions (registration, NOF, prudential compliance, public deposits), CARO 2020 clauses (including whether registration is required), RBI rules on appointment of statutory auditors (eligibility, tenure, rotation) and certification of supervisory returns.'],
          'NBFC auditors report to shareholders and to RBI.',
          'An auditor must report to RBI if an NBFC accepts public deposits without permission.'),
        C('c4', T4, [
            'Ind AS applies to NBFCs in phases based on net worth and listing; their statements follow Division III of Schedule III, which differs from Division II (e.g. liquidity-based order — financial assets first; specific line items for loans, investments, derivatives).',
            'Related party exposure disclosures and other RBI-prescribed disclosures accompany Ind AS statements.',
            'Auditors check Ind AS 109 classification, ECL models, fair values and Division III presentation.'],
          'NBFC statements follow Division III with financial items first.',
          'An NBFC\'s balance sheet starts with cash and loans, not PPE.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Statutory audit of a middle-layer NBFC', 'role': 'Audit senior',
             'situation': 'A ₹3,000 crore vehicle finance NBFC on Ind AS.',
             'steps': ['Check registration, layer and capital compliance.', 'Test loan classification against the 90-day norm.', 'Review ECL model and prudential floor.', 'Report under RBI directions and CARO.'],
             'takeaway': 'Prudential compliance is as important as the financial statements.'}]

    mcqs = [
        Q('m1', 'The principal business test for NBFCs uses the threshold:', ['Fifty percent of assets and fifty percent of income', 'Thirty percent', 'Seventy-five percent', 'Ten percent'], 0,
          'Both conditions. In practice: 50-50 test.', 'c1', T1),
        Q('m2', 'NBFCs cannot:', ['Accept demand deposits', 'Lend money', 'Invest in securities', 'Borrow from banks'], 0,
          'Key difference from banks. In practice: no cheque facility.', 'c1', T1),
        Q('m3', 'RBI\'s scale-based regulation divides NBFCs into:', ['Base, middle, upper and top layers', 'Small and large', 'Listed and unlisted', 'Deposit and non-deposit only'], 0,
          'Four layers. In practice: top expected empty.', 'c1', T1),
        Q('m4', 'Under the glide path, NBFCs adopt the 90-day NPA norm by:', ['31 March 2026', '31 March 2024', '31 March 2030', 'Immediately in 2020'], 0,
          'Staged from 180 days. In practice: check NBFC category.', 'c2', T2),
        Q('m5', 'Income on NPAs of NBFCs is recognised:', ['On realisation', 'On accrual', 'Never', 'Monthly'], 0,
          'Prudential norm. In practice: reverse unrealised.', 'c2', T2),
        Q('m6', 'Ind AS NBFCs present statements under:', ['Division III of Schedule III', 'Division I', 'Division II', 'Third Schedule of BR Act'], 0,
          'NBFC format. In practice: liquidity order.', 'c4', T4),
        Q('m7', 'NBFC auditors report specific matters to RBI under:', ['NBFC Auditor\'s Report Directions', 'SA 810', 'SEBI LODR', 'Income-tax Act'], 0,
          'RBI directions. In practice: separate report.', 'c3', T3),
        Q('m8', 'Minimum NOF for most NBFCs after the phase-in is:', ['Ten crore rupees', 'Two crore rupees', 'One crore rupees', 'Twenty-five lakh rupees'], 0,
          'Raised from ₹2 crore with exceptions. In practice: check timeline.', 'c1', T1),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'NPA', 2.5, 'computation', 'npa', nums=[days_ok]), S('s2', 'NOF', 2.5, 'computation', 'nof|owned', nums=[nof])],
          ['Apply the glide path.'], ['Using the old 180-day rule.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'First company', 2, 'concept', 'registration'), S('s2', 'Second company', 2, 'concept', 'not')],
          ['Apply both tests.'], ['Using only income test.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is the principal business test?', 'Financial assets above half of total assets and financial income above half of gross income.',
          [P('p1', 'Assets', 5, 'assets'), P('p2', 'Income', 5, 'income')], 'c1'),
        V('v2', 'Name the layers under scale-based regulation.', 'Base layer, middle layer, upper layer and top layer.',
          [P('p1', 'Base and middle', 5, 'base|middle'), P('p2', 'Upper and top', 5, 'upper|top')], 'c1'),
        V('v3', 'Describe the NPA glide path for NBFCs.', 'From 180 days to 150 days by March 2024, 120 days by March 2025 and 90 days by March 2026.',
          [P('p1', '180 to 90', 5, '180|90'), P('p2', 'By March 2026', 5, '2026')], 'c2'),
        V('v4', 'What does the NBFC auditor report to RBI?', 'Matters like registration, net owned fund, compliance with prudential norms and acceptance of public deposits.',
          [P('p1', 'Registration and NOF', 5, 'registration|owned'), P('p2', 'Prudential and deposits', 5, 'prudential|deposit')], 'c3'),
        V('v5', 'How does Division III differ from Division II?', 'It presents items in order of liquidity with financial assets first and NBFC-specific line items.',
          [P('p1', 'Liquidity order', 5, 'liquidity'), P('p2', 'Financial assets first', 5, 'financial assets')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'LendEasy P2P Ltd.', 'difficulty': 'moderate',
              'case': 'LendEasy is a peer-to-peer lending NBFC in the base layer. It accepted ₹2 crore from the public as deposits to fund loans. Several borrower loans were overdue 100 days at 31 March 2026. It prepares Ind AS statements.',
              'mcqs': [
                  M('k1a', 'Accepting public deposits without RBI permission must be:', ['Reported by the auditor to RBI', 'Ignored', 'Disclosed only in notes', 'Approved by the board'], 0,
                    'RBI directions. In practice: serious breach.', 'core', topic=T3),
                  M('k1b', 'Loans overdue 100 days at 31 March 2026 are:', ['NPAs under the 90-day norm', 'Standard', 'Special mention', 'Written off'], 0,
                    'Glide path reached 90 days. In practice: reverse income.', 'core', topic=T2),
                  M('k1c', 'LendEasy\'s statements follow:', ['Division III of Schedule III', 'Division II', 'Third Schedule of BR Act', 'Division I'], 0,
                    'Ind AS NBFC format. In practice: ECL.', 'core', topic=T4),
                  M('k1d', 'P2P NBFCs fall in which layer?', ['Base layer', 'Upper layer', 'Top layer', 'Middle layer'], 0,
                    'As per scale-based regulation. In practice: lighter norms.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch14', 2, 'Special Features of Audit of Non-Banking Financial Companies (NBFCs)',
                ['Explain NBFCs, registration and scale-based regulation.',
                 'Apply prudential norms on capital, income recognition and provisioning.',
                 'Perform audit procedures and report to RBI and under CARO.',
                 'Apply Ind AS and Division III presentation.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 20}, 'prereq': ['fin-p3-ch14-u01'],
                 'exam_tip': 'Quote the 90-day glide path date and the scale-based layer in NBFC cases.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['50-50 principal business test.',
                             'NOF moving from ₹2 crore to ₹10 crore.',
                             'Layers: base, middle, upper, top.',
                             'NPA norm 90 days by March 2026.',
                             'RBI auditor report directions; Division III.'],
                 'remember': ['NBFCs cannot take demand deposits.'],
                 'traps': ['Applying the old 180-day norm after March 2026.']},
                [('Principal business', '50% assets + 50% income'), ('NOF', '₹10 crore (phased)'), ('NPA', '> 90 days by 2026'), ('Format', 'Division III')],
                viva, cases)
