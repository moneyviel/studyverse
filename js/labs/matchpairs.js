/* Knowtopia lab: matchpairs — join each left item to its partner on the right with a line
 *
 * PARAMS (all optional; if `pairs` is missing/invalid a built-in states-and-capitals set is used)
 *  title       string   heading above the columns (any language)                         default ''
 *  challenge   string   the "🎯 Challenge" line                                            default auto ('Match all N pairs')
 *  pairs       array    the correct pairs, 2–8 of them: [['Happy','Glad'], …]
 *                       or [{ left:'Happy', right:'Glad' }, …] (also {l,r} / {a,b}).
 *                       Texts up to ~40 characters wrap. Two pairs may share the same right
 *                       text — either copy is then accepted.                              default states & capitals
 *  leftTitle   string   label over the left column                                       default ''
 *  rightTitle  string   label over the right column                                      default ''
 *  shuffle     boolean  mix the left column too (the right column is always mixed)        default true
 *  mode        string   'instant' = every join is checked at once (wrong ones flash red)
 *                       'check'   = join everything first, then press ✔ Check            default 'instant'
 *  speak       boolean  read an item aloud when it is tapped                              default false
 *
 * The child taps an item on one side, then its partner on the other side (or drags a line from one
 * card to another). A coloured line joins them. 'instant': right joins lock with ✓, wrong joins
 * shake and vanish. 'check': joins can be changed (tap a joined card and join it again); ✔ Check
 * locks the right ones and removes the wrong ones. Win = all pairs matched correctly.
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const mix = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const PAL = ['#8b5cf6', '#2ed3a5', '#3b82f6', '#ff9f1c', '#ec4899', '#14b8a6', '#6366f1', '#f59e0b'];
  function norm(arr) {
    return (Array.isArray(arr) ? arr : []).map(x => {
      if (Array.isArray(x)) return [x[0], x[1]];
      if (x && typeof x === 'object') return [x.left != null ? x.left : x.l != null ? x.l : x.a, x.right != null ? x.right : x.r != null ? x.r : x.b];
      return null;
    }).filter(x => x && x[0] != null && x[1] != null && String(x[0]).trim() && String(x[1]).trim())
      .map(x => ({ l: String(x[0]).trim(), r: String(x[1]).trim() })).slice(0, 8);
  }

  Labs.register('matchpairs', {
    title: 'Match the pairs',
    subjects: ['english', 'hindi', 'sanskrit', 'social', 'science', 'evs', 'maths'],
    render(host, p, api) {
      p = p || {};
      let pairs = norm(p.pairs), custom = true;
      if (pairs.length < 2) { pairs = norm(Labs.registry.matchpairs.example.pairs); custom = false; }
      const N = pairs.length;
      const mode = p.mode === 'check' ? 'check' : 'instant';
      const doShuffle = p.shuffle !== false, doSpeak = p.speak === true;
      const challenge = (custom && p.challenge) || `Match all ${N} pairs`;
      const title = custom ? (p.title || '') : '';
      const lt = custom ? (p.leftTitle || '') : 'State', rt = custom ? (p.rightTitle || '') : 'Capital';
      const timers = []; const later = (f, ms) => timers.push(setTimeout(f, ms));
      const T = 'lb-matchpairs-';

      host.innerHTML = `<style>
.${T}w{color:#1b1f3a;font-size:15px;user-select:none;-webkit-user-select:none}
.${T}ch{font-weight:800;margin:0 0 4px;line-height:1.35}
.${T}tt{font-weight:800;font-size:15px;color:#8b5cf6;margin-bottom:2px;line-height:1.35}
.${T}stat{display:flex;justify-content:space-between;gap:8px;font-size:12px;font-weight:800;color:#6b7090;margin:2px 2px 6px}
.${T}g{position:relative;display:grid;grid-template-columns:minmax(0,1fr) 34px minmax(0,1fr);row-gap:7px}
.${T}ht{font-size:12px;font-weight:800;color:#8b5cf6;text-transform:none;text-align:center;line-height:1.3;padding-bottom:1px;overflow-wrap:anywhere}
.${T}svg{position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;overflow:hidden;z-index:2}
.${T}svg line{stroke-width:4;stroke-linecap:round}
.${T}svg line.tmp{stroke:#ffc93c;stroke-dasharray:2 7}
.${T}svg line.bad{stroke:#ff6b6b;animation:${T}fade 1s forwards}
@keyframes ${T}fade{60%{opacity:1}100%{opacity:0}}
.${T}svg circle{stroke:#fff;stroke-width:2}
.${T}c{position:relative;display:flex;align-items:center;min-height:46px;box-sizing:border-box;padding:7px 10px;border-radius:14px;background:#fff;box-shadow:0 2px 0 #e2def3,inset 0 0 0 2px #ebe8f8;font-weight:700;font-size:13.5px;line-height:1.4;cursor:pointer;touch-action:none;overflow-wrap:anywhere;transition:box-shadow .2s,background .2s,transform .15s}
.${T}c.L{grid-column:1;padding-right:14px}
.${T}c.R{grid-column:3;padding-left:14px}
.${T}c .d{position:absolute;top:50%;width:12px;height:12px;margin-top:-6px;border-radius:50%;background:#dcd8f0;box-shadow:0 0 0 3px #fff}
.${T}c.L .d{right:-6px}
.${T}c.R .d{left:-6px}
.${T}c.sel{box-shadow:0 0 0 3px #ffc93c,0 2px 0 #e2def3;transform:translateY(-1px)}
.${T}c.sel .d{background:#ffc93c}
.${T}c.lk{background:var(--t);box-shadow:inset 0 0 0 2px var(--c);cursor:default}
.${T}c.lk .d,.${T}c.ln .d{background:var(--c)}
.${T}c.ln{box-shadow:inset 0 0 0 2px var(--c),0 2px 0 #e2def3}
.${T}c.no{background:#fff0f0;box-shadow:inset 0 0 0 2px #ff6b6b}
.${T}c.shk{animation:${T}shk .45s}
.${T}c.pop{animation:${T}pop .35s}
.${T}c .ok{flex:none;margin-left:auto;padding-left:4px;color:#11a37f;font-weight:900}
@keyframes ${T}shk{20%{transform:translateX(-5px)}40%{transform:translateX(5px)}60%{transform:translateX(-3px)}80%{transform:translateX(3px)}}
@keyframes ${T}pop{0%{transform:scale(.92)}60%{transform:scale(1.04)}100%{transform:scale(1)}}
.${T}fb{margin-top:9px;min-height:40px;border-radius:14px;padding:8px 11px;font-size:13px;font-weight:700;line-height:1.4;background:#f6f5fc;color:#6b7090;transition:background .25s,color .25s;overflow-wrap:anywhere}
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
  <div class="${T}g"></div>
  <div class="${T}fb"></div>
  <div class="${T}bar">${mode === 'check' ? `<button class="${T}btn go ${T}chk">✔ Check</button>` : ''}<button class="${T}btn ${T}rst">🔄 Reset</button></div>
</div>`;
      const root = host.querySelector('.' + T + 'w');
      const $ = s => root.querySelector(s);
      const grid = $('.' + T + 'g'), fb = $('.' + T + 'fb'), chk = $('.' + T + 'chk');
      const NS = 'http://www.w3.org/2000/svg';
      let Lord, Rord, links, locked, col, sel, done, won, st = null, svg, tmp = null, colN = 0, bad = [];
      // links: Map leftIdx -> rightIdx (pair indices into `pairs`; right item k shows pairs[k].r)
      const isRight = (l, r) => pairs[l].r === pairs[r].r;
      const tintOf = c => c + '18';

      function say(html, cls) { fb.className = T + 'fb' + (cls ? ' ' + cls : ''); fb.innerHTML = html; }
      function build() {
        const off = (lt || rt) ? 1 : 0;
        grid.innerHTML = (off ? `<div class="${T}ht" style="grid-column:1;grid-row:1">${esc(lt)}</div><div class="${T}ht" style="grid-column:3;grid-row:1">${esc(rt)}</div>` : '') +
          Lord.map((k, row) => `<div class="${T}c L" data-s="L" data-k="${k}" style="grid-row:${row + 1 + off}"><span class="x">${esc(pairs[k].l)}</span><i class="d"></i></div>`).join('') +
          Rord.map((k, row) => `<div class="${T}c R" data-s="R" data-k="${k}" style="grid-row:${row + 1 + off}"><span class="x">${esc(pairs[k].r)}</span><i class="d"></i></div>`).join('');
        svg = document.createElementNS(NS, 'svg'); svg.setAttribute('class', T + 'svg'); grid.appendChild(svg);
      }
      const card = (s, k) => grid.querySelector(`.${T}c[data-s="${s}"][data-k="${k}"]`);
      /* Line ends are worked out in the grid's own layout pixels (the SVG's user units), not screen pixels:
         the app scales its pages with CSS zoom (text size 90–150%) and cards animate with transforms, and
         either one used to push the lines past the card edge. Ends are also kept inside the grid. */
      const clampPt = (x, y) => ({ x: Math.max(2, Math.min(grid.clientWidth - 2, x)), y: Math.max(2, Math.min(grid.clientHeight - 2, y)) });
      function anchor(s, k) {
        const c = card(s, k);
        if (c.offsetParent === grid) return clampPt(c.offsetLeft + (s === 'L' ? c.offsetWidth : 0), c.offsetTop + c.offsetHeight / 2);
        const g = grid.getBoundingClientRect(), r = c.getBoundingClientRect(), sx = g.width / (grid.offsetWidth || g.width || 1), sy = g.height / (grid.offsetHeight || g.height || 1);
        return clampPt(((s === 'L' ? r.right : r.left) - g.left) / (sx || 1), (r.top + r.height / 2 - g.top) / (sy || 1));
      }
      function gridPt(cx, cy) {
        const g = grid.getBoundingClientRect(), sx = g.width / (grid.offsetWidth || g.width || 1), sy = g.height / (grid.offsetHeight || g.height || 1);
        return clampPt((cx - g.left) / (sx || 1), (cy - g.top) / (sy || 1));
      }
      function mkLine(a, b, cls, color) {
        const ln = document.createElementNS(NS, 'line');
        ln.setAttribute('x1', a.x); ln.setAttribute('y1', a.y); ln.setAttribute('x2', b.x); ln.setAttribute('y2', b.y);
        if (cls) ln.setAttribute('class', cls); if (color) ln.setAttribute('stroke', color);
        svg.appendChild(ln); return ln;
      }
      function lines() {
        if (!svg) return;
        svg.innerHTML = '';
        links.forEach((r, l) => { const c = col[l] || '#8b5cf6'; mkLine(anchor('L', l), anchor('R', r), '', c); });
        bad.forEach(([l, r]) => mkLine(anchor('L', l), anchor('R', r), 'bad'));
        if (tmp) mkLine(tmp.a, tmp.b, 'tmp');
      }
      function draw() {
        grid.querySelectorAll('.' + T + 'c').forEach(el => {
          const s = el.dataset.s, k = +el.dataset.k;
          const l = s === 'L' ? k : [...links].find(([, r]) => r === k)?.[0];
          const linked = l != null && links.has(l) && (s === 'L' || links.get(l) === k);
          const lk = linked && locked.has(l);
          el.classList.toggle('lk', lk); el.classList.toggle('ln', linked && !lk);
          el.classList.toggle('sel', !!sel && sel.s === s && sel.k === k);
          if (linked) { el.style.setProperty('--c', col[l]); el.style.setProperty('--t', tintOf(col[l])); }
          let ok = el.querySelector('.ok');
          if (lk && !ok) el.insertAdjacentHTML('beforeend', '<span class="ok">✓</span>'); else if (!lk && ok) ok.remove();
        });
        $('.' + T + 'sc').textContent = mode === 'instant' ? `✓ ${locked.size}/${N}` : `Joined ${links.size}/${N}`;
        $('.' + T + 'hint').textContent = done ? 'All matched! 🌟' : sel ? `Now tap its partner on the ${sel.s === 'L' ? 'right' : 'left'}` : 'Tap one item, then its partner';
        if (chk) chk.disabled = done || links.size < N;
        lines();
      }
      function anim(s, k, cls) { const el = card(s, k); if (el) { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); } }
      function reset() {
        const ids = pairs.map((_, i) => i);
        Lord = doShuffle ? mix(ids) : ids.slice();
        do { Rord = mix(ids); } while (N > 2 && Rord.some((v, i) => v === Lord[i]) && Math.random() < 0.85);
        links = new Map(); locked = new Set(); col = {}; sel = null; done = false; bad = []; colN = 0; tmp = null;
        build();
        say(mode === 'check' ? 'Join every item to a partner, then press ✔ Check.' : 'Tap an item on the left, then its partner on the right — or drag a line.');
        draw();
      }
      function join(l, r) {
        if (done || locked.has(l)) return;
        const rOwner = [...links].find(([, rr]) => rr === r);
        if (rOwner && locked.has(rOwner[0])) return;
        sel = null;
        if (mode === 'instant') {
          if (isRight(l, r)) {
            // with duplicate right texts, a free twin card may be used
            links.set(l, r); locked.add(l); col[l] = PAL[colN++ % PAL.length];
            api.sfx('correct'); say(`✓ <b>${esc(pairs[l].l)}</b> ↔ <b>${esc(pairs[r].r)}</b>`, 'good');
            draw(); anim('L', l, 'pop'); anim('R', r, 'pop'); winCheck();
          } else {
            api.sfx('wrong'); say(`✗ <b>${esc(pairs[l].l)}</b> and <b>${esc(pairs[r].r)}</b> are not a pair. Try again!`, 'bad');
            const pr = [l, r]; bad.push(pr); draw(); anim('L', l, 'shk'); anim('R', r, 'shk');
            later(() => { bad = bad.filter(x => x !== pr); lines(); }, 1000);
          }
        } else {
          if (rOwner) links.delete(rOwner[0]);
          links.set(l, r); if (!col[l]) col[l] = PAL[colN++ % PAL.length];
          api.sfx('tap');
          const left = N - links.size;
          say(left ? `${left} more to join.` : 'All joined! Press ✔ Check.');
          draw();
        }
      }
      function winCheck() {
        if (locked.size < N) return;
        done = true; sel = null; draw();
        say(`🌟 Super! You matched all ${N} pairs correctly.`, 'win');
        if (!won) { won = true; api.win(`You matched all ${N} pairs correctly!`); }
      }
      function check() {
        if (done) return;
        const wrong = [];
        links.forEach((r, l) => { if (!locked.has(l)) { if (isRight(l, r)) locked.add(l); else wrong.push([l, r]); } });
        if (!wrong.length) { api.sfx('correct'); winCheck(); return; }
        api.sfx('hmm');
        wrong.forEach(([l]) => links.delete(l));
        bad = wrong.slice(); draw();
        wrong.forEach(([l, r]) => { [['L', l], ['R', r]].forEach(([s, k]) => { const el = card(s, k); el.classList.add('no'); anim(s, k, 'shk'); }); });
        say(`${locked.size} of ${N} right ✓. The red ones were wrong — join them again!`, 'bad');
        later(() => { bad = []; grid.querySelectorAll('.' + T + 'c.no').forEach(el => el.classList.remove('no')); draw(); }, 1100);
      }
      function tap(s, k) {
        if (doSpeak) api.speak(s === 'L' ? pairs[k].l : pairs[k].r);
        if (done) return;
        const lockedCard = s === 'L' ? locked.has(k) : [...links].some(([l, r]) => r === k && locked.has(l));
        if (lockedCard) return;
        if (!sel || sel.s === s) { sel = sel && sel.k === k ? null : { s, k }; api.sfx('tap'); draw(); return; }
        const l = s === 'L' ? k : sel.k, r = s === 'R' ? k : sel.k;
        join(l, r);
      }
      const cardAt = (x, y) => { const el = document.elementFromPoint(x, y); const c = el && el.closest && el.closest('.' + T + 'c'); return c && grid.contains(c) ? c : null; };

      grid.addEventListener('pointerdown', e => {
        const c = e.target.closest('.' + T + 'c'); if (!c || st) return;
        st = { s: c.dataset.s, k: +c.dataset.k, el: c, x: e.clientX, y: e.clientY, id: e.pointerId, moved: false };
        try { c.setPointerCapture(e.pointerId); } catch (_) {}
      });
      grid.addEventListener('pointermove', e => {
        if (!st || e.pointerId !== st.id || done) return;
        if (!st.moved) {
          if (Math.hypot(e.clientX - st.x, e.clientY - st.y) < 8) return;
          const lockedCard = st.s === 'L' ? locked.has(st.k) : [...links].some(([l, r]) => r === st.k && locked.has(l));
          if (lockedCard) { st = null; return; }
          st.moved = true; sel = { s: st.s, k: st.k }; draw();
        }
        tmp = { a: anchor(st.s, st.k), b: gridPt(e.clientX, e.clientY) };
        lines(); e.preventDefault();
      });
      const up = e => {
        if (!st || e.pointerId !== st.id) return; const s = st; st = null;
        if (s.moved) {
          tmp = null; const c = e.type === 'pointerup' ? cardAt(e.clientX, e.clientY) : null;
          if (c && c.dataset.s !== s.s) { const k = +c.dataset.k; join(s.s === 'L' ? s.k : k, s.s === 'R' ? s.k : k); }
          else { sel = null; draw(); }
        } else if (e.type === 'pointerup') tap(s.s, s.k);
      };
      grid.addEventListener('pointerup', up); grid.addEventListener('pointercancel', up);
      const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(() => lines()) : null;
      if (ro) ro.observe(grid);
      const onRs = () => lines(); window.addEventListener('resize', onRs);
      grid.addEventListener('animationend', () => { if (svg) lines(); });
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { if (svg) lines(); });
      if (chk) chk.onclick = check;
      $('.' + T + 'rst').onclick = () => { api.sfx('tap'); reset(); };
      reset();
      return () => { timers.forEach(clearTimeout); if (ro) ro.disconnect(); window.removeEventListener('resize', onRs); svg = null; host.innerHTML = ''; };
    },
    example: {
      title: 'States of India and their capitals',
      challenge: 'Join each state to its capital city',
      leftTitle: 'State', rightTitle: 'Capital', mode: 'instant',
      pairs: [['Rajasthan', 'Jaipur'], ['Maharashtra', 'Mumbai'], ['Tamil Nadu', 'Chennai'], ['West Bengal', 'Kolkata'], ['Karnataka', 'Bengaluru'], ['Bihar', 'Patna']]
    },
    examples: [
      { title: 'मुहावरे और उनके अर्थ (कक्षा 7)', challenge: 'हर मुहावरे को उसके सही अर्थ से मिलाओ', leftTitle: 'मुहावरा', rightTitle: 'अर्थ', mode: 'instant',
        pairs: [['आँखों का तारा', 'बहुत प्यारा'], ['नौ दो ग्यारह होना', 'भाग जाना'], ['ईद का चाँद होना', 'बहुत दिनों बाद दिखाई देना'], ['हाथ पैर फूल जाना', 'बहुत घबरा जाना'], ['दाँतों तले उँगली दबाना', 'हैरान होना']] },
      { title: 'Nationalist leaders (Class 10 History)', challenge: 'Match each leader with their work, then press Check', leftTitle: 'Leader', rightTitle: 'Known for', mode: 'check',
        pairs: [['Mahatma Gandhi', 'Led the Salt March to Dandi (1930)'], ['Subhas Chandra Bose', 'Formed the Indian National Army'], ['B. R. Ambedkar', 'Organised the Depressed Classes Association'], ['Alluri Sitarama Raju', 'Led a guerrilla revolt in the Gudem Hills'], ['Jawaharlal Nehru', 'Presided over the Lahore Congress, 1929']] },
      { title: 'Opposites (Class 2)', challenge: 'Find the opposite of each word', leftTitle: 'Word', rightTitle: 'Opposite', shuffle: false,
        pairs: [{ left: 'Hot 🔥', right: 'Cold ❄️' }, { left: 'Big 🐘', right: 'Small 🐭' }, { left: 'Day ☀️', right: 'Night 🌙' }, { left: 'Happy 😀', right: 'Sad 😢' }] }
    ]
  });
})();
