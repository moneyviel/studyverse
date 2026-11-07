"""CA Foundation · Paper 2 Business Laws · Chapter 2 The Indian Contract Act, 1872 · Unit 9 Agency.
Original explanations and problems; Sections 182-238 cited by number. Agent's retainer, remuneration and secret-profit figures are computed."""
from lib import *
from ca_viva import V, P, ALT
from ca_cases import M

UID = 'fnd-p2-ch02-u09'


def Q(qid, marks, diff, pad, q, model, scheme, remarks, mistakes, tips, checks=None):
    d = {'id': qid, 'marks': marks, 'minutes': minutes(marks), 'difficulty': diff, 'pad': pad, 'q': q, 'model': model,
         'scheme': [{'id': f's{i+1}', 'pt': pt, 'm': m, 'skill': sk} for i, (pt, m, sk) in enumerate(scheme)],
         'remarks': remarks, 'mistakes': mistakes, 'tips': tips}
    if checks: d['checks'] = checks
    return d


def MC(mid, q, options, answer, explain, concept, diff='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': diff}
    if check: d['check'] = check
    return d


def build():
    # ---------- Illustration 3: agent's account, retainer and remittance (Sections 213, 217, 218, 219) ----------
    c3 = Checks()
    sales = c3.add('320*1500', 'sale proceeds: 320 cartons at ₹1,500')
    comm = c3.add('480000*5/100', 'commission at 5% of sales')
    exp = c3.add('7200+4800', 'freight and godown rent paid by the agent for the principal')
    remit = c3.add('480000-24000-12000', 'amount to be remitted to the principal')
    t3 = table(['Particulars', '₹'], [
        ['Sale proceeds received (320 cartons × ₹1,500)', sales],
        ['Less: commission at 5% (Section 219)', -comm],
        ['Less: freight paid for the principal (Section 217)', -7200],
        ['Less: godown rent paid for the principal (Section 217)', -4800],
        ['Balance payable to Prakash (Section 218)', remit],
    ], num=[1], title='Account rendered by the agent (Section 213)')

    # ---------- Illustration 4: agent dealing on his own account (Sections 215, 216) ----------
    c4 = Checks()
    profit = c4.add('1150000-950000', 'profit made by the agent on resale')

    # ---------- MCQ / case numbers ----------
    cm = Checks()
    m_ret = cm.add('600000-600000*3/100-9000', 'amount payable to principal after 3% commission and ₹9,000 expenses')
    kc = Checks()
    k_comm = kc.add('2400000*2/100', 'commission at 2% on ₹24,00,000')
    k_net = kc.add('2400000-48000-15000', 'net amount payable to the principal')

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p2', 'chapter': 'fnd-p2-ch02', 'n': 9, 'title': 'Agency',
        'outcomes': ['Define agent and principal (Section 182), state who may appoint and who may be an agent, and explain the modes of creating an agency, including ratification and estoppel.',
                     'Explain the extent of an agent\'s authority in normal situations and emergencies, and distinguish a sub-agent from a substituted agent.',
                     'State the duties and rights of an agent and compute amounts an agent may retain or must account for.',
                     'Explain the principal\'s liability to third parties, the cases where an agent is personally liable, and the modes and effects of termination of agency, including irrevocable agency.'],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 55, 'practice': 50}, 'prereq': ['fnd-p2-ch02-u08'],
                 'exam_tip': 'Frequent problems: minor as agent (Section 184), ratification (Sections 196–200), emergency authority (Section 189), agent dealing on own account (Sections 215–216), sub-agent liability (Sections 192–193), personal liability of agent (Section 230) and irrevocable agency (Section 202).'},
        'concepts': [
            {'id': 'c1', 'title': 'Agent and principal (Sections 182–185)',
             'body': ['Section 182: an agent is someone engaged to act for another, or to stand in for him in dealings with outsiders; the person for whom the act is done, or who is represented, is the principal. The Act does not define "agency" itself. The test is whether the person can bind the principal and create privity of contract between the principal and third parties. The idea: he who acts through another acts himself.',
                      'Section 183: anyone who is a major under the law applicable to him and of sound mind may employ an agent — so minors and persons of unsound mind are unable to have agents of their own.',
                      'Section 184: as between the principal and third persons, anyone may become an agent — even a minor or a person of unsound mind — and the principal is bound by his acts. But such an agent is not responsible to the principal for his conduct, so the principal has no remedy against him.',
                      'Section 185: no consideration is needed to create an agency.'],
             'analogy': 'An agent is the principal\'s extended arm: what the arm signs, the body is bound by.',
             'work': 'Companies act only through agents — directors, managers, sales staff. Before relying on a document, a CA checks that the signatory had authority to bind the company.'},
            {'id': 'c2', 'title': 'Creation of agency',
             'body': ['Express agency: authority given by spoken or written words, e.g. a power of attorney (Sections 186–187).',
                      'Implied agency: authority inferred from the circumstances, conduct or the ordinary course of dealing (Section 187). Two important forms: (a) agency by estoppel (Section 237) — if the principal\'s words or conduct lead a third person to believe that someone is his agent and the third person acts on that belief, the principal cannot later deny the agency; (b) agency of necessity — in an emergency, a person already in charge of another\'s goods may act to save them (for example, a caretaker spends money to put out a fire on the owner\'s farm).',
                      'Agency by operation of law: the law itself treats one person as another\'s agent — for instance, every partner is the agent of the firm for the business of the firm.',
                      'Agency by ratification (Sections 196–200): a person may adopt an act done on his behalf without authority; once ratified, it is as if authorised from the start.'],
             'analogy': 'Agency can be born from a signed letter, from silence that misleads, from a crisis, or from a later "yes, I approve".',
             'work': 'Where an employee has habitually placed orders with a supplier and the company has always paid, the company may be bound by estoppel even after it secretly withdrew the employee\'s authority — a common issue CAs see in disputed payables.'},
            {'id': 'c3', 'title': 'Ratification (Sections 196–200)',
             'body': ['If someone acts for another without authority, the other may ratify or disown the act (Section 196). Ratification may be express or implied from conduct — for example, accepting interest on money lent without authority (Section 197).',
                      'Conditions: (1) the act must have been done on behalf of the principal, not for the actor himself; (2) the principal must have existed and been competent both when the act was done and when he ratifies; (3) the principal must have full knowledge of the material facts (Section 198); (4) the whole transaction must be ratified, not just the favourable part (Section 199); (5) ratification cannot subject a third person to damages or end his rights or interests (Section 200); (6) it must be made within a reasonable time and communicated; and (7) the act must be one the principal could lawfully have done — a void or illegal act (e.g. forgery) cannot be ratified.',
                      'Effect: ratification relates back to the date of the act — the contract binds as if made with authority.'],
             'analogy': 'Ratification is signing a photograph after it is taken: it becomes your picture from the moment the shutter clicked — but you cannot sign only half the photo.',
             'work': 'Board meetings often "ratify" purchases made by an executive beyond his limit. A CA checks that the board was told all material facts; otherwise the ratification may not bind.'},
            {'id': 'c4', 'title': 'Extent of authority (Sections 188, 189)',
             'body': ['Section 188: authority to do an act carries with it authority for every lawful step needed to get it done; authority to run a business covers every lawful step needed for it or customarily taken in running such a business.',
                      'Section 189: in an emergency, an agent may do all acts to protect his principal from loss that a person of ordinary prudence would do in his own case in similar circumstances. Conditions: the agent could not communicate with the principal; there was a real necessity; he acted in good faith; and he acted as a prudent person would in his own case.'],
             'analogy': 'Authority to build a house includes authority to buy the bricks; and if a flood hits the site, the site manager may move the cement to safety without phoning the owner.',
             'work': 'Transporters and clearing agents often face emergencies — spoiling perishables, port delays. A CA checks whether expenses claimed under emergency authority meet the Section 189 test.'},
            {'id': 'c5', 'title': 'Sub-agents and substituted agents (Sections 190–195)',
             'body': ['Section 190: an agent cannot ordinarily delegate — the principal chose him personally. Delegation is allowed where the custom of trade permits it or the nature of the agency requires it.',
                      'Sub-agent (Section 191): someone engaged by the original agent who works under that agent\'s directions. If properly appointed (Section 192), the principal is bound by his acts as if he were an original agent; the agent is responsible to the principal for the sub-agent\'s acts; the sub-agent is responsible to the agent, and to the principal only for fraud or wilful wrong. If improperly appointed (Section 193), the principal is not bound; the agent is responsible for the sub-agent\'s acts to both principal and third persons.',
                      'Substituted agent (Sections 194–195): a person whom the agent, having express or implied authority, names to act for the principal. He is the principal\'s own agent for that part of the business; privity of contract exists between him and the principal. The original agent is not responsible for him, provided he used the discretion of a man of ordinary prudence in selecting him.'],
             'analogy': 'A sub-agent is the agent\'s assistant; a substituted agent is a new agent introduced to the principal and then left to report to him directly.',
             'work': 'A CA firm engaged for an audit cannot outsource the engagement to another firm without the client\'s consent; where component auditors are appointed, engagement letters spell out whether they act under the principal auditor or report directly to the client.'},
            {'id': 'c6', 'title': 'Duties of an agent (Sections 211–218)',
             'body': ['Follow instructions or, absent instructions, the custom of the business — and make good any loss from not doing so (Section 211). Act with reasonable skill and diligence and compensate for direct consequences of negligence or misconduct (Section 212). Render proper accounts on demand (Section 213). In difficulty, use reasonable diligence to communicate with the principal and seek instructions (Section 214).',
                      'Not deal on his own account without the principal\'s consent: if he does so without disclosing all material facts, the principal may repudiate the transaction (Section 215) or claim from the agent any benefit he made (Section 216).',
                      'Not make secret profits; not delegate (Section 190); pay to the principal all sums received on his account, after the deductions he is entitled to (Section 218); and not misuse confidential information gained in the agency.'],
             'analogy': 'An agent is a trusted steward: obey, be careful, keep accounts, ask when unsure, never feather your own nest, and hand over what belongs to the master.',
             'work': 'Commission agents, C&F agents and stockbrokers all owe these duties. Forensic accountants often trace undisclosed "own-account" deals by agents and quantify the profit recoverable under Section 216.'},
            {'id': 'c7', 'title': 'Rights of an agent (Sections 217–225)',
             'body': ['Retainer (Section 217): from money received for the principal, the agent may keep what is due to him for advances, expenses properly incurred and remuneration.',
                      'Remuneration (Section 219): payable only when the act is completed, unless otherwise agreed; an agent guilty of misconduct in the business is not entitled to remuneration for that part of the business (Section 220).',
                      'Lien (Section 221): unless otherwise agreed, the agent may retain the principal\'s goods, papers and other property received by him until his commission, disbursements and services are paid or accounted for. The lien is lost if possession is lost, or waived.',
                      'Indemnity: for the consequences of all lawful acts done in exercise of his authority (Section 222); for acts done in good faith that cause injury to third persons (Section 223) — but not for criminal acts (Section 224); and compensation for injury caused by the principal\'s neglect or want of skill (Section 225).'],
             'blocks': [t3],
             'analogy': 'The agent is allowed to take his fee and costs out of the money he collects — like a waiter keeping the agreed tip from the bill he collects for the restaurant.',
             'work': 'In consignment accounting, the account sales prepared by the agent shows exactly these deductions — commission, expenses — before remitting the balance. CAs reconcile account sales with the consignor\'s books.'},
            {'id': 'c8', 'title': 'Principal\'s liability to third parties (Sections 226–229, 237–238)',
             'body': ['Section 226: contracts made and acts done by an agent within his authority bind the principal as if done by him personally.',
                      'Agent exceeding authority: if the authorised part can be separated from the unauthorised part, the principal is bound only by the authorised part (Section 227); if it cannot be separated, the principal need not recognise the transaction (Section 228). But where the principal has led third persons to believe the acts were within authority, he is bound (Section 237).',
                      'Notice to the agent, given in the course of the business, is notice to the principal (Section 229). The principal is liable for fraud, misrepresentation or wrongs committed by the agent in the course of his business, as if he had done them himself (Section 238).'],
             'analogy': 'The principal answers for his agent\'s work like an owner answers for his shop counter — even for mistakes made behind it during business hours.',
             'work': 'Misselling by a company\'s sales agents creates liability for the company. Auditors assess such claims for provisions and contingent-liability disclosure.'},
            {'id': 'c9', 'title': 'Personal liability of the agent (Sections 230–235)',
             'body': ['Section 230: unless otherwise agreed, an agent cannot personally enforce contracts made for his principal, nor is he personally bound by them. The agent is presumed to be personally liable where: (1) he buys or sells goods for a merchant who lives outside India; (2) he does not disclose the name of the principal; (3) the principal, though disclosed, cannot be sued (e.g. a minor) — unless the third party knew; (4) he is a pretended agent and the principal disowns the act (Section 235); (5) he exceeds his authority, misleading the third party (breach of warranty of authority).',
                      'Undisclosed principal (Section 231): if the other party did not know he was dealing with an agent, the principal may enforce the contract but takes it subject to the defences available against the agent; if the principal reveals himself before completion, the other party may refuse to go on if he can show he would not have contracted with him. Section 233: where the agent is personally liable, the third party may hold either the agent or the principal, or both, liable. Section 234: if the third party, knowing the facts, makes the agent alone (or the principal alone) liable, he cannot later turn to the other.'],
             'analogy': 'Normally the agent is only a messenger; but if he hides the sender, pretends to be a messenger, or sends a parcel for a sender who cannot be traced, he must answer himself.',
             'work': 'Import agents often sign purchase contracts for foreign principals. A CA advising such an agent warns that, under Section 230, he may be personally liable unless the contract clearly excludes it.'},
            {'id': 'c10', 'title': 'Termination of agency (Sections 201–210)',
             'body': ['Modes (Section 201): revocation by the principal; renunciation by the agent; completion of the business; death or unsoundness of mind of either party; insolvency of the principal; expiry of the agreed term. (Dissolution of a firm or winding up of a company that is principal has the same effect.)',
                      'Irrevocable agency (Section 202): if the agent has his own stake in the very property the agency deals with, the agency cannot (unless the contract expressly says so) be brought to an end so as to harm that stake — not even by the principal\'s death or insanity. Example: authority to sell land and repay oneself a debt from the proceeds.',
                      'The principal may revoke at any time until the agent has used the authority in a way that binds the principal (Section 203), but not as regards acts and obligations already arising from acts done (Section 204). Premature revocation or renunciation of a fixed-term agency without sufficient cause requires compensation (Section 205); reasonable notice must be given (Section 206). Revocation may be express or implied (Section 207).',
                      'Effect (Section 208): termination takes effect against the agent when it becomes known to him, and against third persons when it becomes known to them. On the principal\'s death or insanity, the agent must still take reasonable steps to protect the principal\'s interests (Section 209). Termination of the agent\'s authority ends a sub-agent\'s authority too (Section 210).'],
             'analogy': 'Ending an agency is like switching off a light that others are still seeing by: it goes dark for the agent when he is told, and for outsiders when they are told.',
             'work': 'When a company removes an authorised signatory, the CA advises it to inform banks and major suppliers at once — until they are told, Section 208 may still bind the company to the old signatory\'s acts.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'A minor as agent', 'difficulty': 'core', 'minutes': 6,
             'q': 'Ojas appoints Pihu, aged 16, to sell his motorbike for not less than ₹90,000. Pihu sells it to Rahul for ₹75,000. (a) Is Ojas bound by the sale? (b) Can Ojas recover the ₹15,000 shortfall from Pihu?',
             'solution': [legal('Section 184: as between the principal and third persons, any person may become an agent, but a minor agent is not responsible to the principal. Section 183: the principal must be a major of sound mind — here he is.',
                                'Ojas (major) appointed Pihu (minor). She sold for ₹75,000 against an instruction of a minimum of ₹90,000.',
                                'The sale was made by an agent within the kind of act she was appointed to do, so Ojas is bound as against Rahul. Because Pihu is a minor, she cannot be held responsible to Ojas for disobeying instructions.',
                                '(a) Ojas is bound by the sale to Rahul. (b) Ojas cannot recover the ₹15,000 shortfall from Pihu.')],
             'checks': [{'expr': '90000-75000', 'value': 15000, 'label': 'shortfall against instructions'}]},
            {'id': 'i2', 'title': 'Perishables in a strike — emergency authority', 'difficulty': 'moderate', 'minutes': 7,
             'q': 'Sumit, a transporter, is carrying 8 tonnes of grapes from Nashik to Delhi for Tanvi. A sudden transport strike blocks the highway for several days. Sumit tries to call Tanvi, but she is on a flight abroad and unreachable. The grapes start rotting, so Sumit sells them in the nearest market at the best price available. Tanvi sues Sumit for selling without authority. Decide.',
             'solution': [legal('Section 189: when an emergency arises, an agent may do whatever is needed to shield the principal from loss that a person of ordinary prudence would do in his own case under similar circumstances. The agent should be unable to communicate with the principal, there must be real necessity, and he must act in good faith.',
                                'The grapes were perishable and began rotting because of an unforeseen strike. Sumit tried but failed to reach Tanvi, and sold at the best available price.',
                                'All conditions are met: genuine emergency, perishable goods, failed attempt to communicate, and a sale that a prudent owner would make to cut losses. Sumit acted as an agent of necessity.',
                                'Sumit is not liable. Tanvi is bound by the sale and is entitled to the sale proceeds (less proper expenses).')]},
            {'id': 'i3', 'title': 'Agent\'s account: what can he retain?', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'Prakash appoints Qamar as his selling agent at a commission of 5% on sales. Qamar sells 320 cartons of detergent at ₹1,500 each and receives the money. He paid ₹7,200 freight and ₹4,800 godown rent on Prakash\'s behalf. Prepare the account Qamar should render and state the amount payable to Prakash.',
             'solution': [legal('Section 213: the agent must render proper accounts. Section 217: he may retain, out of sums received for the principal, all moneys due to him for advances, expenses properly incurred and remuneration. Section 218: he must pay the balance to the principal. Section 219: remuneration is due on completion of the act.',
                                f'Sales {R(sales)}; commission 5% = {R(comm)}; expenses paid {R(exp)}.',
                                f'Qamar may deduct his commission and the expenses properly incurred for Prakash before remitting. {R(sales)} − {R(comm)} − {R(exp)} = {R(remit)}.',
                                f'Qamar must pay {R(remit)} to Prakash, with the account below.'),
                          t3],
             'checks': c3},
            {'id': 'i4', 'title': 'Agent buys the principal\'s property himself', 'difficulty': 'hard', 'minutes': 8,
             'q': 'Usha engages Vinod to sell her flat. Vinod tells her the best offer is ₹9,50,000 and, without disclosing that the "buyer" is his own brother-in-law acting for him, gets her to agree. Two months later Vinod resells the flat for ₹11,50,000. What are Usha\'s rights?',
             'solution': [legal('Section 215: if an agent deals on his own account without the principal\'s consent and without disclosing all material facts, the principal may repudiate the transaction if the agent dishonestly concealed facts or the dealing was disadvantageous to him. Section 216: if an agent, without the principal\'s knowledge, deals on his own account, the principal may claim from him any benefit resulting from the transaction.',
                                f'Vinod bought the flat for himself through a relative at ₹9,50,000, concealing this, and resold it for ₹11,50,000 — a gain of {R(profit)}.',
                                'Vinod dealt on his own account without disclosure. Since the flat has been resold to a third party, repudiation is no longer practical; but Usha can recover the benefit Vinod made.',
                                f'Usha can claim {R(profit)} from Vinod under Section 216 (she could have repudiated the sale under Section 215 had the flat not been resold). Vinod also forfeits any commission for this misconduct (Section 220).')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Removing an authorised signatory', 'role': 'CA in industry (company secretary-cum-finance head)', 'situation': 'Your company\'s purchase manager has resigned. He was authorised to place orders up to ₹10 lakh with approved vendors.',
             'steps': ['Pass an internal approval revoking his authority from the date of leaving.', 'Write to all approved vendors and banks informing them — under Section 208 termination is effective against third parties only when they come to know of it.',
                       'Collect his purchase order book, digital signature tokens and system access.', 'Review orders placed in his last week and confirm them or cancel promptly.'],
             'takeaway': 'Authority ends inside the company on a date; outside the company it ends only when third parties are told.', 'think': 'If a vendor who was never informed accepts an order from him a week after he leaves, is the company bound?',
             'answer': 'Very likely yes — the vendor did not know of the termination (Section 208), and the company had held him out as its agent (Section 237).'},
            {'id': 'j2', 'title': 'Commission agent\'s account sales', 'role': 'Audit assistant at a consignor', 'situation': 'The client\'s agent in Kolkata remitted ₹38 lakh against sales of ₹42 lakh, deducting commission ₹2.1 lakh and "miscellaneous expenses" ₹1.9 lakh.',
             'steps': ['Check the commission rate in the agency agreement (5% of ₹42 lakh = ₹2.1 lakh — agrees).', 'Ask for supporting bills for the miscellaneous expenses: only expenses properly incurred for the principal can be retained (Section 217).',
                       'Disallow and recover any unsupported amount; it is a sum received on the principal\'s account that must be paid over (Section 218).', 'Recommend periodic accounts from the agent (Section 213).'],
             'takeaway': 'An agent may deduct only what the law and the contract allow — everything else belongs to the principal.', 'think': 'If ₹60,000 of the expenses is unsupported, how much more should the agent remit?',
             'answer': '₹60,000, raising the remittance to ₹38.6 lakh.',
             'checks': [{'expr': '4200000*5/100', 'value': 210000, 'label': 'commission at 5%'}, {'expr': '4200000-210000-190000', 'value': 3800000, 'label': 'remittance as made'}, {'expr': '3800000+60000', 'value': 3860000, 'label': 'remittance after disallowing ₹60,000'}]},
            {'id': 'j3', 'title': 'Agent for a foreign supplier', 'role': 'CA advising an Indian trading company', 'situation': 'Your client signs contracts with Indian buyers for the sale of machines manufactured by a German company, signing "for and on behalf of" the German principal.',
             'steps': ['Explain Section 230: an agent selling goods for a merchant resident abroad is presumed to be personally liable unless the contract shows otherwise.', 'Recommend an express clause in each buyer contract excluding the agent\'s personal liability.',
                       'Ensure the agency agreement with the German company gives the client an indemnity (Section 222) for claims arising from authorised acts.', 'Disclose any guarantees or performance obligations in the client\'s financial statements.'],
             'takeaway': 'With foreign principals, the agent is presumed to be on the hook — draft around it.', 'think': 'Would the presumption apply if the principal were a company in Mumbai?',
             'answer': 'No. For a disclosed principal resident in India, the general rule applies — the agent is not personally liable unless he agreed to be.'},
        ],
        'mcqs': [
            MC('m1', 'Under Section 182, someone engaged to act for another person, or to stand in for him when dealing with outsiders, is called:', ['An agent', 'A bailee', 'A surety', 'A partner only'], 0, 'Section 182 defines agent and principal.', 'c1'),
            MC('m2', 'Who may employ an agent under Section 183?', ['A major of sound mind', 'Any person including a minor', 'Only a company', 'Only a registered trader'], 0, 'The principal must be competent; a minor cannot appoint an agent.', 'c1'),
            MC('m3', 'A minor appointed as an agent:', ['Can bind the principal to third parties but is not liable to the principal', 'Cannot act as an agent at all', 'Is personally liable to the principal for negligence', 'Makes every contract void'], 0, 'Section 184.', 'c1', 'moderate'),
            MC('m4', 'Consideration for creating an agency is:', ['Not necessary', 'Essential', 'Necessary only for written agencies', 'Necessary only for sub-agents'], 0, 'Section 185.', 'c1'),
            MC('m5', 'Which of the following CANNOT be ratified?', ['An act that is void, such as a forged signature', 'A purchase made on the principal\'s behalf without authority', 'A loan of the principal\'s money made without authority', 'A sale made on the principal\'s behalf without authority'], 0, 'Ratification cannot validate a void or illegal act.', 'c3', 'moderate'),
            MC('m6', 'The principal accepts the beneficial part of an unauthorised transaction but rejects the rest. Under Section 199:', ['He is taken to have ratified the whole transaction', 'He has ratified only the beneficial part', 'There is no ratification at all', 'The transaction is void'], 0, 'Ratifying part of a transaction amounts to ratifying the whole.', 'c3', 'moderate'),
            MC('m7', 'In an emergency, an agent may act to protect his principal from loss as:', ['A person of ordinary prudence would in his own case (Section 189)', 'The principal expressly instructed', 'The third party demands', 'The agent personally prefers'], 0, 'Section 189.', 'c4'),
            MC('m8', 'A person engaged by the original agent and working under that agent\'s directions is called:', ['A sub-agent', 'A substituted agent', 'A co-agent', 'A mercantile agent'], 0, 'Section 191.', 'c5'),
            MC('m9', 'Privity of contract exists between the principal and:', ['A substituted agent', 'A properly appointed sub-agent', 'An improperly appointed sub-agent', 'No one except the original agent'], 0, 'A substituted agent is the principal\'s own agent (Section 194). A sub-agent is responsible to the agent.', 'c5', 'moderate'),
            MC('m10', 'An agent sells to himself the principal\'s goods without disclosure, and the deal is disadvantageous to the principal. The principal may:', ['Repudiate the transaction or claim the agent\'s benefit', 'Only claim the agreed commission', 'Do nothing as the goods are sold', 'Sue the buyer only'], 0, 'Sections 215 and 216.', 'c6'),
            MC('m11', 'An agent sells goods for ₹6,00,000 at 3% commission and has paid ₹9,000 expenses for the principal. How much must he pay over?', [R(m_ret), '₹5,82,000', '₹5,91,000', '₹6,00,000'], 0, f'₹6,00,000 − commission ₹18,000 − expenses ₹9,000 = {R(m_ret)} (Sections 217–218).', 'c7', 'moderate', '600000-600000*3/100-9000'),
            MC('m12', 'An agent is NOT entitled to indemnity from the principal for:', ['A criminal act done at the principal\'s request', 'Lawful acts done in exercise of authority', 'Acts done in good faith that injure third persons', 'Expenses properly incurred in the agency'], 0, 'Section 224 — no indemnity for criminal acts, even if employed to do them.', 'c7'),
            MC('m13', 'An agent is presumed to be personally liable when he contracts on behalf of:', ['A merchant resident abroad', 'A disclosed principal resident in India', 'A company registered in India', 'His employer within authority'], 0, 'Section 230, exception (1).', 'c9'),
            MC('m14', 'Kavi owes Lal ₹3,00,000 and authorises Lal to sell Kavi\'s plot and recover the debt from the sale price. Kavi dies before the sale. The agency:', ['Is not terminated — agency coupled with interest (Section 202)', 'Terminates on Kavi\'s death', 'Becomes voidable by Kavi\'s heirs', 'Becomes a substituted agency'], 0, 'Where the agent has an interest in the subject matter, the agency cannot be terminated to the prejudice of that interest.', 'c10', 'moderate'),
            MC('m15', 'As regards third persons, termination of an agent\'s authority takes effect:', ['When it becomes known to them', 'From the date of the principal\'s decision', 'Only after 30 days', 'When the agent returns the papers'], 0, 'Section 208.', 'c10'),
            MC('m16', 'On which person\'s insolvency is an agency terminated under Section 201?', ['The principal', 'The agent', 'The sub-agent', 'The third party'], 0, 'Section 201 lists the principal being adjudicated insolvent.', 'c10'),
        ],
        'questions': [
            Q('q1', 4, 'moderate', 'legal',
              'Wasim, without any authority, buys 50 sacks of sugar from Xavier "on behalf of Yusuf". Yusuf, on learning of it, sells 20 sacks to his own customers at a profit, but refuses to pay for the remaining 30, saying he never authorised the purchase. Is Yusuf liable for the price of all 50 sacks?',
              [legal('Section 196: a person on whose behalf an act is done without his authority may ratify or disown it. Section 197: ratification may be express or implied from conduct. Section 199: ratifying a part of a transaction amounts to ratifying the whole.',
                     'Wasim bought 50 sacks for Yusuf without authority. Yusuf sold 20 of them as his own and refused to pay for 30.',
                     'By selling 20 sacks on his own account, Yusuf by conduct ratified the purchase. He cannot ratify the profitable part and disown the rest; his ratification extends to the whole transaction.',
                     'Yusuf is liable to pay Xavier for all 50 sacks.')],
              [('Ratification — Sections 196 and 197', 1.5, 'provision'), ('Section 199 — whole transaction', 1, 'provision'), ('Conduct amounts to implied ratification', 0.5, 'analysis'), ('Conclusion: liable for 50 sacks', 1, 'conclusion')],
              ['The key words examiners look for: "implied ratification" and "Section 199 — whole transaction".'],
              ['Holding Yusuf liable for only 20 sacks.', 'Ignoring implied ratification by conduct.'],
              ['Number the steps: unauthorised act → conduct → whole ratified.']),
            Q('q2', 5, 'core', 'table',
              'Differentiate a sub-agent from a substituted agent on any five bases.',
              [table(['Basis', 'Sub-agent', 'Substituted agent'], [
                  ['Appointment and control', 'Appointed by the agent; works under the agent\'s control (Section 191)', 'Named by the agent but works under the principal\'s control (Section 194)'],
                  ['Delegation', 'Agent delegates part of his work and keeps his own role', 'Agent hands over that part of the work entirely'],
                  ['Privity of contract with principal', 'None — responsible to the agent', 'Exists — he is the principal\'s own agent'],
                  ['Responsibility of the agent', 'Agent responsible to the principal for the sub-agent\'s acts', 'Agent not responsible once he has selected him with ordinary prudence (Section 195)'],
                  ['Suit by the person appointed', 'Cannot sue the principal for remuneration; claims from the agent', 'Can sue the principal for remuneration'],
                  ['Improper appointment', 'May be improperly appointed (Section 193)', 'Named only under authority, so the question does not arise'],
              ])],
              [('Control / appointment', 1, 'concept'), ('Privity of contract', 1, 'concept'), ('Responsibility of the agent', 1, 'analysis'), ('Right to sue the principal', 1, 'analysis'), ('Any fifth valid point with section', 1, 'provision')],
              ['Most candidates get control and privity right; marks are lost on the agent\'s responsibility.'],
              ['Saying a sub-agent has privity with the principal.'],
              ['Quote Sections 191, 192, 194 and 195 in the table.']),
            Q('q3', 4, 'moderate', 'legal',
              'Zara owes Arjun ₹4,00,000. She appoints Arjun as her agent to sell her shop and authorises him to repay himself the debt out of the sale proceeds. Before the sale, Zara writes to revoke Arjun\'s authority, and a week later she dies. Can Arjun go ahead with the sale?',
              [legal('Section 202: if the agent has his own stake in the very property the agency deals with, the agency cannot — unless the contract expressly provides otherwise — be ended in a way that harms that stake.',
                     'Arjun is Zara\'s creditor for ₹4,00,000 and was authorised to sell her shop and repay himself out of the proceeds. Zara tried to revoke and then died.',
                     'Arjun\'s authority is coupled with an interest in the very property he is to sell. Neither Zara\'s revocation nor her death can end the agency to the prejudice of that interest.',
                     'The agency is irrevocable. Arjun may sell the shop and recover ₹4,00,000 from the proceeds, accounting for any balance to Zara\'s estate.')],
              [('Section 202 stated', 1.5, 'provision'), ('Interest of the agent identified', 1, 'analysis'), ('Revocation and death ineffective', 0.5, 'analysis'), ('Conclusion', 1, 'conclusion')],
              ['Mention that even death does not end such an agency — many candidates stop at revocation.'],
              ['Applying Section 201 (death ends agency) without the Section 202 exception.'],
              ['Write the words "agency coupled with interest".']),
            Q('q4', 6, 'hard', 'legal',
              '(a) State the cases in which an agent is personally liable to third parties. (3 marks) (b) Bina, the wife of Chetan, has for two years bought groceries on credit from Dev Stores, and Chetan has always paid the bills. Chetan then tells Bina to stop, but does not inform Dev Stores. Bina buys groceries worth ₹18,000 on credit. Is Chetan liable? (3 marks)',
              [p('(a) Section 230: an agent normally cannot enforce, and is not bound by, contracts made for his principal. He is presumed to be personally liable where:'),
               ul(['he buys or sells goods on behalf of a merchant living outside India;', 'he does not disclose the name of his principal;', 'the principal, though disclosed, cannot be sued (e.g. a minor or a non-existent company), unless the other party knew;',
                   'he is a pretended agent and the principal disowns the act (Section 235);', 'he exceeds his authority and is liable for breach of warranty of authority;', 'he has expressly agreed to be personally liable.']),
               p('(b)'), legal('Section 237 (agency by estoppel): where a principal, by his words or conduct, has induced third persons to believe that acts done by an agent are within his authority, he is bound by them. Under Section 208, termination of authority takes effect against third persons only when it becomes known to them.',
                               'Chetan had for two years paid for groceries bought by Bina on credit from Dev Stores. He withdrew her authority but did not tell Dev Stores, who supplied ₹18,000 more.',
                               'By his past conduct Chetan held out Bina as his agent. Dev Stores was not told of the withdrawal and acted on that belief.',
                               'Chetan is liable to pay Dev Stores ₹18,000.')],
              [('(a) Section 230 general rule', 1, 'provision'), ('(a) At least four exceptions', 2, 'concept'), ('(b) Section 237 / 208 stated', 1.5, 'provision'), ('(b) Application and conclusion', 1.5, 'conclusion')],
              ['In (b), the word "estoppel" and the fact that Dev Stores was not informed carry the marks.'],
              ['Saying a wife is always her husband\'s agent.', 'Missing the "not informed" point.'],
              ['For (a), a numbered list is ideal.']),
        ],
        'revision': {'summary': ['Agent and principal (182); principal must be major and sane (183); anyone can be an agent but a minor is not liable to the principal (184); no consideration needed (185).',
                                 'Creation: express, implied (estoppel 237, necessity), operation of law, ratification (196–200).',
                                 'Ratification: on behalf of principal; principal competent then and now; full knowledge (198); whole (199); not to harm third parties (200); reasonable time; act not void.',
                                 'Authority: necessary and usual acts (188); emergency (189).',
                                 'Delegation barred (190) except custom or necessity; sub-agent (191–193) vs substituted agent (194–195).',
                                 'Duties 211–218; rights: retainer 217, remuneration 219–220, lien 221, indemnity 222–225.',
                                 'Principal bound by authorised acts (226); separable excess (227/228); notice (229); fraud (238). Agent personally liable — 230 exceptions, 231–235.',
                                 'Termination (201); irrevocable if coupled with interest (202); effect when known (208).'],
                     'remember': ['Minor: can be agent (184), cannot be principal (183).', 'Undisclosed own-account dealing: repudiate (215) or claim benefit (216).', 'Agency coupled with interest survives even death or insanity of the principal (202).'],
                     'traps': ['Do not say a minor agent makes the contract void.', 'Do not allow partial ratification.', 'Do not make the agent responsible for a properly chosen substituted agent.', 'Do not forget third parties must know of termination.']},
        'quickref': [{'k': 'Section 182', 'v': 'Agent and principal defined'}, {'k': 'Sections 183 / 184 / 185', 'v': 'Who may employ; who may be agent; no consideration needed'},
                     {'k': 'Sections 186–187', 'v': 'Express and implied authority'}, {'k': 'Sections 188 / 189', 'v': 'Extent of authority; emergency'}, {'k': 'Sections 190–193', 'v': 'No delegation; sub-agent; proper/improper appointment'},
                     {'k': 'Sections 194–195', 'v': 'Substituted agent; agent\'s duty in naming'}, {'k': 'Sections 196–200', 'v': 'Ratification and its conditions'},
                     {'k': 'Sections 201–210', 'v': 'Termination; irrevocable (202); notice (206); effect (208)'}, {'k': 'Sections 211–218', 'v': 'Agent\'s duties'},
                     {'k': 'Sections 217, 219–225', 'v': 'Agent\'s rights: retainer, remuneration, lien, indemnity'}, {'k': 'Sections 226–229, 237–238', 'v': 'Principal\'s liability to third parties'},
                     {'k': 'Sections 230–235', 'v': 'Personal liability of agent; undisclosed principal; pretended agent'}],
        'viva': [
            V('v1', 'Who can appoint an agent, and who can become an agent?',
              'Under Section 183, any person who is a major and of sound mind can appoint an agent. Under Section 184, any person can become an agent, even a minor, and the principal is bound by his acts towards third parties, but a minor agent is not responsible to the principal.',
              [P('p1', 'Principal must be a major of sound mind (183)', 4, 'major|majority|adult|18', 'sound mind|sane|section 183|183', min=2),
               P('p2', 'Anyone, even a minor, can be an agent (184)', 3, 'any person|anyone|anybody|even a minor|minor can|minor also|even minor|section 184|184'),
               P('p3', 'Minor agent not responsible to the principal', 3, 'not responsible|not liable|not be liable|cannot be held|cannot hold|not hold|no remedy|cannot sue|cannot proceed|not accountable|not answerable')], 'c1'),
            V('v2', 'State the conditions for a valid ratification.',
              'The act must have been done on behalf of the principal; the principal must have existed and been competent when the act was done; he must ratify with full knowledge of the facts; he must ratify the whole transaction; ratification must not injure a third person; it must be within a reasonable time; and the act must not be void or illegal.',
              [P('p1', 'Act done on behalf of the principal', 2, 'on behalf|for the principal|in the name'),
               P('p2', 'Principal existed and was competent at the time', 2, 'exist|competent|capacity|in existence'),
               P('p3', 'Full knowledge of facts (198)', 2, 'knowledge|aware|know the facts|knowing|section 198|198'),
               P('p4', 'Whole transaction ratified (199)', 2, 'whole|entire|all of it|full transaction|not part|section 199|199'),
               P('p5', 'No injury to third parties; reasonable time; act not void', 2, 'third part|third person|reasonable time|not void|lawful|not illegal|section 200|200')], 'c3'),
            V('v3', 'How is a sub-agent different from a substituted agent?',
              'A sub-agent is employed by the agent and works under the agent\'s control; there is no privity of contract between him and the principal, and the agent is responsible for his acts. A substituted agent is named by the agent but works for the principal directly; there is privity of contract with the principal, and the agent is not responsible for him once he has chosen him with ordinary prudence.',
              [P('p1', 'Sub-agent works under the agent\'s control', 3, ALT('sub agent {u} agent', 'subagent {u} agent', 'sub agent {u} control agent', 'sub agent {u} control of the agent', u=('under', 'work under', 'works under', 'controlled by', 'employed by', 'appointed by', 'acts under'))),
               P('p2', 'Substituted agent works for / under the principal; privity with principal', 4, ALT('substitut agent {u} principal', 'substitut {u} principal', u=('under', 'work under', 'works under', 'works for', 'work for', 'controlled by', 'acts for', 'agent of', 'directly for', 'privity with', 'privity of contract with', 'contract with', 'answer to', 'responsible to'))),
               P('p3', 'Agent responsible for sub-agent but not for a properly chosen substituted agent', 3, 'not responsible|not liable|no responsibility|not answerable|ordinary prudence|prudence|section 195|195')], 'c5'),
            V('v4', 'What are the main duties of an agent towards his principal?',
              'An agent must follow the principal\'s instructions or the custom of the trade, act with reasonable skill and diligence, render proper accounts, communicate with the principal in difficulty, not deal on his own account or make secret profits, not delegate his authority, and pay over all sums received for the principal.',
              [P('p1', 'Follow instructions / custom of trade (211)', 2, 'instruction|direction|custom|section 211|211'),
               P('p2', 'Reasonable skill and diligence (212)', 2, 'skill|diligence|care|section 212|212'),
               P('p3', 'Render proper accounts (213)', 2, 'account'),
               P('p4', 'Not deal on own account / no secret profit (215–216)', 2, 'own account|secret profit|secret|conflict|section 215|215|216'),
               P('p5', 'Pay sums received; communicate; not delegate', 2, 'pay|hand over|remit|communicat|delegat|section 218|218', min=1)], 'c6'),
            V('v5', 'When is an agent personally liable to third parties?',
              'Normally an agent is not personally liable, under Section 230. But he is presumed to be personally liable when he contracts for a merchant resident abroad, when he does not disclose the name of his principal, when the principal cannot be sued, when he is only a pretended agent, or when he exceeds his authority.',
              [P('p1', 'General rule: not personally liable (230)', 2, 'normally|general|not personally|not liable|section 230|230'),
               P('p2', 'Merchant resident abroad / foreign principal', 2, 'abroad|foreign|outside india'),
               P('p3', 'Principal undisclosed / unnamed', 2, 'not disclose|undisclosed|unnamed|name not|hide|does not reveal|not reveal'),
               P('p4', 'Principal cannot be sued (minor / non-existent)', 2, 'cannot be sued|cannot sue|incompetent|minor|non existent|not exist'),
               P('p5', 'Pretended agent / exceeds authority', 2, 'pretend|exceed|beyond authority|without authority|warranty|section 235|235')], 'c9'),
            V('v6', 'When does an agency become irrevocable?',
              'Under Section 202, when the agent has his own interest in the property the agency is about, the agency cannot be terminated to the prejudice of that interest unless an express contract allows it. It is not ended even by the death or insanity of the principal.',
              [P('p1', 'Agent has an interest in the subject matter (202)', 5, 'interest', 'agent|subject matter|property|section 202|202', min=2),
               P('p2', 'Cannot be terminated to the prejudice of that interest', 3, 'cannot be terminat|cannot terminat|cannot be revoked|cannot revoke|not revocable|irrevocable|cannot end|cannot be ended|prejudice'),
               P('p3', 'Not ended even by death or insanity of the principal', 2, 'death|dies|insan|unsound')], 'c10'),
            V('v7', 'Explain the authority of an agent in an emergency.',
              'Under Section 189, in an emergency an agent has authority to do all acts to protect his principal from loss that a person of ordinary prudence would do in his own case in similar circumstances, provided he could not communicate with the principal and acted in good faith.',
              [P('p1', 'Protect the principal from loss (189)', 3, 'protect|save|prevent loss|from loss|section 189|189'),
               P('p2', 'As a person of ordinary prudence would in his own case', 4, 'prudence|prudent|reasonable person|own case|his own'),
               P('p3', 'Could not communicate with the principal; good faith', 3, 'communicat|contact|reach|inform|good faith|bona fide|honest|cannot communicat|could not communicat|not communicat|unable to communicat|cannot contact|could not contact|unable to contact|cannot reach|could not reach|not reach|unreachable|not possible to communicat', min=1)], 'c4'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Eshan, the export agent', 'difficulty': 'hard',
            'case': ('Farida, a carpet maker in Bhadohi, appoints Eshan as her agent to sell carpets in Delhi at a commission of 2% on sales. Eshan sells carpets for ₹24,00,000 and spends ₹15,000 on transport, which Farida had agreed to bear. Without telling Farida, Eshan appoints his cousin Gopal to handle some sales; Gopal misappropriates ₹60,000 of the sale proceeds. Separately, Eshan signs a contract "as agent" with Henrik, a buyer in Norway, to sell him carpets made by Farida, without naming her.'),
            'mcqs': [
                M('k1a', 'How much commission is Eshan entitled to?', [R(k_comm), '₹24,000', '₹4,80,000', '₹63,000'], 0,
                  f'2% of ₹24,00,000 = {R(k_comm)} (Section 219).', 'core', '2400000*2/100'),
                M('k1b', 'Before accounting for Gopal\'s misappropriation, how much must Eshan pay over to Farida?', [R(k_net), '₹23,52,000', '₹24,00,000', '₹23,85,000'], 0,
                  f'₹24,00,000 − commission ₹48,000 − transport ₹15,000 = {R(k_net)} (Sections 217–218).', 'moderate', '2400000-48000-15000'),
                M('k1c', 'Who bears the ₹60,000 misappropriated by Gopal, as between Farida and Eshan?', ['Eshan — Gopal was an improperly appointed sub-agent (Section 193)', 'Farida — she is the principal', 'Shared equally', 'Nobody — it is a loss of the third party'], 0,
                  'Delegation was not authorised; for an improperly appointed sub-agent, the agent is responsible to the principal.', 'hard'),
                M('k1d', 'Can Henrik hold Eshan personally liable on the Norway contract?', ['Yes — the principal was not named (Section 230)', 'No — an agent is never personally liable', 'Only if Farida consents', 'Only if Henrik is resident in India'], 0,
                  'An agent who keeps his principal\'s name hidden is presumed to be personally liable.', 'hard'),
            ]}],
    }


# ---------- teaching explanations + topic tags for every MCQ (override the short drafts above) ----------
TWA, TAPPT, TCRE, TEXT = 'What is Agency?', 'Appointment and Authority of Agents', 'Creation of Agency', 'Extent of Agent’s Authority'
TSUB, TDIFF, TDUT, TRIG = 'Sub-agents', 'Difference between a Sub-agent and a Substituted Agent', 'Duties and Obligations of an Agent', 'Rights of an Agent'
TPERS, TREV = 'Personal Liability of Agent to Third Parties', 'Revocation of Authority'
EXPLAIN = {
    'm1': (TWA, 'Section 182: an agent is someone engaged to act for another person or to stand in for him when dealing with outsiders; the person he acts for is the principal. The tempting trap is "a bailee" — a bailee holds goods for a purpose but does not represent the owner in dealings with others. A partner is an agent of the firm, but agency is far wider than partnership. In practice: a clearing and forwarding agent handling customs for an importer acts as the importer\'s agent.'),
    'm2': (TAPPT, 'Section 183: only a person who is a major under his personal law and of sound mind can appoint an agent. The principal must be competent to contract, because the agent\'s acts become his. The tempting trap is "any person including a minor" — a minor cannot appoint an agent, since he cannot contract himself. In practice: a power of attorney signed by a minor is invalid; a guardian must act instead.'),
    'm3': (TAPPT, 'Section 184: as between principal and third persons, any person, even a minor, may become an agent, so the minor\'s acts bind the principal. But a person who is not of majority and sound mind is not responsible to the principal. The tempting trap is "cannot act as an agent at all" — agency capacity depends on the principal, not the agent. In practice: a business that uses a 17-year-old to collect payments is bound by his receipts but cannot sue him for negligence under the agency.'),
    'm4': (TAPPT, 'Section 185: an agency can be created without any consideration. A friend who agrees to act for you without payment is still your agent, with the same authority and duties. The tempting trap is "essential", carried over from the general rule that agreements without consideration are void. In practice: family members often act as unpaid agents under a power of attorney to manage bank accounts or property for relatives living abroad.'),
    'm5': (TCRE, 'Ratification (Sections 196 to 200) can validate only acts that the principal could lawfully have authorised. A void act, such as forging the principal\'s signature, cannot be ratified, and nor can an illegal act. The tempting trap is the unauthorised loan of the principal\'s money — though unauthorised, it is a lawful act and can be ratified. Ratification also cannot injure third parties. In practice: a company cannot adopt a forged cheque, but its board can approve a purchase a manager made without authority.'),
    'm6': (TCRE, 'Section 199: a person ratifying any unauthorised act done on his behalf ratifies the whole transaction of which that act formed part. He cannot accept the benefits and reject the burdens. The tempting trap is "he has ratified only the beneficial part" — the law does not allow selective ratification. In practice: a company that accepts goods bought by an unauthorised manager must also honour the payment terms of that purchase.'),
    'm7': (TEXT, 'Section 189: in an emergency, an agent has authority to do all acts to protect his principal from loss as a person of ordinary prudence would do in his own case under similar circumstances. The tempting trap is "the principal expressly instructed" — in an emergency, the agent may not be able to contact the principal, and the law gives him extended authority. In practice: a transporter carrying perishable goods may sell them en route if they are about to rot and the owner cannot be reached.'),
    'm8': (TSUB, 'Section 191: a sub-agent is someone the original agent engages, and who works under that agent\'s direction, in the business of the agency. The tempting trap is "a substituted agent" — that person is named by the agent at the principal\'s express or implied authority to act for the principal directly, not under the agent\'s control. In practice: when a CA firm engaged by a client outsources part of the work to another firm under its own supervision, that firm acts as a sub-agent.'),
    'm9': (TDIFF, 'A substituted agent, named by the agent with the principal\'s authority, becomes the principal\'s own agent (Section 194), so there is privity of contract between them. A sub-agent, even if properly appointed, is responsible to the agent, not the principal, except for fraud or wilful wrong. The tempting trap is "a properly appointed sub-agent" — proper appointment binds the principal to third parties but creates no privity. In practice: a property owner who authorises his broker to appoint a local broker directly can deal with that local broker himself.'),
    'm10': (TDUT, 'Section 215: if an agent deals on his own account without the principal\'s consent, and either conceals material facts dishonestly or the dealing is disadvantageous, the principal may repudiate the transaction. Section 216 lets the principal claim any benefit the agent made. The tempting trap is "only claim the agreed commission" — the principal has far stronger remedies. In practice: a broker who quietly buys his client\'s property at a low price can be forced to undo the deal or hand over the profit.'),
    'm11': (TRIG, 'Commission = 3% × ₹6,00,000 = ₹18,000. Under Sections 217 and 218 the agent may deduct his commission and expenses properly incurred before paying over: ₹6,00,000 − ₹18,000 − ₹9,000 = ₹5,73,000. The tempting trap is ₹5,82,000, deducting only commission. In practice: a selling agent sends the principal an account sales showing gross sales, commission and expenses, with the net amount remitted.'),
    'm12': (TRIG, 'Section 224: a principal is not liable to indemnify an agent for a criminal act, even if the principal employed him to do it. Sections 222 and 223, by contrast, give indemnity for lawful acts in the exercise of authority and for acts done in good faith that injure third persons. The tempting trap is the good-faith option, which sounds risky but is protected. In practice: an employee told to falsify accounts cannot later claim reimbursement of fines from his employer.'),
    'm13': (TPERS, 'Section 230: an agent generally cannot be sued on contracts made for his principal, but he is presumed personally liable where he buys or sells goods on behalf of a merchant living abroad, where he does not disclose his principal\'s name, or where the principal, though disclosed, cannot be sued. The tempting trap is "a company registered in India" — such a disclosed principal can be sued directly. In practice: Indian import agents of foreign suppliers are careful about their personal exposure.'),
    'm14': (TREV, 'Section 202: when the agent has his own interest in the property he is dealing with, the agency cannot, unless agreed, be ended in a way that harms that interest — not even by the principal\'s death. Lal is to recover his ₹3,00,000 from the sale, so the agency survives Kavi\'s death. The tempting trap is "terminates on Kavi\'s death", the normal Section 201 rule. In practice: lenders take irrevocable powers of attorney to sell secured property for recovery of their dues.'),
    'm15': (TREV, 'Section 208: termination of an agent\'s authority takes effect, as regards third persons, only when it becomes known to them. Until then, third parties can rely on the agent\'s apparent authority. The tempting trap is "from the date of the principal\'s decision" — that applies between principal and agent, but outsiders are protected until they learn of it. In practice: companies that remove an authorised signatory notify banks and major suppliers in writing at once.'),
    'm16': (TREV, 'Section 201 lists the ways an agency ends: revocation by the principal, renunciation by the agent, completion of the business, death or unsoundness of mind of either principal or agent, and the principal being adjudicated insolvent. Only the principal\'s insolvency terminates the agency. The tempting trap is "the agent" — the agent\'s death or unsoundness of mind ends it, but not his insolvency. In practice: when a business is declared insolvent, the authority of its agents ends and the insolvency professional takes over.'),
    'k1/k1a': (TRIG, 'Section 219 entitles the agent to the agreed remuneration once the act is completed. Commission = 2% × ₹24,00,000 = ₹48,000. The tempting trap is ₹63,000, which wrongly adds the ₹15,000 transport expense to the commission — expenses are reimbursed separately. In practice: agents\' commissions are recorded as selling expenses by the principal, and TDS under the Income-tax Act may apply when commission crosses the threshold.'),
    'k1/k1b': (TRIG, 'Sections 217 and 218 let the agent retain his commission and expenses properly incurred before paying over the sale proceeds: ₹24,00,000 − ₹48,000 − ₹15,000 = ₹23,37,000. The tempting trap is ₹23,52,000, deducting commission only and forgetting the agreed transport cost. In practice: the principal\'s accountant reconciles the agent\'s account sales against goods dispatched and the remittance received.'),
    'k1/k1c': (TSUB, 'Eshan appointed Gopal without Farida\'s knowledge or authority, so Gopal is an improperly appointed sub-agent. Section 193 makes the agent responsible for such a sub-agent\'s acts both to the principal and to third persons. So Eshan bears the ₹60,000 as between him and Farida. The tempting trap is "Farida — she is the principal"; she never authorised the delegation. In practice: agency agreements usually forbid sub-delegation without written consent for exactly this reason.'),
    'k1/k1d': (TPERS, 'Section 230 presumes an agent personally liable where he does not disclose the name of his principal. Eshan signed "as agent" but did not name Farida, so Henrik can hold Eshan personally liable. The tempting trap is "only if Henrik is resident in India" — the "merchant resident abroad" rule concerns where the principal lives, and is not what applies here. In practice: export agents usually name the manufacturer in the contract to avoid personal liability for its performance.'),
}


_build_core = build


def build():
    """Applies the teaching explanation and topic tag to every MCQ (unit set and case-study sets)."""
    u = _build_core()
    for q in u['mcqs']:
        q['topic'], q['explain'] = EXPLAIN[q['id']]
    for cs in u.get('cases') or []:
        for q in cs['mcqs']:
            q['topic'], q['explain'] = EXPLAIN[cs['id'] + '/' + q['id']]
    return u


# ---------------------------------------------------------------------------------------------
# Offline auto-check data for the Write tab (matched by tools/ca_vivamatch.py / js/ca-tools.js).
# Per scheme point: kw = keyword groups ("a|b" = alternatives), min = groups needed, nums = figures
# that must appear, wrong/say = remark for a common wrong statement, ai_only = left to AI examiners.
# ---------------------------------------------------------------------------------------------
def _k(*groups, n=None, **extra):
    d = {'kw': list(groups), 'min': len(groups) if n is None else n}
    d.update(extra)
    return d


AUTO = {
    'q1': {'extra_ok': False,
           's1': _k('section 196|ratify|ratification|ratified|ratif', 'section 197|express|implied|conduct'),
           's2': _k('section 199|whole transaction|entire transaction|ratify the whole|ratification of the whole|ratifies the whole|part amounts to whole|cannot ratify part|cannot ratify only part|not ratify a part|cannot ratify a part|ratifying part|ratification of part|whole of the transaction'),
           's3': _k('20 sacks|sold|selling|sale', 'ratified conduct|conduct ratified|ratification conduct|implied ratification|impliedly ratified|ratified impliedly|conduct amounts|implied by conduct|ratified the purchase|ratifies the purchase|ratified the transaction|ratified the contract|amounts to ratification'),
           's4': _k('liable for all 50|liable 50|pay for all 50|pay 50|all 50|50 sacks liable|whole 50|entire 50|pay for 50|liable for 50|price of 50|price of all 50',
                    wrong=[{'kw': ['only 20|liable for 20|20 sacks only|pay for 20'], 'say': 'Ratifying part of a transaction ratifies the whole (Section 199) — Yusuf must pay for all 50 sacks.'}]),
           },
    'q2': {'extra_ok': True,
           's1': _k('agent s control|control of the agent|under the agent|agent control|controlled by the agent', 'principal s control|control of the principal|under the principal|principal control|controlled by the principal'),
           's2': _k('privity', 'no privity|not privity|none|no contract with principal|no direct', 'privity exists|privity exist|exists|direct privity|own agent|principal s agent|agent of the principal', n=3),
           's3': _k('agent responsible|agent is responsible|agent liable|responsible for the sub-agent|responsible for sub agent|agent is liable', 'not responsible|not liable|ordinary prudence|section 195'),
           's4': _k('cannot sue|not sue|no right to sue|claims from the agent|claim from the agent|only against the agent', 'can sue the principal|sue the principal|may sue|right to sue the principal|sue principal'),
           's5': _k('delegate|delegates|delegation|improper|improperly|section 193|section 192|hands over|entirely'),
           },
    'q3': {'extra_ok': False,
           's1': _k('section 202|interest|stake', 'irrevocable|cannot be revoked|cannot be terminated|not revocable|cannot be ended|cannot end|not terminated|cannot terminate|not be revoked|prejudice'),
           's2': _k('coupled with interest|coupled with an interest|interest in the property|interest in the subject matter|interest in the shop|arjun has an interest|arjun interest|own interest|personal interest|stake in the property|stake in the shop|creditor interest|own stake'),
           's3': _k('revocation|revoke|revoked|neither revocation|neither zara revocation', 'death|died|dies|nor death|nor her death', 'ineffective|cannot end|cannot terminate|not end|does not end|no effect|not terminate|not affect|invalid|can end|cannot be ended|cannot be revoked|irrevocable'),
           's4': _k('irrevocable|arjun can sell|arjun may sell|go ahead|proceed with the sale|arjun can go ahead|arjun entitled to sell|sale valid|arjun can recover|arjun sell'),
           },
    'q4': {'extra_ok': True,
           's1': _k('section 230|cannot personally enforce|cannot enforce|not personally bound|not bound by contracts|agent not personally liable|not personally liable'),
           's2': _k('foreign|outside india|abroad|resident abroad', 'undisclosed|not disclose|does not disclose|name of the principal|name not disclosed|unnamed', 'cannot be sued|minor|non existent|not in existence|incompetent', 'pretended|section 235|no authority|disown', 'exceeds|warranty of authority|beyond authority|exceeding', 'expressly agreed|agrees to be personally|special contract|agreed to be personally|contract to that effect|personally liable by contract', n=4),
           's3': _k('section 237|estoppel|held out|holding out|conduct|induced', 'section 208|termination|known|notice|not informed|knowledge|informed|told'),
           's4': _k('chetan liable|chetan is liable|chetan must pay|liable to pay dev|liable to pay 18000|chetan bound|chetan has to pay|liable for 18000|chetan is bound|dev stores can recover|dev can recover|chetan pay 18000|chetan cannot escape|chetan cannot deny',
                    wrong=[{'kw': ['chetan not liable|chetan is not liable'], 'say': 'Chetan held Bina out as his agent and never told Dev Stores of the withdrawal — he is bound (Sections 237, 208).'}]),
           },
}


_build_noauto = build


def build():
    """Adds the offline auto-check fields (kw/min/nums/wrong) to every scheme point."""
    u = _build_noauto()
    for q in u['questions']:
        a = AUTO[q['id']]
        q['extra_ok'] = a.get('extra_ok', False)
        if '_scheme' in a: q['scheme'] = a['_scheme']        # "any N points" split into N one-mark points
        for s in q['scheme']:
            s.update(a[s['id']])
    return u
