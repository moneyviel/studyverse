/* ================= Friendship Galaxy · Rise-Again Rocket · Idea Factory — makers (js/suites-gen.js) =================
   Original content written for Knowtopia. Ideas come from well-known classroom methods (conflict-resolution steps,
   “I-messages”, circle of control, growth mindset “yet” thinking, alternative uses, SCAMPER, word association) —
   nothing is copied. Every puzzle has one clear answer that the app checks; makers re-check before returning.
   Bands: j = Grades 1–3, m = 4–8, s = 9–12, p = CA (uses s plus workplace items where marked).
   Browser: window.SuitesGen   Node: require('./suites-gen.js') (tools/mind/test_suites.js) */
(function (root) {
  'use strict';
  const ri = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
  const pick = a => a[Math.floor(Math.random() * a.length)];
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const sample = (a, n) => shuffle(a).slice(0, n);
  const NAMES = ['Aarav', 'Diya', 'Kabir', 'Meera', 'Ishaan', 'Zoya', 'Vihaan', 'Anaya', 'Reyansh', 'Saanvi', 'Arjun', 'Kiara', 'Neel', 'Tara', 'Farhan', 'Ira', 'Dev', 'Riya', 'Omar', 'Pari'];
  const mixed = (arr, key) => { let s; do { s = shuffle(arr); } while (s.every((x, i) => x === arr[i]) && arr.length > 1); return s; };

  /* =================== 🪐 FRIENDSHIP GALAXY =================== */
  /* fair share: give every friend the same number; leftovers go to the share bowl */
  const TREATS = ['🍬', '🍪', '🍫', '🍓', '🥕', '🎈', '🖍️', '🧁'];
  function fair(b, lvl) {
    const kids = b === 'j' ? ri(2, 3) : b === 'm' ? ri(3, 4) : ri(3, 5);
    const each = b === 'j' ? ri(1, 3) : ri(2, 5), left = lvl >= 2 && b !== 'j' ? ri(1, kids - 1) : (b === 'j' && lvl >= 3 ? ri(0, 1) : 0);
    const total = kids * each + left, names = sample(NAMES, kids), t = pick(TREATS);
    if (Math.floor(total / kids) !== each || total % kids !== left) throw new Error('fair');
    return { g: 'fair', names, total, t, each, left, why: `${total} shared between ${kids} friends: ${each} each${left ? `, and ${left} left over goes in the share bowl (or is shared later), so nobody gets more` : ''}. Fair means everyone gets the same.` };
  }
  /* peace steps: put the steps of solving a disagreement in order */
  const PEACE_STEPS = ['Calm down first (deep breaths)', 'Say how you feel: “I feel … when …”', 'Take turns to listen without interrupting', 'Think of ideas together', 'Choose a plan that is fair to everyone'];
  const PEACE_J = ['Stop and take a deep breath', 'Say “I feel … when …”', 'Take turns to listen', 'Think of a fair idea together'];
  const CONFLICTS = { j: ['Two friends both want the red crayon.', 'You and your brother both want the front seat.', 'Two friends want to play different games.', 'Someone took your place in the line.'],
    m: ['Two teammates want different topics for the project.', 'Your friend keeps borrowing your things without asking.', 'You and your sister argue about the TV remote.', 'A friend told someone your secret.'],
    s: ['Your group can’t agree on who presents the project.', 'Your cousin who shares your room plays music late at night.', 'A friend shared a photo of you without asking.', 'You and a teammate both want the same role in the event.'] };
  function peace(b, lvl) {
    const steps = b === 'j' ? PEACE_J : PEACE_STEPS;
    return { g: 'peace', sit: pick(CONFLICTS[b]), steps, tiles: mixed(steps),
      why: 'Calm bodies think better; each person says how they feel, then everyone listens; “I feel” words don’t blame; ideas come before choosing; the plan should be fair to everyone.' };
  }
  /* I-message builder: pick the right card for each part */
  const IMSG = [
    { s: 'Your friend keeps interrupting you when you speak.', f: ['frustrated', ['like you are the worst', 'like hitting you']], w: ['you start talking while I’m still speaking', ['you always ruin everything', 'you are so rude all the time']], r: ['I lose track of what I wanted to say', ['you are annoying', 'nobody likes you']], a: ['Could you let me finish first?', ['Be quiet, you!', 'Never talk to me again.']] },
    { s: 'Your sibling uses your things without asking.', f: ['upset', ['like you are a thief', 'like breaking your stuff']], w: ['my things are used without asking', ['you steal everything', 'you are a thief']], r: ['I can’t find them when I need them', ['you are the worst', 'Mumma loves you more']], a: ['Can you ask me before you borrow?', ['Get out of my room forever!', 'I’ll hide your toys.']] },
    { s: 'A friend is late every time we meet to play.', f: ['upset', ['like you are the worst', 'like you don’t matter to anyone']], w: ['you arrive late', ['you are useless', 'you never care about anything']], r: ['we lose time and I wait alone', ['you are lazy', 'everyone hates waiting for you']], a: ['Could we set a time that works for you?', ['Don’t bother coming next time.', 'I’ll tell everyone you’re lazy.']] },
    { s: 'A classmate laughs when you answer in class.', f: ['embarrassed', ['like laughing at you too', 'like you are the worst']], w: ['people laugh at my answer', ['you are a horrible person', 'you laugh at everyone all the time']], r: ['I stop wanting to answer', ['you are mean', 'you are jealous of me']], a: ['Can you please not laugh when I answer?', ['I’ll laugh at you next time.', 'You’d better stop or else.']] },
    { s: 'Your teammate didn’t do their part of the project.', f: ['stressed', ['like you are hopeless', 'like you are the laziest']], w: ['your part isn’t done', ['you never do anything', 'you are the laziest person']], r: ['we may miss the deadline', ['you are useless', 'you don’t care about us']], a: ['Can we plan when you can finish it?', ['I’ll tell everyone you did nothing.', 'Do it now or I quit.']] },
    { s: 'Your friend shared your photo without asking.', f: ['hurt', ['like posting yours', 'like you are a horrible friend']], w: ['my photo is shared without asking me', ['you always embarrass me', 'you are a terrible friend']], r: ['I want to choose what others see of me', ['you are so selfish', 'everyone thinks you are mean']], a: ['Could you take it down and ask me next time?', ['I’ll post something worse about you.', 'We are not friends any more.']] }];
  function imsg(b, lvl) {
    const it = pick(b === 'j' ? IMSG.slice(0, 4) : IMSG), slot = (lab, [good, bad]) => ({ lab, opts: shuffle([{ t: good, ok: 1 }].concat(bad.map(t => ({ t, ok: 0 })))) });
    const slots = [slot('I feel…', it.f), slot('when…', it.w), slot('because…', it.r), slot('Please could…', it.a)];
    return { g: 'imsg', sit: it.s, slots: b === 'j' ? slots.filter((_, i) => i !== 2) : slots,
      why: 'An “I-message” names YOUR feeling, describes what happened without blaming, explains why it matters, and asks politely. It solves problems without starting a fight.' };
  }
  /* team builder: match each job to the friend whose strength fits */
  const SKILLS = [['drawing', '🎨', 'Paint the poster by hand'], ['speaking', '🎤', 'Present to the class'], ['maths', '🧮', 'Add up the costs'], ['writing', '✍️', 'Write the report'],
    ['building', '🔨', 'Build the model'], ['organising', '📋', 'Make the to-do list and remind everyone'], ['music', '🎵', 'Make the jingle'], ['computers', '💻', 'Type the slides on the laptop'], ['photos', '📷', 'Click photos at the event']];
  function team(b, lvl) {
    const n = b === 'j' ? 2 : b === 'm' ? 3 : 4, sk = sample(SKILLS, n), names = sample(NAMES, n);
    const people = sk.map((s, i) => ({ name: names[i], skill: s[0], e: s[1] }));
    return { g: 'team', people, tasks: shuffle(sk.map(s => ({ t: s[2], skill: s[0] }))),
      why: people.map(p => `${p.name} is great at ${p.skill}`).join(', ') + '. Good teams give each job to the person whose strength fits — everyone shines and the work gets done well.' };
  }
  /* join-in planner: choose the activity EVERY friend can join */
  const ACTS = [
    { t: 'Football match', e: '⚽', a: ['run', 'outdoor', 'loud'] }, { t: 'Board games', e: '🎲', a: ['indoor'] }, { t: 'Cycling trip', e: '🚲', a: ['cycle', 'outdoor', 'far', 'run'] },
    { t: 'Drawing together', e: '🎨', a: ['indoor', 'quiet'] }, { t: 'Swimming', e: '🏊', a: ['swim', 'outdoor', 'money', 'far'] }, { t: 'Movie at the mall', e: '🎬', a: ['money', 'far', 'outdoor'] },
    { t: 'Picnic in the garden', e: '🧺', a: ['outdoor'] }, { t: 'Treasure hunt at home', e: '🗺️', a: ['indoor', 'run'] }, { t: 'Singing contest', e: '🎤', a: ['loud', 'indoor'] },
    { t: 'Puzzle building', e: '🧩', a: ['indoor', 'quiet'] }, { t: 'Quiet reading circle', e: '📚', a: ['indoor', 'quiet'] }, { t: 'Kite flying', e: '🪁', a: ['outdoor', 'run'] }];
  const NEEDS = [ ['has a hurt ankle and can’t run or pedal', 'run'], ['is not allowed in the pool today', 'swim'], ['has no bicycle', 'cycle'], ['has no pocket money this week', 'money'], ['must stay near home', 'far'],
    ['has a cold and must stay indoors', 'outdoor'], ['has a sore throat and must stay quiet', 'loud'] ];
  function include(b, lvl) {
    for (let k = 0; k < 400; k++) {
      const nn = b === 'j' ? 1 : b === 'm' ? 2 : 3, needs = sample(NEEDS, nn), names = sample(NAMES, nn);
      const fits = a => needs.every(([, bad]) => !a.a.includes(bad));
      const good = ACTS.filter(fits), badActs = ACTS.filter(a => !fits(a));
      if (good.length < 1 || badActs.length < 3) continue;
      const ans = pick(good), opts = shuffle([ans].concat(sample(badActs, 3)));
      if (opts.filter(fits).length !== 1) continue;
      return { g: 'include', friends: needs.map((n, i) => `${names[i]} ${n[0]}`), opts: opts.map(o => ({ t: o.t, e: o.e })), a: opts.indexOf(ans),
        why: `${ans.t} works for everyone. ` + opts.filter(o => o !== ans).map(o => `${o.t} leaves someone out`).join('; ') + '. Including everyone means choosing what all friends can enjoy.' };
    }
    return include(b, lvl);
  }

  /* =================== 🚀 RISE-AGAIN ROCKET =================== */
  const MINDSET = {
    j: [['I can’t do it… YET!', 1], ['I will practise and get better.', 1], ['Mistakes help me learn.', 1], ['Let me try another way.', 1], ['Mistakes show me what to fix.', 1],
        ['I’m just bad at this.', 0], ['I give up.', 0], ['It’s too hard, I quit.', 0], ['I’ll never learn this.', 0], ['Only clever kids can do this.', 0]],
    m: [['I can’t solve this yet, but I’m getting closer.', 1], ['This is hard, so my brain is growing.', 1], ['What can I learn from this mistake?', 1], ['I’ll try a different strategy.', 1], ['Her success shows me what is possible.', 1], ['Feedback helps me improve.', 1],
        ['I’m not a maths person.', 0], ['If I fail, it means I’m not smart.', 0], ['Why try if I might fail?', 0], ['Talent is everything, so practice won’t help.', 0], ['Criticism means I’m useless.', 0], ['I’ll avoid anything I might not be good at.', 0]],
    s: [['Effort and good strategies build ability over time.', 1], ['A low mark shows me what to study next.', 1], ['I can learn a lot from people who do better than me.', 1], ['Struggling with this means I’m stretching.', 1], ['Feedback is information, not a judgement of me.', 1], ['I haven’t mastered this yet.', 1],
        ['Intelligence is fixed — you have it or you don’t.', 0], ['If I need to work hard, I must not be good at it.', 0], ['Others’ success makes me look bad.', 0], ['I avoid challenges so I don’t look foolish.', 0], ['One failure proves I’ll never make it.', 0], ['I’ll only try things I know I can do.', 0]] };
  function yet(b, lvl) {
    const L = MINDSET[b], n = b === 'j' ? 4 : b === 'm' ? 6 : 6, gr = sample(L.filter(x => x[1]), n / 2), fx = sample(L.filter(x => !x[1]), n / 2);
    return { g: 'bins', kind: 'yet', q: 'Sort each thought: does it help you GROW, or keep you STUCK?', bins: ['🌱 Growth thought', '🧱 Stuck thought'], items: shuffle(gr.concat(fx).map(([t, k]) => ({ t, bin: k ? 0 : 1 }))),
      why: 'Growth thoughts treat mistakes and effort as the way to get better (“not yet”). Stuck thoughts treat ability as fixed. You can flip a stuck thought by adding “yet” or asking “what can I learn?”.' };
  }
  const CONTROL = {
    j: [['How kind I am', 1], ['If I say sorry', 1], ['How hard I try', 1], ['If I ask for help', 1], ['Putting my toys away', 1], ['If the sun shines today', 0], ['What other kids think', 0], ['If it rains on sports day', 0], ['When the bell rings', 0], ['What my friend chooses to play', 0]],
    m: [['How much I practise', 1], ['My words and actions', 1], ['How I treat others', 1], ['My attitude after a loss', 1], ['Asking questions in class', 1], ['When I start my homework', 1],
        ['Other people’s opinions of me', 0], ['The weather on match day', 0], ['What questions come in the exam', 0], ['Who the teacher picks as captain', 0], ['Traffic on the way to school', 0], ['What others post online', 0]],
    s: [['My study plan and habits', 1], ['How I respond to feedback', 1], ['How I spend my free time', 1], ['How I use my phone', 1], ['Asking for help when stuck', 1], ['My effort in each attempt', 1],
        ['The cut-off marks', 0], ['Other people’s choices', 0], ['The exam paper’s difficulty', 0], ['The economy and job market', 0], ['What happened in the past', 0], ['What others think of me', 0]] };
  function control(b, lvl) {
    const L = CONTROL[b], n = b === 'j' ? 4 : 6, a = sample(L.filter(x => x[1]), n / 2), c = sample(L.filter(x => !x[1]), n / 2);
    return { g: 'bins', kind: 'control', q: 'Sort each card: can YOU control it, or not?', bins: ['🎯 I can control', '☁️ I can’t control'], items: shuffle(a.concat(c).map(([t, k]) => ({ t, bin: k ? 0 : 1 }))),
      why: 'Put your energy into what you CAN control — your effort, words, choices and habits. For the rest, notice the feeling, then let it go or plan around it.' };
  }
  const LADDERS = {
    j: [['Learn to ride a cycle', ['Wear a helmet', 'Practise with a grown-up holding on', 'Ride a little on your own', 'Ride all the way round the park']],
        ['Plant a flower', ['Get a pot and soil', 'Plant the seed', 'Water it every day', 'Watch the flower bloom']],
        ['Get ready for school', ['Wake up', 'Get dressed in your uniform', 'Have breakfast', 'Put on your shoes and go']]],
    m: [['Get into the school team', ['Ask the coach what skills are needed', 'Make a weekly practice plan', 'Practise and track your progress', 'Play practice matches', 'Go for the trials']],
        ['Improve your maths marks', ['Check which topics you lost marks in', 'Relearn the concept of those topics', 'Practise similar questions', 'Take a mock test', 'Review the mistakes in the mock']],
        ['Save money for a cricket bat', ['Find out the price', 'Decide how much to save each week', 'Put the money aside every week', 'Count your savings', 'Buy the bat']]],
    s: [['Prepare for board exams', ['List all chapters and rate how ready you are', 'Make a day-by-day timetable', 'Study weak topics first', 'Solve past papers under time', 'Revise mistakes before the exam']],
        ['Start a school club', ['Ask a teacher to guide the club', 'Find out who is interested', 'Fix a date and place for the first meeting', 'Hold the first meeting', 'Collect feedback and improve']],
        ['Get an internship', ['Decide what field you want', 'Prepare your CV', 'Apply to a few places', 'Prepare for the interview', 'Follow up after the interview']]],
    p: [['Clear the next CA attempt', ['Analyse last attempt’s marks paper by paper', 'Make a revised study timetable', 'Study weak papers first', 'Write full mock tests', 'Revise from mistakes before the exam']],
        ['Finish a big audit file on time', ['Ask your senior what is most important', 'List all tasks and deadlines in that order', 'Do the key tasks first', 'Review your own work', 'Submit and note lessons learnt']]] };
  function plan(b, lvl, orig) {
    const [goal, steps] = pick(orig === 'p' ? LADDERS.p.concat(LADDERS.s) : LADDERS[b]);
    return { g: 'plan', goal, steps, tiles: mixed(steps), why: 'Big goals feel easy when broken into small steps in the right order: find out what is needed, plan, practise, check, and then go for it.' };
  }
  /* rocket retry: change the angle and power until you land on the planet */
  function rocket(b, lvl) {
    const tries = b === 'j' ? 6 : b === 'm' ? 5 : 4;
    const tx = ri(55, 92), tw = b === 'j' ? 14 : b === 'm' ? 10 : 8;
    return { g: 'rocket', tx, tw, tries, wind: b === 's' && lvl >= 3 ? (Math.random() < .5 ? -1 : 1) * ri(1, 3) : 0 };
  }
  /* rocket physics (shared with the app so the check is the same everywhere) */
  function flight(angle, power, wind) {
    const g = 9.8, v = power * 0.95, a = angle * Math.PI / 180;
    let x = 4, y = 0, vx = v * Math.cos(a), vy = v * Math.sin(a); const pts = [[x, y]];
    for (let i = 0; i < 2000 && y >= 0; i++) { const dt = 0.02; vx += (wind || 0) * 0.15 * dt; x += vx * dt; y += vy * dt; vy -= g * dt; pts.push([x, Math.max(0, y)]); }
    return { land: x, pts };
  }
  /* coping toolbox: pick the helpful tools */
  const COPE = {
    good: ['Take five slow breaths', 'Talk to someone I trust', 'Take a short break and come back', 'Stretch or play outside with a friend', 'Write down what I’m feeling', 'Make a small plan for what to do next', 'Drink water and rest', 'Remind myself of a time I managed'],
    bad: ['Shout at someone nearby', 'Keep it all inside forever', 'Give up and never try again', 'Break something', 'Stay up all night worrying', 'Blame everyone else', 'Refuse to eat or drink all day', 'Scroll the phone for hours to forget'] };
  const SETBACKS = { j: ['Your tower fell down again.', 'You lost the race.', 'You got many sums wrong.'], m: ['You were not picked for the team.', 'You failed a test you studied for.', 'Your friend group left you out.'],
    s: ['You did badly in a mock exam.', 'Your college application was rejected.', 'Your project failed on presentation day.'], p: ['You did not clear one group of the CA exam.', 'Your senior criticised your work in front of others.'] };
  function cope(b, lvl, orig) {
    const need = b === 'j' ? 2 : 3, good = sample(COPE.good, need), bad = sample(COPE.bad, b === 'j' ? 2 : 3);
    return { g: 'multi', kind: 'cope', q: `${pick(orig === 'p' ? SETBACKS.p : SETBACKS[b])} Put the ${need} HELPFUL tools in your toolbox.`, need, items: shuffle(good.map(t => ({ t, ok: 1 })).concat(bad.map(t => ({ t, ok: 0 })))),
      why: 'Helpful tools calm your body, connect you with others or help you make a plan. Unhelpful ones hurt you or others, or keep you stuck.' };
  }

  /* =================== 💡 IDEA FACTORY =================== */
  const USES = [   // object, emoji, good creative uses (really possible), impossible/unsafe uses
    ['Empty plastic bottle', '🧴', ['Plant pot for a small plant', 'Pencil holder', 'Bird feeder (cut by a grown-up)', 'Piggy bank', 'Shaker music instrument', 'Watering can with holes in the cap'], ['Umbrella in heavy rain', 'Safe helmet for cycling', 'Fridge to keep food cold', 'Chair for an adult']],
    ['Old newspaper', '📰', ['Paper hat', 'Wrapping paper for a gift', 'Paper bag', 'Papier-mâché model', 'Kite tail', 'Stuffing to keep shoes in shape'], ['Raincoat for a storm', 'Plate for hot soup', 'Mirror', 'Phone charger']],
    ['Cardboard box', '📦', ['Toy house or castle', 'Storage for toys', 'Robot costume', 'Cat bed', 'Puppet theatre', 'Mini football goal'], ['Boat for crossing a river', 'Ship to sail across the sea', 'Ladder to the roof', 'Bulletproof shield']],
    ['Spoon', '🥄', ['Small shovel for a plant pot', 'Drum stick', 'Plant label stick', 'Paint mixer', 'Catapult arm for a toy'], ['Hammer for nails', 'Umbrella', 'Torch', 'Pair of scissors']],
    ['Old sock', '🧦', ['Sock puppet', 'Dusting cloth', 'Cover for a ball or shoe', 'Bean bag for games', 'Phone cover'], ['Water bottle', 'Swimming goggles', 'Kite', 'Cooking pan']],
    ['Brick', '🧱', ['Doorstop', 'Bookend', 'Plant-pot stand', 'Garden border', 'Paperweight'], ['Pillow', 'Toy for a baby', 'Float in a pool', 'Sponge for washing']],
    ['Paper cup', '🥤', ['String telephone', 'Seed starter pot', 'Pencil cup', 'Mini megaphone', 'Paint-water holder'], ['Hat in a storm', 'Cooking pot on the stove', 'Shoe', 'Strong building block for a house']],
    ['Rubber band', '➰', ['Bundle pencils together', 'Grip on a jar lid', 'Hair tie for a doll', 'Bookmark', 'Guitar string on a box'], ['Necklace for a toddler', 'Bridge to cross water', 'Light bulb', 'Spoon']],
    ['Old T-shirt', '👕', ['Cloth shopping bag', 'Cleaning rag', 'Pillow cover', 'Headband', 'Stuffing for a cushion'], ['Helmet', 'Glass window', 'Frying pan', 'Ladder']],
    ['Glass jar', '🫙', ['Lantern with an LED light inside', 'Storage for buttons', 'Tiny terrarium garden', 'Money jar', 'Pen stand'], ['Football', 'Cushion', 'Sunglasses', 'Toy for a toddler']]];
  function uses(b, lvl) {
    const [obj, e, good, bad] = pick(USES), need = b === 'j' ? 2 : 3;
    return { g: 'multi', kind: 'uses', q: `${e} ${obj}: pick the ${need} uses that could REALLY work (new and clever!).`, need, items: shuffle(sample(good, need).map(t => ({ t, ok: 1 })).concat(sample(bad, b === 'j' ? 2 : 3).map(t => ({ t, ok: 0 })))),
      why: 'Creative thinkers ask “what else could this be?” — but a good idea must also work in real life and be safe. That mix of fresh + useful is creativity.' };
  }
  /* word link: one word that goes with all three */
  const LINKS = {
    j: [['SUN', ['🌻 flower', '👓 glasses', '🌅 set'], 'sunflower, sunglasses, sunset'], ['RAIN', ['🌈 bow', '🧥 coat', '💧 drop'], 'rainbow, raincoat, raindrop'], ['FOOT', ['⚽ ball', '👣 print', '🛤️ path'], 'football, footprint, footpath'],
        ['STAR', ['🐟 fish', '💡 light', '✨ dust'], 'starfish, starlight, stardust'], ['SNOW', ['⛄ man', '❄️ flake', '⚾ ball'], 'snowman, snowflake, snowball'], ['BED', ['🕰️ time', '🏠 room', '📄 sheet'], 'bedtime, bedroom, bedsheet'], ['TEA', ['☕ cup', '🫖 pot', '🥄 spoon'], 'teacup, teapot, teaspoon']],
    m: [['BALL', ['FOOT', 'BASKET', 'SNOW'], 'football, basketball, snowball'], ['HOUSE', ['LIGHT', 'TREE', 'GREEN'], 'lighthouse, treehouse, greenhouse'], ['BOOK', ['NOTE', 'STORY', 'TEXT'], 'notebook, storybook, textbook'],
        ['FLY', ['BUTTER', 'DRAGON', 'FIRE'], 'butterfly, dragonfly, firefly'], ['BOARD', ['BLACK', 'KEY', 'CARD'], 'blackboard, keyboard, cardboard'], ['WORK', ['HOME', 'TEAM', 'NET'], 'homework, teamwork, network'], ['DAY', ['BIRTH', 'WEEK', 'SUN'], 'birthday, weekday, Sunday'], ['MARK', ['BOOK', 'LAND', 'BIRTH'], 'bookmark, landmark, birthmark']],
    s: [['POWER', ['WILL', 'HORSE', 'FIRE'], 'willpower, horsepower, firepower'], ['TABLE', ['TIME', 'PERIODIC', 'TURN'], 'timetable, periodic table, turntable'], ['LINE', ['HEAD', 'DEAD', 'LIFE'], 'headline, deadline, lifeline'],
        ['CASE', ['BOOK', 'SUIT', 'SHOW'], 'bookcase, suitcase, showcase'], ['PRINT', ['FOOT', 'FINGER', 'BLUE'], 'footprint, fingerprint, blueprint'], ['WORK', ['FRAME', 'NET', 'HOME'], 'framework, network, homework'],
        ['POINT', ['VIEW', 'STAND', 'CHECK'], 'viewpoint, standpoint, checkpoint'], ['SHIP', ['FRIEND', 'LEADER', 'SCHOLAR'], 'friendship, leadership, scholarship'], ['LIGHT', ['SPOT', 'HIGH', 'MOON'], 'spotlight, highlight, moonlight']] };
  function link(b, lvl, orig) {
    const [ans, words, how] = pick(LINKS[b]);
    const pool = 'ABCDEFGHIKLMNOPRSTUW'.split('').filter(c => !ans.includes(c));
    const extra = b === 'j' ? 1 : b === 'm' ? 2 : 3;
    return { g: 'link', words, answer: ans, tiles: shuffle(ans.split('').concat(sample(pool, extra))), why: `${ans}: ${how}. Linking far-apart ideas is a key creative skill.` };
  }
  /* SCAMPER: which idea move made this invention? */
  const SCAMP = [['Substitute', 'swap one part for another'], ['Combine', 'join two things into one'], ['Adapt', 'borrow an idea from somewhere else'], ['Modify', 'make it bigger, smaller or a different shape'],
    ['Put to another use', 'use it for something new'], ['Eliminate', 'take a part away'], ['Reverse', 'turn it around or do it the other way']];
  const SCAMP_EX = [
    ['A pencil with an eraser on the end', 1], ['A phone that is also a camera', 1], ['Velcro, inspired by burrs that stick to dogs’ fur', 2], ['A bullet-train nose shaped like a kingfisher’s beak', 2], ['A seedless watermelon', 5],
    ['Paper straws instead of plastic ones', 0], ['Using an old tyre as a garden swing', 4], ['A jumbo-size pizza for parties', 3], ['A mini travel-size toothpaste', 3], ['A sauce bottle turned upside down so it stands on its cap', 6],
    ['Using a cardboard box as a robot costume', 4], ['Swapping a lock’s key for a fingerprint scan', 0], ['Self-service shops where customers serve themselves', 6],
    ['A bicycle with no pedals for toddlers to learn balance', 5], ['A water bottle with a built-in filter', 1], ['A lunch box shaped to fit a school bag pocket', 3]];
  function scamper(b, lvl) {
    const pool = b === 'j' ? SCAMP_EX.filter(x => [1, 3, 4, 5].includes(x[1])) : SCAMP_EX;
    const [idea, k] = pick(pool), wrong = sample([0, 1, 2, 3, 4, 5, 6].filter(x => x !== k), 3), opts = shuffle([k].concat(wrong));
    return { g: 'pick', kind: 'scamper', q: `💡 Invention: “${idea}”. Which idea move made it?`, opts: opts.map(i => ({ t: `${SCAMP[i][0]} — ${SCAMP[i][1]}` })), a: opts.indexOf(k),
      why: `${SCAMP[k][0]}: ${SCAMP[k][1]}. Inventors use these seven moves (SCAMPER) to turn ordinary things into new ideas — try them on anything around you!` };
  }
  /* question quest: open “explore” questions vs closed yes/no questions */
  const QS = {
    open: ['Why do leaves change colour?', 'How could we make our school greener?', 'What would happen if there were no moon?', 'How do birds know where to fly in winter?', 'What else could this box be used for?', 'Why do some things float and others sink?', 'How might robots help farmers?', 'What if animals could talk?', 'How could we reduce waste at lunch?', 'Why is the sky blue?'],
    closed: ['Is the sky blue?', 'Do you like mangoes?', 'Is it raining?', 'Did you finish your homework?', 'Is a whale a fish?', 'Can dogs swim?', 'Is today Monday?', 'Do plants need water?', 'Is this pen red?', 'Are you hungry?'] };
  function curious(b, lvl) {
    const n = b === 'j' ? 2 : 3, o = sample(QS.open, n), c = sample(QS.closed, n);
    return { g: 'bins', kind: 'curious', q: 'Sort the questions: which ones OPEN UP new ideas, and which are just YES/NO?', bins: ['🔭 Explorer question', '✅ Yes/No question'], items: shuffle(o.map(t => ({ t, bin: 0 })).concat(c.map(t => ({ t, bin: 1 })))),
      why: 'Explorer questions start with why, how, what if or what else — they open doors to new ideas. Yes/No questions close quickly. Curious minds ask lots of explorer questions.' };
  }
  /* riddle lab: original lateral-thinking riddles with a hint ladder */
  const RIDDLES = [
    { q: 'I have keys but open no doors. I have space but no room. You can enter, but not go inside. What am I?', a: 'A keyboard', w: ['A piano', 'A house', 'A car'], h: ['Look at what you type on.', 'It has a “space” bar and an “enter” key.'], b: 'ms' },
    { q: 'The more you take, the more you leave behind. What are they?', a: 'Footsteps', w: ['Pencils', 'Coins', 'Breaths'], h: ['Think about walking.', 'They are left on the ground behind you.'], b: 'jms' },
    { q: 'What has a neck but no head, and wears a cap?', a: 'A bottle', w: ['A giraffe', 'A shirt', 'A flag'], h: ['It holds water.', 'You twist the cap off.'], b: 'jms' },
    { q: 'I get wetter the more I dry. What am I?', a: 'A towel', w: ['A comb', 'The sun', 'A fan'], h: ['You use me after a bath.', 'I take the water from you.'], b: 'jms' },
    { q: 'What can you catch but not throw?', a: 'A cold', w: ['A ball', 'A fish', 'A stone'], h: ['It makes you sneeze.', 'Doctors talk about it.'], b: 'jms' },
    { q: 'What goes up but never comes down?', a: 'Your age', w: ['A kite', 'A coin', 'A feather'], h: ['Everyone has one.', 'It changes on your birthday.'], b: 'jms' },
    { q: 'What has many teeth but cannot bite?', a: 'A comb', w: ['A shark', 'A dog', 'A crocodile'], h: ['You use it every morning.', 'It goes through your hair.'], b: 'jms' },
    { q: 'A girl looks out of a ground-floor window of a 20-storey building and steps out — she is not hurt. Why?', a: 'She was on the ground floor', w: ['She had a parachute', 'She landed on a mat', 'It was a dream'], h: ['Read again: which floor is she on?', 'How high is a ground-floor window?'], b: 'ms' },
    { q: 'What word becomes shorter when you add two letters to it?', a: 'Short', w: ['Long', 'Tall', 'Small'], h: ['Take the riddle very literally.', 'Which two letters make a word longer… and “-er”?'], b: 'ms' },
    { q: 'A doctor’s only brother is a farmer, but the farmer has no brother. How?', a: 'The doctor is his sister', w: ['They are step-brothers', 'The farmer is lying', 'The doctor is adopted'], h: ['Who said the doctor is a man?', 'Think about who could be his sibling.'], b: 'ms' },
    { q: 'What has hands but cannot clap?', a: 'A clock', w: ['A robot', 'A glove', 'A baby'], h: ['It hangs on the wall.', 'It tells the time.'], b: 'jms' },
    { q: 'What runs but never walks, has a mouth but never talks?', a: 'A river', w: ['A clock', 'A dog', 'A train'], h: ['It flows to the sea.', 'Its “mouth” is where it meets the sea.'], b: 'ms' },
    { q: 'You see a boat full of people, yet there isn’t a single person on board. How?', a: 'They are all married', w: ['They are all robots', 'It is a painting', 'They are all asleep'], h: ['Think about the word “single”.', 'Single can mean not married.'], b: 's' },
    { q: 'What can travel around the world while staying in one corner?', a: 'A postage stamp', w: ['A satellite', 'A shadow', 'The internet'], h: ['It goes on letters.', 'It sits in the corner of an envelope.'], b: 'ms' },
    { q: 'The moment you tell anyone about me, I am not what I was. What am I?', a: 'A secret', w: ['A sweet', 'A toy', 'Money'], h: ['Friends whisper it.', 'Once you tell it, it is gone.'], b: 'ms' },
    { q: 'Forward I am heavy, backward I am not. What am I?', a: 'Ton', w: ['Rock', 'Weight', 'Iron'], h: ['Spell me backwards.', 'Backwards I spell “not”.'], b: 's' },
    { q: 'What has one eye but cannot see?', a: 'A needle', w: ['A pirate', 'A camera', 'A coin'], h: ['It is used for sewing.', 'Thread goes through its eye.'], b: 'jms' },
    { q: 'A ledger shows a profit, yet the business has no cash in the bank. What is the most likely reason?', a: 'Sales were made on credit', w: ['Inventory was bought for cash', 'Loan instalments were paid', 'Drawings were very high'], h: ['Profit is not the same as cash.', 'Think about debtors.'], b: 'p' },
    { q: 'An auditor finds every invoice number in order, except the same number appears twice. What should catch the auditor’s eye first?', a: 'A possible duplicate payment', w: ['A missing invoice number', 'A late supplier delivery', 'A rounding error'], h: ['Two invoices, one number.', 'Could something be paid twice?'], b: 'p' }];
  function riddle(b, lvl, orig) {
    const key = orig === 'p' ? 'p' : b, pool = RIDDLES.filter(r => r.b.includes(key) || (orig === 'p' && r.b.includes('s')));
    const r = pick(pool), opts = shuffle([r.a].concat(r.w));
    return { g: 'pick', kind: 'riddle', q: '🧩 ' + r.q, opts: opts.map(t => ({ t })), a: opts.indexOf(r.a), hints: r.h, why: `Answer: ${r.a}. Lateral thinking means reading every word carefully and trying a different angle.` };
  }

  const MAKERS = { fair, peace, imsg, team, include, yet, control, plan, rocket, cope, uses, link, scamper, curious, riddle };
  const API = { MAKERS, make: (g, b, lvl) => MAKERS[g](b === 'p' ? 's' : b, Math.max(1, Math.min(5, lvl)), b), flight, MINDSET, CONTROL, LINKS, USES, RIDDLES, SCAMP_EX, IMSG, NEEDS, ACTS };
  if (typeof module !== 'undefined' && module.exports) module.exports = API; else root.SuitesGen = API;
})(typeof window !== 'undefined' ? window : this);
