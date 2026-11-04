/* StudyVerse lab: storysequence — put story / life-cycle / routine panels in the right order
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *  title      string  heading of the sequence (any language)                          default 'Story'
 *  panels     array   panels in the CORRECT order. Each item is { e:'🐦', t:'The crow was thirsty' }
 *                     or ['🐦', 'The crow was thirsty'] (e = emoji(s), t = short caption).
 *                     3–7 panels work best.                                            default Thirsty Crow
 *  stories    array   optional extra sets [{ title, panels }, …]; "New" cycles through them  default none
 *  kind       string  'story' | 'cycle' (life cycle: last step leads back to the first) |
 *                     'routine' — changes small labels and the ending                  default 'story'
 *  speak      boolean read a panel aloud when it is tapped                              default true
 *  challenge  string  the "🎯 Challenge" line                                           default auto
 *
 * The child: drags cards up/down (or taps one card, then another, to swap them); each tap reads the
 * caption aloud. Numbers on the left show the position. "Check" colours cards green (right place) or
 * red. When every card is in place, api.win() is called and the whole sequence is read in order.
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const norm = arr => (Array.isArray(arr) ? arr : []).map(x => Array.isArray(x) ? { e: x[0] || '', t: x[1] || '' } : (x && typeof x === 'object' ? { e: x.e || x.emoji || '', t: x.t || x.text || x.caption || '' } : { e: '', t: String(x || '') })).filter(x => x.e || x.t).slice(0, 8);

  Labs.register('storysequence', {
    title: 'Story order',
    subjects: ['english', 'hindi', 'evs', 'science'],
    render(host, p, api) {
      const sets = [];
      const first = norm(p.panels); if (first.length >= 2) sets.push({ title: p.title || 'Story', panels: first });
      (Array.isArray(p.stories) ? p.stories : []).forEach(s => { const ps = norm(s && s.panels); if (ps.length >= 2) sets.push({ title: (s && s.title) || 'Story', panels: ps }); });
      if (!sets.length) { const ex = Labs.registry.storysequence.example; sets.push({ title: ex.title, panels: norm(ex.panels) }); }
      const kind = ['story', 'cycle', 'routine'].includes(p.kind) ? p.kind : 'story';
      const doSpeak = p.speak !== false;
      const defCh = kind === 'cycle' ? 'Put the life cycle in the right order' : kind === 'routine' ? 'Put the day in the right order' : 'Put the story in the right order';
      const timers = []; const later = (f, ms) => timers.push(setTimeout(f, ms));
      const H = 58, G = 6;
      const TIP = 'Drag a card ↕ or tap two cards to swap them';
      const SEG = (typeof Intl !== 'undefined' && Intl.Segmenter) ? new Intl.Segmenter('en', { granularity: 'grapheme' }) : null;
      const ecount = t => SEG ? Array.from(SEG.segment(String(t))).length : Array.from(String(t)).length;                                              // card height, gap

      host.innerHTML = `<style>
.lb-storysequence-w{color:#1b1f3a;font-size:15px;user-select:none;-webkit-user-select:none}
.lb-storysequence-ch{font-weight:800;margin:0 0 6px;line-height:1.3}
.lb-storysequence-hd{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:6px}
.lb-storysequence-tt{font-weight:800;font-size:16px;color:#8b5cf6}
.lb-storysequence-tip{font-size:12px;font-weight:700;color:#6b7090}
.lb-storysequence-wrap{display:flex;gap:6px}
.lb-storysequence-nums{width:30px;flex:none;position:relative}
.lb-storysequence-num{position:absolute;left:0;width:30px;height:${H}px;display:flex;align-items:center;justify-content:center;font-weight:800;color:#b3a4e6;font-size:16px}
.lb-storysequence-num i{width:26px;height:26px;border-radius:50%;background:#f1effb;display:flex;align-items:center;justify-content:center;font-style:normal}
.lb-storysequence-list{position:relative;flex:1;touch-action:none}
.lb-storysequence-card{position:absolute;left:0;right:0;height:${H}px;display:flex;align-items:center;gap:8px;background:#fff;border-radius:16px;padding:0 8px 0 6px;box-shadow:0 2px 0 #e6e3f5,inset 0 0 0 2px #efedf9;transition:top .25s cubic-bezier(.3,1.2,.5,1),box-shadow .2s,background .25s;cursor:grab;touch-action:none}
.lb-storysequence-card.drag{transition:box-shadow .2s;z-index:5;box-shadow:0 10px 22px rgba(27,31,58,.18),inset 0 0 0 2px #8b5cf6;cursor:grabbing}
.lb-storysequence-card.sel{box-shadow:0 0 0 3px #ffc93c,0 2px 0 #e6e3f5}
.lb-storysequence-card.ok{background:#e3fbf3;box-shadow:inset 0 0 0 2px #2ed3a5}
.lb-storysequence-card.no{background:#fff0f0;box-shadow:inset 0 0 0 2px #ff6b6b;animation:lb-storysequence-shk .4s}
@keyframes lb-storysequence-shk{25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
.lb-storysequence-emo{white-space:nowrap;width:46px;height:46px;flex:none;border-radius:12px;background:#fffaf0;display:flex;align-items:center;justify-content:center;font-size:24px;letter-spacing:-2px;overflow:hidden}
.lb-storysequence-tx{flex:1;font-weight:700;font-size:14px;line-height:1.25;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.lb-storysequence-hn{color:#c9c6dd;font-size:18px;flex:none;letter-spacing:-3px}
.lb-storysequence-cyc{text-align:center;font-weight:800;color:#2ed3a5;font-size:13px;height:0;opacity:0;transition:opacity .4s;overflow:hidden}
.lb-storysequence-cyc.show{height:auto;opacity:1;margin-top:4px}
.lb-storysequence-bar{display:flex;gap:6px;margin-top:10px}
.lb-storysequence-btn{flex:1;border:0;border-radius:14px;min-height:42px;font:inherit;font-weight:800;cursor:pointer;background:#f1effb;color:#8b5cf6}
.lb-storysequence-btn.go{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #6d3fd6}
.lb-storysequence-msg{text-align:center;font-weight:800;font-size:13px;min-height:18px;margin-top:6px;color:#6b7090}
</style>
<div class="lb-storysequence-w">
  <div class="lb-storysequence-ch">🎯 Challenge: ${esc(p.challenge || defCh)}</div>
  <div class="lb-storysequence-hd"><span class="lb-storysequence-tt"></span></div>
  <div class="lb-storysequence-wrap"><div class="lb-storysequence-nums"></div><div class="lb-storysequence-list"></div></div>
  <div class="lb-storysequence-cyc">↻ ${kind === 'cycle' ? 'and the cycle starts again!' : ''}</div>
  <div class="lb-storysequence-msg"></div>
  <div class="lb-storysequence-bar"><button class="lb-storysequence-btn go lb-storysequence-chk">✔ Check</button><button class="lb-storysequence-btn lb-storysequence-read">🔊 Read</button><button class="lb-storysequence-btn lb-storysequence-new">🔀 ${sets.length > 1 ? 'Next' : 'Mix'}</button></div>
</div>`;
      const $ = s => host.querySelector(s);
      const list = $('.lb-storysequence-list'), nums = $('.lb-storysequence-nums'), msg = $('.lb-storysequence-msg'), cyc = $('.lb-storysequence-cyc');
      let si = 0, order = [], cards = [], sel = null, done = false, won = false;
      const top = i => i * (H + G);

      function layout(skip) { order.forEach((ci, pos) => { if (cards[ci] !== skip) cards[ci].style.top = top(pos) + 'px'; }); }
      function clearMarks() { cards.forEach(c => c.classList.remove('ok', 'no')); if (!done) msg.textContent = TIP; }
      function load(k) {
        si = k; const S = sets[si]; const n = S.panels.length;
        $('.lb-storysequence-tt').textContent = S.title;
        list.style.height = nums.style.height = (top(n) - G) + 'px';
        nums.innerHTML = S.panels.map((_, i) => `<div class="lb-storysequence-num" style="top:${top(i)}px"><i>${i + 1}</i></div>`).join('');
        list.innerHTML = S.panels.map((x, i) => `<div class="lb-storysequence-card" data-i="${i}"><div class="lb-storysequence-emo" style="font-size:${ecount(x.e || '•') > 1 ? 17 : 26}px">${esc(x.e || '•')}</div><div class="lb-storysequence-tx">${esc(x.t)}</div><span class="lb-storysequence-hn">⋮⋮</span></div>`).join('');
        cards = Array.from(list.children);
        do { order = shuffle(S.panels.map((_, i) => i)); } while (n > 1 && order.every((v, i) => v === i));
        done = false; sel = null; msg.textContent = TIP; cyc.classList.remove('show');
        cards.forEach(bind); layout();
      }
      const inPlace = () => order.filter((v, i) => v === i).length;
      function afterMove() {
        clearMarks();
        if (!done && inPlace() === order.length) finish();
      }
      function finish() {
        done = true; cards.forEach(c => c.classList.add('ok')); api.sfx('correct');
        msg.textContent = 'Perfect order! 🌟';
        if (kind === 'cycle') cyc.classList.add('show');
        if (!won) { won = true; later(() => api.win(`You put all ${order.length} steps of "${sets[si].title}" in order!`), 400); }
        later(readAll, 600);
      }
      function readAll() { if (doSpeak) api.speak(order.map(ci => sets[si].panels[ci].t).join('. ')); }
      function swap(a, b) { const ia = order.indexOf(a), ib = order.indexOf(b); order[ia] = b; order[ib] = a; layout(); }

      function bind(card) {
        const ci = +card.dataset.i; let st = null;
        card.addEventListener('pointerdown', e => {
          if (done) return;
          st = { y: e.clientY, pos: order.indexOf(ci), moved: false };
          try { card.setPointerCapture(e.pointerId); } catch (_) {}
        });
        card.addEventListener('pointermove', e => {
          if (!st) return;
          const dy = e.clientY - st.y;
          if (!st.moved && Math.abs(dy) < 6) return;
          if (!st.moved) { st.moved = true; card.classList.add('drag'); if (sel) { sel.classList.remove('sel'); sel = null; } clearMarks(); }
          const n = order.length;
          const y = Math.max(-10, Math.min(top(n - 1) + 10, top(st.pos) + dy));
          card.style.top = y + 'px';
          const np = Math.max(0, Math.min(n - 1, Math.round(y / (H + G))));
          const cur = order.indexOf(ci);
          if (np !== cur) { order.splice(cur, 1); order.splice(np, 0, ci); layout(card); api.sfx('tap'); }
        });
        const end = () => {
          if (!st) return; const moved = st.moved; st = null;
          card.classList.remove('drag'); layout();
          if (moved) { afterMove(); return; }
          // tap: read aloud + tap-to-swap
          if (doSpeak) api.speak(sets[si].panels[ci].t);
          if (done) return;
          if (!sel) { sel = card; card.classList.add('sel'); api.sfx('tap'); }
          else if (sel === card) { sel.classList.remove('sel'); sel = null; }
          else { const other = +sel.dataset.i; sel.classList.remove('sel'); sel = null; swap(other, ci); api.sfx('tap'); afterMove(); }
        };
        card.addEventListener('pointerup', end); card.addEventListener('pointercancel', end);
      }
      $('.lb-storysequence-chk').onclick = () => {
        if (done) { readAll(); return; }
        const k = inPlace();
        order.forEach((ci, pos) => { const c = cards[ci]; c.classList.remove('ok', 'no'); void c.offsetWidth; c.classList.add(ci === pos ? 'ok' : 'no'); });
        api.sfx(k === order.length ? 'correct' : 'hmm');
        msg.textContent = k === order.length ? '' : `${k} of ${order.length} in the right place — move the red ones`;
        if (k === order.length) finish();
      };
      $('.lb-storysequence-read').onclick = () => { api.sfx('tap'); readAll(); };
      $('.lb-storysequence-new').onclick = () => { api.sfx('tap'); load((si + 1) % sets.length); };
      load(0);
      return () => { timers.forEach(clearTimeout); host.innerHTML = ''; };
    },
    example: {
      title: 'The Thirsty Crow', kind: 'story',
      challenge: 'Put the story of the thirsty crow in order',
      panels: [
        { e: '🐦☀️', t: 'On a hot day, a crow felt very thirsty.' },
        { e: '🏺', t: 'It found a pot with a little water at the bottom.' },
        { e: '🪨', t: 'It dropped pebbles into the pot, one by one.' },
        { e: '💧', t: 'The water slowly rose up to the top.' },
        { e: '😊', t: 'The crow drank the water and flew away happily.' }
      ]
    },
    examples: [
      { title: 'पौधे का जीवन चक्र', kind: 'cycle', challenge: 'बीज से पेड़ — क्रम से लगाओ',
        panels: [['🌰', 'बीज मिट्टी में बोया गया'], ['🌱', 'बीज से अंकुर निकला'], ['🌿', 'अंकुर बढ़कर पौधा बना'], ['🌸', 'पौधे पर फूल आए'], ['🍎', 'फूल से फल बना — फल में नए बीज']] },
      { title: 'Life cycle of a butterfly', kind: 'cycle', challenge: 'Order the 4 stages of a butterfly',
        panels: [['🥚', 'Egg — laid on a leaf'], ['🐛', 'Larva (caterpillar) — eats leaves and grows'], ['🛌', 'Pupa — rests inside a hard case (chrysalis)'], ['🦋', 'Adult butterfly comes out and lays eggs']],
        stories: [{ title: 'Life cycle of a frog', panels: [['🫧', 'Eggs (frogspawn) in water'], ['🐟', 'Tadpole with a tail swims'], ['🦵', 'Froglet grows legs, tail shrinks'], ['🐸', 'Adult frog lives on land and in water']] }] },
      { title: 'My morning', kind: 'routine', challenge: 'What do you do first? Put your morning in order',
        panels: [['⏰', 'I wake up'], ['🪥', 'I brush my teeth'], ['🛁', 'I take a bath'], ['🥣', 'I eat breakfast'], ['🎒', 'I go to school']] }
    ]
  });
})();
