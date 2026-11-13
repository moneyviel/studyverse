"""CA Final · Paper 4 · Chapter 8 Deductions from Gross Total Income.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch08-u01'
T1 = 'General principles of Chapter VIII deductions'
T2 = 'Deductions for payments and investments'
T3 = 'Health, disability and other personal deductions'
T4 = 'Donations and rent'
T5 = 'Deductions in respect of certain incomes'


def build():
    ck = Checks()
    d123 = ck.add('min(100000+80000,150000)', 'Section 123 deduction (₹)')
    d124 = ck.add('min(50000,50000)', 'Section 124(3) own NPS (₹)')
    d126a = ck.add('min(30000,25000)', 'Section 126 self and family (₹)')
    d126b = ck.add('min(55000,50000)', 'Section 126 senior-citizen parents (₹)')
    d153 = ck.add('min(14000,10000)', 'Section 153 savings interest (₹)')
    tot = ck.add('min(100000+80000,150000)+50000+min(30000,25000)+min(55000,50000)+min(14000,10000)', 'Total deductions (₹)')
    i1 = {'id': 'i1', 'title': 'Personal deductions under the optional regime', 'difficulty': 'core', 'minutes': 8,
          'q': 'Harish, 45, has opted out of the default regime for T.Y. 2026-27. He pays: PPF ₹1,00,000; life insurance premium ₹80,000 (within the premium limits); own NPS ₹50,000 (not claimed elsewhere); health insurance for self and family ₹30,000; health insurance for his parents (both above 60) ₹55,000; and has savings bank interest of ₹14,000. Compute total Chapter VIII deductions.',
          'solution': [table(['Section', 'Working', '₹'], [
              ['123', 'Lower of ₹1,80,000 and ₹1,50,000', inr(d123)],
              ['124(3)', 'Own NPS up to ₹50,000', inr(d124)],
              ['126 — self/family', 'Limit ₹25,000', inr(d126a)],
              ['126 — parents', 'Senior citizens: limit ₹50,000', inr(d126b)],
              ['153', 'Savings interest up to ₹10,000', inr(d153)],
              ['Total', '', inr(tot)]], title='Chapter VIII (optional regime)')],
          'checks': list(ck)}

    c2 = Checks()
    a = c2.add('180000-600000*0.10', '(a) Rent minus 10% of total income (₹)')
    b = c2.add('600000*0.25', '(b) 25% of total income (₹)')
    c = c2.add('5000*12', '(c) ₹5,000 per month (₹)')
    d = c2.add('min(180000-600000*0.10,600000*0.25,5000*12)', 'Deduction under section 134 (₹)')
    i2 = {'id': 'i2', 'title': 'Rent paid without HRA', 'difficulty': 'core', 'minutes': 5,
          'q': 'Ishita, a self-employed designer under the optional regime, pays rent of ₹15,000 a month. She owns no house anywhere and receives no HRA. Her total income before section 134 is ₹6,00,000. Compute the deduction.',
          'solution': [table(['Limit', 'Working', '₹'], [
              ['(a)', '1,80,000 − 10% × 6,00,000', inr(a)],
              ['(b)', '25% × 6,00,000', inr(b)],
              ['(c)', '₹5,000 × 12', inr(c)],
              ['Deduction', 'Least of the three', inr(d)]], title='Section 134')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Chapter VIII deductions are made from gross total income; their total cannot exceed GTI, and they are not allowed against special-rate incomes such as STCG under section 196, LTCG under sections 197 and 198, or casual winnings.',
            'Most deductions (sections 123, 124(3), 126–135, 153, 154) are unavailable under the default regime of section 202(1). Employer NPS contribution under section 124(1) and additional employee cost under section 146 remain available under it.',
            'For profit-linked deductions in Part C, the return must be filed by the due date under section 263(1), the same profits cannot be claimed twice, and audit reports must be furnished where required (section 122).'],
          'Deductions come off GTI, never off special-rate income.',
          'A salaried person in the default regime can still claim the employer\'s NPS contribution.'),
        C('c2', T2, [
            'Section 123: payments such as life insurance premiums (within premium-to-sum assured limits), PPF, EPF, ELSS, NSC, tuition fees, housing loan principal and Sukanya Samriddhi deposits qualify, up to ₹1,50,000 for individuals and HUFs.',
            'Section 124: employer contribution to NPS up to 14% of salary for government employers and 10% for others (14% for employees under the default regime); the employee\'s own contribution qualifies within ₹1,50,000 and an extra ₹50,000 under section 124(3).',
            'Section 129 allows interest on education loans for higher studies for up to 8 years; sections 130 to 132 deal with specified housing loans and electric vehicle loan interest as provided.'],
          'Saving-linked deductions mainly sit in sections 123 and 124.',
          'PPF of ₹1 lakh plus LIC premium of ₹80,000 yields a deduction of ₹1.5 lakh.'),
        C('c3', T3, [
            'Section 126 (health insurance): up to ₹25,000 for self, spouse and dependent children (₹50,000 if any is a senior citizen), and another ₹25,000/₹50,000 for parents; preventive health check-up within these limits; payment other than in cash, except for check-ups.',
            'Section 127 (maintenance or medical treatment of a dependant with disability): flat ₹75,000, or ₹1,25,000 for severe disability. Section 154 (assessee himself with disability): the same amounts. Section 128 (specified diseases): actual expenditure up to ₹40,000, or ₹1,00,000 for senior citizens, net of insurance reimbursements.',
            'Section 153: interest on savings accounts up to ₹10,000 for individuals (non-senior) and HUFs; up to ₹50,000 on all deposits for resident senior citizens.'],
          'Health and disability deductions have fixed caps.',
          'Parents\' policy of ₹55,000 for seniors gives ₹50,000.'),
        C('c4', T4, [
            'Section 133 (donations): donations to specified funds and institutions qualify at 100% or 50%, with or without a ceiling of 10% of adjusted gross total income depending on the category; cash donations above ₹2,000 are not allowed; unavailable to individuals, HUFs and similar persons in the default regime and to companies on concessional regimes.',
            'Section 134 (rent paid): for those not receiving HRA and not owning a residence at the place of work, the deduction is the least of rent minus 10% of total income, 25% of total income and ₹5,000 a month, with a declaration in the prescribed form.',
            'Sections 135 to 137: donations for scientific research or rural development (for those without business income) and contributions to political parties or electoral trusts (other than in cash) are deductible.'],
          'Donations by banking modes; rent relief has a three-way cap.',
          'Rent of ₹15,000 a month with total income of ₹6 lakh gives a deduction of ₹60,000.'),
        C('c5', T5, [
            'Section 140: an eligible start-up (company or LLP incorporated between 1 April 2016 and 31 March 2030, turnover up to ₹300 crore, with a certificate from the Inter-Ministerial Board) can deduct 100% of profits for any 3 consecutive years out of the first 10.',
            'Section 146: assessees subject to tax audit can deduct 30% of additional employee cost for 3 years from the year of employment, if the business is not formed by splitting or reconstruction and a CA report is furnished. Section 148 deducts inter-corporate dividends redistributed within the specified time.',
            'Other income-based deductions include co-operative society income (section 149), royalty on books and patents (sections 151 and 152), and specified IFSC units, SEZ and infrastructure undertakings (sections 138, 139, 144, 147) as provided.'],
          'Profit-linked deductions reward start-ups, jobs and specific sectors.',
          'Additional employee cost of ₹40 lakh gives ₹12 lakh a year for three years.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Regime comparison for an employee', 'role': 'Payroll tax advisor',
             'situation': 'An employee asks whether deductions justify leaving the default regime.',
             'steps': ['List eligible deductions under the optional regime.', 'Compute tax under both regimes.', 'Note deductions available in both.', 'Recommend and document the choice.'],
             'takeaway': 'Only large deductions beat the default regime slabs.'}]

    mcqs = [
        Q('m1', 'Maximum deduction under section 123 is:', ['One lakh fifty thousand rupees', 'One lakh rupees', 'Two lakh rupees', 'Fifty thousand rupees'], 0,
          'Individuals and HUFs. In practice: not in default regime.', 'c2', T2),
        Q('m2', 'Under the default regime, an employee may still claim:', ['Employer contribution to NPS', 'Health insurance premium', 'PPF contribution', 'Donations'], 0,
          'Section 124(1). In practice: 14% of salary.', 'c1', T1),
        Q('m3', 'Health insurance for senior-citizen parents is deductible up to:', ['Fifty thousand rupees', 'Twenty-five thousand rupees', 'One lakh rupees', 'Seventy-five thousand rupees'], 0,
          'Section 126. In practice: non-cash payment.', 'c3', T3),
        Q('m4', 'Deduction for an assessee with severe disability is:', ['One lakh twenty-five thousand rupees', 'Seventy-five thousand rupees', 'Fifty thousand rupees', 'Actual expenditure'], 0,
          'Section 154. In practice: flat amount.', 'c3', T3),
        Q('m5', 'Interest deduction for a resident senior citizen on deposits is up to:', ['Fifty thousand rupees', 'Ten thousand rupees', 'Forty thousand rupees', 'Unlimited'], 0,
          'Section 153. In practice: covers FDs too.', 'c3', T3),
        Q('m6', 'Cash donations are not deductible if they exceed:', ['Two thousand rupees', 'Ten thousand rupees', 'Five hundred rupees', 'Twenty thousand rupees'], 0,
          'Section 133. In practice: use banking modes.', 'c4', T4),
        Q('m7', 'A start-up may claim the section 140 deduction for:', ['Three consecutive years out of ten', 'Five years out of ten', 'Ten years', 'Seven consecutive years'], 0,
          'Profit-linked. In practice: needs IMB certificate.', 'c5', T5),
        Q('m8', 'Deduction for additional employee cost is:', ['Thirty percent for three years', 'Twenty percent for five years', 'One hundred percent once', 'Fifty percent for two years'], 0,
          'Section 146. In practice: CA report needed.', 'c5', T5),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Sections 123 and 124', 2, 'computation', 'NPS', nums=[d123, d124]), S('s2', 'Health insurance', 2, 'computation', 'parents', nums=[d126a, d126b]), S('s3', 'Savings interest and total', 2, 'computation', 'total', nums=[d153, tot])],
          ['Cite sections.'], ['Exceeding ₹1.5 lakh in section 123.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Three limits', 3, 'computation', 'least', nums=[a, b, c]), S('s2', 'Deduction', 1, 'computation', 'deduction', nums=[d])],
          ['State conditions.'], ['Using total income after section 134.'], ['Least of three.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Can Chapter VIII deductions reduce LTCG on listed shares?', 'They are barred against such special-rate gains; they come off the rest of gross total income only.',
          [P('p1', 'Barred', 5, 'barred'), P('p2', 'Special-rate', 5, 'special')], 'c1'),
        V('v2', 'What is the employer NPS limit for a private employee under the default regime?', 'Fourteen percent of salary.',
          [P('p1', 'Fourteen percent', 5, '14|fourteen'), P('p2', 'Salary', 5, 'salary')], 'c2'),
        V('v3', 'How is the section 128 deduction computed?', 'Actual expenditure on specified diseases up to ₹40,000, or ₹1,00,000 for senior citizens, reduced by insurance reimbursement.',
          [P('p1', 'Forty thousand', 5, '40,000'), P('p2', 'Reimbursement', 5, 'reimburse')], 'c3'),
        V('v4', 'Who can claim rent deduction under section 134?', 'Individuals with rent paid for their home who get no house rent allowance and own no residence at the place of work, filing the prescribed declaration.',
          [P('p1', 'Rent paid', 5, 'rent paid'), P('p2', 'Declaration', 5, 'declaration')], 'c4'),
        V('v5', 'What turnover limit applies to an eligible start-up?', 'Turnover up to ₹300 crore in the year of claim.',
          [P('p1', 'Three hundred crore', 5, '300 crore'), P('p2', 'Year of claim', 5, 'year')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Nimbus Robotics', 'difficulty': 'moderate',
              'case': 'Nimbus Robotics Pvt Ltd, incorporated in 2022 with an IMB certificate and turnover of ₹40 crore, earns business profits of ₹6 crore in T.Y. 2026-27 from its eligible business. Its accounts are audited. During the year it hired new eligible employees with additional employee cost of ₹40,00,000.',
              'mcqs': [
                  M('k1a', 'Maximum section 140 deduction if this is one of its chosen years (₹):', ['6,00,00,000', '3,00,00,000', '1,20,00,000', 'Nil'], 0,
                    '100% of eligible profits. In practice: GTI cap.', 'core', check=60000000, topic=T5),
                  M('k1b', 'Section 146 deduction for this year (₹):', ['12,00,000', '40,00,000', '8,00,000', '4,00,000'], 0,
                    '30% × 40,00,000. In practice: repeat for two more years.', 'core', check=1200000, topic=T5),
                  M('k1c', 'Total section 146 deduction over three years for this batch (₹):', ['36,00,000', '12,00,000', '40,00,000', '24,00,000'], 0,
                    '12,00,000 × 3. In practice: if conditions continue.', 'core', check=3600000, topic=T5),
                  M('k1d', 'To keep these deductions, Nimbus must file its return:', ['By the due date under section 263(1)', 'Any time before assessment', 'Within two years', 'Only if asked'], 0,
                    'Section 122. In practice: late return loses Part C deductions.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch08', 1, 'Deductions from Gross Total Income',
                ['Apply the general principles of Chapter VIII.',
                 'Compute deductions for payments and investments.',
                 'Apply health, disability and interest deductions.',
                 'Compute donation and rent deductions.',
                 'Apply deductions for start-ups, employment and other incomes.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 45, 'practice': 30}, 'prereq': ['fin-p4-ch07-u01'],
                 'exam_tip': 'Confirm the regime first; most personal deductions vanish under section 202(1).'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Deductions capped at GTI; not against special-rate income.', 'Section 123 ₹1.5 lakh; 124 NPS.', 'Sections 126–128, 153, 154 personal.',
                             'Section 133 donations; 134 rent.', 'Section 140 start-ups; 146 employment.'],
                 'remember': ['Default regime keeps employer NPS and section 146.'],
                 'traps': ['Allowing section 123 under the default regime.']},
                [('Investments', 'Section 123'), ('NPS', 'Section 124'), ('Health insurance', 'Section 126'), ('Donations', 'Section 133'), ('Start-ups', 'Section 140')],
                viva, cases)
