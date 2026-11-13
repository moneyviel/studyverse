"""CA Intermediate · Paper 2 Corporate and Other Laws · Chapter 9 Accounts of Companies (ss. 128–138).
Scope follows the ICAI study material (with amendments to June 2026); provisions are explained in original words; examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p2-ch09-u01'
T1 = 'Books of account (s. 128)'
T2 = 'Financial statements, consolidation, re-opening and revision (ss. 129–133)'
T3 = 'Approval, Board\'s report, circulation and filing (ss. 134–137)'
T4 = 'Corporate social responsibility (s. 135)'
T5 = 'Internal audit (s. 138)'


def build():
    ck = Checks()
    avg = ck.add('(9+6+12)/3', 'Average net profit of three preceding years (₹ crore)')
    csr = ck.add('9*2/100', 'Minimum CSR spend: 2% of average (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Is CSR applicable, and how much?', 'difficulty': 'core', 'minutes': 7,
          'q': 'Sanjeevani Ltd. had net worth ₹420 crore, turnover ₹850 crore and net profit ₹12 crore in the immediately preceding financial year. Net profits of the last three years were ₹9 crore, ₹6 crore and ₹12 crore. Is CSR applicable and what is the minimum spend? Is a CSR Committee required?',
          'solution': [table(['Test', 'Working', 'Result'], [
              ['Applicability', 'Net profit ₹12 crore ≥ ₹5 crore (one test is enough)', 'Applicable'],
              ['Average net profit', '(9 + 6 + 12) ÷ 3', f'₹{R(avg)} crore'],
              ['Minimum CSR spend', '2% of ₹9 crore', f'₹{R(csr)} crore'],
              ['CSR Committee', 'Spend exceeds ₹50 lakh', 'Required']], title='Section 135')],
          'checks': list(ck)}

    ck2 = Checks()
    q = ck2.add('3', 'Years of revision allowed backwards under section 131')
    i2 = {'id': 'i2', 'title': 'Signing and revising accounts', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'The financial statements of Nakshatra Ltd. (which has a managing director and a CFO and a company secretary) were signed only by two non-executive directors. Later the Board discovers that the statements for two years ago did not comply with section 129. Advise on both points.',
          'solution': [legal('Sections 134 and 131',
                             'Signature by two non-executive directors; non-compliant statements of an earlier year.',
                             'Financial statements are approved by the Board and signed by the chairperson where authorised, or by two directors of whom one is the managing director (if any), and by the CEO (if a director, in that capacity), the CFO and the company secretary where appointed. Under section 131, directors may prepare revised statements for any of the three preceding years if they appear not to comply with section 129 or 134, with the Tribunal\'s approval; revision may be done only once in a financial year.',
                             f'The signing is defective — the MD, CFO and CS must also sign. The company may revise the statements of two years ago (within the {R(q)}-year window) after Tribunal approval.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Section 128: every company keeps books of account and other papers at its registered office giving a true and fair view of its state of affairs, including branches, on accrual basis and by double entry. The Board may decide another place in India, informing the Registrar within seven days.',
            'Books may be kept in electronic form, accessible in India at all times, with a back-up on servers in India.',
            'Branch summaries are sent periodically to the registered office. Books and vouchers are preserved for at least eight years (longer if the Central Government orders during an investigation).',
            'Directors may inspect the books during business hours; the managing director, whole-time director in charge of finance, CFO and others charged with this duty are responsible for compliance.'],
          'Proper books, kept at the right place, for long enough.',
          'A company moving its accounts office to another city must tell the Registrar within seven days.'),
        C('c2', T2, [
            'Section 129: financial statements give a true and fair view, comply with notified accounting standards, and are in the form in Schedule III. A company with subsidiaries, associates or joint ventures also prepares consolidated financial statements and attaches a statement of their salient features in e-Form AOC-1.',
            'Section 130: accounts cannot be reopened or recast unless the Tribunal so orders on application by the Central Government, Income-tax authorities, SEBI or other regulators, because earlier accounts were prepared fraudulently or the company\'s affairs were mismanaged. Re-opening is limited to eight years.',
            'Section 131: directors may voluntarily revise financial statements or the Board\'s report of any of the three preceding years, with Tribunal approval, if they appear not to comply with sections 129 or 134. Revision is allowed once in a financial year, with reasons disclosed.',
            'Section 132 establishes the National Financial Reporting Authority (NFRA) to recommend accounting and auditing standards and monitor compliance; section 133 empowers the Central Government to prescribe accounting standards.'],
          'True and fair statements in the prescribed form; reopening is rare and controlled.',
          'A listed company with two subsidiaries presents both standalone and consolidated statements.'),
        C('c3', T3, [
            'Section 134: statements are approved by the Board before audit and signed by the chairperson where authorised, or by two directors including the MD where there is one, and by the CEO, CFO and company secretary where appointed. The auditor\'s report is attached.',
            'The Board\'s report covers matters such as the web link of the annual return, number of Board meetings, the directors\' responsibility statement, independence declarations, policies on remuneration, explanations on auditors\' qualifications, loans and investments, related party contracts (e-Form AOC-2), state of affairs, material changes after year end, energy conservation and foreign exchange, risk management, CSR, and details of sexual harassment complaints and compliance with the Maternity Benefit Act.',
            'Section 136: copies of financial statements are sent to every member, debenture trustee and others entitled at least 21 days before the AGM (shorter with consent of 95% of members entitled to vote) and placed on the website of listed companies.',
            'Section 137: copies of adopted financial statements are filed with the Registrar within 30 days of the AGM (unadopted copies if the AGM did not adopt them, then adopted ones within 30 days of the adjourned meeting); an OPC files within 180 days of year end.'],
          'Board approval, full signatures, members\' copies and Registrar filing complete the cycle.',
          'Financial statements adopted at an AGM on 25 September must be filed by 25 October.'),
        C('c4', T4, [
            'Section 135: a company with net worth of ₹500 crore or more, turnover of ₹1,000 crore or more, or net profit of ₹5 crore or more during the immediately preceding financial year must comply with CSR provisions.',
            'It constitutes a CSR Committee of three or more directors, at least one independent (an unlisted or private company without independent directors may have two directors). If the CSR obligation does not exceed ₹50 lakh, the Board discharges the committee\'s functions.',
            'The Board ensures spending of at least 2% of average net profits of the three immediately preceding financial years on activities in Schedule VII, giving preference to local areas. Excess spending may be set off over the next three years.',
            'Unspent amounts not related to ongoing projects go to a Schedule VII fund within six months of year end; amounts for ongoing projects go to an Unspent CSR Account within 30 days of year end and are spent within three financial years. From 2026, up to 10% of CSR spending may be through zero coupon zero principal instruments on a Social Stock Exchange.'],
          'Large or profitable companies must spend 2% of average profits on specified social causes.',
          'A company with turnover of ₹1,200 crore but a loss is still covered by the turnover test.'),
        C('c5', T5, [
            'Section 138 and the rules require internal audit by: every listed company; every unlisted public company with paid-up capital of ₹50 crore or more, turnover of ₹200 crore or more, outstanding loans or borrowings over ₹100 crore, or deposits of ₹25 crore or more; and every private company with turnover of ₹200 crore or more or outstanding borrowings over ₹100 crore.',
            'The internal auditor may be a chartered accountant or cost accountant (whether or not in practice) or another professional decided by the Board, and may be an employee.',
            'The Audit Committee or the Board, in consultation with the internal auditor, formulates the scope, functioning, periodicity and methodology of internal audit.'],
          'Bigger companies must have an internal auditor reporting to the Board or Audit Committee.',
          'A private company with ₹250 crore turnover needs an internal auditor.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Annual accounts compliance', 'role': 'Secretarial associate',
             'situation': 'An unlisted public company with turnover of ₹1,100 crore is finalising its accounts and Board\'s report.',
             'steps': ['Check signatures required under section 134.', 'Compute the CSR obligation and spending status.', 'Confirm internal audit applicability.', 'Send copies 21 days before AGM and file within 30 days after.'],
             'takeaway': 'Compliance runs from books to filing in a fixed sequence.'}]

    mcqs = [
        Q('m1', 'Books of account must be preserved for at least:', ['8 years', '5 years', '10 years', '6 years'], 0,
          'Section 128(5) requires books of account and vouchers for at least eight financial years immediately preceding the current year. The Central Government may order longer preservation during an investigation. In practice: keep electronic back-ups in India.', 'c1', T1, 'core', check=8),
        Q('m2', 'If the Board decides to keep books at a place other than the registered office, the Registrar must be informed within:', ['Seven days', 'Thirty days', 'Fifteen days', 'Sixty days'], 0,
          'Section 128(1) allows the Board to decide another place in India for keeping books, with written intimation to the Registrar within seven days of the decision. In practice: file the prescribed form.', 'c1', T1),
        Q('m3', 'The salient features of subsidiaries\' financial statements are attached in:', ['e-Form AOC-1', 'e-Form AOC-2', 'MGT-7', 'ADT-1'], 0,
          'Section 129(3) and rule 5 require a statement of salient features of subsidiaries, associates and joint ventures in e-Form AOC-1 with the financial statements. AOC-2 is for related party contracts. In practice: attach to both sets.', 'c2', T2),
        Q('m4', 'Voluntary revision of financial statements under section 131 is allowed for:', ['Any of the three preceding financial years, with Tribunal approval', 'Any year without approval', 'Only the current year', 'Eight preceding years'], 0,
          'Directors may revise statements or the Board\'s report of any of the three preceding years if they appear not to comply with sections 129 or 134, after Tribunal approval; only once in a financial year. In practice: disclose reasons.', 'c2', T2),
        Q('m5', 'Copies of financial statements must be sent to members at least:', ['21 days before the AGM', '14 days', '30 days', '7 days'], 0,
          'Section 136 requires copies to be sent at least twenty-one days before the meeting; shorter period is allowed with the consent of at least 95% of members entitled to vote. In practice: e-mail is permitted.', 'c3', T3, 'core', check=21),
        Q('m6', 'Adopted financial statements are filed with the Registrar within:', ['30 days of the AGM', '60 days of the AGM', '180 days of year end', '15 days'], 0,
          'Section 137 requires filing within thirty days of the AGM; one person companies file within 180 days of the close of the year. In practice: use AOC-4 forms with required extracts.', 'c3', T3, 'core', check=30),
        Q('m7', 'CSR applies if, in the immediately preceding financial year, net profit is at least:', ['₹5 crore', '₹10 crore', '₹1 crore', '₹50 crore'], 0,
          'Section 135 applies where net worth is ₹500 crore or more, turnover ₹1,000 crore or more, or net profit ₹5 crore or more in the immediately preceding financial year. Any one test is enough. In practice: check all three.', 'c4', T4, 'core', check=5),
        Q('m8', 'The minimum CSR spend is 2% of:', ['Average net profits of the three immediately preceding financial years', 'Current year turnover', 'Current year net profit', 'Net worth'], 0,
          'The Board ensures spending of at least 2% of average net profits made during the three immediately preceding years (or fewer years for newer companies). In practice: compute net profit as per section 198.', 'c4', T4),
        Q('m9', 'A CSR Committee is not required when the CSR obligation does not exceed:', ['₹50 lakh', '₹1 crore', '₹25 lakh', '₹5 crore'], 0,
          'Where the amount to be spent does not exceed fifty lakh rupees, the Board itself performs the CSR Committee\'s functions under section 135(9). In practice: record decisions in Board minutes.', 'c4', T4, 'core', check=50),
        Q('m10', 'A private company must appoint an internal auditor if its turnover in the preceding year is at least:', ['₹200 crore', '₹100 crore', '₹50 crore', '₹500 crore'], 0,
          'Private companies with turnover of ₹200 crore or more, or outstanding borrowings above ₹100 crore, must have an internal auditor under section 138 and the rules. In practice: check both limits.', 'c5', T5, 'core', check=200),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Applicability test', 1, 'concept', '5 crore|net profit'),
           S('s2', 'Average and 2%', 2, 'computation', 'average', nums=[avg, csr]),
           S('s3', 'Committee', 1, 'concept', '50 lakh|committee')],
          ['Use three preceding years.'], ['Using current year profit.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Signing requirement', 2.5, 'application', 'managing director|cfo'),
           S('s2', 'Voluntary revision', 2.5, 'application', 'tribunal', 'three')],
          ['Address both issues.'], ['Thinking revision needs no approval.'], ['Provision → facts → analysis → conclusion.'], checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Where must books of account be kept?', 'At the registered office, or another place in India decided by the Board with intimation to the Registrar within seven days; electronic form is allowed.',
          [P('p1', 'Registered office', 5, 'registered office'), P('p2', 'Other place with intimation', 5, 'seven|intimat|registrar')], 'c1'),
        V('v2', 'Who signs the financial statements?', 'The chairperson if authorised, or two directors including the managing director, and the CEO, CFO and company secretary where appointed.',
          [P('p1', 'Directors and MD', 5, 'director'), P('p2', 'CFO and CS', 5, 'cfo|secretary')], 'c3'),
        V('v3', 'When can accounts be re-opened under section 130?', 'Only on a Tribunal order on application by the Central Government, tax authorities, SEBI or other regulators, where accounts were fraudulently prepared or affairs mismanaged, within eight years.',
          [P('p1', 'Tribunal order', 5, 'tribunal'), P('p2', 'Fraud or mismanagement', 5, 'fraud|mismanag')], 'c2'),
        V('v4', 'State the CSR thresholds.', 'Net worth of ₹500 crore, turnover of ₹1,000 crore, or net profit of ₹5 crore in the immediately preceding financial year.',
          [P('p1', 'Net worth and turnover', 5, 'net worth', 'turnover'), P('p2', 'Net profit ₹5 crore', 5, '5 crore')], 'c4'),
        V('v5', 'Who decides the scope of internal audit?', 'The Audit Committee, or the Board where there is none, in consultation with the internal auditor.',
          [P('p1', 'Audit Committee or Board', 6, 'audit committee|board'), P('p2', 'With internal auditor', 4, 'internal auditor')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Pragya Ltd.', 'difficulty': 'moderate',
              'case': 'Pragya Ltd. (unlisted public) had paid-up capital of ₹60 crore and turnover of ₹180 crore last year. Its CSR obligation for the year was ₹80 lakh, of which ₹30 lakh remained unspent at year end on an ongoing project. Its AGM was held on 28 September.',
              'mcqs': [
                  M('k1a', 'Is internal audit mandatory?', ['Yes, because paid-up capital is at least ₹50 crore', 'No, turnover is below ₹200 crore', 'Only if listed', 'Only if CSR applies'], 0,
                    'For unlisted public companies, any one threshold suffices: paid-up capital of ₹50 crore or more triggers internal audit regardless of turnover. In practice: appoint by Board resolution.', 'moderate', topic=T5),
                  M('k1b', 'The unspent ₹30 lakh for the ongoing project must be:', ['Transferred to an Unspent CSR Account within 30 days of year end', 'Transferred to a Schedule VII fund within six months', 'Carried forward without action', 'Spent within 30 days'], 0,
                    'Unspent amounts relating to ongoing projects go to the Unspent CSR Account within thirty days and are spent within three financial years; other unspent amounts go to a Schedule VII fund within six months. In practice: disclose in the Board\'s report.', 'moderate', topic=T4),
                  M('k1c', 'Last date for filing adopted financial statements:', ['By 28 October', 'By 28 November', 'By 27 March', 'On 28 September itself'], 0,
                    'Section 137 requires filing within thirty days of the AGM; from 28 September this is 28 October. In practice: file AOC-4 with board report and auditor extracts.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p2', 'int-p2-ch09', 1, 'Accounts of Companies',
                ['Apply the rules on books of account.',
                 'Explain financial statements, consolidation, re-opening and voluntary revision.',
                 'Apply approval, signing, Board\'s report, circulation and filing requirements.',
                 'Apply the CSR and internal audit provisions.'],
                {'difficulty': 'core', 'minutes': {'learn': 50, 'practice': 30}, 'prereq': ['int-p2-ch08-u01'],
                 'exam_tip': 'Memorise thresholds: CSR 500/1,000/5 crore and ₹50 lakh committee exemption; internal audit 50/200/100/25 crore.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Books at registered office; other place with 7-day intimation; keep 8 years.', 'FS true and fair, AS, Schedule III; CFS + AOC-1.',
                             'Re-opening only by Tribunal order (8 years); voluntary revision 3 years, once a year.', 'Signing: chair or two directors incl. MD, CEO, CFO, CS.',
                             'Copies 21 days before AGM; filing within 30 days; OPC 180 days.', 'CSR: 2% of 3-year average; unspent rules; internal audit thresholds.'],
                 'remember': ['Board\'s report now includes sexual harassment and maternity benefit compliance details.'],
                 'traps': ['CSR uses the immediately preceding year for applicability but three years for the amount.']},
                [('CSR tests', '₹500 cr NW · ₹1,000 cr TO · ₹5 cr NP'), ('CSR spend', '2% of 3-year average'), ('Filing', '30 days of AGM'), ('Revision', '3 preceding years')],
                viva, cases)
