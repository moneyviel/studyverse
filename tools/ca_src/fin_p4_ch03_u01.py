"""CA Final · Paper 4 · Chapter 3 Profits and Gains of Business or Profession.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch03-u01'
T1 = 'Scope of the head and method of accounting'
T2 = 'Depreciation and additional depreciation'
T3 = 'Deductions and disallowances'
T4 = 'Deduction on actual payment basis'
T5 = 'Presumptive taxation, partners and compliance'


def build():
    ck = Checks()
    n1 = ck.add('(5000000+2000000)*0.15', 'Normal depreciation at 15% on ₹70 lakh (₹)')
    n2 = ck.add('800000*0.075', 'Normal depreciation at 7.5% on ₹8 lakh (₹)')
    a1 = ck.add('2000000*0.20', 'Additional depreciation 20% on ₹20 lakh (₹)')
    a2 = ck.add('800000*0.10', 'Additional depreciation 10% on ₹8 lakh this year (₹)')
    tot = ck.add('(5000000+2000000)*0.15+800000*0.075+2000000*0.20+800000*0.10', 'Total depreciation (₹)')
    i1 = {'id': 'i1', 'title': 'Depreciation for a manufacturer', 'difficulty': 'core', 'minutes': 8,
          'q': 'Ruchika Castings Ltd., a manufacturer, has a plant-and-machinery block (15%) with opening WDV ₹50,00,000 for T.Y. 2026-27. It buys new machinery for ₹20,00,000 put to use on 10 June 2026 and new machinery for ₹8,00,000 put to use on 15 December 2026. No asset was sold. Compute depreciation including additional depreciation.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Normal — full rate', '15% × (50,00,000 + 20,00,000)', inr(n1)],
              ['Normal — half rate', '7.5% × 8,00,000 (used < 180 days)', inr(n2)],
              ['Additional — full', '20% × 20,00,000', inr(a1)],
              ['Additional — half', '10% × 8,00,000 (balance 10% next year)', inr(a2)],
              ['Total', '', inr(tot)]], title='Section 33')],
          'checks': list(ck)}

    c2 = Checks()
    f6 = c2.add('max(300000,600000*0.90)', 'Limit on first ₹6 lakh of book profit (₹)')
    bal = c2.add('400000*0.60', 'Limit on balance ₹4 lakh (₹)')
    lim = c2.add('max(300000,600000*0.90)+400000*0.60', 'Maximum allowable remuneration (₹)')
    dis = c2.add('900000-(max(300000,600000*0.90)+400000*0.60)', 'Disallowed remuneration (₹)')
    i2 = {'id': 'i2', 'title': 'Remuneration to working partners', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Sahni & Batra, a firm, has book profit of ₹10,00,000 for T.Y. 2026-27. Its deed authorises remuneration to two working partners totalling ₹9,00,000, which was paid. Compute the allowable remuneration under section 35(e).',
          'solution': [table(['Slab', 'Working', '₹'], [
              ['First ₹6 lakh', 'Higher of ₹3,00,000 and 90% × 6,00,000', inr(f6)],
              ['Balance ₹4 lakh', '60% × 4,00,000', inr(bal)],
              ['Allowable', '', inr(lim)],
              ['Disallowed', '9,00,000 − allowable', inr(dis)]], title='Section 35(e)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 26 lists income chargeable under this head — profits of any business or profession, specified compensation, perquisites, export incentives, and others. "Business" includes trade, commerce, manufacture or an adventure in the nature of trade; "profession" includes vocation.',
            'Section 27 states that income is computed under the specific deduction provisions (sections 28 to 52 and related), subject to disallowances (sections 35 and 36) and deemed incomes (section 38). Income is computed under the cash or mercantile system regularly employed, read with ICDS notified under section 276(2).',
            'Speculation business is kept separate: its losses can be set off only against speculation profits. Specific provisions apply to banks and NBFCs on interest on bad or doubtful debts (section 277).'],
          'Start from accounting profit, then apply the Act.',
          'An adventure in the nature of trade, such as a single bulk purchase for resale, is business.'),
        C('c2', T2, [
            'Section 33 allows depreciation on tangible assets (buildings, machinery, plant, furniture) and intangibles (know-how, patents, copyrights, trademarks, licences, franchises) owned wholly or partly and used for business. Goodwill is not depreciable. Most assessees use the block-of-assets WDV method; power undertakings may use straight line on actual cost.',
            'Where an asset bought during the year is used for under 180 days in that year, the rate is halved for that first year only.',
            'Additional depreciation of 20% of actual cost is available to manufacturers and power businesses for new plant or machinery (not ships, aircraft, office appliances, road vehicles, used assets, or assets in office or residential premises). If used for less than 180 days, 10% is allowed that year and the balance 10% next year. It is available only with block-based depreciation and is restricted for those opting for certain concessional regimes.'],
          'Half-year rule and a 20% kicker for new factory machinery.',
          'Machinery put to use in December gets half normal and half additional depreciation that year.'),
        C('c3', T3, [
            'Specific deductions include rent, repairs and insurance (section 28), employer contributions to approved funds (section 29), insurance premiums (section 30), bad debts actually written off (section 31(2)), bonus, interest on borrowed capital and other items (section 32), and scientific research and specified business incentives (sections 45 and 46, with section 46 allowing 100% of capital expenditure for specified businesses, excluding land, goodwill and financial instruments).',
            'Section 34 is the residual rule: expenditure not of a capital or personal nature, laid out wholly and exclusively for business, is deductible. Expenditure on offences or to settle infringements is not.',
            'Disallowances: income-tax paid (section 35(a)); 30% of sums payable to residents where tax deductible at source is not deducted or paid by the due date of return (section 35(b)(i)), allowed in the year tax is paid; partner remuneration and interest beyond limits (section 35(e)); payments exceeding ₹10,000 per person per day otherwise than by account payee cheque/draft, ECS or prescribed electronic modes (section 36(4)), with ₹35,000 for goods transporters.'],
          'Allowed if wholly and exclusively for business, unless specifically barred.',
          'Four cash payments of ₹9,000 each on one day to one supplier are all disallowed.'),
        C('c4', T4, [
            'Section 37 allows certain sums only when actually paid, regardless of the accounting method: taxes and duties, employer contributions to PF and welfare funds, leave encashment, bonus or commission to employees, interest to specified financial entities, Indian Railways charges, and dues to micro or small enterprises paid late.',
            'For items other than MSE dues, payment after year-end but by the due date of the return under section 263(1) secures deduction in the year of liability (section 37(3)).',
            'Dues to a micro or small enterprise must be paid within the agreed time (maximum 45 days) or within 15 days if there is no written agreement; otherwise deduction moves to the year of payment. Medium enterprises are outside this rule.'],
          'Paid by the return date — deductible; MSE dues follow the MSMED clock.',
          'Bonus for March 2027 paid in July 2027 before filing is allowed for T.Y. 2026-27.'),
        C('c5', T5, [
            'Section 58 presumptive taxation: eligible assessees (resident individual, HUF or firm other than LLP not in a specified profession or commission/agency business) with turnover up to ₹2 crore — ₹3 crore if cash receipts do not exceed 5% — declare 6% of digital receipts (received by specified modes before the return due date) and 8% of the rest, or higher actual profit. Goods-carriage owners with up to 10 vehicles declare ₹1,000 per ton per month for heavy vehicles and ₹7,500 per vehicle per month for others. Resident individuals and firms in specified professions with receipts up to ₹50 lakh (₹75 lakh if cash ≤ 5%) declare 50%.',
            'Firms under presumption may still deduct partner salary and interest within section 35(e) limits: remuneration up to the higher of ₹3 lakh or 90% of the first ₹6 lakh of book profit plus 60% of the balance; interest up to 12% p.a., only if authorised by the deed.',
            'Books must be kept under section 62. Tax audit under section 63 applies where business turnover exceeds ₹1 crore (₹10 crore if cash receipts and payments are each within 5%), with separate rules for professionals and presumptive cases.'],
          'Small taxpayers may declare a deemed profit; others keep books and may need audit.',
          'A trader with ₹2.8 crore turnover and 3.6% cash receipts can use section 58.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Tax-audit year-end review', 'role': 'Audit senior',
             'situation': 'A manufacturing client closes its books for T.Y. 2026-27.',
             'steps': ['Recompute depreciation and additional depreciation.', 'Check TDS defaults for 30% disallowance.', 'Scan cash payments above ₹10,000.', 'Confirm section 37 payments and MSE dues.'],
             'takeaway': 'Disallowances drive most tax-audit adjustments.'}]

    mcqs = [
        Q('m1', 'Depreciation for an asset acquired and used for less than 180 days in the year is restricted to:', ['Half of the normal rate', 'Nil', 'The full rate', 'Twenty percent'], 0,
          'Section 33(4). In practice: year of acquisition only.', 'c2', T2),
        Q('m2', 'Additional depreciation is NOT available on:', ['A new truck used to deliver goods', 'New factory machinery', 'New power transmission equipment', 'New plant for production'], 0,
          'Road transport vehicles are excluded. In practice: check the asset type.', 'c2', T2),
        Q('m3', 'The residual deduction section under the 2025 Act is:', ['Section 34', 'Section 26', 'Section 58', 'Section 63'], 0,
          'Wholly and exclusively for business. In practice: no capital or personal outlay.', 'c3', T3),
        Q('m4', 'Where TDS on a sum paid to a resident is not deducted, the disallowance is:', ['Thirty percent of the sum', 'The whole sum', 'Ten percent of the sum', 'Nil'], 0,
          'Section 35(b)(i). In practice: allowed when tax is paid.', 'c3', T3),
        Q('m5', 'Cash payment limit per person per day for goods transport operators is:', ['Thirty-five thousand rupees', 'Ten thousand rupees', 'Twenty thousand rupees', 'Fifty thousand rupees'], 0,
          'Section 36(6). In practice: others ₹10,000.', 'c3', T3),
        Q('m6', 'Employer PF contribution for March paid before the return due date is:', ['Allowed in the year of liability', 'Disallowed permanently', 'Allowed only next year', 'Capitalised'], 0,
          'Section 37(3). In practice: keep challans.', 'c4', T4),
        Q('m7', 'Without a written agreement, a buyer must pay a micro enterprise within:', ['Fifteen days', 'Forty-five days', 'Thirty days', 'Sixty days'], 0,
          'MSMED Act section 15. In practice: else deduction on payment.', 'c4', T4),
        Q('m8', 'Presumptive income for professionals under section 58 is:', ['Fifty percent of gross receipts', 'Eight percent of receipts', 'Six percent of receipts', 'Thirty percent of receipts'], 0,
          'Or higher actual profit. In practice: ₹75 lakh with low cash.', 'c5', T5),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Normal depreciation', 3, 'computation', 'normal', nums=[n1, n2]), S('s2', 'Additional depreciation', 3, 'computation', 'additional', nums=[a1, a2, tot])],
          ['Mention carry-forward of balance 10%.'], ['Full rate for assets used under 180 days.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Limit computation', 3, 'computation', 'limit', nums=[lim]), S('s2', 'Disallowance', 2, 'computation', 'disallowed', nums=[dis])],
          ['Use book profit.'], ['Using 90% on the whole book profit.'], ['Two slabs.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What are the conditions for additional depreciation?', 'Manufacturing or power business, new plant or machinery acquired, installed and first used by the assessee, excluding ships, aircraft, office appliances, road vehicles and assets in office or residential premises.',
          [P('p1', 'Manufacturing or power', 5, 'manufactur|power'), P('p2', 'New machinery', 5, 'new')], 'c2'),
        V('v2', 'How does section 36(4) treat cash payments?', 'Expenditure is disallowed where payments to one person in a day exceed ₹10,000 otherwise than through an account payee cheque or draft, ECS or prescribed electronic modes.',
          [P('p1', 'Ten thousand', 5, '10,000'), P('p2', 'Specified modes', 5, 'cheque|electronic')], 'c3'),
        V('v3', 'When is a TDS-default disallowance reversed?', 'The 30% disallowed is allowed in the year in which the tax is deducted and paid.',
          [P('p1', 'Thirty percent', 5, '30%'), P('p2', 'Year of payment', 5, 'paid')], 'c3'),
        V('v4', 'Which assessees are eligible for presumptive business income?', 'Resident individuals, HUFs and firms other than LLPs that are outside specified professions and commission or agency business.',
          [P('p1', 'Resident individual, HUF, firm', 5, 'resident|huf|firm'), P('p2', 'Excludes LLP', 5, 'llp')], 'c5'),
        V('v5', 'What is the tax-audit threshold for a business with low cash transactions?', 'Ten crore rupees of turnover where cash receipts and cash payments are each within five percent.',
          [P('p1', 'Ten crore', 5, '10 crore|ten crore'), P('p2', 'Five percent cash', 5, 'five percent|5%')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Meher Traders', 'difficulty': 'moderate',
              'case': 'Meher, a resident individual trader, has turnover of ₹2,80,00,000 for T.Y. 2026-27. Of this, ₹2,70,00,000 was received through UPI and bank transfers before the return due date and ₹10,00,000 in cash. She opts for section 58.',
              'mcqs': [
                  M('k1a', 'Is she eligible for section 58 despite turnover above ₹2 crore?', ['Yes, cash receipts are within five percent', 'No, limit is two crore', 'No, traders are excluded', 'Yes, without any condition'], 0,
                    '10/280 is about 3.6%. In practice: ₹3 crore cap.', 'core', topic=T5),
                  M('k1b', 'Presumptive income on digital receipts (₹):', ['16,20,000', '21,60,000', '13,50,000', '8,10,000'], 0,
                    '6% × 2,70,00,000. In practice: received by due date.', 'core', check=1620000, topic=T5),
                  M('k1c', 'Presumptive income on cash receipts (₹):', ['80,000', '60,000', '1,00,000', '50,000'], 0,
                    '8% × 10,00,000. In practice: higher rate for cash.', 'core', check=80000, topic=T5),
                  M('k1d', 'Total presumptive business income (₹):', ['17,00,000', '16,80,000', '22,40,000', '16,20,000'], 0,
                    '16,20,000 + 80,000. In practice: or higher actual profit.', 'core', check=1700000, topic=T5),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch03', 1, 'Profits and Gains of Business or Profession',
                ['Identify income chargeable under the business head and method of accounting.',
                 'Compute depreciation and additional depreciation.',
                 'Apply specific deductions and disallowances.',
                 'Apply actual-payment rules including MSE dues.',
                 'Apply presumptive taxation, partner limits, books and tax audit.'],
                {'difficulty': 'hard', 'minutes': {'learn': 60, 'practice': 40}, 'prereq': ['fin-p4-ch02-u01'],
                 'exam_tip': 'Start from net profit, then adjust disallowances section by section with a short reason for each.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 26 charge; section 27 computation.', 'Section 33 depreciation; half rate under 180 days; 20% additional.',
                             'Section 34 residual; 35 and 36 disallowances.', 'Section 37 actual payment; MSE dues.', 'Section 58 presumptive; 62 books; 63 audit.'],
                 'remember': ['Partner remuneration: higher of ₹3 lakh/90% on first ₹6 lakh; 60% on balance.'],
                 'traps': ['Disallowing 100% instead of 30% for resident TDS default.']},
                [('Depreciation', 'Section 33'), ('General deduction', 'Section 34'), ('Actual payment', 'Section 37'), ('Presumptive', 'Section 58'), ('Tax audit', 'Section 63')],
                viva, cases)
