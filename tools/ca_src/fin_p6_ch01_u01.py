"""CA Final · Paper 6 · Integrated Business Solutions · Chapter 1 (Case Study Digest themes).
Original multidisciplinary case material modelled on the ICAI IBS format; all names, businesses and figures are invented and machine-checked."""
from fkit import *

UID = 'fin-p6-ch01-u01'
T1 = 'Reading an integrated case study'
T2 = 'Strategy toolkit: business models and growth paths'
T3 = 'Linking strategy to financial decisions'
T4 = 'Compliance lens: reporting, tax, law and audit'


def build():
    ck = Checks()
    cost = ck.add('200*12', 'Capital outlay for 200 EVs at ₹12 lakh each (₹ lakh)')
    pvin = ck.add('200*3.6*3.6048', 'PV of annual inflows: 200 × ₹3.6 lakh × annuity factor 3.6048 (₹ lakh)')
    pvs = ck.add('200*2*0.5674', 'PV of salvage: 200 × ₹2 lakh × 0.5674 (₹ lakh)')
    npv = ck.add('200*3.6*3.6048+200*2*0.5674-200*12', 'NPV of the expansion (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Should Velora add 200 EVs?', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Velora Mobility Ltd. runs an app-based cab platform and plans to own 200 electric cars (₹12 lakh each) for its premium segment. Each car is expected to give post-tax net cash inflow of ₹3.6 lakh a year for 5 years and a salvage of ₹2 lakh at the end. Cost of capital is 12% (5-year annuity factor 3.6048; year-5 discount factor 0.5674). Evaluate the proposal.',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Outlay', '200 × 12', inr(cost)],
              ['PV of inflows', '200 × 3.6 × 3.6048', f'{pvin:,.2f}'],
              ['PV of salvage', '200 × 2 × 0.5674', f'{pvs:,.2f}'],
              ['NPV', 'PV of inflows + salvage − outlay', f'{npv:,.2f}']], title='Capital budgeting'),
              p('NPV is positive, so the fleet adds value. Strategically it moves Velora from a pure asset-light aggregator towards owning assets; the board should weigh higher fixed costs and battery-technology risk against better service control.')],
          'checks': list(ck)}

    c2 = Checks()
    ll = c2.add('50*3.1699', 'Lease liability: PV of 4 annual payments of ₹50 lakh at 10% (₹ lakh)')
    it = c2.add('50*3.1699*0.10', 'Year 1 interest at 10% (₹ lakh)')
    cl = c2.add('50*3.1699*1.10-50', 'Closing lease liability after year 1 (₹ lakh)')
    dep = c2.add('50*3.1699/4', 'Straight-line depreciation of right-of-use asset (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Charging depot lease under Ind AS 116', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Velora leases a charging depot for 4 years at ₹50 lakh per year payable at year-end. Its incremental borrowing rate is 10% (4-year annuity factor 3.1699). No initial direct costs. Compute the initial lease liability, year-1 interest, closing liability and depreciation of the right-of-use asset.',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Lease liability = ROU asset', '50 × 3.1699', f'{ll:,.3f}'],
              ['Year-1 interest', '10% of opening liability', f'{it:,.3f}'],
              ['Closing liability', 'Opening + interest − payment', f'{cl:,.3f}'],
              ['Depreciation', 'ROU asset ÷ 4', f'{dep:,.3f}']], title='Ind AS 116')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'An IBS case study presents a business with its vision, history, market, people, numbers and open problems, and asks multiple-choice and descriptive questions that draw on financial reporting, financial management, audit, direct tax, indirect tax, corporate laws and strategic management together.',
            'A reliable method: read the questions first; then read the case marking facts by discipline (strategy, numbers, compliance, governance); list the decision each question asks for; solve using the relevant provisions; and conclude with a recommendation in the role assigned (CFO, auditor, consultant).',
            'Marks come from correct identification of the issue, the right provision or tool, accurate computation and a clear, practical recommendation. Facts given in the case override general assumptions; state any assumption you add.'],
          'Think like the decision-maker, not the textbook.',
          'A question asking "advise the CFO" needs a recommendation, not only a computation.'),
        C('c2', T2, [
            'Business models describe how value is created and captured: aggregator or platform, subscription, freemium, on-demand, asset-light versus asset-heavy. Firm stages run from start-up to scale-up; a privately held start-up valued above US$1 billion is commonly called a unicorn.',
            'Growth paths follow the Ansoff matrix: market penetration, market development, product development and diversification (related or unrelated). Integration choices include horizontal (same stage) and vertical — backward towards suppliers or forward towards customers.',
            'Competitive position follows Porter\'s generic strategies (cost leadership, differentiation, focus). SWOT, PESTLE, five forces and value chain analysis frame the external and internal facts in the case.'],
          'Name the strategy, then judge its fit.',
          'A cab platform buying its own EV fleet is a form of backward integration into supply of vehicles.'),
        C('c3', T3, [
            'Strategic choices must pass financial tests: capital budgeting (NPV, IRR, payback), cost of capital, valuation, working capital and funding mix. A positive NPV supports a decision only when strategic and risk factors also fit.',
            'Risk tools — sensitivity, scenario analysis, real options and hedging — show how robust a decision is to key drivers such as utilisation, fuel or power costs, and interest rates.',
            'Funding choices affect control, gearing and cost: equity dilutes, debt raises financial risk, and leases move assets and liabilities on balance sheet under Ind AS 116.'],
          'Strategy proposes; numbers dispose.',
          'An NPV that turns negative at 10% lower utilisation signals high operating risk.'),
        C('c4', T4, [
            'Every strategic move carries reporting effects (Ind AS recognition and disclosure), tax effects (income-tax deductions, GST liability and credits), legal requirements (Companies Act approvals, SEBI rules, FEMA) and audit implications (risk of material misstatement, key audit matters).',
            'Example cross-links: an electronic commerce operator notified under section 9(5) of the CGST Act pays GST on passenger transport by motor cab booked through it; a company needs a special resolution to have more than 15 directors; a lessee recognises a right-of-use asset and lease liability under Ind AS 116.',
            'Ethics and governance run through all areas: independence of auditors, related party approvals, fair disclosure and whistle-blower mechanisms.'],
          'Each decision has a compliance shadow.',
          'Raising funds abroad brings FEMA, Companies Act and Ind AS issues together.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Board note on fleet ownership', 'role': 'Finance director',
             'situation': 'The board must decide between asset-light and owned-fleet models.',
             'steps': ['Summarise strategic rationale.', 'Present NPV and sensitivity.', 'Explain Ind AS and GST effects.', 'Recommend with conditions.'],
             'takeaway': 'Integrated advice wins board approval.'}]

    mcqs = [
        Q('m1', 'A platform that connects riders with independent drivers for a commission follows a:', ['Aggregator (platform) model', 'Subscription model', 'Freemium model', 'Asset-heavy manufacturing model'], 0,
          'Two-sided platform. In practice: commission revenue.', 'c2', T2),
        Q('m2', 'A cab aggregator acquiring a vehicle-leasing company is an example of:', ['Backward vertical integration', 'Forward vertical integration', 'Horizontal integration', 'Unrelated diversification'], 0,
          'Moves toward supply. In practice: control inputs.', 'c2', T2),
        Q('m3', 'Entering a new city with the existing service is, in Ansoff terms:', ['Market development', 'Product development', 'Diversification', 'Market penetration'], 0,
          'New market, same product. In practice: city launch.', 'c2', T2),
        Q('m4', 'GST on passenger transport by motor cab booked through a notified ECO is paid by:', ['The electronic commerce operator', 'The driver in every case', 'The rider under reverse charge', 'No one; it is exempt'], 0,
          'Section 9(5). In practice: ECO liable.', 'c4', T4),
        Q('m5', 'To have more than 15 directors, a company must pass:', ['A special resolution', 'An ordinary resolution', 'A board resolution only', 'No resolution; it is barred'], 0,
          'Section 149(1). In practice: articles too.', 'c4', T4),
        Q('m6', 'Under Ind AS 116, a lessee initially measures the lease liability at:', ['Present value of unpaid lease payments', 'Total undiscounted payments', 'Fair value of the asset', 'First year\'s rent'], 0,
          'Discounted at implicit rate or IBR. In practice: ROU asset too.', 'c4', T4),
        Q('m7', 'A project with positive NPV should be accepted when:', ['It also fits strategy and risk appetite', 'Always, regardless of risk', 'Only if payback is under one year', 'Only if IRR equals cost of capital'], 0,
          'Integrated view. In practice: sensitivity.', 'c3', T3),
        Q('m8', 'The first step in answering an integrated case study is to:', ['Read the questions to know what to look for', 'Start computing immediately', 'Memorise the case facts', 'Skip the descriptive questions'], 0,
          'Focused reading. In practice: saves time.', 'c1', T1),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Outlay and inflows', 3, 'computation', 'annuity', nums=[cost, pvin]), S('s2', 'Salvage and NPV', 3, 'computation', 'NPV', nums=[pvs, npv]), S('s3', 'Strategic comment', 2, 'analysis', 'asset')],
          ['Add a strategic view.'], ['Omitting salvage.'], ['Table and conclusion.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Initial liability', 2, 'computation', 'present value', nums=[ll]), S('s2', 'Interest and closing', 2, 'computation', 'interest', nums=[it, cl]), S('s3', 'Depreciation', 2, 'computation', 'right-of-use', nums=[dep])],
          ['Show both asset and liability.'], ['Expensing lease rent.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Why is an integrated approach needed in IBS cases?', 'Because a business decision affects strategy, finance, reporting, tax, law and audit together, so advice must combine them.',
          [P('p1', 'Strategy', 5, 'strategy'), P('p2', 'Tax', 5, 'tax')], 'c1'),
        V('v2', 'What is the difference between forward and backward integration?', 'Forward integration moves toward customers or distribution; backward integration moves toward suppliers or inputs.',
          [P('p1', 'Customers', 5, 'customers'), P('p2', 'Suppliers', 5, 'suppliers')], 'c2'),
        V('v3', 'How does Ind AS 116 change a lessee\'s balance sheet?', 'It brings a right-of-use asset and a lease liability onto the balance sheet for most leases.',
          [P('p1', 'Right-of-use', 5, 'right-of-use'), P('p2', 'Lease liability', 5, 'lease liability')], 'c4'),
        V('v4', 'What does sensitivity analysis show?', 'How much a key variable can change before the NPV turns negative.',
          [P('p1', 'Key variable', 5, 'key variable'), P('p2', 'NPV', 5, 'npv')], 'c3'),
        V('v5', 'What should a conclusion in a case answer include?', 'A clear recommendation in the assigned role, with conditions or risks attached.',
          [P('p1', 'Recommendation', 5, 'recommendation'), P('p2', 'Risks', 5, 'risks')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Velora Mobility — integrated case', 'difficulty': 'moderate',
              'case': 'Velora Mobility Ltd., founded six years ago, runs a ride-hailing app in 14 cities and was recently valued at US$1.3 billion in a private funding round. Drivers own their cars and pay Velora a commission per ride; Velora is a notified electronic commerce operator. To fund expansion, investors want three nominee directors, which would take the board from 14 to 17 members. Velora is also considering a two-wheeler taxi service in its existing cities.',
              'mcqs': [
                  M('k1a', 'Velora\'s funding valuation makes it a:', ['Unicorn', 'Start-up below scale', 'Listed incumbent', 'Micro enterprise'], 0,
                    'Above US$1 billion, privately held. In practice: growth stage.', 'moderate', topic=T2),
                  M('k1b', 'GST on rides booked through the app is payable by:', ['Velora as the ECO', 'Each driver', 'The rider', 'Nobody'], 0,
                    'Section 9(5). In practice: passenger transport by cab.', 'moderate', topic=T4),
                  M('k1c', 'To increase the board to 17 directors Velora needs:', ['A special resolution', 'An ordinary resolution', 'Central Government approval', 'Nothing more'], 0,
                    'Section 149(1). In practice: articles permitting.', 'moderate', topic=T4),
                  M('k1d', 'Launching two-wheeler taxis in existing cities is:', ['Product development', 'Market development', 'Unrelated diversification', 'Backward integration'], 0,
                    'New service, same market. In practice: Ansoff.', 'moderate', topic=T2),
              ]}]

    return unit(UID, 'p6', 'fin-p6-ch01', 1, 'IBS Case Study Digest',
                ['Apply a structured method to integrated case studies.',
                 'Identify business models and growth strategies.',
                 'Link strategic proposals to financial evaluation.',
                 'Spot reporting, tax, legal and audit consequences of decisions.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 40}, 'prereq': ['fin-p5-ii-ch08-u01'],
                 'exam_tip': 'For each question, name the discipline and provision first, then solve, then advise.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['IBS cases combine six areas with strategy.', 'Business models and Ansoff growth paths.', 'Integration: backward, forward, horizontal.',
                             'NPV supports strategy only with risk fit.', 'Ind AS 116, section 9(5) GST, section 149 board size.'],
                 'remember': ['Facts in the case override general assumptions.'],
                 'traps': ['Giving only computations without advice.']},
                [('Method', 'Read questions first'), ('Strategy', 'Ansoff, Porter'), ('Finance', 'NPV'), ('Reporting', 'Ind AS 116'), ('Tax/Law', 'Section 9(5); section 149')],
                viva, cases)
