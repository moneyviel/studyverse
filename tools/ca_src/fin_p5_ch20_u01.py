"""CA Final · Paper 5 · Chapter 20 Liability to Pay in Certain Cases.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch20-u01'
T1 = 'Transfer of business and agents'
T2 = 'Amalgamation and liquidation'
T3 = 'Directors, partners, guardians and trustees'
T4 = 'Death, partition, dissolution and discontinuance'


def build():
    ck = Checks()
    d = ck.add('30', 'Days within which the liquidator must intimate appointment')
    m = ck.add('3', 'Months for Commissioner to notify liquidator of dues')
    i1 = {'id': 'i1', 'title': 'Company in liquidation', 'difficulty': 'core', 'minutes': 6,
          'q': 'A liquidator is appointed for Sterling Pvt Ltd on 1 July 2026. Explain the timelines and the liability of the directors for unpaid GST of the period before liquidation.',
          'solution': [table(['Step', 'Rule', 'Timeline'], [
              ['Liquidator', 'Intimate appointment to the Commissioner', f'Within {d} days'],
              ['Commissioner', 'Notify liquidator of dues payable', f'Within {m} months of intimation'],
              ['Directors', 'Jointly and severally liable if tax cannot be recovered from the company, unless they prove no gross neglect, misfeasance or breach of duty', 'Section 89']], title='Sections 88 and 89')],
          'checks': list(ck)}

    c2 = Checks()
    r = c2.add('1', 'Months to intimate a partner\'s retirement')
    i2 = {'id': 'i2', 'title': 'Retiring partner', 'difficulty': 'core', 'minutes': 5,
          'q': 'Manoj retires from Sunrise & Co on 30 September 2026. The firm intimates the Commissioner on 15 December 2026. Until when is Manoj liable for the firm\'s GST dues?',
          'solution': [table(['Point', 'Rule', 'Result'], [
              ['Intimation time', f'Within {r} month of retirement', 'Missed (due by 30 October 2026)'],
              ['Liability', 'Continues until intimation is received', 'Up to 15 December 2026'],
              ['Nature', 'Jointly and severally with the firm and other partners', '—']], title='Section 90')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 85: where a taxable person transfers its business wholly or partly (by sale, gift, lease, licence or otherwise, including on death of a sole proprietor), the transferor and transferee are jointly and severally liable for tax, interest and penalty due up to the transfer, to the extent of the transfer. The transferee pays tax on its own supplies from the transfer date and must amend or obtain registration.',
            'Section 86: where an agent supplies or receives taxable goods on behalf of a principal, both are jointly and severally liable for tax on such goods.',
            'These provisions protect revenue when the business changes hands.'],
          'Transfer of business transfers tax risk too.',
          'A buyer of a running shop can be pursued for the seller\'s unpaid GST.'),
        C('c2', T2, [
            'Section 87: when companies are amalgamated or merged under a court or tribunal order with effect from an earlier date, supplies between them from the appointed date to the order date are included in their turnovers and taxed; they are treated as distinct companies up to the order date and their registrations are cancelled from that date.',
            'Section 88: a liquidator must intimate the Commissioner of appointment within 30 days; the Commissioner notifies the liquidator within three months of the amount sufficient for dues. If dues cannot be recovered, directors of a private company are jointly and severally liable unless they prove non-recovery is not due to their gross neglect, misfeasance or breach of duty.',
            'These rules interact with the Insolvency and Bankruptcy Code, which overrides where it provides otherwise.'],
          'Corporate restructuring and winding-up carry GST duties.',
          'Transactions between merging companies before the order date are taxable.'),
        C('c3', T3, [
            'Section 89: if a private company\'s dues cannot be recovered, every person who was a director during the relevant period is jointly and severally liable, unless he proves non-recovery is not due to gross neglect, misfeasance or breach of duty. When a private company converts into a public company, this does not apply to dues of the private company period except penalties imposed on the director personally.',
            'Section 90: the firm and each partner are jointly and severally liable for the firm\'s dues. A retiring partner remains liable for dues up to retirement; if retirement is not intimated within one month, liability continues until intimation.',
            'Section 91: guardians, trustees or agents carrying on business for minors or incapacitated persons are liable as if the beneficiary were conducting the business. Section 92: Court of Wards, Administrator General, Official Trustee, receivers and managers controlling an estate are liable to the same extent.'],
          'People behind the entity can be personally liable.',
          'A partner who retires but delays intimation stays liable longer.'),
        C('c4', T4, [
            'Section 93: on death, if the business continues, the legal representative or successor pays the dues; if discontinued, the legal representative pays out of the estate. On partition of a HUF or AOP, members are jointly and severally liable for pre-partition dues. On dissolution of a firm, every person who was a partner is jointly and severally liable. On termination of guardianship or trust, the ward or beneficiary is liable.',
            'Section 94: where a firm, AOP or HUF discontinues business, dues are determined as if no discontinuance happened, and every person who was a partner, member or coparcener is jointly and severally liable. A change in constitution does not affect liability; on dissolution or partition, liability continues for all.',
            'These provisions are subject to the IBC.'],
          'Liability survives death, partition and dissolution.',
          'Heirs continuing a deceased trader\'s shop inherit its GST dues.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Due diligence on business purchase', 'role': 'Transaction advisor',
             'situation': 'A client is acquiring a running business.',
             'steps': ['Review seller\'s GST returns and notices.', 'Quantify contingent tax exposure.', 'Seek indemnity and escrow.', 'Plan registration amendments.'],
             'takeaway': 'Section 85 makes due diligence essential.'}]

    mcqs = [
        Q('m1', 'On transfer of business, unpaid tax up to transfer is payable by:', ['Transferor and transferee jointly and severally', 'Transferor only', 'Transferee only', 'Neither'], 0,
          'Section 85. In practice: to extent of transfer.', 'c1', T1),
        Q('m2', 'Agent supplying goods for a principal is liable for tax:', ['Jointly and severally with the principal', 'Alone', 'Not at all', 'Only for services'], 0,
          'Section 86. In practice: agent registration needed.', 'c1', T1),
        Q('m3', 'A liquidator must intimate appointment within:', ['Thirty days', 'Three months', 'Seven days', 'Six months'], 0,
          'Section 88(1). In practice: to Commissioner.', 'c2', T2),
        Q('m4', 'Directors of a private company escape liability if they prove absence of:', ['Gross neglect, misfeasance or breach of duty', 'Profits', 'Shareholding', 'Signing authority'], 0,
          'Section 89. In practice: burden on director.', 'c3', T3),
        Q('m5', 'Retirement of a partner must be intimated within:', ['One month', 'Three months', 'Seven days', 'One year'], 0,
          'Section 90. In practice: else liability continues.', 'c3', T3),
        Q('m6', 'If a deceased person\'s business is discontinued, dues are paid by:', ['Legal representative out of the estate', 'The Government', 'Nobody', 'Employees'], 0,
          'Section 93(1). In practice: to extent of estate.', 'c4', T4),
        Q('m7', 'On partition of a HUF, pre-partition dues are payable by:', ['Members jointly and severally', 'Karta only', 'Nobody', 'Eldest member only'], 0,
          'Section 93(2). In practice: in proportion to share.', 'c4', T4),
        Q('m8', 'Supplies between amalgamating companies from appointed date to order date are:', ['Taxable and included in turnover', 'Exempt', 'Not supplies', 'Zero-rated'], 0,
          'Section 87. In practice: distinct companies till order.', 'c2', T2),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Timelines', 2, 'analysis', '30 days', nums=[d, m]), S('s2', 'Directors', 2, 'analysis', 'gross neglect')],
          ['Cite sections.'], ['Making all directors liable without defence.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Intimation rule', 3, 'analysis', 'one month', nums=[r])],
          ['State date of liability end.'], ['Ending liability on retirement date.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Does conversion of a private company to public company affect director liability?', 'Directors are relieved for dues of the private company period, except penalties imposed on them personally.',
          [P('p1', 'Relieved', 5, 'relieved'), P('p2', 'Penalties', 5, 'penalt')], 'c3'),
        V('v2', 'Who is liable when a Court of Wards manages an estate?', 'The Court of Wards, Administrator General, Official Trustee or manager, to the same extent as the owner.',
          [P('p1', 'Court of Wards', 5, 'court of wards'), P('p2', 'Same extent', 5, 'same extent')], 'c3'),
        V('v3', 'What happens to liability on change in constitution of a firm?', 'It is unaffected; the firm as reconstituted remains liable for earlier dues.',
          [P('p1', 'Unaffected', 5, 'unaffected'), P('p2', 'Reconstituted', 5, 'reconstitut')], 'c4'),
        V('v4', 'Who pays dues after a trust terminates?', 'The beneficiary, as if the trust had not existed.',
          [P('p1', 'Beneficiary', 5, 'beneficiary'), P('p2', 'Trust', 5, 'trust')], 'c4'),
        V('v5', 'What must a transferee of business do about registration?', 'Apply for registration or amend it within the prescribed time and pay tax on its own supplies.',
          [P('p1', 'Registration', 5, 'registration'), P('p2', 'Own supplies', 5, 'own supplies')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Patel HUF partition', 'difficulty': 'core',
              'case': 'Patel HUF, a registered trader, was partitioned on 1 October 2026 among four members. GST dues of ₹8,00,000 for earlier periods are later assessed.',
              'mcqs': [
                  M('k1a', 'Who is liable for the dues?', ['All members jointly and severally', 'Karta only', 'No one', 'Only the eldest'], 0,
                    'Section 93(2). In practice: shares considered.', 'core', topic=T4),
                  M('k1b', 'If shares are equal, each member\'s proportionate share (₹):', ['2,00,000', '8,00,000', '4,00,000', '1,00,000'], 0,
                    '8 lakh ÷ 4. In practice: jointly liable for whole.', 'core', check=200000, topic=T4),
                  M('k1c', 'Can the department recover the full amount from one member?', ['Yes, liability is joint and several', 'No', 'Only with consent', 'Only up to share'], 0,
                    'Joint and several. In practice: inter se recovery.', 'core', topic=T4),
                  M('k1d', 'Provisions are subject to:', ['The Insolvency and Bankruptcy Code', 'Income-tax Act', 'Companies Act only', 'FEMA'], 0,
                    'Section 93 opening words. In practice: IBC overrides.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch20', 1, 'Liability to Pay in Certain Cases',
                ['Apply liability on transfer of business and agents.',
                 'Apply liability on amalgamation and liquidation.',
                 'Apply liability of directors, partners, guardians and trustees.',
                 'Apply liability on death, partition and dissolution.'],
                {'difficulty': 'core', 'minutes': {'learn': 20, 'practice': 15}, 'prereq': ['fin-p5-ch19-u01'],
                 'exam_tip': 'Name the section and who is liable, then any defence or time limit.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 85 transfer; 86 agent.', 'Section 87 amalgamation; 88 liquidation (30 days / 3 months).', 'Section 89 directors; 90 partners (1 month intimation).',
                             'Sections 91–92 guardians and Court of Wards.', 'Sections 93–94 death, partition, dissolution, discontinuance.'],
                 'remember': ['IBC overrides where it provides otherwise.'],
                 'traps': ['Ending a retiring partner\'s liability without intimation.']},
                [('Transfer', 'Section 85'), ('Liquidation', 'Section 88'), ('Directors', 'Section 89'), ('Partners', 'Section 90'), ('Death/partition', 'Section 93')],
                viva, cases)
