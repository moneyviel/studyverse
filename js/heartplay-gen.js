/* ================= Heart Compass games: makers and content (js/heartplay-gen.js) =================
   Original content written for Knowtopia (nothing copied). Skills follow widely used school social-emotional
   learning areas, in our own words:
     Know my feelings · Manage my feelings · Read others · Connect & care · Choose wisely
   Games (each puzzle has ONE clear best answer, checked by the app):
     faces   – Feeling Detective: read a face (and, for older students, a situation) → name the feeling
     thermo  – Feelings Thermometer: put feeling words in order from mild to strong
     shoes   – In Their Shoes: same event, different people → give each one the right feeling sticker
     chat    – Friend Chat: reply to a friend in a phone chat; the friend’s mood shows how it lands
     paths   – Choose Your Path: a 3-step story where every choice has a consequence
     breathe – Calm Breath: follow the bubble (hold to breathe in, let go to breathe out), scored on timing
   Bands: j = Grades 1–3, m = 4–8, s = 9–12 and CA.  Works in the browser (window.HeartPlayGen) and Node (tests). */
(function (root) {
  'use strict';
  const ri = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
  const pick = a => a[Math.floor(Math.random() * a.length)];
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const sample = (a, n) => shuffle(a).slice(0, n);
  const NAMES = ['Aarav', 'Diya', 'Kabir', 'Meera', 'Ishaan', 'Zoya', 'Vihaan', 'Anaya', 'Reyansh', 'Saanvi', 'Arjun', 'Kiara', 'Neel', 'Tara', 'Farhan', 'Ira', 'Dev', 'Riya', 'Omar', 'Pari'];

  /* ---------- 1. Feeling Detective ---------- */
  const FACE = {   // drawn by the app; each has a clear, well-known face
    happy: { e: '😊', w: 'Happy' }, sad: { e: '😢', w: 'Sad' }, angry: { e: '😠', w: 'Angry' }, scared: { e: '😨', w: 'Scared' }, surprised: { e: '😲', w: 'Surprised' }, disgusted: { e: '🤢', w: 'Disgusted' } };
  const FACE_SET = { j: ['happy', 'sad', 'angry', 'scared'], m: ['happy', 'sad', 'angry', 'scared', 'surprised'], s: ['happy', 'sad', 'angry', 'scared', 'surprised', 'disgusted'] };
  // situations that clearly point to one feeling; FAR lists feelings that clearly do NOT fit (used as wrong options)
  const SIT = {
    proud: ['finally solves a puzzle that took all week', 'gets a “well done” from the coach after months of practice', 'reads a whole chapter book alone for the first time', 'sees their science model put up in the school hall', 'learns to ride a cycle without help after many falls'],
    embarrassed: ['trips on stage in front of the whole school', 'calls the teacher “Mumma” by mistake in class', 'finds out their shirt was inside out all day', 'sings the wrong words loudly while everyone else is quiet'],
    jealous: ['watches a friend get the new bicycle they wanted', 'sees their best friend spend all break with someone new and wishes it were them', 'hears everyone praise a classmate for the prize they hoped to win'],
    guilty: ['broke a vase and watched their brother get scolded for it', 'copied a friend’s homework and the friend got blamed for copying', 'forgot to feed the pet after promising to do it'],
    relieved: ['finds their lost house key just before dark', 'hears that the scary test has been put off to next week', 'gets news that their grandmother’s operation went well', 'sees their lost dog run back home'],
    frustrated: ['keeps trying a maths problem and it still will not work', 'has the phone freeze for the third time while saving work', 'explains the same thing again and again and nobody listens'],
    nervous: ['waits backstage just before their first dance show', 'sits outside the principal’s office not knowing why they were called', 'is about to speak in front of a new class'],
    lonely: ['eats lunch alone on the first day at a new school', 'stays home sick while the whole class goes on a trip', 'moves to a new city where they know nobody'],
    grateful: ['gets help from a neighbour who carries their heavy bags home', 'receives a handmade card from a friend when they were ill', 'is given notes by a classmate after missing a week of school'],
    disappointed: ['finds the match they waited for all week is cancelled by rain', 'opens a gift box and it is empty because the toy was forgotten', 'misses the cut for the school team by one point'],
    excited: ['has a family trip to the mountains starting tomorrow', 'is counting the hours to their birthday party', 'just heard their favourite author is visiting the school'],
    confused: ['gets two different instructions from two teachers for the same task', 'reads a map where the roads do not match what they see', 'hears a joke everyone laughs at but does not understand it']
  };
  const FEEL_WORD = { proud: 'Proud', embarrassed: 'Embarrassed', jealous: 'Jealous', guilty: 'Guilty', relieved: 'Relieved', frustrated: 'Frustrated', nervous: 'Nervous', lonely: 'Lonely', grateful: 'Grateful', disappointed: 'Disappointed', excited: 'Excited', confused: 'Confused' };
  const FAR = {
    proud: ['guilty', 'lonely', 'confused', 'nervous'], embarrassed: ['proud', 'grateful', 'relieved', 'excited'], jealous: ['grateful', 'relieved', 'proud', 'confused'],
    guilty: ['proud', 'excited', 'grateful', 'lonely'], relieved: ['jealous', 'guilty', 'frustrated', 'lonely'], frustrated: ['relieved', 'grateful', 'proud', 'excited'],
    nervous: ['relieved', 'grateful', 'proud', 'jealous'], lonely: ['proud', 'grateful', 'relieved', 'guilty'], grateful: ['jealous', 'guilty', 'frustrated', 'lonely'],
    disappointed: ['proud', 'relieved', 'grateful', 'excited'], excited: ['guilty', 'lonely', 'disappointed', 'frustrated'], confused: ['proud', 'grateful', 'jealous', 'relieved'] };
  function faces(b, lvl) {
    const useSit = b !== 'j' && (lvl >= 2 && Math.random() < (b === 's' ? .75 : .5));
    const name = pick(NAMES);
    if (useSit) {
      const feel = pick(Object.keys(SIT)), wrong = sample(FAR[feel], 3);
      if (wrong.includes(feel)) throw new Error('faces far');
      return { g: 'faces', mode: 'sit', name, text: `${name} ${pick(SIT[feel])}. How is ${name} most likely feeling?`, opts: shuffle([feel].concat(wrong)).map(k => ({ k, w: FEEL_WORD[k] })), answer: feel,
        why: `Most people would feel ${FEEL_WORD[feel].toLowerCase()} here. Naming the exact feeling helps you understand it and respond well.` };
    }
    const set = FACE_SET[b], feel = pick(set), wrong = sample(set.filter(x => x !== feel), 3);
    return { g: 'faces', mode: 'face', name, face: { feel, skin: ri(0, 4), hair: ri(0, 3) }, opts: shuffle([feel].concat(wrong)).map(k => ({ k, w: FACE[k].w, e: b === 'j' ? FACE[k].e : '' })), answer: feel,
      why: { happy: 'Raised cheeks and a curved-up smile show happiness.', sad: 'Inner eyebrows go up, eyes droop and the mouth turns down — that shows sadness.', angry: 'Eyebrows pulled down into a V and a tight mouth show anger.',
        scared: 'Eyebrows up, very wide eyes and a stretched mouth show fear.', surprised: 'High round eyebrows, wide eyes and a dropped “O” mouth show surprise.', disgusted: 'A wrinkled nose and a raised top lip show disgust.' }[feel] };
  }

  /* ---------- 2. Feelings Thermometer (mild → strong) ---------- */
  const SCALES_J = [{ f: 'Sadness', w: ['A bit sad', 'Sad', 'Very sad'], e: ['🙁', '😢', '😭'] }, { f: 'Fear', w: ['A bit scared', 'Scared', 'Very scared'], e: ['😕', '😨', '😱'] },
    { f: 'Anger', w: ['A bit cross', 'Angry', 'Furious'], e: ['😒', '😠', '😡'] }, { f: 'Happiness', w: ['Pleased', 'Happy', 'Super happy'], e: ['🙂', '😊', '🤩'] }];
  const SCALES = [
    { f: 'Anger', w: ['Annoyed', 'Angry', 'Furious'] }, { f: 'Fear', w: ['Uneasy', 'Scared', 'Terrified'] }, { f: 'Sadness', w: ['Down', 'Sad', 'Heartbroken'] },
    { f: 'Happiness', w: ['Pleased', 'Happy', 'Overjoyed'] }, { f: 'Worry', w: ['Concerned', 'Worried', 'Panicked'] }, { f: 'Liking', w: ['Like', 'Love', 'Adore'] },
    { f: 'Embarrassment', w: ['Awkward', 'Embarrassed', 'Humiliated'] } ];
  function thermo(b, lvl) {
    const sc = pick(b === 'j' ? SCALES_J : SCALES);
    const order = sc.w.map((w, i) => ({ w, e: sc.e ? sc.e[i] : '', r: i }));
    let tiles; do { tiles = shuffle(order); } while (tiles.every((t, i) => t.r === i));
    return { g: 'thermo', family: sc.f, tiles, answer: sc.w.slice(), why: `${sc.w.join(' → ')}: the same family of feeling (${sc.f.toLowerCase()}), from mild to strong. Knowing how strong a feeling is helps you choose what to do — a small feeling may pass, a big one needs a calm-down plan.` };
  }

  /* ---------- 3. In Their Shoes ---------- */
  const SHOES = [   // r: [who, every feeling that fits], no: extra stickers that clearly do not fit anyone
    { t: '{A} wins the drawing prize. {B} also entered and really hoped to win.', r: [['{A}', ['proud', 'happy', 'excited']], ['{B}', ['disappointed', 'sad', 'jealous']]] },
    { t: '{A}’s puppy runs away. Later {B} finds the puppy and brings it back.', r: [['{A} (when the puppy is back)', ['relieved', 'grateful', 'happy']], ['{B}', ['proud', 'happy', 'caring']]] },
    { t: '{A} breaks {B}’s new pencil box by accident.', r: [['{A}', ['guilty', 'embarrassed', 'sorry', 'upset', 'sad']], ['{B}', ['upset', 'sad', 'hurt']]] },
    { t: '{A} is new and alone at lunch. {B} comes over and asks “Want to sit with us?”', r: [['{A} (before)', ['lonely', 'nervous', 'left out']], ['{A} (after)', ['grateful', 'happy']], ['{B}', ['caring', 'kind', 'happy']]] },
    { t: 'The school trip is cancelled. {A} was looking forward to it. {B} was worried about the long bus ride.', r: [['{A}', ['disappointed', 'sad']], ['{B}', ['relieved', 'happy']]] },
    { t: '{A} forgot their lines in the play and the audience giggled. {B} whispered the next line to help.', r: [['{A}', ['embarrassed', 'nervous']], ['{B}', ['caring', 'helpful']]], noDecoy: ['silly'] },
    { t: '{A} hears loud thunder during a storm. {B}, the big sister, holds their hand.', r: [['{A}', ['scared', 'nervous', 'calm']], ['{B}', ['caring', 'protective', 'calm', 'brave']]] },
    { t: '{A} gets full marks after studying hard. {B} copied and got full marks too.', r: [['{A}', ['proud', 'happy', 'relieved']], ['{B} (deep down)', ['guilty', 'nervous', 'worried', 'relieved', 'happy']]], min: 'm' },
    { t: '{A} is about to go on stage for the first time. {B} has done it many times.', r: [['{A}', ['nervous', 'scared', 'excited']], ['{B}', ['confident', 'calm', 'excited', 'nervous']]], noDecoy: ['bored'] },
    { t: '{A} lent {B} a favourite book and {B} returned it torn without saying sorry.', r: [['{A}', ['upset', 'hurt', 'angry', 'sad', 'disappointed']], ['{B} (should feel)', ['guilty', 'sorry', 'embarrassed']]], min: 'm' },
    { t: '{A}’s grandparent is visiting after two years. {B}, the cousin, could not come.', r: [['{A}', ['excited', 'happy']], ['{B}', ['left out', 'sad', 'disappointed']]] },
    { t: '{A} keeps trying a magic trick and it fails. {B} watches and claps when it finally works.', r: [['{A} (while failing)', ['frustrated', 'annoyed']], ['{B} (at the end)', ['happy', 'proud', 'excited']]], noDecoy: ['silly'] },
    { t: '{A}’s team loses the final. {B}’s team wins it.', r: [['{A}', ['disappointed', 'sad', 'upset']], ['{B}', ['proud', 'happy', 'excited']]] },
    { t: '{A} sees everyone laughing at a joke {A} did not understand.', r: [['{A}', ['confused', 'left out', 'embarrassed']]], no: ['proud', 'grateful'], noDecoy: ['silly'] },
    { t: '{A} gives a surprise card to {B}, who was ill all week.', r: [['{A}', ['caring', 'happy', 'kind']], ['{B}', ['grateful', 'touched', 'happy']]] },
    { t: '{A} waits for exam results. {B} already knows they passed.', r: [['{A}', ['nervous', 'worried', 'scared']], ['{B}', ['relieved', 'happy', 'proud']]] },
    { t: '{A} is blamed for a mess that {B} made, and {B} stays quiet.', r: [['{A}', ['angry', 'hurt', 'upset', 'sad']], ['{B} (should feel)', ['guilty', 'sorry']]], min: 'm' },
    { t: '{A} moves to a new city and starts at a school where nobody knows them.', r: [['{A} (first day)', ['nervous', 'lonely', 'scared', 'excited']]], no: ['proud', 'guilty'] }
  ];
  const STICK = { proud: '🥇', happy: '😊', disappointed: '😞', sad: '😢', relieved: '😮‍💨', grateful: '🙏', guilty: '😖', embarrassed: '😳', upset: '😣', lonely: '🥺', helpful: '🤝', caring: '🤗',
    scared: '😨', protective: '🛡️', nervous: '😬', confident: '😎', calm: '😌', hurt: '💔', sorry: '😔', excited: '🤩', 'left out': '😶', frustrated: '😤', confused: '😕', touched: '🥹', worried: '😟', angry: '😠', jealous: '😒', bored: '🥱', silly: '🤪', sleepy: '😴', annoyed: '😑', kind: '💗', brave: '🦁' };
  const DECOY = ['bored', 'sleepy', 'silly'];
  function shoes(b, lvl) {
    for (let t = 0; t < 200; t++) {
      const S = pick(SHOES.filter(x => !(x.min === 'm' && b === 'j'))), [A, B] = sample(NAMES, 2);
      const lab = s => s.replace(/\{A\}/g, A).replace(/\{B\}/g, B);
      const roles = S.r.map(([l, ok]) => ({ who: lab(l), ok, pickd: pick(ok) }));
      const all = new Set(S.r.flatMap(r => r[1]));
      const decoys = sample(DECOY.concat(S.no || []).filter(d => !all.has(d) && !(S.noDecoy || []).includes(d)), b === 'j' ? 1 : b === 'm' ? 2 : 3);
      const stickers = shuffle(roles.map(r => r.pickd).concat(decoys));
      // each sticker must fit at most one person, and the two people need different stickers
      if (stickers.some(st => roles.filter(r => r.ok.includes(st)).length > 1)) continue;
      if (new Set(roles.map(r => r.pickd)).size !== roles.length) continue;
      return { g: 'shoes', text: lab(S.t), roles: roles.map(r => ({ who: r.who, ok: r.ok })), answer: roles.map(r => r.pickd), stickers: stickers.map(k => ({ k, e: STICK[k] || '🙂' })),
        why: roles.map(r => `${r.who}: ${r.ok.join(' or ')}`).join(' · ') + '. The same event can feel very different to each person — that is empathy.' };
    }
    return shoes(b, lvl);
  }

  /* ---------- 4. Friend Chat ---------- */
  const CHAT = {   // [first message, feeling, second message, a helpful idea (full sentence), serious?]
    j: [['My drawing got rain on it 😢', 'sad', 'I worked on it all morning.', 'Shall we draw a new one together?'], ['Nobody picked me for the game today.', 'left out', 'I just stood there.', 'Come and play with me at break!'],
        ['My tooth fell out and it hurts!', 'scared', 'There was a bit of blood.', 'Let’s tell your teacher — a grown-up can help.'], ['My balloon flew away!', 'sad', 'It was my birthday balloon.', 'Want to draw a big balloon for your card?'],
        ['I can’t do the cartwheel. Everyone else can.', 'upset', 'I keep falling.', 'Shall we practise together on the soft grass?'], ['My best friend is absent today.', 'lonely', 'I have nobody to sit with.', 'You can sit with me today!']],
    m: [['I failed the maths test. My parents will be so upset.', 'worried', 'I studied but the questions felt different.', 'We could go through the mistakes together, and you could tell your parents how hard you tried.'],
        ['They chose someone else as captain. Again.', 'disappointed', 'I really thought it would be me this time.', 'Maybe ask the coach what to work on for next time?'],
        ['My best friend is ignoring me and I don’t know why.', 'hurt', 'She sat with another group all day.', 'Maybe ask her kindly if something happened?'],
        ['We’re moving to a new city next month.', 'nervous', 'I won’t know anyone there.', 'Let’s plan a video call every week so we stay close.'],
        ['Someone posted a silly photo of me in the class group 😞', 'embarrassed', 'Everyone is laughing.', 'Let’s report it, tell a teacher and show your parents.', 1],
        ['My cricket bat broke right before the match.', 'frustrated', 'I saved up for it for months.', 'I can lend you mine for the match!'],
        ['My grandfather is in hospital.', 'scared', 'Mumma looked really worried.', 'Maybe make him a get-well card, and ask Mumma how he is doing?', 1],
        ['I forgot my lines in the school play.', 'embarrassed', 'People laughed a bit.', 'You did lots of parts really well — want me to help you practise for next time?']],
    s: [['Board exams are in a month and I feel like I know nothing.', 'overwhelmed', 'Every time I open a book I panic.', 'Let’s make a small day-by-day plan together — and tell a teacher or your parents if the panic doesn’t ease.', 1],
        ['I didn’t get into the college I wanted.', 'disappointed', 'Everyone keeps asking me about it.', 'Want to look at the other good options together?'],
        ['My parents are fighting a lot these days.', 'stressed', 'I can’t focus on anything.', 'Talking to the school counsellor could really help. I can go with you.', 1],
        ['My friend group made plans and left me out.', 'hurt', 'I saw the photos online.', 'Maybe talk honestly with one of them you trust?'],
        ['I messed up my first internship presentation.', 'embarrassed', 'My mind went blank in front of everyone.', 'Ask for feedback and let’s practise the next one together.'],
        ['My phone was stolen with all my notes on it.', 'upset', 'Exams start next week.', 'Tell your parents so you can block the SIM and report it — and I’ll share my notes.', 1],
        ['I keep comparing myself with toppers and feel useless.', 'low', 'Nothing I do feels good enough.', 'Try tracking your own progress week by week — and talk to a teacher or counsellor if it stays this heavy.', 1],
        ['My dog died yesterday.', 'heartbroken', 'He was with me for ten years.', 'Do you want to tell me your favourite memories of him?', 1]],
    p: [['I failed one group in my CA exam.', 'disappointed', 'Everyone at the office knows.', 'Let’s look at the marks paper by paper and plan the next attempt together.', 1],
        ['My articleship principal shouted at me in front of the client.', 'embarrassed', 'I made one small mistake in the file.', 'Maybe ask for a quick private chat to understand what to fix next time.'],
        ['I can’t balance articleship and studies. I’m so tired.', 'exhausted', 'I sleep four hours a night.', 'Let’s plan fixed study hours, and you could ask your principal about study leave.', 1],
        ['My batchmates all cleared and I didn’t.', 'left out', 'I keep seeing their celebration posts.', 'Your journey is your own — want to make a fresh study plan together?']]
  };
  function chat(b, lvl, orig) {
    const [m1, feel, m2, idea, serious] = pick(orig === 'p' ? CHAT.p.concat(CHAT.s.slice(4, 6)) : CHAT[b]), name = pick(NAMES);
    const T1 = [
      [`${feel === 'left out' ? 'That sounds hard — feeling left out really hurts' : `You sound really ${feel}`}. Do you want to tell me what happened?`, 3, 'You named the feeling and invited them to share — they feel heard.'],
      [pick(serious ? ['Everyone feels that sometimes, just move on.', 'Don’t think about it so much.'] : ['Cheer up, it’s not a big deal!', 'Don’t be silly, just forget it.', 'Stop worrying, it’s nothing.']), 0, 'Telling someone their feeling doesn’t matter makes them feel unheard.'],
      [pick(serious ? ['Anyway, did you see the match yesterday?', 'Something like that happened to me too, and mine was worse.'] : ['That’s nothing — something way worse happened to me!', 'Anyway, did you see the match yesterday?']), 0, 'Changing the topic or making it about yourself leaves them alone with the feeling.']];
    const T2 = [
      [`I’m here for you. ${idea}`, 3, 'You stayed kind and offered a helpful idea they can choose.'],
      [pick(['That’s life, deal with it.', 'Just stop thinking about it.']), 0, 'Brushing it off makes a hurting friend feel alone.'],
      [pick(['OK. Bye.', 'Hmm.', 'Whatever you say.']), 0, 'A cold one-word reply feels like you don’t care.']];
    return { g: 'chat', name, m1, m2, feel, t1: shuffle(T1.map(([w, s, why]) => ({ w, s, why }))), t2: shuffle(T2.map(([w, s, why]) => ({ w, s, why }))) };
  }

  /* ---------- 5. Choose Your Path (best choice = index 0; shuffled when played) ---------- */
  const PATHS = {
    j: [
      { t: 'The lost crayons', s: [
        ['You can’t find your crayons and art class is starting.', [['Ask the teacher calmly for help', 'The teacher lends you crayons. Phew!'], ['Sulk and refuse to try', 'You miss the fun drawing time.'], ['Grab crayons from a classmate', 'Your classmate gets upset.']]],
        ['Your friend Pari offers to share her crayons.', [['Say “Thank you!” and share nicely', 'Pari smiles. You draw together.'], ['Take all the best colours', 'Pari doesn’t want to share any more.'], ['Say “I don’t need yours”', 'You sit with no colours.']]],
        ['At home you find your crayons were in your bag pocket all along!', [['Laugh and make a “check my pockets” habit', 'Next time you find things fast.'], ['Blame your mother', 'Mumma feels sad.'], ['Throw the bag on the floor', 'Your lunch box breaks.']]]] },
      { t: 'The big race', s: [
        ['You trip and fall in the class race.', [['Get up, check your knee, and finish if it’s OK', 'Everyone cheers as you finish!'], ['Sit on the track and sulk', 'The race ends without you.'], ['Say the ground pushed you', 'Nobody believes it.']]],
        ['Your knee hurts a little.', [['Tell the teacher so it can be cleaned', 'A plaster and you feel better.'], ['Hide it and say nothing', 'It hurts more later.'], ['Shout at the runner next to you', 'They feel bad and confused.']]],
        ['Your friend Om came first.', [['Say “Well done, Om!”', 'Om is happy and invites you to play.'], ['Say “You only won because I fell”', 'Om feels hurt.'], ['Walk away without a word', 'You both feel awkward.']]]] },
      { t: 'The broken tower', s: [
        ['Your little brother knocks down your block tower.', [['Take a deep breath and count to five', 'You feel calmer.'], ['Push him', 'He cries and you get in trouble.'], ['Break his toy', 'Now two things are broken.']]],
        ['You feel calm now.', [['Tell him “Please be careful with my things”', 'He says sorry.'], ['Shout “I hate you!”', 'He cries and Mumma is upset.'], ['Never talk to him again', 'Playtime becomes lonely.']]],
        ['He wants to help build a new tower.', [['Let him help and give him a job', 'You build a super tall tower together!'], ['Say “Go away”', 'You build alone, and he is sad.'], ['Let him do it all alone', 'He gets stuck and gives up.']]]] }],
    m: [
      { t: 'The group project', s: [
        ['Your group project is due tomorrow and Rohan hasn’t done his part.', [['Message Rohan kindly to ask what’s wrong', 'Rohan says his grandfather was unwell. He’ll send it tonight.'], ['Complain about him in the class group', 'Rohan feels humiliated and stops replying.'], ['Do his part secretly and stay angry', 'You finish at midnight, tired and resentful.']]],
        ['Rohan’s part arrives but it has mistakes.', [['Suggest fixes together on a quick call', 'You fix it in 20 minutes and laugh about it.'], ['Rewrite it without telling him', 'Rohan notices and feels you don’t trust him.'], ['Submit it with the mistakes', 'The group loses marks.']]],
        ['The teacher praises your group’s work.', [['Thank the whole group, including Rohan', 'Everyone feels proud — Rohan most of all.'], ['Say you did most of the work', 'The group goes quiet and feels hurt.'], ['Say nothing and leave', 'Nobody feels the win together.']]]] },
      { t: 'The mean comment', s: [
        ['Someone comments “LOL ugly” under your photo online.', [['Don’t reply — take a screenshot, then block and report', 'You stay calm and keep proof.'], ['Reply with an even meaner comment', 'The fight grows and more people join in.'], ['Delete all your photos in panic', 'You feel worse and nothing changes.']]],
        ['You feel hurt and keep thinking about it.', [['Talk to a parent or trusted adult', 'They help you report it and you feel lighter.'], ['Keep it all to yourself', 'You can’t sleep properly for days.'], ['Ask friends to attack the person', 'It becomes bullying from your side too.']]],
        ['Next week you see the same person teased by others.', [['Don’t join in, and tell a teacher', 'You stopped harm — even to someone who hurt you.'], ['Join in to get even', 'You become what hurt you.'], ['Post about it to show it’s karma', 'Things get messier for everyone.']]]] },
      { t: 'The tryouts', s: [
        ['You are not selected for the school football team.', [['Feel it, then ask the coach what to improve', 'Coach gives you three clear tips.'], ['Say the coach is biased', 'Your friends get tired of hearing it.'], ['Stop playing for a while in anger', 'You miss the game you love.']]],
        ['Your friend got selected.', [['Congratulate them sincerely', 'They thank you and offer to practise with you.'], ['Avoid them for a week', 'The friendship feels strained.'], ['Tell them they were lucky', 'They feel hurt.']]],
        ['Next tryouts are in three months.', [['Make a weekly practice plan', 'You improve steadily and feel ready for the next tryouts.'], ['Practise only the day before', 'You feel unprepared and anxious.'], ['Wait and hope', 'Nothing changes.']]]] }],
    s: [
      { t: 'The exam slump', s: [
        ['Two weeks before boards, your mock score drops badly.', [['Analyse the mistakes and adjust your plan', 'You spot two weak chapters you can fix.'], ['Study all night every night', 'You get exhausted and your focus drops.'], ['Decide you’re just not smart enough', 'You stop trying, and anxiety grows.']]],
        ['You feel your chest tighten while studying.', [['Take slow breaths and a short walk — and tell a parent if it keeps happening', 'Your body calms and you can focus again.'], ['Drink three energy drinks', 'You feel jittery and can’t sleep.'], ['Scroll your phone for two hours', 'You feel guilty and more behind.']]],
        ['A friend messages: “I’m panicking too.”', [['Suggest studying together for an hour', 'You both feel supported and get more done.'], ['Say “Not my problem”', 'Your friend feels alone.'], ['Share scary rumours about the paper', 'Both of you panic more.']]]] },
      { t: 'The internship mistake', ca: 1, s: [
        ['At your internship you send a client the wrong file.', [['Tell your supervisor right away and offer a fix', 'They help you correct it before any harm.'], ['Hope nobody notices', 'The client complains the next day.'], ['Blame the system', 'Your supervisor trusts you less.']]],
        ['Your supervisor is irritated.', [['Stay calm, listen, and note what to do differently', 'They appreciate how you handle feedback.'], ['Argue that it wasn’t a big deal', 'The conversation gets tense.'], ['Go quiet and sulk all day', 'Your work suffers.']]],
        ['A new intern makes the same mistake later.', [['Quietly share the checklist you made', 'They avoid trouble and thank you.'], ['Laugh at them with others', 'The team culture gets worse.'], ['Report them to look good', 'You gain nothing and lose trust.']]]] },
      { t: 'The group chat storm', s: [
        ['Your friends start mocking a classmate in a group chat.', [['Say “Not cool, let’s stop” and save a screenshot for a teacher', 'Two friends agree and the chat moves on.'], ['Add a laughing emoji to fit in', 'The mocking gets worse.'], ['Forward it to others', 'It spreads across the school.']]],
        ['The classmate finds out and is upset.', [['Message them privately with support', 'They feel less alone.'], ['Pretend you weren’t in the chat', 'You feel uneasy for days.'], ['Tell them to toughen up', 'They feel even worse.']]],
        ['The teacher asks the class about it.', [['Be honest about what happened, calmly', 'The teacher handles it fairly and it stops.'], ['Deny everything', 'The truth comes out later.'], ['Blame one friend for all of it', 'The friendship breaks.']]]] }]
  };
  PATHS.p = [
      { t: 'The articleship deadline', s: [
        ['It’s 7 pm and the audit file is due tomorrow. You are only half done.', [['Tell your senior now and agree what to finish first', 'Your senior helps you prioritise. You finish the key parts.'], ['Stay quiet and hope to finish by morning', 'At 2 am you are exhausted and make errors.'], ['Copy last year’s working papers without checking', 'The numbers don’t match this year — big trouble.']]],
        ['Your friend calls to go out tonight.', [['Say no politely and plan to meet on Sunday', 'Your friend understands and you both look forward to Sunday.'], ['Go out and leave the file', 'The file is late and your principal is unhappy.'], ['Snap at your friend for calling', 'Your friend feels hurt.']]],
        ['Next morning the file goes in on time, with one small error found later.', [['Own the error and fix it quickly', 'Your principal trusts you more for being honest.'], ['Say the client sent wrong data', 'The truth comes out and trust drops.'], ['Hide it and hope', 'The error grows in the next stage.']]]] },
      { t: 'Results day', s: [
        ['ICAI results are out. You cleared one group but not the other.', [['Let yourself feel it, then look at your marks calmly', 'You spot exactly which paper pulled you down.'], ['Delete your study apps in anger', 'You lose your notes and plans.'], ['Stop talking to everyone for days', 'You feel more alone.']]],
        ['A relative says, “Others cleared in the first attempt.”', [['Reply calmly, “Everyone’s journey is different. I have a plan.”', 'The conversation ends politely.'], ['Argue loudly at the family dinner', 'Everyone gets upset.'], ['Agree that you are a failure', 'You feel worse and lose confidence.']]],
        ['Your batchmate who cleared offers to share notes.', [['Thank them and make a study plan', 'You start the next attempt with energy.'], ['Refuse because you feel jealous', 'You miss useful help.'], ['Say you don’t need anyone', 'You study alone and get stuck.']]]] }];
  function paths(b, lvl, orig) {
    const st = pick(orig === 'p' ? PATHS.p.concat(PATHS.s.filter(x => x.ca)) : PATHS[b]);

    return { g: 'paths', title: st.t, steps: st.s.map(([sit, opts]) => ({ sit, opts: shuffle(opts.map(([w, res], i) => ({ w, res, best: i === 0 }))) })) };
  }

  /* ---------- 6. Calm Breath ---------- */
  function breathe(b, lvl) {
    const inh = b === 'j' ? 3 : 4, exh = b === 'j' ? 3 : lvl >= 3 ? 6 : 4, cycles = b === 'j' ? 3 : lvl >= 4 ? 5 : 4;
    return { g: 'breathe', inh, exh, cycles, tol: b === 'j' ? 1.2 : b === 'm' ? 1 : .8 };
  }

  const MAKERS = { faces, thermo, shoes, chat, paths, breathe };
  const API = { MAKERS, make: (g, b, lvl) => MAKERS[g](b === 'p' ? 's' : b, Math.max(1, Math.min(5, lvl)), b), FACE, SIT, FAR, SCALES, SHOES, CHAT, PATHS, STICK };
  if (typeof module !== 'undefined' && module.exports) module.exports = API; else root.HeartPlayGen = API;
})(typeof window !== 'undefined' ? window : this);
