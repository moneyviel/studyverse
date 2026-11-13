"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 5 Unit 5 — AS 19 Leases.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch05-u05'
T1 = 'Scope and key terms of AS 19'
T2 = 'Finance lease or operating lease?'
T3 = 'Leases in the books of the lessee'
T4 = 'Leases in the books of the lessor'
T5 = 'Sale and leaseback'


def build():
    ck = Checks()
    pv = ck.add('200000*(0.9091+0.8264+0.7513)', 'Present value of lease payments at 10% (₹)')
    init = ck.add('min(500000, 497360)', 'Asset and liability recognised (₹)')
    int1 = ck.add('497360*10/100', 'Finance charge in year 1 (₹)')
    prin = ck.add('200000-49736', 'Reduction of liability in year 1 (₹)')
    clos = ck.add('497360-150264', 'Liability at end of year 1 (₹)')
    i1 = {'id': 'i1', 'title': 'A finance lease for the lessee', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Lata Ltd. leased a machine (fair value ₹5,00,000; useful life 3 years) for 3 years at ₹2,00,000 a year payable at each year end. The rate implicit in the lease is 10% (PV factors 0.9091, 0.8264, 0.7513). Compute the amount recognised and the year-1 split of the payment.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['PV of lease payments', '2,00,000 × 2.4868', inr(pv)],
              ['Recognised (lower of fair value and PV)', 'Lower of 5,00,000 and 4,97,360', inr(init)],
              ['Finance charge, year 1', '4,97,360 × 10%', inr(int1)],
              ['Principal repaid, year 1', '2,00,000 − 49,736', inr(prin)],
              ['Liability carried forward', '', inr(clos)]], title='Lessee — finance lease'),
              note('The lease covers the whole useful life, so it is a finance lease. The asset is depreciated like owned assets; with no certainty of ownership, over the shorter of lease term and useful life.')],
          'checks': list(ck)}

    ck2 = Checks()
    sl = ck2.add('120000*3/4', 'Straight-line lease expense per year (₹)')
    i2 = {'id': 'i2', 'title': 'Rent-free period in an operating lease', 'difficulty': 'core', 'minutes': 5,
          'q': 'Bindu Ltd. took office space on a 4-year operating lease: no rent in year 1 and ₹1,20,000 a year in years 2–4. What lease expense is recognised each year?',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Total payments', '3 × 1,20,000', inr(360000)],
              ['Expense each year', '3,60,000 ÷ 4', inr(sl)]], title='Operating lease — lessee'),
              p('Year 1 expense of ₹90,000 is accrued as a liability; it is released as rent of ₹1,20,000 is paid in later years. Straight-line applies unless another systematic basis better reflects the pattern of benefit.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A lease is an agreement under which the owner (lessor) lets another party (lessee) use an asset for a fixed time in exchange for one or more payments.',
            'AS 19 does not apply to leases to explore or use natural resources (oil, gas, timber, minerals), licensing agreements for films, videos, plays, manuscripts, patents and copyrights, and leases of land.',
            'Minimum lease payments (MLP) for the lessee are the payments over the lease term (excluding contingent rent, service costs and taxes) plus any residual value guaranteed by the lessee or a related party. For the lessor, MLP also include residual value guaranteed by a third party.',
            'Gross investment of the lessor = MLP + unguaranteed residual value; net investment = gross investment discounted at the interest rate implicit in the lease; the difference is unearned finance income.'],
          'A lease rents the use of an asset; the accounting follows who really bears ownership risk.',
          'A 10-year lease of a delivery fleet is within AS 19; a mining lease is not.'),
        C('c2', T2, [
            'A finance lease passes almost all the risks and rewards of owning the asset to the lessee, whether or not legal title ever moves. All other leases are operating leases.',
            'Indicators of a finance lease: ownership passes at the end; a bargain purchase option; the lease term covers the major part of the asset\'s economic life; the present value of MLP at inception is at least substantially all of the fair value; the asset is so specialised that only the lessee can use it without major changes.',
            'Other pointers: lessee bears the lessor\'s losses on cancellation; gains or losses on residual value fall on the lessee; option to extend at a rent well below market.',
            'Classification is made at the inception of the lease and depends on substance, not the form of the contract.'],
          'Ask who would suffer if the asset broke down or lost value.',
          'A lease of a custom-built machine for its entire life is a finance lease even though the lessor keeps title.'),
        C('c3', T3, [
            'Finance lease: the lessee recognises an asset and a liability at the lower of fair value and the present value of MLP at inception, discounted at the rate implicit in the lease (or the lessee\'s incremental borrowing rate if not practicable). Initial direct costs are added to the asset.',
            'Each payment is split into finance charge and reduction of the liability, so the finance charge gives a constant periodic rate on the outstanding liability.',
            'The leased asset is depreciated on the same basis as owned assets; if ownership is not reasonably certain, over the shorter of lease term and useful life. AS 28 also applies.',
            'Operating lease: lease payments are charged evenly across the lease period, unless some other systematic pattern better represents the time pattern of the user\'s benefit.'],
          'Finance lease: book it like a loan-financed purchase; operating lease: book it like rent.',
          'A finance lessee shows both depreciation and interest; an operating lessee shows lease rent.'),
        C('c4', T4, [
            'Finance lease: the lessor shows a receivable equal to its net investment in the lease. Finance income is recognised to give a constant periodic return on the net investment outstanding. Unguaranteed residual values are reviewed; any reduction is recognised immediately.',
            'A manufacturer or dealer lessor recognises selling profit or loss as for an outright sale; if artificially low rates are quoted, profit is restricted to what would arise at a commercial rate. Initial direct costs are expensed.',
            'Operating lease: the lessor keeps the asset in its balance sheet and depreciates it like similar assets; lease income is recognised on a straight-line basis (unless another systematic basis is more representative). Initial direct costs are deferred over the lease term or expensed.'],
          'Finance lessor holds a receivable; operating lessor holds the asset.',
          'A car rental company leasing cars for weeks keeps them as its PPE.'),
        C('c5', T5, [
            'In a sale and leaseback, the seller sells an asset and leases it back.',
            'If the leaseback is a finance lease, any surplus of sale price over carrying amount is not taken to profit at once; it is spread over the lease period.',
            'If it is an operating lease at fair value, profit or loss is recognised at once. If the price is below fair value, the loss is recognised at once — unless it is compensated by future rentals below market, in which case it is deferred and amortised. If the price is above fair value, the excess over fair value is deferred and amortised over the period of use.',
            'If fair value is below carrying amount in an operating leaseback, that loss is recognised immediately.'],
          'In a leaseback the seller never really let go, so profits are often spread out.',
          'Selling a building for ₹15 crore (fair value ₹12 crore) and leasing it back on an operating lease: ₹3 crore is deferred.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Classifying a new lease', 'role': 'Audit assistant',
             'situation': 'A client has leased specialised packaging equipment for 7 years; its life is 8 years.',
             'steps': ['Compare lease term with economic life.', 'Compute PV of MLP against fair value.', 'Check purchase options and specialisation.', 'Record asset and liability if finance lease.'],
             'takeaway': 'Substance, not the label in the contract, decides the accounting.'}]

    mcqs = [
        Q('m1', 'A finance lease is one that:', ['Transfers substantially all risks and rewards of ownership', 'Always transfers legal title', 'Runs for more than five years', 'Is cancellable at short notice'], 0,
          'Classification depends on whether substantially all the risks and rewards incidental to ownership move to the lessee; title may or may not pass. Length alone is not decisive. In practice: weigh all indicators.', 'c2', T2),
        Q('m2', 'AS 19 does NOT apply to:', ['Leases of land', 'Leases of machinery', 'Leases of vehicles', 'Leases of office equipment'], 0,
          'AS 19 excludes leases of land, leases to explore or use natural resources and licensing agreements for items such as films, patents and copyrights. Plant, vehicles and equipment are covered. In practice: check the asset type first.', 'c1', T1),
        Q('m3', 'A lessee recognises a finance-leased asset at:', ['The lower of fair value and PV of minimum lease payments', 'Fair value always', 'Total lease payments', 'Carrying amount in the lessor\'s books'], 0,
          'At inception the lessee records the asset and liability at the lower of the asset\'s fair value and the present value of minimum lease payments, plus initial direct costs added to the asset. In practice: use the implicit rate where possible.', 'c3', T3),
        Q('m4', 'Opening lease liability ₹6,00,000; implicit rate 12%; annual payment in arrears ₹2,00,000. Liability after the first payment:', ['₹4,72,000', '₹4,00,000', '₹5,28,000', '₹4,28,000'], 0,
          'Finance charge = 12% of ₹6,00,000 = ₹72,000; principal repaid = ₹2,00,000 − 72,000 = ₹1,28,000; closing liability = ₹4,72,000. This keeps a constant rate on the balance. In practice: prepare an amortisation table.', 'c3', T3, 'hard', check=472000),
        Q('m5', 'Lease payments under an operating lease are expensed by the lessee:', ['On a straight-line basis, unless another systematic basis is more representative', 'As paid', 'In the first year', 'At the end of the lease'], 0,
          'AS 19 requires operating lease payments to be expensed evenly across the lease period, unless another systematic pattern better reflects the pattern of benefit. Rent-free periods are averaged. In practice: accrue or prepay the difference.', 'c3', T3),
        Q('m6', 'In a finance lease, the lessor records:', ['A receivable equal to the net investment in the lease', 'The leased asset as PPE', 'Lease rent as income on a straight-line basis', 'Nothing until payment'], 0,
          'The lessor in a finance lease derecognises the asset and shows a receivable equal to its net investment, earning finance income at a constant periodic rate. An operating lessor keeps the asset. In practice: separate unearned income.', 'c4', T4),
        Q('m7', 'For the lessee, minimum lease payments include:', ['Residual value guaranteed by the lessee', 'Contingent rent', 'Service and tax costs paid by the lessor', 'Unguaranteed residual value'], 0,
          'Lessee MLP are payments over the lease term excluding contingent rent, service costs and taxes, plus any residual value the lessee or a related party guarantees. Unguaranteed residual value belongs to the lessor\'s gross investment. In practice: read guarantee clauses.', 'c1', T1),
        Q('m8', 'A leased asset with no reasonable certainty of ownership is depreciated over:', ['The shorter of lease term and useful life', 'Its useful life always', 'The lease term always', 'Five years'], 0,
          'If it is not reasonably certain that the lessee will get ownership by the end of the lease, the asset is fully depreciated over the shorter of the lease term and its useful life. In practice: purchase options can change this.', 'c3', T3),
        Q('m9', 'Sale and operating leaseback at a price above fair value: the excess over fair value is:', ['Deferred and amortised over the period of use', 'Recognised immediately', 'Credited to capital reserve', 'Added to the asset'], 0,
          'Where the sale price exceeds fair value in an operating leaseback, the excess is deferred and amortised over the period the asset is expected to be used, as it is effectively financed by higher rents. In practice: profit up to fair value is recognised.', 'c5', T5),
        Q('m10', 'A manufacturer lessor quoting an artificially low interest rate restricts selling profit to:', ['What would arise if a commercial rate were charged', 'Nil', 'The full selling price', 'The finance income'], 0,
          'Manufacturer or dealer lessors recognise selling profit as on an outright sale, but if artificially low rates are quoted, profit is limited to what a commercial rate would produce. Initial direct costs are expensed. In practice: test the rate quoted.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Present value and recognition', 2, 'computation', 'lower', nums=[pv, init]),
           S('s2', 'Finance charge', 2, 'computation', 'finance', nums=[int1]),
           S('s3', 'Principal and closing liability', 2, 'computation', 'liability', nums=[prin, clos])],
          ['Use the implicit rate.'], ['Recognising at fair value when PV is lower.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Straight-line expense', 2, 'computation', 'straight', nums=[sl]),
           S('s2', 'Accrual in year 1', 1, 'concept', 'accru|liability')],
          ['Average total payments over the term.'], ['Showing nil expense in year 1.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a finance lease?', 'A lease that hands almost all the risks and rewards of owning the asset to the lessee; legal title may stay with the lessor.',
          [P('p1', 'Risks and rewards', 6, 'risk', 'reward'), P('p2', 'Title may not pass', 4, 'title')], 'c2'),
        V('v2', 'Give three indicators of a finance lease.', 'Ownership passing at the end, a bargain purchase option, the lease term covering most of the economic life, PV of payments close to fair value, or a specialised asset.',
          [P('p1', 'Ownership or option', 4, 'ownership|option'), P('p2', 'Life or PV test', 6, 'economic life|present value|fair value|specialised')], 'c2'),
        V('v3', 'How does a lessee account for a finance lease?', 'It records an asset and liability at the lower of fair value and PV of minimum lease payments, splits payments into finance charge and principal, and depreciates the asset.',
          [P('p1', 'Asset and liability at lower', 5, 'lower'), P('p2', 'Split payments and depreciate', 5, 'finance charge|depreciat')], 'c3'),
        V('v4', 'How does a lessor account for an operating lease?', 'It keeps the asset on its balance sheet, depreciates it and recognises lease income on a straight-line basis.',
          [P('p1', 'Asset stays with lessor', 5, 'balance sheet|asset'), P('p2', 'Straight-line income', 5, 'straight')], 'c4'),
        V('v5', 'How is profit on a sale and finance leaseback treated?', 'Any excess of sale proceeds over carrying amount is deferred and amortised over the lease term.',
          [P('p1', 'Deferred', 6, 'deferr'), P('p2', 'Over lease term', 4, 'lease term|amortis')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Sneha Packaging Ltd.', 'difficulty': 'moderate',
              'case': 'Sneha Packaging Ltd. sold its warehouse (carrying amount ₹8 crore, fair value ₹10 crore) for ₹11 crore and leased it back for 5 years on an operating lease at above-market rent. It also leased a specially designed machine for 9 of its 10 years of life.',
              'mcqs': [
                  M('k1a', 'Profit recognised immediately on the warehouse sale:', ['₹2 crore', '₹3 crore', '₹1 crore', 'Nil'], 0,
                    'In an operating leaseback above fair value, profit up to fair value (₹10 crore − ₹8 crore = ₹2 crore) is recognised at once, and the ₹1 crore excess over fair value is deferred. In practice: amortise the excess over the use period.', 'moderate', check=2, topic=T5),
                  M('k1b', 'Amount deferred and amortised:', ['₹1 crore', '₹3 crore', '₹2 crore', 'Nil'], 0,
                    'The excess of sale price ₹11 crore over fair value ₹10 crore, ₹1 crore, is deferred and amortised over the period of use because it is recovered through higher rents. In practice: show it as deferred income.', 'moderate', check=1, topic=T5),
                  M('k1c', 'The machine lease is:', ['A finance lease', 'An operating lease', 'Outside AS 19', 'A sale and leaseback'], 0,
                    'The lease covers the major part of the asset\'s economic life and the machine is specialised, both indicators that substantially all risks and rewards pass, so it is a finance lease. In practice: record asset and liability.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch05', 5, 'Accounting Standard 19 Leases',
                ['Explain the scope and key terms of AS 19.',
                 'Classify leases as finance or operating.',
                 'Account for finance and operating leases by lessees and lessors.',
                 'Account for sale and leaseback transactions.'],
                {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 40}, 'prereq': ['int-p1-ch05-u04'],
                 'exam_tip': 'Classify first using risks and rewards; then build the lease amortisation table at the implicit rate.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Finance lease: substantially all risks and rewards transfer.', 'Excludes land, natural resources, licences.',
                             'Lessee finance lease: lower of FV and PV of MLP; constant rate on liability; depreciate.', 'Operating lease: straight-line expense / income.',
                             'Lessor finance lease: receivable = net investment; constant return.', 'Sale and leaseback: finance → defer excess; operating at FV → recognise.'],
                 'remember': ['Lessee MLP include lessee-guaranteed residual value.'],
                 'traps': ['Rent-free periods are averaged, not ignored.']},
                [('Finance lease', 'Risks and rewards pass'), ('Lessee initial', 'Lower of FV and PV of MLP'), ('Operating lease', 'Straight-line')],
                viva, cases)
