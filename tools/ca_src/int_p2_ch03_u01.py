"""CA Intermediate · Paper 2 Corporate and Other Laws · Chapter 3 Prospectus and Allotment of Securities (ss. 23–42, 447).
Scope follows the ICAI study material; provisions are explained in original words; examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p2-ch03-u01'
T1 = 'Modes of issue and meaning of securities (s. 23, 24)'
T2 = 'Prospectus and deemed prospectus (s. 2(70), 25)'
T3 = 'Contents, filing and validity of prospectus (s. 26–30)'
T4 = 'Shelf, red herring and abridged prospectus (s. 31–33)'
T5 = 'Misstatements: civil and criminal liability (s. 34–37)'
T6 = 'Personation and fraud (s. 38, 447)'
T7 = 'Allotment of securities (s. 39)'
T8 = 'Stock exchange dealing and commission (s. 40)'
T9 = 'GDRs (s. 41) and private placement (s. 42)'


def build():
    ck = Checks()
    cap = ck.add('min(0.05, 0.03)*120*1000000', 'Maximum underwriting commission on 10,00,000 shares issued at ₹120 when articles allow 3%')
    days = ck.add('28-24', 'Days of delay: PAS-3 due 24 November (15 days after 9 November), filed 28 November')
    pen = ck.add('min(1000*4, 2500000)', 'Penalty for delayed PAS-3 under s. 42(9) — ₹1,000 per day, cap ₹25 lakh')
    i1 = {'id': 'i1', 'title': 'Three quick computations', 'difficulty': 'core', 'minutes': 8,
          'q': '(a) Kuber Ltd. issues 10,00,000 shares at ₹120 each; its articles allow underwriting commission of 3%. What is the maximum commission? (b) Neela Pvt. Ltd. allotted securities on private placement on 9 November 2025 and filed PAS-3 on 28 November 2025. What penalty applies? (c) A public issue states minimum subscription of ₹90 crore; ₹72 crore is received. Can the company allot?',
          'solution': [table(['Part', 'Working', 'Answer'], [
              ['(a) Commission cap', 'Lower of 5% of issue price and rate in articles (3%): 3% × ₹120 × 10,00,000', R(cap)],
              ['(b) Late PAS-3', f'Due within 15 days, i.e. by 24 November; {days} days late × ₹1,000', R(pen) + ' each on company, promoters and directors'],
              ['(c) Minimum subscription', '₹72 crore < ₹90 crore stated', 'No allotment; refund application money (within 15 days of closure)']], title='Answers'),
              note('Commission may be paid out of the issue proceeds, profits, or both.')],
          'checks': list(ck)}

    modes = table(['Mode of issue', 'Public company', 'Private company'], [
        ['Public offer — IPO, FPO, offer for sale (through prospectus)', 'Yes', 'No'],
        ['Private placement (s. 42)', 'Yes', 'Yes'],
        ['Rights issue / bonus issue', 'Yes', 'Yes'],
        ['SEBI regulations also apply', 'If listed or proposing to list', 'No'],
    ], title='Ways to issue securities (s. 23)')
    pros = table(['Type', 'Key feature'], [
        ['Prospectus (s. 2(70))', 'Any document issued as a prospectus or any notice, circular or advertisement inviting the public to subscribe or buy securities; includes red herring and shelf prospectus'],
        ['Deemed prospectus (s. 25)', 'Offer document used when securities allotted to an intermediary are offered for sale to the public — presumed if offered within 6 months of allotment or before full consideration is received'],
        ['Shelf prospectus (s. 31)', 'One prospectus for several issues over a validity of up to one year from the first offer; information memorandum before each later offer'],
        ['Red herring prospectus (s. 32)', 'Lacks complete price or quantity details; filed at least 3 days before the issue opens; used in book building'],
        ['Abridged prospectus (s. 33)', 'Summary containing salient features as specified by SEBI; must accompany every application form'],
    ], title='Kinds of prospectus')
    liab = table(['Basis', 'Section 34 — criminal', 'Section 35 — civil'], [
        ['Who is liable', 'Every person who authorises the issue', 'Company, directors at issue, persons named as directors, promoters, persons authorising issue, experts'],
        ['Consequence', 'Punishment under section 447', 'Compensation to every person who suffered loss (plus any s. 36 punishment)'],
        ['Is loss needed?', 'No', 'Yes — loss or damage from acting on the prospectus'],
        ['Defences', 'Misstatement immaterial; reasonable belief that it was true or the omission was necessary', 'Withdrew consent as director; issued without knowledge and public notice given; reliance on competent expert; reasonable belief till allotment; correct copy of an official document'],
        ['Fraudulent intent', '—', 'Unlimited personal liability for all losses'],
    ], title='Liability for misstatements in prospectus')
    fraud = table(['Fraud', 'Imprisonment', 'Fine'], [
        ['Below ₹10 lakh or 1% of turnover (whichever lower), no public interest', 'Up to 5 years', 'Up to ₹50 lakh (or both)'],
        ['At least ₹10 lakh or 1% of turnover (whichever lower)', '6 months to 10 years', 'Not less than the amount involved, up to 3 times it'],
        ['Involving public interest', '3 years to 10 years', 'Not less than the amount involved, up to 3 times it'],
    ], title='Punishment for fraud (s. 447)')
    pp = table(['Requirement', 'Rule'], [
        ['Offerees', 'Not more than 200 identified persons in a financial year per kind of security (excluding QIBs and ESOP employees); otherwise deemed public offer'],
        ['Approval', 'Special resolution for each offer (Board resolution or annual special resolution in specified NCD and QIB cases)'],
        ['Offer letter', 'PAS-4, serially numbered, addressed to the person, sent within 30 days of recording names; no renunciation; record in PAS-5'],
        ['Payment', 'Cheque, demand draft or banking channel from the subscriber\'s own account (first joint holder for joint holdings) — never cash'],
        ['Allotment', 'Within 60 days of receiving money; else refund within next 15 days, failing which 12% p.a. interest from the 60th day'],
        ['Money', 'Kept in a separate scheduled-bank account; not used until allotment and PAS-3 filing'],
        ['Return of allotment', 'PAS-3 within 15 days; default ₹1,000 per day up to ₹25 lakh on company, promoters and directors'],
        ['Advertising', 'No public advertisement or use of media, marketing channels or agents'],
        ['Contravention', 'Penalty on promoters and directors up to the amount raised or ₹2 crore, whichever is lower; refund within 30 days of order'],
    ], title='Private placement (s. 42 and rule 14)')

    concepts = [
        C('c1', T1, [
            'Section 23: a public company may issue securities by public offer through prospectus (IPO, FPO or offer for sale by existing holders), by private placement under section 42, or by rights or bonus issue. A private company may use only rights/bonus issues and private placement.',
            '"Securities" (s. 2(81)) takes the SCRA meaning: shares, bonds, debentures and similar marketable securities, derivatives, units of collective investment schemes and mutual funds, security receipts, certain pass-through certificates of special purpose entities, government securities, notified instruments and rights in securities — but not unit-linked insurance policies.',
            'Notified classes of public companies may list notified securities directly on permitted foreign exchanges (s. 23(3)), and the Central Government may exempt them from specified provisions (s. 23(4)).',
            'Section 24: SEBI administers provisions on issue and transfer of securities and non-payment of dividend for listed and to-be-listed companies; other matters (e.g. prospectus filing, return of allotment, redemption of preference shares) are administered by the Central Government, Tribunal or Registrar.'],
          'A public company can sell in the open market and to friends; a private company may only sell to friends and existing members.',
          'An IPO is a public offer; a start-up\'s angel round is a private placement.',
          blocks=[modes]),
        C('c2', T2, [
            'A prospectus includes any document issued as such and any notice, circular, advertisement or other document inviting public offers to subscribe for or buy securities; it includes red herring and shelf prospectuses.',
            '"Public" includes any section of the public, however selected — persons not personally known to the promoter. A document marked "for private circulation" but sent to thousands of members of other companies was a prospectus (South of England Natural Gas). A single private communication is not an "issue" (Nash v. Lynde).',
            'Deemed prospectus (s. 25): where a company allots securities with a view to their being offered for sale to the public, the offer document is treated as a prospectus. Such intent is presumed if the public offer comes less than six months after allotment, or while part of the consideration is still unpaid to the company.',
            'Besides the section 26 contents, the deemed prospectus must state the net consideration received or receivable and the time and place where the underlying contract can be inspected; the persons making the offer are treated as if named in a prospectus as directors. Where the offeror is a company, signature by two of its directors is enough. A rights issue renounceable in favour of more than fifty outsiders may also become a deemed prospectus.'],
          'Whatever it is called, if the document invites strangers to buy securities, the law treats it as a prospectus.',
          'Offer-for-sale documents used by merchant bankers who bought shares to resell are classic deemed prospectuses.'),
        C('c3', T3, [
            'Section 26: the prospectus must be dated and signed and contain the information and financial reports specified by SEBI (in consultation with the Central Government), with a declaration of compliance with the Act and that nothing in it contravenes the Companies Act, SCRA, SEBI Act and their rules. These content rules do not apply to offers only to existing members or debenture holders, or for securities uniform with those already listed.',
            'The date on the prospectus is deemed its date of publication. A copy signed by every person named as director or proposed director (or attorney) must be filed with the ROC before issue, and the prospectus must say so on its face.',
            'An expert\'s statement may be included only if the expert is not engaged or interested in the company\'s formation, promotion or management and has given written consent not withdrawn before filing.',
            'The prospectus is valid for issue only within 90 days of filing with the ROC. Contravention of section 26: fine ₹50,000 to ₹3 lakh on the company and every person knowingly a party.',
            'Section 27: contract terms or objects stated in a prospectus can be varied only by special resolution (by postal ballot) with newspaper publicity and justification; proceeds cannot be used to trade in equity of other listed companies; dissenters get an exit offer from promoters or controlling shareholders as per SEBI.',
            'Section 28: members may, with the Board, offer their shares to the public; the document is a prospectus; they authorise the company to act and reimburse its expenses. Section 29: public offers must be in demat form (and prescribed unlisted companies must hold and transfer in demat). Section 30: an advertisement of a prospectus must state the memorandum\'s objects, members\' liability, share capital, signatories and their shares, and capital structure.'],
          'A prospectus is like a food label filed with the regulator — it must be accurate, signed, fresh (90 days) and cannot be quietly changed later.',
          'Companies change "objects of the issue" only with postal-ballot approval and an exit route for dissenting shareholders.'),
        C('c4', T4, [
            'Shelf prospectus (s. 31): classes of companies allowed by SEBI may file one prospectus at the first offer, valid for up to one year from the opening of the first offer; later offers need no fresh prospectus.',
            'Before each later offer, an information memorandum (PAS-2) must be filed (within one month before the offer) disclosing new charges, changes in financial position since the last offer and other prescribed changes. Applicants who paid in advance before a change must be told and, if they withdraw, refunded in full within 15 days. Memorandum plus shelf prospectus is deemed a prospectus.',
            'Red herring prospectus (s. 32): does not contain complete price or quantity; filed with the ROC at least three days before the issue opens; carries the same obligations as a prospectus; variations are highlighted in the final prospectus, which after closure states the capital raised, closing price and other details and is filed with the ROC and SEBI. It supports book building (price discovery within a band).',
            'Abridged prospectus (s. 33): a SEBI-specified summary that must accompany every application form, except forms issued for underwriting arrangements, for securities not offered to the public, or offers only to existing members. A full prospectus must be given to anyone who asks before the issue closes. Default: ₹50,000 per default.'],
          'A shelf prospectus is a season pass; a red herring prospectus is a menu without prices until the auction ends.',
          'Banks and NBFCs use shelf prospectuses for repeated bond issues within a year.',
          blocks=[pros]),
        C('c5', T5, [
            'A share contract is one of utmost good faith. A statement is deemed untrue if it misleads in its form and context, or if any inclusion or omission is likely to mislead — e.g. claiming directors took a large part of the capital when each took ten shares, or showing regular dividends that hid losses (Rex v. Kylsant), or using ambiguous figures (Smith v. Chadwick).',
            'Remedies of a misled allottee: rescission (only for original allottees, not market buyers or memorandum subscribers), damages for fraud, compensation under section 35, damages for deceit against those responsible (Peek v. Gurney — market purchasers who did not rely on the prospectus cannot sue), and criminal liability under section 34. They are alternatives; suitable combinations may be pursued.',
            'Section 34 (criminal) and section 35 (civil) are compared in the table. A director cannot escape merely by saying the promoters prepared the statements.',
            'Section 36: anyone who knowingly or recklessly makes a false, deceptive or misleading statement, promise or forecast, or deliberately conceals material facts, to induce agreements to acquire or underwrite securities, to profit from their yield or price movements, or to obtain bank credit, is liable under section 447.',
            'Section 37: suits under sections 34–36 may be brought by any person, group or association affected by the misleading prospectus — enabling class actions. A transferee from the original allottee who did not rely on the prospectus cannot sue.'],
          'A prospectus must tell the whole truth — a half-truth that paints a false picture is treated as a lie.',
          'Investors misled in an IPO can join together through an investor association to sue under section 37.',
          blocks=[liab]),
        C('c6', T6, [
            'Section 38: making or abetting an application in a fictitious name, multiple applications in different names or name combinations, or inducing allotment or transfer to a fictitious name, is punishable under section 447. Every prospectus and application form must reproduce this warning prominently. The court may order disgorgement of gains and seizure of securities; proceeds go to the Investor Education and Protection Fund.',
            'Section 447 defines fraud widely: any act, omission, concealment or abuse of position, by any person or with connivance, with intent to deceive, gain undue advantage, or injure the company, shareholders, creditors or others — whether or not any wrongful gain or loss results.',
            'Punishments are graded (table).'],
          'Applying in ghost names to corner an IPO is fraud even if no one can show a direct loss.',
          'Regulators have prosecuted IPO-allotment scams in which thousands of benami demat accounts were used.',
          blocks=[fraud]),
        C('c7', T7, [
            'Allotment is the company\'s acceptance of an application — an appropriation out of unissued capital. Re-issue of forfeited shares is not an allotment.',
            'No allotment unless the minimum subscription stated in the prospectus is subscribed and the application money for it is actually received by cheque or other instrument (SEBI\'s ICDR rules set minimum subscription at 90% of the issue).',
            'Application money must be at least 5% of nominal value or such higher amount as SEBI specifies (SEBI requires at least 25% of issue price; full price in an offer for sale).',
            'If minimum subscription is not received within 30 days of the prospectus (or SEBI\'s period), money is refunded within 15 days of closure; directors and responsible officers are jointly and severally liable with 15% p.a. interest for delay. Refunds go only to the account that paid.',
            'Return of allotment (PAS-3) is filed within 30 days with a list of allottees and, for non-cash consideration, the stamped contract and a registered valuer\'s report. Default: ₹1,000 per day or ₹1 lakh, whichever is less, on the company and officers in default.'],
          'Minimum subscription is the "go/no-go" line — below it the whole issue is called off and money returned.',
          'An allotment made after receiving only 80% of the stated minimum can be refused by the allottee.'),
        C('c8', T8, [
            'Before a public offer, the company applies to one or more recognised stock exchanges for permission to deal, and names them in the prospectus.',
            'Application money is kept in a separate account in a scheduled bank and used only to adjust against allotment once dealing permission is granted, or to repay applicants within SEBI\'s time if allotment cannot be made. Any condition asking applicants to waive these rules is void.',
            'Default: company fined ₹5 lakh to ₹50 lakh; officers in default ₹50,000 to ₹3 lakh.',
            'Commission (s. 40(6), rule 13): must be authorised by the articles; may be paid from issue proceeds, profits or both; capped at the lower of 5% of the issue price of shares (2.5% for debentures) and the rate in the articles; not payable on securities not offered to the public. The prospectus discloses underwriters, rates and amounts, and the number of securities underwritten; the commission contract is filed with the ROC with the prospectus.'],
          'The issue money sits in an escrow-like account until the exchange says the shares can trade.',
          'Merchant bankers\' underwriting fees in Indian IPOs are well within the 5% ceiling.'),
        C('c9', T9, [
            'Section 41: a company may issue depository receipts abroad after a special resolution, as per the GDR rules. Receipts may be issued by public offer, private placement or as prevalent abroad, against new or existing (sponsored) shares; the underlying shares are allotted to the overseas depository bank. Holders become members and can vote only after converting into shares; until then the depository votes as per the agreement.',
            'Private placement (s. 42) is an offer to a select group through a private placement offer-cum-application letter meeting the conditions in the table. An offer to more than 200 persons in a year (per kind of security, excluding QIBs and ESOP employees) is deemed a public offer, attracting sections 23–41, SCRA and SEBI law.',
            'Offers to bodies corporate or nationals of countries sharing a land border with India need prior Government approval under the FEMA non-debt instrument rules, attached to the offer letter.',
            'No fresh private placement until earlier allotments are completed, withdrawn or abandoned (subject to the 200 limit, multiple issues to prescribed classes are allowed).'],
          'Private placement is a by-invitation dinner — named guests, no posters, a strict guest limit, and the bill paid from each guest\'s own account.',
          'Start-ups raising seed money from angels issue PAS-4 letters to each named investor.',
          blocks=[pp]),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Advising on a private placement', 'role': 'Company secretary',
         'situation': 'A private company wants to raise ₹5 crore from 40 angel investors including one from a neighbouring land-border country.',
         'steps': ['Pass a special resolution with the required explanatory statement and file it with the ROC.', 'Obtain Government approval for the land-border investor; issue serially numbered PAS-4 letters; collect money only through banking channels from each investor\'s account.', 'Allot within 60 days and file PAS-3 within 15 days; keep money in a separate account until then.'],
         'takeaway': 'Private placement compliance is detailed and time-bound.'},
        {'id': 'j2', 'title': 'Reviewing an IPO prospectus', 'role': 'Audit firm manager (expert)',
         'situation': 'The firm\'s report is to be included in a prospectus.',
         'steps': ['Confirm independence — no interest in promotion or management.', 'Give written consent and do not withdraw it before filing.', 'Recognise civil liability under section 35 as an expert if the statement misleads.'],
         'takeaway': 'Experts named in a prospectus share liability for misstatements.'},
    ]

    mcqs = [
        Q('m1', 'A private company can issue securities by:', ['Rights issue, bonus issue or private placement', 'Public offer through prospectus', 'Offer for sale to the public', 'Any of these'], 0,
          'Section 23(2) permits private companies to issue by rights or bonus issue and by private placement; public offers through prospectus, including offers for sale, are only for public companies. In practice: a private company must convert to public before an IPO.', 'c1', T1),
        Q('m2', 'Which is NOT a "security" under the SCRA definition adopted by the Companies Act?', ['A unit-linked insurance policy', 'Debentures', 'Units of a mutual fund', 'Government securities'], 0,
          'The SCRA definition expressly excludes unit-linked insurance policies that combine life cover with investment; debentures, mutual fund units and government securities are all included. In practice: ULIPs are regulated by the insurance regulator instead.', 'c1', T1),
        Q('m3', 'Allotted securities are presumed meant for public sale if the public offer is made within:', ['Six months of allotment', 'One year of allotment', 'Thirty days of allotment', 'Ninety days of allotment'], 0,
          'Section 25(2) presumes this intent where the public offer comes less than six months after allotment, or while consideration is still partly unpaid. The document is then a deemed prospectus. In practice: intermediaries reselling shares quickly trigger this rule.', 'c2', T2, 'moderate'),
        Q('m4', 'A document marked "strictly private" sent by a managing director to a single person is:', ['Not an issue to the public (Nash v. Lynde)', 'Always a prospectus', 'A shelf prospectus', 'A deemed prospectus'], 0,
          'A single private communication lacks the publicity needed to be an issue to the public, as held in Nash v. Lynde, so prospectus rules do not apply. Circulating thousands of copies to a section of the public would be different. In practice: label alone does not decide — the reach does.', 'c2', T2),
        Q('m5', 'The copy of a prospectus filed with the Registrar must be signed by:', ['Every person named as director or proposed director, or his authorised attorney', 'A majority of directors', 'The company secretary only', 'The statutory auditor'], 0,
          'Section 26(4) requires signature by every person named in the prospectus as a director or proposed director, or an attorney authorised by him. A majority is not enough. In practice: directors abroad sign through a written authorisation.', 'c3', T3),
        Q('m6', 'A prospectus is valid for issue only if issued within how many days of its filing with the Registrar?', ['90 days', '30 days', '180 days', '1 year'], 0,
          'A prospectus cannot be issued more than ninety days after a copy is delivered to the Registrar; after that a fresh copy must be filed. One year is the maximum validity of a shelf prospectus. In practice: delayed IPOs re-file their prospectus.', 'c3', T3, 'core', check=90),
        Q('m7', 'Variation of objects stated in a prospectus requires:', ['A special resolution and an exit offer to dissenting shareholders', 'An ordinary resolution only', 'A Board resolution only', 'SEBI approval alone'], 0,
          'Section 27 requires a special resolution (through postal ballot) with newspaper publication and justification, and dissenting shareholders must get an exit offer from promoters or controlling shareholders per SEBI rules. Proceeds cannot be used to trade in other listed equity. In practice: investors approve major changes.', 'c3', T3),
        Q('m8', 'A red herring prospectus must be filed with the Registrar at least:', ['Three days before the subscription list opens', 'Thirty days before', 'On the day of opening', 'After the issue closes'], 0,
          'Section 32 requires filing of the red herring prospectus at least three days before the issue opens; after closing, the final prospectus with price and capital raised is filed with the ROC and SEBI. In practice: it is used in book-built issues.', 'c4', T4, 'core'),
        Q('m9', 'Where applicants under a shelf prospectus withdraw after being told of changes, the company must refund:', ['All subscription money within 15 days', 'Money less administrative charges within 15 days', 'Money at the Board\'s discretion', 'Money within 30 days less charges'], 0,
          'The proviso to section 31(2) requires intimation of changes to advance applicants and, if they wish to withdraw, refund of all subscription money within fifteen days. No deductions are allowed. In practice: the information memorandum must flag such changes clearly.', 'c4', T4, 'moderate'),
        Q('m10', 'An abridged prospectus need NOT accompany an application form when:', ['The offer is made only to existing members', 'The issue is a public offer', 'The application is for debentures offered to the public', 'The company is listed'], 0,
          'Section 33 exempts forms issued for underwriting arrangements, for securities not offered to the public, and offers only to existing members. All other public application forms must carry the abridged prospectus. In practice: rights issue forms to members do not need it.', 'c4', T4),
        Q('m11', 'Liability under section 34 for a misleading prospectus:', ['Arises even if no investor suffers loss', 'Requires proof of loss to an investor', 'Applies only to experts', 'Is limited to compensation'], 0,
          'Section 34 is a criminal provision punishing every person who authorises the issue of a misleading prospectus under section 447; loss is not an element. Compensation for loss is under section 35. In practice: regulators can prosecute even before investors claim.', 'c5', T5),
        Q('m12', 'Which is a valid defence for a person under section 35?', ['On learning of the issue he promptly gave reasonable public notice disowning it, as it had gone out without his knowledge', 'He relied on statements prepared by promoters', 'He did not read the prospectus', 'He was a director only for a short time'], 0,
          'Section 35(2) allows defences such as withdrawal of consent, issue without knowledge with prompt public notice, reliance on a competent expert, reasonable belief and copying official documents. Relying on promoters is not a defence. In practice: directors must review the prospectus themselves.', 'c5', T5, 'moderate'),
        Q('m13', 'In Peek v. Gurney, a buyer who bought shares on the stock exchange months later could not sue the directors for deceit because:', ['He did not buy on the basis of the prospectus as an original allottee', 'The prospectus was true', 'Deceit is not a remedy in law', 'The company had been wound up'], 0,
          'Damages for deceit require that the claimant was an original allottee deceived by the prospectus; a later market purchaser did not act on it. The prospectus there was in fact fraudulent. In practice: secondary market buyers rely on other remedies.', 'c5', T5),
        Q('m14', 'Under section 447, fraud involving public interest is punishable with imprisonment of at least:', ['Three years', 'Six months', 'One year', 'Five years'], 0,
          'Where fraud involves public interest, imprisonment is not less than three years, up to ten years, with fine of at least the amount involved up to three times it. Other frauds of ₹10 lakh or more carry a six-month minimum. In practice: public-interest frauds are treated most severely.', 'c6', T6, 'moderate'),
        Q('m15', 'Making multiple applications in different name combinations for IPO shares is punishable under:', ['Section 38 read with section 447', 'Section 33', 'Section 30', 'Section 41'], 0,
          'Section 38 punishes applications in fictitious names or multiple name combinations, and inducing allotment in fictitious names, under section 447; courts can order disgorgement. Section 33 concerns abridged prospectus. In practice: the warning is printed on every application form.', 'c6', T6),
        Q('m16', 'Under section 39, when minimum subscription is not received within 30 days of the prospectus, application money must be refunded within:', ['15 days of the closure of the issue', '30 days', '60 days', '90 days'], 0,
          'Rule 11 requires refund within fifteen days of closure; directors and responsible officers are jointly and severally liable with 15% interest for delay. Refunds go only to the remitting bank account. In practice: refunds are now automated through ASBA unblocking.', 'c7', T7, 'moderate', check=15),
        Q('m17', 'The return of allotment for a public issue must be filed in PAS-3 within:', ['30 days of allotment', '15 days', '60 days', '7 days'], 0,
          'Rule 12 requires PAS-3 within thirty days of allotment for allotments under section 39; for private placement the time is fifteen days. Default attracts ₹1,000 per day or ₹1 lakh, whichever is less. In practice: secretarial teams diarise this deadline.', 'c7', T7, 'core', check=30),
        Q('m18', 'Articles permit underwriting commission of 3%. The maximum commission on shares issued at ₹100 is:', ['₹3 per share', '₹5 per share', '₹2.50 per share', '₹8 per share'], 0,
          'Commission on shares cannot exceed the lower of 5% of the issue price and the rate authorised by the articles; here 3% of ₹100 is ₹3. The ₹2.50 figure would apply to debentures at the 2.5% cap. In practice: Boards cannot exceed the articles.', 'c8', T8, 'moderate', check=3),
        Q('m19', 'Default under section 40 makes the company liable to a fine of:', ['₹5 lakh to ₹50 lakh', '₹50,000 to ₹3 lakh', '₹1,000 per day', '₹10 lakh to ₹1 crore'], 0,
          'The company is fined between five lakh and fifty lakh rupees; officers in default between ₹50,000 and ₹3 lakh. Other ranges relate to different sections. In practice: misuse of the separate issue account is treated seriously.', 'c8', T8),
        Q('m20', 'The maximum number of persons to whom a private placement of one kind of security may be offered in a financial year is:', ['200', '50', '100', '500'], 0,
          'Rule 14(2) caps private placement at two hundred persons per financial year per kind of security, excluding QIBs and ESOP employees; exceeding it makes the issue a deemed public offer. In practice: count offerees, not just allottees.', 'c9', T9, 'core', check=200),
        Q('m21', 'Ruhi and Sohit are offered shares jointly under private placement, Ruhi\'s name first. Subscription money must come from:', ['Ruhi\'s bank account', 'Sohit\'s bank account', 'Either account', 'Cash from both'], 0,
          'For joint holders, payment must come from the bank account of the person named first in the application, and never in cash. The company records the paying account. In practice: this traces the true investor.', 'c9', T9),
        Q('m22', 'If securities under private placement are not allotted within 60 days, the money must be refunded within the next:', ['15 days, failing which 12% p.a. interest from the 60th day', '30 days with 15% interest', '7 days without interest', '60 days with 18% interest'], 0,
          'Section 42(6) requires refund within fifteen days after the sixty days; if not, interest at twelve percent per annum runs from the expiry of the sixtieth day. In practice: allot promptly or return the money in time.', 'c9', T9, 'moderate'),
    ]

    questions = [
        W('q1', 5, 'Distinguish between civil and criminal liability for misstatements in a prospectus.', [liab],
          [S('s1', 'Persons liable under each', 1.5, 'concept', 'authoris', 'promoter|expert|director'),
           S('s2', 'Consequence — s. 447 vs compensation', 1.5, 'concept', '447', 'compensation'),
           S('s3', 'Loss — not needed vs needed', 1, 'concept', 'loss'),
           S('s4', 'Defences', 1, 'concept', 'immaterial|reasonable|consent|notice|expert')],
          ['A comparison table with defences scores well.'], ['Mixing up section numbers 34 and 35.'], ['Use a table.'], pad='table'),
        W('q2', 4, 'Raksha Instruments Ltd. received 80% of the minimum subscription stated in its prospectus, withdrew part of the money for asset purchase and then allotted shares. Rashmi refuses her allotment. Advise.',
          [legal('Section 39(1) and (3), and section 40(3)',
                 'Only 80% of the stated minimum subscription received; money partly used before allotment; shares allotted.',
                 'No allotment can be made unless the full minimum subscription is subscribed and received. If it is not received within 30 days, application money must be refunded (within 15 days of closure). Application money must stay in a separate bank account and cannot be used for other purposes before allotment.',
                 'The allotment is invalid and Rashmi may refuse it and claim refund; the company and officers face penalties for using the money.')],
          [S('s1', 'Minimum subscription rule', 1.5, 'concept', 'minimum subscription'),
           S('s2', 'Refund obligation', 1, 'application', 'refund|return'),
           S('s3', 'Separate account / misuse', 0.5, 'application', 'separate|account|utilis|withdr'),
           S('s4', 'Conclusion — Rashmi can refuse', 1, 'conclusion', 'refuse|invalid|void|not valid')],
          ['State the rule, apply, conclude.'], ['Thinking 80% is enough.'], ['Provision → facts → analysis → conclusion.']),
        W('q3', 5, 'State the key conditions for an issue of securities by private placement under section 42.', [pp],
          [S('s1', '200-person limit and deemed public offer', 1, 'concept', '200'),
           S('s2', 'Special resolution and PAS-4', 1, 'concept', 'special resolution|pas-4|pas 4'),
           S('s3', 'Payment through bank, no cash', 1, 'concept', 'bank|cash'),
           S('s4', 'Allotment in 60 days / refund / interest', 1, 'concept', '60'),
           S('s5', 'PAS-3 in 15 days; no advertisement', 1, 'concept', 'pas-3|pas 3|return of allotment|advert')],
          ['Cover numbers precisely.'], ['Saying private placement can be advertised.'], ['Use a table or numbered list.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is a deemed prospectus?',
          'When a company allots securities intending that they be offered for sale to the public, the document used to offer them is treated as a prospectus; the intention is presumed if they are offered within six months of allotment or before full consideration is received.',
          [P('p1', 'Offer document for securities allotted for public sale', 5, 'offer', 'public'), P('p2', 'Six months / full consideration presumption', 5, 'six months|6 months|consideration')], 'c2'),
        V('v2', 'What is a red herring prospectus?',
          'A prospectus that does not give complete particulars of the price or quantity of securities, filed with the Registrar at least three days before the issue opens and used in book building.',
          [P('p1', 'Incomplete price or quantity', 5, 'price|quantity|quantum'), P('p2', 'Filed three days before opening', 3, 'three days|3 days'), P('p3', 'Book building', 2, 'book')], 'c4'),
        V('v3', 'Who is liable to pay compensation under section 35?',
          'The company and every director at the time of issue, every person named as a director with consent, every promoter, every person who authorised the issue and every expert whose statement is included.',
          [P('p1', 'Company and directors', 3, 'company|director'), P('p2', 'Promoters', 2, 'promoter'), P('p3', 'Persons authorising issue', 2, 'authoris'), P('p4', 'Experts', 3, 'expert')], 'c5'),
        V('v4', 'What is the maximum underwriting commission on shares and debentures?',
          'For shares, five percent of the issue price or the rate in the articles, whichever is lower; for debentures, two and a half percent or the articles rate, whichever is lower.',
          [P('p1', 'Shares 5%', 4, '5%|five percent|five per cent|5 percent'), P('p2', 'Debentures 2.5%', 4, '2.5|two and a half'), P('p3', 'Or articles rate, if lower', 2, 'article')], 'c8'),
        V('v5', 'Within what time must private placement securities be allotted and the return filed?',
          'Allotment within sixty days of receiving the application money, and the return of allotment in PAS-3 within fifteen days of allotment.',
          [P('p1', 'Allot within 60 days', 5, '60|sixty'), P('p2', 'PAS-3 within 15 days', 5, '15|fifteen')], 'c9'),
    ]

    cases = [{'id': 'k1', 'title': 'The Vardhan Foods IPO', 'difficulty': 'moderate',
              'case': 'Vardhan Foods Ltd. files a red herring prospectus two days before its IPO opens. Its statutory auditor, whose report is included, has given written consent. The final prospectus shows a dividend record but hides that dividends came from selling land. Ajay, an original allottee, lost money; Bina bought the shares on the exchange a month later. Some applicants used several name combinations to get more shares.',
              'mcqs': [
                  M('k1a', 'Filing the red herring prospectus two days before opening is:', ['A contravention — it must be filed at least three days before', 'Valid', 'Valid if SEBI is informed', 'Required only for FPOs'], 0,
                    'Section 32 requires the red herring prospectus to be filed with the Registrar at least three days before the subscription list opens; two days is too late. In practice: issue calendars build in this gap.', 'core', topic=T4),
                  M('k1b', 'Hiding that dividends came from sale of land makes the prospectus:', ['Misleading by omission, attracting sections 34 and 35', 'Accurate, since each statement was literally true', 'A shelf prospectus', 'Exempt as historical information'], 0,
                    'A statement is untrue if its form or context misleads or if an omission is likely to mislead; concealing the source of dividends gives a false impression of trading profits. Literal truth does not save it. In practice: Rex v. Kylsant illustrates this.', 'moderate', topic=T5),
                  M('k1c', 'Who can sue under section 37 for the misleading prospectus?', ['Ajay, the original allottee, but not Bina who bought later on the exchange', 'Both Ajay and Bina', 'Only Bina', 'Neither'], 0,
                    'Section 37 allows persons affected by the misleading prospectus to sue; Bina bought in the market without relying on the prospectus, like the claimant in Peek v. Gurney. In practice: investor associations can bring class actions for original allottees.', 'moderate', topic=T5),
                  M('k1d', 'Applicants who used several name combinations are liable under:', ['Section 38, punishable under section 447', 'Section 33 penalty of ₹50,000', 'No provision', 'Section 42'], 0,
                    'Making multiple applications in different combinations of names to obtain securities is personation under section 38, punishable under section 447 with possible disgorgement. In practice: depositories and registrars screen PAN-linked duplicate applications before allotment to catch such abuse.', 'core', topic=T6),
              ]}]

    return unit(UID, 'p2', 'int-p2-ch03', 1, 'Prospectus and Allotment of Securities',
                ['Identify modes of issue for public and private companies and the meaning of securities.',
                 'Explain prospectus, deemed, shelf, red herring and abridged prospectus and their requirements.',
                 'Apply civil and criminal liability provisions for misstatements and fraud.',
                 'Apply rules on allotment, minimum subscription, stock exchange dealing and commission.',
                 'Explain GDRs and private placement rules with time limits and penalties.'],
                {'difficulty': 'core', 'minutes': {'learn': 55, 'practice': 35}, 'prereq': ['int-p2-ch02-u01'],
                 'exam_tip': 'Numbers are tested heavily: 6 months (deemed prospectus), 90 days (validity), 3 days (RHP), 15/30 days (refund, PAS-3), 5%/2.5% commission, 200 persons, 60 days.'},
                concepts, [i1], jobs, mcqs, questions,
                {'summary': ['Public company: public offer, private placement, rights/bonus; private company: no public offer.',
                             'Deemed prospectus: public offer within 6 months of allotment or before full consideration.', 'Prospectus valid 90 days from filing; signed by all named directors.',
                             'Shelf valid ≤ 1 year; RHP filed ≥ 3 days before opening; abridged prospectus with every form.',
                             's.34 criminal (no loss needed) vs s.35 civil compensation; s.36 inducement; s.37 class action.',
                             'Minimum subscription before allotment; refund within 15 days of closure; PAS-3 in 30 days.',
                             'Commission ≤ 5% shares / 2.5% debentures or articles rate if lower.', 'Private placement: ≤ 200 persons, PAS-4, bank payment, allot in 60 days, PAS-3 in 15 days.'],
                 'remember': ['Fraud needs no wrongful gain or loss (s. 447).', 'Market buyers cannot rescind (Peek v. Gurney).'],
                 'traps': ['PAS-3: 30 days (public) vs 15 days (private placement).', 'Refund interest: 15% (s. 39 default) vs 12% (s. 42).']},
                [('Prospectus validity', '90 days from filing'), ('RHP filing', '≥ 3 days before opening'), ('Shelf validity', '≤ 1 year'), ('Commission cap', '5% shares · 2.5% debentures'),
                 ('Private placement', '≤ 200 persons / year'), ('PAS-3', '30 days (s.39) · 15 days (s.42)')],
                viva, cases,
                topics=['Introduction', 'Public Offer and Private Placement', 'Regulation of Issue and Transfer of Securities', 'Prospectus', 'Mis-statements in Prospectus',
                        'Punishment for Fraudulently Inducing Persons to Invest Money', 'Action by Affected Persons', 'Punishment for Personation', 'Punishment for Fraud',
                        'Allotment of Securities by Company', 'Securities to be Dealt with in Stock Exchanges', 'Global Depository Receipt', 'Private Placement'])
