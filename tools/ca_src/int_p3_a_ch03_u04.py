"""CA Intermediate · Paper 3A Income-tax Law · Chapter 3 Heads of Income · Unit 4 Capital Gains (Income-tax Act, 2025; tax year 2026-27).
Scope follows the ICAI study material; section numbers and limits are taken from it; explanations and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-a-ch03-u04'
T1 = 'Capital asset (s. 2(22))'
T2 = 'Short-term and long-term (s. 2(101), 2(67))'
T3 = 'Transfer and year of charge (ss. 2(109), 67)'
T4 = 'Transactions not regarded as transfer (s. 70)'
T5 = 'Computation, cost of acquisition and improvement (ss. 72, 73, 90)'
T6 = 'Depreciable assets and slump sale (ss. 74, 77)'
T7 = 'Deemed consideration and advance money (ss. 78-81)'
T8 = 'Exemptions and deductions (ss. 82-86)'
T9 = 'Rates of tax (ss. 196-198)'


def build():
    # i1 — land acquired before 23.7.2024: tax with and without indexation
    ck = Checks()
    net = ck.add('7500000-75000', 'Net sale consideration')
    lt = ck.add('7425000-1000000-400000', 'LTCG without indexation (goes into GTI)')
    ta = ck.add('0.125*6025000', 'Tax A @12.5% without indexation')
    icoa = ck.add('round(1000000*390/117)', 'Indexed cost of acquisition')
    icoi = ck.add('400000*390/200', 'Indexed cost of improvement')
    lti = ck.add('7425000-3333333-780000', 'LTCG with indexation')
    tb = ck.add('round(0.20*3311667)', 'Tax B @20% with indexation')
    ex = ck.add('753125-662333', 'Excess tax ignored')
    i1 = {'id': 'i1', 'title': 'Old plot sold — the indexation comparison', 'difficulty': 'hard', 'minutes': 12,
          'q': 'Lakshmi, a resident individual, bought a plot in FY 2005-06 for ₹10,00,000 and built a compound wall in FY 2012-13 for ₹4,00,000. She sells it in September 2026 for ₹75,00,000 (stamp duty value ₹78,00,000), paying brokerage of ₹75,000. Compute the LTCG to be included in total income and the tax on it (ignore cess and basic exemption). CII: 2005-06 = 117, 2012-13 = 200; assume CII for 2026-27 = 390 for this exercise (the actual index had not been notified when the study material was issued).',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Full value of consideration', 'Stamp duty value 78 lakh is within 110% of 75 lakh → actual price', inr(7500000)],
              ['Less brokerage', '', inr(75000)],
              ['Net consideration', '', inr(net)],
              ['Less cost of acquisition and improvement (no indexation)', '10,00,000 + 4,00,000', inr(1400000)],
              ['LTCG included in total income', '', inr(lt)],
              ['Tax A @12.5%', '', inr(ta)],
              ['Indexed cost of acquisition', '10,00,000 × 390/117', inr(icoa)],
              ['Indexed cost of improvement', '4,00,000 × 390/200', inr(icoi)],
              ['LTCG with indexation', '74,25,000 − 33,33,333 − 7,80,000', inr(lti)],
              ['Tax B @20%', '', inr(tb)],
              ['Excess (A − B) ignored', '', inr(ex)],
              ['Tax payable on the LTCG', 'Lower of A and B', inr(tb)]], title='Computation'),
              note('Indexation never changes the income figure in total income; it only caps the tax for land or buildings acquired by a resident individual or HUF before 23 July 2024.')],
          'checks': list(ck)}

    # i2 — capital asset converted into stock-in-trade
    ck2 = Checks()
    cg = ck2.add('4000000-1800000', 'LTCG = FMV on conversion − cost')
    bi = ck2.add('5200000-4000000', 'Business income = sale price − FMV on conversion')
    bond = ck2.add('min(2200000,5000000)', 'Maximum section 85 deduction if whole gain is invested in bonds')
    i2 = {'id': 'i2', 'title': 'Investment land turned into stock', 'difficulty': 'core', 'minutes': 7,
          'q': 'Varun bought land as an investment in June 2021 for ₹18,00,000. On 1 December 2025 he started a real-estate business and converted the land into stock-in-trade; its FMV that day was ₹40,00,000. He sold the plots in January 2027 for ₹52,00,000. Explain the tax treatment and the time limit for a section 85 bond investment.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Year of transfer', 'Conversion on 1.12.2025 (TY 2025-26) is a transfer', '—'],
              ['Year of charge', 'Both incomes fall in TY 2026-27, when the plots are sold', '—'],
              ['Long-term capital gain', 'Held June 2021 to December 2025 (> 24 months): 40,00,000 − 18,00,000', inr(cg)],
              ['Business income', '52,00,000 − 40,00,000', inr(bi)],
              ['Section 85 deduction if he invests ₹22 lakh in notified bonds', 'Lower of gain and investment, within ₹50 lakh', inr(bond)]], title='Treatment'),
              note('For section 85, the six months run from the sale of the converted stock, not from the conversion date (CBDT circular).')],
          'checks': list(ck2)}

    # i3 — residential house: s. 82 two-house option and s. 85 bonds
    ck3 = Checks()
    d82 = ck3.add('7000000+6000000', 'Cost of two new houses (gain ≤ ₹2 crore, two-house option)')
    bal = ck3.add('18000000-13000000', 'LTCG left after s. 82')
    d85 = ck3.add('min(5000000,4000000)', 'Bond investment within 6 months (≤ ₹50 lakh)')
    tx = ck3.add('5000000-4000000', 'Taxable LTCG')
    i3 = {'id': 'i3', 'title': 'Reinvesting gains from a house sale', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Ashok, a resident individual, sells a residential house (owned for 9 years) in July 2026 with LTCG of ₹1,80,00,000. In March 2027 he buys two flats in India costing ₹70,00,000 and ₹60,00,000, and in November 2026 invests ₹40,00,000 in NHAI bonds redeemable after five years. Compute taxable LTCG, assuming he has never used the two-house option before.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['LTCG', '', inr(18000000)],
              ['Less s. 82 (two houses, gain does not exceed ₹2 crore)', '70,00,000 + 60,00,000', inr(d82)],
              ['Balance', '', inr(bal)],
              ['Less s. 85 (bonds within 6 months; cap ₹50 lakh)', '', inr(d85)],
              ['Taxable LTCG', '', inr(tx)]], title='Computation'),
              note('The two-house option can be used only once in a lifetime; once used, later sales qualify only for one house.')],
          'checks': list(ck3)}

    terms = table(['Asset', 'Short-term if held'], [
        ['Listed securities (on a recognised exchange in India), units of UTI, units of equity-oriented funds, zero coupon bonds', 'Up to 12 months'],
        ['Every other capital asset (land, building, unlisted shares, gold, jewellery)', 'Up to 24 months'],
        ['Market linked debentures, unlisted bonds and debentures, and specified mutual fund units bought from 1 April 2023', 'Always short-term (s. 76)']],
        title='Holding-period test')
    rates = table(['Gain', 'Rate'], [
        ['STCG on listed equity shares / equity-oriented fund units with STT (s. 196)', '20%'],
        ['Other STCG', 'Normal slab or entity rates'],
        ['LTCG on listed equity shares (STT on purchase and sale) / equity fund units (STT on sale) (s. 198)', '12.5% on the amount above ₹1,25,000'],
        ['All other LTCG (s. 197)', '12.5% without indexation'],
        ['Land/building bought before 23.7.2024 by resident individual or HUF', 'Lower of 12.5% without and 20% with indexation']],
        title='Rates at a glance')
    ded = table(['Section', 'Who', 'Asset sold', 'Reinvest in', 'Time limit', 'Cap'], [
        ['82', 'Individual/HUF', 'Long-term residential house', 'One house in India (two if gain ≤ ₹2 crore, once in life)', 'Buy 1 yr before/2 yrs after; build in 3 yrs', '₹10 crore'],
        ['83', 'Individual/HUF', 'Urban agricultural land used for agriculture 2 yrs', 'Other agricultural land', '2 years', 'None'],
        ['84', 'Any assessee', 'Land/building of industrial undertaking compulsorily acquired, used 2 yrs', 'Land/building for the undertaking', '3 years', 'None'],
        ['85', 'Any assessee', 'Long-term land or building', 'Notified bonds (NHAI, REC, PFC, IRFC, HUDCO, IREDA) redeemable after 5 yrs', '6 months', '₹50 lakh'],
        ['86', 'Individual/HUF', 'Long-term asset other than a residential house', 'One house in India', 'Buy 1 yr before/2 yrs after; build in 3 yrs', '₹10 crore']],
        title='Reinvestment reliefs')

    concepts = [
        C('c1', T1, [
            'Capital asset [s. 2(22)] means property of any kind held by the assessee, connected with business or not; securities held by FIIs/FPIs and specified investment funds under SEBI or IFSC rules; and taxable ULIPs. "Property" includes rights in an Indian company such as management or control rights.',
            'Excluded: stock-in-trade, consumable stores and raw materials (except securities of FPIs and those funds); personal effects — movable property for personal use of the assessee or a dependent family member; rural agricultural land in India; gold deposit bonds and gold monetisation scheme certificates.',
            'Jewellery, archaeological collections, drawings, paintings, sculptures and works of art are NOT personal effects, so they are capital assets. Jewellery includes ornaments of precious metals and precious or semi-precious stones.',
            'Agricultural land is urban (a capital asset) if within a municipality or cantonment of population 10,000 or more, or within 2 km (population over 10,000 up to 1 lakh), 6 km (over 1 lakh up to 10 lakh) or 8 km (over 10 lakh) measured aerially.'],
          'Whether something is a capital asset depends on how it is held, not on what it is.',
          'A builder\'s unsold flats are stock-in-trade; the same flat held by a salaried buyer as investment is a capital asset.'),
        C('c2', T2, [
            'A short-term capital asset is held for not more than 24 months; for listed securities, UTI units, equity-oriented fund units and zero coupon bonds the limit is 12 months (table). A long-term asset is any other capital asset.',
            'Equity-oriented fund: at least 65% of proceeds in listed domestic equity shares (90%/90% test for fund-of-funds).',
            'Holding periods include the previous owner\'s period for gifts, wills, inheritance and similar modes; amalgamation and demerger shares carry the original holding; equity shares from conversion of preference shares carry the preference period.',
            'They run from allotment for bonus shares, rights shares and ESOP/sweat equity shares, from the offer date for a renounced right, and from the conversion date for stock converted into a capital asset. For shares of a company in liquidation, the period after liquidation is excluded.'],
          'The clock decides the rate: the longer you hold, the gentler the tax.',
          'Listed shares bought on 1 May 2025 and sold on 2 May 2026 are long-term (more than 12 months).',
          blocks=[terms]),
        C('c3', T3, [
            'Transfer [s. 2(109)] includes sale, exchange or relinquishment; extinguishment of rights; compulsory acquisition; conversion of a capital asset into stock-in-trade; maturity of a zero coupon bond; arrangements that enable enjoyment of immovable property (such as society membership); possession given under part performance; and any parting with an interest directly or indirectly.',
            'Section 67 taxes gains in the year of transfer, which is when title effectively passes, not the date of agreement.',
            'Special years: insurance money for destruction by fire, flood, riot or war — year of receipt (FMV of assets received is the consideration); conversion into stock-in-trade — taxed only when that stock is later sold (FMV on conversion is the consideration; sale price less that FMV is business income); compulsory acquisition — year compensation is first received; enhanced compensation — year received, with nil cost; interim-order compensation — year of the final order.',
            'Distribution of assets by a company on liquidation is not a transfer by the company, but shareholders are taxed on the money and FMV of assets received less the deemed dividend portion (s. 68). On a buyback (s. 69) the shareholder is taxed on consideration less cost as capital gains; promoters pay additional tax.'],
          'Capital gains are taxed when ownership really moves, with special clocks where the money comes later.',
          'Compensation for land acquired by the Government is taxed when the first cheque arrives; a later court increase is taxed when received.'),
        C('c4', T4, [
            'Not transfers [s. 70] include: distribution on partition of an HUF; gift, will or irrevocable trust by an individual or HUF; transfer by a company to its wholly owned Indian subsidiary and by a wholly owned subsidiary to its Indian holding company (not stock-in-trade); transfer of assets in an amalgamation or demerger to an Indian company, and shareholders\' exchange of shares under such schemes; conversion of debentures or bonds into shares or debentures of the same company; conversion of preference shares into equity; and redemption of sovereign gold bonds as specified.',
            'Because these are not transfers, the recipient\'s cost and holding period are usually those of the previous owner (s. 73).'],
          'Certain internal reshuffles and family transfers are ignored so that tax arises only on a real disposal later.',
          'Shares received in a merger keep the cost and purchase date of the shares given up.'),
        C('c5', T5, [
            'Capital gain [s. 72] = full value of consideration − expenses wholly for the transfer (brokerage, legal fees, stamp duty paid by seller) − cost of acquisition − cost of improvement. Interest claimed under house property or Chapter VIII and securities transaction tax are not deductible.',
            'Indexation is not used in computing income. For land or buildings acquired before 23 July 2024 by a resident individual or HUF, tax is the lower of 12.5% without indexation and 20% with indexed cost (CII of transfer year ÷ CII of first year held or 2001-02, whichever is later).',
            'Cost for assets acquired by gift, will, inheritance, partition and similar modes is the previous owner\'s cost (s. 73). For assets held before 1 April 2001, the assessee may take FMV on that date, but for land or building not above the stamp duty value on that date.',
            'Bonus shares and self-generated goodwill or brand: cost nil. Rights shares: amount paid; renounced right: cost nil; buyer of a renounced right: price paid for the right plus amount paid to the company.',
            'Listed equity shares or equity fund units acquired before 1 February 2018: cost is the higher of actual cost and the lower of (FMV on 31 January 2018, sale price) — the grandfathering rule.',
            'Cost of improvement covers capital additions on or after 1 April 2001; for goodwill and similar rights it is nil.'],
          'Subtract every rupee that genuinely went into the asset and its sale; the remainder is the gain.',
          'Shares bought in 2016 at ₹100, quoting ₹150 on 31 January 2018 and sold at ₹140, have a cost of ₹140 and no gain.'),
        C('c6', T6, [
            'Depreciable assets in a block [s. 74] are always short-term, whatever the holding period. If sale consideration exceeds opening WDV plus additions plus transfer expenses, the excess is STCG.',
            'If the whole block is sold and the consideration is less than that total, the shortfall is a short-term capital loss; if some assets remain, the shortfall stays as closing WDV.',
            'Power undertakings on straight-line basis take the WDV of the asset as cost (s. 75).',
            'Slump sale [s. 77] — transfer of an undertaking for a lump sum without values assigned to individual assets. Net worth is the cost; consideration is deemed to be FMV computed under Rule 53 (higher of FMV of assets transferred and FMV of consideration). Undertakings held for 36 months or less give STCG; otherwise LTCG. A CA report on net worth must be furnished by the specified date.'],
          'Assets that have been depreciated have had their cost recovered already, so any surplus on sale is treated as a short-term gain.',
          'A trader sells his only computer block for more than its WDV — the excess is a short-term capital gain even after five years of use.'),
        C('c7', T7, [
            'Land or building [s. 78]: if stamp duty value exceeds 110% of consideration, stamp duty value is the full value of consideration. Where agreement and registration dates differ and some consideration was received by banking or online mode on or before the agreement, the value on the agreement date is used. If the assessee disputes the value, the AO may refer to a Valuation Officer, and the lower of that valuation and stamp duty value applies.',
            'Unquoted shares [s. 79]: if consideration is below FMV determined under the rules, FMV is the consideration.',
            'Where consideration cannot be ascertained [s. 80], FMV on the date of transfer is taken.',
            'Advance money [s. 81]: an advance retained on a failed deal before 1 April 2014 reduces the cost of acquisition; one forfeited later is taxed as income from other sources in the year of forfeiture and does not reduce cost. An advance forfeited by a previous owner does not reduce the assessee\'s cost.'],
          'The law replaces an understated price with an objective value when the gap is more than a small tolerance.',
          'A shop sold for ₹1 crore with stamp duty value ₹1.12 crore is taxed on ₹1.12 crore unless part was paid digitally on or before an earlier agreement date when the value was within 110%.'),
        C('c8', T8, [
            'Schedule III exempts gains of an individual or HUF on compulsory acquisition of urban agricultural land used for agriculture for 2 years by them or a parent, where compensation is received on or after 1 April 2004, and awards under the 2013 land acquisition (RFCTLARR) Act (with a stated exception).',
            'Reinvestment deductions (table): the deduction is the lower of gain and amount reinvested, except s. 86, where it is gain × amount invested ÷ net consideration (full gain if the whole net consideration is invested).',
            'Amounts not reinvested before the return is filed must be deposited in the Capital Gains Accounts Scheme by the return due date (only up to ₹10 crore of gain for s. 82 or of net consideration for s. 86); unused deposits are taxed when the reinvestment period ends.',
            'If the new asset is sold within 3 years, its cost is reduced by the earlier deduction (s. 82, 83, 84). Under s. 86 the assessee must not own more than one other house on the date of transfer nor buy another within 2 years or build within 3 years. For s. 85 bonds, sale, conversion or a loan against them within 5 years revives the gain.'],
          'The law forgives the gain if it is ploughed back into the kind of asset the law wants to encourage.',
          'Selling a plot and buying a home with the whole net price clears the entire gain under section 86.',
          blocks=[ded]),
        C('c9', T9, [
            'Rates are summarised in the table. For resident individuals and HUFs, unexhausted basic exemption is set first against special-rate gains; non-residents get no such adjustment.',
            'No Chapter VIII deduction is allowed against STCG under s. 196 or LTCG under ss. 197-198. Rebate u/s 156 is not available against tax on LTCG under s. 198.',
            'Non-residents who bought shares or debentures of an Indian company in foreign currency compute gains in that currency (first proviso relief); it does not apply to s. 198 LTCG.'],
          'Capital gains sit outside the slab ladder at flat rates, with a small tax-free allowance for listed equity.',
          'A resident with ₹2,00,000 of LTCG on listed shares and no other income pays nothing, since the exemption limit absorbs it.',
          blocks=[rates]),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Property sale advisory', 'role': 'Tax associate',
         'situation': 'A client is selling a flat bought in 2012 and wants to minimise tax.',
         'steps': ['Confirm holding period and acquisition date (before 23.7.2024 gives the 12.5%/20% comparison).', 'Check stamp duty value against 110% of price.', 'Model s. 82 (new house) and s. 85 (bonds, 6 months, ₹50 lakh) options.', 'Advise CGAS deposit before the return due date if the house purchase is pending.'],
         'takeaway': 'Timelines drive the relief — note the 6-month, 2-year and 3-year deadlines on day one.'},
        {'id': 'j2', 'title': 'Equity portfolio gains', 'role': 'Article assistant',
         'situation': 'You compute capital gains from a broker\'s annual statement.',
         'steps': ['Split trades into short-term (≤ 12 months) and long-term.', 'Apply grandfathered cost for shares bought before 1.2.2018.', 'Tax STCG with STT at 20%; LTCG above ₹1,25,000 at 12.5%.', 'Set unexhausted basic exemption against these gains for residents.'],
         'takeaway': 'Holding period and grandfathering are where most errors creep in.'},
    ]

    mcqs = [
        Q('m1', 'Which of the following held for personal use is a capital asset?', ['A gold necklace', 'A sofa set', 'A personal car', 'Clothes'], 0,
          'Personal effects (movable property for personal use) are excluded from capital assets, but jewellery, archaeological collections, drawings, paintings, sculptures and works of art are carved out of that exclusion. So a gold necklace is a capital asset. In practice: gains on sale of personal jewellery are taxable.', 'c1', T1),
        Q('m2', 'Agricultural land 5 km (aerially) from a municipality with population 4,00,000 is:', ['A capital asset', 'Not a capital asset', 'A capital asset only if sold to a builder', 'Exempt as agricultural income'], 0,
          'For a municipality with population above 1 lakh up to 10 lakh, land within 6 km aerially is urban and therefore a capital asset. Gains on urban agricultural land are not agricultural income. In practice: confirm census population and distance first.', 'c1', T1, 'moderate'),
        Q('m3', 'Unlisted shares of a company held for 20 months are:', ['A short-term capital asset', 'A long-term capital asset', 'Long-term if held over 12 months', 'Not a capital asset'], 0,
          'The 12-month test applies only to listed securities, UTI units, equity-oriented fund units and zero coupon bonds; unlisted shares fall in the residual 24-month category, so 20 months is short-term. In practice: check listing status on the transfer date.', 'c2', T2),
        Q('m4', 'The holding period of bonus shares is counted from:', ['The date of allotment of the bonus shares', 'The date of purchase of the original shares', '1 April 2001', 'The record date'], 0,
          'For financial assets allotted without payment on the basis of an existing holding, the period runs from allotment. The original shares keep their own purchase date. In practice: brokers usually show allotment dates in statements.', 'c2', T2),
        Q('m5', 'Market linked debentures sold after four years give rise to:', ['Short-term capital gain', 'Long-term capital gain', 'Business income', 'Exempt income'], 0,
          'Section 76 treats gains on market linked debentures, unlisted bonds or debentures, and specified mutual fund units bought from April 2023 as short-term regardless of the holding period. In practice: these are taxed at slab rates.', 'c2', T2, 'moderate'),
        Q('m6', 'Rahul converts listed shares held as investment into stock-in-trade in TY 2025-26 and sells them in TY 2026-27. Capital gains are taxable in:', ['TY 2026-27', 'TY 2025-26', 'Both years equally', 'Never — it is business income'], 0,
          'Conversion is a transfer in the year of conversion, but section 67(6) postpones the charge until the converted stock is sold; FMV on conversion is the consideration. Business income on sale is taxed in the same year. In practice: record FMV on conversion.', 'c3', T3),
        Q('m7', 'Enhanced compensation received on compulsory acquisition is taxed with cost of acquisition taken as:', ['Nil', 'Original cost', 'FMV on date of acquisition', 'Indexed cost'], 0,
          'Enhanced compensation is taxed in the year of receipt and its cost of acquisition and improvement are taken as nil; litigation expenses are deductible. Compensation under an interim order waits for the final order. In practice: this is a common exam point.', 'c3', T3),
        Q('m8', 'Which of the following is NOT regarded as a transfer?', ['Gift of a house by a father to his son', 'Sale of shares by a son to his father', 'Exchange of land for a flat', 'Compulsory acquisition of land'], 0,
          'A gift by an individual or HUF is excluded from transfer by section 70, so no capital gain arises to the donor. Sales, exchanges and compulsory acquisitions are transfers. In practice: the son later uses the father\'s cost and holding period.', 'c4', T4),
        Q('m9', 'Transfer of a capital asset by a company to its wholly owned subsidiary is not a transfer if:', ['The subsidiary is an Indian company and the asset is not stock-in-trade', 'The subsidiary is a foreign company', 'The asset is stock-in-trade', 'The parent holds 51% of shares'], 0,
          'Section 70 excludes transfers by a holding company to a wholly owned subsidiary that is an Indian company, and vice versa, provided the asset is not stock-in-trade. Partial ownership does not qualify. In practice: this supports intra-group reorganisations.', 'c4', T4),
        Q('m10', 'House bought in 1995 for ₹3,00,000; FMV on 1.4.2001 ₹9,00,000; stamp duty value on 1.4.2001 ₹7,50,000. Cost of acquisition is:', ['₹7,50,000', '₹9,00,000', '₹3,00,000', '₹8,25,000'], 0,
          'For assets acquired before 1 April 2001 the assessee may take FMV on that date, but for land or building the FMV cannot exceed the stamp duty value on that date. So ₹7,50,000 is the higher permissible option. In practice: obtain the 2001 circle rate.', 'c5', T5, 'moderate', check=750000),
        Q('m11', 'Listed shares bought in 2016 at ₹200 (STT paid); highest price on 31.1.2018 ₹320; sold in 2026 at ₹290 with STT. Cost of acquisition per share is:', ['₹290', '₹320', '₹200', '₹255'], 0,
          'Cost is the higher of actual cost (₹200) and the lower of FMV on 31 January 2018 (₹320) and sale price (₹290), i.e. higher of ₹200 and ₹290 = ₹290. The gain is nil, not a loss. In practice: grandfathering cannot create a loss.', 'c5', T5, 'hard', check=290),
        Q('m12', 'The cost of acquisition of bonus shares allotted in 2019 is:', ['Nil', 'Face value', 'Market price on allotment', 'Cost of original shares'], 0,
          'Financial assets allotted without payment on the basis of an existing holding have nil cost; bonus shares allotted before 1 April 2001 can take FMV on that date instead. In practice: the whole sale price of post-2001 bonus shares is gain.', 'c5', T5),
        Q('m13', 'Which is NOT deductible in computing capital gains on sale of listed shares?', ['Securities transaction tax', 'Brokerage', 'Cost of acquisition', 'Expenses wholly for the transfer'], 0,
          'Section 72 bars deduction of securities transaction tax and of interest already claimed elsewhere; brokerage, other transfer expenses and the cost of the shares remain deductible as usual. In practice: contract notes show STT separately.', 'c5', T5),
        Q('m14', 'Furniture block opening WDV ₹2,40,000; no additions; the whole block is sold for ₹2,00,000. The result is:', ['Short-term capital loss of ₹40,000', 'Depreciation of ₹20,000', 'Long-term capital loss of ₹40,000', 'No tax effect'], 0,
          'When all assets of a block are sold and the consideration is below the opening WDV plus additions, the block ceases and the shortfall is a short-term capital loss, irrespective of the holding period. In practice: such losses are set off as per the set-off rules.', 'c6', T6, 'moderate'),
        Q('m15', 'In a slump sale, the cost of acquisition of the undertaking is taken as:', ['Its net worth', 'Sum of book values of assets', 'FMV of assets', 'Indexed net worth'], 0,
          'Section 77 deems net worth of the undertaking to be the cost of acquisition and improvement, and FMV under Rule 53 to be the consideration. Holding for more than 36 months makes the gain long-term. In practice: a CA report on net worth is mandatory.', 'c6', T6),
        Q('m16', 'Flat sold for ₹1,00,00,000; stamp duty value ₹1,08,00,000 on the same day. Full value of consideration is:', ['₹1,00,00,000', '₹1,08,00,000', '₹1,04,00,000', '₹1,10,00,000'], 0,
          'Stamp duty value replaces consideration only when it exceeds 110% of the price; 110% of ₹1 crore is ₹1.10 crore, and ₹1.08 crore is within that tolerance. Actual price stands. In practice: compute the 110% limit first.', 'c7', T7, 'core', check=10000000),
        Q('m17', 'An advance forfeited in 2020 on a failed sale of land is:', ['Taxed as income from other sources in the year of forfeiture', 'Deducted from cost of acquisition', 'Exempt', 'Taxed as capital gains when forfeited'], 0,
          'Advances forfeited on or after 1 April 2014 are taxed under other sources in the year of forfeiture and therefore do not reduce cost later; only pre-2014 forfeitures reduce cost. In practice: check the forfeiture date.', 'c7', T7),
        Q('m18', 'LTCG of ₹1,50,00,000 on sale of a residential house; the assessee buys two houses for ₹1,60,00,000 in total (first time using the option). Deduction under section 82 is:', ['₹1,50,00,000', '₹1,60,00,000', '₹2,00,00,000', '₹75,00,000'], 0,
          'Where gain does not exceed ₹2 crore, an individual may once in life invest in two houses; the deduction is the lower of gain and cost of the new houses, so the whole ₹1.5 crore is exempt. In practice: the option cannot be used again.', 'c8', T8, 'moderate', check=15000000),
        Q('m19', 'Under section 86, net consideration ₹80,00,000, LTCG ₹30,00,000 and new house cost ₹60,00,000. Deduction is:', ['₹22,50,000', '₹30,00,000', '₹60,00,000', '₹7,50,000'], 0,
          'Section 86 allows proportionate relief when only part of the net consideration is invested: ₹30,00,000 × 60/80 = ₹22,50,000. Full relief needs investment of the entire net consideration. In practice: compare with section 85 bonds for the balance if the asset is land.', 'c8', T8, 'hard', check=2250000),
        Q('m20', 'The maximum investment eligible for deduction under section 85 in a tax year is:', ['₹50 lakh', '₹1 crore', '₹10 crore', 'No limit'], 0,
          'Investment in notified long-term bonds from gains on land or building is capped at ₹50 lakh across the year of transfer and the next year, and must be made within six months of transfer. In practice: plan the timing across March and April.', 'c8', T8, 'core', check=50),
        Q('m21', 'Mr. Joseph, a resident, has LTCG of ₹3,00,000 on listed shares (STT paid both ways) and other income above the basic exemption limit. Tax on the LTCG before cess is:', ['₹21,875', '₹37,500', '₹15,625', 'Nil'], 0,
          'Under section 198, only LTCG exceeding ₹1,25,000 is taxed at 12.5%: (₹3,00,000 − ₹1,25,000) × 12.5% = ₹21,875. Since other income already uses the exemption limit, no further adjustment applies. In practice: rebate u/s 156 is not available against this tax.', 'c9', T9, 'moderate', check=21875),
        Q('m22', 'STCG on sale of listed equity shares through a recognised stock exchange with STT is taxed at:', ['20%', '15%', '12.5%', 'Slab rates'], 0,
          'Section 196 taxes STCG on listed equity shares, equity-oriented fund units and business trust units at 20% where the sale is chargeable to STT. Other STCG is taxed at slab or normal rates. In practice: intraday gains are speculative business income instead.', 'c9', T9, 'core', check=20),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Consideration test 110%', 1, 'concept', '110', nums=[7500000]),
           S('s2', 'LTCG without indexation', 2, 'computation', 'without indexation|12.5', nums=[lt, ta]),
           S('s3', 'Indexed costs', 2, 'computation', 'indexed', nums=[icoa, icoi]),
           S('s4', 'Tax with indexation', 1.5, 'computation', '20%', nums=[lti, tb]),
           S('s5', 'Lower tax applies', 1.5, 'concept', 'lower|excess', nums=[ex])],
          ['Keep income and tax computations separate.'], ['Putting indexed LTCG into total income.'], ['Step table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Transfer in year of conversion', 1, 'concept', 'conversion'),
           S('s2', 'Taxed in year of sale', 1, 'concept', '2026-27|sold'),
           S('s3', 'LTCG and business income', 1.5, 'computation', 'business income', nums=[cg, bi]),
           S('s4', 'Six months from sale for s. 85', 0.5, 'concept', 'six months|6 months')],
          ['Show both incomes.'], ['Taxing capital gain in the conversion year.'], ['Table.'], pad='table', checks=list(ck2)),
        W('q3', 4, i3['q'], i3['solution'],
          [S('s1', 'Two-house option available', 1, 'concept', 'two|2 crore'),
           S('s2', 'Section 82 deduction', 1.5, 'computation', '82', nums=[d82]),
           S('s3', 'Section 85 within cap', 1, 'computation', '85', nums=[d85]),
           S('s4', 'Taxable LTCG', 0.5, 'computation', 'taxable', nums=[tx])],
          ['Apply s. 82 first, then s. 85.'], ['Ignoring the ₹2 crore condition for two houses.'], ['Table.'], pad='table', checks=list(ck3)),
        W('q4', 4, 'Explain the tax treatment when a depreciable asset forming part of a block is sold.',
          [ul(['Depreciable assets in a block are treated as short-term capital assets regardless of holding period (s. 74).', 'If consideration exceeds opening WDV + actual cost of additions + transfer expenses, the excess is short-term capital gain.', 'If the whole block is sold for less than that total, the block ceases and the shortfall is a short-term capital loss.', 'If some assets remain and consideration is lower, there is no gain or loss — the balance continues as WDV for depreciation.'])],
          [S('s1', 'Always short-term', 1, 'concept', 'short-term|short term'),
           S('s2', 'Excess over WDV + additions = STCG', 1.5, 'concept', 'excess|exceeds'),
           S('s3', 'Block ceases → STCL', 1, 'concept', 'ceases|loss'),
           S('s4', 'Otherwise continues as WDV', 0.5, 'concept', 'wdv')],
          ['Four outcomes.'], ['Calling a gain on a block long-term.'], ['Bulleted list.']),
    ]

    viva = [
        V('v1', 'What is the holding-period test for listed equity shares?',
          'They are short-term if held for up to 12 months before transfer and long-term if held for more than 12 months.',
          [P('p1', '12 months', 6, '12'), P('p2', 'Long-term beyond that', 4, 'long-term|long term')], 'c2'),
        V('v2', 'When is stamp duty value taken as the sale consideration?',
          'When the stamp duty value of land or building is more than 110% of the actual consideration; otherwise the actual price is used.',
          [P('p1', 'Land or building', 3, 'land|building'), P('p2', 'More than 110%', 7, '110')], 'c7'),
        V('v3', 'What is the cost of bonus shares allotted after 2001?',
          'The cost is nil, because they are allotted without any payment on the basis of existing shares.',
          [P('p1', 'Nil', 7, 'nil'), P('p2', 'Allotted without payment', 3, 'without')], 'c5'),
        V('v4', 'What is the rate and threshold for LTCG on listed equity under section 198?',
          'Gains above 1,25,000 rupees in a year are taxed at 12.5%, provided STT conditions are met.',
          [P('p1', '₹1,25,000 threshold', 5, '1,25,000|125000'), P('p2', '12.5%', 5, '12.5')], 'c9'),
        V('v5', 'What are the conditions for section 85?',
          'Long-term gain on land or building must be invested within six months in notified bonds redeemable after five years, up to 50 lakh rupees, and the bonds must be held for five years.',
          [P('p1', 'Land or building', 2, 'land|building'), P('p2', 'Six months', 3, 'six months|6 months'), P('p3', '₹50 lakh', 3, '50 lakh'), P('p4', 'Five-year lock-in', 2, 'five years|5 years')], 'c8'),
    ]

    cases = [{'id': 'k1', 'title': 'The Menon family portfolio', 'difficulty': 'moderate',
              'case': 'Geeta Menon, a resident aged 50, sold in TY 2026-27: (A) listed shares bought in March 2026 for ₹4,00,000 and sold in October 2026 for ₹5,20,000 on the exchange with STT; (B) gold coins inherited from her mother, who bought them in 2010; (C) a painting she bought in 2023 and hung at home, sold in 2026; (D) her personal car bought in 2022, sold at a profit.',
              'mcqs': [
                  M('k1a', 'Gain on the shares in (A) is:', ['STCG of ₹1,20,000 taxed at 20%', 'LTCG of ₹1,20,000 exempt up to ₹1,25,000', 'STCG at slab rates', 'Business income'], 0,
                    'Listed shares held for not more than 12 months are short-term; with STT paid on sale, section 196 applies a 20% rate to the ₹1,20,000 gain. The ₹1,25,000 threshold applies only to long-term gains under section 198. In practice: holding a little longer can change the rate.', 'core', topic=T9),
                  M('k1b', 'For the gold coins in (B), the holding period:', ['Includes her mother\'s holding since 2010', 'Starts from the date of inheritance', 'Is irrelevant because inherited assets are exempt', 'Is counted from 1 April 2001'], 0,
                    'For assets received by inheritance, the previous owner\'s holding period is included and her cost is the previous owner\'s cost. The coins are therefore long-term, being held well over 24 months in total. In practice: keep the mother\'s purchase bills.', 'core', topic=T2),
                  M('k1c', 'The painting in (C) is:', ['A capital asset, as paintings are excluded from personal effects', 'Not a capital asset, being personal effects', 'Stock-in-trade', 'Exempt'], 0,
                    'Paintings, sculptures, drawings, archaeological collections, works of art and jewellery are expressly excluded from personal effects, so they remain capital assets even when held for personal use. Held for up to 24 months, the gain would be short-term. In practice: art sales need cost records.', 'moderate', topic=T1),
                  M('k1d', 'The profit on sale of her personal car in (D) is:', ['Not taxable as capital gains, since the car is a personal effect', 'Long-term capital gain', 'Short-term capital gain', 'Income from other sources'], 0,
                    'A car used personally is movable property held for personal use and is not among the excluded categories, so it is a personal effect outside the definition of capital asset. Its sale gives no capital gain. In practice: a car used in business is different.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p3', 'int-p3-a-ch03', 4, 'Capital Gains',
                ['Identify capital assets and classify them as short-term or long-term.',
                 'Recognise transfers, transactions excluded from transfer and the year of charge.',
                 'Compute capital gains including cost of acquisition, improvement and deemed consideration.',
                 'Apply rules for depreciable assets and slump sale.',
                 'Apply reinvestment deductions and special tax rates.'],
                {'difficulty': 'hard', 'minutes': {'learn': 70, 'practice': 55}, 'prereq': ['int-p3-a-ch03-u03'],
                 'exam_tip': 'Expect a computation combining holding period, cost (2001 FMV or grandfathering), stamp duty value and a section 82/85/86 deduction, plus rate application.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Capital asset excludes stock, personal effects (but not jewellery/art), rural agricultural land.', 'Short-term: ≤ 12 months listed securities; ≤ 24 months others; MLDs etc. always short-term.',
                             'Transfer includes conversion into stock, part-performance possession, society-membership arrangements.', 'Gifts, wills, partition, 100% group transfers, amalgamation/demerger are not transfers.',
                             'Gain = consideration − transfer expenses − cost − improvement; no indexation in income.', 'Stamp duty value replaces price if > 110%.',
                             'Depreciable assets → STCG/STCL; slump sale cost = net worth.', 'Reinvestment: ss. 82, 83, 84, 85 (₹50 lakh, 6 months), 86 (proportionate).',
                             'Rates: STCG equity 20%; LTCG 12.5% (equity above ₹1.25 lakh); old land/building lower of 12.5% and 20% indexed.'],
                 'remember': ['FMV on 1.4.2001 capped at stamp duty value for land/building.', 'Grandfathered cost cannot create a loss.'],
                 'traps': ['Unlisted shares need more than 24 months to be long-term.', 'No rebate u/s 156 against s. 198 tax.']},
                [('Listed securities long-term', '> 12 months'), ('Other assets long-term', '> 24 months'), ('Stamp duty tolerance', '110%'), ('Equity LTCG exemption', '₹1,25,000'),
                 ('LTCG rate', '12.5%'), ('Equity STCG rate', '20%'), ('Section 85 cap', '₹50 lakh in 6 months'), ('Section 82/86 cap', '₹10 crore')],
                viva, cases,
                topics=['Structured Sectional Learning', 'Introduction', 'Capital Asset', 'Short Term and Long Term Capital Assets', 'Transfer', 'Scope and Year of Chargeability',
                        'Capital Gains on Distribution of Assets by Companies in Liquidation', 'Capital Gains on Buyback of Shares', 'Important Definitions',
                        'Transactions not Regarded as Transfer', 'Mode of Computation of Capital Gains', 'Ascertainment of Cost in Specified Circumstances',
                        'Cost of Acquisition', 'Cost of Improvement', 'Capital Gains in Case of Depreciable Assets', 'Capital Gains in respect of Slump Sale',
                        'Deemed Full Value of Consideration', 'Advance Money Received', 'Exemptions and Deductions in respect of Capital Gains',
                        'Reference to Valuation Officer', 'Tax on Short Term Capital Gains', 'Tax on Long Term Capital Gains'])
