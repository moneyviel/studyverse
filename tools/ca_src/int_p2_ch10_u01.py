"""CA Intermediate · Paper 2 Corporate and Other Laws · Chapter 10 Audit and Auditors (ss. 139–148).
Scope follows the ICAI study material (with amendments to June 2026); provisions are explained in original words; examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p2-ch10-u01'
T1 = 'Appointment of auditors and rotation (s. 139)'
T2 = 'Removal, resignation and special notice (s. 140)'
T3 = 'Eligibility, qualifications and disqualifications (s. 141)'
T4 = 'Remuneration, powers, duties and fraud reporting (ss. 142–143)'
T5 = 'Prohibited services, signing, attendance, punishment and cost audit (ss. 144–148)'


def build():
    ck = Checks()
    t1 = ck.add('5', 'Years in one term')
    firm = ck.add('2*5', 'Maximum consecutive years for an audit firm')
    cool = ck.add('5', 'Cooling-off period (years)')
    i1 = {'id': 'i1', 'title': 'How long can the firm stay?', 'difficulty': 'core', 'minutes': 7,
          'q': 'Sarthak Ltd. (unlisted public; paid-up capital ₹15 crore) appointed audit firm Mehta & Co. at its AGM in 2016 and reappointed it in 2021. It also appointed individual auditor CA Rina in another group company (same class) in 2021. Can Mehta & Co. be reappointed in 2026? Can CA Rina be reappointed in 2026?',
          'solution': [table(['Auditor', 'Rule', 'Answer'], [
              ['Mehta & Co. (firm)', f'At most two terms of {R(t1)} years = {R(firm)} consecutive years', f'No — completed 10 years; eligible again only after a {R(cool)}-year cooling-off'],
              ['CA Rina (individual)', f'At most one term of {R(t1)} consecutive years', f'No — must wait {R(cool)} years']], title='Rotation under section 139(2)'),
              note('Rotation applies to listed companies, unlisted public companies with paid-up capital of ₹10 crore or more, private companies with paid-up capital of ₹50 crore or more, and companies with borrowings of ₹50 crore or more.')],
          'checks': list(ck)}

    concepts = [
        C('c1', T1, [
            'First auditor (non-government company): appointed by the Board within 30 days of registration; if the Board fails, members appoint at an EGM within 90 days. The first auditor holds office till the first AGM.',
            'Subsequent auditors are appointed by members at the first AGM for a term from that AGM till the sixth AGM, with written consent and a certificate of eligibility; the company files ADT-1 within 15 days.',
            'Rotation: for listed companies and prescribed classes (unlisted public with paid-up capital ₹10 crore+, private with paid-up capital ₹50 crore+, or any company with borrowings ₹50 crore+), an individual auditor may serve one term of five consecutive years and a firm two terms of five years; then a five-year cooling-off period follows.',
            'Government companies: the Comptroller and Auditor-General appoints the auditor (first auditor within 60 days of registration; subsequent ones within 180 days of the start of the financial year).',
            'Casual vacancy: filled by the Board within 30 days; if caused by resignation, the appointment is also approved by members within three months, and the appointee holds office till the next AGM.'],
          'Members appoint auditors for five-year terms; rotation prevents over-long relationships.',
          'A firm auditing a listed company for ten years must step away for five.'),
        C('c2', T2, [
            'Section 140(1): an auditor may be removed before the end of the term only by a special resolution after prior approval of the Central Government, and after a reasonable opportunity of being heard.',
            'Section 140(2): an auditor who resigns files ADT-3 with the company and the Registrar within 30 days, stating reasons and any other relevant facts.',
            'Section 140(4): special notice is needed for a resolution appointing someone other than the retiring auditor or providing that the retiring auditor shall not be reappointed; the retiring auditor may make written representations to be circulated to members.',
            'Section 140(5): the Tribunal may order a change of auditor if it is satisfied that the auditor has acted fraudulently or abetted fraud; such an auditor cannot be appointed in any company for five years.'],
          'Removing an auditor mid-term is deliberately difficult.',
          'A company unhappy with its auditor mid-term needs the Central Government\'s prior approval and a special resolution.'),
        C('c3', T3, [
            'Only a chartered accountant may be auditor; a firm or LLP may be appointed if a majority of its partners in India are practising chartered accountants, and only those partners may sign.',
            'Disqualified: a body corporate (other than an LLP); an officer or employee of the company; a partner or employee of an officer or employee; a person who, or whose relative or partner, holds securities or interest in the company or its group (a relative may hold up to ₹1 lakh face value); a person indebted to the company or group above ₹5 lakh, or who has given a guarantee for a third party\'s debt above ₹1 lakh; one with a business relationship with the company; one whose relative is a director or KMP; one in full-time employment elsewhere; one holding audits of more than 20 companies (excluding OPCs, dormant, small and private companies with paid-up capital below ₹100 crore); one convicted of fraud within the last ten years; and one providing prohibited services under section 144.',
            'An auditor who becomes disqualified after appointment vacates office, creating a casual vacancy.'],
          'Independence is protected by a long list of financial and personal bars.',
          'An auditor whose wife becomes a director of the company must vacate office.'),
        C('c4', T4, [
            'Section 142: remuneration is fixed by the company in general meeting (the Board may fix it for the first auditor), including expenses.',
            'Section 143: the auditor has a right of access to books and vouchers at all times and to information and explanations from officers. He reports to members on whether the accounts give a true and fair view, with matters such as adequacy of records, branch audits, internal financial controls, pending litigation, and CARO matters for prescribed companies.',
            'Fraud reporting: if the auditor believes a fraud of ₹1 crore or more is being committed against the company by officers or employees, he reports to the Central Government electronically in Form ADT-4 (after seeking the Board\'s or Audit Committee\'s reply); smaller frauds are reported to the Audit Committee or Board and disclosed in the Board\'s report. Failure attracts a penalty of ₹5 lakh (listed) or ₹1 lakh (others).'],
          'The auditor can see everything, must report fully, and must blow the whistle on large frauds.',
          'A ₹2 crore fraud by an employee is reported to the Central Government in ADT-4.'),
        C('c5', T5, [
            'Section 144: the auditor cannot provide accounting and book-keeping, internal audit, design and implementation of financial information systems, actuarial, investment advisory, investment banking, outsourced financial services or management services to the company, its holding or subsidiary — directly or through relatives or associated entities.',
            'Section 145: the auditor signs the report; qualifications that adversely affect the company\'s functioning are read before the general meeting.',
            'Section 146: auditors receive notices of general meetings and attend (personally or through an authorised CA) unless exempted, with the right to be heard on matters concerning them.',
            'Section 147: contravention attracts fines on the company and officers, and on auditors (fines and, if wilful with intent to deceive, imprisonment up to one year); the auditor refunds remuneration and pays damages for misleading statements.',
            'Section 148: the Central Government may require cost records and cost audit for prescribed companies; the cost auditor is appointed by the Board on the Audit Committee\'s recommendation, and the statutory auditor cannot be the cost auditor.'],
          'Independence also means not selling the company other services that the auditor would later check.',
          'An audit firm cannot also run the company\'s payroll outsourcing.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Auditor appointment check', 'role': 'Secretarial associate',
             'situation': 'The company proposes a new audit firm at its AGM after the old firm completed ten years.',
             'steps': ['Check rotation and cooling-off for both firms.', 'Obtain consent and eligibility certificate.', 'Issue special notice as the retiring auditor is not reappointed.', 'File ADT-1 within 15 days of the AGM.'],
             'takeaway': 'Eligibility, rotation and filings must all line up.'}]

    mcqs = [
        Q('m1', 'The first auditor of a non-government company is appointed by the Board within:', ['30 days of registration', '90 days', '60 days', '15 days'], 0,
          'Section 139(6) requires the Board to appoint the first auditor within thirty days of registration; if it fails, members appoint at an EGM within ninety days. In practice: diarise from the incorporation date.', 'c1', T1, 'core', check=30),
        Q('m2', 'An auditor appointed at an AGM holds office until:', ['The conclusion of the sixth AGM from then', 'The next AGM', 'Ten years', 'Removal'], 0,
          'Section 139(1) provides appointment from the conclusion of that AGM till the conclusion of the sixth AGM, i.e. a five-year term. In practice: file ADT-1 within 15 days.', 'c1', T1),
        Q('m3', 'Under rotation, an audit firm may be appointed for at most:', ['Two terms of five consecutive years', 'One term of five years', 'Three terms', 'No limit'], 0,
          'Firms may serve two terms of five consecutive years (ten years) and individuals one term of five; then a five-year cooling-off applies. In practice: plan succession early.', 'c1', T1),
        Q('m4', 'Removal of an auditor before the expiry of the term requires:', ['A special resolution with prior approval of the Central Government', 'A Board resolution', 'An ordinary resolution', 'Tribunal order only'], 0,
          'Section 140(1) needs a special resolution after obtaining the Central Government\'s prior approval, and the auditor must be given a reasonable opportunity of being heard. In practice: apply in the prescribed form.', 'c2', T2),
        Q('m5', 'A resigning auditor files Form ADT-3 within:', ['30 days of resignation', '7 days', '60 days', '15 days'], 0,
          'Section 140(2) requires the resigning auditor to file a statement in ADT-3 with the company and the Registrar within thirty days, giving reasons. In practice: be specific about reasons.', 'c2', T2, 'core', check=30),
        Q('m6', 'An auditor is disqualified if indebted to the company for more than:', ['₹5 lakh', '₹1 lakh', '₹10 lakh', '₹50,000'], 0,
          'Section 141(3)(d) and rule 10 disqualify a person (or relative or partner) indebted to the company or its group above ₹5 lakh; guarantees for third-party debt above ₹1 lakh also disqualify. In practice: check personal loans.', 'c3', T3, 'core', check=5),
        Q('m7', 'The ceiling of 20 company audits excludes:', ['Small companies and one person companies', 'All public companies', 'Listed companies', 'Government companies'], 0,
          'The count of 20 leaves out small, dormant and one person companies, as well as private companies whose paid-up capital is under ₹100 crore. In practice: count only the rest.', 'c3', T3),
        Q('m8', 'An auditor must report a suspected fraud to the Central Government if the amount involved is at least:', ['₹1 crore', '₹50 lakh', '₹10 crore', '₹5 crore'], 0,
          'Frauds of ₹1 crore or more are reported to the Central Government electronically in ADT-4; smaller ones to the Audit Committee or Board, with disclosure in the Board\'s report. In practice: follow the prescribed timeline.', 'c4', T4, 'core', check=1),
        Q('m9', 'Which service can the statutory auditor NOT provide to the company?', ['Internal audit', 'Tax representation', 'Certification work', 'Statutory audit of the subsidiary'], 0,
          'Section 144 prohibits internal audit, accounting, financial information systems design, actuarial, investment advisory and banking, outsourced financial and management services. Tax and certification are not barred if approved. In practice: get Board approval for allowed services.', 'c5', T5),
        Q('m10', 'The cost auditor of a company is appointed by:', ['The Board on the Audit Committee\'s recommendation', 'Members at the AGM', 'The statutory auditor', 'The Central Government'], 0,
          'Under section 148 and the rules, the Board appoints the cost auditor on the Audit Committee\'s recommendation; members ratify remuneration. The statutory auditor cannot be the cost auditor. In practice: file the appointment.', 'c5', T5),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Firm term limit', 2, 'application', 'two terms|10', nums=[firm]),
           S('s2', 'Individual limit and cooling off', 2, 'application', 'cooling|one term')],
          ['Identify the class first.'], ['Applying the individual limit to firms.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, 'CA Arun is proposed as auditor of Kesar Ltd. His brother holds shares of Kesar Ltd. with face value ₹1,00,000. Arun owes Kesar ₹4,00,000 on a car loan. He already audits 18 public companies and 5 small companies. Advise.',
          [legal('Section 141(3) and rule 10',
                 'Relative holds shares of face value ₹1,00,000; auditor owes ₹4,00,000; audits 18 public and 5 small companies.',
                 'A relative may hold securities of face value up to ₹1 lakh without disqualifying the auditor. Indebtedness disqualifies only above ₹5 lakh. The 20-company count leaves out small, dormant and one person companies and private companies with paid-up capital under ₹100 crore.',
                 'Arun is not disqualified: the holding is within ₹1 lakh, the debt is below ₹5 lakh, and his count would be 19 companies.')],
          [S('s1', 'Relative holding ₹1 lakh', 1.5, 'application', '1 lakh'),
           S('s2', 'Indebtedness ₹5 lakh', 1.5, 'application', '5 lakh'),
           S('s3', '20-company limit exclusions', 1, 'application', '20|small'),
           S('s4', 'Conclusion', 1, 'conclusion', 'not disqualified')],
          ['Test each limit.'], ['Counting small companies.'], ['Provision → facts → analysis → conclusion.']),
    ]

    viva = [
        V('v1', 'Who appoints the first auditor of a non-government company?', 'The Board within 30 days of registration; failing which, members at an EGM within 90 days.',
          [P('p1', 'Board within 30 days', 6, 'board', '30'), P('p2', 'Members within 90 days', 4, '90|members')], 'c1'),
        V('v2', 'What is the cooling-off period under rotation?', 'Five years, during which an individual or firm that has completed its term must stay away before any reappointment in the same company.',
          [P('p1', 'Five years', 6, 'five|5'), P('p2', 'Stay away', 4, 'stay away|reappoint')], 'c1'),
        V('v3', 'How can an auditor be removed before the term ends?', 'By special resolution after prior approval of the Central Government, with a reasonable opportunity of being heard.',
          [P('p1', 'Special resolution', 5, 'special resolution'), P('p2', 'Central Government approval', 5, 'central government')], 'c2'),
        V('v4', 'Name three services the auditor cannot provide.', 'Accounting and book-keeping, internal audit, design of financial information systems, actuarial, investment advisory or banking, outsourced financial and management services.',
          [P('p1', 'Accounting or internal audit', 5, 'accounting|internal audit'), P('p2', 'Others', 5, 'actuarial|investment|management|outsourced|information')], 'c5'),
        V('v5', 'What must an auditor do on suspecting a fraud of ₹2 crore?', 'Report it to the Central Government in Form ADT-4 after seeking the Board\'s or Audit Committee\'s response.',
          [P('p1', 'Central Government', 6, 'central government'), P('p2', 'ADT-4', 4, 'adt-4|adt 4')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Vishal Infra Ltd.', 'difficulty': 'moderate',
              'case': 'Vishal Infra Ltd. (listed) had a casual vacancy because its auditor resigned on 1 June. The Board appointed a new firm on 20 June. The company also wants the new firm to design its ERP-based financial information system.',
              'mcqs': [
                  M('k1a', 'The Board\'s appointment on 20 June is:', ['Valid, but must be approved by members within three months', 'Invalid without CAG approval', 'Valid till the sixth AGM', 'Valid only if Tribunal agrees'], 0,
                    'A casual vacancy is filled by the Board within 30 days; where it arises from resignation, members must approve the appointment in a general meeting within three months, and the appointee holds office till the next AGM. In practice: call an EGM if needed.', 'moderate', topic=T1),
                  M('k1b', 'Designing the ERP financial information system is:', ['A prohibited service under section 144', 'Allowed with Board approval', 'Allowed if billed separately', 'Allowed for listed companies'], 0,
                    'Design and implementation of any financial information system is barred for the statutory auditor, directly or indirectly. In practice: engage another firm.', 'core', topic=T5),
                  M('k1c', 'The resigning auditor must file ADT-3 within:', ['30 days of resignation', '7 days', '60 days', '3 months'], 0,
                    'Section 140(2) requires the resigning auditor to file ADT-3 with the company and Registrar within thirty days, stating reasons. In practice: reasons should be specific.', 'core', check=30, topic=T2),
              ]}]

    return unit(UID, 'p2', 'int-p2-ch10', 1, 'Audit and Auditors',
                ['Apply the rules on appointment, rotation and casual vacancies.',
                 'Explain removal and resignation of auditors.',
                 'Apply eligibility and disqualification provisions.',
                 'Explain auditors\' powers, duties, fraud reporting, prohibited services and cost audit.'],
                {'difficulty': 'core', 'minutes': {'learn': 55, 'practice': 35}, 'prereq': ['int-p2-ch09-u01'],
                 'exam_tip': 'Numbers to know: 30/90 days (first auditor), 15 days (ADT-1), 5 years term, 10 years firm, 5 years cooling, ₹1 lakh / ₹5 lakh, 20 companies, ₹1 crore fraud.'},
                concepts, [i1], jobs, mcqs, questions,
                {'summary': ['First auditor: Board in 30 days or members in 90 days; then AGM to sixth AGM.',
                             'Rotation: individual 5 years, firm 10 years; 5-year cooling-off.', 'Government companies: CAG appoints.',
                             'Removal: special resolution + CG approval; resignation: ADT-3 in 30 days.', 'Disqualifications incl. ₹1 lakh securities, ₹5 lakh debt, 20 audits.',
                             'Fraud ≥ ₹1 crore → CG in ADT-4; prohibited services under s. 144; cost auditor by Board.'],
                 'remember': ['Small companies and OPCs do not count towards 20 audits.'],
                 'traps': ['Casual vacancy from resignation needs members\' approval within 3 months.']},
                [('Term', '5 years (AGM to 6th AGM)'), ('Rotation', 'Individual 5 · Firm 10 · Cooling 5'), ('Fraud report', '≥ ₹1 crore → CG'), ('Audit limit', '20 companies')],
                viva, cases)
