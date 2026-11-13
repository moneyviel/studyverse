"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 7 Reporting.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch07-u01'
T1 = 'Forming the opinion and the report structure (SA 700)'
T2 = 'Key audit matters (SA 701)'
T3 = 'Modified opinions (SA 705)'
T4 = 'Emphasis of matter, other matter and other information (SA 706, SA 720)'
T5 = 'Statutory reporting: section 143 and CARO 2020'


def build():
    ck = Checks()
    mat = ck.add('30', 'Materiality (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Choosing the opinion', 'difficulty': 'hard', 'minutes': 9,
          'q': 'Materiality is ₹30 lakh. Decide the opinion: (a) inventory overstated by ₹45 lakh, isolated; (b) depreciation not charged on all assets, overstating profit by ₹8 crore and affecting most line items; (c) records of a branch representing 70% of assets destroyed — no evidence possible; (d) receivables of ₹40 lakh could not be confirmed and no alternative procedures possible.',
          'solution': [table(['Case', 'Nature', 'Material and pervasive?', 'Opinion'], [
              ['(a)', 'Misstatement', 'Material (> ' + inr(mat) + '), not pervasive', 'Qualified'],
              ['(b)', 'Misstatement', 'Material and pervasive', 'Adverse'],
              ['(c)', 'Inability to obtain evidence', 'Material and pervasive', 'Disclaimer'],
              ['(d)', 'Inability to obtain evidence', 'Material, not pervasive', 'Qualified']], title='SA 705 matrix')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'KAM, EOM or other matter?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'For a listed company audit, classify: (a) complex goodwill impairment testing that took most audit effort; (b) a major fire after year end, properly disclosed; (c) prior year statements audited by another auditor; (d) a material uncertainty on going concern, adequately disclosed.',
          'solution': [table(['Matter', 'Treatment'], [
              ['(a)', 'Key audit matter (SA 701)'],
              ['(b)', 'Emphasis of matter (SA 706) — disclosed and fundamental to understanding'],
              ['(c)', 'Other matter paragraph (SA 706/710)'],
              ['(d)', 'Separate Material Uncertainty Related to Going Concern section (SA 570), not a KAM paragraph']], title='Report sections')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'SA 700: the auditor decides whether, judged against materiality, the statements follow the applicable framework, evaluating sufficiency of evidence, uncorrected misstatements, qualitative aspects of accounting practices, and whether statements give a true and fair view.',
            'Report elements: title, addressee, opinion section (first), basis for opinion (SAs, independence, evidence), going concern (where applicable), key audit matters (listed entities), other information, responsibilities of management and TCWG, auditor\'s responsibilities, other legal and regulatory requirements, signature with membership number and UDIN, place and date.',
            'The report is dated no earlier than when sufficient appropriate evidence has been obtained, including that statements have been approved.'],
          'Opinion first, basis next, then responsibilities.',
          'A report dated before board approval of statements is invalid.'),
        C('c2', T2, [
            'Key audit matters are those of most significance in the audit of the current period, selected from matters communicated with TCWG, considering higher assessed risks, significant judgements and significant events.',
            'KAMs are required for audits of listed entities (and where law requires or auditor decides). Each KAM describes why it was significant and how it was addressed. KAMs are not a substitute for a modified opinion, going concern reporting or disclosures.',
            'A matter giving rise to a modified opinion or a going concern material uncertainty is reported in those sections, not as a KAM.'],
          'KAMs tell users where the auditor spent most judgement.',
          'Revenue recognition for long-term contracts is a common KAM.'),
        C('c3', T3, [
            'Modification is needed when statements are materially misstated or the auditor cannot obtain sufficient appropriate evidence. The type depends on the nature (misstatement or limitation) and pervasiveness.',
            'Material but not pervasive → qualified; material and pervasive misstatement → adverse; material and pervasive inability → disclaimer. Pervasive effects are not confined to specific items, or represent a substantial part of the statements, or relate to fundamental disclosures.',
            'The basis for modified opinion paragraph describes and quantifies effects where practicable. If management imposes a scope limitation after acceptance that would lead to a disclaimer, the auditor may withdraw where possible.'],
          'Nature plus pervasiveness decides the opinion.',
          'Missing evidence for most assets leads to a disclaimer.'),
        C('c4', T4, [
            'An emphasis of matter paragraph (SA 706) draws attention to a matter appropriately presented or disclosed that is fundamental to users\' understanding (e.g. a major catastrophe, early application of a standard, significant uncertainty from litigation), without modifying the opinion.',
            'An other matter paragraph refers to matters not presented or disclosed but relevant to understanding the audit or report (e.g. comparative statements audited by another auditor, restriction on distribution).',
            'SA 720: the auditor reads other information in the annual report (directors\' report, chairman\'s statement) for material inconsistencies with statements or the auditor\'s knowledge, and reports on it in a separate section; uncorrected material misstatement of other information is described.'],
          'EOM points to what is disclosed; Other Matter to what is not.',
          'A major fire disclosed after year end can be highlighted as an EOM.'),
        C('c5', T5, [
            'Section 143 requires the auditor to report on matters such as information and explanations obtained, proper books, branch audit reports, agreement with books, compliance with accounting standards, adverse observations on functioning, director disqualification, qualifications related to maintenance of accounts, internal financial controls, and under Rule 11: pending litigations, foreseeable losses, IEPF transfers, funding through intermediaries, dividend compliance, and audit trail.',
            'CARO 2020 applies to most companies (exempting banks, insurance, section 8, OPCs, small companies and certain private companies) and requires reporting on matters like PPE, inventory, loans and advances, deposits, statutory dues, defaults, use of funds, fraud, whistle-blower complaints, related party compliance, internal audit, cash losses, auditor resignation, uncertainty on meeting liabilities, CSR and qualifications in group companies\' CARO reports.',
            'Auditors also communicate deficiencies and other matters to management and TCWG through management letters.'],
          'Indian audits add statutory reporting on top of the SA opinion.',
          'CARO asks whether statutory dues are deposited regularly and lists overdue amounts.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Drafting a listed company report', 'role': 'Audit manager',
             'situation': 'A listed client with an impairment judgement and a qualified inventory issue.',
             'steps': ['Decide opinion type.', 'Draft KAMs excluding the qualified matter.', 'Read other information under SA 720.', 'Complete section 143, Rule 11 and CARO reporting.'],
             'takeaway': 'Each issue belongs in exactly one part of the report.'}]

    mcqs = [
        Q('m1', 'A material and pervasive misstatement leads to:', ['An adverse opinion', 'A qualified opinion', 'A disclaimer', 'An unmodified opinion'], 0,
          'SA 705. In practice: explain basis.', 'c3', T3),
        Q('m2', 'Key audit matters are required for audits of:', ['Listed entities', 'All entities', 'Only banks', 'Only small companies'], 0,
          'Plus where law requires or auditor chooses. In practice: SA 701.', 'c2', T2),
        Q('m3', 'A matter causing a qualified opinion is reported:', ['In the basis for qualified opinion section, not as a KAM', 'As a KAM', 'In EOM', 'In other matter'], 0,
          'Avoid double reporting. In practice: cross-reference.', 'c2', T2),
        Q('m4', 'An emphasis of matter paragraph:', ['Draws attention to an appropriately disclosed fundamental matter', 'Modifies the opinion', 'Reports undisclosed matters', 'Replaces KAMs'], 0,
          'SA 706. In practice: use sparingly.', 'c4', T4),
        Q('m5', 'The opinion section in the auditor\'s report appears:', ['First', 'Last', 'After KAMs', 'After responsibilities'], 0,
          'SA 700 order. In practice: followed by basis for opinion.', 'c1', T1),
        Q('m6', 'SA 720 requires the auditor to:', ['Read other information for material inconsistencies', 'Audit the directors\' report', 'Ignore the annual report', 'Sign the chairman\'s statement'], 0,
          'Not an audit of other information. In practice: separate section.', 'c4', T4),
        Q('m7', 'CARO 2020 does not apply to:', ['Banking companies', 'Listed manufacturing companies', 'Public companies', 'Large private companies'], 0,
          'Exempt classes. In practice: also insurers, section 8, OPCs, small companies.', 'c5', T5),
        Q('m8', 'An inability to obtain evidence that is material but not pervasive leads to:', ['A qualified opinion', 'A disclaimer', 'An adverse opinion', 'An unmodified opinion with EOM'], 0,
          'SA 705 matrix. In practice: describe limitation.', 'c3', T3),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Qualified cases', 3, 'concept', 'qualified', nums=[mat]), S('s2', 'Adverse', 2.5, 'concept', 'adverse'), S('s3', 'Disclaimer', 2.5, 'concept', 'disclaimer')],
          ['Assess pervasiveness.'], ['Disclaiming for misstatements.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'KAM', 1.5, 'concept', 'key audit'), S('s2', 'EOM and other matter', 2, 'concept', 'emphasis|other matter'), S('s3', 'Going concern', 1.5, 'concept', 'material uncertainty')],
          ['Place each correctly.'], ['Reporting going concern as KAM.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'How is the type of modified opinion decided?', 'By the nature of the matter — misstatement or inability to obtain evidence — and whether its effects are pervasive.',
          [P('p1', 'Nature', 5, 'misstatement|inability'), P('p2', 'Pervasive', 5, 'pervasive')], 'c3'),
        V('v2', 'What are key audit matters?', 'Matters of most significance in the current audit, chosen from those communicated with those charged with governance.',
          [P('p1', 'Most significance', 5, 'significance'), P('p2', 'Communicated with governance', 5, 'governance')], 'c2'),
        V('v3', 'Distinguish emphasis of matter and other matter paragraphs.', 'Emphasis of matter highlights a matter already disclosed in the statements; other matter covers things outside the statements relevant to the audit or report.',
          [P('p1', 'Disclosed', 5, 'disclosed'), P('p2', 'Outside statements', 5, 'outside')], 'c4'),
        V('v4', 'What does Rule 11 require auditors to report on?', 'Pending litigations, foreseeable losses, IEPF transfers, funding through intermediaries, dividend compliance and audit trail.',
          [P('p1', 'Litigation and losses', 5, 'litigation|losses'), P('p2', 'Audit trail or dividend', 5, 'audit trail|dividend')], 'c5'),
        V('v5', 'When is a report dated?', 'Not earlier than the date when sufficient appropriate evidence is obtained, including approval of the statements.',
          [P('p1', 'Sufficient evidence', 5, 'evidence'), P('p2', 'Approval', 5, 'approv')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Forge Engineering Ltd.', 'difficulty': 'moderate',
              'case': 'Forge Engineering, a listed company, has not provided for a disputed customer claim of ₹2 crore against materiality of ₹1.5 crore; the issue is isolated. A KAM on revenue from long-term contracts is planned. The directors\' report says profit grew 20%, while audited profit grew 8%. Statutory dues of ₹40 lakh are outstanding over six months.',
              'mcqs': [
                  M('k1a', 'The unprovided claim leads to:', ['A qualified opinion', 'An adverse opinion', 'A disclaimer', 'An unmodified opinion'], 0,
                    'Material, not pervasive. In practice: quantify in basis paragraph.', 'core', topic=T3),
                  M('k1b', 'The 20% vs 8% difference is handled under:', ['SA 720 — material inconsistency in other information', 'SA 701', 'SA 706', 'SA 570'], 0,
                    'Ask management to correct. In practice: describe if uncorrected.', 'core', topic=T4),
                  M('k1c', 'The outstanding statutory dues are reported under:', ['CARO 2020', 'SA 701', 'SA 706', 'SA 720'], 0,
                    'Clause on statutory dues. In practice: list amounts and period.', 'core', topic=T5),
                  M('k1d', 'The long-term contract revenue matter belongs in:', ['Key audit matters section', 'Emphasis of matter', 'Basis for qualified opinion', 'Other matter'], 0,
                    'Significant judgement, not modified. In practice: describe response.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch07', 1, 'Reporting',
                ['Form the opinion and structure the report under SA 700.',
                 'Communicate key audit matters under SA 701.',
                 'Choose the correct modified opinion under SA 705.',
                 'Use EOM, other matter and other information sections.',
                 'Report under section 143, Rule 11 and CARO 2020.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 30}, 'prereq': ['fin-p3-ch06-u01'],
                 'exam_tip': 'Use the 2×2 matrix (misstatement/limitation × pervasive/not) for every opinion question.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['SA 700 report order: opinion first.',
                             'SA 701 KAMs for listed entities.',
                             'SA 705: qualified, adverse, disclaimer.',
                             'SA 706 EOM/other matter; SA 720 other information.',
                             'Section 143, Rule 11, CARO 2020.'],
                 'remember': ['Going concern uncertainty has its own section.'],
                 'traps': ['Disclaiming for a known misstatement.']},
                [('Material, not pervasive', 'Qualified'), ('Misstatement pervasive', 'Adverse'), ('Limitation pervasive', 'Disclaimer'), ('KAM', 'Listed entities')],
                viva, cases)
