"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 13 Group Audits.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch13-u01'
T1 = 'Consolidation requirements and responsibilities'
T2 = 'Audit considerations and using component auditors'
T3 = 'Auditing the consolidation process'
T4 = 'Reporting on consolidated financial statements'


def build():
    ck = Checks()
    share = ck.add('round((300+150)/1500*100,2)', 'Share of consolidated assets audited by other auditors (%)')
    i1 = {'id': 'i1', 'title': 'Components audited by others', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Parent Ltd.\'s consolidated total assets are ₹1,500 crore. Two subsidiaries with assets of ₹300 crore and ₹150 crore are audited by other firms. Compute the share audited by others and describe how the parent auditor reports.',
          'solution': [table(['Point', 'Treatment'], [
              ['Share audited by others', '(300 + 150) ÷ 1,500 = ' + inr(share) + '%'],
              ['Procedures', 'Assess component auditors\' competence and independence; review reports and significant findings'],
              ['Report', 'Other Matter paragraph stating that components with stated assets, revenues and cash flows were audited by other auditors, and the opinion relies on their reports'],
              ['Opinion', 'Not modified merely because of reliance on others']], title='CFS reporting')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Consolidation adjustments to verify', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'List what the parent auditor checks in: (a) elimination of the parent\'s investment against subsidiary equity; (b) intra-group sales with stock still held; (c) a subsidiary with a different year end; (d) a subsidiary using different accounting policies.',
          'solution': [table(['Item', 'Check'], [
              ['(a)', 'Goodwill/capital reserve computed correctly at acquisition (permanent adjustment)'],
              ['(b)', 'Intra-group sales eliminated and unrealised profit in stock removed (current adjustment)'],
              ['(c)', 'Gap within three months and adjustments for significant transactions'],
              ['(d)', 'Uniform policies applied through adjustments']], title='Auditing consolidation')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Section 129(3) requires companies with subsidiaries, associates or joint ventures to prepare consolidated financial statements (CFS), audited like standalone statements; section 143 applies to CFS reporting, including CARO paragraph (xxi) on qualifications in group companies\' CARO reports.',
            'The parent\'s management is responsible for preparing CFS: identifying components, ensuring uniform policies, obtaining component information, and making consolidation adjustments.',
            'The parent\'s auditor (principal auditor) gives the opinion on CFS and reports on internal financial controls of the parent and Indian subsidiaries where applicable; under SA 600 it is not responsible for work done by component auditors unless circumstances should have aroused suspicion, and its report shows this division of responsibility.'],
          'The parent prepares the CFS; its auditor opines on the whole, sharing responsibility with component auditors.',
          'A listed parent with five subsidiaries must present audited CFS.'),
        C('c2', T2, [
            'Audit considerations: understanding the group and its components, materiality for the group and components, risk assessment, and the work needed on significant components.',
            'Where other auditors audit components, the principal auditor considers their competence and independence, communicates instructions and timelines, obtains confirmations (independence, compliance with standards), reviews reports and significant matters, and may perform additional procedures or review their working papers.',
            'Modifications, EOMs or other matters in component auditors\' reports are evaluated for their effect on CFS.'],
          'Rely on component auditors only after evaluating them.',
          'A component auditor\'s qualification on inventory may need to flow into CFS.'),
        C('c3', T3, [
            'Auditing the consolidation covers: completeness of components, correctness of translation of foreign components, elimination of intra-group balances and transactions, unrealised profits, investment elimination and goodwill or capital reserve, NCI computation, and uniformity of policies.',
            'Permanent consolidation adjustments arise at acquisition (goodwill, pre-acquisition reserves); current period adjustments include intra-group eliminations, unrealised profits, dividends and changes in ownership.',
            'Reporting date differences must not exceed three months with adjustments for significant events; consolidation worksheets are reconciled to component statements.'],
          'Check both the one-time and the every-year adjustments.',
          'Unrealised profit on stock sold within the group must be removed.'),
        C('c4', T4, [
            'When the parent\'s auditor audits all components, the report is straightforward. When other auditors audit some components, the parent auditor may include an Other Matter paragraph describing the extent (assets, revenues, cash flows) audited by others and stating reliance on their reports; this is not a modification.',
            'If components are unaudited, the auditor considers materiality: if material, a modification may be needed; otherwise disclose. Component reports under a different framework or auditing standards require additional work or adjustments.',
            'Management representations for CFS are obtained from the parent\'s management.'],
          'Reference to others\' work goes in Other Matter, not the opinion.',
          'Unaudited material components may lead to a qualified CFS opinion.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Group audit coordination', 'role': 'Group audit manager',
             'situation': 'A conglomerate with 12 subsidiaries, three audited by other firms and one overseas.',
             'steps': ['Map components and significance.', 'Send instructions and obtain confirmations.', 'Audit consolidation adjustments.', 'Draft CFS report with Other Matter paragraph.'],
             'takeaway': 'Coordination and documentation make group audits work.'}]

    mcqs = [
        Q('m1', 'Responsibility for preparing consolidated statements lies with:', ['The parent\'s management', 'The principal auditor', 'Component auditors', 'Regulators'], 0,
          'Management\'s duty. In practice: auditor audits.', 'c1', T1),
        Q('m2', 'Reliance on other auditors for components is described in:', ['An Other Matter paragraph', 'The opinion paragraph as a qualification', 'A disclaimer', 'Key audit matters always'], 0,
          'Not a modification. In practice: give extent.', 'c4', T4),
        Q('m3', 'Goodwill computed at acquisition is a:', ['Permanent consolidation adjustment', 'Current period adjustment', 'Not an adjustment', 'Tax item'], 0,
          'One-time at acquisition. In practice: carried forward.', 'c3', T3),
        Q('m4', 'Elimination of unrealised profit on intra-group stock is a:', ['Current period adjustment', 'Permanent adjustment', 'Optional item', 'Disclosure only'], 0,
          'Recurs yearly. In practice: check stock at year end.', 'c3', T3),
        Q('m5', 'CARO paragraph (xxi) relates to:', ['Qualifications in CARO reports of companies in the CFS', 'Inventory', 'Loans', 'Fraud'], 0,
          'CFS-specific clause. In practice: list companies.', 'c1', T1),
        Q('m6', 'Before using a component auditor\'s work, the principal auditor assesses:', ['Competence and independence', 'Their fee', 'Their office size', 'Nothing'], 0,
          'Professional reputation. In practice: obtain confirmations.', 'c2', T2),
        Q('m7', 'The maximum difference between parent and component reporting dates is:', ['Three months', 'Six months', 'One year', 'One month'], 0,
          'With adjustments. In practice: Ind AS 110.', 'c3', T3),
        Q('m8', 'A material unaudited component may lead to:', ['A modified opinion on CFS', 'No effect', 'An emphasis of matter only', 'Resignation always'], 0,
          'Insufficient evidence. In practice: assess materiality.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Share', 1.5, 'computation', 'share', nums=[share]), S('s2', 'Procedures', 1.5, 'concept', 'competence|independence'), S('s3', 'Other Matter', 2, 'concept', 'other matter')],
          ['Describe extent.'], ['Qualifying the opinion for reliance.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Permanent', 1.5, 'concept', 'goodwill|permanent'), S('s2', 'Current', 1.5, 'concept', 'unrealised|eliminated'), S('s3', 'Dates and policies', 2, 'concept', 'three months|uniform')],
          ['Classify adjustments.'], ['Ignoring different year ends.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'How is responsibility shared in a CFS audit with component auditors?', 'The parent\'s auditor gives the CFS opinion but relies on component auditors for their work, with responsibility divided unless circumstances should have raised suspicion.',
          [P('p1', 'Parent\'s auditor opinion', 5, 'parent'), P('p2', 'Divided responsibility', 5, 'divided')], 'c1'),
        V('v2', 'What does the principal auditor obtain from component auditors?', 'Confirmations of independence and compliance with standards, their reports and significant findings.',
          [P('p1', 'Independence confirmation', 5, 'independence'), P('p2', 'Reports and findings', 5, 'report|finding')], 'c2'),
        V('v3', 'Distinguish permanent and current consolidation adjustments.', 'Permanent adjustments arise at acquisition, like goodwill; current adjustments recur each period, like eliminating intra-group transactions.',
          [P('p1', 'At acquisition', 5, 'acquisition'), P('p2', 'Each period', 5, 'each period|recur')], 'c3'),
        V('v4', 'How is reliance on other auditors reported?', 'Through an Other Matter paragraph giving the extent audited by others, which shows divided responsibility but does not modify the opinion.',
          [P('p1', 'Other Matter', 5, 'other matter'), P('p2', 'Extent', 5, 'extent')], 'c4'),
        V('v5', 'What does management do in preparing CFS?', 'Identifies components, applies uniform policies, gathers component information and makes consolidation adjustments.',
          [P('p1', 'Uniform policies', 5, 'uniform'), P('p2', 'Adjustments', 5, 'adjustment')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Meridian Holdings', 'difficulty': 'moderate',
              'case': 'Meridian Holdings has a UK subsidiary audited under ISAs by a UK firm, an Indian subsidiary whose auditor qualified its opinion on receivables, and an associate whose statements are unaudited but immaterial. Its parent auditor audits the parent only.',
              'mcqs': [
                  M('k1a', 'The UK subsidiary audited under ISAs requires the parent auditor to:', ['Assess differences and perform additional work if needed', 'Reject the report', 'Re-audit everything', 'Ignore differences'], 0,
                    'Framework and standards differences. In practice: conversion adjustments.', 'moderate', topic=T4),
                  M('k1b', 'The Indian subsidiary\'s qualification should be:', ['Evaluated for its effect on CFS', 'Ignored', 'Automatically copied', 'Reported to SEBI'], 0,
                    'Materiality at group level. In practice: may modify CFS opinion.', 'core', topic=T2),
                  M('k1c', 'The immaterial unaudited associate needs:', ['Disclosure in the Other Matter paragraph', 'A disclaimer', 'An adverse opinion', 'Nothing at all'], 0,
                    'State reliance on management information. In practice: materiality judgement.', 'moderate', topic=T4),
                  M('k1d', 'The opinion on the CFS is signed by:', ['The parent\'s auditor', 'The UK firm', 'The Indian subsidiary\'s auditor', 'Shareholders'], 0,
                    'Principal auditor, relying on component auditors with divided responsibility. In practice: coordinate.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch13', 1, 'Group Audits',
                ['Explain consolidation requirements and responsibilities.',
                 'Use the work of component auditors.',
                 'Audit consolidation adjustments.',
                 'Report on consolidated financial statements.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['fin-p3-ch12-u01'],
                 'exam_tip': 'Separate responsibilities: parent management prepares; parent auditor opines; component auditors answer for their own work.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 129(3): CFS required; section 143 reporting.',
                             'Principal auditor opines; responsibility divided with component auditors.',
                             'Assess component auditors; obtain confirmations.',
                             'Permanent vs current adjustments.',
                             'Other Matter for reliance; modify for material unaudited components.'],
                 'remember': ['CARO (xxi) for CFS.'],
                 'traps': ['Qualifying merely because others audited components.']},
                [('CFS', 'Section 129(3)'), ('Reliance', 'Other Matter'), ('Goodwill', 'Permanent'), ('URP', 'Current')],
                viva, cases)
