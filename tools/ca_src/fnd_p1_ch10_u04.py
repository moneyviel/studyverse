"""CA Foundation · Paper 1 Accounting · Chapter 10 Partnership and LLP Accounts · Unit 4 Retirement of a Partner.
Original explanations, names and numbers (structure and scope follow the ICAI study material)."""
from fractions import Fraction as F
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M
from fnd_p1_ch10_u03 import tacc, capacc, split, ratio, fr, amt

UID = 'fnd-p1-ch10-u04'


def loan_schedule(principal, n, rate, label):
    """Equal principal instalments + interest on the opening balance. Returns (rows, total interest, list of yearly payments, checks)."""
    c = Checks()
    inst = c.add(f'{principal}/{n}', f'{label}: annual instalment of principal')
    rows, bal, tot_i, pays = [], principal, 0, []
    for y in range(1, n + 1):
        i = c.add(f'{bal}*{rate}/100', f'Year {y} interest @{rate}% on {inr(bal)}')
        pay = c.add(f'{inst}+{i}', f'Year {y} total payment')
        rows.append([f'Year {y}', inr(bal), inr(i), inr(inst), inr(pay), inr(bal - inst)])
        tot_i += i; pays.append((bal, i, inst, pay)); bal -= inst
    rows.append(['Total', '', inr(tot_i), inr(principal), inr(principal + tot_i), ''])
    return rows, tot_i, pays, c


def loan_ledgers(name, pays, from_ac, rate):
    out = []
    for y, (bal, i, inst, pay) in enumerate(pays, 1):
        cr = ([{'date': 'Start Y1', 'part': f'By {from_ac}', 'amt': bal}] if y == 1 else [{'date': f'Start Y{y}', 'part': 'By Balance b/d', 'amt': bal, 'ob': True}])
        cr.append({'date': f'End Y{y}', 'part': f'By Interest A/c ({rate}% on {inr(bal)})', 'amt': i})
        dr = [{'date': f'End Y{y}', 'part': f'To Bank A/c ({inr(inst)} + {inr(i)})', 'amt': pay}]
        blk = {'t': 'ledger', 'ac': f"{name}'s Loan Account — Year {y}", 'dr': dr, 'cr': cr}
        if bal - inst:
            dr.append({'date': f'End Y{y}', 'part': 'To Balance c/d', 'amt': bal - inst, 'bal': True})
            blk['next'] = {'date': f'Start Y{y + 1}', 'side': 'cr', 'amt': bal - inst}
        out.append(blk)
    return out


def build():
    # ============ Illustration 1: gaining ratio — four situations ============
    c1 = Checks()
    A, B, C = F(4, 9), F(3, 9), F(2, 9)
    rows = []
    rows.append(['(a) Nothing agreed about the new ratio', 'Strike out Bela: Asha 4, Chirag 2', ratio(A, C), ratio(A, C) + ' (old ratio between them)'])
    ga, gc = F(1, 2) - A, F(1, 2) - C
    c1.add('1/2-4/9', '(b) Asha gains 1/18'); c1.add('1/2-2/9', '(b) Chirag gains 5/18')
    rows.append(['(b) Asha and Chirag agree to share equally', 'Gain = new − old: Asha 1/2 − 4/9 = 1/18; Chirag 1/2 − 2/9 = 5/18', '1:1', ratio(ga, gc)])
    c1.add('4/9+1/9', '(c) Asha new share 5/9'); c1.add('2/9+2/9', '(c) Chirag new share 4/9')
    rows.append(['(c) Asha takes 1/9 and Chirag 2/9 of Bela\'s share', 'New = old + gain: Asha 4/9 + 1/9 = 5/9; Chirag 2/9 + 2/9 = 4/9', ratio(A + F(1, 9), C + F(2, 9)), ratio(F(1, 9), F(2, 9))])
    c1.add('4/9+3/9*2/3', '(d) Asha new share 6/9'); c1.add('2/9+3/9*1/3', '(d) Chirag new share 3/9')
    rows.append(['(d) Bela\'s share taken by Asha and Chirag in 2:1', 'Asha 4/9 + (3/9 × 2/3) = 6/9; Chirag 2/9 + (3/9 × 1/3) = 3/9', ratio(A + B * F(2, 3), C + B * F(1, 3)), '2:1'])
    assert [r[2] for r in rows] == ['2:1', '1:1', '5:4', '2:1'] and [r[3][:3] for r in rows] == ['2:1', '1:5', '1:2', '2:1']
    gain_tbl = table(['Situation (Asha:Bela:Chirag = 4:3:2, Bela retires)', 'Working', 'New ratio Asha:Chirag', 'Gaining ratio'], rows, title='New ratio and gaining ratio',
                     note='When the continuing partners take over the retiring partner\'s share in their own old ratio, the gaining ratio is simply their old ratio.')

    # ============ Illustration 2: full retirement (Kapoor, Lal, Mehra) ============
    c2 = Checks()
    old = {'Kapoor': F(5, 10), 'Lal': F(3, 10), 'Mehra': F(2, 10)}
    gK = c2.add('3/5-5/10', "Kapoor's gain 1/10"); gM = c2.add('2/5-2/10', "Mehra's gain 2/10")
    gw_L = c2.add('120000*3/10', "Lal's share of goodwill")
    gwK = c2.add('36000*1/3', 'Debited to Kapoor (gaining ratio 1:2)'); gwM = c2.add('36000*2/3', 'Debited to Mehra')
    pdd = c2.add('90000*4/100', 'Provision @4% on receivables')
    rev = c2.add('30000-10000-3600-2400+2000', 'Profit on revaluation')
    rv = split(rev, old)
    res = split(40000, old)
    capL = c2.add('150000+12000+4800+36000', "Lal's total claim")
    loanL = c2.add('202800-32800', "Balance transferred to Lal's loan")
    capK = c2.add('200000+20000+8000-12000', "Kapoor's closing capital")
    capM = c2.add('100000+8000+3200-24000', "Mehra's closing capital")
    bank = c2.add('40000-32800', 'Bank after paying Lal')
    c2.add('68000+170000+216000+87200', 'Balance sheet total')
    c2.add('270000+100000+77600+(90000-3600)+7200', 'Assets total')
    E2 = [
        je('2026 Apr 1', [('Land and Building A/c', 30000), ('Trade Payables A/c', 2000)], [('Revaluation A/c', 32000)], 'Being increase in building and a payable written back'),
        je('Apr 1', [('Revaluation A/c', 16000)], [('Plant A/c', 10000), ('Provision for Doubtful Debts A/c', pdd), ('Inventory A/c', 2400)], 'Being decrease in plant and inventory and provision created'),
        je('Apr 1', [('Revaluation A/c', rev)], [("Kapoor's Capital A/c", rv['Kapoor']), ("Lal's Capital A/c", rv['Lal']), ("Mehra's Capital A/c", rv['Mehra'])], 'Being revaluation profit shared 5:3:2 by all partners including Lal'),
        je('Apr 1', [('General Reserve A/c', 40000)], [("Kapoor's Capital A/c", res['Kapoor']), ("Lal's Capital A/c", res['Lal']), ("Mehra's Capital A/c", res['Mehra'])], 'Being general reserve transferred in the old ratio'),
        je('Apr 1', [("Kapoor's Capital A/c", gwK), ("Mehra's Capital A/c", gwM)], [("Lal's Capital A/c", gw_L)], "Being Lal's share of goodwill debited to the gaining partners in their gaining ratio 1:2"),
        je('Apr 1', [("Lal's Capital A/c", capL)], [('Bank A/c', 32800), ("Lal's Loan A/c", loanL)], "Being ₹32,800 paid to Lal and the balance transferred to his loan account"),
    ]
    rev2 = tacc([('To Plant A/c', 10000), ('To Provision for Doubtful Debts A/c', pdd), ('To Inventory A/c', 2400),
                 ("To Kapoor's Capital A/c (5/10)", rv['Kapoor']), ("To Lal's Capital A/c (3/10)", rv['Lal']), ("To Mehra's Capital A/c (2/10)", rv['Mehra'])],
                [('By Land and Building A/c', 30000), ('By Trade Payables A/c', 2000)], title='Revaluation Account')
    cap2, bal2 = capacc(['Kapoor', 'Lal', 'Mehra'],
                        [("To Lal's Capital A/c (goodwill)", {'Kapoor': gwK, 'Mehra': gwM}), ('To Bank A/c', {'Lal': 32800}), ("To Lal's Loan A/c", {'Lal': loanL})],
                        [('By Balance b/d', {'Kapoor': 200000, 'Lal': 150000, 'Mehra': 100000}), ('By General Reserve A/c', res), ('By Revaluation A/c', rv),
                         ('By Kapoor and Mehra (goodwill)', {'Lal': gw_L})])
    assert bal2 == {'Kapoor': capK, 'Lal': 0, 'Mehra': capM}, bal2
    bs2 = tacc([('Trade payables (70,000 − 2,000)', 68000), ("Lal's loan", loanL), ("Kapoor's capital", capK), ("Mehra's capital", capM)],
               [('Land and building', 270000), ('Plant', 100000), ('Inventory', 77600), ('Trade receivables 90,000 less provision 3,600', 86400), ('Bank', bank)],
               lh='Liabilities', rh='Assets', title='Balance Sheet of Kapoor and Mehra as at 1 April 2026')

    # ============ Illustration 3: loan in instalments ============
    rows3, ti3, pays3, c3 = loan_schedule(170000, 4, 10, "Lal's loan")
    sched3 = table(['Year', 'Opening balance (₹)', 'Interest @10% (₹)', 'Principal instalment (₹)', 'Total paid (₹)', 'Closing balance (₹)'], rows3, num=[2, 3, 4], total=True, title="Repayment schedule of Lal's loan")
    led3 = loan_ledgers('Lal', pays3[:2], "Lal's Capital A/c", 10)

    # ============ Illustration 4: JLP and separate life policies ============
    c4 = Checks()
    oldN = {'Nair': F(2, 5), 'Oberoi': F(2, 5), 'Pillai': F(1, 5)}
    sv = 60000
    jA = split(sv, oldN)
    c4.add('60000*1/5', "Pillai's share of JLP surrender value")
    exc = c4.add('60000-52000', 'Method 2: only the excess over the book value is a gain')
    jB = split(exc, oldN)
    tot_sv = c4.add('40000+35000+25000', 'Total surrender value of the three separate policies')
    pil = c4.add('100000*1/5', "Pillai's share of separate policies")
    jlp_tbl = table(['Method of accounting for premium', 'Position in books before retirement', 'Entry on Pillai\'s retirement (SV ₹60,000)', "Pillai's benefit (₹)"], [
        ['1. Premium charged to P&L each year', 'Policy not in the books', 'Joint Life Policy A/c Dr ₹60,000 To Nair ₹24,000, Oberoi ₹24,000, Pillai ₹12,000 (or through Revaluation A/c)', inr(jA['Pillai'])],
        ['2. Premium debited to policy; kept at surrender value', 'Policy shown at last SV ₹52,000', 'Joint Life Policy A/c Dr ₹8,000 To Revaluation A/c (gain shared 2:2:1)', '1,600 more (12,000 in all)'],
        ['3. Policy at SV with a Joint Life Policy Reserve', 'Policy ₹60,000 (asset) and Reserve ₹60,000 (liability)', 'Joint Life Policy Reserve A/c Dr ₹60,000 To Nair ₹24,000, Oberoi ₹24,000, Pillai ₹12,000', inr(jA['Pillai'])],
    ], title='Joint life policy — three methods, same economic result',
        note='In every method Pillai ends up credited with 1/5 of the current surrender value. The policy itself continues for the remaining partners.')
    E4 = [je('2026 Oct 1', [('Life Policies A/c', tot_sv)], [("Nair's Capital A/c", 40000), ("Oberoi's Capital A/c", 40000), ("Pillai's Capital A/c", pil)],
             'Being surrender value of all separate policies brought into the books and credited 2:2:1 on Pillai\'s retirement')]

    # ============ Questions ============
    qc1 = Checks()
    gP = qc1.add('3/5-3/6', "Pari's gain 3/30"); gR = qc1.add('2/5-1/6', "Rhea's gain 7/30")
    qres = split(36000, {'Pari': F(3, 6), 'Qadir': F(2, 6), 'Rhea': F(1, 6)})
    adjP = qc1.add('12000*3/10', "Pari's share of Qadir's reserve (keep-reserve method)")
    adjR = qc1.add('12000*7/10', "Rhea's share")
    gwP = qc1.add('90000*2/6*3/10', 'Goodwill debited to Pari'); gwR = qc1.add('90000*2/6*7/10', 'Goodwill debited to Rhea')
    Q1 = [
        je('(i)', [('General Reserve A/c', 36000)], [("Pari's Capital A/c", qres['Pari']), ("Qadir's Capital A/c", qres['Qadir']), ("Rhea's Capital A/c", qres['Rhea'])], 'Being reserve distributed in the old ratio 3:2:1 on Qadir\'s retirement'),
        je('(ii) alt.', [("Pari's Capital A/c", adjP), ("Rhea's Capital A/c", adjR)], [("Qadir's Capital A/c", 12000)], "Being Qadir's share of reserve adjusted in the gaining ratio 3:7 (reserve kept in the books)"),
        je('(iii)', [("Pari's Capital A/c", gwP), ("Rhea's Capital A/c", gwR)], [("Qadir's Capital A/c", 30000)], "Being Qadir's share of goodwill (₹90,000 × 2/6) adjusted in the gaining ratio 3:7"),
    ]

    qc2 = Checks()
    oldG = {'Gupta': F(2, 5), 'Hegde': F(2, 5), 'Iyer': F(1, 5)}
    q2rev = qc2.add('40000-6000-5000+4000', 'Profit on revaluation')
    q2rv = split(q2rev, oldG); q2res = split(30000, oldG)
    q2gw = qc2.add('75000*1/5', "Iyer's share of goodwill")
    qc2.add('1/2-2/5', 'Each continuing partner gains 1/10 → gaining ratio 1:1')
    q2I = qc2.add('80000+6000+6600+15000', "Iyer's total claim")
    q2loan = qc2.add('107600-27600', "Iyer's loan")
    q2G = qc2.add('160000+12000+13200-7500', "Gupta's closing capital")
    q2H = qc2.add('120000+12000+13200-7500', "Hegde's closing capital")
    q2bank = qc2.add('34000-27600', 'Bank balance')
    qc2.add('50000+80000+177700+137700', 'Balance sheet total')
    q2revT = tacc([('To Furniture A/c', 6000), ('To Provision for Doubtful Debts A/c', 5000), ("To Gupta's Capital A/c (2/5)", q2rv['Gupta']), ("To Hegde's Capital A/c (2/5)", q2rv['Hegde']), ("To Iyer's Capital A/c (1/5)", q2rv['Iyer'])],
                  [('By Premises A/c', 40000), ('By Creditors A/c', 4000)], title='Revaluation Account')
    q2cap, q2bal = capacc(['Gupta', 'Hegde', 'Iyer'],
                          [("To Iyer's Capital A/c (goodwill)", {'Gupta': 7500, 'Hegde': 7500}), ('To Bank A/c', {'Iyer': 27600}), ("To Iyer's Loan A/c", {'Iyer': q2loan})],
                          [('By Balance b/d', {'Gupta': 160000, 'Hegde': 120000, 'Iyer': 80000}), ('By General Reserve A/c', q2res), ('By Revaluation A/c', q2rv), ('By Gupta and Hegde (goodwill)', {'Iyer': q2gw})])
    assert q2bal == {'Gupta': q2G, 'Hegde': q2H, 'Iyer': 0}, q2bal
    q2bs = tacc([('Creditors (54,000 − 4,000)', 50000), ("Iyer's loan", q2loan), ("Gupta's capital", q2G), ("Hegde's capital", q2H)],
                [('Premises (2,00,000 + 20%)', 240000), ('Furniture', 34000), ('Inventory', 70000), ('Debtors 1,00,000 less provision 5,000', 95000), ('Bank', q2bank)],
                lh='Liabilities', rh='Assets', title='Balance Sheet of Gupta and Hegde as at 30 June 2026')

    rows_q3, ti_q3, pays_q3, qc3 = loan_schedule(120000, 3, 12, "Ravi's loan")
    led_q3 = loan_ledgers('Ravi', pays_q3, "Ravi's Capital A/c", 12)

    # ============ Case ============
    kc = Checks()
    k_g = ratio(F(3, 5) - F(5, 10), F(2, 5) - F(2, 10))
    assert k_g == '1:2'
    k_vg = kc.add('100000*3/10*2/3', "Varun's debit for Uma's goodwill")
    k_j = kc.add('40000*3/10', "Uma's share of JLP surrender value")
    k_due = kc.add('150000+20000*3/10+30000+12000', 'Total due to Uma')

    concepts = [
        {'id': 'c1', 'title': 'Retirement: the firm continues, one partner leaves',
         'body': ['A partner may retire because of age, health, a new career or a dispute. The firm does not close: the remaining (continuing) partners carry on the business, so it is a reconstitution.',
                  'The continuing partners take over the retiring partner\'s share of future profits — they gain. In return, they must settle everything that is due to him: his capital, his share of reserves and undistributed profits, his share of revaluation profit (or loss), his share of goodwill, and his share of any joint life policy.',
                  'Steps: (1) new ratio and gaining ratio, (2) revaluation, (3) reserves, (4) goodwill, (5) life policy, (6) find the final balance of the retiring partner and settle it — in cash, as a loan, or in instalments.'],
         'analogy': 'A flatmate moving out: the others take over her room, and in exchange they refund her deposit and her share of everything bought together.',
         'work': 'A retirement settlement statement is one of the most sensitive documents an accountant prepares — the retiring partner (often with his own adviser) checks every line before signing the release deed.'},
        {'id': 'c2', 'title': 'Gaining ratio and the new ratio',
         'body': ['Gain of a continuing partner = new share − old share. The ratio of these gains is the gaining (benefit) ratio. It is used to debit the continuing partners with the retiring partner\'s share of goodwill.',
                  'If nothing is said, the continuing partners share in their old ratio — strike out the retiring partner\'s figure — and the gaining ratio is their old ratio.',
                  'If the new ratio is given, compute gains = new − old for each. If the gains (the parts of the retiring partner\'s share each one takes) are given, new share = old share + gain.'],
         'analogy': 'When one player leaves a relay team, the others run his leg; who runs how much of it decides who "gained" his lap.',
         'work': 'Goodwill compensation paid by the continuing partners is a real cost to each of them. If the gaining ratio is wrong, one partner pays for a share he never received.'},
        {'id': 'c3', 'title': 'Revaluation on retirement',
         'body': ['Assets and liabilities are revalued exactly as on admission, through a Revaluation (Profit and Loss Adjustment) Account.',
                  'The profit or loss belongs to ALL the existing partners, including the one who is retiring, in the OLD ratio — he was an owner while the values changed.',
                  'If the continuing partners do not want the revised values in their balance sheet, they simply compensate the retiring partner: debit the continuing partners in their gaining ratio and credit the retiring partner with his share of the net gain (reverse for a loss). Alternatively a Memorandum Revaluation Account can be used.'],
         'analogy': 'If the flat you shared went up in value while you lived there, you are entitled to your share of the rise when you move out.',
         'work': 'Valuations on retirement are frequently disputed. A clear revaluation account with the valuer\'s report attached usually settles the argument.'},
        {'id': 'c4', 'title': 'Reserves and accumulated profits',
         'body': ['Undistributed profits and reserves shown in the balance sheet are credited to ALL partners in the OLD ratio (accumulated losses debited the same way).',
                  'Short-cut: if the continuing partners keep their old ratio between themselves, crediting only the retiring partner with his share gives the same result.',
                  'If the continuing partners change their mutual ratio and still want the reserve kept in the books, the retiring partner\'s share is debited to them in the gaining ratio and credited to him.'],
         'analogy': 'The common savings jar is split by everyone\'s share before one person leaves — or the stayers buy out the leaver\'s part of the jar.',
         'work': 'A reviewer checks whether the "only the retiring partner\'s share" short-cut was used where the continuing partners changed ratio — that would be a mistake.'},
        {'id': 'c5', 'title': 'Final amount due and how it is paid',
         'body': ['Retiring partner\'s claim = capital (and current account) balance + share of reserves + share of revaluation profit + share of goodwill + share of joint life policy + interest on capital and salary up to the date, if allowed − drawings, interest on drawings and share of losses.',
                  'Settlement options: paid in full at once (debit his capital, credit Bank); partly paid and the rest transferred to his Loan A/c; paid in instalments with interest on the outstanding balance; kept as a loan carrying interest or a share of profit; or an annuity for life or a fixed period.',
                  'Goodwill (AS 26 — only purchased goodwill may be shown): the retiring partner\'s share is debited to the gaining partners in the gaining ratio and credited to him. Any goodwill already in the books is first written off among all partners in the old ratio.'],
         'analogy': 'A final pay-slip: basic dues plus every allowance owed, minus every advance taken.',
         'work': 'Banks ask for the retirement deed and the settlement statement before releasing a retiring partner from guarantees — the figures must reconcile with the books.'},
        {'id': 'c6', 'title': 'Paying the retiring partner\'s loan in instalments',
         'body': ['When the balance is to be repaid in equal instalments with interest on the outstanding amount, divide the loan by the number of instalments to get the principal part. Each payment = principal instalment + interest on the opening balance of that period.',
                  'The loan account is credited with the opening balance (from the capital account) and with interest each year; it is debited with each payment. Interest is a charge against profit of the firm.'],
         'blocks': [p('Example: ₹60,000 repayable in 3 equal yearly instalments with 10% interest — Year 1 pay 20,000 + 6,000 = ₹26,000; Year 2 pay 20,000 + 4,000 = ₹24,000; Year 3 pay 20,000 + 2,000 = ₹22,000.')],
         'analogy': 'Like an education loan with equal principal repayments: the interest part shrinks each year because the balance shrinks.',
         'work': 'Accountants prepare this schedule at retirement so the firm can plan its cash flow; the interest also has to be reported correctly in the firm\'s income-tax computation.'},
        {'id': 'c7', 'title': 'Joint Life Policy (JLP)',
         'body': ['A JLP is taken by the firm on the lives of all partners jointly; the firm pays the premium, and the sum assured is received on the first death or on maturity. It provides cash to pay out a deceased or retiring partner without draining the business.',
                  'Three ways of treating the premium: (1) as an expense charged to P&L every year — the policy does not appear in the books; (2) as an asset — debited to Joint Life Policy A/c and written down each year to its surrender value; (3) as an asset with a Joint Life Policy Reserve built up from profits, both shown at surrender value.',
                  'On retirement the policy is not received; the retiring partner gets his share of its surrender value. If it is not in the books, it is brought in at surrender value and credited to all partners in the old ratio; if it is shown at a lower figure, only the excess is credited; under the reserve method the reserve is distributed in the old ratio.'],
         'analogy': 'A savings-cum-insurance pot the firm keeps for the day a partner leaves; when someone leaves early, he gets his slice of what the pot is worth today, not its maturity value.',
         'work': 'Auditors confirm the surrender value from the insurer\'s statement before accepting the retirement settlement.'},
        {'id': 'c8', 'title': 'Separate life policies',
         'body': ['Instead of one joint policy, the firm may take a separate policy on each partner\'s life and pay all premiums.',
                  'On retirement, the retiring partner is entitled to his profit-sharing proportion of the surrender value of ALL the policies — not just the policy on his own life.'],
         'analogy': 'Three umbrellas bought from the common purse: the one who leaves gets his share of the value of all three, not merely the one with his name on it.',
         'work': 'The settlement working must list every policy with its surrender value certificate; missing one changes the retiring partner\'s claim.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'New ratio and gaining ratio in four situations', 'difficulty': 'core', 'minutes': 10,
         'q': 'Asha, Bela and Chirag share profits 4:3:2. Bela retires. Find the new ratio of Asha and Chirag and their gaining ratio if: (a) nothing is agreed; (b) they agree to share equally; (c) Asha takes 1/9 and Chirag 2/9 out of Bela\'s share; (d) Bela\'s share is taken by Asha and Chirag in the ratio 2:1.',
         'solution': [gain_tbl], 'checks': c1},
        {'id': 'i2', 'title': 'Retirement with revaluation, reserve, goodwill and part payment', 'difficulty': 'hard', 'minutes': 28,
         'q': ('Kapoor, Lal and Mehra share profits 5:3:2. Balance Sheet at 31 March 2026: Trade payables ₹70,000; General Reserve ₹40,000; Capitals — Kapoor ₹2,00,000, Lal ₹1,50,000, Mehra ₹1,00,000 (total ₹5,60,000). '
               'Assets: Land and building ₹2,40,000; Plant ₹1,10,000; Inventory ₹80,000; Trade receivables ₹90,000; Bank ₹40,000. Lal retires on 1 April 2026; Kapoor and Mehra will share 3:2. '
               'Agreed: goodwill of the firm ₹1,20,000 (not to appear in the books); land and building up by ₹30,000; plant down by ₹10,000; inventory down by ₹2,400; provision for doubtful debts 4%; a payable of ₹2,000 is no longer payable. '
               'Lal is paid ₹32,800 by cheque and the balance is transferred to his loan account. Pass journal entries and prepare the Revaluation Account, Capital Accounts and the Balance Sheet.'),
         'solution': [wn('Gaining ratio', f'Kapoor 3/5 − 5/10 = 1/10; Mehra 2/5 − 2/10 = 2/10 → 1:2. Lal\'s goodwill 1,20,000 × 3/10 = ₹{inr(gw_L)} → Kapoor ₹{inr(gwK)}, Mehra ₹{inr(gwM)}.'),
                      journal(E2, 'Journal (1 April 2026)', 'j2'), rev2, cap2, bs2,
                      note('The reserve is shared among all three in 5:3:2 because Kapoor and Mehra change their mutual ratio (5:2 → 3:2); crediting only Lal with his share would be wrong here.')],
         'checks': c2},
        {'id': 'i3', 'title': "Repaying the retiring partner's loan in instalments", 'difficulty': 'moderate', 'minutes': 12,
         'q': "Continuing Illustration 2: Lal's loan of ₹1,70,000 is to be repaid in four equal annual instalments of principal, with interest at 10% p.a. on the outstanding balance. Prepare the repayment schedule and Lal's Loan Account for the first two years.",
         'solution': [sched3] + led3, 'checks': c3},
        {'id': 'i4', 'title': 'Joint life policy and separate life policies on retirement', 'difficulty': 'moderate', 'minutes': 12,
         'q': '(a) Nair, Oberoi and Pillai share 2:2:1. The firm holds a joint life policy whose surrender value on 1 October 2026 (Pillai\'s retirement) is ₹60,000. Show the entry under each of the three methods of treating the premium; under method 2 the policy stands in the books at ₹52,000. (b) If instead the firm held separate policies with surrender values Nair ₹40,000, Oberoi ₹35,000 and Pillai ₹25,000 (premiums charged to P&L), how much is Pillai entitled to? Pass the entry.',
         'solution': [jlp_tbl, wn('Separate policies', f'Total surrender value = 40,000 + 35,000 + 25,000 = ₹{inr(tot_sv)}. Pillai\'s share 1/5 = ₹{inr(pil)} (not merely the ₹25,000 of his own policy).'), journal(E4, 'Journal', 'j4')],
         'checks': c4},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Settlement statement for a retiring partner', 'role': 'Senior accountant of a trading firm',
         'situation': 'A partner holding a 30% share is retiring after 20 years. He has asked for a written statement of everything due to him, and his lawyer will review it.',
         'steps': ['Confirm from the deed or agreement: valuation of goodwill, interest on capital up to retirement, and how the balance will be paid.',
                   'Close the books (or prepare accounts) up to the retirement date so that profit to that date is known.',
                   'Prepare the revaluation account with valuer\'s and insurer\'s certificates.',
                   'List his capital, current account, reserves share, revaluation share, goodwill share and JLP share; deduct drawings.',
                   'Draw up the repayment schedule if the balance is a loan in instalments, and record the entries.'],
         'takeaway': 'Every number in a retirement settlement must be traceable to the deed, the books or a third-party certificate.',
         'think': 'The continuing partners say the general reserve should stay in the books. The retiring partner objects. What do you do?',
         'answer': 'The reserve can stay in the books, but the retiring partner must still be credited with his share — the continuing partners are debited in their gaining ratio.'},
        {'id': 'j2', 'title': 'Planning cash for an outgoing partner', 'role': 'Finance manager of a partnership firm',
         'situation': 'The firm has to pay ₹40 lakh to a retiring partner but has only ₹8 lakh spare cash.',
         'steps': ['Propose part payment now and the balance as a loan in equal instalments with interest, as allowed by the deed.',
                   'Prepare a schedule showing principal, interest and total payment each year; test it against projected cash flows.',
                   'Check the surrender value of the joint life policy — sometimes it is cheaper to borrow against it than to raise a bank loan.'],
         'takeaway': 'Retirement accounting decides how much is owed; the instalment schedule decides whether the firm can survive paying it.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'A, B and C share profits 3:2:1. B retires and nothing is agreed about the future ratio. The new ratio of A and C is:', 'options': ['3:1', '1:1', '2:1', '3:2'], 'answer': 0, 'explain': "If nothing is agreed about the future ratio, the continuing partners share in their old ratio between themselves. Strike out B's share: A and C continue as 3 : 1. The trap 1 : 1 assumes equal sharing, which applies only when there is no agreement at all on profit sharing — here the old 3 : 2 : 1 agreement still governs A and C. In practice: firms update the deed on a partner's retirement, but if they don't, the old relative ratio carries on.", 'topic': "Calculation of Gaining Ratio", 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'X, Y and Z share 2:2:1. Y retires; X and Z will share 3:2. The gaining ratio of X and Z is:', 'options': ['1:1', '3:2', '2:1', '1:2'], 'answer': 0, 'explain': "Gain = new share − old share. X: 3/5 − 2/5 = 1/5. Z: 2/5 − 1/5 = 1/5. Gaining ratio = 1 : 1. The trap 3 : 2 takes the new ratio as the gaining ratio; they are equal only when continuing partners gain in their old proportion. In practice: the gaining ratio decides how much each continuing partner pays the retiring partner for goodwill, so it is worked out separately.", 'topic': "Calculation of Gaining Ratio", 'concept': 'c2', 'difficulty': 'moderate'},
        {'id': 'm3', 'q': 'Profit on revaluation at the time of retirement is shared by:', 'options': ['All partners including the retiring partner, in the old ratio', 'Continuing partners in the new ratio', 'Continuing partners in the gaining ratio', 'The retiring partner alone'], 'answer': 0, 'explain': "The changes in asset and liability values occurred while the retiring partner was still an owner, so revaluation profit is shared by all partners, including him, in the old ratio. The trap 'continuing partners in the new ratio' would deny the retiring partner his share of gains made during his time. In practice: when a partner retires from a trading firm, the firm's property is usually revalued so that his settlement reflects current market values.", 'topic': "Revaluation of Assets and Liabilities on Retirement of a Partner", 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm4', 'q': "The retiring partner's share of goodwill is debited to:", 'options': ['Continuing partners in the gaining ratio', 'All partners in the old ratio', 'Goodwill Account', 'Continuing partners in the new ratio'], 'answer': 0, 'explain': "The continuing partners gain the retiring partner's share of future profits, so they compensate him for goodwill in their gaining ratio: debit continuing partners' capitals, credit the retiring partner's capital. The trap is debiting Goodwill Account — raising self-generated goodwill is not allowed under AS 26. In practice: a retiring partner's goodwill share is often the largest component of his final settlement in professional firms.", 'topic': "Final Payment to a Retiring Partner", 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm5', 'q': 'A loan of ₹90,000 is repayable in 3 equal annual instalments with 10% interest on the balance. The payment at the end of year 2 is:', 'options': ['₹36,000', '₹39,000', '₹33,000', '₹30,000'], 'answer': 0, 'check': '90000/3+60000*10/100', 'explain': "Principal instalment = 90,000 ÷ 3 = ₹30,000 a year. At the end of year 2, the balance outstanding during that year was 90,000 − 30,000 = ₹60,000, so interest = 60,000 × 10% = ₹6,000. Payment = 30,000 + 6,000 = ₹36,000. The trap ₹39,000 is year 1's payment (interest on the full ₹90,000). In practice: firms often settle a retiring partner in instalments with interest to protect their working capital.", 'topic': "Paying a Partner’s Loan in Instalment", 'concept': 'c6', 'difficulty': 'moderate'},
        {'id': 'm6', 'q': 'A, B and C share 5:3:2. Reserve ₹50,000. C retires and A and B continue in 5:3. Using the short-cut, the entry for the reserve is:', 'options': ["Reserve A/c Dr ₹10,000 To C's Capital A/c", "Reserve A/c Dr ₹50,000 To A and B in 5:3", "C's Capital A/c Dr ₹10,000 To Reserve A/c", 'No entry'], 'answer': 0, 'explain': "Because A and B continue in their old mutual ratio 5 : 3, the short-cut credits only the retiring partner's share of the reserve: 50,000 × 2/10 = ₹10,000. Entry: Reserve A/c Dr ₹10,000, To C's Capital A/c. The trap is distributing the entire reserve, which gives the same result but is not the short-cut asked for; debiting C is simply wrong. In practice: accountants use this short-cut to keep the reserve in the books while settling only the leaver.", 'topic': "Reserve", 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm7', 'q': 'A firm has separate life policies on its three partners (equal partners) with surrender values ₹18,000, ₹24,000 and ₹30,000. The partner whose policy has a surrender value of ₹18,000 retires. His share is:', 'options': ['₹24,000', '₹18,000', '₹6,000', '₹72,000'], 'answer': 0, 'check': '(18000+24000+30000)/3', 'explain': "Separate life policies on partners are assets of the firm, so the retiring partner is entitled to his profit-sharing share of the total surrender value of all policies, not just the value of his own policy. Total = 18,000 + 24,000 + 30,000 = ₹72,000; his 1/3 = ₹24,000. The trap ₹18,000 gives him only his own policy's value. In practice: firms often buy separate partner policies to fund settlements on death or retirement.", 'topic': "Separate Life Policy", 'concept': 'c8', 'difficulty': 'moderate'},
        {'id': 'm8', 'q': 'Under the method where JLP premium is charged to Profit and Loss Account every year, the joint life policy:', 'options': ['Does not appear in the balance sheet', 'Appears at the sum assured', 'Appears at the total premium paid', 'Appears with an equal reserve'], 'answer': 0, 'explain': "If JLP premiums are charged to Profit and Loss every year, they are fully written off as expenses, so the policy does not appear as an asset in the balance sheet. On retirement, its surrender value is brought into the books. The trap 'appears at the total premium paid' describes the method where premiums are capitalised. In practice: many small firms expense the premium, so the policy's value appears only when a partner leaves.", 'topic': "Joint Life Policy", 'concept': 'c7', 'difficulty': 'core'},
        {'id': 'm9', 'q': 'JLP is shown in the books at ₹40,000; its surrender value on a partner\'s retirement is ₹46,000. The amount credited to the Revaluation Account is:', 'options': ['₹6,000', '₹46,000', '₹40,000', '₹86,000'], 'answer': 0, 'check': '46000-40000', 'explain': "The JLP is already carried at ₹40,000. On retirement it is revalued to its surrender value of ₹46,000, so only the increase of 46,000 − 40,000 = ₹6,000 is a gain credited to the Revaluation Account. The trap ₹46,000 credits the whole surrender value, double-counting the ₹40,000 already in the books. In practice: insurers issue a surrender-value certificate that the firm's accountant uses for this adjustment.", 'topic': "Joint Life Policy", 'concept': 'c7', 'difficulty': 'moderate'},
        {'id': 'm10', 'q': 'P, Q and R share 4:3:2. Q retires; P takes 2/9 and R takes 1/9 of the firm\'s profit from Q\'s share. The new ratio of P and R is:', 'options': ['2:1', '4:3', '5:4', '1:1'], 'answer': 0, 'explain': "New share = old share + share taken from Q. P: 4/9 + 2/9 = 6/9. R: 2/9 + 1/9 = 3/9. New ratio = 6 : 3 = 2 : 1. The trap 4 : 3 or 5 : 4 comes from not adding the acquired fractions properly to the old shares. In practice: the deed of retirement records exactly how the retiring partner's share is divided, and the accountant converts it into new ratios.", 'topic': "Calculation of Gaining Ratio", 'concept': 'c2', 'difficulty': 'moderate'},
        {'id': 'm11', 'q': "Which of the following is NOT credited to a retiring partner's capital account?", 'options': ['His drawings during the year', 'His share of revaluation profit', 'His share of goodwill', 'His share of general reserve'], 'answer': 0, 'explain': "A retiring partner's capital is credited with everything owed to him: his share of revaluation profit, goodwill, reserves and current-year profit. His drawings during the year reduce what is due, so they are debited, not credited. The trap is goodwill — it is credited because the continuing partners compensate him for it. In practice: the final settlement statement prepared by the firm's CA lists credits and debits so the leaver can verify the amount.", 'topic': "Final Payment to a Retiring Partner", 'concept': 'c5', 'difficulty': 'core'},
        {'id': 'm12', 'q': 'If the continuing partners do not want revised values in their balance sheet, a revaluation gain of ₹30,000 on A\'s retirement from the firm of A, B and C (equal partners; B and C continue equally) is recorded as:', 'options': ["B's Capital Dr ₹5,000, C's Capital Dr ₹5,000 To A's Capital ₹10,000", "Revaluation Dr ₹30,000 To A, B, C ₹10,000 each", "A's Capital Dr ₹10,000 To B and C", 'No entry is required'], 'answer': 0, 'explain': "Without changing book values, A's share of the revaluation gain (30,000 × 1/3 = ₹10,000) is paid to him by the gainers. B and C each go from 1/3 to 1/2, gaining 1/6 each, so the gaining ratio is 1 : 1. Entry: B's Capital Dr ₹5,000, C's Capital Dr ₹5,000, To A's Capital ₹10,000. The trap is crediting everyone through a Revaluation Account, which changes book values. In practice: this keeps assets at historical cost while settling the leaver fairly.", 'topic': "Revaluation of Assets and Liabilities on Retirement of a Partner", 'concept': 'c3', 'difficulty': 'hard'},
    ]

    questions = [
        {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'journal',
         'q': 'Pari, Qadir and Rhea share profits 3:2:1. Qadir retires; Pari and Rhea will share future profits 3:2. The balance sheet shows a General Reserve of ₹36,000. The goodwill of the firm is valued at ₹90,000 and is not to appear in the books. (a) Calculate the gaining ratio. (b) Pass the entry for the reserve (i) if it is to be distributed, and (ii) if the continuing partners want it to remain in the books. (c) Pass the entry for goodwill.',
         'model': [wn('Gaining ratio', 'Pari 3/5 − 3/6 = 18/30 − 15/30 = 3/30; Rhea 2/5 − 1/6 = 12/30 − 5/30 = 7/30 → 3:7.'),
                   journal(Q1, 'Journal', 'jq1'),
                   note('Entries (i) and (ii) are alternatives. The short-cut of crediting only Qadir would be wrong if Pari and Rhea were not debited, because their mutual ratio changes from 3:1 to 3:2.')],
         'scheme': [{'id': 's1', 'pt': 'Gaining ratio 3:7 with working', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's2', 'pt': 'Reserve distributed 18,000 : 12,000 : 6,000 in the old ratio', 'm': 1.5, 'skill': 'posting'},
                    {'id': 's3', 'pt': "Alternative: Pari ₹3,600 and Rhea ₹8,400 debited, Qadir credited ₹12,000", 'm': 1.5, 'skill': 'concept'},
                    {'id': 's4', 'pt': "Goodwill: Qadir credited ₹30,000; Pari ₹9,000 and Rhea ₹21,000 debited", 'm': 1.5, 'skill': 'computation'}],
         'checks': qc1,
         'remarks': ['Most candidates get the gaining ratio right but then debit goodwill in the new ratio 3:2 — that loses the last step.', 'Part (b)(ii) is answered poorly; many simply write "no entry".'],
         'mistakes': ['Debiting goodwill in the old ratio.', 'Raising goodwill in the books contrary to the question.', 'Using 3/6 and 1/6 as the new shares.'],
         'tips': ['Show the gaining ratio as a working note first — it is needed twice.', 'Label alternative entries clearly as alternatives.']},
        {'id': 'q2', 'marks': 10, 'minutes': minutes(10), 'difficulty': 'hard', 'pad': 'table',
         'q': ('Gupta, Hegde and Iyer share profits 2:2:1. Balance Sheet at 30 June 2026: Creditors ₹54,000; General Reserve ₹30,000; Capitals — Gupta ₹1,60,000, Hegde ₹1,20,000, Iyer ₹80,000 (total ₹4,44,000). '
               'Assets: Premises ₹2,00,000; Furniture ₹40,000; Inventory ₹70,000; Debtors ₹1,00,000; Bank ₹34,000. Iyer retires on that date; Gupta and Hegde will share equally. '
               'Premises are appreciated by 20%; furniture is revalued at ₹34,000; a 5% provision is made on debtors; creditors include ₹4,000 no longer payable. Goodwill of the firm is valued at ₹75,000 and is not to be shown in the books. '
               'Iyer is paid ₹27,600 by cheque and the rest is transferred to his loan account. Draw up the Revaluation Account, the partners\' capital accounts and the firm\'s Balance Sheet after the retirement.'),
         'model': [wn('Gaining ratio', 'Gupta 1/2 − 2/5 = 1/10; Hegde 1/2 − 2/5 = 1/10 → 1:1. Iyer\'s goodwill = 75,000 × 1/5 = ₹15,000 → ₹7,500 each.'), q2revT, q2cap, q2bs],
         'scheme': [{'id': 's1', 'pt': 'Revaluation profit ₹33,000 with each item on the correct side', 'm': 2, 'skill': 'computation'},
                    {'id': 's2', 'pt': 'Revaluation profit and reserve shared 2:2:1 among all three', 'm': 1.5, 'skill': 'posting'},
                    {'id': 's3', 'pt': 'Goodwill ₹15,000 credited to Iyer, debited ₹7,500 each to Gupta and Hegde', 'm': 1.5, 'skill': 'concept'},
                    {'id': 's4', 'pt': "Iyer's claim ₹1,07,600 settled: ₹27,600 bank, ₹80,000 loan", 'm': 1.5, 'skill': 'computation'},
                    {'id': 's5', 'pt': 'Capital accounts balanced: Gupta ₹1,77,700, Hegde ₹1,37,700', 'm': 1.5, 'skill': 'balancing'},
                    {'id': 's6', 'pt': 'Balance sheet at revised values with loan shown, total ₹4,45,400', 'm': 2, 'skill': 'presentation'}],
         'checks': qc2,
         'remarks': ['The creditor written back is often put on the wrong side — a fall in a liability is a gain (credit Revaluation).', 'Candidates who forget to show Iyer\'s loan in the balance sheet lose the presentation marks.'],
         'mistakes': ['Sharing revaluation profit only between Gupta and Hegde.', 'Showing goodwill as an asset.', 'Leaving Iyer\'s capital account with a balance instead of closing it.'],
         'tips': ['Close the retiring partner\'s column fully — to Bank and to Loan.', 'Total the balance sheet before writing the final figures.']},
        {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'ledger',
         'q': "Ravi retired from a firm and the amount due to him, ₹1,20,000, was transferred to his loan account at the start of Year 1. It is to be repaid in three equal annual instalments of principal together with interest at 12% p.a. on the outstanding balance. Prepare Ravi's Loan Account for the three years.",
         'model': [table(['Year', 'Opening balance (₹)', 'Interest @12% (₹)', 'Principal instalment (₹)', 'Total paid (₹)', 'Closing balance (₹)'], rows_q3, num=[2, 3, 4], total=True, title='Repayment schedule')] + led_q3,
         'scheme': [{'id': 's1', 'pt': 'Principal instalment ₹40,000 and interest computed on the opening balance each year', 'm': 1.5, 'skill': 'computation'},
                    {'id': 's2', 'pt': 'Year 1: interest ₹14,400, payment ₹54,400, balance ₹80,000', 'm': 1, 'skill': 'posting'},
                    {'id': 's3', 'pt': 'Year 2: interest ₹9,600, payment ₹49,600, balance ₹40,000', 'm': 1, 'skill': 'posting'},
                    {'id': 's4', 'pt': 'Year 3: interest ₹4,800, payment ₹44,800; account closed', 'm': 1, 'skill': 'balancing'},
                    {'id': 's5', 'pt': 'Correct sides: loan and interest credited, payments debited', 'm': 0.5, 'skill': 'presentation'}],
         'checks': qc3,
         'remarks': ['Some candidates charge interest on the original ₹1,20,000 every year.', 'Others treat the instalment as including interest (equal total payments) — read the question carefully.'],
         'mistakes': ['Debiting interest to the loan account.', 'Not bringing down the balance at the start of each year.'],
         'tips': ['Prepare the small schedule first; the ledger then writes itself.']},
        {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'Explain the three methods of accounting for the premium on a joint life policy and the treatment on the retirement of a partner.',
         'model': [ul(['Premium as expense: premium debited to Joint Life Policy Premium A/c and closed to P&L every year; the policy is not in the books. On retirement the surrender value is brought in and credited to all partners in the old ratio.',
                       'Premium as asset at surrender value: premium debited to Joint Life Policy A/c; at year-end the excess over surrender value is written off to P&L. On retirement only any increase in surrender value over book value is a gain.',
                       'Joint Life Policy Reserve: as in the second method, plus an amount equal to the premium is set aside from profits to a JLP Reserve, which is brought down to the surrender value; both appear at surrender value. On retirement the reserve is distributed in the old ratio.',
                       'In all methods the retiring partner receives his share of the surrender value; the policy continues for the others.'])],
         'scheme': [{'id': 's1', 'pt': 'Expense method and its retirement treatment', 'm': 1, 'skill': 'concept'},
                    {'id': 's2', 'pt': 'Asset (surrender value) method and its treatment', 'm': 1, 'skill': 'concept'},
                    {'id': 's3', 'pt': 'Reserve method and its treatment', 'm': 1, 'skill': 'concept'},
                    {'id': 's4', 'pt': 'Retiring partner gets share of surrender value, not policy amount', 'm': 1, 'skill': 'application'}],
         'remarks': ['Answers often confuse surrender value with sum assured — on retirement the policy has not matured.'],
         'mistakes': ['Saying the retiring partner gets his share of the policy amount.', 'Omitting the treatment on retirement.'],
         'tips': ['Number the three methods and give the entry in brief for each.']},
    ]

    viva = [
        V('v1', 'What is gaining ratio and how is it calculated on the retirement of a partner?',
          'Gaining ratio is the ratio in which the continuing partners acquire the retiring partner\'s share. Each partner\'s gain is his new share minus his old share. If no new ratio is agreed, the continuing partners keep their old ratio and the gaining ratio is the same as their old ratio. It is used to debit them with the retiring partner\'s share of goodwill.',
          [P('p1', 'Ratio in which continuing partners acquire the retiring partner\'s share', 3, 'continuing partner|remaining partner|existing partner', 'acquire|take over|takes over|get|gain|share of the retiring|retiring partner', min=2),
           P('p2', 'Gain = new share − old share', 4, ALT('{n} minus {o}', '{n} less {o}', 'difference between {n} and {o}', 'subtract {o} from {n}', 'deduct {o} from {n}', '{o} deducted from {n}', '{o} subtracted from {n}',
                                                         n=('new share', 'new ratio', 'new profit share'), o=('old share', 'old ratio', 'old profit share'))),
           P('p3', 'Used for the retiring partner\'s goodwill (or: equals old ratio if nothing agreed)', 3, 'goodwill|same as old|same as their old|equal to old|old ratio', min=1)], 'c2'),
        V('v2', 'In what ratio is profit on revaluation shared when a partner retires, and why?',
          'Profit or loss on revaluation is shared by all the partners, including the retiring partner, in the old profit sharing ratio, because the values changed while the retiring partner was still a partner.',
          [P('p1', 'All partners including the retiring partner', 4, 'including the retiring|including retiring|retiring partner also|all partners|all the partners|all three|all existing'),
           P('p2', 'Old ratio', 4, 'old ratio|old profit sharing|existing ratio|original ratio|previous ratio'),
           P('p3', 'Because the change arose while he was a partner', 2, 'still a partner|was a partner|while he was|before retirement|before he retired|during his|when he was|his time|arose before|earned before', min=1)], 'c3'),
        V('v3', 'What items are added to or deducted from a retiring partner\'s capital to find the amount payable to him?',
          'To his capital we add his share of reserves and undistributed profits, his share of revaluation profit, his share of goodwill, his share of the joint life policy, and interest on capital or salary if allowed up to the date of retirement. We deduct his drawings, interest on drawings and his share of any losses or revaluation loss. The balance is paid to him or transferred to his loan account.',
          [P('p1', 'Add share of reserves', 2, 'share reserve|add reserve|plus reserve|reserve share|credit reserve|share undistributed|undistributed profit|accumulated profit'),
           P('p2', 'Add share of revaluation profit', 2, 'revaluation profit|revaluation gain|share revaluation|add revaluation|plus revaluation|revaluation share|profit on revaluation|gain on revaluation'),
           P('p3', 'Add share of goodwill', 2, 'goodwill'),
           P('p4', 'Deduct drawings (and losses)', 2, 'drawing', 'deduct|less|minus|subtract|debit|reduce'),
           P('p5', 'Balance paid in cash or transferred to loan', 2, 'loan|paid|payment|bank|cash|instalment|settle', min=1)], 'c5'),
        V('v4', 'How is a general reserve treated on retirement if the continuing partners do not change their mutual ratio?',
          'Normally the reserve is distributed among all partners in the old ratio. But if the continuing partners keep their old ratio between themselves, it is enough to credit only the retiring partner\'s capital with his share of the reserve, because the gaining ratio is the same as their old ratio and the result is identical.',
          [P('p1', 'Normally distributed among all partners in the old ratio', 4, 'all partner|all the partner|among all|every partner|everyone', 'old ratio|old profit sharing|existing ratio', min=2),
           P('p2', 'Short-cut: credit only the retiring partner with his share', 4, 'only the retiring|only retiring|retiring partner only|just the retiring|only his share|only the share of the retiring|retiring partner share only', min=1),
           P('p3', 'Because gaining ratio equals their old ratio — same result', 2, 'same result|same effect|identical|same as their old|equal to their old|same as old|same ratio', min=1)], 'c4'),
        V('v5', 'What are the three methods of treating joint life policy premium?',
          'First, the premium can be treated as an expense and charged to profit and loss account every year, so the policy does not appear in the books. Second, it can be treated as an asset and the policy is shown at its surrender value, the excess premium being written off. Third, a joint life policy reserve is created out of profits, and both the policy and the reserve appear at the surrender value.',
          [P('p1', 'Premium as expense charged to P&L', 3, 'expense|profit and loss|profit loss|written off every year|charged'),
           P('p2', 'Premium as asset, shown at surrender value', 4, 'asset', 'surrender value|surrender', min=2),
           P('p3', 'Joint life policy reserve method', 3, 'reserve')], 'c7'),
        V('v6', 'If a firm has separate life policies on each partner, what is a retiring partner entitled to?',
          'He is entitled to his profit sharing proportion of the surrender value of all the policies, not just the policy on his own life.',
          [P('p1', 'Share of the surrender value', 4, 'surrender value|surrender'),
           P('p2', 'Of ALL the policies, not only his own', 4, 'all the polic|all polic|every polic|all partners polic|policies of all|each polic|total of all|not just his|not only his|not merely his|not his own only', min=1),
           P('p3', 'In his profit sharing ratio', 2, 'profit sharing|his share|his ratio|proportion|ratio')], 'c8'),
    ]

    kcase = [{'id': 'k1', 'title': "Uma retires from Tanvi, Uma & Varun", 'difficulty': 'hard',
              'case': ('Tanvi, Uma and Varun share profits 5:3:2. Uma retires; Tanvi and Varun will share 3:2. Uma\'s capital is ₹1,50,000 and the General Reserve is ₹20,000. The goodwill of the firm is valued at ₹1,00,000 and will not appear in the books. '
                       'The firm has a joint life policy whose premiums have always been charged to Profit and Loss Account; its surrender value is ₹40,000. There is no revaluation.'),
              'mcqs': [
                  M('k1a', 'What is the gaining ratio of Tanvi and Varun?', ['1:2', '3:2', '5:2', '1:1'], 0, "Gain = new share − old share. Tanvi: 3/5 − 5/10 = 6/10 − 5/10 = 1/10. Varun: 2/5 − 2/10 = 4/10 − 2/10 = 2/10. Gaining ratio = 1 : 2. The trap 3 : 2 is the new ratio, not the gain; Varun actually gains twice as much as Tanvi. In practice: Uma's goodwill will be paid by Tanvi and Varun in this 1 : 2 gaining ratio.", 'moderate') | {'topic': "Calculation of Gaining Ratio"},
                  M('k1b', "How much is debited to Varun's capital for Uma's goodwill?", [R(k_vg), R(10000), R(12000), R(30000)], 0, "Uma's share of goodwill = 1,00,000 × 3/10 = ₹30,000. Tanvi and Varun pay it in their gaining ratio 1 : 2, so Varun is debited 30,000 × 2/3 = ₹20,000 and Tanvi ₹10,000. The trap ₹12,000 uses the new ratio 3 : 2 (Varun 2/5), and ₹10,000 is Tanvi's part. In practice: goodwill compensation is passed through capital accounts so no goodwill asset appears in the books.", 'hard', '100000*3/10*2/3') | {'topic': "Final Payment to a Retiring Partner"},
                  M('k1c', "What is Uma's share of the joint life policy?", [R(k_j), R(30000), R(40000), R(8000)], 0, "Since premiums were charged to profit and loss, the JLP is not in the books; its surrender value of ₹40,000 is brought in on retirement. Uma's share in the old ratio = 40,000 × 3/10 = ₹12,000. The trap ₹40,000 gives her the whole surrender value — the policy is not paid out on retirement, only on maturity or death. In practice: insurers provide a surrender-value certificate, and the firm records it before settling the retiring partner.", 'moderate', '40000*3/10') | {'topic': "Joint Life Policy"},
                  M('k1d', 'What is the total amount due to Uma?', [R(k_due), R(186000), R(192000), R(168000)], 0, "Amount due = capital 1,50,000 + reserve share 20,000 × 3/10 = 6,000 + goodwill share 30,000 + JLP share 12,000 = ₹1,98,000. The trap ₹1,86,000 forgets the JLP; ₹1,92,000 forgets the reserve; ₹1,68,000 forgets goodwill. In practice: a retiring partner's settlement statement lists each component, and the firm may pay part immediately and the rest in instalments with interest.", 'hard', '150000+20000*3/10+30000+12000') | {'topic': "Final Payment to a Retiring Partner"},
              ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch10', 'n': 4,
        'title': 'Retirement of a Partner',
        'outcomes': [
            'Work out the new ratio and the gaining ratio of the continuing partners in every standard situation.',
            'Record revaluation, reserves and goodwill on retirement and close the retiring partner\'s capital account.',
            'Settle the retiring partner\'s claim in cash, as a loan, or in instalments with interest, and prepare the loan account.',
            'Account for joint life policies under all three methods and for separate life policies on retirement.',
        ],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 75}, 'prereq': ['fnd-p1-ch10-u02', 'fnd-p1-ch10-u03'],
                 'exam_tip': 'In a retirement question the retiring partner\'s capital column must end at nil — paid in cash or transferred to loan. If it does not close, something has been missed.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Gain = new share − old share; nothing agreed → continuing partners keep their old ratio (gaining ratio = old ratio).',
                        'Revaluation profit/loss → all partners incl. retiring partner, old ratio.',
                        'Reserves → all partners, old ratio (short-cut: only the retiring partner, if continuing partners keep their mutual ratio).',
                        'Goodwill → retiring partner credited; gaining partners debited in gaining ratio.',
                        'Claim settled in cash, as a loan, in instalments with interest or as an annuity.',
                        'JLP: expense / asset at surrender value / reserve method; retiring partner gets share of surrender value. Separate policies: share of surrender value of all policies.'],
            'remember': ['Instalment payment = principal instalment + interest on opening balance.', 'Only the excess of surrender value over book value is a revaluation gain.', 'The retiring partner\'s capital account must close at nil.'],
            'traps': ["Don't use the new ratio for goodwill — use the gaining ratio.", "Don't use the short-cut for reserves when the continuing partners change their mutual ratio.", "Don't give the retiring partner the sum assured of a JLP — he gets the surrender value share."],
        },
        'quickref': [
            {'k': 'Gain', 'v': 'New share − Old share'},
            {'k': 'New share (gain given)', 'v': 'Old share + Gain'},
            {'k': 'Goodwill on retirement', 'v': "Gaining Partners' Capital A/cs Dr. To Retiring Partner's Capital A/c (gaining ratio)"},
            {'k': 'Revaluation / reserves', 'v': 'All partners incl. retiring, old ratio'},
            {'k': 'Settlement', 'v': "Debit the retiring partner's capital; credit Bank and/or his Loan A/c"},
            {'k': 'Instalment', 'v': 'Loan ÷ n + interest on opening balance'},
            {'k': 'Separate policies', 'v': 'Retiring partner\'s ratio × total surrender value of all policies'},
        ],
        'viva': viva, 'cases': kcase,
    }
