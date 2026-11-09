/* Knowtopia Concept Lab: sound — waves you can see and hear, echoes, and the range of hearing.
 *
 * wave:    amplitude and frequency sliders change a drawn wave (displacement vs time) AND a real tone
 *          (Web Audio, starts only after the child taps Play; stopped on cleanup). Bigger amplitude =
 *          louder, higher frequency = higher pitch. Shows T = 1/f and λ = v/f.
 * echo:    the child sets the distance to a cliff (or the sea bed) and taps Shout: a pulse travels out
 *          and back, a click and its echo play, t = 2d/v is shown. A clear echo needs t ≥ 0.1 s.
 * hearing: a log frequency slider over 1 Hz – 200 kHz with hearing ranges of humans and animals;
 *          infrasonic / audible / ultrasonic zones; audible frequencies can be played.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   mode       string  'wave' | 'echo' | 'hearing'                                       default 'wave'
 *   modes      array   modes offered as tabs                                             default [mode]
 *   goal       string  wave: 'match' (match the dashed target wave) | 'freq' (f = target Hz);
 *                      echo: 'min' (shortest distance for a clear echo) | 'time' (echo after target s);
 *                      hearing: 'who' (target {hear:[names], not:[names]}) | 'ultrasonic' | 'infrasonic' |
 *                      'band' (target [lo,hi] Hz); any: 'none'      default 'match' / 'min' / 'who'
 *   target     any     wave match: {amp, freq}; freq: Hz; time: seconds; who/band as above
 *   challenge  string  challenge text (any language); default made from goal
 *   winText    string  optional win message
 *   amp        number  starting amplitude (1–10, arbitrary units)                        default 4
 *   freq       number  starting frequency in Hz                                          default 300
 *   freqRange  [min,max,step] wave-mode frequency slider in Hz                          default [100,1000,10]
 *   window     number  wave-mode time window shown, in ms                                default 10
 *   v          number  speed of sound in m/s                                             default 343
 *   medium     string  medium name shown (e.g. 'Air', 'Sea water')                       default 'Air'
 *   distance   number  echo: starting distance in m                                      default 40
 *   distRange  [min,max,step] echo distance slider in m                                 default [5,200,1]
 *   scene      string  echo: 'cliff' (horizontal) | 'sea' (ship & sea bed, SONAR)        default 'cliff'
 *   hearFreq   number  hearing: starting frequency in Hz                                 default 1000
 *   creatures  array   hearing: [{name, lo, hi}] in Hz                  default Humans, Dogs, Bats, Elephants, Dolphins
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fN = (v, d = 2) => { const r = Math.round(v * Math.pow(10, d)) / Math.pow(10, d); return String(Object.is(r, -0) ? 0 : r); };
  const hz = v => v >= 1000 ? `${fN(v / 1000, v >= 10000 ? 0 : 1)} kHz` : `${fN(v, 0)} Hz`;
  const big = v => Math.round(v).toLocaleString('en-IN');
  const rng = (a, def) => Array.isArray(a) && a.length >= 2 && +a[1] > +a[0] ? [+a[0], +a[1], +a[2] > 0 ? +a[2] : def[2]] : def;
  const CREAT = [{ name: 'Humans', lo: 20, hi: 20000 }, { name: 'Dogs', lo: 67, hi: 45000 }, { name: 'Bats', lo: 2000, hi: 110000 }, { name: 'Elephants', lo: 16, hi: 12000 }, { name: 'Dolphins', lo: 75, hi: 150000 }];
  const CCOL = ['#8b5cf6', '#ff9f1c', '#1b1f3a', '#6b7090', '#3b82f6', '#2ed3a5', '#ff6b6b'];

  const CSS = `
.lb-sound-w{font-size:14px;color:#1b1f3a;-webkit-user-select:none;user-select:none}
.lb-sound-ch{font-weight:800;font-size:14px;margin-bottom:6px;line-height:1.25}
.lb-sound-svg{width:100%;height:auto;display:block;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:16px}
.lb-sound-row{display:flex;gap:6px;margin-top:6px}
.lb-sound-b{flex:1 1 0;min-width:0;min-height:42px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:13px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0 6px}
.lb-sound-b.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-sound-b.play{background:#2ed3a5;color:#fff;box-shadow:0 3px 0 #1a9c78}
.lb-sound-b.play.on{background:#ff6b6b;box-shadow:0 3px 0 #c94545}
.lb-sound-b:active{transform:translateY(2px)}
.lb-sound-sl{display:flex;align-items:center;gap:8px;font-weight:800;font-size:13px;margin-top:2px}
.lb-sound-sl span{min-width:70px}
.lb-sound-sl input{flex:1;min-width:0;accent-color:#8b5cf6;height:34px}
.lb-sound-sl b{min-width:62px;text-align:right;color:#3b82f6;font-variant-numeric:tabular-nums}
.lb-sound-out{background:#f6f4ff;border-radius:12px;padding:6px 10px;margin-top:5px;font-weight:800;font-size:13px;line-height:1.35;min-height:36px}
.lb-sound-out i{font-style:normal;color:#6b7090;font-size:12px}
`;

  Labs.register('sound', {
    title: 'Sound lab',
    subjects: ['science', 'physics'],
    render(host, p, api) {
      const ex = this.example || {};
      const diffMode = p.mode !== undefined && p.mode !== ex.mode;
      p = Object.assign({}, p);
      if (diffMode) ['modes', 'goal', 'target'].forEach(k => { if (p[k] === ex[k]) delete p[k]; });
      if (diffMode || p.goal !== ex.goal || p.target !== ex.target) ['challenge', 'winText'].forEach(k => { if (p[k] === ex[k]) delete p[k]; });

      const ALL = ['wave', 'echo', 'hearing'];
      let mode = ALL.includes(p.mode) ? p.mode : 'wave';
      const modes = (Array.isArray(p.modes) ? p.modes : []).filter(m => ALL.includes(m));
      if (!modes.includes(mode)) modes.unshift(mode);
      const V = +p.v > 0 ? +p.v : 343;
      const medium = String(p.medium || 'Air');
      const GOALS = { wave: ['match', 'freq', 'none'], echo: ['min', 'time', 'none'], hearing: ['who', 'ultrasonic', 'infrasonic', 'band', 'none'] };
      const GDEF = { wave: 'match', echo: 'min', hearing: 'who' };
      let won = false, raf = 0;
      const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(p.winText ? String(p.winText) : m); };

      // ---------- audio (created only after a tap) ----------
      let ctx = null, osc = null, gain = null;
      const audio = () => {
        if (!ctx) { const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return null; try { ctx = new AC(); } catch (e) { return null; } }
        if (ctx.state === 'suspended') ctx.resume();
        return ctx;
      };
      function toneOn(f, vol) {
        const c = audio(); if (!c) return false;
        if (!osc) {
          osc = c.createOscillator(); gain = c.createGain(); gain.gain.value = 0; osc.type = 'sine';
          osc.frequency.value = f; osc.connect(gain); gain.connect(c.destination); osc.start();
        }
        osc.frequency.setTargetAtTime(f, c.currentTime, 0.015);
        gain.gain.setTargetAtTime(vol, c.currentTime, 0.03);
        return true;
      }
      function toneOff() {
        if (!osc || !ctx) return;
        const o = osc, g = gain; osc = null; gain = null;
        try { g.gain.setTargetAtTime(0, ctx.currentTime, 0.03); o.stop(ctx.currentTime + 0.25); } catch (e) { }
      }
      function click(at, vol) {
        const c = audio(); if (!c) return;
        const o = c.createOscillator(), g = c.createGain(), t = c.currentTime + at;
        o.type = 'triangle'; o.frequency.setValueAtTime(900, t); o.frequency.exponentialRampToValueAtTime(300, t + 0.08);
        g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t + 0.005); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.09);
        o.connect(g); g.connect(c.destination); o.start(t); o.stop(t + 0.1);
      }

      host.innerHTML = `<style>${CSS}</style><div class="lb-sound-w">
  <div class="lb-sound-ch"></div>
  ${modes.length > 1 ? `<div class="lb-sound-row" style="margin:0 0 6px">${modes.map(m => `<button class="lb-sound-b" data-mode="${m}">${{ wave: '〰 Wave', echo: '📣 Echo', hearing: '👂 Hearing' }[m]}</button>`).join('')}</div>` : ''}
  <div class="lb-sound-body"></div></div>`;
      const chEl = host.querySelector('.lb-sound-ch'), body = host.querySelector('.lb-sound-body');
      let cleanupMode = () => { };
      const goalFor = m => (p.goal && GOALS[m].includes(p.goal)) ? p.goal : GDEF[m];
      const setCh = (m, def) => { chEl.textContent = '🎯 Challenge: ' + (p.challenge && (!p.goal || GOALS[m].includes(p.goal)) && m === (ALL.includes(p.mode) ? p.mode : 'wave') ? String(p.challenge) : def); };

      function setup() {
        cleanupMode(); toneOff(); cancelAnimationFrame(raf);
        host.querySelectorAll('[data-mode]').forEach(b => b.classList.toggle('on', b.dataset.mode === mode));
        cleanupMode = mode === 'wave' ? waveMode(goalFor('wave')) : mode === 'echo' ? echoMode(goalFor('echo')) : hearingMode(goalFor('hearing'));
      }

      // ================= WAVE =================
      function waveMode(goal) {
        const fR = rng(p.freqRange, [100, 1000, 10]);
        const snapF = v => Math.min(fR[1], Math.max(fR[0], Math.round((v - fR[0]) / fR[2]) * fR[2] + fR[0]));
        let A = Math.min(10, Math.max(1, Math.round(+p.amp || 4))), F = snapF(+p.freq || 300);
        const win = +p.window > 0 ? +p.window : 10;
        const tg = goal === 'match' ? Object.assign({ amp: 8, freq: 600 }, typeof p.target === 'object' && p.target ? p.target : {}) : null;
        if (tg) { tg.amp = Math.min(10, Math.max(1, Math.round(+tg.amp))); tg.freq = snapF(+tg.freq); }
        const tf = goal === 'freq' ? snapF(+p.target || 500) : 0;
        if (tg && A === tg.amp && F === tg.freq) A = tg.amp > 1 ? tg.amp - 1 : 2;
        if (goal === 'freq' && F === tf) F = snapF(F === fR[0] ? F + fR[2] : fR[0]);
        setCh('wave', goal === 'match' ? 'Make your wave match the dashed mystery wave (loudness AND pitch).' : goal === 'freq' ? `Make a sound of ${hz(tf)}.` : 'Change amplitude and frequency. Listen and watch!');
        let playing = false, phase = 0, touched = false, last = performance.now(), targetPlay = 0;
        body.innerHTML = `<svg class="lb-sound-svg" viewBox="0 0 360 150"></svg>
<div class="lb-sound-sl"><span>Amplitude</span><input type="range" class="lb-sound-a" min="1" max="10" step="1" value="${A}"><b></b></div>
<div class="lb-sound-sl"><span>Frequency</span><input type="range" class="lb-sound-f" min="${fR[0]}" max="${fR[1]}" step="${fR[2]}" value="${F}"><b></b></div>
<div class="lb-sound-row"><button class="lb-sound-b play" data-play="1">🔊 Play</button>${tg ? '<button class="lb-sound-b" data-tplay="1">🎵 Mystery sound</button>' : ''}</div>
<div class="lb-sound-out"></div>`;
        const sv = body.querySelector('svg'), out = body.querySelector('.lb-sound-out'), aIn = body.querySelector('.lb-sound-a'), fIn = body.querySelector('.lb-sound-f'), pBtn = body.querySelector('[data-play]');
        const X0 = 30, X1 = 350, Y0 = 72, kA = 5.6;
        const path = (amp, f, ph) => {
          let d = '';
          for (let i = 0; i <= 320; i++) { const t = win * i / 320 / 1000; const y = Y0 - amp * kA * Math.sin(2 * Math.PI * f * t - ph); d += (i ? 'L' : 'M') + (X0 + i).toFixed(1) + ' ' + y.toFixed(1); }
          return d;
        };
        function draw() {
          let o = `<line x1="${X0}" y1="${Y0}" x2="${X1}" y2="${Y0}" stroke="#c4c8e0" stroke-width="1.5"/><line x1="${X0}" y1="12" x2="${X0}" y2="132" stroke="#1b1f3a" stroke-width="1.5"/>`;
          o += `<text x="${X0 + 4}" y="12" font-size="10" font-weight="800" fill="#6b7090">displacement</text><text x="${X1}" y="145" text-anchor="end" font-size="10" font-weight="800" fill="#6b7090">time → (${fN(win)} ms shown)</text>`;
          if (tg) o += `<path d="${path(tg.amp, tg.freq, phase)}" fill="none" stroke="#2ed3a5" stroke-width="3" stroke-dasharray="6 5" opacity=".95"/>`;
          o += `<path d="${path(A, F, phase)}" fill="none" stroke="#8b5cf6" stroke-width="3.5" stroke-linejoin="round"/>`;
          // one period bracket
          const Tpx = 320 * (1000 / F) / win;
          if (Tpx > 14 && Tpx < 300) {
            const x0 = X0 + ((phase / (2 * Math.PI)) * Tpx) % Tpx; const yb = 136;
            o += `<path d="M${x0} ${yb - 5} V${yb} H${x0 + Tpx} V${yb - 5}" fill="none" stroke="#ff6b6b" stroke-width="2"/><text x="${x0 + Tpx / 2}" y="${yb - 6}" text-anchor="middle" font-size="10" font-weight="800" fill="#ff6b6b">T</text>`;
          }
          // amplitude marker
          o += `<line x1="${X0 - 10}" y1="${Y0}" x2="${X0 - 10}" y2="${Y0 - A * kA}" stroke="#3b82f6" stroke-width="3"/><path d="M${X0 - 10} ${Y0 - A * kA - 1} l-4 7 h8z" fill="#3b82f6"/><text x="${X0 - 18}" y="${Y0 - A * kA / 2 + 4}" text-anchor="middle" font-size="10" font-weight="800" fill="#3b82f6">A</text>`;
          sv.innerHTML = o;
        }
        function info() {
          aIn.nextElementSibling.textContent = `${A}`;
          fIn.nextElementSibling.textContent = hz(F);
          const pitch = F < (fR[0] + (fR[1] - fR[0]) / 3) ? 'low' : F < (fR[0] + 2 * (fR[1] - fR[0]) / 3) ? 'medium' : 'high';
          out.innerHTML = `Pitch: ${pitch} (${hz(F)}) · Loudness ∝ A² = ${A * A}<br><i>T = 1/f = ${fN(1000 / F, 2)} ms · λ = v/f = ${fN(V, 0)} ÷ ${fN(F, 0)} = ${fN(V / F, 2)} m</i>`;
          if (playing) toneOn(F, 0.25 * A / 10);
        }
        function check() {
          if (!touched) return;
          if (tg && A === tg.amp && F === tg.freq) winOnce(`Matched! Amplitude ${A} sets loudness, frequency ${hz(F)} sets pitch.`);
          if (goal === 'freq' && F === tf) winOnce(`${hz(F)}: ${fN(F, 0)} vibrations every second. T = 1/f = ${fN(1000 / F, 2)} ms.`);
        }
        function loop(now) {
          const dt = Math.min(0.05, (now - last) / 1000); last = now;
          phase = (phase + dt * (playing ? 6 : 2)) % (Math.PI * 200);
          draw(); raf = requestAnimationFrame(loop);
        }
        const onIn = e => { if (e.target === aIn) A = +aIn.value; else if (e.target === fIn) F = +fIn.value; touched = true; info(); check(); };
        const onClick = e => {
          const b = e.target.closest('button'); if (!b) return;
          if (b.dataset.play) {
            playing = !playing;
            if (playing) { clearTimeout(targetPlay); if (!toneOn(F, 0.25 * A / 10)) playing = false; } else toneOff();
            pBtn.classList.toggle('on', playing); pBtn.textContent = playing ? '🔇 Stop' : '🔊 Play';
          } else if (b.dataset.tplay) {
            playing = false; pBtn.classList.remove('on'); pBtn.textContent = '🔊 Play';
            if (toneOn(tg.freq, 0.25 * tg.amp / 10)) { clearTimeout(targetPlay); targetPlay = setTimeout(toneOff, 1200); }
          }
        };
        body.addEventListener('input', onIn); body.addEventListener('click', onClick);
        info(); raf = requestAnimationFrame(loop);
        return () => { cancelAnimationFrame(raf); clearTimeout(targetPlay); toneOff(); body.removeEventListener('input', onIn); body.removeEventListener('click', onClick); };
      }

      // ================= ECHO =================
      function echoMode(goal) {
        const dR = rng(p.distRange, [5, 200, 1]);
        const snapD = v => Math.min(dR[1], Math.max(dR[0], Math.round((v - dR[0]) / dR[2]) * dR[2] + dR[0]));
        let D = snapD(+p.distance || 40);
        const sea = p.scene === 'sea';
        const tt = +p.target || 1;
        setCh('echo', goal === 'min' ? 'Find the SHORTEST distance that still gives a clear echo. Shout to test!' : goal === 'time' ? `Set the distance so the echo comes back after ${fN(tt)} s. Shout to test!` : 'Change the distance and shout. When is the echo clear?');
        let shot = null, timers = [];
        body.innerHTML = `<svg class="lb-sound-svg" viewBox="0 0 360 170"></svg>
<div class="lb-sound-sl"><span>${sea ? 'Depth' : 'Distance'}</span><input type="range" min="${dR[0]}" max="${dR[1]}" step="${dR[2]}" value="${D}"><b></b></div>
<div class="lb-sound-row"><button class="lb-sound-b play" data-shout="1">${sea ? '📡 Send pulse' : '📣 Shout!'}</button></div>
<div class="lb-sound-out"></div>`;
        const sv = body.querySelector('svg'), out = body.querySelector('.lb-sound-out'), dIn = body.querySelector('input');
        const tEcho = () => 2 * D / V;
        // geometry: horizontal (cliff) or vertical (sea)
        const S0 = sea ? 44 : 46, S1 = sea ? 156 : 334;
        const posOf = d => S0 + (S1 - S0) * d / dR[1];
        function draw(now) {
          const wallP = posOf(D);
          let o = '';
          let pulse = null, el = 0;
          if (shot) {
            el = (now - shot.t0) / 1000;
            const total = shot.t;
            if (el <= total) { const half = total / 2; pulse = el <= half ? { at: S0 + (wallP - S0) * el / half, back: false } : { at: wallP - (wallP - S0) * (el - half) / half, back: true }; }
          }
          if (!sea) {
            o += `<rect x="0" y="0" width="360" height="132" fill="#dff1ff"/><rect x="0" y="132" width="360" height="38" fill="#9fd88a"/>`;
            o += `<path d="M${wallP} 132 L${wallP + 4} 70 L${wallP + 14} 40 L${wallP + 10} 18 L360 10 V132Z" fill="#8a7a6b" stroke="#6b5d50" stroke-width="2"/>`;
            o += `<g transform="translate(24 96)"><circle cx="0" cy="-14" r="9" fill="#ffcf9e" stroke="#1b1f3a" stroke-width="2"/><path d="M0 -5 V22 M0 22 L-8 36 M0 22 L8 36 M0 4 L10 -4 M0 4 L-9 12" stroke="#1b1f3a" stroke-width="3" stroke-linecap="round" fill="none"/><path d="M5 -14 l6 -3 v6z" fill="#1b1f3a"/></g>`;
            if (pulse) { for (let k = 0; k < 3; k++) { const x = pulse.at - (pulse.back ? -1 : 1) * k * 7; o += `<path d="M${x} 66 q${pulse.back ? -10 : 10} 18 0 36" fill="none" stroke="${pulse.back ? '#ff6b6b' : '#8b5cf6'}" stroke-width="${3.5 - k}" opacity="${1 - k * 0.3}"/>`; } }
            o += `<line x1="${S0}" y1="150" x2="${wallP}" y2="150" stroke="#1b1f3a" stroke-width="1.5"/><path d="M${S0} 150 l6 -4 v8z M${wallP} 150 l-6 -4 v8z" fill="#1b1f3a"/><text x="${(S0 + wallP) / 2}" y="164" text-anchor="middle" font-size="11.5" font-weight="800" fill="#1b1f3a">d = ${fN(D, 1)} m</text>`;
          } else {
            o += `<rect x="0" y="0" width="360" height="40" fill="#dff1ff"/><rect x="0" y="40" width="360" height="130" fill="#4aa3df"/>`;
            o += `<path d="M0 ${wallP} Q90 ${wallP - 6} 180 ${wallP} T360 ${wallP} V170 H0Z" fill="#c9a25a"/>`;
            o += `<path d="M150 30 h70 l-10 14 h-50z" fill="#ff6b6b"/><rect x="172" y="18" width="22" height="12" rx="2" fill="#fff"/>`;
            if (pulse) { for (let k = 0; k < 3; k++) { const y = pulse.at - (pulse.back ? -1 : 1) * k * 6; o += `<path d="M168 ${y} q17 ${pulse.back ? -9 : 9} 34 0" fill="none" stroke="${pulse.back ? '#ffc93c' : '#fff'}" stroke-width="${3.5 - k}" opacity="${1 - k * 0.3}"/>`; } }
            o += `<line x1="90" y1="${S0}" x2="90" y2="${wallP}" stroke="#fff" stroke-width="1.5"/><text x="96" y="${Math.max(S0 + 14, (S0 + wallP) / 2 + 4)}" font-size="11.5" font-weight="800" fill="#1b1f3a" stroke="#fff" stroke-width="3" paint-order="stroke">depth = ${big(D)} m</text>`;
          }
          const tShow = shot ? Math.min(el, shot.t) : 0;
          o += `<rect x="${sea ? 250 : 120}" y="8" width="${sea ? 100 : 110}" height="24" rx="10" fill="rgba(255,255,255,.9)"/><text x="${sea ? 300 : 175}" y="25" text-anchor="middle" font-size="13" font-weight="800" fill="#1b1f3a">⏱ ${fN(tShow, 2)} s</text>`;
          sv.innerHTML = o;
        }
        function info() {
          dIn.nextElementSibling.textContent = `${fN(D, 1)} m`;
          const t = tEcho(), clear = t >= 0.1;
          out.innerHTML = `t = 2d ÷ v = 2 × ${fN(D, 1)} ÷ ${fN(V, 0)} = <span style="color:#8b5cf6">${fN(t, 3)} s</span>` +
            (sea ? '' : clear ? ' → <span style="color:#14a37f">clear echo (≥ 0.1 s)</span>' : ' → <span style="color:#e04848">too quick, it mixes with your shout (< 0.1 s)</span>') +
            `<br><i>Speed of sound in ${esc(medium)} = ${fN(V, 0)} m/s</i>`;
        }
        function frame(now) { draw(now); if (shot && (now - shot.t0) / 1000 <= shot.t + 0.05) raf = requestAnimationFrame(frame); else { draw(now); } }
        function shout() {
          const t = tEcho();
          cancelAnimationFrame(raf); timers.forEach(clearTimeout); timers = [];
          shot = { t0: performance.now(), t };
          click(0, 0.35); if (t >= 0.1 || sea) click(t, 0.12); else click(t, 0.25);
          raf = requestAnimationFrame(frame);
          timers.push(setTimeout(() => {
            if (goal === 'min') {
              const prev = D - dR[2];
              if (t >= 0.1 && (prev < dR[0] || 2 * prev / V < 0.1)) winOnce(`At ${fN(D, 1)} m the echo takes ${fN(t, 3)} s. You need t ≥ 0.1 s, so d ≥ ${fN(0.1 * V / 2, 1)} m.`);
              else api.sfx('hmm');
            } else if (goal === 'time') {
              if (Math.abs(t - tt) <= Math.max(0.01, dR[2] / V + 1e-9)) winOnce(`d = v × t ÷ 2 = ${fN(V, 0)} × ${fN(tt)} ÷ 2 = ${fN(V * tt / 2, 1)} m`);
              else api.sfx('hmm');
            }
          }, t * 1000 + 150));
        }
        const onIn = () => { D = +dIn.value; shot = null; info(); draw(performance.now()); };
        const onClick = e => { if (e.target.closest('[data-shout]')) shout(); };
        body.addEventListener('input', onIn); body.addEventListener('click', onClick);
        info(); draw(performance.now());
        return () => { cancelAnimationFrame(raf); timers.forEach(clearTimeout); body.removeEventListener('input', onIn); body.removeEventListener('click', onClick); };
      }

      // ================= HEARING =================
      function hearingMode(goal) {
        const cr = (Array.isArray(p.creatures) && p.creatures.length ? p.creatures : CREAT).filter(c => c && +c.hi > +c.lo && +c.lo > 0).map(c => ({ name: String(c.name), lo: +c.lo, hi: +c.hi })).slice(0, 7);
        const LMIN = 0, LMAX = Math.log10(200000);
        const fOf = s => Math.pow(10, LMIN + (LMAX - LMIN) * s / 1000);
        const sOf = f => Math.round((Math.log10(f) - LMIN) / (LMAX - LMIN) * 1000);
        const roundF = f => { const p10 = Math.pow(10, Math.floor(Math.log10(f)) - 1); return Math.max(1, Math.round(f / p10) * p10); };
        let S = sOf(+p.hearFreq || 1000), F = roundF(fOf(S));
        let tgt = p.target;
        let whoH = [], whoN = [], band = null;
        if (goal === 'who') { tgt = tgt && typeof tgt === 'object' && !Array.isArray(tgt) ? tgt : { hear: ['Dogs'], not: ['Humans'] }; whoH = (tgt.hear || []).map(String); whoN = (tgt.not || []).map(String); }
        if (goal === 'band') band = Array.isArray(tgt) && tgt.length === 2 ? tgt.map(Number) : [20, 20000];
        const defCh = goal === 'who' ? `Find a sound that ${whoH.join(' and ') || '…'} can hear but ${whoN.join(' and ') || 'nobody else'} cannot.`
          : goal === 'ultrasonic' ? 'Find an ultrasonic sound (above 20 kHz). Who can still hear it?'
            : goal === 'infrasonic' ? 'Find an infrasonic sound (below 20 Hz). Who can hear it?'
              : goal === 'band' ? `Set a frequency between ${hz(band[0])} and ${hz(band[1])}.` : 'Slide through the frequencies. Who can hear what?';
        setCh('hearing', defCh);
        let playing = false, touched = false;
        const rowH = 17, top = 34, X0 = 16, X1 = 344;
        const xOf = f => X0 + (X1 - X0) * (Math.log10(f) - LMIN) / (LMAX - LMIN);
        const H = top + cr.length * rowH + 30;
        body.innerHTML = `<svg class="lb-sound-svg" viewBox="0 0 360 ${H}"></svg>
<div class="lb-sound-sl"><span>Frequency</span><input type="range" min="0" max="1000" step="1" value="${S}"><b></b></div>
<div class="lb-sound-row"><button class="lb-sound-b play" data-play="1">🔊 Play</button></div>
<div class="lb-sound-out"></div>`;
        const sv = body.querySelector('svg'), out = body.querySelector('.lb-sound-out'), sIn = body.querySelector('input'), pBtn = body.querySelector('[data-play]');
        const hears = f => cr.filter(c => f >= c.lo && f <= c.hi).map(c => c.name);
        function draw() {
          let o = `<rect x="${X0}" y="8" width="${xOf(20) - X0}" height="${H - 16}" fill="#e9e6ff" rx="6"/><rect x="${xOf(20)}" y="8" width="${xOf(20000) - xOf(20)}" height="${H - 16}" fill="#e3fbf3"/><rect x="${xOf(20000)}" y="8" width="${X1 - xOf(20000)}" height="${H - 16}" fill="#fff1dc" rx="6"/>`;
          o += `<text x="${(X0 + xOf(20)) / 2}" y="22" text-anchor="middle" font-size="9.5" font-weight="800" fill="#7a5cd6">INFRA</text><text x="${(xOf(20) + xOf(20000)) / 2}" y="22" text-anchor="middle" font-size="10" font-weight="800" fill="#14a37f">AUDIBLE (humans)</text><text x="${(xOf(20000) + X1) / 2}" y="22" text-anchor="middle" font-size="9.5" font-weight="800" fill="#d9822b">ULTRA</text>`;
          cr.forEach((c, i) => {
            const y = top + i * rowH, on = F >= c.lo && F <= c.hi, col = CCOL[i % CCOL.length];
            o += `<rect x="${xOf(c.lo)}" y="${y}" width="${xOf(c.hi) - xOf(c.lo)}" height="${rowH - 5}" rx="6" fill="${col}" opacity="${on ? 0.95 : 0.35}"/>`;
            const lx = xOf(c.lo) + 4, fits = xOf(c.hi) - xOf(c.lo) > 60;
            o += `<text x="${fits ? lx : xOf(c.hi) + 4}" y="${y + rowH - 8.5}" font-size="10.5" font-weight="800" fill="${fits ? '#fff' : col}">${esc(c.name)}${on ? ' ✓' : ''}</text>`;
          });
          const ax = top + cr.length * rowH + 4;
          [1, 10, 100, 1000, 10000, 100000].forEach(f => { o += `<line x1="${xOf(f)}" y1="${ax}" x2="${xOf(f)}" y2="${ax + 4}" stroke="#6b7090"/><text x="${xOf(f)}" y="${ax + 15}" text-anchor="middle" font-size="9.5" font-weight="700" fill="#6b7090">${hz(f)}</text>`; });
          const mx = xOf(F);
          o += `<line x1="${mx}" y1="10" x2="${mx}" y2="${ax}" stroke="#ff6b6b" stroke-width="3"/><circle cx="${mx}" cy="${ax}" r="5" fill="#ff6b6b"/>`;
          sv.innerHTML = o;
        }
        function info() {
          sIn.nextElementSibling.textContent = hz(F);
          const zone = F < 20 ? 'infrasonic' : F > 20000 ? 'ultrasonic' : 'audible';
          const who = hears(F);
          out.innerHTML = `${hz(F)} is <span style="color:#8b5cf6">${zone}</span>. Who hears it: ${who.length ? esc(who.join(', ')) : 'nobody here'}` +
            `<br><i>${playing && (F < 20 || F > 20000) ? '🔇 Your ears cannot hear this one!' : 'Humans hear about 20 Hz – 20 kHz (ranges are approximate).'}</i>`;
          if (playing) { if (F >= 20 && F <= 20000) toneOn(F, F > 8000 ? 0.08 : 0.16); else if (osc) gain.gain.setTargetAtTime(0, ctx.currentTime, 0.03); }
        }
        function check() {
          if (!touched) return;
          const who = hears(F), names = cr.map(c => c.name);
          if (goal === 'who' && whoH.every(n => who.includes(n) || !names.includes(n)) && whoN.every(n => !who.includes(n)) && whoH.some(n => who.includes(n)))
            winOnce(`${hz(F)}: ${whoH.join(', ')} can hear it, ${whoN.join(', ')} cannot.`);
          else if (goal === 'ultrasonic' && F > 20000) winOnce(`${hz(F)} is ultrasonic. Heard by: ${who.join(', ') || 'none of these'}.`);
          else if (goal === 'infrasonic' && F < 20) winOnce(`${hz(F)} is infrasonic. Heard by: ${who.join(', ') || 'none of these'}.`);
          else if (goal === 'band' && F >= band[0] && F <= band[1]) winOnce(`${hz(F)} is inside ${hz(band[0])} – ${hz(band[1])}.`);
        }
        const onIn = () => { S = +sIn.value; F = roundF(fOf(S)); touched = true; draw(); info(); check(); };
        const onClick = e => {
          if (!e.target.closest('[data-play]')) return;
          playing = !playing;
          if (playing) { if (!toneOn(F >= 20 && F <= 20000 ? F : 440, F >= 20 && F <= 20000 ? (F > 8000 ? 0.08 : 0.16) : 0)) playing = false; } else toneOff();
          pBtn.classList.toggle('on', playing); pBtn.textContent = playing ? '🔇 Stop' : '🔊 Play';
          info();
        };
        body.addEventListener('input', onIn); body.addEventListener('click', onClick);
        draw(); info();
        return () => { toneOff(); body.removeEventListener('input', onIn); body.removeEventListener('click', onClick); };
      }

      const onTab = e => { const b = e.target.closest('[data-mode]'); if (!b) return; mode = b.dataset.mode; api.sfx('tap'); setup(); };
      host.addEventListener('click', onTab);
      setup();
      return () => {
        cleanupMode(); cancelAnimationFrame(raf); toneOff(); host.removeEventListener('click', onTab);
        if (ctx) { const c = ctx; ctx = null; setTimeout(() => { try { c.close(); } catch (e) { } }, 300); }
      };
    },
    example: {
      mode: 'wave',
      modes: ['wave', 'echo', 'hearing'],
      goal: 'match', target: { amp: 8, freq: 600 },
      amp: 4, freq: 300, freqRange: [100, 1000, 10],
      challenge: 'Make your wave match the dashed mystery wave — louder AND higher. Tap 🔊 to listen.'
    },
    examples: [
      { mode: 'echo', modes: ['echo'], goal: 'min', distance: 60, distRange: [5, 100, 1], challenge: 'Grade 9: Find the shortest distance to the cliff for a clear echo (t ≥ 0.1 s).' },
      { mode: 'echo', modes: ['echo'], scene: 'sea', v: 1500, medium: 'Sea water', goal: 'time', target: 2, distance: 500, distRange: [100, 3000, 50], challenge: 'Grade 9 SONAR: The echo came back after 2 s. Set the sea depth to match.' },
      { mode: 'hearing', modes: ['hearing'], goal: 'who', target: { hear: ['Dogs'], not: ['Humans'] }, hearFreq: 1000, challenge: 'Grade 8: Find a whistle that a dog can hear but you cannot.' }
    ]
  });
})();
