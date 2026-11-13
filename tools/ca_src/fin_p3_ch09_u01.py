"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 9 Related Services.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch09-u01'
T1 = 'Agreed-upon procedures (SRS 4400)'
T2 = 'Compilation engagements (SRS 4410)'
T3 = 'Comparing audits, reviews and related services'
T4 = 'Reports and practical issues in related services'


def build():
    ck = Checks()
    diff = ck.add('48.6-45', 'Difference found between invoices and claim (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Reporting factual findings', 'difficulty': 'core', 'minutes': 6,
          'q': 'A franchisor asks the auditor to perform agreed procedures on a franchisee\'s royalty claim: total sales invoices for the quarter, compare with the sales reported in the royalty statement (₹45 lakh), and recompute royalty at 5%. The invoices total ₹48.6 lakh. What does the report contain?',
          'solution': [table(['Element', 'Content'], [
              ['Procedures', 'List each agreed procedure'],
              ['Findings', 'Invoices total ₹48.6 lakh vs reported ₹45 lakh — difference ₹' + inr(diff) + ' lakh; royalty underpaid accordingly'],
              ['Assurance', 'No assurance expressed; users draw their own conclusions'],
              ['Use', 'Restricted to parties who agreed to the procedures']], title='SRS 4400 report')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Compilation with known errors', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'During a compilation for Nova Traders, the accountant notices that depreciation has not been charged and opening balances seem wrong. Management refuses to correct them. What should the accountant do?',
          'solution': [table(['Step', 'Action'], [
              ['Inform', 'Bring the matters to management\'s attention and propose corrections'],
              ['If not corrected', 'Consider withdrawing from the engagement; otherwise ensure the statements are not misleading'],
              ['Verification', 'No duty to verify all balances — but do not ignore known errors'],
              ['Report', 'States that no audit or review was performed and no assurance is given']], title='SRS 4410')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'In an agreed-upon procedures engagement, the practitioner carries out audit-type procedures agreed with the entity and any appropriate third parties, and reports factual findings. It is a non-assurance engagement: users assess the procedures and findings themselves.',
            'Terms agreed include nature, purpose, procedures, identified users, use restrictions and report form. Independence is not normally required by the standard unless the terms or law require it; if not independent, this is stated.',
            'The report lists the procedures, findings (including errors and exceptions), states that no audit or review was done and no assurance given, and restricts use to the agreed parties.'],
          'Do exactly what was agreed and report what you found — no opinion.',
          'A lender may ask for agreed procedures on a borrower\'s stock statements.'),
        C('c2', T2, [
            'In a compilation engagement, the accountant uses accounting expertise to collect, classify and summarise financial information into statements; no assurance is expressed.',
            'The accountant needs knowledge of the business and the framework, reads the compiled information for obvious misstatements, and obtains management\'s acknowledgement of responsibility.',
            'If information is incorrect, incomplete or misleading, the accountant asks management for revised information; if refused, considers withdrawing. The report states that the work was a compilation, that no audit or review was performed, and that management is responsible.'],
          'Compile, read for obvious errors, and say clearly no assurance is given.',
          'A small firm hires an accountant to prepare its year-end statements.'),
        C('c3', T3, [
            'Audits give reasonable assurance (positive opinion); reviews give limited assurance (negative conclusion); agreed-upon procedures and compilations give no assurance.',
            'Related services rely on agreed scope and management-provided information; their usefulness depends on users understanding the limits.',
            'Choosing the right engagement depends on user needs, cost and the level of comfort required.'],
          'Assurance falls from reasonable to limited to none.',
          'A bank needing comfort on stock may accept AUP findings rather than a full audit.'),
        C('c4', T4, [
            'Engagement letters for related services must spell out that no assurance is expressed and that the engagement cannot be relied on to detect errors, fraud or illegal acts.',
            'Ethical requirements still apply (integrity, objectivity, competence, confidentiality, professional behaviour) even when independence is not required.',
            'Reports should avoid wording that implies assurance, and should not be associated with misleading information.'],
          'No assurance does not mean no ethics.',
          'An accountant should refuse to compile statements known to be misleading.'),
    ]

    jobs = [{'id': 'j1', 'title': 'AUP for a lender', 'role': 'Practising CA',
             'situation': 'A bank wants factual findings on a borrower\'s receivable ageing.',
             'steps': ['Agree procedures with bank and borrower.', 'Perform procedures exactly.', 'Report findings and exceptions.', 'Restrict the report to the bank and borrower.'],
             'takeaway': 'Clear terms and factual reporting protect everyone.'}]

    mcqs = [
        Q('m1', 'An agreed-upon procedures engagement provides:', ['No assurance', 'Reasonable assurance', 'Limited assurance', 'Absolute assurance'], 0,
          'Factual findings only. In practice: users conclude.', 'c1', T1),
        Q('m2', 'An AUP report is usually restricted to:', ['Parties who agreed to the procedures', 'The public', 'All shareholders', 'Regulators only'], 0,
          'Others may misinterpret. In practice: state restriction.', 'c1', T1),
        Q('m3', 'A compilation engagement involves:', ['Collecting, classifying and summarising financial information', 'Auditing balances', 'Reviewing internal controls', 'Giving an opinion'], 0,
          'SRS 4410. In practice: no assurance.', 'c2', T2),
        Q('m4', 'If management refuses to correct misleading information in a compilation, the accountant should consider:', ['Withdrawing', 'Issuing an opinion', 'Ignoring it', 'Charging extra'], 0,
          'Avoid association. In practice: document.', 'c2', T2),
        Q('m5', 'A review engagement provides:', ['Limited assurance', 'No assurance', 'Reasonable assurance', 'Absolute assurance'], 0,
          'Negative form conclusion. In practice: SRE 2400.', 'c3', T3),
        Q('m6', 'Independence in an AUP engagement is:', ['Not normally required unless terms or law require it', 'Always required', 'Prohibited', 'Required only for banks'], 0,
          'State if not independent. In practice: check terms.', 'c1', T1),
        Q('m7', 'In related services, ethical principles:', ['Still apply', 'Do not apply', 'Apply only to audits', 'Are optional'], 0,
          'Integrity and objectivity always. In practice: Code of Ethics.', 'c4', T4),
        Q('m8', 'A compilation report states that:', ['No audit or review was performed', 'Statements are true and fair', 'Limited assurance is given', 'Controls are effective'], 0,
          'Avoid implying assurance. In practice: management responsibility noted.', 'c2', T2),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Findings', 2, 'computation', 'difference|findings', nums=[diff]), S('s2', 'No assurance', 1.5, 'concept', 'no assurance'), S('s3', 'Restriction', 1.5, 'concept', 'restricted')],
          ['List procedures.'], ['Expressing an opinion.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Inform and withdraw', 2, 'concept', 'withdraw|management'), S('s2', 'Report wording', 2, 'concept', 'no audit|no assurance')],
          ['Avoid association with misleading info.'], ['Ignoring known errors.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is the objective of an AUP engagement?', 'To perform procedures of an audit nature agreed with the entity and users and report factual findings.',
          [P('p1', 'Agreed procedures', 5, 'agreed'), P('p2', 'Factual findings', 5, 'factual')], 'c1'),
        V('v2', 'What is a compilation engagement?', 'Using accounting expertise to collect, classify and summarise financial information, where the accountant gives users zero assurance.',
          [P('p1', 'Collect and summarise', 5, 'collect|summari'), P('p2', 'Zero assurance', 5, 'zero assurance')], 'c2'),
        V('v3', 'Compare assurance levels across engagements.', 'Audits give reasonable assurance, reviews limited assurance, and related services give none.',
          [P('p1', 'Reasonable and limited', 5, 'reasonable|limited'), P('p2', 'Related services none', 5, 'related services')], 'c3'),
        V('v4', 'Why are AUP reports restricted?', 'Because people unaware of the reasons for the procedures may misread the findings.',
          [P('p1', 'Unaware users', 5, 'unaware'), P('p2', 'Misread', 5, 'misread')], 'c1'),
        V('v5', 'Which ethical principles apply to related services?', 'Integrity, objectivity, confidentiality, professional behaviour, and competence exercised with due care.',
          [P('p1', 'Integrity and objectivity', 5, 'integrity|objectivity'), P('p2', 'Confidentiality and behaviour', 5, 'confidentiality|behaviour')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Harmony Foods', 'difficulty': 'core',
              'case': 'Harmony Foods engages a CA to compile its statements for internal use. Opening balances contain errors. A team member suggests verifying all balances like an audit. The client also wants the CA to perform agreed procedures for its distributor on rebate claims.',
              'mcqs': [
                  M('k1a', 'Verifying all balances in the compilation is:', ['Not required, but known errors must be addressed', 'Mandatory', 'Prohibited', 'Required by SA 500'], 0,
                    'Compilation is not an audit. In practice: read for obvious errors.', 'core', topic=T2),
                  M('k1b', 'The opening balance errors should be:', ['Brought to management\'s attention for correction', 'Ignored', 'Corrected secretly', 'Reported to police'], 0,
                    'SRS 4410. In practice: withdraw if refused.', 'core', topic=T2),
                  M('k1c', 'The rebate claims work is governed by:', ['SRS 4400', 'SRS 4410', 'SA 700', 'SRE 2410'], 0,
                    'Agreed-upon procedures. In practice: factual findings.', 'core', topic=T1),
                  M('k1d', 'The AUP report should be restricted to:', ['Harmony and the distributor', 'The public', 'Harmony\'s bank only', 'No restriction'], 0,
                    'Agreeing parties. In practice: state clearly.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch09', 1, 'Related Services',
                ['Perform and report agreed-upon procedures engagements.',
                 'Perform and report compilation engagements.',
                 'Compare assurance levels across engagements.',
                 'Apply ethical and reporting practices to related services.'],
                {'difficulty': 'core', 'minutes': {'learn': 20, 'practice': 15}, 'prereq': ['fin-p3-ch08-u01'],
                 'exam_tip': 'Always say "no assurance" for AUP and compilation answers.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['SRS 4400: factual findings, no assurance.',
                             'Restricted use to agreeing parties.',
                             'SRS 4410: compile, read for obvious errors.',
                             'Withdraw if misleading info not corrected.',
                             'Ethics apply even without independence.'],
                 'remember': ['Audit: reasonable; review: limited; related: none.'],
                 'traps': ['Expressing an opinion in an AUP report.']},
                [('SRS 4400', 'AUP'), ('SRS 4410', 'Compilation'), ('Assurance', 'None'), ('Use', 'Restricted')],
                viva, cases)
