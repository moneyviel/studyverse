"""CA Intermediate · Paper 5 Auditing and Ethics · Chapter 6 Audit Documentation (SA 230).
Scope follows the ICAI study material; explanations, names and figures are original."""
from ikit import *

UID = 'int-p5-ch06-u01'
T1 = 'Meaning, objective and nature of audit documentation'
T2 = 'Purpose of audit documentation'
T3 = 'Form, content and extent'
T4 = 'Timely preparation, audit file and final assembly'
T5 = 'Significant matters, departures and completion memorandum'
T6 = 'Ownership, custody and retention'


def build():
    ck = Checks()
    last = ck.add('60', 'Days after report date by which the final file is ordinarily assembled')
    keep = ck.add('7', 'Minimum retention period in years (from report date or group report date, if later)')
    i1 = {'id': 'i1', 'title': 'Timeline for an audit file', 'difficulty': 'core', 'minutes': 5,
          'q': 'CA Tanvi signs the audit report of Brahmaputra Foods Ltd. on 20 May 2027; the group auditor\'s report on the parent is dated 30 June 2027. By when should her file be assembled, how long must it be kept, and what may she still change after the report date?',
          'solution': [table(['Point', 'Guidance'], [
              ['Assembly of the final file', f'Ordinarily within {last} days of 20 May 2027 — i.e. by about mid-July 2027.'],
              ['Retention', f'At least {keep} years, counted from the later of the auditor\'s report (20 May 2027) and the group auditor\'s report (30 June 2027) — so at least until 30 June 2034.'],
              ['Changes during assembly', 'Only administrative ones: discarding superseded drafts, sorting and cross-referencing, signing off completion checklists, and documenting evidence obtained and agreed before the report date.'],
              ['Changes after assembly', 'No deletion or discarding before the retention period ends. Any later addition or modification records the reasons, who made it and when, and who reviewed it.']], title='Documentation timeline'),
              note('Assembly is administrative: no new audit procedures or new conclusions are drawn after the report date.')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Is the working paper good enough?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'A trainee\'s working paper on receivables says only: "Debtors checked — OK". Explain what is missing under SA 230 and rewrite its key elements.',
          'solution': [ul(['Identifying characteristics of items tested (e.g. confirmation numbers, customer codes, amounts selected and how).',
                           'Nature, timing and extent of procedures (confirmations sent on a date, alternative procedures for non-replies).',
                           'Results and evidence obtained (replies received, differences found and their resolution).',
                           'Conclusion reached on the assertion (existence and valuation of receivables).',
                           'Who performed the work and when; who reviewed it, when and to what extent.']),
                       p('The test is whether an experienced auditor with no previous connection to the audit could understand what was done, what was found and what was concluded. "Checked — OK" fails that test.')]}

    form = table(['The documentation must let an experienced outside auditor understand', 'In recording procedures also note'], [
        ['Nature, timing and extent of procedures performed', 'Identifying characteristics of the items or matters tested'],
        ['Results of procedures and evidence obtained', 'Who performed the work and the date it was completed'],
        ['Significant matters, conclusions and significant professional judgements', 'Who reviewed the work, the date and extent of review']], title='SA 230: form, content and extent')
    facts = table(['Factor affecting form, content and extent', ''], [
        ['Size and complexity of the entity', ''], ['Nature of procedures', ''], ['Identified risks of material misstatement', ''],
        ['Significance of evidence obtained', ''], ['Nature and extent of exceptions', ''], ['Need to document conclusions not readily seen from the work', ''],
        ['Audit methodology and tools used', '']], title='Factors')

    concepts = [
        C('c1', T1, [
            'Audit documentation is the record of procedures performed, relevant evidence obtained and conclusions reached; it is often called the working papers.',
            'The auditor aims to keep a record that adequately shows the basis for the report, and evidence that the audit was planned and performed according to SAs and legal and regulatory requirements.',
            'It may be on paper, electronic or other media. Examples: audit programmes, analyses, issues memoranda, summaries of significant matters, confirmation and representation letters, checklists, and correspondence on significant matters; abstracts or copies of entity records may be included.'],
          'If it is not documented, for review purposes it was not done.',
          'An e-mail from the lawyer confirming a claim\'s status forms part of audit documentation.'),
        C('c2', T2, [
            'Documentation helps the engagement team plan and perform the audit; helps supervisors direct, supervise and review; makes the team accountable for its work; retains matters of continuing significance for future audits; enables quality control reviews and inspections; and enables external inspections under law or regulation.'],
          'Working papers are the audit\'s memory and its defence.',
          'Notes about a long-running tax dispute help next year\'s team plan quickly.'),
        C('c3', T3, [
            'The documentation must be sufficient for an experienced auditor with no previous connection with the audit to understand the work, the results and the conclusions (table).',
            'Its form, content and extent depend on factors such as size and complexity, the procedures used, risks, significance of evidence, exceptions and the methodology used.',
            'Oral explanations alone are not adequate support, but they may clarify information in the documentation. Discussions of significant matters with management and those charged with governance are recorded, including when and with whom.'],
          'Write for a stranger who must understand your audit without asking you.',
          'A note "inventory OK" is useless; "test-counted 25 items worth ₹8.4 lakh; no differences" is useful.',
          blocks=[form, facts]),
        C('c4', T4, [
            'Documentation should be prepared on a timely basis; work done later tends to be less accurate.',
            'The audit file holds the documentation for an engagement. Final assembly is completed timely after the report date — ordinarily within 60 days — and involves only administrative changes, not new procedures or conclusions.',
            'After assembly, nothing is deleted or discarded before the end of the retention period. If modifications or additions are needed later, the auditor records the specific reasons, when and by whom they were made and reviewed.'],
          'Close the file soon after signing, then seal it for the retention period.',
          'Superseded drafts may be discarded during assembly, not after it.'),
        C('c5', T5, [
            'Significant matters include those giving rise to significant risks, results suggesting material misstatement or a need to revise risk assessment, circumstances causing significant difficulty, and findings that could modify the opinion or require an Emphasis of Matter paragraph.',
            'If the auditor departs from a relevant requirement of an SA in exceptional circumstances, the documentation records how alternative procedures achieved its aim and the reasons for the departure.',
            'Matters arising after the report date requiring new or additional procedures are documented with the circumstances, procedures, evidence, conclusions and their effect.',
            'A completion memorandum summarising significant matters and how they were addressed helps review, especially in large or complex audits.'],
          'The thinking behind the hard calls is the most important part of the file.',
          'A judgement on impairment of a major plant is recorded with the data and reasoning used.'),
        C('c6', T6, [
            'Unless law or regulation says otherwise, audit documentation is the property of the auditor (SQC 1). He may, at his discretion, give clients extracts or portions, provided this does not undermine the validity of the work or, in assurance engagements, his independence or that of his staff.',
            'Retention: a minimum of seven years, counted from the report date or, if later, the group auditor\'s report date.',
            'The firm must keep documentation confidential and safe, maintain its integrity, and keep it accessible and retrievable.'],
          'The client pays for the opinion, not for the auditor\'s notebooks.',
          'A director\'s demand to take away the audit files can be politely refused.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'File review before sign-off', 'role': 'Audit manager',
         'situation': 'The report will be signed tomorrow.',
         'steps': ['Check every significant risk has a documented response and conclusion.', 'Ensure preparer and reviewer sign-offs with dates.', 'Prepare a completion memorandum of significant matters.', 'Confirm discussions with management are recorded.'],
         'takeaway': 'Review the judgments, not just the ticks.'},
        {'id': 'j2', 'title': 'Archiving the file', 'role': 'Audit senior',
         'situation': 'The report was signed three weeks ago.',
         'steps': ['Remove superseded drafts and cross-reference papers.', 'Sign off the assembly checklist within 60 days.', 'Lock the electronic file and record retention date.'],
         'takeaway': 'Assembly is administrative; no new conclusions after the report date.'},
    ]

    mcqs = [
        Q('m1', 'Audit documentation should be sufficient to enable:', ['An experienced auditor with no previous connection with the audit to understand the work', 'The client\'s accountant to redo the audit', 'Only the engagement partner to understand it', 'Shareholders to verify figures'], 0,
          'SA 230 sets the standard of an experienced outside auditor who must be able to understand the nature, timing and extent of procedures, results, evidence, and significant matters and judgements. Other readers are not the benchmark. In practice: avoid cryptic notes.', 'c3', T3),
        Q('m2', 'The final audit file is ordinarily assembled within:', ['60 days of the date of the auditor\'s report', '30 days of year-end', '7 years', '1 year of the report'], 0,
          'SQC 1 and SA 230 indicate that an appropriate time limit for completing assembly is ordinarily not more than 60 days after the report date. Seven years is the retention period, not the assembly limit. In practice: diarise the date.', 'c4', T4, 'core'),
        Q('m3', 'Audit documentation is ordinarily retained for at least:', ['7 years from the report date (or group report date, if later)', '3 years', '8 years from year-end', '10 years'], 0,
          'SQC 1 sets a minimum retention of seven years, counted from the report date or, if later, the group auditor\'s report date. Firms may keep it longer. In practice: track retention dates in the archive.', 'c6', T6, 'core'),
        Q('m4', 'Audit documentation belongs to:', ['The auditor, unless law provides otherwise', 'The client', 'The shareholders', 'The Registrar of Companies'], 0,
          'SQC 1 states that documentation is the property of the auditor unless law or regulation specifies otherwise; the auditor may share extracts at his discretion without compromising the work or independence. In practice: clients cannot demand working papers.', 'c6', T6),
        Q('m5', 'Which change is permitted during final assembly of the audit file?', ['Discarding superseded drafts', 'Performing new substantive tests', 'Changing the audit opinion', 'Deleting evidence that conflicts with conclusions'], 0,
          'Assembly allows only administrative changes such as discarding superseded documentation, sorting and cross-referencing, signing off checklists, and recording evidence obtained before the report date. New procedures or conclusions are not part of assembly. In practice: keep conflicting evidence.', 'c4', T4),
        Q('m6', 'Oral explanations by the auditor are:', ['Not adequate support on their own but may clarify documentation', 'Fully adequate support', 'Prohibited', 'A substitute for working papers'], 0,
          'SA 230 states that oral explanations alone do not represent adequate support for work performed or conclusions reached, but they may explain or clarify information in the documentation. In practice: write it down.', 'c3', T3),
        Q('m7', 'A summary of significant matters and how they were addressed is called a:', ['Completion memorandum', 'Engagement letter', 'Management representation letter', 'Audit programme'], 0,
          'A completion memorandum (audit documentation summary) records significant matters and their resolution, aiding review and inspection, especially in large and complex audits. Engagement and representation letters serve other purposes. In practice: partners review it before signing.', 'c5', T5),
        Q('m8', 'In documenting procedures, the auditor records who performed the work and:', ['Who reviewed it, when and to what extent', 'The fees charged', 'The client\'s opinion of the work', 'The auditor\'s tax status'], 0,
          'SA 230 requires recording identifying characteristics of items tested, who performed the work and when, and who reviewed it, the date and extent of review. This supports accountability and quality review. In practice: use sign-off fields.', 'c3', T3),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Assembly 60 days', 1, 'concept', '60'),
           S('s2', 'Retention 7 years from later date', 1.5, 'concept', 'seven|7', 'group|later'),
           S('s3', 'Administrative changes only', 1.5, 'concept', 'administrative|superseded')],
          ['Use the later date for retention.'], ['Counting retention from year-end.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Items tested identified', 1, 'concept', 'identifying|items'),
           S('s2', 'Procedures and results', 1, 'concept', 'nature|results|evidence'),
           S('s3', 'Conclusion', 1, 'concept', 'conclusion'),
           S('s4', 'Preparer and reviewer', 1, 'concept', 'review')],
          ['Apply the "experienced auditor" test.'], ['Accepting tick-mark notes.'], ['List + note.']),
        W('q3', 3, 'A director of Ganga Textiles Ltd. insists that the company owns the audit working papers because it paid the audit fee. Comment.',
          [p('The contention is not correct. Under SQC 1, unless law or regulation provides otherwise, audit documentation is the property of the auditor. The fee buys the audit opinion, not the working papers. The auditor may, at his discretion, make portions or extracts available to the client, provided this does not undermine the validity of the work or the independence of the auditor or his staff.')],
          [S('s1', 'Property of auditor', 1.5, 'concept', 'property|belongs|own'),
           S('s2', 'SQC 1', 0.5, 'concept', 'sqc'),
           S('s3', 'Extracts at discretion', 1, 'concept', 'discretion|extract')],
          ['Conclude clearly.'], ['Agreeing with the director.'], ['Short paragraph.']),
    ]

    viva = [
        V('v1', 'What is audit documentation?',
          'It is the record of audit procedures performed, the relevant evidence obtained and the conclusions the auditor reached.',
          [P('p1', 'Procedures', 3, 'procedure'), P('p2', 'Evidence', 3, 'evidence'), P('p3', 'Conclusions', 4, 'conclusion')], 'c1'),
        V('v2', 'Give three purposes of audit documentation.',
          'It helps the team plan and perform the audit, helps supervisors review the work, and enables quality control and external inspections.',
          [P('p1', 'Plan and perform', 3, 'plan'), P('p2', 'Supervise and review', 3, 'review|supervis'), P('p3', 'Inspections', 4, 'inspection|quality')], 'c2'),
        V('v3', 'What may be changed after the report date during assembly?',
          'Only administrative matters such as discarding superseded drafts, sorting and cross-referencing papers and signing off checklists; all real audit work belongs before the report date.',
          [P('p1', 'Administrative only', 6, 'administrative|superseded|sorting'), P('p2', 'Audit work before report date', 4, 'before the report date|report date')], 'c4'),
        V('v4', 'How long must audit files be retained?',
          'At least seven years, counted from the report date, or from the group auditor\'s report date if that is later.',
          [P('p1', 'Seven years', 6, 'seven|7'), P('p2', 'From report date', 4, 'report')], 'c6'),
        V('v5', 'What is recorded if the auditor departs from an SA requirement?',
          'How the alternative procedures performed achieve the aim of that requirement, and the reasons for the departure.',
          [P('p1', 'Alternative procedures', 5, 'alternative'), P('p2', 'Reasons', 5, 'reason')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'CA Raghav\'s file', 'difficulty': 'moderate',
              'case': 'CA Raghav signed the audit report of Indus Polymers Ltd. on 15 June. On 25 August he still had not assembled the file. In September, he wanted to add a note explaining a judgement on inventory valuation made in May, and to delete an old draft letter.',
              'mcqs': [
                  M('k1a', 'Raghav\'s delay in assembling the file is:', ['Beyond the ordinary 60-day limit', 'Within the limit', 'Irrelevant', 'Required by SA 230'], 0,
                    '15 June plus 60 days is about 14 August, so assembly by 25 August exceeds the ordinary limit set by firm policy under SQC 1. Timely assembly protects the file\'s integrity. In practice: set reminders on the report date.', 'core', topic=T4),
                  M('k1b', 'Adding a note in September about the May judgement requires:', ['Recording the reasons, who made it and when, and who reviewed it', 'No documentation', 'Re-issuing the audit report', 'Client approval'], 0,
                    'After assembly, any modification or addition must document specific reasons, when and by whom it was made and reviewed. It must not be presented as if done earlier. In practice: date additions clearly.', 'moderate', topic=T4),
                  M('k1c', 'Deleting the old draft letter in September (after assembly) is:', ['Not permitted before the retention period ends', 'Permitted as administrative', 'Permitted with client consent', 'Mandatory'], 0,
                    'Discarding superseded drafts is allowed only during final assembly; once the file is assembled, nothing is deleted or discarded before the retention period ends. In practice: clean up drafts before closing the file.', 'moderate', topic=T4),
                  M('k1d', 'The judgement on inventory valuation is best documented as:', ['A significant matter with the data, reasoning and conclusion', 'A tick mark', 'An oral explanation to the partner', 'Not needed'], 0,
                    'Significant professional judgements must be documented so an experienced auditor can understand them; oral explanations alone are not adequate. Including data and reasoning shows the basis for the conclusion. In practice: add it to the completion memorandum.', 'core', topic=T5),
              ]}]

    return unit(UID, 'p5', 'int-p5-ch06', 1, 'Audit Documentation',
                ['Explain the meaning, objective, nature and purposes of audit documentation (SA 230).',
                 'Apply the requirements on form, content and extent of documentation.',
                 'Explain timely preparation, assembly of the final audit file and later changes.',
                 'Document significant matters, departures and completion memoranda.',
                 'Explain ownership, custody and retention of audit documentation.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 25}, 'prereq': ['int-p5-ch05-u01'],
                 'exam_tip': 'Remember three numbers and one rule: 60 days to assemble, 7 years to retain (from the later report date), ownership with the auditor, and only administrative changes after the report date.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Documentation = record of procedures, evidence and conclusions.', 'Experienced outside auditor test.', 'Record preparer, reviewer, dates and items tested.',
                             'Assemble within ordinarily 60 days; administrative changes only.', 'Retain at least 7 years from the later of report or group report date.',
                             'Property of the auditor (SQC 1); extracts at discretion.'],
                 'remember': ['Oral explanations alone are not adequate.', 'Document reasons for any departure from an SA.'],
                 'traps': ['Retention runs from report date, not year-end.', 'No deletion after assembly.']},
                [('Assembly', '≤ 60 days after report'), ('Retention', '≥ 7 years'), ('Ownership', 'Auditor'), ('Standard', 'SA 230')],
                viva, cases,
                topics=['Audit Documentation'])
