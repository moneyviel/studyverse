"""CA Final · Paper 1 Financial Reporting · Chapter 5 Unit 5 Ind AS 38 Intangible Assets.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch05-u05'
T1 = 'Definition: identifiability, control and future benefits'
T2 = 'Acquired intangibles: separately and in business combinations'
T3 = 'Internally generated intangibles: research and development'
T4 = 'Measurement after recognition, useful life and amortisation'


def build():
    ck = Checks()
    exp = ck.add('40+20', 'Expensed (₹ lakh): research + development before criteria met')
    cap = ck.add('70', 'Capitalised development cost (₹ lakh)')
    am = ck.add('70/5*6/12', 'Amortisation for the first year of use (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'A new drug formulation', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Nova Pharma spends ₹40 lakh on research (April–July). On 1 August all six development criteria are first met. Development costs are ₹20 lakh in July and ₹70 lakh from August to March. The formulation is available for use on 1 October of the next year (expected life 5 years, straight-line). How much is expensed and capitalised in the first year, and what is the amortisation for the following year?',
          'solution': [table(['Item', 'Treatment', '₹ lakh'], [
              ['Research costs', 'Expense', inr(40)],
              ['Development before criteria met (July)', 'Expense — not reinstated later', inr(20)],
              ['Total expensed', '', inr(exp)],
              ['Development after criteria met', 'Capitalise as intangible asset under development', inr(cap)],
              ['Amortisation next year (6 months from 1 October)', '70 ÷ 5 × 6/12', inr(am)]], title='Ind AS 38 — R&D')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Recognise or not?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Decide recognition: (a) a customer list bought from a competitor for ₹5 crore; (b) the company\'s own brand built through years of advertising; (c) a 3-year software licence purchased; (d) ₹2 crore spent training sales staff; (e) a customer relationship of an acquired subsidiary, valued at ₹8 crore in a business combination; (f) costs of launching a new product line.',
          'solution': [table(['Item', 'Recognise?', 'Reason'], [
              ['(a)', 'Yes', 'Separately acquired; price reflects expected benefits'],
              ['(b)', 'No', 'Internally generated brands cannot be recognised'],
              ['(c)', 'Yes', 'Acquired right with reliable cost; amortise over 3 years'],
              ['(d)', 'No', 'Training costs are expensed'],
              ['(e)', 'Yes', 'Identifiable intangible acquired in a business combination at fair value, separate from goodwill'],
              ['(f)', 'No', 'Start-up and launch costs are expensed']], title='Recognition')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Ind AS 38 treats as an intangible asset any non-monetary resource that has no physical form yet can be identified. Identifiable means either separable (can be sold, licensed, rented or exchanged) or arising from contractual or other legal rights.',
            'Control is the power to obtain the benefits and restrict others\' access — usually through legal rights. Skilled staff, market share or customer loyalty without contracts usually lack control.',
            'Future economic benefits include revenues and cost savings. Where an item has both tangible and intangible parts, judgement decides which dominates (e.g. software integral to a machine is PPE).'],
          'Intangibles are rights you can point to and protect — not general goodwill or talent.',
          'A trained workforce is valuable but not an asset, as employees can leave.'),
        C('c2', T2, [
            'Recognition requires probable future benefits and reliably measurable cost. For separately acquired intangibles, both are presumed met; cost is purchase price plus non-refundable taxes and directly attributable costs (professional fees, testing), excluding introduction costs, advertising and administrative overheads.',
            'In a business combination, intangibles are recognised at fair value separately from goodwill if identifiable — even if the acquiree had not recognised them (e.g. customer relationships, brands, in-process R&D).',
            'Acquisition by Government grant may be at fair value or nominal amount plus directly attributable costs; exchanges follow fair value unless commercial substance is lacking.'],
          'Buying an intangible proves its value; building one internally needs stricter tests.',
          'An acquired brand appears in consolidated accounts even though the target never showed it.'),
        C('c3', T3, [
            'Internally generated goodwill is never recognised. Internally generated brands, mastheads, publishing titles, customer lists and similar items are not recognised.',
            'For internal projects, research phase spending is expensed. Development spending is capitalised only when all of these are shown: technical feasibility of completion; intention to complete and use or sell; ability to use or sell; how the asset will generate probable future benefits (a market or internal usefulness); availability of technical, financial and other resources; and ability to measure the expenditure reliably.',
            'If research and development phases cannot be distinguished, all costs are treated as research. Costs expensed earlier are not reinstated later. Cost includes materials, services, employee costs and directly attributable overheads from the date criteria are met; it excludes selling, admin and training costs and initial operating losses.'],
          'Research is always expensed; development waits until success is demonstrable.',
          'Designing a prototype after feasibility is proven is development; exploring alternative materials is research.'),
        C('c4', T4, [
            'After recognition: cost model, or revaluation model only if fair value can be measured by reference to an active market (rare for intangibles). Revaluation follows principles like Ind AS 16.',
            'Useful life is finite (amortised systematically from availability for use, over the shorter of economic and legal life) or indefinite (no foreseeable limit to cash flows; not amortised, tested annually for impairment and reviewed each period). Residual value is normally zero unless there is a commitment or active market.',
            'Amortisation reflects the pattern of consumption; a revenue-based method is presumed inappropriate except where the asset is expressed as a measure of revenue or revenue and consumption are highly correlated. Life, method and residual value are reviewed at least each year end. Derecognition gains or losses go to profit or loss.'],
          'Finite lives are amortised; indefinite lives are tested for impairment instead.',
          'A broadcasting licence renewable at little cost may have an indefinite life.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Capitalising software development', 'role': 'Audit senior',
             'situation': 'A tech company capitalised all salaries of its developers for the year.',
             'steps': ['Identify the date each project met all six criteria.', 'Expense costs before that date and research costs.', 'Exclude admin, training and marketing.', 'Check amortisation start and impairment of incomplete projects.'],
             'takeaway': 'The capitalisation start date is the heart of an R&D review.'}]

    mcqs = [
        Q('m1', 'An asset is identifiable if it:', ['Is separable or arises from contractual or legal rights', 'Has physical form', 'Has a market price', 'Is internally generated'], 0,
          'Either test is enough. In practice: licences arise from legal rights.', 'c1', T1),
        Q('m2', 'Internally generated brands are:', ['Not recognised as assets', 'Recognised at fair value', 'Recognised at cost', 'Capitalised if valuable'], 0,
          'Costs cannot be distinguished from developing the business as a whole. In practice: acquired brands are recognised.', 'c3', T3),
        Q('m3', 'Research phase expenditure is:', ['Expensed when incurred', 'Capitalised', 'Capitalised after feasibility', 'Deferred'], 0,
          'No asset can be shown to exist in research. In practice: track phases separately.', 'c3', T3),
        Q('m4', 'Development costs expensed in earlier periods can later be:', ['Not reinstated as an asset', 'Reinstated once criteria are met', 'Reinstated with auditor approval', 'Transferred to goodwill'], 0,
          'Ind AS 38 prohibits reinstatement. In practice: capitalise from the criteria date only.', 'c3', T3),
        Q('m5', 'An intangible with an indefinite useful life is:', ['Not amortised but tested for impairment annually', 'Amortised over 10 years', 'Amortised over 20 years', 'Expensed immediately'], 0,
          'Indefinite does not mean infinite; life is reviewed each period. In practice: change to finite is an estimate change.', 'c4', T4),
        Q('m6', 'The revaluation model for intangibles requires:', ['An active market', 'Management valuation', 'Auditor consent', 'A business combination'], 0,
          'Without an active market, the cost model applies. In practice: taxi licences may have one.', 'c4', T4),
        Q('m7', 'Customer relationships of an acquired company are recognised in consolidation:', ['At fair value, separately from goodwill, if identifiable', 'Never', 'Only if the acquiree recognised them', 'At nil'], 0,
          'Business combination accounting captures identifiable intangibles. In practice: valuation experts are used.', 'c2', T2),
        Q('m8', 'Revenue-based amortisation is:', ['Presumed inappropriate, rebuttable in limited cases', 'Always required', 'Always allowed', 'Required for software'], 0,
          'Revenue reflects more than consumption of the asset. In practice: allowed when the right is expressed as a revenue cap.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Expensed', 2, 'computation', 'expense', nums=[exp]), S('s2', 'Capitalised', 1.5, 'computation', 'capitalise', nums=[cap]), S('s3', 'Amortisation', 1.5, 'computation', 'amortisation', nums=[am])],
          ['Use the criteria date.'], ['Reinstating July costs.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Acquired items', 2, 'concept', 'acquired'), S('s2', 'Internal brand', 1, 'concept', 'internally'), S('s3', 'Expenses', 2, 'concept', 'expensed|training|start-up'), S('s4', 'Combination', 1, 'concept', 'combination')],
          ['Give a reason for each.'], ['Recognising the own brand.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Define an intangible asset.', 'A non-monetary resource with no physical form that is identifiable, controlled by the entity and expected to yield future economic benefits.',
          [P('p1', 'Identifiable non-monetary', 5, 'identifiable|non-monetary'), P('p2', 'Control and benefits', 5, 'control|benefit')], 'c1'),
        V('v2', 'List the development-phase criteria.', 'Technical feasibility, intention to complete, ability to use or sell, probable benefits, availability of resources, and reliable measurement of cost.',
          [P('p1', 'Feasibility and intention', 5, 'feasib|intention'), P('p2', 'Resources and measurement', 5, 'resource|measur')], 'c3'),
        V('v3', 'Why is internally generated goodwill not recognised?', 'Goodwill built internally fails the identifiability test, and its cost cannot be measured reliably.',
          [P('p1', 'Identifiability fails', 5, 'identifiab'), P('p2', 'Cost reliability', 5, 'reliab|cost')], 'c3'),
        V('v4', 'How is an indefinite-life intangible treated?', 'It is not amortised; it is tested for impairment every year and its life assessment is reviewed each period.',
          [P('p1', 'Annual impairment test', 6, 'impairment'), P('p2', 'Life reviewed', 4, 'review')], 'c4'),
        V('v5', 'What is the effect of failing to separate research from development?', 'All the expenditure is treated as research and expensed.',
          [P('p1', 'Treated as research', 6, 'research'), P('p2', 'Expensed', 4, 'expens')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'PixelSoft Ltd.', 'difficulty': 'moderate',
              'case': 'PixelSoft Ltd. develops a game engine. Feasibility was proven on 1 September; costs before that were ₹1.2 crore, and after, ₹3 crore including ₹20 lakh of marketing launch expenses. It also bought a 10-year music licence for ₹50 lakh and a domain name renewable indefinitely at minimal cost.',
              'mcqs': [
                  M('k1a', 'Amount capitalised for the game engine (₹ crore):', ['2.8', '3.0', '4.2', '1.2'], 0,
                    'Post-criteria costs of 3.0 less marketing 0.2 = 2.8. In practice: pre-September costs are expensed.', 'moderate', check=2.8, topic=T3),
                  M('k1b', 'The ₹1.2 crore spent before 1 September is:', ['Expensed', 'Capitalised retrospectively', 'Deferred', 'Goodwill'], 0,
                    'Costs before criteria are met are expensed and never reinstated. In practice: keep project logs.', 'core', topic=T3),
                  M('k1c', 'Annual amortisation of the music licence (₹ lakh):', ['5', '50', '10', 'Nil'], 0,
                    '50 ÷ 10 = 5, over its legal life. In practice: start when available for use.', 'core', check=5, topic=T4),
                  M('k1d', 'The domain name renewable indefinitely at minimal cost may be:', ['An indefinite-life intangible tested annually for impairment', 'Amortised over 1 year', 'Expensed', 'Inventory'], 0,
                    'No foreseeable limit to its cash flows if renewals are expected. In practice: review each year.', 'moderate', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch05', 5, 'Ind AS 38 "Intangible Assets"',
                ['Apply the definition and recognition criteria for intangibles.',
                 'Measure separately acquired and combination-acquired intangibles.',
                 'Distinguish research and development and apply capitalisation criteria.',
                 'Apply cost/revaluation models, useful lives and amortisation.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 30}, 'prereq': ['fin-p1-ch05-u04'],
                 'exam_tip': 'For R&D questions, find the date all six criteria are met — costs before it are expensed forever.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Identifiable (separable or legal), controlled, future benefits.',
                             'Acquired: cost or fair value in a combination.',
                             'Research → expense; development → capitalise after six criteria.',
                             'No internally generated goodwill, brands, customer lists.',
                             'Finite: amortise; indefinite: annual impairment test.'],
                 'remember': ['Revaluation only with active market.'],
                 'traps': ['Expensed development costs are never reinstated.']},
                [('Identifiable', 'Separable or legal rights'), ('Research', 'Expense'), ('Development', 'Capitalise if 6 criteria'), ('Indefinite life', 'No amortisation; test annually')],
                viva, cases)
