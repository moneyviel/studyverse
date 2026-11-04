/* StudyVerse Concept Lab: compare — compare and measure length, weight and capacity (Grades 1-5).
 *
 *  length   : objects are bars that start from a common START line (or, at first, out of line).
 *             The child slides them to line up, then taps the longest/shortest, drags rows into
 *             order, or measures one object with a cm ruler or with non-standard units (clips,
 *             hand spans …) laid end to end.
 *  weight   : a two-pan balance that tips realistically (heavier side goes down, equal = level).
 *             The child drags (or taps, then taps a pan) objects onto the pans to compare, then
 *             answers; or balances one object with unit weights (g / kg / cubes …).
 *  capacity : containers of different shapes (tall-thin vs short-wide). The child pours cups
 *             (or a measuring jug) into them to find which holds more, to order them, or to find
 *             how many cups / ml one holds.
 *
 * PARAMS (all optional)
 *   mode      string  'length' | 'weight' | 'capacity'                               default 'length'
 *   objects   array   [{ name, emoji, value }]  value = length in cm | weight in g | capacity in ml.
 *                     2-5 objects (balance/measure use only the target).  default: set for the mode
 *   goal      string  length:   'longest' | 'shortest' | 'order' | 'measure'      default 'longest'
 *                     weight:   'heaviest' | 'lightest' | 'order' | 'balance'     default 'heaviest'
 *                     capacity: 'most' | 'least' | 'order' | 'measure'            default 'most'
 *                     (other names are mapped: longest/heaviest↔most, measure↔balance …)
 *   order     string  'asc' (smallest first) | 'desc' — for goal 'order'           default 'asc'
 *   target    string|number  name or 0-based index of the object to measure/balance  default 0
 *   unit      string  length: 'cm' (ruler) or a non-standard unit name, e.g. 'clips', 'hand spans',
 *                     'matchsticks', 'cubes'.  weight: 'g' | 'kg' (shows 1 kg 200 g) or e.g.
 *                     'cubes', 'marbles'.  capacity: 'cups' | 'glasses' | 'ml' (measuring jug) |
 *                     'spoons' | 'bottles'.        default length 'cm', weight 'g', capacity 'cups'
 *   unitSize  number  size of one non-standard unit: cm (length), g (weight), ml (capacity).
 *                     default clip 3, matchstick 4, cube 2, hand span 15, step 30 (cm);
 *                     cube/marble 10 g; cup 250, glass 200, spoon 5, bottle 500, ml-jug 100 (ml)
 *   unitEmoji string  emoji drawn for one unit                       default 📎 / 🧊 / 🥤 by mode
 *   weights   array   unit weights offered for 'balance' in grams, e.g. [500,200,100,50]
 *                                                  default: g/kg set that can make the answer
 *   lineUp    boolean length: start with bars NOT lined up, so the child must line them up
 *                                                  default true (for longest/shortest)
 *   showValues boolean show each object's value from the start                  default false
 *   challenge string  challenge line                               default generated from goal
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const COLS = ['#8b5cf6', '#2ed3a5', '#ffc93c', '#ff6b6b', '#3b82f6'];
  const r2 = v => Math.round(v * 100) / 100;
  const DEF = {
    length: [{ name: 'Pencil', emoji: '✏️', value: 12 }, { name: 'Crayon', emoji: '🖍️', value: 7 }, { name: 'Ruler', emoji: '📏', value: 15 }],
    weight: [{ name: 'Apple', emoji: '🍎', value: 150 }, { name: 'Watermelon', emoji: '🍉', value: 2000 }, { name: 'Book', emoji: '📕', value: 500 }],
    capacity: [{ name: 'Glass', emoji: '🥛', value: 250 }, { name: 'Jug', emoji: '🫖', value: 1000 }, { name: 'Bottle', emoji: '🍶', value: 750 }]
  };
  const GOALS = {
    length: { longest: 'longest', shortest: 'shortest', order: 'order', measure: 'measure', heaviest: 'longest', most: 'longest', lightest: 'shortest', least: 'shortest', balance: 'measure' },
    weight: { heaviest: 'heaviest', lightest: 'lightest', order: 'order', balance: 'balance', measure: 'balance', longest: 'heaviest', most: 'heaviest', shortest: 'lightest', least: 'lightest' },
    capacity: { most: 'most', least: 'least', order: 'order', measure: 'measure', balance: 'measure', longest: 'most', heaviest: 'most', shortest: 'least', lightest: 'least' }
  };
  const fmtW = (g, unit) => {
    g = Math.round(g);
    if (unit === 'kg' && g >= 1000) { const k = Math.floor(g / 1000), r = g % 1000; return r ? `${k} kg ${r} g` : `${k} kg`; }
    return `${g} g`;
  };
  const fmtC = ml => { ml = Math.round(ml); if (ml >= 1000) { const l = Math.floor(ml / 1000), r = ml % 1000; return r ? `${l} L ${r} ml` : `${l} L`; } return `${ml} ml`; };
  const unitLabel = (n, u) => `${r2(n)} ${n === 1 ? u.replace(/s$/i, '') : u}`;

  Labs.register('compare', {
    title: 'Compare & measure',
    subjects: ['maths', 'evs'],
    render(host, p, api) {
      const mode = ['length', 'weight', 'capacity'].includes(p.mode) ? p.mode : 'length';
      let objs = (Array.isArray(p.objects) ? p.objects : []).filter(o => o && isFinite(+o.value) && +o.value > 0)
        .map((o, i) => ({ name: String(o.name == null ? '' : o.name), emoji: String(o.emoji || (mode === 'length' ? '📏' : mode === 'weight' ? '📦' : '🫙')), value: +o.value, i }));
      if (objs.length < 1) objs = DEF[mode].map((o, i) => Object.assign({ i }, o));
      objs = objs.slice(0, 5);
      let goal = GOALS[mode][p.goal] || { length: 'longest', weight: 'heaviest', capacity: 'most' }[mode];
      if (objs.length < 2 && !['measure', 'balance'].includes(goal)) goal = mode === 'weight' ? 'balance' : 'measure';
      const desc = p.order === 'desc';
      let ti = 0;
      if (typeof p.target === 'number' && objs[p.target]) ti = p.target;
      else if (p.target != null) { const k = objs.findIndex(o => o.name === String(p.target)); if (k >= 0) ti = k; }
      const T = objs[ti];
      const showVals = !!p.showValues;
      const unitIn = p.unit ? String(p.unit).trim() : '';
      const lc = unitIn.toLowerCase();

      // ---- units
      let unit, unitSize, unitEmoji, std;
      if (mode === 'length') {
        unit = unitIn || 'cm'; std = ['cm', 'centimetre', 'centimetres', 'सेमी'].includes(lc) || !unitIn;
        if (std) unit = unitIn && unitIn !== 'centimetres' && unitIn !== 'centimetre' ? unitIn : 'cm';
        const guess = /clip/.test(lc) ? [3, '📎'] : /match/.test(lc) ? [4, '🔥'] : /cube|block/.test(lc) ? [2, '🟧'] : /span|hand|बित्ता|बालिश्त/.test(lc) ? [15, '✋'] : /step|foot|feet|pace|कदम/.test(lc) ? [30, '👣'] : /eras/.test(lc) ? [4, '🧽'] : [3, '📎'];
        unitSize = +p.unitSize > 0 ? +p.unitSize : guess[0]; unitEmoji = p.unitEmoji || guess[1];
      } else if (mode === 'weight') {
        unit = unitIn || 'g'; std = ['g', 'kg', 'gram', 'grams', 'ग्राम', 'किलोग्राम'].includes(lc) || !unitIn;
        if (std) unit = /k|कि/.test(lc) ? 'kg' : (unitIn === 'ग्राम' ? 'g' : (lc === 'kg' ? 'kg' : 'g'));
        unitSize = +p.unitSize > 0 ? +p.unitSize : 10; unitEmoji = p.unitEmoji || (/marble|कंच/.test(lc) ? '🔮' : /coin|सिक्/.test(lc) ? '🪙' : '🧊');
      } else {
        unit = unitIn || 'cups'; std = ['ml', 'millilitre', 'millilitres', 'मिली'].includes(lc);
        const guess = std ? [100, '🧪'] : /glass|गिलास/.test(lc) ? [200, '🥛'] : /spoon|चम्मच/.test(lc) ? [5, '🥄'] : /bottle|बोतल/.test(lc) ? [500, '🍼'] : /mug|मग/.test(lc) ? [300, '☕'] : /bucket|बाल्टी/.test(lc) ? [10000, '🪣'] : /^l$|litre|liter|लीटर/.test(lc) ? [1000, '🫙'] : [250, '🥤'];
        unitSize = +p.unitSize > 0 ? +p.unitSize : guess[0]; unitEmoji = p.unitEmoji || guess[1];
      }
      const uName = mode === 'capacity' && std ? `${unitSize} ml jug` : unit;

      // ---- challenge text
      const nm = o => o.name || o.emoji;
      const chDef = {
        longest: 'Line the objects up at the start. Tap the longest one.',
        shortest: 'Line the objects up at the start. Tap the shortest one.',
        heaviest: 'Use the balance to compare. Which is the heaviest?',
        lightest: 'Use the balance to compare. Which is the lightest?',
        most: `Pour ${unit} into each container. Which holds the most?`,
        least: `Pour ${unit} into each container. Which holds the least?`,
        order: `Put them in order from ${desc ? (mode === 'length' ? 'longest' : mode === 'weight' ? 'heaviest' : 'holds most') : (mode === 'length' ? 'shortest' : mode === 'weight' ? 'lightest' : 'holds least')} to ${desc ? (mode === 'length' ? 'shortest' : mode === 'weight' ? 'lightest' : 'holds least') : (mode === 'length' ? 'longest' : mode === 'weight' ? 'heaviest' : 'holds most')}.`,
        measure: mode === 'length' ? (std ? `How long is the ${nm(T)}? Use the ruler.` : `How many ${unit} long is the ${nm(T)}?`) : `How many ${uName} does the ${nm(T)} hold? Fill it to the top.`,
        balance: `Add weights to balance the ${nm(T)}. How heavy is it?`
      }[goal];

      host.innerHTML = `
<style>
.lb-compare-w{color:#1b1f3a;font-size:14px;position:relative}
.lb-compare-ch{font-weight:800;font-size:14.5px;line-height:1.35;margin-bottom:8px}
.lb-compare-msg{font-size:13px;font-weight:700;color:#6b7090;margin:6px 2px 0;min-height:18px;line-height:1.35}
.lb-compare-msg.good{color:#0f9b74}.lb-compare-msg.bad{color:#e04848}
.lb-compare-row2{display:flex;gap:8px;margin-top:8px}
.lb-compare-b{flex:1;min-height:42px;border:none;border-radius:13px;font-family:inherit;font-weight:800;font-size:14px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0 8px}
.lb-compare-b.go{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-compare-b:active{transform:translateY(2px);box-shadow:none}
.lb-compare-b[hidden]{display:none}
.lb-compare-stage{background:linear-gradient(#f7f5ff,#eef1ff);border-radius:18px;padding:10px 10px 8px}
/* length */
.lb-compare-rows{position:relative}
.lb-compare-lr{position:relative;padding:4px 0 6px;transition:transform .2s;border-radius:12px}
.lb-compare-lr.drag{transition:none;z-index:3;background:rgba(255,255,255,.85);box-shadow:0 6px 16px rgba(27,31,58,.18)}
.lb-compare-lr.sel{background:#efe9ff}
.lb-compare-lab{display:flex;align-items:center;gap:6px;font-weight:800;font-size:13.5px;line-height:1.3;margin-bottom:3px}
.lb-compare-lab span.lb-compare-nn{flex:1;overflow-wrap:anywhere}
.lb-compare-val{font-size:12px;font-weight:900;color:#fff;background:#6b7090;border-radius:999px;padding:1px 8px;white-space:nowrap}
.lb-compare-hd{width:40px;height:30px;flex:none;border-radius:10px;background:#fff;box-shadow:0 0 0 2px #e3e0fb inset;display:flex;align-items:center;justify-content:center;font-size:16px;color:#8b5cf6;cursor:grab;touch-action:none}
.lb-compare-tr{position:relative;height:34px;border-left:3px dashed #ff6b6b;margin-left:2px}
.lb-compare-bar{position:absolute;top:2px;height:30px;border-radius:9px;cursor:grab;touch-action:none;display:flex;align-items:center;padding-left:5px;box-sizing:border-box;font-size:18px;box-shadow:0 3px 0 rgba(27,31,58,.18),inset 0 -6px 0 rgba(0,0,0,.08);transition:left .45s cubic-bezier(.3,1.4,.5,1)}
.lb-compare-bar.nt{transition:none}
.lb-compare-bar.ok{box-shadow:0 0 0 3px #2ed3a5,0 3px 0 rgba(27,31,58,.18)}
.lb-compare-start{font-size:10px;font-weight:900;color:#ff6b6b;letter-spacing:.5px;margin:0 0 2px 0}
.lb-compare-lane{position:relative;height:28px;margin-left:2px;border-left:3px dashed #ff6b6b}
.lb-compare-u{position:absolute;top:2px;height:24px;border-radius:7px;background:#fff;box-shadow:0 0 0 2px #c9c2f7 inset;display:flex;align-items:center;justify-content:center;font-size:15px;box-sizing:border-box;animation:lbcmpin .25s}
.lb-compare-u.drop{background:rgba(255,255,255,.5);box-shadow:0 0 0 2px #b9b2f5 inset;border:2px dashed #b9b2f5;animation:none;color:#8b5cf6;font-weight:900}
@keyframes lbcmpin{from{transform:scale(.4);opacity:0}}
.lb-compare-ruler{position:relative;height:34px;margin-left:2px;background:#fff8dc;border-radius:0 6px 6px 0;box-shadow:inset 0 0 0 1.5px #f0d77a}
.lb-compare-tk{position:absolute;top:0;width:1.5px;background:#7a6520}
.lb-compare-tn{position:absolute;top:15px;font-size:10px;font-weight:800;transform:translateX(-50%);color:#5c4b12}
.lb-compare-step{display:flex;align-items:center;gap:6px;justify-content:center;margin-top:8px;flex-wrap:wrap}
.lb-compare-step button{width:44px;height:42px;border:none;border-radius:12px;background:#8b5cf6;color:#fff;font-size:22px;font-weight:900;cursor:pointer;font-family:inherit}
.lb-compare-step output{min-width:86px;text-align:center;font-size:20px;font-weight:900;background:#fff;border-radius:12px;padding:6px 8px;box-shadow:0 0 0 2px #e3e0fb inset}
/* weight */
.lb-compare-svg{width:100%;height:auto;display:block;touch-action:manipulation}
.lb-compare-tray{display:flex;flex-wrap:wrap;gap:5px;justify-content:center;margin-top:7px;padding:6px;border-radius:16px;background:#fffbea;box-shadow:0 0 0 2px #ffe9a6 inset;min-height:52px;align-items:center}
.lb-compare-tl{width:100%;text-align:center;font-size:11px;font-weight:800;color:#a07a00;text-transform:uppercase;letter-spacing:.4px}
.lb-compare-chip{display:flex;align-items:center;gap:4px;min-height:42px;padding:3px 8px 3px 5px;border-radius:13px;background:#fff;box-shadow:0 3px 0 #dcdff2,0 0 0 2px #e6e8f7 inset;font-weight:800;font-size:13.5px;line-height:1.25;cursor:grab;touch-action:none;user-select:none;-webkit-user-select:none;max-width:100%;box-sizing:border-box}
.lb-compare-chip .lb-compare-ce{font-size:21px;line-height:1;flex:none}
.lb-compare-chip .lb-compare-ct{overflow-wrap:anywhere}
.lb-compare-chip.sel{box-shadow:0 0 0 3px #8b5cf6 inset,0 4px 10px rgba(139,92,246,.35);transform:translateY(-2px)}
.lb-compare-chip.wt{background:linear-gradient(#9aa3b8,#6b7489);color:#fff;box-shadow:0 3px 0 #4a5266;padding:4px 10px}
.lb-compare-ans{display:flex;gap:7px;margin-top:8px}
.lb-compare-slot{flex:1;min-height:52px;border-radius:14px;border:2.5px dashed #b9b2f5;background:rgba(255,255,255,.6);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:3px;box-sizing:border-box;cursor:pointer;min-width:0}
.lb-compare-slot small{font-size:10.5px;font-weight:900;color:#8b5cf6;text-transform:uppercase;letter-spacing:.3px;text-align:center;line-height:1.15}
.lb-compare-slot .lb-compare-sc{font-size:12.5px;font-weight:800;text-align:center;line-height:1.2;overflow-wrap:anywhere}
.lb-compare-slot.hot,.lb-compare-hot{border-color:#8b5cf6!important;background:#f1ecff!important}
.lb-compare-slot.ok{border-style:solid;border-color:#2ed3a5;background:#eafff7}
.lb-compare-bad{animation:lbcmpsh .45s}
@keyframes lbcmpsh{0%,100%{transform:translateX(0)}25%{transform:translateX(-6px)}50%{transform:translateX(6px)}75%{transform:translateX(-3px)}}
.lb-compare-read{display:flex;justify-content:space-between;font-weight:900;font-size:13px;margin-top:2px;gap:6px}
.lb-compare-read .lb-compare-ib{flex:0 0 auto;min-height:36px;min-width:40px;border:none;border-radius:10px;background:#fff;box-shadow:0 0 0 2px #e3e0fb inset;font-family:inherit;font-weight:800;font-size:12.5px;cursor:pointer;color:#1b1f3a;padding:0 8px}
.lb-compare-read{align-items:center}
.lb-compare-row2:empty{display:none}
.lb-compare-read span{white-space:nowrap;background:#fff;border-radius:10px;padding:3px 8px;box-shadow:0 0 0 2px #e3e0fb inset}
/* capacity */
.lb-compare-cons{display:flex;gap:6px;justify-content:space-around;align-items:flex-end}
.lb-compare-con{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;min-width:0;max-width:130px}
.lb-compare-con svg{display:block;width:100%;height:auto;max-height:150px;touch-action:manipulation;cursor:pointer}
.lb-compare-cn{border:none;font-family:inherit;font-weight:800;font-size:12.5px;line-height:1.25;background:#fff;color:#1b1f3a;border-radius:11px;padding:5px 6px;min-height:40px;width:100%;box-shadow:0 0 0 2px #e3e0fb inset;cursor:pointer;overflow-wrap:anywhere;position:relative}
.lb-compare-cn.sel{box-shadow:0 0 0 3px #8b5cf6 inset;background:#f3eeff}
.lb-compare-cn.ok{box-shadow:0 0 0 3px #2ed3a5 inset;background:#eafff7}
.lb-compare-cn b{position:absolute;top:-9px;right:-4px;background:#8b5cf6;color:#fff;border-radius:999px;font-size:11px;min-width:20px;height:20px;line-height:20px}
.lb-compare-cc{font-size:12px;font-weight:900;color:#3b82f6;text-align:center;min-height:16px;line-height:1.2}
.lb-compare-cb{display:flex;gap:4px;width:100%}
.lb-compare-cb button{flex:1;height:40px;border:none;border-radius:11px;font-family:inherit;font-size:15px;font-weight:900;cursor:pointer;background:#e3f0ff;color:#1d4ed8;padding:0}
.lb-compare-cb button.lb-compare-ce{flex:0 0 36px;background:#eef0fb;color:#6b7090}
.lb-compare-src{display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:6px;font-size:12px;font-weight:800;color:#6b7090}
.lb-compare-ghost{position:fixed;z-index:9999;pointer-events:none;transform:translate(-50%,-60%) scale(1.1);opacity:.93;box-shadow:0 8px 20px rgba(27,31,58,.25)!important}
</style>
<div class="lb-compare-w">
  <div class="lb-compare-ch">🎯 Challenge: ${esc(p.challenge || chDef)}</div>
  <div class="lb-compare-body"></div>
  <div class="lb-compare-msg" aria-live="polite"></div>
  <div class="lb-compare-row2"></div>
</div>`;
      const $ = s => host.querySelector(s);
      const body = $('.lb-compare-body'), msgEl = $('.lb-compare-msg'), btnRow = $('.lb-compare-row2');
      let won = false, raf = 0, timers = [];
      const later = (f, ms) => timers.push(setTimeout(f, ms));
      const say = (t, cls = '') => { msgEl.textContent = t; msgEl.className = 'lb-compare-msg ' + cls; };
      const shake = el => { if (!el) return; el.classList.remove('lb-compare-bad'); void el.getBoundingClientRect(); el.classList.add('lb-compare-bad'); };
      const doWin = m => { if (won) return; won = true; say('🎉 ' + m, 'good'); api.sfx('correct'); api.speak(m); api.win(m); };
      const sorted = () => objs.slice().sort((a, b) => desc ? b.value - a.value : a.value - b.value);
      const fmtV = v => mode === 'length' ? `${r2(v)} cm` : mode === 'weight' ? fmtW(v, unit) : fmtC(v);
      const orderOK = arr => arr.every((o, k) => k === 0 || (desc ? arr[k - 1].value >= o.value : arr[k - 1].value <= o.value));

      // ================= generic drag-or-tap (for chips/tokens) =================
      let dsel = null, drag = null, ghost = null, H = {};
      function dropAt(x, y) { const el = document.elementFromPoint(x, y); return el && host.contains(el) ? el.closest('[data-drop]') : null; }
      function onDown(e) {
        const el = e.target.closest('[data-drag]'); if (!el || !host.contains(el) || won) return;
        e.preventDefault();
        drag = { el, key: el.dataset.drag, id: e.pointerId, x0: e.clientX, y0: e.clientY, moved: false };
      }
      function onMove(e) {
        if (!drag || e.pointerId !== drag.id) return;
        if (!drag.moved && Math.hypot(e.clientX - drag.x0, e.clientY - drag.y0) > 7) {
          drag.moved = true;
          const g = document.createElement('div'); g.innerHTML = H.ghost ? H.ghost(drag.key) : drag.el.outerHTML;
          ghost = g.firstElementChild || g; ghost.classList.add('lb-compare-ghost'); ghost.removeAttribute('data-drag'); document.body.appendChild(ghost);
        }
        if (drag.moved) {
          e.preventDefault(); ghost.style.left = e.clientX + 'px'; ghost.style.top = e.clientY + 'px';
          host.querySelectorAll('.hot,.lb-compare-hot').forEach(x => x.classList.remove('hot', 'lb-compare-hot'));
          const t = dropAt(e.clientX, e.clientY); t && t.classList.add(t.tagName === 'DIV' || t.tagName === 'BUTTON' ? 'hot' : 'lb-compare-hot');
        }
      }
      function onUp(e) {
        if (!drag || e.pointerId !== drag.id) return;
        const d = drag; drag = null;
        if (ghost) { ghost.remove(); ghost = null; }
        host.querySelectorAll('.hot,.lb-compare-hot').forEach(x => x.classList.remove('hot', 'lb-compare-hot'));
        if (d.moved) { const t = dropAt(e.clientX, e.clientY); dsel = null; if (t) H.place(d.key, t.dataset.drop); else H.redraw(); return; }
        if (H.tapItem && H.tapItem(d.key)) return;
        dsel = dsel === d.key ? null : d.key; api.sfx('tap'); H.redraw();
        if (dsel) say(H.selHint || 'Now tap where it should go.');
      }
      function onClick(e) {
        if (e.target.closest('[data-drag]')) return;
        const dz = e.target.closest('[data-drop]');
        if (dz && host.contains(dz) && dsel != null && !won) { const k = dsel; dsel = null; H.place(k, dz.dataset.drop); return; }
        H.click && H.click(e);
      }
      host.addEventListener('pointerdown', onDown);
      host.addEventListener('click', onClick);
      window.addEventListener('pointermove', onMove, { passive: false });
      window.addEventListener('pointerup', onUp);
      window.addEventListener('pointercancel', onUp);
      const extraCleanup = [];

      // ======================================================= LENGTH
      if (mode === 'length') {
        const measure = goal === 'measure';
        const list = measure ? [T] : objs.slice();
        const lineUp = !measure && goal !== 'order' ? p.lineUp !== false : p.lineUp === true;
        const maxV = Math.max(...list.map(o => o.value));
        // span of the track in cm
        let span = measure && std ? Math.ceil(maxV) + 3 : maxV * (lineUp ? 1.35 : 1.08);
        if (measure && !std) span = Math.max(maxV, Math.ceil(maxV / unitSize + 1) * unitSize) * 1.04;
        const pct = cm => cm / span * 100;
        let offs = list.map(() => 0), rows = list.slice(), selRow = -1, ans = 0, units = 0, picked = -1;
        const resetL = () => {
          offs = list.map(o => lineUp ? Math.random() * Math.max(0, span - o.value) * .85 : 0);
          if (lineUp && offs.every(x => x < span * .04)) offs[0] = span * .2;
          if (measure && std) offs = [1 + Math.floor(Math.random() * 2)];
          rows = list.slice(); if (goal === 'order') { for (let k = 0; k < 6 && orderOK(rows); k++) rows.sort(() => Math.random() - .5); if (orderOK(rows) && rows.length > 1) rows.reverse(); }
          selRow = -1; ans = 0; units = 0; picked = -1;
        };
        function drawL() {
          let h = `<div class="lb-compare-stage"><div class="lb-compare-start">▼ START</div><div class="lb-compare-rows">`;
          rows.forEach((o, k) => {
            const c = COLS[o.i % COLS.length];
            const sv = showVals || won ? `<span class="lb-compare-val">${measure && !std ? unitLabel(r2(o.value / unitSize), unit) : esc(fmtV(o.value))}</span>` : '';
            h += `<div class="lb-compare-lr${selRow === k ? ' sel' : ''}" data-row="${k}">
              <div class="lb-compare-lab">${goal === 'order' ? `<span class="lb-compare-hd" data-h="${k}" aria-label="move">⇅</span>` : ''}<span>${esc(o.emoji)}</span><span class="lb-compare-nn">${esc(o.name)}</span>${sv}</div>
              <div class="lb-compare-tr"><div class="lb-compare-bar${won && (picked === k || goal === 'order') ? ' ok' : ''}" data-bar="${k}" style="left:${pct(offs[list.indexOf(o)])}%;width:${pct(o.value)}%;background:linear-gradient(90deg,${c},${c}cc)" role="button" aria-label="${esc(o.name)}"></div></div></div>`;
          });
          h += `</div>`;
          if (measure && std) {
            let tk = '';
            for (let c = 0; c <= span; c += .5) { const big = c % 1 === 0; tk += `<div class="lb-compare-tk" style="left:${pct(c)}%;height:${big ? 13 : 7}px"></div>`; if (big && (span <= 22 || c % 5 === 0)) tk += `<div class="lb-compare-tn" style="left:${pct(c)}%">${c}</div>`; }
            h += `<div class="lb-compare-ruler" aria-label="centimetre ruler">${tk}</div><div style="font-size:11px;font-weight:800;color:#6b7090;text-align:right;margin-top:2px">cm</div>`;
          }
          if (measure && !std) {
            let u = '';
            for (let k = 0; k < units; k++) u += `<div class="lb-compare-u" style="left:${pct(k * unitSize)}%;width:${pct(unitSize)}%">${esc(unitEmoji)}</div>`;
            if (!won && (units + 1) * unitSize <= span) u += `<div class="lb-compare-u drop" data-drop="lane" style="left:${pct(units * unitSize)}%;width:${pct(unitSize)}%">+</div>`;
            h += `<div class="lb-compare-lane">${u}</div>`;
          }
          h += `</div>`;
          if (measure && std) h += `<div class="lb-compare-step"><button data-st="-1" aria-label="less">−</button><output>${ans} cm</output><button data-st="1" aria-label="more">+</button></div>`;
          if (measure && !std) h += `<div class="lb-compare-step"><span class="lb-compare-chip" data-drag="unit" style="cursor:grab">${esc(unitEmoji)} <span class="lb-compare-ct">1 ${esc(unit.replace(/s$/i, ''))}</span></span><button data-un="-1" aria-label="remove one">−</button><output>${units}</output><button data-un="1" aria-label="add one">+</button></div>`;
          body.innerHTML = h;
          btnRow.innerHTML = (lineUp ? `<button class="lb-compare-b" data-a="line">⇤ Line up</button>` : '') + (goal === 'order' || measure ? `<button class="lb-compare-b go" data-a="check">✔ Check</button>` : '') + `<button class="lb-compare-b" data-a="new">↺ Reset</button>`;
        }
        H.redraw = drawL;
        H.ghost = () => `<span class="lb-compare-chip">${esc(unitEmoji)}</span>`;
        H.place = (key, drop) => { if (drop === 'lane') addUnit(1); else drawL(); };
        H.selHint = 'Now tap the dashed box to lay it down.';
        function addUnit(d) {
          if (won) return;
          units = Math.max(0, units + d);
          if (units * unitSize > span) { units--; say('That is far past the end!', 'bad'); return; }
          api.sfx('tap'); drawL();
          const end = units * unitSize;
          say(units ? (end < T.value - 1e-9 ? `${units} laid. The ${nm(T)} is still longer.` : Math.abs(end - T.value) < 1e-9 ? `${units} laid. They reach the end exactly!` : `${units} laid. That goes past the end.`) : '');
        }
        // bar drag (horizontal) and row reorder (vertical)
        let bd = null;
        function bDown(e) {
          if (won) return;
          const bar = e.target.closest('[data-bar]'), hd = e.target.closest('[data-h]');
          if (!bar && !hd) return;
          e.preventDefault(); e.stopPropagation();
          if (hd) { const row = hd.closest('.lb-compare-lr'); bd = { kind: 'row', k: +hd.dataset.h, row, id: e.pointerId, y0: e.clientY, x0: e.clientX, moved: false }; return; }
          const k = +bar.dataset.bar, o = rows[k], li = list.indexOf(o);
          bd = { kind: 'bar', k, li, bar, id: e.pointerId, x0: e.clientX, y0: e.clientY, off0: offs[li], W: bar.parentElement.getBoundingClientRect().width, moved: false };
        }
        function bMove(e) {
          if (!bd || e.pointerId !== bd.id) return;
          const dx = e.clientX - bd.x0, dy = e.clientY - bd.y0;
          if (!bd.moved && Math.hypot(dx, dy) > 6) { bd.moved = true; if (bd.kind === 'row') bd.row.classList.add('drag'); else bd.bar.classList.add('nt'); }
          if (!bd.moved) return;
          e.preventDefault();
          if (bd.kind === 'bar') {
            const o = list[bd.li]; let off = bd.off0 + dx / bd.W * span;
            off = Math.max(0, Math.min(span - o.value, off));
            if (measure && std) off = Math.round(off * 2) / 2; else if (off < span * .03) off = 0;
            offs[bd.li] = off; bd.bar.style.left = pct(off) + '%';
          } else bd.row.style.transform = `translateY(${dy}px)`;
        }
        function bUp(e) {
          if (!bd || e.pointerId !== bd.id) return;
          const d = bd; bd = null;
          if (d.kind === 'bar') {
            d.bar.classList.remove('nt');
            if (d.moved) { api.sfx('tap'); if (offs[d.li] === 0 && !(measure && std)) say('Lined up at the start ✔'); if (measure && std) say(offs[d.li] === 0 ? 'Its start is at 0 on the ruler ✔' : `Its start is at ${offs[d.li]} cm.`); return; }
            tapRow(d.k); return;
          }
          if (!d.moved) { tapRow(d.k); return; }
          // reorder
          const els = [...body.querySelectorAll('.lb-compare-lr')];
          let to = 0; els.forEach((el, j) => { if (j === d.k) return; const r = el.getBoundingClientRect(); if (e.clientY > r.top + r.height / 2) to++; });
          const [o] = rows.splice(d.k, 1); rows.splice(to, 0, o); selRow = -1; api.sfx('tap'); drawL();
        }
        function tapRow(k) {
          if (won) return;
          if (goal === 'order') {
            if (selRow < 0) { selRow = k; api.sfx('tap'); drawL(); say('Now tap another one to swap them.'); return; }
            if (selRow !== k) { [rows[selRow], rows[k]] = [rows[k], rows[selRow]]; api.sfx('tap'); }
            selRow = -1; drawL(); say(''); return;
          }
          if (measure) return;
          const o = rows[k], vals = list.map(x => x.value);
          const best = goal === 'longest' ? Math.max(...vals) : Math.min(...vals);
          if (o.value === best) {
            picked = k; offs = list.map(() => 0); won = false; drawL();
            const all = list.slice().sort((a, b) => b.value - a.value).map(x => nm(x)).join(' > ');
            doWin(`Yes! The ${nm(o)} is the ${goal}. ${list.length > 2 ? 'Longest to shortest: ' + all + '.' : ''}`); drawL();
          } else {
            api.sfx('wrong'); shake(body.querySelector(`[data-bar="${k}"]`));
            const aligned = offs.every(x => x === 0);
            say(aligned ? `Not the ${goal}. Compare where each one ends.` : `Hmm. Line them up at the START first, then compare the ends.`, 'bad');
          }
        }
        H.click = e => {
          const a = e.target.closest('[data-a]');
          if (a) {
            if (a.dataset.a === 'new') { won = false; api.resetWin && api.resetWin(); resetL(); drawL(); say(''); return; }
            if (won) return;
            if (a.dataset.a === 'line') { offs = offs.map(() => 0); api.sfx('tap'); drawL(); say('All lined up at the START. Now compare the ends.'); return; }
            if (a.dataset.a === 'check') {
              if (goal === 'order') {
                if (orderOK(rows)) { doWin(`Correct order: ${rows.map(nm).join(', ')}.`); drawL(); }
                else { api.sfx('wrong'); say('Not in order yet. Line them up and look at the ends.', 'bad'); shake(body.querySelector('.lb-compare-rows')); }
              } else if (std) {
                if (Math.abs(ans - Math.round(T.value)) < 1e-9) { doWin(`Yes! The ${nm(T)} is ${r2(T.value)} cm long.`); drawL(); }
                else { api.sfx('wrong'); say(offs[0] !== 0 ? 'Tip: slide it so its start is at 0, then read the end.' : `Not ${ans} cm. Read the number at its end.`, 'bad'); }
              } else {
                const need = Math.round(T.value / unitSize), exact = Math.abs(T.value / unitSize - need) < 1e-9;
                if (units === need) { doWin(`Yes! The ${nm(T)} is ${exact ? '' : 'about '}${need} ${need === 1 ? unit.replace(/s$/i, '') : unit} long.`); drawL(); }
                else { api.sfx('wrong'); say(units < need ? `Not yet: lay ${unit} until they reach the end.` : `Too many ${unit} — they go past the end.`, 'bad'); }
              }
            }
            return;
          }
          const st = e.target.closest('[data-st]'); if (st && !won) { ans = Math.max(0, Math.min(200, ans + +st.dataset.st)); api.sfx('tap'); drawL(); return; }
          const un = e.target.closest('[data-un]'); if (un && !won) { addUnit(+un.dataset.un); return; }
          const lane = e.target.closest('[data-drop="lane"]'); if (lane && !won) addUnit(1);
        };
        body.addEventListener('pointerdown', bDown);
        window.addEventListener('pointermove', bMove, { passive: false });
        window.addEventListener('pointerup', bUp); window.addEventListener('pointercancel', bUp);
        extraCleanup.push(() => { body.removeEventListener('pointerdown', bDown); window.removeEventListener('pointermove', bMove); window.removeEventListener('pointerup', bUp); window.removeEventListener('pointercancel', bUp); });
        resetL(); drawL();
        say(goal === 'order' ? 'Drag ⇅ to move a row, or tap two rows to swap them.' : measure ? (std ? 'Slide the object so it starts at 0. Read the ruler.' : `Lay ${unit} end to end: drag ${unitEmoji} to the dashed box or press +.`) : lineUp ? 'Slide each bar to the red START line (or press Line up).' : 'Tap the one you choose.');
      }

      // ======================================================= WEIGHT
      if (mode === 'weight') {
        const bal = goal === 'balance';
        let weights;
        if (bal) {
          if (!std) weights = [unitSize];
          else if (Array.isArray(p.weights) && p.weights.length) weights = [...new Set(p.weights.map(Number).filter(x => x > 0))].sort((a, b) => b - a).slice(0, 6);
          else {
            const SER = [5000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1];
            let rem = Math.round(T.value); const use = new Set();
            SER.forEach(s => { while (rem >= s) { rem -= s; use.add(s); } });
            SER.filter(s => s <= T.value).slice(0, 3).forEach(s => use.add(s));
            weights = [...use].sort((a, b) => b - a).slice(0, 6);
          }
        }
        const wName = w => std ? (w >= 1000 && w % 1000 === 0 ? `${w / 1000} kg` : `${w} g`) : unitEmoji;
        let loc = {}, pans = { L: [], R: [] }, wid = 0, rank = [], pick = null;
        const items = {}; // key -> {w, label, emoji}
        objs.forEach(o => { items['o' + o.i] = { w: o.value, emoji: o.emoji, label: o.name, o }; });
        const resetW = () => {
          pans = { L: [], R: [] }; rank = objs.map(() => null); pick = null; loc = {};
          Object.keys(items).forEach(k => { if (k[0] === 'w') delete items[k]; });
          if (bal) { pans.L = ['o' + T.i]; }
        };
        const panW = s => pans[s].reduce((a, k) => a + items[k].w, 0);
        let ang = 0, vel = 0, last = 0;
        const targetAng = () => {
          const a = panW('L'), b = panW('R');
          if (Math.abs(a - b) < 1e-9) return 0;
          const m0 = Math.max(...objs.map(o => o.value)) * .15 + 1;
          return 15 * Math.tanh(3 * (b - a) / (a + b + m0));
        };
        function svgPan(s) {
          const ks = pans[s];
          let it = '';
          const n = ks.length, per = 4;
          ks.forEach((k, j) => {
            const row = Math.floor(j / per), col = j % per, inRow = Math.min(per, n - row * per);
            const x = (col - (inRow - 1) / 2) * 26, y = 52 - row * 22;
            const I = items[k];
            if (k[0] === 'w' && std) it += `<g data-drag="${k}" style="cursor:pointer"><path d="M${x - 11} ${y + 4} L${x - 8} ${y - 14} L${x + 8} ${y - 14} L${x + 11} ${y + 4} Z" fill="#7b8499" stroke="#4a5266" stroke-width="1.2"/><text x="${x}" y="${y - 2}" font-size="7.5" font-weight="900" fill="#fff" text-anchor="middle">${esc(wName(I.w))}</text></g>`;
            else it += `<text data-drag="${k}" x="${x}" y="${y}" font-size="22" text-anchor="middle" style="cursor:pointer">${esc(I.emoji)}</text>`;
          });
          return `<line x1="0" y1="0" x2="-44" y2="56" stroke="#9aa0c0" stroke-width="2"/><line x1="0" y1="0" x2="44" y2="56" stroke="#9aa0c0" stroke-width="2"/>
            <rect data-drop="${s}" x="-58" y="4" width="116" height="66" fill="transparent"/>
            <path data-drop="${s}" d="M-52 56 Q0 76 52 56 Z" fill="#ffc93c" stroke="#d9a300" stroke-width="2"/>${it}`;
        }
        function fillPans() { const svg = body.querySelector('.lb-compare-svg'); if (!svg) return; svg.querySelector('.lb-compare-pl').innerHTML = svgPan('L'); svg.querySelector('.lb-compare-pr').innerHTML = svgPan('R'); drawScene(); }
        function drawScene() {
          const svg = body.querySelector('.lb-compare-svg'); if (!svg) return;
          const a = ang * Math.PI / 180, cx = 180, cy = 44, Lh = 108;
          svg.querySelector('.lb-compare-beam').setAttribute('transform', `rotate(${ang} ${cx} ${cy})`);
          svg.querySelector('.lb-compare-pl').setAttribute('transform', `translate(${cx - Lh * Math.cos(a)} ${cy - Lh * Math.sin(a)})`);
          svg.querySelector('.lb-compare-pr').setAttribute('transform', `translate(${cx + Lh * Math.cos(a)} ${cy + Lh * Math.sin(a)})`);
          svg.querySelector('.lb-compare-needle').setAttribute('transform', `rotate(${ang} ${cx} ${cy})`);
        }
        function tick(t) {
          const dt = Math.min(.05, last ? (t - last) / 1000 : .016); last = t;
          const tg = targetAng();
          vel += ((tg - ang) * 28 - vel * 5.5) * dt; ang += vel * dt;
          if (Math.abs(tg - ang) < .02 && Math.abs(vel) < .02) { ang = tg; vel = 0; drawScene(); raf = 0; last = 0; return; }
          drawScene(); raf = requestAnimationFrame(tick);
        }
        const kick = () => { if (!raf) { last = 0; raf = requestAnimationFrame(tick); } };
        function readout() {
          const a = panW('L'), b = panW('R');
          const st = bal ? (Math.abs(a - b) < 1e-9 ? '⚖ Level' : a > b ? '⬇ Left' : '⬇ Right') : Math.abs(a - b) < 1e-9 ? (a ? '⚖ Level — equal' : 'Empty') : (a > b ? '⬇ Left is heavier' : '⬇ Right is heavier');
          const B1 = `<button class="lb-compare-ib" data-a="clear" aria-label="empty the pans">⤺ Clear</button>`, B2 = `<button class="lb-compare-ib" data-a="new" aria-label="reset">↺</button>`;
          if (bal) return `<div class="lb-compare-read">${B1}${B2}<span>${esc(T.emoji)} ${won ? esc(std ? fmtW(T.value, unit) : `${pans.R.length} ${unit}`) : '?'}</span><span>${st}</span><span>${std ? fmtW(b, unit) : `${pans.R.length} ${esc(unit)}`}</span></div>`;
          return `<div class="lb-compare-read">${B1}<span>${st}</span>${B2}</div>`;
        }
        function drawW() {
          const inTray = Object.keys(items).filter(k => k[0] === 'o' && !pans.L.includes(k) && !pans.R.includes(k) && !rank.includes(k) && pick !== k);
          let h = `<div class="lb-compare-stage"><svg class="lb-compare-svg" viewBox="0 10 360 160" role="img" aria-label="pan balance">
            <rect x="140" y="160" width="80" height="8" rx="4" fill="#c9cdea"/><path d="M180 44 L165 162 L195 162 Z" fill="#b5bae0"/>
            <g class="lb-compare-needle"><path d="M180 44 L180 76" stroke="#ff6b6b" stroke-width="3.5" stroke-linecap="round"/></g>
            <path d="M168 92 A 18 18 0 0 0 192 92" fill="none" stroke="#6b7090" stroke-width="1.5"/><line x1="180" y1="86" x2="180" y2="98" stroke="#6b7090" stroke-width="1.5"/>
            <g class="lb-compare-beam"><rect x="68" y="39" width="224" height="10" rx="5" fill="#6b7090"/><circle cx="180" cy="44" r="7" fill="#ffc93c" stroke="#1b1f3a" stroke-width="2"/></g>
            <g class="lb-compare-pl"></g><g class="lb-compare-pr"></g></svg>${readout()}</div>`;
          h += `<div class="lb-compare-tray" data-drop="tray">`;
          if (bal) h += weights.map(w => `<span class="lb-compare-chip wt${dsel === 'W' + w ? ' sel' : ''}" data-drag="W${w}">${std ? '⚖ ' : `<span class="lb-compare-ce">${esc(unitEmoji)}</span>`}<span class="lb-compare-ct">${esc(std ? wName(w) : '1 ' + unit.replace(/s$/i, ''))}</span></span>`).join('');
          else h += inTray.map(k => chip(k)).join('') || '<span style="font-size:12px;color:#a07a00;font-weight:700">(all objects are out)</span>';
          h += `</div>`;
          if (goal === 'heaviest' || goal === 'lightest') h += `<div class="lb-compare-ans"><div class="lb-compare-slot${won ? ' ok' : ''}" data-drop="pick"><small>🏆 ${goal === 'heaviest' ? 'Heaviest' : 'Lightest'}</small>${pick ? `<span class="lb-compare-sc">${esc(items[pick].emoji)} ${esc(items[pick].label)}</span>` : ''}</div></div>`;
          if (goal === 'order') h += `<div class="lb-compare-ans">${rank.map((k, j) => `<div class="lb-compare-slot${won ? ' ok' : ''}" data-drop="r${j}"><small>${j === 0 ? (desc ? 'Heaviest' : 'Lightest') : j === rank.length - 1 ? (desc ? 'Lightest' : 'Heaviest') : j + 1}</small>${k ? `<span class="lb-compare-sc" data-drag="${k}">${esc(items[k].emoji)} ${esc(items[k].label)}</span>` : ''}</div>`).join('')}</div>`;
          body.innerHTML = h;
          fillPans();
          btnRow.innerHTML = '';
        }
        const chip = k => `<span class="lb-compare-chip${dsel === k ? ' sel' : ''}" data-drag="${k}"><span class="lb-compare-ce">${esc(items[k].emoji)}</span><span class="lb-compare-ct">${esc(items[k].label)}</span></span>`;
        H.redraw = drawW;
        H.ghost = k => k[0] === 'W' ? `<span class="lb-compare-chip wt">${esc(std ? wName(+k.slice(1)) : unitEmoji)}</span>` : k[0] === 'w' ? `<span class="lb-compare-chip wt">${esc(std ? wName(items[k].w) : unitEmoji)}</span>` : chip(k);
        H.selHint = bal ? 'Now tap the right pan.' : 'Now tap a pan or a box.';
        const takeOut = k => { ['L', 'R'].forEach(s => { pans[s] = pans[s].filter(x => x !== k); }); rank = rank.map(x => x === k ? null : x); if (pick === k) pick = null; };
        H.tapItem = key => {
          // tapping something on a pan or in a slot sends it back to the tray
          if (key[0] === 'w') { takeOut(key); delete items[key]; api.sfx('tap'); drawW(); kick(); return true; }
          if (key[0] === 'o' && (pans.L.includes(key) || pans.R.includes(key) || rank.includes(key))) {
            if (bal && key === 'o' + T.i) return true;
            takeOut(key); api.sfx('tap'); dsel = null; drawW(); kick(); return true;
          }
          return false;
        };
        H.place = (key, drop) => {
          if (won) return;
          if (bal && key === 'o' + T.i) { drawW(); return; }
          if (key[0] === 'W') { // new unit weight
            if (drop !== 'R' && drop !== 'L') { drawW(); return; }
            if (pans[drop].length >= 12) { say('That pan is full!', 'bad'); drawW(); return; }
            const k = 'w' + (++wid); items[k] = { w: +key.slice(1), emoji: unitEmoji, label: '' }; pans[drop].push(k);
          } else if (key[0] === 'w') { takeOut(key); if (drop === 'L' || drop === 'R') pans[drop].push(key); else delete items[key]; }
          else {
            if (drop === 'L' || drop === 'R') { takeOut(key); if (pans[drop].length >= 8) { say('That pan is full!', 'bad'); drawW(); return; } pans[drop].push(key); }
            else if (drop === 'tray') takeOut(key);
            else if (drop === 'pick') { takeOut(key); pick = key; }
            else if (drop[0] === 'r') { const j = +drop.slice(1); takeOut(key); rank[j] = key; }
          }
          api.sfx('tap'); dsel = null; drawW(); kick(); check();
        };
        function check() {
          const a = panW('L'), b = panW('R');
          if (bal) {
            const ok = Math.abs(a - b) < 1e-9 || (!std && Math.abs(a - b) < unitSize / 2 && b > 0);
            if (ok) { doWin(`Balanced! The ${nm(T)} weighs ${std ? fmtW(T.value, unit) : `${Math.abs(a - b) < 1e-9 ? '' : 'about '}${pans.R.length} ${unit}`}.`); drawW(); return; }
            say(b === 0 ? '' : b < a ? `Right pan: ${std ? fmtW(b, unit) : pans.R.length + ' ' + unit}. Left side still goes down — add more.` : 'Too much! The right side went down. Tap a weight to take it off.', b > a ? 'bad' : '');
            return;
          }
          if (pick) {
            const vals = objs.map(o => o.value), best = goal === 'heaviest' ? Math.max(...vals) : Math.min(...vals);
            if (items[pick].w === best) { const s = objs.slice().sort((x, y) => y.value - x.value).map(nm).join(' > '); doWin(`Yes! The ${nm(items[pick].o)} is the ${goal}. Heaviest to lightest: ${s}.`); drawW(); }
            else { api.sfx('wrong'); const k = pick; pick = null; later(() => { drawW(); }, 50); say(`Not the ${goal}. Put two things on the pans and see which side goes down.`, 'bad'); }
            return;
          }
          if (goal === 'order' && rank.every(Boolean)) {
            const arr = rank.map(k => items[k].o);
            if (orderOK(arr)) { doWin(`Correct! ${arr.map(nm).join(', ')}.`); drawW(); }
            else { api.sfx('wrong'); say('Not in order yet. Test pairs on the balance.', 'bad'); body.querySelectorAll('.lb-compare-slot').forEach(shake); }
            return;
          }
          if (a || b) say(Math.abs(a - b) < 1e-9 ? 'Level: both sides weigh the same.' : `The ${a > b ? 'left' : 'right'} side went down, so it is heavier.`);
        }
        H.click = e => {
          const a = e.target.closest('[data-a]'); if (!a) return;
          if (a.dataset.a === 'new') { won = false; api.resetWin && api.resetWin(); resetW(); drawW(); kick(); say(''); return; }
          if (won) return;
          if (a.dataset.a === 'clear') { pans.R.concat(pans.L).forEach(k => { if (k[0] === 'w') delete items[k]; }); pans = { L: bal ? ['o' + T.i] : [], R: [] }; api.sfx('tap'); drawW(); kick(); say(''); }
        };
        resetW(); ang = targetAng(); drawW(); kick();
        say(bal ? 'Drag a weight onto the right pan (or tap it, then the pan).' : 'Drag objects onto the pans (or tap one, then a pan).');
      }

      // ======================================================= CAPACITY
      if (mode === 'capacity') {
        const meas = goal === 'measure';
        const list = meas ? [T] : objs.slice();
        const maxC = Math.max(...list.map(o => o.value));
        const ASP = [2.3, .75, 1.5, 1.05, 1.9];
        // area ∝ capacity; vary aspect so the eye can be fooled
        const dims = list.map((o, k) => {
          const A = (meas ? 9000 : 7600) * o.value / maxC; let hh = Math.sqrt(A * ASP[k % ASP.length]), ww = A / hh;
          if (hh > 112) { hh = 112; ww = A / hh; } if (ww > 92) { ww = 92; hh = Math.min(112, A / ww); }
          return { w: Math.max(18, ww), h: Math.max(14, hh) };
        });
        let fill = list.map(() => 0), spill = list.map(() => false), rankC = [], pickC = -1;
        const cupsIn = k => fill[k] / unitSize;
        function conSVG(k) {
          const o = list[k], d = dims[k], W = 100, Hh = 122, x0 = (W - d.w) / 2, y0 = Hh - 4 - d.h;
          const lvl = Math.min(1, fill[k] / o.value), wh = d.h * lvl;
          let marks = '';
          if (std && meas) { for (let m = unitSize; m < o.value; m += unitSize) { const y = Hh - 4 - d.h * m / o.value; marks += `<line x1="${x0 + d.w - 9}" x2="${x0 + d.w}" y1="${y}" y2="${y}" stroke="#94a3b8" stroke-width="1"/>`; } }
          return `<svg viewBox="0 0 ${W} ${Hh}" data-drop="c${k}" role="img" aria-label="${esc(o.name)}">
            <rect data-drop="c${k}" x="0" y="0" width="${W}" height="${Hh}" fill="transparent"/>
            <rect x="${x0}" y="${Hh - 4 - wh}" width="${d.w}" height="${wh}" fill="#60a5fa" opacity=".85" style="transition:all .4s"/>
            ${wh > 0 ? `<rect x="${x0}" y="${Hh - 4 - wh}" width="${d.w}" height="3" fill="#bfdbfe" style="transition:all .4s"/>` : ''}
            ${marks}
            <path d="M${x0} ${y0 - 2} L${x0} ${Hh - 10} Q${x0} ${Hh - 4} ${x0 + 6} ${Hh - 4} L${x0 + d.w - 6} ${Hh - 4} Q${x0 + d.w} ${Hh - 4} ${x0 + d.w} ${Hh - 10} L${x0 + d.w} ${y0 - 2}" fill="rgba(255,255,255,.25)" stroke="#475569" stroke-width="2.5" stroke-linejoin="round"/>
            <ellipse cx="${W / 2}" cy="${y0 - 2}" rx="${d.w / 2}" ry="2.5" fill="none" stroke="#475569" stroke-width="1.5"/>
            ${spill[k] ? `<path d="M${x0 + d.w} ${y0} q6 6 3 ${Math.min(30, d.h)}" stroke="#60a5fa" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="${Math.min(W - 4, x0 + d.w + 5)}" cy="${Hh - 6}" r="4" fill="#60a5fa"/>` : ''}
            <text x="${W / 2}" y="${Math.max(16, y0 - 8)}" text-anchor="middle" font-size="16">${esc(o.emoji)}</text>
          </svg>`;
        }
        function drawC() {
          let h = `<div class="lb-compare-stage"><div class="lb-compare-src"><span class="lb-compare-chip${dsel === 'cup' ? ' sel' : ''}" data-drag="cup"><span class="lb-compare-ce">${esc(unitEmoji)}</span><span class="lb-compare-ct">${std ? `${unitSize} ml` : '1 ' + esc(unit.replace(/s$/i, ''))}</span></span><span>← drag to pour</span><button class="lb-compare-b" data-a="new" style="flex:0 0 auto;min-height:40px" aria-label="reset">↺</button></div><div class="lb-compare-cons">`;
          list.forEach((o, k) => {
            const n = cupsIn(k);
            const cnt = fill[k] ? (std ? fmtC(Math.min(fill[k], o.value)) : `${r2(n)} ${n === 1 ? unit.replace(/s$/i, '') : unit}`) + (spill[k] ? ' 💦' : fill[k] >= o.value ? ' full' : '') : (showVals || won ? fmtC(o.value) : '');
            const rk = rankC.indexOf(k);
            h += `<div class="lb-compare-con">${conSVG(k)}<div class="lb-compare-cc">${esc(cnt)}</div>
              <div class="lb-compare-cb"><button data-pour="${k}" aria-label="pour one">+${esc(unitEmoji)}</button><button class="lb-compare-ce" data-empty="${k}" aria-label="empty">↺</button></div>
              ${meas ? `<div class="lb-compare-cn" style="cursor:default">${esc(o.name)}</div>` : `<button class="lb-compare-cn${won && (pickC === k || goal === 'order') ? ' ok' : rk >= 0 || pickC === k ? ' sel' : ''}" data-pick="${k}">${esc(o.name || o.emoji)}${rk >= 0 ? `<b>${rk + 1}</b>` : ''}</button>`}</div>`;
          });
          h += `</div></div>`;
          body.innerHTML = h;
          btnRow.innerHTML = '';
        }
        H.redraw = drawC;
        H.ghost = () => `<span class="lb-compare-chip"><span class="lb-compare-ce">${esc(unitEmoji)}</span></span>`;
        H.selHint = 'Now tap a container to pour.';
        function pour(k) {
          if (won) return;
          const o = list[k];
          if (spill[k]) { say('It is already overflowing! Empty it (↺) to start again.', 'bad'); return; }
          fill[k] += unitSize; api.sfx('tap');
          if (fill[k] > o.value + 1e-9) spill[k] = true;
          drawC();
          const n = cupsIn(k);
          if (meas) {
            const exact = Math.abs(fill[k] - o.value) < unitSize / 2;
            if (exact && !spill[k]) { doWin(`Full! The ${nm(o)} holds ${std ? fmtC(o.value) : `${r2(n)} ${unit}`}${!std ? ` (${fmtC(o.value)})` : ''}.`); drawC(); return; }
            if (spill[k]) { say('Oops, it overflowed! Empty it and pour again — stop when it is just full.', 'bad'); api.sfx('wrong'); return; }
            say(`${std ? fmtC(fill[k]) : `${r2(n)} ${unit}`} poured. Keep going until it is full.`);
          } else {
            if (spill[k]) say(`The ${nm(o)} overflowed on ${unit === 'ml' ? fmtC(fill[k]) : 'pour ' + n}. It holds ${std ? 'less than ' + fmtC(fill[k]) : `${Math.floor(o.value / unitSize + 1e-9)} full ${unit}`}.`);
            else if (Math.abs(fill[k] - o.value) < 1e-9) say(`The ${nm(o)} is full: ${std ? fmtC(fill[k]) : `${r2(n)} ${unit}`}.`, 'good');
            else say(`${std ? fmtC(fill[k]) : `${r2(n)} ${unit}`} in the ${nm(o)}.`);
          }
        }
        H.place = (key, drop) => { if (drop && drop[0] === 'c') pour(+drop.slice(1)); else drawC(); };
        H.click = e => {
          const a = e.target.closest('[data-a]');
          if (a) { won = false; api.resetWin && api.resetWin(); fill = list.map(() => 0); spill = list.map(() => false); rankC = []; pickC = -1; drawC(); say(''); return; }
          if (won) return;
          const pb = e.target.closest('[data-pour]'); if (pb) { pour(+pb.dataset.pour); return; }
          const eb = e.target.closest('[data-empty]'); if (eb) { const k = +eb.dataset.empty; fill[k] = 0; spill[k] = false; api.sfx('tap'); drawC(); say(''); return; }
          const pk = e.target.closest('[data-pick]');
          if (pk) {
            const k = +pk.dataset.pick;
            if (goal === 'order') {
              const at = rankC.indexOf(k);
              if (at >= 0) rankC.splice(at); else rankC.push(k);
              api.sfx('tap'); drawC();
              if (rankC.length === list.length) {
                const arr = rankC.map(j => list[j]);
                if (orderOK(arr)) { doWin(`Correct! ${arr.map(nm).join(', ')}.`); drawC(); }
                else { api.sfx('wrong'); say('Not in order yet. Pour cups to test. Tap a name to undo.', 'bad'); shake(body.querySelector('.lb-compare-cons')); }
              } else say(`Tap the ${desc ? 'next biggest' : 'next smallest'}. (${rankC.length} of ${list.length})`);
              return;
            }
            const vals = list.map(o => o.value), best = goal === 'most' ? Math.max(...vals) : Math.min(...vals);
            if (list[k].value === best) { pickC = k; const s = list.slice().sort((x, y) => y.value - x.value).map(o => `${nm(o)} ${fmtC(o.value)}`).join(' > '); doWin(`Yes! The ${nm(list[k])} holds the ${goal}. ${s}.`); drawC(); }
            else { api.sfx('wrong'); shake(pk); say(`Not that one. A tall container does not always hold more — pour and count!`, 'bad'); }
          }
        };
        drawC();
        say(meas ? `Pour ${unit === 'ml' ? 'the jug' : unit} in: drag ${unitEmoji} onto the container or press +.` : goal === 'order' ? `Pour to test, then tap the names in order (${desc ? 'most' : 'least'} first).` : 'Pour to test (drag the cup or press +). Then tap the name of your answer.');
      }

      return () => {
        cancelAnimationFrame(raf); timers.forEach(clearTimeout); extraCleanup.forEach(f => f());
        host.removeEventListener('pointerdown', onDown); host.removeEventListener('click', onClick);
        window.removeEventListener('pointermove', onMove); window.removeEventListener('pointerup', onUp); window.removeEventListener('pointercancel', onUp);
        if (ghost) ghost.remove();
      };
    },
    example: {
      mode: 'weight', goal: 'heaviest', unit: 'g',
      objects: [{ name: 'Apple', emoji: '🍎', value: 150 }, { name: 'Pumpkin', emoji: '🎃', value: 1200 }, { name: 'School bag', emoji: '🎒', value: 900 }],
      challenge: 'Which is the heaviest? Test them on the balance, then drop it in the 🏆 box.'
    },
    examples: [
      { mode: 'length', goal: 'longest', unit: 'cm', objects: [{ name: 'Snake', emoji: '🐍', value: 14 }, { name: 'Caterpillar', emoji: '🐛', value: 9 }, { name: 'पेंसिल (pencil)', emoji: '✏️', value: 11 }], challenge: 'Who is the longest? Line them up at the start first!' },
      { mode: 'length', goal: 'measure', unit: 'clips', objects: [{ name: 'Crayon', emoji: '🖍️', value: 9 }], challenge: 'How many paper clips long is the crayon?' },
      { mode: 'capacity', goal: 'most', unit: 'cups', objects: [{ name: 'Tall glass', emoji: '🥛', value: 500 }, { name: 'Wide bowl', emoji: '🥣', value: 750 }, { name: 'Mug', emoji: '☕', value: 250 }], challenge: 'Which one holds the most water? Pour cups to find out.' }
    ]
  });
})();
