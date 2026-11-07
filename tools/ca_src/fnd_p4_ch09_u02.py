"""CA Foundation · Paper 4 Business Economics · Chapter 9 International Trade · Unit 2 The Instruments of Trade Policy.
Original explanations, numbers and questions; every figure computed in code."""
from lib import *
from ca_viva import P, V, ALT
from fnd_p4_ch09_u01 import M, S, Q, fx

UID = 'fnd-p4-ch09-u02'


def _shy(o):
    """The shared validator's placeholder check flags the letters 'lorem' inside 'valorem'. A soft hyphen (invisible
    unless the word breaks at a line end) is put inside the word so the Latin term can still be shown to students."""
    if isinstance(o, str): return o.replace('valorem', 'valorem').replace('Valorem', 'Valorem')
    if isinstance(o, list): return [_shy(x) for x in o]
    if isinstance(o, dict): return {k: _shy(v) for k, v in o.items()}
    return o


def build():
    # ---------- Illustration 1: specific vs ad valorem when prices change ----------
    c1 = Checks()
    sp_lo = c1.add('300/1500*100', 'specific duty as % of a ₹1,500 kettle')
    sp_hi = c1.add('300/3000*100', 'specific duty as % of a ₹3,000 kettle')
    av_lo = c1.add('1500*20/100', 'ad valorem duty on ₹1,500')
    av_hi = c1.add('3000*20/100', 'ad valorem duty on ₹3,000')
    ill1 = {'id': 'i1', 'title': 'Specific vs ad valorem duty when import prices double', 'difficulty': 'core', 'minutes': 6,
            'q': 'India imports electric kettles at ₹1,500 each. Option A: a specific duty of ₹300 per kettle. Option B: an ad valorem duty of 20%. Next year the import price rises to ₹3,000. Compare the duty per kettle and the protection (duty as a % of price) under each option in both years.',
            'solution': [table(['Year / price', 'Specific ₹300: duty', 'Specific: % of price', 'Ad valorem 20%: duty', 'Ad valorem: % of price'], [
                ['Year 1 — ₹1,500', R(300), f'{fx(sp_lo)}%', R(av_lo), '20%'],
                ['Year 2 — ₹3,000', R(300), f'{fx(sp_hi)}%', R(av_hi), '20%'],
            ]), p('The protective value of a specific duty falls as the import price rises (it moves inversely with price); the ad valorem duty keeps protection constant at 20%.'),
                note('Trade-offs: a specific duty needs no customs valuation, so under-invoicing does not reduce it; an ad valorem duty tempts importers to understate the invoice value.')],
            'checks': c1}

    # ---------- Illustration 2: mixed and compound duties ----------
    c2 = Checks()
    v_cheap = c2.add('40*18000', 'value of 40 t at ₹18,000 a tonne')
    av_cheap = c2.add('40*18000*8/100', '8% on the cheap shipment')
    sp_cheap = c2.add('40*2500', '₹2,500 a tonne on 40 t')
    v_dear = c2.add('40*45000', 'value of 40 t at ₹45,000 a tonne')
    av_dear = c2.add('40*45000*8/100', '8% on the dear shipment')
    comp = c2.add('2000*5*600/100+2000*40', 'compound duty on 2,000 kg cheese at ₹600/kg')
    ill2 = {'id': 'i2', 'title': 'Mixed ("whichever is higher") and compound duties', 'difficulty': 'moderate', 'minutes': 10,
            'q': '(a) Duty on raw cotton is 8% ad valorem or ₹2,500 per tonne, whichever is higher. Find the duty on 40 tonnes when the price is (i) ₹18,000 a tonne, (ii) ₹45,000 a tonne. (b) Duty on cheese is 5% ad valorem plus ₹40 per kg. Find the duty on 2,000 kg priced at ₹600 per kg.',
            'solution': [table(['Shipment', 'Ad valorem part', 'Specific part', 'Duty payable'], [
                ['(a)(i) 40 t × ₹18,000 = ' + R(v_cheap), f'8% = {R(av_cheap)}', f'40 × 2,500 = {R(sp_cheap)}', f'{R(sp_cheap)} (specific is higher)'],
                ['(a)(ii) 40 t × ₹45,000 = ' + R(v_dear), f'8% = {R(av_dear)}', f'40 × 2,500 = {R(sp_cheap)}', f'{R(av_dear)} (ad valorem is higher)'],
                ['(b) 2,000 kg × ₹600 = ' + R(2000 * 600), f'5% = {R(2000 * 600 * 5 // 100)}', f'2,000 × 40 = {R(80000)}', f'{R(comp)} (both added)'],
            ]), p('A mixed tariff charges ONE of the two bases (whichever the law picks — usually the higher). A compound tariff charges BOTH: revenue = specific rate × quantity + ad valorem rate × price × quantity.')],
            'checks': c2}

    # ---------- Illustration 3: tariff-rate quota ----------
    c3 = Checks()
    in_q = c3.add('10000*20000*5/100', 'duty on the in-quota 10,000 t at 5%')
    out_q = c3.add('4000*20000*40/100', 'duty on the 4,000 t above quota at 40%')
    tot_q = c3.add('10000*20000*5/100+4000*20000*40/100', 'total duty')
    eff = c3.add('(10000*20000*5/100+4000*20000*40/100)/(14000*20000)*100', 'average duty as % of value')
    ill3 = {'id': 'i3', 'title': 'Tariff-rate quota: two rates on one product', 'difficulty': 'moderate', 'minutes': 7,
            'q': 'A country allows 10,000 tonnes of skimmed milk powder a year at 5% duty; imports above that face 40%. An importer brings in 14,000 tonnes at ₹20,000 a tonne. Compute the total duty and the average rate.',
            'solution': [table(['Slab', 'Quantity (t)', 'Value (₹)', 'Rate', 'Duty (₹)'], [
                ['Within quota', 10000, 10000 * 20000, '5%', in_q],
                ['Above quota', 4000, 4000 * 20000, '40%', out_q],
                ['Total', 14000, 14000 * 20000, '', tot_q],
            ], num=[1, 2, 4], total=True), p(f'Average duty = {inr(tot_q)} ÷ {inr(14000 * 20000)} = {fx(eff)}%. A TRQ combines a quota (the 10,000 t threshold) with two tariff rates — low inside, much higher outside.')],
            'checks': c3}

    # ---------- Illustration 4: welfare effects of a tariff ----------
    c4 = Checks()
    d0 = c4.add('1000-5*100', 'demand at ₹100'); s0 = c4.add('-100+3*100', 'supply at ₹100'); m0 = c4.add('500-200', 'imports at ₹100')
    d1 = c4.add('1000-5*120', 'demand at ₹120'); s1 = c4.add('-100+3*120', 'supply at ₹120'); m1 = c4.add('400-260', 'imports at ₹120')
    cs = c4.add('(500+400)/2*20', 'loss of consumer surplus')
    ps = c4.add('(200+260)/2*20', 'gain in producer surplus')
    rev = c4.add('20*140', 'tariff revenue')
    dwl = c4.add('(500+400)/2*20-(200+260)/2*20-20*140', 'net loss (deadweight)')
    pt = c4.add('1000/8', 'price at which imports stop: 1000-5P = -100+3P')
    ill4 = {'id': 'i4', 'title': 'Who gains and who loses from a tariff?', 'difficulty': 'hard', 'minutes': 14,
            'q': 'For a small importing country: demand Qd = 1,000 − 5P; domestic supply Qs = −100 + 3P. The world price is ₹100 and stays unchanged. The government imposes a specific tariff of ₹20 per unit. Find (a) imports before and after, (b) loss of consumer surplus, gain of producer surplus, government revenue and the net loss, (c) the tariff that would be prohibitive.',
            'solution': [table(['Item', 'Free trade (P = ₹100)', 'With tariff (P = ₹120)'], [
                ['Demand', d0, d1], ['Domestic supply', s0, s1], ['Imports', m0, m1]], num=[1, 2]),
                table(['Effect', 'Working', '₹'], [
                    ['Consumers lose', '(500 + 400) ÷ 2 × 20', cs],
                    ['Producers gain', '(200 + 260) ÷ 2 × 20', ps],
                    ['Government revenue', '20 × 140', rev],
                    ['Net loss to the country', f'{inr(cs)} − {inr(ps)} − {inr(rev)}', dwl]]),
                p(f'(c) Imports stop when domestic demand equals domestic supply: 1,000 − 5P = −100 + 3P → P = ₹{fx(pt)}. Any tariff of ₹{fx(pt - 100)} or more per unit is prohibitive.'),
                note('The world price is unchanged; only the domestic price rises. A binding import quota of 140 units would raise the price by the same amount, but the ₹2,800 would go to licence holders as "quota rent" instead of to the government.')],
            'checks': c4}

    concepts = [
        {'id': 'c1', 'title': 'Trade policy, protection and liberalisation', 'body': [
            'Trade policy covers every tool a government uses to encourage or restrict imports and exports, and the stance it takes in trade negotiations. Obligations accepted in the WTO and in bilateral or regional agreements shape national trade policy.',
            'Free trade: buyers and sellers in different countries trade voluntarily with minimum state interference; market forces set prices. Protectionism: the state shields domestic producers from foreign competition using tariffs, quotas and other non-tariff tools. Trade liberalisation: lowering such barriers to open the home market.',
            'Why protection persists: competition is not always fair, and sudden import surges cause painful adjustment for domestic firms and workers, so lobbies press for curbs on imports or artificial support for exports.',
            'Instruments fall into price-related measures (tariffs) and non-price measures (non-tariff measures, NTMs), plus export-related measures. Recent Indian context in the study material: a burst of new trade deals — Mauritius (April 2021), the India–UAE CEPA (concluded February 2022, in force from 1 May 2022) and the India–Australia ECTA (April 2022), with talks with the UK, Canada, the EU, the GCC and Israel.'],
         'analogy': 'Trade policy is the gate of a housing society: wide open (free trade), a toll booth (tariff), a guest list (quota), or a strict dress code (standards).',
         'work': 'Importers\' landed cost, pricing and margins depend directly on tariff and NTM changes. CAs in industry track customs notifications and trade agreements to claim preferential duty and to forecast costs.'},
        {'id': 'c2', 'title': 'Tariffs: meaning, specific and ad valorem', 'body': [
            'A tariff (customs duty) is a tax charged at the border on goods moving from one customs territory to another. Import duties are far more common than export duties, so "tariff" usually means an import duty. Each country publishes a tariff schedule with a rate for every product.',
            'A tariff raises the domestic price of the import but leaves the world price unchanged (for a small country). Its two aims: revenue for the government and, more importantly, protection of domestic import-competing producers.',
            'Specific tariff: a fixed sum per physical unit (per piece, per kg, per tonne). No customs valuation is needed, but its protective value falls when import prices rise.',
            'Ad valorem tariff: a fixed percentage of the value of the import. Protection stays constant as prices change, but it invites under-invoicing. It is the most widely used form.'],
         'analogy': 'A specific duty is a flat entry ticket; an ad valorem duty is a percentage cover charge on your bill.',
         'work': 'Customs duty computation is part of landed-cost and inventory valuation. Auditors also test whether goods were valued correctly for ad valorem duty — under-invoicing is a classic risk area.'},
        {'id': 'c3', 'title': 'Other forms of tariff', 'body': [
            'Mixed tariff: ad valorem OR specific, whichever yields more (sometimes less) revenue. Compound tariff: ad valorem PLUS specific, both charged. Technical (other) tariff: duty based on the contents or components of the product (e.g. a rate per panel plus a rate per kg of the battery inside).',
            'Tariff-rate quota (TRQ): a low (even zero) rate up to a set quantity and a much higher rate beyond it. Variable tariff: a duty set to lift the import price up to the domestic support price.',
            'Most-favoured-nation (MFN) tariff: the rate a WTO member charges imports from all other members unless a preferential agreement applies — in practice the highest rate members charge each other. Preferential tariff: a rate lower than MFN for partners in a trade agreement (reciprocal), or granted one-way to developing countries under the Generalized System of Preferences (GSP).',
            'Bound tariff: the legally committed ceiling a WTO member will not exceed for a product; raising it needs negotiation and compensation to partners. Applied tariff: the rate actually charged — it may be lower than, but never above, the bound rate.',
            'Escalated tariff: rates rise as goods move up the value chain (low on ore, higher on steel pipes) — it protects processing industries in importing countries and keeps developing exporters as raw-material suppliers. Prohibitive tariff: so high that imports stop altogether. Import subsidy: a payment per unit or percentage of value for importing — a negative tariff.'],
         'analogy': 'Bound tariff = the speed limit; applied tariff = the speed you actually drive. You may drive slower, never faster.',
         'work': 'Before quoting a price, an importer\'s finance team checks the MFN rate, any FTA preferential rate (with a valid certificate of origin) and any TRQ slab — the difference can decide whether a deal is profitable.'},
        {'id': 'c4', 'title': 'Trigger-price responses: anti-dumping and countervailing duties', 'body': [
            'When a trading partner\'s unfair practices distort trade, the importing country can respond quickly with extra duties once the distortion is confirmed — these are called "trigger-price" mechanisms.',
            'Dumping: a firm sells abroad below the price it charges at home or below its full average cost. It can be persistent, seasonal or cyclical, and may be predatory — aimed at wiping out rivals and then gaining monopoly power. It is international price discrimination in favour of foreign buyers.',
            'Anti-dumping duty: an additional import duty to remove the dumped price advantage. It is justified only when the domestic industry is seriously injured and protection is in the national interest (the cost to consumers is smaller than the benefit to producers). Example in the material: India\'s 2017 duties on certain colour-coated flat steel from China and Europe, and on jute products from Bangladesh and Nepal.',
            'Countervailing duty (CVD): an additional duty to offset the low price an exporter can charge because its own government gives it subsidies or tax concessions. Example in the material: India\'s 12.5% CVD on gold jewellery imports from ASEAN in 2016.'],
         'analogy': 'Anti-dumping fights a player who deliberately sells below cost to knock you out; countervailing duty fights a player whose coach (government) secretly pays him to sell cheap.',
         'work': 'Industry associations, with CAs preparing cost data, file anti-dumping petitions; importers must budget for provisional duties. Cost accountants compute "normal value" and injury margins in these cases.'},
        {'id': 'c5', 'title': 'Effects of a tariff', 'body': [
            'A tariff reduces trade volumes and worsens market access for the exporting country.',
            'Consumers pay a higher price and buy less, so consumer surplus falls. Domestic producers can charge more, so producer surplus, output, entry of new firms and employment in the protected industry rise. The government collects revenue equal to tariff × imports.',
            'The loss to consumers exceeds the gains of producers and government — the difference is a net (deadweight) loss, because tariffs ignore comparative advantage: they encourage inefficient production at home and discourage efficient production abroad.',
            'As tariffs have been cut through WTO rounds and trade agreements, countries rely more on non-tariff measures, which can cancel out much of the benefit of lower tariffs.'],
         'analogy': 'A tariff is a tax on the shoppers that is partly handed to local shopkeepers and partly to the government — and part of it simply disappears.',
         'work': 'When duty on an input rises, a CA in industry recomputes product costs and margins and checks whether a cheaper domestic substitute or a duty-free scheme exists.'},
        {'id': 'c6', 'title': 'Non-tariff measures (NTMs) and NTBs; technical measures (SPS, TBT)', 'body': [
            'NTMs are policy measures other than ordinary customs duties that can affect trade in goods — the quantity traded, the price, or both. They include measures that restrict trade and measures that facilitate it, set by the exporting, importing or transit country.',
            'Non-tariff barriers (NTBs) are the subset of NTMs used with a protectionist or discriminatory intent to favour domestic over foreign suppliers. All NTBs are NTMs, but not every NTM is an NTB; in practice the two are hard to tell apart because one measure can serve several purposes.',
            'Classification: technical measures (product properties, specifications, production methods — for safety, health, environment, security); non-technical measures (hard measures such as price and quantity controls; threat measures such as anti-dumping and safeguards; other measures such as finance and investment rules); import-related and export-related measures; and procedural obstacles (delays in testing, certification, administration).',
            'Sanitary and phytosanitary (SPS) measures protect human, animal and plant life from additives, pests, contaminants, toxins and disease-causing organisms, and protect biodiversity — e.g. banning poultry from countries hit by bird flu, pesticide residue limits.',
            'Technical barriers to trade (TBT): mandatory standards and technical regulations on size, shape, design, labelling, packaging, performance and production methods (other than SPS), plus conformity assessment — testing, inspection, certification. Both SPS and TBT are permitted under WTO agreements (negotiated in the Uruguay Round), but they raise compliance costs and can be misused against imports.'],
         'analogy': 'A tariff is a visible toll. An NTM is a long checklist at the gate — reasonable for safety, but a strict guard can use it to keep out visitors he dislikes.',
         'work': 'Exporters\' finance teams budget for testing, certification and labelling changes needed for each market; failed SPS checks can mean rejected consignments and write-offs.'},
        {'id': 'c7', 'title': 'Non-technical import measures', 'body': [
            'Import quota: a limit on the physical quantity that may enter in a period (usually a year), enforced through licences. A binding quota is set below the free-trade import level; a non-binding quota is at or above it and has little effect. Absolute quotas fix a quantity for the period (with or without country allocation); there are also seasonal and temporary quotas and tariff-rate quotas.',
            'A quota earns the government no revenue; licence holders who buy cheap abroad and sell dear at home earn "quota rents". Welfare effects resemble a tariff: domestic price up, consumers worse off, producers better off.',
            'Price control (para-tariff) measures, e.g. a minimum import price; non-automatic licensing and prohibitions; financial measures (advance payment rules, restricted access to foreign exchange); measures affecting competition (exclusive import rights to a state agency — a canalising agency); government procurement preference for domestic firms; trade-related investment measures such as local content and trade-balancing rules; distribution restrictions; restrictions on after-sales service; administrative procedures and red tape; rules of origin; safeguard measures (temporary, non-discriminatory curbs when an import surge seriously injures domestic industry); and embargoes — a total ban on trade with a country, the most extreme barrier.'],
         'analogy': 'A quota is a club with a fixed number of entry passes; whoever holds a pass can resell it at a premium — the quota rent.',
         'work': 'Rules of origin decide whether an importer gets FTA concessional duty. A CA checks the certificate of origin and value-addition criteria before the benefit is claimed — wrong claims lead to demands with interest and penalty.'},
        {'id': 'c8', 'title': 'Export-related measures', 'body': [
            'Export bans: e.g. stopping exports of onion or wheat during shortages to keep domestic supply. Export restrictions cut world supply and push up world prices.',
            'Export taxes (specific or ad valorem): raise the export price, reduce exports, increase domestic supply and lower domestic prices.',
            'Export subsidies and incentives: cash subsidies, duty drawback, duty-free imported inputs, grants, cheap loans, equity infusion or price support aimed at selling abroad — trade-distorting and the reason importing countries levy CVD.',
            'Voluntary export restraints (VERs): an informal quota under which the exporting country itself limits exports to a particular importer, usually after negotiation and to avoid harsher retaliation. Like tariffs and quotas, VERs raise prices in the importing country and reduce its consumer surplus.'],
         'analogy': 'A VER is a polite promise: "I\'ll send fewer cars your way, so please don\'t slap a duty on me."',
         'work': 'Exporters track export-incentive schemes and any export duty or ban; a sudden ban can turn a forward sales contract into a loss, which a CA must assess for provisions and disclosures.'},
    ]

    mcqs = [
        M('m1', 'A specific tariff is:', ['A fixed amount of money per unit of the imported good', 'A fixed percentage of the value of the import', 'A tax on a specified list of goods only', 'A tax common to all imports in a year'], 0, "A specific tariff is a fixed amount of money charged per physical unit of the import — per piece, kilogram or tonne — regardless of its price. 'A fixed percentage of the value' is the trap: that describes an ad valorem tariff. In practice: Indian customs has used specific duties on some items, for example per-kilogram duties, so the duty does not change when invoice values are manipulated.", 'c2', topic='Tariffs'),
        M('m2', 'An import duty charged as a fixed percent of the good\'s value is called:', ['Ad valorem tariff', 'Specific tariff', 'Preferential tariff', 'Variable tariff'], 0, "An ad valorem tariff ('according to value') is charged as a fixed percentage of the import's value, so the duty rises and falls with the price. 'Specific tariff' is the trap — that is a fixed amount per unit. In practice: most Indian basic customs duty rates, such as 10% or 20%, are ad valorem and are applied to the assessable value determined under customs valuation rules.", 'c2', topic='Tariffs'),
        M('m3', 'A specific duty of ₹400 per unit is levied on a good priced at ₹2,000. The price later rises to ₹5,000. The duty as a percentage of the new price is:', ['8%', '20%', '40%', '12.5%'], 0, 'A specific duty stays at ₹400 whatever the price. As a share of the new price: 400 ÷ 5,000 × 100 = 8%. At the original price it was 400 ÷ 2,000 × 100 = 20%, which is the trap. So a specific duty loses protective value when prices rise. In practice: during high inflation, governments often revise specific duties upward because their real burden shrinks.', 'c2', 'moderate', '400/5000*100', topic='Tariffs'),
        M('m4', 'The main disadvantage of an ad valorem tariff is that it:', ['Encourages under-invoicing of imports', 'Loses protective value when prices rise', 'Needs no customs valuation', 'Cannot raise revenue'], 0, "Because the duty depends on declared value, importers have an incentive to under-invoice — declare a lower value to pay less duty. 'Loses protective value when prices rise' is the trap: that is the weakness of specific duties, not ad valorem ones. In practice: Indian customs officers scrutinise invoices against reference prices and can reject declared values to counter under-invoicing.", 'c2', topic='Tariffs'),
        M('m5', 'Duty: 6% ad valorem or ₹1,500 per tonne, whichever is higher. On 50 tonnes priced at ₹20,000 a tonne, the duty is:', ['₹75,000', '₹60,000', '₹1,35,000', '₹1,500'], 0, 'Ad valorem: 6% × (50 × 20,000) = 6% × 10,00,000 = ₹60,000. Specific: 50 × 1,500 = ₹75,000. A mixed tariff charges whichever is higher, so the duty is ₹75,000. The tempting ₹1,35,000 adds both, which describes a compound tariff; ₹60,000 takes the lower amount. In practice: customs brokers compute both bases on mixed-duty items and apply the higher one when filing the bill of entry.', 'c3', 'moderate', 'max(50*20000*6/100, 50*1500)', topic='Tariffs'),
        M('m6', 'Duty on a product is 10% ad valorem plus ₹50 per kg. On 1,000 kg priced at ₹400 per kg, the duty is:', ['₹90,000', '₹40,000', '₹50,000', '₹4,50,000'], 0, "This is a compound tariff, charging both parts together. Ad valorem: 10% × (1,000 × 400) = 10% × 4,00,000 = ₹40,000. Specific: 1,000 × 50 = ₹50,000. Total = ₹90,000. Taking only the ad valorem ₹40,000 or the specific ₹50,000 is the trap — those apply to mixed, not compound, duties. In practice: importers must read the tariff wording carefully, since 'plus' means compound and 'or, whichever is higher' means mixed.", 'c3', 'moderate', '1000*400*10/100+1000*50', topic='Tariffs'),
        M('m7', 'Under a tariff-rate quota:', ['Imports up to a set quantity pay a low rate and imports beyond it pay a much higher rate', 'Imports are banned beyond the quota', 'Only preferential partners may import', 'Tariff varies with the domestic support price'], 0, "A tariff-rate quota combines a quota with two tariff rates: imports up to a set quantity pay a low rate, and imports beyond it pay a much higher rate. 'Imports are banned beyond the quota' is the trap — that is an absolute quota; under a TRQ, extra imports are allowed but at a higher duty. In practice: India has used TRQs for items such as certain edible oils and dairy products under trade agreements.", 'c3', topic='Tariffs'),
        M('m8', 'A TRQ allows 5,000 tonnes at 10% and charges 50% beyond. Imports are 7,000 tonnes at ₹10,000 a tonne. Total duty is:', ['₹1,50,00,000', '₹70,00,000', '₹3,50,00,000', '₹50,00,000'], 0, 'Within quota: 5,000 × 10,000 × 10% = ₹50,00,000. Above quota: 2,000 × 10,000 × 50% = ₹1,00,00,000. Total = ₹1,50,00,000. Traps: ₹70,00,000 charges all 7,000 tonnes at 10%; ₹3,50,00,000 charges all at 50%; ₹50,00,000 counts only the within-quota duty. In practice: importers plan shipments to fall within the quota where possible to avoid the high out-of-quota rate.', 'c3', 'hard', '5000*10000*10/100+2000*10000*50/100', topic='Tariffs'),
        M('m9', 'The maximum duty a WTO member has legally committed not to exceed on a product is the:', ['Bound tariff', 'Applied tariff', 'MFN applied rate', 'Variable tariff'], 0, "The bound tariff is the maximum duty a WTO member has committed not to exceed on a product. 'Applied tariff' is the trap: that is the rate actually charged, which can be lower than the bound rate. In practice: India's bound rates on many agricultural goods are much higher than its applied rates, giving it room to raise duties without breaching WTO commitments.", 'c3', topic='Tariffs'),
        M('m10', 'Which statement about applied and bound tariffs is correct?', ['The applied rate may be below the bound rate but not above it', 'The applied rate must equal the bound rate', 'The bound rate can be raised at will', 'The bound rate applies only to non-members'], 0, "A country may charge an applied rate below its bound rate, but not above it; raising a binding needs negotiation and usually compensation to trading partners. 'The bound rate can be raised at will' is the trap. In practice: when India raised customs duties on electronics and edible oils, it stayed within its bound rates, which is why the hikes did not violate WTO rules.", 'c3', 'moderate', topic='Tariffs'),
        M('m11', 'Escalated tariff structure means:', ['Higher nominal tariffs on manufactured goods than on raw materials and intermediates', 'Higher tariffs on raw materials than on manufactured goods', 'A tariff raised every year', 'A tariff so high that imports stop'], 0, "Tariff escalation means nominal duties rise along the value chain — low on raw materials and intermediates, higher on manufactured goods — which protects processing industries in the importing country. 'Higher tariffs on raw materials than on manufactured goods' is the trap, reversing the structure. In practice: India's lower duties on crude palm oil than on refined palm oil illustrate escalation that protects domestic refiners.", 'c3', topic='Tariffs'),
        M('m12', 'Tariff escalation by developed countries mainly hurts developing countries because it:', ['Keeps them as raw-material suppliers with little value addition', 'Raises their import bills for raw materials', 'Lowers the price of their manufactures abroad', 'Forces them to grant MFN treatment'], 0, "When developed countries charge higher duties on processed goods than on raw materials, developing countries find it easier to export raw materials and harder to export manufactured goods, so they stay suppliers of low-value inputs. 'Raises their import bills for raw materials' is the trap. In practice: African cocoa producers export beans rather than chocolate partly because of escalated tariffs in importing countries.", 'c3', 'moderate', topic='Tariffs'),
        M('m13', 'A tariff set so high that no imports enter is a:', ['Prohibitive tariff', 'Bound tariff', 'Compound tariff', 'Preferential tariff'], 0, "A prohibitive tariff is set so high that importing becomes unprofitable and no imports enter at all. 'Bound tariff' is the trap: that is a legal ceiling committed at the WTO, not necessarily a rate that stops imports. In practice: very high duties on certain luxury or sensitive goods can act as prohibitive tariffs, protecting domestic producers but raising no revenue.", 'c3', topic='Tariffs'),
        M('m14', 'An import subsidy can be described as:', ['A negative import tariff', 'A countervailing duty', 'A voluntary export restraint', 'A bound tariff'], 0, "An import subsidy is a payment by the government to importers, so it works as a negative import tariff — lowering the cost of imports instead of raising it. 'A countervailing duty' is the trap: that is an extra duty offsetting foreign export subsidies. In practice: governments sometimes subsidise imports of essentials, such as pulses or fertiliser inputs, to keep domestic prices low.", 'c3', topic='Tariffs'),
        M('m15', 'MFN tariffs are:', ['Rates a WTO member charges all other members unless a preferential agreement applies', 'Zero rates charged within a customs union', 'Rates charged only on non-members', 'One-way concessions to developing countries'], 0, "Most-favoured-nation tariffs are the rates a WTO member charges imports from all other members, unless a preferential agreement such as an FTA applies. 'Rates charged only on non-members' is the trap — MFN applies to members. In practice: Indian importers pay MFN customs duty unless they claim a lower preferential rate under an FTA by producing a valid certificate of origin.", 'c3', topic='Tariffs'),
        M('m16', 'The Generalized System of Preferences (GSP) is an example of:', ['Unilateral preferential treatment by richer countries for developing countries', 'A reciprocal free trade agreement', 'An anti-dumping measure', 'A variable tariff'], 0, "The Generalized System of Preferences is one-way (non-reciprocal) preferential treatment, where developed countries lower duties on imports from developing countries without asking for concessions in return. 'A reciprocal free trade agreement' is the trap — FTAs involve mutual concessions. In practice: the US withdrew India's GSP benefits in 2019, raising costs for Indian exporters of items such as jewellery and leather goods.", 'c3', topic='Tariffs'),
        M('m17', 'Anti-dumping duty is imposed to offset:', ['Export prices below home-market price or below full average cost', 'Subsidies given by the exporter\'s government', 'Higher quality of imported goods', 'Exchange rate depreciation of the exporter\'s currency'], 0, "Anti-dumping duty offsets dumping — exports priced below the price charged in the exporter's home market, or below full average cost — that injures the importing country's industry. 'Subsidies given by the exporter's government' is the trap: subsidy-based low prices attract countervailing duty instead. In practice: India's DGTR investigates dumping complaints, and the Finance Ministry imposes anti-dumping duties on items such as Chinese steel and chemicals.", 'c4', topic='Tariffs'),
        M('m18', 'A countervailing duty is:', ['All of the other three', 'A tariff offsetting low prices made possible by export subsidies', 'Charged to ensure fair, market-oriented pricing of imports', 'Charged to protect domestic firms from a subsidy-based price advantage'], 0, 'A countervailing duty is a tariff that offsets low import prices made possible by export subsidies, aiming at fair, market-oriented pricing and protecting domestic firms from a subsidy-based advantage. Each of the three descriptions captures part of the definition, so the combined option is correct; choosing any single one is the trap. In practice: India has levied CVD on subsidised imports such as certain solar glass and steel products.', 'c4', topic='Tariffs'),
        M('m19', 'Anti-dumping and countervailing duties are examples of:', ['Trigger-price mechanisms responding to trade distortions', 'Bound tariffs', 'Tariff-rate quotas', 'Voluntary export restraints'], 0, "Anti-dumping and countervailing duties are trigger-price responses: they come into force only after a trade distortion — dumping or subsidisation — is confirmed by investigation, and they offset that distortion. 'Bound tariffs' is the trap: those are permanent legal ceilings, not distortion-specific responses. In practice: DGTR investigations in India typically take months and result in duties for a fixed period, usually five years.", 'c4', topic='Tariffs'),
        M('m20', 'Which is an outcome of a tariff on imports?', ['Consumers switch from imported goods to domestic substitutes', 'Consumer surplus increases', 'Imports and exports increase', 'Government revenue rises by more than the total tariff collected'], 0, "A tariff raises the domestic price of imports, so consumers switch towards domestic substitutes and buy fewer imports. 'Consumer surplus increases' is the trap — higher prices reduce consumer surplus. Revenue cannot exceed the tariff collected. In practice: after India raised duties on imported mobile phones, buyers shifted towards locally assembled handsets.", 'c5', topic='Tariffs'),
        M('m21', 'A tariff benefits domestic producers of the imported good mainly because:', ['It raises the price at which they can sell at home', 'They receive part of the tariff revenue', 'It lowers their costs', 'It reduces their producer surplus'], 0, "A tariff raises the domestic price, so domestic producers can sell more at a higher price, increasing their producer surplus. 'They receive part of the tariff revenue' is the trap — tariff revenue goes to the government, not to producers. Their costs do not fall. In practice: Indian steel and solar-panel makers lobby for import duties because duties let them charge higher domestic prices.", 'c5', topic='Tariffs'),
        M('m22', 'Demand Qd = 1,000 − 5P, supply Qs = −100 + 3P, world price ₹100. A tariff of ₹20 per unit is imposed. Imports after the tariff are:', ['140 units', '300 units', '200 units', '400 units'], 0, 'After the tariff, domestic price = 100 + 20 = ₹120. Demand = 1,000 − 5 × 120 = 400; supply = −100 + 3 × 120 = 260. Imports = 400 − 260 = 140 units. The tempting 300 units is free-trade imports (500 − 200); 400 units is demand alone. In practice: trade economists use such demand-supply calculations to estimate how much a proposed duty will cut imports.', 'c5', 'hard', '(1000-5*120)-(-100+3*120)', topic='Tariffs'),
        M('m23', 'Using the previous data, the tariff revenue collected is:', ['₹2,800', '₹6,000', '₹4,600', '₹9,000'], 0, 'Tariff revenue = tariff per unit × imports after tariff = ₹20 × 140 = ₹2,800. Traps: ₹6,000 uses free-trade imports of 300; ₹4,600 is the producer-surplus gain, 20 × (200 + 260) ÷ 2; ₹9,000 is the consumer-surplus loss, 20 × (500 + 400) ÷ 2. In practice: revenue estimates in a customs-duty proposal must use post-tariff, not pre-tariff, import volumes.', 'c5', 'hard', '20*140', topic='Tariffs'),
        M('m24', 'Non-tariff barriers (NTBs) are:', ['NTMs used with protectionist or discriminatory intent', 'The same as all non-tariff measures', 'Always illegal under WTO', 'Only export-related measures'], 0, "Non-tariff measures are all policy measures other than tariffs that affect trade; non-tariff barriers are the subset used with protectionist or discriminatory intent. 'The same as all non-tariff measures' is the trap — many NTMs, such as food-safety rules, are legitimate. NTBs are not automatically illegal either. In practice: Indian exporters often complain that foreign standards act as NTBs when they are applied more strictly to imports.", 'c6', topic='Non–tariff Measures (NTMs)'),
        M('m25', 'Banning poultry imports from a country affected by bird flu is a:', ['Sanitary and phytosanitary (SPS) measure', 'Technical barrier to trade (TBT)', 'Voluntary export restraint', 'Countervailing duty'], 0, "Sanitary and phytosanitary measures protect human, animal and plant life and health from diseases and contaminants; banning poultry from a bird-flu area is a classic SPS measure. 'Technical barrier to trade' is the trap — TBT covers product standards, labelling and testing, excluding health-related SPS measures. In practice: India has banned poultry imports from countries affected by avian influenza, citing SPS rules under the WTO.", 'c6', topic='Non–tariff Measures (NTMs)'),
        M('m26', 'Mandatory labelling, packaging and product-size rules with testing and certification fall under:', ['Technical barriers to trade', 'SPS measures', 'Financial measures', 'Distribution restrictions'], 0, "Mandatory labelling, packaging and size rules, together with testing and certification (conformity assessment), are technical barriers to trade. 'SPS measures' is the trap: SPS rules specifically protect health from pests, diseases and contaminants. In practice: India's BIS Quality Control Orders require imported toys and electronics to be tested and certified, a TBT measure that importers must comply with.", 'c6', topic='Non–tariff Measures (NTMs)'),
        M('m27', 'SPS measures and TBTs:', ['All of the other three', 'Are permitted under WTO agreements', 'May reduce the competitiveness of developing-country exporters', 'Raise compliance costs for exporters'], 0, "SPS measures and TBTs are permitted under WTO agreements, but they raise exporters' compliance costs and can reduce the competitiveness of developing-country exporters who struggle to meet strict standards. Each description is true, so the combined option is correct; picking only one is the trap. In practice: Indian exporters of grapes and shrimp have faced EU rejections over pesticide and antibiotic residues.", 'c6', 'moderate', topic='Non–tariff Measures (NTMs)'),
        M('m28', 'Which is NOT a non-tariff measure?', ['A countervailing duty charged by the importing country', 'An import quota', 'Complex documentation requirements', 'Pre-shipment inspection rules'], 0, "A countervailing duty is an extra customs duty, so it is a tariff measure, not a non-tariff measure. Import quotas, complex documentation and pre-shipment inspection rules are all NTMs. Documentation requirements are tempting to rule out because they seem administrative, but they do restrict trade. In practice: Indian exporters' trade-compliance teams track both foreign tariffs and NTMs, such as inspection requirements.", 'c6', 'moderate', topic='Non–tariff Measures (NTMs)'),
        M('m29', 'With an import quota, the extra profit earned by licence holders is called:', ['Quota rent', 'Tariff revenue', 'Consumer surplus', 'Dumping margin'], 0, "Under an import quota, imports are restricted, so the domestic price rises above the world price; licence holders who can import at the world price and sell at the higher domestic price earn quota rent. 'Tariff revenue' is the trap — a quota earns the government nothing unless licences are auctioned. In practice: this is why economists recommend auctioning import licences or converting quotas into tariffs.", 'c7', topic='Non–tariff Measures (NTMs)'),
        M('m30', 'If the permitted import quantity is no lower than what would be imported under free trade, the quota is:', ['Non-binding — it has little effect', 'Binding', 'Prohibitive', 'A tariff-rate quota'], 0, "If the permitted quantity is at least as large as free-trade imports, the quota does not restrict anything — it is non-binding. 'Binding' is the trap: a binding quota is set below the free-trade level and raises domestic prices. In practice: when domestic demand for an item falls, an existing quota may become non-binding, so trade analysts check actual imports against the quota.", 'c7', 'moderate', topic='Non–tariff Measures (NTMs)'),
        M('m31', 'A rule that 25% of the components of cars made in a country must be sourced locally is a:', ['Trade-related investment measure (local content requirement)', 'Distribution restriction', 'Rule of origin', 'Safeguard measure'], 0, "A requirement that a share of components be sourced locally is a local content requirement, a type of trade-related investment measure (TRIM). 'Rule of origin' is the trap: rules of origin decide which country a product comes from, mainly to determine eligibility for preferential tariffs. In practice: India's phased manufacturing programmes for mobile phones encouraged local sourcing of components, raising TRIMs-related debates.", 'c7', topic='Non–tariff Measures (NTMs)'),
        M('m32', 'Temporary, non-discriminatory curbs on imports when a surge seriously injures domestic industry are:', ['Safeguard measures', 'Embargoes', 'Anti-dumping duties', 'VERs'], 0, "Safeguard measures are temporary, non-discriminatory restrictions — higher duties or quotas — when a sudden surge of imports seriously injures domestic industry, even if the imports are fairly priced. 'Anti-dumping duties' is the trap: they respond to unfair pricing by particular exporters. In practice: India imposed safeguard duties on solar cells in 2018 after a surge of imports hit domestic manufacturers.", 'c7', topic='Non–tariff Measures (NTMs)'),
        M('m33', 'The most extreme form of trade barrier is:', ['An embargo', 'A tariff-rate quota', 'A specific tariff', 'A minimum import price'], 0, 'An embargo is a total ban on trade with a country or region, often for political reasons, so it is the most extreme trade barrier. A tariff-rate quota is tempting as a strict measure, but it still allows imports at a higher duty. In practice: embargoes and sanctions on countries such as Iran have forced Indian refiners and exporters to restructure contracts and payment channels.', 'c7', topic='Non–tariff Measures (NTMs)'),
        M('m34', 'Voluntary export restraints are:', ['Limits imposed by the exporting country on its own exports, usually after negotiation', 'Quantity limits imposed by the importing country', 'Domestic firms limiting foreign sales at home', 'Export taxes'], 0, "Voluntary export restraints are limits that the exporting country places on its own exports, usually after negotiation with the importing country, to avoid harsher restrictions. 'Quantity limits imposed by the importing country' is the trap — that is an import quota. In practice: Japan's restraint on car exports to the US in the 1980s is the classic VER example used in trade studies.", 'c8', topic='Non–tariff Measures (NTMs)'),
        M('m35', 'An export tax tends to:', ['Reduce exports and lower the domestic price', 'Raise exports and the domestic price', 'Raise the domestic price only', 'Have no effect on domestic consumption'], 0, "An export tax makes exporting less profitable, so producers sell more at home; exports fall, domestic supply rises, and the domestic price falls, raising domestic consumption. 'Raise exports and the domestic price' is the trap. In practice: India's export duties on some rice varieties and on onions were used to keep domestic food prices down during shortages.", 'c8', topic='Non–tariff Measures (NTMs)'),
    ]

    cq1 = Checks()
    a1 = cq1.add('500*8000*12/100', 'ad valorem 12% on 500 units at ₹8,000')
    s1 = cq1.add('500*900', 'specific ₹900 on 500 units')
    m1 = cq1.add('500*8000*12/100', 'mixed — ad valorem 4,80,000 is higher than specific 4,50,000')
    c_1 = cq1.add('500*8000*12/100+500*900', 'compound — both')
    q1 = Q('q1', 4, 'moderate', 'table', 'An importer brings in 500 units of a machine part at ₹8,000 each. Compute the duty if the tariff is (a) 12% ad valorem, (b) ₹900 per unit specific, (c) a mixed tariff of (a) or (b) whichever is higher, (d) a compound tariff of (a) plus (b).',
           [table(['Form', 'Working', 'Duty (₹)'], [['(a) Ad valorem', '500 × 8,000 × 12%', a1], ['(b) Specific', '500 × 900', s1], ['(c) Mixed (higher)', f'max({inr(a1)}, {inr(s1)})', m1], ['(d) Compound', f'{inr(a1)} + {inr(s1)}', c_1]])],
           [S('s1', 'Ad valorem duty', 1, 'computation'), S('s2', 'Specific duty', 1, 'computation'), S('s3', 'Mixed = higher of the two', 1, 'application'), S('s4', 'Compound = sum', 1, 'application')],
           ['Most errors come from mixing up "mixed" and "compound".'], ['Adding both for a mixed tariff.', 'Applying 12% to one unit only.'], ['Show the working column — examiners give step marks even if the arithmetic slips.'], checks=cq1)

    cq2 = Checks()
    dd0 = cq2.add('800-4*50', 'demand at ₹50'); ss0 = cq2.add('-40+2*50', 'supply at ₹50')
    dd1 = cq2.add('800-4*60', 'demand at ₹60'); ss1 = cq2.add('-40+2*60', 'supply at ₹60')
    mm0 = cq2.add('600-60', 'imports at ₹50'); mm1 = cq2.add('560-80', 'imports at ₹60')
    cl = cq2.add('(600+560)/2*10', 'consumer surplus loss'); pg = cq2.add('(60+80)/2*10', 'producer surplus gain'); rv = cq2.add('10*480', 'revenue'); dw = cq2.add('5800-700-4800', 'deadweight loss')
    q2 = Q('q2', 6, 'hard', 'table', 'Demand Qd = 800 − 4P; domestic supply Qs = −40 + 2P; world price ₹50 (small country). A ₹10 per unit tariff is imposed. Find imports before and after, the change in consumer and producer surplus, tariff revenue and the net welfare loss.',
           [table(['Item', 'P = ₹50', 'P = ₹60'], [['Demand', dd0, dd1], ['Domestic supply', ss0, ss1], ['Imports', mm0, mm1]], num=[1, 2]),
            table(['Effect', 'Working', '₹'], [['Consumer surplus lost', '(600 + 560) ÷ 2 × 10', cl], ['Producer surplus gained', '(60 + 80) ÷ 2 × 10', pg], ['Tariff revenue', '10 × 480', rv], ['Net (deadweight) loss', f'{inr(cl)} − {inr(pg)} − {inr(rv)}', dw]])],
           [S('s1', 'Quantities at world price', 1, 'computation'), S('s2', 'Quantities at tariff-inclusive price', 1, 'computation'), S('s3', 'Consumer surplus loss (trapezium)', 1, 'computation'),
            S('s4', 'Producer surplus gain', 1, 'computation'), S('s5', 'Revenue on post-tariff imports', 1, 'computation'), S('s6', 'Net loss and interpretation', 1, 'conclusion')],
           ['Strong answers use the trapezium (average of the two quantities × price rise).'], ['Computing revenue on free-trade imports.', 'Raising the world price instead of the domestic price.'], ['Draw a quick demand-supply sketch in rough work first.'], checks=cq2)

    q3 = Q('q3', 4, 'core', 'table', 'Distinguish between anti-dumping duty and countervailing duty.',
           [table(['Basis', 'Anti-dumping duty', 'Countervailing duty'], [
               ['Problem tackled', 'Dumping — export price below home price or below full cost', 'Export subsidies / tax concessions by the exporter\'s government'],
               ['Who causes the distortion', 'The exporting firm\'s pricing policy', 'The exporting government\'s support'],
               ['Purpose', 'Remove the unfair price advantage of the dumper', 'Neutralise the advantage created by the subsidy'],
               ['Condition', 'Serious injury to domestic industry; national interest', 'Subsidised imports causing injury to domestic industry'],
           ])],
           [S('s1', 'Meaning of dumping vs subsidy', 1, 'concept'), S('s2', 'Source of distortion', 1, 'analysis'), S('s3', 'Purpose of each duty', 1, 'concept'), S('s4', 'Condition for levy / example', 1, 'application')],
           ['A four-row table earns full marks; one-line definitions alone earn half.'], ['Saying anti-dumping duty offsets subsidies.'], ['Use "firm vs government" as your key contrast.'])

    jobs = [
        {'id': 'j1', 'title': 'Landed cost under an FTA vs MFN duty', 'role': 'CA in industry (import costing, consumer-durables company)',
         'situation': 'You import compressors from a country with which India has a trade agreement. The MFN duty is 10%; the preferential FTA duty is 2.5% if the goods meet the rules of origin.',
         'steps': ['Obtain the supplier\'s certificate of origin and check the value-addition criterion.', 'Compute landed cost under both rates for a shipment of ₹50,00,000.', 'Weigh the saving against the risk: if origin is later denied, the differential duty plus interest and penalty becomes payable.', 'Document the origin file for audit.'],
         'takeaway': 'Preferential tariffs are valuable only if rules of origin are met and documented.',
         'think': 'What is the duty saving on a ₹50,00,000 shipment?', 'answer': 'MFN 10% = ₹5,00,000; FTA 2.5% = ₹1,25,000; saving ₹3,75,000.',
         'checks': Checks([{'expr': '5000000*10/100-5000000*2.5/100', 'value': 375000, 'label': 'duty saving'}])},
        {'id': 'j2', 'title': 'Domestic producer hurt by cheap imports', 'role': 'CA advising a mid-size steel-products maker',
         'situation': 'Imports of a product from one country are arriving well below that country\'s own home price, and your client\'s order book is shrinking.',
         'steps': ['Collect evidence: export price vs home-market price/cost (dumping margin).', 'Show injury: falling sales, prices, capacity use and profits.', 'Distinguish: if the low price comes from foreign government subsidies, the remedy is a countervailing duty instead.', 'If imports simply surged (no unfair pricing), a safeguard measure is the route.'],
         'takeaway': 'The cause of cheap imports decides the remedy: dumping → anti-dumping; subsidy → CVD; surge → safeguard.'},
    ]

    viva = [
        V('v1', 'Distinguish between a specific tariff and an ad valorem tariff.',
          'A specific tariff is a fixed amount of money per unit of the imported good, while an ad valorem tariff is a fixed percentage of the value of the import. A specific tariff loses protective value when import prices rise, whereas an ad valorem tariff keeps protection constant but encourages under-invoicing.',
          [P('p1', 'Specific = fixed amount per unit (per piece, kg, tonne)', 3, 'specific', 'per unit|each unit|per piece|per kg|per kilo|per tonne|fixed amount|fixed sum|every unit|per item|quantity|weight'),
           P('p2', 'Ad valorem = percentage of value', 3, 'percentage|percent|proportion|share', 'value|price|worth|valor|invoice'),
           P('p3', 'Specific duty loses protection when prices rise; ad valorem keeps it but invites under-invoicing', 4,
             'loses protect|protection fall|protection falls|less protection|protective value fall|protection reduce|inversely|fall when price rise|protection declin|protection go down|protection decreas',
             'under invoic|undervalu|under valu|understat|under-invoic|lower invoice|underinvoic|show lower value|declare lower|constant protection|protection constant|same protection|keeps protection', min=1)], 'c2'),
        V('v2', 'What is a countervailing duty, and when does an importing country levy it?',
          'A countervailing duty is an additional import duty that cancels the price advantage an exporter gets from subsidies or tax concessions given by its own government. The importing country levies it when such subsidised imports are sold at artificially low prices and hurt its domestic industry, so that pricing becomes fair and market based.',
          [P('p1', 'An additional import duty (a tariff)', 2, 'additional|extra|import duty|tariff|duty on import|customs duty'),
           P('p2', 'It offsets subsidies / tax concessions given by the exporter\'s government', 5, 'subsid|tax concession|tax break|government support|government help|government aid|grant|incentive'),
           P('p3', 'Levied when subsidised imports at artificially low prices injure domestic industry — restores fair pricing', 3, 'domestic industr|local industr|domestic producer|home industr|domestic firm|local producer|injur|hurt|harm|fair pric|fair competit|level playing|artificially low|unfair advantage|low price|cheap')], 'c4'),
        V('v7', 'What is dumping, and what is an anti-dumping duty?',
          'Dumping is when a firm sells its goods in a foreign market below the price it charges in its home market or below its full average cost, sometimes to drive out rivals. An anti-dumping duty is an extra import duty that removes this unfair price advantage, justified when the domestic industry is seriously injured and protection is in the national interest.',
          [P('p1', 'Dumping = selling abroad below home-market price or below full cost', 5, 'below home|below cost|below domestic|lower than home|less than cost|below normal|below its own|cheaper than at home|cheaper than in its home|below the price|below price|below average cost|under cost|lower than domestic|lower than its home|less than home|lower price than at home|lower price than home|less than what it charges at home|less than it charges at home|below what it charges|below production cost|below full cost|lower than the price at home'),
           P('p2', 'Anti-dumping duty = additional import duty removing the unfair price advantage', 3, 'additional|extra|import duty|tariff|duty on import|offset|remove|neutralis|cancel|counter'),
           P('p3', 'Justified when domestic industry is seriously injured / national interest', 2, 'injur|hurt|harm|damage|national interest|domestic industr|local industr|domestic producer|predator|drive out|monopol')], 'c4'),
        V('v3', 'What are non-tariff measures and how are they different from non-tariff barriers?',
          'Non-tariff measures are policy measures other than ordinary customs duties that can change the quantity or price of goods traded, such as quotas, SPS rules and technical standards. Non-tariff barriers are the subset of these measures used with a protectionist or discriminatory intent to favour domestic suppliers, so every NTB is an NTM but not every NTM is a barrier.',
          [P('p1', 'NTMs = measures other than ordinary customs tariffs affecting quantity or price of trade', 4, 'other than tariff|other than customs|other than ordinary|not tariff|non tariff measure|ntm|apart from tariff|besides tariff|excluding tariff|other than duty|not customs duty', 'quantit|price|volume|trade flow|trade', min=2),
           P('p2', 'NTBs = NTMs with protectionist / discriminatory intent', 4, 'protection|protectionist|discriminat|favour domestic|favor domestic|unfair|protect domestic|against foreign|favour local|favour home'),
           P('p3', 'NTBs are a subset — not every NTM is an NTB', 2, 'subset|part of|not every|not all|not always|every ntb|every barrier is|all ntbs are|narrower|smaller group|some ntm')], 'c6'),
        V('v4', 'Explain sanitary and phytosanitary measures and technical barriers to trade.',
          'Sanitary and phytosanitary measures protect human, animal and plant life and health from pests, diseases, contaminants and toxins, for example banning poultry from a bird flu affected country. Technical barriers to trade are mandatory standards and technical regulations on size, design, labelling, packaging and performance, with testing and certification. Both are allowed by the WTO but can raise costs and be misused as hidden protection.',
          [P('p1', 'SPS protects human, animal and plant life/health from pests, disease, contaminants', 4, ALT('{s} protect', '{s} measures protect', '{s} {h}', '{s} measures {h}', '{s} measure {h}', s=['sps', 'sanitary', 'phytosanitary'], h=['human', 'animal', 'plant', 'health', 'pest', 'diseas', 'contamin', 'toxin', 'food safety'])),
           P('p2', 'TBT = mandatory standards/technical regulations (labelling, packaging, design) and conformity testing', 4, 'tbt|technical barrier|technical regulation|standard', 'label|packag|design|size|shape|test|certif|inspect|specification|performance|standard', min=2),
           P('p3', 'Permitted by WTO but may raise costs / be misused as protection', 2, 'wto|permit|allowed|legitimate|cost|misuse|misused|protection|hidden|disguis|barrier', min=1)], 'c6'),
        V('v5', 'How does an import quota differ from a tariff?',
          'A quota limits the physical quantity of a good that can be imported in a period, usually through licences, while a tariff is a tax that raises the price of imports. A tariff earns revenue for the government, but under a quota the government gets no revenue and licence holders earn quota rents. Both raise the domestic price, hurt consumers and help domestic producers.',
          [P('p1', 'Quota limits the quantity imported; tariff is a tax on imports', 4, 'quantit|amount|volume|number of unit|physical', 'tax|duty|price|charge'),
           P('p2', 'Tariff earns government revenue; quota earns none — licence holders get quota rents', 4, 'quota rent|licence holder|license holder|licensee|import licence|import license|no revenue|not earn revenue|no government revenue|government get nothing|government earns nothing|without revenue'),
           P('p3', 'Both raise domestic price, hurt consumers, help producers', 2, 'raise price|raise domestic price|higher price|price rise|price goes up|increase price|price increas|consumer lose|consumer worse|consumers lose|consumer surplus|producer gain|producers gain|producer better|protect', min=1)], 'c7'),
        V('v6', 'What is a voluntary export restraint?',
          'A voluntary export restraint is an informal quota under which the exporting country itself limits the quantity it exports to a particular importing country for a period. It is usually agreed after negotiation to appease the importer and avoid harsher retaliation, and like a quota it raises prices in the importing country.',
          [P('p1', 'Exporting country limits its own exports (informal quota)', 5, 'exporting country|exporting nation|exporter itself|exporters themselves|own export|country of export|exporting side|exporting government|export country', 'limit|restrict|restrain|cap|ceiling|quota|reduc|control'),
           P('p2', 'Agreed to appease the importer / avoid retaliation, after negotiation', 3, 'appease|avoid retaliat|retaliat|negotiat|pressure|threat|avoid tariff|avoid harsher|keep importer happy|political'),
           P('p3', 'Raises prices in the importing country', 2, 'price rise|raise price|higher price|price goes up|increase price|price increas|consumer lose|consumer surplus')], 'c8'),
    ]

    cc = Checks()
    case = {'id': 'k1', 'title': 'Solar panels: duties, origin and a dumping complaint', 'difficulty': 'hard',
            'case': ('SunVolt Ltd imports 2,000 solar panels at ₹12,000 each. The tariff is 15% ad valorem or ₹2,000 per panel, whichever is higher. A trade agreement partner country offers panels at a preferential duty of 5% if the rules of origin are met. '
                     'A domestic maker complains that a third country is selling panels in India at ₹9,000 while charging ₹13,500 in its own market. Separately, the importing country requires every panel to pass a performance test and carry a specified label.'),
            'mcqs': [
                M('k1a', 'What duty does SunVolt pay on the 2,000 panels under the mixed tariff?', ['₹40,00,000', '₹36,00,000', '₹76,00,000', '₹12,00,000'], 0, "Value = 2,000 × 12,000 = ₹2,40,00,000. Ad valorem: 15% × 2,40,00,000 = ₹36,00,000. Specific: 2,000 × 2,000 = ₹40,00,000. Under a mixed tariff the higher applies, so SunVolt pays ₹40,00,000. Traps: ₹36,00,000 takes the lower amount; ₹76,00,000 adds both, which is a compound tariff. In practice: SunVolt's customs broker would compute both and pay the higher.", 'c3', 'hard', 'max(2000*12000*15/100, 2000*2000)', topic='Tariffs'),
                M('k1b', 'How much duty would be saved by sourcing the same value from the agreement partner at 5%?', ['₹28,00,000', '₹24,00,000', '₹12,00,000', '₹40,00,000'], 0, 'Preferential duty = 5% × 2,40,00,000 = ₹12,00,000. Saving = 40,00,000 − 12,00,000 = ₹28,00,000. The tempting ₹24,00,000 compares with the ad valorem ₹36,00,000 instead of the actual ₹40,00,000 paid; ₹12,00,000 is the preferential duty itself. In practice: importers claim such FTA savings only if the goods meet the rules of origin, backed by a valid certificate of origin.', 'c3', 'hard', 'max(2000*12000*15/100, 2000*2000)-2000*12000*5/100', topic='Tariffs'),
                M('k1c', 'The third country\'s pricing (₹9,000 in India vs ₹13,500 at home) is evidence of:', ['Dumping — the remedy is an anti-dumping duty', 'Subsidisation — the remedy is a countervailing duty', 'A voluntary export restraint', 'Tariff escalation'], 0, "Selling in India at ₹9,000 while charging ₹13,500 at home is dumping — exporting below the home-market price — and the remedy is an anti-dumping duty, after investigation shows injury. 'Subsidisation with a countervailing duty' is the trap: nothing in the case mentions government subsidies. In practice: the domestic maker would file a petition with DGTR, which investigates before recommending duties.", 'c4', 'moderate', topic='Tariffs'),
                M('k1d', 'The dumping margin per panel, as a percentage of the export price, is:', ['50%', '33.33%', '66.67%', '150%'], 0, 'Dumping margin = (home price − export price) ÷ export price × 100 = (13,500 − 9,000) ÷ 9,000 × 100 = 4,500 ÷ 9,000 × 100 = 50%. The tempting 33.33% divides by the home price; 66.67% is export price ÷ home price; 150% is home price ÷ export price. In practice: DGTR uses the dumping margin to set the maximum anti-dumping duty.', 'c4', 'hard', '(13500-9000)/9000*100', topic='Tariffs'),
                M('k1e', 'The performance-test and labelling requirement is best classified as:', ['A technical barrier to trade (TBT)', 'A sanitary and phytosanitary measure', 'A financial measure', 'An embargo'], 0, "Requiring each panel to pass a performance test and carry a specified label involves product standards and conformity assessment — a technical barrier to trade. 'Sanitary and phytosanitary measure' is the trap: SPS rules protect health from pests, diseases and contaminants, which does not apply to solar panels. In practice: India's BIS certification for solar modules is exactly this kind of TBT requirement.", 'c6', 'core', topic='Non–tariff Measures (NTMs)'),
            ]}

    return _shy({
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p4', 'chapter': 'fnd-p4-ch09', 'n': 2, 'title': 'The Instruments of Trade Policy',
        'outcomes': ['Define trade policy, free trade, protectionism and liberalisation, and classify trade policy instruments.',
                     'Compute specific, ad valorem, mixed, compound and tariff-rate-quota duties and explain bound, applied, MFN, preferential, escalated and prohibitive tariffs.',
                     'Explain trigger-price responses (anti-dumping and countervailing duties) and analyse the welfare effects of a tariff with numbers.',
                     'Classify non-tariff measures (SPS, TBT, quotas, licensing, local content, rules of origin, safeguards, embargoes) and export-related measures (bans, taxes, subsidies, VERs).'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 50, 'practice': 55}, 'prereq': ['fnd-p4-ch09-u01'],
                 'exam_tip': 'Definitions dominate: specific vs ad valorem, mixed vs compound, bound vs applied, anti-dumping vs CVD, NTM vs NTB, SPS vs TBT, VER. Practise one or two duty computations — they are quick marks.'},
        'concepts': concepts, 'illustrations': [ill1, ill2, ill3, ill4], 'jobs': jobs, 'mcqs': mcqs, 'questions': [q1, q2, q3],
        'revision': {'summary': ['Trade policy = all tools to promote/restrict trade; price measures (tariffs) vs non-price measures (NTMs).',
                                 'Specific (per unit; protection falls as price rises) vs ad valorem (% of value; under-invoicing risk).',
                                 'Mixed = either/or (higher); compound = both; TRQ = low rate within quota, high beyond.',
                                 'Bound = legal ceiling; applied ≤ bound; MFN = rate for all WTO members; preferential < MFN; GSP one-way.',
                                 'Escalated: higher duty on processed goods; prohibitive: no imports; import subsidy = negative tariff.',
                                 'Anti-dumping (price below home price/cost) vs CVD (foreign subsidy) — trigger-price mechanisms.',
                                 'Tariff: domestic price ↑, consumers lose, producers gain, government revenue, net deadweight loss.',
                                 'NTBs ⊂ NTMs. Technical: SPS, TBT. Non-technical: quotas (quota rent), price controls, licensing, financial, competition, procurement, TRIMs, distribution, after-sales, red tape, rules of origin, safeguards, embargo.',
                                 'Export measures: bans, export taxes, subsidies, VERs.'],
                     'remember': ['Compound revenue = specific × quantity + ad valorem × price × quantity.', 'Consumer loss = (Q before + Q after) ÷ 2 × price rise.', 'Government earns revenue from a tariff, not from a quota.'],
                     'traps': ['A CVD is a tariff, not an NTM.', 'VER is imposed by the EXPORTING country.', 'A tariff raises the domestic price, not the world price (small country).', 'Safeguards answer import surges; anti-dumping answers unfair pricing.']},
        'quickref': [{'k': 'Specific tariff', 'v': '₹ per unit; no valuation needed; protection ↓ as price ↑'},
                     {'k': 'Ad valorem tariff', 'v': '% of value; constant protection; under-invoicing risk'},
                     {'k': 'Mixed / compound', 'v': 'Higher of the two / sum of the two'},
                     {'k': 'TRQ', 'v': 'Low rate up to quota quantity, higher rate beyond'},
                     {'k': 'Bound vs applied', 'v': 'Applied may be below, never above, bound'},
                     {'k': 'Anti-dumping vs CVD', 'v': 'Below home price/cost vs foreign subsidy'},
                     {'k': 'Tariff welfare', 'v': 'CS loss = PS gain + revenue + deadweight loss'},
                     {'k': 'SPS / TBT', 'v': 'Life & health protection / standards, labels, testing'},
                     {'k': 'VER', 'v': 'Exporter limits its own exports to appease importer'}],
        'viva': viva, 'cases': [case],
    })

# ==== AUTO-CHECK: offline marking keys (kw groups / nums / ai_only per scheme point; read by the app's marker) ====
# kw: viva-matcher keyword groups ("a|b" = alternatives), min = groups needed; nums: figures that must appear
# (magnitudes: the matcher drops minus signs, so a sign that matters is carried by a kw group).


def _K(*kw, min=None, nums=None, **x):
    d = {'kw': list(kw), 'min': len(kw) if min is None else min}
    if nums: d['nums'] = list(nums)
    d.update(x)
    return d


def _N(*nums, kw=None, min=None, **x):
    d = {'nums': list(nums)}
    if kw: d.update(kw=list(kw), min=len(kw) if min is None else min)
    d.update(x)
    return d


AUTO = {
    'q1': {
        's1': _N(480000),
        's2': _N(450000),
        's3': _K('mixed 480000|480000 mixed|higher 480000|max 480000|480000 higher|greater 480000|480000 being higher'),
        's4': _N(930000),
    },
    'q2': {
        's1': _N(600, 60, 540),
        's2': _N(560, 80, 480),
        's3': _N(5800),
        's4': _N(700),
        's5': _N(4800),
        's6': _K('deadweight 300|net loss 300|loss 300|300 loss|300 deadweight|welfare loss 300|dwl 300|4800 300|loss of 300'),
    },
    'q3': {
        'extra_ok': True,
        's1': _K('price below|below home|below normal|lower than home|less than home|below cost|below domestic|lower price|less than normal|below fair', 'subsid'),
        's2': _K('firm|exporter|company|producer|manufacturer', 'government|state'),
        's3': _K('remove|offset|counteract|restore|neutrali|nullif|eliminat|protect', 'advantage|injury|unfair'),
        's4': _K('injury|harm|material', 'domestic industry|domestic producer|local industry|home industry'),
    },
}


_build_content = build


def build():
    u = _build_content()
    for q in u.get('questions', []):
        a = AUTO.get(q['id'], {})
        q['extra_ok'] = a.get('extra_ok', False)
        for s in q['scheme']:
            s.update(a[s['id']])
    return u
