"""CA Intermediate · Paper 5 Auditing and Ethics · Chapter 1 Nature, Objective and Scope of Audit.
Scope follows the ICAI study material; explanations, examples and scenarios are original."""
from ikit import *

UID = 'int-p5-ch01-u01'
T1 = 'Meaning and nature of audit'
T2 = 'Origin and interdisciplinary nature'
T3 = 'Objectives of the auditor (SA 200)'
T4 = 'Scope of audit — what it covers and what it does not'
T5 = 'Inherent limitations of audit'
T6 = 'Benefits, appointment and reporting'
T7 = 'Assurance engagements and their elements'
T8 = 'Reasonable vs limited assurance'
T9 = 'Qualities of an auditor'
T10 = 'Engagement and quality control standards'


def build():
    scope = table(['Within the scope of audit', 'Outside the scope of audit'], [
        ['Covering every area of the entity relevant to the financial statements', 'Preparing and presenting the financial statements (management\'s job)'],
        ['Judging whether records and source documents are reliable and sufficient', 'Judging the technical condition or life of machinery and buildings (engineers\' job)'],
        ['Checking that information is properly disclosed and policies are suitable and consistent', 'Proving that documents are genuine (forensic experts\' job)'],
        ['Expressing an opinion on the financial statements', 'Conducting an official investigation with legal powers'],
    ], title='Scope of audit')
    limits = table(['Source of limitation', 'Example'], [
        ['Nature of financial reporting', 'Estimates such as provisions and useful lives involve judgement; internal controls can be overridden by collusion'],
        ['Nature of audit procedures', 'Testing is on a sample basis; the auditor cannot force anyone to hand over information; fraud may use forged documents or hidden related parties'],
        ['Audit is not an investigation', 'No legal powers to search premises or take statements on oath'],
        ['Timeliness vs cost', 'Information loses relevance with time; checking everything would cost too much and take too long'],
        ['Future events', 'Later events may hit the entity\'s ability to continue in business'],
    ], title='Inherent limitations (SA 200)')
    assur = table(['Basis', 'Reasonable assurance engagement', 'Limited assurance engagement'], [
        ['Level of assurance', 'High (but not absolute)', 'Lower — moderate'],
        ['Work done', 'Extensive procedures', 'Fewer procedures, mainly enquiry and analysis'],
        ['Conclusion', 'Positive opinion on the subject matter', 'Limited conclusion — nothing has come to notice suggesting a misstatement'],
        ['Example', 'Audit of financial statements', 'Review of quarterly financial results'],
    ], title='Reasonable vs limited assurance')
    stds = table(['Standards', 'Apply to', 'Examples'], [
        ['Standards on Auditing (SAs)', 'Audits of historical financial information', 'SA 200, SA 230, SA 315, SA 500, SA 700 (Revised)'],
        ['Standards on Review Engagements (SREs)', 'Reviews of historical financial information', 'SRE 2400 (Revised), SRE 2410'],
        ['Standards on Assurance Engagements (SAEs)', 'Assurance on other subject matter (e.g. projections, controls)', 'SAE 3400, SAE 3420'],
        ['Standards on Related Services (SRSs)', 'Agreed-upon procedures and compilations (no assurance)', 'SRS 4400, SRS 4410 (Revised)'],
        ['Standard on Quality Control (SQC 1)', 'The firm\'s quality system for all the above services', 'SQC 1'],
    ], title='Engagement and quality control standards issued under the authority of the ICAI Council')

    illus = [
        {'id': 'i1', 'title': 'Is this inside or outside the scope of audit?', 'difficulty': 'core', 'minutes': 6,
         'q': 'State whether each matter falls within the auditor\'s scope: (a) a pending penalty notice from an environmental tribunal is not disclosed in the notes; (b) the client asks the auditor to certify that a newly built warehouse will last 40 years; (c) the auditor is asked to confirm whether signatures on a sale deed are genuine; (d) the inventory valuation method was changed from FIFO to weighted average without disclosure.',
         'solution': [table(['Matter', 'Within scope?', 'Reason'], [
             ['(a) Undisclosed penalty notice', 'Yes', 'Proper disclosure of contingent liabilities is part of the audit; the auditor should ask for disclosure'],
             ['(b) Life of the warehouse', 'No', 'Needs an engineer\'s expertise; the auditor may rely on an expert\'s report'],
             ['(c) Genuineness of signatures', 'No', 'The auditor is not an expert in authenticating documents'],
             ['(d) Change in valuation method', 'Yes', 'The auditor checks the suitability and consistent application of accounting policies and their disclosure']], title='Analysis')]},
        {'id': 'i2', 'title': 'Which engagement and which standard?', 'difficulty': 'moderate', 'minutes': 6,
         'q': 'A bank asks Deccan Mills Pvt. Ltd. for (a) half-yearly results with a CA\'s assurance report, quickly; (b) projected statements for three years with a CA\'s report; (c) the company also asks the CA only to put its trial balance into proper financial-statement format and sign a report. Identify the type of engagement and the set of standards for each.',
         'solution': [table(['Request', 'Type of engagement', 'Standards'], [
             ['(a) Half-yearly results, quick assurance', 'Review — limited assurance', 'Standards on Review Engagements (e.g. SRE 2410 if done by the entity\'s auditor)'],
             ['(b) Projected statements', 'Assurance on prospective financial information — moderate assurance on assumptions', 'Standards on Assurance Engagements (SAE 3400)'],
             ['(c) Compiling statements', 'Related service — compilation, no assurance', 'Standards on Related Services (SRS 4410 (Revised))']], title='Answer'),
             note('SQC 1 governs the firm\'s quality system for all three engagements.')]},
    ]

    concepts = [
        C('c1', T1, [
            'An audit is an independent examination of the financial information of any entity — profit-making or not, small or large, whatever its legal form — carried out to express an opinion on that information.',
            'Independence means the auditor\'s judgement is not subordinate to anyone\'s wishes. Relationships (a relative who owns the business) or financial interests (holding the client\'s shares) destroy independence.',
            'Management prepares the financial statements; the auditor only expresses an opinion through a written report. To do so the auditor checks that the statements agree with the books, entries are supported by evidence, nothing is omitted, presentation is clear, classification and disclosure follow accounting standards, and the overall picture is true and fair.',
            'The essence of audit is assurance: it adds credibility so that users can rely on the statements.'],
          'An audit is like an independent food inspector\'s seal on a packet — the maker cooks, the inspector checks and certifies.',
          'Banks, investors, tax authorities and insurers all rely on audited statements before lending, investing, assessing or settling claims.'),
        C('c2', T2, [
            'Auditing is ancient: Kautilya\'s Arthashastra (around the 4th century BC) mentions a fixed accounting year, closing of accounts and their checking. The word comes from the Latin "audire" — to hear — because accounts were once read aloud to the auditor.',
            'In India, an Auditor General was first appointed in 1860; today the Comptroller and Auditor General of India is a constitutional authority auditing government receipts and spending. The ICAI was set up by an Act of Parliament in 1949 to regulate the profession.',
            'Auditing draws on many subjects: accounting (the base), law and taxation, economics, behavioural science (dealing with people), statistics and mathematics (sampling), data processing (IT audit), financial management (ratios, working capital) and production and costing (understanding operations).'],
          'An auditor is a general physician of business — needing a little of many sciences to diagnose well.',
          'Modern audit teams include IT specialists and data analysts alongside accountants.'),
        C('c3', T3, [
            'Under SA 200, the auditor\'s overall objectives are two: (a) to get reasonable assurance that the statements, taken as a whole, contain no material misstatement, whether caused by fraud or error, so that an opinion can be given on whether they are prepared, in all material respects, in line with the applicable financial reporting framework; and (b) based on what the audit finds, to issue a report on those statements and make the communications that the SAs call for.',
            'Reasonable assurance is a high level of assurance but not absolute — not a guarantee. Absolute assurance is impossible because of the inherent limitations of an audit.',
            'Misstatements may arise from fraud (intentional) or error (unintentional); the auditor looks at their effect on the statements as a whole.'],
          'Reasonable assurance is like a doctor\'s full health check-up — a strong indication of good health, not a promise you will never fall ill.',
          'An unmodified audit report does not mean the company is a safe investment; it means the statements are fairly presented.'),
        C('c4', T4, [
            'The purpose of an audit is to raise intended users\' confidence in the financial statements by an opinion on whether they follow the applicable financial reporting framework (for Indian companies, Schedule III to the Companies Act, 2013 along with accounting standards).',
            'Scope includes: covering all aspects of the entity relevant to the statements; being satisfied that records and source documents are reliable and sufficient (through study of systems and controls, tests and enquiries); and checking proper disclosure, including management\'s choice and consistent use of accounting policies.',
            'An audit deals with historical financial information — events and conditions of past periods.',
            'Outside scope: preparing the statements, judging technical matters needing other experts, authenticating documents and conducting official investigations. Investigation is a special-purpose, narrow examination (e.g. into a suspected fraud); audit is general and broad.'],
          'The auditor checks the recipe, ingredients and plating of a dish — but does not cook it, test the oven\'s wiring or interrogate the chef under oath.',
          'When a fraud is suspected, companies appoint forensic auditors for an investigation separate from the statutory audit.',
          blocks=[scope]),
        C('c5', T5, [
            'An auditor cannot reduce audit risk to zero, so absolute assurance is impossible. SA 200 traces this to five sources (table).',
            'Nature of financial reporting: many items need management judgement; internal controls can fail or be overridden by collusion between employees.',
            'Nature of audit procedures: sampling; no legal power to compel information; management fraud may use carefully planned schemes and fake documents; undisclosed related parties.',
            'Audit is not an investigation; information loses relevance with time and must be balanced against cost; future events may affect the entity\'s survival.'],
          'Inherent limitations are like a net with a fine but finite mesh — it catches most fish, but a determined small one can slip through.',
          'Frauds discovered years later — often involving collusion and forged papers — show why an audit is not a guarantee.',
          blocks=[limits]),
        C('c6', T6, [
            'An engagement is the formal agreement between auditor and client, recorded in an engagement letter. External audit engagements are reasonable assurance engagements.',
            'Benefits: reliable, high-quality information; protection of absentee owners (shareholders) who do not run the company; a moral check on employees; use by tax authorities and by lenders for credit decisions; detection of errors or frauds; pointing out weaknesses in controls.',
            'Audit may be compulsory (companies; businesses crossing tax-audit limits; bodies receiving government grants) or voluntary (firms choosing to be audited for its benefits).',
            'Appointment: generally by owners — members at the AGM for companies, partners for firms; by the Comptroller and Auditor General for government companies; or by a government authority under a law. The report goes to whoever appointed the auditor.'],
          'For shareholders who never visit the office, the auditor is their independent pair of eyes inside the company.',
          'Lenders usually make audited statements a condition for renewing working-capital limits.'),
        C('c7', T7, [
            'An assurance engagement is one in which a practitioner gives a conclusion meant to increase the confidence of intended users (other than the party responsible for the subject matter) about how a subject matter measures up against criteria.',
            'Five elements: (1) a three-party relationship — practitioner, responsible party and intended users; (2) an appropriate subject matter; (3) suitable criteria (standards, laws, rules); (4) sufficient (quantity) and appropriate (quality) evidence; (5) a written assurance report in suitable form.',
            '"Practitioner" is wider than "auditor" — assurance can cover things other than historical financial information.'],
          'An assurance engagement is a referee\'s decision: two teams (responsible party and users), a match (subject matter), a rulebook (criteria), replays (evidence) and the final call (report).',
          'Assurance on a company\'s sustainability (ESG) report is an assurance engagement on non-financial information.'),
        C('c8', T8, [
            'Reasonable assurance engagements (audits) give a high level of assurance through extensive procedures. Limited assurance engagements (reviews) give a lower, moderate level through fewer procedures, but still need sufficient appropriate evidence.',
            'Engagements on matters other than historical financial information include examination of prospective financial information (forecasts, projections) and reports on controls.',
            'For prospective information, the practitioner checks that assumptions are not unreasonable, the information is properly prepared and presented, and material assumptions are disclosed — but cannot say the results will be achieved, so the assurance is moderate and negatively worded.'],
          'An audit is a full medical; a review is a quick check-up; a projection report says "your diet plan looks sensible" — not "you will lose 10 kg".',
          'Listed companies\' quarterly results are reviewed (limited assurance) while annual results are audited.',
          blocks=[assur]),
        C('c9', T9, [
            'Personal qualities: integrity, independence, tact, caution, firmness, good temper, discretion, diligence, judgement, patience, clear thinking and reliability.',
            'Professional qualities: thorough knowledge of accounting in all its branches, auditing standards, law, taxation and business — the auditor must be an expert to review others\' work critically.',
            'Because the auditor holds a position of trust, the highest integrity backed by independence matters most.'],
          'A good auditor is part detective, part diplomat and part judge.',
          'Audit firms train staff in both technical standards and soft skills like professional scepticism and communication.'),
        C('c10', T10, [
            'Engagement standards issued under the authority of the ICAI Council: SAs (audits), SREs (reviews), SAEs (other assurance), SRSs (agreed-upon procedures and compilations — no assurance).',
            'SQC 1 sets the firm\'s system of quality control for all services covered by the engagement standards, so that the firm complies with professional and legal requirements and issues appropriate reports. ICAI has issued SQM 1 and SQM 2 to replace it, but their mandatory date has been deferred; SQC 1 continues to apply until ICAI announces otherwise.',
            'Why standards: global benchmarks, better reporting quality, uniformity, professional skill and audit quality.',
            'Duty: follow the standards. If a required procedure would be ineffective in the circumstances, the practitioner performs alternative procedures, documents how they meet the aim and why he departed, and draws attention to the departure in the report — disclosure alone does not excuse non-compliance.'],
          'Engagement standards are the rulebook for each game; the quality control standard is the club\'s own training and discipline system.',
          'Peer review and NFRA inspections check whether firms actually follow the standards.',
          blocks=[stds]),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Explaining reasonable assurance to a client', 'role': 'Audit senior',
         'situation': 'A partner of a client firm complains that a small fraud by a purchase manager colluding with a supplier was not caught by last year\'s audit.',
         'steps': ['Explain that audit gives reasonable, not absolute, assurance and uses sampling.', 'Point to the inherent limitation of collusion and forged documents.', 'Recommend stronger controls (rotation, vendor checks) and note the matter for this year\'s risk assessment.'],
         'takeaway': 'Audit is not a guarantee; management remains responsible for preventing fraud.'},
        {'id': 'j2', 'title': 'Choosing the right engagement', 'role': 'Newly practising CA',
         'situation': 'A client wants a "certificate" for projections required by a bank.',
         'steps': ['Identify the engagement as assurance on prospective information under SAE 3400.', 'Check reasonableness of assumptions, preparation and disclosure.', 'Issue a moderate-assurance report — never promise the projections will be achieved.'],
         'takeaway': 'Pick the engagement and standard first; the report wording follows.'},
    ]

    mcqs = [
        Q('m1', 'Audit of financial statements provides:', ['Reasonable assurance — a high but not absolute level', 'Absolute assurance', 'Limited assurance only', 'No assurance'], 0,
          'Under SA 200 the auditor obtains reasonable assurance, which is a high level of assurance but not a guarantee, because inherent limitations such as sampling and judgement make absolute assurance impossible. Limited assurance is provided by reviews. In practice: audit reports never say the statements are "correct".', 'c3', T3),
        Q('m2', 'Responsibility for preparing financial statements lies with:', ['Management of the entity', 'The statutory auditor', 'The tax authorities', 'The bankers'], 0,
          'Management prepares and presents the financial statements and designs internal controls; the auditor only expresses an opinion on them. If the auditor prepared them, independence would be lost. In practice: the audit report itself states management\'s and the auditor\'s separate responsibilities.', 'c1', T1),
        Q('m3', 'A CA is asked to audit the proprietary business of his brother. He:', ['Should not accept, as independence is impaired by the relationship', 'May accept if the fee is reasonable', 'May accept if the business is small', 'Must accept, as a relative knows the business best'], 0,
          'Independence means the auditor\'s judgement must not be subject to anyone\'s influence. A close family relationship creates such influence, so the CA should not audit his brother\'s business. Size or fee does not cure lack of independence. In practice: firms check relationships before accepting every engagement.', 'c1', T1),
        Q('m4', 'The word "audit" comes from the Latin "audire", meaning:', ['To hear', 'To check', 'To count', 'To report'], 0,
          'Audire means to hear; in early times accounts were read aloud to auditors who listened and judged whether stewards had acted properly. The modern audit involves examining evidence rather than only hearing. In practice: inquiry, which involves listening, is still a basic audit procedure.', 'c2', T2),
        Q('m5', 'Which of these is outside the scope of a financial statement audit?', ['Authenticating whether documents are genuine', 'Checking disclosure of contingent liabilities', 'Evaluating consistency of accounting policies', 'Assessing reliability of accounting records'], 0,
          'The auditor is not an expert in authenticating documents, so determining genuineness is outside the audit scope. Disclosure, accounting policies and reliability of records are all within scope. In practice: where authenticity is doubted, a forensic expert is engaged.', 'c4', T4),
        Q('m6', 'The main difference between audit and investigation is that:', ['Audit is general and broad; investigation is special-purpose and narrow', 'Audit is optional; investigation is always mandatory', 'Audit covers future events; investigation covers past events', 'There is no difference'], 0,
          'An audit aims at an opinion on the statements as a whole, whereas an investigation is a critical examination for a specific purpose, such as checking a suspected fraud. Both deal with past events. In practice: a company may order an investigation into a particular division after a whistle-blower complaint.', 'c4', T4),
        Q('m7', 'Collusion between the storekeeper and the accountant to pass fake purchase bills is an example of:', ['An inherent limitation arising from the nature of financial reporting and internal control', 'A failure of the auditor\'s independence', 'An error in sampling', 'A future event'], 0,
          'Internal controls can be defeated when two or more people collude; this is one reason an audit cannot give absolute assurance. It does not relate to the auditor\'s independence. In practice: auditors assess fraud risk but cannot guarantee detection of well-concealed collusion.', 'c5', T5),
        Q('m8', 'The auditor cannot force management to provide information. This is a:', ['Legal limitation on obtaining audit evidence', 'Practical limitation arising from sampling', 'Limitation of financial reporting', 'Benefit of audit'], 0,
          'The auditor has no legal power to compel production of information; if it is not given, he can only report the matter. Sampling is a practical limitation of a different kind. In practice: refusal of information may lead to a modified opinion.', 'c5', T5, 'moderate'),
        Q('m9', 'In the case of a government company, the statutory auditor is appointed by:', ['The Comptroller and Auditor General of India', 'Members at the AGM', 'The Board of Directors', 'The Registrar of Companies'], 0,
          'For government companies, the CAG appoints the statutory auditor; for other companies members appoint the auditor at the AGM. The board or the Registrar do not make the regular appointment. In practice: the CAG may also conduct a supplementary audit of government companies.', 'c6', T6),
        Q('m10', 'Which is NOT a benefit of audit?', ['Audited figures can be relied on to predict future results with certainty', 'Audit acts as a moral check on employees', 'Lenders use audited statements for credit decisions', 'Audit may reveal weaknesses in controls'], 0,
          'Audit deals with historical financial information and gives no certainty about future results; future events are in fact an inherent limitation. The other options are genuine benefits. In practice: investors must still judge future prospects themselves.', 'c6', T6),
        Q('m11', 'Which is NOT an element of an assurance engagement?', ['A guarantee of future performance', 'Suitable criteria', 'A three-party relationship', 'Sufficient appropriate evidence'], 0,
          'The five elements are three parties (practitioner, responsible party, users), a proper subject matter, suitable criteria, enough reliable evidence and a written report. No assurance engagement guarantees future performance. In practice: missing criteria would make an engagement impossible to perform.', 'c7', T7),
        Q('m12', '"Sufficient" and "appropriate" evidence refer respectively to:', ['Quantity and quality', 'Quality and quantity', 'Cost and time', 'Relevance and timeliness only'], 0,
          'Sufficiency measures how much evidence is obtained, while appropriateness measures its quality — relevance and reliability. The two work together: poorer quality cannot always be offset by more quantity. In practice: external confirmations are usually more reliable than internal records.', 'c7', T7),
        Q('m13', 'A review of interim financial information is a:', ['Limited assurance engagement', 'Reasonable assurance engagement', 'Related service with no assurance', 'Investigation'], 0,
          'A review involves fewer procedures than an audit and provides a moderate (limited) level of assurance; it still requires sufficient appropriate evidence. Compilation is a related service with no assurance. In practice: quarterly results of listed companies are subject to limited review.', 'c8', T8),
        Q('m14', 'Examination of prospective financial information is governed by:', ['Standards on Assurance Engagements (SAE 3400)', 'Standards on Auditing', 'Standards on Review Engagements', 'Standards on Related Services'], 0,
          'Prospective information is not historical, so SAs and SREs do not apply; SAE 3400 deals with its examination. Related services give no assurance. In practice: projections submitted to banks for loans are examined under SAE 3400.', 'c10', T10, 'moderate'),
        Q('m15', 'A compilation engagement, where the CA only helps prepare financial statements, falls under:', ['Standards on Related Services', 'Standards on Auditing', 'Standards on Review Engagements', 'Standards on Assurance Engagements'], 0,
          'Compilation is a related service (SRS 4410) in which the practitioner assists management without providing any assurance, and the report says so. SAs, SREs and SAEs all involve assurance. In practice: many small businesses use compilation services for bank or tax purposes.', 'c10', T10),
        Q('m16', 'When an auditor cannot perform a procedure required by an SA and uses an alternative procedure, he must:', ['Document how the alternative achieves the aim and the reason for departure, and draw attention to it in the report', 'Do nothing more if satisfied', 'Withdraw from the engagement', 'Ask management to perform the procedure'], 0,
          'The practitioner documents how the alternative procedures meet the objective of the required one, records the reason for departure and draws attention to it in the report; mere disclosure does not excuse non-compliance. In practice: unanswered debtor confirmations are often replaced by checking later receipts and invoices.', 'c10', T10, 'moderate'),
        Q('m17', 'The quality control standard currently applicable to audit firms in India is:', ['SQC 1, since the mandatory date of SQM 1 and SQM 2 has been deferred', 'SQM 1, mandatory from 1 April 2025', 'SA 220 only', 'No quality standard applies'], 0,
          'ICAI issued SQM 1 and SQM 2 to replace SQC 1, but in March 2026 deferred their mandatory date until further announcement, so SQC 1 continues to apply. SA 220 deals with quality at the engagement level. In practice: firms may adopt SQM 1 early but are not required to.', 'c10', T10, 'moderate'),
    ]

    questions = [
        W('q1', 5, 'Explain the inherent limitations of an audit.',
          [limits, p('Because of these limitations, an auditor cannot obtain absolute assurance; the assurance is reasonable — high but not a guarantee.')],
          [S('s1', 'Nature of financial reporting — judgement, control override', 1, 'concept', 'judgement|judgment|estimate|collusion|override'),
           S('s2', 'Nature of audit procedures — sampling, no power to compel, fraud schemes', 1.5, 'concept', 'sampl|test', 'force|compel|power|fraud|forged|fake', n=1),
           S('s3', 'Not an investigation', 1, 'concept', 'not an investigation|not investigation|not an official'),
           S('s4', 'Timeliness vs cost', 0.75, 'concept', 'timel|relevance|cost'),
           S('s5', 'Future events', 0.75, 'concept', 'future')],
          ['Group the points under the five SA 200 headings.'], ['Listing benefits instead of limitations.'], ['Use a two-column table with examples.'], pad='table'),
        W('q2', 4, 'Distinguish between a reasonable assurance engagement and a limited assurance engagement, with examples.',
          [assur],
          [S('s1', 'Level of assurance', 1, 'concept', 'high', 'moderate|lower|limited'),
           S('s2', 'Extent of procedures', 1, 'concept', 'procedure', 'extensive|fewer|elaborate'),
           S('s3', 'Nature of conclusion', 1, 'concept', 'opinion|conclusion'),
           S('s4', 'Examples — audit vs review', 1, 'application', 'audit', 'review')],
          ['Four rows, each contrasted, earn full marks.'], ['Saying a review needs no evidence.'], ['Use a table.'], pad='table'),
        W('q3', 4, 'Shiv Traders, a partnership, wants its CA to (a) certify the remaining life of its old boiler and (b) disclose in the accounts a pending legal claim against it. Comment on whether each falls within the scope of audit.',
          [legal('Scope of audit (as explained in the ICAI study material / SA 200)', 'The CA is asked to certify the technical life of a boiler and to consider disclosure of a pending legal claim.',
                 'Judging the physical condition or remaining life of machinery needs an engineer\'s expertise and is outside the auditor\'s competence; the auditor may use an expert\'s work but does not certify it himself. Proper disclosure of contingent liabilities is part of the auditor\'s responsibility for checking disclosure.',
                 '(a) Outside the scope of audit; (b) within the scope — the auditor should ensure appropriate disclosure.')],
          [S('s1', 'Boiler life — outside scope, needs engineer/expert', 2, 'application', 'outside|not within|beyond', 'engineer|expert|competence', n=2),
           S('s2', 'Legal claim disclosure — within scope', 2, 'application', 'within scope|within the scope|part of', 'disclos')],
          ['State the principle, apply it, conclude.'], ['Treating every request from the client as audit work.'], ['Use provision–facts–analysis–conclusion.']),
    ]

    viva = [
        V('v1', 'What are the overall objectives of the auditor under SA 200?',
          'To obtain reasonable assurance that the statements taken as a whole contain no material misstatement due to fraud or error so that an opinion can be expressed, and to report and communicate as required by the SAs.',
          [P('p1', 'Reasonable assurance', 3, 'reasonable assurance'), P('p2', 'Free from material misstatement — fraud or error', 4, 'no material misstatement|free from material|free of material', 'fraud|error'), P('p3', 'Report and communicate', 3, 'report|communicat')], 'c3'),
        V('v2', 'Why can an audit never give absolute assurance?',
          'Because of inherent limitations: management judgement in reporting, sampling and lack of power to compel information, fraud with forged documents or collusion, audit not being an investigation, and the need to balance time and cost.',
          [P('p1', 'Inherent limitations', 3, 'inherent|limitation'), P('p2', 'Sampling / procedures', 3, 'sampl|procedure|compel|power'), P('p3', 'Fraud, collusion or forgery', 2, 'fraud|collusion|forg'), P('p4', 'Judgement / not investigation / cost', 2, 'judgement|judgment|investigation|cost')], 'c5'),
        V('v3', 'Name the elements of an assurance engagement.',
          'There must be three parties, namely the practitioner, the responsible party and intended users; a subject matter; suitable criteria; enough sufficient and appropriate evidence; and finally a written report.',
          [P('p1', 'Three-party relationship', 2, 'three party|three-party|practitioner'), P('p2', 'Subject matter', 2, 'subject matter'), P('p3', 'Suitable criteria', 2, 'criteria'), P('p4', 'Sufficient appropriate evidence', 2, 'evidence'), P('p5', 'Written report', 2, 'report')], 'c7'),
        V('v4', 'Who appoints the auditor of a company and of a government company?',
          'In a company the members appoint the auditor at the annual general meeting. In a government company the Comptroller and Auditor General of India appoints the auditor.',
          [P('p1', 'Members at AGM', 5, 'member|shareholder', 'agm|annual general meeting|general meeting'), P('p2', 'C&AG for government companies', 5, 'comptroller|cag|c&ag')], 'c6'),
        V('v5', 'Which standards apply to a compilation engagement, and does it give assurance?',
          'Standards on Related Services apply, specifically SRS 4410. A compilation gives no assurance and the report says so.',
          [P('p1', 'Standards on Related Services / SRS 4410', 6, 'related service|srs 4410|srs'), P('p2', 'No assurance', 4, 'no assurance|without assurance|does not provide assurance|not an assurance')], 'c10'),
    ]

    cases = [{'id': 'k1', 'title': 'Questions at Malabar Spices Ltd.', 'difficulty': 'moderate',
              'case': 'Malabar Spices Ltd.\'s auditors issued a clean report. Months later, an investor complained that the share price fell after the company lost a major export contract. The company had also hidden a small fraud by producing forged supplier invoices to the auditors. The bank now wants the half-yearly results reviewed and a report on next year\'s projections.',
              'mcqs': [
                  M('k1a', 'The investor\'s complaint about the fall in share price after losing a contract:', ['Is misplaced — an audit does not assure future performance', 'Shows the auditor was negligent', 'Means the audit report must be withdrawn', 'Shows the audit was a limited review'], 0,
                    'Audit covers historical financial information and provides no assurance about future events, which are an inherent limitation. A later business loss does not by itself show audit failure. In practice: investors must judge future prospects themselves.', 'core', topic=T5),
                  M('k1b', 'The forged supplier invoices that misled the auditors illustrate:', ['An inherent limitation — the auditor is not an expert in authenticating documents', 'Lack of independence', 'A limited assurance engagement', 'An error in the engagement letter'], 0,
                    'Management fraud using forged documents can deceive an auditor who is not a document expert; this is an inherent limitation of audit procedures. It does not by itself indicate the auditor lacked independence. In practice: auditors stay alert to signs of forgery and use confirmations.', 'moderate', topic=T5),
                  M('k1c', 'Review of the half-yearly results is a:', ['Limited assurance engagement under Standards on Review Engagements', 'Reasonable assurance engagement under SAs', 'Related service', 'Investigation'], 0,
                    'A review provides limited (moderate) assurance with fewer procedures and is performed under SREs, such as SRE 2410 when done by the entity\'s auditor. An audit would be under SAs. In practice: reviews rely mainly on enquiry and analytical procedures.', 'core', topic=T8),
                  M('k1d', 'For next year\'s projections, the CA:', ['Reports on reasonableness of assumptions, preparation and disclosure, without assuring results will be achieved', 'Certifies that the projections will be met', 'Performs a compilation only', 'Cannot issue any report'], 0,
                    'Under SAE 3400, the practitioner gives moderate assurance that assumptions are not unreasonable and the information is properly prepared and disclosed; he cannot assure future results. In practice: the report states that actual results may differ.', 'moderate', topic=T10),
              ]}]

    return unit(UID, 'p5', 'int-p5-ch01', 1, 'Nature, Objective and Scope of Audit',
                ['Explain the meaning, nature, origin and interdisciplinary character of audit.',
                 'State the auditor\'s objectives under SA 200 and explain reasonable assurance.',
                 'Identify what falls within and outside the scope of audit and the inherent limitations.',
                 'Explain benefits of audit, who appoints the auditor and to whom the report goes.',
                 'Describe assurance engagements, the reasonable/limited distinction and the engagement and quality control standards.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 30}, 'prereq': [],
                 'exam_tip': 'Case-based MCQs test scope, limitations and the type of engagement; descriptive questions ask for limitations or reasonable vs limited assurance.'},
                concepts, illus, jobs, mcqs, questions,
                {'summary': ['Audit = independent examination of financial information to express an opinion.', 'SA 200 objectives: reasonable assurance + reporting.',
                             'Scope: all relevant aspects, reliability of records, proper disclosure — not preparation, expert matters, authentication or investigation.',
                             'Inherent limitations: reporting judgement, procedures, not investigation, time vs cost, future events.',
                             'Assurance engagement: 3 parties, subject matter, criteria, evidence, report.', 'Audit = reasonable; review = limited; projections = moderate on assumptions.',
                             'Standards: SA, SRE, SAE, SRS + SQC 1.'],
                 'remember': ['Sufficient = quantity; appropriate = quality.', 'SQC 1 still applies; SQM 1/2 deferred.'],
                 'traps': ['Reasonable assurance is high, not moderate.', 'Compilation gives no assurance.']},
                [('Audit gives', 'Reasonable (high, not absolute) assurance'), ('Review gives', 'Limited (moderate) assurance'), ('Projections', 'SAE 3400'),
                 ('Compilation', 'SRS 4410 — no assurance'), ('Govt. company auditor', 'Appointed by C&AG')],
                viva, cases,
                topics=['Introduction', 'Origin of Auditing', 'Meaning and Nature of Auditing', 'Interdisciplinary Nature of Auditing', 'Objectives of Audit', 'Scope of Audit',
                        'Inherent Limitations of Audit', 'What is an Engagement?', 'Benefits of Audit', 'Audit — Mandatory or Voluntary?', 'Who Appoints an Auditor?',
                        'To Whom Report is Submitted', 'Meaning of Assurance Engagement', 'Qualities of Auditor', 'Engagement and Quality Control Standards'])
