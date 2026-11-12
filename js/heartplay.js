/* ================= 💗 Heart Compass games (js/heartplay.js) =================
   Hands-on emotional-intelligence games, played through the Mind Gym game engine (js/mindplay.js).
   Content and checks: js/heartplay-gen.js. Every game has a clear best answer checked by the app —
   no self-rating questionnaires, so nobody can “fake” a good result by tapping “Always”.
   Looks by age: j 🎈 Feelings Fair · m 🧭 Heart Quest · s/CA 💠 Heart Lab. Timed run: Rainbow Challenge / Heart Expedition / Heart Check.
   Skills (scorecard “Heart Wheel”): Know my feelings · Manage my feelings · Read others · Connect & care · Choose wisely */
(function () {
  'use strict';
  const D = document, $1 = (s, r) => (r || D).querySelector(s);
  const P = () => window.MindPlay;
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  const THEME = {
    j: { name: 'Feelings Fair', e: '🎈', test: 'Rainbow Challenge', cls: 'pl-j hp-j', hero: 'Play games about feelings — yours and your friends’!' },
    m: { name: 'Heart Quest', e: '🧭', test: 'Heart Expedition', cls: 'pl-m hp-m', hero: 'Explore the islands of feelings, friendship and smart choices.' },
    s: { name: 'Heart Lab', e: '💠', test: 'Heart Check', cls: 'pl-s hp-s', hero: 'Train the five skills of emotional intelligence, then take the timed check.' } };
  const GAMES = [
    { id: 'faces', e: '🕵️', skill: 'Read others', n: { j: 'Feeling Detective', m: 'Face Reader', s: 'Emotion Decoder' }, d: 'Read faces and situations — name the feeling' },
    { id: 'thermo', e: '🌡️', skill: 'Know my feelings', n: { j: 'Feelings Thermometer', m: 'Feeling Meter', s: 'Intensity Scale' }, d: 'Put feeling words in order, from mild to strong' },
    { id: 'shoes', e: '👟', skill: 'Read others', n: { j: 'In Their Shoes', m: 'In Their Shoes', s: 'Perspective Switch' }, d: 'One event, different people — give each the right feeling' },
    { id: 'chat', e: '💬', skill: 'Connect & care', n: { j: 'Kind Words Chat', m: 'Friend Chat', s: 'Support Chat' }, d: 'Reply to a friend who is having a hard time' },
    { id: 'paths', e: '🛤️', skill: 'Choose wisely', n: { j: 'Story Paths', m: 'Choose Your Path', s: 'Decision Paths' }, d: 'A story where every choice changes what happens' },
    { id: 'breathe', e: '🫧', skill: 'Manage my feelings', n: { j: 'Bubble Breathing', m: 'Calm Breath', s: 'Calm Breath' }, d: 'Breathe with the bubble to calm your body' }];
  const PLAY = () => P().PLAY;

  /* ---------- cartoon face (pure SVG, drawn from simple settings) ---------- */
  const SKIN = ['#ffd7b5', '#f2c094', '#d9a06b', '#b97a4b', '#8d5a36'], HAIR = ['#2b1d14', '#4a2c17', '#111', '#7a4a1f'];
  function face(feel, skin, hair, size) {
    const F = {
      happy: { bl: 'M30 36 q8 -6 16 0', br: 'M54 36 q8 -6 16 0', eye: 4.5, mouth: 'M34 64 q16 16 32 0', fill: 'none', cheek: .45 },
      sad: { bl: 'M30 38 q8 -2 16 -6', br: 'M54 32 q8 4 16 6', eye: 4, mouth: 'M36 72 q14 -12 28 0', fill: 'none', tear: 1 },
      angry: { bl: 'M30 32 l16 7', br: 'M70 32 l-16 7', eye: 4, mouth: 'M38 70 q12 -5 24 0', fill: 'none', red: 1 },
      scared: { bl: 'M30 30 q8 -6 16 -2', br: 'M54 28 q8 -4 16 2', eye: 6.5, mouth: 'M40 66 q10 -6 20 0 q-10 10 -20 0', fill: '#7a2b2b' },
      surprised: { bl: 'M30 28 q8 -8 16 0', br: 'M54 28 q8 -8 16 0', eye: 6.5, mouth: 'M50 62 m-7 0 a7 9 0 1 0 14 0 a7 9 0 1 0 -14 0', fill: '#7a2b2b' },
      disgusted: { bl: 'M30 36 l16 2', br: 'M70 33 l-16 4', eye: 3, mouth: 'M36 68 q8 -8 14 -2 q6 6 14 -4', fill: 'none', green: 1, nose: 1 } }[feel];
    const sk = SKIN[skin] || SKIN[0], hr = HAIR[hair] || HAIR[0];
    return `<svg viewBox="0 0 100 100" class="hp-face" style="width:${size || 150}px" aria-hidden="true">
      <circle cx="50" cy="52" r="38" fill="${F.green ? '#cfe8b8' : F.red ? '#ffb39a' : sk}" stroke="#3a2a20" stroke-width="2"/>
      <path d="M14 46 q2 -34 36 -34 q34 0 36 34 q-6 -18 -36 -20 q-30 2 -36 20z" fill="${hr}"/>
      ${F.cheek ? `<circle cx="30" cy="60" r="6" fill="#ff7b7b" opacity="${F.cheek}"/><circle cx="70" cy="60" r="6" fill="#ff7b7b" opacity="${F.cheek}"/>` : ''}
      <path d="${F.bl}" stroke="#3a2a20" stroke-width="3" fill="none" stroke-linecap="round"/><path d="${F.br}" stroke="#3a2a20" stroke-width="3" fill="none" stroke-linecap="round"/>
      <g class="hp-eyes"><circle cx="38" cy="46" r="${F.eye}" fill="#2a1d14"/><circle cx="62" cy="46" r="${F.eye}" fill="#2a1d14"/><circle cx="39.5" cy="44.5" r="1.4" fill="#fff"/><circle cx="63.5" cy="44.5" r="1.4" fill="#fff"/></g>
      ${F.nose ? '<path d="M46 56 q4 -4 8 0" stroke="#3a2a20" stroke-width="2" fill="none"/>' : '<path d="M49 52 q2 4 0 6" stroke="#3a2a20" stroke-width="1.6" fill="none"/>'}
      <path d="${F.mouth}" stroke="#3a2a20" stroke-width="3" fill="${F.fill}" stroke-linecap="round" stroke-linejoin="round"/>
      ${F.tear ? '<path d="M64 52 q3 6 0 9 q-3 -3 0 -9z" fill="#5bb8ff" class="hp-tear"/>' : ''}</svg>`;
  }

  /* ---------- games ---------- */
  function setup() {
    const X = PLAY();

    X.faces = (host, p, done) => {
      const b = P().band();
      host.innerHTML = p.mode === 'face'
        ? `<p class="pl-q">${b === 'j' ? `How is ${E(p.name)} feeling?` : `Look closely at ${E(p.name)}’s face. Which feeling is it?`}</p><div class="hp-stage"><button type="button" class="hp-facebtn" aria-label="Face to read">${face(p.face.feel, p.face.skin, p.face.hair, b === 'j' ? 170 : 150)}</button></div>`
        : `<div class="hp-story"><span class="hp-av" aria-hidden="true">${face('happy', Math.floor(Math.random() * 5), Math.floor(Math.random() * 4), 56).replace('class="hp-face"', 'class="hp-face neutral"')}</span><p class="pl-q">${E(p.text)}</p></div>`;
      host.insertAdjacentHTML('beforeend', `<div class="hp-opts">${p.opts.map(o => `<button type="button" class="hp-opt" data-k="${o.k}">${o.e ? `<span>${o.e}</span>` : ''}${E(o.w)}</button>`).join('')}</div>`);
      const fb = $1('.hp-facebtn', host); if (fb) fb.onclick = () => { fb.classList.remove('wig'); void fb.offsetWidth; fb.classList.add('wig'); S('tap'); };
      host.querySelectorAll('.hp-opt').forEach(x => x.onclick = () => {
        const ok = x.dataset.k === p.answer;
        host.querySelectorAll('.hp-opt').forEach(y => { y.disabled = true; if (y.dataset.k === p.answer) y.classList.add('ok'); });
        if (!ok) x.classList.add('no');
        done(ok, p.why);
      });
    };

    X.thermo = (host, p, done) => {
      const slots = [null, null, null];
      host.innerHTML = `<p class="pl-q">Fill the thermometer: tap the <b>mildest</b> feeling first, then the next, then the <b>strongest</b>.</p>
        <div class="hp-thermo"><div class="hp-tube"><div class="hp-merc"></div></div><div class="hp-slots"></div></div><div class="hp-tiles"></div><button type="button" class="btn pl-chkT">✓ Check</button>`;
      const draw = (reveal) => {
        const filled = slots.filter(x => x != null).length;
        $1('.hp-merc', host).style.height = `${12 + filled * 29}%`;
        $1('.hp-slots', host).innerHTML = [2, 1, 0].map(i => { const t = slots[i] != null ? p.tiles[slots[i]] : null;
          const cls = reveal ? (t && t.w === p.answer[i] ? ' ok' : ' no') : '';
          return `<button type="button" class="hp-slot${t ? ' full' : ''}${cls}" data-s="${i}"><small>${['Mild', 'Medium', 'Strong'][i]}</small>${t ? `${t.e ? t.e + ' ' : ''}${E(t.w)}` : '…'}${reveal && (!t || t.w !== p.answer[i]) ? ` <i>→ ${E(p.answer[i])}</i>` : ''}</button>`; }).join('');
        $1('.hp-tiles', host).innerHTML = p.tiles.map((t, i) => `<button type="button" class="hp-tile${slots.includes(i) ? ' used' : ''}" data-t="${i}" ${slots.includes(i) || reveal ? 'disabled' : ''}>${t.e ? `<span>${t.e}</span>` : ''}${E(t.w)}</button>`).join('');
        if (reveal) return;
        host.querySelectorAll('[data-t]').forEach(x => x.onclick = () => { const k = slots.indexOf(null); if (k < 0) return; S('tap'); slots[k] = +x.dataset.t; draw(); });
        host.querySelectorAll('[data-s]').forEach(x => x.onclick = () => { const k = +x.dataset.s; if (slots[k] == null) return; S('tap'); slots[k] = null; draw(); });
      };
      draw();
      $1('.pl-chkT', host).onclick = () => {
        if (slots.includes(null)) { toast('Place all three feelings first'); return; }
        $1('.pl-chkT', host).remove(); draw(true);
        const ok = slots.every((t, i) => p.tiles[t].w === p.answer[i]);
        done(ok, p.why);
      };
    };

    X.shoes = (host, p, done) => {
      const given = p.roles.map(() => null); let held = null;
      host.innerHTML = `<div class="hp-event">${E(p.text)}</div><p class="pl-q">Give each person the feeling sticker that fits. Tap a sticker, then tap a person.</p><div class="hp-roles"></div><div class="hp-stickers"></div><button type="button" class="btn pl-chkS">✓ Check</button>`;
      const draw = reveal => {
        $1('.hp-roles', host).innerHTML = p.roles.map((r, i) => { const g = given[i] != null ? p.stickers[given[i]] : null, cls = reveal ? (g && r.ok.includes(g.k) ? ' ok' : ' no') : '';
          return `<button type="button" class="hp-role${cls}" data-r="${i}"><span class="hp-who">${E(r.who)}</span><span class="hp-drop">${g ? `${g.e}<small>${E(g.k)}</small>` : '＋'}</span>${reveal && !(g && r.ok.includes(g.k)) ? `<small class="hp-fix">fits: ${E(r.ok.join(', '))}</small>` : ''}</button>`; }).join('');
        $1('.hp-stickers', host).innerHTML = p.stickers.map((t, i) => `<button type="button" class="hp-stk${held === i ? ' held' : ''}${given.includes(i) ? ' used' : ''}" data-k="${i}" ${reveal ? 'disabled' : ''}><span>${t.e}</span><small>${E(t.k)}</small></button>`).join('');
        if (reveal) return;
        host.querySelectorAll('[data-k]').forEach(x => x.onclick = () => { S('tap'); const i = +x.dataset.k; const at = given.indexOf(i); if (at >= 0) given[at] = null; held = held === i ? null : i; draw(); });
        host.querySelectorAll('[data-r]').forEach(x => x.onclick = () => { const r = +x.dataset.r; if (held == null) { if (given[r] != null) { given[r] = null; S('tap'); draw(); } return; } S('open'); given[r] = held; held = null; draw(); });
      };
      draw();
      $1('.pl-chkS', host).onclick = () => {
        if (given.includes(null)) { toast('Give everyone a sticker first'); return; }
        $1('.pl-chkS', host).remove(); draw(true);
        const ok = p.roles.every((r, i) => r.ok.includes(p.stickers[given[i]].k));
        done(ok, p.why);
      };
    };

    X.chat = (host, p, done) => {
      const moods = ['😞', '😟', '🙂', '😊'];
      let mood = 1, score = 0;
      host.innerHTML = `<div class="hp-phone"><div class="hp-ph-top"><span class="hp-ph-av">${E(p.name[0])}</span><b>${E(p.name)}</b><span class="hp-mood" aria-label="Friend’s mood">${moods[mood]}</span></div><div class="hp-msgs"></div><div class="hp-replies"></div></div>`;
      const msgs = $1('.hp-msgs', host), rep = $1('.hp-replies', host);
      const say = (txt, me) => new Promise(res => {
        if (me) { msgs.insertAdjacentHTML('beforeend', `<div class="hp-b me">${E(txt)}</div>`); msgs.scrollTop = 1e4; return setTimeout(res, 250); }
        msgs.insertAdjacentHTML('beforeend', '<div class="hp-b typing"><i></i><i></i><i></i></div>'); msgs.scrollTop = 1e4;
        setTimeout(() => { const t = msgs.querySelector('.typing'); if (t) t.outerHTML = `<div class="hp-b">${E(txt)}</div>`; msgs.scrollTop = 1e4; S('tap'); res(); }, 900);
      });
      const setMood = m => { mood = Math.max(0, Math.min(3, m)); const el = $1('.hp-mood', host); el.textContent = moods[mood]; el.classList.remove('bump'); void el.offsetWidth; el.classList.add('bump'); };
      const ask = opts => new Promise(res => {
        rep.innerHTML = opts.map((o, i) => `<button type="button" class="hp-rep" data-i="${i}">${E(o.w)}</button>`).join('');
        rep.querySelectorAll('.hp-rep').forEach(x => x.onclick = () => { rep.innerHTML = ''; res(opts[+x.dataset.i]); });
      });
      (async () => {
        await say(p.m1);
        const a = await ask(p.t1); await say(a.w, true); score += a.s; setMood(mood + (a.s ? 2 : -1));
        await say(a.s ? p.m2 : 'Oh… okay. ' + p.m2);
        const b2 = await ask(p.t2); await say(b2.w, true); score += b2.s; setMood(mood + (b2.s ? 1 : -1));
        await say(b2.s ? 'Thanks. That really helps 💛' : 'Hmm… never mind.');
        const ok = score === 6;
        done(ok, `${a.s ? '✓ ' : '✗ '}${a.why} ${b2.s ? '✓ ' : '✗ '}${b2.why}`, null, score / 6);
      })();
    };

    X.paths = (host, p, done) => {
      let k = 0, good = 0; const log = [];
      host.innerHTML = `<div class="hp-ptitle">📖 ${E(p.title)}</div><div class="hp-trail">${p.steps.map((_, i) => `<i data-p="${i}"></i>`).join('')}</div><div class="hp-scene"></div>`;
      const scene = $1('.hp-scene', host);
      const step = () => {
        const st = p.steps[k];
        scene.innerHTML = `<div class="hp-sit">${E(st.sit)}</div><p class="pl-q">What do you do?</p><div class="hp-opts col">${st.opts.map((o, i) => `<button type="button" class="hp-opt" data-i="${i}">${E(o.w)}</button>`).join('')}</div>`;
        scene.querySelectorAll('.hp-opt').forEach(x => x.onclick = () => {
          const o = st.opts[+x.dataset.i]; if (o.best) good++; log.push(o);
          host.querySelector(`[data-p="${k}"]`).className = o.best ? 'y' : 'n';
          scene.querySelectorAll('.hp-opt').forEach(y => { y.disabled = true; if (st.opts[+y.dataset.i].best) y.classList.add('ok'); });
          if (!o.best) x.classList.add('no');
          S(o.best ? 'right' : 'wrong');
          scene.insertAdjacentHTML('beforeend', `<div class="hp-res ${o.best ? 'ok' : 'no'}">${o.best ? '✨' : '⚠️'} ${E(o.res)}${o.best ? '' : `<br><small>Better choice: ${E(st.opts.find(z => z.best).w)}</small>`}</div><button type="button" class="btn hp-go">${k + 1 < p.steps.length ? 'Continue the story ▶' : 'Finish story'}</button>`);
          $1('.hp-go', scene).onclick = () => { S('tap'); k++; if (k < p.steps.length) step(); else end(); };
        });
      };
      const end = () => {
        scene.innerHTML = `<div class="hp-sit">${good === p.steps.length ? '🌈 Best ending! Every choice was calm, kind and wise.' : `You made ${good} of ${p.steps.length} best choices.`}</div>`;
        done(good === p.steps.length, 'Wise choices usually: pause before reacting, take responsibility, and think about how others will feel.', null, good / p.steps.length);
      };
      step();
    };

    X.breathe = (host, p, done) => {
      const total = p.cycles * (p.inh + p.exh);
      host.innerHTML = `<p class="pl-q">${P().band() === 'j' ? 'Press and HOLD while the bubble grows. Let go while it shrinks.' : 'Hold the button while the bubble grows (breathe in), let go while it shrinks (breathe out).'}</p>
        <div class="hp-bwrap"><div class="hp-bubble"></div><div class="hp-blabel">Get ready…</div></div><div class="hp-sync"><i></i></div><button type="button" class="hp-hold">🫧 Hold</button><p class="sub hp-bnote">${p.cycles} breaths · in ${p.inh}s · out ${p.exh}s</p>`;
      const bub = $1('.hp-bubble', host), lab = $1('.hp-blabel', host), sync = $1('.hp-sync i', host), btn = $1('.hp-hold', host);
      let held = false, good = 0, all = 0, t0 = 0, raf = 0, over = false;
      const down = e => { e.preventDefault(); held = true; btn.classList.add('on'); }, up = () => { held = false; btn.classList.remove('on'); };
      btn.addEventListener('pointerdown', down); ['pointerup', 'pointerleave', 'pointercancel'].forEach(ev => btn.addEventListener(ev, up));
      btn.addEventListener('keydown', e => { if (e.key === ' ' || e.key === 'Enter') down(e); }); btn.addEventListener('keyup', up);
      const tick = now => {
        if (!host.isConnected) return cancelAnimationFrame(raf);
        const t = (now - t0) / 1000;
        if (t >= total) return finish();
        const c = t % (p.inh + p.exh), inPh = c < p.inh, f = inPh ? c / p.inh : 1 - (c - p.inh) / p.exh;
        bub.style.transform = `scale(${0.35 + 0.65 * f})`; lab.textContent = inPh ? 'Breathe in…' : 'Breathe out…';
        const edge = Math.min(c, Math.abs(c - p.inh), (p.inh + p.exh) - c) < p.tol / 2;   // short grace time at each switch
        if (!edge) { all++; if (held === inPh) good++; }
        const r = all ? good / all : 0; sync.style.width = `${Math.round(r * 100)}%`; bub.classList.toggle('sync', held === inPh);
        raf = requestAnimationFrame(tick);
      };
      let n = 3; lab.textContent = 'Starting in 3…';
      const cd = setInterval(() => { if (!host.isConnected) return clearInterval(cd); n--; if (n > 0) lab.textContent = `Starting in ${n}…`; else { clearInterval(cd); t0 = performance.now(); raf = requestAnimationFrame(tick); } }, 800);
      function finish() {
        if (over) return; over = true; cancelAnimationFrame(raf); btn.disabled = true; lab.textContent = 'Well done 🌿';
        const r = all ? good / all : 0, ok = r >= 0.7;
        done(ok, `You breathed in time with the bubble ${Math.round(r * 100)}% of the time. Slow breathing — especially a long breath out — tells your body it is safe, which calms big feelings.`, null, Math.min(1, r / 0.85));
      }
    };
  }

  function style() {
    if (D.getElementById('hpCss')) return;
    D.head.insertAdjacentHTML('beforeend', `<style id="hpCss">
      .hp-j{--plh:linear-gradient(135deg,#ff7eb3,#ffd166);--plc:#ff4f8b}.hp-m{--plh:linear-gradient(135deg,#ff7a59,#8e44ad);--plc:#c2410c}.hp-s{--plh:linear-gradient(135deg,#3b1d4a,#0f3d4a);--plc:#e0408f}
      .hp-stage{display:flex;justify-content:center}.hp-facebtn{border:0;background:radial-gradient(circle,#fff6e0,transparent 70%);border-radius:50%;cursor:pointer;padding:6px;animation:mpPop .5s both}.hp-facebtn.wig{animation:plHit .4s}
      .hp-face .hp-eyes{animation:hpBlink 4s infinite;transform-origin:50px 46px}.hp-tear{animation:hpTear 1.8s infinite}
      .hp-face.neutral{display:inline-block}.hp-story{display:flex;gap:10px;align-items:flex-start}.hp-av{flex:none}
      .hp-opts{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}.hp-opts.col{grid-template-columns:1fr}
      .hp-opt{border:2px solid rgba(0,0,0,.1);border-radius:14px;background:#fff;padding:12px;font-size:16px;font-weight:700;cursor:pointer;font-family:inherit;color:#1f2d33;display:flex;gap:8px;align-items:center;justify-content:center;text-align:left;line-height:1.3}
      .hp-opts.col .hp-opt{justify-content:flex-start}.hp-opt span{font-size:26px}.hp-opt.ok{border-color:#1e9e6a;background:#e6f7ef}.hp-opt.no{border-color:#e45;background:#fdeaea;animation:mgShake .4s}
      .hp-thermo{display:flex;gap:12px;justify-content:center;align-items:stretch;margin:8px 0}.hp-tube{width:26px;border-radius:14px;background:#eee;position:relative;overflow:hidden;box-shadow:inset 0 0 0 2px #ddd}
      .hp-merc{position:absolute;left:0;right:0;bottom:0;background:linear-gradient(0deg,#ffd166,#ff7a59,#e63946);transition:height .5s cubic-bezier(.3,1.5,.5,1)}
      .hp-slots{display:flex;flex-direction:column;gap:8px;flex:1;max-width:240px}.hp-slot{border:2px dashed var(--plc);border-radius:12px;background:#fff;padding:10px;text-align:left;font-weight:800;font-size:16px;cursor:pointer;color:#1f2d33;font-family:inherit}
      .hp-slot small{display:block;font-size:11px;color:#889;font-weight:700}.hp-slot.full{border-style:solid;background:#fff6dc}.hp-slot.ok{background:#e6f7ef;border-color:#1e9e6a}.hp-slot.no{background:#fdeaea;border-color:#e45}.hp-slot i{color:#1e9e6a;font-style:normal}
      .hp-tiles,.hp-stickers{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:10px 0}
      .hp-tile{border:0;border-radius:999px;padding:10px 16px;background:var(--plc);color:#fff;font-weight:800;font-size:16px;cursor:pointer;font-family:inherit;box-shadow:0 4px 0 rgba(0,0,0,.2);animation:mpPop .3s both}.hp-tile span{margin-right:4px}.hp-tile.used{visibility:hidden}
      .hp-event{padding:12px;border-radius:14px;background:linear-gradient(135deg,#fff3e0,#ffe0ec);font-weight:700;line-height:1.4;color:#3a2a20}
      .hp-roles{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px}.hp-role{border:2px solid rgba(0,0,0,.08);border-radius:16px;background:#fff;padding:10px;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:6px;font-family:inherit;color:#1f2d33}
      .hp-who{font-weight:800;font-size:14px;text-align:center}.hp-drop{width:70px;height:70px;border-radius:50%;border:2px dashed var(--plc);display:grid;place-items:center;font-size:30px;line-height:1}.hp-drop small{display:block;font-size:10px}
      .hp-role.ok{border-color:#1e9e6a;background:#e6f7ef}.hp-role.no{border-color:#e45;background:#fdeaea}.hp-fix{font-size:11px;color:#1e9e6a}
      .hp-stk{border:0;border-radius:14px;background:#fff;padding:6px 10px;cursor:pointer;display:flex;flex-direction:column;align-items:center;box-shadow:0 3px 10px rgba(0,0,0,.12);font-family:inherit;color:#1f2d33}.hp-stk span{font-size:28px}.hp-stk small{font-size:11px;font-weight:700}
      .hp-stk.held{outline:3px solid var(--plc);transform:translateY(-4px) rotate(-4deg)}.hp-stk.used{opacity:.35}
      .hp-phone{border-radius:24px;background:#eef2f7;padding:0 0 10px;overflow:hidden;box-shadow:0 0 0 6px #1f2540}.hp-ph-top{display:flex;align-items:center;gap:8px;background:#1f2540;color:#fff;padding:10px 12px}
      .hp-ph-av{width:32px;height:32px;border-radius:50%;background:var(--plc);display:grid;place-items:center;font-weight:900}.hp-mood{margin-left:auto;font-size:28px}.hp-mood.bump{animation:plHit .5s}
      .hp-msgs{min-height:170px;max-height:300px;overflow:auto;display:flex;flex-direction:column;gap:6px;padding:10px}
      .hp-b{max-width:80%;padding:9px 12px;border-radius:16px 16px 16px 4px;background:#fff;color:#1f2d33;box-shadow:0 1px 2px rgba(0,0,0,.08);animation:mpPop .25s both;line-height:1.35}
      .hp-b.me{align-self:flex-end;border-radius:16px 16px 4px 16px;background:#d6f5e6}.hp-b.typing{display:flex;gap:4px}.hp-b.typing i{width:7px;height:7px;border-radius:50%;background:#99a;animation:hpDot 1s infinite}.hp-b.typing i:nth-child(2){animation-delay:.15s}.hp-b.typing i:nth-child(3){animation-delay:.3s}
      .hp-replies{display:flex;flex-direction:column;gap:6px;padding:0 10px}.hp-rep{border:2px solid var(--plc);border-radius:999px;background:#fff;color:#1f2d33;padding:9px 12px;text-align:left;cursor:pointer;font-family:inherit;font-size:14px;animation:mpPop .3s both}
      .hp-ptitle{font-weight:900;font-size:17px;color:var(--plc)}.hp-trail{display:flex;gap:6px;margin:6px 0 10px}.hp-trail i{flex:1;height:8px;border-radius:9px;background:rgba(0,0,0,.1)}.hp-trail .y{background:#1e9e6a}.hp-trail .n{background:#f4a261}
      .hp-sit{padding:12px;border-radius:14px;background:#f4f0ff;font-weight:700;line-height:1.45;color:#2a2350;animation:mpPop .35s both}
      .hp-res{margin:10px 0;padding:10px;border-radius:12px;font-weight:700;animation:mpPop .3s both}.hp-res.ok{background:#e6f7ef;color:#14532d}.hp-res.no{background:#fff1e0;color:#7c2d12}.hp-res small{font-weight:600}
      .hp-bwrap{position:relative;height:220px;display:grid;place-items:center}.hp-bubble{width:200px;height:200px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,#9ad7ff 40%,#5aa9e6);box-shadow:0 0 30px #9ad7ff;transform:scale(.35);transition:background .3s}
      .hp-bubble.sync{background:radial-gradient(circle at 35% 30%,#fff,#a8f0c6 40%,#3cbf7f);box-shadow:0 0 34px #7ee0a8}.hp-blabel{position:absolute;font-weight:900;font-size:20px;color:#1f2d33;text-shadow:0 1px 0 #fff}
      .hp-sync{height:8px;border-radius:9px;background:rgba(0,0,0,.08);overflow:hidden;margin:6px 0}.hp-sync i{display:block;height:100%;width:0;background:#3cbf7f;transition:width .2s}
      .hp-hold{display:block;width:100%;border:0;border-radius:20px;padding:20px;font-size:22px;font-weight:900;background:var(--plc);color:#fff;cursor:pointer;touch-action:none;user-select:none;-webkit-user-select:none;font-family:inherit;box-shadow:0 6px 0 rgba(0,0,0,.2)}
      .hp-hold.on{transform:translateY(4px);box-shadow:0 2px 0 rgba(0,0,0,.2);filter:brightness(1.1)}.hp-bnote{text-align:center}
      .pl-s .hp-opt,.pl-s .hp-slot,.pl-s .hp-role,.pl-s .hp-stk,.pl-s .hp-rep{background:#232a48;color:#eef}.pl-s .hp-event,.pl-s .hp-sit{background:#2a2350;color:#f3eaff}.pl-s .hp-blabel{color:#fff;text-shadow:none}
      @keyframes hpBlink{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.1)}}@keyframes hpTear{0%{transform:translateY(0);opacity:1}100%{transform:translateY(14px);opacity:0}}@keyframes hpDot{50%{transform:translateY(-4px)}}
    </style>`);
  }

  function boot() {
    if (!window.MindPlay || !window.HeartPlayGen) return setTimeout(boot, 200);
    setup(); style();
    MindPlay.addSuite({ id: 'eq', test: 'eq', theme: THEME, games: GAMES, gen: () => window.HeartPlayGen, back: () => window.MindGym.open(), backLabel: 'Mind Gym', store: 'htests', kind: g => g.skill });
  }
  boot();
  window.HeartPlay = { face };
})();
