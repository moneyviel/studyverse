"""CA Final · Paper 5 · Part II Customs · Chapter 8 Foreign Trade Policy.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ii-ch08-u01'
T1 = 'Framework of the Foreign Trade Policy'
T2 = 'Status holders and trade facilitation'
T3 = 'Duty exemption schemes: Advance Authorisation and DFIA'
T4 = 'EPCG, EOU and deemed exports'


def build():
    ck = Checks()
    va = ck.add('(9200000-8000000)/8000000*100', 'Value addition: (FOB − CIF of inputs)/CIF × 100 (%)')
    eo1 = ck.add('5000000*6', 'EPCG export obligation on imported capital goods: 6 × duty saved (₹)')
    eo2 = ck.add('2000000*6*0.75', 'EPCG export obligation on indigenous capital goods: 4.5 × duty saved (₹)')
    tot = ck.add('5000000*6+2000000*6*0.75', 'Total specific export obligation (₹)')
    i1 = {'id': 'i1', 'title': 'Value addition and EPCG obligation', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Narmada Fabrics (a) holds an Advance Authorisation: CIF value of duty-free inputs ₹80 lakh, FOB value of exports realised ₹92 lakh — check value addition; (b) under EPCG, saved duty of ₹50 lakh on imported machines and ₹20 lakh on machines sourced from a domestic maker. Compute the specific export obligation.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Value addition', '(92 − 80)/80 × 100', f'{va:g}% — meets the 15% minimum'],
              ['EO on imported CG', '6 × ₹50 lakh', f'₹{inr(eo1)}'],
              ['EO on indigenous CG', '75% of 6 times = 4.5 × ₹20 lakh', f'₹{inr(eo2)}'],
              ['Total specific EO', 'To be met in 6 years from issue', f'₹{inr(tot)}']], title='FTP 2023 schemes')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Which status category?', 'difficulty': 'core', 'minutes': 5,
          'q': 'Coral Exports has export performance (FOB) of US$1.2 million, 1.5 million and 1.4 million over the three preceding years and US$0.9 million in the current year so far. Which status can it claim?',
          'solution': [table(['Point', 'Rule', 'Result'], [
              ['Total', 'Current plus three preceding years', 'US$5 million'],
              ['Threshold', 'One Star needs US$3 million; Two Star US$15 million', 'One Star Export House'],
              ['Yearly performance', 'Exports in the preceding years (two of three suffice for One Star from 21 August 2026)', 'Met']], title='Status holders')]}

    concepts = [
        C('c1', T1, [
            'The Foreign Trade (Development and Regulation) Act, 1992 empowers the Central Government to frame the Foreign Trade Policy (section 5). FTP 2023 came into force on 1 April 2023 without a fixed end date and is updated as needed. The Directorate General of Foreign Trade (DGFT) under the Ministry of Commerce administers it.',
            'The policy package has the FTP (11 chapters), the Handbook of Procedures, Appendices and Aayat Niryat Forms, and the ITC (HS) classification of export and import items, which says whether an item is free, restricted or prohibited. SCOMET items need special authorisation.',
            'Import or export needs an Importer Exporter Code (IEC) unless exempted. DGFT\'s interpretation of the policy and ITC (HS) classification is final; relaxations can be sought from the Policy Relaxation Committee, Norms Committee or EPCG Committee. FTP benefits do not override tax laws.'],
          'Act, policy, handbook and ITC (HS) work together.',
          'An exporter without an IEC cannot ship goods unless exempted.'),
        C('c2', T2, [
            'Status holders are exporters recognised on export performance (FOB, in convertible currency or rupees) over the current and three preceding years: One Star US$3 million, Two Star 15, Three Star 50, Four Star 200 and Five Star 800. Performance is not transferable and re-exports do not count; MSEs, ISO/BIS units, North-East and J&K/Ladakh units and fruit and vegetable exports get double weightage for One Star.',
            'Privileges include self-declaration clearances, priority norm fixation within 60 days, exemption from negotiating documents through banks and from bank guarantees under schemes, and other facilitation.',
            'Facilitation measures include the Niryat Bandhu mentoring scheme, Districts as Export Hubs, Towns of Export Excellence, the AEO programme (customs-certified compliant traders under the WCO SAFE framework) and online DGFT services.'],
          'Recognition grows with export scale.',
          'An exporter with US$16 million over four years qualifies as Two Star.'),
        C('c3', T3, [
            'Advance Authorisation allows duty-free import of inputs physically incorporated in export products (with normal wastage), fuel, oil and catalysts, and mandatory spares up to 10% of CIF value. It is subject to actual user condition and is non-transferable even after export. Validity for import is 12 months from issue. Minimum value addition is 15%, computed as (FOB of exports realised − CIF of inputs)/CIF × 100.',
            'Annual Advance Authorisation is available to exporters with performance in at least the two preceding years, up to the higher of 300% of FOB of the preceding year\'s exports and ₹1 crore. Where a foreign buyer supplies inputs free, their notional value is added to both sides for value addition.',
            'DFIA allows duty-free import of inputs after export, with minimum value addition of 20%; it is transferable once export obligation is fulfilled, but is not issued for inputs with actual-user or pre-import conditions. Exports must be completed within 12 months of the online application, and the DFIA is valid for 12 months from issue.'],
          'Import inputs duty-free against an export commitment.',
          'Inputs of ₹80 lakh producing exports of ₹92 lakh give 15% value addition.'),
        C('c4', T4, [
            'EPCG lets an exporter bring in capital goods used before, during or after manufacture without customs duty (or buy them domestically), against a specific export obligation of 6 times the duties, taxes and cess saved, to be met in 6 years from issue, in addition to any average export obligation (average exports of the preceding three years). For indigenously sourced capital goods, the specific obligation is 25% lower (4.5 times). The authorisation is valid for import for 24 months.',
            'EOU, EHTP, STP and BTP units export their entire output (except permitted DTA sales), may import or procure inputs duty-free, and must be positive net foreign exchange earners, computed cumulatively in 5-year blocks. Exit is permitted on payment of applicable duties.',
            'Deemed exports are specified supplies in which goods do not leave India but payment is received in rupees or free foreign exchange, such as supplies against Advance Authorisation, EPCG, to EOUs, and to specified projects. They give a level playing field to domestic suppliers through benefits like refund of terminal excise or drawback, as specified.'],
          'Capital goods duty-free for exporting six times the savings.',
          'Duty saved ₹50 lakh on machines means exports of ₹3 crore in six years.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Export obligation tracker', 'role': 'EXIM manager',
             'situation': 'The company holds several EPCG and Advance Authorisations.',
             'steps': ['List each authorisation\'s obligation and deadline.', 'Track realised exports.', 'Compute value addition.', 'Apply for extension early where needed.'],
             'takeaway': 'Unmet obligations bring duty plus interest.'}]

    mcqs = [
        Q('m1', 'The FTP is framed under section 5 of:', ['Foreign Trade (Development and Regulation) Act, 1992', 'Customs Act, 1962', 'FEMA, 1999', 'Customs Tariff Act, 1975'], 0,
          'Enabling Act. In practice: DGFT administers.', 'c1', T1),
        Q('m2', 'Export threshold for a One Star Export House is:', ['Three million US dollars', 'Fifteen million', 'One million', 'Fifty million'], 0,
          'Status table. In practice: double weightage cases.', 'c2', T2),
        Q('m3', 'Minimum value addition under Advance Authorisation is:', ['Fifteen percent', 'Twenty percent', 'Ten percent', 'Twenty-five percent'], 0,
          'General rule. In practice: some products lower.', 'c3', T3),
        Q('m4', 'Minimum value addition under DFIA is:', ['Twenty percent', 'Fifteen percent', 'Ten percent', 'Thirty percent'], 0,
          'DFIA rule. In practice: transferable later.', 'c3', T3),
        Q('m5', 'Which authorisation is transferable after export obligation is met?', ['DFIA', 'Advance Authorisation', 'Annual Advance Authorisation', 'None'], 0,
          'Actual user for AA. In practice: DFIA traded.', 'c3', T3),
        Q('m6', 'EPCG specific export obligation is:', ['Six times duty saved in six years', 'Eight times in eight years', 'Four times in four years', 'Equal to duty saved'], 0,
          'EPCG rule. In practice: plus average EO.', 'c4', T4),
        Q('m7', 'EOUs must be:', ['Positive net foreign exchange earners', 'Located in SEZs', 'Exempt from GST on DTA sales', 'Export 50% of output'], 0,
          'NFE in 5-year blocks. In practice: monitored.', 'c4', T4),
        Q('m8', 'Mandatory spares under Advance Authorisation are allowed up to:', ['Ten percent of CIF value', 'Five percent', 'Twenty percent', 'Fifteen percent'], 0,
          'Spares rule. In practice: shipped with exports.', 'c3', T3),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Value addition', 2, 'computation', '15%', nums=[va]), S('s2', 'EO imported', 2, 'computation', '6 times', nums=[eo1]), S('s3', 'EO indigenous', 2, 'computation', '4.5', nums=[eo2, tot])],
          ['State period.'], ['Applying 6 times to indigenous goods.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Total', 1, 'computation', '5 million'), S('s2', 'Category', 2, 'analysis', 'One Star')],
          ['Show threshold.'], ['Using only the current year.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is the actual user condition?', 'Inputs imported under the authorisation must be used by the holder in its own manufacture; they stay non-transferred to others even after export.',
          [P('p1', 'Own manufacture', 5, 'own manufacture'), P('p2', 'Non-transferred', 5, 'non-transferred')], 'c3'),
        V('v2', 'What is the role of ITC (HS)?', 'It classifies items for export and import and states whether each is free, restricted or prohibited.',
          [P('p1', 'Restricted', 5, 'restricted'), P('p2', 'Prohibited', 5, 'prohibited')], 'c1'),
        V('v3', 'Why do deemed exports exist?', 'To give domestic suppliers a level playing field against foreign suppliers for specified supplies within India.',
          [P('p1', 'Level playing field', 5, 'level playing field'), P('p2', 'Domestic suppliers', 5, 'domestic suppliers')], 'c4'),
        V('v4', 'What is an AEO?', 'A business certified by Customs as compliant and secure under the WCO SAFE framework, entitled to faster clearances.',
          [P('p1', 'Compliant', 5, 'compliant'), P('p2', 'SAFE', 5, 'safe')], 'c2'),
        V('v5', 'How is EPCG average export obligation set?', 'As the average exports of the applicant in the preceding three licensing years, maintained every year.',
          [P('p1', 'Average', 5, 'average'), P('p2', 'Three licensing years', 5, 'three licensing years')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Inputs supplied free by buyer', 'difficulty': 'moderate',
              'case': 'Under an Advance Authorisation, CIF value of imported inputs is ₹40 lakh; the foreign buyer also supplies inputs worth ₹10 lakh free. FOB value of exports realised is ₹48 lakh (excluding the free inputs).',
              'mcqs': [
                  M('k1a', 'Value of inputs for value addition (₹ lakh):', ['50', '40', '10', '48'], 0,
                    'Add notional free inputs. In practice: both sides.', 'moderate', check=50, topic=T3),
                  M('k1b', 'Export value for value addition (₹ lakh):', ['58', '48', '50', '38'], 0,
                    '48 + 10 notional. In practice: realisation excludes notional.', 'moderate', check=58, topic=T3),
                  M('k1c', 'Value addition achieved (%):', ['16', '20', '15', '12'], 0,
                    '(58 − 50)/50. In practice: minimum met.', 'moderate', check=16, topic=T3),
                  M('k1d', 'Can the imported inputs be sold locally?', ['No, actual user condition applies', 'Yes, freely', 'Yes, after a year', 'Only to EOUs'], 0,
                    'Non-transferable. In practice: even after export.', 'moderate', topic=T3),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ii-ch08', 1, 'Foreign Trade Policy',
                ['Explain the framework and administration of FTP 2023.',
                 'Apply status holder recognition and facilitation measures.',
                 'Apply Advance Authorisation and DFIA provisions.',
                 'Apply EPCG, EOU and deemed export provisions.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p5-ii-ch07-u01'],
                 'exam_tip': 'Memorise the scheme numbers: 15% and 20% value addition, 6 times in 6 years, 24 and 12 months validity.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['FT(D&R) Act 1992; FTP 2023 from 1 April 2023; DGFT.', 'IEC needed; ITC (HS) free/restricted/prohibited.', 'Status: 3/15/50/200/800 US$ million.',
                             'AA: 15% VA, actual user, 12 months; DFIA: 20% VA, transferable.', 'EPCG: 6 times in 6 years; indigenous 4.5 times; 24 months validity.'],
                 'remember': ['EOU must be positive NFE in 5-year blocks.'],
                 'traps': ['Treating Advance Authorisation as transferable.']},
                [('Act', 'FT(D&R) Act 1992'), ('Status', 'Export houses'), ('AA', 'Duty-free inputs'), ('DFIA', 'Transferable'), ('EPCG', 'Capital goods')],
                viva, cases)
