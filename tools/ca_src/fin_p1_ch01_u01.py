"""CA Final · Paper 1 Financial Reporting · Chapter 1 Introduction to Indian Accounting Standards.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch01-u01'
T1 = 'Why India moved from AS to Ind AS'
T2 = 'Global standards: IASB, IFRS, convergence and adoption'
T3 = 'How Ind AS are made, numbered and structured'
T4 = 'Roadmap for applying Ind AS'
T5 = 'Statutory framework and Division II of Schedule III'


def build():
    ck = Checks()
    nw = ck.add('200+80+150+120-15', 'Net worth (₹ crore) under section 2(57)')
    i1 = {'id': 'i1', 'title': 'Does the roadmap catch this company?', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Orion Ltd. (listed) had at 31 March 2014 (₹ crore): equity capital 200; securities premium 80; general reserve 150; retained earnings 120; revaluation reserve 60; capital reserve arising on amalgamation 20; miscellaneous expenditure not written off 15. Compute net worth for the Ind AS roadmap and identify the phase.',
          'solution': [table(['Item', 'Treatment', '₹ crore'], [
              ['Paid-up capital', 'Include', inr(200)],
              ['Securities premium', 'Include', inr(80)],
              ['General reserve and retained earnings', 'Reserves created out of profits — include', inr(270)],
              ['Revaluation reserve', 'Exclude (reserve from revaluation)', '—'],
              ['Capital reserve on amalgamation', 'Exclude', '—'],
              ['Miscellaneous expenditure not written off', 'Deduct', '(15)'],
              ['Net worth', '', inr(nw)]], title='Net worth — section 2(57)'),
              p('Listed with net worth of ₹' + inr(nw) + ' crore (₹500 crore or more), Orion falls in Phase I: Ind AS from accounting periods beginning 1 April 2016, with comparatives for 2015-16 and transition date 1 April 2015. Its group companies (holding, subsidiaries, joint ventures, associates) are covered too.')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Dates on first adoption', 'difficulty': 'core', 'minutes': 6,
          'q': 'Pinnacle Pvt. Ltd. (unlisted, net worth ₹120 crore) decides to adopt Ind AS voluntarily for the year ending 31 March 2028. Identify its first Ind AS reporting period, comparative period, date of transition and which version of Ind AS it applies. Can it later revert to AS if net worth falls?',
          'solution': [table(['Point', 'Answer'], [
              ['First Ind AS reporting period', '1 April 2027 – 31 March 2028'],
              ['Comparative period', '2026-27, restated under Ind AS'],
              ['Date of transition (opening Ind AS balance sheet)', '1 April 2026'],
              ['Standards applied', 'Ind AS effective at the end of the first Ind AS reporting period (31 March 2028)'],
              ['Reverting to AS', 'Not allowed — once Ind AS is applied, voluntarily or mandatorily, it continues for all later periods']], title='First-time adoption timeline')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Accounting standards set principles for recognition, measurement, presentation and disclosure so that financial statements are reliable and comparable. In India the Accounting Standards Board (ASB) of ICAI drafts them; the Central Government notifies them for companies on NFRA\'s recommendation, and ICAI issues them for non-corporate entities.',
            'Before Ind AS, Indian companies followed the AS framework (27 standards in force). AS struggled with newer complexities: compound and convertible instruments, embedded and commodity derivatives, group restructurings, digital-age revenue models, share-based pay, complex deferred tax and limited disclosures on revenue, related parties and segments.',
            'With growing foreign capital and cross-border listings, a framework close to global practice was needed — leading to Ind AS, converged with IFRS. Companies not covered by Ind AS (and non-corporate entities) continue with AS.'],
          'Ind AS arrived because Indian businesses became more global and complex than the old rules could describe.',
          'A start-up issuing compulsorily convertible preference shares to foreign investors needs guidance AS never really gave.'),
        C('c2', T2, [
            'The International Accounting Standards Committee (1973) sought to harmonise practice; in 2001 it was replaced by the International Accounting Standards Board (IASB) under the IFRS Foundation, which issues IFRS. An interpretations committee resolves application issues.',
            'IOSCO\'s endorsement and the European Union\'s requirement of IFRS for listed companies from 2005 made IFRS a leading global framework alongside US GAAP; the G20 backed a single set of high-quality global standards.',
            'Adoption means using IFRS exactly as issued; convergence means aligning national standards with IFRS while allowing changes for local conditions. India chose convergence: Ind AS are largely IFRS with some "carve-outs" (departures) and "carve-ins" (additions).',
            'Benefits: comparability across countries, lower cost of capital for cross-border fund-raising, easier group reporting, better disclosure and investor confidence.'],
          'India speaks the global accounting language with a local accent — convergence, not word-for-word adoption.',
          'Ind AS allows certain choices (carve-outs) that IFRS does not, to suit Indian law and practice.'),
        C('c3', T3, [
            'Process: the ASB studies the IFRS, identifies needed changes, issues an exposure draft for public comment, finalises the standard, and the ICAI Council approves and recommends it to NFRA; NFRA reviews and recommends it to the Central Government (MCA), which notifies it in the Official Gazette under the Companies (Indian Accounting Standards) Rules, 2015.',
            'Numbering follows IFRS: standards derived from IAS keep IAS numbers (Ind AS 1 to 41), and those from IFRS are numbered from 101 (e.g. Ind AS 101 first-time adoption, Ind AS 115 revenue, Ind AS 116 leases, Ind AS 117 insurance contracts). Interpretations appear as appendices to the related Ind AS.',
            'Typical structure: objective, scope, definitions, recognition, measurement, presentation, disclosure, effective date and transition, with appendices (application guidance and integral material) — and a comparison with IFRS explaining carve-outs.'],
          'Knowing the numbering lets you jump straight from an IFRS reference to the matching Ind AS.',
          'IFRS 15 becomes Ind AS 115; IAS 16 becomes Ind AS 16.'),
        C('c4', T4, [
            'Companies — Phase I (periods from 1 April 2016): listed or about-to-be-listed companies, and unlisted companies, with net worth of ₹500 crore or more. Phase II (from 1 April 2017): all other listed companies, and unlisted companies with net worth of ₹250–500 crore. Holding, subsidiary, joint venture and associate companies of covered companies follow them. Companies listed on SME exchanges are outside the roadmap. Voluntary early adoption is allowed for other companies.',
            'Net worth (section 2(57)): paid-up capital plus reserves created out of profits and securities premium, minus accumulated losses and any deferred or miscellaneous expenditure still carried on the balance sheet; reserves from revaluation, write-back of depreciation and amalgamation are excluded. It is measured on standalone figures as at 31 March 2014 (or the first audited statements after that for newer companies).',
            'NBFCs: Phase I from 1 April 2018 (net worth ₹500 crore or more); Phase II from 1 April 2019 (listed NBFCs below ₹500 crore and unlisted NBFCs of ₹250–500 crore); others stay on AS and cannot adopt voluntarily. Scheduled commercial banks and insurers follow separate timelines set by their regulators.',
            'Key transition rules: one year\'s comparatives under Ind AS, so the transition date is the start of the comparative year; standards effective at the end of the first Ind AS period apply; once applied, Ind AS cannot be abandoned; it applies to both standalone and consolidated statements; overseas group entities may prepare standalone statements under local law if the Indian parent consolidates under Ind AS.'],
          'Size and listing decide when Ind AS arrived — and once in, there is no way back.',
          'A subsidiary of a Phase I company had to adopt Ind AS in 2016 even if it was tiny.'),
        C('c5', T5, [
            'Section 129 requires financial statements to give a true and fair view and comply with notified standards in the form of Schedule III; section 133 empowers the Central Government to prescribe standards recommended by ICAI after NFRA\'s examination. SEBI\'s regulations require listed entities to publish results in the format and under the standards applicable.',
            'Schedule III Division II sets the format for Ind AS companies: a balance sheet (assets, equity and liabilities split into current and non-current), a statement showing movements in equity, a profit and loss statement that also carries other comprehensive income (items that will and will not be reclassified to profit or loss), and notes. Division I is for AS companies; Division III for Ind AS NBFCs.',
            'ICAI\'s Guidance Note on Division II explains presentation issues such as classification of financial liabilities, other equity components and additional disclosures (e.g. ageing of receivables and payables, ratios, undisclosed income and crypto holdings).'],
          'Schedule III is the shape of the box; Ind AS decides what goes into it.',
          'Gains on remeasuring defined benefit plans go to OCI and are shown as items that will not be reclassified.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Ind AS applicability memo', 'role': 'Article assistant',
             'situation': 'A private group with a listed parent asks which entities must use Ind AS.',
             'steps': ['Identify the parent\'s phase from listing and net worth.', 'List all subsidiaries, associates and joint ventures.', 'Apply the group rule to each Indian entity.', 'Note overseas entities that may use local GAAP for standalone accounts.'],
             'takeaway': 'Ind AS travels through the group — check every related company, not just the parent.'}]

    mcqs = [
        Q('m1', 'Ind AS are best described as:', ['Converged with IFRS, with some carve-outs and carve-ins', 'Identical to IFRS', 'Identical to US GAAP', 'Unrelated to IFRS'], 0,
          'India chose convergence: Ind AS track IFRS but depart where Indian conditions require. In practice: read the comparison appendix to each Ind AS.', 'c2', T2),
        Q('m2', 'Ind AS are notified for companies by:', ['The Central Government (MCA) on NFRA\'s recommendation', 'ICAI alone', 'SEBI', 'RBI'], 0,
          'Section 133 empowers the Government to prescribe standards recommended by ICAI after NFRA\'s examination. In practice: notified in the Gazette.', 'c3', T3),
        Q('m3', 'Which Ind AS is derived from an IFRS (not an IAS)?', ['Ind AS 115', 'Ind AS 16', 'Ind AS 12', 'Ind AS 37'], 0,
          'Standards from IFRS are numbered 101 onwards; 16, 12 and 37 come from IAS. In practice: Ind AS 115 mirrors IFRS 15.', 'c3', T3),
        Q('m4', 'An unlisted company with net worth of ₹300 crore (31 March 2014) fell under:', ['Phase II, from 1 April 2017', 'Phase I, from 1 April 2016', 'No mandatory phase', 'The NBFC roadmap'], 0,
          'Unlisted companies with net worth of ₹250–500 crore were in Phase II. In practice: its group companies followed.', 'c4', T4),
        Q('m5', 'For roadmap net worth, which item is excluded?', ['Revaluation reserve', 'Securities premium', 'General reserve', 'Paid-up capital'], 0,
          'Reserves from revaluation, write-back of depreciation and amalgamation do not count. In practice: deduct accumulated losses too.', 'c4', T4),
        Q('m6', 'A company adopting Ind AS for 2028-29 has a transition date of:', ['1 April 2027', '1 April 2028', '31 March 2029', '1 April 2026'], 0,
          'One year of comparatives means the opening Ind AS balance sheet is at the start of the comparative year. In practice: restate 2027-28.', 'c4', T4),
        Q('m7', 'An unlisted NBFC with net worth of ₹100 crore wishing to adopt Ind AS voluntarily:', ['Cannot — voluntary adoption is not allowed for NBFCs', 'Can adopt from any year', 'Must adopt from 2018', 'Needs SEBI approval'], 0,
          'NBFCs apply Ind AS only if they meet the roadmap criteria. In practice: they continue under AS.', 'c4', T4),
        Q('m8', 'The Schedule III format for Ind AS companies (other than NBFCs) is:', ['Division II', 'Division I', 'Division III', 'Part IV'], 0,
          'Division I is for AS companies, Division II for Ind AS companies, Division III for Ind AS NBFCs. In practice: OCI is shown under Division II.', 'c5', T5),
        Q('m9', 'Once a company starts applying Ind AS:', ['It must continue even if it no longer meets the criteria', 'It may revert next year', 'It reverts if net worth falls', 'It needs yearly approval'], 0,
          'The rules prohibit going back once Ind AS has been applied. In practice: plan voluntary adoption carefully.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Inclusions', 1.5, 'concept', 'premium|reserve'), S('s2', 'Exclusions', 1.5, 'concept', 'revaluation|amalgamation'),
           S('s3', 'Net worth and phase', 2, 'computation', 'phase', nums=[nw])],
          ['Use section 2(57).'], ['Including the revaluation reserve.'], ['Table and conclusion.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Periods', 1.5, 'concept', '2027|2028'), S('s2', 'Transition date', 1.5, 'concept', '1 april 2026'), S('s3', 'No reversal', 1, 'concept', 'revert|continue')],
          ['State each date clearly.'], ['Taking the transition date as the start of the first Ind AS year.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Distinguish adoption and convergence of IFRS.', 'Adoption uses IFRS exactly as issued by the IASB; convergence aligns national standards with IFRS while permitting departures for local conditions, as India did.',
          [P('p1', 'Adoption as issued', 5, 'as issued|exactly'), P('p2', 'Convergence with departures', 5, 'align|departure|carve')], 'c2'),
        V('v2', 'Outline how an Ind AS is notified.', 'ASB drafts and exposes it, the ICAI Council approves and recommends it, NFRA examines and recommends it, and the Central Government notifies it.',
          [P('p1', 'ASB and ICAI', 5, 'asb|council'), P('p2', 'NFRA and Government', 5, 'nfra|government|notif')], 'c3'),
        V('v3', 'Which companies were in Phase I?', 'Companies, listed or unlisted, whose net worth was 500 crore rupees or more, together with their holding, subsidiary, joint venture and associate companies, from 1 April 2016.',
          [P('p1', '500 crore', 6, '500 crore'), P('p2', 'Group companies', 4, 'holding|subsidiar')], 'c4'),
        V('v4', 'How is net worth computed for the roadmap?', 'Paid-up capital plus reserves from profits and securities premium, less accumulated losses and unwritten-off expenditure, excluding revaluation, depreciation write-back and amalgamation reserves.',
          [P('p1', 'Inclusions', 5, 'capital|premium'), P('p2', 'Exclusions', 5, 'revaluation|amalgamation')], 'c4'),
        V('v5', 'What does Division II of Schedule III contain?', 'Formats for an Ind AS company\'s balance sheet, its statement of changes in equity, and its profit and loss statement with other comprehensive income, plus the related notes.',
          [P('p1', 'Statements', 5, 'balance sheet|changes in equity'), P('p2', 'OCI', 5, 'comprehensive')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'The Vega group', 'difficulty': 'moderate',
              'case': 'Vega Holdings Ltd. (listed, net worth ₹650 crore at 31 March 2014) has: Vega Retail Pvt. Ltd. (Indian subsidiary, net worth ₹40 crore); Vega Finance Ltd. (unlisted NBFC subsidiary, net worth ₹180 crore); and Vega Europe GmbH (German subsidiary).',
              'mcqs': [
                  M('k1a', 'Vega Holdings applied Ind AS from:', ['Accounting periods beginning 1 April 2016', '1 April 2017', '1 April 2018', 'Voluntary only'], 0,
                    'Listed with net worth above ₹500 crore — Phase I. In practice: transition date 1 April 2015.', 'core', topic=T4),
                  M('k1b', 'Vega Retail Pvt. Ltd.:', ['Must apply Ind AS as a subsidiary of a Phase I company', 'Continues with AS due to its small size', 'Applies Ind AS from 2019', 'Uses German GAAP'], 0,
                    'Subsidiaries of covered companies follow the parent\'s phase regardless of size. In practice: both standalone and consolidated.', 'moderate', topic=T4),
                  M('k1c', 'Vega Europe GmbH\'s standalone accounts:', ['May follow German requirements, provided the parent consolidates under Ind AS', 'Must follow Ind AS', 'Need no accounts', 'Must use US GAAP'], 0,
                    'Overseas group entities may prepare standalone statements under local law. In practice: Ind AS adjustments are made for consolidation.', 'moderate', topic=T4),
                  M('k1d', 'Vega Finance Ltd. is governed for Ind AS by:', ['The NBFC roadmap, as an NBFC subsidiary of a Phase I company', 'The banking roadmap', 'No roadmap', 'SEBI LODR alone'], 0,
                    'NBFCs follow the NBFC roadmap, which covers holding, subsidiary, JV and associate NBFCs of companies already covered. In practice: it would apply Ind AS from 1 April 2018.', 'hard', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch01', 1, 'Introduction to Indian Accounting Standards',
                ['Explain why India moved from AS to Ind AS and how Ind AS relate to IFRS.',
                 'Describe how Ind AS are developed, notified, numbered and structured.',
                 'Apply the Ind AS roadmap for companies and NBFCs, including net worth.',
                 'Identify statutory provisions and the Division II format of Schedule III.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': [],
                 'exam_tip': 'For roadmap questions, compute net worth first, then apply listing status and group relationships.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['AS limits → need for IFRS-converged Ind AS.',
                             'IASB issues IFRS; India converges with carve-outs/carve-ins.',
                             'ASB → ICAI Council → NFRA → MCA notification.',
                             'Ind AS 1–41 from IAS; 101+ from IFRS.',
                             'Phase I ₹500 crore (2016); Phase II listed/₹250 crore (2017); NBFCs 2018/2019.',
                             'Schedule III Division II for Ind AS companies.'],
                 'remember': ['No reverting to AS once Ind AS applied.', 'Transition date = start of comparative year.'],
                 'traps': ['Revaluation reserve excluded from net worth.', 'NBFCs cannot adopt voluntarily.']},
                [('Phase I', '≥ ₹500 crore; FY 2016-17'), ('Phase II', 'Listed or ≥ ₹250 crore; FY 2017-18'), ('NBFC Phase I', '≥ ₹500 crore; FY 2018-19'), ('Division II', 'Ind AS format')],
                viva, cases)
