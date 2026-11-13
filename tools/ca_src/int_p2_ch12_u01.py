"""CA Intermediate · Paper 2 Corporate and Other Laws · Chapter 12 The Limited Liability Partnership Act, 2008.
Scope follows the ICAI study material; provisions are explained in original words; examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p2-ch12-u01'
T1 = 'Nature of an LLP and key definitions'
T2 = 'Partners, designated partners and incorporation'
T3 = 'Relations of partners, liability and contribution'
T4 = 'Financial disclosures, audit and annual filings'
T5 = 'Conversion, winding up and comparison with firms and companies'


def build():
    i1 = {'id': 'i1', 'title': 'Is it a small LLP, and what must it file?', 'difficulty': 'core', 'minutes': 6,
          'q': 'Arya Consultants LLP has partners\' contribution of ₹20 lakh and turnover of ₹35 lakh in the last year (statutory limits apply, without any higher prescribed amount). Its year ends on 31 March 2026. Is it a small LLP, and by when must it file its annual return and statement of account and solvency?',
          'solution': [table(['Point', 'Rule', 'Answer'], [
              ['Small LLP?', 'Contribution ≤ ₹25 lakh and turnover ≤ ₹40 lakh (higher amounts may be prescribed up to ₹5 crore and ₹50 crore)', 'Yes'],
              ['Annual return', 'Within 60 days of close of financial year', 'By 30 May 2026'],
              ['Statement of account and solvency', 'Within six months from the end of the year', 'By 30 September 2026']], title='LLP filings'),
              note('Small LLPs get lighter penalties and simpler compliance, but still file these documents.')],
          'checks': []}

    i2 = {'id': 'i2', 'title': 'Who pays for a partner\'s wrong?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Ravi, a partner of Swift Logistics LLP, negligently damaged a client\'s goods while handling a contract for the LLP, causing loss of ₹8 lakh. The client sues the LLP and also Meena, another partner. Advise.',
          'solution': [legal('Sections 26 and 27, LLP Act, 2008',
                             'Loss caused by Ravi\'s wrongful act in the course of LLP business; client sues LLP and Meena.',
                             'Every partner is an agent of the LLP, not of other partners. The LLP is liable for a partner\'s wrongful act or omission in the course of its business or with its authority. An obligation of the LLP is solely its own; a partner is not personally liable for another partner\'s wrongful acts. The partner who committed the act remains personally liable for his own wrongful act.',
                             'The LLP is liable to the client for ₹8 lakh; Meena is not personally liable; Ravi may be personally liable for his own negligence.')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'An LLP is a body corporate registered under the LLP Act, 2008 — a legal entity separate from its partners, with perpetual succession. Changes in partners do not affect its existence, rights or liabilities.',
            'It combines the flexibility of a partnership with the limited liability of a company; the Indian Partnership Act, 1932 does not apply to it.',
            'An LLP may be formed only to carry on a lawful business with a view to profit — not for charitable purposes.',
            'A small LLP is one whose contribution does not exceed ₹25 lakh (or a prescribed higher amount up to ₹5 crore) and whose turnover for the preceding year does not exceed ₹40 lakh (or a prescribed amount up to ₹50 crore).'],
          'An LLP is a firm with a corporate body and limited liability.',
          'Retirement of a partner does not dissolve an LLP, unlike a partnership firm.'),
        C('c2', T2, [
            'An LLP needs at least two partners; there is no maximum. If the number falls below two for more than six months, the remaining partner who knows it becomes personally liable for obligations incurred during that time.',
            'Any individual or body corporate may be a partner (except persons of unsound mind, undischarged insolvents, or those who have applied to be adjudged insolvent).',
            'There must be at least two designated partners who are individuals, at least one resident in India (stayed in India for at least 120 days in the financial year). Designated partners obtain a Designated Partner Identification Number and are responsible for compliance; their particulars are filed within 30 days of appointment.',
            'Incorporation: two or more persons subscribe to an incorporation document filed with the Registrar with a statement of compliance; the Registrar registers it within 14 days and issues a certificate of incorporation. The name ends with "LLP" or "Limited Liability Partnership".'],
          'Two partners, two designated partners and one of them resident in India.',
          'A company can be a partner of an LLP but cannot be a designated partner itself; it nominates an individual.'),
        C('c3', T3, [
            'Mutual rights and duties of partners are governed by the LLP agreement; where the agreement is silent, the First Schedule applies (equal sharing, indemnity for business payments, no remuneration, consent of all partners for new partners, and so on).',
            'Every partner is an agent of the LLP but not of other partners. The LLP is not bound by a partner\'s act where the partner had no authority and the other party knew it or did not believe him to be a partner.',
            'The LLP is liable for a partner\'s wrongful act in the course of its business; obligations of the LLP are its own, and partners are not personally liable merely by being partners. A partner remains liable for his own wrongful acts, and in cases of fraud intended to deceive creditors, liability may be unlimited for those involved.',
            'Contribution may be in tangible or intangible property, cash, promissory notes, binding promises to bring in money or assets later, or agreements to render services; its monetary value and nature are disclosed in the accounts.'],
          'Partners act for the LLP, not for each other; the LLP carries its own debts.',
          'A partner who commits fraud to cheat creditors loses the shield of limited liability.'),
        C('c4', T4, [
            'Section 34: the LLP keeps proper books of account on cash or accrual basis and by double-entry at its registered office, preserved for the prescribed period.',
            'It prepares a statement of account and solvency within six months from the end of each financial year and files it with the Registrar. Accounts are audited as prescribed; the Central Government may exempt classes of LLPs (small LLPs as notified).',
            'Section 35: an annual return is filed with the Registrar within 60 days of the close of the financial year.',
            'Changes in partners, designated partners or registered office are notified to the Registrar within 30 days. The LLP\'s documents filed with the Registrar are open to public inspection.'],
          'Books, solvency statement, audit and annual return keep an LLP transparent.',
          'An LLP with a 31 March year end files its annual return by 30 May.'),
        C('c5', T5, [
            'A partnership firm, private company or unlisted public company may convert into an LLP under the Second, Third and Fourth Schedules. All partners or shareholders become partners of the LLP, and its assets, liabilities, rights and obligations vest in the LLP; the firm or company is deemed dissolved. The LLP informs the Registrar of Firms or Companies within 15 days.',
            'Winding up may be voluntary or by the Tribunal (for example, on inability to pay debts, default in filing for five consecutive years, or acting against the sovereignty of India).',
            'Compared with a partnership firm: an LLP is a body corporate with limited liability and perpetual succession, and registration is compulsory. Compared with a company: it has no share capital, internal governance by agreement, and fewer compliance requirements.',
            'Foreign LLPs may set up a place of business in India and are subject to prescribed provisions.'],
          'A firm or company can become an LLP, carrying everything across.',
          'On conversion of a private company, all its shareholders become partners of the new LLP.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Setting up an LLP', 'role': 'Article assistant',
             'situation': 'Two chartered accountants and a company want to form an LLP for consulting.',
             'steps': ['Check partner eligibility and designated partners (one resident).', 'Obtain DPINs and reserve the name.', 'File the incorporation document and LLP agreement.', 'Diarise the annual return and solvency statement.'],
             'takeaway': 'Designated partners carry the compliance load.'}]

    mcqs = [
        Q('m1', 'The minimum number of partners in an LLP is:', ['Two', 'One', 'Seven', 'Three'], 0,
          'Every LLP must have at least two partners, and there is no maximum limit. If the number falls below two for over six months, the remaining partner with knowledge becomes personally liable. In practice: admit a new partner quickly.', 'c2', T2),
        Q('m2', 'At least one designated partner must be resident in India, meaning he stayed in India during the financial year for at least:', ['120 days', '182 days', '90 days', '60 days'], 0,
          'The LLP Act, as amended, treats a person as resident in India for this purpose if he has stayed in India for not less than 120 days during the financial year. In practice: check travel records.', 'c2', T2, 'core', check=120),
        Q('m3', 'An LLP\'s annual return is filed within:', ['60 days of the close of the financial year', '30 days', 'Six months', '90 days'], 0,
          'Section 35 requires the annual return to be filed with the Registrar within sixty days of the closure of the financial year. The statement of account and solvency is due within six months. In practice: designated partners sign.', 'c4', T4, 'core', check=60),
        Q('m4', 'A partner of an LLP is:', ['An agent of the LLP but not of other partners', 'An agent of all partners', 'Not an agent at all', 'An employee of the LLP'], 0,
          'Section 26 makes every partner an agent of the LLP for its business, but not of other partners, so one partner\'s acts do not personally bind the others. In practice: authority limits should be clear.', 'c3', T3),
        Q('m5', 'A partner of an LLP is personally liable for:', ['His own wrongful acts', 'All debts of the LLP', 'Wrongful acts of other partners', 'Nothing in any case'], 0,
          'The LLP\'s obligations are its own and partners are not personally liable for other partners\' wrongs, but a partner is liable for his own wrongful acts or omissions, and fraud can bring unlimited liability. In practice: insurance helps.', 'c3', T3),
        Q('m6', 'Where the LLP agreement is silent, the mutual rights and duties of partners are governed by:', ['The First Schedule to the LLP Act', 'The Indian Partnership Act, 1932', 'The Companies Act, 2013', 'The courts\' discretion'], 0,
          'The First Schedule provides default terms when the LLP agreement is silent; the Indian Partnership Act does not apply to LLPs. In practice: draft a full LLP agreement.', 'c3', T3),
        Q('m7', 'Which can convert into an LLP under the Act?', ['An unlisted public company', 'A listed public company', 'A Section 8 company only', 'A trust'], 0,
          'Partnership firms, private companies and unlisted public companies may convert into LLPs under the Second to Fourth Schedules. Listed companies are not included. In practice: all shareholders become partners.', 'c5', T5),
        Q('m8', 'The maximum contribution limit that may be prescribed for a small LLP is:', ['₹5 crore', '₹25 lakh', '₹50 crore', '₹10 crore'], 0,
          'The Act sets ₹25 lakh contribution and ₹40 lakh turnover for a small LLP, with power to prescribe higher amounts up to ₹5 crore and ₹50 crore respectively. In practice: check current notified limits.', 'c1', T1, 'core', check=5),
        Q('m9', 'An LLP is NOT allowed to be formed for:', ['Charitable purposes', 'Professional services', 'Trading', 'Manufacturing'], 0,
          'An LLP must carry on a lawful business with a view to profit; non-profit or charitable objects cannot be pursued through an LLP. In practice: use a trust or Section 8 company instead.', 'c1', T1),
        Q('m10', 'Changes in partners must be notified to the Registrar within:', ['30 days', '60 days', '15 days', '7 days'], 0,
          'The LLP files notice of any change in partners or designated partners within thirty days. On conversion, the LLP informs the Registrar of Firms or Companies within 15 days. In practice: update the agreement too.', 'c4', T4, 'core', check=30),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Small LLP test', 1.5, 'concept', '25 lakh|40 lakh'),
           S('s2', 'Annual return date', 1.5, 'concept', '60 days|30 may'),
           S('s3', 'Solvency statement date', 1, 'concept', 'six months|30 september')],
          ['Apply both small-LLP limits.'], ['Mixing up the two deadlines.'], ['Table.'], pad='table'),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Partner as agent of LLP', 1.5, 'application', 'agent'),
           S('s2', 'LLP liable', 1.5, 'application', 'llp is liable|liable'),
           S('s3', 'Other partner not liable; wrongdoer liable', 2, 'conclusion', 'meena|personally')],
          ['Separate LLP, wrongdoer and co-partner.'], ['Making all partners jointly liable as in a firm.'], ['Provision → facts → analysis → conclusion.']),
    ]

    viva = [
        V('v1', 'What is an LLP?', 'A body corporate formed under the LLP Act, 2008, a legal entity separate from its partners with perpetual succession and limited liability.',
          [P('p1', 'Body corporate, separate entity', 6, 'body corporate|separate'), P('p2', 'Perpetual succession', 4, 'perpetual')], 'c1'),
        V('v2', 'State the requirements for designated partners.', 'At least two individuals as designated partners, at least one resident in India, each holding a DPIN.',
          [P('p1', 'Two individuals', 5, 'two'), P('p2', 'One resident', 5, 'resident')], 'c2'),
        V('v3', 'What forms of contribution are allowed?', 'Tangible or intangible property, cash, promissory notes, binding promises to bring in money or assets, and agreements to render services.',
          [P('p1', 'Property and cash', 5, 'property|cash'), P('p2', 'Services or notes', 5, 'services|promissory')], 'c3'),
        V('v4', 'What annual documents does an LLP file?', 'A statement of account and solvency within six months of year end and an annual return within 60 days of year end.',
          [P('p1', 'Statement of account and solvency', 5, 'solvency'), P('p2', 'Annual return', 5, 'annual return')], 'c4'),
        V('v5', 'What happens on conversion of a firm into an LLP?', 'Partners of the firm become LLP partners, all assets and liabilities vest in the LLP, and the firm is deemed dissolved.',
          [P('p1', 'Vesting in LLP', 5, 'vest|transfer'), P('p2', 'Firm dissolved', 5, 'dissolv')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Saffron Studio LLP', 'difficulty': 'moderate',
              'case': 'Saffron Studio LLP has two partners: Kiran (resident in India) and Nova Pvt. Ltd. One day Kiran retires and Nova Pvt. Ltd. continues alone for eight months, signing new contracts.',
              'mcqs': [
                  M('k1a', 'Can Nova Pvt. Ltd. itself be a designated partner?', ['No; a body corporate partner nominates an individual to act as designated partner', 'Yes', 'Only if it is a listed company', 'Only with Registrar approval'], 0,
                    'Designated partners must be individuals; where a body corporate is a partner, it nominates an individual to act as designated partner. In practice: file consent and DPIN.', 'moderate', topic=T2),
                  M('k1b', 'Consequence of continuing with one partner for eight months:', ['The remaining partner, knowing of it, is personally liable for obligations after six months', 'No consequence', 'The LLP is automatically dissolved', 'The Registrar must strike it off at once'], 0,
                    'If an LLP carries on with fewer than two partners for more than six months, the remaining partner who knows this becomes personally liable for obligations incurred during that period. In practice: admit a partner within six months.', 'moderate', topic=T2),
                  M('k1c', 'Does Kiran\'s retirement dissolve the LLP?', ['No, an LLP has perpetual succession', 'Yes', 'Only if the agreement says so', 'Only after 30 days'], 0,
                    'An LLP is a separate legal entity with perpetual succession; changes in partners do not affect its existence. Notice of the change is filed within 30 days. In practice: update records.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p2', 'int-p2-ch12', 1, 'The Limited Liability Partnership Act, 2008',
                ['Explain the nature of an LLP and key definitions including small LLP.',
                 'Apply the rules on partners, designated partners and incorporation.',
                 'Explain partners\' relations, liability and contribution.',
                 'State financial disclosure and filing requirements, conversion and winding up.'],
                {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 25}, 'prereq': ['int-p2-ch11-u01'],
                 'exam_tip': 'Contrast LLP with a firm and a company in tables; remember 2 partners, 2 designated partners, 120 days, 30/60 days and six months.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['LLP: body corporate, separate entity, perpetual succession, profit motive.', 'Small LLP: ₹25 lakh / ₹40 lakh (up to ₹5 crore / ₹50 crore prescribable).',
                             'Min 2 partners; 2 designated partners, one resident (120 days).', 'Partner is agent of LLP, not of others; liable for own wrongs.',
                             'Solvency statement within 6 months; annual return within 60 days; changes within 30 days.', 'Conversion from firm, private and unlisted public companies.'],
                 'remember': ['Below two partners for over six months → personal liability.'],
                 'traps': ['The Indian Partnership Act does not apply to LLPs.']},
                [('Partners', 'Min 2, no max'), ('Resident DP', '≥ 120 days'), ('Annual return', '60 days'), ('Solvency statement', '6 months')],
                viva, cases)
