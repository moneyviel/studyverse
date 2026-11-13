"""CA Intermediate · Paper 2 Corporate and Other Laws · Chapter 6 Registration of Charges (ss. 77–87 and Registration of Charges Rules, 2014).
Scope follows the ICAI study material; provisions are explained in original words; examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p2-ch06-u01'
T1 = 'Meaning of charge; fixed and floating charges'
T2 = 'Duty to register and time limits (s. 77)'
T3 = 'Effect of non-registration and constructive notice (ss. 77(3)-(4), 80)'
T4 = 'Registration by charge-holder, acquired property and modification (ss. 78-79)'
T5 = 'Registers of charges (ss. 81, 85)'
T6 = 'Satisfaction, receivers, penalties and rectification (ss. 82-87)'


def build():
    # i1 — time limits for a charge created on 4 March 2026
    ck = Checks()
    d30 = ck.add('(31-4)+3', 'Days from 4 March to 3 April')
    d60 = ck.add('30+30', 'Days from 4 March to 3 May')
    d120 = ck.add('60+(31-3)+30+2', 'Days from 4 March to 2 July (60 + 28 + 30 + 2)')
    i1 = {'id': 'i1', 'title': 'Counting the days for registration', 'difficulty': 'core', 'minutes': 6,
          'q': 'Udaan Castings Ltd. created a charge on its plant in favour of a bank on 4 March 2026. By which dates must it register the charge (a) with the normal fee, (b) to avoid ad valorem fees, and (c) at the latest with the Registrar\'s permission?',
          'solution': [table(['Stage', 'Period from creation', 'Last date'], [
              ['(a) Normal', f'{R(d30)} days', '3 April 2026'],
              ['(b) With additional fees (Registrar\'s permission)', f'{R(d60)} days', '3 May 2026'],
              ['(c) With ad valorem fees (Registrar\'s permission)', f'A further 60 days ({R(d120)} days in all)', '2 July 2026']], title='Section 77(1) — charges created on or after 2 November 2018'),
              note('Extensions need an application in CHG-1 (CHG-9 for debentures) with a declaration that late filing will not hurt intervening creditors, and the Registrar must be satisfied that there was sufficient cause.')],
          'checks': list(ck)}

    # i2 — priority after late registration
    ck2 = Checks()
    y = ck2.add('min(300, 200)', 'Bank Y (registered first) recovers in full (₹ lakh)')
    x = ck2.add('300-200', 'Bank X gets only the balance (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Who is paid first?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Rangoli Prints Ltd. mortgaged its warehouse to Bank X for ₹2 crore on 5 January 2026 but registered the charge only on 25 February 2026 with additional fees. Meanwhile, on 20 January it mortgaged the same warehouse to Bank Y for ₹2 crore, registered on 28 January. In liquidation the warehouse fetches ₹3 crore. How is it shared?',
          'solution': [table(['Lender', 'Position', '₹ lakh'], [
              ['Bank Y', 'Its rights arose and were registered before Bank X\'s charge was actually registered', R(y)],
              ['Bank X', 'Late registration cannot defeat rights acquired before it', R(x)]], title='Third proviso to section 77(1)'),
              p('Bank X can still sue the company for its unpaid ₹1 crore as an ordinary debt — section 77(4) keeps the obligation to repay alive even where security is lost.')],
          'checks': list(ck2)}

    fx = table(['Point', 'Fixed charge', 'Floating charge'], [
        ['Assets', 'Specific, identified, usually permanent (land, buildings, machinery)', 'A class of changing assets, present and future (stock, debtors, raw material)'],
        ['Dealing', 'Cannot be sold without the lender\'s consent', 'Can be used and sold in the ordinary course of business'],
        ['Buyer of asset', 'Takes subject to the charge', 'Takes free of the charge'],
        ['Becomes fixed', '—', 'On crystallisation: default enforced, business ceases, or liquidation']], title='Fixed vs floating charge')
    tl = table(['Event', 'Time limit', 'Form'], [
        ['Create or modify a charge', '30 days; +30 with additional fees; +60 more with ad valorem fees', 'CHG-1 / CHG-9 (debentures)'],
        ['Registrar\'s certificate', 'On registration / modification', 'CHG-2 / CHG-3'],
        ['Satisfaction of charge', '30 days; up to 300 days with additional fees', 'CHG-4; certificate CHG-5'],
        ['Receiver or manager appointed', '30 days of order or appointment', 'CHG-6'],
        ['Company\'s register of charges', 'Entries forthwith; kept permanently', 'CHG-7'],
        ['Rectification by Central Government', 'On application', 'CHG-8']], title='Key time limits and forms')

    concepts = [
        C('c1', T1, [
            'Section 2(16): a charge means a security interest or lien that a company grants over its assets, its undertakings or both; a mortgage is a charge too.',
            'A fixed charge attaches to specific, identified assets; the company may use them but cannot sell them without the lender\'s consent. It ends when the loan is repaid in full.',
            'A floating charge hovers over a changing class of assets such as stock or debtors. The company deals with them freely in the ordinary course, and buyers take them free of the charge.',
            'Crystallisation turns a floating charge into a fixed one over the assets then held — when the lender enforces after a breach, the business stops, or the company goes into liquidation.'],
          'A fixed charge holds a particular asset; a floating charge hovers until it lands.',
          'A bakery\'s flour stock under a floating charge can be baked and sold daily; its oven under a fixed charge cannot be sold without the bank\'s nod.',
          blocks=[fx]),
        C('c2', T2, [
            'Section 77: a company creating a charge on its property — tangible or otherwise, in or outside India — must register its particulars with the Registrar within 30 days, with the instrument signed by the company and the charge-holder. A charge by deposit of title deeds also needs registration.',
            'For charges created on or after 2 November 2018, the Registrar may allow registration within 60 days of creation on additional fees, and within a further 60 days on ad valorem fees (charged on the value of the charge). An application with a declaration that intervening creditors are not harmed is needed, and the Registrar must find sufficient cause.',
            'Copies of the instrument are verified by a director, the company secretary or an authorised officer of the charge-holder; where the property is only outside India, a person interested in the charge (other than the company) may also verify it.',
            'The Registrar issues a certificate of registration (CHG-2) or modification (CHG-3), which is conclusive evidence that the registration requirements were met. Certain charges in favour of the RBI are outside section 77.'],
          'Thirty days is the rule; every day beyond costs more and risks priority.',
          'A charge created in Dubai on the company\'s Dubai office still has to be registered in India.',
          blocks=[tl]),
        C('c3', T3, [
            'Section 77(3): a charge is not taken into account by a liquidator, an insolvency professional or any other creditor unless it is registered and a certificate issued. The lender becomes unsecured in a winding up.',
            'Section 77(4): non-registration does not cancel the debt; the lender can still recover the money as an ordinary creditor.',
            'Late registration does not affect rights acquired in the property before the charge was actually registered, so a later lender who registers first may rank ahead.',
            'Section 80: anyone acquiring the property, or an interest in it, is deemed to have notice of a registered charge from the date of registration (constructive notice). Registered particulars are public on the MCA portal, which also prevents the same asset being pledged twice.'],
          'Registration is what turns a private promise into security that the world must respect.',
          'A buyer of a registered-charge factory cannot later claim he did not know of the mortgage.'),
        C('c4', T4, [
            'Section 78: if the company does not register within 30 days, the charge-holder may apply. The Registrar gives notice to the company and, if no objection, registers within 14 days. The Registrar refuses if the company registers itself or shows sufficient cause. The charge-holder may recover the fees from the company.',
            'Section 79(a): a company acquiring property already subject to a charge must register that charge under section 77.',
            'Section 79(b): any modification of a registered charge must be registered — for example changing terms or interest rate (other than bank rate), increasing or reducing limits, ceding a pari passu charge, changing the repayment schedule, assigning the charge, or releasing part of the property.'],
          'If the borrower is lazy, the lender can protect itself; and every change must be put on record.',
          'A bank that raises a cash-credit limit from ₹5 crore to ₹8 crore requires the company to register the modification.'),
        C('c5', T5, [
            'Section 81: the Registrar keeps a register of all charges for each company; the particulars on the MCA portal are treated as that register, and anyone may inspect it on payment of a fee.',
            'Section 85: every company keeps a register of charges in CHG-7 at its registered office, covering all charges including floating charges, acquired property, modifications and satisfaction, with a copy of each instrument. Entries are made forthwith and authenticated by a director, the secretary or an authorised person.',
            'Members and creditors may inspect the company\'s register and instruments free during business hours; others pay a fee, subject to reasonable restrictions in the articles. The register is preserved permanently and instruments for eight years after satisfaction.'],
          'Two registers tell the same story: one at the Registrar, one at the registered office.',
          'A supplier who is a creditor may inspect the company\'s register of charges without paying.'),
        C('c6', T6, [
            'Section 82: the company must report full payment or satisfaction of a charge in CHG-4 within 30 days; the Registrar may allow up to 300 days on additional fees. The Registrar sends a show-cause notice to the charge-holder (up to 14 days) unless the form is signed by the charge-holder, then records satisfaction and issues CHG-5.',
            'Section 83: on evidence that a debt has been paid or property released, the Registrar may record satisfaction even without the company\'s intimation, and informs affected parties within 30 days.',
            'Section 84: whoever obtains an order for, or appoints, a receiver or manager of charged property must inform both the company and the Registrar, attaching the order or appointment document, within 30 days (CHG-6), and again on ceasing.',
            'Section 86: for default, the company pays a penalty of ₹5 lakh and each officer in default ₹50,000. Wilfully giving false information or suppressing material facts for registration attracts section 447 (fraud).',
            'Section 87: the Central Government (through Regional Directors) may extend time for intimation of satisfaction or rectify omissions or mis-statements, if satisfied the default was accidental or for sufficient cause and does not prejudice creditors or shareholders (CHG-8).'],
          'A charge should leave the record as carefully as it entered it.',
          'A company that repaid its loan but forgot to file CHG-4 can apply to the Regional Director for more time.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Charge filing tracker', 'role': 'Secretarial associate',
         'situation': 'A company signs three loan agreements and one top-up in a quarter.',
         'steps': ['Record creation dates and compute 30/60/120-day deadlines.', 'File CHG-1 with signed instruments.', 'Register the top-up as a modification.', 'Update the CHG-7 register forthwith.'],
         'takeaway': 'Every charge event needs a deadline diary.'},
        {'id': 'j2', 'title': 'Due diligence on a property purchase', 'role': 'Article assistant',
         'situation': 'A client is buying an office from a company.',
         'steps': ['Search the charges on the MCA portal.', 'Ask for satisfaction certificates for any charge shown.', 'Make the purchase subject to CHG-4 filing.'],
         'takeaway': 'Constructive notice means the buyer must look before buying.'},
    ]

    mcqs = [
        Q('m1', 'A charge on a company\'s stock-in-trade that the company may sell in the ordinary course is a:', ['Floating charge', 'Fixed charge', 'Pledge only', 'Lien that never crystallises'], 0,
          'A floating charge covers a changing class of assets, present and future, which the company may use and sell freely in normal business until crystallisation. Buyers take such goods free of the charge. In practice: lenders monitor stock statements.', 'c1', T1),
        Q('m2', 'A floating charge crystallises when:', ['The company goes into liquidation', 'The company buys new stock', 'The loan is renewed', 'The charge is registered'], 0,
          'Crystallisation happens when the lender enforces security after a breach, the company stops business, or it goes into liquidation. The charge then fixes on the assets held at that moment and they can no longer be dealt with. In practice: watch covenant breaches.', 'c1', T1),
        Q('m3', 'Normal period for registering a charge with the Registrar is:', ['30 days of creation', '60 days of creation', '21 days of creation', '90 days of creation'], 0,
          'Section 77(1) requires the particulars and instrument to be filed within 30 days of creating the charge. The Registrar may allow 60 days with additional fees and a further 60 days with ad valorem fees. In practice: file promptly to protect priority.', 'c2', T2, 'core', check=30),
        Q('m4', 'A charge created on 10 March 2026 and not registered within 30 days can be registered without ad valorem fees up to:', ['9 May 2026', '9 April 2026', '8 July 2026', '10 June 2026'], 0,
          'The 60-day window from creation, on additional fees, runs from 10 March to 9 May 2026. Beyond that, a further 60 days is available only with ad valorem fees. In practice: count from the date of creation, not discovery.', 'c2', T2, 'hard'),
        Q('m5', 'The certificate of registration of a charge issued by the Registrar is:', ['Conclusive evidence that registration requirements were complied with', 'Only prima facie evidence', 'Valid for one year', 'Required only for floating charges'], 0,
          'Under section 77(2) the certificate (CHG-2, or CHG-3 for modification) is conclusive evidence that the requirements of the Chapter and rules as to registration have been met. In practice: keep it with the loan file.', 'c2', T2),
        Q('m6', 'An unregistered charge is:', ['Not recognised by the liquidator, though the debt remains recoverable', 'Void along with the debt', 'Valid against all creditors', 'Treated as a fixed charge'], 0,
          'Section 77(3) prevents a liquidator or other creditor from taking an unregistered charge into account, but section 77(4) keeps the contract to repay alive, so the lender ranks as unsecured. In practice: register to keep security.', 'c3', T3),
        Q('m7', 'A purchaser of property with a registered charge is deemed to know of the charge from:', ['The date of registration of the charge', 'The date of purchase', 'The date he inspects the register', '30 days after creation'], 0,
          'Section 80 deems anyone acquiring charged property or an interest in it to know of the charge from the day it was registered, whether or not he actually searched. In practice: search the MCA records before buying.', 'c3', T3),
        Q('m8', 'If the charge-holder applies for registration, the Registrar registers it after giving notice to the company within:', ['14 days if there is no objection', '30 days', '7 days', '60 days'], 0,
          'Under section 78 the Registrar informs the company and, where it raises no objection, allows registration within 14 days. He will not do so if the company itself registers or shows sufficient cause. In practice: lenders use this route often.', 'c4', T4, 'core', check=14),
        Q('m9', 'Which is a modification of charge requiring registration?', ['Enhancing the loan limit secured by the charge', 'A change in the company\'s registered office', 'Appointment of a new director', 'Payment of an instalment on time'], 0,
          'Section 79(b) covers changes in terms, extent or operation of a charge — such as enhancing or reducing limits, changing interest (other than bank rate) or repayment schedule, ceding pari passu, assignment or partial release. In practice: file CHG-1 for each.', 'c4', T4),
        Q('m10', 'Who can inspect the company\'s register of charges free of charge?', ['A member or a creditor of the company', 'Any member of the public', 'Only the Registrar', 'Only directors'], 0,
          'Section 85(2) lets members and creditors inspect the register and instruments of charge during business hours without fees; other persons pay a prescribed fee, subject to reasonable restrictions in the articles. In practice: keep the register at the registered office.', 'c5', T5),
        Q('m11', 'Instruments creating or modifying a charge must be preserved for how long after satisfaction?', ['8 years', '5 years', 'Permanently', '3 years'], 0,
          'Under the rules, the register of charges is kept permanently, while each instrument creating or modifying a charge is kept for eight years from the date the charge is satisfied. In practice: archive instruments with the satisfaction certificate.', 'c5', T5, 'core', check=8),
        Q('m12', 'Intimation of satisfaction of a charge must normally be given within:', ['30 days of payment or satisfaction', '14 days', '60 days', '300 days in every case'], 0,
          'Section 82 requires the company to inform the Registrar in CHG-4 within 30 days of full payment or satisfaction; the Registrar may allow up to 300 days on additional fees. In practice: file CHG-4 as soon as the no-dues letter arrives.', 'c6', T6, 'core', check=30),
        Q('m13', 'Penalty on a company in default under the charges chapter (s. 86(1)) is:', ['₹5 lakh, and ₹50,000 on each officer in default', '₹1 lakh, and ₹10,000 on each officer', '₹10 lakh only', 'Imprisonment of officers only'], 0,
          'Section 86(1) imposes a penalty of ₹5 lakh on the company and ₹50,000 on every officer in default. Wilful false information or suppression attracts fraud under section 447 under section 86(2). In practice: penalties apply per default.', 'c6', T6, 'moderate'),
        Q('m14', 'Notice of appointment of a receiver of charged property must be given to the company and Registrar within:', ['30 days of the order or appointment', '7 days', '60 days', '14 days'], 0,
          'Section 84 requires the person obtaining the order or making the appointment to inform the company and Registrar within 30 days, attaching the order or appointing document; the Registrar records it, and a further notice is given on cessation. In practice: use Form CHG-6.', 'c6', T6, 'core', check=30),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Normal 30 days', 1, 'computation', '3 april', nums=[d30]),
           S('s2', 'Additional fee period', 1.5, 'computation', '3 may', nums=[d60]),
           S('s3', 'Ad valorem period', 1.5, 'computation', '2 july', nums=[d120])],
          ['Count from creation.'], ['Counting from the date the default was noticed.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Late registration does not defeat earlier rights', 2, 'concept', 'before|prior'),
           S('s2', 'Bank Y paid in full', 1, 'computation', 'bank y', nums=[y]),
           S('s3', 'Bank X balance; debt survives', 2, 'computation', 'sue|ordinary|unsecured', nums=[x])],
          ['Apply the third proviso to section 77(1).'], ['Ranking by date of creation alone.'], ['Table + note.'], pad='table', checks=list(ck2)),
        W('q3', 4, 'Nirmal Pvt. Ltd. bought a factory from Sagar Ltd. that was mortgaged to a bank with the bank\'s consent. Six months later Nirmal\'s accountant says nothing needs to be filed because Sagar created the charge. Advise.',
          [legal('Sections 77 and 79(a)',
                 'Nirmal acquired property already subject to a registered charge.',
                 'Section 79(a) applies the registration provisions of section 77 to a company acquiring property subject to a charge. The acquiring company must register the charge in its own name within the time limits, and the charge-holder may also apply under section 78. Default attracts penalties under section 86.',
                 'The accountant is wrong; Nirmal must register the charge now, seeking the Registrar\'s permission for late filing where the period allows.')],
          [S('s1', 'Section 79(a)', 1.5, 'concept', '79'),
           S('s2', 'Acquirer must register', 1.5, 'application', 'acquir'),
           S('s3', 'Conclusion', 1, 'conclusion', 'wrong|must register')],
          ['Name the section first.'], ['Assuming only the original creator files.'], ['Provision → facts → analysis → conclusion.']),
    ]

    viva = [
        V('v1', 'What is a charge?',
          'A security interest or lien that a company grants over its assets or undertakings to back a loan; a mortgage also counts as a charge.',
          [P('p1', 'Interest or lien as security', 6, 'lien|interest', 'security'), P('p2', 'Includes mortgage', 4, 'mortgage')], 'c1'),
        V('v2', 'What is crystallisation of a floating charge?',
          'It is the moment a floating charge becomes a fixed charge over the assets then held, as when the lender enforces after a default, the company stops business or goes into liquidation.',
          [P('p1', 'Becomes fixed', 6, 'fixed'), P('p2', 'Triggers', 4, 'liquidation|default|enforce')], 'c1'),
        V('v3', 'What is the effect of failing to register a charge?',
          'The liquidator and other creditors ignore the charge, so the lender ranks as unsecured, though the debt itself remains recoverable; late registration also cannot defeat rights acquired meanwhile.',
          [P('p1', 'Security lost', 6, 'unsecured|ignore|not taken'), P('p2', 'Debt survives', 4, 'debt|recover')], 'c3'),
        V('v4', 'What is constructive notice of a charge?',
          'Anyone acquiring charged property is deemed to know of a registered charge from the date of registration, whether or not he actually checked the records.',
          [P('p1', 'Deemed knowledge', 6, 'deemed'), P('p2', 'From registration', 4, 'registration')], 'c3'),
        V('v5', 'When can the Central Government rectify the register of charges?',
          'When omission to report satisfaction in time, or an omission or mis-statement in a filing, was accidental, inadvertent or for sufficient cause and does not prejudice creditors or shareholders, on application in Form CHG-8.',
          [P('p1', 'Accidental or sufficient cause', 6, 'accidental|inadvert|sufficient'), P('p2', 'CHG-8', 4, 'chg-8|chg 8')], 'c6'),
    ]

    cases = [{'id': 'k1', 'title': 'Kesar Agro Ltd.', 'difficulty': 'moderate',
              'case': 'Kesar Agro Ltd. created a charge on its cold storage in favour of Prabhat Bank on 1 June 2026 but did not register it. On 15 June it created a second charge on the same property in favour of Unnati Bank, registered on 22 June. Prabhat Bank discovers the lapse on 5 July. Kesar also repaid an old term loan in full on 1 May 2026 but has not told the Registrar.',
              'mcqs': [
                  M('k1a', 'What can Prabhat Bank do on 5 July?', ['Apply to the Registrar itself under section 78 and recover the fees from Kesar', 'Nothing, as only the company can register', 'Sue Unnati Bank', 'Wait for the company to file within 300 days'], 0,
                    'When the company fails to register within 30 days, the charge-holder may apply; the Registrar gives notice and registers within 14 days if there is no objection, and the charge-holder recovers the fees from the company. In practice: lenders file promptly.', 'core', topic=T4),
                  M('k1b', 'If Prabhat\'s charge is registered on 20 July, its priority against Unnati Bank is:', ['Behind Unnati Bank, whose rights arose before Prabhat\'s registration', 'Ahead, as it was created first', 'Equal', 'Void entirely'], 0,
                    'Late registration does not prejudice rights acquired in the property before the charge is actually registered. Unnati\'s charge was created and registered first, so it ranks ahead. In practice: delay costs priority.', 'moderate', topic=T3),
                  M('k1c', 'Last date for Kesar to report satisfaction of the old loan without seeking extra time:', ['31 May 2026', '1 June 2026', '15 June 2026', '30 June 2026'], 0,
                    'Section 82 requires intimation within 30 days of full payment; 30 days from 1 May 2026 ends on 31 May 2026. The Registrar may allow up to 300 days with additional fees. In practice: file CHG-4 on receiving the no-dues certificate.', 'moderate', topic=T6),
                  M('k1d', 'For the default in registration, the penalty on Kesar Agro Ltd. is:', ['₹5 lakh', '₹50,000', '₹1 lakh', '₹10 lakh'], 0,
                    'Section 86(1) imposes a penalty of ₹5 lakh on the company and ₹50,000 on each officer in default for contravening the charges chapter. Fraud provisions apply only to wilful false information or suppression. In practice: officers are separately liable.', 'core', check=5, topic=T6),
              ]}]

    return unit(UID, 'p2', 'int-p2-ch06', 1, 'Registration of Charges',
                ['Define a charge and distinguish fixed and floating charges.',
                 'Apply the duty and time limits to register charges and modifications.',
                 'Explain the effects of non-registration, priority and constructive notice.',
                 'Explain registers of charges, satisfaction, receivers, penalties and rectification.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 30}, 'prereq': ['int-p2-ch05-u01'],
                 'exam_tip': 'Date questions are common: count 30, 60 and a further 60 days from creation; 30 and 300 days from satisfaction.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Charge = interest or lien as security; includes mortgage.', 'Fixed vs floating; crystallisation on enforcement, cessation or liquidation.',
                             'Register within 30 days; 60 days with additional fees; further 60 days with ad valorem fees.', 'Unregistered charge ignored by liquidator; debt survives; priority lost.',
                             'Constructive notice from date of registration (s. 80).', 'Charge-holder may register (s. 78); acquirer and modifications too (s. 79).',
                             'Satisfaction: 30 days, up to 300 days; Registrar may act on evidence (s. 83).', 'Penalty ₹5 lakh / ₹50,000; rectification by Central Government (s. 87).'],
                 'remember': ['Members and creditors inspect free.', 'Register permanent; instruments 8 years after satisfaction.'],
                 'traps': ['Count from creation, not discovery.', 'Charge-holder route needs no objection from the company.']},
                [('Registration', '30 / 60 / +60 days'), ('Satisfaction', '30 / 300 days'), ('Registrar notice', '14 days'), ('Penalty', '₹5 lakh company · ₹50,000 officer')],
                viva, cases)
