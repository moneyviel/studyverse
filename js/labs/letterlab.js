/* StudyVerse lab: letterlab — alphabet / varnamala explorer (Grades 1-2, English & Hindi)
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *  script     string   'en' (English a–z) or 'hi' (Hindi स्वर + व्यंजन)                  default 'en'
 *  set        string   which letters: 'all' | 'vowels' (स्वर) | 'consonants' (व्यंजन)    default 'all'
 *  only       array    restrict to these letters, e.g. ['क','ख','ग','घ'] or ['a','b','c'] default none
 *  letters    array    custom letter data replacing the built-in list. Each item:
 *                      { l:'क', v:false, words:[['कबूतर','🕊️'],['केला','🍌']] }
 *                      (l = letter, v = true if vowel/स्वर, words = [word, emoji] pairs)    default built-in
 *  mode       string   challenge: 'find'  = which letter starts this word?
 *                                 'case'  = match UPPER to lower case (English only)
 *                                 'sort'  = put letters in Vowel / Consonant bin          default 'find'
 *  rounds     number   correct answers needed to win (case mode: pairs on the board)     default 5
 *  start      string   tab shown first: 'explore' | 'play'                                default 'explore'
 *  challenge  string   the "🎯 Challenge" line (any language)                             default auto
 *
 * The child: taps letters to hear them and see example words (Explore), then plays the
 * chosen mode (Play). Win = `rounds` correct answers (or a fully matched case board).
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  // ---- built-in English data: letter, words [word, emoji]
  const EN = [
    ['a', [['apple', '🍎'], ['ant', '🐜'], ['axe', '🪓']]], ['b', [['ball', '⚽'], ['bus', '🚌'], ['bat', '🦇']]],
    ['c', [['cat', '🐱'], ['cup', '☕'], ['cake', '🎂']]], ['d', [['dog', '🐶'], ['duck', '🦆'], ['drum', '🥁']]],
    ['e', [['egg', '🥚'], ['elephant', '🐘'], ['envelope', '✉️']]], ['f', [['fish', '🐟'], ['frog', '🐸'], ['flower', '🌸']]],
    ['g', [['goat', '🐐'], ['grapes', '🍇'], ['gift', '🎁']]], ['h', [['hat', '🎩'], ['hen', '🐔'], ['house', '🏠']]],
    ['i', [['ink', '🖋️'], ['insect', '🐞'], ['ice', '🧊']]], ['j', [['jeep', '🚙'], ['juice', '🧃'], ['jet', '✈️']]],
    ['k', [['kite', '🪁'], ['key', '🔑'], ['king', '🤴']]], ['l', [['lion', '🦁'], ['leaf', '🍃'], ['lemon', '🍋']]],
    ['m', [['mango', '🥭'], ['moon', '🌙'], ['monkey', '🐒']]], ['n', [['nose', '👃'], ['nut', '🥜'], ['net', '🥅']]],
    ['o', [['orange', '🍊'], ['owl', '🦉'], ['ox', '🐂']]], ['p', [['parrot', '🦜'], ['pen', '🖊️'], ['pig', '🐷']]],
    ['q', [['queen', '👸'], ['question', '❓']]], ['r', [['rabbit', '🐇'], ['rose', '🌹'], ['rain', '🌧️']]],
    ['s', [['sun', '☀️'], ['star', '⭐'], ['snake', '🐍']]], ['t', [['tiger', '🐯'], ['tree', '🌳'], ['train', '🚆']]],
    ['u', [['umbrella', '☂️'], ['unicorn', '🦄'], ['up', '⬆️']]], ['v', [['van', '🚐'], ['violin', '🎻'], ['vase', '🏺']]],
    ['w', [['watch', '⌚'], ['whale', '🐳'], ['window', '🪟']]], ['x', [['xylophone', '🎼'], ['fox', '🦊'], ['box', '📦']]],
    ['y', [['yak', '🐃'], ['yo-yo', '🪀'], ['yacht', '⛵']]], ['z', [['zebra', '🦓'], ['zero', '0️⃣'], ['zip', '🤐']]]
  ].map(([l, words]) => ({ l, v: 'aeiou'.includes(l), words, noSort: l === 'y' }));

  // ---- built-in Hindi data (स्वर then व्यंजन). noStart = letter that (almost) never begins a word.
  const HV = [
    ['अ', [['अनानास', '🍍'], ['अखबार', '📰']]], ['आ', [['आम', '🥭'], ['आग', '🔥'], ['आलू', '🥔']]],
    ['इ', [['इमारत', '🏢'], ['इंजन', '🚂']]], ['ई', [['ईंट', '🧱'], ['ईद', '🌙']]],
    ['उ', [['उल्लू', '🦉'], ['उँगली', '☝️']]], ['ऊ', [['ऊँट', '🐪'], ['ऊन', '🧶']]],
    ['ऋ', [['ऋषि', '🧘'], ['ऋतु', '🌦️']]], ['ए', [['एक', '1️⃣'], ['एड़ी', '🦶']]],
    ['ऐ', [['ऐनक', '👓'], ['ऐरावत', '🐘']]], ['ओ', [['ओस', '💧'], ['ओला', '🧊']]],
    ['औ', [['औरत', '👩'], ['औज़ार', '🔧']]],
    ['अं', [['अंगूर', '🍇'], ['अंडा', '🥚']], 1], ['अः', [['प्रातः', '🌅'], ['दुःख', '😢']], 2]
  ].map(([l, words, f]) => ({ l, v: true, words, noSort: !!f, noStart: f === 2 }));
  const HC = [
    ['क', [['कबूतर', '🕊️'], ['केला', '🍌'], ['कप', '☕']]], ['ख', [['खरगोश', '🐇'], ['खाना', '🍛']]],
    ['ग', [['गाय', '🐄'], ['गेंद', '⚽'], ['गमला', '🪴']]], ['घ', [['घर', '🏠'], ['घड़ी', '⌚'], ['घोड़ा', '🐎']]],
    ['ङ', [['रंग (रङ्ग)', '🎨'], ['पंख (पङ्ख)', '🪶']], 1],
    ['च', [['चम्मच', '🥄'], ['चश्मा', '👓'], ['चाँद', '🌙']]], ['छ', [['छतरी', '☂️'], ['छिपकली', '🦎']]],
    ['ज', [['जहाज़', '🚢'], ['जूता', '👞']]], ['झ', [['झंडा', '🚩'], ['झरना', '🏞️']]],
    ['ञ', [['पंजा (पञ्जा)', '🖐️']], 1],
    ['ट', [['टमाटर', '🍅'], ['टोपी', '🧢']]], ['ठ', [['ठेला', '🛒'], ['ठंड', '🥶']]],
    ['ड', [['डाकिया', '📮'], ['डलिया', '🧺']]], ['ढ', [['ढोल', '🥁'], ['ढाल', '🛡️']]],
    ['ण', [['बाण', '🏹'], ['गणित', '➗']], 1],
    ['त', [['तरबूज़', '🍉'], ['तितली', '🦋'], ['तारा', '⭐']]], ['थ', [['थाली', '🍽️'], ['थैला', '👜']]],
    ['द', [['दरवाज़ा', '🚪'], ['दाँत', '🦷'], ['दूध', '🥛']]], ['ध', [['धनुष', '🏹'], ['धूप', '☀️']]],
    ['न', [['नल', '🚰'], ['नाव', '⛵'], ['नाक', '👃']]],
    ['प', [['पेड़', '🌳'], ['पत्ता', '🍃'], ['पतंग', '🪁']]], ['फ', [['फूल', '🌸'], ['फल', '🍇']]],
    ['ब', [['बकरी', '🐐'], ['बत्तख', '🦆'], ['बस', '🚌']]], ['भ', [['भालू', '🐻'], ['भेड़', '🐑']]],
    ['म', [['मछली', '🐟'], ['मोर', '🦚'], ['मकान', '🏠']]],
    ['य', [['योग', '🧘'], ['यान', '🚀']]], ['र', [['रेल', '🚆'], ['राजा', '🤴']]],
    ['ल', [['लड़का', '👦'], ['लालटेन', '🏮']]], ['व', [['वन', '🌲'], ['वर्षा', '🌧️']]],
    ['श', [['शेर', '🦁'], ['शहद', '🍯']]], ['ष', [['षट्कोण', '⬡'], ['धनुष', '🏹']]],
    ['स', [['सेब', '🍎'], ['साँप', '🐍'], ['सूरज', '☀️']]], ['ह', [['हाथी', '🐘'], ['हिरन', '🦌']]],
    ['क्ष', [['क्षत्रिय', '🛡️'], ['कक्षा', '🏫']]], ['त्र', [['त्रिशूल', '🔱'], ['त्रिभुज', '🔺']]],
    ['ज्ञ', [['ज्ञानी', '🧙'], ['यज्ञ', '🔥']]], ['श्र', [['श्रमिक', '👷']]]
  ].map(([l, words, f]) => ({ l, v: false, words, noStart: !!f }));
  const HI = HV.concat(HC);

  const isDeva = s => /[ऀ-ॿ]/.test(s);
  const plain = w => String(w).replace(/\s*\(.*\)\s*/g, '');            // "रंग (रङ्ग)" -> "रंग"
  const COMB = /[ऀ-ःऺ-ॏ॑-ॗॢॣ‌‍]/;
  // does word start with letter l? (conjunct letters like क्ष must match fully and not be followed by halant)
  function startsWith(word, l) {
    word = plain(word).toLowerCase(); l = String(l).toLowerCase();
    if (!word.startsWith(l)) return false;
    const nx = word.charAt(l.length);
    if (!isDeva(l)) return true;
    if (nx === '्') return false;                                   // क् + ष = क्ष, not क
    if (/^[अ-औ]$/.test(l) && /[ंः]/.test(nx) && l.length === 1) return false; // अं / अः are separate
    return true;
  }
  // hide the first akshara of a word: केला -> ?ला , क्षत्रिय -> ?त्रिय
  function hideFirst(word, l) {
    word = plain(word);
    let i = String(l).length;
    while (i < word.length && COMB.test(word[i])) i++;
    return { hidden: word.slice(0, i), rest: word.slice(i) };
  }

  Labs.register('letterlab', {
    title: 'Letter lab',
    subjects: ['english', 'hindi'],
    render(host, p, api) {
      const script = p.script === 'hi' ? 'hi' : 'en';
      let L = Array.isArray(p.letters) && p.letters.length ? p.letters.map(x => ({ l: String(x.l || x.letter || ''), v: !!x.v, words: (x.words || []).filter(w => Array.isArray(w) && w[0]), noSort: !!x.noSort })).filter(x => x.l) : (script === 'hi' ? HI : EN);
      if (p.set === 'vowels') L = L.filter(x => x.v); else if (p.set === 'consonants') L = L.filter(x => !x.v);
      if (Array.isArray(p.only) && p.only.length) { const o = p.only.map(String); const f = L.filter(x => o.includes(x.l)); if (f.length) L = f; }
      if (!L.length) L = script === 'hi' ? HI : EN;
      const hindi = L.some(x => isDeva(x.l));
      let mode = ['find', 'case', 'sort'].includes(p.mode) ? p.mode : 'find';
      if (mode === 'case' && hindi) mode = 'find';                        // Hindi has no capital letters
      if (mode === 'sort' && (!L.some(x => x.v) || !L.some(x => !x.v))) mode = 'find';
      const rounds = Math.max(1, Math.min(20, parseInt(p.rounds, 10) || 5));
      const vName = hindi ? 'स्वर' : 'Vowel', cName = hindi ? 'व्यंजन' : 'Consonant';
      const defCh = { find: `Find the first letter of ${rounds} words`, case: `Match each BIG letter to its small letter`, sort: `Sort ${rounds} letters into ${vName} and ${cName}` }[mode];
      const show = l => hindi ? l : l.toUpperCase() + ' ' + l;
      const sayLetter = x => {
        const w = x.words[0];
        if (hindi) api.speak(w ? `${x.l}. ${x.l} से ${plain(w[0])}` : x.l);
        else api.speak(w ? `${x.l.toUpperCase()}. ${x.l.toUpperCase()} for ${w[0]}` : x.l.toUpperCase());
      };
      const timers = [];
      const later = (f, ms) => timers.push(setTimeout(f, ms));

      host.innerHTML = `<style>
.lb-letterlab-w{font-size:15px;color:#1b1f3a;user-select:none;-webkit-user-select:none}
.lb-letterlab-ch{font-weight:800;margin:0 0 8px;line-height:1.3}
.lb-letterlab-tabs{display:flex;background:#f1effb;border-radius:14px;padding:4px;gap:4px;margin-bottom:10px}
.lb-letterlab-tab{flex:1;border:0;background:transparent;border-radius:11px;min-height:40px;font:inherit;font-weight:800;color:#6b7090;cursor:pointer}
.lb-letterlab-tab.on{background:#fff;color:#8b5cf6;box-shadow:0 2px 6px rgba(139,92,246,.18)}
.lb-letterlab-pane{min-height:280px}
.lb-letterlab-card{display:flex;gap:12px;align-items:center;background:linear-gradient(135deg,#f5f0ff,#eafff8);border-radius:18px;padding:10px 12px;min-height:96px}
.lb-letterlab-big{min-width:84px;height:84px;border-radius:20px;background:#fff;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:800;color:#8b5cf6;box-shadow:0 3px 0 #e4dcfb;cursor:pointer;border:0;font-family:inherit;padding:0 8px}
.lb-letterlab-big.v{color:#ff6b6b;box-shadow:0 3px 0 #ffd9d9}
.lb-letterlab-words{display:flex;flex-wrap:wrap;gap:6px;flex:1}
.lb-letterlab-word{border:0;background:#fff;border-radius:12px;padding:6px 9px;min-height:40px;font:inherit;font-weight:700;color:#1b1f3a;cursor:pointer;display:flex;align-items:center;gap:5px}
.lb-letterlab-word b{color:#8b5cf6}
.lb-letterlab-word span{font-size:22px}
.lb-letterlab-tag{font-size:12px;font-weight:800;color:#6b7090;margin-top:3px}
.lb-letterlab-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(44px,1fr));gap:6px;margin-top:10px;max-height:206px;overflow-y:auto;padding:2px}
.lb-letterlab-key{height:44px;border:0;border-radius:12px;background:#f3f4fb;font:inherit;font-size:20px;font-weight:800;color:#1b1f3a;cursor:pointer;transition:transform .15s,background .15s}
.lb-letterlab-key.v{background:#fff0f0;color:#e14d4d}
.lb-letterlab-key.on{background:#8b5cf6;color:#fff;transform:scale(1.08)}
.lb-letterlab-legend{display:flex;gap:12px;font-size:12px;color:#6b7090;font-weight:700;margin-top:6px}
.lb-letterlab-legend i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:4px;vertical-align:-1px}
.lb-letterlab-score{display:flex;gap:5px;justify-content:center;margin:2px 0 10px}
.lb-letterlab-dot{width:14px;height:14px;border-radius:50%;background:#e8e9f3;transition:background .3s,transform .3s}
.lb-letterlab-dot.on{background:#2ed3a5;transform:scale(1.15)}
.lb-letterlab-q{text-align:center;background:#fffaf0;border-radius:18px;padding:12px 8px}
.lb-letterlab-emo{font-size:58px;line-height:1.1}
.lb-letterlab-qw{font-size:28px;font-weight:800;letter-spacing:1px;margin-top:4px}
.lb-letterlab-qw u{display:inline-block;min-width:30px;border-bottom:4px solid #ffc93c;text-decoration:none;color:#ffc93c}
.lb-letterlab-opts{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.lb-letterlab-opt{height:58px;border:0;border-radius:16px;background:#fff;box-shadow:0 3px 0 #dcdff0,inset 0 0 0 2px #e8e9f3;font:inherit;font-size:28px;font-weight:800;color:#1b1f3a;cursor:pointer}
.lb-letterlab-opt.ok{background:#2ed3a5;color:#fff;box-shadow:0 3px 0 #1fa983}
.lb-letterlab-opt.no{background:#ff6b6b;color:#fff;box-shadow:0 3px 0 #d94b4b;animation:lb-letterlab-shk .4s}
@keyframes lb-letterlab-shk{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
@keyframes lb-letterlab-pop{from{transform:scale(.6);opacity:0}to{transform:scale(1);opacity:1}}
.lb-letterlab-pop{animation:lb-letterlab-pop .35s cubic-bezier(.2,1.5,.4,1)}
.lb-letterlab-row{display:flex;gap:8px;justify-content:center;margin:8px 0}
.lb-letterlab-tile{flex:1;max-width:62px;height:62px;border:0;border-radius:16px;font:inherit;font-size:30px;font-weight:800;cursor:pointer;transition:transform .15s,background .2s,opacity .3s}
.lb-letterlab-tile.up{background:#efe8ff;color:#7c4dea}
.lb-letterlab-tile.lo{background:#e5f8ff;color:#2a6fd6}
.lb-letterlab-tile.sel{transform:translateY(-4px) scale(1.06);box-shadow:0 0 0 3px #ffc93c}
.lb-letterlab-tile.done{background:#2ed3a5;color:#fff;opacity:.75;cursor:default}
.lb-letterlab-tile.no{animation:lb-letterlab-shk .4s;background:#ffe1e1}
.lb-letterlab-hint{text-align:center;color:#6b7090;font-size:13px;font-weight:700;margin:6px 0}
.lb-letterlab-sortbox{position:relative;height:120px;display:flex;align-items:center;justify-content:center;touch-action:none}
.lb-letterlab-drag{width:88px;height:88px;border-radius:24px;background:#fff;box-shadow:0 5px 0 #dcdff0,inset 0 0 0 3px #ece9fb;display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:800;cursor:grab;touch-action:none;position:relative;z-index:2}
.lb-letterlab-drag.go{transition:transform .3s,opacity .3s}
.lb-letterlab-bins{display:flex;gap:10px}
.lb-letterlab-bin{flex:1;min-height:104px;border:3px dashed;border-radius:20px;font:inherit;font-weight:800;font-size:17px;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding:8px 6px;gap:4px;transition:transform .15s}
.lb-letterlab-bin.vb{border-color:#ff9a9a;background:#fff5f5;color:#e14d4d}
.lb-letterlab-bin.cb{border-color:#9ec0ff;background:#f3f7ff;color:#2a6fd6}
.lb-letterlab-bin.hot{transform:scale(1.04)}
.lb-letterlab-bin small{display:flex;flex-wrap:wrap;gap:3px;justify-content:center;font-size:15px;color:#1b1f3a}
.lb-letterlab-btn{border:0;border-radius:14px;min-height:42px;padding:0 16px;font:inherit;font-weight:800;background:#f1effb;color:#8b5cf6;cursor:pointer}
</style>
<div class="lb-letterlab-w">
  <div class="lb-letterlab-ch">🎯 Challenge: ${esc(p.challenge || defCh)}</div>
  <div class="lb-letterlab-tabs"><button class="lb-letterlab-tab" data-t="explore">🔤 Explore</button><button class="lb-letterlab-tab" data-t="play">🎮 Play</button></div>
  <div class="lb-letterlab-pane"></div>
</div>`;
      const pane = host.querySelector('.lb-letterlab-pane');
      const tabs = host.querySelectorAll('.lb-letterlab-tab');
      let tab = p.start === 'play' ? 'play' : 'explore';
      let cur = L[0], score = 0, won = false;
      let cleanupPane = null;

      const dots = () => `<div class="lb-letterlab-score">${Array.from({ length: rounds }, (_, i) => `<i class="lb-letterlab-dot${i < score ? ' on' : ''}"></i>`).join('')}</div>`;
      function gotPoint(msg) {
        score++;
        if (score >= rounds && !won) { won = true; later(() => api.win(msg), 500); }
      }

      // ---------- Explore ----------
      function explore() {
        pane.innerHTML = `<div class="lb-letterlab-card"></div>
          <div class="lb-letterlab-grid">${L.map((x, i) => `<button class="lb-letterlab-key${x.v ? ' v' : ''}" data-i="${i}">${esc(x.l)}</button>`).join('')}</div>
          <div class="lb-letterlab-legend"><span><i style="background:#ffb3b3"></i>${vName}</span><span><i style="background:#dfe1ee"></i>${cName}</span><span>Tap a letter or word to hear it</span></div>`;
        const card = pane.querySelector('.lb-letterlab-card');
        function showCard(x, say) {
          cur = x;
          pane.querySelectorAll('.lb-letterlab-key').forEach(k => k.classList.toggle('on', L[k.dataset.i] === x));
          card.innerHTML = `<button class="lb-letterlab-big${x.v ? ' v' : ''} lb-letterlab-pop">${esc(show(x.l))}</button>
            <div style="flex:1"><div class="lb-letterlab-words">${x.words.map((w, i) => {
              const h = startsWith(w[0], x.l) ? hideFirst(w[0], x.l) : null;
              return `<button class="lb-letterlab-word" data-w="${i}"><span>${esc(w[1] || '')}</span><em style="font-style:normal">${h ? `<b>${esc(h.hidden)}</b>${esc(h.rest)}` : esc(w[0])}</em></button>`;
            }).join('')}</div>
            <div class="lb-letterlab-tag">${x.v ? vName : cName}${x.noStart ? ' · rarely starts a word' : ''}</div></div>`;
          card.querySelector('.lb-letterlab-big').onclick = () => { api.sfx('tap'); sayLetter(x); };
          card.querySelectorAll('.lb-letterlab-word').forEach(b => b.onclick = () => { api.sfx('tap'); api.speak(plain(x.words[b.dataset.w][0])); });
          if (say) sayLetter(x);
        }
        pane.querySelectorAll('.lb-letterlab-key').forEach(k => k.onclick = () => { api.sfx('tap'); showCard(L[k.dataset.i], true); });
        showCard(cur, false);
      }

      // ---------- Play: find the first letter ----------
      function playFind() {
        const pool = [];
        L.forEach(x => x.words.forEach(w => { if (!x.noStart && startsWith(w[0], x.l)) pool.push({ x, w }); }));
        if (!pool.length) { pane.innerHTML = '<div class="lb-letterlab-hint">No words to play with.</div>'; return; }
        let order = shuffle(pool), qi = 0, locked = false;
        function ask() {
          const q = order[qi % order.length]; qi++;
          const h = hideFirst(q.w[0], q.x.l);
          const others = shuffle(L.filter(y => y.l !== q.x.l && !startsWith(q.w[0], y.l))).slice(0, 3);
          const opts = shuffle([q.x].concat(others));
          locked = false;
          pane.innerHTML = dots() + `<div class="lb-letterlab-q lb-letterlab-pop"><div class="lb-letterlab-emo">${esc(q.w[1] || '❓')}</div>
            <div class="lb-letterlab-qw"><u>?</u>${esc(h.rest)}</div>
            <div class="lb-letterlab-hint">Which letter does it start with? <button class="lb-letterlab-btn" style="min-height:34px;padding:0 10px">🔊</button></div></div>
            <div class="lb-letterlab-opts">${opts.map(o => `<button class="lb-letterlab-opt" data-l="${esc(o.l)}">${esc(hindi ? o.l : o.l)}</button>`).join('')}</div>`;
          pane.querySelector('.lb-letterlab-q .lb-letterlab-btn').onclick = () => api.speak(plain(q.w[0]));
          later(() => api.speak(plain(q.w[0])), 300);
          pane.querySelectorAll('.lb-letterlab-opt').forEach(b => b.onclick = () => {
            if (locked) return;
            if (b.dataset.l === q.x.l) {
              locked = true; b.classList.add('ok'); api.sfx('correct');
              const u = pane.querySelector('.lb-letterlab-qw u'); u.textContent = h.hidden; u.style.color = '#2ed3a5'; u.style.borderColor = '#2ed3a5';
              api.speak(hindi ? `${q.x.l} से ${plain(q.w[0])}` : `${q.x.l.toUpperCase()} for ${q.w[0]}`);
              gotPoint(hindi ? `शाबाश! You found ${rounds} first letters.` : `Super! You found the first letter of ${rounds} words.`);
              pane.querySelectorAll('.lb-letterlab-dot')[score - 1] && pane.querySelectorAll('.lb-letterlab-dot')[score - 1].classList.add('on');
              later(ask, 1300);
            } else { b.classList.remove('no'); void b.offsetWidth; b.classList.add('no'); api.sfx('wrong'); }
          });
        }
        ask();
      }

      // ---------- Play: upper / lower case board ----------
      function playCase() {
        const n = Math.max(3, Math.min(5, rounds, L.length));
        const pick = shuffle(L).slice(0, n);
        const ups = shuffle(pick), los = shuffle(pick);
        let sel = null, done = 0;
        pane.innerHTML = `<div class="lb-letterlab-hint">Tap a BIG letter, then its small letter</div>
          <div class="lb-letterlab-row">${ups.map(x => `<button class="lb-letterlab-tile up" data-l="${esc(x.l)}">${esc(x.l.toUpperCase())}</button>`).join('')}</div>
          <div style="text-align:center;font-size:22px;color:#c9cbe0">⇅</div>
          <div class="lb-letterlab-row">${los.map(x => `<button class="lb-letterlab-tile lo" data-l="${esc(x.l)}">${esc(x.l.toLowerCase())}</button>`).join('')}</div>
          <div class="lb-letterlab-hint lb-letterlab-st">Matched 0 of ${n}</div>
          <div style="text-align:center;margin-top:10px"><button class="lb-letterlab-btn lb-letterlab-new">🔀 New letters</button></div>`;
        const st = pane.querySelector('.lb-letterlab-st');
        pane.querySelector('.lb-letterlab-new').onclick = () => { api.sfx('tap'); playCase(); };
        pane.querySelectorAll('.lb-letterlab-tile').forEach(t => t.onclick = () => {
          if (t.classList.contains('done')) return;
          const isUp = t.classList.contains('up');
          if (!sel || sel.classList.contains('up') === isUp) {
            if (sel) sel.classList.remove('sel');
            sel = t; t.classList.add('sel'); api.sfx('tap'); api.speak(t.dataset.l.toUpperCase());
            return;
          }
          if (sel.dataset.l === t.dataset.l) {
            [sel, t].forEach(e => { e.classList.remove('sel'); e.classList.add('done'); });
            api.sfx('correct'); done++; st.textContent = `Matched ${done} of ${n}`;
            api.speak(`${t.dataset.l.toUpperCase()} and small ${t.dataset.l}`);
            if (done === n && !won) { won = true; later(() => api.win(`All ${n} pairs matched — capital and small letters!`), 400); }
          } else { t.classList.remove('no'); void t.offsetWidth; t.classList.add('no'); api.sfx('wrong'); }
          sel && sel.classList.remove('sel'); sel = null;
        });
      }

      // ---------- Play: vowel / consonant sort (drag or tap a bin) ----------
      function playSort() {
        const pool = L.filter(x => !x.noSort);
        let queue = shuffle(pool), qi = 0, x = null, busy = false;
        const placed = { v: [], c: [] };
        pane.innerHTML = dots() + `<div class="lb-letterlab-hint">Drag the letter into the right box (or tap a box)</div>
          <div class="lb-letterlab-sortbox"><div class="lb-letterlab-drag"></div></div>
          <div class="lb-letterlab-bins"><button class="lb-letterlab-bin vb" data-b="v">${vName}<small></small></button><button class="lb-letterlab-bin cb" data-b="c">${cName}<small></small></button></div>`;
        const tile = pane.querySelector('.lb-letterlab-drag');
        const bins = pane.querySelectorAll('.lb-letterlab-bin');
        function next() {
          if (qi >= queue.length) { queue = shuffle(pool); qi = 0; }
          x = queue[qi++]; busy = false;
          tile.classList.remove('go'); tile.style.transform = ''; tile.style.opacity = '1';
          tile.textContent = hindi ? x.l : x.l.toUpperCase() + x.l;
          tile.classList.remove('lb-letterlab-pop'); void tile.offsetWidth; tile.classList.add('lb-letterlab-pop');
        }
        function drop(b) {
          if (busy || won) return;
          const ok = (b === 'v') === x.v;
          const bin = pane.querySelector(`[data-b="${b}"]`);
          if (ok) {
            busy = true; api.sfx('correct'); api.speak(x.l);
            const r1 = tile.getBoundingClientRect(), r2 = bin.getBoundingClientRect();
            tile.classList.add('go');
            tile.style.transform = `translate(${r2.left + r2.width / 2 - r1.left - r1.width / 2}px,${r2.top + r2.height / 2 - r1.top - r1.height / 2}px) scale(.3)`; tile.style.opacity = '0';
            placed[b].push(x.l); if (placed[b].length > 8) placed[b].shift();
            bin.querySelector('small').textContent = placed[b].join(' ');
            gotPoint(hindi ? `बहुत बढ़िया! ${rounds} letters sorted into ${vName} and ${cName}.` : `Great sorting! ${rounds} letters in the right box.`);
            const d = pane.querySelectorAll('.lb-letterlab-dot')[score - 1]; d && d.classList.add('on');
            later(next, 450);
          } else {
            api.sfx('wrong'); tile.classList.add('go'); tile.style.transform = '';
            bin.classList.remove('lb-letterlab-pop'); bin.style.animation = 'lb-letterlab-shk .4s'; later(() => { bin.style.animation = ''; }, 420);
            later(() => tile.classList.remove('go'), 320);
          }
        }
        bins.forEach(b => b.onclick = () => drop(b.dataset.b));
        let drag = null;
        const binAt = (cx, cy) => { let hit = null; bins.forEach(b => { const r = b.getBoundingClientRect(); if (cx >= r.left && cx <= r.right && cy >= r.top - 20 && cy <= r.bottom) hit = b; }); return hit; };
        tile.addEventListener('pointerdown', e => { if (busy) return; drag = { x: e.clientX, y: e.clientY }; tile.classList.remove('go'); try { tile.setPointerCapture(e.pointerId); } catch (_) {} });
        tile.addEventListener('pointermove', e => {
          if (!drag) return;
          tile.style.transform = `translate(${e.clientX - drag.x}px,${e.clientY - drag.y}px) scale(1.05)`;
          const h = binAt(e.clientX, e.clientY); bins.forEach(b => b.classList.toggle('hot', b === h));
        });
        const end = e => {
          if (!drag) return;
          const moved = Math.hypot(e.clientX - drag.x, e.clientY - drag.y); drag = null;
          bins.forEach(b => b.classList.remove('hot'));
          const h = binAt(e.clientX, e.clientY);
          if (h && moved > 10) drop(h.dataset.b);
          else { tile.classList.add('go'); tile.style.transform = ''; if (moved <= 10) api.speak(x.l); }
        };
        tile.addEventListener('pointerup', end); tile.addEventListener('pointercancel', end);
        next();
      }

      function setTab(t) {
        tab = t; tabs.forEach(b => b.classList.toggle('on', b.dataset.t === t));
        timers.forEach(clearTimeout); timers.length = 0;
        if (t === 'explore') explore();
        else if (mode === 'case') playCase(); else if (mode === 'sort') playSort(); else playFind();
      }
      tabs.forEach(b => b.onclick = () => { api.sfx('tap'); setTab(b.dataset.t); });
      setTab(tab);
      return () => { timers.forEach(clearTimeout); timers.length = 0; host.innerHTML = ''; };
    },
    example: {
      script: 'en', set: 'all', mode: 'find', rounds: 5, start: 'explore',
      challenge: 'Find the first letter of 5 picture words'
    },
    examples: [
      { script: 'hi', set: 'all', mode: 'sort', rounds: 6, start: 'play', challenge: 'स्वर और व्यंजन अलग करो — sort 6 letters' },
      { script: 'en', set: 'all', mode: 'case', rounds: 5, start: 'play', challenge: 'Match capital letters to small letters' },
      { script: 'hi', set: 'consonants', only: ['क', 'ख', 'ग', 'घ', 'च', 'छ', 'ज', 'झ', 'ट', 'त', 'प', 'ब', 'म'], mode: 'find', rounds: 4, start: 'play', challenge: 'चित्र देखो — पहला अक्षर चुनो (4 words)' }
    ]
  });
})();
