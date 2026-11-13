"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 15 Overview of Audit of Public Sector Undertakings.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch15-u01'
T1 = 'Framework of government audit and the C&AG'
T2 = 'Financial and compliance audit of PSUs'
T3 = 'Performance and comprehensive audit'
T4 = 'Propriety audit and C&AG reporting'


def build():
    ck = Checks()
    over = ck.add('round((145-100)/100*100,2)', 'Cost overrun (%)')
    delay = ck.add('48-30', 'Delay in completion (months)')
    i1 = {'id': 'i1', 'title': 'A performance audit finding', 'difficulty': 'core', 'minutes': 6,
          'q': 'A state PSU built a power plant budgeted at ₹100 crore and 30 months; it cost ₹145 crore and took 48 months. Compute the overrun and delay and suggest the performance audit angle.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Cost overrun', '(145 − 100) ÷ 100', inr(over) + '%'],
              ['Delay', '48 − 30', inr(delay) + ' months'],
              ['Economy', 'Were inputs bought at least cost?', '—'],
              ['Efficiency and effectiveness', 'Were resources used well and objectives achieved?', '—']], title='3Es of performance audit')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Propriety concerns', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Comment from a propriety audit angle: (a) a PSU spent heavily on a chairman\'s farewell party; (b) a contract was awarded to a relative of a director without tender; (c) a costly car was bought for an officer not entitled to it.',
          'solution': [table(['Case', 'Propriety issue'], [
              ['(a)', 'Expenditure not justified by public interest — wasteful'],
              ['(b)', 'Favouritism; violates fairness and financial rules'],
              ['(c)', 'Benefit to an individual beyond entitlement']], title='Canons of financial propriety')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'The Comptroller and Auditor General of India (C&AG), under Articles 148–151 of the Constitution and the C&AG (DPC) Act, 1971, audits receipts and expenditure of the Union and States and of bodies substantially financed by government, including government companies and corporations.',
            'For government companies, the C&AG appoints the statutory auditor (a chartered accountant firm), issues directions on the manner of audit, conducts supplementary or test audit, and comments on or supplements the auditor\'s report (section 143(5)–(7) of the Companies Act).',
            'C&AG reports are laid before Parliament or state legislatures and examined by the Public Accounts Committee and Committee on Public Undertakings.'],
          'Public money needs a public auditor — the C&AG.',
          'A statutory auditor of a PSU reports on C&AG directions under section 143(5).'),
        C('c2', T2, [
            'PSU audit elements: auditor (C&AG and appointed auditors), responsible party, intended users (legislature, public), subject matter and criteria. Principles include independence, objectivity, professional judgement, communication and quality control.',
            'Financial audit gives an opinion on whether financial statements present a true and fair view in line with the framework.',
            'Compliance audit checks whether activities, transactions and information follow authorities — laws, rules, regulations, budgets, policies and contracts — and principles of sound financial management.'],
          'Financial audit asks "are the numbers right?"; compliance audit asks "were the rules followed?".',
          'A compliance audit checks whether procurement followed tender rules.'),
        C('c3', T3, [
            'Performance audit is an independent assessment of whether government undertakings, programmes or systems operate with economy, efficiency and effectiveness (the 3Es), and whether there is room for improvement.',
            'Planning involves choosing topics on risk and significance, defining objectives and criteria, designing methods (data analysis, field visits, surveys) and reporting findings with recommendations.',
            'Comprehensive audit of PSUs appraises overall performance: achievement of targets, cost control, capital planning, idle capacity, pricing, delays and overruns, and investment returns.'],
          'Performance audit judges value for money.',
          'A plant 50% over budget and 18 months late is a classic performance audit finding.'),
        C('c4', T4, [
            'Propriety audit examines whether expenditure meets standards of financial propriety: spending no more than the occasion demands, no authority using powers to benefit itself, public money not used for any person\'s benefit unless allowed, and charges for services rendered by government recovered.',
            'It looks at wisdom, faithfulness and economy of decisions, not just legality.',
            'C&AG audit reports compile findings from financial, compliance and performance audits; they are submitted to the President or Governor and laid before the legislature for scrutiny.'],
          'Legal is not always proper — propriety audit asks if it was right to spend.',
          'Lavish spending on events by a PSU may be legal but improper.'),
    ]

    jobs = [{'id': 'j1', 'title': 'PSU statutory audit', 'role': 'Audit manager in a CA firm appointed by C&AG',
             'situation': 'A state power distribution company with large subsidy receivables.',
             'steps': ['Study C&AG directions under section 143(5).', 'Perform financial audit per SAs.', 'Answer directions and sub-directions.', 'Coordinate with C&AG on supplementary audit.'],
             'takeaway': 'PSU audits add C&AG directions to normal SA work.'}]

    mcqs = [
        Q('m1', 'The statutory auditor of a government company is appointed by:', ['The C&AG', 'Shareholders in AGM', 'The board', 'SEBI'], 0,
          'Section 139(5)/(7). In practice: CA firms empanelled.', 'c1', T1),
        Q('m2', 'Directions from C&AG to the statutory auditor are issued under:', ['Section 143(5)', 'Section 143(12)', 'Section 134', 'Section 186'], 0,
          'Auditor reports on directions. In practice: sub-directions too.', 'c1', T1),
        Q('m3', 'Performance audit examines:', ['Economy, efficiency and effectiveness', 'Only arithmetic accuracy', 'Only tax', 'Only legality'], 0,
          '3Es. In practice: value for money.', 'c3', T3),
        Q('m4', 'Compliance audit checks:', ['Adherence to laws, rules, budgets and contracts', 'Only profit', 'Only stock', 'Market price'], 0,
          'Authorities and criteria. In practice: procurement rules.', 'c2', T2),
        Q('m5', 'Propriety audit focuses on:', ['Whether spending meets standards of financial propriety', 'Only legality', 'Only valuation', 'Only revenue'], 0,
          'Wisdom and economy. In practice: canons of propriety.', 'c4', T4),
        Q('m6', 'C&AG reports are examined by:', ['Public Accounts Committee and Committee on Public Undertakings', 'SEBI', 'RBI', 'NFRA'], 0,
          'Legislative oversight. In practice: laid before legislature.', 'c4', T4),
        Q('m7', 'A comprehensive audit of a PSU appraises:', ['Overall performance including targets and costs', 'Only cash', 'Only tax returns', 'Only HR'], 0,
          'Broader than financial audit. In practice: overruns, idle capacity.', 'c3', T3),
        Q('m8', 'The constitutional articles relating to the C&AG include:', ['Articles 148 to 151', 'Articles 14 to 18', 'Articles 300 to 305', 'Article 21'], 0,
          'Constitutional authority. In practice: DPC Act 1971.', 'c1', T1),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Overrun and delay', 2, 'computation', 'overrun|delay', nums=[over, delay]), S('s2', '3Es', 2, 'concept', 'economy|efficiency|effectiveness')],
          ['Use 3Es.'], ['Only reporting numbers.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Wasteful spending', 1.5, 'concept', 'wasteful|public interest'), S('s2', 'Favouritism', 1.5, 'concept', 'favouritism|fairness'), S('s3', 'Entitlement', 1, 'concept', 'entitlement')],
          ['Cite canons.'], ['Treating legality as enough.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is the role of C&AG in government company audits?', 'Appointing the statutory auditor, issuing directions, conducting supplementary or test audit and commenting on the audit report.',
          [P('p1', 'Appoint and direct', 5, 'appoint|direction'), P('p2', 'Supplementary audit', 5, 'supplementary')], 'c1'),
        V('v2', 'Distinguish financial and compliance audit.', 'Financial audit opines on whether statements give a true and fair view; compliance audit checks adherence to laws, rules and other authorities.',
          [P('p1', 'True and fair', 5, 'fair'), P('p2', 'Adherence to rules', 5, 'laws|rules')], 'c2'),
        V('v3', 'What are the 3Es?', 'Economy, efficiency and effectiveness.',
          [P('p1', 'Economy and efficiency', 5, 'economy|efficiency'), P('p2', 'Effectiveness', 5, 'effectiveness')], 'c3'),
        V('v4', 'State a canon of financial propriety.', 'Expenditure should be no more than the occasion demands, and no authority should use its powers to benefit itself.',
          [P('p1', 'No more than occasion', 5, 'occasion'), P('p2', 'No self-benefit', 5, 'benefit')], 'c4'),
        V('v5', 'Who scrutinises C&AG reports?', 'Parliament or state legislatures through the Public Accounts Committee and the Committee on Public Undertakings.',
          [P('p1', 'Legislature', 5, 'parliament|legislature'), P('p2', 'Committees', 5, 'committee')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'State Transport Corporation', 'difficulty': 'core',
              'case': 'A state road transport corporation\'s new buses cost 20% above market rates due to a single-vendor order. 30% of the fleet is idle. A CA firm appointed by C&AG audits its accounts, and C&AG plans a performance review.',
              'mcqs': [
                  M('k1a', 'Paying 20% above market rates relates to:', ['Economy', 'Effectiveness only', 'Legality only', 'Taxation'], 0,
                    'Least-cost acquisition. In practice: tender review.', 'core', topic=T3),
                  M('k1b', '30% idle fleet indicates a problem with:', ['Efficiency of resource use', 'Accounting policy', 'Audit fees', 'Tax'], 0,
                    'Underutilisation. In practice: comprehensive audit.', 'core', topic=T3),
                  M('k1c', 'The CA firm\'s report must also address:', ['C&AG directions under section 143(5)', 'SEBI KAMs', 'RBI LFAR', 'Tax audit'], 0,
                    'Government company requirement. In practice: sub-directions.', 'core', topic=T1),
                  M('k1d', 'Single-vendor ordering without justification raises:', ['Compliance and propriety concerns', 'No concern', 'Only economy gains', 'Revenue issues'], 0,
                    'Procurement rules and fairness. In practice: report findings.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch15', 1, 'Overview of Audit of Public Sector Undertakings',
                ['Explain the government audit framework and the C&AG\'s role.',
                 'Distinguish financial and compliance audit of PSUs.',
                 'Conduct performance and comprehensive audits.',
                 'Apply propriety audit principles and understand C&AG reporting.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 15}, 'prereq': ['fin-p3-ch14-u02'],
                 'exam_tip': 'Name the audit type (financial, compliance, performance, propriety) before analysing a PSU case.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['C&AG: Articles 148–151; DPC Act 1971.',
                             'Appoints PSU auditors; directions under 143(5).',
                             'Financial vs compliance audit.',
                             'Performance audit: 3Es; comprehensive audit.',
                             'Propriety audit canons; PAC and COPU.'],
                 'remember': ['Legal spending can still be improper.'],
                 'traps': ['Thinking shareholders appoint PSU auditors.']},
                [('C&AG', 'Arts 148–151'), ('143(5)', 'Directions'), ('3Es', 'Economy, efficiency, effectiveness'), ('Propriety', 'Wisdom of spending')],
                viva, cases)
