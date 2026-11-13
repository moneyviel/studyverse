"""CA Intermediate · Paper 2 Corporate and Other Laws · Chapter 11 Companies Incorporated Outside India (ss. 379–393).
Scope follows the ICAI study material; provisions are explained in original words; examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p2-ch11-u01'
T1 = 'Foreign company and application of the Act (s. 2(42), 379)'
T2 = 'Documents to be delivered on establishing business (s. 380)'
T3 = 'Accounts, annual return, display and service (ss. 381–384)'
T4 = 'Prospectus and Indian Depository Receipts (ss. 386–391)'
T5 = 'Punishment, validity of contracts and mergers (ss. 392–393, 234)'


def build():
    ck = Checks()
    ind = ck.add('30+25', 'Indian holding in the paid-up capital (%)')
    i1 = {'id': 'i1', 'title': 'Is it treated like an Indian company?', 'difficulty': 'core', 'minutes': 6,
          'q': 'Orion Inc., incorporated in Singapore, has a branch office in Bengaluru. Indian citizens hold 30% and an Indian company holds 25% of its paid-up capital (equity and preference together). What is its status under the Companies Act, 2013?',
          'solution': [table(['Point', 'Rule', 'Answer'], [
              ['Foreign company?', 'Incorporated outside India with a place of business in India, doing business here', 'Yes'],
              ['Indian holding', '30% + 25%', f'{R(ind)}% — at least 50%'],
              ['Consequence', 'Section 379(2)', 'Must comply with Chapter XXII and other prescribed provisions for its Indian business as if it were a company incorporated in India']], title='Section 379')],
          'checks': list(ck)}

    ck2 = Checks()
    mx = ck2.add('300000+50000*9', 'Maximum fine on the company for 10 days of continuing default (₹)')
    i2 = {'id': 'i2', 'title': 'Late filing by a foreign company', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Nova LLC, a foreign company, opened an office in Mumbai on 1 May but filed Form FC-1 only on 20 June, and the default continued for 10 days beyond the first day for another filing. What are the consequences, and are its contracts in India valid?',
          'solution': [legal('Sections 380, 392 and 393',
                             'FC-1 filed after 30 days; continuing default.',
                             'Documents must be delivered within 30 days of establishing a place of business in India. On contravention of Chapter XXII the foreign company is liable to a fine of ₹1 lakh to ₹3 lakh, plus up to ₹50,000 for each day after the first during a continuing default; every officer in default is liable to a fine of ₹25,000 to ₹5 lakh. Section 393 says failure to comply does not invalidate contracts, but the company cannot sue on them until it complies.',
                             f'Nova LLC is in default (FC-1 was due by 31 May). Its maximum fine for the 10-day continuing default is {inr(mx)}. Its contracts remain valid, but it cannot bring suits on them until it complies.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Section 2(42): a foreign company is any company or body corporate incorporated outside India that has a place of business in India (itself or through an agent, physically or electronically) and carries on some business activity in India in any way.',
            'Section 379(1): sections 380 to 386 and 392–393 apply to all foreign companies.',
            'Section 379(2): where at least 50% of the paid-up share capital (equity, preference or both) of a foreign company is held by Indian citizens, companies incorporated in India, or both together, it must also comply with prescribed provisions as if it were an Indian company, for its business in India.'],
          'A foreign company becomes partly "Indian" when Indians own half or more of it.',
          'A US company selling to Indian customers through an Indian website and agent can be a foreign company.'),
        C('c2', T2, [
            'Within 30 days of establishing a place of business in India, a foreign company files with the Registrar (Form FC-1): a certified copy of its charter, memorandum and articles (with English translation if needed); the address of its registered or principal office; a list of directors and secretary; names and addresses of persons resident in India authorised to accept service of documents; the address of its principal place of business in India; details of any Indian office it opened and shut in the past; and a declaration that no director or authorised representative has been convicted or debarred.',
            'Any alteration in these documents or particulars is filed within 30 days (Form FC-2).'],
          'Registration documents must reach the Registrar within 30 days of setting up in India.',
          'A change of the authorised representative in India is reported in FC-2 within 30 days.'),
        C('c3', T3, [
            'Section 381: every foreign company prepares financial statements of its Indian business operations each year (as per Schedule III and applicable standards, with auditor\'s report), and files them with the Registrar within six months of the close of its financial year (FC-3), along with a list of all places of business in India. The Registrar may extend the time by up to three months.',
            'Additional documents include statements of related party transactions, repatriation of profits and transfer of funds.',
            'An annual return (FC-4) is filed within 60 days from the end of the financial year.',
            'Section 382: the foreign company displays its name and country of incorporation outside every office in India in English and a local language, and states the limited liability of members on letterheads and notices.',
            'Section 383: documents are served on it by leaving them at, or sending them to, the authorised person\'s address. Section 384 applies provisions on debentures, annual return, registration of charges, books of account (kept at the principal place of business in India) and inspection, inquiry and investigation.'],
          'The Indian business is accounted for and reported almost like an Indian company.',
          'A foreign company with a 31 December year end must file FC-3 by 30 June.'),
        C('c4', T4, [
            'Sections 386–389: a prospectus issued in India by a foreign company is dated, contains prescribed particulars, includes experts\' consent where an expert statement is included, and is registered with the Registrar before issue.',
            'Section 390: the Central Government may make rules for offering Indian Depository Receipts (IDRs) — instruments issued by a domestic depository in India against underlying equity shares of an issuing company incorporated outside India.',
            'Section 391: civil and criminal liability for misstatements in prospectus (sections 34–36) applies to such issues, as does Chapter XX on winding up where applicable.'],
          'Foreign companies raising money in India face prospectus rules similar to Indian companies.',
          'An IDR lets Indian investors hold an interest in a foreign company\'s shares.'),
        C('c5', T5, [
            'Section 392: a foreign company contravening Chapter XXII is liable to a fine of at least ₹1 lakh and up to ₹3 lakh, and up to ₹50,000 per day for continuing contravention; each officer in default is liable to a fine of at least ₹25,000 and up to ₹5 lakh.',
            'Section 393: failure to comply does not affect the validity of contracts, dealings or transactions, or the company\'s liability to be sued, but the company cannot institute a suit or legal proceeding on them until it complies.',
            'Section 234: mergers between Indian companies and companies in notified foreign jurisdictions are allowed, with prior RBI approval, and consideration may be paid in cash, depository receipts or both.',
            'The Central Government may exempt classes of foreign companies from prospectus requirements for offerings in International Financial Services Centres.'],
          'Non-compliance costs fines and blocks lawsuits, but does not cancel deals.',
          'A defaulting foreign company can still be sued in India by its customers.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Foreign company compliance', 'role': 'Secretarial associate',
             'situation': 'A German company has opened a liaison-cum-project office in Pune.',
             'steps': ['Check whether it is a foreign company and the Indian shareholding.', 'File FC-1 within 30 days.', 'Plan FC-3 within six months of its year end and FC-4 within 60 days.', 'Display name and country of incorporation.'],
             'takeaway': 'Registration, annual filings and display are the core obligations.'}]

    mcqs = [
        Q('m1', 'A foreign company must deliver documents to the Registrar within how many days of establishing a place of business in India?', ['30 days', '60 days', '90 days', '6 months'], 0,
          'Section 380 requires delivery of the prescribed documents within thirty days of establishing a place of business in India, in Form FC-1. Alterations are also reported within thirty days. In practice: prepare translations early.', 'c2', T2, 'core', check=30),
        Q('m2', 'A foreign company must comply as if Indian when Indian citizens and companies together hold at least what share of its paid-up capital?', ['50%', '26%', '51%', '75%'], 0,
          'Section 379(2) applies when not less than 50% of paid-up share capital, equity or preference, is held by Indian citizens, Indian bodies corporate, or both. In practice: count both classes of shares.', 'c1', T1, 'core', check=50),
        Q('m3', 'Financial statements of a foreign company\'s Indian business are filed within:', ['Six months of the close of its financial year', '30 days of the AGM', '60 days of year end', 'One year'], 0,
          'Section 381 and the rules require FC-3 to be filed no later than six months after its financial year ends; the Registrar may extend by up to three months for special reasons. In practice: attach required statements.', 'c3', T3),
        Q('m4', 'The annual return of a foreign company (FC-4) is filed within:', ['60 days from the end of its financial year', '30 days', '6 months', '90 days'], 0,
          'The rules require FC-4 to be filed within sixty days from the last day of the financial year, with particulars as at the year end. In practice: diarise both FC-3 and FC-4.', 'c3', T3, 'core', check=60),
        Q('m5', 'Which is NOT required in Form FC-1?', ['Audited financial statements of the global company for the last ten years', 'Certified copy of the charter or memorandum', 'List of directors and secretary', 'Name and address of the person authorised to accept service in India'], 0,
          'FC-1 includes the constitution documents, addresses, list of directors and secretary, authorised persons in India, principal place of business and declarations. Ten years of global accounts are not required. In practice: check the form checklist.', 'c2', T2),
        Q('m6', 'Maximum fine on a foreign company for contravening Chapter XXII (excluding continuing fine) is:', ['₹3 lakh', '₹1 lakh', '₹5 lakh', '₹25,000'], 0,
          'Section 392 provides a fine of not less than ₹1 lakh and up to ₹3 lakh, plus up to ₹50,000 per day for continuing contravention. Officers face ₹25,000 to ₹5 lakh. In practice: comply promptly.', 'c5', T5, 'core', check=3),
        Q('m7', 'If a foreign company fails to comply with Chapter XXII, its contracts in India are:', ['Valid, but it cannot sue on them until it complies', 'Void', 'Voidable at the other party\'s option', 'Valid and enforceable without restriction'], 0,
          'Section 393 preserves the validity of contracts and the company\'s liability to be sued, but bars it from instituting suits on them until compliance. In practice: compliance restores the right to sue.', 'c5', T5),
        Q('m8', 'A foreign company must display outside every office in India:', ['Its name and country of incorporation', 'Its share price', 'Its global turnover', 'Names of all shareholders'], 0,
          'Section 382 requires display of the name and the country of incorporation in English and the local language, and a statement of limited liability where applicable. In practice: also show on letterheads.', 'c3', T3),
        Q('m9', 'An Indian Depository Receipt is issued by:', ['A domestic depository in India against shares of a foreign company', 'The foreign company directly', 'SEBI', 'An Indian company on its own shares'], 0,
          'IDRs are instruments created by a domestic depository in India against underlying equity shares of a company incorporated outside India, under rules made under section 390. In practice: SEBI rules also apply.', 'c4', T4),
        Q('m10', 'A foreign company may merge into an Indian company with the prior approval of:', ['The Reserve Bank of India', 'SEBI only', 'The Registrar only', 'No approval'], 0,
          'Section 234 permits cross-border mergers with companies in notified jurisdictions, requiring prior RBI approval along with Chapter XV procedures. In practice: also follow FEMA rules.', 'c5', T5),
    ]

    questions = [
        W('q1', 3, i1['q'], i1['solution'],
          [S('s1', 'Foreign company test', 1, 'concept', 'outside india|place of business'),
           S('s2', '50% holding', 2, 'computation', '50', nums=[ind])],
          ['Add equity and preference holdings.'], ['Counting only equity.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', '30-day filing rule', 1.5, 'application', '30 days'),
           S('s2', 'Fine on company and officers', 2, 'computation', '50,000|3 lakh', nums=[mx]),
           S('s3', 'Contracts valid; suit barred', 1.5, 'application', 'cannot sue|valid')],
          ['Cover penalty and contract validity.'], ['Saying contracts become void.'], ['Provision → facts → analysis → conclusion.'], checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a foreign company?', 'A company or body corporate incorporated outside India that has a place of business in India, physically or electronically, and conducts business activity in India.',
          [P('p1', 'Incorporated outside India', 5, 'outside india'), P('p2', 'Place of business in India', 5, 'place of business')], 'c1'),
        V('v2', 'What does FC-1 contain?', 'Constitution documents, registered office address, list of directors and secretary, persons authorised to accept service, principal place of business in India and declarations.',
          [P('p1', 'Charter and directors', 5, 'charter|memorandum|director'), P('p2', 'Authorised person and address', 5, 'authorised|address')], 'c2'),
        V('v3', 'What are the time limits for FC-3 and FC-4?', 'FC-3 (financial statements) within six months of year end, extendable by three months; FC-4 (annual return) within 60 days of year end.',
          [P('p1', 'Six months', 5, 'six months|6 months'), P('p2', '60 days', 5, '60')], 'c3'),
        V('v4', 'What is the effect of non-compliance on contracts?', 'Contracts remain valid and the company can be sued, but it cannot sue on them until it complies.',
          [P('p1', 'Contracts valid', 5, 'valid'), P('p2', 'Cannot sue', 5, 'cannot|sue')], 'c5'),
        V('v5', 'What is an IDR?', 'An Indian Depository Receipt — an instrument issued by a domestic depository in India against underlying shares of a foreign company.',
          [P('p1', 'Domestic depository', 5, 'depository'), P('p2', 'Foreign company shares', 5, 'foreign|outside')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Helios GmbH', 'difficulty': 'moderate',
              'case': 'Helios GmbH (Germany) opened a branch in Chennai on 1 April 2026. Its financial year ends on 31 December. Indian shareholders hold 40% of its capital.',
              'mcqs': [
                  M('k1a', 'FC-1 was due by:', ['1 May 2026', '30 June 2026', '1 April 2026', '31 December 2026'], 0,
                    'Thirty days from establishing the place of business on 1 April gives 1 May 2026 as the last date for FC-1. In practice: file earlier if possible.', 'core', topic=T2),
                  M('k1b', 'Financial statements for the year ending 31 December 2026 are due by:', ['30 June 2027', '31 March 2027', '1 March 2027', '31 December 2027'], 0,
                    'FC-3 is due within six months of year end: 30 June 2027, extendable by three months on application. In practice: arrange the Indian audit early.', 'moderate', topic=T3),
                  M('k1c', 'With 40% Indian holding, section 379(2):', ['Does not apply', 'Applies', 'Applies only to preference shares', 'Applies after five years'], 0,
                    'Section 379(2) applies only where Indian citizens or companies hold at least 50%; at 40% Helios follows only the general provisions for foreign companies. In practice: monitor shareholding changes.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p2', 'int-p2-ch11', 1, 'Companies Incorporated Outside India',
                ['Define a foreign company and explain when it is treated like an Indian company.',
                 'State the documents and filings required on establishing business in India.',
                 'Explain accounts, annual return, display and service requirements.',
                 'Explain prospectus, IDR, punishment and validity of contracts provisions.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['int-p2-ch10-u01'],
                 'exam_tip': 'Remember: 50% Indian holding, FC-1/FC-2 in 30 days, FC-3 in 6 months (+3), FC-4 in 60 days, fines ₹1–3 lakh + ₹50,000/day.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Foreign company: incorporated abroad, place of business in India (physical or electronic).', '≥ 50% Indian holding → comply as Indian company.',
                             'FC-1 within 30 days; changes FC-2 within 30 days.', 'FC-3 within 6 months (+3); FC-4 within 60 days.',
                             'Display name and country; books at principal place in India.', 'Fine ₹1–3 lakh + ₹50,000/day; officers ₹25,000–₹5 lakh; contracts valid, suits barred.'],
                 'remember': ['IDRs are issued by a domestic depository.'],
                 'traps': ['Non-compliance does not void contracts.']},
                [('FC-1', '30 days'), ('FC-3', '6 months (+3)'), ('FC-4', '60 days'), ('Indian control', '≥ 50%')],
                viva, cases)
