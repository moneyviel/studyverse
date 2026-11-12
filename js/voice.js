/* ================= 🔊 Natural voice (js/voice.js) =================
   Speaks like a person: text is split into sentences and phrases, each is spoken separately with short,
   human-like pauses (longer after a full stop or a question, shorter after a comma), questions rise a little,
   and the best voice on the phone is used (Google / natural voices first — see bestVoice() in js/app.js).
   Note: the voice itself comes from the phone or browser; newer phones have the most natural voices.
   Adds a small 🔊 button to every question, option and message in Mind Gym, the brain/heart games, puzzles and
   Arcade. Tapping 🔊 on a question reads the question and then each option (“Option 1 … Option 2 …”).
   window.Voice = { say(text), stop() } — window.speak() also uses it. */
(function () {
  'use strict';
  const D = document, SS = () => ('speechSynthesis' in window ? window.speechSynthesis : null);
  let run = 0, timer = 0;
  const clean = t => String(t || '').replace(/🔊/g, '').replace(/\s+/g, ' ').trim();
  function chunks(text) {
    const out = [];
    // sentences first, then phrases at commas, semicolons, colons and dashes (only when long enough to need a breath)
    String(text).split(/(?<=[.!?।…])\s+|\n+/).forEach(sent => {
      sent = sent.trim(); if (!sent) return;
      const end = /\?\s*$/.test(sent) ? 'q' : /[.!।…]\s*$/.test(sent) ? 's' : 's';
      const parts = sent.length > 70 ? sent.split(/(?<=[,;:])\s+|\s+[—–]\s+/) : [sent];
      parts.forEach((p, i) => { p = p.trim(); if (p) out.push({ t: p, gap: i < parts.length - 1 ? 230 : end === 'q' ? 560 : 430, q: end === 'q' && i === parts.length - 1 }); });
    });
    return out;
  }
  function say(text, opts) {
    const s = SS(); text = clean(text); if (!s || !text) return;
    stop(); const my = ++run;
    const hi = /[ऀ-ॿ]/.test(text);
    let v = null; try { v = window.bestVoice ? window.bestVoice(hi) : null; } catch (e) {}
    let spoken = text; try { if (window.speechText) spoken = window.speechText(text, hi); } catch (e) {}
    const list = chunks(spoken); let i = 0;
    let baseRate = 0.92; try { if (typeof VOICE !== 'undefined' && VOICE.rate) baseRate = VOICE.rate; } catch (e) {}
    const next = () => {
      if (my !== run || i >= list.length) { if (my === run && opts && opts.done) opts.done(); return; }
      const c = list[i++], u = new SpeechSynthesisUtterance(c.t);
      u.lang = v ? v.lang : (hi ? 'hi-IN' : 'en-IN'); if (v) u.voice = v;
      u.rate = baseRate * (0.97 + Math.random() * 0.06);          // tiny natural variation
      u.pitch = c.q ? 1.12 : 1.03; u.volume = 1;
      let moved = false; const go = () => { if (moved) return; moved = true; timer = setTimeout(next, c.gap); };
      u.onend = go; u.onerror = go;
      // safety: some phones never fire onend
      setTimeout(() => { if (!moved && my === run && !s.speaking) go(); }, 400 + c.t.length * 120);
      s.speak(u);
    };
    next();
  }
  function stop() { run++; clearTimeout(timer); try { const s = SS(); if (s) s.cancel(); } catch (e) {} D.querySelectorAll('.vx.on').forEach(x => x.classList.remove('on')); }
  window.Voice = { say, stop };
  window.speak = t => say(t);

  /* ---------- 🔊 buttons everywhere in games ---------- */
  const Q = '.fm-sheet .fm-qt, .fm-talk .pl-q, #s-mind .mg-q, #s-mind .pl-q, #s-mind .hp-sit, #s-mind .hp-event, #s-mind .sx-q, #s-mind .sx-card-t, .pz-cl, .pz-ctx, .arc-p, .arc-lq';
  const O = '.fm-sheet button.fm-o, #s-mind .mg-o:not(.pic), #s-mind .hp-opt, #s-mind .hp-rep, #s-mind .hp-tile, #s-mind .sx-opt, #s-mind .sx-chip';
  const M = '.fm-sheet .fm-fb > p, .fm-sheet .fm-hero p, .fm-sheet .fm-tipc p, #s-mind .hp-b:not(.me):not(.typing), #s-mind .mg-fb > p:not(.mg-v), #s-mind .pl-fb > p:not(.mg-v), #s-mind .hp-res, #s-mind .pl-hero p, #s-mind .mg-out, #s-mind .sx-why, .arc-exp, .arc-hint';
  const btn = (kind) => `<span class="vx vx-${kind}" role="button" tabindex="0" aria-label="Listen">🔊</span>`;
  function decorate() {
    D.querySelectorAll(`${Q}, ${O}, ${M}`).forEach(el => {
      if (el.querySelector(':scope > .vx') || el.closest('.vx') || !clean(el.textContent)) return;
      const kind = el.matches(Q) ? 'q' : el.matches(O) ? 'o' : 'm';
      el.insertAdjacentHTML('beforeend', btn(kind));
    });
  }
  const textOf = el => { const c = el.cloneNode(true); c.querySelectorAll('.vx, .hp-tear, svg').forEach(x => x.remove()); return clean(c.textContent); };
  function readFor(b) {
    const host = b.parentElement; if (!host) return '';
    let t = textOf(host);
    if (b.classList.contains('vx-q')) {
      const scope = host.closest('.card, .pl-stage, .hp-scene, .pz-root, .arc-game') || D;
      const opts = [...scope.querySelectorAll(O)].filter(o => !o.disabled && o.offsetParent !== null);
      if (opts.length) t += '. ' + opts.map((o, i) => `Option ${i + 1}: ${textOf(o)}.`).join(' ');
    }
    return t;
  }
  function activate(e) {
    const b = e.target.closest && e.target.closest('.vx'); if (!b) return;
    e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation();
    if (b.classList.contains('on')) { stop(); return; }
    stop(); b.classList.add('on');
    say(readFor(b), { done: () => b.classList.remove('on') });
  }
  D.addEventListener('click', activate, true);
  D.addEventListener('pointerdown', e => { if (e.target.closest && e.target.closest('.vx')) { e.stopPropagation(); } }, true);
  D.addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && e.target.classList && e.target.classList.contains('vx')) activate(e); }, true);
  // stop talking when the student moves on
  D.addEventListener('click', e => { if (e.target.closest && e.target.closest('#plNext, #mgNext, .back, nav button, .fm-btn, .fm-back')) stop(); }, true);

  let t = 0; new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; try { decorate(); } catch (e) {} }); }).observe(D.documentElement, { childList: true, subtree: true });
  D.head.insertAdjacentHTML('beforeend', `<style id="vxCss">
    .vx{display:inline-grid;place-items:center;width:26px;height:26px;margin-left:6px;border-radius:50%;background:rgba(109,74,255,.12);font-size:13px;cursor:pointer;vertical-align:middle;flex:none;line-height:1;user-select:none;-webkit-user-select:none}
    .vx:hover{background:rgba(109,74,255,.25)}.vx.on{background:#6d4aff;animation:vxPulse 1s infinite}.vx:focus-visible{outline:3px solid #2b6cff}
    .vx-o{width:22px;height:22px;font-size:11px;margin-left:auto;padding-left:0}.hp-b .vx{width:20px;height:20px;font-size:10px}
    @keyframes vxPulse{50%{box-shadow:0 0 0 6px rgba(109,74,255,.2)}}
  </style>`);
})();
