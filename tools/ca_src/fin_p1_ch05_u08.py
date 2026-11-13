"""CA Final · Paper 1 Financial Reporting · Chapter 5 Unit 8 Ind AS 116 Leases.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch05-u08'
T1 = 'Identifying a lease'
T2 = 'Lessee accounting: right-of-use asset and lease liability'
T3 = 'Lessor accounting: finance and operating leases'
T4 = 'Special situations: modifications, sale and leaseback, exemptions'


def build():
    ck = Checks()
    pv = ck.add('10*3.7908', 'Initial lease liability (₹ lakh)')
    intr = ck.add('10*3.7908*0.1', 'Interest for year 1 (₹ lakh)')
    cl = ck.add('10*3.7908*1.1-10', 'Liability at end of year 1 (₹ lakh)')
    rou = ck.add('10*3.7908+1.2', 'Right-of-use asset (₹ lakh)')
    dep = ck.add('(10*3.7908+1.2)/5', 'Depreciation year 1 (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Leasing a warehouse', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Kite Logistics leases a warehouse for 5 years, paying ₹10 lakh at the end of each year. The rate implicit in the lease is not readily determinable; the incremental borrowing rate is 10% (5-year annuity factor 3.7908). Initial direct costs are ₹1.2 lakh. Compute the lease liability and right-of-use asset at commencement, year-1 interest, closing liability and year-1 depreciation (straight-line).',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Lease liability at commencement', '10 × 3.7908', inr(pv)],
              ['Right-of-use asset', 'Liability + initial direct costs 1.2', inr(rou)],
              ['Interest year 1', '37.908 × 10%', inr(intr)],
              ['Liability end of year 1', '37.908 + 3.7908 − 10', inr(cl)],
              ['Depreciation year 1', '39.108 ÷ 5', inr(dep)]], title='Lessee accounting')],
          'checks': list(ck)}

    ck2 = Checks()
    nil = ck2.add('25*3.1699', 'Net investment in the lease (₹ lakh)')
    fi = ck2.add('25*3.1699*0.1', 'Finance income year 1 (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'A lessor with a finance lease', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Vega Leasing leases a machine for its entire 4-year economic life, receiving ₹25 lakh at the end of each year. The rate implicit in the lease is 10% (4-year annuity factor 3.1699). There is no residual value. Classify the lease and compute the net investment and year-1 finance income.',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Classification', 'Lease term covers the whole economic life — risks and rewards pass', 'Finance lease'],
              ['Net investment in the lease', '25 × 3.1699', inr(nil)],
              ['Finance income year 1', '79.2475 × 10%', inr(fi)],
              ['Machine', 'Derecognised by the lessor', '—']], title='Lessor accounting')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A contract contains a lease when, for a period, it gives the customer the right to direct the use of a specified (identified) asset and to obtain substantially all its economic benefits, in return for payment.',
            'Identified asset: explicitly or implicitly specified, with no substantive substitution right for the supplier (a right is substantive only if the supplier can practically substitute and would benefit from doing so). A capacity portion is identified only if physically distinct or substantially all of the capacity.',
            'Right to direct use: the customer decides how and for what purpose the asset is used, or those decisions are predetermined and the customer operates or designed the asset. Lease and non-lease components are separated, though a lessee may elect, by class of asset, not to separate them.'],
          'Ask: is there a specific asset, and does the customer call the shots and get the benefits?',
          'A dedicated rail wagon is a lease; a courier service using any truck from a pool is not.'),
        C('c2', T2, [
            'At commencement, the lessee recognises a lease liability: the present value of unpaid lease payments (fixed payments less incentives, index-linked variable payments, residual value guarantees, purchase options reasonably certain, and termination penalties), discounted at the rate implicit in the lease or, if not readily determinable, the incremental borrowing rate.',
            'The right-of-use asset is measured at the liability plus payments made at or before commencement (less incentives received), initial direct costs and estimated restoration costs.',
            'Afterwards, the asset is depreciated (over the shorter of lease term and useful life unless ownership transfers) and tested for impairment; the liability accrues interest and is reduced by payments. Remeasurement occurs when lease term, purchase option assessment, residual guarantees or index-linked payments change, with the adjustment to the right-of-use asset.'],
          'Lessees bring every lease on-balance sheet: an asset to use, a debt to pay.',
          'Rent of 10 a year for 5 years at 10% becomes a liability of about 37.9.'),
        C('c3', T3, [
            'Lessors classify each lease. A finance lease passes to the lessee nearly all the risks and rewards that come with owning the asset; otherwise it is an operating lease. Indicators include transfer of ownership, a bargain purchase option, lease term for the major part of economic life, present value of payments amounting to substantially all of fair value, and a specialised asset.',
            'Finance lease: derecognise the asset and recognise a receivable equal to the net investment in the lease; recognise finance income producing a constant periodic return. Manufacturer or dealer lessors also recognise selling profit at commencement.',
            'Operating lease: keep the asset, depreciate it and recognise lease income on a straight-line (or other systematic) basis; initial direct costs are added to the asset and expensed over the lease term.'],
          'Lessors still use the old two-way split; lessees do not.',
          'Leasing a machine for its whole life is a finance lease for the lessor.'),
        C('c4', T4, [
            'Recognition exemptions: a lessee may elect not to recognise short-term leases (12 months or less, no purchase option) and leases of low-value underlying assets; payments are then expensed straight-line.',
            'Lease modifications: a modification that adds a right of use at a stand-alone price is a separate lease; otherwise the lessee remeasures the liability at a revised discount rate and adjusts the asset (with a gain or loss for scope reductions).',
            'Sale and leaseback: if the transfer is a sale under Ind AS 115, the seller-lessee measures the right-of-use asset at the proportion of the previous carrying amount retained and recognises only the gain on rights transferred. If not a sale, the asset stays and proceeds are a financial liability.'],
          'Exemptions keep small and short leases simple; modifications and sale-leasebacks need careful arithmetic.',
          'A laptop lease can be expensed as low-value.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Building a lease register', 'role': 'Assistant finance manager',
             'situation': 'A retail chain has 150 store leases and wants Ind AS 116 compliance.',
             'steps': ['Identify which contracts contain leases.', 'Decide the lease term including extension options reasonably certain.', 'Compute liabilities and right-of-use assets using borrowing rates.', 'Set up remeasurement triggers.'],
             'takeaway': 'Lease term and discount rate are the judgements that move the numbers most.'}]

    mcqs = [
        Q('m1', 'If the rate implicit in the lease cannot be readily determined, the lessee uses:', ['Its incremental borrowing rate', 'The bank rate', 'Zero', 'The lessor\'s cost of capital'], 0,
          'This is the fallback discount rate. In practice: adjust for term and security.', 'c2', T2),
        Q('m2', 'Initial direct costs incurred by a lessee are:', ['Added to the right-of-use asset', 'Expensed', 'Added to the liability', 'Ignored'], 0,
          'They form part of the asset\'s cost. In practice: examples include commissions.', 'c2', T2),
        Q('m3', 'A supplier\'s substitution right makes the asset not identified when:', ['It is practically able to substitute and would benefit economically', 'It exists in the contract', 'The customer agrees', 'The asset is small'], 0,
          'Both conditions are needed. In practice: most substitution rights are not substantive.', 'c1', T1),
        Q('m4', 'Under Ind AS 116, lessors classify leases as:', ['Finance or operating', 'Only finance', 'Only operating', 'Short or long'], 0,
          'Lessor accounting retains the dual model. In practice: assess risks and rewards.', 'c3', T3),
        Q('m5', 'A lease of 12 months or less without a purchase option may be:', ['Expensed under the short-term exemption', 'Capitalised always', 'Treated as a finance lease', 'Ignored'], 0,
          'An election by class of asset. In practice: disclose the expense.', 'c4', T4),
        Q('m6', 'Lease income under an operating lease is recognised by the lessor:', ['On a straight-line or other systematic basis', 'When cash is received', 'Upfront', 'At the end'], 0,
          'This spreads income over the term. In practice: free months are spread too.', 'c3', T3),
        Q('m7', 'In a sale and leaseback that qualifies as a sale, the seller-lessee recognises gain:', ['Only on the rights transferred to the buyer-lessor', 'In full', 'Not at all', 'In OCI'], 0,
          'The retained portion is not a disposal. In practice: compute the proportion retained.', 'c4', T4),
        Q('m8', 'Variable payments linked to sales are:', ['Excluded from the lease liability and expensed', 'Included at expected value', 'Capitalised', 'Treated as a guarantee'], 0,
          'Only index or rate-linked variables are included. In practice: percentage rent is expensed.', 'c2', T2),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Liability', 2, 'computation', 'liability', nums=[pv]), S('s2', 'Right-of-use asset', 2, 'computation', 'right-of-use', nums=[rou]), S('s3', 'Interest and closing', 2, 'computation', 'interest', nums=[intr, cl]), S('s4', 'Depreciation', 2, 'computation', 'depreciation', nums=[dep])],
          ['Use the borrowing rate.'], ['Leaving initial direct costs out of the asset.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Classification', 1.5, 'concept', 'finance lease'), S('s2', 'Net investment', 2, 'computation', 'net investment', nums=[nil]), S('s3', 'Finance income', 1.5, 'computation', 'finance income', nums=[fi])],
          ['Give the indicator.'], ['Keeping the machine on the lessor\'s books.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'When does a contract contain a lease?', 'When it gives the customer, for a period and in return for payment, control over how an identified asset is used.',
          [P('p1', 'Identified asset', 5, 'identified'), P('p2', 'Control of use', 5, 'control')], 'c1'),
        V('v2', 'What is included in the right-of-use asset at commencement?', 'The lease liability, payments made at or before commencement less incentives, initial direct costs and estimated restoration costs.',
          [P('p1', 'Liability and payments', 5, 'liability|payment'), P('p2', 'Direct and restoration costs', 5, 'direct|restoration')], 'c2'),
        V('v3', 'What makes a lease a finance lease for the lessor?', 'The lessee takes on nearly all the risks and rewards that come with ownership of the asset.',
          [P('p1', 'Risks and rewards', 6, 'risk|reward'), P('p2', 'Ownership', 4, 'ownership')], 'c3'),
        V('v4', 'Which recognition exemptions are available to lessees?', 'Short-term leases of twelve months or less and leases of low-value assets, with payments expensed on a straight-line basis.',
          [P('p1', 'Short-term', 5, 'short-term'), P('p2', 'Low-value', 5, 'low-value')], 'c4'),
        V('v5', 'How is the lease liability measured subsequently?', 'It increases by interest at the discount rate and decreases by lease payments, with remeasurement when payments or assessments change.',
          [P('p1', 'Interest and payments', 6, 'interest'), P('p2', 'Remeasurement', 4, 'remeasure')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Metro Mart Ltd.', 'difficulty': 'moderate',
              'case': 'Metro Mart Ltd. leases a store for 3 years with an option to extend by 2 years that it is reasonably certain to exercise. Rent is ₹20 lakh a year in arrears; 5-year annuity factor at its 9% borrowing rate is 3.8897. It also rents laptops worth ₹40,000 each and a temporary kiosk for 6 months. Store rent includes a 2% share of sales.',
              'mcqs': [
                  M('k1a', 'Lease term for measurement:', ['5 years', '3 years', '2 years', '6 months'], 0,
                    'Reasonably certain extensions are included. In practice: reassess on significant events.', 'core', topic=T2),
                  M('k1b', 'Initial lease liability for the store (₹ lakh):', ['77.794', '60', '100', '50.62'], 0,
                    '20 × 3.8897 = 77.794. In practice: discount at the borrowing rate.', 'moderate', check=77.794, topic=T2),
                  M('k1c', 'The 2% share of sales is:', ['Expensed as incurred, outside the liability', 'Included in the liability', 'Added to the asset', 'A guarantee'], 0,
                    'Sales-based variable payments are excluded. In practice: disclose them.', 'core', topic=T2),
                  M('k1d', 'The laptops and the 6-month kiosk can be:', ['Expensed under the low-value and short-term exemptions', 'Capitalised', 'Finance leases', 'Ignored'], 0,
                    'Both qualify for the exemptions. In practice: apply consistently by class.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch05', 8, 'Ind AS 116 "Leases"',
                ['Identify whether a contract contains a lease.',
                 'Measure lessee right-of-use assets and lease liabilities.',
                 'Classify and account for leases by lessors.',
                 'Apply exemptions, modifications and sale and leaseback rules.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 40}, 'prereq': ['fin-p1-ch05-u07'],
                 'exam_tip': 'Set out the lease term and discount rate first; then build the liability table year by year.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Lease: identified asset + right to control its use.',
                             'Lessee: liability at PV; asset = liability + extras.',
                             'Depreciate asset; unwind interest on liability.',
                             'Lessor: finance vs operating by risks and rewards.',
                             'Exemptions: short-term and low-value.'],
                 'remember': ['Sales-based rent is not in the liability.'],
                 'traps': ['Ignoring reasonably certain extension options.']},
                [('Discount rate', 'Implicit, else incremental borrowing'), ('ROU asset', 'Liability + IDC + prepayments + restoration'), ('Lessor', 'Finance or operating'), ('Exemptions', 'Short-term, low-value')],
                viva, cases)
