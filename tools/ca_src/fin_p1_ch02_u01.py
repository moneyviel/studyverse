"""CA Final · Paper 1 Financial Reporting · Chapter 2 Conceptual Framework for Financial Reporting under Ind AS.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch02-u01'
T1 = 'Status, objective and usefulness of general purpose financial reports'
T2 = 'Qualitative characteristics of useful information'
T3 = 'Financial statements, reporting entity and the elements'
T4 = 'Recognition, derecognition and measurement'
T5 = 'Presentation, disclosure and capital maintenance'


def build():
    ck = Checks()
    nom = ck.add('150000-100000', 'Profit — financial capital in nominal terms')
    cpp = ck.add('150000-100000*1.10', 'Profit — financial capital in constant purchasing power')
    phy = ck.add('150000-1000*120', 'Profit — physical capital maintenance')
    i1 = {'id': 'i1', 'title': 'How much profit, really?', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Asha starts a business on 1 April with ₹1,00,000 cash and buys 1,000 units at ₹100. She sells all units for ₹1,50,000 in cash by 31 March. General prices rose 10% in the year, and the replacement cost of a unit at year end is ₹120. Compute profit under (a) financial capital maintenance in nominal money, (b) financial capital maintenance in constant purchasing power, and (c) physical capital maintenance.',
          'solution': [table(['Concept', 'Capital to be maintained ₹', 'Profit ₹'], [
              ['(a) Nominal financial capital', inr(100000), inr(nom)],
              ['(b) Constant purchasing power', '1,00,000 × 1.10 = 1,10,000', inr(cpp)],
              ['(c) Physical capital (operating capability)', '1,000 units × ₹120 = 1,20,000', inr(phy)]], title='Capital maintenance'),
              note('The difference between each figure and ₹50,000 is a capital maintenance adjustment shown in equity, not income.')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Asset or not?', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Apply the Framework\'s definitions: (a) a skilled, loyal workforce built over years; (b) a non-cancellable contract to buy raw material next year at market price; (c) a patent the entity owns but has decided never to use and cannot sell; (d) a court case the entity is likely to lose, arising from a defective product sold last year.',
          'solution': [table(['Item', 'Conclusion', 'Reason'], [
              ['(a) Workforce', 'Not an asset', 'The entity does not control the employees\' future service — they can leave'],
              ['(b) Purchase contract at market price', 'Executory contract — combined right and obligation of equal value; usually nothing recognised', 'Neither party has performed; at market terms the net position is nil'],
              ['(c) Unusable, unsellable patent', 'Not an asset (no economic resource)', 'A right must have the potential to produce economic benefits'],
              ['(d) Likely court loss', 'Liability', 'Present obligation from a past event (the sale) to transfer economic resources']], title='Definitions of elements')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'The Conceptual Framework under Ind AS is not itself a standard and does not override any Ind AS. It helps standard-setters develop consistent standards, helps preparers form policies where no Ind AS applies, and helps everyone understand and interpret standards.',
            'The objective of general purpose financial reporting is to give existing and potential investors, lenders and other creditors information useful in deciding whether to provide resources — buying or selling instruments, lending, and voting on or influencing management\'s use of resources.',
            'Reports show economic resources and claims, changes in them (from performance on an accrual basis and from cash flows or issues of claims), and how efficiently management has used resources (stewardship). They cannot provide all information users need, are based partly on estimates, and do not show the value of the entity.'],
          'Financial reports serve capital providers first — everything else in the Framework follows from that purpose.',
          'A bank deciding on a loan relies on the borrower\'s accrual-based profits and cash flows to judge repayment ability.'),
        C('c2', T2, [
            'Fundamental characteristics: relevance — information capable of making a difference to decisions through predictive or confirmatory value, with materiality as an entity-specific aspect; and faithful representation — complete, neutral and free from error. Neutrality is supported by prudence (caution under uncertainty, without deliberately understating or overstating). Substance over form is part of faithful representation.',
            'Enhancing characteristics: comparability, verifiability, timeliness and understandability. They improve useful information but cannot make irrelevant or misrepresented information useful.',
            'Cost constraint: the benefit of reporting information should justify its cost. Measurement uncertainty does not stop information being useful if it is described faithfully.'],
          'Relevant and faithful come first; the four enhancers polish what is already useful.',
          'An estimate of a warranty provision is useful if its basis and uncertainty are disclosed honestly.'),
        C('c3', T3, [
            'Financial statements cover a specified period (with comparatives) and are prepared on the going concern assumption. A reporting entity may be a single entity, a part of one, or several entities — consolidated (parent with subsidiaries), unconsolidated or combined.',
            'Asset: an economic resource that the entity controls now because of something that has already happened; an economic resource is a right capable of producing economic benefits. Liability: a duty, existing now because of past events, to hand over an economic resource. Equity is the residual interest after deducting all liabilities.',
            'Income: rises in assets or falls in liabilities that lift equity, leaving out money put in by owners; expenses: the reverse, leaving out payouts to owners.',
            'Control means the present ability to direct the use of the resource and obtain its benefits. An obligation exists when the entity has no practical ability to avoid it. The unit of account and executory contracts (both sides unperformed) are also addressed.'],
          'Assets are rights the entity controls; liabilities are duties it cannot avoid; equity is what is left.',
          'Leased office space is an asset because the lessee controls the right to use it during the lease.'),
        C('c4', T4, [
            'Recognition captures an item that meets an element definition in the statements when doing so gives relevant information and a faithful representation. Recognition may be inappropriate where existence is uncertain, the probability of inflows or outflows is low, or measurement uncertainty is so high that no measure is faithful — though disclosure may still be needed.',
            'Derecognition removes all or part of an asset when control is lost, or of a liability when the obligation no longer exists; any retained component is recognised separately.',
            'Measurement bases: historical cost (entry price plus transaction costs, adjusted for consumption, impairment and payments) and current value — fair value (exit price to market participants), value in use for assets and fulfilment value for liabilities (entity-specific present values), and current cost (cost to replace now). The choice depends on relevance and faithful representation, how the item contributes to cash flows and the cost of measurement.'],
          'Recognise when it helps users; measure on the basis that best tells the story of the item.',
          'Investment property held to earn rentals and capital growth may be best described at fair value.'),
        C('c5', T5, [
            'Presentation and disclosure communicate efficiently: classify by shared characteristics, aggregate without hiding, and avoid offsetting unless required. The statement of profit or loss is the primary source of information on performance; income and expenses are included in other comprehensive income only when an Ind AS requires, typically when current value remeasurements are excluded from profit or loss. Amounts in OCI are, in principle, reclassified to profit or loss in a later period (recycling), unless a standard says otherwise.',
            'Capital maintenance links capital to profit: under financial capital maintenance (nominal money or constant purchasing power) profit is the increase in net assets in money terms beyond the opening capital; under physical capital maintenance profit arises only after maintaining operating capability (e.g. at current replacement cost). Increases needed to maintain capital are capital maintenance adjustments within equity.',
            'Most Indian companies use historical cost with financial capital in nominal terms; the Framework does not prescribe a single model.'],
          'Profit is what is left after keeping the starting capital intact — and "intact" can be measured in different ways.',
          'With high inflation, physical capital maintenance reports much lower profit than nominal capital maintenance.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Policy where no standard applies', 'role': 'Audit senior',
             'situation': 'A client earns income from a new digital token loyalty scheme that no Ind AS directly covers.',
             'steps': ['Look for Ind AS dealing with similar issues.', 'Apply the Framework\'s definitions and recognition criteria.', 'Choose a measurement basis that gives relevant and faithful information.', 'Disclose the policy and judgements.'],
             'takeaway': 'Ind AS 8 sends you to the Framework when a gap appears.'}]

    mcqs = [
        Q('m1', 'The Conceptual Framework:', ['Does not override any Ind AS', 'Overrides Ind AS in conflict', 'Is a standard in its own right', 'Applies only to banks'], 0,
          'Where the Framework conflicts with a standard, the standard prevails. In practice: it guides policy choice when no standard applies.', 'c1', T1),
        Q('m2', 'The primary users of general purpose financial reports are:', ['Existing and potential investors, lenders and other creditors', 'Tax authorities', 'Management', 'Employees only'], 0,
          'They cannot demand information directly and rely on these reports. In practice: regulators may find them useful but are not the target.', 'c1', T1),
        Q('m3', 'Which is a fundamental qualitative characteristic?', ['Faithful representation', 'Comparability', 'Timeliness', 'Verifiability'], 0,
          'Relevance and faithful representation are fundamental; the others enhance. In practice: enhancing ones cannot rescue misleading information.', 'c2', T2),
        Q('m4', 'Prudence in the Framework means:', ['Caution in judgements under uncertainty, without deliberate understatement', 'Always understating assets', 'Creating hidden reserves', 'Ignoring gains'], 0,
          'Prudence supports neutrality; asymmetric bias is not allowed. In practice: estimates should be balanced.', 'c2', T2),
        Q('m5', 'An asset is defined as:', ['An economic resource the entity controls now, arising from past events', 'Anything with a cost', 'A future benefit that is probable', 'Cash and receivables only'], 0,
          'The revised definition focuses on a right with potential to produce benefits, controlled now. In practice: probability is not part of the definition.', 'c3', T3),
        Q('m6', 'Fair value is:', ['An exit price between market participants at the measurement date', 'The entity\'s own value in use', 'Historical cost less depreciation', 'Replacement cost'], 0,
          'Fair value is market-based; value in use and fulfilment value are entity-specific. In practice: Ind AS 113 explains it.', 'c4', T4),
        Q('m7', 'Profit under physical capital maintenance arises only after:', ['Maintaining the entity\'s operating capability', 'Maintaining nominal money capital', 'Paying dividends', 'Revaluing all assets'], 0,
          'Physical capital is measured by productive capacity, e.g. at current cost. In practice: reduces profits in inflation.', 'c5', T5),
        Q('m8', 'Amounts recognised in OCI are, in principle:', ['Reclassified to profit or loss later, unless a standard says otherwise', 'Never reclassified', 'Taken directly to retained earnings always', 'Treated as equity contributions'], 0,
          'The Framework presumes recycling where it improves relevance. In practice: some Ind AS prohibit it (e.g. revaluation surplus).', 'c5', T5),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Nominal', 2, 'computation', 'nominal', nums=[nom]), S('s2', 'Constant purchasing power', 2, 'computation', 'purchasing', nums=[cpp]), S('s3', 'Physical', 2, 'computation', 'physical', nums=[phy])],
          ['State the capital to be maintained first.'], ['Deducting replacement cost under nominal capital.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Control test', 1.5, 'concept', 'control'), S('s2', 'Executory contract', 1.5, 'concept', 'executory'), S('s3', 'Economic resource', 1, 'concept', 'potential|economic'), S('s4', 'Liability', 1, 'concept', 'obligation')],
          ['Apply the definition word by word.'], ['Treating the workforce as an asset.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is the objective of general purpose financial reporting?', 'To give existing and potential investors, lenders and other creditors information useful for decisions about providing resources to the entity.',
          [P('p1', 'Users', 5, 'investor|lender|creditor'), P('p2', 'Resource decisions', 5, 'resource|decision')], 'c1'),
        V('v2', 'Name the enhancing qualitative characteristics.', 'Comparability, verifiability, timeliness and understandability.',
          [P('p1', 'Comparability and verifiability', 5, 'comparab|verifiab'), P('p2', 'Timeliness and understandability', 5, 'timel|understand')], 'c2'),
        V('v3', 'Define a liability under the Framework.', 'A duty the entity has now, because of past events, to hand over an economic resource; it must be a present obligation.',
          [P('p1', 'Present obligation', 5, 'present obligation'), P('p2', 'Transfer resource', 5, 'transfer|economic resource')], 'c3'),
        V('v4', 'When might an item meeting a definition not be recognised?', 'Where existence is uncertain, the probability of flows is low, or measurement uncertainty is very high, the item is left out when recognising it would fail the usefulness test of relevance and faithful representation; disclosure is given instead.',
          [P('p1', 'Uncertainty', 5, 'uncertain|probability'), P('p2', 'Usefulness test', 5, 'relevant|faithful|useful')], 'c4'),
        V('v5', 'Distinguish financial and physical capital maintenance.', 'Financial capital maintenance measures capital in money terms, nominal or constant purchasing power; physical capital maintenance measures it as productive capacity or operating capability.',
          [P('p1', 'Money terms', 5, 'money|nominal'), P('p2', 'Operating capability', 5, 'capacity|capability')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Delta Pharma', 'difficulty': 'moderate',
              'case': 'Delta Pharma (Ind AS) has: an internally generated brand built over 20 years; a lawsuit filed by a patient this year about a drug sold last year, which lawyers say Delta will probably lose; a licence to a molecule that regulators have permanently banned; and a plant measured at depreciated historical cost while its replacement cost has doubled.',
              'mcqs': [
                  M('k1a', 'The lawsuit is:', ['A liability — present obligation arising from a past sale', 'An executory contract', 'Equity', 'Not an element'], 0,
                    'The past event (the sale) created an obligation Delta cannot practically avoid. In practice: Ind AS 37 governs measurement.', 'moderate', topic=T3),
                  M('k1b', 'The licence to a banned molecule:', ['Fails the asset definition, having no potential to produce benefits', 'Is an asset at cost', 'Is a liability', 'Is income'], 0,
                    'A right with no potential for economic benefits is not an economic resource. In practice: derecognise or impair it.', 'moderate', topic=T3),
                  M('k1c', 'Measuring the plant at depreciated historical cost:', ['Is an acceptable measurement basis under the Framework', 'Is prohibited', 'Must change to replacement cost', 'Must change to fair value'], 0,
                    'The Framework allows historical cost and current values; standards decide which applies. In practice: Ind AS 16 permits cost or revaluation.', 'core', topic=T4),
                  M('k1d', 'If Delta measured profit after maintaining operating capability at replacement cost, it would be using:', ['Physical capital maintenance', 'Nominal financial capital maintenance', 'Cash accounting', 'Going concern basis'], 0,
                    'Replacement-cost based capital maintenance is physical. In practice: reported profit would fall.', 'core', topic=T5),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch02', 1, 'Conceptual Framework for Financial Reporting under Indian Accounting Standards (Ind AS)',
                ['Explain the status, objective and limits of general purpose financial reporting.',
                 'Apply the qualitative characteristics of useful information.',
                 'Apply the definitions of the elements, including control and obligation.',
                 'Explain recognition, derecognition, measurement bases, presentation and capital maintenance.'],
                {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 25}, 'prereq': ['fin-p1-ch01-u01'],
                 'exam_tip': 'Quote the definition, then test each part of it against the facts — that is how marks are awarded in Framework questions.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Framework guides but never overrides Ind AS.',
                             'Primary users: investors, lenders, creditors.',
                             'Fundamental: relevance (incl. materiality), faithful representation (prudence, substance).',
                             'Enhancing: comparability, verifiability, timeliness, understandability.',
                             'Asset = present economic resource controlled; liability = present obligation to transfer.',
                             'Measurement: historical cost, fair value, value in use/fulfilment value, current cost.',
                             'Capital maintenance: financial (nominal/CPP) vs physical.'],
                 'remember': ['Probability is not in the element definitions.'],
                 'traps': ['Enhancing characteristics cannot make useless information useful.']},
                [('Asset', 'Present economic resource controlled'), ('Liability', 'Present obligation to transfer'), ('Fundamental QCs', 'Relevance, faithful representation'), ('OCI', 'Recycled unless standard bars')],
                viva, cases)
