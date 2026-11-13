"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 8 Specialised Areas.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch08-u01'
T1 = 'Special purpose frameworks (SA 800)'
T2 = 'Single statements and specific elements (SA 805)'
T3 = 'Summary financial statements (SA 810)'
T4 = 'Reporting choices across specialised engagements'


def build():
    ck = Checks()
    m = ck.add('round(250*0.01,2)', 'Materiality for the receivables schedule at 1% (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Auditing a single schedule', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A lender asks the auditor of Ivy Ltd. to give an opinion only on its schedule of trade receivables of ₹250 lakh. The auditor also audits Ivy\'s complete statements, which carry a qualified opinion on inventory. The auditor sets materiality for the schedule at 1% of its value. Explain the approach.',
          'solution': [table(['Point', 'Treatment'], [
              ['Standard', 'SA 805 — specific element of a financial statement'],
              ['Materiality', 'Set for the element: 1% × 250 = ₹' + inr(m) + ' lakh'],
              ['Related items', 'Consider interrelated items (sales, allowance for credit loss)'],
              ['Modification on full statements', 'Consider relevance; qualified inventory issue may not affect receivables'],
              ['Report', 'Separate report on the schedule, distinguishable from the main report']], title='SA 805')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Reporting on summary statements', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'An auditor is asked to report on abridged financial statements of a company whose audited statements carry (a) an unmodified opinion; (b) a qualified opinion; (c) an adverse opinion. What opinion can be given on the summary statements?',
          'solution': [table(['Audited opinion', 'Summary report under SA 810'], [
              ['(a) Unmodified', 'Unmodified opinion that summary is consistent with audited statements'],
              ['(b) Qualified', 'Unmodified on consistency, but describe the qualified opinion and its basis and effect'],
              ['(c) Adverse or disclaimer', 'Withhold an opinion on the summary statements']], title='SA 810')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'A special purpose framework is designed to meet the information needs of specific users — e.g. tax basis, cash basis, regulator\'s provisions, contract-based reporting. SA 800 adapts other SAs for such audits.',
            'The auditor understands the purpose, intended users and steps taken by management to choose the framework, and confirms it is acceptable. Interpretation of contract terms used as a basis must be described.',
            'The report describes the purpose and, where appropriate, includes an emphasis of matter alerting users that the statements are prepared under a special purpose framework and may not suit other purposes; distribution or use may be restricted.'],
          'Special frameworks need users told what the statements are — and are not — for.',
          'Statements prepared to meet a loan agreement\'s definitions follow SA 800.'),
        C('c2', T2, [
            'SA 805 covers audits of a single statement (e.g. balance sheet only) or a specific element, account or item (e.g. receivables, royalty payable, provision for income tax). All relevant SAs apply, adapted to the engagement.',
            'Materiality is set for the single statement or element; interrelated items must be considered (e.g. sales when auditing receivables). The auditor may need to audit more than the element alone.',
            'If the opinion on the complete statements is adverse or a disclaimer, the auditor does not include an unmodified opinion on an element in the same report; a separate report on the element may be issued only if it is not a major portion of the statements and the law permits.'],
          'Auditing one item still needs the context of the whole.',
          'An opinion on royalties payable requires understanding sales figures used.'),
        C('c3', T3, [
            'SA 810 covers reporting on summary (abridged) financial statements derived from audited statements by the same auditor. Using the applied criteria, the auditor judges whether the summary agrees in every material way with the audited statements.',
            'Procedures: compare summary with audited statements, evaluate adequacy of disclosure of the summarised nature, check that audited statements are available to users, and ensure the summary report is dated no earlier than the audited report.',
            'If the audited report is modified, the summary report states this; if adverse or disclaimer, the auditor withholds an opinion on the summary.'],
          'Summary statements can only be as good as the audited set.',
          'Abridged statements sent to shareholders need consistency with audited accounts.'),
        C('c4', T4, [
            'Each specialised engagement uses tailored reports: identifying the framework or criteria, purpose, users and responsibilities.',
            'Restrictions on distribution or use, emphasis of matter on the basis of preparation, and other matter paragraphs are common features.',
            'Engagement acceptance requires agreeing terms (SA 210) and confirming the framework\'s acceptability and the auditor\'s ability to obtain evidence.'],
          'Tailor the report to the user and the framework.',
          'A cash-basis statement for a charity donor includes a restricted-use note.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Lender-specific audit request', 'role': 'Audit manager',
             'situation': 'A bank needs audited statements under the loan agreement\'s accounting rules.',
             'steps': ['Confirm the framework\'s acceptability and users.', 'Agree terms in writing.', 'Audit applying adapted SAs.', 'Issue a report with basis-of-preparation EOM and restriction.'],
             'takeaway': 'Know the user, the framework and the limits on use.'}]

    mcqs = [
        Q('m1', 'Statements prepared on a tax basis for filing with tax authorities follow:', ['A special purpose framework under SA 800', 'SA 810', 'SA 805 only', 'SRE 2400'], 0,
          'Specific users. In practice: EOM on basis.', 'c1', T1),
        Q('m2', 'An audit of only the schedule of receivables falls under:', ['SA 805', 'SA 800', 'SA 810', 'SA 700 only'], 0,
          'Specific element. In practice: element materiality.', 'c2', T2),
        Q('m3', 'Abridged financial statements are reported on under:', ['SA 810', 'SA 805', 'SA 720', 'SRS 4410'], 0,
          'Summary statements. In practice: consistency opinion.', 'c3', T3),
        Q('m4', 'If audited statements carry an adverse opinion, the auditor reporting on summary statements:', ['Withholds an opinion', 'Gives unmodified opinion', 'Gives qualified opinion', 'Gives EOM only'], 0,
          'SA 810. In practice: explain why.', 'c3', T3),
        Q('m5', 'In SA 805 engagements, materiality is determined for:', ['The single statement or element', 'The full financial statements', 'Nothing', 'Revenue only'], 0,
          'Element-level. In practice: may be lower.', 'c2', T2),
        Q('m6', 'An SA 800 report usually includes:', ['An emphasis of matter on the basis of preparation', 'Key audit matters always', 'A disclaimer', 'No opinion'], 0,
          'Alerts users. In practice: may restrict use.', 'c1', T1),
        Q('m7', 'The summary report under SA 810 cannot be dated:', ['Earlier than the audited statements\' report', 'Later than year end', 'After AGM', 'At all'], 0,
          'Consistency in time. In practice: same or later date.', 'c3', T3),
        Q('m8', 'Before accepting any specialised engagement, the auditor must:', ['Confirm the framework is acceptable and agree terms', 'Issue the report', 'Ignore users', 'Skip independence'], 0,
          'SA 210 preconditions. In practice: written terms.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'SA 805', 1, 'concept', '805'), S('s2', 'Materiality', 2, 'computation', 'materiality', nums=[m]), S('s3', 'Interrelated and report', 2, 'concept', 'interrelated|separate')],
          ['Consider the main opinion.'], ['Using full-statement materiality.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Unmodified', 1.5, 'concept', 'consistent'), S('s2', 'Qualified', 2, 'concept', 'describe'), S('s3', 'Withhold', 1.5, 'concept', 'withhold')],
          ['Cite SA 810.'], ['Giving an opinion despite adverse audit report.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is a special purpose framework?', 'A reporting basis built for particular users\' needs rather than general users, such as a tax or contractual basis.',
          [P('p1', 'Particular users', 5, 'particular users'), P('p2', 'Examples', 5, 'tax|contract')], 'c1'),
        V('v2', 'Why must interrelated items be considered under SA 805?', 'Because an element is affected by related accounts, so evidence on them is needed for a sound opinion.',
          [P('p1', 'Related accounts', 5, 'related'), P('p2', 'Evidence', 5, 'evidence')], 'c2'),
        V('v3', 'What opinion is expressed under SA 810?', 'Whether, judged against materiality, the summary agrees with the audited statements under the applied criteria.',
          [P('p1', 'Agrees', 5, 'agrees'), P('p2', 'Applied criteria', 5, 'criteria')], 'c3'),
        V('v4', 'When can a separate SA 805 report be given if the main opinion is adverse?', 'Only if the element forms a minor part of the statements, law permits it, and the opinion sits in a separate report.',
          [P('p1', 'Minor part', 5, 'minor'), P('p2', 'Separate report', 5, 'separate')], 'c2'),
        V('v5', 'What features are common in specialised reports?', 'Description of purpose and users, emphasis of matter on basis of preparation, and restriction on use.',
          [P('p1', 'Purpose and users', 5, 'purpose|users'), P('p2', 'Restriction', 5, 'restrict')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Stellar Retail Ltd.', 'difficulty': 'moderate',
              'case': 'Stellar Retail\'s main audit report contains a disclaimer of opinion. The company asks its auditor to (a) report on its abridged statements for a newspaper, and (b) give an opinion on its schedule of rent payable, which is 2% of total expenses.',
              'mcqs': [
                  M('k1a', 'On the abridged statements, the auditor should:', ['Withhold an opinion', 'Give an unmodified opinion', 'Give a qualified opinion', 'Refer only to KAMs'], 0,
                    'Disclaimer on audited set. In practice: SA 810.', 'core', topic=T3),
                  M('k1b', 'The rent schedule engagement falls under:', ['SA 805', 'SA 800', 'SA 810', 'SRS 4400'], 0,
                    'Specific element. In practice: separate report.', 'core', topic=T2),
                  M('k1c', 'An unmodified opinion on rent payable can be given:', ['Only in a separate report, as rent is not a major portion and if law permits', 'In the same report as the disclaimer', 'Never', 'Always'], 0,
                    'SA 805 restriction. In practice: assess carefully.', 'hard', topic=T2),
                  M('k1d', 'Before acceptance, the auditor must confirm:', ['Acceptability of the criteria and terms', 'Only fee', 'Only timing', 'Nothing'], 0,
                    'SA 210. In practice: written engagement letter.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch08', 1, 'Specialised Areas',
                ['Audit statements under special purpose frameworks.',
                 'Audit single statements and specific elements.',
                 'Report on summary financial statements.',
                 'Choose reporting features across specialised engagements.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 20}, 'prereq': ['fin-p3-ch07-u01'],
                 'exam_tip': 'Match the request to SA 800, 805 or 810 first.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['SA 800: special purpose frameworks.',
                             'SA 805: single statements/elements.',
                             'SA 810: summary statements consistency.',
                             'Adverse/disclaimer → withhold summary opinion.',
                             'EOM on basis; restriction on use.'],
                 'remember': ['Element materiality may be lower.'],
                 'traps': ['Giving an unmodified summary opinion after an adverse audit opinion.']},
                [('SA 800', 'Special framework'), ('SA 805', 'Element'), ('SA 810', 'Summary'), ('Adverse main', 'Withhold')],
                viva, cases)
