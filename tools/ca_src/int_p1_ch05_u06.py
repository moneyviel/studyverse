"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 5 Unit 6 — AS 26 Intangible Assets.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch05-u06'
T1 = 'What an intangible asset is'
T2 = 'Recognition and initial measurement'
T3 = 'Internally generated intangibles: research and development'
T4 = 'Items always expensed'
T5 = 'Amortisation, impairment and retirement'


def build():
    ck = Checks()
    cap = ck.add('30', 'Development cost capitalised (₹ lakh)')
    exp = ck.add('12+18', 'Expensed: research + development before criteria met (₹ lakh)')
    am = ck.add('30/5*3/12', 'Amortisation for January–March (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'From research to a product', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Medha Pharma Ltd. (year ends 31 March 2027) spent ₹12 lakh on research in April–June 2026 and ₹18 lakh on development in July–September 2026. All recognition criteria for development were first met on 1 October 2026; it then spent ₹30 lakh to December. The product was available for use on 1 January 2027 with a useful life of 5 years. Show the treatment.',
          'solution': [table(['Item', 'Treatment', '₹ lakh'], [
              ['Research', 'Expense', R(12)],
              ['Development before criteria met', 'Expense (cannot be reinstated later)', R(18)],
              ['Total expensed', '', R(exp)],
              ['Development from 1 October', 'Capitalise as intangible asset', R(cap)],
              ['Amortisation (from 1 January)', '30 ÷ 5 × 3/12', R(am)]], title='AS 26 R&D')],
          'checks': list(ck)}

    ck2 = Checks()
    pat = ck2.add('6000000/8', 'Annual amortisation of the patent (₹)')
    i2 = {'id': 'i2', 'title': 'Life of a purchased patent', 'difficulty': 'core', 'minutes': 5,
          'q': 'Arun Tech Ltd. bought a patent for ₹60,00,000. Its legal life is 12 years, but the technology is expected to be useful for only 8 years. Compute annual amortisation and say whether an annual recoverable amount test is needed.',
          'solution': [table(['Item', 'Working', 'Answer'], [
              ['Useful life', 'Shorter of legal life (12) and expected use (8)', '8 years'],
              ['Annual amortisation', '60,00,000 ÷ 8', inr(pat)]], title='Amortisation'),
              p('The life is within the 10-year presumption, so the yearly recoverable amount test that applies to lives beyond 10 years is not required; normal AS 28 impairment indicators still apply.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'An intangible asset is an identifiable, non-monetary asset with no physical form, that the enterprise uses to make goods or deliver services, to let out, or to run its administration.',
            'Three features: identifiability (separable from goodwill), control (power to obtain benefits and restrict others\' access, usually by legal rights), and future economic benefits (revenue or cost savings).',
            'Examples: software, patents, copyrights, licences, franchises, import quotas, customer or supplier relationships, marketing rights. AS 26 does not cover financial assets, mineral rights, insurance contracts, goodwill on amalgamation (AS 14) and intangibles covered by other standards.'],
          'An asset you cannot touch but can identify, control and profit from.',
          'Staff skills are not an intangible asset — the company cannot control them.'),
        C('c2', T2, [
            'An intangible is recognised only if it is probable that its expected economic benefits will flow to the enterprise and its cost can be measured reliably; it is then measured at cost.',
            'Separately acquired: purchase price, import duties and non-refundable taxes, and directly attributable costs of preparing it for use.',
            'Acquired in an amalgamation in the nature of purchase: at fair value if it can be measured reliably; otherwise it is included in goodwill. Acquired by exchange: fair value of what is given up; by government grant: under AS 12.',
            'Later expenditure is added to cost only if it is likely to enable the asset to generate benefits beyond its originally assessed standard and can be measured reliably; otherwise it is expensed.'],
          'Recognise only what you can measure and expect to benefit from.',
          'A licence bought for ₹10 lakh plus ₹50,000 legal fees is recorded at ₹10.5 lakh.'),
        C('c3', T3, [
            'Internally generated goodwill is never recognised. Internally generated brands, mastheads, publishing titles, customer lists and similar items are not recognised either, as their cost cannot be separated from building the business as a whole.',
            'Research (original investigation to gain new knowledge) is always expensed.',
            'Development (applying research to plan or design new or improved products or processes before commercial use) is capitalised only when all of these can be shown: technical feasibility of completion; intention to complete and use or sell; ability to use or sell; how it will generate probable benefits (a market or internal usefulness); adequate technical, financial and other resources; and ability to measure the expenditure reliably.',
            'If research and development phases cannot be distinguished, all expenditure is treated as research. Cost of an internally generated intangible includes only expenditure from the date the criteria are first met; earlier expenses are not reinstated.'],
          'Think of research as exploring and development as building — only proven building is capitalised.',
          'Designing a prototype that has passed technical tests may be development; searching for new materials is research.'),
        C('c4', T4, [
            'Expensed when incurred, even if they may bring future benefits: start-up costs (unless part of PPE cost), training, advertising and promotion, relocation or reorganisation, and expenditure on research.',
            'Expenditure on an intangible item initially recognised as an expense is not later recognised as part of an asset\'s cost.'],
          'Some spending builds the business but cannot be capitalised.',
          'A launch advertising campaign of ₹2 crore is an expense, however successful.'),
        C('c5', T5, [
            'The depreciable amount is allocated systematically over the best estimate of useful life. There is a rebuttable presumption that the useful life does not exceed ten years from when the asset is available for use.',
            'Amortisation starts when the asset is available for use. The method reflects the pattern of benefits consumed; if that cannot be determined reliably, straight-line is used. Residual value is assumed to be zero unless there is a commitment by a third party to buy it or an active market.',
            'Amortisation period and method are revisited every year end. Where the life chosen is longer than ten years, recoverable amount is estimated at least annually, even without signs of impairment; AS 28 applies generally.',
            'On retirement or disposal, the asset is derecognised and the gain or loss (net proceeds less carrying amount) goes to profit and loss.'],
          'Ten years is the default ceiling; going beyond it needs evidence and annual testing.',
          'Software expected to be used for 4 years is amortised over 4, even if the licence is perpetual.'),
    ]

    jobs = [{'id': 'j1', 'title': 'R&D capitalisation review', 'role': 'Audit assistant',
             'situation': 'A tech client capitalised all R&D for a new app, including early user surveys and brand launch costs.',
             'steps': ['Split research and development phases.', 'Find the date all six criteria were met.', 'Remove launch, training and branding costs.', 'Set amortisation start and life.'],
             'takeaway': 'The date the criteria are met is the gateway for capitalisation.'}]

    mcqs = [
        Q('m1', 'Which can be recognised as an intangible asset?', ['A patent purchased from another company', 'Internally generated goodwill', 'An internally generated brand', 'Skilled staff'], 0,
          'A purchased patent is identifiable, controlled through legal rights and has a reliable cost. Internally generated goodwill and brands are not recognised, and staff skills are not controlled. In practice: check control first.', 'c1', T1),
        Q('m2', 'Expenditure in the research phase is:', ['Always expensed when incurred', 'Capitalised if successful', 'Capitalised if material', 'Deferred for five years'], 0,
          'Research cannot show that an asset exists that will generate probable future benefits, so AS 26 requires all research expenditure to be expensed when incurred. In practice: keep phase-wise cost records.', 'c3', T3),
        Q('m3', 'Development cost is capitalised only when the enterprise can demonstrate, among others:', ['Technical feasibility and ability to measure the expenditure reliably', 'That the product will sell at a profit in year one', 'Board approval only', 'That research was capitalised'], 0,
          'All criteria must be met: technical feasibility, intention to complete, ability to use or sell, probable benefits, adequate resources and reliable measurement. Board approval alone is not enough. In practice: document each criterion.', 'c3', T3),
        Q('m4', 'Development costs expensed before the criteria were met:', ['Cannot be reinstated as an asset later', 'Are reinstated when the criteria are met', 'Are added to goodwill', 'Are reversed through reserves'], 0,
          'Expenditure on an intangible item that was recognised as an expense in earlier periods stays an expense; it is never moved back into an asset\'s cost later. Capitalisation runs only from the date criteria are met. In practice: get the date right.', 'c3', T3),
        Q('m5', 'Which is expensed as incurred?', ['Advertising and promotional activities', 'Cost of a purchased software licence', 'Directly attributable cost of preparing a patent for use', 'Development cost after criteria are met'], 0,
          'AS 26 lists start-up, training, advertising and promotion, relocation and reorganisation costs as expenses when incurred, because they cannot be separated from developing the business as a whole. In practice: do not defer launch costs.', 'c4', T4),
        Q('m6', 'The rebuttable presumption for the maximum useful life of an intangible asset is:', ['Ten years from when it is available for use', 'Five years', 'Twenty years', 'Its legal life'], 0,
          'AS 26 assumes a useful life of at most ten years, counted from when the asset can first be used, unless persuasive evidence supports a longer life, in which case recoverable amount is tested annually. In practice: justify longer lives.', 'c5', T5),
        Q('m7', 'Residual value of an intangible asset is normally assumed to be:', ['Zero', 'Ten per cent of cost', 'Its market value', 'Its cost'], 0,
          'Residual value is taken as zero unless a third party has committed to buy the asset at the end of its life or there is an active market for it. In practice: most intangibles are amortised fully.', 'c5', T5),
        Q('m8', 'A licence costing ₹40 lakh with a useful life of 5 years, available for use on 1 October (year ends 31 March). Amortisation for the first year:', ['₹4 lakh', '₹8 lakh', '₹2 lakh', '₹6 lakh'], 0,
          'Annual amortisation is ₹40 lakh ÷ 5 = ₹8 lakh; it starts when the asset is available for use, so six months gives ₹4 lakh. In practice: use straight-line if the pattern is unclear.', 'c5', T5, 'moderate', check=4),
        Q('m9', 'If the useful life of an intangible asset is estimated beyond ten years, the enterprise must:', ['Estimate its recoverable amount at least annually', 'Write it off immediately', 'Revalue it each year', 'Stop amortising it'], 0,
          'Where the presumption of ten years is rebutted, AS 26 requires the recoverable amount to be estimated at least at each financial year end, even with no indication of impairment, and the reasons disclosed. In practice: keep strong evidence.', 'c5', T5),
        Q('m10', 'An intangible acquired in an amalgamation in the nature of purchase whose fair value cannot be measured reliably is:', ['Included in goodwill', 'Recognised at nil', 'Recognised at the transferor\'s book value', 'Expensed'], 0,
          'Such an intangible is recognised at fair value only when that can be measured reliably; otherwise it is not recognised separately and is subsumed in goodwill. In practice: get a valuation where possible.', 'c2', T2),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Research and pre-criteria development expensed', 2, 'computation', 'expense', nums=[exp]),
           S('s2', 'Capitalised from criteria date', 1.5, 'computation', 'capitalis', nums=[cap]),
           S('s3', 'Amortisation from available for use', 1.5, 'computation', 'amortis', nums=[am])],
          ['Use the criteria date.'], ['Reinstating earlier development costs.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Shorter useful life', 1, 'concept', 'shorter|8'),
           S('s2', 'Annual amortisation', 2, 'computation', 'amortisation', nums=[pat])],
          ['Economic life can be shorter than legal life.'], ['Using legal life.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What makes an asset "identifiable"?', 'It can be separated from the enterprise and its goodwill — sold, licensed or rented — or arises from contractual or legal rights.',
          [P('p1', 'Separable', 6, 'separa'), P('p2', 'From goodwill', 4, 'goodwill|legal')], 'c1'),
        V('v2', 'Why is internally generated goodwill not recognised?', 'Because it is neither separable nor tied to legal rights, so it fails identifiability, and what it cost to build cannot be measured reliably.',
          [P('p1', 'Fails identifiability', 5, 'identifiab|separable'), P('p2', 'Cost unreliable', 5, 'cost')], 'c3'),
        V('v3', 'List the conditions for capitalising development cost.', 'Technical feasibility, intention to complete, ability to use or sell, probable future benefits, adequate resources, and reliable measurement of expenditure.',
          [P('p1', 'Feasibility and intention', 5, 'feasib|intention'), P('p2', 'Benefits, resources, measurement', 5, 'resource|benefit|measure')], 'c3'),
        V('v4', 'From when does amortisation start?', 'From the date the intangible asset is available for use.',
          [P('p1', 'Available for use', 6, 'available'), P('p2', 'Date-based start', 4, 'date')], 'c5'),
        V('v5', 'Name two costs that are always expensed.', 'Advertising and promotion, staff training, start-up costs, relocation and research expenditure.',
          [P('p1', 'Advertising or training', 5, 'advertis|training'), P('p2', 'Research or start-up', 5, 'research|start-up|relocation')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Navya Foods Ltd.', 'difficulty': 'moderate',
              'case': 'Navya Foods Ltd. spent ₹50 lakh on TV ads for its new snack brand, ₹15 lakh on training its sales team and ₹40 lakh to buy the "Crunchy" brand from another company (expected useful life 6 years). It values its own brand "Navya" at ₹2 crore based on an expert report.',
              'mcqs': [
                  M('k1a', 'The "Navya" brand valued by the expert is:', ['Not recognised, as it is internally generated', 'Recognised at ₹2 crore', 'Recognised at cost of ads', 'Recognised as goodwill'], 0,
                    'Internally generated brands are not recognised as intangible assets, as their cost cannot be distinguished from developing the business. An expert valuation does not change this. In practice: no entry is passed.', 'core', topic=T3),
                  M('k1b', 'Amount expensed this year from the ads and training:', ['₹65 lakh', '₹50 lakh', '₹15 lakh', 'Nil'], 0,
                    'Advertising (₹50 lakh) and training (₹15 lakh) are expensed as incurred under AS 26, giving ₹65 lakh. They cannot be capitalised even if they build the brand. In practice: show under other expenses.', 'moderate', check=65, topic=T4),
                  M('k1c', 'Annual amortisation of the purchased "Crunchy" brand:', ['₹6.67 lakh', '₹4 lakh', '₹10 lakh', '₹8 lakh'], 0,
                    'A purchased brand is recognised at cost ₹40 lakh and amortised over its useful life of 6 years: ₹6.67 lakh a year, within the ten-year presumption. In practice: review the life yearly.', 'moderate', check=round(40/6, 2), topic=T5),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch05', 6, 'Accounting Standard 26 Intangible Assets',
                ['Identify intangible assets and their recognition criteria.',
                 'Distinguish research from development and apply capitalisation criteria.',
                 'Identify costs that are always expensed.',
                 'Amortise intangibles and apply the ten-year presumption and impairment rules.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 30, 'practice': 30}, 'prereq': ['int-p1-ch05-u05'],
                 'exam_tip': 'Draw a phase timeline: research → development before criteria → development after criteria → available for use.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Identifiable, controlled, future benefits, no physical form.', 'Recognise if benefits probable and cost reliable; at cost.',
                             'No internally generated goodwill, brands, titles, customer lists.', 'Research expensed; development capitalised once all six criteria met.',
                             'Advertising, training, start-up, relocation expensed.', 'Amortise from available for use; presumed life ≤ 10 years; annual test if longer.'],
                 'remember': ['Expensed costs are never reinstated.'],
                 'traps': ['Legal life is not automatically useful life.']},
                [('Presumed life', '≤ 10 years'), ('Research', 'Expense'), ('Residual value', 'Zero (usually)')],
                viva, cases)
