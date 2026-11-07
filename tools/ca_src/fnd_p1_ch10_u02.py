"""CA Foundation · Paper 1 Accounting · Chapter 10 Partnership and LLP Accounts · Unit 2 Treatment of Goodwill in Partnership Accounts.
Original explanations, names and numbers; scope and topic order follow the ICAI study material (May 2027 onwards)."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p1-ch10-u02'


def stmt(title, rows, note_=None):
    return table(['Particulars', '₹'], [[a, inr(b) if isinstance(b, (int, float)) else b] for a, b in rows], title=title, note=note_)


def build():
    # ============ Illustration 1: valuation by every method ============
    c1 = Checks()
    yrs = [('2021-22', 160000), ('2022-23', 180000), ('2023-24', 210000), ('2024-25', 230000), ('2025-26', 270000)]
    wsum = c1.add('160000*1+180000*2+210000*3+230000*4+270000*5', 'Sum of weighted profits')
    wavg = c1.add('3420000/15', 'Weighted average profit')
    savg = c1.add('(160000+180000+210000+230000+270000)/5', 'Simple average profit')
    normal = c1.add('1200000*15/100', 'Normal profit = 15% of capital employed ₹12,00,000')
    sup = c1.add('228000-180000', 'Super profit (weighted average − normal)')
    g_a = c1.add('228000*3', '(a) 3 years\' purchase of weighted average profit')
    g_b = c1.add('210000*3', '(b) 3 years\' purchase of simple average profit')
    g_c = c1.add('48000*4', '(c) 4 years\' purchase of super profit')
    g_d = c1.add('48000*3.3522', '(d) Annuity method — 5 years at 15% (factor 3.3522)')
    g_e = c1.add('48000/(15/100)', '(e) Capitalisation of super profit')
    g_f = c1.add('228000/(15/100)-1200000', '(f) Capitalisation of average profit − capital employed')
    WT = table(['Year', 'Profit (₹)', 'Weight', 'Product (₹)'], [[y, inr(pf), str(i + 1), inr(pf * (i + 1))] for i, (y, pf) in enumerate(yrs)] +
               [['Total', inr(sum(pf for _, pf in yrs)), '15', inr(wsum)]], num=[1, 2, 3], total=True, title='Weighted average (rising trend, so recent years carry more weight)')
    RES = table(['Method', 'Working', 'Goodwill (₹)'], [
        ['(a) Average profit — weighted', '2,28,000 × 3', inr(g_a)], ['(b) Average profit — simple', '2,10,000 × 3', inr(g_b)],
        ['(c) Super profit — number of years\' purchase', '48,000 × 4', inr(g_c)], ['(d) Super profit — annuity', '48,000 × 3.3522', inr(g_d)],
        ['(e) Capitalisation of super profit', '48,000 ÷ 15%', inr(g_e)], ['(f) Capitalisation of average profit', '2,28,000 ÷ 15% − 12,00,000', inr(g_f)]], title='Summary of results')

    # ============ Illustration 2: admission ============
    c2 = Checks()
    na = c2.add('3/5-1/6', "A's new share (13/30)")
    nb = c2.add('2/5-1/12', "B's new share (19/60)")
    c2.add('13/30*60', 'A in sixtieths'); c2.add('19/60*60', 'B in sixtieths'); c2.add('1/4*60', 'C in sixtieths')
    cg = c2.add('240000*1/4', "C's share of goodwill")
    ga = c2.add('60000*2/3', 'Credited to A (sacrifice 1/6 of 1/4 → 2 parts of 3)')
    gb = c2.add('60000*1/3', 'Credited to B (1 part of 3)')
    wa = c2.add('30000*3/5', 'Existing goodwill written off — A (old ratio)')
    wb = c2.add('30000*2/5', 'Existing goodwill written off — B (old ratio)')
    E2 = [
        je('(i)', [("A's Capital A/c", wa), ("B's Capital A/c", wb)], [('Goodwill A/c', 30000)], 'Being goodwill already in the books written off in the old ratio 3:2'),
        je('(ii)', [('Bank A/c', 260000)], [("C's Capital A/c", 200000), ("A's Capital A/c", ga), ("B's Capital A/c", gb)], "Being capital and C's share of goodwill brought in cash; goodwill credited to A and B in the sacrificing ratio 2:1"),
    ]
    E2b = [je('(b)', [("C's Capital A/c", cg)], [("A's Capital A/c", ga), ("B's Capital A/c", gb)], "Being C's share of goodwill adjusted through capital accounts, as C brings no cash for goodwill")]

    # ============ Illustration 3: change in ratio ============
    c3 = Checks()
    pg = c3.add('15/30-10/30', 'P gains (5/30)'); ql = c3.add('10/30-9/30', 'Q sacrifices (1/30)'); rl = c3.add('10/30-6/30', 'R sacrifices (4/30)')
    pp_ = c3.add('180000*5/30', 'P pays'); qq = c3.add('180000*1/30', 'Q receives'); rr = c3.add('180000*4/30', 'R receives')
    E3 = [je('2026 Apr 1', [("P's Capital A/c", pp_)], [("Q's Capital A/c", qq), ("R's Capital A/c", rr)], 'Being goodwill adjusted for the change in ratio from equal to 5:3:2 — gainer debited, sacrificers credited')]
    CR = table(['Partner', 'Old share', 'New share', 'Gain / (sacrifice)', 'Goodwill adjustment (₹)'], [
        ['P', '10/30', '15/30', '+5/30', f'Dr {inr(pp_)}'], ['Q', '10/30', '9/30', '(1/30)', f'Cr {inr(qq)}'], ['R', '10/30', '6/30', '(4/30)', f'Cr {inr(rr)}']], title='Gain and sacrifice')

    # ============ Illustration 4: retirement ============
    c4 = Checks()
    a1 = c4.add('290000+30000', '2024-25 adjusted (add back abnormal fire loss)')
    a2 = c4.add('350000-20000', '2025-26 adjusted (remove non-recurring gain)')
    avg4 = c4.add('(310000+320000+330000)/3', 'Average adjusted profit')
    gw4 = c4.add('320000*2', 'Goodwill — 2 years\' purchase')
    os_ = c4.add('640000*3/10', "O's share of goodwill")
    mg = c4.add('6/10-4/10', "M's gain"); ng = c4.add('4/10-3/10', "N's gain")
    mp = c4.add('192000*2/3', 'M pays (gaining ratio 2:1)'); np_ = c4.add('192000*1/3', 'N pays')
    E4 = [je('2026 Mar 31', [("M's Capital A/c", mp), ("N's Capital A/c", np_)], [("O's Capital A/c", os_)], "Being O's share of goodwill adjusted through the continuing partners' capital accounts in the gaining ratio 2:1")]

    # ============ Q1 ============
    q1 = Checks()
    q1_ce = q1.add('1640000-60000-100000-380000', 'Capital employed')
    q1_ap = q1.add('205000-8000', 'Average maintainable profit (excluding income from non-trade investments)')
    q1_np = q1.add('1100000*10/100', 'Normal profit')
    q1_sp = q1.add('197000-110000', 'Super profit')
    q1_a = q1.add('87000*3', '3 years\' purchase of super profit')
    q1_b = q1.add('87000/(10/100)', 'Capitalisation of super profit')
    q1_c = q1.add('197000/(10/100)-1100000', 'Capitalisation of average profit')

    # ============ Q2 ============
    q2 = Checks()
    q2_z = q2.add('160000*2/8', "Z's share of goodwill (2/8 of ₹1,60,000)")
    q2_cash = q2.add('40000-16000', 'Goodwill brought in cash (₹24,000) — the rest adjusted through capital')
    q2.add('5/8-4/8', "X's sacrifice"); q2.add('3/8-2/8', "Y's sacrifice")
    q2_wx = q2.add('40000*5/8', 'Existing goodwill written off — X'); q2_wy = q2.add('40000*3/8', 'Existing goodwill written off — Y')
    Q2E = [
        je('(i)', [("X's Capital A/c", q2_wx), ("Y's Capital A/c", q2_wy)], [('Goodwill A/c', 40000)], 'Being existing goodwill written off in the old ratio 5:3'),
        je('(ii)', [('Bank A/c', 174000)], [("Z's Capital A/c", 150000), ("X's Capital A/c", 12000), ("Y's Capital A/c", 12000)], 'Being capital and part of goodwill brought in by Z; goodwill shared by X and Y in the sacrificing ratio 1:1'),
        je('(iii)', [("Z's Capital A/c", 16000)], [("X's Capital A/c", 8000), ("Y's Capital A/c", 8000)], "Being balance of Z's share of goodwill adjusted through capital accounts"),
    ]

    # ============ Q4 ============
    q4 = Checks()
    q4_w = q4.add('(150000*1+180000*2+240000*3)/6', 'Weighted average profit')
    q4_g = q4.add('205000*3', 'Goodwill')
    q4_s = q4.add('615000*1/5', "G's share")
    q4_e = q4.add('123000/2', 'E and F each (gaining ratio 1:1)')
    Q4E = [je('2026 Mar 31', [("E's Capital A/c", q4_e), ("F's Capital A/c", q4_e)], [("G's Capital A/c", q4_s)], "Being G's share of goodwill adjusted in the gaining ratio 1:1")]

    # ============ Case ============
    k = Checks()
    k_g = k.add('(140000+160000+180000)/3*2', 'goodwill')
    k_r = k.add('320000*1/5', "Rohan's share")
    k_short = k.add('64000-40000', 'goodwill not brought in cash')

    concepts = [
        {'id': 'c1', 'title': 'What goodwill is and what creates it',
         'body': ['Goodwill is the value of a firm\'s reputation that lets it expect future profits above the normal profits earned by similar businesses. In plain words, it is the likelihood that existing customers keep coming back.',
                  'It is an intangible asset — it cannot be seen or touched — but it is real: a buyer will pay more than the net assets for a business that earns super profits. If net assets are worth ₹5 lakh and a buyer pays ₹6 lakh, ₹1 lakh is paid for goodwill.',
                  'Factors that build goodwill: quality of goods or service; personal reputation and skill of the owners; location (e.g. a busy market); near-monopoly rights such as a sole dealership; trademarks and patents; managerial ability; research that lowers cost or improves quality; favourable long-term contracts for materials.',
                  'Goodwill needs valuing when the profit-sharing ratio changes, a partner is admitted, a partner retires or dies, and when the business is dissolved or sold.'],
         'analogy': 'Two tea stalls sell the same tea at the same price, but one always has a queue. The queue is goodwill — and anyone buying that stall would pay extra for it.',
         'work': 'Valuation of goodwill is a negotiation point in every change of partners; CAs often prepare the valuation note that partners sign.'},
        {'id': 'c2', 'title': 'Accounting standard view: no self-generated goodwill in the books',
         'body': ['Under AS 26 (Intangible Assets), an intangible can be recognised only if it is identifiable, the enterprise controls its future economic benefits, and its cost can be measured reliably. Internally generated (inherent) goodwill fails these tests — it is not separable, its benefits are uncertain and no cost was paid for it — so it is not recognised.',
                  'Only purchased goodwill — goodwill for which money or money\'s worth was actually paid (e.g. paying ₹3 lakh for net assets of ₹2.5 lakh) — may be recorded.',
                  'Therefore, on admission, retirement, death or a change in ratio, Goodwill Account is NOT raised in the books. The agreed value is used only to compensate partners through their capital accounts.',
                  'If a Goodwill Account already exists in the books at the time of reconstitution, it is written off immediately among the old partners in their old ratio, whether it was purchased or not.'],
         'analogy': 'You can\'t put "I am popular" on your balance sheet; you can only show the price you actually paid when you bought someone else\'s popular shop.',
         'work': 'Auditors object when a firm raises goodwill on reconstitution just to inflate capital balances — it overstates assets and misleads banks.'},
        {'id': 'c3', 'title': 'Average profit method — simple and weighted',
         'body': ['Goodwill = average profit × number of years\' purchase. Past profits are first adjusted for abnormal or non-recurring items (fire loss, one-off gains), for expected future changes (e.g. a fair salary to working partners, loss of a contract) and for income from non-trade investments.',
                  'Simple average: total adjusted profits ÷ number of years — used when profits show no clear trend.',
                  'Weighted average: profits multiplied by weights (usually 1, 2, 3 … with the highest weight on the latest year), total ÷ sum of weights — used when profits clearly rise or fall.',
                  'The number of years\' purchase is a matter of judgement and negotiation — it represents how many years the advantage is expected to last.'],
         'analogy': 'Judging a batsman: if his scores are steadily improving, you trust his recent innings more (weighted); if they bounce around, you take his plain average.',
         'work': 'In practice the adjustment of past profits is where most negotiation happens — e.g. whether a one-time government subsidy should be removed.'},
        {'id': 'c4', 'title': 'Super profit methods',
         'body': ['Super profit = average maintainable profit − normal profit, where normal profit = capital employed × normal rate of return (NRR) of similar firms.',
                  'Steps: (1) find capital employed (assets − outside liabilities, excluding goodwill, fictitious assets and non-trade investments); (2) find the average maintainable profit; (3) apply the NRR to capital employed; (4) subtract. No super profit, no goodwill.',
                  '(a) Number of years\' purchase: goodwill = super profit × years.',
                  '(b) Annuity method: goodwill = super profit × present value of an annuity of ₹1 for the given years at the given rate — it recognises the time value of money, so it gives a lower figure than multiplying the super profit by the same number of years.',
                  '(c) Capitalisation of super profit: goodwill = super profit ÷ NRR (× 100 when NRR is in %).',
                  'Logic: an incoming partner pays only for the excess earnings, because normal profit could be earned by investing the same capital in any similar business.'],
         'analogy': 'If any shop in the market earns ₹1 lakh on ₹10 lakh, and yours earns ₹1.4 lakh, the extra ₹40,000 a year is what a buyer pays for.',
         'work': 'Valuers use super-profit logic for professional practices (CA, medical, legal firms) where the partners\' personal skill drives excess earnings.'},
        {'id': 'c5', 'title': 'Capitalisation of average profit',
         'body': ['Normal value of the business = average profit ÷ NRR. Goodwill = normal value − actual capital employed (net assets).',
                  'If the same average profit and capital employed are used, this gives exactly the same figure as capitalising the super profit, because (P ÷ r) − C = (P − r × C) ÷ r.'],
         'analogy': 'Ask: "What would I have to invest elsewhere at the normal rate to earn this profit?" Whatever exceeds the assets actually invested is goodwill.',
         'work': 'This is the crude ancestor of the earnings-capitalisation methods analysts use to value businesses.'},
        {'id': 'c6', 'title': 'Why goodwill is valued when partners change',
         'body': ['Every reconstitution changes future shares: some partners give up part of their share (sacrifice), others get more (gain). The gainers should compensate the sacrificers for the value they give up.',
                  'Sacrifice = old share − new share (positive). Gain = new share − old share (positive). Compensation = goodwill of the firm × fraction sacrificed or gained.'],
         'analogy': 'If you hand over a slice of your pizza to a newcomer, it is fair that the newcomer pays you for that slice — and goodwill decides the price of the whole pizza.',
         'work': 'Disputes on reconstitution are mostly about the sacrifice/gain calculation; a clean ratio table attached to the deed prevents them.'},
        {'id': 'c7', 'title': 'Goodwill on admission of a new partner',
         'body': ['Sacrificing ratio = old share − new share for each old partner. If only the newcomer\'s share is given (and nothing about who gives it up), the old partners sacrifice in their old ratio.',
                  'Case 1 — premium brought in cash: Bank A/c Dr (capital + premium), To New Partner\'s Capital A/c (capital), To Old Partners\' Capital A/cs (premium, in the sacrificing ratio). Only partners who sacrifice get a share.',
                  'Case 2 — no cash for goodwill: New Partner\'s Capital A/c Dr, To Old Partners\' Capital A/cs (his share of goodwill, sacrificing ratio). Partly in cash: combine both entries.',
                  'Case 3 — premium paid privately to the old partners: no entry in the firm\'s books (the amount each receives should still follow the sacrificing ratio).',
                  'Existing goodwill in the books is first written off to the old partners in their old ratio.'],
         'analogy': 'The newcomer buys a ticket to join the profits. If he pays at the counter (cash), the money is passed to the sellers; if he can\'t pay now, the ticket price is entered against his own account.',
         'work': 'When a new partner joins a CA firm, the admission agreement states the goodwill value and whether it is paid in cash or adjusted — the accountant passes exactly these entries.'},
        {'id': 'c8', 'title': 'Goodwill on change in ratio, retirement and death',
         'body': ['Change in profit-sharing ratio (no one joins or leaves): value goodwill; gainers\' capital accounts are debited and sacrificers\' credited with goodwill × fraction gained/sacrificed. A partner with no change is left out.',
                  'Retirement: the continuing partners gain the retiring partner\'s share. Gaining ratio = new share − old share. Entry: Continuing Partners\' Capital A/cs Dr (gaining ratio), To Retiring Partner\'s Capital A/c (his share of goodwill).',
                  'Death: the same entry, crediting the deceased partner\'s capital account (payable to his legal representatives), with goodwill valued on the date of death.',
                  'In every case goodwill is not shown in the balance sheet after the adjustment.'],
         'analogy': 'When a player leaves the team, the players who take over his positions pay him for the advantage they gain.',
         'work': 'Retirement settlements often hinge on the goodwill figure; the retiring partner\'s CA checks the profit adjustments before he signs.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Valuing goodwill by every method', 'difficulty': 'moderate', 'minutes': 15,
         'q': 'Profits of Vardhan & Co.: 2021-22 ₹1,60,000; 2022-23 ₹1,80,000; 2023-24 ₹2,10,000; 2024-25 ₹2,30,000; 2025-26 ₹2,70,000. Capital employed ₹12,00,000; normal rate of return 15%. Present value of an annuity of ₹1 for 5 years at 15% is 3.3522. Value goodwill by: (a) 3 years\' purchase of weighted average profit; (b) 3 years\' purchase of simple average profit; (c) 4 years\' purchase of super profit; (d) annuity method for 5 years; (e) capitalisation of super profit; (f) capitalisation of average profit. Use the weighted average for (c)–(f).',
         'solution': [WT, stmt('Super profit', [('Weighted average profit (34,20,000 ÷ 15)', wavg), ('Less: normal profit (12,00,000 × 15%)', '(1,80,000)'), ('Super profit', sup)]), RES,
                      note(f'Methods (e) and (f) both give ₹{inr(g_e)}: capitalising super profit and capitalising average profit minus capital employed are algebraically the same when the same inputs are used. The annuity value (₹{inr(g_d)}) is below the simple 5-year purchase (₹{inr(sup * 5)}) because later super profits are discounted.')],
         'checks': c1},
        {'id': 'i2', 'title': 'Admission: sacrifice not in the old ratio; premium in cash or adjusted', 'difficulty': 'hard', 'minutes': 15,
         'q': 'A and B share profits 3:2. Their balance sheet shows Goodwill ₹30,000. C is admitted for a 1/4 share, which he takes 1/6 from A and 1/12 from B. Goodwill of the firm is valued at ₹2,40,000. C brings ₹2,00,000 as capital and his share of goodwill in cash. (a) Find the new ratio and the sacrificing ratio and pass the entries. (b) What entry is passed if C brings no cash for goodwill? (c) What if C pays the goodwill privately to A and B?',
         'solution': [wn('Ratios', f'New shares: A = 3/5 − 1/6 = 13/30 = 26/60; B = 2/5 − 1/12 = 19/60; C = 1/4 = 15/60 → new ratio 26:19:15. Sacrificing ratio A 1/6 : B 1/12 = 2:1 (not the old 3:2).'),
                      wn('Goodwill', f'C\'s share = 2,40,000 × 1/4 = ₹{inr(cg)} → A ₹{inr(ga)}, B ₹{inr(gb)}.'),
                      journal(E2, 'Journal — (a) goodwill brought in cash', 'j2'), journal(E2b, 'Journal — (b) no cash for goodwill (replaces the goodwill part of entry (ii))', 'j2b'),
                      p('(c) Paid privately: no entry for goodwill in the firm\'s books; only the capital is recorded (Bank Dr ₹2,00,000, To C\'s Capital). The old goodwill is still written off as in entry (i).')],
         'checks': c2},
        {'id': 'i3', 'title': 'Change in profit-sharing ratio among existing partners', 'difficulty': 'core', 'minutes': 8,
         'q': 'P, Q and R share profits equally. From 1 April 2026 they agree to share 5:3:2. Goodwill is valued at ₹1,80,000. Pass the adjustment entry without raising goodwill.',
         'solution': [CR, journal(E3, 'Journal', 'j3'), note('Only the net effect is passed. Raising goodwill at ₹1,80,000 and writing it off in the new ratio would give the same capital balances but is not allowed under AS 26 for inherent goodwill.')],
         'checks': c3},
        {'id': 'i4', 'title': 'Retirement: adjusted average profits and the gaining ratio', 'difficulty': 'moderate', 'minutes': 12,
         'q': 'M, N and O share profits 4:3:3. O retires on 31 March 2026; M and N will share 3:2. The deed values goodwill at twice the average profit of the last 3 years (2 years\' purchase). Profits: 2023-24 ₹3,10,000; 2024-25 ₹2,90,000 (after an abnormal loss by fire of ₹30,000); 2025-26 ₹3,50,000 (including a non-recurring gain of ₹20,000). Value goodwill and pass the entry.',
         'solution': [stmt('Valuation', [('2023-24', 310000), ('2024-25 (2,90,000 + 30,000 abnormal loss)', a1), ('2025-26 (3,50,000 − 20,000 non-recurring gain)', a2),
                                          ('Average adjusted profit', avg4), ('Goodwill (× 2)', gw4), ("O's share (3/10)", os_)]),
                      wn('Gaining ratio', 'M: 6/10 − 4/10 = 2/10; N: 4/10 − 3/10 = 1/10 → 2:1.'), journal(E4, 'Journal', 'j4')],
         'checks': c4},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Preparing the goodwill note for a new partner\'s admission', 'role': 'Senior article assistant in a CA firm\'s advisory team',
         'situation': 'A design studio with two partners is admitting a third for a 20% share. The partners want goodwill "at 3 years\' purchase of last year\'s profit" — last year included a one-time ₹6 lakh consultancy fee from a client that has since closed.',
         'steps': ['Collect five years\' profits and identify non-recurring items.',
                   'Recommend excluding the one-time fee and deducting a fair salary for the working partners so that profits are "maintainable".',
                   'Show the effect of simple vs weighted average and of the super-profit method in a comparison table for negotiation.',
                   'Once agreed, draft the entries: premium in cash to the old partners in their sacrificing ratio; no Goodwill Account raised.'],
         'takeaway': 'The valuation method matters less than the quality of the profits it is applied to.',
         'think': 'The old partners want to raise Goodwill A/c at the agreed value so that their capital balances look bigger to the bank. Is that acceptable?',
         'answer': 'No. Inherent goodwill cannot be recognised (AS 26); it must be adjusted through capital accounts. Raising it would overstate assets.'},
        {'id': 'j2', 'title': 'Settling a retiring partner\'s goodwill', 'role': 'Accountant of a manufacturing partnership',
         'situation': 'One of four partners retires. The deed says goodwill is two years\' purchase of average profits of three years. The continuing partners will share in a new ratio that is not their old ratio.',
         'steps': ['Compute the gaining ratio from the new and old shares — not the old ratio.',
                   'Value goodwill per the deed after adjusting abnormal items.',
                   'Debit continuing partners in the gaining ratio and credit the retiring partner; write off any goodwill already in the books in the old ratio (all four partners).',
                   'Carry the retiring partner\'s balance to his loan account if payment is deferred.'],
         'takeaway': 'Retirement uses the gaining ratio; using the old ratio is the classic error.',
         'think': 'If one continuing partner\'s share actually falls after the retirement, how is he treated?',
         'answer': 'He has a sacrifice, not a gain, so he is credited (compensated) along with the retiring partner, and the gainers bear the total.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'Under AS 26, internally generated goodwill:', 'options': ['Is not recognised as an asset', 'Is recognised at a valuer\'s estimate', 'Is recognised only on admission of a partner', 'Is recognised and amortised over 10 years'], 'answer': 0, 'explain': "AS 26 prohibits recognising internally generated goodwill because it is not an identifiable resource controlled by the entity and its cost cannot be measured reliably. Only goodwill purchased for consideration can be recorded. The trap 'recognised at a valuer's estimate' would let firms inflate assets with an opinion. In practice: when partners change, goodwill is valued only to adjust capitals among partners, and it is not left in the balance sheet as an asset.", 'topic': "Goodwill", 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'Profits of the last three years are ₹90,000, ₹1,20,000 and ₹1,50,000 (weights 1, 2, 3). The weighted average profit is:', 'options': ['₹1,30,000', '₹1,20,000', '₹1,40,000', '₹1,10,000'], 'answer': 0, 'check': '(90000*1+120000*2+150000*3)/6', 'explain': "Multiply each year's profit by its weight and divide by the sum of weights: (90,000 × 1 + 1,20,000 × 2 + 1,50,000 × 3) ÷ 6 = (90,000 + 2,40,000 + 4,50,000) ÷ 6 = ₹1,30,000. The trap ₹1,20,000 is the simple average, which ignores the weights. In practice: valuers give heavier weight to recent years when a business is growing, as recent profits better predict the future.", 'topic': "Methods for Goodwill Valuation", 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm3', 'q': 'Average profit ₹1,80,000; capital employed ₹10,00,000; normal rate 12%. Goodwill at 3 years\' purchase of super profit is:', 'options': ['₹1,80,000', '₹5,40,000', '₹5,00,000', '₹60,000'], 'answer': 0, 'check': '(180000-1000000*12/100)*3', 'explain': "Normal profit = 10,00,000 × 12% = ₹1,20,000. Super profit = average profit 1,80,000 − 1,20,000 = ₹60,000. Goodwill = 60,000 × 3 years' purchase = ₹1,80,000. The trap ₹5,40,000 multiplies the whole average profit by 3, forgetting that goodwill reflects only the excess over normal profit. In practice: when a CA firm admits a partner, goodwill is often negotiated as a few years' purchase of the firm's above-normal earnings.", 'topic': "Methods for Goodwill Valuation", 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm4', 'q': 'Average profit ₹90,000; normal rate of return 12%; net assets ₹6,20,000. Goodwill by capitalisation of average profit is:', 'options': ['₹1,30,000', '₹7,50,000', '₹1,08,000', '₹16,400'], 'answer': 0, 'check': '90000/(12/100)-620000', 'explain': "Capitalised value of the business = average profit ÷ normal rate = 90,000 ÷ 12% = ₹7,50,000. Goodwill = capitalised value − net assets = 7,50,000 − 6,20,000 = ₹1,30,000. The trap ₹7,50,000 forgets to deduct net assets — that is the whole business's value, not goodwill. In practice: buyers of small businesses estimate what they would pay for the earnings stream and treat the excess over tangible assets as goodwill.", 'topic': "Methods for Goodwill Valuation", 'concept': 'c5', 'difficulty': 'moderate'},
        {'id': 'm5', 'q': 'X and Y share 3:2. Z is admitted and the new ratio is 2:2:1. The sacrificing ratio of X and Y is:', 'options': ['1:0 (only X sacrifices)', '3:2', '1:1', '2:3'], 'answer': 0, 'explain': "Sacrifice = old share − new share. X: 3/5 − 2/5 = 1/5. Y: 2/5 − 2/5 = 0. Only X gives up anything, so the sacrificing ratio is 1 : 0 and all of Z's goodwill compensation goes to X. The trap is the old ratio 3 : 2, which applies only when the old partners give up in their existing ratio. In practice: when a firm admits a partner, the accountant always works out actual sacrifices from old and new ratios rather than assuming them.", 'topic': "Accounting Treatment of Goodwill in Case of Admission of a New Partner", 'concept': 'c7', 'difficulty': 'hard'},
        {'id': 'm6', 'q': 'A and B share 5:3. C joins for 1/4 share (nothing said about who gives it up) and brings ₹40,000 as premium for goodwill. A\'s share of the premium is:', 'options': ['₹25,000', '₹20,000', '₹15,000', '₹10,000'], 'answer': 0, 'check': '40000*5/8', 'explain': "When only the newcomer's share is given and nothing is said about who gives it up, the old partners are assumed to sacrifice in their old ratio, 5 : 3. A's share of the premium = 40,000 × 5/8 = ₹25,000 (B gets ₹15,000). The trap ₹20,000 splits the premium equally. In practice: the premium brought by a new partner is credited to the old partners' capital accounts, and they often withdraw it soon after.", 'topic': "Accounting Treatment of Goodwill in Case of Admission of a New Partner", 'concept': 'c7', 'difficulty': 'core'},
        {'id': 'm7', 'q': 'The incoming partner pays the premium for goodwill privately to the old partners. In the firm\'s books:', 'options': ['No entry is passed for goodwill', 'Goodwill A/c is debited', 'Premium A/c is credited', 'Old partners\' capital accounts are credited'], 'answer': 0, 'explain': "If the new partner pays goodwill premium privately to the old partners outside the business, the money never enters the firm. So no entry for goodwill is passed in the firm's books. The trap is debiting Goodwill A/c — that would raise self-generated goodwill, which AS 26 does not allow. In practice: such private settlements are rare in professional firms because written records help in later disputes and tax scrutiny.", 'topic': "Accounting Treatment of Goodwill in Case of Admission of a New Partner", 'concept': 'c7', 'difficulty': 'core'},
        {'id': 'm8', 'q': 'Goodwill already appearing in the books at the time of admission is:', 'options': ['Written off among old partners in the old ratio', 'Written off among all partners in the new ratio', 'Left in the balance sheet', 'Credited to the new partner'], 'answer': 0, 'explain': "Goodwill already in the books belongs to the old partnership. On admission it is written off by debiting the old partners' capital accounts in their old ratio, so the new partner does not bear any of it. The trap 'among all partners in the new ratio' would unfairly charge the newcomer for goodwill created before he joined. In practice: on admission, the accountant writes off existing goodwill before recording the newcomer's premium, so that capitals reflect fair value.", 'topic': "Accounting Treatment of Goodwill in Case of Admission of a New Partner", 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm9', 'q': 'A, B and C share 3:2:1. C retires; A and B will share equally. The gaining ratio of A and B is:', 'options': ['0:1 — only B gains', '3:2', '1:1', '1:2'], 'answer': 0, 'explain': "Gain = new share − old share. A's gain = 1/2 − 1/2 = nil; B's gain = 1/2 − 1/3 = 1/6. Only B gains, so B alone compensates the retiring partner C for goodwill. The trap 3 : 2 assumes continuing partners gain in their old ratio, which happens only when the new ratio is in that same proportion. In practice: on a partner's retirement, the accountant computes the gaining ratio from the new arrangement so the right partner pays.", 'topic': "Accounting Treatment of Goodwill in Case of Retirement or Death of a Partner", 'concept': 'c8', 'difficulty': 'hard'},
        {'id': 'm10', 'q': 'Super profit ₹25,000 is expected for 5 years; the present value of an annuity of ₹1 for 5 years at 12% is 3.6048. Goodwill by the annuity method is:', 'options': ['₹90,120', '₹1,25,000', '₹2,08,333', '₹75,000'], 'answer': 0, 'check': '25000*3.6048', 'explain': "Under the annuity method, goodwill is the present value of the expected super profits: 25,000 × 3.6048 = ₹90,120. The trap ₹1,25,000 (25,000 × 5) ignores the time value of money — ₹25,000 received in year 5 is worth less today. In practice: valuers and investment bankers discount expected future earnings in the same way when valuing businesses in mergers or acquisitions.", 'topic': "Methods for Goodwill Valuation", 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm11', 'q': 'Which of the following does NOT affect the value of a firm\'s goodwill?', 'options': ['The depreciation method used in its books', 'Location of the business', 'Managerial skill', 'Possession of trademarks and patents'], 'answer': 0, 'explain': "Goodwill reflects a firm's ability to earn more than normal profits. Location, managerial skill and valuable trademarks or patents all create that ability. The depreciation method chosen in the books is only an accounting policy; it shifts profit between years but does not create super earning power. The trap is thinking any factor that changes reported profit changes goodwill. In practice: buyers of a well-known sweet shop pay goodwill for its location and brand, not its accounting methods.", 'topic': "Goodwill", 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm12', 'q': 'The weighted average method is preferred when past profits:', 'options': ['Show a clear rising or falling trend', 'Fluctuate with no pattern', 'Are all equal', 'Include losses in some years'], 'answer': 0, 'explain': "Weighted average gives more importance (higher weights) to recent years. That suits profits with a clear rising or falling trend, since recent years better indicate future earnings. When profits fluctuate without any pattern, the simple average is more appropriate — that is the trap. In practice: a growing start-up's recent profits matter most, so valuers weight them more heavily in deciding a partner's entry premium.", 'topic': "Methods for Goodwill Valuation", 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm13', 'q': 'A, B and C share equally and change to 3:2:1. Goodwill is ₹1,20,000. The adjusting entry is:', 'options': ["A's Capital Dr ₹20,000; To C's Capital ₹20,000", "C's Capital Dr ₹20,000; To A's Capital ₹20,000", "A's Capital Dr ₹20,000; To B's and C's Capital ₹10,000 each", 'No entry is needed'], 'answer': 0, 'explain': "Old shares are 1/3 each. A: 3/6 − 1/3 = 1/6 gain → 1,20,000 × 1/6 = ₹20,000. B: 2/6 − 1/3 = 0. C: 1/6 − 1/3 = −1/6, a sacrifice of ₹20,000. The gaining partner compensates the sacrificing one: A's Capital Dr ₹20,000, To C's Capital ₹20,000. The trap is crediting B, who neither gains nor sacrifices. In practice: when a senior partner takes a smaller role, goodwill adjustments through capital accounts keep the change fair.", 'topic': "Accounting Treatment of Goodwill in Case of Change in Profit Sharing Ratio", 'concept': 'c8', 'difficulty': 'moderate'},
    ]

    questions = [
        {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'The balance sheet of Kaveri & Co. shows total assets of ₹16,40,000, which include goodwill ₹60,000 and non-trade investments ₹1,00,000 (yielding ₹8,000 a year, included in profits). Outside liabilities are ₹3,80,000. The average profit of the last four years is ₹2,05,000. The normal rate of return is 10%. Value goodwill by (a) 3 years\' purchase of super profit, (b) capitalisation of super profit and (c) capitalisation of average profit.',
         'model': [stmt('Capital employed', [('Total assets', 1640000), ('Less: goodwill', '(60,000)'), ('Less: non-trade investments', '(1,00,000)'), ('Less: outside liabilities', '(3,80,000)'), ('Capital employed', q1_ce)]),
                   stmt('Super profit', [('Average profit', 205000), ('Less: income from non-trade investments', '(8,000)'), ('Average maintainable profit', q1_ap), ('Less: normal profit (11,00,000 × 10%)', '(1,10,000)'), ('Super profit', q1_sp)]),
                   table(['Method', 'Working', 'Goodwill (₹)'], [['(a) 3 years\' purchase', '87,000 × 3', inr(q1_a)], ['(b) Capitalisation of super profit', '87,000 ÷ 10%', inr(q1_b)],
                                                             ['(c) Capitalisation of average profit', '19,70,000 − 11,00,000', inr(q1_c)]], title='Goodwill')],
         'checks': q1,
         'scheme': [{'id': 's1', 'pt': 'Capital employed ₹11,00,000 (goodwill, non-trade investments and liabilities excluded)', 'm': 2, 'skill': 'computation'},
                    {'id': 's2', 'pt': 'Average maintainable profit ₹1,97,000', 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Normal profit ₹1,10,000 and super profit ₹87,000', 'm': 1, 'skill': 'computation'},
                    {'id': 's4', 'pt': 'Goodwill (a) ₹2,61,000, (b) and (c) ₹8,70,000', 'm': 2, 'skill': 'computation'}],
         'remarks': ['Many candidates left goodwill and non-trade investments inside capital employed, inflating normal profit.', 'Candidates who excluded the investments from capital employed but forgot to remove their income from profit were inconsistent and lost a mark.'],
         'mistakes': ['Including existing goodwill in capital employed.', 'Not removing non-trade income from average profit.', 'Capitalising average profit without deducting capital employed.'],
         'tips': ['Be consistent: whatever you exclude from capital employed, exclude its income from profit.', 'Present each method in one line with its formula.']},
        {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'hard', 'pad': 'journal',
         'q': 'X and Y share profits 5:3. Goodwill appears in their books at ₹40,000. Z is admitted and the new ratio of X, Y and Z is 4:2:2. Goodwill of the firm is valued at ₹1,60,000. Z brings ₹1,50,000 as capital and ₹24,000 towards goodwill in cash; the rest of his goodwill share is to be adjusted through capital accounts. Pass journal entries.',
         'model': [wn('Sacrificing ratio', 'X: 5/8 − 4/8 = 1/8; Y: 3/8 − 2/8 = 1/8 → 1:1 (not the old ratio 5:3).'),
                   wn("Z's goodwill", f'1,60,000 × 2/8 = ₹{inr(q2_z)}; cash ₹24,000; balance ₹16,000 adjusted.'),
                   journal(Q2E, 'Journal', 'jq2')],
         'checks': q2,
         'scheme': [{'id': 's1', 'pt': 'Existing goodwill ₹40,000 written off in old ratio 5:3', 'm': 1, 'skill': 'concept'},
                    {'id': 's2', 'pt': 'Sacrificing ratio 1:1 computed', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Cash entry: Z capital ₹1,50,000; goodwill ₹24,000 to X and Y equally', 'm': 2, 'skill': 'posting'},
                    {'id': 's4', 'pt': 'Balance ₹16,000 debited to Z\'s capital, credited to X and Y equally', 'm': 1.5, 'skill': 'posting'}],
         'remarks': ['Most candidates shared goodwill in the old ratio 5:3 — the new ratio given in the question changes the sacrifice.', 'Some raised Goodwill A/c for ₹1,60,000, which is not permitted.'],
         'mistakes': ['Using the old ratio as the sacrificing ratio.', 'Forgetting to write off the existing goodwill.', 'Crediting the whole ₹40,000 goodwill share in cash.'],
         'tips': ['Always compute old − new for each partner before distributing goodwill.', 'Write the narration stating the ratio used.']},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'Explain the accounting treatment of goodwill on reconstitution of a partnership firm in the light of the accounting standard on intangible assets.',
         'model': [ul(['AS 26 allows an intangible asset to be recognised only if it is identifiable, its future benefits are controlled and probable, and its cost can be measured reliably.',
                       'Inherent (self-generated) goodwill meets none of these conditions — no price has been paid for it — so it cannot be recorded. Only purchased goodwill can appear in the books.',
                       'On admission, retirement, death or change in ratio, Goodwill Account is not raised. The agreed value is adjusted through partners\' capital accounts: gaining/new partners debited, sacrificing/outgoing partners credited (or premium brought in cash credited to sacrificers).',
                       'Any goodwill already in the books is written off immediately among the old partners in their old ratio.'])],
         'scheme': [{'id': 's1', 'pt': 'Recognition conditions under AS 26', 'm': 1, 'skill': 'concept'},
                    {'id': 's2', 'pt': 'Inherent goodwill not recognised; only purchased goodwill', 'm': 1, 'skill': 'concept'},
                    {'id': 's3', 'pt': 'Adjustment through capital accounts (gainers Dr, sacrificers Cr)', 'm': 1, 'skill': 'application'},
                    {'id': 's4', 'pt': 'Existing goodwill written off in old ratio', 'm': 1, 'skill': 'application'}],
         'remarks': ['Answers that only listed valuation methods missed the point of the question.', 'Naming the standard and stating the recognition conditions earned the first mark easily.'],
         'mistakes': ['Saying goodwill is raised and then written off in the new ratio (an outdated method).', 'Confusing sacrificing ratio with gaining ratio for retirement.'],
         'tips': ['Four crisp points, one per mark.']},
        {'id': 'q4', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'journal',
         'q': 'E, F and G share profits 2:2:1. G retires on 31 March 2026 and E and F will share equally. Goodwill is to be valued at 3 years\' purchase of the weighted average profit of the last three years (weights 1, 2 and 3): 2023-24 ₹1,50,000; 2024-25 ₹1,80,000; 2025-26 ₹2,40,000. Value goodwill and pass the adjusting entry.',
         'model': [stmt('Valuation', [('Weighted profits (1,50,000 × 1 + 1,80,000 × 2 + 2,40,000 × 3)', '12,30,000'), ('Weighted average (÷ 6)', q4_w), ('Goodwill (× 3)', q4_g), ("G's share (1/5)", q4_s)]),
                   wn('Gaining ratio', 'E: 1/2 − 2/5 = 1/10; F: 1/2 − 2/5 = 1/10 → 1:1.'), journal(Q4E, 'Journal', 'jq4')],
         'checks': q4,
         'scheme': [{'id': 's1', 'pt': 'Weighted average ₹2,05,000', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's2', 'pt': "Goodwill ₹6,15,000 and G's share ₹1,23,000", 'm': 1, 'skill': 'computation'},
                    {'id': 's3', 'pt': 'Gaining ratio 1:1', 'm': 1, 'skill': 'computation'},
                    {'id': 's4', 'pt': 'Entry: E and F Dr ₹61,500 each, G Cr ₹1,23,000', 'm': 1.5, 'skill': 'posting'}],
         'remarks': ['Dividing weighted profits by 3 instead of the sum of weights (6) was the most common slip.'],
         'mistakes': ['Dividing by the number of years in a weighted average.', 'Using the old ratio 2:2 as the gaining ratio without checking.'],
         'tips': ['Show the weight table — it earns marks even if the arithmetic slips.']},
    ]

    viva = [
        V('v1', 'What is goodwill, and which factors affect its value?',
          'Goodwill is the value of the reputation of a firm that enables it to earn profits above the normal profits of similar firms in future. It is an intangible asset. Its value depends on factors like the quality of goods, the location, the personal reputation and managerial skill of the owners, monopoly rights, and trademarks and patents.',
          [P('p1', 'Value of reputation → ability to earn more than normal profits', 4, 'reputation|super profit|above normal|more than normal|excess profit|over and above|extra profit'),
           P('p2', 'Intangible asset', 2, 'intangible|cannot be seen|cannot be touched|can t be seen|not physical'),
           P('p3', 'Factors: quality, location, owner\'s reputation/skill, monopoly, trademarks/patents', 4, 'quality|location|skill|monopoly|trademark|patent|management|managerial|contract', min=1)], 'c1'),
        V('v2', 'Why is goodwill not raised in the books on admission or retirement of a partner?',
          'Because of AS 26 on intangible assets. Goodwill that the firm has built itself is internally generated or inherent goodwill. It is not identifiable and its cost cannot be measured reliably since nothing was paid for it, so it cannot be recognised. Only purchased goodwill can be recorded. So on reconstitution the value of goodwill is adjusted through the partners\' capital accounts instead.',
          [P('p1', 'AS 26 / accounting standard on intangibles', 2, 'as 26|26|accounting standard|standard'),
           P('p2', 'Inherent/self-generated goodwill — no cost paid, cannot be measured reliably — not recognised', 4, 'internally generated|inherent|self generated|selfgenerated|own goodwill|built itself|not purchased|nothing paid|no cost|not paid|no consideration'),
           P('p3', 'Only purchased goodwill can be recorded', 2, 'purchased|bought|paid for'),
           P('p4', 'Adjusted through partners\' capital accounts', 2, 'capital account|capital accounts|through capital|partners capital')], 'c2'),
        V('v3', 'Explain the super profit method of valuing goodwill.',
          'First find normal profit by applying the normal rate of return to the capital employed. Super profit is the average maintainable profit minus the normal profit. Goodwill is then the super profit multiplied by the agreed number of years\' purchase. Alternatively it can be valued by the annuity method, discounting the super profits, or by capitalising the super profit at the normal rate of return.',
          [P('p1', 'Normal profit = capital employed × normal rate of return', 3, 'normal profit|normal rate', 'capital employed|capital invested|net assets', min=2),
           P('p2', 'Super profit = average profit − normal profit', 4, 'super profit|excess profit', 'minus normal|less normal|over normal|above normal|exceeds normal|deduct normal|subtract normal|excess over normal|minus the normal|less the normal'),
           P('p3', 'Goodwill = super profit × years\' purchase (or annuity / capitalisation)', 3, 'years purchase|year purchase|number of years|multiplied|multiply|times|annuity|capitalis|capitaliz', min=1)], 'c4'),
        V('v4', 'How is goodwill treated when a new partner is admitted?',
          'If the new partner brings his share of goodwill in cash as premium, Bank is debited and the old partners\' capital accounts are credited in their sacrificing ratio. If he cannot bring it in cash, his capital account is debited and the old partners\' capital accounts are credited in the sacrificing ratio. If he pays the premium privately to the old partners, no entry is made in the firm\'s books. Existing goodwill is written off in the old ratio.',
          [P('p1', 'Premium in cash → credited to old partners in sacrificing ratio', 4, 'cash|bank|premium', 'sacrific'),
           P('p2', 'No cash → new partner\'s capital debited, old partners credited', 3, 'new partner capital debit|debit new partner|new partner s capital account is debit|debit his capital|his capital account debit|capital of new partner debit|charged to new partner|debiting new partner|new partner capital account debit|his capital account is debit|capital account debit'),
           P('p3', 'Paid privately → no entry; existing goodwill written off in old ratio', 3, 'private|privately|outside the firm|outside the books|directly to', 'no entry|not recorded|nothing recorded|no record|not entered|old ratio', min=1)], 'c7'),
        V('v5', 'Which ratio is used to adjust goodwill on retirement or death, and how is it calculated?',
          'On retirement or death the gaining ratio is used, because the continuing partners gain the share of the outgoing partner. Gaining ratio is the new share minus the old share of each continuing partner. The continuing partners\' capital accounts are debited in the gaining ratio and the retiring partner\'s or deceased partner\'s capital account is credited with his share of goodwill.',
          [P('p1', 'Gaining ratio', 4, 'gaining ratio|gain ratio|ratio of gain|gaining'),
           P('p2', 'Gain = new share − old share', 3, 'new share minus old|new minus old|new share less old|new share old share|new ratio minus old|new less old|difference between new and old'),
           P('p3', 'Continuing partners debited; outgoing partner credited', 3, 'continuing|remaining|other partners', 'debit', 'credit', min=2)], 'c8'),
        V('v6', 'When would you use a weighted average instead of a simple average of profits?',
          'A weighted average is used when past profits show a clear rising or falling trend, so that recent years, which better reflect the future, get more weight; the highest weight goes to the latest year. When profits fluctuate without any clear trend, a simple average is used.',
          [P('p1', 'Weighted average when there is a clear trend (rising/falling)', 4, 'trend|increasing|decreasing|rising|falling|growing|declining'),
           P('p2', 'Higher weight to recent years', 3, 'recent|latest|current year|last year'),
           P('p3', 'Simple average when no clear trend / fluctuating', 3, ALT('simple {f}', 'simple average {f}', '{f} simple', f=('fluctuat', 'fluctuate', 'irregular', 'no trend', 'no clear trend', 'without trend', 'without a trend', 'without any trend', 'without any clear trend', 'without a clear trend', 'no pattern', 'random', 'up and down', 'erratic', 'varying')))], 'c3'),
    ]

    cases_ = [{
        'id': 'k1', 'title': 'Sohan & Mohan admit Rohan', 'difficulty': 'hard',
        'case': ('Sohan and Mohan share profits 3:1. On 1 April 2026 they admit Rohan for a 1/5 share, which he takes entirely from Sohan. Goodwill will be taken as twice (2 years\' purchase) the average profit of the last three years: ₹1,40,000, ₹1,60,000 and ₹1,80,000. '
                 'Rohan brings ₹2,50,000 as capital but only ₹40,000 towards his share of goodwill in cash. No goodwill appears in the books.'),
        'mcqs': [
            M('k1a', 'The new profit-sharing ratio of Sohan, Mohan and Rohan is:', ['11:5:4', '3:1:1', '12:4:5', '2:1:1'], 0,
              "Rohan takes his 1/5 entirely from Sohan. Sohan: 3/4 − 1/5 = 15/20 − 4/20 = 11/20. Mohan keeps 1/4 = 5/20. Rohan has 1/5 = 4/20. New ratio = 11 : 5 : 4. The trap 3 : 1 : 1 assumes Rohan's share comes from both old partners in some ratio, rather than wholly from Sohan. In practice: new partners in family firms often take their share from the senior partner who is slowing down.", 'hard') | {'topic': "Accounting Treatment of Goodwill in Case of Admission of a New Partner"},
            M('k1b', 'Goodwill of the firm is valued at:', [R(k_g), R(160000), R(360000), R(480000)], 0,
              "Average profit = (1,40,000 + 1,60,000 + 1,80,000) ÷ 3 = ₹1,60,000. Goodwill = 2 years' purchase = 1,60,000 × 2 = ₹3,20,000. The trap ₹1,60,000 forgets to multiply by the years' purchase; ₹4,80,000 multiplies the average by 3. In practice: the years' purchase reflects how long the firm's advantage is expected to last, agreed between partners.", 'core', '(140000+160000+180000)/3*2') | {'topic': "Methods for Goodwill Valuation"},
            M('k1c', 'Total amount credited to Sohan\'s capital for goodwill (cash plus adjustment) is:', [R(k_r), R(48000), R(40000), R(16000)], 0,
              "Rohan's share of goodwill = 3,20,000 × 1/5 = ₹64,000. Because Sohan alone gives up the share, all ₹64,000 is credited to Sohan — ₹40,000 from the cash brought and ₹24,000 by adjustment through Rohan's capital. The trap ₹48,000 splits the goodwill between Sohan and Mohan in the old 3 : 1 ratio, but Mohan sacrifices nothing. In practice: goodwill compensation always follows the actual sacrifice.", 'hard', '320000*1/5') | {'topic': "Accounting Treatment of Goodwill in Case of Admission of a New Partner"},
            M('k1d', 'The entry for the goodwill not brought in cash is:', [f"Rohan's Capital A/c Dr {R(k_short)}; To Sohan's Capital A/c", f"Goodwill A/c Dr {R(k_short)}; To Sohan's Capital A/c", f"Sohan's Capital A/c Dr {R(k_short)}; To Rohan's Capital A/c", 'No entry is required'], 0,
              "Rohan's goodwill share is ₹64,000 but he brings only ₹40,000 in cash. The ₹24,000 shortfall is charged to his capital account and credited to the sacrificing partner: Rohan's Capital A/c Dr ₹24,000, To Sohan's Capital A/c ₹24,000. The trap is debiting Goodwill A/c — that would raise internally generated goodwill, which AS 26 does not allow. In practice: newcomers short of cash often settle goodwill through their capital account.", 'moderate') | {'topic': "Accounting Treatment of Goodwill in Case of Admission of a New Partner"},
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch10', 'n': 2,
        'title': 'Treatment of Goodwill in Partnership Accounts',
        'outcomes': [
            'Explain the meaning of goodwill, the factors that affect it and when it needs to be valued.',
            'Apply the accounting standard rule that inherent goodwill is not recognised and adjust goodwill through capital accounts instead.',
            'Value goodwill by the average profit (simple and weighted), super profit (years\' purchase, annuity, capitalisation) and capitalisation of average profit methods.',
            'Compute sacrificing and gaining ratios and pass goodwill entries on admission, change in ratio, retirement and death.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 60}, 'prereq': ['fnd-p1-ch10-u01'],
                 'exam_tip': 'Goodwill appears inside almost every admission, retirement and death question. Get the sacrifice/gain table right first — the entries follow automatically.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Goodwill = value of reputation that yields profits above normal; an intangible asset.',
                        'AS 26: inherent goodwill is never recognised; only purchased goodwill. On reconstitution adjust through capital accounts; write off existing goodwill in the old ratio.',
                        'Average profit method: adjusted average (simple or weighted) × years\' purchase.',
                        'Super profit = average profit − capital employed × NRR; goodwill = super profit × years, × annuity factor, or ÷ NRR.',
                        'Admission → sacrificing ratio; retirement/death → gaining ratio; change in ratio → gainers pay sacrificers.'],
            'remember': ['Sacrifice = old − new; gain = new − old.', 'Only newcomer\'s share given → sacrifice in old ratio.', 'Private premium → no entry.', 'Capitalisation of super profit = capitalisation of average profit − capital employed.'],
            'traps': ['Don\'t raise Goodwill A/c on reconstitution.', 'Don\'t divide a weighted total by the number of years.', 'Don\'t include goodwill or non-trade investments in capital employed.', 'Don\'t assume the gaining ratio equals the new ratio.'],
        },
        'quickref': [
            {'k': 'Simple average method', 'v': 'Goodwill = (Σ adjusted profits ÷ n) × years\' purchase'},
            {'k': 'Weighted average', 'v': 'Σ(profit × weight) ÷ Σ weights'},
            {'k': 'Normal profit', 'v': 'Capital employed × normal rate of return'},
            {'k': 'Super profit', 'v': 'Average maintainable profit − normal profit'},
            {'k': 'Annuity method', 'v': 'Super profit × PV of annuity of ₹1 for n years at r%'},
            {'k': 'Capitalisation (super profit)', 'v': 'Super profit × 100 ÷ NRR'},
            {'k': 'Capitalisation (average profit)', 'v': 'Average profit × 100 ÷ NRR − capital employed'},
            {'k': 'Admission entry (cash)', 'v': 'Bank Dr; To New partner\'s capital; To Old partners\' capital (sacrificing ratio)'},
            {'k': 'Retirement/death entry', 'v': 'Continuing partners\' capital Dr (gaining ratio); To Outgoing partner\'s capital'},
        ],
        'viva': viva, 'cases': cases_,
    }
