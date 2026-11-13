"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 18 SDG and ESG Assurance.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch18-u01'
T1 = 'SDGs and global sustainability reporting trends'
T2 = 'Integrated reporting and ESG evolution in India'
T3 = 'BRSR: structure and nine principles'
T4 = 'Assurance on sustainability information and climate in audits'


def build():
    ck = Checks()
    inten = ck.add('round(18000/600,2)', 'Emission intensity (tonnes CO₂e per ₹ crore revenue)')
    chg = ck.add('round((18000-20000)/20000*100,2)', 'Change in absolute emissions (%)')
    i1 = {'id': 'i1', 'title': 'Assuring an emissions metric', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A listed company reports Scope 1 and 2 emissions of 18,000 tonnes CO₂e on revenue of ₹600 crore, down from 20,000 tonnes last year. Compute emission intensity and change, and list what an assurance practitioner would check.',
          'solution': [table(['Item', 'Working / Check', 'Result'], [
              ['Intensity', '18,000 ÷ 600', inr(inten) + ' t per ₹ crore'],
              ['Change in emissions', '(18,000 − 20,000) ÷ 20,000', inr(chg) + '%'],
              ['Boundary', 'Which entities and sites are included', '—'],
              ['Data', 'Fuel and power records, emission factors, calculations', '—'],
              ['Standard', 'SAE 3410 (GHG statements) / SAE 3000', '—']], title='ESG assurance')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Climate risk in the financial audit', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'A coal-dependent power company faces stricter emission rules. How might climate risks affect the statutory audit?',
          'solution': [table(['Area', 'Audit consideration'], [
              ['Impairment', 'Shorter useful lives, lower cash flows — test assumptions (Ind AS 36)'],
              ['Provisions', 'Decommissioning, penalties, onerous contracts (Ind AS 37)'],
              ['Going concern', 'Regulatory changes threatening operations (SA 570)'],
              ['Other information', 'Consistency of sustainability claims with statements (SA 720)']], title='Climate in audit')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'The UN\'s 17 Sustainable Development Goals (2015, target 2030) cover poverty, hunger, health, education, gender equality, water, energy, decent work, industry, inequality, cities, consumption, climate, life below water and on land, peace and partnerships.',
            'Global trends: GRI standards for impact reporting, ISSB\'s IFRS S1 and S2 for investor-focused sustainability and climate disclosures, TCFD recommendations (governance, strategy, risk management, metrics and targets), and regional rules (EU CSRD, US and UK climate disclosure requirements).',
            'Investors increasingly integrate ESG factors into decisions, making reliable sustainability information important.'],
          'Sustainability reporting is moving from voluntary to regulated.',
          'IFRS S2 requires climate-related risk disclosures for investors.'),
        C('c2', T2, [
            'Integrated reporting explains how an organisation creates value over time using six capitals: financial, manufactured, intellectual, human, social and relationship, and natural.',
            'India\'s ESG journey: National Voluntary Guidelines (2011), Business Responsibility Reports for top listed companies, National Guidelines on Responsible Business Conduct (2019), and the Business Responsibility and Sustainability Report (BRSR) mandated by SEBI for the top 1,000 listed companies by market capitalisation.',
            'ICAI initiatives include its Sustainability Reporting Standards Board, guidance and the Standard on Assurance Engagements for sustainability information.'],
          'Value creation is broader than profit — six capitals.',
          'A listed company in the top 1,000 must file a BRSR with its annual report.'),
        C('c3', T3, [
            'The BRSR has three sections: general disclosures (company details, products, operations, employees), management and process disclosures (policies, governance for the nine principles), and principle-wise performance (essential and leadership indicators).',
            'The nine NGRBC principles: ethics and transparency; sustainable and safe goods and services; employee well-being; stakeholder responsiveness; human rights; environment protection; responsible public policy advocacy; inclusive growth; and consumer value.',
            'BRSR Core is a set of key ESG metrics (e.g. emissions, water, energy, waste, employee well-being, gender diversity) for which SEBI requires assessment or assurance for top listed entities in a phased manner, along with value chain disclosures.'],
          'Nine principles, three sections, and a core set needing independent checks.',
          'Water consumption and GHG emissions are BRSR Core metrics.'),
        C('c4', T4, [
            'Assurance on sustainability information uses standards such as SAE 3000 (assurance other than audits or reviews of historical financial information) and SAE 3410 (GHG statements); assurance can be limited or reasonable.',
            'Procedures: understand reporting boundaries and criteria, assess risks, test data collection systems, recalculate metrics, verify source documents and estimates, and evaluate disclosures.',
            'Climate in financial audits: the auditor considers climate-related risks in assessing risks of material misstatement — asset impairment, useful lives, provisions, fair values, going concern — and reads sustainability information for consistency with the financial statements.'],
          'ESG numbers need the same rigour as financial numbers.',
          'A company claiming net zero while expanding coal assets invites audit scrutiny.'),
    ]

    jobs = [{'id': 'j1', 'title': 'BRSR Core assurance', 'role': 'Sustainability assurance manager',
             'situation': 'A top-150 listed company needs assurance on its BRSR Core metrics.',
             'steps': ['Agree criteria, boundaries and level of assurance.', 'Understand data systems.', 'Test and recalculate metrics.', 'Report under SAE 3000/3410.'],
             'takeaway': 'Boundaries and data systems are the heart of ESG assurance.'}]

    mcqs = [
        Q('m1', 'The number of UN Sustainable Development Goals is:', ['Seventeen', 'Ten', 'Nine', 'Twenty'], 0,
          'Adopted 2015 for 2030. In practice: map to business.', 'c1', T1),
        Q('m2', 'The BRSR is mandatory for:', ['Top 1,000 listed companies by market capitalisation', 'All companies', 'Only banks', 'Only unlisted companies'], 0,
          'SEBI requirement. In practice: part of annual report.', 'c2', T2),
        Q('m3', 'Integrated reporting is built around:', ['Six capitals', 'Three capitals', 'Profit only', 'Tax only'], 0,
          'Value creation over time. In practice: IIRC framework.', 'c2', T2),
        Q('m4', 'BRSR principle-wise disclosures are based on:', ['Nine NGRBC principles', 'Seventeen SDGs directly', 'Ind AS', 'CARO'], 0,
          'National guidelines. In practice: essential and leadership indicators.', 'c3', T3),
        Q('m5', 'Assurance on a GHG statement is governed by:', ['SAE 3410', 'SA 700', 'SRE 2400', 'SRS 4400'], 0,
          'Specific standard. In practice: SAE 3000 for other info.', 'c4', T4),
        Q('m6', 'Climate risk can affect the statutory audit through:', ['Impairment, useful lives and provisions', 'Nothing', 'Only marketing', 'Only payroll'], 0,
          'Risk of material misstatement. In practice: SA 315.', 'c4', T4),
        Q('m7', 'TCFD recommendations cover:', ['Governance, strategy, risk management, metrics and targets', 'Only targets', 'Only governance', 'Only emissions'], 0,
          'Four pillars. In practice: basis of IFRS S2.', 'c1', T1),
        Q('m8', 'BRSR Core metrics require:', ['Assessment or assurance for top listed entities in phases', 'No checks', 'Only board approval', 'Tax audit'], 0,
          'SEBI glide path. In practice: value chain too.', 'c3', T3),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Metrics', 2, 'computation', 'intensity|change', nums=[inten, chg]), S('s2', 'Checks', 3, 'concept', 'boundary|data|3410')],
          ['Define boundaries.'], ['Ignoring emission factors.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Impairment and provisions', 2.5, 'concept', 'impairment|provision'), S('s2', 'Going concern and other info', 2.5, 'concept', 'going concern|consistency')],
          ['Cite Ind AS and SAs.'], ['Treating ESG as outside the audit.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Name the three sections of BRSR.', 'General disclosures, management and process disclosures, and principle-wise performance disclosures.',
          [P('p1', 'General and management', 5, 'general|management'), P('p2', 'Principle-wise', 5, 'principle')], 'c3'),
        V('v2', 'What are the six capitals of integrated reporting?', 'Financial, manufactured, intellectual, human, social and relationship, and natural capital.',
          [P('p1', 'Financial and manufactured', 5, 'financial|manufactured'), P('p2', 'Human and natural', 5, 'human|natural')], 'c2'),
        V('v3', 'Which standards apply to sustainability assurance?', 'SAE 3000 for assurance on non-historical information and SAE 3410 for greenhouse gas statements.',
          [P('p1', 'SAE 3000', 5, '3000'), P('p2', 'SAE 3410', 5, '3410')], 'c4'),
        V('v4', 'How do climate risks affect a financial statement audit?', 'Through impairment, useful lives, provisions, fair values and going concern, plus consistency of other information.',
          [P('p1', 'Impairment and provisions', 5, 'impairment|provision'), P('p2', 'Going concern', 5, 'going concern')], 'c4'),
        V('v5', 'What do the SDGs aim for?', 'A global agenda to end poverty, protect the planet and ensure prosperity by 2030 through 17 goals.',
          [P('p1', 'Poverty and planet', 5, 'poverty|planet'), P('p2', '2030', 5, '2030')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Elara Consumer Goods', 'difficulty': 'moderate',
              'case': 'Elara, among the top 1,000 listed companies, publishes a BRSR claiming 40% renewable energy. Its auditor notices the plant using that energy was sold mid-year. Elara also faces new plastic packaging rules that may make some machinery obsolete.',
              'mcqs': [
                  M('k1a', 'Elara must publish:', ['A BRSR', 'Only a CSR report', 'Nothing', 'An LFAR'], 0,
                    'Top 1,000 listed. In practice: with annual report.', 'core', topic=T2),
                  M('k1b', 'The renewable energy claim requires checking:', ['Reporting boundary after the plant sale', 'Only invoices', 'Tax returns', 'Nothing'], 0,
                    'Boundary changes affect metrics. In practice: restate if needed.', 'moderate', topic=T4),
                  M('k1c', 'Possible obsolescence of machinery affects:', ['Impairment and useful lives in the audit', 'Only marketing', 'BRSR only', 'Nothing'], 0,
                    'Climate/regulatory risk. In practice: Ind AS 36.', 'core', topic=T4),
                  M('k1d', 'An inconsistency between BRSR claims and financial statements is handled under:', ['SA 720', 'SA 610', 'SA 505', 'SRS 4410'], 0,
                    'Other information. In practice: request correction.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch18', 1, 'Sustainable Development Goals (SDG) & Environment, Social and Governance (ESG) Assurance',
                ['Explain SDGs and global sustainability reporting trends.',
                 'Describe integrated reporting and ESG evolution in India.',
                 'Explain BRSR structure and principles.',
                 'Perform assurance on sustainability information and consider climate in audits.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 15}, 'prereq': ['fin-p3-ch17-u01'],
                 'exam_tip': 'Link ESG facts to both assurance standards (SAE 3000/3410) and financial audit SAs.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['17 SDGs by 2030.',
                             'GRI, ISSB (S1, S2), TCFD.',
                             'Integrated reporting: six capitals.',
                             'BRSR: top 1,000 listed; nine principles; BRSR Core.',
                             'SAE 3000/3410; climate in SA 315/570/720.'],
                 'remember': ['Boundaries matter for ESG metrics.'],
                 'traps': ['Treating BRSR as unaudited marketing.']},
                [('SDGs', '17'), ('BRSR', 'Top 1,000 listed'), ('Principles', 'Nine NGRBC'), ('GHG assurance', 'SAE 3410')],
                viva, cases)
