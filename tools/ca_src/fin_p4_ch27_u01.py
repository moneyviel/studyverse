"""CA Final · Paper 4 · Chapter 27 Overview of Model Tax Conventions.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch27-u01'
T1 = 'OECD, UN and US Models'
T2 = 'Persons covered and residence'
T3 = 'Permanent establishment and business profits'
T4 = 'Distributive rules for specific income'


def build():
    ck = Checks()
    d = ck.add('8', 'Duration of construction project (months)')
    s = ck.add('45+60+50+45', 'Days of service presence in a 12-month period')
    i1 = {'id': 'i1', 'title': 'PE under OECD and UN Models', 'difficulty': 'moderate', 'minutes': 7,
          'q': '(a) A foreign contractor runs a construction project in India lasting 8 months. (b) A foreign consultancy sends staff who are present in India for 45, 60, 50 and 45 days across four visits within a twelve-month period (no fixed place used). Does a PE arise under the OECD and UN Models?',
          'solution': [table(['Case', 'OECD Model', 'UN Model'], [
              ['(a) Construction', f'{d} months — not above 12 months: no PE', 'More than 6 months: PE'],
              ['(b) Services', 'No service PE article: test fixed place', f'{s} days exceed 183 in 12 months: service PE']], title='Article 5')],
          'checks': list(ck)}

    c2 = Checks()
    n = c2.add('4', 'Number of tie-breaker tests for individuals')
    i2 = {'id': 'i2', 'title': 'Dual-resident individual', 'difficulty': 'core', 'minutes': 5,
          'q': 'Arjun is resident of both India and Country X under their domestic laws. He has a permanent home in both, but his family, business and social ties are in Country X. Apply the tie-breaker rule.',
          'solution': [table(['Test', 'Facts', 'Result'], [
              ['1. Permanent home', 'Available in both', 'Move to next test'],
              ['2. Centre of vital interests', 'Family and business ties in X', 'Resident of Country X'],
              ['3. Habitual abode', 'Not needed', '—'],
              [f'4. Nationality, then mutual agreement (total {n} tests)', 'Not needed', '—']], title='Article 4(2)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'The OECD Model began with a 1963 draft, was substantially revised in 1977 and is updated periodically (latest 2025). It favours residence-state taxation and is used mainly between developed countries.',
            'The UN Model, finalised in 1980 and updated in 2001, 2011, 2017, 2021 and 2025, gives greater taxing rights to source (often developing) countries — for example, wider PE definitions, a service PE, and articles on fees for services and automated digital services. The US Model reflects US treaty policy.',
            'Both Models have seven chapters (OECD 32 articles, UN 31) with broadly similar numbering (scope, definitions, taxation of income, methods for elimination of double taxation, special provisions); their Commentaries are key interpretive aids.'],
          'OECD leans to residence; UN protects source.',
          'India\'s treaties often borrow UN-style service PE clauses.'),
        C('c2', T2, [
            'Article 1 covers persons resident of one or both states; provisions deal with fiscally transparent entities and a saving clause preserving a state\'s right to tax its own residents. The UN Model 2025 adds a rule requiring source-state relief only where the residence state actually taxes, to address double non-taxation.',
            'Article 2 lists taxes covered (taxes on income and capital). Article 3 defines terms; undefined terms take domestic meaning unless context requires otherwise (Article 3(2)).',
            'Article 4 defines a resident as a person liable to tax by reason of domicile, residence, place of management or similar criteria. Dual-resident individuals are resolved by tie-breakers in order: permanent home, centre of vital interests, habitual abode, nationality, and finally mutual agreement. For non-individuals, the current Models leave residence to competent authorities by mutual agreement.'],
          'Residence decides treaty access; tie-breakers decide which state.',
          'Family ties abroad can make an Indian dual resident a resident of the other state.'),
        C('c3', T3, [
            'Article 5 defines a permanent establishment: a fixed place of business (office, branch, factory, mine), construction sites lasting over 12 months (OECD) or over 6 months (UN), and dependent agents who habitually conclude or play the principal role in concluding contracts. Preparatory or auxiliary activities are excluded, subject to anti-fragmentation rules.',
            'The UN Model adds a service PE where services are furnished through employees for more than 183 days in any twelve-month period, and includes agents maintaining stock for delivery; the insurance PE clause was removed in 2025 in favour of a separate insurance premiums article.',
            'Article 7 allows the source state to tax business profits only if attributable to a PE; the UN Model contains a limited force-of-attraction rule covering sales and activities similar to those through the PE.'],
          'No PE, no source tax on business profits.',
          'An 8-month construction project is a PE under the UN Model but not the OECD Model.'),
        C('c4', T4, [
            'Article 8 gives international shipping and air transport profits to the residence state (with UN alternatives for shipping). Articles 10, 11 and 12 allow source taxation of dividends, interest and royalties at capped rates (OECD gives royalties exclusively to residence).',
            'UN-specific articles: 12AA (fees for services, replacing the former 12A on technical services and Article 14 in 2025), 12B (income from automated digital services, added in 2021, taxable on a gross or net basis at the taxpayer\'s option), and 12C (insurance premiums).',
            'Article 13 covers capital gains, including gains from shares deriving value from immovable property (tested over 365 days). Articles 15 to 21 cover employment, directors\' fees, entertainers and sportspersons, pensions, government service, students and other income; Articles 23–27 deal with elimination of double taxation, non-discrimination, MAP, exchange of information and assistance in collection.'],
          'Distributive rules allocate each income type.',
          'Fees for services from India to a UN-model treaty partner may be taxed in India under Article 12AA.'),
    ]

    jobs = [{'id': 'j1', 'title': 'PE exposure check', 'role': 'International tax analyst',
             'situation': 'A foreign engineering firm plans a 10-month project in India.',
             'steps': ['Identify which Model the treaty follows.', 'Compute project and service days.', 'Assess agent activities.', 'Attribute profits if a PE exists.'],
             'takeaway': 'Treaty wording, not the Model, finally decides.'}]

    mcqs = [
        Q('m1', 'The UN Model generally favours:', ['Source-state taxation', 'Residence-state taxation', 'No taxation', 'Third-state taxation'], 0,
          'Developing countries. In practice: wider PE.', 'c1', T1),
        Q('m2', 'The OECD Model was first published as a draft in:', ['1963', '1977', '1980', '2017'], 0,
          'History. In practice: updated periodically.', 'c1', T1, check=1963),
        Q('m3', 'The first tie-breaker test for dual-resident individuals is:', ['Permanent home', 'Nationality', 'Habitual abode', 'Centre of vital interests'], 0,
          'Article 4(2). In practice: sequential.', 'c2', T2),
        Q('m4', 'Under the OECD Model, a construction site is a PE if it lasts more than:', ['Twelve months', 'Six months', 'Ninety days', 'One hundred eighty-three days'], 0,
          'Article 5(3). In practice: UN six months.', 'c3', T3),
        Q('m5', 'A service PE under the UN Model requires presence exceeding:', ['One hundred eighty-three days in twelve months', 'Ninety days', 'Thirty days', 'Twelve months'], 0,
          'Article 5(3)(b). In practice: aggregate visits.', 'c3', T3),
        Q('m6', 'Income from automated digital services is covered by UN Model Article:', ['Article twelve B', 'Article twelve A', 'Article twelve C', 'Article seven'], 0,
          'Added in 2021. In practice: no OECD equivalent.', 'c4', T4),
        Q('m7', 'In the 2025 UN Model, former Article 12A and Article 14 were replaced by:', ['Article 12AA — fees for services', 'Article 12B', 'Article 15', 'Article 7'], 0,
          'Broader services article. In practice: check treaty text.', 'c4', T4),
        Q('m8', 'Limited force of attraction appears in:', ['The UN Model\'s business profits article', 'The OECD Model', 'Article 4', 'Article 13'], 0,
          'Article 7 UN. In practice: similar sales attributed.', 'c3', T3),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Construction PE', 3, 'analysis', 'months', nums=[d]), S('s2', 'Service PE', 3, 'analysis', '183', nums=[s])],
          ['Compare Models.'], ['Using OECD thresholds for UN treaties.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Order of tests', 2, 'analysis', 'permanent home', nums=[n]), S('s2', 'Conclusion', 2, 'judgement', 'vital interests')],
          ['Stop at the first decisive test.'], ['Jumping to nationality.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Why does the UN Model widen the PE definition?', 'To preserve taxing rights of source countries, typically developing countries.',
          [P('p1', 'Source countries', 5, 'source'), P('p2', 'Developing', 5, 'developing')], 'c1'),
        V('v2', 'How is dual residence of a company resolved under current Models?', 'By mutual agreement between competent authorities, considering place of effective management and other factors.',
          [P('p1', 'Mutual agreement', 5, 'mutual agreement'), P('p2', 'Competent authorities', 5, 'competent')], 'c2'),
        V('v3', 'What is a dependent agent PE?', 'An agent who habitually concludes contracts or plays the principal role in concluding them for the enterprise.',
          [P('p1', 'Habitually', 5, 'habitually'), P('p2', 'Principal role', 5, 'principal role')], 'c3'),
        V('v4', 'How may Article 12B income be taxed?', 'On a gross basis at a capped rate, or on a net basis at the taxpayer\'s option.',
          [P('p1', 'Gross basis', 5, 'gross'), P('p2', 'Net basis', 5, 'net')], 'c4'),
        V('v5', 'What does Article 3(2) provide?', 'Undefined terms take their domestic-law meaning unless the context requires otherwise.',
          [P('p1', 'Domestic law', 5, 'domestic'), P('p2', 'Context', 5, 'context')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Aurora Engineering GmbH', 'difficulty': 'core',
              'case': 'Aurora Engineering GmbH installs equipment at an Indian plant over 7 months. The relevant treaty follows the UN Model for PE (construction threshold six months).',
              'mcqs': [
                  M('k1a', 'Does Aurora have a PE under the treaty?', ['Yes, the project exceeds six months', 'No', 'Only if it has an office', 'Only after twelve months'], 0,
                    'UN threshold. In practice: count from start.', 'core', topic=T3),
                  M('k1b', 'Months by which the project exceeds the threshold:', ['1', '5', '7', '6'], 0,
                    '7 − 6. In practice: any excess suffices.', 'core', check=1, topic=T3),
                  M('k1c', 'Under an OECD-style clause, would a PE arise?', ['No, twelve months is not exceeded', 'Yes', 'Only for services', 'Only with an agent'], 0,
                    'OECD threshold. In practice: treaty decides.', 'core', topic=T3),
                  M('k1d', 'Profits taxable in India are those:', ['Attributable to the PE', 'Worldwide profits of Aurora', 'Only royalties', 'Nil in all cases'], 0,
                    'Article 7. In practice: attribution rules.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch27', 1, 'Overview of Model Tax Conventions',
                ['Compare the OECD, UN and US Models.',
                 'Apply persons covered and residence tie-breakers.',
                 'Apply PE and business profits rules.',
                 'Identify distributive rules for specific income.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 15}, 'prereq': ['fin-p4-ch26-u01'],
                 'exam_tip': 'State which Model the clause follows before applying thresholds.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['OECD (1963/1977/2025) residence-oriented; UN (1980–2025) source-oriented.', 'Article 4 tie-breakers: home, vital interests, abode, nationality, MAP.', 'Article 5: 12 vs 6 months; UN service PE 183 days.',
                             'UN Articles 12AA, 12B, 12C.', 'Article 7 business profits; limited force of attraction (UN).'],
                 'remember': ['Article 12A was replaced by 12AA in the 2025 UN Model.'],
                 'traps': ['Applying a service PE under an OECD-style treaty.']},
                [('Residence', 'Article 4'), ('PE', 'Article 5'), ('Business profits', 'Article 7'), ('Fees for services', 'UN Article 12AA'), ('ADS', 'UN Article 12B')],
                viva, cases)
