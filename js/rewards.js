/* ================= 🎁 Rewards (js/rewards.js) =================
   Four free, never-paid motivators for school and CA students. All state lives in ST.rw (saved with save()):
     ST.rw = { sh: shields held (0–2), shDay: day a shield was last earned, shSaved: [day, n] last rescue,
               cards: { cardId: 'YYYY-MM-DD' }, init: 1 after the first silent card check,
               box: { d: day opened, r: reward }, boxes: boxes opened, acc/cols/stk: owned accessories / map colours / stickers,
               wear: accessory worn, mapc: map colour in use, bonus: bonus stars from boxes,
               boss: { wk: Monday key, tries, beaten, best, qids }, bossWins, bossLog: [Monday keys beaten],
               maxCh / maxSub: most chapters / subjects ever finished (school), q: [celebrations waiting] }
   1. 🛡️ Streak shield — every 7th day of a streak earns 1 shield (max 2). If exactly one day is missed, a shield is used
      the next time the app opens (the streak's last day moves to yesterday) and a kind message is queued.
      liveStreak() / bumpStreak() / hud() in js/app.js are wrapped here (they are globals, called by name).
   2. 🎁 Mystery box — once a day after today's goal (js/practice.js ST.daily) a box card waits at the top of Practice.
      Opening it gives one free cosmetic: an avatar accessory, a map frame colour (school), a sticker, a box-only card,
      or a few bonus stars. Rewards show in Me (🃏 My cards card → album → My stuff).
   3. 🃏 Collectible cards — an album in Me. Cards unlock by learning (3-star quests, finished chapters and subjects,
      CA unit steps), streak milestones, mystery boxes and weekly bosses.
   4. 👾 Boss of the week — 10 of the student's own weak questions (school: ST.qstats of their grade; CA: ST.ca.mcq),
      filled from recent quests / units. 7 right answers beat it; 3 tries a week; resets every Monday (app day keys).
   One celebration sheet (.sheet, swipe-to-close via js/sheets.js) shows rewards one at a time from a queue.
   Practice order: Today's goal → 🎁 box (only when waiting) → 👾 boss → 🎮 Play (js/playhub.js) → 🧮 Calculator Academy.
   Me: 🃏 My cards right after the profile card.  window.Rewards = { … } */
(function () {
  'use strict';
  const D = document, $1 = (s, r) => (r || D).querySelector(s);
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const STx = () => { try { return ST; } catch (e) { return null; } };
  const isCA = () => { const s = STx(); return !!(s && s.profile && s.profile.course === 'ca'); };
  const isParent = () => { try { return !!(window.Cloud && Cloud.isParent && Cloud.isParent()); } catch (e) { return false; } };
  const day = () => today();
  const dk = d => d.toISOString().slice(0, 10);
  const plus = (k, n) => dk(new Date(Date.parse(k + 'T00:00:00Z') + n * 864e5));
  const monday = k => { const t = new Date(k + 'T00:00:00Z'); return plus(k, -((t.getUTCDay() + 6) % 7)); };
  const saveNow = () => { try { save(); } catch (e) {} };
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const reduced = () => { try { return matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } };
  const MAX_SH = 2;

  function R() {
    const s = STx(); if (!s) return {};
    const r = s.rw = s.rw && typeof s.rw === 'object' ? s.rw : {};
    if (!r.cards || typeof r.cards !== 'object') r.cards = {};
    ['acc', 'cols', 'stk', 'q', 'bossLog'].forEach(k => { if (!Array.isArray(r[k])) r[k] = []; });
    r.sh = Math.max(0, Math.min(MAX_SH, +r.sh || 0)); r.boxes = +r.boxes || 0; r.bossWins = +r.bossWins || 0;
    return r;
  }

  /* ================= cards ================= */
  /* [id, emoji, name, fact (Knowtopia's own words), rarity c / r / e] — the unlock rule comes from the set (RULES) */
  const SETS = [
    { id: 'sci', e: '🔬', n: 'Scientists', for: 's', col: '#3b82f6', cards: [
      ['raman', '🌈', 'C.V. Raman', 'Found that light changes colour a little when it scatters (the Raman effect). Nobel Prize in Physics, 1930. National Science Day, 28 Feb, marks his discovery.', 'c'],
      ['kalam', '🚀', 'A.P.J. Abdul Kalam', 'The “Missile Man of India”. Led the SLV-3 rocket project and India’s missile programme, then served as the 11th President (2002–2007).', 'c'],
      ['curie', '☢️', 'Marie Curie', 'Discovered polonium and radium. The first person to win Nobel Prizes in two sciences: Physics (1903) and Chemistry (1911).', 'c'],
      ['newton', '🍎', 'Isaac Newton', 'Explained the three laws of motion and gravity that pulls everything together. Also built an early reflecting telescope.', 'c'],
      ['ramanujan', '♾️', 'Srinivasa Ramanujan', 'A mostly self-taught maths genius from Tamil Nadu. India celebrates National Mathematics Day on his birthday, 22 December.', 'c'],
      ['jcbose', '🌱', 'Jagadish Chandra Bose', 'A pioneer of radio-wave research. His crescograph showed that plants respond to things around them.', 'c'],
      ['aryabhata', '🌏', 'Aryabhata', 'Indian mathematician–astronomer of the 5th century. He wrote that the Earth spins on its axis. India’s first satellite (1975) carries his name.', 'c'],
      ['einstein', '💡', 'Albert Einstein', 'Gave us the theory of relativity and E = mc². Won the 1921 Nobel Prize for explaining the photoelectric effect.', 'c'],
      ['bhabha', '⚛️', 'Homi J. Bhabha', 'Father of India’s nuclear programme. Founded TIFR in Mumbai and the atomic research centre at Trombay, now BARC.', 'r'],
      ['sarabhai', '🛰️', 'Vikram Sarabhai', 'Father of India’s space programme. He led the setting up of ISRO in 1969.', 'r'],
      ['galileo', '🔭', 'Galileo Galilei', 'Improved the telescope and in 1610 spotted the four biggest moons of Jupiter.', 'r'],
      ['darwin', '🐢', 'Charles Darwin', 'Explained how living things change over time by natural selection, in his 1859 book “On the Origin of Species”.', 'r'],
      ['snbose', '🧪', 'Satyendra Nath Bose', 'Worked with Einstein on Bose–Einstein statistics. Particles called “bosons” are named after him.', 'r'],
      ['chawla', '👩‍🚀', 'Kalpana Chawla', 'The first woman of Indian origin to go to space, on the Space Shuttle Columbia in 1997.', 'e'],
      ['lovelace', '💻', 'Ada Lovelace', 'In 1843 she wrote steps for Charles Babbage’s Analytical Engine — often called the first computer program.', 'e']] },
    { id: 'free', e: '🇮🇳', n: 'Freedom fighters', for: 's', col: '#f97316', cards: [
      ['gandhi', '🕊️', 'Mahatma Gandhi', 'Led India’s freedom struggle with satyagraha — truth and non-violence. In 1930 he walked to Dandi in the Salt March.', 'c'],
      ['nehru', '🌹', 'Jawaharlal Nehru', 'India’s first Prime Minister (1947–1964). His birthday, 14 November, is celebrated as Children’s Day.', 'c'],
      ['patel', '🧱', 'Sardar Vallabhbhai Patel', 'The “Iron Man of India”. After 1947 he brought more than 560 princely states together into one India.', 'c'],
      ['ambedkar', '📜', 'Dr B.R. Ambedkar', 'Chaired the committee that drafted India’s Constitution and fought all his life for equality and the rights of Dalits.', 'c'],
      ['laxmibai', '🐎', 'Rani Lakshmibai', 'The Rani of Jhansi. She fought bravely against British forces in the revolt of 1857.', 'c'],
      ['tilak', '📣', 'Bal Gangadhar Tilak', 'Declared “Swaraj is my birthright and I shall have it!” and made Ganesh festivals public to bring people together.', 'c'],
      ['naidu', '🎶', 'Sarojini Naidu', 'The “Nightingale of India” — a poet, the first Indian woman to preside over the Congress (1925) and India’s first woman Governor.', 'c'],
      ['azadm', '📚', 'Maulana Abul Kalam Azad', 'Freedom fighter and independent India’s first Education Minister. His birthday, 11 November, is National Education Day.', 'r'],
      ['lajpat', '🦁', 'Lala Lajpat Rai', 'Called “Punjab Kesari” (Lion of Punjab). He led the 1928 protest against the Simon Commission in Lahore.', 'r'],
      ['pandey', '🎖️', 'Mangal Pandey', 'A sepoy whose stand at Barrackpore in March 1857 is remembered as an early spark of the 1857 revolt.', 'r'],
      ['azadc', '🔥', 'Chandrashekhar Azad', 'A fearless young revolutionary who vowed the British would never capture him alive.', 'r'],
      ['bhagat', '✊', 'Bhagat Singh', 'Revolutionary who made “Inquilab Zindabad” famous. He gave his life for India in 1931, aged just 23.', 'e'],
      ['netaji', '🎺', 'Subhas Chandra Bose', '“Netaji” led the Azad Hind Fauj (Indian National Army) and gave the call “Dilli Chalo!”', 'e']] },
    { id: 'won', e: '🏛️', n: 'Indian wonders', for: 'b', col: '#a16207', cards: [
      ['taj', '🕌', 'Taj Mahal, Agra', 'A white-marble tomb built by Shah Jahan in memory of Mumtaz Mahal. A UNESCO World Heritage Site.', 'c'],
      ['qutub', '🗼', 'Qutub Minar, Delhi', 'A brick tower about 73 m tall. Qutb-ud-din Aibak began building it around 1200.', 'c'],
      ['redfort', '🏰', 'Red Fort, Delhi', 'A red-sandstone fort built by Shah Jahan. The Prime Minister raises the flag here every Independence Day.', 'c'],
      ['gateway', '⛩️', 'Gateway of India, Mumbai', 'A grand arch by the sea, built to mark King George V’s visit in 1911 and finished in 1924.', 'c'],
      ['golden', '✨', 'Golden Temple, Amritsar', 'Harmandir Sahib. Its langar (community kitchen) serves free meals to thousands of people every day.', 'c'],
      ['sanchi', '☸️', 'Sanchi Stupa', 'In Madhya Pradesh. The Great Stupa was first built in Emperor Ashoka’s time, in the 3rd century BCE.', 'c'],
      ['ajanta', '🎨', 'Ajanta Caves', 'Buddhist caves cut into rock in Maharashtra, famous for their ancient wall paintings.', 'r'],
      ['jantar', '☀️', 'Jantar Mantar, Jaipur', 'Giant stone instruments for watching the sky, built by Sawai Jai Singh II — including a huge sundial.', 'r'],
      ['meenakshi', '🛕', 'Meenakshi Temple, Madurai', 'Famous for its tall, colourful gopurams (gateway towers) covered with carved figures.', 'r'],
      ['hampi', '🪨', 'Hampi', 'Ruins of Vijayanagara, a great empire’s capital in Karnataka. Look for the stone chariot at the Vittala temple.', 'r'],
      ['konark', '🛞', 'Konark Sun Temple', 'A 13th-century temple in Odisha shaped like the Sun god’s chariot, with 24 carved stone wheels.', 'e'],
      ['brihad', '🗿', 'Brihadisvara Temple, Thanjavur', 'Built by the Chola king Raja Raja I and completed in 1010 CE. Its tower is about 66 m tall.', 'e']] },
    { id: 'ani', e: '🐾', n: 'Animals', for: 's', col: '#16a34a', cards: [
      ['tiger', '🐅', 'Bengal tiger', 'India’s national animal. Every tiger’s stripes are different, like a fingerprint.', 'c'],
      ['peacock', '🦚', 'Indian peafowl', 'India’s national bird. Only the male — the peacock — has the long, colourful tail.', 'c'],
      ['elephant', '🐘', 'Asian elephant', 'India’s national heritage animal. Its ears are smaller than an African elephant’s.', 'c'],
      ['lion', '🦁', 'Asiatic lion', 'Lives in the wild only in and around the Gir forest of Gujarat.', 'c'],
      ['rhino', '🦏', 'One-horned rhino', 'Most of the world’s one-horned rhinos live in Kaziranga National Park, Assam.', 'c'],
      ['dolphin', '🐬', 'Ganges river dolphin', 'India’s national aquatic animal. It is almost blind and finds food by listening to echoes.', 'r'],
      ['snowleo', '🐆', 'Snow leopard', 'Lives high in the Himalayas. Its long, thick tail helps it balance and keeps it warm.', 'r'],
      ['cobra', '🐍', 'King cobra', 'The longest venomous snake in the world. It mostly eats other snakes.', 'r'],
      ['turtle', '🐢', 'Olive ridley turtle', 'Thousands nest together on Odisha’s beaches in a mass nesting called “arribada”.', 'r'],
      ['squirrel', '🐿️', 'Indian giant squirrel', 'A colourful tree squirrel about 1 m long from nose to tail tip — Maharashtra’s state animal.', 'r'],
      ['redpanda', '🦊', 'Red panda', 'Lives in the forests of the eastern Himalayas, spends most of its time in trees and eats mostly bamboo.', 'e'],
      ['bustard', '🦤', 'Great Indian bustard', 'One of the heaviest flying birds. Critically endangered — most live in Rajasthan.', 'e']] },
    { id: 'spc', e: '🚀', n: 'Space', for: 's', col: '#6d28d9', cards: [
      ['sun', '☀️', 'The Sun', 'Our nearest star. Its light takes about 8 minutes to reach Earth.', 'r'],
      ['moon', '🌙', 'The Moon', 'Earth’s only natural satellite. We always see the same side of it.', 'r'],
      ['jupiter', '🪐', 'Jupiter', 'The biggest planet. Its Great Red Spot is a storm larger than the whole Earth.', 'r'],
      ['mars', '🔴', 'Mars', 'Iron-rich dust makes it red. It has Olympus Mons, the tallest volcano in the solar system.', 'r'],
      ['chandrayaan', '🌗', 'Chandrayaan-3', 'On 23 August 2023 India became the first country to land near the Moon’s south pole.', 'e'],
      ['mangalyaan', '🛰️', 'Mangalyaan', 'India’s Mars Orbiter reached Mars in 2014 — the first Asian mission to get there, on its first try.', 'e'],
      ['aditya', '🔆', 'Aditya-L1', 'India’s first mission to study the Sun, watching it from about 1.5 million km away.', 'e'],
      ['iss', '🛸', 'Space station', 'The International Space Station circles the Earth about once every 90 minutes.', 'e'],
      ['milkyway', '🌌', 'The Milky Way', 'Our home galaxy, with hundreds of billions of stars.', 'e'],
      ['blackhole', '⚫', 'Black hole', 'Gravity so strong that not even light can escape. The first photo of one was shown in 2019.', 'e'],
      ['saturn', '💫', 'Saturn', 'Its famous rings are made of countless pieces of ice and rock.', 'e'],
      ['venus', '🌋', 'Venus', 'The hottest planet — over 450 °C — because its thick clouds trap heat.', 'e']] },
    { id: 'acc', e: '📘', n: 'Accounting ideas', for: 'c', col: '#0f766e', cards: [
      ['as', '📏', 'Accounting Standards — what and why', 'Common written rules for recognising, measuring and showing items, so accounts of different businesses can be compared and trusted.', 'c'],
      ['faa', '🧭', 'Fundamental accounting assumptions', 'Going concern, consistency and accrual. If they are followed, no note is needed; if one is not followed, it must be disclosed.', 'c'],
      ['entity', '🏢', 'Entity, money measurement and periodicity', 'The business is separate from its owner, only events measurable in money are recorded, and its life is split into periods.', 'c'],
      ['accrual', '⏱️', 'Accrual and matching', 'Record income when earned and expenses when incurred — not when cash moves — and match costs with the revenue of the same period.', 'c'],
      ['dual', '⚖️', 'Dual aspect — the accounting equation', 'Every transaction has two sides, so Assets = Liabilities + Capital always holds.', 'c'],
      ['debcred', '↔️', 'Rules of debit and credit', 'Personal: debit the receiver, credit the giver. Real: debit what comes in, credit what goes out. Nominal: debit expenses and losses, credit incomes and gains.', 'c'],
      ['capexp', '🏗️', 'Capital vs revenue expenditure', 'Capital spending gives benefit for years (a machine); revenue spending is used up within the year (wages, repairs) and goes to the P&L.', 'c'],
      ['caprec', '💰', 'Capital vs revenue receipts', 'Capital receipts (a loan taken, sale of a fixed asset) are not income; revenue receipts (sales, interest earned) go to the P&L.', 'c'],
      ['brs', '🏦', 'Bank reconciliation — add or less', 'Explains why the cash book and the pass book balances differ, e.g. cheques issued but not yet presented.', 'c'],
      ['conserv', '🛡️', 'Conservatism, consistency and materiality', 'Provide for all known losses but do not count profits early, keep methods the same each year, and show what matters to users.', 'r'],
      ['tberr', '🔍', 'Errors the trial balance does not reveal', 'Complete omission, errors of principle, compensating errors and posting to the wrong account on the correct side — the totals still agree.', 'r'],
      ['nrv', '📦', 'Inventory at the lower of cost and NRV', 'Inventory is valued at cost or net realisable value, whichever is lower.', 'r'],
      ['depn', '📉', 'Depreciation — SLM and WDV', 'SLM charges the same amount every year; WDV charges a fixed rate on the falling book value, so the charge drops each year.', 'r'],
      ['baddebt', '🧾', 'Bad debts and provision for doubtful debts', 'Write off debts that cannot be recovered, and keep a provision for those that may not be.', 'r'],
      ['prov', '📑', 'Provisions, contingent liabilities and contingent assets', 'A provision is recognised for a present obligation with a probable outflow; a contingent liability is disclosed; a contingent asset is not recognised.', 'e'],
      ['goodwill', '🤝', 'Goodwill in partnership', 'The value of a firm’s reputation to earn more than normal profits — valued by average profit, super profit or capitalisation methods.', 'e'],
      ['premium', '🏷️', 'Shares at premium and at discount', 'Premium goes to the Securities Premium account. Under the Companies Act, 2013 shares generally cannot be issued at a discount (sweat equity is the exception).', 'e'],
      ['bonus', '🎁', 'Bonus issue', 'Free shares given to existing shareholders by capitalising reserves — no cash comes in.', 'e']] },
    { id: 'lead', e: '💼', n: 'Business leaders & economists', for: 'c', col: '#b45309', cards: [
      ['jamsetji', '🏭', 'Jamsetji Tata', 'Founder of the Tata Group. He planned India’s first steel plant, which opened at Jamshedpur in 1907–08 after his death.', 'c'],
      ['jrd', '✈️', 'J.R.D. Tata', 'Got India’s first commercial pilot licence (1929) and founded Tata Airlines, which became Air India.', 'c'],
      ['kurien', '🥛', 'Verghese Kurien', 'Father of the White Revolution. He built Amul’s cooperative model, helping India become the world’s largest milk producer.', 'c'],
      ['murthy', '🖥️', 'N.R. Narayana Murthy', 'Co-founded Infosys in 1981, starting with ₹10,000 borrowed from his wife, Sudha Murty.', 'c'],
      ['dhirubhai', '📈', 'Dhirubhai Ambani', 'Founded Reliance Industries and brought millions of ordinary Indians into the share market.', 'r'],
      ['kiran', '🧬', 'Kiran Mazumdar-Shaw', 'Started Biocon in 1978 from a garage in Bengaluru and grew it into a global biotech company.', 'r'],
      ['naoroji', '🎩', 'Dadabhai Naoroji', 'The “Grand Old Man of India”. His drain theory showed how wealth flowed out of India to Britain.', 'r'],
      ['kautilya', '📜', 'Kautilya (Chanakya)', 'Ancient thinker whose Arthashastra discusses statecraft, taxes and running an economy.', 'r'],
      ['ratan', '🚗', 'Ratan Tata', 'Led the Tata Group from 1991 to 2012, when it bought global brands like Tetley and Jaguar Land Rover.', 'r'],
      ['nooyi', '🥤', 'Indra Nooyi', 'Indian-born business leader who was CEO of PepsiCo from 2006 to 2018.', 'r'],
      ['smith', '🤲', 'Adam Smith', 'Wrote “The Wealth of Nations” (1776) and described the “invisible hand” of markets.', 'e'],
      ['keynes', '🏛️', 'John Maynard Keynes', 'Showed that government spending can fight recessions and unemployment (The General Theory, 1936).', 'e'],
      ['manmohan', '📘', 'Dr Manmohan Singh', 'Economist who, as Finance Minister, led India’s 1991 reforms, then served as Prime Minister (2004–2014).', 'e'],
      ['sen', '🏅', 'Amartya Sen', 'Won the 1998 Nobel Prize in Economics for his work on welfare, poverty and famines.', 'e']] }];
  /* unlock rules per set (in card order): [kind, n]. kinds: mastery = 3-star quests · chapters · subjects (every quest done) ·
     streak = best streak · steps = CA unit steps done · box = found in a mystery box · boss = weekly bosses beaten */
  const seq = (k, ns) => ns.map(n => [k, n]);
  const RULES = {
    sci: seq('mastery', [1, 2, 3, 5, 7, 10, 13, 16, 20, 25, 30, 40, 50, 65, 80]),
    free: seq('chapters', [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 18, 22, 26]),
    won: { s: seq('streak', [2, 3, 4, 5, 7, 10, 14, 21, 30, 45, 60, 100]), c: seq('box', Array(12).fill(0)) },
    ani: seq('box', Array(12).fill(0)),
    spc: seq('subjects', [1, 2, 3, 4]).concat(seq('boss', [1, 2, 3, 4, 5, 6, 7, 8])),
    acc: seq('steps', [1, 3, 6, 10, 15, 20, 25, 30, 40, 50, 60, 75, 90, 110, 130, 150, 175, 200]),
    lead: seq('streak', [2, 3, 5, 7, 10, 14, 21, 30]).concat(seq('box', [0, 0]), seq('boss', [1, 2, 3, 4]))
  };
  const ALL = [];
  SETS.forEach(st => st.cards.forEach((c, i) => { const r = RULES[st.id]; const rs = Array.isArray(r) ? { s: r[i], c: r[i] } : { s: r.s[i], c: r.c[i] };
    ALL.push({ id: st.id + '-' + c[0], set: st.id, e: c[1], n: c[2], t: c[3], r: c[4], rule: rs }); }));
  const byId = id => ALL.find(c => c.id === id);
  const setsFor = ca => SETS.filter(s => s.for === 'b' || s.for === (ca ? 'c' : 's'));
  const album = ca => { const ids = setsFor(ca).map(s => s.id); return ALL.filter(c => ids.includes(c.set)); };
  const ruleOf = (c, ca) => c.rule[ca ? 'c' : 's'];
  const RAR = { c: 'Common', r: 'Rare', e: 'Epic' };
  function howTo(c, ca) {
    const [k, n] = ruleOf(c, ca), p = (x, a, b) => x === 1 ? a : b;
    switch (k) {
      case 'mastery': return `Get ⭐⭐⭐ in ${n} ${p(n, 'quest', 'quests')}`;
      case 'chapters': return `Finish ${n} ${p(n, 'chapter', 'chapters')} (every quest done)`;
      case 'subjects': return `Finish every quest in ${n} ${p(n, 'subject', 'subjects')}`;
      case 'streak': return `Reach a ${n}-day 🔥 streak`;
      case 'steps': return `Finish ${n} CA unit ${p(n, 'step', 'steps')} (Learn, Examples, MCQ…)`;
      case 'boss': return `Beat ${n} weekly ${p(n, 'boss', 'bosses')} 👾`;
      default: return 'Find it in a 🎁 mystery box';
    }
  }

  /* ---------- progress counters ---------- */
  const mastered = () => { const s = STx(); return Object.values((s && s.topics) || {}).filter(t => t && t.stars >= 3).length; };
  const bestStreak = () => { const s = STx(); return Math.max(+(s.streak && s.streak.best) || 0, +(s.streak && s.streak.n) || 0); };
  function caSteps() { const s = STx(), u = (s.ca && s.ca.units) || {}; const K = ['learn', 'illus', 'job', 'mcq', 'write', 'revise']; let n = 0; Object.values(u).forEach(x => { if (x) K.forEach(k => { if (x[k]) n++; }); }); return n; }
  async function schoolDone() {          // chapters / subjects finished in the current grade (best ever kept in ST.rw)
    const r = R(), s = STx(), g = s.profile.grade; let ch = 0, sub = 0;
    try {
      for (const x of (typeof curSubjects === 'function' ? curSubjects(g) : [])) {
        const d = await subjectData(g, x.id); if (!d || !d.chapters) continue; let all = d.chapters.length > 0;
        d.chapters.forEach(c => { const ok = c.topics.length && c.topics.every(t => topicStars(t.id) > 0); if (ok) ch++; else all = false; });
        if (all) sub++;
      }
    } catch (e) {}
    r.maxCh = Math.max(+r.maxCh || 0, ch); r.maxSub = Math.max(+r.maxSub || 0, sub);
    return { chapters: r.maxCh, subjects: r.maxSub };
  }
  let checking = false, recheck = false;
  async function checkCards() {
    const s = STx(); if (!s || !s.profile || isParent()) return [];
    if (checking) { recheck = true; return []; } checking = true;
    try {
      const r = R(), ca = isCA();
      const cnt = { mastery: mastered(), streak: bestStreak(), boss: r.bossWins, steps: 0, chapters: 0, subjects: 0 };
      if (ca) cnt.steps = caSteps(); else Object.assign(cnt, await schoolDone());
      const fresh = [];
      album(ca).forEach(c => { const [k, n] = ruleOf(c, ca); if (r.cards[c.id] || k === 'box') return; if ((cnt[k] || 0) >= n) { r.cards[c.id] = day(); fresh.push(c.id); } });
      const first = !r.init; r.init = 1;
      if (fresh.length) { if (fresh.length >= 3 || first) r.q.push({ k: 'cards', ids: fresh }); else fresh.forEach(id => r.q.push({ k: 'card', id })); }
      saveNow(); if (fresh.length) pump();
      return fresh;
    } finally { checking = false; if (recheck) { recheck = false; setTimeout(checkCards, 50); } }
  }

  /* ================= 🛡️ streak shield ================= */
  let inRepair = false;
  function repair() {                     // missed exactly one day + a shield → the shield bridges it (once)
    const s = STx(); if (!s || !s.profile || !s.streak || inRepair) return false;
    const r = R(), t = day(), last = s.streak.last;
    if (!last || !(s.streak.n > 0) || r.sh < 1 || last !== plus(t, -2)) return false;
    inRepair = true;
    try { r.sh--; s.streak.last = plus(t, -1); r.shSaved = [t, s.streak.n]; r.q.push({ k: 'saved', n: s.streak.n }); saveNow(); try { hud(); } catch (e) {} }
    finally { inRepair = false; }
    pump(); return true;
  }
  const _live = window.liveStreak, _bump = window.bumpStreak, _hud = window.hud;
  if (typeof _live === 'function') window.liveStreak = function () { try { repair(); } catch (e) {} return _live.apply(this, arguments); };
  if (typeof _bump === 'function') window.bumpStreak = function () {
    try { repair(); } catch (e) {}
    const s = STx(), before = s && s.streak && s.streak.last;
    const res = _bump.apply(this, arguments);
    try {
      const t = day();
      if (s && s.profile && before !== t && s.streak.last === t) {
        const r = R(), n = s.streak.n || 0;
        if (n > 0 && n % 7 === 0 && r.shDay !== t) { r.shDay = t; if (r.sh < MAX_SH) { r.sh++; r.q.push({ k: 'shield', n }); } saveNow(); markShield(); pump(); }
        setTimeout(checkCards, 60);
      }
    } catch (e) {}
    return res;
  };
  if (typeof _hud === 'function') window.hud = function () { const x = _hud.apply(this, arguments); markShield(); return x; };
  function markShield() {
    const b = D.getElementById('streakBtn'); if (!b) return; const s = STx(); const n = s && s.profile ? R().sh : 0;
    let m = D.getElementById('rwShMark');
    if (!n) { if (m) m.remove(); return; }
    if (!m) { b.insertAdjacentHTML('beforeend', '<span id="rwShMark" class="rw-shm"><span aria-hidden="true">🛡️</span><span class="sr-only"></span></span>'); m = D.getElementById('rwShMark'); }
    m.querySelector('.sr-only').textContent = `, ${n} streak shield${n > 1 ? 's' : ''}`;
    m.classList.toggle('two', n > 1);
  }
  function shieldHTML() {                  // section for the streak sheet (js/stars.js streak())
    const s = STx(); if (!s || !s.profile) return ''; const r = R(), n = r.sh, cur = typeof liveStreak === 'function' ? liveStreak() : (s.streak.n || 0), to7 = 7 - (cur % 7);
    const saved = r.shSaved && r.shSaved[0] && r.shSaved[0] >= plus(day(), -6) ? `<p class="st-small">🛡️ A shield saved your ${r.shSaved[1]}-day streak on ${new Date(r.shSaved[0] + 'T00:00:00Z').toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' })}.</p>` : '';
    return `<div class="rw-shbox" role="group" aria-label="Streak shields"><div class="rw-shtop"><b><span aria-hidden="true">🛡️</span> Streak shields</b><span class="rw-shn" aria-label="${n} of ${MAX_SH} shields">${'🛡️'.repeat(n)}${'<i>◯</i>'.repeat(MAX_SH - n)}</span></div>
      <p class="st-small">Every 7 days in a row earns a shield (you can hold ${MAX_SH}). Miss one day and a shield keeps your streak safe by itself.${n < MAX_SH ? ` Next shield: ${to7} more study day${to7 === 1 ? '' : 's'}.` : ''}</p>${saved}</div>`;
  }

  /* ================= 🎁 mystery box ================= */
  const GOAL = () => (window.Garden && Garden.GOAL) || 50;
  const goalHit = () => { const s = STx(); const d = s && s.daily; return !!(d && d.d === day() && (+d.xp || 0) >= GOAL()); };
  const boxWaiting = () => { const s = STx(); return !!(s && s.profile) && goalHit() && !((R().box || {}).d === day()); };
  const ACC = [['tophat', '🎩', 'Top hat'], ['crown', '👑', 'Crown'], ['shades', '🕶️', 'Cool shades'], ['gradcap', '🎓', 'Graduation cap'], ['bow', '🎀', 'Bow'], ['cap', '🧢', 'Cap'], ['flower', '🌸', 'Flower'], ['star', '🌟', 'Star clip']];
  const COLS = [['sunset', '#ff8a3d', 'Sunset orange'], ['ocean', '#2fa4ff', 'Ocean blue'], ['forest', '#2ecc71', 'Forest green'], ['royal', '#a066ff', 'Royal purple'], ['rose', '#ff6fa8', 'Rose pink'], ['gold', '#ffc93c', 'Gold']];
  const STK = [['unicorn', '🦄', 'Unicorn'], ['rainbow', '🌈', 'Rainbow'], ['pizza', '🍕', 'Pizza'], ['bike', '🚲', 'Bicycle'], ['guitar', '🎸', 'Guitar'], ['football', '⚽', 'Football'], ['cricket', '🏏', 'Cricket'], ['paint', '🎨', 'Paint'], ['sunflower', '🌻', 'Sunflower'], ['panda', '🐼', 'Panda'], ['melon', '🍉', 'Watermelon'], ['balloon', '🎈', 'Balloon']];
  function pickReward() {
    const r = R(), ca = isCA(), opts = [];
    const cards = album(ca).filter(c => ruleOf(c, ca)[0] === 'box' && !r.cards[c.id]);
    const acc = ACC.filter(a => !r.acc.includes(a[0])), col = ca ? [] : COLS.filter(c => !r.cols.includes(c[0])), stk = STK.filter(x => !r.stk.includes(x[0]));
    if (cards.length) opts.push(['card', 35, cards]); if (acc.length) opts.push(['acc', 20, acc]); if (col.length) opts.push(['col', 15, col]); if (stk.length) opts.push(['stk', 20, stk]);
    opts.push(['stars', 10]);
    let x = Math.random() * opts.reduce((a, o) => a + o[1], 0), o = opts[opts.length - 1];
    for (const y of opts) { if ((x -= y[1]) < 0) { o = y; break; } }
    if (o[0] === 'stars') return { k: 'stars', n: 10 };
    const it = o[2][Math.floor(Math.random() * o[2].length)];
    return o[0] === 'card' ? { k: 'card', id: it.id } : { k: o[0], id: it[0] };
  }
  function openBox(btn) {
    if (!boxWaiting()) return null;
    const r = R(), rw = pickReward();
    r.box = { d: day(), r: rw }; r.boxes++;                       // saved first: a box opens once, even if the app closes mid-animation
    if (rw.k === 'card') r.cards[rw.id] = day();
    else if (rw.k === 'acc') { r.acc.push(rw.id); if (!r.wear) r.wear = rw.id; }
    else if (rw.k === 'col') { r.cols.push(rw.id); r.mapc = rw.id; applyMap(); }
    else if (rw.k === 'stk') r.stk.push(rw.id);
    saveNow();
    if (rw.k === 'stars') { r.bonus = (+r.bonus || 0) + rw.n; saveNow(); try { addXP(rw.n); } catch (e) {} }
    S('open');
    const card = btn && btn.closest('.rw-box');
    const done = () => { r.q.unshift({ k: 'box', r: rw }); saveNow(); renderPractice(true); pump(); };
    if (card && !reduced()) { card.classList.add('rw-shake'); setTimeout(() => { card.classList.add('rw-open'); }, 650); setTimeout(done, 1000); } else done();
    return rw;
  }
  function rewardInfo(rw) {
    if (!rw) return null;
    if (rw.k === 'stars') return { e: '⭐', n: `${rw.n} bonus stars`, d: 'Added to your stars.' };
    if (rw.k === 'card') { const c = byId(rw.id); return c ? { e: c.e, n: c.n, d: 'A new card for your album!', card: c } : null; }
    const L = rw.k === 'acc' ? ACC : rw.k === 'col' ? COLS : STK, it = L.find(x => x[0] === rw.id); if (!it) return null;
    if (rw.k === 'acc') return { e: it[1], n: it[2], d: 'Your avatar is wearing it now. Change it in Me › My cards › My stuff.' };
    if (rw.k === 'col') return { e: '🎨', n: `${it[2]} map frame`, d: 'Your World map has a new frame colour.', col: it[1] };
    return { e: it[1], n: `${it[2]} sticker`, d: 'Added to your sticker book in Me.' };
  }
  function applyMap() {
    const s = STx(); const r = s && s.profile ? R() : {}; const c = !isCA() && COLS.find(x => x[0] === r.mapc);
    D.documentElement.classList.toggle('rw-mapc', !!c); if (c) D.documentElement.style.setProperty('--rw-map', c[1]); else D.documentElement.style.removeProperty('--rw-map');
  }

  /* ================= 👾 boss of the week ================= */
  const BOSSES = [['👾', 'Glitch the Quiz Bug'], ['🐉', 'Muddle the Dragon'], ['🦖', 'Forget-o-saurus'], ['🐙', 'Octo-Oops'], ['🤖', 'Robo-Riddle'], ['👻', 'Ghost of Mistakes'], ['🦑', 'Slip the Squid'], ['🦂', 'Tricky Scorpion']];
  const BOSSES_CA = [['📒', 'The Unbalanced Ledger'], ['👻', 'Ghost of the Missing Entry'], ['🐉', 'Depreciation Dragon'], ['🧙', 'Wrong-Side Wizard'], ['🦉', 'The Audit Owl'], ['🐙', 'Suspense Account Octopus']];
  const TRIES = 3, QN = 10;
  const need = n => Math.max(1, Math.min(7, Math.ceil(n * 0.7)));
  const wkIndex = wk => Math.floor(Date.parse(wk + 'T00:00:00Z') / (7 * 864e5));
  function boss() {
    const r = R(), wk = monday(day());
    if (!r.boss || r.boss.wk !== wk) r.boss = { wk, tries: 0, beaten: false, best: 0, qids: null };
    const L = isCA() ? BOSSES_CA : BOSSES, b = L[wkIndex(wk) % L.length];
    return Object.assign(r.boss, { e: b[0], name: b[1] });
  }
  function bossData(b) { const o = Object.assign({}, b); delete o.e; delete o.name; return o; }
  /* rough count of questions available without loading content (for the card's message) */
  function bossReady() {
    const s = STx(), b = boss(); if (b.qids && b.qids.length) return true;
    if (isCA()) { const c = s.ca || {}; const w = Object.values(c.mcq || {}).filter(x => x && x.w > 0).length; return w + Object.keys(c.units || {}).length * 3 >= 5; }
    const g = s.profile.grade, w = Object.keys(s.qstats || {}).filter(k => k.startsWith(`g${g}-`) && s.qstats[k].w > 0).length;
    return w + Object.keys(s.topics || {}).filter(k => k.startsWith(`g${g}-`)).length * 3 >= 5;
  }
  const okQ = q => q && typeof q.q === 'string' && Array.isArray(q.options) && q.options.length >= 2 && q.options.length <= 5 && Number.isInteger(+q.answer) && q.answer >= 0 && q.answer < q.options.length;
  async function schoolQs(keys) {
    const s = STx(), g = s.profile.grade, idx = {};
    for (const x of curSubjects(g)) { const d = await subjectData(g, x.id); if (d && d.chapters) d.chapters.forEach(c => c.topics.forEach(t => { idx[t.id] = t; })); }
    const get = k => { const [tid, i] = k.split('#'), t = idx[tid], q = t && t.quiz && t.quiz[+i]; return okQ(q) ? { q, key: k, ca: false } : null; };
    if (keys) return keys.map(get).filter(Boolean);
    const out = [], seen = new Set(), add = k => { if (out.length >= QN || seen.has(k)) return; const x = get(k); if (x) { seen.add(k); out.push(x); } };
    const st = s.qstats || {};
    Object.keys(st).filter(k => k.startsWith(`g${g}-`) && st[k].w > 0).sort((a, b) => (st[b].w * 2 - st[b].s * .5) - (st[a].w * 2 - st[a].s * .5)).forEach(add);
    const recent = Object.entries(s.topics || {}).filter(([id]) => idx[id]).sort((a, b) => String(b[1].last || '').localeCompare(String(a[1].last || ''))).map(([id]) => id);
    for (let round = 0; out.length < QN && round < 4; round++) recent.forEach(id => { const t = idx[id]; const ks = shuffle(t.quiz.map((q, i) => `${id}#${i}`)).filter(k => !seen.has(k)); if (ks[0]) add(ks[0]); });
    return out;
  }
  async function caQs(keys) {
    const X = window.Ca && Ca._; if (!X || !X.unitData) return [];
    const c = X.C(), cache = {};
    const unit = async uid => { if (!(uid in cache)) { try { cache[uid] = await X.unitData(uid); } catch (e) { cache[uid] = null; } } return cache[uid]; };
    const get = async k => { const [uid, qid] = k.split('#'), d = await unit(uid), q = d && (d.mcqs || []).find(x => String(x.id) === qid); return okQ(q) ? { q, key: k, ca: true } : null; };
    if (keys) { const out = []; for (const k of keys) { const x = await get(k); if (x) out.push(x); } return out; }
    const out = [], seen = new Set(), add = async k => { if (out.length >= QN || seen.has(k)) return; seen.add(k); const x = await get(k); if (x) out.push(x); };
    const m = c.mcq || {};
    for (const k of Object.keys(m).filter(k => m[k] && m[k].w > 0).sort((a, b) => (m[b].w * 2 - m[b].s * .5) - (m[a].w * 2 - m[a].s * .5))) { if (out.length >= QN) break; await add(k); }
    const recent = Object.entries(c.units || {}).sort((a, b) => String((b[1] || {}).t || '').localeCompare(String((a[1] || {}).t || ''))).map(([id]) => id).slice(0, 6);
    for (let round = 0; out.length < QN && round < 4; round++) for (const uid of recent) { const d = await unit(uid); const ks = shuffle(((d && d.mcqs) || []).map(q => `${uid}#${q.id}`)).filter(k => !seen.has(k)); if (ks[0]) await add(ks[0]); }
    return out;
  }
  async function bossList() {
    const b = boss(), ca = isCA();
    if (b.qids && b.qids.length) { const l = ca ? await caQs(b.qids) : await schoolQs(b.qids); if (l.length >= 5) return l; }
    const l = ca ? await caQs() : await schoolQs();
    if (l.length >= 5) { b.qids = l.map(x => x.key); saveNow(); }
    return l;
  }
  function bossScreen() {
    let s = D.getElementById('s-boss');
    if (!s) { $1('main').insertAdjacentHTML('beforeend', '<section class="screen" id="s-boss" aria-label="Boss of the week"></section>'); s = D.getElementById('s-boss'); }
    return s;
  }
  const backToPractice = () => { if (isCA() && window.CaTools) CaTools.practiceHub(); else practiceScreen(); };
  async function startBoss() {
    const b = boss();
    if (b.beaten) { toast('You already beat this week’s boss! 🏆'); return; }
    if (b.tries >= TRIES) { toast('No tries left this week. A new boss comes on Monday!'); return; }
    style(); const el = bossScreen(); show('boss', 'practice'); window.scrollTo(0, 0);
    el.innerHTML = '<div class="card"><p class="sub" role="status">Waking up the boss…</p></div>';
    const list = await bossList();
    if (list.length < 5) { el.innerHTML = `<button class="back" id="rwBkB">← Practice</button><div class="card"><h2>${b.e} The boss is asleep</h2><p class="sub">${isCA() ? 'Answer a few MCQs in your units first' : 'Finish a quest first'} — then the boss can use your tricky questions.</p><button class="btn" id="rwBkGo">${isCA() ? 'Go to CA Journey ▶' : 'Go to my world ▶'}</button></div>`;
      $1('#rwBkB').onclick = backToPractice; $1('#rwBkGo').onclick = () => (isCA() && window.Ca ? Ca.home() : worldScreen()); return; }
    runBoss(el, shuffle(list));
  }
  function runBoss(el, list) {
    const b = boss(), ca = isCA(), N = list.length, NEED = need(N);
    let i = 0, right = 0, counted = false, shownAt = Date.now(); const orders = list.map(x => shuffle(x.q.options.map((o, k) => k))), hist = [];
    const hp = () => Math.max(0, NEED - right);
    const top = () => `<div class="rw-bhead"><span class="rw-bemo" id="rwBemo" aria-hidden="true">${b.e}</span><div class="rw-bhp"><b>${E(b.name)}</b>
        <div class="rw-hpbar" role="progressbar" aria-label="Boss health" aria-valuemin="0" aria-valuemax="${NEED}" aria-valuenow="${hp()}"><i style="width:${hp() / NEED * 100}%"></i></div>
        <small>Boss health ${hp()} / ${NEED} · try ${Math.min(TRIES, b.tries + (counted ? 0 : 1))} of ${TRIES}</small></div></div>`;
    const render = () => {
      const x = list[i], q = x.q, ord = orders[i];
      el.innerHTML = `<button class="back" id="rwBkB">← Practice</button><div class="card rw-bcard">${top()}<div class="sr-only" aria-live="polite" id="rwBlive"></div>
        <span class="tag">Question ${i + 1} of ${N}</span><h2 class="qtext">${E(q.q)}</h2>
        <div id="rwQo">${ord.map(k => `<button class="opt" data-k="${k}">${E(q.options[k])}</button>`).join('')}</div><div id="rwQx"></div>
        <div class="rw-bnav" id="rwBnav"></div></div>`;
      $1('#rwBkB').onclick = () => { S('tap'); backToPractice(); };
      shownAt = Date.now();
      el.querySelectorAll('#rwQo .opt').forEach(btn => btn.onclick = () => answer(+btn.dataset.k));
      window.scrollTo(0, 0);
    };
    const answer = k => {
      if (hist[i]) return; const x = list[i], q = x.q, ok = k === +q.answer; hist[i] = { k, ok };
      if (!counted) { counted = true; b.tries++; saveNow(); }
      const secs = (Date.now() - shownAt) / 1000;
      try {
        if (ca) { if (window.Ca && Ca._ && Ca._.recordAns) Ca._.recordAns(x.key, ok, secs * 1000, q); }
        else { const s = STx(), st = s.qstats[x.key] || { s: 0, w: 0 }; st.s++; if (!ok) { st.w++; if (q.mistake) s.mistakes[q.mistake] = (s.mistakes[q.mistake] || 0) + 1; } s.qstats[x.key] = st;
          if (typeof logAns === 'function') logAns(x.key, ok, secs); saveNow(); }
      } catch (e) {}
      if (ok) { right++; S('correct'); if (!ca) try { addXP(10); } catch (e) {} } else S('wrong');
      el.querySelectorAll('#rwQo .opt').forEach(o => { o.disabled = true; const kk = +o.dataset.k; if (kk === +q.answer) o.classList.add('right'); else if (kk === k) o.classList.add('wrong'); });
      const h = el.querySelector('.rw-bhead'); if (h) h.outerHTML = top();
      const em = D.getElementById('rwBemo'); if (em && ok && !reduced()) { em.classList.add('rw-hit'); }
      $1('#rwBlive').textContent = ok ? `Hit! Boss health ${hp()} of ${NEED}.` : `Missed. Boss health ${hp()} of ${NEED}.`;
      $1('#rwQx').innerHTML = `<div class="explain ${ok ? 'good' : 'bad'}"><div class="verdict">${ok ? (hp() ? '💥 Hit! Correct!' : '💥 Final hit!') : `🤔 Not quite — it's <b>${E(q.options[q.answer])}</b>`}</div>${q.explain ? `<div class="why">${E(q.explain)}</div>` : ''}</div>`;
      $1('#rwBnav').innerHTML = `<button class="btn mint" id="rwNx">${i < N - 1 ? 'Next ▶' : 'See result ▶'}</button>`;
      $1('#rwNx').onclick = () => { if (i < N - 1) { i++; render(); } else finish(); };
      setTimeout(() => { const q2 = $1('#rwQx'); if (q2 && q2.scrollIntoView) q2.scrollIntoView({ behavior: reduced() ? 'auto' : 'smooth', block: 'nearest' }); }, 100);
    };
    const finish = () => {
      const r = R(), win = right >= NEED; b.best = Math.max(b.best || 0, right);
      let card = null;
      if (win && !b.beaten) {
        b.beaten = true; r.bossWins++; r.bossLog.push(b.wk); if (r.bossLog.length > 60) r.bossLog.shift();
        try { const s = STx(); s.badges = s.badges || {}; if (!s.badges.boss) s.badges.boss = day(); } catch (e) {}
        const pick = album(ca).filter(c => ruleOf(c, ca)[0] === 'boss' && !r.cards[c.id]).sort((a, c) => ruleOf(a, ca)[1] - ruleOf(c, ca)[1])[0];
        if (pick) { r.cards[pick.id] = day(); card = pick; }
        r.q.unshift({ k: 'boss', name: b.name, e: b.e, card: card && card.id });
      }
      saveNow();
      try { if (ca) addXP(Math.max(5, right * 2)); } catch (e) {}
      try { bumpStreak(); } catch (e) {}
      const left = TRIES - b.tries;
      S(win ? 'unlock' : 'hmm');
      el.innerHTML = `<button class="back" id="rwBkB">← Practice</button><div class="card done-card rw-bres"><div class="rw-bbig" aria-hidden="true">${win ? '🏆' : b.e}</div>
        <h2>${win ? `You beat ${E(b.name)}!` : `${E(b.name)} got away!`}</h2><p class="sub">${right} of ${N} right · you needed ${NEED}.</p>
        <p class="sub">${win ? 'You earned the 👾 Boss badge' + (card ? ' and an epic card' : '') + '. A new boss arrives on Monday.' : left > 0 ? `You have ${left} ${left === 1 ? 'try' : 'tries'} left this week. Each question you got wrong is a chance to learn it.` : 'No tries left this week — a new boss arrives on Monday. Keep practising!'}</p>
        <button class="btn" id="rwBdone">Back to Practice</button></div>`;
      $1('#rwBkB').onclick = backToPractice; $1('#rwBdone').onclick = () => { S('tap'); backToPractice(); };
      pump(); setTimeout(checkCards, 100);
    };
    render();
  }

  /* ================= Practice cards ================= */
  function boxHTML() {
    return `<div class="card rw-box" id="rwBox"><div class="rw-boxrow"><span class="rw-gift" aria-hidden="true">🎁</span><div><h3>Mystery box</h3><p class="sub">You reached today’s goal! A free surprise is waiting.</p></div></div>
      <button class="btn" type="button" id="rwBoxOpen" aria-label="Open today's mystery box">Open my box ✨</button></div>`;
  }
  function bossHTML() {
    const b = boss(), left = TRIES - b.tries, ready = bossReady();
    const msg = b.beaten ? 'Beaten this week! 🏆 A new boss arrives on Monday.' : !ready ? (isCA() ? 'Answer some MCQs in your units — the boss is made from the ones you find tricky.' : 'Finish a quest — the boss is made from the questions you find tricky.')
      : left <= 0 ? 'No tries left this week. A new boss arrives on Monday.' : `10 of your trickiest questions. Get 7 right to win. ${left} ${left === 1 ? 'try' : 'tries'} left this week.`;
    const btn = b.beaten || left <= 0 ? '' : ready ? `<button class="btn${isCA() ? '' : ' mint'}" type="button" id="rwBossGo">${b.tries ? 'Fight again ⚔️' : 'Fight the boss ⚔️'}</button>` : `<button class="btn ghost" type="button" id="rwBossWake">${isCA() ? 'Go to CA Journey ▶' : 'Start a quest ▶'}</button>`;
    return `<div class="card rw-boss${b.beaten ? ' won' : ''}" id="rwBoss"><div class="rw-boxrow"><span class="rw-bemo2" aria-hidden="true">${b.beaten ? '🏆' : b.e}</span><div><span class="tag">Boss of the week</span><h3>${E(b.name)}</h3><p class="sub">${msg}</p></div></div>${btn}</div>`;
  }
  function wirePractice() {
    const o = D.getElementById('rwBoxOpen'); if (o) o.onclick = () => openBox(o);
    const g = D.getElementById('rwBossGo'); if (g) g.onclick = () => { S('open'); startBoss(); };
    const w = D.getElementById('rwBossWake'); if (w) w.onclick = () => { S('tap'); if (isCA() && window.Ca) Ca.home(); else worldScreen(); };
  }
  /* host + anchor: school = right after Today's goal; CA = top of the practice tiles. Our cards always sit before 🎮 Play. */
  function practiceHost() {
    const p = D.getElementById('s-practice');
    if (!isCA() && p && p.classList.contains('active')) { const g = p.querySelector(':scope > .goalcard'); if (g) return { host: p, after: g }; }
    const c = D.getElementById('s-ca');
    if (isCA() && c && c.classList.contains('active')) { const h = c.querySelector(':scope > .ca-hubs'); if (h) return { host: h, after: null }; }
    return null;
  }
  function renderPractice(force) {
    const at = practiceHost(); if (!at) return;
    const { host, after } = at;
    const bx = host.querySelector(':scope > #rwBox'), bs = host.querySelector(':scope > #rwBoss'), want = boxWaiting();
    const play = host.querySelector(':scope > #phTile'), first = want ? bx : bs;
    const ok = !force && bs && !!bx === want && (!want || bx.nextElementSibling === bs)
      && (after ? after.nextElementSibling === first : host.firstElementChild === first) && (!play || bs.nextElementSibling === play);
    if (ok) return;
    if (bx) bx.remove(); if (bs) bs.remove();
    const html = (want ? boxHTML() : '') + bossHTML();
    if (play) play.insertAdjacentHTML('beforebegin', html);
    else if (after) after.insertAdjacentHTML('afterend', html);
    else host.insertAdjacentHTML('afterbegin', html);
    wirePractice();
  }

  /* ================= Me: 🃏 My cards + album ================= */
  function meHTML() {
    const r = R(), ca = isCA(), al = album(ca), have = al.filter(c => r.cards[c.id]);
    const recent = have.slice().sort((a, b) => String(r.cards[b.id]).localeCompare(String(r.cards[a.id]))).slice(0, 6);
    const extras = [r.boxes ? `🎁 ${r.boxes} ${r.boxes === 1 ? 'box' : 'boxes'} opened` : '', r.bossWins ? `👾 ${r.bossWins} ${r.bossWins === 1 ? 'boss' : 'bosses'} beaten` : '', r.sh ? `🛡️ ${r.sh} shield${r.sh > 1 ? 's' : ''}` : ''].filter(Boolean);
    return `<div class="card rw-me" id="rwMe"><div class="rw-meh"><h3><span aria-hidden="true">🃏</span> My cards</h3><b>${have.length} / ${al.length}</b></div>
      <div class="rw-mebar" role="progressbar" aria-label="Cards collected" aria-valuemin="0" aria-valuemax="${al.length}" aria-valuenow="${have.length}"><i style="width:${al.length ? have.length / al.length * 100 : 0}%"></i></div>
      ${recent.length ? `<div class="rw-merow" aria-label="Latest cards: ${E(recent.map(c => c.n).join(', '))}">${recent.map(c => `<span class="rw-mini r-${c.r}" aria-hidden="true">${c.e}</span>`).join('')}</div>` : `<p class="sub">${ca ? 'Finish unit steps, keep your streak and open mystery boxes to collect cards.' : 'Get ⭐⭐⭐ in a quest, finish chapters, keep your streak and open mystery boxes to collect cards.'}</p>`}
      ${extras.length ? `<p class="sub rw-mex">${extras.join(' · ')}</p>` : ''}
      <button class="btn" type="button" id="rwMeOpen">Open my album ▶</button></div>`;
  }
  function renderMe() {
    const m = D.getElementById(isCA() ? 's-ca' : 's-me'); if (!m || !m.classList.contains('active')) return;
    const prof = m.querySelector(isCA() ? ':scope > .ca-prof' : ':scope > .mecard'); if (!prof) return;
    const anc = prof.nextElementSibling && prof.nextElementSibling.matches('.sv-planbar') ? prof.nextElementSibling : prof;   // js/plans.js keeps its plan strip right under the profile
    if (!m.querySelector(':scope > #rwMe')) { anc.insertAdjacentHTML('afterend', meHTML()); D.getElementById('rwMeOpen').onclick = () => { S('open'); openAlbum(); }; }
    else if (!anc.nextElementSibling || anc.nextElementSibling.id !== 'rwMe') anc.insertAdjacentElement('afterend', m.querySelector(':scope > #rwMe'));
    const av = prof.querySelector('.meav, .ca-avatar'), r = R(), a = ACC.find(x => x[0] === r.wear);
    if (av) { let w = av.querySelector('.rw-wear'); if (!a) { if (w) w.remove(); } else { av.classList.add('rw-avw'); if (!w) { av.insertAdjacentHTML('beforeend', '<span class="rw-wear" aria-hidden="true"></span>'); w = av.querySelector('.rw-wear'); } if (w.textContent !== a[1]) w.textContent = a[1]; } }
  }
  function cardHTML(c, owned, ca) {
    const st = SETS.find(s => s.id === c.set);
    if (!owned) return `<div class="rw-cd locked r-${c.r}" role="listitem"><div class="rw-in"><div class="rw-face rw-front"><span class="rw-ce sil" aria-hidden="true">${c.e}</span><span class="rw-lock" aria-hidden="true">🔒</span><small class="rw-how">${E(howTo(c, ca))}</small><span class="sr-only">Locked ${RAR[c.r].toLowerCase()} card. How to unlock: ${E(howTo(c, ca))}</span></div></div></div>`;
    return `<div class="rw-cd r-${c.r}" role="listitem"><button type="button" class="rw-in" data-cid="${c.id}" aria-pressed="false" aria-label="${E(c.n)}, ${RAR[c.r]} card. Tap to flip." style="--sc:${st.col}">
      <span class="rw-face rw-front"><span class="rw-rar">${RAR[c.r]}</span><span class="rw-ce" aria-hidden="true">${c.e}</span><b>${E(c.n)}</b></span>
      <span class="rw-face rw-back"><b>${E(c.n)}</b><span class="rw-txt">${E(c.t)}</span></span></button></div>`;
  }
  function stuffHTML() {
    const r = R(), ca = isCA();
    const acc = ACC.filter(a => r.acc.includes(a[0])), col = COLS.filter(c => r.cols.includes(c[0])), stk = STK.filter(s => r.stk.includes(s[0]));
    if (!acc.length && !col.length && !stk.length && !r.bossWins && !r.bonus) return `<div class="card"><h3><span aria-hidden="true">🎒</span> My stuff</h3><p class="sub">Reach today’s goal to get a free 🎁 mystery box: hats, ${ca ? '' : 'map colours, '}stickers and cards are inside.</p></div>`;
    return `<div class="card rw-stuff"><h3><span aria-hidden="true">🎒</span> My stuff</h3>
      ${acc.length ? `<h4>Avatar accessories <small>tap to wear</small></h4><div class="rw-chips">${acc.map(a => `<button type="button" class="rw-chip${r.wear === a[0] ? ' on' : ''}" data-wear="${a[0]}" aria-pressed="${r.wear === a[0]}"><span aria-hidden="true">${a[1]}</span> ${E(a[2])}</button>`).join('')}</div>` : ''}
      ${col.length && !ca ? `<h4>Map frame colours <small>tap to use</small></h4><div class="rw-chips">${col.map(c => `<button type="button" class="rw-chip${r.mapc === c[0] ? ' on' : ''}" data-mapc="${c[0]}" aria-pressed="${r.mapc === c[0]}"><i class="rw-dot" style="background:${c[1]}" aria-hidden="true"></i> ${E(c[2])}</button>`).join('')}</div>` : ''}
      ${stk.length ? `<h4>Stickers</h4><div class="rw-stk" role="list">${stk.map(s => `<span role="listitem" title="${E(s[2])}"><span aria-hidden="true">${s[1]}</span><span class="sr-only">${E(s[2])}</span></span>`).join('')}</div>` : ''}
      ${r.bossWins ? `<h4>Badges</h4><div class="rw-chips"><span class="rw-chip on"><span aria-hidden="true">👾</span> Boss beaten ×${r.bossWins}</span></div>` : ''}
      ${r.bonus ? `<p class="sub">⭐ ${r.bonus} bonus stars from boxes</p>` : ''}</div>`;
  }
  function albumScreen() {
    let s = D.getElementById('s-cards');
    if (!s) { $1('main').insertAdjacentHTML('beforeend', '<section class="screen" id="s-cards" aria-label="My cards"></section>'); s = D.getElementById('s-cards'); }
    return s;
  }
  function openAlbum() {
    style(); checkCards();
    const el = albumScreen(), r = R(), ca = isCA(); show('cards', 'me'); window.scrollTo(0, 0);
    const al = album(ca), have = al.filter(c => r.cards[c.id]).length;
    el.innerHTML = `<button class="back" id="rwAbB">← ${ca ? 'Profile' : 'Me'}</button>
      <div class="card"><h2><span aria-hidden="true">🃏</span> My cards</h2><p class="sub">${have} of ${al.length} collected. Tap a card to flip it. Grey cards show how to unlock them.</p>
        <p class="rw-key"><span class="rw-k r-c">Common</span><span class="rw-k r-r">Rare</span><span class="rw-k r-e">Epic</span></p></div>
      ${stuffHTML()}
      ${setsFor(ca).map(st => { const cs = al.filter(c => c.set === st.id), n = cs.filter(c => r.cards[c.id]).length;
        return `<div class="card rw-set"><h3><span aria-hidden="true">${st.e}</span> ${E(st.n)} <small>${n} / ${cs.length}</small></h3><div class="rw-grid" role="list">${cs.map(c => cardHTML(c, !!r.cards[c.id], ca)).join('')}</div></div>`; }).join('')}`;
    $1('#rwAbB').onclick = () => { S('tap'); meScreen(); };
    el.querySelectorAll('[data-cid]').forEach(b => b.onclick = () => { const on = !b.classList.contains('flip'); b.classList.toggle('flip', on); b.setAttribute('aria-pressed', on); S('tap'); });
    el.querySelectorAll('[data-wear]').forEach(b => b.onclick = () => { const id = b.dataset.wear; r.wear = r.wear === id ? null : id; saveNow(); S('tap'); toast(r.wear ? 'Looking great! 😎' : 'Accessory off'); openAlbum(); });
    el.querySelectorAll('[data-mapc]').forEach(b => b.onclick = () => { const id = b.dataset.mapc; r.mapc = r.mapc === id ? null : id; saveNow(); applyMap(); S('tap'); toast(r.mapc ? 'New map frame colour 🎨' : 'Map frame colour off'); openAlbum(); });
  }

  /* ================= one celebration sheet, one at a time ================= */
  let cel = null, showing = null, opener = null;
  function celSheet() {
    if (cel) return cel; style();
    cel = D.createElement('div'); cel.className = 'sheet rw-cel'; cel.id = 'rwCel'; cel.setAttribute('role', 'dialog'); cel.setAttribute('aria-modal', 'true'); cel.setAttribute('aria-labelledby', 'rwCelT');
    cel.innerHTML = '<div class="sheet-in"><div class="sheet-grab"></div><div id="rwCelBody"></div></div>';
    cel.addEventListener('keydown', e => { if (e.key === 'Escape') { e.stopPropagation(); closeCel(); } });
    D.body.appendChild(cel); return cel;
  }
  const busy = () => {
    if (D.querySelector('.sheet.show:not(#rwCel),.asksheet.show')) return true;
    const a = D.querySelector('.screen.active'); if (!a || a.id === 's-onboard') return true;
    if (a.querySelector('.opt, .lv-opt, .qtext')) return true;          // inside a quiz (also between questions): wait until it ends
    if (D.getElementById('svGate')) return true;
    return false;
  };
  function celHTML(it) {
    const s = STx();
    if (it.k === 'saved') return { t: `Your 🛡️ shield saved your ${it.n}-day streak!`, b: `You missed a day, so a shield kept your 🔥 streak safe. Study today to make it ${it.n + 1}!`, e: '🛡️' };
    if (it.k === 'shield') return { t: '🛡️ Streak shield earned!', b: `${it.n} days in a row — amazing! If you ever miss one day, this shield keeps your streak safe by itself. You have ${R().sh} of ${MAX_SH}.`, e: '🛡️' };
    if (it.k === 'card') { const c = byId(it.id); if (!c) return null; return { t: 'New card unlocked!', card: c }; }
    if (it.k === 'cards') { const cs = (it.ids || []).map(byId).filter(Boolean); if (!cs.length) return null; return { t: `${cs.length} new card${cs.length > 1 ? 's' : ''} unlocked!`, b: 'For all your learning so far. See them in Me › My cards.', many: cs }; }
    if (it.k === 'box') { const x = rewardInfo(it.r); if (!x) return null; return x.card ? { t: '🎁 Your mystery box had…', card: x.card } : { t: '🎁 Your mystery box had…', e: x.e, sub: x.n, b: x.d, col: x.col }; }
    if (it.k === 'boss') { const c = it.card && byId(it.card); return { t: `You beat ${it.name}! 🏆`, b: `You earned the 👾 Boss badge${c ? ' and an epic card' : ''}. See you next Monday!`, e: '👾', card: c || null }; }
    return null;
  }
  function pump() {
    const s = STx(); if (!s || !s.profile || showing || isParent()) return;
    const r = R(); if (!r.q.length) return;
    if (busy()) return;
    const it = r.q[0], h = celHTML(it); if (!h) { r.q.shift(); saveNow(); return pump(); }
    const sh = celSheet(); showing = it; opener = D.activeElement;
    const c = h.card;
    sh.querySelector('#rwCelBody').innerHTML = `<div class="rw-celin">${c ? `<div class="rw-celcard r-${c.r}" style="--sc:${(SETS.find(x => x.id === c.set) || {}).col}"><span class="rw-rar">${RAR[c.r]}</span><span class="rw-ce" aria-hidden="true">${c.e}</span><b>${E(c.n)}</b><span class="rw-txt">${E(c.t)}</span></div>`
        : h.many ? `<div class="rw-many" aria-hidden="true">${h.many.slice(0, 8).map(x => `<span class="rw-mini r-${x.r}">${x.e}</span>`).join('')}</div>`
        : `<div class="rw-celbig" aria-hidden="true"${h.col ? ` style="color:${h.col}"` : ''}>${h.e}</div>`}
      <h2 id="rwCelT" tabindex="-1">${E(h.t)}</h2>${h.sub ? `<p class="rw-celsub">${E(h.sub)}</p>` : ''}${h.b ? `<p class="sub">${E(h.b)}</p>` : ''}
      <div class="rw-celbtns">${it.k === 'card' || it.k === 'cards' || (it.k === 'box' && (it.r || {}).k === 'card') || (it.k === 'boss' && c) ? '<button class="btn ghost" type="button" id="rwCelAlb">See my album</button>' : ''}<button class="btn" type="button" data-close id="rwCelOk">Yay! 🎉</button></div></div>`;
    sh.classList.add('show'); S('unlock');
    $1('#rwCelOk', sh).onclick = closeCel;
    const al = $1('#rwCelAlb', sh); if (al) al.onclick = () => { closeCel(); openAlbum(); };
    setTimeout(() => { const f = sh.querySelector('#rwCelT'); if (f) f.focus(); }, 40);
  }
  function closeCel() {
    if (!cel) return; cel.classList.remove('show');
    const r = R(), i = showing ? r.q.indexOf(showing) : -1; if (i >= 0) { r.q.splice(i, 1); saveNow(); }
    showing = null;
    try { if (opener && opener.focus && D.contains(opener)) opener.focus(); } catch (e) {}
    setTimeout(pump, 450);
  }

  /* ================= style ================= */
  let css = false;
  function style() {
    if (css) return; css = true;
    const st = D.createElement('style'); st.id = 'rwCss';
    st.textContent = `
.rw-shm{display:inline-block;font-size:11px;margin-left:2px;vertical-align:top;line-height:1}.rw-shm.two::after{content:'2';font-size:9px;font-weight:900}
.rw-shbox{background:#eef6ff;border-radius:14px;padding:10px 12px;margin:10px 0}.rw-shtop{display:flex;justify-content:space-between;align-items:center;gap:8px}
.rw-shn{font-size:20px;letter-spacing:2px}.rw-shn i{font-style:normal;color:#b8c2d8;font-size:16px}
.rw-boxrow{display:flex;gap:12px;align-items:center;margin-bottom:10px}.rw-boxrow h3{margin:0}.rw-boxrow p.sub{margin:2px 0 0}.rw-boxrow .tag{margin-bottom:2px}
.rw-gift,.rw-bemo2{font-size:44px;line-height:1;flex:none;width:52px;text-align:center}
.rw-box{background:linear-gradient(135deg,#fff7d6,#ffe9f3)}
.rw-box .rw-gift{animation:rwBob 1.6s ease-in-out infinite}
@keyframes rwBob{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-4px) rotate(-6deg)}}
.rw-shake .rw-gift{animation:rwShake .6s linear}
@keyframes rwShake{0%,100%{transform:rotate(0)}15%{transform:rotate(-18deg) scale(1.1)}30%{transform:rotate(16deg) scale(1.15)}45%{transform:rotate(-14deg) scale(1.2)}60%{transform:rotate(12deg) scale(1.25)}80%{transform:rotate(-6deg) scale(1.3)}}
.rw-open .rw-gift{transform:scale(1.8);opacity:0;transition:transform .3s ease-out,opacity .3s}
.rw-boss{background:linear-gradient(135deg,#f1edff,#e7f0ff)}.rw-boss.won{background:linear-gradient(135deg,#e6fbf2,#fff8e1)}
.rw-bhead{display:flex;gap:12px;align-items:center;margin-bottom:10px}.rw-bemo{font-size:50px;line-height:1;flex:none}.rw-bhp{flex:1;min-width:0}.rw-bhp b{display:block;font-size:16px}.rw-bhp small{color:var(--muted);font-size:12.5px;font-weight:700}
.rw-hpbar{height:14px;border-radius:9px;background:#ffe1e1;overflow:hidden;margin:4px 0 2px;border:2px solid #ffb4b4}.rw-hpbar i{display:block;height:100%;background:linear-gradient(90deg,#ff6b6b,#ff9f43);border-radius:7px;transition:width .5s ease}
.rw-hit{animation:rwHit .5s ease}@keyframes rwHit{0%,100%{transform:none}20%{transform:translateX(-8px) rotate(-8deg);filter:brightness(1.6)}50%{transform:translateX(8px) rotate(8deg)}75%{transform:translateX(-4px)}}
.rw-bnav{margin-top:12px}.rw-bbig{font-size:64px;line-height:1.1}.rw-bres h2{margin:6px 0}
.rw-meh{display:flex;justify-content:space-between;align-items:center}.rw-meh h3{margin:0}.rw-meh b{font-size:15px;color:var(--violet,#7c4dff)}
.rw-mebar{height:10px;border-radius:9px;background:#eef0fb;overflow:hidden;margin:8px 0 10px}.rw-mebar i{display:block;height:100%;background:linear-gradient(90deg,#7c4dff,#2ed3a5);border-radius:9px}
.rw-merow{display:flex;gap:6px;margin-bottom:8px;flex-wrap:wrap}.rw-mex{margin:0 0 10px}
.rw-mini{display:inline-flex;align-items:center;justify-content:center;width:40px;height:52px;border-radius:9px;background:#f4f1ff;font-size:24px;border:2px solid #cfd5ea}
.rw-mini.r-r,.rw-k.r-r{border-color:#3b82f6}.rw-mini.r-e,.rw-k.r-e{border-color:#a855f7;box-shadow:0 0 0 2px #fde68a}
.rw-avw{position:relative}.meav.rw-avw{display:inline-block}.rw-wear{position:absolute;top:-14px;right:-12px;font-size:.55em;transform:rotate(12deg);line-height:1}.ca-avatar .rw-wear{font-size:22px;top:-12px;right:-10px}
.rw-key{display:flex;gap:8px;margin:0}.rw-k{font-size:12px;font-weight:800;border:2px solid #cfd5ea;border-radius:999px;padding:2px 10px}
.rw-set h3 small{color:var(--muted);font-size:13px;font-weight:800}
.rw-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:8px}
.rw-cd{perspective:700px;min-width:0}
.rw-in{position:relative;display:block;width:100%;aspect-ratio:3/4;min-height:132px;border:none;padding:0;background:none;cursor:pointer;font-family:inherit;color:var(--ink);transform-style:preserve-3d;transition:transform .5s cubic-bezier(.3,.9,.4,1.1)}
.rw-in.flip{transform:rotateY(180deg)}
.rw-face{position:absolute;inset:0;border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:8px 6px;text-align:center;backface-visibility:hidden;-webkit-backface-visibility:hidden;background:#fff;border:3px solid #cfd5ea;overflow:hidden}
.rw-front{background:linear-gradient(160deg,#fff 40%,color-mix(in srgb,var(--sc,#7c4dff) 22%,#fff))}
.rw-back{transform:rotateY(180deg);justify-content:flex-start;background:#fffdf4}
.rw-face b{font-size:12.5px;line-height:1.15}.rw-txt{font-size:11.5px;line-height:1.3;font-weight:600;color:#3b4060;overflow:auto}
.rw-ce{font-size:38px;line-height:1.1}.rw-ce.sil{filter:grayscale(1) brightness(0);opacity:.18}
.rw-rar{position:absolute;top:5px;left:6px;font-size:9.5px;font-weight:900;text-transform:uppercase;letter-spacing:.4px;color:#6b7194}
.r-r .rw-face{border-color:#3b82f6}.r-r .rw-rar{color:#2563eb}
.r-e .rw-face{border-color:#a855f7;box-shadow:inset 0 0 0 2px #fde68a}.r-e .rw-rar{color:#9333ea}
.rw-cd.locked .rw-face{background:#f1f2f7;border-style:dashed;border-color:#c5c9db;box-shadow:none}
.rw-cd.locked .rw-in{cursor:default}.rw-lock{font-size:14px;opacity:.7}.rw-how{font-size:11px;line-height:1.25;color:#555b7a;font-weight:700}
.rw-stuff h4{margin:10px 0 6px;font-size:14px}.rw-stuff h4 small{color:var(--muted);font-weight:700;font-size:12px}
.rw-chips{display:flex;flex-wrap:wrap;gap:6px}.rw-chip{border:2px solid #e3e6f6;background:#fff;border-radius:999px;padding:7px 12px;font-family:inherit;font-weight:800;font-size:13.5px;cursor:pointer;color:var(--ink);min-height:40px;display:inline-flex;align-items:center;gap:4px}
.rw-chip.on{border-color:var(--violet,#7c4dff);background:#f1edff}.rw-dot{display:inline-block;width:16px;height:16px;border-radius:50%}
.rw-stk{display:flex;flex-wrap:wrap;gap:8px;font-size:30px}
.rw-cel .sheet-in{text-align:center;max-height:90vh;overflow-y:auto}.rw-cel h2{margin:8px 0 4px;font-size:22px}.rw-cel h2:focus{outline:none}
.rw-celbig{font-size:72px;line-height:1.1;animation:rwPop .5s cubic-bezier(.2,1.6,.4,1)}
.rw-celsub{font-weight:800;font-size:17px;margin:2px 0}
.rw-celcard{position:relative;width:190px;margin:4px auto 6px;border-radius:18px;border:4px solid #cfd5ea;padding:24px 12px 14px;display:flex;flex-direction:column;align-items:center;gap:6px;background:linear-gradient(160deg,#fff 40%,color-mix(in srgb,var(--sc,#7c4dff) 25%,#fff));animation:rwFlipIn .7s ease}
.rw-celcard.r-r{border-color:#3b82f6}.rw-celcard.r-e{border-color:#a855f7;box-shadow:0 0 0 4px #fde68a,0 0 26px #fde68a}
.rw-celcard .rw-ce{font-size:60px}.rw-celcard b{font-size:16px}.rw-celcard .rw-txt{font-size:13px}
.rw-many{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;margin:6px 0;animation:rwPop .5s ease}
.rw-celbtns{display:flex;gap:8px;margin-top:12px}.rw-celbtns .btn{flex:1}
@keyframes rwPop{0%{transform:scale(.3);opacity:0}100%{transform:scale(1);opacity:1}}
@keyframes rwFlipIn{0%{transform:perspective(600px) rotateY(180deg) scale(.6);opacity:0}100%{transform:perspective(600px) rotateY(0) scale(1);opacity:1}}
html.rw-mapc #map{box-shadow:0 0 0 4px var(--rw-map),0 10px 40px rgba(0,0,0,.45)}
@media (prefers-reduced-motion: reduce){.rw-in{transition:none}.rw-box .rw-gift,.rw-celbig,.rw-celcard,.rw-many,.rw-hit{animation:none}}
html.sv-hc .rw-box,html.sv-hc .rw-boss,html.sv-hc .rw-shbox{background:#fff;border:2px solid #000}html.sv-hc .rw-face{background:#fff;border:2px solid #000;color:#000}html.sv-hc .rw-ce.sil{opacity:.5}`;
    D.head.appendChild(st);
  }

  /* ================= boot ================= */
  let lastBoxNote = '';
  function tick() {
    const s = STx(); if (!s || !s.profile || isParent()) return;
    markShield(); renderPractice(false); renderMe();
    if (boxWaiting() && lastBoxNote !== day() && R().boxNote !== day()) { lastBoxNote = day(); R().boxNote = day(); saveNow();
      if (!D.getElementById('rwBox')) setTimeout(() => { try { toast('🎁 A mystery box is waiting for you in Practice!'); } catch (e) {} }, 2600); }
    pump();
  }
  function boot() {
    style(); applyMap();
    try { repair(); } catch (e) {}
    let t = 0; new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; try { tick(); } catch (e) {} }); }).observe(D.body, { childList: true, subtree: true });
    setInterval(() => { try { tick(); } catch (e) {} }, 2000);
    D.addEventListener('visibilitychange', () => { if (D.visibilityState === 'visible') { try { repair(); hud(); tick(); } catch (e) {} } });
    setTimeout(() => { try { const s = STx(); if (s && s.profile) { checkCards(); markShield(); } } catch (e) {} }, 1200);
    tick();
  }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
  window.Rewards = { shieldHTML, checkCards, openAlbum, startBoss, openBox, boss: () => bossData(boss()), boxWaiting, pump, repair, CARDS: ALL, SETS, album, howTo, _need: need };
})();
