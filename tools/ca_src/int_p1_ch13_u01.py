"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 13 — Amalgamation of Companies (accounting entries).
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch13-u01'
T1 = 'Amalgamation, absorption and external reconstruction'
T2 = 'Computing purchase consideration and exchange ratios'
T3 = 'Closing the books of the transferor company'
T4 = 'Entries in the books of the transferee company'
T5 = 'Inter-company holdings, debts and unrealised profit'


def build():
    ck = Checks()
    net = ck.add('1500000-400000', 'Book value of net assets taken over (₹)')
    prof = ck.add('1300000-1100000-20000', 'Profit on realisation (₹)')
    i1 = {'id': 'i1', 'title': 'Realisation account of the transferor', 'difficulty': 'core', 'minutes': 8,
          'q': 'Lotus Ltd. is absorbed by Rose Ltd. Lotus\'s assets (book value) total ₹15,00,000 and its liabilities taken over are ₹4,00,000. Rose pays purchase consideration of ₹13,00,000. Lotus pays its own liquidation expenses of ₹20,000. Compute the profit or loss on realisation.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Net assets transferred at book value', '15,00,000 − 4,00,000', inr(net)],
              ['Purchase consideration', '', inr(1300000)],
              ['Less: liquidation expenses borne by Lotus', '', inr(20000)],
              ['Profit on realisation (to equity shareholders)', '13,00,000 − 11,00,000 − 20,000', inr(prof)]], title='Realisation account')],
          'checks': list(ck)}

    ck2 = Checks()
    ratio = ck2.add('30/40', 'Shares of Rose for each Lotus share')
    newsh = ck2.add('100000*0.75', 'Shares to be issued by Rose')
    up = ck2.add('60000*20/120', 'Unrealised profit in Rose\'s stock bought from Lotus (₹)')
    i2 = {'id': 'i2', 'title': 'Exchange ratio and inter-company items', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Intrinsic values are ₹40 per Rose share and ₹30 per Lotus share; Lotus has 1,00,000 shares. Rose holds stock of ₹60,000 bought from Lotus at cost plus 20%, and Lotus owes Rose ₹50,000. Compute the shares to be issued and the adjustments in Rose\'s books.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Exchange ratio', '30 ÷ 40', f'{R(ratio)} Rose share per Lotus share'],
              ['Shares issued', '1,00,000 × 0.75', R(newsh)],
              ['Inter-company debt', 'Cancel payable and receivable', inr(50000)],
              ['Unrealised profit in stock', '60,000 × 20/120', inr(up)]], title='Exchange ratio and adjustments'),
              note('The unrealised profit is removed from stock by reducing reserves (or goodwill/capital reserve) in Rose\'s books after amalgamation.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'In an amalgamation two or more companies combine: either a new company is formed to take over existing ones, or an existing company absorbs one or more others (absorption).',
            'External reconstruction is when a new company is formed to take over an existing company\'s business, usually to restructure it.',
            'For accounting, AS 14 classifies amalgamations as being in the nature of merger (pooling of interests method) or purchase (purchase method).'],
          'Whatever the legal form, the accounting follows merger or purchase.',
          'A newly formed company taking over a struggling company\'s business is an external reconstruction.'),
        C('c2', T2, [
            'Purchase consideration is the payment to the transferor\'s shareholders in shares, securities, cash or other assets.',
            'Methods: lump sum (stated amount); net payment (sum of all payments to shareholders); net assets (agreed value of assets taken over less liabilities taken over); and intrinsic value (number of shares based on each company\'s value per share).',
            'Intrinsic value per share = net assets available to equity shareholders ÷ number of equity shares. The exchange ratio is the transferor\'s value per share divided by the transferee\'s value per share.',
            'Payments to debenture holders and creditors, and liquidation expenses borne by the transferee, are not part of purchase consideration.'],
          'Value both companies per share; the ratio decides how many new shares are issued.',
          'If a transferor share is worth ₹60 and a transferee share ₹40, each transferor share gets 1.5 new shares.'),
        C('c3', T3, [
            'The transferor closes its books through a realisation account: assets (except cash if retained) are transferred at book values to its debit; liabilities taken over to its credit; purchase consideration is credited with a debit to the transferee\'s account.',
            'Receipt of consideration is debited to shares, securities or bank. Liabilities not taken over are paid; liquidation expenses are debited to realisation (if borne by the transferor).',
            'Share capital and reserves are transferred to equity shareholders\' account; profit or loss on realisation also goes there. Preference shareholders are paid as agreed, any difference going to realisation.',
            'Finally, shares and cash received are distributed to shareholders, closing all accounts.'],
          'Realisation account collects everything; shareholders\' account settles the rest.',
          'Fictitious assets like preliminary expenses are transferred to the equity shareholders\' account, not realisation.'),
        C('c4', T4, [
            'Purchase method: the transferee debits "Business purchase" and credits the liquidator of the transferor with the consideration; it then records assets and liabilities at agreed values, with goodwill or capital reserve for the difference. Statutory reserves are recorded against an Amalgamation Adjustment Reserve.',
            'Pooling method: assets, liabilities and reserves are recorded at book values; the difference between consideration and transferor\'s share capital is adjusted in reserves.',
            'Shares issued are recorded at nominal value plus premium; liquidation expenses paid by the transferee are debited to goodwill (or capital reserve) under the purchase method.',
            'The post-amalgamation balance sheet is prepared in Schedule III format with notes.'],
          'The transferee records what it bought and what it paid.',
          'Shares issued at ₹12 (face ₹10) credit share capital ₹10 and securities premium ₹2 per share.'),
        C('c5', T5, [
            'Inter-company owings (debtors and creditors, bills) are cancelled in the transferee\'s books after amalgamation.',
            'Unrealised profit on goods sold between the companies still in stock is removed from stock against reserves or the goodwill/capital reserve.',
            'If the transferee holds shares in the transferor, consideration is paid only to outside shareholders; the investment is cancelled, its cost compared with the share of net assets.',
            'If the transferor holds shares in the transferee, those shares are part of assets taken over and may be cancelled or reissued as agreed.'],
          'Remove everything the two companies owed or earned from each other.',
          'If the transferee already owns 20% of the transferor, only the other 80% receive consideration.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Amalgamation working papers', 'role': 'Accounts executive',
             'situation': 'Your company is absorbing a sister company; the scheme fixes an exchange ratio and agreed asset values.',
             'steps': ['Compute purchase consideration and shares to be issued.', 'Prepare realisation and shareholders\' accounts for the transferor.', 'Record assets, liabilities, goodwill or capital reserve in the transferee.', 'Eliminate inter-company debts and unrealised profit.'],
             'takeaway': 'Two sets of books close and open in one transaction.'}]

    mcqs = [
        Q('m1', 'In the transferor\'s books, purchase consideration is credited to:', ['Realisation account', 'Equity shareholders account', 'Share capital', 'Goodwill'], 0,
          'The transferor debits the transferee (purchasing company) and credits realisation account with the purchase consideration, as part of working out profit or loss on realisation. In practice: then receive the shares or cash.', 'c3', T3),
        Q('m2', 'Preliminary expenses of the transferor at amalgamation are transferred to:', ['Equity shareholders account', 'Realisation account', 'Transferee', 'Goodwill'], 0,
          'Fictitious assets such as preliminary expenses are not transferred to the transferee; they reduce what belongs to equity shareholders and are debited to their account. In practice: close them first.', 'c3', T3),
        Q('m3', 'Intrinsic value per share of A ₹50 and of B ₹25. For each share of B, A issues:', ['0.5 share', '2 shares', '1 share', '1.5 shares'], 0,
          'Exchange ratio = value of B share ÷ value of A share = 25 ÷ 50 = 0.5, so each B share gets half an A share. In practice: fractional entitlements are settled in cash.', 'c2', T2, 'moderate', check=0.5),
        Q('m4', 'Under the net assets method, purchase consideration equals:', ['Agreed value of assets taken over less liabilities taken over', 'Book value of share capital', 'Market value of shares', 'Assets at book value'], 0,
          'The net assets method values the business taken over as the agreed values of assets less the liabilities taken over, which equals the consideration. In practice: exclude fictitious assets.', 'c2', T2),
        Q('m5', 'Liquidation expenses of the transferor paid by the transferee (purchase method) are debited to:', ['Goodwill (or reduce capital reserve)', 'Profit and loss of the transferor', 'Share capital', 'Realisation account of the transferee'], 0,
          'Under the purchase method, liquidation expenses borne by the transferee are part of the cost of acquisition and debited to goodwill or set against capital reserve. In practice: the transferor makes no entry if it bears nothing.', 'c4', T4),
        Q('m6', 'Inter-company debts between the amalgamating companies are:', ['Cancelled in the transferee\'s books', 'Paid in cash', 'Added to goodwill', 'Shown as contingent liabilities'], 0,
          'After amalgamation, the debtor and creditor are the same company, so the mutual owings are cancelled by a contra entry in the transferee\'s books. In practice: reconcile balances first.', 'c5', T5),
        Q('m7', 'Stock ₹36,000 bought from the transferor at cost plus 20%. Unrealised profit:', ['₹6,000', '₹7,200', '₹3,600', '₹4,800'], 0,
          'Profit included = 36,000 × 20/120 = ₹6,000, which is removed from stock against reserves or goodwill/capital reserve. In practice: use margin on selling price.', 'c5', T5, 'moderate', check=6000),
        Q('m8', 'If the transferee already holds 30% of the transferor\'s shares, consideration is paid to:', ['The remaining 70% shareholders only', 'All shareholders', 'The transferee itself too', 'Debenture holders'], 0,
          'A company does not pay itself; consideration goes only to outside shareholders, and the transferee\'s existing investment is cancelled against its share of net assets. In practice: adjust goodwill.', 'c5', T5),
        Q('m9', 'Assets ₹20 lakh (book), liabilities taken over ₹6 lakh, consideration ₹12 lakh, no expenses. Realisation shows:', ['Loss of ₹2 lakh', 'Profit of ₹2 lakh', 'Loss of ₹8 lakh', 'Nil'], 0,
          'Net assets transferred at book value are ₹14 lakh; consideration ₹12 lakh is ₹2 lakh less, a loss on realisation borne by equity shareholders. In practice: post it to their account.', 'c3', T3, 'moderate'),
        Q('m10', 'External reconstruction means:', ['A new company formed to take over an existing company\'s business', 'Reducing share capital internally', 'Merging two subsidiaries', 'Buying back shares'], 0,
          'In external reconstruction a new company is formed to take over the business of an existing company, which is then wound up; internal reconstruction happens without liquidation. In practice: accounting is similar to absorption.', 'c1', T1),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Net assets at book value', 1.5, 'computation', 'net assets', nums=[net]),
           S('s2', 'Profit on realisation', 2.5, 'computation', 'realisation', nums=[prof])],
          ['Use book values in the transferor.'], ['Using agreed values in the transferor\'s books.'], ['Account format or table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Exchange ratio', 2, 'computation', 'ratio', nums=[ratio, newsh]),
           S('s2', 'Debt cancelled', 1, 'concept', 'cancel'),
           S('s3', 'Unrealised profit', 2, 'computation', 'unrealised', nums=[up])],
          ['Value per share of each company.'], ['Inverting the ratio.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What are the methods of computing purchase consideration?', 'Lump sum, net payment, net assets and intrinsic value (exchange ratio) methods.',
          [P('p1', 'Net payment and net assets', 6, 'net payment|net assets'), P('p2', 'Lump sum or intrinsic', 4, 'lump|intrinsic')], 'c2'),
        V('v2', 'How does the transferor close its books?', 'Through a realisation account for assets and liabilities taken over and consideration, and an equity shareholders account that receives capital, reserves, realisation profit and the final distribution.',
          [P('p1', 'Realisation account', 5, 'realisation'), P('p2', 'Shareholders account', 5, 'shareholders')], 'c3'),
        V('v3', 'What is the exchange ratio?', 'The number of transferee shares given for one transferor share, equal to the transferor\'s value per share divided by the transferee\'s value per share.',
          [P('p1', 'Shares for one share', 5, 'one'), P('p2', 'Value per share ratio', 5, 'value per share|divided')], 'c2'),
        V('v4', 'How are inter-company owings treated?', 'They are cancelled against each other in the transferee\'s books after amalgamation.',
          [P('p1', 'Cancelled', 6, 'cancel'), P('p2', 'Transferee books', 4, 'transferee')], 'c5'),
        V('v5', 'What happens to unrealised profit on inter-company stock?', 'It is removed from the stock value and debited to reserves or adjusted against goodwill or capital reserve.',
          [P('p1', 'Removed from stock', 6, 'stock'), P('p2', 'Against reserves or goodwill', 4, 'reserve|goodwill')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Asha Ltd. absorbs Bhakti Ltd.', 'difficulty': 'moderate',
              'case': 'Asha Ltd. absorbs Bhakti Ltd. (purchase method). Bhakti has 2,00,000 equity shares; Asha agrees to issue 1 share of ₹10 at ₹15 for every 2 Bhakti shares and pay ₹1 per Bhakti share in cash. Bhakti\'s net assets at agreed values are ₹16,50,000.',
              'mcqs': [
                  M('k1a', 'Purchase consideration:', ['₹17,00,000', '₹15,00,000', '₹10,00,000', '₹16,50,000'], 0,
                    'Shares: 1,00,000 × ₹15 = ₹15,00,000; cash: 2,00,000 × ₹1 = ₹2,00,000; total ₹17,00,000 under the net payment method. In practice: value shares at the issue price.', 'moderate', check=1700000, topic=T2),
                  M('k1b', 'Goodwill in Asha\'s books:', ['₹50,000', '₹1,50,000', 'Capital reserve ₹50,000', 'Nil'], 0,
                    'Consideration ₹17,00,000 exceeds net assets ₹16,50,000 by ₹50,000, recorded as goodwill under the purchase method. In practice: amortise it.', 'moderate', check=50000, topic=T4),
                  M('k1c', 'Securities premium credited by Asha:', ['₹5,00,000', '₹10,00,000', '₹15,00,000', '₹2,00,000'], 0,
                    '1,00,000 shares issued at ₹5 premium each give ₹5,00,000 of securities premium; ₹10,00,000 goes to share capital. In practice: record both credits in one entry.', 'core', check=500000, topic=T4),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch13', 1, 'Amalgamation of Companies',
                ['Distinguish amalgamation, absorption and external reconstruction.',
                 'Compute purchase consideration and exchange ratios.',
                 'Close the books of the transferor company.',
                 'Record the amalgamation in the transferee\'s books, including inter-company adjustments.'],
                {'difficulty': 'hard', 'minutes': {'learn': 35, 'practice': 50}, 'prereq': ['int-p1-ch12-u01'],
                 'exam_tip': 'Compute purchase consideration first, then prepare realisation, shareholders\' and transferee entries in that order.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Amalgamation, absorption, external reconstruction.', 'PC methods: lump sum, net payment, net assets, intrinsic value.',
                             'Transferor: realisation account, shareholders account, final distribution.', 'Transferee: business purchase, assets and liabilities, goodwill/capital reserve.',
                             'Cancel inter-company owings; remove unrealised profit.', 'Pay only outside shareholders where shares are cross-held.'],
                 'remember': ['Fictitious assets go to shareholders, not realisation.'],
                 'traps': ['Debenture holders are not paid out of purchase consideration.']},
                [('PC methods', 'Lump sum · net payment · net assets · intrinsic'), ('Exchange ratio', 'Transferor value ÷ transferee value'), ('Inter-company', 'Cancel and remove profit')],
                viva, cases)
