/* StudyVerse Concept Lab: clockset — "Clock & calendar"
 * The child drags the hour / minute hands of an analogue clock (geared like a real clock) and sees the
 * digital time, am/pm, 24-hour time, words and elapsed time change live. Calendar mode counts days.
 *
 * PARAMS (all optional)
 *  name        type            meaning                                                               default
 *  mode        string          'set'      : set the clock to `target`                                  'set'
 *                              'ampm'     : like set, but am/pm matters; shows 12-hour and 24-hour time
 *                              'elapsed'  : start at `start`, move the hands forward to `end`
 *                                           (or by `duration`) and read the time passed
 *                              'calendar' : tap dates on a month calendar to count days
 *  target      string          time to set, "3:45", "7:30 pm" or "19:30"                              "3:45" (ampm: "6:30 pm")
 *  start       string          time the clock starts at                                               "12:00" (elapsed: "8:30")
 *  end         string          elapsed mode: finishing time                                           "10:15"
 *  duration    string|number   elapsed mode instead of end: "2:15" (h:mm) or minutes, e.g. 135          none
 *  snap        number          minutes per step when dragging (1, 5, 15, 30, 60)                       5
 *  digital     boolean         show the digital readout (false = read the hands yourself)             true
 *  showWords   boolean         show the time in words ("quarter to four")                              true
 *  show24      boolean         show 24-hour time                                                       ampm/elapsed: true, set: false
 *  year        number          calendar: year                                                          2026
 *  month       number          calendar: month 1-12                                                    3
 *  from        string|number   calendar: start date "2026-03-05" or a day of `month`                   5
 *  days        number          calendar: answer is this many days after `from` (negative = before)     10
 *  to          string|number   calendar: answer date instead of `days`                                none
 *  newChallenge boolean        show the "New" button                                                   true
 *  challenge   string          challenge text (any language); default generated                        auto
 */
(function () {
  const T = 'clockset';
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const MON = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const WK = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const NUMW = ['twelve', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve'];
  const MINW = n => { const o = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'quarter', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']; return n <= 20 ? o[n] : 'twenty-' + o[n - 20]; };
  const pad = n => String(n).padStart(2, '0');
  // parse "3:45", "7:30 pm", "19:30", "12 am" → minutes since midnight (or since 0 for 12h when no am/pm: flag)
  function parseTime(v) {
    if (v == null || v === '') return null;
    const s = String(v).trim().toLowerCase().replace(/\./g, ':');
    const m = s.match(/^(\d{1,2})(?::(\d{1,2}))?\s*(am|pm|a\s*m|p\s*m)?$/);
    if (!m) return null;
    let h = +m[1], mi = +(m[2] || 0); const ap = m[3] ? m[3].replace(/\s/g, '') : '';
    if (mi > 59 || h > 24) return null;
    if (ap) { if (h < 1 || h > 12) return null; h = h % 12 + (ap === 'pm' ? 12 : 0); }
    return { min: (h % 24) * 60 + mi, ampm: !!ap || h >= 13 || h === 0 };
  }
  const t12 = m => { m = ((m % 1440) + 1440) % 1440; const h = Math.floor(m / 60), mi = m % 60; return `${h % 12 === 0 ? 12 : h % 12}:${pad(mi)}`; };
  const ap = m => (((m % 1440) + 1440) % 1440) < 720 ? 'am' : 'pm';
  const t24 = m => { m = ((m % 1440) + 1440) % 1440; return `${pad(Math.floor(m / 60))}:${pad(m % 60)}`; };
  function words(m) {
    m = ((m % 720) + 720) % 720; const h = Math.floor(m / 60), mi = m % 60;
    if (mi === 0) return `${NUMW[h]} o'clock`;
    if (mi === 30) return `half past ${NUMW[h]}`;
    if (mi < 30) return `${MINW(mi)}${mi === 15 ? '' : mi === 1 ? ' minute' : ' minutes'} past ${NUMW[h]}`;
    const r = 60 - mi; return `${MINW(r)}${r === 15 ? '' : r === 1 ? ' minute' : ' minutes'} to ${NUMW[(h + 1) % 12]}`;
  }
  const dur = d => { const h = Math.floor(d / 60), m = d % 60; return (h ? `${h} h` : '') + (h && m ? ' ' : '') + (m || !h ? `${m} min` : ''); };

  const CSS = `
  .lb-clockset-w{user-select:none;-webkit-user-select:none}
  .lb-clockset-ch{font-weight:800;font-size:14.5px;line-height:1.3;color:#1b1f3a;background:#f4f0ff;border-radius:14px;padding:9px 12px;margin-bottom:8px}
  .lb-clockset-top{display:flex;align-items:center;gap:10px}
  .lb-clockset-face{flex:1.25;min-width:0;max-width:250px;margin:0 auto}
  .lb-clockset-svg{display:block;width:100%;height:auto;touch-action:none;cursor:grab}
  .lb-clockset-side{flex:1;min-width:0;display:flex;flex-direction:column;gap:6px;align-items:stretch}
  .lb-clockset-dig{background:#1b1f3a;color:#7dffd4;border-radius:14px;text-align:center;font-weight:800;font-size:30px;letter-spacing:1px;padding:6px 4px;font-variant-numeric:tabular-nums;line-height:1.1}
  .lb-clockset-dig small{font-size:15px;color:#ffc93c;margin-left:3px}
  .lb-clockset-tag{background:#f7f8fe;border-radius:12px;padding:5px 8px;font-weight:800;font-size:13px;text-align:center;color:#1b1f3a;line-height:1.25}
  .lb-clockset-tag .k{display:block;font-size:10.5px;color:#6b7090;text-transform:uppercase;letter-spacing:.4px}
  .lb-clockset-words{text-align:center;font-weight:800;font-size:15px;color:#7c4ddb;margin:6px 0 2px;min-height:20px}
  .lb-clockset-tl{margin:6px 0 2px}
  .lb-clockset-tl svg{display:block;width:100%;height:auto}
  .lb-clockset-hint{text-align:center;font-weight:800;font-size:13.5px;color:#7c4ddb;min-height:20px;margin:4px 0 6px}
  .lb-clockset-row{display:flex;gap:6px;justify-content:center;flex-wrap:wrap}
  .lb-clockset-s{height:42px;min-width:44px;border:none;border-radius:14px;font-family:inherit;font-weight:800;font-size:14px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 4px 0 #d3d7ef;padding:0 10px}
  .lb-clockset-s:active{transform:translateY(3px);box-shadow:0 1px 0 #d3d7ef}
  .lb-clockset-s.h{background:#8b5cf6;color:#fff;box-shadow:0 4px 0 #5b33c9}
  .lb-clockset-s.m{background:#3b82f6;color:#fff;box-shadow:0 4px 0 #2563c9}
  .lb-clockset-cal{background:#fbfbff;border-radius:18px;box-shadow:inset 0 0 0 2px #eceefa;padding:8px}
  .lb-clockset-cm{display:flex;align-items:center;justify-content:space-between;font-weight:800;font-size:17px;margin-bottom:6px}
  .lb-clockset-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:3px}
  .lb-clockset-wd{text-align:center;font-weight:800;font-size:11px;color:#6b7090;padding:2px 0}
  .lb-clockset-wd.su{color:#ff6b6b}
  .lb-clockset-day{height:40px;border:none;border-radius:10px;background:#fff;font-family:inherit;font-weight:800;font-size:15px;color:#1b1f3a;cursor:pointer;box-shadow:inset 0 0 0 1.5px #e3e6f6;padding:0;position:relative}
  .lb-clockset-day.su{color:#e04848}
  .lb-clockset-day.rng{background:#e6f0ff;box-shadow:none}
  .lb-clockset-day.from{background:#ffc93c;box-shadow:none;color:#1b1f3a}
  .lb-clockset-day.sel{background:#8b5cf6;color:#fff;box-shadow:none}
  .lb-clockset-day i{position:absolute;right:3px;top:1px;font-style:normal;font-size:9px;color:#3b82f6}
  .lb-clockset-day.sel i{color:#fff}
  `;

  Labs.register(T, {
    title: 'Clock & calendar',
    subjects: ['maths'],
    render(host, p, api) {
      const mode = ['set', 'ampm', 'elapsed', 'calendar'].includes(p.mode) ? p.mode : 'set';
      if (mode === 'calendar') return renderCalendar(host, p, api);
      const snap = [1, 5, 10, 15, 30, 60].includes(+p.snap) ? +p.snap : 5;
      const showDig = p.digital !== false;
      const show24 = p.show24 != null ? !!p.show24 : mode !== 'set';
      const useAP = mode === 'ampm' || mode === 'elapsed';
      const st = parseTime(p.start);
      let start = st ? st.min : (mode === 'elapsed' ? 510 : 720);
      let target, need = 0;
      function setupTarget() {
        if (mode === 'elapsed') {
          const e = parseTime(p.end);
          let d = null;
          if (p.duration != null && p.duration !== '') {
            const m = String(p.duration).match(/^(\d+):(\d{1,2})$/); d = m ? +m[1] * 60 + +m[2] : Math.round(+p.duration);
            if (!isFinite(d) || d <= 0) d = null;
          }
          if (d) { need = d; target = start + d; }
          else { let em = e ? e.min : 615; if (e && !e.ampm && em < start % 1440 && em + 720 > start % 1440) em += 720; need = ((em - start) % 1440 + 1440) % 1440 || 1440; target = start + need; }
        } else {
          const t = parseTime(p.target);
          target = t ? t.min : (mode === 'ampm' ? 1110 : 225);
          if (mode === 'ampm' && t && !t.ampm) target = t.min; // "6:30" without am/pm → morning
        }
      }
      setupTarget();
      // keep target reachable with snap
      const snapT = v => Math.round(v / snap) * snap;
      let snapE = snap; if (target % snap || start % snap) snapE = 1;
      let cur = start, raw = start, customText = p.challenge ? String(p.challenge) : '';

      function defaultText() {
        if (mode === 'set') return `Set the clock to ${t12(target)} (${words(target)})`;
        if (mode === 'ampm') return `Set the clock to ${t12(target)} ${ap(target)}. What is that in 24-hour time?`;
        return p.duration ? `It is ${t12(start)} ${ap(start)}. Move the clock ${dur(need)} later. What time will it be?` : `Start ${t12(start)} ${ap(start)}, end ${t12(target)} ${ap(target)}. Move the hands forward — how much time passes?`;
      }

      host.innerHTML = `<style>${CSS}</style><div class="lb-clockset-w">
        <div class="lb-clockset-ch"></div>
        <div class="lb-clockset-top"><div class="lb-clockset-face"><svg class="lb-clockset-svg" viewBox="0 0 240 240"></svg></div><div class="lb-clockset-side"></div></div>
        <div class="lb-clockset-words"></div>
        <div class="lb-clockset-tl"></div>
        <div class="lb-clockset-hint"></div>
        <div class="lb-clockset-row"></div></div>`;
      const $ = s => host.querySelector(s);
      const svg = $('svg'), side = $('.lb-clockset-side'), wEl = $('.lb-clockset-words'), tlEl = $('.lb-clockset-tl'), hintEl = $('.lb-clockset-hint'), rowEl = $('.lb-clockset-row'), chEl = $('.lb-clockset-ch');
      const hint = t => { hintEl.textContent = t || ''; };
      const C = 120, R = 108;

      // static face
      let face = `<defs><radialGradient id="lbcsg" cx="50%" cy="40%"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#f1f3ff"/></radialGradient></defs>
        <circle cx="${C}" cy="${C}" r="${R + 8}" fill="#8b5cf6"/><circle cx="${C}" cy="${C}" r="${R}" fill="url(#lbcsg)"/>`;
      for (let i = 0; i < 60; i++) {
        const a = i * Math.PI / 30, big = i % 5 === 0;
        const r1 = R - (big ? 11 : 6), r2 = R - 2;
        face += `<line x1="${(C + r1 * Math.sin(a)).toFixed(2)}" y1="${(C - r1 * Math.cos(a)).toFixed(2)}" x2="${(C + r2 * Math.sin(a)).toFixed(2)}" y2="${(C - r2 * Math.cos(a)).toFixed(2)}" stroke="${big ? '#1b1f3a' : '#a9aecb'}" stroke-width="${big ? 2.6 : 1.3}" stroke-linecap="round"/>`;
      }
      for (let h = 1; h <= 12; h++) { const a = h * Math.PI / 6, r = R - 26; face += `<text x="${(C + r * Math.sin(a)).toFixed(2)}" y="${(C - r * Math.cos(a) + 7).toFixed(2)}" text-anchor="middle" font-size="20" font-weight="800" fill="#1b1f3a">${h}</text>`; }
      if (snap <= 5) for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6, r = R + 0; } // (minute numbers omitted for clarity)
      face += `<g class="sky"></g><g class="arc"></g><g class="hands"></g>`;
      svg.innerHTML = face;
      const gHands = svg.querySelector('.hands'), gArc = svg.querySelector('.arc'), gSky = svg.querySelector('.sky');

      function drawHands() {
        const m = ((cur % 720) + 720) % 720;
        const ma = (m % 60) * 6, ha = m / 2;
        const hand = (ang, len, w, col, tail) => `<g transform="rotate(${ang.toFixed(2)} ${C} ${C})"><path d="M${C - w / 2} ${C + tail} L${C - w * .35} ${C - len + w} L${C} ${C - len} L${C + w * .35} ${C - len + w} L${C + w / 2} ${C + tail} Z" fill="${col}" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></g>`;
        gHands.innerHTML = hand(ha, 58, 11, '#8b5cf6', 12) + hand(ma, 88, 7.5, '#3b82f6', 16) + `<circle cx="${C}" cy="${C}" r="7" fill="#1b1f3a"/><circle cx="${C}" cy="${C}" r="2.6" fill="#ffc93c"/>`;
        // am/pm sky badge
        if (useAP) {
          const day = ap(cur) === 'am' ? (((cur % 1440) + 1440) % 1440 >= 360) : (((cur % 1440) + 1440) % 1440 < 1080);
          gSky.innerHTML = day
            ? `<g transform="translate(214,24)"><circle r="9" fill="#ffc93c"/>${[0, 45, 90, 135, 180, 225, 270, 315].map(a => `<line x1="0" y1="-12" x2="0" y2="-15" stroke="#ffb000" stroke-width="2.2" stroke-linecap="round" transform="rotate(${a})"/>`).join('')}</g>`
            : `<g transform="translate(214,24)"><circle r="10" fill="#3b4a8a"/><circle cx="4" cy="-3" r="8.5" fill="#f1f3ff"/><circle cx="-12" cy="-8" r="1.3" fill="#ffc93c"/><circle cx="12" cy="7" r="1.1" fill="#ffc93c"/></g>`;
        }
        // elapsed: shade the minute hand's sweep for the current hour part
        if (mode === 'elapsed' && cur !== start) {
          const d = cur - start;
          if (Math.abs(d) < 60) {
            const a0 = ((start % 60) + 60) % 60 * 6, a1 = a0 + d * 6;
            const s0 = Math.min(a0, a1), s1 = Math.max(a0, a1);
            const pt = a => `${(C + 96 * Math.sin(a * Math.PI / 180)).toFixed(2)} ${(C - 96 * Math.cos(a * Math.PI / 180)).toFixed(2)}`;
            gArc.innerHTML = `<path d="M${C} ${C}L${pt(s0)}A96 96 0 ${s1 - s0 > 180 ? 1 : 0} 1 ${pt(s1)}Z" fill="#2ed3a5" opacity=".25"/>`;
          } else gArc.innerHTML = `<circle cx="${C}" cy="${C}" r="96" fill="#2ed3a5" opacity=".12"/>`;
        } else gArc.innerHTML = '';
      }
      function readout() {
        let s = '';
        if (showDig || won) s += `<div class="lb-clockset-dig">${t12(cur)}${useAP ? `<small>${ap(cur)}</small>` : ''}</div>`;
        else s += `<div class="lb-clockset-dig">--:--</div>`;
        if (show24 && (showDig || won)) s += `<div class="lb-clockset-tag"><span class="k">24-hour</span>${t24(cur)}</div>`;
        if (mode === 'elapsed') {
          const d = cur - start;
          s += `<div class="lb-clockset-tag"><span class="k">Time passed</span>${d < 0 ? '−' : ''}${dur(Math.abs(d))}</div>`;
        } else if (mode === 'set') {
          s += `<div class="lb-clockset-tag"><span style="color:#8b5cf6">Short hand: hours</span><br><span style="color:#3b82f6">Long hand: minutes</span></div>`;
        } else {
          const mm = ((cur % 1440) + 1440) % 1440;
          const part = mm === 0 ? 'midnight' : mm === 720 ? 'noon' : mm < 720 ? (mm < 360 ? 'night (am)' : 'morning') : mm < 960 ? 'afternoon' : mm < 1140 ? 'evening' : 'night';
          s += `<div class="lb-clockset-tag"><span class="k">Part of day</span>${part}</div>`;
        }
        side.innerHTML = s;
        wEl.textContent = p.showWords === false || (!showDig && !won) ? '' : words(cur) + (useAP ? (((cur % 1440) + 1440) % 1440 === 720 ? ' (noon)' : ((cur % 1440) + 1440) % 1440 === 0 ? ' (midnight)' : ` ${ap(cur)}`) : '');
        if (mode === 'elapsed') drawTimeline();
      }
      function drawTimeline() {
        const W = 360, x0 = 22, x1 = 338;
        const span = Math.max(need, cur - start, 60) + 30;
        const X = m => x0 + (m - start) / span * (x1 - x0);
        let s = `<rect x="${x0}" y="22" width="${x1 - x0}" height="10" rx="5" fill="#eef0fb"/>`;
        const curX = X(Math.max(start, cur));
        s += `<rect x="${x0}" y="22" width="${Math.max(0, curX - x0)}" height="10" rx="5" fill="#2ed3a5"/>`;
        // hour marks
        const first = Math.ceil(start / 60) * 60;
        for (let h = first; h <= start + span; h += 60) { const x = X(h); if (x > x1) break; s += `<line x1="${x}" x2="${x}" y1="18" y2="36" stroke="#6b7090" stroke-width="1.5"/><text x="${x}" y="50" text-anchor="middle" font-size="11" font-weight="800" fill="#6b7090">${t12(h)}</text>`; }
        s += `<circle cx="${X(start)}" cy="27" r="7" fill="#ffc93c" stroke="#fff" stroke-width="2"/><text x="${X(start)}" y="12" text-anchor="middle" font-size="11" font-weight="800" fill="#b07d00">start</text>`;
        if (!p.duration) s += `<path d="M${X(target)} 20l-5 -7h10z" fill="#ff6b6b"/><text x="${Math.min(x1 - 8, X(target))}" y="11" text-anchor="middle" font-size="11" font-weight="800" fill="#e04848">end</text>`;
        if (cur > start) s += `<circle cx="${Math.min(x1, curX)}" cy="27" r="7" fill="#3b82f6" stroke="#fff" stroke-width="2"/>`;
        tlEl.innerHTML = `<svg viewBox="0 0 ${W} 66">${s}</svg>`;
      }
      function buildRow() {
        let s = `<button class="lb-clockset-s h" data-d="-60">−1 h</button><button class="lb-clockset-s m" data-d="${-snapE}">−${snapE}m</button><button class="lb-clockset-s m" data-d="${snapE}">+${snapE}m</button><button class="lb-clockset-s h" data-d="60">+1 h</button>`;
        s += `<button class="lb-clockset-s" data-act="reset">↺</button>`;
        if (p.newChallenge !== false) s += `<button class="lb-clockset-s" data-act="new">✨ New</button>`;
        rowEl.innerHTML = s;
      }
      const setText = () => { chEl.textContent = '🎯 Challenge: ' + (customText || defaultText()); };

      // ---------- win ----------
      let won = false;
      function check() {
        if (won) return;
        let ok;
        if (mode === 'set') ok = (((cur - target) % 720) + 720) % 720 === 0;
        else if (mode === 'ampm') ok = (((cur - target) % 1440) + 1440) % 1440 === 0;
        else ok = cur - start === need;
        if (!ok) {
          if (mode === 'ampm' && (((cur - target) % 720) + 720) % 720 === 0) { hint(`The hands are right, but it is ${ap(cur)}! Go round once more.`); api.sfx('hmm'); }
          return;
        }
        won = true; api.sfx('correct'); hint('⭐ Right on time!'); readout();
        if (mode === 'set') api.win(`${t12(target)} — ${words(target)}`);
        else if (mode === 'ampm') api.win(`${t12(target)} ${ap(target)} = ${t24(target)} in 24-hour time`);
        else api.win(`From ${t12(start)} ${ap(start)} to ${t12(cur)} ${ap(cur)} is ${dur(need)}`);
      }
      function setCur(v, quiet) {
        if (mode === 'elapsed') v = Math.max(start - 720, Math.min(start + 1440 * 2, v));
        if (v === cur) return; cur = v; if (!quiet) api.sfx('tap'); drawHands(); readout();
      }

      // ---------- dragging ----------
      let drag = null;
      function angleAt(ev) { const r = svg.getBoundingClientRect(); const x = (ev.clientX - r.left) / r.width * 240 - C, y = (ev.clientY - r.top) / r.height * 240 - C; return { a: (Math.atan2(x, -y) * 180 / Math.PI + 360) % 360, d: Math.hypot(x, y) }; }
      svg.addEventListener('pointerdown', ev => {
        const { a, d } = angleAt(ev); if (d > R + 10) return;
        const m = ((cur % 720) + 720) % 720, ma = (m % 60) * 6, ha = m / 2;
        const diff = (x, y) => { const t = Math.abs(x - y) % 360; return t > 180 ? 360 - t : t; };
        const dm = diff(a, ma), dh = diff(a, ha);
        // prefer the hour hand when the touch is near the centre & close to it
        const which = (dh + (d > 66 ? 25 : 0)) < dm ? 'h' : 'm';
        drag = { which, last: a }; raw = cur;
        try { svg.setPointerCapture(ev.pointerId); } catch (e) { }
        hint(which === 'h' ? 'Moving the hour hand' : 'Moving the minute hand');
        ev.preventDefault();
      });
      svg.addEventListener('pointermove', ev => {
        if (!drag) return;
        const { a } = angleAt(ev);
        let da = a - drag.last; if (da > 180) da -= 360; if (da < -180) da += 360; drag.last = a;
        raw += drag.which === 'm' ? da / 6 : da * 2; // minute hand: 6°/min; hour hand: 0.5°/min
        const st2 = drag.which === 'h' ? Math.max(snapE, 15) : snapE;
        const v = Math.round(raw / st2) * st2;
        setCur(drag.which === 'h' ? v - (v % snapE) : v, true);
      });
      const up = () => { if (!drag) return; drag = null; const v = Math.round(cur / snapE) * snapE; setCur(v, true); raw = cur; hint(''); api.sfx('tap'); check(); };
      svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);

      rowEl.addEventListener('click', e => {
        const b = e.target.closest('button'); if (!b) return;
        if (b.dataset.d) { setCur(cur + +b.dataset.d); raw = cur; hint(''); check(); return; }
        if (b.dataset.act === 'reset') { cur = raw = start; drawHands(); readout(); hint(''); api.sfx('tap'); return; }
        if (b.dataset.act === 'new') {
          const r = (a, b2) => a + Math.floor(Math.random() * (b2 - a + 1));
          const st3 = Math.max(snapE, 5);
          if (mode === 'set') { let t; do { t = r(0, 143) * 5; t = Math.round(t / st3) * st3; } while (t === target); target = t; cur = raw = start; }
          else if (mode === 'ampm') { let t; do { t = Math.round(r(0, 287) * 5 / st3) * st3; } while (t === target); target = t; cur = raw = start; }
          else { start = Math.round(r(72, 216) * 5 / st3) * st3; need = Math.round(r(4, 60) * 5 / st3) * st3; target = start + need; cur = raw = start; }
          customText = ''; snapE = snap; if (target % snap || start % snap) snapE = 1;
          if (won) { won = false; api.resetWin && api.resetWin(); }
          setText(); buildRow(); drawHands(); readout(); hint(''); api.sfx('tap');
        }
      });

      setText(); buildRow(); drawHands(); readout();
      return () => { drag = null; };
    },
    example: { mode: 'set', target: '3:45', start: '12:00', snap: 5 },
    examples: [
      { mode: 'ampm', target: '18:30', start: '6:00', snap: 15, challenge: 'The train leaves at 18:30. Set the clock — is that am or pm? Turn the hands past 12 to switch!' },
      { mode: 'elapsed', start: '8:30', end: '1:15', snap: 5, challenge: 'School starts at 8:30 am and ends at 1:15 pm. Move the hands forward — how long is the school day?' },
      { mode: 'calendar', year: 2026, month: 8, from: 10, days: 12, challenge: 'Raksha Bandhan practice starts on 10 August. The show is 12 days later. Tap the show date!' }
    ]
  });

  // ================= calendar mode =================
  function renderCalendar(host, p, api) {
    const y0 = Math.round(+p.year) || 2026;
    const m0 = Math.min(12, Math.max(1, Math.round(+p.month) || 3)) - 1;
    const D = (y, m, d) => Date.UTC(y, m, d);
    const parseD = v => {
      if (v == null || v === '') return null;
      const s = String(v).trim(); let m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
      if (m) return D(+m[1], +m[2] - 1, +m[3]);
      m = s.match(/^(\d{1,2})$/); if (m) return D(y0, m0, +m[1]);
      return null;
    };
    const DAY = 86400000;
    let from = parseD(p.from) || D(y0, m0, 5);
    let target = parseD(p.to);
    let days = Math.round(+p.days);
    if (target == null) { if (!isFinite(days) || !days) days = 10; target = from + days * DAY; }
    let view = new Date(from); let vy = view.getUTCFullYear(), vm = view.getUTCMonth();
    let sel = null, won = false, customText = p.challenge ? String(p.challenge) : '';
    const fmt = t => { const d = new Date(t); return `${d.getUTCDate()} ${MON[d.getUTCMonth()]}`; };
    const fmtY = t => { const d = new Date(t); return `${d.getUTCDate()} ${MON[d.getUTCMonth()]} ${d.getUTCFullYear()}`; };
    const wk = t => WK[new Date(t).getUTCDay()];
    const defaultText = () => p.to != null && p.to !== '' ? `How many days from ${fmt(from)} to ${fmt(target)}? Tap ${fmt(target)} to count.` : `What date is ${Math.abs(Math.round((target - from) / DAY))} days ${target >= from ? 'after' : 'before'} ${fmt(from)}? Tap it!`;

    host.innerHTML = `<style>${CSS}</style><div class="lb-clockset-w">
      <div class="lb-clockset-ch"></div>
      <div class="lb-clockset-cal"><div class="lb-clockset-cm"><button class="lb-clockset-s" data-nav="-1" aria-label="previous month">◀</button><span></span><button class="lb-clockset-s" data-nav="1" aria-label="next month">▶</button></div><div class="lb-clockset-grid"></div></div>
      <div class="lb-clockset-words"></div>
      <div class="lb-clockset-hint"></div>
      <div class="lb-clockset-row"><button class="lb-clockset-s" data-act="reset">↺ Clear</button>${p.newChallenge !== false ? '<button class="lb-clockset-s" data-act="new">✨ New</button>' : ''}</div></div>`;
    const $ = s => host.querySelector(s);
    const chEl = $('.lb-clockset-ch'), grid = $('.lb-clockset-grid'), title = $('.lb-clockset-cm span'), wEl = $('.lb-clockset-words'), hintEl = $('.lb-clockset-hint');
    const hint = t => { hintEl.textContent = t || ''; };
    const setText = () => { chEl.textContent = '🎯 Challenge: ' + (customText || defaultText()); };
    function draw() {
      title.textContent = `${MON[vm]} ${vy}`;
      let s = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'].map((w, i) => `<div class="lb-clockset-wd${i ? '' : ' su'}">${w}</div>`).join('');
      const first = new Date(D(vy, vm, 1)).getUTCDay(), n = new Date(D(vy, vm + 1, 0)).getUTCDate();
      for (let i = 0; i < first; i++) s += '<div></div>';
      const lo = sel == null ? null : Math.min(from, sel), hi = sel == null ? null : Math.max(from, sel);
      for (let d = 1; d <= n; d++) {
        const t = D(vy, vm, d); const dow = (first + d - 1) % 7;
        let cls = dow === 0 ? ' su' : '';
        if (t === from) cls += ' from'; else if (sel != null && t === sel) cls += ' sel'; else if (lo != null && t > lo && t < hi) cls += ' rng';
        const cnt = sel != null && t > lo && t <= hi ? Math.round((t - lo) / DAY) : '';
        s += `<button class="lb-clockset-day${cls}" data-t="${t}">${d}${cnt !== '' && t !== from ? `<i>${cnt}</i>` : ''}</button>`;
      }
      grid.innerHTML = s;
      if (sel == null) wEl.innerHTML = `Start: <span style="color:#b07d00">${esc(fmt(from))}</span> (${wk(from)}). Tap another date.`;
      else { const dd = Math.round((sel - from) / DAY); wEl.textContent = `${fmt(sel)} (${wk(sel)}) is ${Math.abs(dd)} day${Math.abs(dd) === 1 ? '' : 's'} ${dd >= 0 ? 'after' : 'before'} ${fmt(from)}`; }
    }
    grid.addEventListener('click', e => {
      const b = e.target.closest('[data-t]'); if (!b) return;
      const t = +b.dataset.t; if (t === from) { sel = null; draw(); return; }
      sel = t; api.sfx('tap'); hint(''); draw();
      if (!won && t === target) { won = true; api.sfx('correct'); hint('⭐ Correct date!'); const dd = Math.round((target - from) / DAY); api.win(`${fmtY(target)} is a ${wk(target)} — ${Math.abs(dd)} days ${dd >= 0 ? 'after' : 'before'} ${fmt(from)}`); }
      else if (!won) { const dd = Math.round((target - from) / DAY), got = Math.round((t - from) / DAY); hint(p.to != null && p.to !== '' ? 'Tap the end date to finish' : got < dd ? 'Not yet — count further' : 'Too far — count back'); }
    });
    host.querySelector('.lb-clockset-cm').addEventListener('click', e => { const b = e.target.closest('[data-nav]'); if (!b) return; vm += +b.dataset.nav; if (vm < 0) { vm = 11; vy--; } if (vm > 11) { vm = 0; vy++; } api.sfx('tap'); draw(); });
    host.querySelector('.lb-clockset-row').addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      if (b.dataset.act === 'reset') { sel = null; hint(''); draw(); return; }
      if (b.dataset.act === 'new') {
        const r = (a, c) => a + Math.floor(Math.random() * (c - a + 1));
        const nd = new Date(D(y0, r(0, 11), r(1, 28))); from = nd.getTime(); target = from + r(3, 25) * DAY; p = Object.assign({}, p, { to: null });
        vy = nd.getUTCFullYear(); vm = nd.getUTCMonth(); sel = null; customText = '';
        if (won) { won = false; api.resetWin && api.resetWin(); }
        setText(); hint(''); draw(); api.sfx('tap');
      }
    });
    setText(); draw();
    return () => { };
  }
})();
