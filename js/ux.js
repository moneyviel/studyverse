/* ================= Comfort & accessibility settings =================
   1. Text size: a smooth slider from 90% to 150% (108% "Comfort" default), applied with CSS zoom so every layout scales together
      and the app width is recalculated, so nothing spills off the screen.
   2. Read-aloud everywhere: labs, games, cards; a 🔊 is added wherever there is instruction text.
   3. Listen mode (for blind and low-vision students, and young readers): every screen is read aloud
      automatically, choices are numbered, and answers and commands can be given by voice, by number
      keys or by tapping. The reading, voice and keyboard engine lives in js/a11y.js.
   4. High contrast, reduce motion (both follow the phone's own setting until changed here),
      vibration, and timers (normal / extra time / no timer) for timed games. */
(function () {
  const SIZES = [['S', .95, 'Small'], ['M', 1.08, 'Comfort'], ['L', 1.2, 'Large'], ['XL', 1.34, 'Extra large'], ['XXL', 1.5, 'Huge']];
  const TIMERS = [['normal', 'Normal'], ['extra', 'Extra time'], ['off', 'No timer']];
  /* hc / rm / timer: null = follow the phone (or, for timers, "no timer" while Listen mode is on) */
  const UX = Object.assign({ size: 1, listen: false, voiceAns: true, hc: null, rm: null, timer: null, haptics: true, asked: false }, (() => { try { return JSON.parse(localStorage.getItem('sv_ux') || '{}'); } catch (e) { return {}; } })());
  const saveUX = () => { try { localStorage.setItem('sv_ux', JSON.stringify(UX)); } catch (e) {} };
  /* Text size is a continuous zoom (0.9–1.5) set with a slider. UX.z is the saved value; UX.size (the old
     5-step index) is kept in step for older saved settings. data-ts keeps the S…XXL bands for CSS rules. */
  const Z_MIN = .9, Z_MAX = 1.5, Z_DEF = 1.08;
  const clampZ = z => Math.min(Z_MAX, Math.max(Z_MIN, Math.round((+z || Z_DEF) * 100) / 100));
  const bandOf = z => z < 1.015 ? 0 : z < 1.14 ? 1 : z < 1.27 ? 2 : z < 1.42 ? 3 : 4;
  if (typeof UX.z !== 'number') UX.z = (SIZES[UX.size] || SIZES[1])[1];
  UX.z = clampZ(UX.z);
  /* live = true while the slider is being dragged: the app behind updates, the settings sheet keeps its own zoom (--zux) so the slider does not move under the finger */
  function applySize(live) {
    const z = clampZ(UX.z), zn = Math.min(z, 1.12), r = document.documentElement, i = bandOf(z);
    r.style.setProperty('--z', z); r.style.setProperty('--zn', zn); r.style.setProperty('--znav', zn / z);
    if (!live) r.style.setProperty('--zux', z);
    r.dataset.ts = SIZES[i][0]; UX.size = i;
  }
  const mq = q => { try { return window.matchMedia(q); } catch (e) { return { matches: false, addEventListener() {} }; } };
  const MQ_HC = mq('(prefers-contrast: more)'), MQ_RM = mq('(prefers-reduced-motion: reduce)');
  const hcOn = () => UX.hc == null ? !!MQ_HC.matches : !!UX.hc;
  const rmOn = () => UX.rm == null ? !!MQ_RM.matches : !!UX.rm;
  const timerMode = () => UX.timer || (UX.listen ? 'off' : 'normal');
  function applyPrefs() {
    const h = document.documentElement.classList;
    h.toggle('sv-hc', hcOn()); h.toggle('sv-rm', rmOn()); h.toggle('sv-listen', !!UX.listen);
  }
  applySize(); applyPrefs();
  [MQ_HC, MQ_RM].forEach(m => { try { m.addEventListener('change', applyPrefs); } catch (e) {} });

  /* ---------- Settings sheet ---------- */
  function settings() {
    let s = document.getElementById('uxSheet');
    if (!s) {
      document.body.insertAdjacentHTML('beforeend', `<div class="sheet" id="uxSheet" role="dialog" aria-modal="true" aria-labelledby="uxTitle"><div class="sheet-in ux-in"><div class="sheet-grab"></div>
        <h2 id="uxTitle"><span aria-hidden="true">Aa</span> Reading comfort</h2><p class="sub">Make the app easy to read and listen to.</p>
        <h3 id="uxTsH">Text size</h3>
        <div class="ux-ts"><button class="ux-tsb" id="uxTsDn" aria-label="Smaller text"><span aria-hidden="true">A−</span></button>
          <input type="range" id="uxTs" min="${Z_MIN}" max="${Z_MAX}" step="0.01" aria-labelledby="uxTsH">
          <button class="ux-tsb" id="uxTsUp" aria-label="Bigger text"><span aria-hidden="true">A+</span></button></div>
        <div class="ux-tsrow"><b id="uxTsV" aria-hidden="true"></b><button class="ux-tsreset" id="uxTsReset">Reset</button></div>
        <div class="ux-prev" id="uxPrev">The quick brown fox jumps over the lazy dog. 123 + 456 = 579.</div>
        <h3 style="margin-top:14px">Listening</h3>
        <label class="ux-row"><span><b><span aria-hidden="true">🎧</span> Listen mode</b><small>Reads every screen and question aloud, with numbered choices. Answer by voice, keys 1–9 or tap. Hold the big 🎤 button and say "help" to hear what you can say. For blind and low-vision students and young readers.</small></span><input type="checkbox" id="uxListen"></label>
        <label class="ux-row"><span><b><span aria-hidden="true">🎤</span> Answer by voice</b><small>In Listen mode, the microphone opens after each question. Say "option 2", "B" or the answer.</small></span><input type="checkbox" id="uxVoice"></label>
        <h3 style="margin-top:14px">Seeing</h3>
        <label class="ux-row"><span><b><span aria-hidden="true">🌗</span> High contrast</b><small>Stronger colours, thick outlines and ✓ / ✗ marks on answers.</small></span><input type="checkbox" id="uxHc"></label>
        <label class="ux-row"><span><b><span aria-hidden="true">🐢</span> Reduce motion</b><small>Stops bouncing, sliding and flashing animations.</small></span><input type="checkbox" id="uxRm"></label>
        <label class="ux-row"><span><b><span aria-hidden="true">📳</span> Vibration</b><small>Two short buzzes for right, one long buzz for wrong, a tick for a new screen.</small></span><input type="checkbox" id="uxHap"></label>
        <h3 style="margin-top:14px" id="uxTmH">Timed games</h3><p class="sub" id="uxTmD">In Listen mode timers are off unless you pick one here. The clock also waits while the app is talking.</p>
        <div class="ux-sizes ux-timer" role="radiogroup" aria-labelledby="uxTmH" aria-describedby="uxTmD">${TIMERS.map(([k, n]) => `<button role="radio" data-t="${k}"><small>${n}</small></button>`).join('')}</div>
        <button class="btn" id="uxDone" style="margin-top:14px">Done</button></div></div>`);
      s = document.getElementById('uxSheet');
      const ts = s.querySelector('#uxTs');
      /* input: live preview while dragging (sheet zoom held still); change / buttons: commit, save and rescale the sheet too */
      ts.addEventListener('input', () => { UX.z = clampZ(ts.value); applySize(true); paintSize(); });
      ts.addEventListener('change', () => { UX.z = clampZ(ts.value); saveUX(); applySize(); paintSize(); });
      const nudge = d => { UX.z = clampZ(Math.round((UX.z + d) * 20) / 20); saveUX(); applySize(); paintSize(); try { sfx('tap'); } catch (e) {} };
      s.querySelector('#uxTsDn').onclick = () => nudge(-.05);
      s.querySelector('#uxTsUp').onclick = () => nudge(.05);
      s.querySelector('#uxTsReset').onclick = () => { UX.z = Z_DEF; saveUX(); applySize(); paintSize(); try { sfx('tap'); } catch (e) {} toast(`Text size reset to ${Math.round(Z_DEF * 100)}%`); };
      s.querySelectorAll('.ux-timer button').forEach(b => b.onclick = () => { UX.timer = b.dataset.t; saveUX(); paint(); sfx('tap'); toast(`Timers: ${b.textContent}`); });
      s.querySelector('#uxListen').onchange = e => setListen(e.target.checked);
      s.querySelector('#uxVoice').onchange = e => { UX.voiceAns = e.target.checked; saveUX(); };
      s.querySelector('#uxHc').onchange = e => { UX.hc = e.target.checked; saveUX(); applyPrefs(); };
      s.querySelector('#uxRm').onchange = e => { UX.rm = e.target.checked; saveUX(); applyPrefs(); };
      s.querySelector('#uxHap').onchange = e => { UX.haptics = e.target.checked; saveUX(); if (UX.haptics && navigator.vibrate) navigator.vibrate([30, 60, 30]); };
      s.querySelector('#uxDone').onclick = () => s.classList.remove('show');
      s.addEventListener('click', e => { if (e.target === s) s.classList.remove('show'); });
    }
    var paintSize = () => { const z = clampZ(UX.z), pc = Math.round(z * 100), n = SIZES[bandOf(z)][2], ts = s.querySelector('#uxTs');
      if (+ts.value !== z) ts.value = z;
      ts.setAttribute('aria-valuetext', `Text size ${pc}%, ${n}`); ts.style.setProperty('--pct', ((z - Z_MIN) / (Z_MAX - Z_MIN) * 100).toFixed(1) + '%');
      s.querySelector('#uxTsV').textContent = `${pc}% · ${n}`;
      s.querySelector('#uxTsDn').disabled = z <= Z_MIN; s.querySelector('#uxTsUp').disabled = z >= Z_MAX;
      const zux = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--zux')) || z;
      s.querySelector('#uxPrev').style.fontSize = (15 * z / zux).toFixed(2) + 'px'; };
    var paint = () => { paintSize();
      const tm = timerMode(); s.querySelectorAll('.ux-timer button').forEach(b => { const on = b.dataset.t === tm; b.classList.toggle('on', on); b.setAttribute('aria-checked', String(on)); b.tabIndex = on ? 0 : -1; });
      s.querySelector('#uxListen').checked = !!UX.listen; s.querySelector('#uxVoice').checked = !!UX.voiceAns;
      s.querySelector('#uxHc').checked = hcOn(); s.querySelector('#uxRm').checked = rmOn(); s.querySelector('#uxHap').checked = UX.haptics !== false; };
    paint(); s.classList.add('show');
  }
  function setListen(on) {
    UX.listen = !!on; UX.asked = true; saveUX(); applyPrefs();
    const cb = document.getElementById('uxListen'); if (cb) cb.checked = UX.listen;
    if (window.A11Y) A11Y.listenChanged(UX.listen);
    else { toast(UX.listen ? '🎧 Listen mode on' : 'Listen mode off'); if (UX.listen) speak('Listen mode is on.'); }
  }
  function addHeaderButton() {
    const st = document.querySelector('header .stats'); if (!st || document.getElementById('uxBtn')) return;
    st.insertAdjacentHTML('afterbegin', '<button class="pill uxbtn" id="uxBtn" aria-label="Text size, listening and accessibility settings">Aa</button>');
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

  /* screen changes: re-scan for speakers (Listen-mode reading itself is done by js/a11y.js) */
  let tm = null;
  const mo = new MutationObserver(() => { clearTimeout(tm); tm = setTimeout(() => { addHeaderButton(); addSpeakers(document); }, 300); });
  const boot = () => { addHeaderButton(); mo.observe(document.querySelector('main') || document.body, { childList: true, subtree: true });
    if (!document.getElementById('srLive')) document.body.insertAdjacentHTML('beforeend', '<div id="srLive" class="sr-only" role="status" aria-live="polite"></div><div id="srAlert" class="sr-only" role="alert" aria-live="assertive"></div>'); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  /* screen-reader announcements for toasts (and spoken in Listen mode, after whatever is being read) */
  const _toast = window.toast; if (_toast) window.toast = function (m) { _toast(m); if (window.A11Y) { A11Y.announceToast(String(m)); if (UX.listen) A11Y.say(A11Y.clean(String(m)), { queue: true }); return; }
    const l = document.getElementById('srLive'); if (l) l.textContent = m; if (UX.listen) speak(String(m).replace(/[^\p{L}\p{N}\s.,!?%₹:'-]/gu, '')); };
  window.UX = { settings, state: UX, save: saveUX, apply: applyPrefs, setListen, timerMode, hcOn, rmOn, setSize: z => { UX.z = clampZ(z); saveUX(); applySize(); } };
})();
