/* Knowtopia lab: sortbins — drag (or tap, then tap a bin) cards into 2–4 labelled bins
 *
 * PARAMS (all optional; if `items` is missing/invalid a built-in wet/dry waste set is used)
 *  title      string   heading shown above the cards (any language)                     default ''
 *  challenge  string   the "🎯 Challenge" line                                            default auto ('Sort every card into the right bin')
 *  bins       array    2–4 bins: [{ name:'Wet waste', emoji:'🍌', color:'#2ed3a5' }, …]
 *                      or plain strings ['Wet', 'Dry']. color = any CSS hex colour.      default palette colours
 *  items      array    cards: [{ text:'Banana peel', emoji:'🍌', bin:0, why:'It rots…' }, …]
 *                      bin = bin index (0-based) or the bin's name. Also accepts
 *                      ['Banana peel', 0, 'why…'] arrays. Up to 12 cards.                 default waste set
 *  shuffle    boolean  mix the card order                                                default true
 *  showWhy    boolean  show an item's `why` when it is placed wrong / after the win      default true
 *  mode       string   'sort'  = instant feedback on every drop (wrong drops shake back)
 *                      'check' = place every card first, then press ✔ Check             default 'sort'
 *  speak      boolean  read a card aloud when it is tapped                               default false
 *
 * The child drags a card onto a bin (or taps a card, then taps a bin). In 'sort' mode a right drop
 * locks the card inside the bin, a wrong drop shakes the card back and shows its `why`. In 'check'
 * mode cards can be moved freely (tap a placed card, then another bin or the card tray); ✔ Check
 * locks right cards and sends wrong ones back with reasons. Win = every card in its correct bin.
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const mix = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const PAL = ['#8b5cf6', '#2ed3a5', '#ff9f1c', '#3b82f6'];
  const tint = (c, a) => { const m = /^#?([0-9a-f]{6}|[0-9a-f]{3})$/i.exec(String(c || '').trim()); if (!m) return null; let h = m[1]; if (h.length === 3) h = h.split('').map(x => x + x).join(''); const n = parseInt(h, 16); return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`; };
  const key = s => String(s == null ? '' : s).trim().toLowerCase();

  function normBins(arr) {
    return (Array.isArray(arr) ? arr : []).map((b, i) => {
      if (b == null) return null;
      if (typeof b !== 'object') b = { name: String(b) };
      const name = String(b.name || b.label || b.title || b.t || '').trim(); if (!name) return null;
      const color = tint(b.color, 1) ? String(b.color).trim() : PAL[i % PAL.length];
      return { name, emoji: String(b.emoji || b.e || ''), color };
    }).filter(Boolean).slice(0, 4);
  }
  function normItems(arr, bins) {
    const find = v => {
      if (typeof v === 'number' || (typeof v === 'string' && /^\s*\d+\s*$/.test(v))) { const n = +v; return n >= 0 && n < bins.length ? n : -1; }
      const k = key(v); return bins.findIndex(b => key(b.name) === k || (b.emoji && key(b.emoji) === k));
    };
    return (Array.isArray(arr) ? arr : []).map(x => {
      if (Array.isArray(x)) x = { text: x[0], bin: x[1], why: x[2] };
      if (!x || typeof x !== 'object') return null;
      const text = String(x.text || x.t || x.name || '').trim(); const emoji = String(x.emoji || x.e || '');
      if (!text && !emoji) return null;
      const bin = find(x.bin != null ? x.bin : x.b); if (bin < 0) return null;
      return { text, emoji, bin, why: String(x.why || x.reason || '').trim() };
    }).filter(Boolean).slice(0, 12);
  }

  Labs.register('sortbins', {
    title: 'Sort into bins',
    subjects: ['evs', 'science', 'social', 'english', 'hindi', 'sanskrit', 'maths'],
    render(host, p, api) {
      p = p || {};
      let bins = normBins(p.bins), items = bins.length >= 2 ? normItems(p.items, bins) : [];
      let custom = true;
      if (bins.length < 2 || items.length < 2) {           // fall back to the built-in set (with its own default goal)
        const ex = Labs.registry.sortbins.example; bins = normBins(ex.bins); items = normItems(ex.items, bins); custom = false;
      }
      const mode = p.mode === 'check' ? 'check' : 'sort';
      const showWhy = p.showWhy !== false, doShuffle = p.shuffle !== false, doSpeak = p.speak === true;
      const N = items.length, B = bins.length;
      const challenge = (custom && p.challenge) || `Sort every card into the right bin${B === 2 ? ` — ${bins[0].name} or ${bins[1].name}?` : ''}`;
      const title = custom ? (p.title || '') : '';
      const cols = B === 3 ? 3 : 2;
      const timers = []; const later = (f, ms) => timers.push(setTimeout(f, ms));
      const T = 'lb-sortbins-';

      host.innerHTML = `<style>
.${T}w{color:#1b1f3a;font-size:15px;user-select:none;-webkit-user-select:none}
.${T}ch{font-weight:800;margin:0 0 4px;line-height:1.35}
.${T}tt{font-weight:800;font-size:15px;color:#8b5cf6;margin-bottom:4px;line-height:1.35}
.${T}stat{display:flex;justify-content:space-between;font-size:12px;font-weight:800;color:#6b7090;margin:2px 2px 6px}
.${T}tray{min-height:52px;display:flex;flex-wrap:wrap;gap:6px;padding:8px;border-radius:16px;background:#f6f5fc;border:2px dashed #dcd8f0;align-content:flex-start;transition:background .2s,border-color .2s}
.${T}tray.over{background:#efeafe;border-color:#8b5cf6}
.${T}tray.empty{justify-content:center;align-items:center}
.${T}tray.gone{display:none}
.${T}tray-e{font-size:12px;font-weight:700;color:#a5a8c0}
.${T}card{display:inline-flex;align-items:center;gap:5px;max-width:100%;min-height:40px;box-sizing:border-box;padding:6px 11px;border-radius:13px;background:#fff;box-shadow:0 2px 0 #e2def3,inset 0 0 0 2px #ebe8f8;font-weight:700;font-size:14px;line-height:1.35;cursor:grab;touch-action:none;transition:box-shadow .2s,background .2s,opacity .2s,transform .15s;overflow-wrap:break-word;word-break:normal}
.${T}card .e{font-size:19px;line-height:1;flex:none}
.${T}card .x{min-width:0}
.${T}card.sel{box-shadow:0 0 0 3px #ffc93c,0 2px 0 #e2def3;transform:translateY(-2px)}
.${T}card.lift{opacity:.3}
.${T}card.ok{background:#e3fbf3;box-shadow:inset 0 0 0 2px #2ed3a5;cursor:pointer}
.${T}card.no{background:#fff0f0;box-shadow:inset 0 0 0 2px #ff6b6b}
.${T}card.shk{animation:${T}shk .45s}
.${T}card.pop{animation:${T}pop .35s}
.${T}in .${T}card{font-size:12.5px;min-height:34px;padding:4px 8px;border-radius:11px;width:100%}
.${T}in .${T}card .e{font-size:16px}
@keyframes ${T}shk{20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(4px)}}
@keyframes ${T}pop{0%{transform:scale(.6)}70%{transform:scale(1.08)}100%{transform:scale(1)}}
.${T}ghost{position:fixed;z-index:9999;pointer-events:none;margin:0;opacity:.95;transform:rotate(-3deg) scale(1.05);box-shadow:0 12px 26px rgba(27,31,58,.25),inset 0 0 0 2px #8b5cf6 !important;font-family:inherit}
.${T}bins{display:grid;gap:7px;margin-top:9px}
.${T}bin{border-radius:16px;padding:6px 6px 7px;min-height:96px;border:2px solid var(--c);background:var(--t);display:flex;flex-direction:column;transition:transform .15s,box-shadow .2s;cursor:pointer;min-width:0}
.${T}bin.over{transform:scale(1.03);box-shadow:0 0 0 3px var(--c)}
.${T}bin.cue{box-shadow:0 0 0 2px #ffc93c}
.${T}bin.bad{animation:${T}bad .5s}
@keyframes ${T}bad{30%{box-shadow:0 0 0 4px #ff6b6b}}
.${T}bh{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:2px 6px;text-align:center;font-weight:800;font-size:13.5px;color:var(--c);line-height:1.3;padding:2px 2px 5px;overflow-wrap:break-word;hyphens:auto}
.${T}bh .n{flex-basis:100%;order:3;min-width:0}
.${T}bh .e{font-size:20px;line-height:1;flex:none}
.${T}bh .n{color:#1b1f3a}
.${T}bh .k{flex:none;font-size:11px;font-weight:800;color:#fff;background:var(--c);border-radius:9px;padding:1px 6px}
.${T}in{display:flex;flex-direction:column;gap:4px;flex:1}
.${T}fb{margin-top:8px;min-height:40px;border-radius:14px;padding:8px 11px;font-size:13px;font-weight:700;line-height:1.4;background:#f6f5fc;color:#6b7090;transition:background .25s,color .25s}
.${T}fb.good{background:#e3fbf3;color:#11795d}
.${T}fb.bad{background:#fff0f0;color:#c0392b}
.${T}fb.win{background:#fff6d6;color:#8a5a00}
.${T}bar{display:flex;gap:6px;margin-top:8px}
.${T}btn{flex:1;border:0;border-radius:14px;min-height:42px;font:inherit;font-weight:800;font-size:14px;cursor:pointer;background:#f1effb;color:#8b5cf6}
.${T}btn.go{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #6d3fd6}
.${T}btn:disabled{opacity:.45;cursor:default}
</style>
<div class="${T}w">
  <div class="${T}ch">🎯 Challenge: ${esc(challenge)}</div>
  ${title ? `<div class="${T}tt">${esc(title)}</div>` : ''}
  <div class="${T}stat"><span class="${T}hint"></span><span class="${T}sc"></span></div>
  <div class="${T}tray"></div>
  <div class="${T}bins" style="grid-template-columns:repeat(${cols},minmax(0,1fr))">${bins.map((b, i) => `<div class="${T}bin" data-b="${i}" style="--c:${esc(b.color)};--t:${tint(b.color, 0.09) || '#f7f7fb'}"><div class="${T}bh">${b.emoji ? `<span class="e">${esc(b.emoji)}</span>` : ''}<span class="n">${esc(b.name)}</span><span class="k">0</span></div><div class="${T}in"></div></div>`).join('')}</div>
  <div class="${T}fb"></div>
  <div class="${T}bar">${mode === 'check' ? `<button class="${T}btn go ${T}chk">✔ Check</button>` : ''}<button class="${T}btn ${T}rst">🔄 Reset</button></div>
</div>`;
      const root = host.querySelector('.' + T + 'w');
      const $ = s => root.querySelector(s);
      const tray = $('.' + T + 'tray'), binEls = Array.from(root.querySelectorAll('.' + T + 'bin')), fb = $('.' + T + 'fb');
      const chk = $('.' + T + 'chk');
      let order, place, locked, seq, sel, mistakes, done, won, ghost = null, st = null;

      const cardHTML = i => { const it = items[i]; return `<div class="${T}card${locked[i] ? ' ok' : ''}${sel === i ? ' sel' : ''}" data-i="${i}">${it.emoji ? `<span class="e">${esc(it.emoji)}</span>` : ''}${it.text ? `<span class="x">${esc(it.text)}</span>` : ''}</div>`; };
      const cardEl = i => root.querySelector(`.${T}card[data-i="${i}"]`);
      function say(html, cls) { fb.className = T + 'fb' + (cls ? ' ' + cls : ''); fb.innerHTML = html; }
      function draw() {
        const left = order.filter(i => place[i] < 0);
        tray.classList.toggle('empty', !left.length); tray.classList.toggle('gone', done);
        tray.innerHTML = left.length ? left.map(cardHTML).join('') : `<span class="${T}tray-e">${done ? '🌟 All sorted!' : mode === 'check' ? 'All cards placed — press ✔ Check' : ''}</span>`;
        binEls.forEach((el, b) => {
          const inB = order.filter(i => place[i] === b).sort((a, c) => seq[a] - seq[c]);
          el.querySelector('.' + T + 'in').innerHTML = inB.map(cardHTML).join('');
          el.querySelector('.k').textContent = inB.length;
          el.classList.toggle('cue', sel != null && !done);
        });
        const right = items.filter((it, i) => locked[i]).length;
        $('.' + T + 'sc').textContent = mode === 'sort' ? `✓ ${right}/${N}${mistakes ? `  ·  ✗ ${mistakes}` : ''}` : `Placed ${items.filter((_, i) => place[i] >= 0).length}/${N}`;
        $('.' + T + 'hint').textContent = done ? 'Tap a card to see why' : sel != null ? 'Now tap a bin 👇' : 'Drag a card, or tap it then a bin';
        if (chk) chk.disabled = done || left.length > 0;
      }
      function anim(i, cls) { const el = cardEl(i); if (el) { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); } }
      function reset() {
        order = doShuffle ? mix(items.map((_, i) => i)) : items.map((_, i) => i);
        place = items.map(() => -1); locked = items.map(() => false); seq = items.map(() => 0);
        sel = null; mistakes = 0; done = false;
        say(mode === 'check' ? 'Place every card in a bin, then press ✔ Check.' : 'Where does each card belong? Drop it in a bin.');
        draw();
      }
      let seqN = 0;
      function whyLine(i) { return showWhy && items[i].why ? ' ' + esc(items[i].why) : ''; }
      function drop(i, b) {
        if (done || locked[i]) return;
        sel = null;
        if (b === 'tray') { if (mode === 'check') { place[i] = -1; api.sfx('tap'); } draw(); return; }
        if (b == null || b < 0) { draw(); return; }
        if (mode === 'sort') {
          if (items[i].bin === b) {
            place[i] = b; locked[i] = true; seq[i] = ++seqN; api.sfx('correct');
            say(`✓ <b>${esc(items[i].text || items[i].emoji)}</b> → ${esc(bins[b].name)}`, 'good');
            draw(); anim(i, 'pop'); winCheck();
          } else {
            mistakes++; api.sfx('wrong');
            say(`✗ <b>${esc(items[i].text || items[i].emoji)}</b> is not in “${esc(bins[b].name)}”.${whyLine(i) || ' Try another bin!'}`, 'bad');
            draw(); anim(i, 'shk'); const be = binEls[b]; be.classList.remove('bad'); void be.offsetWidth; be.classList.add('bad');
          }
        } else {
          place[i] = b; seq[i] = ++seqN; api.sfx('tap');
          const left = items.filter((_, k) => place[k] < 0).length;
          say(left ? `${left} card${left > 1 ? 's' : ''} left to place.` : 'All placed! Press ✔ Check.');
          draw(); anim(i, 'pop');
        }
      }
      function winCheck() {
        if (!locked.every(Boolean)) return;
        done = true; sel = null; draw();
        const extra = mode === 'sort' ? (mistakes ? ` (${mistakes} wrong tr${mistakes > 1 ? 'ies' : 'y'})` : ' with no mistakes') : '';
        say(`🌟 Brilliant! All ${N} cards are in the right bins${extra}.${showWhy && items.some(x => x.why) ? ' Tap any card to see why.' : ''}`, 'win');
        if (!won) { won = true; api.win(`You sorted all ${N} cards correctly${extra}!`); }
      }
      function check() {
        if (done) return;
        const wrong = [];
        items.forEach((it, i) => { if (!locked[i] && place[i] >= 0) { if (it.bin === place[i]) locked[i] = true; else wrong.push(i); } });
        if (!wrong.length) { api.sfx('correct'); winCheck(); return; }
        api.sfx('hmm'); draw();
        wrong.forEach(i => { const el = cardEl(i); if (el) { el.classList.add('no'); anim(i, 'shk'); } });
        const right = locked.filter(Boolean).length;
        const reasons = showWhy ? wrong.filter(i => items[i].why).slice(0, 2).map(i => `<br>• <b>${esc(items[i].text || items[i].emoji)}</b>: ${esc(items[i].why)}`).join('') : '';
        say(`${right} of ${N} right. The red card${wrong.length > 1 ? 's go' : ' goes'} back — try again!${reasons}`, 'bad');
        if (chk) chk.disabled = true;
        later(() => { wrong.forEach(i => { if (!locked[i]) place[i] = -1; }); draw(); }, 1100);
      }
      function tapCard(i) {
        const it = items[i];
        if (!done && sel != null && sel !== i && place[i] >= 0) { drop(sel, place[i]); return; }   // tapped a card inside a bin = tap that bin
        if (doSpeak && it.text) api.speak(it.text);
        if (locked[i]) {        // a right card: show its reason
          if (showWhy && it.why) say(`<b>${esc(it.text || it.emoji)}</b> → ${esc(bins[it.bin].name)}: ${esc(it.why)}`, done ? 'win' : 'good');
          return;
        }
        if (done) return;
        sel = sel === i ? null : i; api.sfx('tap'); draw();
      }
      function targetAt(x, y) {
        const el = document.elementFromPoint(x, y); if (!el || !root.contains(el)) return null;
        const b = el.closest('.' + T + 'bin'); if (b) return +b.dataset.b;
        if (el.closest('.' + T + 'tray')) return 'tray';
        return null;
      }
      function hover(t) { binEls.forEach((el, b) => el.classList.toggle('over', t === b)); tray.classList.toggle('over', t === 'tray' && mode === 'check'); }
      function endGhost() { if (ghost) { ghost.remove(); ghost = null; } hover(null); }

      root.addEventListener('pointerdown', e => {
        const c = e.target.closest('.' + T + 'card'); if (!c || st) return;
        const i = +c.dataset.i; st = { i, el: c, x: e.clientX, y: e.clientY, moved: false, id: e.pointerId };
        if (!locked[i] && !done) { try { c.setPointerCapture(e.pointerId); } catch (_) {} }
      });
      root.addEventListener('pointermove', e => {
        if (!st || e.pointerId !== st.id || locked[st.i] || done) return;
        if (!st.moved) {
          if (Math.hypot(e.clientX - st.x, e.clientY - st.y) < 7) return;
          st.moved = true; const r = st.el.getBoundingClientRect();
          st.ox = st.x - r.left; st.oy = st.y - r.top;
          ghost = st.el.cloneNode(true); ghost.classList.remove('sel'); ghost.classList.add(T + 'ghost'); ghost.style.width = r.width + 'px';
          document.body.appendChild(ghost); st.el.classList.add('lift');
          if (sel != null) { sel = null; binEls.forEach(el => el.classList.remove('cue')); const s = root.querySelector('.' + T + 'card.sel'); if (s) s.classList.remove('sel'); }
        }
        ghost.style.left = (e.clientX - st.ox) + 'px'; ghost.style.top = (e.clientY - st.oy) + 'px';
        hover(targetAt(e.clientX, e.clientY));
        e.preventDefault();
      });
      const up = e => {
        if (!st || e.pointerId !== st.id) return; const s = st; st = null;
        if (s.moved) { const t = e.type === 'pointercancel' ? null : targetAt(e.clientX, e.clientY); endGhost(); s.el.classList.remove('lift'); if (t === null) draw(); else drop(s.i, t); }
        else if (e.type === 'pointerup') tapCard(s.i);
      };
      root.addEventListener('pointerup', up); root.addEventListener('pointercancel', up);
      root.addEventListener('click', e => {
        if (e.target.closest('.' + T + 'card') || sel == null) return;
        const b = e.target.closest('.' + T + 'bin');
        if (b) drop(sel, +b.dataset.b);
        else if (e.target.closest('.' + T + 'tray')) drop(sel, 'tray');
      });
      if (chk) chk.onclick = check;
      $('.' + T + 'rst').onclick = () => { api.sfx('tap'); reset(); };
      reset();
      return () => { timers.forEach(clearTimeout); endGhost(); host.innerHTML = ''; };
    },
    example: {
      title: 'Kitchen waste',
      challenge: 'Help Riya sort the waste: wet waste or dry waste?',
      mode: 'sort',
      bins: [{ name: 'Wet waste', emoji: '🟢', color: '#2ed3a5' }, { name: 'Dry waste', emoji: '🔵', color: '#3b82f6' }],
      items: [
        { text: 'Banana peel', emoji: '🍌', bin: 0, why: 'It rots quickly — it is kitchen (wet) waste.' },
        { text: 'Newspaper', emoji: '📰', bin: 1, why: 'Paper is dry waste — it can be recycled.' },
        { text: 'Vegetable peels', emoji: '🥕', bin: 0, why: 'Peels rot and can be made into compost.' },
        { text: 'Plastic bottle', emoji: '🧴', bin: 1, why: 'Plastic does not rot — it is dry waste.' },
        { text: 'Leftover rice', emoji: '🍚', bin: 0, why: 'Leftover food is wet waste.' },
        { text: 'Glass jar', emoji: '🫙', bin: 1, why: 'Glass is dry waste and can be recycled.' },
        { text: 'Tea leaves', emoji: '🍵', bin: 0, why: 'Used tea leaves rot — wet waste.' },
        { text: 'Tin can', emoji: '🥫', bin: 1, why: 'Metal is dry waste — it can be recycled.' }
      ]
    },
    examples: [
      { title: 'शब्द पहचानो (कक्षा 3)', challenge: 'हर शब्द को सही डिब्बे में रखो — संज्ञा, सर्वनाम या क्रिया?', mode: 'sort',
        bins: [{ name: 'संज्ञा', emoji: '🏷️', color: '#8b5cf6' }, { name: 'सर्वनाम', emoji: '👉', color: '#ff9f1c' }, { name: 'क्रिया', emoji: '🏃', color: '#2ed3a5' }],
        items: [
          { text: 'गाय', bin: 'संज्ञा', why: 'गाय एक प्राणी का नाम है — संज्ञा।' },
          { text: 'वह', bin: 'सर्वनाम', why: '"वह" नाम के स्थान पर आता है — सर्वनाम।' },
          { text: 'दौड़ना', bin: 'क्रिया', why: 'दौड़ना एक काम है — क्रिया।' },
          { text: 'दिल्ली', bin: 'संज्ञा', why: 'दिल्ली एक स्थान का नाम है — संज्ञा।' },
          { text: 'हम', bin: 'सर्वनाम', why: '"हम" नाम के स्थान पर आता है — सर्वनाम।' },
          { text: 'खाना खाता है', bin: 'क्रिया', why: 'खाना खाना एक काम है — क्रिया।' },
          { text: 'तुम', bin: 'सर्वनाम', why: '"तुम" नाम के स्थान पर आता है — सर्वनाम।' }
        ] },
      { title: 'Indian Constitution — Seventh Schedule (Class 10)', challenge: 'Place each subject in the Union, State or Concurrent List, then press Check', mode: 'check',
        bins: [{ name: 'Union List', emoji: '🏛️', color: '#3b82f6' }, { name: 'State List', emoji: '🏠', color: '#2ed3a5' }, { name: 'Concurrent List', emoji: '🤝', color: '#8b5cf6' }],
        items: [
          { text: 'Defence', bin: 0, why: 'Defence is of national importance — Union List.' },
          { text: 'Police', bin: 1, why: 'Police and public order are State subjects.' },
          { text: 'Education', bin: 2, why: 'Education is in the Concurrent List (since 1976).' },
          { text: 'Foreign affairs', bin: 0, why: 'Dealing with other countries is a Union subject.' },
          { text: 'Agriculture', bin: 1, why: 'Agriculture is a State subject.' },
          { text: 'Marriage and divorce', bin: 2, why: 'Both Union and States can make laws on marriage.' },
          { text: 'Banking and currency', bin: 0, why: 'Banking and currency are Union subjects.' },
          { text: 'Forests', bin: 2, why: 'Forests moved to the Concurrent List in 1976.' }
        ] },
      { title: 'Which materials let electricity pass? (Class 6)', challenge: 'Sort into conductors and insulators', mode: 'sort',
        bins: ['Conductor ⚡', 'Insulator 🚫'],
        items: [['Iron nail 🔩', 0, 'Metals like iron are good conductors.'], ['Rubber eraser', 1, 'Rubber does not let current flow — insulator.'], ['Copper wire', 0, 'Copper is a metal — a very good conductor.'], ['Plastic scale 📏', 1, 'Plastic is an insulator.'], ['Aluminium foil', 0, 'Aluminium is a metal — conductor.'], ['Wooden pencil body ✏️', 1, 'Dry wood is an insulator.'], ['Steel spoon 🥄', 0, 'Steel is a metal — conductor.']] }
    ]
  });
})();
