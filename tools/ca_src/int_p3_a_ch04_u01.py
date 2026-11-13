"""CA Intermediate · Paper 3A Income-tax Law · Chapter 4 Income of Other Persons included in Total Income of Assessee (Income-tax Act, 2025; tax year 2026-27).
Scope follows the ICAI study material; section numbers are taken from it; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-a-ch04-u01'
T1 = 'Purpose of clubbing; transfer of income without asset (s. 96)'
T2 = 'Revocable transfers (ss. 97-98)'
T3 = 'Spouse: remuneration from a concern with substantial interest (s. 99(1)(a)(i))'
T4 = 'Spouse and son\'s wife: assets transferred without adequate consideration (s. 99(1)(a)(ii), (b), (2))'
T5 = 'Minor child (s. 99(1)(c)) and the ₹1,500 exemption'
T6 = 'Transfers for benefit of spouse or son\'s wife (s. 99(1)(d)) and cross transfers'
T7 = 'Conversion of self-acquired property into HUF property (s. 99(3)); income includes loss'


def build():
    # i1 — proportionate clubbing where a gift is invested in business
    ck = Checks()
    d = ck.add('800000+1200000', 'Total investment on the first day of the tax year (own + gifted)')
    club = ck.add('900000*1200000/2000000', 'Clubbed = profit × gifted capital ÷ total investment')
    own = ck.add('900000-540000', 'Profit remaining with the transferee')
    i1 = {'id': 'i1', 'title': 'A gift from father-in-law put into business', 'difficulty': 'core', 'minutes': 7,
          'q': 'On 10 March 2026 Mr. Dinesh gifts ₹12,00,000 to his daughter-in-law Anjali. On 1 April 2026 Anjali\'s boutique business has her own capital of ₹8,00,000 plus the ₹12,00,000 gift. The business earns ₹9,00,000 in tax year 2026-27. How much is included in Mr. Dinesh\'s income, and would the answer change if the ₹12,00,000 were a genuine loan?',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Total investment on 1 April 2026 (D)', '8,00,000 + 12,00,000', inr(d)],
              ['Gifted asset invested (C)', '', inr(1200000)],
              ['Business income (B)', '', inr(900000)],
              ['Included in Mr. Dinesh\'s income', 'B × C ÷ D = 9,00,000 × 12 ÷ 20', inr(club)],
              ['Taxed in Anjali\'s hands', '', inr(own)]], title='Section 99(1)(b) with 99(2)'),
              p('A genuine loan is consideration-backed, so no clubbing arises. The gift itself is not taxable for Anjali under section 92(2)(m) because a father-in-law is a relative.')],
          'checks': list(ck)}

    # i2 — minor child income with the ₹1,500 exemption (optional regime)
    ck2 = Checks()
    son = ck2.add('18000-1500', 'Son: FD interest less ₹1,500')
    dau = ck2.add('1200-1200', 'Daughter: bank interest ₹1,200 fully exempt (below ₹1,500)')
    tot = ck2.add('16500+0', 'Included in Mr. Gupta\'s income')
    i2 = {'id': 'i2', 'title': 'Two minor children, one talented', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Mr. Gupta (income ₹14,00,000) and Mrs. Gupta (income ₹9,00,000) both opt out of the default regime. Their minor son earns FD interest of ₹18,000 on a deposit gifted by his grandfather. Their minor daughter earns ₹60,000 from singing performances and ₹1,200 interest on a deposit made from that income. Compute the amount to be clubbed.',
          'solution': [table(['Child', 'Income', 'Treatment', 'Clubbed ₹'], [
              ['Son', 'FD interest 18,000', 'All minor\'s income is clubbed; less ₹1,500', inr(son)],
              ['Daughter', 'Singing 60,000', 'Income from her own skill and talent — taxed in her hands, not clubbed', '—'],
              ['Daughter', 'Bank interest 1,200', 'Interest is clubbed even though the deposit came from talent income; fully exempt as below ₹1,500', inr(dau)],
              ['Total in Mr. Gupta\'s hands (higher income parent)', '', '', inr(tot)]], title='Section 99(1)(c)'),
              note('The ₹1,500-per-child exemption under Schedule III (Table: S. No. 17) is available only because the parent has opted out of the default regime.')],
          'checks': list(ck2)}

    # i3 — both spouses with substantial interest
    ck3 = Checks()
    mr = 700000
    sal_m = ck3.add('70000*12-75000', 'Mr. Vikas\'s salary after standard deduction (default regime)')
    sal_w = ck3.add('40000*12-75000', 'Mrs. Vikas\'s salary after standard deduction')
    gti_m = ck3.add('765000+700000+405000', 'Mr. Vikas: own salary + other income + wife\'s salary clubbed')
    i3 = {'id': 'i3', 'title': 'Both spouses hold a substantial interest', 'difficulty': 'hard', 'minutes': 8,
          'q': 'Mr. and Mrs. Vikas hold 12% and 10% of the equity of Yamuna Agro Pvt. Ltd. Both work there without technical or professional qualifications at monthly salaries of ₹70,000 and ₹40,000. Mr. Vikas\'s other income is ₹7,00,000 and Mrs. Vikas\'s is ₹8,00,000. Both follow the default regime (standard deduction ₹75,000). Compute their gross total incomes.',
          'solution': [p('Together they hold 22% with relatives, so each has a substantial interest. With neither qualified, both salaries are clubbed in the hands of the spouse whose total income before inclusion is higher.'),
                       table(['Item', 'Mr. Vikas ₹', 'Mrs. Vikas ₹'], [
                           ['Own salary (net of standard deduction)', inr(sal_m), inr(sal_w)],
                           ['Other income', inr(mr), inr(800000)],
                           ['Income before clubbing', inr(1465000), inr(1205000)]], title='Who has higher income?'),
                       p(f'Mr. Vikas\'s income before clubbing (₹14,65,000) is higher, so Mrs. Vikas\'s salary is clubbed in his hands: his GTI = 7,65,000 + 7,00,000 + 4,05,000 = ₹18,70,000; Mrs. Vikas\'s GTI = her other income ₹8,00,000.'),
                       note(f'Had Mrs. Vikas\'s income been higher, his salary would have gone to her instead. Once chosen, the same spouse continues in later years unless the Assessing Officer decides otherwise after hearing the other.')],
          'checks': list(ck3)}

    summ = table(['Section', 'Situation', 'Clubbed in hands of'], [
        ['96', 'Income transferred without transferring the asset', 'Transferor'],
        ['97(1)', 'Revocable transfer of assets', 'Transferor'],
        ['99(1)(a)(i)', 'Spouse paid by a business where the individual holds a substantial interest (unless due to spouse\'s technical/professional qualification)', 'Individual; if both have substantial interest, spouse with higher income'],
        ['99(1)(a)(ii)', 'Asset (not house property) transferred to spouse without adequate consideration, not under agreement to live apart', 'Transferor spouse'],
        ['99(1)(b)', 'Asset transferred to son\'s wife without adequate consideration', 'Transferor'],
        ['99(1)(c)', 'Minor child\'s income (except own work/skill, or disability under s. 154)', 'Parent with higher income (or parent maintaining the child)'],
        ['99(1)(d)', 'Asset transferred to any person/AOP for benefit of spouse or son\'s wife', 'Transferor, to the extent of benefit'],
        ['99(3)', 'Self-acquired property converted into HUF property', 'Individual']], title='Clubbing at a glance')

    concepts = [
        C('c1', T1, [
            'Because individuals are taxed at progressive slab rates, people may try to shift income to family members with lower income. Clubbing provisions (sections 96–100) tax such income in the transferor\'s hands.',
            'Section 96: if a person transfers the income from an asset without transferring the asset, the income remains taxable in the transferor\'s hands — whether the transfer is revocable or not.'],
          'You cannot give away the fruit and keep the tree for tax purposes.',
          'Assigning rent of a shop to a brother while keeping the shop leaves the rent taxable for the owner.',
          blocks=[summ]),
        C('c2', T2, [
            'Section 97(1): all income from a revocable transfer of assets is taxed in the transferor\'s hands. "Transfer" includes any settlement, trust, covenant, agreement or arrangement (s. 98).',
            'A transfer is revocable if it provides for re-transfer of the income or asset to the transferor, or gives the transferor a right to re-assume power over it.',
            'Exception (s. 97(2)): a trust not revocable during the beneficiary\'s lifetime, or any other transfer not revocable during the transferee\'s lifetime, provided the transferor derives no direct or indirect benefit. Clubbing applies from when the power to revoke arises.'],
          'If you can take it back, it was never really given away.',
          'A trust that can be revoked after five years is clubbed from the date the power to revoke arises.'),
        C('c3', T3, [
            'Salary, commission, fees or any other pay (cash or kind) that a spouse gets from a business where the individual holds a substantial interest is added to the individual\'s income.',
            'Substantial interest: in a company, equity shares carrying 20% or more of voting power held beneficially by the individual alone or with relatives; in other concerns, entitlement to 20% or more of profits, alone or with relatives, at any time in the year.',
            'No clubbing if the remuneration is solely attributable to the spouse\'s technical or professional knowledge, experience and qualification.',
            'If both spouses have a substantial interest and both earn remuneration, it is clubbed in the hands of the spouse whose total income before inclusion is greater; the same spouse continues later unless the Assessing Officer decides otherwise after a hearing.'],
          'Paying an unqualified spouse a salary from your own company does not split your income.',
          'A wife who is a qualified chartered accountant working as CFO of her husband\'s company keeps her salary in her own hands.'),
        C('c4', T4, [
            'Spouse: income from an asset (other than house property) transferred directly or indirectly without adequate consideration — and not under an agreement to live apart — is clubbed with the transferor. For house property, section 25(a) makes the transferor the deemed owner instead.',
            'Son\'s wife: income from any asset transferred without adequate consideration by her father-in-law or mother-in-law is clubbed with the transferor.',
            'Natural love and affection is not adequate consideration. Income from the accretion (reinvested income) is not clubbed; only income from the transferred asset itself.',
            'If the transferred asset is invested in a business or as capital in a firm (s. 99(2)): clubbed income = income from the business or interest from the firm × value of transferred asset invested ÷ total investment, both on the first day of the tax year.',
            'Clubbing applies only while the relationship exists — not for transfers before marriage or after divorce.'],
          'A gift within the family moves the asset, but its income still follows the giver.',
          'Interest on bonds gifted to a wife is clubbed; interest on an FD she makes from that interest is not.'),
        C('c5', T5, [
            'All income of a minor child is clubbed with the parent whose total income (before inclusion) is greater; if the marriage does not subsist, with the parent who maintains the child. "Child" includes step-child and adopted child (s. 2(25)).',
            'Not clubbed: income from manual work done by the child, income from activities involving the child\'s skill, talent or specialised knowledge, and all income of a child with a disability specified in section 154. Income from investing such talent income is clubbed.',
            'Exemption of up to ₹1,500 per child (Schedule III, Table S. No. 17) is available only to a parent who opts out of the default regime.',
            'A house property transferred to a minor child (other than a minor married daughter) makes the parent the deemed owner under section 25(a), so it is taxed directly, not clubbed, and the ₹1,500 exemption cannot apply. Clubbing covers a minor married daughter too.'],
          'A child\'s own sweat and talent stay with the child; the rest of their income is the parent\'s.',
          'Prize money from a chess championship won by a 14-year-old is taxed in the child\'s hands.'),
        C('c6', T6, [
            'Section 99(1)(d): income from assets transferred without adequate consideration to any person or AOP is clubbed with the transferor to the extent it is for the immediate or deferred benefit of the spouse or son\'s wife.',
            'Cross transfers: where two persons make interconnected gifts to each other\'s spouse or child to avoid clubbing, each is treated as the indirect transferor, and income is clubbed to the extent of the cross transfer (Supreme Court in Keshavji Morarji).'],
          'Routing a gift through a third party or a cousin does not break the chain.',
          'Two brothers each gifting ₹5 lakh to the other\'s wife are treated as gifting to their own wives.'),
        C('c7', T7, [
            'Section 99(3): if an individual converts self-acquired property into HUF property — by impressing it with family character, throwing it into the common stock, or transferring it without adequate consideration — income from it continues to be taxed in the individual\'s hands.',
            'On partition, income from the converted property received by the spouse is clubbed with the individual under section 99(1)(a); a minor child\'s share is clubbed under section 99(1)(c).',
            'Income includes loss (s. 99(5)): if clubbed income is a loss, it is included in the transferor\'s computation.',
            'Section 97 covers revocable transfers by any person; section 99 covers transfers, revocable or not, by individuals only. The transferee whose income is clubbed can be required to pay the tax relating to it (s. 100).'],
          'Moving property into the family pool does not move its income out of your return.',
          'A loss from a business funded by a gift to the spouse also reduces the transferor\'s income.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Family tax review', 'role': 'Tax associate',
         'situation': 'A client has gifted funds to his wife and daughter-in-law and pays his wife a salary from his firm.',
         'steps': ['List each transfer with date, value and consideration.', 'Check substantial interest and the wife\'s qualifications.', 'Apply proportionate clubbing where gifts were invested in business.', 'Exclude income from accretion; note gift-tax position under s. 92(2)(m).'],
         'takeaway': 'Map every family transfer before computing any return.'},
        {'id': 'j2', 'title': 'Minor child\'s income', 'role': 'Article assistant',
         'situation': 'A parent asks whether a child actor\'s earnings and savings interest must be clubbed.',
         'steps': ['Separate talent income from investment income.', 'Identify the parent with higher income.', 'Apply ₹1,500 exemption only if that parent opts out of the default regime.'],
         'takeaway': 'Talent income stays with the child; interest on it does not.'},
    ]

    mcqs = [
        Q('m1', 'Mr. Karan assigns the rent of his shop to his sister but keeps the shop. The rent is taxable in the hands of:', ['Mr. Karan', 'His sister', 'Both equally', 'Neither'], 0,
          'Section 96 clubs income transferred without transferring the asset with the transferor, whether the transfer is revocable or irrevocable. The sister is not the owner, so the rent stays with Mr. Karan. In practice: transfer the asset if income is to move.', 'c1', T1),
        Q('m2', 'A transfer is deemed revocable if it:', ['Gives the transferor a right to re-assume power over the asset or income', 'Is made by registered deed', 'Is made to a relative', 'Is made for adequate consideration'], 0,
          'Section 98 treats a transfer as revocable if it provides for re-transfer to the transferor or lets him re-assume power, directly or indirectly, over the income or asset. Registration or the identity of the transferee does not decide it. In practice: read the trust deed.', 'c2', T2),
        Q('m3', 'Substantial interest in a company for clubbing means holding equity with voting power of at least:', ['20%, alone or with relatives', '10% held personally', '26% held personally', '51% held personally'], 0,
          'An individual has substantial interest if he, alone or together with relatives, beneficially owns equity shares carrying 20% or more of voting power at any time in the year; for other concerns, 20% of profits. In practice: add relatives\' holdings.', 'c3', T3, 'core'),
        Q('m4', 'A wife works in her husband\'s company (he holds 35%) as an engineer with relevant qualifications. Her salary is:', ['Taxable in her own hands', 'Clubbed with the husband', 'Exempt', 'Split equally'], 0,
          'Clubbing of spouse\'s remuneration does not apply where it is solely attributable to her technical or professional knowledge, experience and qualification. Her engineering qualification fits the role. In practice: keep evidence of qualification and duties.', 'c3', T3),
        Q('m5', 'Mr. Joseph gifts bonds to his wife; she earns ₹20,000 interest and invests it in an FD earning ₹1,600. Amount clubbed with Mr. Joseph:', ['₹20,000', '₹21,600', '₹1,600', 'Nil'], 0,
          'Income from the transferred asset (bond interest) is clubbed, but income from the accretion — interest on reinvested income — is not, so ₹20,000 is clubbed and ₹1,600 is taxed in her hands. In practice: track reinvested amounts separately.', 'c4', T4, 'moderate', check=20000),
        Q('m6', 'Gift of ₹6,00,000 invested in son\'s wife\'s business; her own capital ₹4,00,000 on the first day of the tax year; profit ₹5,00,000. Clubbed with the father-in-law:', ['₹3,00,000', '₹5,00,000', '₹2,00,000', 'Nil'], 0,
          'Section 99(2) clubs income × gifted amount ÷ total investment on the first day of the year = 5,00,000 × 6 ÷ 10 = ₹3,00,000. The rest stays with her. In practice: use opening values, not average balances.', 'c4', T4, 'hard', check=300000),
        Q('m7', 'Rohit gifts shares to his fiancée; they marry six months later. Dividend after marriage is:', ['Not clubbed, as she was not his wife at the time of transfer', 'Clubbed from the date of marriage', 'Clubbed for the whole year', 'Exempt'], 0,
          'Section 99(1)(a)(ii) requires the transferee to be the spouse when the asset is transferred; a pre-marriage gift is outside it, so dividends stay with her. In practice: timing of the transfer matters.', 'c4', T4, 'moderate'),
        Q('m8', 'A house property gifted by a husband to his wife (not under an agreement to live apart) is taxed:', ['In the husband\'s hands as deemed owner under section 25', 'In the wife\'s hands', 'Under clubbing of minor\'s income', 'Not at all'], 0,
          'For house property, section 25(a) makes the transferring spouse the deemed owner, so the annual value is taxed directly in his hands; the clubbing provision for other assets does not apply. In practice: the same rule covers gifts to a minor child (not a minor married daughter).', 'c4', T4),
        Q('m9', 'Income of a minor child from a dance performance is:', ['Taxable in the child\'s own hands', 'Clubbed with the higher-income parent', 'Clubbed with the mother', 'Exempt'], 0,
          'Income from activities involving the child\'s skill, talent or specialised knowledge is excluded from clubbing and is assessed in the child\'s hands. Investment income earned from it is clubbed. In practice: a guardian files the child\'s return.', 'c5', T5),
        Q('m10', 'The ₹1,500 per child exemption for clubbed minor income is available:', ['Only if the parent opts out of the default regime', 'Under both regimes', 'Only under the default regime', 'Only for a disabled child'], 0,
          'Schedule III (Table S. No. 17) gives up to ₹1,500 per child, but the exemption is not available to a parent computing tax under the default regime of section 202(1). In practice: it matters only at the margin.', 'c5', T5),
        Q('m11', 'Where the parents\' marriage does not subsist, a minor\'s income is clubbed with:', ['The parent who maintains the child', 'The father always', 'The parent with higher income', 'The mother always'], 0,
          'If the marriage subsists, the higher-income parent; if not, the parent who maintains the minor during the year. In practice: maintenance is a question of fact.', 'c5', T5),
        Q('m12', 'Two friends each gift ₹4 lakh to the other\'s wife at the same time. This is:', ['A cross transfer; income is clubbed with each husband as indirect transferor', 'Not covered by clubbing', 'A revocable transfer', 'Taxed only as a gift'], 0,
          'Interconnected gifts that act as consideration for each other are cross transfers; courts treat each person as the indirect transferor to his own spouse, so income is clubbed to the extent of the cross transfer. In practice: substance prevails over form.', 'c6', T6),
        Q('m13', 'Income from self-acquired property converted into HUF property is taxed in the hands of:', ['The individual who converted it', 'The HUF', 'The Karta', 'All members equally'], 0,
          'Section 99(3) keeps such income in the individual\'s total income and excludes it from the HUF\'s. On partition, the spouse\'s share is clubbed too. In practice: conversion gives no tax saving.', 'c7', T7),
        Q('m14', 'If the clubbed amount is a loss, it:', ['Is included in the transferor\'s income as a loss', 'Is ignored', 'Stays with the transferee', 'Is carried forward by the transferee'], 0,
          'Section 99(5) provides that income includes loss, so a loss from a clubbed source reduces the transferor\'s total income, following the set-off rules. In practice: clubbing can help as well as hurt.', 'c7', T7),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Total investment on first day', 1, 'computation', 'first day|total investment', nums=[d]),
           S('s2', 'Proportionate clubbing', 2, 'computation', '99(2)|proportion', nums=[club]),
           S('s3', 'Loan alternative', 1, 'concept', 'loan')],
          ['Use first-day values.'], ['Clubbing the whole profit.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Higher-income parent', 1, 'concept', 'higher'),
           S('s2', 'Talent income excluded', 1, 'concept', 'talent|skill'),
           S('s3', 'Interest clubbed with exemption', 2, 'computation', '1,500', nums=[son, tot])],
          ['Separate talent and investment income.'], ['Clubbing the singing income.'], ['Table.'], pad='table', checks=list(ck2)),
        W('q3', 5, i3['q'], i3['solution'],
          [S('s1', 'Substantial interest with relatives', 1, 'concept', '20%|substantial'),
           S('s2', 'Incomes before clubbing', 2, 'computation', 'before', nums=[sal_m, sal_w]),
           S('s3', 'Clubbed in higher-income spouse', 2, 'computation', 'higher', nums=[gti_m])],
          ['Compare incomes before inclusion.'], ['Clubbing each salary separately.'], ['Table + working.'], pad='table', checks=list(ck3)),
    ]

    viva = [
        V('v1', 'Why do clubbing provisions exist?',
          'To stop individuals from reducing tax under the slab system by diverting income or income-earning assets to family members with lower income.',
          [P('p1', 'Prevent diversion', 6, 'divert|shift|avoid'), P('p2', 'Progressive slabs', 4, 'slab|progressive')], 'c1'),
        V('v2', 'When is a minor\'s income not clubbed?',
          'When it arises from manual work done by the child, from activities using the child\'s skill, talent or specialised knowledge, or when the child has a disability specified in section 154.',
          [P('p1', 'Manual work', 3, 'manual|work'), P('p2', 'Skill or talent', 4, 'skill|talent'), P('p3', 'Disability', 3, 'disab')], 'c5'),
        V('v3', 'How is proportionate clubbing worked out where a gifted asset is put into business?',
          'Clubbed income equals the business income or interest multiplied by the value of the gifted asset invested and divided by the total investment, both taken on the first day of the tax year.',
          [P('p1', 'Proportion formula', 6, 'multipl|ratio|proportion|divided'), P('p2', 'First day of tax year', 4, 'first day')], 'c4'),
        V('v4', 'What is substantial interest for clubbing?',
          'Holding, alone or with relatives, equity shares carrying at least 20% of voting power in a company, or a right to at least 20% of profits in any other concern.',
          [P('p1', '20%', 6, '20'), P('p2', 'With relatives', 4, 'relative')], 'c3'),
        V('v5', 'Is income from accretion to a gifted asset clubbed?',
          'Only the income of the transferred asset is clubbed; the accretion, that is income produced by reinvesting it, is assessed with the transferee, except for a minor child, whose whole income is clubbed.',
          [P('p1', 'Accretion excluded', 6, 'reinvest|accretion'), P('p2', 'Minor exception', 4, 'minor')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'The Mehra family', 'difficulty': 'moderate',
              'case': 'Mr. Mehra (income ₹20 lakh) gifted ₹10 lakh of bonds to his wife (interest ₹80,000) and a flat to his minor son (rent ₹2,40,000 a year). His wife reinvested the bond interest in an FD that earned ₹4,000. His wife (income ₹6 lakh) works in his company, where he holds 40%, as a receptionist without special qualification, at ₹3,00,000 a year. Both opt out of the default regime.',
              'mcqs': [
                  M('k1a', 'The bond interest and FD interest are treated as follows:', ['₹80,000 clubbed; ₹4,000 taxed in wife\'s hands', 'Both clubbed', 'Neither clubbed', 'Only ₹4,000 clubbed'], 0,
                    'Income from the transferred asset is clubbed with the transferring husband, but income from reinvesting that income is accretion and stays with the wife. In practice: track reinvestment separately.', 'core', topic=T4),
                  M('k1b', 'The rent from the flat gifted to the minor son is:', ['Taxed in Mr. Mehra\'s hands as deemed owner under section 25', 'Clubbed with ₹1,500 exemption', 'Taxed in the son\'s hands', 'Exempt'], 0,
                    'A house property transferred to a minor child (not a minor married daughter) without adequate consideration makes the transferor the deemed owner, so income from house property is taxed directly in his hands, without the ₹1,500 exemption. In practice: compute it under house property.', 'moderate', topic=T5),
                  M('k1c', 'The wife\'s salary of ₹3,00,000 is:', ['Clubbed with Mr. Mehra', 'Taxed in her hands', 'Exempt', 'Clubbed with the son'], 0,
                    'Mr. Mehra holds a substantial interest (40%) and her remuneration is not due to technical or professional qualification, so section 99(1)(a)(i) clubs it with his income. In practice: a qualified role would change this.', 'core', topic=T3),
                  M('k1d', 'Amount clubbed with Mr. Mehra in respect of his wife:', ['₹3,80,000', '₹3,84,000', '₹80,000', '₹3,00,000'], 0,
                    'Clubbed items are her salary ₹3,00,000 and bond interest ₹80,000 = ₹3,80,000; the FD interest of ₹4,000 is accretion and not clubbed. In practice: present a separate clubbing schedule in the return.', 'hard', check=380000, topic=T4),
              ]}]

    return unit(UID, 'p3', 'int-p3-a-ch04', 1, 'Income of Other Persons included in Total Income of Assessee',
                ['Explain why clubbing provisions exist and apply sections 96–98.',
                 'Club remuneration and asset income of the spouse and son\'s wife, including proportionate clubbing.',
                 'Club a minor child\'s income and apply the ₹1,500 exemption.',
                 'Apply clubbing to transfers for the benefit of spouse or son\'s wife, cross transfers and HUF conversions.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 40}, 'prereq': ['int-p3-a-ch03-u05'],
                 'exam_tip': 'Identify the relationship and the nature of income first; then apply the right sub-clause of section 99, the first-day proportion rule and the ₹1,500 exemption (optional regime only).'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['s. 96: income without asset → transferor.', 's. 97: revocable transfer → transferor; exceptions for life-long irrevocable transfers.',
                             's. 99(1)(a)(i): spouse remuneration from substantial-interest concern (20%) unless qualified.', 's. 99(1)(a)(ii), (b): assets to spouse or son\'s wife without adequate consideration.',
                             's. 99(2): proportionate clubbing on first-day investment.', 's. 99(1)(c): minor\'s income → higher-income parent; ₹1,500 exemption only outside default regime.',
                             's. 99(1)(d), cross transfers, s. 99(3) HUF conversion; income includes loss.'],
                 'remember': ['House property gifts to spouse/minor → s. 25 deemed ownership.', 'Accretion is not clubbed (except minor).'],
                 'traps': ['Pre-marriage gifts are not clubbed.', 'Talent income of a minor stays with the minor.']},
                [('Substantial interest', '20% votes/profits'), ('Minor exemption', '₹1,500 per child (optional regime)'), ('s. 99(2)', 'B × C ÷ D'), ('House to spouse', 's. 25(a)')],
                viva, cases,
                topics=['Structured Sectional Learning', 'Introduction', 'Income of Other Persons Includible in Total Income of Assessee', 'Income of Other Persons Includible in Total Income of Individual',
                        'Cross Transfers', 'Conversion of Self-Acquired Property into the Property of a Hindu Undivided Family', 'Income Includes Loss', 'Distinction between Section 96, 97 and Section 99'])
