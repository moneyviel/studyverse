"""CA Final · Paper 4 · Chapter 22 Double Taxation Relief.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch22-u01'
T1 = 'Concept and methods of double taxation relief'
T2 = 'Bilateral relief under section 159'
T3 = 'Unilateral relief under section 160'
T4 = 'Foreign tax credit rules'


def build():
    ck = Checks()
    tax = ck.add('(400000*0.05+400000*0.10+300000*0.15)*1.04', 'Indian tax on ₹15 lakh incl. cess (₹)')
    rate = ck.add('round((400000*0.05+400000*0.10+300000*0.15)*1.04/1500000*100,2)', 'Indian average rate (%)')
    rel = ck.add('500000*min(0.0728,0.10)', 'Relief on ₹5 lakh at lower rate (₹)')
    net = ck.add('(400000*0.05+400000*0.10+300000*0.15)*1.04-500000*0.0728', 'Net tax payable (₹)')
    i1 = {'id': 'i1', 'title': 'Unilateral relief', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Ritu, a resident under the default regime, has Indian income of ₹10,00,000 and income of ₹5,00,000 from Country Z (no tax treaty with India), on which she paid tax of ₹50,000 there. Compute her tax liability for T.Y. 2026-27 after relief under section 160.',
          'solution': [table(['Step', 'Working', '₹ / %'], [
              ['Tax on ₹15 lakh with cess', '1,05,000 × 1.04', inr(tax)],
              ['Indian average rate', '1,09,200 ÷ 15,00,000', f'{rate}%'],
              ['Foreign rate', '50,000 ÷ 5,00,000', '10%'],
              ['Relief', '5,00,000 × lower rate (7.28%)', inr(rel)],
              ['Net tax payable', '', inr(net)]], title='Section 160')],
          'checks': list(ck)}

    c2 = Checks()
    it = c2.add('2000000*0.25', 'Indian tax on foreign income at 25% (₹)')
    ft = c2.add('2000000*0.30', 'Foreign tax actually paid (₹)')
    tr = c2.add('2000000*0.15', 'Foreign tax permitted under treaty (₹)')
    fc = c2.add('min(2000000*0.25,2000000*0.30,2000000*0.15)', 'Foreign tax credit allowed (₹)')
    i2 = {'id': 'i2', 'title': 'Credit capped by the treaty', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Indus Tech Ltd (Indian rate 25%; ignore surcharge and cess) earns ₹20,00,000 of royalty from Country K, which withheld tax at 30%. The India–K treaty limits source taxation of royalty to 15%. Compute the foreign tax credit.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Indian tax on the income', '25% × 20,00,000', inr(it)],
              ['Foreign tax paid', '30% × 20,00,000', inr(ft)],
              ['Tax as per treaty', '15% × 20,00,000 (excess ignored)', inr(tr)],
              ['FTC', 'Lower of Indian tax and treaty-permitted foreign tax', inr(fc)]], title='Rule 76')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Double taxation arises when the same income is taxed in two countries — usually because one taxes on residence and another on source. Relief may be juridical (same person) or economic (same income in different hands).',
            'Methods: exemption (income taxed only in one country, fully or with progression), credit (home country allows credit for foreign tax — full or ordinary, limited to home tax), and tax sparing (credit for tax foregone by the source country under incentives).',
            'Relief is bilateral when given under a treaty between two countries, and unilateral when a country grants it on its own where no treaty exists. India uses the credit method in most treaties.'],
          'Treaties allocate taxing rights; credits avoid paying twice.',
          'An Indian resident taxed in the UK on rent gets credit in India for UK tax.'),
        C('c2', T2, [
            'Section 159 empowers the Central Government to enter into agreements with other countries or specified territories to grant relief, avoid double taxation, exchange information and assist in recovery; agreements with specified associations may also be adopted.',
            'Where an agreement exists, its provisions apply to the extent more beneficial than the Act; however, a non-resident claiming treaty benefit must furnish a Tax Residence Certificate from his country and prescribed information (Form No. 41), and treaty benefits cannot override GAAR.',
            'Terms not defined in the treaty or Act take meanings notified by the Government. Treaty relief cannot be used to avoid tax through treaty shopping where a principal purpose test or limitation-of-benefit clause applies.'],
          'Treaty or Act, whichever is better — with a TRC in hand.',
          'A Mauritius resident without a TRC cannot claim the treaty rate.'),
        C('c3', T3, [
            'Section 160 grants unilateral relief to a resident where income accrues outside India (and is not deemed to accrue in India), has been taxed in a country with no treaty with India, and tax has been paid there.',
            'Relief is the doubly taxed income multiplied by the lower of the Indian rate and the foreign rate (or the Indian rate if equal). The Indian rate is Indian tax after reliefs but before double taxation relief, divided by total income; the foreign rate is foreign tax actually paid divided by income assessed there.',
            'Agricultural income from a non-treaty country is also covered where it is taxed abroad.'],
          'Relief equals doubly taxed income times the lower average rate.',
          'At an Indian average rate of 7.28%, ₹5 lakh of foreign income earns relief of ₹36,400.'),
        C('c4', T4, [
            'Rule 76: foreign tax credit is allowed to residents in the year the corresponding income is offered to tax in India, against tax, surcharge and cess (not interest, fee or penalty), and is computed source-wise and country-wise as the lower of Indian tax on that income and foreign tax paid.',
            'Foreign tax paid in excess of treaty limits is ignored. Disputed foreign tax is allowed later once the dispute is settled, on a claim within six months from the end of the month of settlement. Currency is converted at the TT buying rate on the last day of the month before tax was paid.',
            'A statement in the prescribed form with proof of foreign tax must be filed by the return due date (and FTC against MAT/AMT is computed similarly).'],
          'Credit is the lower of the two taxes, source by source.',
          'Royalty taxed at 30% abroad under a 15% treaty cap earns credit of only 15%.'),
    ]

    jobs = [{'id': 'j1', 'title': 'FTC claim for an expatriate', 'role': 'Tax associate',
             'situation': 'A returning employee paid tax in two countries on foreign salary.',
             'steps': ['Identify treaty or non-treaty countries.', 'Compute Indian tax on each source.', 'Apply treaty limits to foreign tax.', 'File the FTC statement with proof by the due date.'],
             'takeaway': 'Credit is lost if paperwork is late.'}]

    mcqs = [
        Q('m1', 'Unilateral relief under section 160 is available when:', ['There is no treaty with the other country', 'There is a treaty', 'Income is deemed to accrue in India', 'The assessee is non-resident'], 0,
          'Conditions. In practice: resident only.', 'c3', T3),
        Q('m2', 'Relief under section 160 is computed at:', ['The lower of the Indian and foreign rates', 'The Indian rate always', 'The foreign rate always', 'The higher rate'], 0,
          'Average rates. In practice: equal = Indian rate.', 'c3', T3),
        Q('m3', 'A non-resident must furnish which document to claim treaty benefit?', ['Tax Residence Certificate', 'Passport only', 'Bank statement', 'Audit report'], 0,
          'Section 159. In practice: plus Form No. 41.', 'c2', T2),
        Q('m4', 'Treaty provisions apply:', ['To the extent more beneficial than the Act', 'Always over the Act', 'Never over the Act', 'Only to companies'], 0,
          'Section 159. In practice: GAAR may override.', 'c2', T2),
        Q('m5', 'Foreign tax credit is NOT available against:', ['Interest and penalty', 'Income-tax', 'Surcharge', 'Health and education cess'], 0,
          'Rule 76(4). In practice: only tax components.', 'c4', T4),
        Q('m6', 'Foreign tax paid above the treaty rate is:', ['Ignored for credit', 'Fully credited', 'Refunded by India', 'Carried forward'], 0,
          'Rule 76. In practice: seek refund abroad.', 'c4', T4),
        Q('m7', 'The method where the home country credits foreign tax limited to home tax is:', ['Ordinary credit', 'Full credit', 'Exemption', 'Tax sparing'], 0,
          'Common method. In practice: India uses credit.', 'c1', T1),
        Q('m8', 'Claim for credit of a disputed foreign tax after settlement must be made within:', ['Six months from end of month of settlement', 'One year', 'Thirty days', 'Two years'], 0,
          'Rule 76(6). In practice: with proof.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Indian tax and rate', 3, 'computation', 'average', nums=[tax]), S('s2', 'Relief and net tax', 3, 'computation', 'relief', nums=[rel, net])],
          ['Define rates.'], ['Using the foreign rate when higher.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Taxes compared', 3, 'computation', 'treaty', nums=[it, ft, tr]), S('s2', 'FTC', 2, 'computation', 'credit', nums=[fc])],
          ['Mention excess ignored.'], ['Allowing full foreign tax.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is tax sparing?', 'Credit by the residence country for tax the source country gave up under incentives, as if it had been paid.',
          [P('p1', 'Credit', 5, 'credit'), P('p2', 'Incentives', 5, 'incentive')], 'c1'),
        V('v2', 'What is the Indian rate of tax for section 160?', 'Indian income-tax after reliefs but before double taxation relief, divided by total income.',
          [P('p1', 'Divided by total income', 5, 'total income'), P('p2', 'Before relief', 5, 'before')], 'c3'),
        V('v3', 'Is a TRC alone enough for treaty benefit?', 'A TRC is necessary, and prescribed information in Form No. 41 must also be furnished.',
          [P('p1', 'Necessary', 5, 'necessary'), P('p2', 'Form No. 41', 5, '41')], 'c2'),
        V('v4', 'How is FTC computed when income comes from several countries?', 'Separately for each source of income from each country, then aggregated.',
          [P('p1', 'Separately', 5, 'separately'), P('p2', 'Aggregated', 5, 'aggregat')], 'c4'),
        V('v5', 'Which exchange rate applies to convert foreign tax?', 'The TT buying rate on the last day of the month before the month of payment or deduction.',
          [P('p1', 'TT buying', 5, 'tt buying'), P('p2', 'Last day', 5, 'last day')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Kapoor\'s foreign rent', 'difficulty': 'core',
              'case': 'Aman Kapoor, resident, earns rent from a flat in a country with which India has no treaty. The rent is ₹8,00,000 and he paid tax of ₹1,20,000 there. His Indian average rate of tax works out to 12%.',
              'mcqs': [
                  M('k1a', 'Foreign average rate (%):', ['15', '12', '10', '20'], 0,
                    '1,20,000 ÷ 8,00,000. In practice: actual tax paid.', 'core', check=15, topic=T3),
                  M('k1b', 'Rate used for relief (%):', ['12', '15', '13.5', '27'], 0,
                    'Lower rate. In practice: Indian rate.', 'core', check=12, topic=T3),
                  M('k1c', 'Relief under section 160 (₹):', ['96,000', '1,20,000', '24,000', '1,08,000'], 0,
                    '8,00,000 × 12%. In practice: deducted from Indian tax.', 'core', check=96000, topic=T3),
                  M('k1d', 'Is the extra foreign tax (above relief) refundable in India?', ['No', 'Yes', 'Only for companies', 'Only if treaty exists'], 0,
                    'Relief limited. In practice: cost to taxpayer.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch22', 1, 'Double Taxation Relief',
                ['Explain double taxation and methods of relief.',
                 'Apply bilateral relief and treaty conditions.',
                 'Compute unilateral relief under section 160.',
                 'Compute foreign tax credit under Rule 76.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 30, 'practice': 25}, 'prereq': ['fin-p4-ch21-u01'],
                 'exam_tip': 'Compute both average rates to two decimals and apply the lower one.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Methods: exemption, credit, tax sparing.', 'Section 159 treaties; TRC and Form No. 41.', 'Section 160 relief at the lower average rate.',
                             'Rule 76 FTC: lower of Indian tax and foreign tax; excess over treaty ignored.'],
                 'remember': ['No FTC on interest, fee or penalty.'],
                 'traps': ['Granting relief at the higher foreign rate.']},
                [('Bilateral relief', 'Section 159'), ('Unilateral relief', 'Section 160'), ('FTC', 'Rule 76')],
                viva, cases)
