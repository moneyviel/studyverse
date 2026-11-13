"""CA Final · Paper 4 · Chapter 6 Income of Other Persons included in Total Income of Assessee.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch06-u01'
T1 = 'Transfers of income and revocable transfers'
T2 = 'Clubbing of spouse and son\'s wife income'
T3 = 'Clubbing of minor child\'s income'
T4 = 'HUF conversions, deemed ownership and recovery'


def build():
    ck = Checks()
    cl = ck.add('500000*1000000/(1000000+1500000)', 'Profit clubbed with husband (₹)')
    ow = ck.add('500000-500000*1000000/(1000000+1500000)', 'Profit taxed in wife\'s hands (₹)')
    i1 = {'id': 'i1', 'title': 'Gifted money invested in spouse\'s business', 'difficulty': 'core', 'minutes': 6,
          'q': 'Vikram gifted ₹10,00,000 to his wife Anjali, who invested it with ₹15,00,000 of her own money in her proprietary boutique; the amounts stood so on 1 April 2026. The boutique earned ₹5,00,000 in T.Y. 2026-27. How much is clubbed?',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Proportion', '10,00,000 ÷ 25,00,000 (values on first day of the year)', '40%'],
              ['Clubbed with Vikram', '5,00,000 × 40%', inr(cl)],
              ['Taxed in Anjali\'s hands', 'Balance', inr(ow)]], title='Section 99(2)')],
          'checks': list(ck)}

    c2 = Checks()
    op = c2.add('4000-1500+0', 'Clubbed income of child A under optional regime (₹)')
    ob = c2.add('1200-1200', 'Clubbed income of child B under optional regime (₹)')
    dr = c2.add('4000+1200', 'Clubbed under default regime (₹)')
    i2 = {'id': 'i2', 'title': 'Three minor children', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Arun (total income ₹12,00,000) and Bela (₹8,00,000) are married. Their minor children earned in T.Y. 2026-27: child A, interest on a gifted FD ₹4,000; child B, savings interest ₹1,200; child C, ₹20,000 prize won in a singing contest. Compute the amount clubbed if Arun (i) opts out of the default regime; (ii) stays in it.',
          'solution': [table(['Child', 'Treatment', '₹'], [
              ['A — optional regime', '4,000 − 1,500 exemption', inr(op)],
              ['B — optional regime', 'Fully covered by exemption', inr(ob)],
              ['C', 'Skill-based income — not clubbed, taxed in child\'s hands', '—'],
              ['Default regime total', 'No exemption: 4,000 + 1,200', inr(dr)]], title='Clubbed with Arun (higher income)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Sections 96 to 100 prevent tax avoidance by diverting income to family members. Section 96: where income is transferred without transferring the asset, the income remains taxable in the transferor\'s hands, whether the transfer is revocable or not.',
            'Section 97(1): income from a revocable transfer of assets is taxed in the transferor\'s hands. A transfer is revocable if it contains a provision for re-transfer of the income or asset to the transferor or gives him a right to reassume power over it (section 98).',
            'Section 97(2) exception: a trust not revocable during the beneficiary\'s lifetime, or another transfer not revocable during the transferee\'s lifetime, from which the transferor derives no benefit — clubbing applies only when the power to revoke arises.'],
          'Giving away income without the asset changes nothing.',
          'Assigning next year\'s rent to a friend while keeping the flat still taxes the rent in the owner\'s hands.'),
        C('c2', T2, [
            'Section 99(1)(a)(i): remuneration of a spouse from a concern in which the individual has substantial interest (20% voting power or profit share, alone or with relatives) is clubbed with whichever spouse has the greater income before inclusion, unless it is solely due to the spouse\'s technical or professional qualification and experience.',
            'Section 99(1)(a)(ii): income from assets transferred to the spouse without adequate consideration (except under an agreement to live apart) is clubbed with the transferor. Section 99(1)(b) applies the same to a son\'s wife; section 99(1)(d) covers transfers to others for the benefit of spouse or son\'s wife. Income on the accretion (income from accumulated income) is not clubbed.',
            'Section 99(2): where the asset is invested in a business, the clubbed share is the proportion of the transferred asset\'s value on the first day of the year to total investment on that day; for investment in a firm as a partner, the interest from the firm is apportioned similarly. House property gifted to a spouse or minor child is instead deemed owned by the transferor under section 25(a).'],
          'Gifts to spouse or daughter-in-law carry tax back to the giver.',
          '₹10 lakh gifted to a wife and invested with her own ₹15 lakh clubs 40% of the profit.'),
        C('c3', T3, [
            'Section 99(1)(c): all income of a minor child is clubbed with the parent whose income (before inclusion) is greater; if the marriage does not subsist, with the parent maintaining the child. Once included, it stays with that parent unless the AO decides otherwise after a hearing. It applies even to a minor married daughter.',
            'Exceptions: income from manual work by the minor, from activities using the minor\'s skill, talent or specialised knowledge, and income of a minor suffering from a disability specified in section 154. Such income is taxed in the minor\'s own hands.',
            'Schedule III (Sl. No. 17) exempts up to ₹1,500 per child of clubbed income — but only if the parent opts out of the default regime.'],
          'The richer parent pays tax on the child\'s passive income.',
          'Interest of ₹4,000 on a child\'s FD is clubbed at ₹2,500 under the optional regime.'),
        C('c4', T4, [
            'Section 99(3): where an individual converts his separate property into HUF property or throws it into the common stock, income from it is clubbed with the individual. After a partition, income from the share received by his spouse is also clubbed.',
            'Section 25(a) makes a transferor of house property to a spouse (unless the couple has agreed to live apart) or to a minor child who is not a married daughter the deemed owner, so clubbing provisions and the minor-child exemption do not apply to it.',
            'Section 100: tax on clubbed income may be recovered from the transferee, who is liable for the portion of tax attributable to it; joint holders are jointly and severally liable.'],
          'Throwing property into the HUF pot does not shift the tax.',
          'A father who converts his flat into HUF property is still taxed on its rent.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Family tax review', 'role': 'Tax consultant',
             'situation': 'A client has gifted funds to his wife and minor children.',
             'steps': ['Trace each gifted asset and its income.', 'Apply the proportion rule for business investments.', 'Pick the parent with higher income.', 'Check regime choice for the ₹1,500 exemption.'],
             'takeaway': 'Gifts within the family need a clubbing check every year.'}]

    mcqs = [
        Q('m1', 'Income from an asset gifted to one\'s brother is:', ['Taxed in the brother\'s hands', 'Clubbed with the donor', 'Exempt', 'Taxed at thirty percent'], 0,
          'Section 99 does not reach a brother. In practice: the brother pays tax on it.', 'c2', T2),
        Q('m2', 'Substantial interest in a company for clubbing means voting power of at least:', ['Twenty percent', 'Ten percent', 'Fifty percent', 'Twenty-five percent'], 0,
          'Alone or with relatives. In practice: test any time in the year.', 'c2', T2),
        Q('m3', 'Remuneration of a qualified CA spouse from the other spouse\'s firm with substantial interest is:', ['Not clubbed if due to professional qualification', 'Always clubbed', 'Exempt', 'Clubbed only if above ₹1 lakh'], 0,
          'Exception in section 99(1)(a)(i). In practice: document qualification.', 'c2', T2),
        Q('m4', 'Minor child\'s income from performing in concerts is:', ['Taxed in the child\'s hands', 'Clubbed with father', 'Clubbed with mother', 'Exempt fully'], 0,
          'Skill-based exception. In practice: file child\'s return.', 'c3', T3),
        Q('m5', 'The ₹1,500 per child exemption is available only if the parent:', ['Opts out of the default regime', 'Is a senior citizen', 'Has income below ₹5 lakh', 'Is the mother'], 0,
          'Schedule III Sl. No. 17. In practice: compare regimes.', 'c3', T3),
        Q('m6', 'Minor\'s income where parents are married goes to the parent whose income before inclusion is:', ['Greater', 'Lower', 'Equal split', 'Chosen by the child'], 0,
          'Section 99(1)(c). In practice: fixed in later years.', 'c3', T3),
        Q('m7', 'A house gifted to a spouse is taxed in the donor\'s hands because:', ['He is the deemed owner under section 25(a)', 'Section 96 applies', 'It is a revocable transfer', 'The spouse is a minor'], 0,
          'Deemed ownership. In practice: not clubbing.', 'c4', T4),
        Q('m8', 'Income from property thrown into the HUF common stock is taxed in the hands of:', ['The individual who converted it', 'The HUF', 'The karta only', 'All coparceners equally'], 0,
          'Section 99(3). In practice: also after partition for spouse\'s share.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Proportion', 2, 'computation', 'first day'), S('s2', 'Clubbed amount', 3, 'computation', 'clubbed', nums=[cl, ow])],
          ['Use values on first day.'], ['Using year-end balances.'], ['Show ratio.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Exceptions', 2, 'analysis', 'skill'), S('s2', 'Optional regime', 2, 'computation', 'exemption', nums=[op]), S('s3', 'Default regime', 2, 'computation', 'default', nums=[dr])],
          ['State parent selection.'], ['Giving ₹1,500 exemption under default regime.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'When is a transfer revocable?', 'When it provides for re-transfer of the income or asset to the transferor or gives him a right to reassume power over it.',
          [P('p1', 'Re-transfer', 5, 're-transfer|retransfer'), P('p2', 'Reassume power', 5, 'reassume')], 'c1'),
        V('v2', 'Is income from accumulated income of a gifted asset clubbed?', 'It stays with the spouse; only the income from the original asset is clubbed.',
          [P('p1', 'Stays with spouse', 5, 'spouse'), P('p2', 'Original asset', 5, 'original')], 'c2'),
        V('v3', 'Which minor\'s income is taxed in the minor\'s own hands?', 'Income from manual work, from skill or talent, and income of a minor with a specified disability.',
          [P('p1', 'Manual work or skill', 5, 'manual|skill'), P('p2', 'Disability', 5, 'disability')], 'c3'),
        V('v4', 'Who can be served notice for tax on clubbed income?', 'The transferee, who is liable for the tax attributable to the clubbed income.',
          [P('p1', 'Transferee', 5, 'transferee'), P('p2', 'Attributable tax', 5, 'attributable')], 'c4'),
        V('v5', 'How is income clubbed when gifted money is invested in a business?', 'In the ratio of the gifted amount to total investment on the first day of the tax year.',
          [P('p1', 'Ratio', 5, 'ratio|proportion'), P('p2', 'First day', 5, 'first day')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Joshi family', 'difficulty': 'moderate',
              'case': 'Ramesh Joshi holds 30% of the shares of Joshi Textiles Pvt Ltd. His wife Meena, a commerce graduate with no technical qualification, draws a salary of ₹6,00,000 from it. Ramesh\'s own income is ₹18,00,000; Meena has no other income. Ramesh also gifted ₹3,00,000 to his son\'s wife, who earned ₹24,000 interest on it.',
              'mcqs': [
                  M('k1a', 'Meena\'s salary is:', ['Clubbed with Ramesh', 'Taxed in Meena\'s hands', 'Exempt', 'Taxed in the company'], 0,
                    'Substantial interest, no professional qualification. In practice: higher-income spouse.', 'core', topic=T2),
                  M('k1b', 'Amount clubbed from Meena\'s salary (₹):', ['6,00,000', '3,00,000', 'Nil', '1,80,000'], 0,
                    'Whole remuneration. In practice: computed as salary.', 'core', check=600000, topic=T2),
                  M('k1c', 'Interest earned by the son\'s wife (₹) clubbed with Ramesh:', ['24,000', 'Nil', '12,000', '3,00,000'], 0,
                    'Section 99(1)(b). In practice: inadequate consideration.', 'core', check=24000, topic=T2),
                  M('k1d', 'If Meena held an engineering degree applied in the job, the salary would be:', ['Taxed in her hands', 'Clubbed anyway', 'Exempt', 'Split equally'], 0,
                    'Professional qualification exception. In practice: evidence needed.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch06', 1, 'Income of Other Persons included in Total Income of Assessee',
                ['Apply provisions on transfer of income and revocable transfers.',
                 'Club income of spouse and son\'s wife.',
                 'Club income of a minor child and apply the exemption.',
                 'Apply HUF conversion, deemed ownership and recovery provisions.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 35, 'practice': 25}, 'prereq': ['fin-p4-ch05-u01'],
                 'exam_tip': 'Name the relationship and the section first, then compute the clubbed share.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Sections 96–98 transfers and revocability.', 'Section 99(1)(a)/(b)/(d) spouse and son\'s wife.', 'Section 99(1)(c) minor; ₹1,500 exemption only outside default regime.',
                             'Section 99(2) proportion; 99(3) HUF conversion.', 'Section 100 recovery from transferee.'],
                 'remember': ['House property gifts go via section 25(a).'],
                 'traps': ['Clubbing a minor\'s talent income.']},
                [('Revocable transfer', 'Section 97'), ('Clubbing', 'Section 99'), ('Recovery', 'Section 100')],
                viva, cases)
