/* StudyVerse Concept Lab: patternbuilder — repeating and growing patterns (Grades 1-3).
 *
 * The child continues a pattern by dragging (or tap-then-tap) tokens into empty slots, taps the
 * part that repeats, or spots and fixes the tile that breaks the pattern. Growing patterns are
 * drawn as towers that get taller (1, 2, 3 …) and the child builds the next tower.
 *
 * PARAMS (all optional)
 *   core       array of strings  the repeating unit. A token may be an emoji ('🍎'), a colour
 *                                ('red', 'लाल', '#ff6b6b', 'color:blue'), a shape
 *                                ('shape:triangle', 'shape:star:red'; shapes: circle square triangle
 *                                star heart diamond) or a short word/letter ('क', 'clap').
 *                                                                              default ['🍎','🍌']
 *   mode       string  'extend'  = fill the next slots from the palette
 *                      'find'    = tap the tiles that make the repeating part (any one full unit)
 *                      'mistake' = tap the tile that breaks the pattern, then fix it
 *                                                                              default 'extend'
 *   show       number  tiles shown (extend: before the blanks; find/mistake: total).
 *                      With `growing`: number of towers shown.  default extend 2×core (min 4),
 *                      find/mistake 3×core (min 6); growing = growing.length − blanks
 *   blanks     number  empty slots to fill (extend). With `growing`: towers to build.
 *                                                    default = core length (max 4); growing 1
 *   palette    array   tokens offered to drag. Missing core tokens are added automatically.
 *                                                    default = core + 1-2 decoys of the same kind
 *   decoys     array   extra wrong tokens to mix into the default palette (useful for words)
 *                                                    default [] (emoji/colour/shape decoys auto)
 *   growing    array of numbers  growing pattern: tower k has growing[k] tiles of token
 *                      core[k % core.length]. Include the answer towers, e.g. [1,2,3,4] shows
 *                      1,2,3 and the child builds 4. Missing towers continue by the last step.
 *                      Used by 'extend' and 'mistake' (one tower has a wrong count). default none
 *   colorWords boolean treat colour names (red, नीला …) as colour swatches     default true
 *   mistakeAt  number  1-based position of the wrong tile/tower (mistake mode) default random
 *   fix        boolean mistake mode: after finding the mistake, the child must fix it  default true
 *   challenge  string  challenge line                              default generated from mode
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const COLORS = {
    red: '#ef4444', blue: '#3b82f6', green: '#22c55e', yellow: '#facc15', orange: '#fb923c',
    purple: '#8b5cf6', violet: '#8b5cf6', pink: '#f472b6', brown: '#a16207', black: '#1b1f3a',
    white: '#ffffff', grey: '#9ca3af', gray: '#9ca3af',
    'लाल': '#ef4444', 'नीला': '#3b82f6', 'हरा': '#22c55e', 'पीला': '#facc15', 'नारंगी': '#fb923c',
    'बैंगनी': '#8b5cf6', 'गुलाबी': '#f472b6', 'भूरा': '#a16207', 'काला': '#1b1f3a', 'सफ़ेद': '#ffffff', 'सफेद': '#ffffff'
  };
  const SHAPES = ['circle', 'square', 'triangle', 'star', 'heart', 'diamond'];
  const SHAPE_COL = { circle: '#ff6b6b', square: '#3b82f6', triangle: '#2ed3a5', star: '#ffc93c', heart: '#f472b6', diamond: '#8b5cf6' };
  const POOL = {
    emoji: ['🍎', '🍌', '🍇', '⭐', '🌸', '🐟', '🚗', '🎈', '🍓', '🐱', '🌙', '🦋'],
    color: ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink'],
    shape: SHAPES.map(s => 'shape:' + s)
  };
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const clampI = (v, lo, hi, d) => { v = Math.round(+v); return isFinite(v) ? Math.max(lo, Math.min(hi, v)) : d; };

  function parse(raw, colorWords) {
    const s = String(raw == null ? '' : raw).trim();
    if (/^#[0-9a-f]{3}([0-9a-f]{3})?$/i.test(s)) return { kind: 'color', color: s, label: '' };
    let m = s.match(/^colou?r:(.+)$/i);
    if (m) { const c = m[1].trim(); return { kind: 'color', color: COLORS[c.toLowerCase()] || COLORS[c] || c, label: '' }; }
    m = s.match(/^shape:([a-z]+)(?::(.+))?$/i);
    if (m && SHAPES.includes(m[1].toLowerCase())) {
      const sh = m[1].toLowerCase(), c = m[2] ? (COLORS[m[2].toLowerCase()] || m[2]) : SHAPE_COL[sh];
      return { kind: 'shape', shape: sh, color: c };
    }
    if (colorWords && (COLORS[s.toLowerCase()] || COLORS[s])) return { kind: 'color', color: COLORS[s.toLowerCase()] || COLORS[s], label: s };
    if (s && /\p{Extended_Pictographic}/u.test(s) && !/[\p{L}\p{N}]/u.test(s)) return { kind: 'emoji', text: s };
    return { kind: 'text', text: s || '?' };
  }
  function shapeSVG(sh, c) {
    const st = `fill="${esc(c)}" stroke="rgba(27,31,58,.35)" stroke-width="2" stroke-linejoin="round"`;
    const d = {
      circle: `<circle cx="16" cy="16" r="12" ${st}/>`,
      square: `<rect x="5" y="5" width="22" height="22" rx="3" ${st}/>`,
      triangle: `<path d="M16 4 L29 27 L3 27 Z" ${st}/>`,
      star: `<path d="M16 3 L19.6 11.6 L29 12.4 L21.9 18.6 L24 27.8 L16 23 L8 27.8 L10.1 18.6 L3 12.4 L12.4 11.6 Z" ${st}/>`,
      heart: `<path d="M16 28 C6 20 3 15 3 10.5 C3 6.5 6 4 9.5 4 C12.5 4 14.6 6 16 8.5 C17.4 6 19.5 4 22.5 4 C26 4 29 6.5 29 10.5 C29 15 26 20 16 28 Z" ${st}/>`,
      diamond: `<path d="M16 3 L28 16 L16 29 L4 16 Z" ${st}/>`
    }[sh];
    return `<svg viewBox="0 0 32 32" width="70%" height="70%" aria-hidden="true">${d}</svg>`;
  }
  function tokHTML(t) {
    if (t.kind === 'emoji') return `<span class="lb-patternbuilder-em">${esc(t.text)}</span>`;
    if (t.kind === 'color') return `<span class="lb-patternbuilder-dot" style="background:${esc(t.color)}"></span>${t.label ? `<span class="lb-patternbuilder-cl">${esc(t.label)}</span>` : ''}`;
    if (t.kind === 'shape') return shapeSVG(t.shape, t.color);
    return `<span class="lb-patternbuilder-tx">${esc(t.text)}</span>`;
  }
  function period(arr) {
    const n = arr.length;
    for (let p = 1; p <= n; p++) { if (n % p) continue; let ok = true; for (let i = p; i < n; i++) if (arr[i] !== arr[i - p]) { ok = false; break; } if (ok) return p; }
    return n;
  }

  Labs.register('patternbuilder', {
    title: 'Pattern builder',
    subjects: ['maths', 'evs', 'english', 'hindi'],
    render(host, p, api) {
      const colorWords = p.colorWords !== false;
      let core = (Array.isArray(p.core) ? p.core : []).map(x => String(x == null ? '' : x).trim()).filter(Boolean).slice(0, 8);
      if (!core.length) core = ['🍎', '🍌'];
      const mode = ['extend', 'find', 'mistake'].includes(p.mode) ? p.mode : 'extend';
      const P = period(core); core = core.slice(0, P);
      const distinct = [...new Set(core)];
      const info = {}; const tk = s => (info[s] || (info[s] = parse(s, colorWords)));
      const tile = (s, cls = '', attrs = '') => `<div class="lb-patternbuilder-tile k-${tk(s).kind} ${cls}" ${attrs}>${tokHTML(tk(s))}</div>`;

      // ---- growing set-up
      let growing = Array.isArray(p.growing) ? p.growing.map(n => Math.round(+n)).filter(n => isFinite(n) && n >= 0) : [];
      const isGrow = growing.length >= 2 && mode !== 'find';
      let counts = [], shownN = 0, blanksN = 0;
      if (isGrow) {
        blanksN = clampI(p.blanks, 1, 2, 1);
        shownN = p.show != null ? clampI(p.show, 2, 6, 3) : Math.max(2, Math.min(6, growing.length - (mode === 'extend' ? blanksN : 0)));
        const total = shownN + (mode === 'extend' ? blanksN : 0);
        counts = growing.slice(0, total);
        while (counts.length < total) { const k = counts.length; counts.push(Math.max(0, counts[k - 1] + (counts[k - 1] - counts[k - 2]))); }
        counts = counts.map(c => Math.min(10, c));
      }
      const growTok = k => core[k % core.length];

      // ---- repeating set-up
      const defShow = mode === 'extend' ? Math.max(4, 2 * P) : Math.max(6, 3 * P);
      const show = p.show != null ? clampI(p.show, Math.min(2, defShow), 16, defShow) : Math.min(16, defShow);
      const blanks = clampI(p.blanks, 1, 8, Math.min(4, P));
      const seqAt = i => core[i % P];

      // ---- palette
      const kind0 = tk(core[0]).kind;
      let palette;
      if (Array.isArray(p.palette) && p.palette.length) {
        palette = [...new Set(p.palette.map(x => String(x).trim()).filter(Boolean))];
        distinct.forEach(t => { if (!palette.includes(t)) palette.push(t); });
      } else {
        const extra = (Array.isArray(p.decoys) ? p.decoys.map(String) : []).filter(t => !distinct.includes(t));
        let pool = (POOL[kind0] || []).filter(t => !distinct.includes(t) && !distinct.some(d => tk(d).kind === 'color' && tk(t).kind === 'color' && tk(d).color === tk(t).color));
        const nDec = extra.length ? 0 : (distinct.length <= 2 ? 2 : 1);
        palette = distinct.concat(extra, shuffle(pool).slice(0, nDec));
      }
      palette = palette.slice(0, 8);

      const chDefault = {
        extend: isGrow ? 'Look how the towers grow. Build the next one!' : `Fill the ${blanks} empty box${blanks > 1 ? 'es' : ''} to continue the pattern.`,
        find: 'Tap the tiles that make the part that repeats.',
        mistake: isGrow ? 'One tower is wrong. Tap it, then fix it.' : 'One tile breaks the pattern. Tap it, then fix it.'
      }[mode];

      host.innerHTML = `
<style>
.lb-patternbuilder-w{color:#1b1f3a;font-size:14px}
.lb-patternbuilder-ch{font-weight:800;font-size:14.5px;line-height:1.35;margin-bottom:8px}
.lb-patternbuilder-strip{background:linear-gradient(#f7f5ff,#eef1ff);border-radius:18px;padding:12px 8px;display:flex;flex-wrap:wrap;gap:7px;justify-content:center;align-items:flex-end;min-height:70px}
.lb-patternbuilder-tile{min-width:46px;min-height:46px;border-radius:14px;background:#fff;box-shadow:0 3px 0 #dcdff2,0 0 0 2px #e6e8f7 inset;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:3px 6px;box-sizing:border-box;transition:transform .18s,box-shadow .18s,background .18s;user-select:none;-webkit-user-select:none;max-width:100%;position:relative}
.lb-patternbuilder-tile.k-emoji,.lb-patternbuilder-tile.k-shape{width:46px;height:46px;padding:0}
.lb-patternbuilder-tile.k-color{width:46px;padding:4px}
.lb-patternbuilder-em{font-size:27px;line-height:1}
.lb-patternbuilder-dot{width:28px;height:28px;border-radius:50%;box-shadow:0 0 0 2px rgba(27,31,58,.18) inset;flex:none}
.lb-patternbuilder-cl{font-size:10px;font-weight:800;color:#6b7090;line-height:1.2;margin-top:1px;text-align:center;word-break:break-word}
.lb-patternbuilder-tx{font-size:16px;font-weight:800;line-height:1.4;text-align:center;overflow-wrap:anywhere}
.lb-patternbuilder-slot{background:#fff;box-shadow:none;border:2.5px dashed #b9b2f5;}
.lb-patternbuilder-slot.lb-patternbuilder-empty{background:rgba(255,255,255,.6)}
.lb-patternbuilder-slot.lb-patternbuilder-empty::after{content:'?';font-weight:900;color:#b9b2f5;font-size:20px}
.lb-patternbuilder-slot.lb-patternbuilder-hot{border-color:#8b5cf6;background:#f1ecff;transform:scale(1.06)}
.lb-patternbuilder-slot.lb-patternbuilder-filled{border-style:solid;border-color:#c9c2f7}
.lb-patternbuilder-ok{box-shadow:0 0 0 3px #2ed3a5 inset!important;background:#eafff7!important;border-color:#2ed3a5!important}
.lb-patternbuilder-bad{animation:lbpbshake .45s;box-shadow:0 0 0 3px #ff6b6b inset!important;background:#fff0f0!important}
.lb-patternbuilder-sel{box-shadow:0 0 0 3px #8b5cf6 inset,0 4px 10px rgba(139,92,246,.35)!important;transform:translateY(-3px)}
.lb-patternbuilder-tap{cursor:pointer}
.lb-patternbuilder-g0{box-shadow:0 0 0 3px #8b5cf6 inset!important;background:#f3eeff!important}
.lb-patternbuilder-g1{box-shadow:0 0 0 3px #ffc93c inset!important;background:#fff8e1!important}
@keyframes lbpbshake{0%,100%{transform:translateX(0)}20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(4px)}}
@keyframes lbpbpop{0%{transform:scale(.6)}70%{transform:scale(1.12)}100%{transform:scale(1)}}
.lb-patternbuilder-pop{animation:lbpbpop .28s ease}
.lb-patternbuilder-tow{display:flex;flex-direction:column;align-items:center;gap:3px}
.lb-patternbuilder-tbox{display:grid;grid-auto-flow:column;grid-template-rows:repeat(var(--r,5),30px);gap:2px;padding:4px;border-radius:12px;min-width:38px;justify-content:center;transition:background .2s,box-shadow .2s;transform:scaleY(-1);box-sizing:border-box}
.lb-patternbuilder-tbox>*{transform:scaleY(-1)}
.lb-patternbuilder-tbox .lb-patternbuilder-tile{width:30px;height:30px;min-width:30px;min-height:30px;border-radius:8px;padding:0;box-shadow:0 2px 0 #dcdff2,0 0 0 1.5px #e6e8f7 inset}
.lb-patternbuilder-tbox .lb-patternbuilder-em{font-size:19px}
.lb-patternbuilder-tbox .lb-patternbuilder-dot{width:20px;height:20px}
.lb-patternbuilder-tbox .lb-patternbuilder-cl{display:none}
.lb-patternbuilder-tbox .lb-patternbuilder-tx{font-size:11px;line-height:1.1}
.lb-patternbuilder-tbox.k-text .lb-patternbuilder-tile{width:auto;min-width:30px;padding:0 4px}
.lb-patternbuilder-tbox.lb-patternbuilder-dz{border:2.5px dashed #b9b2f5;background:rgba(255,255,255,.65);min-width:52px}
.lb-patternbuilder-tbox.lb-patternbuilder-dz.lb-patternbuilder-hot{border-color:#8b5cf6;background:#f1ecff}
.lb-patternbuilder-tbox.lb-patternbuilder-pk{cursor:pointer;background:rgba(255,255,255,.5)}
.lb-patternbuilder-n{font-size:13px;font-weight:900;color:#6b7090;min-height:18px}
.lb-patternbuilder-msg{font-size:13px;font-weight:700;color:#6b7090;margin:7px 2px 0;min-height:18px;line-height:1.35}
.lb-patternbuilder-msg.good{color:#0f9b74}.lb-patternbuilder-msg.bad{color:#e04848}
.lb-patternbuilder-pl{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:8px;padding:9px 6px;border-radius:16px;background:#fffbea;box-shadow:0 0 0 2px #ffe9a6 inset}
.lb-patternbuilder-pl:empty{display:none}
.lb-patternbuilder-pl .lb-patternbuilder-tile{cursor:grab;touch-action:none}
.lb-patternbuilder-pll{width:100%;text-align:center;font-size:11px;font-weight:800;color:#a07a00;text-transform:uppercase;letter-spacing:.4px}
.lb-patternbuilder-row{display:flex;gap:8px;margin-top:9px}
.lb-patternbuilder-b{flex:1;min-height:42px;border:none;border-radius:13px;font-family:inherit;font-weight:800;font-size:14.5px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef}
.lb-patternbuilder-b.lb-patternbuilder-go{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-patternbuilder-b:active{transform:translateY(2px);box-shadow:none}
.lb-patternbuilder-b[hidden]{display:none}
.lb-patternbuilder-pm{display:flex;gap:6px}
.lb-patternbuilder-pm button{width:42px;height:40px;border:none;border-radius:12px;background:#8b5cf6;color:#fff;font-size:20px;font-weight:900;cursor:pointer;font-family:inherit}
.lb-patternbuilder-ghost{position:fixed;z-index:9999;pointer-events:none;transform:translate(-50%,-50%) scale(1.12);opacity:.92;box-shadow:0 8px 20px rgba(27,31,58,.25)!important}
</style>
<div class="lb-patternbuilder-w">
  <div class="lb-patternbuilder-ch">🎯 Challenge: ${esc(p.challenge || chDefault)}</div>
  <div class="lb-patternbuilder-strip" aria-label="pattern"></div>
  <div class="lb-patternbuilder-msg" aria-live="polite"></div>
  <div class="lb-patternbuilder-pl"></div>
  <div class="lb-patternbuilder-row">
    <button class="lb-patternbuilder-b lb-patternbuilder-go" data-a="check" hidden>✔ Check</button>
    <button class="lb-patternbuilder-b" data-a="new">↺ New try</button>
  </div>
</div>`;
      const $ = s => host.querySelector(s);
      const strip = $('.lb-patternbuilder-strip'), msgEl = $('.lb-patternbuilder-msg'), pal = $('.lb-patternbuilder-pl'), checkB = $('[data-a=check]');
      let won = false, sel = null, ghost = null, drag = null, timers = [];
      let st = {};
      const later = (f, ms) => timers.push(setTimeout(f, ms));
      const say = (t, cls = '') => { msgEl.textContent = t; msgEl.className = 'lb-patternbuilder-msg ' + cls; };
      const speakCore = () => api.speak(core.map(s => tk(s).label || tk(s).text || tk(s).shape || '').filter(Boolean).join(', '));
      const doWin = m => { if (won) return; won = true; draw(); say('🎉 ' + m, 'good'); api.sfx('correct'); speakCore(); api.win(m); };

      function setup() {
        won = false; sel = null; api.resetWin && api.resetWin();
        st = { fill: [], tower: [], found: false, m: -1, wrongTok: null, cnt: [], picked: [] };
        if (mode === 'mistake') {
          if (isGrow) {
            const n = counts.length;
            let m = p.mistakeAt != null ? clampI(p.mistakeAt, 1, n, 2) - 1 : 1 + Math.floor(Math.random() * (n - 1));
            st.m = m; st.cnt = counts.slice();
            const delta = counts[m] <= 1 ? 1 : (Math.random() < .5 ? -1 : 1);
            st.cnt[m] = counts[m] + delta;
          } else {
            let m = p.mistakeAt != null ? clampI(p.mistakeAt, 1, show, P + 1) - 1 : P + Math.floor(Math.random() * Math.max(1, show - P));
            if (m >= show) m = show - 1;
            st.m = m;
            const right = seqAt(m);
            const alt = distinct.filter(t => t !== right);
            const dec = palette.filter(t => !distinct.includes(t));
            st.wrongTok = alt.length ? alt[Math.floor(Math.random() * alt.length)] : (dec[0] || (kind0 === 'emoji' ? '🍓' : 'shape:star'));
          }
        }
        draw();
        const m0 = { extend: isGrow ? 'Drag tiles into the dashed box, or tap a tile then tap the box.' : 'Drag a tile into a box, or tap a tile then tap a box.', find: 'Tap the tiles that repeat (tap again to undo).', mistake: isGrow ? 'Count the tiles in each tower.' : 'Say the pattern aloud. Which tile does not fit?' }[mode];
        say(m0);
      }

      // ------------------------------------------------ drawing
      function draw() {
        let h = '';
        if (isGrow) {
          const R = Math.max(2, Math.min(5, Math.max(...counts, ...(st.cnt.length ? st.cnt : [0]), ...st.tower.map(a => (a || []).length))));
          const nShow = mode === 'extend' ? shownN + blanksN : counts.length;
          for (let k = 0; k < nShow; k++) {
            const tok = growTok(k), kk = tk(tok).kind;
            if (mode === 'extend' && k >= shownN) {
              const bi = k - shownN, items = st.tower[bi] || [];
              h += `<div class="lb-patternbuilder-tow"><div class="lb-patternbuilder-tbox lb-patternbuilder-dz k-${kk}${won ? ' lb-patternbuilder-ok' : ''}" style="--r:${R}" data-drop="t${bi}" aria-label="build here">${items.map((s, j) => tile(s, 'lb-patternbuilder-tap', `data-rm="${bi}:${j}"`)).join('')}</div><div class="lb-patternbuilder-n">${items.length || '?'}</div></div>`;
            } else {
              const c = mode === 'mistake' ? st.cnt[k] : counts[k];
              const cls = mode === 'mistake' ? ' lb-patternbuilder-pk' + (st.found && k === st.m ? (won ? ' lb-patternbuilder-ok' : ' lb-patternbuilder-g1') : '') : '';
              h += `<div class="lb-patternbuilder-tow"><div class="lb-patternbuilder-tbox k-${kk}${cls}" style="--r:${R}" data-g="${k}">${Array.from({ length: c }, () => tile(tok)).join('')}</div><div class="lb-patternbuilder-n">${c}</div>${mode === 'mistake' && st.found && k === st.m && !won ? '<div class="lb-patternbuilder-pm"><button data-pm="-1" aria-label="one less">−</button><button data-pm="1" aria-label="one more">+</button></div>' : ''}</div>`;
            }
          }
        } else if (mode === 'extend') {
          for (let i = 0; i < show; i++) h += tile(seqAt(i));
          for (let b = 0; b < blanks; b++) {
            const f = st.fill[b];
            h += f != null ? tile(f, 'lb-patternbuilder-slot lb-patternbuilder-filled lb-patternbuilder-tap' + (won ? ' lb-patternbuilder-ok' : ''), `data-drop="s${b}" data-rm="s${b}"`) : `<div class="lb-patternbuilder-tile lb-patternbuilder-slot lb-patternbuilder-empty lb-patternbuilder-tap" data-drop="s${b}" aria-label="empty box"></div>`;
          }
        } else if (mode === 'find') {
          for (let i = 0; i < show; i++) {
            let cls = 'lb-patternbuilder-tap';
            if (won) cls += ' lb-patternbuilder-g' + (Math.floor((i - st.start + P * 100) / P) % 2);
            else if (st.picked.includes(i)) cls += ' lb-patternbuilder-sel';
            h += tile(seqAt(i), cls, `data-i="${i}"`);
          }
        } else {
          for (let i = 0; i < show; i++) {
            const tok = i === st.m ? (st.fixedTok || st.wrongTok) : seqAt(i);
            let cls = 'lb-patternbuilder-tap', at = `data-i="${i}"`;
            if (i === st.m && st.found) { cls += won ? ' lb-patternbuilder-ok' : ' lb-patternbuilder-slot lb-patternbuilder-g1'; at += ` data-drop="m"`; }
            h += tile(tok, cls, at);
          }
        }
        strip.innerHTML = h;
        // palette
        const needPal = !won && ((mode === 'extend') || (mode === 'mistake' && !isGrow && st.found && p.fix !== false));
        pal.innerHTML = needPal ? `<div class="lb-patternbuilder-pll">${mode === 'mistake' ? 'Which tile belongs there?' : 'Tiles'}</div>` + palette.map((s, j) => tile(s, sel === j ? 'lb-patternbuilder-sel' : '', `data-drag="${j}" role="button" aria-label="tile"`)).join('') : '';
        checkB.hidden = !(isGrow && mode === 'extend' && !won);
      }

      // ------------------------------------------------ actions
      function place(j, target) {
        if (won) return;
        const tok = palette[j];
        if (target[0] === 's') {
          const b = +target.slice(1); st.fill[b] = tok; sel = null; api.sfx('tap'); draw();
          const el = strip.querySelector(`[data-drop="s${b}"]`); el && el.classList.add('lb-patternbuilder-pop');
          if (st.fill.filter(x => x != null).length === blanks) checkExtend();
        } else if (target[0] === 't') {
          const b = +target.slice(1); const arr = st.tower[b] || (st.tower[b] = []);
          if (arr.length >= 10) { say('That tower is full.', 'bad'); return; }
          arr.push(tok); api.sfx('tap'); draw(); say(`This tower has ${arr.length} tile${arr.length > 1 ? 's' : ''}.`);
        } else if (target === 'm') {
          sel = null;
          if (tok === seqAt(st.m)) { st.fixedTok = tok; doWin('You fixed the pattern! It goes ' + core.map(s => tk(s).label || tk(s).text || tk(s).shape || '●').join(' ') + ' again and again.'); }
          else { api.sfx('wrong'); draw(); flashBad(strip.querySelector('[data-drop="m"]')); say('Not that one. What comes before and after this spot?', 'bad'); }
        }
      }
      function flashBad(el) { if (!el) return; el.classList.remove('lb-patternbuilder-bad'); void el.offsetWidth; el.classList.add('lb-patternbuilder-bad'); }
      function checkExtend() {
        const wrong = [];
        for (let b = 0; b < blanks; b++) if (st.fill[b] !== seqAt(show + b)) wrong.push(b);
        if (!wrong.length) {
          doWin(`Great! The pattern repeats: ${core.map(s => tk(s).label || tk(s).text || tk(s).shape || '●').join(' ')}.`);
        } else {
          api.sfx('wrong');
          wrong.forEach(b => flashBad(strip.querySelector(`[data-drop="s${b}"]`)));
          say(`${wrong.length} box${wrong.length > 1 ? 'es are' : ' is'} not right yet. Tap a red box to empty it.`, 'bad');
          later(() => { wrong.forEach(b => { if (!won) st.fill[b] = undefined; }); if (!won) draw(); }, 900);
        }
      }
      function checkTowers() {
        let ok = true;
        for (let b = 0; b < blanksN; b++) {
          const want = counts[shownN + b], tok = growTok(shownN + b), arr = st.tower[b] || [];
          if (arr.length !== want || arr.some(s => s !== tok)) ok = false;
        }
        if (ok) { doWin(`Yes! The towers go ${counts.join(', ')}. Each one grows by ${counts[1] - counts[0]}.`); return; }
        api.sfx('hmm');
        const arr = st.tower[0] || [], want = counts[shownN], tok = growTok(shownN);
        let m = 'Not yet. ';
        if (arr.some(s => s !== tok)) m += 'Check which tile this tower uses.';
        else if (arr.length < want) m += 'Look at how much each tower grows. Add more.';
        else if (arr.length > want) m += 'Too many! Tap a tile to take it out.';
        else m += 'Check the next tower too.';
        strip.querySelectorAll('.lb-patternbuilder-dz').forEach(flashBad); say(m, 'bad');
      }
      function tapStrip(el) {
        if (won) return;
        if (mode === 'find') {
          const i = +el.dataset.i; const k = st.picked.indexOf(i);
          if (k >= 0) st.picked.splice(k, 1); else st.picked.push(i);
          api.sfx('tap'); draw();
          if (st.picked.length === P) {
            const s = st.picked.slice().sort((a, b) => a - b);
            const contiguous = s[s.length - 1] - s[0] === P - 1;
            if (contiguous) { st.start = s[0]; doWin(`Yes! ${core.map(s => tk(s).label || tk(s).text || tk(s).shape || '●').join(' ')} is the part that repeats.`); }
            else {
              api.sfx('wrong'); say('Those tiles are not side by side. Pick tiles next to each other.', 'bad');
              s.forEach(i => flashBad(strip.querySelector(`[data-i="${i}"]`))); later(() => { if (!won) { st.picked = []; draw(); } }, 700);
            }
          } else if (st.picked.length > 0) say(`${st.picked.length} picked. Does the pattern start again after them?`);
        } else if (mode === 'mistake' && !isGrow) {
          const i = +el.dataset.i;
          if (st.found) { if (i === st.m && sel != null) place(sel, 'm'); return; }
          if (i === st.m) {
            st.found = true; api.sfx('coin');
            if (p.fix === false) { doWin('You found the tile that broke the pattern!'); return; }
            draw(); say('Found it! Now drag the right tile onto it (or tap a tile, then tap the yellow box).', 'good');
          } else { api.sfx('wrong'); flashBad(el); say('That tile fits the pattern. Look again.', 'bad'); }
        }
      }
      function tapTower(el) {
        if (won || mode !== 'mistake' || st.found) return;
        const k = +el.dataset.g;
        if (k === st.m) { st.found = true; api.sfx('coin'); draw(); if (p.fix === false) { doWin('You found the wrong tower!'); return; } say(`Found it! It has ${st.cnt[k]}. Use − or + to fix it.`, 'good'); }
        else { api.sfx('wrong'); flashBad(el); say('That tower fits. Count each one and look at how it grows.', 'bad'); }
      }

      // ------------------------------------------------ pointer: drag OR tap-select then tap-target
      function dropAt(x, y) { const el = document.elementFromPoint(x, y); return el && host.contains(el) ? el.closest('[data-drop]') : null; }
      function onDown(e) {
        const el = e.target.closest('[data-drag]'); if (!el || !host.contains(el) || won) return;
        e.preventDefault();
        drag = { el, j: +el.dataset.drag, id: e.pointerId, x0: e.clientX, y0: e.clientY, moved: false };
      }
      function onMove(e) {
        if (!drag || e.pointerId !== drag.id) return;
        if (!drag.moved && Math.hypot(e.clientX - drag.x0, e.clientY - drag.y0) > 7) {
          drag.moved = true;
          ghost = drag.el.cloneNode(true); ghost.classList.add('lb-patternbuilder-ghost'); ghost.classList.remove('lb-patternbuilder-sel');
          const r = drag.el.getBoundingClientRect(); ghost.style.width = r.width + 'px'; ghost.style.height = r.height + 'px';
          document.body.appendChild(ghost);
        }
        if (drag.moved) {
          e.preventDefault();
          ghost.style.left = e.clientX + 'px'; ghost.style.top = e.clientY + 'px';
          host.querySelectorAll('.lb-patternbuilder-hot').forEach(x => x.classList.remove('lb-patternbuilder-hot'));
          const t = dropAt(e.clientX, e.clientY); t && t.classList.add('lb-patternbuilder-hot');
        }
      }
      function onUp(e) {
        if (!drag || e.pointerId !== drag.id) return;
        const d = drag; drag = null;
        if (ghost) { ghost.remove(); ghost = null; }
        host.querySelectorAll('.lb-patternbuilder-hot').forEach(x => x.classList.remove('lb-patternbuilder-hot'));
        if (d.moved) { const t = dropAt(e.clientX, e.clientY); if (t) place(d.j, t.dataset.drop); return; }
        // tap on a palette tile
        if (sel === d.j) {
          // second tap: put it into the first empty spot
          sel = null;
          if (mode === 'extend' && !isGrow) { const b = [...Array(blanks).keys()].find(b => st.fill[b] == null); if (b != null) { place(d.j, 's' + b); return; } }
          else if (mode === 'extend' && isGrow) { place(d.j, 't0'); sel = d.j; draw(); return; }
          else if (mode === 'mistake') { place(d.j, 'm'); return; }
          draw(); return;
        }
        sel = d.j; api.sfx('tap'); draw();
        say(mode === 'mistake' ? 'Now tap the yellow box.' : isGrow ? 'Now tap the dashed box to add it.' : 'Now tap an empty box.');
      }
      function onClick(e) {
        const t = e.target;
        if (t.closest('[data-drag]')) return;
        const btn = t.closest('[data-a]');
        if (btn) { if (btn.dataset.a === 'new') { api.sfx('tap'); setup(); } else checkTowers(); return; }
        const pm = t.closest('[data-pm]');
        if (pm) {
          const k = st.m; st.cnt[k] = Math.max(0, Math.min(10, st.cnt[k] + +pm.dataset.pm)); api.sfx('tap');
          if (st.cnt[k] === counts[k]) { doWin(`Fixed! The towers go ${counts.join(', ')}.`); } else { draw(); say(`Now it has ${st.cnt[k]}.`); }
          return;
        }
        const rm = t.closest('[data-rm]');
        if (rm && !won && sel == null) {
          const v = rm.dataset.rm;
          if (v[0] === 's') { st.fill[+v.slice(1)] = undefined; api.sfx('tap'); draw(); say('Box emptied.'); }
          else { const [b, j] = v.split(':').map(Number); st.tower[b].splice(j, 1); api.sfx('tap'); draw(); say(`This tower has ${st.tower[b].length} tile${st.tower[b].length === 1 ? '' : 's'}.`); }
          return;
        }
        const dz = t.closest('[data-drop]');
        if (dz && sel != null) { const j = sel; if (dz.dataset.drop[0] === 't') { place(j, dz.dataset.drop); sel = j; draw(); } else place(j, dz.dataset.drop); return; }
        if (dz && sel == null && !won && mode === 'extend') { say('First pick a tile from the yellow tray.'); return; }
        const g = t.closest('[data-g]'); if (g && isGrow) { tapTower(g); return; }
        const ti = t.closest('[data-i]'); if (ti) { tapStrip(ti); return; }
      }
      host.addEventListener('pointerdown', onDown);
      host.addEventListener('click', onClick);
      window.addEventListener('pointermove', onMove, { passive: false });
      window.addEventListener('pointerup', onUp);
      window.addEventListener('pointercancel', onUp);
      setup();
      return () => {
        timers.forEach(clearTimeout);
        host.removeEventListener('pointerdown', onDown); host.removeEventListener('click', onClick);
        window.removeEventListener('pointermove', onMove); window.removeEventListener('pointerup', onUp); window.removeEventListener('pointercancel', onUp);
        if (ghost) ghost.remove();
      };
    },
    example: { core: ['🍎', '🍌', '🍌'], mode: 'extend', show: 6, blanks: 3, challenge: 'Apple, banana, banana… Fill the 3 empty boxes to continue the pattern!' },
    examples: [
      { core: ['red', 'blue', 'yellow'], mode: 'mistake', show: 9, challenge: 'One bead is the wrong colour. Find it and fix it!' },
      { core: ['क', 'ख', 'ग'], mode: 'find', show: 9, challenge: 'कौन-सा भाग बार-बार आ रहा है? Tap the part that repeats.' },
      { core: ['⭐'], growing: [1, 2, 3, 4], mode: 'extend', show: 3, blanks: 1, challenge: 'The star towers grow: 1, 2, 3… Build the next tower and press Check.' }
    ]
  });
})();
