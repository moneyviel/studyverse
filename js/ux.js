/* ================= Comfort & accessibility =================
   1. Text size: 5 levels (Comfort default), applied with CSS zoom so every layout scales together
      and the app width is recalculated, so nothing spills off the screen.
   2. Read-aloud everywhere: labs, games, cards; a 🔊 is added wherever there is instruction text.
   3. Listen mode (for blind and low-vision students, and young readers): every screen is read aloud
      automatically, options are numbered, and answers can be given by voice ("option 2", "B",
      or the answer itself), by keys 1–4, or by tapping. Vibration and sounds confirm each action. */
(function () {
  const SIZES = [['S', .95, 'Small'], ['M', 1.08, 'Comfort'], ['L', 1.2, 'Large'], ['XL', 1.34, 'Extra large'], ['XXL', 1.5, 'Huge']];
  const UX = Object.assign({ size: 1, listen: false, voiceAns: true }, (() => { try { return JSON.parse(localStorage.getItem('sv_ux') || '{}'); } catch (e) { return {}; } })());
  const saveUX = () => { try { localStorage.setItem('sv_ux', JSON.stringify(UX)); } catch (e) {} };
  function applySize() { document.documentElement.style.setProperty('--z', SIZES[UX.size][1]); document.documentElement.style.setProperty('--zn', Math.min(SIZES[UX.size][1], 1.12)); document.documentElement.style.setProperty('--znav', Math.min(SIZES[UX.size][1], 1.12) / SIZES[UX.size][1]); document.documentElement.dataset.ts = SIZES[UX.size][0]; }
  applySize();

  /* ---------- Settings sheet ---------- */
  function settings() {
    let s = document.getElementById('uxSheet');
    if (!s) {
      document.body.insertAdjacentHTML('beforeend', `<div class="sheet" id="uxSheet" role="dialog" aria-label="Reading and accessibility settings"><div class="sheet-in"><div class="sheet-grab"></div>
        <h2>Aa Reading comfort</h2><p class="sub">Make the app easy to read and listen to.</p>
        <h3>Text size</h3><div class="ux-sizes" role="radiogroup" aria-label="Text size">${SIZES.map(([k, z, n], i) => `<button role="radio" data-i="${i}" aria-label="${n}"><span style="font-size:${Math.round(13 * z)}px">Aa</span><small>${n}</small></button>`).join('')}</div>
        <div class="ux-prev">The quick brown fox jumps over the lazy dog. 123 + 456 = 579.</div>
        <h3 style="margin-top:14px">Listening</h3>
        <label class="ux-row"><span><b>🎧 Listen mode</b><small>Reads every screen and question aloud, with numbered options. Answer by voice, keys 1–4 or tap. For blind and low-vision students and young readers.</small></span><input type="checkbox" id="uxListen"></label>
        <label class="ux-row"><span><b>🎤 Answer by voice</b><small>In Listen mode, say "option 2", "B" or the answer.</small></span><input type="checkbox" id="uxVoice"></label>
        <button class="btn" id="uxDone" style="margin-top:12px">Done</button></div></div>`);
      s = document.getElementById('uxSheet');
      s.querySelectorAll('.ux-sizes button').forEach(b => b.onclick = () => { UX.size = +b.dataset.i; saveUX(); applySize(); paint(); sfx('tap'); });
      s.querySelector('#uxListen').onchange = e => { UX.listen = e.target.checked; saveUX(); toast(UX.listen ? '🎧 Listen mode on' : 'Listen mode off'); if (UX.listen) { speak('Listen mode is on. I will read every screen for you. Press 1 to 4 or say an option to answer.'); } };
      s.querySelector('#uxVoice').onchange = e => { UX.voiceAns = e.target.checked; saveUX(); };
      s.querySelector('#uxDone').onclick = () => s.classList.remove('show');
      s.addEventListener('click', e => { if (e.target === s) s.classList.remove('show'); });
    }
    const paint = () => { s.querySelectorAll('.ux-sizes button').forEach((b, i) => { b.classList.toggle('on', i === UX.size); b.setAttribute('aria-checked', i === UX.size); }); s.querySelector('#uxListen').checked = !!UX.listen; s.querySelector('#uxVoice').checked = !!UX.voiceAns; };
    paint(); s.classList.add('show');
  }
  function addHeaderButton() {
    const st = document.querySelector('header .stats'); if (!st || document.getElementById('uxBtn')) return;
    st.insertAdjacentHTML('afterbegin', '<button class="pill uxbtn" id="uxBtn" aria-label="Text size and listening settings">Aa</button>');
    document.getElementById('uxBtn').onclick = settings;
  }

  /* ---------- 🔊 on labs and game instructions ---------- */
  function addSpeakers(root) {
    root.querySelectorAll('.lab-box').forEach(box => {
      if (box.querySelector(':scope > .lab-spk')) return;
      box.insertAdjacentHTML('afterbegin', '<button class="spk lab-spk" data-ra=".lab-box" aria-label="Read this activity aloud">🔊</button>');
    });
    root.querySelectorAll('.game h3, .gtitle, .rv-top h3').forEach(h => { if (!h.querySelector('.spk')) h.insertAdjacentHTML('beforeend', ' <button class="spk" data-ra=".card" aria-label="Read aloud">🔊</button>'); });
  }

  /* ---------- Listen mode ---------- */
  let lastRead = '';
  function readScreen() {
    if (!UX.listen) return;
    const scr = document.querySelector('.screen.active'); if (!scr) return;
    const q = scr.querySelector('.qtext');
    const opts = [...scr.querySelectorAll('.opt:not([disabled])')];
    let text;
    if (q && opts.length) {
      opts.forEach((o, i) => { o.setAttribute('aria-label', `Option ${i + 1}: ${o.textContent.trim()}`); if (!o.querySelector('.optn')) o.insertAdjacentHTML('afterbegin', `<span class="optn" aria-hidden="true">${i + 1}</span>`); });
      text = q.textContent.replace('🔊', '').trim() + '. ' + opts.map((o, i) => `Option ${i + 1}: ${o.textContent.replace(/^\d/, '').trim()}`).join('. ') + '. Say or press the option number.';
    } else {
      const h = scr.querySelector('h2, h1'); const p = scr.querySelector('.bubble, p.sub, .rv-sum');
      text = [h && h.textContent, p && p.textContent].filter(Boolean).join('. ').replace(/🔊/g, '');
    }
    if (!text || text === lastRead) return; lastRead = text;
    try { ReadAlong.stop(); } catch (e) {} speak(text);
    if (q && opts.length && UX.voiceAns) listenAnswer(opts);
  }
  let rec = null;
  function listenAnswer(opts) {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition; if (!SR) return;
    try { if (rec) rec.abort(); } catch (e) {}
    const start = () => { if (!UX.listen || speechSynthesis.speaking) return setTimeout(start, 400);
      rec = new SR(); rec.lang = /[ऀ-ॿ]/.test(opts.map(o => o.textContent).join('')) ? 'hi-IN' : 'en-IN';
      rec.onresult = e => { const said = e.results[0][0].transcript.toLowerCase().trim(); pickBySpeech(said, opts); };
      rec.onerror = () => {}; try { rec.start(); } catch (e) {} };
    setTimeout(start, 600);
  }
  const WORDN = { one: 1, first: 1, two: 2, second: 2, to: 2, too: 2, three: 3, third: 3, four: 4, for: 4, fourth: 4, a: 1, b: 2, c: 3, d: 4, 'एक': 1, 'दो': 2, 'तीन': 3, 'चार': 4 };
  function pickBySpeech(said, opts) {
    let n = null; const m = said.match(/\b([1-4])\b/); if (m) n = +m[1];
    if (!n) for (const w of said.split(/\s+/)) if (WORDN[w] && /option|number|answer|^.$|एक|दो|तीन|चार|first|second|third|fourth/.test(said)) { n = WORDN[w]; break; }
    if (!n) { const norm = s => s.toLowerCase().replace(/[^a-z0-9ऀ-ॿ ]/g, '').trim(); const hit = opts.findIndex(o => norm(o.textContent.replace(/^\d/, '')) === norm(said)); if (hit >= 0) n = hit + 1; }
    if (n && opts[n - 1]) { if (navigator.vibrate) navigator.vibrate(30); opts[n - 1].click(); }
    else { speak("Sorry, I didn't catch that. Say option one, two, three or four."); listenAnswer(opts); }
  }
  document.addEventListener('keydown', e => {
    if (/input|textarea/i.test(document.activeElement?.tagName || '')) return;
    const scr = document.querySelector('.screen.active'); if (!scr) return;
    if (/^[1-4]$/.test(e.key)) { const opts = [...scr.querySelectorAll('.opt:not([disabled])')]; const o = opts[+e.key - 1]; if (o) { o.click(); e.preventDefault(); } }
    else if (e.key === 'Enter') { const nx = scr.querySelector('#nx, #tNext, .btn.next'); if (nx) { nx.click(); e.preventDefault(); } }
    else if (e.key.toLowerCase() === 'r' && !e.ctrlKey) { lastRead = ''; readScreen(); }
  });

  /* screen changes: re-scan for speakers and read in Listen mode */
  let tm = null;
  const mo = new MutationObserver(() => { clearTimeout(tm); tm = setTimeout(() => { addHeaderButton(); addSpeakers(document); readScreen(); }, 350); });
  const boot = () => { addHeaderButton(); mo.observe(document.querySelector('main') || document.body, { childList: true, subtree: true }); document.body.insertAdjacentHTML('beforeend', '<div id="srLive" class="sr-only" aria-live="polite"></div>'); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  /* screen-reader announcements for toasts */
  const _toast = window.toast; if (_toast) window.toast = function (m) { _toast(m); const l = document.getElementById('srLive'); if (l) l.textContent = m; if (UX.listen) speak(String(m).replace(/[^\p{L}\p{N}\s.,!?%₹:'-]/gu, '')); };
  window.UX = { settings, state: UX };
})();
