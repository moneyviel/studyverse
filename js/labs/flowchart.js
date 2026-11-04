/* StudyVerse Concept Lab: flowchart — animated process flow with yes/no branches and an
   "arrange the steps" challenge.

   PARAMS (all optional — missing ones fall back to `example`)
   ─────────────────────────────────────────────────────────────────────────────────────────
   title     string   Heading text.                                              'Process'
   nodes     object[] Steps: {id, emoji?, text, info?, type?:'step'|'decision'}. A 'decision'
                      node asks a question; its outgoing edges carry labels (e.g. 'Yes'/'No').
   edges     object[] Arrows {from, to, label?}. Missing → nodes are joined in array order.
                      Arrows that go back up (loops) are drawn on the right side.
   order     string[] Node ids for the arrange challenge, in the correct order.
                      Default: the main path from the first node (first arrow at each branch).
   task      string   'arrange' (sort shuffled steps) | 'play' (play the flow to the end). 'arrange'
   challenge string   Challenge text (else generated).
   speed     number   Token travel time per arrow in ms.                         650

   What the child does: presses "Next step" to send a glowing token along the arrows; each step lights
   up with its explanation; at a decision they choose the branch (Yes/No) themselves. "Auto" plays it
   all. Challenge tab: drag the shuffled step cards into the right order and press Check.
*/
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const PAL = ['#8b5cf6', '#3b82f6', '#2ed3a5', '#ff9f43', '#ff6b6b', '#14b8a6'];
  Labs.register('flowchart', {
    title: 'Process flow', subjects: ['science', 'social', 'civics', 'evs', 'maths'],
    render(host, p, api) {
      const ex = this.example || {};
      const nodes = (Array.isArray(p.nodes) && p.nodes.length ? p.nodes : ex.nodes).map((n, i) => ({ ...n, id: n.id != null ? String(n.id) : 'n' + i, k: i }));
      const byId = Object.fromEntries(nodes.map(n => [n.id, n]));
      let edges = Array.isArray(p.edges) && !(p.edges === ex.edges && p.nodes !== ex.nodes) ? p.edges : [];
      if (!edges || !edges.length) edges = nodes.slice(1).map((n, i) => ({ from: nodes[i].id, to: n.id }));
      edges = edges.map(e => ({ ...e, from: String(e.from), to: String(e.to) })).filter(e => byId[e.from] && byId[e.to]);
      const out = id => edges.filter(e => e.from === id);
      /* back-edge detection (DFS) and longest-path layering */
      const state = {}, back = new Set();
      const dfs = id => { state[id] = 1; out(id).forEach(e => { if (state[e.to] === 1) back.add(e); else if (!state[e.to]) dfs(e.to); }); state[id] = 2; };
      dfs(nodes[0].id); nodes.forEach(n => { if (!state[n.id]) dfs(n.id); });
      const fwd = edges.filter(e => !back.has(e));
      const layer = {}; nodes.forEach(n => layer[n.id] = 0);
      for (let it = 0; it < nodes.length; it++) fwd.forEach(e => { if (layer[e.to] < layer[e.from] + 1) layer[e.to] = layer[e.from] + 1; });
      const layers = []; nodes.forEach(n => { (layers[layer[n.id]] = layers[layer[n.id]] || []).push(n); });
      /* main path for arrange */
      const main = []; { let cur = nodes[0], guard = 0; while (cur && !main.includes(cur) && guard++ < 99) { main.push(cur); const o = out(cur.id).filter(e => !back.has(e)); cur = o.length ? byId[o[0].to] : null; } }
      const order = (Array.isArray(p.order) && p.order.length ? p.order.map(String).filter(id => byId[id]) : main.map(n => n.id));
      const task = p.task === 'play' ? 'play' : 'arrange', speed = +p.speed > 100 ? +p.speed : 650;

      host.innerHTML = `<div class="lb-flowchart-w"><style>
.lb-flowchart-w{font-size:14px;color:#1b1f3a;user-select:none;-webkit-user-select:none}
.lb-flowchart-ch{font-weight:800;font-size:14px;line-height:1.3;margin-bottom:6px}
.lb-flowchart-tabs{display:flex;gap:6px;margin-bottom:6px}
.lb-flowchart-tabs button{flex:1;min-height:40px;border:none;border-radius:12px;background:#eef0fb;color:#1b1f3a;font:inherit;font-weight:800;font-size:13px;cursor:pointer}
.lb-flowchart-tabs button.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-flowchart-sc{max-height:236px;overflow-y:auto;border-radius:16px;background:#f6f7ff;scroll-behavior:smooth}
.lb-flowchart-fl{position:relative}
.lb-flowchart-fl svg{position:absolute;left:0;top:0;pointer-events:none}
.lb-flowchart-n{position:absolute;height:46px;display:flex;align-items:center;gap:6px;padding:0 8px;background:#fff;border:2px solid #e3e6f7;border-radius:14px;font-weight:800;font-size:12.5px;line-height:1.15;cursor:pointer;transition:all .25s;box-shadow:0 2px 0 #e3e6f7;overflow:hidden}
.lb-flowchart-n .e{font-size:20px;flex:none}
.lb-flowchart-n .x{overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.lb-flowchart-n.dec{background:#fff8e1;border-color:#ffd66b;border-style:dashed}
.lb-flowchart-n.done{border-color:#c4b5fd;background:#f5f2ff}
.lb-flowchart-n.cur{border-color:#8b5cf6;border-style:solid;background:#8b5cf6;color:#fff;transform:scale(1.04);box-shadow:0 6px 16px rgba(139,92,246,.4)}
.lb-flowchart-el{font-size:10px;font-weight:800}
.lb-flowchart-info{display:flex;gap:10px;align-items:flex-start;background:#fff;border:2px solid #eef0fb;border-radius:14px;padding:7px 10px;margin-top:6px;min-height:58px;font-size:13px;line-height:1.3}
.lb-flowchart-info .e{font-size:26px;line-height:1}
.lb-flowchart-info b{display:block;font-size:14px}
.lb-flowchart-bar{display:flex;align-items:center;gap:8px;margin-top:6px;min-height:42px}
.lb-flowchart-msg{flex:1;font-weight:800;font-size:13.5px;line-height:1.25}
.lb-flowchart-bar button{min-height:42px;border:none;border-radius:12px;padding:0 12px;font:inherit;font-weight:800;cursor:pointer;background:#2ed3a5;color:#fff;box-shadow:0 3px 0 #1a9c78;white-space:nowrap}
.lb-flowchart-bar button.g{background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef}
.lb-flowchart-bar button.v{background:#8b5cf6;box-shadow:0 3px 0 #5b33c9}
.lb-flowchart-bar button.no{background:#ff6b6b;box-shadow:0 3px 0 #d84a4a}
.lb-flowchart-list{position:relative;touch-action:none}
.lb-flowchart-row{position:absolute;left:0;right:0;height:40px;display:flex;align-items:center;gap:8px;background:#fff;border:2px solid #e3e6f7;border-radius:12px;padding:0 10px;font-weight:800;font-size:13px;transition:top .18s ease,border-color .2s,background .2s;cursor:grab;box-shadow:0 2px 0 #e3e6f7}
.lb-flowchart-row.drag{transition:none;z-index:3;box-shadow:0 8px 20px rgba(27,31,58,.2);border-color:#8b5cf6;cursor:grabbing}
.lb-flowchart-row .h{color:#b6bad6}
.lb-flowchart-row .num{width:22px;height:22px;border-radius:50%;background:#eef0fb;display:grid;place-items:center;font-size:11.5px;flex:none}
.lb-flowchart-row .l{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lb-flowchart-row.ok{border-color:#2ed3a5;background:#effcf7}.lb-flowchart-row.ok .num{background:#2ed3a5;color:#fff}
.lb-flowchart-row.bad{border-color:#ff6b6b;background:#fff3f3}
.lb-flowchart-hint{color:#6b7090;font-weight:800;font-size:11.5px;margin:0 2px 4px}
@keyframes lb-flowchart-glow{0%,100%{r:7}50%{r:10}}
</style>
<div class="lb-flowchart-ch"></div>
<div class="lb-flowchart-tabs"><button data-t="p" class="on">▶ Play</button><button data-t="c">🎯 Challenge</button></div>
<div class="lb-flowchart-p"><div class="lb-flowchart-sc"><div class="lb-flowchart-fl"></div></div>
<div class="lb-flowchart-info"></div>
<div class="lb-flowchart-bar"><div class="lb-flowchart-msg"></div><span class="lb-flowchart-btns" style="display:flex;gap:6px"></span></div></div>
<div class="lb-flowchart-c" style="display:none"></div></div>`;
      const $ = s => host.querySelector(s);
      const sc = $('.lb-flowchart-sc'), fl = $('.lb-flowchart-fl'), info = $('.lb-flowchart-info'), msg = $('.lb-flowchart-p .lb-flowchart-msg'), btns = $('.lb-flowchart-btns'), cBox = $('.lb-flowchart-c');
      $('.lb-flowchart-ch').textContent = '🎯 Challenge: ' + (p.challenge || (task === 'arrange' ? `Put the ${order.length} steps in the right order` : 'Play the process all the way to the end'));
      const timers = [], NS = 'http://www.w3.org/2000/svg';
      let won = false, pos = {}, cur = null, visited = new Set(), moving = false, auto = false, raf = 0;
      const NH = 46, GAP = 30, TOP = 10;

      function layout() {
        const W = fl.clientWidth || sc.clientWidth || 340, hasBack = back.size > 0, RW = hasBack ? W - 30 : W;
        pos = {};
        layers.forEach((L, li) => {
          const n = L.length, gw = 8, w = Math.min(n === 1 ? 250 : 170, (RW - 16 - gw * (n - 1)) / n), tot = n * w + (n - 1) * gw, x0 = (RW - tot) / 2;
          L.forEach((nd, j) => { pos[nd.id] = { x: x0 + j * (w + gw), y: TOP + li * (NH + GAP), w, h: NH }; });
        });
        const H = TOP * 2 + layers.length * (NH + GAP) - GAP;
        fl.style.height = H + 'px';
        let s = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><defs><marker id="lb-fc-ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#9aa0c0"/></marker></defs>`;
        edges.forEach((e, i) => {
          const a = pos[e.from], b = pos[e.to]; let d, lx, ly;
          if (back.has(e)) { const x1 = a.x + a.w, y1 = a.y + NH / 2, x2 = b.x + b.w, y2 = b.y + NH / 2, xr = Math.min(W - 6, Math.max(x1, x2) + 24); d = `M${x1} ${y1} C${xr} ${y1} ${xr} ${y2} ${x2 + 3} ${y2}`; lx = xr - 6; ly = (y1 + y2) / 2; }
          else { const x1 = a.x + a.w / 2, y1 = a.y + NH, x2 = b.x + b.w / 2, y2 = b.y - 3, my = (y1 + y2) / 2; d = `M${x1} ${y1} C${x1} ${my} ${x2} ${my} ${x2} ${y2}`; lx = (x1 + x2) / 2; ly = my; }
          s += `<path id="lb-fc-e${i}" d="${d}" fill="none" stroke="#c9cde6" stroke-width="2.5" marker-end="url(#lb-fc-ar)"/>`;
          if (e.label) { const c = /^(yes|haan|हाँ|हां)/i.test(e.label) ? '#1a9c78' : /^(no|nahi|नहीं)/i.test(e.label) ? '#e04848' : '#6b7090'; s += `<rect x="${lx - 15}" y="${ly - 8}" width="30" height="15" rx="7" fill="#fff" stroke="${c}"/><text class="lb-flowchart-el" x="${lx}" y="${ly + 3.5}" text-anchor="middle" fill="${c}">${esc(String(e.label).slice(0, 5))}</text>`; }
        });
        s += `<circle class="tok" r="0" fill="#ffc93c" stroke="#fff" stroke-width="2" style="filter:drop-shadow(0 0 6px #ffc93c)"/></svg>`;
        s += nodes.map(n => { const q = pos[n.id]; return `<div class="lb-flowchart-n${n.type === 'decision' ? ' dec' : ''}${visited.has(n.id) ? ' done' : ''}${cur === n.id ? ' cur' : ''}" data-id="${esc(n.id)}" style="left:${q.x}px;top:${q.y}px;width:${q.w}px"><span class="e">${esc(n.emoji || (n.type === 'decision' ? '❓' : '•'))}</span><span class="x">${esc(n.text)}</span></div>`; }).join('');
        fl.innerHTML = s;
        fl.querySelectorAll('.lb-flowchart-n').forEach(d => d.addEventListener('click', () => { api.sfx('tap'); showInfo(byId[d.dataset.id]); }));
      }
      function showInfo(n) { info.innerHTML = `<div class="e">${esc(n.emoji || '•')}</div><div><b>${esc(n.text)}</b>${esc(n.info || '')}</div>`; }
      function mark() { fl.querySelectorAll('.lb-flowchart-n').forEach(d => { d.classList.toggle('cur', d.dataset.id === cur); d.classList.toggle('done', visited.has(d.dataset.id) && d.dataset.id !== cur); }); }
      function scrollTo(id) { const q = pos[id]; if (q) sc.scrollTop = Math.max(0, q.y - sc.clientHeight / 2 + NH / 2); }
      function arrive(id) {
        cur = id; visited.add(id); mark(); scrollTo(id); const n = byId[id]; showInfo(n); api.speak(n.text + (n.info ? '. ' + n.info : ''));
        const o = out(id);
        if (!o.length) { msg.textContent = '🏁 The end! Process complete.'; setBtns([['⟲ Again', 'g', restart]]); auto = false; if (task === 'play' && !won) { won = true; api.win('You followed the whole process to the end!'); } return; }
        if (o.length > 1) { msg.textContent = n.type === 'decision' ? 'You decide:' : 'Choose a path:'; auto = false; setBtns(o.map(e => [e.label || byId[e.to].text.slice(0, 10), /^(no|nahi|नहीं)/i.test(e.label || '') ? 'no' : '', () => go(e)])); return; }
        msg.textContent = back.size || edges.some(e => out(e.from).length > 1) ? `Step ${visited.size}` : `Step ${visited.size} of ${nodes.length}`;
        setBtns([['⟲', 'g', restart], [auto ? '⏸ Pause' : '⏩ Auto', 'v', toggleAuto], ['Next ▶', '', () => go(o[0])]]);
        if (auto) timers.push(setTimeout(() => { if (auto && cur === id) go(o[0]); }, 1400));
      }
      function go(e) {
        if (moving) return; moving = true; api.sfx('tap');
        const path = fl.querySelector('#lb-fc-e' + edges.indexOf(e)), tok = fl.querySelector('.tok'); if (!path) { moving = false; arrive(e.to); return; }
        const L = path.getTotalLength(), t0 = performance.now(); tok.setAttribute('r', 7);
        const step = t => { const k = Math.min(1, (t - t0) / speed), pt = path.getPointAtLength(L * (k < .5 ? 2 * k * k : 1 - (-2 * k + 2) ** 2 / 2)); tok.setAttribute('cx', pt.x); tok.setAttribute('cy', pt.y); if (pos[e.to] && k > .3) sc.scrollTop += ((pos[e.to].y - sc.clientHeight / 2) - sc.scrollTop) * .08; if (k < 1) raf = requestAnimationFrame(step); else { tok.setAttribute('r', 0); moving = false; arrive(e.to); } };
        raf = requestAnimationFrame(step);
      }
      function toggleAuto() { auto = !auto; const o = out(cur); if (auto && o.length === 1) go(o[0]); else arrive(cur); }
      function setBtns(list) { btns.innerHTML = ''; list.forEach(([t, c, f]) => { const b = document.createElement('button'); b.textContent = t; if (c) b.className = c; b.addEventListener('click', f); btns.appendChild(b); }); }
      function restart() { visited = new Set(); auto = false; cancelAnimationFrame(raf); moving = false; layout(); arrive(nodes[0].id); }

      /* ---- arrange challenge ---- */
      const ROW = 45; let ord = [], checked = false;
      function startArrange() {
        checked = false; const items = order.map(id => byId[id]); ord = items.slice();
        for (let t = 0; t < 6 && ord.every((n, i) => n === items[i]); t++) ord.sort(() => Math.random() - .5);
        cBox.innerHTML = `<div class="lb-flowchart-hint">⬆️ First step on top · drag ↕ to sort</div><div class="lb-flowchart-list" style="height:${ord.length * ROW}px"></div><div class="lb-flowchart-bar"><div class="lb-flowchart-msg">Drag the steps, then press Check.</div><button class="g sh">🔀</button><button class="ck">✔ Check</button></div>`;
        const list = cBox.querySelector('.lb-flowchart-list');
        ord.forEach(n => { const r = document.createElement('div'); r.className = 'lb-flowchart-row'; r.innerHTML = `<span class="h">⋮⋮</span><span class="num"></span><span>${esc(n.emoji || '•')}</span><span class="l">${esc(n.text)}</span>`; r._n = n; list.appendChild(r); });
        place();
        let drag = null;
        list.addEventListener('pointerdown', e0 => { const r = e0.target.closest('.lb-flowchart-row'); if (!r) return; drag = { r, y0: e0.clientY, top: ord.indexOf(r._n) * ROW }; r.classList.add('drag'); list.setPointerCapture && list.setPointerCapture(e0.pointerId); if (checked) { checked = false; list.querySelectorAll('.lb-flowchart-row').forEach(x => x.classList.remove('ok', 'bad')); } });
        list.addEventListener('pointermove', e2 => { if (!drag) return; const top = Math.max(-6, Math.min((ord.length - 1) * ROW + 6, drag.top + e2.clientY - drag.y0)); drag.r.style.top = top + 'px'; const want = Math.max(0, Math.min(ord.length - 1, Math.round(top / ROW))), at = ord.indexOf(drag.r._n); if (want !== at) { ord.splice(at, 1); ord.splice(want, 0, drag.r._n); place(drag.r); api.sfx('tap'); } });
        const end = () => { if (!drag) return; drag.r.classList.remove('drag'); drag = null; place(); };
        list.addEventListener('pointerup', end); list.addEventListener('pointercancel', end);
        cBox.querySelector('.sh').addEventListener('click', () => { api.sfx('tap'); startArrange(); });
        cBox.querySelector('.ck').addEventListener('click', () => {
          let ok = 0; checked = true;
          cBox.querySelectorAll('.lb-flowchart-row').forEach(r => { const i = ord.indexOf(r._n), good = order[i] === r._n.id; ok += good; r.classList.toggle('ok', good); r.classList.toggle('bad', !good); });
          const m = cBox.querySelector('.lb-flowchart-msg');
          if (ok === ord.length) { api.sfx('correct'); m.textContent = 'Perfect order! 🎉'; if (!won) { won = true; api.win(`You arranged all ${ord.length} steps in the right order!`); } }
          else { api.sfx('wrong'); m.textContent = `${ok} of ${ord.length} in place. Fix the red ones!`; }
        });
      }
      function place(skip) { cBox.querySelectorAll('.lb-flowchart-row').forEach(r => { const i = ord.indexOf(r._n); r.querySelector('.num').textContent = i + 1; if (r !== skip) r.style.top = i * ROW + 'px'; }); }
      function tab(t) {
        host.querySelectorAll('.lb-flowchart-tabs button').forEach(b => b.classList.toggle('on', b.dataset.t === t));
        $('.lb-flowchart-p').style.display = t === 'p' ? '' : 'none'; cBox.style.display = t === 'c' ? '' : 'none';
        auto = false; if (t === 'c') startArrange(); else { layout(); mark(); }
      }
      host.querySelectorAll('.lb-flowchart-tabs button').forEach(b => b.addEventListener('click', () => { api.sfx('tap'); tab(b.dataset.t); }));
      layout(); arrive(nodes[0].id); sc.scrollTop = 0;
      const onResize = () => { if ($('.lb-flowchart-p').style.display !== 'none') { layout(); mark(); } };
      window.addEventListener('resize', onResize);
      return () => { timers.forEach(clearTimeout); cancelAnimationFrame(raf); auto = false; window.removeEventListener('resize', onResize); };
    },
    example: {
      title: 'How a bill becomes a law', task: 'arrange',
      challenge: 'Put the 6 steps of law-making in the right order',
      nodes: [
        { id: 'a', emoji: '📝', text: 'Bill introduced in Parliament', info: 'A minister or member proposes a new law, called a Bill.' },
        { id: 'b', emoji: '🗣️', text: 'Debate in first House', info: 'Members discuss it, may send it to a committee, and suggest changes.' },
        { id: 'c', emoji: '🗳️', text: 'Passed by majority?', type: 'decision', info: 'Members vote. If most say yes, it goes ahead.' },
        { id: 'x', emoji: '🗑️', text: 'Bill falls', info: 'If it is not passed, it does not become a law.' },
        { id: 'd', emoji: '🏛️', text: 'Same steps in other House', info: 'Lok Sabha and Rajya Sabha both must pass the Bill.' },
        { id: 'e', emoji: '✍️', text: 'President gives assent', info: 'The President signs the Bill.' },
        { id: 'f', emoji: '📕', text: 'Bill becomes an Act (law)', info: 'It is printed in the Gazette and must be followed.' }
      ],
      edges: [{ from: 'a', to: 'b' }, { from: 'b', to: 'c' }, { from: 'c', to: 'd', label: 'Yes' }, { from: 'c', to: 'x', label: 'No' }, { from: 'd', to: 'e' }, { from: 'e', to: 'f' }]
    },
    examples: [
      { title: 'Scientific method (Class 6-8)', task: 'arrange', challenge: 'Arrange the steps of the scientific method',
        nodes: [{ id: 'q', emoji: '❓', text: 'Ask a question', info: 'Why do plants bend toward the window?' },
          { id: 'h', emoji: '💡', text: 'Make a guess (hypothesis)', info: 'Plants grow toward light.' },
          { id: 't', emoji: '🧪', text: 'Do an experiment', info: 'Keep one plant in a box with a hole, one in the open.' },
          { id: 'o', emoji: '👀', text: 'Observe and record', info: 'Write down what happens each day.' },
          { id: 'c', emoji: '🤔', text: 'Does the result match the guess?', type: 'decision', info: 'Compare your results with your hypothesis.' },
          { id: 'k', emoji: '📢', text: 'Share the conclusion', info: 'Tell others what you found.' }],
        edges: [{ from: 'q', to: 'h' }, { from: 'h', to: 't' }, { from: 't', to: 'o' }, { from: 'o', to: 'c' }, { from: 'c', to: 'k', label: 'Yes' }, { from: 'c', to: 'h', label: 'No' }] },
      { title: 'Journey of food (Class 7)', task: 'play', challenge: 'Press Next and follow the food all the way through',
        nodes: [{ id: 'm', emoji: '👄', text: 'Mouth', info: 'Teeth chew; saliva starts breaking down starch.' },
          { id: 'f', emoji: '🥤', text: 'Food pipe (oesophagus)', info: 'Muscles push the food down.' },
          { id: 's', emoji: '🫃', text: 'Stomach', info: 'Acid and juices digest proteins.' },
          { id: 'i', emoji: '🌀', text: 'Small intestine', info: 'Digestion completes; nutrients are absorbed into blood.' },
          { id: 'l', emoji: '💧', text: 'Large intestine', info: 'Water and salts are absorbed.' },
          { id: 'r', emoji: '🚽', text: 'Rectum & anus', info: 'Undigested waste leaves the body.' }], edges: [] }
    ]
  });
})();
