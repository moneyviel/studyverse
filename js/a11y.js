/* ================= StudyVerse accessibility layer =================
   For blind and low-vision children (and young children who cannot read yet).
   Loaded last; it adds to the existing screens without changing how they look for sighted users.
   1. Screen readers: names for every control, roles, dialogs (focus moved in and back, Escape closes,
      background made inert), keyboard-operable maps, focus moved to each new screen's heading,
      results announced in a live region.
   2. Listen mode ("Talk to me"): every screen is read aloud, choices are numbered, a big hold-to-talk
      button and voice commands everywhere ("next", "repeat", "read the lesson", "open maths", "help"…),
      spoken step-by-step solutions after each answer, Hindi voice + recognition for Hindi/Sanskrit.
   3. Labs: a spoken description of every lab type, narration of what changes, and sonification
      (graphs as rising/falling tones, bars as notes, numbers as counted beeps, sliders as pitch).
   4. Games playable by sound + number keys/voice; timers can get extra time or be switched off,
      and they wait while the app is talking.
   5. Haptics: two short buzzes = right, one long = wrong, a tick = new screen.
   6. First launch: any key, a screen reader, or saying "listen" offers to turn Listen mode on. */
(function () {
  'use strict';
  const D = document;
  const U = () => (window.UX && UX.state) || {};
  const listenOn = () => !!U().listen;
  const g = name => { try { return ({ ST: () => ST, NAV: () => NAV, RUN: () => RUN, CUR: () => CUR })[name](); } catch (e) { return null; } };
  const $1 = (s, r = D) => r.querySelector(s);
  const $$ = (s, r = D) => [...r.querySelectorAll(s)];
  const visible = el => !!el && el.isConnected && el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden' && !el.closest('[hidden],[inert]');
  const activeScreen = () => $1('.screen.active');
  const SHEETS = '.sheet, .asksheet';
  /* the full-screen Parent Hub is the bottom layer: a sheet opened over it (higher z-index) is the top one */
  const openSheet = () => { const l = $$(SHEETS).filter(s => s.classList.contains('show')); return l.filter(s => !s.classList.contains('pv-hub')).pop() || l.pop() || null; };
  const scope = () => openSheet() || activeScreen() || D.body;
  const FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]):not([type=hidden]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"]),summary';
  const now = () => Date.now();
  const DEVA = /[ऀ-ॿ]/;

  /* ---------------- text helpers ---------------- */
  const EMO = /(?:[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{1F1E6}-\u{1F1FF}\u{2300}-\u{23FF}\u{25A0}-\u{25FF}\u{2190}-\u{21FF}\u{2800}-\u{28FF}](?:️|‍|[\u{1F3FB}-\u{1F3FF}])*)+/gu;
  const KEEP_SYM = /[×÷−+=<>%₹°²³√π]/;
  function clean(s) { return String(s || '').replace(/→/g, ' then ').replace(EMO, m => (KEEP_SYM.test(m) ? m : ' ')).replace(/[▶◀✕✔✓☆★⠿›‹•·|]/g, ' ').replace(/\s+([.,!?;:।])/g, '$1').replace(/\s{2,}/g, ' ').trim(); }
  function txt(el) {
    if (!el) return '';
    if (el.nodeType === 1 && el.closest && el.closest('svg') && el.tagName.toLowerCase() !== 'svg') return clean(el.getAttribute('aria-label') || el.textContent);
    let s = '';
    const w = D.createTreeWalker(el, NodeFilter.SHOW_TEXT, { acceptNode: n => { const p = n.parentElement; return p && p.closest('.spk,script,style,[aria-hidden="true"],.sr-skip,.sv-labbar') && !(el.matches && el.matches('[aria-hidden="true"]')) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT; } });
    while (w.nextNode()) { const p = w.currentNode.parentElement; s += (p && /^(B|STRONG|SMALL|SPAN|I|EM)$/.test(p.tagName) ? ' ' : '') + w.currentNode.nodeValue + ' '; }
    return clean(s);
  }
  const sentence = s => { s = clean(s); return s && !/[.!?।:]$/.test(s) ? s + '.' : s; };
  const join = parts => parts.filter(Boolean).map(sentence).join(' ');
  const norm = s => String(s || '').toLowerCase().replace(/[’']/g, '').replace(/[^a-z0-9ऀ-ॿ ]+/g, ' ').replace(/\s+/g, ' ').trim();

  /* ---------------- language: English, or Hindi for Hindi/Sanskrit courses ---------------- */
  function courseLang() {
    const nav = g('NAV') || {};
    if (['hindi', 'sanskrit'].includes(nav.subject)) return 'hi';
    const r = scope(); const t = (r && r.textContent || '').slice(0, 4000);
    const dv = (t.match(/[ऀ-ॿ]/g) || []).length, la = (t.match(/[A-Za-z]/g) || []).length;
    return dv > la ? 'hi' : 'en';
  }
  const STR = {
    en: { opt: 'Option', sayOpt: 'Say the option number, or press it.', sayNum: 'Say a number, or press it.', correct: 'Correct!', wrong: 'Not quite.', answerIs: 'The answer is', step: 'Step', steps: 'Here is how to solve it',
      sayNext: 'Say next, or press Enter.', bigIdeas: 'Big ideas', example: 'There is a worked example. Say "read the steps" to hear it.', lab: 'There is a hands-on lab here. Say "describe the lab" to explore it.',
      nextPlay: 'Say next to start playing.', nextQuiz: 'Say next to start the quiz.', notCaught: "Sorry, I didn't catch that. Say help to hear what you can say.", noChoice: 'There is no choice number', paused: 'Paused. Say resume, or press P.', resumed: 'Going again.',
      noMic: 'Voice input is not available on this browser. You can use the number keys instead.', listening: 'Listening', on: 'Listen mode is on. I will read every screen for you. Hold the big talk button, or press M, and say help to hear what you can say.', off: 'Listen mode off',
      question: 'Question', of: 'of', trueW: 'True', falseW: 'False', none: 'There is nothing like that on this screen.', home: 'Going home.', lessonNone: 'Open a lesson first. Say open, then a subject.',
      hintNone: 'No hint here. After you answer, say explain.', stepsNone: 'There are no steps on this screen.', gotIt: 'Got it.', teach: 'Type or say your explanation for Gappu. Say "explain to Gappu" when you are done, or say skip.',
      secLeft: n => `${n} seconds left`, timeUp: 'Time is up!', choose: 'You chose', sure: 'How sure are you? Say sure, think so, or guessing.' },
    hi: { opt: 'विकल्प', sayOpt: 'विकल्प का नंबर बोलो, या दबाओ।', sayNum: 'नंबर बोलो, या दबाओ।', correct: 'सही!', wrong: 'नहीं, यह सही नहीं है।', answerIs: 'सही उत्तर है', step: 'चरण', steps: 'हल ऐसे करें',
      sayNext: 'आगे बोलो, या Enter दबाओ।', bigIdeas: 'मुख्य बातें', example: 'यहाँ एक हल किया हुआ उदाहरण है। सुनने के लिए बोलो: चरण पढ़ो।', lab: 'यहाँ एक प्रयोग है। उसे जानने के लिए बोलो: लैब बताओ।',
      nextPlay: 'खेल शुरू करने के लिए आगे बोलो।', nextQuiz: 'क्विज़ शुरू करने के लिए आगे बोलो।', notCaught: 'माफ़ करना, मैं समझ नहीं पाई। मदद बोलो।', noChoice: 'यह नंबर नहीं है', paused: 'रुक गए। फिर शुरू करने के लिए आगे बोलो।', resumed: 'फिर से शुरू।',
      noMic: 'इस ब्राउज़र में आवाज़ से जवाब नहीं दे सकते। नंबर दबाओ।', listening: 'सुन रही हूँ', on: 'सुनने वाला मोड चालू है। मैं हर स्क्रीन पढ़कर सुनाऊँगी। बड़ा बटन दबाकर रखो और मदद बोलो।', off: 'सुनने वाला मोड बंद',
      question: 'प्रश्न', of: 'में से', trueW: 'सही', falseW: 'गलत', none: 'इस स्क्रीन पर ऐसा कुछ नहीं है।', home: 'घर चलते हैं।', lessonNone: 'पहले कोई पाठ खोलो।',
      hintNone: 'यहाँ संकेत नहीं है। जवाब के बाद समझाओ बोलो।', stepsNone: 'इस स्क्रीन पर चरण नहीं हैं।', gotIt: 'ठीक है।', teach: 'गप्पू को अपने शब्दों में समझाओ। फिर बोलो: गप्पू को समझाओ।',
      secLeft: n => `${n} सेकंड बचे`, timeUp: 'समय खत्म!', choose: 'तुमने चुना', sure: 'तुम्हें कितना यकीन है? बोलो: पक्का, शायद, या अंदाज़ा।' } };
  const T = k => { const L = STR[courseLang()] || STR.en; return k in L ? L[k] : STR.en[k]; };

  /* ---------------- speech output (per-sentence language, promise when finished) ---------------- */
  const synth = () => ('speechSynthesis' in window ? window.speechSynthesis : null);
  let protectUntil = 0, sayId = 0;
  function say(text, o = {}) {
    const s = synth(); text = String(text || '').trim();
    if (!s || !text) return Promise.resolve();
    const queue = o.queue || (!o.force && now() < protectUntil && s.speaking);
    if (!queue) { try { window.ReadAlong && ReadAlong.active && ReadAlong.stop(); } catch (e) {} try { s.cancel(); } catch (e) {} }
    const my = ++sayId;
    /* split into sentences, then re-join neighbours of the same language (Chrome cuts very long utterances, so cap at ~160 chars) */
    const parts = [];
    text.split(/(?<=[.!?।])\s+|(?<=:)\s+(?=\S)|\n+/).map(x => x.trim()).filter(Boolean).forEach(p => {
      const last = parts[parts.length - 1], hi = DEVA.test(p) && !/[A-Za-z]{3}/.test(p.replace(/[\u0900-\u097F]/g, ''));
      if (last && last.hi === hi && last.t.length + p.length < 160) last.t += ' ' + p; else parts.push({ t: p, hi });
    });
    if (o.protect) protectUntil = now() + Math.min(9000, 600 + text.length * 70);
    return new Promise(res => {
      let left = parts.length; if (!left) return res();
      parts.forEach(({ t: p }) => {
        const hi = DEVA.test(p); let v = null, said = p;
        try { v = bestVoice(hi); } catch (e) {}
        try { said = speechText(p, hi); } catch (e) {}
        const u = new SpeechSynthesisUtterance(said);
        u.lang = v ? v.lang : (hi ? 'hi-IN' : 'en-IN'); try { if (v) u.voice = v; } catch (e) {}
        let rate = 0.9; try { rate = VOICE.rate || 0.9; } catch (e) {}
        u.rate = rate * (o.rate || 1); u.pitch = 1.04; u.volume = 1;
        u.onend = u.onerror = () => { if (--left <= 0) { if (my === sayId) protectUntil = 0; res(); } };
        try { s.speak(u); } catch (e) { res(); }
      });
    });
  }
  const speaking = () => { const s = synth(); return !!(s && s.speaking) || !!(window.ReadAlong && ReadAlong.active); };
  function stopSpeech() { protectUntil = 0; try { synth() && synth().cancel(); } catch (e) {} try { ReadAlong.stop(); } catch (e) {} }
  /* the whole app's speak() now picks the language sentence by sentence */
  window.speak = t => { say(t, { force: true }); };

  /* ---------------- live regions ---------------- */
  function region(id, assertive) {
    let l = D.getElementById(id);
    if (!l) { D.body.insertAdjacentHTML('beforeend', `<div id="${id}" class="sr-only" role="${assertive ? 'alert' : 'status'}" aria-live="${assertive ? 'assertive' : 'polite'}"></div>`); l = D.getElementById(id); }
    return l;
  }
  let annT = 0;
  function announce(msg, assertive, id) {
    msg = clean(msg); if (!msg) return; const l = region(id || (assertive ? 'srAlert' : 'srLive'), assertive);
    clearTimeout(annT); l.textContent = ''; annT = setTimeout(() => { l.textContent = msg; }, 40);
  }

  /* ---------------- haptics ---------------- */
  const PAT = { ok: [30, 60, 30], bad: [220], nav: [12], win: [40, 50, 40, 50, 90], tap: [8] };
  function buzz(k) { if (U().haptics === false || !navigator.vibrate) return; try { navigator.vibrate(PAT[k] || PAT.tap); } catch (e) {} }

  /* ---------------- timers: normal / extra / off, and holding the clock while talking ---------------- */
  let paused = false;
  const timerMode = () => (window.UX && UX.timerMode ? UX.timerMode() : 'normal');
  const timeScale = () => ({ off: 0, extra: 2 }[timerMode()] ?? 1);
  const holdClock = () => paused || D.hidden || (listenOn() && speaking()) || !!openSheet();
  const warned = new WeakMap();
  function timerTick(host, secsLeft) {
    const w = warned.get(host) || new Set(); warned.set(host, w);
    [30, 10, 5].forEach(n => { if (secsLeft <= n && secsLeft > n - 2 && !w.has(n)) { w.add(n); announce(T('secLeft')(n)); if (listenOn()) say(T('secLeft')(n), { queue: true }); } });
  }
  function togglePause(force) {
    paused = force == null ? !paused : force;
    const m = paused ? T('paused') : T('resumed'); announce(m); toastQuiet(m); if (listenOn()) say(m, { force: true });
  }
  const toastQuiet = m => { const t = $1('#toast'); if (!t) return; t.textContent = m; t.classList.add('show'); clearTimeout(toastQuiet.t); toastQuiet.t = setTimeout(() => t.classList.remove('show'), 1900); };

  /* ================= 1. Screen-reader semantics ================= */
  const AVN = { '🦁': 'Lion', '🐯': 'Tiger', '🦊': 'Fox', '🐼': 'Panda', '🐨': 'Koala', '🐸': 'Frog', '🦄': 'Unicorn', '🐙': 'Octopus', '🦉': 'Owl', '🐬': 'Dolphin', '🚀': 'Rocket', '⭐': 'Star' };
  const DECOR = '.ob-hero,.cemoji,.gbig,.face,.confetti,.arc-ce,.arc-res-e,.arc-hdr-e,.arc-dice,.arc-bossface,.arc-hero,.arc-shot,.arc-float,.arc-grip,.arc-cl,.arc-lines,.arc-ground,.eq,.sheet-grab,.oarrow,.chgo,.arc-hp,.arc-tbar,.arc-lbar,.mission .ck,.goalring,.gplant i,.rv-n';
  const EMOJI_IN = 'h1,h2,h3,[role=heading],.tag,.gtype,.verdict,.back,.btn,.choice b,.ch-btns button,.tst-conf button,.arc-card b,.arc-bar b,.arc-life,.viewtgl button,.chfilter button,.rv-filter button,.gdone,.arc-exp b,.dna,.q3bar span,.hello,.ask-sec>b,.rv-sec>b,.exans,.arc-rl,.reallife,.arc-res-score,.arc-xp,.tst-row b,.anrow b,.stepname,.ask-head b,.arc-for,.arc-sltitle';
  function hideEmoji(el) {
    if (el.closest('svg,.opt,.arc-lb,.mbtn,.ochip,.arc-tile,.ra-reading')) return;
    const w = D.createTreeWalker(el, NodeFilter.SHOW_TEXT, { acceptNode: n => (n.parentElement.closest('.sv-emo,.spk,[aria-hidden="true"],svg') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT) });
    const nodes = []; while (w.nextNode()) { EMO.lastIndex = 0; if (EMO.test(w.currentNode.nodeValue)) nodes.push(w.currentNode); }
    if (!nodes.length) return;
    const hasWords = /[\p{L}\p{N}]/u.test(el.textContent.replace(EMO, '')) || el.hasAttribute('aria-label');
    if (!hasWords) return;
    nodes.forEach(n => {
      const frag = D.createDocumentFragment(); let last = 0; const v = n.nodeValue; EMO.lastIndex = 0; let m;
      while ((m = EMO.exec(v))) { if (KEEP_SYM.test(m[0])) continue; if (m.index > last) frag.appendChild(D.createTextNode(v.slice(last, m.index))); const sp = D.createElement('span'); sp.className = 'sv-emo'; sp.setAttribute('aria-hidden', 'true'); sp.textContent = m[0]; frag.appendChild(sp); last = m.index + m[0].length; }
      if (last === 0) return; if (last < v.length) frag.appendChild(D.createTextNode(v.slice(last)));
      n.parentNode.replaceChild(frag, n);
    });
  }
  const setA = (el, k, v) => { if (el.getAttribute(k) !== String(v)) el.setAttribute(k, v); };
  function label(el, name) { if (name && !el.hasAttribute('aria-label')) el.setAttribute('aria-label', name); }
  const starsOf = el => (el.textContent.match(/⭐/g) || []).length;
  function fix(root) {
    if (!root || root.nodeType !== 1) return;
    const q = s => (root.matches && root.matches(s) ? [root] : []).concat($$(s, root));
    q(DECOR).forEach(e => setA(e, 'aria-hidden', 'true'));
    q('img:not([alt])').forEach(e => e.setAttribute('alt', ''));
    q('#tClose').forEach(e => setA(e, 'aria-label', 'Close lesson and go back to the chapter'));
    q('.tbar .pills').forEach(e => { const n = e.children.length, at = [...e.children].findIndex(i => i.classList.contains('on')); setA(e, 'role', 'img'); setA(e, 'aria-label', at >= 0 ? `Step ${at + 1} of ${n}` : `All ${n} steps done`); });
    q('.spk:not([aria-label])').forEach(e => e.setAttribute('aria-label', 'Read aloud'));
    q('.ask-lang').forEach(e => setA(e, 'aria-label', 'Voice language: ' + (e.textContent.trim() === 'EN' ? 'English. Tap for Hindi' : 'Hindi. Tap for English')));
    q('.choice.av').forEach(e => { setA(e, 'aria-label', AVN[e.dataset.a] || 'Hero'); setA(e, 'aria-pressed', e.classList.contains('sel')); });
    q('.choice.subj').forEach(e => setA(e, 'aria-pressed', e.classList.contains('sel')));
    q('#obName,#dName').forEach(e => label(e, 'Your first name'));
    q('#ans').forEach(e => label(e, 'Your explanation for Gappu'));
    q('#askIn').forEach(e => label(e, 'Your doubt'));
    q('#musicTgl').forEach(e => { setA(e, 'role', 'switch'); setA(e, 'aria-label', 'Music'); setA(e, 'aria-checked', e.classList.contains('on')); });
    [['#musVol', 'Music volume'], ['#sfxVol', 'Effects volume'], ['#vRate', 'Reading speed'], ['#vEn', 'English reading voice'], ['#vHi', 'Hindi reading voice']].forEach(([s, n]) => q(s).forEach(e => label(e, n)));
    q('#gradeChips button').forEach(e => setA(e, 'aria-pressed', e.classList.contains('on')));
    q('.ux-sizes button').forEach(e => { if (!e.hasAttribute('tabindex')) e.tabIndex = e.classList.contains('on') ? 0 : -1; });
    q('.tst-pal button').forEach(e => setA(e, 'aria-label', `Question ${e.textContent.trim()}${e.classList.contains('cur') ? ', current' : ''}${e.classList.contains('done') ? ', answered' : ', not answered'}${e.classList.contains('mark') ? ', marked for review' : ''}`));
    q('#tTime').forEach(e => { setA(e, 'role', 'timer'); setA(e, 'aria-live', 'off'); });
    q('.tcard').forEach(e => { const b = txt($1('.tbody b', e)), h = txt($1('.tbody span', e)), s = starsOf($1('.tstars', e) || e); setA(e, 'aria-label', `Quest ${txt($1('.tnum', e)) || ''}: ${b}${e.classList.contains('done') ? `, done, ${s} of 3 stars` : ''}. ${h}`.replace('Quest : ', 'Quest: ')); });
    q('.bigstars').forEach(e => { setA(e, 'role', 'img'); setA(e, 'aria-label', `${$$('.on', e).length} of 3 stars`); });
    q('.tstars').forEach(e => setA(e, 'aria-hidden', 'true'));
    q('.progress').forEach(e => { const i = $1('i', e); const v = i ? Math.round(parseFloat(i.style.width) || 0) : 0; setA(e, 'role', 'progressbar'); setA(e, 'aria-label', 'Progress'); setA(e, 'aria-valuemin', 0); setA(e, 'aria-valuemax', 100); setA(e, 'aria-valuenow', v); });
    q('.hud-bar').forEach(e => { const v = Math.round(parseFloat(($1('i', e) || {}).style?.width) || 0); setA(e, 'role', 'progressbar'); setA(e, 'aria-label', 'Grade journey'); setA(e, 'aria-valuemin', 0); setA(e, 'aria-valuemax', 100); setA(e, 'aria-valuenow', v); });
    q('.arc-bar b').forEach(e => { setA(e, 'role', 'heading'); setA(e, 'aria-level', '2'); });
    q('.arc-hearts').forEach(e => { setA(e, 'role', 'img'); setA(e, 'aria-label', `${(e.textContent.match(/❤/g) || []).length} hearts left`); });
    q('.arc-slog,.arc-sfb,.arc-mlog,#sfb').forEach(e => { setA(e, 'aria-live', 'polite'); });
    q('.arc-board').forEach(e => setA(e, 'aria-hidden', 'true'));
    q('.arc-ladder').forEach(e => { setA(e, 'role', 'img'); setA(e, 'aria-label', `Coin ladder: ${$$('.won', e).length} of ${e.children.length} steps climbed`); });
    q('.arc-mc').forEach(memLabel);
    q('.mbtn').forEach(e => { setA(e, 'aria-label', `${e.dataset.s === 'L' ? 'Left' : 'Right'}: ${e.textContent.trim()}${e.classList.contains('ok') ? ', matched' : ''}`); setA(e, 'aria-pressed', e.classList.contains('sel')); });
    q('.viewtgl').forEach(e => setA(e, 'aria-label', 'Chapter view'));
    q('.lab-loading').forEach(e => setA(e, 'role', 'status'));
    q('.lab-win').forEach(e => { setA(e, 'role', 'status'); });
    q('.gsearch>span').forEach(e => setA(e, 'aria-hidden', 'true'));
    q('.map').forEach(e => { if (!e.hasAttribute('aria-label')) { setA(e, 'role', 'region'); setA(e, 'aria-label', e.id === 'cmap' ? 'Chapter map' : 'Subject map'); } });
    q('.vis svg, .explain svg').forEach(e => { if (e.hasAttribute('role')) return; const t = $$('text', e).map(x => x.textContent.trim()).filter(Boolean); setA(e, 'role', 'img'); setA(e, 'aria-label', 'Picture' + (t.length ? ': ' + [...new Set(t)].slice(0, 6).join(', ') : ' explaining the answer')); });
    q('svg').forEach(e => { if (e.hasAttribute('role') || e.hasAttribute('aria-hidden') || e.closest('.lab-box,.map,[role=img]')) return; if (e.closest('button,[role=button]')) { setA(e, 'aria-hidden', 'true'); return; } const t = $$('text', e).map(x => x.textContent.trim()).filter(Boolean); if (t.length) { setA(e, 'role', 'img'); setA(e, 'aria-label', [...new Set(t)].slice(0, 6).join(', ')); } else setA(e, 'aria-hidden', 'true'); });
    q('canvas').forEach(e => { if (!e.hasAttribute('role')) { setA(e, 'role', 'img'); setA(e, 'aria-label', (e.closest('.lab-box') && e.closest('.lab-box').getAttribute('aria-label')) || 'Moving picture. Use Describe to hear what it shows.'); } });
    q('.arc-mvup,.arc-mvdn').forEach(e => { const r = e.closest('.arc-row'); if (r) setA(e, 'aria-label', `Move "${txt($1('.arc-rt', r))}" ${e.classList.contains('arc-mvup') ? 'up' : 'down'}`); });
    q(EMOJI_IN).forEach(hideEmoji);
  }
  function memLabel(b) {
    const i = +b.dataset.i + 1, side = b.classList.contains('arc-side-L') ? 'purple' : 'green', t = txt($1('.arc-mb', b));
    const st = b.classList.contains('done') ? `matched: ${t}` : b.classList.contains('flip') ? `${side}: ${t}` : `${side}, face down`;
    setA(b, 'aria-label', `Card ${i}, ${st}`);
  }

  /* ---------- maps: every island/chapter becomes a real button ---------- */
  function wrapWorlds() {
    if (!window.Worlds || Worlds._a11y) return; Worlds._a11y = true;
    const _render = Worlds.render;
    Worlds.render = function (el, grade, nodes, kind, onTap) {
      const r = _render.apply(this, arguments);
      try {
        const svg = $1('svg', el); if (!svg) return r;
        svg.setAttribute('role', 'group'); svg.setAttribute('aria-label', kind === 'grade' ? `Grade ${grade} subjects` : 'Chapters');
        [...svg.children].forEach(ch => { if (!ch.classList.contains('node')) ch.setAttribute('aria-hidden', 'true'); });
        $$('.node', el).forEach(gn => {
          const n = nodes[+gn.dataset.i] || {}, soon = n.state === 'soon';
          const lab = kind === 'grade'
            ? `${n.title}${n.sub ? ', ' + n.sub : ''}${soon ? ', coming soon' : `, ${Math.round(n.pct || 0)}% done`}${n.state === 'current' ? ', next up' : ''}`
            : `Chapter ${n.num}: ${n.title}, ${n.sub || ''}${n.state === 'done' ? ', done' : ''}${n.stars ? `, ${n.stars} of 3 stars` : ''}${n.state === 'current' ? ', next up' : ''}`;
          gn.setAttribute('role', 'button'); gn.setAttribute('tabindex', '0'); gn.setAttribute('aria-label', lab); gn.dataset.svLabel = lab;
          if (soon) gn.setAttribute('aria-disabled', 'true');
          gn.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.stopPropagation(); onTap(+gn.dataset.i); } });
        });
      } catch (e) {}
      return r;
    };
  }

  /* ---------- dialogs and sheets ---------- */
  const DLG = new Map();       // sheet -> opener
  function sheetHeading(s) { return $1('h2,h3,.ask-head b', s); }
  function dialogOpened(s) {
    if (DLG.has(s)) return;
    DLG.set(s, D.activeElement && D.activeElement !== D.body ? D.activeElement : null);
    s.setAttribute('role', s.id === 'svOffer' ? 'alertdialog' : 'dialog'); s.setAttribute('aria-modal', 'true');
    const h = sheetHeading(s); if (h) { if (!h.id) h.id = (s.id || 'sv') + 'Title'; s.setAttribute('aria-labelledby', h.id); }
    if (s.dataset.svInert) { s.removeAttribute('inert'); delete s.dataset.svInert; }   // a sheet opened on top of another sheet was made inert when the first one opened
    $$('body > *').forEach(e => { if (e !== s && !e.matches('#srLive,#srAlert,#svTalk,script') && !e.classList.contains('show')) { if (!e.hasAttribute('inert')) { e.setAttribute('inert', ''); e.dataset.svInert = '1'; } } });
    setTimeout(() => { if (!s.classList.contains('show')) return; if (s.contains(D.activeElement)) return; const t = h || $1(FOCUSABLE, s); focusEl(t); }, 60);
    buzz('nav');
    if (listenOn()) setTimeout(() => readScreen(true), 350);
  }
  function dialogClosed(s) {
    if (!DLG.has(s)) return; const op = DLG.get(s); DLG.delete(s);
    if (!openSheet()) $$('[data-sv-inert]').forEach(e => { e.removeAttribute('inert'); delete e.dataset.svInert; });
    setTimeout(() => { if (openSheet()) return; if (op && op.isConnected && visible(op)) focusEl(op); else focusBest(true); }, 30);
    if (listenOn()) { lastKey = ''; setTimeout(() => readScreen(), 400); }
  }
  const sheetObs = new MutationObserver(recs => recs.forEach(r => { const s = r.target; if (!s.matches || !s.matches(SHEETS)) return; s.classList.contains('show') ? dialogOpened(s) : dialogClosed(s); }));
  function watchSheets() { $$(SHEETS).forEach(s => { if (s._svw) return; s._svw = 1; sheetObs.observe(s, { attributes: true, attributeFilter: ['class'] }); if (s.classList.contains('show')) dialogOpened(s); }); }
  function closeTop() {
    const s = openSheet(); if (!s) return false;
    if (s.hasAttribute('data-pinned') || s.hasAttribute('data-noclose')) return false;       // Parent Home (parent accounts) and must-answer sheets (new password) cannot be closed
    if (window.SheetSwipe) { SheetSwipe.close(s); return true; }   // the sheet's own close / done / cancel button (js/sheets.js)
    const btn = $$('button', s).find(b => b.matches('.ask-x,#rvX,#uxDone,[data-close]') || /^(close|done|got it|no thanks)$/i.test(b.textContent.trim()));
    if (btn) btn.click(); else s.classList.remove('show');
    return true;
  }

  /* ---------- focus ---------- */
  let selfFocus = false;
  function focusEl(el) {
    if (!el || !el.isConnected) return;
    if (!el.matches(FOCUSABLE) && !el.hasAttribute('tabindex')) el.setAttribute('tabindex', '-1');
    selfFocus = true; try { el.focus({ preventScroll: true }); } catch (e) {} selfFocus = false;
  }
  const NEXT_SEL = '#nx,#rvBack,.tfn,.gnext,.arc-next,#trAgain';
  const Q_SEL = '.qtext,#fs,#spq,#tfc,#scard,.arc-qt,.arc-lq,.arc-oddc h3,.arc-chain h3,.arc-sintro';
  const HEAD_SEL = '#worldTitle,#subTitle,.chead h2,.ob h1,.arc-res h2,.arc-bar b,.arc-hdr h2,#gbox h3,.done-card h2,h1,h2,[role=heading],h3';
  function focusBest(screenLevel) {
    const r = scope(); if (!r) return;
    const pick = sel => $$(sel, r).find(visible);
    let t = null;
    if (!screenLevel) { const fb = $$('.explain,.arc-exp,.tfwhy,.gdone', r).some(visible); if (fb) t = pick(NEXT_SEL); }
    t = t || pick(Q_SEL) || pick(HEAD_SEL) || pick(FOCUSABLE);
    if (t) focusEl(t);
  }
  const lostFocus = () => { const a = D.activeElement; return !a || a === D.body || !a.isConnected || a.disabled || !visible(a); };

  /* ================= 2. Listen mode: what is on the screen, as speech ================= */
  const CHOICE_SETS = ['.arc-mgrid .arc-mc', '.opt:not([disabled]):not(.arc-gone)', '.tfbtns .tfb', '.arc-lbtns .arc-lb', '.sbuckets .sbk', '.arc-bks .arc-bk', '.arc-tiles:not(.lock) .arc-tile', '.opool .ochip:not(:disabled)', '.mgrid .mbtn:not(.ok)',
    '.arc-grid .arc-card', '.tcard', '#chList .chrow', '.map .node:not(.soon)', '.gs-res .gs-hit', '.ob .choice:not(.off)', '#s-me .grid5 .choice', '.ask-log .ask-msg:last-child .ask-alt', '#tConf.show button'];
  function getChoices(r = scope()) {
    for (const s of CHOICE_SETS) { const l = $$(s, r).filter(visible); if (l.length) return l; }
    return [];
  }
  const NOBADGE = '.tcard,.arc-opt,.node,.tst-pal button';
  function numberChoices(ch) {
    $$('[data-svn]').forEach(e => { if (!ch.includes(e)) e.removeAttribute('data-svn'); });
    if (!listenOn()) return;
    ch.forEach((e, i) => { if (!e.matches(NOBADGE)) setA(e, 'data-svn', String(i + 1)); });
  }
  const labelOf = el => clean(el.dataset.svLabel || (el.matches('.arc-mc,.mbtn,.tcard') ? el.getAttribute('aria-label') : '') || txt(el) || el.getAttribute('aria-label') || '');
  const listChoices = (ch, word) => ch.map((e, i) => `${word ? word + ' ' : ''}${i + 1}: ${sentence(labelOf(e))}`).join(' ');

  function questionSpeech(r, ch) {
    const tag = txt($1('.tag', $1('.qtext', r).closest('.card') || r));
    const q = txt($1('.qtext', r));
    let s = join([tag, q]) + ' ' + listChoices(ch, T('opt')) + ' ' + T('sayOpt');
    const sel = $1('#tOpts .opt.sel', r);
    if (sel && $1('#tConf.show', r)) s = `${T('choose')} ${T('opt').toLowerCase()} ${ch.indexOf(sel) + 1}: ${sentence(txt(sel))} ${T('sure')}`;
    return s;
  }
  function feedbackSpeech(ex) {
    const verdict = txt($1('.verdict', ex)), why = txt($1('.why', ex));
    const steps = $$('.exstep', ex).map(s => txt(s).replace(/^\d+\.\s*/, ''));
    return join([verdict, why]) + (steps.length ? ` ${T('steps')}: ` + steps.map((s, i) => `${T('step')} ${i + 1}: ${sentence(s)}`).join(' ') : '');
  }
  function learnSpeech(r) {
    const card = $1('.card', r), title = txt($1('h2', card)), hook = txt($1('.bubble', r));
    const pts = $$('.point', r).map(p => txt($1('div', p) || p));
    const lab = $1('.labcard', r), labOk = lab && lab.style.display !== 'none' && $1('.lab-box', lab);
    const go = $1('#learnGo', r);
    return join([title, hook]) + (pts.length ? ` ${T('bigIdeas')}: ` + pts.map((p, i) => `${i + 1}. ${sentence(p)}`).join(' ') : '') + ' ' + ($1('#exBtn', r) ? T('example') + ' ' : '') + (labOk ? T('lab') + ' ' : '') + (go && /play/i.test(go.textContent) ? T('nextPlay') : T('nextQuiz'));
  }
  function gameSpeech(gb, ch) {
    const title = txt($1('h3', gb)), kind = txt($1('.gtype', gb));
    const done = $1('.gdone', gb); if (done) return join([txt(done)]) + ' ' + T('sayNext');
    if ($1('.mgrid', gb)) {
      const L = ch.filter(e => e.dataset.s === 'L'), sel = $1('.mbtn.sel', gb);
      const lines = ch.map((e, i) => `${i + 1}: ${sentence(e.textContent.trim())}`);
      return (sel ? `You picked ${sentence(sel.textContent.trim())} Now pick its partner from the right side. ` : join([kind, title]) + ` Left side: ${lines.slice(0, L.length).join(' ')} Right side: ${lines.slice(L.length).join(' ')} Pick one from the left, then its partner on the right. `) + T('sayNum');
    }
    if ($1('#scard', gb)) { const fb = txt($1('#sfb', gb)); return join([/goes in/.test(fb) ? fb : '', kind + ': ' + title, (fb.match(/^\d+ of \d+/) || [''])[0], txt($1('#scard', gb))]) + ' ' + listChoices(ch) + ' ' + T('sayNum'); }
    if ($1('.opool', gb)) { const done2 = $$('.ostep', gb).map(txt); return join([kind + ': ' + title, txt($1('.sub', gb)), done2.length ? 'So far: ' + done2.join(', ') : '']) + ' ' + (ch.length ? 'What comes next? ' + listChoices(ch) + ' ' + T('sayNum') : ''); }
    if ($1('#tfc', gb)) { const c = $1('#tfc', gb); if (c.classList.contains('good') || c.classList.contains('bad')) return join([c.classList.contains('good') ? T('correct') : T('wrong'), txt($1('#tfw', gb))]) + ' ' + T('sayNext'); return join([kind, txt(c)]) + ` 1: ${T('trueW')}. 2: ${T('falseW')}. ` + T('sayNum'); }
    if ($1('#fs', gb)) { const s = txt($1('#fs', gb)).replace(/\?/g, ' blank '); const b = $1('#fs .blank', gb); if (b && (b.classList.contains('ok') || b.classList.contains('no'))) return join([b.classList.contains('ok') ? T('correct') : T('wrong') + ' ' + T('answerIs') + ' ' + b.textContent, s]); return join([kind, s]) + ' ' + listChoices(ch, T('opt')) + ' ' + T('sayOpt'); }
    if ($1('#spq', gb)) return join([txt($1('#spq', gb))]) + ' ' + listChoices(ch, T('opt'));
    return join([kind, title]);
  }
  function arcadeSpeech(r, ch) {
    const res = $1('.arc-res', r);
    if (res) return join([txt($1('h2', res)), txt($1('.arc-res-score', res)), ...$$('.arc-rl', res).map(txt)]) + ' Say "play again", or "back" for the arcade.';
    const menu = $1('.arc-menu', r);
    if (menu) return join(['Arcade', txt($1('.arc-hdr .sub', menu))]) + ` ${ch.length} games. ` + ch.map((e, i) => `${i + 1}: ${sentence(txt($1('b', e)))} ${sentence(txt($1('.arc-cd', e)))}`).join(' ') + ' ' + T('sayNum');
    const gm = $1('.arc-game', r); if (!gm) return '';
    const id = gm.dataset.game, name = txt($1('.arc-bar b', gm));
    const exp = $$('.arc-exp', gm).filter(visible).pop(), nx = $1('.arc-next', gm);
    const qs = () => { const qt = $1('.arc-qt', gm); return qt && ch.length && ch[0].matches('.opt') ? join([txt(qt)]) + ' ' + listChoices(ch, T('opt')) + ' ' + T('sayOpt') : ''; };
    if (exp && nx) return join([txt(exp)]) + ' ' + T('sayNext');
    if (id === 'boss') return join([`Boss ${txt($1('.arc-hpt', gm))}`, `${(txt($1('.arc-hearts', gm)) || '')}`, $1('.arc-hearts', gm) ? $1('.arc-hearts', gm).getAttribute('aria-label') : '']) + ' ' + qs();
    if (id === 'quizshow') { const lifes = $$('.arc-life:not([disabled])', gm).map(txt); return join([txt($1('.arc-for', gm)), txt($1('.arc-gappu', gm))]) + ' ' + qs() + (lifes.length ? ` Lifelines: say ${lifes.join(', or ')}.` : ''); }
    if (id === 'lightning') { const c = $1('.arc-count', gm); if (c && visible(c)) return `${name}. Get ready! Answer as many as you can.` + (timeScale() ? ' The clock waits while I talk.' : ' No timer.'); const lq = $1('.arc-lq', gm); if (!lq) return ''; return join([txt($1('.arc-lwhy', gm)), txt(lq)]) + ' ' + listChoices(ch) + ' ' + T('sayNum'); }
    if (id === 'memory') { const last = txt($1('.arc-mline', gm)); return join([last, `${name}. ${$$('.arc-mc', gm).length} cards, face down. Purple cards are questions, green cards are answers. Say a card number to flip it, and I will read it. Find the pairs that go together.`]); }
    if (id === 'storm') { const it = $1('.arc-sintro', gm); if (it && visible(it)) return join([txt($1('.arc-round', gm)), txt(it)]); const fb = txt($1('.arc-sfb', gm)); const d = $1('.arc-drop', gm); return join([fb, d && visible(d) ? 'Catch: ' + txt(d) : '']) + ' Baskets: ' + listChoices(ch) + ' ' + T('sayNum'); }
    if (id === 'odd') return join([txt($1('.arc-oddc .tag', gm)), txt($1('.arc-oddc h3', gm))]) + ' ' + listChoices(ch) + ' ' + T('sayNum');
    if (id === 'chain') { const rows = $$('.arc-row', gm).map((rw, i) => `${i + 1}: ${sentence(txt($1('.arc-rt', rw)))}`).join(' '); return join([txt($1('.arc-chain .tag', gm)), txt($1('.arc-chain h3', gm)), txt($1('.arc-chain .sub', gm)), txt($1('.arc-exp', gm))]) + ` The steps now: ${rows} Say "swap 1 and 3", or "move 2 up", then say "check".`; }
    if (id === 'snakes') { const qb = $1('.arc-slq', gm); if (qb && visible(qb)) return join([txt($1('.arc-sltitle', qb))]) + ' ' + qs();
      const me = +txt($1('.arc-p0', gm)) || 1, L = window.Arcade && Arcade.LADDERS, Sn = window.Arcade && Arcade.SNAKES;
      const near = L && Sn ? [1, 2, 3, 4, 5, 6].map(d => me + d).filter(n => L[n] || Sn[n]).map(n => L[n] ? `a ladder on ${n}` : `a snake on ${n}`) : [];
      return join([txt($1('.arc-slog', gm)), `You are on square ${me} of 100. Robo is on ${txt($1('.arc-p1', gm))}`, near.length ? 'Coming up: ' + near.join(', ') : '', txt($1('.arc-turn', gm)),
        me > 94 ? `You need exactly ${100 - me} to reach 100. A bigger roll means you stay` : '']) + ($1('.arc-roll:not([disabled])', gm) ? ' Say roll, or press Enter.' : ''); }
    return join([name]) + ' ' + qs();
  }
  function genericSpeech(r, ch) {
    const id = r.id;
    if (id === 's-world') return join([txt($1('#worldTitle', r)), txt($1('#hudName', r)) + ' ' + txt($1('#hudPct', r)), txt($1('#q3bar span', r))]) + ` Your subjects: ${listChoices(ch)} Say "open", then a subject, or press its number. Say help to hear more.`;
    if (id === 's-subject') { const list = ch.slice(0, 15); return join([txt($1('#subTitle', r))]) + ` ${ch.length} chapters. ${listChoices(list)} ${T('sayNum')} You can also say "start test" or "games".`; }
    if (id === 's-chapter' && $1('.tcard', r)) return join([txt($1('.chead', r)), txt($1('.ch-ready', r))]) + ` ${ch.length} quests. ${listChoices(ch)} ${T('sayNum')} You can also say "start test", "revision sheet" or "games".`;
    const h = $$('h1,h2,[role=heading]', r).find(visible), subs = $$('p.sub,.tst-how p,.ready b', r).filter(visible).slice(0, 3).map(txt);
    const btns = $$('.btn,.ch-btns button', r).filter(visible).slice(0, 6).map(txt).filter(Boolean);
    return join([txt(h), ...subs]) + (ch.length ? ' ' + listChoices(ch) + ' ' + T('sayNum') : (btns.length ? ` Buttons: ${btns.join(', ')}.` : ''));
  }
  function sheetSpeech(s) {
    if (s.id === 'svOffer') return join([txt($1('h2', s)), txt($1('p', s))]) + ' Press Enter or say yes. Press Escape or say no.';
    if (s.id === 'askSheet') { const last = $$('.ask-msg.bot', s).pop(); const t = last ? txt(last) : ''; return last && $$('.ask-msg', s).length > 1 ? t : join([txt($1('.ask-head', s)), 'Type your doubt, or hold the talk button and say ask, then your question.']); }
    if (s.id === 'sheet3d') return labState.desc || join([txt($1('h3', s))]);
    return join([txt(sheetHeading(s)), txt($1('p.sub', s))]) + ' Use Tab to move. Press Escape to close.';
  }
  function describe() {
    const s = openSheet(); if (s) return { text: sheetSpeech(s), ch: getChoices(s) };
    const r = activeScreen(); if (!r) return { text: '', ch: [] };
    const ch = getChoices(r);
    let text = '';
    const ex = $$('.explain', r).filter(visible).pop();
    if (ex && $1('.qtext', r)) text = feedbackSpeech(ex) + ' ' + T('sayNext');
    else if ($1('.arc-stage,.arc-menu,.arc-res', r)) text = arcadeSpeech(r, ch);
    else if ($1('.lv-root', r) && window.Live && Live.speech) text = Live.speech(r, ch, listChoices);
    else if ($1('.qtext', r) && ch.length && ch[0].matches('.opt')) text = questionSpeech(r, ch);
    else if ($1('#learnGo', r)) text = learnSpeech(r);
    else if ($1('#tBtn', r) && $1('#ans', r)) text = join([txt($1('.tag', r)), txt($1('#gs', r))]) + ' ' + T('teach');
    else if ($1('#gbox', r)) text = gameSpeech($1('#gbox', r), ch);
    else text = genericSpeech(r, ch);
    return { text: clean(text), ch };
  }
  let lastKey = '', readT = 0;
  function readScreen(force) {
    const d = describe(); numberChoices(d.ch);
    if (!listenOn()) return d;
    if (!d.text || (!force && d.text === lastKey)) return d;
    if (recActive() && !force) return d;
    lastKey = d.text;
    const isFeedback = /^(Correct|Not quite|सही|नहीं)/.test(d.text) || !!$1('.explain .verdict', scope());
    const key = d.text;
    say(d.text, { protect: isFeedback, force: !!force }).then(() => {
      if (lastKey !== key || !U().voiceAns || !d.ch.length || recActive()) return;
      if (d.ch[0].matches('.opt,.tfb,.arc-lb,.sbk,.arc-bk,.arc-tile')) setTimeout(() => { if (lastKey === key && !speaking()) startRec({ auto: true }); }, 400);
    });
    return d;
  }

  /* ================= 3. Voice commands ================= */
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  let rec = null, holding = false, micDenied = false, recUsed = false;
  const recActive = () => !!rec;
  function startRec(o = {}) {
    if (!SR || (o.auto && micDenied)) { if (!o.auto) { say(T('noMic'), { force: true }); announce(T('noMic')); } return; }
    stopRec();
    if (!o.auto) stopSpeech();
    try { rec = new SR(); } catch (e) { rec = null; return; }
    const me = rec;
    rec.lang = courseLang() === 'hi' ? 'hi-IN' : 'en-IN'; rec.interimResults = false; rec.maxAlternatives = 4; rec.continuous = !!o.hold;
    let got = [];
    rec.onresult = e => { for (let i = e.resultIndex; i < e.results.length; i++) if (e.results[i].isFinal) got.push([...e.results[i]].map(a => a.transcript)); if (!o.hold && got.length) { const a = got.flat(); got = []; handleSpeech(a); } };
    rec.onerror = ev => { if (ev.error === 'not-allowed' || ev.error === 'service-not-allowed') { if (!micDenied) toast('Please allow the microphone to talk to StudyVerse'); micDenied = true; } };
    rec.onend = () => { if (rec === me) rec = null; talkState(false); if (o.hold && got.length) { const a = got.map(x => x[0]).join(' '); handleSpeech([a, ...got.flat()]); } };
    try { rec.start(); recUsed = true; talkState(true); if (!o.auto) { try { sfx('tap'); } catch (e) {} announce(T('listening')); } } catch (e) { rec = null; }
  }
  function stopRec() { if (rec) { const r = rec; rec = null; try { r.stop(); } catch (e) {} } talkState(false); }
  function talkState(on) { const b = $1('#svTalk'); if (b) { b.classList.toggle('on', on); b.setAttribute('aria-pressed', String(on)); } }

  const NUMW = { one: 1, won: 1, first: 1, two: 2, to: 2, too: 2, second: 2, three: 3, tree: 3, third: 3, four: 4, for: 4, fourth: 4, five: 5, fifth: 5, six: 6, sixth: 6, seven: 7, eight: 8, ate: 8, nine: 9, ten: 10, eleven: 11, twelve: 12, thirteen: 13, fourteen: 14, fifteen: 15, sixteen: 16,
    'एक': 1, 'दो': 2, 'तीन': 3, 'चार': 4, 'पांच': 5, 'पाँच': 5, 'छह': 6, 'छः': 6, 'सात': 7, 'आठ': 8, 'नौ': 9, 'दस': 10, 'ग्यारह': 11, 'बारह': 12 };
  const LETW = { a: 1, ay: 1, b: 2, be: 2, bee: 2, c: 3, see: 3, sea: 3, d: 4, dee: 4 };
  function numberIn(said) {
    const m = said.match(/^(?:option|number|answer|card|choice|basket|quest|chapter|विकल्प|नंबर|कार्ड)?\s*(\d{1,2})$/) || said.match(/^(\d{1,2})(?:st|nd|rd|th)?(?: one| option)?$/);
    if (m) return +m[1];
    const w = said.replace(/^(option|number|answer|card|choice|basket|the|विकल्प|नंबर|कार्ड)\s+/, '').replace(/\s+(one|option)$/, '').trim();
    if (NUMW[w]) return NUMW[w];
    const l = said.match(/^(?:option|answer)?\s*([a-z]{1,3})$/); if (l && LETW[l[1]] && (said.length <= 3 || /^(option|answer)/.test(said))) return LETW[l[1]];
    return null;
  }
  function activate(el) {
    if (!el) return false;
    if (el.click && el instanceof HTMLElement) el.click(); else el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    return true;
  }
  function pick(n) {
    const ch = getChoices(); const el = ch[n - 1];
    if (!el) { say(`${T('noChoice')} ${n}.`, { force: true }); return false; }
    if (el.matches('[aria-disabled=true]')) { say(labelOf(el), { force: true }); return true; }
    buzz('tap'); activate(el); return true;
  }
  const vis1 = (sel, r = scope()) => $$(sel, r).find(visible);
  const clickFirst = sel => { const b = vis1(sel); return b ? activate(b) : false; };
  function primary() {
    return clickFirst('#nx, #rvBack, #tNext, .gnext, .tfn, .arc-next, #learnGo, #dNext, #tGo, #pStart, #dGo, #obGo, #sjGo, .arc-roll:not([disabled]), #gBack, #exBtn, #svOfferYes');
  }
  function back() {
    if (closeTop()) return true;
    return clickFirst('.arc-quit, .arc-back, #arcBack, .back, #chBack, #rsBack, #tBack, #trBack, #bmBack, #obBack, #sjBack, #stBack, #dBack, #tClose');
  }
  function goHome() { if (closeTop()) {} say(T('home'), { force: true }); try { (g('ST') || {}).profile ? worldScreen() : null; } catch (e) {} return true; }
  function readLesson() {
    const run = g('RUN'); const t = run && run.t;
    if (!t) { const card = vis1('.rvcard,.ask-card'); if (card) { say(txt(card), { force: true }); return true; } say(T('lessonNone'), { force: true }); return true; }
    const L = t.learn || {};
    say(join([t.title, L.hook]) + ((L.points || []).length ? ` ${T('bigIdeas')}: ` + L.points.map((p, i) => `${i + 1}. ${sentence(p)}`).join(' ') : '') + (L.example ? ' ' + join(['Example: ' + L.example.q, ...(L.example.steps || []).map((s, i) => `${T('step')} ${i + 1}: ${s}`), T('answerIs') + ' ' + L.example.answer]) : '') + (L.reallife ? ' ' + sentence('In real life: ' + L.reallife) : ''), { force: true });
    return true;
  }
  function readSteps() {
    const r = scope();
    const ex = $$('.explain', r).filter(visible).pop(); if (ex && $1('.exstep', ex)) { say(feedbackSpeech(ex), { force: true }); return true; }
    const run = g('RUN'), E = run && run.t && run.t.learn && run.t.learn.example;
    if (E) { const b = $1('#exBtn', r); let k = 0; while (b && b.isConnected && k++ < 20) b.click(); say(join(['Example: ' + E.q, ...(E.steps || []).map((s, i) => `${T('step')} ${i + 1}: ${s}`), T('answerIs') + ' ' + E.answer]), { force: true }); return true; }
    if ($1('.arc-chain', r)) { lastKey = ''; readScreen(true); return true; }
    say(T('stepsNone'), { force: true }); return true;
  }
  function explain() {
    const r = scope();
    const w = $$('.explain .why, .arc-exp p, .arc-lwhy, #tfw, .tfwhy', r).filter(visible).pop();
    if (w) { say(txt(w), { force: true }); return true; }
    return hint();
  }
  function hint() {
    const run = g('RUN'), t = run && run.t; const qt = txt(vis1('.qtext, .arc-qt, #fs, #spq'));
    if (!t || !t.learn) { const life = vis1('.arc-life[data-l=gappu]:not([disabled])'); if (life) return activate(life); say(T('hintNone'), { force: true }); return true; }
    const words = new Set(norm(qt).split(' ').filter(w => w.length > 3));
    const pts = (t.learn.points || []).map(p => [p, norm(p).split(' ').filter(w => words.has(w)).length]).sort((a, b) => b[1] - a[1]);
    const tip = (pts[0] && pts[0][1] ? pts[0][0] : (t.revise && t.revise.summary) || t.learn.hook || (t.learn.points || [])[0]);
    say('Hint: ' + tip, { force: true }); return true;
  }
  function startTest() {
    if (clickFirst('#tGo')) return true;
    if (clickFirst('#chTest, #rsTest, #sbMock')) { setTimeout(() => { if (listenOn()) { lastKey = ''; readScreen(true); } }, 900); return true; }
    const nav = g('NAV') || {};
    if (nav.subject && window.Tests) { Tests.run(nav.chapter != null ? 'chapter' : 'mock', nav.subject, nav.chapter); return true; }
    say('Open a subject or a chapter first, then say start test.', { force: true }); return true;
  }
  const SUBJ_ALIAS = { maths: 'maths math mathematics गणित मैथ्स', english: 'english अंग्रेज़ी अंग्रेजी इंग्लिश', hindi: 'hindi हिंदी हिन्दी', sanskrit: 'sanskrit संस्कृत', evs: 'evs environment environmental पर्यावरण', science: 'science विज्ञान साइंस', social: 'social sst सामाजिक', history: 'history इतिहास', geography: 'geography भूगोल', civics: 'civics political राजनीति', economics: 'economics अर्थशास्त्र', physics: 'physics भौतिकी', chemistry: 'chemistry रसायन', biology: 'biology जीव', accountancy: 'accountancy accounts लेखाशास्त्र', business: 'business व्यवसाय', polsci: 'political polsci', psychology: 'psychology मनोविज्ञान', sociology: 'sociology समाजशास्त्र', cs: 'computer cs कंप्यूटर' };
  function openThing(what) {
    what = norm(what).replace(/^(the|my)\s+/, '');
    let m = what.match(/^(chapter|अध्याय)\s+(\S+)/); if (m) { const n = numberIn(m[2]) || numberIn('number ' + m[2]); const nav = g('NAV') || {}; if (n && nav.subject) { chapterScreen(nav.subject, n - 1); return true; } }
    m = what.match(/^(quest|topic|lesson|पाठ)\s+(\S+)/); if (m) { const n = numberIn(m[2]); const c = $$('.tcard').filter(visible)[n - 1]; if (c) return activate(c); }
    if (/^(games?|arcade|खेल)/.test(what)) return clickFirst('#chArc, #sbArc, #pArc') || (window.Tests && (Tests.arcade({ grade: (g('ST') || {}).profile.grade }), true));
    if (/^(practice|practise|अभ्यास)/.test(what)) { practiceScreen(); return true; }
    if (/^(settings|setting|सेटिंग)/.test(what)) { UX.settings(); return true; }
    if (/^(lab|the lab|try it|experiment|लैब|प्रयोग)/.test(what)) { if (g('RUN')) { open3D(); return true; } }
    if (/^(revision|revision sheet)/.test(what)) return clickFirst('#chSheet');
    if (/^(ask|doubt)/.test(what)) { Ask.open(); return true; }
    const ST_ = g('ST'); if (!ST_ || !ST_.profile) return false;
    let subs = []; try { subs = curSubjects(ST_.profile.grade); } catch (e) {}
    const hit = subs.find(s => { const al = (SUBJ_ALIAS[s.id] || s.id) + ' ' + norm(s.name); const short = what.split(' ').length <= 3; return al.split(' ').some(a => a && (what === a || (short && (what.startsWith(a + ' ') || what.endsWith(' ' + a) || (a.length > 3 && what.includes(a)))))); });
    if (hit) { closeTop(); subjectScreen(hit.id); return true; }
    return false;
  }
  function chainMove(a, b, mode) {
    const list = vis1('.arc-list'); if (!list || list.classList.contains('lock')) return false;
    const rows = [...list.children]; const A = rows[a - 1]; if (!A) return false;
    if (mode === 'swap') { const B = rows[b - 1]; if (!B || A === B) return false; const ph = D.createElement('div'); list.insertBefore(ph, A); list.insertBefore(A, B); list.insertBefore(B, ph); ph.remove(); }
    else if (mode === 'up') { if (A.previousElementSibling) list.insertBefore(A, A.previousElementSibling); }
    else if (mode === 'down') { if (A.nextElementSibling) list.insertBefore(A.nextElementSibling, A); }
    else if (mode === 'to') { const B = rows[b - 1]; if (!B) return false; list.insertBefore(A, a < b ? B.nextElementSibling : B); }
    chainReset(list); try { sfx('tap'); } catch (e) {}
    const pos = [...list.children].indexOf(A) + 1; const m = `${txt($1('.arc-rt', A))} is now number ${pos} of ${rows.length}.`;
    announce(m); if (listenOn()) { lastKey = ''; say(m + ' ' + [...list.children].map((r, i) => `${i + 1}: ${sentence(txt($1('.arc-rt', r)))}`).join(' '), { force: true }); }
    return true;
  }
  function chainReset(list) { $$('.arc-row', list).forEach(r => r.classList.remove('good', 'bad')); const x = $1('.arc-x', list.closest('.arc-chain')); if (x) x.innerHTML = ''; }
  function help() {
    const ctx = [];
    if (getChoices().length) ctx.push('To choose, say a number, like "option 2", or say the answer.');
    if (vis1('.tfb,.arc-lb.yes')) ctx.push('Say true or false.');
    if (vis1('#tConf')) ctx.push('Say sure, think so, or guessing. Say mark, to come back later. Say submit at the end.');
    if (vis1('.arc-list')) ctx.push('Say "swap 1 and 3", "move 2 up", "move 4 to 1", then "check".');
    if (vis1('.arc-life')) ctx.push('Lifelines: say fifty fifty, ask Gappu, or skip.');
    if (vis1('.lab-box')) ctx.push('Say "describe the lab", or "hear the graph".');
    const en = 'Here is what you can say. Next. Back. Repeat. Read the lesson. Read the steps. Explain. Hint. Go home. Open maths, or any subject. Open chapter 2. Start test. Practice. Games. Pause. Ask, then your doubt. Stop talking. Slower, or faster. ' + ctx.join(' ') + ' On a keyboard: number keys choose, Enter goes next, R repeats, H is help, P pauses, M opens the microphone, Escape closes a window.';
    const hi = 'तुम ये बोल सकते हो: आगे। पीछे। दोबारा। पाठ पढ़ो। चरण पढ़ो। समझाओ। संकेत। घर। गणित खोलो। टेस्ट शुरू करो। मदद। जवाब के लिए विकल्प का नंबर बोलो, जैसे विकल्प दो।';
    const msg = courseLang() === 'hi' ? hi : en;
    announce(msg); if (listenOn() || recUsed) say(msg, { force: true }); return true;
  }
  const CMDS = [
    [/^(help|commands|what can i say|मदद|हेल्प|सहायता)$/, help],
    [/^(repeat|again|say (it|that) again|pardon|what did you say|read (the )?(screen|question|it)|दोबारा|फिर से|रिपीट|फिर बोलो)$/, () => { lastKey = ''; const d = readScreen(true); if (!listenOn()) say(d.text, { force: true }); return true; }],
    [/^(stop|quiet|be quiet|shh+|silence|stop talking|चुप|बस)$/, () => { stopSpeech(); return true; }],
    [/^(pause|wait|hold on|रुको)$/, () => { togglePause(true); return true; }],
    [/^(resume|go on|carry on|unpause|start again|चलो)$/, () => { togglePause(false); return true; }],
    [/^(slower|slow down|speak slower|धीरे)$/, () => setRate(-0.1)], [/^(faster|speed up|speak faster|तेज़|तेज)$/, () => setRate(0.1)],
    [/^(listen mode off|turn off listen mode|stop listen mode)$/, () => { UX.setListen(false); return true; }],
    [/^(listen|listen mode|turn on listen mode|listen mode on|read aloud)$/, () => { if (!listenOn()) UX.setListen(true); else { lastKey = ''; readScreen(true); } return true; }],
    [/^(true|right|yes it is|सही|सच)$/, () => clickFirst('.tfb[data-v="1"], .arc-lb.yes')],
    [/^(false|wrong|no it isnt|गलत|झूठ)$/, () => clickFirst('.tfb[data-v="0"], .arc-lb.no')],
    [/^(sure|i am sure|im sure|पक्का)$/, () => clickFirst('#tConf.show button[data-c=sure]')],
    [/^(think so|i think so|think|शायद)$/, () => clickFirst('#tConf.show button[data-c=think]')],
    [/^(guess|guessing|i am guessing|im guessing|अंदाज़ा|अंदाजा)$/, () => clickFirst('#tConf.show button[data-c=guess]')],
    [/^(mark|mark it|review later|flag)$/, () => clickFirst('#tMark')],
    [/^(submit|finish test|submit test)$/, () => clickFirst('#tNext')],
    [/^(roll|roll the dice|roll dice|पासा)$/, () => clickFirst('.arc-roll:not([disabled])')],
    [/^(check|check order|check it)$/, () => clickFirst('.arc-check')],
    [/^(fifty fifty|50 50|5050|50:50)$/, () => clickFirst('.arc-life[data-l=fifty]:not([disabled])')],
    [/^(ask gappu|gappu)$/, () => clickFirst('.arc-life[data-l=gappu]:not([disabled])')],
    [/^(skip|skip it|skip this)$/, () => clickFirst('.arc-life[data-l=skip]:not([disabled]), #tSkip')],
    [/^(play again|again please)$/, () => clickFirst('.arc-again')],
    [/^(explain to gappu|done explaining|send)$/, () => clickFirst('#tBtn')],
    [/^(next|continue|go on|okay|ok|next one|next question|आगे|अगला|नेक्स्ट|आगे बढ़ो)$/, () => { if (paused) togglePause(false); return primary() || (say('There is no next button here. Say help.', { force: true }), true); }],
    [/^(previous|previous question|last question|पिछला)$/, () => clickFirst('#qPrev, #nxPrev, #tPrev:not([disabled]), #rvPrev:not([disabled])')],
    [/^(back|go back|पीछे|वापस|बैक)$/, back],
    [/^((go )?home|home screen|main menu|घर|होम|घर चलो)$/, goHome],
    [/^(read|read the|read me)? ?(the )?(lesson|lessons|topic|whole lesson|big ideas)$|^(पाठ|पाठ पढ़ो|पूरा पाठ)$/, readLesson],
    [/^(read )?(the )?(steps|solution|working|example)$|^(how (do i|to) solve( it)?)$|^(चरण|चरण पढ़ो|हल)$/, readSteps],
    [/^(explain|why|explanation|tell me why|समझाओ|क्यों)$/, explain],
    [/^(hint|clue|give me a hint|a hint|संकेत|हिंट)$/, hint],
    [/^(start|begin|let'?s go|let'?s play|play)$/, () => primary() || startTest()],
    [/^(start (a |the )?(chapter |mock )?test|take (a |the )?test|test|mock test|chapter test|टेस्ट|टेस्ट शुरू करो)$/, startTest],
    [/^(describe|describe the lab|what is on (the )?screen|where am i|लैब बताओ)$/, () => { if (labState.box && labState.box.isConnected) { describeLab(true); return true; } lastKey = ''; const d = readScreen(true); if (!listenOn()) say(d.text, { force: true }); return true; }],
    [/^(hear|play|listen to)? ?(the )?(graph|chart|picture|sound|pattern)$|^count( it)?$/, () => { if (labState.box && labState.box.isConnected) { hearLab(); return true; } say('There is no graph on this screen.', { force: true }); return true; }],
    [/^(revision sheet|revise)$/, () => clickFirst('#chSheet')],
    [/^(games|arcade|play games|खेल)$/, () => openThing('games')],
    [/^(practice|practise|अभ्यास)$/, () => openThing('practice')],
    [/^(settings|open settings)$/, () => openThing('settings')]
  ];
  function setRate(d) { try { VOICE.rate = Math.max(.6, Math.min(1.3, (VOICE.rate || .9) + d)); localStorage.setItem('sv_voice', JSON.stringify(VOICE)); } catch (e) {} say(d > 0 ? 'Faster.' : 'Slower.', { force: true }); return true; }
  function tryCommand(said) {
    const ch = getChoices();
    if (ch.length) { const hit = ch.findIndex(e => norm(labelOf(e).replace(/^(left|right):\s*/i, '')) === said || norm(e.textContent) === said); if (hit >= 0 && !CMDS.slice(0, 3).some(([re]) => re.test(said))) return pick(hit + 1); }
    let m;
    if ((m = said.match(/^swap\s+(\S+)\s+(?:and|with)\s+(\S+)$/))) { const a = numberIn(m[1]), b = numberIn(m[2]); if (a && b) return chainMove(a, b, 'swap'); }
    if ((m = said.match(/^move\s+(\S+)\s+(up|down)$/))) { const a = numberIn(m[1]); if (a) return chainMove(a, 0, m[2]); }
    if ((m = said.match(/^move\s+(\S+)\s+to\s+(\S+)$/))) { const a = numberIn(m[1]), b = numberIn(m[2]); if (a && b) return chainMove(a, b, 'to'); }
    if ((m = said.match(/^(?:open|go to|show|start)\s+(.+)$/)) || (m = said.match(/^(.+)\s+(?:खोलो|खोलें|खोल दो)$/))) { if (openThing(m[1])) return true; }
    if ((m = said.match(/^(?:ask|doubt|question)\s+(.{3,})$/))) { Ask.open(); setTimeout(() => Ask.ask(m[1]), 400); return true; }
    for (const [re, fn] of CMDS) if (re.test(said)) { const r = fn(said); if (r !== false) return true; }
    const n = numberIn(said); if (n) return pick(n);
    if (ch.length && said.length >= 3) { const hits = ch.map((e, i) => [i, norm(labelOf(e))]).filter(([, l]) => l && (l.includes(said) || (said.includes(l) && l.length >= 3))); if (hits.length === 1) return pick(hits[0][0] + 1); }
    if (said.split(' ').length <= 3 && openThing(said)) return true;
    return false;
  }
  function handleSpeech(alts) {
    alts = alts.map(a => String(a || '').trim()).filter(Boolean); if (!alts.length) return;
    for (const a of alts) { const s = norm(a); if (s && tryCommand(s)) return; }
    const r = scope(), raw = alts[0];
    const ans = $1('#ans', r); if (ans && visible(ans)) { ans.value = (ans.value + ' ' + raw).trim(); ans.dispatchEvent(new Event('input', { bubbles: true })); say(T('gotIt') + ' ' + T('teach'), { force: true }); return; }
    const ask = $1('#askIn', r); if (ask && visible(ask)) { Ask.ask(raw); return; }
    say(T('notCaught'), { force: true });
  }

  /* ================= 4. Keyboard ================= */
  let digitBuf = '', digitT = 0;
  const isTyping = a => a && ((/^(input|textarea|select)$/i.test(a.tagName) && !/^(range|checkbox|radio|button)$/i.test(a.type || '')) || a.isContentEditable);
  const isInteractive = a => a && a !== D.body && (a.matches('button,a[href],input,select,textarea,summary,[role=button],[role=radio],[role=tab],[role=switch],[role=checkbox]') || a.isContentEditable);
  D.addEventListener('keydown', e => {
    lastKeyAt = now();
    if (e.defaultPrevented || e.ctrlKey || e.metaKey || e.altKey) return;
    if (!isTyping(D.activeElement)) maybeOffer('key');   // never interrupt someone typing a name or an answer
    const a = D.activeElement;
    if (e.key === 'Escape') { if (closeTop()) { e.preventDefault(); } else if (recActive()) stopRec(); else stopSpeech(); return; }
    if (isTyping(a)) return;
    if (a && a.closest && a.closest('.lab-box') && !/^[Hh?]$/.test(e.key)) return;    // labs keep their own keys
    const role = a && a.getAttribute && a.getAttribute('role');
    if ((role === 'radio' || role === 'tab') && /^Arrow(Left|Right|Up|Down)$/.test(e.key)) {
      const grp = a.closest(role === 'radio' ? '[role=radiogroup]' : '[role=tablist]'); const items = $$(`[role=${role}]`, grp); const i = items.indexOf(a);
      const j = (i + (/Right|Down/.test(e.key) ? 1 : -1) + items.length) % items.length; e.preventDefault(); items[j].focus(); items[j].click(); return;
    }
    if (/^[0-9]$/.test(e.key) && !e.repeat) {
      if (a && a.closest && a.closest('.sheet.show:not(#svOffer)') && !getChoices().length) return;
      const ch = getChoices(); if (!ch.length) return;
      e.preventDefault(); clearTimeout(digitT); digitBuf += e.key;
      const go = () => { const n = +digitBuf; digitBuf = ''; if (n >= 1) pick(n); };
      if (ch.length >= 10 && digitBuf.length === 1 && +digitBuf <= Math.floor(ch.length / 10)) digitT = setTimeout(go, 700); else go();
      return;
    }
    if (e.key === 'Enter' && !isInteractive(a)) { if (primary()) e.preventDefault(); return; }
    const k = e.key.toLowerCase();
    if (k === 'r' && !e.repeat) { lastKey = ''; const d = readScreen(true); if (!listenOn()) { announce(d.text); } e.preventDefault(); }
    else if ((k === 'h' || e.key === '?') && !e.repeat) { help(); e.preventDefault(); }
    else if (k === 'p' && !e.repeat) { togglePause(); e.preventDefault(); }
    else if ((k === 'm' || k === 'v') && !e.repeat && listenOn()) { recActive() ? stopRec() : startRec({}); e.preventDefault(); }
    else if (k === 's' && vis1('#tConf.show')) clickFirst('#tConf.show button[data-c=sure]');
    else if (k === 't' && vis1('#tConf.show')) clickFirst('#tConf.show button[data-c=think]');
    else if (k === 'g' && vis1('#tConf.show')) clickFirst('#tConf.show button[data-c=guess]');
  });

  /* ---------- hold-to-talk button ---------- */
  function buildTalk() {
    if ($1('#svTalk')) return;
    D.body.insertAdjacentHTML('beforeend', `<button id="svTalk" class="sv-talk" aria-pressed="false" aria-label="Hold to talk. Say help to hear what you can say."><span aria-hidden="true">🎤</span><b>Hold to talk</b></button>`);
    const b = $1('#svTalk'); let downAt = 0;
    b.addEventListener('pointerdown', e => { e.preventDefault(); downAt = now(); holding = true; startRec({ hold: true }); try { b.setPointerCapture(e.pointerId); } catch (er) {} });
    const up = () => { if (!holding) return; holding = false; const held = now() - downAt; if (held < 350) { stopRec(); setTimeout(() => startRec({}), 60); } else setTimeout(() => { if (rec) try { rec.stop(); } catch (e) {} }, 250); };
    b.addEventListener('pointerup', up); b.addEventListener('pointercancel', up);
    b.addEventListener('click', e => { if (now() - downAt < 1500) return; recActive() ? stopRec() : startRec({}); });
    b.addEventListener('keydown', e => { if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) { e.preventDefault(); e.stopPropagation(); downAt = now(); holding = true; startRec({ hold: true }); } });
    b.addEventListener('keyup', e => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); up(); } });
  }

  /* ---------- quick Listen-mode switch for screen-reader and keyboard users (first thing on the page) ---------- */
  function buildSkip() {
    if ($1('#svQuick')) return;
    D.body.insertAdjacentHTML('afterbegin', `<button id="svQuick" class="sv-skip">Turn on Listen mode: the app reads everything aloud</button>`);
    const b = $1('#svQuick'); b.onclick = () => { if (listenOn()) UX.settings(); else UX.setListen(true); };
    const paint = () => { b.textContent = listenOn() ? 'Listen mode is on. Open reading and accessibility settings' : 'Turn on Listen mode: the app reads everything aloud'; };
    paint(); A11Y._paintSkip = paint;
  }

  /* ---------- first launch: offer Listen mode ---------- */
  let lastPtr = 0, lastKeyAt = 0, offered = false;
  D.addEventListener('pointerdown', () => { lastPtr = now(); }, true);
  D.addEventListener('click', e => { if (e.isTrusted && now() - lastPtr > 900 && now() - lastKeyAt > 900 && e.target !== D.body) maybeOffer('sr'); }, true);
  D.addEventListener('focusin', e => { if (!selfFocus && e.isTrusted && now() - lastPtr > 900 && now() - lastKeyAt > 900 && e.target !== D.body && !isTyping(e.target) && D.hasFocus()) maybeOffer('sr'); }, true);   // never while focusing a text box
  function maybeOffer(why) {
    if (offered || U().asked || listenOn()) return;
    if (why === 'key' && (g('ST') || {}).profile) return;          // keys: only on first launch; screen readers: any time, once
    offered = true;
    setTimeout(() => offerListen(why), why === 'key' ? 30 : 300);
  }
  function offerListen() {
    if ($1('#svOffer')) return;
    D.body.insertAdjacentHTML('beforeend', `<div class="sheet" id="svOffer"><div class="sheet-in"><div class="sheet-grab"></div><h2 id="svOfferT"><span aria-hidden="true">🎧</span> Shall I read the app aloud?</h2>
      <p class="sub" id="svOfferP">Listen mode reads every screen and question to you. You can answer with number keys, or with your voice.</p>
      <button class="btn" id="svOfferYes">Yes, turn on Listen mode</button><div style="height:8px"></div><button class="btn ghost" id="svOfferNo">No thanks</button></div></div>`);
    const s = $1('#svOffer'); s.setAttribute('aria-describedby', 'svOfferP'); watchSheets();
    const done = yes => { s.classList.remove('show'); setTimeout(() => s.remove(), 300); if (yes) UX.setListen(true); else { U().asked = true; UX.save(); } stopRec(); };
    $1('#svOfferYes').onclick = () => done(true); $1('#svOfferNo').onclick = () => done(false);
    s.classList.add('show');
    setTimeout(() => focusEl($1('#svOfferYes')), 80);
    say('Welcome to StudyVerse. Shall I read the app aloud for you? Press Enter, or say yes, to turn on Listen mode. Press Escape, or say no, to skip.', { force: true }).then(() => {
      if (!SR || !s.isConnected || !navigator.permissions) return;
      navigator.permissions.query({ name: 'microphone' }).then(p => { if (p.state !== 'granted' || !s.isConnected) return;
        try { const r = new SR(); r.lang = 'en-IN'; r.onresult = e => { const t = norm(e.results[0][0].transcript); if (/^(yes|yeah|listen|ok|okay|हाँ|हां)/.test(t)) done(true); else if (/^(no|nope|नहीं)/.test(t)) done(false); }; r.start(); } catch (e) {} }).catch(() => {});
    });
  }

  /* ================= 5. Labs: description, narration and sonification ================= */
  const LABDESC = {
    algebratiles: 'Coloured tiles stand for x squared, x and ones. Sliders change how many of each, to build and factor expressions.',
    anglemaker: 'An angle with one arm that turns. As it opens, the size in degrees and the type of angle are read out.',
    areagrid: 'A grid of squares. Shapes are made of squares, and the app counts the area and the perimeter.',
    arraygrid: 'Rows and columns of objects, to see multiplication and sharing. Change the rows and columns and hear the total.',
    atom3d: 'A 3D model of an atom, with the nucleus in the middle and electrons in shells around it.',
    balance: 'A balance scale. Both sides must weigh the same, just like both sides of an equation.',
    bodysystem: 'A picture of the body. Choose a system to hear its parts and what they do.',
    budget: 'Money in and money out. Sliders change income, spending and interest, and the totals are read out.',
    calculuslab: 'A curve with a moving point. It shows the slope, the tangent and the area under the curve.',
    cell3d: 'A 3D model of a cell with its parts, like the nucleus, cell membrane and mitochondria.',
    circlelab: 'A circle with its radius, diameter and circumference, worked out as the size changes.',
    circuit: 'An electric circuit with a cell, wires, a switch and a bulb. Close the switch and the bulb lights up.',
    circularflow: 'Money and goods flowing in a circle between households, firms and the government.',
    clockset: 'A clock face with an hour hand and a minute hand. Set the time and hear it read.',
    compare: 'Two things side by side, to compare which is longer, heavier, more or less.',
    coordplane: 'A grid with an x axis and a y axis. Points are placed by their coordinates.',
    datachart: 'A chart made of bars or pictures. Each bar shows how many. Say "hear the graph" to hear the bars as notes, low for few and high for many.',
    density: 'A tank of water. Objects sink or float depending on their density.',
    dnalab: 'A DNA ladder. A pairs with T, and G pairs with C.',
    earthlayers3d: 'A 3D model of the Earth cut open, showing the crust, mantle, outer core and inner core.',
    fieldlines: 'Electric charges with field lines going from positive to negative.',
    flowchart: 'Steps in a process, one after another, like a flow chart.',
    foodchain: 'A food chain: who eats whom, from plants to animals.',
    forces: 'Pushes and pulls on an object. Bigger forces make bigger changes in motion.',
    fractionbar: 'Bars and pies cut into equal parts, to see fractions. The fraction is read out as it changes.',
    globe3d: 'A 3D globe of the Earth that turns, with lines of latitude and longitude.',
    graphplot: 'A graph with an x axis and a y axis, and a line or curve. Say "hear the graph": the tone rises when the line goes up and falls when it goes down, and clicks where it crosses the x axis.',
    indiamap: 'A map of India with its states and places.',
    letterlab: 'Letters and their sounds. Choose a letter to hear it and words that start with it.',
    magnetlab: 'Magnets with north and south poles. Like poles push away, unlike poles pull together.',
    matchpairs: 'Pairs to match: each item on one side goes with one item on the other side.',
    matrabuilder: 'Hindi letters with matras. Add a matra to a letter to make a new sound.',
    molecule3d: 'A 3D model of a molecule, showing atoms joined by bonds.',
    moneycounter: 'Coins and notes in rupees. Add them up to make an amount.',
    moon3d: 'A 3D model of the Moon and its phases as it goes around the Earth.',
    motion: 'An object moving. Distance, speed and time are shown and read out.',
    numberline: 'A number line with a frog. The frog hops along the numbers to show adding, taking away and skip counting. Say "count it" to hear the number as beeps.',
    optics: 'Light rays going through lenses and bouncing off mirrors.',
    particles: 'Tiny particles in a box. They move faster when hotter, as in solids, liquids and gases.',
    patternbuilder: 'A pattern of shapes or numbers that repeats or grows. Find what comes next.',
    patterns: 'Number and shape patterns. Say "hear the graph" to hear how the pattern grows.',
    periodictable: 'The periodic table of elements, in rows called periods and columns called groups.',
    phlab: 'Test tubes with an indicator. The colour shows if a liquid is an acid, neutral or a base, on the pH scale from 0 to 14.',
    photosynthesis: 'A plant using sunlight, water and carbon dioxide to make food and oxygen.',
    placevalue: 'An abacus with hundreds, tens and ones. Beads add up to a number. Say "count it" to hear it as beeps.',
    plant3d: 'A 3D model of a plant with its roots, stem, leaves and flower.',
    probability: 'A chance machine with coins, dice or spinners. It counts how often each result happens.',
    punctuation: 'A sentence that needs punctuation marks, like a full stop, comma or question mark.',
    punnett: 'A Punnett square to work out which traits children can get from their parents.',
    ratiolab: 'Two amounts compared as a ratio. Change one and see the other.',
    reaction: 'A chemical equation to balance, so there are the same atoms on both sides.',
    sandhi: 'Two words joined by sandhi rules to make one word.',
    sentencebuilder: 'Word cards to put in order to make a sentence.',
    simplemachines: 'Levers, pulleys and ramps that make work easier.',
    solar3d: 'A 3D model of the Sun and the planets going around it.',
    solid3d: 'A 3D solid shape that turns, with its faces, edges and corners counted.',
    sortbins: 'Items to sort into the right bins or groups.',
    sound: 'A sound wave. Loudness and pitch change the wave. You can hear the sound.',
    statlab: 'A set of data with its mean, median and mode. Say "hear the graph" to hear the values.',
    storysequence: 'Parts of a story to put in the right order.',
    supplydemand: 'Supply and demand lines. Where they cross is the market price. Say "hear the graph" to hear the lines.',
    symmetry: 'A shape and its mirror line. Both halves match.',
    taccount: 'An accounting workbench with debit and credit sides that must balance.',
    tensemachine: 'A time machine for verbs: past, present and future tense.',
    timeline: 'Events in order of time, from earliest to latest.',
    titration: 'An acid and a base mixed drop by drop until the indicator changes colour.',
    triangle: 'A triangle with its sides and angles. The three angles always add up to 180 degrees.',
    unitcircle: 'A circle with radius one, used to find sine, cosine and tangent of an angle.',
    vectorlab: 'Arrows called vectors, with size and direction, added head to tail.',
    watercycle3d: 'The water cycle: evaporation, condensation, rain and collection.',
    wavelab: 'A wave with its wavelength, amplitude and frequency. Say "hear the graph" to hear the wave.',
    wordbuilder: 'Letters or parts to join into words.',
    worldmap: 'A map of the world with its continents and oceans.'
  };
  const labState = { box: null, host: null, spec: null, def: null, snap: [], desc: '' };
  function labLines(box) {
    /* readable lines: a short row of chips ("3", "hops of", "+2", "= 6") becomes one sentence */
    const out = [];
    const walk = el => {
      if (el.matches('button,svg,script,style,canvas,.sv-labbar,.lab-spk,[aria-hidden="true"]') || !visible(el)) return;
      const t = clean((el.innerText || '').replace(/\n+/g, ' '));
      if (!t) return;
      if (t.length <= 140 && !$1('button,input,select,textarea,svg,canvas', el)) { out.push(t); return; }
      [...el.childNodes].forEach(n => { if (n.nodeType === 3) { const x = clean(n.nodeValue); if (x) out.push(x); } else if (n.nodeType === 1) walk(n); });
    };
    [...box.children].forEach(walk);
    return [...new Set(out.filter(l => /[\p{L}\p{N}]/u.test(l)))];
  }
  function controlsSummary(box) {
    const sl = $$('input[type=range]', box).filter(visible).map(i => i.getAttribute('aria-label') || '').filter(Boolean);
    const bt = $$('button:not(.spk)', box).filter(visible).map(b => clean(b.getAttribute('aria-label') || b.textContent)).filter(Boolean);
    return [sl.length ? `${sl.length} slider${sl.length > 1 ? 's' : ''}: ${sl.slice(0, 5).join(', ')}` : '', bt.length ? `buttons: ${bt.slice(0, 8).join(', ')}` : ''].filter(Boolean).join('; and ');
  }
  function describeLab(full, speakIt = true) {
    const { box, spec, def } = labState; if (!box || !box.isConnected) return '';
    const run = g('RUN'), t = run && run.t;
    const lines = labLines(box).slice(0, 10);
    const ctl = controlsSummary(box);
    const parts = [`${def.title || 'Lab'}`, LABDESC[spec.type] || '', ctl ? 'It has ' + ctl : '', lines.length ? 'Right now it shows: ' + lines.join('. ') : ''];
    if (full && t) { const L = t.learn || {}; parts.push(t.revise && t.revise.summary ? 'In short: ' + t.revise.summary : L.hook, ...((L.points || []).slice(0, 4))); }
    const text = join(parts) + (hasSound(box) ? ' Say "hear the graph", or use the Hear it button.' : '');
    labState.desc = text;
    if (speakIt) { announce(text); if (listenOn() || full === 'btn') say(text, { force: true }); }
    return text;
  }
  function labelRanges(box) {
    $$('input,select,textarea', box).forEach(i => {
      if (i.getAttribute('aria-label') || i.getAttribute('aria-labelledby') || (i.id && $1(`label[for="${i.id}"]`, box)) || i.closest('label')) return;
      let t = '';
      const prev = i.previousElementSibling; if (prev && !prev.matches('input,button')) t = clean(prev.textContent);
      if (!t && i.parentElement) { const c = i.parentElement.cloneNode(true); $$('input,select,output,button', c).forEach(x => x.remove()); t = clean(c.textContent); }
      if (!t) { const nx = i.nextElementSibling; if (nx && !nx.matches('input,button')) t = clean(nx.textContent); }
      i.setAttribute('aria-label', (t || i.name || 'Value').slice(0, 60));
    });
    const SYMN = { '+': 'more', '−': 'less', '-': 'less', '–': 'less', '⤢': 'full screen', '↺': 'reset', '⟲': 'reset', '↻': 'turn', '‹': 'previous', '◀': 'previous', '›': 'next', '▶': 'play', '⏸': 'pause', '✕': 'close', '×': 'close', '?': 'help' };
    $$('button', box).forEach(b => {
      if (b.getAttribute('aria-label') || b.closest('.sv-labbar')) return; const t = b.textContent.trim(); if (!SYMN[t]) return;
      let ctx = ''; const p = b.parentElement;
      if (p) { const ls = [...p.childNodes].filter(n => !(n.nodeType === 1 && n.matches('button,input,output,select'))).map(n => clean(n.textContent)).filter(x => x && !/^[\d.\s−-]+$/.test(x)); if (ls.length === 1) ctx = ls[0]; }
      b.setAttribute('aria-label', (ctx && ctx.length < 30 ? ctx + ': ' : '') + SYMN[t]);
    });
    $$('[aria-label]:not([role])', box).forEach(e => { if (/^(DIV|SPAN|P|I|B)$/.test(e.tagName)) e.setAttribute('role', e.children.length ? 'group' : 'img'); });
    $$('[role=img]:not([aria-label]):not([aria-labelledby]),[role=image]:not([aria-label])', box).forEach(e => e.setAttribute('aria-label', clean(e.textContent) || `${labState.def.title} picture`));
    $$('*', box).forEach(e => { if (e.closest('svg') || e.matches(FOCUSABLE)) return; const cs = getComputedStyle(e); if (!/(auto|scroll)/.test(cs.overflowX + cs.overflowY)) return; if (e.scrollWidth <= e.clientWidth + 4 && e.scrollHeight <= e.clientHeight + 4) return; if ($1(FOCUSABLE, e)) return; e.tabIndex = 0; if (!e.getAttribute('role')) e.setAttribute('role', 'region'); if (!e.getAttribute('aria-label')) e.setAttribute('aria-label', 'Scrollable part of the lab. Use arrow keys to scroll.'); });
    $$('svg', box).forEach(s => { if (s.hasAttribute('role') || s.closest('button')) return; const f = $1(FOCUSABLE, s); s.setAttribute('role', f ? 'group' : 'img'); s.setAttribute('aria-label', `${labState.def.title} picture. Use Describe to hear what it shows.`); });
    $$('canvas', box).forEach(c => { c.setAttribute('role', 'img'); c.setAttribute('aria-label', `${labState.def.title}: a moving 3D picture. Use Describe to hear what it shows.`); });
  }
  /* labs set their own colours; darken any lab text that is below WCAG AA contrast (same hue, just deeper) */
  const rgbOf = c => { const m = String(c).match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p[3] == null ? 1 : p[3] }; };
  const lumOf = c => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(c.r) + .7152 * f(c.g) + .0722 * f(c.b); };
  const ratioOf = (a, b) => { const x = lumOf(a), y = lumOf(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  function bgOf(el) { const layers = []; let owner = null; for (let e = el; e; e = e.parentElement) { const st = getComputedStyle(e); if (st.backgroundImage !== 'none') return null; const c = rgbOf(st.backgroundColor); if (c && c.a > 0) { layers.push(c); if (c.a >= 1) { owner = e; break; } } }
    if (!layers.length || layers[layers.length - 1].a < 1) return null; let bg = layers.pop(); const solo = !layers.length; while (layers.length) { const t = layers.pop(); bg = { r: t.r * t.a + bg.r * (1 - t.a), g: t.g * t.a + bg.g * (1 - t.a), b: t.b * t.a + bg.b * (1 - t.a), a: 1 }; } bg.owner = solo ? owner : null; return bg; }
  const fixedSel = new Set();
  function cssFix(el, prop, val) {
    /* a CSS rule (not an inline style) so labs that redraw their readouts keep the fix */
    const cls = e => [...e.classList].filter(c => /^[\w-]+$/.test(c) && !/^(ra-w|ra-reading|popin|shake)$/.test(c)).map(c => '.' + c).join('');
    const p = el.parentElement, own = el.tagName.toLowerCase() + cls(el), par = p && !p.classList.contains('lab-box') ? p.tagName.toLowerCase() + cls(p) : '';
    let anc = ''; if (!/\.lb-/.test(par + own)) for (let e = p && p.parentElement; e && !e.classList.contains('lab-box'); e = e.parentElement) { const c = [...e.classList].find(x => /^lb-[\w-]+$/.test(x)); if (c) { anc = '.' + c + ' '; break; } }
    const sel = `.lab-box ${anc}${par ? par + ' > ' : ''}${own}`;
    if (!/\.lb-/.test(sel)) { el.style.setProperty(prop, val); return; }      // rules must stay inside one lab type
    if (fixedSel.has(sel + prop)) { el.style.setProperty(prop, val); return; }
    /* only share the fix when every matching element has the same colours (per-item colours get their own inline fix) */
    const key = e => { const b = bgOf(e); return getComputedStyle(e).color + '|' + (b ? `${Math.round(b.r)},${Math.round(b.g)},${Math.round(b.b)}` : '?') + '|' + getComputedStyle(e).backgroundColor; };
    const k0 = key(el); let same = true; try { same = $$(sel.slice(9), el.closest('.lab-box') || D).every(x => key(x) === k0); } catch (e) { same = false; }
    if (!same) { el.style.setProperty(prop, val); return; }
    fixedSel.add(sel + prop);
    let st = D.getElementById('svLabContrast'); if (!st) { st = D.createElement('style'); st.id = 'svLabContrast'; D.head.appendChild(st); }
    try { st.sheet.insertRule(`${sel}{${prop}:${val}!important}`, st.sheet.cssRules.length); } catch (e) { el.style.setProperty(prop, val); }
  }
  function autoContrast(root) {
    $$('*', root).forEach(el => {
      if (el.closest('svg') || el.closest('.sv-labbar') || !visible(el)) return;
      if (![...el.childNodes].some(n => n.nodeType === 3 && /[\p{L}\p{N}]/u.test(n.nodeValue))) return;
      const st = getComputedStyle(el); let fg = rgbOf(st.color); const bg = bgOf(el); if (!fg || !bg || fg.a < 1) return;
      const px = parseFloat(st.fontSize), need = (px >= 24 || (+st.fontWeight >= 700 && px >= 18.66)) ? 3.1 : 4.6;
      if (ratioOf(fg, bg) >= need) return;
      const rgb = c => `rgb(${Math.round(c.r)},${Math.round(c.g)},${Math.round(c.b)})`; let k = 0;
      const INK = { r: 27, g: 31, b: 58 };
      if (lumOf(fg) > lumOf(bg)) {
        /* light text on a coloured chip: dark ink if that reads well, otherwise deepen the chip (if it is this element or its parent) */
        if (ratioOf(INK, bg) >= need + .3) { cssFix(el, 'color', rgb(INK)); return; }
        const o = bg.owner; if (!o || !root.contains(o) || (o !== el && o !== el.parentElement)) return;
        let b2 = { r: bg.r, g: bg.g, b: bg.b }; while (ratioOf(fg, b2) < need && k++ < 30) b2 = { r: b2.r * .93, g: b2.g * .93, b: b2.b * .93 };
        cssFix(o, 'background-color', rgb(b2)); return;
      }
      while (ratioOf(fg, bg) < need && k++ < 12) fg = { r: fg.r * .88, g: fg.g * .88, b: fg.b * .88 };
      if (ratioOf(fg, bg) < need) fg = ratioOf({ r: 255, g: 255, b: 255 }, bg) > ratioOf({ r: 0, g: 0, b: 0 }, bg) ? { r: 255, g: 255, b: 255 } : { r: 0, g: 0, b: 0 };
      cssFix(el, 'color', rgb(fg));
    });
  }
  function labMounted(host, box, spec, def) {
    labState.box = box; labState.host = host; labState.spec = spec; labState.def = def || {};
    try {
      box.setAttribute('role', 'group'); box.setAttribute('aria-label', `${def.title || 'Lab'}: hands-on lab`);
      host.insertAdjacentHTML('afterbegin', `<div class="sv-labbar" role="toolbar" aria-label="Lab tools for blind and low-vision learners"><button type="button" class="sv-ldesc">🔊 Describe</button><button type="button" class="sv-lhear">🎵 Hear it</button></div>`);
      $1('.sv-ldesc', host).onclick = () => describeLab('btn');
      $1('.sv-lhear', host).onclick = () => hearLab();
      labelRanges(box); autoContrast(box);
      labState.snap = labLines(box);
      let lt = 0;
      const changed = e => {
        if (e && e.type === 'input' && e.target.type === 'range' && listenOn()) { const i = e.target, f = (+i.value - +(i.min || 0)) / ((+(i.max || 100) - +(i.min || 0)) || 1); Son.blip(Son.pitch(f), 0, .07, 0, 'triangle', .18); }
        clearTimeout(lt); lt = setTimeout(() => {
          if (!box.isConnected) return; labelRanges(box); autoContrast(box);
          const cur = labLines(box), old = new Set(labState.snap); labState.snap = cur;
          const diff = cur.filter(l => !old.has(l)).slice(0, 4);
          if (!diff.length) return; const m = diff.join('. ');
          announce(m); if (listenOn()) say(m, { force: true });
        }, 550);
      };
      box.addEventListener('input', changed, true); box.addEventListener('change', changed, true); box.addEventListener('click', changed, true); box.addEventListener('pointerup', changed, true);
      [300, 900, 1800].forEach(ms => setTimeout(() => { if (box.isConnected) { autoContrast(box); labelRanges(box); } }, ms));
      if (listenOn() && host.closest('#sheet3d')) setTimeout(() => describeLab(true), 300);
      else setTimeout(() => describeLab(false, false), 50);
    } catch (e) { console.warn('lab a11y', e); }
  }
  function labUnmounted() { labState.box = null; labState.desc = ''; }

  /* ---------- sonification (Web Audio) ---------- */
  const Son = {
    ac() { try { initAudio(); } catch (e) {} try { if (typeof SND !== 'undefined' && SND.ctx) return { c: SND.ctx, d: SND.sfx }; } catch (e) {} if (!this._c) { try { this._c = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { return null; } } return { c: this._c, d: this._c.destination }; },
    pitch: f => 220 * Math.pow(2, 2.4 * Math.max(0, Math.min(1, f))),
    blip(freq, at = 0, dur = .12, pan = 0, type = 'sine', gain = .25) {
      const a = this.ac(); if (!a) return; const { c, d } = a, t = c.currentTime + .02 + at;
      const o = c.createOscillator(), gn = c.createGain(); o.type = type; o.frequency.setValueAtTime(freq, t);
      let n = gn; if (c.createStereoPanner) { const p = c.createStereoPanner(); p.pan.value = pan; gn.connect(p); n = p; }
      o.connect(gn); n.connect(d); gn.gain.setValueAtTime(0, t); gn.gain.linearRampToValueAtTime(gain, t + .01); gn.gain.exponentialRampToValueAtTime(.0001, t + dur); o.start(t); o.stop(t + dur + .05);
    },
    curve(pts, axisY, dur = 2.6) {
      const a = this.ac(); if (!a || pts.length < 2) return 0; const { c, d } = a, t0 = c.currentTime + .05;
      const o = c.createOscillator(), gn = c.createGain(); o.type = 'triangle';
      let n = gn, pan = null; if (c.createStereoPanner) { pan = c.createStereoPanner(); gn.connect(pan); n = pan; }
      o.connect(gn); n.connect(d);
      gn.gain.setValueAtTime(0, t0); gn.gain.linearRampToValueAtTime(.22, t0 + .05);
      pts.forEach((p, i) => { const t = t0 + dur * i / (pts.length - 1); o.frequency.linearRampToValueAtTime(this.pitch(p.y), t); if (pan) pan.pan.linearRampToValueAtTime(p.x * 2 - 1, t); });
      gn.gain.setValueAtTime(.22, t0 + dur); gn.gain.linearRampToValueAtTime(0, t0 + dur + .08); o.start(t0); o.stop(t0 + dur + .12);
      if (axisY != null) for (let i = 1; i < pts.length; i++) if ((pts[i - 1].y - axisY) * (pts[i].y - axisY) < 0) this.blip(1800, .05 + dur * i / (pts.length - 1), .05, pts[i].x * 2 - 1, 'square', .12);
      return dur;
    },
    bars(vals) { const mx = Math.max(...vals, 1e-9); vals.forEach((v, i) => this.blip(this.pitch(v / mx), i * .32, .26, vals.length > 1 ? i / (vals.length - 1) * 1.6 - .8 : 0, 'triangle', .25)); return vals.length * .32; },
    count(n) { n = Math.max(0, Math.min(50, n | 0)); let t = 0; for (let i = 1; i <= n; i++) { this.blip(i % 5 === 0 ? 523 : 880, t, .09, 0, 'sine', .28); t += i % 5 === 0 ? .55 : .3; } return t; }
  };
  function svgCurves(box) {
    const out = [];
    $$('svg', box).forEach(svg => {
      const R = svg.getBoundingClientRect(); if (R.width < 40) return;
      let axisY = null, axisW = 0;
      $$('line', svg).forEach(l => { const b = l.getBoundingClientRect(); const sw = parseFloat(getComputedStyle(l).strokeWidth) || 1; if (b.height < 2 && b.width > R.width * .6 && sw * b.width > axisW) { axisW = sw * b.width; axisY = 1 - (b.top - R.top) / R.height; } });
      $$('path,polyline', svg).forEach(p => {
        const cs = getComputedStyle(p); if (cs.stroke === 'none' || cs.display === 'none' || (cs.fill !== 'none' && cs.fill !== 'rgba(0, 0, 0, 0)')) return;
        let L = 0; try { L = p.getTotalLength(); } catch (e) { return; }
        const m = p.getScreenCTM(); if (!m || L < 20) return;
        const pts = []; for (let i = 0; i <= 48; i++) { const q = p.getPointAtLength(L * i / 48).matrixTransform(m); pts.push({ x: (q.x - R.left) / R.width, y: 1 - (q.y - R.top) / R.height }); }
        const xs = pts.map(q => q.x), ys = pts.map(q => q.y), wx = Math.max(...xs) - Math.min(...xs), wy = Math.max(...ys) - Math.min(...ys);
        if (wx < .35) return;
        if (pts[0].x > pts[pts.length - 1].x) pts.reverse();
        out.push({ pts, axisY, score: wx + (wy > .02 ? .2 : 0) + (parseFloat(cs.strokeWidth) || 1) / 10 });
      });
    });
    return out.sort((a, b) => b.score - a.score);
  }
  function svgBars(box) {
    for (const svg of $$('svg', box)) {
      const rs = $$('rect', svg).map(r => ({ r, b: r.getBoundingClientRect() })).filter(x => x.b.width > 3 && x.b.height > 1);
      const byW = {}; rs.forEach(x => { const k = Math.round(x.b.width / 2) + '|' + Math.round((x.b.top + x.b.height) / 3); (byW[k] = byW[k] || []).push(x); });
      const best = Object.values(byW).filter(l => l.length >= 2 && new Set(l.map(x => Math.round(x.b.height))).size > 1).sort((a, b) => b.length - a.length)[0];
      if (best) return best.sort((a, b) => a.b.left - b.b.left).map(x => x.b.height);
    }
    return null;
  }
  function mainNumber(box) {
    /* the number worth counting: a result after "=", a value after a label like "Frog at" / "Total:", else the biggest number on show */
    const ls = labLines(box);
    for (let i = ls.length - 1; i >= 0; i--) { const m = ls[i].match(/=\s*(\d{1,2})\s*$/); if (m) return +m[1]; }
    for (let i = 0; i < ls.length - 1; i++) if (/(\bat|total|in all|sum|count|:)$/i.test(ls[i]) && /^\d{1,2}$/.test(ls[i + 1])) return +ls[i + 1];
    let best = null, size = 0;
    $$('*', box).forEach(el => { if (el.children.length || !visible(el) || el.closest('button,svg')) return; const m = (el.textContent || '').match(/^\D{0,12}(\d{1,2})\D{0,12}$/); if (!m) return; const fs = parseFloat(getComputedStyle(el).fontSize) || 0; if (fs > size) { size = fs; best = +m[1]; } });
    if (best == null) { for (const l of labLines(box)) { const m = l.match(/(?:^|[^\d.])(\d{1,2})(?![\d.])/); if (m && +m[1] > 0) { best = +m[1]; break; } } }
    return best;
  }
  const hasSound = box => !!(svgBars(box) || svgCurves(box).length || mainNumber(box));
  function hearLab() {
    const box = labState.box; if (!box) return;
    stopSpeech();
    const bars = svgBars(box); if (bars) { say(`${bars.length} bars, from left to right. Higher notes mean more.`, { force: true }).then(() => Son.bars(bars)); return; }
    const cv = svgCurves(box); if (cv.length) { const c = cv[0], up = c.pts[c.pts.length - 1].y - c.pts[0].y; say(`Here is the graph, from left to right.${c.axisY != null ? ' A click means it crosses the x axis.' : ''}`, { force: true }).then(() => { const d = Son.curve(c.pts, c.axisY); setTimeout(() => say(Math.abs(up) < .03 ? 'It stays level.' : up > 0 ? 'Overall it goes up.' : 'Overall it goes down.', { queue: true }), d * 1000 + 300); }); return; }
    const n = mainNumber(box); if (n) { say(`Counting to ${n}. Every fifth beep is lower.`, { force: true }).then(() => { const d = Son.count(n); setTimeout(() => say(String(n), { queue: true }), d * 1000 + 200); }); return; }
    say('This lab has no graph or number to play as sound. Say describe instead.', { force: true });
  }

  /* ================= 6. Hooks into the app ================= */
  function wrapGlobals() {
    if (typeof window.show === 'function' && !window.show._a11y) {
      const _show = window.show;
      window.show = function (id) { const r = _show.apply(this, arguments); screenChanged(); $$('nav button').forEach(b => { if (b.classList.contains('on')) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current'); }); return r; };
      window.show._a11y = true;
    }
    if (typeof window.sfx === 'function' && !window.sfx._a11y) {
      const _sfx = window.sfx;
      window.sfx = function (k) { try { onSfx(k); } catch (e) {} return _sfx.apply(this, arguments); };
      window.sfx._a11y = true;
    }
  }
  let lastChoiceAt = 0;
  D.addEventListener('click', e => { if (e.target.closest && e.target.closest('.opt,.tfb,.sbk,.mbtn,.ochip,.arc-lb,.arc-bk,.arc-tile,.arc-mc,.arc-check,.tst-conf button')) lastChoiceAt = now(); }, true);
  function onSfx(k) {
    if (k === 'correct' || (k === 'coin' && now() - lastChoiceAt < 1600)) { buzz('ok'); result(true); }
    else if (k === 'wrong') { buzz('bad'); result(false); }
    else if (k === 'unlock') buzz('win');
  }
  let resT = 0, pendingOk = null;
  function result(ok) {
    pendingOk = ok; clearTimeout(resT);
    resT = setTimeout(() => {
      const fb = lastFeedback && now() - lastFeedback.t < 1500 && lastFeedback.el.isConnected ? lastFeedback.el : null;
      let m = '';
      if (fb) m = fb.matches('.explain') ? feedbackSpeech(fb) : txt(fb);
      if (!m || !/[\p{L}]/u.test(m)) m = pendingOk ? T('correct') : T('wrong');
      else if (!/^(correct|not quite|wrong|right|सही|नहीं)/i.test(m) && !fb?.matches('.explain')) m = (pendingOk ? T('correct') : T('wrong')) + ' ' + m;
      announce(m);
    }, 260);
  }
  let screenT = 0, pendingScreen = false;
  function screenChanged() {
    pendingScreen = true; buzz('nav'); clearTimeout(screenT);
    screenT = setTimeout(() => { if (!pendingScreen) return; pendingScreen = false; if (!openSheet() && !isTyping(D.activeElement)) focusBest(true); }, 160);
  }

  /* one observer: fix semantics at once (micro-task), then focus / read after things settle */
  let lastFeedback = null, settleT = 0, swapFocus = false;
  const FEEDBACK = '.explain,.arc-exp,.arc-lwhy,.gdone,.arc-mline,.tfwhy,.arc-res,.lab-win.show';
  const VOLATILE = '.arc-time,#tTime,.arc-tmr,#tm,.timer,.arc-score,.arc-tbar,.arc-mv,.arc-pf,.arc-die,.arc-p0,.arc-p1,.arc-count,.arc-float,.arc-hpt,.arc-combo,.arc-hearts,.arc-lvl,.lab-loading';
  const REFIX = '.choice,.mbtn,#musicTgl,#gradeChips button,.tst-pal button,.arc-ladder span,.progress i,.hud-bar i';
  const isVolatile = n => { const e = n.nodeType === 1 ? n : n.parentElement; return !!(e && e.closest && e.closest(VOLATILE)); };
  const mainObs = new MutationObserver(recs => {
    let sig = false;
    for (const r of recs) {
      const t = r.target;
      if (r.type === 'attributes') {
        if (t.matches('.arc-mc')) memLabel(t);
        else if (t.matches(REFIX)) fix(t.closest('.progress,.hud-bar,.arc-ladder') || t);
        if (t.matches('.lab-win.show')) { lastFeedback = { el: t, t: now() }; announce(txt(t)); }
        else if (t.matches('.blank.ok,.blank.no')) lastFeedback = { el: t.closest('#fs') || t, t: now() };
        if (t.matches('.tst-conf,.opt,.blank,.mbtn,.tfcard,.arc-tiles,.choice,.sbk,#tPal,.arc-list,.arc-life')) sig = true;
        continue;
      }
      if (isVolatile(t)) continue;
      if (t.nodeType === 1 && t.matches('#sfb,.arc-sfb,.arc-slog,#tfw,.tfwhy')) lastFeedback = { el: t, t: now() };
      r.addedNodes.forEach(n => {
        if (n.nodeType !== 1) return; fix(n);
        if (n.matches('.arc-menu,.arc-game,.arc-res')) swapFocus = true;
        const f = n.matches(FEEDBACK) ? n : $1(FEEDBACK, n); if (f) { lastFeedback = { el: f, t: now() }; if (f.matches('.gdone,.arc-res')) announce(txt(f.matches('.arc-res') ? $1('h2', f) : f) + ' ' + txt($1('.arc-res-score', f))); }
      });
      sig = true;
    }
    if (!sig) return;
    clearTimeout(settleT);
    settleT = setTimeout(() => {
      const fresh = lastFeedback && now() - lastFeedback.t < 900 && lastFeedback.el.isConnected;
      if (swapFocus && !openSheet()) { swapFocus = false; focusBest(true); buzz('nav'); }
      else if (!openSheet() && !pendingScreen && (lostFocus() || (fresh && !isInteractive(D.activeElement)))) focusBest(false);
      readScreen();
    }, 320);
  });

  /* ---------------- boot ---------------- */
  function boot() {
    region('srLive'); region('srAlert', true);
    wrapGlobals(); wrapWorlds(); buildTalk(); buildSkip(); buildListenBar(); watchSheets();
    fix(D.body);
    mainObs.observe(D.querySelector('main') || D.body, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['class', 'disabled', 'hidden'] });
    new MutationObserver(recs => { recs.forEach(r => r.addedNodes.forEach(n => { if (n.nodeType === 1 && n !== D.querySelector('main')) fix(n); })); watchSheets(); }).observe(D.body, { childList: true });
    $$(SHEETS).forEach(s => mainObs.observe(s, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['class', 'disabled', 'hidden'] }));
    const watchNew = new MutationObserver(recs => recs.forEach(r => r.addedNodes.forEach(n => { if (n.nodeType === 1 && n.matches && n.matches(SHEETS)) mainObs.observe(n, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['class', 'disabled', 'hidden'] }); })));
    watchNew.observe(D.body, { childList: true });
    if (listenOn()) setTimeout(() => readScreen(true), 900);
  }
  /* visible controls while Listen mode is on: stop the current reading, or turn Listen mode off */
  function buildListenBar() {
    if ($1('#svLBar')) return;
    if (!$1('#svLBarCss')) D.head.insertAdjacentHTML('beforeend', `<style id="svLBarCss">#svLBar{display:none}html.sv-listen #svLBar{display:flex;position:fixed;top:calc(64px + env(safe-area-inset-top));left:50%;transform:translateX(-50%);z-index:965;gap:6px;align-items:center;background:#15161C;color:#fff;border-radius:999px;padding:5px 6px 5px 12px;box-shadow:0 6px 18px rgba(0,0,0,.35);font:600 13px/1 system-ui,sans-serif}#svLBar button{border:0;border-radius:999px;padding:8px 12px;font:700 13px/1 system-ui,sans-serif;cursor:pointer;min-height:36px}#svLBar .s{background:#fff;color:#15161C}#svLBar .o{background:#C9A76A;color:#15161C}</style>`);
    D.body.insertAdjacentHTML('beforeend', `<div id="svLBar" role="region" aria-label="Listen mode controls"><span aria-hidden="true">🎧</span><button type="button" class="s" id="svLStop">⏹ Stop reading</button><button type="button" class="o" id="svLOff">Turn off</button></div>`);
    $1('#svLStop').onclick = () => { stopSpeech(); toastQuiet('Stopped — tap 🎧 Listen in Aa settings to hear it again'); };
    $1('#svLOff').onclick = () => { UX.setListen(false); };
  }
  function listenChanged(on) {
    buildListenBar();
    D.documentElement.classList.toggle('sv-listen', on);
    if (A11Y._paintSkip) A11Y._paintSkip();
    if (on) { toastQuiet('🎧 Listen mode on'); announce(T('on')); lastKey = ''; say(T('on'), { force: true }).then(() => { if (!openSheet()) readScreen(true); }); }
    else { stopRec(); stopSpeech(); $$('[data-svn]').forEach(e => e.removeAttribute('data-svn')); toastQuiet(T('off')); announce(T('off')); }
  }

  const cue = m => { announce(m); if (listenOn()) say(m, { force: true }); };
  const announceToast = m => { const l = region('srToast'); l.textContent = ''; setTimeout(() => { l.textContent = clean(m); }, 60); };
  window.A11Y = { announceToast, autoContrast, cue, say, announce, clean, buzz, readScreen, describe, getChoices, timeScale, holdClock, timerTick, isPaused: () => paused, togglePause,
    labMounted, labUnmounted, describeLab, hearLab, Son, listenChanged, handleSpeech, tryCommand: s => tryCommand(norm(s)), courseLang, startRec, stopRec, focusBest, offerListen };
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
})();
