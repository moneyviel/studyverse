"""CA Final · Paper 4 · Chapter 21 Non-Resident Taxation.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch21-u01'
T1 = 'Residential status'
T2 = 'Scope of total income and deemed accrual'
T3 = 'Business connection and significant economic presence'
T4 = 'Presumptive regimes and head office expenditure'
T5 = 'Special rates for non-residents'


def build():
    ck = Checks()
    d1 = ck.add('130', 'Days in India in T.Y. 2026-27 (Rao and Lee)')
    d2 = ck.add('400', 'Days in India in preceding four years')
    i1 = {'id': 'i1', 'title': 'Visitors and residential status', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'For T.Y. 2026-27: (a) Rao, an Indian citizen working abroad who visits India, stays 130 days this year and 400 days in the preceding four years; his income other than from foreign sources is ₹18,00,000. (b) Lee, a foreign national with the same stay pattern, has Indian income of ₹5,00,000. Determine their residential status (basic conditions only).',
          'solution': [table(['Person', 'Test', 'Result'], [
              ['Rao', f'Visiting citizen: {inr(d1)} days ≥ 120 and {inr(d2)} days ≥ 365 with Indian income > ₹15 lakh', 'Resident — but not ordinarily resident'],
              ['Lee', f'Foreign national: {inr(d1)} days ≥ 60 and {inr(d2)} days ≥ 365', 'Resident (ROR/RNOR by further tests)']], title='Section 6')],
          'checks': list(ck)}

    c2 = Checks()
    sh = c2.add('(400000000+100000000)*0.075', 'Presumptive income of shipping company at 7.5% (₹)')
    ho = c2.add('min(4000000,80000000*0.05)', 'Head office expenditure allowed (₹)')
    i2 = {'id': 'i2', 'title': 'Presumptive shipping income and head office costs', 'difficulty': 'core', 'minutes': 6,
          'q': '(a) A non-resident shipping company receives ₹40 crore for carriage from Indian ports and ₹10 crore for carriage to Indian ports in T.Y. 2026-27. Compute presumptive income. (b) A non-resident bank\'s Indian branch has adjusted total income of ₹8 crore and claims head office expenditure of ₹40 lakh. How much is allowed?',
          'solution': [table(['Item', 'Working', '₹'], [
              ['(a) Shipping', '7.5% × (40 crore + 10 crore)', inr(sh)],
              ['(b) Head office expenditure', 'Lower of claim and 5% of adjusted total income', inr(ho)]], title='Sections 61 and 60')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 6: an individual is resident if in India for 182 days or more in the tax year, or for 60 days or more in the year and 365 days or more in the four preceding years. For Indian citizens leaving for employment abroad or as crew, and for Indian citizens or persons of Indian origin visiting India, the 60 days becomes 182 days — except that visitors with Indian-source income above ₹15 lakh are resident if in India for 120 days and 365 days in the preceding four years.',
            'An Indian citizen with income other than from foreign sources above ₹15 lakh who is not liable to tax in any other country is deemed resident (section 6(7)); deemed residents and the 120-day visitors are always resident but not ordinarily resident.',
            'A resident individual is "not ordinarily resident" if non-resident in 9 of the 10 preceding years, or in India for 729 days or less in the 7 preceding years. A HUF follows its manager\'s status for NOR. A company is resident if it is Indian or its place of effective management is in India.'],
          'Days in India decide status, with special rules for citizens and visitors.',
          'A visiting citizen earning ₹18 lakh in India becomes resident at 120 days.'),
        C('c2', T2, [
            'Section 5: a resident and ordinarily resident is taxed on worldwide income; a not ordinarily resident on Indian income and on foreign income from a business controlled or profession set up in India; a non-resident only on income received or deemed received in India or accruing or deemed to accrue in India.',
            'Section 9 deems income to accrue in India through a business connection, property or asset or source in India, transfer of a capital asset in India (including shares of foreign companies deriving substantial value — over ₹10 crore and at least 50% of total assets — from Indian assets), salaries for services in India, dividends by Indian companies, interest, royalty and fees for technical services payable by residents (with exceptions) or for Indian businesses, and monetary gifts by residents to non-residents.',
            'Royalties and FTS are taxable in India regardless of whether the non-resident has a residence, business connection or rendered services in India (section 9(11)).'],
          'Non-residents pay on Indian-source income; deeming rules widen the source.',
          'Royalty paid by an Indian company to a US firm for software used in India is deemed to accrue in India.'),
        C('c3', T3, [
            'Business connection includes any business activity carried out through a dependent agent who habitually concludes or plays the principal role in concluding contracts for the non-resident, maintains stock for delivery, or secures orders. Independent agents acting in the ordinary course of business are excluded, as are purchase operations for export and certain news collection or film shooting activities.',
            'Significant economic presence (SEP) also creates a business connection: transactions with persons in India exceeding ₹2 crore in a year (including downloads of data or software), or systematic and continuous soliciting of business or interaction with at least 3 lakh users in India — whether or not the non-resident has a place of business here.',
            'Only income attributable to the operations or SEP in India is taxable; treaty provisions (PE) may still give relief where more beneficial.'],
          'Agents and digital footprints both create taxable presence.',
          'An overseas app with 5 lakh Indian users has SEP even without an office.'),
        C('c4', T4, [
            'Section 61 presumptive income for non-residents: shipping 7.5% of amounts for carriage from Indian ports (and received in India for carriage from other ports); cruise ships 20%; aircraft operations 5%; services for mineral oil exploration 10%; civil construction for turnkey power projects 10%. Lower profits may be claimed only with books and audit.',
            'Section 60 limits head office expenditure of a non-resident to the lower of actual attributable expenditure and 5% of adjusted total income (or 5% of average adjusted total income where the current figure is a loss).',
            'Sections 316 and 59 deal with shipping companies\' summary assessment before port clearance and special computation for non-residents.'],
          'Turnover-based deemed profits keep non-resident compliance simple.',
          'Shipping receipts of ₹50 crore imply presumptive income of ₹3.75 crore.'),
        C('c5', T5, [
            'Section 207: non-residents and foreign companies pay 20% on dividends (10% from IFSC units), interest from Indian concerns, and royalty or FTS from Indian residents or concerns; lower rates apply to specified infrastructure and bond interest (often 5% or 9%). No deductions are allowed and no return is required if TDS has been deducted at full rates.',
            'Sections 208 to 211 give special rates for income from bonds and GDRs, units purchased in foreign currency by offshore funds and investment by NRIs in foreign exchange assets, with no deductions and no indexation.',
            'Treaty rates apply where more beneficial, subject to a tax residency certificate and other conditions.'],
          'Passive income of non-residents is taxed gross at flat rates.',
          'Royalty of ₹50 lakh to a non-resident without a treaty benefit attracts tax of ₹10 lakh.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Inbound tax health-check', 'role': 'International tax analyst',
             'situation': 'A foreign SaaS company sells to Indian customers through a local reseller.',
             'steps': ['Check agent dependence and contract conclusion.', 'Test SEP thresholds.', 'Characterise payments as business income or royalty.', 'Compare Act and treaty rates.'],
             'takeaway': 'Nexus first, characterisation second, rate last.'}]

    mcqs = [
        Q('m1', 'A foreign national in India for 70 days this year and 400 days in the preceding four years is:', ['Resident', 'Non-resident', 'Deemed resident', 'Not taxable'], 0,
          'Sixty-day rule. In practice: check NOR.', 'c1', T1),
        Q('m2', 'A visiting Indian citizen with Indian income above ₹15 lakh is resident if in India for at least:', ['One hundred twenty days with three hundred sixty-five in prior four years', 'One hundred eighty-two days only', 'Sixty days', 'Ninety days'], 0,
          'Section 6(5). In practice: RNOR.', 'c1', T1),
        Q('m3', 'A company incorporated abroad is resident in India if:', ['Its place of effective management is in India', 'It has an Indian customer', 'It has an Indian director', 'It files a return in India'], 0,
          'Section 6. In practice: POEM guidelines.', 'c1', T1),
        Q('m4', 'A not ordinarily resident is taxed on foreign income only if it is:', ['From a business controlled in India', 'From a foreign job', 'Received abroad', 'Interest abroad'], 0,
          'Section 5. In practice: plus Indian income.', 'c2', T2),
        Q('m5', 'SEP arises where transactions with persons in India exceed:', ['Two crore rupees', 'Fifty lakh rupees', 'Ten crore rupees', 'One crore rupees'], 0,
          'Rule 13. In practice: or 3 lakh users.', 'c3', T3),
        Q('m6', 'Presumptive rate for non-resident aircraft operations is:', ['Five percent', 'Seven and a half percent', 'Ten percent', 'Twenty percent'], 0,
          'Section 61. In practice: of specified receipts.', 'c4', T4),
        Q('m7', 'Head office expenditure is capped at:', ['Five percent of adjusted total income', 'Ten percent', 'Two percent', 'No cap'], 0,
          'Section 60. In practice: average if loss.', 'c4', T4),
        Q('m8', 'Royalty received by a non-resident from an Indian concern is taxed under section 207 at:', ['Twenty percent', 'Ten percent', 'Thirty percent', 'Forty percent'], 0,
          'Gross basis. In practice: treaty may lower.', 'c5', T5),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Rao', 3, 'analysis', '120', nums=[d1, d2]), S('s2', 'Lee', 3, 'analysis', '60')],
          ['State the rule used.'], ['Applying 60-day rule to visiting citizens.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Shipping', 3, 'computation', '7.5', nums=[sh]), S('s2', 'Head office', 2, 'computation', '5%', nums=[ho])],
          ['Cite sections.'], ['Allowing full head office claim.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Who is a deemed resident?', 'An Indian citizen with income other than from foreign sources above ₹15 lakh who is liable to tax in no other country by residence or similar criteria.',
          [P('p1', 'Indian citizen', 5, 'citizen'), P('p2', 'Fifteen lakh', 5, '15 lakh')], 'c1'),
        V('v2', 'When is a resident individual not ordinarily resident?', 'If non-resident in nine of the ten preceding years, or in India for 729 days or less in the seven preceding years.',
          [P('p1', 'Nine of ten', 5, 'nine of the ten'), P('p2', '729 days', 5, '729')], 'c1'),
        V('v3', 'What is significant economic presence?', 'Transactions with persons in India above ₹2 crore or systematic interaction with at least 3 lakh Indian users.',
          [P('p1', 'Two crore', 5, '2 crore'), P('p2', 'Users', 5, 'users')], 'c3'),
        V('v4', 'Is an independent agent a business connection?', 'An independent agent acting in its ordinary course of business is excluded from business connection.',
          [P('p1', 'Excluded', 5, 'excluded'), P('p2', 'Ordinary course', 5, 'ordinary course')], 'c3'),
        V('v5', 'When are foreign company shares deemed situated in India?', 'When they derive substantial value from Indian assets — over ₹10 crore and at least 50% of total assets.',
          [P('p1', 'Substantial value', 5, 'substantial'), P('p2', 'Fifty percent', 5, '50%')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Nordic Design AB', 'difficulty': 'moderate',
              'case': 'Nordic Design AB, a Swedish company with no office in India, earns ₹3 crore from Indian clients for software licences and ₹50 lakh as fees for technical services from an Indian company in T.Y. 2026-27. Assume no treaty benefit is claimed.',
              'mcqs': [
                  M('k1a', 'Does Nordic have SEP based on transactions?', ['Yes, payments exceed ₹2 crore', 'No, it has no office', 'Only if users exceed 3 lakh', 'No, licences are excluded'], 0,
                    'Rule 13(1). In practice: attribution needed.', 'core', topic=T3),
                  M('k1b', 'Tax on FTS under section 207 (₹):', ['10,00,000', '5,00,000', '15,00,000', '20,00,000'], 0,
                    '20% × 50,00,000. In practice: plus surcharge and cess.', 'core', check=1000000, topic=T5),
                  M('k1c', 'If the licence fees are royalty, tax at 20% (₹):', ['60,00,000', '30,00,000', '90,00,000', '6,00,000'], 0,
                    '20% × 3 crore. In practice: treaty may reduce.', 'core', check=6000000, topic=T5),
                  M('k1d', 'Are any expenses deductible against such royalty and FTS?', ['No, they are taxed on gross basis', 'Yes, all expenses', 'Only salaries', 'Only depreciation'], 0,
                    'Section 207. In practice: unless PE-connected.', 'core', topic=T5),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch21', 1, 'Non Resident Taxation',
                ['Determine residential status of individuals, HUFs and companies.',
                 'Apply scope of total income and deemed accrual rules.',
                 'Apply business connection and SEP.',
                 'Compute presumptive income and head office expenditure.',
                 'Apply special rates for non-residents.'],
                {'difficulty': 'hard', 'minutes': {'learn': 55, 'practice': 35}, 'prereq': ['fin-p4-ch20-u01'],
                 'exam_tip': 'Status first, then scope, then deeming provision, then rate (Act vs treaty).'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 6: 182/60+365; 120 days and ₹15 lakh rule; deemed resident.', 'NOR tests 9/10 and 729 days; POEM for companies.', 'Section 9 deemed accrual; indirect transfer.',
                             'SEP: ₹2 crore or 3 lakh users.', 'Section 61 presumptive; section 60 HO cap 5%; section 207 rates.'],
                 'remember': ['Royalty/FTS taxable regardless of presence.'],
                 'traps': ['Ignoring the ₹15 lakh test for visiting citizens.']},
                [('Residence', 'Section 6'), ('Scope', 'Section 5'), ('Deemed accrual', 'Section 9'), ('Presumptive', 'Section 61'), ('Special rates', 'Section 207')],
                viva, cases)
