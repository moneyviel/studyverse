"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 14 — Internal Reconstruction.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch14-u01'
T1 = 'Meaning and need for internal reconstruction'
T2 = 'Alteration of share capital (s. 61)'
T3 = 'Reduction of share capital (s. 66) and capital reduction account'
T4 = 'Sacrifices by creditors and debenture holders'
T5 = 'Balance sheet after reconstruction'


def build():
    ck = Checks()
    sh = ck.add('100000*(10-3)', 'Reduction in equity capital (₹)')
    deb = ck.add('500000*10/100', 'Sacrifice by debenture holders (₹)')
    tot = ck.add('700000+50000', 'Total credited to capital reduction account (₹)')
    wo = ck.add('450000+100000+20000+130000', 'Losses and assets written off (₹)')
    cr = ck.add('750000-700000', 'Balance to capital reserve (₹)')
    i1 = {'id': 'i1', 'title': 'A reduction scheme', 'difficulty': 'core', 'minutes': 9,
          'q': 'Shanti Ltd. has 1,00,000 equity shares of ₹10 fully paid and ₹5,00,000 debentures. Under an approved scheme: equity shares are reduced to ₹3 each; debenture holders give up 10% of their claim; the debit balance of profit and loss ₹4,50,000, goodwill ₹1,00,000 and preliminary expenses ₹20,000 are written off; and plant is written down by ₹1,30,000. Compute the capital reduction account balance.',
          'solution': [table(['Capital reduction account', 'Working', '₹'], [
              ['Credit: equity capital reduced', '1,00,000 × ₹7', inr(sh)],
              ['Credit: debenture holders\' sacrifice', '10% × 5,00,000', inr(deb)],
              ['Total credits', '', inr(tot)],
              ['Debit: P&L, goodwill, preliminary expenses, plant', '4,50,000 + 1,00,000 + 20,000 + 1,30,000', inr(wo)],
              ['Balance transferred to capital reserve', '', inr(cr)]], title='Capital reduction account')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Consolidation and sub-division', 'difficulty': 'core', 'minutes': 5,
          'q': 'Tapas Ltd. has 50,000 equity shares of ₹10 each, fully paid. Show the effect of (a) consolidating them into shares of ₹50 each; (b) instead sub-dividing them into shares of ₹2 each.',
          'solution': [table(['Change', 'Working', 'Result'], [
              ['(a) Consolidation', '₹5,00,000 ÷ ₹50', '10,000 shares of ₹50'],
              ['(b) Sub-division', '₹5,00,000 ÷ ₹2', '2,50,000 shares of ₹2']], title='Alteration of share capital'),
              note('Total share capital stays ₹5,00,000; only the number and face value change. No capital reduction account is needed.')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Internal reconstruction reorganises a company\'s capital structure without liquidating it or forming a new company. It is used when a company has accumulated losses, overvalued assets and fictitious assets that make its balance sheet unrealistic and block dividends.',
            'It may involve alteration of share capital, reduction of share capital, compromise with creditors and debenture holders, and a revaluation of assets and liabilities.',
            'In contrast, external reconstruction involves a new company taking over the old one\'s business.'],
          'Internal reconstruction cleans up the balance sheet from within.',
          'A company with ₹40 lakh of accumulated losses reduces capital to wipe them out and restart dividends.'),
        C('c2', T2, [
            'Section 61: if its articles allow, a company may by ordinary resolution increase authorised capital, consolidate shares into larger denominations, sub-divide shares into smaller ones, convert fully paid shares into stock (and back), and cancel unissued shares.',
            'These changes do not reduce paid-up capital, so no capital reduction account or Tribunal approval is needed (except consolidation altering voting percentages).',
            'Entries simply transfer balances between old and new share capital accounts.'],
          'Alteration changes the labels on capital, not its amount.',
          'Splitting ₹10 shares into ₹1 shares increases the number tenfold, with the same total capital.'),
        C('c3', T3, [
            'Section 66: a company may reduce share capital by special resolution confirmed by the Tribunal — by extinguishing or reducing liability on unpaid capital, cancelling paid-up capital that is lost or not represented by assets, or paying off capital in excess of needs.',
            'The reduction is credited to a capital reduction (reconstruction) account. This account is debited with accumulated losses, fictitious assets (preliminary expenses, discounts on issue), goodwill and reductions in overvalued assets, and credited with any increases in asset values.',
            'Any credit balance left is transferred to capital reserve; the account should not be left with a debit balance — the reduction must be enough.',
            'Creditors are given notice and may object; the Tribunal confirms only if creditors are protected.'],
          'Capital reduction absorbs losses that capital can no longer support.',
          'Reducing ₹10 shares to ₹6 creates ₹4 per share to write off losses.'),
        C('c4', T4, [
            'Debenture holders and creditors may also make sacrifices — giving up part of principal or interest arrears, accepting shares instead of cash, or reducing interest rates. The amount given up is credited to capital reduction account.',
            'Preference shareholders may give up dividend arrears (which are not liabilities) or have their shares reduced or converted. Arrears of preference dividend sacrificed need no entry, but are disclosed.',
            'Directors or shareholders may give loans or waive claims; contingent liabilities that crystallise are provided.'],
          'Everyone with a claim may share the pain of reconstruction.',
          'Creditors accepting 80 paise per rupee give ₹20 per ₹100 to the capital reduction account.'),
        C('c5', T5, [
            'After reconstruction, the balance sheet shows reduced share capital (often with the words "and reduced" for a period, if required), assets at revised values, no accumulated losses or fictitious assets, and any capital reserve arising.',
            'Notes give details of the scheme, the reduction and changes in liabilities.'],
          'The new balance sheet should reflect real values and a clean slate.',
          'Equity share capital shown as "1,00,000 shares of ₹3 each".'),
    ]

    jobs = [{'id': 'j1', 'title': 'Reconstruction journal', 'role': 'Accounts executive',
             'situation': 'The Tribunal has approved a reduction scheme; you must pass entries and redraft the balance sheet.',
             'steps': ['Credit capital reduction with shares reduced and sacrifices.', 'Debit losses, fictitious assets and asset write-downs.', 'Transfer any balance to capital reserve.', 'Prepare the revised balance sheet.'],
             'takeaway': 'The capital reduction account must close with no debit balance.'}]

    mcqs = [
        Q('m1', 'Sub-division of ₹10 shares into ₹2 shares under section 61 requires:', ['An ordinary resolution if the articles permit', 'Tribunal approval', 'A special resolution and Tribunal', 'Creditors\' consent'], 0,
          'Alteration under section 61 — consolidation, sub-division, conversion into stock, increase of authorised capital — needs only an ordinary resolution if the articles allow. Paid-up capital is unchanged. In practice: file notice with the Registrar.', 'c2', T2),
        Q('m2', 'Reduction of share capital under section 66 requires:', ['A special resolution confirmed by the Tribunal', 'An ordinary resolution', 'Board resolution only', 'SEBI approval only'], 0,
          'Capital reduction needs a special resolution and confirmation by the Tribunal after notice to creditors and regulators. Creditors may object. In practice: prepare a detailed scheme.', 'c3', T3),
        Q('m3', '50,000 shares of ₹10 fully paid are reduced to ₹4 each. Amount credited to capital reduction account:', ['₹3,00,000', '₹2,00,000', '₹5,00,000', '₹50,000'], 0,
          'Each share is reduced by ₹6; 50,000 × ₹6 = ₹3,00,000 is credited to capital reduction account and used to write off losses. In practice: debit equity share capital.', 'c3', T3, 'moderate', check=300000),
        Q('m4', 'Which is debited to capital reduction account?', ['Debit balance of profit and loss', 'Increase in value of land', 'Share capital reduced', 'Debenture holders\' sacrifice'], 0,
          'Accumulated losses, fictitious assets, goodwill and write-downs of assets are debited; reductions of capital, sacrifices and asset appreciation are credited. In practice: list both sides first.', 'c3', T3),
        Q('m5', 'A credit balance remaining in capital reduction account is transferred to:', ['Capital reserve', 'General reserve', 'Profit and loss', 'Securities premium'], 0,
          'Any surplus after writing off losses and adjusting assets is a capital profit and is transferred to capital reserve. A debit balance should not remain. In practice: design the scheme to avoid it.', 'c3', T3),
        Q('m6', 'Debenture holders agree to give up 20% of ₹10,00,000 debentures. Capital reduction account is credited with:', ['₹2,00,000', '₹8,00,000', '₹10,00,000', '₹20,000'], 0,
          'The amount given up, 20% × ₹10,00,000 = ₹2,00,000, reduces the debentures and is credited to capital reduction account. In practice: debit debentures.', 'c4', T4, 'moderate', check=200000),
        Q('m7', 'Arrears of preference dividend given up in a reconstruction:', ['Need no journal entry, as they were not a liability', 'Are credited to capital reduction', 'Are debited to profit and loss', 'Are credited to capital reserve'], 0,
          'Undeclared preference dividend arrears are not liabilities, so waiving them requires no accounting entry, though the fact is disclosed. In practice: note it in the scheme.', 'c4', T4),
        Q('m8', 'Consolidation of shares changes:', ['The number and face value of shares, not total capital', 'Total paid-up capital', 'Reserves', 'Liabilities'], 0,
          'Consolidation combines shares into larger denominations, so fewer shares carry higher face value; total paid-up capital is unchanged. In practice: transfer between capital accounts.', 'c2', T2),
        Q('m9', 'Internal reconstruction differs from external reconstruction because it:', ['Does not involve liquidating the company or forming a new one', 'Always involves a new company', 'Requires amalgamation', 'Is only for private companies'], 0,
          'Internal reconstruction reorganises capital within the same company; external reconstruction sees a new company take over the old company\'s business. In practice: no realisation account is needed internally.', 'c1', T1),
        Q('m10', 'Increase in the value of land agreed under the scheme is:', ['Credited to capital reduction account', 'Credited to profit and loss', 'Debited to capital reduction', 'Ignored'], 0,
          'Asset appreciation agreed in the scheme adds to the amount available for writing off losses, so it is credited to capital reduction account. In practice: debit land.', 'c3', T3),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Credits to capital reduction', 2, 'computation', 'reduced', nums=[sh, deb, tot]),
           S('s2', 'Debits written off', 2, 'computation', 'written off|plant', nums=[wo]),
           S('s3', 'Capital reserve', 2, 'computation', 'capital reserve', nums=[cr])],
          ['Prepare the account in T-form.'], ['Leaving a debit balance.'], ['Account or table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Consolidation', 1.5, 'concept', '10,000'),
           S('s2', 'Sub-division', 1.5, 'concept', '2,50,000')],
          ['Capital stays the same.'], ['Using capital reduction account.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is internal reconstruction?', 'A reorganisation of a company\'s capital — through alteration or reduction and compromises with creditors — carried out without liquidating the company.',
          [P('p1', 'Reorganise capital', 5, 'capital'), P('p2', 'Same company continues', 5, 'liquidat|without')], 'c1'),
        V('v2', 'What does the capital reduction account do?', 'It receives the capital reduced and sacrifices by claimholders, and is used to write off losses, fictitious assets and overvaluation, any surplus going to capital reserve.',
          [P('p1', 'Write off losses', 6, 'loss'), P('p2', 'Surplus to capital reserve', 4, 'capital reserve')], 'c3'),
        V('v3', 'How does section 61 differ from section 66?', 'Section 61 alters the form of capital without reducing it, by ordinary resolution; section 66 reduces capital by special resolution confirmed by the Tribunal.',
          [P('p1', 'Alteration', 5, 'alter'), P('p2', 'Reduction with Tribunal', 5, 'tribunal')], 'c2'),
        V('v4', 'Who may make sacrifices in a reconstruction?', 'Equity and preference shareholders, debenture holders and creditors, by giving up capital, principal, interest or arrears.',
          [P('p1', 'Shareholders', 5, 'shareholder'), P('p2', 'Lenders and creditors', 5, 'debenture|creditor')], 'c4'),
        V('v5', 'Is an entry needed when preference dividend arrears are waived?', 'Undeclared arrears were never a recorded liability, so waiving them is simply disclosed in the notes.',
          [P('p1', 'Only disclosed', 6, 'disclos'), P('p2', 'Never recorded', 4, 'never|recorded')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Prerna Industries Ltd.', 'difficulty': 'moderate',
              'case': 'Prerna Industries Ltd. has 2,00,000 equity shares of ₹10 fully paid, a profit and loss debit balance of ₹9,00,000, goodwill ₹2,00,000 and machinery overvalued by ₹1,50,000. The scheme reduces shares to ₹5 each and creditors of ₹3,00,000 agree to accept 90%.',
              'mcqs': [
                  M('k1a', 'Total credits to capital reduction account:', ['₹10,30,000', '₹10,00,000', '₹9,00,000', '₹13,00,000'], 0,
                    'Share reduction 2,00,000 × ₹5 = ₹10,00,000 plus creditors\' sacrifice 10% of ₹3,00,000 = ₹30,000 gives ₹10,30,000. In practice: debit creditors.', 'moderate', check=1030000, topic=T3),
                  M('k1b', 'Total debits for losses and write-downs:', ['₹12,50,000', '₹11,00,000', '₹9,00,000', '₹10,50,000'], 0,
                    'P&L ₹9,00,000 + goodwill ₹2,00,000 + machinery ₹1,50,000 = ₹12,50,000. In practice: list all items in the scheme.', 'moderate', check=1250000, topic=T3),
                  M('k1c', 'The scheme as drafted:', ['Is insufficient, leaving a debit of ₹2,20,000', 'Leaves a capital reserve of ₹2,20,000', 'Balances exactly', 'Needs no change'], 0,
                    'Credits of ₹10,30,000 fall short of debits of ₹12,50,000 by ₹2,20,000, so the account would end with a debit balance; the reduction must be deeper. In practice: revise the scheme.', 'hard', topic=T3),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch14', 1, 'Internal Reconstruction',
                ['Explain the need for internal reconstruction.',
                 'Account for alteration of share capital.',
                 'Account for reduction of capital through the capital reduction account.',
                 'Record sacrifices by creditors and prepare the revised balance sheet.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 25, 'practice': 40}, 'prereq': ['int-p1-ch13-u01'],
                 'exam_tip': 'Draw the capital reduction account first; it must close without a debit balance.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Reorganise capital without liquidation.', 'Section 61 alteration: ordinary resolution, no reduction.',
                             'Section 66 reduction: special resolution + Tribunal.', 'Capital reduction account: credit reductions and sacrifices; debit losses and write-downs.',
                             'Surplus → capital reserve; no debit balance.', 'Waived preference arrears: disclose only.'],
                 'remember': ['Asset appreciation is credited to capital reduction.'],
                 'traps': ['Do not use capital reduction for consolidation or sub-division.']},
                [('Alteration', 's. 61, ordinary resolution'), ('Reduction', 's. 66, special resolution + Tribunal'), ('Surplus', 'Capital reserve')],
                viva, cases)
