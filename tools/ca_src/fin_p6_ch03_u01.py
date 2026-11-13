"""CA Final · Paper 6 · Integrated Business Solutions · Chapter 3 (Case Studies Published in Students' Journal themes).
Original multidisciplinary case material modelled on the ICAI IBS format; all names, businesses and figures are invented and machine-checked."""
from fkit import *

UID = 'fin-p6-ch03-u01'
T1 = 'Strategy in regulated, R&D-led industries'
T2 = 'Accounting for research, development and intangibles'
T3 = 'International expansion and transfer pricing'
T4 = 'CSR, sustainability and ethical leadership'


def build():
    ck = Checks()
    avg = ck.add('(84+96+120)/3', 'Average net profit of the three preceding years (₹ crore)')
    csr = ck.add('(84+96+120)/3*0.02', 'Minimum CSR spend at 2% of average net profit (₹ crore)')
    uns = ck.add('(84+96+120)/3*0.02-1.4', 'Unspent amount (₹ crore)')
    i1 = {'id': 'i1', 'title': 'CSR obligation of Calyx Pharma', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Calyx Pharmaceuticals Ltd. had net profits (computed under section 198) of ₹84 crore, ₹96 crore and ₹120 crore in the three preceding years and a turnover of ₹1,450 crore last year. It spent ₹1.4 crore on CSR this year, all on a hospital project that will run for two more years. Compute the CSR obligation and explain the treatment of the shortfall.',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Applicability', 'Turnover above ₹1,000 crore (also profit above ₹5 crore)', 'Applies'],
              ['Average net profit', '(84 + 96 + 120) ÷ 3', inr(avg)],
              ['Minimum CSR spend', '2% of average', f'{csr:g}'],
              ['Unspent', 'Required − spent', f'{uns:g}']], title='Section 135'),
              p('As the shortfall relates to an ongoing project, it must be moved to an Unspent CSR Account within 30 days of the year-end and spent within the following three years; the board report must explain the reasons.')],
          'checks': list(ck)}

    c2 = Checks()
    adj = c2.add('(1200-1000)*10000', 'Transfer pricing adjustment: (ALP − actual price) × quantity (₹)')
    i2 = {'id': 'i2', 'title': 'Pricing exports to the Kenyan subsidiary', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Calyx sells 10,000 kg of an active pharmaceutical ingredient to its wholly owned subsidiary in Kenya at ₹1,000 per kg. Comparable sales of the same ingredient by Calyx to unrelated buyers in similar markets and terms are at ₹1,200 per kg. Determine the arm\'s length adjustment and the method.',
          'solution': [table(['Point', 'Rule', 'Result'], [
              ['Relationship', 'Wholly owned subsidiary is an associated enterprise', 'International transaction'],
              ['Method', 'Comparable uncontrolled price, as reliable internal comparables exist', 'CUP'],
              ['Adjustment', '(₹1,200 − ₹1,000) × 10,000 kg', f'₹{inr(adj)} added to income']], title='Transfer pricing (sections 161–173, Income-tax Act, 2025)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Pharmaceutical, agrochemical and similar firms compete through R&D pipelines, patents, regulatory approvals and manufacturing quality. Strategy choices include innovator versus generic, contract manufacturing, in-licensing, and expansion into regulated or emerging markets.',
            'Porter\'s five forces explain profitability: buyer power (hospitals, governments), supplier power (API makers), threat of substitutes (generics after patent expiry), entry barriers (approvals, capital) and rivalry. Value chain analysis shows where cost or differentiation is created — R&D, quality, distribution.',
            'Leaders balance short-term profit with long-term investment, and must align growth with compliance, pricing regulation and patient safety.'],
          'Patents and approvals are the moat.',
          'Patent expiry invites generics and erodes margins quickly.'),
        C('c2', T2, [
            'Under Ind AS 38, research expenditure is expensed. Development cost is capitalised only when the entity can show technical feasibility, intention to complete, ability to use or sell, probable future economic benefits, adequate resources, and reliable measurement of expenditure.',
            'Acquired patents and licences are recognised at cost; intangibles with finite lives are amortised, those with indefinite lives are tested for impairment annually under Ind AS 36. Internally generated brands and customer lists are never capitalised.',
            'Auditors focus on capitalisation judgements and impairment of development assets, often reporting them as key audit matters under SA 701 for listed companies.'],
          'Research is expense; development may be an asset.',
          'Clinical trial costs before feasibility is shown are expensed.'),
        C('c3', T3, [
            'Entering markets such as Africa raises questions of entry mode (export, distributor, subsidiary, joint venture), regulatory registration, currency and payment risk, and FEMA rules on overseas investment.',
            'Transactions with associated enterprises abroad are international transactions; income is computed using the arm\'s length price determined under section 165 of the Income-tax Act, 2025 by the most appropriate method — CUP, resale price, cost plus, profit split, TNMM or another prescribed method.',
            'Under-pricing exports to a subsidiary shifts profit abroad and invites adjustment; documentation and benchmarking protect the company. Treasury hedges currency exposure on receivables.'],
          'Price group transactions as if between strangers.',
          'Charging a subsidiary less than unrelated buyers leads to an upward adjustment in India.'),
        C('c4', T4, [
            'Section 135 applies to a company with net worth of ₹500 crore or more, turnover of ₹1,000 crore or more, or net profit of ₹5 crore or more in the preceding year. It must spend at least 2% of average net profits of the three preceding years on Schedule VII activities through its CSR policy.',
            'An unspent amount linked to an ongoing project goes to an Unspent CSR Account within 30 days of year-end and is spent within three years; other unspent amounts go to a Schedule VII fund within six months of year-end.',
            'Large listed companies report ESG performance through the Business Responsibility and Sustainability Report. Ethical leadership covers fair pricing of essential medicines, transparent clinical data and protecting whistle-blowers.'],
          'Doing good is also a compliance duty.',
          'A company with ₹1,450 crore turnover must comply even if profits dip.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Africa entry paper', 'role': 'Head of international business',
             'situation': 'The board asks whether to export through distributors or set up a subsidiary.',
             'steps': ['Compare entry modes on control and risk.', 'Model returns and currency exposure.', 'Plan transfer pricing and FEMA compliance.', 'Recommend with phased milestones.'],
             'takeaway': 'Entry mode decides both control and compliance load.'}]

    mcqs = [
        Q('m1', 'Under Ind AS 38, expenditure in the research phase is:', ['Expensed when incurred', 'Capitalised always', 'Capitalised if probable', 'Deferred for five years'], 0,
          'Research phase. In practice: expense.', 'c2', T2),
        Q('m2', 'Development cost may be capitalised only when, among others, the entity shows:', ['Technical feasibility of completion', 'Any expected benefit', 'Board approval only', 'Patent filing'], 0,
          'Six criteria. In practice: evidence needed.', 'c2', T2),
        Q('m3', 'Threat of generics after patent expiry is, in five forces terms:', ['Threat of substitutes', 'Supplier power', 'Buyer power', 'Entry barrier'], 0,
          'Substitutes. In practice: price erosion.', 'c1', T1),
        Q('m4', 'CSR applies if net profit in the preceding year is at least:', ['Five crore rupees', 'One crore rupees', 'Ten crore rupees', 'Fifty crore rupees'], 0,
          'Section 135(1). In practice: or net worth/turnover.', 'c4', T4),
        Q('m5', 'Minimum CSR spend is:', ['Two percent of average net profit of three preceding years', 'Two percent of turnover', 'Five percent of profit', 'One percent of net worth'], 0,
          'Section 135(5). In practice: Schedule VII.', 'c4', T4),
        Q('m6', 'Unspent CSR money for an ongoing project goes to the Unspent CSR Account within:', ['Thirty days of year-end', 'Six months', 'One year', 'Ninety days'], 0,
          'Section 135(6). In practice: spend in 3 years.', 'c4', T4),
        Q('m7', 'Arm\'s length price for international transactions is determined under which section of the Income-tax Act, 2025?', ['Section 165', 'Section 92C', 'Section 135', 'Section 188'], 0,
          'New Act numbering. In practice: most appropriate method.', 'c3', T3),
        Q('m8', 'Where reliable prices of the same goods sold to unrelated parties exist, the preferred method is usually:', ['Comparable uncontrolled price', 'Profit split', 'TNMM', 'Cost plus'], 0,
          'Direct comparison. In practice: internal CUP.', 'c3', T3),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Applicability', 1, 'analysis', 'turnover'), S('s2', 'Obligation', 3, 'computation', '2%', nums=[avg, csr, uns]), S('s3', 'Treatment of unspent', 2, 'analysis', 'unspent')],
          ['State timeline.'], ['Using current year profit.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'AE and method', 2, 'analysis', 'CUP'), S('s2', 'Adjustment', 3, 'computation', 'adjustment', nums=[adj])],
          ['Explain method choice.'], ['Reducing income instead.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Can internally generated brands be capitalised?', 'Ind AS 38 prohibits recognising internally generated brands, so they stay off the balance sheet.',
          [P('p1', 'Prohibits', 5, 'prohibits'), P('p2', 'Brands', 5, 'brands')], 'c2'),
        V('v2', 'Why do auditors flag development cost capitalisation?', 'Because it involves significant judgement on feasibility and future benefits, making it a key audit matter.',
          [P('p1', 'Judgement', 5, 'judgement'), P('p2', 'Key audit matter', 5, 'key audit matter')], 'c2'),
        V('v3', 'What entry modes are available for a new foreign market?', 'Exporting, distributors, licensing, joint ventures and wholly owned subsidiaries.',
          [P('p1', 'Joint ventures', 5, 'joint venture'), P('p2', 'Subsidiaries', 5, 'subsidiar')], 'c3'),
        V('v4', 'What is BRSR?', 'The Business Responsibility and Sustainability Report through which large listed companies disclose ESG performance.',
          [P('p1', 'ESG', 5, 'esg'), P('p2', 'Listed', 5, 'listed')], 'c4'),
        V('v5', 'What happens to unspent CSR money not linked to an ongoing project?', 'It is transferred to a Schedule VII fund within six months of year-end.',
          [P('p1', 'Schedule VII fund', 5, 'schedule vii fund'), P('p2', 'Six months', 5, 'six months')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Calyx Pharmaceuticals — integrated case', 'difficulty': 'moderate',
              'case': 'Calyx Pharmaceuticals Ltd., a listed company, spent ₹60 crore this year on a new diabetes molecule: ₹22 crore on early laboratory research and ₹38 crore on late-stage development after the molecule cleared feasibility tests, with funds committed to finish it. Its key patent on a blockbuster drug expires next year. Calyx also sells to its Kenyan subsidiary below prices charged to unrelated distributors.',
              'mcqs': [
                  M('k1a', 'Amount eligible for capitalisation (₹ crore):', ['38', '60', '22', 'Nil'], 0,
                    'Development after feasibility. In practice: Ind AS 38.', 'moderate', check=38, topic=T2),
                  M('k1b', 'The patent expiry mainly increases:', ['Threat of substitutes from generics', 'Supplier power', 'Entry barriers', 'Buyer switching costs'], 0,
                    'Generic entry. In practice: plan pipeline.', 'moderate', topic=T1),
                  M('k1c', 'Sales to the Kenyan subsidiary must be tested at:', ['Arm\'s length price', 'Cost', 'Any agreed price', 'Market value in Kenya only'], 0,
                    'Sections 161–173. In practice: documentation.', 'moderate', topic=T3),
                  M('k1d', 'Development capitalisation judgement may be reported by the auditor as a:', ['Key audit matter', 'Qualification by default', 'Emphasis of matter always', 'Fraud report'], 0,
                    'SA 701. In practice: listed entity.', 'moderate', topic=T2),
              ]}]

    return unit(UID, 'p6', 'fin-p6-ch03', 1, 'Case Studies Published in Students\' Journal',
                ['Analyse strategy in R&D-led regulated industries.',
                 'Apply Ind AS 38 to research and development spending.',
                 'Evaluate international expansion and transfer pricing.',
                 'Apply CSR rules and ethical leadership principles.'],
                {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 40}, 'prereq': ['fin-p6-ch02-u01'],
                 'exam_tip': 'Separate research from development by the feasibility date before computing any capitalised amount.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Five forces and patents shape pharma strategy.', 'Ind AS 38: research expensed; development on six criteria.', 'Transfer pricing: ALP under section 165, Income-tax Act 2025.',
                             'CSR: ₹500 crore NW / ₹1,000 crore turnover / ₹5 crore profit; 2% of average.', 'Unspent: 30 days to Unspent CSR Account, or 6 months to fund.'],
                 'remember': ['Internally generated brands are never capitalised.'],
                 'traps': ['Using current year profit for CSR.']},
                [('Strategy', 'Five forces'), ('Intangibles', 'Ind AS 38'), ('Transfer pricing', 'Section 165'), ('CSR', 'Section 135'), ('Audit', 'SA 701')],
                viva, cases)
