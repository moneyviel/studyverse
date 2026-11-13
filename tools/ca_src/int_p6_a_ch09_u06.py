"""CA Intermediate · Paper 6A Financial Management · Chapter 9 Unit 6 Financing of Working Capital.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch09-u06'
T1 = 'Sources of working capital finance'
T2 = 'Money market instruments: commercial paper, bills, ICDs'
T3 = 'Bank finance for working capital'


def build():
    ck = Checks()
    cp = ck.add('(100-97.5)/97.5*365/90*100', 'Effective annual cost of CP (%)')
    tot = ck.add('10.40+0.5', 'Cost including 0.5% issue expenses (approx.)')
    i1 = {'id': 'i1', 'title': 'Cost of commercial paper', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'A highly rated company issues 90-day commercial paper of face value ₹100 at ₹97.50. Issue and rating costs add about 0.5% a year. Compute the effective annual cost and compare with a 12% cash credit.',
          'solution': [table(['Item', 'Working', 'Answer'], [
              ['Discount yield', '2.50 ÷ 97.50 × 365 ÷ 90', str(round(cp, 2)) + '%'],
              ['Add issue costs', '+0.5%', str(round(tot, 2)) + '%']], title='Commercial paper'),
              p('At about 10.9%, CP is cheaper than the 12% cash credit, so the company should use CP for part of its seasonal needs, keeping bank lines as back-up.')],
          'checks': list(ck)}

    ck2 = Checks()
    m2 = ck2.add('0.75*400 - 120', 'Method II: 75% of current assets − current liabilities (other than bank)')
    m1 = ck2.add('0.75*(400-120)', 'Method I: 75% of (current assets − current liabilities)')
    i2 = {'id': 'i2', 'title': 'How much will the bank lend?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A borrower\'s projected current assets are ₹400 lakh and current liabilities other than bank borrowings ₹120 lakh. Using the Tandon Committee methods (now historical, as RBI lets banks set their own methods), compute maximum permissible bank finance under Method I and Method II.',
          'solution': [table(['Method', 'Working', '₹ lakh'], [
              ['Method I', '75% of working capital gap (400 − 120)', inr(m1)],
              ['Method II', '75% of current assets − other current liabilities', inr(m2)]], title='MPBF (Tandon)'),
              note('Method II requires the borrower to fund 25% of total current assets from long-term sources, giving a lower bank limit.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Spontaneous sources: trade credit and accrued expenses (wages, taxes) that rise with activity.',
            'Short-term sources: bank cash credit and overdraft, working capital demand loans, bill discounting, commercial paper, inter-corporate deposits, factoring, advances from customers, and public deposits (subject to law).',
            'Long-term sources (for permanent working capital): equity, retained earnings, long-term loans and debentures. The mix follows the firm\'s financing approach (matching, conservative or aggressive).'],
          'Use spontaneous credit first, short-term finance for swings and long-term funds for the base.',
          'Advance payments from customers fund a builder\'s construction working capital.'),
        C('c2', T2, [
            'Commercial paper: an unsecured promissory note issued at a discount by highly rated companies; maturity from 7 days to less than one year; issued in denominations of ₹5 lakh or multiples; cheaper than bank credit for strong borrowers and repayable by rolling over.',
            'Bill discounting: a bank pays the drawer the present value of a trade bill before maturity; cost is the discount charged. Inter-corporate deposits: short-term loans between companies, quick but costlier and riskier.',
            'Certificates of deposit are issued by banks; treasury bills by the Government — these are investment rather than borrowing options for companies.'],
          'The money market lets strong companies borrow directly from investors for short periods.',
          'A company with a top short-term rating raises ₹50 crore through 90-day CP below its bank rate.'),
        C('c3', T3, [
            'Forms of bank finance: cash credit (borrow up to a limit against hypothecated stock and debtors, interest on amount used); overdraft; working capital demand loan; bills purchased or discounted; letters of credit and bank guarantees (non-fund-based).',
            'Assessment: the Tandon Committee introduced maximum permissible bank finance (MPBF) with three methods, and the Chore Committee suggested separating limits into loan and cash credit components. RBI withdrew MPBF in 1997; banks now use Board-approved methods such as the projected balance sheet method, turnover method (for smaller borrowers) and cash budget method.',
            'Banks require a margin (borrower\'s contribution), security, periodic stock statements and drawing power checks.'],
          'Banks fund the gap between current assets and spontaneous credit, after the borrower puts in a margin.',
          'A cash credit limit of ₹5 crore with drawing power of ₹4 crore lets the borrower draw only ₹4 crore.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Funding plan for peak season', 'role': 'Finance analyst trainee',
             'situation': 'A company needs ₹20 crore extra for three months each year.',
             'steps': ['Estimate the size and timing of the peak need.', 'Compare cost of CP, cash credit and bill discounting.', 'Check credit rating and bank limits.', 'Recommend a mix with back-up lines.'],
             'takeaway': 'Cheapest is not enough — keep a reliable back-up for rollover risk.'}]

    mcqs = [
        Q('m1', 'Commercial paper maturity ranges from:', ['7 days to less than one year', '1 day to 30 days', '1 to 3 years', '90 days to 5 years'], 0,
          'CP is a short-term money market instrument within these limits. In practice: commonly 90 days.', 'c2', T2),
        Q('m2', 'CP is issued:', ['At a discount to face value', 'At a premium', 'With monthly coupons', 'Only by banks'], 0,
          'Investors pay less than face value and receive the face value at maturity. In practice: discount reflects the yield.', 'c2', T2),
        Q('m3', 'In a cash credit, interest is charged on:', ['Amount actually used', 'Full sanctioned limit', 'Drawing power', 'Security value'], 0,
          'The borrower pays interest only on the outstanding balance. In practice: a commitment charge may apply on unused limits.', 'c3', T3),
        Q('m4', 'Which is a spontaneous source of working capital?', ['Trade credit', 'Commercial paper', 'Debentures', 'Term loan'], 0,
          'Trade credit grows naturally with purchases. In practice: accrued wages are another example.', 'c1', T1),
        Q('m5', 'RBI withdrew the MPBF prescription in:', ['1997', '1975', '2010', '1991'], 0,
          'Banks have since used Board-approved methods. In practice: Tandon methods remain useful concepts.', 'c3', T3, check=1997),
        Q('m6', 'CA ₹200 lakh; other CL ₹60 lakh. MPBF under Tandon Method II:', ['₹90 lakh', '₹105 lakh', '₹140 lakh', '₹150 lakh'], 0,
          '75% × 200 − 60 = 150 − 60 = 90. In practice: Method I gives 105.', 'c3', T3, 'moderate', check=90),
        Q('m7', 'A bank guarantee is an example of:', ['Non-fund-based facility', 'Fund-based facility', 'Equity finance', 'Trade credit'], 0,
          'No funds are disbursed unless the guarantee is invoked. In practice: letters of credit are similar.', 'c3', T3),
        Q('m8', 'Inter-corporate deposits are:', ['Short-term loans between companies', 'Bank deposits by individuals', 'Long-term bonds', 'Government securities'], 0,
          'ICDs are quick but often costlier. In practice: subject to Companies Act limits on loans.', 'c2', T2),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Yield', 2, 'computation', 'yield', nums=[cp]), S('s2', 'Total cost', 1, 'computation', 'issue', nums=[tot]), S('s3', 'Comparison', 1, 'concept', 'cheaper|cash credit')],
          ['Annualise correctly.'], ['Dividing by face value instead of issue price.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Method I', 2, 'computation', 'method i', nums=[m1]), S('s2', 'Method II', 2, 'computation', 'method ii', nums=[m2])],
          ['State the margin in each.'], ['Mixing up the two methods.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is commercial paper?', 'An unsecured short-term promissory note issued at a discount by highly rated companies to raise funds from investors.',
          [P('p1', 'Unsecured note', 5, 'unsecured|promissory'), P('p2', 'Discount', 5, 'discount')], 'c2'),
        V('v2', 'Name two spontaneous sources.', 'Trade credit from suppliers and accrued expenses such as outstanding wages and taxes.',
          [P('p1', 'Trade credit', 5, 'trade credit'), P('p2', 'Accruals', 5, 'accrued|outstanding')], 'c1'),
        V('v3', 'What is a cash credit?', 'A bank facility allowing borrowing up to a limit against hypothecation of stock and receivables, with interest only on the amount used.',
          [P('p1', 'Limit against security', 5, 'limit|hypothecat'), P('p2', 'Interest on use', 5, 'interest')], 'c3'),
        V('v4', 'What did the Tandon Committee recommend?', 'Norms for inventory and receivables and the concept of maximum permissible bank finance with three methods requiring rising borrower contribution.',
          [P('p1', 'MPBF', 5, 'permissible|mpbf'), P('p2', 'Methods', 5, 'method|contribution')], 'c3'),
        V('v5', 'How do banks assess working capital today?', 'Using Board-approved methods such as the projected balance sheet, turnover or cash budget method, within RBI prudential norms.',
          [P('p1', 'Board-approved', 5, 'board'), P('p2', 'Methods', 5, 'turnover|projected|cash budget')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Vertex Chemicals', 'difficulty': 'moderate',
              'case': 'Vertex Chemicals (top short-term rating) has projected current assets of ₹300 crore and other current liabilities of ₹90 crore. Its bank charges 11.5% on cash credit. It can issue 180-day CP at ₹95 per ₹100 face value.',
              'mcqs': [
                  M('k1a', 'Working capital gap (₹ crore):', ['210', '300', '90', '225'], 0,
                    'Current assets 300 − other current liabilities 90 = 210. In practice: bank and own funds fill this gap.', 'core', check=210, topic=T3),
                  M('k1b', 'MPBF under Tandon Method II (₹ crore):', ['135', '157.5', '210', '225'], 0,
                    '75% × 300 − 90 = 135. In practice: Method I would give 157.5.', 'moderate', check=135, topic=T3),
                  M('k1c', 'Annualised cost of the CP:', ['10.67%', '5.26%', '11.50%', '10.00%'], 0,
                    '5 ÷ 95 × 365 ÷ 180 = 10.67%. In practice: add issue costs before comparing.', 'moderate', check=10.67, topic=T2),
                  M('k1d', 'Best course for seasonal needs:', ['Use CP for part, keep cash credit as back-up', 'Use only ICDs', 'Issue equity', 'Avoid short-term finance'], 0,
                    'CP is cheaper but carries rollover risk; a bank line provides back-up. In practice: watch market conditions.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch09', 6, 'Financing of Working Capital',
                ['Identify spontaneous, short-term and long-term sources of working capital.',
                 'Evaluate commercial paper, bill discounting and ICDs.',
                 'Explain forms and assessment of bank working capital finance.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 25}, 'prereq': ['int-p6-a-ch09-u05'],
                 'exam_tip': 'Annualise every short-term cost before comparing sources.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Spontaneous: trade credit, accruals.',
                             'Short-term: CC, OD, WCDL, bills, CP, ICDs, factoring.',
                             'CP: 7 days to < 1 year; ₹5 lakh multiples; issued at discount.',
                             'Tandon MPBF (historical); banks now use own methods.'],
                 'remember': ['CP cost = discount ÷ issue price × 365 ÷ days.'],
                 'traps': ['MPBF is no longer prescribed by RBI.']},
                [('CP maturity', '7 days to < 1 year'), ('Method I', '75% of (CA − CL)'), ('Method II', '75% CA − CL')],
                viva, cases)
