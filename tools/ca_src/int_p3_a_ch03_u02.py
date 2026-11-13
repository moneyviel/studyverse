"""CA Intermediate · Paper 3A Income-tax Law · Chapter 3 Heads of Income · Unit 2 Income from House Property (Income-tax Act, 2025; tax year 2026-27).
Scope follows the ICAI study material; section numbers and limits are taken from it; explanations and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-a-ch03-u02'
T1 = 'Chargeability and conditions (s. 20)'
T2 = 'Deemed owners (s. 25)'
T3 = 'Composite rent and foreign property'
T4 = 'Annual value (s. 21)'
T5 = 'Special cases: vacancy, self-occupation, stock-in-trade'
T6 = 'Deductions: 30% and interest (s. 22)'
T7 = 'Arrears and unrealised rent (s. 23)'
T8 = 'Co-owned property (s. 24) and losses'


def build():
    ck = Checks()
    er = ck.add('min(max(360000,390000),375000)', 'ER = higher of MV and FR, restricted to SR')
    act = ck.add('10*30000-30000', 'Actual rent for let period (10 months) less unrealised rent (Rule 21)')
    act_full = ck.add('12*30000-30000', 'Actual rent had there been no vacancy')
    gav = ck.add('375000', 'GAV = ER, since actual rent would be below ER even without vacancy')
    nav = ck.add('375000-36000', 'NAV = GAV − municipal taxes paid (10% of MV)')
    sd = ck.add('0.30*339000', '30% of NAV')
    inc = ck.add('339000-101700-80000', 'Income from house property')
    i1 = {'id': 'i1', 'title': 'Let-out property with vacancy and unrealised rent', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Sushma\'s flat: municipal value ₹3,60,000; fair rent ₹3,90,000; standard rent ₹3,75,000; let at ₹30,000 p.m.; vacant for 2 months; ₹30,000 rent could not be realised (Rule 21 conditions met). She paid municipal tax of 10% of municipal value and interest on a housing loan of ₹80,000. Compute income from house property for tax year 2026-27.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Expected rent', 'Higher of MV and FR (3,90,000) restricted to SR', inr(er)],
              ['Actual rent for let period', '30,000 × 10 − 30,000 unrealised', inr(act)],
              ['Test: actual rent without vacancy', '30,000 × 12 − 30,000', inr(act_full)],
              ['GAV', 'Actual would be below ER even without vacancy → ER is GAV', inr(gav)],
              ['Less municipal taxes paid', '10% × 3,60,000', inr(36000)],
              ['NAV', '', inr(nav)],
              ['Less 30% of NAV', '', inr(sd)],
              ['Less interest (no ceiling for let-out property)', '', inr(80000)],
              ['Income from house property', '', inr(inc)]], title='Computation'),
              note('Actual rent becomes the GAV only when it falls below ER because of vacancy; here the shortfall exists independently of vacancy.')],
          'checks': list(ck)}

    ck2 = Checks()
    pre = ck2.add('200000/5', 'One-fifth of pre-construction interest')
    tot = ck2.add('210000+40000', 'Current interest + 1/5 pre-construction')
    ded = ck2.add('min(250000,200000)', 'Capped at ₹2,00,000 (acquisition/construction completed within 5 years, certificate furnished)')
    i2 = {'id': 'i2', 'title': 'Self-occupied house — both regimes', 'difficulty': 'core', 'minutes': 6,
          'q': 'Vikram lives in his own house built with a bank loan taken on 1 June 2022; construction finished on 15 October 2025 (within 5 years). Pre-construction interest (to 31 March 2025) totals ₹2,00,000; interest for tax year 2026-27 is ₹2,10,000; he has the lender\'s certificate. Compute income from house property under (a) the optional regime, (b) the default regime.',
          'solution': [table(['Item', '₹'], [
              ['Annual value (self-occupied, s. 21(6))', 'Nil'],
              ['Interest for the year', inr(210000)],
              ['Add 1/5 of pre-construction interest (instalments run from tax year 2025-26, the year of completion)', inr(pre)],
              ['Total interest', inr(tot)],
              ['(a) Optional regime — deduction capped', inr(ded)],
              ['(a) Loss from house property', '(' + inr(ded) + ')'],
              ['(b) Default regime — no interest deduction for self-occupied property', 'Nil income']], title='Computation'),
              note('Pre-construction interest is spread over 5 years starting with the year of completion (2025-26), so tax year 2026-27 takes the second instalment.')],
          'checks': list(ck2)}

    ck3 = Checks()
    arr = ck3.add('40000+60000', 'Unrealised rent recovered + arrears received')
    ded3 = ck3.add('0.30*100000', '30% deduction u/s 23(3)')
    inc3 = ck3.add('100000-30000', 'Taxable under house property')
    i3 = {'id': 'i3', 'title': 'Arrears and unrealised rent after sale', 'difficulty': 'core', 'minutes': 4,
          'q': 'Farah sold her shop in February 2026. In tax year 2026-27 she recovers ₹40,000 of earlier unrealised rent (excluded from actual rent in an earlier year) and receives ₹60,000 as arrears after a rent dispute. Compute her income from house property.',
          'solution': [table(['Particulars', '₹'], [
              ['Unrealised rent recovered + arrears of rent', inr(arr)],
              ['Less 30% deduction', inr(ded3)],
              ['Income from house property', inr(inc3)]], title='Computation'),
              note('Taxable in the year of receipt even though she no longer owns the property.')],
          'checks': list(ck3)}

    av = table(['Situation', 'Gross annual value'], [
        ['Let out throughout', 'Higher of expected rent (ER) and actual rent received/receivable'],
        ['Let out, vacant part of year', 'Actual rent, if it is below ER because of vacancy; otherwise higher of ER and actual'],
        ['Self-occupied or unoccupied (up to 2 houses, individual/HUF)', 'Nil — no municipal tax deduction'],
        ['More than 2 self-occupied houses', 'Others deemed let out — ER is GAV'],
        ['Let out part of year, self-occupied part (single unit)', 'Higher of ER for whole year and actual rent for let period'],
        ['Portion let out, portion self-occupied', 'Treat each portion separately, apportioning values and taxes'],
        ['Stock-in-trade not let', 'Nil for 2 years from end of the FY of completion certificate; then ER'],
    ], title='Annual value by situation')
    interest = table(['Property', 'Default regime', 'Optional regime'], [
        ['Let out / deemed let out', '30% of NAV + full interest; loss cannot be set off against other heads', '30% of NAV + full interest; loss set off against other heads up to ₹2 lakh'],
        ['Self-occupied / unoccupied (acquisition or construction completed within 5 years from end of year of borrowing, with lender\'s certificate)', 'No deduction', 'Interest up to ₹2,00,000 in total for one or two such houses'],
        ['Self-occupied — other cases (e.g. repairs, delayed completion)', 'No deduction', 'Up to ₹30,000 (total ceiling still ₹2,00,000)'],
    ], title='Deductions u/s 22')

    concepts = [
        C('c1', T1, [
            'Section 20 charges the annual value of buildings or lands appurtenant to them (garden, garage) owned by the assessee, except portions he uses for his own business or profession whose profits are taxed.',
            'Three conditions: (i) building or appurtenant land; (ii) assessee is the owner — one entitled to receive income in his own right; registration of the deed is not essential; building owner need not own the land; leasehold ownership counts; (iii) not used for own business or profession.',
            'Letting of vacant land is taxed under other sources or business. Letting a residential house is always house property income. A person in the business of letting commercial properties is taxed under business. Sub-letting by a tenant is not house property income (other sources or business).'],
          'House property tax is a tax on ownership of a building\'s earning capacity, not on the tenant\'s use.',
          'A shop owner who runs his own business from it pays no house-property tax on that shop.'),
        C('c2', T2, [
            'Section 25 treats some non-legal owners as owners: an individual who transfers property to a spouse (except under an agreement to live apart) or to a minor child (except a minor married daughter) without adequate consideration; the holder of an impartible estate; a member to whom a co-operative society, company or AOP allots a building under a house-building scheme; a person in possession under part performance of a contract (s. 53A, Transfer of Property Act); and a person acquiring rights by sale, exchange or a lease of 12 years or more (not month-to-month or up to one-year leases), or by transactions enabling enjoyment of the property.',
            '"Child" includes step and adopted children (s. 2(25)).',
            'For arrears and unrealised rent, ownership in the year of receipt does not matter.'],
          'Deemed ownership follows the real enjoyment of the property, not the paperwork.',
          'A buyer living in a flat with full payment made but no registered deed is the owner for this head.'),
        C('c3', T3, [
            'Composite rent covers building plus other assets (furniture, machinery) or services (lifts, security, power backup). The part for services goes to business or other sources; the building part to house property.',
            'If letting of building and other assets is inseparable (tenant would not take one without the other), the whole rent is business or other-sources income, even if amounts are fixed separately. If separable, building rent is house property and asset rent goes to business/other sources, even if one composite rent is charged.',
            'Property abroad: taxable for residents (ROR) whether or not brought to India; for RNOR and non-residents only if received in India. Foreign municipal taxes paid are deductible.'],
          'Separate what the tenant pays for walls from what he pays for comforts.',
          'A furnished office let with furniture as a package the tenant must take is taxed as other-sources income.'),
        C('c4', T4, [
            'Four reference values: municipal value (MV, for municipal taxes), fair rent (FR, similar property nearby), standard rent (SR, maximum under rent control law) and actual rent received or receivable.',
            'Expected rent (ER) = higher of MV and FR, but not more than SR. GAV for a let-out property = higher of ER and actual rent (s. 21(1)).',
            'Actual rent excludes unrealised rent if Rule 21 conditions are met: bona fide tenancy; the tenant in default has left or eviction steps are under way; tenant not occupying another property of the owner; reasonable steps taken for legal recovery or shown to be futile.',
            'NAV = GAV less municipal taxes (including water, sewerage) borne and actually paid by the owner during the year — arrears are allowed when paid.'],
          'Expected rent is what the market would pay, capped by law; the owner is taxed on the better of that and what he actually gets.',
          'Rent control law can cap expected rent below what the market would pay.',
          blocks=[av]),
        C('c5', T5, [
            'Vacancy (s. 21(2)): if actual rent is below ER because of vacancy, actual rent is GAV; if it would be below ER anyway, ER is GAV.',
            'Self-occupied or unoccupied (s. 21(6)): annual value Nil for up to two houses chosen by an individual or HUF each year; others are deemed let out at ER (with municipal tax deduction). The owner must not let it at any time or derive other benefit.',
            'A single unit rented for some months and lived in by the owner for the remaining months (s. 21(7)): GAV is higher of full-year ER and actual rent; full municipal taxes paid are deductible.',
            'Stock-in-trade (builders, s. 21(5)): unlet units carry Nil annual value until two years have passed after the close of the financial year in which the completion certificate came.',
            'Portion let and portion self-occupied: compute each part separately on a reasonable basis (area, floors).'],
          'The law gives every family two homes free of notional tax; a third is taxed as if rented.',
          'An owner who lets a flat until December and moves in from January is compared against a full year\'s expected rent.'),
        C('c6', T6, [
            'Section 22 deductions are exhaustive: (a) 30% of NAV as a flat standard deduction regardless of actual repairs — not available where annual value is Nil; (b) interest on borrowed capital for acquisition, construction, repairs, renewal or reconstruction, including interest on a fresh loan to repay such a loan, on accrual basis.',
            'Pre-construction or pre-acquisition interest (period before the year of completion) is allowed in five equal instalments from the year of completion; interest for the completion year is fully allowable.',
            'Ceilings for self-occupied property apply only in the optional regime (table); the default regime allows no interest deduction for self-occupied houses. Let-out and deemed let-out properties have no ceiling in either regime.',
            'Interest payable outside India is disallowed if tax was not deducted or paid and there is no agent in India. Interest on unpaid interest is not deductible; unpaid purchase price payable with interest is treated as borrowed capital.'],
          'The 30% is the law\'s fixed allowance for upkeep; interest is the real cost of financing the house.',
          'Home-loan borrowers living in their own house usually prefer the optional regime for the ₹2 lakh interest deduction.',
          blocks=[interest]),
        C('c7', T7, [
            'Section 23: arrears of rent received, and unrealised rent later recovered, are taxed as house property income in the year of receipt, whether or not the assessee still owns the property.',
            'A deduction of 30% of the amount received is allowed (s. 23(3)); no deduction for municipal taxes or interest.'],
          'Old rent that arrives late is taxed when it lands, with a 30% allowance.',
          'Rent arrears won in a court settlement years later are taxed in the year of settlement.'),
        C('c8', T8, [
            'Section 24: co-owners with definite shares are not assessed as an AOP; each is taxed on his share.',
            'If co-owned property is self-occupied by each, annual value is Nil for each and each may claim interest up to ₹30,000/₹2,00,000 (optional regime), the ceiling covering all his self-occupied properties together.',
            'If let out, compute income as for a single owner and apportion by shares.',
            'Losses: under the default regime, house property loss cannot be set off against other heads; under the optional regime, up to ₹2 lakh can be set off against other heads in the year, the rest carried forward (Chapter 5).'],
          'Co-owners split the house\'s tax bill in proportion to their shares, each with his own interest ceiling.',
          'Two sisters co-owning a flat with a joint loan can each claim up to ₹2 lakh interest under the optional regime.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Choosing which houses are self-occupied', 'role': 'Tax consultant',
         'situation': 'A client has three houses, all used by family.',
         'steps': ['Compute income of each as if deemed let out.', 'Try each pair as self-occupied under the chosen regime, remembering interest ceilings.', 'Pick the combination with the lowest total income; the choice can change yearly.'],
         'takeaway': 'Run all combinations — the best pair differs between regimes.'},
        {'id': 'j2', 'title': 'Unrealised rent claim', 'role': 'Article assistant',
         'situation': 'A landlord wants to exclude three months\' unpaid rent.',
         'steps': ['Check Rule 21: bona fide tenancy, tenant vacated or eviction started, no other property of owner occupied, legal steps taken.', 'Exclude the amount from actual rent if all met.', 'Track it: if recovered later, tax it u/s 23 with 30% deduction.'],
         'takeaway': 'Unrealised rent is excluded only with evidence of genuine recovery efforts.'},
    ]

    mcqs = [
        Q('m1', 'Rent received for an empty plot with no building on it is taxed as:', ['Income from other sources or business income, as the case may be', 'Income from house property', 'Capital gains', 'Exempt'], 0,
          'Section 20 covers buildings and land appurtenant to them; bare land has no building, so its rent falls under other sources or business. Garden or garage land attached to a building is covered. In practice: parking-plot rent is usually other sources.', 'c1', T1),
        Q('m2', 'Income from sub-letting of a house by a tenant is taxable as:', ['Income from other sources or business, as the case may be', 'Income from house property', 'Salary', 'Capital gains'], 0,
          'The tenant is not the owner, so sub-letting income cannot be house property income; it is taxed as other sources or business depending on facts. Only owners (actual or deemed) are taxed under this head. In practice: tenants show it under other sources.', 'c1', T1),
        Q('m3', 'An individual gifts a house to his minor married daughter. For house-property purposes, the owner is:', ['The daughter', 'The father', 'Both jointly', 'The daughter\'s husband'], 0,
          'Section 25 deems the transferor to be owner when property goes to a minor child without adequate consideration, but excludes a minor married daughter; she is therefore the owner. Transfers to a spouse are similarly deemed, except under an agreement to live apart. In practice: check age and marital status.', 'c2', T2, 'moderate'),
        Q('m4', 'A person taking a building on a lease of 12 years or more:', ['Is deemed owner for house-property purposes', 'Is never an owner', 'Is owner only if he pays stamp duty', 'Is treated as a tenant'], 0,
          'Section 25 treats one who acquires rights by sale, exchange or a lease of not less than 12 years as owner; month-to-month or up to one-year leases are excluded. In practice: long-lease holders pay tax on letting the building.', 'c2', T2),
        Q('m5', 'Where letting of a building and furniture is inseparable, the composite rent is taxed as:', ['Business income or income from other sources', 'House property income', 'Partly house property and partly other sources', 'Exempt'], 0,
          'If the tenant would not take the building without the furniture, the lettings are inseparable and the entire rent goes to business or other sources, even if amounts are fixed separately. Separable lettings are split. In practice: draft agreements carefully.', 'c3', T3),
        Q('m6', 'MV ₹30,000; FR ₹36,000; SR ₹28,000; actual rent ₹25,000. The GAV is:', ['₹28,000', '₹36,000', '₹30,000', '₹25,000'], 0,
          'Expected rent is the higher of MV and FR (₹36,000) restricted to SR (₹28,000), so ER is ₹28,000; it exceeds actual rent of ₹25,000, so GAV is ₹28,000. In practice: standard rent caps the notional value.', 'c4', T4, 'core', check=28000),
        Q('m7', 'Municipal taxes are deductible from GAV when:', ['Borne by the owner and actually paid during the tax year', 'Merely levied during the year', 'Paid by the tenant', 'Due but unpaid'], 0,
          'Municipal taxes (including water and sewerage taxes) are deductible only if borne and actually paid by the owner during the year; arrears paid later are deductible in the year of payment. In practice: keep receipts for the year.', 'c4', T4),
        Q('m8', 'For self-occupied property, annual value is Nil for:', ['Up to two houses chosen by an individual or HUF', 'Only one house', 'Any number of houses', 'Two houses for all assessees including companies'], 0,
          'Section 21(6) allows Nil annual value for up to two self-occupied or unoccupied houses of an individual or HUF, chosen each year; others are deemed let out. No municipal tax deduction applies to those two. In practice: choose the pair that minimises income.', 'c5', T5),
        Q('m9', 'A builder\'s unsold flats held as stock-in-trade and not let have Nil annual value for:', ['Two years after the close of the FY of the completion certificate', 'One year', 'Five years', 'Until sold'], 0,
          'Section 21(5) keeps the annual value of unlet stock-in-trade at Nil until two years after the close of the financial year of the completion certificate; thereafter ER is taxable. In practice: builders track inventory age.', 'c5', T5, 'moderate'),
        Q('m10', 'A house is let out April–December at ₹50,000 p.m. and self-occupied January–March. ER is ₹4,80,000. GAV is:', ['₹4,80,000', '₹4,50,000', '₹3,60,000', 'Nil'], 0,
          'For a single unit let for part of the year and self-occupied for the rest, GAV is the higher of full-year ER and actual rent for the let period: ER ₹4,80,000 versus ₹4,50,000. The shortfall is due to self-occupation, not vacancy. In practice: full-year municipal tax is deductible.', 'c5', T5, 'moderate', check=480000),
        Q('m11', 'The 30% deduction u/s 22(1)(a) is computed on:', ['Net annual value', 'Gross annual value', 'Actual rent', 'Municipal value'], 0,
          'The standard deduction is 30% of NAV (GAV less municipal taxes paid), irrespective of actual repair expenses; it is not allowed where annual value is Nil. In practice: no bills are needed.', 'c6', T6),
        Q('m12', 'Under the optional regime, interest on a loan for repairs of a self-occupied house is deductible up to:', ['₹30,000', '₹2,00,000', '₹1,50,000', '₹50,000'], 0,
          'Interest on loans for repairs (or for acquisition/construction not completed within 5 years) is limited to ₹30,000; ₹2 lakh applies to timely acquisition or construction with a certificate. The default regime allows nothing for self-occupied homes. In practice: check the purpose of the loan.', 'c6', T6, 'core', check=30000),
        Q('m13', 'Pre-construction interest is allowed:', ['In five equal instalments from the year of completion', 'Fully in the year of completion', 'Over ten years', 'Not at all'], 0,
          'Interest for the period before the year of completion is deductible in five equal annual instalments starting with that year; interest for the completion year itself is fully allowable. The total for self-occupied homes remains within the ceilings. In practice: maintain a schedule.', 'c6', T6),
        Q('m14', 'Under the default regime, interest on a loan for a let-out property is:', ['Fully deductible, but resulting loss cannot be set off against other heads', 'Not deductible', 'Limited to ₹2 lakh', 'Limited to ₹30,000'], 0,
          'Let-out property interest has no ceiling in either regime, but under the default regime a house property loss cannot be set off against other heads; under the optional regime up to ₹2 lakh can be. In practice: plan rent and loan levels accordingly.', 'c6', T6, 'moderate'),
        Q('m15', 'Arrears of rent received after the property was sold are:', ['Taxable as house property income in the year of receipt with a 30% deduction', 'Not taxable as the assessee is no longer owner', 'Taxable as capital gains', 'Taxable with no deduction'], 0,
          'Section 23 taxes arrears and later-recovered unrealised rent in the year of receipt, even if the assessee no longer owns the property, allowing 30% deduction. In practice: such receipts often arise from settlements.', 'c7', T7),
        Q('m16', 'Two sisters own a house in equal shares and each lives there with her family. Under the optional regime, each:', ['Gets Nil annual value and may claim interest up to the ceiling', 'Is assessed as an AOP', 'Gets no interest deduction', 'Shares a single ₹2 lakh ceiling'], 0,
          'Co-owners with definite shares are taxed individually; for self-occupation each has Nil annual value and her own interest ceiling, though the ceiling covers all her self-occupied properties together. In practice: joint home loans give double benefit.', 'c8', T8),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Expected rent', 1, 'computation', 'expected rent|er', nums=[er]),
           S('s2', 'Actual rent and vacancy test', 2, 'computation', 'vacancy|actual', nums=[act, act_full]),
           S('s3', 'GAV and NAV', 1.5, 'computation', 'gav|nav', nums=[gav, nav]),
           S('s4', 'Deductions and income', 1.5, 'computation', '30%|interest', nums=[sd, inc])],
          ['Show the vacancy test explicitly.'], ['Taking actual rent as GAV just because there was vacancy.'], ['Step table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Nil annual value', 0.5, 'concept', 'nil'),
           S('s2', 'Pre-construction 1/5', 1, 'computation', '1/5|one-fifth|pre-construction', nums=[pre]),
           S('s3', 'Ceiling ₹2 lakh', 1.5, 'computation', '2,00,000|ceiling|restricted', nums=[ded]),
           S('s4', 'Default regime — no deduction', 1, 'concept', 'default', 'no interest|not allowed|nil')],
          ['Compute both regimes.'], ['Applying the ₹2 lakh cap under the default regime.'], ['Table.'], pad='table', checks=list(ck2)),
        W('q3', 4, 'Explain the conditions in Rule 21 for excluding unrealised rent and the treatment if it is later recovered.',
          [ul(['The tenancy is bona fide.', 'The tenant in default has left, or eviction steps are under way.', 'He is not occupying any other property of the assessee.', 'The assessee has taken reasonable steps to institute legal proceedings for recovery, or satisfies the AO that they would be futile.']),
           p('If unrealised rent is recovered later, it is taxed under section 23 in the year of recovery, whether or not the assessee owns the property then, with a deduction of 30%.')],
          [S('s1', 'Bona fide tenancy', 0.5, 'concept', 'bona fide'),
           S('s2', 'Tenant vacated / steps', 0.75, 'concept', 'vacat|left|evict'),
           S('s3', 'No other property occupied', 0.75, 'concept', 'not occupying|any other property|another property'),
           S('s4', 'Legal proceedings', 0.75, 'concept', 'legal|proceeding'),
           S('s5', 'Later recovery taxed u/s 23 with 30%', 1.25, 'concept', '23|recover', '30%')],
          ['Four conditions + recovery rule.'], ['Forgetting the 30% deduction on recovery.'], ['Bulleted list.']),
    ]

    viva = [
        V('v1', 'How is expected rent determined?',
          'Take the bigger of municipal value and fair rent; that figure cannot exceed the standard rent fixed under rent control law.',
          [P('p1', 'Higher of MV and FR', 6, 'municipal', 'fair'), P('p2', 'Restricted to SR', 4, 'standard')], 'c4'),
        V('v2', 'What deductions are allowed under section 22?',
          'Thirty percent of net annual value as a flat deduction, and interest on borrowed capital for acquisition, construction, repairs, renewal or reconstruction of the property.',
          [P('p1', '30% of NAV', 5, 'thirty|30%'), P('p2', 'Interest on borrowed capital', 5, 'interest')], 'c6'),
        V('v3', 'When is interest on a self-occupied house deductible up to ₹2 lakh?',
          'Under the optional regime, when the loan is for acquisition or construction completed within five years from the end of the tax year of borrowing and the lender\'s interest certificate is furnished.',
          [P('p1', 'Optional regime', 2, 'optional'), P('p2', 'Acquisition/construction within 5 years', 5, 'five years|5 years'), P('p3', 'Lender certificate', 3, 'certificate')], 'c6'),
        V('v4', 'How are arrears of rent taxed?',
          'In the year of receipt, under house property, even if the person no longer owns the property, after a deduction of thirty percent.',
          [P('p1', 'Year of receipt', 4, 'year of receipt|received'), P('p2', 'Ownership not required', 3, 'no longer|not the owner|even if'), P('p3', '30% deduction', 3, 'thirty|30%')], 'c7'),
        V('v5', 'What are the three conditions for income to be taxed as house property?',
          'There must be a building or land appurtenant to it, the assessee must own it, and he must not use it for his own business or profession whose profits are taxed.',
          [P('p1', 'Building or appurtenant land', 3, 'building'), P('p2', 'Owner', 3, 'own'), P('p3', 'Not used for own business', 4, 'business|profession')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'The Kulkarni properties', 'difficulty': 'moderate',
              'case': 'Mr. Kulkarni owns: (A) a flat in Nashik where he lives; (B) a bungalow in Lonavala kept for weekends, never let; (C) a flat in Pune let to a tenant; (D) a cottage in Goa used by his family during holidays. He has a home loan on (A) for its purchase completed within 3 years, interest ₹2,40,000, and pays tax under the optional regime.',
              'mcqs': [
                  M('k1a', 'How many of his houses can have Nil annual value?', ['Two, chosen by him', 'Three — A, B and D', 'All four', 'One'], 0,
                    'An individual can treat at most two self-occupied or unoccupied houses as having Nil annual value; among A, B and D he chooses two, and the third is deemed let out at expected rent. C is actually let out. In practice: he should test each pair.', 'core', topic=T5),
                  M('k1b', 'The maximum interest deduction for flat A (self-occupied) is:', ['₹2,00,000', '₹2,40,000', '₹30,000', 'Nil'], 0,
                    'Under the optional regime, interest on a loan for acquisition completed within five years, with a certificate, is deductible up to ₹2 lakh for self-occupied property. Under the default regime it would be nil. In practice: the excess ₹40,000 is lost.', 'core', check=200000, topic=T6),
                  M('k1c', 'The house not chosen as self-occupied among A, B and D will be taxed on:', ['Expected rent as GAV, less municipal taxes, 30% and interest', 'Nil value', 'Actual rent only', 'Capital value'], 0,
                    'A house beyond the two Nil-value houses is deemed let out; its GAV is the expected rent, from which municipal taxes, 30% of NAV and any interest are deducted. There is no vacancy allowance. In practice: deemed rent often makes this the costliest choice.', 'moderate', topic=T5),
                  M('k1d', 'If the Pune flat (C) shows a loss, under the optional regime it can be set off against his salary up to:', ['₹2,00,000', 'Any amount', 'Nil', '₹50,000'], 0,
                    'Under the optional regime, house property loss can be set off against other heads up to ₹2 lakh in a year, with the balance carried forward; under the default regime no inter-head set-off is allowed. In practice: this is a key regime consideration.', 'moderate', check=200000, topic=T8),
              ]}]

    return unit(UID, 'p3', 'int-p3-a-ch03', 2, 'Income from House Property',
                ['Explain the conditions for taxing income under "Income from house property" and deemed ownership.',
                 'Treat composite rent and foreign property correctly.',
                 'Determine annual value for let-out, vacant, self-occupied, deemed let-out and stock-in-trade property.',
                 'Apply deductions u/s 22 under both regimes and tax arrears and unrealised rent.',
                 'Compute income of co-owners.'],
                {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 40}, 'prereq': ['int-p3-a-ch03-u01'],
                 'exam_tip': 'Expect a GAV/NAV computation with vacancy or unrealised rent and a self-occupied interest question under both regimes; remember ER = max(MV, FR) capped at SR.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Charge: annual value of owned buildings not used for own business (s. 20).', 'Deemed owners: spouse/minor transfers, 12-year leases, part-performance, society allotments (s. 25).',
                             'ER = higher of MV and FR, capped at SR; GAV = higher of ER and actual rent.', 'Vacancy: actual rent is GAV only if shortfall is due to vacancy.',
                             'Two self-occupied houses → Nil; others deemed let out.', 'Deductions: 30% of NAV + interest; self-occupied interest only in optional regime (₹2 L / ₹30,000).',
                             'Arrears and unrealised rent: taxed on receipt, 30% deduction (s. 23).', 'Default regime: HP loss not set off against other heads.'],
                 'remember': ['Pre-construction interest: 5 equal instalments from completion year.', 'Municipal tax deductible only when paid by owner.'],
                 'traps': ['No 30% deduction on Nil-value property.', 'Sub-letting income is not house property income.']},
                [('ER', 'max(MV, FR) capped at SR'), ('Standard deduction', '30% of NAV'), ('SOP interest (optional)', '₹2,00,000 / ₹30,000'), ('Nil value houses', '2 (individual/HUF)'),
                 ('Arrears deduction', '30% (s. 23)'), ('Stock-in-trade Nil value', '2 years after completion certificate year')],
                viva, cases,
                topics=['Structured Sectional Learning', 'Chargeability', 'Conditions for Chargeability', 'Composite Rent', 'Income from House Property Situated outside India',
                        'Determination of Annual Value', 'Deductions from Annual Value', 'Computation of Income from House Property for Different Categories of Property',
                        'Provision for Arrears of Rent and Unrealized Rent Received Subsequently', 'Treatment of Income from Co-owned Property'])
