"""CA Intermediate · Paper 3A Income-tax Law · Chapter 2 Residential Status and Scope of Total Income (Income-tax Act, 2025; tax year 2026-27).
Scope follows the ICAI study material; section numbers are taken from it; explanations and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-a-ch02-u01'
T1 = 'Basic conditions for an individual'
T2 = 'Exceptions: leaving India, visiting India, crew'
T3 = 'Deemed resident (s. 6(7))'
T4 = 'Ordinarily resident or not (s. 6(13))'
T5 = 'HUF, firm, AOP, company and others'
T6 = 'Scope of total income (s. 5)'
T7 = 'Accrual, receipt and deemed receipt (s. 7)'
T8 = 'Income deemed to accrue or arise in India (s. 9)'


def build():
    i1 = {'id': 'i1', 'title': 'Five residential-status puzzles', 'difficulty': 'moderate', 'minutes': 12,
          'q': 'Determine status for tax year 2026-27: (a) Kiran, Indian citizen, leaves India for the first time on 25 September 2026 for a job in Germany (in India 177 days). (b) Meera, Indian citizen living in Dubai, visits India for 125 days; Indian income ₹18 lakh; 450 days in India in the preceding 4 years. (c) Same as (b) but Indian income ₹9 lakh. (d) Leo, a British citizen, has visited India 100 days every year for 10 years. (e) Rohan, Indian citizen in a no-tax country, not liable to tax there, Indian income ₹20 lakh, 30 days in India.',
          'solution': [table(['Person', 'Test applied', 'Status'], [
              ['(a) Kiran', 'Leaving for employment — only the 182-day test; 177 < 182', 'Non-resident'],
              ['(b) Meera', 'Visiting, Indian income > ₹15 lakh — 120 days + 365 days in 4 years met; stay 120–181 days', 'Resident but not ordinarily resident'],
              ['(c) Meera with ₹9 lakh', 'Visiting, Indian income ≤ ₹15 lakh — only the 182-day test applies', 'Non-resident'],
              ['(d) Leo', '100 ≥ 60 and 400 ≥ 365 → resident; 700 days in 7 years ≤ 729', 'Resident but not ordinarily resident'],
              ['(e) Rohan', 'Indian citizen, not liable to tax elsewhere, Indian income > ₹15 lakh', 'Deemed resident — always not ordinarily resident']], title='Answer'),
              note('"Indian income" here means total income other than income from foreign sources.')],
          'checks': []}

    ck2 = Checks()
    ror = ck2.add('25000+12000+18000+7000+30000+60000+14000+45000+11000+9000+22000+13000+17000+6000+10000+19000+4000', 'ROR: global income')
    rnor = ck2.add('25000+6000+18000+15000+60000+14000+11000+9000+22000+6000+10000+4000', 'RNOR: Indian income + business controlled/profession set up in India')
    nr = ck2.add('25000+6000+18000+15000+35000+14000+11000+9000+22000+10000+4000', 'NR: income received or accruing in India')
    rows = [
        ['Profits of a shop in Pune', '25,000', '25,000', '25,000'],
        ['Interest on UK government bonds, half received in India', '12,000', '6,000', '6,000'],
        ['STCG on shares of an Indian company, sale proceeds received in Paris', '18,000', '18,000', '18,000'],
        ['Dividend from a French company, received in Paris', '7,000', '—', '—'],
        ['LTCG on machinery sold in France, half received in India', '30,000', '15,000', '15,000'],
        ['Profits of a business in France controlled from Bengaluru (₹35,000 received in India)', '60,000', '60,000', '35,000'],
        ['Profits of a business in Jaipur managed from Paris', '14,000', '14,000', '14,000'],
        ['Rent of a flat in Paris banked there and later sent to India', '45,000', '—', '—'],
        ['Interest on debentures of an Indian company, received in Paris', '11,000', '11,000', '11,000'],
        ['Fees for technical services rendered in India, received abroad', '9,000', '9,000', '9,000'],
        ['Profits of a business in Kolkata managed from Paris', '22,000', '22,000', '22,000'],
        ['Rent of a house in Sri Lanka, received there', '13,000', '—', '—'],
        ['Untaxed foreign income of earlier years brought to India', '—', '—', '—'],
        ['Agricultural income from land in Sri Lanka, received there', '17,000', '—', '—'],
        ['Income of a profession in Kenya set up in India, received there', '6,000', '6,000', '—'],
        ['Savings bank interest in India', '10,000', '10,000', '10,000'],
        ['Profits of a business in Vietnam controlled from Vietnam', '19,000', '—', '—'],
        ['Dividend from an Indian company', '4,000', '4,000', '4,000'],
        ['Gross total income', inr(ror), inr(rnor), inr(nr)]]
    i2 = {'id': 'i2', 'title': 'One set of incomes, three statuses', 'difficulty': 'hard', 'minutes': 15,
          'q': 'Compute gross total income of Varun for tax year 2026-27 if he is (a) ROR, (b) RNOR, (c) non-resident, from the items listed in the solution table.',
          'solution': [table(['Particulars', 'ROR ₹', 'RNOR ₹', 'NR ₹'], rows, title='Gross total income'),
                       note('Remittance of income already earned abroad is not "receipt" in India; agricultural income from foreign land is taxable for an ROR.')],
          'checks': list(ck2)}

    basic = table(['Who', '182-day test', 'Alternative test'], [
        ['Any individual (general rule)', '182 days or more in the tax year', '60 days or more in the year AND 365 days or more in the 4 preceding years'],
        ['Indian citizen leaving India for employment abroad, or as crew of an Indian ship', 'Applies', 'Not available'],
        ['Indian citizen / person of Indian origin visiting India, Indian income ≤ ₹15 lakh', 'Applies', 'Not available'],
        ['Indian citizen / PIO visiting India, Indian income > ₹15 lakh', 'Applies', '120 days or more in the year AND 365 days in 4 preceding years (then RNOR)'],
    ], title='Is the individual resident?')
    nor = table(['Not ordinarily resident if any of these', 'Ordinarily resident only if both'], [
        ['Non-resident in 9 of the 10 preceding tax years, or', 'Resident in at least 2 of the 10 preceding tax years, and'],
        ['729 days or less in India in the 7 preceding tax years, or', '730 days or more in India in the 7 preceding tax years'],
        ['Resident only through the 120-day visiting rule, or', ''],
        ['Deemed resident under s. 6(7)', ''],
    ], title='RNOR vs ROR (s. 6(13))')
    scope = table(['Income', 'ROR', 'RNOR', 'NR'], [
        ['Received or deemed received in India', 'Taxable', 'Taxable', 'Taxable'],
        ['Accrues or deemed to accrue in India', 'Taxable', 'Taxable', 'Taxable'],
        ['Accrues outside India from a business controlled from India or a profession set up in India', 'Taxable', 'Taxable', 'Not taxable'],
        ['Accrues and received outside India — any other', 'Taxable', 'Not taxable', 'Not taxable'],
    ], title='Scope of total income (s. 5)')
    s9 = table(['Income', 'Deemed to accrue in India when'], [
        ['Through asset, property, source, business connection in India or transfer of a capital asset in India', 'Always (s. 9(2)); business income only to the extent attributable to Indian operations'],
        ['Salary', 'Services rendered in India (including rest or leave period between Indian service); or paid by Government to an Indian citizen for service abroad (s. 9(3))'],
        ['Dividend', 'Paid by an Indian company outside India (s. 9(4))'],
        ['Interest', 'Payable by Government; by a resident (unless for business abroad or earning foreign income); by a non-resident if borrowed for business in India (s. 9(5))'],
        ['Royalty', 'Payable by Government; by a resident (same exceptions); by a non-resident for business in India or earning Indian income (s. 9(6))'],
        ['Fees for technical services', 'Same pattern as royalty (s. 9(7)); taxable even if services rendered outside India and no place of business here (s. 9(11))'],
        ['Gifts', 'Sums taxable under s. 92(2)(m) paid without consideration by a resident to a non-resident, foreign company or RNOR (s. 9(8))'],
    ], title='Income deemed to accrue or arise in India (s. 9)')

    concepts = [
        C('c1', T1, [
            'Total income (s. 2(108)) is the income in section 5 computed as per the Act. Its scope depends on residential status, determined afresh for each tax year under section 6.',
            'Individuals and HUFs can be resident and ordinarily resident (ROR), resident but not ordinarily resident (RNOR) or non-resident (NR); other persons are only resident or non-resident.',
            'An individual is resident if in India for 182 days or more in the tax year, or 60 days or more in the year plus 365 days or more in the four preceding years (table for exceptions).',
            'Counting rules: both arrival and departure days count; stay need not be continuous or at one place; stay in territorial waters (12 nautical miles) counts; residence is independent of citizenship.',
            'Person of Indian origin (s. 2(78)): the individual, either parent or any grandparent was born in undivided India. "Income from foreign sources" means income accruing outside India and not deemed to accrue in India, excluding income from a business controlled from India or a profession set up in India.'],
          'The 182-day rule is the main gate; the 60 + 365 rule is a side gate that some visitors and emigrants cannot use.',
          'A foreign executive spending 70 days a year in India for five years becomes resident once the 4-year total crosses 365 days.',
          blocks=[basic]),
        C('c2', T2, [
            'For an Indian citizen leaving India in the year for employment abroad, or as a crew member of an Indian ship, the 60-day alternative does not apply — only 182 days.',
            'For an Indian citizen or PIO who lives abroad and visits India: if total income other than foreign-source income is ₹15 lakh or less, only the 182-day test applies; if above ₹15 lakh, the 60-day figure becomes 120 days (with 365 days in four years) — and a person resident only by this route is RNOR.',
            'For an Indian citizen who is crew on a foreign-bound ship, days between the Continuous Discharge Certificate dates of joining and signing off for an eligible voyage (international traffic to or from an Indian port) are excluded (Rule 8).'],
          'Emigrants and visitors get a stricter test so that short trips home don\'t make them taxable on world income.',
          'An Indian seafarer whose CDC shows 187 days on an eligible voyage counts only the remaining days of the year.'),
        C('c3', T3, [
            'Section 6(7): an Indian citizen whose total income other than foreign-source income exceeds ₹15 lakh, and who is not liable to tax in any other country by reason of domicile, residence or similar criteria, is deemed resident — even with no stay in India.',
            '"Liable to tax" (s. 2(66)) means a tax liability under that country\'s law, including where later exempted.',
            'It does not apply if the person is already resident under the day-count rules. Only citizens (not PIOs) can be deemed residents, and a deemed resident is always RNOR.'],
          'Deemed residence closes the "stateless taxpayer" loophole for wealthy citizens who are taxed nowhere.',
          'An Indian citizen living in a zero-tax jurisdiction with ₹20 lakh of Indian rent is deemed resident (RNOR).'),
        C('c4', T4, [
            'A resident individual is RNOR if any condition in the table applies; otherwise ROR. Equivalently, ROR needs residence in at least 2 of the 10 preceding years AND 730+ days in the 7 preceding years.',
            'Residents by the 120-day visiting rule and deemed residents are always RNOR.'],
          'Ordinary residence asks whether the person has really put down roots, not just visited.',
          'A returning NRI is usually RNOR for the first year or two after coming back.',
          blocks=[nor]),
        C('c5', T5, [
            'HUF: resident if control and management of its affairs is wholly or partly in India; non-resident if wholly outside. A resident HUF is ROR only if the Karta satisfies both ordinary-residence conditions; else RNOR.',
            'Control and management means de facto central control — the "head and brain" — not day-to-day operations or a mere right to control.',
            'Firm, AOP, BOI, local authority and artificial juridical person: resident if control and management is wholly or partly in India. Partners\' or members\' status is irrelevant.',
            'Company: resident if it is Indian, or if for that year its place of effective management (POEM) — where key management and commercial decisions for the business as a whole are in substance made — is in India in that year (s. 220 deals with POEM transition; Final level).'],
          'For bodies, residence follows the brain (control), not the hands (operations).',
          'An Indian company run entirely from London is still resident because it is Indian.'),
        C('c6', T6, [
            'Section 5 sets scope by status (table). Three factors decide taxability: residential status, place of accrual or receipt (actual or deemed), and time of accrual or receipt.',
            'All persons are taxed on income received or deemed received in India and income accruing or deemed to accrue in India. Only ROR (and other residents) are taxed on income arising outside India; RNOR only where it comes from a business controlled from India or a profession set up in India.',
            'Salary of non-resident seafarers for service outside India on foreign-going ships, credited to an NRE account in India, is not included (CBDT Circulars 13/2017 and 17/2017).'],
          'ROR pays tax on the whole world, RNOR on India plus Indian-run foreign business, NR only on India.',
          'An NRI\'s rent from a flat in Pune is taxable in India wherever it is received.',
          blocks=[scope]),
        C('c7', T7, [
            'Income accrues when the right to receive it arises; it is due when payment can be enforced (e.g. December salary accrues daily, falls due at month-end).',
            'Receipt means the first occasion the money comes under the recipient\'s control; later remittance to India is not a receipt in India. Income taxed on accrual cannot be taxed again on receipt; showing foreign income in a balance sheet prepared in India is not receipt.',
            'Deemed receipt (s. 7(1)): interest credited to a recognised provident fund above 9.5% p.a., transfer of employer\'s contribution and interest from an unrecognised to a recognised PF, and contributions by the Central Government or other employer to an employee\'s pension scheme under s. 124.'],
          'Income is caught at its first landing — moving it from one bank to another later does not create a new landing.',
          'Foreign rent banked in London and later wired to India is not "received in India".'),
        C('c8', T8, [
            'Certain income is deemed to accrue in India though it actually arises outside (table).',
            'Capital gains on transfer of a capital asset situated in India are deemed to arise in India whatever the place of transfer, registration or payment.',
            'Activities not treated as business in India for a non-resident (s. 9(9)(c)): purchasing goods in India for export; collecting news for transmission abroad by news agencies or publishers; displaying uncut diamonds in notified zones by foreign mining companies; and film shooting in India by non-citizen individuals or by firms/companies with no Indian-citizen or resident partners/shareholders.',
            'Royalty covers patents, designs, trade marks, know-how, equipment use, copyright including films and broadcasting, computer software licences — excluding amounts taxable as capital gains. Fees for technical services means consideration for managerial, technical or consultancy services, excluding construction/assembly/mining projects and salary.',
            'Allowances and perquisites paid abroad by Government to an Indian citizen for service abroad are exempt (Schedule III, Table Sl. No. 9) in both regimes, though the salary itself is deemed to accrue in India.'],
          'Section 9 is the long arm of Indian tax law — it reaches income that physically arises abroad but whose roots are in India.',
          'A Colombo consultant advising on an Indian project is taxed in India on his fee even if he never visits.',
          blocks=[s9]),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Status for a returning NRI', 'role': 'Tax associate',
         'situation': 'A client returned to India on 1 April 2025 after 30 years in the US (30 days a year in India).',
         'steps': ['Check 182 days → resident for 2026-27.', 'Check 2 of 10 years resident: only 2025-26 → fails; 730 days in 7 years: 30 × 6 + 365 < 730 → fails.', 'Conclude RNOR; foreign income not taxed unless from India-controlled business.'],
         'takeaway': 'RNOR status gives returning NRIs a transition window.'},
        {'id': 'j2', 'title': 'Withholding on a foreign consultant', 'role': 'Finance executive',
         'situation': 'Company pays a Singapore consultant for advice on an Indian plant.',
         'steps': ['Fees for technical services utilised in India are deemed to accrue in India (s. 9(7)).', 'Section 9(11): taxable even though rendered outside India.', 'Consider TDS before remitting.'],
         'takeaway': 'Where services are used, not where rendered, decides FTS taxability.'},
    ]

    mcqs = [
        Q('m1', 'Nikhil, an Indian citizen, went abroad for the first time on 18 September 2026 to join a job in Canada and spent 170 days in India in tax year 2026-27. He is:', ['Non-resident', 'Resident and ordinarily resident', 'Resident but not ordinarily resident', 'Deemed resident'], 0,
          'For an Indian citizen leaving India for employment, only the 182-day test applies; 170 days is less, so he is non-resident even though he exceeds 60 days. In practice: the date of departure is critical.', 'c2', T2),
        Q('m2', 'Sana, an Indian citizen settled in Qatar, spends 135 days in India during the year, earns ₹19 lakh from Indian sources and spent 420 days in India over the preceding four years. She is:', ['Resident but not ordinarily resident', 'Non-resident', 'Resident and ordinarily resident', 'Deemed resident'], 0,
          'With Indian income above ₹15 lakh, the alternative test becomes 120 days plus 365 days in four years, which she meets; such a resident is RNOR. In practice: high-income visitors must watch the 120-day mark.', 'c2', T2, 'moderate'),
        Q('m3', 'Which of these can be a deemed resident under section 6(7)?', ['An Indian citizen not liable to tax elsewhere with Indian income above ₹15 lakh', 'A person of Indian origin with Indian income above ₹15 lakh', 'A foreign citizen living in India', 'A company incorporated abroad'], 0,
          'Only Indian citizens can be deemed residents, and only where Indian income exceeds ₹15 lakh and they are not liable to tax in another country by domicile or residence. PIOs and foreigners are excluded. In practice: a deemed resident is always RNOR.', 'c3', T3),
        Q('m4', 'Ishita stayed 195 days in India this year and 810 days over the 7 preceding years; she was non-resident in 8 of the 10 preceding years. She is:', ['Resident and ordinarily resident', 'Resident but not ordinarily resident', 'Non-resident', 'Deemed resident'], 0,
          'She is resident (195 ≥ 182). She was resident in 2 of 10 years (non-resident in 8) and stayed 810 ≥ 730 days in 7 years, so both conditions for ordinary residence are met. In practice: count carefully — 8 out of 10 non-resident still leaves 2 resident years.', 'c4', T4, 'moderate'),
        Q('m5', 'An individual is not ordinarily resident if he has been in India in the 7 preceding years for:', ['729 days or less', '730 days or more', '365 days or less', '182 days or less'], 0,
          'Section 6(13) treats a resident as not ordinarily resident if he was non-resident in 9 of 10 preceding years or in India for 729 days or less in the 7 preceding years. 730 or more is needed for ordinary residence. In practice: one day can change status.', 'c4', T4, 'core', check=729),
        Q('m6', 'A HUF whose affairs are controlled partly from Delhi and partly from Dubai, with a Karta satisfying both additional conditions, is:', ['Resident and ordinarily resident', 'Resident but not ordinarily resident', 'Non-resident', 'Deemed resident'], 0,
          'Partial control in India makes the HUF resident, and the Karta meeting both ordinary-residence conditions makes it ROR. If control were wholly abroad it would be non-resident. In practice: the Karta\'s history decides ROR vs RNOR.', 'c5', T5),
        Q('m7', 'An Indian company whose entire business is run from Singapore is:', ['Resident in India', 'Non-resident', 'RNOR', 'Deemed resident'], 0,
          'An Indian company is always resident; the place of effective management test matters only for foreign companies. Companies can never be RNOR, which is a status only for individuals and HUFs. In practice: Indian companies pay tax on their global income.', 'c5', T5),
        Q('m8', 'Income of an RNOR accruing outside India is taxable only if:', ['It is derived from a business controlled from India or a profession set up in India', 'It exceeds ₹15 lakh', 'It is later remitted to India', 'It is from a foreign government'], 0,
          'Section 5 includes, for an RNOR, foreign income derived from a business controlled from India or a profession set up in India; other foreign income is excluded even if later remitted. In practice: returning NRIs keep foreign investment income outside the net for a while.', 'c6', T6),
        Q('m9', 'Rent from a London property, deposited in a London bank and later remitted to India, is taxable for:', ['An ROR only', 'All three statuses', 'RNOR and ROR', 'Non-residents only'], 0,
          'Income first received abroad is not received in India merely because it is later remitted; it is foreign income taxable only for an ROR. RNOR and NR exclude it. In practice: the first point of receipt is decisive.', 'c7', T7),
        Q('m10', 'Under section 7(1), interest credited to a recognised provident fund is deemed received to the extent it exceeds:', ['9.5% per annum', '8% per annum', '12% per annum', '10% per annum'], 0,
          'Annual accretion to a recognised PF by way of interest in excess of 9.5% p.a. is deemed to be received; also covered are transfers from unrecognised to recognised PF and employer contributions to the s. 124 pension scheme. In practice: employers credit within the limit.', 'c7', T7, 'moderate'),
        Q('m11', 'A non-resident transfers shares of an Indian company in Singapore and receives consideration in Dubai. The capital gain is:', ['Deemed to accrue in India and taxable', 'Not taxable since transfer took place abroad', 'Exempt because consideration was received abroad', 'Taxable only in Singapore'], 0,
          'Capital gains from transfer of a capital asset situated in India are deemed to accrue in India regardless of where the transfer is executed or consideration paid. Shares of an Indian company are situated in India. In practice: buyers must consider withholding.', 'c8', T8),
        Q('m12', 'A non-resident borrows from another non-resident and invests in shares of an Indian company. Interest paid is:', ['Not deemed to accrue in India', 'Deemed to accrue in India', 'Taxable as royalty', 'Taxable only if paid in India'], 0,
          'Interest payable by a non-resident is deemed to accrue in India only when the money is used for a business or profession carried on by him in India; investing in shares is not such a business. In practice: if used in Indian business, it would be taxable.', 'c8', T8, 'moderate'),
        Q('m13', 'Fees for technical services paid by a resident to a non-resident for services utilised in India but rendered abroad are:', ['Taxable in India under section 9(7) read with 9(11)', 'Not taxable as services were rendered outside India', 'Taxable only if the non-resident has an office in India', 'Exempt'], 0,
          'Section 9(11) taxes interest, royalty and fees for technical services deemed to accrue under 9(5)–(7) whether or not the non-resident has a residence, business connection or rendered services in India. In practice: usage in India is decisive.', 'c8', T8),
        Q('m14', 'Shooting of a film in India by a foreign citizen individual:', ['Is not treated as business carried out in India', 'Is business in India and taxable', 'Is taxable only if released in India', 'Is royalty'], 0,
          'Section 9(9)(c) excludes from business in India the shooting of films by non-citizen individuals, and by firms or companies with no Indian-citizen or resident partners or shareholders. Income from such shooting is not deemed to accrue in India. In practice: foreign film crews shooting in India rely on this.', 'c8', T8),
        Q('m15', 'Salary paid by the Government of India to an Indian citizen posted abroad is:', ['Deemed to accrue in India; but foreign allowances are exempt', 'Not taxable at all', 'Fully exempt including salary', 'Taxable only for ROR'], 0,
          'Section 9(3)(b) deems such salary to accrue in India, taxable even for a non-resident; allowances and perquisites paid abroad for service abroad are exempt under Schedule III (Table Sl. No. 9) in both regimes. In practice: diplomats pay tax on basic salary.', 'c8', T8, 'moderate'),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Kiran — non-resident', 1, 'application', 'non-resident|non resident', '182'),
           S('s2', 'Meera ₹18 lakh — RNOR via 120 days', 1, 'application', '120', 'not ordinarily|rnor'),
           S('s3', 'Meera ₹9 lakh — non-resident', 1, 'application', '15 lakh|9 lakh', 'non-resident|non resident'),
           S('s4', 'Leo — RNOR (700 days)', 1, 'application', '700|729', 'not ordinarily|rnor'),
           S('s5', 'Rohan — deemed resident, RNOR', 1, 'application', 'deemed')],
          ['State the test, then the status.'], ['Applying the 60-day rule to emigrants or low-income visitors.'], ['Table.'], pad='table'),
        W('q2', 8, i2['q'], i2['solution'],
          [S('s1', 'ROR global income', 3, 'computation', 'ror|ordinarily resident', nums=[ror]),
           S('s2', 'RNOR including India-controlled foreign business', 3, 'computation', 'rnor|not ordinarily', nums=[rnor]),
           S('s3', 'NR — Indian-sourced and received in India', 2, 'computation', 'non-resident|nr', nums=[nr])],
          ['Use three columns and justify doubtful items in notes.'], ['Treating later remittance as receipt in India.', 'Exempting foreign agricultural income.'], ['Columnar table.'], pad='table', checks=list(ck2)),
        W('q3', 4, 'Explain how the residential status of a HUF and of a company is determined.',
          [p('HUF: resident if control and management of its affairs is wholly or partly in India; otherwise non-resident. A resident HUF is ROR only if the Karta was resident in at least 2 of 10 preceding years and in India 730 days or more in 7 preceding years; else RNOR.'),
           p('Company: resident if it is Indian, or if in that year its place of effective management (where key management and commercial decisions are in substance made) is in India in that year; otherwise non-resident.')],
          [S('s1', 'HUF — control and management', 1.5, 'concept', 'control', 'management'),
           S('s2', 'HUF — Karta conditions for ROR', 1, 'concept', 'karta'),
           S('s3', 'Company — Indian company or POEM', 1.5, 'concept', 'indian', 'effective management|poem')],
          ['Two short paragraphs suffice.'], ['Using days of stay for a company.'], ['Paragraphs.']),
    ]

    viva = [
        V('v1', 'What are the two basic conditions for an individual to be resident?',
          'Stay in India for 182 days or more in the tax year, or 60 days or more in the tax year together with 365 days or more in the four preceding tax years.',
          [P('p1', '182 days', 5, '182'), P('p2', '60 days + 365 days in 4 years', 5, '60', '365')], 'c1'),
        V('v2', 'When does the 120-day rule apply?',
          'For an Indian citizen or person of Indian origin visiting India whose total income other than foreign source income exceeds fifteen lakh rupees; then 120 days in the year plus 365 days in four years makes him resident but not ordinarily resident.',
          [P('p1', 'Visiting citizen/PIO', 3, 'citizen|origin|visit'), P('p2', 'Indian income > ₹15 lakh', 4, '15 lakh|fifteen lakh'), P('p3', 'Becomes RNOR', 3, 'not ordinarily|rnor')], 'c2'),
        V('v3', 'Who is a deemed resident?',
          'An Indian citizen whose income other than foreign source income exceeds fifteen lakh rupees and who is not liable to tax in any other country because of domicile or residence. He is always not ordinarily resident.',
          [P('p1', 'Indian citizen', 3, 'citizen'), P('p2', '> ₹15 lakh Indian income', 3, '15 lakh|fifteen lakh'), P('p3', 'Not liable to tax elsewhere', 4, 'not liable|no tax|liable to tax in any other')], 'c3'),
        V('v4', 'What is the scope of total income of a non-resident?',
          'Just two kinds: money received in India, actually or by deeming, and income that accrues or arises in India, actually or by deeming.',
          [P('p1', 'Received/deemed received in India', 5, 'received'), P('p2', 'Accrues/deemed to accrue in India', 5, 'accru|arise')], 'c6'),
        V('v5', 'When is royalty payable by a resident not deemed to accrue in India?',
          'When it is for a right, property or information used for a business or profession carried on by the resident outside India, or for making or earning income from a source outside India.',
          [P('p1', 'Business carried on outside India', 5, 'outside india', 'business|profession'), P('p2', 'Earning income from a source outside India', 5, 'source outside|income from any source outside|foreign source')], 'c8'),
    ]

    cases = [{'id': 'k1', 'title': 'The Menon family across borders', 'difficulty': 'moderate',
              'case': 'Arun Menon, an Indian citizen, has lived in Oman (no income-tax) for years. In tax year 2026-27 he spent 40 days in India; his rent and interest from India total ₹22 lakh. His sister Lata, a British citizen whose father was born in Kerala, spent 140 days in India, has ₹16 lakh of Indian income and 500 days in India in the preceding four years. Their family HUF is managed by the Karta in Kochi. A Singapore firm paid Arun ₹5 lakh for advising a Chennai company on its Indian plant.',
              'mcqs': [
                  M('k1a', 'Arun\'s residential status is:', ['Deemed resident — RNOR', 'Non-resident', 'ROR', 'Resident under the 120-day rule'], 0,
                    'Arun is an Indian citizen, not liable to tax in Oman, with Indian income above ₹15 lakh, so section 6(7) makes him a deemed resident, always RNOR. His 40 days do not matter. In practice: zero-tax residence triggers this rule.', 'moderate', topic=T3),
                  M('k1b', 'Lata\'s residential status is:', ['RNOR — person of Indian origin meeting the 120-day rule', 'Non-resident — she is not a citizen', 'Deemed resident', 'ROR'], 0,
                    'Her father was born in undivided India, so she is a person of Indian origin; with Indian income above ₹15 lakh, 140 days and 500 days in four years satisfy the 120-day rule, making her RNOR. Deemed residence applies only to citizens. In practice: PIOs follow the same visitor rules.', 'moderate', topic=T2),
                  M('k1c', 'The Menon HUF managed from Kochi is:', ['Resident; ROR or RNOR depending on the Karta\'s history', 'Non-resident', 'Always RNOR', 'Deemed resident'], 0,
                    'Control and management in India makes the HUF resident; whether ROR or RNOR depends on whether the Karta meets both additional conditions. In practice: the Karta\'s own residential history over the past ten years decides the HUF\'s sub-status.', 'core', topic=T5),
                  M('k1d', 'The ₹5 lakh paid to Arun\'s Singapore firm for advice on the Indian plant is:', ['Fees for technical services deemed to accrue in India', 'Not taxable as rendered outside India', 'Exempt as consultancy', 'Taxable only if paid in India'], 0,
                    'Consultancy is technical service; payable by a resident for services used in India, it is deemed to accrue in India under section 9(7), and section 9(11) removes the need for services to be rendered here. In practice: the Chennai company should consider TDS.', 'moderate', topic=T8),
              ]}]

    return unit(UID, 'p3', 'int-p3-a-ch02', 1, 'Residential Status and Scope of Total Income',
                ['Determine the residential status of individuals, including exceptions and deemed residence.',
                 'Distinguish ROR and RNOR and determine status of HUFs, firms, AOPs and companies.',
                 'Apply section 5 to compute the scope of total income for each status.',
                 'Explain accrual, receipt, deemed receipt and income deemed to accrue or arise in India.'],
                {'difficulty': 'core', 'minutes': {'learn': 50, 'practice': 40}, 'prereq': ['int-p3-a-ch01-u01'],
                 'exam_tip': 'A three-column (ROR/RNOR/NR) computation is almost certain; also expect status puzzles involving 120 days, ₹15 lakh, deemed residence and section 9 cases.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Resident: 182 days, or 60 days + 365 days in 4 years.', 'Emigrating citizens/crew and low-income visitors: only 182 days.',
                             'Visitors with Indian income > ₹15 L: 120 days + 365 → RNOR.', 'Deemed resident: citizen, Indian income > ₹15 L, not taxed elsewhere → RNOR.',
                             'ROR: resident 2 of 10 years AND 730+ days in 7 years.', 'HUF/firm/AOP: control and management; company: Indian or POEM in India.',
                             'ROR — global; RNOR — India + India-controlled foreign business; NR — India only.', 's. 9 deems salary, dividend, interest, royalty, FTS and Indian-asset gains to accrue in India.'],
                 'remember': ['Arrival and departure days both count.', 'Remittance of foreign income is not receipt in India.'],
                 'traps': ['PIOs cannot be deemed residents.', 'Companies and firms are never RNOR.']},
                [('Main test', '182 days'), ('Alternative', '60 days + 365 in 4 yrs'), ('Visitor > ₹15 L', '120 days + 365'), ('ROR', '2 of 10 yrs + 730 days in 7'),
                 ('Deemed resident', 's. 6(7)'), ('Deemed accrual', 's. 9')],
                viva, cases,
                topics=['Structured Sectional Learning', 'Introduction', 'Residential Status', 'Scope of Total Income'])
