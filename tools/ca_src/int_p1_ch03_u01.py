"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 3 Applicability of Accounting Standards.
Criteria as in the ICAI study material (May 2027 onwards): non-company entities — revised ICAI scheme for periods from
1 April 2024 (MSME / Large); companies — Companies (Accounting Standards) Rules, 2021 (SMC / Non-SMC). Wording original."""
from ikit import *

UID = 'int-p1-ch03-u01'
T1 = 'Three questions to decide applicability'
T2 = 'Which enterprises AS apply to, and the mandatory status'
T3 = 'Companies Act link: sections 129, 133 and 143'
T4 = 'Materiality and the item test'
T5 = 'Accounting Standards versus tax rules (ICDS)'
T6 = 'Non-company entities: MSME or Large (from 1 April 2024)'
T7 = 'Exemptions and relaxations for MSMEs'
T8 = 'Companies: SMC and Non-SMC'


def build():
    msme = table(['Condition (all must hold)', 'MSME test'], [
        ['Listing', 'Equity or debt securities not listed and not in the process of listing, in India or abroad'],
        ['Nature', 'Not a bank, financial institution or insurance company'],
        ['Turnover', 'Turnover (excluding other income) of the immediately preceding accounting year does not exceed ₹250 crore'],
        ['Borrowings', 'Borrowings stayed at or below ₹50 crore throughout the preceding accounting year (a single day above disqualifies)'],
        ['Group', 'Neither the parent nor a subsidiary of any entity outside the MSME category'],
    ], title='Non-company entity as MSME (revised ICAI scheme, periods from 1 April 2024)', note='Conditions are tested as at the end of the relevant accounting period. An entity that is not an MSME is a Large entity and complies with all AS in full.')
    msme_ex = table(['Standard', 'Position for MSMEs'], [
        ['AS 3, AS 17, AS 20, AS 24', 'Not applicable to any MSME'],
        ['AS 18, AS 28', 'Not applicable to MSMEs with turnover ≤ ₹50 crore AND borrowings ≤ ₹10 crore (preceding year) that are not holding/subsidiary of an MSME outside this band'],
        ['AS 10, AS 11, AS 26, AS 29', 'Exempt from specified (encouraged / extra) disclosure paragraphs'],
        ['AS 15', 'Relaxed: non-vesting short-term compensated absences, discounting beyond 12 months, defined-benefit and other long-term benefits may use another rational method (e.g. as if payable to all employees at year-end)'],
        ['AS 19', 'Specified lease disclosures not required'],
        ['AS 22', 'Only current tax applies; deferred tax need not be recognised. On first use, the accumulated DTA/DTL is adjusted against opening revenue reserves / owner\'s funds'],
        ['AS 28 (MSMEs not exempt)', 'Value in use may be a reasonable estimate instead of present value; some disclosures not needed'],
        ['AS 14, AS 27 (jointly controlled operations/assets)', 'Generally no such transactions — not applicable, but apply if they occur'],
        ['AS 21, 23, 25, 27 (consolidation part)', 'Apply only if the entity is required, or chooses, to prepare consolidated or interim reports'],
    ], title='MSME exemptions and relaxations (summary)')
    smc = table(['Item', 'Small and Medium-sized Company (SMC)'], [
        ['Definition source', 'Companies (Accounting Standards) Rules, 2021 (notified 23 June 2021)'],
        ['Tests', 'Same five tests as an MSME: unlisted, not bank/FI/insurer, turnover ≤ ₹250 crore and borrowings ≤ ₹50 crore in the preceding year, not holding/subsidiary of a non-SMC'],
        ['Not applicable at all', 'AS 17 Segment Reporting'],
        ['Relaxations', 'AS 15 (actuarial valuation by Projected Unit Credit Method still required, discount rate from government bond yields), AS 19 disclosures, AS 20 diluted EPS disclosure, AS 28 value in use by reasonable estimate, AS 29 paras 66–67 disclosures'],
        ['AS 25', 'Only if the company must or chooses to prepare interim reports (e.g. SEBI quarterly results of listed Non-SMCs)'],
        ['Non-SMC', 'Complies with all AS in full'],
    ], title='Companies not on Ind AS')

    concepts = [
        C('c1', T1, [
            'To decide whether a particular standard applies, ask three questions in order: (a) does it apply to this enterprise? (b) does it apply to this financial statement? (c) does it apply to this item? Only a "yes" to all three makes the standard bite. The preface to the statements of AS answers these questions.',
            'AS are mandatory from the dates notified (for companies, by MCA) and apply generally to all enterprises, subject to the exceptions discussed in this chapter. How "mandatory" they are for an enterprise depends on whether the statute governing it demands compliance.'],
          'Applicability is a three-lock door: the enterprise key, the statement key and the item key must all turn.',
          'Before ticking "AS 3 complied" for a client, a CA first checks whether AS 3 applies to that client at all — many small entities are exempt.'),
        C('c2', T2, [
            'AS apply to every enterprise engaged in commercial, industrial or business activity — corporate, co-operative or any other form — whether or not profit-oriented, and even if set up for charitable or religious purposes.',
            'They do not apply to an enterprise whose activities are entirely non-commercial (for example, only collecting donations and passing them to flood victims). If even a small part of the activity is commercial, industrial or business in nature, AS apply to all of its activities.',
            'Where the governing statute does not demand compliance (for example a partnership firm), the mandatory status works through ICAI members: in an attest function they must check compliance and, if there are deviations, disclose them adequately in their report. Preparing the statements and making proper disclosure remain the management\'s responsibility; the auditor forms and reports an opinion.'],
          'A charity that also runs a paid café is "in business" for accounting purposes — the café pulls the whole charity under the standards.',
          'An auditor of a partnership firm reports non-compliance with an AS in the audit report, even though no partnership law requires the AS.'),
        C('c3', T3, [
            'Section 129(1): a company\'s financial statements must follow the standards that the Government has notified under section 133.',
            'Section 143(3)(e): the auditor reports whether, in his opinion, the company\'s statements follow the section 133 standards.',
            'Section 129(5): if a company does not comply with an AS, it must disclose the deviation, the reasons and the financial effect, if any.',
            'Proviso to section 129(1): statements are not treated as failing to give a true and fair view merely because they omit matters that the governing law does not require — for insurance companies (Insurance Act, 1938 / IRDA Act, 1999), banking companies (Banking Regulation Act, 1949), electricity companies (Electricity Act, 2003) or companies governed by any other special law.',
            'Section 133: the Central Government prescribes standards as recommended by ICAI, in consultation with NFRA.'],
          'Section 129 tells the company to follow the rules; section 143 tells the auditor to blow the whistle if it doesn\'t; section 129(5) tells the company to confess and explain any deviation.',
          'A CA drafting company accounts includes a "deviation from AS" note under section 129(5) whenever a sector law forces a different treatment.'),
        C('c4', T4, [
            'Standards are meant for material items only. An item is material if omitting or misstating it would likely affect the economic decisions of users.',
            'Materiality is not purely about size — the information the item conveys matters. A ₹50,000 penalty for breaking the law may be small against crores of expenses, yet it is material because of what it says about the company. So materiality is judged case by case.',
            'Material items should be shown separately rather than clubbed — penalties should not be buried in legal charges.'],
          'Materiality is like spotting a stain on a shirt: a tiny ink spot on a white collar matters more than a bigger mark on the inside lining.',
          'Auditors scrutinise small but sensitive items — related-party payments, penalties, fraud losses — regardless of amount.'),
        C('c5', T5, [
            'Accounting Standards aim at comparable, transparent and fair financial statements. Tax deductions and exemptions reflect the Government\'s fiscal policy. So an expense charged under an AS is not automatically deductible for tax, and income exempt from tax must still be recognised in the books.',
            'Example: under AS 19 a lessee charges depreciation on an asset taken on finance lease, but for tax purposes depreciation goes to the lessor as legal owner.',
            'ICDS: under the income-tax law the Central Government has notified ten Income Computation and Disclosure Standards (I Accounting Policies; II Valuation of Inventories; III Construction Contracts; IV Revenue Recognition; V Tangible Fixed Assets; VI Effects of Changes in Foreign Exchange Rates; VII Government Grants; VIII Securities; IX Borrowing Costs; X Provisions, Contingent Liabilities and Contingent Assets). They apply from assessment year 2017-18 to assessees following the mercantile system — other than individuals and HUFs not required to get a tax audit — for computing income under the heads business or profession, and other sources. (The study material describes them with reference to section 145(2) of the 1961 Act.)',
            'ICDS govern only the tax computation; the books continue to follow AS.'],
          'AS write the company\'s report card for investors; ICDS write the tax department\'s marking scheme — the same performance can earn different marks in each.',
          'Tax auditors reconcile book profit with taxable profit, listing ICDS adjustments item by item.'),
        C('c6', T6, [
            'ICAI\'s Council (433rd meeting, 13–15 August 2024) revised the criteria for non-company entities. The revised scheme applies to accounting periods commencing on or after 1 April 2024 and replaces the earlier four-level classification (the March 2021 announcement).',
            'There are now just two buckets for non-company entities — MSMEs (micro, small and medium-sized entities) and Large entities.',
            'An MSME must satisfy all five tests in the table; the conditions are checked as at the end of the relevant accounting period. Any other non-company entity is a Large entity and must comply with all AS in full.',
            'The announcement does not apply to non-company entities that must follow Ind AS or AS under their own regulators\' requirements.'],
          'Two lanes on the highway: the MSME lane with some speed-breakers removed, and the Large lane where every rule applies.',
          'A CA classifying an LLP or a trust each year checks the previous year\'s turnover and peak borrowings — a single month above ₹50 crore of borrowing takes it out of the MSME lane.',
          blocks=[msme]),
        C('c7', T7, [
            'MSMEs get exemptions and relaxations (see table). The key ones: AS 3, 17, 20 and 24 do not apply to any MSME; AS 18 and AS 28 do not apply to the smaller MSMEs (turnover up to ₹50 crore and borrowings up to ₹10 crore); AS 22 applies only for current tax.',
            'Conditions for using them: (1) an MSME that uses any exemption discloses that it is an MSME and has complied with AS as applicable to MSMEs; (2) an entity that ceases to be an MSME applies the full standards from the current period, need not restate the previous year\'s figures, and discloses that it was an MSME, used the exemptions and has not restated comparatives; (3) an entity that becomes an MSME after being Large gets the exemptions only after it has remained an MSME for two consecutive years; (4) if it uses exemptions for some but not all standards, it names the standards where it used them; (5) if it forgoes an exemption it must comply fully with that standard; (6) partial use and disclosure must not mislead users.'],
          'Exemptions are a discount coupon: you must say you used it, list where you used it, you only qualify after two straight years in the club, and if you stop qualifying you pay full price from today without re-billing last year.',
          'When an MSME client crosses ₹250 crore turnover, the CA plans for full AS (cash flow statement, segment reporting, EPS) from the current year with the required transition disclosures.',
          blocks=[msme_ex]),
        C('c8', T8, [
            'Companies not on Ind AS follow the AS notified under the Companies (Accounting Standards) Rules, 2021 and are classified as Small and Medium-sized Companies (SMCs) or Non-SMCs.',
            'An SMC is defined by the same five kinds of tests (unlisted; not a bank, FI or insurer; turnover not above ₹250 crore and borrowings not above ₹50 crore in the preceding year; not holding or subsidiary of a non-SMC), satisfied as at the end of the period.',
            'Non-SMCs comply with all AS in full. SMCs: AS 17 does not apply at all; relaxations in AS 15 (but defined-benefit and long-term benefit liabilities must still be determined actuarially by the Projected Unit Credit Method, using government-bond yields), AS 19 (disclosures), AS 20 (diluted EPS disclosure), AS 28 (value in use by reasonable estimate) and AS 29 (paragraphs 66–67 disclosures).',
            'AS 25 never forces anyone to prepare interim reports; it governs them only if a company must (e.g. listed Non-SMCs under SEBI) or chooses to prepare them.',
            'Compare: an SMC still prepares a cash flow statement (AS 3 applies in full to companies), while an MSME non-company entity does not. And SMCs must use actuarial valuation for gratuity; MSMEs may use a simpler rational method.'],
          'SMC relief is narrower than MSME relief — companies get a lighter backpack, non-corporates a much lighter one.',
          'A private company with ₹180 crore turnover and ₹30 crore borrowing still needs an actuary\'s gratuity valuation and a cash flow statement — a common surprise for promoters.',
          blocks=[smc]),
    ]

    illustrations = [
        {'id': 'i1', 'title': 'MSME or Large?', 'difficulty': 'moderate', 'minutes': 8,
         'q': 'Classify each non-company entity for the year 2025-26 under the revised scheme: (a) Anand & Co. (firm): preceding-year turnover ₹210 crore, other income ₹45 crore, peak borrowings ₹38 crore; (b) Bharat LLP: turnover ₹120 crore, but borrowings touched ₹55 crore for two weeks last year; (c) City Co-operative Bank: turnover ₹40 crore; (d) Dhruv Trust: turnover ₹60 crore, borrowings ₹8 crore, debt securities listed on BSE; (e) Ekta & Sons: turnover ₹35 crore, borrowings ₹6 crore, subsidiary of a Large entity.',
         'solution': [table(['Entity', 'Failing test (if any)', 'Category'], [
             ['(a) Anand & Co.', 'None — turnover tested excluding other income (₹210 crore ≤ ₹250 crore)', 'MSME'],
             ['(b) Bharat LLP', 'Borrowings exceeded ₹50 crore at some time in the preceding year', 'Large'],
             ['(c) City Co-operative Bank', 'It is a bank', 'Large'],
             ['(d) Dhruv Trust', 'Its debt securities are listed', 'Large'],
             ['(e) Ekta & Sons', 'Subsidiary of an entity that is not an MSME', 'Large'],
         ]), note('All five conditions must be satisfied; failing any one makes the entity Large.')]},
        {'id': 'i2', 'title': 'Which standards can a small MSME skip?', 'difficulty': 'moderate', 'minutes': 6,
         'q': 'Fern & Co., an unlisted firm, is an MSME with preceding-year turnover of ₹42 crore and peak borrowings of ₹7 crore; it is not part of any group. State whether it must apply: AS 3, AS 18, AS 22 (deferred tax), AS 28, AS 2, AS 9.',
         'solution': [table(['Standard', 'Applies?', 'Reason'], [
             ['AS 3 Cash Flow Statements', 'No', 'Not applicable to any MSME'],
             ['AS 18 Related Party Disclosures', 'No', 'Turnover ≤ ₹50 crore and borrowings ≤ ₹10 crore'],
             ['AS 22 — deferred tax', 'No', 'MSMEs account only for current tax'],
             ['AS 28 Impairment of Assets', 'No', 'Same smaller-MSME band as AS 18'],
             ['AS 2 Valuation of Inventories', 'Yes', 'No exemption'],
             ['AS 9 Revenue Recognition', 'Yes', 'No exemption'],
         ]), note('Fern must disclose that it is an MSME and has complied with AS as applicable to MSMEs.')]},
        {'id': 'i3', 'title': 'Leaving and joining the MSME club', 'difficulty': 'hard', 'minutes': 6,
         'q': 'Garnet Traders was an MSME in 2023-24 and used the AS 3 exemption. Its 2024-25 turnover was ₹290 crore. Separately, Opal LLP was a Large entity until 2023-24 and met all MSME tests in 2024-25 and 2025-26. Explain the AS position of each for 2025-26.',
         'solution': [legal('An entity that ceases to be an MSME applies the full standards from the current period, without restating comparatives, and discloses these facts; an entity that becomes an MSME after being Large gets exemptions only after remaining an MSME for two consecutive years.',
                            'Garnet\'s preceding-year (2024-25) turnover of ₹290 crore exceeds ₹250 crore. Opal has been an MSME for 2024-25 and 2025-26.',
                            'Garnet is Large for 2025-26 and must prepare a cash flow statement and apply all standards from 2025-26. Opal completes two consecutive years as an MSME at the end of 2025-26.',
                            'Garnet: apply full AS in 2025-26; previous-year figures need not be revised; disclose that it was an MSME, availed exemptions and did not revise comparatives. Opal: may avail MSME exemptions from 2025-26 (its second consecutive MSME year), with the MSME disclosure.')]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'The annual classification note', 'role': 'Audit assistant on a group of family firms',
         'situation': 'Your manager asks you to classify five group firms and an LLP for the current year before the audit plan is fixed.',
         'steps': ['Collect last year\'s audited turnover (excluding other income) and the month-wise peak borrowings.', 'Check listing status and whether any entity is a bank, FI or insurer.', 'Map group relationships — an MSME cannot be holding/subsidiary of a non-MSME.', 'Apply the two-consecutive-years rule for entities moving into the MSME band.', 'Record exemptions each entity will use and draft the required disclosure notes.'],
         'takeaway': 'Classification is redone every year from the previous year\'s data and checked as at the period end.',
         'think': 'Why does the test use "at any time during the year" for borrowings but a full-year figure for turnover?',
         'answer': 'Borrowing risk can peak briefly — a year-end figure could hide heavy mid-year debt, so the peak is tested.'},
        {'id': 'j2', 'title': 'Tax vs books on a finance lease', 'role': 'Tax consultant',
         'situation': 'A client (lessee) has charged depreciation on a finance-leased machine and claimed it in the tax return.',
         'steps': ['Book treatment under AS 19 is correct — the lessee depreciates the leased asset.', 'For tax, depreciation belongs to the lessor as legal owner.', 'Disallow the depreciation in the tax computation and claim lease rentals as applicable under tax law.'],
         'takeaway': 'An AS charge does not guarantee a tax deduction.'},
    ]

    mcqs = [
        Q('m1', 'The revised ICAI scheme for classifying non-company entities applies to accounting periods commencing on or after:', ['1 April 2024', '1 April 2023', '13 August 2024', '1 April 2025'], 0,
          'The ICAI Council considered the revision at its meeting of 13–15 August 2024, but the scheme applies to accounting periods commencing on or after 1 April 2024. The tempting trap is the August 2024 meeting date. In practice: a firm with a 2024-25 year already uses the MSME/Large classification even though the announcement came mid-year.', 'c6', T6),
        Q('m2', 'Which is NOT a condition for a non-company entity to be an MSME?', ['Borrowings never exceeded ₹100 crore', 'Turnover (excluding other income) not above ₹250 crore', 'Not a bank or insurance company', 'Not a subsidiary of a non-MSME'], 0,
          'The borrowing limit is ₹50 crore, checked across the whole of the preceding year (the peak counts), not ₹100 crore. The other three options are genuine conditions, along with the listing test. The trap is that ₹100 crore sounds like a plausible larger limit. In practice: a CA checks month-wise loan balances, because one spike above ₹50 crore disqualifies the entity.', 'c6', T6),
        Q('m3', 'For the MSME turnover test, turnover is taken:', ['Excluding other income, for the immediately preceding accounting year', 'Including other income, for the current year', 'Average of the last three years', 'Excluding other income, for the current year'], 0,
          'The test uses turnover excluding other income of the immediately preceding accounting year, while the conditions are checked as at the end of the current period. Including other income or using current-year figures are the usual traps. In practice: interest or rent received by a trading firm is ignored for this test.', 'c6', T6, 'moderate'),
        Q('m4', 'Which Accounting Standard does NOT apply to any MSME?', ['AS 3 Cash Flow Statements', 'AS 9 Revenue Recognition', 'AS 2 Valuation of Inventories', 'AS 1 Disclosure of Accounting Policies'], 0,
          'AS 3, AS 17, AS 20 and AS 24 are not applicable to MSMEs at all. AS 1, AS 2 and AS 9 apply fully because every entity must disclose policies, value inventory and recognise revenue properly. The trap is to think small entities escape all disclosure standards. In practice: an MSME firm\'s accounts have no cash flow statement but still carry a policy note.', 'c7', T7),
        Q('m5', 'AS 18 and AS 28 are not applicable to MSMEs whose preceding-year turnover and borrowings do not exceed:', ['₹50 crore and ₹10 crore', '₹250 crore and ₹50 crore', '₹10 crore and ₹1 crore', '₹100 crore and ₹25 crore'], 0,
          'Within the MSME category, the smaller entities — turnover up to ₹50 crore and borrowings up to ₹10 crore, and not holding/subsidiary of an MSME outside this band — are exempt from AS 18 and AS 28 entirely. ₹250 crore and ₹50 crore are the MSME entry limits, which is the trap. In practice: a mid-sized MSME with ₹120 crore turnover must still give related-party disclosures.', 'c7', T7, 'moderate'),
        Q('m6', 'A Large entity becomes an MSME in 2024-25. It can first avail MSME exemptions:', ['Only after remaining an MSME for two consecutive years', 'Immediately in 2024-25', 'Never', 'Only with ICAI\'s permission'], 0,
          'An entity that was not an MSME and then becomes one qualifies for the exemptions only after it has stayed an MSME for two consecutive years. The trap is "immediately", which would let entities hop in and out of the regime. In practice: the CA keeps a two-year history of classification for each entity.', 'c7', T7),
        Q('m7', 'An MSME stops qualifying in the current year. Which is correct?', ['Apply full AS from the current period; previous-year figures need not be revised; disclose the facts', 'Revise previous-year figures to full AS', 'Continue exemptions for two more years', 'Apply full AS from the next year'], 0,
          'On ceasing to be an MSME the relevant standards apply from the current period, the corresponding previous-year figures need not be revised merely because of the change, and the entity discloses that it was an MSME, used exemptions and has not revised comparatives. The trap is restating last year. In practice: such a firm\'s first cash flow statement may show no comparatives with an explanatory note.', 'c7', T7, 'moderate'),
        Q('m8', 'Under the MSME relaxation for AS 22, an MSME:', ['Accounts only for current tax and adjusts the accumulated deferred tax balance against opening reserves on first use', 'Ignores income-tax altogether', 'Accounts only for deferred tax', 'Charges the accumulated deferred tax to current-year profit'], 0,
          'MSMEs comply with AS 22 only for current tax (recognition, measurement and presentation). On first availing the exemption, the deferred tax asset or liability carried from the previous period is adjusted against opening revenue reserves or owner\'s funds — not routed through current profit. The trap is charging it to profit. In practice: this removes the deferred tax line from small firms\' balance sheets.', 'c7', T7, 'hard'),
        Q('m9', 'Which standard is NOT applicable at all to a Small and Medium-sized Company (SMC)?', ['AS 17 Segment Reporting', 'AS 3 Cash Flow Statements', 'AS 18 Related Party Disclosures', 'AS 15 Employee Benefits'], 0,
          'For SMCs only AS 17 is wholly inapplicable; AS 15, 19, 20, 28 and 29 carry relaxations, and AS 3 and AS 18 apply in full. The trap is AS 3, which MSME non-company entities can skip but companies cannot. In practice: every company not on Ind AS, however small, attaches a cash flow statement unless another law exempts it.', 'c8', T8),
        Q('m10', 'An SMC with a gratuity scheme (a defined benefit plan) must:', ['Still determine the liability actuarially using the Projected Unit Credit Method', 'Use any rational method, such as all employees retiring at year-end', 'Ignore gratuity until paid', 'Follow cash basis'], 0,
          'SMCs are relaxed from some AS 15 paragraphs, but they must still determine defined-benefit and other long-term benefit liabilities actuarially by the Projected Unit Credit Method, with the discount rate based on government bond yields. The "any rational method" option is the MSME relaxation for non-company entities, which is the trap. In practice: even small companies obtain an actuary\'s certificate for gratuity.', 'c8', T8, 'hard'),
        Q('m11', 'AS 25 Interim Financial Reporting requires a company to:', ['Apply it only if the company must or chooses to prepare an interim report', 'Prepare quarterly reports in all cases', 'Prepare half-yearly reports in all cases', 'Never prepare interim reports'], 0,
          'AS 25 does not itself require any interim report; it governs the content and recognition when a company is required (for example SEBI quarterly results of listed companies) or elects to prepare one. The trap is "quarterly reports in all cases". In practice: unlisted companies usually prepare no interim reports and AS 25 then has no work to do.', 'c8', T8),
        Q('m12', 'Accounting Standards apply to an enterprise that collects donations and also runs a small paid canteen because:', ['Even a small commercial activity brings all its activities under AS', 'Charitable enterprises are always covered', 'AS apply only to the canteen part', 'Donations are commercial income'], 0,
          'AS apply unless no part of the enterprise\'s activity is commercial, industrial or business in nature; once even a small part is, AS apply to all its activities, including the non-commercial ones. The trap is "only to the canteen part". In practice: NGOs running training-for-fee or shops must prepare AS-compliant accounts for the whole organisation.', 'c2', T2, 'moderate'),
        Q('m13', 'Under section 129(5) of the Companies Act, 2013, a company not complying with an AS must disclose:', ['The deviation, the reasons and the financial effect', 'Only the name of the standard', 'Nothing if the auditor agrees', 'Only the financial effect'], 0,
          'Section 129(5) requires disclosure of the deviation from the accounting standards, the reasons for it and the financial effects, if any. Mentioning only the standard or only the effect is incomplete; an auditor\'s agreement does not remove the disclosure. In practice: such notes often arise where a sector regulator prescribes a different treatment.', 'c3', T3),
        Q('m14', 'A company pays a penalty of ₹50,000 for a legal violation; its annual expenses run into hundreds of crores. Under the AS framework the penalty:', ['Is material and should be shown separately because of its nature', 'Is immaterial because of its size', 'Should be clubbed with legal charges', 'Need not be recorded'], 0,
          'Materiality depends on the size and the nature of the item; a penalty for breaking the law conveys important information about the company even if the amount is small, so it is material and should not be clubbed with legal charges. The trap is judging by size alone. In practice: auditors list such penalties for disclosure regardless of amount.', 'c4', T4),
        Q('m15', 'An expense charged in the books under an Accounting Standard is:', ['Not automatically deductible for income-tax', 'Always deductible for income-tax', 'Never deductible for income-tax', 'Deductible only for companies'], 0,
          'AS aim at fair presentation, while tax deductions depend on the tax law and fiscal policy, so an AS charge may or may not be deductible. Example: a lessee depreciates a finance-leased asset under AS 19, but the tax depreciation goes to the lessor as owner. The traps "always" and "never" ignore that the two systems are independent. In practice: tax audits reconcile such differences line by line.', 'c5', T5),
        Q('m16', 'How many Income Computation and Disclosure Standards (ICDS) have been notified?', ['10', '27', '29', '12'], 0,
          'Ten ICDS have been notified (I to X), from Accounting Policies to Provisions, Contingent Liabilities and Contingent Assets, applicable from assessment year 2017-18. 27 is the number of AS in force and 29 the number issued. In practice: ICDS adjustments appear in the tax audit report and the return, not in the books.', 'c5', T5, check='10'),
    ]

    questions = [
        W('q1', 5, 'Under ICAI\'s August 2024 announcement, how are non-company entities now grouped for the purpose of Accounting Standards? From when does the new grouping apply?',
          [p('The revised scheme is effective for accounting periods beginning on or after 1 April 2024. It sorts non-company entities into just two groups — MSMEs and Large entities.'),
           p('To be an MSME, an entity must pass all of these tests, checked as at the end of the relevant period: (i) its shares or debt securities are unlisted and no listing is in process, in India or abroad; (ii) it is neither a bank nor a financial institution nor an insurer; (iii) its turnover for the preceding year, leaving out other income, is ₹250 crore or less; (iv) its borrowings never went above ₹50 crore during the preceding year; (v) it is neither the holding entity nor a subsidiary of any entity that falls outside the MSME category.'),
           p('Any non-company entity failing even one test is a Large entity. Large entities comply with all Accounting Standards in full; MSMEs get specified exemptions and relaxations.')],
          [S('s1', 'Effective date — periods from 1 April 2024', 0.5, 'provision', '2024'),
           S('s2', 'Two categories — MSME and Large', 1, 'concept', 'msme|micro small', 'large'),
           S('s3', 'Listing and bank/FI/insurer tests', 1, 'provision', 'unlisted|not listed|no listing|not be listed', 'neither a bank|not a bank|nor a bank|not be a bank|nor an insurer|not an insurer'),
           S('s4', 'Turnover ≤ ₹250 crore and borrowings ≤ ₹50 crore (preceding year)', 1.5, 'provision', 'turnover', 'borrow', nums=[2500000000, 500000000]),
           S('s5', 'Group test and Large entity complies in full', 1, 'provision', 'neither the holding|not a holding|not holding|not be a holding|nor a subsidiary|holding entity', 'full|all accounting standards|entirety')],
          ['Write the ₹ limits exactly; "₹250 crore" and "₹50 crore" carry the marks.'],
          ['Quoting the old four-level classification.', 'Using current-year turnover or including other income.'],
          ['List the five MSME conditions as (i)–(v).']),
        W('q2', 5, 'State the additional requirements (conditions and disclosures) that apply when an MSME avails the exemptions or relaxations given to it.',
          [ul(['An MSME availing exemptions discloses in a note that it is an MSME and has complied with AS as far as applicable to an MSME.',
               'If it no longer qualifies, the relevant standards apply from the current period; previous-year figures need not be revised, and it discloses that it was an MSME, availed exemptions and did not revise the previous-year figures.',
               'An entity that becomes an MSME after not being one gets the exemptions only after remaining an MSME for two consecutive years.',
               'If it avails exemptions for some but not all standards, it discloses the standards for which it has availed them.',
               'If it does not avail an exemption, it complies fully with that standard; partial use of exemptions must not mislead users.'])],
          [S('s1', 'Disclosure of MSME status and compliance', 1, 'provision', 'disclos', 'msme'),
           S('s2', 'Ceasing — current period, no restatement, disclose', 1.5, 'provision', 'current period|current year', 'not revis|need not be revised|no revision|not restat|without restat'),
           S('s3', 'Two consecutive years before exemptions', 1, 'provision', 'two consecutive|2 consecutive|two years'),
           S('s4', 'Name the standards where exemption used', 0.5, 'provision', 'standard', 'avail'),
           S('s5', 'Not availing → comply fully; not misleading', 1, 'provision', 'comply|full', 'must not mislead|not mislead|should not mislead|not be misleading|not misleading')],
          ['Students often omit the "no restatement of comparatives" point.'],
          ['Saying the previous year must be restated.', 'Allowing exemptions in the very first year of qualifying.'],
          ['Five numbered points match the five marks.']),
        W('q3', 6, 'Determine with reasons the category and the position regarding AS 3 for each of the following for 2025-26: (a) Hira Ltd., unlisted company, turnover ₹190 crore, borrowings ₹40 crore; (b) Jade & Co., a partnership, turnover ₹190 crore, borrowings ₹40 crore; (c) Kesar LLP, turnover ₹270 crore (including other income ₹35 crore), borrowings ₹20 crore; (d) Lotus Ltd., unlisted company, turnover ₹300 crore. All figures relate to the preceding year; no group links; none is a bank, FI or insurer.',
          [table(['Entity', 'Category', 'AS 3 Cash Flow Statement'], [
              ['(a) Hira Ltd.', 'SMC (company within ₹250 crore turnover and ₹50 crore borrowings)', 'Applies — AS 3 is not exempted for companies'],
              ['(b) Jade & Co.', 'MSME (non-company entity within the limits)', 'Not applicable — exempt for all MSMEs'],
              ['(c) Kesar LLP', 'MSME — turnover excluding other income is ₹235 crore', 'Not applicable'],
              ['(d) Lotus Ltd.', 'Non-SMC (turnover above ₹250 crore)', 'Applies in full'],
          ]), note('Same numbers, different answers for a company and a firm: AS 3 relief exists only for MSME non-company entities.')],
          [S('s1', 'Hira — SMC, AS 3 applies', 1.5, 'application', 'hira', 'smc|small and medium sized compan|small and medium-sized compan'),
           S('s2', 'Jade — MSME, AS 3 not applicable', 1.5, 'application', 'jade', 'msme', 'not applicable|exempt|not required|need not'),
           S('s3', 'Kesar — turnover excluding other income ₹235 crore → MSME', 1.5, 'application', 'kesar', 'msme', 'other income|excluding', nums=[2350000000]),
           S('s4', 'Lotus — Non-SMC, AS 3 applies', 1.5, 'application', 'lotus', 'non smc|non-smc|not an smc|not smc|not a small', 'appl|required|must|full')],
          ['The trap is (a): many candidates exempt the SMC from AS 3.'], ['Testing turnover including other income for Kesar.'],
          ['Make a three-column table: entity, category with reason, AS 3 position.'], pad='table', difficulty='moderate',
          checks=[{'expr': '270-35', 'value': 235, 'label': 'Kesar turnover excluding other income (₹ crore)'}]),
    ]

    viva = [
        V('v1', 'What three questions decide whether an Accounting Standard applies?',
          'First, does it apply to the enterprise concerned? Second, does it apply to the financial statement concerned? Third, does it apply to the financial item concerned?',
          [P('p1', 'Enterprise', 3, 'enterprise|entity'), P('p2', 'Financial statement', 3, 'financial statement|statement'), P('p3', 'Financial item', 4, 'item')], 'c1'),
        V('v2', 'State the five conditions for a non-company entity to be an MSME.',
          'It must not be listed or in the process of listing; it must not be a bank, an insurer or a financial institution; its preceding year turnover, leaving out other income, must not exceed 250 crore; its borrowings must not exceed 50 crore at any time in the preceding year, and it must not be a holding or subsidiary of a non MSME.',
          [P('p1', 'Not listed', 2, 'not be listed|not listed|unlisted|must not be listed'), P('p2', 'Not a bank, FI or insurer', 2, 'bank|insur|financial institution'),
           P('p3', 'Turnover up to ₹250 crore', 2, '250 crore|two hundred and fifty crore'), P('p4', 'Borrowings up to ₹50 crore', 2, '50 crore|fifty crore'),
           P('p5', 'Not holding/subsidiary of non-MSME', 2, 'not be a holding|not a holding|not holding|nor a subsidiary')], 'c6'),
        V('v3', 'Which Accounting Standards are not applicable to any MSME?',
          'Four standards are switched off for every MSME: cash flow statements under AS 3, segment reporting under AS 17, earnings per share under AS 20 and discontinuing operations under AS 24.',
          [P('p1', 'AS 3', 3, 'as 3|cash flow'), P('p2', 'AS 17', 2, 'as 17|segment'), P('p3', 'AS 20', 3, 'as 20|earnings per share|eps'), P('p4', 'AS 24', 2, 'as 24|discontinu')], 'c7'),
        V('v4', 'How does relief for an SMC differ from relief for an MSME?',
          'An SMC is a company and gets narrower relief: only AS 17 is fully exempt, it must still prepare a cash flow statement, and it must value gratuity actuarially using the projected unit credit method. An MSME non company entity is exempt from AS 3, 17, 20 and 24 and may use a simpler rational method for employee benefits.',
          [P('p1', 'SMC — only AS 17 fully exempt', 3, 'smc|compan', 'as 17|segment'), P('p2', 'SMC still prepares cash flow (AS 3)', 2, 'cash flow|as 3'),
           P('p3', 'SMC — actuarial / projected unit credit', 3, 'actuar|projected unit credit'), P('p4', 'MSME — simpler rational method', 2, 'rational|simpler')], 'c8'),
        V('v5', 'Is every expense charged under an Accounting Standard deductible for income tax? Give an example.',
          'No. Accounting Standards aim at fair presentation while deductions depend on tax law. For example, a lessee depreciates a finance leased asset under AS 19, but tax depreciation is allowed to the lessor as legal owner.',
          [P('p1', 'Not automatically deductible', 4, 'not|no'), P('p2', 'Tax law / fiscal policy decides', 2, 'tax law|fiscal|income tax act|tax rule'),
           P('p3', 'Finance lease example — lessor gets tax depreciation', 4, 'lease', 'lessor|owner')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'The Mehra group\'s compliance map', 'difficulty': 'hard',
              'case': 'The Mehra group has: Mehra Foods Pvt. Ltd. (unlisted, turnover ₹160 crore, borrowings ₹30 crore); Mehra Exports, a partnership firm (turnover ₹45 crore, borrowings ₹9 crore, not part of any holding structure); and Mehra Agro LLP, which was a Large entity until 2023-24 and met the MSME tests in 2024-25. All turnover figures exclude other income and relate to the preceding year. The year under review is 2024-25.',
              'mcqs': [
                  M('k1a', 'Mehra Foods Pvt. Ltd. is classified as:', ['SMC', 'MSME', 'Large entity', 'Non-SMC'], 0,
                    'Mehra Foods is a company, so the Companies (Accounting Standards) Rules, 2021 classification applies — it is within the ₹250 crore turnover and ₹50 crore borrowing limits and unlisted, so it is an SMC. MSME and Large are categories for non-company entities, which is the trap. In practice: the same numbers can lead to different labels for a company and a firm.', 'moderate', topic=T8),
                  M('k1b', 'Mehra Exports need not apply:', ['Six standards: AS 3, 17, 18, 20, 24 and 28', 'Only AS 3', 'Any Accounting Standard', 'Only AS 17'], 0,
                    'As an MSME it is exempt from AS 3, 17, 20 and 24; with turnover up to ₹50 crore and borrowings up to ₹10 crore it is also outside AS 18 and AS 28. "Any Accounting Standard" is wrong — AS 1, 2, 9 and others still apply. In practice: the firm\'s accounts will carry a note that it is an MSME and has complied with AS as applicable to MSMEs.', 'hard', topic=T7),
                  M('k1c', 'Mehra Agro LLP, for 2024-25:', ['Cannot yet avail MSME exemptions', 'Avails all MSME exemptions immediately', 'Must restate 2023-24 figures', 'Is a Large entity forever'], 0,
                    'An entity that was not an MSME and then becomes one gets the exemptions only after remaining an MSME for two consecutive years; 2024-25 is only its first year. Restatement relates to entities leaving the MSME category. In practice: Agro LLP prepares full-AS accounts for 2024-25 and may avail exemptions from 2025-26 if it still qualifies.', 'hard', topic=T7),
                  M('k1d', 'Mehra Foods Pvt. Ltd. must prepare a cash flow statement because:', ['AS 3 has no exemption for SMCs', 'It is a Large entity', 'Its borrowings exceed ₹10 crore', 'All companies must apply Ind AS'], 0,
                    'For companies not on Ind AS only AS 17 is wholly inapplicable to SMCs; AS 3 applies in full. "Large entity" is a non-company category, and the ₹10 crore borrowing limit relates to the smaller-MSME band for AS 18/28. In practice: promoters of small private companies are often surprised that a cash flow statement is still required.', 'moderate', topic=T8),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch03', 1, 'Applicability of Accounting Standards',
                ['Apply the three-step test (enterprise, statement, item) and explain the mandatory status of AS.',
                 'Link AS compliance with sections 129, 133 and 143 of the Companies Act, 2013.',
                 'Explain materiality and the difference between AS and tax rules, including the ten ICDS.',
                 'Classify non-company entities as MSME or Large under the revised scheme from 1 April 2024 and apply the exemptions and conditions.',
                 'Classify companies as SMC or Non-SMC and state the relaxations available to SMCs.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 35}, 'prereq': ['int-p1-ch01-u01'],
                 'exam_tip': 'Scenario MCQs test the MSME limits (₹250 crore / ₹50 crore; ₹50 crore / ₹10 crore for AS 18 and 28), the two-consecutive-years rule and the difference between SMC and MSME relief.'},
                concepts, illustrations, jobs, mcqs, questions,
                {'summary': ['Three questions: enterprise → statement → item.', 'AS apply to all commercial/industrial/business enterprises; any commercial part brings the whole entity in.',
                             'Companies: s.129(1) comply; s.129(5) disclose deviation, reasons, effect; s.143(3)(e) auditor reports; s.133 Government prescribes.',
                             'Materiality depends on size and nature; show material items separately.', 'AS ≠ tax: ten ICDS for tax computation from AY 2017-18.',
                             'Non-company: MSME (5 tests: unlisted, not bank/FI/insurer, turnover ≤ ₹250 cr, borrowings ≤ ₹50 cr, not group of non-MSME) or Large (full AS). From periods beginning 1 April 2024.',
                             'MSME relief: AS 3, 17, 20, 24 out; AS 18, 28 out for turnover ≤ ₹50 cr & borrowings ≤ ₹10 cr; AS 22 current tax only; AS 15 rational method.',
                             'Companies: SMC (AS 17 out; relaxations in AS 15, 19, 20, 28, 29) or Non-SMC (full).'],
                 'remember': ['Two consecutive years as MSME before exemptions.', 'Ceasing MSME: full AS from current period, no restatement, disclose.', 'SMC gratuity: actuarial, Projected Unit Credit Method.'],
                 'traps': ['Turnover excludes other income; borrowings tested at ANY time in the preceding year.', 'SMCs still prepare cash flow statements.', 'AS 25 never forces interim reports.']},
                [('MSME limits', 'Turnover ≤ ₹250 cr (excl. other income) · borrowings ≤ ₹50 cr (any time) — preceding year'),
                 ('Small-MSME band', 'Turnover ≤ ₹50 cr & borrowings ≤ ₹10 cr → AS 18, AS 28 not applicable'), ('Not for any MSME', 'AS 3 · AS 17 · AS 20 · AS 24'),
                 ('Not for SMC', 'AS 17 (others relaxed: 15, 19, 20, 28, 29)'), ('Companies Act', 's.129(1) comply · s.129(5) disclose deviation · s.133 prescribe · s.143(3)(e) audit report'),
                 ('Entry rule', 'Exemptions only after two consecutive MSME years'), ('ICDS', '10 standards, from AY 2017-18')],
                viva, cases,
                topics=['Introduction', 'Applicability of Accounting Standards', 'Revised Criteria for Classification of Non-company Entities',
                        'Applicability of Accounting Standards to Companies'])
