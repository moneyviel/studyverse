"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 11 Accounts and Records.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch11-u01'
T1 = 'Accounts to be kept (s. 35 and Rule 56)'
T2 = 'Electronic records, place of keeping and special persons'
T3 = 'Retention period (s. 36) and consequences of failure'


def build():
    i1 = {'id': 'i1', 'title': 'How long to keep the books?', 'difficulty': 'core', 'minutes': 5,
          'q': 'Rhea Traders must file its annual return for FY 2026-27 by 31 December 2027. Till when must it keep records for FY 2026-27? What if an appeal for that year is decided on 15 March 2034?',
          'solution': [table(['Situation', 'Keep until', 'Reason'], [
              ['Normal case', '31 December 2033', '72 months from the due date of the annual return'],
              ['Appeal pending', '31 December 2033 or one year after the appeal is decided (15 March 2035), whichever is later — so 15 March 2035', 'Section 36 proviso']], title='Section 36')],
          'checks': []}

    ck = Checks()
    m = ck.add('72/12', '72 months expressed in years')
    i2 = {'id': 'i2', 'title': 'Unaccounted stock found', 'difficulty': 'moderate', 'minutes': 5,
          'q': 'During an inspection, an officer finds goods worth ₹4,00,000 in Rhea\'s godown that are not recorded in its stock register. What is the consequence, and for how many years must Rhea generally retain records?',
          'solution': [table(['Point', 'Answer'], [
              ['Consequence', 'Under section 35(6), the officer may determine tax on the unaccounted goods as if they had been supplied, under sections 73 or 74'],
              ['Retention', '72 months = ' + str(int(m)) + ' years from the annual return due date']], title='Sections 35 and 36')],
          'checks': list(ck)}

    concepts = [
        C('c1', T1, [
            'Section 35(1): every registered person keeps, at the principal place of business named in the registration, a true and correct account of production or manufacture of goods, inward and outward supplies, stock of goods, ITC availed, output tax payable and paid, and other prescribed particulars.',
            'Where there is more than one place of business, accounts relating to each place are kept there too.',
            'Rule 56: separate records for goods received and supplied, advances received and adjusted, tax payable under reverse charge, names and addresses of suppliers and customers, and complete stock records (opening balance, receipts, supplies, goods lost, stolen, destroyed, written off or given as free samples, closing balance).',
            'Manufacturers keep monthly production accounts; service providers keep accounts of goods used in providing services and services supplied; works contractors keep project-wise details.'],
          'The law asks for a complete trail from what comes in, through what is made, to what goes out.',
          'A bakery records flour received, bread produced, bread sold, and bread thrown away at day-end.'),
        C('c2', T2, [
            'Accounts may be kept electronically, with backups and the ability to produce them in hard copy or electronic form when required. Any entry must not be erased or overwritten; corrections are made by striking out with attestation, and electronic changes leave an audit trail.',
            'An agent keeps records of authorisation, goods or services received and supplied on behalf of each principal, and tax paid. Owners or operators of warehouses and godowns and transporters must keep records of consignor, consignee and goods, whether or not registered, and may enrol on the common portal.',
            'Documents found at an unregistered place of business are presumed to belong to the registered person unless he proves otherwise.'],
          'Records can be paper or digital, but they must be original, complete and traceable.',
          'A cloud accounting system that keeps an edit log meets the electronic-records requirement.'),
        C('c3', T3, [
            'Section 36: books and records are kept for 72 months from the due date of the annual return for the year to which they relate.',
            'If the person is a party to an appeal, revision or other proceeding, or is under investigation, records relating to it are kept for one year after its final disposal or the 72-month period, whichever is later.',
            'Section 35(6): if accounts are not kept as required, the proper officer may treat unaccounted goods or services as supplied and determine tax on them under section 73 or 74. Under-reported or missing records also attract penalties.'],
          'Six years after the annual return is the minimum life of GST records — longer if a dispute is open.',
          'Records for a year whose annual return was due on 31 December 2027 are kept at least until 31 December 2033.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Record-keeping health check', 'role': 'Article assistant',
             'situation': 'A client keeps purchase bills in a cupboard and stock records only in Excel without logs.',
             'steps': ['List required registers under Rule 56.', 'Move to software with an audit trail.', 'Keep copies at each place of business.', 'Set a retention schedule linked to annual return dates.'],
             'takeaway': 'An audit trail is the electronic equivalent of not erasing entries.'}]

    mcqs = [
        Q('m1', 'GST accounts must be kept at:', ['The principal place of business, and the relevant records at each other place', 'The CA\'s office', 'Any place the person chooses', 'The bank'], 0,
          'Section 35(1) requires them at the principal place, with records for each additional place kept there. In practice: electronic access can satisfy this.', 'c1', T1),
        Q('m2', 'Records must ordinarily be retained for:', ['72 months from the due date of the annual return', 'Six years from the end of the financial year', 'Five years from the invoice date', 'Eight years from registration'], 0,
          'Section 36 counts 72 months from the annual return due date. In practice: proceedings can extend it.', 'c3', T3, check=72),
        Q('m3', 'Corrections in accounts must be made:', ['By striking out and attesting, without erasing', 'By erasing and rewriting', 'With correction fluid', 'Only at year end'], 0,
          'Rule 56 bans erasure or overwriting; electronic records keep an audit trail. In practice: track all edits.', 'c2', T2),
        Q('m4', 'Which person must keep records even if unregistered?', ['A warehouse owner storing goods for others', 'A salaried employee', 'A farmer', 'A consumer'], 0,
          'Warehouse and godown owners and transporters keep records of goods and consignors whether or not registered. In practice: they may enrol on the portal.', 'c2', T2),
        Q('m5', 'If goods are found unaccounted, the officer may:', ['Treat them as supplied and determine tax', 'Only warn the person', 'Seize the bank account automatically', 'Cancel registration immediately'], 0,
          'Section 35(6) allows tax to be determined as if the goods were supplied, under section 73 or 74. In practice: keep stock records updated.', 'c3', T3),
        Q('m6', 'Stock records under Rule 56 must include goods:', ['Lost, stolen, destroyed, written off or given as free samples', 'Ordered but not yet received', 'Of competitors', 'Held by customers'], 0,
          'The stock account shows opening stock, receipts, supplies, these losses and closing stock. In practice: such losses also need ITC reversal.', 'c1', T1),
        Q('m7', 'Under appeal, records are kept for:', ['One year after final disposal or 72 months, whichever is later', 'Only 72 months', 'Until the appeal is filed', 'Permanently'], 0,
          'The proviso to section 36 extends the period. In practice: tag disputed years in the archive.', 'c3', T3),
        Q('m8', 'An agent must keep records of:', ['Authorisations and goods or services handled for each principal', 'Only his own commission', 'Nothing', 'His personal expenses'], 0,
          'Rule 56 requires agents to keep principal-wise details, including tax paid. In practice: these support the principal\'s returns.', 'c2', T2),
    ]

    questions = [
        W('q1', 3, i1['q'], i1['solution'],
          [S('s1', 'Normal period', 1, 'concept', '72 months|2033'), S('s2', 'Appeal rule', 1, 'concept', 'later|one year'), S('s3', 'Date', 1, 'concept', '2035')],
          ['Count from the annual return due date.'], ['Counting from the year end.'], ['Table.'], pad='table'),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Section 35(6)', 2, 'concept', '35(6)|supplied'), S('s2', 'Retention', 1, 'computation', '72', nums=[m])],
          ['Name the section.'], ['Saying records may be destroyed after 3 years.'], ['Table.'], pad='table', checks=list(ck)),
    ]

    viva = [
        V('v1', 'What accounts does section 35 require?', 'Production or manufacture, inward and outward supplies, stock, input tax credit availed, output tax payable and paid, and other prescribed details.',
          [P('p1', 'Supplies and stock', 5, 'supplies|stock'), P('p2', 'Credit and tax', 5, 'credit|output tax')], 'c1'),
        V('v2', 'How long are records retained?', 'For 72 months from the due date of the annual return, extended to one year after disposal of any pending proceeding if that is later.',
          [P('p1', '72 months', 6, '72'), P('p2', 'Proceedings', 4, 'appeal|proceeding|disposal')], 'c3'),
        V('v3', 'Can records be electronic?', 'Yes, records may be kept in electronic form if backed up, producible on demand and with an audit trail of changes.',
          [P('p1', 'Electronic allowed', 5, 'electronic'), P('p2', 'Audit trail', 5, 'audit trail|backup')], 'c2'),
        V('v4', 'Who must keep records though unregistered?', 'Owners or operators of warehouses and godowns and transporters handling goods for others.',
          [P('p1', 'Warehouses', 5, 'warehouse|godown'), P('p2', 'Transporters', 5, 'transporter')], 'c2'),
        V('v5', 'What is the effect of section 35(6)?', 'Where accounts are not kept properly, the officer may treat unaccounted goods or services as supplied and determine the tax.',
          [P('p1', 'Deemed supplied', 6, 'supplied'), P('p2', 'Tax determined', 4, 'determin')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Metro Warehousing', 'difficulty': 'core',
              'case': 'Metro Warehousing (unregistered, as it only stores exempt agricultural produce) holds goods for many traders. One trader, Kumar & Co. (registered), keeps its stock register in software without edit logs and has an appeal pending for FY 2025-26.',
              'mcqs': [
                  M('k1a', 'Must Metro keep records?', ['Yes, of consignors, consignees and goods', 'No, being unregistered', 'Only if turnover exceeds ₹20 lakh', 'Only for taxable goods'], 0,
                    'Warehouse owners must keep such records whether or not registered. In practice: enrol on the portal if required.', 'core', topic=T2),
                  M('k1b', 'Kumar\'s software without edit logs:', ['Does not meet the audit-trail requirement', 'Is fully compliant', 'Is better than paper', 'Is optional'], 0,
                    'Electronic records must show changes through an audit trail. In practice: enable logs.', 'core', topic=T2),
                  M('k1c', 'Kumar must keep FY 2025-26 records until:', ['The later of 72 months from the annual return due date and one year after the appeal is decided', '72 months only', 'Appeal filing', '3 years'], 0,
                    'Section 36 extends retention for years under appeal. In practice: archive separately.', 'moderate', topic=T3),
                  M('k1d', 'If Kumar\'s stock is found short of records:', ['Tax may be determined as if the goods were supplied', 'Nothing happens', 'Only interest applies', 'Registration is automatically cancelled'], 0,
                    'Section 35(6) applies to goods not accounted for. In practice: reconcile stock monthly.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch11', 1, 'Accounts and Records',
                ['List the accounts and records to be maintained and where.',
                 'Apply rules for electronic records and special persons.',
                 'Determine the retention period and consequences of non-maintenance.'],
                {'difficulty': 'core', 'minutes': {'learn': 20, 'practice': 15}, 'prereq': ['int-p3-b-ch10-u01'],
                 'exam_tip': 'Retention period questions turn on the annual return due date — write it first.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['s. 35: production, supplies, stock, ITC, output tax — at principal place and each place.',
                             'Rule 56: no erasure; electronic with audit trail; agents, warehouses, transporters.',
                             's. 36: 72 months from annual return due date; longer if proceedings.',
                             's. 35(6): unaccounted goods treated as supplied.'],
                 'remember': ['Warehouse owners keep records even if unregistered.'],
                 'traps': ['72 months run from annual return due date, not year end.']},
                [('Retention', '72 months'), ('Proceedings', '+1 year after disposal'), ('Unaccounted goods', 's. 35(6)')],
                viva, cases)
