"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 11 Prospective Financial Information and Other Assurance Services.
Scope follows the ICAI study material; explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch11-u01'
T1 = 'Prospective financial information: forecasts and projections (SAE 3400)'
T2 = 'Examining and reporting on PFI'
T3 = 'Controls at a service organisation (SAE 3402)'
T4 = 'Pro forma financial information in prospectuses (SAE 3420)'


def build():
    ck = Checks()
    cover = ck.add('round(36/24,2)', 'Projected debt service coverage ratio')
    i1 = {'id': 'i1', 'title': 'A projection for a bank loan', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'A start-up submits projections to a bank showing cash available for debt service of ₹36 lakh a year against interest and instalments of ₹24 lakh, assuming a new plant reaches 90% capacity in year 1. Compute the coverage ratio and describe the practitioner\'s assurance and report.',
          'solution': [table(['Point', 'Treatment'], [
              ['Coverage ratio', '36 ÷ 24 = ' + inr(cover) + ' times'],
              ['Type of PFI', 'Projection — based on hypothetical assumptions (new plant ramp-up)'],
              ['Assurance on assumptions', 'Negative form: nothing suggests assumptions do not provide a reasonable basis (given the hypothetical ones)'],
              ['Opinion on preparation', 'Whether PFI is properly prepared on the assumptions and presented under the framework'],
              ['Caveat', 'Actual results likely to differ; variations may be material']], title='SAE 3400')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Type 1 or Type 2?', 'difficulty': 'core', 'minutes': 5,
          'q': 'A payroll service company wants a report for its clients\' auditors. (a) Clients\' auditors only need to understand how controls are designed now. (b) They want to rely on controls having worked through the year. Which SAE 3402 report fits each?',
          'solution': [table(['Need', 'Report'], [
              ['(a)', 'Type 1 — description and suitability of design at a specified date'],
              ['(b)', 'Type 2 — description, design and operating effectiveness throughout a period']], title='SAE 3402')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Prospective financial information (PFI) is financial information about the future, based on assumptions about events that may occur and possible actions by the entity. It is highly subjective and needs considerable judgement.',
            'A forecast is based on best-estimate assumptions about events management expects to take place; a projection is based on hypothetical assumptions (events not necessarily expected) or a mix of best-estimate and hypothetical assumptions, often for start-ups or major changes.',
            'Because outcomes depend on future events, the practitioner cannot express an opinion on whether results will be achieved.'],
          'Forecasts use best estimates; projections use "what if" assumptions.',
          'A new plant\'s first-year output is a hypothetical assumption.'),
        C('c2', T2, [
            'Before accepting, the practitioner considers intended use, distribution, whether assumptions are general-purpose or limited, period covered, and own competence. Acceptance is refused if assumptions are clearly unrealistic.',
            'Examination: understand the business, the process of preparing PFI, the past track record; evaluate assumptions (best estimate assumptions supported, hypothetical ones consistent with purpose), check calculations and consistency, and obtain written representations. The period covered should not extend beyond what management has a reasonable basis for.',
            'Report: identify the PFI, refer to SAE 3400, state management\'s responsibility, give negative assurance on assumptions, an opinion on proper preparation and presentation, and caveats that actual results may differ materially. Modify if presentation is inadequate or assumptions unreasonable, or withdraw.'],
          'Negative assurance on assumptions; positive opinion on preparation.',
          'A report on a 10-year projection must warn that results may vary materially.'),
        C('c3', T3, [
            'SAE 3402 covers assurance reports by a service auditor on controls at a service organisation that are likely relevant to user entities\' internal control over financial reporting.',
            'Type 1: management\'s description of its system and the suitability of design of controls at a specified date. Type 2: also operating effectiveness throughout a specified period, with tests of controls and results described.',
            'The service auditor obtains a written assertion from the service organisation, evaluates the description, tests controls (Type 2), considers subservice organisations (carve-out or inclusive method) and reports deviations.'],
          'Type 2 reports let user auditors rely on outsourced controls.',
          'A data centre provider issues a Type 2 report for its bank clients.'),
        C('c4', T4, [
            'Pro forma financial information illustrates how a major event or deal (e.g. an acquisition or divestment) would have changed the unadjusted figures had it happened earlier — commonly in prospectuses.',
            'Under SAE 3420, the practitioner reports on whether the responsible party has put the pro forma information together properly on the applicable criteria, considering the source of unadjusted information, adjustments and their support.',
            'The practitioner does not update or reissue reports on historical information used, and does not express an opinion on whether the pro forma reflects actual results.'],
          'Pro forma shows "what if it had happened earlier" — compiled, not predicted.',
          'A prospectus shows combined profits as if an acquisition occurred at the year start.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Examining projections for an IPO-bound company', 'role': 'Assurance manager',
             'situation': 'A company needs reports on projections and pro forma information for investors.',
             'steps': ['Assess acceptance and period covered.', 'Test assumptions and calculations.', 'Obtain representations.', 'Issue SAE 3400 and SAE 3420 reports with caveats.'],
             'takeaway': 'Future-looking information needs careful wording and caveats.'}]

    mcqs = [
        Q('m1', 'A forecast is based on:', ['Best-estimate assumptions', 'Hypothetical assumptions only', 'Historical results only', 'Audited figures'], 0,
          'Projection uses hypothetical. In practice: label clearly.', 'c1', T1),
        Q('m2', 'On assumptions underlying PFI, the practitioner gives:', ['Negative (moderate) assurance', 'Positive opinion', 'Absolute assurance', 'No comment'], 0,
          'SAE 3400. In practice: plus opinion on preparation.', 'c2', T2),
        Q('m3', 'A practitioner should decline a PFI engagement when:', ['Assumptions are clearly unrealistic', 'Period is one year', 'Client is a start-up', 'Fees are high'], 0,
          'Or PFI inappropriate for use. In practice: assess at acceptance.', 'c2', T2),
        Q('m4', 'A Type 2 report under SAE 3402 includes:', ['Operating effectiveness of controls over a period', 'Only design at a date', 'Financial statements', 'Tax compliance'], 0,
          'Supports reliance. In practice: tests and results described.', 'c3', T3),
        Q('m5', 'Pro forma financial information illustrates:', ['Impact of a significant event as if it happened earlier', 'Future forecasts', 'Audited results', 'Tax computations'], 0,
          'SAE 3420. In practice: prospectuses.', 'c4', T4),
        Q('m6', 'A PFI report must caution that:', ['Actual results are likely to differ and variations may be material', 'Results are guaranteed', 'Assumptions are audited', 'No risk exists'], 0,
          'Future uncertainty. In practice: standard caveat.', 'c2', T2),
        Q('m7', 'Under SAE 3402, subservice organisations can be dealt with by:', ['Carve-out or inclusive method', 'Ignoring them', 'Auditing user entities', 'Disclaimer only'], 0,
          'Two approaches. In practice: state which used.', 'c3', T3),
        Q('m8', 'A projection rather than a forecast is typical for:', ['A start-up or major business change', 'A stable mature business', 'Last year\'s results', 'Interim review'], 0,
          'Hypothetical assumptions. In practice: restricted use.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Coverage', 1.5, 'computation', 'coverage', nums=[cover]), S('s2', 'Projection', 1.5, 'concept', 'projection|hypothetical'), S('s3', 'Assurance and caveats', 3, 'concept', 'negative|differ')],
          ['State caveats.'], ['Giving an opinion on achievability.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Type 1', 1.5, 'concept', 'type 1'), S('s2', 'Type 2', 1.5, 'concept', 'type 2')],
          ['Match need to type.'], ['Using Type 1 for reliance.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Distinguish a forecast and a projection.', 'A forecast uses best-estimate assumptions; a projection uses hypothetical assumptions or a mix of both.',
          [P('p1', 'Best estimate', 5, 'best-estimate|best estimate'), P('p2', 'Hypothetical', 5, 'hypothetical')], 'c1'),
        V('v2', 'What does a PFI report contain?', 'Identification of PFI, management responsibility, negative assurance on assumptions, opinion on preparation and presentation, and caveats on achievability.',
          [P('p1', 'Negative assurance', 5, 'negative'), P('p2', 'Caveats', 5, 'caveat')], 'c2'),
        V('v3', 'What is a Type 1 report?', 'A report on the service organisation\'s description of its system and the suitability of design of controls at a specified date.',
          [P('p1', 'Description', 5, 'description'), P('p2', 'Design at a date', 5, 'design')], 'c3'),
        V('v4', 'What is pro forma financial information?', 'Information illustrating how a significant event or transaction would have changed unadjusted figures had it happened at an earlier date.',
          [P('p1', 'Significant event', 5, 'significant event|transaction'), P('p2', 'Earlier date', 5, 'earlier')], 'c4'),
        V('v5', 'Why can\'t a practitioner give an opinion on achieving PFI results?', 'Because results depend on future events and actions that may not occur as expected.',
          [P('p1', 'Future events', 5, 'future'), P('p2', 'May not occur', 5, 'may not occur')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Star Logistics Ltd.', 'difficulty': 'moderate',
              'case': 'Star Logistics outsources payroll to PayGrid Ltd. Its auditor wants to reduce substantive payroll testing. Separately, Star is listing and its prospectus will show combined results with a company it acquired after year end. It also plans to publish a five-year forecast.',
              'mcqs': [
                  M('k1a', 'To reduce substantive testing, the auditor needs from PayGrid:', ['A Type 2 SAE 3402 report', 'A Type 1 report', 'A forecast', 'A pro forma report'], 0,
                    'Operating effectiveness needed. In practice: check period overlap.', 'core', topic=T3),
                  M('k1b', 'The combined results in the prospectus are reported on under:', ['SAE 3420', 'SAE 3400', 'SRE 2410', 'SA 810'], 0,
                    'Pro forma compilation. In practice: compiled on criteria.', 'core', topic=T4),
                  M('k1c', 'The five-year forecast engagement follows:', ['SAE 3400', 'SAE 3402', 'SA 700', 'SRS 4410'], 0,
                    'Prospective information. In practice: caveats.', 'core', topic=T2),
                  M('k1d', 'For the forecast\'s assumptions the practitioner gives:', ['Negative assurance', 'A positive opinion', 'No comment', 'Guarantee'], 0,
                    'Moderate level. In practice: opinion on preparation separately.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch11', 1, 'Prospective Financial Information and Other Assurance Services',
                ['Distinguish forecasts and projections.',
                 'Examine and report on prospective financial information.',
                 'Report on controls at service organisations.',
                 'Report on compilation of pro forma financial information.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 15}, 'prereq': ['fin-p3-ch10-u01'],
                 'exam_tip': 'Identify the SAE first: 3400 future, 3402 service controls, 3420 pro forma.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['PFI: forecast (best estimate) vs projection (hypothetical).',
                             'SAE 3400: negative assurance on assumptions + opinion on preparation.',
                             'SAE 3402: Type 1 design; Type 2 effectiveness.',
                             'SAE 3420: pro forma compiled on criteria.',
                             'Always include caveats for future information.'],
                 'remember': ['No opinion on achievability of results.'],
                 'traps': ['Treating a projection as a forecast.']},
                [('SAE 3400', 'PFI'), ('SAE 3402', 'Service org controls'), ('SAE 3420', 'Pro forma'), ('Type 2', 'Over a period')],
                viva, cases)
